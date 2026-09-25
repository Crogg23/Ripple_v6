-- MO homes binned by reported total nurse hours per resident-day (half-hour bins): homes, Reliant homes, harm and J-L citations per 100 beds since 2023-06-17 (dose-response check for the staffing link)
with nh as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn, CHAIN_ID, NUMBER_OF_CERTIFIED_BEDS beds, REPORTED_TOTAL_NURSE_STAFFING_HOURS_PER_RESIDENT_PER_DAY hprd
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME where STATE='MO' and NUMBER_OF_CERTIFIED_BEDS>0),
d as (select lpad(trim(CMS_CERTIFICATION_NUMBER_CCN),6,'0') ccn, count_if(SCOPE_SEVERITY_CODE in ('G','H','I','J','K','L')) harm, count_if(SCOPE_SEVERITY_CODE in ('J','K','L')) jkl
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES where SURVEY_DATE >= '2023-06-17' and STATE='MO' group by 1)
select case when hprd is null then 'no data' when hprd < 2 then '<2.0' when hprd >= 5 then '5.0+' else to_varchar(floor(hprd*2)/2,'0.0')||'-'||to_varchar(floor(hprd*2)/2+0.5,'0.0') end hprd_bin,
  count(*) homes, count_if(CHAIN_ID='446') reliant_homes, sum(beds) beds, sum(coalesce(harm,0)) harm, sum(coalesce(jkl,0)) jkl,
  round(100*sum(coalesce(harm,0))/sum(beds),2) harm_per_100_beds, round(100*sum(coalesce(jkl,0))/sum(beds),2) jkl_per_100_beds,
  round(100*sum(iff(CHAIN_ID='446',0,coalesce(harm,0)))/nullif(sum(iff(CHAIN_ID='446',0,beds)),0),2) harm_per_100_beds_nonreliant
from nh left join d on d.ccn=nh.ccn group by 1 order by 1
