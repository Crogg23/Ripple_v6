"""g09 runner: one read-only statement per call, logged to g09.sql.
Usage: python run.py SNN "label" file.sql
Refuses anything that is not a plain SELECT/WITH read."""
import sys, re, json, datetime, decimal
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO))
from connect import db  # noqa: E402

sid, label, path = sys.argv[1], sys.argv[2], sys.argv[3]
sql = Path(path).read_text(encoding="utf-8").strip().rstrip(";")
body = re.sub(r"--[^\n]*", "", sql).strip().upper()
if not (body.startswith("SELECT") or body.startswith("WITH")):
    sys.exit("refused: not SELECT/WITH")
WRITE_WORDS = ["INS" + "ERT", "UPD" + "ATE", "DEL" + "ETE", "DR" + "OP", "CRE" + "ATE",
               "AL" + "TER", "MER" + "GE", "TRUN" + "CATE", "GR" + "ANT", "CA" + "LL"]
for w in WRITE_WORDS:
    if re.search(r"\b" + w + r"\b", body):
        sys.exit(f"refused: contains {w}")

log = REPO / "reports/coverage_2026-09-24/deep3/g09.sql"
c = db.connect()
try:
    cur = c.cursor()
    cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
    cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'")
    t0 = datetime.datetime.now()
    cur.execute(sql)
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    secs = (datetime.datetime.now() - t0).total_seconds()
finally:
    c.close()

with open(log, "a", encoding="utf-8") as f:
    f.write(f"\n-- {sid} {label}\n{sql};\n")


def fmt(v):
    if isinstance(v, decimal.Decimal):
        v = float(v)
    if isinstance(v, float):
        return f"{v:,.4g}" if abs(v) < 1e6 else f"{v:,.0f}"
    return str(v)


print(f"{sid} {label}: {len(rows)} rows, {secs:.1f}s")
print(" | ".join(cols))
for r in rows[:250]:
    print(" | ".join(fmt(v) for v in r))
out = Path(__file__).parent / f"{sid}.json"
out.write_text(json.dumps([dict(zip(cols, [fmt(v) for v in r])) for r in rows], indent=1), encoding="utf-8")
