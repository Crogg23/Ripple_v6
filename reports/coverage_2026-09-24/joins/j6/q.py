"""j6 runner: python q.py <label> <sqlfile>. Read-only guard, logs to j6.sql, prints rows."""
import sys, re, os, json
sys.path.insert(0, r"C:\Code\Ripple_v6")
from connect import db

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(os.path.dirname(HERE), "j6.sql")
CNT = os.path.join(HERE, "count.txt")

label, path = sys.argv[1], sys.argv[2]
sql = open(path, encoding="utf-8").read().strip().rstrip(";")
body = re.sub(r"--[^\n]*", "", sql).strip().lower()
assert body.startswith("select") or body.startswith("with"), "read-only: SELECT/WITH only"
for bad in ["insert ", "update ", "delete ", "drop ", "create ", "alter ", "merge ", "truncate "]:
    assert bad not in body, bad
n = int(open(CNT).read()) + 1 if os.path.exists(CNT) else 1
assert n <= 45, "budget"
open(CNT, "w").write(str(n))
with open(LOG, "a", encoding="utf-8") as f:
    f.write(f"\n-- [{n}] {label}\n{sql};\n")
c = db.connect()
cur = c.cursor()
cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
cur.execute("ALTER SESSION SET QUERY_TAG = 'joins-2026-09-24'")
try:
    cur.execute(sql)
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    print(f"[{n}] {len(rows)} rows")
    print(" | ".join(cols))
    for r in rows[:200]:
        print(" | ".join("" if v is None else str(v) for v in r))
except Exception as e:
    print(f"[{n}] ERROR {e}")
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"-- [{n}] FAILED: {str(e)[:200]}\n")
finally:
    c.close()
