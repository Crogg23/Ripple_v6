"""j7 runner: python run.py TAG file.sql [maxprint] -> runs one read-only statement, logs to ../j7.sql, prints rows, saves json."""
import sys, json, re, os
sys.path.insert(0, r'C:\Code\Ripple_v6')
from connect import db
HERE = os.path.dirname(os.path.abspath(__file__))
tag, path = sys.argv[1], sys.argv[2]
sql = open(path, encoding='utf-8').read().strip().rstrip(';')
body = re.sub(r'--[^\n]*', '', sql).strip()
# read-only guard: must start with SELECT or WITH, and hold exactly one statement
assert re.match(r'^(SELECT|WITH)\b', body, re.I), 'read-only only'
assert ';' not in re.sub(r"'[^']*'", '', body), 'one statement only'
c = db.connect()
cur = c.cursor()
cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
cur.execute("ALTER SESSION SET QUERY_TAG = 'joins-2026-09-24'")
cnt_file = os.path.join(HERE, 'count.txt')
n = int(open(cnt_file).read()) + 1 if os.path.exists(cnt_file) else 1
open(cnt_file, 'w').write(str(n))
with open(os.path.join(HERE, '..', 'j7.sql'), 'a', encoding='utf-8') as f:
    f.write(f"\n-- [{tag}] statement {n}\n{sql};\n")
try:
    cur.execute(sql)
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
except Exception as e:
    print('ERROR', e)
    sys.exit(1)
finally:
    c.close()
json.dump({'cols': cols, 'rows': [[str(x) if x is not None else None for x in r] for r in rows]},
          open(os.path.join(HERE, tag + '.json'), 'w'), indent=0)
print(f'stmt {n}, {len(rows)} rows')
print(' | '.join(cols))
for r in rows[:int(sys.argv[3]) if len(sys.argv) > 3 else 80]:
    print(' | '.join('' if x is None else str(x) for x in r))
