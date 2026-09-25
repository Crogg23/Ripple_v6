"""Skeptic pass on g17 Duffy lead. Read-only: SELECT/WITH only. Run from repo root."""
import json, sys
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))
from connect import db  # noqa: E402
HERE = Path(__file__).resolve().parent
L = "LIBRARY_RAW.LANDING.FED_FEC_COMMITTEE_TO_COMMITTEE"
SUM = "LIBRARY_MARTS.POLITICS.POLITICS__FEC_CANDIDATE_SUMMARY"
CAND = "LIBRARY_MARTS.POLITICS.POLITICS__FEC_CANDIDATE"
CM = "LIBRARY_MARTS.POLITICS.POLITICS__FEC_COMMITTEE"
Q = {}
for k in (sys.argv[1:] or ["K1", "K2", "K3", "K4", "K5", "K6"]):
    Q[k] = (HERE / (k + ".sql")).read_text(encoding="utf-8")


def conv(v):
    if isinstance(v, Decimal):
        return float(v)
    if isinstance(v, (date, datetime)):
        return v.isoformat()
    return v


def main():
    for k, sql in Q.items():
        head = sql.lstrip().split(None, 1)[0].upper()
        if head not in ("SELECT", "WITH"):
            raise SystemExit("refused " + k)
    c = db.connect()
    cur = c.cursor()
    cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
    cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-skeptic-2026-09-24'")
    out = {}
    for k, sql in Q.items():
        try:
            cur.execute(sql)
            cols = [d[0] for d in cur.description]
            rows = [[conv(v) for v in r] for r in cur.fetchall()]
            out[k] = {"cols": cols, "rows": rows}
            print("\n===== %s (%d rows)" % (k, len(rows)))
            print(" | ".join(cols))
            for r in rows[:160]:
                print(" | ".join("" if v is None else str(v) for v in r))
        except Exception as e:
            out[k] = {"error": str(e)[:600]}
            print("\n===== %s ERROR %s" % (k, str(e)[:600]))
    cur.close()
    c.close()
    (HERE / ("skeptic_results_" + "_".join(sys.argv[1:]) + ".json" if sys.argv[1:] else "skeptic_results.json")).write_text(json.dumps(out, indent=1, default=str), encoding="utf-8")
    print("\nstatements: %d + 2 ALTER SESSION" % len(Q))


if __name__ == "__main__":
    main()
