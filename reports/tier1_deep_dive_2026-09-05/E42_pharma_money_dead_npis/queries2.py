"""E42 part 2: tighter second-NPI test, exclusion-list proxy for 'reason', Part B control for the 10."""
import json
from _shared.q import run, open_log
D = "reports/tier1_deep_dive_2026-09-05/E42_pharma_money_dead_npis"
open_log(f"{D}/queries.log")
NP = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES"
R = json.load(open(f"{D}/results.json"))
top = R["q2_top"][:10]
ids = ",".join(f"'{r['NPI']}'" for r in top)
OUT = {}

tabs = run("""select table_schema, table_name, row_count from LIBRARY_MARTS.information_schema.tables
  where table_name ilike '%LEIE%' or table_name ilike '%PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER%' or table_name ilike '%SAM_EXCLUSIONS%'""", "q13_find_tables")
for t in tabs: print(t)
OUT["q13_tables"] = tabs
fq = lambda pat: next((f"LIBRARY_MARTS.{t['TABLE_SCHEMA']}.{t['TABLE_NAME']}" for t in tabs if pat in t['TABLE_NAME'] and t['TABLE_SCHEMA']!='TIMELINE'), None)
LEIE, PARTB, SAM = fq("LEIE"), fq("BY_PROVIDER"), fq("SAM_EXCLUSIONS")

# Q14 tight second-NPI test: same last+first name AND same state as the Open Payments recipient, live type-1 rows only
vals = " union all ".join(f"select '{r['NPI']}' dead_npi, '{r['LN'].upper()}' ln, '{R['q2_top'][i]['FN'].upper()}' fn, '{r['ST']}' st" for i,r in enumerate(top))
OUT["q14_second_npi_tight"] = run(f"""
with t as ({vals})
select t.dead_npi, t.ln, t.st, count(p.NPI) live_same_name_state, listagg(p.NPI||':'||p.HEALTHCARE_PROVIDER_TAXONOMY_CODE_1, ' ') hits
from t left join {NP} p on upper(p.PROVIDER_LAST_NAME_LEGAL_NAME)=t.ln and upper(p.PROVIDER_FIRST_NAME)=t.fn
  and p.ENTITY_TYPE_CODE='1' and p.NPI_DEACTIVATION_DATE is null and p.PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME=t.st
group by 1,2,3 order by 1""", "q14_second_npi_tight")

if LEIE:
    cols = [c['COLUMN_NAME'] for c in run(f"select column_name from LIBRARY_MARTS.information_schema.columns where table_name='{LEIE.split('.')[-1]}' and table_schema='{LEIE.split('.')[1]}'", "q15_leie_cols")]
    print(cols)
    OUT["q15_leie"] = run(f"select NPI, LAST_NAME, FIRST_NAME, EXCLUSION_TYPE, EXCLUSION_DATE, STATE, WAS_REINSTATED from {LEIE} where NPI in ({ids})", "q15_leie_top10")
if SAM:
    OUT["q16_sam"] = run(f"select NPI, count(*) n from {SAM} where NPI in ({ids}) group by 1", "q16_sam_top10")
if PARTB:
    OUT["q17_partb"] = run(f"select RNDRNG_NPI, count(*) n from {PARTB} where RNDRNG_NPI in ({ids}) group by 1", "q17_partb_top10")

json.dump(OUT, open(f"{D}/results2.json","w"), indent=1, default=str)
for k,v in OUT.items():
    print("==",k,len(v))
    for r in v[:20]: print(r)
