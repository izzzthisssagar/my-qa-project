# QA Mastery Talent — Data Engineering Design

> Companion to the PRD, UX, and Architecture docs. Covers the data-flow concerns: the verified-skills sync **pipeline**, the marketplace **metrics/analytics layer** (North Star + funnel), **data quality & contracts**, and **orchestration** — all right-sized for a solo founder on Supabase.

**Status:** v1.0 · **Principle:** ELT-in-place on Postgres. No Kafka, no Airflow, no Snowflake.

---

## 0. The right-sizing decision (most important section)

A senior data engineer's first job is to **not** over-build. Running the skill's decision framework against this context:

| Decision | Framework signal | Choice for Talent |
|---|---|---|
| **Batch vs streaming** | "Real-time insight required?" → marketplace *metrics* tolerate daily latency; the only real-time need is *messaging*, which is OLTP (Supabase Realtime, already designed in Architecture ADR-002), not analytics. | **Batch** for analytics. |
| **Volume** | < 1 TB/day (orders of magnitude under) — thousands of rows/day at launch. | **Warehouse compute = the OLTP Postgres itself.** No Spark. |
| **Warehouse vs lakehouse** | BI/SQL on structured data, no ML training pipeline, no unstructured lake. | **Neither** — a guarded `analytics` schema of views *in the same Postgres*. |
| **Orchestration** | One cron-able sync + nightly checks; solo operator. | **`pg_cron` + GitHub Actions**, not Airflow/Dagster. |
| **Lambda/Kappa** | No dual batch+stream codebase needed. | **Single path** (ELT-in-place). |

> The skill ships `pipeline_orchestrator.py` that *can* emit an Airflow DAG (`--type airflow --destination snowflake`). I am **deliberately not using it** — introducing Airflow + a warehouse for a few thousand daily events would be negative ROI and ops burden the founder can't carry. This is the engineering decision, recorded so it's revisited only when volume justifies it (see §6 escape hatch).

**The whole data platform:**
```
OLTP (talent_* tables, RLS)  ──events──►  audit_events (append-only spine)
        │                                          │
        │ pg_cron / GH Actions (batch ELT)         │
        ▼                                          ▼
  talent_verified_skills (read-model)      analytics.* views (metrics)
        ▲                                          │
        └──── grading events (CDC) ───────┘   service-role only → founder dashboard
```

---

## 1. Event instrumentation — one spine, `audit_events`

The platform already has an append-only, service-role-only `audit_events(actor_id, action, target, metadata jsonb, created_at)`. **Reuse it as the single event spine** — do not add a parallel analytics-events table. The marketplace just emits new `action` values from its Server Actions (same place entitlement/score events are already emitted).

### Canonical event taxonomy (data contract)

Each event is a row; `metadata` carries a **versioned, validated** payload. Emit from `talent/actions.ts` via the service role.

| `action` | Emitted when | Required `metadata` (contract v1) |
|---|---|---|
| `talent.role_selected` | onboarding role chosen | `{ "role": "tester\|client\|both" }` |
| `talent.profile_published` | tester sets `is_public=true` | `{ "tester_id", "specialties_count", "devices_count", "portfolio_count" }` |
| `talent.project_posted` | client posts | `{ "project_id", "required_types": [], "engagement" }` |
| `talent.application_submitted` | tester applies | `{ "project_id", "tester_id" }` |
| `talent.contact_initiated` | conversation created | `{ "conversation_id", "client_id", "tester_id", "from": "directory\|project" }` |
| `talent.message_sent` | message inserted | `{ "conversation_id", "sender_role": "client\|tester" }` |
| `talent.connection_made` | 2nd reply in a convo (both sides spoke) | `{ "conversation_id" }` |
| `talent.hire_marked` | application → hired | `{ "project_id", "tester_id" }` |
| `talent.reported` | content reported | `{ "target_type", "target_id" }` |

**Contract enforcement:** a single `emitTalentEvent(action, metadata)` helper (in `lib/talent/events.ts`) Zod-validates `metadata` against the action before insert. Invalid payload = throw in dev/CI, log + drop in prod (never block the user action). This is the **data contract at the producer** — the cheapest place to guarantee quality.

> `connection_made` is derived: the `sendMessage` action checks "has the other participant already sent ≥1 message in this conversation?" and, if this crosses the threshold and no `connection_made` exists yet, emits it. This makes the North Star a first-class event, not a fragile after-the-fact SQL guess.

---

## 2. Metrics layer — `analytics` schema views

Extend the existing guarded `analytics` schema (service-role-only; never exposed to anon/authenticated — the documented leak guard). Conceptually this is a tiny **star**: `audit_events` is the fact stream; `profiles` / `talent_projects` are dimensions. At this scale, **views over the fact stream are the implementation** (no materialization until a view gets slow — §6).

### 2.1 North Star — Weekly Connected Pairs
```sql
-- A "connected pair" = a conversation where BOTH sides have spoken (real intent),
-- counted in the week it connected. NOT raw signups.
create or replace view analytics.weekly_connected_pairs as
select date_trunc('week', created_at)::date as week,
       count(*) as connected_pairs
from public.audit_events
where action = 'talent.connection_made'
group by 1
order by 1 desc;
```

### 2.2 The two-sided funnel (where users drop)
```sql
-- Supply funnel: signup → picked tester → published → got contacted → connected.
create or replace view analytics.tester_funnel as
with t as (
  select p.id,
    exists(select 1 from public.talent_profiles tp where tp.id = p.id)                     as has_profile,
    exists(select 1 from public.talent_profiles tp where tp.id = p.id and tp.is_public)    as is_public,
    exists(select 1 from public.talent_conversations c where c.tester_id = p.id)           as contacted,
    exists(select 1 from public.audit_events e
           join public.talent_conversations c on c.id = (e.metadata->>'conversation_id')::uuid
           where e.action='talent.connection_made' and c.tester_id = p.id)                 as connected
  from public.profiles p
  where p.talent_role in ('tester','both')
)
select count(*) as testers,
       count(*) filter (where has_profile) as built_profile,
       count(*) filter (where is_public)   as published,
       count(*) filter (where contacted)   as got_contacted,
       count(*) filter (where connected)   as connected
from t;
```
(Mirror `analytics.client_funnel`: posted-or-browsed → filtered → contacted → connected → hired.)

### 2.3 Marketplace health — liquidity & speed
```sql
create or replace view analytics.marketplace_liquidity as
select
  (select count(*) from public.talent_profiles where is_public)                       as active_testers,
  (select count(*) from public.talent_projects where status='open')                   as open_projects,
  (select count(*) from public.talent_conversations
     where created_at > now() - interval '7 days')                                     as contacts_7d,
  -- median hours from project post to its first application (demand→supply speed)
  (select percentile_cont(0.5) within group (order by extract(epoch from (a.created_at - pr.created_at))/3600)
     from public.talent_applications a
     join public.talent_projects pr on pr.id = a.project_id)                           as median_hrs_to_first_application;
```

| Metric | View | Why it matters (UX/PRD link) |
|---|---|---|
| Weekly Connected Pairs | `weekly_connected_pairs` | North Star (PRD §0) — real intent, not vanity |
| Supply/demand funnels | `tester_funnel`, `client_funnel` | Confirms/refutes the UX "Valley of Death" (UX §2) |
| Time-to-first-contact / application | `marketplace_liquidity` | Cold-start health (UX §2B, PRD §5) |
| Active testers : open projects | `marketplace_liquidity` | Liquidity balance — when to push which side |

All reachable **only** via service role → feeds the founder dashboard, never the public API.

---

## 3. The one real pipeline — verified-skills sync (ADR-004 operationalized)

`talent_verified_skills` is a denormalized **read-model** fed from the grading/certificate domain. This is the only component with genuine data-pipeline concerns (CDC, idempotency, freshness, reconciliation). Modeled as **SCD Type 1** (overwrite current state; keep `earned_at` for "when first achieved").

### 3.1 Dual-path: event-driven + scheduled reconcile (belt and suspenders)
```
PATH A (fresh):  grading writes a passing score / certificate
                 → existing server action ALSO calls syncVerifiedSkills(userId)
                 → service-role UPSERT into talent_verified_skills
                   ON CONFLICT (tester_id, skill) DO UPDATE … (idempotent)

PATH B (correct): pg_cron nightly job re-derives ALL badges from source of truth
                 and reconciles drift (catches missed events, backfills, removes
                 revoked badges). Source of truth always wins.
```

### 3.2 Idempotency & correctness
- **Upsert key** `(tester_id, skill)` → re-running PATH A or B never duplicates. Safe to retry.
- **PATH B is the truth**: a full re-derive from grading means a missed event in PATH A self-heals within 24h — no fragile exactly-once machinery needed (we get *eventually-correct* cheaply).
- **Watermark:** PATH B records `last_reconciled_at` in a tiny `talent_sync_state` row; alert if it goes stale (§4).
- **DLQ-lite:** if PATH A's sync throws, it must **not** break the user's grading action — wrap in try/catch, log a `talent.sync_failed` audit event with the `userId`; PATH B sweeps it up. No separate queue infra.

### 3.3 Scheduled job (pg_cron, guarded exactly like existing retention jobs)
```sql
do $$
begin
  create extension if not exists pg_cron;
  perform cron.schedule('reconcile-verified-skills', '30 3 * * *',
    $q$select analytics.reconcile_verified_skills()$q$);  -- service-role fn, full re-derive
exception when others then
  raise notice 'pg_cron unavailable — verified-skills reconcile skipped (enable in Supabase cloud)';
end $$;
```
*(Same guarded pattern as `prune-audit-events` in `…_analytics_and_retention.sql`, so `db:reset` never breaks locally/CI.)*

**Why not a trigger on the grading tables?** A Postgres trigger would couple grading writes to marketplace schema and run inside the grading transaction (risk: a marketplace bug rolls back a learner's score). The Server-Action call (PATH A) + nightly reconcile (PATH B) keeps the domains decoupled — consistent with Architecture ADR-004.

---

## 4. Data quality & contracts

Quality is enforced at **three layers**, cheapest-first:

**Layer 1 — Constraints (in the migration, free & always-on):**
`handle citext unique`, `unique(client_id, tester_id, project_id)` on conversations, FK `on delete cascade`, `check` on enums/ranges, `not null` on event-critical columns. Most "bad data" is impossible by construction.

**Layer 2 — Producer contracts (§1):** `emitTalentEvent` Zod-validates every event payload before insert. Schema = the contract.

**Layer 3 — Scheduled assertions (the "data quality validator", done in SQL):** a service-role function `analytics.dq_checks()` run by `pg_cron` (or the existing GH Actions weekly cadence) that returns failing checks; non-empty result → POST to the existing `NOTIFY_WEBHOOK` (already wired for the marketing feedback job).

| Dimension | Check (example) | Action on fail |
|---|---|---|
| **Freshness** | `talent_sync_state.last_reconciled_at > now() - interval '36 hours'` | alert — pipeline stalled |
| **Completeness** | no `talent_messages` row whose `conversation_id` has no `talent_conversations` parent | alert — orphan (should be impossible via FK; this catches drift) |
| **Uniqueness** | no duplicate public `handle` (defense-in-depth over the constraint) | alert |
| **Validity** | every `audit_events.action like 'talent.%'` row has its contract-required `metadata` keys | alert — producer bug |
| **Consistency** | `talent_verified_skills` count per user == re-derived count from grading | alert — drift between read-model and truth |

```sql
-- sketch: returns one row per failing check; empty = healthy
create or replace function analytics.dq_checks()
returns table(check_name text, failures bigint) language sql security definer as $$
  select 'stale_verified_skills_sync',
         (select count(*) from public.talent_sync_state
          where last_reconciled_at < now() - interval '36 hours')
  union all
  select 'orphan_messages',
         (select count(*) from public.talent_messages m
          left join public.talent_conversations c on c.id = m.conversation_id
          where c.id is null)
  -- … remaining checks …
  ;
$$;
```

---

## 5. Orchestration & DataOps

| Concern | Implementation (reuse existing) |
|---|---|
| **Scheduling** | `pg_cron` for in-DB jobs (reconcile, retention, DQ); GitHub Actions cron for anything needing egress (e.g. webhook alert), matching the existing weekly marketing-feedback workflow. |
| **Lineage** | Linear and documented: `Server Actions → audit_events → analytics.* views`; `grading → syncVerifiedSkills → talent_verified_skills`. No tool needed; this doc *is* the lineage. |
| **CI/CD for data** | RLS + schema changes ship via the same migration flow; `pnpm test:rls` already exists — add a test asserting `analytics.*` and `audit_events` are **deny-all** to anon/authenticated (the leak guard) and that `dq_checks()` runs clean on seed data. |
| **Retention** | Extend the existing pruning block: keep `audit_events` 180d (already set). Marketplace events live in the same table, so they inherit it — but **roll weekly North-Star / funnel counts into a tiny `analytics.metrics_daily` snapshot table** before pruning, so history survives the 180-day cut. |
| **Incident response** | DQ alert → `NOTIFY_WEBHOOK`. Runbook: stale sync → run `reconcile_verified_skills()` manually; drift → trust PATH B (re-derive); orphan/contract failures → check the offending Server Action. |
| **Observability** | Supabase logs + `get_advisors` (RLS/index gaps) + the `analytics.*` views as the product KPIs surface. |

---

## 6. Scale escape hatch (when to revisit)

Right-sized now ≠ stuck. Triggers to graduate the stack, in order:

1. **A view gets slow** (directory/funnel p95 > target) → convert the hot view to a **materialized view** refreshed by `pg_cron`; add covering indexes. (Still all Postgres.)
2. **`audit_events` write contention or > ~10M rows** → partition by month (`pg_partman`) and/or roll up aggressively into `metrics_daily`.
3. **Founder wants BI/self-serve exploration** → nightly `COPY`/logical-replication of `analytics.*` into **BigQuery free tier** or DuckDB; introduce **dbt** for the metric models *only then* (the views in §2 are already dbt-model-shaped, so this is a lift-and-shift).
4. **Event volume → real streaming need** (unlikely for a hiring marketplace) → only then consider Kafka/Kinesis. Until a metric demands sub-minute latency, this stays out.

Each step is a clean, reversible upgrade — and none is needed to launch.

---

## 7. Build order (data-engineering slice)

1. In `20260621000017_talent.sql`: add `talent_verified_skills`, `talent_sync_state`, the `analytics.*` views (§2), `analytics.reconcile_verified_skills()`, `analytics.dq_checks()`, and the guarded `pg_cron` jobs.
2. `lib/talent/events.ts`: `emitTalentEvent` with per-action Zod contracts (§1); wire into every Server Action.
3. `syncVerifiedSkills(userId)` (PATH A) called from the grading/certificate write path; reconcile fn (PATH B).
4. Extend `pnpm test:rls`: assert `analytics`/`audit_events` deny-all; assert `dq_checks()` clean on seed.
5. Add a `metrics_daily` rollup + a DQ-alert step to a GH Actions weekly job (clone the marketing-feedback workflow).

**Verification:** seed a fake connected pair → confirm `analytics.weekly_connected_pairs` increments; flip a grading score → confirm a badge appears via PATH A and survives PATH B; break a contract payload → confirm `dq_checks()` flags it and the webhook fires; confirm anon/authenticated get **zero** rows from `analytics.*`.
