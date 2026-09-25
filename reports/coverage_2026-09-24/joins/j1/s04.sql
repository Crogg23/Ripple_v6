-- per Reliant home: earliest Reliant/DeStefane control date (ADP rows dropped), harm citations before/after it, all-time deficiency span, staffing, fines
with rel as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn, PROVIDER_NAME, CITY, STATE, NUMBER_OF_CERTIFIED_BEDS beds, OVERALL_RATING star, SPECIAL_FOCUS_STATUS sff,
   REPORTED_TOTAL_NURSE_STAFFING_HOURS_PER_RESIDENT_PER_DAY hprd, REPORTED_RN_STAFFING_HOURS_PER_RESIDENT_PER_DAY rn, TOTAL_NURSING_STAFF_TURNOVER turn, NUMBER_OF_FINES nf, TOTAL_AMOUNT_OF_FINES_IN_DOLLARS fines, NUMBER_OF_PAYMENT_DENIALS pd,
   DATE_FIRST_APPROVED_TO_PROVIDE_MEDICARE_AND_MEDICAID_SERVICES first_appr
   from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME where CHAIN_ID='446'),
en as (select distinct lpad(trim(CCN),6,'0') ccn, ENROLLMENT_ID from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS),
j as (select en.ccn, min(try_to_date(o.ASSOCIATION_DATE_OWNER,'MM/DD/YYYY')) rel_from from en join LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP o on o.ENROLLMENT_ID=en.ENROLLMENT_ID
   where o.ASSOCIATE_ID_OWNER in ('1951309095','5092951160','4688749625','1658762539','1557792165','1951650696','7315471299') and o.ROLE_TEXT_OWNER not ilike 'ADP%' group by 1),
d as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn, SURVEY_DATE, SCOPE_SEVERITY_CODE sev from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES)
select rel.*, j.rel_from, min(d.SURVEY_DATE) first_survey, max(d.SURVEY_DATE) last_survey,
  count_if(d.sev in ('G','H','I','J','K','L')) harm, count_if(d.sev in ('J','K','L')) jkl,
  count_if(d.sev in ('G','H','I','J','K','L') and d.SURVEY_DATE < j.rel_from) harm_before, count_if(d.sev in ('G','H','I','J','K','L') and d.SURVEY_DATE >= j.rel_from) harm_after
from rel left join j on j.ccn=rel.ccn left join d on d.ccn=rel.ccn
group by all order by j.rel_from desc nulls first
