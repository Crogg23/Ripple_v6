"""Skeptic read-only runner. Usage: python run.py s01 [s02 ...]  (sNN.sql in this folder)
Counts statements (incl. the 2 ALTER SESSION lines) in count.txt."""
import sys, json, re, datetime, decimal
from pathlib import Path
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
from connect import db
BAD = ["INS"+"ERT","UPD"+"ATE","DEL"+"ETE","DR"+"OP","CRE"+"ATE","ALT"+"ER","MER"+"GE","TRUNC"+"ATE","GR"+"ANT","REV"+"OKE","CA"+"LL","PU"+"T","CO"+"PY"]
def clean(sql):
    body = "\n".join(l for l in sql.splitlines() if not l.strip().startswith("--")).strip().rstrip(";")
    head = body.lstrip().split(None,1)[0].upper()
    if head not in ("SELECT","WITH"): raise SystemExit("refused "+head)
    s = re.sub(r"'[^']*'","''",body)
    for w in BAD:
        if re.search(r"\b"+w+r"\b", s, re.I): raise SystemExit("refused "+w)
    return body
def conv(v):
    if isinstance(v,(datetime.date,datetime.datetime)): return v.isoformat()
    if isinstance(v,decimal.Decimal): return float(v)
    return v
labs = sys.argv[1:]
st = [(l, clean((HERE/f"{l}.sql").read_text(encoding="utf-8"))) for l in labs]
cf = HERE/"count.txt"; n = int(cf.read_text()) if cf.exists() else 0
c = db.connect(); cur = c.cursor()
cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-skeptic-2026-09-24'")
n += 2; cf.write_text(str(n))
for l, b in st:
    n += 1; cf.write_text(str(n))
    try:
        cur.execute(b); cols=[d[0] for d in cur.description]; rows=[[conv(v) for v in r] for r in cur.fetchall()]
        (HERE/f"{l}.json").write_text(json.dumps({"cols":cols,"rows":rows},default=str),encoding="utf-8")
        print(f"== {l} stmt {n}: {len(rows)} rows"); print(" | ".join(cols))
        for r in rows[:200]: print(" | ".join("" if v is None else str(v) for v in r))
    except Exception as e:
        print(f"== {l} stmt {n} ERROR {e}")
cur.close(); c.close()
