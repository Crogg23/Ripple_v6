"""g67 deep3 runner: read-only SELECT/WITH only, logs every statement to g67.sql, saves results as pickled DataFrames."""
import sys, re, time
from pathlib import Path
import pandas as pd
REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO))
from connect import db

HERE = Path(__file__).resolve().parent
SQL_LOG = HERE.parent / "g67.sql"
COUNT_FILE = HERE / "count.txt"
REFUSE = ["INSERT", "UPDATE", "DELETE", "DROP", "CREATE", "ALTER", "MERGE", "TRUNCATE", "GRANT", "PUT", "COPY"]
BUDGET = 35


def load_queries(path):
    txt = Path(path).read_text(encoding="utf-8")
    blocks = re.split(r"^--\s*@(\S+)\s*$", txt, flags=re.M)
    return [(blocks[i], blocks[i + 1].strip().rstrip(";")) for i in range(1, len(blocks), 2)]


def main(qfile):
    qs = load_queries(qfile)
    for label, sql in qs:
        body = "\n".join(l for l in sql.splitlines() if not l.strip().startswith("--"))
        head = body.lstrip().upper()
        if not (head.startswith("SELECT") or head.startswith("WITH")):
            raise SystemExit(f"refused non-read statement {label}")
        words = set(re.findall(r"[A-Z_]+", re.sub(r"'[^']*'", "", body).upper()))
        hit = [w for w in REFUSE if w in words]
        if hit:
            raise SystemExit(f"refused {label}: contains {hit}")
    n = int(COUNT_FILE.read_text()) if COUNT_FILE.exists() else 0
    if n + len(qs) > BUDGET:
        raise SystemExit(f"budget: {n} used, {len(qs)} asked, cap {BUDGET}")
    c = db.connect()
    cur = c.cursor()
    cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
    cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'")
    for label, sql in qs:
        n += 1
        t0 = time.time()
        with open(SQL_LOG, "a", encoding="utf-8") as f:
            f.write(f"\n-- S{n:02d} {label}\n{sql};\n")
        try:
            cur.execute(sql)
            cols = [d[0] for d in cur.description]
            rows = cur.fetchall()
            err = None
        except Exception as e:
            cols, rows, err = [], [], str(e)
        dt = time.time() - t0
        COUNT_FILE.write_text(str(n))
        print(f"== S{n:02d} {label} ({dt:.1f}s) {'ERR ' + err if err else str(len(rows)) + ' rows'}")
        if err:
            continue
        df = pd.DataFrame(rows, columns=cols)
        df.to_pickle(HERE / f"S{n:02d}_{label}.pkl")
        with pd.option_context("display.max_columns", 40, "display.width", 250, "display.max_colwidth", 60):
            print(df.head(40).to_string())
    cur.close()
    c.close()


if __name__ == "__main__":
    main(sys.argv[1])
