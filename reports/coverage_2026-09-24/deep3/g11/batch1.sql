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
