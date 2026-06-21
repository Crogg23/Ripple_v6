#!/usr/bin/env python3
"""Wave 2 — ArcGIS Hub / Open Data index reader (priority #1, 40 portals).

WHAT IT DOES (metadata only, no data download):
  Per ArcGIS portal, list every dataset with title, dataset ID, column/field
  names, record count, and last-updated date.

HOW (2 calls per portal, then paginate):
  1. RESOLVE the portal's ArcGIS org:
        GET https://hub.arcgis.com/utilities/domains/<hostname>  ->  orgId
     (Hub sites map a domain to an ArcGIS org. orgId is the clean per-portal scope.)
  2. LIST that org's datasets from the central Hub search index:
        GET https://hub.arcgis.com/api/v3/datasets
              ?filter[orgId]=<orgId>
              &page[size]=100
              &fields[datasets]=name,recordCount,modified,created,fields,type
     JSON:API sparse fieldsets keep each page ~17x smaller (only the attrs we need).
     Each record carries: id (dataset ID), name (title), recordCount (rows),
     fields (columns), modified (last-updated, epoch ms). Paginate via links.next.

SCOPE NOTE: filter[orgId] returns the datasets that org owns — the standard, clean
proxy for "this portal's catalog". A Hub site that federates other orgs' groups may
expose a few extra items we won't see here; full reconciliation is out of scope for
an index harvest. We only assert what the API returns.

Run standalone (used for the STEP-0 gut check on 3 portals):
    python arcgis_reader.py --portals loc_asheville_open loc_dc_open loc_detroit_open
    python arcgis_reader.py --limit 3        # first 3 ArcGIS portals from Wave 1
"""

from __future__ import annotations

import argparse
import json
import time
from urllib.parse import quote

import portal_lib as P

HUB_DOMAINS_UTIL = "https://hub.arcgis.com/utilities/domains/{host}"
HUB_DATASETS = "https://hub.arcgis.com/api/v3/datasets"
SPARSE_FIELDS = "name,recordCount,modified,created,fields,type"


def _resolve_org_id(session, host: str) -> tuple[str | None, str | None]:
    """domain -> orgId via the Hub domains utility. Returns (orgId, error)."""
    status, j, err = P.get_json(session, HUB_DOMAINS_UTIL.format(host=quote(host)))
    if err:
        return None, f"orgId resolve failed: {err}"
    if isinstance(j, dict) and j.get("orgId"):
        return j["orgId"], None
    return None, "orgId resolve failed: no orgId in domains response"


def _field_names(attrs: dict) -> list | None:
    """Extract column names from a Hub dataset's `fields` array (list of dicts)."""
    fields = attrs.get("fields")
    if not isinstance(fields, list) or not fields:
        return None
    return [f.get("name") for f in fields if isinstance(f, dict) and f.get("name")]


def harvest_portal(session, portal: dict) -> tuple[dict, list[dict]]:
    """Harvest one ArcGIS portal. Returns (portal_log, [dataset_records])."""
    host = P.host_of(portal.get("base_url") or portal.get("api_base") or "")
    if not host:
        return P.portal_result(portal, status="error", datasets=[],
                               error="no usable host in Wave-1 record"), []

    org_id, err = _resolve_org_id(session, host)
    if not org_id:
        return P.portal_result(portal, status="error", datasets=[], error=err,
                               api_base="hub.arcgis.com/api/v3/datasets"), []
    P.pause()

    datasets: list[dict] = []
    capped = timed_out = False
    t_start = time.time()
    base = (f"{HUB_DATASETS}?filter[orgId]={quote(org_id)}"
            f"&page[size]={P.PAGE_SIZE}&fields[datasets]={quote(SPARSE_FIELDS)}")
    url: str | None = base
    pages = 0
    total = None
    while url and pages < P.PER_PORTAL_MAX_PAGES:
        if P.expired(t_start):
            timed_out = True
            break
        status, j, err = P.get_json(session, url)
        if err or not isinstance(j, dict):
            if pages == 0:
                return P.portal_result(portal, status="error", datasets=[],
                                       error=f"datasets query failed: {err}",
                                       api_base="hub.arcgis.com/api/v3/datasets"), []
            break  # partial page failure mid-pagination: keep what we have
        if total is None:
            total = (j.get("meta", {}).get("stats", {}) or {}).get("totalCount")
        for d in j.get("data", []):
            attrs = d.get("attributes", {}) or {}
            datasets.append(P.make_dataset_record(
                portal,
                dataset_id=d.get("id"),
                dataset_title=attrs.get("name"),
                columns=_field_names(attrs),
                row_count=attrs.get("recordCount"),
                last_updated=P.epoch_ms_to_iso(attrs.get("modified")),
                resource_type=attrs.get("type"),
                extra={"feature_server_url": attrs.get("url"),
                       "org_id": org_id},
            ))
            if len(datasets) >= P.PER_PORTAL_MAX_DATASETS:
                capped = True
                break
        pages += 1
        if capped:
            break
        url = (j.get("links", {}) or {}).get("next")
        if url:
            P.pause()

    status = "ok" if datasets else "empty"
    notes = f"orgId={org_id}"
    if total is not None:
        notes += f"; api_total={total}"
    if capped:
        notes += f"; CAPPED at {P.PER_PORTAL_MAX_DATASETS}"
    if timed_out:
        notes += f"; TIMED_OUT at {P.PER_PORTAL_MAX_SECONDS}s (partial)"
    return P.portal_result(portal, status=status, datasets=datasets, capped=capped,
                           api_base="hub.arcgis.com/api/v3/datasets", notes=notes), datasets


def harvest(portals: list[dict], log=print) -> tuple[list[dict], list[dict]]:
    """Harvest a list of ArcGIS portals. Returns (portal_logs, all_dataset_records)."""
    session = P.make_session()
    logs, all_ds = [], []
    try:
        for i, portal in enumerate(portals, 1):
            sid = portal.get("source_id", "?")
            try:
                plog, ds = harvest_portal(session, portal)
            except Exception as e:  # one portal must never kill the run
                plog, ds = P.portal_result(portal, status="error", datasets=[],
                                           error=f"unexpected: {type(e).__name__}: {e}"), []
            logs.append(plog)
            all_ds.extend(ds)
            tag = plog["status"].upper()
            extra = f" ({plog['error']})" if plog["error"] else f" — {plog['dataset_count']} datasets"
            log(f"  [{i}/{len(portals)}] {tag:<5} {sid:<28}{extra}")
            P.pause()
    finally:
        session.close()
    return logs, all_ds


# --------------------------------------------------------------------------- #
# CLI — for the STEP-0 gut check
# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser(description="Wave 2 ArcGIS Hub index reader")
    ap.add_argument("--portals", nargs="*", help="specific source_ids to harvest")
    ap.add_argument("--limit", type=int, help="first N ArcGIS portals from Wave 1")
    ap.add_argument("--sample", type=int, default=3,
                    help="how many sample datasets to print per portal")
    args = ap.parse_args()

    confirmed = P.load_confirmed_portals("ARCGIS")
    if args.portals:
        wanted = set(args.portals)
        portals = [p for p in confirmed if p.get("source_id") in wanted]
    elif args.limit:
        portals = confirmed[:args.limit]
    else:
        portals = confirmed

    print(f"ArcGIS reader — {len(portals)} portal(s) "
          f"(of {len(confirmed)} ARCGIS-confirmed in Wave 1)\n")
    logs, datasets = harvest(portals)

    print("\n" + "=" * 70)
    print("SAMPLE OUTPUT")
    print("=" * 70)
    for plog in logs:
        sid = plog["portal_source_id"]
        print(f"\n● {sid} — {plog['portal_name']}")
        print(f"  status={plog['status']} datasets={plog['dataset_count']} "
              f"capped={plog['capped']} notes={plog['notes']}")
        if plog["error"]:
            print(f"  error: {plog['error']}")
        sample = [d for d in datasets if d["portal_source_id"] == sid][:args.sample]
        for d in sample:
            cols = d["columns"]
            colshow = (f"{d['column_count']} cols: " + ", ".join(cols[:6]) +
                       (" …" if cols and len(cols) > 6 else "")) if cols else "columns UNKNOWN"
            keys = (" | join-keys: " + ", ".join(d["join_keys_matched"])) if d["has_join_key"] else ""
            rc = d["row_count"] if d["row_count"] is not None else "unknown"
            print(f"    - {str(d['dataset_title'])[:54]!r}")
            print(f"        id={d['dataset_id']}  rows={rc}  updated={d['last_updated']}")
            print(f"        {colshow}{keys}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
