"""Hunch 33 - the nursing-home chains from NURSINGHOME411 (hunch 2) -> FEC committees (the DIM) and donor EMPLOYER.
Run from repo root: PYTHONPATH=reports/politics_probe_2026-09-05 python3 reports/politics_probe_2026-09-05/33_chain_pacs/probe.py
"""
import json
from pathlib import Path
from _shared.q import run, open_log
HERE = Path(__file__).resolve().parent
open_log(HERE / "probe.log")

NH = "LIBRARY_MARTS.HEALTH.HEALTH__FED_NURSINGHOME411"
PEN = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES"
D = "LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES_DIM"
C2C = "LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEE_TO_CANDIDATE"
I = "LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS"

def norm(col):
    return (f"trim(regexp_replace(regexp_replace(regexp_replace(upper({col}),'[^A-Z0-9 ]',' '),"
            f"'\\\\b(LLC|L L C|INC|INCORPORATED|CORP|CORPORATION|CO|LTD|PC|P C|PA|LP|LLP|PLLC|THE|DBA|GROUP|HOLDINGS)\\\\b',' '),' +',' '))")

# chains: one row per CHAIN_ID, pinned on the id (CHAIN_NAME ilike leaks, per traps)
CHAINS = f"""(select CHAIN_ID, max(CHAIN_NAME) chain_name, {norm('max(CHAIN_NAME)')} cn, count(*) homes
             from {NH} where nullif(trim(CHAIN_ID),'') is not null group by 1)"""

out = {}
# 1. chain side: how many chains, how many carry a multi-word name we can match on
out["chains"] = run(f"""select count(*) chains, sum(homes) homes,
  sum(iff(length(cn)>=10 and cn like '% %',1,0)) multiword, sum(iff(cn not like '% %',1,0)) single_word
  from {CHAINS}""", "chain shape: multi-word vs single-word names")[0]

# 2. DIM side: shape, key check, ambiguity share
out["dim"] = run(f"""select count(*) n, count(distinct CMTE_ID) cmte_ids, sum(iff(IS_AMBIGUOUS,1,0)) ambiguous,
  sum(iff(nullif(trim(CONNECTED_ORG_NM),'') is not null,1,0)) with_connected_org,
  sum(iff(CYCLE is null,1,0)) null_cycle from {D}""", "DIM shape, CMTE_ID as key, ambiguity")[0]

# 3. chain name inside a committee name or its connected org (multi-word chains only; contains, not equals, so 'X PAC' still hits)
out["chain_pacs"] = run(f"""
with c as (select * from {CHAINS} where length(cn)>=10 and cn like '% %'),
     d as (select CMTE_ID, max(CMTE_NM) cmte_nm, max(CONNECTED_ORG_NM) conn, max(CMTE_TP) tp, max(CMTE_DSGN) dsgn, max(CMTE_ST) st,
                  max(ORG_TP) org_tp, boolor_agg(IS_AMBIGUOUS) amb, {norm('max(CMTE_NM)')} nm_n, {norm('max(CONNECTED_ORG_NM)')} conn_n
           from {D} group by 1)
select c.CHAIN_ID, c.chain_name, c.homes, d.CMTE_ID, d.cmte_nm, d.conn, d.tp, d.dsgn, d.st, d.org_tp, d.amb,
  iff(contains(d.conn_n, c.cn),'connected_org','cmte_name') how
from c join d on contains(d.nm_n, c.cn) or contains(d.conn_n, c.cn)
order by c.homes desc""", "chain name in committee name / connected org")

# 4. money those committees moved to candidates (MEMO_CD <> 'X' — the earmark-memo trap)
ids = ",".join(f"'{r['CMTE_ID']}'" for r in out["chain_pacs"]) or "''"
out["pac_money_out"] = run(f"""
select CMTE_ID, count(*) gifts, round(sum(TRANSACTION_AMT)) dollars, count(distinct CAND_ID) candidates,
  min(TRANSACTION_DT) g0, max(TRANSACTION_DT) g1, listagg(distinct CYCLE::int, ',') cycles
from {C2C} where CMTE_ID in ({ids}) and coalesce(MEMO_CD,'') <> 'X' group by 1 order by dollars desc""", "chain PAC -> candidates, memo rows out")

# 5. money those committees took in from individuals
out["pac_money_in"] = run(f"""
select CMTE_ID, count(*) gifts, round(sum(TRANSACTION_AMT)) dollars, count(distinct DONOR_NAME) donors,
  min(TRANSACTION_DATE) g0, max(TRANSACTION_DATE) g1
from {I} where CMTE_ID in ({ids}) group by 1 order by dollars desc""", "individuals -> chain PAC")

# 6. chain name = donor EMPLOYER, every multi-word chain at once, with the chain's fine load next to it
out["by_employer"] = run(f"""
with c as (select * from {CHAINS} where length(cn)>=10 and cn like '% %'),
     f as (select p.CMS_CERTIFICATION_NUMBER_CCN ccn, sum(iff(PENALTY_TYPE='Fine', FINE_AMOUNT, 0)) fine_dollars, sum(iff(PENALTY_TYPE='Fine',1,0)) fines
           from {PEN} p group by 1),
     cf as (select n.CHAIN_ID, sum(f.fine_dollars) fine_dollars, sum(f.fines) fines from {NH} n left join f on f.ccn=n.CMS_CERTIFICATION_NUMBER_CCN group by 1),
     i as (select {norm('EMPLOYER')} emp, STATE, CMTE_ID, DONOR_NAME, TRANSACTION_AMT, TRANSACTION_DATE from {I} where nullif(trim(EMPLOYER),'') is not null)
select c.CHAIN_ID, c.chain_name, c.homes, cf.fines, round(cf.fine_dollars) fine_dollars,
  count(*) gifts, round(sum(i.TRANSACTION_AMT)) dollars, count(distinct i.DONOR_NAME) donors, count(distinct i.CMTE_ID) committees,
  listagg(distinct i.STATE, ',') donor_states, min(i.TRANSACTION_DATE) g0, max(i.TRANSACTION_DATE) g1
from c join i on i.emp=c.cn left join cf on cf.CHAIN_ID=c.CHAIN_ID
group by 1,2,3,4,5 order by dollars desc limit 40""", "chain name = donor employer, with fines")

# 7. eyeball the top 3 employer hits donor by donor, and where the chain's homes actually are
top3 = [r["CHAIN_ID"] for r in out["by_employer"][:3]]
t3 = ",".join(f"'{c}'" for c in top3)
out["eyeball"] = run(f"""
with c as (select * from {CHAINS} where CHAIN_ID in ({t3}))
select c.chain_name, DONOR_NAME, OCCUPATION, CITY, STATE, count(*) gifts, round(sum(TRANSACTION_AMT)) dollars, count(distinct CMTE_ID) committees
from {I} i join c on {norm('i.EMPLOYER')}=c.cn group by 1,2,3,4,5 qualify row_number() over (partition by c.chain_name order by dollars desc)<=8 order by 1, dollars desc""", "top 3 chains, donor by donor")
out["eyeball_homes"] = run(f"""select CHAIN_ID, max(CHAIN_NAME) chain_name, listagg(distinct STATE, ',') home_states, count(*) homes
  from {NH} where CHAIN_ID in ({t3}) group by 1""", "where those 3 chains' homes are")

(HERE / "results.json").write_text(json.dumps(out, indent=1, default=str))
for k, v in out.items():
    print("==", k)
    for r in (v if isinstance(v, list) else [v])[:45]: print(r)
