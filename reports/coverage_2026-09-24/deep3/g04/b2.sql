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
