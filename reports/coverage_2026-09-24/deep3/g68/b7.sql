-- @ice_stints_corroborate_by_month
-- Second source for the EOIR lead: ICE detention stays by book-in month, split by entry date (fixed cohort: entered by 2021-12-31) and book-in criminality.
WITH s AS (
  SELECT STAY_ID, TRY_TO_DATE(LEFT(STAY_BOOK_IN_AT::VARCHAR, 10)) bi, TRY_TO_DATE(LEFT(ENTRY_DATE::VARCHAR, 10)) ent,
         ENTRY_DATE IS NOT NULL AND TRIM(ENTRY_DATE::VARCHAR) <> '' ent_raw, BOOK_IN_CRIMINALITY crim
  FROM LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_STINTS)
SELECT DATE_TRUNC('month', bi)::DATE mon, COUNT(DISTINCT STAY_ID) stays,
       COUNT(DISTINCT IFF(ent_raw, STAY_ID, NULL)) stays_entry_raw, COUNT(DISTINCT IFF(ent IS NOT NULL, STAY_ID, NULL)) stays_entry_parsed,
       COUNT(DISTINCT IFF(ent <= '2021-12-31', STAY_ID, NULL)) stays_entered_by_2021,
       COUNT(DISTINCT IFF(ent < '2006-01-01', STAY_ID, NULL)) stays_entered_pre2006,
       COUNT(DISTINCT IFF(ent <= '2021-12-31' AND crim ILIKE '%other%', STAY_ID, NULL)) by2021_other_violator,
       COUNT(DISTINCT IFF(ent <= '2021-12-31' AND crim ILIKE '%convicted%', STAY_ID, NULL)) by2021_convicted,
       COUNT(DISTINCT IFF(crim ILIKE '%other%', STAY_ID, NULL)) all_other_violator,
       ANY_VALUE(crim) crim_example
FROM s
WHERE bi >= '2023-01-01'
GROUP BY 1 ORDER BY 1
