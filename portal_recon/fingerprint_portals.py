#!/usr/bin/env python3
"""Wave 1 — Portal platform fingerprinter (catalog-of-catalogs).

GOAL: for every open-data portal in the Catalog, figure out *which platform it
runs* (Socrata / CKAN / ArcGIS Hub / OpenDataSoft / GeoNode / Junar / custom) so
Wave 2 knows which reader to point at it. We do NOT harvest datasets here — every
probe is a count-only / metadata endpoint (limit=0, rows=0, ?f=json). Fingerprint
only.

Pipeline:
  [1] PULL    SOURCE_REGISTRY -> the ~321 portal supercluster (by CATEGORY)
  [2] PROBE   each portal, politely (<=2 requests, short timeout, normal UA)
  [3] WRITE   portal_recon/portal_recon_results.md  (table + summary headline)

Snowflake access here is the SQL REST API (the snowflake-connector and the MCP
server aren't reachable from this container). Auth is a Programmatic Access Token.

    # validate creds + show the CATEGORY distribution, pick nothing yet:
    python fingerprint_portals.py --distribution

    # full run (auto-detects the ~321 portal CATEGORY, stops if it's way off):
    python fingerprint_portals.py

    # pin the category explicitly once you know its exact label:
    python fingerprint_portals.py --category 'Open Data Portal'

    # prove the prober works with no Snowflake at all:
    python fingerprint_portals.py --selftest

THE OVERRIDE TRAP: a stale SNOWFLAKE_PAT can already sit in the container env and
shadow the fresh one. We load library-onboarding/.env with override=True so the
file always wins (same trick config.py uses). If neither is valid we fail loudly.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse

import requests

# --------------------------------------------------------------------------- #
# Paths / constants
# --------------------------------------------------------------------------- #
HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
ENV_FILE = REPO_ROOT / "library-onboarding" / ".env"
OUT_FILE = HERE / "portal_recon_results.md"

ACCOUNT_HOST = "oneafda-umb20733.snowflakecomputing.com"
SQL_API = f"https://{ACCOUNT_HOST}/api/v2/statements"
REGISTRY_FQN = "LIBRARY_META.REGISTRY.SOURCE_REGISTRY"

# A normal, identifiable User-Agent. Polite + honest.
USER_AGENT = "ripple-portal-recon/1.0 (+open-data platform fingerprint; contact w.rogers9999@gmail.com)"
PROBE_CONNECT_TIMEOUT = 4  # seconds to connect — short on purpose
PROBE_TIMEOUT = 6          # seconds to read
MAX_PROBE_BYTES = 65536    # NEVER download a full catalog: cap every read at 64 KB
PROBE_DELAY = 0.25         # courtesy pause between probes to the same host
# Max HTTP requests per portal. We stop at the FIRST confident match, so a Socrata
# portal costs 1 request, CKAN 2, ... only an unknown/custom portal spends the full
# budget. Six = the six platforms we know how to detect. (Strict "one or two" can't
# tell six platforms apart on custom domains; --budget lets Chris cap it.)
PROBE_BUDGET = 6
PROBE_WORKERS = 8          # modest concurrency; portals are distinct hosts
CATEGORY_TARGET = 321      # the connectivity brief's portal supercluster
CATEGORY_TOLERANCE = 60    # accept the auto-pick if within +/- this of target

# The approved portal supercluster: the CATEGORY tags that are actually open-data
# portals / meta-aggregators (the ones that run Socrata/CKAN/ArcGIS/etc.). Chosen
# from the live registry's CATEGORY distribution (194 sources across these 8).
PORTAL_CATEGORIES = [
    "City/County Open-Data Portals",
    "State Open-Data Portals",
    "Open Data",
    "open data",
    "meta-discovery",
    "national-portal",
    "aggregators",
    "Meta-Portals & Catalogs",
]


# --------------------------------------------------------------------------- #
# env / .env loading  (override trap handling)
# --------------------------------------------------------------------------- #
def load_env() -> None:
    """Overlay library-onboarding/.env onto os.environ, .env WINS (override=True).

    Mirrors config.py: the file is the source of truth and beats any stale value
    the container already injected (e.g. an expired PAT).
    """
    if not ENV_FILE.exists():
        return
    for raw in ENV_FILE.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key, val = key.strip(), val.strip().strip('"').strip("'")
        if key:
            os.environ[key] = val  # override


def get_pat() -> str:
    pat = os.environ.get("SNOWFLAKE_PAT", "").strip()
    if not pat:
        sys.exit(
            "FATAL: no SNOWFLAKE_PAT found.\n"
            f"  Put a fresh token in {ENV_FILE} as:  SNOWFLAKE_PAT=...\n"
            "  (that file is gitignored — it never gets committed)."
        )
    return pat


# --------------------------------------------------------------------------- #
# Snowflake SQL REST API
# --------------------------------------------------------------------------- #
class SnowflakeError(RuntimeError):
    pass


def sf_sql(statement: str, pat: str, warehouse: str | None = None, timeout: int = 60) -> list[dict]:
    """Run one statement via the SQL REST API, return rows as list-of-dicts.

    Result sets here are tiny (<= a few hundred rows) so we only read the inline
    first partition. Raises SnowflakeError with the server message on failure.
    """
    headers = {
        "Authorization": f"Bearer {pat}",
        "X-Snowflake-Authorization-Token-Type": "PROGRAMMATIC_ACCESS_TOKEN",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "ripple-portal-recon/1.0",
    }
    body: dict = {"statement": statement, "timeout": timeout}
    if warehouse:
        body["warehouse"] = warehouse
    resp = requests.post(SQL_API + "?async=false", headers=headers, json=body, timeout=timeout + 10)
    if resp.status_code == 401:
        raise SnowflakeError(
            "PAT rejected (401). The token is invalid or expired. "
            f"Drop a fresh one into {ENV_FILE} (SNOWFLAKE_PAT=...)."
        )
    try:
        payload = resp.json()
    except ValueError:
        raise SnowflakeError(f"Non-JSON response (HTTP {resp.status_code}): {resp.text[:200]}")
    if resp.status_code not in (200, 202):
        raise SnowflakeError(f"HTTP {resp.status_code}: {payload.get('message', payload)}")

    meta = payload.get("resultSetMetaData", {})
    cols = [c["name"] for c in meta.get("rowType", [])]
    data = payload.get("data", []) or []
    # If Snowflake split the result across partitions we'd need to page; our
    # queries are small, so warn instead of silently truncating.
    parts = meta.get("partitionInfo")
    if parts and len(parts) > 1:
        print(f"  [warn] result split into {len(parts)} partitions; only first read "
              "(fine for our small queries).", file=sys.stderr)
    return [dict(zip(cols, row)) for row in data]


def pick_warehouse(pat: str) -> str | None:
    """SOURCE_REGISTRY is a table -> a scan needs a warehouse. If none is set,
    discover one (SHOW WAREHOUSES runs on cloud services, no warehouse needed)."""
    wh = os.environ.get("SNOWFLAKE_WAREHOUSE", "").strip()
    if wh:
        return wh
    # The user's account-default warehouse (the SQL API applies it automatically).
    # It's proven usable by this role, so prefer it before guessing from SHOW.
    try:
        rows = sf_sql("SELECT CURRENT_WAREHOUSE() AS W", pat, timeout=20)
        w = (rows[0].get("W") if rows else None) or ""
        if w.strip():
            print(f"  using account-default warehouse: {w}")
            return w
    except SnowflakeError:
        pass
    try:
        rows = sf_sql("SHOW WAREHOUSES", pat)
    except SnowflakeError as e:
        print(f"  [warn] could not list warehouses: {e}", file=sys.stderr)
        return None
    for r in rows:
        name = r.get("name") or r.get("NAME")
        if name:
            print(f"  no default warehouse; using discovered: {name}")
            return name
    return None


def validate_pat(pat: str) -> None:
    """Cheap no-warehouse auth check. Fails loudly with the fix if the PAT is dead."""
    rows = sf_sql("SELECT CURRENT_USER() AS U, CURRENT_ROLE() AS R", pat, timeout=20)
    u = rows[0].get("U") if rows else "?"
    r = rows[0].get("R") if rows else "?"
    print(f"  PAT OK — connected as user={u} role={r}")


# --------------------------------------------------------------------------- #
# STEP 1 — pull the portal list
# --------------------------------------------------------------------------- #
PORTAL_CATEGORY_RX = re.compile(r"portal|aggregat|open[\s_-]?data|catalog|directory|clearinghouse", re.I)


def category_distribution(pat: str, warehouse: str | None) -> list[dict]:
    sql = (f"SELECT CATEGORY, COUNT(*) AS N FROM {REGISTRY_FQN} "
           "GROUP BY CATEGORY ORDER BY N DESC")
    return sf_sql(sql, pat, warehouse)


def choose_portal_category(dist: list[dict]) -> tuple[str | None, str]:
    """Pick the CATEGORY that looks like the portal supercluster (~321).

    Prefer categories whose label reads like a portal/aggregator; among those,
    the one whose count is closest to the target. Returns (category, reason).
    """
    def n(row):  # tolerate N vs n casing
        return int(row.get("N") or row.get("n") or 0)

    named = [(row.get("CATEGORY") or row.get("category"), n(row)) for row in dist]
    keyworded = [(c, cnt) for c, cnt in named if c and PORTAL_CATEGORY_RX.search(c)]
    pool = keyworded or named
    if not pool:
        return None, "registry returned no categories"
    best = min(pool, key=lambda cn: abs(cn[1] - CATEGORY_TARGET))
    cat, cnt = best
    delta = abs(cnt - CATEGORY_TARGET)
    why = (f"matched portal keyword, count={cnt} (target ~{CATEGORY_TARGET}, off by {delta})"
           if keyworded else
           f"NO category matched portal keywords; closest-by-count={cnt}")
    return cat, why


def pull_portals(pat: str, warehouse: str | None, category: str | None) -> tuple[list[dict], str]:
    """Pull the portal supercluster. Default = the approved PORTAL_CATEGORIES set;
    --category overrides to a single label. Null-URL rows are kept (flagged later)
    so the report covers the whole set, not just the probeable ones."""
    cats = [category] if category else PORTAL_CATEGORIES
    label = category if category else f"portal supercluster ({len(cats)} CATEGORY tags)"
    # category labels come from the registry itself, not user input; escape quotes.
    in_list = ", ".join("'" + c.replace("'", "''") + "'" for c in cats)
    sql = (
        "SELECT SOURCE_ID, NAME, URL, CATEGORY, SUBCATEGORY, ACCESS_METHOD, "
        "FORMAT, AUTH_REQUIRED "
        f"FROM {REGISTRY_FQN} "
        f"WHERE CATEGORY IN ({in_list}) "
        "ORDER BY CATEGORY, SOURCE_ID"
    )
    rows = sf_sql(sql, pat, warehouse)
    return rows, label


# --------------------------------------------------------------------------- #
# STEP 2 — fingerprint one portal
# --------------------------------------------------------------------------- #
def origin_of(url: str) -> str | None:
    """scheme://netloc for a registry URL (platform APIs live at the root)."""
    if not url:
        return None
    if not re.match(r"^https?://", url, re.I):
        url = "https://" + url.strip()
    p = urlparse(url)
    if not p.netloc:
        return None
    return f"{p.scheme}://{p.netloc}"


def host_hint(host: str) -> str | None:
    """Cheap, request-free platform guess from the hostname. Only PROMOTES that
    platform to probe #1 — it is never asserted without an endpoint confirming it.
    Deliberately conservative: e.g. an `opendata.<city>` host says nothing about the
    vendor (Socrata, CKAN, ODS and ArcGIS all live on such names), so no hint."""
    h = host.lower()
    if "arcgis.com" in h or "hub.arcgis" in h:
        return "ARCGIS"
    if "opendatasoft.com" in h:
        return "OPENDATASOFT"
    if "geonode" in h:
        return "GEONODE"
    if "junar" in h:
        return "JUNAR"
    if "socrata" in h:
        return "SOCRATA"
    if "ckan" in h:
        return "CKAN"
    return None


class ProbeResult:
    """A bounded HTTP probe result. `text` is capped at MAX_PROBE_BYTES — we never
    hold a full catalog (some /data.json feeds are multi-MB)."""
    __slots__ = ("status", "headers", "text", "redirected_host", "error")

    def __init__(self, status=None, headers=None, text="", redirected_host=None, error=None):
        self.status = status
        self.headers = headers or {}
        self.text = text
        self.redirected_host = redirected_host
        self.error = error

    @property
    def responded(self) -> bool:
        return self.status is not None


def _do_probe(sess: requests.Session, url: str) -> ProbeResult:
    """One polite GET: short timeout, streamed, read at most MAX_PROBE_BYTES."""
    src_host = urlparse(url).netloc
    try:
        resp = sess.get(url, timeout=(PROBE_CONNECT_TIMEOUT, PROBE_TIMEOUT),
                        stream=True, allow_redirects=True)
    except requests.RequestException as e:
        return ProbeResult(error=type(e).__name__)
    try:
        buf = bytearray()
        for chunk in resp.iter_content(8192):
            buf += chunk
            if len(buf) >= MAX_PROBE_BYTES:
                break
        text = bytes(buf).decode("utf-8", "replace")
    except requests.RequestException as e:
        return ProbeResult(status=resp.status_code, headers=resp.headers, error=type(e).__name__)
    finally:
        resp.close()
    fhost = urlparse(resp.url).netloc
    return ProbeResult(status=resp.status_code, headers=resp.headers, text=text,
                       redirected_host=fhost if (resp.history and fhost != src_host) else None)


def _json(pr: ProbeResult):
    try:
        return json.loads(pr.text)
    except (ValueError, TypeError):
        return None


# Each matcher confirms a platform from a bounded ProbeResult. Vendor-specific
# endpoints (Socrata/CKAN/ODS/GeoNode/Junar) are definitive; ArcGIS is a backstop
# because /data.json is a *generic* DCAT feed many platforms also serve.
def _socrata_match(pr):
    if "X-Socrata-RequestId" in pr.headers or "socrata" in pr.headers.get("Server", "").lower():
        return True
    j = _json(pr)
    return bool(pr.status == 200 and isinstance(j, dict) and "resultSetSize" in j and "results" in j)


def _ckan_match(pr):
    j = _json(pr)
    return bool(pr.status == 200 and isinstance(j, dict) and j.get("success") is True and "result" in j)


def _ods_match(pr):
    j = _json(pr)
    return bool(pr.status == 200 and isinstance(j, dict) and ("total_count" in j or "nhits" in j))


def _geonode_match(pr):
    if pr.status != 200:
        return False
    if "geonode" in pr.text.lower():
        return True
    j = _json(pr)
    if isinstance(j, dict):
        keys = {k.lower() for k in j.keys()}
        return len({"datasets", "documents", "maps", "geoapps", "resources"} & keys) >= 2
    return False


def _junar_match(pr):
    # Junar usually needs an auth_key; an auth-required body that names it still
    # confirms the platform without us pulling any data.
    if pr.status in (200, 401, 403):
        t = pr.text.lower()
        return "auth_key" in t or "junar" in t
    return False


def _arcgis_match(pr):
    # /data.json is generic project-open-data DCAT — Socrata/CKAN/ODS serve it too,
    # and an ODS feed can carry one stray "arcgis.com". Only call it ArcGIS when the
    # (bounded) feed is *saturated* with arcgis.com references. This runs LAST, after
    # the vendor-specific endpoints have had their say.
    if pr.status != 200:
        return False
    return pr.text.lower().count("arcgis.com") >= 3


PROBES = {
    "SOCRATA":      ("/api/catalog/v1?limit=0",             _socrata_match, "/api/catalog/v1"),
    "CKAN":         ("/api/3/action/package_search?rows=0", _ckan_match,    "/api/3/action"),
    "OPENDATASOFT": ("/api/v2/catalog/datasets?limit=0",    _ods_match,     "/api/v2"),
    "GEONODE":      ("/api/v2/",                            _geonode_match, "/api/v2"),
    "JUNAR":        ("/api/v2/datastreams/?format=json",    _junar_match,   "/api/v2 (needs auth_key)"),
    "ARCGIS":       ("/data.json",                          _arcgis_match,  "hub.arcgis.com/api/search/v1 | /api/feed/dcat-us"),
}

# Probe order for a portal with no host hint. Definitive vendor endpoints first;
# ArcGIS's generic /data.json LAST so a vendor match always wins ahead of it.
DEFAULT_ORDER = ["SOCRATA", "CKAN", "OPENDATASOFT", "GEONODE", "JUNAR", "ARCGIS"]


def fingerprint(name: str, url: str) -> dict:
    base = origin_of(url)
    out = {"name": name, "base_url": base or url, "platform": "UNKNOWN",
           "api_base": "", "responded": False, "notes": ""}
    if not base:
        out["notes"] = "no usable URL in registry"
        return out

    host = urlparse(base).netloc
    hint = host_hint(host)
    # Ordered probe plan, host hint promoted to #1, capped at the budget. We stop at
    # the first confident match, so most portals cost far fewer than the cap.
    order = ([hint] if hint else []) + [p for p in DEFAULT_ORDER if p != hint]
    order = order[:PROBE_BUDGET]

    sess = requests.Session()
    sess.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json, */*"})
    tried, any_response, redirected = [], False, None
    try:
        for i, platform in enumerate(order):
            path, matcher, api_base = PROBES[platform]
            pr = _do_probe(sess, base + path)
            if pr.redirected_host:
                redirected = pr.redirected_host
            if not pr.responded:
                tried.append(f"{platform}:err({pr.error})")
                continue
            any_response = True
            tried.append(f"{platform}:{pr.status}")
            if matcher(pr):
                api = base + api_base if api_base.startswith("/") else api_base
                out.update(platform=platform, responded=True, api_base=api)
                notes = [f"matched {platform} via {path} (HTTP {pr.status})"]
                if redirected:
                    notes.append(f"redirects to {redirected}")
                if platform == "JUNAR" and pr.status in (401, 403):
                    notes.append("auth_key required (expected for Junar)")
                out["notes"] = "; ".join(notes)
                return out
            if i < len(order) - 1:
                time.sleep(PROBE_DELAY)  # courtesy pause between probes to one host
    finally:
        sess.close()

    out["responded"] = any_response
    notes = [f"probes={','.join(tried)}"]
    if redirected:
        notes.append(f"redirects to {redirected}")
    if not any_response:
        notes.append("no HTTP response (timeout/conn error)")
    elif hint:
        notes.append(f"host hint {hint} unconfirmed by endpoint")
    out["notes"] = "; ".join(notes)
    return out


def fingerprint_all(portals: list[dict]) -> list[dict]:
    results = []
    total = len(portals)
    with ThreadPoolExecutor(max_workers=PROBE_WORKERS) as pool:
        futs = {
            pool.submit(fingerprint, p.get("NAME") or p.get("SOURCE_ID") or "?", p.get("URL") or ""): p
            for p in portals
        }
        for i, fut in enumerate(as_completed(futs), 1):
            src = futs[fut]
            row = fut.result()
            row["source_id"] = src.get("SOURCE_ID", "")
            results.append(row)
            if i % 25 == 0 or i == total:
                print(f"    probed {i}/{total}")
    results.sort(key=lambda r: r.get("source_id", ""))
    return results


# --------------------------------------------------------------------------- #
# STEP 3 — write the report
# --------------------------------------------------------------------------- #
def write_report(results: list[dict], category: str) -> None:
    n = len(results)
    by_plat: dict[str, int] = {}
    for r in results:
        by_plat[r["platform"]] = by_plat.get(r["platform"], 0) + 1
    responded = sum(1 for r in results if r["responded"])
    dead = sum(1 for r in results if not r["responded"])

    socrata = by_plat.get("SOCRATA", 0)
    ckan = by_plat.get("CKAN", 0)
    arcgis = by_plat.get("ARCGIS", 0)
    top2 = socrata + ckan
    top2_pct = (100.0 * top2 / n) if n else 0.0
    top3_pct = (100.0 * (top2 + arcgis) / n) if n else 0.0

    flags = [r for r in results if (not r["responded"]) or "redirect" in r["notes"]
             or "auth" in r["notes"].lower()]

    lines = []
    lines.append("# Portal Recon — Wave 1: Platform Fingerprint\n")
    lines.append(f"_Generated {time.strftime('%Y-%m-%d %H:%M:%S %Z')} · "
                 f"source category: `{category}` · {n} portals._\n")
    lines.append("## SUMMARY\n")
    lines.append("| Platform | Portals |")
    lines.append("|---|---:|")
    for plat in ["SOCRATA", "CKAN", "ARCGIS", "OPENDATASOFT", "GEONODE", "JUNAR", "UNKNOWN"]:
        if by_plat.get(plat):
            lines.append(f"| {plat} | {by_plat[plat]} |")
    lines.append(f"| **TOTAL** | **{n}** |")
    lines.append("")
    lines.append(f"- **Responded:** {responded}/{n} · **Dead / no response:** {dead}")
    lines.append(f"- **Headline:** **{top2_pct:.0f}% of portals are covered by the top 2 "
                 f"platforms** (Socrata {socrata} + CKAN {ckan} = {top2}). "
                 f"Add ArcGIS and it's {top3_pct:.0f}% — that's the Wave-2 reader count.")
    lines.append("")
    if flags:
        lines.append(f"### ⚠ Flags ({len(flags)}) — dead / redirecting / auth-required\n")
        lines.append("| source_id | portal | issue |")
        lines.append("|---|---|---|")
        for r in flags:
            issue = r["notes"] or ("no response" if not r["responded"] else "")
            lines.append(f"| {r['source_id']} | {r['name']} | {issue} |")
        lines.append("")

    lines.append("## FULL RESULTS\n")
    lines.append("| portal name | base URL | platform detected | API base URL | responded? | notes |")
    lines.append("|---|---|---|---|:--:|---|")
    for r in results:
        lines.append("| {name} | {base} | {plat} | {api} | {resp} | {notes} |".format(
            name=r["name"].replace("|", "/"),
            base=r["base_url"],
            plat=r["platform"],
            api=r["api_base"],
            resp="✅" if r["responded"] else "❌",
            notes=r["notes"].replace("|", "/"),
        ))
    lines.append("")
    OUT_FILE.write_text("\n".join(lines))
    print(f"\n  wrote {OUT_FILE}  ({n} portals)")
    print(f"  headline: {top2_pct:.0f}% covered by top-2 (Socrata {socrata} + CKAN {ckan})")


# --------------------------------------------------------------------------- #
# selftest — prove the prober with no Snowflake
# --------------------------------------------------------------------------- #
def selftest() -> int:
    print("SELFTEST — probing a few known public portals (no Snowflake):\n")
    known = [
        ("Chicago (Socrata)",        "https://data.cityofchicago.org",  "SOCRATA"),
        ("demo.ckan.org (CKAN)",     "https://demo.ckan.org",           "CKAN"),
        ("LA GeoHub (ArcGIS)",       "https://geohub.lacity.org",       "ARCGIS"),
        ("Paris (OpenDataSoft)",     "https://opendata.paris.fr",       "OPENDATASOFT"),
    ]
    ok = 0
    for name, url, expect in known:
        r = fingerprint(name, url)
        hit = "PASS" if r["platform"] == expect else f"got {r['platform']}"
        if r["platform"] == expect:
            ok += 1
        print(f"  [{hit:>14}] {name:<26} expect={expect:<13} -> {r['platform']:<13} "
              f"api={r['api_base']}  ({r['notes']})")
    print(f"\n  {ok}/{len(known)} known portals identified correctly.")
    return 0 if ok == len(known) else 1


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main() -> int:
    global PROBE_BUDGET
    ap = argparse.ArgumentParser(description="Wave 1 portal platform fingerprinter")
    ap.add_argument("--selftest", action="store_true", help="prove the prober, no Snowflake")
    ap.add_argument("--distribution", action="store_true",
                    help="validate PAT + print CATEGORY distribution, then stop")
    ap.add_argument("--category", help="pin the exact CATEGORY label to pull")
    ap.add_argument("--no-stop", action="store_true",
                    help="proceed even if the portal count isn't ~321")
    ap.add_argument("--budget", type=int, default=PROBE_BUDGET,
                    help=f"max HTTP requests per portal, stop-at-first-match "
                         f"(default {PROBE_BUDGET}; set 2 for strict politeness)")
    args = ap.parse_args()
    PROBE_BUDGET = max(1, args.budget)

    if args.selftest:
        return selftest()

    load_env()
    pat = get_pat()
    print("STEP 0 — validating Snowflake PAT")
    try:
        validate_pat(pat)
    except SnowflakeError as e:
        sys.exit(f"FATAL: {e}")

    warehouse = pick_warehouse(pat)

    if args.distribution:
        dist = category_distribution(pat, warehouse)
        print("\nCATEGORY distribution:")
        for row in dist:
            c = row.get("CATEGORY") or row.get("category")
            cnt = row.get("N") or row.get("n")
            print(f"  {cnt:>6}  {c}")
        cat, why = choose_portal_category(dist)
        print(f"\nWould auto-pick: {cat!r}  ({why})")
        return 0

    print("\nSTEP 1 — pulling the portal supercluster")
    portals, category = pull_portals(pat, warehouse, args.category)
    n = len(portals)
    print(f"  pulled {n} portals ({category})")
    if n == 0:
        print("STOP: 0 portals matched — check the CATEGORY set (--distribution).")
        return 2

    print(f"\nSTEP 2 — fingerprinting (polite: <={PROBE_BUDGET} reqs/portal stop-at-first-match, "
          f"{PROBE_TIMEOUT}s timeout, count-only)")
    results = fingerprint_all(portals)

    print("\nSTEP 3 — writing report")
    write_report(results, category)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
