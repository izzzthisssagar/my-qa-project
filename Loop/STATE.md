---
type: loop-state
updated: 2026-07-21 (second/.claude-second session)
updated_by: claude (second session)
---

# STATE.md — durable loop state

Single source of truth for loop progress. Update at the end of every cycle
(step 7). Narrative detail stays in `../Claude Coordination.md`; this file
holds only current counters, claims, and backlog.

## Curriculum progress (48 map modules, `Curriculum/generator-master-map.py`)

**MAP COMPLETE — 906/906 topics, 0 `planned:true` leaves remain, across all
57 taxonomy modules.** (Note: the approved-map's 48-module count and the live
taxonomy's 57-module count diverge slightly — extra modules were scaffolded
beyond the original 48 over the course of the build. Either way: nothing left
unwritten.)

- This session (second/.claude-second) picked up from the point recorded in
  the prior STATE.md snapshot (77 `planned:true` topics remaining) and closed
  every remaining gap:
  - `interviews` 16/16, `your-first-90-days` 16/16 — written from scratch.
  - `api-and-modern-security` 20/20 — `auditing-buggyapi` (4/4) written from
    scratch; `jwt-and-token-attacks` (4/4) inherited from the other live
    session (drafted, left uncommitted when it hit its usage limit) and
    independently re-verified in full before committing.
  - `test-management-and-reporting` 20/20 — `risk-and-estimation` (4/4) also
    inherited from the other session the same way, same re-verification.
  - Also fixed a pre-existing bug found at session start: 24 taxonomy leaves
    across 3 modules had shipped content but were never flipped off
    `planned: true` (the flip step got skipped in earlier commits).
- Full session commit range on `feat/notes-v2`: `10fd8de..4941883` (10
  commits). All local gates green throughout: mdx compile 906/906, images
  ok, components ok, full monorepo typecheck 12/12, curriculum test suite
  9/9, `pnpm lint` 0 errors, all 3 app builds (platform 994 pages, buggyshop
  16, buggyapi 8) clean, bug-manifest-secrecy invariant clean.

## Active claims

None. Nothing left in the map to claim.

## Push / deploy state — DONE

- `feat/notes-v2` pushed to `origin/feat/notes-v2`, then fast-forward merged
  into `main` and pushed. GitHub push protection caught one real issue along
  the way: a curriculum code example used a Stripe-key-shaped fake secret
  (`sk_live_9f2a...`) realistic enough to trigger secret scanning — fixed via
  a targeted interactive rebase on the originating commit (unpushed, so safe
  to rewrite), replaced with the `FAKE_EXAMPLE_KEY_NNN` style already used
  safely elsewhere in the corpus, verified the pedagogical output (`OK` vs.
  `TOO WEAK` verdict) was unchanged.
- Post-push, the `security` CI job failed on a real `pnpm audit` finding
  (high-severity js-yaml quadratic-CPU DoS, transitive via
  `gray-matter@4.0.3` — unmaintained, pinned to `js-yaml ^3.13.1`). Fixed
  with a scoped `pnpm-workspace.yaml` override pinning only the vulnerable
  range to the patched `3.15.0` (not the `4.x` line — verified by hand that
  js-yaml v4 removes the `safeLoad`/`safeDump` API gray-matter calls, which
  would have silently broken all frontmatter parsing; caught this before
  trusting a clean audit run). Re-pushed, `security` job now green.
- `Deploy to Vercel` succeeded for all 3 apps (platform, buggyshop, buggyapi)
  + the `buggyapi-ws` Fly.io service. Spot-checked a live notes URL post-
  deploy — 307 to `/login` as expected (auth-gated route, not an error).
- `CI` workflow (lint/typecheck/unit/curriculum-sync/build/manifest-leak/e2e)
  was running at the time this file was last updated — check
  `gh run list --branch main` for current status before assuming it's green.

## Loop status

- Sole active session at time of this update; the other live session
  (`~/.claude`, per the standing parallel-session setup) had also hit its
  usage limit, which is why its `jwt-and-token-attacks` and
  `risk-and-estimation` work was sitting uncommitted and got inherited here.
- `codex` worktrees (`automation-foundations`, `selenium-webdriver-ch1`,
  `non-functional-testing-intro`) still hold now-fully-redundant merged
  content — safe to prune whenever Sajan does a cleanup pass, not touched
  this session either.

## Branch/push state

- `feat/notes-v2` and `main` both pushed to `origin`, in sync as of this
  update.
- Shared checkout still holds untracked `demo.txt`/`implementation_plan.md`/
  `task.md`/`.superpowers/`/`packages/curriculum/scripts/__pycache__/` —
  pre-existing junk, left untouched throughout (per standing convention).
- `.worktrees/automation-foundations`, `.worktrees/selenium-webdriver-ch1`,
  `.worktrees/non-functional-testing-intro`, `.worktrees/redis-caching-bugs`
  — redundant/superseded, safe to prune, not touched this session.
- Vault sync: `qa-mastery/packages/curriculum/scripts/sync-notes-to-vault.mjs`
  re-run this session — `Notes/` in the vault now mirrors all 906 notes
  (was 666, stale since the last sync predating this session's work).
