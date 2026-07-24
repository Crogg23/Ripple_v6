#!/usr/bin/env python3
"""Ripple data intake funnel: one front door for "I want data X".

Given a URL, sniff it and route to the CHEAPEST tool that ends in an OWNED copy in
LIBRARY_RAW (the acquisition ladder). It RECOMMENDS the tier + the exact command to
run -- it does not auto-execute (a human confirms what gets pulled).

    python scripts/intake.py https://example.gov/data.csv --source-id FED_X
    python scripts/intake.py https://example.gov/data.csv --source-id FED_X --record

Tiers (cheapest first; see outputs/BACKFILL_RUNBOOK_2026-07-23.md "Routing policy"):
  1 server-side direct   public file at a direct URL (CSV/ZIP)  -> server_side_load.py
  2 server-side resolver  redirecting/metadata-indexed download  -> + a `resolver` spec
  3 server-side keyed      public API needing a free key         -> + an `auth` spec
  4 AI agent (last resort) scrape / JS site / bespoke one-off    -> library-onboarding/onboard.py

The classifier is deliberately conservative: when unsure it routes UP a tier (toward
the AI agent) rather than silently mislabel a source.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from urllib.parse import urlparse

_REPO = Path(__file__).resolve().parents[1]

# Hosts already on the RIPPLE_BULK_EGRESS allow-list (keep in sync with
# infra/ddl/08_bulk_ingest.sql). A source on another host needs one ALTER first.
ALLOWED_HOSTS = {
    "files.consumerfinance.gov", "leidata.gleif.org", "goldencopy.gleif.org",
    "www.sec.gov", "www.irs.gov", "apps.irs.gov", "www.fec.gov",
    "echo.epa.gov", "download.cms.gov", "data.cms.gov",
    "static.nhtsa.gov", "data.transportation.gov", "enforcedata.dol.gov",
    "arlweb.msha.gov", "download.open.fda.gov", "files.usaspending.gov",
    "s3.amazonaws.com", "irs-form-990.s3.amazonaws.com",
}

_UA = {"User-Agent": "Ripple intake sniff (contact w.rogers9999@gmail.com)"}


def _sniff(url: str) -> dict:
    """Lightweight probe: follow redirects, read headers + a few bytes. No full pull."""
    import requests
    info = {"url": url, "final_url": url, "content_type": "", "disposition": "",
            "cross_host_redirect": False, "looks_html": False, "looks_zip": False,
            "error": ""}
    start_host = urlparse(url).hostname or ""
    try:
        # Ranged GET (0-2047): cheap, works where HEAD is blocked; reveals redirect + magic bytes.
        r = requests.get(url, headers={**_UA, "Range": "bytes=0-2047"},
                         stream=True, timeout=60, allow_redirects=True)
        info["final_url"] = r.url
        info["content_type"] = (r.headers.get("Content-Type", "") or "").lower()
        info["disposition"] = (r.headers.get("Content-Disposition", "") or "").lower()
        final_host = urlparse(r.url).hostname or ""
        info["cross_host_redirect"] = bool(final_host and final_host != start_host)
        info["final_host"] = final_host
        head = next(r.iter_content(chunk_size=2048), b"") or b""
        r.close()
        info["looks_zip"] = head[:2] == b"PK"
        low = head[:512].lstrip().lower()
        info["looks_html"] = low.startswith(b"<!doctype html") or low.startswith(b"<html")
    except Exception as e:  # noqa: BLE001
        info["error"] = str(e)[:160]
    return info


def _classify(url: str, info: dict) -> dict:
    """Return {tier, tool, reason, spec_hint}. Conservative: unsure -> AI agent."""
    path = urlparse(info.get("final_url", url)).path.lower()
    ct, disp = info["content_type"], info["disposition"]
    is_zip = info["looks_zip"] or path.endswith(".zip") or "zip" in ct
    is_csv = (path.endswith((".csv", ".txt", ".tsv", ".psv"))
              or "csv" in ct or "text/plain" in ct or ".csv" in disp)
    is_json_api = ("json" in ct or path.endswith(".json")) and not is_csv

    if info["error"]:
        return {"tier": "?", "tool": "manual", "reason": f"could not sniff: {info['error']}",
                "spec_hint": ""}
    if info["looks_html"]:
        return {"tier": 4, "tool": "onboard.py (AI agent)",
                "reason": "response is an HTML page, not a data file -> scrape territory",
                "spec_hint": "onboard.py --name <SID>  (steer: extract the table/links)"}
    if info["cross_host_redirect"] and info.get("final_host") not in ALLOWED_HOSTS:
        return {"tier": 2, "tool": "server_side_load.py + resolver",
                "reason": (f"redirects to {info.get('final_host')} (not on the egress "
                           "allow-list) -> use a resolver hop or add the host"),
                "spec_hint": "add a 'resolver' to the spec, or ALTER RIPPLE_BULK_EGRESS to add the host"}
    if is_zip:
        return {"tier": 1, "tool": "server_side_load.py",
                "reason": "direct ZIP download", "spec_hint": "kind='zip', member_pattern=r'\\.csv$'"}
    if is_csv:
        return {"tier": 1, "tool": "server_side_load.py",
                "reason": "direct CSV/text download", "spec_hint": "kind='csv', delimiter=','"}
    if is_json_api:
        return {"tier": 3, "tool": "server_side_load.py (+ auth if keyed) / onboard.py",
                "reason": "JSON/API response -> keyed path if it needs a free api_key, else AI agent",
                "spec_hint": "auth={'style':'query','param':'api_key'} (set RIPPLE_API_KEY secret)"}
    return {"tier": 4, "tool": "onboard.py (AI agent)",
            "reason": f"unrecognized shape (content-type {ct!r}) -> route up to the AI agent",
            "spec_hint": ""}


def _record(source_id: str, url: str, tier, tool: str) -> None:
    """Log the routing decision to LIBRARY_META.REGISTRY.INTAKE_ROUTING (best-effort)."""
    sys.path.insert(0, str(_REPO / "library-onboarding"))
    import snow  # noqa: E402
    conn = snow.connect()
    try:
        snow.execute(conn,
            "CREATE TABLE IF NOT EXISTS LIBRARY_META.REGISTRY.INTAKE_ROUTING ("
            "SOURCE_ID VARCHAR, URL VARCHAR, TIER VARCHAR, TOOL VARCHAR, "
            "ROUTED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP())")
        snow.execute(conn,
            "INSERT INTO LIBRARY_META.REGISTRY.INTAKE_ROUTING (SOURCE_ID, URL, TIER, TOOL) "
            "VALUES (%s, %s, %s, %s)", (source_id, url, str(tier), tool))
    finally:
        conn.close()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Ripple data intake funnel (routes a URL to the cheapest owned-copy path)")
    ap.add_argument("url", help="the data URL to route")
    ap.add_argument("--source-id", default="", help="intended SOURCE_ID (for the recommendation + record)")
    ap.add_argument("--record", action="store_true", help="log the routing decision to INTAKE_ROUTING")
    args = ap.parse_args(argv)

    info = _sniff(args.url)
    c = _classify(args.url, info)
    sid = args.source_id or "<SID>"

    print(f"\nIntake: {args.url}")
    if info.get("final_url") != args.url:
        print(f"  -> redirects to: {info['final_url']}")
    print(f"  content-type: {info['content_type'] or '(unknown)'}"
          f"{'  [looks like ZIP]' if info['looks_zip'] else ''}"
          f"{'  [looks like HTML]' if info['looks_html'] else ''}")
    print(f"\n  TIER {c['tier']} -> {c['tool']}")
    print(f"  why: {c['reason']}")
    if c["spec_hint"]:
        print(f"  spec: {c['spec_hint']}")
    if c["tier"] in (1, 2, 3):
        print(f"\n  next: add a spec to scripts/server_side_specs.py, then")
        print(f"        python scripts/server_side_load.py --spec {sid} --run")
    elif c["tier"] == 4:
        print(f"\n  next: python library-onboarding/onboard.py --name {sid}  (AI agent; last resort)")

    if args.record and args.source_id:
        try:
            _record(args.source_id, args.url, c["tier"], c["tool"])
            print("\n  (routing decision recorded in LIBRARY_META.REGISTRY.INTAKE_ROUTING)")
        except Exception as e:  # noqa: BLE001
            print(f"\n  (record skipped: {str(e)[:120]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
