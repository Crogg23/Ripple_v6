-- deep3/g73: deep pass 3, 2026-09-24. Python door (connect/db.py), read-only SELECT/WITH only, QUERY_TAG 'deep3-2026-09-24'.
-- Every connection first ran: ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300; ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'. Six connections; those pairs are not counted.
-- Tables: CORE.DIM_ZIP_POINT, CORE.XWALK_ZCTA_COUNTY, CORE.DIM_COUNTY, CORE.XWALK_HOSPITAL_CCN_EIN, CORE.DIM_DATE.
-- 15 statements (S01-S15), all below, in run order. Outputs: g73/out_Sxx.txt and g73/out_Sxx.csv.
-- Note: S11 first failed the runner's own one-statement guard (a '; ' separator inside LISTAGG); it never reached the warehouse. Fixed separator, rerun.

-- S01 Columns and types for the five tables
SELECT TABLE_NAME, ORDINAL_POSITION, COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
FROM LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'CORE' AND TABLE_NAME IN ('DIM_ZIP_POINT','XWALK_ZCTA_COUNTY','DIM_COUNTY','XWALK_HOSPITAL_CCN_EIN','DIM_DATE')
ORDER BY 1, 2
;

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

;

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

;

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

;

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

;

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
;

-- S07 XWALK_HOSPITAL_CCN_EIN: profile by tier and for-profit flag; ZIP agreement, NTEE health share, widths, facility type from CCN digits
SELECT MATCH_TIER, MATCH_RULE, PROPRIETARY_NONPROFIT pn, COUNT(*) n, COUNT(DISTINCT CCN) ccns, COUNT(DISTINCT EIN) eins,
       COUNT_IF(CCN_ZIP5 = EIN_ZIP5) zip_same, COUNT_IF(LEFT(CCN_ZIP5, 3) <> LEFT(EIN_ZIP5, 3)) zip3_diff,
       COUNT_IF(EIN_NTEE LIKE 'E%') ntee_e, COUNT_IF(NULLIF(TRIM(EIN_NTEE), '') IS NULL) ntee_blank,
       COUNT_IF(NOT REGEXP_LIKE(EIN, '^[0-9]{9}$')) ein_not9, COUNT_IF(LENGTH(CCN) <> 6) ccn_not6,
       COUNT_IF(TRY_TO_NUMBER(SUBSTR(CCN, 3, 4)) BETWEEN 1 AND 879) short_term,
       COUNT_IF(TRY_TO_NUMBER(SUBSTR(CCN, 3, 4)) BETWEEN 1300 AND 1399) cah,
       COUNT_IF(TRY_TO_NUMBER(SUBSTR(CCN, 3, 4)) BETWEEN 2000 AND 2299) ltch,
       COUNT_IF(TRY_TO_NUMBER(SUBSTR(CCN, 3, 4)) BETWEEN 3025 AND 3099) rehab,
       COUNT_IF(TRY_TO_NUMBER(SUBSTR(CCN, 3, 4)) BETWEEN 3300 AND 3399) childrens,
       COUNT_IF(TRY_TO_NUMBER(SUBSTR(CCN, 3, 4)) BETWEEN 4000 AND 4499) psych,
       COUNT_IF(TRY_TO_NUMBER(SUBSTR(CCN, 3, 4)) IS NULL) ccn_letter,
       COUNT(DISTINCT BUILT_AT) built_ats
FROM LIBRARY_MARTS.CORE.XWALK_HOSPITAL_CCN_EIN
GROUP BY 1, 2, 3 ORDER BY 1, 3

;

-- S08 XWALK_HOSPITAL_CCN_EIN: exact EIN fan-out (battery's 37/32/32 came from APPROX_TOP_K), top 15 with totals
WITH e AS (SELECT EIN, ANY_VALUE(EIN_NAME) ein_name, ANY_VALUE(EIN_ZIP5) ein_zip, COUNT(*) n, COUNT(DISTINCT CCN) ccns,
                  COUNT(DISTINCT LEFT(CCN, 2)) ccn_states, COUNT(DISTINCT CCN_ZIP5) ccn_zips,
                  ARRAY_AGG(DISTINCT MATCH_TIER) tiers, SUM(IFF(PROPRIETARY_NONPROFIT = 'P', 1, 0)) p_rows
           FROM LIBRARY_MARTS.CORE.XWALK_HOSPITAL_CCN_EIN GROUP BY 1)
SELECT EIN, ein_name, ein_zip, n, ccns, ccn_states, ccn_zips, tiers, p_rows,
       COUNT(*) OVER () all_eins, SUM(IFF(ccns > 1, 1, 0)) OVER () eins_multi,
       SUM(IFF(ccns > 1, ccns, 0)) OVER () ccns_on_shared_eins, SUM(IFF(ccns >= 10, ccns, 0)) OVER () ccns_on_10plus_eins
FROM e
QUALIFY ROW_NUMBER() OVER (ORDER BY ccns DESC, EIN) <= 15
ORDER BY ccns DESC, EIN

;

-- S09 XWALK_HOSPITAL_CCN_EIN: eyeball samples with group totals: for-profit hospitals matched to a tax-exempt EIN; tier 3 matches in another ZIP3; tier 3 EINs claimed by 2+ hospitals in different ZIP3s
WITH x AS (SELECT * FROM LIBRARY_MARTS.CORE.XWALK_HOSPITAL_CCN_EIN),
t3 AS (SELECT EIN, COUNT(DISTINCT CCN) c, COUNT(DISTINCT LEFT(CCN_ZIP5, 3)) z3 FROM x WHERE MATCH_TIER = 3 GROUP BY 1)
SELECT * FROM (
  SELECT 'P_forprofit' grp, COUNT(*) OVER () grp_rows, CCN, CCN_NAME, CCN_ZIP5, EIN, EIN_NAME, EIN_ZIP5, EIN_NTEE, MATCH_TIER
  FROM x WHERE PROPRIETARY_NONPROFIT = 'P' QUALIFY ROW_NUMBER() OVER (ORDER BY HASH(CCN)) <= 15)
UNION ALL
SELECT * FROM (
  SELECT 'T3_other_zip3', COUNT(*) OVER (), CCN, CCN_NAME, CCN_ZIP5, EIN, EIN_NAME, EIN_ZIP5, EIN_NTEE, MATCH_TIER
  FROM x WHERE MATCH_TIER = 3 AND LEFT(CCN_ZIP5, 3) <> LEFT(EIN_ZIP5, 3) QUALIFY ROW_NUMBER() OVER (ORDER BY HASH(CCN)) <= 12)
UNION ALL
SELECT * FROM (
  SELECT 'T3_shared_ein', COUNT(*) OVER (), x.CCN, x.CCN_NAME, x.CCN_ZIP5, x.EIN, x.EIN_NAME, x.EIN_ZIP5, x.EIN_NTEE, x.MATCH_TIER
  FROM x JOIN t3 ON t3.EIN = x.EIN WHERE x.MATCH_TIER = 3 AND t3.c > 1 AND t3.z3 > 1 QUALIFY ROW_NUMBER() OVER (ORDER BY x.EIN, x.CCN) <= 18)

;

-- S10 Crosswalk coverage against its own source (Medicare hospital enrollments): match rate by for-profit flag and CCN type, then non-profit short-term hospitals by state
WITH h AS (SELECT CCN, ANY_VALUE(STATE) st, ANY_VALUE(PROPRIETARY_NONPROFIT) pn FROM LIBRARY_RAW.LANDING.FED_CMS_HOSPITAL_ENROLLMENTS GROUP BY 1),
x AS (SELECT DISTINCT CCN FROM LIBRARY_MARTS.CORE.XWALK_HOSPITAL_CCN_EIN),
j AS (SELECT h.*, (x.CCN IS NOT NULL) hit,
             CASE WHEN TRY_TO_NUMBER(SUBSTR(h.CCN, 3, 4)) BETWEEN 1 AND 879 THEN 'short-term'
                  WHEN TRY_TO_NUMBER(SUBSTR(h.CCN, 3, 4)) BETWEEN 1300 AND 1399 THEN 'CAH'
                  WHEN TRY_TO_NUMBER(SUBSTR(h.CCN, 3, 4)) BETWEEN 2000 AND 2299 THEN 'LTCH'
                  WHEN TRY_TO_NUMBER(SUBSTR(h.CCN, 3, 4)) BETWEEN 3025 AND 3099 THEN 'rehab'
                  WHEN TRY_TO_NUMBER(SUBSTR(h.CCN, 3, 4)) BETWEEN 3300 AND 3399 THEN 'childrens'
                  WHEN TRY_TO_NUMBER(SUBSTR(h.CCN, 3, 4)) BETWEEN 4000 AND 4499 THEN 'psych'
                  ELSE 'other' END typ
      FROM h LEFT JOIN x ON x.CCN = h.CCN)
SELECT 'by_type' cut, pn, typ, NULL st, COUNT(*) ccns, COUNT_IF(hit) matched, ROUND(100 * COUNT_IF(hit) / COUNT(*), 1) pct
FROM j GROUP BY 2, 3
UNION ALL
SELECT 'np_short_term_by_state', pn, typ, st, COUNT(*), COUNT_IF(hit), ROUND(100 * COUNT_IF(hit) / COUNT(*), 1)
FROM j WHERE pn = 'N' AND typ = 'short-term' GROUP BY 2, 3, 4
ORDER BY 1, 7 DESC
;

-- S11 DIM_ZIP_POINT: which ZIPs are missing (by state), and is the "primary county" of a multi-county ZIP simply the most populous county it touches? with examples
WITH p AS (SELECT * FROM LIBRARY_MARTS.CORE.DIM_ZIP_POINT),
x AS (SELECT x.ZCTA5, x.COUNTY_FIPS, x.COUNTY_NAME, x.STATE_USPS, dc.POPULATION_2020 pop
      FROM LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY x LEFT JOIN LIBRARY_MARTS.CORE.DIM_COUNTY dc ON dc.COUNTY_FIPS = x.COUNTY_FIPS),
z AS (SELECT ZCTA5, MAX_BY(COUNTY_FIPS, pop) big_fips, MAX(pop) big_pop, MIN(pop) small_pop, COUNT(*) span,
             LISTAGG(COUNTY_NAME || ' ' || STATE_USPS || ' (' || pop || ')', ' + ') WITHIN GROUP (ORDER BY pop DESC) counties
      FROM x GROUP BY 1),
miss AS (SELECT x.STATE_USPS st, COUNT(DISTINCT x.ZCTA5) n FROM x LEFT JOIN p ON p.ZCTA5 = x.ZCTA5 WHERE p.ZCTA5 IS NULL GROUP BY 1),
j AS (SELECT p.ZCTA5, p.PRIMARY_COUNTY_FIPS, p.COUNTY_SPAN, z.big_fips, z.big_pop, z.small_pop, z.counties FROM p JOIN z ON z.ZCTA5 = p.ZCTA5 WHERE p.COUNTY_SPAN > 1)
SELECT 'summary' k, NULL zcta, (SELECT COUNT(*) FROM j) multi_county_zips,
       (SELECT COUNT_IF(PRIMARY_COUNTY_FIPS = big_fips) FROM j) primary_is_most_populous,
       (SELECT COUNT_IF(big_pop >= 20 * small_pop) FROM j) span_with_20x_pop_gap,
       (SELECT OBJECT_AGG(st, n::variant) FROM miss)::string detail
UNION ALL
SELECT 'example', ZCTA5, COUNTY_SPAN, NULL, NULL, PRIMARY_COUNTY_FIPS || ' <- ' || counties
FROM j WHERE ZCTA5 IN ('93243', '93225', '93510', '92371', '85118', '75009', '30114', '20619')

;

-- S12 XWALK_HOSPITAL_CCN_EIN: does the matched IRS name look like the hospital? Jaro-Winkler by tier, junk-entity names, odd-width CCNs
WITH x AS (SELECT *, JAROWINKLER_SIMILARITY(CCN_NAME, EIN_NAME) jw FROM LIBRARY_MARTS.CORE.XWALK_HOSPITAL_CCN_EIN)
SELECT MATCH_TIER, COUNT(*) n, COUNT_IF(jw < 70) low_sim, MEDIAN(jw) med_jw,
       COUNT_IF(REGEXP_LIKE(EIN_NAME, '.*(MEDICAL STAFF|STAFF ASSOC|EMPLOYEE|CREDIT UNION|PHYSICIAN|AUXILIARY|FOUNDATION).*')) junk_like_ein_name,
       COUNT_IF(TRY_TO_NUMBER(SUBSTR(CCN, 3, 4)) BETWEEN 2000 AND 2299 AND jw < 70) ltch_low_sim,
       COUNT_IF(PROPRIETARY_NONPROFIT = 'P' AND jw < 70) forprofit_low_sim,
       ARRAY_SLICE(ARRAY_AGG(IFF(jw < 70, CCN || ' ' || PROPRIETARY_NONPROFIT || ' ' || CCN_NAME || ' => ' || EIN_NAME, NULL)) WITHIN GROUP (ORDER BY jw), 0, 20) low_sim_examples,
       ARRAY_AGG(IFF(LENGTH(CCN) <> 6, CCN, NULL)) odd_width_ccns
FROM x GROUP BY 1 ORDER BY 1

;

-- S13 Hospital units: letter CCNs (psych unit S, rehab unit T, swing beds U/W/Y/Z) vs their parent hospital in the source; is the for-profit flag the same on both?
WITH h AS (SELECT CCN, ANY_VALUE(PROPRIETARY_NONPROFIT) pn, COUNT(DISTINCT PROPRIETARY_NONPROFIT) pn_vals, ANY_VALUE(ORGANIZATION_NAME) nm
           FROM LIBRARY_RAW.LANDING.FED_CMS_HOSPITAL_ENROLLMENTS GROUP BY 1),
u AS (SELECT CCN, pn, nm, SUBSTR(CCN, 3, 1) letter, LEFT(CCN, 2) || IFF(SUBSTR(CCN, 3, 1) = 'Z', '1', '0') || SUBSTR(CCN, 4, 3) parent
      FROM h WHERE REGEXP_LIKE(CCN, '^[0-9]{2}[A-Z][0-9]{3}$')),
x AS (SELECT DISTINCT CCN FROM LIBRARY_MARTS.CORE.XWALK_HOSPITAL_CCN_EIN)
SELECT u.letter, COUNT(*) unit_ccns, COUNT_IF(p.CCN IS NOT NULL) parent_found, COUNT_IF(p.pn <> u.pn) pn_disagree,
       COUNT_IF(xu.CCN IS NOT NULL) units_in_xwalk, COUNT_IF(xu.CCN IS NOT NULL AND xp.CCN IS NOT NULL) unit_and_parent_in_xwalk,
       COUNT_IF(xu.CCN IS NOT NULL AND u.pn = 'P' AND p.pn = 'N') xwalk_units_P_parent_N,
       ANY_VALUE(k.all_ccns) source_ccns, ANY_VALUE(k.two_flags) source_ccns_with_two_flags, ANY_VALUE(k.x_nonstd) xwalk_ccns_not_6_digits,
       ARRAY_SLICE(ARRAY_AGG(IFF(p.pn <> u.pn, u.CCN || ' ' || u.pn || ' vs ' || p.CCN || ' ' || p.pn || ' ' || u.nm, NULL)), 0, 8) examples
FROM u LEFT JOIN h p ON p.CCN = u.parent
LEFT JOIN x xu ON xu.CCN = u.CCN LEFT JOIN x xp ON xp.CCN = u.parent
CROSS JOIN (SELECT (SELECT COUNT(*) FROM h) all_ccns, (SELECT COUNT_IF(pn_vals > 1) FROM h) two_flags,
                   (SELECT COUNT_IF(NOT REGEXP_LIKE(CCN, '^[0-9]{6}$')) FROM x) x_nonstd) k
GROUP BY 1 ORDER BY 2 DESC
;

-- S14 XWALK_HOSPITAL_CCN_EIN: do units and suffixed CCNs carry the same EIN as their parent hospital row in the table?
WITH x AS (SELECT CCN, EIN FROM LIBRARY_MARTS.CORE.XWALK_HOSPITAL_CCN_EIN),
k AS (SELECT CCN, EIN,
             CASE WHEN REGEXP_LIKE(CCN, '^[0-9]{6}$') THEN 'plain'
                  WHEN REGEXP_LIKE(CCN, '^[0-9]{2}[A-Z][0-9]{3}$') THEN 'unit_' || SUBSTR(CCN, 3, 1)
                  ELSE 'suffixed' END kind,
             CASE WHEN REGEXP_LIKE(CCN, '^[0-9]{2}[A-Z][0-9]{3}$')
                  THEN LEFT(CCN, 2) || IFF(SUBSTR(CCN, 3, 1) IN ('Z', 'M', 'R'), '1', '0') || SUBSTR(CCN, 4, 3)
                  WHEN NOT REGEXP_LIKE(CCN, '^[0-9]{6}$') THEN LEFT(CCN, 6) END parent
      FROM x)
SELECT IFF(GROUPING(k.kind) = 1, 'ALL', k.kind) kind, COUNT(*) ccns, COUNT_IF(p.CCN IS NOT NULL) parent_in_xwalk,
       COUNT_IF(p.EIN = k.EIN) same_ein_as_parent, COUNT_IF(p.CCN IS NOT NULL AND p.EIN <> k.EIN) other_ein,
       COUNT(DISTINCT k.EIN) eins
FROM k LEFT JOIN x p ON p.CCN = k.parent
GROUP BY ROLLUP (k.kind) ORDER BY 2 DESC
;

-- S15 Connecticut in the ZIP tables: CT ZIPs in the crosswalk vs CT rows in DIM_ZIP_POINT; which dot holds the most ZIPs
SELECT (SELECT COUNT(DISTINCT ZCTA5) FROM LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY WHERE STATE_USPS = 'CT') ct_zips_in_xwalk,
       (SELECT COUNT(*) FROM LIBRARY_MARTS.CORE.DIM_ZIP_POINT WHERE STATE_USPS = 'CT' OR STATE_FIPS = '09' OR PRIMARY_COUNTY_FIPS LIKE '09%') ct_rows_in_point,
       (SELECT PRIMARY_COUNTY_FIPS || ' ' || COUNTY_NAME || ' ' || COUNT(*) FROM LIBRARY_MARTS.CORE.DIM_ZIP_POINT GROUP BY PRIMARY_COUNTY_FIPS, COUNTY_NAME ORDER BY COUNT(*) DESC LIMIT 1) biggest_dot
;
