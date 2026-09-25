-- H15 time check: longest runs of trading days with the 10-year yield below the 3-month yield (inverted curve)
with r as (select try_to_date(SERIES_DESCRIPTION) d,
             try_to_double(MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_3_MONTH_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS) m3,
             try_to_double(MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_10_YEAR_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS) y10
           from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_FRB_H15_SELECTED_RATES),
s as (select d, m3, y10, iff(y10 < m3, 1, 0) inv from r where d is not null and m3 is not null and y10 is not null),
g as (select *, row_number() over (order by d) - row_number() over (partition by inv order by d) grp from s)
select min(d) start_d, max(d) end_d, count(*) trading_days, round(min(y10 - m3),2) deepest_pts,
  (select min(d) from s) series_start, (select count(*) from s) days_both
from g where inv = 1 group by grp
qualify row_number() over (order by count(*) desc) <= 6
order by trading_days desc
