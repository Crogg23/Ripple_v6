from _shared.q import run, open_log
open_log("reports/tier1_deep_dive_2026-09-05/30_penalty_then_new_owner/queries.log")
E="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS"
P="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES"
POS="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER"
NH="LIBRARY_MARTS.HEALTH.HEALTH__FED_NURSINGHOME411"
def show(rows):
    for r in rows: print(r)
PEN=f"(select CMS_CERTIFICATION_NUMBER_CCN ccn, min(PENALTY_DATE) first_pen, max(PENALTY_DATE) last_pen, count(*) n_pen from {P} group by 1)"
ENR=f"(select CCN, ASSOCIATE_ID, ORGANIZATION_NAME, STATE, INCORPORATION_DATE, try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD') enroll_dt from {E})"
# 1 POS_OTHER cat 21: is it SNF?
show(run(f"select PRVDR_CTGRY_CD, PRVDR_CTGRY_SBTYP_CD, count(*) n, count(CHOW_DT) chow_dated from {POS} where PRVDR_CTGRY_CD in ('21','19','06') group by 1,2 order by 1,2","pos cat 21 subtypes"))
show(run(f"select count(*) pos21, count(distinct MEDICARE_MEDICAID_PRVDR_NUMBER) d_num, count(distinct e.CCN) in_enroll, count(distinct pen.ccn) in_pen, count(distinct iff(p.CHOW_DT is not null, pen.ccn, null)) pen_chow_dated, count(distinct iff(p.CHOW_DT>pen.first_pen, pen.ccn, null)) chow_after_first_pen from {POS} p left join {ENR} e on e.CCN=p.MEDICARE_MEDICAID_PRVDR_NUMBER left join {PEN} pen on pen.ccn=p.MEDICARE_MEDICAID_PRVDR_NUMBER where p.PRVDR_CTGRY_CD='21'","pos21 vs enroll/pen"))
show(run(f"select year(CHOW_DT) y, count(*) n from {POS} where PRVDR_CTGRY_CD='21' and CHOW_DT is not null group by 1 order by 1 desc limit 8","pos21 chow by year"))
# 2 NH411 flag Y
show(run(f"select count(*) n, count(pen.ccn) penalized, count(e.CCN) in_enroll, sum(iff(e.enroll_dt>='2023-06-17',1,0)) enroll_recent, sum(iff(e.INCORPORATION_DATE>='2023-06-17',1,0)) incorp_recent, sum(iff(e.enroll_dt>pen.first_pen,1,0)) enroll_after_pen from {NH} n left join {ENR} e on e.CCN=n.CMS_CERTIFICATION_NUMBER_CCN left join {PEN} pen on pen.ccn=n.CMS_CERTIFICATION_NUMBER_CCN where n.PROVIDER_CHANGED_OWNERSHIP_IN_LAST_12_MONTHS='Y'","nh411 flag Y cross"))
# 3 rebuild B: enrollment date after first penalty
show(run(f"""select count(*) penalized_matched, sum(iff(e.enroll_dt>pen.first_pen,1,0)) enroll_after_first_pen,
 sum(iff(e.enroll_dt>pen.first_pen and datediff(day,pen.first_pen,e.enroll_dt)<=365,1,0)) within_365,
 sum(iff(e.enroll_dt>pen.first_pen and datediff(day,pen.first_pen,e.enroll_dt)<=180,1,0)) within_180,
 sum(iff(e.enroll_dt>pen.first_pen and e.INCORPORATION_DATE>pen.first_pen,1,0)) both_after,
 sum(iff(e.INCORPORATION_DATE>pen.first_pen,1,0)) incorp_after,
 sum(iff(e.enroll_dt>pen.first_pen and pen.last_pen>e.enroll_dt,1,0)) penalized_again_after_new_enroll
 from {ENR} e join {PEN} pen on pen.ccn=e.CCN""","rebuild B enroll_dt"))
show(run(f"""select case when datediff(day,pen.first_pen,e.enroll_dt) between 0 and 90 then 'a 0-90' when datediff(day,pen.first_pen,e.enroll_dt) between 91 and 180 then 'b 91-180'
  when datediff(day,pen.first_pen,e.enroll_dt) between 181 and 365 then 'c 181-365' when datediff(day,pen.first_pen,e.enroll_dt) between 366 and 730 then 'd 366-730' else 'e 731+' end bucket, count(*) n
 from {ENR} e join {PEN} pen on pen.ccn=e.CCN where e.enroll_dt>pen.first_pen group by 1 order by 1""","gap buckets enroll_dt"))
# 4 base rate: events per 1000 home-years, calendar-matched exposure to 2026-02-12
show(run(f"""with h as (
 select e.CCN, e.enroll_dt, e.INCORPORATION_DATE, pen.first_pen, iff(pen.ccn is null,'no penalty','penalized') grp,
  iff(pen.ccn is null, to_date('2023-06-17'), pen.first_pen) t0
 from {ENR} e left join {PEN} pen on pen.ccn=e.CCN)
 select grp, count(*) homes, sum(datediff(day,t0,'2026-02-12'))/365.25 home_years,
  sum(iff(enroll_dt>t0,1,0)) new_enroll, round(1000*sum(iff(enroll_dt>t0,1,0))/(sum(datediff(day,t0,'2026-02-12'))/365.25),1) new_enroll_per_1000hy,
  sum(iff(enroll_dt>t0 and datediff(day,t0,enroll_dt)<=365,1,0)) new_enroll_365, round(100*sum(iff(enroll_dt>t0 and datediff(day,t0,enroll_dt)<=365,1,0))/count(*),2) pct_within_365,
  sum(iff(INCORPORATION_DATE>t0,1,0)) new_incorp, count(INCORPORATION_DATE) incorp_filled,
  round(1000*sum(iff(INCORPORATION_DATE>t0,1,0))/(sum(iff(INCORPORATION_DATE is not null, least(datediff(day,t0,'2024-09-17'),9999),0))/365.25),1) new_incorp_per_1000hy_to_202409
 from h group by 1""","base rate penalized vs not"))
# 4b same but t0 for unpenalized set to match penalized first_pen distribution: use median first_pen
show(run(f"select median(first_pen) med_first_pen, min(first_pen) mn, percentile_cont(0.25) within group (order by first_pen) q1, percentile_cont(0.75) within group (order by first_pen) q3 from {PEN}","first_pen distribution"))
# 5 reverse causality: penalties in 365d before vs after enroll_dt, for homes newly enrolled in window
show(run(f"""select count(distinct e.CCN) homes_new_enroll_in_window,
 sum(iff(p.PENALTY_DATE between dateadd(day,-365,e.enroll_dt) and dateadd(day,-1,e.enroll_dt),1,0)) pen_365_before,
 sum(iff(p.PENALTY_DATE between e.enroll_dt and dateadd(day,365,e.enroll_dt),1,0)) pen_365_after,
 count(distinct iff(p.PENALTY_DATE between dateadd(day,-365,e.enroll_dt) and dateadd(day,-1,e.enroll_dt),e.CCN,null)) homes_pen_before,
 count(distinct iff(p.PENALTY_DATE between e.enroll_dt and dateadd(day,365,e.enroll_dt),e.CCN,null)) homes_pen_after
 from {ENR} e left join {P} p on p.CMS_CERTIFICATION_NUMBER_CCN=e.CCN
 where e.enroll_dt between '2024-06-17' and '2025-05-13'""","before vs after new enrollment, symmetric 365d, fully observable window"))
# 6 chain concentration of the 39 and of the enroll-after set
show(run(f"""select e.INCORPORATION_DATE, e.STATE, count(*) n, listagg(e.ORGANIZATION_NAME, ' | ') names from {ENR} e join {PEN} pen on pen.ccn=e.CCN where e.INCORPORATION_DATE>pen.first_pen group by 1,2 having count(*)>1 order by 3 desc""","the 39 grouped by incorp date+state"))
show(run(f"""select e.enroll_dt, e.STATE, count(*) n from {ENR} e join {PEN} pen on pen.ccn=e.CCN where e.enroll_dt>pen.first_pen group by 1,2 having count(*)>=3 order by 3 desc limit 12""","enroll-after set: same-day clusters"))
show(run(f"""select count(distinct e.ASSOCIATE_ID) d_assoc, count(*) homes from {ENR} e join {PEN} pen on pen.ccn=e.CCN where e.enroll_dt>pen.first_pen""","enroll-after set: distinct associate ids"))
