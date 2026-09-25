-- Verify in the warehouse: direct CO2e (no supplier sectors 9-13,16,17, no biogenic gas 8) for LNG terminals, 2015 vs 2023, and Sabine Pass's growth rank among facilities reporting both years
with d as (
  select FACILITY_ID, REPORTING_YEAR, sum(CO2E_EMISSION) t
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_GHGRP_EMISSION
  where SECTOR_ID not in (9,10,11,12,13,16,17) and coalesce(GAS_ID,0) <> 8 and CO2E_EMISSION is not null
  group by 1,2),
w as (select FACILITY_ID, sum(iff(REPORTING_YEAR=2015,t,0)) y15, sum(iff(REPORTING_YEAR=2023,t,0)) y23 from d group by 1),
r as (select FACILITY_ID, y15, y23, y23-y15 chg, rank() over (order by y23-y15 desc) rk, count(*) over () n_both from w where y15>0 and y23>0)
select 'lng_all' k, count(*) n, round(sum(w.y15)/1e6,2) a, round(sum(w.y23)/1e6,2) b, null rk
from w where FACILITY_ID in ('1002259','1013179','1014135','1013553','1005420','1013753','1006016')
union all
select 'sabine', n_both, round(y15/1e6,2), round(y23/1e6,2), rk from r where FACILITY_ID = '1002259'
union all
select 'next_'||FACILITY_ID, n_both, round(y15/1e6,2), round(y23/1e6,2), rk from r where rk between 2 and 3
