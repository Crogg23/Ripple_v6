-- S02 DIM_DATE: one row per day? every derived column checked against the date itself; exact vs APPROX_TOP_K month counts
WITH ym AS (SELECT YEAR_MONTH, COUNT(*) n FROM LIBRARY_MARTS.CORE.DIM_DATE GROUP BY 1)
SELECT COUNT(*) n, COUNT(DISTINCT d.DATE_DAY) days, MIN(d.DATE_DAY) d0, MAX(d.DATE_DAY) d1,
       DATEDIFF(day, MIN(d.DATE_DAY), MAX(d.DATE_DAY)) + 1 expected_days,
       ANY_VALUE(k.ym_n) year_months, ANY_VALUE(k.ym_max) exact_max_days_per_month, ANY_VALUE(k.ym_min) exact_min_days_per_month,
       ANY_VALUE(a.approx) approx_top5_year_month,
       COUNT_IF(d.YEAR_MONTH <> TO_CHAR(d.DATE_DAY, 'YYYY-MM')) bad_year_month,
       COUNT_IF(d.DAY_OF_WEEK_ISO <> DAYOFWEEKISO(d.DATE_DAY)) bad_dow,
       COUNT_IF(d.WEEK_OF_YEAR_ISO <> WEEKISO(d.DATE_DAY)) bad_isoweek,
       COUNT_IF(d.IS_WEEKEND IS NULL) null_weekend,
       COUNT_IF(d.IS_WEEKEND <> (DAYOFWEEKISO(d.DATE_DAY) IN (6, 7))) bad_weekend,
       COUNT_IF(d.IS_WEEKEND) weekend_days,
       COUNT_IF(d.US_FISCAL_YEAR <> YEAR(d.DATE_DAY) + IFF(MONTH(d.DATE_DAY) >= 10, 1, 0)) bad_fy,
       COUNT_IF(d.YEAR_NUMBER <> YEAR(d.DATE_DAY) OR d.QUARTER_NUMBER <> QUARTER(d.DATE_DAY)
                OR d.MONTH_NUMBER <> MONTH(d.DATE_DAY) OR d.DAY_OF_MONTH <> DAY(d.DATE_DAY)) bad_parts,
       COUNT_IF(d.MONTH_NAME <> TO_CHAR(d.DATE_DAY, 'MMMM')) bad_month_name,
       ARRAY_AGG(DISTINCT d.DAY_NAME) day_names
FROM LIBRARY_MARTS.CORE.DIM_DATE d
CROSS JOIN (SELECT COUNT(*) ym_n, MAX(n) ym_max, MIN(n) ym_min FROM ym) k
CROSS JOIN (SELECT APPROX_TOP_K(YEAR_MONTH, 5) approx FROM LIBRARY_MARTS.CORE.DIM_DATE) a

-- S03 XWALK_ZCTA_COUNTY: grain, duplicates, exact vs APPROX_TOP_K for the "347 rows" ZIPs, code widths, CT codes
WITH x AS (SELECT * FROM LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY),
z AS (SELECT ZCTA5, COUNT(*) n, COUNT(DISTINCT COUNTY_FIPS) c FROM x GROUP BY 1),
cf AS (SELECT COUNTY_FIPS, COUNT(*) n FROM x GROUP BY 1)
SELECT (SELECT COUNT(*) FROM x) n,
       (SELECT COUNT(DISTINCT ZCTA5, COUNTY_FIPS) FROM x) distinct_pairs,
       (SELECT COUNT(*) FROM z) zctas,
       (SELECT COUNT(*) FROM cf) counties,
       (SELECT MAX(n) FROM z) exact_max_rows_per_zcta,
       (SELECT COUNT_IF(c > 1) FROM z) zctas_multi_county,
       (SELECT MAX(c) FROM z) max_counties_per_zcta,
       (SELECT OBJECT_AGG(ZCTA5, n::variant) FROM z WHERE ZCTA5 IN ('99901','99833','99827')) exact_battery_zips,
       (SELECT APPROX_TOP_K(ZCTA5, 5) FROM x) approx_top5_zcta,
       (SELECT OBJECT_AGG(COUNTY_FIPS, n::variant) FROM cf WHERE COUNTY_FIPS IN ('06037','04013','06073')) exact_battery_counties,
       (SELECT ARRAY_AGG(OBJECT_CONSTRUCT('f', COUNTY_FIPS, 'n', n)) FROM (SELECT * FROM cf ORDER BY n DESC LIMIT 5)) exact_top5_county,
       (SELECT COUNT_IF(ZCTA5 IS NULL OR LENGTH(ZCTA5) <> 5) FROM x) bad_zcta,
       (SELECT COUNT_IF(COUNTY_FIPS IS NULL OR LENGTH(COUNTY_FIPS) <> 5) FROM x) bad_county,
       (SELECT COUNT_IF(LEFT(COUNTY_FIPS, 2) <> STATE_FIPS) FROM x) state_prefix_mismatch,
       (SELECT ARRAY_AGG(DISTINCT COUNTY_FIPS) WITHIN GROUP (ORDER BY COUNTY_FIPS) FROM x WHERE COUNTY_FIPS LIKE '09%') ct_codes,
       (SELECT ARRAY_AGG(DISTINCT VINTAGE) FROM x) vintages,
       (SELECT ARRAY_AGG(DISTINCT XWALK_TYPE) FROM x) types,
       (SELECT COUNT(DISTINCT STATE_USPS) FROM x) states

-- S04 Cross-check the three geography tables: county codes in the ZIP tables that DIM_COUNTY does not hold, and DIM_COUNTY counties no ZIP touches
WITH dc AS (SELECT COUNTY_FIPS f, STATE_NAME FROM LIBRARY_MARTS.CORE.DIM_COUNTY),
s AS (
  SELECT 'XWALK_ZCTA_COUNTY' src, STATE_USPS st, COUNTY_FIPS f, COUNT(*) r FROM LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY GROUP BY 1, 2, 3
  UNION ALL
  SELECT 'DIM_ZIP_POINT', STATE_USPS, PRIMARY_COUNTY_FIPS, COUNT(*) FROM LIBRARY_MARTS.CORE.DIM_ZIP_POINT GROUP BY 1, 2, 3),
j AS (SELECT s.*, (dc.f IS NOT NULL) hit FROM s LEFT JOIN dc ON dc.f = s.f),
rev AS (SELECT 'DIM_COUNTY not in XWALK' src, LEFT(dc.f, 2) st, dc.f, 1 r, FALSE hit
        FROM dc LEFT JOIN (SELECT DISTINCT COUNTY_FIPS f FROM LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY) x ON x.f = dc.f WHERE x.f IS NULL)
SELECT src, st, COUNT(*) counties, COUNT_IF(NOT hit) counties_missing, SUM(r) rows_, SUM(IFF(hit, 0, r)) rows_missing,
       ARRAY_AGG(IFF(hit, NULL, f)) WITHIN GROUP (ORDER BY f) missing_codes
FROM (SELECT * FROM j UNION ALL SELECT * FROM rev)
GROUP BY 1, 2 HAVING COUNT_IF(NOT hit) > 0
UNION ALL
SELECT src, 'ALL', COUNT(*), COUNT_IF(NOT hit), SUM(r), SUM(IFF(hit, 0, r)), NULL FROM j GROUP BY 1
ORDER BY 1, 2

-- S05 DIM_COUNTY: grain, code widths, population nulls and totals, territories, CT rows, smallest and largest
SELECT COUNT(*) n, COUNT(DISTINCT COUNTY_FIPS) fips, COUNT_IF(LENGTH(COUNTY_FIPS) <> 5) bad_fips,
       COUNT_IF(LEFT(COUNTY_FIPS, 2) <> STATE_FIPS) prefix_mismatch, COUNT(DISTINCT STATE_FIPS) states,
       COUNT_IF(POPULATION_2020 IS NULL) pop_null, COUNT_IF(POPULATION_2020 = 0) pop_zero,
       SUM(POPULATION_2020) pop_sum, SUM(IFF(STATE_FIPS = '72', 0, POPULATION_2020)) pop_sum_no_pr,
       COUNT_IF(STATE_FIPS = '72') pr_rows, COUNT_IF(STATE_FIPS > '56' AND STATE_FIPS <> '72') other_territory_rows,
       MEDIAN(POPULATION_2020) med_pop,
       ARRAY_AGG(IFF(STATE_FIPS = '09', COUNTY_FIPS || ' ' || COUNTY_NAME || ' ' || POPULATION_2020, NULL)) WITHIN GROUP (ORDER BY COUNTY_FIPS) ct_rows,
       ARRAY_AGG(IFF(STATE_FIPS = '02' AND COUNTY_FIPS IN ('02063','02066','02261'), COUNTY_FIPS || ' ' || COUNTY_NAME, NULL)) ak_valdez,
       MIN_BY(COUNTY_FIPS || ' ' || COUNTY_NAME || ' ' || POPULATION_2020, POPULATION_2020) smallest,
       MAX_BY(COUNTY_FIPS || ' ' || COUNTY_NAME || ' ' || POPULATION_2020, POPULATION_2020) largest,
       COUNT_IF(POP_CENTER_LAT IS NULL OR POP_CENTER_LON IS NULL) pt_null,
       COUNT_IF(POP_CENTER_LON > 0) lon_positive, ARRAY_AGG(DISTINCT VINTAGE) vintages
FROM LIBRARY_MARTS.CORE.DIM_COUNTY

-- S06 DIM_ZIP_POINT: how many ZIPs share one dot, whose dot it is, and whether COUNTY_SPAN agrees with the crosswalk
WITH p AS (SELECT * FROM LIBRARY_MARTS.CORE.DIM_ZIP_POINT),
xs AS (SELECT ZCTA5, COUNT(DISTINCT COUNTY_FIPS) span FROM LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY GROUP BY 1),
pt AS (SELECT ROUND(LAT, 5) la, ROUND(LON, 5) lo, COUNT(*) n FROM p GROUP BY 1, 2),
m AS (SELECT POINT_METHOD, COUNT(*) n FROM p GROUP BY 1),
j AS (SELECT p.*, xs.span, dc.POP_CENTER_LAT, dc.POP_CENTER_LON FROM p
      LEFT JOIN xs ON xs.ZCTA5 = p.ZCTA5 LEFT JOIN LIBRARY_MARTS.CORE.DIM_COUNTY dc ON dc.COUNTY_FIPS = p.PRIMARY_COUNTY_FIPS)
SELECT COUNT(*) n, COUNT(DISTINCT j.ZCTA5) zctas,
       ANY_VALUE(k.pts) distinct_points, ANY_VALUE(k.maxn) max_zips_on_one_point, ANY_VALUE(k.medn) median_zips_per_point,
       ANY_VALUE(q.xz) xwalk_zctas, ANY_VALUE(q.x_not_p) xwalk_zips_not_in_point,
       COUNT_IF(span IS NULL) point_zips_not_in_xwalk,
       COUNT_IF(span IS NOT NULL AND span <> COUNTY_SPAN) span_disagree,
       COUNT_IF(ABS(LAT - POP_CENTER_LAT) < 0.0001 AND ABS(LON - POP_CENTER_LON) < 0.0001) point_is_primary_pop_center,
       COUNT_IF(POP_CENTER_LAT IS NULL) primary_county_not_in_dim,
       MEDIAN(HAVERSINE(LAT, LON, POP_CENTER_LAT, POP_CENTER_LON)) med_km_point_to_pop_center,
       COUNT_IF(COUNTY_SPAN > 1) multi_county_zips,
       ANY_VALUE(mm.methods) methods
FROM j
CROSS JOIN (SELECT COUNT(*) pts, MAX(n) maxn, MEDIAN(n) medn FROM pt) k
CROSS JOIN (SELECT COUNT(*) xz, COUNT_IF(p.ZCTA5 IS NULL) x_not_p FROM xs LEFT JOIN p ON p.ZCTA5 = xs.ZCTA5) q
CROSS JOIN (SELECT OBJECT_AGG(POINT_METHOD, n::variant) methods FROM m) mm
