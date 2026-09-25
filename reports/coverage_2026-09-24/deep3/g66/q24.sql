-- H15 check: the Treasury sold no 30-year bonds from Feb 2002 to Feb 2006, yet q02 found only 43 empty 30-year rows in that window.
-- Is the 30-year column really the 30-year? Per year 2000-2007: numeric count, ND count, blank count, average 20y and 30y.
with r as (select try_to_date(SERIES_DESCRIPTION) d,
             MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_20_YEAR_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS y20,
             MARKET_YIELD_ON_U_S_TREASURY_SECURITIES_AT_30_YEAR_CONSTANT_MATURITY_QUOTED_ON_INVESTMENT_BASIS y30
           from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_FRB_H15_SELECTED_RATES)
select year(d) yr, count(*) n, count_if(try_to_double(y30) is not null) y30_num, count_if(y30 = 'ND') y30_nd,
  count_if(y30 is null or trim(y30) = '') y30_blank, round(avg(try_to_double(y20)),2) avg_y20, round(avg(try_to_double(y30)),2) avg_y30,
  min(iff(try_to_double(y30) is null and (y30 is null or trim(y30)=''), d, null)) first_blank_30, max(iff(try_to_double(y30) is null and (y30 is null or trim(y30)=''), d, null)) last_blank_30
from r where d between '2000-01-01' and '2007-12-31' group by 1 order by 1
