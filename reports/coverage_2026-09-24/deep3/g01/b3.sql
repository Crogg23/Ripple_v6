-- @estab_sterilizer_sites
with s as (
  select fei_number, establishment_name, city, state_code, iso_country_code, postal_code, address_line_1,
         owner_operator_firm_name, owner_operator_number, products
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_ESTABLISHMENT_REG
  where establishment_type::string ilike '%contract sterilizer%'
), f as (
  select s.fei_number, count(distinct p.value:product_code::string) product_codes,
         count(distinct iff(p.value:openfda:device_class::string = '3', p.value:product_code::string, null)) class3_codes
  from s, lateral flatten(input => s.products) p
  group by 1
), a as (
  select fei_number, any_value(establishment_name) est, any_value(owner_operator_firm_name) owner,
    any_value(city) city, any_value(state_code) st, any_value(iso_country_code) ctry,
    any_value(left(postal_code,5)) zip, any_value(address_line_1) addr, count(*) listing_rows
  from s group by 1
)
select a.*, f.product_codes, f.class3_codes
from a left join f on a.fei_number = f.fei_number
order by listing_rows desc
-- @epa_eto_emitters
select pgm_sys_acrnm, reporting_year, unit_of_measure, pollutant_name,
  count(distinct registry_id) facilities, sum(annual_emission) total_emission
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_AIR_EMISSIONS_POLL_RPT_COMBINED_EMISSIONS
where pollutant_name ilike '%ethylene oxide%'
group by 1,2,3,4 order by 1,2
