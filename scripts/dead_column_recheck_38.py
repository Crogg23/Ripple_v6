"""Re-check the 38 columns the first diagnosis waved through.

Two bad rules in the first pass:
  ROW_SUBSET  fired on any row-count difference, before looking at values.
              Dropping 80 of 12,847 rows cannot empty a full column.
  sampling    500K-row sample on big tables saw no values and called the
              column raw-empty. The exact count says otherwise.

This pass uses exact counts, no sampling, and asks the only question that
matters: does raw hold values the mart does not?

Writes reports/dead_columns_recheck_2026-09-08.csv.
"""

from __future__ import annotations

import collections
import csv
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from connect import db  # noqa: E402

SUSPECT = {"ROW_SUBSET", "raw_also_empty"}


def probe(item):
    """Exact non-blank counts on both sides, plus top raw values."""
    (schema, mart, raw), cols = item
    cols = sorted(set(cols))
    conn = db.connect()
    out = {}
    try:
        msel, rsel = ["count(*)"], ["count(*)"]
        for c in cols:
            msel.append(f"count_if(trim(to_varchar(\"{c}\")) <> '')")
            rsel.append(f"count_if(trim(to_varchar(\"{c}\")) <> '')")
        mv = db.rows(conn, f'select {", ".join(msel)} from LIBRARY_MARTS."{schema}"."{mart}"')[0]
        rv = db.rows(conn, f'select {", ".join(rsel)} from {raw}')[0]

        # top values for the ones raw actually holds, no sample
        need = [c for i, c in enumerate(cols) if rv[1 + i] > 0 and mv[1 + i] == 0]
        tops: dict[str, str] = {}
        if need:
            pairs = ", ".join(f"'{c}', to_varchar(\"{c}\")" for c in need)
            sql = f"""
            select f.key::varchar, f.value::varchar, count(*)
            from {raw}, lateral flatten(input => object_construct_keep_null({pairs})) f
            where trim(f.value::varchar) <> ''
            group by 1, 2
            qualify row_number() over (partition by f.key::varchar order by count(*) desc) <= 5
            """
            acc: dict[str, list[str]] = {}
            for col, val, cnt in db.rows(conn, sql):
                acc.setdefault(col, []).append(f"{val} {cnt}")
            tops = {k: " | ".join(v)[:200] for k, v in acc.items()}

        for i, c in enumerate(cols):
            out[c] = dict(
                mart_rows=mv[0], raw_rows=rv[0],
                mart_non_blank=mv[1 + i], raw_non_blank=rv[1 + i],
                raw_top_values=tops.get(c, ""),
            )
        return (schema, mart, raw), out, ""
    except Exception as exc:  # noqa: BLE001
        return (schema, mart, raw), {}, str(exc)[:160]
    finally:
        conn.close()


def main():
    path = sorted((REPO / "reports").glob("dead_columns_2026-09-08.csv"))[-1]
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    targets = [r for r in rows if r["verdict"] in SUSPECT and r["raw_table"]]

    by = collections.defaultdict(list)
    for r in targets:
        by[(r["schema"], r["mart_table"], r["raw_table"])].append(r["column"])
    print(f"{len(targets)} columns across {len(by)} tables")

    got: dict = {}
    with ThreadPoolExecutor(max_workers=6) as ex:
        for key, res, err in ex.map(probe, by.items()):
            if err:
                print("ERR", key[1], err)
            got[key] = res

    out_rows = []
    for r in targets:
        key = (r["schema"], r["mart_table"], r["raw_table"])
        d = got.get(key, {}).get(r["column"])
        if not d:
            continue
        if d["raw_non_blank"] == 0:
            v = "raw_also_empty"
        elif d["mart_non_blank"] == 0:
            v = "MODEL_LOST_IT"
        elif d["mart_non_blank"] >= d["raw_non_blank"] * 0.999:
            v = "SOURCE_THIN"
        else:
            v = "PARTIAL_LOSS"
        out_rows.append(dict(
            schema=r["schema"], mart_table=r["mart_table"], column=r["column"],
            raw_table=r["raw_table"], old_verdict=r["verdict"], verdict=v,
            **d,
        ))

    out = REPO / "reports" / "dead_columns_recheck_2026-09-08.csv"
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        w.writerows(out_rows)

    t = collections.Counter(r["verdict"] for r in out_rows)
    print(f"wrote {out}")
    for k, v in t.most_common():
        print(f"  {v:6}  {k}")
    for r in out_rows:
        if r["verdict"] in ("MODEL_LOST_IT", "PARTIAL_LOSS"):
            print(f"   {r['verdict']:14} {r['mart_table'][:38]:38} {r['column'][:30]:30} "
                  f"raw={r['raw_non_blank']:>8} mart={r['mart_non_blank']:>8}")


if __name__ == "__main__":
    main()
