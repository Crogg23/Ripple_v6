"""Hunch 84: independent expenditures for/against members of Energy & Commerce, Ways & Means, Senate Finance.
Run from repo root: PYTHONPATH=reports/politics_probe_2026-09-05 python3 reports/politics_probe_2026-09-05/84_ie_at_cms_overseers/probe.py"""
from _shared.q import run, open_log
from pathlib import Path
open_log(Path(__file__).with_name("probe.log"))
P = lambda t, r: print(f"\n== {t}") or [print(x) for x in r]

IE_M = "LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES"
IE_L = "LIBRARY_RAW.LANDING.FED_FEC_INDEPENDENT_EXPENDITURES"
MEM = "LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP"
LEG = "LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_LEGISLATORS"
DIM = "LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES_DIM"

# 1. landing vs mart: rows, distinct tran keys, cycles
P("ie landing vs mart", run(f"""
select 'landing' src, count(*) n, count(distinct file_num||'|'||tran_id) tran_keys, min(fec_election_yr) y0, max(fec_election_yr) y1, count(distinct cycle_file) cycle_files from {IE_L}
union all select 'mart', count(*), count(distinct file_num||'|'||tran_id), min(fec_election_yr), max(fec_election_yr), null from {IE_M}""", "84_ie_counts"))
P("ie mart by year", run(f"select fec_election_yr, count(*) n, sum(try_to_number(exp_amo,14,2)) usd from {IE_M} group by 1 order by 1", "84_ie_by_year"))
P("ie sample", run(f"select cand_id, cand_name, spe_id, spe_nam, sup_opp, exp_amo, exp_date, amndt_ind, file_num, prev_file_num, tran_id from {IE_M} limit 5", "84_ie_sample"))

# 2. committee roster: which codes are the three committees
P("committee codes", run(f"""select committee_code, committee_name, is_subcommittee, count(*) members, count(distinct bioguide) d_bioguide
from {MEM} where committee_name ilike '%energy and commerce%' or committee_name ilike '%ways and means%' or committee_name ilike '%finance%'
group by 1,2,3 order by 1""", "84_cmte_codes"))

# 3. legislators: FEC_IDS shape, legislator_set
P("legislator sets + fec_ids sample", run(f"select legislator_set, count(*) n, count(distinct bioguide) d, count_if(nullif(fec_ids,'') is not null) with_fec, any_value(fec_ids) sample_ids from {LEG} group by 1", "84_leg_sets"))

# 4. members of the three parent committees -> their FEC candidate ids
ROSTER = f"""
with mem as (select distinct bioguide, committee_name from {MEM}
  where is_subcommittee in ('false','False','0','') and (committee_code in ('HSIF','HSWM','SSFI')
     or committee_name in ('House Committee on Energy and Commerce','House Committee on Ways and Means','Senate Committee on Finance'))),
leg as (select distinct bioguide, name_official_full, party, state, trim(f.value::string) fec_id
  from {LEG}, lateral split_to_table(regexp_replace(fec_ids,'[\\\\[\\\\]"'' ]',''), ',') f where nullif(fec_ids,'') is not null),
roster as (select m.committee_name, l.* from mem m join leg l using (bioguide) where l.fec_id <> '')
"""
P("roster size", run(ROSTER + "select committee_name, count(distinct bioguide) members, count(distinct fec_id) fec_ids from roster group by 1", "84_roster"))

# 5. the number: IE $ for/against roster members, dedup amended filings (drop any file_num that a later filing supersedes)
BASE = ROSTER + f""",
ie as (select * from {IE_M} where file_num not in (select prev_file_num from {IE_M} where prev_file_num is not null))
"""
P("IE by committee x sup_opp (all years, dedup)", run(BASE + """
select r.committee_name, ie.sup_opp, count(*) n, count(distinct r.bioguide) members_hit, round(sum(try_to_number(ie.exp_amo,14,2))) usd
from ie join roster r on ie.cand_id = r.fec_id group by 1,2 order by 1,2""", "84_ie_by_cmte"))
P("IE by year (roster only)", run(BASE + """
select ie.fec_election_yr, ie.sup_opp, round(sum(try_to_number(ie.exp_amo,14,2))) usd, count(distinct r.bioguide) members
from ie join roster r on ie.cand_id = r.fec_id group by 1,2 order by 1,2""", "84_ie_roster_by_year"))
P("top 10 spenders at roster, with DIM org", run(BASE + f"""
select ie.spe_id, any_value(ie.spe_nam) spender, any_value(d.cmte_tp) tp, any_value(d.connected_org_nm) org, any_value(d.is_ambiguous) amb,
  round(sum(iff(ie.sup_opp='S',try_to_number(ie.exp_amo,14,2),0))) usd_for, round(sum(iff(ie.sup_opp='O',try_to_number(ie.exp_amo,14,2),0))) usd_against,
  count(distinct r.bioguide) members
from ie join roster r on ie.cand_id = r.fec_id
left join (select cmte_id, any_value(cmte_tp) cmte_tp, any_value(connected_org_nm) connected_org_nm, max(is_ambiguous::int)::boolean is_ambiguous from {DIM} group by 1) d on d.cmte_id = ie.spe_id
group by 1 order by usd_for+usd_against desc limit 10""", "84_top_spenders"))
P("top 10 targets", run(BASE + """
select r.name_official_full, r.party, r.state, r.committee_name, round(sum(iff(ie.sup_opp='S',try_to_number(ie.exp_amo,14,2),0))) usd_for, round(sum(iff(ie.sup_opp='O',try_to_number(ie.exp_amo,14,2),0))) usd_against
from ie join roster r on ie.cand_id = r.fec_id group by 1,2,3,4 order by usd_for+usd_against desc limit 10""", "84_top_targets"))
