# QA Mastery Talent — DevOps & Release Spec

> Companion to the Backend/Frontend/Security specs. CI gates, migration deployment, release strategy, observability, and rollback — for the **managed-serverless** stack the project actually runs on.

**Status:** v1.0 · **Platform:** Vercel + Supabase + GitHub Actions · **Principle:** extend the existing pipeline; no new infra.

---

## 0. Right-sizing — what this skill offers vs. what we use

This skill centers on Docker / Kubernetes / Terraform / ECS / blue-green. **None of it applies here** and I deliberately do **not** use the `terraform_scaffolder`, `deployment_manager` (K8s), or container pipeline generators. The stack is fully managed serverless:

| Skill default | Our reality |
|---|---|
| Docker image build/push | **None** — Vercel builds from source |
| K8s blue-green / readiness gates | **Vercel atomic immutable deploys** — a broken build never goes live; instant promote-previous rollback (native) |
| Terraform / ECS / VPC | **Supabase + Vercel managed** — no IaC to write |
| Self-run Postgres | **Supabase** (backups, PITR, pg_cron managed) |

Recording this so it's revisited only if the project ever leaves managed serverless — which, for a solo founder at $0, it should not.

**The existing pipeline is already strong** (verified by reading the workflows): `ci.yml` (lint/typecheck/unit/curriculum/Supabase-migrations/e2e), `deploy.yml` (atomic Vercel prod, auto last-good rollback), `deploy-staging.yml` (applies migrations via `supabase db push`, guarded), `security.yml` (**gitleaks + `pnpm audit --prod` already present** — the secops recommendation is *already done*), and `/api/health` (DB readiness probe, 503 on failure, minimal body). Marketplace work = **extend**, not rebuild.

---

## 1. Environments & promotion

```
local (supabase start, applies migrations)         ← dev: real local stack, ci.yml mirrors it
   │  PR → Vercel Preview deploy (per-branch URL)   ← test the talent feature in isolation
   ▼
staging (qa-mastery-staging: rnmxbtokqebkqibsjmrt)  ← deploy-staging.yml: supabase db push on merge
   ▼
production (Vercel prod alias, on push to main)     ← deploy.yml; /talent gated by feature flag
```

- **Preview deploys** (Vercel's Git integration) give every PR a live URL — exercise `/talent/*` end-to-end before merge.
- **Feature flag** is the real production safety net: `/talent` ships dark and is exposed per-cohort, decoupled from deploys (§3).

---

## 2. CI gates (extend `ci.yml` + `security.yml`)

Add to the existing jobs (do not fork new workflows):

| Gate | Where | New for Talent |
|---|---|---|
| Lint / Typecheck / Unit | `ci.yml` (exists) | new action/component unit tests |
| **RLS tests** (`pnpm test:rls`) | `ci.yml` | **the 5 negative tests** (Backend §5) — the access-control launch gate |
| E2E (Playwright) | `ci.yml` (exists) | onboarding→publish; post→filter→contact; **realtime delivery across two browser contexts** |
| Bundle budget | `ci.yml` (add) | `bundle_analyzer.py` ≥ 90; fail on new heavy dep |
| Lighthouse (perf/a11y) | `ci.yml` (add) | perf ≥ 90 on `/talent/u/[handle]`, a11y ≥ 95 — Frontend SLOs |
| Secret scan (gitleaks) | `security.yml` (**exists**) | nothing — already covers new files |
| Dep audit (`pnpm audit --prod`) | `security.yml` (**exists**) | nothing |

CI mirrors prod: it boots a **real local Supabase and applies migrations**, so `20260621000017_talent.sql` is exercised on every PR (a bad migration fails CI, not prod).

---

## 3. Migration deployment & release strategy

### 3.1 The migration path is already built
`deploy-staging.yml` runs `supabase db push` on merge to main → `20260621000017_talent.sql` applies to staging automatically **once the deploy secrets are set** (currently guarded/inert). Required (from infra backlog):
- Secrets: `SUPABASE_ACCESS_TOKEN`, `STAGING_SERVICE_ROLE_KEY`
- Vars: `SUPABASE_PROJECT_REF` (`rnmxbtokqebkqibsjmrt`), `STAGING_SUPABASE_URL`
- Also pending (dashboard-only): Supabase Auth **Site URL + `/auth/callback` redirect allowlist**; weekly-action secrets `SUPABASE_URL` / `SERVICE_ROLE_KEY` / `NOTIFY_WEBHOOK`.

> For the live DB (already used for the feedback table), apply `20260621000017_talent.sql` via Supabase MCP `execute_sql` and record it in `supabase_migrations.schema_migrations` at version `20260621000017` so `db push` stays clean — the exact pattern used for the feedback migration.

### 3.2 Expand/contract discipline (the safety property)
`deploy.yml` (app) and `deploy-staging.yml` (migration) both fire on push to main, **in parallel** — so the app could deploy before the migration applies. This is **safe here because the migration is strictly additive**:
- New `talent_*` tables — unused by old code.
- One **nullable** `profiles.talent_role` column (default `'none'`) — backward-compatible; old code ignores it.
- The **feature flag gates `/talent`**, so even mid-deploy the marketplace is invisible.

**Rule:** only **additive** migrations reach `main`. Any future destructive change (drop/rename) follows expand → migrate → contract across two releases. Never a breaking migration in one shot.

### 3.3 Progressive release (no blue-green needed)
Vercel deploys are atomic; the marketplace rollout is controlled by the **feature flag**, not infra:
1. **Dark launch** — code in prod, flag off.
2. **Seed supply** — enable for QA Mastery graduates only (cold-start fix, UX §2B).
3. **Cohort** — enable for an invited client cohort; watch `weekly_connected_pairs` + SLOs.
4. **General** — flip on for all.
Each step is a config change, **no redeploy**, instantly reversible.

---

## 4. Observability (golden signals, managed tools)

| Signal | Source (mostly existing) |
|---|---|
| **Latency** | Vercel Analytics (API) + Speed Insights (CWV) — enforce Frontend/Backend SLOs |
| **Traffic** | Vercel + `analytics.*` product views (Data-Eng §2) |
| **Errors** | Vercel runtime logs; `ActionResult` error codes; (optional) Sentry |
| **Saturation** | Supabase dashboard (connections, CPU), `get_advisors` for RLS/index gaps |
| **Uptime** | external monitor on **`/api/health`** (exists) — 503 when DB down |
| **Data quality** | `analytics.dq_checks()` → `NOTIFY_WEBHOOK` (Data-Eng §4) |
| **Audit/abuse** | `audit_events` stream; alert on report/contact spikes |

Add a `/talent`-aware note to the health story: `/api/health` already proves DB reachability, which covers the marketplace (same Postgres). No new probe needed.

---

## 5. Rollback runbook (serverless — three layers, fastest first)

| Failure | Action | Speed |
|---|---|---|
| Marketplace misbehaving (bug, abuse, bad UX) | **Flip the feature flag off** — no deploy | **seconds** |
| Bad app deploy | **Vercel: promote previous deployment** (instant alias swap) or revert the commit | seconds–1 min |
| Bad data (not schema) | **Supabase PITR** restore (enable on paid tier; free = ≤24h backup) | minutes–hours |
| Bad migration | migrations are **forward-only + additive** → write a **compensating migration**; never edit history. Additive design means most "bad migrations" are inert, not breaking | one release |

**RPO ≤ 24h** (free backups) / **≤ 5 min** (PITR, recommend before scale). **RTO ≤ 4h** — app is stateless (instant Vercel redeploy); only message data is loss-sensitive → PITR is the lever.

---

## 6. Pre-launch ops checklist
- [ ] Staging deploy secrets set → `deploy-staging.yml` applies `20260621000017_talent.sql` to staging
- [ ] Live DB: migration applied via MCP + recorded in `schema_migrations`
- [ ] CI extended: `test:rls` (5 negative tests), `/talent` e2e, bundle + Lighthouse gates green
- [ ] Feature flag wired; dark-launch verified in prod (flag off = `/talent` 404/redirect)
- [ ] External uptime monitor on `/api/health`; Vercel Speed Insights on
- [ ] `dq_checks()` cron + `NOTIFY_WEBHOOK` alerting live
- [ ] Rollback drill done: flag-kill tested; Vercel promote-previous tested
- [ ] PITR enabled (or accept ≤24h RPO at launch, documented)

---

## 7. Summary
The deployment platform is already chosen and managed (Vercel + Supabase), and the existing pipeline already does atomic deploys with auto-rollback, staged DB migrations, secret scanning, dependency audit, and a health probe — so I explicitly skipped this skill's Docker/K8s/Terraform tooling. Marketplace delivery is **additive migrations + feature-flagged progressive rollout**: the single `20260621000017_talent.sql` flows through the existing `deploy-staging.yml` path, the app ships dark behind a flag, and the flag (not blue-green) drives seed→cohort→general exposure with a seconds-fast kill switch. Rollback is three layers (flag → Vercel promote-previous → Supabase PITR), and CI gains the marketplace's RLS/e2e/perf gates. **Enabling the staging deploy secrets is the one infra prerequisite before M0 ships.**
