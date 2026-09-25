"""Run one numbered read-only statement for deep3/g63.
Usage: python run.py S01 path/to/stmt.sql [max_print_rows]
Saves out_Sxx.csv next to this file. Refuses anything that is not SELECT/WITH.
"""
import sys, csv, re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from connect import db

sid, f = sys.argv[1], sys.argv[2]
limit = int(sys.argv[3]) if len(sys.argv) > 3 else 80
here = Path(__file__).resolve().parent
sql = Path(f).read_text(encoding='utf-8').strip().rstrip(';')
body = re.sub(r'--[^\n]*', '', sql).strip().upper()
assert body.startswith('SELECT') or body.startswith('WITH'), 'read-only only'
for bad in ('INSERT ', 'UPDATE ', 'DELETE ', 'DROP ', 'CREATE ', 'ALTER ', 'MERGE ', 'TRUNCATE ', 'GRANT '):
    assert bad not in body, bad

c = db.connect()
cur = c.cursor()
cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'")
cur.execute(sql)
cols = [d[0] for d in cur.description]
rows = cur.fetchall()
c.close()

with open(here / f'out_{sid}.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh)
    w.writerow(cols)
    w.writerows(rows)

print('|'.join(cols))
for r in rows[:limit]:
    print('|'.join('' if v is None else str(v) for v in r))
print(f'-- {len(rows)} rows')
