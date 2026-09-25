"""Skeptic batch for g00 MDS/Reliant lead. Read-only: 2 ALTER SESSION + SELECT/WITH only, one connection."""
import csv, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
from connect import db

MDS = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY"
NH = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME"
DEF = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES"
PEN = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES"

Q = [
 ("K1_star_mo", f"SELECT * FROM {NH} WHERE STATE = 'MO'"),
 ("K2_def_mo", f"""SELECT CMS_CERTIFICATION_NUMBER_CCN ccn, SURVEY_DATE, SURVEY_TYPE, COMPLAINT_DEFICIENCY, STANDARD_DEFICIENCY,
   COUNT(*) n_all,
   COUNT_IF(TRY_TO_NUMBER(REGEXP_SUBSTR(DEFICIENCY_TAG_NUMBER,'[0-9]+')) IN (600,602,607,609,610)) n_abuse,
   COUNT_IF(TRY_TO_NUMBER(REGEXP_SUBSTR(DEFICIENCY_TAG_NUMBER,'[0-9]+')) IN (600,602,607,609,610) AND SCOPE_SEVERITY_CODE IN ('G','H','I','J','K','L')) n_abuse_hj,
   COUNT_IF(SCOPE_SEVERITY_CODE IN ('G','H','I','J','K','L')) n_harm,
   COUNT_IF(SCOPE_SEVERITY_CODE IN ('J','K','L')) n_jkl,
   LISTAGG(DISTINCT IFF(TRY_TO_NUMBER(REGEXP_SUBSTR(DEFICIENCY_TAG_NUMBER,'[0-9]+')) IN (600,602,607,609,610), DEFICIENCY_TAG_NUMBER, NULL), ',') abuse_raw
   FROM {DEF} WHERE STATE = 'MO' GROUP BY 1,2,3,4,5"""),
 ("K3_pen_mo", f"SELECT p.* FROM {PEN} p WHERE p.CMS_CERTIFICATION_NUMBER_CCN IN (SELECT CMS_CERTIFICATION_NUMBER_CCN FROM {NH} WHERE STATE = 'MO')"),
 ("K4_mds_mo", f"""SELECT CCN, TO_VARCHAR(REPORT_DATE) report_date, LEFT(MDS_ITEM_QUESTION_DESCRIPTION, 70) q, MDS_ITEM_RESPONSE r, OVERALL_PERCENT,
     TOTAL_RESIDENTS, LONG_STAY_PERCENT, SHORT_STAY_PERCENT, LONG_STAY_RESIDENTS, SHORT_STAY_RESIDENTS
   FROM {MDS} WHERE STATE = 'MO' AND MDS_ITEM_QUESTION_DESCRIPTION LIKE ANY ('I6000:%','A1500%','I5950:%','I5900:%','N0415A1%','I4800:%')
   UNION ALL
   SELECT CCN, NULL, 'MAXN', NULL, NULL, TO_VARCHAR(MAX(TRY_TO_NUMBER(TOTAL_RESIDENTS))), NULL, NULL, NULL, NULL
   FROM {MDS} WHERE STATE = 'MO' GROUP BY CCN"""),
 ("K5_mds_dups", f"""WITH k AS (SELECT MDS_ITEM_QUESTION_DESCRIPTION q, CCN, MDS_ITEM_RESPONSE r, COUNT(*) n,
     COUNT(DISTINCT OVERALL_PERCENT) np, COUNT(DISTINCT TOTAL_RESIDENTS) nt, COUNT(DISTINCT REPORT_DATE) nd
   FROM {MDS} GROUP BY 1,2,3)
   SELECT LEFT(q, 60) q, SUM(n) rows_, SUM(n-1) dup_rows, COUNT_IF(n>1) dup_keys, COUNT_IF(np>1) pct_conflicts,
     COUNT_IF(nt>1) tot_conflicts, MAX(nd) max_dates
   FROM k GROUP BY q HAVING SUM(n-1) > 0 OR q LIKE 'I6000:%' ORDER BY dup_rows DESC LIMIT 30"""),
]

def main():
    c = db.connect()
    cur = c.cursor()
    cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
    cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-skeptic-2026-09-24'")
    for label, sql in Q:
        first = sql.lstrip().split(None, 1)[0].upper()
        assert first in ("SELECT", "WITH"), label
        try:
            cur.execute(sql)
            cols = [d[0] for d in cur.description]
            rows = cur.fetchall()
            with open(HERE / f"{label}.csv", "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f); w.writerow(cols); w.writerows(rows)
            print(label, len(rows), "rows", "qid", cur.sfqid)
        except Exception as e:
            print(label, "FAILED", repr(e)[:400])
    c.close()

if __name__ == "__main__":
    main()
