"""Hunch 36 - nursing-chain / DME money -> the four committees that oversee CMS (House E&C, Ways & Means, Senate Finance, HELP).
Donor side reuses hunch 33's legs: chain name = donor EMPLOYER, plus the chain PACs. Hunch 32's DME leg came back empty and is carried as a check.
Run from repo root: PYTHONPATH=reports/politics_probe_2026-09-05 python3 reports/politics_probe_2026-09-05/36_industry_to_overseers/probe.py
"""
import json
from pathlib import Path
from _shared.q import run, open_log
HERE = Path(__file__).resolve().parent
open_log(HERE / "probe.log")

NH = "LIBRARY_MARTS.HEALTH.HEALTH__FED_NURSINGHOME411"
D = "LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES_DIM"
C2C = "LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEE_TO_CANDIDATE"
I = "LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS"
MF = "LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_FEC_ID"
CM = "LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP"

def norm(col):
    return (f"trim(regexp_replace(regexp_replace(regexp_replace(upper({col}),'[^A-Z0-9 ]',' '),"
            f"'\\\\b(LLC|L L C|INC|INCORPORATED|CORP|CORPORATION|CO|LTD|PC|P C|PA|LP|LLP|PLLC|THE|DBA|GROUP|HOLDINGS)\\\\b',' '),' +',' '))")
CHAINS = f"""(select CHAIN_ID, max(CHAIN_NAME) chain_name, {norm('max(CHAIN_NAME)')} cn, count(*) homes
             from {NH} where nullif(trim(CHAIN_ID),'') is not null group by 1 having length(cn)>=10 and cn like '% %')"""
# hunch 33's committee-name matches, minus the ones the eye rejected (Front Porch = two progressive PACs; Encompass/Acadia = substring of a different company)
CHAIN_PACS = "('C00292094','C00513192','C00434233','C00421735','C00459008','C00421420','C00347955','C00423871','C00242271','C00067231')"
DME = ["SUNSHINE SENIOR SOLUTIONS","JL WEBB DME","ABSOLUTE MEDICAL SUPPLIES SERVICES","MAIN STREET DME","SOUTHEASTERN MEDEQUIP",
       "EXPRESS HEALTHCARE","LIFELINE MEDICAL SUPPLY","TEMECULA MEDICAL SUPPLIES","ALMAZ MED SUPPLY"]
DME_LIST = ",".join(f"'{n}'" for n in DME)

out = {}
# 1. which committee codes are the overseers, and is the membership table one snapshot
out["codes"] = run(f"""select COMMITTEE_CODE, COMMITTEE_NAME, count(*) members, count(distinct BIOGUIDE) bioguides
  from {CM} where IS_SUBCOMMITTEE='False' and (COMMITTEE_NAME ilike '%Energy and Commerce%' or COMMITTEE_NAME ilike '%Ways and Means%'
   or COMMITTEE_NAME ilike '%Committee on Finance%' or COMMITTEE_NAME ilike '%Health, Education, Labor%')
  group by 1,2 order by 1""", "the four oversight committees")
CODES = ",".join(f"'{r['COMMITTEE_CODE']}'" for r in out["codes"])

# overseer members -> their FEC candidate ids -> every committee in the DIM tied to that candidate
OVERSEER_CMTES = f"""(select d.CMTE_ID, m.BIOGUIDE, m.FULL_NAME, listagg(distinct c.COMMITTEE_CODE, ',') within group (order by c.COMMITTEE_CODE) codes
   from {CM} c join {MF} m on m.BIOGUIDE=c.BIOGUIDE join {D} d on d.CAND_ID=m.FEC_ID
   where c.IS_SUBCOMMITTEE='False' and c.COMMITTEE_CODE in ({CODES}) group by 1,2,3)"""
# 2. key checks on that chain: members, members with an FEC id, committees reached
out["overseers"] = run(f"""
with c as (select distinct BIOGUIDE from {CM} where IS_SUBCOMMITTEE='False' and COMMITTEE_CODE in ({CODES})),
     m as (select BIOGUIDE, count(*) n, count(distinct FEC_ID) fec_ids from {MF} group by 1)
select count(*) members, sum(iff(m.BIOGUIDE is not null,1,0)) with_fec_id, max(m.n) max_rows_per_member,
  (select count(*) from {OVERSEER_CMTES}) cmtes_reached, (select count(distinct CMTE_ID) from {OVERSEER_CMTES}) distinct_cmtes
from c left join m on m.BIOGUIDE=c.BIOGUIDE""", "overseers: members -> FEC id -> committees, key checks")[0]

# 3. chain employees' money, split by where it landed
out["chain_indiv"] = run(f"""
with c as (select * from {CHAINS}),
     i as (select CMTE_ID, {norm('EMPLOYER')} emp, TRANSACTION_AMT from {I} where nullif(trim(EMPLOYER),'') is not null),
     g as (select i.CMTE_ID, count(*) gifts, sum(i.TRANSACTION_AMT) dollars, count(distinct c.CHAIN_ID) chains from i join c on c.cn=i.emp group by 1),
     k as (select g.*, d.CAND_ID, d.CMTE_TP, o.BIOGUIDE from g left join {D} d on d.CMTE_ID=g.CMTE_ID left join {OVERSEER_CMTES} o on o.CMTE_ID=g.CMTE_ID)
select case when BIOGUIDE is not null then 'overseer member' when nullif(CAND_ID,'') is not null then 'other candidate'
            when CMTE_TP in ('Q','N','O','V','W') then 'PAC / super PAC' else 'party / other' end bucket,
  count(*) committees, sum(gifts) gifts, round(sum(dollars)) dollars
from k group by 1 order by dollars desc""", "chain employees' money by recipient bucket")

# 4. the same split for ALL individual money — the baseline the hunch has to beat
out["baseline"] = run(f"""
with g as (select CMTE_ID, count(*) gifts, sum(TRANSACTION_AMT) dollars from {I} group by 1),
     k as (select g.*, d.CAND_ID, d.CMTE_TP, o.BIOGUIDE from g left join {D} d on d.CMTE_ID=g.CMTE_ID left join {OVERSEER_CMTES} o on o.CMTE_ID=g.CMTE_ID)
select case when BIOGUIDE is not null then 'overseer member' when nullif(CAND_ID,'') is not null then 'other candidate'
            when CMTE_TP in ('Q','N','O','V','W') then 'PAC / super PAC' else 'party / other' end bucket,
  count(*) committees, sum(gifts) gifts, round(sum(dollars)) dollars
from k group by 1 order by dollars desc""", "all individual money by the same buckets")

# 5. chain PACs -> candidates, memo rows out, split the same way
out["chain_pac"] = run(f"""
with x as (select CMTE_ID, CAND_ID, TRANSACTION_AMT from {C2C} where CMTE_ID in {CHAIN_PACS} and coalesce(MEMO_CD,'')<>'X' and nullif(CAND_ID,'') is not null),
     o as (select distinct m.FEC_ID cand_id from {CM} c join {MF} m on m.BIOGUIDE=c.BIOGUIDE where c.IS_SUBCOMMITTEE='False' and c.COMMITTEE_CODE in ({CODES}))
select iff(o.cand_id is not null,'overseer member','other candidate') bucket, count(*) gifts, round(sum(x.TRANSACTION_AMT)) dollars, count(distinct x.CAND_ID) candidates
from x left join o on o.cand_id=x.CAND_ID group by 1 order by dollars desc""", "chain PACs -> overseer vs other candidates")
out["pac_baseline"] = run(f"""
with x as (select CAND_ID, TRANSACTION_AMT from {C2C} where coalesce(MEMO_CD,'')<>'X' and nullif(CAND_ID,'') is not null),
     o as (select distinct m.FEC_ID cand_id from {CM} c join {MF} m on m.BIOGUIDE=c.BIOGUIDE where c.IS_SUBCOMMITTEE='False' and c.COMMITTEE_CODE in ({CODES}))
select iff(o.cand_id is not null,'overseer member','other candidate') bucket, count(*) gifts, round(sum(x.TRANSACTION_AMT)) dollars, count(distinct x.CAND_ID) candidates
from x left join o on o.cand_id=x.CAND_ID group by 1 order by dollars desc""", "all committee->candidate money, same split")

# 6. who on the oversight committees gets the most chain money, and from which chain
out["top_members"] = run(f"""
with c as (select * from {CHAINS}),
     i as (select CMTE_ID, {norm('EMPLOYER')} emp, TRANSACTION_AMT from {I} where nullif(trim(EMPLOYER),'') is not null),
     g as (select i.CMTE_ID, c.chain_name, count(*) gifts, sum(i.TRANSACTION_AMT) dollars from i join c on c.cn=i.emp group by 1,2),
     p as (select x.CMTE_ID, d.CONNECTED_ORG_NM chain_name, count(*) gifts, sum(x.TRANSACTION_AMT) dollars
           from {C2C} x join {D} d on d.CMTE_ID=x.CMTE_ID join {OVERSEER_CMTES} o on o.CMTE_ID=d.CMTE_ID  -- placeholder, replaced below
           where 1=0 group by 1,2)
select o.FULL_NAME, o.codes, round(sum(g.dollars)) dollars, sum(g.gifts) gifts,
  max_by(g.chain_name, g.dollars) top_chain, round(max(g.dollars)) top_chain_dollars
from g join {OVERSEER_CMTES} o on o.CMTE_ID=g.CMTE_ID group by 1,2 order by dollars desc limit 15""", "overseer members by chain-employee dollars")

# 7. eyeball the top 3 member rows: the actual donors behind them
top3 = [r["FULL_NAME"] for r in out["top_members"][:3]]
t3 = ",".join("'" + n.replace("'", "''") + "'" for n in top3)
out["eyeball"] = run(f"""
with c as (select * from {CHAINS}),
     o as (select * from {OVERSEER_CMTES} where FULL_NAME in ({t3}))
select o.FULL_NAME, c.chain_name, i.DONOR_NAME, i.OCCUPATION, i.CITY, i.STATE, count(*) gifts, round(sum(i.TRANSACTION_AMT)) dollars,
  min(i.TRANSACTION_DATE) g0, max(i.TRANSACTION_DATE) g1, listagg(distinct i.TRANSACTION_TYPE, ',') tx_types
from {I} i join o on o.CMTE_ID=i.CMTE_ID join c on c.cn={norm('i.EMPLOYER')}
group by 1,2,3,4,5,6 qualify row_number() over (partition by o.FULL_NAME order by dollars desc)<=5 order by 1, dollars desc""", "top 3 members: the donors behind the money")

# 8. the DME leg, for the record
out["dme"] = run(f"""select count(*) gifts, round(sum(TRANSACTION_AMT)) dollars, count(distinct CMTE_ID) committees
  from {I} where {norm('EMPLOYER')} in ({DME_LIST}) or {norm('DONOR_NAME')} in ({DME_LIST})""", "the nine DME names, any side")[0]

(HERE / "results.json").write_text(json.dumps(out, indent=1, default=str))
for k, v in out.items():
    print("==", k)
    for r in (v if isinstance(v, list) else [v])[:45]: print(r)
