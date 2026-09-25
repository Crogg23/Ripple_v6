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
