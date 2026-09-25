-- Debt cliff: profile. Years, aggregates, cliff flag, peak flag, sample of the 22 cliff rows
select 'profile' k, count(*)::text a, count(distinct COUNTRY_CODE)::text b, min(DATA_YEAR)::text c, max(DATA_YEAR)::text d,
  count_if(IS_AGGREGATE)::text e, count_if(IS_REPAYMENT_CLIFF)::text f, count_if(IS_PEAK_SERVICE_YEAR)::text g,
  count_if(TOTAL_DEBT_SERVICE_USD is null)::text h, count_if(abs(TOTAL_DEBT_SERVICE_USD - PRINCIPAL_REPAYMENT_USD - INTEREST_PAYMENT_USD) > 1e6)::text i,
  count(distinct COUNTRY_YEAR_ID)::text j
from LIBRARY_MARTS.MONEY_FINANCE.MONEY__DEBT_REPAYMENT_CLIFF
union all
select 'year', DATA_YEAR::text, count(*)::text, count_if(IS_AGGREGATE)::text, count_if(IS_REPAYMENT_CLIFF)::text, count_if(IS_PEAK_SERVICE_YEAR)::text,
  round(sum(iff(IS_AGGREGATE,0,TOTAL_DEBT_SERVICE_USD))/1e9,1)::text, null,null,null,null
from LIBRARY_MARTS.MONEY_FINANCE.MONEY__DEBT_REPAYMENT_CLIFF group by 2
union all
select 'cliff', COUNTRY_CODE||' '||COUNTRY_NAME, DATA_YEAR::text, round(TOTAL_DEBT_SERVICE_USD/1e9,2)::text, round(PREV_YEAR_TOTAL_DEBT_SERVICE_USD/1e9,2)::text,
  round(YOY_CHANGE_PCT,2)::text, IS_AGGREGATE::text, IS_PEAK_SERVICE_YEAR::text, round(PRINCIPAL_SHARE_OF_SERVICE,2)::text, null, null
from LIBRARY_MARTS.MONEY_FINANCE.MONEY__DEBT_REPAYMENT_CLIFF where IS_REPAYMENT_CLIFF
