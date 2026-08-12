-- Q1b: state ranking of penalty dollars per facility
WITH pen AS (
  SELECT CMS_CERTIFICATION_NUMBER_CCN ccn, SUM(FINE_AMOUNT) fine_usd, COUNT(*) n_pen
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES GROUP BY 1)
SELECT r.STATE, COUNT(*) facilities,
  SUM(COALESCE(p.fine_usd,0)) total_penalty_usd,
  SUM(COALESCE(p.fine_usd,0))/COUNT(*) penalty_usd_per_facility,
  AVG(r.OVERALL_RATING) avg_rating
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME r
LEFT JOIN pen p ON p.ccn=r.CMS_CERTIFICATION_NUMBER_CCN
GROUP BY 1 ORDER BY penalty_usd_per_facility DESC
