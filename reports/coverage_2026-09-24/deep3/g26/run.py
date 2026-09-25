"""g26 deep3 runner: read-only SELECT/WITH only, logs every statement to g26.sql.

Usage (repo root): python reports/coverage_2026-09-24/deep3/g26/run.py <batch.sql>
Statements in the batch file start with a line '-- @label'.
Results land in g26/rNN_label.json (big pulls as .csv).
"""
import csv
import json
import re
import sys
import time
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO))
from connect import db  # noqa: E402

HERE = Path(__file__).resolve().parent
SQL_LOG = HERE.parent / "g26.sql"
COUNT_FILE = HERE / "count.txt"
REFUSE = ["INSERT", "UPDATE", "DELETE", "DROP", "CREATE", "ALTER", "MERGE", "TRUNCATE", "GRANT", "PUT", "COPY"]


def load_queries(path):
    txt = Path(path).read_text(encoding="utf-8")
    blocks = re.split(r"^--\s*@(\S+)\s*$", txt, flags=re.M)
    return [(blocks[i], blocks[i + 1].strip().rstrip(";")) for i in range(1, len(blocks), 2)]


def conv(v):
    if isinstance(v, Decimal):
        return float(v)
    if isinstance(v, (date, datetime)):
        return v.isoformat()
    return v


def main(qfile):
    qs = load_queries(qfile)
    for label, sql in qs:
        body = "\n".join(l for l in sql.splitlines() if not l.strip().startswith("--"))
        head = body.lstrip().upper()
        if not (head.startswith("SELECT") or head.startswith("WITH")):
            raise SystemExit(f"refused non-read statement {label}")
        words = set(re.findall(r"[A-Z_]+", re.sub(r"'[^']*'", "", body).upper()))
        hit = [w for w in REFUSE if w in words]
        if hit:
            raise SystemExit(f"refused {label}: contains {hit}")
    n = int(COUNT_FILE.read_text()) if COUNT_FILE.exists() else 0
    if not SQL_LOG.exists():
        SQL_LOG.write_text(
            "-- g26 deep pass 3, 2026-09-24. Every statement run, in order, numbered.\n"
            "-- Door: Python (connect/db.py). Read-only. Session setup on each connection (not counted):\n"
            "--   ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;\n"
            "--   ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';\n", encoding="utf-8")
    c = db.connect()
    cur = c.cursor()
    cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
    cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'")
    for label, sql in qs:
        n += 1
        t0 = time.time()
        with open(SQL_LOG, "a", encoding="utf-8") as f:
            f.write(f"\n-- [{n}] {label}\n{sql};\n")
        try:
            cur.execute(sql)
            cols = [d[0] for d in cur.description]
            rows = [[conv(v) for v in r] for r in cur.fetchall()]
            err = None
        except Exception as e:
            cols, rows, err = [], [], str(e)[:800]
        dt = time.time() - t0
        COUNT_FILE.write_text(str(n))
        if len(rows) > 5000:
            out = HERE / f"r{n:02d}_{label}.csv"
            with open(out, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(cols)
                w.writerows(rows)
        else:
            out = HERE / f"r{n:02d}_{label}.json"
            out.write_text(json.dumps({"n": n, "label": label, "secs": round(dt, 1), "cols": cols,
                                       "rows": rows, "err": err}, indent=1, default=str), encoding="utf-8")
        print(f"== [{n}] {label} ({dt:.1f}s) {'ERR ' + err if err else str(len(rows)) + ' rows'} -> {out.name}")
        if not err:
            print(" | ".join(cols))
            for r in rows[:60]:
                print(" | ".join("" if v is None else str(v) for v in r))
    cur.close()
    c.close()


if __name__ == "__main__":
    main(sys.argv[1])
