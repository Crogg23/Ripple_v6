"""Hunch 15: are banned (SAM-excluded) companies getting disaster-relief contracts?
Every query run for this hunch. Run from repo root: PYTHONPATH=reports/tier1_deep_dive_2026-09-05 python3 .../queries.py [step]
"""
import sys, json
from _shared.q import run, open_log
D = "reports/tier1_deep_dive_2026-09-05/15_banned_disaster_contractors"
open_log(f"{D}/queries.log")
T = "LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FULL_R2"
E = "LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS"
step = sys.argv[1] if len(sys.argv) > 1 else "all"
def save(name, rows):
    json.dump(rows, open(f"{D}/{name}.json", "w"), default=str, indent=1); print(name, len(rows))

# Disaster slice = FEMA as awarding sub-agency, OR a disaster keyword in the description.
KW = "(HURRICANE|DISASTER|FEMA|WILDFIRE|FLOOD|TORNADO|EARTHQUAKE|EMERGENCY RESPONSE|DEBRIS REMOVAL|BLUE ROOF|EMERGENCY MANAGEMENT)"
DIS = f"""(AWARDING_SUB_AGENCY_NAME ilike '%Emergency Management%'
   or regexp_like(upper(coalesce(TRANSACTION_DESCRIPTION,'')), '.*{KW}.*'))"""

if step in ("all", "discover"):
    save("cols_r2", run(f"select column_name, data_type from LIBRARY_RAW.information_schema.columns where table_schema='LANDING' and table_name='FED_USASPENDING_CONTRACTS_FULL_R2' order by ordinal_position", "cols r2"))
    save("cols_excl", run(f"select column_name, data_type from LIBRARY_MARTS.information_schema.columns where table_schema='PROCUREMENT' and table_name='PROCUREMENT__FED_SAM_EXCLUSIONS' order by ordinal_position", "cols excl"))
    # trap check: R2 column case. "recipient_uei" quoted lowercase FAILS; bare RECIPIENT_UEI works (R2 is uppercase, unlike the older USAspending landings)
    save("excl_profile", run(f"""select count(*) n, count(distinct UEI) uei, count(distinct nullif(trim(CAGE_CODE),'')) cage,
        sum(iff(IS_ENTITY_NOT_INDIVIDUAL,1,0)) ents, sum(iff(IS_CURRENTLY_EXCLUDED,1,0)) cur,
        min(ACTIVATION_DATE) mn, max(ACTIVATION_DATE) mx, count(TERMINATION_DATE) term from {E}""", "excl profile"))
    save("excl_class", run(f"select RECORD_STATUS, CLASSIFICATION, count(*) n from {E} group by 1,2 order by 3 desc", "excl class"))
    save("excl_type", run(f"select EXCLUSION_TYPE, count(*) n from {E} group by 1 order by 2 desc", "excl type"))
    save("excl_termraw", run(f"select TERMINATION_DATE_RAW, count(*) n from {E} where TERMINATION_DATE is null group by 1 order by 2 desc limit 5", "excl term raw"))
    save("excl_act_years", run(f"select year(ACTIVATION_DATE) y, count(*) n from {E} group by 1 order by 1", "excl activation years"))

if step in ("all", "slice"):
    # one scan of the 93M-row table: how big is the disaster slice, by sub-agency and by year
    save("slice_agency", run(f"""select AWARDING_SUB_AGENCY_NAME sub, count(*) n,
        sum(try_to_number(FEDERAL_ACTION_OBLIGATION,18,2)) oblig,
        min(try_to_date(ACTION_DATE)) mn, max(try_to_date(ACTION_DATE)) mx
        from {T} where {DIS} group by 1 order by 2 desc limit 40""", "slice by sub-agency"))
    save("slice_year", run(f"""select year(try_to_date(ACTION_DATE)) y,
        iff(AWARDING_SUB_AGENCY_NAME ilike '%Emergency Management%','FEMA','keyword') how,
        count(*) n, sum(try_to_number(FEDERAL_ACTION_OBLIGATION,18,2)) oblig from {T} where {DIS} group by 1,2 order by 1,2""", "slice by year"))
    save("r2_profile", run(f"""select count(*) n, count(distinct RECIPIENT_UEI) uei, count(distinct nullif(trim(CAGE_CODE),'')) cage,
        min(try_to_date(ACTION_DATE)) mn, max(try_to_date(ACTION_DATE)) mx,
        count(distinct CONTRACT_AWARD_UNIQUE_KEY) awards from {T}""", "r2 profile"))

if step in ("all", "join"):
    # the join: disaster slice x exclusions on UEI, then on CAGE, then on exact entity name. One row per (transaction, exclusion record).
    save("matches", run(f"""with d as (
        select CONTRACT_AWARD_UNIQUE_KEY awk, AWARD_ID_PIID piid, try_to_date(ACTION_DATE) act, try_to_date(PERIOD_OF_PERFORMANCE_START_DATE) pstart,
               try_to_number(FEDERAL_ACTION_OBLIGATION,18,2) oblig, try_to_number(CURRENT_TOTAL_VALUE_OF_AWARD,18,2) ctv,
               AWARDING_SUB_AGENCY_NAME sub, RECIPIENT_UEI uei, nullif(trim(CAGE_CODE),'') cage, RECIPIENT_NAME rname,
               upper(trim(RECIPIENT_NAME)) rn, left(TRANSACTION_DESCRIPTION, 120) descr, AWARD_TYPE atype, USASPENDING_PERMALINK link
        from {T} where {DIS})
      select 'UEI' how, d.*, e.SAM_NUMBER sam, e.ENTITY_NAME ename, e.CLASSIFICATION cls, e.EXCLUSION_TYPE etype, e.EXCLUDING_AGENCY eagency,
             e.ACTIVATION_DATE act_on, e.TERMINATION_DATE term_on, e.TERMINATION_DATE_RAW term_raw
      from d join {E} e on e.UEI = d.uei and e.IS_ENTITY_NOT_INDIVIDUAL
      union all
      select 'CAGE', d.*, e.SAM_NUMBER, e.ENTITY_NAME, e.CLASSIFICATION, e.EXCLUSION_TYPE, e.EXCLUDING_AGENCY, e.ACTIVATION_DATE, e.TERMINATION_DATE, e.TERMINATION_DATE_RAW
      from d join {E} e on e.CAGE_CODE = d.cage and e.IS_ENTITY_NOT_INDIVIDUAL and (e.UEI is null or e.UEI <> d.uei)
      union all
      select 'NAME', d.*, e.SAM_NUMBER, e.ENTITY_NAME, e.CLASSIFICATION, e.EXCLUSION_TYPE, e.EXCLUDING_AGENCY, e.ACTIVATION_DATE, e.TERMINATION_DATE, e.TERMINATION_DATE_RAW
      from d join {E} e on upper(trim(e.ENTITY_NAME)) = d.rn and e.IS_ENTITY_NOT_INDIVIDUAL and (e.UEI is null or e.UEI <> d.uei)
           and (e.CAGE_CODE is null or e.CAGE_CODE <> coalesce(d.cage,''))
      order by 1, act""", "disaster x exclusions"))

# matched transactions, one row per transaction, earliest exclusion activation among its matches
MATCHED = f"""with d as (
        select CONTRACT_AWARD_UNIQUE_KEY awk, AWARD_ID_PIID piid, try_to_date(ACTION_DATE) act,
               try_to_number(FEDERAL_ACTION_OBLIGATION,18,2) oblig, try_to_number(CURRENT_TOTAL_VALUE_OF_AWARD,18,2) ctv,
               AWARDING_SUB_AGENCY_NAME sub, RECIPIENT_UEI uei, nullif(trim(CAGE_CODE),'') cage, upper(trim(RECIPIENT_NAME)) rn,
               left(TRANSACTION_DESCRIPTION,120) descr, USASPENDING_PERMALINK link, hash(*) rowkey
        from {T} where {DIS}),
      m as (
        select d.*, e.SAM_NUMBER sam, e.ENTITY_NAME ename, e.EXCLUSION_TYPE etype, e.EXCLUDING_AGENCY eagency, e.ACTIVATION_DATE act_on,
               coalesce(e.TERMINATION_DATE, '2099-12-31'::date) term_on,
               case when e.UEI = d.uei then 'UEI' when e.CAGE_CODE = d.cage then 'CAGE' else 'NAME' end how
        from d join {E} e on e.IS_ENTITY_NOT_INDIVIDUAL and (e.UEI = d.uei or e.CAGE_CODE = d.cage or upper(trim(e.ENTITY_NAME)) = d.rn)),
      one as (
        select rowkey, awk, piid, act, oblig, ctv, sub, uei, rn, descr, link,
               min(how) how, min(act_on) first_act_on, max(act_on) last_act_on,
               max(iff(act between act_on and term_on, 1, 0)) in_window,
               max(iff(act >= act_on, 1, 0)) after_ban_start,
               min(iff(act >= act_on, etype, null)) etype_hit, min(iff(act >= act_on, eagency, null)) eagency_hit,
               min(iff(act >= act_on, act_on, null)) act_on_hit, max(iff(act >= act_on, term_on, null)) term_on_hit,
               count(*) excl_records
        from m group by all)"""

if step in ("all", "window"):
    save("window_summary", run(f"""{MATCHED}
      select how, in_window, after_ban_start, iff(sub ilike '%Emergency Management%','FEMA','other') fema,
             count(*) n, count(distinct uei) recips, count(distinct awk) awards,
             sum(oblig) oblig, sum(greatest(oblig,0)) oblig_pos
      from one group by all order by 1,2,3,4""", "window summary"))
    save("window_year", run(f"""{MATCHED}
      select year(act) y, in_window, count(*) n, count(distinct uei) recips, sum(oblig) oblig
      from one group by all order by 1,2""", "window by year"))
    save("in_window_rows", run(f"""{MATCHED}
      select * from one where after_ban_start = 1 order by act""", "rows on/after ban start"))
    save("company_timeline", run(f"""{MATCHED}
      select uei, rn, min(act) first_award, max(act) last_award, count(*) n, sum(oblig) oblig,
             first_act_on, last_act_on, max(in_window) any_in_window, max(after_ban_start) any_after,
             sum(iff(in_window=1, oblig, 0)) oblig_in_window
      from one group by uei, rn, first_act_on, last_act_on order by oblig desc""", "company timeline"))

if step in ("all", "repro"):
    # try to rebuild the first pass's "26 companies, $169M" several ways
    save("repro", run(f"""with d as (
        select CONTRACT_AWARD_UNIQUE_KEY awk, try_to_number(FEDERAL_ACTION_OBLIGATION,18,2) oblig,
               try_to_number(CURRENT_TOTAL_VALUE_OF_AWARD,18,2) ctv, try_to_number(TOTAL_DOLLARS_OBLIGATED,18,2) tdo,
               AWARDING_SUB_AGENCY_NAME sub, RECIPIENT_UEI uei, upper(trim(RECIPIENT_NAME)) rn
        from {T} where {DIS})
      select 'A uei, entities, all disaster, sum oblig' v, count(distinct d.uei) cos, sum(oblig) dollars from d join {E} e on e.UEI=d.uei and e.IS_ENTITY_NOT_INDIVIDUAL
      union all select 'B uei, entities, FEMA only, sum oblig', count(distinct d.uei), sum(oblig) from d join {E} e on e.UEI=d.uei and e.IS_ENTITY_NOT_INDIVIDUAL where sub ilike '%Emergency Management%'
      union all select 'C uei, entities, all disaster, sum ctv (per transaction)', count(distinct d.uei), sum(ctv) from d join {E} e on e.UEI=d.uei and e.IS_ENTITY_NOT_INDIVIDUAL
      union all select 'D uei, entities, all disaster, ctv once per award', count(distinct uei), sum(ctv) from (select d.uei, d.awk, max(ctv) ctv from d join {E} e on e.UEI=d.uei and e.IS_ENTITY_NOT_INDIVIDUAL group by 1,2)
      union all select 'E uei, entities, all disaster, tdo once per award', count(distinct uei), sum(tdo) from (select d.uei, d.awk, max(tdo) tdo from d join {E} e on e.UEI=d.uei and e.IS_ENTITY_NOT_INDIVIDUAL group by 1,2)
      union all select 'F uei, ALL excl rows incl individuals, all disaster, sum oblig', count(distinct d.uei), sum(oblig) from d join {E} e on e.UEI=d.uei
      union all select 'G uei, entities, FEMA only, ctv once per award', count(distinct uei), sum(ctv) from (select d.uei, d.awk, max(ctv) ctv from d join {E} e on e.UEI=d.uei and e.IS_ENTITY_NOT_INDIVIDUAL where sub ilike '%Emergency Management%' group by 1,2)
      union all select 'H name, entities, all disaster, sum oblig', count(distinct d.rn), sum(oblig) from d join {E} e on upper(trim(e.ENTITY_NAME))=d.rn and e.IS_ENTITY_NOT_INDIVIDUAL
      union all select 'I uei, entities, FEMA only, tdo once per award', count(distinct uei), sum(tdo) from (select d.uei, d.awk, max(tdo) tdo from d join {E} e on e.UEI=d.uei and e.IS_ENTITY_NOT_INDIVIDUAL where sub ilike '%Emergency Management%' group by 1,2)
      """, "repro first pass"))
    # is the exclusions mart deduped? how many records per UEI
    save("excl_per_uei", run(f"select cnt, count(*) ueis from (select UEI, count(*) cnt from {E} where UEI is not null group by 1) group by 1 order by 1 limit 10", "excl records per uei"))
