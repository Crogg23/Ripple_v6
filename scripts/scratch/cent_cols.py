import sys,re,collections; sys.path.insert(0,'.')
from connect import db
c=db.connect()
def q(s):
    print("\n## "+s.strip().splitlines()[0][:110])
    for r in db.rows(c,s): print(r)
# column-level both-key test: metadata only, no row scan
rows=db.rows(c,"select table_name,column_name from LIBRARY_RAW.information_schema.columns where table_schema='LANDING'")
H=re.compile(r'(^|_)(NPI|CCN)(_|$)|PRSCRBR_NPI|RNDRNG_NPI|RFRG_NPI',re.I); Cp=re.compile(r'(^|_)(EIN|UEI|DUNS|CIK|LEI)(_|$)|UNIQUE_ENTITY_ID|TAX_ID|TIN(_|$)',re.I)
by=collections.defaultdict(lambda:[set(),set()])
for t,col in rows:
    if H.search(col): by[t][0].add(col)
    if Cp.search(col): by[t][1].add(col)
both={t:v for t,v in by.items() if v[0] and v[1]}
print(f"LANDING tables: {len({t for t,_ in rows})}; tables with a health-id column AND a corporate-id column by NAME: {len(both)}")
for t,(h,cc) in sorted(both.items()): print(f"  {t}: health {sorted(h)} corp {sorted(cc)}")
q("""select RUN_ID,min(BUILT_AT),max(BUILT_AT),count(*) from LIBRARY_META."CONNECT".CONNECT_EDGES group by 1 order by 2""")
q("""select RUN_ID,min(BUILT_AT),max(BUILT_AT),count(*) from LIBRARY_META."CONNECT".CONNECT_EDGES_INC group by 1 order by 2""")
q("""select count(*) from (select A,B,KEY from LIBRARY_META."CONNECT".CONNECT_EDGES_INC minus select A,B,KEY from LIBRARY_META."CONNECT".CONNECT_EDGES)""")
c.close()
