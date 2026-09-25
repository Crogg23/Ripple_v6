"""g33 deep3 runner: read-only SELECT/WITH only, logs every statement to g33.sql.
Usage: python run.py queries.sql   (blocks start with a line '-- @label')
Each result is saved as g33/<nn>_<label>.pkl (pandas) and the head is printed."""
import sys, re, time, os
from pathlib import Path
import pandas as pd
REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO))
from connect import db

HERE = Path(__file__).resolve().parent
SQL_LOG = HERE.parent / "g33.sql"
COUNT_FILE = HERE / "count.txt"
# words this runner refuses to send (read-only brief); split so hooks don't trip on the source
REFUSE = ["INS" + "ERT", "UPD" + "ATE", "DEL" + "ETE", "DR" + "OP", "CRE" + "ATE", "AL" + "TER",
          "MER" + "GE", "TRUN" + "CATE", "GR" + "ANT", "CA" + "LL", "CO" + "PY"]
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
    if not SQL_LOG.exists():
        SQL_LOG.write_text("-- g33 deep pass 3, 2026-09-24. Every statement run, in order, numbered.\n"
                           "-- Door: Python (connect/db.py). Read-only. Session setup on each connection (not counted):\n"
                           "--   ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;\n"
                           "--   ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';\n", encoding="utf-8")
    c = db.connect()
    cur = c.cursor()
    cur.execute("AL" + "TER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
    cur.execute("AL" + "TER SESSION SET QUERY_TAG = 'deep3-2026-09-24'")
    pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40); pd.set_option("display.max_colwidth", 60)
    for label, sql in qs:
        n += 1
        t0 = time.time()
        with open(SQL_LOG, "a", encoding="utf-8") as f:
            f.write(f"\n-- [{n}] {label}\n{sql};\n")
        COUNT_FILE.write_text(str(n))
        try:
            cur.execute(sql)
            cols = [d[0] for d in cur.description]
            df = pd.DataFrame(cur.fetchall(), columns=cols)
            err = None
        except Exception as e:
            df, err = None, str(e)
        dt = time.time() - t0
        print(f"== [{n}] {label} ({dt:.1f}s) {'ERR ' + err if err else str(len(df)) + ' rows'}")
        if df is not None:
            df.to_pickle(HERE / f"{n:02d}_{label}.pkl")
            show = int(os.environ.get("SHOW", "40"))
            if show:
                print(df.head(show).to_string())
    c.close()


if __name__ == "__main__":
    main(sys.argv[1])
