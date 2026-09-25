-- S13 CourtListener Supreme Court dockets by filing year and the kind of court appealed from (state vs federal), with cert grants and denials: tests whether state-court petitions fell or only grants did
WITH d AS (
  SELECT YEAR(TRY_TO_DATE(DATE_FILED::string)) y, NULLIF(TRIM(APPEAL_FROM_ID),'') af,
         NULLIF(TRIM(DATE_CERT_GRANTED::string),'') g, NULLIF(TRIM(DATE_CERT_DENIED::string),'') dn
  FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS
  WHERE COURT_ID = 'scotus')
SELECT d.y, CASE WHEN d.af IS NULL THEN 'blank' WHEN c.JURISDICTION LIKE 'S%' THEN 'state' WHEN c.JURISDICTION LIKE 'F%' THEN 'federal' ELSE 'other:'||COALESCE(c.JURISDICTION,'?') END kind,
       COUNT(*) n, COUNT(d.g) granted, COUNT(d.dn) denied
FROM d LEFT JOIN LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_COURTS c ON c.ID = d.af
WHERE d.y >= 2000 OR d.y IS NULL
GROUP BY 1,2 ORDER BY 1,2;
