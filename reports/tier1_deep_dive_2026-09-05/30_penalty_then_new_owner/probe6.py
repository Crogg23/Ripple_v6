from _shared.q import run, open_log
open_log("reports/tier1_deep_dive_2026-09-05/30_penalty_then_new_owner/queries.log")
E="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS"
P="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES"
NH="LIBRARY_MARTS.HEALTH.HEALTH__FED_NURSINGHOME411"
def show(rows):
    for r in rows: print(r)
ENR=f"(select CCN, ASSOCIATE_ID, ORGANIZATION_NAME, STATE, PROPRIETARY_NONPROFIT, INCORPORATION_DATE, try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD') enroll_dt from {E})"
for y0,lo,hi,ylo,yhi in [("2023H2","2023-06-17","2023-12-31","2024-01-01","2024-12-31"),("2024","2024-01-01","2024-12-31","2025-01-01","2025-12-31")]:
    H=f"""(select e.CCN, e.enroll_dt, e.PROPRIETARY_NONPROFIT,
        (select count(*) from {P} p where p.CMS_CERTIFICATION_NUMBER_CCN=e.CCN and p.PENALTY_DATE between '{lo}' and '{hi}') n_pen_y,
        (select coalesce(sum(FINE_AMOUNT),0) from {P} p where p.CMS_CERTIFICATION_NUMBER_CCN=e.CCN and p.PENALTY_DATE between '{lo}' and '{hi}') fines_y
      from {ENR} e where e.enroll_dt <= '{yhi}')"""
    show(run(f"select count(*) dropped_enrolled_after_window from {ENR} where enroll_dt > '{yhi}'", f"cohort {y0}: homes dropped (current enrollment after window)"))
    show(run(f"""select '{y0}' cohort, case when n_pen_y=0 then '0 no penalty' when n_pen_y=1 then '1 one penalty' else '2 two or more' end grp,
       count(*) homes, sum(iff(enroll_dt >= '{ylo}',1,0)) new_enroll_next_year, round(100*sum(iff(enroll_dt >= '{ylo}',1,0))/count(*),2) pct
     from {H} h group by 1,2 order by 2""",f"prospective cohort {y0}: penalty count -> new enrollment next year"))
    show(run(f"""select '{y0}' cohort, case when n_pen_y=0 then 'a none' when fines_y<25000 then 'b under $25k' when fines_y<100000 then 'c $25k-100k' else 'd $100k+' end fine_band,
       count(*) homes, sum(iff(enroll_dt >= '{ylo}',1,0)) new_enroll_next_year, round(100*sum(iff(enroll_dt >= '{ylo}',1,0))/count(*),2) pct
     from {H} h group by 1,2 order by 2""",f"prospective cohort {y0}: fine band -> new enrollment next year"))
    show(run(f"""select '{y0}' cohort, PROPRIETARY_NONPROFIT, iff(n_pen_y>0,'penalized','no penalty') grp,
       count(*) homes, sum(iff(enroll_dt >= '{ylo}',1,0)) new_enroll_next_year, round(100*sum(iff(enroll_dt >= '{ylo}',1,0))/count(*),2) pct
     from {H} h group by 1,2,3 order by 2,3""",f"prospective cohort {y0}: by for-profit flag"))
# same design on INCORPORATION_DATE for 2023H2 only (incorp visible to 2024-09-17): penalty in 2023H2 -> incorporated 2024-01-01..2024-09-17
show(run(f"""with h as (select e.CCN, e.INCORPORATION_DATE, (select count(*) from {P} p where p.CMS_CERTIFICATION_NUMBER_CCN=e.CCN and p.PENALTY_DATE between '2023-06-17' and '2023-12-31') n_pen_y
  from {ENR} e where e.INCORPORATION_DATE is not null and e.INCORPORATION_DATE<='2024-09-17')
 select iff(n_pen_y>0,'penalized 2023H2','no penalty 2023H2') grp, count(*) homes_with_incorp_date, sum(iff(INCORPORATION_DATE>='2024-01-01',1,0)) incorp_2024_to_sep, round(100*sum(iff(INCORPORATION_DATE>='2024-01-01',1,0))/count(*),2) pct from h group by 1""","incorp-date version of the cohort test"))
# state clustering of the 650: top states share
show(run(f"""select e.STATE, count(*) n from {ENR} e join (select CMS_CERTIFICATION_NUMBER_CCN ccn, min(PENALTY_DATE) first_pen from {P} group by 1) pen on pen.ccn=e.CCN where e.enroll_dt>pen.first_pen group by 1 order by 2 desc limit 8""","enroll-after set by state"))
