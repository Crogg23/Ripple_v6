#!/usr/bin/env python3
"""publish_lead.py — the ONLY sanctioned writer of the 'published' verdict.

Two-step publish gate (2026-07-20, beta ruling B1): a Reading-Room Confirm is a
private NOMINATION. Nothing reads PUBLISHED=TRUE — in V_LEADS_PUBLISHED, the
LEAD_QUEUE pipeline, or connect.safety.gate_rows — until a human runs THIS
script with --apply. The review buttons and the `connect review` CLI cannot
write 'published' (connect/safety.py keeps it out of VALID on purpose).

Guards, in order:
  1. refuses unless the lead's LATEST verdict is 'confirmed'  (confirm first)
  2. refuses SMOKE_TEST and empty lead ids
  3. previews by default; writes one append-only row only with --apply
  4. rides the RIPPLE_REVIEW_PAT / RIPPLE_REVIEW_WRITER lane (INSERT+SELECT on
     the one DECISIONS table and nothing else) — it CANNOT touch anything else,
     by grant design. It never falls back to another credential.

Usage:
  python scripts/publish_lead.py <LEAD_ID> --by chris            # preview
  python scripts/publish_lead.py <LEAD_ID> --by chris \
      --reason "pin #1: receipts re-derived + primary sources checked" --apply
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
    ap = argparse.ArgumentParser(description="Publish a confirmed lead (two-step gate).")
    ap.add_argument("lead_id", help="LEAD_ID of the lead to publish")
    ap.add_argument("--by", required=True, help="reviewer name for the audit row")
    ap.add_argument("--reason", default="", help="why this publishes (required with --apply)")
    ap.add_argument("--apply", action="store_true", help="write the verdict (default: preview)")
    args = ap.parse_args()

    lead_id = args.lead_id.strip()
    if not lead_id or lead_id.upper() == "SMOKE_TEST":
        print(f"REFUSED: {lead_id!r} is not a publishable lead id.")
        return 2
    if args.apply and not args.reason.strip():
        print("REFUSED: --apply requires --reason (the publish act is part of the receipt chain).")
        return 2

    pat = (os.environ.get("RIPPLE_REVIEW_PAT") or "").strip()
    if not pat:
        print("HALT: RIPPLE_REVIEW_PAT is not set in library-onboarding/.env — the publish "
              "lane never falls back to another credential. Mint it per "
              "CLOSE_THE_LOOP_checklist.md Step 2.")
        return 2

    conn = snow.connect(pat=pat, role="RIPPLE_REVIEW_WRITER", warehouse="SERVE_WH")
    try:
        cur = conn.cursor()
        try:
            cur.execute(
                f"""SELECT DECISION, REVIEWER, DECIDED_AT FROM {DECISIONS_FQN}
                    WHERE TARGET_KIND = 'lead' AND TARGET_ID = %s
                    ORDER BY DECIDED_AT DESC LIMIT 5""",
                (lead_id,),
            )
            history = cur.fetchall()
        finally:
            cur.close()

        if not history:
            print(f"REFUSED: no verdict on record for {lead_id} — confirm it in the "
                  "Reading Room first (two-step gate: confirm, then publish).")
            return 2

        latest = (history[0][0] or "").strip().lower()
        print(f"lead {lead_id}: latest verdict = {latest!r} "
              f"(by {history[0][1]}, {history[0][2]}); {len(history)} recent verdict(s) shown")

        if latest == "published":
            print("No-op: this lead is already published.")
            return 0
        if latest != "confirmed":
            print(f"REFUSED: latest verdict is {latest!r}, not 'confirmed'. "
                  "Publish only follows an explicit confirm.")
            return 2

        if not args.apply:
            print("\nPREVIEW only — would append:")
            print(f"  DECISION='published'  TARGET_ID={lead_id}  REVIEWER={args.by}  "
                  f"REASON={args.reason!r}")
            print("Re-run with --apply (and --reason) to write it.")
            return 0

        cur = conn.cursor()
        try:
            cur.execute(
                f"""INSERT INTO {DECISIONS_FQN}
                    (TARGET_KIND, TARGET_ID, DECISION, REASON, REVIEWER)
                    SELECT 'lead', %s, 'published', %s, %s""",
                (lead_id, args.reason, args.by),
            )
        finally:
            cur.close()
        print(f"PUBLISHED: {lead_id} — one append-only row written to {DECISIONS_FQN}. "
              "V_LEADS_PUBLISHED now reads it as PUBLISHED=TRUE.")
        print("Reminder: run scripts/export_review_decisions.py and commit the CSV "
              "(human verdicts are the only non-regenerable data).")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
