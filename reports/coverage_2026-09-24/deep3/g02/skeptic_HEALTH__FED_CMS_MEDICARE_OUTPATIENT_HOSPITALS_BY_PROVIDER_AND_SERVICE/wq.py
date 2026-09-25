"""Skeptic query helper. Read-only. Logs each statement to wlog.sql, counts statements."""
import json, sys, datetime, decimal
from pathlib import Path
sys.path.insert(0, r"C:/Code/Ripple_v6")
from connect import db
HERE=Path(__file__).resolve().parent
_c=None
def conn():
    global _c
    if _c is None:
        _c=db.connect(); cur=_c.cursor()
        cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
        cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-skeptic-2026-09-24'")
        cur.close()
        with open(HERE/'wlog.sql','a') as f: f.write("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;\nALTER SESSION SET QUERY_TAG = 'deep3-skeptic-2026-09-24';\n\n")
    return _c
def cl(v):
    if isinstance(v,decimal.Decimal): return float(v)
    if isinstance(v,(datetime.date,datetime.datetime)): return v.isoformat()
    return v
def run(sid,sql):
    s=sql.strip().rstrip(';'); assert s.split(None,1)[0].upper() in ('SELECT','WITH'); assert ';' not in s
    with open(HERE/'wlog.sql','a') as f: f.write(f"-- {sid}\n{s};\n\n")
    cur=conn().cursor(); cur.execute(s); cols=[c[0] for c in cur.description]
    rows=[dict(zip(cols,[cl(x) for x in r])) for r in cur.fetchall()]; cur.close()
    (HERE/f'{sid}.json').write_text(json.dumps(rows,default=str))
    return rows
