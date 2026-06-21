#!/usr/bin/env python3
"""Wave 2 — CKAN index reader (priority #3, 25 portals).

WHAT IT DOES (metadata only, no data download):
  Per CKAN portal, list every dataset (package) with title, dataset ID, its
  resource list, and last-updated date. Columns + row count live in CKAN's
  DataStore (not the package metadata), so we pull them with a BOUNDED enrichment
  pass and mark the rest unknown — never guessed.

HOW:
  1. LIST packages, paginated (the efficient batched form of package_show):
        GET <api>/package_search?rows=100&start=N
     Each package -> title, name (dataset ID), metadata_modified, resources[].
  2. ENRICH columns + row count (bounded, polite):
     for the first DataStore-active resource of each dataset, up to a per-portal cap,
        GET <api>/datastore_search?resource_id=<id>&limit=0
     -> result.fields (columns) + result.total (row count). Beyond the cap, a
     dataset keeps its resource list but columns/rows stay unknown (Wave 3 finishes).

Run standalone:
    python ckan_reader.py --portals loc_boston_open st_ca_open --sample 3
"""

from __future__ import annotations

import argparse
import time

import portal_lib as P

# Bounded DataStore enrichment so a huge portal can't trigger thousands of probes.
# 0 disables enrichment entirely (resource list only). Tunable from the orchestrator.
CKAN_ENRICH_PER_PORTAL = 200


def _api_base(portal: dict) -> str:
    """CKAN action API. Use Wave-1's api_base (handles /data subpaths), else derive."""
    api = (portal.get("api_base") or "").strip()
    if api:
        return api.rstrip("/")
    host = P.host_of(portal.get("base_url") or "")
    return f"https://{host}/api/3/action"


def _resource_summary(resources: list) -> list[dict]:
    """The 'resource/field list' for a package: each file with name + format."""
    out = []
    for r in resources or []:
        if not isinstance(r, dict):
            continue
        out.append({
            "id": r.get("id"),
            "name": r.get("name"),
            "format": r.get("format"),
            "datastore_active": bool(r.get("datastore_active")),
        })
    return out


def _first_datastore_resource_id(resources: list) -> str | None:
    for r in resources or []:
        if isinstance(r, dict) and r.get("datastore_active") and r.get("id"):
            return r["id"]
    return None


def _enrich_columns_rows(session, api: str, resource_id: str):
    """datastore_search?limit=0 -> (columns, row_count), each None on miss."""
    url = f"{api}/datastore_search?resource_id={resource_id}&limit=0"
    status, j, err = P.get_json(session, url)
    if err or not isinstance(j, dict) or not j.get("success"):
        return None, None
    result = j.get("result", {}) or {}
    fields = result.get("fields") or []
    # drop CKAN's internal auto columns (_id, _full_text)
    cols = [f.get("id") for f in fields
            if isinstance(f, dict) and f.get("id") and not str(f["id"]).startswith("_")]
    return (cols or None), result.get("total")


def harvest_portal(session, portal: dict, enrich_cap: int = CKAN_ENRICH_PER_PORTAL
                   ) -> tuple[dict, list[dict]]:
    api = _api_base(portal)
    capped = timed_out = False
    t_start = time.time()
    total = None

    # PHASE 1 — paginate the FULL index first (the core deliverable: title, id,
    # resources, modified for every dataset). Enrichment must never starve this.
    records: list[dict] = []
    pending: list[tuple[dict, str]] = []   # (record, first-datastore-resource-id) to enrich
    start = pages = 0
    while pages < P.PER_PORTAL_MAX_PAGES:
        if P.expired(t_start):
            timed_out = True
            break
        url = f"{api}/package_search?rows={P.PAGE_SIZE}&start={start}"
        status, j, err = P.get_json(session, url)
        if err or not isinstance(j, dict) or not j.get("success"):
            if pages == 0:
                return P.portal_result(portal, status="error", datasets=[],
                                       error=f"package_search failed: {err or 'success=false'}",
                                       api_base=api), []
            break
        result = j.get("result", {}) or {}
        if total is None:
            total = result.get("count")
        packages = result.get("results", [])
        if not packages:
            break
        for pkg in packages:
            resources = pkg.get("resources", []) or []
            rec = P.make_dataset_record(
                portal,
                dataset_id=pkg.get("name") or pkg.get("id"),
                dataset_title=pkg.get("title") or pkg.get("name"),
                columns=None, row_count=None,
                last_updated=P.clean_iso(pkg.get("metadata_modified")),
                resource_type="dataset",
                extra={"ckan_id": pkg.get("id"),
                       "num_resources": pkg.get("num_resources"),
                       "resources": _resource_summary(resources),
                       "organization": (pkg.get("organization") or {}).get("name")
                                       if isinstance(pkg.get("organization"), dict) else None},
            )
            records.append(rec)
            rid = _first_datastore_resource_id(resources)
            if rid:
                pending.append((rec, rid))
            if len(records) >= P.PER_PORTAL_MAX_DATASETS:
                capped = True
                break
        pages += 1
        if capped:
            break
        start += P.PAGE_SIZE
        if total is not None and start >= total:
            break
        P.pause()

    # PHASE 2 — best-effort column/row enrichment within whatever budget remains.
    # Bounded by enrich_cap AND the wall-clock budget, so it never blocks the index.
    enriched = 0
    for rec, rid in pending:
        if enriched >= enrich_cap or P.expired(t_start):
            break
        cols, rows = _enrich_columns_rows(session, api, rid)
        if cols or rows is not None:
            rec["columns"] = cols
            rec["column_count"] = len(cols) if cols else None
            rec["row_count"] = P.clean_count(rows)
            rec["has_join_key"], rec["join_keys_matched"] = P.flag_join_keys(cols)
        enriched += 1
        P.pause()

    datasets = records
    status = "ok" if datasets else "empty"
    notes = (f"api_total={total}" if total is not None else "")
    if enrich_cap:
        notes += f"; enriched_cols/rows={enriched}"
    if capped:
        notes += f"; CAPPED at {P.PER_PORTAL_MAX_DATASETS}"
    if timed_out:
        notes += f"; TIMED_OUT at {P.PER_PORTAL_MAX_SECONDS}s (partial)"
    return P.portal_result(portal, status=status, datasets=datasets, capped=capped,
                           api_base=api, notes=notes), datasets


def harvest(portals: list[dict], log=print, enrich_cap: int = CKAN_ENRICH_PER_PORTAL
            ) -> tuple[list[dict], list[dict]]:
    session = P.make_session()
    logs, all_ds = [], []
    try:
        for i, portal in enumerate(portals, 1):
            sid = portal.get("source_id", "?")
            try:
                plog, ds = harvest_portal(session, portal, enrich_cap)
            except Exception as e:
                plog, ds = P.portal_result(portal, status="error", datasets=[],
                                           error=f"unexpected: {type(e).__name__}: {e}"), []
            logs.append(plog)
            all_ds.extend(ds)
            extra = f" ({plog['error']})" if plog["error"] else f" — {plog['dataset_count']} datasets"
            log(f"  [{i}/{len(portals)}] {plog['status'].upper():<5} {sid:<28}{extra}")
            P.pause()
    finally:
        session.close()
    return logs, all_ds


def main() -> int:
    ap = argparse.ArgumentParser(description="Wave 2 CKAN index reader")
    ap.add_argument("--portals", nargs="*")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--sample", type=int, default=3)
    ap.add_argument("--enrich", type=int, default=CKAN_ENRICH_PER_PORTAL,
                    help="per-portal DataStore enrichment cap (0=off)")
    args = ap.parse_args()

    confirmed = P.load_confirmed_portals("CKAN")
    if args.portals:
        wanted = set(args.portals)
        portals = [p for p in confirmed if p.get("source_id") in wanted]
    elif args.limit:
        portals = confirmed[:args.limit]
    else:
        portals = confirmed

    print(f"CKAN reader — {len(portals)} portal(s) (of {len(confirmed)} confirmed), "
          f"enrich_cap={args.enrich}\n")
    logs, datasets = harvest(portals, enrich_cap=args.enrich)
    print("\n" + "=" * 70 + "\nSAMPLE OUTPUT\n" + "=" * 70)
    for plog in logs:
        sid = plog["portal_source_id"]
        print(f"\n● {sid} — {plog['portal_name']}  [{plog['status']}, "
              f"{plog['dataset_count']} datasets; {plog['notes']}]")
        if plog["error"]:
            print(f"  error: {plog['error']}")
        for d in [x for x in datasets if x["portal_source_id"] == sid][:args.sample]:
            cols = d["columns"]
            colshow = (f"{d['column_count']} cols: " + ", ".join(cols[:6])) if cols else "columns UNKNOWN"
            rc = d["row_count"] if d["row_count"] is not None else "unknown"
            keys = (" | join-keys: " + ", ".join(d["join_keys_matched"])) if d["has_join_key"] else ""
            print(f"    - {str(d['dataset_title'])[:50]!r}  id={d['dataset_id']}")
            print(f"        rows={rc}  updated={d['last_updated']}  {colshow}{keys}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
