"""Post-land lifecycle: the shared steps every loader runs after a successful atomic swap.

Unifies what was previously scattered across bridge_fuel_load, server_side_load, and
onboard.py into one call:

    lifecycle.on_success(source_id, table_name, spec, conn)

Steps (in order):
    1. Log to INGEST_RUNS (already done by loaders — this is the hook point AFTER)
    2. Scaffold dbt staging model if missing
    3. Trigger incremental connection engine for the landed table

This module is imported by bridge_fuel_load and server_side_load. The onboard agent
has its own checkpoint pipeline (RECON→SCRIPT→LOAD→DBT→REGISTRY→CONNECT) that does
the same things differently, so it doesn't use this.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


def on_success(source_id: str, table_name: str | None = None,
               key_cols: list[dict] | None = None,
               description: str = "",
               conn=None,
               skip_scaffold: bool = False,
               skip_connect: bool = False) -> dict:
    """Run post-land lifecycle steps after a successful load.

    Args:
        source_id: e.g. "FED_FEC_LEADERSHIP_PAC"
        table_name: landing table name (defaults to source_id.upper())
        key_cols: [{"col": "src_name", "as": "CANONICAL"}] for scaffold
        description: one-line description for schema.yml
        conn: Snowflake connection (used for scaffold DESCRIBE)
        skip_scaffold: skip dbt scaffold step
        skip_connect: skip connection engine step

    Returns:
        dict with keys: scaffolded (path|None), connected (bool), errors (list)
    """
    table_name = table_name or source_id.upper()
    key_cols = key_cols or []
    result = {"scaffolded": None, "connected": False, "errors": []}

    # Step 1: Scaffold dbt staging model if missing
    if not skip_scaffold:
        try:
            from loadkit.scaffold import scaffold_if_missing
            scaffolded = scaffold_if_missing(
                source_id=source_id,
                table_name=table_name,
                key_cols=key_cols,
                description=description,
                conn=conn,
            )
            result["scaffolded"] = scaffolded
        except Exception as e:
            result["errors"].append(f"scaffold: {e}")

    # Step 2: Trigger incremental connection engine
    if not skip_connect:
        try:
            _connect_one(source_id)
            result["connected"] = True
        except Exception as e:
            result["errors"].append(f"connect: {e}")

    return result


def _connect_one(source_id: str) -> None:
    """Run `python -m connect.incremental connect-one --source <id>` as a subprocess.

    We shell out rather than importing directly because connect.incremental imports
    heavy dependencies (snowflake-connector, the full connect package) and we don't
    want lifecycle to drag those in when imported from bridge_fuel_load (which has
    its own connection management).
    """
    cmd = [
        sys.executable, "-m", "connect.incremental",
        "connect-one", "--source", source_id.lower(),
    ]
    result = subprocess.run(
        cmd,
        cwd=str(REPO),
        capture_output=True,
        text=True,
        timeout=300,  # 5 min cap — single-table should be fast
    )
    if result.returncode != 0:
        stderr = (result.stderr or "").strip()[:200]
        raise RuntimeError(f"connect-one failed (rc={result.returncode}): {stderr}")
