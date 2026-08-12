-- Q7a: distribution of facilities by quarters-in-noncompliance (3yr window, max 12)
-- split by whether ANY formal enforcement action exists
SELECT
  CASE WHEN QUARTERS_WITH_NONCOMPLIANCE=0 THEN '0'
       WHEN QUARTERS_WITH_NONCOMPLIANCE<=3 THEN '1-3'
       WHEN QUARTERS_WITH_NONCOMPLIANCE<=7 THEN '4-7'
       WHEN QUARTERS_WITH_NONCOMPLIANCE<=11 THEN '8-11'
       ELSE '12 (entire 3 years)' END qnc_bucket,
  IFF(FORMAL_ACTION_COUNT>0,'has formal enforcement','zero formal enforcement') enforcement,
  COUNT(*) facilities,
  AVG(INFORMAL_ACTION_COUNT) avg_informal_actions,
  SUM(IFF(TOTAL_PENALTIES>0,1,0)) facilities_with_any_penalty
FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO
WHERE QUARTERS_WITH_NONCOMPLIANCE IS NOT NULL
GROUP BY 1,2 ORDER BY 1,2
-- Q7b: state ranking of chronic (8+ quarters) noncompliance with zero formal enforcement
SELECT STATE,
  COUNT(*) facilities_total,
  SUM(IFF(QUARTERS_WITH_NONCOMPLIANCE>=8,1,0)) chronic_8plus,
  SUM(IFF(QUARTERS_WITH_NONCOMPLIANCE>=8 AND FORMAL_ACTION_COUNT=0,1,0)) chronic_zero_enforcement,
  ROUND(100*chronic_zero_enforcement/NULLIF(chronic_8plus,0),1) pct_chronic_unenforced
FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO
WHERE QUARTERS_WITH_NONCOMPLIANCE IS NOT NULL AND STATE IS NOT NULL AND STATE<>'' AND STATE<>'nan'
GROUP BY 1 HAVING chronic_8plus>=50 ORDER BY chronic_zero_enforcement DESC
