"""Hunch 86: Google political advertisers with six-figure spend and no FEC committee.
Run from repo root: PYTHONPATH=reports/politics_probe_2026-09-05 python3 reports/politics_probe_2026-09-05/86_google_ads_no_fec/probe.py"""
from _shared.q import run, open_log
from pathlib import Path
open_log(Path(__file__).with_name("probe.log"))
P = lambda t, r: print(f"\n== {t}") or [print(x) for x in r]

WK = "LIBRARY_MARTS.EDUCATION.EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_WEEKLY_SPEND"
WK_L = "LIBRARY_RAW.LANDING.FED_GOOGLE_POLADS_ADVERTISER_WEEKLY_SPEND"
ST = "LIBRARY_MARTS.EDUCATION.EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_STATS"
GEO = "LIBRARY_MARTS.EDUCATION.EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_GEO_SPEND"
DIM = "LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES_DIM"
PAC = "LIBRARY_MARTS.POLITICS.POLITICS__FED_FEC_PAC_SUMMARY"
NORM = lambda c: f"trim(regexp_replace(regexp_replace(regexp_replace(upper({c}),'[^A-Z0-9 ]',' '),'\\\\b(INC|LLC|CORP|CO|COMMITTEE|THE|FOR|OF|PAC)\\\\b',' '),' +',' '))"

# 1. shape: landing vs mart, cycles, keys
P("weekly landing vs mart", run(f"select 'landing' s, count(*) n, count(distinct advertiser_id) d_adv from {WK_L} union all select 'mart', count(*), count(distinct advertiser_id) from {WK}", "86_wk_counts"))
P("weekly by cycle", run(f"select election_cycle, count(*) n, count(distinct advertiser_id) adv, round(sum(try_to_number(spend_usd,14,2))) usd, min(week_start_date) w0, max(week_start_date) w1 from {WK} group by 1 order by 1", "86_wk_cycle"))
P("stats shape", run(f"select count(*) n, count(distinct advertiser_id) d_adv, count_if(nullif(public_ids_list,'') is not null) with_public_ids, count_if(regions ilike '%US%') us_rows from {ST}", "86_stats_shape"))
P("stats sample w/ public ids", run(f"select advertiser_id, advertiser_name, public_ids_list, regions, spend_usd from {ST} where nullif(public_ids_list,'') is not null order by try_to_number(spend_usd) desc limit 5", "86_stats_sample"))
P("geo sample", run(f"select country, country_subdivision_primary, count(*) n from {GEO} group by 1,2 order by n desc limit 5", "86_geo_sample"))

# 2. six-figure US advertisers, tag whether they carry an FEC id or their name matches a DIM committee name
BASE = f"""
with adv as (select advertiser_id, any_value(advertiser_name) nm, round(sum(try_to_number(spend_usd,14,2))) usd, min(election_cycle) c0, max(election_cycle) c1
  from {WK} group by 1 having usd >= 100000),
st as (select advertiser_id, public_ids_list, regions from {ST} qualify row_number() over (partition by advertiser_id order by try_to_number(spend_usd) desc)=1),
dimn as (select distinct {NORM('cmte_nm')} k from {DIM}),
geo as (select advertiser_id, country_subdivision_primary st from {GEO} where country='US' qualify row_number() over (partition by advertiser_id order by try_to_number(spend_usd,14,2) desc)=1),
tagged as (select a.*, st.regions, st.public_ids_list, g.st top_state,
   regexp_like(coalesce(st.public_ids_list,''),'.*C[0-9]{{8}}.*') has_fec_id,
   d.k is not null name_in_dim, {NORM('a.nm')} nk
  from adv a left join st using (advertiser_id) left join geo g using (advertiser_id) left join dimn d on d.k = {NORM('a.nm')})
"""
P("six-figure advertisers: fec id / name-in-dim split", run(BASE + "select has_fec_id, name_in_dim, count(*) n, round(sum(usd)) usd from tagged where regions ilike '%US%' group by 1,2 order by 1,2", "86_split"))
P("no FEC id, no DIM name: top 15", run(BASE + "select nm, usd, c0, c1, top_state, public_ids_list from tagged where regions ilike '%US%' and not has_fec_id and not name_in_dim order by usd desc limit 15", "86_top_nofec"))
P("no FEC id, no DIM name: by state", run(BASE + "select top_state, count(*) advertisers, round(sum(usd)) usd from tagged where regions ilike '%US%' and not has_fec_id and not name_in_dim group by 1 order by usd desc limit 12", "86_by_state"))
# 3. cross-check the FEC leg exists: pac summary IE column populated
P("pac summary IE populated", run(f"select count(*) n, count(distinct cmte_id) d, count_if(independent_expenditures>0) with_ie, round(sum(independent_expenditures)) ie_usd from {PAC}", "86_pac_ie"))
