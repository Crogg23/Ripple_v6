import json
from _shared.q import run, open_log
D = "reports/tier1_deep_dive_2026-09-05/E49_contracts_during_ban"
open_log(f"{D}/queries.log")
import importlib.util, sys
src = open(f"{D}/queries.py").read()
WIN = src.split('WIN = f"""')[1].split('"""')[0]
SAM = "LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS"
USA = "LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FULL_R2"
WIN = WIN.replace("{SAM}", SAM).replace("{USA}", USA)
out = {}
# positive money only, per award, new-during-ban vs pre-ban
out["pos_kind"] = run(WIN + """select iff(pop_start >= ban_start,'started during ban','started before ban') kind,
  count(*) actions, count(distinct award_key) awards, count(distinct uei) ueis, sum(obl) obl, median(obl) med, max(obl) mx
  from hit where obl > 0 group by 1""", "positive_by_kind")
# top 15 positive awards with everything
out["top_pos"] = run(WIN + """select award_key, piid, uei, max(RECIPIENT_NAME) recipient, max(ENTITY_NAME) sam_name, max(agency) agency,
  max(sub_agency) sub_agency, max(EXCLUDING_AGENCY) excl_by, max(EXCLUSION_TYPE) excl_type, min(ban_start) ban_start, max(ban_end) ban_end,
  min(pop_start) pop_start, min(action_date) first_in, min(days_in) days_in, count(*) actions, sum(obl) obl, max(NAICS_DESCRIPTION) naics,
  max(TRANSACTION_DESCRIPTION) descr, max(USASPENDING_PERMALINK) link, iff(min(pop_start)>=min(ban_start),'started during ban','started before ban') kind
  from hit where obl > 0 group by 1,2,3 order by obl desc limit 15""", "top_positive_awards")
# the biggest negative: Treasury
out["top_neg"] = run(WIN + """select award_key, uei, max(RECIPIENT_NAME) recipient, max(agency) agency, min(ban_start) ban_start, min(pop_start) pop_start,
  count(*) actions, sum(obl) obl, max(TRANSACTION_DESCRIPTION) descr from hit where obl < 0 group by 1,2 order by obl limit 8""", "top_negative_awards")
# per-UEI share of positive money: how concentrated
out["uei_pos"] = run(WIN + """select uei, max(RECIPIENT_NAME) recipient, max(EXCLUDING_AGENCY) excl_by, max(EXCLUSION_TYPE) excl_type, min(ban_start) ban_start,
  count(distinct award_key) awards, sum(obl) obl from hit where obl>0 group by 1 order by obl desc""", "positive_by_uei")
# exclusion type of the hits with positive money
out["pos_excl"] = run(WIN + """select EXCLUSION_TYPE, EXCLUDING_AGENCY, count(distinct uei) ueis, count(distinct award_key) awards, sum(obl) obl
  from hit where obl>0 group by 1,2 order by obl desc""", "positive_by_exclusion")
# same-day: how many positive actions land within 7 days of the ban start (paperwork lag)?
out["lag"] = run(WIN + """select case when days_in<=7 then '0-7 days' when days_in<=30 then '8-30 days' when days_in<=90 then '31-90 days'
  when days_in<=365 then '91-365 days' else 'over a year' end lag, count(*) actions, count(distinct award_key) awards, sum(obl) obl
  from hit where obl>0 group by 1""", "positive_lag_buckets")
json.dump(json.loads(json.dumps(out, default=str)), open(f"{D}/results2.json","w"), indent=1)
for k,v in out.items():
    print("==",k)
    for r in v[:15]: print({a:b for a,b in r.items() if a not in ('LINK','AWARD_KEY')})
