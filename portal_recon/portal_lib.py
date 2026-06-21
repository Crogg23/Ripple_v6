#!/usr/bin/env python3
"""Wave 2 — shared politeness + helpers for the platform index readers.

Wave 1 fingerprinted each portal's PLATFORM (Socrata / CKAN / ArcGIS / ...).
Wave 2 opens each confirmed portal and harvests the INDEX of every dataset inside
it: title, dataset ID, column/field names, row count, last-updated. This is
METADATA harvesting — nothing is downloaded or ingested, nothing touches landing.

This module is the shared layer every reader (arcgis/socrata/ckan) reuses:
  - one polite HTTP session (normal identifying UA, short timeouts, no retries)
  - a bounded JSON GET that never holds more than one page in memory
  - the standard per-dataset record shape (so all three readers emit the same thing)
  - the light join-key flag (STEP 3) — a cheap "does this column list carry a known
    join key?" boolean, NOT the full Wave-3 tagging
  - input loading (the Wave 1 results) + missing-field discipline (unknown != guess)

POLITENESS IS MANDATORY. Every reader paginates, caps per-portal work, pauses
between requests to one host, and identifies itself. These are public servers.
"""

from __future__ import annotations

import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests

# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #
HERE = Path(__file__).resolve().parent
INPUT_FILE = HERE / "portal_recon_results.json"          # Wave 1 output (input)
INDEX_JSON = HERE / "portal_datasets_index.json"         # Wave 2 master asset
INDEX_MD = HERE / "portal_datasets_index.md"             # Wave 2 human summary

# --------------------------------------------------------------------------- #
# Politeness budget (be a good citizen — these are public servers)
# --------------------------------------------------------------------------- #
# A normal browser User-Agent. Many of these public open-data APIs sit behind
# Cloudflare, whose generic bot rules return 502 to a custom bot UA even though the
# CKAN/Socrata/ArcGIS endpoints are built for programmatic access. A normal browser
# UA is what gets served; we stay good citizens through RATE (delays, caps,
# pagination, one-retry) — never through volume.
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
CONNECT_TIMEOUT = 5          # seconds to connect — short on purpose
READ_TIMEOUT = 20            # seconds to read one metadata page
REQUEST_DELAY = 0.25         # courtesy pause between requests to the SAME host
PAGE_SIZE = 100              # datasets per page (all three APIs page in 100s fine)
PER_PORTAL_MAX_DATASETS = 25000  # cap: one giant portal can't run forever (Chris: 25k)
PER_PORTAL_MAX_PAGES = 300       # hard stop on pagination regardless of count (250 pp = 25k)
PER_PORTAL_MAX_SECONDS = 300     # wall-clock budget/portal: a slow straggler can't stall the run
                                 # (a 25k portal at normal speed finishes well inside this)


# --------------------------------------------------------------------------- #
# HTTP — one polite, bounded GET
# --------------------------------------------------------------------------- #
def make_session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json, */*"})
    return s


TRANSIENT_STATUSES = {429, 502, 503, 504}   # worth ONE gentle retry, not more
RETRY_PAUSE = 1.5                           # seconds before the single retry


def get_json(session: requests.Session, url: str,
             timeout: tuple[int, int] | None = None,
             retries: int = 1) -> tuple[int | None, object, str | None]:
    """One polite GET returning (status, parsed_json_or_None, error_or_None).

    At most ONE retry, and only on a transient failure (a network/timeout error,
    or a 429/502/503/504 server blip) after a short pause — never a tight loop, so
    a portal is never hammered. A persistent error or non-JSON body is logged and
    skipped via (status, None, reason).
    """
    last = (None, None, "no attempt")
    for attempt in range(retries + 1):
        try:
            resp = session.get(url, timeout=timeout or (CONNECT_TIMEOUT, READ_TIMEOUT))
        except requests.RequestException as e:
            last = (None, None, f"{type(e).__name__}")
            if attempt < retries:
                time.sleep(RETRY_PAUSE)
                continue
            return last
        if resp.status_code == 200:
            try:
                return resp.status_code, resp.json(), None
            except ValueError:
                ct = resp.headers.get("content-type", "?")
                return resp.status_code, None, f"non-JSON body (content-type={ct})"
        last = (resp.status_code, None, f"HTTP {resp.status_code}")
        if resp.status_code in TRANSIENT_STATUSES and attempt < retries:
            time.sleep(RETRY_PAUSE)
            continue
        return last
    return last


def host_of(url: str) -> str:
    """Bare hostname for a URL (the domains/util endpoints want host, not scheme)."""
    if not re.match(r"^https?://", url or "", re.I):
        url = "https://" + (url or "").strip()
    return urlparse(url).netloc


def pause() -> None:
    time.sleep(REQUEST_DELAY)


def expired(t_start: float, budget: float | None = None) -> bool:
    """True once a portal has used its wall-clock budget — checked between pages so
    a slow portal returns partial results instead of stalling the whole run."""
    return (time.time() - t_start) > (budget if budget is not None else PER_PORTAL_MAX_SECONDS)


# --------------------------------------------------------------------------- #
# Missing-field discipline — unknown is null, never a guess
# --------------------------------------------------------------------------- #
def clean_count(value) -> int | None:
    """A row/record count is real only if the API gave a non-negative integer.
    Esri returns -1 for 'not counted'; many APIs omit it. Those are UNKNOWN (None).
    0 is a legitimate count (an empty dataset) and is kept."""
    if value is None:
        return None
    try:
        n = int(value)
    except (TypeError, ValueError):
        return None
    return n if n >= 0 else None


def epoch_ms_to_iso(value) -> str | None:
    """Convert an epoch-milliseconds timestamp to an ISO-8601 UTC string.
    None / 0 / unparseable => UNKNOWN (None), never a fabricated date."""
    if not value:
        return None
    try:
        ms = int(value)
    except (TypeError, ValueError):
        return None
    if ms <= 0:
        return None
    try:
        return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).isoformat()
    except (OverflowError, OSError, ValueError):
        return None


def clean_iso(value) -> str | None:
    """Pass through a string date the API already returned (Socrata/CKAN ISO),
    else UNKNOWN. We don't reformat — we just refuse to invent one."""
    if not value or not isinstance(value, str):
        return None
    v = value.strip()
    return v or None


def clean_columns(names) -> list[str] | None:
    """A column list is real only if the API returned a non-empty list of names.
    Missing / empty => UNKNOWN (None). De-dupes while preserving order."""
    if not names or not isinstance(names, (list, tuple)):
        return None
    seen, out = set(), []
    for n in names:
        if n is None:
            continue
        s = str(n).strip()
        if s and s not in seen:
            seen.add(s)
            out.append(s)
    return out or None


# --------------------------------------------------------------------------- #
# STEP 3 — light join-key flag (cheap first signal, NOT the Wave-3 tagging)
# --------------------------------------------------------------------------- #
# Short, ambiguous keys are matched on whole TOKENS (so 'ein' matches a column
# named "EIN"/"ein_number" but never "protein"). camelCase is split first.
_JOIN_KEY_TOKENS: dict[str, set[str]] = {
    "EIN":   {"ein"},
    "NPI":   {"npi"},
    "NDC":   {"ndc"},
    "CIK":   {"cik"},
    "UEI":   {"uei"},
    "LEI":   {"lei"},
    "DUNS":  {"duns"},
    "MMSI":  {"mmsi"},
    "NAICS": {"naics"},
    "SIC":   {"sic"},
    "FIPS":  {"fips", "geoid", "geoid10", "geoid20"},
    "ZIP":   {"zip", "zipcode", "zcta", "postalcode"},
    "LATLON": {"lat", "latitude", "lon", "lng", "longitude", "latdd", "londd"},
    "COUNTRY_ISO": {"iso", "iso2", "iso3", "iso3166", "countrycode"},
}


def _tokens(name: str) -> set[str]:
    """Split a column name into lowercase tokens: camelCase + non-alphanumerics."""
    s = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", str(name))
    return {t for t in re.split(r"[^A-Za-z0-9]+", s.lower()) if t}


def flag_join_keys(columns) -> tuple[bool, list[str]]:
    """Cheap pass: does this column list look like it carries any known join key?
    Returns (has_join_key, sorted list of which keys matched). Columns unknown
    (None) => (False, []) — we never flag what we couldn't read."""
    if not columns:
        return False, []
    all_tokens: set[str] = set()
    for col in columns:
        all_tokens |= _tokens(col)
    matched = [key for key, toks in _JOIN_KEY_TOKENS.items() if all_tokens & toks]
    # normalize label for the lat/lon pair
    matched = ["lat/lon" if k == "LATLON" else k for k in matched]
    return (bool(matched), sorted(matched))


# --------------------------------------------------------------------------- #
# Standard per-dataset record (every reader emits exactly this shape)
# --------------------------------------------------------------------------- #
def make_dataset_record(portal: dict, *, dataset_id, dataset_title,
                        columns=None, row_count=None, last_updated=None,
                        resource_type=None, extra=None) -> dict:
    cols = clean_columns(columns)
    has_key, keys = flag_join_keys(cols)
    rec = {
        "portal_source_id": portal.get("source_id", ""),
        "portal_name": portal.get("name", ""),
        "portal_base_url": portal.get("base_url", ""),
        "platform": portal.get("platform", ""),
        "dataset_id": dataset_id,
        "dataset_title": dataset_title,
        "columns": cols,                                   # list | None (unknown)
        "column_count": (len(cols) if cols is not None else None),
        "row_count": clean_count(row_count),               # int | None (unknown)
        "last_updated": last_updated,                       # iso str | None
        "resource_type": resource_type,                    # platform-specific | None
        "has_join_key": has_key,
        "join_keys_matched": keys,
    }
    if extra:
        rec.update(extra)
    return rec


def portal_result(portal: dict, *, status: str, datasets: list,
                  error: str | None = None, capped: bool = False,
                  api_base: str | None = None, notes: str = "") -> dict:
    """Per-portal harvest log entry — captures the outcome even on failure so a
    dead portal is visible in the index, not silently dropped."""
    return {
        "portal_source_id": portal.get("source_id", ""),
        "portal_name": portal.get("name", ""),
        "portal_base_url": portal.get("base_url", ""),
        "platform": portal.get("platform", ""),
        "api_base": api_base or portal.get("api_base", ""),
        "status": status,                  # "ok" | "empty" | "error"
        "error": error,
        "dataset_count": len(datasets),
        "capped": capped,
        "notes": notes,
    }


# --------------------------------------------------------------------------- #
# Input — the Wave 1 confirmed portals
# --------------------------------------------------------------------------- #
def load_confirmed_portals(platform: str | None = None) -> list[dict]:
    """Load Wave 1 results; return the platform-confirmed portals (optionally one
    platform). Keeps both API-confirmed ('pass-1'/'subpath'/'redirect-reprobe')
    and the softer 'branding' detections (those have no api_base — the reader
    derives it and may fail gracefully)."""
    data = json.loads(INPUT_FILE.read_text())
    results = data.get("results", [])
    out = []
    for r in results:
        plat = r.get("platform", "")
        if plat in ("UNKNOWN", ""):
            continue
        if platform and plat != platform:
            continue
        out.append(r)
    return out
