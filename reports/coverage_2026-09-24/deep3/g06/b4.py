M = "LIBRARY_MARTS.HEALTH."
PB = f"{M}HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER"
PBS = f"{M}HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVI"
QUERIES = [
 ("q18_skinsub", "Redo of q17 with a CTE: top 60 NPs plus 1760952360, share of surviving service-line payment on skin-substitute codes (Q41-Q43, A20)",
  f"""WITH top AS (SELECT RNDRNG_NPI npi FROM {PB} WHERE RNDRNG_PRVDR_TYPE='Nurse Practitioner'
                  QUALIFY RANK() OVER (ORDER BY TOT_MDCR_PYMT_AMT DESC) <= 60
                  UNION SELECT '1760952360')
  SELECT s.RNDRNG_NPI, SUM(s.EST_MDCR_PYMT_AMT) svc_pay,
         SUM(IFF(s.HCPCS_CD LIKE 'Q41%' OR s.HCPCS_CD LIKE 'Q42%' OR s.HCPCS_CD LIKE 'Q43%' OR s.HCPCS_CD LIKE 'A20%', s.EST_MDCR_PYMT_AMT, 0)) skin_pay,
         MAX(IFF(s.HCPCS_CD LIKE 'Q41%' OR s.HCPCS_CD LIKE 'Q42%' OR s.HCPCS_CD LIKE 'Q43%' OR s.HCPCS_CD LIKE 'A20%', s.HCPCS_CD, NULL)) a_skin_code
  FROM {PBS} s JOIN top ON top.npi = s.RNDRNG_NPI GROUP BY 1"""),
 ("q19_npbase", "Base rate: every NP in Part B 2024 by payment band, how many are missing from the current PECOS enrollment file, and how many sit on either pending list",
  f"""WITH np AS (SELECT RNDRNG_NPI npi, TOT_MDCR_PYMT_AMT pay FROM {PB} WHERE RNDRNG_PRVDR_TYPE='Nurse Practitioner'),
  pec AS (SELECT DISTINCT NPI FROM {M}HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT),
  pen AS (SELECT NPI FROM {M}HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_NON_PHYSICIANS
          UNION SELECT NPI FROM {M}HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS)
  SELECT CASE WHEN np.pay > 5e6 THEN 'a 5M+' WHEN np.pay > 1e6 THEN 'b 1M-5M' WHEN np.pay > 1e5 THEN 'c 100K-1M' ELSE 'd under 100K' END band,
         COUNT(*) n, COUNT_IF(pec.NPI IS NULL) not_in_pecos, COUNT_IF(pen.NPI IS NOT NULL) on_pending,
         COUNT_IF(pec.NPI IS NULL AND pen.NPI IS NOT NULL) gone_and_pending
  FROM np LEFT JOIN pec ON pec.NPI = np.npi LEFT JOIN pen ON pen.NPI = np.npi GROUP BY 1 ORDER BY 1"""),
 ("q20_loaddates", "When the join partners landed: landing table created dates for PECOS, order/refer, NPPES, LEIE, opt-out, Part B",
  """SELECT table_name, row_count, created, last_altered FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES
     WHERE table_schema='LANDING' AND (table_name ILIKE '%PECOS%' OR table_name ILIKE '%ORDER_AND_REFERRING%' OR table_name ILIKE '%NPPES%'
       OR table_name ILIKE '%LEIE%' OR table_name ILIKE '%OPT_OUT%' OR table_name ILIKE '%PHYSICIAN_OTHER_PRACTITIONERS%') ORDER BY 1"""),
]
