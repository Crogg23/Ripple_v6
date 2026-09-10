#!/usr/bin/env python3
"""Fast path for the big CMS year-series files: gzip parts, PUT, one COPY INTO.

Why this exists (2026-09-09): bridge_fuel_load lands through 500k-row pandas
chunks and measured ~6 min per million rows. The Part D drug file is 25M rows a
year, twelve years. The ARCOS and 2026-07-23 Part D loads proved the other path:
PUT gzip parts to a stage, one COPY INTO, 25M rows in about 3 minutes.

Same contract as bridge_fuel: all columns TEXT, three provenance stamps with the
same names and types, staging table + atomic swap, INGEST_RUNS row, registry
row, dbt scaffold, connect wiring. Only the transport differs.

Steps per file:
  1. stream-download to .scratch/cms_years/<SID>.csv (skip if size matches)
  2. read it with the csv module (quoted newlines safe), write gzip parts of
     PART_ROWS rows, no header, count rows, sha256 the source bytes
  3. CREATE <TABLE>__STAGING (cols from header, key col renamed to NPI)
  4. CREATE STAGE, PUT parts, COPY INTO staging, check rows_loaded == counted
  5. atomic swap, log success, register, lifecycle
  6. delete local files

    python scripts/cms_years_fast_load.py --families PARTB_PROVIDER_SERVICE,PARTD_PRESCRIBER_DRUG
    python scripts/cms_years_fast_load.py --sid FED_CMS_PARTD_PRESCRIBER_DRUG_DY2013 --run
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import gzip
import hashlib
import os
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

_REPO = Path(__file__).resolve().parents[1]
_LIB = _REPO / "library-onboarding"
for p in (_REPO, _REPO / "scripts", _LIB):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
try:
    from dotenv import load_dotenv
    load_dotenv(_LIB / ".env", override=True)
except Exception:  # pragma: no cover
    pass

import ingest  # noqa: E402
import snow  # noqa: E402
import _bulk_load_utils as bulk  # noqa: E402
import bridge_fuel_load as bf  # noqa: E402  reuse _register, _has_success
import sprint_cms_years_specs as SPECMOD  # noqa: E402
from config import settings  # noqa: E402
from loadkit import atomic_load  # noqa: E402

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

UA = {"User-Agent": "Ripple-Library/1.0 (data onboarding; w.rogers9999@gmail.com)"}
SCRATCH = _REPO / ".scratch" / "cms_years"
SCRATCH.mkdir(parents=True, exist_ok=True)
PART_ROWS = 1_500_000          # ~300-400 MB uncompressed per part, ~20 parts on the big file
PUT_PARALLEL = 8               # --put-parallel; lower it to leave upstream headroom
MAX_MBPS = 0.0                 # --max-mbps download cap, 0 = no cap
csv.field_size_limit(1 << 30)


def log(msg: str) -> None:
    line = f"{dt.datetime.now():%H:%M:%S}  {msg}"
    print(line, flush=True)
    with open(SCRATCH / "fast.log", "a", encoding="utf-8") as f:
        f.write(f"{dt.datetime.now():%Y-%m-%d} {line}\n")


# ---------------------------------------------------------------- download
def download(url: str, dest: Path, tries: int = 6) -> int:
    """Stream to disk with Range resume. Skip if the file is already there at the
    server's size. A stall (no bytes for 120 s) or a dropped socket resumes from
    the .part size instead of starting over; CMS answers Range with 206."""
    tmp = dest.with_suffix(".part")
    last = None
    for attempt in range(1, tries + 1):
        try:
            have = tmp.stat().st_size if tmp.exists() else 0
            hdr = dict(UA)
            if have:
                hdr["Range"] = f"bytes={have}-"
            with requests.get(url, headers=hdr, stream=True, timeout=(30, 120)) as r:
                if have and r.status_code == 206:
                    total = have + int(r.headers.get("Content-Length") or 0)
                    mode = "ab"
                elif r.status_code == 200:
                    total = int(r.headers.get("Content-Length") or 0)
                    have, mode = 0, "wb"
                else:
                    r.raise_for_status()
                    raise RuntimeError(f"unexpected status {r.status_code}")
                if dest.exists() and total and dest.stat().st_size == total:
                    log(f"    download cached ({total/1e9:.2f} GB)")
                    return total
                if have and have == total:
                    pass
                else:
                    if have:
                        log(f"    resuming at {have/1e9:.2f} of {total/1e9:.2f} GB (try {attempt})")
                    n = have
                    t_start = time.time()
                    got = 0
                    with open(tmp, mode) as f:
                        for block in r.iter_content(1 << 20):
                            if block:
                                f.write(block)
                                n += len(block)
                                got += len(block)
                                if MAX_MBPS:
                                    ahead = got / (MAX_MBPS * 1e6) - (time.time() - t_start)
                                    if ahead > 0:
                                        time.sleep(ahead)
                    if total and n != total:
                        raise RuntimeError(f"short download: {n} of {total} bytes")
            os.replace(tmp, dest)
            log(f"    downloaded {dest.stat().st_size/1e9:.2f} GB")
            return dest.stat().st_size
        except Exception as exc:  # noqa: BLE001
            last = exc
            log(f"    download try {attempt}/{tries} failed: {str(exc)[:100]}")
            time.sleep(min(60, 10 * attempt))
    raise RuntimeError(f"download failed after {tries} tries: {last}")


# ---------------------------------------------------------------- split
def split_to_parts(src: Path, part_dir: Path, delimiter: str = ",",
                   encoding: str = "utf-8-sig", quote_none: bool = False) -> tuple[list[str], int, str]:
    """Read with the csv module, write gzip parts without header.
    Returns (source header, data row count, sha256 of the source file)."""
    part_dir.mkdir(parents=True, exist_ok=True)
    for old in part_dir.glob("*.gz"):
        old.unlink()
    sha = hashlib.sha256()
    with open(src, "rb") as fb:
        for block in iter(lambda: fb.read(1 << 24), b""):
            sha.update(block)
    rows = 0
    part = 0
    with open(src, encoding=encoding, errors="replace", newline="") as f:
        rdr = csv.reader(f, delimiter=delimiter,
                         quoting=csv.QUOTE_NONE if quote_none else csv.QUOTE_MINIMAL)
        header = next(rdr)
        out = None
        w = None
        for rec in rdr:
            if not rec:
                continue  # blank line
            if out is None or rows % PART_ROWS == 0:
                if out is not None:
                    out.close()
                part += 1
                out = gzip.open(part_dir / f"part_{part:03d}.csv.gz", "wt",
                                encoding="utf-8", newline="", compresslevel=1)
                w = csv.writer(out, lineterminator="\n")
            if len(rec) != len(header):
                raise RuntimeError(f"row {rows + 1}: {len(rec)} fields, header has {len(header)}")
            w.writerow(rec)
            rows += 1
        if out is not None:
            out.close()
    log(f"    split {rows:,} rows into {part} gzip parts")
    return header, rows, sha.hexdigest()


# ---------------------------------------------------------------- columns
def landing_columns(header: list[str], spec: dict) -> list[str]:
    """sf_col every header, rename the declared NPI column, error on dupes."""
    cols = [bulk.sf_col(h) for h in header]
    want = {kc["col"].strip().lower(): kc["as"] for kc in spec.get("key_cols", [])}
    hits = 0
    for i, h in enumerate(header):
        if h.strip().lower() in want:
            cols[i] = want[h.strip().lower()]
            hits += 1
    if hits != len(want):
        raise RuntimeError(f"key column not found in header: {want} vs {header[:12]}")
    if len(set(cols)) != len(cols):
        dupes = sorted({c for c in cols if cols.count(c) > 1})
        raise RuntimeError(f"duplicate landing columns: {dupes}")
    return cols


# ---------------------------------------------------------------- land
def land(conn, spec: dict, csv_path: Path) -> dict:
    sid = spec["source_id"]
    table = sid.upper()
    stg = atomic_load.staging_name(table)
    db, sc = settings.raw_database, settings.raw_schema
    fq = f'"{db}"."{sc}"'
    stage = f"STG_{table}"
    url = spec["download_url"]
    started = ingest._utcnow()
    run_id = str(uuid.uuid4())
    part_dir = SCRATCH / f"{sid}_parts"
    cur = conn.cursor()
    try:
        header, rows, sha = split_to_parts(csv_path, part_dir,
                                            delimiter=spec.get("delimiter", ","),
                                            encoding=spec.get("encoding", "utf-8-sig"),
                                            quote_none=bool(spec.get("quote_none")))
        if rows == 0:
            raise RuntimeError("source has 0 data rows")
        cols = landing_columns(header, spec)
        ingested_micros = int(started.timestamp() * 1_000_000)

        cur.execute(f'DROP TABLE IF EXISTS {fq}."{stg}"')
        cur.execute(f'CREATE TABLE {fq}."{stg}" ('
                    + ", ".join(f'"{c}" VARCHAR' for c in cols)
                    + f', "{ingest.META_INGESTED_AT}" NUMBER'
                    f', "{ingest.META_SOURCE_RUN_ID}" VARCHAR'
                    f', "{ingest.META_SRC_SHA256}" VARCHAR)')
        cur.execute(f'CREATE OR REPLACE STAGE {fq}."{stage}"')
        t0 = time.time()
        put_sql = (f"PUT 'file://{part_dir.as_posix()}/part_*.csv.gz' @{fq}.\"{stage}\" "
                   f"AUTO_COMPRESS=FALSE PARALLEL={PUT_PARALLEL}")
        for attempt in range(1, 5):
            try:
                cur.execute(put_sql)   # parts already in the stage are skipped, so a retry only sends what is missing
                break
            except Exception as exc:  # noqa: BLE001
                if attempt == 4:
                    raise
                log(f"    PUT try {attempt} failed, retrying in {30 * attempt}s: {str(exc)[:90]}")
                time.sleep(30 * attempt)
        log(f"    PUT done in {time.time() - t0:.0f}s")
        sel = ", ".join(f"${i + 1}" for i in range(len(cols)))
        t0 = time.time()
        cur.execute(f"""
COPY INTO {fq}."{stg}"
FROM (SELECT {sel}, {ingested_micros}, '{run_id}', '{sha}' FROM @{fq}."{stage}")
FILE_FORMAT=(TYPE=CSV COMPRESSION=GZIP FIELD_DELIMITER=',' SKIP_HEADER=0
             FIELD_OPTIONALLY_ENCLOSED_BY='"' NULL_IF=('') EMPTY_FIELD_AS_NULL=TRUE
             ENCODING='UTF8')
ON_ERROR=ABORT_STATEMENT
""")
        loaded = sum(int(r[3]) for r in cur.fetchall())
        log(f"    COPY done in {time.time() - t0:.0f}s, rows_loaded={loaded:,}")
        cur.execute(f'DROP STAGE {fq}."{stage}"')
        key = spec["key_cols"][0]["as"] if spec.get("key_cols") else cols[0]
        cur.execute(f'SELECT COUNT(*), COUNT(DISTINCT "{key}") FROM {fq}."{stg}"')
        n_stg, n_npi = cur.fetchone()
        if not (loaded == rows == n_stg):
            raise RuntimeError(f"row mismatch: counted {rows:,}, COPY {loaded:,}, staging {n_stg:,}")

        # live-table schema check, same rule as bridge_fuel
        live = bf._table_columns(conn, db, sc, table)
        if live is not None:
            stg_cols = bf._table_columns(conn, db, sc, stg) or []
            if set(stg_cols) != set(live):
                raise RuntimeError(f"schema drift vs live {table}; staging left for inspection")

        atomic_load.execute_swap(conn, table, database=db, schema=sc)
        ended = ingest._utcnow()
        ingest._log_run(conn, sid, run_id, "success", rows, csv_path.stat().st_size, sha, url,
                        started, ended,
                        f"{spec['name']}. Fast path: gzip parts, PUT, COPY INTO staging, atomic swap. "
                        f"{rows:,} rows, {len(cols)} source cols, {n_npi:,} distinct {key}.")
        try:
            bf._register(conn, spec)
        except Exception as exc:
            log(f"    register warn: {exc}")
        log(f"    LOADED {rows:,} rows -> {db}.{sc}.{table}  distinct {key} {n_npi:,}")
        try:
            from loadkit.lifecycle import on_success
            # skip_connect: the graph-wiring subprocess hung 4.5 h past its 300 s timeout
            # on 2026-09-10 and the idle warehouse token expired. Wire the series once
            # at the end with connect.incremental, not per file.
            lc = on_success(sid, table, key_cols=spec.get("key_cols"),
                            description=spec.get("name", ""), conn=conn, skip_connect=True)
            log(f"    lifecycle: scaffold={'yes' if lc['scaffolded'] else 'no'} "
                f"connect={'yes' if lc['connected'] else 'no'} errors={lc['errors']}")
        except Exception as exc:
            log(f"    lifecycle warn: {exc}")
        return {"sid": sid, "status": "success", "rows": rows}
    except Exception as exc:
        ended = ingest._utcnow()
        try:
            cur.execute(f'DROP STAGE IF EXISTS {fq}."{stage}"')
        except Exception:
            pass
        try:
            ingest._log_run(conn, sid, run_id, "failed", None, None, "", url, started, ended,
                            f"Fast path failed (staging {stg} left or dropped, live {table} untouched): {exc}")
        except Exception:
            pass
        log(f"    FAILED {sid}: {exc}")
        return {"sid": sid, "status": f"failed: {exc}", "rows": 0}
    finally:
        cur.close()
        for g in part_dir.glob("*.gz"):
            try:
                g.unlink()
            except Exception:
                pass


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--families", default="PARTB_PROVIDER_SERVICE,PARTD_PRESCRIBER_DRUG")
    ap.add_argument("--sid", help="one source_id instead of families")
    ap.add_argument("--run", action="store_true", help="land; without it, list only")
    ap.add_argument("--keep", action="store_true", help="keep the downloaded csv")
    ap.add_argument("--put-parallel", type=int, default=8, help="PUT upload streams, default 8")
    ap.add_argument("--max-mbps", type=float, default=0.0, help="download cap in MB/s, 0 = none")
    args = ap.parse_args()
    global PUT_PARALLEL, MAX_MBPS
    PUT_PARALLEL, MAX_MBPS = args.put_parallel, args.max_mbps

    specs = {s["source_id"]: s for s in SPECMOD.SPECS}
    if args.sid:
        todo = [specs[args.sid]]
    else:
        fams = args.families.split(",")
        todo = [specs[f"FED_CMS_{f}_DY{y}"] for f in fams for y in SPECMOD._YEARS]
    for s in todo:
        print(s["source_id"], s["download_url"][-45:])
    if not args.run:
        print(f"\n{len(todo)} files. Add --run to land.")
        return 0

    results = []
    conn = None
    try:
        for s in todo:
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass
            conn = snow.connect()   # fresh per file: tokens expire after long idle downloads
            if bf._has_success(conn, s["source_id"]):
                log(f"{s['source_id']}  already landed, skip")
                results.append((s["source_id"], "skip", 0))
                continue
            log(f"==> {s['source_id']}")
            t0 = time.time()
            csv_path = SCRATCH / f"{s['source_id']}.csv"
            try:
                download(s["download_url"], csv_path)
            except Exception as exc:
                log(f"    download FAILED: {exc}")
                results.append((s["source_id"], f"download failed: {exc}", 0))
                continue
            r = land(conn, s, csv_path)
            if r["status"] == "success" and not args.keep:
                try:
                    csv_path.unlink()
                except Exception:
                    pass
            log(f"<== {s['source_id']}  {r['status']}  rows={r['rows']:,}  {(time.time() - t0) / 60:.1f} min")
            results.append((s["source_id"], r["status"], r["rows"]))
    finally:
        if conn is not None:
            conn.close()
    ok = sum(1 for _, st, _ in results if st == "success")
    log(f"done: {ok} loaded, {sum(1 for _, st, _ in results if st == 'skip')} skipped, "
        f"{len(results) - ok - sum(1 for _, st, _ in results if st == 'skip')} failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
