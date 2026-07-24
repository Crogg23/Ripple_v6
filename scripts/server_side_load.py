#!/usr/bin/env python3
"""Server-side bulk loader: Snowflake fetches the file, we never touch the bytes.

The companion to scripts/bridge_fuel_load.py for GB-scale sources that stall when
pulled through the laptop. Instead of downloading locally, this calls two Snowflake
stored procs (see infra/ddl/08_bulk_ingest.sql) that fetch + unzip on Snowflake's
OWN compute (cloud-to-cloud), then COPYs the staged file into the all-TEXT landing
table -- reusing the EXACT same ledger as every other load: the density gate
(ingest.assess_density), the INGEST_RUNS log (ingest._log_run), the SOURCE_REGISTRY
upsert (register via bridge_fuel_load._register), and the atomic staging swap
(loadkit.atomic_load). So a server-side load is first-class in the same freshness
ledger, indistinguishable downstream from a laptop-pulled one.

    python scripts/server_side_load.py --spec cfpb_complaints --run
    python scripts/server_side_load.py --list
    python scripts/server_side_load.py --spec all --run

Flow per spec (--run):
    1. CALL RIPPLE_FETCH_TO_STAGE(url, raw_stage_path)     -- stream URL -> stage
    2. if kind='zip': CALL RIPPLE_UNZIP_MEMBER_TO_STAGE     -- staged zip -> .gz
    3. INFER_SCHEMA the staged file header -> all-TEXT staging table + 3 stamp cols
    4. COPY INTO staging  (MATCH_BY_COLUMN_NAME; stamps via per-run column DEFAULTs)
    5. density gate on a head sample -> empty => drop staging, log 'empty', no register
    6. atomic swap staging -> live, then log 'success', then register LAST

Safe by default: previews (fetch + infer, no swap) unless --run; skips already-landed
unless --force.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from pathlib import Path

# Windows consoles default to cp1252; never let a print() crash the load.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # pragma: no cover
        pass

_REPO = Path(__file__).resolve().parents[1]
_LIB = _REPO / "library-onboarding"
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))
if str(_LIB) not in sys.path:
    sys.path.insert(0, str(_LIB))

try:
    from dotenv import load_dotenv

    load_dotenv(_LIB / ".env", override=True)
except Exception:  # pragma: no cover
    pass

import pandas as pd  # noqa: E402  (only used for the small density sample)

import ingest        # noqa: E402  library-onboarding/ingest.py
import snow          # noqa: E402  library-onboarding/snow.py
from config import settings  # noqa: E402
from loadkit import atomic_load  # noqa: E402

# Reuse bridge-fuel's registry upsert verbatim (same MERGE, same facet-clobber guard).
sys.path.insert(0, str(_REPO / "scripts"))
from bridge_fuel_load import _register, _registry_has_row  # noqa: E402

STAGE = "LIBRARY_RAW.LANDING.BULK_STAGE"


# --------------------------------------------------------------------------- #
# Specs: the GB-scale sources this path exists for. Only fields that differ
# from the defaults are set; everything else falls through to _register's cfg.
# --------------------------------------------------------------------------- #
def _load_specs() -> dict[str, dict]:
    import server_side_specs  # scripts/server_side_specs.py
    return {d["source_id"]: d for d in server_side_specs.SPECS}


# --------------------------------------------------------------------------- #
# Stage helpers
# --------------------------------------------------------------------------- #
def _basename_from_url(url: str) -> str:
    tail = url.split("?", 1)[0].rstrip("/").rsplit("/", 1)[-1]
    return tail or "download.bin"


def _stage_paths(s: dict, url: str) -> tuple[str, str]:
    """(raw_stage_path, copy_stage_path). For zip: copy path is the extracted .gz.
    For csv: fetch gzips on the fly (a big raw CSV overflows the fetch proc's /tmp
    sandbox), so both paths carry a .gz suffix -- the proc compresses to it and COPY
    reads the .gz natively. `url` is the RESOLVED download URL (may differ from
    s['url'] when a resolver hop is used), so the staged basename matches the fetch."""
    sid = s["source_id"].lower()
    if s.get("kind") == "zip":
        raw = f"bulk/{sid}/" + _basename_from_url(url)
        return raw, f"bulk/{sid}/{sid}.gz"
    raw = f"bulk/{sid}/" + _basename_from_url(url) + ".gz"
    return raw, raw


def _resolve_url(s: dict) -> str:
    """The effective download URL. Most sources return s['url'] unchanged; a source
    with a 'resolver' hop (e.g. GLEIF: a metadata API returns the real, rotating
    download link) fetches the small metadata doc client-side and extracts the link.

    resolver = {
      'url':  '<metadata endpoint>',
      'type': 'json' | 'regex'   (default 'json'),
      'path': 'a.b.0.c'  for json (dotted keys; ints index lists)  OR
              '<regex>'  for regex (capture group 1 is the URL),
    }
    The resolved host must ALSO be on the RIPPLE_BULK_EGRESS allow-list.
    """
    r = s.get("resolver")
    if not r:
        return s["url"]
    import requests
    resp = requests.get(r["url"], timeout=120, allow_redirects=True,
                        headers={"User-Agent": "Ripple resolver", "Accept": "application/json"})
    resp.raise_for_status()
    if r.get("type", "json") == "json":
        val = resp.json()
        for key in str(r["path"]).split("."):
            val = val[int(key)] if isinstance(val, list) else val[key]
        if not isinstance(val, str):
            raise RuntimeError(f"resolver json path {r['path']!r} did not resolve to a URL string")
        return val
    import re as _re
    m = _re.search(r["path"], resp.text)
    if not m:
        raise RuntimeError(f"resolver regex {r['path']!r} matched nothing at {r['url']}")
    return m.group(1)


def _call_json(conn, sql: str, params: tuple) -> dict:
    val = snow.fetch_scalar(conn, sql, params)
    try:
        return json.loads(val) if val else {}
    except Exception:
        return {"raw": val}


def _stage_md5(conn, stage_path: str) -> str:
    """MD5 of the staged file (change-detection fingerprint stored in the SHA256 col).
    LIST returns its rows directly to the cursor (cols: name, size, md5, last_modified);
    `FROM (LIST ...)` is NOT valid SQL, so read the cursor."""
    cur = conn.cursor()
    try:
        cur.execute(f"LIST '@{STAGE}/{stage_path}'")
        rows = cur.fetchall()
        cols = [d[0].lower() for d in cur.description]
        idx = cols.index("md5") if "md5" in cols else 2
        return rows[0][idx] if rows else ""
    except Exception:
        return ""
    finally:
        cur.close()


# --------------------------------------------------------------------------- #
# Schema + load
# --------------------------------------------------------------------------- #
def _rawline_format(conn) -> str:
    """Format that returns each physical line as a single field $1 (no delimiter
    splitting, no enclosure). COMPRESSION=AUTO handles .gz and plain files."""
    name = "LIBRARY_RAW.LANDING.BULK_FMT_RAWLINE"
    snow.execute(
        conn,
        f"CREATE OR REPLACE FILE FORMAT {name} TYPE=CSV "
        "FIELD_DELIMITER='\\u0001' RECORD_DELIMITER='\\n' COMPRESSION=AUTO "
        "FIELD_OPTIONALLY_ENCLOSED_BY=NONE ERROR_ON_COLUMN_COUNT_MISMATCH=FALSE "
        "REPLACE_INVALID_CHARACTERS=TRUE ENCODING='UTF8'")
    return name


def _load_format(conn, delimiter: str, skip_header: bool = True, enclosure: str = '"') -> str:
    """Named CSV format for the actual COPY: MULTI_LINE + ragged-row tolerance.
    Government CSVs carry embedded newlines/quotes in free-text fields (CFPB
    narratives), so MATCH_BY_COLUMN_NAME's strict header-vs-data count check -- and
    INFER_SCHEMA -- reject the file. Positional load with these tolerances is the
    raw-mirror path. skip_header=False for headerless files (synthesized C1..CN cols).

    enclosure: the field quote char (default '"'). Set falsy (spec enclosure=None/'')
    for TAB flat files that use NO enclosure but carry stray '"' in free-text (NHTSA
    complaint narratives) -- with an enclosure set, a lone quote makes Snowflake expect
    a delimiter after it and throw 'Found character X instead of field delimiter'.
    No enclosure => MULTI_LINE off (line boundaries can't be inferred without quotes)."""
    tag = {",": "COMMA", "|": "PIPE", "\t": "TAB", ";": "SEMI"}.get(delimiter, "CUSTOM")
    skip = 1 if skip_header else 0
    enc_on = bool(enclosure)
    enc_sql = "FIELD_OPTIONALLY_ENCLOSED_BY='\"'" if enc_on else "FIELD_OPTIONALLY_ENCLOSED_BY=NONE"
    multiline = "TRUE" if enc_on else "FALSE"
    name = (f"LIBRARY_RAW.LANDING.BULK_FMT_{tag}_LOAD"
            f"{'' if skip_header else '_NOHDR'}{'' if enc_on else '_NOENC'}")
    snow.execute(
        conn,
        f"CREATE OR REPLACE FILE FORMAT {name} TYPE=CSV "
        f"FIELD_DELIMITER='{delimiter}' SKIP_HEADER={skip} MULTI_LINE={multiline} "
        f"{enc_sql} TRIM_SPACE=FALSE "
        "REPLACE_INVALID_CHARACTERS=TRUE ENCODING='UTF8' "
        "ERROR_ON_COLUMN_COUNT_MISMATCH=FALSE EMPTY_FIELD_AS_NULL=FALSE")
    return name


def _derive_columns(conn, copy_path: str, delimiter: str, has_header: bool, enclosure: str = '"') -> list[str]:
    """Column names for the staging table, from the FIRST line of the staged file.

    INFER_SCHEMA can't handle ragged government CSVs (a single short data row makes
    it throw 'header defined N columns while data contains M'), so we read only the
    first line (raw, one field) and split it with csv.reader -- which handles the
    quoting. With a header: use the names. Headerless (has_header=False): count the
    fields and synthesize C1..CN. The first line carries no embedded newline, so
    this is safe."""
    import csv
    import io as _io
    cur = conn.cursor()
    try:
        cur.execute(
            f"SELECT $1 FROM '@{STAGE}/{copy_path}' "
            f"(FILE_FORMAT => '{_rawline_format(conn)}') LIMIT 1")
        row = cur.fetchone()
    finally:
        cur.close()
    if not row or row[0] is None:
        raise RuntimeError(f"could not read a first line from @{STAGE}/{copy_path}")
    if enclosure:
        fields = next(csv.reader(_io.StringIO(row[0]), delimiter=delimiter))
    else:
        fields = next(csv.reader(_io.StringIO(row[0]), delimiter=delimiter, quoting=csv.QUOTE_NONE))
    if not has_header:
        return [f"C{i + 1}" for i in range(len(fields))]
    # De-dupe collisions (some gov headers repeat a name) so the DDL is valid.
    seen, out = {}, []
    for nm in fields:
        nm = (nm or "").strip() or "COL"
        if nm in seen:
            seen[nm] += 1
            nm = f"{nm}_{seen[nm]}"
        else:
            seen[nm] = 0
        out.append(nm)
    return out


def _build_staging(conn, table: str, columns: list[str]) -> str:
    """CREATE OR REPLACE <TABLE>__STAGING: source cols all TEXT + the 3 provenance
    stamp cols (populated after COPY -- COPY MATCH_BY_COLUMN_NAME leaves unmatched
    table columns NULL, it does NOT apply column DEFAULTs, so we stamp via UPDATE)."""
    db, sc = settings.raw_database, settings.raw_schema
    stg = atomic_load.staging_name(table)
    fq = f'"{db}"."{sc}"."{stg}"'
    col_ddl = ",\n  ".join(f'"{c}" TEXT' for c in columns)
    ddl = (
        f"CREATE OR REPLACE TABLE {fq} (\n  {col_ddl},\n"
        f'  "{ingest.META_INGESTED_AT}" TIMESTAMP_NTZ,\n'
        f'  "{ingest.META_SOURCE_RUN_ID}" TEXT,\n'
        f'  "{ingest.META_SRC_SHA256}" TEXT\n)')
    snow.execute(conn, ddl)
    return stg


def _stamp_staging(conn, stg: str, run_id: str, started, sha: str) -> None:
    """Set the 3 provenance columns (identical for every row of a snapshot load).
    One UPDATE pass; the stamps then ride the atomic swap into the live table."""
    db, sc = settings.raw_database, settings.raw_schema
    ts = started.replace(tzinfo=None).isoformat(sep=" ", timespec="seconds")
    snow.execute(
        conn,
        f'UPDATE "{db}"."{sc}"."{stg}" SET '
        f'"{ingest.META_INGESTED_AT}" = %s::TIMESTAMP_NTZ, '
        f'"{ingest.META_SOURCE_RUN_ID}" = %s, "{ingest.META_SRC_SHA256}" = %s',
        (ts, run_id, sha))


def _copy_into_staging(conn, stg: str, copy_path: str, columns: list[str], load_fmt: str) -> int:
    """Positional COPY: file field i -> source column i (meta cols excluded from the
    list, so they stay NULL until _stamp_staging). Positional + the LOAD format's
    ragged-row tolerance is what survives messy government CSVs."""
    db, sc = settings.raw_database, settings.raw_schema
    fq = f'"{db}"."{sc}"."{stg}"'
    col_list = ", ".join(f'"{c}"' for c in columns)
    cur = conn.cursor()
    try:
        cur.execute(
            f"COPY INTO {fq} ({col_list}) FROM '@{STAGE}/{copy_path}' "
            f"FILE_FORMAT=(FORMAT_NAME='{load_fmt}') ON_ERROR=ABORT_STATEMENT")
        rows = cur.fetchall()
    finally:
        cur.close()
    # COPY returns one row per file: rows_loaded is col index 3.
    return sum(int(r[3]) for r in rows) if rows else 0


def _density_sample(conn, stg: str) -> pd.DataFrame:
    """Head sample of the staged rows (SOURCE cols only) for the density gate."""
    db, sc = settings.raw_database, settings.raw_schema
    meta = {ingest.META_INGESTED_AT, ingest.META_SOURCE_RUN_ID, ingest.META_SRC_SHA256}
    cur = conn.cursor()
    try:
        cur.execute(
            f'SELECT * FROM "{db}"."{sc}"."{stg}" LIMIT {ingest.DENSITY_SAMPLE_ROWS}')
        names = [d[0] for d in cur.description]
        data = cur.fetchall()
    finally:
        cur.close()
    df = pd.DataFrame(data, columns=names)
    return df[[c for c in df.columns if c not in meta]]


def _drop_staging(conn, stg: str) -> None:
    db, sc = settings.raw_database, settings.raw_schema
    try:
        snow.execute(conn, f'DROP TABLE IF EXISTS "{db}"."{sc}"."{stg}"')
    except Exception:
        pass


def _record_refresh_config(conn, s: dict, url: str, columns: list[str], has_header: bool) -> None:
    """Upsert the source's steady-state refresh config into BULK_REFRESH so the
    server-side RIPPLE_REFRESH_SOURCE proc + refresh TASK can re-pull it without the
    client (schema known => no header re-parse). resolver/keyed sources are marked
    NOT schedulable (they still need this client loader). ENABLED stays opt-in."""
    sid = s["source_id"]
    schedulable = not (s.get("resolver") or s.get("auth"))
    arr = "ARRAY_CONSTRUCT(" + ", ".join(
        "'" + str(c).replace("'", "''") + "'" for c in columns) + ")" if columns else "ARRAY_CONSTRUCT()"
    kind = s.get("kind", "csv")
    member = s.get("member_pattern", "")
    delim = s.get("delimiter", ",")
    cadence = s.get("update_cadence", "")
    snow.execute(
        conn,
        "MERGE INTO LIBRARY_META.REGISTRY.BULK_REFRESH t "
        "USING (SELECT %s AS SOURCE_ID, %s AS URL) src ON t.SOURCE_ID = src.SOURCE_ID "
        "WHEN MATCHED THEN UPDATE SET URL=src.URL, KIND=%s, MEMBER_PATTERN=%s, DELIMITER=%s, "
        f"HAS_HEADER=%s, COLUMNS={arr}, SCHEDULABLE=%s, CADENCE_BUCKET=%s, UPDATED_AT=CURRENT_TIMESTAMP() "
        "WHEN NOT MATCHED THEN INSERT (SOURCE_ID, URL, KIND, MEMBER_PATTERN, DELIMITER, HAS_HEADER, "
        f"COLUMNS, SCHEDULABLE, ENABLED, CADENCE_BUCKET) VALUES (src.SOURCE_ID, src.URL, %s, %s, %s, %s, {arr}, %s, FALSE, %s)",
        (sid, url,
         kind, member, delim, has_header, schedulable, cadence,
         kind, member, delim, has_header, schedulable, cadence))


# --------------------------------------------------------------------------- #
# Load one spec
# --------------------------------------------------------------------------- #
def _staged_exists(conn, path: str) -> bool:
    cur = conn.cursor()
    try:
        cur.execute(f"LIST '@{STAGE}/{path}'")
        return bool(cur.fetchall())
    except Exception:
        return False
    finally:
        cur.close()


def _finalize_table(conn, spec_for_register: dict, sid: str, table: str, stg: str,
                    n: int, run_id: str, started, sha: str, url: str,
                    min_rows: int | None = None) -> dict:
    """Shared tail for every land path (single/manifest/members/json): stamp the 3
    provenance cols, run the density gate, atomic-swap staging->live, log the run, and
    register LAST. min_rows overrides the density floor (json lands 1 VARIANT row/file)."""
    _stamp_staging(conn, stg, run_id, started, sha)
    sample = _density_sample(conn, stg)
    floor = ingest.DENSITY_MIN_ROWS if min_rows is None else min_rows
    density = ingest.assess_density(sample, min_rows=floor)
    ended = ingest._utcnow()
    if density["empty"]:
        _drop_staging(conn, stg)
        ingest._log_run(conn, sid, run_id, "empty", n, None, sha, url, started, ended,
                        f"EMPTY LOAD -- {density['reason']}. {ingest._density_note(density)}.")
        print(f"    EMPTY -- {density['reason']}; not registered.")
        return {"source_id": sid, "status": "empty", "rows": n}
    atomic_load.execute_swap(conn, table, database=settings.raw_database, schema=settings.raw_schema)
    ingest._log_run(conn, sid, run_id, "success", n, None, sha, url, started, ended,
                    f"{spec_for_register.get('name', sid)}. Server-side load of {n:,} rows. "
                    f"{ingest._density_note(density)}.")
    try:
        _register(conn, spec_for_register)
    except Exception as exc:
        exc._run_status_logged = True
        raise
    print(f"    LOADED {n:,} rows -> LIBRARY_RAW.LANDING.{table}; registered")
    return {"source_id": sid, "status": "loaded", "rows": n, "density": density["populated_fraction"]}


def _resolve_manifest(s: dict) -> list[str]:
    """UPGRADE 1: a manifest spec loads MANY files that share a schema and APPENDS them
    into ONE landing table. `manifest` is a static list of URLs, or a resolver dict:
      {'type':'json','url':...,'path':'a.b','item':'file','base':'https://host'}
      {'type':'regex','url':...,'path':'<regex w/ 1 capture group>','base':...}
    'base' is prefixed to relative hrefs. Resolved hosts must be on RIPPLE_BULK_EGRESS."""
    m = s["manifest"]
    if isinstance(m, list):
        return list(m)
    import requests
    r = requests.get(m["url"], timeout=180, allow_redirects=True,
                     headers={"User-Agent": "Ripple manifest", "Accept": "application/json"})
    r.raise_for_status()
    base = m.get("base", "")
    if m.get("type", "json") == "json":
        val = r.json()
        for key in (str(m["path"]).split(".") if m.get("path") else []):
            val = val[int(key)] if isinstance(val, list) else val[key]
        item = m.get("item")
        out = []
        for v in val:
            u = v.get(item) if (item and isinstance(v, dict)) else v
            if isinstance(u, str):
                out.append(base + u if (base and not u.startswith("http")) else u)
        return out
    import re as _re
    return [base + u if (base and not u.startswith("http")) else u
            for u in _re.findall(m["path"], r.text)]


def _load_manifest(s: dict, do_run: bool, force: bool, reuse_staged: bool, refresh: bool) -> dict:
    sid = s["source_id"]
    table = sid.upper()
    has_header = s.get("has_header", True)
    delim = s.get("delimiter", ",")
    enc = s.get("enclosure", '"')
    is_zip = s.get("kind") == "zip"
    urls = _resolve_manifest(s)
    print(f"\n=== {sid}  ({s.get('name','')}) ===  manifest: {len(urls)} files")
    if not urls:
        return {"source_id": sid, "status": "ERROR: manifest resolved to 0 files"}
    conn = snow.connect()
    try:
        if not force and not refresh and do_run and ingest._latest_success_sha(conn, sid) is not None:
            print("    already landed — skipping (use --force to reload)")
            return {"source_id": sid, "status": "skip (already landed)"}
        started = ingest._utcnow()
        run_id = str(uuid.uuid4())
        copy_paths = []
        for i, u in enumerate(urls):
            raw = f"bulk/{sid.lower()}/part_{i:04d}_{_basename_from_url(u)}" + ("" if is_zip else ".gz")
            cp = f"bulk/{sid.lower()}/part_{i:04d}.gz" if is_zip else raw
            if reuse_staged and _staged_exists(conn, cp):
                copy_paths.append(cp)
                continue
            _call_json(conn, f"CALL {settings.raw_database}.{settings.raw_schema}."
                       "RIPPLE_FETCH_TO_STAGE(%s, %s)", (u, raw))
            if is_zip:
                _call_json(conn, f"CALL {settings.raw_database}.{settings.raw_schema}."
                           "RIPPLE_UNZIP_MEMBER_TO_STAGE(%s, %s, %s)",
                           (raw, s.get("member_pattern", ""), cp))
            copy_paths.append(cp)
            if (i + 1) % 10 == 0:
                print(f"    fetched {i + 1}/{len(urls)} files")
        print(f"    fetched {len(copy_paths)} files to stage")
        columns = _derive_columns(conn, copy_paths[0], delim, has_header, enclosure=enc)
        print(f"    {'header' if has_header else 'headerless'}: {len(columns)} columns")
        if not do_run:
            print("    PREVIEW only (add --run to land)")
            return {"source_id": sid, "status": "preview", "cols": len(columns), "files": len(copy_paths)}
        load_fmt = _load_format(conn, delim, skip_header=has_header, enclosure=enc)
        stg = _build_staging(conn, table, columns)
        total = 0
        for cp in copy_paths:
            total += _copy_into_staging(conn, stg, cp, columns, load_fmt)
        print(f"    COPY -> staging {stg}: {total:,} rows from {len(copy_paths)} files")
        sha = f"manifest:{len(copy_paths)}:{_basename_from_url(urls[-1])}"
        try:
            res = _finalize_table(conn, s, sid, table, stg, total, run_id, started, sha, urls[0])
        except Exception as exc:
            if not getattr(exc, "_run_status_logged", False):
                ingest._log_run(conn, sid, run_id, "failed", None, None, sha, urls[0],
                                started, ingest._utcnow(), f"Manifest load failed: {str(exc)[:400]}")
            raise
        try:
            _record_refresh_config(conn, s, urls[0], columns, has_header)
        except Exception:
            pass
        return res
    finally:
        conn.close()


def _load_members(s: dict, do_run: bool, force: bool, reuse_staged: bool, refresh: bool) -> dict:
    """UPGRADE 2: one zip -> MANY per-member landing tables. `members` = list of
    {pattern, suffix, delimiter?, has_header?, enclosure?}. Fetch the zip once; for each
    member unzip -> derive -> staging <SID>_<SUFFIX> -> COPY -> finalize."""
    sid = s["source_id"]
    url = _resolve_url(s)
    raw = f"bulk/{sid.lower()}/" + _basename_from_url(url)
    members = s["members"]
    print(f"\n=== {sid}  ({s.get('name','')}) ===  {len(members)} members from one zip")
    conn = snow.connect()
    results = []
    try:
        if not (reuse_staged and _staged_exists(conn, raw)):
            f = _call_json(conn, f"CALL {settings.raw_database}.{settings.raw_schema}."
                           "RIPPLE_FETCH_TO_STAGE(%s, %s)", (url, raw))
            print(f"    fetched zip: bytes={f.get('bytes_downloaded')}")
        for m in members:
            msid = f"{sid}_{m['suffix']}"
            mtable = msid.upper()
            if not force and not refresh and do_run and ingest._latest_success_sha(conn, msid) is not None:
                print(f"    {msid}: already landed — skip")
                results.append({"source_id": msid, "status": "skip (already landed)"})
                continue
            started = ingest._utcnow()
            run_id = str(uuid.uuid4())
            cp = f"bulk/{sid.lower()}/{m['suffix'].lower()}.gz"
            unz = _call_json(conn, f"CALL {settings.raw_database}.{settings.raw_schema}."
                             "RIPPLE_UNZIP_MEMBER_TO_STAGE(%s, %s, %s)", (raw, m["pattern"], cp))
            delim = m.get("delimiter", s.get("delimiter", "\t"))
            hh = m.get("has_header", s.get("has_header", True))
            enc = m.get("enclosure", s.get("enclosure", '"'))
            cols = _derive_columns(conn, cp, delim, hh, enclosure=enc)
            print(f"    {msid}: member={unz.get('chosen_member')} {len(cols)} cols")
            if not do_run:
                results.append({"source_id": msid, "status": "preview", "cols": len(cols)})
                continue
            fmt = _load_format(conn, delim, skip_header=hh, enclosure=enc)
            stg = _build_staging(conn, mtable, cols)
            n = _copy_into_staging(conn, stg, cp, cols, fmt)
            spec_reg = {**s, "source_id": msid, "name": f"{s.get('name', sid)} - {m['suffix']}"}
            spec_reg.pop("members", None)
            sha = f"member:{m['suffix']}"
            try:
                results.append(_finalize_table(conn, spec_reg, msid, mtable, stg, n, run_id, started, sha, url))
            except Exception as exc:
                if not getattr(exc, "_run_status_logged", False):
                    ingest._log_run(conn, msid, run_id, "failed", None, None, sha, url,
                                    started, ingest._utcnow(), f"Member load failed: {str(exc)[:400]}")
                results.append({"source_id": msid, "status": f"ERROR: {str(exc)[:120]}"})
        total = sum(r.get("rows", 0) for r in results if r.get("status") == "loaded")
        return {"source_id": sid, "status": "loaded", "rows": total, "members": results}
    finally:
        conn.close()


def _json_format(conn) -> str:
    name = "LIBRARY_RAW.LANDING.BULK_FMT_JSON"
    snow.execute(conn, f"CREATE OR REPLACE FILE FORMAT {name} TYPE=JSON COMPRESSION=AUTO "
                 "STRIP_OUTER_ARRAY=FALSE")
    return name


def _build_variant_staging(conn, table: str) -> str:
    db, sc = settings.raw_database, settings.raw_schema
    stg = atomic_load.staging_name(table)
    fq = f'"{db}"."{sc}"."{stg}"'
    snow.execute(conn, f'CREATE OR REPLACE TABLE {fq} ("RAW" VARIANT, '
                 f'"{ingest.META_INGESTED_AT}" TIMESTAMP_NTZ, '
                 f'"{ingest.META_SOURCE_RUN_ID}" TEXT, "{ingest.META_SRC_SHA256}" TEXT)')
    return stg


def _copy_json(conn, stg: str, copy_path: str, fmt: str) -> int:
    db, sc = settings.raw_database, settings.raw_schema
    fq = f'"{db}"."{sc}"."{stg}"'
    cur = conn.cursor()
    try:
        cur.execute(f'COPY INTO {fq} ("RAW") FROM \'@{STAGE}/{copy_path}\' '
                    f"FILE_FORMAT=(FORMAT_NAME='{fmt}') ON_ERROR=ABORT_STATEMENT")
        rows = cur.fetchall()
    finally:
        cur.close()
    return sum(int(r[3]) for r in rows) if rows else 0


def _load_json(s: dict, do_run: bool, force: bool, reuse_staged: bool, refresh: bool) -> dict:
    """UPGRADE 3: openFDA-style zipped JSON -> a single-column RAW VARIANT table. Each
    .json.zip lands one VARIANT row (the whole doc; dbt flattens RAW:results downstream).
    Supports a manifest of parts (multi-part openFDA datasets) => one row per part."""
    sid = s["source_id"]
    table = sid.upper()
    urls = _resolve_manifest(s) if s.get("manifest") else [_resolve_url(s)]
    print(f"\n=== {sid}  ({s.get('name','')}) ===  json: {len(urls)} file(s)")
    conn = snow.connect()
    try:
        if not force and not refresh and do_run and ingest._latest_success_sha(conn, sid) is not None:
            print("    already landed — skipping (use --force)")
            return {"source_id": sid, "status": "skip (already landed)"}
        started = ingest._utcnow()
        run_id = str(uuid.uuid4())
        copy_paths = []
        for i, u in enumerate(urls):
            raw = f"bulk/{sid.lower()}/part_{i:04d}_{_basename_from_url(u)}"
            cp = f"bulk/{sid.lower()}/part_{i:04d}.json.gz"
            if reuse_staged and _staged_exists(conn, cp):
                copy_paths.append(cp)
                continue
            _call_json(conn, f"CALL {settings.raw_database}.{settings.raw_schema}."
                       "RIPPLE_FETCH_TO_STAGE(%s, %s)", (u, raw))
            # openFDA parts are .json.zip -> unzip the .json member to .gz for COPY
            _call_json(conn, f"CALL {settings.raw_database}.{settings.raw_schema}."
                       "RIPPLE_UNZIP_MEMBER_TO_STAGE(%s, %s, %s)", (raw, r"\.json$", cp))
            copy_paths.append(cp)
        print(f"    fetched {len(copy_paths)} json file(s)")
        if not do_run:
            print("    PREVIEW only (add --run to land)")
            return {"source_id": sid, "status": "preview", "files": len(copy_paths)}
        fmt = _json_format(conn)
        stg = _build_variant_staging(conn, table)
        total = 0
        for cp in copy_paths:
            total += _copy_json(conn, stg, cp, fmt)
        print(f"    COPY -> staging {stg}: {total:,} VARIANT row(s)")
        sha = f"json:{len(copy_paths)}"
        # json lands 1 VARIANT row per file; relax the density floor to 1
        return _finalize_table(conn, s, sid, table, stg, total, run_id, started, sha, urls[0], min_rows=1)
    finally:
        conn.close()


def _load_manifest_members(s: dict, do_run: bool, force: bool, reuse_staged: bool, refresh: bool) -> dict:
    """UPGRADE 4: manifest + members combo — iterate MANY zips, extract named members
    from each, APPEND per member type across all zips into N landing tables.
    Use case: SEC insider quarterly zips (35 zips x 4 members each)."""
    sid = s["source_id"]
    members = s["members"]
    urls = _resolve_manifest(s)
    print(f"\n=== {sid}  ({s.get('name','')}) ===  manifest+members: {len(urls)} zips x {len(members)} members")
    if not urls:
        return {"source_id": sid, "status": "ERROR: manifest resolved to 0 files"}
    conn = snow.connect()
    results = []
    try:
        started = ingest._utcnow()
        run_id = str(uuid.uuid4())
        # Per-member accumulators: {suffix: [copy_paths]}
        member_paths = {m["suffix"]: [] for m in members}
        member_cols = {}  # derived from first zip's members

        # Phase 1: fetch all zips and extract all members to stage
        for i, u in enumerate(urls):
            raw = f"bulk/{sid.lower()}/zip_{i:04d}_{_basename_from_url(u)}"
            if not (reuse_staged and _staged_exists(conn, raw)):
                _call_json(conn, f"CALL {settings.raw_database}.{settings.raw_schema}."
                           "RIPPLE_FETCH_TO_STAGE(%s, %s)", (u, raw))
            for m in members:
                cp = f"bulk/{sid.lower()}/zip_{i:04d}_{m['suffix'].lower()}.gz"
                if reuse_staged and _staged_exists(conn, cp):
                    member_paths[m["suffix"]].append(cp)
                    continue
                _call_json(conn, f"CALL {settings.raw_database}.{settings.raw_schema}."
                           "RIPPLE_UNZIP_MEMBER_TO_STAGE(%s, %s, %s)", (raw, m["pattern"], cp))
                member_paths[m["suffix"]].append(cp)
            if (i + 1) % 5 == 0:
                print(f"    fetched+extracted {i + 1}/{len(urls)} zips")
        print(f"    fetched all {len(urls)} zips, extracted {sum(len(v) for v in member_paths.values())} member files")

        # Derive columns from the first zip's members
        for m in members:
            paths = member_paths[m["suffix"]]
            if not paths:
                continue
            delim = m.get("delimiter", s.get("delimiter", "\t"))
            hh = m.get("has_header", s.get("has_header", True))
            enc = m.get("enclosure", s.get("enclosure", '"'))
            member_cols[m["suffix"]] = _derive_columns(conn, paths[0], delim, hh, enclosure=enc)
            print(f"    {m['suffix']}: {len(member_cols[m['suffix']])} cols from first file")

        if not do_run:
            for m in members:
                results.append({"source_id": f"{sid}_{m['suffix']}", "status": "preview",
                                "cols": len(member_cols.get(m["suffix"], [])),
                                "files": len(member_paths[m["suffix"]])})
            return {"source_id": sid, "status": "preview", "members": results}

        # Phase 2: COPY all member files into per-member staging tables, then finalize each
        for m in members:
            msid = f"{sid}_{m['suffix']}"
            mtable = msid.upper()
            paths = member_paths[m["suffix"]]
            if not paths:
                results.append({"source_id": msid, "status": "skip (no files)"})
                continue
            if not force and not refresh and ingest._latest_success_sha(conn, msid) is not None:
                print(f"    {msid}: already landed — skip")
                results.append({"source_id": msid, "status": "skip (already landed)"})
                continue
            m_started = ingest._utcnow()
            m_run_id = str(uuid.uuid4())
            delim = m.get("delimiter", s.get("delimiter", "\t"))
            hh = m.get("has_header", s.get("has_header", True))
            enc = m.get("enclosure", s.get("enclosure", '"'))
            cols = member_cols[m["suffix"]]
            fmt = _load_format(conn, delim, skip_header=hh, enclosure=enc)
            stg = _build_staging(conn, mtable, cols)
            total = 0
            for cp in paths:
                total += _copy_into_staging(conn, stg, cp, cols, fmt)
            print(f"    {msid}: COPY {total:,} rows from {len(paths)} files -> staging {stg}")
            spec_reg = {**s, "source_id": msid, "name": f"{s.get('name', sid)} - {m['suffix']}"}
            spec_reg.pop("members", None)
            spec_reg.pop("manifest", None)
            sha = f"manifest_members:{len(paths)}:{m['suffix']}"
            try:
                results.append(_finalize_table(conn, spec_reg, msid, mtable, stg, total, m_run_id, m_started, sha, urls[0]))
            except Exception as exc:
                if not getattr(exc, "_run_status_logged", False):
                    ingest._log_run(conn, msid, m_run_id, "failed", None, None, sha, urls[0],
                                    m_started, ingest._utcnow(), f"Manifest+member load failed: {str(exc)[:400]}")
                results.append({"source_id": msid, "status": f"ERROR: {str(exc)[:120]}"})
        total_rows = sum(r.get("rows", 0) for r in results if r.get("status") == "loaded")
        return {"source_id": sid, "status": "loaded", "rows": total_rows, "members": results}
    finally:
        conn.close()


def load_spec(s: dict, do_run: bool = False, force: bool = False,
              reuse_staged: bool = False, refresh: bool = False) -> dict:
    if s.get("members") and s.get("manifest"):
        return _load_manifest_members(s, do_run, force, reuse_staged, refresh)
    if s.get("members"):
        return _load_members(s, do_run, force, reuse_staged, refresh)
    if s.get("manifest"):
        return _load_manifest(s, do_run, force, reuse_staged, refresh)
    if s.get("kind") == "json":
        return _load_json(s, do_run, force, reuse_staged, refresh)
    sid = s["source_id"]
    table = sid.upper()
    url = _resolve_url(s)              # resolver hop (GLEIF etc.) or s['url'] unchanged
    has_header = s.get("has_header", True)
    raw_path, copy_path = _stage_paths(s, url)
    print(f"\n=== {sid}  ({s.get('name','')}) ===")
    print(f"    {url}  [kind={s.get('kind','csv')}, header={has_header}]")

    conn = snow.connect()
    try:
        if not force and not refresh and do_run and ingest._latest_success_sha(conn, sid) is not None:
            print("    already landed — skipping (use --force to reload, --refresh to check for changes)")
            return {"source_id": sid, "status": "skip (already landed)"}

        started = ingest._utcnow()
        run_id = str(uuid.uuid4())
        fetched = {}

        # 1+2. FETCH (+ UNZIP) server-side, unless the file is already staged and
        # --reuse-staged is set (resume a load without re-pulling GBs).
        if reuse_staged and _staged_exists(conn, copy_path):
            print(f"    reusing already-staged file @{STAGE}/{copy_path} (no re-fetch)")
        else:
            auth = s.get("auth")
            if auth:
                # Keyed fetch: inject the RIPPLE_API_KEY secret as a header or query
                # param (closes the auth-key gap for public APIs like data.gov).
                fetched = _call_json(
                    conn, f"CALL {settings.raw_database}.{settings.raw_schema}."
                    "RIPPLE_FETCH_TO_STAGE_KEYED(%s, %s, %s, %s)",
                    (url, raw_path, auth.get("style", "query"), auth.get("param", "api_key")))
            else:
                fetched = _call_json(
                    conn, f"CALL {settings.raw_database}.{settings.raw_schema}."
                    "RIPPLE_FETCH_TO_STAGE(%s, %s)", (url, raw_path))
            print(f"    fetched: http={fetched.get('http_status')} "
                  f"bytes={fetched.get('bytes_downloaded'):,}"
                  if fetched.get("bytes_downloaded") else f"    fetched: {fetched}")
            if s.get("kind") == "zip":
                unz = _call_json(
                    conn, f"CALL {settings.raw_database}.{settings.raw_schema}."
                    "RIPPLE_UNZIP_MEMBER_TO_STAGE(%s, %s, %s)",
                    (raw_path, s.get("member_pattern", ""), copy_path))
                print(f"    unzipped: member={unz.get('chosen_member')} "
                      f"gz_bytes={unz.get('gz_bytes')}")

        # 3. Column names from the first line (parsed in Python; INFER_SCHEMA
        #    chokes on ragged government CSVs). Headerless => synthesized C1..CN.
        delim = s.get("delimiter", ",")
        enc = s.get("enclosure", '"')
        columns = _derive_columns(conn, copy_path, delim, has_header, enclosure=enc)
        print(f"    {'header' if has_header else 'headerless'}: {len(columns)} columns: "
              f"{', '.join(columns[:15])}{' ...' if len(columns) > 15 else ''}")
        if not do_run:
            print("    PREVIEW only (add --run to land)")
            return {"source_id": sid, "status": "preview", "cols": len(columns)}

        # Change-detection fingerprint = the ORIGIN server's ETag/Last-Modified
        # (stable across re-fetches). NOT the stage md5: internal-stage files are
        # encrypted, so their md5 changes every upload even for identical content.
        # Fall back to stage md5 only when the origin gives neither (weaker).
        sha = (fetched.get("etag") or fetched.get("last_modified")
               or _stage_md5(conn, raw_path) or _stage_md5(conn, copy_path))
        # Cost discipline (Phase 4): on --refresh, if the fetched file's content is
        # unchanged since the last success, skip the expensive COPY + swap + re-store.
        if refresh:
            prior = ingest._latest_success_sha(conn, sid)
            if sha and prior and sha == prior:
                print(f"    unchanged since last load (sha {sha[:12]}…) — skipping COPY/re-store")
                return {"source_id": sid, "status": "skip (unchanged)"}
        load_fmt = _load_format(conn, delim, skip_header=has_header, enclosure=enc)

        # 4. staging + positional COPY + stamp
        try:
            stg = _build_staging(conn, table, columns)
            n = _copy_into_staging(conn, stg, copy_path, columns, load_fmt)
            _stamp_staging(conn, stg, run_id, started, sha)
            print(f"    COPY -> staging {stg}: {n:,} rows (stamped)")

            # 5. density gate (snapshot => min_rows floor, like bridge_fuel)
            sample = _density_sample(conn, stg)
            density = ingest.assess_density(sample, min_rows=ingest.DENSITY_MIN_ROWS)
            ended = ingest._utcnow()
            if density["empty"]:
                _drop_staging(conn, stg)
                ingest._log_run(conn, sid, run_id, "empty", n, fetched.get("target_size"),
                                sha, url, started, ended,
                                f"EMPTY LOAD -- {density['reason']}. "
                                f"{ingest._density_note(density)}. Server-side COPY of {n:,} rows "
                                f"into staging {stg} but no real data; staging dropped, live "
                                f"{table} untouched, NOT registered.")
                print(f"    EMPTY -- {density['reason']}; logged 'empty', not registered.")
                return {"source_id": sid, "status": "empty", "rows": n,
                        "density": density["populated_fraction"]}

            # 6. atomic swap, THEN success, THEN register LAST
            atomic_load.execute_swap(conn, table, database=settings.raw_database,
                                     schema=settings.raw_schema)
            ingest._log_run(conn, sid, run_id, "success", n, fetched.get("target_size"),
                            sha, url, started, ended,
                            f"{s.get('name', sid)}. Server-side bulk load of {n:,} rows "
                            f"(fetch->stage->COPY->atomic swap). {ingest._density_note(density)}.")
            try:
                _register(conn, s)
            except Exception as exc:
                exc._run_status_logged = True
                raise
            try:
                _record_refresh_config(conn, s, url, columns, has_header)
            except Exception as e:  # noqa: BLE001  never fail a good load over the control row
                print(f"    (refresh-config record skipped: {str(e)[:100]})")
            print(f"    LOADED {n:,} rows -> LIBRARY_RAW.LANDING.{table}; registered")
            return {"source_id": sid, "status": "loaded", "rows": n,
                    "density": density["populated_fraction"]}
        except Exception as exc:
            if not getattr(exc, "_run_status_logged", False):
                try:
                    ingest._log_run(conn, sid, run_id, "failed", None,
                                    fetched.get("target_size"), sha,
                                    url, started, ingest._utcnow(),
                                    f"Server-side load failed: {str(exc)[:500]}")
                except Exception:
                    pass
            raise
    finally:
        conn.close()


def _run_one(s: dict, args) -> dict:
    try:
        return load_spec(s, do_run=args.run, force=args.force,
                         reuse_staged=args.reuse_staged, refresh=args.refresh)
    except Exception as e:  # noqa: BLE001
        print(f"    [{s['source_id']}] ERROR: {str(e)[:200]}")
        return {"source_id": s["source_id"], "status": f"ERROR: {str(e)[:120]}"}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Server-side bulk loader (Snowflake fetches the file)")
    ap.add_argument("--spec", help="source_id, comma-list, or 'all'")
    ap.add_argument("--list", action="store_true", help="list known specs")
    ap.add_argument("--run", action="store_true", help="actually land (default previews)")
    ap.add_argument("--force", action="store_true", help="reload even if already landed")
    ap.add_argument("--reuse-staged", action="store_true",
                    help="skip fetch/unzip if the file is already on BULK_STAGE "
                         "(resume a load without re-pulling GBs)")
    ap.add_argument("--refresh", action="store_true",
                    help="re-fetch even if already landed, but skip the COPY/re-store "
                         "when the file content is unchanged (SHA match) - cheap refresh")
    args = ap.parse_args(argv)

    try:
        specs = _load_specs()
    except Exception as e:  # noqa: BLE001
        print(f"(no server_side_specs module yet: {e})")
        specs = {}

    if args.list or not args.spec:
        print("Known server-side specs:")
        for k, v in specs.items():
            print(f"  {k:28} kind={v.get('kind','csv'):4} {v.get('name','')[:60]}")
        return 0

    if args.spec == "all":
        targets = list(specs.values())
    else:
        ids = [x.strip() for x in args.spec.split(",") if x.strip()]
        missing = [i for i in ids if i not in specs]
        if missing:
            raise SystemExit(f"unknown spec(s): {missing}. known: {list(specs)}")
        targets = [specs[i] for i in ids]

    results = [_run_one(s, args) for s in targets]
    landed = [r for r in results if r.get("status") == "loaded"]
    errored = [r for r in results if str(r.get("status", "")).startswith("ERROR")]
    print(f"\n{len(landed)}/{len(results)} loaded, "
          f"{sum(r.get('rows', 0) for r in landed):,} rows."
          + (f" {len(errored)} errored: {[r['source_id'] for r in errored]}" if errored else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
