-- Q3a: top 30 parents by total toxic releases (pounds) across their 2023 TRI
-- facility portfolio, with facility counts and ECHO compliance/enforcement stats.
-- Parent = TRI's EPA-standardized parent company name (C_17); grams converted to lbs.
WITH fac AS (
  SELECT UPPER(C_17_STANDARD_PARENT_CO_NAME) parent,
         C_3_FRS_ID frs_id,
         SUM(IFF(C_50_UNIT_OF_MEASURE='Grams', C_107_TOTAL_RELEASES/453.592, C_107_TOTAL_RELEASES)) rel_lbs
  FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023
  WHERE C_17_STANDARD_PARENT_CO_NAME IS NOT NULL AND C_17_STANDARD_PARENT_CO_NAME NOT IN ('','nan','NA')
  GROUP BY 1,2)
SELECT f.parent,
  COUNT(DISTINCT f.frs_id) facilities,
  SUM(f.rel_lbs) total_release_lbs,
  SUM(e.QUARTERS_WITH_NONCOMPLIANCE) total_noncompliance_quarters,
  SUM(IFF(e.QUARTERS_WITH_NONCOMPLIANCE>=8,1,0)) chronic_noncompliant_facilities,
  SUM(e.FORMAL_ACTION_COUNT) formal_actions,
  SUM(e.TOTAL_PENALTIES) total_epa_penalties_usd
FROM fac f
LEFT JOIN LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO e ON e.FRS_ID=f.frs_id
GROUP BY 1 ORDER BY total_release_lbs DESC LIMIT 30
-- Q3b: facilities whose matched owner LEI filed a GLEIF reporting exception
-- (refused to name a parent) vs owners with a named parent relationship.
WITH xw AS (
  SELECT DISTINCT EPA_REGISTRY_ID, MATCHED_LEI
  FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK
  WHERE MATCHED_LEI IS NOT NULL AND MATCHED_LEI NOT IN ('','nan')),
repex AS (SELECT DISTINCT LEI FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_GLEIF_REPEX),
rel AS (
  SELECT DISTINCT RELATIONSHIP_STARTNODE_NODEID lei
  FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_GLEIF_RELATIONSHIPS
  WHERE RELATIONSHIP_RELATIONSHIPTYPE IN ('IS_ULTIMATELY_CONSOLIDATED_BY','IS_DIRECTLY_CONSOLIDATED_BY')),
tri AS (
  SELECT C_3_FRS_ID frs_id,
    SUM(IFF(C_50_UNIT_OF_MEASURE='Grams', C_107_TOTAL_RELEASES/453.592, C_107_TOTAL_RELEASES)) rel_lbs
  FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023 GROUP BY 1)
SELECT
  CASE WHEN r.LEI IS NOT NULL AND p.lei IS NULL THEN 'exception only (refused to name parent)'
       WHEN p.lei IS NOT NULL AND r.LEI IS NULL THEN 'named parent only'
       WHEN p.lei IS NOT NULL AND r.LEI IS NOT NULL THEN 'both (partial exception)'
       ELSE 'neither on file' END owner_transparency,
  COUNT(DISTINCT x.EPA_REGISTRY_ID) facilities,
  COUNT(DISTINCT t.frs_id) tri_facilities,
  AVG(t.rel_lbs) avg_release_lbs_per_tri_facility,
  AVG(e.QUARTERS_WITH_NONCOMPLIANCE) avg_noncompliance_quarters,
  AVG(e.FORMAL_ACTION_COUNT) avg_formal_actions,
  AVG(e.TOTAL_PENALTIES) avg_penalties_usd
FROM xw x
LEFT JOIN repex r ON r.LEI=x.MATCHED_LEI
LEFT JOIN rel p ON p.lei=x.MATCHED_LEI
LEFT JOIN tri t ON t.frs_id=x.EPA_REGISTRY_ID
LEFT JOIN LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO e ON e.FRS_ID=x.EPA_REGISTRY_ID
GROUP BY 1 ORDER BY facilities DESC
