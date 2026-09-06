"""Hunch 22 - redlined neighborhoods vs toxic sites today. Every query, SELECT only.
Run from repo root: PYTHONPATH=reports/tier1_deep_dive_2026-09-05 python3 reports/tier1_deep_dive_2026-09-05/22_redlined_toxic_sites/queries.py
Writes results.json next to this file; story.py builds the charts from it."""
import json, os, sys
from _shared.q import run, open_log
HERE = os.path.dirname(os.path.abspath(__file__))
open_log(os.path.join(HERE, "queries.log"))

M = "LIBRARY_MARTS.HOUSING.HOUSING__FED_MAPPING_INEQUALITY"          # 1,155 rows - one polygon per (city, grade)
L = "LIBRARY_RAW.LANDING.FED_MAPPING_INEQUALITY"                      # 10,154 rows - every HOLC polygon
F = "LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_FACILITY"     # 64,990 facilities, DDMMSS coords
B = "LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023"   # 78,647 chemical rows, 21,870 facilities, decimal coords

R = {}
def q(key, sql): R[key] = run(sql, key); return R[key]

# ---------- 0. what the tables are ----------
q("mart_grade_dist", f"select HOLC_GRADE, count(*) n, count(GEOMETRY) g from {M} group by 1 order by 1")
q("mart_shape", f"select count(*) n, count(distinct CITY||'|'||STATE) cities, count(distinct HOLC_NEIGHBORHOOD_KEY) keys, count(distinct HOLC_ID) holc_ids, count(distinct SOURCE_ID) srcs from {M}")
q("mart_one_per_city_grade", f"select count(*) city_grade_pairs, sum(n) rows_, max(n) max_per_pair from (select CITY, STATE, trim(HOLC_GRADE) g, count(*) n from {M} group by 1,2,3)")
q("landing_shape", f"select count(*) n, sum(iff(HOLC_GRADE='',1,0)) exact_blank, sum(iff(nullif(trim(HOLC_GRADE),'') is null,1,0)) blank_any, count(distinct HOLC_ID) holc_ids, count(distinct CITY||'|'||STATE) cities, count(distinct GEOMETRY) geoms, count(distinct _SOURCE_RUN_ID) runs from {L}")
q("landing_grade_dist", f"select trim(HOLC_GRADE) g, count(*) n from {L} group by 1 order by 1")
q("mart_geoms_in_landing", f"select count(*) n from {M} m join {L} l on l.GEOMETRY=m.GEOMETRY")
q("geometry_parse", f"select count(*) n, count(try_to_geography(GEOMETRY)) parsed, regexp_substr(min(GEOMETRY),'\"type\": \"[A-Za-z]+') sample_type from {L}")
q("geometry_types", f"select regexp_substr(GEOMETRY,'\"type\": \"([A-Za-z]+)\"',1,1,'e') t, count(*) n from {L} group by 1")

# ---------- 1. coordinate formats in the facility table ----------
q("facility_coord_formats", f"""select count(*) n, count(FAC_LATITUDE) fac_lat, count(PREF_LATITUDE) pref_lat,
  sum(iff(abs(FAC_LATITUDE)>90,1,0)) fac_ddmmss, sum(iff(FAC_LATITUDE=0,1,0)) fac_zero,
  sum(iff(FAC_LATITUDE between 1 and 90,1,0)) fac_decimal_band,
  max(PREF_LATITUDE) pref_max, sum(iff(PREF_LATITUDE<>floor(PREF_LATITUDE),1,0)) pref_fractional,
  count(distinct PREF_LATITUDE) pref_distinct from {F}""")
q("facility_coord_sample", f"select FAC_LATITUDE, FAC_LONGITUDE, PREF_LATITUDE, PREF_LONGITUDE, STATE_ABBR from {F} where FAC_LATITUDE>0 order by random() limit 6")
q("basic_shape", f"""select count(*) rows_, count(distinct C_2_TRIFD) facilities, min(C_1_YEAR) y0, max(C_1_YEAR) y1,
  min(C_12_LATITUDE) la0, max(C_12_LATITUDE) la1, sum(iff(C_50_UNIT_OF_MEASURE='Grams',1,0)) gram_rows,
  round(sum(iff(C_50_UNIT_OF_MEASURE='Grams', C_107_TOTAL_RELEASES/453.592, C_107_TOTAL_RELEASES))) total_lbs from {B}""")
q("basic_to_facility", f"select count(distinct b.C_2_TRIFD) matched from {B} b join {F} f on f.TRI_FACILITY_ID=b.C_2_TRIFD")

# ---------- shared CTEs ----------
POLYS_L = f"""polys as (select HOLC_ID||'|'||CITY||'|'||STATE||'|'||row_number() over (order by GEOMETRY) k, CITY, STATE, trim(HOLC_GRADE) g,
  try_to_geography(GEOMETRY) geo, st_area(try_to_geography(GEOMETRY))/1e6 km2 from {L})"""
POLYS_M = f"polys as (select HOLC_NEIGHBORHOOD_KEY k, CITY, STATE, trim(HOLC_GRADE) g, try_to_geography(GEOMETRY) geo, st_area(try_to_geography(GEOMETRY))/1e6 km2 from {M})"
PTS_B = f"""pts as (select C_2_TRIFD id, any_value(C_12_LATITUDE) lat, any_value(C_13_LONGITUDE) lon,
  sum(iff(C_50_UNIT_OF_MEASURE='Grams', C_107_TOTAL_RELEASES/453.592, C_107_TOTAL_RELEASES)) lbs,
  max(iff(C_46_CARCINOGEN='YES',1,0)) carc from {B} group by 1)"""
# DDMMSS -> decimal; a few rows have lat/lon swapped (lat>72 with lon<72), swap back; drop what is still outside the US band
PTS_F = f"""fac as (select TRI_FACILITY_ID id, FAC_CLOSED_IND closed,
  floor(FAC_LATITUDE/10000)+floor(mod(FAC_LATITUDE,10000)/100)/60+mod(FAC_LATITUDE,100)/3600 la,
  -(floor(FAC_LONGITUDE/10000)+floor(mod(FAC_LONGITUDE,10000)/100)/60+mod(FAC_LONGITUDE,100)/3600) lo
  from {F} where FAC_LATITUDE>0 and FAC_LONGITUDE>0),
fpts as (select * from (select id, closed, iff(la>72 and -lo<72, -lo, la) lat, iff(la>72 and -lo<72, -la, lo) lon from fac)
  where lat between 18 and 72 and lon between -180 and -65)"""

# ---------- 2. the first pass, reproduced on the mart (the 1,155-row slice) ----------
q("mart_join_by_grade", f"""with {PTS_B}, {POLYS_M}
select g, count(distinct p.id) sites, count(distinct y.k) polys_hit, round(sum(p.lbs)) lbs
from pts p join polys y on st_contains(y.geo, st_makepoint(p.lon, p.lat)) group by 1 order by 1""")
q("mart_area_by_grade", f"with {POLYS_M} select g, count(*) polys, round(sum(km2),1) km2 from polys group by 1 order by 1")

# ---------- 3. the rebuild on every polygon (LANDING) ----------
q("landing_area_by_grade", f"with {POLYS_L} select g, count(*) polys, round(sum(km2),1) km2, round(median(km2),2) med_km2 from polys group by 1 order by 1")
q("landing_join_by_grade", f"""with {PTS_B}, {POLYS_L}
select g, count(distinct p.id) sites, count(*) pairs, count(distinct y.k) polys_hit, round(sum(p.lbs)) lbs,
  round(median(p.lbs)) med_lbs_per_site, sum(p.carc) carc_sites, sum(iff(p.lbs>0,1,0)) sites_nonzero
from pts p join polys y on st_contains(y.geo, st_makepoint(p.lon, p.lat)) group by 1 order by 1""")
q("landing_join_500m", f"""with {PTS_B}, {POLYS_L}
select g, count(distinct p.id) sites from pts p join polys y on st_dwithin(y.geo, st_makepoint(p.lon, p.lat), 500) group by 1 order by 1""")
q("landing_polys_with_site", f"""with {PTS_B}, {POLYS_L},
hit as (select distinct y.k from pts p join polys y on st_contains(y.geo, st_makepoint(p.lon, p.lat)))
select y.g, count(*) polys, count(h.k) polys_with_site, round(100*count(h.k)/count(*),1) pct from polys y left join hit h on h.k=y.k group by 1 order by 1""")
# same join, other facility table (DDMMSS converted), all 65k facilities incl. closed
q("landing_join_facility_table", f"""with {PTS_F}, {POLYS_L}
select g, count(distinct f.id) sites, sum(iff(f.closed='0',1,0)) open_sites from fpts f join polys y on st_contains(y.geo, st_makepoint(f.lon, f.lat)) group by 1 order by 1""")
q("facility_pts_kept", f"with {PTS_F} select count(*) kept from fpts")

# ---------- 4. per city ----------
q("landing_city_grade", f"""with {PTS_B}, {POLYS_L},
hits as (select p.id, p.lbs, y.CITY, y.STATE, y.g from pts p join polys y on st_contains(y.geo, st_makepoint(p.lon, p.lat))),
area as (select CITY, STATE, g, count(*) polys, sum(km2) km2 from polys group by 1,2,3),
tot as (select CITY, STATE, count(distinct id) total_sites from hits where g in ('A','B','C','D') group by 1,2)
select a.CITY, a.STATE, a.g, a.polys, round(a.km2,2) km2, count(distinct h.id) sites, round(coalesce(sum(h.lbs),0)) lbs, t.total_sites
from area a join tot t on t.CITY=a.CITY and t.STATE=a.STATE
left join hits h on h.CITY=a.CITY and h.STATE=a.STATE and h.g=a.g
where a.g in ('A','B','C','D') group by 1,2,3,4,5,8 order by t.total_sites desc, a.CITY, a.g""")

# ---------- 5. pounds distribution, top sites ----------
q("landing_top_sites", f"""with {PTS_B}, {POLYS_L}
select p.id, y.CITY, y.STATE, y.g, round(p.lbs) lbs from pts p join polys y on st_contains(y.geo, st_makepoint(p.lon, p.lat))
where y.g in ('A','B','C','D') qualify row_number() over (order by p.lbs desc) <= 10""")
q("landing_lbs_excl_top1_per_grade", f"""with {PTS_B}, {POLYS_L},
h as (select distinct p.id, p.lbs, y.g from pts p join polys y on st_contains(y.geo, st_makepoint(p.lon, p.lat)) where y.g in ('A','B','C','D'))
select g, round(sum(lbs)) lbs, round(sum(lbs)-max(lbs)) lbs_minus_biggest, round(percentile_cont(0.75) within group (order by lbs)) p75 from h group by 1 order by 1""")

q("landing_join_500m_lbs", f"""with {PTS_B}, {POLYS_L},
h as (select p.id, p.lbs, y.g from pts p join polys y on st_dwithin(y.geo, st_makepoint(p.lon, p.lat), 500)),
d as (select distinct id, lbs, g from h)
select g, count(*) sites, round(sum(lbs)) lbs from d group by 1 order by 1""")

with open(os.path.join(HERE, "results.json"), "w") as f:
    json.dump(R, f, indent=1, default=str)
print("wrote results.json", file=sys.stderr)
