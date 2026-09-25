-- chart rows: MO homes by staffing bin (reported total nurse hours per resident-day) x Reliant or not: homes, beds, harm (G-L) and J-L citations since 2023-06-17 per 100 beds
with nh as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn, iff(CHAIN_ID='446','Reliant','Other MO') grp, NUMBER_OF_CERTIFIED_BEDS beds, REPORTED_TOTAL_NURSE_STAFFING_HOURS_PER_RESIDENT_PER_DAY hprd
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME where STATE='MO' and NUMBER_OF_CERTIFIED_BEDS>0),
d as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn, count_if(SCOPE_SEVERITY_CODE in ('G','H','I','J','K','L')) harm, count_if(SCOPE_SEVERITY_CODE in ('J','K','L')) jkl
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES where SURVEY_DATE >= '2023-06-17' and STATE='MO' group by 1)
select case when hprd is null then 'no data' when hprd < 2.5 then 'under 2.5' when hprd < 3 then '2.5-3.0' when hprd < 3.5 then '3.0-3.5' else '3.5+' end hprd_bin, grp,
  count(*) homes, sum(beds) beds, sum(coalesce(harm,0)) harm, sum(coalesce(jkl,0)) jkl,
  round(100*sum(coalesce(harm,0))/sum(beds),2) harm_per_100_beds, round(100*sum(coalesce(jkl,0))/sum(beds),2) jkl_per_100_beds
from nh left join d on d.ccn=nh.ccn group by 1,2 order by 1,2
