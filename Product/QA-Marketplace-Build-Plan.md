# QA Mastery Talent — Fullstack Delivery Plan

> The executable build plan that ties together the PRD, UX, Architecture, Data-Engineering, and Design-System docs. Stack validation, an honest quality baseline, the milestone-by-milestone MVP delivery, testing, and CI/CD.

**Status:** v1.0 · **Profile:** `saas-startup` (validated) · **Surface:** web-first inside `apps/platform`

---

## 0. Assumptions surfaced (skill discipline — Karpathy #1)

The four required assumptions, from project context (not guessed):

| Assumption | Value | Source |
|---|---|---|
| Team size today → 12mo | **1 → ~2** (solo founder, dev-light) | `qa-mastery-marketing` memory |
| Deployment cadence | **Daily / continuous** (Vercel; "ship #1 weekly" + push-to-deploy) | marketing system |
| Audience | **Customer-facing** marketplace | PRD §0 |
| Monthly cloud + SaaS ceiling | **~$0 (free tiers)**: Supabase + Vercel | $0-organic constraint |
| Data sensitivity | **PII-only** (profiles, messages; no payments in MVP) | PRD §4, §5 |
| Traffic (yr-1 p99) | **Low** (< ~10 rps) | early-stage estimate |

## 0.1 Stack decision — VALIDATED by the decision engine

`fullstack_decision_engine.py` with the above inputs → **`saas-startup`, 100% fit**:
> `next-app-router-postgres` · **modular monolith** · Tailwind · Postgres · hosting Vercel + Supabase.

This is an **independent confirmation of Architecture ADR-001** — the engine reached the same conclusion we designed, from first principles. No stack change. Anti-patterns it flags for this profile (all already avoided in our docs): premature microservices, premature queues/Redis, a separate API server. **Defer Redis/queue until measured need** — matches Data-Eng §0.

## 0.2 Verifiable success criteria (skill requirement — three numeric targets)

Every recommendation must ship measurable SLOs. For Talent on free-tier Vercel + Supabase:

| Layer | Metric | Target | Measured by |
|---|---|---|---|
| **API** (Server Actions / route handlers) | p50 / p95 / p99 | **150 / 400 / 800 ms** (warm; excl. cold start). Directory query **p95 < 300 ms** | Supabase logs + Vercel analytics |
| **Frontend** (mobile-4G) | LCP / INP / CLS | **< 2.5 s / < 200 ms / < 0.1** | Vercel Speed Insights / Lighthouse CI |
| **Availability** | Uptime SLO | **99.5%** (inherits Vercel + Supabase; realistic at free tier) | uptime check on `/api/health` |

These become the **launch gate** alongside the UX gate (client reaches a relevant tester in < 3 min, > 80% task success).

---

## 1. Quality baseline — honest reporting

I ran `code_quality_analyzer.py` against the existing platform. **The headline "28/100, Grade F" is a measurement artifact, not the codebase's real state** — reported transparently:

| Analyzer claim | Reality (verified) |
|---|---|
| "0 dependencies" | I scoped it to `apps/platform/src`; the root + app `package.json` (19 deps) sit a level up. False. |
| "1% test coverage" | Real tests live in `packages/*/test`, `e2e/tests`, and `pnpm test:rls` — outside the scanned path. Coverage is *not* 1%. |
| "No README/LICENSE" | Both exist at the repo root, outside scope. |
| **"3 High SQL-injection"** | **Verified false positives.** The regex flags `select`/`delete` near template literals; the actual hits are a JSX `<select>` (`test-case-form.tsx:30`) and a `querySelectorAll(\`.${RING}\`)` (`locator-lab.tsx:70`) — DOM/React, not SQL. All DB access is the parameterized Supabase client + RLS. **No SQL injection exists.** |

**Real quality posture** (from the architecture analyzers earlier): 0 circular deps, coupling 0/100, feature-based App Router, passing typecheck, RLS test suite, Playwright e2e, SOC2-minded `audit_events`. **Healthy.** The only genuine, actionable signal: one file > 500 lines (`learn/actions.ts`, 591) — pre-existing, not blocking.

**Standard for the marketplace code we add:** keep `talent/actions.ts` focused (split if > ~400 lines), add RLS tests + e2e for every new flow (§4), and don't regress the perf budget (§0.2).

---

## 2. MVP scope (locked from PRD §4 Phase 1)

Tester profiles (skills + device matrix + portfolio), verified-skill import, client project posting, QA-native directory + filters, consent-gated Realtime messaging, moderation basics. **Out:** payments/escrow, reviews, mobile, AI matching, automated assessments.

---

## 3. Delivery milestones (executable order)

Each milestone is independently shippable behind the `talent` feature flag. File paths match existing conventions.

### M0 — Foundation (schema + flag)
- `supabase/migrations/20260621000017_talent.sql` — all `talent_*` tables, RLS (3 archetypes from Arch §5), GIN/trigram indexes, `profiles.talent_role`, `talent_messages` → realtime publication, `analytics.*` views + `dq_checks()` + guarded `pg_cron` jobs (Data-Eng §7).
- Feature flag + middleware gate for `/talent/*`.
- `lib/talent/events.ts` (`emitTalentEvent` + Zod contracts, Data-Eng §1).
- **DoD:** migration applies; `pnpm test:rls` green incl. new negative tests (non-participant can't read a conversation; `analytics`/`audit_events` deny-all to anon/authenticated).

### M1 — Tester profile + portfolio
- Routes: `(app)/talent/onboarding`, `(app)/talent/profile`, `(app)/talent/u/[handle]`.
- Server Actions in `talent/actions.ts`: `upsertTesterProfile`, `setAvailability`, `addPortfolioItem` (incl. the **reuse picker** linking existing `bug_reports`/`test_cases`, Arch ADR-003), Storage signed-URL minting.
- `getPublicProfile()` via the `security definer` projection view (no PII leak).
- Components (Design-System §2): profile editor, `DeviceChip`, `PortfolioArtifactCard`, `ProfileStrengthMeter`, `VerifiedBadge`.
- **DoD:** a tester builds a public profile + adds one artifact in < 10 min (UX usability target); emits `profile_published`.

### M2 — Verified-skills pipeline
- `syncVerifiedSkills(userId)` (PATH A) wired into the grading/certificate write path; `analytics.reconcile_verified_skills()` (PATH B) on `pg_cron` (Data-Eng §3). Idempotent upsert; `talent_sync_state` watermark.
- **DoD:** flip a graded score → badge appears (A) and survives nightly re-derive (B); `dq_checks` freshness check green.

### M3 — Client posting + directory
- Routes: `(app)/talent/post` (guided `PostProjectWizard`), `(app)/talent/testers` (`TesterDirectory`), `(app)/talent/projects/[id]`.
- `searchTesters(filters)` — Postgres GIN array-overlap + trigram (Arch ADR-005); rule-based ranking (verified > specialty > recency).
- Components: `TesterCard`, `ProjectCard`, `FacetChip`/`FilterGroup`, **`EmptyState`** (cold-start — launch-blocking, Design-System §2.3).
- **DoD:** client filters to a relevant tester in < 3 min, > 80% success; never an empty/irrelevant grid; emits `project_posted` / `application_submitted`.

### M4 — Connect + Realtime messaging
- `contactTester()` (creates `talent_conversations`, consent boundary), `sendMessage()` (emits `message_sent`, derives `connection_made` — Data-Eng §1).
- `(app)/talent/inbox` — Postgres Changes subscription on `talent_messages` (RLS-authorized) + Broadcast typing (Arch ADR-002); `MessageBubble`, `ConversationThread`.
- **DoD:** message delivered live between two browsers; non-participant RLS negative test passes; `weekly_connected_pairs` increments.

### M5 — Moderation + applications
- `reportContent()` (insert-own, service-role triage), `applyToProject()`, application status management.
- Rate limits on signup/posting (reuse existing rate-limit util in `lib/help-agent/rate-limit.ts` as the pattern).
- **DoD:** report reaches the service-role queue; rate limit blocks abuse.

### M6 — Launch gate
- Seed supply (graduates) **before** opening the directory (cold-start, UX §2B).
- Verify all §0.2 SLOs + UX gates. Flip the flag for a cohort.

---

## 4. Testing strategy (reuse the existing harness)

| Layer | Tool (already in repo) | New for Talent |
|---|---|---|
| **RLS / data** | `pnpm test:rls` (`packages/db`) | participant-only messaging; `is_public` profile visibility; NDA artifact hidden; `analytics`/`audit_events` deny-all |
| **Unit** | `turbo test` per package | Zod event contracts; `searchTesters` filter builder; status→tone map |
| **E2E** | Playwright (`e2e/tests`) | tester onboarding→publish; client post→filter→contact; realtime delivery between two contexts |
| **Perf** | Lighthouse CI / Vercel Speed Insights | enforce §0.2 LCP/INP/CLS budget on `/talent/testers` |
| **Type** | `pnpm typecheck` | must stay green |

## 5. CI/CD (existing workflows)
- `ci.yml` → typecheck + lint + unit + RLS on every PR (add the new RLS/e2e specs).
- `deploy-staging.yml` / `deploy.yml` → Vercel preview per PR, prod on merge (push-to-deploy = the daily cadence).
- `security.yml` → keep; the false-positive SQL flags above are **not** from this pipeline.
- **Migration safety:** single additive migration; apply via Supabase MCP, record in `schema_migrations` so `db push` stays clean (Arch §6).

---

## 6. Risks to delivery (fullstack lens)

| Risk | Mitigation |
|---|---|
| Cold-start empty directory kills the client journey | M6 seeds supply first; `EmptyState` is launch-blocking |
| Realtime RLS misconfig leaks messages | M4 ships with the non-participant negative RLS test as a gate |
| `talent/actions.ts` bloats like `learn/actions.ts` (591 lines) | Split by domain (profile / projects / messaging) from the start |
| Free-tier limits (Supabase connections, Vercel function duration) | Keyset pagination, indexed queries (§0.2), defer Redis until measured |
| Solo founder bandwidth | Milestones are independently shippable behind the flag; no big-bang launch |

---

## 7. One-paragraph summary

The decision engine independently confirmed the stack we designed (`saas-startup` → Next.js modular monolith on Postgres, Vercel + Supabase, 100% fit). The existing codebase is healthy — the analyzer's "Grade F" and three "SQL-injection" findings were verified as scoping artifacts and regex false positives (a JSX `<select>` and a DOM `querySelectorAll`), not real defects. The marketplace ships as six independently-deployable milestones behind a `talent` feature flag, reusing the existing auth, RLS test harness, Playwright e2e, CI/CD, and design primitives — gated on concrete SLOs (API p95 < 400 ms, directory p95 < 300 ms, LCP < 2.5 s, 99.5% uptime) and the UX success criteria. **M0 (the single `20260621000017_talent.sql` migration + RLS tests) is the first executable step.**
