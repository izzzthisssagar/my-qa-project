# QA Mastery Talent — Backend Spec (M0 migration + API contract)

> The backend implementation spec: the complete `talent` migration (schema + RLS + indexes), the Server-Action API contract, security hardening, and performance/RPO-RTO targets. Ready to drop into the repo on go-ahead.

**Status:** v1.0 · **Pattern:** modular monolith, Server Actions (no standalone API service) · **DB:** Supabase Postgres + RLS

---

## 0. Assumptions + engine validation (skill discipline)

| Backend assumption | Value | Notes |
|---|---|---|
| Read/write ratio + p99 QPS | **~20:1**, p99 **< 10 QPS** | marketplace = browse-heavy |
| Tenancy | **shared-multi-tenant**, isolated by **RLS** | one DB, row-level isolation |
| Data sensitivity | **PII** (profiles, messages) — no PCI/PHI in MVP | payments deferred to V1.0 |
| Pattern | **modular monolith** | Arch ADR-001 |

`backend_decision_engine.py` → **modular-monolith on Postgres, shared-multi-tenant, PII tier, defer Redis/queue** (fit 100%). **Framework caveat (honest):** the engine assumes a *standalone* API service (FastAPI/Express). We deliberately diverge — the backend is **Next.js Server Actions colocated in `apps/platform`** (the fullstack `saas-startup` profile). The engine's *transferable* guidance — pattern, data tier, defer Redis — holds; its framework pick does not apply to a Server-Action backend.

### Verifiable criteria (latency + SLO + RPO/RTO — all three required)
| | Target |
|---|---|
| Latency p50 / p95 / p99 | **150 / 400 / 800 ms** (directory read p95 **< 300 ms**) |
| Uptime SLO | **99.5%** (named error-budget consumer: the founder) |
| **RPO** | **≤ 24 h** (Supabase daily backups, free tier); **≤ 5 min** when PITR is enabled (paid) |
| **RTO** | **≤ 4 h** (restore from Supabase backup; stateless app redeploys from Vercel instantly) |

---

## 1. The migration — `supabase/migrations/20260621000017_talent.sql`

Conventions copied from `…_feedback.sql` / `…_audit_events.sql`: lowercase SQL, `(select auth.uid())`, named indexes `table_cols`, guarded extensions, explanatory comments.

```sql
-- 0017 — talent: the QA freelance/job marketplace module.
--
-- Two-sided: testers (supply) publish QA-native profiles + proof artifacts;
-- clients (demand) post projects and contact testers. Messaging is gated by an
-- explicit consent boundary (a conversation row) and enforced in RLS, never the
-- UI. Verified-skill badges are a service-role-written snapshot of grading data
-- (see analytics.reconcile_verified_skills). PII (email/phone) NEVER enters a
-- talent_* table or any public view — contact happens only via talent_messages.

create extension if not exists pg_trgm;  -- fuzzy name/headline search

-- ── profiles: opt into a marketplace role ────────────────────────────────────
alter table public.profiles
  add column if not exists talent_role text not null default 'none'
    check (talent_role in ('none', 'tester', 'client', 'both'));

-- ── tester profile (1:1 with profiles, opt-in) ───────────────────────────────
create table public.talent_profiles (
  id uuid primary key references public.profiles (id) on delete cascade,
  handle text not null unique check (handle = lower(handle) and char_length(handle) between 3 and 32),
  headline text check (char_length(headline) <= 120),
  bio text check (char_length(bio) <= 2000),
  location text,
  timezone text,
  langs text[] not null default '{}',
  availability text not null default 'open'
    check (availability in ('open', 'busy', 'not_looking')),
  rate_cents integer check (rate_cents is null or rate_cents >= 0),
  discipline text not null default 'both'
    check (discipline in ('manual', 'automation', 'both')),
  specialties text[] not null default '{}',  -- validated against taxonomy in app (Zod)
  stack text[] not null default '{}',
  is_public boolean not null default false,
  verification_status text not null default 'unverified'
    check (verification_status in ('unverified', 'pending', 'verified')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- ── device matrix ────────────────────────────────────────────────────────────
create table public.talent_devices (
  id uuid primary key default gen_random_uuid(),
  tester_id uuid not null references public.talent_profiles (id) on delete cascade,
  kind text not null check (kind in ('mobile', 'desktop', 'tablet')),
  device text not null,
  os text,
  os_version text,
  browser text,
  created_at timestamptz not null default now()
);

-- ── portfolio: curation layer over existing artifacts OR net-new items ────────
create table public.talent_portfolio_items (
  id uuid primary key default gen_random_uuid(),
  tester_id uuid not null references public.talent_profiles (id) on delete cascade,
  type text not null check (type in ('bug_report', 'test_case', 'automation', 'coverage', 'other')),
  -- when linking a reused artifact (Arch ADR-003); null for net-new external items
  source_table text check (source_table in ('bug_reports', 'test_cases', 'capstone_submissions')),
  source_id uuid,
  title text not null check (char_length(title) <= 160),
  body text check (char_length(body) <= 8000),
  repo_url text,
  asset_path text,                        -- Supabase Storage object path (signed on read)
  is_nda boolean not null default false,
  created_at timestamptz not null default now(),
  check ((source_id is null) = (source_table is null))  -- both or neither
);

-- ── verified skills: service-role snapshot of grading (SCD type 1) ───────────
create table public.talent_verified_skills (
  id uuid primary key default gen_random_uuid(),
  tester_id uuid not null references public.talent_profiles (id) on delete cascade,
  skill text not null,
  score smallint check (score between 0 and 100),
  source text not null check (source in ('lab', 'certificate')),
  earned_at timestamptz not null,
  updated_at timestamptz not null default now(),
  unique (tester_id, skill)               -- idempotent upsert key
);

-- singleton reconcile watermark (Data-Eng §3.2)
create table public.talent_sync_state (
  id boolean primary key default true check (id),  -- single row
  last_reconciled_at timestamptz
);
insert into public.talent_sync_state (id, last_reconciled_at) values (true, null)
  on conflict do nothing;

-- ── projects (client postings) ───────────────────────────────────────────────
create table public.talent_projects (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null references public.profiles (id) on delete cascade,
  title text not null check (char_length(title) between 3 and 160),
  description text check (char_length(description) <= 8000),
  project_type text not null
    check (project_type in ('web', 'mobile', 'api', 'game', 'desktop', 'embedded', 'other')),
  stack text[] not null default '{}',
  required_types text[] not null default '{}',
  engagement text not null check (engagement in ('one_off', 'ongoing', 'full_time')),
  budget_cents integer check (budget_cents is null or budget_cents >= 0),
  tooling text[] not null default '{}',
  nda_required boolean not null default false,
  status text not null default 'open' check (status in ('open', 'closed')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- ── applications (tester → project) ──────────────────────────────────────────
create table public.talent_applications (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references public.talent_projects (id) on delete cascade,
  tester_id uuid not null references public.profiles (id) on delete cascade,
  status text not null default 'applied'
    check (status in ('applied', 'shortlisted', 'declined', 'hired')),
  note text check (char_length(note) <= 2000),
  created_at timestamptz not null default now(),
  unique (project_id, tester_id)
);

-- ── conversations (the consent boundary) ─────────────────────────────────────
create table public.talent_conversations (
  id uuid primary key default gen_random_uuid(),
  client_id uuid not null references public.profiles (id) on delete cascade,
  tester_id uuid not null references public.profiles (id) on delete cascade,
  project_id uuid references public.talent_projects (id) on delete set null,
  created_by uuid not null references public.profiles (id),
  created_at timestamptz not null default now(),
  unique (client_id, tester_id, project_id),
  check (client_id <> tester_id)
);

-- ── messages (Realtime; immutable) ───────────────────────────────────────────
create table public.talent_messages (
  id uuid primary key default gen_random_uuid(),
  conversation_id uuid not null references public.talent_conversations (id) on delete cascade,
  sender_id uuid not null references public.profiles (id) on delete cascade,
  body text not null check (char_length(body) between 1 and 8000),
  attachments jsonb not null default '[]'::jsonb,
  read_at timestamptz,
  created_at timestamptz not null default now()
);

-- ── shortlists & reports ─────────────────────────────────────────────────────
create table public.talent_shortlists (
  client_id uuid not null references public.profiles (id) on delete cascade,
  tester_id uuid not null references public.talent_profiles (id) on delete cascade,
  created_at timestamptz not null default now(),
  primary key (client_id, tester_id)
);

create table public.talent_reports (
  id uuid primary key default gen_random_uuid(),
  reporter_id uuid not null references public.profiles (id) on delete set null,
  target_type text not null check (target_type in ('profile', 'project', 'message')),
  target_id uuid not null,
  reason text not null check (char_length(reason) between 1 and 2000),
  status text not null default 'new' check (status in ('new', 'reviewing', 'actioned', 'dismissed')),
  created_at timestamptz not null default now()
);
```

### 1.1 Indexes (skill's index strategy — equality, composite, partial, GIN, trigram)
```sql
-- directory: array-overlap filters (specialties && $1, stack && $1)
create index talent_profiles_specialties_gin on public.talent_profiles using gin (specialties);
create index talent_profiles_stack_gin       on public.talent_profiles using gin (stack);
-- directory: only public rows, newest first (partial + covering-ish)
create index talent_profiles_public on public.talent_profiles (updated_at desc) where is_public;
-- fuzzy name/headline
create index talent_profiles_handle_trgm   on public.talent_profiles using gin (handle gin_trgm_ops);
create index talent_profiles_headline_trgm on public.talent_profiles using gin (headline gin_trgm_ops);
create index talent_devices_tester on public.talent_devices (tester_id);
create index talent_portfolio_tester on public.talent_portfolio_items (tester_id);
create index talent_verified_tester on public.talent_verified_skills (tester_id);
-- projects directory
create index talent_projects_open on public.talent_projects (created_at desc) where status = 'open';
create index talent_projects_reqtypes_gin on public.talent_projects using gin (required_types);
create index talent_applications_project on public.talent_applications (project_id, status);
create index talent_applications_tester  on public.talent_applications (tester_id);
-- messaging hot paths (composite — the participant lookup + thread order)
create index talent_conversations_client on public.talent_conversations (client_id, tester_id);
create index talent_messages_convo on public.talent_messages (conversation_id, created_at desc);
create index talent_reports_status on public.talent_reports (status, created_at desc);
```

### 1.2 RLS — three archetypes (Arch §5)
```sql
alter table public.talent_profiles        enable row level security;
alter table public.talent_devices         enable row level security;
alter table public.talent_portfolio_items enable row level security;
alter table public.talent_verified_skills enable row level security;
alter table public.talent_projects        enable row level security;
alter table public.talent_applications    enable row level security;
alter table public.talent_conversations   enable row level security;
alter table public.talent_messages        enable row level security;
alter table public.talent_shortlists      enable row level security;
alter table public.talent_reports         enable row level security;
alter table public.talent_sync_state      enable row level security;  -- no policy = service-role only

-- (a) public-read / owner-write — profile
create policy "read public or own profile" on public.talent_profiles for select
  using (is_public = true or (select auth.uid()) = id);
create policy "owner writes own profile" on public.talent_profiles for all
  using ((select auth.uid()) = id) with check ((select auth.uid()) = id);

-- devices & portfolio: visible if the PARENT profile is visible to the caller; NDA hides portfolio
create policy "read devices via visible parent" on public.talent_devices for select
  using (exists (select 1 from public.talent_profiles p
                 where p.id = tester_id and (p.is_public or (select auth.uid()) = p.id)));
create policy "owner writes own devices" on public.talent_devices for all
  using ((select auth.uid()) = tester_id) with check ((select auth.uid()) = tester_id);

create policy "read non-nda portfolio via visible parent" on public.talent_portfolio_items for select
  using (exists (select 1 from public.talent_profiles p
                 where p.id = tester_id and (p.is_public or (select auth.uid()) = p.id))
         and (not is_nda or (select auth.uid()) = tester_id));
create policy "owner writes own portfolio" on public.talent_portfolio_items for all
  using ((select auth.uid()) = tester_id) with check ((select auth.uid()) = tester_id);

-- verified skills: public read, service-role write only (no insert/update/delete policy)
create policy "anyone reads verified skills" on public.talent_verified_skills for select using (true);

-- projects: public read when open, owner writes
create policy "read open or own projects" on public.talent_projects for select
  using (status = 'open' or (select auth.uid()) = owner_id);
create policy "owner writes own projects" on public.talent_projects for all
  using ((select auth.uid()) = owner_id) with check ((select auth.uid()) = owner_id);

-- applications: project owner OR the applying tester
create policy "owner or applicant reads application" on public.talent_applications for select
  using ((select auth.uid()) = tester_id
         or exists (select 1 from public.talent_projects pr
                    where pr.id = project_id and pr.owner_id = (select auth.uid())));
create policy "tester submits own application" on public.talent_applications for insert
  with check ((select auth.uid()) = tester_id);
create policy "owner updates application status" on public.talent_applications for update
  using (exists (select 1 from public.talent_projects pr
                 where pr.id = project_id and pr.owner_id = (select auth.uid())));

-- (b) participant-only — conversations + messages (the security-critical pair)
create policy "participants read conversation" on public.talent_conversations for select
  using ((select auth.uid()) in (client_id, tester_id));
create policy "creator opens conversation" on public.talent_conversations for insert
  with check ((select auth.uid()) = created_by
              and (select auth.uid()) in (client_id, tester_id));

create policy "participants read messages" on public.talent_messages for select
  using (exists (select 1 from public.talent_conversations c
                 where c.id = conversation_id and (select auth.uid()) in (c.client_id, c.tester_id)));
create policy "participants send as self" on public.talent_messages for insert
  with check ((select auth.uid()) = sender_id
              and exists (select 1 from public.talent_conversations c
                          where c.id = conversation_id and (select auth.uid()) in (c.client_id, c.tester_id)));
-- read_at updated via a scoped RPC (mark_read), not a broad UPDATE policy.

-- shortlists: owner only
create policy "owner manages shortlist" on public.talent_shortlists for all
  using ((select auth.uid()) = client_id) with check ((select auth.uid()) = client_id);

-- (c) insert-own / service-role-triage — reports (copies feedback pattern)
create policy "users file own reports" on public.talent_reports for insert
  with check ((select auth.uid()) = reporter_id);
-- no select/update policy: triage is service-role only.
```

### 1.3 Realtime + scheduled jobs (guarded like existing migrations)
```sql
-- Realtime: messages must be in the publication + full replica identity so the
-- conversation_id filter is available on the change payload.
do $$
begin
  alter table public.talent_messages replica identity full;
  alter publication supabase_realtime add table public.talent_messages;
exception when others then
  raise notice 'supabase_realtime publication unavailable — add talent_messages in cloud';
end $$;

do $$
begin
  create extension if not exists pg_cron;
  perform cron.schedule('reconcile-verified-skills', '30 3 * * *',
    $q$select analytics.reconcile_verified_skills()$q$);
exception when others then
  raise notice 'pg_cron unavailable — verified-skills reconcile skipped (enable in Supabase cloud)';
end $$;
```

### 1.4 Public-profile projection view (no PII; Arch ADR-003/006)
```sql
-- Serves /talent/u/[handle]: only public columns, joins linked artifacts read-only.
create or replace view public.talent_public_profile
with (security_invoker = true) as
select p.id, p.handle, p.headline, p.bio, p.location, p.timezone, p.langs,
       p.availability, p.rate_cents, p.discipline, p.specialties, p.stack,
       p.verification_status, p.updated_at
from public.talent_profiles p
where p.is_public;   -- RLS still applies (security_invoker); email/phone never selected
```

> **`analytics.reconcile_verified_skills()` and `analytics.dq_checks()`** are defined in the analytics schema (Data-Eng §3–4). The reconcile body must join the **real grading/progress/certificate tables** (`progress`, `quiz_attempts`, certificates) — left as a documented TODO here because those columns weren't verified in this pass; wire against the actual schema, keep it `security definer`, service-role-granted.

---

## 2. Server-Action API contract

RPC-style (not REST) — each is a typed Server Action in `talent/actions.ts`. Uniform result shape:

```ts
type ActionResult<T> =
  | { ok: true; data: T }
  | { ok: false; error: { code: ErrorCode; message: string; fields?: Record<string,string> } };
// ErrorCode: 'UNAUTHENTICATED'|'FORBIDDEN'|'VALIDATION'|'NOT_FOUND'|'CONFLICT'|'RATE_LIMITED'|'INTERNAL'
```

| Action | Input (Zod) | AuthZ | Returns | Emits |
|---|---|---|---|---|
| `upsertTesterProfile` | profile fields; `specialties`/`stack` ∈ taxonomy | self | `talent_profiles` row | — |
| `setAvailability` | `'open'\|'busy'\|'not_looking'` | self | ok | — |
| `addDeviceRow` / `removeDeviceRow` | device fields | self (owner) | row / ok | — |
| `addPortfolioItem` | type, optional `(source_table, source_id)`, title/body/repo/asset, is_nda | self; if linking, must own the source artifact | item | — |
| `publishProfile` | `is_public: boolean` | self; require ≥1 specialty & profile completeness | ok | `talent.profile_published` |
| `getPublicProfile` | `handle` | public | view row + non-NDA portfolio + badges | — |
| `searchTesters` | filters: specialties[], stack[], deviceReal?, availability?, rateMax?, verifiedOnly?, cursor | public | page (keyset) | — |
| `postProject` | project fields | client/both | project | `talent.project_posted` |
| `applyToProject` | `project_id`, note | tester/both | application | `talent.application_submitted` |
| `setApplicationStatus` | `application_id`, status | project owner | ok | `talent.hire_marked` (if hired) |
| `contactTester` | `tester_id`, `project_id?` | client/both; upsert conversation | conversationId | `talent.contact_initiated` |
| `sendMessage` | `conversation_id`, body, attachments? | participant | message | `talent.message_sent` (+ derive `connection_made`) |
| `markRead` | `conversation_id` | participant | ok | — |
| `shortlistTester` / `unshortlist` | `tester_id` | client | ok | — |
| `reportContent` | target_type, target_id, reason | authed | ok | `talent.reported` |

**Validation:** every input parsed with Zod at the top of the action; failure → `{ ok:false, error:{ code:'VALIDATION', fields } }`. **AuthZ is defense-in-depth:** the action checks role/ownership *and* RLS enforces it at the DB — a bug in one is caught by the other. **PII:** no action ever returns `auth.users.email/phone`.

---

## 3. Security hardening (skill's workflow, adapted to Supabase/Server Actions)

| Control | Implementation |
|---|---|
| **AuthN** | Supabase Auth (`@supabase/ssr`), existing — no custom JWT. |
| **AuthZ** | **RLS is the authorization layer** (server-truth) + action-level role checks. The participant-only message policy is the keystone (§1.2b). |
| **Rate limiting** | Reuse `lib/help-agent/rate-limit.ts` pattern on write actions: `contactTester`, `sendMessage`, `postProject`, `reportContent` (e.g. N/15min). Returns `RATE_LIMITED`. |
| **Input validation** | Zod on every action; `text[]` taxonomy validated against an allow-list (not free text) before insert. |
| **File uploads** | Private buckets `talent-portfolio`, `talent-avatars`; validate MIME + size; **signed URLs minted in a Server Action only after an ownership/visibility check**; NDA items never get a public signed URL. |
| **PII boundary** | email/phone confined to `auth.users`; public view (§1.4) + every action exclude them; contact only via `talent_messages`. |
| **Audit** | Sensitive actions write `audit_events` (existing), feeding analytics + a forensic trail. |
| **Security headers / CSP** | inherited from the existing Next.js app config — no change. |

---

## 4. Performance & reliability

- **N+1 avoidance:** directory render fetches profiles + their top badges/devices via a single query with `lateral`/aggregation, not per-card round-trips. `getPublicProfile` batches portfolio + badges + devices in parallel.
- **Pagination:** **keyset** (`where updated_at < $cursor`) on the partial `talent_profiles_public` index — stable under inserts, O(1) deep pages (vs OFFSET).
- **Index proof:** every directory/messaging query must show `Index Scan` (not `Seq Scan`) under `EXPLAIN ANALYZE` before launch.
- **Load test (skill's `api_load_tester.py`):** against a Vercel preview of `/talent/testers` and the `sendMessage` path — `--concurrency 50 --duration 30`; assert p95 < targets (§0) and that rate limits return 429 under burst. (Run post-deploy; can't load-test Server Actions pre-deploy.)
- **RPO/RTO:** Supabase managed backups (RPO ≤24h free / ≤5min PITR paid; RTO ≤4h). App is stateless → instant Vercel redeploy. Messages are the only loss-sensitive data; PITR recommended before scale.

---

## 5. Test gates (extend `pnpm test:rls`)
Negative RLS tests that MUST pass before M0 is done:
1. A non-participant **cannot** `select` a conversation's messages.
2. A user **cannot** `insert` a message into a conversation they're not in (even with a forged `sender_id`).
3. A non-owner **cannot** read another tester's **NDA** portfolio item or a non-public profile.
4. `anon`/`authenticated` get **zero** rows from `analytics.*`, `audit_events`, `talent_reports`, `talent_sync_state`.
5. A tester **cannot** link a portfolio item to a `source_id` they don't own.

---

## 6. Next step
This SQL is complete and convention-matching. On your go-ahead I'll write it to **`qa-mastery/supabase/migrations/20260621000017_talent.sql`** and the negative RLS tests to `packages/db/test`, then you (or I, with DB access) apply via Supabase MCP and run `pnpm test:rls`. I held off writing it directly because applying a migration to the live DB is consequential — your call on timing.
```
