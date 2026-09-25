"""g29 runner: read-only statements, one connection per call.

Usage: python run.py batch.sql
The batch holds blocks headed by '-- Sxx title'. Each block is one SELECT/WITH.
Output: stdout (first 40 rows), g29/out_<Sxx>.txt, .csv and .pkl (all rows).
"""
import re
import sys
import time
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO))
from connect import db  # noqa: E402

WRITE_WORDS = ["INS" + "ERT", "UPD" + "ATE", "DEL" + "ETE", "DR" + "OP", "CRE" + "ATE",
               "AL" + "TER", "MER" + "GE", "TRUN" + "CATE", "GR" + "ANT", "CO" + "PY"]


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
        code = re.sub(r"--[^\n]*", "", body)
        first = code.strip().lstrip("(").split(None, 1)[0].upper()
        if first not in ("SELECT", "WITH"):
            sys.exit(f"refusing {label}: starts with {first}")
        if ";" in code:
            sys.exit(f"refusing {label}: more than one statement")
        for w in WRITE_WORDS:
            if re.search(r"\b" + w + r"\b", code, flags=re.I):
                sys.exit(f"refusing {label}: contains {w}")
    c = db.connect()
    log = []
    try:
        cur = c.cursor()
        cur.execute("AL" + "TER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
        cur.execute("AL" + "TER SESSION SET QUERY_TAG = 'deep3-2026-09-24'")
        for label, head, body in todo:
            lines = [head]
            t0 = time.time()
            try:
                cur.execute(body)
                qid = cur.sfqid
                cols = [d[0] for d in cur.description]
                rows = cur.fetchall()
                df = pd.DataFrame(rows, columns=cols)
                df.to_pickle(HERE / f"out_{label}.pkl")
                df.to_csv(HERE / f"out_{label}.csv", index=False)
                lines.append(" | ".join(cols))
                for r in rows[:40]:
                    lines.append(" | ".join("" if v is None else str(v) for v in r))
                lines.append(f"({len(rows)} rows; {time.time()-t0:.1f}s; qid {qid})")
                log.append(f"{label}\t{len(rows)} rows\t{time.time()-t0:.1f}s\t{qid}")
            except Exception as e:  # keep going; a failed statement still counts
                lines.append(f"ERROR: {e}")
                log.append(f"{label}\tERROR\t{str(e)[:200]}")
            txt = "\n".join(lines)
            print(txt[:5000])
            print()
            (HERE / f"out_{label}.txt").write_text(txt, encoding="utf-8")
        cur.close()
    finally:
        c.close()
    with open(HERE / "runlog.tsv", "a", encoding="utf-8") as fh:
        fh.write("\n".join(log) + "\n")


if __name__ == "__main__":
    main()
