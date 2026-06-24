# QA Mastery Talent — Spec Suite Index

> A two-sided QA freelance & job marketplace, built as a module inside the existing QA Mastery platform. This is the entry point to the full specification: eleven cross-referenced docs taking the product from positioning to RLS policies, CI gates, and a test suite. Plus the first executable step (M0) now in the repo.

**One-liner:** the hiring layer for QA — testers showcase real proof (bug reports, automation scripts, device matrix, verified-from-labs badges); developers/companies filter on QA-native signals and contact them. Web-first, free at launch, inside `apps/platform` on the existing Next.js + Supabase + Vercel stack.

---

## Read in this order

| # | Doc | Lens | Read it for |
|---|---|---|---|
| 1 | [PRD](./QA-Marketplace-PRD.md) | Product | personas, features, entities, MVP→V1.0 roadmap, risks |
| 2 | [UX Research](./QA-Marketplace-UX-Research.md) | UX | proto-personas, journey maps, the validation research plan |
| 3 | [Architecture](./QA-Marketplace-Architecture.md) | System design | component model, ER diagram, **6 ADRs**, RLS strategy |
| 4 | [Data Engineering](./QA-Marketplace-Data-Engineering.md) | Data | event spine, North-Star metric, verified-skills pipeline, data quality |
| 5 | [Design System](./QA-Marketplace-Design-System.md) | UI | status tokens, components, WCAG contrast, dark-first brand |
| 6 | [Build Plan](./QA-Marketplace-Build-Plan.md) | Fullstack delivery | stack validation, SLOs, M0–M6 milestones |
| 7 | [Backend Spec](./QA-Marketplace-Backend-Spec.md) | Backend | **the full migration SQL** + Server-Action API contract |
| 8 | [Frontend Spec](./QA-Marketplace-Frontend-Spec.md) | Frontend | mixed rendering, Server/Client boundary map, perf budget |
| 9 | [Security Spec](./QA-Marketplace-Security-Spec.md) | Security | threat model, OWASP Top 10, GDPR for global PII |
| 10 | [DevOps Spec](./QA-Marketplace-DevOps-Spec.md) | DevOps | CI gates, additive-migration release, rollback runbook |
| 11 | [Test Plan](./QA-Marketplace-Test-Plan.md) | QA | RLS tests, E2E (incl. realtime), requirements→tests matrix |

---

## The decisions that shaped it

- **Module, not new app** (Arch ADR-001) — shares auth, Paddle, DB, design system; the talent pool is open to anyone with verifiable QA experience, with graduates fast-tracked via lab-verified badges.
- **Reuse existing artifacts** (Arch ADR-003) — the platform already stores `bug_reports` / `test_cases` / `capstone_submissions`; graduates get an instant portfolio.
- **Consent boundary + PII in RLS** (Arch ADR-006, Sec §1) — no message without a conversation row; email/phone never leave `auth.users`.
- **Realtime via Supabase Postgres Changes** (Arch ADR-002) — RLS-authorized, no new infra.
- **Right-sized everywhere** — rejected Kafka/Airflow/Snowflake (Data-Eng), Terraform/K8s (DevOps); validated the stack with each skill's decision engine.
- **Free at launch** — build two-sided liquidity first (PRD); monetize (Paddle escrow/featured/subscription) in V1.0.

## The North Star
**Weekly Connected Pairs** — a client and tester who exchange ≥2 messages (real intent), emitted as a first-class `talent.connection_made` event. Not raw signups.

---

## M0 — first executable step (in the repo)

The migration and its security tests are written and ship together:

| File | What |
|---|---|
| `qa-mastery/supabase/migrations/20260621000017_talent.sql` | all `talent_*` tables, RLS (3 archetypes), GIN/trigram indexes, `profiles.talent_role`, realtime publication, `analytics.*` views + `dq_checks()` + guarded `pg_cron`, the PII-safe public-profile view |
| `qa-mastery/packages/db/test/talent-rls.test.ts` | the 5 negative RLS invariants (the launch gate) |

**Status:** files written, **not yet applied**. To validate + apply:
1. `pnpm exec supabase start` (CI does this too) → migration applies locally.
2. `pnpm --filter @qa-mastery/db test:rls` → the 5 invariants must pass.
3. Cloud: apply via Supabase MCP `execute_sql` + record in `schema_migrations` at `20260621000017` (the feedback-migration pattern), or enable the staging deploy secrets so `deploy-staging.yml` runs `supabase db push`.

**One TODO carried forward:** `analytics.reconcile_verified_skills()` ships as a watermark-only stub — wire it to the real grading/progress/certificate tables to populate `talent_verified_skills` (Backend §1, Data-Eng §3).

## What's next (M1→M6)
Tester profile + portfolio → verified-skills pipeline → client posting + directory → Realtime messaging → moderation → feature-flagged launch (seed graduates before opening the directory). Full sequence in the [Build Plan](./QA-Marketplace-Build-Plan.md) §3.
