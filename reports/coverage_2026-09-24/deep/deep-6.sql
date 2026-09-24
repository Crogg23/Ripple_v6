-- deep-6: coverage deep pass, 2026-09-24
-- Tables: HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS, HEALTH__FED_CMS_PART_D_PRESCRIBERS,
--         HEALTH__FED_FDA_DEVICE_ENFORCEMENT, HEALTH__FED_FDA_MAUDE, HEALTH__FED_HRSA_PROVIDER_RELIEF_FUND
-- Door: Python (connect/db.py). Every connection opens with
--   ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300
--   ALTER SESSION SET QUERY_TAG = 'coverage-b-2026-09-24'
-- Read-only: SELECT / WITH only. Statements below in run order; labels are -- @name.

-- @q01_optout_count_sample
SELECT (SELECT COUNT(*) FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS) AS n_total, t.*
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS t LIMIT 5;

-- @q02_partd_count_sample
SELECT (SELECT COUNT(*) FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS) AS n_total, t.*
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS t LIMIT 5;

-- @q03_enf_count_sample
SELECT (SELECT COUNT(*) FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DEVICE_ENFORCEMENT) AS n_total, t.* EXCLUDE (OPENFDA)
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DEVICE_ENFORCEMENT t LIMIT 5;

-- @q04_maude_count_sample
SELECT (SELECT COUNT(*) FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_MAUDE) AS n_total, t.* EXCLUDE (DEVICE_OPENFDA)
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_MAUDE t LIMIT 5;

-- @q05_prf_count_sample
SELECT (SELECT COUNT(*) FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_PROVIDER_RELIEF_FUND) AS n_total, t.*
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_PROVIDER_RELIEF_FUND t LIMIT 5;

-- @q06_optout_specialty_by_start_year
SELECT COALESCE(SPECIALTY,'(ALL)') AS specialty, COUNT(*) n, COUNT(DISTINCT NPI) npis,
  COUNT_IF(YEAR(OPTOUT_EFFECTIVE_DATE) < 2016) pre2016,
  COUNT_IF(YEAR(OPTOUT_EFFECTIVE_DATE) BETWEEN 2016 AND 2019) y16_19,
  COUNT_IF(YEAR(OPTOUT_EFFECTIVE_DATE) = 2020) y20, COUNT_IF(YEAR(OPTOUT_EFFECTIVE_DATE) = 2021) y21,
  COUNT_IF(YEAR(OPTOUT_EFFECTIVE_DATE) = 2022) y22, COUNT_IF(YEAR(OPTOUT_EFFECTIVE_DATE) = 2023) y23,
  COUNT_IF(YEAR(OPTOUT_EFFECTIVE_DATE) = 2024) y24, COUNT_IF(YEAR(OPTOUT_EFFECTIVE_DATE) = 2025) y25,
  COUNT_IF(YEAR(OPTOUT_EFFECTIVE_DATE) = 2026) y26,
  COUNT_IF(OPTOUT_END_DATE < '2026-09-24') end_passed, MIN(OPTOUT_END_DATE) min_end, MAX(OPTOUT_END_DATE) max_end,
  MAX(LAST_UPDATED) max_upd
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS
GROUP BY ROLLUP(SPECIALTY) ORDER BY n DESC LIMIT 25;

-- @q07_optout_mh_by_month
SELECT DATE_TRUNC('month', OPTOUT_EFFECTIVE_DATE) m,
  COUNT_IF(SPECIALTY ILIKE '%counselor%') mhc, COUNT_IF(SPECIALTY ILIKE '%marriage%') mft,
  COUNT_IF(SPECIALTY ILIKE '%psycholog%') psych, COUNT_IF(SPECIALTY ILIKE '%social work%') csw,
  COUNT_IF(SPECIALTY ILIKE '%psychiatr%') psychiatry, COUNT(*) all_specs
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS
WHERE OPTOUT_EFFECTIVE_DATE >= '2022-07-01'
GROUP BY 1 ORDER BY 1;

-- @q08_optout_vs_pecos_by_state
WITH oo AS (
  SELECT DISTINCT NPI, UPPER(TRIM(STATE_CODE)) st,
    CASE WHEN SPECIALTY ILIKE '%counselor%' OR SPECIALTY ILIKE '%marriage%' THEN 'NEW'
         WHEN SPECIALTY ILIKE '%psycholog%' OR SPECIALTY ILIKE '%social work%' THEN 'OLD' END grp,
    IFF(OPTOUT_EFFECTIVE_DATE >= '2024-01-01', 1, 0) since24
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS
),
pe AS (
  SELECT DISTINCT NPI, UPPER(TRIM(STATE_CD)) st,
    CASE WHEN PROVIDER_TYPE_DESC ILIKE '%counselor%' OR PROVIDER_TYPE_DESC ILIKE '%marriage%' THEN 'NEW'
         WHEN PROVIDER_TYPE_DESC ILIKE '%psycholog%' OR PROVIDER_TYPE_DESC ILIKE '%social work%' THEN 'OLD' END grp,
    PROVIDER_TYPE_DESC
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT
),
types AS (SELECT LISTAGG(DISTINCT PROVIDER_TYPE_DESC, ' ; ') t FROM pe WHERE grp IS NOT NULL),
ov AS (SELECT COUNT(DISTINCT oo.NPI) both_lists FROM oo JOIN pe ON oo.NPI = pe.NPI AND oo.grp = pe.grp WHERE oo.grp IS NOT NULL),
a AS (SELECT st, grp, COUNT(DISTINCT NPI) oo_all, COUNT(DISTINCT IFF(since24 = 1, NPI, NULL)) oo_24 FROM oo WHERE grp IS NOT NULL GROUP BY 1, 2),
b AS (SELECT st, grp, COUNT(DISTINCT NPI) enr FROM pe WHERE grp IS NOT NULL GROUP BY 1, 2),
j AS (SELECT COALESCE(a.st, b.st) st, COALESCE(a.grp, b.grp) grp, NVL(oo_all, 0) oo_all, NVL(oo_24, 0) oo_24, NVL(enr, 0) enr
      FROM a FULL JOIN b ON a.st = b.st AND a.grp = b.grp),
w AS (SELECT st,
        SUM(IFF(grp = 'NEW', oo_all, 0)) new_oo, SUM(IFF(grp = 'NEW', oo_24, 0)) new_oo24, SUM(IFF(grp = 'NEW', enr, 0)) new_enr,
        SUM(IFF(grp = 'OLD', oo_all, 0)) old_oo, SUM(IFF(grp = 'OLD', enr, 0)) old_enr
      FROM j GROUP BY ROLLUP(st))
SELECT COALESCE(st, '(US)') st, new_oo, new_oo24, new_enr,
  ROUND(new_oo / NULLIF(new_oo + new_enr, 0), 3) new_optout_share,
  old_oo, old_enr, ROUND(old_oo / NULLIF(old_oo + old_enr, 0), 3) old_optout_share,
  ROUND((new_oo / NULLIF(new_oo + new_enr, 0)) / NULLIF(old_oo / NULLIF(old_oo + old_enr, 0), 0), 2) new_vs_old,
  (SELECT both_lists FROM ov) both_lists, (SELECT t FROM types) pecos_types
FROM w ORDER BY new_oo DESC NULLS LAST LIMIT 60;

-- @q09_partd_column_checks
SELECT COUNT(*) n, COUNT(DISTINCT NPI) npis, MIN(DATA_YEAR) y0, MAX(DATA_YEAR) y1,
  COUNT_IF(TRY_TO_NUMBER(OPIOID_TOT_CLMS::VARCHAR) >= 500) op500,
  COUNT_IF(TRY_TO_NUMBER(OPIOID_LA_TOT_CLMS::VARCHAR) > 0) la_any, COUNT_IF(TRY_TO_NUMBER(OPIOID_LA_TOT_CLMS::VARCHAR) >= 500) la500,
  COUNT_IF(TRY_TO_NUMBER(ANTPSYCT_GE65_TOT_CLMS::VARCHAR) > 0) ap_any, COUNT_IF(TRY_TO_NUMBER(ANTPSYCT_GE65_TOT_CLMS::VARCHAR) >= 500) ap500,
  COUNT_IF(NULLIF(OPIOID_LA_TOT_CLMS, '') IS NOT NULL AND TRY_TO_NUMBER(OPIOID_LA_TOT_CLMS::VARCHAR) IS NULL) la_nonnum,
  COUNT_IF(NULLIF(ANTPSYCT_GE65_TOT_CLMS, '') IS NOT NULL AND TRY_TO_NUMBER(ANTPSYCT_GE65_TOT_CLMS::VARCHAR) IS NULL) ap_nonnum,
  COUNT_IF(NULLIF(ANTPSYCT_GE65_TOT_CLMS, '') IS NULL) ap_blank,
  COUNT_IF(NULLIF(OPIOID_LA_TOT_CLMS, '') IS NULL) la_blank,
  ARRAY_AGG(DISTINCT ANTPSYCT_GE65_SPRSN_FLAG) ap_flags, ARRAY_AGG(DISTINCT GE65_SPRSN_FLAG) ge65_flags,
  COUNT_IF(GE65_SPRSN_FLAG = '#') ge65_hash, COUNT_IF(GE65_SPRSN_FLAG = '*') ge65_star,
  SUM(TRY_TO_NUMBER(OPIOID_LA_TOT_CLMS::VARCHAR)) la_sum, SUM(TRY_TO_NUMBER(ANTPSYCT_GE65_TOT_CLMS::VARCHAR)) ap_sum,
  SUM(TRY_TO_NUMBER(OPIOID_TOT_CLMS::VARCHAR)) op_sum
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS;

-- @q10_partd_la_opioid_vs_specialty
WITH b AS (
  SELECT NPI, PRSCRBR_LAST_ORG_NAME ln, PRSCRBR_FIRST_NAME fn, PRSCRBR_CRDNTLS cr, PRSCRBR_CITY city,
    PRSCRBR_STATE_ABRVTN st, PRSCRBR_TYPE spec,
    TRY_TO_NUMBER(TOT_CLMS::VARCHAR) tot, TRY_TO_NUMBER(OPIOID_TOT_CLMS::VARCHAR) op, TRY_TO_NUMBER(OPIOID_LA_TOT_CLMS::VARCHAR) la,
    TRY_TO_NUMBER(OPIOID_TOT_BENES::VARCHAR) opb, TRY_TO_NUMBER(OPIOID_LA_TOT_BENES::VARCHAR) lab,
    TRY_TO_NUMBER(OPIOID_LA_TOT_DRUG_CST::VARCHAR, 14, 2) la_cost, ROUND(BENE_AVG_AGE, 1) age
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS
),
s AS (
  SELECT spec, COUNT(*) n_spec, COUNT_IF(la > 0) n_la, MEDIAN(IFF(la > 0, la, NULL)) med_la,
    APPROX_PERCENTILE(IFF(la > 0, la, NULL), 0.99) p99_la
  FROM b GROUP BY spec
)
SELECT b.NPI, b.fn, b.ln, b.cr, b.city, b.st, b.spec, b.tot, b.op, b.la, b.opb, b.lab, b.la_cost, b.age,
  s.n_spec, s.n_la, s.med_la, ROUND(s.p99_la) p99_la, ROUND(b.la / NULLIF(s.p99_la, 0), 1) x_p99,
  RANK() OVER (PARTITION BY b.spec ORDER BY b.la DESC) rk_in_spec,
  RANK() OVER (ORDER BY b.la DESC) rk_us
FROM b JOIN s ON b.spec = s.spec
WHERE b.la >= 200
QUALIFY rk_us <= 15 OR (s.n_la >= 100 AND b.la / NULLIF(s.p99_la, 0) >= 3)
ORDER BY x_p99 DESC LIMIT 60;

-- @q11_partd_antipsychotic65_vs_specialty
WITH b AS (
  SELECT NPI, PRSCRBR_LAST_ORG_NAME ln, PRSCRBR_FIRST_NAME fn, PRSCRBR_CRDNTLS cr, PRSCRBR_CITY city,
    PRSCRBR_STATE_ABRVTN st, PRSCRBR_TYPE spec,
    TRY_TO_NUMBER(GE65_TOT_CLMS::VARCHAR) g65, TRY_TO_NUMBER(ANTPSYCT_GE65_TOT_CLMS::VARCHAR) ap,
    TRY_TO_NUMBER(ANTPSYCT_GE65_TOT_BENES::VARCHAR) apb, TRY_TO_NUMBER(TOT_BENES::VARCHAR) benes,
    TRY_TO_NUMBER(BENE_AGE_GT_84_CNT::VARCHAR) over84, ROUND(BENE_AVG_AGE, 1) age
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS
),
s AS (
  SELECT spec, COUNT(*) n_spec, COUNT_IF(ap > 0) n_ap, MEDIAN(IFF(ap > 0, ap, NULL)) med_ap,
    APPROX_PERCENTILE(IFF(ap > 0, ap, NULL), 0.99) p99_ap, SUM(ap) spec_ap
  FROM b GROUP BY spec
),
top1000 AS (
  SELECT spec, COUNT(*) n_top FROM (SELECT spec FROM b ORDER BY ap DESC NULLS LAST LIMIT 1000) GROUP BY spec
)
SELECT b.NPI, b.fn, b.ln, b.cr, b.city, b.st, b.spec, b.g65, b.ap, ROUND(b.ap / NULLIF(b.g65, 0), 3) ap_share65,
  b.apb, b.benes, b.over84, b.age, s.n_spec, s.n_ap, s.med_ap, ROUND(s.p99_ap) p99_ap,
  ROUND(b.ap / NULLIF(s.p99_ap, 0), 1) x_p99, NVL(t.n_top, 0) spec_in_top1000,
  RANK() OVER (ORDER BY b.ap DESC) rk_us
FROM b JOIN s ON b.spec = s.spec LEFT JOIN top1000 t ON t.spec = b.spec
WHERE b.ap >= 300
QUALIFY rk_us <= 15 OR (s.n_ap >= 100 AND b.ap / NULLIF(s.p99_ap, 0) >= 3)
ORDER BY x_p99 DESC LIMIT 60;

-- @q12_enf_status_class
SELECT STATUS, CLASSIFICATION, COUNT(*) product_rows, COUNT(DISTINCT EVENT_ID) events, COUNT(DISTINCT RECALLING_FIRM) firms,
  MIN(RECALL_INITIATION_DATE) init_min, MAX(RECALL_INITIATION_DATE) init_max,
  COUNT_IF(RECALL_INITIATION_DATE < '2020-01-01') init_pre2020, COUNT_IF(RECALL_INITIATION_DATE >= '2024-01-01') init_2024p,
  MEDIAN(DATEDIFF(day, RECALL_INITIATION_DATE, TERMINATION_DATE)) med_days_to_term,
  COUNT_IF(TERMINATION_DATE IS NOT NULL) has_term, MAX(REPORT_DATE) max_report, MAX(TERMINATION_DATE) max_term
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DEVICE_ENFORCEMENT
GROUP BY 1, 2 ORDER BY 1, 2;

-- @q13_enf_class1_ongoing_by_firm
WITH asof AS (SELECT MAX(REPORT_DATE) d FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DEVICE_ENFORCEMENT),
e AS (
  SELECT RECALLING_FIRM firm, EVENT_ID, MIN(RECALL_INITIATION_DATE) init, COUNT(*) products,
    ANY_VALUE(LEFT(REASON_FOR_RECALL, 110)) reason
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DEVICE_ENFORCEMENT
  WHERE CLASSIFICATION = 'Class I' AND STATUS = 'Ongoing' GROUP BY 1, 2
),
closed AS (
  SELECT MEDIAN(d) med_close, APPROX_PERCENTILE(d, 0.9) p90_close FROM (
    SELECT EVENT_ID, DATEDIFF(day, MIN(RECALL_INITIATION_DATE), MAX(TERMINATION_DATE)) d
    FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DEVICE_ENFORCEMENT
    WHERE CLASSIFICATION = 'Class I' AND STATUS = 'Terminated' AND RECALL_INITIATION_DATE >= '2012-01-01' GROUP BY 1)
)
SELECT e.firm, COUNT(*) events, SUM(products) product_rows, MIN(init) oldest,
  MEDIAN(DATEDIFF(day, init, asof.d)) med_days_open, COUNT_IF(DATEDIFF(day, init, asof.d) > closed.p90_close) open_past_p90,
  ANY_VALUE(closed.med_close) class1_med_close, ANY_VALUE(closed.p90_close) class1_p90_close, ANY_VALUE(asof.d) asof,
  MIN_BY(e.reason, e.init) oldest_reason
FROM e CROSS JOIN asof CROSS JOIN closed
GROUP BY e.firm ORDER BY events DESC, product_rows DESC LIMIT 25;
-- ERROR: 001003 (42000): SQL compilation error:
syntax error line 18 at position 23 unexpected 'CROSS'.
syntax error line 18 at position 23 unexpected 'CROSS'.
syntax error line 19 at position 0 unexpected 'GR

-- @q14_maude_event_types
SELECT EVENT_TYPE, COUNT(*) rows_, COUNT(DISTINCT MDR_REPORT_KEY) reports, COUNT(DISTINCT REPORT_NUMBER) rpt_numbers,
  MIN(DATE_RECEIVED) recv_min, MAX(DATE_RECEIVED) recv_max,
  COUNT_IF(DATE_OF_EVENT < '2020-01-01') event_pre2020, COUNT_IF(DATE_OF_EVENT < '2018-01-01') event_pre2018,
  COUNT_IF(DATE_OF_EVENT IS NULL) no_event_date, COUNT(DISTINCT MANUFACTURER_D_NAME) makers
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_MAUDE GROUP BY 1 ORDER BY 2 DESC;

-- @q15_maude_deaths_maker_code_vs_peers
WITH mp AS (
  SELECT MANUFACTURER_D_NAME mfr, DEVICE_REPORT_PRODUCT_CODE pc, ANY_VALUE(LEFT(GENERIC_NAME, 50)) gen, MODE(LEFT(BRAND_NAME, 45)) brand,
    COUNT(DISTINCT MDR_REPORT_KEY) reports,
    COUNT(DISTINCT IFF(EVENT_TYPE = 'Death', MDR_REPORT_KEY, NULL)) deaths,
    COUNT(DISTINCT IFF(EVENT_TYPE = 'Injury', MDR_REPORT_KEY, NULL)) injuries,
    COUNT(DISTINCT IFF(EVENT_TYPE = 'Death' AND DATE_OF_EVENT < '2020-01-01', MDR_REPORT_KEY, NULL)) deaths_old_event
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_MAUDE GROUP BY 1, 2
),
pcs AS (SELECT pc, SUM(reports) pc_reports, SUM(deaths) pc_deaths, COUNT(*) pc_makers FROM mp GROUP BY 1)
SELECT mp.mfr, mp.pc, mp.gen, mp.brand, mp.reports, mp.deaths, mp.injuries, mp.deaths_old_event,
  ROUND(mp.deaths / NULLIF(mp.reports, 0), 4) death_rate, pcs.pc_reports, pcs.pc_deaths, pcs.pc_makers,
  ROUND(pcs.pc_deaths / NULLIF(pcs.pc_reports, 0), 4) pc_death_rate,
  ROUND(mp.deaths / NULLIF(pcs.pc_deaths, 0), 3) share_pc_deaths, ROUND(mp.reports / NULLIF(pcs.pc_reports, 0), 3) share_pc_reports
FROM mp JOIN pcs ON mp.pc = pcs.pc
ORDER BY mp.deaths DESC LIMIT 30;

-- @q16_prf_sanity
SELECT COUNT(*) n, COUNT(DISTINCT NAME_KEY || '|' || STATE) key_states, COUNT(DISTINCT NAME_KEY || '|' || STATE || '|' || CITY) key_state_city,
  COUNT_IF(PAYMENT_AMOUNT <= 0) nonpos, MIN(PAYMENT_AMOUNT) pmin, MAX(PAYMENT_AMOUNT) pmax, SUM(PAYMENT_AMOUNT) total,
  COUNT_IF(NAME_WORDS = 1) one_word, COUNT(DISTINCT STATE) states,
  COUNT_IF(PAYMENT_AMOUNT >= 1e8) over100m, SUM(IFF(PAYMENT_AMOUNT >= 1e8, PAYMENT_AMOUNT, 0)) sum_over100m,
  COUNT_IF(PAYMENT_AMOUNT < 1000) under1k,
  COUNT_IF(NAME_KEY ILIKE '%HOSPITAL%' OR NAME_KEY ILIKE '%MEDICAL CENTER%' OR NAME_KEY ILIKE '%HEALTH SYSTEM%') hosp_like,
  SUM(IFF(NAME_KEY ILIKE '%HOSPITAL%' OR NAME_KEY ILIKE '%MEDICAL CENTER%' OR NAME_KEY ILIKE '%HEALTH SYSTEM%', PAYMENT_AMOUNT, 0)) hosp_like_sum
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_PROVIDER_RELIEF_FUND;

-- @q17_optout_state_supply_billing_only
WITH oo AS (
  SELECT DISTINCT NPI, UPPER(TRIM(STATE_CODE)) st,
    CASE WHEN SPECIALTY ILIKE '%counselor%' OR SPECIALTY ILIKE '%marriage%' THEN 'NEW'
         WHEN SPECIALTY ILIKE '%psycholog%' OR SPECIALTY ILIKE '%social work%' THEN 'OLD' END grp
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS
),
pe AS (
  SELECT NPI, UPPER(TRIM(STATE_CD)) st,
    CASE WHEN PROVIDER_TYPE_DESC ILIKE '%counselor%' OR PROVIDER_TYPE_DESC ILIKE '%marriage%' THEN 'NEW'
         WHEN PROVIDER_TYPE_DESC ILIKE '%psycholog%' OR PROVIDER_TYPE_DESC ILIKE '%social work%' THEN 'OLD' END grp,
    MAX(IFF(PROVIDER_TYPE_DESC ILIKE 'PRACTITIONER%', 1, 0)) bills
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT GROUP BY 1, 2, 3
),
pb AS (
  SELECT RNDRNG_NPI NPI, UPPER(TRIM(RNDRNG_PRVDR_STATE_ABRVTN)) st,
    CASE WHEN RNDRNG_PRVDR_TYPE ILIKE '%counselor%' OR RNDRNG_PRVDR_TYPE ILIKE '%marriage%' THEN 'NEW'
         WHEN RNDRNG_PRVDR_TYPE ILIKE '%psycholog%' OR RNDRNG_PRVDR_TYPE ILIKE '%social work%' THEN 'OLD' END grp,
    TRY_TO_NUMBER(TOT_BENES::VARCHAR) benes
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER
),
a AS (SELECT st, grp, COUNT(*) oo FROM oo WHERE grp IS NOT NULL GROUP BY 1, 2),
b AS (SELECT st, grp, COUNT_IF(bills = 1) enr_bill, COUNT_IF(bills = 0) enr_ordref FROM pe WHERE grp IS NOT NULL GROUP BY 1, 2),
c AS (SELECT st, grp, COUNT(*) pb_billers, SUM(benes) pb_benes FROM pb WHERE grp IS NOT NULL GROUP BY 1, 2),
u AS (SELECT st, grp FROM a UNION SELECT st, grp FROM b UNION SELECT st, grp FROM c),
j AS (
  SELECT u.st, u.grp, NVL(a.oo, 0) oo, NVL(b.enr_bill, 0) enr_bill, NVL(b.enr_ordref, 0) enr_ordref,
    NVL(c.pb_billers, 0) pb_billers, NVL(c.pb_benes, 0) pb_benes
  FROM u LEFT JOIN a ON a.st = u.st AND a.grp = u.grp
         LEFT JOIN b ON b.st = u.st AND b.grp = u.grp
         LEFT JOIN c ON c.st = u.st AND c.grp = u.grp
),
w AS (
  SELECT st,
    SUM(IFF(grp = 'NEW', oo, 0)) new_oo, SUM(IFF(grp = 'NEW', enr_bill, 0)) new_bill, SUM(IFF(grp = 'NEW', enr_ordref, 0)) new_ordref,
    SUM(IFF(grp = 'NEW', pb_billers, 0)) new_pb, SUM(IFF(grp = 'NEW', pb_benes, 0)) new_pb_benes,
    SUM(IFF(grp = 'OLD', oo, 0)) old_oo, SUM(IFF(grp = 'OLD', enr_bill, 0)) old_bill,
    SUM(IFF(grp = 'OLD', pb_billers, 0)) old_pb, SUM(IFF(grp = 'OLD', pb_benes, 0)) old_pb_benes
  FROM j GROUP BY ROLLUP(st)
)
SELECT COALESCE(st, '(US)') st, new_oo, new_bill, new_ordref, new_pb, new_pb_benes,
  ROUND(new_oo / NULLIF(new_oo + new_bill, 0), 3) new_oo_share,
  ROUND(new_oo / NULLIF(new_pb, 0), 2) new_oo_per_biller,
  old_oo, old_bill, old_pb, ROUND(old_oo / NULLIF(old_oo + old_bill, 0), 3) old_oo_share,
  ROUND(old_oo / NULLIF(old_pb, 0), 2) old_oo_per_biller
FROM w ORDER BY new_oo DESC LIMIT 60;

-- @q18_enf_class1_ongoing_by_firm
WITH refd AS (SELECT MAX(REPORT_DATE) d FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DEVICE_ENFORCEMENT),
e AS (
  SELECT RECALLING_FIRM firm, EVENT_ID, MIN(RECALL_INITIATION_DATE) init, COUNT(*) products,
    ANY_VALUE(LEFT(REASON_FOR_RECALL, 110)) reason
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DEVICE_ENFORCEMENT
  WHERE CLASSIFICATION = 'Class I' AND STATUS = 'Ongoing' GROUP BY 1, 2
),
closed AS (
  SELECT MEDIAN(d) med_close, APPROX_PERCENTILE(d, 0.9) p90_close, COUNT(*) n_closed FROM (
    SELECT EVENT_ID, DATEDIFF(day, MIN(RECALL_INITIATION_DATE), MAX(TERMINATION_DATE)) d
    FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DEVICE_ENFORCEMENT
    WHERE CLASSIFICATION = 'Class I' AND STATUS = 'Terminated' AND RECALL_INITIATION_DATE >= '2012-01-01' GROUP BY 1)
)
SELECT e.firm, COUNT(*) events, SUM(e.products) product_rows, MIN(e.init) oldest,
  MEDIAN(DATEDIFF(day, e.init, r.d)) med_days_open,
  COUNT_IF(DATEDIFF(day, e.init, r.d) > c.p90_close) open_past_p90,
  ANY_VALUE(c.med_close) class1_med_close, ANY_VALUE(c.p90_close) class1_p90_close, ANY_VALUE(c.n_closed) n_closed,
  ANY_VALUE(r.d) ref_date,
  (SELECT COUNT(*) FROM e e2, refd r2, closed c2 WHERE DATEDIFF(day, e2.init, r2.d) > c2.p90_close) all_open_past_p90,
  MIN_BY(e.reason, e.init) oldest_reason
FROM e, refd r, closed c
GROUP BY e.firm ORDER BY events DESC, product_rows DESC LIMIT 25;

-- @q19_maude_death_outliers_check
WITH d AS (
  SELECT MANUFACTURER_D_NAME mfr, DEVICE_REPORT_PRODUCT_CODE pc, MDR_REPORT_KEY k,
    ANY_VALUE(DATE_RECEIVED) recv, ANY_VALUE(DATE_OF_EVENT) ev, MAX(PRODUCT_PROBLEM_FLAG) ppf
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_MAUDE
  WHERE EVENT_TYPE = 'Death' AND DEVICE_REPORT_PRODUCT_CODE IN ('LGW', 'FKX', 'OZO', 'ONU', 'DTK', 'DSQ', 'MVK', 'QBJ', 'NIQ')
  GROUP BY 1, 2, 3
),
t AS (
  SELECT d.*, IFF(mfr IN ('NEVRO CORP.', 'CONCORD MANUFACTURING', 'MEDTRONIC PUERTO RICO OPERATIONS CO.', 'SPECTRANETICS',
      'BARD PERIPHERAL VASCULAR, INC.', 'THORATEC CORPORATION', 'HEARTWARE, INC.', 'DEXCOM, INC.', 'ZOLL MANUFACTURING CORPORATION',
      'MEDTRONIC IRELAND', 'ABBOTT VASCULAR', 'BOSTON SCIENTIFIC CORPORATION'), mfr, '(other makers)') who
  FROM d
),
pd AS (SELECT pc, who, recv, COUNT(*) n FROM t GROUP BY 1, 2, 3),
mx AS (SELECT pc, who, MAX(n) max_one_day, MAX_BY(recv, n) busiest_day FROM pd GROUP BY 1, 2)
SELECT t.pc, t.who, COUNT(*) deaths, COUNT_IF(ppf = 'Y') device_problem_y, COUNT_IF(ppf = 'N') device_problem_n,
  COUNT_IF(ev < '2020-01-01') event_pre2020, COUNT_IF(ev IS NULL) no_event_date,
  MIN(ev) ev_min, MAX(ev) ev_max, COUNT(DISTINCT recv) recv_days,
  ANY_VALUE(mx.max_one_day) max_one_day, ANY_VALUE(mx.busiest_day) busiest_day
FROM t JOIN mx ON mx.pc = t.pc AND mx.who = t.who
GROUP BY 1, 2 ORDER BY 1, 3 DESC;

-- @q20_partd_antipsych_highvolume_peers
WITH b AS (
  SELECT NPI, PRSCRBR_FIRST_NAME fn, PRSCRBR_LAST_ORG_NAME ln, PRSCRBR_CRDNTLS cr, PRSCRBR_CITY city,
    PRSCRBR_STATE_ABRVTN st, PRSCRBR_TYPE spec,
    TRY_TO_NUMBER(GE65_TOT_CLMS::VARCHAR) g65, TRY_TO_NUMBER(ANTPSYCT_GE65_TOT_CLMS::VARCHAR) ap,
    TRY_TO_NUMBER(TOT_BENES::VARCHAR) benes, TRY_TO_NUMBER(BENE_AGE_GT_84_CNT::VARCHAR) over84, ROUND(BENE_AVG_AGE, 1) age
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS
),
hv AS (SELECT *, ap / g65 share FROM b WHERE g65 >= 30000 AND spec NOT ILIKE '%psych%' AND ap IS NOT NULL),
s AS (SELECT COUNT(*) n_hv, MEDIAN(share) med_share, APPROX_PERCENTILE(share, 0.9) p90_share,
        APPROX_PERCENTILE(share, 0.99) p99_share, SUM(ap) hv_ap FROM hv),
all_np AS (SELECT SUM(ap) ap_all, SUM(IFF(spec NOT ILIKE '%psych%', ap, 0)) ap_nonpsych FROM b)
SELECT hv.NPI, hv.fn, hv.ln, hv.cr, hv.city, hv.st, hv.spec, hv.g65, hv.ap, ROUND(hv.share, 3) share,
  hv.benes, hv.over84, hv.age, s.n_hv, ROUND(s.med_share, 4) med_share, ROUND(s.p90_share, 4) p90_share,
  ROUND(s.p99_share, 4) p99_share, ROUND(hv.share / NULLIF(s.med_share, 0), 1) x_median,
  s.hv_ap, all_np.ap_all, all_np.ap_nonpsych
FROM hv, s, all_np ORDER BY hv.share DESC LIMIT 30;

-- @q21_partd_vs_leie_all
WITH b AS (
  SELECT NPI::VARCHAR npi, PRSCRBR_FIRST_NAME fn, PRSCRBR_LAST_ORG_NAME ln, PRSCRBR_CITY city, PRSCRBR_STATE_ABRVTN st,
    PRSCRBR_TYPE spec, TRY_TO_NUMBER(TOT_CLMS::VARCHAR) tot, TRY_TO_NUMBER(TOT_DRUG_CST::VARCHAR, 16, 2) cost,
    TRY_TO_NUMBER(OPIOID_TOT_CLMS::VARCHAR) op, TRY_TO_NUMBER(OPIOID_LA_TOT_CLMS::VARCHAR) la,
    TRY_TO_NUMBER(ANTPSYCT_GE65_TOT_CLMS::VARCHAR) ap
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS
),
r AS (
  SELECT npi, RANK() OVER (ORDER BY la DESC NULLS LAST) rk_la, RANK() OVER (ORDER BY ap DESC NULLS LAST) rk_ap,
    RANK() OVER (ORDER BY op DESC NULLS LAST) rk_op FROM b
),
l AS (
  SELECT NPI::VARCHAR npi, LAST_NAME, FIRST_NAME, BUSINESS_NAME, STATE, EXCLUSION_DATE, EXCLUSION_TYPE, REINSTATEMENT_DATE, GENERAL_CATEGORY
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE WHERE NPI_IS_REAL::VARCHAR ILIKE 'true'
)
SELECT b.npi, b.fn, b.ln, b.city, b.st, b.spec, b.tot, b.cost, b.op, b.la, b.ap, r.rk_la, r.rk_ap, r.rk_op,
  l.FIRST_NAME l_fn, l.LAST_NAME l_ln, l.BUSINESS_NAME l_biz, l.STATE l_st, l.EXCLUSION_DATE, l.EXCLUSION_TYPE, l.REINSTATEMENT_DATE,
  IFF(UPPER(TRIM(b.ln)) = UPPER(TRIM(l.LAST_NAME)), 1, 0) last_agree
FROM b JOIN l ON b.npi = l.npi JOIN r ON r.npi = b.npi
ORDER BY l.EXCLUSION_DATE;

-- @q22_prf_vs_leie_sam
WITH x AS (
  SELECT 'LEIE' src, IFF(IS_ENTITY_NOT_INDIVIDUAL::VARCHAR ILIKE 'true', 'ORG', 'PERSON') kind,
    trim(regexp_replace(trim(regexp_replace(regexp_replace(upper(
      IFF(IS_ENTITY_NOT_INDIVIDUAL::VARCHAR ILIKE 'true', BUSINESS_NAME, FIRST_NAME || ' ' || LAST_NAME)), '[^A-Z0-9 ]', ' '), '\\s+', ' ')),
      '(\\s+(LLC|L L C|INC|INCORPORATED|CORP|CORPORATION|CO|LP|L P|LTD|PC|P C|LLP|OPCO|OPERATIONS|OPERATING|HOLDINGS|THE))+$', '')) k,
    UPPER(TRIM(STATE)) st, UPPER(TRIM(CITY)) city, EXCLUSION_DATE xd, REINSTATEMENT_DATE rd, EXCLUSION_TYPE xt,
    IFF(IS_ENTITY_NOT_INDIVIDUAL::VARCHAR ILIKE 'true', BUSINESS_NAME, FIRST_NAME || ' ' || LAST_NAME) xname, GENERAL_CATEGORY cat
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE
  UNION ALL
  SELECT 'SAM', IFF(IS_ENTITY_NOT_INDIVIDUAL::VARCHAR ILIKE 'true', 'ORG', 'PERSON'),
    trim(regexp_replace(trim(regexp_replace(regexp_replace(upper(
      IFF(IS_ENTITY_NOT_INDIVIDUAL::VARCHAR ILIKE 'true', ENTITY_NAME, FIRST_NAME || ' ' || LAST_NAME)), '[^A-Z0-9 ]', ' '), '\\s+', ' ')),
      '(\\s+(LLC|L L C|INC|INCORPORATED|CORP|CORPORATION|CO|LP|L P|LTD|PC|P C|LLP|OPCO|OPERATIONS|OPERATING|HOLDINGS|THE))+$', '')),
    UPPER(TRIM(STATE)), UPPER(TRIM(CITY)), ACTIVATION_DATE, TERMINATION_DATE, EXCLUSION_TYPE,
    IFF(IS_ENTITY_NOT_INDIVIDUAL::VARCHAR ILIKE 'true', ENTITY_NAME, FIRST_NAME || ' ' || LAST_NAME), EXCLUDING_AGENCY
  FROM LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS
  WHERE EXCLUDING_AGENCY <> 'HHS'
)
SELECT p.PRF_ROW_ID, p.PROVIDER_NAME, p.NAME_WORDS, p.STATE, p.CITY, p.PAYMENT_AMOUNT,
  x.src, x.kind, x.xname, x.city xcity, x.xd, x.rd, x.xt, x.cat, IFF(p.CITY = x.city, 1, 0) city_agree
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_PROVIDER_RELIEF_FUND p
JOIN x ON p.NAME_KEY = x.k AND p.STATE = x.st
WHERE x.k IS NOT NULL AND LENGTH(x.k) > 3
ORDER BY p.PAYMENT_AMOUNT DESC;

-- @q23_prf_vs_hcris_2019
WITH h AS (
  SELECT PROVIDER_CCN ccn, HOSPITAL_NAME,
    trim(regexp_replace(trim(regexp_replace(regexp_replace(upper(HOSPITAL_NAME), '[^A-Z0-9 ]', ' '), '\\s+', ' ')),
      '(\\s+(LLC|L L C|INC|INCORPORATED|CORP|CORPORATION|CO|LP|L P|LTD|PC|P C|LLP|OPCO|OPERATIONS|OPERATING|HOLDINGS|THE))+$', '')) k,
    UPPER(TRIM(STATE_CODE)) st, UPPER(TRIM(CITY)) city, NUMBER_OF_BEDS beds, TOTAL_DAYS_TITLE_XIX mcaid_days,
    TOTAL_DAYS_TITLE_XVIII mcare_days, TOTAL_DAYS_ALL all_days, NET_PATIENT_REVENUE npr, NET_INCOME ni,
    CASH_ON_HAND_AND_IN_BANKS cash, TOTAL_ASSETS assets, CCN_FACILITY_TYPE ft, TYPE_OF_CONTROL toc, FISCAL_YEAR_END_DATE fye
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS
  WHERE FISCAL_YEAR_END_DATE BETWEEN '2019-01-01' AND '2019-12-31'
  QUALIFY ROW_NUMBER() OVER (PARTITION BY PROVIDER_CCN ORDER BY FISCAL_YEAR_LENGTH_DAYS DESC, FISCAL_YEAR_END_DATE DESC) = 1
),
p AS (SELECT NAME_KEY k, STATE st, CITY city, SUM(PAYMENT_AMOUNT) paid, COUNT(*) n_lines
      FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_PROVIDER_RELIEF_FUND GROUP BY 1, 2, 3)
SELECT h.*, p.paid, p.n_lines, COUNT(*) OVER (PARTITION BY p.k, p.st, p.city) ccn_per_payee,
  (SELECT COUNT(*) FROM h) n_hcris_2019
FROM h JOIN p ON h.k = p.k AND h.st = p.st AND h.city = p.city;

-- @q24_prf_hospital_paid_vs_revenue_with_snf
WITH h AS (
  SELECT PROVIDER_CCN ccn, HOSPITAL_NAME,
    trim(regexp_replace(trim(regexp_replace(regexp_replace(upper(HOSPITAL_NAME), '[^A-Z0-9 ]', ' '), '\\s+', ' ')),
      '(\\s+(LLC|L L C|INC|INCORPORATED|CORP|CORPORATION|CO|LP|L P|LTD|PC|P C|LLP|OPCO|OPERATIONS|OPERATING|HOLDINGS|THE))+$', '')) k,
    UPPER(TRIM(STATE_CODE)) st, UPPER(TRIM(CITY)) city, NUMBER_OF_BEDS beds, NET_PATIENT_REVENUE npr,
    CCN_FACILITY_TYPE ft, TYPE_OF_CONTROL toc
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS
  WHERE FISCAL_YEAR_END_DATE BETWEEN '2019-01-01' AND '2019-12-31'
  QUALIFY ROW_NUMBER() OVER (PARTITION BY PROVIDER_CCN ORDER BY FISCAL_YEAR_LENGTH_DAYS DESC, FISCAL_YEAR_END_DATE DESC) = 1
),
p AS (SELECT NAME_KEY k, STATE st, CITY city, SUM(PAYMENT_AMOUNT) paid
      FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_PROVIDER_RELIEF_FUND GROUP BY 1, 2, 3),
m AS (SELECT h.*, p.paid, COUNT(*) OVER (PARTITION BY p.k, p.st, p.city) ccn_per_payee
      FROM h JOIN p ON h.k = p.k AND h.st = p.st AND h.city = p.city),
snf AS (
  SELECT trim(regexp_replace(trim(regexp_replace(regexp_replace(upper(ORGANIZATION_NAME), '[^A-Z0-9 ]', ' '), '\\s+', ' ')),
      '(\\s+(LLC|L L C|INC|INCORPORATED|CORP|CORPORATION|CO|LP|L P|LTD|PC|P C|LLP|OPCO|OPERATIONS|OPERATING|HOLDINGS|THE))+$', '')) k,
    UPPER(TRIM(STATE)) st, COUNT(DISTINCT CCN) n_snf, ANY_VALUE(NURSING_HOME_PROVIDER_NAME) a_home
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS GROUP BY 1, 2
)
SELECT m.ccn, m.HOSPITAL_NAME, m.city, m.st, m.ft, m.toc, m.beds, m.npr, m.paid, m.ccn_per_payee,
  NVL(snf.n_snf, 0) n_snf, snf.a_home
FROM m LEFT JOIN snf ON snf.k = m.k AND snf.st = m.st
WHERE m.npr > 1000000;

-- @q25_enf_class1_ongoing_past_p90
WITH refd AS (SELECT MAX(REPORT_DATE) d FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DEVICE_ENFORCEMENT),
closed AS (
  SELECT APPROX_PERCENTILE(d, 0.9) p90_close FROM (
    SELECT EVENT_ID, DATEDIFF(day, MIN(RECALL_INITIATION_DATE), MAX(TERMINATION_DATE)) d
    FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DEVICE_ENFORCEMENT
    WHERE CLASSIFICATION = 'Class I' AND STATUS = 'Terminated' AND RECALL_INITIATION_DATE >= '2012-01-01' GROUP BY 1)
),
e AS (
  SELECT RECALLING_FIRM firm, EVENT_ID, MIN(RECALL_INITIATION_DATE) init, MIN(CENTER_CLASSIFICATION_DATE) classified,
    COUNT(*) products, ANY_VALUE(LEFT(PRODUCT_DESCRIPTION, 70)) product, ANY_VALUE(LEFT(REASON_FOR_RECALL, 90)) reason,
    ANY_VALUE(LEFT(PRODUCT_QUANTITY, 30)) qty
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DEVICE_ENFORCEMENT
  WHERE CLASSIFICATION = 'Class I' AND STATUS = 'Ongoing' GROUP BY 1, 2
)
SELECT e.firm, e.EVENT_ID, e.init, e.classified, DATEDIFF(day, e.init, r.d) days_open, ROUND(DATEDIFF(day, e.init, r.d) / 365.25, 1) yrs_open,
  e.products, e.qty, e.product, e.reason, c.p90_close
FROM e, refd r, closed c
WHERE DATEDIFF(day, e.init, r.d) > c.p90_close
ORDER BY e.init;

-- @q26_maude_injury_makers_and_spikes
WITH mb AS (
  SELECT MANUFACTURER_D_NAME mfr, LEFT(BRAND_NAME, 40) brand, DATE_TRUNC('month', DATE_RECEIVED) m,
    COUNT(DISTINCT MDR_REPORT_KEY) n_all, COUNT(DISTINCT IFF(EVENT_TYPE = 'Injury', MDR_REPORT_KEY, NULL)) n_inj,
    COUNT(DISTINCT IFF(EVENT_TYPE = 'Death', MDR_REPORT_KEY, NULL)) n_death
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_MAUDE GROUP BY 1, 2, 3
),
agg AS (
  SELECT mfr, brand, SUM(n_all) reports, SUM(n_inj) injuries, SUM(n_death) deaths, COUNT(*) months,
    MEDIAN(n_all) med_month, MAX(n_all) max_month, MAX_BY(m, n_all) peak_month,
    MEDIAN(n_inj) med_inj_month, MAX(n_inj) max_inj_month, MAX_BY(m, n_inj) peak_inj_month
  FROM mb GROUP BY 1, 2
)
SELECT *, ROUND(max_month / NULLIF(med_month, 0), 1) spike_x, ROUND(max_inj_month / NULLIF(med_inj_month, 0), 1) inj_spike_x
FROM agg
QUALIFY RANK() OVER (ORDER BY injuries DESC) <= 15
     OR (reports >= 2000 AND RANK() OVER (ORDER BY max_inj_month / NULLIF(med_inj_month, 0) DESC NULLS LAST) <= 12)
ORDER BY injuries DESC;

-- @q27_leie_miranda_detail
SELECT l.*, (SELECT COUNT(*) FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE) leie_rows,
  (SELECT MAX(EXCLUSION_DATE) FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE) leie_max_excl
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE l
WHERE l.NPI::VARCHAR = '1285673012' OR (UPPER(l.LAST_NAME) = 'MIRANDA' AND UPPER(l.FIRST_NAME) = 'EDUARDO');

-- ============================================================
-- Notes
-- q13 failed to compile: ASOF is a reserved word in Snowflake, so a CTE
--   named asof breaks. Rerun as q18 with the CTE renamed refd.
-- Count: 27 SELECT/WITH statements (q13 counted) + 8 session-setting
--   statements (2 per connection x 4 connections) = 35.
-- q21-q24 returned row-level matches; the rollups in deep-6.md were
--   computed from those rows in Python, no extra warehouse calls.
