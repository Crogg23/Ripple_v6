"""g02 deep3 query helper. Read-only: one SELECT/WITH per call. Logs every statement to g02/log.sql."""
import json, sys, datetime, decimal
from pathlib import Path
REPO = Path(r"C:/Code/Ripple_v6")
sys.path.insert(0, str(REPO))
from connect import db

HERE = Path(__file__).resolve().parent
LOG = HERE / "log.sql"
_conn = None


def conn():
    global _conn
    if _conn is None:
        _conn = db.connect()
        cur = _conn.cursor()
        cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
        cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'")
        cur.close()
    return _conn


def _clean(v):
    if isinstance(v, decimal.Decimal):
        return float(v)
    if isinstance(v, (datetime.date, datetime.datetime)):
        return v.isoformat()
    return v


def run(sid, label, sql):
    s = sql.strip().rstrip(";")
    head = s.split(None, 1)[0].upper()
    assert head in ("SELECT", "WITH"), "read-only: SELECT or WITH only"
    assert ";" not in s, "one statement per call"
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"-- {sid} {label}\n{s};\n\n")
    cur = conn().cursor()
    t0 = datetime.datetime.now()
    cur.execute(s)
    cols = [c[0] for c in cur.description]
    rows = [dict(zip(cols, [_clean(x) for x in r])) for r in cur.fetchall()]
    cur.close()
    secs = (datetime.datetime.now() - t0).total_seconds()
    (HERE / f"{sid}.json").write_text(json.dumps(rows, default=str), encoding="utf-8")
    print(f"[{sid}] {label}: {len(rows)} rows, {secs:.1f}s")
    return rows


def load(sid):
    return json.loads((HERE / f"{sid}.json").read_text(encoding="utf-8"))
