"""Cache the spring layout onto outputs/connect_graph.json (ADDITIVE x/y).

The connection graph has 638 connected nodes and 20,696 edges, but no cached
positions. Every viz that wants to draw it re-runs the O(n^2) force-directed
layout from scratch — that's the 17MB / slow-render problem in
connection_explorer.html. This computes the layout ONCE and writes an ``x``/``y``
onto each connected node (purely additive — no node/edge/field is dropped), so any
downstream renderer can read the cached coordinates instead of recomputing.

Isolated nodes (82 of them, e.g. FED_NOAA_AIS) get NO position — they aren't in
the spring layout's connected set, and a fabricated coordinate would lie about
where they sit. Renderers must handle them explicitly (see leads_overlay.py).

Idempotent: running twice produces the same coordinates (the layout is seeded).
After writing, the file is re-loaded and node/edge counts are asserted unchanged.

Run:  python -m connect.cache_layout
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from .discover import GRAPH_OUT
from .explore import _spring_layout


def cache_layout(path: Path | None = None) -> Path:
    path = path or GRAPH_OUT
    graph = json.loads(path.read_text())

    nodes = graph["nodes"]
    edges = graph["edges"]
    n_nodes_before, n_edges_before = len(nodes), len(edges)

    connected = sorted({e["a"] for e in edges} | {e["b"] for e in edges})

    # Same weighting the explorer uses: stronger overlaps pull harder.
    max_m = max((e["matched"] for e in edges), default=1)
    elist = [(e["a"], e["b"], math.log1p(e["matched"]) / math.log1p(max_m)) for e in edges]

    pos = _spring_layout(connected, elist)

    positioned = 0
    for nd in nodes:
        p = pos.get(nd["id"])
        if p is not None:
            nd["x"], nd["y"] = float(p[0]), float(p[1])
            positioned += 1
        else:
            # Isolated node: leave x/y absent so renderers can spot it and decide.
            nd.pop("x", None)
            nd.pop("y", None)

    graph.setdefault("meta", {})["layout"] = {
        "engine": "explore._spring_layout",
        "connected_positioned": positioned,
        "isolated": n_nodes_before - positioned,
    }

    path.write_text(json.dumps(graph), encoding="utf-8")

    # Re-load and assert the additive write changed nothing structural.
    reloaded = json.loads(path.read_text())
    assert len(reloaded["nodes"]) == n_nodes_before, "node count changed!"
    assert len(reloaded["edges"]) == n_edges_before, "edge count changed!"
    assert sum(1 for nd in reloaded["nodes"] if "x" in nd) == positioned, "position count drift!"

    print(f"cached layout: {positioned} connected nodes positioned, "
          f"{n_nodes_before - positioned} isolated left unpositioned")
    print(f"nodes={len(reloaded['nodes'])} edges={len(reloaded['edges'])} (unchanged)")
    print(f"wrote {path}")
    return path


if __name__ == "__main__":
    cache_layout()
