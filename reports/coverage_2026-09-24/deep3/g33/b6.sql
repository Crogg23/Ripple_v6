-- @usgs_site_temp_ph
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

-- @usgs_day_counts
select to_date(datetime) d, data_type, parameter_cd, count(*) n, count(distinct site_no) sites,
  count_if(value = -999999) sentinel
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_USGS_WATER
group by 1, 2, 3 order by 1, 2, 3;
