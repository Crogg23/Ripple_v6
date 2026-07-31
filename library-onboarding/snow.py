"""Shared Snowflake connection + tiny query helpers.

Used by the LOAD and REGISTRY checkpoints. Connections are short-lived: open,
do the work, close.
"""

from __future__ import annotations

from typing import Optional

from config import ConfigError, settings


def connect(*, pat=None, warehouse=None, role=None, session_parameters=None):
    """Open a Snowflake connection. Fails loudly if credentials are missing.

    Auth precedence: a Programmatic Access Token (SNOWFLAKE_PAT) is used in place
    of a password when present. By default the PAT is supplied as the password;
    set SNOWFLAKE_AUTHENTICATOR=PROGRAMMATIC_ACCESS_TOKEN to pass it as a token.

    Optional keyword overrides (all default to config settings, so every existing
    caller is unchanged): `pat` swaps the credential (e.g. a read-only serving PAT),
    `warehouse`/`role` pin the session, and `session_parameters` are applied AT
    CONNECT (one round trip) instead of via post-connect ALTER SESSION calls.
    config.settings freezes env at import, so overrides MUST be parameters here —
    mutating os.environ after import does nothing.
    """
    settings.require("snowflake_account", "snowflake_user", "snowflake_warehouse")
    pat = (pat or "").strip() or None
    if not (pat or settings.snowflake_pat.strip()
            or settings.snowflake_password.strip() or settings.has_private_key()):
        raise ConfigError(
            "No usable Snowflake credential. Set SNOWFLAKE_PAT, SNOWFLAKE_PASSWORD, or "
            "generate a key pair with `python scripts/rotate_dbt_keypair.py` and "
            "register the printed public key on the user."
        )
    try:
        import snowflake.connector
    except ImportError as exc:  # pragma: no cover
        raise ConfigError(
            "snowflake-connector-python is required. Run `pip install -r requirements.txt`."
        ) from exc

    kwargs = {
        "account": settings.snowflake_account,
        "user": settings.snowflake_user,
        "warehouse": warehouse or settings.snowflake_warehouse,
        "role": role or settings.snowflake_role or None,
    }
    if session_parameters:
        # merge, never replace: every session keeps the hung-query guards even
        # when a caller pins only its own parameters
        sp = dict(session_parameters)
        try:
            secs = int(getattr(settings, "statement_timeout_s", 3600) or 0)
        except Exception:
            secs = 3600
        if secs > 0:
            sp.setdefault("STATEMENT_TIMEOUT_IN_SECONDS", secs if "STATEMENT_TIMEOUT_IN_SECONDS" not in sp else sp["STATEMENT_TIMEOUT_IN_SECONDS"])
            sp.setdefault("ABORT_DETACHED_QUERY", True)
        kwargs["session_parameters"] = sp
    tok = (pat or settings.snowflake_pat).strip()
    auth = settings.snowflake_authenticator.strip()
    if tok:
        if auth:
            kwargs["authenticator"] = auth
            kwargs["token"] = tok
        else:
            kwargs["password"] = tok  # PATs work as a password replacement
    elif settings.has_private_key():
        # Key-pair auth (2026-07-29). Deliberately ranked ABOVE the password: this
        # machine has a stale SNOWFLAKE_PASSWORD in its environment that Snowflake
        # rejects (error 250001), so preferring the password would fail every script
        # while a working key sat right there. An explicitly passed `pat` still wins,
        # since callers use that to pin a narrower serving credential.
        kwargs["private_key"] = _private_key_der(settings.snowflake_private_key_path)
    else:
        kwargs["password"] = settings.snowflake_password
    conn = snowflake.connector.connect(**kwargs)
    if not session_parameters:
        _apply_session_guards(conn)
    return conn


def _private_key_der(path: str) -> bytes:
    """Load the PEM private key and hand the connector the DER bytes it wants."""
    from pathlib import Path

    from cryptography.hazmat.primitives import serialization

    p = Path(path).expanduser()
    if not p.exists():
        raise ConfigError(
            f"Snowflake private key not found at {p}. Generate one with "
            "`python scripts/rotate_dbt_keypair.py` and register the public key."
        )
    with open(p, "rb") as fh:
        key = serialization.load_pem_private_key(fh.read(), password=None)
    return key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )


def _apply_session_guards(conn) -> None:
    """Clamp the session so a hung or detached query can't hold (and bill) the
    warehouse for the account-default 48h during an unattended pour. Best-effort --
    never fail a connect over it."""
    try:
        secs = int(getattr(settings, "statement_timeout_s", 3600) or 0)
    except Exception:
        secs = 3600
    if secs <= 0:
        return
    cur = conn.cursor()
    try:
        # ALTER SESSION doesn't accept a bind param for this setting, so the
        # int() cast above is the only thing standing between this f-string
        # and injection if settings.statement_timeout_s is ever sourced from
        # somewhere less trusted. Re-validate right at the interpolation
        # point too, so this line stays safe even if that upstream cast is
        # ever refactored away.
        if not isinstance(secs, int):
            raise TypeError(f"statement_timeout_s must be int, got {type(secs).__name__}")
        cur.execute(f"ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = {secs}")
        cur.execute("ALTER SESSION SET ABORT_DETACHED_QUERY = TRUE")
    except Exception:
        pass
    finally:
        cur.close()


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
