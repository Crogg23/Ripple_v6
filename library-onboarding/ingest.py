"""Checkpoints 2 + 3 -- SCRIPT and LOAD.

Checkpoint 2: Claude writes a source-specific ``fetch_data(context)`` that
downloads/parses the source and returns a pandas DataFrame (raw, all values as
strings) -- and stashes the raw source bytes for content hashing.

Checkpoint 3: we run it, content-hash the source (SHA-256), stamp every row with
``_INGESTED_AT / _SOURCE_RUN_ID / _SRC_SHA256``, snapshot-replace the landing
table ``LIBRARY_RAW.LANDING.<UPPER(SOURCE_ID)>`` (idempotent by construction), and
write one row to ``LIBRARY_META.INGEST_LOGS.INGEST_RUNS``.

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

import browser
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
    load_mode = (config.get("load_mode") or "snapshot").strip().lower()
    live = not (settings.fake_llm or not settings.snowflake_ready())

    # Chunked: a single very large file streamed in row-batches (separate path, so the
    # snapshot/incremental logic below is untouched). Same landing table + provenance.
    if load_mode == "chunked":
        return _run_chunked(config, code, run_id, started, source_id, table, url, live)

    incremental = load_mode == "incremental"
    cursor_field = (config.get("cursor_field") or "").strip()

    # Incremental: read the high-water mark BEFORE fetching, so the fetch pulls only
    # records newer than what we already hold. None => first run (bounded backfill).
    since = None
    if incremental and cursor_field and live:
        try:
            wm_conn = snow.connect()
            try:
                since = _watermark(wm_conn, table, cursor_field)
            finally:
                wm_conn.close()
        except Exception:
            since = None

    # allow_empty only on a CONTINUING incremental run (we already hold a watermark):
    # then "0 new rows" is a legit no-op. On the FIRST incremental run (since is None,
    # empty table) 0 rows means the backfill found nothing -> fail loudly so the source
    # isn't falsely marked onboarded with no data landed.
    df, raw_bytes, source_file = _execute_fetch(
        config, code, since=since, allow_empty=incremental and since is not None
    )
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
        "load_mode": "incremental" if incremental else "snapshot",
        "since": since,
        "columns": ", ".join(map(str, df.columns)),
        "sample_rows": df.head(SAMPLE_ROWS).astype(str).to_dict(orient="records"),
    }

    if not live:
        why = "fake mode" if settings.fake_llm else "Snowflake creds not set"
        verb = f"append to (since {since or 'start'})" if incremental else "snapshot-replace"
        result["status"] = (
            f"DRY RUN ({why}) -- would {verb} LIBRARY_RAW.LANDING.{table} "
            f"with {len(df):,} rows (sha {sha[:12]})"
        )
        return result

    conn = snow.connect()
    try:
        # Incremental run that found nothing new since the watermark -> clean no-op.
        if incremental and len(df) == 0:
            ended = _utcnow()
            _log_run(conn, source_id, run_id, "success", 0, file_bytes, sha, url,
                     started, ended, f"Incremental: no new rows since {since or 'start'}.")
            result["status"] = f"UP TO DATE -- no new rows since {since or 'start'} (incremental)"
            return result

        # Snapshot only: skip the reload when the content hash is unchanged.
        if not incremental and settings.skip_if_unchanged:
            last = _latest_success_sha(conn, source_id)
            if last == sha:
                result["status"] = (
                    f"UNCHANGED -- sha {sha[:12]} matches last successful run; reload skipped "
                    "(set ONBOARD_SKIP_IF_UNCHANGED=0 to force)"
                )
                result["skipped"] = True
                return result
        try:
            _load_landing(conn, df, table, overwrite=not incremental)
            ended = _utcnow()
            _log_run(conn, source_id, run_id, "success", len(df), file_bytes, sha, url,
                     started, ended, _auto_message(config, len(df)))
            if incremental:
                result["status"] = (
                    f"Appended {len(df):,} rows (incremental since {since or 'start'}) "
                    f"-> LIBRARY_RAW.LANDING.{table}"
                )
            else:
                result["status"] = f"Loaded {len(df):,} rows -> LIBRARY_RAW.LANDING.{table}"
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
# Chunked load (C3) -- stream a large file and write it in row-batches
# ---------------------------------------------------------------------------
def _run_chunked(config: dict, code: str, run_id: str, started, source_id: str,
                 table: str, url: str, live: bool) -> dict:
    """Stream a too-big-for-memory source in chunks, writing each to the landing
    table as it arrives. The table grows chunk-by-chunk, so a crash leaves the rows
    already landed in place; a re-run resumes from the current row count.

    Same landing-table shape + provenance stamps as snapshot/incremental. Each row
    carries the SHA-256 of ITS chunk (per-chunk provenance, since the whole file is
    never held in memory); INGEST_RUNS gets a manifest SHA over all chunk hashes.
    """
    chunk_rows = max(1, settings.chunk_rows)
    max_rows = max(0, settings.chunk_max_rows)

    if not live:
        why = "fake mode" if settings.fake_llm else "Snowflake creds not set"
        return {
            "run_id": run_id, "load_mode": "chunked", "rows": 0,
            "status": (f"DRY RUN ({why}) -- would STREAM a chunked load into "
                       f"LIBRARY_RAW.LANDING.{table} in batches of {chunk_rows:,} rows"
                       + (f" (capped at {max_rows:,})" if max_rows else "")),
        }

    # Resume detection: rows already in the landing table that were NOT followed by a
    # successful run = a prior chunked load that crashed mid-stream. Resume from there.
    # If the last run DID succeed, a fresh re-run replaces the table (full reload).
    conn0 = snow.connect()
    try:
        existing = _landing_count(conn0, table)
        had_success = _latest_success_sha(conn0, source_id) is not None
    finally:
        conn0.close()
    resume = existing > 0 and not had_success
    resume_from = existing if resume else 0

    chunk_iter = _execute_fetch_chunks(config, code, resume_from_row=resume_from,
                                       chunk_rows=chunk_rows, chunk_max_rows=max_rows)

    conn = snow.connect()
    try:
        appended, manifest_sha, file_bytes, columns, sample = _load_landing_chunked(
            conn, chunk_iter, table, run_id, started,
            resume_from_row=resume_from, fresh=not resume, max_rows=max_rows,
        )
        ended = _utcnow()
        total = resume_from + appended
        verb = f"resumed from row {resume_from:,}; appended" if resume else "streamed"
        msg = (f"Chunked load: {verb} {appended:,} rows in batches of {chunk_rows:,} "
               f"-> LIBRARY_RAW.LANDING.{table} (table now {total:,} rows"
               + (f"; capped at {max_rows:,}/run)." if max_rows else ").")
               + f" Manifest sha {manifest_sha[:12]}.")
        _log_run(conn, source_id, run_id, "success", appended, file_bytes, manifest_sha,
                 url, started, ended, msg)
        status = (f"Streamed {appended:,} rows in {chunk_rows:,}-row chunks "
                  f"-> LIBRARY_RAW.LANDING.{table} (table now {total:,} rows)"
                  + (f" [resumed from {resume_from:,}]" if resume else ""))
        return {
            "run_id": run_id, "sha256": manifest_sha, "file_bytes": file_bytes,
            "rows": appended, "load_mode": "chunked", "resumed_from": resume_from,
            "columns": ", ".join(map(str, columns)), "sample_rows": sample,
            "status": status,
        }
    except Exception as exc:
        ended = _utcnow()
        # Rows already written stay put -- log the partial progress so the next run
        # can resume from the current landing row count.
        try:
            landed = _landing_count(conn, table)
            _log_run(conn, source_id, run_id, "failed", None, None, "", url, started, ended,
                     f"Chunked load failed after landing {landed:,} rows (resumable): {exc}")
        except Exception:
            pass
        raise
    finally:
        conn.close()


def _execute_fetch_chunks(config: dict, code: str, resume_from_row: int,
                          chunk_rows: int, chunk_max_rows: int):
    """Exec the generated code and return an ITERATOR of DataFrame chunks.

    The generated ``fetch_data`` is expected to be a generator that ``yield``s
    DataFrames (streaming the download). A generator function returns its generator
    object without running the body, so building this is cheap -- the network work
    happens lazily as the loader pulls each chunk. If the code returns a single
    DataFrame instead, it is treated as a one-chunk stream.

    SECURITY: executes model-generated Python, only after Checkpoint-2 approval.
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
        "render": browser.render,
        # chunked controls the generated fetch honours:
        "load_mode": "chunked",
        "resume_from_row": resume_from_row,  # skip this many data rows (resume)
        "chunk_rows": chunk_rows,            # rows per yielded chunk
        "chunk_max_rows": chunk_max_rows,    # stop after this many (0 = unlimited)
        "since": None,
        "source_bytes": None,
        "source_file": "",
    }
    result = fetch(context)
    if hasattr(result, "columns"):           # a single DataFrame -> one chunk
        return iter([result])
    if result is None:
        raise RuntimeError("Chunked fetch_data returned None -- it must yield DataFrame chunks.")
    return iter(result)


def _load_landing_chunked(conn, chunk_iter, table: str, run_id: str, started,
                          resume_from_row: int, fresh: bool, max_rows: int):
    """Write a stream of DataFrame chunks to the landing table, bounded memory.

    First chunk of a FRESH load replaces the table (snapshot-style); every other
    chunk appends. On resume, all chunks append. Returns
    ``(appended_rows, manifest_sha, file_bytes, columns, sample_rows)``.
    """
    from snowflake.connector.pandas_tools import write_pandas

    database, schema = settings.raw_database, settings.raw_schema
    snow.execute(conn, f'CREATE SCHEMA IF NOT EXISTS "{database}"."{schema}"')
    ingested_at = started.replace(tzinfo=None)

    appended = 0
    file_bytes = 0
    chunk_shas: list[str] = []
    columns: list = []
    sample: list = []
    n = 0
    # Resume is enforced HERE, not in the generated code: a resumed fetch re-yields
    # the file from the start, and we drop the rows already landed. This is dup-safe
    # regardless of whether the model's fetch honoured resume_from_row.
    to_skip = resume_from_row if not fresh else 0
    for chunk in chunk_iter:
        if not hasattr(chunk, "columns"):
            raise RuntimeError("Chunked fetch_data must yield pandas DataFrames.")
        if len(chunk) == 0:
            continue
        if to_skip > 0:
            if len(chunk) <= to_skip:
                to_skip -= len(chunk)
                continue
            chunk = chunk.iloc[to_skip:]
            to_skip = 0
        if n == 0:
            _reject_html(chunk)  # catch an HTML/landing page streamed as data

        csv_bytes = chunk.to_csv(index=False).encode("utf-8")
        chunk_sha = hashlib.sha256(csv_bytes).hexdigest()
        file_bytes += len(csv_bytes)
        chunk_shas.append(chunk_sha)

        out = _stringify(chunk)
        out[META_INGESTED_AT] = ingested_at
        out[META_SOURCE_RUN_ID] = run_id
        out[META_SRC_SHA256] = chunk_sha  # per-chunk provenance
        overwrite = (n == 0 and fresh)    # fresh first chunk replaces; otherwise append

        ok, _chunks, _nrows, _ = write_pandas(
            conn, out, table_name=table, database=database, schema=schema,
            auto_create_table=True, overwrite=overwrite, quote_identifiers=False,
        )
        if not ok:
            raise RuntimeError(f"write_pandas reported failure on chunk {n + 1} of {table}.")

        if n == 0:
            columns = list(out.columns)
            sample = out.head(SAMPLE_ROWS).astype(str).to_dict(orient="records")
        appended += len(chunk)
        n += 1
        print(f"  chunk {n}: +{len(chunk):,} rows "
              f"(run {appended:,}, table {resume_from_row + appended:,})", flush=True)

        if max_rows and appended >= max_rows:
            print(f"  hit ONBOARD_CHUNK_MAX_ROWS={max_rows:,} -- stopping stream (cap).", flush=True)
            break

    if appended == 0 and resume_from_row == 0:
        raise RuntimeError(
            "Chunked fetch_data yielded no rows -- failing loudly (bad URL / parse / "
            "wrong format?)."
        )
    manifest_sha = hashlib.sha256("".join(chunk_shas).encode("utf-8")).hexdigest()
    return appended, manifest_sha, file_bytes, columns, sample


def _landing_count(conn, table: str) -> int:
    """Rows currently in the landing table (0 if it doesn't exist yet)."""
    fqt = f'"{settings.raw_database}"."{settings.raw_schema}"."{table}"'
    try:
        return int(snow.fetch_scalar(conn, f"SELECT COUNT(*) FROM {fqt}") or 0)
    except Exception:
        return 0


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _execute_fetch(config: dict, code: str, since: Optional[str] = None,
                   allow_empty: bool = False) -> Tuple[object, Optional[bytes], str]:
    """Run Claude-generated code and return (DataFrame, raw_bytes, source_file).

    ``since`` is the incremental high-water mark (or None) handed to the fetch as
    ``context["since"]`` so it can pull only newer records. ``allow_empty`` lets an
    incremental run that finds no new rows return cleanly (a no-op, not an error).

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
        "since": since,  # incremental high-water mark (or None on first/snapshot run)
        "env": dict(os.environ),
        "source_bytes": None,
        "source_file": "",
        # Headless-browser renderer (C1b). Generated scrape_js code calls
        # html = context["render"](url) to get fully-rendered HTML (JS executed,
        # bot-challenge cleared), then parses it with BeautifulSoup exactly like a
        # static page. Lazily imports Playwright -- no cost unless actually called.
        "render": browser.render,
    }
    df = fetch(context)
    if not hasattr(df, "columns"):
        raise RuntimeError("fetch_data must return a pandas.DataFrame.")
    if len(df) == 0:
        if allow_empty:
            return df, None, ""  # incremental: no new rows since the watermark
        raise RuntimeError("fetch_data returned 0 rows -- failing loudly (schema drift?).")

    raw_bytes = context.get("source_bytes")
    if raw_bytes is not None and not isinstance(raw_bytes, (bytes, bytearray)):
        raw_bytes = str(raw_bytes).encode("utf-8")

    _reject_html(df)  # a docs/landing page parsed AS data instead of the dataset
    return df, raw_bytes, context.get("source_file", "") or ""


def _reject_html(df) -> None:
    """Fail loudly when an HTML page lands AS DATA (a false "success").

    Judge the DataFrame's shape, NOT the raw bytes -- scrape sources legitimately
    fetch an HTML page (raw_bytes is HTML) but parse it into a proper multi-column
    table, which is fine. The failure we catch is when the HTML itself becomes the
    data: a docs/landing page parsed into a single bogus column (the
    fed_cms_hpt_enforcement case: one ``DOCTYPE_HTML`` column of junk rows).
    """
    cols = [str(c) for c in df.columns]
    if len(cols) != 1:
        return  # real tabular data (incl. legitimately-scraped tables)
    name = cols[0].upper()
    first = ""
    try:
        nonnull = df.iloc[:, 0].dropna()
        if len(nonnull):
            first = str(nonnull.iloc[0]).lstrip().upper()
    except Exception:
        first = ""
    if ("DOCTYPE" in name or "HTML" in name or name.startswith("<")
            or first.startswith(("<!DOCTYPE", "<HTML", "<"))):
        raise RuntimeError(
            f"fetch_data parsed HTML into a single column ('{df.columns[0]}'), not "
            "tabular data -- the fetch likely hit a docs/landing URL. Fix the URL/parse."
        )


def _stringify(df):
    """Coerce every source column to text (the raw landing convention)."""
    df = df.where(df.notna(), None)
    df.columns = [_sf_col(c) for c in df.columns]
    for col in df.columns:
        df[col] = df[col].map(lambda v: "" if v is None else str(v))
    return df


# Snowflake reserved words that are INVALID as unquoted identifiers. Landing
# columns are created unquoted (write_pandas quote_identifiers=False), so a source
# column literally named one of these (e.g. a portal "group"/"order"/"values"
# column) crashes the CREATE TABLE with "unexpected 'GROUP'". Prefix to dodge it.
# (Only columns that would otherwise FAIL are touched -- no working load regresses.)
_SF_RESERVED = frozenset({
    "ACCOUNT", "ALL", "ALTER", "AND", "ANY", "AS", "BETWEEN", "BY", "CASE", "CAST",
    "CHECK", "COLUMN", "CONNECT", "CONNECTION", "CONSTRAINT", "CREATE", "CROSS",
    "CURRENT", "CURRENT_DATE", "CURRENT_TIME", "CURRENT_TIMESTAMP", "CURRENT_USER",
    "DATABASE", "DELETE", "DISTINCT", "DROP", "ELSE", "EXISTS", "FALSE", "FOLLOWING",
    "FOR", "FROM", "FULL", "GRANT", "GROUP", "GSCLUSTER", "HAVING", "ILIKE", "IN",
    "INCREMENT", "INNER", "INSERT", "INTERSECT", "INTO", "IS", "ISSUE", "JOIN",
    "LATERAL", "LEFT", "LIKE", "LOCALTIME", "LOCALTIMESTAMP", "MINUS", "NATURAL",
    "NOT", "NULL", "OF", "ON", "OR", "ORDER", "ORGANIZATION", "QUALIFY", "REGEXP",
    "REVOKE", "RIGHT", "RLIKE", "ROW", "ROWS", "SAMPLE", "SCHEMA", "SELECT", "SET",
    "SOME", "START", "TABLE", "TABLESAMPLE", "THEN", "TO", "TRIGGER", "TRUE",
    "TRY_CAST", "UNION", "UNIQUE", "UPDATE", "USING", "VALUES", "VIEW", "WHEN",
    "WHENEVER", "WHERE", "WITH",
})


def _sf_col(name) -> str:
    """Sanitize to an unquoted, uppercase Snowflake identifier (matches LANDING)."""
    clean = re.sub(r"[^0-9A-Za-z_]+", "_", str(name)).strip("_") or "COL"
    if clean[0].isdigit():
        clean = "C_" + clean
    clean = clean.upper()
    if clean in _SF_RESERVED:
        clean = "C_" + clean
    return clean


def _df_bytes(df) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def _load_landing(conn, df, table: str, overwrite: bool = True) -> None:
    """Write the frame to the landing table.

    overwrite=True  -> snapshot-replace (the default, idempotent mirror).
    overwrite=False -> append (incremental; landing becomes an append log and
                       staging dedups to current-state-per-key).
    """
    from snowflake.connector.pandas_tools import write_pandas

    database, schema = settings.raw_database, settings.raw_schema
    snow.execute(conn, f'CREATE SCHEMA IF NOT EXISTS "{database}"."{schema}"')
    ok, _chunks, nrows, _ = write_pandas(
        conn, df, table_name=table, database=database, schema=schema,
        auto_create_table=True, overwrite=overwrite, quote_identifiers=False,
    )
    if not ok:
        raise RuntimeError(f"write_pandas reported failure loading {table}.")


def _watermark(conn, table: str, cursor_field: str) -> Optional[str]:
    """High-water mark = MAX(cursor_field) in the landing table.

    None if the table doesn't exist yet (first incremental run -> backfill). The
    cursor must be lexicographically orderable as TEXT (ISO date/timestamp), which
    is how the raw mirror stores everything; that covers date_received, record_date,
    created_at, etc. (For a numeric id cursor, recon should pick a date instead.)
    """
    col = _sf_col(cursor_field)
    fqt = f'"{settings.raw_database}"."{settings.raw_schema}"."{table}"'
    try:
        return snow.fetch_scalar(conn, f"SELECT MAX({col}) FROM {fqt}")
    except Exception:
        return None  # table not created yet


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
        f"LIBRARY_RAW.LANDING.{config['landing_table']} via the onboarding agent."
    )


def _utcnow() -> _dt.datetime:
    return _dt.datetime.now(_dt.timezone.utc)
