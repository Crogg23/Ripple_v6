"""Skeptic read-only runner for g72 / DIM_TRACT. SELECT/WITH only. Usage: python run.py batchfile.sql
Statements separated by a line '-- @@ name'."""
import sys, json, re, datetime, decimal
from pathlib import Path
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
from connect import db
BAD = ["INS"+"ERT","UPD"+"ATE","DEL"+"ETE","DR"+"OP","CRE"+"ATE","ALT"+"ER","MER"+"GE","TRUNC"+"ATE","GR"+"ANT","REV"+"OKE","CA"+"LL","PU"+"T","CO"+"PY"]
def conv(v):
    if isinstance(v,(datetime.date,datetime.datetime)): return v.isoformat()
    if isinstance(v,decimal.Decimal): return float(v)
    return v
txt = (HERE/sys.argv[1]).read_text(encoding="utf-8")
parts = re.split(r"^-- @@ (\S+)\s*$", txt, flags=re.M)
stmts = [(parts[i], parts[i+1].strip().rstrip(";")) for i in range(1,len(parts),2)]
for name, body in stmts:
    b = "\n".join(l for l in body.splitlines() if not l.strip().startswith("--")).strip()
    if b.split(None,1)[0].upper() not in ("SELECT","WITH"): raise SystemExit(f"refused {name}")
    s = re.sub(r"'[^']*'","''",b)
    for w in BAD:
        if re.search(r"\b"+w+r"\b", s, re.I): raise SystemExit(f"refused {name}: {w}")
c = db.connect(); cur = c.cursor()
cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-skeptic-2026-09-24'")
out = {}
for name, body in stmts:
    try:
        cur.execute(body)
        cols=[d[0] for d in cur.description]; rows=[[conv(v) for v in r] for r in cur.fetchall()]
        out[name]={"cols":cols,"rows":rows}
        print(f"===== {name}: {len(rows)} rows"); print(" | ".join(cols))
        for r in rows[:120]: print(" | ".join("" if v is None else str(v) for v in r))
    except Exception as e:
        out[name]={"error":str(e)}; print(f"===== {name} ERROR {e}")
cur.close(); c.close()
(HERE/(Path(sys.argv[1]).stem+".json")).write_text(json.dumps(out,default=str,indent=0),encoding="utf-8")
