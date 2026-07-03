"""Atomic, idempotent landing: a crash or interrupt never leaves a half-table.

We land into a STAGING table and only swap it over the live table on FULL success.
If anything dies mid-stream (PAT death, SUSPEND, OOM), the live table is untouched
and the staging table is simply overwritten on the next run -- ZERO manual cleanup.
This is the property that lets a build session be "let loose": a failed load is a
no-op you re-run, not a mess you debug.

The SQL-plan functions are pure (unit-tested); `execute_swap` runs them behind a
connection (`# pragma: no cover`).
"""
from __future__ import annotations


def staging_name(table: str) -> str:
    return f"{table}__STAGING"


def swap_plan(table: str, *, database: str, schema: str) -> dict:
    """The statements that atomically promote the staging table to live.

    Snowflake `ALTER TABLE a SWAP WITH b` is a metadata-only atomic swap: after it,
    the old live data sits under the staging name and is dropped. If the live table
    does not exist yet, the staging table is renamed in. Either way the live table
    is never in a half-written state.
    """
    fq = f'"{database}"."{schema}"."{table}"'
    stg = f'"{database}"."{schema}"."{staging_name(table)}"'
    return {
        "swap_if_exists": f"ALTER TABLE {fq} SWAP WITH {stg}",
        "rename_if_absent": f"ALTER TABLE {stg} RENAME TO {fq}",
        "drop_staging": f"DROP TABLE IF EXISTS {stg}",
    }


def execute_swap(conn, table: str, *, database: str, schema: str) -> str:  # pragma: no cover - live I/O
    """Promote <TABLE>__STAGING to <TABLE> atomically. Call ONLY after the staging
    load fully succeeded (and its smoke referee passed). Returns the path taken."""
    from snow import execute, fetch_scalar  # noqa: E402

    plan = swap_plan(table, database=database, schema=schema)
    # Qualify INFORMATION_SCHEMA with the target database: unqualified it resolves
    # against the SESSION's current database, which only happens to be LIBRARY_RAW
    # today. A session parked elsewhere would see "table absent", take the rename
    # path, and error (or worse, rename over nothing) — so pin it explicitly.
    exists = fetch_scalar(
        conn,
        f'SELECT COUNT(*) FROM "{database}".INFORMATION_SCHEMA.TABLES '
        "WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s",
        (schema, table),
    )
    if exists:
        execute(conn, plan["swap_if_exists"])   # live <-> staging, atomic
        execute(conn, plan["drop_staging"])     # drop the now-old data
        return "swapped"
    execute(conn, plan["rename_if_absent"])      # first load: staging becomes live
    return "renamed"
