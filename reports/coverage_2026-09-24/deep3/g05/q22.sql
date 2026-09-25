-- HHA robustness: exact state shares by era (STATE column, no ZIP approximation); top ZIP3 prefixes nationally for 2019+ enrollments; HHA NPIs on the OIG exclusion list
with t as (select NPI, STATE, left(ZIP_CODE,3) z3, try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD') enr_dt
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS),
l as (select trim(NPI) npi, EXCLUSION_DATE, EXCLUSION_TYPE, BUSINESS_NAME from LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE where NPI_IS_REAL)
select * from (select 'state' k, STATE a, count_if(year(enr_dt)>=2019) b, count_if(year(enr_dt)<2013) c, count_if(year(enr_dt) between 2013 and 2018) d, count(*) e
  from t group by 2 order by 3 desc limit 8)
union all select 'nat', 'all', count_if(year(enr_dt)>=2019), count_if(year(enr_dt)<2013), count_if(year(enr_dt) between 2013 and 2018), count(*) from t
union all select * from (select 'zip3', STATE||' '||z3, count_if(year(enr_dt)>=2019), count_if(year(enr_dt)<2013), count_if(year(enr_dt) between 2013 and 2018), count(*)
  from t group by 2 order by 3 desc limit 14)
union all select 'leie', l.BUSINESS_NAME||' | '||t.STATE||' | '||l.EXCLUSION_TYPE, year(l.EXCLUSION_DATE), year(t.enr_dt), null, null from t join l on l.npi=trim(t.NPI)
order by 1, 3 desc
