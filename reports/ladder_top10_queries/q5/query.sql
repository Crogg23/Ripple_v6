-- Q5 Part A: active systems whose lead 90th-percentile samples exceeded the
-- 15 ppb (0.015 mg/L) action level, but with ZERO Lead & Copper Rule (rule 350)
-- violations on file. Aggregated by state with population served.
WITH lead_exceed AS (
  SELECT PWSID, MAX(SAMPLE_MEASURE) max_pb90, COUNT(*) n_exceed_samples
  FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_LCR_SAMPLES
  WHERE CONTAMINANT_CODE='PB90' AND SAMPLE_MEASURE > 0.015
  GROUP BY 1),
lcr_viol AS (
  SELECT DISTINCT PWSID
  FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT
  WHERE RULE_CODE='350' OR CONTAMINANT_CODE IN ('1030','PB90'))
SELECT p.STATE_CODE state,
  COUNT(*) systems_exceeding_no_violation,
  SUM(p.POPULATION_SERVED_COUNT) population_served,
  AVG(e.max_pb90)*1000 avg_max_lead_ppb,
  MAX(e.max_pb90)*1000 worst_lead_ppb
FROM lead_exceed e
JOIN LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS p
  ON p.PWSID=e.PWSID AND p.PWS_ACTIVITY_CODE='A'
LEFT JOIN lcr_viol v ON v.PWSID=e.PWSID
WHERE v.PWSID IS NULL
GROUP BY 1 ORDER BY population_served DESC
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
