---
type: loop-definition
created: 2026-07-18
model: https://github.com/cobusgreyling/loop-engineering
participants: [claude1, claude2, codex]
---

# LOOP.md — qa-mastery curriculum loop

Loop engineering for this project: instead of Sajan prompting each session by
hand, each agent runs a designed loop over the curriculum backlog, coordinated
through durable state (`STATE.md` + `../Claude Coordination.md`), with hard
gates (`gate.yaml`) and Sajan as the human gate for anything irreversible.

## Agents and lanes (as of 2026-07-18 11:30)

| Agent   | Session                     | Lane                                                        |
|---------|-----------------------------|-------------------------------------------------------------|
| claude1 | "claude" (other Claude Code)| `non-functional-testing-intro` (claimed, in flight)         |
| claude2 | this Claude Code session    | `automation-foundations` (claimed 2026-07-18 11:30)         |
| codex   | Codex CLI                   | `nosql-and-modern-data` ch4 on branch `codex/redis-caching-bugs` |
| codex-2 | second Codex (dormant)      | docker lane                                                 |

`selenium-webdriver` (0/16) is the next open scaffolded lane — first claim in
the Coordination log wins. After that: 12 never-scaffolded Track E/F/G modules
(scaffold + claim required, see STATE.md).

## The cycle — every iteration, every agent

1. **Read state.** Tail of `../Claude Coordination.md` (last ~10 entries) and
   `STATE.md`. If your lane was counter-claimed or Sajan overrode, re-plan
   before touching anything.
2. **Triage.** Pick the smallest next unit of your lane: **one chapter
   (4 notes) max per cycle.**
3. **Claim.** Append a claim entry to the Coordination log BEFORE writing any
   file. Claims name exact paths.
4. **Act (implementer).** Write only inside your lane's content/media paths and
   your own taxonomy lines. Sub-agents allowed, isolated to content/media dirs;
   root owns taxonomy, verification, and commits.
5. **Verify (checker).** Full existing gate bar — MDX compile gate, curriculum
   tests, typecheck, all playgrounds executed for real in both languages,
   images viewed + license-verified via Commons, videos oembed-verified.
   Never trust an unverified draft, including your own from a dead run.
6. **Commit.** Local only. Isolated hunks; `git diff --cached --stat` before
   every commit. Consult `gate.yaml` first.
7. **Write state.** Completion entry in the Coordination log (existing format)
   AND update the counters in `STATE.md`.
8. **Continue or stop.** Next cycle if lane has work and gates pass. Stop and
   escalate to Sajan if: lane empty, gate blocked twice on the same unit, or a
   conflict survives one full log round-trip.

## Phase

**L2 (assisted autonomy).** Loops run without prompting, but every
irreversible action (push, merge, deploy, publish, bulk delete) requires
Sajan. Comprehension debt rule: every commit must be summarized in the
Coordination log entry — no silent landings.

## Joining the loop (claude1 / codex: paste this into your session)

> Read `My Qa Projecct/Loop/LOOP.md`, `STATE.md`, and `gate.yaml`. Adopt the
> cycle for your lane: run one cycle now, then keep cycling until your lane is
> empty or a gate escalates to Sajan. Update STATE.md at the end of every
> cycle.
