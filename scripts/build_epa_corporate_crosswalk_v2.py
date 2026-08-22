"""Extend XC_EPA_CORPORATE_CROSSWALK with a brand-token match pass (v2).

v1 ladder (exact 1.00 / fuzzy 0.80-0.85 / address-UEI) only matched whole
names, so chain facilities ("WALMART SUPERCENTER #4821") never reached
their parent. v2 adds:

  brand    0.75  first token of facility name (len>=5, not blocklisted)
                 = first token of a GLEIF-US company core name, where that
                 token resolves to exactly one preferred parent entity
                 (prefer: is an ultimate parent in the ownership graph,
                 then most children, then shortest name).

All brand matches carry REVIEW_FLAG = TRUE (confidence < 0.8 -> no
auto-accept, same rule as v1). v1 matches are preserved untouched; brand
fills only rows v1 left unmatched.

    python scripts/build_epa_corporate_crosswalk_v2.py --run
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "scripts"))

from _snowflake_conn import connect  # noqa: E402

L = "LIBRARY_RAW.LANDING"

NORM = ("TRIM(REGEXP_REPLACE(REGEXP_REPLACE(UPPER({c}), '[^A-Z0-9 ]', ' '), ' +', ' '))")

# prefixes that look like brands but are governments, generic words, or programs
BLOCKLIST = """('CITY','TOWN','COUNTY','VILLAGE','STATE','RESIDENCE','RESIDENTIAL','UNIVERSITY',
 'SCHOOL','UNITED','FORMER','PRIVATE','PUBLIC','NORTH','SOUTH','WEST','EAST','LAKE','RIVER',
 'GRAND','FIRST','GENERAL','NATIONAL','AMERICAN','TRACT','PARCEL','UNKNOWN','VACANT','ABANDONED',
 'HIGHWAY','ROUTE','INTERSTATE','DEPARTMENT','BUREAU','OFFICE','AGENCY','DISTRICT','AUTHORITY',
 'BOARD','HOUSE','BUILDING','PROPERTY','SITE','WELL','MINE','LANDFILL','FARM','RANCH','STORE',
 'STATION','PLANT','FACILITY','CENTER','CENTRE','MAIN','OLD','NEW')"""

SQL = f"""
CREATE OR REPLACE TABLE {L}.XC_EPA_CORPORATE_CROSSWALK AS
WITH prev AS (
  SELECT * FROM {L}.XC_EPA_CORPORATE_CROSSWALK
),
epa_unmatched AS (
  SELECT f.REGISTRY_ID AS EPA_REGISTRY_ID,
         f.PRIMARY_NAME AS FACILITY_NAME,
         {NORM.format(c='f.PRIMARY_NAME')} AS NAME_NORM,
         SPLIT_PART({NORM.format(c='f.PRIMARY_NAME')},' ',1) AS TOK1
  FROM {L}.FED_EPA_FRS_FULL f
  JOIN prev p ON p.EPA_REGISTRY_ID = f.REGISTRY_ID
  WHERE p.MATCHED_LEI IS NULL AND f.PRIMARY_NAME IS NOT NULL
),
-- brand candidates: first tokens with real scale, alphabetic, len>=5, not blocklisted
brands AS (
  SELECT TOK1 AS BRAND, COUNT(*) AS N_FAC
  FROM epa_unmatched
  WHERE LENGTH(TOK1) >= 5 AND TOK1 REGEXP '[A-Z]+' AND TOK1 NOT IN {BLOCKLIST}
  GROUP BY 1
  HAVING COUNT(*) >= 500
),
gleif AS (
  SELECT "LEI" AS LEI, "Entity.LegalName" AS LEGAL_NAME,
         {NORM.format(c='"Entity.LegalName"')} AS NAME_NORM,
         SPLIT_PART({NORM.format(c='"Entity.LegalName"')},' ',1) AS TOK1
  FROM {L}.INTL_GLEIF
  WHERE "Entity.LegalAddress.Country" = 'US'
),
-- how parental is each entity: number of children it ultimately consolidates
parent_deg AS (
  SELECT RELATIONSHIP_ENDNODE_NODEID AS LEI, COUNT(*) AS N_CHILDREN
  FROM {L}.INTL_GLEIF_RELATIONSHIPS
  WHERE RELATIONSHIP_RELATIONSHIPTYPE = 'IS_ULTIMATELY_CONSOLIDATED_BY'
  GROUP BY 1
),
-- one preferred entity per brand token
brand_target AS (
  SELECT b.BRAND, g.LEI, g.LEGAL_NAME,
         ROW_NUMBER() OVER (PARTITION BY b.BRAND
                            ORDER BY COALESCE(pd.N_CHILDREN,0) DESC,
                                     LENGTH(g.NAME_NORM), g.LEI) AS RN
  FROM brands b
  JOIN gleif g ON g.TOK1 = b.BRAND
  LEFT JOIN parent_deg pd ON pd.LEI = g.LEI
),
brand_pick AS (
  SELECT BRAND, LEI, LEGAL_NAME FROM brand_target WHERE RN = 1
),
m_brand AS (
  SELECT e.EPA_REGISTRY_ID, bp.LEI, bp.LEGAL_NAME
  FROM epa_unmatched e
  JOIN brand_pick bp ON bp.BRAND = e.TOK1
),
-- ultimate parent + CIK for the new matches, same rails as v1
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
edgar AS (
  SELECT {NORM.format(c='TITLE')} AS NAME_NORM, MIN(CIK_STR) AS CIK
  FROM {L}.FED_SEC_EDGAR_COMPANY_TICKERS
  GROUP BY 1 HAVING COUNT(DISTINCT CIK_STR) = 1
)
SELECT
  p.EPA_REGISTRY_ID, p.FACILITY_NAME,
  COALESCE(p.MATCHED_LEI, mb.LEI)              AS MATCHED_LEI,
  COALESCE(p.MATCHED_LEGAL_NAME, mb.LEGAL_NAME) AS MATCHED_LEGAL_NAME,
  COALESCE(p.MATCH_METHOD, IFF(mb.LEI IS NOT NULL, 'brand', NULL)) AS MATCH_METHOD,
  COALESCE(p.MATCH_CONFIDENCE, IFF(mb.LEI IS NOT NULL, 0.75, NULL)) AS MATCH_CONFIDENCE,
  COALESCE(p.ULTIMATE_PARENT_LEI, pn.PARENT_LEI) AS ULTIMATE_PARENT_LEI,
  COALESCE(p.PARENT_LEGAL_NAME, pn.PARENT_LEGAL_NAME, mb.LEGAL_NAME) AS PARENT_LEGAL_NAME,
  COALESCE(p.PARENT_CIK, ed.CIK)               AS PARENT_CIK,
  p.PARENT_UEI,
  COALESCE(p.REVIEW_FLAG, FALSE) OR (p.MATCHED_LEI IS NULL AND mb.LEI IS NOT NULL) AS REVIEW_FLAG,
  CURRENT_TIMESTAMP()::TIMESTAMP_NTZ AS _INGESTED_AT,
  IFF(p.MATCHED_LEI IS NULL AND mb.LEI IS NOT NULL, 'xc-build-v2-brand', p._SOURCE_RUN_ID) AS _SOURCE_RUN_ID
FROM prev p
LEFT JOIN m_brand mb    ON mb.EPA_REGISTRY_ID = p.EPA_REGISTRY_ID
LEFT JOIN parent_name pn ON pn.CHILD_LEI = mb.LEI
LEFT JOIN edgar ed       ON ed.NAME_NORM = COALESCE(pn.PARENT_NAME_NORM,
                                                    {NORM.format(c='mb.LEGAL_NAME')})
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args()
    if not args.run:
        print(SQL)
        return
    conn = connect()
    cur = conn.cursor()
    try:
        # preview the brand dictionary first, then build
        cur.execute(SQL)
        cur.execute(f"""SELECT COUNT(*), COUNT(MATCHED_LEI), COUNT(ULTIMATE_PARENT_LEI),
                        COUNT(PARENT_CIK) FROM {L}.XC_EPA_CORPORATE_CROSSWALK""")
        t, lei, up, cik = cur.fetchone()
        print(f"facilities={t:,} lei_matched={lei:,} ({lei/t:.1%}) ult_parent={up:,} cik={cik:,}")
        cur.execute(f"SELECT MATCH_METHOD, COUNT(*) FROM {L}.XC_EPA_CORPORATE_CROSSWALK "
                    f"WHERE MATCH_METHOD IS NOT NULL GROUP BY 1")
        for r in cur.fetchall():
            print(" ", r)
        cur.execute(f"""SELECT MATCHED_LEGAL_NAME, COUNT(*) FROM {L}.XC_EPA_CORPORATE_CROSSWALK
                        WHERE MATCH_METHOD = 'brand' GROUP BY 1 ORDER BY 2 DESC LIMIT 25""")
        print("top brand matches:")
        for r in cur.fetchall():
            print("  ", r[0], r[1])
    finally:
        conn.close()


if __name__ == "__main__":
    main()
