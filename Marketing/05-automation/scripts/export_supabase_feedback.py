#!/usr/bin/env python3
"""
export_supabase_feedback.py — pull in-app feedback from Supabase into the
feedback-intake.csv shape, deduped by id, ready for feedback_triage.py.

Reads the `public.feedback` table (created by migration 0015) over PostgREST
using the SERVICE ROLE key (server-side only — bypasses RLS to read all rows).
Stdlib only; no pip installs.

Env (same names as the app):
    NEXT_PUBLIC_SUPABASE_URL      e.g. https://xxxx.supabase.co
    SUPABASE_SERVICE_ROLE_KEY     service role secret  (NEVER commit / NEVER client-side)

Usage:
    export NEXT_PUBLIC_SUPABASE_URL=https://xxxx.supabase.co
    export SUPABASE_SERVICE_ROLE_KEY=sb_secret_...
    python export_supabase_feedback.py                       # merge into master CSV
    python export_supabase_feedback.py --out feedback.csv    # write a fresh file
    python export_supabase_feedback.py --since 2026-06-01    # only newer rows
    python export_supabase_feedback.py --selftest            # offline mapping test

The master CSV keeps the marketing columns; triage fields (reach/impact/
confidence/effort) are left blank for the Friday triage to fill.
"""
import argparse
import csv
import json
import os
import sys
import urllib.parse
import urllib.request

HEADERS = ["id", "date", "source", "user_segment", "type", "raw_text",
           "theme", "reach", "impact", "confidence", "effort", "status"]

DEFAULT_MASTER = os.path.join(
    os.path.dirname(__file__), "..", "..", "02-feedback-loop", "feedback-intake.csv"
)


def fetch_rows(base_url, key, since=None):
    """GET public.feedback over PostgREST. Returns list of dicts."""
    params = {
        "select": "id,created_at,type,message,rating,context,theme,status",
        "order": "created_at.desc",
    }
    if since:
        params["created_at"] = f"gte.{since}"
    url = f"{base_url.rstrip('/')}/rest/v1/feedback?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Accept": "application/json",
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def to_intake(row):
    """Map a feedback row to the feedback-intake.csv shape."""
    created = (row.get("created_at") or "")[:10]  # YYYY-MM-DD
    return {
        "id": str(row.get("id", "")),
        "date": created,
        "source": "in_app",
        "user_segment": "",                  # not captured in-app; fill at triage
        "type": row.get("type", ""),
        "raw_text": (row.get("message", "") or "").replace("\n", " ").strip(),
        "theme": row.get("theme", "") or "",
        "reach": "", "impact": "", "confidence": "", "effort": "",
        "status": row.get("status", "new") or "new",
    }


def read_master(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADERS)
        w.writeheader()
        for r in rows:
            w.writerow({h: r.get(h, "") for h in HEADERS})


def merge(master, incoming):
    """Merge incoming intake rows into master, deduped by id (in_app rows)."""
    seen_ids = {r.get("id") for r in master if r.get("source") == "in_app"}
    added = [r for r in incoming if r["id"] not in seen_ids]
    return master + added, added


def selftest():
    sample = [
        {"id": "11111111-1111-1111-1111-111111111111", "created_at": "2026-06-21T08:30:00Z",
         "type": "feature", "message": "Add a dark\nmode toggle", "rating": 4,
         "context": "lesson:bug-reporting", "theme": None, "status": "new"},
    ]
    mapped = [to_intake(r) for r in sample]
    assert mapped[0]["source"] == "in_app"
    assert mapped[0]["date"] == "2026-06-21"
    assert mapped[0]["raw_text"] == "Add a dark mode toggle"
    assert mapped[0]["status"] == "new"
    print("selftest OK — mapping produces:")
    print(json.dumps(mapped[0], indent=2))


def main():
    ap = argparse.ArgumentParser(description="Export Supabase feedback to intake CSV.")
    ap.add_argument("--out", help="write a fresh CSV here instead of merging the master")
    ap.add_argument("--master", default=DEFAULT_MASTER, help="master CSV to merge into")
    ap.add_argument("--since", help="only rows with created_at >= this ISO date/datetime")
    ap.add_argument("--selftest", action="store_true", help="offline mapping test, no network")
    args = ap.parse_args()

    if args.selftest:
        selftest()
        return

    base = os.environ.get("NEXT_PUBLIC_SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    if not base or not key:
        sys.exit("Set NEXT_PUBLIC_SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY env vars.")

    rows = fetch_rows(base, key, since=args.since)
    incoming = [to_intake(r) for r in rows]
    print(f"fetched {len(incoming)} feedback rows from Supabase")

    if args.out:
        write_csv(args.out, incoming)
        print(f"wrote {len(incoming)} rows -> {args.out}")
        return

    master = read_master(args.master)
    merged, added = merge(master, incoming)
    write_csv(args.master, merged)
    print(f"merged: +{len(added)} new (master now {len(merged)} rows) -> {args.master}")
    print("next: python feedback_triage.py", os.path.abspath(args.master))


if __name__ == "__main__":
    main()
