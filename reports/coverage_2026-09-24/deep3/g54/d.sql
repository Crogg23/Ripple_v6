-- [d1_istat_measures]
select dataflow_id, freq, split_part(dimension_keys, '.', -1) measure, count(*) n, count(distinct series_key) series,
  count_if(obs_value < 0) negatives, min(obs_value) min_v, round(median(obs_value), 2) med_v, max(obs_value) max_v,
  count(distinct obs_year) years, min(date) d0, max(date) d1
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_IT_ISTAT
group by 1, 2, 3
order by 1, 2, n desc
