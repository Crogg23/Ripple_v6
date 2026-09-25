-- per-home before/after for the 12 homes Reliant took over in 2024-25: harm and J-L before vs after the control date, window 2023-06-17 to file end, with fines by penalty date
with nh as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn, PROVIDER_NAME, STATE, NUMBER_OF_CERTIFIED_BEDS beds from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME where CHAIN_ID='446'),
en as (select distinct lpad(trim(CCN),6,'0') ccn, ENROLLMENT_ID from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS),
j as (select en.ccn, min(try_to_date(o.ASSOCIATION_DATE_OWNER,'MM/DD/YYYY')) rel_from from en join LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP o on o.ENROLLMENT_ID=en.ENROLLMENT_ID
   where o.ASSOCIATE_ID_OWNER in ('1951309095','5092951160','4688749625','1658762539','1557792165','1951650696','7315471299') and o.ROLE_TEXT_OWNER not ilike 'ADP%' group by 1),
d as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn, SURVEY_DATE, SCOPE_SEVERITY_CODE sev from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES where SURVEY_DATE >= '2023-06-17'),
p as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn, PENALTY_DATE, PENALTY_TYPE, FINE_AMOUNT from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES)
select nh.ccn, nh.PROVIDER_NAME, nh.STATE, nh.beds, j.rel_from,
  round(datediff('day','2023-06-17'::date, j.rel_from)/365.25,2) yrs_pre, round(datediff('day', j.rel_from, '2026-05-20'::date)/365.25,2) yrs_post,
  (select count(distinct SURVEY_DATE) from d where d.ccn=nh.ccn and d.SURVEY_DATE < j.rel_from) surveys_pre, (select count(distinct SURVEY_DATE) from d where d.ccn=nh.ccn and d.SURVEY_DATE >= j.rel_from) surveys_post,
  (select count(*) from d where d.ccn=nh.ccn and d.sev in ('G','H','I','J','K','L') and d.SURVEY_DATE < j.rel_from) harm_pre,
  (select count(*) from d where d.ccn=nh.ccn and d.sev in ('G','H','I','J','K','L') and d.SURVEY_DATE >= j.rel_from) harm_post,
  (select count(*) from d where d.ccn=nh.ccn and d.sev in ('J','K','L') and d.SURVEY_DATE < j.rel_from) jkl_pre,
  (select count(*) from d where d.ccn=nh.ccn and d.sev in ('J','K','L') and d.SURVEY_DATE >= j.rel_from) jkl_post,
  (select count(*) from d where d.ccn=nh.ccn and d.SURVEY_DATE < j.rel_from) alltags_pre, (select count(*) from d where d.ccn=nh.ccn and d.SURVEY_DATE >= j.rel_from) alltags_post,
  (select coalesce(sum(FINE_AMOUNT),0) from p where p.ccn=nh.ccn and p.PENALTY_DATE < j.rel_from) fines_pre, (select coalesce(sum(FINE_AMOUNT),0) from p where p.ccn=nh.ccn and p.PENALTY_DATE >= j.rel_from) fines_post
from nh join j on j.ccn=nh.ccn where j.rel_from >= '2023-06-17' order by j.rel_from
