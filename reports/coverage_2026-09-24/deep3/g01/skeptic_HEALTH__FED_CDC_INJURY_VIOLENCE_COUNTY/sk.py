"""Skeptic pass, read-only. SELECT/WITH only."""
import sys, json
from pathlib import Path
REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))
from connect import db
HERE = Path(__file__).resolve().parent
Q = {
"s1_landing_check": """
with l as (select * from LIBRARY_RAW.LANDING.FED_CDC_INJURY_VIOLENCE_COUNTY where intent = 'Drug_OD')
select 'AGG' k, period, null geoid, null name, count(*) n, count(distinct geoid) geos,
       sum(try_to_number(count_sup)) s, max(data_as_of)::string asof, any_value(ttm_date_range) rng
from l group by period
union all
select 'ROW', period, geoid, name, 1, 1, try_to_number(count_sup), data_as_of::string, count_sup
from l where geoid in ('04013','40131','40143','08031','08041')
order by 1, 3, 2""",
"s2_mart_check": """
select * from LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY
where geoid in ('04013','40131','40143','08031') and intent in ('Drug_OD','All_Suicide')
order by geoid, intent, period""",
"s3_other_county_od_tables": """
select table_catalog, table_schema, table_name, row_count
from LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES
where (table_name ilike '%OVERDOSE%' or table_name ilike '%DRUG_POISON%' or table_name ilike '%MARICOPA%'
   or table_name ilike '%OPIOID%' or table_name ilike '%MORTALITY%COUNTY%' or table_name ilike '%WONDER%')
order by table_name""",
}
c = db.connect(); cur = c.cursor()
cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-skeptic-2026-09-24'")
for k, sql in Q.items():
    try:
        cur.execute(sql); cols=[d[0] for d in cur.description]; rows=cur.fetchall(); err=None
    except Exception as e:
        cols, rows, err = [], [], str(e)
    (HERE/f"{k}.json").write_text(json.dumps({"cols":cols,"rows":[[None if v is None else str(v) for v in r] for r in rows],"err":err},indent=1),encoding="utf-8")
    print("==", k, err or f"{len(rows)} rows"); print(" | ".join(cols))
    for r in rows[:80]: print(" | ".join("" if v is None else str(v) for v in r))
cur.close(); c.close()
