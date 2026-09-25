"""g79 runner: runs numbered read-only statements from a .sql batch file, saves each result as CSV."""
import sys, re, csv, json
from pathlib import Path
sys.path.insert(0, r"C:\Code\Ripple_v6")
from connect import db

HERE = Path(__file__).parent
batch = Path(sys.argv[1])
text = batch.read_text(encoding="utf-8")
# statements separated by lines starting with '-- S'
parts = re.split(r"(?m)^(-- S\d+[^\n]*)\n", text)
stmts = []
for i in range(1, len(parts), 2):
    head = parts[i]; body = parts[i + 1].strip().rstrip(";")
    sid = re.match(r"-- (S\d+)", head).group(1)
    stmts.append((sid, head, body))
for sid, head, body in stmts:
    first = re.sub(r"--[^\n]*\n", "", body).strip().split()[0].upper()
    assert first in ("SELECT", "WITH"), f"{sid} not read-only: {first}"
c = db.connect()
cur = c.cursor()
cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'")
for sid, head, body in stmts:
    print("==", head, flush=True)
    try:
        cur.execute(body)
        cols = [d[0] for d in cur.description]
        rows = cur.fetchall()
        with open(HERE / f"out_{sid}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(cols)
            for r in rows:
                w.writerow([json.dumps(v, default=str) if isinstance(v, (dict, list)) else v for v in r])
        print(f"   {len(rows)} rows, cols={cols}")
    except Exception as e:
        print("   ERROR", e)
cur.close(); c.close()
