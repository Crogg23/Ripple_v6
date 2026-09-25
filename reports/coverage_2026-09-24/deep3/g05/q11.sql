-- HHA eyeball: every agency at 14545 Friar St, Van Nuys, joined to Home Health Compare (CCN): suite, enrollment date, certification date, star, spend ratio, episodes
with t as (select lpad(trim(CCN),6,'0') ccn, ENROLLMENT_ID, ORGANIZATION_NAME, ADDRESS_LINE_2, INCORPORATION_DATE, PROPRIETARY_NONPROFIT,
             try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD') enr_dt
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS
           where upper(regexp_replace(trim(ADDRESS_LINE_1),'[^A-Za-z0-9 ]','')) = '14545 FRIAR ST' and left(ZIP_CODE,5)='91411'),
h as (select lpad(trim(CCN),6,'0') ccn, CERTIFICATION_DATE, QUALITY_OF_PATIENT_CARE_STAR_RATING star, FOOTNOTE_FOR_QUALITY_OF_PATIENT_CARE_STAR_RATING star_fn,
        HOW_MUCH_MEDICARE_SPENDS_ON_AN_EPISODE_OF_CARE_AT_THIS_AGENCY_COMPARED_TO_MEDICARE_SPENDING_ACROSS_ALL_AGENCIES_NATIONALLY spend,
        NO_OF_EPISODES_TO_CALC_HOW_MUCH_MEDICARE_SPENDS_PER_EPISODE_OF_CARE_AT_AGENCY_COMPARED_TO_SPENDING_AT_ALL_AGENCIES_NATIONAL eps, TYPE_OF_OWNERSHIP
      from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH)
select t.ccn, t.enr_dt, h.CERTIFICATION_DATE, t.INCORPORATION_DATE, t.ADDRESS_LINE_2, left(t.ORGANIZATION_NAME,32) org, t.PROPRIETARY_NONPROFIT pnp,
  h.star, left(h.star_fn,40) star_fn, h.spend, h.eps, h.TYPE_OF_OWNERSHIP
from t left join h using (ccn) order by t.enr_dt
