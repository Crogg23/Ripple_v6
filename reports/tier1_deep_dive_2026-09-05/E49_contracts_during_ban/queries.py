"""E49 - contract actions dated inside a SAM exclusion window. Python door only, SELECT only."""
import json, sys
from _shared.q import run, open_log
D = "reports/tier1_deep_dive_2026-09-05/E49_contracts_during_ban"
open_log(f"{D}/queries.log")

SAM = "LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS"
USA = "LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FULL_R2"

# One exclusion window per (UEI, activation): ban start to ban end, open bans end today.
# Junk activation dates (1908, 2099) are cut to 2000..today.
WIN = f"""
with win as (
  select nullif(trim(UEI),'') uei, ENTITY_NAME, EXCLUDING_AGENCY, EXCLUSION_TYPE, CLASSIFICATION,
         ACTIVATION_DATE ban_start, coalesce(TERMINATION_DATE, current_date) ban_end, TERMINATION_DATE is null open_ban
  from {SAM}
  where nullif(trim(UEI),'') is not null and ACTIVATION_DATE between '2000-01-01' and current_date
),
acts as (
  select try_to_date(ACTION_DATE) action_date, try_to_number(FEDERAL_ACTION_OBLIGATION) obl,
         try_to_number(CURRENT_TOTAL_VALUE_OF_AWARD) cur_val,
         try_to_date(PERIOD_OF_PERFORMANCE_START_DATE) pop_start,
         CONTRACT_AWARD_UNIQUE_KEY award_key, AWARD_ID_PIID piid, AWARDING_AGENCY_NAME agency, AWARDING_SUB_AGENCY_NAME sub_agency,
         RECIPIENT_UEI uei, RECIPIENT_NAME, AWARD_TYPE, NAICS_DESCRIPTION, TRANSACTION_DESCRIPTION, USASPENDING_PERMALINK,
         row_number() over (order by CONTRACT_AWARD_UNIQUE_KEY, ACTION_DATE, FEDERAL_ACTION_OBLIGATION, TRANSACTION_DESCRIPTION) row_id
  from {USA}
  where RECIPIENT_UEI in (select uei from win)
),
hit as (
  -- one row per ACTION: a UEI can carry several overlapping ban windows; keep the earliest window that covers the action
  select a.*, w.ban_start, w.ban_end, w.open_ban, w.EXCLUDING_AGENCY, w.EXCLUSION_TYPE, w.ENTITY_NAME,
         datediff(day, w.ban_start, a.action_date) days_in
  from acts a join win w on w.uei = a.uei
  where a.action_date between w.ban_start and w.ban_end
  qualify row_number() over (partition by a.row_id order by w.ban_start, w.ban_end) = 1
)
"""

out = {}
out["sam_win"] = run(WIN + "select count(*) windows, count(distinct uei) ueis, sum(iff(open_ban,1,0)) open_bans, min(ban_start), max(ban_start) from win", "sam_windows")
out["acts_any"] = run(WIN + "select count(*) actions, count(distinct uei) ueis, count(distinct award_key) awards, sum(obl) obl from acts", "acts_any_time")
out["fanout_check"] = run(WIN.replace("  qualify row_number() over (partition by a.row_id order by w.ban_start, w.ban_end) = 1\n","") + "select count(*) joined_rows, count(distinct row_id) distinct_actions, sum(obl) raw_sum from hit", "fanout_before_dedupe")
out["hit_total"] = run(WIN + """select count(*) actions, count(distinct award_key) awards, count(distinct uei) ueis,
  sum(obl) obl, sum(iff(obl>0,obl,0)) obl_pos, sum(iff(obl<0,obl,0)) obl_neg, sum(iff(obl=0,1,0)) zero_actions,
  min(action_date) first_hit, max(action_date) last_hit from hit""", "hit_total")
# new awards vs modifications: did the award's period of performance start inside the ban?
out["hit_newness"] = run(WIN + """select iff(pop_start >= ban_start, 'started during ban', 'started before ban') kind,
  count(*) actions, count(distinct award_key) awards, count(distinct uei) ueis, sum(obl) obl, sum(iff(obl>0,obl,0)) obl_pos
  from hit group by 1 order by 1""", "hit_newness")
# per-award roll: one row per award x window
out["awards"] = run(WIN + """select award_key, piid, uei, max(RECIPIENT_NAME) recipient, max(ENTITY_NAME) sam_name,
  max(agency) agency, max(sub_agency) sub_agency, max(EXCLUDING_AGENCY) excluding_agency, max(EXCLUSION_TYPE) exclusion_type,
  min(ban_start) ban_start, max(ban_end) ban_end, max(open_ban) open_ban, min(pop_start) pop_start,
  min(action_date) first_action_in_ban, max(action_date) last_action_in_ban, min(days_in) days_in,
  count(*) actions, sum(obl) obl, max(cur_val) cur_val, max(AWARD_TYPE) award_type, max(NAICS_DESCRIPTION) naics,
  max(TRANSACTION_DESCRIPTION) descr, max(USASPENDING_PERMALINK) link,
  iff(min(pop_start) >= min(ban_start), 'started during ban', 'started before ban') kind
  from hit group by 1,2,3 order by obl desc""", "awards_in_ban")
# dollar buckets, so one big award cannot hide the shape
out["buckets"] = run(WIN + """select case when obl <= 0 then 'zero or negative' when obl < 1000 then 'under $1k' when obl < 10000 then '$1k-10k'
  when obl < 100000 then '$10k-100k' when obl < 1000000 then '$100k-1M' else '$1M+' end bucket,
  count(*) actions, count(distinct award_key) awards, sum(obl) obl from hit group by 1""", "buckets")
# days into the ban, monthly
out["timing"] = run(WIN + """select floor(days_in/30) month_in, count(*) actions, sum(iff(obl>0,obl,0)) obl_pos, count(distinct award_key) awards
  from hit group by 1 order by 1""", "timing_months_in")
# by awarding agency
out["agency"] = run(WIN + """select agency, count(*) actions, count(distinct award_key) awards, count(distinct uei) ueis, sum(obl) obl
  from hit group by 1 order by obl desc""", "by_agency")
# by year of action
out["years"] = run(WIN + """select year(action_date) yr, count(*) actions, count(distinct award_key) awards, sum(obl) obl from hit group by 1 order by 1""", "by_year")

# awards whose in-ban actions sit under different windows: began-before under one window, began-during under another
out["straddle"] = run(WIN + """select award_key, max(RECIPIENT_NAME) recipient, count(distinct ban_start) windows, min(ban_start) first_ban, max(ban_start) last_ban, min(pop_start) pop_start,
  sum(iff(pop_start>=ban_start,1,0)) acts_after, sum(iff(pop_start<ban_start,1,0)) acts_before, sum(obl) obl, sum(iff(obl>0,obl,0)) obl_pos
  from hit group by 1 having acts_after>0 and acts_before>0 order by obl_pos desc""", "straddling_awards")
# REBUILD A DIFFERENT WAY: join on CAGE code instead of UEI
CAGE = f"""
with win as (
  select upper(nullif(trim(CAGE_CODE),'')) cage, ACTIVATION_DATE ban_start, coalesce(TERMINATION_DATE, current_date) ban_end
  from {SAM} where nullif(trim(CAGE_CODE),'') is not null and ACTIVATION_DATE between '2000-01-01' and current_date
),
acts as (
  select try_to_date(ACTION_DATE) action_date, try_to_number(FEDERAL_ACTION_OBLIGATION) obl, CONTRACT_AWARD_UNIQUE_KEY award_key,
         upper(trim(CAGE_CODE)) cage, RECIPIENT_UEI uei
  from {USA} where upper(trim(CAGE_CODE)) in (select cage from win)
)
select count(*) actions, count(distinct award_key) awards, count(distinct a.cage) cages, sum(obl) obl, sum(iff(obl>0,obl,0)) obl_pos
from acts a join win w on w.cage=a.cage where a.action_date between w.ban_start and w.ban_end
"""
out["cage_rebuild"] = run(CAGE, "rebuild_via_cage")
out["cage_profile"] = run(f"select count(nullif(trim(CAGE_CODE),'')) filled, count(distinct nullif(trim(CAGE_CODE),'')) dist from {SAM}", "sam_cage_profile")

def clean(o):
    return json.loads(json.dumps(o, default=str))
json.dump(clean(out), open(f"{D}/results.json","w"), indent=1)
for k,v in out.items():
    if k!="awards": print(k, v)
print("awards rows", len(out["awards"]))
for a in out["awards"][:25]: print({k:a[k] for k in ("RECIPIENT","AGENCY","OBL","DAYS_IN","KIND","FIRST_ACTION_IN_BAN","BAN_START","EXCLUSION_TYPE")})
