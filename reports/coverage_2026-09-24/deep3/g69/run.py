"""g69 read-only runner. Usage: python run.py q01 [q02 ...]
Each qNN.sql in this folder: comment lines, then one SELECT/WITH statement.
Results -> qNN.json; statement appended to ../g69.sql; counter in count.txt."""
import sys, json, re, datetime, decimal
from pathlib import Path
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO))
from connect import db

WRITE_WORDS = ["INS" + "ERT", "UPD" + "ATE", "DEL" + "ETE", "DR" + "OP", "CRE" + "ATE", "ALT" + "ER",
               "MER" + "GE", "TRUNC" + "ATE", "GR" + "ANT", "REV" + "OKE", "CA" + "LL", "PU" + "T", "CO" + "PY"]


def clean(sql):
    body = "\n".join(l for l in sql.splitlines() if not l.strip().startswith("--")).strip().rstrip(";")
    head = body.lstrip().split(None, 1)[0].upper()
    if head not in ("SELECT", "WITH"):
        raise SystemExit(f"refused: statement starts with {head}")
    stripped = re.sub(r"'[^']*'", "''", body)
    for w in WRITE_WORDS:
        if re.search(r"\b" + w + r"\b", stripped, re.I):
            raise SystemExit(f"refused: contains {w}")
    return body


def conv(v):
    if isinstance(v, (datetime.date, datetime.datetime)):
        return v.isoformat()
    if isinstance(v, decimal.Decimal):
        return float(v)
    return v


labels = sys.argv[1:]
stmts = []
for lab in labels:
    raw = (HERE / f"{lab}.sql").read_text(encoding="utf-8")
    stmts.append((lab, raw, clean(raw)))
c = db.connect()
cur = c.cursor()
cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'")
cnt_f = HERE / "count.txt"
n = int(cnt_f.read_text()) if cnt_f.exists() else 0
for lab, raw, body in stmts:
    n += 1
    cnt_f.write_text(str(n))
    with open(HERE.parent / "g69.sql", "a", encoding="utf-8") as f:
        f.write(f"\n-- [{lab}] statement {n}\n{raw.strip().rstrip(';')};\n")
    try:
        cur.execute(body)
        cols = [d[0] for d in cur.description]
        rows = [[conv(v) for v in r] for r in cur.fetchall()]
        (HERE / f"{lab}.json").write_text(json.dumps({"cols": cols, "rows": rows}, default=str, indent=0), encoding="utf-8")
        print(f"===== {lab} (stmt {n}) {len(rows)} rows")
        print(" | ".join(cols))
        for r in rows[:90]:
            print(" | ".join("" if v is None else str(v) for v in r))
    except Exception as e:
        print(f"===== {lab} (stmt {n}) ERROR: {e}")
cur.close()
c.close()
