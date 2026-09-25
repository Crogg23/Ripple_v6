-- @sterilizer_sole_source
with s as (
  select fei_number, iso_country_code c, owner_operator_firm_name o, products
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_ESTABLISHMENT_REG
  where establishment_type::string ilike '%contract sterilizer%'
), f as (
  select distinct s.fei_number, s.c, upper(s.o) o, p.value:product_code::string pc,
         p.value:openfda:device_class::string dc
  from s, lateral flatten(input => s.products) p
), pc as (
  select pc, max(dc) dc, count(distinct fei_number) n_sites, count(distinct o) n_owners, any_value(o) one_owner
  from f group by 1
)
select 'ALL' owner, count(*) codes, count_if(n_sites = 1) sole_site_codes, count_if(n_owners = 1) sole_owner_codes,
       count_if(n_owners = 1 and dc = '3') sole_owner_class3
from pc
union all
select * from (
  select one_owner, null, count_if(n_sites = 1), count(*), count_if(dc = '3')
  from pc where n_owners = 1 group by 1
  qualify row_number() over (order by count(*) desc) <= 12
)
-- @estab_status5_and_willowbrook
select status_code, fei_number, any_value(establishment_name) est, any_value(city) city, any_value(state_code) st,
       any_value(iso_country_code) ctry, count(*) n_rows, any_value(establishment_type::string) etype
from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_ESTABLISHMENT_REG
where status_code = '5' or (city ilike 'willowbrook%' and establishment_type::string ilike '%steril%')
group by 1,2 order by n_rows desc limit 40
-- @faers_avandia_2014q2
with ps as (
  select coalesce(nullif(isr,''), primaryid) rid
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DRUG
  where role_cod = 'PS' and upper(trim(drugname)) = 'AVANDIA' and src_quarter in ('2014q1','2014q2','2013q3')
)
select d.src_quarter, d.rept_cod, d.occp_cod, d.mfr_sndr, d.reporter_country, count(*) n,
       min(d.event_dt) min_event, max(d.event_dt) max_event, min(d.init_fda_dt) min_init, max(d.init_fda_dt) max_init,
       count(distinct coalesce(nullif(d.c_case,''), d.caseid)) cases
from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DEMO d
join ps on coalesce(nullif(d.isr,''), d.primaryid) = ps.rid
group by 1,2,3,4,5 order by 1, n desc
