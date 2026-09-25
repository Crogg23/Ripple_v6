-- ICIS-Air full and partial compliance evaluations, aggregated per facility (1.78M rows in)
select PGM_SYS_ID, count(*) n_eval,
  count_if(COMP_MONITOR_TYPE_DESC ilike 'FCE%') n_fce,
  count_if(COMP_MONITOR_TYPE_DESC ilike 'FCE%' and year(ACTUAL_END_DATE) between 2016 and 2025) n_fce_16_25,
  max(iff(COMP_MONITOR_TYPE_DESC ilike 'FCE%', ACTUAL_END_DATE, null)) last_fce,
  max(ACTUAL_END_DATE) last_eval,
  listagg(distinct COMP_MONITOR_TYPE_CODE, '|') codes
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FCES_PCES
group by 1
