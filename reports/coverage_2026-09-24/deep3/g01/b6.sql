-- @faers_lawyer_reports
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
group by 1,2,3
-- @icis_air_inspections_sterilizers
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
group by 1,2,3 order by 1
