---
type: dev-log
date: 2026-07-10
topic: QA Mastery — Notes v2 build
project: qa-mastery
ai-first: true
tags: [dev-log, qa-mastery, notes-wiki, track-a]
---

## For future Claude

Dev log for the QA Mastery **Notes v2** build sessions (2026-07-09 → 10, Claude Code, branch `feat/notes-v2` in the `qa-mastery/` repo — code repo, NOT vault content). Read this to know exactly where the interactive notes wiki stands, what the locked template requires, and what comes next. Deep state also lives in Claude auto-memory (`qa-notes-vision`); this note is the vault's copy of record.

## Summary

Track A **Module 1 "How a computer works" is COMPLETE — 20/20 topics live** in-platform, and **Module 2 "Operating systems & files" Chapter 1 (4/4)** is done. The note template is user-approved and locked: roast-mentor voice + 18 audited sections per note. All verified on production builds via scripted browser; committed through `0cfc739` on `feat/notes-v2` (local only — push when Sajan says ship).

## What was built

- **Component library** (`apps/platform/src/app/(app)/notes/note-components.tsx`): Hook, Callout, Figure, Video, Term, Quiz, Flashcards, Takeaways, Complete (+XP confetti), FirstTime, WhenItBreaks (accordion), WhereToCheck, AskCommunity, Challenge, Resources, WorkedExample, HotspotImage (tap-pin explorer), PartsQuest (collect-all legend), StepChecklist (progress missions), **FlowAnimation** (playable staged diagram: autoplay/pause/step), **CodePlayground** (editable+runnable code via the simulator's Wandbox server action — verified executing real Python live).
- **24 template notes** written (20 in [[Module 1 — How a computer works]] scope + 4 in Module 2 Ch1), each carrying all 18 sections. ~30 CC/PD images from Wikimedia Commons self-hosted under `apps/platform/public/notes/` with attribution rendered.
- **Curriculum taxonomy** (`packages/curriculum/src/notes/taxonomy.ts`) now carries Module 1 (5 chapters) + Module 2 (5 chapters, ch2–5 as `planned:true` stubs) per the approved [[01-master-curriculum-map|curriculum v4.1 map]] (7 tracks / 48 modules / ~876 topics).

## Decisions locked (user-approved)

1. **Interactivity rule** — no wall-of-text; every note interleaves ≤3 paragraphs with an interactive block; real CC images required (confidence: user-stated, firm).
2. **Voice rule** — roast-flavored mentor: banter + tech-roasting + everyday examples, exact technical truth after every joke.
3. **Flow+Code rule (2026-07-10)** — FlowAnimation AND CodePlayground required in EVERY note, not just showcase ones ("not just on the CPU note but all notes").

## Problems hit & fixed

- next-mdx-remote v6 strips JSX attribute expressions by default (`blockJS`) — array props arrived `undefined`; fixed with `options={{ blockJS: false }}` (repo-authored MDX = trusted).
- Client-component map exported from a `"use client"` module loses members across the RSC boundary — components must be named imports in the server page.
- Wikimedia thumb URLs 404 when requested width ≥ original — always fetch `thumburl` via the Commons API (with a User-Agent header; anonymous urllib gets 403).

## Also this session (platform, merged to main)

- Phase 5 (Notes wiki) merged as PR #87; Phase 6 (Tasks) merged as PR #88 after fixing a real bug (partial unique index broke the accept-task upsert) + optimistic-UI fixes; follow-up PR #89 (accept/grade transition split) fixed the main-branch CI failure. Platform main = Phases 0–6 complete.

## Next steps

- [ ] Module 2 Chapter 2 "Windows, macOS & Linux" (screenshots: Linux free; Windows/macOS copyrighted — plan around)
- [ ] Then M2 ch3–5 → Modules 3–5 → Tracks B–G per the map
- [ ] Rewrite the 37 old v1 encyclopedia notes to the full template when their modules arrive
- [ ] Push `feat/notes-v2` + PR when Sajan says ship; Phase 7 design sweep still pending
