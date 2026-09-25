-- @rcra_lqg_mfg_cei_only_by_state
with lqg_mfg as (
  select distinct f.id_number, f.activity_location st
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_FACILITIES f
  join LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_RCRA_NAICS n on n.id_number = f.id_number
  where f.hreport_universe_record like '%LQG%' and left(n.naics_code, 2) in ('31', '32', '33')
),
ev as (
  select id_number, max(evaluation_start_date) last_cei
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_EVALUATIONS
  where evaluation_type = 'CEI' and evaluation_start_date <= '2026-09-24'
    and id_number in (select id_number from lqg_mfg)
  group by 1
)
select m.st, count(*) mfg_n, count_if(ev.last_cei >= '2016-07-01') cei_10y, count_if(ev.last_cei >= '2021-07-01') cei_5y
from lqg_mfg m left join ev on ev.id_number = m.id_number
group by 1 order by 2 desc;

-- @rcra_eval_types_lqg_mfg_since_2016
with lqg_mfg as (
  select distinct f.id_number
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_FACILITIES f
  join LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_RCRA_NAICS n on n.id_number = f.id_number
  where f.hreport_universe_record like '%LQG%' and left(n.naics_code, 2) in ('31', '32', '33')
)
select e.activity_location st, e.evaluation_type, any_value(e.evaluation_desc) evaluation_desc, count(*) n
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_EVALUATIONS e
join lqg_mfg m on m.id_number = e.id_number
where e.evaluation_start_date between '2016-07-01' and '2026-09-24'
group by 1, 2 order by 1, 4 desc;
