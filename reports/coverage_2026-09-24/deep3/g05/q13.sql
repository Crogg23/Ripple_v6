-- Hospital enrollments: new enrollments by era (date inside ENROLLMENT_ID) and type, for-profit and psych mix; plus the pre-1900 incorporation dates
with t as (select *, try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD') enr_dt from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS)
select 'era' k, case when year(enr_dt)<2013 then 'a_pre2013' when year(enr_dt)<2019 then 'b_2013_18' else 'c_2019on' end a, PROVIDER_TYPE_CODE b,
  count(*) n, count_if(PROPRIETARY_NONPROFIT='P') fp, count_if(SUBGROUP_PSYCHIATRIC='Y') psych, count_if(SUBGROUP_PSYCHIATRIC='Y' and PROPRIETARY_NONPROFIT='P') psych_fp,
  count_if(SUBGROUP_LONG_TERM='Y') ltch, count_if(SUBGROUP_REHABILITATION='Y') rehab, count_if(SUBGROUP_SHORT_TERM='Y') shortterm,
  count_if(STATE='TX') tx, count_if(STATE='TX' and PROPRIETARY_NONPROFIT='P') tx_fp, count_if(enr_dt is null) bad_id
from t group by 2,3
union all select 'inc_pre1900', INCORPORATION_DATE::text, null, count(*), null, null, null, null, null, null, null, null, null from t where year(INCORPORATION_DATE)<1900 group by 2
union all select * from (select 'new_state_2019on', STATE, null, count(*), count_if(PROPRIETARY_NONPROFIT='P'), count_if(SUBGROUP_PSYCHIATRIC='Y'), null, null, null, null, null, null, null
  from t where year(enr_dt)>=2019 and PROVIDER_TYPE_CODE='00-09' group by 2 order by 4 desc limit 10)
order by 1, 2, 3
