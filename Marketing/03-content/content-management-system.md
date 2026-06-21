# Content Management System (CMS) — Reusable Workflow

A lightweight, $0, project-agnostic system to plan → draft → schedule → publish → measure content. Built for QA Mastery but designed to run **any** project (just swap the config). No paid CMS tool needed — a CSV + scripts + your calendar.

---

## The pipeline

```
IDEA  →  BACKLOG  →  DRAFT  →  SCHEDULED  →  PUBLISHED  →  MEASURED  →  (recycle winners)
```

State lives in one file: [`content-pipeline.csv`](./content-pipeline.csv). One row per content piece. The [`content_scheduler.py`](../05-automation/scripts/content_scheduler.py) script reads it to tell you what to post today and flags overdue/empty slots.

---

## content-pipeline.csv columns
`id, pillar, channel, planned_date, status, hook, body_link, cta, repurposed_from, posted_url, impressions, comments, clicks, signups`

- **pillar:** teach | differentiate | build-public | proof | engage
- **channel:** linkedin | reddit | mot | devto | blog | youtube
- **status:** idea → backlog → draft → scheduled → published → measured
- **repurposed_from:** id of the source piece (track the write-once-post-5× chain)
- last 4 columns: filled after posting → feeds what to recycle

---

## Roles in the loop (you wear all hats, but separate the *modes*)
1. **Planner mode (Mon, 20 min):** pull from calendar + top feedback themes → set the week's 3 rows to `draft`.
2. **Maker mode (batch, 1–2 sittings):** write all drafts at once. Batching beats daily context-switching.
3. **Publisher mode (Mon/Wed/Fri):** post the scheduled piece, paste `posted_url`, set `published`.
4. **Analyst mode (Sun, 15 min):** fill metrics, set `measured`, mark winners to recycle.

## Where content comes from (never run dry)
- The [12-week calendar](./content-calendar.md) (the backbone).
- **Top feedback themes** — every recurring question is a post. The feedback loop *is* your content engine.
- Your own QA notes in `../../Resources/` — you already have 90 days of material. Mine it.
- Community questions you answered well → expand into a post.

## Making it reusable for other projects
This whole folder is a template. To reuse for another project:
1. Copy `05-automation/config/project.example.yaml` → `project.<name>.yaml`, edit name/pillars/channels.
2. Start fresh `content-pipeline.csv` and `feedback-intake.csv` with the same headers.
3. Point the scripts at the new config: `python content_scheduler.py --config project.<name>.yaml`.

The system doesn't care what the product is — it manages content + feedback for any of your projects.

---

## Definition of done for a content piece
- [ ] Hook tested (would *you* stop scrolling?)
- [ ] One clear CTA
- [ ] Link in first comment (LinkedIn)
- [ ] Logged in `content-pipeline.csv`
- [ ] Replied to comments within 2h
- [ ] Metrics captured Sunday
