#!/usr/bin/env python3
"""Wave 1.5 — reclaim pass over the portals pass-1 left UNKNOWN.

Pass-1 (fingerprint_portals.py) probes each portal at its registered origin. That
misses real platforms in three recoverable ways, which this pass retries — without
guessing (every reclaim is still endpoint-confirmed, except branding which is
labelled as softer):

  C) REDIRECT  the registered URL 301s cross-domain (portal moved) -> re-probe the
               redirect target's origin.
  B) SUBPATH   national portals run CKAN under a path (/data, /data/en, ...) -> try
               the CKAN endpoint at those subpaths.
  A) BRANDING  SPA/custom homepages that 200 on everything -> fetch the homepage and
               read *specific* platform branding (softer; flagged, not API-confirmed).

Confirmed pass-1 portals are NOT re-touched. Rewrites the single deliverable
(portal_recon_results.md) with the merged result + a reclaim delta, and dumps
portal_recon_results.json for reproducibility.

    python reclaim.py
"""

from __future__ import annotations

import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

import fingerprint_portals as fp
from fingerprint_portals import (PROBES, _do_probe, get_pat, load_env, origin_of,
                                 pick_warehouse, pull_portals, sf_sql)

OUT_FILE = fp.OUT_FILE
JSON_FILE = OUT_FILE.with_suffix(".json")

# CKAN is the platform that habitually lives under a URL subpath on national portals.
CKAN_SUBPATHS = ["/data", "/data/en", "/data/fr", "/catalog"]
# When a portal redirected cross-domain, re-probe the new origin for these.
REDIRECT_PLATFORMS = ["SOCRATA", "CKAN", "OPENDATASOFT", "ARCGIS"]
# Homepage branding markers — deliberately specific to avoid false positives (no
# bare "arcgis"/"esri", which appear on any embedded map). Order: most-specific first.
BRANDING = [
    ("OPENDATASOFT", ("opendatasoft", "ods-widgets")),
    ("GEONODE",      ("geonode",)),
    ("JUNAR",        ("junar",)),
    ("SOCRATA",      ("powered by socrata", "socrata.com", "api.us.socrata.com")),
    ("CKAN",         ("powered by ckan", "ckan.org", "/base/css/ckan", 'content="ckan')),
    ("ARCGIS",       ("opendata.arcgis", "hub.arcgis", "arcgis hub", "/sharing/rest/")),
]


# --------------------------------------------------------------------------- #
# parse pass-1 results (single deliverable is the source of truth for confirmed)
# --------------------------------------------------------------------------- #
def parse_prior(path) -> dict:
    """{base_url: {platform, api_base, responded, notes}} from the FULL RESULTS table.
    Names had '|' replaced with '/' on write, so splitting on '|' is safe."""
    prior, in_full = {}, False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## FULL RESULTS"):
            in_full = True
            continue
        if in_full and line.startswith("| ") and "---" not in line and "portal name" not in line:
            p = [x.strip() for x in line.strip().strip("|").split("|")]
            if len(p) >= 6:  # name | base | platform | api | resp | notes
                prior[p[1]] = {"platform": p[2], "api_base": p[3],
                               "responded": "✅" in p[4], "notes": p[5]}
    return prior


# --------------------------------------------------------------------------- #
# enhanced probing
# --------------------------------------------------------------------------- #
def _probe_platforms(sess, base, plats, tried, tag):
    for plat in plats:
        path, matcher, api_base = PROBES[plat]
        pr = _do_probe(sess, base + path)
        if not pr.responded:
            tried.append(f"{tag}/{plat}:x")
            continue
        tried.append(f"{tag}/{plat}:{pr.status}")
        if matcher(pr):
            api = base + api_base if api_base.startswith("/") else api_base
            return plat, api
        time.sleep(fp.PROBE_DELAY)
    return None


def _branding(html: str):
    h = html.lower()
    for plat, needles in BRANDING:
        if any(nd in h for nd in needles):
            return plat
    return None


def reclaim_one(row: dict) -> dict:
    base = row["base_url"]
    notes = row.get("notes", "")
    out = dict(row)
    out["method"] = ""
    if not base or not base.startswith("http"):
        out["notes"] = "reclaim: no usable URL"
        return out

    sess = requests.Session()
    sess.headers.update({"User-Agent": fp.USER_AGENT, "Accept": "application/json, */*"})
    tried = []
    try:
        # C) redirect target
        m = re.search(r"redirects to ([^\s;]+)", notes)
        if m:
            nb = "https://" + m.group(1).split(":")[0].strip("/")
            hit = _probe_platforms(sess, nb, REDIRECT_PLATFORMS, tried, "redir")
            if hit:
                out.update(platform=hit[0], api_base=hit[1], responded=True,
                           method="redirect-reprobe",
                           notes=f"reclaimed at redirect target {nb} ({hit[0]})")
                return out

        # B) CKAN at common subpaths
        for sp in CKAN_SUBPATHS:
            hit = _probe_platforms(sess, base + sp, ["CKAN", "OPENDATASOFT"], tried, f"sub{sp}")
            if hit:
                out.update(platform=hit[0], api_base=hit[1], responded=True,
                           method="subpath",
                           notes=f"reclaimed at subpath {sp} ({hit[0]})")
                return out

        # A) homepage branding (softer — flagged, not API-confirmed)
        pr = _do_probe(sess, base + "/")
        if pr.responded:
            out["responded"] = True
            plat = _branding(pr.text)
            if plat:
                out.update(platform=plat, method="branding",
                           notes=f"homepage branding => {plat} (NOT API-confirmed)")
                return out
            out["notes"] = "reclaim: no subpath/redirect/branding match"
        else:
            out["notes"] = "reclaim: still no homepage response"
        return out
    finally:
        sess.close()


# --------------------------------------------------------------------------- #
# report (rewrites the single deliverable, now with source_id + method)
# --------------------------------------------------------------------------- #
def write_report(results, label, n_confirmed, n_targets, n_reclaimed):
    n = len(results)
    by_plat = {}
    for r in results:
        by_plat[r["platform"]] = by_plat.get(r["platform"], 0) + 1
    responded = sum(1 for r in results if r["responded"])
    dead = n - responded
    detected = sorted(((p, c) for p, c in by_plat.items() if p != "UNKNOWN"),
                      key=lambda x: (-x[1], x[0]))
    total_detected = sum(c for _, c in detected)
    top2_n = sum(c for _, c in detected[:2])
    top3_n = sum(c for _, c in detected[:3])
    top2_lbl = " + ".join(f"{p} {c}" for p, c in detected[:2]) or "—"
    top3_lbl = " + ".join(f"{p} {c}" for p, c in detected[:3]) or "—"
    pct = lambda x: (100.0 * x / n) if n else 0.0
    branding_only = sum(1 for r in results if r.get("method") == "branding")

    L = []
    L.append("# Portal Recon — Wave 1: Platform Fingerprint\n")
    L.append(f"_Generated {time.strftime('%Y-%m-%d %H:%M:%S %Z')} · source: `{label}` · "
             f"{n} portals · includes Wave-1.5 reclaim pass._\n")
    L.append("## SUMMARY\n")
    L.append("| Platform | Portals |")
    L.append("|---|---:|")
    for plat in ["SOCRATA", "ARCGIS", "CKAN", "OPENDATASOFT", "GEONODE", "JUNAR", "UNKNOWN"]:
        if by_plat.get(plat):
            L.append(f"| {plat} | {by_plat[plat]} |")
    L.append(f"| **TOTAL** | **{n}** |")
    L.append("")
    L.append(f"- **Responded:** {responded}/{n} · **Dead / no response:** {dead}")
    L.append(f"- **Headline:** **{pct(top2_n):.0f}% of portals are covered by the top-2 "
             f"platforms** ({top2_lbl} = {top2_n} of {n}). Top-3 ({top3_lbl}) = "
             f"{pct(top3_n):.0f}%; all detected platforms = {total_detected} "
             f"({pct(total_detected):.0f}%). Those are your Wave-2 readers, by priority.")
    L.append(f"- **Reclaim pass:** retried {n_targets} UNKNOWNs, recovered **{n_reclaimed}** "
             f"(coverage {pct_prev(n_confirmed, n):.0f}% → {pct(total_detected):.0f}%). "
             f"Of recovered, {branding_only} are homepage-branding only (softer — verify in Wave 2).")
    L.append("")

    flags = [r for r in results if (not r["responded"]) or "redirect" in r["notes"].lower()
             or "auth" in r["notes"].lower()]
    if flags:
        L.append(f"### ⚠ Flags ({len(flags)}) — dead / redirecting / auth-required\n")
        L.append("| source_id | portal | issue |")
        L.append("|---|---|---|")
        for r in flags:
            issue = r["notes"] or ("no response" if not r["responded"] else "")
            L.append(f"| {r['source_id']} | {r['name'].replace('|','/')} | {issue.replace('|','/')} |")
        L.append("")

    L.append("## FULL RESULTS\n")
    L.append("| source_id | portal name | base URL | platform detected | API base URL | responded? | method | notes |")
    L.append("|---|---|---|---|---|:--:|---|---|")
    for r in results:
        L.append("| {sid} | {name} | {base} | {plat} | {api} | {resp} | {method} | {notes} |".format(
            sid=r.get("source_id", ""),
            name=r["name"].replace("|", "/"),
            base=r["base_url"],
            plat=r["platform"],
            api=r["api_base"],
            resp="✅" if r["responded"] else "❌",
            method=r.get("method", "") or ("pass-1" if r["platform"] != "UNKNOWN" else ""),
            notes=r["notes"].replace("|", "/"),
        ))
    L.append("")
    OUT_FILE.write_text("\n".join(L))
    JSON_FILE.write_text(json.dumps(
        {"label": label, "n": n, "by_platform": by_plat,
         "reclaimed": n_reclaimed, "results": results}, indent=2))
    print(f"\n  wrote {OUT_FILE} and {JSON_FILE.name}")
    print(f"  headline now: {pct(top2_n):.0f}% top-2 ({top2_lbl}); "
          f"detected {total_detected}/{n}; reclaimed {n_reclaimed}")


def pct_prev(confirmed, n):
    return (100.0 * confirmed / n) if n else 0.0


# --------------------------------------------------------------------------- #
def main() -> int:
    load_env()
    pat = get_pat()
    print("validating PAT…")
    fp.validate_pat(pat)
    wh = pick_warehouse(pat)

    if not OUT_FILE.exists():
        sys.exit(f"No pass-1 results at {OUT_FILE}. Run fingerprint_portals.py first.")
    prior = parse_prior(OUT_FILE)
    portals, label = pull_portals(pat, wh, None)
    print(f"  pulled {len(portals)} portals; parsed {len(prior)} pass-1 rows")

    confirmed, targets = [], []
    for p in portals:
        base = origin_of(p.get("URL") or "")
        pr = prior.get(base or "")
        row = {"source_id": p.get("SOURCE_ID", ""),
               "name": p.get("NAME") or p.get("SOURCE_ID") or "?",
               "base_url": base or (p.get("URL") or ""),
               "platform": "UNKNOWN", "api_base": "", "responded": False,
               "notes": "", "method": ""}
        if pr and pr["platform"] != "UNKNOWN":
            row.update(platform=pr["platform"], api_base=pr["api_base"],
                       responded=True, notes=pr["notes"], method="pass-1")
            confirmed.append(row)
        else:
            if pr:
                row["notes"], row["responded"] = pr["notes"], pr["responded"]
            targets.append(row)

    print(f"  confirmed pass-1: {len(confirmed)} · reclaim targets (UNKNOWN): {len(targets)}")
    print("  reclaiming (redirect-reprobe → CKAN subpaths → homepage branding)…")

    results = list(confirmed)
    done = 0
    with ThreadPoolExecutor(max_workers=fp.PROBE_WORKERS) as pool:
        futs = {pool.submit(reclaim_one, t): t for t in targets}
        for fut in as_completed(futs):
            results.append(fut.result())
            done += 1
            if done % 20 == 0 or done == len(targets):
                print(f"    reclaimed {done}/{len(targets)}")

    n_reclaimed = sum(1 for r in results if r.get("method") in ("redirect-reprobe", "subpath", "branding"))
    results.sort(key=lambda r: r["source_id"])
    write_report(results, label, len(confirmed), len(targets), n_reclaimed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
