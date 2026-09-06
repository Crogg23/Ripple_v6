"""Hunch 32 - LEIE-excluded org names -> FEC individual-contribution EMPLOYER / org DONOR_NAME / committee treasurer+connected org.
Run from repo root: PYTHONPATH=reports/politics_probe_2026-09-05 python3 reports/politics_probe_2026-09-05/32_excluded_donors/probe.py
"""
import json, sys
from pathlib import Path
from _shared.q import run, open_log
HERE = Path(__file__).resolve().parent
open_log(HERE / "probe.log")

L = "LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE"
I = "LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS"
D = "LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES_DIM"

# one normalizer for both sides: upper, strip punctuation, drop corp suffixes, squeeze spaces
def norm(col):
    return (f"trim(regexp_replace(regexp_replace(regexp_replace(upper({col}),'[^A-Z0-9 ]',' '),"
            f"'\\\\b(LLC|L L C|INC|INCORPORATED|CORP|CORPORATION|CO|LTD|PC|P C|PA|LP|LLP|PLLC|THE|DBA)\\\\b',' '),' +',' '))")

out = {}
# 1. LEIE org side: what a "name" is here
out["leie_orgs"] = run(f"""select count(*) n, count(distinct nullif(trim(BUSINESS_NAME),'')) names,
  count(distinct iff(length({norm('BUSINESS_NAME')})>=10 and {norm('BUSINESS_NAME')} like '% %', {norm('BUSINESS_NAME')}, null)) multiword_names,
  min(EXCLUSION_DATE) d0, max(EXCLUSION_DATE) d1
  from {L} where nullif(trim(BUSINESS_NAME),'') is not null""", "LEIE org names: total vs multi-word")[0]

# 2. FEC indiv side: shape, key check, employer fill
out["indiv"] = run(f"""select count(*) n, count(distinct SUB_ID) sub_ids, min(TRANSACTION_DATE) d0, max(TRANSACTION_DATE) d1,
  sum(iff(nullif(trim(EMPLOYER),'') is null,1,0)) blank_employer,
  sum(iff(ENTITY_TYPE='IND',1,0)) ind_rows, sum(iff(ENTITY_TYPE<>'IND',1,0)) non_ind_rows
  from {I}""", "indiv shape, SUB_ID as key, employer blanks")[0]

# 3. LEIE org name = donor EMPLOYER (multi-word only)
out["by_employer"] = run(f"""
with e as (select {norm('BUSINESS_NAME')} bn, min(EXCLUSION_DATE) excl, max(STATE) st, count(*) excl_rows
           from {L} where nullif(trim(BUSINESS_NAME),'') is not null group by 1
           having length(bn)>=10 and bn like '% %'),
     i as (select {norm('EMPLOYER')} emp, STATE, CMTE_ID, DONOR_NAME, TRANSACTION_AMT, TRANSACTION_DATE, TRANSACTION_TYPE from {I}
           where nullif(trim(EMPLOYER),'') is not null)
select e.bn, e.st leie_st, e.excl, count(*) gifts, round(sum(i.TRANSACTION_AMT)) dollars,
  count(distinct i.DONOR_NAME) donors, count(distinct i.CMTE_ID) committees,
  sum(iff(i.STATE=e.st,1,0)) same_state_gifts, min(i.TRANSACTION_DATE) g0, max(i.TRANSACTION_DATE) g1
from e join i on i.emp=e.bn group by 1,2,3 order by dollars desc limit 40""", "LEIE org = donor employer, per name")

# 4. LEIE org name = DONOR_NAME on non-individual rows
out["by_donor_org"] = run(f"""
with e as (select {norm('BUSINESS_NAME')} bn, min(EXCLUSION_DATE) excl, max(STATE) st from {L}
           where nullif(trim(BUSINESS_NAME),'') is not null group by 1 having length(bn)>=10 and bn like '% %'),
     i as (select {norm('DONOR_NAME')} dn, STATE, CMTE_ID, TRANSACTION_AMT, ENTITY_TYPE from {I} where ENTITY_TYPE<>'IND')
select e.bn, e.st leie_st, e.excl, count(*) gifts, round(sum(i.TRANSACTION_AMT)) dollars, count(distinct i.CMTE_ID) committees,
  sum(iff(i.STATE=e.st,1,0)) same_state_gifts, listagg(distinct i.ENTITY_TYPE, ',') etypes
from e join i on i.dn=e.bn group by 1,2,3 order by dollars desc limit 20""", "LEIE org = org donor name")

# 5. LEIE org name = committee CONNECTED_ORG_NM or CMTE_NM (the DIM, not the raw table)
out["by_committee"] = run(f"""
with e as (select {norm('BUSINESS_NAME')} bn, min(EXCLUSION_DATE) excl, max(STATE) st from {L}
           where nullif(trim(BUSINESS_NAME),'') is not null group by 1 having length(bn)>=10 and bn like '% %')
select e.bn, e.st leie_st, e.excl, d.CMTE_ID, d.CMTE_NM, d.CONNECTED_ORG_NM, d.CMTE_ST, d.CMTE_TP, d.IS_AMBIGUOUS
from e join {D} d on {norm('d.CONNECTED_ORG_NM')}=e.bn or {norm('d.CMTE_NM')}=e.bn
order by 3 desc limit 20""", "LEIE org = committee name / connected org")

# 6. the nine named suppliers from hunch 23 (8 banned + Almaz), both donor-side columns
NINE = ["SUNSHINE SENIOR SOLUTIONS","JL WEBB DME","ABSOLUTE MEDICAL SUPPLIES SERVICES","MAIN STREET DME","SOUTHEASTERN MEDEQUIP",
        "EXPRESS HEALTHCARE","LIFELINE MEDICAL SUPPLY","TEMECULA MEDICAL SUPPLIES","ALMAZ MED SUPPLY"]
lst = ",".join(f"'{n}'" for n in NINE)
out["nine"] = run(f"""
select nm, side, count(*) gifts, round(sum(TRANSACTION_AMT)) dollars, count(distinct DONOR_NAME) donors, count(distinct CMTE_ID) committees,
  listagg(distinct STATE, ',') states, min(TRANSACTION_DATE) g0, max(TRANSACTION_DATE) g1
from (
  select {norm('EMPLOYER')} nm, 'employer' side, * from {I} where {norm('EMPLOYER')} in ({lst})
  union all
  select {norm('DONOR_NAME')} nm, 'donor_name' side, * from {I} where {norm('DONOR_NAME')} in ({lst})
) group by 1,2 order by dollars desc""", "the nine DME names as employer / donor")

# 7. eyeball: the top 3 employer hits, donor by donor (small: only the matched rows)
top3 = [r["BN"] for r in out["by_employer"][:3]]
t3 = ",".join(f"'{b}'" for b in top3)
out["eyeball"] = run(f"""
select {norm('EMPLOYER')} emp, DONOR_NAME, OCCUPATION, CITY, STATE, count(*) gifts, round(sum(TRANSACTION_AMT)) dollars,
  count(distinct CMTE_ID) committees, min(TRANSACTION_DATE) g0, max(TRANSACTION_DATE) g1
from {I} where {norm('EMPLOYER')} in ({t3}) group by 1,2,3,4,5 order by 1, dollars desc""", "top 3 employer hits, donor by donor")

# 8. what those top-3 LEIE rows actually are (who was excluded, where, why)
out["eyeball_leie"] = run(f"""select {norm('BUSINESS_NAME')} bn, BUSINESS_NAME, STATE, CITY, EXCLUSION_TYPE, EXCLUSION_DATE, NPI
  from {L} where {norm('BUSINESS_NAME')} in ({t3}) order by 1, EXCLUSION_DATE""", "the LEIE side of the top 3")

def default(o):
    return str(o)
(HERE / "results.json").write_text(json.dumps(out, indent=1, default=default))
for k, v in out.items():
    print("==", k)
    for r in (v if isinstance(v, list) else [v])[:45]: print(r)
