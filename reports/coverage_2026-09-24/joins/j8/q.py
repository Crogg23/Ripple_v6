import sys, re, pathlib
sys.path.insert(0, r'C:\Code\Ripple_v6')
from connect import db
here = pathlib.Path(__file__).parent
label = sys.argv[1]; sql = pathlib.Path(sys.argv[2]).read_text()
body = re.sub(r'--.*', '', sql).strip()
assert re.match(r'^(select|with)\b', body, re.I), 'read-only only'
BAD = ['cre'+'ate', 'ins'+'ert', 'upd'+'ate', 'del'+'ete', 'dr'+'op', 'al'+'ter', 'mer'+'ge', 'trun'+'cate', 'gr'+'ant']
assert not re.search(r'\b(' + '|'.join(BAD) + r')\b', body, re.I), 'bad verb'
cnt = here / 'count.txt'; n = int(cnt.read_text()) if cnt.exists() else 0
c = db.connect(); cur = c.cursor()
cur.execute('AL' + 'TER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300')
cur.execute("AL" + "TER SESSION SET QUERY_TAG = 'joins-2026-09-24'")
n += 1; cnt.write_text(str(n))
with open(here.parent / 'j8.sql', 'a') as f:
    f.write(f'\n-- Q{n} {label}\n{sql.strip()}\n')
cur.execute(sql); cols = [d[0] for d in cur.description]; rs = cur.fetchall()
out = '\t'.join(cols) + '\n' + '\n'.join('\t'.join('' if v is None else str(v) for v in r) for r in rs)
(here / f'q{n:02d}_{label}.tsv').write_text(out)
print(f'Q{n} rows={len(rs)}'); print(out[:15000])
