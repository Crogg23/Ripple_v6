-- @rcra_evals_by_state_year_agency
with lqg_mfg as (
  select distinct f.id_number
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_FACILITIES f
  join LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_RCRA_NAICS n on n.id_number = f.id_number
  where f.hreport_universe_record like '%LQG%' and left(n.naics_code, 2) in ('31', '32', '33')
)
select e.activity_location st, year(e.evaluation_start_date) yr, e.evaluation_agency agency,
  count(*) evals, count(distinct e.id_number) sites,
  count_if(m.id_number is not null) evals_lqg_mfg, count(distinct m.id_number) sites_lqg_mfg
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_EVALUATIONS e
left join lqg_mfg m on m.id_number = e.id_number
where e.activity_location in ('CA', 'LA', 'NY', 'TX', 'IL', 'NJ', 'CT', 'PA', 'OH', 'IN', 'MI', 'NC')
  and e.evaluation_start_date between '2010-01-01' and '2026-09-24'
group by 1, 2, 3 order by 1, 2, 3;

-- @rcra_la_tx_lqg_mfg_list
with lqg as (
  select id_number, activity_location st, facility_name, city_name, zip_code, hreport_universe_record
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_FACILITIES
  where hreport_universe_record like '%LQG%' and activity_location in ('LA', 'TX')
),
mfg as (
  select id_number, listagg(distinct naics_code, ' ') naics
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_RCRA_NAICS
  where left(naics_code, 2) in ('31', '32', '33') and id_number in (select id_number from lqg)
  group by 1
),
ev as (
  select id_number, max(evaluation_start_date) last_ev, count(*) n_ev,
    count_if(evaluation_start_date >= '2021-07-01') n_ev_5y, count_if(found_violation = 'Y') n_viol,
    max(iff(evaluation_agency = 'E', evaluation_start_date, null)) last_epa_ev
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_EVALUATIONS
  where id_number in (select id_number from mfg) and evaluation_start_date <= '2026-09-24'
  group by 1
),
enf as (
  select id_number, count(*) n_enf, max(enforcement_action_date) last_enf, sum(coalesce(fmp_amount, 0)) fmp
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_ENFORCEMENTS
  where id_number in (select id_number from mfg)
  group by 1
),
vio as (
  select id_number, count(*) n_vio, count_if(actual_rtc_date is null) open_vio, max(date_violation_determined) last_vio
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_VIOLATIONS
  where id_number in (select id_number from mfg)
  group by 1
)
select lqg.*, mfg.naics, ev.last_ev, ev.n_ev, ev.n_ev_5y, ev.n_viol, ev.last_epa_ev,
  enf.n_enf, enf.last_enf, enf.fmp, vio.n_vio, vio.open_vio, vio.last_vio
from lqg join mfg on mfg.id_number = lqg.id_number
left join ev on ev.id_number = lqg.id_number
left join enf on enf.id_number = lqg.id_number
left join vio on vio.id_number = lqg.id_number;
