"""g76 deep3 runner: read-only SELECT/WITH only. Logs every statement it sends to g76/sent.sql.

Usage: python run.py b1.sql   (blocks separated by lines '-- @Sxx label')
"""
import sys, json, re, time
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO))
from connect import db  # noqa: E402

HERE = Path(__file__).resolve().parent
SENT = HERE / "sent.sql"
COUNT_FILE = HERE / "count.txt"
REFUSE = ["INSERT", "UPDATE", "DELETE", "DROP", "CREATE", "ALTER", "MERGE", "TRUNCATE", "GRANT", "PUT", "COPY"]
BUDGET = 35


def load(path):
    txt = Path(path).read_text(encoding="utf-8")
    parts = re.split(r"^--\s*@(\S+)\s*(.*)$", txt, flags=re.M)
    out = []
    for i in range(1, len(parts), 3):
        out.append((parts[i], parts[i + 1].strip(), parts[i + 2].strip().rstrip(";")))
    return out


def main(qfile):
    qs = load(qfile)
    for sid, label, sql in qs:
        body = "\n".join(l for l in sql.splitlines() if not l.strip().startswith("--"))
        head = body.lstrip().upper()
        if not (head.startswith("SELECT") or head.startswith("WITH")):
            raise SystemExit(f"refused non-read statement {sid}")
        words = set(re.findall(r"[A-Z_]+", re.sub(r"'[^']*'", "", body).upper()))
        hit = [w for w in REFUSE if w in words]
        if hit:
            raise SystemExit(f"refused {sid}: contains {hit}")
    n = int(COUNT_FILE.read_text()) if COUNT_FILE.exists() else 0
    if n + len(qs) > BUDGET:
        raise SystemExit(f"budget: {n} used, {len(qs)} more would pass {BUDGET}")
    c = db.connect()
    cur = c.cursor()
    cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
    cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'")
    for sid, label, sql in qs:
        n += 1
        COUNT_FILE.write_text(str(n))
        with open(SENT, "a", encoding="utf-8") as f:
            f.write(f"\n-- {sid} {label}\n{sql};\n")
        t0 = time.time()
        try:
            cur.execute(sql)
            cols = [d[0] for d in cur.description]
            rows = cur.fetchall()
            err = None
        except Exception as e:  # noqa: BLE001
            cols, rows, err = [], [], str(e)
        dt = time.time() - t0
        res = {"sid": sid, "label": label, "secs": round(dt, 1), "cols": cols,
               "rows": [[(str(v) if v is not None else None) for v in r] for r in rows], "err": err}
        if len(rows) > 500:
            import csv
            with open(HERE / f"out_{sid}.csv", "w", newline="", encoding="utf-8") as fh:
                w = csv.writer(fh); w.writerow(cols); w.writerows(res["rows"])
            res["rows"] = res["rows"][:20]
        (HERE / f"out_{sid}.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
        print(f"== {sid} [{n}] {label} ({dt:.1f}s) {'ERR ' + err if err else str(len(rows)) + ' rows'}")
        if not err:
            print(" | ".join(cols))
            for r in rows[:(120 if len(rows) <= 500 else 10)]:
                print(" | ".join("" if v is None else str(v) for v in r))
    cur.close()
    c.close()


if __name__ == "__main__":
    main(sys.argv[1])
