"""
The Library compiler -- one deterministic layout for all 1,043 tables.

    python -m viz.compile_library        # -> outputs/library.json

Supersedes viz/compile_anatomy.py (368 charted tables, three lenses) and
viz/compile_atlas.py (1,043 tables, presence states). One universe, one JSON,
read by viz/library_app.py. Heavy thinking happens HERE, at build time; the
renderer just draws a file.

Determinism is load-bearing. Same inputs -> byte-identical output, every run.
Nothing here uses an unseeded RNG or the wall clock.

THE UNIVERSE is every fingerprinted table -- 1,043 of them, indexed by sorted
name so a table's number never changes between builds. Each carries a presence
state:

    lit        has at least one verified link
    dark       carries a real, populated ID and still links to nothing
    keyless    no populated ID column at all -- nothing to join on yet
    uncharted  never put through link discovery (the parked PORTAL crawl)

Presence-first: all four states are drawn, all four are clickable. The
uncharted tables are quiet, not absent -- and never the headline.

THE THREE LENSES share ONE coordinate box, so a table keeps its identity and
simply MOVES when the arrangement changes. The compiler emits, per lens, a
ready-to-interpolate [x, y] per table -- the renderer's morph is a pure
lookup, no special cases.

    subject      domain rooms (squarified treemap); uncharted tables live in
                 an annex band along the bottom edge
    connection   tables fall toward the IDs they carry; keyless in the centre
                 void, uncharted on an outer ring
    journey      the dbt pipeline, five banks left to right in run order;
                 tables never wired into the build sit in a dimmed siding
                 left of intake

INPUTS (all on disk, zero Snowflake cost)
    library-onboarding/ripple_dbt/target/manifest.json   the dbt DAG
    outputs/connect_graph.json          charted tables + verified links
    outputs/connect_fingerprints.json   1,043 tables x ID columns x fill
    outputs/thelibrary_inventory.json   row counts
    outputs/thelibrary_content.json     plain-English one-liners
"""

from __future__ import annotations

import argparse
import collections
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "library-onboarding" / "ripple_dbt" / "target" / "manifest.json"
GRAPH = ROOT / "outputs" / "connect_graph.json"
FINGERPRINTS = ROOT / "outputs" / "connect_fingerprints.json"
INVENTORY = ROOT / "outputs" / "thelibrary_inventory.json"
CONTENT = ROOT / "outputs" / "thelibrary_content.json"
OUT = ROOT / "outputs" / "library.json"

# The confidence ladder. Meaning and ordering are sacred (design brief D2) --
# strongest first, and a weaker link may never be drawn like a stronger one.
LADDER = ["STEEL", "STRONG", "BRIDGE", "CORROBORATED", "GEO", "PROBABILISTIC"]

LADDER_LABELS = [
    ("Same ID number", "Both records carry the same government ID -- the same "
                       "licence number, the same tax number. Same thing, no doubt."),
    ("Same industry code", "They share an industry or sector code. Very likely "
                           "the same thing, not quite certain."),
    ("Through a third file", "Not linked directly. A third dataset knows them "
                             "both, so we can get from one to the other."),
    ("Same name and place", "Same name, same location. Better than a name on "
                            "its own -- still not proof."),
    ("Same place only", "Only the location lines up. A hint, nothing more."),
    ("Similar name only", "The names look alike. That's a hunch, and a person "
                          "has to check it."),
]

# The pipeline stages, in run order.
STAGES = [
    ("intake", "AS IT ARRIVED", "Raw files, exactly as the agency published "
                                "them. Nothing cleaned, nothing thrown away."),
    ("staging", "TIDIED UP", "The same data, made usable: dates turned into "
                             "dates, columns given real names. One for each "
                             "raw file."),
    ("bridge", "COMBINED", "The few places where several sources are welded "
                           "into one record before anything reads them."),
    ("shelf", "READY TO USE", "The finished tables, sorted by subject. This is "
                              "what an investigation actually reads."),
    ("desk", "NEEDS A PERSON", "The end of the line: lists of flagged people "
                               "and companies waiting for someone to check "
                               "them."),
]

DESK_SCHEMAS = {"REVIEW"}

# Presence states, in brightness order. Index is what the payload stores.
STATE_NAMES = ["lit", "dark", "keyless", "uncharted"]
LIT, DARK, KEYLESS, UNCHARTED = range(4)

# Classification vocabularies, NOT identity. connect/discover.py excludes
# these from edge generation for the same reason: two firms sharing a NAICS
# code are in the same industry, not the same entity. They still show in a
# table's key list (they're real columns) but they can't make a table "dark"
# and they exert no layout pull.
VOCAB_FAMILIES = {"NAICS", "SIC", "NCES"}

# An ID only tells you something if it's rare. Nearly every table carries a
# name and a ZIP code, so those can't pick out anything on their own. The
# renderer reads this from the payload rather than hard-coding its own copy.
COMMON_ID_CUTOFF = 45

# One shared coordinate box for all three lenses -- what lets a table keep its
# identity and simply move when the arrangement changes.
BOX = (1600.0, 900.0)


# ------------------------------------------------------------------ helpers


def seeded(n: int) -> float:
    """Deterministic [0,1) from an integer. mulberry32's mixing, one step."""
    n = (n + 0x6D2B79F5) & 0xFFFFFFFF
    t = n
    t = (t ^ (t >> 15)) * (t | 1) & 0xFFFFFFFF
    t ^= (t + ((t ^ (t >> 7)) * (t | 61) & 0xFFFFFFFF)) & 0xFFFFFFFF
    t &= 0xFFFFFFFF
    return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296.0


def key_of(name: str) -> int:
    """Stable hash of a table name -> int. Not Python's salted hash()."""
    h = 2166136261
    for ch in name:
        h = ((h ^ ord(ch)) * 16777619) & 0xFFFFFFFF
    return h


def squarify(items, x, y, w, h):
    """Squarified treemap. items = [(id, weight)], returns [(id, x, y, w, h)].
    Deterministic: no RNG, stable sort."""
    out = []
    items = [(i, max(float(v), 1e-9)) for i, v in items if v is not None]
    if not items:
        return out
    total = sum(v for _, v in items)
    scale = (w * h) / total
    items = sorted(items, key=lambda t: (-t[1], t[0]))
    rest = [(i, v * scale) for i, v in items]

    def worst(row, length):
        if not row or length <= 0:
            return math.inf
        s = sum(row)
        mx, mn = max(row), min(row)
        return max((length * length * mx) / (s * s), (s * s) / (length * length * mn))

    while rest:
        length = min(w, h)
        row, row_ids = [], []
        while rest:
            nxt = rest[0][1]
            if row and worst(row + [nxt], length) > worst(row, length):
                break
            row_ids.append(rest[0][0])
            row.append(nxt)
            rest.pop(0)
        s = sum(row)
        thick = s / length if length else 0
        off = 0.0
        for rid, val in zip(row_ids, row):
            side = val / thick if thick else 0
            if w >= h:
                out.append((rid, x, y + off, thick, side))
            else:
                out.append((rid, x + off, y, side, thick))
            off += side
        if w >= h:
            x += thick
            w -= thick
        else:
            y += thick
            h -= thick
    return out


def honesty(k: dict) -> float:
    """How real a key column is: fill x sqrt(distinct/nonnull).

    A column that is 100% 'populated' with one repeated placeholder collapses
    toward zero -- the NPPES EIN / NOAA imo_number trap, encoded so it can
    never fool a layout again.
    """
    nonnull = k.get("nonnull") or 0
    if nonnull <= 0:
        return 0.0
    fill = (k.get("populated_pct") or 0.0) / 100.0
    return fill * math.sqrt(min(1.0, (k.get("distinct") or 0) / nonnull))


# ------------------------------------------------------------------- reading


def read_dbt():
    """The lineage DAG. Every object, its job, and what it runs after."""
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    nodes, sources, child_map = m["nodes"], m["sources"], m["child_map"]
    models = {k: v for k, v in nodes.items() if v["resource_type"] == "model"}

    objects = {}
    for uid, s in sources.items():
        objects[uid] = {
            "name": s["name"].upper(),
            "stage": "intake",
            "schema": s.get("schema", ""),
            "desc": (s.get("description") or "").strip(),
        }
    for uid, mo in models.items():
        top = mo["path"].split("/")[0]
        if top == "staging":
            stage = "staging"
        elif top == "intermediate":
            stage = "bridge"
        elif mo.get("schema") in DESK_SCHEMAS:
            stage = "desk"
        else:
            stage = "shelf"
        objects[uid] = {
            "name": mo["name"].upper(),
            "stage": stage,
            "schema": mo.get("schema", ""),
            "desc": (mo.get("description") or "").strip(),
        }

    lineage = []
    for parent, kids in child_map.items():
        if parent not in objects:
            continue
        for kid in kids:
            if kid in objects and kid in models:
                lineage.append((parent, kid))
    lineage.sort()
    return objects, lineage, models, sources, child_map


def resolve_domains(names, sources, models, child_map):
    """A landing table's real subject = the schema of the mart built from it.

    The domain label on the connect graph is 62% 'other' -- unusable. Walking
    the dbt DAG downstream resolves the real subject for most charted tables.
    """
    by_name = {v["name"].upper(): k for k, v in sources.items()}
    marts = {
        k: v.get("schema")
        for k, v in models.items()
        if v["path"].split("/")[0] == "marts"
    }

    def descend(uid, seen):
        found = []
        for kid in child_map.get(uid, []):
            if kid in seen or kid not in models:
                continue
            seen.add(kid)
            if kid in marts:
                found.append(marts[kid])
            else:
                found.extend(descend(kid, seen))
        return found

    out = {}
    for name in names:
        uid = by_name.get(name)
        if not uid:
            continue
        hits = descend(uid, set())
        if hits:
            counts = collections.Counter(hits)
            out[name] = max(counts.items(), key=lambda t: (t[1], t[0]))[0]
    return out


# ------------------------------------------------------------------ building


def build():
    objects, lineage, models, sources, child_map = read_dbt()
    graph = json.loads(GRAPH.read_text(encoding="utf-8"))
    fps = json.loads(FINGERPRINTS.read_text(encoding="utf-8"))
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    content = json.loads(CONTENT.read_text(encoding="utf-8"))

    fps = {k: v for k, v in fps.items() if isinstance(v, dict)}
    names = sorted(fps)                      # THE universe: index never changes
    idx = {n: i for i, n in enumerate(names)}
    N = len(names)

    graph_ids = {n["id"] for n in graph["nodes"]}
    graph_rows = {n["id"]: n.get("rows") or 0 for n in graph["nodes"]}

    degree = collections.Counter()
    for e in graph["edges"]:
        degree[e["a"]] += 1
        degree[e["b"]] += 1

    domains = resolve_domains(names, sources, models, child_map)

    rows_by_name = {}
    for rec in inventory:
        rows_by_name[rec["physical_name"].upper()] = rec.get("row_count") or 0

    blurb = {}
    for rec in content:
        fn = (rec.get("friendly_name") or "").upper()
        one = (rec.get("one_liner") or "").strip()
        if fn and one:
            blurb[fn] = one
        phys = rec["object_fqn"].split(".")[-1].upper()
        if one:
            blurb.setdefault(phys, one)

    desc_by_name = {}
    for o in objects.values():
        if o["desc"]:
            desc_by_name.setdefault(o["name"], o["desc"].split("\n")[0][:260])

    # ---- every table: rows, keys (honest ones only), state, domain
    tables = []
    for name in names:
        rec = fps[name]
        keys = sorted({
            k["key"] for k in rec.get("keys", [])
            if isinstance(k, dict) and honesty(k) > 0
        })
        if name not in graph_ids:
            state = UNCHARTED
        elif degree.get(name, 0) > 0:
            state = LIT
        elif set(keys) - VOCAB_FAMILIES:
            state = DARK
        else:
            state = KEYLESS
        tables.append({
            "n": name,
            "rows": rec.get("rows") or rows_by_name.get(name)
                    or graph_rows.get(name, 0) or 0,
            "deg": degree.get(name, 0),
            "keys": keys,
            "dom": domains.get(name, "UNFILED"),
            "state": state,
            "desc": blurb.get(name, desc_by_name.get(name, "")),
        })

    # ---- edges, re-indexed into the 1,043-table universe
    tier_idx = {t: i for i, t in enumerate(LADDER)}
    edges = []
    for e in sorted(graph["edges"], key=lambda e: (e["a"], e["b"], e["key"])):
        if e["a"] not in idx or e["b"] not in idx:
            continue
        edges.append([
            idx[e["a"]], idx[e["b"]],
            tier_idx.get(e["tier"], len(LADDER) - 1),
            e["key"],
            int(e.get("matched") or 0),
        ])

    # ---- stages with real counts
    stage_members = collections.defaultdict(list)
    for uid, o in objects.items():
        stage_members[o["stage"]].append(uid)
    stages = [{"id": sid, "label": label, "role": role,
               "count": len(stage_members[sid])}
              for sid, label, role in STAGES]

    layouts = {
        "stacks": layout_stacks(tables),
        "constellation": layout_constellation(tables),
        "refinery": layout_refinery(objects, lineage, tables),
    }

    # Charted table i's seat on the pipeline (index into refinery.nodes), or
    # its siding seat -- every table has one; -1 never appears any more.
    xref = layouts["refinery"].pop("xref")

    # ---- the morph's food: one [x,y] per table per lens, parallel arrays.
    positions = {
        "subject": [[c["x"] + c["w"] / 2, c["y"] + c["h"] / 2]
                    for c in sorted(layouts["stacks"]["cells"],
                                    key=lambda c: c["i"])],
        "connection": [[n["x"], n["y"]]
                       for n in layouts["constellation"]["nodes"]],
        "journey": [[layouts["refinery"]["nodes"][s]["x"],
                     layouts["refinery"]["nodes"][s]["y"]] for s in xref],
    }

    counts = collections.Counter(t["state"] for t in tables)
    hubs = sorted(((t["n"], t["deg"]) for t in tables if t["deg"] > 0),
                  key=lambda t: (-t[1], t[0]))[:12]

    payload = {
        "meta": {
            "tables": N,
            "links": len(edges),
            "pairs_tested": (graph.get("meta") or {}).get("pairs_tested"),
            "states": {STATE_NAMES[s]: counts.get(s, 0) for s in range(4)},
            "dbt_objects": len(objects),
            "lineage_edges": len(lineage),
            "stage_counts": {s["id"]: s["count"] for s in stages},
            "domains_resolved": len(domains),
            "connected_rows": sum(t["rows"] for t in tables if t["deg"] > 0),
            "hubs": hubs,
            "common_id_cutoff": COMMON_ID_CUTOFF,
        },
        "ladder_labels": [list(x) for x in LADDER_LABELS],
        "stages": stages,
        "state_names": STATE_NAMES,
        "tables": tables,
        "edges": edges,
        "layouts": layouts,
        "xref": xref,
        "positions": positions,
        "box": list(BOX),
    }
    return payload


# ------------------------------------------------------------------ layouts


def layout_stacks(tables):
    """SUBJECT lens. Domain rooms squarified by table count; one shelf cell
    per table sized by log-rows. Uncharted tables live in an annex band along
    the bottom edge -- present, seated, quiet."""
    BW, BH = BOX
    ANNEX_H = BH * 0.10
    main_h = BH - ANNEX_H - 4

    charted = [i for i, t in enumerate(tables) if t["state"] != UNCHARTED]
    annexed = [i for i, t in enumerate(tables) if t["state"] == UNCHARTED]

    by_dom = collections.defaultdict(list)
    for i in charted:
        by_dom[tables[i]["dom"]].append(i)

    rooms_geo = squarify([(d, len(v)) for d, v in by_dom.items()],
                         6, 6, BW - 12, main_h - 12)

    out_rooms, out_cells = [], []
    for dom, x, y, w, h in sorted(rooms_geo, key=lambda r: r[0]):
        out_rooms.append({"d": dom, "x": round(x, 2), "y": round(y, 2),
                          "w": round(w, 2), "h": round(h, 2),
                          "n": len(by_dom[dom])})
        inner = (x + 3, y + 15, max(w - 6, 1), max(h - 18, 1))
        # Row counts span nine orders of magnitude; log-weight or one 300M-row
        # table eats the whole room.
        items = [(i, math.log10(max(tables[i]["rows"], 1)) + 1)
                 for i in by_dom[dom]]
        for i, cx, cy, cw, ch in squarify(items, *inner):
            out_cells.append({"i": i, "x": round(cx, 2), "y": round(cy, 2),
                              "w": round(cw, 2), "h": round(ch, 2)})

    # The annex: everything collected but not yet put through link discovery.
    # One long quiet band -- a real room with a real door, not a footnote.
    ay = BH - ANNEX_H
    annex = {"x": 6.0, "y": round(ay, 2), "w": BW - 12, "h": round(ANNEX_H - 6, 2)}
    items = [(i, math.log10(max(tables[i]["rows"], 1)) + 1) for i in annexed]
    for i, cx, cy, cw, ch in squarify(items, annex["x"] + 2, annex["y"] + 12,
                                      annex["w"] - 4, annex["h"] - 14):
        out_cells.append({"i": i, "x": round(cx, 2), "y": round(cy, 2),
                          "w": round(cw, 2), "h": round(ch, 2)})

    out_cells.sort(key=lambda c: c["i"])
    return {"box": list(BOX), "rooms": out_rooms, "cells": out_cells,
            "annex": annex}


def layout_constellation(tables):
    """CONNECTION lens. Tables fall toward the IDs they carry.

    A table belongs to its RAREST key -- averaging drags everything into one
    NAME/ZIP blob. Keyless tables sit in the centre void (they speak none of
    the Library's languages); uncharted tables ring the outside, dim.
    """
    BW, BH = BOX
    cx, cy, rx, ry = BW / 2, BH / 2, BW * 0.355, BH * 0.345

    fam = collections.Counter()
    for t in tables:
        if t["state"] == UNCHARTED:
            continue      # the parked crawl doesn't vote on well geography
        for k in t["keys"]:
            if k not in VOCAB_FAMILIES:
                fam[k] += 1
    wells = [k for k, _ in sorted(fam.items(), key=lambda t: (-t[1], t[0]))][:14]
    n = len(wells)
    well_pos = {}
    for i, k in enumerate(wells):
        ang = -math.pi / 2 + 2 * math.pi * i / n
        well_pos[k] = (cx + rx * math.cos(ang), cy + ry * math.sin(ang))

    nodes = []
    homed = collections.Counter()
    for t in tables:
        h = key_of(t["n"])
        mine = [k for k in t["keys"] if k in well_pos]
        if t["state"] == UNCHARTED:
            # The outer ring: collected, not yet run through discovery. Off the
            # charted field because that is exactly where it is.
            a = seeded(h) * 2 * math.pi
            r = 1.28 + 0.10 * seeded(h ^ 0x85EBCA6B)
            x, y = cx + rx * r * math.cos(a), cy + ry * r * math.sin(a)
            w = 0
        elif not mine:
            # Keyless: inside the field, touching no well, because there is
            # nothing here to join on yet.
            a = seeded(h) * 2 * math.pi
            r = 0.10 + 0.14 * seeded(h ^ 0x85EBCA6B)
            x, y = cx + rx * r * math.cos(a), cy + ry * r * math.sin(a)
            w = 0
        else:
            home = min(mine, key=lambda k: (fam[k], k))
            homed[home] += 1
            hx, hy = well_pos[home]
            others = [k for k in mine
                      if k != home and fam[k] <= COMMON_ID_CUTOFF]
            if others:
                ox = sum(well_pos[k][0] for k in others) / len(others)
                oy = sum(well_pos[k][1] for k in others) / len(others)
                pull = min(0.10 + 0.05 * len(others), 0.22)
                hx += (ox - hx) * pull
                hy += (oy - hy) * pull
            spread = 62 if not others else 48
            a = seeded(h) * 2 * math.pi
            r = spread * math.sqrt(seeded(h ^ 0x9E3779B9))
            x, y = hx + r * math.cos(a), hy + r * math.sin(a)
            # w counts DISCRIMINATING keys only -- two rare IDs on one table is
            # what lets a question cross between worlds.
            w = sum(1 for k in mine if fam[k] <= COMMON_ID_CUTOFF)
        nodes.append({"x": round(x, 2), "y": round(y, 2), "w": w,
                      "keyed": bool(mine)})
    return {
        "box": list(BOX),
        # n = tables that CARRY the key; h = tables FILED here (rarest key).
        "wells": [{"k": k, "x": round(well_pos[k][0], 2),
                   "y": round(well_pos[k][1], 2),
                   "n": fam[k], "h": homed.get(k, 0)} for k in wells],
        "nodes": nodes,
    }


def layout_refinery(objects, lineage, tables):
    """JOURNEY lens. Five banks left to right in run order, plus a dimmed
    siding LEFT of intake for tables never wired into the build. Every table
    gets a real seat -- the renderer never invents a position."""
    BW, BH = BOX
    SIDING_W = BW * 0.115
    top_pad, bot_pad = 26.0, 26.0
    inner_h = BH - top_pad - bot_pad

    order = [s[0] for s in STAGES]
    lanes = {sid: [] for sid in order}
    for uid, o in objects.items():
        lanes[o["stage"]].append(uid)
    for sid in lanes:
        lanes[sid].sort(key=lambda u: (objects[u]["schema"], objects[u]["name"]))

    pos, bands = {}, []
    band_w = (BW - SIDING_W) / len(order)

    def pack(members, x0, width, key):
        """Grid-pack into a band; returns (cols, cell) and fills pos[key]."""
        count = len(members)
        inner_w = width * 0.80
        pad = (width - inner_w) / 2.0
        if count == 0:
            return round(x0 + pad, 2), round(inner_w, 2), 0, 3.0
        cols = max(1, min(28, int(round(math.sqrt(count * inner_w / inner_h)))))
        rows = math.ceil(count / cols)
        cw = inner_w / cols
        ch = min(inner_h / rows, cw * 1.5)
        top = top_pad + (inner_h - ch * rows) / 2.0
        for i, m in enumerate(members):
            c, r = i % cols, i // cols
            pos[key(m)] = [round(x0 + pad + c * cw + cw / 2, 2),
                           round(top + r * ch + ch / 2, 2)]
        # Cell size capped at 13 so a 4-object bank doesn't render as slabs.
        return (round(x0 + pad, 2), round(inner_w, 2), cols,
                round(min(min(cw, ch) * 0.62, 13.0), 2))

    # The siding first: fingerprinted tables with no seat anywhere in the DAG.
    dbt_names = {o["name"] for o in objects.values()}
    unwired = sorted(t["n"] for t in tables if t["n"] not in dbt_names)
    x, w, cols, cell = pack(unwired, 0.0, SIDING_W, lambda name: ("siding", name))
    bands.append({"id": "siding", "x": x, "w": w, "cols": cols, "cell": cell})

    for si, sid in enumerate(order):
        x0 = SIDING_W + si * band_w
        x, w, cols, cell = pack(lanes[sid], x0, band_w, lambda uid: uid)
        bands.append({"id": sid, "x": x, "w": w, "cols": cols, "cell": cell})

    uids = sorted(u for u in pos if not isinstance(u, tuple))
    nodes = [{"id": objects[u]["name"], "s": objects[u]["stage"],
              "x": pos[u][0], "y": pos[u][1]} for u in uids]
    uidx = {u: i for i, u in enumerate(uids)}
    for name in unwired:                     # siding seats come after dbt seats
        nodes.append({"id": name, "s": "siding",
                      "x": pos[("siding", name)][0],
                      "y": pos[("siding", name)][1]})

    # Intake sources are the tables themselves; a name can also appear as a
    # staging model. An intake/siding seat wins; any seat beats none.
    seat_by_name = {}
    for i, nd in enumerate(nodes):
        if nd["s"] in ("intake", "siding") or nd["id"] not in seat_by_name:
            seat_by_name.setdefault(nd["id"], i)
            if nd["s"] in ("intake", "siding"):
                seat_by_name[nd["id"]] = i
    xref = [seat_by_name[t["n"]] for t in tables]

    links = sorted({(uidx[a], uidx[b]) for a, b in lineage
                    if a in uidx and b in uidx})
    return {"box": list(BOX), "bands": bands, "nodes": nodes,
            "links": [list(l) for l in links], "xref": xref}


# -------------------------------------------------------------------- output


def main():
    argparse.ArgumentParser(description=__doc__).parse_args()
    payload = build()
    OUT.write_text(json.dumps(payload, indent=1, sort_keys=True),
                   encoding="utf-8")
    m = payload["meta"]
    print(f"library.json  {OUT.stat().st_size/1024:.0f} KB")
    print(f"  tables  {m['tables']:,}   links {m['links']:,}")
    for s, c in m["states"].items():
        print(f"  {s:<10}{c:>5,}")
    print(f"  dbt objects {m['dbt_objects']:,}  ({m['lineage_edges']:,} lineage edges)")


if __name__ == "__main__":
    main()
