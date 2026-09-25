-- NRC name variants: every spelling containing NORFOLK SOUTHERN, COX, TARGA per year in the main copy 2017-2025,
-- to test whether the company-level breaks in the secondary copy are real or name drift
with m as (select upper(trim(RESPONSIBLE_COMPANY)) co, year(DATE_TIME_RECEIVED) y
           from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_USCG_NRC_INCIDENTS
           where year(DATE_TIME_RECEIVED) between 2017 and 2025
             and (RESPONSIBLE_COMPANY ilike '%NORFOLK SOUTHERN%' or RESPONSIBLE_COMPANY ilike 'COX %' or RESPONSIBLE_COMPANY ilike '%TARGA%')),
m2 as (select case when co like '%NORFOLK%' then 'NS' when co like '%TARGA%' then 'TARGA' else 'COX' end fam, co, y from m)
select fam, co,
  count_if(y = 2017) y17, count_if(y = 2018) y18, count_if(y = 2019) y19, count_if(y = 2020) y20, count_if(y = 2021) y21,
  count_if(y = 2022) y22, count_if(y = 2023) y23, count_if(y = 2024) y24, count_if(y = 2025) y25, count(*) tot
from m2 group by rollup(fam, co) having count(*) >= 5 order by fam, tot desc;
