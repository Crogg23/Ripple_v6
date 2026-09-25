-- CFTC time detail: PJM Western Hub day-ahead peak and off-peak futures (ICE), by quarter 2023 - 2026.
-- Top-4 share of the short side, open interest, number of traders, number of big commercial shorts.
select trim(CFTC_CONTRACT_MARKET_CODE) code, left(any_value(MARKET_AND_EXCHANGE_NAMES),45) nm,
  year(AS_OF_DATE_IN_FORM_YYYY_MM_DD) || 'Q' || quarter(AS_OF_DATE_IN_FORM_YYYY_MM_DD) q, count(*) wks,
  round(avg(CONCENTRATION_GROSS_LT_4_TDR_SHORT_ALL),1) g4s, round(avg(CONCENTRATION_GROSS_LT_8_TDR_SHORT_ALL),1) g8s,
  round(avg(CONCENTRATION_NET_LT_4_TDR_SHORT_ALL),1) n4s, round(avg(CONCENTRATION_GROSS_LT_4_TDR_LONG_ALL),1) g4l,
  round(avg(try_to_number(trim(OPEN_INTEREST_ALL))),0) oi, round(avg(try_to_number(trim(TRADERS_TOTAL_ALL))),0) traders,
  round(avg(try_to_number(trim(TRADERS_COMMERCIAL_SHORT_ALL))),1) comm_short_traders,
  round(avg(try_to_double(trim(OF_OI_COMMERCIAL_SHORT_ALL))),1) pct_comm_short
from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_CFTC_COT_FUTURES
where trim(CFTC_CONTRACT_MARKET_CODE) in ('0643DB','0643DC') and AS_OF_DATE_IN_FORM_YYYY_MM_DD >= '2023-01-01'
group by 1, 3 order by 1, 3
