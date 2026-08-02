#!/usr/bin/env python3
"""publish_pattern.py — the ONLY sanctioned writer of a PATTERN-grain 'published'.

The mission ruling (2026-08-01): the systemic pattern is the headline; an
individual lead is only ever the receipt. So patterns publish FIRST, at their
own grain (TARGET_KIND='cohort'), and publishing a pattern NEVER flips its
member leads to PUBLISHED — members stay unpublished until each one passes
scripts/publish_lead.py on its own. The inheritance guard that enforces that
lives in scripts/provision_pattern_publish.sql (run it before first use).

Same two-step gate as leads (2026-07-20, beta ruling B1): a Pattern Desk
Confirm is a private NOMINATION. Nothing reads a pattern as published until a
human runs THIS script with --apply.

Guards, in order:
  1. refuses unless the cohort's LATEST verdict is 'confirmed'  (confirm first)
  2. refuses SMOKE_TEST and empty cohort ids
  3. previews by default; writes one append-only row only with --apply
  4. rides the RIPPLE_REVIEW_PAT / RIPPLE_REVIEW_WRITER lane (INSERT+SELECT on
     the one DECISIONS table and nothing else). It never falls back to another
     credential.

Usage:
  python scripts/publish_pattern.py "3363|100-249" --by chris          # preview
  python scripts/publish_pattern.py "3363|100-249" --by chris \
      --reason "cohort re-derived from frozen 300A evidence; rates checked" --apply
"""

from __future__ import annotations

import argparse
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


def main() -> int:
    ap = argparse.ArgumentParser(description="Publish a confirmed pattern/cohort (two-step gate).")
    ap.add_argument("cohort_id", help="COHORT_ID of the pattern to publish (e.g. '3363|100-249')")
    ap.add_argument("--by", required=True, help="reviewer name for the audit row")
    ap.add_argument("--reason", default="", help="why this publishes (required with --apply)")
    ap.add_argument("--apply", action="store_true", help="write the verdict (default: preview)")
    args = ap.parse_args()

    cohort_id = args.cohort_id.strip()
    if not cohort_id or cohort_id.upper() == "SMOKE_TEST":
        print(f"REFUSED: {cohort_id!r} is not a publishable cohort id.")
        return 2
    if args.apply and not args.reason.strip():
        print("REFUSED: --apply requires --reason (the publish act is part of the receipt chain).")
        return 2

    pat = (os.environ.get("RIPPLE_REVIEW_PAT") or "").strip()
    if not pat:
        print("HALT: RIPPLE_REVIEW_PAT is not set in library-onboarding/.env — the publish "
              "lane never falls back to another credential. Mint it per "
              "archive/CLOSE_THE_LOOP_checklist.md Step 2.")
        return 2

    conn = snow.connect(pat=pat, role="RIPPLE_REVIEW_WRITER", warehouse="SERVE_WH")
    try:
        cur = conn.cursor()
        try:
            cur.execute(
                f"""SELECT DECISION, REVIEWER, DECIDED_AT FROM {DECISIONS_FQN}
                    WHERE TARGET_KIND = 'cohort' AND TARGET_ID = %s
                    ORDER BY DECIDED_AT DESC LIMIT 5""",
                (cohort_id,),
            )
            history = cur.fetchall()
        finally:
            cur.close()

        if not history:
            print(f"REFUSED: no verdict on record for cohort {cohort_id} — confirm it at the "
                  "Pattern Desk first (two-step gate: confirm, then publish).")
            return 2

        latest = (history[0][0] or "").strip().lower()
        print(f"cohort {cohort_id}: latest verdict = {latest!r} "
              f"(by {history[0][1]}, {history[0][2]}); {len(history)} recent verdict(s) shown")

        if latest == "published":
            print("No-op: this pattern is already published.")
            return 0
        if latest != "confirmed":
            print(f"REFUSED: latest verdict is {latest!r}, not 'confirmed'. "
                  "Publish only follows an explicit confirm.")
            return 2

        if not args.apply:
            print("\nPREVIEW only — would append:")
            print(f"  DECISION='published'  TARGET_KIND=cohort  TARGET_ID={cohort_id}  "
                  f"REVIEWER={args.by}  REASON={args.reason!r}")
            print("Publishing the pattern does NOT publish its member leads — each lead "
                  "still needs scripts/publish_lead.py on its own.")
            print("Re-run with --apply (and --reason) to write it.")
            return 0

        cur = conn.cursor()
        try:
            cur.execute(
                f"""INSERT INTO {DECISIONS_FQN}
                    (TARGET_KIND, TARGET_ID, DECISION, REASON, REVIEWER)
                    SELECT 'cohort', %s, 'published', %s, %s""",
                (cohort_id, args.reason, args.by),
            )
        finally:
            cur.close()
        print(f"PUBLISHED (pattern grain): cohort {cohort_id} — one append-only row written "
              f"to {DECISIONS_FQN}. V_PATTERNS_PUBLISHED now carries it; member leads are "
              "unchanged (still unpublished individually).")
        print("Reminder: run scripts/export_review_decisions.py and commit the CSV "
              "(human verdicts are the only non-regenerable data).")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
