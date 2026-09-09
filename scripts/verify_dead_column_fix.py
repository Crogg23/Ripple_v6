"""Did the 118 columns come back? Count them in the rebuilt mart tables."""

from __future__ import annotations

import collections
import csv
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from connect import db  # noqa: E402


def check(item):
    (sch, tbl), cols = item
    cols = sorted(set(cols))
    sel = ["count(*)"]
    for c in cols:
        sel.append(f'count("{c}")')
        sel.append(f"count_if(trim(to_varchar(\"{c}\")) <> '')")
    conn = db.connect()
    try:
        v = db.rows(conn, f'select {", ".join(sel)} from LIBRARY_MARTS."{sch}"."{tbl}"')[0]
        return tbl, cols, v, ""
    except Exception as exc:  # noqa: BLE001
        return tbl, cols, None, str(exc)[:120]
    finally:
        conn.close()


def main():
    path = sorted((REPO / "reports").glob("dead_columns_*.csv"))[-1]
    by = collections.defaultdict(list)
    raw_nb = {}
    for r in csv.DictReader(open(path, encoding="utf-8")):
        if r["verdict"] != "MODEL_LOST_IT":
            continue
        by[(r["schema"], r["mart_table"])].append(r["column"])
        raw_nb[(r["mart_table"], r["column"])] = int(r["raw_non_blank"] or 0)

    alive, still, errs = 0, [], []
    rows_out = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        for tbl, cols, v, err in ex.map(check, by.items()):
            if err:
                errs.append((tbl, err))
                continue
            for i, c in enumerate(cols):
                nn, nb = v[1 + i * 2], v[2 + i * 2]
                rows_out.append((tbl, c, v[0], nn, nb, raw_nb.get((tbl, c), 0)))
                if nb > 0:
                    alive += 1
                else:
                    still.append((tbl, c))

    print(f"columns now carrying values : {alive}")
    print(f"columns still empty         : {len(still)}")
    for t, c in still:
        print(f"   still empty: {t} . {c}")
    for t, e in errs:
        print(f"   ERROR: {t} {e}")

    out = REPO / "reports" / "dead_column_fix_verified_2026-09-08.csv"
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["mart_table", "column", "rows", "non_null", "non_blank", "raw_non_blank"])
        w.writerows(sorted(rows_out))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
