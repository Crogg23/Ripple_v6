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
