-- Q5 Part B: active community / non-transient systems (the ones the Lead & Copper
-- Rule applies to) with NO lead or copper samples in the loaded LCR sample data.
WITH sampled AS (
  SELECT DISTINCT PWSID FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_LCR_SAMPLES)
SELECT p.STATE_CODE state,
  COUNT(*) systems_never_sampled,
  SUM(p.POPULATION_SERVED_COUNT) population_served,
  SUM(IFF(p.PWS_TYPE_CODE='CWS',1,0)) community_systems
FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS p
LEFT JOIN sampled s ON s.PWSID=p.PWSID
WHERE p.PWS_ACTIVITY_CODE='A' AND p.PWS_TYPE_CODE IN ('CWS','NTNCWS') AND s.PWSID IS NULL
GROUP BY 1 ORDER BY population_served DESC
