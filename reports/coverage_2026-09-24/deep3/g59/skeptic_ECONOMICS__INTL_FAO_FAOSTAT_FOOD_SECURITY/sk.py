# skeptic runner: read-only, SELECT/WITH only, outputs stay in this folder
import sys, json, decimal, datetime
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, r'C:\Code\Ripple_v6')
from connect import db
T = 'LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_FAO_FAOSTAT_FOOD_SECURITY'
CTRY = "try_to_number(AREA_CODE) < 5000 and try_to_number(AREA_CODE) not in (351,420,429)"
Q = {
'k1_integrity': f"""
select count(*) n, count(distinct AREA_CODE, ITEM_CODE, ELEMENT_CODE, YEAR_CODE) n_keys,
  count(distinct AREA_CODE) areas, count(distinct ITEM_CODE) items,
  count_if(VALUE is null or VALUE = '') blank_vals, count(distinct FLAG) flags
from {T}""",
'k2_headline': f"""
with v as (select AREA_CODE, AREA, ITEM_CODE, YEAR_CODE, VALUE, FLAG, try_to_double(VALUE) x
           from {T} where ELEMENT = 'Value' and ITEM_CODE in ('210071','210081','210401')
             and YEAR_CODE in ('20142016','20222024'))
select ITEM_CODE, YEAR_CODE,
  max(iff(AREA = 'World', x, null)) world,
  sum(iff({CTRY}, x, null)) pub_sum,
  count_if({CTRY} and x is not null) pub_n,
  count_if({CTRY} and VALUE like '<%') lt_n, listagg(distinct iff({CTRY} and VALUE like '<%', VALUE, null), ',') lt_vals,
  count_if({CTRY} and FLAG = 'Q') q_n, count_if({CTRY} and FLAG = 'O') o_n,
  max(iff(AREA = 'Southern Asia', x, null)) s_asia,
  max(iff(AREA = 'Southern Asia (excluding India)', x, null)) s_asia_ex_india,
  max(iff(AREA = 'Central Asia and Southern Asia', x, null)) cs_asia,
  max(iff(AREA = 'Central Asia', x, null)) c_asia,
  max(iff(AREA = 'Sub-Saharan Africa (including Sudan)', x, null)) ssa_inc_sudan,
  max(iff(AREA = 'Sub-Saharan Africa', x, null)) ssa,
  max(iff(AREA = 'Eastern Asia', x, null)) e_asia,
  count_if(AREA = 'World') world_rows
from v group by 1,2 order by 1,2""",
'k3_notes_on_blanks': f"""
select ITEM_CODE, FLAG, coalesce(NOTE,'<null>') note, count(*) n, count(distinct AREA_CODE) areas,
  listagg(distinct iff(AREA in ('India','China, mainland','Bangladesh','Sudan','Türkiye'), AREA, null), '|') big
from {T} where ITEM_CODE in ('210071','210401','210091','210081') and ELEMENT = 'Value'
  and (VALUE is null or VALUE = '')
group by 1,2,3 order by 1,2,4 desc""",
'k4_excluding_areas_and_q_stability': f"""
select 'excl_area' kind, AREA_CODE || ' ' || AREA label, count(*) n, count(distinct ITEM_CODE) items
from {T} where AREA ilike '%excluding%' or AREA ilike '%including%' group by 1,2
union all
select 'q_areas_210071', YEAR_CODE, count(distinct AREA_CODE), count(distinct iff(AREA in ('India','China, mainland'), AREA, null))
from {T} where ITEM_CODE = '210071' and ELEMENT = 'Value' and FLAG = 'Q' group by 1,2
order by 1,2""",
}
labels = sys.argv[1:]
c = db.connect(); cur = c.cursor()
cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-skeptic-2026-09-24'")
def conv(v):
    if isinstance(v, decimal.Decimal): return float(v)
    if isinstance(v, (datetime.date, datetime.datetime)): return v.isoformat()
    return v
for lab in labels:
    sql = Q[lab].strip()
    assert sql.split(None,1)[0].upper() in ('SELECT','WITH')
    cur.execute(sql)
    cols = [d[0] for d in cur.description]
    rows = [[conv(v) for v in r] for r in cur.fetchall()]
    (HERE / f'{lab}.json').write_text(json.dumps({'sql': sql, 'cols': cols, 'rows': rows}, default=str, indent=0), encoding='utf-8')
    print(f'===== {lab}: {len(rows)} rows'); print(' | '.join(cols))
    for r in rows[:80]: print(' | '.join('' if v is None else str(v) for v in r))
cur.close(); c.close()
