"""Fingerprint every landed table: which join keys does it carry, and are they
ACTUALLY populated?

The portal index tags datasets by key *type* from column names alone. That's
what burned us today — a column literally named NPI that's 100% empty, a CCN
that's numeric noise. Fingerprinting adds the missing half: it goes to the data
and measures population (non-null %, distinct count) for every key column, so a
dead key never poses as a live connection.

Output: outputs/connect_fingerprints.json
  { "<TABLE>": {
      "rows": int,
      "keys": [ {column, key, tier, mode, nonnull, distinct, populated_pct} ... ]
  } }
"""

from __future__ import annotations

import json
from pathlib import Path

from . import db
from .keys import detect_key, join_mode, normalize_sql, quote_ident

OUT = Path(__file__).resolve().parents[1] / "outputs" / "connect_fingerprints.json"

# Tables that aren't real joinable sources (early proofs / archive captures / demos).
SKIP_TABLES = {"INTL_DEMO_QUOTES_TOSCRAPE_JS"}

MAX_KEY_COLS_PER_TABLE = 16  # guard against a runaway aggregate query


def landed_tables(conn) -> list[str]:
    """Return non-portal tables + portal tables that carry a STEEL/STRONG entity key.

    Portal tables are only included if their columns match at least one hard entity
    key (EIN/NPI/UEI/CIK/etc.) -- the connectable-first gate. This keeps NAME/ZIP-only
    city scrapes out while activating portals that can actually link to the spine.
    """
    from .keys import ENTITY_KEYS, detect_key

    # Core tables (non-portal) -- always included
    sql = f"""
        SELECT TABLE_NAME
        FROM {db.RAW_DB}.INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = '{db.RAW_SCHEMA}' AND TABLE_TYPE = 'BASE TABLE'
              AND TABLE_NAME NOT LIKE 'PORTAL_%%'
        ORDER BY TABLE_NAME
    """
    core = [r[0] for r in db.rows(conn, sql) if r[0] not in SKIP_TABLES]

    # Portal tables -- only those with at least one STEEL/STRONG entity key column
    portal_sql = f"""
        SELECT t.TABLE_NAME, c.COLUMN_NAME
        FROM {db.RAW_DB}.INFORMATION_SCHEMA.TABLES t
        JOIN {db.RAW_DB}.INFORMATION_SCHEMA.COLUMNS c
            ON c.TABLE_SCHEMA = t.TABLE_SCHEMA AND c.TABLE_NAME = t.TABLE_NAME
        WHERE t.TABLE_SCHEMA = '{db.RAW_SCHEMA}' AND t.TABLE_TYPE = 'BASE TABLE'
              AND t.TABLE_NAME LIKE 'PORTAL_%%'
        ORDER BY t.TABLE_NAME
    """
    portal_rows = db.rows(conn, portal_sql)
    from collections import defaultdict
    table_cols = defaultdict(list)
    for tbl, col in portal_rows:
        if tbl not in SKIP_TABLES:
            table_cols[tbl].append(col)

    entity_key_set = set(ENTITY_KEYS)
    connectable_portals = []
    for tbl, cols in table_cols.items():
        for col in cols:
            key, _tier = detect_key(col)
            if key and key in entity_key_set:
                connectable_portals.append(tbl)
                break

    return core + sorted(set(connectable_portals))


def table_columns(conn, table: str) -> list[str]:
    sql = f"""
        SELECT COLUMN_NAME
        FROM {db.RAW_DB}.INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = '{db.RAW_SCHEMA}' AND TABLE_NAME = '{table}'
        ORDER BY ORDINAL_POSITION
    """
    return [r[0] for r in db.rows(conn, sql)]


def _key_columns(columns: list[str]) -> list[dict]:
    """Detect the key-bearing columns of a table (skip provenance columns)."""
    out = []
    for c in columns:
        if c.startswith("_"):  # _INGESTED_AT / _SOURCE_RUN_ID / _SRC_SHA256
            continue
        key, tier = detect_key(c)
        if key:
            out.append({"column": c, "key": key, "tier": tier, "mode": join_mode(key)})
    return out


def fingerprint_table(conn, table: str) -> dict:
    cols = table_columns(conn, table)
    keycols = _key_columns(cols)
    rows_total = db.scalar(conn, f"SELECT COUNT(*) FROM {db.fqn(table)}") or 0

    # Measure population for the VALUE keys in one scan. Spatial keys (lat/lon,
    # geometry) get a plain non-null count (distinct is meaningless for geometry).
    measured = keycols[:MAX_KEY_COLS_PER_TABLE]
    if len(keycols) > MAX_KEY_COLS_PER_TABLE:
        print(f"    [cap] {table}: measuring {MAX_KEY_COLS_PER_TABLE}/{len(keycols)} key cols")

    selects = []
    for i, kc in enumerate(measured):
        qc = quote_ident(kc["column"])
        if kc["mode"] == "value":
            expr = normalize_sql(kc["key"], qc)
        else:
            expr = f"TRY_TO_DOUBLE(TO_VARCHAR({qc}))" if kc["key"] == "LATLON" else qc
        selects.append(f"COUNT({expr}) AS nn_{i}")
        if kc["mode"] == "value":
            selects.append(f"APPROX_COUNT_DISTINCT({expr}) AS nd_{i}")
        else:
            selects.append(f"COUNT(DISTINCT {qc}) AS nd_{i}")

    stats = {}
    if selects:
        row = db.dicts(conn, f"SELECT {', '.join(selects)} FROM {db.fqn(table)}")[0]
        for i in range(len(measured)):
            stats[i] = (int(row[f"NN_{i}"] or 0), int(row[f"ND_{i}"] or 0))

    keys_out = []
    for i, kc in enumerate(measured):
        nn, nd = stats.get(i, (0, 0))
        keys_out.append({
            **kc,
            "nonnull": nn,
            "distinct": nd,
            "populated_pct": round(nn / rows_total * 100, 1) if rows_total else 0.0,
        })
    return {"rows": rows_total, "keys": keys_out}


def run(tables: list[str] | None = None, write: bool = True) -> dict:
    conn = db.connect()
    try:
        targets = tables or landed_tables(conn)
        print(f"fingerprinting {len(targets)} landed tables ...")
        result = {}
        for t in targets:
            fp = fingerprint_table(conn, t)
            live = [k for k in fp["keys"] if k["populated_pct"] > 0]
            tags = ", ".join(f"{k['key']}({k['populated_pct']:.0f}%)" for k in live) or "—"
            print(f"  {t:<42} rows={fp['rows']:>10,}  keys: {tags}")
            result[t] = fp
    finally:
        conn.close()

    if write:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(result, indent=2))
        print(f"\nwrote {OUT}")
    return result


if __name__ == "__main__":
    run()
