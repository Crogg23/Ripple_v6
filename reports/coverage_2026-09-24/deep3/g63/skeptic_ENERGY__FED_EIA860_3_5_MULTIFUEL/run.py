"""Skeptic runner: one read-only SELECT/WITH per call, no semicolons inside. Usage: python run.py K01 stmt.sql"""
import sys, csv, re
from pathlib import Path
sys.path.insert(0, r'C:\Code\Ripple_v6')
from connect import db
sid, f = sys.argv[1], sys.argv[2]
here = Path(__file__).resolve().parent
sql = Path(f).read_text(encoding='utf-8').strip().rstrip(';')
body = re.sub(r'--[^\n]*', '', sql).strip().upper()
assert body.startswith('SELECT') or body.startswith('WITH'), 'read-only only'
assert ';' not in body, 'one statement only'
c = db.connect(); cur = c.cursor()
cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-skeptic-2026-09-24'")
cur.execute(sql)
cols = [d[0] for d in cur.description]; rows = cur.fetchall(); c.close()
with open(here / f'out_{sid}.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh); w.writerow(cols); w.writerows(rows)
print('|'.join(cols))
lim = int(sys.argv[3]) if len(sys.argv) > 3 else 60
for r in rows[:lim]: print('|'.join('' if v is None else str(v) for v in r))
print(f'-- {len(rows)} rows')
