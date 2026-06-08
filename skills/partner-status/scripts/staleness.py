#!/usr/bin/env python3
"""
staleness.py — flag partner accounts that have gone quiet relative to their own
expected contact cadence.

Why this is a script and not eyeballed: the question "is this partner overdue?"
is per-partner date arithmetic against a different threshold for each account,
across many accounts. Doing it by hand is where mistakes creep in. This keeps it
deterministic and consistent.

Input: a JSON array on stdin (or via --file), one object per tracked partner:
  [
    {"name": "Acme Corp",  "last_active": "2026-05-28", "cadence_days": 7,  "owner": "Dana Lee"},
    {"name": "Initech",    "last_active": "2026-04-22", "cadence_days": 30, "owner": "Dana Lee"},
    {"name": "Umbrella",   "last_active": null,          "cadence_days": 90, "owner": "Priya Shah"}
  ]
- last_active: ISO date (YYYY-MM-DD) of the most recent real activity, or null /
  omitted if nothing was found at all.
- cadence_days: expected days between active touches (weekly=7, biweekly=14,
  monthly=30, quarterly=90, or any explicit number).
- owner (optional): account rep, passed straight through to the output so flags
  come pre-attributed to whoever needs to act.

Severity:
  OK       idle <= cadence_days
  watch    cadence_days < idle <= cadence_days * grace
  overdue  idle > cadence_days * grace
  unknown  no last_active date available (never seen / not in lookback or ledger)

Output: a human-readable table to stderr and a JSON array to stdout (so the
caller can consume it programmatically), each partner annotated with idle_days
and flag.

Usage:
  python3 staleness.py --grace 1.5 < partners_activity.json
  python3 staleness.py --file partners_activity.json --asof 2026-06-02
"""

import argparse
import datetime as dt
import json
import sys


def parse_date(value):
    if not value:
        return None
    try:
        return dt.date.fromisoformat(str(value).strip()[:10])
    except ValueError:
        return None


def classify(idle_days, cadence_days, grace):
    if idle_days is None or cadence_days is None:
        return "unknown"
    if idle_days <= cadence_days:
        return "OK"
    if idle_days <= cadence_days * grace:
        return "watch"
    return "overdue"


def main():
    ap = argparse.ArgumentParser(description="Flag partners overdue vs cadence.")
    ap.add_argument("--grace", type=float, default=1.5,
                    help="overdue once idle > cadence_days * grace (default 1.5)")
    ap.add_argument("--asof", default=None,
                    help="reference date YYYY-MM-DD (default: today)")
    ap.add_argument("--file", default=None,
                    help="read JSON from this path instead of stdin")
    args = ap.parse_args()

    asof = parse_date(args.asof) or dt.date.today()

    raw = open(args.file).read() if args.file else sys.stdin.read()
    try:
        partners = json.loads(raw)
    except json.JSONDecodeError as e:
        sys.exit(f"Could not parse input JSON: {e}")
    if not isinstance(partners, list):
        sys.exit("Input must be a JSON array of partner objects.")

    results = []
    for p in partners:
        name = p.get("name", "(unnamed)")
        cadence = p.get("cadence_days")
        last = parse_date(p.get("last_active"))
        idle = (asof - last).days if last else None
        flag = classify(idle, cadence, args.grace)
        results.append({
            "name": name,
            "owner": p.get("owner"),
            "last_active": last.isoformat() if last else None,
            "cadence_days": cadence,
            "idle_days": idle,
            "flag": flag,
        })

    # Sort so the things needing attention float to the top.
    order = {"overdue": 0, "unknown": 1, "watch": 2, "OK": 3}
    results.sort(key=lambda r: (order.get(r["flag"], 9),
                                -(r["idle_days"] or 0)))

    # Human-readable table to stderr (won't pollute the JSON on stdout).
    width = max([len(r["name"]) for r in results] + [7])
    print(f"As of {asof.isoformat()}  (grace ×{args.grace})\n", file=sys.stderr)
    header = f"{'Partner'.ljust(width)}  {'Last active':<12} {'Cadence':>8} {'Idle':>6}  Flag"
    print(header, file=sys.stderr)
    print("-" * len(header), file=sys.stderr)
    for r in results:
        la = r["last_active"] or "—"
        cad = f"{r['cadence_days']}d" if r["cadence_days"] is not None else "—"
        idle = str(r["idle_days"]) if r["idle_days"] is not None else "—"
        print(f"{r['name'].ljust(width)}  {la:<12} {cad:>8} {idle:>6}  {r['flag']}",
              file=sys.stderr)

    needs = [r for r in results if r["flag"] in ("overdue", "watch", "unknown")]
    if needs:
        print(f"\nNeeds attention: {len(needs)} of {len(results)} partner(s).",
              file=sys.stderr)
    else:
        print("\nAll tracked partners are within cadence.", file=sys.stderr)

    # Machine-readable to stdout.
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
