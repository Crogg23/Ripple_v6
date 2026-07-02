#!/usr/bin/env python3
"""Build POLITICS__SCOTUS_JUSTICE -- the SCOTUS justice dimension + crosswalk spine.

Derived from the already-landed SCDB (LIBRARY_RAW.LANDING.FED_SCDB, the modern
1946-present Spaeth database): ONE ROW PER JUSTICE, keyed on JUSTICE_NAME (the
Spaeth / Judicial-Common-Space convention, e.g. 'WHRehnquist', 'ACBarrett'). This is
the closed-set (~40 modern justices) crosswalk brick the judiciary expansion bolts
onto:
  * Judicial Common Space (JCS) ideology joins by IDENTITY on JUSTICE_NAME (same
    Spaeth convention) -- near-STEEL within this closed set.
  * FJC judge nid resolves by name-match when FJC lands (PROBABILISTIC -> stored
    with a match_method/confidence at that point, per the detective-trust doctrine).

Independent by design: needs no FJC, no name-resolution moat, no new landing --
just the SCDB rows Ripple already holds. Additive: creates one new POLITICS mart,
touches nothing existing (isolation contract).

    python3 politics/loaders/build_scotus_justice.py         # build + smoke test
"""
from __future__ import annotations

import sys
from pathlib import Path as _RepoPath

_REPO = _RepoPath(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO / "library-onboarding"))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(str(_REPO / "library-onboarding" / ".env"), override=True)

import snow  # noqa: E402

MART = "LIBRARY_MARTS.POLITICS.POLITICS__SCOTUS_JUSTICE"
SRC = "LIBRARY_RAW.LANDING.FED_SCDB"

DDL = f"""
CREATE OR REPLACE TABLE {MART} AS
WITH j AS (
  SELECT
    TRY_TO_NUMBER(JUSTICE)  AS justice_code,
    JUSTICENAME             AS justice_name,
    TRY_TO_NUMBER(TERM)     AS term,
    CASEID                  AS case_id
  FROM {SRC}
  WHERE NULLIF(TRIM(JUSTICENAME), '') IS NOT NULL
    AND TRY_TO_NUMBER(JUSTICE) IS NOT NULL
),
agg AS (
  SELECT
    justice_name,
    MIN(justice_code)       AS justice_code,   -- 1:1 with name (asserted in smoke)
    MIN(term)               AS first_term,
    MAX(term)               AS last_term,
    COUNT(*)                AS n_votes,
    COUNT(DISTINCT case_id) AS n_cases
  FROM j
  GROUP BY justice_name
)
SELECT
  justice_name,                                          -- PK + crosswalk key (STEEL within the closed set)
  justice_code,                                          -- SCDB numeric justice id
  first_term,
  last_term,
  (last_term = (SELECT MAX(last_term) FROM agg))
                              AS is_current_bench,        -- served in the most recent term SCDB holds
  n_votes,
  n_cases,
  'SCDB/Spaeth; JUSTICE_NAME = JCS convention (identity join); FJC via name->nid on land'
                              AS join_note,
  CURRENT_TIMESTAMP()         AS _built_at
FROM agg
ORDER BY first_term, justice_code
"""

# Must-pass proofs. Each: (label, sql -> scalar, predicate).
SMOKE = [
    ("row count == distinct modern justices (expect ~40)",
     f"SELECT COUNT(*) FROM {MART}", lambda v: v >= 35),
    ("justice_name unique (PK integrity)",
     f"SELECT COUNT(*) - COUNT(DISTINCT justice_name) FROM {MART}", lambda v: v == 0),
    ("justice_code unique (1:1 with name)",
     f"SELECT COUNT(*) - COUNT(DISTINCT justice_code) FROM {MART}", lambda v: v == 0),
    ("no null keys",
     f"SELECT COUNT(*) FROM {MART} WHERE justice_name IS NULL OR justice_code IS NULL",
     lambda v: v == 0),
    ("terms in sane range 1946-2025",
     f"SELECT COUNT(*) FROM {MART} WHERE first_term < 1946 OR last_term > 2025",
     lambda v: v == 0),
    ("EXTERNAL anchor: current bench == 9 justices",
     f"SELECT COUNT(*) FROM {MART} WHERE is_current_bench", lambda v: v == 9),
    ("EXTERNAL anchor: WHRehnquist present, 1971-2004",
     f"SELECT COUNT(*) FROM {MART} WHERE justice_name='WHRehnquist' "
     "AND first_term=1971 AND last_term=2004", lambda v: v == 1),
]


def main() -> int:
    print(f"=== build {MART} (from {SRC}) ===", flush=True)
    conn = snow.connect()
    try:
        snow.execute(conn, "CREATE SCHEMA IF NOT EXISTS LIBRARY_MARTS.POLITICS")
        snow.execute(conn, DDL)
        n = snow.fetch_scalar(conn, f"SELECT COUNT(*) FROM {MART}")
        print(f"  built -> {n} justices", flush=True)
        print("\n=== smoke test ===", flush=True)
        ok = True
        for label, sql, check in SMOKE:
            v = snow.fetch_scalar(conn, sql)
            passed = bool(check(v))
            ok = ok and passed
            print(f"  [{'PASS' if passed else 'FAIL'}] {label}  (got {v})", flush=True)
        print(f"\n{'ALL SMOKE PASS' if ok else 'SMOKE FAILED'} -> {MART}", flush=True)
        return 0 if ok else 1
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
