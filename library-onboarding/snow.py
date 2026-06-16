"""Shared Snowflake connection + tiny query helpers.

Used by the LOAD and REGISTRY checkpoints. Connections are short-lived: open,
do the work, close.
"""

from __future__ import annotations

from typing import Optional

from config import ConfigError, settings


def connect():
    """Open a Snowflake connection. Fails loudly if credentials are missing."""
    settings.require("snowflake_account", "snowflake_user", "snowflake_password", "snowflake_warehouse")
    try:
        import snowflake.connector
    except ImportError as exc:  # pragma: no cover
        raise ConfigError(
            "snowflake-connector-python is required. Run `pip install -r requirements.txt`."
        ) from exc
    return snowflake.connector.connect(
        account=settings.snowflake_account,
        user=settings.snowflake_user,
        password=settings.snowflake_password,
        warehouse=settings.snowflake_warehouse,
        role=settings.snowflake_role or None,
    )


def fetch_scalar(conn, sql: str, params: Optional[tuple] = None):
    cur = conn.cursor()
    try:
        cur.execute(sql, params or ())
        row = cur.fetchone()
        return row[0] if row else None
    finally:
        cur.close()


def execute(conn, sql: str, params: Optional[tuple] = None) -> None:
    cur = conn.cursor()
    try:
        cur.execute(sql, params or ())
    finally:
        cur.close()
