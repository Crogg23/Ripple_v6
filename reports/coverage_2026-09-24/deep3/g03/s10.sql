-- S10 Open Payments PY2024 x profile roster on profile ID: do blank-NPI payment rows recover an NPI, and do NPIs agree?
WITH p AS (
  SELECT NULLIF(TRIM(npi),'') npi, covered_recipient_profile_id::string pid, total_amount_of_payment_usdollars amt
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS
  WHERE covered_recipient_type NOT ILIKE '%Teaching Hospital%'),
r AS (SELECT profile_id::string pid, NULLIF(TRIM(npi),'') npi FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_PROFILE_SUPPLEMENT)
SELECT IFF(p.npi IS NULL,'pay_npi_blank','pay_npi_present') side,
       COUNT(*) rows_, ROUND(SUM(p.amt)) dollars, COUNT_IF(p.pid IS NULL OR p.pid='') pid_blank,
       COUNT_IF(r.pid IS NOT NULL) pid_landed, COUNT_IF(r.npi IS NOT NULL) roster_has_npi,
       ROUND(SUM(IFF(p.npi IS NULL AND r.npi IS NOT NULL, p.amt, 0))) recovered_dollars,
       COUNT_IF(p.npi IS NOT NULL AND r.npi IS NOT NULL AND p.npi<>r.npi) npi_disagree,
       COUNT(DISTINCT IFF(p.npi IS NULL AND r.npi IS NOT NULL, r.npi, NULL)) recovered_npis
FROM p LEFT JOIN r ON r.pid = p.pid
GROUP BY 1
