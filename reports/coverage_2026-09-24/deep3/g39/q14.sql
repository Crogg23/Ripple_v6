-- Verify in the warehouse: null-CO2e rows vs the facility's reporting status that year; sum split supplier vs direct
with e as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_GHGRP_EMISSION),
f as (select FACILITY_ID, REPORTING_YEAR, max(nullif(trim(REPORTING_STATUS),'')) st from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_GHGRP_FACILITY group by 1,2)
select coalesce(f.st,'(reported)') status, iff(e.GAS_ID is null,'gas null','gas set') gas, count(*) n, count_if(e.CO2E_EMISSION is null) co2e_null,
  round(sum(iff(e.SECTOR_ID in (10,11,12,13,16), e.CO2E_EMISSION, 0))/1e9,2) supplier_bt, round(sum(e.CO2E_EMISSION)/1e9,2) all_bt
from e left join f on f.FACILITY_ID = e.FACILITY_ID and f.REPORTING_YEAR = e.REPORTING_YEAR
group by 1,2 order by 1,2
