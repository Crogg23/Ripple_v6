-- CFTC futures profile: duplicates, keys, dates, impossible percentages (>100), text-number parse rate
with f as (select *, hash(*) h from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_CFTC_COT_FUTURES)
select count(*) n, count(distinct h) distinct_rows,
  count(distinct trim(CFTC_CONTRACT_MARKET_CODE)||'|'||AS_OF_DATE_IN_FORM_YYYY_MM_DD) code_date,
  count(distinct trim(CFTC_CONTRACT_MARKET_CODE)) codes, count(distinct MARKET_AND_EXCHANGE_NAMES) names,
  min(AS_OF_DATE_IN_FORM_YYYY_MM_DD) d0, max(AS_OF_DATE_IN_FORM_YYYY_MM_DD) d1,
  count_if(AS_OF_DATE_IN_FORM_YYMMDD <> AS_OF_DATE_IN_FORM_YYYY_MM_DD) date_cols_disagree,
  count_if(trim(CFTC_CONTRACT_MARKET_CODE) <> trim(CFTC_CONTRACT_MARKET_CODE_QUOTES)) code_cols_disagree,
  count_if(CONCENTRATION_GROSS_LT_4_TDR_SHORT_ALL > 100) g4s_over100, count_if(CONCENTRATION_GROSS_LT_4_TDR_LONG_ALL > 100) g4l_over100,
  count_if(CONCENTRATION_NET_LT_8_TDR_SHORT_ALL > 100) n8s_over100,
  count_if(greatest(CONCENTRATION_GROSS_LT_4_TDR_SHORT_ALL,CONCENTRATION_GROSS_LT_4_TDR_LONG_ALL,CONCENTRATION_GROSS_LT_8_TDR_SHORT_ALL,CONCENTRATION_GROSS_LT_8_TDR_LONG_ALL) > 100) any_gross_over100,
  count_if(CONCENTRATION_GROSS_LT_4_TDR_SHORT_ALL is null) g4s_null,
  count_if(try_to_number(trim(OPEN_INTEREST_ALL)) is null) oi_unparsed, count_if(try_to_number(trim(TRADERS_TOTAL_ALL)) is null) traders_unparsed,
  count_if(try_to_number(trim(OPEN_INTEREST_ALL)) = 0) oi_zero,
  count_if(dayofweekiso(AS_OF_DATE_IN_FORM_YYYY_MM_DD) <> 2) not_tuesday,
  count_if(CONCENTRATION_GROSS_LT_4_TDR_SHORT_ALL < CONCENTRATION_NET_LT_4_TDR_SHORT_ALL) net_gt_gross
from f
