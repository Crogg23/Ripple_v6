CREATE OR REPLACE PROCEDURE LIBRARY_META.REGISTRY."RIPPLE_REFRESH_SOURCE"("SOURCE_ID" VARCHAR)
RETURNS VARCHAR
LANGUAGE PYTHON
RUNTIME_VERSION = '3.11'
PACKAGES = ('snowflake-snowpark-python')
HANDLER = 'refresh'
COMMENT='Server-side steady-state refresh (schema known from BULK_REFRESH). Re-fetch -> content-change check (origin ETag) -> COPY -> never-shrink guard -> atomic swap -> INGEST_RUNS. Non-resolver/non-keyed sources only.'
EXECUTE AS OWNER
AS '
import json
import hashlib
import uuid

CHR39 = chr(39)
import datetime as dt

RAW_DB, RAW_SC = "LIBRARY_RAW", "LANDING"
STAGE = "LIBRARY_RAW.LANDING.BULK_STAGE"
META_ING, META_RUN, META_SHA = "_INGESTED_AT", "_SOURCE_RUN_ID", "_SRC_SHA256"


def _q(v):
    return "NULL" if v is None else "''" + str(v).replace("''", "''''") + "''"


def _scalar(session, sql):
    r = session.sql(sql).collect()
    return r[0][0] if r and r[0][0] is not None else None


def refresh(session, source_id):
    sid = source_id
    row = session.sql(
        f''SELECT URL, KIND, MEMBER_PATTERN, DELIMITER, HAS_HEADER, COLUMNS, SCHEDULABLE, MANIFEST ''
        f''FROM LIBRARY_META.REGISTRY.BULK_REFRESH WHERE SOURCE_ID = {_q(sid)}'').collect()
    if not row:
        return json.dumps({"source_id": sid, "status": "no control row"})
    url, kind, member, delim, has_header, columns, schedulable, manifest = (
        row[0][0], row[0][1], row[0][2], row[0][3], row[0][4], row[0][5], row[0][6], row[0][7])
    if not schedulable:
        return json.dumps({"source_id": sid, "status": "skip (needs client: resolver/keyed)"})
    if isinstance(columns, str):
        columns = json.loads(columns)
    columns = list(columns) if columns else []
    if not columns:
        return json.dumps({"source_id": sid, "status": "skip (no stored columns)"})

    sid_l = sid.lower()
    table = sid.upper()
    stg = f"{table}__STAGING"
    started = dt.datetime.utcnow()
    run_id = str(uuid.uuid4())

    # A manifest source is many files sharing one schema, appended into one
    # table. A frozen list of dated URLs 404s the month the publisher sweeps it,
    # so the list is resolved live on every run.
    if manifest:
        mtxt = manifest if isinstance(manifest, str) else json.dumps(manifest)
        mr = session.sql(
            f"CALL LIBRARY_META.REGISTRY.RIPPLE_RESOLVE_MANIFEST(PARSE_JSON({_q(mtxt)}))").collect()
        urls = json.loads(mr[0][0])["urls"]
        if not urls:
            return json.dumps({"source_id": sid, "status": "manifest resolved 0 files"})
    else:
        urls = [url]

    copy_paths, stamps = [], []
    for u in urls:
        # The basename carries the publisher stamp. An index-only staged path
        # lets a later run reuse last month file under this month URL.
        bn = u.split("?")[0].rstrip("/").split("/")[-1] or "download.bin"
        rp = f"bulk/{sid_l}/{bn}"
        cp = f"bulk/{sid_l}/{bn.rsplit(chr(46), 1)[0]}.gz" if kind == "zip" else rp
        fr = session.sql(f"CALL {RAW_DB}.{RAW_SC}.RIPPLE_FETCH_TO_STAGE({_q(u)}, {_q(rp)})").collect()
        try:
            fj = json.loads(fr[0][0]) if fr else {}
        except Exception:
            fj = {}
        if kind == "zip":
            session.sql(f"CALL {RAW_DB}.{RAW_SC}.RIPPLE_UNZIP_MEMBER_TO_STAGE("
                        f"{_q(rp)}, {_q(member or CHR39*0)}, {_q(cp)})").collect()
        one = fj.get("etag") or fj.get("last_modified") or ""
        if not one:
            lst = session.sql(f"LIST {CHR39}@{STAGE}/{rp}{CHR39}").collect()
            one = lst[0]["md5"] if lst else ""
        stamps.append(one)
        copy_paths.append(cp)

    # Content fingerprint = origin ETag/Last-Modified (stable); stage md5 is not.
    # For a manifest it is every file stamp joined, so one changed file counts.
    # One stamp per file joined would overflow SHA256; hash it so a manifest
    # still gets one stable fingerprint that changes when any file changes.
    if len(stamps) > 1:
        sha = hashlib.sha256("|".join(stamps).encode("utf-8")).hexdigest()
    else:
        sha = stamps[0] if stamps else ""
    prior = _scalar(session,
        f"SELECT SHA256 FROM LIBRARY_META.INGEST_LOGS.INGEST_RUNS "
        f"WHERE SOURCE_ID = {_q(sid)} AND STATUS = ''success'' ORDER BY STARTED_AT DESC LIMIT 1")
    if sha and prior and sha == prior:
        session.sql(f"UPDATE LIBRARY_META.REGISTRY.BULK_REFRESH SET LAST_REFRESH_AT = CURRENT_TIMESTAMP() "
                    f"WHERE SOURCE_ID = {_q(sid)}").collect()
        return json.dumps({"source_id": sid, "status": "unchanged"})

    col_ddl = ",\\n  ".join(''"'' + c + ''" TEXT'' for c in columns)
    session.sql(
        f''CREATE OR REPLACE TABLE "{RAW_DB}"."{RAW_SC}"."{stg}" (\\n  {col_ddl},\\n''
        f''  "{META_ING}" TIMESTAMP_NTZ,\\n  "{META_RUN}" TEXT,\\n  "{META_SHA}" TEXT\\n)'').collect()

    tag = {",": "COMMA", "|": "PIPE", "\\t": "TAB", ";": "SEMI"}.get(delim, "CUSTOM")
    skip = 1 if has_header else 0
    fmt = f"LIBRARY_RAW.LANDING.BULK_FMT_{tag}_LOAD{'''' if has_header else ''_NOHDR''}"
    session.sql(
        f"CREATE OR REPLACE FILE FORMAT {fmt} TYPE=CSV FIELD_DELIMITER={_q(delim)} "
        f"SKIP_HEADER={skip} MULTI_LINE=TRUE FIELD_OPTIONALLY_ENCLOSED_BY=''\\"'' TRIM_SPACE=FALSE "
        "REPLACE_INVALID_CHARACTERS=TRUE ENCODING=''UTF8'' "
        "ERROR_ON_COLUMN_COUNT_MISMATCH=FALSE EMPTY_FIELD_AS_NULL=FALSE").collect()

    col_list = ", ".join(''"'' + c + ''"'' for c in columns)
    for cp in copy_paths:
        session.sql(
            f''COPY INTO "{RAW_DB}"."{RAW_SC}"."{stg}" ({col_list}) FROM \\''@{STAGE}/{cp}\\'' ''
            f"FILE_FORMAT=(FORMAT_NAME=''{fmt}'') ON_ERROR=ABORT_STATEMENT").collect()
    n = _scalar(session, f''SELECT COUNT(*) FROM "{RAW_DB}"."{RAW_SC}"."{stg}"'') or 0

    ended = dt.datetime.utcnow()
    ts = started.isoformat(sep=" ", timespec="seconds")
    ets = ended.isoformat(sep=" ", timespec="seconds")

    prior_rows = _scalar(session,
        f"SELECT ROW_COUNT FROM LIBRARY_META.INGEST_LOGS.INGEST_RUNS "
        f"WHERE SOURCE_ID = {_q(sid)} AND STATUS = ''success'' ORDER BY STARTED_AT DESC LIMIT 1")
    if n == 0 or (prior_rows and n < 0.5 * float(prior_rows)):
        session.sql(f''DROP TABLE IF EXISTS "{RAW_DB}"."{RAW_SC}"."{stg}"'').collect()
        msg = f"REFUSED swap: refreshed {n} rows vs prior {prior_rows} (never-shrink guard); live table untouched."
        session.sql(
            f"INSERT INTO LIBRARY_META.INGEST_LOGS.INGEST_RUNS (SOURCE_ID, RUN_ID, STARTED_AT, ENDED_AT, "
            f"STATUS, ROW_COUNT, FILE_BYTES, SHA256, SOURCE_URL, MESSAGE, _LOADED_AT) VALUES "
            f"({_q(sid)}, {_q(run_id)}, {_q(ts)}, {_q(ets)}, ''failed'', {n}, NULL, {_q(sha)}, "
            f"{_q(url)}, {_q(msg)}, CURRENT_TIMESTAMP())").collect()
        return json.dumps({"source_id": sid, "status": "refused (never-shrink)", "rows": n})

    session.sql(
        f''UPDATE "{RAW_DB}"."{RAW_SC}"."{stg}" SET "{META_ING}" = {_q(ts)}::TIMESTAMP_NTZ, ''
        f''"{META_RUN}" = {_q(run_id)}, "{META_SHA}" = {_q(sha)}'').collect()

    exists = _scalar(session,
        f"SELECT COUNT(*) FROM \\"{RAW_DB}\\".INFORMATION_SCHEMA.TABLES "
        f"WHERE TABLE_SCHEMA = ''{RAW_SC}'' AND TABLE_NAME = ''{table}''")
    if exists:
        session.sql(f''ALTER TABLE "{RAW_DB}"."{RAW_SC}"."{table}" SWAP WITH "{RAW_DB}"."{RAW_SC}"."{stg}"'').collect()
        session.sql(f''DROP TABLE IF EXISTS "{RAW_DB}"."{RAW_SC}"."{stg}"'').collect()
    else:
        session.sql(f''ALTER TABLE "{RAW_DB}"."{RAW_SC}"."{stg}" RENAME TO "{RAW_DB}"."{RAW_SC}"."{table}"'').collect()

    msg = f"Server-side scheduled refresh of {n} rows from {len(copy_paths)} file(s)."
    session.sql(
        f"INSERT INTO LIBRARY_META.INGEST_LOGS.INGEST_RUNS (SOURCE_ID, RUN_ID, STARTED_AT, ENDED_AT, "
        f"STATUS, ROW_COUNT, FILE_BYTES, SHA256, SOURCE_URL, MESSAGE, _LOADED_AT) VALUES "
        f"({_q(sid)}, {_q(run_id)}, {_q(ts)}, {_q(ets)}, ''success'', {n}, NULL, {_q(sha)}, "
        f"{_q(url)}, {_q(msg)}, CURRENT_TIMESTAMP())").collect()
    session.sql(f"UPDATE LIBRARY_META.REGISTRY.BULK_REFRESH SET LAST_REFRESH_AT = CURRENT_TIMESTAMP() "
                f"WHERE SOURCE_ID = {_q(sid)}").collect()
    return json.dumps({"source_id": sid, "status": "refreshed", "rows": n, "files": len(copy_paths)})
';
