-- S01 FISS + order/refer: row counts, NPI shape, blanks, overlap between the two lists, landing table load dates
WITH f AS (SELECT npi, last_name, first_name FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FISCAL_INTERMEDIARY_SHARED_SYSTEM_ATTENDING_AND_RENDERING),
o AS (SELECT npi, last_name, first_name FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_ORDER_AND_REFERRING),
fd AS (SELECT DISTINCT npi FROM f),
od AS (SELECT DISTINCT npi FROM o)
SELECT
 (SELECT COUNT(*) FROM f) f_rows,
 (SELECT COUNT(DISTINCT npi) FROM f) f_npi,
 (SELECT COUNT_IF(NOT REGEXP_LIKE(npi, '[12][0-9]{9}')) FROM f) f_bad_npi,
 (SELECT COUNT_IF(last_name IS NULL OR TRIM(last_name) = '') FROM f) f_blank_last,
 (SELECT COUNT_IF(first_name IS NULL OR TRIM(first_name) = '') FROM f) f_blank_first,
 (SELECT COUNT(*) FROM o) o_rows,
 (SELECT COUNT(DISTINCT npi) FROM o) o_npi,
 (SELECT COUNT_IF(NOT REGEXP_LIKE(npi, '[12][0-9]{9}')) FROM o) o_bad_npi,
 (SELECT COUNT_IF(first_name IS NULL OR TRIM(first_name) = '') FROM o) o_blank_first,
 (SELECT COUNT(*) FROM fd JOIN od ON fd.npi = od.npi) both_npi,
 (SELECT COUNT(*) FROM fd LEFT JOIN od ON fd.npi = od.npi WHERE od.npi IS NULL) f_only,
 (SELECT COUNT(*) FROM od LEFT JOIN fd ON fd.npi = od.npi WHERE fd.npi IS NULL) o_only,
 (SELECT ARRAY_AGG(OBJECT_CONSTRUCT('t', table_name, 'created', created, 'altered', last_altered, 'rows', row_count))
    FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES
   WHERE table_schema = 'LANDING'
     AND table_name IN ('FED_CMS_FISCAL_INTERMEDIARY_SHARED_SYSTEM_ATTENDING_AND_RENDERING', 'FED_CMS_ORDER_AND_REFERRING',
                        'FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS', 'FED_CMS_FEDERALLY_QUALIFIED_HEALTH_CENTER_ENROLLMENTS',
                        'FED_HHS_OIG_LEIE', 'FED_CMS_NURSING_HOME', 'FED_CMS_NURSING_HOME_DEFICIENCIES', 'FED_HRSA_UDS_SERVICE_DELIVERY_SITES',
                        'FED_CMS_NPPES')) load_dates;

-- S02 order/refer: every Y/N combination across the five service flags, plus the duplicated NPIs in both lists
SELECT 'combo' kind, partb || dme || hha || pmd || hospice k, COUNT(*) n, NULL nm
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_ORDER_AND_REFERRING GROUP BY 2
UNION ALL
SELECT 'dup_O', npi, COUNT(*), LISTAGG(last_name || ',' || first_name || ',' || partb || dme || hha || pmd || hospice, ' / ')
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_ORDER_AND_REFERRING GROUP BY npi HAVING COUNT(*) > 1
UNION ALL
SELECT 'dup_F', npi, COUNT(*), LISTAGG(last_name || ',' || first_name, ' / ')
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FISCAL_INTERMEDIARY_SHARED_SYSTEM_ATTENDING_AND_RENDERING GROUP BY npi HAVING COUNT(*) > 1
ORDER BY kind, n DESC;

-- S03 SNF and FQHC enrollments: profile side by side (flags, blanks, sentinels, repeats, enrollment date parsed from the ID)
WITH x AS (
  SELECT 'SNF' t, enrollment_id, npi, ccn, associate_id, multiple_npi_flag, proprietary_nonprofit, organization_type_structure,
         incorporation_date, affiliation_entity_id, organization_name, address_line_1, zip_code,
         TRY_TO_DATE(SUBSTR(enrollment_id, 2, 8), 'YYYYMMDD') enr_date
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS
  UNION ALL
  SELECT 'FQHC', enrollment_id, npi, ccn, associate_id, multiple_npi_flag, proprietary_nonprofit, organization_type_structure,
         incorporation_date, NULL, organization_name, address_line_1, zip_code,
         TRY_TO_DATE(SUBSTR(enrollment_id, 2, 8), 'YYYYMMDD')
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FEDERALLY_QUALIFIED_HEALTH_CENTER_ENROLLMENTS
)
SELECT t, COUNT(*) n, COUNT(DISTINCT enrollment_id) enr, COUNT(DISTINCT npi) npis, COUNT(DISTINCT ccn) ccns,
       COUNT_IF(ccn IS NULL OR TRIM(ccn) = '') ccn_blank, COUNT(DISTINCT associate_id) assoc,
       COUNT_IF(npi IS NULL OR NOT REGEXP_LIKE(npi, '[12][0-9]{9}')) bad_npi,
       ARRAY_AGG(DISTINCT multiple_npi_flag) mflag_vals, COUNT_IF(multiple_npi_flag = 'Y') mflag_y,
       ARRAY_AGG(DISTINCT proprietary_nonprofit) pn_vals, COUNT_IF(proprietary_nonprofit = 'P') pn_p, COUNT_IF(proprietary_nonprofit = 'N') pn_n,
       ARRAY_AGG(DISTINCT organization_type_structure) ots,
       COUNT_IF(incorporation_date IS NULL) inc_null, COUNT_IF(incorporation_date < '1900-01-01') inc_pre1900,
       MIN(incorporation_date) inc_min, MAX(incorporation_date) inc_max,
       COUNT_IF(incorporation_date >= '2022-01-01') inc_2022p,
       COUNT_IF(affiliation_entity_id IS NULL OR TRIM(affiliation_entity_id) = '') aff_blank, COUNT(DISTINCT affiliation_entity_id) affs,
       MIN(enr_date) enr_min, MAX(enr_date) enr_max, COUNT_IF(enr_date IS NULL) enr_unparsed,
       COUNT(DISTINCT UPPER(address_line_1) || LEFT(zip_code, 5)) addrs
FROM x GROUP BY t;

-- S04 SNF and FQHC: NPIs, CCNs and addresses that repeat across enrollments (top 12 each), to see what the 107 and 82 are
WITH x AS (
  SELECT 'SNF' t, enrollment_id, npi, ccn, associate_id, multiple_npi_flag, organization_name, enrollment_state, address_line_1, zip_code
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS
  UNION ALL
  SELECT 'FQHC', enrollment_id, npi, ccn, associate_id, multiple_npi_flag, organization_name, enrollment_state, address_line_1, zip_code
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FEDERALLY_QUALIFIED_HEALTH_CENTER_ENROLLMENTS
), g AS (
  SELECT t, 'npi' k, npi v, COUNT(*) n, COUNT(DISTINCT ccn) ccns, COUNT(DISTINCT associate_id) assocs, COUNT(DISTINCT organization_name) orgs,
         COUNT(DISTINCT enrollment_state) states, ANY_VALUE(organization_name) an_org, ARRAY_AGG(DISTINCT multiple_npi_flag) mf,
         ROW_NUMBER() OVER (PARTITION BY t ORDER BY COUNT(*) DESC) rk
  FROM x GROUP BY t, npi HAVING COUNT(*) > 1
  UNION ALL
  SELECT t, 'ccn', ccn, COUNT(*), COUNT(DISTINCT ccn), COUNT(DISTINCT associate_id), COUNT(DISTINCT organization_name),
         COUNT(DISTINCT enrollment_state), ANY_VALUE(organization_name), ARRAY_AGG(DISTINCT multiple_npi_flag),
         ROW_NUMBER() OVER (PARTITION BY t ORDER BY COUNT(*) DESC)
  FROM x WHERE ccn IS NOT NULL AND TRIM(ccn) <> '' GROUP BY t, ccn HAVING COUNT(*) > 1
)
, g2 AS (SELECT g.*, COUNT(*) OVER (PARTITION BY t, k) groups_repeating, SUM(n) OVER (PARTITION BY t, k) rows_in_repeats FROM g)
SELECT * FROM g2 WHERE rk <= 12 ORDER BY t, k, n DESC;

-- S05 CDC leading causes: completeness of year x state x cause, and US row vs sum of states per cause in 1999 and 2017, and state spread in 2017
WITH c AS (SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_LEADING_CAUSES_STATE),
agg AS (
  SELECT cause_name, year,
         SUM(IFF(state = 'United States', deaths, 0)) us_deaths,
         SUM(IFF(state <> 'United States', deaths, 0)) states_deaths,
         MAX(IFF(state = 'United States', age_adjusted_death_rate, NULL)) us_rate,
         MIN(IFF(state <> 'United States', age_adjusted_death_rate, NULL)) min_rate,
         MAX(IFF(state <> 'United States', age_adjusted_death_rate, NULL)) max_rate,
         STDDEV(IFF(state <> 'United States', age_adjusted_death_rate, NULL)) / AVG(IFF(state <> 'United States', age_adjusted_death_rate, NULL)) cv,
         COUNT(*) rows_
  FROM c WHERE year IN (1999, 2017) GROUP BY 1, 2
)
SELECT 'meta' kind, NULL cause_name, NULL year,
       (SELECT COUNT(*) FROM c) a, (SELECT COUNT(DISTINCT year, state, cause_name) FROM c) b,
       (SELECT COUNT(DISTINCT state) FROM c) cc, (SELECT COUNT(DISTINCT year) FROM c) d,
       (SELECT COUNT_IF(deaths IS NULL OR age_adjusted_death_rate IS NULL) FROM c) e,
       (SELECT MIN(year) FROM c) f, (SELECT MAX(year) FROM c) g, NULL h
UNION ALL
SELECT 'cause', cause_name, year, us_deaths, states_deaths, us_rate, min_rate, max_rate, ROUND(cv, 3), rows_, NULL
FROM agg
ORDER BY kind DESC, cause_name, year;
