"""Hunch 34: member office spend (MRA disbursements) vs redlined-zone toxic-site density.
No congressional-district geometry table exists in the warehouse (checked information_schema for DISTRICT/CONGRESS/TIGER/CD),
so the redlining side (hunch 22, city level) is rolled to STATE and compared to member spend per office-year by state.
Run from repo root: PYTHONPATH=reports/politics_probe_2026-09-05 python3 reports/politics_probe_2026-09-05/34_member_spend_vs_redlined/probe.py
"""
import json, sys, collections, math
from pathlib import Path
from _shared.q import run, open_log
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
open_log(HERE / "probe.log")
out = {}
if (HERE / "results.json").exists():
    out.update(json.load(open(HERE / "results.json")))
def q(k, sql):
    if k in out: return
    out[k] = run(sql, k)
    json.dump(out, open(HERE / "results.json", "w"), default=str, indent=1)

# Is there a district geometry anywhere? (name search across both catalogs)
q("district_geo_tables", """select table_catalog, table_schema, table_name, row_count from LIBRARY_RAW.information_schema.tables
 where (table_name ilike '%DISTRICT%' or table_name ilike '%CONGRESS%' or table_name ilike '%TIGER%' or table_name ilike '%\\_CD%' or table_name ilike 'XC\\_%')
 union all select table_catalog, table_schema, table_name, row_count from LIBRARY_MARTS.information_schema.tables
 where (table_name ilike '%DISTRICT%' or table_name ilike '%CONGRESS%' or table_name ilike '%TIGER%' or table_name ilike '%\\_CD%') order by 3""")

# Member office spend per office-year (detail rows only, try_to_number), state via legislator name match (last + first initial, unique).
q("spend_by_state", """
with offices as (
  select left(C_ORGANIZATION,4) yr, regexp_replace(C_ORGANIZATION, '^[0-9]{4} HON\\\\. ', '') office,
    sum(try_to_number(AMOUNT)) amt, count(*) n
  from LIBRARY_RAW.LANDING.FED_HOUSE_DISBURSEMENTS
  where DESCRIPTION not ilike '%TOTALS%' and C_ORGANIZATION regexp '^[0-9]{4} HON\\\\. .*'
  group by 1,2),
office_parts as (
  select *, regexp_substr(upper(regexp_replace(regexp_replace(office, ' (JR\\\\.?|SR\\\\.?|II|III|IV)$', ''), '[^A-Z ]', '')), '[A-Z]+$') last_nm,
    upper(left(office,1)) first_init from offices),
reps as (
  select BIOGUIDE, upper(regexp_replace(NAME_LAST,'[^A-Za-z]','')) last_nm, upper(left(NAME_FIRST,1)) first_init, STATE, DISTRICT
  from LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_LEGISLATORS where TERM_TYPE='rep' and TERM_END >= '2016-01-01'),
m as (
  select o.yr, o.office, o.amt, o.n, r.STATE, r.DISTRICT, count(*) over (partition by o.yr, o.office) hits
  from office_parts o join reps r on o.last_nm=r.last_nm and o.first_init=r.first_init)
select STATE, count(distinct office) members, count(*) office_years, sum(amt) spend, avg(amt) avg_spend_per_office_year,
  median(amt) med_spend_per_office_year, count(distinct DISTRICT) districts
from m where hits = 1 and yr between '2016' and '2025' group by 1 order by 1""")
q("spend_match_rate", """
with offices as (
  select distinct regexp_replace(C_ORGANIZATION, '^[0-9]{4} HON\\\\. ', '') office
  from LIBRARY_RAW.LANDING.FED_HOUSE_DISBURSEMENTS
  where DESCRIPTION not ilike '%TOTALS%' and C_ORGANIZATION regexp '^[0-9]{4} HON\\\\. .*'),
office_parts as (
  select *, regexp_substr(upper(regexp_replace(regexp_replace(office, ' (JR\\\\.?|SR\\\\.?|II|III|IV)$', ''), '[^A-Z ]', '')), '[A-Z]+$') last_nm,
    upper(left(office,1)) first_init from offices),
reps as (
  select BIOGUIDE, upper(regexp_replace(NAME_LAST,'[^A-Za-z]','')) last_nm, upper(left(NAME_FIRST,1)) first_init
  from LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_LEGISLATORS where TERM_TYPE='rep' and TERM_END >= '2016-01-01')
select (select count(*) from offices) offices, count(distinct o.office) matched,
  count(distinct case when c=1 then o.office end) matched_unique
from (select o.office, count(*) c from office_parts o join reps r on o.last_nm=r.last_nm and o.first_init=r.first_init group by 1) o""")

# Redlining side: hunch 22 city-level results, rolled to state. D-grade TRI sites per km2 of D-grade HOLC area.
red = json.load(open(REPO / "reports/tier1_deep_dive_2026-09-05/22_redlined_toxic_sites/results.json"))["landing_city_grade"]
st = collections.defaultdict(lambda: {"cities": set(), "d_sites": 0, "d_km2": 0.0, "all_sites": 0, "all_km2": 0.0, "d_lbs": 0.0})
for r in red:
    s = st[r["STATE"]]; s["cities"].add(r["CITY"])
    s["all_sites"] += r["SITES"]; s["all_km2"] += r["KM2"]
    if r["G"] == "D":
        s["d_sites"] += r["SITES"]; s["d_km2"] += r["KM2"]; s["d_lbs"] += r["LBS"]
rows = []
spend = {r["STATE"]: r for r in out["spend_by_state"]}
for k, s in st.items():
    if k not in spend or s["d_km2"] == 0: continue
    rows.append({"STATE": k, "holc_cities": len(s["cities"]), "d_sites": s["d_sites"], "d_km2": round(s["d_km2"], 1),
                 "d_sites_per_km2": round(s["d_sites"] / s["d_km2"], 4), "d_lbs": s["d_lbs"],
                 "d_share_of_sites": round(s["d_sites"] / s["all_sites"], 3) if s["all_sites"] else None,
                 "members": spend[k]["MEMBERS"], "avg_spend": float(spend[k]["AVG_SPEND_PER_OFFICE_YEAR"]),
                 "med_spend": float(spend[k]["MED_SPEND_PER_OFFICE_YEAR"])})
def rank(v):
    o = sorted(range(len(v)), key=lambda i: v[i]); r = [0]*len(v)
    for j, i in enumerate(o): r[i] = j
    return r
def pearson(x, y):
    n = len(x); mx, my = sum(x)/n, sum(y)/n
    sx = math.sqrt(sum((a-mx)**2 for a in x)); sy = math.sqrt(sum((b-my)**2 for b in y))
    return sum((a-mx)*(b-my) for a, b in zip(x, y)) / (sx*sy) if sx and sy else None
x = [r["d_sites_per_km2"] for r in rows]; y = [r["med_spend"] for r in rows]
out["state_table"] = sorted(rows, key=lambda r: -r["d_sites_per_km2"])
out["correlation"] = {"states": len(rows), "pearson_density_vs_median_spend": round(pearson(x, y), 3),
                      "spearman_density_vs_median_spend": round(pearson(rank(x), rank(y)), 3),
                      "pearson_dshare_vs_median_spend": round(pearson([r["d_share_of_sites"] or 0 for r in rows], y), 3)}
top = sorted(rows, key=lambda r: -r["d_sites_per_km2"])
k = max(1, len(top)//4)
out["quartiles"] = {"top_quartile_states": [r["STATE"] for r in top[:k]], "top_q_median_spend": round(sum(r["med_spend"] for r in top[:k])/k),
                    "bottom_quartile_states": [r["STATE"] for r in top[-k:]], "bottom_q_median_spend": round(sum(r["med_spend"] for r in top[-k:])/k)}
json.dump(out, open(HERE / "results.json", "w"), default=str, indent=1)
print(json.dumps({"correlation": out["correlation"], "quartiles": out["quartiles"]}, indent=1))
