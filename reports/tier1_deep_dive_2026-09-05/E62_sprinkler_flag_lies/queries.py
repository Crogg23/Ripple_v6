"""E62 - sprinkler flag lies. Every query for the deliverable, SELECT only, Python door.
Run: PYTHONPATH=reports/tier1_deep_dive_2026-09-05 python3 reports/tier1_deep_dive_2026-09-05/E62_sprinkler_flag_lies/queries.py
Probe scripts probe.py / probe2.py / probe3.py hold the exploration; this file is the reproducible set."""
from _shared.q import run, open_log
import json
D="reports/tier1_deep_dive_2026-09-05/E62_sprinkler_flag_lies/"
open_log(D+"queries.log")
F="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_FIRE_DEFICIENCIES"
H="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME"
SNAP="'2026-05-01'"   # PROCESSING_DATE of the flag file, all 14,700 rows
TAGS="('0351','0353','0354','0352','0342','0400','0112','0322')"
# open at snapshot = cited on or before the flag date, and not corrected by the flag date
BASE=f"""with y as (select CMS_CERTIFICATION_NUMBER_CCN ccn, STATE from {H} where AUTOMATIC_SPRINKLER_SYSTEMS_IN_ALL_REQUIRED_AREAS='Yes'),
k as (select CMS_CERTIFICATION_NUMBER_CCN ccn, PROVIDER_NAME, STATE, SURVEY_DATE, DEFICIENCY_TAG_NUMBER tag, DEFICIENCY_DESCRIPTION descr,
  SCOPE_SEVERITY_CODE ss, DEFICIENCY_CORRECTED status, CORRECTION_DATE cd,
  (SURVEY_DATE <= {SNAP} and (CORRECTION_DATE is null or CORRECTION_DATE > {SNAP})) as open_at_snap,
  datediff(day, SURVEY_DATE, {SNAP}) days_open
  from {F} where DEFICIENCY_PREFIX='K' and DEFICIENCY_TAG_NUMBER in {TAGS})
"""
Q={
"01 flag values (the column has no No)": f"select AUTOMATIC_SPRINKLER_SYSTEMS_IN_ALL_REQUIRED_AREAS flag, count(*) homes from {H} group by 1 order by 2 desc",
"02 flag snapshot date": f"select PROCESSING_DATE, count(*) n from {H} group by 1",
"03 home CCN is a key": f"select count(*) n, count(distinct CMS_CERTIFICATION_NUMBER_CCN) d from {H}",
"04 fire table joins clean": f"select count(*) n, count(distinct f.CMS_CERTIFICATION_NUMBER_CCN) homes, sum(iff(h.CMS_CERTIFICATION_NUMBER_CCN is null,1,0)) orphans, min(SURVEY_DATE) mn, max(SURVEY_DATE) mx, max(f.PROCESSING_DATE) fire_snapshot from {F} f left join {H} h using(CMS_CERTIFICATION_NUMBER_CCN)",
"05 sprinkler tag codes, exact": f"select DEFICIENCY_TAG_NUMBER tag, DEFICIENCY_DESCRIPTION descr, count(*) cites, count(distinct CMS_CERTIFICATION_NUMBER_CCN) homes from {F} where DEFICIENCY_DESCRIPTION ilike '%sprinkler%' group by 1,2 order by 3 desc",
"06 sprinkler in health (F) file": f"select count(*) n from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES where DEFICIENCY_DESCRIPTION ilike '%sprinkler%'",
"07 status values in fire file": f"select DEFICIENCY_CORRECTED status, count(*) n, sum(iff(CORRECTION_DATE is null,1,0)) no_date from {F} group by 1 order by 2 desc",
"08 rebuild first pass: K0351 since 2024-06-01, Yes homes": BASE+"select count(*) cites, count(distinct k.ccn) homes, sum(iff(y.ccn is not null,1,0)) cites_yes, count(distinct iff(y.ccn is not null,k.ccn,null)) homes_yes from k left join y using(ccn) where tag='0351' and SURVEY_DATE>='2024-06-01'",
"09 rebuild first pass: open at snapshot, in window": BASE+"select count(*) cites, count(distinct k.ccn) homes, sum(iff(cd is null,1,0)) no_date from k join y using(ccn) where tag='0351' and SURVEY_DATE>='2024-06-01' and (cd is null or cd>"+SNAP+")",
"10 open K0351 at Yes homes, all time, survey on/before snapshot": BASE+"select count(*) cites, count(distinct k.ccn) homes, sum(iff(cd is null,1,0)) no_date from k join y using(ccn) where tag='0351' and open_at_snap",
"11 open K0351 at Yes homes by status": BASE+"select status, count(*) cites, count(distinct k.ccn) homes, sum(iff(cd is null,1,0)) no_date, round(avg(days_open)) avg_days, max(days_open) max_days from k join y using(ccn) where tag='0351' and open_at_snap group by 1 order by 2 desc",
"12 K0351 lifetime at Yes homes by status": BASE+"select status, count(*) cites, count(distinct k.ccn) homes, sum(iff(open_at_snap,1,0)) open_cites from k join y using(ccn) where tag='0351' group by 1 order by 2 desc",
"13 open sprinkler family at Yes homes by tag": BASE+"select tag, min(descr) descr, count(*) cites, count(distinct k.ccn) homes, sum(iff(open_at_snap,1,0)) open_cites, count(distinct iff(open_at_snap,k.ccn,null)) open_homes from k join y using(ccn) group by 1 order by 3 desc",
"14 open K0351 Yes homes by state": BASE+"select k.STATE state, count(distinct k.ccn) open_homes, count(*) open_cites, sum(iff(cd is null,1,0)) no_date, sum(iff(status like 'Waiver%',1,0)) waiver, sum(iff(status like '%no plan%',1,0)) no_plan, round(avg(days_open)) avg_days, max(days_open) max_days, (select count(*) from y y2 where y2.STATE=k.STATE) yes_homes from k join y using(ccn) where tag='0351' and open_at_snap group by 1 order by 2 desc, 1",
"15 open K0351 Yes homes age buckets": BASE+"select case when days_open<90 then 'a. under 90 days' when days_open<365 then 'b. 90 days to 1 yr' when days_open<730 then 'c. 1 to 2 yrs' when days_open<1825 then 'd. 2 to 5 yrs' else 'e. over 5 yrs' end bucket, count(*) cites, sum(iff(status like 'Waiver%',1,0)) waiver, sum(iff(status like '%no plan%',1,0)) no_plan, sum(iff(status like '%has plan%',1,0)) has_plan, sum(iff(status like '%date of correction%',1,0)) has_date, sum(iff(status like 'No revisit%',1,0)) no_revisit from k join y using(ccn) where tag='0351' and open_at_snap group by 1 order by 1",
"16 open K0351 Yes homes days-open stats": BASE+"select median(days_open) med, round(avg(days_open)) avg, max(days_open) mx, sum(iff(days_open>=365,1,0)) over_1yr from k join y using(ccn) where tag='0351' and open_at_snap",
"17 open K0351 Yes homes scope": BASE+"select ss scope, count(*) cites from k join y using(ccn) where tag='0351' and open_at_snap group by 1 order by 1",
"18 open K0351 Yes homes full list": BASE+"select k.ccn, PROVIDER_NAME, k.STATE state, SURVEY_DATE, ss, status, cd, days_open from k join y using(ccn) where tag='0351' and open_at_snap order by days_open desc",
"19 open K0351 at Partial / Data Not Available homes": f"select h.AUTOMATIC_SPRINKLER_SYSTEMS_IN_ALL_REQUIRED_AREAS flag, count(*) cites from {F} f join {H} h using(CMS_CERTIFICATION_NUMBER_CCN) where f.DEFICIENCY_TAG_NUMBER='0351' and f.SURVEY_DATE<={SNAP} and (f.CORRECTION_DATE is null or f.CORRECTION_DATE>{SNAP}) group by 1",
"20 promised dates past the fire file's own date": BASE+"select count(*) n from k join y using(ccn) where tag='0351' and open_at_snap and cd > '2026-06-01'",
"21 repeat K0351 homes (2+ surveys), Yes flag": BASE+"select count(*) homes, sum(iff(n>=3,1,0)) three_plus from (select k.ccn, count(distinct SURVEY_DATE) n from k join y using(ccn) where tag='0351' group by 1) where n>=2",
"22 base rate check: Yes share overall vs cited": BASE+f"select (select count(*) from {H} where AUTOMATIC_SPRINKLER_SYSTEMS_IN_ALL_REQUIRED_AREAS='Yes')/ (select count(*) from {H}) yes_share_all, count(distinct iff(y.ccn is not null,k.ccn,null))/count(distinct k.ccn) yes_share_cited from k left join y using(ccn) where tag='0351'",
}
out={}
for l,q in Q.items():
    r=run(q,l); out[l]=r
    print("==",l)
    for x in r[:12]: print(x)
json.dump(out,open(D+"results.json","w"),default=str,indent=1)

# --- skeptic fix 1: for the 25 durable rows (waiver + no plan), was there a LATER fire survey before the snapshot that did not re-cite K0351?
Q2={
"23 durable 25: later survey check": BASE+f"""
select k.ccn, k.PROVIDER_NAME, k.STATE state, k.SURVEY_DATE, k.status, k.days_open,
  (select max(f2.SURVEY_DATE) from {F} f2 where f2.CMS_CERTIFICATION_NUMBER_CCN=k.ccn and f2.DEFICIENCY_PREFIX='K'
     and f2.SURVEY_DATE > k.SURVEY_DATE and f2.SURVEY_DATE <= {SNAP}) later_k_survey,
  (select count(*) from {F} f3 where f3.CMS_CERTIFICATION_NUMBER_CCN=k.ccn and f3.DEFICIENCY_TAG_NUMBER='0351'
     and f3.SURVEY_DATE > k.SURVEY_DATE and f3.SURVEY_DATE <= {SNAP}) later_k0351
from k join y using(ccn)
where tag='0351' and open_at_snap and (status like 'Waiver%' or status like '%no plan%')
order by status, days_open desc""",
}
for l,q in Q2.items():
    r=run(q,l); out[l]=r
    print("==",l)
    for x in r: print(x)
json.dump(out,open(D+"results.json","w"),default=str,indent=1)
