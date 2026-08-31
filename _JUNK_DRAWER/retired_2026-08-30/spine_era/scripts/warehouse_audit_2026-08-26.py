"""Full warehouse audit, 2026-08-26 — a fresh run of the same methodology as
reports/the_audit_2026-08-24/, re-verified live against the current warehouse
(post entity-graph rebuild + merge). Reuses the platform's own key-detection
and normalization code (connect/keys.py, connect/spine_entity.py,
connect/entity_index_specs.py) rather than a second competing heuristic.

Phases:
  A. Live inventory (databases pulled live from SHOW DATABASES, never a
     hardcoded list) — tables + columns, name-zone tagging (a naming-convention
     GROUPING, not a liveness verdict — see schema_zone()).
  B. Live row counts on every BASE TABLE (threaded). Views are NOT counted
     (cost); the summary marks them uncounted instead of summing them as zero.
  C. Entity-grade key detection per table (pure Python, the platform's own
     tagger) + spine-wired cross-check against DISPLAY_SPECS.
  D. Distinct-value + 5-sample verification for every detected entity-grade
     key column (threaded) — the count+COUNT(DISTINCT)+sample discipline the
     constitution requires, never a bare null check.
  E. Entity-graph headline numbers — pulled live from the platform's own
     LIBRARY_META.CONNECT tables (not re-derived; that's already the live
     source of truth).
  F. Known-trap cross-check — round-number loader-cap signature on row
     counts, cross-referenced against honesty/traps.py's registry.

Writes CSVs to reports/the_audit_2026-08-26/. No DDL/DML — read-only.
"""
import csv
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)
sys.path.insert(0, os.path.join(REPO, "connect"))
sys.path.insert(0, os.path.join(REPO, "honesty"))

from scripts._snowflake_conn import connect  # noqa: E402
from keys import detect_key, normalize_sql, quote_ident  # noqa: E402
from spine_entity import candidate_keys_for_columns, SPINE_ENTITY_BY_KEY  # noqa: E402
from entity_index_specs import DISPLAY_SPECS, table_keys  # noqa: E402
from traps import traps_for_source  # noqa: E402

OUT = os.path.join(REPO, "reports", "the_audit_2026-08-26")
os.makedirs(OUT, exist_ok=True)

# FIXED 2026-08-26: the database list is now pulled live from SHOW DATABASES
# (excluding Snowflake system/user scratch DBs) instead of hardcoded -- the exact
# hardcoded-inventory failure this platform has hit twice (a 5-of-7-DB sweep the
# same day this script was written). See real_dbs().
EXCLUDE_DBS = {"SNOWFLAKE"}


def real_dbs(cur):
    cur.execute("SHOW DATABASES")
    names = [r[1] for r in cur.fetchall()]
    return [n for n in names if n not in EXCLUDE_DBS and not n.startswith("USER$")]

ROUND_CAPS = {500, 1000, 2000, 5000, 10000, 20000, 25000, 50000, 100000,
              1000000, 20000000}

WIRED_TABLE_NAMES = set(DISPLAY_SPECS.keys())


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def schema_zone(db, schema):
    """A NAME-PATTERN GUESS, not a measurement. Renamed from schema_status
    2026-08-26 after its labels were mistaken for findings: it had stamped
    THE_LIBRARY "legacy_dead" (it is the live reading-room layer and the repo
    SQL runner's default database) and REVIEW "junk_schema" (it is the human
    sign-off machinery CLAUDE.md makes non-negotiable). Nothing here is
    evidence of liveness or deadness -- it only groups schemas by naming
    convention so a reader can sort the summary. Liveness claims require a
    live check plus a reference grep, per the constitution.
    """
    s = schema.upper()
    if s.startswith("_RESTORE_") or s.startswith("CONNECT_BAK_") or s.startswith("CONNECT_PRESPINE_"):
        return "name_suggests_backup"
    if s in ("REVIEW", "UNCATEGORIZED"):
        return "name_suggests_holding_area"
    if db == "LIBRARY_MARTS_PREDBT_20260729":
        return "name_suggests_premigration"
    if db == "THE_LIBRARY":
        return "presentation_layer"
    return "unlabeled"


def bare_table_name(db, schema, table):
    """The name the spine actually reads: bare LIBRARY_RAW.LANDING table name,
    or the source table a mart mirrors (dropped when unclear)."""
    if db == "LIBRARY_RAW":
        return table
    return None


# ---------------------------------------------------------------------------
# Phase A — live inventory
# ---------------------------------------------------------------------------
def phase_a():
    conn = connect()
    cur = conn.cursor()
    dbs = real_dbs(cur)
    log(f"Phase A: live inventory across {len(dbs)} databases (from SHOW DATABASES): "
        + ", ".join(dbs))
    tables = []
    columns = []
    for db in dbs:
        t0 = time.time()
        cur.execute(f"""
            select '{db}' as db, table_schema, table_name, table_type,
                   row_count, bytes, created, last_altered
            from {db}.information_schema.tables
            where table_schema not in ('INFORMATION_SCHEMA')
            order by table_schema, table_name
        """)
        rows = cur.fetchall()
        for r in rows:
            tables.append({
                "db": r[0], "schema": r[1], "table": r[2], "type": r[3],
                "row_count_meta": r[4], "bytes": r[5],
                "created": r[6], "last_altered": r[7],
                "name_zone": schema_zone(db, r[1]),
            })
        cur.execute(f"""
            select '{db}' as db, table_schema, table_name, column_name,
                   ordinal_position, data_type
            from {db}.information_schema.columns
            where table_schema not in ('INFORMATION_SCHEMA')
            order by table_schema, table_name, ordinal_position
        """)
        for r in cur.fetchall():
            columns.append({
                "db": r[0], "schema": r[1], "table": r[2], "column": r[3],
                "ordinal": r[4], "data_type": r[5],
            })
        log(f"  {db}: {len([x for x in tables if x['db']==db])} tables, "
            f"{len([x for x in columns if x['db']==db])} columns "
            f"({time.time()-t0:.1f}s)")
    conn.close()
    return tables, columns


# ---------------------------------------------------------------------------
# Phase B — live row counts (threaded)
# ---------------------------------------------------------------------------
_thread_conn = {}


def _get_conn():
    import threading
    tid = threading.get_ident()
    if tid not in _thread_conn:
        _thread_conn[tid] = connect()
    return _thread_conn[tid]


def _count_one(db, schema, table):
    conn = _get_conn()
    cur = conn.cursor()
    fq = f'{db}."{schema}"."{table}"'
    try:
        cur.execute(f"SELECT COUNT(*) FROM {fq}")
        return (db, schema, table, cur.fetchone()[0], None)
    except Exception as e:
        return (db, schema, table, None, str(e)[:200])


def phase_b(tables):
    base_tables = [t for t in tables if t["type"] == "BASE TABLE"]
    log(f"Phase B: live COUNT(*) on {len(base_tables)} base tables (12 workers)...")
    results = {}
    t0 = time.time()
    done = 0
    with ThreadPoolExecutor(max_workers=12) as ex:
        futs = {ex.submit(_count_one, t["db"], t["schema"], t["table"]): t for t in base_tables}
        for fut in as_completed(futs):
            db, schema, table, n, err = fut.result()
            results[(db, schema, table)] = (n, err)
            done += 1
            if done % 500 == 0:
                log(f"  ...{done}/{len(base_tables)} counted ({time.time()-t0:.0f}s elapsed)")
    log(f"Phase B done: {done} tables in {time.time()-t0:.0f}s")
    for t in tables:
        key = (t["db"], t["schema"], t["table"])
        if key in results:
            t["row_count_live"], t["count_error"] = results[key]
        else:
            t["row_count_live"], t["count_error"] = None, None
    return tables


# ---------------------------------------------------------------------------
# Phase C — entity-grade key detection + spine-wired cross-check
# ---------------------------------------------------------------------------
def phase_c(tables, columns):
    log("Phase C: entity-grade key detection...")
    cols_by_table = {}
    for c in columns:
        cols_by_table.setdefault((c["db"], c["schema"], c["table"]), []).append(c["column"])

    key_instances = []
    for t in tables:
        if t["type"] != "BASE TABLE":
            continue
        key = (t["db"], t["schema"], t["table"])
        col_names = cols_by_table.get(key, [])
        hits = candidate_keys_for_columns(col_names)
        entity_hits = [h for h in hits if h[2] != "place"]
        t["entity_key_count"] = len(entity_hits)
        t["place_key_count"] = len(hits) - len(entity_hits)
        bare = bare_table_name(t["db"], t["schema"], t["table"])
        t["spine_wired"] = bool(bare and bare in WIRED_TABLE_NAMES)
        for col, klabel, sentity in entity_hits:
            key_instances.append({
                "db": t["db"], "schema": t["schema"], "table": t["table"],
                "column": col, "key": klabel, "spine_entity": sentity,
                "spine_wired": t["spine_wired"],
            })
    log(f"Phase C done: {len(key_instances)} entity-grade key-column instances "
        f"across {len({(k['db'],k['schema'],k['table']) for k in key_instances})} tables")
    return key_instances


# ---------------------------------------------------------------------------
# Phase D — distinct + sample verification (threaded)
# ---------------------------------------------------------------------------
def _verify_one(inst):
    conn = _get_conn()
    cur = conn.cursor()
    fq = f'{inst["db"]}."{inst["schema"]}"."{inst["table"]}"'
    qcol = quote_ident(inst["column"])
    try:
        expr = normalize_sql(inst["key"], qcol)
    except KeyError as e:
        return {**inst, "n_total": None, "n_distinct": None, "sample": "",
                "error": f"no_norm_rule: {e}"}
    try:
        cur.execute(f"SELECT COUNT(*), COUNT(DISTINCT {expr}) FROM {fq}")
        n_total, n_distinct = cur.fetchone()
        sample = []
        if n_distinct and n_distinct > 0:
            cur.execute(f"SELECT DISTINCT {expr} AS v FROM {fq} WHERE {expr} IS NOT NULL LIMIT 5")
            sample = [str(r[0]) for r in cur.fetchall()]
        return {**inst, "n_total": n_total, "n_distinct": n_distinct,
                "sample": "|".join(sample), "error": None}
    except Exception as e:
        return {**inst, "n_total": None, "n_distinct": None, "sample": "",
                "error": str(e)[:200]}


def phase_d(key_instances):
    log(f"Phase D: distinct+sample verification on {len(key_instances)} key columns (12 workers)...")
    t0 = time.time()
    verified = []
    done = 0
    with ThreadPoolExecutor(max_workers=12) as ex:
        futs = {ex.submit(_verify_one, inst): inst for inst in key_instances}
        for fut in as_completed(futs):
            verified.append(fut.result())
            done += 1
            if done % 200 == 0:
                log(f"  ...{done}/{len(key_instances)} verified ({time.time()-t0:.0f}s elapsed)")
    log(f"Phase D done: {done} in {time.time()-t0:.0f}s")
    return verified


# ---------------------------------------------------------------------------
# Phase E — entity-graph headline numbers (live, reused from the platform's
# own tables — NOT re-derived, per house rule: check for existing work first)
# ---------------------------------------------------------------------------
def phase_e():
    log("Phase E: entity-graph headline numbers (live CONNECT tables)...")
    conn = connect()
    cur = conn.cursor()
    graph_tables = [
        ("LIBRARY_META", "CONNECT", "ENTITY_MAP"),
        ("LIBRARY_META", "CONNECT", "ENTITY_INDEX"),
        ("LIBRARY_META", "CONNECT", "MATCH_PAIRS"),
        ("LIBRARY_META", "CONNECT", "KEYSET_LIVE"),
        ("LIBRARY_META", "CONNECT", "CONNECT_EDGES"),
        ("LIBRARY_META", "CONNECT", "LEADS"),
    ]
    rows = []
    for db, schema, table in graph_tables:
        try:
            cur.execute(f'SELECT COUNT(*) FROM {db}."{schema}"."{table}"')
            n = cur.fetchone()[0]
            rows.append({"table": f"{db}.{schema}.{table}", "live_rows": n, "error": None})
            log(f"  {table}: {n:,}")
        except Exception as e:
            rows.append({"table": f"{db}.{schema}.{table}", "live_rows": None, "error": str(e)[:200]})
            log(f"  {table}: ERROR {str(e)[:100]}")
    try:
        # "CONNECT" is a reserved word in Snowflake -- unquoted it produced a
        # syntax error and this breakdown silently failed in the 08-26 run.
        cur.execute('SELECT TIER, COUNT(*) FROM LIBRARY_META."CONNECT".CONNECT_EDGES GROUP BY TIER ORDER BY 2 DESC')
        for tier, n in cur.fetchall():
            log(f"    edge tier {tier}: {n:,}")
    except Exception as e:
        log(f"  CONNECT_EDGES tier breakdown failed: {str(e)[:150]}")
    conn.close()
    return rows


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    t0 = time.time()
    tables, columns = phase_a()
    tables = phase_b(tables)
    key_instances = phase_c(tables, columns)
    verified = phase_d(key_instances)
    graph_rows = phase_e()

    # Round-cap trap flag + known-trap registry cross-check
    for t in tables:
        rc = t.get("row_count_live")
        t["round_cap_flag"] = bool(rc in ROUND_CAPS)
        traps = traps_for_source(t["table"]) if t["db"] == "LIBRARY_RAW" else ()
        t["known_traps"] = "|".join(traps)

    # Write outputs
    with open(os.path.join(OUT, "tables.csv"), "w", newline="", encoding="utf-8") as fh:
        cols = ["db", "schema", "table", "type", "name_zone", "row_count_meta",
                "row_count_live", "count_error", "round_cap_flag", "known_traps",
                "bytes", "entity_key_count", "place_key_count", "spine_wired",
                "created", "last_altered"]
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(tables)

    with open(os.path.join(OUT, "columns.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["db", "schema", "table", "column", "ordinal", "data_type"])
        w.writeheader()
        w.writerows(columns)

    with open(os.path.join(OUT, "key_columns_verified.csv"), "w", newline="", encoding="utf-8") as fh:
        cols = ["db", "schema", "table", "column", "key", "spine_entity",
                "spine_wired", "n_total", "n_distinct", "sample", "error"]
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(verified)

    with open(os.path.join(OUT, "entity_graph_live.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["table", "live_rows", "error"])
        w.writeheader()
        w.writerows(graph_rows)

    # scale summary by schema.
    # FIXED 2026-08-26: views are never COUNT(*)'d (cost), and the old summary
    # silently summed their missing counts as 0 -- which made every view-only
    # schema print as "0 rows, 0 bytes" and read as measured-empty. THE_LIBRARY
    # (254 views serving 100M+ rows) nearly got a DROP DATABASE off that line.
    # The summary now carries how many objects were counted vs skipped, and a
    # rows_live of "" (not 0) when nothing in the schema was measured.
    from collections import defaultdict
    agg = defaultdict(lambda: {"tables": 0, "counted": 0, "views_uncounted": 0,
                               "rows_live": 0, "bytes": 0})
    for t in tables:
        k = (t["db"], t["schema"], t["name_zone"])
        a = agg[k]
        a["tables"] += 1
        if t["row_count_live"] is not None:
            a["counted"] += 1
            a["rows_live"] += t["row_count_live"]
        else:
            a["views_uncounted"] += 1
        if t["bytes"]:
            a["bytes"] += t["bytes"]
    with open(os.path.join(OUT, "scale_summary_by_schema.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["db", "schema", "name_zone", "objects", "counted_tables",
                    "uncounted_views", "rows_live_counted_tables_only", "bytes"])
        for (db, schema, zone), v in sorted(agg.items()):
            rows_cell = v["rows_live"] if v["counted"] else "NOT_MEASURED"
            w.writerow([db, schema, zone, v["tables"], v["counted"],
                        v["views_uncounted"], rows_cell, v["bytes"]])

    log(f"ALL DONE in {time.time()-t0:.0f}s. Outputs in {OUT}")
    log(f"Totals: {len(tables)} tables/views, {len(columns)} columns, "
        f"{len(key_instances)} key instances, {len(verified)} verified")


if __name__ == "__main__":
    main()
