"""Profile every column in LIBRARY_MARTS.

Pass 1 (one scan per table): row_count, non_null, distinct, min, max, blank.
Pass 2 (one scan per table): top-5 values for low-cardinality columns, via
flatten over an object built from the qualifying columns. Tables above
SAMPLE_OVER rows are sampled; those rows carry sampled=Y.

Writes reports/catalog_profile_<date>.csv, one row per column.
"""

from __future__ import annotations

import csv
import datetime as dt
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from connect import db  # noqa: E402

DB = "LIBRARY_MARTS"
THREADS = 6
SAMPLE_OVER = 2_000_000
SAMPLE_ROWS = 500_000
TOPN_MAX_DISTINCT = 100

# types min/max and blank-string checks do not apply to
NO_ORDER = {"VARIANT", "ARRAY", "OBJECT", "GEOGRAPHY", "GEOMETRY", "BINARY"}
TEXTY = {"TEXT", "VARCHAR", "STRING", "CHAR"}
NO_CAST = {"GEOGRAPHY", "GEOMETRY"}

_print_lock = threading.Lock()
_done = 0


def q(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def fetch_layout(conn):
    sql = f"""
    select c.TABLE_SCHEMA, c.TABLE_NAME, c.COLUMN_NAME, c.DATA_TYPE, c.ORDINAL_POSITION,
           t.ROW_COUNT, t.BYTES
    from {DB}.INFORMATION_SCHEMA.COLUMNS c
    join {DB}.INFORMATION_SCHEMA.TABLES t
      on t.TABLE_SCHEMA = c.TABLE_SCHEMA and t.TABLE_NAME = c.TABLE_NAME
    where t.TABLE_TYPE = 'BASE TABLE'
    order by 1, 2, 5
    """
    layout: dict[tuple[str, str], dict] = {}
    for sch, tbl, col, dtype, pos, rc, by in db.rows(conn, sql):
        e = layout.setdefault((sch, tbl), {"row_count": rc, "bytes": by, "cols": []})
        e["cols"].append((col, (dtype or "").upper()))
    return layout


def pass1_sql(sch, tbl, cols):
    sel = ["count(*)"]
    for col, dtype in cols:
        c = q(col)
        sel.append(f"count({c})")
        if dtype in NO_CAST:
            # GEOGRAPHY/GEOMETRY reject ::varchar; WKT is the text form
            sel.append(f"approx_count_distinct(st_aswkt({c}))")
        else:
            sel.append(f"approx_count_distinct({c}::varchar)")
        if dtype in NO_ORDER:
            sel.append("null")
            sel.append("null")
        else:
            sel.append(f"min({c})::varchar")
            sel.append(f"max({c})::varchar")
        if dtype in TEXTY:
            sel.append(f"count_if(trim({c}) = '')")
        else:
            sel.append("null")
    return f"select {', '.join(sel)} from {DB}.{q(sch)}.{q(tbl)}"


def topn_sql(sch, tbl, cols, sampled):
    pairs = ", ".join(f"'{c}', to_varchar({q(c)})" for c in cols)
    src = f"{DB}.{q(sch)}.{q(tbl)}"
    if sampled:
        src += f" sample ({SAMPLE_ROWS} rows)"
    return f"""
    select f.key::varchar, f.value::varchar, count(*)
    from {src},
         lateral flatten(input => object_construct_keep_null({pairs})) f
    group by 1, 2
    qualify row_number() over (partition by f.key::varchar order by count(*) desc) <= 5
    """


def profile_table(key, meta, total):
    global _done
    sch, tbl = key
    cols = meta["cols"]
    out = []
    conn = db.connect()
    try:
        vals = db.rows(conn, pass1_sql(sch, tbl, cols))[0]
        rows_n = vals[0]
        stats = {}
        for i, (col, dtype) in enumerate(cols):
            nn, dist, mn, mx, blank = vals[1 + i * 5 : 6 + i * 5]
            stats[col] = dict(
                non_null=nn, distinct=dist, min_v=mn, max_v=mx, blank=blank, dtype=dtype
            )

        low = [c for c, s in stats.items() if s["distinct"] and s["distinct"] <= TOPN_MAX_DISTINCT]
        tops: dict[str, list[str]] = {}
        sampled = bool(rows_n and rows_n > SAMPLE_OVER)
        if low and rows_n:
            for chunk in [low[i : i + 60] for i in range(0, len(low), 60)]:
                try:
                    for col, val, cnt in db.rows(conn, topn_sql(sch, tbl, chunk, sampled)):
                        tops.setdefault(col, []).append(f"{val} {cnt}")
                except Exception as exc:  # noqa: BLE001
                    tops["__err__"] = [str(exc)[:120]]

        for col, s in stats.items():
            nn = s["non_null"] or 0
            dist = s["distinct"] or 0
            out.append(
                dict(
                    schema=sch,
                    table=tbl,
                    column=col,
                    data_type=s["dtype"],
                    row_count=rows_n,
                    non_null=nn,
                    non_null_pct=round(100 * nn / rows_n, 2) if rows_n else "",
                    distinct_count=dist,
                    distinct_ratio=round(dist / rows_n, 6) if rows_n else "",
                    blank_string=s["blank"] if s["blank"] is not None else "",
                    min_value=(s["min_v"] or "")[:120],
                    max_value=(s["max_v"] or "")[:120],
                    top_5_values=" | ".join(tops.get(col, []))[:400],
                    top_5_sampled="Y" if (sampled and col in tops) else "",
                    error="",
                )
            )
    except Exception as exc:  # noqa: BLE001
        for col, dtype in cols:
            out.append(
                dict(
                    schema=sch, table=tbl, column=col, data_type=dtype, row_count="",
                    non_null="", non_null_pct="", distinct_count="", distinct_ratio="",
                    blank_string="", min_value="", max_value="", top_5_values="",
                    top_5_sampled="", error=str(exc)[:200],
                )
            )
    finally:
        conn.close()

    with _print_lock:
        _done += 1
        if _done % 25 == 0 or _done == total:
            print(f"  {_done}/{total} tables", flush=True)
    return out


FIELDS = [
    "schema", "table", "column", "data_type", "row_count", "non_null", "non_null_pct",
    "distinct_count", "distinct_ratio", "blank_string", "min_value", "max_value",
    "top_5_values", "top_5_sampled", "error",
]


def main():
    conn = db.connect()
    layout = fetch_layout(conn)
    conn.close()
    total = len(layout)
    print(f"{total} base tables, {sum(len(v['cols']) for v in layout.values())} columns")

    results = []
    with ThreadPoolExecutor(max_workers=THREADS) as ex:
        futs = [ex.submit(profile_table, k, v, total) for k, v in layout.items()]
        for f in futs:
            results.extend(f.result())

    stamp = dt.date.today().isoformat()
    path = Path(__file__).resolve().parents[1] / "reports" / f"catalog_profile_{stamp}.csv"
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(results)
    errs = sum(1 for r in results if r["error"])
    print(f"wrote {path}  rows={len(results)}  errors={errs}")


if __name__ == "__main__":
    main()
