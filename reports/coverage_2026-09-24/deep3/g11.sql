-- deep3/g11: deep pass 3, 2026-09-24. Python door (connect/db.py), read-only SELECT/WITH only.
-- Every connection first ran: ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300; ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'.
-- 6 connections (12 session statements) + 26 query statements S01-S26 below. Budget was 35.
-- Tables: HEALTH__INTL_HEALTHCANADA_DPD_DRUG, HEALTH__FED_FDA_GUDID__STAGING, HEALTH__FED_HRSA_UDS_HEALTH_CENTER_INFO,
--         HEALTH__FED_HRSA_UDS_TABLE3A_PATIENTS, HEALTH__ST_OEHHA_PROPOSITION_65_LIST.
-- Join partners: ENVIRONMENT__FED_EPA_TRI_BASIC_2023, ENVIRONMENT__FED_EPA_ECHO, HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES, HEALTH__FED_FDA_GUDID.
-- Failed statements (still counted): S04 and S22 (alias SAMPLE is reserved), S12 and S13 (TRY_TO_NUMBER on a FLOAT column).
-- S06 ran but its line regex lost the backslash in transit ('\d' became 'd'), so every line came back NULL; S09 reruns it with [0-9].
-- The same lost backslash hit S05's director count ('\s+' became 's+'); S24 redoes director matching with [[:space:]].
-- Per-statement results: reports/coverage_2026-09-24/deep3/g11/Sxx.json

-- ===== connection 1: S01-S07 =====
-- S01 discovery: sibling tables for joins (TRI years, UDS, DPD, GUDID, HPSA)
SELECT table_schema, table_name, row_count
FROM LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES
WHERE table_name ILIKE '%EPA_TRI%' OR table_name ILIKE '%UDS%' OR table_name ILIKE '%DPD%'
   OR table_name ILIKE '%GUDID%' OR table_name ILIKE '%OEHHA%' OR table_name ILIKE '%HEALTHCANADA%' OR table_name ILIKE '%FQHC%'
ORDER BY 2;

-- S02 DPD drug: profile, duplicate check on drug_code, flag values
WITH t AS (SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__INTL_HEALTHCANADA_DPD_DRUG),
d AS (SELECT drug_code, COUNT(*) c FROM t GROUP BY 1)
SELECT (SELECT COUNT(*) FROM t) n, (SELECT COUNT(*) FROM d) codes, (SELECT MAX(c) FROM d) max_rows_per_code,
       (SELECT COUNT(DISTINCT drug_identification_number) FROM t) dins,
       (SELECT COUNT(DISTINCT brand_name) FROM t) brands, (SELECT COUNT(DISTINCT ai_group_no) FROM t) ai_groups,
       (SELECT MIN(last_update_date) FROM t) lud0, (SELECT MAX(last_update_date) FROM t) lud1,
       (SELECT COUNT_IF(last_update_date IS NULL) FROM t) lud_null,
       (SELECT SYSTEM$TYPEOF(MAX(last_update_date)) FROM t) lud_type,
       (SELECT COUNT(DISTINCT _source_run_id) FROM t) runs, (SELECT COUNT(DISTINCT _src_sha256) FROM t) files,
       (SELECT ARRAY_AGG(DISTINCT pediatric_flag) FROM t) ped_vals, (SELECT COUNT_IF(pediatric_flag='Y') FROM t) ped_y,
       (SELECT OBJECT_AGG(COALESCE(drug_class,'<null>'), c::variant) FROM (SELECT drug_class, COUNT(*) c FROM t GROUP BY 1)) classes,
       (SELECT COUNT_IF(NULLIF(TRIM(product_categorization),'') IS NULL) FROM t) cat_blank,
       (SELECT MIN(TRY_TO_NUMBER(drug_code)) FROM t) code_min, (SELECT MAX(TRY_TO_NUMBER(drug_code)) FROM t) code_max,
       (SELECT COUNT_IF(NULLIF(TRIM(accession_number),'') IS NOT NULL) FROM t) accession_filled,
       (SELECT OBJECT_AGG(COALESCE(number_of_ais::string,'<null>'), c::variant) FROM (SELECT number_of_ais, COUNT(*) c FROM t GROUP BY 1)) ais;

-- S03 DPD drug: last-update month by class (time rhythm)
SELECT DATE_TRUNC('month', last_update_date) m, COUNT(*) n,
       COUNT_IF(drug_class='Human') human, COUNT_IF(drug_class='Veterinary') vet, COUNT_IF(drug_class='Disinfectant') disinf,
       COUNT(DISTINCT last_update_date) distinct_days, MAX_BY(last_update_date, 1) any_day,
       MEDIAN(TRY_TO_NUMBER(drug_code)) median_code
FROM LIBRARY_MARTS.HEALTH.HEALTH__INTL_HEALTHCANADA_DPD_DRUG GROUP BY 1 ORDER BY 1;

-- S04 GUDID staging: what the raw blocks hold
SELECT COUNT(*) n, SYSTEM$TYPEOF(ANY_VALUE(raw)) raw_type, MIN(LEN(raw::string)) len_min, MAX(LEN(raw::string)) len_max,
       COUNT(DISTINCT raw::string) distinct_raw,
       ARRAY_AGG(DISTINCT ARRAY_TO_STRING(OBJECT_KEYS(TRY_PARSE_JSON(raw::string)),',')) keysets,
       ANY_VALUE(LEFT(raw::string, 1500)) sample
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_GUDID__STAGING;

-- S05 UDS health center info: profile, id uniqueness, funding flags, shared directors and addresses
WITH t AS (SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_UDS_HEALTH_CENTER_INFO)
SELECT COUNT(*) n, COUNT(DISTINCT bhcmisid) ids, COUNT(DISTINCT grantnumber) grants, COUNT(DISTINCT healthcenterstate) states,
       COUNT(DISTINCT UPPER(TRIM(projectdirectoremail))) emails,
       COUNT(DISTINCT UPPER(REGEXP_REPLACE(TRIM(projectdirector),'\s+',' '))) directors,
       COUNT(DISTINCT UPPER(TRIM(healthcenterstreetaddress))||'|'||LEFT(healthcenterzipcode,5)) addresses,
       ARRAY_AGG(DISTINCT fundingchc) chc_vals, COUNT_IF(fundingchc='True') chc_true,
       COUNT_IF(fundingmsaw='True') msaw_true, COUNT_IF(fundinghp='True') hp_true, COUNT_IF(fundingrph='True') rph_true,
       ARRAY_AGG(DISTINCT urbanruralflag) ur_vals, COUNT_IF(urbanruralflag='Rural') rural,
       ARRAY_AGG(DISTINCT reportingyear) years, COUNT(DISTINCT _source_run_id) runs,
       COUNT_IF(LOWER(projectdirectoremail) LIKE ANY ('%@gmail.com','%@yahoo.com','%@hotmail.com','%@aol.com','%@outlook.com')) freemail
FROM t;

-- S06 UDS Table 3A: per age line, blank marker '--' vs zero vs counts; smallest shown count (suppression test)
WITH t AS (SELECT bhcmisid, T3A_L1_CA, T3A_L1_CB, T3A_L2_CA, T3A_L2_CB, T3A_L3_CA, T3A_L3_CB, T3A_L4_CA, T3A_L4_CB, T3A_L5_CA, T3A_L5_CB, T3A_L6_CA, T3A_L6_CB, T3A_L7_CA, T3A_L7_CB, T3A_L8_CA, T3A_L8_CB, T3A_L9_CA, T3A_L9_CB, T3A_L10_CA, T3A_L10_CB, T3A_L11_CA, T3A_L11_CB, T3A_L12_CA, T3A_L12_CB, T3A_L13_CA, T3A_L13_CB, T3A_L14_CA, T3A_L14_CB, T3A_L15_CA, T3A_L15_CB, T3A_L16_CA, T3A_L16_CB, T3A_L17_CA, T3A_L17_CB, T3A_L18_CA, T3A_L18_CB, T3A_L19_CA, T3A_L19_CB, T3A_L20_CA, T3A_L20_CB, T3A_L21_CA, T3A_L21_CB, T3A_L22_CA, T3A_L22_CB, T3A_L23_CA, T3A_L23_CB, T3A_L24_CA, T3A_L24_CB, T3A_L25_CA, T3A_L25_CB, T3A_L26_CA, T3A_L26_CB, T3A_L27_CA, T3A_L27_CB, T3A_L28_CA, T3A_L28_CB, T3A_L29_CA, T3A_L29_CB, T3A_L30_CA, T3A_L30_CB, T3A_L31_CA, T3A_L31_CB, T3A_L32_CA, T3A_L32_CB, T3A_L33_CA, T3A_L33_CB, T3A_L34_CA, T3A_L34_CB, T3A_L35_CA, T3A_L35_CB, T3A_L36_CA, T3A_L36_CB, T3A_L37_CA, T3A_L37_CB, T3A_L38_CA, T3A_L38_CB, T3A_L39_CA, T3A_L39_CB FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_UDS_TABLE3A_PATIENTS),
long AS (SELECT bhcmisid, col, val FROM t UNPIVOT(val FOR col IN (T3A_L1_CA, T3A_L1_CB, T3A_L2_CA, T3A_L2_CB, T3A_L3_CA, T3A_L3_CB, T3A_L4_CA, T3A_L4_CB, T3A_L5_CA, T3A_L5_CB, T3A_L6_CA, T3A_L6_CB, T3A_L7_CA, T3A_L7_CB, T3A_L8_CA, T3A_L8_CB, T3A_L9_CA, T3A_L9_CB, T3A_L10_CA, T3A_L10_CB, T3A_L11_CA, T3A_L11_CB, T3A_L12_CA, T3A_L12_CB, T3A_L13_CA, T3A_L13_CB, T3A_L14_CA, T3A_L14_CB, T3A_L15_CA, T3A_L15_CB, T3A_L16_CA, T3A_L16_CB, T3A_L17_CA, T3A_L17_CB, T3A_L18_CA, T3A_L18_CB, T3A_L19_CA, T3A_L19_CB, T3A_L20_CA, T3A_L20_CB, T3A_L21_CA, T3A_L21_CB, T3A_L22_CA, T3A_L22_CB, T3A_L23_CA, T3A_L23_CB, T3A_L24_CA, T3A_L24_CB, T3A_L25_CA, T3A_L25_CB, T3A_L26_CA, T3A_L26_CB, T3A_L27_CA, T3A_L27_CB, T3A_L28_CA, T3A_L28_CB, T3A_L29_CA, T3A_L29_CB, T3A_L30_CA, T3A_L30_CB, T3A_L31_CA, T3A_L31_CB, T3A_L32_CA, T3A_L32_CB, T3A_L33_CA, T3A_L33_CB, T3A_L34_CA, T3A_L34_CB, T3A_L35_CA, T3A_L35_CB, T3A_L36_CA, T3A_L36_CB, T3A_L37_CA, T3A_L37_CB, T3A_L38_CA, T3A_L38_CB, T3A_L39_CA, T3A_L39_CB))),
p AS (SELECT bhcmisid, TO_NUMBER(REGEXP_SUBSTR(col,'L(\d+)_',1,1,'e',1)) line, RIGHT(col,1) sex, val,
             TRY_TO_NUMBER(REPLACE(val,',','')) num FROM long)
SELECT line,
       COUNT_IF(sex='A' AND val='--') m_dash, COUNT_IF(sex='B' AND val='--') f_dash,
       COUNT_IF(num=0) zero_cells, COUNT_IF(num IS NULL AND val<>'--') other_text,
       MIN(IFF(num>0,num,NULL)) min_pos, SUM(IFF(sex='A',num,0)) male_sum, SUM(IFF(sex='B',num,0)) female_sum,
       COUNT(*) cells
FROM p GROUP BY line ORDER BY line;

-- S07 Prop 65: profile, dates, keys, blanks, extra columns
WITH t AS (SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__ST_OEHHA_PROPOSITION_65_LIST)
SELECT COUNT(*) n, COUNT(DISTINCT chemical) chems, COUNT(DISTINCT chemical_key) keys, COUNT(DISTINCT cas_no) cas,
       COUNT_IF(cas_no LIKE '--%') cas_dash, COUNT(DISTINCT chemical||'|'||COALESCE(type_of_toxicity,'')) chem_tox,
       ARRAY_AGG(DISTINCT type_of_toxicity) tox_vals,
       ARRAY_AGG(DISTINCT listing_mechanism) mechs,
       COUNT_IF(NULLIF(TRIM(nsrl_or_madl_g_day::string),'') IS NOT NULL) nsrl_filled,
       SYSTEM$TYPEOF(MAX(date_listed)) date_type, MIN(date_listed) d0, MAX(date_listed) d1, COUNT_IF(date_listed IS NULL) d_null,
       COUNT_IF(col_6 IS NOT NULL OR col_7 IS NOT NULL OR col_8 IS NOT NULL) extra_filled,
       (SELECT MAX(c) FROM (SELECT chemical, COUNT(*) c FROM t GROUP BY 1)) max_rows_per_chem
FROM t;

-- ===== connection 2: S08-S13 =====
-- S08 GUDID staging: what the raw blocks hold (rerun of S04, which failed on the reserved word SAMPLE)
SELECT COUNT(*) n, SYSTEM$TYPEOF(ANY_VALUE(raw)) raw_type, MIN(LEN(raw::string)) len_min, MAX(LEN(raw::string)) len_max,
       COUNT(DISTINCT raw::string) distinct_raw,
       ARRAY_SLICE(ARRAY_AGG(DISTINCT ARRAY_TO_STRING(OBJECT_KEYS(TRY_PARSE_JSON(raw::string)),',')),0,10) keysets,
       ANY_VALUE(LEFT(raw::string, 1200)) raw_sample
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_GUDID__STAGING;

-- S09 UDS Table 3A: per age line, '--' vs zero vs counts, smallest shown count (rerun of S06 with a working line regex)
WITH t AS (SELECT bhcmisid, T3A_L1_CA, T3A_L1_CB, T3A_L2_CA, T3A_L2_CB, T3A_L3_CA, T3A_L3_CB, T3A_L4_CA, T3A_L4_CB, T3A_L5_CA, T3A_L5_CB, T3A_L6_CA, T3A_L6_CB, T3A_L7_CA, T3A_L7_CB, T3A_L8_CA, T3A_L8_CB, T3A_L9_CA, T3A_L9_CB, T3A_L10_CA, T3A_L10_CB, T3A_L11_CA, T3A_L11_CB, T3A_L12_CA, T3A_L12_CB, T3A_L13_CA, T3A_L13_CB, T3A_L14_CA, T3A_L14_CB, T3A_L15_CA, T3A_L15_CB, T3A_L16_CA, T3A_L16_CB, T3A_L17_CA, T3A_L17_CB, T3A_L18_CA, T3A_L18_CB, T3A_L19_CA, T3A_L19_CB, T3A_L20_CA, T3A_L20_CB, T3A_L21_CA, T3A_L21_CB, T3A_L22_CA, T3A_L22_CB, T3A_L23_CA, T3A_L23_CB, T3A_L24_CA, T3A_L24_CB, T3A_L25_CA, T3A_L25_CB, T3A_L26_CA, T3A_L26_CB, T3A_L27_CA, T3A_L27_CB, T3A_L28_CA, T3A_L28_CB, T3A_L29_CA, T3A_L29_CB, T3A_L30_CA, T3A_L30_CB, T3A_L31_CA, T3A_L31_CB, T3A_L32_CA, T3A_L32_CB, T3A_L33_CA, T3A_L33_CB, T3A_L34_CA, T3A_L34_CB, T3A_L35_CA, T3A_L35_CB, T3A_L36_CA, T3A_L36_CB, T3A_L37_CA, T3A_L37_CB, T3A_L38_CA, T3A_L38_CB, T3A_L39_CA, T3A_L39_CB FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_UDS_TABLE3A_PATIENTS),
long AS (SELECT bhcmisid, col, val FROM t UNPIVOT(val FOR col IN (T3A_L1_CA, T3A_L1_CB, T3A_L2_CA, T3A_L2_CB, T3A_L3_CA, T3A_L3_CB, T3A_L4_CA, T3A_L4_CB, T3A_L5_CA, T3A_L5_CB, T3A_L6_CA, T3A_L6_CB, T3A_L7_CA, T3A_L7_CB, T3A_L8_CA, T3A_L8_CB, T3A_L9_CA, T3A_L9_CB, T3A_L10_CA, T3A_L10_CB, T3A_L11_CA, T3A_L11_CB, T3A_L12_CA, T3A_L12_CB, T3A_L13_CA, T3A_L13_CB, T3A_L14_CA, T3A_L14_CB, T3A_L15_CA, T3A_L15_CB, T3A_L16_CA, T3A_L16_CB, T3A_L17_CA, T3A_L17_CB, T3A_L18_CA, T3A_L18_CB, T3A_L19_CA, T3A_L19_CB, T3A_L20_CA, T3A_L20_CB, T3A_L21_CA, T3A_L21_CB, T3A_L22_CA, T3A_L22_CB, T3A_L23_CA, T3A_L23_CB, T3A_L24_CA, T3A_L24_CB, T3A_L25_CA, T3A_L25_CB, T3A_L26_CA, T3A_L26_CB, T3A_L27_CA, T3A_L27_CB, T3A_L28_CA, T3A_L28_CB, T3A_L29_CA, T3A_L29_CB, T3A_L30_CA, T3A_L30_CB, T3A_L31_CA, T3A_L31_CB, T3A_L32_CA, T3A_L32_CB, T3A_L33_CA, T3A_L33_CB, T3A_L34_CA, T3A_L34_CB, T3A_L35_CA, T3A_L35_CB, T3A_L36_CA, T3A_L36_CB, T3A_L37_CA, T3A_L37_CB, T3A_L38_CA, T3A_L38_CB, T3A_L39_CA, T3A_L39_CB))),
p AS (SELECT bhcmisid, TO_NUMBER(REGEXP_SUBSTR(col,'L([0-9]+)_',1,1,'e',1)) line, RIGHT(col,1) sex, val,
             TRY_TO_NUMBER(REPLACE(val,',','')) num FROM long)
SELECT line,
       COUNT_IF(sex='A' AND val='--') m_dash, COUNT_IF(sex='B' AND val='--') f_dash,
       COUNT_IF(num=0) zero_cells, COUNT_IF(num IS NULL AND val<>'--') other_text,
       ARRAY_SLICE(ARRAY_AGG(DISTINCT IFF(num IS NULL AND val<>'--', val, NULL)),0,6) other_vals,
       MIN(IFF(num>0,num,NULL)) min_pos, SUM(IFF(sex='A',num,0)) male_sum, SUM(IFF(sex='B',num,0)) female_sum
FROM p GROUP BY line ORDER BY line;

-- S10 UDS Table 3A: does lines 1-38 add up to the line 39 total, and how big is the gap each '--' hides
WITH t AS (SELECT bhcmisid, T3A_L1_CA, T3A_L1_CB, T3A_L2_CA, T3A_L2_CB, T3A_L3_CA, T3A_L3_CB, T3A_L4_CA, T3A_L4_CB, T3A_L5_CA, T3A_L5_CB, T3A_L6_CA, T3A_L6_CB, T3A_L7_CA, T3A_L7_CB, T3A_L8_CA, T3A_L8_CB, T3A_L9_CA, T3A_L9_CB, T3A_L10_CA, T3A_L10_CB, T3A_L11_CA, T3A_L11_CB, T3A_L12_CA, T3A_L12_CB, T3A_L13_CA, T3A_L13_CB, T3A_L14_CA, T3A_L14_CB, T3A_L15_CA, T3A_L15_CB, T3A_L16_CA, T3A_L16_CB, T3A_L17_CA, T3A_L17_CB, T3A_L18_CA, T3A_L18_CB, T3A_L19_CA, T3A_L19_CB, T3A_L20_CA, T3A_L20_CB, T3A_L21_CA, T3A_L21_CB, T3A_L22_CA, T3A_L22_CB, T3A_L23_CA, T3A_L23_CB, T3A_L24_CA, T3A_L24_CB, T3A_L25_CA, T3A_L25_CB, T3A_L26_CA, T3A_L26_CB, T3A_L27_CA, T3A_L27_CB, T3A_L28_CA, T3A_L28_CB, T3A_L29_CA, T3A_L29_CB, T3A_L30_CA, T3A_L30_CB, T3A_L31_CA, T3A_L31_CB, T3A_L32_CA, T3A_L32_CB, T3A_L33_CA, T3A_L33_CB, T3A_L34_CA, T3A_L34_CB, T3A_L35_CA, T3A_L35_CB, T3A_L36_CA, T3A_L36_CB, T3A_L37_CA, T3A_L37_CB, T3A_L38_CA, T3A_L38_CB, T3A_L39_CA, T3A_L39_CB FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_UDS_TABLE3A_PATIENTS),
long AS (SELECT bhcmisid, col, val FROM t UNPIVOT(val FOR col IN (T3A_L1_CA, T3A_L1_CB, T3A_L2_CA, T3A_L2_CB, T3A_L3_CA, T3A_L3_CB, T3A_L4_CA, T3A_L4_CB, T3A_L5_CA, T3A_L5_CB, T3A_L6_CA, T3A_L6_CB, T3A_L7_CA, T3A_L7_CB, T3A_L8_CA, T3A_L8_CB, T3A_L9_CA, T3A_L9_CB, T3A_L10_CA, T3A_L10_CB, T3A_L11_CA, T3A_L11_CB, T3A_L12_CA, T3A_L12_CB, T3A_L13_CA, T3A_L13_CB, T3A_L14_CA, T3A_L14_CB, T3A_L15_CA, T3A_L15_CB, T3A_L16_CA, T3A_L16_CB, T3A_L17_CA, T3A_L17_CB, T3A_L18_CA, T3A_L18_CB, T3A_L19_CA, T3A_L19_CB, T3A_L20_CA, T3A_L20_CB, T3A_L21_CA, T3A_L21_CB, T3A_L22_CA, T3A_L22_CB, T3A_L23_CA, T3A_L23_CB, T3A_L24_CA, T3A_L24_CB, T3A_L25_CA, T3A_L25_CB, T3A_L26_CA, T3A_L26_CB, T3A_L27_CA, T3A_L27_CB, T3A_L28_CA, T3A_L28_CB, T3A_L29_CA, T3A_L29_CB, T3A_L30_CA, T3A_L30_CB, T3A_L31_CA, T3A_L31_CB, T3A_L32_CA, T3A_L32_CB, T3A_L33_CA, T3A_L33_CB, T3A_L34_CA, T3A_L34_CB, T3A_L35_CA, T3A_L35_CB, T3A_L36_CA, T3A_L36_CB, T3A_L37_CA, T3A_L37_CB, T3A_L38_CA, T3A_L38_CB, T3A_L39_CA, T3A_L39_CB))),
p AS (SELECT bhcmisid, TO_NUMBER(REGEXP_SUBSTR(col,'L([0-9]+)_',1,1,'e',1)) line, RIGHT(col,1) sex, val,
             TRY_TO_NUMBER(REPLACE(val,',','')) num FROM long),
c AS (SELECT bhcmisid, SUM(IFF(line<=38, COALESCE(num,0), 0)) sum138, SUM(IFF(line=39, num, 0)) tot39,
             COUNT_IF(line<=38 AND val='--') dash138, COUNT_IF(line=39 AND num IS NULL) tot_missing
      FROM p GROUP BY 1)
SELECT COUNT(*) centers, COUNT_IF(tot_missing>0) tot39_missing, COUNT_IF(tot_missing=0 AND sum138=tot39) exact,
       COUNT_IF(tot_missing=0 AND sum138<tot39) sum_under, COUNT_IF(tot_missing=0 AND sum138>tot39) sum_over,
       SUM(IFF(tot_missing=0, tot39, 0)) total_patients, SUM(IFF(tot_missing=0, tot39-sum138, 0)) total_gap,
       SUM(IFF(tot_missing=0, dash138, 0)) dash_cells,
       MIN(IFF(tot_missing=0 AND dash138>0, (tot39-sum138)/dash138, NULL)) min_gap_per_dash,
       MEDIAN(IFF(tot_missing=0 AND dash138>0, (tot39-sum138)/dash138, NULL)) med_gap_per_dash,
       MAX(IFF(tot_missing=0 AND dash138>0, (tot39-sum138)/dash138, NULL)) max_gap_per_dash,
       COUNT_IF(tot_missing=0 AND dash138=0 AND sum138<>tot39) nodash_mismatch,
       MEDIAN(IFF(tot_missing=0, tot39, NULL)) median_center, MAX(tot39) max_center, MIN(IFF(tot_missing=0, tot39, NULL)) min_center
FROM c;

-- S11 Prop 65: listings per year, mechanism, safe-harbor fill; names of the null-date rows
SELECT YEAR(date_listed) y, COUNT(*) n, COUNT(DISTINCT chemical) chems,
       COUNT_IF(type_of_toxicity ILIKE '%cancer%') cancer, COUNT_IF(type_of_toxicity ILIKE '%developmental%' OR type_of_toxicity ILIKE '%male%') repro,
       COUNT_IF(listing_mechanism ILIKE '%SQE%') sqe, COUNT_IF(listing_mechanism ILIKE '%AB%') ab,
       COUNT_IF(listing_mechanism ILIKE '%FR%') fr, COUNT_IF(listing_mechanism ILIKE '%LC%') lc,
       COUNT_IF(NULLIF(TRIM(nsrl_or_madl_g_day::string),'') IS NOT NULL) nsrl,
       ARRAY_SLICE(ARRAY_AGG(IFF(date_listed IS NULL, chemical, NULL)),0,12) null_date_names,
       ARRAY_SLICE(ARRAY_AGG(DISTINCT col_6::string),0,3) col6_vals
FROM LIBRARY_MARTS.HEALTH.HEALTH__ST_OEHHA_PROPOSITION_65_LIST GROUP BY 1 ORDER BY 1;

-- S12 Prop 65 x TRI 2023 on CAS: land rate and pounds, split by TRI's own carcinogen flag
WITH p65 AS (SELECT TRIM(cas_no) cas, MIN(chemical) p65_name,
         BOOLOR_AGG(type_of_toxicity ILIKE '%cancer%') p65_cancer,
         BOOLOR_AGG(type_of_toxicity ILIKE '%developmental%' OR type_of_toxicity ILIKE '%male%') p65_repro,
         MIN(date_listed) first_listed
       FROM LIBRARY_MARTS.HEALTH.HEALTH__ST_OEHHA_PROPOSITION_65_LIST WHERE cas_no NOT LIKE '--%' AND NULLIF(TRIM(cas_no),'') IS NOT NULL GROUP BY 1),
tri AS (SELECT TRIM(c_40_cas) cas, MAX(c_37_chemical) tri_name, MAX(c_46_carcinogen) tri_carc,
               COUNT(*) forms, COUNT(DISTINCT c_2_trifd) facs, SUM(TRY_TO_NUMBER(c_107_total_releases)) lbs,
               SUM(IFF(c_8_st='CA', TRY_TO_NUMBER(c_107_total_releases), 0)) ca_lbs
        FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023 WHERE c_50_unit_of_measure ILIKE 'Pounds' GROUP BY 1)
SELECT tri.tri_carc, (p65.cas IS NOT NULL) on_p65, COALESCE(p65.p65_cancer,FALSE) p65_cancer, COALESCE(p65.p65_repro,FALSE) p65_repro,
       COUNT(*) chems, SUM(forms) forms, SUM(lbs) lbs, SUM(ca_lbs) ca_lbs,
       ARRAY_SLICE(ARRAY_AGG(tri_name) WITHIN GROUP (ORDER BY lbs DESC),0,8) top_chems
FROM tri LEFT JOIN p65 ON p65.cas = tri.cas
GROUP BY ROLLUP(1,2,3,4) ORDER BY 1,2,3,4;

-- S13 Prop 65 x TRI 2023: which Prop 65 chemicals carry the pounds; TRI flag vs Prop 65 listing
WITH p65 AS (SELECT TRIM(cas_no) cas, MIN(chemical) p65_name,
         BOOLOR_AGG(type_of_toxicity ILIKE '%cancer%') p65_cancer,
         BOOLOR_AGG(type_of_toxicity ILIKE '%developmental%' OR type_of_toxicity ILIKE '%male%') p65_repro,
         MIN(date_listed) first_listed
       FROM LIBRARY_MARTS.HEALTH.HEALTH__ST_OEHHA_PROPOSITION_65_LIST WHERE cas_no NOT LIKE '--%' AND NULLIF(TRIM(cas_no),'') IS NOT NULL GROUP BY 1),
tri AS (SELECT TRIM(c_40_cas) cas, MAX(c_37_chemical) tri_name, MAX(c_46_carcinogen) tri_carc, MAX(c_43_classification) cls,
               COUNT(DISTINCT c_2_trifd) facs, SUM(TRY_TO_NUMBER(c_107_total_releases)) lbs,
               SUM(IFF(c_8_st='CA', TRY_TO_NUMBER(c_107_total_releases), 0)) ca_lbs,
               COUNT(DISTINCT IFF(c_8_st='CA', c_2_trifd, NULL)) ca_facs
        FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023 WHERE c_50_unit_of_measure ILIKE 'Pounds' GROUP BY 1)
SELECT tri.cas, tri_name, p65_name, tri_carc, p65_cancer, p65_repro, first_listed, facs, ROUND(lbs) lbs, ca_facs, ROUND(ca_lbs) ca_lbs
FROM tri JOIN p65 ON p65.cas = tri.cas
ORDER BY lbs DESC LIMIT 40;

-- ===== connection 3: S14-S18 =====
-- S14 Prop 65 x TRI 2023 on CAS: land rate and pounds, split by TRI's own carcinogen flag (rerun of S12; total_releases is already FLOAT)
WITH p65 AS (SELECT TRIM(cas_no) cas, MIN(chemical) p65_name,
         BOOLOR_AGG(type_of_toxicity ILIKE '%cancer%') p65_cancer,
         BOOLOR_AGG(type_of_toxicity ILIKE '%developmental%' OR type_of_toxicity ILIKE '%male%') p65_repro,
         MIN(date_listed) first_listed
       FROM LIBRARY_MARTS.HEALTH.HEALTH__ST_OEHHA_PROPOSITION_65_LIST WHERE cas_no NOT LIKE '--%' AND NULLIF(TRIM(cas_no),'') IS NOT NULL AND date_listed IS NOT NULL GROUP BY 1),
tri AS (SELECT TRIM(c_40_cas) cas, MAX(c_37_chemical) tri_name, MAX(c_46_carcinogen) tri_carc,
               COUNT(*) forms, COUNT(DISTINCT c_2_trifd) facs, SUM(c_107_total_releases::float) lbs,
               SUM(IFF(c_8_st='CA', c_107_total_releases::float, 0)) ca_lbs
        FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023 WHERE c_50_unit_of_measure ILIKE 'Pounds' GROUP BY 1)
SELECT tri.tri_carc, (p65.cas IS NOT NULL) on_p65, COALESCE(p65.p65_cancer,FALSE) p65_cancer, COALESCE(p65.p65_repro,FALSE) p65_repro,
       COUNT(*) chems, SUM(forms) forms, ROUND(SUM(lbs)) lbs, ROUND(SUM(ca_lbs)) ca_lbs,
       ARRAY_SLICE(ARRAY_AGG(tri_name) WITHIN GROUP (ORDER BY lbs DESC),0,8) top_chems
FROM tri LEFT JOIN p65 ON p65.cas = tri.cas
GROUP BY ROLLUP(1,2,3,4) ORDER BY 1,2,3,4;

-- S15 Prop 65 x TRI 2023: which Prop 65 chemicals carry the pounds; TRI carcinogen flag next to the Prop 65 listing (rerun of S13)
WITH p65 AS (SELECT TRIM(cas_no) cas, MIN(chemical) p65_name,
         BOOLOR_AGG(type_of_toxicity ILIKE '%cancer%') p65_cancer,
         BOOLOR_AGG(type_of_toxicity ILIKE '%developmental%' OR type_of_toxicity ILIKE '%male%') p65_repro,
         MIN(date_listed) first_listed
       FROM LIBRARY_MARTS.HEALTH.HEALTH__ST_OEHHA_PROPOSITION_65_LIST WHERE cas_no NOT LIKE '--%' AND NULLIF(TRIM(cas_no),'') IS NOT NULL AND date_listed IS NOT NULL GROUP BY 1),
tri AS (SELECT TRIM(c_40_cas) cas, MAX(c_37_chemical) tri_name, MAX(c_46_carcinogen) tri_carc, MAX(c_43_classification) cls,
               COUNT(DISTINCT c_2_trifd) facs, SUM(c_107_total_releases::float) lbs,
               SUM(IFF(c_8_st='CA', c_107_total_releases::float, 0)) ca_lbs,
               COUNT(DISTINCT IFF(c_8_st='CA', c_2_trifd, NULL)) ca_facs
        FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023 WHERE c_50_unit_of_measure ILIKE 'Pounds' GROUP BY 1)
SELECT tri.cas, tri_name, p65_name, tri_carc, p65_cancer, p65_repro, first_listed, facs, ROUND(lbs) lbs, ca_facs, ROUND(ca_lbs) ca_lbs
FROM tri JOIN p65 ON p65.cas = tri.cas
ORDER BY lbs DESC LIMIT 40;

-- S16 DPD drug: which days carry the bulk last-update stamps
SELECT last_update_date d, COUNT(*) n, COUNT_IF(drug_class='Human') human, MIN(TRY_TO_NUMBER(drug_code)) code_min, MAX(TRY_TO_NUMBER(drug_code)) code_max
FROM LIBRARY_MARTS.HEALTH.HEALTH__INTL_HEALTHCANADA_DPD_DRUG GROUP BY 1 ORDER BY n DESC LIMIT 10;

-- S17 UDS: patients per weekly open site-hour, joined to the site roster on grant number, ranked inside each state
WITH c AS (SELECT bhcmisid, TRY_TO_NUMBER(REPLACE(T3A_L39_CA,',','')) + TRY_TO_NUMBER(REPLACE(T3A_L39_CB,',','')) tot FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_UDS_TABLE3A_PATIENTS),
i AS (SELECT bhcmisid, grantnumber, healthcentername, healthcentercity, healthcenterstate st, urbanruralflag ur FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_UDS_HEALTH_CENTER_INFO),
s AS (SELECT health_center_number g, COUNT(*) sites, SUM(TRY_TO_NUMBER(operating_hours_per_week::string)) hrs,
             COUNT_IF(location_type_description ILIKE '%mobile%') mobile, COUNT_IF(location_setting_description ILIKE '%school%') school,
             COUNT_IF(site_type_description ILIKE '%admin%' AND site_type_description NOT ILIKE '%service%') admin_only,
             ARRAY_AGG(DISTINCT health_center_type) types
      FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES GROUP BY 1),
j AS (SELECT i.*, c.tot, s.sites, s.hrs, s.mobile, s.school, s.admin_only, s.types, c.tot/NULLIF(s.hrs,0) per_hr
      FROM i JOIN c USING (bhcmisid) LEFT JOIN s ON s.g = i.grantnumber),
r AS (SELECT j.*, COUNT(*) OVER () n_all, COUNT(sites) OVER () n_landed, MEDIAN(per_hr) OVER () nat_med,
             MEDIAN(per_hr) OVER (PARTITION BY st) st_med, COUNT(per_hr) OVER (PARTITION BY st) st_n,
             per_hr / NULLIF(MEDIAN(per_hr) OVER (PARTITION BY st),0) x_state
      FROM j)
SELECT bhcmisid, healthcentername, healthcentercity, st, ur, tot, sites, hrs, mobile, school, admin_only, ROUND(per_hr,1) per_hr,
       ROUND(st_med,1) st_med, st_n, ROUND(x_state,1) x_state, n_all, n_landed, ROUND(nat_med,1) nat_med, types
FROM r WHERE st_n >= 10 ORDER BY x_state DESC NULLS LAST LIMIT 15;

-- S18 GUDID staging: device records per block, first DI of each block, and whether it is already in the 5.08M GUDID table
WITH s AS (SELECT raw:results[0]:identifiers[0]:id::string di0, raw:results[0]:identifiers[0]:type::string di0_type,
                  ARRAY_SIZE(raw:results) k, raw:results[0]:publish_date::string pd
           FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_GUDID__STAGING),
g AS (SELECT DISTINCT primary_di FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_GUDID WHERE primary_di IN (SELECT di0 FROM s))
SELECT COUNT(*) blocks, SUM(k) records, MIN(k) k_min, MAX(k) k_max, COUNT(DISTINCT di0) distinct_first_di,
       ARRAY_AGG(DISTINCT di0_type) di_types, COUNT_IF(g.primary_di IS NOT NULL) first_di_in_main, MIN(pd) pd_min, MAX(pd) pd_max
FROM s LEFT JOIN g ON g.primary_di = s.di0;

-- ===== connection 4: S19-S21 =====
-- S19 Prop 65 hygiene: delisted rows, footnote rows, group listings with no CAS, route-limited listings, how lead is listed
SELECT COUNT(*) n, COUNT_IF(chemical ILIKE '%delisted%') delisted_rows, COUNT_IF(date_listed IS NULL) nodate_rows,
       COUNT_IF(cas_no LIKE '--%') dash_cas, COUNT_IF(cas_no LIKE '--%' AND date_listed IS NOT NULL AND chemical NOT ILIKE '%delisted%') dash_cas_live,
       COUNT_IF(chemical ILIKE ANY ('%ingested%','%airborne%','%gas)%','%inhal%','%oral%','%respirable%')) route_rows,
       COUNT_IF(cas_no LIKE '%,%' OR TRIM(cas_no) LIKE '% %' OR cas_no LIKE '%/%') multi_cas,
       ARRAY_SLICE(ARRAY_AGG(IFF(chemical ILIKE '%delisted%', LEFT(chemical,70), NULL)),0,6) delisted_sample,
       ARRAY_SLICE(ARRAY_AGG(IFF(cas_no LIKE '--%' AND date_listed IS NOT NULL AND chemical NOT ILIKE '%delisted%', LEFT(chemical,60), NULL)),0,15) dash_names,
       ARRAY_AGG(IFF(chemical ILIKE 'lead%' OR chemical ILIKE 'arsenic%' OR chemical ILIKE 'nickel%', LEFT(chemical,50)||' | '||cas_no||' | '||type_of_toxicity, NULL)) metal_rows
FROM LIBRARY_MARTS.HEALTH.HEALTH__ST_OEHHA_PROPOSITION_65_LIST;

-- S20 Prop 65 x TRI 2023, corrected: delisted and footnote rows dropped; total and air pounds by TRI flag and Prop 65 harm
WITH p65 AS (SELECT TRIM(cas_no) cas, MIN(chemical) p65_name,
         BOOLOR_AGG(type_of_toxicity ILIKE '%cancer%') p65_cancer,
         BOOLOR_AGG(type_of_toxicity ILIKE '%developmental%' OR type_of_toxicity ILIKE '%male%') p65_repro,
         BOOLOR_AGG(chemical ILIKE ANY ('%ingested%','%airborne%','%gas)%','%inhal%','%oral%','%respirable%')) route_limited,
         MIN(date_listed) first_listed
       FROM LIBRARY_MARTS.HEALTH.HEALTH__ST_OEHHA_PROPOSITION_65_LIST
       WHERE cas_no NOT LIKE '--%' AND NULLIF(TRIM(cas_no),'') IS NOT NULL AND date_listed IS NOT NULL
         AND chemical NOT ILIKE '%delisted%'
       GROUP BY 1),
tri AS (SELECT TRIM(c_40_cas) cas, MAX(c_46_carcinogen) tri_carc, COUNT(DISTINCT c_2_trifd) facs,
               SUM(c_107_total_releases::float) lbs, SUM(COALESCE(TRY_TO_DOUBLE(c_51_5_1_fugitive_air::string),0)+COALESCE(TRY_TO_DOUBLE(c_52_5_2_stack_air::string),0)) air_lbs,
               SUM(IFF(c_8_st='CA', c_107_total_releases::float, 0)) ca_lbs, SUM(IFF(c_8_st='CA', COALESCE(TRY_TO_DOUBLE(c_51_5_1_fugitive_air::string),0)+COALESCE(TRY_TO_DOUBLE(c_52_5_2_stack_air::string),0), 0)) ca_air
        FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023 WHERE c_50_unit_of_measure ILIKE 'Pounds' GROUP BY 1)
SELECT tri_carc, (p65.cas IS NOT NULL) on_p65, p65_cancer, p65_repro, route_limited,
       COUNT(*) chems, ROUND(SUM(lbs)) lbs, ROUND(SUM(air_lbs)) air_lbs, ROUND(SUM(ca_lbs)) ca_lbs, ROUND(SUM(ca_air)) ca_air
FROM tri LEFT JOIN p65 ON p65.cas = tri.cas
GROUP BY GROUPING SETS ((tri_carc, on_p65, p65_cancer, p65_repro, route_limited), (on_p65), ())
ORDER BY 1,2,3,4,5;

-- S21 California TRI sites: air pounds of Prop 65 chemicals per site, ranked against same-sector California peers, plus ECHO record on FRS ID
WITH p65 AS (SELECT TRIM(cas_no) cas, MIN(chemical) p65_name,
         BOOLOR_AGG(type_of_toxicity ILIKE '%cancer%') p65_cancer,
         BOOLOR_AGG(type_of_toxicity ILIKE '%developmental%' OR type_of_toxicity ILIKE '%male%') p65_repro,
         BOOLOR_AGG(chemical ILIKE ANY ('%ingested%','%airborne%','%gas)%','%inhal%','%oral%','%respirable%')) route_limited,
         MIN(date_listed) first_listed
       FROM LIBRARY_MARTS.HEALTH.HEALTH__ST_OEHHA_PROPOSITION_65_LIST
       WHERE cas_no NOT LIKE '--%' AND NULLIF(TRIM(cas_no),'') IS NOT NULL AND date_listed IS NOT NULL
         AND chemical NOT ILIKE '%delisted%'
       GROUP BY 1),
tri AS (SELECT c_2_trifd trifd, c_3_frs_id::varchar frs, c_4_facility_name name, c_6_city city, c_23_industry_sector sector,
               c_17_standard_parent_co_name parent, c_37_chemical chem, TRIM(c_40_cas) cas, COALESCE(TRY_TO_DOUBLE(c_51_5_1_fugitive_air::string),0)+COALESCE(TRY_TO_DOUBLE(c_52_5_2_stack_air::string),0) air
        FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023 WHERE c_8_st='CA' AND c_50_unit_of_measure ILIKE 'Pounds'),
f AS (SELECT trifd, MAX(frs) frs, MAX(name) name, MAX(city) city, MAX(sector) sector, MAX(parent) parent,
             SUM(IFF(p.cas IS NOT NULL, air, 0)) p65_air, SUM(IFF(p.p65_cancer, air, 0)) cancer_air,
             SUM(IFF(p.cas IS NOT NULL AND NOT COALESCE(p.route_limited,FALSE), air, 0)) p65_air_noroute,
             ARRAY_SLICE(ARRAY_AGG(IFF(p.cas IS NOT NULL AND air>0, chem||' '||ROUND(air), NULL)) WITHIN GROUP (ORDER BY air DESC),0,5) top_chems
      FROM tri LEFT JOIN p65 p ON p.cas = tri.cas GROUP BY 1),
r AS (SELECT f.*, COUNT(*) OVER () ca_facs, SUM(p65_air) OVER () ca_air, p65_air/NULLIF(SUM(p65_air) OVER (),0) share,
             SUM(cancer_air) OVER () ca_cancer_air, cancer_air/NULLIF(SUM(cancer_air) OVER (),0) cancer_share,
             MEDIAN(p65_air) OVER () ca_med, MEDIAN(p65_air) OVER (PARTITION BY sector) sec_med, COUNT(*) OVER (PARTITION BY sector) sec_n
      FROM f WHERE p65_air > 0),
top AS (SELECT * FROM r ORDER BY p65_air DESC LIMIT 12),
e AS (SELECT frs_id::varchar frs_id, MAX(quarters_with_noncompliance) qnc, MAX(formal_action_count) formal, MAX(total_inspection_count) insp,
             MAX(last_penalty_amt_allocated) last_pen_alloc, MAX(date_last_formal_action) last_formal, MAX(compliance_status) status
      FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO WHERE frs_id::varchar IN (SELECT frs FROM top) GROUP BY 1)
SELECT top.name, top.city, top.sector, top.parent, top.frs, ROUND(top.p65_air) p65_air, ROUND(top.p65_air_noroute) p65_air_noroute,
       ROUND(top.cancer_air) cancer_air, ROUND(top.share,3) share, ROUND(top.cancer_share,3) cancer_share,
       ROUND(top.sec_med) sec_med, top.sec_n, ROUND(top.p65_air/NULLIF(top.sec_med,0),1) x_sector, ROUND(top.ca_med) ca_med, top.ca_facs,
       ROUND(top.ca_air) ca_air, ROUND(top.ca_cancer_air) ca_cancer_air, top.top_chems,
       e.qnc, e.formal, e.insp, e.last_pen_alloc, e.last_formal, e.status, (e.frs_id IS NOT NULL) echo_hit
FROM top LEFT JOIN e ON e.frs_id = top.frs ORDER BY top.p65_air DESC;

-- ===== connection 5: S22-S24 =====
-- S22 TRI 2023 trap check: same site + same CAS on more than one row (amendment or double load?)
WITH d AS (SELECT c_2_trifd trifd, TRIM(c_40_cas) cas, COUNT(*) n, COUNT(DISTINCT c_36_doc_ctrl_num) docs, MAX(c_4_facility_name) name, MAX(c_8_st) st,
                  ARRAY_AGG(c_37_chemical||' '||c_49_form_type||' '||ROUND(c_107_total_releases::float)||' air '||ROUND(COALESCE(TRY_TO_DOUBLE(c_51_5_1_fugitive_air::string),0)+COALESCE(TRY_TO_DOUBLE(c_52_5_2_stack_air::string),0))) forms
           FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023 GROUP BY 1,2 HAVING COUNT(*) > 1)
SELECT (SELECT COUNT(*) FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023) all_rows, COUNT(*) dup_pairs, SUM(n) dup_rows, SUM(docs) dup_docs, COUNT_IF(st='CA') ca_dup_pairs,
       ARRAY_SLICE(ARRAY_AGG(name||' ['||st||'] '||cas||' :: '||ARRAY_TO_STRING(forms,' / ')) WITHIN GROUP (ORDER BY st='CA' DESC, n DESC),0,10) sample
FROM d;

-- S23 Styrene air per TRI site: California fiberglass shops ranked against every US styrene reporter and their national sector peers
WITH s AS (SELECT c_2_trifd trifd, MAX(c_4_facility_name) name, MAX(c_6_city) city, MAX(c_8_st) st, MAX(c_23_industry_sector) sector,
                  MAX(c_30_primary_naics) naics, SUM(COALESCE(TRY_TO_DOUBLE(c_51_5_1_fugitive_air::string),0)) fug, SUM(COALESCE(TRY_TO_DOUBLE(c_52_5_2_stack_air::string),0)) stk, SUM(COALESCE(TRY_TO_DOUBLE(c_51_5_1_fugitive_air::string),0)+COALESCE(TRY_TO_DOUBLE(c_52_5_2_stack_air::string),0)) air, MAX(c_49_form_type) form,
                  MAX(c_122_8_9_production_ratio) prod_ratio
           FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023 WHERE TRIM(c_40_cas)='100-42-5' AND c_50_unit_of_measure ILIKE 'Pounds' GROUP BY 1)
SELECT name, city, st, sector, naics, form, ROUND(air) air, ROUND(fug) fug, ROUND(stk) stk, prod_ratio,
       RANK() OVER (ORDER BY air DESC) nat_rank, COUNT(*) OVER () nat_n, ROUND(MEDIAN(air) OVER ()) nat_med,
       ROUND(MEDIAN(air) OVER (PARTITION BY naics)) naics_med, COUNT(*) OVER (PARTITION BY naics) naics_n,
       ROUND(SUM(air) OVER ()) nat_air, ROUND(SUM(IFF(st='CA',air,0)) OVER ()) ca_air, SUM(IFF(st='CA',1,0)) OVER () ca_n,
       ROUND(MEDIAN(IFF(st='CA',air,NULL)) OVER ()) ca_med
FROM s QUALIFY st='CA' ORDER BY air DESC LIMIT 12;

-- S24 UDS: health centers that share a street address or a project director (are they one outfit filed twice?)
WITH i AS (SELECT bhcmisid, grantnumber, healthcentername, healthcentercity, healthcenterstate, fundingchc, fundingmsaw, fundinghp, fundingrph,
                  UPPER(TRIM(healthcenterstreetaddress))||'|'||LEFT(healthcenterzipcode,5) addr,
                  UPPER(REGEXP_REPLACE(TRIM(projectdirector),'[[:space:]]+',' ')) director, LOWER(TRIM(projectdirectoremail)) email
           FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_UDS_HEALTH_CENTER_INFO),
c AS (SELECT bhcmisid, TRY_TO_NUMBER(REPLACE(T3A_L39_CA,',','')) + TRY_TO_NUMBER(REPLACE(T3A_L39_CB,',','')) tot FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_UDS_TABLE3A_PATIENTS),
k AS (SELECT addr, COUNT(*) OVER (PARTITION BY addr) n_addr, COUNT(*) OVER (PARTITION BY director) n_dir, i.* FROM i)
SELECT k.bhcmisid, k.grantnumber, k.healthcentername, k.healthcentercity, k.healthcenterstate, k.director, k.email, k.n_addr, k.n_dir,
       k.fundingchc, k.fundingmsaw, k.fundinghp, k.fundingrph, c.tot
FROM k JOIN c USING (bhcmisid) WHERE k.n_addr > 1 OR k.n_dir > 1 ORDER BY k.addr, k.director;

-- ===== connection 6: S25-S26 =====
-- S25 TRI 2023 trap check: same site + same CAS on more than one row (rerun of S22, which failed on the reserved word SAMPLE)
WITH d AS (SELECT c_2_trifd trifd, TRIM(c_40_cas) cas, COUNT(*) n, COUNT(DISTINCT c_36_doc_ctrl_num) docs, MAX(c_4_facility_name) name, MAX(c_8_st) st,
                  ARRAY_AGG(c_37_chemical||' '||c_49_form_type||' '||ROUND(c_107_total_releases::float)||' air '||ROUND(COALESCE(TRY_TO_DOUBLE(c_51_5_1_fugitive_air::string),0)+COALESCE(TRY_TO_DOUBLE(c_52_5_2_stack_air::string),0))) forms
           FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023 GROUP BY 1,2 HAVING COUNT(*) > 1)
SELECT (SELECT COUNT(*) FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023) all_rows, COUNT(*) dup_pairs, SUM(n) dup_rows, SUM(docs) dup_docs, COUNT_IF(st='CA') ca_dup_pairs,
       COUNT_IF(cas='100-42-5') styrene_dup_pairs,
       ARRAY_SLICE(ARRAY_AGG(name||' ['||st||'] '||cas||' :: '||ARRAY_TO_STRING(forms,' / ')) WITHIN GROUP (ORDER BY st='CA' DESC, n DESC),0,10) examples
FROM d;

-- S26 California air pounds the CAS join cannot see: unmatched TRI rows that are metal/PAC/isocyanate groups or carry TRI's own carcinogen flag (upper bound on what the styrene share misses)
WITH p65 AS (SELECT DISTINCT TRIM(cas_no) cas FROM LIBRARY_MARTS.HEALTH.HEALTH__ST_OEHHA_PROPOSITION_65_LIST
       WHERE cas_no NOT LIKE '--%' AND NULLIF(TRIM(cas_no),'') IS NOT NULL AND date_listed IS NOT NULL AND chemical NOT ILIKE '%delisted%')
SELECT COUNT(*) forms, COUNT(DISTINCT c_2_trifd) sites, ROUND(SUM(COALESCE(TRY_TO_DOUBLE(c_51_5_1_fugitive_air::string),0)+COALESCE(TRY_TO_DOUBLE(c_52_5_2_stack_air::string),0))) air,
       ARRAY_SLICE(ARRAY_AGG(c_37_chemical||' '||ROUND(COALESCE(TRY_TO_DOUBLE(c_51_5_1_fugitive_air::string),0)+COALESCE(TRY_TO_DOUBLE(c_52_5_2_stack_air::string),0))) WITHIN GROUP (ORDER BY COALESCE(TRY_TO_DOUBLE(c_51_5_1_fugitive_air::string),0)+COALESCE(TRY_TO_DOUBLE(c_52_5_2_stack_air::string),0) DESC),0,10) top_rows
FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023 t LEFT JOIN p65 ON p65.cas = TRIM(t.c_40_cas)
WHERE t.c_8_st='CA' AND t.c_50_unit_of_measure ILIKE 'Pounds' AND p65.cas IS NULL
  AND (t.c_46_carcinogen='YES' OR t.c_37_chemical ILIKE ANY ('%lead%','%nickel%','%arsenic%','%cadmium%','%chromium%','%cobalt%','%mercury%','%polycyclic%','%beryllium%','%antimony%','%diisocyanate%'));
