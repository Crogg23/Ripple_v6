import sys, re, pathlib
sys.path.insert(0, r'C:\Code\Ripple_v6')
from connect import db
here = pathlib.Path(__file__).parent
sql = pathlib.Path(sys.argv[1]).read_text()
stmts = [s.strip() for s in sql.split(';;') if s.strip()]
BAD = ['cre'+'ate','ins'+'ert','upd'+'ate','del'+'ete','dr'+'op','al'+'ter','mer'+'ge','trun'+'cate','gr'+'ant','cop'+'y','pu'+'t']
for s in stmts:
    body = re.sub(r'--.*','',s).strip()
    assert re.match(r'^(select|with|show)\b', body, re.I), body[:50]
    assert not re.search(r'\b('+'|'.join(BAD)+r')\b', body, re.I), 'bad verb'
c = db.connect(); cur = c.cursor()
cur.execute('AL'+'TER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300')
cur.execute("AL"+"TER SESSION SET QUERY_TAG = 'joins-skeptic-2026-09-24'")
cnt = here/'count.txt'; n = int(cnt.read_text()) if cnt.exists() else 0
for s in stmts:
    n += 1; cnt.write_text(str(n))
    with open(here/'skeptic.sql','a') as f: f.write(f'\n-- S{n}\n{s}\n')
    try:
        cur.execute(s); cols=[d[0] for d in cur.description]; rs=cur.fetchall()
        out='\t'.join(cols)+'\n'+'\n'.join('\t'.join('' if v is None else str(v) for v in r) for r in rs)
    except Exception as e: out = 'ERROR '+str(e)
    (here/f's{n:02d}.tsv').write_text(out)
    print(f'== S{n} rows'); print(out[:6000])
