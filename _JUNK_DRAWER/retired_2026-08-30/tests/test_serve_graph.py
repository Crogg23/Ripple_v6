"""Tests for serve/serve_graph.py's build_figure() -- pure computation over an
in-memory graph dict (no Snowflake, no real Streamlit rendering needed; only
st.warning is called on specific branches, captured via monkeypatch).
2026-07-31: serve/ had zero test coverage; this locks in the two bugs fixed
earlier this session (the tier-deselection revert-to-default bug, and the
silent full-graph fallback on a stale focus) so they can never silently
regress.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "serve"))

import serve_graph as G  # noqa: E402


def _tiny_graph():
    """Two connected nodes (A, B) both with baked x/y, one isolated node (C)
    with no x/y, and one STEEL edge between A and B."""
    return {
        "nodes": [
            {"id": "SRC_A", "x": 0.0, "y": 0.0, "domain": "health"},
            {"id": "SRC_B", "x": 1.0, "y": 1.0, "domain": "health"},
            {"id": "SRC_C", "domain": "other"},  # isolated -- no x/y
        ],
        "edges": [
            {"a": "SRC_A", "b": "SRC_B", "tier": "STEEL"},
        ],
    }


# --------------------------------------------------------------------------- #
# tier selection -- None means "use the default", [] means "show nothing"
# --------------------------------------------------------------------------- #
def test_tiers_none_uses_default_tiers():
    fig = G.build_figure(_tiny_graph(), tiers=None, include_samples=True)
    edge_traces = [t for t in fig.data if t.mode == "lines"]
    assert len(edge_traces) == 1  # the STEEL edge is in DEFAULT_TIERS


def test_tiers_empty_list_shows_no_edges_not_the_default(monkeypatch):
    """2026-07-30 fix: `set(tiers) & set(ALL_TIERS) or set(DEFAULT_TIERS)` used
    to treat an explicit empty selection as falsy and silently revert to the
    default tiers. A user who deselects every tier checkbox must actually see
    zero edges, not the STEEL/STRONG/BRIDGE default."""
    fig = G.build_figure(_tiny_graph(), tiers=[], include_samples=True)
    edge_traces = [t for t in fig.data if t.mode == "lines"]
    assert len(edge_traces) == 0


def test_tiers_filters_to_only_the_requested_tier():
    graph = _tiny_graph()
    graph["edges"].append({"a": "SRC_A", "b": "SRC_B", "tier": "GEO"})
    fig = G.build_figure(graph, tiers=["GEO"], include_samples=True)
    edge_traces = [t for t in fig.data if t.mode == "lines"]
    assert len(edge_traces) == 1
    assert edge_traces[0].name.startswith("GEO")


def test_unknown_tier_names_are_silently_dropped_not_erroring():
    fig = G.build_figure(_tiny_graph(), tiers=["STEEL", "NOT_A_REAL_TIER"], include_samples=True)
    edge_traces = [t for t in fig.data if t.mode == "lines"]
    assert len(edge_traces) == 1


# --------------------------------------------------------------------------- #
# focus resolution -- the dossier "jump to graph" ego-view
# --------------------------------------------------------------------------- #
def test_focus_on_a_real_node_builds_an_ego_view():
    fig = G.build_figure(_tiny_graph(), tiers=None, include_samples=True, focus=["SRC_A"])
    assert "neighborhood" in fig.layout.title.text
    assert "1 source(s)" in fig.layout.title.text


def test_focus_resolving_to_nothing_falls_back_to_full_graph_and_warns(monkeypatch):
    """2026-07-30 fix: if none of the requested focus ids are in the cached
    graph (a stale connect_graph.json snapshot), build_figure used to silently
    render the full unfiltered graph with no signal to the caller. It must now
    warn."""
    warnings = []
    monkeypatch.setattr(G.st, "warning", lambda msg: warnings.append(msg))

    fig = G.build_figure(_tiny_graph(), tiers=None, include_samples=True,
                         focus=["SRC_NOT_IN_GRAPH"])
    assert len(warnings) == 1
    assert "cached graph" in warnings[0]
    assert "Connection graph" == fig.layout.title.text.split("<br>")[0]  # full-graph title, not ego


def test_focus_none_is_the_full_graph_with_no_warning(monkeypatch):
    warnings = []
    monkeypatch.setattr(G.st, "warning", lambda msg: warnings.append(msg))
    fig = G.build_figure(_tiny_graph(), tiers=None, include_samples=True, focus=None)
    assert warnings == []
    assert fig.layout.title.text.split("<br>")[0] == "Connection graph"


# --------------------------------------------------------------------------- #
# isolated nodes -- gutter placement, no fabricated coordinates
# --------------------------------------------------------------------------- #
def test_isolated_node_with_no_baked_xy_is_gutter_placed_not_dropped(monkeypatch):
    monkeypatch.setattr(G.st, "warning", lambda msg: None)
    fig = G.build_figure(_tiny_graph(), tiers=None, include_samples=True)
    node_traces = [t for t in fig.data if t.mode == "markers"]
    all_ids = set()
    for t in node_traces:
        all_ids.update(t.customdata)
    assert "SRC_C" in all_ids  # isolated node still shows up, in the gutter


# --------------------------------------------------------------------------- #
# _domain_color -- stable across process restarts (not Python's salted hash())
# --------------------------------------------------------------------------- #
def test_domain_color_is_deterministic():
    assert G._domain_color("health") == G._domain_color("health")


def test_domain_color_falls_back_for_empty_domain():
    assert G._domain_color("") == G._domain_color(None)
