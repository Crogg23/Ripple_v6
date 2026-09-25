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

-- S12 XWALK_HOSPITAL_CCN_EIN: does the matched IRS name look like the hospital? Jaro-Winkler by tier, junk-entity names, odd-width CCNs
WITH x AS (SELECT *, JAROWINKLER_SIMILARITY(CCN_NAME, EIN_NAME) jw FROM LIBRARY_MARTS.CORE.XWALK_HOSPITAL_CCN_EIN)
SELECT MATCH_TIER, COUNT(*) n, COUNT_IF(jw < 70) low_sim, MEDIAN(jw) med_jw,
       COUNT_IF(REGEXP_LIKE(EIN_NAME, '.*(MEDICAL STAFF|STAFF ASSOC|EMPLOYEE|CREDIT UNION|PHYSICIAN|AUXILIARY|FOUNDATION).*')) junk_like_ein_name,
       COUNT_IF(TRY_TO_NUMBER(SUBSTR(CCN, 3, 4)) BETWEEN 2000 AND 2299 AND jw < 70) ltch_low_sim,
       COUNT_IF(PROPRIETARY_NONPROFIT = 'P' AND jw < 70) forprofit_low_sim,
       ARRAY_SLICE(ARRAY_AGG(IFF(jw < 70, CCN || ' ' || PROPRIETARY_NONPROFIT || ' ' || CCN_NAME || ' => ' || EIN_NAME, NULL)) WITHIN GROUP (ORDER BY jw), 0, 20) low_sim_examples,
       ARRAY_AGG(IFF(LENGTH(CCN) <> 6, CCN, NULL)) odd_width_ccns
FROM x GROUP BY 1 ORDER BY 1

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
