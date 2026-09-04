import sys,json; sys.path.insert(0,'.')
from connect import db
c=db.connect()
def q(s):
    print("\n## "+s.strip().splitlines()[0][:110])
    for r in db.rows(c,s): print(r)
D=json.load(open('scripts/scratch/g2_out.json'))
fec=[n for n,*_ in D['1']['top'][:30]]
cand=[n.split(':')[1] for n in fec if n.startswith('FEC_CAND_ID')]; cmte=[n.split(':')[1] for n in fec if n.startswith('FEC_CMTE_ID')]
leis=[D[i]['top'][0][0].split(':')[1] for i in ('2','3','4','5')]
q(f"""select C1, max(C2), max(C6), max(C3), count(*) from LIBRARY_RAW.LANDING.FED_FEC_CANDIDATES where C1 in ({','.join(repr(x) for x in cand)}) group by 1""")
q(f"""select CMTE_ID, max(CMTE_NM), max(CMTE_TP), max(CMTE_DSGN), max(CMTE_PTY_AFFILIATION), count(*) from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES_DIM where CMTE_ID in ({','.join(repr(x) for x in cmte)}) group by 1""")
q(f"""select KEY_TYPE, KEY_VALUE, CANONICAL_NAME, ENTITY_TYPE from LIBRARY_META."CONNECT".ENTITY_GOLDEN where KEY_TYPE='LEI' and KEY_VALUE in ({','.join(repr(x) for x in leis)})""")
# entity_golden key types present, from the sample of rows joined — cheap via bridge: which key types does GOLDEN hold?
q("""select KEY_TYPE, count(*) from LIBRARY_META."CONNECT".ENTITY_GOLDEN group by 1 order by 2 desc""")
c.close()
