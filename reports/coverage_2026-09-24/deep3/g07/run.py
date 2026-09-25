"""g07 read-only runner. Usage: python run.py batch.sql
Statements in batch.sql are separated by lines starting with '-- #'.
Each statement must start with SELECT or WITH. Appends to ../g07.sql, writes results to out_<n>.txt.
"""
import sys, re, json, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO))
from connect import db  # noqa

SQL_LOG = HERE.parent / "g07.sql"
COUNT_FILE = HERE / "count.json"

src = Path(sys.argv[1]).read_text(encoding="utf-8")
blocks = [b.strip() for b in re.split(r"^-- #", src, flags=re.M) if b.strip()]
stmts = []
for b in blocks:
    lines = b.splitlines()
    title = lines[0].strip()
    body = "\n".join(lines[1:]).strip().rstrip(";")
    head = re.sub(r"^(\s*--[^\n]*\n)*", "", body + "\n").lstrip().upper()
    if not (head.startswith("SELECT") or head.startswith("WITH")):
        raise SystemExit(f"refused non-read statement: {title}")
    bad = re.search(r"\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|MERGE|TRUNCATE|GRANT|REVOKE|COPY|PUT|CALL)\b\s", body.upper())
    if bad:
        raise SystemExit(f"refused keyword {bad.group(1)} in: {title}")
    stmts.append((title, body))

cnt = json.loads(COUNT_FILE.read_text()) if COUNT_FILE.exists() else {"n": 0}
c = db.connect()
cur = c.cursor()
cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'")
with open(SQL_LOG, "a", encoding="utf-8") as log:
    for title, body in stmts:
        cnt["n"] += 1
        n = cnt["n"]
        log.write(f"-- #{n} {title}\n{body};\n\n")
        t0 = time.time()
        out = HERE / f"out_{n:02d}.txt"
        try:
            cur.execute(body)
            cols = [d[0] for d in cur.description]
            rows = cur.fetchall()
            with open(out, "w", encoding="utf-8") as f:
                f.write("\t".join(cols) + "\n")
                for r in rows:
                    f.write("\t".join("" if v is None else str(v) for v in r) + "\n")
            print(f"== #{n} {title} ({len(rows)} rows, {time.time()-t0:.1f}s)")
            print("\t".join(cols))
            for r in rows[:80]:
                print("\t".join("" if v is None else str(v) for v in r))
        except Exception as e:
            print(f"== #{n} {title} ERROR {e}")
            out.write_text(f"ERROR {e}", encoding="utf-8")
        COUNT_FILE.write_text(json.dumps(cnt))
cur.close()
c.close()
