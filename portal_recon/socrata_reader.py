#!/usr/bin/env python3
"""Wave 2 — Socrata index reader (priority #2, 35 portals).

WHAT IT DOES (metadata only, no data download):
  Per Socrata portal, list every dataset with title, the 4x4 dataset ID, column
  list, and last-updated date. Row count is NOT exposed by the Discovery catalog,
  so it is honestly recorded as unknown (a per-dataset count query would be a data
  request, out of scope for an index harvest).

HOW (Socrata Discovery API, deep-paginated):
    GET https://<portal>/api/catalog/v1?only=dataset&limit=100&scroll_id=<last_id>
  - only=dataset  -> the clean dataset index (skips derived charts/maps/filters)
  - scroll_id     -> Socrata caps offset paging at 10k; scroll_id pages past it by
                     passing the previous page's last resource.id. Empty = start.
  Each result's `resource` carries: id (4x4), name (title), columns_field_name /
  columns_name (columns), data_updated_at / updatedAt (last-updated).

Run standalone:
    python socrata_reader.py --portals loc_chicago_open st_ny_open --sample 3
"""

from __future__ import annotations

import argparse
import time

import portal_lib as P

SOCRATA_ONLY = "dataset"     # the dataset index; not charts/maps/filters/hrefs


def _api_base(portal: dict) -> str:
    """Socrata catalog endpoint. Use Wave-1's api_base if present, else derive."""
    api = (portal.get("api_base") or "").strip()
    if api:
        return api.rstrip("/")
    host = P.host_of(portal.get("base_url") or "")
    return f"https://{host}/api/catalog/v1"


def _columns(resource: dict) -> list | None:
    """Prefer the machine field names (best for join detection), fall back to the
    human column labels."""
    return resource.get("columns_field_name") or resource.get("columns_name")


def harvest_portal(session, portal: dict) -> tuple[dict, list[dict]]:
    """Harvest one Socrata portal via scroll_id deep pagination."""
    api = _api_base(portal)
    # CRITICAL: /api/catalog/v1 returns the GLOBAL federated catalog (all Socrata
    # customers, 10k+) unless scoped to this portal's own domain. Without this,
    # every portal would report everyone's datasets.
    host = P.host_of(portal.get("base_url") or api)
    scope = f"domains={host}&search_context={host}"
    datasets: list[dict] = []
    capped = timed_out = False
    t_start = time.time()
    scroll_id = ""
    pages = 0
    total = None

    while pages < P.PER_PORTAL_MAX_PAGES:
        if P.expired(t_start):
            timed_out = True
            break
        url = (f"{api}?only={SOCRATA_ONLY}&{scope}&limit={P.PAGE_SIZE}"
               f"&scroll_id={scroll_id}")
        status, j, err = P.get_json(session, url)
        if err or not isinstance(j, dict):
            if pages == 0:
                return P.portal_result(portal, status="error", datasets=[],
                                       error=f"catalog query failed: {err}",
                                       api_base=api), []
            break  # mid-pagination failure: keep what we have
        if total is None:
            total = j.get("resultSetSize")
        results = j.get("results", [])
        if not results:
            break
        for item in results:
            resource = item.get("resource", {}) or {}
            datasets.append(P.make_dataset_record(
                portal,
                dataset_id=resource.get("id"),
                dataset_title=resource.get("name"),
                columns=_columns(resource),
                row_count=None,   # Discovery catalog does not expose row count
                last_updated=P.clean_iso(resource.get("data_updated_at")
                                         or resource.get("updatedAt")),
                resource_type=resource.get("type"),
                extra={"permalink": item.get("permalink"),
                       "domain_category": (item.get("classification", {}) or {})
                                          .get("domain_category")},
            ))
            scroll_id = resource.get("id") or scroll_id
            if len(datasets) >= P.PER_PORTAL_MAX_DATASETS:
                capped = True
                break
        pages += 1
        if capped:
            break
        P.pause()

    status = "ok" if datasets else "empty"
    notes = ""
    if total is not None:
        # Socrata caps the reported total at 10000.
        notes = (f"api_total>=10000 (Socrata-capped)" if total == 10000
                 else f"api_total={total}")
    if capped:
        notes += f"; CAPPED at {P.PER_PORTAL_MAX_DATASETS}"
    if timed_out:
        notes += f"; TIMED_OUT at {P.PER_PORTAL_MAX_SECONDS}s (partial)"
    return P.portal_result(portal, status=status, datasets=datasets, capped=capped,
                           api_base=api, notes=notes), datasets


def harvest(portals: list[dict], log=print) -> tuple[list[dict], list[dict]]:
    session = P.make_session()
    logs, all_ds = [], []
    try:
        for i, portal in enumerate(portals, 1):
            sid = portal.get("source_id", "?")
            try:
                plog, ds = harvest_portal(session, portal)
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
    ap = argparse.ArgumentParser(description="Wave 2 Socrata index reader")
    ap.add_argument("--portals", nargs="*")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--sample", type=int, default=3)
    args = ap.parse_args()

    confirmed = P.load_confirmed_portals("SOCRATA")
    if args.portals:
        wanted = set(args.portals)
        portals = [p for p in confirmed if p.get("source_id") in wanted]
    elif args.limit:
        portals = confirmed[:args.limit]
    else:
        portals = confirmed

    print(f"Socrata reader — {len(portals)} portal(s) (of {len(confirmed)} confirmed)\n")
    logs, datasets = harvest(portals)
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
            keys = (" | join-keys: " + ", ".join(d["join_keys_matched"])) if d["has_join_key"] else ""
            print(f"    - {str(d['dataset_title'])[:54]!r}  id={d['dataset_id']}  updated={d['last_updated']}")
            print(f"        {colshow}{keys}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
