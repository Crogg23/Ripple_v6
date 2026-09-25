"""j3 runner: one SELECT/WITH per call. Logs statement to j3/all.sql and result to j3/out_<n>.txt.
Usage: python run.py <label> <sqlfile>"""
import sys, os, pathlib, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4]))
_SQLF=str(pathlib.Path(sys.argv[2]).resolve())
os.chdir(pathlib.Path(__file__).resolve().parents[4])
from connect import db

here = pathlib.Path(__file__).resolve().parent
label, sqlfile = sys.argv[1], _SQLF
sql = pathlib.Path(sqlfile).read_text(encoding='utf-8').strip().rstrip(';')
assert re.match(r'^\s*(select|with)\b', sql, re.I), 'read-only only'
assert not re.search(r'\b(insert|update|delete|drop|create|alter|merge|truncate)\b', re.sub(r"'[^']*'", "", sql), re.I), 'write keyword'
cnt = here / 'count.txt'
n = int(cnt.read_text()) + 1 if cnt.exists() else 1
c = db.connect()
cur = c.cursor()
cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
cur.execute("ALTER SESSION SET QUERY_TAG = 'joins-2026-09-24'")
cur.execute(sql)
cols = [d[0] for d in cur.description]
rows = cur.fetchall()
cnt.write_text(str(n))
with open(here / 'all.sql', 'a', encoding='utf-8') as f:
    f.write(f"\n-- #{n} {label}\n{sql};\n")
out = ['\t'.join(cols)] + ['\t'.join('' if v is None else str(v) for v in r) for r in rows]
(here / f'out_{n:02d}_{label}.txt').write_text('\n'.join(out), encoding='utf-8')
print(f'#{n} rows={len(rows)}')
print('\n'.join(out[:200]))
