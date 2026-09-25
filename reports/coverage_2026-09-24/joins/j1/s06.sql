-- before/after acquisition: harm (G-L) and J-L per 100 bed-years since 2023-06-17, for Reliant legacy homes, Reliant 2024-25 acquisitions split at their own control date, and other MO homes split at 2024-12-01
with nh as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn, CHAIN_ID, STATE, NUMBER_OF_CERTIFIED_BEDS beds from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME where STATE in ('MO','KS') and NUMBER_OF_CERTIFIED_BEDS>0),
en as (select distinct lpad(trim(CCN),6,'0') ccn, ENROLLMENT_ID from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS),
j as (select en.ccn, min(try_to_date(o.ASSOCIATION_DATE_OWNER,'MM/DD/YYYY')) rel_from from en join LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP o on o.ENROLLMENT_ID=en.ENROLLMENT_ID
   where o.ASSOCIATE_ID_OWNER in ('1951309095','5092951160','4688749625','1658762539','1557792165','1951650696','7315471299') and o.ROLE_TEXT_OWNER not ilike 'ADP%' group by 1),
b as (select nh.*, j.rel_from, '2023-06-17'::date w0, (select max(SURVEY_DATE) from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES) w1,
   case when nh.CHAIN_ID='446' and j.rel_from is null then 'reliant_no_owner_row'
        when nh.CHAIN_ID='446' and j.rel_from < '2023-06-17' then 'reliant_legacy'
        when nh.CHAIN_ID='446' then 'reliant_acquired'
        when nh.STATE='MO' then 'other_mo' else 'other_ks' end grp,
   case when grp='reliant_acquired' then j.rel_from when grp in ('other_mo','other_ks') then '2024-12-01'::date else null end split
   from nh left join j on j.ccn=nh.ccn),
d as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn, SURVEY_DATE, SCOPE_SEVERITY_CODE sev from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES
   where SURVEY_DATE >= '2023-06-17' and SCOPE_SEVERITY_CODE in ('G','H','I','J','K','L')),
h as (select b.ccn, count_if(d.SURVEY_DATE < coalesce(b.split, b.w1+1)) harm_pre, count_if(d.SURVEY_DATE >= b.split) harm_post,
   count_if(d.sev in ('J','K','L') and d.SURVEY_DATE < coalesce(b.split, b.w1+1)) jkl_pre, count_if(d.sev in ('J','K','L') and d.SURVEY_DATE >= b.split) jkl_post
   from b left join d on d.ccn=b.ccn group by 1)
select grp, count(*) homes, sum(beds) beds, min(w1) w1,
  sum(harm_pre) harm_pre, round(sum(beds*datediff('day', w0, coalesce(split, w1))/365.25),0) bedyrs_pre, round(100*sum(harm_pre)/nullif(sum(beds*datediff('day', w0, coalesce(split, w1))/365.25),0),2) harm_rate_pre, round(100*sum(jkl_pre)/nullif(sum(beds*datediff('day', w0, coalesce(split, w1))/365.25),0),2) jkl_rate_pre,
  sum(harm_post) harm_post, round(sum(iff(split is null,0,beds*datediff('day', split, w1)/365.25)),0) bedyrs_post, round(100*sum(harm_post)/nullif(sum(iff(split is null,0,beds*datediff('day', split, w1)/365.25)),0),2) harm_rate_post, round(100*sum(jkl_post)/nullif(sum(iff(split is null,0,beds*datediff('day', split, w1)/365.25)),0),2) jkl_rate_post
from b join h on h.ccn=b.ccn group by 1 order by 1
