"""g06 runner: read-only SELECT/WITH only. Logs every statement to ../g06.sql, saves results as JSON here.

Usage: python run.py batchfile.py   (batchfile defines QUERIES = [(label, comment, sql), ...])
"""
import json, sys, re, datetime, decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO))
from connect import db  # noqa: E402

SQL_LOG = HERE.parent / "g06.sql"
COUNT = HERE / "count.txt"


def conv(v):
    if isinstance(v, (datetime.date, datetime.datetime)):
        return v.isoformat()
    if isinstance(v, decimal.Decimal):
        return float(v)
    return v


def main():
    ns = {}
    exec(Path(sys.argv[1]).read_text(encoding="utf-8"), ns)
    queries = ns["QUERIES"]
    for label, comment, sql in queries:
        s = sql.strip().rstrip(";")
        first = re.sub(r"^\s*(--[^\n]*\n\s*)*", "", s).split(None, 1)[0].upper()
        assert first in ("SELECT", "WITH"), f"{label}: not read-only ({first})"
        bad = re.search(r"\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|MERGE|TRUNCATE|GRANT|REVOKE)\b", s.upper())
        assert not bad, f"{label}: forbidden word {bad.group(0)}"
    n0 = int(COUNT.read_text()) if COUNT.exists() else 0
    assert n0 + len(queries) <= 33, f"budget: {n0} used + {len(queries)} > 33"
    c = db.connect()
    cur = c.cursor()
    try:
        cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
        cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'")
        for label, comment, sql in queries:
            s = sql.strip().rstrip(";")
            n0 += 1
            COUNT.write_text(str(n0))
            with SQL_LOG.open("a", encoding="utf-8") as f:
                f.write(f"\n-- [{label}] statement {n0}\n-- {comment}\n{s}\n;\n")
            try:
                cur.execute(s)
                cols = [d[0] for d in cur.description]
                rows = [[conv(v) for v in r] for r in cur.fetchall()]
                (HERE / f"{label}.json").write_text(json.dumps({"cols": cols, "rows": rows}, default=str), encoding="utf-8")
                print(f"{label}: {len(rows)} rows, cols={cols[:12]}")
            except Exception as ex:  # keep going, log the error
                print(f"{label}: ERROR {ex}")
                with SQL_LOG.open("a", encoding="utf-8") as f:
                    f.write(f"-- [{label}] ERROR: {str(ex)[:300]}\n")
    finally:
        cur.close()
        c.close()
    print("statements used:", n0)


if __name__ == "__main__":
    main()
