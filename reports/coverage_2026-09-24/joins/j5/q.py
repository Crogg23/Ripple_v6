# j5 harness: run one labelled read-only statement, append to j5.sql, print result
import sys, os, json, re
sys.path.insert(0, r'C:\Code\Ripple_v6')
from connect import db
D = r'C:\Code\Ripple_v6\reports\coverage_2026-09-24\joins'
label = sys.argv[1]
sql = open(sys.argv[2], encoding='utf-8').read().strip().rstrip(';')
assert re.match(r'^\s*(--[^\n]*\n\s*)*(select|with)\b', sql, re.I), 'read-only only'
cnt_f = os.path.join(D, 'j5', 'count.txt')
n = int(open(cnt_f).read()) if os.path.exists(cnt_f) else 0
n += 1
open(cnt_f, 'w').write(str(n))
with open(os.path.join(D, 'j5.sql'), 'a', encoding='utf-8') as f:
    f.write(f'-- [{label}] statement {n}\n{sql}\n;\n\n')
c = db.connect()
cur = c.cursor()
cur.execute('ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300')
cur.execute("ALTER SESSION SET QUERY_TAG = 'joins-2026-09-24'")
cur.execute(sql)
cols = [d[0] for d in cur.description]
rs = cur.fetchall()
out = os.path.join(D, 'j5', label + '.json')
json.dump({'cols': cols, 'rows': [[str(x) if x is not None else None for x in r] for r in rs]}, open(out, 'w', encoding='utf-8'), indent=0)
print(f'#{n} rows={len(rs)}')
print(' | '.join(cols))
for r in rs[:int(os.environ.get('SHOW', '80'))]:
    print(' | '.join('' if x is None else str(x) for x in r))
c.close()
