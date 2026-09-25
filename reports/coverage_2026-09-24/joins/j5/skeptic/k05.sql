select CCN_FACILITY_TYPE, PROVIDER_TYPE, count(*) n, count(distinct PROVIDER_CCN) ccns,
  sum(iff(try_to_number(substr(PROVIDER_CCN,3,4)) between 1500 and 1799 or PROVIDER_CCN in ('971787','971743','A91509','971758','A91592','741649'),1,0)) hospice_range
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS group by 1,2 order by 3 desc
