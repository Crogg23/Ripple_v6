"""g08 runner: read-only SELECT/WITH statements, logged to g08.sql and g08/<batch>.json.

Usage: python run.py <batch_file.py>   (batch file defines QUERIES = [(label, sql), ...])
"""
import json
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO))
from connect import db  # noqa: E402

SQL_LOG = HERE.parent / "g08.sql"
COUNT_FILE = HERE / "count.txt"
SAFE = re.compile(r"^\s*(select|with)\b", re.I)
BAD = re.compile(r"\b(create|insert|update|delete|drop|alter|merge|truncate|grant|revoke|copy|put|call)\b", re.I)


def main():
    batch = Path(sys.argv[1])
    ns = {}
    exec(batch.read_text(encoding="utf-8"), ns)
    queries = ns["QUERIES"]
    for label, sql in queries:
        body = re.sub(r"'[^']*'", "''", sql)
        if not SAFE.match(sql) or BAD.search(body):
            raise SystemExit(f"refused non-read statement: {label}")
    used = int(COUNT_FILE.read_text()) if COUNT_FILE.exists() else 0
    if used + len(queries) > 35:
        raise SystemExit(f"budget: {used} used, {len(queries)} more would pass 35")
    conn = db.connect()
    out = {}
    try:
        cur = conn.cursor()
        cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
        cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'")
        cur.close()
        with SQL_LOG.open("a", encoding="utf-8") as log:
            for label, sql in queries:
                used += 1
                COUNT_FILE.write_text(str(used))
                log.write(f"\n-- [{used}] {label}\n{sql.strip()};\n")
                t0 = time.time()
                cur = conn.cursor()
                try:
                    cur.execute(sql)
                    cols = [c[0] for c in cur.description]
                    rows = [[str(v) if v is not None else None for v in r] for r in cur.fetchall()]
                    out[label] = {"cols": cols, "rows": rows, "secs": round(time.time() - t0, 1)}
                except Exception as e:  # keep going, record the error
                    out[label] = {"error": str(e)[:500]}
                finally:
                    cur.close()
                res = out[label]
                print(f"\n=== [{used}] {label} ({res.get('secs', 'ERR')}s)")
                if "error" in res:
                    print("ERROR", res["error"])
                else:
                    print(" | ".join(res["cols"]))
                    for r in res["rows"][:60]:
                        print(" | ".join("" if v is None else v for v in r))
                    if len(res["rows"]) > 60:
                        print(f"... {len(res['rows'])} rows")
    finally:
        conn.close()
    (HERE / (batch.stem + ".json")).write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"\nstatements used: {used}")


if __name__ == "__main__":
    main()
