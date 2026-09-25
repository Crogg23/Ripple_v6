"""skeptic runner: read-only SELECT/WITH only. Usage: python run.py batch.sql"""
import csv, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
from connect import db  # noqa

def blocks(text):
    parts = re.split(r"^(-- Q\d+\b.*)$", text, flags=re.M)
    return [(parts[i].split()[1], parts[i].strip(), parts[i+1].strip().rstrip(";").strip()) for i in range(1, len(parts), 2)]

todo = blocks(Path(sys.argv[1]).read_text(encoding="utf-8"))
for label, head, body in todo:
    first = re.sub(r"^\s*(--[^\n]*\n\s*)*", "", body).split(None, 1)[0].upper()
    if first not in ("SELECT", "WITH") or ";" in body:
        sys.exit(f"refusing {label}")
c = db.connect()
try:
    cur = c.cursor()
    cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
    cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-skeptic-2026-09-24'")
    for label, head, body in todo:
        print(head)
        try:
            cur.execute(body)
            cols = [d[0] for d in cur.description]
            rows = cur.fetchall()
            with open(HERE / f"out_{label}.csv", "w", newline="", encoding="utf-8") as fh:
                w = csv.writer(fh); w.writerow(cols); w.writerows(rows)
            print(" | ".join(cols))
            for r in rows[:40]:
                print(" | ".join("" if v is None else str(v) for v in r))
            print(f"({len(rows)} rows)")
        except Exception as e:
            print("ERROR:", e)
finally:
    c.close()
