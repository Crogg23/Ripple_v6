"""Skeptic pass on g34 Yuma lead. Read-only SELECT/WITH. Usage: python sk.py <label> [<label>...]"""
import csv, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4]))
from connect import db

VE = "LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT"
AS_ = "LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PN_VIOLATION_ASSOC"
PWS = "LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS"

Q = {
"tables": """SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE, ROW_COUNT FROM LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES
 WHERE TABLE_NAME ILIKE '%SDWA%' ORDER BY 1,2""",
"yuma_viols": f"""SELECT VIOLATION_ID, ANY_VALUE(VIOLATION_CODE) vc, ANY_VALUE(CONTAMINANT_CODE) cc, ANY_VALUE(VIOLATION_CATEGORY_CODE) cat,
 ANY_VALUE(IS_HEALTH_BASED_IND) hb, ANY_VALUE(PUBLIC_NOTIFICATION_TIER) tier, ANY_VALUE(CALCULATED_PUB_NOTIF_TIER) ctier,
 MIN(COMPL_PER_BEGIN_DATE) b, MAX(COMPL_PER_END_DATE) e, MIN(NON_COMPL_PER_BEGIN_DATE) nb, MAX(NON_COMPL_PER_END_DATE) ne,
 COUNT(DISTINCT VIOL_MEASURE) n_meas, LISTAGG(DISTINCT VIOL_MEASURE, '/') meas, ANY_VALUE(RULE_CODE) rule, ANY_VALUE(VIOL_ORIGINATOR_CODE) orig,
 ANY_VALUE(SAMPLE_RESULT_ID) sample, MIN(VIOL_FIRST_REPORTED_DATE) vfr, MAX(VIOL_LAST_REPORTED_DATE) vlr, ANY_VALUE(VIOLATION_STATUS) status,
 ANY_VALUE(IS_MAJOR_VIOL_IND) major, ANY_VALUE(FACILITY_ID) fac, COUNT(*) nrows, COUNT(DISTINCT SUBMISSIONYEARQUARTER) nsub,
 LISTAGG(DISTINCT ENFORCEMENT_ACTION_TYPE_CODE || ':' || COALESCE(ENF_ACTION_CATEGORY,'') || '@' || COALESCE(ENFORCEMENT_DATE::string,'') || '/fr' || COALESCE(ENF_FIRST_REPORTED_DATE::string,''), ' ') enf
 FROM {VE} WHERE PWSID = 'AZ0414024'
 GROUP BY 1 HAVING MIN(COMPL_PER_BEGIN_DATE) >= '2017-01-01' OR ANY_VALUE(CONTAMINANT_CODE) IN ('1008','1009') OR ANY_VALUE(VIOLATION_CODE) IN ('11','13','75')
 ORDER BY b, VIOLATION_ID""",
"nat_clo2": f"""WITH v AS (
 SELECT PWSID, VIOLATION_ID, ANY_VALUE(VIOLATION_CODE) vc, ANY_VALUE(CONTAMINANT_CODE) cc, ANY_VALUE(PUBLIC_NOTIFICATION_TIER) tier,
        ANY_VALUE(IS_HEALTH_BASED_IND) hb, MIN(COMPL_PER_BEGIN_DATE) b, MIN(VIOL_FIRST_REPORTED_DATE) fr, COUNT(DISTINCT VIOL_MEASURE) nm,
        COUNT(DISTINCT VIOLATION_CODE) nvc
 FROM {VE} WHERE VIOLATION_ID IS NOT NULL AND (VIOLATION_CODE = '13' OR CONTAMINANT_CODE = '1008') GROUP BY 1,2),
a AS (SELECT DISTINCT PWSID, RELATED_VIOLATION_ID FROM {AS_})
SELECT v.PWSID, v.vc, v.cc, v.tier, v.hb, COUNT(*) n, COUNT_IF(v.b >= '2015-01-01') n15, COUNT_IF(a.PWSID IS NOT NULL) n_pn,
       MIN(v.b) b0, MAX(v.b) b1, MEDIAN(DATEDIFF('day', v.b, v.fr)) med_lag_days, MAX(v.nm) max_meas_variants, MAX(v.nvc) max_codes,
       MIN(v.fr) fr0, MAX(v.fr) fr1
FROM v LEFT JOIN a ON a.PWSID = v.PWSID AND a.RELATED_VIOLATION_ID = v.VIOLATION_ID
GROUP BY 1,2,3,4,5 ORDER BY n DESC""",
"yuma_assoc": f"""SELECT * FROM {AS_} WHERE PWSID = 'AZ0414024' ORDER BY COMPL_PER_BEGIN_DATE, PN_VIOLATION_ID""",
"yuma_pws": f"""SELECT PWSID, PWS_NAME, SUBMISSIONYEARQUARTER, PWS_ACTIVITY_CODE, PWS_TYPE_CODE, GW_SW_CODE, PRIMARY_SOURCE_CODE,
 POPULATION_SERVED_COUNT, SERVICE_CONNECTIONS_COUNT, IS_WHOLESALER_IND, OWNER_TYPE_CODE, CITY_NAME, FIRST_REPORTED_DATE, LAST_REPORTED_DATE
 FROM {PWS} WHERE PWSID = 'AZ0414024' OR (STATE_CODE = 'AZ' AND PWS_NAME ILIKE '%YUMA%' AND POPULATION_SERVED_COUNT > 1000)""",
"ve_shape": f"""SELECT SUBMISSIONYEARQUARTER, COUNT(*) n, COUNT(DISTINCT PWSID || '|' || VIOLATION_ID) viols, COUNT_IF(VIOLATION_ID IS NULL) null_id,
 COUNT(DISTINCT LEFT(PWSID,2)) prefixes, COUNT(DISTINCT PWSID) systems, MIN(COMPL_PER_BEGIN_DATE) b0, MAX(COMPL_PER_BEGIN_DATE) b1,
 MAX(VIOL_FIRST_REPORTED_DATE) fr1,
 COUNT_IF(VIOLATION_CODE = '13') c13_rows, COUNT_IF(VIOLATION_CODE = '13' AND VIOLATION_ID IS NULL) c13_nullid,
 COUNT(DISTINCT IFF(VIOLATION_CODE = '13', PWSID || '|' || VIOLATION_ID, NULL)) c13_viols,
 COUNT(DISTINCT IFF(VIOLATION_CODE = '13' AND COMPL_PER_BEGIN_DATE >= '2015-01-01', PWSID || '|' || VIOLATION_ID, NULL)) c13_since2015,
 COUNT(DISTINCT IFF(VIOLATION_CODE = '13' AND COMPL_PER_BEGIN_DATE >= '2015-01-01', PWSID, NULL)) c13_sys_since2015
 FROM {VE} GROUP BY 1 ORDER BY 1""",
"yuma_fac": """SELECT * FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_FACILITIES WHERE PWSID = 'AZ0414024'""",
"yuma_visits": """SELECT * FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_SITE_VISITS WHERE PWSID = 'AZ0414024'""",
"az_pn_month": f"""WITH v AS (
 SELECT PWSID, VIOLATION_ID, ANY_VALUE(VIOLATION_CODE) vc, ANY_VALUE(PUBLIC_NOTIFICATION_TIER) tier, MIN(COMPL_PER_BEGIN_DATE) b, MIN(VIOL_FIRST_REPORTED_DATE) fr
 FROM {VE} WHERE LEFT(PWSID,2) = 'AZ' AND VIOLATION_ID IS NOT NULL GROUP BY 1,2)
SELECT TO_CHAR(DATE_TRUNC('month', fr), 'YYYY-MM') m, COUNT(*) all_v, COUNT_IF(vc = '75') pn, COUNT(DISTINCT IFF(vc = '75', PWSID, NULL)) pn_sys,
       COUNT_IF(vc = '75' AND PWSID = 'AZ0414024') pn_yuma, COUNT_IF(tier = '1') t1, COUNT_IF(tier = '1' AND DATEDIFF('day', b, fr) > 180) t1_late180,
       COUNT_IF(vc = '75' AND DATEDIFF('day', b, fr) > 180) pn_late180
FROM v WHERE fr BETWEEN '2019-01-01' AND '2024-12-31' GROUP BY 1 ORDER BY 1""",
}

def run(labels, extra=None):
    q = dict(Q); q.update(extra or {})
    c = db.connect()
    try:
        cur = c.cursor()
        cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
        cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-skeptic-2026-09-24'")
        for lab in labels:
            sql = q.get(lab, "")
            if lab == "ref":
                import glob
                tl = list(csv.reader(open(HERE / "out_tables.csv", encoding="utf-8")))[1:]
                refs = [r for r in tl if "REF" in r[1].upper()]
                if not refs:
                    print("== ref: no SDWA ref table, skipped"); continue
                sql = f"SELECT * FROM LIBRARY_MARTS.{refs[0][0]}.{refs[0][1]} LIMIT 20000"
            assert sql.lstrip().upper().startswith(("SELECT", "WITH")) and ";" not in sql
            try:
                cur.execute(sql)
            except Exception as ex:
                print(f"== {lab}: ERROR {ex}"); continue
            cols = [d[0] for d in cur.description]
            rows = cur.fetchall()
            with open(HERE / f"out_{lab}.csv", "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f); w.writerow(cols); w.writerows(rows)
            print(f"== {lab}: {len(rows)} rows")
    finally:
        c.close()

if __name__ == "__main__":
    run(sys.argv[1:])
