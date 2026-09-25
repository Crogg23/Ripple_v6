# skeptic harness: one read-only statement per call; result to skeptic/<label>.json
import sys, os, json, re
sys.path.insert(0, r'C:\Code\Ripple_v6')
from connect import db
D = r'C:\Code\Ripple_v6\reports\coverage_2026-09-24\joins\j5\skeptic'
label = sys.argv[1]; sql = open(sys.argv[2], encoding='utf-8').read().strip().rstrip(';')
assert re.match(r'^\s*(--[^\n]*\n\s*)*(select|with|show)\b', sql, re.I), 'read-only only'
c = db.connect(); cur = c.cursor()
cur.execute('ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300')
cur.execute("ALTER SESSION SET QUERY_TAG = 'joins-skeptic-2026-09-24'")
cur.execute(sql)
cols = [d[0] for d in cur.description]; rs = cur.fetchall()
json.dump({'sql': sql, 'cols': cols, 'rows': [[None if x is None else str(x) for x in r] for r in rs]}, open(os.path.join(D, label + '.json'), 'w', encoding='utf-8'), indent=0)
print(f'rows={len(rs)}'); print(' | '.join(cols))
for r in rs[:int(os.environ.get('SHOW', '60'))]: print(' | '.join('' if x is None else str(x) for x in r))
c.close()
