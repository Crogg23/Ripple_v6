"""What is actually in raw for the columns the mart shows as dead?

Reads reports/dead_columns_<date>.csv, takes every MODEL_LOST_IT row, and pulls
the top raw values for that column. Then re-verdicts:

  SENTINEL_SCRUBBED  every raw value is placeholder junk. The model was right.
  MODEL_LOST_IT      raw holds real values. A real loss.
  ROW_SUBSET         mart has fewer rows than raw. Not a column problem.

Rewrites the same file with raw_top_values and a corrected verdict.
"""

from __future__ import annotations

import csv
import re
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from connect import db  # noqa: E402

THREADS = 6
SAMPLE_OVER = 2_000_000
SAMPLE_ROWS = 500_000

SENTINEL = {
    "<UNAVAIL>", "UNAVAIL", "N/A", "NA", "N.A.", "NULL", "NONE", "NAN", "UNKNOWN",
    "UNK", "NOT AVAILABLE", "NOT APPLICABLE", "NOT REPORTED", "MISSING", "TBD",
    "-", "--", "---", ".", "..", "*", "**", "?", "??", "0000-00-00", "00000000",
    "9999-12-31", "99999999", "BLANK", "EMPTY", "NO DATA", "NOT PROVIDED",
}

_lock = threading.Lock()
_done = 0


def q(n: str) -> str:
    return '"' + n.replace('"', '""') + '"'


def is_sentinel(v: str) -> bool:
    s = (v or "").strip().upper()
    if s in SENTINEL:
        return True
    if re.fullmatch(r"[-*.#?_ ]+", s):
        return True
    if re.fullmatch(r"0+", s) or re.fullmatch(r"9+", s):
        return True
    return False


def topn_sql(tbl, cols, sampled):
    pairs = ", ".join(f"'{c}', to_varchar({q(c)})" for c in cols)
    src = f"{tbl} sample ({SAMPLE_ROWS} rows)" if sampled else tbl
    return f"""
    select f.key::varchar, f.value::varchar, count(*)
    from {src}, lateral flatten(input => object_construct_keep_null({pairs})) f
    where trim(f.value::varchar) <> ''
    group by 1, 2
    qualify row_number() over (partition by f.key::varchar order by count(*) desc) <= 5
    """


def pull(tbl, cols, rows_n, total):
    global _done
    conn = db.connect()
    out: dict[str, list[tuple[str, int]]] = {}
    err = ""
    try:
        sampled = rows_n > SAMPLE_OVER
        for chunk in [cols[i : i + 50] for i in range(0, len(cols), 50)]:
            for col, val, cnt in db.rows(conn, topn_sql(tbl, chunk, sampled)):
                out.setdefault(col, []).append((val, cnt))
    except Exception as exc:  # noqa: BLE001
        err = str(exc)[:180]
    finally:
        conn.close()
        with _lock:
            _done += 1
            if _done % 10 == 0 or _done == total:
                print(f"  {_done}/{total} tables", flush=True)
    return tbl, out, err


def main():
    path = sorted((REPO / "reports").glob("dead_columns_*.csv"))[-1]
    rows = list(csv.DictReader(open(path, encoding="utf-8")))

    targets = [r for r in rows if r["verdict"] == "MODEL_LOST_IT"]
    want: dict[str, tuple[list[str], int]] = {}
    for r in targets:
        cols, n = want.setdefault(r["raw_table"], ([], int(r["raw_rows"])))
        if r["column"].upper() not in cols:
            cols.append(r["column"].upper())

    total = len(want)
    print(f"{len(targets)} columns across {total} raw tables")
    got: dict[str, dict] = {}
    errs: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=THREADS) as ex:
        for tbl, res, err in ex.map(
            lambda kv: pull(kv[0], kv[1][0], kv[1][1], total), want.items()
        ):
            got[tbl] = res
            if err:
                errs[tbl] = err

    tally: dict[str, int] = {}
    for r in rows:
        if r["verdict"] != "MODEL_LOST_IT":
            continue
        vals = got.get(r["raw_table"], {}).get(r["column"].upper(), [])
        r["raw_top_values"] = " | ".join(f"{v} {n}" for v, n in vals)[:300]
        if errs.get(r["raw_table"]):
            r["verdict"] = "value_probe_failed"
            r["error"] = errs[r["raw_table"]]
        elif int(r["mart_rows"]) != int(r["raw_rows"]):
            r["verdict"] = "ROW_SUBSET"
        elif not vals:
            r["verdict"] = "raw_also_empty"
        elif all(is_sentinel(v) for v, _ in vals):
            r["verdict"] = "SENTINEL_SCRUBBED"
        # else stays MODEL_LOST_IT

    fields = list(rows[0].keys())
    if "raw_top_values" not in fields:
        fields.insert(fields.index("verdict"), "raw_top_values")
    for r in rows:
        r.setdefault("raw_top_values", "")

    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    for r in rows:
        tally[r["verdict"]] = tally.get(r["verdict"], 0) + 1
    print(f"rewrote {path}")
    for k, v in sorted(tally.items(), key=lambda x: -x[1]):
        print(f"  {v:6}  {k}")


if __name__ == "__main__":
    main()
