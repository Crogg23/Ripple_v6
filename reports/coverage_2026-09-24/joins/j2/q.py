"""j2 runner: read-only. Usage: python reports/coverage_2026-09-24/joins/j2/q.py <batch.sql>
Batch file: statements separated by lines starting with '-- #'. Each is appended to j2.sql and results to j2/results.jsonl."""
import sys, json, re, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4]))
from connect import db

D = pathlib.Path(__file__).resolve().parent
SQL_LOG = D.parent / "j2.sql"
src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
parts = re.split(r"(?m)^-- #", src)
stmts = []
for p in parts:
    if not p.strip():
        continue
    label, _, body = p.partition("\n")
    body = body.strip().rstrip(";")
    first = re.sub(r"(?s)--[^\n]*\n", "", body + "\n").strip().lower()
    assert first.startswith("select") or first.startswith("with"), f"not read-only: {label}"
    assert not re.search(r"\b(insert|update|delete|drop|create|alter|merge|truncate)\b", re.sub(r"'[^']*'", "", first)), label
    stmts.append((label.strip(), body))

c = db.connect()
cur = c.cursor()
cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
cur.execute("ALTER SESSION SET QUERY_TAG = 'joins-2026-09-24'")
with open(SQL_LOG, "a", encoding="utf-8") as log, open(D / "results.jsonl", "a", encoding="utf-8") as res:
    for label, body in stmts:
        log.write(f"-- #{label}\n{body};\n\n")
        try:
            cur.execute(body)
            cols = [d[0] for d in cur.description]
            rows = cur.fetchall()
        except Exception as e:
            print(f"### {label}\nERROR {e}\n")
            res.write(json.dumps({"label": label, "error": str(e)}) + "\n")
            continue
        print(f"### {label}  ({len(rows)} rows)")
        print(" | ".join(cols))
        for r in rows[:80]:
            print(" | ".join("" if v is None else str(v) for v in r))
        print()
        res.write(json.dumps({"label": label, "cols": cols, "rows": [[str(v) for v in r] for r in rows]}) + "\n")
c.close()
