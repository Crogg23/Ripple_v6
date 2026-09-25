-- g01 deep pass 3, 2026-09-24. Every statement run, in order, numbered.
-- Door: Python (connect/db.py). Read-only. Session setup on each connection (not counted):
--   ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
--   ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';

-- [1] estab_sample
select * from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_ESTABLISHMENT_REG
where owner_operator_firm_name ilike 'sterigenics%' limit 3;

-- [2] faers_by_quarter
select src_quarter, count(*) n,
  count_if(role_cod in ('PS','SS','C','I')) role_ok,
  count(distinct isr) isrs,
  count_if(isr is null or isr = '') isr_blank,
  count_if(primaryid is not null and primaryid <> '') pid_filled,
  count(dose_amt) dose_filled, max(dose_amt) max_dose,
  count(exp_dt) exp_filled
from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DRUG
group by 1 order by 1;

-- [3] va_all
select * from LIBRARY_MARTS.HEALTH.HEALTH__FED_VA_ALLCAUSE_MORTALITY;

-- [4] od_all
select * from LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_OVERDOSE;

-- [5] inj_landing_all
select * from LIBRARY_RAW.LANDING.FED_CDC_INJURY_VIOLENCE_COUNTY;

-- [6] estab_sample2
select * from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_ESTABLISHMENT_REG
where establishment_name ilike 'sterigenics%' limit 2;

-- [7] estab_profile
select count(*) n, count(distinct fei_number) fei, count(distinct registration_number) reg,
  count(distinct owner_operator_number) owners,
  count(distinct fei_number || '|' || coalesce(k_number,'') || '|' || coalesce(pma_number,'') || '|' || coalesce(proprietary_name,'')) fei_prod_combos,
  count_if(status_code = '1') s1, count_if(status_code = '5') s5, count(distinct status_code) n_status,
  count(distinct reg_expiry_date_year) n_expiry,
  count_if(establishment_type::string ilike '%steril%') steril_rows,
  count(distinct iff(establishment_type::string ilike '%steril%', fei_number, null)) steril_fei,
  count(distinct iff(establishment_type::string ilike '%steril%' and iso_country_code = 'US', fei_number, null)) steril_fei_us,
  count_if(k_number is not null and k_number <> '') k_filled,
  count(distinct _source_run_id) runs
from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_ESTABLISHMENT_REG;

-- [8] vasuicide_national_all
select * from LIBRARY_MARTS.HEALTH.HEALTH__FED_VA_SUICIDE_NATIONAL;

-- [9] estab_sterilizer_sites
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
order by listing_rows desc;

-- [10] epa_eto_emitters
select pgm_sys_acrnm, reporting_year, unit_of_measure, pollutant_name,
  count(distinct registry_id) facilities, sum(annual_emission) total_emission
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_AIR_EMISSIONS_POLL_RPT_COMBINED_EMISSIONS
where pollutant_name ilike '%ethylene oxide%'
group by 1,2,3,4 order by 1,2;

-- [11] estab_x_epa_eto
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
order by p.listing_rows desc, p.fei_number;

-- [12] echo_sterilizers
select frs_id, facility_name, city, state, county, fips_code, pct_minority, population_density,
  compliance_status, significant_noncompliance_flag, quarters_with_noncompliance, three_yr_compliance_history,
  total_inspection_count, date_last_inspection, informal_action_count, formal_action_count,
  date_last_formal_action, total_penalties, penalty_count, last_penalty_amt, date_last_penalty,
  tri_on_site_releases, is_major_facility
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO
where frs_id in ('110000332015','110000334745','110000349720','110000352706','110000357827','110000403242','110000466488','110000469065','110000472541','110000478162','110000479740','110000498168','110000499425','110000882466','110001260803','110001638032','110001742419','110002131014','110002338738','110006625474','110009356464','110010307373','110014421438','110015320543','110018354010','110019608735','110024942678','110031315903','110035029313','110037143203','110055923336','110062088636','110066023145','110070557911','110070848179','110071091875','110071440424','110071673291','110071778836','110071786584','110071854207','110071854691','110071947898');

-- [13] eto_tri_gap_check
select registry_id, pgm_sys_acrnm, reporting_year::int yr, count(*) n_rows,
  count_if(pollutant_name = 'Ethylene oxide') eto_rows
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_AIR_EMISSIONS_POLL_RPT_COMBINED_EMISSIONS
where registry_id in ('110031315903','110000499425','110000349720','110015320543','110000472541','110002338738')
group by 1,2,3 order by 1,2,3;

-- [14] faers_drugnames
select upper(trim(drugname)) dn, count(*) n, count_if(role_cod = 'PS') ps,
  count(distinct src_quarter) quarters, count(*) over () distinct_names
from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DRUG
group by 1
qualify row_number() over (order by count(*) desc) <= 40;

-- [15] faers_demo_occp
select left(src_quarter,4) yr, occp_cod, count(*) n,
  count_if(gndr_cod in ('M','F')) sex_mf, count_if(gndr_cod in ('Y','N')) sex_yn,
  count_if(i_f_cod in ('I','F') or i_f_code in ('I','F')) if_ok
from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DEMO
group by 1,2 order by 1,3 desc;

-- [16] faers_lawyer_reports
with demo as (
  select coalesce(nullif(isr,''), primaryid) rid, occp_cod,
         coalesce(nullif(c_case,''), caseid) case_id, left(src_quarter,4) yr
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DEMO
), ps as (
  select coalesce(nullif(isr,''), primaryid) rid, upper(trim(drugname)) dn
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DRUG
  where role_cod = 'PS'
), j as (
  select ps.dn, demo.yr, demo.occp_cod, demo.case_id
  from ps join demo on ps.rid = demo.rid
), tot as (
  select dn, count(*) reports, count(distinct case_id) cases, count_if(occp_cod = 'LW') lw,
         count(distinct iff(occp_cod = 'LW', case_id, null)) lw_cases
  from j group by 1
), top as (
  select dn from tot qualify row_number() over (order by lw desc) <= 10
)
select 'ALL' kind, 'ALL' dn, 'ALL' yr, count(*) reports, count(distinct case_id) cases,
       count_if(occp_cod = 'LW') lw, count(distinct iff(occp_cod = 'LW', case_id, null)) lw_cases
from j
union all
select * from (
  select 'DRUG', dn, 'ALL', reports, cases, lw, lw_cases from tot
  qualify row_number() over (order by lw desc) <= 30
)
union all
select 'YEAR', j.dn, j.yr, count(*), count(distinct j.case_id), count_if(j.occp_cod = 'LW'),
       count(distinct iff(j.occp_cod = 'LW', j.case_id, null))
from j join top on j.dn = top.dn
group by 1,2,3;

-- [17] icis_air_inspections_sterilizers
with ids as (
  select column1 registry_id from values ('110002338738'),('110024942678'),('110037143203'),('110009356464'),
    ('110000334745'),('110010307373'),('110000332015'),('110000469065'),('110001742419'),('110015320543'),
    ('110000478162'),('110000349720'),('110000403242')
), links as (
  select distinct l.registry_id, l.pgm_sys_id, l.pgm_sys_acrnm
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_PROGRAM_LINKS l
  join ids on l.registry_id = ids.registry_id
  where l.pgm_sys_acrnm ilike '%AIR%'
)
select links.registry_id, links.pgm_sys_acrnm, links.pgm_sys_id,
       count(f.activity_id) fce_pce_count, min(f.actual_end_date) first_eval, max(f.actual_end_date) last_eval,
       count_if(f.actual_end_date >= '2019-01-01') evals_since_2019
from links
left join LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FCES_PCES f
  on f.pgm_sys_id = links.pgm_sys_id
group by 1,2,3 order by 1;

-- [18] faers_lw_by_quarter
with demo as (
  select coalesce(nullif(isr,''), primaryid) rid, occp_cod, rept_cod, src_quarter
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DEMO
), ps as (
  select coalesce(nullif(isr,''), primaryid) rid, upper(trim(drugname)) dn
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DRUG
  where role_cod = 'PS'
    and upper(trim(drugname)) in ('METOCLOPRAMIDE','METOCLOPRAMIDE HYDROCHLORIDE','REGLAN','YAZ','AVANDIA')
)
select ps.dn, demo.src_quarter, count(*) reports, count_if(demo.occp_cod = 'LW') lw,
       count_if(demo.occp_cod = 'LW' and demo.rept_cod = 'DIR') lw_direct,
       count_if(demo.occp_cod = 'LW' and demo.rept_cod = 'EXP') lw_expedited
from ps join demo on ps.rid = demo.rid
group by 1,2 order by 1,2;

-- [19] icis_air_state_baseline
with fac as (
  select pgm_sys_id, state, facility_name, city
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES
  where state in ('TX','TN','GA','MO','PA')
), ev as (
  select pgm_sys_id, count_if(actual_end_date >= '2019-01-01') evals_since_2019
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FCES_PCES
  group by 1
)
select fac.state, count(*) facilities,
       median(coalesce(ev.evals_since_2019,0)) median_evals,
       avg(coalesce(ev.evals_since_2019,0)) avg_evals,
       count_if(coalesce(ev.evals_since_2019,0) = 0) zero_evals,
       listagg(iff(fac.city ilike 'laredo' and (fac.facility_name ilike '%midwest%' or fac.facility_name ilike '%steril%'),
                   fac.pgm_sys_id || ' ' || fac.facility_name, null), '; ') laredo_sterilizer_hits
from fac left join ev on fac.pgm_sys_id = ev.pgm_sys_id
group by 1 order by 1;

-- [20] deroyal_eto_rows
select registry_id, pgm_sys_acrnm, pgm_sys_id, reporting_year, pollutant_name, annual_emission, unit_of_measure, nei_type
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_AIR_EMISSIONS_POLL_RPT_COMBINED_EMISSIONS
where registry_id in ('110002338738','110024942678') and pollutant_name = 'Ethylene oxide'
order by 1, 4, 2;

-- [21] sterilizer_sole_source
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
);

-- [22] estab_status5_and_willowbrook
select status_code, fei_number, any_value(establishment_name) est, any_value(city) city, any_value(state_code) st,
       any_value(iso_country_code) ctry, count(*) n_rows, any_value(establishment_type::string) etype
from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_ESTABLISHMENT_REG
where status_code = '5' or (city ilike 'willowbrook%' and establishment_type::string ilike '%steril%')
group by 1,2 order by n_rows desc limit 40;

-- [23] faers_avandia_2014q2
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
group by 1,2,3,4,5 order by 1, n desc;
