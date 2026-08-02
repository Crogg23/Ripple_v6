"""
DEEPFIELD atlas compiler.

Reads the connect engine's outputs and bakes a deterministic layout for the
Library's structural map. Heavy thinking happens HERE, at build time; the
renderer just draws a file (constitution section 7: AI/compute is a build-time
tool, not a runtime dependency).

    python -m viz.compile_atlas            # -> outputs/atlas.json
    python -m viz.compile_atlas --inline   # also inject into docs/deepfield.html

Inputs (all free, on disk, zero Snowflake cost):
    outputs/connect_fingerprints.json   every table x every ID column x fill
    outputs/connect_graph.json          the verified edges

Determinism is load-bearing. Same inputs -> byte-identical layout, every run,
forever. Position becomes memory: a source you learned last month is in the
same place today. Nothing here may use an unseeded RNG or wall-clock time.

The four states a table can be in -- this is the spine of the whole design
(constitution section 1.1, the lensing method). Verified live 2026-08-02:

    LIT        155  in the graph, has >=1 verified edge
    DARK        82  in the graph, carries a real key, and STILL has zero edges
    KEYLESS    131  in the graph but no populated identity column at all
    UNCHARTED  675  never entered the graph (PORTAL_* crawl, parked by an open
                    decision in connect/discover.py EDGE_UNIVERSE_EXCLUDE_*)

These must never be drawn alike, because each one is a different job:

    DARK       "we looked, with a real key, and found nothing."
               That is EVIDENCE, and it is the lensing hunt list. 82 is small
               enough for a human to actually work through.
    KEYLESS    "we cannot look, there is nothing to join on."
               That is an ACQUISITION problem -- go get better columns.
    UNCHARTED  "we never looked, on purpose."
               That is a parked DECISION (the portal crawl), Chris's to make.

Collapsing these into one grey "unconnected" bucket -- which is what every
off-the-shelf tool does -- destroys the only distinction that tells you what
to do next.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FP_PATH = ROOT / "outputs" / "connect_fingerprints.json"
GRAPH_PATH = ROOT / "outputs" / "connect_graph.json"
OUT_PATH = ROOT / "outputs" / "atlas.json"
HTML_PATH = ROOT / "docs" / "deepfield.html"

# ---------------------------------------------------------------- constants

# Key families that get their own anchor well, in a fixed, hand-ordered
# sequence. Order determines angular position, so DO NOT reorder casually --
# reordering rotates the entire map and burns everyone's spatial memory.
# Grouped so related families land as neighbours (health next to health,
# money next to money), which is what makes the finished chart legible.
WELLS: list[tuple[str, str, str]] = [
    # (key family, display label, semantic band)
    ("NPI",         "NPI",          "health"),
    ("CCN",         "CCN",          "health"),
    ("DEA",         "DEA",          "health"),
    ("EIN",         "EIN",          "money"),
    ("UEI",         "UEI",          "money"),
    ("DUNS",        "DUNS",         "money"),
    ("CIK",         "CIK",          "money"),
    ("LEI",         "LEI",          "money"),
    ("FEC_CAND_ID", "FEC",          "money"),
    ("BIOGUIDE",    "BIOGUIDE",     "civic"),
    ("DOCKET",      "DOCKET",       "civic"),
    ("FRS_ID",      "FRS",          "environment"),
    ("PWSID",       "PWSID",        "environment"),
    ("MINE_ID",     "MINE",         "environment"),
    ("IMO",         "IMO",          "environment"),
    ("FIPS",        "FIPS",         "place"),
    ("ZIP",         "ZIP",          "place"),
    ("ADDRESS",     "ADDRESS",      "place"),
    ("LATLON",      "LATLON",       "place"),
    ("STATE",       "STATE",        "place"),
    ("COUNTRY",     "COUNTRY",      "place"),
    ("NAME",        "NAME",         "name"),
]

# Families that are really the same well wearing a different column name.
# Folding them here (rather than minting a well for a 1-table family) keeps the
# anchor ring readable without silently dropping the table into the void.
FAMILY_ALIASES = {
    "DEA_NO":       "DEA",
    "FEC_CMTE_ID":  "FEC_CAND_ID",   # candidate + committee: both FEC identity
    "MMSI":         "IMO",           # both vessel identity
    "GEOM":         "LATLON",        # geometry is coordinates
    "ICPSR":        "BIOGUIDE",      # both legislator identity
}

# Classification vocabularies, NOT identity. connect/discover.py excludes these
# from edge generation for the same reason (VOCAB_KEYS): two firms sharing a
# NAICS code are in the same industry, not the same entity. They must not exert
# layout pull either, or every table in an industry would clump as if related.
VOCAB_FAMILIES = {"NAICS", "SIC", "NCES"}

BAND_HUE = {
    "health":      "#55c2d4",
    "money":       "#d98a5f",
    "civic":       "#e0b04a",
    "environment": "#7fbf6e",
    "place":       "#5f7fd9",
    "name":        "#9b85e0",
}

# Proof tiers, ordered weakest -> strongest. Index is what the renderer stores.
TIERS = ["GEO", "BRIDGE", "CORROBORATED", "STRONG", "STEEL"]

STATE_LIT, STATE_DARK, STATE_KEYLESS, STATE_UNCHARTED = 0, 1, 2, 3
STATE_NAMES = ["lit", "dark", "keyless", "uncharted"]

# Canvas is unitless; the renderer scales to fit. Field radius vs the parked ring.
FIELD_R = 1.0
RING_R_MIN, RING_R_MAX = 1.30, 1.46


# ---------------------------------------------------------------- utilities

def mulberry32(seed: int):
    """Deterministic PRNG, bit-identical to the canonical JS mulberry32 the
    renderer uses, so layout jitter can be reproduced on either side.

    Verified against the JS reference for seed 20260802:
        0.3173061307, 0.1282845410, 0.4758024374, 0.9570986144, 0.1107757660

    The subtlety that makes a hand-port wrong: in
        t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    `^` binds LOOSER than `+`, so the trailing `^ t` applies to the whole sum.
    Dropping it still yields a plausible-looking random sequence -- which is
    exactly why it survives casual testing. Unsigned-vs-signed masking is NOT
    a problem here: multiplication mod 2^32 is representation-independent.
    """
    state = seed & 0xFFFFFFFF

    def nxt() -> float:
        nonlocal state
        state = (state + 0x6D2B79F5) & 0xFFFFFFFF
        t = state
        t = (t ^ (t >> 15)) * (1 | t) & 0xFFFFFFFF
        t = ((t + ((t ^ (t >> 7)) * (61 | t) & 0xFFFFFFFF)) ^ t) & 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296.0

    return nxt


def split_key(key: str) -> list[str]:
    """Edge keys can be composite: 'CCN~NPI' (bridged), 'NAME@ZIP' (compound).
    Both separators mean 'this edge travels over more than one family'."""
    return [p for p in re.split(r"[~@]", key) if p]


def base_family(key: str) -> str:
    """Map a fingerprint/edge key onto its anchor well, or '' if it has none.

    Resolution order: exact well, alias, then each component of a composite key
    ('CCN~NPI', 'NAME@ZIP'). Vocabulary families resolve to '' on purpose -- see
    VOCAB_FAMILIES.
    """
    known = {w[0] for w in WELLS}
    for part in [key] + split_key(key):
        if part in VOCAB_FAMILIES:
            continue
        if part in known:
            return part
        alias = FAMILY_ALIASES.get(part)
        if alias:
            return alias
    return ""


def key_weight(k: dict) -> float:
    """How much this column should pull its table toward that key's well.

    Two factors, both mandated by constitution section 7's honesty rules:
      fill      -- what fraction of rows actually carry a value
      honesty   -- distinct/nonnull, which collapses toward 0 for a
                   sentinel-masked column that LOOKS fully populated
                   (the NPPES EIN / NOAA imo_number trap)

    A column that is 100% 'populated' with one repeated placeholder gets
    almost no pull, which is the correct behaviour: it is not a real key.
    """
    nonnull = k.get("nonnull") or 0
    if nonnull <= 0:
        return 0.0
    fill = (k.get("populated_pct") or 0.0) / 100.0
    distinct = k.get("distinct") or 0
    honesty = math.sqrt(min(1.0, distinct / nonnull)) if nonnull else 0.0
    # Hard-ID families pull harder than soft ones. A shared NAME or ADDRESS is
    # a hunch; a shared NPI is a fact. The layout must reflect that ordering or
    # the name well would swallow the map (1,242 of 2,694 edges ride NAME@ZIP).
    fam = base_family(k.get("key") or "")
    if fam in ("NAME", "ADDRESS"):
        tier_boost = 0.30
    elif fam in ("STATE", "COUNTRY", "ZIP", "LATLON"):
        tier_boost = 0.55
    else:
        tier_boost = 1.0
    return fill * honesty * tier_boost


# ---------------------------------------------------------------- layout

def place_wells() -> list[dict]:
    """Fixed anchor positions. Wells sit on an ellipse, evenly spaced by index,
    with a deterministic radial stagger so the ring does not read as a clock
    face. Never randomised, never recomputed from edge counts -- if well
    positions moved when the data moved, the map would lose its permanence."""
    out = []
    n = len(WELLS)
    for i, (key, label, band) in enumerate(WELLS):
        ang = -math.pi / 2 + (i / n) * math.tau + 0.13
        # Stagger radius on a fixed 5-cycle: readable, deterministic, no RNG.
        stagger = 0.62 + 0.38 * ((i * 7) % 5) / 4.0
        r = FIELD_R * 0.74 * stagger
        out.append({
            "key": key, "label": label, "band": band, "hue": BAND_HUE[band],
            "x": math.cos(ang) * r,
            "y": math.sin(ang) * r * 0.66,   # squashed: a chart, not a clock
        })
    return out


def relax(nodes: list[dict], iterations: int = 260, min_dist: float = 0.022) -> None:
    """Collision relaxation via a uniform spatial hash. O(n) per pass instead
    of O(n^2), and fully deterministic: cells are visited in sorted order and
    displacement is symmetric, so there is no iteration-order drift."""
    if not nodes:
        return
    cell = min_dist * 2.0
    for step in range(iterations):
        grid: dict[tuple[int, int], list[int]] = {}
        for i, nd in enumerate(nodes):
            gx, gy = int(nd["x"] // cell), int(nd["y"] // cell)
            grid.setdefault((gx, gy), []).append(i)

        moved = 0.0
        for (gx, gy) in sorted(grid.keys()):
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    other = grid.get((gx + dx, gy + dy))
                    if not other:
                        continue
                    for i in grid[(gx, gy)]:
                        for j in other:
                            if j <= i:
                                continue
                            a, b = nodes[i], nodes[j]
                            vx, vy = b["x"] - a["x"], b["y"] - a["y"]
                            d2 = vx * vx + vy * vy
                            if d2 >= min_dist * min_dist:
                                continue
                            if d2 == 0:
                                # Exactly coincident (identical barycentre AND
                                # identical jitter). Nudge deterministically by
                                # index parity rather than skipping, or the pair
                                # stays welded together forever.
                                nodes[j]["x"] += min_dist * 0.5
                                nodes[j]["y"] += min_dist * 0.25
                                moved += min_dist * 0.5
                                continue
                            d = math.sqrt(d2)
                            push = (min_dist - d) * 0.5
                            ux, uy = vx / d, vy / d
                            a["x"] -= ux * push; a["y"] -= uy * push
                            b["x"] += ux * push; b["y"] += uy * push
                            moved += push
        if moved < 1e-5:
            break


# ---------------------------------------------------------------- compile

def compile_atlas() -> dict:
    fp = json.loads(FP_PATH.read_text(encoding="utf-8"))
    graph = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))

    # Tolerate a partially-written or older-format upstream file rather than
    # dying on a KeyError halfway through: this runs unattended after the
    # connect engine, and a crash here would look like the engine failed.
    fp = {k: v for k, v in (fp or {}).items() if isinstance(v, dict)}
    if not fp:
        raise SystemExit("compile_atlas: no usable fingerprints; run `python -m connect fingerprint` first")
    graph_nodes = [n for n in (graph.get("nodes") or []) if isinstance(n, dict) and n.get("id")]
    graph_edges = [e for e in (graph.get("edges") or [])
                   if isinstance(e, dict) and e.get("a") and e.get("b")]

    graph_ids = {n["id"] for n in graph_nodes}
    graph_rows = {n["id"]: n.get("rows") or 0 for n in graph_nodes}

    degree: dict[str, int] = {}
    for e in graph_edges:
        degree[e["a"]] = degree.get(e["a"], 0) + 1
        degree[e["b"]] = degree.get(e["b"], 0) + 1

    wells = place_wells()
    well_index = {w["key"]: i for i, w in enumerate(wells)}

    rnd = mulberry32(20260802)

    # ---- classify + place every table, in sorted order for determinism
    nodes: list[dict] = []
    for name in sorted(fp.keys()):
        rec = fp[name]
        rows = rec.get("rows") or graph_rows.get(name, 0) or 0

        # Which wells does this table speak, and how strongly?
        pulls: dict[int, float] = {}
        for k in (rec.get("keys") or []):
            if not isinstance(k, dict):
                continue
            fam = base_family(k.get("key") or "")
            if not fam:
                continue
            w = key_weight(k)
            if w <= 0:
                continue
            wi = well_index[fam]
            pulls[wi] = pulls.get(wi, 0.0) + w

        dominant = max(pulls, key=lambda i: (pulls[i], -i)) if pulls else -1

        if name not in graph_ids:
            state = STATE_UNCHARTED
        elif degree.get(name, 0) > 0:
            state = STATE_LIT
        elif pulls:
            state = STATE_DARK        # has a real key and still no edge
        else:
            state = STATE_KEYLESS     # nothing to join on

        if state == STATE_UNCHARTED:
            # The parked ring, well outside the charted field. Deliberately
            # reads as "off the map", because that is exactly what it is.
            ang = rnd() * math.tau
            rr = RING_R_MIN + rnd() * (RING_R_MAX - RING_R_MIN)
            x, y = math.cos(ang) * rr, math.sin(ang) * rr * 0.66
        elif state == STATE_KEYLESS:
            # The void at the centre: inside the field, touching no well,
            # because it speaks none of the Library's languages.
            ang = rnd() * math.tau
            rr = 0.055 + rnd() * 0.075
            x, y = math.cos(ang) * rr, math.sin(ang) * rr * 0.66
        else:
            # LIT and DARK are placed identically, on purpose. A dark table sits
            # exactly where its keys say it belongs -- right beside the well it
            # speaks, with no corridor running to it. That visible absence, in
            # the middle of lit territory, IS the lensing signal.
            tw = sum(pulls.values())
            x = sum(wells[i]["x"] * w for i, w in pulls.items()) / tw
            y = sum(wells[i]["y"] * w for i, w in pulls.items()) / tw
            # Jitter scaled by how many languages it speaks: monolingual tables
            # cling to their well, polyglots spread into the straits between.
            spread = 0.055 + 0.055 * min(3, len(pulls) - 1)
            x += (rnd() - 0.5) * spread
            y += (rnd() - 0.5) * spread * 0.7

        nodes.append({
            "name": name, "x": x, "y": y, "rows": rows, "state": state,
            "well": dominant, "deg": degree.get(name, 0),
            "langs": len(pulls),
        })

    # Relax only the charted field; the parked ring is meant to look like a ring.
    relax([n for n in nodes if n["state"] != STATE_UNCHARTED])

    node_index = {n["name"]: i for i, n in enumerate(nodes)}

    # ---- edges
    edges = []
    dropped = 0
    for e in sorted(graph_edges, key=lambda e: (e["a"], e["b"], e.get("key") or "")):
        ai, bi = node_index.get(e["a"]), node_index.get(e["b"])
        if ai is None or bi is None:
            # An edge whose endpoint has no fingerprint. Zero of these today,
            # but a stale fingerprint file would otherwise silently delete
            # verified connections, which is exactly the kind of quiet data
            # loss this platform has been burned by before.
            dropped += 1
            continue
        tier = e.get("tier", "CORROBORATED")
        ti = TIERS.index(tier) if tier in TIERS else 2
        fam = base_family(e.get("key") or "")
        wi = well_index.get(fam, -1)
        edges.append([ai, bi, ti, wi, round(float(e.get("confidence") or 0), 3)])

    # ---- census
    counts = {k: 0 for k in STATE_NAMES}
    rows_by_state = {k: 0 for k in STATE_NAMES}
    for n in nodes:
        k = STATE_NAMES[n["state"]]
        counts[k] += 1
        rows_by_state[k] += n["rows"] or 0

    if dropped:
        print(f"  ! {dropped} edge(s) dropped: endpoint missing from fingerprints "
              f"-- re-run `python -m connect fingerprint`")

    tier_counts: dict[str, int] = {}
    for e in graph_edges:
        t = e.get("tier", "?")
        tier_counts[t] = tier_counts.get(t, 0) + 1

    # NOTE: keyed on the RAW edge key, not base_family(). That is deliberate --
    # 'NAME@ZIP' and 'CCN~NPI' are the things the engine actually matched on,
    # and collapsing them into 'NAME' and 'CCN' would hide that 46% of the mesh
    # rides a compound name+place match rather than a hard ID. Named
    # 'top_keys', not 'top_families', so nobody mistakes it for a family roll-up.
    key_counts: dict[str, int] = {}
    for e in graph_edges:
        key_counts[e.get("key") or "?"] = key_counts.get(e.get("key") or "?", 0) + 1

    hubs = sorted(
        ((n["name"], n["deg"]) for n in nodes if n["deg"] > 0),
        key=lambda t: (-t[1], t[0]),
    )[:12]

    return {
        "meta": {
            "generated_from": "outputs/connect_fingerprints.json + outputs/connect_graph.json",
            "tables_total": len(nodes),
            "counts": counts,
            "rows_by_state": rows_by_state,
            "edges_total": len(edges),
            "pairs_tested": (graph.get("meta") or {}).get("pairs_tested"),
            "tiers": tier_counts,
            "top_keys": sorted(key_counts.items(), key=lambda t: (-t[1], t[0]))[:14],
            "hubs": hubs,
            "extent": round(max(
                (abs(v) for n in nodes for v in (n["x"], n["y"])), default=1.0), 4),
            "extent_y": round(max(
                (abs(n["y"]) for n in nodes), default=1.0), 4),
            "deterministic_seed": 20260802,
        },
        "tiers": TIERS,
        "wells": wells,
        # Compact numeric rows keep the embedded payload small.
        # [x, y, logRows, wellIdx, state, degree, langs]
        "nodes": [
            [round(n["x"], 4), round(n["y"], 4),
             round(math.log10(max(1, n["rows"] or 1)), 3),
             n["well"], n["state"], n["deg"], n["langs"]]
            for n in nodes
        ],
        "names": [n["name"] for n in nodes],
        "edges": edges,
    }


def inline_into_html(atlas: dict) -> bool:
    """Replace the ATLAS payload block inside the standalone HTML so the file
    stays self-contained (no fetch -- it must work from file:// by double-click)."""
    if not HTML_PATH.exists():
        print(f"  ! {HTML_PATH} not found; skipped inlining")
        return False
    html = HTML_PATH.read_text(encoding="utf-8")
    start = "/*ATLAS_START*/"
    end = "/*ATLAS_END*/"
    if start not in html or end not in html:
        print("  ! ATLAS markers not found in deepfield.html; skipped inlining")
        return False
    payload = json.dumps(atlas, separators=(",", ":"))
    pre = html.split(start)[0]
    post = html.split(end)[1]
    HTML_PATH.write_text(f"{pre}{start}\nvar ATLAS={payload};\n{end}{post}", encoding="utf-8")
    print(f"  inlined {len(payload):,} bytes into {HTML_PATH.relative_to(ROOT)}")
    return True


def main() -> None:
    ap = argparse.ArgumentParser(description="Compile the DEEPFIELD atlas layout.")
    ap.add_argument("--inline", action="store_true",
                    help="also inject the payload into docs/deepfield.html")
    args = ap.parse_args()

    atlas = compile_atlas()
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(atlas, separators=(",", ":")), encoding="utf-8")

    m = atlas["meta"]
    c = m["counts"]
    total = max(1, m["tables_total"])
    print(f"atlas -> {OUT_PATH.relative_to(ROOT)}")
    print(f"  tables      {total:,}")
    print(f"  lit         {c['lit']:>5,}  ({c['lit']/total:>5.1%})  connected")
    print(f"  dark        {c['dark']:>5,}  ({c['dark']/total:>5.1%})  has a key, no edge  <- the hunt list")
    print(f"  keyless     {c['keyless']:>5,}  ({c['keyless']/total:>5.1%})  nothing to join on")
    print(f"  uncharted   {c['uncharted']:>5,}  ({c['uncharted']/total:>5.1%})  never entered the graph")
    print(f"  edges       {m['edges_total']:,}")
    print(f"  wells       {len(atlas['wells'])}")

    if args.inline:
        inline_into_html(atlas)


if __name__ == "__main__":
    main()
