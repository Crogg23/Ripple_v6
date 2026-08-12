-- Q7b: state ranking of chronic (8+ quarters) noncompliance with zero formal enforcement
SELECT STATE,
  COUNT(*) facilities_total,
  SUM(IFF(QUARTERS_WITH_NONCOMPLIANCE>=8,1,0)) chronic_8plus,
  SUM(IFF(QUARTERS_WITH_NONCOMPLIANCE>=8 AND FORMAL_ACTION_COUNT=0,1,0)) chronic_zero_enforcement,
  ROUND(100*chronic_zero_enforcement/NULLIF(chronic_8plus,0),1) pct_chronic_unenforced
FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO
WHERE QUARTERS_WITH_NONCOMPLIANCE IS NOT NULL AND STATE IS NOT NULL AND STATE<>'' AND STATE<>'nan'
GROUP BY 1 HAVING chronic_8plus>=50 ORDER BY chronic_zero_enforcement DESC
