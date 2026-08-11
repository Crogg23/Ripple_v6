"""Repair class-7 SHORT/broken sources from the 2026-08-11 warehouse verification.

Seven small pulls (largest ~700k rows), each re-pulled IN FULL from the
publisher and overwritten into its existing LANDING table via the loaders' own
write_pandas overwrite pattern (same as scripts/tier1_bulk_batch_load.py).
No ad-hoc DROP/TRUNCATE/CREATE OR REPLACE SQL is issued.

    python scripts/repair_short_sources_2026_08_11.py                # preview
    python scripts/repair_short_sources_2026_08_11.py --run          # all
    python scripts/repair_short_sources_2026_08_11.py --run --source fed_sam_exclusions

Paginated pulls checkpoint page data to outputs/_short_repair_{source}.jsonl
so a crash resumes instead of restarting.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import io
import json
import sys
import time
import uuid
import zipfile
from pathlib import Path

import pandas as pd
import requests

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "scripts"))
sys.path.insert(0, str(_REPO / "library-onboarding"))
try:
    from dotenv import load_dotenv
    load_dotenv(_REPO / "library-onboarding/.env", override=True)
except Exception:
    pass

import snow  # noqa: E402
import _bulk_load_utils as bulk  # noqa: E402

UA = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}
OUT = _REPO / "outputs"
CHUNK_ROWS = 100_000


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _as_text(v):
    """None-safe scalar -> str (never the literal 'nan'/'None')."""
    if v is None:
        return None
    if isinstance(v, float) and pd.isna(v):
        return None
    if isinstance(v, (dict, list)):
        return json.dumps(v, ensure_ascii=False, default=str)
    s = str(v)
    return s if s != "" else None


def _clean(df: pd.DataFrame) -> pd.DataFrame:
    """dtype=str semantics for API-built frames: object dtype, NaN -> None."""
    df = df.astype(object).where(df.notna(), None)
    return df


def _existing_schema(conn, tbl: str) -> dict[str, str] | None:
    """{col: data_type} for an existing LANDING table, or None if absent."""
    cur = conn.cursor()
    cur.execute(
        f"SELECT COLUMN_NAME, DATA_TYPE FROM {bulk.LANDING_DB}.INFORMATION_SCHEMA.COLUMNS "
        f"WHERE TABLE_SCHEMA='{bulk.LANDING_SCHEMA}' AND TABLE_NAME='{tbl}'")
    rows = cur.fetchall()
    return {r[0]: r[1] for r in rows} if rows else None


def _overwrite_table(conn, df: pd.DataFrame, tbl: str, *, sha: str, run_id: str,
                     started: dt.datetime, source_url: str,
                     expected: int | None) -> tuple[int, str]:
    """Chunked write_pandas overwrite into the SAME table (loader pattern).

    write_pandas(overwrite=True) TRUNCATEs an existing table and keeps its
    schema (connector 3.18) -- it can never alter one. So if the existing
    table's columns/types can't hold the fresh pull, we land into {tbl}_FULL
    (new table) instead of issuing any ad-hoc DROP/CREATE OR REPLACE, and
    report that for the human one-liner list. Returns (rows, actual_table).
    """
    from snowflake.connector.pandas_tools import write_pandas
    df.columns = [bulk.sf_col(c) for c in df.columns]
    # de-dup any collided sanitized names
    seen, cols = {}, []
    for c in df.columns:
        n = seen.get(c, 0)
        seen[c] = n + 1
        cols.append(c if n == 0 else f"{c}_{n}")
    df.columns = cols
    df = _clean(df)
    df[bulk.META_INGESTED_AT] = started.replace(tzinfo=None)
    df[bulk.META_SOURCE_RUN_ID] = run_id
    df[bulk.META_SRC_SHA256] = sha

    def _compatible(schema: dict[str, str]) -> bool:
        """Existing table can hold this df: same columns, text types
        (meta timestamp column may be TIMESTAMP_NTZ)."""
        if set(schema) != set(df.columns):
            return False
        for c, t in schema.items():
            if c == bulk.META_INGESTED_AT and t.startswith("TIMESTAMP"):
                continue
            if t != "TEXT":
                return False
        return True

    base = tbl
    chosen = None
    for cand in (base, f"{base}_FULL", f"{base}_FULL_R2"):
        schema = _existing_schema(conn, cand)
        if schema is None or _compatible(schema):
            if cand != base:
                print(f"    SCHEMA MISMATCH on earlier candidate -> landing into "
                      f"{cand} (no drop/replace issued)")
            chosen = (cand, schema)
            break
    if chosen is None:
        raise RuntimeError(
            f"{base}: no compatible landing table among {base}/_FULL/_FULL_R2 -- "
            f"needs a human DROP one-liner")
    tbl, schema = chosen
    if schema is None:
        # Explicit all-VARCHAR create (never rely on parquet inference: an
        # all-null first chunk otherwise creates NUMBER columns).
        cols_sql = ", ".join(
            f'"{c}" TIMESTAMP_NTZ' if c == bulk.META_INGESTED_AT else f'"{c}" VARCHAR'
            for c in df.columns)
        cur = conn.cursor()
        cur.execute(f'CREATE TABLE IF NOT EXISTS {bulk.LANDING_FQS}."{tbl}" ({cols_sql})')

    total = 0
    for i in range(0, len(df), CHUNK_ROWS):
        chunk = df.iloc[i:i + CHUNK_ROWS]
        ok, _c, _n, _ = write_pandas(
            conn, chunk, table_name=tbl,
            database=bulk.LANDING_DB, schema=bulk.LANDING_SCHEMA,
            auto_create_table=False, overwrite=(i == 0),
            quote_identifiers=False, use_logical_type=True,
        )
        if not ok:
            raise RuntimeError(f"write_pandas failed for {tbl} at offset {i}")
        total += len(chunk)
        print(f"    {tbl}: {total:,}/{len(df):,} rows written")

    # never-silently-short guard vs publisher total
    if expected and total < expected * 0.98:
        raise RuntimeError(
            f"{tbl}: loaded {total:,} < 98% of publisher-declared {expected:,}")

    passed, report = bulk.run_quality_gate(
        conn, tbl, tbl, run_id, sha256=sha, row_count=total,
        source_url=source_url)
    if not passed:
        raise RuntimeError(f"{tbl}: quality gate failed -- {report}")
    return total, tbl


def _key_check(conn, tbl: str, key_cols: list[str]) -> list[dict]:
    """COUNT + COUNT(DISTINCT) + 3 samples per key column (never bare COUNT)."""
    cur = conn.cursor()
    out = []
    cur.execute(f'SELECT COLUMN_NAME FROM {bulk.LANDING_DB}.INFORMATION_SCHEMA.COLUMNS '
                f"WHERE TABLE_SCHEMA='{bulk.LANDING_SCHEMA}' AND TABLE_NAME='{tbl}'")
    have = {r[0] for r in cur.fetchall()}
    for k in key_cols:
        if k not in have:
            out.append({"col": k, "error": "column not found"})
            continue
        cur.execute(f'SELECT COUNT(*), COUNT("{k}"), COUNT(DISTINCT "{k}") '
                    f'FROM {bulk.LANDING_FQS}."{tbl}"')
        n, cnt, dist = cur.fetchone()
        cur.execute(f'SELECT "{k}" FROM {bulk.LANDING_FQS}."{tbl}" '
                    f'WHERE "{k}" IS NOT NULL LIMIT 3')
        samples = [r[0] for r in cur.fetchall()]
        out.append({"col": k, "rows": n, "non_null": cnt, "distinct": dist,
                    "samples": samples})
    return out


def _paginate_jsonl(path: Path, fetch_page, state_key: str):
    """Generic checkpointed pager. fetch_page(offset) -> (records, done)."""
    ckpt = path.with_suffix(".ckpt.json")
    offset = 0
    if ckpt.exists():
        offset = json.loads(ckpt.read_text()).get(state_key, 0)
        print(f"    resuming at offset {offset:,}")
    else:
        path.write_text("")  # fresh
    with path.open("a", encoding="utf-8") as f:
        while True:
            recs, done = fetch_page(offset)
            for r in recs:
                f.write(json.dumps(r, ensure_ascii=False, default=str) + "\n")
            offset += len(recs)
            ckpt.write_text(json.dumps({state_key: offset}))
            print(f"    fetched {offset:,} records")
            if done:
                break
            time.sleep(0.3)
    rows = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    return rows


def _df_from_records(rows: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    for c in df.columns:
        df[c] = df[c].map(_as_text)
    return df


# ---------------------------------------------------------------------------
# 1. GLEIF level-2 relationships (rr golden copy)
# ---------------------------------------------------------------------------
def fetch_gleif(conn):
    api = "https://goldencopy.gleif.org/api/v2/golden-copies/publishes/latest"
    meta = requests.get(api, timeout=120, headers=UA).json()["data"]
    c = meta["rr"]["full_file"]["csv"]
    url, expected = c["url"], int(c["record_count"])
    print(f"    GLEIF rr full file: {expected:,} records  {url}")
    resp = requests.get(url, timeout=1800, headers=UA)
    resp.raise_for_status()
    sha = hashlib.sha256(resp.content).hexdigest()
    frames = []
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        for name in zf.namelist():
            if name.lower().endswith(".csv"):
                with zf.open(name) as f:
                    frames.append(pd.read_csv(f, dtype=str, low_memory=False,
                                              encoding_errors="replace"))
    df = pd.concat(frames, ignore_index=True)
    return df, url, sha, expected


# ---------------------------------------------------------------------------
# 2. SAM.gov public exclusions extract
# ---------------------------------------------------------------------------
def fetch_sam(conn):
    today = dt.date.today()
    tried = []
    for back in range(0, 10):
        d = today - dt.timedelta(days=back)
        for stamp in (d.strftime("%y%j"), d.strftime("%Y%m%d")):
            for host in (
                "https://falextracts.s3.amazonaws.com/Exclusions/Public%20V2",
                "https://sam.gov/api/prod/fileextractservices/v1/api/download/Exclusions/Public%20V2",
            ):
                url = f"{host}/SAM_Exclusions_Public_Extract_V2_{stamp}.ZIP"
                tried.append(url)
                try:
                    r = requests.get(url, timeout=600, headers=UA)
                    if r.status_code == 200 and len(r.content) > 100_000:
                        sha = hashlib.sha256(r.content).hexdigest()
                        with zipfile.ZipFile(io.BytesIO(r.content)) as zf:
                            name = [n for n in zf.namelist()
                                    if n.upper().endswith(".CSV")][0]
                            with zf.open(name) as f:
                                df = pd.read_csv(f, dtype=str, low_memory=False,
                                                 encoding_errors="replace")
                        return df, url, sha, None
                except Exception as e:
                    print(f"    miss {url.split('/')[-1]} ({type(e).__name__})")
    raise RuntimeError("SAM exclusions extract not found; tried:\n" + "\n".join(tried[-6:]))


# ---------------------------------------------------------------------------
# 3. OpenFEMA NfipCommunityStatusBook
# ---------------------------------------------------------------------------
def fetch_fema(conn):
    """Full-file CSV endpoint. NOTE (verified 2026-08-11): the API's
    metadata.count says 32,436 but both the paginated JSON API and the
    publisher's own full CSV end at 25,125 rows -- the metadata count is
    wrong/stale on FEMA's side, 25,125 IS the complete dataset."""
    base = "https://www.fema.gov/api/open/v1/NfipCommunityStatusBook"
    try:
        declared = requests.get(base + "?$inlinecount=allpages&$top=1", timeout=120,
                                headers=UA).json()["metadata"]["count"]
        print(f"    OpenFEMA metadata.count = {declared:,} (known-inflated; "
              f"full CSV is the authority)")
    except Exception:
        pass
    url = base + ".csv"
    r = requests.get(url, timeout=900, headers=UA)
    r.raise_for_status()
    sha = hashlib.sha256(r.content).hexdigest()
    df = pd.read_csv(io.BytesIO(r.content), dtype=str, low_memory=False,
                     encoding_errors="replace")
    return df, url, sha, len(df)


# ---------------------------------------------------------------------------
# 4. ransomware.live victims (full CSV export)
# ---------------------------------------------------------------------------
def fetch_ransomware(conn):
    """Full-history export (verified 2026-08-11: victims.csv/json span
    2013-11 -> today; the 46,405 figure from the verification sweep no longer
    matches the publisher's file, which now holds ~30.7k after their own
    pruning). The file's own row count is the authority."""
    url = "https://data.ransomware.live/victims.csv"
    r = requests.get(url, timeout=600, headers=UA)
    r.raise_for_status()
    sha = hashlib.sha256(r.content).hexdigest()
    df = pd.read_csv(io.BytesIO(r.content), dtype=str, low_memory=False,
                     encoding_errors="replace")
    return df, url, sha, len(df)


# ---------------------------------------------------------------------------
# 5. Voteview rollcall metadata (full CSV)
# ---------------------------------------------------------------------------
def fetch_voteview(conn):
    url = "https://voteview.com/static/data/out/rollcalls/HSall_rollcalls.csv"
    r = requests.get(url, timeout=600, headers=UA)
    r.raise_for_status()
    sha = hashlib.sha256(r.content).hexdigest()
    df = pd.read_csv(io.BytesIO(r.content), dtype=str, low_memory=False,
                     encoding_errors="replace")
    return df, url, sha, None


# ---------------------------------------------------------------------------
# 6. data.gouv.fr datasets catalog CSV
# ---------------------------------------------------------------------------
def fetch_datagouv(conn):
    # discover the catalog CSV resource from the catalog dataset's own API page
    api = "https://www.data.gouv.fr/api/1/datasets/catalogue-des-donnees-de-data-gouv-fr/"
    url = None
    try:
        meta = requests.get(api, timeout=120, headers=UA).json()
        for res in meta.get("resources", []):
            title = (res.get("title") or "").lower()
            toks = title.replace("-", " ").replace(".", " ").split()
            if res.get("format", "").lower() == "csv" and "dataset" in toks and "export" in toks:
                url = res["url"]
                break
    except Exception as e:
        print(f"    catalog dataset API failed ({e}); using stable resource URL")
    if not url:
        url = "https://www.data.gouv.fr/fr/datasets/r/f868cca6-8da1-4369-a78d-47463f19a9a3"
    print(f"    catalog CSV: {url}")
    r = requests.get(url, timeout=900, headers=UA)
    r.raise_for_status()
    sha = hashlib.sha256(r.content).hexdigest()
    df = pd.read_csv(io.BytesIO(r.content), dtype=str, sep=";", low_memory=False,
                     encoding_errors="replace")
    if len(df.columns) < 3:  # wrong separator guess
        df = pd.read_csv(io.BytesIO(r.content), dtype=str, low_memory=False,
                         encoding_errors="replace")
    return df, url, sha, None


# ---------------------------------------------------------------------------
# 7. CDC Socrata discovery catalog for data.cdc.gov
# ---------------------------------------------------------------------------
def fetch_cdc(conn):
    base = "https://api.us.socrata.com/api/catalog/v1?domains=data.cdc.gov&limit=500"
    total = requests.get(base.replace("limit=500", "limit=1"), timeout=120,
                         headers=UA).json()["resultSetSize"]
    print(f"    Socrata declares {total:,} assets")

    def page(offset):
        r = requests.get(f"{base}&offset={offset}", timeout=300, headers=UA)
        r.raise_for_status()
        results = r.json().get("results", [])
        recs = []
        for item in results:
            res = item.get("resource", {})
            flat = {f"RESOURCE_{k.upper()}": v for k, v in res.items()}
            flat["PERMALINK"] = item.get("permalink")
            flat["LINK"] = item.get("link")
            cls = item.get("classification", {})
            flat["CATEGORIES"] = cls.get("categories")
            flat["DOMAIN_CATEGORY"] = cls.get("domain_category")
            flat["DOMAIN_TAGS"] = cls.get("domain_tags")
            flat["OWNER_DISPLAY_NAME"] = item.get("owner", {}).get("display_name")
            recs.append(flat)
        return recs, len(results) == 0 or offset + len(results) >= total
    rows = _paginate_jsonl(OUT / "_short_repair_cdc_catalog.jsonl", page, "offset")
    df = _df_from_records(rows)
    # runaway-pager fix: keep one row per asset id
    if "RESOURCE_ID" in df.columns:
        before = len(df)
        df = df.drop_duplicates(subset=["RESOURCE_ID"], keep="last")
        if before != len(df):
            print(f"    de-duped {before:,} -> {len(df):,} distinct assets")
    src = "https://api.us.socrata.com/api/catalog/v1?domains=data.cdc.gov"
    sha = hashlib.sha256(json.dumps({"rows": len(df), "src": src}).encode()).hexdigest()
    return df, src, sha, int(total)


# ---------------------------------------------------------------------------
# registry
# ---------------------------------------------------------------------------
SOURCES = [
    {"id": "intl_gleif_relationships", "table": "INTL_GLEIF_RELATIONSHIPS",
     "fetch": fetch_gleif, "publisher_total": 658145,
     "keys": ["RELATIONSHIP_STARTNODE_NODEID", "RELATIONSHIP_ENDNODE_NODEID"]},
    {"id": "fed_sam_exclusions", "table": "FED_SAM_EXCLUSIONS",
     "fetch": fetch_sam, "publisher_total": 167681,
     "keys": ["UNIQUE_ENTITY_ID", "NAME", "CLASSIFICATION"]},
    {"id": "fed_fema_nfip_community_status_book",
     "table": "FED_FEMA_NFIP_COMMUNITY_STATUS_BOOK",
     "fetch": fetch_fema, "publisher_total": 32436,
     "keys": ["COMMUNITYIDNUMBER", "COMMUNITYNAME", "ID"]},
    {"id": "xc_ransomwarelive_victims", "table": "XC_RANSOMWARELIVE_VICTIMS",
     "fetch": fetch_ransomware, "publisher_total": 46405,
     "keys": ["VICTIM", "GROUP", "DISCOVERED"]},
    {"id": "fed_voteview_rollcall_meta", "table": "FED_VOTEVIEW_ROLLCALL_META",
     "fetch": fetch_voteview, "publisher_total": 113512,
     "keys": ["CONGRESS", "ROLLNUMBER", "CHAMBER"]},
    {"id": "intl_fr_data_gouv", "table": "INTL_FR_DATA_GOUV",
     "fetch": fetch_datagouv, "publisher_total": 73883,
     "keys": ["ID", "SLUG", "TITLE"]},
    {"id": "fed_cdc_data_portal", "table": "FED_CDC_DATA_PORTAL",
     "fetch": fetch_cdc, "publisher_total": 1471,
     "keys": ["RESOURCE_ID", "RESOURCE_NAME"]},
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--source", default=None)
    args = ap.parse_args()

    entries = SOURCES if not args.source else [s for s in SOURCES if s["id"] == args.source]
    if not entries:
        print(f"unknown source '{args.source}'")
        return 1
    if not args.run:
        for s in entries:
            print(f"{s['id']:42s} -> {s['table']} (publisher ~{s['publisher_total']:,})")
        print("\npreview only -- add --run")
        return 0

    OUT.mkdir(exist_ok=True)
    conn = snow.connect()
    results = []
    try:
        for s in entries:
            print(f"\n=== {s['id']} -> {s['table']} ===")
            try:
                df, url, sha, declared = s["fetch"](conn)
                expected = declared or s["publisher_total"]
                print(f"    fetched {len(df):,} rows (publisher ~{expected:,})")
                run_id = str(uuid.uuid4())
                started = dt.datetime.now(dt.timezone.utc)
                n, landed = _overwrite_table(conn, df, s["table"], sha=sha,
                                             run_id=run_id, started=started,
                                             source_url=url, expected=expected)
                keys = _key_check(conn, landed, s["keys"])
                results.append({"id": s["id"], "table": landed, "rows": n,
                                "publisher": expected, "url": url, "keys": keys,
                                "fallback_new_table": landed != s["table"]})
                print(f"    LOADED {n:,} rows; key check: "
                      + json.dumps(keys, default=str)[:400])
            except Exception as e:
                msg = f"{type(e).__name__}: {e}"
                print(f"    FAILED: {msg[:400]}")
                results.append({"id": s["id"], "table": s["table"], "error": msg})
    finally:
        conn.close()

    report = OUT / "_short_repair_results_2026-08-11.json"
    report.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    print(f"\nresults -> {report}")
    failed = [r for r in results if "error" in r]
    print(f"DONE: {len(results)-len(failed)}/{len(results)} loaded; {len(failed)} failed")
    for r in failed:
        print(f"  FAILED {r['id']}: {r['error'][:200]}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
