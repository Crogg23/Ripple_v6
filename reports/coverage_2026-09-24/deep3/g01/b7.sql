-- @faers_lw_by_quarter
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
group by 1,2 order by 1,2
-- @icis_air_state_baseline
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
group by 1 order by 1
-- @deroyal_eto_rows
select registry_id, pgm_sys_acrnm, pgm_sys_id, reporting_year, pollutant_name, annual_emission, unit_of_measure, nei_type
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_AIR_EMISSIONS_POLL_RPT_COMBINED_EMISSIONS
where registry_id in ('110002338738','110024942678') and pollutant_name = 'Ethylene oxide'
order by 1, 4, 2
