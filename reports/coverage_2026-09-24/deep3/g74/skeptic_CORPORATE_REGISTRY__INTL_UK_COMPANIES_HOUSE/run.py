"""Skeptic runner: read-only SELECT/WITH only. Usage: python run.py file.sql label"""
import csv, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
REPO = Path("C:/Code/Ripple_v6")
sys.path.insert(0, str(REPO))
from connect import db

sql = Path(sys.argv[1]).read_text(encoding="utf-8").strip().rstrip(";")
label = sys.argv[2]
first = re.sub(r"^\s*(--[^\n]*\n\s*)*", "", sql).split(None, 1)[0].upper()
if first not in ("SELECT", "WITH") or ";" in sql:
    sys.exit("refusing")
c = db.connect()
try:
    cur = c.cursor()
    cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
    cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-skeptic-2026-09-24'")
    cur.execute(sql)
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    with open(HERE / f"out_{label}.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(cols); w.writerows(rows)
    print(" | ".join(cols))
    for r in rows[:200]:
        print(" | ".join("" if v is None else str(v) for v in r))
    print(f"({len(rows)} rows)")
finally:
    c.close()
