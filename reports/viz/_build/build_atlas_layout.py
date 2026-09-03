"""Layout v2 for the Atlas — geography means something now.

Continents are domains. Each table is assigned one of seven super-domains
from the registry's DOMAIN_PRIMARY; tables without a card inherit the
majority domain of their name prefix (FED_CMS_* follows its carded
siblings); the rest land in UNCHARTED. Inside a region, tables joined by
paved roads get a spring layout; loners sit in a calm grid below them.
Regions are shelf-packed into a wide map.

Frozen world rule unchanged: atlas_coords.json pins every known table.
Delete it to re-lay the world (a deliberate act).

Run after build_atlas_data.py:
    python reports/viz/_build/build_atlas_layout.py
"""

from __future__ import annotations

import json
import math
import random
from pathlib import Path

BUILD = Path(__file__).resolve().parent
DATA = BUILD / "atlas_data.json"
COORDS = BUILD / "atlas_coords.json"

SPRING_ITERS = 250
MIN_SEP = 190.0
CELL_W, CELL_H = 250.0, 150.0   # loner grid cell
PAD = 260.0                     # region padding

SUPER = {
    "health_medicine": "HEALTH",
    "money_in_politics": "MONEY & POLITICS",
    "spending_budget": "MONEY & POLITICS",
    "money_finance": "FINANCE & CORPORATES",
    "corporate_entities": "FINANCE & CORPORATES",
    "economy_labor_trade": "FINANCE & CORPORATES",
    "justice_courts": "JUSTICE & ENFORCEMENT",
    "sanctions_enforcement": "JUSTICE & ENFORCEMENT",
    "crime_security": "JUSTICE & ENFORCEMENT",
    "immigration_migration": "JUSTICE & ENFORCEMENT",
    "government_power": "GOVERNMENT",
    "open_data_portal": "GOVERNMENT",
    "energy_environment": "ENVIRONMENT & ENERGY",
    "transport_movement": "ENVIRONMENT & ENERGY",
    "geo_demographics": "ENVIRONMENT & ENERGY",
    "housing_social": "SOCIETY & RESEARCH",
    "science_research": "SOCIETY & RESEARCH",
}
UNCHARTED = "UNCHARTED"
# fixed hue order — validated against the dark surface, do not reshuffle
REGION_ORDER = [
    "HEALTH", "MONEY & POLITICS", "FINANCE & CORPORATES",
    "JUSTICE & ENFORCEMENT", "GOVERNMENT", "ENVIRONMENT & ENERGY",
    "SOCIETY & RESEARCH", UNCHARTED,
]


def assign_domains(nodes):
    """Carded domain -> super-domain; else prefix majority; else UNCHARTED."""
    for n in nodes:
        n["region"] = SUPER.get(n.get("domain"))
    prefix_votes: dict[str, dict[str, int]] = {}
    for n in nodes:
        if n["region"]:
            pfx = "_".join(n["name"].split("_")[:2])
            prefix_votes.setdefault(pfx, {})
            prefix_votes[pfx][n["region"]] = prefix_votes[pfx].get(n["region"], 0) + 1
    inferred = 0
    for n in nodes:
        if not n["region"]:
            pfx = "_".join(n["name"].split("_")[:2])
            votes = prefix_votes.get(pfx)
            if votes:
                n["region"] = max(votes, key=votes.get)
                inferred += 1
            else:
                n["region"] = UNCHARTED
    return inferred


def components(names, edges):
    parent = {n: n for n in names}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    comps: dict[str, list[str]] = {}
    for n in names:
        comps.setdefault(find(n), []).append(n)
    return sorted(comps.values(), key=len, reverse=True)


def spring(names, edges, iters=SPRING_ITERS):
    rnd = random.Random(42)
    n = len(names)
    if n == 1:
        return {names[0]: (0.0, 0.0)}
    r = math.sqrt(n) * 180
    pos = {
        m: (r * math.cos(2 * math.pi * i / n) + rnd.uniform(-9, 9),
            r * math.sin(2 * math.pi * i / n) + rnd.uniform(-9, 9))
        for i, m in enumerate(names)
    }
    k = 280.0
    idx = set(names)
    es = [(a, b) for a, b in edges if a in idx and b in idx]
    for it in range(iters):
        temp = 30 * (1 - it / iters) + 1
        disp = {m: [0.0, 0.0] for m in names}
        for i, a in enumerate(names):
            ax, ay = pos[a]
            for b in names[i + 1:]:
                bx, by = pos[b]
                dx, dy = ax - bx, ay - by
                d2 = dx * dx + dy * dy + 0.01
                f = k * k / d2
                disp[a][0] += dx * f; disp[a][1] += dy * f
                disp[b][0] -= dx * f; disp[b][1] -= dy * f
        for a, b in es:
            ax, ay = pos[a]; bx, by = pos[b]
            dx, dy = ax - bx, ay - by
            d = math.sqrt(dx * dx + dy * dy) + 0.01
            if d <= k:
                continue
            f = (d - k) / k
            disp[a][0] -= dx / d * f * d; disp[a][1] -= dy / d * f * d
            disp[b][0] += dx / d * f * d; disp[b][1] += dy / d * f * d
        for m in names:
            dx, dy = disp[m]
            d = math.sqrt(dx * dx + dy * dy) + 0.01
            step = min(d, temp)
            x, y = pos[m]
            pos[m] = (x + dx / d * step, y + dy / d * step)
    # separation sweeps
    for _ in range(40):
        clean = True
        for i, a in enumerate(names):
            ax, ay = pos[a]
            for b in names[i + 1:]:
                bx, by = pos[b]
                dx, dy = ax - bx, ay - by
                d = math.sqrt(dx * dx + dy * dy) + 0.01
                if d < MIN_SEP:
                    clean = False
                    push = (MIN_SEP - d) / 2
                    ux, uy = dx / d, dy / d
                    pos[a] = (pos[a][0] + ux * push, pos[a][1] + uy * push)
                    pos[b] = (pos[b][0] - ux * push, pos[b][1] - uy * push)
                    ax, ay = pos[a]
        if clean:
            break
    xs = [p[0] for p in pos.values()]; ys = [p[1] for p in pos.values()]
    x0, y0 = min(xs), min(ys)
    return {m: (x - x0, y - y0) for m, (x, y) in pos.items()}


def region_layout(members, paved_pairs):
    """Each join family lays out alone and tight; families and loners tile
    the region like city blocks. No cross-family repulsion, no dead air."""
    mset = set(members)
    local = [(a, b) for a, b in paved_pairs if a in mset and b in mset]
    fams = [c for c in components(members, local) if len(c) > 1]
    lone = sorted(m for c in components(members, local) if len(c) == 1 for m in c)

    blocks = []  # (w, h, {name: (x, y)})
    for fam in sorted(fams, key=len, reverse=True):
        sp = spring(fam, local)
        bw = max(p[0] for p in sp.values()) + CELL_W
        bh = max(p[1] for p in sp.values()) + CELL_H
        blocks.append((bw, bh, sp))
    if lone:
        cols = max(3, math.ceil(math.sqrt(len(lone) * 0.9)))
        grid = {m: ((i % cols) * CELL_W + CELL_W / 2, (i // cols) * CELL_H)
                for i, m in enumerate(lone)}
        blocks.append((cols * CELL_W, math.ceil(len(lone) / cols) * CELL_H, grid))

    # shelf-pack the blocks inside the region
    total_area = sum(bw * bh for bw, bh, _ in blocks)
    target_w = max(math.sqrt(total_area * 1.7), max(bw for bw, _, _ in blocks))
    pos = {}
    x = y = row_h = 0.0
    w = 0.0
    for bw, bh, bp in blocks:
        if x > 0 and x + bw > target_w:
            x = 0.0
            y += row_h + CELL_H * 0.7
            row_h = 0.0
        for m, (mx, my) in bp.items():
            pos[m] = (mx + x, my + y)
        x += bw + CELL_W * 0.6
        w = max(w, x)
        row_h = max(row_h, bh)
    h = y + row_h
    return pos, (w + PAD, h + PAD)


def shelf_pack(sizes):
    """Pack region boxes into rows aiming at a wide-screen map. Returns origins."""
    order = sorted(range(len(sizes)), key=lambda i: -sizes[i][1])
    total_area = sum(w * h for w, h in sizes)
    target_w = math.sqrt(total_area * 1.9)
    origins = [None] * len(sizes)
    x = y = row_h = 0.0
    for i in order:
        w, h = sizes[i]
        if x > 0 and x + w > target_w:
            x = 0.0
            y += row_h + PAD
            row_h = 0.0
        origins[i] = (x, y)
        x += w + PAD
        row_h = max(row_h, h)
    return origins


def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    nodes = data["nodes"]
    names = {n["name"] for n in nodes}
    inferred = assign_domains(nodes)
    paved_pairs = [(e["a"], e["b"]) for e in data["paved"]]

    frozen = json.loads(COORDS.read_text(encoding="utf-8")) if COORDS.exists() else {}
    coords: dict[str, tuple[float, float]] = {}
    regions = []

    if not frozen:
        groups = {r: [n["name"] for n in nodes if n["region"] == r] for r in REGION_ORDER}
        groups = {r: g for r, g in groups.items() if g}
        layouts, sizes, keys = [], [], []
        for r, members in groups.items():
            pos, size = region_layout(members, paved_pairs)
            layouts.append(pos); sizes.append(size); keys.append(r)
        origins = shelf_pack(sizes)
        for r, pos, (w, h), (ox, oy) in zip(keys, layouts, sizes, origins):
            for m, (x, y) in pos.items():
                coords[m] = (round(x + ox + PAD / 2, 1), round(y + oy + PAD / 2, 1))
            regions.append({
                "name": r, "slot": REGION_ORDER.index(r),
                "x": ox, "y": oy, "w": w, "h": h,
                "count": len(pos),
            })
    else:
        coords = {m: tuple(xy) for m, xy in frozen.items() if m in names}
        regions = data.get("regions", [])
        if not regions:
            # data file was rebuilt and lost the boxes: recompute from coords
            by_r: dict[str, list[tuple[float, float]]] = {}
            node_region = {n["name"]: n["region"] for n in nodes}
            for m, xy in coords.items():
                by_r.setdefault(node_region[m], []).append(xy)
            for r in REGION_ORDER:
                pts = by_r.get(r)
                if not pts:
                    continue
                xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
                regions.append({
                    "name": r, "slot": REGION_ORDER.index(r),
                    "x": min(xs) - PAD / 2, "y": min(ys) - PAD / 2,
                    "w": max(xs) - min(xs) + PAD, "h": max(ys) - min(ys) + PAD,
                    "count": len(pts),
                })
        rnd = random.Random(7)
        neighbors: dict[str, list[str]] = {}
        for a, b in paved_pairs:
            neighbors.setdefault(a, []).append(b)
            neighbors.setdefault(b, []).append(a)
        pending = [m for m in names if m not in coords]
        for _ in range(3):
            still = []
            for m in pending:
                anchors = [coords[x] for x in neighbors.get(m, []) if x in coords]
                if anchors:
                    ax = sum(p[0] for p in anchors) / len(anchors)
                    ay = sum(p[1] for p in anchors) / len(anchors)
                    coords[m] = (round(ax + rnd.uniform(-150, 150), 1),
                                 round(ay + rnd.uniform(-150, 150), 1))
                else:
                    still.append(m)
            pending = still
        if pending:  # no wired anchor: park at the bottom of their region, or the map
            by_region = {r["name"]: r for r in regions}
            node_region = {n["name"]: n["region"] for n in nodes}
            for i, m in enumerate(sorted(pending)):
                r = by_region.get(node_region.get(m))
                if r:
                    coords[m] = (round(r["x"] + PAD + (i % 5) * CELL_W, 1),
                                 round(r["y"] + r["h"] + CELL_H, 1))
                else:
                    coords[m] = (round((i % 8) * CELL_W, 1),
                                 round(max(y for _, y in coords.values()) + 2 * CELL_H, 1))

    for n in nodes:
        n["x"], n["y"] = coords[n["name"]]
    data["regions"] = regions
    DATA.write_text(json.dumps(data, indent=1), encoding="utf-8")
    COORDS.write_text(json.dumps({m: list(xy) for m, xy in sorted(coords.items())}),
                      encoding="utf-8")
    counts = {r["name"]: r["count"] for r in regions}
    print(f"regions {counts}  inferred-domain {inferred}  placed {len(coords)}")


if __name__ == "__main__":
    main()
