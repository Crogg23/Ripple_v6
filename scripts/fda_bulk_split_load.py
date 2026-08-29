#!/usr/bin/env python3
"""Local-split loader for openFDA bulk JSON files too big for the server-side
whole-doc-as-VARIANT path (scripts/server_side_load.py's `_load_json`).

Some openFDA download.json parts (device/510k, device/pma, device/
registrationlisting, device/udi) pretty-print to well over Snowflake's 128MB
per-document JSON parse limit once decompressed, even though the .json.zip is
a modest size on disk. `_load_json` COPYs the whole doc into one VARIANT row
per file and errors with:
    Error parsing JSON: document is too large, max size 134217728 bytes

Fix: download the file locally (not cloud-to-cloud), stream-parse with ijson
so we never hold the whole doc in memory, re-chunk the `results` array into
many small {"results": [...]} docs (default 2,000 records/chunk -- safely
under the 128MB cap for any of these sources), gzip each chunk, PUT it
directly to the same Snowflake stage server_side_load.py uses, and then reuse
server_side_load.py's own _json_format/_build_variant_staging/_copy_json/
_finalize_table so the result lands through the EXACT same ledger (density
gate, INGEST_RUNS log, atomic swap, SOURCE_REGISTRY upsert) as every other
server-side load. Downstream (RAW:results LATERAL FLATTEN) is unaffected --
chunk boundaries are invisible once flattened.

Usage:
    python scripts/fda_bulk_split_load.py --spec FED_FDA_DEVICE_510K --run
    python scripts/fda_bulk_split_load.py --spec FED_FDA_GUDID --run --chunk-records 2000
"""
from __future__ import annotations

import argparse
import gzip
import io
import json
import re
import sys
import tempfile
import uuid
import zipfile
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_LIB = _REPO / "library-onboarding"
for p in (_REPO, _LIB, _REPO / "scripts"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

try:
    from dotenv import load_dotenv
    load_dotenv(_LIB / ".env", override=True)
except Exception:
    pass

import ijson  # noqa: E402
import requests  # noqa: E402

import ingest  # noqa: E402
import snow  # noqa: E402
from config import settings  # noqa: E402
import server_side_load as ssl  # noqa: E402
import server_side_specs  # noqa: E402

DEFAULT_CHUNK_RECORDS = 2000
CHECKPOINT = _REPO / "logs" / "fda_split_checkpoint.json"


def _load_checkpoint() -> dict:
    if CHECKPOINT.exists():
        try:
            return json.loads(CHECKPOINT.read_text())
        except Exception:
            return {}
    return {}


def _save_checkpoint(cp: dict) -> None:
    CHECKPOINT.parent.mkdir(exist_ok=True)
    CHECKPOINT.write_text(json.dumps(cp, indent=1))


def _load_spec(source_id: str) -> dict:
    specs = ssl._load_specs()
    if source_id not in specs:
        raise SystemExit(f"unknown source_id {source_id!r}. Known: {sorted(specs)}")
    return specs[source_id]


def _urls(s: dict) -> list[str]:
    return ssl._resolve_manifest(s) if s.get("manifest") else [ssl._resolve_url(s)]


def _download_and_extract_json(url: str, tmpdir: Path) -> Path:
    """Download a .json.zip locally and return the path to the extracted .json member."""
    zpath = tmpdir / "part.zip"
    with requests.get(url, stream=True, timeout=300, headers={"User-Agent": "Ripple fda-split-load"}) as r:
        r.raise_for_status()
        with open(zpath, "wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 20):
                if chunk:
                    f.write(chunk)
    with zipfile.ZipFile(zpath) as zf:
        member = next(n for n in zf.namelist() if n.endswith(".json"))
        out = tmpdir / "part.json"
        with zf.open(member) as src, open(out, "wb") as dst:
            while True:
                buf = src.read(1 << 20)
                if not buf:
                    break
                dst.write(buf)
    zpath.unlink(missing_ok=True)
    return out


def _iter_result_chunks(json_path: Path, chunk_records: int):
    """Stream-parse `results` (an array anywhere at top level) and yield lists of
    `chunk_records` raw python objects at a time -- never holds the whole doc."""
    with open(json_path, "rb") as f:
        objs = ijson.items(f, "results.item")
        buf = []
        for obj in objs:
            buf.append(obj)
            if len(buf) >= chunk_records:
                yield buf
                buf = []
        if buf:
            yield buf


def _put_chunk(conn_holder: list, chunk: list, stage_path: str, tmpdir: Path) -> None:
    # PUT keeps the LOCAL basename as the staged object name, so the local temp
    # file must already be named exactly like the target part (part_NNNN_MMMMM.json.gz).
    doc = json.dumps({"results": chunk}).encode("utf-8")
    fname = stage_path.split("/")[-1]
    stage_dir = "/".join(stage_path.split("/")[:-1])
    gz_path = tmpdir / fname
    with gzip.open(gz_path, "wb", compresslevel=6) as gz:
        gz.write(doc)
    uri = "file://" + str(gz_path.resolve()).replace("\\", "/")
    last_err = None
    for attempt in range(3):
        try:
            cur = conn_holder[0].cursor()
            try:
                cur.execute(
                    f"PUT '{uri}' '@{ssl.STAGE}/{stage_dir}/' AUTO_COMPRESS=FALSE OVERWRITE=TRUE"
                )
            finally:
                cur.close()
            last_err = None
            break
        except Exception as e:
            last_err = e
            print(f"        PUT failed (attempt {attempt+1}/3): {e} -- reconnecting")
            try:
                conn_holder[0].close()
            except Exception:
                pass
            conn_holder[0] = snow.connect()
    if last_err is not None:
        raise last_err
    gz_path.unlink(missing_ok=True)


def load_source(source_id: str, do_run: bool, chunk_records: int, force: bool) -> dict:
    s = _load_spec(source_id)
    table = source_id.upper()
    conn_holder = [snow.connect()]
    try:
        if not force and do_run and ingest._latest_success_sha(conn_holder[0], source_id) is not None:
            print("    already landed -- skipping (use --force)")
            return {"source_id": source_id, "status": "skip (already landed)"}
        urls = _urls(s)
        print(f"\n=== {source_id} ({s.get('name','')}) === split-load: {len(urls)} source file(s), "
              f"chunk={chunk_records} records/part")
        started = ingest._utcnow()
        run_id = str(uuid.uuid4())
        total_parts = 0
        total_records = 0
        cp = _load_checkpoint()
        src_cp = cp.setdefault(source_id, {"done_urls": [], "chunk_records": chunk_records})
        # If a prior checkpointed run used a different chunk size, the staged
        # parts are incompatible with resuming -- start clean for this source.
        if src_cp.get("chunk_records") != chunk_records:
            src_cp = {"done_urls": [], "chunk_records": chunk_records}
            cp[source_id] = src_cp
        done_urls = set(src_cp.get("done_urls", []))
        if do_run and not done_urls:
            # Clear any stale/contaminated staged files (e.g. a leftover whole-doc
            # part from a prior failed server_side_load.py attempt at this source_id)
            # -- only when we have no checkpointed progress to protect.
            cur = conn_holder[0].cursor()
            try:
                cur.execute(f"REMOVE '@{ssl.STAGE}/bulk/{source_id.lower()}/'")
            except Exception:
                pass
            finally:
                cur.close()
        elif done_urls:
            print(f"    resuming: {len(done_urls)}/{len(urls)} source file(s) already staged (checkpoint)")
        with tempfile.TemporaryDirectory(prefix="fda_split_") as td:
            tmpdir = Path(td)
            for fi, url in enumerate(urls):
                if url in done_urls:
                    total_parts_note = ""
                    print(f"    [{fi+1}/{len(urls)}] already staged, skipping: {url}")
                    continue
                print(f"    [{fi+1}/{len(urls)}] downloading {url}")
                json_path = _download_and_extract_json(url, tmpdir)
                url_records = 0
                for ci, chunk in enumerate(_iter_result_chunks(json_path, chunk_records)):
                    part_name = f"part_{fi:04d}_{ci:05d}.json.gz"
                    stage_path = f"bulk/{source_id.lower()}/{part_name}"
                    if do_run:
                        _put_chunk(conn_holder, chunk, stage_path, tmpdir)
                    total_parts += 1
                    total_records += len(chunk)
                    url_records += len(chunk)
                json_path.unlink(missing_ok=True)
                print(f"        -> {total_parts} chunk(s) so far, {total_records:,} record(s)")
                if do_run:
                    src_cp["done_urls"].append(url)
                    _save_checkpoint(cp)
        if not do_run:
            print("    PREVIEW only (add --run to land)")
            return {"source_id": source_id, "status": "preview", "records": total_records}
        # COPY every staged chunk into one VARIANT staging table, then finalize
        # through server_side_load's own shared tail (density gate + atomic swap +
        # INGEST_RUNS log + SOURCE_REGISTRY upsert).
        fmt = ssl._json_format(conn_holder[0])
        stg = ssl._build_variant_staging(conn_holder[0], table)
        cur = conn_holder[0].cursor()
        try:
            cur.execute(f"LIST '@{ssl.STAGE}/bulk/{source_id.lower()}/'")
            rows = cur.fetchall()
        finally:
            cur.close()
        chunk_re = re.compile(r"part_\d{4}_\d{5}\.json\.gz$")
        staged_paths = sorted(
            r[0].split("/", 1)[-1] for r in rows if chunk_re.search(r[0])
        )
        total = 0
        for i, sp in enumerate(staged_paths):
            total += ssl._copy_json(conn_holder[0], stg, sp, fmt)
            if (i + 1) % 20 == 0:
                print(f"        COPY progress: {i+1}/{len(staged_paths)} parts, {total:,} rows")
        print(f"    COPY -> staging {stg}: {total:,} VARIANT row(s) from {len(staged_paths)} part(s)")
        sha = f"split_json:{len(staged_paths)}:{total_records}"
        result = ssl._finalize_table(conn_holder[0], s, source_id, table, stg, total, run_id, started, sha, urls[0], min_rows=1)
        # Successful finalize means the table is live; clear this source's checkpoint
        # so a future --force reload starts clean instead of "resuming" a stale state.
        cp2 = _load_checkpoint()
        cp2.pop(source_id, None)
        _save_checkpoint(cp2)
        return result
    finally:
        conn_holder[0].close()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--spec", required=True, help="source_id (e.g. FED_FDA_DEVICE_510K) or 'all'")
    ap.add_argument("--run", action="store_true", help="actually land (default: preview/dry-run)")
    ap.add_argument("--force", action="store_true", help="reload even if already landed")
    ap.add_argument("--chunk-records", type=int, default=DEFAULT_CHUNK_RECORDS)
    args = ap.parse_args(argv)

    if args.spec == "all":
        ids = sorted(ssl._load_specs())
    else:
        ids = [args.spec]
    results = [load_source(sid, args.run, args.chunk_records, args.force) for sid in ids]
    for r in results:
        print(r)
    # Quality gate: load_source finalizes through server_side_load's shared density
    # gate (see its docstring), which logs STATUS='empty' rather than raising for a
    # degenerate load -- so this batch's own exit code must check for that verdict
    # rather than assume "no exception" means "no bad load" (real errors DO already
    # propagate as exceptions here, since load_source has no its-own try/except).
    bad = [r for r in results if r.get("status") == "empty"]
    if bad:
        raise RuntimeError(f"QUALITY GATE FAILED for: {[r['source_id'] for r in bad]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
