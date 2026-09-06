from _shared.q import run, open_log
import json
open_log("reports/tier1_deep_dive_2026-09-05/E62_sprinkler_flag_lies/queries.log")
F="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_FIRE_DEFICIENCIES"
H="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME"
SNAP="'2026-05-01'"
YES=f"""with y as (select CMS_CERTIFICATION_NUMBER_CCN ccn, STATE from {H} where AUTOMATIC_SPRINKLER_SYSTEMS_IN_ALL_REQUIRED_AREAS='Yes'),
k as (select f.CMS_CERTIFICATION_NUMBER_CCN ccn, f.PROVIDER_NAME, f.STATE, f.SURVEY_DATE, f.DEFICIENCY_TAG_NUMBER tag, f.SCOPE_SEVERITY_CODE ss, f.DEFICIENCY_CORRECTED status, f.CORRECTION_DATE cd,
  (f.CORRECTION_DATE is null or f.CORRECTION_DATE > {SNAP}) as open_at_snap
  from {F} f where f.DEFICIENCY_PREFIX='K' and f.DEFICIENCY_TAG_NUMBER in ('0351','0353','0354','0352','0342','0400','0112','0322'))
"""
out={}
Q={
"landing snapshot date": f"select PROCESSING_DATE, count(*) n from LIBRARY_RAW.LANDING.FED_CMS_NURSING_HOME group by 1",
"mart processing null?": f"select count(*) n, count(PROCESSING_DATE) p from {H}",
"rebuild: k0351 since 2024-06-01 at Yes homes": YES+f"select count(*) cites, count(distinct k.ccn) homes, sum(iff(y.ccn is not null,1,0)) cites_yes, count(distinct iff(y.ccn is not null,k.ccn,null)) homes_yes from k left join y using(ccn) where tag='0351' and SURVEY_DATE>='2024-06-01'",
"rebuild: open k0351 at Yes homes (any survey date)": YES+f"select count(*) cites, count(distinct k.ccn) homes, sum(iff(open_at_snap,1,0)) open_cites, count(distinct iff(open_at_snap,k.ccn,null)) open_homes from k join y using(ccn) where tag='0351'",
"open k0351 at Yes homes by status": YES+f"select status, count(*) cites, count(distinct k.ccn) homes, sum(iff(cd is null,1,0)) no_date, sum(iff(cd>{SNAP},1,0)) dated_after_snap, min(SURVEY_DATE) oldest, max(SURVEY_DATE) newest from k join y using(ccn) where tag='0351' and open_at_snap group by 1 order by 2 desc",
"all-status k0351 at Yes homes by status": YES+f"select status, count(*) cites, count(distinct k.ccn) homes, sum(iff(open_at_snap,1,0)) open_cites from k join y using(ccn) where tag='0351' group by 1 order by 2 desc",
"open sprinkler-family at Yes homes by tag": YES+f"select tag, count(*) cites, count(distinct k.ccn) homes, sum(iff(open_at_snap,1,0)) open_cites, count(distinct iff(open_at_snap,k.ccn,null)) open_homes from k join y using(ccn) group by 1 order by 2 desc",
"open k0351 Yes homes by state": YES+f"select k.STATE, count(distinct k.ccn) open_homes, count(*) open_cites, sum(iff(cd is null,1,0)) no_date, sum(iff(status like 'Waiver%',1,0)) waiver_cites, round(avg(datediff(day,SURVEY_DATE,{SNAP}))) avg_days_open, max(datediff(day,SURVEY_DATE,{SNAP})) max_days_open, (select count(*) from y y2 where y2.STATE=k.STATE) yes_homes_in_state from k join y using(ccn) where tag='0351' and open_at_snap group by 1 order by 2 desc, 1",
"open k0351 Yes homes age buckets": YES+f"select case when datediff(day,SURVEY_DATE,{SNAP})<90 then 'a. under 90 days' when datediff(day,SURVEY_DATE,{SNAP})<365 then 'b. 90 days to 1 yr' when datediff(day,SURVEY_DATE,{SNAP})<730 then 'c. 1 to 2 yrs' when datediff(day,SURVEY_DATE,{SNAP})<1825 then 'd. 2 to 5 yrs' else 'e. over 5 yrs' end bucket, count(*) cites, count(distinct k.ccn) homes, sum(iff(status like 'Waiver%',1,0)) waiver, sum(iff(status like '%no plan%',1,0)) no_plan, sum(iff(status like '%has plan%',1,0)) has_plan, sum(iff(status like '%date of correction%',1,0)) has_date from k join y using(ccn) where tag='0351' and open_at_snap group by 1 order by 1",
"open k0351 Yes homes scope": YES+f"select ss, count(*) cites, count(distinct k.ccn) homes from k join y using(ccn) where tag='0351' and open_at_snap group by 1 order by 1",
"open k0351 Yes homes list": YES+f"select k.ccn, k.PROVIDER_NAME, k.STATE, SURVEY_DATE, ss, status, cd, datediff(day,SURVEY_DATE,{SNAP}) days_open from k join y using(ccn) where tag='0351' and open_at_snap order by days_open desc",
"open k0351 at Partial/DNA homes": f"select h.AUTOMATIC_SPRINKLER_SYSTEMS_IN_ALL_REQUIRED_AREAS f, count(*) cites, count(distinct f.CMS_CERTIFICATION_NUMBER_CCN) homes from {F} f join {H} h using(CMS_CERTIFICATION_NUMBER_CCN) where f.DEFICIENCY_TAG_NUMBER='0351' and (f.CORRECTION_DATE is null or f.CORRECTION_DATE>{SNAP}) group by 1",
"repeat k0351 same home 2+ surveys, Yes flag": YES+f"select count(*) homes, sum(iff(n>=3,1,0)) three_plus from (select k.ccn, count(distinct SURVEY_DATE) n from k join y using(ccn) where tag='0351' group by 1) where n>=2",
"correction-date-after-snap: how far after": YES+f"select datediff(day,{SNAP},cd) d, count(*) n from k join y using(ccn) where tag='0351' and cd>{SNAP} group by 1 order by 1",
}
for l,q in Q.items():
    r=run(q,l); out[l]=r
    print("==",l)
    for x in r[:70]: print(x)
json.dump(out,open("reports/tier1_deep_dive_2026-09-05/E62_sprinkler_flag_lies/probe3.json","w"),default=str,indent=1)
