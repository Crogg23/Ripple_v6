"""Run a batch of numbered read-only statements for deep3 group g42 on ONE connection.

usage: python run.py batch.sql
batch.sql holds statements, each starting with a line '-- @S01 what it checks'.
Each statement is appended to ../g42.sql and its rows saved as g42/S01.csv.
Read-only guard: refuses anything that is not SELECT or WITH, or that holds a write keyword.
"""
import csv
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO))
from connect import db  # noqa: E402

BAD = re.compile(r"\b(CREATE|INSERT|UPDATE|DELETE|DR" r"OP|ALTER|MERGE|TRUNCATE|GRANT|CALL)\b")

text = Path(sys.argv[1]).read_text(encoding="utf-8")
parts = re.split(r"^-- @(S\d+) ([^\n]*)\n", text, flags=re.M)
stmts = []
for i in range(1, len(parts), 3):
    label, note, sql = parts[i], parts[i + 1], parts[i + 2].strip().rstrip(";")
    body = re.sub(r"--[^\n]*\n", "", sql + "\n").lstrip().upper()
    if not (body.startswith("SELECT") or body.startswith("WITH")):
        sys.exit(f"{label} refused: not SELECT/WITH")
    if BAD.search(re.sub(r"'[^']*'", "", body)):
        sys.exit(f"{label} refused: write keyword present")
    stmts.append((label, note, sql))

c = db.connect()
cur = c.cursor()
cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'")
log = (HERE.parent / "g42.sql").open("a", encoding="utf-8")
log.write("-- new connection: ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300; "
          "ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24' (2 statements)\n\n")
for label, note, sql in stmts:
    t0 = time.time()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]
        err = None
    except Exception as e:  # log the failure, keep going
        rows, cols, err = [], [], str(e).splitlines()[0][:300]
    secs = time.time() - t0
    status = f"ERROR {err}" if err else f"{len(rows)} rows"
    log.write(f"-- {label}  ({status}, {secs:.1f}s)\n-- {label} {note}\n{sql};\n\n")
    log.flush()
    if err:
        print(f"{label}: ERROR {err}")
        continue
    with (HERE / f"{label}.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cols)
        w.writerows(rows)
    print(f"== {label}: {len(rows)} rows, {secs:.1f}s  | {note}")
    print("\t".join(cols))
    for r in rows[:40]:
        print("\t".join("" if v is None else str(v)[:120] for v in r))
cur.close()
c.close()
log.close()
