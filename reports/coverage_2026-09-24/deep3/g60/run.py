"""g60 runner: read-only statements, one connection per batch file.

Usage: python run.py b1.sql
Blocks are headed by '-- Sxx title'. Each block is one SELECT/WITH.
Writes out_<Sxx>.txt (first 80 rows) and out_<Sxx>.csv (all rows), and appends to log.sql.
"""
import csv
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO))
from connect import db  # noqa: E402

WRITE_WORDS = r"\b(insert|update|delete|drop|create|alter|merge|truncate|grant)\b"


def blocks(text):
    parts = re.split(r"^(-- S\d+[a-z]?\b.*)$", text, flags=re.M)
    out = []
    for i in range(1, len(parts), 2):
        head = parts[i].strip()
        body = parts[i + 1].strip().rstrip(";").strip()
        out.append((head.split()[1], head, body))
    return out


def main():
    src = Path(sys.argv[1])
    todo = blocks(src.read_text(encoding="utf-8"))
    for label, head, body in todo:
        stripped = re.sub(r"^\s*(--[^\n]*\n\s*)*", "", body).lstrip("(")
        first = stripped.split(None, 1)[0].upper()
        if first not in ("SELECT", "WITH"):
            sys.exit(f"refusing {label}: starts with {first}")
        if ";" in body:
            sys.exit(f"refusing {label}: more than one statement")
        no_strings = re.sub(r"'[^']*'", "", body)
        no_comments = re.sub(r"--[^\n]*", "", no_strings)
        bad = re.search(WRITE_WORDS, no_comments, re.I)
        if bad:
            sys.exit(f"refusing {label}: contains {bad.group(0)}")
    c = db.connect()
    log = open(HERE / "log.sql", "a", encoding="utf-8")
    log.write(f"\n-- ===== connection: {src.name} (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)\n")
    try:
        cur = c.cursor()
        cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
        cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'")
        for label, head, body in todo:
            lines = [head]
            t0 = time.time()
            try:
                cur.execute(body)
                cols = [d[0] for d in cur.description]
                rows = cur.fetchall()
                with open(HERE / f"out_{label}.csv", "w", newline="", encoding="utf-8") as fh:
                    w = csv.writer(fh)
                    w.writerow(cols)
                    w.writerows(rows)
                lines.append(" | ".join(cols))
                for r in rows[:80]:
                    lines.append(" | ".join("" if v is None else str(v) for v in r))
                lines.append(f"({len(rows)} rows; csv has all)")
                status = f"{time.time() - t0:.1f}s, {len(rows)} rows"
            except Exception as e:  # keep going; a failed statement still counts
                lines.append(f"ERROR: {e}")
                status = f"{time.time() - t0:.1f}s, ERROR"
            log.write(f"\n{head} ({status})\n{body};\n")
            txt = "\n".join(lines)
            print(txt)
            print()
            (HERE / f"out_{label}.txt").write_text(txt, encoding="utf-8")
        cur.close()
    finally:
        log.close()
        c.close()


if __name__ == "__main__":
    main()
