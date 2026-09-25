"""g64 runner: read-only statements, one connection per call.

Usage: python run.py batch.sql
The batch holds blocks headed by '-- Sxx title'. Each block is one SELECT/WITH.
Output: stdout (first 60 rows), g64/out_<Sxx>.txt, and g64/out_<Sxx>.csv (all rows).
"""
import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO))
from connect import db  # noqa: E402


def blocks(text):
    parts = re.split(r"^(-- S\d+[a-z]?\b.*)$", text, flags=re.M)
    out = []
    for i in range(1, len(parts), 2):
        head = parts[i].strip()
        body = parts[i + 1].strip().rstrip(";").strip()
        label = head.split()[1]
        out.append((label, head, body))
    return out


def main():
    src = Path(sys.argv[1])
    todo = blocks(src.read_text(encoding="utf-8"))
    for label, head, body in todo:
        first = re.sub(r"^\s*(--[^\n]*\n\s*)*", "", body).lstrip("(").split(None, 1)[0].upper()
        if first not in ("SELECT", "WITH"):
            sys.exit(f"refusing {label}: starts with {first}")
        if ";" in body:
            sys.exit(f"refusing {label}: more than one statement")
    c = db.connect()
    try:
        cur = c.cursor()
        cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
        cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'")
        for label, head, body in todo:
            lines = [head]
            try:
                cur.execute(body)
                cols = [d[0] for d in cur.description]
                rows = cur.fetchall()
                with open(HERE / f"out_{label}.csv", "w", newline="", encoding="utf-8") as fh:
                    w = csv.writer(fh)
                    w.writerow(cols)
                    w.writerows(rows)
                lines.append(" | ".join(cols))
                for r in rows[:60]:
                    lines.append(" | ".join("" if v is None else str(v) for v in r))
                lines.append(f"({len(rows)} rows; csv has all)")
            except Exception as e:  # keep going; a failed statement still counts
                lines.append(f"ERROR: {e}")
            txt = "\n".join(lines)
            print(txt)
            print()
            (HERE / f"out_{label}.txt").write_text(txt, encoding="utf-8")
        cur.close()
    finally:
        c.close()


if __name__ == "__main__":
    main()
