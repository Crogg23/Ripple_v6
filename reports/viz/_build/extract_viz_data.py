"""Extract data for the three A-track visuals into JSON files (read-only)."""
import json, os, sys
sys.path.insert(0, r"c:\Code\Ripple_v6")
from scripts._snowflake_conn import connect

OUT = os.path.dirname(os.path.abspath(__file__))

conn = connect()
cur = conn.cursor()

def q(sql):
    cur.execute(sql)
    return cur.fetchall()

# ---------- A1: county polygons (simplified) + metrics ----------
print("counties...", flush=True)
rows = q("""
    select c.GEOID, c.NAME, c.STUSPS, d.POPULATION_2020,
           coalesce(ST_ASGEOJSON(ST_SIMPLIFY(c.GEOMETRY, 3000)), ST_ASGEOJSON(c.GEOMETRY))
    from LIBRARY_MARTS.REFERENCE.REFERENCE__CENSUS_CB_COUNTY c
    left join LIBRARY_MARTS.CORE.DIM_COUNTY d on d.COUNTY_FIPS = c.GEOID
""")
counties = [{"g": r[0], "n": r[1], "s": r[2], "p": int(r[3]) if r[3] else None,
             "geom": json.loads(r[4])} for r in rows]
json.dump(counties, open(os.path.join(OUT, "counties.json"), "w"))
print(f"  {len(counties)} counties", flush=True)

print("states...", flush=True)
rows = q("""
    select STUSPS, coalesce(ST_ASGEOJSON(ST_SIMPLIFY(GEOMETRY, 8000)), ST_ASGEOJSON(GEOMETRY))
    from LIBRARY_MARTS.REFERENCE.REFERENCE__CENSUS_CB_STATE
""")
json.dump([{"s": r[0], "geom": json.loads(r[1])} for r in rows],
          open(os.path.join(OUT, "states.json"), "w"))

print("arcos by county...", flush=True)
rows = q("""
    with cty as (
        select GEOID, upper(NAME) as NM, STUSPS
        from LIBRARY_MARTS.REFERENCE.REFERENCE__CENSUS_CB_COUNTY
    )
    select cty.GEOID, sum(a.TOTAL_MME), sum(a.DOSAGE_UNITS),
           min(year(a.TRANSACTION_DATE)), max(year(a.TRANSACTION_DATE))
    from LIBRARY_MARTS.HEALTH.HEALTH__FED_DEA_ARCOS a
    join cty on upper(trim(a.BUYER_COUNTY)) = cty.NM
            and upper(trim(a.BUYER_STATE)) = cty.STUSPS
    where a.TOTAL_MME is not null
    group by 1
""")
json.dump([{"g": r[0], "mme": float(r[1] or 0), "du": float(r[2] or 0),
            "y0": r[3], "y1": r[4]} for r in rows],
          open(os.path.join(OUT, "arcos_county.json"), "w"))
print(f"  {len(rows)} counties matched", flush=True)

print("epa facilities by county...", flush=True)
rows = q("""
    select lpad(trim(FIPS_CODE), 5, '0'), count(*)
    from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FACILITIES
    where FIPS_CODE is not null and trim(FIPS_CODE) <> ''
    group by 1
""")
json.dump([{"g": r[0], "n": int(r[1])} for r in rows],
          open(os.path.join(OUT, "epa_county.json"), "w"))

# ---------- A2: ZIP->ZIP opioid flows ----------
print("arcos flows...", flush=True)
rows = q("""
    with f as (
        select left(trim(REPORTER_ZIP),5) as rz, left(trim(BUYER_ZIP),5) as bz,
               year(TRANSACTION_DATE) as yr, sum(TOTAL_MME) as mme
        from LIBRARY_MARTS.HEALTH.HEALTH__FED_DEA_ARCOS
        where TOTAL_MME is not null and TRANSACTION_DATE is not null
          and REPORTER_ZIP is not null and BUYER_ZIP is not null
        group by 1,2,3
    ),
    top_pairs as (
        select rz, bz, sum(mme) as tot
        from f where rz <> bz
        group by 1,2
        order by tot desc
        limit 4000
    )
    select f.rz, f.bz, f.yr, f.mme,
           zr.LAT, zr.LON, zb.LAT, zb.LON, zr.STATE_USPS, zb.STATE_USPS
    from f
    join top_pairs t on t.rz = f.rz and t.bz = f.bz
    join LIBRARY_MARTS.CORE.DIM_ZIP_POINT zr on zr.ZCTA5 = f.rz
    join LIBRARY_MARTS.CORE.DIM_ZIP_POINT zb on zb.ZCTA5 = f.bz
""")
json.dump([[r[0], r[1], int(r[2]), float(r[3]), r[4], r[5], r[6], r[7], r[8], r[9]]
           for r in rows],
          open(os.path.join(OUT, "flows.json"), "w"))
print(f"  {len(rows)} pair-year rows", flush=True)

# ---------- A3: heartbeat wall ----------
print("heartbeat...", flush=True)
rows = q("""
    select RIPPLE_SOURCE, to_char(date_trunc('month', RIPPLE_DAY), 'YYYY-MM'),
           sum(N_ROWS)
    from LIBRARY_MARTS.TIMELINE.TIMELINE__WAREHOUSE
    where RIPPLE_DAY between '1990-01-01' and '2026-12-31'
    group by 1,2
""")
hb = {}
for src, mon, n in rows:
    hb.setdefault(src, {})[mon] = int(n)
json.dump(hb, open(os.path.join(OUT, "heartbeat.json"), "w"))
print(f"  {len(hb)} sources", flush=True)

conn.close()
print("DONE")
