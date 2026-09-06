from _shared.q import run, open_log
open_log("reports/tier1_deep_dive_2026-09-05/30_penalty_then_new_owner/queries.log")
E="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS"
P="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES"
def show(rows):
    for r in rows: print(r)
# a ENROLLMENT_ID format
show(run(f"""select count(*) n, sum(iff(regexp_like(ENROLLMENT_ID,'^O[0-9]{{14}}$'),1,0)) fmt_ok,
 count(try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD')) parsed, min(try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD')) mn, max(try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD')) mx,
 sum(iff(try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD')>='2023-06-17',1,0)) since_pen_start from {E}""","enrollment_id format"))
show(run(f"select year(try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD')) y, count(*) n from {E} group by 1 order by 1","enrollment_id by year"))
show(run(f"select ENROLLMENT_ID, INCORPORATION_DATE, ORGANIZATION_NAME from {E} order by ENROLLMENT_ID desc limit 8","latest enrollment ids"))
# b sentinels
show(run(f"select sum(iff(INCORPORATION_DATE<'1900-01-01',1,0)) pre1900, sum(iff(INCORPORATION_DATE<'1950-01-01',1,0)) pre1950, sum(iff(INCORPORATION_DATE > try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD'),1,0)) incorp_after_enroll from {E}","incorp sentinels & incorp after enroll"))
# c POS_OTHER: SNFs there?
show(run("select column_name from LIBRARY_MARTS.information_schema.columns where table_schema='HEALTH' and table_name='HEALTH__FED_CMS_POS_OTHER' and (column_name ilike '%CTGRY%' or column_name ilike '%PRVDR_NUM%' or column_name ilike '%CHOW%' or column_name ilike '%SUBTYP%') order by 1","pos_other cols"))
show(run("select PRVDR_CTGRY_CD, count(*) n, count(CHOW_DT) chow_dated, sum(iff(CHOW_CNT>0,1,0)) chow_cnt_pos, max(CHOW_DT) mx from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER group by 1 order by 2 desc","pos_other by category"))
# d the flag
show(run("select PROVIDER_CHANGED_OWNERSHIP_IN_LAST_12_MONTHS f, count(*) n from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME group by 1","nursing_home chow flag"))
show(run("select PROVIDER_CHANGED_OWNERSHIP_IN_LAST_12_MONTHS f, count(*) n from LIBRARY_MARTS.HEALTH.HEALTH__FED_NURSINGHOME411 group by 1","nh411 chow flag"))
# e the 39
show(run(f"""with pen as (select CMS_CERTIFICATION_NUMBER_CCN ccn, min(PENALTY_DATE) first_pen, max(PENALTY_DATE) last_pen, count(*) n_pen, sum(FINE_AMOUNT) fines from {P} group by 1)
 select e.CCN, e.ORGANIZATION_NAME, e.ORGANIZATION_TYPE_STRUCTURE, e.PROPRIETARY_NONPROFIT, e.STATE, e.INCORPORATION_DATE, try_to_date(substr(e.ENROLLMENT_ID,2,8),'YYYYMMDD') enroll_dt, pen.first_pen, pen.last_pen, datediff(day,pen.first_pen,e.INCORPORATION_DATE) gap_days, pen.n_pen, pen.fines,
 (select count(*) from {P} p2 where p2.CMS_CERTIFICATION_NUMBER_CCN=e.CCN and p2.PENALTY_DATE>e.INCORPORATION_DATE) pen_after_incorp
 from {E} e join pen on pen.ccn=e.CCN where e.INCORPORATION_DATE>pen.first_pen order by gap_days""","the 39"))
# f gap buckets
show(run(f"""with pen as (select CMS_CERTIFICATION_NUMBER_CCN ccn, min(PENALTY_DATE) first_pen from {P} group by 1)
 select case when datediff(day,pen.first_pen,e.INCORPORATION_DATE) between 0 and 90 then 'a 0-90' when datediff(day,pen.first_pen,e.INCORPORATION_DATE) between 91 and 180 then 'b 91-180'
  when datediff(day,pen.first_pen,e.INCORPORATION_DATE) between 181 and 365 then 'c 181-365' else 'd 366+' end bucket, count(*) n
 from {E} e join pen on pen.ccn=e.CCN where e.INCORPORATION_DATE>pen.first_pen group by 1 order by 1""","gap buckets incorp"))
