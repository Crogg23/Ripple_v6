"""skeptic runner: python run.py <n> <sqlfile>. Only runs text starting with SELECT or WITH."""
import sys, re
sys.path.insert(0, r"C:\Code\Ripple_v6")
from connect import db
n, path = sys.argv[1], sys.argv[2]
sql = open(path, encoding="utf-8").read().strip().rstrip(";")
body = re.sub(r"--[^\n]*", "", sql).strip().lower()
assert body.startswith("select") or body.startswith("with")
assert ";" not in body
c = db.connect(); cur = c.cursor()
cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
cur.execute("ALTER SESSION SET QUERY_TAG = 'joins-skeptic-2026-09-24'")
out = []
try:
    cur.execute(sql); cols = [d[0] for d in cur.description]; rows = cur.fetchall()
    out.append(f"[{n}] {len(rows)} rows"); out.append(" | ".join(cols))
    for r in rows[:300]: out.append(" | ".join("" if v is None else str(v) for v in r))
except Exception as e:
    out.append(f"[{n}] ERROR {e}")
finally:
    c.close()
txt = "\n".join(out); print(txt)
open(f"out_{n}.txt", "w", encoding="utf-8").write(sql + "\n\n" + txt)
