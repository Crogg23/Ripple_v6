"""Run one numbered statement for deep3 group g03, log it, save result as CSV.

usage: python run.py S01 path/to/stmt.sql
Appends the statement to ../g03.sql and writes g03/S01.csv.
Read-only guard: refuses anything that is not SELECT or WITH.
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

label, path = sys.argv[1], Path(sys.argv[2])
sql = path.read_text(encoding="utf-8").strip().rstrip(";")
head = re.sub(r"--[^\n]*\n", "", sql).lstrip().upper()
if not (head.startswith("SELECT") or head.startswith("WITH")):
    sys.exit("refused: not SELECT/WITH")
if re.search(r"\b(CREATE|INSERT|UPDATE|DELETE|DROP|ALTER|MERGE|TRUNCATE|GRANT)\b", re.sub(r"'[^']*'", "", head)):
    sys.exit("refused: write keyword present")

c = db.connect()
cur = c.cursor()
cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'")
t0 = time.time()
cur.execute(sql)
rows = cur.fetchall()
cols = [d[0] for d in cur.description]
secs = time.time() - t0
cur.close()
c.close()

out = HERE / f"{label}.csv"
with out.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(cols)
    w.writerows(rows)

with (HERE.parent / "g03.sql").open("a", encoding="utf-8") as f:
    f.write(f"-- {label}  ({len(rows)} rows, {secs:.1f}s)\n{sql};\n\n")

print(f"{label}: {len(rows)} rows, {secs:.1f}s -> {out.name}")
if len(rows) <= 60:
    print("\t".join(cols))
    for r in rows:
        print("\t".join("" if v is None else str(v) for v in r))
