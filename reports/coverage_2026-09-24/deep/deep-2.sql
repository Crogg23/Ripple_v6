-- deep-2.sql : coverage deep pass, agent deep-2, 2026-09-24
-- Door: Python (connect/db.py). Every connection first ran:
--   ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300
--   ALTER SESSION SET QUERY_TAG = 'coverage-b-2026-09-24'
-- Read-only: SELECT / WITH only. Numbered in run order.

-- [1] all tables: column types for the columns I will use
SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE
FROM LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'ENVIRONMENT'
  AND TABLE_NAME IN ('ENVIRONMENT__FED_EPA_SDWA_SDWA_LCR_SAMPLES','ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT','ENVIRONMENT__FED_EPA_TRI_BASIC_2023','ENVIRONMENT__FED_FRACFOCUS_REGISTRY','ENVIRONMENT__FED_NID_DAMS','ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS')
  AND COLUMN_NAME IN ('SAMPLE_MEASURE','SAMPLING_END_DATE','SAMPLING_START_DATE','COMPL_PER_BEGIN_DATE','NON_COMPL_PER_BEGIN_DATE','NON_COMPL_PER_END_DATE','ENFORCEMENT_DATE','ENFORCEMENT_ID','VIOLATION_ID','SEVERITY_IND_CNT','CALCULATED_RTC_DATE','C_65_ON_SITE_RELEASE_TOTAL','C_107_TOTAL_RELEASES','C_51_5_1_FUGITIVE_AIR','C_52_5_2_STACK_AIR','C_12_LATITUDE','TVD','TOTAL_BASE_WATER_VOLUME','MASS_INGREDIENT','PERCENT_HF_JOB','JOB_START_DATE','LAST_INSPECTION_DATE','NID_HEIGHT_FT','YEAR_COMPLETED','INSPECTION_FREQUENCY','HAS_EMERGENCY_ACTION_PLAN','POPULATION_SERVED_COUNT','PWS_DEACTIVATION_DATE','CONDITION_ASSESSMENT_DATE','_SRC_FILE')
ORDER BY 1, 2;

-- [2] LCR sample
SELECT * FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_LCR_SAMPLES LIMIT 5;

-- [3] VIOL sample
SELECT * FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT LIMIT 5;

-- [4] TRI sample (key columns)
SELECT C_2_TRIFD, C_4_FACILITY_NAME, C_6_CITY, C_8_ST, C_17_STANDARD_PARENT_CO_NAME, C_23_INDUSTRY_SECTOR, C_37_CHEMICAL, C_50_UNIT_OF_MEASURE, C_49_FORM_TYPE, C_52_5_2_STACK_AIR, C_65_ON_SITE_RELEASE_TOTAL, C_88_OFF_SITE_RELEASE_TOTAL, C_107_TOTAL_RELEASES
FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023 LIMIT 5;

-- [5] FRACFOCUS sample
SELECT * FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_FRACFOCUS_REGISTRY LIMIT 5;

-- [6] NID sample
SELECT * FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_NID_DAMS LIMIT 5;

-- [7] LCR count + profile by contaminant and unit
SELECT CONTAMINANT_CODE, UNIT_OF_MEASURE, COUNT(*) n, COUNT(DISTINCT SAR_ID) sar_ids, COUNT(DISTINCT PWSID) systems,
  COUNT(DISTINCT SUBMISSIONYEARQUARTER) releases, MIN(SAMPLING_END_DATE) min_end, MAX(SAMPLING_END_DATE) max_end,
  MEDIAN(SAMPLE_MEASURE) med, APPROX_PERCENTILE(SAMPLE_MEASURE, 0.99) p99, MAX(SAMPLE_MEASURE) mx,
  COUNT_IF(SAMPLE_MEASURE > 0.015) over_015, COUNT_IF(SAMPLE_MEASURE > 1) over_1, COUNT_IF(SAMPLE_MEASURE >= 15) ge_15,
  COUNT_IF(RESULT_SIGN_CODE IS NOT NULL) sign_filled, COUNT_IF(SAMPLING_END_DATE > '2026-09-24') future_end
FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_LCR_SAMPLES
GROUP BY 1, 2 ORDER BY n DESC;

-- [8] VIOL count + profile: health flag x status x enforcement link
SELECT IS_HEALTH_BASED_IND, VIOLATION_STATUS,
  CASE WHEN ENFORCEMENT_ID IS NULL THEN 'no_enf' WHEN ENFORCEMENT_ID LIKE '99999%' THEN 'enf_9999_placeholder' ELSE 'enf_real' END enf,
  COUNT(*) n, COUNT_IF(VIOLATION_ID IS NULL) no_viol_id, APPROX_COUNT_DISTINCT(PWSID || '|' || VIOLATION_ID) viol_keys,
  COUNT(DISTINCT SUBMISSIONYEARQUARTER) releases, MIN(COMPL_PER_BEGIN_DATE) min_b, MAX(COMPL_PER_BEGIN_DATE) max_b,
  COUNT_IF(COMPL_PER_BEGIN_DATE < '1970-01-01') pre1970
FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT
GROUP BY 1, 2, 3 ORDER BY n DESC;

-- [9] TRI count + profile by unit and form type
SELECT C_1_YEAR, C_50_UNIT_OF_MEASURE, C_49_FORM_TYPE, COUNT(*) n, COUNT(DISTINCT C_2_TRIFD) facilities,
  SUM(C_65_ON_SITE_RELEASE_TOTAL) onsite, SUM(C_107_TOTAL_RELEASES) total_rel, MAX(C_65_ON_SITE_RELEASE_TOTAL) mx,
  COUNT_IF(C_65_ON_SITE_RELEASE_TOTAL IS NULL) onsite_null, COUNT(DISTINCT C_36_DOC_CTRL_NUM) docs
FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023
GROUP BY 1, 2, 3 ORDER BY n DESC;

-- [10] FRACFOCUS count + profile
SELECT COUNT(*) n, COUNT(DISTINCT INGREDIENT_RECORD_ID) ing_ids, COUNT(DISTINCT DISCLOSURE_ID) disclosures, COUNT(DISTINCT API_NUMBER) wells,
  COUNT(DISTINCT OPERATOR_NAME) operators, COUNT(DISTINCT STATE_NAME) states, COUNT(DISTINCT _SRC_FILE) files,
  COUNT_IF(JOB_START_DATE IS NOT NULL) job_date_filled,
  COUNT_IF(REGEXP_LIKE(TRIM(CAS_NUMBER), '[0-9]{2,7}-[0-9]{2}-[0-9]')) cas_numeric,
  COUNT_IF(CAS_NUMBER IS NULL OR TRIM(CAS_NUMBER) = '') cas_blank,
  COUNT_IF(TOTAL_BASE_WATER_VOLUME IS NULL) water_null, COUNT_IF(TOTAL_BASE_WATER_VOLUME = 0) water_zero
FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_FRACFOCUS_REGISTRY;

-- [11] FRACFOCUS non-numeric CAS values (trade secret markers)
SELECT UPPER(TRIM(CAS_NUMBER)) cas, COUNT(*) n
FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_FRACFOCUS_REGISTRY
WHERE NOT REGEXP_LIKE(TRIM(CAS_NUMBER), '[0-9]{2,7}-[0-9]{2}-[0-9]') OR CAS_NUMBER IS NULL
GROUP BY 1 ORDER BY n DESC LIMIT 40;

-- [12] NID count + profile: hazard x condition
SELECT HAZARD_POTENTIAL, CONDITION_ASSESSMENT, COUNT(*) n, COUNT(DISTINCT NID_ID) ids, COUNT_IF(IS_ASSOCIATED_STRUCTURE) assoc,
  COUNT_IF(LAST_INSPECTION_DATE IS NULL) insp_null, COUNT_IF(LAST_INSPECTION_DATE = '1980-01-01') insp_1980,
  COUNT_IF(LAST_INSPECTION_DATE < '2021-09-24') insp_5y_old, COUNT_IF(HAS_EMERGENCY_ACTION_PLAN) eap_true,
  MIN(LAST_INSPECTION_DATE) min_i, MAX(LAST_INSPECTION_DATE) max_i
FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_NID_DAMS
GROUP BY 1, 2 ORDER BY 1, n DESC;

-- [13] LCR lead: systems over 0.015 mg/L at the 90th percentile in 3+ periods since 2015 (0.015 < v <= 1), joined to PWS, top 40 by population
WITH pb AS (
  SELECT PWSID, SAMPLING_START_DATE s, SAMPLING_END_DATE e, MAX(SAMPLE_MEASURE) v
  FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_LCR_SAMPLES
  WHERE CONTAMINANT_CODE = 'PB90' AND SAMPLING_END_DATE BETWEEN '2015-01-01' AND '2026-09-24'
  GROUP BY 1, 2, 3
), per AS (
  SELECT PWSID, COUNT(*) periods, COUNT_IF(v > 0.015 AND v <= 1) over_periods, COUNT_IF(v > 1) unit_suspect,
    MIN(IFF(v > 0.015 AND v <= 1, e, NULL)) first_over, MAX(IFF(v > 0.015 AND v <= 1, e, NULL)) last_over,
    MAX(IFF(v <= 1, v, NULL)) max_mgl, MAX_BY(v, e) latest_v, MAX(e) latest_e
  FROM pb GROUP BY 1
), pws AS (
  SELECT PWSID, COUNT(*) pws_rows, ANY_VALUE(PWS_NAME) pws_name, ANY_VALUE(STATE_CODE) st, MAX(POPULATION_SERVED_COUNT) pop,
    ANY_VALUE(PWS_TYPE_CODE) typ, ANY_VALUE(PWS_ACTIVITY_CODE) act, MAX(PWS_DEACTIVATION_DATE) deact
  FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS GROUP BY 1
)
SELECT per.PWSID, pws.pws_name, pws.st, pws.typ, pws.act, pws.pop, per.periods, per.over_periods, per.first_over, per.last_over,
  per.max_mgl, per.latest_v, per.latest_e, pws.pws_rows,
  COUNT(*) OVER () n_qualifying, SUM(pws.pop) OVER () pop_qualifying,
  COUNT_IF(pws.act = 'A' AND pws.typ = 'CWS') OVER () n_active_cws
FROM per LEFT JOIN pws ON pws.PWSID = per.PWSID
WHERE per.over_periods >= 3
ORDER BY pws.pop DESC NULLS LAST LIMIT 40;

-- [14] LCR lead: peers by system type and size band, active systems, since 2015
WITH pb AS (
  SELECT PWSID, SAMPLING_END_DATE e, MAX(SAMPLE_MEASURE) v
  FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_LCR_SAMPLES
  WHERE CONTAMINANT_CODE = 'PB90' AND SAMPLING_END_DATE BETWEEN '2015-01-01' AND '2026-09-24'
  GROUP BY 1, 2
), per AS (
  SELECT PWSID, COUNT(*) periods, COUNT_IF(v > 0.015 AND v <= 1) over_periods, MAX_BY(v, e) latest_v
  FROM pb GROUP BY 1
), pws AS (
  SELECT PWSID, MAX(POPULATION_SERVED_COUNT) pop, ANY_VALUE(PWS_TYPE_CODE) typ, ANY_VALUE(PWS_ACTIVITY_CODE) act
  FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS GROUP BY 1
)
SELECT pws.typ, CASE WHEN pop <= 500 THEN '1: <=500' WHEN pop <= 3300 THEN '2: 501-3.3K' WHEN pop <= 10000 THEN '3: 3.3K-10K'
    WHEN pop <= 100000 THEN '4: 10K-100K' ELSE '5: >100K' END band,
  COUNT(*) systems, SUM(pop) pop, COUNT_IF(over_periods >= 1) ever_over, COUNT_IF(over_periods >= 3) over_3plus,
  COUNT_IF(latest_v > 0.015 AND latest_v <= 1) latest_over, SUM(IFF(latest_v > 0.015 AND latest_v <= 1, pop, 0)) pop_latest_over,
  SUM(IFF(over_periods >= 3, pop, 0)) pop_over_3plus,
  ROUND(100 * COUNT_IF(over_periods >= 1) / COUNT(*), 1) pct_ever_over
FROM per JOIN pws ON pws.PWSID = per.PWSID
WHERE pws.act = 'A'
GROUP BY 1, 2 ORDER BY 1, 2;

-- [15] LCR value bands for PB90 and CU90 (unit check), with sample systems in the top band
SELECT CONTAMINANT_CODE,
  CASE WHEN SAMPLE_MEASURE <= 0.015 THEN 'a <=0.015' WHEN SAMPLE_MEASURE <= 0.05 THEN 'b 0.015-0.05' WHEN SAMPLE_MEASURE <= 0.1 THEN 'c 0.05-0.1'
       WHEN SAMPLE_MEASURE <= 1 THEN 'd 0.1-1' WHEN SAMPLE_MEASURE <= 15 THEN 'e 1-15' WHEN SAMPLE_MEASURE <= 1000 THEN 'f 15-1000' ELSE 'g >1000' END band,
  COUNT(*) n, COUNT(DISTINCT PWSID) systems, COUNT_IF(SAMPLE_MEASURE = ROUND(SAMPLE_MEASURE)) whole_numbers,
  ARRAY_SLICE(ARRAY_AGG(PWSID || '=' || SAMPLE_MEASURE) WITHIN GROUP (ORDER BY SAMPLE_MEASURE DESC), 0, 4) top_examples
FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_LCR_SAMPLES
GROUP BY 1, 2 ORDER BY 1, 2;

-- [16] VIOL: per system, health-based violations begun 2015+, deduped to one row per violation, no formal action, joined to PWS; top 30 by population
WITH v AS (
  SELECT PWSID, VIOLATION_ID, ANY_VALUE(VIOLATION_CATEGORY_CODE) cat, ANY_VALUE(CONTAMINANT_CODE) contam, ANY_VALUE(VIOLATION_STATUS) status,
    MIN(COMPL_PER_BEGIN_DATE) b,
    COUNT_IF(ENF_ACTION_CATEGORY = 'Formal') n_formal, COUNT_IF(ENF_ACTION_CATEGORY = 'Informal') n_informal
  FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT
  WHERE IS_HEALTH_BASED_IND = 'Y' AND VIOLATION_ID IS NOT NULL AND COMPL_PER_BEGIN_DATE BETWEEN '2015-01-01' AND '2026-09-24'
  GROUP BY 1, 2
), per AS (
  SELECT PWSID, COUNT(*) hb, COUNT_IF(n_formal = 0) hb_no_formal, COUNT_IF(n_formal = 0 AND n_informal = 0) hb_no_action,
    COUNT_IF(status = 'Unaddressed') unaddressed_now, COUNT(DISTINCT YEAR(b)) yrs, MIN(b) first_b, MAX(b) last_b,
    MODE(contam) top_contam, MODE(cat) top_cat
  FROM v GROUP BY 1
), pws AS (
  SELECT PWSID, ANY_VALUE(PWS_NAME) pws_name, ANY_VALUE(STATE_CODE) st, MAX(POPULATION_SERVED_COUNT) pop,
    ANY_VALUE(PWS_TYPE_CODE) typ, ANY_VALUE(PWS_ACTIVITY_CODE) act
  FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS GROUP BY 1
)
SELECT per.*, pws.pws_name, pws.st, pws.typ, pws.act, pws.pop,
  COUNT(*) OVER () n_qualifying, SUM(pws.pop) OVER () pop_qualifying
FROM per LEFT JOIN pws ON pws.PWSID = per.PWSID
WHERE per.hb_no_formal >= 5 AND per.yrs >= 3
ORDER BY pws.pop DESC NULLS LAST LIMIT 30;

-- [17] VIOL: state peers, health-based violations begun 2015+, share with no formal action / no action / unaddressed
WITH v AS (
  SELECT PWSID, VIOLATION_ID, ANY_VALUE(VIOLATION_STATUS) status,
    COUNT_IF(ENF_ACTION_CATEGORY = 'Formal') n_formal, COUNT_IF(ENF_ACTION_CATEGORY = 'Informal') n_informal,
    COUNT_IF(ENF_ACTION_CATEGORY = 'Resolving') n_resolving
  FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT
  WHERE IS_HEALTH_BASED_IND = 'Y' AND VIOLATION_ID IS NOT NULL AND COMPL_PER_BEGIN_DATE BETWEEN '2015-01-01' AND '2026-09-24'
  GROUP BY 1, 2
)
SELECT LEFT(PWSID, 2) st, COUNT(*) hb_viol, COUNT(DISTINCT PWSID) systems,
  ROUND(100 * COUNT_IF(n_formal = 0) / COUNT(*), 1) pct_no_formal,
  ROUND(100 * COUNT_IF(n_formal = 0 AND n_informal = 0) / COUNT(*), 1) pct_no_action,
  ROUND(100 * COUNT_IF(status = 'Unaddressed') / COUNT(*), 1) pct_unaddressed,
  COUNT_IF(status = 'Unaddressed') unaddressed, SUM(n_formal) formal_rows, SUM(n_informal) informal_rows, SUM(n_resolving) resolving_rows
FROM v GROUP BY 1 HAVING COUNT(*) >= 200 ORDER BY pct_no_formal DESC;

-- [18] LCR unit check by state: PB90 rows 2015+, median and share of values between 1 and 15 (ppb-looking), states ranked by median
SELECT LEFT(PWSID, 2) st, COUNT(*) n, MEDIAN(SAMPLE_MEASURE) med, COUNT_IF(SAMPLE_MEASURE > 0.015 AND SAMPLE_MEASURE <= 1) over_in_band,
  COUNT_IF(SAMPLE_MEASURE > 1) over_1, ROUND(100 * COUNT_IF(SAMPLE_MEASURE > 1) / COUNT(*), 1) pct_over_1,
  COUNT_IF(SAMPLE_MEASURE > 0.1 AND SAMPLE_MEASURE <= 1) band_01_1
FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_LCR_SAMPLES
WHERE CONTAMINANT_CODE = 'PB90' AND SAMPLING_END_DATE BETWEEN '2015-01-01' AND '2026-09-24'
GROUP BY 1 ORDER BY pct_over_1 DESC, med DESC LIMIT 12;

-- [19] VIOL: by primacy agency (who regulates), health-based violations begun 2015+, share with no action at all and share unaddressed today
WITH v AS (
  SELECT PWSID, VIOLATION_ID, ANY_VALUE(VIOLATION_STATUS) status, MIN(COMPL_PER_BEGIN_DATE) b,
    COUNT_IF(ENF_ACTION_CATEGORY IN ('Formal', 'Informal')) n_action
  FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT
  WHERE IS_HEALTH_BASED_IND = 'Y' AND VIOLATION_ID IS NOT NULL AND COMPL_PER_BEGIN_DATE BETWEEN '2015-01-01' AND '2026-09-24'
  GROUP BY 1, 2
), pws AS (
  SELECT PWSID, ANY_VALUE(PRIMACY_AGENCY_CODE) prim, ANY_VALUE(PRIMACY_TYPE) ptype, MAX(POPULATION_SERVED_COUNT) pop, ANY_VALUE(PWS_TYPE_CODE) typ
  FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS GROUP BY 1
), sys AS (
  SELECT v.PWSID, pws.prim, pws.ptype, pws.pop, pws.typ, COUNT(*) hb, COUNT_IF(n_action = 0) hb_no_action,
    COUNT_IF(status = 'Unaddressed') unaddr, MIN(IFF(status = 'Unaddressed', b, NULL)) oldest_unaddr
  FROM v LEFT JOIN pws ON pws.PWSID = v.PWSID GROUP BY 1, 2, 3, 4, 5
)
SELECT CASE WHEN ptype = 'State' THEN 'ALL STATE-RUN (' || COUNT(DISTINCT prim) || ' agencies)' ELSE prim || ' ' || ptype END regulator,
  COUNT(*) systems, SUM(hb) hb_viol, ROUND(100 * SUM(hb_no_action) / SUM(hb), 1) pct_no_action,
  ROUND(100 * SUM(unaddr) / SUM(hb), 1) pct_unaddressed, SUM(unaddr) unaddressed, COUNT_IF(unaddr > 0) systems_w_unaddr,
  SUM(IFF(unaddr > 0 AND typ = 'CWS', pop, 0)) cws_pop_w_unaddr, MEDIAN(IFF(unaddr > 0, DATEDIFF('day', oldest_unaddr, '2026-09-24'), NULL)) med_days_oldest_unaddr
FROM sys
GROUP BY CASE WHEN ptype = 'State' THEN 'ALL STATE-RUN (' || 'x' || ')' ELSE prim || ' ' || ptype END, ptype, IFF(ptype = 'State', NULL, prim)
ORDER BY hb_viol DESC;

-- [20] VIOL: systems holding health-based violations that are Unaddressed today, begun 2015+, top 30 by population
WITH v AS (
  SELECT PWSID, VIOLATION_ID, ANY_VALUE(VIOLATION_STATUS) status, ANY_VALUE(CONTAMINANT_CODE) contam, ANY_VALUE(VIOLATION_CATEGORY_CODE) cat,
    MIN(COMPL_PER_BEGIN_DATE) b, COUNT_IF(ENF_ACTION_CATEGORY IN ('Formal', 'Informal')) n_action
  FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT
  WHERE IS_HEALTH_BASED_IND = 'Y' AND VIOLATION_ID IS NOT NULL AND COMPL_PER_BEGIN_DATE BETWEEN '2015-01-01' AND '2026-09-24'
  GROUP BY 1, 2
), pws AS (
  SELECT PWSID, ANY_VALUE(PWS_NAME) pws_name, ANY_VALUE(STATE_CODE) st, ANY_VALUE(PRIMACY_AGENCY_CODE) prim, MAX(POPULATION_SERVED_COUNT) pop,
    ANY_VALUE(PWS_TYPE_CODE) typ, ANY_VALUE(PWS_ACTIVITY_CODE) act
  FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS GROUP BY 1
), sys AS (
  SELECT PWSID, COUNT(*) hb, COUNT_IF(status = 'Unaddressed') unaddr, COUNT_IF(status = 'Unaddressed' AND n_action = 0) unaddr_no_action,
    MIN(IFF(status = 'Unaddressed', b, NULL)) oldest_unaddr, MODE(IFF(status = 'Unaddressed', contam, NULL)) unaddr_contam,
    MODE(IFF(status = 'Unaddressed', cat, NULL)) unaddr_cat
  FROM v GROUP BY 1 HAVING COUNT_IF(status = 'Unaddressed') > 0
)
SELECT sys.*, pws.pws_name, pws.st, pws.prim, pws.typ, pws.act, pws.pop,
  COUNT(*) OVER () n_systems, SUM(IFF(pws.typ = 'CWS', pws.pop, 0)) OVER () cws_pop_total,
  COUNT_IF(pws.typ = 'CWS' AND pws.pop > 10000) OVER () cws_over_10k
FROM sys LEFT JOIN pws ON pws.PWSID = sys.PWSID
ORDER BY pws.pop DESC NULLS LAST LIMIT 30;

-- [21] TRI: top 25 facilities by on-site release, pounds rows only, with share of national on-site total
WITH f AS (
  SELECT C_2_TRIFD, ANY_VALUE(C_4_FACILITY_NAME) fac, ANY_VALUE(C_6_CITY) city, ANY_VALUE(C_8_ST) st, ANY_VALUE(C_17_STANDARD_PARENT_CO_NAME) parent,
    ANY_VALUE(C_23_INDUSTRY_SECTOR) sector, SUM(C_65_ON_SITE_RELEASE_TOTAL) onsite, MAX_BY(C_37_CHEMICAL, C_65_ON_SITE_RELEASE_TOTAL) top_chem,
    MAX(C_65_ON_SITE_RELEASE_TOTAL) top_chem_lb
  FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023
  WHERE C_50_UNIT_OF_MEASURE = 'Pounds'
  GROUP BY 1
)
SELECT f.*, ROUND(100 * onsite / SUM(onsite) OVER (), 2) pct_nat,
  ROUND(100 * SUM(onsite) OVER (ORDER BY onsite DESC ROWS UNBOUNDED PRECEDING) / SUM(onsite) OVER (), 1) cum_pct,
  COUNT(*) OVER () facilities, SUM(onsite) OVER () nat_onsite
FROM f QUALIFY ROW_NUMBER() OVER (ORDER BY onsite DESC) <= 25 ORDER BY onsite DESC;

-- [22] TRI: sector split of on-site release, plus facility concentration within sector
WITH f AS (
  SELECT C_2_TRIFD, ANY_VALUE(C_23_INDUSTRY_SECTOR) sector, SUM(C_65_ON_SITE_RELEASE_TOTAL) onsite
  FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023
  WHERE C_50_UNIT_OF_MEASURE = 'Pounds' GROUP BY 1
), r AS (
  SELECT f.*, PERCENT_RANK() OVER (ORDER BY onsite DESC) pr, ROW_NUMBER() OVER (ORDER BY onsite DESC) rn FROM f
)
SELECT sector, COUNT(*) facilities, SUM(onsite) onsite, ROUND(100 * SUM(onsite) / SUM(SUM(onsite)) OVER (), 1) pct_nat,
  COUNT_IF(rn <= 218) in_top_1pct_facilities, SUM(IFF(rn <= 218, onsite, 0)) onsite_top_1pct
FROM r GROUP BY 1 ORDER BY onsite DESC LIMIT 15;

-- [23] TRI: non-mining facilities, carcinogen air releases (stack + fugitive), top 20
WITH f AS (
  SELECT C_2_TRIFD, ANY_VALUE(C_4_FACILITY_NAME) fac, ANY_VALUE(C_6_CITY) city, ANY_VALUE(C_8_ST) st, ANY_VALUE(C_17_STANDARD_PARENT_CO_NAME) parent,
    ANY_VALUE(C_23_INDUSTRY_SECTOR) sector,
    SUM(COALESCE(TRY_TO_DOUBLE(C_51_5_1_FUGITIVE_AIR), 0) + COALESCE(TRY_TO_DOUBLE(C_52_5_2_STACK_AIR), 0)) carc_air,
    MAX_BY(C_37_CHEMICAL, COALESCE(TRY_TO_DOUBLE(C_51_5_1_FUGITIVE_AIR), 0) + COALESCE(TRY_TO_DOUBLE(C_52_5_2_STACK_AIR), 0)) top_chem,
    COUNT_IF(TRY_TO_DOUBLE(C_52_5_2_STACK_AIR) IS NULL AND C_52_5_2_STACK_AIR IS NOT NULL) bad_text
  FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023
  WHERE C_50_UNIT_OF_MEASURE = 'Pounds' AND C_46_CARCINOGEN = 'YES' AND C_23_INDUSTRY_SECTOR NOT ILIKE '%mining%'
  GROUP BY 1
)
SELECT f.*, ROUND(100 * carc_air / SUM(carc_air) OVER (), 2) pct, COUNT_IF(carc_air > 0) OVER () facilities_w_carc_air, SUM(carc_air) OVER () total_carc_air
FROM f QUALIFY ROW_NUMBER() OVER (ORDER BY carc_air DESC) <= 20 ORDER BY carc_air DESC;

-- [24] VIOL (rerun of [19], group-by fixed): by primacy agency, health-based violations begun 2015+; lead-service-line inventory code 5200 split out
WITH v AS (
  SELECT PWSID, VIOLATION_ID, ANY_VALUE(VIOLATION_STATUS) status, ANY_VALUE(CONTAMINANT_CODE) contam, MIN(COMPL_PER_BEGIN_DATE) b,
    COUNT_IF(ENF_ACTION_CATEGORY IN ('Formal', 'Informal')) n_action
  FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT
  WHERE IS_HEALTH_BASED_IND = 'Y' AND VIOLATION_ID IS NOT NULL AND COMPL_PER_BEGIN_DATE BETWEEN '2015-01-01' AND '2026-09-24'
  GROUP BY 1, 2
), pws AS (
  SELECT PWSID, ANY_VALUE(PRIMACY_AGENCY_CODE) prim, ANY_VALUE(PRIMACY_TYPE) ptype, MAX(POPULATION_SERVED_COUNT) pop, ANY_VALUE(PWS_TYPE_CODE) typ
  FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS GROUP BY 1
), sys AS (
  SELECT v.PWSID, pws.prim, pws.ptype, pws.pop, pws.typ,
    COUNT_IF(contam <> '5200') hb, COUNT_IF(contam <> '5200' AND n_action = 0) hb_no_action,
    COUNT_IF(contam <> '5200' AND status = 'Unaddressed') unaddr, COUNT_IF(contam = '5200') lsl_5200,
    MIN(IFF(contam <> '5200' AND status = 'Unaddressed', b, NULL)) oldest_unaddr
  FROM v LEFT JOIN pws ON pws.PWSID = v.PWSID GROUP BY 1, 2, 3, 4, 5
)
SELECT prim, ptype, COUNT(*) systems, SUM(hb) hb_viol_ex5200, ROUND(100 * SUM(hb_no_action) / NULLIF(SUM(hb), 0), 1) pct_no_action,
  ROUND(100 * SUM(unaddr) / NULLIF(SUM(hb), 0), 1) pct_unaddressed, SUM(unaddr) unaddressed, COUNT_IF(unaddr > 0) systems_w_unaddr,
  SUM(IFF(unaddr > 0 AND typ = 'CWS', pop, 0)) cws_pop_w_unaddr, MEDIAN(IFF(unaddr > 0, DATEDIFF('day', oldest_unaddr, '2026-09-24'), NULL)) med_days_oldest_unaddr,
  SUM(lsl_5200) lsl_5200_viol
FROM sys GROUP BY 1, 2 HAVING SUM(hb) >= 150 ORDER BY pct_no_action DESC;

-- [25] FRACFOCUS: operator x state, one row per disclosure first; share of CAS-bearing ingredient rows withheld as secret, water per job, with the state's own share as the peer
WITH d AS (
  SELECT DISCLOSURE_ID, ANY_VALUE(OPERATOR_NAME) op, ANY_VALUE(STATE_NAME) st, COUNT(*) n_rows,
    COUNT_IF(NULLIF(TRIM(CAS_NUMBER), '') IS NOT NULL) n_cas_rows,
    COUNT_IF(CAS_NUMBER ILIKE ANY ('%proprietary%', '%confidential%', '%trade secret%', 'CBI')) n_secret,
    MAX(TOTAL_BASE_WATER_VOLUME) water, MIN(TOTAL_BASE_WATER_VOLUME) water_min
  FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_FRACFOCUS_REGISTRY GROUP BY 1
), os AS (
  SELECT op, st, COUNT(*) disclosures, SUM(n_cas_rows) cas_rows, SUM(n_secret) secret_rows,
    ROUND(100 * SUM(n_secret) / NULLIF(SUM(n_cas_rows), 0), 1) pct_secret, ROUND(100 * COUNT_IF(n_secret > 0) / COUNT(*), 1) pct_jobs_w_secret,
    ROUND(SUM(water) / 1e9, 2) water_bn_gal, MEDIAN(water) med_water_per_job
  FROM d GROUP BY 1, 2
), w AS (
  SELECT os.*, ROUND(100 * SUM(secret_rows) OVER (PARTITION BY st) / SUM(cas_rows) OVER (PARTITION BY st), 1) state_pct_secret,
    SUM(disclosures) OVER (PARTITION BY st) state_disclosures, ROUND(100 * SUM(secret_rows) OVER () / SUM(cas_rows) OVER (), 1) nat_pct_secret
  FROM os
)
SELECT w.*, ROUND(pct_secret - state_pct_secret, 1) pts_over_state
FROM w
QUALIFY ROW_NUMBER() OVER (ORDER BY disclosures DESC) <= 20
  OR (disclosures >= 500 AND ROW_NUMBER() OVER (ORDER BY IFF(disclosures >= 500, pct_secret - state_pct_secret, -999) DESC) <= 12)
ORDER BY disclosures DESC;

-- [26] FRACFOCUS checks: water per job spread, repetition within a disclosure, form versions, Clayton Williams depth, wells with several disclosures
WITH d AS (
  SELECT DISCLOSURE_ID, ANY_VALUE(API_NUMBER) api, ANY_VALUE(OPERATOR_NAME) op, ANY_VALUE(FF_VERSION) ffv,
    MAX(TOTAL_BASE_WATER_VOLUME) water, MIN(TOTAL_BASE_WATER_VOLUME) water_min, MAX(TVD) tvd
  FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_FRACFOCUS_REGISTRY GROUP BY 1
)
SELECT COUNT(*) disclosures, COUNT_IF(water <> water_min) water_varies_in_disclosure,
  MEDIAN(water) p50_water, APPROX_PERCENTILE(water, 0.9) p90, APPROX_PERCENTILE(water, 0.99) p99, MAX(water) max_water,
  COUNT_IF(water > 100000000) jobs_over_100m_gal, COUNT_IF(water < 1000) jobs_under_1k_gal,
  ROUND(SUM(water) / 1e9, 1) total_water_bn_gal,
  COUNT_IF(ffv::VARCHAR = '1') v1, COUNT_IF(ffv::VARCHAR = '2') v2, COUNT_IF(ffv::VARCHAR = '3') v3, COUNT_IF(ffv::VARCHAR = '4') v4,
  MAX(IFF(op ILIKE 'Clayton Williams%', tvd, NULL)) cwei_max_tvd, COUNT_IF(op ILIKE 'Clayton Williams%' AND tvd > 40000) cwei_tvd_over_40k,
  COUNT_IF(tvd > 40000) all_tvd_over_40k, COUNT(DISTINCT api) wells, COUNT(*) - COUNT(DISTINCT api) extra_disclosures_on_same_well
FROM d;

-- [27] NID: high-hazard dams (not associated structures), rated Poor or Unsatisfactory, by owner type and by state (grouping sets)
WITH h AS (
  SELECT *, CONDITION_ASSESSMENT IN ('Poor', 'Unsatisfactory') bad,
    COALESCE(CONDITION_ASSESSMENT, '') IN ('Not Rated', 'Not Available', '') unrated,
    LAST_INSPECTION_DATE IS NULL OR LAST_INSPECTION_DATE < '2021-09-24' insp_5y,
    TRY_TO_NUMBER(INSPECTION_FREQUENCY) freq
  FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_NID_DAMS
  WHERE HAZARD_POTENTIAL = 'High' AND NOT COALESCE(IS_ASSOCIATED_STRUCTURE, FALSE)
)
SELECT PRIMARY_OWNER_TYPE, STATE, COUNT(*) high_hazard, COUNT_IF(bad) poor_unsat, ROUND(100 * COUNT_IF(bad) / COUNT(*), 1) pct_bad,
  ROUND(100 * COUNT_IF(unrated) / COUNT(*), 1) pct_unrated,
  COUNT_IF(bad AND insp_5y) bad_insp_5y_or_none,
  COUNT_IF(bad AND freq > 0 AND LAST_INSPECTION_DATE IS NOT NULL AND DATEADD('year', freq, LAST_INSPECTION_DATE) < '2026-09-24') bad_overdue_own_schedule,
  COUNT_IF(bad AND NOT COALESCE(HAS_EMERGENCY_ACTION_PLAN, FALSE)) bad_no_eap,
  ROUND(MEDIAN(IFF(bad AND LAST_INSPECTION_DATE > '1950-01-01', DATEDIFF('day', LAST_INSPECTION_DATE, '2026-09-24') / 365.25, NULL)), 1) bad_med_yrs_since_insp
FROM h
GROUP BY GROUPING SETS ((PRIMARY_OWNER_TYPE), (STATE))
QUALIFY STATE IS NULL OR ROW_NUMBER() OVER (PARTITION BY STATE IS NULL ORDER BY COUNT_IF(bad) DESC) <= 20
ORDER BY STATE NULLS FIRST, poor_unsat DESC;

-- [28] NID: top owners of high-hazard Poor/Unsatisfactory dams
SELECT OWNER_NAMES, ANY_VALUE(PRIMARY_OWNER_TYPE) owner_type, COUNT(*) dams, COUNT_IF(CONDITION_ASSESSMENT = 'Unsatisfactory') unsat,
  LISTAGG(DISTINCT STATE, ',') states,
  COUNT_IF(NOT COALESCE(HAS_EMERGENCY_ACTION_PLAN, FALSE)) no_eap, COUNT_IF(LAST_INSPECTION_DATE IS NULL OR LAST_INSPECTION_DATE < '2021-09-24') insp_5y_or_none,
  MIN(LAST_INSPECTION_DATE) oldest_insp, ROUND(SUM(NID_STORAGE_ACRE_FT)) storage_af
FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_NID_DAMS
WHERE HAZARD_POTENTIAL = 'High' AND CONDITION_ASSESSMENT IN ('Poor', 'Unsatisfactory') AND NOT COALESCE(IS_ASSOCIATED_STRUCTURE, FALSE)
GROUP BY 1 ORDER BY dams DESC LIMIT 25;

-- [29] NID: high-hazard Unsatisfactory dams, largest by storage, named
SELECT NID_ID, DAM_NAME, OWNER_NAMES, PRIMARY_OWNER_TYPE, STATE, COUNTY, CITY, YEAR_COMPLETED, NID_HEIGHT_FT, NID_STORAGE_ACRE_FT,
  LAST_INSPECTION_DATE, INSPECTION_FREQUENCY, HAS_EMERGENCY_ACTION_PLAN, OPERATIONAL_STATUS, CONDITION_ASSESSMENT_DATE, DATA_LAST_UPDATED
FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_NID_DAMS
WHERE HAZARD_POTENTIAL = 'High' AND CONDITION_ASSESSMENT = 'Unsatisfactory' AND NOT COALESCE(IS_ASSOCIATED_STRUCTURE, FALSE)
ORDER BY NID_STORAGE_ACRE_FT DESC NULLS LAST LIMIT 25;

-- [30] LCR lead: active community systems of 10K+ people whose latest 90th-percentile lead (period ending 2024+) is over 0.015 mg/L
WITH pb AS (
  SELECT PWSID, SAMPLING_END_DATE e, MAX(SAMPLE_MEASURE) v
  FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_LCR_SAMPLES
  WHERE CONTAMINANT_CODE = 'PB90' AND SAMPLING_END_DATE BETWEEN '2015-01-01' AND '2026-09-24'
  GROUP BY 1, 2
), per AS (
  SELECT PWSID, COUNT(*) periods, COUNT_IF(v > 0.015 AND v <= 1) over_periods, MAX_BY(v, e) latest_v, MAX(e) latest_e
  FROM pb GROUP BY 1
), pws AS (
  SELECT PWSID, ANY_VALUE(PWS_NAME) pws_name, ANY_VALUE(STATE_CODE) st, MAX(POPULATION_SERVED_COUNT) pop, ANY_VALUE(PWS_TYPE_CODE) typ, ANY_VALUE(PWS_ACTIVITY_CODE) act
  FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS GROUP BY 1
)
SELECT per.PWSID, pws.pws_name, pws.st, pws.pop, per.latest_e, per.latest_v, per.over_periods, per.periods,
  COUNT(*) OVER () n_systems, SUM(pws.pop) OVER () pop_total
FROM per JOIN pws ON pws.PWSID = per.PWSID
WHERE pws.act = 'A' AND pws.typ = 'CWS' AND pws.pop >= 10000 AND per.latest_e >= '2024-01-01' AND per.latest_v > 0.015 AND per.latest_v <= 1
ORDER BY pws.pop DESC;

-- [31] VIOL: community systems with a health-based violation Unaddressed for 2+ years (begun 2015 to 2024-09-24), excluding code 5200, top 30 by population
WITH v AS (
  SELECT PWSID, VIOLATION_ID, ANY_VALUE(VIOLATION_STATUS) status, ANY_VALUE(CONTAMINANT_CODE) contam, ANY_VALUE(VIOLATION_CATEGORY_CODE) cat,
    MIN(COMPL_PER_BEGIN_DATE) b, COUNT_IF(ENF_ACTION_CATEGORY = 'Formal') n_formal, COUNT_IF(ENF_ACTION_CATEGORY = 'Informal') n_informal
  FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT
  WHERE IS_HEALTH_BASED_IND = 'Y' AND VIOLATION_ID IS NOT NULL AND COMPL_PER_BEGIN_DATE BETWEEN '2015-01-01' AND '2024-09-24'
    AND CONTAMINANT_CODE <> '5200'
  GROUP BY 1, 2 HAVING ANY_VALUE(VIOLATION_STATUS) = 'Unaddressed'
), pws AS (
  SELECT PWSID, ANY_VALUE(PWS_NAME) pws_name, ANY_VALUE(STATE_CODE) st, ANY_VALUE(PRIMACY_AGENCY_CODE) prim, MAX(POPULATION_SERVED_COUNT) pop,
    ANY_VALUE(PWS_TYPE_CODE) typ, ANY_VALUE(PWS_ACTIVITY_CODE) act
  FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS GROUP BY 1
), sys AS (
  SELECT PWSID, COUNT(*) unaddr_2y, MIN(b) oldest, LISTAGG(DISTINCT contam || '/' || cat, ',') codes, SUM(n_formal) formal, SUM(n_informal) informal
  FROM v GROUP BY 1
)
SELECT sys.*, pws.pws_name, pws.st, pws.prim, pws.pop,
  COUNT(*) OVER () n_cws, SUM(pws.pop) OVER () pop_total
FROM sys JOIN pws ON pws.PWSID = sys.PWSID
WHERE pws.typ = 'CWS' AND pws.act = 'A'
ORDER BY pws.pop DESC LIMIT 30;

-- [32] NID boring test: are stale inspection dates only on bad dams, or on every high-hazard dam in the state (reporting lag)?
SELECT COALESCE(STATE, 'ALL') st,
  COUNT_IF(CONDITION_ASSESSMENT IN ('Satisfactory', 'Fair')) good_n,
  ROUND(MEDIAN(IFF(CONDITION_ASSESSMENT IN ('Satisfactory', 'Fair') AND LAST_INSPECTION_DATE > '1950-01-01', DATEDIFF('day', LAST_INSPECTION_DATE, '2026-09-24') / 365.25, NULL)), 1) good_med_yrs,
  COUNT_IF(CONDITION_ASSESSMENT IN ('Poor', 'Unsatisfactory')) bad_n,
  ROUND(MEDIAN(IFF(CONDITION_ASSESSMENT IN ('Poor', 'Unsatisfactory') AND LAST_INSPECTION_DATE > '1950-01-01', DATEDIFF('day', LAST_INSPECTION_DATE, '2026-09-24') / 365.25, NULL)), 1) bad_med_yrs,
  MAX(DATA_LAST_UPDATED) newest_record_update, MEDIAN(DATEDIFF('day', DATA_LAST_UPDATED, '2026-09-24')) med_days_since_record_update
FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_NID_DAMS
WHERE HAZARD_POTENTIAL = 'High' AND NOT COALESCE(IS_ASSOCIATED_STRUCTURE, FALSE)
GROUP BY GROUPING SETS ((STATE), ())
HAVING GROUPING(STATE) = 1 OR STATE IN ('Georgia', 'Indiana', 'Pennsylvania', 'Kentucky', 'New Mexico', 'Hawaii', 'Mississippi')
ORDER BY st;

-- [33] NID: BIA high-hazard dams rated Poor/Unsatisfactory, worst first
SELECT NID_ID, DAM_NAME, STATE, COUNTY, CONDITION_ASSESSMENT, YEAR_COMPLETED, NID_HEIGHT_FT, NID_STORAGE_ACRE_FT, LAST_INSPECTION_DATE,
  INSPECTION_FREQUENCY, HAS_EMERGENCY_ACTION_PLAN, OPERATIONAL_STATUS, COUNT(*) OVER () n
FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_NID_DAMS
WHERE HAZARD_POTENTIAL = 'High' AND CONDITION_ASSESSMENT IN ('Poor', 'Unsatisfactory') AND NOT COALESCE(IS_ASSOCIATED_STRUCTURE, FALSE)
  AND OWNER_NAMES = 'BIA'
ORDER BY CONDITION_ASSESSMENT DESC, LAST_INSPECTION_DATE NULLS FIRST LIMIT 30;

-- [34] VIOL label check: on health-based violations begun 2015+, what enforcement categories and action codes sit on the rows, EPA-run tribal/WY/AK vs everyone else
SELECT CASE WHEN LEFT(PWSID, 2) IN ('06', '08', '09', '10') THEN 'EPA tribal region' WHEN LEFT(PWSID, 2) IN ('WY', 'AK') THEN LEFT(PWSID, 2) ELSE 'other' END grp,
  COALESCE(ENF_ACTION_CATEGORY, IFF(ENFORCEMENT_ID IS NULL, '(no enforcement row)', '(id but no category)')) category,
  COUNT(*) n_rows, APPROX_COUNT_DISTINCT(PWSID || '|' || VIOLATION_ID) viol_keys,
  ARRAY_SLICE(ARRAY_AGG(DISTINCT ENFORCEMENT_ACTION_TYPE_CODE), 0, 12) codes
FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT
WHERE IS_HEALTH_BASED_IND = 'Y' AND VIOLATION_ID IS NOT NULL AND COMPL_PER_BEGIN_DATE BETWEEN '2015-01-01' AND '2026-09-24'
GROUP BY 1, 2 ORDER BY 1, n_rows DESC;

-- [35] NID label check: emergency-plan flag values (TRUE / FALSE / NULL) on high-hazard Poor/Unsatisfactory dams, and whether a plan revision date sits on "no plan" rows
SELECT COALESCE(STATE, 'ALL') st, COUNT(*) bad_dams, COUNT_IF(HAS_EMERGENCY_ACTION_PLAN) eap_true, COUNT_IF(NOT HAS_EMERGENCY_ACTION_PLAN) eap_false,
  COUNT_IF(HAS_EMERGENCY_ACTION_PLAN IS NULL) eap_null, COUNT_IF(NOT COALESCE(HAS_EMERGENCY_ACTION_PLAN, FALSE) AND EAP_LAST_REVISION_DATE IS NOT NULL) no_plan_but_revision_date
FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_NID_DAMS
WHERE HAZARD_POTENTIAL = 'High' AND CONDITION_ASSESSMENT IN ('Poor', 'Unsatisfactory') AND NOT COALESCE(IS_ASSOCIATED_STRUCTURE, FALSE)
GROUP BY GROUPING SETS ((STATE), ())
HAVING GROUPING(STATE) = 1 OR COUNT_IF(NOT COALESCE(HAS_EMERGENCY_ACTION_PLAN, FALSE)) >= 30
ORDER BY bad_dams DESC;

-- note: [19] failed at compile (GROUP BY error) and returned nothing; it still counts toward the 35. Rerun as [24].
-- total statements sent: 35 (plus the two session settings per connection).
