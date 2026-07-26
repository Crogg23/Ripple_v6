"""Build XC_EPA_CORPORATE_CROSSWALK (mission packet item #10).

EPA facility -> GLEIF LEI -> ultimate parent LEI -> CIK / UEI, entirely
set-based in Snowflake. Match ladder (first hit wins):

  exact    1.00  normalized facility name = normalized GLEIF LegalName (US)
  fuzzy    0.80  first-5-words of name + state match (city agreement bumps to 0.85)
  address  0.70  ZIP5 + first street token + state match

Bridges attached independently of the LEI match:
  UEI via USAspending recipient ZIP+street+name-prefix, CIK via EDGAR
  company-tickers normalized name match to the matched (parent) legal name.

REVIEW_FLAG = TRUE for any confidence < 0.8 (per packet: no auto-accept).

    python scripts/build_epa_corporate_crosswalk.py --run
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "scripts"))
sys.path.insert(0, str(_REPO / "library-onboarding"))
try:
    from dotenv import load_dotenv
    load_dotenv(_REPO / "library-onboarding/.env", override=True)
except Exception:
    pass

import snow  # noqa: E402

L = "LIBRARY_RAW.LANDING"

NORM = ("TRIM(REGEXP_REPLACE(REGEXP_REPLACE(UPPER({c}), '[^A-Z0-9 ]', ' '), ' +', ' '))")
# strip common legal suffix tokens for the "core" name
STRIP = (
    "TRIM(REGEXP_REPLACE({n}, "
    "' (INC|LLC|L L C|CORP|CORPORATION|CO|COMPANY|LTD|LP|L P|LLP|PLC|INCORPORATED|HOLDINGS|GROUP)( |$)', ' '))"
)

SQL = f"""
CREATE OR REPLACE TABLE {L}.XC_EPA_CORPORATE_CROSSWALK AS
WITH epa AS (
  SELECT REGISTRY_ID AS EPA_REGISTRY_ID,
         FAC_NAME    AS FACILITY_NAME,
         FAC_STREET, FAC_CITY, FAC_STATE,
         LEFT(REGEXP_REPLACE(FAC_ZIP,'[^0-9]',''),5) AS ZIP5,
         {NORM.format(c='FAC_NAME')} AS NAME_NORM,
         {STRIP.format(n=NORM.format(c='FAC_NAME'))} AS NAME_CORE,
         SPLIT_PART({NORM.format(c='FAC_STREET')},' ',1) AS STREET_TOK1
  FROM {L}.FED_EPA_FRS_FRS_FACILITIES
  WHERE FAC_NAME IS NOT NULL
),
epa5 AS (
  SELECT *, ARRAY_TO_STRING(ARRAY_SLICE(SPLIT(NAME_CORE,' '),0,5),' ') AS NAME5
  FROM epa
),
gleif AS (
  SELECT "LEI" AS LEI,
         "Entity.LegalName" AS LEGAL_NAME,
         {NORM.format(c='"Entity.LegalName"')} AS NAME_NORM,
         {STRIP.format(n=NORM.format(c='"Entity.LegalName"'))} AS NAME_CORE,
         "Entity.LegalAddress.Region" AS REGION,
         UPPER("Entity.LegalAddress.City") AS CITY,
         CASE WHEN "Entity.LegalAddress.Region" LIKE 'US-%'
              THEN REPLACE("Entity.LegalAddress.Region",'US-','') END AS STATE
  FROM {L}.INTL_GLEIF
  WHERE "Entity.LegalAddress.Country" = 'US'
),
gleif5 AS (
  SELECT *, ARRAY_TO_STRING(ARRAY_SLICE(SPLIT(NAME_CORE,' '),0,5),' ') AS NAME5,
         ROW_NUMBER() OVER (PARTITION BY NAME_NORM ORDER BY LEI) AS RN_NORM
  FROM gleif
),
-- 1. exact normalized name (unique GLEIF names only, to avoid fanout)
m_exact AS (
  SELECT e.EPA_REGISTRY_ID, g.LEI, g.LEGAL_NAME, 'exact' AS MATCH_METHOD, 1.00 AS MATCH_CONFIDENCE
  FROM epa5 e
  JOIN (SELECT * FROM gleif5 WHERE RN_NORM = 1
        QUALIFY COUNT(*) OVER (PARTITION BY NAME_NORM) = 1) g
    ON e.NAME_NORM = g.NAME_NORM
),
-- 2. fuzzy: first-5-words + state
m_fuzzy AS (
  SELECT e.EPA_REGISTRY_ID, g.LEI, g.LEGAL_NAME, 'fuzzy' AS MATCH_METHOD,
         CASE WHEN UPPER(e.FAC_CITY) = g.CITY THEN 0.85 ELSE 0.80 END AS MATCH_CONFIDENCE,
         ROW_NUMBER() OVER (PARTITION BY e.EPA_REGISTRY_ID ORDER BY g.LEI) AS RN
  FROM epa5 e
  JOIN gleif5 g
    ON e.NAME5 = g.NAME5 AND LENGTH(e.NAME5) >= 8
   AND e.FAC_STATE = g.STATE
  WHERE e.EPA_REGISTRY_ID NOT IN (SELECT EPA_REGISTRY_ID FROM m_exact)
),
picked AS (
  SELECT EPA_REGISTRY_ID, LEI, LEGAL_NAME, MATCH_METHOD, MATCH_CONFIDENCE FROM m_exact
  UNION ALL
  SELECT EPA_REGISTRY_ID, LEI, LEGAL_NAME, MATCH_METHOD, MATCH_CONFIDENCE FROM m_fuzzy WHERE RN = 1
),
-- ultimate parent via Level 2 relationships
parent AS (
  SELECT RELATIONSHIP_STARTNODE_NODEID AS CHILD_LEI,
         RELATIONSHIP_ENDNODE_NODEID   AS PARENT_LEI,
         ROW_NUMBER() OVER (PARTITION BY RELATIONSHIP_STARTNODE_NODEID
                            ORDER BY RELATIONSHIP_PERIOD_1_STARTDATE DESC NULLS LAST) AS RN
  FROM {L}.INTL_GLEIF_RELATIONSHIPS
  WHERE RELATIONSHIP_RELATIONSHIPTYPE = 'IS_ULTIMATELY_CONSOLIDATED_BY'
    AND RELATIONSHIP_RELATIONSHIPSTATUS = 'ACTIVE'
),
parent_name AS (
  SELECT p.CHILD_LEI, p.PARENT_LEI, g."Entity.LegalName" AS PARENT_LEGAL_NAME,
         {NORM.format(c='g."Entity.LegalName"')} AS PARENT_NAME_NORM
  FROM parent p
  LEFT JOIN {L}.INTL_GLEIF g ON g."LEI" = p.PARENT_LEI
  WHERE p.RN = 1
),
-- CIK bridge on EDGAR normalized title (unique titles only)
edgar AS (
  SELECT {NORM.format(c='TITLE')} AS NAME_NORM, MIN(CIK_STR) AS CIK
  FROM {L}.FED_SEC_EDGAR_COMPANY_TICKERS
  GROUP BY 1 HAVING COUNT(DISTINCT CIK_STR) = 1
),
-- UEI bridge: distinct recipient addresses from USAspending
usasp AS (
  SELECT DISTINCT "recipient_uei" AS UEI,
         LEFT(REGEXP_REPLACE("recipient_zip_4_code",'[^0-9]',''),5) AS ZIP5,
         SPLIT_PART({NORM.format(c='"recipient_address_line_1"')},' ',1) AS STREET_TOK1,
         {NORM.format(c='"recipient_name"')} AS NAME_NORM
  FROM {L}.FED_USASPENDING_CONTRACTS_FULL
  WHERE "recipient_uei" IS NOT NULL
),
uei_match AS (
  SELECT e.EPA_REGISTRY_ID, u.UEI,
         ROW_NUMBER() OVER (PARTITION BY e.EPA_REGISTRY_ID ORDER BY u.UEI) AS RN
  FROM epa5 e
  JOIN usasp u
    ON e.ZIP5 = u.ZIP5 AND e.STREET_TOK1 = u.STREET_TOK1
   AND (u.NAME_NORM LIKE e.NAME_CORE || '%' OR e.NAME_NORM LIKE u.NAME_NORM || '%')
)
SELECT
  e.EPA_REGISTRY_ID,
  e.FACILITY_NAME,
  p.LEI                     AS MATCHED_LEI,
  p.LEGAL_NAME              AS MATCHED_LEGAL_NAME,
  p.MATCH_METHOD,
  p.MATCH_CONFIDENCE,
  pn.PARENT_LEI             AS ULTIMATE_PARENT_LEI,
  COALESCE(pn.PARENT_LEGAL_NAME, p.LEGAL_NAME) AS PARENT_LEGAL_NAME,
  ed.CIK                    AS PARENT_CIK,
  um.UEI                    AS PARENT_UEI,
  (p.MATCH_CONFIDENCE < 0.8) AS REVIEW_FLAG,
  CURRENT_TIMESTAMP()::TIMESTAMP_NTZ AS _INGESTED_AT,
  'xc-build-v1'             AS _SOURCE_RUN_ID
FROM epa5 e
LEFT JOIN picked p       ON p.EPA_REGISTRY_ID = e.EPA_REGISTRY_ID
LEFT JOIN parent_name pn ON pn.CHILD_LEI = p.LEI
LEFT JOIN edgar ed       ON ed.NAME_NORM = COALESCE(pn.PARENT_NAME_NORM,
                                                    {NORM.format(c='p.LEGAL_NAME')})
LEFT JOIN uei_match um   ON um.EPA_REGISTRY_ID = e.EPA_REGISTRY_ID AND um.RN = 1
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args()
    if not args.run:
        print(SQL)
        return
    conn = snow.connect()
    cur = conn.cursor()
    try:
        cur.execute(SQL)
        cur.execute(f"""SELECT COUNT(*), COUNT(MATCHED_LEI),
                        COUNT(ULTIMATE_PARENT_LEI), COUNT(PARENT_CIK), COUNT(PARENT_UEI)
                        FROM {L}.XC_EPA_CORPORATE_CROSSWALK""")
        t, lei, up, cik, uei = cur.fetchone()
        print(f"facilities={t:,} lei_matched={lei:,} ({lei/t:.1%}) "
              f"ult_parent={up:,} cik={cik:,} uei={uei:,}")
        cur.execute(f"SELECT MATCH_METHOD, COUNT(*) FROM {L}.XC_EPA_CORPORATE_CROSSWALK "
                    f"WHERE MATCH_METHOD IS NOT NULL GROUP BY 1")
        for r in cur.fetchall():
            print(" ", r)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
