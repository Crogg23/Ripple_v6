"""Skeptic runner: read-only. Each statement must start with SELECT or WITH and hold no semicolon. Usage: python sk.py <batch>"""
import sys, json, datetime, decimal
from pathlib import Path
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
from connect import db

M = "LIBRARY_MARTS.HEALTH."
PB = M + "HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER"
PBS = M + "HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVI"
NP_ = M + "HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_NON_PHYSICIANS"
PH_ = M + "HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS"
H = "'1760952360'"

B1 = [
("s1_prov", f"""WITH agg AS (SELECT COUNT(*) n_rows, COUNT(DISTINCT RNDRNG_NPI) n_npi,
   COUNT_IF(RNDRNG_PRVDR_TYPE='Nurse Practitioner') n_np_rows,
   COUNT(DISTINCT IFF(RNDRNG_PRVDR_TYPE='Nurse Practitioner', RNDRNG_NPI, NULL)) n_np_npi,
   MEDIAN(IFF(RNDRNG_PRVDR_TYPE='Nurse Practitioner', TOT_MDCR_PYMT_AMT, NULL)) med_np,
   COUNT_IF(RNDRNG_PRVDR_TYPE='Nurse Practitioner' AND TOT_MDCR_PYMT_AMT > 8519635.91) np_above_her,
   COUNT_IF(RNDRNG_PRVDR_TYPE='Nurse Practitioner' AND RNDRNG_PRVDR_STATE_ABRVTN='NV' AND TOT_MDCR_PYMT_AMT > 8519635.91) nv_np_above_her
 FROM {PB})
SELECT p.*, agg.* FROM {PB} p CROSS JOIN agg WHERE p.RNDRNG_NPI = {H}"""),
("s2_svc", f"""SELECT * FROM {PBS} WHERE RNDRNG_NPI = {H} ORDER BY EST_MDCR_PYMT_AMT DESC"""),
("s3_pendrank", f"""WITH p AS (SELECT NPI npi, 'NONPHYS' src FROM {NP_} UNION ALL SELECT NPI, 'PHYS' FROM {PH_}),
 pb AS (SELECT TRIM(RNDRNG_NPI) npi, COUNT(*) n, SUM(TOT_MDCR_PYMT_AMT) pay FROM {PB} GROUP BY 1),
 j AS (SELECT p.src, p.npi, pb.pay, pb.n FROM p JOIN pb ON pb.npi = TRIM(p.npi))
SELECT src, npi, pay, n, RANK() OVER (ORDER BY pay DESC) rk,
  (SELECT COUNT(DISTINCT npi) FROM j) n_billed_npi, (SELECT COUNT(*) FROM j) n_billed_rows,
  (SELECT COUNT_IF(NOT REGEXP_LIKE(npi, '[0-9]{{10}}')) FROM p) bad_fmt, (SELECT COUNT(*) FROM p) n_p,
  (SELECT COUNT(*) - COUNT(DISTINCT npi) FROM p WHERE src='NONPHYS') dup_nonphys
FROM j QUALIFY rk <= 5 ORDER BY rk"""),
("s4_lists", f"""SELECT 'PECOS' src, NPI, FIRST_NAME fn, LAST_NAME ln, STATE_CD st, PROVIDER_TYPE_DESC||' '||ENRLMT_ID info FROM {M}HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT WHERE NPI={H} OR LAST_NAME ILIKE 'HUNTL%'
UNION ALL SELECT 'ORF', NPI, FIRST_NAME, LAST_NAME, NULL, PARTB||DME||HHA FROM {M}HEALTH__FED_CMS_ORDER_AND_REFERRING WHERE NPI={H} OR LAST_NAME ILIKE 'HUNTL%'
UNION ALL SELECT 'LEIE', NPI, FIRST_NAME, LAST_NAME, STATE, SPECIALTY||' '||EXCLUSION_TYPE||' '||TO_VARCHAR(EXCLUSION_DATE) FROM {M}HEALTH__FED_HHS_OIG_LEIE WHERE NPI={H} OR LAST_NAME ILIKE 'HUNTL%'
UNION ALL SELECT 'OPTOUT', NPI, FIRST_NAME, LAST_NAME, STATE_CODE, SPECIALTY FROM {M}HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS WHERE NPI={H} OR LAST_NAME ILIKE 'HUNTL%'
UNION ALL SELECT 'PEND_PHYS', NPI, FIRST_NAME, LAST_NAME, NULL, NULL FROM {PH_} WHERE NPI={H} OR LAST_NAME ILIKE 'HUNTL%'
UNION ALL SELECT 'PEND_NONPHYS', NPI, FIRST_NAME, LAST_NAME, NULL, NULL FROM {NP_} WHERE NPI={H} OR LAST_NAME ILIKE 'HUNTL%'
UNION ALL SELECT 'NPPES_NAME', NPI, PROVIDER_FIRST_NAME, PROVIDER_LAST_NAME_LEGAL_NAME, PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME,
   HEALTHCARE_PROVIDER_TAXONOMY_CODE_1||' '||COALESCE(HEALTHCARE_PROVIDER_TAXONOMY_CODE_2,'')||' '||COALESCE(PROVIDER_CREDENTIAL_TEXT,'')||' '||COALESCE(PROVIDER_FIRST_LINE_BUSINESS_PRACTICE_LOCATION_ADDRESS,'')
   FROM {M}HEALTH__FED_CMS_NPPES WHERE NPI={H} OR (PROVIDER_LAST_NAME_LEGAL_NAME='HUNTLY' AND PROVIDER_FIRST_NAME='MARY')"""),
("s5_q4205", f"""WITH q AS (SELECT RNDRNG_NPI npi, HCPCS_CD cd, RNDRNG_PRVDR_TYPE typ, RNDRNG_PRVDR_STATE_ABRVTN st,
   TRY_TO_DOUBLE(TO_VARCHAR(TOT_BENES)) b, TRY_TO_DOUBLE(TO_VARCHAR(TOT_SRVCS)) s, TRY_TO_DOUBLE(TO_VARCHAR(TOT_BENE_DAY_SRVCS)) bd,
   EST_MDCR_PYMT_AMT pay, AVG_MDCR_PYMT_AMT avgp FROM {PBS}
   WHERE HCPCS_CD LIKE 'Q41%' OR HCPCS_CD LIKE 'Q42%' OR HCPCS_CD LIKE 'Q43%' OR HCPCS_CD LIKE 'A20%')
SELECT IFF(cd='Q4205','Q4205','OTHER_SKIN') grp, COUNT(*) n_lines, COUNT(DISTINCT npi) n_npi, SUM(pay) tot_pay, MEDIAN(pay) med_line_pay, MAX(pay) max_line_pay,
  MEDIAN(s/NULLIF(b,0)) med_units_per_bene, MEDIAN(s/NULLIF(bd,0)) med_units_per_day, MEDIAN(bd/NULLIF(b,0)) med_days_per_bene,
  MEDIAN(avgp) med_pay_per_unit, MEDIAN(pay/NULLIF(b,0)) med_pay_per_bene,
  COUNT_IF(pay > 5912560) lines_above_her, COUNT_IF(s/NULLIF(b,0) > 5678/31) lines_more_units_per_bene,
  COUNT_IF(typ='Nurse Practitioner') np_lines, MEDIAN(IFF(typ='Nurse Practitioner', pay, NULL)) med_np_line_pay,
  COUNT_IF(st='NV') nv_lines, SUM(IFF(st='NV', pay, 0)) nv_pay
FROM q GROUP BY ROLLUP(IFF(cd='Q4205','Q4205','OTHER_SKIN'))"""),
("s6_tables", """SELECT 'MARTS' db, table_schema, table_name, row_count, created FROM LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES
  WHERE table_name ILIKE ANY ('%REVOK%','%REVALID%','%REASSIGN%','%PRECLUS%','%DEACTIV%','%OTHER_PRACTITIONERS%','%PENDING_INITIAL%','%TERMINAT%','%SKIN%')
UNION ALL SELECT 'RAW', table_schema, table_name, row_count, created FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES
  WHERE table_name ILIKE ANY ('%REVOK%','%REVALID%','%REASSIGN%','%PRECLUS%','%DEACTIV%','%OTHER_PRACTITIONERS%','%PENDING_INITIAL%','%TERMINAT%','%SKIN%')
ORDER BY 1,2,3"""),
("s7_deact", """SELECT * FROM LIBRARY_RAW.LANDING.FED_CMS_NPPES_DEACTIVATED WHERE TO_VARCHAR(OBJECT_CONSTRUCT(*)) ILIKE '%1760952360%' LIMIT 5"""),
("s8_q4205rank", f"""WITH q AS (SELECT RNDRNG_NPI npi, RNDRNG_PRVDR_TYPE typ, RNDRNG_PRVDR_STATE_ABRVTN st, EST_MDCR_PYMT_AMT pay,
   TRY_TO_DOUBLE(TO_VARCHAR(TOT_BENES)) b, TRY_TO_DOUBLE(TO_VARCHAR(TOT_SRVCS)) s, TRY_TO_DOUBLE(TO_VARCHAR(TOT_BENE_DAY_SRVCS)) bd FROM {PBS} WHERE HCPCS_CD='Q4205')
SELECT npi, typ, st, pay, b, s, bd, s/NULLIF(b,0) upb, RANK() OVER (ORDER BY pay DESC) rk_pay, RANK() OVER (ORDER BY s/NULLIF(b,0) DESC) rk_upb, COUNT(*) OVER () n
FROM q QUALIFY rk_pay <= 6 OR npi = {H} ORDER BY rk_pay"""),
]
BATCHES = {"b1": B1}

def conv(v):
    if isinstance(v, (datetime.date, datetime.datetime)): return v.isoformat()
    if isinstance(v, decimal.Decimal): return float(v)
    return v

def main():
    extra = HERE / "extra.py"
    if extra.exists():
        ns = dict(globals()); exec(extra.read_text(encoding="utf-8"), ns); BATCHES.update(ns.get("EXTRA", {}))
    qs = BATCHES[sys.argv[1]]
    for lab, s in qs:
        assert s.strip().split(None, 1)[0].upper() in ("SELECT", "WITH"), lab
        assert ";" not in s, lab
    c = db.connect(); cur = c.cursor()
    cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
    cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-skeptic-2026-09-24'")
    for lab, s in qs:
        try:
            cur.execute(s)
            cols = [d[0] for d in cur.description]
            rows = [[conv(v) for v in r] for r in cur.fetchall()]
            (HERE / f"{lab}.json").write_text(json.dumps({"cols": cols, "rows": rows}, default=str), encoding="utf-8")
            print(f"== {lab}: {len(rows)} rows"); print(cols)
            for r in rows[:40]: print(r)
        except Exception as e:
            print(f"== {lab}: ERROR {e}")
    c.close()

main()
