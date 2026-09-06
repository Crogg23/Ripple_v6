"""Hunch 35: House FD/PTR index vs committee membership. What the index can and cannot carry. SELECT only."""
import json
from _shared.q import run, open_log
open_log("reports/politics_probe_2026-09-05/35_committee_vs_trades/probe.log")
R = {}
DEDUPE = """fd as (select * from (select t.*, hash(*) h from LIBRARY_RAW.LANDING.FED_HOUSE_FD_PTR_INDEX t) qualify row_number() over (partition by h order by h) = 1)"""
R["ptr_by_year"] = run(f"""with {DEDUPE} select index_year, count(*) ptr_filings, count(distinct last||'|'||first||'|'||statedst) filers
  from fd where filingtype = 'P' group by 1 order by 1""", "ptr_by_year")
# match filer -> legislator on surname + state + district (multi-field, not a bare surname); then -> current House committee seat
MATCH = f"""{DEDUPE},
ptr as (select last, first, statedst, left(statedst,2) st, try_to_number(right(statedst,2)) dist, count(*) n_ptr, max(index_year) last_year
        from fd where filingtype='P' and index_year >= '2023' group by 1,2,3,4,5),
leg as (select distinct bioguide, name_last, name_first, state, try_to_number(district) district from LIBRARY_RAW.LANDING.FED_CONGRESS_LEGISLATORS
        where term_type='rep' and term_end >= '2023-01-01'),
m as (select p.*, l.bioguide, l.name_first, l.name_last
      from ptr p left join leg l on upper(l.name_last)=upper(p.last) and l.state=p.st and l.district=p.dist),
seat as (select distinct bioguide, committee_code, committee_name from LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP
         where committee_code like 'H%' and is_subcommittee='False')"""
R["match_funnel"] = run(f"""with {MATCH}
  select count(*) filers_2023_plus, count(distinct bioguide) matched_to_bioguide, sum(n_ptr) ptr_filings,
         sum(iff(bioguide is not null, n_ptr, 0)) ptr_filings_matched,
         (select count(distinct m.bioguide) from m join seat s on s.bioguide=m.bioguide) matched_on_committee,
         (select count(distinct bioguide) from seat) house_members_on_committees
  from m""", "match_funnel")
R["fanout_check"] = run(f"""with {MATCH} select count(*) pairs_matching_2plus_bioguides from (select last, first, statedst from m group by 1,2,3 having count(distinct bioguide) > 1)""", "fanout_check")
R["eyeball"] = run(f"""with {MATCH} select last, first, statedst, name_last, name_first, bioguide, n_ptr from m where bioguide is not null order by random() limit 5""", "eyeball_5")
R["by_committee"] = run(f"""with {MATCH} select s.committee_code, count(distinct m.bioguide) members_with_ptr, sum(m.n_ptr) ptr_filings
  from m join seat s on s.bioguide=m.bioguide group by 1 order by 3 desc limit 10""", "ptr_by_committee")
json.dump(R, open("reports/politics_probe_2026-09-05/35_committee_vs_trades/results.json","w"), indent=1, default=str)
for k,v in R.items():
    print("==", k)
    for r in v: print("  ", r)
