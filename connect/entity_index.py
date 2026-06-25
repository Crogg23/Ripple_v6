"""ENTITY_INDEX — a denormalized per-(entity, source) projection for dossiers.

One row per (entity_id, source_table): the label that source shows for the entity,
how many rows it has there, and a small preview object. The dossier verb rolls up
every source row for an entity from here; name search resolves against ENTITY_GOLDEN
(one row per entity) and then reads this for the cross-domain breakdown.

Rebuilt as a tail step of ``connect spine``; also exposed as ``connect entity-index``.
"""

from __future__ import annotations

from . import db, store
from .discover import domain_of
from .entity_index_specs import DISPLAY_SPECS
from .keys import normalize_sql, quote_ident
from .spine import _addr_expr, _name_expr  # one definition of name/addr, shared

INDEX_FQN = store.cfqn("ENTITY_INDEX")
EMAP_FQN = store.cfqn("ENTITY_MAP")


def build(conn, run_id: str = "") -> int:
    parts = []
    for tbl, spec in DISPLAY_SPECS.items():
        key = spec["key"]
        norm = normalize_sql(key, quote_ident(spec["key_col"]))
        preview_pairs = [f"'place', ANY_VALUE({_addr_expr(spec)})"]
        for label, col in spec.get("extra", {}).items():
            preview_pairs.append(f"'{label}', ANY_VALUE(TRIM({quote_ident(col)}))")
        preview = f"OBJECT_CONSTRUCT({', '.join(preview_pairs)})"
        parts.append(f"""
          SELECT e.ENTITY_ID, ANY_VALUE(e.ENTITY_TYPE) AS ENTITY_TYPE,
                 '{key}' AS KEY_TYPE, ANY_VALUE({norm}) AS KEY_VALUE,
                 '{tbl}' AS SOURCE_TABLE, '{domain_of(tbl)}' AS DOMAIN,
                 ANY_VALUE({_name_expr(spec)}) AS DISPLAY_LABEL,
                 COUNT(*) AS ROW_COUNT, {preview} AS PREVIEW
          FROM {db.fqn(tbl)} t
          JOIN {EMAP_FQN} e ON e.KEY_TYPE = '{key}' AND e.KEY_VALUE = {norm}
          WHERE {norm} IS NOT NULL
          GROUP BY e.ENTITY_ID""")
    union = " UNION ALL ".join(parts)
    db.rows(conn, f"""
        CREATE OR REPLACE TABLE {INDEX_FQN} AS
        SELECT *, UPPER(REGEXP_REPLACE(COALESCE(DISPLAY_LABEL, ''), '[^A-Za-z0-9]+', ' ')) AS DISPLAY_NORM
        FROM ( {union} )""")
    return int(db.scalar(conn, f"SELECT COUNT(*) FROM {INDEX_FQN}") or 0)


def run() -> int:
    conn = db.connect()
    try:
        store.ensure_schema(conn)
        n = build(conn)
    finally:
        conn.close()
    print(f"entity index: {n:,} (entity, source) rows -> {INDEX_FQN}")
    return n


if __name__ == "__main__":
    run()
