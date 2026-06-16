"""Shared Snowflake connection + tiny query helpers.

Used by the LOAD and REGISTRY checkpoints. Connections are short-lived: open,
do the work, close.
"""

from __future__ import annotations

from typing import Optional

from config import ConfigError, settings


def connect():
    """Open a Snowflake connection. Fails loudly if credentials are missing.

    Auth precedence: a Programmatic Access Token (SNOWFLAKE_PAT) is used in place
    of a password when present. By default the PAT is supplied as the password;
    set SNOWFLAKE_AUTHENTICATOR=PROGRAMMATIC_ACCESS_TOKEN to pass it as a token.
    """
    settings.require("snowflake_account", "snowflake_user", "snowflake_warehouse")
    if not (settings.snowflake_pat.strip() or settings.snowflake_password.strip()):
        raise ConfigError("Set SNOWFLAKE_PAT (programmatic access token) or SNOWFLAKE_PASSWORD.")
    try:
        import snowflake.connector
    except ImportError as exc:  # pragma: no cover
        raise ConfigError(
            "snowflake-connector-python is required. Run `pip install -r requirements.txt`."
        ) from exc

    kwargs = {
        "account": settings.snowflake_account,
        "user": settings.snowflake_user,
        "warehouse": settings.snowflake_warehouse,
        "role": settings.snowflake_role or None,
    }
    pat = settings.snowflake_pat.strip()
    auth = settings.snowflake_authenticator.strip()
    if pat:
        if auth:
            kwargs["authenticator"] = auth
            kwargs["token"] = pat
        else:
            kwargs["password"] = pat  # PATs work as a password replacement
    else:
        kwargs["password"] = settings.snowflake_password
    return snowflake.connector.connect(**kwargs)


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
