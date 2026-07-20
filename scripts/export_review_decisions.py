#!/usr/bin/env python3
"""export_review_decisions.py — the decisions micro-export.

Human verdicts in LIBRARY_META.REVIEW.DECISIONS are the first NON-REGENERABLE
data in the platform (leads and marts rebuild from source; a human's recorded
judgment does not). This dumps the FULL append-only log — including the
SMOKE_TEST proof row, which is part of the audit story — to a git-committable
CSV. Run it after every review session; commit the file.

Read-only: rides the RIPPLE_REVIEW_PAT lane (SELECT on the one table). Writes
nothing to the warehouse.

Usage:
  python scripts/export_review_decisions.py            # -> outputs/review_decisions_export.csv
  python scripts/export_review_decisions.py --out path/to/file.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_LIB = _REPO / "library-onboarding"

try:
    from dotenv import load_dotenv

    load_dotenv(_LIB / ".env", override=True)
except Exception:
    pass

if str(_LIB) not in sys.path:
    sys.path.insert(0, str(_LIB))

import snow  # noqa: E402

DECISIONS_FQN = '"LIBRARY_META"."REVIEW"."DECISIONS"'
DEFAULT_OUT = _REPO / "outputs" / "review_decisions_export.csv"


def main() -> int:
    ap = argparse.ArgumentParser(description="Export the append-only decisions log to CSV.")
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="output CSV path")
    args = ap.parse_args()

    pat = (os.environ.get("RIPPLE_REVIEW_PAT") or "").strip()
    if not pat:
        print("HALT: RIPPLE_REVIEW_PAT is not set in library-onboarding/.env — this export "
              "reads the review lane and never falls back to another credential.")
        return 2

    conn = snow.connect(pat=pat, role="RIPPLE_REVIEW_WRITER", warehouse="SERVE_WH")
    try:
        cur = conn.cursor()
        try:
            cur.execute(
                f"""SELECT DECISION_ID, TARGET_KIND, TARGET_ID, DECISION, REASON,
                           REVIEWER, MODEL_VERSION, QUEUE_SNAPSHOT, DECIDED_AT
                    FROM {DECISIONS_FQN}
                    ORDER BY DECIDED_AT, DECISION_ID"""
            )
            cols = [c[0] for c in cur.description]
            rows = cur.fetchall()
        finally:
            cur.close()
    finally:
        conn.close()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for r in rows:
            w.writerow([json.dumps(v) if isinstance(v, (dict, list)) else v for v in r])

    print(f"exported {len(rows)} decision row(s) -> {out}")
    print("Commit this file: `git add` + commit — verdicts are non-regenerable.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
