-- @house_ie_general_only
-- Same as S12 but split by election type, so general-election outside money (swing seats) is apart from primary fights
WITH b AS (
  SELECT CYCLE_FILE, CAN_OFFICE_STATE, CAN_OFFICE_DIS, LEFT(ELE_TYPE, 1) ele, TRY_TO_DOUBLE(EXP_AMO) amt
  FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES
  WHERE NOT (IS_SUPERSEDED::string ILIKE 'true') AND CYCLE_FILE IN (2022, 2024) AND LEFT(CAND_ID, 1) = 'H')
SELECT CYCLE_FILE, CAN_OFFICE_STATE, CAN_OFFICE_DIS, ele, COUNT(*) n_lines, SUM(IFF(amt < 5e6, amt, 0)) ie_usd, COUNT_IF(amt >= 5e6) n_huge
FROM b GROUP BY 1, 2, 3, 4
