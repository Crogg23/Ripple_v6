"""Skeptic pass on g78 FRA rail deaths lead. Read-only: SELECT/WITH only.
Usage: python sk.py s1 s2 ...   (runs only named statements; counter in count.txt)"""
import sys, json, re
from pathlib import Path
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
from connect import db
from queries import Q

WRITE = ["INS"+"ERT","UPD"+"ATE","DEL"+"ETE","DR"+"OP","CRE"+"ATE","ALT"+"ER","MER"+"GE","TRUNC"+"ATE","GR"+"ANT","REV"+"OKE","CA"+"LL","PU"+"T","CO"+"PY"]
QUOTED = re.compile("\x27[^\x27]*\x27")
def guard(sql):
    head = sql.lstrip().split(None,1)[0].upper()
    assert head in ("SELECT","WITH"), head
    s = QUOTED.sub("", sql)
    for w in WRITE:
        assert not re.search(r"\b"+w+r"\b", s, re.I), w
    return sql

names = sys.argv[1:]
for k in names: guard(Q[k])
cnt = HERE/"count.txt"
n = int(cnt.read_text()) if cnt.exists() else 0
c = db.connect(); cur = c.cursor()
cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-skeptic-2026-09-24'")
for k in names:
    n += 1; cnt.write_text(str(n))
    try:
        cur.execute(Q[k]); cols=[d[0] for d in cur.description]; rows=cur.fetchall(); err=None
    except Exception as e:
        cols, rows, err = [], [], str(e)
    (HERE/f"{k}.json").write_text(json.dumps({"sql":Q[k],"cols":cols,"rows":[[None if v is None else str(v) for v in r] for r in rows],"err":err},indent=1),encoding="utf-8")
    print("==", k, f"(stmt {n})", err or f"{len(rows)} rows"); print(" | ".join(cols))
    for r in rows[:90]: print(" | ".join("" if v is None else str(v) for v in r))
cur.close(); c.close()
