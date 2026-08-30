"""Level-3 name check for the agency-split old-HMDA lender id (2026-08-30).

The historic loan file carries no lender name, so names come from the CFPB legacy-id -> LEI
crosswalk (ARID_2017 = agency code + respondent id, with RESPONDENT_NAME). Same ids, same split.
60 random matched pairs per edge; same normalizer as scripts/pass2_precision_check_2026_08_29.py.
Output: reports/recon/pass2/hmda_split_precision_2026-08-30.json
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import _snowflake_conn as sf
from pass2_precision_check_2026_08_29 import name_match
OUT = os.path.join(os.path.dirname(HERE), "reports", "recon", "pass2", "hmda_split_precision_2026-08-30.json")
DB = "LIBRARY_RAW.LANDING"
EDGES = [
  ("Old-HMDA id, bank-regulator rows (agency 1-3) -> FDIC cert",
   f"""WITH l AS (SELECT NULLIF(LTRIM(SUBSTR(REGEXP_REPLACE(ARID_2017,'[^0-9]',''),2),'0'),'') v, RESPONDENT_NAME nm
              FROM {DB}.FED_CFPB_HMDA_ARID2017_LEI_XREF WHERE LEFT(TRIM(ARID_2017),1) IN ('1','2','3')
              QUALIFY ROW_NUMBER() OVER (PARTITION BY v ORDER BY RANDOM())=1),
        r AS (SELECT NULLIF(LTRIM(REGEXP_REPLACE(CERT,'[^0-9]',''),'0'),'') v, NAME nm FROM {DB}.FED_FDIC_BANK_DATA
              QUALIFY ROW_NUMBER() OVER (PARTITION BY v ORDER BY RANDOM())=1)
      SELECT l.v, l.nm, r.nm FROM l JOIN r USING (v) WHERE l.v IS NOT NULL ORDER BY RANDOM() LIMIT 60"""),
  ("Old-HMDA id, HUD rows (agency 7) -> Form 5500 sponsor EIN",
   f"""WITH l AS (SELECT NULLIF(SUBSTR(REGEXP_REPLACE(ARID_2017,'[^0-9]',''),2),'') v, RESPONDENT_NAME nm
              FROM {DB}.FED_CFPB_HMDA_ARID2017_LEI_XREF WHERE LEFT(TRIM(ARID_2017),1)='7'
              QUALIFY ROW_NUMBER() OVER (PARTITION BY v ORDER BY RANDOM())=1),
        r AS (SELECT NULLIF(REGEXP_REPLACE(SPONS_DFE_EIN,'[^0-9]',''),'') v, SPONSOR_DFE_NAME nm FROM {DB}.FED_DOL_FORM5500_FULL
              QUALIFY ROW_NUMBER() OVER (PARTITION BY v ORDER BY RANDOM())=1)
      SELECT l.v, l.nm, r.nm FROM l JOIN r USING (v) WHERE l.v IS NOT NULL ORDER BY RANDOM() LIMIT 60"""),
]
cur = sf.connect().cursor(); cur.execute("ALTER SESSION SET QUERY_TAG='hmda_split_precision_2026_08_30'")
out = []
for label, sql in EDGES:
    cur.execute(sql); rows = cur.fetchall()
    nm = [name_match(r[1], r[2]) for r in rows]; scored = [x for x in nm if x is not None]
    miss = [(r[0], str(r[1])[:40], str(r[2])[:40]) for r, m in zip(rows, nm) if m is False]
    res = dict(label=label, pairs=len(rows), name_scored=len(scored),
               name_match_pct=round(100*sum(scored)/len(scored),1) if scored else None, mismatches=miss[:8])
    out.append(res); print(label, "| names", res["name_match_pct"], "% of", len(scored), "| e.g.", miss[:3])
json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, default=str)
