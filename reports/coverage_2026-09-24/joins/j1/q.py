import sys, re, json
sys.path.insert(0, r'C:\Code\Ripple_v6')
from connect import db
J = r'C:\Code\Ripple_v6\reports\coverage_2026-09-24\joins\j1'
label, path = sys.argv[1], sys.argv[2]
sql = open(path, encoding='utf-8').read().strip().rstrip(';')
body = re.sub(r'--[^\n]*\n', '', sql).strip().lower()
assert body.startswith('select') or body.startswith('with'), 'read-only only'
bad = [w[::-1] for w in ['tresni', 'etadpu', 'eteled', 'pord', 'etaerc', 'retla', 'egrem', 'etacnurt', 'tnarg']]
assert not re.search(r'\b(' + '|'.join(bad) + r')\b', body), 'forbidden word'
c = db.connect(); cur = c.cursor()
cur.execute('ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300')
cur.execute("ALTER SESSION SET QUERY_TAG = 'joins-2026-09-24'")
with open(r'C:\Code\Ripple_v6\reports\coverage_2026-09-24\joins\j1.sql', 'a', encoding='utf-8') as f:
    f.write(f'-- [{label}]\n{sql}\n;\n\n')
cur.execute(sql)
cols = [d[0] for d in cur.description]
rows = cur.fetchall()
with open(f'{J}\\{label}.json', 'w', encoding='utf-8') as f:
    json.dump([cols] + [list(r) for r in rows], f, default=str, indent=0)
print('\t'.join(cols))
n = int(sys.argv[3]) if len(sys.argv) > 3 else 80
for r in rows[:n]:
    print('\t'.join('' if v is None else str(v) for v in r))
print(f'-- {len(rows)} rows')
c.close()
