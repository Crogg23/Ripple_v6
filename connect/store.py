"""Shared persistence for the entity layer.

The connect engine historically wrote only ``outputs/connect_graph.json`` plus a
couple of TRANSIENT scratch tables. The entity layer (leads, the entity spine, the
entity index, fuzzy links) needs PERSISTED tables — they all live in
``LIBRARY_META.CONNECT``. ``CONNECT`` is a reserved word, so it is ALWAYS quoted.

Everything here is deliberately tiny: a name builder + a schema guard, so every
new module spells the schema the same way and we never duplicate the DDL prelude.
"""

from __future__ import annotations

import json

from . import db
from .discover import CONNECT_DB, CONNECT_SCHEMA  # single source of truth for the names


def cfqn(table: str) -> str:
    """Fully-qualified, quoted name of a PERSISTENT table in LIBRARY_META.CONNECT."""
    return f'"{CONNECT_DB}"."{CONNECT_SCHEMA}"."{table.strip().upper()}"'


def ensure_schema(conn) -> None:
    """Create the CONNECT schema if it isn't there yet (idempotent)."""
    db.rows(conn, f'CREATE SCHEMA IF NOT EXISTS "{CONNECT_DB}"."{CONNECT_SCHEMA}"')


# =========================================================================== #
# CANONICAL EDGE WRITER — the graph, queryable.
# discover.run() has always computed the full edge list (with the join columns)
# but only ever wrote it to outputs/connect_graph.json. This persists that same
# list to LIBRARY_META.CONNECT.CONNECT_EDGES so the graph is queryable from SQL
# (and therefore evidence.dev) and survives a fresh checkout.
# =========================================================================== #
EDGES_TABLE = "CONNECT_EDGES"

# Column list for a fresh CONNECT_EDGES. A_COL/B_COL are the JOIN columns — the
# reason a bare (A, B, KEY) edge could not become a real SQL join (audit D19).
_EDGES_COLS = (
    'A STRING, B STRING, KEY STRING, TIER STRING, A_COL STRING, B_COL STRING, '
    'MATCHED NUMBER, A_DISTINCT NUMBER, B_DISTINCT NUMBER, MATCH_RATE FLOAT, '
    'CONFIDENCE FLOAT, "SAMPLE" VARIANT, RUN_ID STRING, '
    'BUILT_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()'
)

# INSERT columns, in order (SAMPLE is PARSE_JSON'd from a json string param).
_EDGE_INSERT_COLS = (
    "A", "B", "KEY", "TIER", "A_COL", "B_COL", "MATCHED", "A_DISTINCT",
    "B_DISTINCT", "MATCH_RATE", "CONFIDENCE", "SAMPLE", "RUN_ID",
)


def write_edges(conn, edges: list[dict], run_id: str, *,
                table: str = EDGES_TABLE, chunk: int = 1000) -> int:
    """Full-replace CONNECT_EDGES with `edges` (the graph['edges'] shape from
    discover.run()). Returns the row count written.

    Each edge dict carries: a, b, key, tier, a_col, b_col, matched, a_distinct,
    b_distinct, match_rate, confidence, sample. A_COL/B_COL make an edge a real
    SQL join (A.A_COL = B.B_COL). SAMPLE is stored as VARIANT.

    Legacy CONNECT_EDGES (created 2026-07-02) predates A_COL/B_COL; they are added
    in place via ALTER ADD COLUMN IF NOT EXISTS — an ALTER, NOT a CREATE OR REPLACE,
    so existing grants (RIPPLE_READER SELECT) are preserved without COPY GRANTS."""
    ensure_schema(conn)
    fqn = cfqn(table)
    db.rows(conn, f"CREATE TABLE IF NOT EXISTS {fqn} ({_EDGES_COLS})")
    db.rows(conn, f"ALTER TABLE {fqn} ADD COLUMN IF NOT EXISTS A_COL STRING")
    db.rows(conn, f"ALTER TABLE {fqn} ADD COLUMN IF NOT EXISTS B_COL STRING")
    db.rows(conn, f"TRUNCATE TABLE {fqn}")
    if not edges:
        return 0

    collist = ", ".join(f'"{c}"' for c in _EDGE_INSERT_COLS)
    # VALUES gives column1..column13; SELECT applies PARSE_JSON to the sample col
    # (column12). One multi-row INSERT per chunk keeps it O(edges / chunk) round-trips.
    sel = ("SELECT column1, column2, column3, column4, column5, column6, column7, "
           "column8, column9, column10, column11, PARSE_JSON(column12), column13")
    row_ph = "(" + ",".join(["%s"] * 13) + ")"

    written = 0
    for i in range(0, len(edges), chunk):
        batch = edges[i:i + chunk]
        params: list = []
        for e in batch:
            params += [
                e["a"], e["b"], e["key"], e["tier"],
                e.get("a_col") or None, e.get("b_col") or None,
                int(e.get("matched") or 0), int(e.get("a_distinct") or 0),
                int(e.get("b_distinct") or 0), float(e.get("match_rate") or 0.0),
                float(e.get("confidence") or 0.0),
                json.dumps(e.get("sample") or []), run_id,
            ]
        values = ", ".join([row_ph] * len(batch))
        db.rows(conn, f"INSERT INTO {fqn} ({collist}) {sel} FROM VALUES {values}",
                tuple(params))
        written += len(batch)
    return written
