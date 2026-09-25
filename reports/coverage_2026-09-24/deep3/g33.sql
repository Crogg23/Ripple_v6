-- g33 deep pass 3, 2026-09-24. Every statement run, in order, numbered.
-- Door: Python (connect/db.py). Read-only. Session setup on each connection (not counted):
--   ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
--   ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';

-- [1] fs220_all
select * from LIBRARY_MARTS.FINANCE.FINANCE__FED_NCUA_CALL_REPORTS_FS220;

-- [2] foicu_all
select * from LIBRARY_MARTS.FINANCE.FINANCE__FED_NCUA_CALL_REPORTS_FOICU;

-- [3] culist_all
select * from LIBRARY_MARTS.FINANCE.FINANCE__FED_NCUA_FEDERALLY_INSURED_CU_LIST;

-- [4] ncua_mergers_all
select * from LIBRARY_MARTS.FINANCE.FINANCE__FED_NCUA_CHARTER_MERGER_EVENTS;

-- [5] mmf_all
select * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_MONEY_MARKET_FUND_INFORMATION;

-- [6] icisair_fac_all
select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES;

-- [7] icisair_viol_all
select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY;

-- [8] icisair_formal_all
select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS;

-- [9] rcra_profile
with f as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_FACILITIES)
select 'all' k, 'all' v, count(*) n, count(distinct id_number) d from f
union all select 'handler', 'distinct handler_id / id+handler', count(distinct handler_id), count(distinct id_number || '|' || coalesce(handler_id, '')) from f
union all select 'univ', hreport_universe_record, count(*), count(distinct id_number) from f group by 2
union all select 'fedgen', fed_waste_generator, count(*), count(distinct id_number) from f group by 2
union all select 'univ_x_fedgen', coalesce(hreport_universe_record, 'NULL') || '|' || coalesce(fed_waste_generator, 'NULL'), count(*), count(distinct id_number) from f group by 2
union all select 'fe', full_enforcement, count(*), count(distinct id_number) from f group by 2
union all select 'run', _source_run_id, count(*), count(distinct id_number) from f group by 2
union all select 'st_ne_loc', iff(state_code = activity_location, 'same', 'diff'), count(*), count(distinct id_number) from f group by 2
union all select * from (select 'name', facility_name, count(*), count(distinct id_number) from f group by 2 order by 3 desc limit 15)
union all select * from (select 'lqg_state', activity_location, count(*), count(distinct id_number) from f where hreport_universe_record = 'LQG' group by 2 order by 3 desc limit 60);

-- [10] usgs_profile
select parameter_cd, parameter_name, unit_cd, data_type, count(*) n, count(distinct site_no) sites,
  count_if(value = -999999) sentinel, count_if(value is null) nulls, count_if(value < 0 and value <> -999999) neg,
  min(datetime) t0, max(datetime) t1,
  min(iff(value = -999999, null, value)) vmin, median(iff(value = -999999, null, value)) vmed, max(value) vmax,
  count(distinct site_no || '|' || to_varchar(datetime)) uniq_site_time
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_USGS_WATER
group by 1, 2, 3, 4 order by n desc;

-- [11] rcra_lqg_inspection_by_state
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

-- [12] rcra_evals_by_state_year_agency
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

-- [13] rcra_la_tx_lqg_mfg_list
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

-- [14] rcra_la_ids_evaluated_since_2021_07
select f.id_number, f.facility_name, f.street_address, f.city_name, f.zip_code, f.hreport_universe_record,
  max(e.evaluation_start_date) last_ev, count(*) n_ev
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_FACILITIES f
join LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_RCRA_EVALUATIONS e on e.id_number = f.id_number
where f.activity_location = 'LA' and e.evaluation_start_date between '2021-07-01' and '2026-09-24'
group by 1, 2, 3, 4, 5, 6;

-- [15] usgs_site_temp_ph
select site_no, any_value(site_name) site_name, any_value(state_cd) state_cd, any_value(county_cd) county_cd, parameter_cd,
  count(*) n, count_if(value = -999999) sentinel, count_if(value < -50 and value <> -999999) junk_low,
  min(iff(value > -50, value, null)) vmin, approx_percentile(iff(value > -50, value, null), 0.5) vmed,
  approx_percentile(iff(value > -50, value, null), 0.95) vp95, max(value) vmax,
  count_if(parameter_cd = '00010' and value >= 30) n_ge30c,
  count_if(parameter_cd = '00400' and value > -50 and (value < 6 or value > 9)) n_ph_out,
  min(datetime) t0, max(datetime) t1
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_USGS_WATER
where data_type = 'real-time' and parameter_cd in ('00010', '00400')
group by site_no, parameter_cd;

-- [16] usgs_day_counts
select to_date(datetime) d, data_type, parameter_cd, count(*) n, count(distinct site_no) sites,
  count_if(value = -999999) sentinel
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_USGS_WATER
group by 1, 2, 3 order by 1, 2, 3;

-- [17] rcra_lqg_mfg_cei_only_by_state
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

-- [18] rcra_eval_types_lqg_mfg_since_2016
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
