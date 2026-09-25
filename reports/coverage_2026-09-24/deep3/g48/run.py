"""g48 runner: one connection per batch file, read-only guard, logs every statement.

Usage: python reports/coverage_2026-09-24/deep3/g48/run.py <batch.sql>
Batch file: statements separated by lines starting with '-- [label]'.
Results land in g48/out_<label>.json; every statement is appended to deep3/g48.sql.
"""
import json
import re
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO))
from connect import db  # noqa: E402

HERE = Path(__file__).resolve().parent
SQL_LOG = HERE.parent / "g48.sql"
COUNT_FILE = HERE / "count.json"


def parse(text):
    parts = re.split(r"^-- \[([^\]]+)\]\s*$", text, flags=re.M)
    out = []
    for i in range(1, len(parts), 2):
        label = parts[i].strip()
        body = parts[i + 1].strip().rstrip(";").strip()
        # strip leading comment lines for the guard
        code = "\n".join(l for l in body.splitlines() if not l.strip().startswith("--")).strip()
        if not re.match(r"^(select|with)\b", code, flags=re.I):
            raise SystemExit(f"refusing non-read statement in [{label}]")
        if re.search(r"\b(insert|update|delete|drop|create|alter|merge|truncate|grant|revoke)\b\s", code, flags=re.I):
            # allow the words inside strings? keep it strict
            raise SystemExit(f"refusing statement with write keyword in [{label}]")
        out.append((label, body))
    return out


def main():
    batch = Path(sys.argv[1])
    stmts = parse(batch.read_text(encoding="utf-8"))
    cnt = json.loads(COUNT_FILE.read_text()) if COUNT_FILE.exists() else {"select": 0, "session": 0}
    c = db.connect()
    cur = c.cursor()
    setup = [
        "ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300",
        "ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'",
    ]
    for s in setup:
        cur.execute(s)
        cnt["session"] += 1
    with SQL_LOG.open("a", encoding="utf-8") as log:
        log.write(f"\n-- ===== connection: {batch.name} (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)\n")
        for label, body in stmts:
            t0 = time.time()
            err = None
            rows, cols = [], []
            try:
                cur.execute(body)
                cols = [d[0] for d in cur.description]
                rows = cur.fetchall()
            except Exception as e:  # keep going, record the error
                err = str(e)[:500]
            dt = time.time() - t0
            cnt["select"] += 1
            log.write(f"\n-- [{label}] ({dt:.1f}s{', ERROR' if err else ''})\n{body};\n")
            res = {"label": label, "cols": cols, "rows": [[str(x) if x is not None else None for x in r] for r in rows], "err": err, "secs": round(dt, 1)}
            (HERE / f"out_{label}.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
            print(f"===== [{label}] {dt:.1f}s rows={len(rows)} {'ERR ' + err if err else ''}")
            if cols:
                print(" | ".join(cols))
                for r in rows[:60]:
                    print(" | ".join("" if x is None else str(x) for x in r))
    cur.close()
    c.close()
    COUNT_FILE.write_text(json.dumps(cnt))
    print("COUNT", cnt)


if __name__ == "__main__":
    main()
