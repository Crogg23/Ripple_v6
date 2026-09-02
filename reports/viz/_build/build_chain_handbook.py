"""Build THE Join Handbook — the "Follow the joins out" chain explorer — as one self-contained page.

Chris's handbook is the dark chain-explorer page (design-canvas build, downloaded 2026-08-29 as
"Ripple Join Handbook - refined.html"). Its pieces live in ./chain/:

  chain_template.html      the page (markup + the x-dc page script)      <- edit this
  base_tables.js           HANDBOOK_TABLES  (209 tables, spine joins, 08-29 snapshot)
  base_context.js          HANDBOOK_CONTEXT (rows / domain per table)
  base_schema.js           HANDBOOK_SCHEMA  (fqn, notes, columns per table)
  dc_runtime.js, vendor_react*.js, fonts_woff2_b64.json   runtime + fonts, inlined
  repo_payload.json        the merged layers from build_join_handbook.py --dump-data
                           (spine edges + pass-2 measured edges + verified place columns + clocks)

This script folds the payload's layers INTO the base data (new "measured" tier, place + time per
table, tables new to the handbook), stamps META, and writes:

  reports/viz/join_handbook.html            the page (repo original)
  reports/viz/_build/chain/DATA.js          the merged data, for receipts / diffs

Run:  python reports/viz/_build/build_join_handbook.py --dump-data reports/viz/_build/chain/repo_payload.json
      python reports/viz/_build/build_chain_handbook.py
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

BUILD = Path(__file__).resolve().parent
CHAIN = BUILD / "chain"
VIZ = BUILD.parent
OUT = VIZ / "join_handbook.html"
PLACE_CSV = VIZ.parent / "location_index" / "location_columns_verified.csv"
SNAPSHOT = "2026-09-01"


def load_global(path: Path) -> object:
    txt = path.read_text(encoding="utf-8")
    txt = txt[txt.index("=") + 1:].strip()
    obj, _end = json.JSONDecoder().raw_decode(txt)  # the file may carry a second statement (META)
    return obj


def js_blob(name: str, obj: object) -> str:
    s = json.dumps(obj, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")
    return f"window.{name} = {s};"


def pretty_label(table_id: str) -> str:
    return table_id.replace("_", " ")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--payload", type=Path, default=CHAIN / "repo_payload.json")
    args = ap.parse_args()

    tables: list[dict] = load_global(CHAIN / "base_tables.js")
    context: dict = load_global(CHAIN / "base_context.js")
    schema: dict = load_global(CHAIN / "base_schema.js")
    payload = json.loads(args.payload.read_text(encoding="utf-8"))
    by_id = {t["id"]: t for t in tables}
    notes = payload.get("notes", {})

    # rows / fqn for tables the base never saw: from the place scan (whole-table row counts)
    mart_rows: dict[str, tuple[int, str, str]] = {}
    if PLACE_CSV.exists():
        with PLACE_CSV.open(encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f):
                name = r["table"].split("__", 1)[1] if "__" in r["table"] else r["table"]
                mart_rows[name] = (int(float(r["rows"] or 0)), r["domain"], r["table"])

    # ---- 1. tables new to the handbook ---------------------------------------------------
    added_tables = []
    for pt in payload["tables"]:
        tid = pt["name"]
        if tid in by_id:
            continue
        mart = None
        for e in (pt.get("place") or []) + (pt.get("time") or []):
            if e.get("mart"):
                mart = e["mart"]
                break
        rows, dom, mart_name = mart_rows.get(tid, (0, "", mart or ""))
        if not mart_name and mart:
            mart_name = mart
        schema_name = mart_name.split("__", 1)[0] if "__" in mart_name else ""
        fqn = f"LIBRARY_MARTS.{schema_name}.{mart_name}" if schema_name else tid
        t = {"id": tid, "label": pretty_label(tid), "reliableCount": 0, "placeCount": pt.get("n_place", 0),
             "fuzzyCount": 0, "conns": []}
        tables.append(t)
        by_id[tid] = t
        context[tid] = {"rows": rows, "dom": (dom or schema_name).lower(), "one": "", "life": "modeled"}
        schema[tid] = {"fqn": fqn, "schema": schema_name, "tbl": mart_name, "rows": rows, "dom": (dom or schema_name).lower(),
                       "life": "modeled", "model": mart_name.lower(), "desc": "", "notes": {}, "cols": []}
        added_tables.append(tid)

    # ---- 2. the measured-not-in-spine edges (pass 2) --------------------------------------
    added_edges = 0
    skipped = 0
    for self_id, edges in payload["edges"].items():
        for e in edges:
            if e.get("src") != "pass2":
                continue
            other = e["other"]
            if self_id not in by_id or other not in by_id:
                continue
            t = by_id[self_id]
            if any(c["id"] == other and c["jk"] == e["key"] and c.get("lc") == e.get("col_self") for c in t["conns"]):
                skipped += 1
                continue
            t["conns"].append({
                "id": other, "lbl": by_id[other]["label"], "tier": "measured",
                "pct": e.get("rate"), "n": e.get("matched"),
                "lc": e.get("col_self"), "rc": e.get("col_other"), "jk": e["key"],
                "verdict": e.get("verdict", ""), "note": e.get("note", ""), "norm": e.get("norm", ""),
                "pairs": e.get("pairs"), "names_pct": e.get("names_pct"), "states_pct": e.get("states_pct"),
                "measured_on": e.get("measured_on", ""),
            })
            added_edges += 1

    # ---- 3. place + clock per table -------------------------------------------------------
    axis_tables = (notes.get("place") or {}).get("axis_tables", {})
    place_tables = time_tables = 0
    for pt in payload["tables"]:
        tid = pt["name"]
        s = schema.setdefault(tid, {"fqn": tid, "cols": [], "notes": {}})
        if pt.get("place"):
            s["place"] = [{k: p.get(k) for k in ("kind", "label", "column", "verdict", "note", "fill", "distinct", "trap")}
                          for p in pt["place"]]
            for p in s["place"]:
                p["others"] = axis_tables.get(p["kind"], 0)
            place_tables += 1
            by_id[tid]["placeCount"] = pt.get("n_place", len(pt["place"]))
        if pt.get("time"):
            s["time"] = [{k: c.get(k) for k in ("column", "format", "grain", "meaning", "label", "rows", "lo", "hi", "desc", "trap")}
                         for c in pt["time"]]
            s["clock"] = pt.get("clock")
            time_tables += 1

    # ---- 4. META ---------------------------------------------------------------------------
    key_gloss = {}
    for k, v in (notes.get("keys") or {}).items():
        key_gloss[k] = {"name": v.get("name", k), "desc": v.get("desc", "")}
    tier_count = Counter(c["tier"] for t in tables for c in t["conns"])
    meta = {
        "snapshotDate": SNAPSHOT,
        "totalTables": len(tables),
        "listedTables": len(tables),
        "totalReliable": tier_count["solid"] + tier_count["strong"] + tier_count["translation"],
        "measuredEdges": tier_count["measured"],
        "measuredOn": (notes.get("measured_on") or "2026-08-29"),
        "keys": key_gloss,
        "corrections": notes.get("corrections") or [],
        "traps": notes.get("traps") or [],
        "place": {"measuredOn": (notes.get("place") or {}).get("measured_on"),
                  "axisTables": axis_tables,
                  "axisLabel": (notes.get("place") or {}).get("axis_label", {}),
                  "tables": place_tables},
        "time": {"measuredOn": (notes.get("time") or {}).get("measured_on"),
                 "grainTables": (notes.get("time") or {}).get("grain_tables", {}),
                 "meaningTables": (notes.get("time") or {}).get("meaning_tables", {}),
                 "tables": time_tables},
        "newTables": sum(1 for t in tables if not any(c["tier"] != "location" for c in t["conns"])),
        "noIdTables": sum(1 for t in tables if not any(c["tier"] != "location" for c in t["conns"])),
    }

    # ---- 5. assemble ----------------------------------------------------------------------
    template = (CHAIN / "chain_template.html").read_text(encoding="utf-8")
    fonts = json.loads((CHAIN / "fonts_woff2_b64.json").read_text(encoding="utf-8"))
    for uuid, b64 in fonts.items():
        template = template.replace(f'url("{uuid}")', f'url("data:font/woff2;base64,{b64}")')
    body_start = template.index("<x-dc>")
    body = template[body_start:template.rindex("</body>")]
    # </script> inside the page script would close the block: x-dc scripts are plain text, keep as is.

    scripts = "\n".join([
        "<script>" + (CHAIN / "vendor_react.js").read_text(encoding="utf-8") + "</script>",
        "<script>" + (CHAIN / "vendor_react_dom.js").read_text(encoding="utf-8") + "</script>",
        "<script>" + js_blob("HANDBOOK_TABLES", tables) + "</script>",
        "<script>" + js_blob("HANDBOOK_META", meta) + "</script>",
        "<script>" + js_blob("HANDBOOK_CONTEXT", context) + "</script>",
        "<script>" + js_blob("HANDBOOK_SCHEMA", schema) + "</script>",
        "<script>" + (CHAIN / "human_names.js").read_text(encoding="utf-8") + "</script>",
        "<script>" + (CHAIN / "dc_runtime.js").read_text(encoding="utf-8") + "</script>",
    ])
    tabbar = (
        '<div style="position:sticky;top:0;z-index:50;display:flex;align-items:center;gap:8px;'
        'padding:10px 30px;background:rgba(11,14,19,0.92);backdrop-filter:blur(8px);'
        'border-bottom:1px solid rgba(255,255,255,0.07);font-family:\'IBM Plex Sans\',system-ui,sans-serif;">'
        '<span style="font-family:monospace;font-size:10.5px;letter-spacing:0.14em;text-transform:uppercase;color:#9aa5b3;margin-right:10px;">Ripple · join handbook</span>'
        + ''.join(
            f'<button id="tab-{k}" style="font-size:12.5px;padding:6px 14px;border-radius:999px;'
            f'border:1px solid rgba(255,255,255,0.10);background:transparent;color:#9aa5b3;cursor:pointer;">{lbl}</button>'
            for k, lbl in [("things", "Things"), ("map", "Map"), ("routes", "Routes"), ("trails", "Trails"), ("pivot", "Pivot")])
        + '</div>')
    panel = 'font-family:\'IBM Plex Sans\',system-ui,sans-serif;color:#e8eaed;background:#0b0e13;padding:26px 30px 70px;min-height:90vh;'
    views = (
        '<div id="view-things" style="display:none;' + panel + '">'
        '<h2 style="font-size:22px;margin:0 0 4px;">Start with a thing in the world</h2>'
        '<div style="font-size:13px;color:#9aa5b3;margin-bottom:16px;">a doctor, a company, a mine — pick one and see everything the warehouse can say about it, and what it can become next</div>'
        '<div id="things-host"></div>'
        '</div>'
        '<div id="view-map" style="display:none;' + panel + '" >'
        '<h2 style="font-size:22px;margin:0 0 4px;">The whole warehouse at a glance</h2>'
        '<div style="font-size:13px;color:#9aa5b3;margin-bottom:12px;">the joined tables, gathered into neighborhoods by the language they speak · arcs are bridges between worlds · click a dot to open it in the pivot</div>'
        '<div style="display:flex;gap:16px;align-items:center;margin-bottom:10px;">'
        '<input id="map-find" placeholder="highlight a table by name" style="padding:7px 12px;font-size:12.5px;background:#10161d;color:#e8eaed;border:1px solid rgba(255,255,255,0.12);border-radius:8px;outline:none;width:260px;">'
        '<label style="font-size:12px;color:#9aa5b3;display:flex;gap:6px;align-items:center;"><input type="checkbox" id="map-place"> show place-only joins</label>'
        '<span id="map-status" style="font-size:12px;color:#8a95a3;"></span></div>'
        '<canvas id="map-canvas" style="width:100%;height:760px;border:1px solid rgba(255,255,255,0.06);border-radius:14px;background:#0a0d12;"></canvas>'
        '<div id="map-legend" style="margin-top:10px;"></div>'
        '</div>'
        '<div id="view-routes" style="display:none;' + panel + '">'
        '<h2 style="font-size:22px;margin:0 0 4px;">Can I get from A to B?</h2>'
        '<div style="font-size:13px;color:#9aa5b3;margin-bottom:14px;">pick two tables — every route shows each hop\'s key, match % and the weakest link you must cross</div>'
        '<datalist id="route-tables"></datalist>'
        '<div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center;">'
        '<input id="route-a" list="route-tables" placeholder="from table" style="padding:8px 12px;font-size:12.5px;background:#10161d;color:#e8eaed;border:1px solid rgba(255,255,255,0.12);border-radius:8px;outline:none;width:300px;">'
        '<button id="route-swap" title="swap ends" style="font-size:13px;padding:7px 10px;border-radius:8px;border:1px solid rgba(255,255,255,0.12);background:transparent;color:#9aa5b3;cursor:pointer;">⇄</button>'
        '<input id="route-b" list="route-tables" placeholder="to table" style="padding:8px 12px;font-size:12.5px;background:#10161d;color:#e8eaed;border:1px solid rgba(255,255,255,0.12);border-radius:8px;outline:none;width:300px;">'
        '<button id="route-go" style="font-size:12.5px;padding:8px 18px;border-radius:999px;border:1px solid rgba(76,154,255,0.5);background:rgba(76,154,255,0.15);color:#cfe2ff;cursor:pointer;">find routes</button>'
        '<label style="font-size:12px;color:#9aa5b3;display:flex;gap:6px;align-items:center;"><input type="checkbox" id="route-place"> allow place joins</label>'
        '</div><div id="route-out"></div>'
        '</div>'
        '<div id="view-trails" style="display:none;' + panel + '">'
        '<h2 style="font-size:22px;margin:0 0 4px;">Three walks worth taking</h2>'
        '<div style="font-size:13px;color:#9aa5b3;">curated chains, each hop annotated with why the join holds</div>'
        '<div id="trails-host"></div>'
        '</div>')
    explorer = "<script>" + (CHAIN / "explorer.js").read_text(encoding="utf-8") + "</script>"
    html = ("<!DOCTYPE html>\n<html><head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            "<title>The Join Handbook</title>\n<style>body{margin:0;background:#0b0e13;}</style>\n" + scripts + "\n</head>\n<body>\n"
            + tabbar + views + '<div id="view-pivot" style="display:none;">' + body + "</div>" + explorer + "</body></html>\n")
    args.out.write_text(html, encoding="utf-8")
    (CHAIN / "DATA.js").write_text("\n".join([js_blob("HANDBOOK_TABLES", tables), js_blob("HANDBOOK_META", meta),
                                              js_blob("HANDBOOK_CONTEXT", context), js_blob("HANDBOOK_SCHEMA", schema)]),
                                   encoding="utf-8")

    print(f"wrote {args.out}  ({len(html):,} bytes)")
    print(f"  {len(tables)} tables ({len(added_tables)} new to the handbook), joins by tier: {dict(tier_count)}")
    print(f"  measured layer: {added_edges} directed edges added ({skipped} already present)")
    print(f"  place: {place_tables} tables carry verified place columns; clocks: {time_tables} tables")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
