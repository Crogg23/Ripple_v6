"""Why is a mart column dead? Ask the raw table it came from.

Dead means 100% null, or >99% empty string, in reports/catalog_profile_*.csv.
For each dead mart column we find the same-named column in the raw landing
table dbt says the mart descends from, and count it there.

  raw also empty   -> the source never published it. Correctly dead.
  raw has values   -> the model or the cast lost it. A real bug.
  no raw column    -> the mart derived it. Needs a look at the SQL.

Writes reports/dead_columns_<date>.csv.
"""

from __future__ import annotations

import csv
import datetime as dt
import json
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from connect import db  # noqa: E402

MANIFEST = REPO / "library-onboarding" / "ripple_dbt" / "target" / "manifest.json"
THREADS = 6
TEXTY = {"TEXT", "VARCHAR", "STRING", "CHAR"}

_lock = threading.Lock()
_done = 0


def q(n: str) -> str:
    return '"' + n.replace('"', '""') + '"'


def mart_to_raw() -> dict[tuple[str, str], str]:
    """One raw table per mart table, or nothing when it is not a clean single."""
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    nodes, sources, parent = m["nodes"], m["sources"], m["parent_map"]

    def walk(uid, seen):
        if uid in seen:
            return set()
        seen.add(uid)
        out = set()
        for p in parent.get(uid, []):
            if p.startswith("source."):
                s = sources[p]
                out.add(f"{s['database']}.{s['schema']}.{s['identifier']}")
            else:
                out |= walk(p, seen)
        return out

    out = {}
    for uid, n in nodes.items():
        if n.get("resource_type") != "model":
            continue
        if n.get("config", {}).get("materialized") != "table":
            continue
        if (n.get("database") or "").upper() != "LIBRARY_MARTS":
            continue
        raws = sorted(walk(uid, set()))
        raws = [r for r in raws if r.startswith("LIBRARY_RAW.")]
        if len(raws) == 1:
            out[(n["schema"].upper(), n.get("alias", n["name"]).upper())] = raws[0]
    return out


def raw_layout(conn) -> dict[str, dict[str, str]]:
    sql = """
    select TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, DATA_TYPE
    from LIBRARY_RAW.INFORMATION_SCHEMA.COLUMNS
    """
    out: dict[str, dict[str, str]] = {}
    for sch, tbl, col, dtype in db.rows(conn, sql):
        out.setdefault(f"LIBRARY_RAW.{sch}.{tbl}", {})[col.upper()] = (dtype or "").upper()
    return out


def load_dead(profile: Path):
    """Dead mart columns, with the reason they read as dead."""
    dead = []
    for r in csv.DictReader(open(profile, encoding="utf-8")):
        rc = int(r["row_count"]) if r["row_count"] else 0
        if not rc:
            continue
        nn = float(r["non_null_pct"]) if r["non_null_pct"] else 0.0
        bl = int(r["blank_string"]) if r["blank_string"] else 0
        if nn == 0.0:
            dead.append((r, "all_null"))
        elif bl and bl / rc > 0.99:
            dead.append((r, "all_blank_string"))
    return dead


def probe(raw_tbl, cols, total):
    """One query: non-null and non-blank counts for these raw columns."""
    global _done
    sel = ["count(*)"]
    for col, dtype in cols:
        c = q(col)
        sel.append(f"count({c})")
        sel.append(f"count_if(trim({c}) <> '')" if dtype in TEXTY else f"count({c})")
    sql = f"select {', '.join(sel)} from {raw_tbl}"
    conn = db.connect()
    try:
        v = db.rows(conn, sql)[0]
        res = {}
        for i, (col, _) in enumerate(cols):
            res[col] = (v[0], v[1 + i * 2], v[2 + i * 2])
        return raw_tbl, res, ""
    except Exception as exc:  # noqa: BLE001
        return raw_tbl, {}, str(exc)[:180]
    finally:
        conn.close()
        with _lock:
            _done += 1
            if _done % 20 == 0 or _done == total:
                print(f"  {_done}/{total} raw tables", flush=True)


FIELDS = [
    "schema", "mart_table", "column", "data_type", "mart_rows", "dead_reason",
    "raw_table", "raw_column_exists", "raw_rows", "raw_non_null", "raw_non_blank",
    "verdict", "error",
]


def main():
    profile = sorted((REPO / "reports").glob("catalog_profile_*.csv"))[-1]
    dead = load_dead(profile)
    print(f"{len(dead)} dead mart columns from {profile.name}")

    m2r = mart_to_raw()
    conn = db.connect()
    rawcols = raw_layout(conn)
    conn.close()

    # group the raw lookups: one query per raw table
    want: dict[str, list[tuple[str, str]]] = {}
    rows = []
    for r, reason in dead:
        key = (r["schema"].upper(), r["table"].upper())
        raw = m2r.get(key)
        col = r["column"].upper()
        rec = dict(
            schema=r["schema"], mart_table=r["table"], column=r["column"],
            data_type=r["data_type"], mart_rows=r["row_count"], dead_reason=reason,
            raw_table=raw or "", raw_column_exists="", raw_rows="", raw_non_null="",
            raw_non_blank="", verdict="", error="",
        )
        if not raw:
            rec["verdict"] = "no_single_raw_parent"
        elif col not in rawcols.get(raw, {}):
            rec["raw_column_exists"] = "N"
            rec["verdict"] = "derived_in_model"
        else:
            rec["raw_column_exists"] = "Y"
            want.setdefault(raw, [])
            if (col, rawcols[raw][col]) not in want[raw]:
                want[raw].append((col, rawcols[raw][col]))
        rows.append(rec)

    total = len(want)
    print(f"{total} raw tables to probe")
    results = {}
    errs = {}
    with ThreadPoolExecutor(max_workers=THREADS) as ex:
        for raw, res, err in ex.map(lambda kv: probe(kv[0], kv[1], total), want.items()):
            results[raw] = res
            if err:
                errs[raw] = err

    for rec in rows:
        if rec["raw_column_exists"] != "Y":
            continue
        raw = rec["raw_table"]
        if raw in errs:
            rec["error"] = errs[raw]
            rec["verdict"] = "probe_failed"
            continue
        rr, nn, nb = results[raw].get(rec["column"].upper(), (None, None, None))
        rec["raw_rows"], rec["raw_non_null"], rec["raw_non_blank"] = rr, nn, nb
        if not rr:
            rec["verdict"] = "raw_table_empty"
        elif (nb or 0) == 0:
            rec["verdict"] = "raw_also_empty"
        else:
            rec["verdict"] = "MODEL_LOST_IT"

    stamp = dt.date.today().isoformat()
    path = REPO / "reports" / f"dead_columns_{stamp}.csv"
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    tally: dict[str, int] = {}
    for r in rows:
        tally[r["verdict"]] = tally.get(r["verdict"], 0) + 1
    print(f"wrote {path}")
    for k, v in sorted(tally.items(), key=lambda x: -x[1]):
        print(f"  {v:6}  {k}")


if __name__ == "__main__":
    main()
