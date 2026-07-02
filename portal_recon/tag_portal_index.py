#!/usr/bin/env python3
"""Wave 3 — load the harvested dataset index into Snowflake + confidence-tier
every join-key match.

Two jobs, one script:

  1. LOAD   the Wave-2 master index (portal_datasets_index.json.gz, ~338k datasets)
            into ONE Snowflake table: LIBRARY_META.REGISTRY.PORTAL_DATASET_INDEX.
            Batched. Idempotent (CREATE OR REPLACE). Count-verified against the
            source index before anything downstream is trusted.

  2. TAG    every dataset by which join keys its COLUMN NAMES actually carry, each
            at a confidence tier (STEEL / STRONG / GEO / PROBABILISTIC) — the same
            discipline as the connectivity brief. Honest matching: a column literally
            named "ein" is STEEL; a column named "id" or "name" is NOT a steel match.
            Ambiguous => tier down or skip. A false steel tag is worse than no tag.

Modes
-----
  --local      Stream the gz and compute the full tier breakdown locally. No
               Snowflake. This is the analytical core and is fully verifiable
               offline (it also independently re-counts the source index).
  --selftest   Assert the tagger on crafted column lists (no data, no network).
  --load       Create the table, batch-load it, verify the row count in Snowflake,
               add the tag columns, write the tags back, verify the distribution.
               Needs a LIVE SNOWFLAKE_PAT (REST SQL API, same path Wave 1 uses).
  --dry-run    With --load: print the DDL + a real sample batch instead of sending.

Run
---
    set -a; source ../library-onboarding/.env; set +a   # live PAT must be loaded
    python tag_portal_index.py --local                  # offline breakdown
    python tag_portal_index.py --selftest               # prove the tagger
    python tag_portal_index.py --load --dry-run         # show SQL, send nothing
    python tag_portal_index.py --load                   # do the Snowflake load+tag

Only ONE new table is written to LIBRARY_META. No dbt models, no landing tables,
no ingest of portal data.
"""

from __future__ import annotations

import argparse
import gzip
import json
import os
import sys
import time
import uuid
from collections import Counter
from pathlib import Path

# --------------------------------------------------------------------------- #
# Paths / target
# --------------------------------------------------------------------------- #
HERE = Path(__file__).resolve().parent
INDEX_GZ = HERE / "portal_datasets_index.json.gz"     # Wave-2 master asset (input)
SUMMARY_JSON = HERE / "portal_index_tier_summary.json"  # --local writes this

TARGET_DB = "LIBRARY_META"
TARGET_SCHEMA = "REGISTRY"
TARGET_TABLE = "PORTAL_DATASET_INDEX"
TARGET_FQN = f"{TARGET_DB}.{TARGET_SCHEMA}.{TARGET_TABLE}"

ACCOUNT_HOST = "oneafda-umb20733.snowflakecomputing.com"
SQL_API = f"https://{ACCOUNT_HOST}/api/v2/statements"

EXPECTED_TOTAL = 338520        # Wave-2 totals.datasets_indexed (verified at load)

# --------------------------------------------------------------------------- #
# Confidence-tier reference — the heart of the tagging.
# --------------------------------------------------------------------------- #
# Tiers, strongest first. top_tier reports the strongest tier a dataset carries.
TIER_ORDER = ["STEEL", "STRONG", "GEO", "PROBABILISTIC"]
TIER_RANK = {t: i for i, t in enumerate(TIER_ORDER)}   # lower index = stronger

# Each join key -> (tier, set of whole-token patterns it matches on).
#
# Matching is on whole TOKENS after splitting camelCase + non-alphanumerics and
# lowercasing (so 'ein' matches a column "EIN" / "ein_number" / "employerEin" but
# never "protein"). Short, ambiguous keys stay strict on purpose.
#
# STEEL keys are EXACTLY the connectivity-brief steel set — hard entity IDs only.
# Anything ambiguous is tiered down or left out (see NOTES in the brief: NDC/CUSIP
# are deliberately NOT auto-tagged steel here).
KEY_TOKENS: dict[str, tuple[str, set[str]]] = {
    # ---- STEEL — hard entity IDs (precise, trustworthy) -------------------
    "EIN":    ("STEEL", {"ein"}),
    "NPI":    ("STEEL", {"npi"}),
    "CIK":    ("STEEL", {"cik"}),
    "UEI":    ("STEEL", {"uei"}),
    "DUNS":   ("STEEL", {"duns"}),
    # BIOGUIDE — the Congressional member ID (1 letter + 6 digits, e.g. 'S000148').
    # 'bioguide' is a distinctive whole-token (no false friend anywhere), so a bare
    # token match is safe. Makes every legislator a first-class spine entity.
    "BIOGUIDE": ("STEEL", {"bioguide"}),
    # ICPSR — the Voteview/ICPSR member number (small integer, e.g. '40305'). The
    # 'icpsr' token has ONE dangerous false friend: STATE_ICPSR (a STATE code, tokens
    # -> {icpsr, state}). So ICPSR matches 'icpsr' UNLESS 'state' co-occurs on the
    # same column -- the EXCLUDE set below. (See KEY_EXCLUDE + tokens() matching.)
    "ICPSR":  ("STEEL", {"icpsr"}),
    # DOI (digital object identifier) is DELIBERATELY EXCLUDED. Auditing the 8
    # datasets a 'doi' token matched showed 0 real DOIs — every hit was "Date Of
    # Injury" (median_days_doi_to_order...) or an env-justice "Demographic Index"
    # (DOI_Aggregate/DOI_Concentration). A false steel tag is worse than no tag, so
    # we don't tag it. (Re-add only with a disambiguating co-token if ever needed.)
    "PATENT": ("STEEL", {"patent"}),
    "LEI":    ("STEEL", {"lei"}),
    "IMO":    ("STEEL", {"imo"}),
    "MMSI":   ("STEEL", {"mmsi"}),
    "CCN":    ("STEEL", {"ccn"}),
    # ---- STRONG — domain-native IDs --------------------------------------
    "DOCKET": ("STRONG", {"docket"}),
    "NAICS":  ("STRONG", {"naics"}),
    "NCES":   ("STRONG", {"nces"}),
    "SIC":    ("STRONG", {"sic"}),
    # ---- GEO — abundant but coarse ---------------------------------------
    "FIPS":    ("GEO", {"fips", "geoid", "geoid10", "geoid20", "statefp", "countyfp"}),
    "ZIP":     ("GEO", {"zip", "zipcode", "zip5", "zcta", "zcta5", "postcode", "postalcode"}),
    "LATLON":  ("GEO", {"lat", "latitude", "lon", "lng", "longitude", "latdd", "londd"}),
    "COUNTRY": ("GEO", {"country", "countrycode", "iso2", "iso3", "iso3166", "cntry"}),
    "GEOM":    ("GEO", {"geom", "geometry", "thegeom", "wkt", "wkb", "shape", "latlong", "lnglat"}),
    # ---- PROBABILISTIC — name/address only (fuzzy, never clean) -----------
    "NAME":    ("PROBABILISTIC", {
        "name", "fullname", "firstname", "lastname", "surname", "lname", "fname",
        "mname", "businessname", "orgname", "companyname",
        "company", "organization", "vendor", "recipient", "grantee", "employer",
        "applicant", "borrower", "payee",
    }),
    "ADDRESS": ("PROBABILISTIC", {"address", "addr", "street", "streetaddress", "mailingaddress"}),
}

# Pair rules: a key matches only if BOTH tokens appear somewhere in the column set.
# (catches "postal_code" -> {postal, code}, which neither single token covers.)
PAIR_RULES: list[tuple[str, tuple[str, str]]] = [
    ("ZIP", ("postal", "code")),
]

# Exclusion tokens: a key matches its KEY_TOKENS only if NONE of these co-occur in
# the SAME token set. This is how we disambiguate a false friend that shares a
# token with a real key -- e.g. STATE_ICPSR (a state code, tokens {icpsr, state})
# must NOT tag as the member key ICPSR. The 'state' token vetoes the ICPSR match.
# (The DOI note above wanted exactly this kind of disambiguating co-token guard.)
KEY_EXCLUDE: dict[str, set[str]] = {
    "ICPSR": {"state"},
}

import re

_CAMEL = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")
_NONALNUM = re.compile(r"[^A-Za-z0-9]+")


def tokens(name: str) -> set[str]:
    """Split a column name into lowercase tokens: camelCase + non-alphanumerics."""
    s = _CAMEL.sub(" ", str(name))
    return {t for t in _NONALNUM.split(s.lower()) if t}


def tag_columns(columns) -> tuple[list[str] | None, str | None]:
    """Confidence-tier a dataset from its column names.

    Returns (join_keys, top_tier):
      - columns is None/unknown -> (None, None)        : unassessable (no columns)
      - columns known, no key   -> ([],   "NONE")      : assessed, carries nothing
      - columns known, keys hit -> (keys, strongest)   : sorted keys + best tier

    'keys' is the list of matched join-key labels (e.g. ["EIN","FIPS","NAME"]),
    ordered strongest tier first then alphabetically.
    """
    if not columns:
        return None, None
    all_tokens: set[str] = set()
    for col in columns:
        all_tokens |= tokens(col)

    matched: list[str] = []
    for key, (_tier, toks) in KEY_TOKENS.items():
        if (all_tokens & toks) and not (all_tokens & KEY_EXCLUDE.get(key, set())):
            matched.append(key)
    for key, (a, b) in PAIR_RULES:
        if key not in matched and a in all_tokens and b in all_tokens:
            matched.append(key)

    if not matched:
        return [], "NONE"

    matched.sort(key=lambda k: (TIER_RANK[KEY_TOKENS[k][0]], k))
    top_tier = KEY_TOKENS[matched[0]][0]
    return matched, top_tier


# --------------------------------------------------------------------------- #
# source_url — best-effort dataset URL (explicit where the API gave one, else the
# platform-standard dataset page). Never fabricated beyond the platform convention.
# --------------------------------------------------------------------------- #
def derive_source_url(rec: dict) -> str:
    plat = rec.get("platform")
    base = (rec.get("portal_base_url") or "").rstrip("/")
    did = rec.get("dataset_id") or ""
    if plat == "SOCRATA":
        return rec.get("permalink") or (f"{base}/d/{did}" if base and did else base)
    if plat == "ARCGIS":
        return rec.get("feature_server_url") or (f"{base}/datasets/{did}" if base and did else base)
    if plat == "CKAN":
        return f"{base}/dataset/{did}" if base and did else base
    return base


# --------------------------------------------------------------------------- #
# Streaming reader — never holds more than a small buffer of the 360MB JSON.
# --------------------------------------------------------------------------- #
def stream_datasets(path: Path = INDEX_GZ):
    """Yield each dataset record from the gz index's top-level "datasets":[...] array
    without loading the whole 360MB document into memory."""
    dec = json.JSONDecoder()
    marker = '"datasets":['
    with gzip.open(path, "rt", encoding="utf-8") as f:
        # Advance to the start of the datasets array.
        buf = f.read(4_000_000)
        idx = buf.find(marker)
        while idx == -1:
            more = f.read(4_000_000)
            if not more:
                raise ValueError('could not find "datasets":[ in index')
            buf = buf[-32:] + more
            idx = buf.find(marker)
        buf = buf[idx + len(marker):]

        while True:
            buf = buf.lstrip().lstrip(",").lstrip()
            if buf[:1] == "]":
                return
            try:
                obj, end = dec.raw_decode(buf)
            except ValueError:
                more = f.read(2_000_000)
                if not more:
                    return
                buf += more
                continue
            yield obj
            buf = buf[end:]


def to_row(rec: dict, uid: int) -> dict:
    """Map a Wave-2 record to a target-table row (+ computed tags)."""
    cols = rec.get("columns")
    join_keys, top_tier = tag_columns(cols)
    return {
        "dataset_uid": uid,
        "portal_source_id": rec.get("portal_source_id") or "",
        "portal_name": rec.get("portal_name") or "",
        "platform": rec.get("platform") or "",
        "dataset_title": rec.get("dataset_title") or "",
        "dataset_id": rec.get("dataset_id") or "",
        "column_names": cols,                    # list | None
        "row_count": rec.get("row_count"),       # int | None
        "last_updated": rec.get("last_updated"),  # str | None
        "source_url": derive_source_url(rec),
        "join_keys": join_keys,                  # list | None
        "top_tier": top_tier,                    # str | None
    }


# --------------------------------------------------------------------------- #
# --local — compute + report the full breakdown offline
# --------------------------------------------------------------------------- #
def cmd_local() -> int:
    t0 = time.time()
    total = 0
    cols_known = 0
    by_tier = Counter()          # top_tier (incl. NONE / UNKNOWN_COLUMNS)
    by_key = Counter()           # each matched join key
    by_platform = Counter()
    steel_by_key = Counter()
    geo_and_steel = 0
    ein_carriers = 0

    for rec in stream_datasets():
        total += 1
        by_platform[rec.get("platform") or "?"] += 1
        cols = rec.get("columns")
        join_keys, top_tier = tag_columns(cols)
        if cols is None:
            by_tier["UNKNOWN_COLUMNS"] += 1
            continue
        cols_known += 1
        by_tier[top_tier] += 1
        if join_keys:
            tiers_present = set()
            for k in join_keys:
                by_key[k] += 1
                t = KEY_TOKENS.get(k, ("PROBABILISTIC", set()))[0]
                tiers_present.add(t)
                if t == "STEEL":
                    steel_by_key[k] += 1
            if "EIN" in join_keys:
                ein_carriers += 1
            if "GEO" in tiers_present and "STEEL" in tiers_present:
                geo_and_steel += 1

    dt = time.time() - t0
    has_any_key = sum(by_tier[t] for t in TIER_ORDER)
    no_key = by_tier["NONE"]
    unknown_cols = by_tier["UNKNOWN_COLUMNS"]

    print("=" * 64)
    print("WAVE 3 — LOCAL TIER BREAKDOWN (computed from the source index)")
    print("=" * 64)
    print(f"source index           : {INDEX_GZ.name}")
    print(f"datasets streamed      : {total:,}   (expected {EXPECTED_TOTAL:,})")
    print(f"  columns exposed      : {cols_known:,}")
    print(f"  columns UNKNOWN      : {unknown_cols:,}   (cannot be join-tagged)")
    print(f"streamed in            : {dt:.1f}s")
    print("-" * 64)
    print("BY TOP TIER (of the column-known set):")
    for t in TIER_ORDER:
        print(f"  {t:<14}: {by_tier[t]:>8,}")
    print(f"  {'NONE':<14}: {no_key:>8,}   (columns known, no key matched)")
    print(f"  carries a key : {has_any_key:>8,}")
    print("-" * 64)
    print("BY JOIN KEY (a dataset can carry several):")
    for k, n in sorted(by_key.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"  {k:<10} [{KEY_TOKENS.get(k,('?',))[0]:<13}] : {n:>8,}")
    print("-" * 64)
    print("STEEL detail (precise IDs — eyeball these):")
    for k, n in sorted(steel_by_key.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"  {k:<10}: {n:>8,}")
    print("-" * 64)
    print(f"datasets carrying EIN           : {ein_carriers:,}")
    print(f"datasets carrying GEO + STEEL   : {geo_and_steel:,}   (cross-joinable gold)")
    print("-" * 64)
    print("BY PORTAL PLATFORM:")
    for p, n in by_platform.most_common():
        print(f"  {p:<10}: {n:>8,}")
    print("=" * 64)

    if total != EXPECTED_TOTAL:
        print(f"[WARN] streamed {total:,} != expected {EXPECTED_TOTAL:,} — investigate.")

    summary = {
        "source_index": INDEX_GZ.name,
        "datasets_total": total,
        "expected_total": EXPECTED_TOTAL,
        "columns_known": cols_known,
        "columns_unknown": unknown_cols,
        "by_top_tier": {t: by_tier[t] for t in TIER_ORDER},
        "none_no_key": no_key,
        "carries_a_key": has_any_key,
        "by_join_key": dict(by_key),
        "steel_by_key": dict(steel_by_key),
        "ein_carriers": ein_carriers,
        "geo_and_steel": geo_and_steel,
        "by_platform": dict(by_platform),
    }
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2))
    print(f"wrote {SUMMARY_JSON.name}")
    return 0 if total == EXPECTED_TOTAL else 1


# --------------------------------------------------------------------------- #
# --selftest — prove the tagger (no data, no network)
# --------------------------------------------------------------------------- #
def cmd_selftest() -> int:
    cases = [
        # (columns, expect_keys_subset, expect_top_tier)
        (["EIN", "name"], {"EIN", "NAME"}, "STEEL"),
        (["ein_number", "amount"], {"EIN"}, "STEEL"),
        (["npi", "provider_zip"], {"NPI", "ZIP"}, "STEEL"),
        (["state_fips", "county_fips"], {"FIPS"}, "GEO"),
        (["latitude", "longitude"], {"LATLON"}, "GEO"),
        (["the_geom", "resolution"], {"GEOM"}, "GEO"),
        (["postal_code"], {"ZIP"}, "GEO"),
        (["naics_code", "company"], {"NAICS", "NAME"}, "STRONG"),
        (["country", "iso3"], {"COUNTRY"}, "GEO"),
        (["full_name", "address"], {"NAME", "ADDRESS"}, "PROBABILISTIC"),
        # politician IDs (Step-K politics) — first-class STEEL member keys
        (["bioguide", "name_last"], {"BIOGUIDE", "NAME"}, "STEEL"),
        (["icpsr", "party_code"], {"ICPSR"}, "STEEL"),
        (["icpsr_id", "congress"], {"ICPSR"}, "STEEL"),
        # honest non-matches: generic columns are NOT keys
        (["id", "value", "date"], set(), "NONE"),
        (["protein", "weight"], set(), "NONE"),     # 'protein' must NOT match EIN
        (["description", "status"], set(), "NONE"),
        (["state_icpsr", "party_code"], set(), "NONE"),  # STATE_ICPSR is a STATE code, NOT member ICPSR
        (["fec_case_ids", "status"], set(), "NONE"),     # EPA Formal-Enforcement-Case, NOT an FEC key
        ([], None, None),                            # empty -> unassessable
        (None, None, None),                          # unknown -> unassessable
    ]
    ok = True
    for cols, want_keys, want_tier in cases:
        keys, tier = tag_columns(cols)
        keyset = set(keys) if keys else (set() if keys == [] else None)
        passed = (tier == want_tier) and (
            want_keys is None and keys is None
            or want_keys is not None and keyset is not None and want_keys <= keyset
        )
        # for the non-match cases require EXACT empty
        if want_keys == set():
            passed = passed and keyset == set()
        flag = "ok " if passed else "FAIL"
        ok = ok and passed
        print(f"  [{flag}] cols={cols!r:<42} -> keys={keys} tier={tier}")
    print("SELFTEST:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


# --------------------------------------------------------------------------- #
# Snowflake REST SQL API (same path Wave 1 uses) — only touched by --load
# --------------------------------------------------------------------------- #
class SnowflakeError(RuntimeError):
    pass


def _pat() -> str:
    pat = os.environ.get("SNOWFLAKE_PAT", "").strip()
    if not pat:
        raise SnowflakeError(
            "SNOWFLAKE_PAT is not set. Load the live PAT first:\n"
            "  set -a; source ../library-onboarding/.env; set +a"
        )
    return pat


def sf_sql(statement: str, pat: str, warehouse: str | None = None, timeout: int = 120) -> list[dict]:
    """Run one statement via the SQL REST API; return rows as list-of-dicts.

    Handles the async (202) handle-poll and reads inline result partitions. Our
    write batches and verification queries are small, so first-partition reads
    are sufficient for the SELECTs here.
    """
    import requests

    headers = {
        "Authorization": f"Bearer {pat}",
        "X-Snowflake-Authorization-Token-Type": "PROGRAMMATIC_ACCESS_TOKEN",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "ripple-portal-wave3/1.0",
    }
    body: dict = {"statement": statement, "timeout": timeout}
    if warehouse:
        body["warehouse"] = warehouse
    resp = requests.post(SQL_API, headers=headers,
                         params={"requestId": str(uuid.uuid4())},
                         json=body, timeout=timeout + 15)
    if resp.status_code == 401:
        raise SnowflakeError(
            "PAT rejected (401 — 'Programmatic access token is invalid'). The token "
            "is revoked/expired. Drop a fresh one into ../library-onboarding/.env "
            "(SNOWFLAKE_PAT=...) and reload it; it must beat any stale container value."
        )
    try:
        payload = resp.json()
    except ValueError:
        raise SnowflakeError(f"Non-JSON response (HTTP {resp.status_code}): {resp.text[:200]}")

    # Async: poll the statement handle until it finishes.
    handle = payload.get("statementHandle")
    if resp.status_code == 202 and handle:
        for _ in range(120):
            time.sleep(1.0)
            r2 = requests.get(f"{SQL_API}/{handle}", headers=headers,
                              params={"requestId": str(uuid.uuid4())}, timeout=60)
            if r2.status_code == 202:
                continue
            payload = r2.json()
            resp = r2
            break
    if resp.status_code not in (200, 202):
        raise SnowflakeError(f"HTTP {resp.status_code}: {payload.get('message', payload)}")

    meta = payload.get("resultSetMetaData", {})
    cols = [c["name"] for c in meta.get("rowType", [])]
    data = payload.get("data", []) or []
    return [dict(zip(cols, row)) for row in data]


def pick_warehouse(pat: str) -> str | None:
    """A table scan/insert needs a warehouse. Prefer the account-default, else the
    first one SHOW WAREHOUSES returns (both run on cloud services, no warehouse)."""
    wh = os.environ.get("SNOWFLAKE_WAREHOUSE", "").strip()
    if wh:
        return wh
    try:
        rows = sf_sql("SELECT CURRENT_WAREHOUSE() AS W", pat, timeout=30)
        if rows and rows[0].get("W"):
            print(f"  using account-default warehouse: {rows[0]['W']}")
            return rows[0]["W"]
    except SnowflakeError:
        pass
    rows = sf_sql("SHOW WAREHOUSES", pat)
    if rows:
        name = rows[0].get("name") or rows[0].get("NAME")
        print(f"  no default warehouse; using discovered: {name}")
        return name
    return None


# ---- SQL literal helpers (inline literals; --dry-run prints a real batch) ----
def _s(v) -> str:
    if v is None:
        return "NULL"
    s = str(v).replace("\\", "\\\\").replace("'", "''")
    s = s.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    return "'" + s + "'"


def _i(v) -> str:
    if v is None:
        return "NULL"
    try:
        return str(int(v))
    except (TypeError, ValueError):
        return "NULL"


def _json_lit(arr) -> str:
    """A SQL STRING literal holding the JSON for an array column (NOT wrapped in
    PARSE_JSON — the outer SELECT does that, the standard/robust idiom). Dollar-quote
    to dodge escaping, with a single-quote-escaped fallback if the (vanishingly rare)
    content holds '$$'."""
    if arr is None:
        return "NULL"
    js = json.dumps(arr, ensure_ascii=True)
    if "$$" not in js:
        return f"$${js}$$"
    esc = js.replace("\\", "\\\\").replace("'", "''")
    return f"'{esc}'"


DDL = f"""CREATE OR REPLACE TABLE {TARGET_FQN} (
    dataset_uid       NUMBER        NOT NULL,
    portal_source_id  STRING,
    portal_name       STRING,
    platform          STRING,
    dataset_title     STRING,
    dataset_id        STRING,
    column_names      ARRAY,
    row_count         NUMBER,
    last_updated      STRING,
    source_url        STRING
)
COMMENT = 'Wave-3 master index of harvested open-data-portal datasets (metadata only). One row = one dataset. column_names is the source column list; join_keys/top_tier (added post-load) confidence-tier what each dataset connects to.'"""

ALTER_TAGS = f"""ALTER TABLE {TARGET_FQN}
    ADD COLUMN join_keys ARRAY,
               top_tier  STRING"""

BASE_COLS = ("dataset_uid", "portal_source_id", "portal_name", "platform",
             "dataset_title", "dataset_id", "column_names", "row_count",
             "last_updated", "source_url")


def _base_values_row(r: dict) -> str:
    # column7 (column_names) is a JSON STRING literal here; the SELECT PARSE_JSONs it.
    return ("(" + ", ".join([
        _i(r["dataset_uid"]), _s(r["portal_source_id"]), _s(r["portal_name"]),
        _s(r["platform"]), _s(r["dataset_title"]), _s(r["dataset_id"]),
        _json_lit(r["column_names"]), _i(r["row_count"]), _s(r["last_updated"]),
        _s(r["source_url"]),
    ]) + ")")


def _base_insert_sql(batch: list[dict]) -> str:
    vals = ",\n".join(_base_values_row(r) for r in batch)
    # JSON string in VALUES, PARSE_JSON(...)::ARRAY in the SELECT — the robust idiom.
    sel = ("column1, column2, column3, column4, column5, column6, "
           "TRY_PARSE_JSON(column7)::ARRAY, column8, column9, column10")
    return (f"INSERT INTO {TARGET_FQN} ({', '.join(BASE_COLS)})\n"
            f"SELECT {sel} FROM VALUES\n{vals}")


def _tag_update_sql(batch: list[dict]) -> str:
    vals = ",\n".join(
        f"({_i(r['dataset_uid'])}, {_json_lit(r['join_keys'])}, {_s(r['top_tier'])})"
        for r in batch
    )
    return (f"UPDATE {TARGET_FQN} t\n"
            f"SET join_keys = s.jk, top_tier = s.tt\n"
            f"FROM (SELECT column1::number AS uid,\n"
            f"             TRY_PARSE_JSON(column2)::ARRAY AS jk,\n"
            f"             column3 AS tt\n"
            f"      FROM VALUES\n{vals}) s\n"
            f"WHERE t.dataset_uid = s.uid")


def cmd_load(batch_size: int, dry_run: bool, limit: int | None) -> int:
    print("=" * 64)
    print(f"WAVE 3 — LOAD + TAG  ->  {TARGET_FQN}")
    print("=" * 64)

    # Read + tag the whole index in memory as compact rows (338k small dicts).
    print("reading + tagging the source index ...")
    rows: list[dict] = []
    for i, rec in enumerate(stream_datasets()):
        rows.append(to_row(rec, i))
        if limit and len(rows) >= limit:
            break
    source_count = len(rows)
    print(f"  rows prepared: {source_count:,}")

    if dry_run:
        print("\n--- DRY RUN: DDL ---\n" + DDL)
        print("\n--- DRY RUN: sample base INSERT (first 2 rows) ---")
        print(_base_insert_sql(rows[:2]))
        print("\n--- DRY RUN: ALTER ---\n" + ALTER_TAGS)
        tagged = [r for r in rows[:50] if r["top_tier"] is not None]
        print("\n--- DRY RUN: sample tag UPDATE (first 2 tagged rows) ---")
        print(_tag_update_sql(tagged[:2]) if tagged else "(no tagged rows in sample)")
        print("\nDRY RUN complete — nothing was sent to Snowflake.")
        return 0

    pat = _pat()
    wh = pick_warehouse(pat)
    if not wh:
        raise SnowflakeError("No warehouse available — set SNOWFLAKE_WAREHOUSE.")

    # 1) Create the table (idempotent).
    print(f"\n[1] CREATE OR REPLACE TABLE {TARGET_FQN}")
    sf_sql(DDL, pat, wh)

    # 2) Batched base load.
    print(f"[2] loading {source_count:,} rows in batches of {batch_size} ...")
    for start in range(0, source_count, batch_size):
        batch = rows[start:start + batch_size]
        sf_sql(_base_insert_sql(batch), pat, wh)
        if (start // batch_size) % 25 == 0:
            print(f"    {min(start + batch_size, source_count):,}/{source_count:,}")

    # 3) Verify the row count in Snowflake BEFORE we trust any tagging.
    print("[3] verifying row count in Snowflake (gate) ...")
    rc = sf_sql(f"SELECT COUNT(*) AS N FROM {TARGET_FQN}", pat, wh)
    loaded = int(rc[0]["N"])
    print(f"    Snowflake COUNT(*) = {loaded:,}   source = {source_count:,}")
    if loaded != source_count:
        raise SnowflakeError(
            f"ROW COUNT MISMATCH: Snowflake {loaded:,} != source {source_count:,}. "
            "Refusing to tag an unverified table."
        )
    print("    ✓ count verified.")

    # 4) Add the tag columns.
    print("[4] adding tag columns join_keys, top_tier ...")
    sf_sql(ALTER_TAGS, pat, wh)

    # 5) Write tags back (only the column-known rows carry a tier).
    taggable = [r for r in rows if r["top_tier"] is not None]
    print(f"[5] writing tags for {len(taggable):,} column-known rows ...")
    for start in range(0, len(taggable), batch_size):
        batch = taggable[start:start + batch_size]
        sf_sql(_tag_update_sql(batch), pat, wh)
        if (start // batch_size) % 25 == 0:
            print(f"    {min(start + batch_size, len(taggable)):,}/{len(taggable):,}")

    # 6) Verify the tag distribution.
    print("[6] tag distribution in Snowflake:")
    dist = sf_sql(
        f"SELECT COALESCE(top_tier,'UNKNOWN_COLUMNS') AS TIER, COUNT(*) AS N "
        f"FROM {TARGET_FQN} GROUP BY 1 ORDER BY 2 DESC", pat, wh)
    for row in dist:
        print(f"    {row['TIER']:<16}: {int(row['N']):>8,}")
    print("=" * 64)
    print(f"DONE. Master index now lives in {TARGET_FQN}.")
    print("git no longer needs the 57MB gz — the queryable truth is in Snowflake.")
    return 0


# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser(description="Wave 3 — load + confidence-tier the portal dataset index.")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--local", action="store_true", help="offline tier breakdown (no Snowflake)")
    g.add_argument("--selftest", action="store_true", help="prove the tagger (no data/network)")
    g.add_argument("--load", action="store_true", help="load + tag in Snowflake (needs live PAT)")
    ap.add_argument("--dry-run", action="store_true", help="with --load: print SQL, send nothing")
    ap.add_argument("--batch", type=int, default=1000, help="rows per Snowflake statement (default 1000)")
    ap.add_argument("--limit", type=int, default=None, help="cap rows (smoke test only)")
    args = ap.parse_args()

    if args.selftest:
        return cmd_selftest()
    if args.local:
        return cmd_local()
    if args.load:
        return cmd_load(args.batch, args.dry_run, args.limit)
    return 2


if __name__ == "__main__":
    sys.exit(main())
