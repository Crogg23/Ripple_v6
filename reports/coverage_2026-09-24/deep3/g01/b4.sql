-- @estab_x_epa_eto
with eto as (
  select registry_id, pgm_sys_acrnm pg, reporting_year::int yr, sum(annual_emission) lbs
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_AIR_EMISSIONS_POLL_RPT_COMBINED_EMISSIONS
  where pollutant_name = 'Ethylene oxide' and unit_of_measure = 'Pounds'
  group by 1,2,3
), ids as (select distinct registry_id from eto),
frs as (
  select f.registry_id, any_value(f.facility_name) facility_name, any_value(f.address) address,
         any_value(upper(trim(f.city))) city, any_value(f.state_code) state_code
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FACILITIES f
  join ids on f.registry_id = ids.registry_id
  group by 1
),
fda as (
  select fei_number, any_value(establishment_name) est, any_value(owner_operator_firm_name) owner,
         any_value(address_line_1) addr, any_value(upper(trim(city))) city, any_value(state_code) st,
         count(*) listing_rows
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_ESTABLISHMENT_REG
  where establishment_type::string ilike '%contract sterilizer%' and iso_country_code = 'US'
  group by 1
),
pairs as (
  select fda.*, frs.registry_id, frs.facility_name, frs.address frs_addr,
         iff(split_part(trim(fda.addr),' ',1) = split_part(trim(frs.address),' ',1), 1, 0) same_num
  from fda join frs on fda.st = frs.state_code and fda.city = frs.city
)
select p.fei_number, p.est, p.owner, p.addr, p.city, p.st, p.listing_rows,
       p.registry_id, p.facility_name, p.frs_addr, p.same_num,
       sum(iff(e.pg='TRIS' and e.yr=2015, e.lbs, null)) tri2015,
       sum(iff(e.pg='TRIS' and e.yr=2018, e.lbs, null)) tri2018,
       sum(iff(e.pg='TRIS' and e.yr=2019, e.lbs, null)) tri2019,
       sum(iff(e.pg='TRIS' and e.yr=2020, e.lbs, null)) tri2020,
       sum(iff(e.pg='TRIS' and e.yr=2021, e.lbs, null)) tri2021,
       sum(iff(e.pg='TRIS' and e.yr=2022, e.lbs, null)) tri2022,
       sum(iff(e.pg='TRIS' and e.yr=2023, e.lbs, null)) tri2023,
       sum(iff(e.pg='TRIS' and e.yr=2024, e.lbs, null)) tri2024,
       sum(iff(e.pg='EIS' and e.yr=2017, e.lbs, null)) eis2017,
       sum(iff(e.pg='EIS' and e.yr=2020, e.lbs, null)) eis2020
from pairs p left join eto e on p.registry_id = e.registry_id
group by 1,2,3,4,5,6,7,8,9,10,11
order by p.listing_rows desc, p.fei_number
