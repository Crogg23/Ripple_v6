"""g17 deep3 runner. Read-only. Runs one batch file of labelled SELECT/WITH statements.

Usage (repo root): python reports/coverage_2026-09-24/deep3/g17/run.py <batch.sql>
Statements are split on lines that start with '-- S'. Anything that is not
SELECT/WITH is refused before it reaches the warehouse.
"""
import json
import sys
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO))
from connect import db  # noqa: E402

HERE = Path(__file__).resolve().parent


def split(text):
    out, label, buf = [], None, []
    for line in text.splitlines():
        if line.startswith("-- S"):
            if label and "".join(buf).strip():
                out.append((label, "\n".join(buf).strip().rstrip(";")))
            label, buf = line[3:].strip(), []
        elif label:
            buf.append(line)
    if label and "".join(buf).strip():
        out.append((label, "\n".join(buf).strip().rstrip(";")))
    return out


def conv(v):
    if isinstance(v, Decimal):
        return float(v)
    if isinstance(v, (date, datetime)):
        return v.isoformat()
    return v


def main():
    batch = Path(sys.argv[1])
    stmts = split(batch.read_text(encoding="utf-8"))
    for label, sql in stmts:
        head = sql.lstrip().split(None, 1)[0].upper()
        if head not in ("SELECT", "WITH"):
            raise SystemExit(f"refused non-read statement {label}: {head}")
    c = db.connect()
    cur = c.cursor()
    cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
    cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'")
    results = {}
    for label, sql in stmts:
        try:
            cur.execute(sql)
            cols = [d[0] for d in cur.description]
            rows = [[conv(v) for v in r] for r in cur.fetchall()]
            results[label] = {"cols": cols, "rows": rows}
            print(f"\n===== {label}  ({len(rows)} rows)")
            print(" | ".join(cols))
            for r in rows[:80]:
                print(" | ".join("" if v is None else str(v) for v in r))
        except Exception as e:  # keep going; a failed statement still counts
            results[label] = {"error": str(e)[:500]}
            print(f"\n===== {label}  ERROR {str(e)[:300]}")
    cur.close()
    c.close()
    (HERE / (batch.stem + "_results.json")).write_text(
        json.dumps(results, indent=1, default=str), encoding="utf-8")
    print(f"\nstatements run: {len(stmts)} + 2 ALTER SESSION")


if __name__ == "__main__":
    main()
