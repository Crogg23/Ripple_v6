"""Skeptic runner, SELECT/WITH only. Usage: python run.py s1 s2 ..."""
import sys, json, decimal, datetime
from pathlib import Path
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))
from connect import db
from q import Q

def conv(v):
    if isinstance(v, (datetime.date, datetime.datetime)): return v.isoformat()
    if isinstance(v, decimal.Decimal): return float(v)
    return v

labels = sys.argv[1:]
for lab in labels:
    assert Q[lab].strip().split(None, 1)[0].upper() in ('SELECT', 'WITH')
c = db.connect(); cur = c.cursor()
cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-skeptic-2026-09-24'")
for lab in labels:
    try:
        cur.execute(Q[lab].strip())
    except Exception as ex:
        print('=====', lab, 'ERROR', str(ex)[:400]); continue
    cols = [d[0] for d in cur.description]
    rows = [[conv(v) for v in r] for r in cur.fetchall()]
    (HERE / f"{lab}.json").write_text(json.dumps({'cols': cols, 'rows': rows}, default=str), encoding='utf-8')
    print('=====', lab, len(rows)); print(cols)
    for r in rows: print(r)
