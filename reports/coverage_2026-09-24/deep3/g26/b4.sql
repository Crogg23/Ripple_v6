-- @icis_sector_by_year
with c as (
  select case_number, try_to_number(substr(case_number, 4, 4)) yr,
         case
           when left(primary_sic_code, 2) = '13' or left(primary_naics_code, 3) = '211' then 'oil_gas_extraction'
           when left(primary_sic_code, 2) = '29' or left(primary_naics_code, 3) = '324' then 'refining'
           when left(primary_sic_code, 3) = '491' or left(primary_naics_code, 4) = '2211' then 'power'
           when left(primary_sic_code, 3) in ('494', '495') or left(primary_naics_code, 4) in ('2213', '5622') then 'water_sewer_waste'
           when left(primary_sic_code, 2) = '28' or left(primary_naics_code, 3) = '325' then 'chemicals'
           when left(primary_sic_code, 1) in ('2', '3') or left(primary_naics_code, 2) in ('31', '32', '33') then 'other_mfg'
           when nullif(primary_sic_code, '') is null and nullif(primary_naics_code, '') is null then 'no_code'
           else 'other'
         end sector
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_EPA_ICIS_FEC_CASE_FACILITIES
  where try_to_number(substr(case_number, 4, 4)) between 2012 and 2026)
select yr, sector, count(distinct case_number) cases
from c group by 1, 2 order by 2, 1;
