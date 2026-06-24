"""Templated, LLM-free bulk loader for the portal dataset index.

The 76,670 ArcGIS + Socrata datasets in PORTAL_DATASET_INDEX all speak a uniform
API and already have their columns harvested — so they need NO recon and NO
codegen. This loader skips the whole 5-checkpoint / Claude path: it reads
candidates from the index, fetches each via its platform template, and lands it
to LIBRARY_RAW.LANDING with the SAME provenance stamps + INGEST_RUNS log +
SOURCE_REGISTRY row as everything else (reuses ingest.py / register.py).

Deterministic, cheap, fast — the throughput lever from 37 sources to thousands.

    python -m connect harvest --limit 5 --max-rows 500          # safe capped batch
    python -m connect harvest --platform SOCRATA --with-key --limit 50

Safe by default: skips anything already landed, caps rows, previews unless --run.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
import re
import uuid
from urllib.parse import urlparse

import pandas as pd
import requests

from . import db

# Reuse the real landing/registry plumbing (one source of truth for provenance).
import ingest          # library-onboarding/ingest.py (on path via connect.db)
import register        # library-onboarding/register.py
import snow

INDEX = "LIBRARY_META.REGISTRY.PORTAL_DATASET_INDEX"
UA = {"User-Agent": "Mozilla/5.0 (ripple-portal-loader)"}
SOC_PAGE = 50_000
ARC_PAGE = 2_000


# --------------------------------------------------------------------------- #
# Candidate selection
# --------------------------------------------------------------------------- #
def candidates(conn, platform=None, with_key=False, min_rows=1, max_rows=200_000,
               limit=20) -> list[dict]:
    where = ["ARRAY_SIZE(column_names) > 0", "NULLIF(TRIM(source_url),'') IS NOT NULL",
             "platform IN ('SOCRATA','ARCGIS')"]
    if platform:
        where.append(f"platform = '{platform.upper()}'")
    if with_key:
        where.append("join_keys IS NOT NULL AND ARRAY_SIZE(join_keys) > 0")
    # size band: unknown OK (Socrata reports none), else within [min,max]
    where.append(f"(row_count IS NULL OR row_count BETWEEN {min_rows} AND {max_rows})")
    q = f"""
        SELECT platform, portal_name, dataset_id, dataset_title, source_url,
               row_count, top_tier, join_keys
        FROM {INDEX}
        WHERE {' AND '.join(where)}
        ORDER BY CASE top_tier WHEN 'STEEL' THEN 0 WHEN 'STRONG' THEN 1
                               WHEN 'GEO' THEN 2 ELSE 3 END, row_count NULLS LAST
        LIMIT {int(limit)}
    """
    return db.dicts(conn, q)


# Entity keys (STEEL/STRONG) come from the shared tagger -- single source of truth.
from .keys import ENTITY_KEYS  # noqa: E402


def live_key_types(entity_only: bool = True) -> set[str]:
    """Key types the EXISTING landed Library carries (excludes already-bulk-loaded
    portal_* tables). These are what new datasets can wire into."""
    from .fingerprint import OUT as FP_PATH
    try:
        data = json.loads(FP_PATH.read_text())
    except FileNotFoundError:
        return set()
    keys = set()
    for t, info in data.items():
        if t.startswith("PORTAL_"):
            continue
        for k in info["keys"]:
            if k["populated_pct"] > 0:
                keys.add(k["key"])
    return (keys & set(ENTITY_KEYS)) if entity_only else keys


def connectable_candidates(conn, limit=50, size_cap=2_000_000) -> list[dict]:
    """Datasets carrying an ENTITY key — wide net, but ordered so the ones that
    share a key with data you ALREADY hold come first (they wire in immediately)."""
    live = live_key_types() or {"NPI"}
    net = ", ".join(f"'{k}'" for k in ENTITY_KEYS)
    live_arr = ", ".join(f"'{k}'" for k in live)
    q = f"""
        SELECT platform, portal_name, dataset_id, dataset_title, source_url,
               row_count, top_tier, join_keys,
               ARRAYS_OVERLAP(join_keys, ARRAY_CONSTRUCT({live_arr})) AS hits_live
        FROM {INDEX}
        WHERE ARRAY_SIZE(column_names) > 0 AND NULLIF(TRIM(source_url),'') IS NOT NULL
          AND platform IN ('SOCRATA','ARCGIS')
          AND ARRAYS_OVERLAP(join_keys, ARRAY_CONSTRUCT({net}))
          AND (row_count IS NULL OR row_count <= {size_cap})
        ORDER BY hits_live DESC,
                 CASE top_tier WHEN 'STEEL' THEN 0 WHEN 'STRONG' THEN 1 ELSE 2 END,
                 row_count NULLS LAST
        LIMIT {int(limit)}
    """
    return db.dicts(conn, q)


def verify_connections(conn, new_tables: list[str]) -> list[dict]:
    """For each freshly-loaded table, do its entity keys ACTUALLY overlap an
    existing source? Honest check — turns 'carries a key' into 'joins on N rows'."""
    from .fingerprint import OUT as FP_PATH, fingerprint_table
    from .keys import normalize_sql  # noqa
    from .overlap import value_overlap

    existing = {t: info for t, info in json.loads(FP_PATH.read_text()).items()
                if not t.startswith("PORTAL_")}
    # best existing column per entity key
    holders: dict[str, tuple] = {}
    for t, info in existing.items():
        for k in info["keys"]:
            if k["key"] in ENTITY_KEYS and k["populated_pct"] > 0:
                if k["key"] not in holders or k["distinct"] > holders[k["key"]][2]:
                    holders[k["key"]] = (t, k["column"], k["distinct"])

    found = []
    for nt in new_tables:
        fp = fingerprint_table(conn, nt)
        for k in fp["keys"]:
            key = k["key"]
            if key in holders and k["mode"] == "value" and k["populated_pct"] > 0:
                et, ecol, _ = holders[key]
                try:
                    ov = value_overlap(conn, nt, k["column"], et, ecol, key)
                except Exception:
                    continue
                if ov["matched"] > 0:
                    found.append({"new": nt, "key": key, "existing": et,
                                  "matched": ov["matched"], "rate": ov["match_rate"]})
                    print(f"    + {nt[:34]} -{key}-> {et}: {ov['matched']:,} matched ({ov['match_rate']}%)")
    return found


# --------------------------------------------------------------------------- #
# SOURCE_ID minting (clearly namespaced as bulk-portal-sourced; no collisions)
# --------------------------------------------------------------------------- #
def _slug(s: str, n: int = 22) -> str:
    s = re.sub(r"[^0-9a-z]+", "_", (s or "").lower()).strip("_")
    return s[:n].strip("_") or "portal"


def source_id_for(rec: dict) -> str:
    plat = rec["PLATFORM"].lower()[:3]                 # soc / arc
    portal = _slug(rec["PORTAL_NAME"])
    did = _slug(rec["DATASET_ID"], 40)
    return f"portal_{plat}_{portal}_{did}"


# --------------------------------------------------------------------------- #
# Platform fetch templates (proven live 2026-06-23)
# --------------------------------------------------------------------------- #
def _flatten(v):
    """Scalars stay; dicts/lists become JSON strings (raw landing is all-TEXT)."""
    if isinstance(v, (dict, list)):
        return json.dumps(v, ensure_ascii=False)
    return v


def fetch_socrata(rec: dict, max_rows: int) -> list[dict]:
    domain = urlparse(rec["SOURCE_URL"]).netloc
    endpoint = f"https://{domain}/resource/{rec['DATASET_ID']}.json"
    out, offset = [], 0
    while len(out) < max_rows:
        page = min(SOC_PAGE, max_rows - len(out))
        r = requests.get(endpoint, headers=UA, timeout=60,
                         params={"$limit": page, "$offset": offset})
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        out.extend({k: _flatten(v) for k, v in row.items()} for row in batch)
        offset += len(batch)
        if len(batch) < page:
            break
    return out


def _arcgis_service_url(item_id: str) -> str | None:
    meta = requests.get(f"https://www.arcgis.com/sharing/rest/content/items/{item_id}",
                        headers=UA, timeout=30, params={"f": "json"}).json()
    return meta.get("url")


def fetch_arcgis(rec: dict, max_rows: int) -> list[dict]:
    item_id, _, layer = rec["DATASET_ID"].rpartition("_")
    svc = _arcgis_service_url(item_id)
    if not svc:
        raise RuntimeError("no FeatureServer url for item")
    qurl = f"{svc}/{layer}/query"
    out, offset = [], 0
    while len(out) < max_rows:
        page = min(ARC_PAGE, max_rows - len(out))
        r = requests.get(qurl, headers=UA, timeout=60, params={
            "where": "1=1", "outFields": "*", "f": "geojson",
            "resultRecordCount": page, "resultOffset": offset})
        r.raise_for_status()
        gj = r.json()
        feats = gj.get("features", [])
        if not feats:
            break
        for f in feats:
            row = {k: _flatten(v) for k, v in (f.get("properties") or {}).items()}
            if f.get("geometry"):
                row["GEOMETRY"] = json.dumps(f["geometry"], ensure_ascii=False)
            out.append(row)
        offset += len(feats)
        if not gj.get("properties", {}).get("exceededTransferLimit") and len(feats) < page:
            break
    return out


FETCHERS = {"SOCRATA": fetch_socrata, "ARCGIS": fetch_arcgis}


# --------------------------------------------------------------------------- #
# Load one dataset (fetch -> stamp -> land -> log -> register)
# --------------------------------------------------------------------------- #
def _already_landed(conn, table: str) -> bool:
    n = snow.fetch_scalar(
        conn,
        f"SELECT COUNT(*) FROM {db.RAW_DB}.INFORMATION_SCHEMA.TABLES "
        f"WHERE TABLE_SCHEMA='{db.RAW_SCHEMA}' AND TABLE_NAME='{table}'")
    return bool(n)


def load_one(conn, rec: dict, max_rows: int, force: bool = False) -> dict:
    sid = source_id_for(rec)
    table = sid.upper()
    if not force and _already_landed(conn, table):
        return {"source_id": sid, "status": "skip (already landed)", "rows": 0}

    started = ingest._utcnow()
    run_id = str(uuid.uuid4())
    rows = FETCHERS[rec["PLATFORM"]](rec, max_rows)
    if not rows:
        return {"source_id": sid, "status": "skip (0 rows fetched)", "rows": 0}

    df = pd.DataFrame(rows)
    df = df.loc[:, ~df.columns.duplicated()]          # drop dup column names
    sha = hashlib.sha256(ingest._df_bytes(df)).hexdigest()
    df[ingest.META_INGESTED_AT] = started.replace(tzinfo=None)
    df["_SOURCE_RUN_ID"] = run_id
    df["_SRC_SHA256"] = sha
    df = ingest._stringify(df)

    ingest._load_landing(conn, df, table, overwrite=True)
    ended = ingest._utcnow()
    ingest._log_run(conn, sid, run_id, "success", len(rows),
                    len(ingest._df_bytes(df)), sha, rec["SOURCE_URL"], started, ended,
                    f"Bulk portal load ({rec['PLATFORM']}) of {len(rows)} rows.")

    jk = rec.get("JOIN_KEYS")
    join_keys = ", ".join(json.loads(jk) if isinstance(jk, str) else (jk or [])) if jk else ""
    cfg = {
        "source_id": sid, "name": rec["DATASET_TITLE"] or sid,
        "publisher": rec["PORTAL_NAME"], "url": rec["SOURCE_URL"],
        "description": f"{rec['DATASET_TITLE']} — bulk-loaded from {rec['PORTAL_NAME']} ({rec['PLATFORM']}).",
        "access_method": "api", "format": rec["PLATFORM"].lower(), "cost": "free",
        "auth": {"type": "none"}, "join_keys": join_keys, "priority_tier": "3",
        "geographic_scope": "", "unit_of_observation": "one row = one record",
        "notes": "Auto-loaded by connect.portal_loader (no LLM).",
    }
    snow.execute(conn, *register._merge_sql(register._build_row(cfg, {})))
    return {"source_id": sid, "status": "loaded", "rows": len(rows), "platform": rec["PLATFORM"]}


def run(platform=None, with_key=False, limit=10, max_rows=500, do_run=False,
        force=False, connectable=False, verify=False) -> list[dict]:
    conn = db.connect()
    try:
        if connectable:
            cands = connectable_candidates(conn, limit=limit)
            live = live_key_types()
            print(f"selected {len(cands)} CONNECTABLE candidates "
                  f"(entity-key datasets; your live keys: {sorted(live)})")
        else:
            cands = candidates(conn, platform=platform, with_key=with_key,
                               max_rows=max_rows if max_rows > 200_000 else 200_000,
                               limit=limit)
            print(f"selected {len(cands)} candidate datasets "
                  f"(platform={platform or 'SOCRATA+ARCGIS'}, with_key={with_key})")
        if not do_run:
            for c in cands:
                print(f"  PREVIEW {c['PLATFORM']:<8} {source_id_for(c)}  "
                      f"rows~{c['ROW_COUNT']} keys={c.get('JOIN_KEYS')}  {str(c['DATASET_TITLE'])[:45]}")
            print("\n(preview only — add --run to actually load)")
            return cands
        results = []
        for c in cands:
            try:
                res = load_one(conn, c, max_rows=max_rows, force=force)
            except Exception as e:
                res = {"source_id": source_id_for(c), "status": f"ERROR: {str(e)[:90]}", "rows": 0}
            print(f"  [{res['status']:<22}] {res['source_id']}  ({res.get('rows',0)} rows)")
            results.append(res)
        landed = [r for r in results if r["status"] == "loaded"]
        print(f"\n{len(landed)}/{len(results)} loaded, {sum(r['rows'] for r in landed):,} rows total.")

        if verify and landed:
            print(f"\nverifying real connections for {len(landed)} new tables ...")
            conns = verify_connections(conn, [r["source_id"].upper() for r in landed])
            wired = {c["new"] for c in conns}
            print(f"\n{len(wired)}/{len(landed)} new tables wired into existing data "
                  f"({len(conns)} real connections).")
        return results
    finally:
        conn.close()


if __name__ == "__main__":
    run()
