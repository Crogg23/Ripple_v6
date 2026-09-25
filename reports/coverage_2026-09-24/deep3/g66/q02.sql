-- H15 rates: is it clean? header rows, parse rate, duplicate dates, ND and blank counts, series start dates
with r as (
  select SERIES_DESCRIPTION d_txt, try_to_date(SERIES_DESCRIPTION) d,
    MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_1_MONTH_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS m1,
    MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_3_MONTH_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS m3,
    MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_2_YEAR_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS y2,
    MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_10_YEAR_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS y10,
    MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_20_YEAR_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS y20,
    MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_30_YEAR_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS y30
  from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_FRB_H15_SELECTED_RATES)
select count(*) n, count(d) parsed, count(distinct d) distinct_dates,
  listagg(distinct case when d is null then left(d_txt,40) end, ' || ') unparsed_vals,
  min(d) first_d, max(d) last_d,
  count_if(m3='ND') m3_nd, count_if(m3 is null or trim(m3)='') m3_blank, count_if(try_to_double(m3) is null and m3<>'ND' and trim(m3)<>'') m3_other,
  count_if(y10='ND') y10_nd, count_if(try_to_double(y10) is not null) y10_num,
  min(case when try_to_double(m1) is not null then d end) m1_start,
  min(case when try_to_double(y20) is not null then d end) y20_start,
  count_if(d between '1987-01-01' and '1993-09-30' and try_to_double(y20) is null) y20_gap_rows,
  count_if(d between '2002-03-01' and '2006-01-31' and try_to_double(y30) is null) y30_gap_rows,
  count_if(dayofweekiso(d) in (6,7)) weekend_rows,
  count_if(try_to_double(m3) < 0 or try_to_double(y10) < 0) negative_rows,
  max(try_to_double(y10)) y10_max, min(try_to_double(y10)) y10_min
from r
