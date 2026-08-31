"""The entity spine — the persisted "who's who" of the Library.

v1 resolves on HARD IDs only, which is zero-false-merge by construction: the same
NPI (or CCN / EIN / ...) value across N source tables is, definitionally, one
real-world entity. We do NOT fuse different ID *types* into one entity here —
a provider's NPI and a facility's CCN are linked by a *relationship* (works-at),
not an *identity*, and the only public crosswalk we have (NPI<->CCN facility
affiliation) is exactly that relationship; fusing them would merge a doctor with a
hospital. True cross-ID-type identity (a person across sources with no shared ID)
is the fuzzy frontier handled — gated — in resolve.py (Phase 5).

So clustering here is just GROUP BY (key_type, key_value). Each distinct hard-ID
value is an entity; member_tables records every source that carries it; the golden
record picks a canonical name/address from the most authoritative source.

Writes to LIBRARY_META.CONNECT (all CREATE OR REPLACE -> a rebuild is idempotent;
ENTITY_ID is content-addressed so a rebuild renumbers no one):
    CONNECT_NODES   one row per (hard key value, source table)
    MATCH_PAIRS     the same value seen in two tables (the pairs discover discards)
    ENTITY_MAP      one row per entity: id, key, member tables, source count
    ENTITY_GOLDEN   one row per entity: canonical name + address

    python -m connect spine
"""

from __future__ import annotations

import uuid

from . import db, store
from .entity_index_specs import DISPLAY_SPECS, entity_type_sql, table_keys
from .keys import normalize_sql, quote_ident

KEYSET_FQN = store.cfqn("SPINE_KEYSET")   # transient working set
NODES_FQN = store.cfqn("CONNECT_NODES")
PAIRS_FQN = store.cfqn("MATCH_PAIRS")
EMAP_FQN = store.cfqn("ENTITY_MAP")
GOLD_FQN = store.cfqn("ENTITY_GOLDEN")
LEADS_FQN = store.cfqn("LEADS")

# entity type from the hard key (references the GROUP BY column `key_type`).
# Generated from entity_index_specs.ENTITY_TYPE_BY_KEY -- the ONE source of truth.
# This used to be a hand-written CASE string duplicated in incremental.py and two
# dicts elsewhere, with a comment in each asking the next person to keep all four in
# lockstep. Generating it removes the drift risk entirely.
_ENTITY_TYPE_SQL = entity_type_sql("key_type")


def _name_expr(spec: dict) -> str:
    """Canonical-name expression: prefer org/facility name, else 'LAST, FIRST'."""
    parts = []
    if spec.get("org"):
        # 2026-08-24: the portal crawls were written through pandas, so a missing
        # name lands as the literal string 'nan' (7/83 rows on the DC NPDES tables,
        # 19/1,392 on a Utah clinic table). Treat it as no name, never as a name.
        parts.append(f"NULLIF(NULLIF(TRIM({quote_ident(spec['org'])}), ''), 'nan')")
    if spec.get("person"):
        last, first = spec["person"]
        parts.append(f"NULLIF(TRIM({quote_ident(last)}) || ', ' || TRIM({quote_ident(first)}), ', ')")
    if not parts:
        return "CAST(NULL AS STRING)"
    return parts[0] if len(parts) == 1 else f"COALESCE({', '.join(parts)})"


def _addr_expr(spec: dict) -> str:
    bits = [f"TRIM(COALESCE({quote_ident(spec[k])}, ''))" for k in ("city", "state", "zip") if spec.get(k)]
    if not bits:
        return "CAST(NULL AS STRING)"
    joined = " || ' ' || ".join(bits)
    return f"NULLIF(TRIM({joined}), '')"


def _build_hard_keyset(conn) -> int:
    """Materialize DISTINCT normalized hard-key values per source into a transient
    working table. One INSERT per (table, key) pair -- almost always one per spec'd
    table, except a table with extra_keys (e.g. FED_VOTEVIEW_MEMBERS: ICPSR +
    BIOGUIDE) gets one INSERT per key. NPPES (~9.6M rows) is the big single one."""
    db.rows(conn, f"CREATE OR REPLACE TRANSIENT TABLE {KEYSET_FQN} "
                  f"(table_name STRING, key_type STRING, val STRING)")
    n = 0
    for tbl, spec in DISPLAY_SPECS.items():
        for key, key_col in table_keys(spec):
            norm = normalize_sql(key, quote_ident(key_col))
            db.rows(conn, f"INSERT INTO {KEYSET_FQN} "
                          f"SELECT DISTINCT '{tbl}', '{key}', {norm} "
                          f"FROM {db.fqn(tbl)} WHERE {norm} IS NOT NULL")
            n += 1
    return n


def _build_nodes(conn, run_id: str) -> None:
    db.rows(conn, f"""
        CREATE OR REPLACE TABLE {NODES_FQN} AS
        SELECT MD5(key_type || '|' || val) AS NODE_ID, key_type AS KEY_TYPE,
               val AS KEY_VALUE, table_name AS TABLE_NAME,
               '{run_id}' AS RUN_ID, CURRENT_TIMESTAMP() AS BUILT_AT
        FROM {KEYSET_FQN}""")


def _build_pairs(conn, run_id: str) -> None:
    """The cross-source pairs discover.py computes then throws away: same hard-ID
    value in two different tables. Bounded (only values that appear in 2+ tables)."""
    db.rows(conn, f"""
        CREATE OR REPLACE TABLE {PAIRS_FQN} AS
        SELECT a.key_type AS KEY_TYPE, a.val AS KEY_VALUE,
               a.table_name AS TABLE_A, b.table_name AS TABLE_B,
               '{run_id}' AS RUN_ID, CURRENT_TIMESTAMP() AS BUILT_AT
        FROM {KEYSET_FQN} a
        JOIN {KEYSET_FQN} b
          ON a.key_type = b.key_type AND a.val = b.val AND a.table_name < b.table_name""")


def _build_entity_map(conn, run_id: str) -> None:
    db.rows(conn, f"""
        CREATE OR REPLACE TABLE {EMAP_FQN} AS
        SELECT 'ENT_' || LEFT(MD5(key_type || '|' || val), 16) AS ENTITY_ID,
               key_type AS KEY_TYPE, val AS KEY_VALUE,
               {_ENTITY_TYPE_SQL} AS ENTITY_TYPE,
               ARRAY_AGG(DISTINCT table_name) WITHIN GROUP (ORDER BY table_name) AS MEMBER_TABLES,
               COUNT(DISTINCT table_name) AS SOURCE_COUNT,
               '{run_id}' AS RUN_ID, CURRENT_TIMESTAMP() AS BUILT_AT
        FROM {KEYSET_FQN}
        GROUP BY key_type, val""")


def _build_golden(conn, run_id: str) -> None:
    """Survivorship: per entity, take name+address from the lowest-authority-rank
    (= most authoritative) source that actually has a name; tie-break by longest,
    then by SRC (alphabetical table name) so a genuine tie -- e.g. the same NPI
    reported with an identical-length name in two same-authority annual snapshots
    like FED_CMS_OPEN_PAYMENTS_2022 vs _2023 -- resolves the SAME way every run,
    not by incidental scan order. incremental.py's _merge_golden and validate()
    use the IDENTICAL ORDER BY; keep all three in lockstep."""
    attrs = " UNION ALL ".join(
        f"SELECT '{key}' AS KEY_TYPE, "
        f"{normalize_sql(key, quote_ident(key_col))} AS KEY_VALUE, "
        f"{_name_expr(spec)} AS NAME, {_addr_expr(spec)} AS ADDR, "
        f"{spec['authority']} AS AUTH, '{tbl}' AS SRC "
        f"FROM {db.fqn(tbl)} "
        f"WHERE {normalize_sql(key, quote_ident(key_col))} IS NOT NULL"
        for tbl, spec in DISPLAY_SPECS.items()
        for key, key_col in table_keys(spec))
    db.rows(conn, f"""
        CREATE OR REPLACE TABLE {GOLD_FQN} AS
        WITH attrs AS ( {attrs} ),
        ranked AS (
          SELECT e.ENTITY_ID, e.ENTITY_TYPE, a.KEY_TYPE, a.KEY_VALUE, a.NAME, a.ADDR, a.SRC,
                 ROW_NUMBER() OVER (PARTITION BY a.KEY_TYPE, a.KEY_VALUE
                     ORDER BY IFF(a.NAME IS NULL, 1, 0), a.AUTH, LENGTH(a.NAME) DESC NULLS LAST, a.SRC) AS RN
          FROM attrs a
          JOIN {EMAP_FQN} e ON e.KEY_TYPE = a.KEY_TYPE AND e.KEY_VALUE = a.KEY_VALUE )
        SELECT ENTITY_ID, ENTITY_TYPE, KEY_TYPE, KEY_VALUE,
               NAME AS CANONICAL_NAME,
               {normalize_sql('NAME', 'NAME')} AS NAME_NORM,
               ADDR AS CANONICAL_ADDR, SRC AS NAME_SOURCE,
               '{run_id}' AS RUN_ID, CURRENT_TIMESTAMP() AS BUILT_AT
        FROM ranked WHERE RN = 1""")


def _backfill_leads(conn) -> int:
    """Stamp LEADS.LEFT_ENTITY_ID from the spine (if the LEADS table exists)."""
    exists = db.scalar(conn,
        f"SELECT COUNT(*) FROM {store.CONNECT_DB}.INFORMATION_SCHEMA.TABLES "
        f"WHERE TABLE_SCHEMA = '{store.CONNECT_SCHEMA}' AND TABLE_NAME = 'LEADS'")
    if not exists:
        return 0
    db.rows(conn, f"""
        UPDATE {LEADS_FQN} t SET LEFT_ENTITY_ID = e.ENTITY_ID
        FROM {EMAP_FQN} e
        WHERE e.KEY_TYPE = t.LEFT_KEY_TYPE AND e.KEY_VALUE = t.LEFT_KEY_VALUE""")
    return int(db.scalar(conn, f"SELECT COUNT(*) FROM {LEADS_FQN} WHERE LEFT_ENTITY_ID IS NOT NULL") or 0)


def _summarize(conn) -> dict:
    by_type = {r["ENTITY_TYPE"]: int(r["N"]) for r in db.dicts(
        conn, f"SELECT ENTITY_TYPE, COUNT(*) N FROM {EMAP_FQN} GROUP BY 1 ORDER BY 2 DESC")}
    return {
        "nodes": int(db.scalar(conn, f"SELECT COUNT(*) FROM {NODES_FQN}") or 0),
        "entities": int(db.scalar(conn, f"SELECT COUNT(*) FROM {EMAP_FQN}") or 0),
        "multi_source": int(db.scalar(conn, f"SELECT COUNT(*) FROM {EMAP_FQN} WHERE SOURCE_COUNT >= 2") or 0),
        "golden": int(db.scalar(conn, f"SELECT COUNT(*) FROM {GOLD_FQN}") or 0),
        "by_type": by_type,
    }


def run(write: bool = True) -> dict:
    run_id = uuid.uuid4().hex[:16]
    conn = db.connect()
    try:
        store.ensure_schema(conn)
        print(f"spine: building hard-key set over {len(DISPLAY_SPECS)} sources …")
        _build_hard_keyset(conn)
        _build_nodes(conn, run_id)
        _build_pairs(conn, run_id)
        _build_entity_map(conn, run_id)
        _build_golden(conn, run_id)
        from . import entity_index
        idx_rows = entity_index.build(conn, run_id)
        backfilled = _backfill_leads(conn)
        stats = _summarize(conn)
        # Keep the incremental state coherent with this full rebuild: refresh the
        # persisted keyset twins + re-pin every table's content-key. Fail-safe — a
        # problem here must never break the backstop rebuild itself.
        try:
            from .incremental import sync_after_rebuild
            sync_after_rebuild(conn, reseed=True)
            print("  synced incremental state (SPINE_KEYSET_LIVE + CONNECT_WATERMARK)")
        except Exception as ex:
            print(f"  [warn] incremental state sync skipped: {str(ex)[:120]}")
    finally:
        conn.close()
    tier = ", ".join(f"{k}={v:,}" for k, v in stats["by_type"].items())
    print(f"spine: {stats['entities']:,} entities ({stats['multi_source']:,} multi-source) "
          f"from {stats['nodes']:,} nodes; {stats['golden']:,} golden records; by type: {tier}")
    print(f"  entity index: {idx_rows:,} (entity, source) rows")
    if backfilled:
        print(f"  backfilled LEFT_ENTITY_ID on {backfilled} leads")
    return stats


if __name__ == "__main__":
    run()
