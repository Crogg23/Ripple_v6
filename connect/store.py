"""Shared persistence for the entity layer.

The connect engine historically wrote only ``outputs/connect_graph.json`` plus a
couple of TRANSIENT scratch tables. The entity layer (leads, the entity spine, the
entity index, fuzzy links) needs PERSISTED tables — they all live in
``LIBRARY_META.CONNECT``. ``CONNECT`` is a reserved word, so it is ALWAYS quoted.

Everything here is deliberately tiny: a name builder + a schema guard, so every
new module spells the schema the same way and we never duplicate the DDL prelude.
"""

from __future__ import annotations

from . import db
from .discover import CONNECT_DB, CONNECT_SCHEMA  # single source of truth for the names


def cfqn(table: str) -> str:
    """Fully-qualified, quoted name of a PERSISTENT table in LIBRARY_META.CONNECT."""
    return f'"{CONNECT_DB}"."{CONNECT_SCHEMA}"."{table.strip().upper()}"'


def ensure_schema(conn) -> None:
    """Create the CONNECT schema if it isn't there yet (idempotent)."""
    db.rows(conn, f'CREATE SCHEMA IF NOT EXISTS "{CONNECT_DB}"."{CONNECT_SCHEMA}"')
