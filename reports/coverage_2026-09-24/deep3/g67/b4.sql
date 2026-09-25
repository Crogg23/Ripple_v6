-- @house_ie_by_district
-- Outside money (independent expenditures) per House district, 2024 and 2026 cycles, superseded lines dropped: a contested-seat yardstick
SELECT FEC_ELECTION_YR, CAN_OFFICE_STATE, CAN_OFFICE_DIS, COUNT(*) n_lines,
       SUM(TRY_TO_DECIMAL(REPLACE(EXP_AMO, ',', ''), 16, 2)) ie_usd, COUNT_IF(TRY_TO_DECIMAL(REPLACE(EXP_AMO, ',', ''), 16, 2) IS NULL) bad_amt
FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES
WHERE CAN_OFFICE = 'H' AND FEC_ELECTION_YR IN (2024, 2026) AND COALESCE(IS_SUPERSEDED, FALSE) = FALSE
GROUP BY 1, 2, 3
