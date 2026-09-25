-- CFTC time check: rows, report dates and markets per year. Looks for gaps, the separately loaded 2024, and where 2026 stops.
select year(AS_OF_DATE_IN_FORM_YYYY_MM_DD) yr, count(*) n, count(distinct AS_OF_DATE_IN_FORM_YYYY_MM_DD) dates,
  count(distinct trim(CFTC_CONTRACT_MARKET_CODE)) markets, round(count(*)/count(distinct AS_OF_DATE_IN_FORM_YYYY_MM_DD),0) mkts_per_date,
  min(AS_OF_DATE_IN_FORM_YYYY_MM_DD) first_d, max(AS_OF_DATE_IN_FORM_YYYY_MM_DD) last_d,
  count(distinct CFTC_MARKET_CODE_IN_INITIALS) exchanges,
  median(try_to_number(trim(TRADERS_TOTAL_ALL))) med_traders
from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_CFTC_COT_FUTURES
group by 1 order by 1
