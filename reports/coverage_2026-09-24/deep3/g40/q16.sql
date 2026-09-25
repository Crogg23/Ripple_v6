-- (second rerun of q14: Kuwaiti Oil Fires has a zero base year; every division now zero-safe) OWID CO2 time check:
-- countries only (3-letter code), top 20 emitters in 2024, change vs 2019, 2023 and 2005; world and sum-of-countries for the double-count test
with o as (select ENTITY, CODE, try_to_number(YEAR) y, try_to_double(ANNUAL_CO_EMISSIONS) x from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__XC_OWID_CO2),
c as (select ENTITY, CODE, max(iff(y=2024,x,null)) e24, max(iff(y=2023,x,null)) e23, max(iff(y=2019,x,null)) e19, max(iff(y=2005,x,null)) e05
      from o where length(CODE)=3 group by 1,2),
w as (select ENTITY, max(iff(y=2024,x,null)) e24, max(iff(y=2023,x,null)) e23, max(iff(y=2019,x,null)) e19, max(iff(y=2005,x,null)) e05
      from o where CODE='OWID_WRL' or ENTITY in ('International aviation','International shipping','Kuwaiti Oil Fires (GCP)') group by 1)
select * from (select 'top' k, ENTITY, round(e24/1e6,1) mt24, round(100*(e24/nullif(e19,0)-1),1) pct_vs19, round(100*(e24/nullif(e23,0)-1),1) pct_vs23, round(100*(e24/nullif(e05,0)-1),1) pct_vs05 from c where e24 is not null order by e24 desc limit 20)
union all select 'sum_countries', count(*)::text, round(sum(e24)/1e6,1), null, null, null from c where e24 is not null
union all select 'world_or_bunker', ENTITY, round(e24/1e6,1), round(100*(e24/nullif(e19,0)-1),1), round(100*(e24/nullif(e23,0)-1),1), round(100*(e24/nullif(e05,0)-1),1) from w
