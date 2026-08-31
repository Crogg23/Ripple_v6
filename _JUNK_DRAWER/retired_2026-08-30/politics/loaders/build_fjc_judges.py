#!/usr/bin/env python3
"""Land the FJC Biographical Directory of Article III Federal Judges + build the
judiciary spine and the SCOTUS crosswalk that activates POLITICS__SCOTUS_JUSTICE.

Source (public domain, US gov work): the Federal Judicial Center export CSVs at
https://www.fjc.gov/sites/default/files/history/ .
  * judges.csv                    -- 1 row / judge (nid PK) + demographics
  * federal-judicial-service.csv  -- 1 row / (nid, sequence) appointment (Court Type,
                                     Appointing President, confirmation vote, dates)

Lands two raw mirrors, then builds three additive POLITICS marts:
  POLITICS__FJC_JUDGE              -- judge dimension, STEEL on nid
  POLITICS__FJC_APPOINTMENT        -- appointment/confirmation record, STEEL on nid
  POLITICS__FJC_SCOTUS_CROSSWALK   -- FJC nid <-> SCDB justice_name (name-match, with
                                     match_method + confidence; match rate REPORTED,
                                     not asserted -- detective-trust doctrine). This is
                                     what lets FJC judges bolt onto POLITICS__SCOTUS_JUSTICE.

    python3 politics/loaders/build_fjc_judges.py             # land + build + smoke
    python3 politics/loaders/build_fjc_judges.py --skip-fetch  # rebuild marts only
"""
from __future__ import annotations

import io
import sys
from pathlib import Path as _RepoPath

import pandas as pd
import requests

_REPO = _RepoPath(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO / "library-onboarding"))
sys.path.insert(0, str(_REPO / "politics" / "loaders"))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(str(_REPO / "library-onboarding" / ".env"), override=True)

import snow  # noqa: E402
from build_skeleton import land  # noqa: E402  (shared TEXT-mirror + completeness referee)

BASE = "https://www.fjc.gov/sites/default/files/history/"
UA = {"User-Agent": "Ripple-Library/1.0 (data onboarding; w.rogers9999@gmail.com)"}
FILES = {
    "fed_fjc_judges": ("judges.csv", 4000),                    # (file, min_rows floor)
    "fed_fjc_service": ("federal-judicial-service.csv", 4700),
}


def fetch(fname: str) -> pd.DataFrame:
    r = requests.get(BASE + fname, headers=UA, timeout=120)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.content.decode("utf-8-sig")), dtype=str, keep_default_na=False)
    print(f"  fetched {fname:32} {len(df):>5} rows x {len(df.columns)} cols", flush=True)
    return df


MARTS = [
    ("POLITICS__FJC_JUDGE", """
CREATE OR REPLACE TABLE LIBRARY_MARTS.POLITICS.POLITICS__FJC_JUDGE AS
SELECT
  NULLIF(TRIM(NID),'')                        AS nid,            -- FJC person PK (STEEL)
  NULLIF(TRIM(JID),'')                        AS jid,
  NULLIF(TRIM(LAST_NAME),'')                  AS last_name,
  NULLIF(TRIM(FIRST_NAME),'')                 AS first_name,
  NULLIF(TRIM(MIDDLE_NAME),'')                AS middle_name,
  NULLIF(TRIM(SUFFIX),'')                     AS suffix,
  TRIM(FIRST_NAME || ' ' || IFF(MIDDLE_NAME='','',MIDDLE_NAME||' ') || LAST_NAME
       || IFF(SUFFIX='','',' '||SUFFIX))      AS full_name,
  TRY_TO_NUMBER(BIRTH_YEAR)                   AS birth_year,
  TRY_TO_NUMBER(DEATH_YEAR)                   AS death_year,
  NULLIF(TRIM(GENDER),'')                     AS gender,
  NULLIF(TRIM(RACE_OR_ETHNICITY),'')          AS race_or_ethnicity,
  _INGESTED_AT                                AS _ingested_at
FROM LIBRARY_RAW.LANDING.FED_FJC_JUDGES
WHERE NULLIF(TRIM(NID),'') IS NOT NULL
"""),
    ("POLITICS__FJC_APPOINTMENT", """
CREATE OR REPLACE TABLE LIBRARY_MARTS.POLITICS.POLITICS__FJC_APPOINTMENT AS
SELECT
  NULLIF(TRIM(NID),'')                        AS nid,            -- -> POLITICS__FJC_JUDGE (STEEL)
  TRY_TO_NUMBER(SEQUENCE)                     AS sequence,
  NULLIF(TRIM(JUDGE_NAME),'')                 AS judge_name,
  NULLIF(TRIM(COURT_TYPE),'')                 AS court_type,
  NULLIF(TRIM(COURT_NAME),'')                 AS court_name,
  NULLIF(TRIM(APPOINTMENT_TITLE),'')          AS appointment_title,
  NULLIF(TRIM(APPOINTING_PRESIDENT),'')       AS appointing_president,
  NULLIF(TRIM(PARTY_OF_APPOINTING_PRESIDENT),'') AS party_of_appointing_president,
  NULLIF(TRIM(NOMINATION_DATE),'')            AS nomination_date,
  NULLIF(TRIM(CONFIRMATION_DATE),'')          AS confirmation_date,
  TRY_TO_DATE(CONFIRMATION_DATE,'MM/DD/YYYY') AS confirmation_dt,
  NULLIF(TRIM(AYES_NAYS),'')                  AS ayes_nays,
  NULLIF(TRIM(COMMISSION_DATE),'')            AS commission_date,
  NULLIF(TRIM(TERMINATION_DATE),'')           AS termination_date,
  (NULLIF(TRIM(SERVICE_AS_CHIEF_JUDGE_BEGIN),'') IS NOT NULL) AS is_chief_service,
  _INGESTED_AT                                AS _ingested_at
FROM LIBRARY_RAW.LANDING.FED_FJC_SERVICE
WHERE NULLIF(TRIM(NID),'') IS NOT NULL
"""),
    ("POLITICS__FJC_SCOTUS_CROSSWALK", """
CREATE OR REPLACE TABLE LIBRARY_MARTS.POLITICS.POLITICS__FJC_SCOTUS_CROSSWALK AS
WITH fjc_scotus AS (
  SELECT DISTINCT j.nid, j.last_name,
    UPPER(REGEXP_REPLACE(LEFT(j.first_name,1)||LEFT(COALESCE(j.middle_name,''),1)||j.last_name,'[^A-Za-z]','')) AS cand_fml,
    UPPER(REGEXP_REPLACE(LEFT(j.first_name,1)||j.last_name,'[^A-Za-z]','')) AS cand_fl
  FROM LIBRARY_MARTS.POLITICS.POLITICS__FJC_JUDGE j
  WHERE j.nid IN (SELECT nid FROM LIBRARY_MARTS.POLITICS.POLITICS__FJC_APPOINTMENT
                  WHERE court_type='Supreme Court')
),
scdb AS (
  SELECT justice_name, justice_code, first_term, last_term,
    UPPER(REGEXP_REPLACE(justice_name,'[0-9]+$','')) AS jn_nodigit
  FROM LIBRARY_MARTS.POLITICS.POLITICS__SCOTUS_JUSTICE
),
j AS (
  SELECT s.justice_name, s.justice_code, s.first_term, s.last_term,
    f.nid, f.last_name AS fjc_last_name,
    CASE
      WHEN UPPER(s.justice_name)=f.cand_fml THEN 'first_middle_last'
      WHEN UPPER(s.justice_name)=f.cand_fl  THEN 'first_last'
      WHEN s.jn_nodigit=f.cand_fml          THEN 'first_middle_last_suffixstripped'
      WHEN s.jn_nodigit=f.cand_fl           THEN 'first_last_suffixstripped'
    END AS match_method
  FROM scdb s
  LEFT JOIN fjc_scotus f
    ON UPPER(s.justice_name) IN (f.cand_fml, f.cand_fl)
    OR s.jn_nodigit         IN (f.cand_fml, f.cand_fl)
  QUALIFY ROW_NUMBER() OVER (PARTITION BY s.justice_name ORDER BY (f.nid IS NOT NULL) DESC, f.nid) = 1
)
SELECT
  justice_name,                                          -- SCDB / JCS key
  justice_code, first_term, last_term,
  nid                                        AS fjc_nid, -- FJC person id (STEEL once matched)
  fjc_last_name,
  COALESCE(match_method,'unmatched')         AS match_method,
  (nid IS NOT NULL)                          AS is_matched,
  CASE WHEN match_method LIKE 'first_middle_last%' THEN 0.98
       WHEN match_method LIKE 'first_last%'        THEN 0.90
       ELSE 0.00 END                         AS confidence,
  CURRENT_TIMESTAMP()                        AS _built_at
FROM j
"""),
]


def build_marts(conn) -> None:
    snow.execute(conn, "CREATE SCHEMA IF NOT EXISTS LIBRARY_MARTS.POLITICS")
    for name, ddl in MARTS:
        snow.execute(conn, ddl)
        print(f"  built {name}", flush=True)


def smoke(conn) -> bool:
    def sc(sql):
        return snow.fetch_scalar(conn, sql)
    checks = [
        ("judges landed >= 4000", sc("SELECT COUNT(*) FROM LIBRARY_RAW.LANDING.FED_FJC_JUDGES"), lambda v: v >= 4000),
        ("service landed >= 4700", sc("SELECT COUNT(*) FROM LIBRARY_RAW.LANDING.FED_FJC_SERVICE"), lambda v: v >= 4700),
        ("FJC_JUDGE nid unique (PK)",
         sc("SELECT COUNT(*)-COUNT(DISTINCT nid) FROM LIBRARY_MARTS.POLITICS.POLITICS__FJC_JUDGE"), lambda v: v == 0),
        ("every appointment nid resolves to a judge (0 orphans)",
         sc("SELECT COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__FJC_APPOINTMENT a "
            "LEFT JOIN LIBRARY_MARTS.POLITICS.POLITICS__FJC_JUDGE j USING(nid) WHERE j.nid IS NULL"),
         lambda v: v == 0),
        ("EXTERNAL anchor: 121 Supreme Court appointment rows",
         sc("SELECT COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__FJC_APPOINTMENT WHERE court_type='Supreme Court'"),
         lambda v: v == 121),
        ("crosswalk has 40 SCDB justices",
         sc("SELECT COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__FJC_SCOTUS_CROSSWALK"), lambda v: v == 40),
        ("crosswalk match rate >= 35/40 (reported, not full)",
         sc("SELECT COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__FJC_SCOTUS_CROSSWALK WHERE is_matched"),
         lambda v: v >= 35),
        ("matched fjc_nid all exist in FJC_JUDGE (0 bad)",
         sc("SELECT COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__FJC_SCOTUS_CROSSWALK x WHERE x.is_matched AND NOT EXISTS "
            "(SELECT 1 FROM LIBRARY_MARTS.POLITICS.POLITICS__FJC_JUDGE j WHERE j.nid=x.fjc_nid)"), lambda v: v == 0),
        ("anchor: JGRoberts matched to a Roberts",
         sc("SELECT COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__FJC_SCOTUS_CROSSWALK "
            "WHERE justice_name='JGRoberts' AND is_matched AND fjc_last_name='Roberts'"), lambda v: v == 1),
    ]
    ok = True
    print("\n=== smoke test ===", flush=True)
    for label, val, chk in checks:
        p = bool(chk(val)); ok = ok and p
        print(f"  [{'PASS' if p else 'FAIL'}] {label}  (got {val})", flush=True)
    # report the crosswalk misses (visibility, not a failure)
    rows = conn.cursor().execute(
                        "SELECT justice_name, first_term, last_term FROM "
                        "LIBRARY_MARTS.POLITICS.POLITICS__FJC_SCOTUS_CROSSWALK WHERE NOT is_matched "
                        "ORDER BY first_term").fetchall()
    if rows:
        print(f"\n  UNMATCHED SCOTUS justices ({len(rows)}) -- quarantined, need manual nid:", flush=True)
        for r in rows:
            print(f"    {r[0]:<16} {r[1]}-{r[2]}", flush=True)
    return ok


def main() -> int:
    print("=== FJC Biographical Directory of Article III Judges ===", flush=True)
    if "--skip-fetch" not in sys.argv:
        for sid, (fname, floor) in FILES.items():
            df = fetch(fname)
            land(df, sid, BASE + fname,
                 f"FJC {fname}; one row = one {'judge' if 'judges' in fname else 'appointment'}.",
                 min_rows=floor)
    conn = snow.connect()
    try:
        build_marts(conn)
        ok = smoke(conn)
    finally:
        conn.close()
    print(f"\n{'ALL SMOKE PASS' if ok else 'SMOKE FAILED'} -> LIBRARY_MARTS.POLITICS.POLITICS__FJC_*", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
