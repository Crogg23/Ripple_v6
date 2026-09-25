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
