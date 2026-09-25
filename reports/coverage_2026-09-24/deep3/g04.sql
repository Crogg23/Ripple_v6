-- deep3/g04: deep pass 3, 2026-09-24. Python door (connect/db.py), QUERY_TAG 'deep3-2026-09-24'.
-- Every connection first ran: ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300, then ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'. Not counted.
-- Read-only: every statement below is a single SELECT or WITH. Runner: reports/coverage_2026-09-24/deep3/g04/run.py (refuses anything else).
-- 30 statements sent, S01-S30. S23 failed to compile (unsupported subquery) and was rewritten as S26. Results: g04/out_Sxx.json.
-- Tables: FISCAL_INTERMEDIARY_SHARED_SYSTEM_ATTENDING_AND_RENDERING (FISS), ORDER_AND_REFERRING (O&R),
--         SKILLED_NURSING_FACILITY_ENROLLMENTS (SNF), CDC_LEADING_CAUSES_STATE (CDC), FEDERALLY_QUALIFIED_HEALTH_CENTER_ENROLLMENTS (FQHC).
-- Join partners read: FED_HHS_OIG_LEIE, FED_CMS_NPPES, FED_CMS_PECOS_PROVIDER_ENROLLMENT, FED_CMS_OPT_OUT_AFFIDAVITS,
--         FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER (DY2024), FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_REFER (DY2024),
--         FED_CMS_NURSING_HOME, FED_CMS_NURSING_HOME_DEFICIENCIES, FED_HRSA_UDS_SERVICE_DELIVERY_SITES, LIBRARY_RAW.INFORMATION_SCHEMA.TABLES.


-- ===== batch b1 =====
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

-- ===== batch b2 =====
-- S06 SNF and FQHC by enrollment year (date parsed from the enrollment ID): count, share with no incorporation date, for-profit share, LLC share
WITH x AS (
  SELECT 'SNF' t, TRY_TO_DATE(SUBSTR(enrollment_id, 2, 8), 'YYYYMMDD') enr, incorporation_date inc, proprietary_nonprofit pn, organization_type_structure ots
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS
  UNION ALL
  SELECT 'FQHC', TRY_TO_DATE(SUBSTR(enrollment_id, 2, 8), 'YYYYMMDD'), incorporation_date, proprietary_nonprofit, organization_type_structure
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FEDERALLY_QUALIFIED_HEALTH_CENTER_ENROLLMENTS
)
SELECT t, YEAR(enr) enr_year, COUNT(*) n, COUNT_IF(inc IS NULL) inc_null, ROUND(COUNT_IF(inc IS NULL) / COUNT(*), 3) inc_null_share,
       COUNT_IF(pn = 'P') for_profit, COUNT_IF(ots = 'LLC') llc, MAX(inc) inc_max,
       COUNT_IF(inc IS NOT NULL AND inc > enr) inc_after_enr
FROM x GROUP BY 1, 2 ORDER BY 1, 2;

-- S07 OIG exclusion list (LEIE, real NPIs only) joined to order/refer (O) and FISS attending (F); by how long ago the exclusion was, with name agreement; L rows are the LEIE denominator
WITH l AS (
  SELECT npi, UPPER(TRIM(last_name)) ln, UPPER(TRIM(first_name)) fn, exclusion_type, exclusion_date, has_waiver, was_reinstated, is_entity_not_individual
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE WHERE npi_is_real
),
o AS (SELECT npi, UPPER(TRIM(last_name)) ln, UPPER(TRIM(first_name)) fn FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_ORDER_AND_REFERRING),
f AS (SELECT npi, UPPER(TRIM(last_name)) ln, UPPER(TRIM(first_name)) fn FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FISCAL_INTERMEDIARY_SHARED_SYSTEM_ATTENDING_AND_RENDERING),
m AS (
  SELECT 'L' lst, l.*, l.ln lln, l.fn lfn FROM l
  UNION ALL SELECT 'O', l.*, o.ln, o.fn FROM l JOIN o ON o.npi = l.npi
  UNION ALL SELECT 'F', l.*, f.ln, f.fn FROM l JOIN f ON f.npi = l.npi
)
SELECT lst,
  CASE WHEN exclusion_date >= '2026-05-01' THEN 'a_2026-05+'
       WHEN exclusion_date >= '2025-08-01' THEN 'b_3-12mo'
       WHEN exclusion_date >= '2023-08-01' THEN 'c_1-3y'
       WHEN exclusion_date >= '2016-08-01' THEN 'd_3-10y'
       WHEN exclusion_date IS NULL THEN 'z_nodate'
       ELSE 'e_10y+' END age,
  COUNT(*) rows_, COUNT(DISTINCT npi) npis,
  COUNT_IF(ln = lln) last_agrees, COUNT_IF(fn = lfn) first_agrees, COUNT_IF(ln = lln OR fn = lfn) either_agrees,
  COUNT_IF(has_waiver) waiver, COUNT_IF(was_reinstated) reinst, COUNT_IF(is_entity_not_individual) entity
FROM m GROUP BY 1, 2 ORDER BY 1, 2;

-- S08 LEIE hits on order/refer: every excluded person whose exclusion is 3+ months older than the list load, name agreeing, no waiver (eyeball + types)
WITH l AS (
  SELECT npi, UPPER(TRIM(last_name)) ln, UPPER(TRIM(first_name)) fn, exclusion_type, exclusion_date, specialty, general_category, state, city,
         has_waiver, was_reinstated, reinstatement_date
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE WHERE npi_is_real
),
o AS (SELECT npi, UPPER(TRIM(last_name)) ln, UPPER(TRIM(first_name)) fn, partb || dme || hha || pmd || hospice flags FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_ORDER_AND_REFERRING),
f AS (SELECT DISTINCT npi FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FISCAL_INTERMEDIARY_SHARED_SYSTEM_ATTENDING_AND_RENDERING)
SELECT l.npi, l.ln, l.fn, o.ln o_ln, o.fn o_fn, l.exclusion_type, l.exclusion_date, l.specialty, l.general_category, l.state, l.city,
       o.flags, IFF(f.npi IS NOT NULL, 'Y', 'N') on_fiss, l.has_waiver, l.reinstatement_date
FROM l JOIN o ON o.npi = l.npi LEFT JOIN f ON f.npi = l.npi
WHERE l.exclusion_date < '2026-05-01' AND (l.ln = o.ln OR l.fn = o.fn)
ORDER BY l.exclusion_date;

-- S09 NPPES deactivated NPIs on the order/refer (O) and FISS (F) lists, by deactivation year; plus how many list NPIs are missing from NPPES entirely
WITH d AS (
  SELECT npi, npi_deactivation_date dd, npi_reactivation_date rd, npi_deactivation_reason_code rc, entity_type_code et,
         provider_last_name_legal_name ln
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES
),
o AS (SELECT DISTINCT npi FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_ORDER_AND_REFERRING),
f AS (SELECT DISTINCT npi FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FISCAL_INTERMEDIARY_SHARED_SYSTEM_ATTENDING_AND_RENDERING),
j AS (
  SELECT 'O' lst, o.npi, d.npi dnpi, d.dd, d.rd, d.rc, d.ln FROM o LEFT JOIN d ON d.npi = o.npi
  UNION ALL
  SELECT 'F', f.npi, d.npi, d.dd, d.rd, d.rc, d.ln FROM f LEFT JOIN d ON d.npi = f.npi
  UNION ALL
  SELECT 'N', d.npi, d.npi, d.dd, d.rd, d.rc, d.ln FROM d WHERE d.dd IS NOT NULL
)
SELECT lst,
       CASE WHEN dnpi IS NULL THEN 'not_in_nppes' WHEN dd IS NULL THEN 'active'
            WHEN rd IS NOT NULL AND rd >= dd THEN 'reactivated' ELSE 'deact_' || YEAR(dd) END status,
       COUNT(*) n, ARRAY_AGG(DISTINCT rc) reason_codes, COUNT_IF(ln IS NULL OR ln = '') blank_name, MIN(dd) dmin, MAX(dd) dmax
FROM j GROUP BY 1, 2 ORDER BY 1, 2;

-- S10 FQHC for-profit vs nonprofit: HRSA health-center site list land rate by NPI and by CCN, by org type
WITH q AS (
  SELECT enrollment_id, npi, REGEXP_REPLACE(UPPER(ccn), '[^0-9A-Z]', '') ccn, proprietary_nonprofit pn, organization_type_structure ots, associate_id
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FEDERALLY_QUALIFIED_HEALTH_CENTER_ENROLLMENTS
),
hn AS (SELECT DISTINCT TRIM(fqhc_site_npi_number) v FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES WHERE fqhc_site_npi_number IS NOT NULL),
hc AS (SELECT DISTINCT REGEXP_REPLACE(UPPER(fqhc_site_medicare_billing_number), '[^0-9A-Z]', '') v FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES WHERE fqhc_site_medicare_billing_number IS NOT NULL)
SELECT pn, ots, COUNT(*) n, COUNT(DISTINCT associate_id) orgs,
       COUNT_IF(hn.v IS NOT NULL) npi_in_hrsa, COUNT_IF(hc.v IS NOT NULL) ccn_in_hrsa, COUNT_IF(hn.v IS NOT NULL OR hc.v IS NOT NULL) either_in_hrsa,
       (SELECT COUNT(*) FROM hn) hrsa_npis, (SELECT COUNT(*) FROM hc) hrsa_ccns
FROM q LEFT JOIN hn ON hn.v = q.npi LEFT JOIN hc ON hc.v = q.ccn
GROUP BY ROLLUP(pn, ots) ORDER BY pn, ots;

-- S11 FQHC for-profit enrollments, one row per organization: names, place, type, dates, HRSA match
WITH q AS (
  SELECT * , REGEXP_REPLACE(UPPER(ccn), '[^0-9A-Z]', '') ccn2, TRY_TO_DATE(SUBSTR(enrollment_id, 2, 8), 'YYYYMMDD') enr
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FEDERALLY_QUALIFIED_HEALTH_CENTER_ENROLLMENTS WHERE proprietary_nonprofit = 'P'
),
hn AS (SELECT DISTINCT TRIM(fqhc_site_npi_number) v FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES WHERE fqhc_site_npi_number IS NOT NULL),
hc AS (SELECT DISTINCT REGEXP_REPLACE(UPPER(fqhc_site_medicare_billing_number), '[^0-9A-Z]', '') v FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES WHERE fqhc_site_medicare_billing_number IS NOT NULL)
SELECT associate_id, ANY_VALUE(organization_name) org, ANY_VALUE(doing_business_as_name) dba, LISTAGG(DISTINCT enrollment_state, ',') states,
       LISTAGG(DISTINCT city, ',') cities, COUNT(*) enrollments, ANY_VALUE(organization_type_structure) ots, ANY_VALUE(organization_other_type_text) other_txt,
       MIN(incorporation_date) inc, MIN(enr) enr_first, MAX(enr) enr_last, COUNT_IF(hn.v IS NOT NULL) npi_hrsa, COUNT_IF(hc.v IS NOT NULL) ccn_hrsa,
       LISTAGG(DISTINCT ccn2, ',') ccns
FROM q LEFT JOIN hn ON hn.v = q.npi LEFT JOIN hc ON hc.v = q.ccn2
GROUP BY associate_id ORDER BY enrollments DESC, org;

-- S12 CDC: each state's 1999-to-2017 change in age-adjusted rate by cause, against the US change; top 3 risers and bottom 2 per cause, with the median state
WITH c AS (SELECT state, cause_name, year, age_adjusted_death_rate r, deaths FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_LEADING_CAUSES_STATE WHERE cause_name <> 'All causes'),
w AS (SELECT state, cause_name, MAX(IFF(year = 1999, r, NULL)) r99, MAX(IFF(year = 2017, r, NULL)) r17,
             MAX(IFF(year = 1999, deaths, NULL)) d99, MAX(IFF(year = 2017, deaths, NULL)) d17 FROM c GROUP BY 1, 2),
us AS (SELECT cause_name, r99 us99, r17 us17 FROM w WHERE state = 'United States'),
z AS (SELECT w.*, us.us99, us.us17, w.r17 / NULLIF(w.r99, 0) ratio,
             ROW_NUMBER() OVER (PARTITION BY w.cause_name ORDER BY w.r17 / NULLIF(w.r99, 0) DESC) up_rk,
             ROW_NUMBER() OVER (PARTITION BY w.cause_name ORDER BY w.r17 / NULLIF(w.r99, 0) ASC) dn_rk,
             MEDIAN(w.r17 / NULLIF(w.r99, 0)) OVER (PARTITION BY w.cause_name) med_ratio,
             COUNT_IF(w.r17 > w.r99) OVER (PARTITION BY w.cause_name) n_states_up
      FROM w JOIN us ON us.cause_name = w.cause_name WHERE w.state <> 'United States')
SELECT cause_name, state, r99, r17, d99, d17, ROUND(ratio, 2) ratio, ROUND(us17 / us99, 2) us_ratio, ROUND(med_ratio, 2) med_state_ratio, n_states_up, up_rk, dn_rk
FROM z WHERE up_rk <= 3 OR dn_rk <= 2 ORDER BY cause_name, up_rk;

-- S13 SNF enrollments joined to Care Compare nursing homes by CCN: by operator incorporation era, each home against its own state's average
WITH s AS (
  SELECT ccn s_ccn, incorporation_date inc, proprietary_nonprofit pn, affiliation_entity_id aff
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS
),
n AS (
  SELECT cms_certification_number_ccn n_ccn, state n_state, overall_rating rating,
         adjusted_total_nurse_staffing_hours_per_resident_per_day hprd,
         total_amount_of_fines_in_dollars fines, number_of_certified_beds beds, abuse_icon,
         IFF(special_focus_status IS NOT NULL AND TRIM(special_focus_status) <> '', 1, 0) sff,
         total_nursing_staff_turnover turnover,
         date_first_approved_to_provide_medicare_and_medicaid_services first_ok, processing_date
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME
),
st AS (SELECT n_state, AVG(rating) m_rating, AVG(hprd) m_hprd, AVG(fines / NULLIF(beds, 0)) m_fpb,
              AVG(IFF(abuse_icon = 'Y', 1, 0)) m_abuse, AVG(turnover) m_turn, AVG(sff) m_sff FROM n GROUP BY n_state),
j AS (
  SELECT s.*, n.*, st.m_rating, st.m_hprd, st.m_fpb, st.m_abuse, st.m_turn, st.m_sff,
         CASE WHEN s.inc IS NULL THEN 'z_null' WHEN s.inc < '1900-01-01' THEN 'y_sentinel'
              WHEN s.inc >= '2022-01-01' THEN 'a_2022+' WHEN s.inc >= '2018-01-01' THEN 'b_2018-21' ELSE 'c_pre2018' END grp
  FROM s LEFT JOIN n ON n.n_ccn = s.s_ccn LEFT JOIN st ON st.n_state = n.n_state
)
SELECT grp, COUNT(*) enr, COUNT(n_ccn) landed,
       ROUND(AVG(rating - m_rating), 3) d_rating_mean, ROUND(MEDIAN(rating - m_rating), 3) d_rating_med,
       ROUND(AVG(IFF(rating = 1, 1, 0)), 3) one_star_share,
       ROUND(AVG(hprd - m_hprd), 3) d_hprd_mean, ROUND(MEDIAN(hprd - m_hprd), 3) d_hprd_med,
       ROUND(AVG(fines / NULLIF(beds, 0) - m_fpb), 1) d_fines_per_bed, ROUND(MEDIAN(fines / NULLIF(beds, 0) - m_fpb), 1) d_fpb_med,
       ROUND(AVG(IFF(abuse_icon = 'Y', 1, 0) - m_abuse), 3) d_abuse, ROUND(AVG(sff - m_sff), 4) d_sff,
       ROUND(AVG(turnover - m_turn), 2) d_turnover,
       ROUND(AVG(IFF(pn = 'P', 1, 0)), 3) for_profit_share,
       COUNT_IF(first_ok < DATEADD(year, -1, inc)) home_older_than_operator,
       ARRAY_AGG(DISTINCT abuse_icon) abuse_vals, MAX(processing_date) nh_processing
FROM j GROUP BY grp ORDER BY grp;

-- ===== batch b3 =====
-- S14 carbon-date both lists: newest NPPES enumeration months on each list, and NPIs deactivated per month on each list vs all of NPPES (decay curve)
WITH n AS (SELECT npi, provider_enumeration_date ed, npi_deactivation_date dd, npi_reactivation_date rd FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES),
lists AS (
  SELECT DISTINCT 'O' lst, npi FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_ORDER_AND_REFERRING
  UNION ALL
  SELECT DISTINCT 'F', npi FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FISCAL_INTERMEDIARY_SHARED_SYSTEM_ATTENDING_AND_RENDERING
),
j AS (SELECT lists.lst, n.ed, n.dd, n.rd FROM lists JOIN n ON n.npi = lists.npi)
SELECT 'enum' kind, lst, TO_CHAR(DATE_TRUNC('month', ed), 'YYYY-MM') m, COUNT(*) n FROM j WHERE ed >= '2025-01-01' GROUP BY 1, 2, 3
UNION ALL
SELECT 'enum_max', lst, TO_CHAR(MAX(ed)), COUNT_IF(ed >= '2026-01-01') FROM j GROUP BY 1, 2
UNION ALL
SELECT 'deact', lst, TO_CHAR(DATE_TRUNC('month', dd), 'YYYY-MM'), COUNT(*) FROM j WHERE dd >= '2024-07-01' AND (rd IS NULL OR rd < dd) GROUP BY 1, 2, 3
UNION ALL
SELECT 'deact', 'NPPES', TO_CHAR(DATE_TRUNC('month', dd), 'YYYY-MM'), COUNT(*) FROM n WHERE dd >= '2024-07-01' AND (rd IS NULL OR rd < dd) GROUP BY 1, 2, 3
ORDER BY 1, 3, 2;

-- S15 order/refer NPIs by NPPES deactivation status: still on FISS, billed Part B in 2024 (name agreeing), referred DME in 2024, service flags
WITH n AS (
  SELECT npi, npi_deactivation_date dd FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES
  WHERE npi_deactivation_date IS NOT NULL AND (npi_reactivation_date IS NULL OR npi_reactivation_date < npi_deactivation_date)
),
o AS (SELECT npi, ANY_VALUE(UPPER(TRIM(last_name))) ln, ANY_VALUE(partb || dme || hha || pmd || hospice) flags
      FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_ORDER_AND_REFERRING GROUP BY npi),
f AS (SELECT DISTINCT npi FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FISCAL_INTERMEDIARY_SHARED_SYSTEM_ATTENDING_AND_RENDERING),
b AS (SELECT rndrng_npi npi, UPPER(TRIM(rndrng_prvdr_last_org_name)) bln, tot_mdcr_alowd_amt amt
      FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER),
r AS (SELECT rfrg_npi npi, suplr_mdcr_alowd_amt ramt FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_REFER),
j AS (
  SELECT o.*, n.dd,
         CASE WHEN n.npi IS NULL THEN 'a_not_deactivated' WHEN n.dd < '2025-01-01' THEN 'b_deact_pre2025'
              WHEN n.dd < '2026-02-01' THEN 'c_deact_2025-01_to_2026-01' ELSE 'd_deact_2026-02+' END grp,
         IFF(f.npi IS NULL, 0, 1) in_f, b.bln, b.amt, r.ramt
  FROM o LEFT JOIN n ON n.npi = o.npi LEFT JOIN f ON f.npi = o.npi LEFT JOIN b ON b.npi = o.npi LEFT JOIN r ON r.npi = o.npi
)
SELECT grp, COUNT(*) npis, SUM(in_f) in_fiss, COUNT(bln) in_partb24, COUNT_IF(bln = ln) partb_last_agrees,
       ROUND(SUM(amt)) partb24_allowed, COUNT(ramt) in_dme_ref24, ROUND(SUM(ramt)) dme_ref24_allowed,
       COUNT_IF(flags = 'YYYYY') all5, COUNT_IF(SUBSTR(flags, 3, 1) = 'Y') hha_y, COUNT_IF(SUBSTR(flags, 5, 1) = 'Y') hospice_y,
       MIN(dd) dmin, MAX(dd) dmax
FROM j GROUP BY grp ORDER BY grp;

-- S16 eyeball: order/refer NPIs deactivated 2025-01 to 2026-01 and gone from FISS; 10 by hash plus the 5 biggest DME referrers in 2024
WITH n AS (
  SELECT npi, npi_deactivation_date dd FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES
  WHERE npi_deactivation_date >= '2025-01-01' AND npi_deactivation_date < '2026-02-01'
    AND (npi_reactivation_date IS NULL OR npi_reactivation_date < npi_deactivation_date)
),
o AS (SELECT npi, last_name, first_name, partb || dme || hha || pmd || hospice flags FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_ORDER_AND_REFERRING),
f AS (SELECT DISTINCT npi FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FISCAL_INTERMEDIARY_SHARED_SYSTEM_ATTENDING_AND_RENDERING),
b AS (SELECT rndrng_npi npi, rndrng_prvdr_last_org_name bln, rndrng_prvdr_first_name bfn, rndrng_prvdr_city bcity, rndrng_prvdr_state_abrvtn bst,
             rndrng_prvdr_type btype, tot_benes FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER),
r AS (SELECT rfrg_npi npi, suplr_mdcr_alowd_amt ramt, tot_suplr_benes rbenes FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_REFER),
j AS (
  SELECT o.npi, o.last_name, o.first_name, o.flags, n.dd, b.bln, b.bfn, b.bcity, b.bst, b.btype, b.tot_benes, r.ramt, r.rbenes
  FROM o JOIN n ON n.npi = o.npi LEFT JOIN f ON f.npi = o.npi LEFT JOIN b ON b.npi = o.npi LEFT JOIN r ON r.npi = o.npi
  WHERE f.npi IS NULL
)
SELECT * FROM (SELECT 'hash' kind, j.* FROM j ORDER BY HASH(npi) LIMIT 10)
UNION ALL
SELECT * FROM (SELECT 'top_dme', j.* FROM j WHERE ramt IS NOT NULL ORDER BY ramt DESC LIMIT 5);

-- S17 SNF: operator incorporation era, for-profit homes only, each home against its state's for-profit average; split by chain membership; top chains in the 2022+ group
WITH s AS (
  SELECT ccn s_ccn, incorporation_date inc, NULLIF(TRIM(affiliation_entity_name), '') aff
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS
),
n AS (
  SELECT cms_certification_number_ccn n_ccn, state n_state, overall_rating rating, health_inspection_rating hir,
         adjusted_total_nurse_staffing_hours_per_resident_per_day hprd, total_nursing_staff_turnover turnover,
         total_amount_of_fines_in_dollars / NULLIF(number_of_certified_beds, 0) fpb, IFF(abuse_icon = 'Y', 1, 0) abuse
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME WHERE ownership_type ILIKE 'for profit%'
),
st AS (SELECT n_state, AVG(rating) m_rating, AVG(hir) m_hir, AVG(hprd) m_hprd, AVG(turnover) m_turn, AVG(fpb) m_fpb, AVG(abuse) m_abuse FROM n GROUP BY n_state),
j AS (
  SELECT s.*, n.*, st.m_rating, st.m_hir, st.m_hprd, st.m_turn, st.m_fpb, st.m_abuse,
         CASE WHEN s.inc IS NULL THEN 'z_null' WHEN s.inc < '1900-01-01' THEN 'y_sentinel'
              WHEN s.inc >= '2022-01-01' THEN 'a_2022+' WHEN s.inc >= '2018-01-01' THEN 'b_2018-21' ELSE 'c_pre2018' END grp
  FROM s JOIN n ON n.n_ccn = s.s_ccn JOIN st ON st.n_state = n.n_state
)
SELECT 'grp' kind, grp, IFF(aff IS NULL, 'no_chain', 'chain') sub, COUNT(*) homes,
       ROUND(AVG(rating - m_rating), 3) d_rating, ROUND(MEDIAN(rating - m_rating), 2) d_rating_med,
       ROUND(AVG(hir - m_hir), 3) d_inspection, ROUND(AVG(hprd - m_hprd), 3) d_hprd, ROUND(MEDIAN(hprd - m_hprd), 3) d_hprd_med,
       ROUND(AVG(turnover - m_turn), 2) d_turnover, ROUND(AVG(fpb - m_fpb), 1) d_fines_per_bed, ROUND(AVG(abuse - m_abuse), 3) d_abuse,
       ROUND(AVG(IFF(rating = 1, 1, 0)), 3) one_star
FROM j GROUP BY ROLLUP(grp, IFF(aff IS NULL, 'no_chain', 'chain'))
UNION ALL
SELECT * FROM (
  SELECT 'chain_2022+', grp, aff, COUNT(*), ROUND(AVG(rating - m_rating), 3), ROUND(MEDIAN(rating - m_rating), 2), ROUND(AVG(hir - m_hir), 3),
         ROUND(AVG(hprd - m_hprd), 3), ROUND(MEDIAN(hprd - m_hprd), 3), ROUND(AVG(turnover - m_turn), 2), ROUND(AVG(fpb - m_fpb), 1),
         ROUND(AVG(abuse - m_abuse), 3), ROUND(AVG(IFF(rating = 1, 1, 0)), 3)
  FROM j WHERE grp = 'a_2022+' AND aff IS NOT NULL GROUP BY grp, aff ORDER BY COUNT(*) DESC LIMIT 12
)
ORDER BY kind DESC, grp, sub;

-- S18 SNF before/after test: for-profit homes whose operator company formed 2022+, health citations per year in up to 2 years before vs after that date, against same-state stable for-profit homes (operator formed pre-2018) over the same calendar windows
WITH d AS (
  SELECT cms_certification_number_ccn ccn, survey_date sd, UPPER(TRIM(scope_severity_code)) ss
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES
),
rng AS (SELECT MIN(sd) d0, MAX(sd) d1, ARRAY_AGG(DISTINCT ss) ss_vals FROM d),
nh AS (SELECT cms_certification_number_ccn ccn, state FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME WHERE ownership_type ILIKE 'for profit%'),
s AS (SELECT ccn, incorporation_date inc FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS),
t AS (
  SELECT s.ccn, nh.state, s.inc,
         GREATEST(DATEADD(day, -730, s.inc), rng.d0) b0, s.inc b1, LEAST(DATEADD(day, 730, s.inc), rng.d1) a1
  FROM s JOIN nh ON nh.ccn = s.ccn CROSS JOIN rng
  WHERE s.inc >= '2022-01-01' AND DATEDIFF(day, rng.d0, s.inc) >= 365 AND DATEDIFF(day, s.inc, rng.d1) >= 365
),
p AS (SELECT s.ccn, nh.state FROM s JOIN nh ON nh.ccn = s.ccn WHERE s.inc >= '1900-01-01' AND s.inc < '2018-01-01'),
pn AS (SELECT state, COUNT(*) n_peer FROM p GROUP BY state),
pd AS (SELECT p.state, d.sd, COUNT(*) n_all, COUNT_IF(d.ss >= 'G') n_harm FROM d JOIN p ON p.ccn = d.ccn GROUP BY 1, 2),
td AS (
  SELECT t.ccn,
         COUNT_IF(d.sd >= t.b0 AND d.sd < t.b1) tb_all, COUNT_IF(d.sd >= t.b0 AND d.sd < t.b1 AND d.ss >= 'G') tb_harm,
         COUNT_IF(d.sd >= t.b1 AND d.sd <= t.a1) ta_all, COUNT_IF(d.sd >= t.b1 AND d.sd <= t.a1 AND d.ss >= 'G') ta_harm
  FROM t LEFT JOIN d ON d.ccn = t.ccn GROUP BY t.ccn
),
tp AS (
  SELECT t.ccn,
         SUM(IFF(pd.sd >= t.b0 AND pd.sd < t.b1, pd.n_all, 0)) / ANY_VALUE(pn.n_peer) pb_all,
         SUM(IFF(pd.sd >= t.b0 AND pd.sd < t.b1, pd.n_harm, 0)) / ANY_VALUE(pn.n_peer) pb_harm,
         SUM(IFF(pd.sd >= t.b1 AND pd.sd <= t.a1, pd.n_all, 0)) / ANY_VALUE(pn.n_peer) pa_all,
         SUM(IFF(pd.sd >= t.b1 AND pd.sd <= t.a1, pd.n_harm, 0)) / ANY_VALUE(pn.n_peer) pa_harm
  FROM t JOIN pd ON pd.state = t.state JOIN pn ON pn.state = t.state GROUP BY t.ccn
),
x AS (
  SELECT t.*, td.tb_all, td.tb_harm, td.ta_all, td.ta_harm, tp.pb_all, tp.pb_harm, tp.pa_all, tp.pa_harm,
         DATEDIFF(day, t.b0, t.b1) / 365.25 yb, DATEDIFF(day, t.b1, t.a1) / 365.25 ya
  FROM t JOIN td ON td.ccn = t.ccn JOIN tp ON tp.ccn = t.ccn
)
SELECT COUNT(*) homes, MIN(inc) inc_min, MAX(inc) inc_max, (SELECT d0 FROM rng) data_start, (SELECT d1 FROM rng) data_end,
       (SELECT ss_vals FROM rng) ss_vals,
       ROUND(SUM(tb_all) / SUM(yb), 2) treated_before_py, ROUND(SUM(ta_all) / SUM(ya), 2) treated_after_py,
       ROUND(SUM(pb_all) / SUM(yb), 2) peer_before_py, ROUND(SUM(pa_all) / SUM(ya), 2) peer_after_py,
       ROUND(SUM(tb_harm) / SUM(yb), 3) treated_harm_before_py, ROUND(SUM(ta_harm) / SUM(ya), 3) treated_harm_after_py,
       ROUND(SUM(pb_harm) / SUM(yb), 3) peer_harm_before_py, ROUND(SUM(pa_harm) / SUM(ya), 3) peer_harm_after_py,
       ROUND(MEDIAN(tb_all / yb - pb_all / yb), 2) med_gap_before, ROUND(MEDIAN(ta_all / ya - pa_all / ya), 2) med_gap_after,
       COUNT_IF(tb_all = 0) treated_zero_before, COUNT_IF(ta_all = 0) treated_zero_after,
       ROUND(AVG(yb), 2) avg_years_before, ROUND(AVG(ya), 2) avg_years_after
FROM x;

-- S19 CDC: full series for Hawaii flu/pneumonia and Mississippi Alzheimer's with the US, plus the 15 biggest one-year jumps in any state-cause (50+ deaths both years)
WITH c AS (SELECT state, cause_name, year, age_adjusted_death_rate r, deaths FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_LEADING_CAUSES_STATE),
l AS (SELECT c.*, LAG(r) OVER (PARTITION BY state, cause_name ORDER BY year) pr, LAG(deaths) OVER (PARTITION BY state, cause_name ORDER BY year) pdths FROM c)
SELECT 'series' kind, state, cause_name, year, r, deaths, NULL jump
FROM c WHERE (state IN ('Hawaii', 'United States') AND cause_name = 'Influenza and pneumonia')
          OR (state IN ('Mississippi', 'United States') AND cause_name = 'Alzheimer''s disease')
UNION ALL
SELECT * FROM (
  SELECT 'jump', state, cause_name, year, r, deaths, ROUND(r / pr, 2)
  FROM l WHERE pdths >= 50 AND deaths >= 50 AND cause_name <> 'All causes' AND pr > 0
  ORDER BY ABS(LN(r / pr)) DESC LIMIT 15
)
ORDER BY kind DESC, cause_name, state, year;

-- ===== batch b4 =====
-- S20 order/refer flag combos decoded: per combo, how many are NPPES-deactivated (and since 2025-07), active opt-outs, on FISS, billed Part B in 2024
WITH o AS (SELECT npi, ANY_VALUE(partb || dme || hha || pmd || hospice) flags FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_ORDER_AND_REFERRING GROUP BY npi),
n AS (SELECT npi, npi_deactivation_date dd FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES
      WHERE npi_deactivation_date IS NOT NULL AND (npi_reactivation_date IS NULL OR npi_reactivation_date < npi_deactivation_date)),
oo AS (SELECT npi, MAX(IFF(optout_end_date IS NULL OR optout_end_date >= '2026-08-01', 1, 0)) active FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS GROUP BY npi),
f AS (SELECT DISTINCT npi FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FISCAL_INTERMEDIARY_SHARED_SYSTEM_ATTENDING_AND_RENDERING),
b AS (SELECT DISTINCT rndrng_npi npi FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER)
SELECT o.flags, COUNT(*) npis, COUNT(n.npi) deact_any, COUNT_IF(n.dd >= '2025-07-01') deact_since_2025_07,
       COUNT_IF(oo.active = 1) optout_active, COUNT(oo.npi) optout_ever, COUNT(f.npi) in_fiss, COUNT(b.npi) in_partb24,
       ROUND(MEDIAN(IFF(n.dd >= '2025-07-01', DATEDIFF(day, n.dd, '2026-08-05'::DATE), NULL))) med_days_since_deact
FROM o LEFT JOIN n ON n.npi = o.npi LEFT JOIN oo ON oo.npi = o.npi LEFT JOIN f ON f.npi = o.npi LEFT JOIN b ON b.npi = o.npi
GROUP BY o.flags ORDER BY npis DESC;

-- S21 FQHC enrollments vs HRSA health-center sites: hits by NPI/CCN and by ZIP5 + street number, by enrollment era; organizations with no hit at all; HRSA site types
WITH q AS (
  SELECT enrollment_id, associate_id, organization_name org, enrollment_state st, npi, REGEXP_REPLACE(UPPER(ccn), '[^0-9A-Z]', '') ccn,
         LEFT(zip_code, 5) z5, REGEXP_SUBSTR(TRIM(address_line_1), '^[0-9]+') anum, organization_type_structure ots, organization_other_type_text ott,
         TRY_TO_DATE(SUBSTR(enrollment_id, 2, 8), 'YYYYMMDD') enr
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FEDERALLY_QUALIFIED_HEALTH_CENTER_ENROLLMENTS
),
h AS (
  SELECT TRIM(fqhc_site_npi_number) hnpi, REGEXP_REPLACE(UPPER(fqhc_site_medicare_billing_number), '[^0-9A-Z]', '') hccn,
         LEFT(site_postal_code, 5) hz5, REGEXP_SUBSTR(TRIM(site_address), '^[0-9]+') hanum, health_center_type, site_status_description
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES
),
hn AS (SELECT DISTINCT hnpi v FROM h WHERE hnpi IS NOT NULL AND hnpi <> ''),
hc AS (SELECT DISTINCT hccn v FROM h WHERE hccn IS NOT NULL AND hccn <> ''),
ha AS (SELECT DISTINCT hz5 || '|' || hanum v FROM h WHERE hanum IS NOT NULL),
m AS (
  SELECT q.*, IFF(hn.v IS NOT NULL OR hc.v IS NOT NULL, 1, 0) id_hit, IFF(ha.v IS NOT NULL, 1, 0) addr_hit
  FROM q LEFT JOIN hn ON hn.v = q.npi LEFT JOIN hc ON hc.v = q.ccn LEFT JOIN ha ON ha.v = q.z5 || '|' || q.anum
),
org AS (
  SELECT associate_id, ANY_VALUE(org) org, LISTAGG(DISTINCT st, ',') sts, ANY_VALUE(ots) ots, ANY_VALUE(ott) ott,
         COUNT(*) n, SUM(id_hit) id_hits, SUM(GREATEST(id_hit, addr_hit)) any_hits, MIN(enr) e0, MAX(enr) e1
  FROM m GROUP BY associate_id
)
SELECT 'era' kind, CASE WHEN enr < '2015-01-01' THEN 'a_pre2015' WHEN enr < '2020-01-01' THEN 'b_2015-19' WHEN enr < '2024-01-01' THEN 'c_2020-23' ELSE 'd_2024+' END k1,
       NULL k2, COUNT(*) n1, SUM(id_hit) n2, SUM(GREATEST(id_hit, addr_hit)) n3, NULL k3
FROM m GROUP BY 2
UNION ALL
SELECT 'org_summary', ots, NULL, COUNT(*), COUNT_IF(any_hits = 0), SUM(IFF(any_hits = 0, n, 0)), NULL FROM org GROUP BY ots
UNION ALL
SELECT * FROM (
  SELECT 'org_no_hit', org, sts, n, id_hits, any_hits, ots || ' / ' || COALESCE(ott, '') || ' / ' || TO_CHAR(e0) || '..' || TO_CHAR(e1)
  FROM org WHERE any_hits = 0 ORDER BY n DESC, org LIMIT 25
)
UNION ALL
SELECT 'hrsa_types', health_center_type, site_status_description, COUNT(*), COUNT_IF(hccn IS NOT NULL AND hccn <> ''), COUNT_IF(hnpi IS NOT NULL AND hnpi <> ''), NULL
FROM h GROUP BY 2, 3
ORDER BY kind, n1 DESC;

-- S22 SNF survey-cycle test: for-profit homes whose operator company formed between their 2nd-latest and latest standard surveys, vs same-state stable for-profit homes (operator formed pre-2018)
WITH s AS (SELECT ccn, incorporation_date inc FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS),
n AS (
  SELECT cms_certification_number_ccn ccn, state,
         rating_cycle_1_standard_survey_health_date c1d, rating_cycle_2_standard_health_survey_date c2d,
         rating_cycle_1_number_of_standard_health_deficiencies c1n, rating_cycle_2_number_of_standard_health_deficiencies c2n
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME
  WHERE ownership_type ILIKE 'for profit%'
    AND rating_cycle_1_standard_survey_health_date IS NOT NULL AND rating_cycle_2_standard_health_survey_date IS NOT NULL
    AND rating_cycle_1_number_of_standard_health_deficiencies IS NOT NULL AND rating_cycle_2_number_of_standard_health_deficiencies IS NOT NULL
),
j AS (
  SELECT n.*, s.inc,
         CASE WHEN s.inc > n.c2d AND s.inc < n.c1d THEN 'a_formed_between_surveys'
              WHEN s.inc >= '2022-01-01' AND s.inc <= n.c2d THEN 'b_formed_2022+_before_both'
              WHEN s.inc >= '1900-01-01' AND s.inc < '2018-01-01' THEN 'c_stable_pre2018'
              ELSE 'd_other' END grp
  FROM n JOIN s ON s.ccn = n.ccn
),
ctl AS (SELECT state, AVG(c2n) m_c2, AVG(c1n) m_c1, AVG(c1n - c2n) m_chg, COUNT(*) n_ctl FROM j WHERE grp = 'c_stable_pre2018' GROUP BY state)
SELECT j.grp, COUNT(*) homes, ROUND(AVG(c2n), 2) mean_c2_before, ROUND(AVG(c1n), 2) mean_c1_after,
       ROUND(AVG(c2n - m_c2), 2) gap_c2, ROUND(AVG(c1n - m_c1), 2) gap_c1,
       ROUND(MEDIAN(c2n - m_c2), 2) med_gap_c2, ROUND(MEDIAN(c1n - m_c1), 2) med_gap_c1,
       ROUND(AVG((c1n - c2n) - m_chg), 2) did_mean, ROUND(MEDIAN((c1n - c2n) - m_chg), 2) did_median,
       ROUND(STDDEV((c1n - c2n) - m_chg) / SQRT(COUNT(*)), 2) did_se,
       COUNT_IF((c1n - c2n) > m_chg) worse_than_peers, MIN(c2d) c2_min, MAX(c1d) c1_max,
       ROUND(AVG(DATEDIFF(day, c2d, c1d))) avg_days_between
FROM j JOIN ctl ON ctl.state = j.state GROUP BY j.grp ORDER BY j.grp;

-- ===== batch b5 =====
-- S23 SNF survey-cycle test, robustness: (1) peers matched on survey calendar years instead of state, (2) state peers but only surveys from 2022 on, (3) state peers dropping the 4 biggest chains in the treated group
WITH s AS (SELECT ccn, incorporation_date inc, NULLIF(TRIM(affiliation_entity_name), '') aff FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS),
n AS (
  SELECT cms_certification_number_ccn ccn, state,
         rating_cycle_1_standard_survey_health_date c1d, rating_cycle_2_standard_health_survey_date c2d,
         rating_cycle_1_number_of_standard_health_deficiencies c1n, rating_cycle_2_number_of_standard_health_deficiencies c2n
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME
  WHERE ownership_type ILIKE 'for profit%'
    AND rating_cycle_1_standard_survey_health_date IS NOT NULL AND rating_cycle_2_standard_health_survey_date IS NOT NULL
    AND rating_cycle_1_number_of_standard_health_deficiencies IS NOT NULL AND rating_cycle_2_number_of_standard_health_deficiencies IS NOT NULL
),
j AS (
  SELECT n.*, s.inc, s.aff, YEAR(n.c2d) y2, YEAR(n.c1d) y1,
         CASE WHEN s.inc > n.c2d AND s.inc < n.c1d THEN 'T'
              WHEN s.inc >= '1900-01-01' AND s.inc < '2018-01-01' THEN 'C' END grp
  FROM n JOIN s ON s.ccn = n.ccn
),
topaff AS (SELECT aff FROM j WHERE grp = 'T' AND aff IS NOT NULL GROUP BY aff ORDER BY COUNT(*) DESC LIMIT 4),
cal AS (SELECT y2, y1, AVG(c2n) m_c2, AVG(c1n) m_c1, COUNT(*) n_c FROM j WHERE grp = 'C' GROUP BY y2, y1),
st22 AS (SELECT state, AVG(c2n) m_c2, AVG(c1n) m_c1, COUNT(*) n_c FROM j WHERE grp = 'C' AND c2d >= '2022-01-01' GROUP BY state),
st AS (SELECT state, AVG(c2n) m_c2, AVG(c1n) m_c1 FROM j WHERE grp = 'C' GROUP BY state),
v AS (
  SELECT 'v1_calendar_matched' variant, j.c2n - cal.m_c2 g2, j.c1n - cal.m_c1 g1, j.c2d, j.c1d FROM j JOIN cal ON cal.y2 = j.y2 AND cal.y1 = j.y1 WHERE j.grp = 'T' AND cal.n_c >= 10
  UNION ALL
  SELECT 'v2_state_2022on', j.c2n - st22.m_c2, j.c1n - st22.m_c1, j.c2d, j.c1d FROM j JOIN st22 ON st22.state = j.state WHERE j.grp = 'T' AND j.c2d >= '2022-01-01' AND st22.n_c >= 5
  UNION ALL
  SELECT 'v3_state_no_top4_chains', j.c2n - st.m_c2, j.c1n - st.m_c1, j.c2d, j.c1d FROM j JOIN st ON st.state = j.state
  WHERE j.grp = 'T' AND (j.aff IS NULL OR j.aff NOT IN (SELECT aff FROM topaff))
)
SELECT variant, COUNT(*) homes, ROUND(AVG(g2), 2) gap_before, ROUND(AVG(g1), 2) gap_after, ROUND(MEDIAN(g2), 2) med_before, ROUND(MEDIAN(g1), 2) med_after,
       ROUND(AVG(g1 - g2), 2) did, ROUND(MEDIAN(g1 - g2), 2) did_med, ROUND(STDDEV(g1 - g2) / SQRT(COUNT(*)), 2) did_se, COUNT_IF(g1 > g2) worse,
       ROUND(AVG(DATEDIFF(day, c2d, c1d))) days_between, (SELECT LISTAGG(aff, ' | ') FROM topaff) top4
FROM v GROUP BY variant ORDER BY variant;

-- S24 decode Part B = N on order/refer: share of each flag combo present in the PECOS enrollment file, plus that file's load date
WITH o AS (SELECT npi, ANY_VALUE(partb || dme || hha || pmd || hospice) flags FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_ORDER_AND_REFERRING GROUP BY npi),
p AS (SELECT npi, COUNT(*) enrl, LISTAGG(DISTINCT provider_type_cd, ',') WITHIN GROUP (ORDER BY provider_type_cd) types
      FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT GROUP BY npi)
SELECT o.flags, COUNT(*) npis, COUNT(p.npi) in_pecos, ROUND(COUNT(p.npi) / COUNT(*), 3) share_in_pecos,
       (SELECT TO_CHAR(created) FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES WHERE table_schema = 'LANDING' AND table_name = 'FED_CMS_PECOS_PROVIDER_ENROLLMENT') pecos_loaded,
       MODE(p.types) top_type
FROM o LEFT JOIN p ON p.npi = o.npi GROUP BY o.flags ORDER BY npis DESC;

-- S25 eyeball 6 nursing homes whose operator company formed between their two latest standard surveys (biggest rise first), with star rating and chain
WITH s AS (SELECT ccn, incorporation_date inc, organization_name op, NULLIF(TRIM(affiliation_entity_name), '') aff FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS),
n AS (
  SELECT cms_certification_number_ccn ccn, provider_name, city, state, overall_rating, number_of_certified_beds beds,
         rating_cycle_1_standard_survey_health_date c1d, rating_cycle_2_standard_health_survey_date c2d,
         rating_cycle_1_number_of_standard_health_deficiencies c1n, rating_cycle_2_number_of_standard_health_deficiencies c2n,
         date_first_approved_to_provide_medicare_and_medicaid_services first_ok
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME WHERE ownership_type ILIKE 'for profit%'
)
SELECT n.ccn, n.provider_name, n.city, n.state, s.op, s.aff, s.inc, n.first_ok, n.c2d, n.c2n, n.c1d, n.c1n, n.overall_rating, n.beds
FROM n JOIN s ON s.ccn = n.ccn
WHERE s.inc > n.c2d AND s.inc < n.c1d
ORDER BY (n.c1n - n.c2n) DESC, n.ccn LIMIT 6;

-- ===== batch b6 =====
-- S26 (rewrite of S23, which failed to compile) SNF survey-cycle robustness: (1) peers matched on survey calendar years, (2) state peers, surveys from 2022 on only, (3) state peers dropping the 4 biggest chains in the treated group
WITH s AS (SELECT ccn, incorporation_date inc, NULLIF(TRIM(affiliation_entity_name), '') aff FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS),
n AS (
  SELECT cms_certification_number_ccn ccn, state,
         rating_cycle_1_standard_survey_health_date c1d, rating_cycle_2_standard_health_survey_date c2d,
         rating_cycle_1_number_of_standard_health_deficiencies c1n, rating_cycle_2_number_of_standard_health_deficiencies c2n
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME
  WHERE ownership_type ILIKE 'for profit%'
    AND rating_cycle_1_standard_survey_health_date IS NOT NULL AND rating_cycle_2_standard_health_survey_date IS NOT NULL
    AND rating_cycle_1_number_of_standard_health_deficiencies IS NOT NULL AND rating_cycle_2_number_of_standard_health_deficiencies IS NOT NULL
),
j AS (
  SELECT n.*, s.inc, s.aff, YEAR(n.c2d) y2, YEAR(n.c1d) y1,
         CASE WHEN s.inc > n.c2d AND s.inc < n.c1d THEN 'T'
              WHEN s.inc >= '1900-01-01' AND s.inc < '2018-01-01' THEN 'C' END grp
  FROM n JOIN s ON s.ccn = n.ccn
),
topaff AS (SELECT aff, COUNT(*) k FROM j WHERE grp = 'T' AND aff IS NOT NULL GROUP BY aff ORDER BY k DESC LIMIT 4),
toplist AS (SELECT LISTAGG(aff || ' ' || k, ' | ') top4 FROM topaff),
cal AS (SELECT y2, y1, AVG(c2n) m_c2, AVG(c1n) m_c1, COUNT(*) n_c FROM j WHERE grp = 'C' GROUP BY y2, y1),
st22 AS (SELECT state, AVG(c2n) m_c2, AVG(c1n) m_c1, COUNT(*) n_c FROM j WHERE grp = 'C' AND c2d >= '2022-01-01' GROUP BY state),
st AS (SELECT state, AVG(c2n) m_c2, AVG(c1n) m_c1 FROM j WHERE grp = 'C' GROUP BY state),
v AS (
  SELECT 'v1_calendar_matched' variant, j.c2n - cal.m_c2 g2, j.c1n - cal.m_c1 g1, j.c2d, j.c1d
  FROM j JOIN cal ON cal.y2 = j.y2 AND cal.y1 = j.y1 WHERE j.grp = 'T' AND cal.n_c >= 10
  UNION ALL
  SELECT 'v2_state_2022on', j.c2n - st22.m_c2, j.c1n - st22.m_c1, j.c2d, j.c1d
  FROM j JOIN st22 ON st22.state = j.state WHERE j.grp = 'T' AND j.c2d >= '2022-01-01' AND st22.n_c >= 5
  UNION ALL
  SELECT 'v3_state_no_top4_chains', j.c2n - st.m_c2, j.c1n - st.m_c1, j.c2d, j.c1d
  FROM j JOIN st ON st.state = j.state LEFT JOIN topaff ON topaff.aff = j.aff
  WHERE j.grp = 'T' AND topaff.aff IS NULL
)
SELECT v.variant, COUNT(*) homes, ROUND(AVG(g2), 2) gap_before, ROUND(AVG(g1), 2) gap_after, ROUND(MEDIAN(g2), 2) med_before, ROUND(MEDIAN(g1), 2) med_after,
       ROUND(AVG(g1 - g2), 2) did, ROUND(MEDIAN(g1 - g2), 2) did_med, ROUND(STDDEV(g1 - g2) / SQRT(COUNT(*)), 2) did_se, COUNT_IF(g1 > g2) worse,
       ROUND(AVG(DATEDIFF(day, c2d, c1d))) days_between, ANY_VALUE(toplist.top4) top4
FROM v CROSS JOIN toplist GROUP BY v.variant ORDER BY v.variant;

-- S27 stakes: order/refer NPIs with Part B = N (no current enrollment), their 2024 DME referrals (DY2024), split by NPPES deactivation
WITH o AS (SELECT npi, ANY_VALUE(partb) partb FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_ORDER_AND_REFERRING GROUP BY npi),
n AS (SELECT npi FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES
      WHERE npi_deactivation_date IS NOT NULL AND (npi_reactivation_date IS NULL OR npi_reactivation_date < npi_deactivation_date)),
r AS (SELECT rfrg_npi npi, suplr_mdcr_alowd_amt amt, tot_suplr_benes benes FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_REFER)
SELECT o.partb, IFF(n.npi IS NULL, 'npi_active', 'npi_deactivated') npi_status, COUNT(*) npis, COUNT(r.npi) dme_referrers_2024,
       ROUND(SUM(r.amt)) dme_allowed_2024, ROUND(MEDIAN(r.amt)) median_referrer_allowed, ROUND(MAX(r.amt)) max_referrer_allowed,
       ROUND(SUM(r.amt) / NULLIF(COUNT(r.npi), 0)) mean_referrer_allowed
FROM o LEFT JOIN n ON n.npi = o.npi LEFT JOIN r ON r.npi = o.npi
GROUP BY 1, 2 ORDER BY 1, 2;

-- ===== batch b7 =====
-- S28 OIG-excluded people (real NPI, no waiver) on order/refer: flag combos by exclusion age, and presence in PECOS enrollment
WITH l AS (
  SELECT npi, MIN(exclusion_date) exd, MAX(IFF(has_waiver, 1, 0)) waiver
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE WHERE npi_is_real GROUP BY npi
),
o AS (SELECT npi, ANY_VALUE(partb || dme || hha || pmd || hospice) flags FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_ORDER_AND_REFERRING GROUP BY npi),
p AS (SELECT DISTINCT npi FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT)
SELECT IFF(l.exd >= '2026-05-01', 'a_excluded_2026-05+', 'b_excluded_before_2026-05') age, l.waiver, o.flags, COUNT(*) npis, COUNT(p.npi) in_pecos,
       MIN(l.exd) exd_min, MAX(l.exd) exd_max
FROM l JOIN o ON o.npi = l.npi LEFT JOIN p ON p.npi = l.npi
GROUP BY 1, 2, 3 ORDER BY 1, 2, 3;

-- S29 the glance said one NPI sits on 107 SNF enrollments and another on 82 FQHC enrollments: count those NPIs in the marts and the landing tables
SELECT 'mart_snf' src, npi, COUNT(*) n FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS
 WHERE npi IN ('1386028397', '1245023100', '1336953629') GROUP BY 1, 2
UNION ALL
SELECT 'landing_snf', npi, COUNT(*) FROM LIBRARY_RAW.LANDING.FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS
 WHERE npi IN ('1386028397', '1245023100', '1336953629') GROUP BY 1, 2
UNION ALL
SELECT 'mart_fqhc', npi, COUNT(*) FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FEDERALLY_QUALIFIED_HEALTH_CENTER_ENROLLMENTS
 WHERE npi IN ('1083820583', '1033752688', '1821336959') GROUP BY 1, 2
UNION ALL
SELECT 'landing_fqhc', npi, COUNT(*) FROM LIBRARY_RAW.LANDING.FED_CMS_FEDERALLY_QUALIFIED_HEALTH_CENTER_ENROLLMENTS
 WHERE npi IN ('1083820583', '1033752688', '1821336959') GROUP BY 1, 2
ORDER BY 1, 2;

-- ===== batch b8 =====
-- S30 who are the Part B = N clinicians on order/refer (NPI still active in NPPES): trainee share, enumeration year, top primary taxonomy codes, vs Part B = Y
WITH o AS (SELECT npi, ANY_VALUE(partb) partb FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_ORDER_AND_REFERRING GROUP BY npi),
n AS (SELECT npi, healthcare_provider_taxonomy_code_1 tx, YEAR(provider_enumeration_date) ey, npi_deactivation_date dd, npi_reactivation_date rd
      FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES),
j AS (SELECT o.partb, n.tx, n.ey FROM o JOIN n ON n.npi = o.npi WHERE n.dd IS NULL OR n.rd >= n.dd)
SELECT 'share' kind, partb, NULL tx, COUNT(*) npis, COUNT_IF(tx = '390200000X') trainees, ROUND(MEDIAN(ey)) med_enum_year, COUNT_IF(ey >= 2020) enum_2020_on
FROM j GROUP BY partb
UNION ALL
SELECT * FROM (
  SELECT 'top_tx_partb_N', partb, tx, COUNT(*), NULL, ROUND(MEDIAN(ey)), COUNT_IF(ey >= 2020)
  FROM j WHERE partb = 'N' GROUP BY partb, tx ORDER BY COUNT(*) DESC LIMIT 10
)
ORDER BY kind, npis DESC;
