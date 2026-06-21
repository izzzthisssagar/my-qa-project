# Automation Wiring — $0 Setup Guide

Make the manual weekly rhythm run itself, free. Start manual; add these only when the volume actually hurts. Three tiers, cheapest first.

---

## Tier 0 — Manual (start here, day 1)
No setup. Export Tally + Supabase feedback weekly → paste into `02-feedback-loop/feedback-intake.csv` → run `feedback_triage.py`. Fine until you get ~20+ feedback items/week. Don't automate before this hurts.

---

## Tier 1 — Auto-collect feedback into one sheet (Zapier or Make, free tier)

**Goal:** every Tally submission and every in-app feedback row lands in ONE Google Sheet automatically, in `feedback-intake.csv` shape. No more manual exports.

### A. Tally → Google Sheet (built-in, no Zapier needed)
1. In Tally: form → **Integrations → Google Sheets → Connect**.
2. Map form fields to columns: `source` (set constant "tally"), `user_segment`, `type`, `raw_text`, `email`.
3. Done. Every submission appends a row.

### B. Supabase in-app feedback → same Sheet (Zapier free, 100 tasks/mo)
1. Zapier → **New Zap**.
2. **Trigger:** Schedule by Zapier → every day (free tier is daily, not instant — fine for this).
3. **Action:** Webhooks by Zapier (or Supabase step) → GET new `feedback` rows. Easiest: expose a Supabase **Edge Function** or REST endpoint that returns rows where `created_at > last_run`, using the service role key (server-side only).
4. **Action:** Google Sheets → "Create rows" mapping to the same columns (`source` = "in_app").
5. Test, turn on.

> **Make.com** does the same with a more generous free tier (1000 ops/mo) if you outgrow Zapier's 100.

### C. Pull the Sheet down for triage
Export the Google Sheet as CSV (File → Download → CSV) over the master, or use `review_aggregator.py` to merge a downloaded export:
```bash
python review_aggregator.py --master ../02-feedback-loop/feedback-intake.csv --add ~/Downloads/feedback-sheet.csv
python feedback_triage.py ../02-feedback-loop/feedback-intake.csv
```

---

## Tier 2 — Daily "what to post" reminder (GitHub Action, free)

**Goal:** every morning, get a message telling you today's post — no opening files.

The scripts are stdlib-only, so a GitHub Action can run them on a cron and ping you.

### Setup
1. Put the `Marketing/` folder in a GitHub repo (private is fine).
2. Add a Slack/Discord **incoming webhook URL** as a repo secret `NOTIFY_WEBHOOK`.
3. Create `.github/workflows/daily-post.yml`:

```yaml
name: Daily post reminder
on:
  schedule:
    - cron: "0 3 * * *"   # 03:00 UTC — adjust to your morning (Nepal = UTC+5:45)
  workflow_dispatch: {}     # lets you run it manually too
jobs:
  remind:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Compute today's post
        id: post
        run: |
          TODAY=$(date -u +%F)
          OUT=$(python Marketing/05-automation/scripts/content_scheduler.py \
                Marketing/03-content/content-pipeline.csv --today "$TODAY")
          # escape for JSON
          echo "body<<EOF" >> $GITHUB_OUTPUT
          echo "$OUT" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT
      - name: Notify
        run: |
          curl -s -X POST -H 'Content-type: application/json' \
            --data "$(python -c 'import json,os;print(json.dumps({"text":os.environ["B"]}))')" \
            "${{ secrets.NOTIFY_WEBHOOK }}"
        env:
          B: ${{ steps.post.outputs.body }}
```

4. Commit. Each morning you get today's scheduled post (and overdue/empty-slot warnings) in Slack/Discord.

> Note: `content_scheduler.py` takes `--today` explicitly (no system-clock dependency in the script) — the workflow injects the date via `date -u +%F`.

### Optional: weekly feedback digest
Add a second workflow on `cron: "0 4 * * 5"` (Fridays) that runs `feedback_triage.py` and posts the ranked backlog to the same webhook. Now your Friday triage arrives on its own.

---

## What to automate vs leave manual

| Automate (worth it) | Keep manual (judgment) |
|---|---|
| Collecting feedback into one place | Deciding what to ship (RICE is a guide, you choose) |
| Daily "what to post" reminder | Writing the actual posts |
| Weekly backlog digest | Replying to comments (this is the relationship) |
| Cross-posting reminders | Closing the loop ("you asked, we built it") |

**Rule:** automate the *remembering and gathering*, never the *judging and talking*. The human parts are where trust is built.

---

## Reusing for other projects
Every piece here is repo + CSV + webhook. Copy the workflow files into another project's repo, point them at that project's `content-pipeline.csv` / `feedback-intake.csv`, set its own webhook secret. Same machine, new project — see [`config/project.example.yaml`](./config/project.example.yaml).
