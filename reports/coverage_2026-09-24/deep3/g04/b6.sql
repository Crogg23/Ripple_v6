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
