-- @house_ie_by_district_v2
-- Retry of S11 (0 rows: FEC_ELECTION_YR/IS_SUPERSEDED filters did not match). Uses CYCLE_FILE and the string test other reports use.
-- Lines of $5M+ counted apart: the table carries typo-sized amounts.
WITH b AS (
  SELECT CYCLE_FILE, CAN_OFFICE_STATE, CAN_OFFICE_DIS, TRY_TO_DOUBLE(EXP_AMO) amt
  FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES
  WHERE NOT (IS_SUPERSEDED::string ILIKE 'true') AND CYCLE_FILE IN (2022, 2024, 2026) AND LEFT(CAND_ID, 1) = 'H')
SELECT CYCLE_FILE, CAN_OFFICE_STATE, CAN_OFFICE_DIS, COUNT(*) n_lines,
       SUM(IFF(amt < 5e6, amt, 0)) ie_usd, COUNT_IF(amt >= 5e6) n_huge, SUM(IFF(amt >= 5e6, amt, 0)) huge_usd
FROM b GROUP BY 1, 2, 3
