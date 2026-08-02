"""
Library anatomy compiler.

Reads what the Library actually IS -- from files already on disk, zero
Snowflake cost -- and bakes three deterministic layouts, one per candidate
visual paradigm. Heavy thinking happens HERE, at build time; the renderer just
draws a file (constitution section 7: AI/compute is a build-time tool, not a
runtime dependency).

    python -m viz.compile_anatomy            # -> outputs/anatomy.json
    python -m viz.compile_anatomy --inline   # also inject into the HTML

Determinism is load-bearing. Same inputs -> byte-identical output, every run.
Nothing here uses an unseeded RNG or the wall clock.

INPUTS (all verified present 2026-08-02)
    library-onboarding/ripple_dbt/target/manifest.json   the dbt DAG: what runs
                                                         after what. THE
                                                         sequential-interaction
                                                         source. 1,344 models,
                                                         1,110 declared sources.
    outputs/connect_graph.json          368 charted tables, 2,694 verified joins
    outputs/connect_fingerprints.json   1,043 tables x every ID column x fill
    outputs/thelibrary_inventory.json   428 objects: row counts, join keys, kind
    outputs/thelibrary_content.json     232 plain-English one-liners

THE THREE AXES, which is the whole point. Chris asked for STRUCTURE,
FUNCTIONAL INFRASTRUCTURE and SEQUENTIAL INTERACTION. They are three different
graphs over the same tables, and they are at right angles to each other:

    STRUCTURE   what exists and how it groups   -> domain rooms, row counts
    FUNCTION    what each part's job is         -> layer role (intake/staging/
                                                   shelf/desk), key families
    SEQUENCE    what feeds what, in what order  -> the dbt lineage DAG

A paradigm that only draws one of the three is only a third of an answer.
Each layout below leads with one axis and carries the other two as overlays.
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
OUT = ROOT / "outputs" / "anatomy.json"
HTML = ROOT / "docs" / "library-anatomy.html"

START = "/*ANATOMY_START*/"
END = "/*ANATOMY_END*/"

# The confidence ladder. Meaning and ordering are sacred (design brief D2) --
# strongest first, and a weaker link may never be drawn like a stronger one.
LADDER = ["STEEL", "STRONG", "BRIDGE", "CORROBORATED", "GEO", "PROBABILISTIC"]

# The pipeline stages, in run order. This IS the functional infrastructure:
# every object in the warehouse is doing exactly one of these five jobs.
STAGES = [
    ("intake", "INTAKE", "Raw landing tables. Whatever the agency published, "
                         "as published. Nothing cleaned, nothing dropped."),
    ("staging", "STAGING", "One view per source. Types cast, columns renamed, "
                           "1:1 with intake. The translation layer."),
    ("bridge", "BRIDGE", "The few places several sources are welded into one "
                         "record before anything reads them."),
    ("shelf", "SHELVES", "The finished, queryable tables, filed by subject. "
                         "This is what an investigation actually reads."),
    ("desk", "THE DESK", "Where the machine hands work to a human. Queues of "
                         "flagged units awaiting sign-off."),
]

# Review-schema models are marts, but functionally they are the end of the
# line: the human hand-off. Splitting them out is what makes the sequence
# readable as a sequence rather than a wall.
DESK_SCHEMAS = {"REVIEW"}


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

    Deterministic: no RNG, input order preserved after a stable sort.
    """
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


def resolve_domains(source_names, sources, models, child_map):
    """A landing table's real subject = the schema of the mart built from it.

    The domain label carried on the connect graph is 62% 'other' -- unusable as
    an organising axis. Walking the dbt DAG downstream instead resolves 342 of
    368 charted tables to a real subject. Verified this session.
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
    for name in source_names:
        uid = by_name.get(name)
        if not uid:
            continue
        hits = descend(uid, set())
        if hits:
            # Ties break by name so the result is stable across runs.
            counts = collections.Counter(hits)
            best = max(counts.items(), key=lambda t: (t[1], t[0]))[0]
            out[name] = best
    return out


# ------------------------------------------------------------------ building


def build():
    objects, lineage, models, sources, child_map = read_dbt()
    graph = json.loads(GRAPH.read_text(encoding="utf-8"))
    fps = json.loads(FINGERPRINTS.read_text(encoding="utf-8"))
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    content = json.loads(CONTENT.read_text(encoding="utf-8"))

    gnodes = sorted(graph["nodes"], key=lambda n: n["id"])
    gedges = graph["edges"]
    charted = [n["id"] for n in gnodes]

    domains = resolve_domains(charted, sources, models, child_map)

    rows_by_name = {}
    for rec in inventory:
        rows_by_name[rec["physical_name"].upper()] = rec.get("row_count") or 0
    for n in gnodes:
        rows_by_name.setdefault(n["id"], n.get("rows") or 0)

    blurb = {}
    for rec in content:
        fn = (rec.get("friendly_name") or "").upper()
        one = (rec.get("one_liner") or "").strip()
        if fn and one:
            blurb[fn] = one
        phys = rec["object_fqn"].split(".")[-1].upper()
        if one:
            blurb.setdefault(phys, one)

    # ---- tables: the 368 charted, with degree, keys, domain, rows
    degree = collections.Counter()
    for e in gedges:
        degree[e["a"]] += 1
        degree[e["b"]] += 1

    key_families = collections.defaultdict(set)
    for n in gnodes:
        fp = fps.get(n["id"]) or {}
        for k in fp.get("keys", []):
            if (k.get("populated_pct") or 0) > 0:
                key_families[n["id"]].add(k["key"])

    idx = {name: i for i, name in enumerate(charted)}
    tables = []
    for name in charted:
        gn = next(n for n in gnodes if n["id"] == name)
        tables.append({
            "n": name,
            "rows": rows_by_name.get(name, gn.get("rows") or 0),
            "deg": degree.get(name, 0),
            "keys": sorted(key_families.get(name, ())),
            "dom": domains.get(name, "UNFILED"),
            "desc": blurb.get(name, objects_desc(objects, name)),
        })

    tier_idx = {t: i for i, t in enumerate(LADDER)}
    edges = []
    for e in sorted(gedges, key=lambda e: (e["a"], e["b"], e["key"])):
        if e["a"] not in idx or e["b"] not in idx:
            continue
        edges.append([
            idx[e["a"]], idx[e["b"]],
            tier_idx.get(e["tier"], len(LADDER) - 1),
            e["key"],
            int(e.get("matched") or 0),
        ])

    # ---- stages: the functional infrastructure, with real counts
    stage_members = collections.defaultdict(list)
    for uid, o in objects.items():
        stage_members[o["stage"]].append(uid)
    stages = []
    for sid, label, role in STAGES:
        stages.append({
            "id": sid,
            "label": label,
            "role": role,
            "count": len(stage_members[sid]),
        })

    # ---- flow: stage-to-stage volume, the sequence in one line
    flow = collections.Counter()
    for a, b in lineage:
        flow[(objects[a]["stage"], objects[b]["stage"])] += 1
    flows = [
        {"from": a, "to": b, "n": n}
        for (a, b), n in sorted(flow.items(), key=lambda t: (-t[1], t[0]))
    ]

    # ---- convergence: where many sources become one thing. The machine's
    # actual brain, and it is small enough to name every part of.
    parents = collections.defaultdict(list)
    for a, b in lineage:
        parents[b].append(objects[a]["name"])
    convergence = []
    for uid, ps in parents.items():
        if len(ps) < 2:
            continue
        o = objects[uid]
        convergence.append({
            "name": o["name"],
            "stage": o["stage"],
            "schema": o["schema"],
            "feeds": sorted(ps),
            "desc": o["desc"].split("\n")[0][:260],
        })
    convergence.sort(key=lambda c: (-len(c["feeds"]), c["name"]))

    payload = {
        "meta": {
            "charted": len(tables),
            "joins": len(edges),
            "dbt_objects": len(objects),
            "lineage_edges": len(lineage),
            "fingerprinted": len(fps),
            "portal_parked": sum(1 for k in fps if k.startswith("PORTAL_")),
            "domains_resolved": len(domains),
            "connected_rows": sum(t["rows"] for t in tables if t["deg"] > 0),
        },
        "ladder": LADDER,
        "stages": stages,
        "flows": flows,
        "convergence": convergence[:24],
        "tables": tables,
        "edges": edges,
        "layouts": {
            "refinery": layout_refinery(objects, lineage),
            "constellation": layout_constellation(tables, edges),
            "stacks": layout_stacks(tables),
        },
    }
    return payload


def objects_desc(objects, name):
    for o in objects.values():
        if o["name"] == name and o["desc"]:
            return o["desc"].split("\n")[0][:260]
    return ""


# ------------------------------------------------------------------ layouts
#
# Each layout declares its own model box, sized to the aspect of the canvas it
# will land in. The renderer fits that box uniformly -- so nothing is ever
# stretched, and no layout wastes half the element on letterbox bars.

BOX_REFINERY = (1600, 800)
BOX_CONSTELLATION = (1600, 900)
BOX_STACKS = (1600, 900)


def layout_refinery(objects, lineage):
    """PARADIGM A -- sequence first. Five banks, left to right, in run order.

    Reads like a plant floor: material enters at the left and comes out the
    right as finished shelves. Within a bank, objects are packed into a grid
    of cells sorted by subject then name, so a table sits in the same cell
    every build. Lineage is drawn bank-to-bank.
    """
    order = [s[0] for s in STAGES]
    lanes = {sid: [] for sid in order}
    for uid, o in objects.items():
        lanes[o["stage"]].append(uid)
    for sid in lanes:
        lanes[sid].sort(key=lambda u: (objects[u]["schema"], objects[u]["name"]))

    BW, BH = BOX_REFINERY
    top_pad, bot_pad = 26.0, 26.0
    inner_h = BH - top_pad - bot_pad

    pos = {}
    bands = []
    band_w = BW / len(order)
    for si, sid in enumerate(order):
        members = lanes[sid]
        x0 = si * band_w
        inner_w = band_w * 0.80
        pad = (band_w - inner_w) / 2.0
        count = len(members)
        if count == 0:
            bands.append({"id": sid, "x": round(x0 + pad, 2), "w": round(inner_w, 2),
                          "cols": 0, "cell": 3.0})
            continue
        # Column count that keeps cells roughly square inside the band.
        cols = max(1, min(28, int(round(math.sqrt(count * inner_w / inner_h)))))
        rows = math.ceil(count / cols)
        cw = inner_w / cols
        ch = min(inner_h / rows, cw * 1.5)
        top = top_pad + (inner_h - ch * rows) / 2.0
        for i, uid in enumerate(members):
            c, r = i % cols, i // cols
            pos[uid] = [round(x0 + pad + c * cw + cw / 2, 2),
                        round(top + r * ch + ch / 2, 2)]
        # The renderer should not have to re-derive cell size from the grid.
        # Capped: BRIDGE holds 4 objects and THE DESK holds 3, and without a
        # ceiling those two banks render as a handful of enormous slabs that
        # read as "important" rather than "few".
        bands.append({"id": sid, "x": round(x0 + pad, 2), "w": round(inner_w, 2),
                      "cols": cols, "cell": round(min(min(cw, ch) * 0.62, 13.0), 2)})

    uids = sorted(pos)
    uidx = {u: i for i, u in enumerate(uids)}
    nodes = [{"id": objects[u]["name"], "s": objects[u]["stage"],
              "x": pos[u][0], "y": pos[u][1]} for u in uids]
    links = sorted({(uidx[a], uidx[b]) for a, b in lineage
                    if a in uidx and b in uidx})
    return {"box": [BW, BH], "bands": bands, "nodes": nodes,
            "links": [list(l) for l in links]}


def layout_constellation(tables, edges):
    """PARADIGM B -- identity first. Tables fall toward the IDs they carry.

    A table that carries only NPI sits inside the NPI well. A table carrying
    NPI and EIN sits in the gap between them -- and those in-between tables
    are the ones worth finding, because they are how a question crosses from
    one world to another. Position is meaning, not decoration.
    """
    BW, BH = BOX_CONSTELLATION
    cx, cy, rx, ry = BW / 2, BH / 2, BW * 0.355, BH * 0.345
    # A key carried by half the Library is not an identity, it's a column.
    # Only the discriminating keys get to pull a table off its home well --
    # otherwise NAME and ZIP drag everything into one blob in the middle,
    # which is precisely what makes an ordinary force layout useless here.
    UBIQUITOUS = 45

    fam = collections.Counter()
    for t in tables:
        for k in t["keys"]:
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
        mine = [k for k in t["keys"] if k in well_pos]
        h = key_of(t["n"])
        if mine:
            # A table belongs to its RAREST key, not to an average of its keys.
            # Averaging looks reasonable and is wrong: almost everything carries
            # NAME and ZIP, so every table drifts into the same crowded blob and
            # the specific wells empty out. The rarest ID is also the one that
            # actually says what a table is -- NPI means doctors, CCN means
            # facilities, NAME means nothing in particular.
            home = min(mine, key=lambda k: (fam[k], k))
            homed[home] += 1
            hx, hy = well_pos[home]
            # Extra keys pull it a little way toward each partner well, so the
            # tables sitting between two wells are exactly the tables that can
            # carry a question from one world into the other.
            others = [k for k in mine if k != home and fam[k] <= UBIQUITOUS]
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
            # w counts DISCRIMINATING keys only. A table carrying NAME and ZIP
            # is not a bridge between two worlds -- everything carries those.
            # Two rare IDs on one table is what actually lets a question cross.
            w = sum(1 for k in mine if fam[k] <= UBIQUITOUS)
        else:
            # No populated ID column at all. Not a verdict, just a fact: there
            # is nothing here to join on yet. Parked quietly at the rim.
            a = seeded(h) * 2 * math.pi
            x, y = cx + rx * 1.30 * math.cos(a), cy + ry * 1.26 * math.sin(a)
            w = 0
        nodes.append({"x": round(x, 2), "y": round(y, 2), "w": w,
                      "keyed": bool(mine)})
    return {
        "box": [BW, BH],
        # n = tables that CARRY this key anywhere; h = tables FILED here (this
        # was their rarest key). Labelling with n while drawing h is how a map
        # ends up saying 48 above a well with four dots under it.
        "wells": [{"k": k, "x": round(well_pos[k][0], 2),
                   "y": round(well_pos[k][1], 2),
                   "n": fam[k], "h": homed.get(k, 0)} for k in wells],
        "nodes": nodes,
    }


def layout_stacks(tables):
    """PARADIGM C -- place first. The Library as a floor plan you walk.

    Subject rooms sized by how much is filed in them; inside each room, one
    shelf cell per table sized by row count. Nothing moves between builds, so
    after a week you know where things live the way you know a real building.
    """
    by_dom = collections.defaultdict(list)
    for i, t in enumerate(tables):
        by_dom[t["dom"]].append(i)

    BW, BH = BOX_STACKS
    room_weights = [(d, len(v)) for d, v in by_dom.items()]
    rooms = squarify(room_weights, 6, 6, BW - 12, BH - 12)

    out_rooms, out_cells = [], []
    for dom, x, y, w, h in sorted(rooms, key=lambda r: r[0]):
        out_rooms.append({"d": dom, "x": round(x, 2), "y": round(y, 2),
                          "w": round(w, 2), "h": round(h, 2),
                          "n": len(by_dom[dom])})
        inner = (x + 3, y + 15, max(w - 6, 1), max(h - 18, 1))
        # Row counts span nine orders of magnitude; log-weight the shelves or a
        # single 300M-row table eats the whole room.
        items = [(i, math.log10(max(tables[i]["rows"], 1)) + 1) for i in by_dom[dom]]
        for i, cx, cy, cw, ch in squarify(items, *inner):
            out_cells.append({"i": i, "x": round(cx, 2), "y": round(cy, 2),
                              "w": round(cw, 2), "h": round(ch, 2)})
    out_cells.sort(key=lambda c: c["i"])
    return {"box": [BW, BH], "rooms": out_rooms, "cells": out_cells}


# -------------------------------------------------------------------- output


def inline(payload):
    if not HTML.exists():
        raise SystemExit(f"missing {HTML} -- write the page first")
    src = HTML.read_text(encoding="utf-8")
    i, j = src.find(START), src.find(END)
    if i < 0 or j < 0:
        raise SystemExit(f"missing {START}/{END} markers in {HTML}")
    blob = json.dumps(payload, separators=(",", ":"), sort_keys=True)
    out = src[: i + len(START)] + "\nconst ANATOMY=" + blob + ";\n" + src[j:]
    HTML.write_text(out, encoding="utf-8")
    return len(blob)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inline", action="store_true",
                    help="also inject the payload into docs/library-anatomy.html")
    args = ap.parse_args()

    payload = build()
    OUT.write_text(json.dumps(payload, indent=1, sort_keys=True), encoding="utf-8")
    m = payload["meta"]
    print(f"anatomy.json  {OUT.stat().st_size/1024:.0f} KB")
    print(f"  charted tables   {m['charted']}")
    print(f"  verified joins   {m['joins']}")
    print(f"  dbt objects      {m['dbt_objects']}  ({m['lineage_edges']} lineage edges)")
    print(f"  domains resolved {m['domains_resolved']}/{m['charted']}")
    if args.inline:
        n = inline(payload)
        print(f"  inlined {n/1024:.0f} KB into {HTML.name}")


if __name__ == "__main__":
    main()
