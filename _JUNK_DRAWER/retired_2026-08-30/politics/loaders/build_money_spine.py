"""Phase 2 -- close the clean money spine + the first box-score stat: money raised.

Lands 3 FEC bulk files (cn / ccl / weball) for cycles 2024 + 2026 (CYCLE grain
preserved), then builds 4 additive marts in LIBRARY_MARTS.POLITICS:

  POLITICS__FEC_CANDIDATE          (CAND_ID, CYCLE)            candidate identity
  POLITICS__FEC_CAND_CMTE_LINK     (CAND_ID, CMTE_ID, CYCLE)   the linkage bridge
  POLITICS__FEC_CANDIDATE_SUMMARY  (CAND_ID, CYCLE)            dollars (the only $ file)
  POLITICS__MEMBER_MONEY_RAISED    (BIOGUIDE, CYCLE)           the payoff stat

Identity graph closed: bioguide -> fec_cand_id -> CAND_ID (candidate) -> linkage
-> CMTE_ID -> committee master (fed_fec_bulk).

Money raised is computed NET of inter-committee transfers
(net_receipts = TTL_RECEIPTS - TRANS_FROM_AUTH) so it is NOT double-counted.

Usage:
  python politics/loaders/build_money_spine.py              # fetch + land + build
  python politics/loaders/build_money_spine.py --skip-fetch # rebuild marts only
"""
from __future__ import annotations
import io
import sys
import zipfile

import pandas as pd
import requests

from pathlib import Path as _RepoPath
_REPO = _RepoPath(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO / "library-onboarding"))
sys.path.insert(0, str(_REPO / "politics" / "loaders"))
import snow  # noqa: E402
from build_skeleton import land  # noqa: E402  (reuse the first-class land() helper)

CYCLES = {"2024": "24", "2026": "26"}

# FEC column layouts. cn/ccl confirmed live from the FEC header files; weball is
# FEC's documented all-candidates layout (its header file 404s) -- validated at
# load by the field-count check in read_fec().
CN_COLS = ["CAND_ID", "CAND_NAME", "CAND_PTY_AFFILIATION", "CAND_ELECTION_YR", "CAND_OFFICE_ST",
           "CAND_OFFICE", "CAND_OFFICE_DISTRICT", "CAND_ICI", "CAND_STATUS", "CAND_PCC",
           "CAND_ST1", "CAND_ST2", "CAND_CITY", "CAND_ST", "CAND_ZIP"]
CCL_COLS = ["CAND_ID", "CAND_ELECTION_YR", "FEC_ELECTION_YR", "CMTE_ID", "CMTE_TP", "CMTE_DSGN", "LINKAGE_ID"]
WEBALL_COLS = ["CAND_ID", "CAND_NAME", "CAND_ICI", "PTY_CD", "CAND_PTY_AFFILIATION", "TTL_RECEIPTS",
               "TRANS_FROM_AUTH", "TTL_DISB", "TRANS_TO_AUTH", "COH_BOP", "COH_COP", "CAND_CONTRIB",
               "CAND_LOANS", "OTHER_LOANS", "CAND_LOAN_REPAY", "OTHER_LOAN_REPAY", "DEBTS_OWED_BY",
               "TTL_INDIV_CONTRIB", "CAND_OFFICE_ST", "CAND_OFFICE_DISTRICT", "SPEC_ELECTION",
               "PRIM_ELECTION", "RUN_ELECTION", "GEN_ELECTION", "GEN_ELECTION_PRECENT",
               "OTHER_POL_CMTE_CONTRIB", "POL_PTY_CONTRIB", "CVG_END_DT", "INDIV_REFUNDS", "CMTE_REFUNDS"]

FILES = {
    "cn":     (CN_COLS,     "fed_fec_bulk_candidates"),
    "ccl":    (CCL_COLS,    "fed_fec_bulk_linkages"),
    "weball": (WEBALL_COLS, "fed_fec_bulk_summary"),
}


def read_fec(content: bytes, cols, label: str) -> pd.DataFrame:
    """Parse a pipe-delimited FEC bulk file (no header). Reports field-count
    mismatches loudly -- inspect-before-load, never silently mis-shape."""
    text = content.decode("latin-1")
    rows, bad = [], 0
    for line in text.splitlines():
        if not line.strip():
            continue
        parts = line.split("|")
        if len(parts) != len(cols):
            bad += 1
            parts = (parts + [""] * len(cols))[:len(cols)]
        rows.append(parts)
    df = pd.DataFrame(rows, columns=cols)
    if bad:
        print(f"    [{label}] WARNING: {bad}/{len(df)} rows had a field-count mismatch (padded/truncated)")
    return df


def fetch_file(prefix: str, cols, cycle: str, yy: str) -> pd.DataFrame:
    url = f"https://www.fec.gov/files/bulk-downloads/{cycle}/{prefix}{yy}.zip"
    r = requests.get(url, timeout=180)
    r.raise_for_status()
    zf = zipfile.ZipFile(io.BytesIO(r.content))
    txt_name = [n for n in zf.namelist() if n.lower().endswith(".txt")][0]
    df = read_fec(zf.read(txt_name), cols, f"{prefix}{yy}")
    df["CYCLE"] = cycle
    print(f"    {prefix}{yy}: {len(df):,} rows  (inner={txt_name})")
    return df


def fetch_and_land():
    for prefix, (cols, source_id) in FILES.items():
        parts = [fetch_file(prefix, cols, cyc, yy) for cyc, yy in CYCLES.items()]
        df = pd.concat(parts, ignore_index=True)
        land(df, source_id, f"https://www.fec.gov/files/bulk-downloads/",
             f"FEC bulk {prefix} (cycles {'+'.join(CYCLES)}); one row = one record per cycle.")


# ---------------------------------------------------------------------------
# Marts (additive, POLITICS namespace). Cycle grain preserved on every key.
# ---------------------------------------------------------------------------
DDL = [
("mart fec_candidate", """
CREATE OR REPLACE TABLE LIBRARY_MARTS.POLITICS.POLITICS__FEC_CANDIDATE AS
SELECT
  NULLIF(TRIM(CAND_ID),'')                         AS cand_id,
  CYCLE                                            AS cycle,
  NULLIF(TRIM(CAND_NAME),'')                       AS cand_name,
  NULLIF(TRIM(CAND_PTY_AFFILIATION),'')            AS party,
  NULLIF(TRIM(CAND_OFFICE),'')                     AS office,
  NULLIF(TRIM(CAND_OFFICE_ST),'')                  AS office_state,
  NULLIF(TRIM(CAND_OFFICE_DISTRICT),'')            AS office_district,
  NULLIF(TRIM(CAND_ICI),'')                        AS incumbent_challenger,
  NULLIF(TRIM(CAND_STATUS),'')                     AS cand_status,
  NULLIF(TRIM(CAND_PCC),'')                        AS principal_cmte_id,
  TRY_TO_NUMBER(NULLIF(TRIM(CAND_ELECTION_YR),'')) AS cand_election_yr
FROM LIBRARY_RAW.LANDING.FED_FEC_BULK_CANDIDATES
WHERE NULLIF(TRIM(CAND_ID),'') IS NOT NULL
QUALIFY ROW_NUMBER() OVER (PARTITION BY cand_id, cycle ORDER BY cand_election_yr DESC NULLS LAST) = 1
"""),

("mart fec_cand_cmte_link", """
CREATE OR REPLACE TABLE LIBRARY_MARTS.POLITICS.POLITICS__FEC_CAND_CMTE_LINK AS
SELECT
  NULLIF(TRIM(CAND_ID),'')                         AS cand_id,
  NULLIF(TRIM(CMTE_ID),'')                         AS cmte_id,
  CYCLE                                            AS cycle,
  NULLIF(TRIM(CMTE_TP),'')                         AS cmte_tp,
  NULLIF(TRIM(CMTE_DSGN),'')                       AS cmte_dsgn,
  TRY_TO_NUMBER(NULLIF(TRIM(CAND_ELECTION_YR),'')) AS cand_election_yr,
  TRY_TO_NUMBER(NULLIF(TRIM(FEC_ELECTION_YR),''))  AS fec_election_yr,
  NULLIF(TRIM(LINKAGE_ID),'')                      AS linkage_id
FROM LIBRARY_RAW.LANDING.FED_FEC_BULK_LINKAGES
WHERE NULLIF(TRIM(CAND_ID),'') IS NOT NULL AND NULLIF(TRIM(CMTE_ID),'') IS NOT NULL
QUALIFY ROW_NUMBER() OVER (PARTITION BY cand_id, cmte_id, cycle ORDER BY linkage_id) = 1
"""),

("mart fec_candidate_summary", """
CREATE OR REPLACE TABLE LIBRARY_MARTS.POLITICS.POLITICS__FEC_CANDIDATE_SUMMARY AS
SELECT
  NULLIF(TRIM(CAND_ID),'')                                 AS cand_id,
  CYCLE                                                    AS cycle,
  NULLIF(TRIM(CAND_NAME),'')                               AS cand_name,
  NULLIF(TRIM(CAND_ICI),'')                                AS incumbent_challenger,
  NULLIF(TRIM(CAND_PTY_AFFILIATION),'')                    AS party,
  TRY_TO_DECIMAL(NULLIF(TRIM(TTL_RECEIPTS),''), 18, 2)     AS ttl_receipts,
  TRY_TO_DECIMAL(NULLIF(TRIM(TRANS_FROM_AUTH),''), 18, 2)  AS trans_from_auth,
  TRY_TO_DECIMAL(NULLIF(TRIM(TTL_DISB),''), 18, 2)         AS ttl_disb,
  TRY_TO_DECIMAL(NULLIF(TRIM(TRANS_TO_AUTH),''), 18, 2)    AS trans_to_auth,
  TRY_TO_DECIMAL(NULLIF(TRIM(COH_COP),''), 18, 2)          AS cash_on_hand_close,
  TRY_TO_DECIMAL(NULLIF(TRIM(TTL_INDIV_CONTRIB),''), 18, 2) AS ttl_indiv_contrib,
  TRY_TO_DECIMAL(NULLIF(TRIM(DEBTS_OWED_BY),''), 18, 2)    AS debts_owed_by,
  NULLIF(TRIM(CVG_END_DT),'')                              AS coverage_end_date,
  -- NET of inter-committee transfers (de-double-counted; the publishable figures)
  COALESCE(TRY_TO_DECIMAL(NULLIF(TRIM(TTL_RECEIPTS),''),18,2),0)
    - COALESCE(TRY_TO_DECIMAL(NULLIF(TRIM(TRANS_FROM_AUTH),''),18,2),0) AS net_receipts,
  COALESCE(TRY_TO_DECIMAL(NULLIF(TRIM(TTL_DISB),''),18,2),0)
    - COALESCE(TRY_TO_DECIMAL(NULLIF(TRIM(TRANS_TO_AUTH),''),18,2),0)   AS net_disbursements
FROM LIBRARY_RAW.LANDING.FED_FEC_BULK_SUMMARY
WHERE NULLIF(TRIM(CAND_ID),'') IS NOT NULL
QUALIFY ROW_NUMBER() OVER (PARTITION BY cand_id, cycle ORDER BY coverage_end_date DESC NULLS LAST) = 1
"""),

("mart member_money_raised", """
CREATE OR REPLACE TABLE LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_MONEY_RAISED AS
WITH member_cand AS (
  -- SITTING members only -> their FEC candidate IDs (1:many)
  SELECT DISTINCT s.bioguide, s.full_name, s.party, s.state, s.last_term_type, b.fec_id AS cand_id
  FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_SPINE s
  JOIN LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_FEC_ID b ON b.bioguide = s.bioguide
  WHERE s.legislator_set = 'current'
),
joined AS (
  -- join on (cand_id, cycle): naturally keeps only the CAND_IDs active in each cycle
  SELECT mc.bioguide, mc.full_name, mc.party, mc.state, mc.last_term_type, mc.cand_id,
         fs.cycle, fs.ttl_receipts, fs.trans_from_auth, fs.net_receipts, fs.cash_on_hand_close
  FROM member_cand mc
  JOIN LIBRARY_MARTS.POLITICS.POLITICS__FEC_CANDIDATE_SUMMARY fs ON fs.cand_id = mc.cand_id
)
SELECT
  bioguide,
  cycle,
  ANY_VALUE(full_name)                 AS full_name,
  ANY_VALUE(party)                     AS party,
  ANY_VALUE(state)                     AS state,
  ANY_VALUE(last_term_type)            AS chamber,
  COUNT(DISTINCT cand_id)              AS n_candidate_ids,
  ARRAY_AGG(DISTINCT cand_id) WITHIN GROUP (ORDER BY cand_id) AS cand_ids,
  SUM(ttl_receipts)                    AS ttl_receipts_gross,
  SUM(trans_from_auth)                 AS trans_from_auth,
  SUM(net_receipts)                    AS money_raised_net,   -- THE STAT
  SUM(cash_on_hand_close)              AS cash_on_hand_close
FROM joined
GROUP BY bioguide, cycle
"""),
]


def build_models():
    conn = snow.connect()
    cur = conn.cursor()
    try:
        for label, sql in DDL:
            cur.execute(sql)
            print(f"  built {label}")
        conn.commit()
        checks = {
            "fec_candidate_rows": "SELECT COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_CANDIDATE",
            "fec_candidate_dupe_key": "SELECT COUNT(*) FROM (SELECT cand_id,cycle FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_CANDIDATE GROUP BY 1,2 HAVING COUNT(*)>1)",
            "link_rows": "SELECT COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_CAND_CMTE_LINK",
            "link_dupe_key": "SELECT COUNT(*) FROM (SELECT cand_id,cmte_id,cycle FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_CAND_CMTE_LINK GROUP BY 1,2,3 HAVING COUNT(*)>1)",
            "summary_rows": "SELECT COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_CANDIDATE_SUMMARY",
            "summary_dupe_key": "SELECT COUNT(*) FROM (SELECT cand_id,cycle FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_CANDIDATE_SUMMARY GROUP BY 1,2 HAVING COUNT(*)>1)",
            "summary_with_receipts": "SELECT COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_CANDIDATE_SUMMARY WHERE ttl_receipts IS NOT NULL",
            "money_raised_rows": "SELECT COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_MONEY_RAISED",
            "money_raised_members": "SELECT COUNT(DISTINCT bioguide) FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_MONEY_RAISED",
            "money_raised_dupe_key": "SELECT COUNT(*) FROM (SELECT bioguide,cycle FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_MONEY_RAISED GROUP BY 1,2 HAVING COUNT(*)>1)",
            "by_cycle": "SELECT cycle, COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_MONEY_RAISED GROUP BY 1 ORDER BY 1",
        }
        print("\nINTEGRITY:")
        for k, q in checks.items():
            cur.execute(q)
            print(f"  {k:<26} {cur.fetchall()}")
    finally:
        cur.close()
        conn.close()


def main(skip_fetch: bool):
    if not skip_fetch:
        print("FETCH + LAND (3 files x 2 cycles):")
        fetch_and_land()
    print("\nBUILD MARTS:")
    build_models()
    print("\nDONE.")


if __name__ == "__main__":
    main(skip_fetch="--skip-fetch" in sys.argv)
