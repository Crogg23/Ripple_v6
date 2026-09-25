-- @eoir_detained_date_fill_by_case_id_band
-- Dull-explanation test: did EOIR start filling DATE_DETAINED more often? Fill rate among detained/released-custody cases by case-number band (a proxy for when the case was opened, see S09).
SELECT FLOOR(CASE_ID / 500000) * 500000 band, COUNT(*) n,
       COUNT_IF(CUSTODY IN ('D','R')) dr, COUNT_IF(CUSTODY IN ('D','R') AND DATE_DETAINED IS NOT NULL) dr_det_filled,
       COUNT_IF(CUSTODY IN ('D','R') AND DATE_OF_ENTRY IS NOT NULL) dr_entry_filled,
       COUNT_IF(CUSTODY = 'N' AND DATE_DETAINED IS NOT NULL) n_with_det
FROM LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EOIR_CASES
WHERE CASE_ID >= 9000000
GROUP BY 1 ORDER BY 1
