import json
from _shared.q import run, open_log
D = "reports/tier1_deep_dive_2026-09-05/E49_contracts_during_ban"
open_log(f"{D}/queries.log")
src = open(f"{D}/queries.py").read()
WIN = src.split('WIN = f"""')[1].split('"""')[0].replace("{SAM}","LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS").replace("{USA}","LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FULL_R2")
out = {}
out["pos_total"] = run(WIN + "select count(*) actions, count(distinct award_key) awards, count(distinct uei) ueis, sum(obl) obl, median(obl) med from hit where obl>0", "positive_total")
# award-level positive sums, top 3 share and without-top-3 shape
out["pos_awards"] = run(WIN + """select award_key, sum(obl) obl from hit where obl>0 group by 1 order by 2 desc""", "positive_award_sums")
# per-award positive money for the histogram (log buckets)
out["pos_award_buckets"] = run(WIN + """, a as (select award_key, uei, sum(obl) obl, iff(min(pop_start)>=min(ban_start),'started during ban','started before ban') kind from hit where obl>0 group by 1,2)
 select kind, case when obl<1000 then 'under $1k' when obl<10000 then '$1k-10k' when obl<100000 then '$10k-100k' when obl<1000000 then '$100k-1M' else '$1M+' end bucket,
 count(*) awards, sum(obl) obl from a group by 1,2 order by 1,2""", "positive_award_buckets")
out["lag_new"] = run(WIN + """, a as (select award_key, min(days_in) days_in, sum(obl) obl, iff(min(pop_start)>=min(ban_start),'started during ban','started before ban') kind from hit where obl>0 group by 1)
 select case when days_in<=7 then '0-7 days' when days_in<=30 then '8-30 days' when days_in<=90 then '31-90 days' when days_in<=365 then '91-365 days' else 'over a year' end lag,
 count(*) awards, sum(obl) obl from a where kind='started during ban' group by 1""", "lag_new_during_ban_awards")
out["uei_pos_new"] = run(WIN + """, a as (select award_key, uei, max(RECIPIENT_NAME) recipient, max(EXCLUDING_AGENCY) excl_by, max(EXCLUSION_TYPE) excl_type, min(ban_start) ban_start, sum(obl) obl, iff(min(pop_start)>=min(ban_start),1,0) new_ from hit where obl>0 group by 1,2)
 select uei, max(recipient) recipient, max(excl_by) excl_by, max(excl_type) excl_type, min(ban_start) ban_start, count(*) awards, sum(obl) obl from a where new_=1 group by 1 order by obl desc""", "positive_by_uei_new_during_ban")
# sanity: was FEDERAL_ACTION_OBLIGATION parse clean? how many in-ban rows failed try_to_number / try_to_date
out["parse"] = run(f"""select count(*) n, sum(iff(try_to_number(FEDERAL_ACTION_OBLIGATION) is null,1,0)) bad_obl, sum(iff(try_to_date(ACTION_DATE) is null,1,0)) bad_date
 from LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FULL_R2 where RECIPIENT_UEI in (select nullif(trim(UEI),'') from LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS where UEI is not null)""", "parse_check")
json.dump(json.loads(json.dumps(out, default=str)), open(f"{D}/results3.json","w"), indent=1)
for k,v in out.items():
    if k=="pos_awards":
        s=[float(r["OBL"]) for r in v]; print(k, len(s), sum(s), "top3", sum(s[:3]), "top5", sum(s[:5]), "median", s[len(s)//2]); continue
    print(k, v)
