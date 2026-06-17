"""Checkpoints 2 + 3 -- SCRIPT and LOAD.

Checkpoint 2: Claude writes a source-specific ``fetch_data(context)`` that
downloads/parses the source and returns a pandas DataFrame (raw, all values as
strings) -- and stashes the raw source bytes for content hashing.

Checkpoint 3: we run it, content-hash the source (SHA-256), stamp every row with
``_INGESTED_AT / _SOURCE_RUN_ID / _SRC_SHA256``, snapshot-replace the landing
table ``RIPPLE_RAW.LANDING.<UPPER(SOURCE_ID)>`` (idempotent by construction), and
write one row to ``RIPPLE_META.INGEST_LOGS.INGEST_RUNS``.

If the content hash matches the source's last successful run, the reload is
skipped (set ONBOARD_SKIP_IF_UNCHANGED=0 to force).
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import os
import re
import uuid
from typing import Optional, Tuple

import snow
from config import ConfigError, settings
from llm import call_claude, extract_code, render_prompt

META_INGESTED_AT = "_INGESTED_AT"
META_SOURCE_RUN_ID = "_SOURCE_RUN_ID"
META_SRC_SHA256 = "_SRC_SHA256"
SAMPLE_ROWS = 5


# ---------------------------------------------------------------------------
# Checkpoint 2 -- generate the ingestion script
# ---------------------------------------------------------------------------
def generate_ingest_script(config: dict, feedback: Optional[str] = None) -> str:
    schema_repr = "\n".join(
        f"  - {f.get('name')} ({f.get('type')}): {f.get('description','')}"
        for f in config.get("schema_fields", [])
    ) or "  (schema unknown -- infer from the source)"

    prompt = render_prompt(
        "generate_ingest",
        name=config["name"],
        url=config["url"],
        access_pattern=config.get("access_pattern", "unknown"),
        auth_type=config.get("auth", {}).get("type", "none"),
        auth_notes=config.get("auth", {}).get("notes", ""),
        data_format=config.get("format", "unknown"),
        rate_limits=config.get("rate_limits", "unspecified"),
        schema=schema_repr,
        feedback=feedback or "(none)",
    )
    raw = call_claude(
        user=prompt,
        system=(
            "You write robust Python data-ingestion functions for a raw landing "
            "zone. Output ONLY a Python code block defining `def fetch_data(context):` "
            "that returns a pandas.DataFrame of strings. No Snowflake code."
        ),
        kind="ingest",
        fake_context=config,
        max_tokens=4096,
    )
    return extract_code(raw, "python")


# ---------------------------------------------------------------------------
# Checkpoint 3 -- execute + load
# ---------------------------------------------------------------------------
def run_ingest(config: dict, code: str) -> dict:
    run_id = str(uuid.uuid4())
    started = _utcnow()
    source_id = config["source_id"]
    table = config["landing_table"]
    url = config["url"]

    df, raw_bytes, source_file = _execute_fetch(config, code)
    payload = raw_bytes if raw_bytes else _df_bytes(df)
    sha = hashlib.sha256(payload).hexdigest()
    file_bytes = len(payload)

    df = _stringify(df)  # raw mirror: all source columns are text
    df[META_INGESTED_AT] = started.replace(tzinfo=None)
    df[META_SOURCE_RUN_ID] = run_id
    df[META_SRC_SHA256] = sha

    result = {
        "run_id": run_id,
        "sha256": sha,
        "file_bytes": file_bytes,
        "source_file": source_file,
        "rows": int(len(df)),
        "columns": ", ".join(map(str, df.columns)),
        "sample_rows": df.head(SAMPLE_ROWS).astype(str).to_dict(orient="records"),
    }

    if settings.fake_llm or not settings.snowflake_ready():
        why = "fake mode" if settings.fake_llm else "Snowflake creds not set"
        result["status"] = (
            f"DRY RUN ({why}) -- would snapshot-replace RIPPLE_RAW.LANDING.{table} "
            f"with {len(df):,} rows (sha {sha[:12]})"
        )
        return result

    conn = snow.connect()
    try:
        if settings.skip_if_unchanged:
            last = _latest_success_sha(conn, source_id)
            if last == sha:
                result["status"] = (
                    f"UNCHANGED -- sha {sha[:12]} matches last successful run; reload skipped "
                    "(set ONBOARD_SKIP_IF_UNCHANGED=0 to force)"
                )
                result["skipped"] = True
                return result
        try:
            _load_landing(conn, df, table)
            ended = _utcnow()
            _log_run(conn, source_id, run_id, "success", len(df), file_bytes, sha, url,
                     started, ended, _auto_message(config, len(df)))
            result["status"] = f"Loaded {len(df):,} rows -> RIPPLE_RAW.LANDING.{table}"
        except Exception as exc:
            ended = _utcnow()
            try:
                _log_run(conn, source_id, run_id, "failed", None, file_bytes, sha, url,
                         started, ended, f"Load failed: {exc}")
            except Exception:
                pass
            raise
    finally:
        conn.close()
    return result


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _execute_fetch(config: dict, code: str) -> Tuple[object, Optional[bytes], str]:
    """Run Claude-generated code and return (DataFrame, raw_bytes, source_file).

    SECURITY: this executes model-generated Python. It only runs after the
    foreman approved the exact code shown at Checkpoint 2.
    """
    try:
        import pandas as pd  # noqa: F401  (available to generated code)
    except ImportError as exc:  # pragma: no cover
        raise ConfigError("pandas is required. Run `pip install -r requirements.txt`.") from exc

    namespace: dict = {}
    exec(compile(code, "<generated_ingest>", "exec"), namespace)  # noqa: S102
    fetch = namespace.get("fetch_data")
    if not callable(fetch):
        raise RuntimeError("Generated script did not define fetch_data(context).")

    context = {
        "url": config["url"],
        "source_name": config["name"],
        "auth_type": config.get("auth", {}).get("type", "none"),
        "env": dict(os.environ),
        "source_bytes": None,
        "source_file": "",
    }
    df = fetch(context)
    if not hasattr(df, "columns"):
        raise RuntimeError("fetch_data must return a pandas.DataFrame.")
    if len(df) == 0:
        raise RuntimeError("fetch_data returned 0 rows -- failing loudly (schema drift?).")

    raw_bytes = context.get("source_bytes")
    if raw_bytes is not None and not isinstance(raw_bytes, (bytes, bytearray)):
        raw_bytes = str(raw_bytes).encode("utf-8")

    _reject_html(df, raw_bytes)  # a docs/landing page fetched instead of the data
    return df, raw_bytes, context.get("source_file", "") or ""


def _reject_html(df, raw_bytes) -> None:
    """Fail loudly when an HTML page lands instead of the dataset.

    Symptom seen in the wild (fed_cms_hpt_enforcement): the generated fetch hit a
    docs/landing URL, so pandas parsed an HTML page into a single bogus column
    (e.g. ``DOCTYPE_HTML``) -- a false "success" of junk rows. Catch it here.
    """
    head = bytes(raw_bytes[:256]).lstrip().lower() if raw_bytes else b""
    if head.startswith((b"<!doctype html", b"<html", b"<!doctype>")):
        raise RuntimeError(
            "fetch_data returned an HTML page, not data -- the fetch hit a docs/"
            "landing URL instead of the dataset endpoint. Fix the URL/parse."
        )
    cols = [str(c).upper() for c in df.columns]
    if len(cols) == 1 and ("DOCTYPE" in cols[0] or "HTML" in cols[0] or "<" in cols[0]):
        raise RuntimeError(
            f"fetch_data parsed HTML into a single column ('{df.columns[0]}'), not "
            "tabular data -- the fetch hit the wrong URL. Fix the URL/parse."
        )


def _stringify(df):
    """Coerce every source column to text (the raw landing convention)."""
    df = df.where(df.notna(), None)
    df.columns = [_sf_col(c) for c in df.columns]
    for col in df.columns:
        df[col] = df[col].map(lambda v: "" if v is None else str(v))
    return df


def _sf_col(name) -> str:
    """Sanitize to an unquoted, uppercase Snowflake identifier (matches LANDING)."""
    clean = re.sub(r"[^0-9A-Za-z_]+", "_", str(name)).strip("_") or "COL"
    if clean[0].isdigit():
        clean = "C_" + clean
    return clean.upper()


def _df_bytes(df) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def _load_landing(conn, df, table: str) -> None:
    from snowflake.connector.pandas_tools import write_pandas

    database, schema = settings.raw_database, settings.raw_schema
    snow.execute(conn, f'CREATE SCHEMA IF NOT EXISTS "{database}"."{schema}"')
    ok, _chunks, nrows, _ = write_pandas(
        conn, df, table_name=table, database=database, schema=schema,
        auto_create_table=True, overwrite=True, quote_identifiers=False,
    )
    if not ok:
        raise RuntimeError(f"write_pandas reported failure loading {table}.")


def _latest_success_sha(conn, source_id: str) -> Optional[str]:
    fqt = f'"{settings.meta_database}"."{settings.ingest_log_schema}"."{settings.ingest_log_table}"'
    return snow.fetch_scalar(
        conn,
        f"SELECT SHA256 FROM {fqt} WHERE SOURCE_ID=%s AND STATUS='success' "
        "ORDER BY STARTED_AT DESC LIMIT 1",
        (source_id,),
    )


def _log_run(conn, source_id, run_id, status, row_count, file_bytes, sha, url, started, ended, message) -> None:
    fqt = f'"{settings.meta_database}"."{settings.ingest_log_schema}"."{settings.ingest_log_table}"'
    snow.execute(
        conn,
        f"INSERT INTO {fqt} (SOURCE_ID, RUN_ID, STARTED_AT, ENDED_AT, STATUS, ROW_COUNT, "
        "FILE_BYTES, SHA256, SOURCE_URL, MESSAGE, _LOADED_AT) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, CURRENT_TIMESTAMP())",
        (source_id, run_id, started.replace(tzinfo=None), ended.replace(tzinfo=None),
         status, row_count, file_bytes, sha, url, message),
    )


def _auto_message(config: dict, rows: int) -> str:
    desc = config.get("description") or config["name"]
    unit = config.get("unit_of_observation") or "one row = one record"
    return (
        f"{desc}. {unit}. Snapshot-replace load of {rows} rows into "
        f"RIPPLE_RAW.LANDING.{config['landing_table']} via the onboarding agent."
    )


def _utcnow() -> _dt.datetime:
    return _dt.datetime.now(_dt.timezone.utc)
