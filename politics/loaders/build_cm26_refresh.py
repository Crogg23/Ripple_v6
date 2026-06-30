"""Maintenance pass -- refresh the FEC committee master to the 2026 (cm26) snapshot
and re-resolve the 2026 candidate->committee linkages.

WHY: Phase 2 landed the committee master from a 2024 snapshot (LANDING.FED_FEC_BULK,
20,938 rows, NO cycle column). 2026 (119th-cycle) linkage CMTE_IDs therefore resolve
only ~57% against it (2024 resolves ~98%) -- the gap is staleness, not error.

ADDITIVE-ONLY design (the committee master is a single-snapshot table with no cycle
column, so per the handoff we do NOT overwrite it):
  1. Land the 2026 committee master (cm26) as its OWN landing object keyed by cycle:
       LIBRARY_RAW.LANDING.FED_FEC_BULK_COMMITTEES   (cm 15-col layout + CYCLE='2026')
     The verified 2024 FED_FEC_BULK is never written -- it stays byte-for-byte.
  2. Build the cycle-aware committee master mart (the UNION the linkages resolve against):
       LIBRARY_MARTS.POLITICS.POLITICS__FEC_COMMITTEE  (CMTE_ID, CYCLE)
       2024 rows from FED_FEC_BULK (read-only) + 2026 rows from the new landing.
  3. Re-resolve: 2026 POLITICS__FEC_CAND_CMTE_LINK against the 2026 committee rows.

Touches no 2024 data and no existing object. New landing table + new mart only.

Usage:
  python politics/loaders/build_cm26_refresh.py              # fetch + land + build
  python politics/loaders/build_cm26_refresh.py --skip-fetch # rebuild the mart only
"""
from __future__ import annotations
import io
import sys
import zipfile

import requests

sys.path.insert(0, r"c:\Code\Ripple_v6\library-onboarding")
sys.path.insert(0, r"c:\Code\Ripple_v6\politics\loaders")
import snow  # noqa: E402
from build_skeleton import land  # noqa: E402  (the first-class land() helper)
from build_money_spine import read_fec  # noqa: E402  (the pipe-delimited FEC parser)

CYCLE = "2026"
YY = "26"
SOURCE_ID = "fed_fec_bulk_committees"

# FEC committee master (cm) layout = 15 fields. Column names renamed to MATCH the
# existing committee master (FED_FEC_BULK: CMTE_ID->FEC_CMTE_ID, CAND_ID->FEC_CAND_ID)
# so the cycle-aware union mart is symmetric across both snapshots.
CM_COLS = ["FEC_CMTE_ID", "CMTE_NM", "TRES_NM", "CMTE_ST1", "CMTE_ST2", "CMTE_CITY", "CMTE_ST",
           "CMTE_ZIP", "CMTE_DSGN", "CMTE_TP", "CMTE_PTY_AFFILIATION", "CMTE_FILING_FREQ",
           "ORG_TP", "CONNECTED_ORG_NM", "FEC_CAND_ID"]

CM_URL = f"https://www.fec.gov/files/bulk-downloads/{CYCLE}/cm{YY}.zip"


def fetch_and_land():
    print(f"FETCH cm{YY} -- {CM_URL}")
    r = requests.get(CM_URL, timeout=180)
    r.raise_for_status()
    zf = zipfile.ZipFile(io.BytesIO(r.content))
    txt_name = [n for n in zf.namelist() if n.lower().endswith(".txt")][0]
    df = read_fec(zf.read(txt_name), CM_COLS, f"cm{YY}")
    df["CYCLE"] = CYCLE
    print(f"    cm{YY}: {len(df):,} rows  (inner={txt_name})")
    # Idempotent snapshot-replace into the NEW landing object (never FED_FEC_BULK).
    land(df, SOURCE_ID, CM_URL,
         f"FEC bulk committee master cm{YY} (cycle {CYCLE}); one row = one committee. "
         f"Cycle-keyed refresh; complements the 2024 snapshot in fed_fec_bulk.")


# ---------------------------------------------------------------------------
# The cycle-aware committee master mart -- the UNION the linkages resolve against.
# 2024 rows come from the untouched FED_FEC_BULK (read-only); 2026 from the new land.
# Keyed (cmte_id, cycle). NEW object -> additive.
# ---------------------------------------------------------------------------
MART_SQL = """
CREATE OR REPLACE TABLE LIBRARY_MARTS.POLITICS.POLITICS__FEC_COMMITTEE AS
WITH unioned AS (
  -- 2024 snapshot (existing committee master, labeled cycle 2024; read-only)
  SELECT
    NULLIF(TRIM(FEC_CMTE_ID),'')          AS cmte_id,
    '2024'                                AS cycle,
    NULLIF(TRIM(CMTE_NM),'')              AS cmte_nm,
    NULLIF(TRIM(TRES_NM),'')              AS tres_nm,
    NULLIF(TRIM(CMTE_CITY),'')            AS cmte_city,
    NULLIF(TRIM(CMTE_ST),'')              AS cmte_st,
    NULLIF(TRIM(CMTE_ZIP),'')             AS cmte_zip,
    NULLIF(TRIM(CMTE_DSGN),'')            AS cmte_dsgn,
    NULLIF(TRIM(CMTE_TP),'')              AS cmte_tp,
    NULLIF(TRIM(CMTE_PTY_AFFILIATION),'') AS cmte_pty_affiliation,
    NULLIF(TRIM(CMTE_FILING_FREQ),'')     AS cmte_filing_freq,
    NULLIF(TRIM(ORG_TP),'')               AS org_tp,
    NULLIF(TRIM(CONNECTED_ORG_NM),'')     AS connected_org_nm,
    NULLIF(TRIM(FEC_CAND_ID),'')          AS cand_id
  FROM LIBRARY_RAW.LANDING.FED_FEC_BULK
  UNION ALL
  -- 2026 refresh (the new cm26 landing object)
  SELECT
    NULLIF(TRIM(FEC_CMTE_ID),'')          AS cmte_id,
    CYCLE                                 AS cycle,
    NULLIF(TRIM(CMTE_NM),'')              AS cmte_nm,
    NULLIF(TRIM(TRES_NM),'')              AS tres_nm,
    NULLIF(TRIM(CMTE_CITY),'')            AS cmte_city,
    NULLIF(TRIM(CMTE_ST),'')              AS cmte_st,
    NULLIF(TRIM(CMTE_ZIP),'')             AS cmte_zip,
    NULLIF(TRIM(CMTE_DSGN),'')            AS cmte_dsgn,
    NULLIF(TRIM(CMTE_TP),'')              AS cmte_tp,
    NULLIF(TRIM(CMTE_PTY_AFFILIATION),'') AS cmte_pty_affiliation,
    NULLIF(TRIM(CMTE_FILING_FREQ),'')     AS cmte_filing_freq,
    NULLIF(TRIM(ORG_TP),'')               AS org_tp,
    NULLIF(TRIM(CONNECTED_ORG_NM),'')     AS connected_org_nm,
    NULLIF(TRIM(FEC_CAND_ID),'')          AS cand_id
  FROM LIBRARY_RAW.LANDING.FED_FEC_BULK_COMMITTEES
)
SELECT *
FROM unioned
WHERE cmte_id IS NOT NULL
QUALIFY ROW_NUMBER() OVER (PARTITION BY cmte_id, cycle ORDER BY cmte_nm NULLS LAST) = 1
"""

LINK = "LIBRARY_MARTS.POLITICS.POLITICS__FEC_CAND_CMTE_LINK"
CMTE = "LIBRARY_MARTS.POLITICS.POLITICS__FEC_COMMITTEE"
OLD_CM = "LIBRARY_RAW.LANDING.FED_FEC_BULK"


def build_and_resolve():
    conn = snow.connect()
    cur = conn.cursor()
    try:
        cur.execute(MART_SQL)
        conn.commit()
        print("  built mart POLITICS__FEC_COMMITTEE (cycle-aware committee master)")

        def rows(sql, p=()):
            cur.execute(sql, p)
            return cur.fetchall()

        print("\nMART INTEGRITY:")
        print("  committee rows by cycle      :",
              rows(f"SELECT cycle, COUNT(*) FROM {CMTE} GROUP BY cycle ORDER BY cycle"))
        print("  dup (cmte_id, cycle)         :",
              rows(f"SELECT COUNT(*) FROM (SELECT cmte_id,cycle FROM {CMTE} GROUP BY 1,2 HAVING COUNT(*)>1)")[0][0])
        print("  distinct committees by cycle :",
              rows(f"SELECT cycle, COUNT(DISTINCT cmte_id) FROM {CMTE} GROUP BY cycle ORDER BY cycle"))

        # RE-RESOLVE: 2026 linkages against the cycle-matched committee rows.
        print("\nRE-RESOLUTION  (2026 linkages -> committee master):")
        print("  BEFORE (vs 2024-only snapshot FED_FEC_BULK):")
        print("   ", rows(f"""
            SELECT l.cycle, COUNT(*) AS link_rows,
                   SUM(IFF(cm.FEC_CMTE_ID IS NOT NULL,1,0)) AS resolved,
                   ROUND(100.0*SUM(IFF(cm.FEC_CMTE_ID IS NOT NULL,1,0))/COUNT(*),2) AS pct
            FROM {LINK} l
            LEFT JOIN (SELECT DISTINCT FEC_CMTE_ID FROM {OLD_CM}) cm ON cm.FEC_CMTE_ID = l.cmte_id
            GROUP BY l.cycle ORDER BY l.cycle"""))
        print("  AFTER (vs cycle-aware mart POLITICS__FEC_COMMITTEE, matched on cycle):")
        print("   ", rows(f"""
            SELECT l.cycle, COUNT(*) AS link_rows,
                   SUM(IFF(c.cmte_id IS NOT NULL,1,0)) AS resolved,
                   ROUND(100.0*SUM(IFF(c.cmte_id IS NOT NULL,1,0))/COUNT(*),2) AS pct
            FROM {LINK} l
            LEFT JOIN {CMTE} c ON c.cmte_id = l.cmte_id AND c.cycle = l.cycle
            GROUP BY l.cycle ORDER BY l.cycle"""))
    finally:
        cur.close()
        conn.close()


def main(skip_fetch: bool):
    if not skip_fetch:
        fetch_and_land()
    print("\nBUILD MART + RE-RESOLVE:")
    build_and_resolve()
    print("\nDONE.")


if __name__ == "__main__":
    main(skip_fetch="--skip-fetch" in sys.argv)
