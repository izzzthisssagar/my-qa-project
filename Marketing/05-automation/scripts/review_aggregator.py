#!/usr/bin/env python3
"""
review_aggregator.py — normalize scattered feedback into the master CSV.

You collect feedback from many places (Reddit, LinkedIn, Discord, DMs, Tally
exports, in-app Supabase exports). This merges any number of source files into
one deduplicated feedback-intake.csv, assigning fresh sequential ids and a
default status of 'new'.

Accepts:
  - CSVs that already have some intake columns (e.g. a Tally export) — it maps
    what it can and leaves blanks for triage fields.
  - A simple "pasted notes" .txt where each non-empty line becomes one row
    (use --source and --type to tag them), for quick community/DM capture.

Project-agnostic. Output stays in feedback-intake.csv shape so feedback_triage.py
can consume it directly.

Usage:
    # merge a Tally/Supabase CSV export into the master
    python review_aggregator.py --master feedback-intake.csv --add tally_export.csv

    # turn pasted community notes into rows
    python review_aggregator.py --master feedback-intake.csv \\
        --add reddit_notes.txt --source reddit --type feature

    # dry run (print, don't write)
    python review_aggregator.py --master feedback-intake.csv --add x.csv --dry-run
"""
import csv
import os
import sys
import argparse

HEADERS = ["id", "date", "source", "user_segment", "type", "raw_text",
           "theme", "reach", "impact", "confidence", "effort", "status"]


def load_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def read_master(path):
    if not os.path.exists(path):
        return []
    return load_csv(path)


def next_id(rows):
    mx = 0
    for r in rows:
        try:
            mx = max(mx, int(r.get("id") or 0))
        except ValueError:
            pass
    return mx + 1


def rows_from_txt(path, source, type_, date_):
    out = []
    with open(path, encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if ln:
                out.append({"source": source, "type": type_,
                            "raw_text": ln, "date": date_})
    return out


def rows_from_csv(path):
    out = []
    for r in load_csv(path):
        # map loosely: keep any matching header, route common Tally names
        row = {h: (r.get(h) or "") for h in HEADERS}
        if not row["raw_text"]:
            row["raw_text"] = (r.get("message") or r.get("feedback")
                               or r.get("What do you want") or "")
        out.append(row)
    return out


def norm(row, _id):
    full = {h: "" for h in HEADERS}
    full.update({k: v for k, v in row.items() if k in HEADERS})
    full["id"] = str(_id)
    if not full["status"]:
        full["status"] = "new"
    return full


def main():
    ap = argparse.ArgumentParser(description="Merge feedback sources into master CSV.")
    ap.add_argument("--master", required=True)
    ap.add_argument("--add", required=True, help="CSV or TXT to merge in")
    ap.add_argument("--source", default="manual", help="tag for TXT lines")
    ap.add_argument("--type", default="feature", help="type for TXT lines")
    ap.add_argument("--date", default="", help="date for TXT lines (YYYY-MM-DD)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    master = read_master(args.master)
    existing = {(r.get("raw_text") or "").strip().lower() for r in master}
    nid = next_id(master)

    if args.add.lower().endswith(".txt"):
        incoming = rows_from_txt(args.add, args.source, args.type, args.date)
    else:
        incoming = rows_from_csv(args.add)

    added = []
    for r in incoming:
        key = (r.get("raw_text") or "").strip().lower()
        if not key or key in existing:
            continue  # dedupe by exact text
        existing.add(key)
        added.append(norm(r, nid))
        nid += 1

    print(f"master: {len(master)} rows | incoming: {len(incoming)} | "
          f"new after dedupe: {len(added)}")
    for r in added:
        print(f"  + [{r['id']}] {r['source']}/{r['type']}: {r['raw_text'][:55]}")

    if args.dry_run:
        print("\n(dry run — nothing written)")
        return

    out = master + added
    with open(args.master, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADERS)
        w.writeheader()
        for r in out:
            w.writerow({h: r.get(h, "") for h in HEADERS})
    print(f"\nwrote {len(out)} rows -> {args.master}")
    print("next: run feedback_triage.py on the master to re-rank.")


if __name__ == "__main__":
    main()
