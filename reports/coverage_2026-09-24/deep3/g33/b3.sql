-- @rcra_lqg_inspection_by_state
with lqg as (
  select id_number, activity_location st,
    iff(upper(facility_name) like 'CON%EDISON%', 1, 0) coned
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_FACILITIES
  where hreport_universe_record like '%LQG%'
),
ev as (
  select id_number, max(evaluation_start_date) last_ev, min(evaluation_start_date) first_ev, count(*) n_ev,
    count_if(found_violation = 'Y') n_viol
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_EVALUATIONS
  where id_number in (select id_number from lqg) and evaluation_start_date <= '2026-09-24'
  group by 1
),
mfg as (
  select distinct id_number from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_RCRA_NAICS
  where left(naics_code, 2) in ('31', '32', '33') and id_number in (select id_number from lqg)
)
select lqg.st, count(*) lqg_n, sum(coned) coned_n, count(mfg.id_number) mfg_n,
  count(ev.id_number) ever_ev,
  count_if(ev.last_ev >= '2021-07-01') ev_5y,
  count_if(mfg.id_number is not null and ev.id_number is not null) mfg_ever,
  count_if(mfg.id_number is not null and ev.last_ev >= '2021-07-01') mfg_ev_5y,
  count_if(mfg.id_number is not null and ev.last_ev >= '2016-07-01') mfg_ev_10y,
  count_if(mfg.id_number is not null and ev.id_number is null) mfg_never,
  (select max(evaluation_start_date) from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_EVALUATIONS where evaluation_start_date <= '2026-09-24') e_max
from lqg left join ev on ev.id_number = lqg.id_number left join mfg on mfg.id_number = lqg.id_number
group by 1 order by 2 desc;
