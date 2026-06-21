# Automation Toolkit — $0, Reusable Across Projects

Three small Python scripts (stdlib only — no installs) that remove the boring parts of running marketing solo. Built for QA Mastery but **project-agnostic**: point them at any project's CSVs (see [`config/project.example.yaml`](./config/project.example.yaml)).

| Script | Does | Run when |
|---|---|---|
| [`export_supabase_feedback.py`](./scripts/export_supabase_feedback.py) | Pulls **real in-app feedback** from the Supabase `feedback` table (PostgREST, service role) into the master CSV, deduped | Weekly (automated, see below) |
| [`feedback_triage.py`](./scripts/feedback_triage.py) | Reads feedback CSV → RICE-ranks features, lists bugs, surfaces hot themes | Every Friday |
| [`content_scheduler.py`](./scripts/content_scheduler.py) | Reads content pipeline → "what to post today", overdue + empty-slot warnings | Daily / Monday |
| [`review_aggregator.py`](./scripts/review_aggregator.py) | Merges scattered feedback (CSV exports, pasted notes) into the master CSV, deduped | When you collect feedback |

> **Live wiring:** the in-app feedback widget (built into `qa-mastery/apps/platform`) writes to Supabase `public.feedback`. `export_supabase_feedback.py` reads it back into the marketing CSV, and [`.github/workflows/marketing-feedback.yml`](../../.github/workflows/marketing-feedback.yml) runs export → triage → commit → notify every Friday automatically. Set repo secrets `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, and (optional) `NOTIFY_WEBHOOK`. Test the mapping offline with `python export_supabase_feedback.py --selftest`.

All scripts: `python <script>.py --help`. No dependencies — any Python 3.

---

## The weekly machine

```
Mon   content_scheduler.py --week     → plan + draft the week
Daily content_scheduler.py --today    → what to post now
Fri   review_aggregator.py            → fold the week's feedback into master
Fri   feedback_triage.py             → ranked backlog → pick 1 to ship
Sun   update targets-and-metrics.md   → steer
```

## Examples

```bash
cd 05-automation/scripts

# Ranked backlog from feedback
python feedback_triage.py ../../02-feedback-loop/feedback-intake.csv

# What to post this week (pass today's date — keeps output reproducible)
python content_scheduler.py ../../03-content/content-pipeline.csv --today 2026-06-22 --week

# Fold pasted Reddit notes into the master feedback list
python review_aggregator.py --master ../../02-feedback-loop/feedback-intake.csv \
    --add reddit_notes.txt --source reddit --type feature --date 2026-06-22

# Then re-rank
python feedback_triage.py ../../02-feedback-loop/feedback-intake.csv
```

## Reuse for another project
1. `cp config/project.example.yaml config/project.<name>.yaml` and edit.
2. Create that project's own `feedback-intake.csv` and `content-pipeline.csv` (same headers).
3. Run the scripts pointing at those files. Same toolkit, new project.

## Heavier option
The `product-manager-toolkit` skill ships a fuller `rice_prioritizer.py` with portfolio analysis and quarterly roadmap generation — use it when you want capacity planning, not just ranking.

## Optional next-level automation (when you outgrow manual)
- **Zapier / Make ($0 tier):** auto-append Tally + Supabase submissions into a Google Sheet → one master, no manual export.
- **GitHub Action (cron):** run `content_scheduler.py` each morning, post the "what to post today" to your Slack/Discord/email.
- **Supabase scheduled function:** nightly export of new `feedback` rows into the intake shape.
Keep it manual until the volume actually hurts — premature automation wastes your scarce time.
