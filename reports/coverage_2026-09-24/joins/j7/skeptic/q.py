import sys, re, json
sys.path.insert(0, r'C:\Code\Ripple_v6')
from connect import db
sql = open(sys.argv[1], encoding='utf-8').read().strip().rstrip(';')
body = re.sub(r'--[^\n]*', '', sql).strip()
assert re.match(r'^(SELECT|WITH)\b', body, re.I)
assert ';' not in re.sub(r"'[^']*'", '', body)
c = db.connect(); cur = c.cursor()
cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
cur.execute("ALTER SESSION SET QUERY_TAG = 'joins-skeptic-2026-09-24'")
cur.execute(sql); cols=[d[0] for d in cur.description]; rows=cur.fetchall(); c.close()
print(' | '.join(cols))
for r in rows[:int(sys.argv[2]) if len(sys.argv)>2 else 200]: print(' | '.join('' if x is None else str(x) for x in r))
print(len(rows),'rows')
