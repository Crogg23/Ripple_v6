"""g14 runner: read-only. Runs '-- Qn: title' blocks from a batch file, appends them to ../g14.sql, prints results.
Each block must be one statement starting with SELECT or WITH (no inner semicolons)."""
import sys, re, os
sys.path.insert(0, r"C:\Code\Ripple_v6")
from connect import db

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "..", "g14.sql")
batch = open(sys.argv[1], encoding="utf-8").read()
blocks = re.split(r"(?m)^(?=-- Q\d+:)", batch)
blocks = [b.strip() for b in blocks if b.strip().startswith("-- Q")]


def body_of(b):
    return "\n".join(l for l in b.splitlines() if not l.strip().startswith("--")).strip().rstrip(";").strip()


for b in blocks:
    body = body_of(b)
    first = body.split(None, 1)[0].upper()
    assert first in ("SELECT", "WITH"), "read-only only, got: " + first
    assert ";" not in body, "one statement per block"

c = db.connect()
cur = c.cursor()
cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'")
maxrows = int(os.environ.get("MAXROWS", "80"))
with open(LOG, "a", encoding="utf-8") as log:
    for b in blocks:
        head = b.splitlines()[0]
        body = body_of(b)
        log.write("\n" + b.rstrip().rstrip(";") + ";\n")
        print("=" * 100)
        print(head)
        try:
            cur.execute(body)
            cols = [d[0] for d in cur.description]
            rs = cur.fetchall()
            m = re.search(r"\[save:(\w+)\]", head)
            if m:
                import csv
                with open(os.path.join(HERE, m.group(1) + ".csv"), "w", newline="", encoding="utf-8") as f:
                    w = csv.writer(f)
                    w.writerow(cols)
                    w.writerows(rs)
                print(f"saved {len(rs)} rows to {m.group(1)}.csv")
                continue
            print(" | ".join(cols))
            for r in rs[:maxrows]:
                print(" | ".join("" if v is None else str(v) for v in r))
            print(f"({len(rs)} rows)")
        except Exception as e:
            print("ERROR:", str(e)[:600])
c.close()
