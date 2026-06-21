#!/usr/bin/env python3
"""
feedback_triage.py — turn raw feedback into a ranked, ship-ready backlog.

Reads a feedback CSV (see ../../02-feedback-loop/feedback-intake.csv), computes a
RICE score for each feature/ux/content/pricing item, separates bugs into a
severity triage, groups by theme, and prints a ranked backlog.

Project-agnostic: works for any project whose feedback CSV uses the same headers.

Usage:
    python feedback_triage.py path/to/feedback-intake.csv
    python feedback_triage.py path/to/feedback-intake.csv --json
    python feedback_triage.py path/to/feedback-intake.csv --top 10

CSV headers expected:
    id,date,source,user_segment,type,raw_text,theme,reach,impact,confidence,effort,status

Word -> number maps (RICE):
    impact:     massive=3, high=2, medium=1, low=0.5, minimal=0.25
    confidence: high=1.0, medium=0.8, low=0.5
    effort:     xs=0.25, s=0.5, m=1, l=2, xl=3
"""
import csv
import sys
import json
import argparse
from collections import defaultdict

IMPACT = {"massive": 3.0, "high": 2.0, "medium": 1.0, "low": 0.5, "minimal": 0.25}
CONFIDENCE = {"high": 1.0, "medium": 0.8, "low": 0.5}
EFFORT = {"xs": 0.25, "s": 0.5, "m": 1.0, "l": 2.0, "xl": 3.0}

SCOREABLE = {"feature", "ux", "content", "pricing"}


def num(value, table, default):
    if value is None:
        return default
    v = str(value).strip().lower()
    if v in table:
        return table[v]
    try:
        return float(v)  # allow raw numbers too
    except ValueError:
        return default


def rice(row):
    try:
        reach = float(str(row.get("reach", "")).strip() or 0)
    except ValueError:
        reach = 0.0
    impact = num(row.get("impact"), IMPACT, 1.0)
    conf = num(row.get("confidence"), CONFIDENCE, 0.8)
    effort = num(row.get("effort"), EFFORT, 1.0) or 1.0
    return round((reach * impact * conf) / effort, 1)


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    ap = argparse.ArgumentParser(description="Rank feedback into a backlog (RICE).")
    ap.add_argument("csv_path", help="feedback CSV file")
    ap.add_argument("--top", type=int, default=0, help="limit backlog to top N")
    ap.add_argument("--json", action="store_true", help="output JSON")
    args = ap.parse_args()

    rows = load(args.csv_path)

    bugs, scored, praise = [], [], []
    for r in rows:
        t = (r.get("type") or "").strip().lower()
        if t == "bug":
            bugs.append(r)
        elif t == "praise":
            praise.append(r)
        elif t in SCOREABLE:
            r["_rice"] = rice(r)
            scored.append(r)

    scored.sort(key=lambda r: r["_rice"], reverse=True)
    if args.top:
        scored = scored[: args.top]

    # theme frequency = signal strength
    themes = defaultdict(int)
    for r in rows:
        th = (r.get("theme") or "").strip()
        if th:
            themes[th] += 1
    hot = sorted(themes.items(), key=lambda kv: kv[1], reverse=True)

    if args.json:
        print(json.dumps({
            "backlog": [{"id": r.get("id"), "theme": r.get("theme"),
                          "type": r.get("type"), "rice": r["_rice"],
                          "text": r.get("raw_text")} for r in scored],
            "bugs": [{"id": r.get("id"), "text": r.get("raw_text")} for r in bugs],
            "themes": dict(hot),
            "praise_count": len(praise),
        }, indent=2))
        return

    print("\n" + "=" * 64)
    print("  FEEDBACK TRIAGE — ranked backlog")
    print("=" * 64)

    if bugs:
        print(f"\n🐞 BUGS — fix before features ({len(bugs)}):")
        for r in bugs:
            print(f"   [{r.get('id')}] {r.get('raw_text','')[:70]}")

    print(f"\n🏆 RANKED BACKLOG (RICE) — build top-down:")
    if not scored:
        print("   (no scoreable items)")
    for i, r in enumerate(scored, 1):
        print(f"   {i:>2}. RICE {r['_rice']:>7}  [{r.get('theme','-')}]  "
              f"{r.get('raw_text','')[:55]}")

    print(f"\n🔥 HOT THEMES (3+ = strong signal):")
    for th, n in hot:
        flag = "  ⭐" if n >= 3 else ""
        print(f"   {n:>2}x  {th}{flag}")

    if praise:
        print(f"\n💚 PRAISE ({len(praise)}) — mine these for testimonials.")

    print("\nNext step: pick the top backlog item that fits next week, mark it"
          " 'planned' in the CSV, ship it, then 'announced'.\n")


if __name__ == "__main__":
    main()
