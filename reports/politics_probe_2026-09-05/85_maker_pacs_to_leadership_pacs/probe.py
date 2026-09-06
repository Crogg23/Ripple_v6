"""Hunch 85: Open Payments makers -> their corporate PACs (DIM CONNECTED_ORG_NM) -> money into leadership PACs.
Run from repo root: PYTHONPATH=reports/politics_probe_2026-09-05 python3 reports/politics_probe_2026-09-05/85_maker_pacs_to_leadership_pacs/probe.py"""
from _shared.q import run, open_log
from pathlib import Path
open_log(Path(__file__).with_name("probe.log"))
P = lambda t, r: print(f"\n== {t}") or [print(x) for x in r]

OP = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS"
DIM = "LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES_DIM"
C2C = "LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEE_TO_CANDIDATE"
LP = "LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_LEADERSHIP_PAC"
LEG = "LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_LEGISLATORS"
# name fold: upper, strip punctuation, drop corporate suffixes, squeeze spaces
NORM = lambda c: f"trim(regexp_replace(regexp_replace(regexp_replace(upper({c}),'[^A-Z0-9 ]',' '),'\\\\b(INC|INCORPORATED|LLC|L L C|CORP|CORPORATION|CO|COMPANY|LTD|LIMITED|LP|PLC|USA|US|THE)\\\\b',' '),' +',' '))"

# 1. DIM shape: ids repeat? cycle null? ambiguous?
P("dim shape", run(f"select count(*) n, count(distinct cmte_id) d_id, count_if(cycle is null) cycle_null, count_if(is_ambiguous) amb, count_if(nullif(connected_org_nm,'') is not null) with_org from {DIM}", "85_dim_shape"))
# 2. leadership pac table shape
P("leadership pac shape", run(f"select count(*) n, count(distinct fec_committee_id) d_cmte, count(distinct fec_candidate_id) d_cand, min(fec_election_yr) y0, max(fec_election_yr) y1, listagg(distinct cmte_dsgn,',') dsgn from {LP}", "85_lp_shape"))
# 3. c2c: transaction types + memo trap
P("c2c tp x memo", run(f"select transaction_tp, memo_cd, count(*) n, round(sum(transaction_amt)) usd from {C2C} group by 1,2 order by n desc limit 12", "85_c2c_tp"))
# 4. top payers, folded
P("top 15 payers folded", run(f"select {NORM('applicable_manufacturer_or_applicable_gpo_making_payment_name')} payer, count(distinct applicable_manufacturer_or_applicable_gpo_making_payment_name) spellings, round(sum(total_amount_of_payment_usdollars)) usd from {OP} group by 1 order by 3 desc limit 15", "85_top_payers"))

# 5. match: payer folded name == DIM connected org folded name (multi-word only)
MATCH = f"""
with payer as (select {NORM('applicable_manufacturer_or_applicable_gpo_making_payment_name')} k, round(sum(total_amount_of_payment_usdollars)) op_usd
  from {OP} group by 1 having k like '% %'),
org as (select distinct cmte_id, {NORM('connected_org_nm')} k, cmte_nm, cmte_tp, is_ambiguous from {DIM} where nullif(connected_org_nm,'') is not null),
hit as (select p.k, p.op_usd, o.cmte_id, o.cmte_nm, o.cmte_tp, o.is_ambiguous from payer p join org o using (k))
"""
P("match count", run(MATCH + "select count(distinct k) makers, count(distinct cmte_id) pacs, count_if(is_ambiguous) amb_rows, count(*) n_rows from hit", "85_match_count"))
P("match sample top 12 by OP $", run(MATCH + "select k, op_usd, cmte_id, cmte_nm, cmte_tp, is_ambiguous from hit qualify row_number() over (partition by k order by cmte_id)=1 order by op_usd desc limit 12", "85_match_sample"))

# 6. the number: maker PAC -> leadership PAC (OTHER_ID = leadership PAC id), memo excluded
FLOW = MATCH + f""",
lp as (select distinct fec_committee_id, fec_candidate_id from {LP}),
flow as (select h.k maker, h.op_usd, c.cmte_id giver, c.other_id lp_id, lp.fec_candidate_id cand, c.cycle, c.transaction_amt
  from hit h join {C2C} c on c.cmte_id = h.cmte_id join lp on lp.fec_committee_id = c.other_id
  where coalesce(c.memo_cd,'') <> 'X' and c.transaction_tp in ('24K','24Z'))
"""
P("flow total", run(FLOW + "select count(*) n, count(distinct maker) makers, count(distinct lp_id) lpacs, count(distinct cand) cands, round(sum(transaction_amt)) usd, min(cycle) c0, max(cycle) c1 from flow", "85_flow_total"))
P("flow by cycle", run(FLOW + "select cycle, count(*) n, round(sum(transaction_amt)) usd from flow group by 1 order by 1", "85_flow_cycle"))
P("top makers -> leadership PACs", run(FLOW + """select maker, op_usd, count(distinct lp_id) lpacs, round(sum(transaction_amt)) usd from flow group by 1,2 order by usd desc limit 10""", "85_flow_makers"))
P("top candidate leadership PACs fed by makers", run(FLOW + f"""select f.cand, any_value(l.name_official_full) who, any_value(l.party) p, any_value(l.state) st, count(distinct f.maker) makers, round(sum(f.transaction_amt)) usd
from flow f left join (select distinct trim(v.value::string) fid, name_official_full, party, state from {LEG}, lateral split_to_table(regexp_replace(fec_ids,'[\\\\[\\\\]"'' ]',''),',') v) l on l.fid=f.cand
group by 1 order by usd desc limit 10""", "85_flow_cands"))
