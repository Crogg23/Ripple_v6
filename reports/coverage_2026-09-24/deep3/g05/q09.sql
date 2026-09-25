-- HHA -> POS file (CCN) for the exact county: check the ZIP3 LA approximation per year, then top counties for 2019+ enrollments vs their pre-2013 count
with t as (select lpad(trim(CCN),6,'0') ccn, STATE, left(ZIP_CODE,3) z3, try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD') enr_dt
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS),
p as (select lpad(trim(CCN),6,'0') ccn, max(lpad(FIPS_STATE_CD,2,'0')||lpad(FIPS_CNTY_CD,3,'0')) fips, max(STATE_CD) pst, max(CITY_NAME) pcity
      from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER group by 1),
j as (select t.*, p.fips, p.pcity, (STATE='CA' and (z3 between '900' and '916' or z3 in ('918','935'))) la_z3 from t left join p using (ccn))
select 'yr' k, year(enr_dt)::text a, count(*) total, count(fips) landed, count_if(fips='06037') la_exact, count_if(la_z3) la_zip3,
  count_if(fips='06037' and not la_z3) exact_not_z3, count_if(la_z3 and fips<>'06037') z3_not_exact
from j where year(enr_dt)>=2010 group by 2
union all
select * from (select 'cty', fips||' '||any_value(STATE)||' '||any_value(pcity), count_if(year(enr_dt)>=2019), count(*), count_if(year(enr_dt)<2013),
  count_if(year(enr_dt) between 2013 and 2018), null, null
  from j where fips is not null group by fips order by 3 desc limit 12)
order by 1 desc, 2
