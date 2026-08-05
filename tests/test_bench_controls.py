"""
Tests for bench/controls.py - the knob -> Dash control layer.

Run it either way:

    python -m pytest tests/test_bench_controls.py -q
    python bench/controls.py            # same checks, with a printed report

The fixtures are NOT invented. Every Knob below is built by reading a real
Plotly validator off this install, so if plotly 6.9.0 ever disagrees with
SPEC 4.1's table, this test is where it shows up.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import plotly.graph_objects as go

from bench import controls
from bench.controls import Knob

DF_COLUMNS = ["STATE", "TOTAL", "AGENCY", "FILED_ON"]


# ---------------------------------------------------------------- fixtures


def _bounds(v):
    """min/max off a real validator, or (None, None). NumberValidator calls
    them min_val/max_val, which is the sort of thing you only learn by looking."""
    if getattr(v, "has_min_max", False):
        return v.min_val, v.max_val
    return None, None


def from_validator(path: str, obj, prop: str, control: str, **over) -> Knob:
    """Build a Knob out of a live Plotly validator. No guessed property names."""
    v = obj._get_validator(prop)
    lo, hi = _bounds(v)
    kw = dict(
        path=path,
        label=prop,
        control=control,
        options=tuple(getattr(v, "values", ()) or ()) if control in ("dropdown",)
        else tuple(getattr(v, "flags", ()) or ()) if control == "multi"
        else (),
        extras=tuple(getattr(v, "extras", ()) or ()) if control == "multi" else (),
        min=lo, max=hi,
        default=getattr(obj, prop, None),
        description=f"{prop} on {type(obj).__name__} ({type(v).__name__})",
        depth=path.count(".") ,
    )
    kw.update(over)
    return Knob(**kw)


def fixtures() -> dict[str, Knob]:
    """One knob per control type in SPEC 4.1, each off a real validator."""
    bar, lay, ax = go.Bar(), go.Layout(), go.layout.XAxis()
    return {
        # EnumeratedValidator -> dropdown          ['v', 'h']
        "dropdown": from_validator("trace.orientation", bar, "orientation", "dropdown"),
        # BooleanValidator -> toggle
        "toggle": from_validator("trace.cliponaxis", bar, "cliponaxis", "toggle"),
        # ColorValidator -> picker + hex box
        "color": from_validator("layout.paper_bgcolor", lay, "paper_bgcolor", "color",
                                default="#0d1117"),
        # NumberValidator with both bounds -> slider   (opacity is 0..1)
        "slider": from_validator("trace.opacity", bar, "opacity", "slider", default=1.0),
        # NumberValidator with an infinite top -> number box (layout.width is 10..inf)
        "number": from_validator("layout.width", lay, "width", "slider"),
        # IntegerValidator -> number box, step 1
        "integer": from_validator("layout.xaxis.nticks", ax, "nticks", "number", step=1),
        # AngleValidator -> number box, -180..180
        "angle": from_validator("trace.textangle", bar, "textangle", "number",
                                min=-180, max=180),
        # StringValidator -> text box
        "text": from_validator("trace.name", bar, "name", "text"),
        # AnyValidator -> text box (last resort)
        "any": from_validator("layout.uirevision", lay, "uirevision", "text"),
        # FlaglistValidator -> multi-select        flags + extras
        "multi": from_validator("trace.hoverinfo", bar, "hoverinfo", "multi"),
        # CompoundValidator -> expandable sub-section
        "section": from_validator("trace.marker", bar, "marker", "section",
                                  default=None),
        # DataArrayValidator -> dropdown of the df's columns
        "column": from_validator("trace.x", bar, "x", "column",
                                 options=tuple(DF_COLUMNS)),
    }


def fake_tree() -> dict:
    """Six buckets, three tiers, with a real section+children in MARK."""
    bar, lay, ax = go.Bar(), go.Layout(), go.layout.XAxis()
    f = fixtures()
    return {
        "DATA": {
            0: [f["column"],
                from_validator("trace.y", bar, "y", "column",
                               options=tuple(DF_COLUMNS)),
                from_validator("trace.text", bar, "text", "column",
                               options=tuple(DF_COLUMNS))],
            1: [], 2: [],
        },
        "MARK": {
            0: [f["dropdown"], f["slider"]],
            1: [f["section"],
                from_validator("trace.marker.color", bar.marker, "color", "color"),
                from_validator("trace.marker.opacity", bar.marker, "opacity",
                               "slider"),
                f["toggle"]],
            2: [from_validator("trace.marker.line.width", bar.marker.line, "width",
                               "slider")],
        },
        "SCALE": {
            0: [from_validator("layout.xaxis.categoryorder", ax, "categoryorder",
                               "dropdown"),
                from_validator("layout.xaxis.type", ax, "type", "dropdown")],
            1: [from_validator("layout.xaxis.tickformat", ax, "tickformat", "text")],
            2: [from_validator("layout.xaxis.minor.dtick", go.layout.xaxis.Minor(),
                               "dtick", "text")],
        },
        "FRAME": {
            0: [f["color"], f["number"],
                from_validator("layout.showlegend", lay, "showlegend", "toggle")],
            1: [from_validator("layout.margin", lay, "margin", "section"),
                from_validator("layout.margin.l", go.layout.Margin(), "l", "number")],
            2: [f["integer"]],
        },
        "INTERACTION": {
            0: [from_validator("layout.hovermode", lay, "hovermode", "dropdown")],
            1: [from_validator("layout.dragmode", lay, "dragmode", "dropdown"),
                f["multi"]],
            2: [],
        },
        "MOTION": {
            0: [from_validator("layout.transition.duration",
                               go.layout.Transition(), "duration", "number")],
            1: [from_validator("layout.transition.easing",
                               go.layout.Transition(), "easing", "dropdown")],
            2: [],
        },
    }


# ---------------------------------------------------------------- walkers


def walk(comp):
    """Every Dash component in a subtree, root first."""
    yield comp
    kids = getattr(comp, "children", None)
    if kids is None:
        return
    if not isinstance(kids, (list, tuple)):
        kids = [kids]
    for k in kids:
        if hasattr(k, "_prop_names") or hasattr(k, "children"):
            yield from walk(k)


def ids_in(comp) -> list[dict]:
    out = []
    for c in walk(comp):
        cid = getattr(c, "id", None)
        if isinstance(cid, dict):
            out.append(cid)
    return out


def parts_for(comp, path: str) -> list[str]:
    return [i["part"] for i in ids_in(comp)
            if i.get("bench") == "knob" and i.get("path") == path]


# ---------------------------------------------------------------- tests


def test_every_control_type_builds_and_carries_its_id():
    for name, knob in fixtures().items():
        comp = controls.control(knob, None)
        assert comp is not None, name
        got = parts_for(comp, knob.path)
        if controls.kind(knob) == "section":
            assert "body" in got, f"{name}: section needs a body div"
            assert "value" not in got, f"{name}: a section is not a setting"
        else:
            assert got.count("value") == 1, f"{name}: want exactly one value id, got {got}"
            assert "row" in got, f"{name}: every row needs a styling target"


def test_colour_always_renders_both_picker_and_hex():
    knob = fixtures()["color"]
    got = parts_for(controls.control(knob, "#ff0000"), knob.path)
    assert "value" in got and "hex" in got, got


def test_default_is_grey_and_changed_is_lit():
    knob = fixtures()["slider"]                  # trace.opacity, default 1.0
    grey = controls.control(knob, None)
    lit = controls.control(knob, 0.4)
    assert not controls.is_changed(knob, None)
    assert not controls.is_changed(knob, 1.0)    # same as default -> still grey
    assert controls.is_changed(knob, 0.4)
    assert grey.style["borderLeft"] == "2px solid transparent"
    assert lit.style["borderLeft"] == f"2px solid {controls.ACCENT}"
    assert lit.style["background"] == controls.PANEL_2


def test_unbounded_number_degrades_from_slider_to_box():
    # layout.width really is min=10, max=inf on plotly 6.9.0.
    knob = fixtures()["number"]
    assert knob.control == "slider"
    assert math.isinf(float(knob.max))
    assert controls.kind(knob) == "number"


def test_coerce_round_trips_the_awkward_widgets():
    f = fixtures()
    assert controls.coerce(f["toggle"], True) is True
    assert controls.coerce(f["multi"], ["x", "y", "text"]) == "x+y+text"
    assert controls.coerce(f["multi"], ["all", "x"]) == "all"      # extras win
    assert controls.coerce(f["multi"], []) is None
    assert controls.coerce(f["text"], "  ") is None
    assert controls.coerce(f["text"], "sales") == "sales"
    assert controls.coerce(f["column"], None) is None


def test_hex_normaliser():
    assert controls._as_hex("#abc") == "#aabbcc"
    assert controls._as_hex("#0d1117") == "#0d1117"
    assert controls._as_hex("rgba(13,17,23,0.5)") == "#0d1117"
    assert controls._as_hex("white") == "#ffffff"
    assert controls._as_hex("not a colour") is None


def test_panel_has_six_buckets_in_atlas_order_with_data_open():
    p = controls.panel(fake_tree(), {"trace.opacity": 0.4})
    sections = [c for c in walk(p)
                if isinstance(getattr(c, "id", None), dict)
                and c.id.get("bench") == "bucket" and c.id.get("part") == "section"]
    names = [s.id["bucket"] for s in sections]
    assert names == list(controls.BUCKET_ORDER), names
    opens = {s.id["bucket"]: bool(s.open) for s in sections}
    assert opens["DATA"] is True
    assert not any(v for k, v in opens.items() if k != "DATA"), opens


def test_search_cuts_every_tier():
    tree = fake_tree()
    # 'minor.dtick' only exists in SCALE tier 2 - if search finds it, search
    # is genuinely reaching past the tiers.
    p = controls.panel(tree, {}, query="minor")
    found = [i["path"] for i in ids_in(p)
             if i.get("bench") == "knob" and i.get("part") == "row"]
    assert found == ["layout.xaxis.minor.dtick"], found
    # and every surviving bucket opens itself
    sections = [c for c in walk(p)
                if isinstance(getattr(c, "id", None), dict)
                and c.id.get("bench") == "bucket" and c.id.get("part") == "section"]
    assert [s.id["bucket"] for s in sections] == ["SCALE"]
    assert all(s.open for s in sections)


def test_section_nests_its_children():
    """trace.marker.color and trace.marker.opacity must land INSIDE trace.marker."""
    tree = fake_tree()
    p = controls.panel(tree, {})
    body = None
    for c in walk(p):
        cid = getattr(c, "id", None)
        if isinstance(cid, dict) and cid.get("path") == "trace.marker" \
                and cid.get("part") == "body":
            body = c
    assert body is not None, "no body div for the trace.marker section"
    inside = [i["path"] for i in ids_in(body)
              if i.get("bench") == "knob" and i.get("part") == "row"]
    assert "trace.marker.color" in inside and "trace.marker.opacity" in inside, inside
    assert "trace.cliponaxis" not in inside, "a non-child leaked into the section"


def test_mapping_feeds_the_column_knobs():
    p = controls.panel(fake_tree(), {}, mapping={"x": "STATE", "y": "TOTAL"})
    rows = {}
    for c in walk(p):
        cid = getattr(c, "id", None)
        if isinstance(cid, dict) and cid.get("part") == "row":
            rows[cid["path"]] = c
    assert rows["trace.x"].style["borderLeft"] == f"2px solid {controls.ACCENT}"
    assert rows["trace.text"].style["borderLeft"] == "2px solid transparent"


def test_every_knob_id_is_a_dict_pattern_id():
    p = controls.panel(fake_tree(), {"trace.opacity": 0.4})
    for c in walk(p):
        cid = getattr(c, "id", None)
        if cid is None:
            continue
        assert isinstance(cid, dict), f"string id found: {cid!r}"
        assert cid.get("bench") in ("knob", "bucket", "panel"), cid


def test_panel_survives_a_real_dash_app():
    """Dash's own layout validation, no duplicate ids, and it serialises.

    Building components that *construct* is not the same as building
    components Dash will accept. This is the check that says it will.
    """
    import json

    from dash import Dash, dcc, html
    from dash import _validate
    from plotly.utils import PlotlyJSONEncoder

    app = Dash(__name__)
    app.layout = html.Div([dcc.Store(id="spec"),
                           controls.panel(fake_tree(), {"trace.opacity": 0.4})])
    _validate.validate_layout(app.layout, app.layout)

    seen: dict[str, int] = {}
    for c in walk(app.layout):
        cid = getattr(c, "id", None)
        if cid is None:
            continue
        key = json.dumps(cid, sort_keys=True) if isinstance(cid, dict) else str(cid)
        seen[key] = seen.get(key, 0) + 1
    dupes = {k: n for k, n in seen.items() if n > 1}
    assert not dupes, f"duplicate ids would break Dash: {dupes}"

    json.dumps(app.layout.to_plotly_json(), cls=PlotlyJSONEncoder)


def test_one_all_callback_catches_every_editor():
    """The whole reason for the dict ids: 2,488 knobs, one callback."""
    from dash import ALL, Dash, Input, Output, State, dcc, html

    app = Dash(__name__)
    app.layout = html.Div([dcc.Store(id="spec"),
                           controls.panel(fake_tree(), {})])

    @app.callback(Output("spec", "data"),
                  Input({"bench": "knob", "path": ALL, "part": ALL}, "value"),
                  State("spec", "data"), prevent_initial_call=True)
    def _knob_changed(values, spec):        # pragma: no cover - never run here
        return spec

    assert len(app.callback_map) == 1


def test_expanded_builds_only_the_buckets_you_name():
    """The payload lever. All six headers still draw; only DATA's rows exist."""
    tree = fake_tree()
    full = controls.panel(tree, {})
    lean = controls.panel(tree, {}, expanded=("DATA",))

    def rows(p):
        return [i["path"] for i in ids_in(p)
                if i.get("bench") == "knob" and i.get("part") == "row"]

    def sections(p):
        return [c.id["bucket"] for c in walk(p)
                if isinstance(getattr(c, "id", None), dict)
                and c.id.get("part") == "section"]

    assert sections(lean) == sections(full) == list(controls.BUCKET_ORDER)
    assert set(rows(lean)) == {"trace.x", "trace.y", "trace.text"}
    assert len(rows(full)) > len(rows(lean))
    assert sum(1 for _ in walk(lean)) < sum(1 for _ in walk(full))


def test_search_ignores_expanded():
    """A search that can't reach a collapsed bucket is not a search."""
    p = controls.panel(fake_tree(), {}, query="minor", expanded=("DATA",))
    found = [i["path"] for i in ids_in(p)
             if i.get("bench") == "knob" and i.get("part") == "row"]
    assert found == ["layout.xaxis.minor.dtick"], found


def test_custom_mode_greys_the_lot():
    p = controls.panel(fake_tree(), {}, disabled=True,
                       banner="custom code — knobs are read-only until you Reset")
    rows = [c for c in walk(p)
            if isinstance(getattr(c, "id", None), dict)
            and c.id.get("part") == "row"]
    assert rows and all(r.style["opacity"] == "0.55" for r in rows)
    banners = [c for c in walk(p)
               if isinstance(getattr(c, "id", None), dict)
               and c.id.get("part") == "banner"]
    assert len(banners) == 1


# ------------------------------------------------------------------- lazy
# The pane used to build all ~2,000 knobs for every chart on every repaint:
# 14,177 components and a 4 MB layout payload for `bar`, measured. These are
# the checks that it now builds Tier 0 and nothing else, WITHOUT losing reach.


def deep_tree() -> dict:
    """A tree with a real grandchild, all in one tier.

    `trace.marker.colorbar.tickfont.size` sits three sections deep. Rendering a
    section and its grandchild in the SAME `_render` call is the case that used
    to lose the grandchild, and it is exactly what a search does - a search
    flattens all three tiers into one list.
    """
    bar = go.Bar()
    f = fixtures()
    empty = {0: [], 1: [], 2: []}
    return {
        "DATA": {0: [f["column"]], 1: [], 2: []},
        "MARK": {
            0: [],
            1: [],
            2: [from_validator("trace.marker", bar, "marker", "section"),
                from_validator("trace.marker.colorbar", bar.marker, "colorbar",
                               "section"),
                from_validator("trace.marker.colorbar.tickfont",
                               bar.marker.colorbar, "tickfont", "section"),
                from_validator("trace.marker.colorbar.tickfont.size",
                               bar.marker.colorbar.tickfont, "size", "number"),
                from_validator("trace.marker.colorbar.tickangle",
                               bar.marker.colorbar, "tickangle", "number")],
        },
        "SCALE": dict(empty), "FRAME": dict(empty),
        "INTERACTION": dict(empty), "MOTION": dict(empty),
    }


def rows_in(comp) -> list[str]:
    return [i["path"] for i in ids_in(comp)
            if i.get("bench") == "knob" and i.get("part") == "row"]


def test_lazy_builds_tier0_and_nothing_else():
    tree = fake_tree()
    t0 = {k.path for b in tree.values() for k in b[0]}
    deeper = {k.path for b in tree.values() for t in (1, 2) for k in b[t]}

    lean = controls.panel(tree, {}, lazy=True)
    built = set(rows_in(lean))
    assert built == t0, built ^ t0
    assert not (built & deeper), "a Tier 1/2 knob was built on first paint"
    assert sum(1 for _ in walk(lean)) < sum(1 for _ in walk(
        controls.panel(tree, {})))


def test_lazy_builds_no_expensive_widget_for_an_unopened_tier():
    """A colour knob is a picker AND a hex box. Neither may exist unopened."""
    tree = fake_tree()          # trace.marker.color lives in MARK tier 1
    lean = controls.panel(tree, {}, lazy=True)
    assert "trace.marker.color" not in rows_in(lean)
    pickers = [c for c in walk(lean) if getattr(c, "type", None) == "color"]
    full = [c for c in walk(controls.panel(tree, {}))
            if getattr(c, "type", None) == "color"]
    assert len(pickers) < len(full)


def test_a_collapsed_bucket_holds_no_knob_components():
    """Not hidden. Absent. Hidden-but-present is the bug this replaces."""
    lean = controls.panel(fake_tree(), {}, lazy=True, expanded=("DATA",))
    assert set(rows_in(lean)) == {"trace.x", "trace.y", "trace.text"}
    heads = sorted(c.id["bucket"] for c in walk(lean)
                   if isinstance(getattr(c, "id", None), dict)
                   and c.id.get("bench") == "bucket"
                   and c.id.get("part") == "section")
    assert heads == sorted(controls.BUCKET_ORDER), "a bucket header went missing"


def test_opening_one_bucket_materialises_only_that_bucket():
    tree = fake_tree()
    opened = controls.opened_with((), {"bench": "bucket", "bucket": "MARK",
                                       "part": "section"})
    assert opened == ("MARK:1",)
    p = controls.panel(tree, {}, lazy=True, opened=opened)
    built = set(rows_in(p))
    mark1 = {k.path for k in tree["MARK"][1] if controls.kind(k) != "section"}
    scale1 = {k.path for k in tree["SCALE"][1]}
    assert mark1 <= built, mark1 - built
    assert not (scale1 & built), "an unopened bucket built its Tier 1"
    assert not ({k.path for k in tree["MARK"][2]} & built), "Tier 2 came too"


def test_show_everything_also_brings_show_more():
    """Tier 2 under an unbuilt Tier 1 would be a hole you can see through."""
    tree = fake_tree()
    opened = controls.opened_with((), {"bench": "bucket", "bucket": "MARK",
                                       "part": "all"})
    assert set(opened) == {"MARK:1", "MARK:2"}
    built = set(rows_in(controls.panel(tree, {}, lazy=True, opened=opened)))
    assert {k.path for k in tree["MARK"][2]} <= built


def test_every_expander_carries_an_id_so_the_click_can_be_heard():
    p = controls.panel(fake_tree(), {}, lazy=True)
    parts = {(i["bucket"], i["part"]) for i in ids_in(p)
             if i.get("bench") == "bucket"}
    assert ("MARK", "section") in parts
    assert ("MARK", "more") in parts, "no click target for Tier 1"
    assert ("MARK", "all") in parts, "no click target for Tier 2"
    # and the id round-trips back to the token that materialises it
    assert controls.token_for({"bench": "bucket", "bucket": "MARK",
                               "part": "more"}) == "MARK:1"
    assert controls.token_for({"bench": "bucket", "bucket": "MARK",
                               "part": "all"}) == "MARK:2"
    assert controls.token_for({"bench": "knob", "path": "x", "part": "value"}) is None


def test_opened_with_ignores_anything_that_is_not_an_expander():
    assert controls.opened_with(("A:1",), None) == ("A:1",)
    assert controls.opened_with(("A:1",), "bench-reset") == ("A:1",)
    assert controls.opened_with(("A:1",), {"bench": "chart", "key": "bar"}) == ("A:1",)


def test_search_still_reaches_every_tier_when_lazy():
    """'minor.dtick' is SCALE Tier 2 and nothing is open. Search must find it."""
    p = controls.panel(fake_tree(), {}, query="minor", lazy=True)
    assert rows_in(p) == ["layout.xaxis.minor.dtick"]
    editors = [i for i in ids_in(p) if i.get("bench") == "knob"
               and i.get("part") == "value"]
    assert editors == [{"bench": "knob", "path": "layout.xaxis.minor.dtick",
                        "part": "value"}], editors


def test_search_carries_the_grandchild_it_matched():
    """The one that used to vanish: a match three sections deep.

    "tickfont" matches both the section and the setting inside it, so the
    section survives `_prune_sections` and the setting renders inside it.
    """
    p = controls.panel(deep_tree(), {}, query="tickfont", lazy=True)
    assert "trace.marker.colorbar.tickfont.size" in rows_in(p)
    body = next(c for c in walk(p)
                if isinstance(getattr(c, "id", None), dict)
                and c.id.get("path") == "trace.marker.colorbar.tickfont"
                and c.id.get("part") == "body")
    assert "trace.marker.colorbar.tickfont.size" in rows_in(body)


def test_a_search_that_only_hits_a_container_shows_nothing_it_cannot_turn():
    """A section is furniture, not a setting. It must not pad the count."""
    p = controls.panel(deep_tree(), {}, query="colorbar CompoundValidator",
                       lazy=True)
    assert rows_in(p) == []
    line = next(c.children for c in walk(p)
                if isinstance(getattr(c, "children", None), str)
                and "match" in c.children)
    assert line.startswith("0 knobs match"), line


def test_a_grandchild_survives_being_rendered_in_one_tier():
    """Same knob, no search - `_render` used to throw the whole branch away."""
    p = controls.panel(deep_tree(), {}, lazy=True, opened=("MARK:2",))
    assert "trace.marker.colorbar.tickfont.size" in rows_in(p)
    assert "trace.marker.colorbar.tickangle" in rows_in(p)
    ids = [tuple(sorted(i.items())) for i in ids_in(p)]
    assert len(ids) == len(set(ids)), "a knob rendered twice"


def test_the_search_cap_says_how_many_it_left_out():
    tree = fake_tree()
    p = controls.panel(tree, {}, query="a", lazy=True, limit=2)
    built = rows_in(p)
    assert len(built) == 2, built
    line = next(c.children for c in walk(p)
                if isinstance(getattr(c, "children", None), str)
                and "match" in c.children)
    assert "more" in line and "Narrow your search" in line, line
    # uncapped, the same search reaches everything it matched
    whole = rows_in(controls.panel(tree, {}, query="a", lazy=True, limit=None))
    assert len(whole) > len(built)


def test_the_search_cap_is_silent_when_nothing_was_cut():
    p = controls.panel(fake_tree(), {}, query="minor", lazy=True, limit=60)
    line = next(c.children for c in walk(p)
                if isinstance(getattr(c, "children", None), str)
                and "match" in c.children)
    assert "more" not in line and "Narrow" not in line, line


def test_materialised_is_exactly_what_the_all_input_will_carry():
    p = controls.panel(fake_tree(), {}, lazy=True)
    got = controls.materialised(p)
    from_ids = sorted({i["path"] for i in ids_in(p)
                       if i.get("bench") == "knob"
                       and i.get("part") in ("value", "hex")})
    assert got == from_ids
    assert got and len(got) < 40, got


def test_lazy_keeps_the_grey_and_lit_rule():
    tree = fake_tree()
    p = controls.panel(tree, {"layout.paper_bgcolor": "#101820"}, lazy=True)
    rows = {c.id["path"]: c for c in walk(p)
            if isinstance(getattr(c, "id", None), dict)
            and c.id.get("part") == "row"}
    assert rows["layout.paper_bgcolor"].style["borderLeft"] \
        == f"2px solid {controls.ACCENT}"
    assert rows["layout.showlegend"].style["borderLeft"] == "2px solid transparent"


def test_lazy_custom_mode_still_greys_everything_it_drew():
    p = controls.panel(fake_tree(), {}, lazy=True, disabled=True,
                       banner=" custom code ")
    rows = [c for c in walk(p)
            if isinstance(getattr(c, "id", None), dict)
            and c.id.get("part") == "row"]
    assert rows and all(r.style["opacity"] == "0.55" for r in rows)


def test_lazy_pane_survives_a_real_dash_app():
    import json

    from dash import ALL, Dash, Input, Output, State, _validate, dcc, html
    from plotly.utils import PlotlyJSONEncoder

    app = Dash(__name__)
    app.layout = html.Div([dcc.Store(id="spec"), dcc.Store(id="open"),
                           controls.panel(fake_tree(), {}, lazy=True,
                                          opened=("MARK:1",))])
    _validate.validate_layout(app.layout, app.layout)

    seen: dict[str, int] = {}
    for c in walk(app.layout):
        cid = getattr(c, "id", None)
        if cid is None:
            continue
        key = json.dumps(cid, sort_keys=True) if isinstance(cid, dict) else str(cid)
        seen[key] = seen.get(key, 0) + 1
    assert not {k: n for k, n in seen.items() if n > 1}

    @app.callback(Output("spec", "data"),
                  Input({"bench": "knob", "path": ALL, "part": ALL}, "value"),
                  State("spec", "data"), prevent_initial_call=True)
    def _knob(values, spec):        # pragma: no cover - never run here
        return spec

    @app.callback(Output("open", "data"),
                  Input({"bench": "bucket", "bucket": ALL, "part": ALL},
                        "n_clicks"),
                  State("open", "data"), prevent_initial_call=True)
    def _open(clicks, opened):      # pragma: no cover - never run here
        return opened

    assert len(app.callback_map) == 2
    json.dumps(app.layout.to_plotly_json(), cls=PlotlyJSONEncoder)


# ------------------------------------------------- the caching pass


def test_options_falls_back_when_a_value_is_unhashable():
    """An 'already an option dict' entry is unhashable, so the lru_cache
    raises TypeError internally - the fallback must still build the list."""
    values = [{"label": "Viridis", "value": "viridis"}, "plasma"]
    out = controls._options(values)
    assert out == [{"label": "Viridis", "value": "viridis"},
                   {"label": "plasma", "value": "plasma"}]


def test_options_cached_path_matches_the_uncached_one():
    values = ["linear", "log", True, 3, None]
    first = controls._options(values)
    second = controls._options(list(values))          # same content, new list
    assert first == second == controls._build_options(values)
    assert first is not second                        # a fresh list each call


def test_row_styles_are_the_shared_module_constants():
    """_row builds up to ~1,895 rows per pane; each must reuse the
    precomputed style dicts, and nothing may have mutated them."""
    knob = Knob(path="layout.title.text", control="text")
    unchanged = controls.control(knob, None)
    changed = controls.control(knob, "hello")
    disabled = controls.control(knob, None, disabled=True)

    assert unchanged.style is controls._ROW_STYLE[(False, False)]
    assert changed.style is controls._ROW_STYLE[(True, False)]
    assert disabled.style is controls._ROW_STYLE[(False, True)]
    assert unchanged.style["opacity"] == "1"
    assert disabled.style["opacity"] == "0.55"
    assert changed.style["borderLeft"].endswith(controls.ACCENT)


# ---------------------------------------------------------------- report


def main() -> int:
    """The printed version, for `python bench/controls.py`."""
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_")]
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"  ok    {name}")
        except AssertionError as e:
            failed += 1
            print(f"  FAIL  {name}: {e}")

    print("\n--- what rendered ---")
    fx = fixtures()
    print(f"{len(fx)} fixture knobs, one per SPEC 4.1 control type:")
    for name, knob in fx.items():
        comp = controls.control(knob, None)
        parts = parts_for(comp, knob.path)
        print(f"  {name:9s} {knob.path:28s} kind={controls.kind(knob):8s} "
              f"-> {type(comp).__name__:8s} parts={sorted(set(parts))}")

    tree = fake_tree()
    p = controls.panel(tree, {"trace.opacity": 0.4, "layout.paper_bgcolor": "#101820"},
                       mapping={"x": "STATE", "y": "TOTAL"})
    comps = list(walk(p))
    ids = ids_in(p)
    rows = [i for i in ids if i.get("part") == "row"]
    values = [i for i in ids if i.get("part") == "value"]
    n_knobs = sum(len(t) for b in tree.values() for t in b.values())
    print(f"\nfull panel: {n_knobs} knobs in the tree -> {len(comps)} components, "
          f"{len(ids)} dict ids, {len(rows)} rows, {len(values)} value editors")
    print(f"buckets rendered: "
          f"{[c.id['bucket'] for c in comps if isinstance(getattr(c,'id',None), dict) and c.id.get('part')=='section']}")

    # What a REAL chart's knob tree costs. knobs.py isn't finished, so stand in
    # the honest number: every setting under layout (ATLAS 1.2) is 2,488.
    import time
    LAYOUT_NODES = 2488                      # ATLAS 1.2, measured on this install
    big = {b: {0: [], 1: [], 2: []} for b in controls.BUCKET_ORDER}
    props = sorted(go.Layout()._valid_props)
    for i in range(LAYOUT_NODES):
        prop = props[i % len(props)]
        b = controls.BUCKET_ORDER[i % 6]
        big[b][i % 3].append(Knob(path=f"layout.{prop}.{i}", label=prop,
                                  control="text", default=None,
                                  description="stand-in", depth=2))
    n = sum(len(t) for bb in big.values() for t in bb.values())

    import json

    from plotly.utils import PlotlyJSONEncoder

    def weigh(label, **kw):
        t0 = time.perf_counter()
        p = controls.panel(big, {}, **kw)
        build = (time.perf_counter() - t0) * 1000
        payload = len(json.dumps(p.to_plotly_json(), cls=PlotlyJSONEncoder)) / 1024
        print(f"  {label:22s} {sum(1 for _ in walk(p)):6d} components  "
              f"{build:5.0f} ms build  {payload:8.0f} KB over the wire")

    print(f"\nscale check - {n} SYNTHETIC knobs, spread evenly over the three")
    print("tiers, so Tier 0 here is ~830. A real tree's Tier 0 is ~33 - see below.")
    weigh("eager (expanded=None)")
    weigh("eager, expanded=DATA", expanded=("DATA",))
    weigh("lazy=True", lazy=True)
    weigh("lazy + MARK open", lazy=True, opened=("MARK:1",))
    weigh("lazy + search 'font'", lazy=True, query="font")

    # The number that actually matters: the real tree for a real chart.
    from bench import knobs as knobs_mod

    real = knobs_mod.tree("bar", DF_COLUMNS)
    n_real = sum(len(t) for b in real.values() for t in b.values())
    per_tier = [sum(len(real[b][t]) for b in knobs_mod.BUCKETS) for t in (0, 1, 2)]

    def weigh_real(label, **kw):
        t0 = time.perf_counter()
        p = controls.accordion(real, {}, **kw)
        build = (time.perf_counter() - t0) * 1000
        payload = len(json.dumps(p.to_plotly_json(), cls=PlotlyJSONEncoder)) / 1024
        n_rows = len([i for i in ids_in(p) if i.get("part") == "row"])
        print(f"  {label:22s} {sum(1 for _ in walk(p)):6d} components  "
              f"{n_rows:5d} rows  {build:5.0f} ms  {payload:8.0f} KB")

    print(f"\nreal tree - knobs.tree('bar'): {n_real} knobs, "
          f"T0={per_tier[0]} T1={per_tier[1]} T2={per_tier[2]}")
    weigh_real("eager (was)")
    weigh_real("lazy=True (now)", lazy=True)
    weigh_real("lazy + MARK open", lazy=True, opened=("MARK:1",))
    weigh_real("lazy + 'tickfont'", lazy=True, query="tickfont")

    print(f"\n{len(tests) - failed}/{len(tests)} checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
