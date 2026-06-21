#!/usr/bin/env python3
"""
content_scheduler.py — tell me what to post today and flag gaps.

Reads a content pipeline CSV (see ../../03-content/content-pipeline.csv) and:
  - shows what's scheduled for today / this week
  - flags overdue (past-dated, not yet published) pieces
  - warns about empty upcoming slots so you never go dark
  - summarizes the pipeline by status and pillar (balance check)

Project-agnostic: any project using the same pipeline CSV headers works.
Dates must be ISO (YYYY-MM-DD). 'today' is passed in (no system clock dependency
so output is reproducible); defaults to the TODAY env-style arg.

Usage:
    python content_scheduler.py path/to/content-pipeline.csv --today 2026-06-22
    python content_scheduler.py path/to/content-pipeline.csv --today 2026-06-22 --week
"""
import csv
import sys
import argparse
from datetime import date, timedelta
from collections import Counter

PUBLISHED = {"published", "measured"}


def parse_date(s):
    s = (s or "").strip()
    if not s:
        return None
    try:
        y, m, d = map(int, s.split("-"))
        return date(y, m, d)
    except Exception:
        return None


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    ap = argparse.ArgumentParser(description="What to post today + pipeline health.")
    ap.add_argument("csv_path")
    ap.add_argument("--today", required=True, help="ISO date YYYY-MM-DD (reference 'today')")
    ap.add_argument("--week", action="store_true", help="show the next 7 days")
    args = ap.parse_args()

    today = parse_date(args.today)
    if not today:
        sys.exit("--today must be YYYY-MM-DD")

    rows = load(args.csv_path)
    horizon = today + timedelta(days=7)

    due_today, this_week, overdue = [], [], []
    for r in rows:
        d = parse_date(r.get("planned_date"))
        st = (r.get("status") or "").strip().lower()
        if d is None or st in PUBLISHED:
            continue
        if d == today:
            due_today.append(r)
        if today <= d <= horizon:
            this_week.append(r)
        if d < today:
            overdue.append(r)

    def line(r):
        return (f"[{r.get('planned_date')}] {r.get('channel','?'):8} "
                f"{r.get('pillar','?'):13} {r.get('status','?'):9} "
                f"{(r.get('hook') or '(no hook yet)')[:50]}")

    print("\n" + "=" * 64)
    print(f"  CONTENT SCHEDULER  —  today = {today.isoformat()}")
    print("=" * 64)

    print("\n📅 DUE TODAY:")
    print("   " + "\n   ".join(line(r) for r in due_today) if due_today
          else "   nothing scheduled — pull from the calendar!")

    if overdue:
        print("\n⚠️  OVERDUE (past date, not published):")
        for r in overdue:
            print("   " + line(r))

    if args.week:
        print("\n🗓️  NEXT 7 DAYS:")
        for r in sorted(this_week, key=lambda r: r.get("planned_date") or ""):
            print("   " + line(r))
        # empty-slot warning: expect ~3/week
        if len(this_week) < 3:
            print(f"\n   ⚠️  only {len(this_week)} pieces in the next 7 days "
                  "(target ~3). Add rows from content-calendar.md.")

    # health summary
    by_status = Counter((r.get("status") or "?").strip().lower() for r in rows)
    by_pillar = Counter((r.get("pillar") or "?").strip().lower() for r in rows)
    print("\n📊 PIPELINE HEALTH:")
    print("   status:", dict(by_status))
    print("   pillar:", dict(by_pillar))
    print("   (keep pillars balanced — don't be all 'differentiate'.)\n")


if __name__ == "__main__":
    main()
