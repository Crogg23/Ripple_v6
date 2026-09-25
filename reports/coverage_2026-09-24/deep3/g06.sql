-- deep3/g06: deep pass 3 hand-queries, 2026-09-24
-- Tables: HEALTH__FED_CMS_MEDICARE_DIABETES_PREVENTION_PROGRAM, HEALTH__FED_IHS_FACILITIES, HEALTH__FED_CMS_MAIN,
--         HEALTH__FED_VA_SUICIDE_APPENDIX, HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_NON_PHYSICIANS
-- Door: Python (connect/db.py). Every connection first ran:
--   ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
--   ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';
-- Read-only: SELECT / WITH only. Runner: g06/run.py (refuses anything else). Results saved as g06/<label>.json.

-- [q01_mdpp] statement 1
-- MDPP: whole table (1,037 rows), analysed locally
SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DIABETES_PREVENTION_PROGRAM
;

-- [q02_ihs] statement 2
-- IHS facilities: whole table (1,006 rows), analysed locally
SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_IHS_FACILITIES
;

-- [q03_cmsmain] statement 3
-- CMS dataset catalog: whole table (158 rows), lookup check
SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MAIN
;

-- [q04_vaapp] statement 4
-- VA suicide appendix: whole table (144 raw spreadsheet rows)
SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_VA_SUICIDE_APPENDIX
;

-- [q05_pending] statement 5
-- Pending initial enrollment, non-physicians: whole table (6,880 rows)
SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_NON_PHYSICIANS
;

-- [q06_vanat] statement 6
-- VA suicide national (typed sibling, 690 rows): duplicate check and non-veteran peer
SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_VA_SUICIDE_NATIONAL
;

-- [q07_landing] statement 7
-- When each source landed: landing table created / last altered / row count
SELECT table_name, row_count, created, last_altered FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES
     WHERE table_schema='LANDING' AND (table_name ILIKE '%PENDING_INITIAL%' OR table_name ILIKE '%DIABETES_PREVENTION%'
       OR table_name ILIKE '%IHS%' OR table_name = 'FED_CMS_MAIN' OR table_name ILIKE '%VA_SUICIDE%') ORDER BY 1
;

-- [q08_nppes] statement 8
-- NPPES record for every MDPP supplier NPI and every pending NPI (both pending lists): enumeration date, deactivation, taxonomy, practice state
WITH n AS (SELECT NPI, 'MDPP' src FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DIABETES_PREVENTION_PROGRAM
               UNION SELECT NPI, 'NONPHYS' FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_NON_PHYSICIANS
               UNION SELECT NPI, 'PHYS' FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS)
  SELECT n.src, n.NPI, x.NPI AS nppes_npi, x.ENTITY_TYPE_CODE, x.PROVIDER_ENUMERATION_DATE, x.LAST_UPDATE_DATE,
         x.NPI_DEACTIVATION_DATE, x.NPI_REACTIVATION_DATE, x.NPI_DEACTIVATION_REASON_CODE,
         x.HEALTHCARE_PROVIDER_TAXONOMY_CODE_1 AS tax1, x.PROVIDER_CREDENTIAL_TEXT AS cred,
         x.PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME AS st,
         LEFT(x.PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_POSTAL_CODE, 5) AS zip5,
         x.PROVIDER_ORGANIZATION_NAME_LEGAL_BUSINESS_NAME AS org, x.PROVIDER_LAST_NAME_LEGAL_NAME AS ln, x.PROVIDER_FIRST_NAME AS fn
  FROM n LEFT JOIN LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES x ON x.NPI = n.NPI
;

-- [q09_pendflags] statement 9
-- Pending NPIs (both lists) against approved enrollment (PECOS), order/refer eligibility, OIG exclusions (LEIE), opt-out, Part B 2024 billing, Part D 2024 prescribing. Each side aggregated to NPI first
WITH p AS (SELECT NPI, 'NONPHYS' src FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_NON_PHYSICIANS
           UNION ALL SELECT NPI, 'PHYS' FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS),
  pec AS (SELECT NPI, COUNT(*) n_enr, LISTAGG(DISTINCT STATE_CD, ',') pec_st, LISTAGG(DISTINCT PROVIDER_TYPE_DESC, ' | ') pec_types
          FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT WHERE NPI IN (SELECT NPI FROM p) GROUP BY 1),
  orf AS (SELECT NPI, COUNT(*) n_orf, MAX(PARTB) orf_partb, MAX(DME) orf_dme, MAX(HHA) orf_hha, MAX(HOSPICE) orf_hospice
          FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_ORDER_AND_REFERRING WHERE NPI IN (SELECT NPI FROM p) GROUP BY 1),
  leie AS (SELECT NPI, MIN(EXCLUSION_DATE) excl_date, LISTAGG(DISTINCT EXCLUSION_TYPE, ',') excl_type, MAX(REINSTATEMENT_DATE) reinst,
                  MAX(SPECIALTY) excl_spec, MAX(STATE) excl_st, MAX(LAST_NAME) excl_ln
           FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE WHERE NPI IN (SELECT NPI FROM p) GROUP BY 1),
  opt AS (SELECT NPI, MIN(OPTOUT_EFFECTIVE_DATE) opt_eff, MAX(OPTOUT_END_DATE) opt_end
          FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS WHERE NPI IN (SELECT NPI FROM p) GROUP BY 1),
  pb AS (SELECT RNDRNG_NPI NPI, MAX(RNDRNG_PRVDR_TYPE) pb_type, MAX(RNDRNG_PRVDR_STATE_ABRVTN) pb_st,
                SUM(TRY_TO_DOUBLE(TO_VARCHAR(TOT_BENES))) pb_benes, SUM(TOT_MDCR_PYMT_AMT) pb_pay
         FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER WHERE RNDRNG_NPI IN (SELECT NPI FROM p) GROUP BY 1),
  pd AS (SELECT NPI, MAX(PRSCRBR_TYPE) pd_type, MAX(PRSCRBR_STATE_ABRVTN) pd_st,
                SUM(TRY_TO_DOUBLE(TO_VARCHAR(TOT_CLMS))) pd_clms, SUM(TRY_TO_DOUBLE(TO_VARCHAR(TOT_DRUG_CST))) pd_cost
         FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS WHERE NPI IN (SELECT NPI FROM p) GROUP BY 1)
  SELECT p.src, p.NPI, pec.n_enr, pec.pec_st, pec.pec_types, orf.n_orf, orf.orf_partb, orf.orf_dme, orf.orf_hha, orf.orf_hospice,
         leie.excl_date, leie.excl_type, leie.reinst, leie.excl_spec, leie.excl_st, leie.excl_ln, opt.opt_eff, opt.opt_end,
         pb.pb_type, pb.pb_st, pb.pb_benes, pb.pb_pay, pd.pd_type, pd.pd_st, pd.pd_clms, pd.pd_cost
  FROM p LEFT JOIN pec ON pec.NPI=p.NPI LEFT JOIN orf ON orf.NPI=p.NPI LEFT JOIN leie ON leie.NPI=p.NPI
         LEFT JOIN opt ON opt.NPI=p.NPI LEFT JOIN pb ON pb.NPI=p.NPI LEFT JOIN pd ON pd.NPI=p.NPI
;

-- [q10_mdpp_svc] statement 10
-- Every Part B 2024 service row on codes G9870-G9891 (the MDPP code block), any NPI: patients, sessions, estimated payment
SELECT RNDRNG_NPI, MAX(RNDRNG_PRVDR_LAST_ORG_NAME) nm, MAX(RNDRNG_PRVDR_TYPE) typ, MAX(RNDRNG_PRVDR_STATE_ABRVTN) st, HCPCS_CD,
         MAX(HCPCS_DESC) descr, SUM(TRY_TO_DOUBLE(TO_VARCHAR(TOT_BENES))) benes, SUM(TRY_TO_DOUBLE(TO_VARCHAR(TOT_SRVCS))) srvcs,
         SUM(EST_MDCR_PYMT_AMT) est_pay, AVG(AVG_MDCR_PYMT_AMT) avg_pay
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVI
  WHERE HCPCS_CD BETWEEN 'G9870' AND 'G9891' GROUP BY RNDRNG_NPI, HCPCS_CD
;

-- [q11_mdpp_prov] statement 11
-- Part B 2024 provider totals for every MDPP-type provider or listed MDPP supplier NPI
SELECT RNDRNG_NPI, RNDRNG_PRVDR_LAST_ORG_NAME nm, RNDRNG_PRVDR_TYPE typ, RNDRNG_PRVDR_STATE_ABRVTN st, RNDRNG_PRVDR_ENT_CD ent,
         TOT_HCPCS_CDS, TOT_BENES, TOT_SRVCS, TOT_MDCR_PYMT_AMT,
         IFF(RNDRNG_NPI IN (SELECT NPI FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DIABETES_PREVENTION_PROGRAM), 1, 0) in_list
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER
  WHERE RNDRNG_PRVDR_TYPE ILIKE '%diabet%' OR RNDRNG_NPI IN (SELECT NPI FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DIABETES_PREVENTION_PROGRAM)
;

-- [q12_hospgen] statement 12
-- CMS Care Compare hospital list, whole table (5,432 rows), to match IHS/tribal hospitals by state+city+ZIP locally
SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_GENERAL
;

-- [q13_hospenr] statement 13
-- Medicare hospital enrollments (9,175 rows), key columns, to test whether each IHS/tribal hospital bills Medicare
SELECT ENROLLMENT_ID, ENROLLMENT_STATE, PROVIDER_TYPE_TEXT, NPI, CCN, ORGANIZATION_NAME, DOING_BUSINESS_AS_NAME,
         ORGANIZATION_TYPE_STRUCTURE, ORGANIZATION_OTHER_TYPE_TEXT, PROPRIETARY_NONPROFIT, ADDRESS_LINE_1, CITY, STATE, ZIP_CODE
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS
;

-- [q14_ihsscb] statement 14
-- IHS standard code book facility list (8,733 rows): second snapshot of the same facility codes, for status and bed changes
SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_IHS_SCB_FACILITY
;

-- [q15_huntly] statement 15
-- Pending-list NP 1760952360: her Part B 2024 provider row (drug vs medical split, address) plus every surviving service line
SELECT 'PROV' lvl, RNDRNG_PRVDR_LAST_ORG_NAME nm, RNDRNG_PRVDR_CRDNTLS cred, RNDRNG_PRVDR_CITY city, RNDRNG_PRVDR_ZIP5 zip,
         NULL hcpcs, NULL descr, NULL pos, TOT_BENES benes, TOT_SRVCS srvcs, TOT_MDCR_PYMT_AMT pay, DRUG_MDCR_PYMT_AMT drug_pay,
         MED_MDCR_PYMT_AMT med_pay, BENE_AVG_AGE avg_age
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER WHERE RNDRNG_NPI='1760952360'
  UNION ALL
  SELECT 'SVC', RNDRNG_PRVDR_LAST_ORG_NAME, NULL, NULL, NULL, HCPCS_CD, HCPCS_DESC, PLACE_OF_SRVC, TOT_BENES, TOT_SRVCS,
         EST_MDCR_PYMT_AMT, AVG_MDCR_PYMT_AMT, NULL, NULL
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVI WHERE RNDRNG_NPI='1760952360'
;

-- [q16_nppeer] statement 16
-- Peer group: every nurse practitioner in Part B 2024. National and Nevada medians, count over $1M/$5M, and the top 60 plus 1760952360 with current enrollment (PECOS), order/refer, pending-list and OIG-exclusion flags
WITH np AS (SELECT RNDRNG_NPI npi, RNDRNG_PRVDR_LAST_ORG_NAME nm, RNDRNG_PRVDR_STATE_ABRVTN st, TRY_TO_DOUBLE(TOT_BENES) benes,
                     TOT_MDCR_PYMT_AMT pay, DRUG_MDCR_PYMT_AMT drug_pay
              FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER WHERE RNDRNG_PRVDR_TYPE='Nurse Practitioner'),
  stats AS (SELECT COUNT(*) n_np, MEDIAN(pay) med_pay, PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY pay) p99_pay,
                   COUNT_IF(pay > 1e6) n_over_1m, COUNT_IF(pay > 5e6) n_over_5m, MEDIAN(pay / NULLIF(benes,0)) med_per_bene FROM np),
  nv AS (SELECT COUNT(*) n_nv, MEDIAN(pay) med_nv, COUNT_IF(pay > 1e6) nv_over_1m FROM np WHERE st='NV'),
  top AS (SELECT np.*, RANK() OVER (ORDER BY pay DESC) rk, RANK() OVER (PARTITION BY st ORDER BY pay DESC) rk_state FROM np
          QUALIFY rk <= 60 OR npi='1760952360'),
  pec AS (SELECT DISTINCT NPI FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT WHERE NPI IN (SELECT npi FROM top)),
  orf AS (SELECT DISTINCT NPI FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_ORDER_AND_REFERRING WHERE NPI IN (SELECT npi FROM top)),
  pen AS (SELECT NPI FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_NON_PHYSICIANS
          UNION SELECT NPI FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS),
  lei AS (SELECT NPI, MIN(EXCLUSION_DATE) excl_date FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE WHERE NPI IN (SELECT npi FROM top) GROUP BY 1)
  SELECT top.*, stats.*, nv.*, IFF(pec.NPI IS NULL, 0, 1) in_pecos, IFF(orf.NPI IS NULL, 0, 1) in_orf,
         IFF(top.npi IN (SELECT NPI FROM pen), 1, 0) pending, lei.excl_date
  FROM top CROSS JOIN stats CROSS JOIN nv LEFT JOIN pec ON pec.NPI=top.npi LEFT JOIN orf ON orf.NPI=top.npi LEFT JOIN lei ON lei.NPI=top.npi
  ORDER BY top.rk
;

-- [q17_skinsub] statement 17
-- Top 60 NPs plus 1760952360: share of surviving service-line payment on skin-substitute codes (Q41xx-Q43xx, A20xx) vs all lines
SELECT RNDRNG_NPI, SUM(EST_MDCR_PYMT_AMT) svc_pay,
         SUM(IFF(HCPCS_CD LIKE 'Q41%' OR HCPCS_CD LIKE 'Q42%' OR HCPCS_CD LIKE 'Q43%' OR HCPCS_CD LIKE 'A20%', EST_MDCR_PYMT_AMT, 0)) skin_pay,
         MAX(IFF(HCPCS_CD LIKE 'Q41%' OR HCPCS_CD LIKE 'Q42%' OR HCPCS_CD LIKE 'Q43%' OR HCPCS_CD LIKE 'A20%', HCPCS_DESC, NULL)) a_skin_desc,
         LISTAGG(DISTINCT PLACE_OF_SRVC, ',') pos
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVI WHERE RNDRNG_NPI IN (SELECT RNDRNG_NPI npi FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER WHERE RNDRNG_PRVDR_TYPE='Nurse Practitioner'
            QUALIFY RANK() OVER (ORDER BY TOT_MDCR_PYMT_AMT DESC) <= 60) OR RNDRNG_NPI='1760952360' GROUP BY 1
;
-- [q17_skinsub] ERROR: 002031 (42601): SQL compilation error:
Unsupported subquery type cannot be evaluated at line 5, position 126

-- [q18_skinsub] statement 18
-- Redo of q17 with a CTE: top 60 NPs plus 1760952360, share of surviving service-line payment on skin-substitute codes (Q41-Q43, A20)
WITH top AS (SELECT RNDRNG_NPI npi FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER WHERE RNDRNG_PRVDR_TYPE='Nurse Practitioner'
                  QUALIFY RANK() OVER (ORDER BY TOT_MDCR_PYMT_AMT DESC) <= 60
                  UNION SELECT '1760952360')
  SELECT s.RNDRNG_NPI, SUM(s.EST_MDCR_PYMT_AMT) svc_pay,
         SUM(IFF(s.HCPCS_CD LIKE 'Q41%' OR s.HCPCS_CD LIKE 'Q42%' OR s.HCPCS_CD LIKE 'Q43%' OR s.HCPCS_CD LIKE 'A20%', s.EST_MDCR_PYMT_AMT, 0)) skin_pay,
         MAX(IFF(s.HCPCS_CD LIKE 'Q41%' OR s.HCPCS_CD LIKE 'Q42%' OR s.HCPCS_CD LIKE 'Q43%' OR s.HCPCS_CD LIKE 'A20%', s.HCPCS_CD, NULL)) a_skin_code
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVI s JOIN top ON top.npi = s.RNDRNG_NPI GROUP BY 1
;

-- [q19_npbase] statement 19
-- Base rate: every NP in Part B 2024 by payment band, how many are missing from the current PECOS enrollment file, and how many sit on either pending list
WITH np AS (SELECT RNDRNG_NPI npi, TOT_MDCR_PYMT_AMT pay FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER WHERE RNDRNG_PRVDR_TYPE='Nurse Practitioner'),
  pec AS (SELECT DISTINCT NPI FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT),
  pen AS (SELECT NPI FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_NON_PHYSICIANS
          UNION SELECT NPI FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS)
  SELECT CASE WHEN np.pay > 5e6 THEN 'a 5M+' WHEN np.pay > 1e6 THEN 'b 1M-5M' WHEN np.pay > 1e5 THEN 'c 100K-1M' ELSE 'd under 100K' END band,
         COUNT(*) n, COUNT_IF(pec.NPI IS NULL) not_in_pecos, COUNT_IF(pen.NPI IS NOT NULL) on_pending,
         COUNT_IF(pec.NPI IS NULL AND pen.NPI IS NOT NULL) gone_and_pending
  FROM np LEFT JOIN pec ON pec.NPI = np.npi LEFT JOIN pen ON pen.NPI = np.npi GROUP BY 1 ORDER BY 1
;

-- [q20_loaddates] statement 20
-- When the join partners landed: landing table created dates for PECOS, order/refer, NPPES, LEIE, opt-out, Part B
SELECT table_name, row_count, created, last_altered FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES
     WHERE table_schema='LANDING' AND (table_name ILIKE '%PECOS%' OR table_name ILIKE '%ORDER_AND_REFERRING%' OR table_name ILIKE '%NPPES%'
       OR table_name ILIKE '%LEIE%' OR table_name ILIKE '%OPT_OUT%' OR table_name ILIKE '%PHYSICIAN_OTHER_PRACTITIONERS%') ORDER BY 1
;

-- [q21_posbeds] statement 21
-- Bed counts for every Care Compare hospital from the Provider of Services file, joined on CCN, to size-match the IHS hospital peer group
SELECT p.CCN, p.PRVDR_CTGRY_CD, p.PRVDR_CTGRY_SBTYP_CD, p.STATE_CD, p.BED_CNT, p.CRTFD_BED_CNT, p.GNRL_CNTL_TYPE_CD
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER p WHERE p.CCN IN (SELECT CCN FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_GENERAL)
;

-- Totals: 21 SELECT/WITH statements (q01-q21; q17 failed to compile and was redone as q18) + 2 ALTER SESSION per connection x 5 connections = 31 of the 35 budget.
-- Everything else in g06.md was computed locally in Python from the saved results in g06/*.json.
