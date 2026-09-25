-- @icisair_viol_all
select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY;

-- @icisair_formal_all
select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS;

-- @rcra_profile
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

-- @usgs_profile
select parameter_cd, parameter_name, unit_cd, data_type, count(*) n, count(distinct site_no) sites,
  count_if(value = -999999) sentinel, count_if(value is null) nulls, count_if(value < 0 and value <> -999999) neg,
  min(datetime) t0, max(datetime) t1,
  min(iff(value = -999999, null, value)) vmin, median(iff(value = -999999, null, value)) vmed, max(value) vmax,
  count(distinct site_no || '|' || to_varchar(datetime)) uniq_site_time
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_USGS_WATER
group by 1, 2, 3, 4 order by n desc;
