# Claude Operating Manual — Sajan's QA Vault

> Read this before doing anything in this vault. It complements `CLAUDE.md`
> (repo conventions — teaching style, note formats, housekeeping); on conflict,
> `CLAUDE.md` wins for study-note content, this file wins for vault operations.

---

## Section 0 — AI-First Vault Rule

Notes written by Claude here serve future-Claude *and* a human learner. Every
Claude-written note must:

1. **Be self-contained** — explain itself without surrounding context.
2. **Open with a 2–3 sentence plain-English summary.**
3. **Carry frontmatter** — `type`, `date`, `topic`, `tags` minimum.
4. **Date external claims** — "Selenium 4.25 current (as of 2026-07)".
5. **Keep source URLs inline** for every external claim.
6. **Cross-link aggressively** — every QA concept, tool, or roadmap day
   referenced uses `[[wikilinks]]` so the graph stays traversable.

## Section 0.5 — Verify Live State Before Acting

Read the actual note/code/schema before claiming anything about it. For
library facts (Selenium, TestNG, Playwright versions/APIs) verify against
current docs — training data is stale.

---

## Vault Identity

- **Owner:** Sajan (dpokhrel275@gmail.com) — learning QA, building QA Mastery
- **Purpose:** QA study knowledge base + the product being built from it
- **Git:** this vault IS the repo `izzzthisssagar/my-qa-project` (obsidian-git
  plugin installed). Two Claude Code sessions work here in parallel — check
  `git status` before committing; never sweep another session's changes.

## Structure

| Path | What lives there |
|---|---|
| `Home.md` | Dashboard / entry point |
| `Resources/` | All study notes (the spine: two roadmap notes) |
| `Resources/attachments/` | Images/files pasted into notes |
| `Product/` | Platform + marketplace specs |
| `Curriculum/`, `Marketing/` | Curriculum HTML, marketing assets |
| `qa-mastery/` | Platform code — own git repo, NOT vault content |
| `graphify-out/` | Generated knowledge graph (read-only artifacts) |
| `Logs/` | Vault operations log (per-day, append-only) |
| `index.md` | Catalog of every note — read this FIRST when navigating |

## Operating rules

- New study notes → `Resources/`, matching the heading style in `CLAUDE.md`.
- Update `index.md` when adding/removing notes.
- Log vault operations to `Logs/YYYY-MM-DD.md` (`**HH:MM** - action | description`).
- Don't touch `qa-mastery/`, `graphify-out/` or `.obsidian/plugins/` from
  vault commands — they're code/artifacts, not notes.
