-- CFTC verification: (1) full-history record check for the two PJM Western Hub day-ahead contracts, back to their first report;
-- (2) why CFTC_COMMODITY_CODE = '064' matched nothing: the raw stored values for power rows.
select 'pjm' k, trim(CFTC_CONTRACT_MARKET_CODE) code, min(AS_OF_DATE_IN_FORM_YYYY_MM_DD)::text first_d, max(AS_OF_DATE_IN_FORM_YYYY_MM_DD)::text last_d,
  count(*)::text wks,
  max(iff(AS_OF_DATE_IN_FORM_YYYY_MM_DD < '2016-01-01', CONCENTRATION_GROSS_LT_4_TDR_SHORT_ALL, null))::text max_pre2016,
  max(iff(AS_OF_DATE_IN_FORM_YYYY_MM_DD between '2016-01-01' and '2025-12-31', CONCENTRATION_GROSS_LT_4_TDR_SHORT_ALL, null))::text max_2016_2025,
  max(iff(AS_OF_DATE_IN_FORM_YYYY_MM_DD >= '2026-01-01', CONCENTRATION_GROSS_LT_4_TDR_SHORT_ALL, null))::text max_2026,
  max_by(AS_OF_DATE_IN_FORM_YYYY_MM_DD, CONCENTRATION_GROSS_LT_4_TDR_SHORT_ALL)::text date_of_max,
  count_if(AS_OF_DATE_IN_FORM_YYYY_MM_DD >= '2026-01-01' and CONCENTRATION_GROSS_LT_4_TDR_SHORT_ALL > 65)::text wks_2026_over65,
  count_if(AS_OF_DATE_IN_FORM_YYYY_MM_DD < '2025-01-01' and CONCENTRATION_GROSS_LT_4_TDR_SHORT_ALL > 65)::text wks_pre2025_over65
from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_CFTC_COT_FUTURES
where trim(CFTC_CONTRACT_MARKET_CODE) in ('0643DB','0643DC')
group by 2
union all
select 'code_raw', '[' || CFTC_COMMODITY_CODE || ']', length(CFTC_COMMODITY_CODE)::text, count(*)::text, min(left(trim(CFTC_CONTRACT_MARKET_CODE),3)), null, null, null, null, null, null
from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_CFTC_COT_FUTURES
where left(trim(CFTC_CONTRACT_MARKET_CODE),3) = '064' or try_to_number(trim(CFTC_COMMODITY_CODE)) = 64
group by 2, 3
