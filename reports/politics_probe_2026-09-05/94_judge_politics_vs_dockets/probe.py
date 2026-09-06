"""Hunch 94 probe: every query in the order run."""
from _shared.q import run, open_log
open_log("reports/politics_probe_2026-09-05/94_judge_politics_vs_dockets/probe.log")
L="LIBRARY_RAW.LANDING."
def show(r,n=40):
    for x in r[:n]: print({k:(str(v)[:90] if v is not None else None) for k,v in x.items()})
show(run(f"select POLITICAL_PARTY, SOURCE, count(*) n, count(distinct PERSON_ID) persons from {L}FED_COURTLISTENER_JUDGE_POLITICAL_AFFILIATIONS group by 1,2 order by 3 desc","pa_party"))
show(run(f"select count(*) n, count(distinct PERSON_ID) persons, count(distinct ID) ids from {L}FED_COURTLISTENER_JUDGE_POLITICAL_AFFILIATIONS","pa_counts"))
show(run(f"""select count(*) n, count(distinct ID) ids, count_if(nullif(DISPOSITION,'') is not null) has_disp, count(distinct DISPOSITION) disps, count(distinct NATURE_OF_SUIT) nos,
  min(DATE_FILED) d0, max(DATE_FILED) d1 from {L}FED_COURTLISTENER_FJC_IDB_CL_LINKED""","linked_counts"))
show(run(f"""select count(*) n, count_if(nullif(ASSIGNED_TO_ID,'') is not null) assigned, count(distinct IDB_DATA_ID) idb_ids
  from {L}FED_COURTLISTENER_DOCKETS where nullif(IDB_DATA_ID,'') is not null""","dockets_with_idb"))
show(run(f"select column_name, data_type from LIBRARY_RAW.information_schema.columns where table_schema='LANDING' and table_name='FED_FEC_INDIV_CONTRIBUTIONS' order by ordinal_position","fec_cols"),60)


# ===== SECTION =====
"""Hunch 94: judge party vs disposition. Leg: POLITICAL_AFFILIATIONS (PERSON_ID) -> DOCKETS.ASSIGNED_TO_ID -> DOCKETS.IDB_DATA_ID -> FJC_IDB_CL_LINKED (JUDGMENT, NATURE_OF_SUIT).
IDB FILEJUDG is blank on the big districts, so the FJC_SERVICE route is not used; CourtListener already linked IDB rows to dockets and dockets to judges.
Second leg (thin, one query): CL judge name+state vs FEC indiv NAME/STATE, transaction dated before first judicial DATE_START."""
from _shared.q import run, open_log
open_log("reports/politics_probe_2026-09-05/94_judge_politics_vs_dockets/probe.log")
L="LIBRARY_RAW.LANDING."
def show(r,n=40):
    for x in r[:n]: print({k:(str(v)[:100] if v is not None else None) for k,v in x.items()})
PARTY = f"""
party as (
  select PERSON_ID, POLITICAL_PARTY p from {L}FED_COURTLISTENER_JUDGE_POLITICAL_AFFILIATIONS
  where POLITICAL_PARTY in ('d','r') and nullif(PERSON_ID,'') is not null
  qualify row_number() over (partition by PERSON_ID order by nullif(DATE_START,'') desc nulls last, ID desc) = 1
),
cases as (
  select party.p, d.ASSIGNED_TO_ID judge, l.NATURE_OF_SUIT nos, l.JUDGMENT jd, l.DISPOSITION disp, l.PRO_SE, try_to_date(l.DATE_FILED) filed
  from {L}FED_COURTLISTENER_DOCKETS d
  join party on d.ASSIGNED_TO_ID = party.PERSON_ID
  join {L}FED_COURTLISTENER_FJC_IDB_CL_LINKED l on l.ID = d.IDB_DATA_ID
)
"""
show(run(f"""with {PARTY} select p, count(*) cases, count(distinct judge) judges, count_if(jd in ('1','2')) decided_pl_or_def,
  count_if(jd='1') for_plaintiff, count_if(jd='2') for_defendant, round(100.0*count_if(jd='1')/nullif(count_if(jd in ('1','2')),0),1) pct_plaintiff,
  min(filed) d0, max(filed) d1 from cases group by 1""", "party_x_judgment"))
show(run(f"""with {PARTY} select nos, p, count(*) cases, count_if(jd='1') for_pl, count_if(jd='2') for_def,
  round(100.0*count_if(jd='1')/nullif(count_if(jd in ('1','2')),0),1) pct_plaintiff
  from cases where nos in ('442','440','710','790','791','830','840','365','367','410','445','550','555','190','195') group by 1,2 order by 1,2""", "nos_x_party"), 40)
show(run(f"""with {PARTY} select p, iff(PRO_SE in ('1','3'),'pro se plaintiff','represented') side, count(*) cases, count_if(jd='1') for_pl, count_if(jd='2') for_def,
  round(100.0*count_if(jd='1')/nullif(count_if(jd in ('1','2')),0),1) pct_plaintiff from cases where nos='442' group by 1,2 order by 1,2""", "nos442_prose"))
# thin leg: FEC name match, pre-appointment
show(run(f"""with j as (
  select j.ID person_id, upper(j.NAME_LAST) ln, upper(j.NAME_FIRST) fn, min(try_to_date(p.DATE_START)) first_bench, min(p.LOCATION_STATE) st
  from {L}FED_COURTLISTENER_JUDGES j join {L}FED_COURTLISTENER_POSITIONS p on p.PERSON_ID = j.ID and p.POSITION_TYPE like 'jud%'
  join (select distinct PERSON_ID from {L}FED_COURTLISTENER_JUDGE_POLITICAL_AFFILIATIONS where POLITICAL_PARTY in ('d','r')) pa on pa.PERSON_ID = j.ID
  where length(j.NAME_LAST) >= 4 and length(j.NAME_FIRST) >= 3 group by 1,2,3
  having first_bench is not null and st is not null
),
m as (
  select j.person_id, f.NAME, f.CITY, f.STATE, f.EMPLOYER, f.OCCUPATION, try_to_date(f.TRANSACTION_DT,'MMDDYYYY') dt, try_to_number(f.TRANSACTION_AMT) amt, j.first_bench
  from {L}FED_FEC_INDIV_CONTRIBUTIONS f join j on f.NAME = j.ln || ', ' || j.fn and f.STATE = j.st
)
select count(*) rows_matched, count(distinct person_id) judges_matched, count_if(dt < first_bench) pre_bench_rows, count(distinct iff(dt < first_bench, person_id, null)) judges_pre_bench,
  sum(iff(dt < first_bench, amt, 0)) pre_bench_dollars, count_if(upper(OCCUPATION) like '%ATTORNEY%' or upper(OCCUPATION) like '%LAWYER%') occ_lawyer,
  count_if(upper(OCCUPATION) like '%JUDGE%') occ_judge from m""", "fec_name_match"))
show(run(f"""with j as (
  select j.ID person_id, upper(j.NAME_LAST) ln, upper(j.NAME_FIRST) fn, min(try_to_date(p.DATE_START)) first_bench, min(p.LOCATION_STATE) st
  from {L}FED_COURTLISTENER_JUDGES j join {L}FED_COURTLISTENER_POSITIONS p on p.PERSON_ID = j.ID and p.POSITION_TYPE like 'jud%'
  join (select distinct PERSON_ID from {L}FED_COURTLISTENER_JUDGE_POLITICAL_AFFILIATIONS where POLITICAL_PARTY in ('d','r')) pa on pa.PERSON_ID = j.ID
  where length(j.NAME_LAST) >= 4 and length(j.NAME_FIRST) >= 3 group by 1,2,3 having first_bench is not null and st is not null
)
select j.person_id, f.NAME, f.CITY, f.STATE, f.EMPLOYER, f.OCCUPATION, f.TRANSACTION_DT, f.TRANSACTION_AMT, j.first_bench
from {L}FED_FEC_INDIV_CONTRIBUTIONS f join j on f.NAME = j.ln || ', ' || j.fn and f.STATE = j.st
where try_to_date(f.TRANSACTION_DT,'MMDDYYYY') < j.first_bench order by random() limit 12""", "fec_sample"), 12)


# ===== SECTION =====
"""Hunch 94, pass 2: why zero pre-bench FEC rows - check the FEC table's date range and eyeball the name matches."""
from _shared.q import run, open_log
open_log("reports/politics_probe_2026-09-05/94_judge_politics_vs_dockets/probe.log")
L="LIBRARY_RAW.LANDING."
def show(r,n=40):
    for x in r[:n]: print({k:(str(v)[:100] if v is not None else None) for k,v in x.items()})
show(run(f"""select count(*) n, min(try_to_date(TRANSACTION_DT,'MMDDYYYY')) d0, max(try_to_date(TRANSACTION_DT,'MMDDYYYY')) d1,
  count_if(try_to_date(TRANSACTION_DT,'MMDDYYYY') is null) bad_dates, count(distinct substr(TRANSACTION_DT,5,4)) years from {L}FED_FEC_INDIV_CONTRIBUTIONS""", "fec_dates"))
show(run(f"""with j as (
  select j.ID person_id, upper(j.NAME_LAST) ln, upper(j.NAME_FIRST) fn, min(try_to_date(p.DATE_START)) first_bench, min(p.LOCATION_STATE) st
  from {L}FED_COURTLISTENER_JUDGES j join {L}FED_COURTLISTENER_POSITIONS p on p.PERSON_ID = j.ID and p.POSITION_TYPE like 'jud%'
  join (select distinct PERSON_ID from {L}FED_COURTLISTENER_JUDGE_POLITICAL_AFFILIATIONS where POLITICAL_PARTY in ('d','r')) pa on pa.PERSON_ID = j.ID
  where length(j.NAME_LAST) >= 4 and length(j.NAME_FIRST) >= 3 group by 1,2,3 having first_bench is not null and st is not null
)
select j.person_id, j.first_bench, f.NAME, f.CITY, f.STATE, f.EMPLOYER, f.OCCUPATION, f.TRANSACTION_DT, f.TRANSACTION_AMT
from {L}FED_FEC_INDIV_CONTRIBUTIONS f join j on f.NAME = j.ln || ', ' || j.fn and f.STATE = j.st order by random() limit 10""", "fec_sample_any"), 10)
