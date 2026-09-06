from _shared.q import run, open_log
open_log("reports/tier1_deep_dive_2026-09-05/30_penalty_then_new_owner/queries.log")
E="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS"
P="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES"
POS="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER"
def show(rows):
    for r in rows: print(r)
ENR=f"(select CCN, ASSOCIATE_ID, ORGANIZATION_NAME, STATE, INCORPORATION_DATE, try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD') enroll_dt from {E})"
PEN=f"(select CMS_CERTIFICATION_NUMBER_CCN ccn, min(PENALTY_DATE) first_pen, max(PENALTY_DATE) last_pen, count(*) n_pen from {P} group by 1)"
# POS_OTHER: which column is the CCN
show(run("select column_name from LIBRARY_MARTS.information_schema.columns where table_schema='HEALTH' and table_name='HEALTH__FED_CMS_POS_OTHER' and (column_name ilike '%NUM%' or column_name ilike '%CCN%' or column_name ilike '%PRVDR_ID%') order by 1","pos_other id-ish cols"))
show(run(f"select PRVDR_CTGRY_CD, count(distinct CCN) d_prvdr_num, min(CCN) mn, max(CCN) mx from {POS} group by 1 order by 1","pos CCN distinct by cat"))
show(run(f"select count(*) pos21, count(distinct p.CCN) d, count(distinct e.CCN) in_enroll, count(distinct pen.ccn) in_pen, count(distinct iff(p.CHOW_DT>pen.first_pen,pen.ccn,null)) chow_after_first_pen, count(distinct iff(p.CHOW_DT>='2023-06-17',p.CCN,null)) chow_since from {POS} p left join {ENR} e on e.CCN=p.CCN left join {PEN} pen on pen.ccn=p.CCN where p.PRVDR_CTGRY_CD='21'","pos21 via CCN"))
# first_pen distribution
show(run(f"select median(datediff(day,'2023-06-17',first_pen)) med_days_from_start, count(*) homes, sum(iff(first_pen<='2023-12-31',1,0)) first_pen_2023h2, sum(iff(first_pen between '2024-01-01' and '2024-12-31',1,0)) first_pen_2024 from {PEN}","first_pen distribution"))
# prospective cohorts: penalty in year Y -> new enrollment in year Y+1, vs no penalty in Y
for y0,lo,hi,ylo,yhi in [("2023H2","2023-06-17","2023-12-31","2024-01-01","2024-12-31"),("2024","2024-01-01","2024-12-31","2025-01-01","2025-12-31")]:
    show(run(f"""with h as (
      select e.CCN, e.enroll_dt, e.INCORPORATION_DATE,
        (select count(*) from {P} p where p.CMS_CERTIFICATION_NUMBER_CCN=e.CCN and p.PENALTY_DATE between '{lo}' and '{hi}') n_pen_y,
        (select coalesce(sum(FINE_AMOUNT),0) from {P} p where p.CMS_CERTIFICATION_NUMBER_CCN=e.CCN and p.PENALTY_DATE between '{lo}' and '{hi}') fines_y,
        (select count(*) from {P} p where p.CMS_CERTIFICATION_NUMBER_CCN=e.CCN and p.PENALTY_DATE < '{lo}') n_pen_before
      from {ENR} e where e.enroll_dt < '{ylo}')
     select '{y0}' cohort, case when n_pen_y=0 then '0 no penalty' when n_pen_y=1 then '1 one penalty' else '2 two or more' end grp,
       count(*) homes, sum(iff(enroll_dt between '{ylo}' and '{yhi}',1,0)) new_enroll_next_year,
       round(100*sum(iff(enroll_dt between '{ylo}' and '{yhi}',1,0))/count(*),2) pct
     from h group by 1,2 order by 2""",f"prospective cohort {y0}: penalty -> new enrollment next year"))
    show(run(f"""with h as (
      select e.CCN, e.enroll_dt,
        (select coalesce(sum(FINE_AMOUNT),0) from {P} p where p.CMS_CERTIFICATION_NUMBER_CCN=e.CCN and p.PENALTY_DATE between '{lo}' and '{hi}') fines_y,
        (select count(*) from {P} p where p.CMS_CERTIFICATION_NUMBER_CCN=e.CCN and p.PENALTY_DATE between '{lo}' and '{hi}') n_pen_y
      from {ENR} e where e.enroll_dt < '{ylo}')
     select '{y0}' cohort, case when n_pen_y=0 then 'a none' when fines_y<25000 then 'b under $25k' when fines_y<100000 then 'c $25k-100k' else 'd $100k+' end fine_band,
       count(*) homes, sum(iff(enroll_dt between '{ylo}' and '{yhi}',1,0)) new_enroll_next_year,
       round(100*sum(iff(enroll_dt between '{ylo}' and '{yhi}',1,0))/count(*),2) pct
     from h group by 1,2 order by 2""",f"prospective cohort {y0}: fine band -> new enrollment next year"))
# reverse: penalties 365d before vs after a new enrollment, fully observable window
show(run(f"""select count(distinct e.CCN) homes_new_enroll_in_window,
 sum(iff(p.PENALTY_DATE between dateadd(day,-365,e.enroll_dt) and dateadd(day,-1,e.enroll_dt),1,0)) pen_365_before,
 sum(iff(p.PENALTY_DATE between e.enroll_dt and dateadd(day,365,e.enroll_dt),1,0)) pen_365_after,
 count(distinct iff(p.PENALTY_DATE between dateadd(day,-365,e.enroll_dt) and dateadd(day,-1,e.enroll_dt),e.CCN,null)) homes_pen_before,
 count(distinct iff(p.PENALTY_DATE between e.enroll_dt and dateadd(day,365,e.enroll_dt),e.CCN,null)) homes_pen_after
 from {ENR} e left join {P} p on p.CMS_CERTIFICATION_NUMBER_CCN=e.CCN
 where e.enroll_dt between '2024-06-17' and '2025-05-13'""","penalties 365d before vs after new enrollment"))
# monthly: penalties per home-month relative to new enrollment (-12..+12), for charting
show(run(f"""select floor(datediff(day,e.enroll_dt,p.PENALTY_DATE)/30.44) rel_month, count(*) n_pen, count(distinct e.CCN) homes
 from {ENR} e join {P} p on p.CMS_CERTIFICATION_NUMBER_CCN=e.CCN
 where e.enroll_dt between '2024-06-17' and '2025-05-13' and abs(datediff(day,e.enroll_dt,p.PENALTY_DATE))<=365 group by 1 order by 1""","penalties by month relative to new enrollment"))
# chain concentration
show(run(f"""select e.INCORPORATION_DATE, e.STATE, count(*) n, listagg(e.ORGANIZATION_NAME, ' | ') names from {ENR} e join {PEN} pen on pen.ccn=e.CCN where e.INCORPORATION_DATE>pen.first_pen group by 1,2 having count(*)>1 order by 3 desc""","the 39 grouped by incorp date+state"))
show(run(f"""select e.enroll_dt, e.STATE, count(*) n from {ENR} e join {PEN} pen on pen.ccn=e.CCN where e.enroll_dt>pen.first_pen group by 1,2 having count(*)>=3 order by 3 desc limit 12""","enroll-after set: same-day clusters"))
show(run(f"""select count(distinct e.ASSOCIATE_ID) d_assoc, count(*) homes, sum(iff(e.ORGANIZATION_NAME ilike '%OPCO%' or e.ORGANIZATION_NAME ilike '%OPERAT%' or e.ORGANIZATION_NAME ilike '%SNF%',1,0)) opco_named from {ENR} e join {PEN} pen on pen.ccn=e.CCN where e.enroll_dt>pen.first_pen""","enroll-after set: distinct associate ids"))
