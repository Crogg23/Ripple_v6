"""Hunch 30 - penalty, then a new owner. Load-bearing queries, consolidated.
Run from repo root: PYTHONPATH=reports/tier1_deep_dive_2026-09-05 python3 reports/tier1_deep_dive_2026-09-05/30_penalty_then_new_owner/queries.py
Exploration lives in probe_cols.py / probe2..6.py in this folder; everything is logged to queries.log.
Writes results.json for build_story.py."""
import json, datetime, decimal
from _shared.q import run, open_log
D = "reports/tier1_deep_dive_2026-09-05/30_penalty_then_new_owner"
open_log(f"{D}/queries.log")
E = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS"
P = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES"
NH = "LIBRARY_MARTS.HEALTH.HEALTH__FED_NURSINGHOME411"
ENR = f"(select CCN, ASSOCIATE_ID, ORGANIZATION_NAME, STATE, PROPRIETARY_NONPROFIT, INCORPORATION_DATE, try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD') enroll_dt from {E})"
PEN = f"(select CMS_CERTIFICATION_NUMBER_CCN ccn, min(PENALTY_DATE) first_pen, max(PENALTY_DATE) last_pen, count(*) n_pen from {P} group by 1)"
R = {}

# 1. keys: one row per home in enrollments, CCN 6-9 chars; penalties 6-char CCN
R["keys_enroll"] = run(f"select count(*) n, count(distinct CCN) d_ccn, count(distinct ENROLLMENT_ID) d_enr, sum(iff(regexp_like(ENROLLMENT_ID,'^O[0-9]{{14}}$'),1,0)) enr_fmt_ok from {E}", "keys enroll")
R["keys_pen"] = run(f"select count(*) n, count(distinct CMS_CERTIFICATION_NUMBER_CCN) d_ccn, min(PENALTY_DATE) mn, max(PENALTY_DATE) mx from {P}", "keys penalties")

# 2. the two clocks in the enrollment file
R["clocks"] = run(f"""select count(*) homes, count(INCORPORATION_DATE) incorp_filled, min(INCORPORATION_DATE) incorp_min, max(INCORPORATION_DATE) incorp_max,
  sum(iff(INCORPORATION_DATE<'1900-01-01',1,0)) incorp_pre1900, sum(iff(INCORPORATION_DATE>=current_date,1,0)) incorp_future,
  count(try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD')) enroll_parsed, min(try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD')) enroll_min, max(try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD')) enroll_max,
  sum(iff(INCORPORATION_DATE > try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD'),1,0)) incorp_after_enroll from {E}""", "two clocks")
R["incorp_by_year"] = run(f"select year(INCORPORATION_DATE) y, count(*) n from {E} where INCORPORATION_DATE>='2015-01-01' group by 1 order by 1", "incorp by year")
R["enroll_by_year"] = run(f"select year(try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD')) y, count(*) n from {E} where try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD')>='2015-01-01' group by 1 order by 1", "enroll by year")

# 3. first pass reproduced (incorporation date after first penalty)
R["first_pass"] = run(f"""select count(*) penalized_homes, count(e.CCN) matched, count(e.INCORPORATION_DATE) with_incorp,
  sum(iff(e.INCORPORATION_DATE>pen.first_pen,1,0)) incorp_after_first_pen, sum(iff(e.INCORPORATION_DATE>='2023-06-17',1,0)) incorp_since_202306
  from {PEN} pen left join {ENR} e on e.CCN=pen.ccn""", "first pass reproduced")
R["the39"] = run(f"""select e.CCN, e.ORGANIZATION_NAME, e.STATE, e.INCORPORATION_DATE, e.enroll_dt, pen.first_pen, datediff(day,pen.first_pen,e.INCORPORATION_DATE) gap_days, pen.n_pen,
  (select count(*) from {P} p2 where p2.CMS_CERTIFICATION_NUMBER_CCN=e.CCN and p2.PENALTY_DATE>e.INCORPORATION_DATE) pen_after_incorp
  from {ENR} e join {PEN} pen on pen.ccn=e.CCN where e.INCORPORATION_DATE>pen.first_pen order by gap_days""", "the 39")
R["the39_clusters"] = run(f"""select e.INCORPORATION_DATE, e.STATE, count(*) n, listagg(e.ORGANIZATION_NAME, ' | ') names from {ENR} e join {PEN} pen on pen.ccn=e.CCN
  where e.INCORPORATION_DATE>pen.first_pen group by 1,2 having count(*)>1 order by 3 desc""", "the 39 clustered by incorp date+state")

# 4. rebuilt a different way: enrollment record date after first penalty
R["rebuild"] = run(f"""select count(*) penalized_matched, sum(iff(e.enroll_dt>pen.first_pen,1,0)) enroll_after_first_pen,
  sum(iff(e.enroll_dt>pen.first_pen and datediff(day,pen.first_pen,e.enroll_dt)<=365,1,0)) within_365,
  sum(iff(e.enroll_dt>pen.first_pen and datediff(day,pen.first_pen,e.enroll_dt)<=180,1,0)) within_180,
  sum(iff(e.enroll_dt>pen.first_pen and e.INCORPORATION_DATE>pen.first_pen,1,0)) both_clocks_after,
  sum(iff(e.enroll_dt>pen.first_pen and pen.last_pen>e.enroll_dt,1,0)) penalized_again_after_new_record,
  count(distinct iff(e.enroll_dt>pen.first_pen, e.ASSOCIATE_ID, null)) distinct_owners_in_set
  from {ENR} e join {PEN} pen on pen.ccn=e.CCN""", "rebuild via enrollment date")
R["gap_enroll"] = run(f"""select case when datediff(day,pen.first_pen,e.enroll_dt) between 0 and 90 then '0-90 days' when datediff(day,pen.first_pen,e.enroll_dt) between 91 and 180 then '91-180'
  when datediff(day,pen.first_pen,e.enroll_dt) between 181 and 365 then '181-365' when datediff(day,pen.first_pen,e.enroll_dt) between 366 and 730 then '366-730' else '731+' end bucket,
  min(datediff(day,pen.first_pen,e.enroll_dt)) o, count(*) n from {ENR} e join {PEN} pen on pen.ccn=e.CCN where e.enroll_dt>pen.first_pen group by 1 order by o""", "gap buckets enrollment date")
R["gap_incorp"] = run(f"""select case when datediff(day,pen.first_pen,e.INCORPORATION_DATE) between 0 and 90 then '0-90 days' when datediff(day,pen.first_pen,e.INCORPORATION_DATE) between 91 and 180 then '91-180'
  when datediff(day,pen.first_pen,e.INCORPORATION_DATE) between 181 and 365 then '181-365' when datediff(day,pen.first_pen,e.INCORPORATION_DATE) between 366 and 730 then '366-730' else '731+' end bucket,
  min(datediff(day,pen.first_pen,e.INCORPORATION_DATE)) o, count(*) n from {ENR} e join {PEN} pen on pen.ccn=e.CCN where e.INCORPORATION_DATE>pen.first_pen group by 1 order by o""", "gap buckets incorporation date")

# 5. the enrollment-date clock validated against the one CMS ownership-change flag that is ever Y
R["nh411_flag"] = run(f"select PROVIDER_CHANGED_OWNERSHIP_IN_LAST_12_MONTHS f, count(*) n from {NH} group by 1 order by 1", "nh411 flag values")
R["nh411_flag_cross"] = run(f"""select count(*) flagged_y, count(e.CCN) in_enroll, sum(iff(e.enroll_dt>='2023-06-17',1,0)) enroll_record_since_202306,
  sum(iff(e.enroll_dt>='2024-12-01',1,0)) enroll_record_in_12mo_before_snapshot, sum(iff(e.INCORPORATION_DATE>='2023-06-17',1,0)) incorp_since_202306, count(pen.ccn) penalized
  from {NH} n left join {ENR} e on e.CCN=n.CMS_CERTIFICATION_NUMBER_CCN left join {PEN} pen on pen.ccn=n.CMS_CERTIFICATION_NUMBER_CCN
  where n.PROVIDER_CHANGED_OWNERSHIP_IN_LAST_12_MONTHS='Y'""", "nh411 flag Y vs the two clocks")

# 5b. clock-free check: CMS-flagged ownership changes vs penalized share of all homes
R["flag_vs_pen"] = run(f"""select sum(iff(n.PROVIDER_CHANGED_OWNERSHIP_IN_LAST_12_MONTHS='Y',1,0)) flagged, sum(iff(n.PROVIDER_CHANGED_OWNERSHIP_IN_LAST_12_MONTHS='Y' and pen.ccn is not null,1,0)) flagged_penalized,
  count(*) all_homes, count(pen.ccn) all_penalized from {NH} n left join {PEN} pen on pen.ccn=n.CMS_CERTIFICATION_NUMBER_CCN""", "clock-free: flagged changes vs penalized base")
R["orwa_owners"] = run(f"select count(*) n_rows, count(distinct ASSOCIATE_ID) d_assoc, count(distinct STATE) states from {E} where ORGANIZATION_NAME ilike '% SNF HEALTHCARE LLC'", "OR-WA pattern: distinct owner ids")

# 6. base rate, calendar-matched: penalized in year Y -> new enrollment record in year Y+1, vs homes with no penalty in Y
R["cohorts"] = []
for y0, lo, hi, ylo, yhi in [("2023 H2", "2023-06-17", "2023-12-31", "2024-01-01", "2024-12-31"), ("2024", "2024-01-01", "2024-12-31", "2025-01-01", "2025-12-31")]:
    H = f"""(select e.CCN, e.enroll_dt, e.PROPRIETARY_NONPROFIT,
        (select count(*) from {P} p where p.CMS_CERTIFICATION_NUMBER_CCN=e.CCN and p.PENALTY_DATE between '{lo}' and '{hi}') n_pen_y,
        (select coalesce(sum(FINE_AMOUNT),0) from {P} p where p.CMS_CERTIFICATION_NUMBER_CCN=e.CCN and p.PENALTY_DATE between '{lo}' and '{hi}') fines_y
      from {ENR} e where e.enroll_dt <= '{yhi}')"""
    R["cohorts"] += run(f"""select '{y0}' cohort, 'penalty count' cut, case when n_pen_y=0 then 'no penalty' when n_pen_y=1 then 'one penalty' else 'two or more' end grp, 1 o,
       count(*) homes, sum(iff(enroll_dt >= '{ylo}',1,0)) new_record_next_year, round(100*sum(iff(enroll_dt >= '{ylo}',1,0))/count(*),2) pct
     from {H} h group by 1,2,3 order by 3""", f"cohort {y0}: penalty count -> new record next year")
    R["cohorts"] += run(f"""select '{y0}' cohort, 'fine band' cut, case when n_pen_y=0 then 'no penalty' when fines_y<25000 then 'under $25k' when fines_y<100000 then '$25k-100k' else '$100k+' end grp,
       case when n_pen_y=0 then 0 when fines_y<25000 then 1 when fines_y<100000 then 2 else 3 end o,
       count(*) homes, sum(iff(enroll_dt >= '{ylo}',1,0)) new_record_next_year, round(100*sum(iff(enroll_dt >= '{ylo}',1,0))/count(*),2) pct
     from {H} h group by 1,2,3,4 order by 4""", f"cohort {y0}: fine band -> new record next year")
    R["cohorts"] += run(f"""select '{y0}' cohort, 'ownership' cut, PROPRIETARY_NONPROFIT || ' / ' || iff(n_pen_y>0,'penalized','no penalty') grp, 0 o,
       count(*) homes, sum(iff(enroll_dt >= '{ylo}',1,0)) new_record_next_year, round(100*sum(iff(enroll_dt >= '{ylo}',1,0))/count(*),2) pct
     from {H} h where PROPRIETARY_NONPROFIT in ('P','N') group by 1,2,3 order by 3""", f"cohort {y0}: for-profit split")
R["cohort_dropped"] = run(f"select sum(iff(enroll_dt>'2024-12-31',1,0)) dropped_2023h2, sum(iff(enroll_dt>'2025-12-31',1,0)) dropped_2024 from {ENR}", "cohort homes dropped (record dated after the window)")

# 7. does the penalty come before or after the new record? symmetric 365-day window, fully observable
R["rel_month"] = run(f"""select floor(datediff(day,e.enroll_dt,p.PENALTY_DATE)/30.44) rel_month, count(*) n_pen, count(distinct e.CCN) homes
  from {ENR} e join {P} p on p.CMS_CERTIFICATION_NUMBER_CCN=e.CCN
  where e.enroll_dt between '2024-06-17' and '2025-05-13' and abs(datediff(day,e.enroll_dt,p.PENALTY_DATE))<=365 group by 1 order by 1""", "penalties by month relative to new record")
R["rel_total"] = run(f"""select count(distinct e.CCN) homes_new_record,
  sum(iff(p.PENALTY_DATE between dateadd(day,-365,e.enroll_dt) and dateadd(day,-1,e.enroll_dt),1,0)) pen_365_before,
  sum(iff(p.PENALTY_DATE between e.enroll_dt and dateadd(day,365,e.enroll_dt),1,0)) pen_365_after
  from {ENR} e left join {P} p on p.CMS_CERTIFICATION_NUMBER_CCN=e.CCN where e.enroll_dt between '2024-06-17' and '2025-05-13'""", "penalties 365d before vs after new record")

# 8. no change-of-ownership file for nursing homes is landed: POS_OTHER categories never touch a penalty CCN
R["pos_other"] = run(f"""select p.PRVDR_CTGRY_CD cat, count(*) n, count(CHOW_DT) chow_dated, count(distinct pen.ccn) penalty_ccn_hits
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER p left join {PEN} pen on pen.ccn=p.CCN group by 1 order by 2 desc""", "pos_other: any nursing homes?")

def dflt(o):
    if isinstance(o, (datetime.date, datetime.datetime)): return o.isoformat()
    if isinstance(o, decimal.Decimal): return float(o)
    raise TypeError
json.dump(R, open(f"{D}/results.json", "w"), default=dflt, indent=1)
for k, v in R.items():
    if k not in ("the39", "rel_month", "cohorts"): print(k, v)
print("cohorts:"); [print(c) for c in R["cohorts"]]
