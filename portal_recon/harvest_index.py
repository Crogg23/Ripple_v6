#!/usr/bin/env python3
"""Wave 2 — harvest the dataset INDEX of every confirmed portal (orchestrator).

Runs the three platform readers (ArcGIS / Socrata / CKAN) across the Wave-1
platform-confirmed portals and writes the master index + a human summary.

  STEP 2  harvest the index   — every dataset: title, ID, columns, row count, modified
  STEP 3  light join-key flag — does the column list carry a known join key?
  STEP 4  output              — portal_datasets_index.json (+ .md)

POLITENESS: within a portal each reader is sequential + spaced (one gentle stream
to that host). ACROSS portals we parallelize over distinct hosts (like Wave 1), so
no single server sees concurrency — it just cuts wall-clock time.

    python harvest_index.py                       # full run (all 3 platforms)
    python harvest_index.py --platforms ARCGIS    # one platform
    python harvest_index.py --workers 6 --ckan-enrich 200
    python harvest_index.py --limit 5             # first 5 portals/platform (smoke)
"""

from __future__ import annotations

import argparse
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

import portal_lib as P
import arcgis_reader
import socrata_reader
import ckan_reader

PLATFORMS = ["ARCGIS", "SOCRATA", "CKAN"]   # the three Wave-2 readers, by priority
DEFAULT_WORKERS = 6


def harvest_one(portal: dict, ckan_enrich: int) -> tuple[dict, list[dict]]:
    """Dispatch one portal to its reader, each in its own thread-safe session."""
    plat = portal.get("platform")
    session = P.make_session()
    try:
        if plat == "ARCGIS":
            return arcgis_reader.harvest_portal(session, portal)
        if plat == "SOCRATA":
            return socrata_reader.harvest_portal(session, portal)
        if plat == "CKAN":
            return ckan_reader.harvest_portal(session, portal, ckan_enrich)
        return P.portal_result(portal, status="error", datasets=[],
                               error=f"no reader for platform {plat}"), []
    except Exception as e:   # one portal must never kill the run
        return P.portal_result(portal, status="error", datasets=[],
                               error=f"unexpected: {type(e).__name__}: {e}"), []
    finally:
        session.close()


def collect_portals(platforms, limit=None) -> list[dict]:
    portals = []
    for plat in platforms:
        ps = P.load_confirmed_portals(plat)
        if limit:
            ps = ps[:limit]
        portals.extend(ps)
    return portals


def run_portals(portals, workers, ckan_enrich) -> tuple[list[dict], list[dict]]:
    """Harvest a list of portals in parallel across distinct hosts."""
    logs, datasets = [], []
    done = 0
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futs = {pool.submit(harvest_one, p, ckan_enrich): p for p in portals}
        for fut in as_completed(futs):
            plog, ds = fut.result()
            logs.append(plog)
            datasets.extend(ds)
            done += 1
            tag = plog["status"].upper()
            sid = plog["portal_source_id"]
            info = (f"({plog['error']})" if plog["error"]
                    else f"{plog['dataset_count']} datasets")
            print(f"  [{done}/{len(portals)}] {tag:<5} {plog['platform']:<8} {sid:<28} {info}",
                  flush=True)
    logs.sort(key=lambda r: (r["platform"], r["portal_source_id"]))
    return logs, datasets


def reclaim(workers, ckan_enrich) -> tuple[list[dict], list[dict], dict]:
    """Re-harvest only the portals that errored/came back empty, gently, and merge
    the better outcome back into the existing index (Wave-1 reclaim pattern)."""
    payload = json.loads(P.INDEX_JSON.read_text())
    logs, datasets = payload["portals"], payload["datasets"]
    cfg = payload.get("config", {})
    err_ids = {l["portal_source_id"] for l in logs if l["status"] != "ok"}
    if not err_ids:
        print("Reclaim: no errored/empty portals — nothing to do.")
        return logs, datasets, cfg

    by_id = {p["source_id"]: p for p in collect_portals(cfg.get("platforms", PLATFORMS))}
    retry = [by_id[s] for s in sorted(err_ids) if s in by_id]
    print(f"Reclaim: retrying {len(retry)} errored/empty portals "
          f"({workers} workers, ckan_enrich={ckan_enrich})\n")
    new_logs, new_ds = run_portals(retry, workers, ckan_enrich)
    new_by = {l["portal_source_id"]: l for l in new_logs}

    rank = {"ok": 2, "empty": 1, "error": 0}
    merged_logs, replaced = [], set()
    for l in logs:
        sid = l["portal_source_id"]
        nl = new_by.get(sid)
        if nl and (rank[nl["status"]], nl["dataset_count"]) >= (rank[l["status"]], l["dataset_count"]):
            merged_logs.append(nl)
            replaced.add(sid)
        else:
            merged_logs.append(l)
    merged_logs.sort(key=lambda r: (r["platform"], r["portal_source_id"]))
    merged_ds = [d for d in datasets if d["portal_source_id"] not in replaced]
    merged_ds += [d for d in new_ds if d["portal_source_id"] in replaced]
    recovered = sum(1 for s in replaced if new_by[s]["status"] == "ok")
    print(f"\nReclaim: recovered {recovered}/{len(retry)} portals to OK.")
    return merged_logs, merged_ds, cfg


# --------------------------------------------------------------------------- #
# STEP 4 — outputs
# --------------------------------------------------------------------------- #
def build_totals(logs, datasets) -> dict:
    by_plat: dict[str, dict] = {}
    for plog in logs:
        b = by_plat.setdefault(plog["platform"], {"portals": 0, "ok": 0, "error": 0,
                                                   "empty": 0, "datasets": 0})
        b["portals"] += 1
        b[plog["status"]] = b.get(plog["status"], 0) + 1
        b["datasets"] += plog["dataset_count"]

    with_cols = sum(1 for d in datasets if d["columns"])
    with_rows = sum(1 for d in datasets if d["row_count"] is not None)
    with_key = sum(1 for d in datasets if d["has_join_key"])
    key_counts: dict[str, int] = {}
    for d in datasets:
        for k in d["join_keys_matched"]:
            key_counts[k] = key_counts.get(k, 0) + 1

    return {
        "portals_attempted": len(logs),
        "portals_ok": sum(1 for r in logs if r["status"] == "ok"),
        "portals_empty": sum(1 for r in logs if r["status"] == "empty"),
        "portals_error": sum(1 for r in logs if r["status"] == "error"),
        "datasets_indexed": len(datasets),
        "datasets_with_columns": with_cols,
        "datasets_with_row_count": with_rows,
        "datasets_with_join_key": with_key,
        "join_key_counts": dict(sorted(key_counts.items(), key=lambda x: -x[1])),
        "by_platform": by_plat,
    }


def write_json(logs, datasets, totals, config) -> None:
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "wave": 2,
        "description": "Dataset index harvested from Wave-1 platform-confirmed portals "
                       "(metadata only — no data ingested).",
        "input": "portal_recon_results.json",
        "platforms": config["platforms"],
        "config": config,
        "totals": totals,
        "portals": logs,
        "datasets": datasets,
    }
    # Compact (no indent): this is a machine asset — the .md is the human view —
    # and the dataset list is large, so every byte of indentation is wasted weight.
    text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    P.INDEX_JSON.write_text(text)
    size_mb = P.INDEX_JSON.stat().st_size / 1_048_576
    print(f"\n  wrote {P.INDEX_JSON.name}  ({len(datasets):,} datasets, {size_mb:.1f} MB)")
    # GitHub rejects files >100 MB. If the master asset is that big, also emit a gzip
    # (it decompresses to the identical JSON) so a committable artifact always exists.
    gz = P.INDEX_JSON.with_suffix(".json.gz")
    if size_mb > 80:
        import gzip
        with gzip.open(gz, "wt", encoding="utf-8") as f:
            f.write(text)
        print(f"  wrote {gz.name}  ({gz.stat().st_size/1_048_576:.1f} MB gzipped) "
              f"— raw JSON is too large for git, commit the .gz")
    elif gz.exists():
        gz.unlink()  # stale gzip from a previous larger run


def write_md(logs, datasets, totals, config) -> None:
    pct = lambda a, b: (100.0 * a / b) if b else 0.0
    n = totals["datasets_indexed"]
    L = []
    L.append("# Portal Dataset Index — Wave 2\n")
    L.append(f"_Generated {time.strftime('%Y-%m-%d %H:%M:%S %Z')} · input: "
             f"`portal_recon_results.json` · readers: ArcGIS / Socrata / CKAN · "
             f"metadata only, nothing ingested._\n")

    # Headline
    L.append("## Headline\n")
    L.append(f"- **{n:,} datasets indexed** across "
             f"**{totals['portals_ok']}** live portals "
             f"({totals['portals_attempted']} attempted, "
             f"{totals['portals_error']} errored, {totals['portals_empty']} empty).")
    L.append(f"- **{totals['datasets_with_join_key']:,} datasets "
             f"({pct(totals['datasets_with_join_key'], n):.0f}%) carry at least one "
             f"known join key** — the connectivity signal (light pass; full tagging is Wave 3).")
    L.append(f"- Columns captured for {totals['datasets_with_columns']:,} "
             f"({pct(totals['datasets_with_columns'], n):.0f}%); row counts for "
             f"{totals['datasets_with_row_count']:,} "
             f"({pct(totals['datasets_with_row_count'], n):.0f}%). Missing = `unknown`, never guessed.\n")

    # By platform
    L.append("## By platform\n")
    L.append("| Platform | Portals (ok/err/empty) | Datasets |")
    L.append("|---|---|---:|")
    for plat in config["platforms"]:
        b = totals["by_platform"].get(plat)
        if not b:
            continue
        L.append(f"| {plat} | {b.get('ok',0)}/{b.get('error',0)}/{b.get('empty',0)} "
                 f"| {b['datasets']:,} |")
    L.append(f"| **TOTAL** | **{totals['portals_ok']}/{totals['portals_error']}/"
             f"{totals['portals_empty']}** | **{n:,}** |")
    L.append("")

    # Join keys
    if totals["join_key_counts"]:
        L.append("## Join keys detected (light scan)\n")
        L.append("| Join key | Datasets |")
        L.append("|---|---:|")
        for k, c in totals["join_key_counts"].items():
            L.append(f"| {k} | {c:,} |")
        L.append("")

    # Top 20 portals by dataset count (the biggest boxes)
    ranked = sorted(logs, key=lambda r: -r["dataset_count"])
    L.append("## Top 20 portals by dataset count (the biggest boxes)\n")
    L.append("| # | Portal | Platform | Datasets | Capped? |")
    L.append("|---:|---|---|---:|:--:|")
    for i, r in enumerate(ranked[:20], 1):
        L.append(f"| {i} | {r['portal_source_id']} | {r['platform']} "
                 f"| {r['dataset_count']:,} | {'⚠' if r['capped'] else ''} |")
    L.append("")

    # Errors / empties — the flags
    flags = [r for r in logs if r["status"] != "ok"]
    if flags:
        L.append(f"## ⚠ Portals with no index ({len(flags)}) — errored or empty\n")
        L.append("| Portal | Platform | Status | Reason |")
        L.append("|---|---|---|---|")
        for r in sorted(flags, key=lambda r: (r["platform"], r["portal_source_id"])):
            reason = (r["error"] or "no datasets returned").replace("|", "/")
            L.append(f"| {r['portal_source_id']} | {r['platform']} | {r['status']} | {reason} |")
        L.append("")

    # Full per-portal table
    L.append("## All portals\n")
    L.append("| Portal | Platform | Datasets | Status | Notes |")
    L.append("|---|---|---:|---|---|")
    for r in sorted(logs, key=lambda r: (r["platform"], -r["dataset_count"])):
        L.append(f"| {r['portal_source_id']} | {r['platform']} | {r['dataset_count']:,} "
                 f"| {r['status']} | {(r['notes'] or '').replace('|','/')} |")
    L.append("")

    P.INDEX_MD.write_text("\n".join(L))
    print(f"  wrote {P.INDEX_MD.name}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Wave 2 dataset-index harvester")
    ap.add_argument("--platforms", nargs="*", default=PLATFORMS,
                    choices=PLATFORMS, help="which readers to run")
    ap.add_argument("--workers", type=int, default=DEFAULT_WORKERS,
                    help="concurrent portals (distinct hosts)")
    ap.add_argument("--ckan-enrich", type=int, default=ckan_reader.CKAN_ENRICH_PER_PORTAL,
                    help="per-portal CKAN DataStore enrichment cap (0=off)")
    ap.add_argument("--limit", type=int, help="first N portals per platform (smoke test)")
    ap.add_argument("--reclaim", action="store_true",
                    help="retry only the errored/empty portals in the existing index and merge")
    args = ap.parse_args()

    t0 = time.time()
    if args.reclaim:
        logs, datasets, config = reclaim(args.workers, args.ckan_enrich)
        config = dict(config or {})
        config.setdefault("platforms", args.platforms)
    else:
        portals = collect_portals(args.platforms, args.limit)
        print(f"Harvesting {len(portals)} portals across {args.platforms} "
              f"({args.workers} workers, ckan_enrich={args.ckan_enrich})\n")
        logs, datasets = run_portals(portals, args.workers, args.ckan_enrich)
        config = {
            "platforms": args.platforms,
            "per_portal_cap": P.PER_PORTAL_MAX_DATASETS,
            "per_portal_max_seconds": P.PER_PORTAL_MAX_SECONDS,
            "ckan_enrich_per_portal": args.ckan_enrich,
            "page_size": P.PAGE_SIZE,
            "workers": args.workers,
        }
    totals = build_totals(logs, datasets)
    print("\n" + "=" * 70)
    write_json(logs, datasets, totals, config)
    write_md(logs, datasets, totals, config)
    print(f"\n  done in {time.time() - t0:.0f}s — "
          f"{totals['datasets_indexed']:,} datasets, "
          f"{totals['datasets_with_join_key']:,} with a join key")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
