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
