#!/usr/bin/env python
"""
THE BENCH - the round trip, and the one state object.

    python -m pytest tests/test_bench.py -q
    python tests/test_bench.py                 (same checks, prints the counts)

SPEC section 10 lists six things that have to be true before the Bench is done.
This file is the independent check on four of them - the four about state:

    item 3   the knob panel is GENERATED, never hand-written, and tiered
    item 4   turning a knob updates the chart AND the code
    item 5   editing the code updates the chart AND the knobs - or drops to
             CUSTOM cleanly
    item 7   tests cover knob generation for >= 20 trace types, a codegen
             round-trip battery, and CUSTOM-mode fallback on malformed code

and one rule from SPEC section 3 that everything else leans on:

    "knobs holds only non-default values. A knob at its default is absent."

WHY THIS FILE EXISTS ALONGSIDE tests/test_bench_app.py
------------------------------------------------------
That file drives the callbacks - it fakes a Dash context and proves the wiring
does not loop. This one goes underneath the wiring and hammers the state layer
in breadth: 48 trace types, 46 specs through the round trip, 22 pieces of
deliberately broken code. If the app is the machine, this is the metallurgy.

Nothing here needs a browser, a callback context, or a warehouse. Every
transition is a plain function call on `bench.app`'s four `_apply_*` handlers
plus the render lanes, which is what makes 300-odd assertions run in seconds.

WHAT "GENERATED, NOT HAND-WRITTEN" IS PROVED WITH
-------------------------------------------------
Two ways, both independent of knobs.py's own bookkeeping:

  1. Every property Plotly declares on the trace object and on go.Layout is
     re-derived HERE, straight off the live library, and has to appear in the
     tree. A hand-written panel would drift the moment Plotly shipped a new
     property; this catches that on the next test run.
  2. Every knob path in the tree is handed back to Plotly - `validator_for`
     has to find a live validator, and its class name has to be the one the
     Knob claims. A hand-typed path answers None.
"""

from __future__ import annotations

import json
import keyword
import sys
import warnings
from pathlib import Path

import plotly.graph_objects as go
import pytest
from dash import no_update

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bench import app as bench_app  # noqa: E402
from bench import codegen, controls, data, knobs, registry  # noqa: E402


# =====================================================================
# THE HARNESS
# ---------------------------------------------------------------------
# One screen's worth of Bench, driven by calling the handlers directly.
# The render lanes derive everything from the spec; the four `_apply_*`
# handlers are the only things that change it.
# =====================================================================


def _widgets(component) -> tuple[list[dict], list]:
    """Every knob widget in a rendered pane, the way Dash reports them.

    A pattern-matching callback gets one entry per matching id - including
    the wrapper Divs, which have no `value` prop and arrive as None. We keep
    those, because a guard that trips over them is a guard with a hole.
    """
    ids, values = [], []
    for node in component._traverse():
        cid = getattr(node, "id", None)
        if isinstance(cid, dict) and cid.get("bench") == "knob":
            ids.append(dict(cid))
            values.append(getattr(node, "value", None))
    return ids, values


def _marked_changed(component, plotly_only: bool = False) -> list[str]:
    """The paths of every row drawn as 'you changed this'.

    controls.py puts a dot next to a changed knob and lights its left edge.
    The dot is the cheapest thing to count, and it is what SPEC section 8
    means by "you should be able to see at a glance what you have touched".

    `plotly_only` drops the mapping slots. A mapping slot holding a column is
    genuinely set - the picker guessed it for you - so it is right that it
    lights up. It is just not what SPEC section 3's "absent means default"
    rule is about, which is `knobs`.
    """
    out = []
    for node in component._traverse():
        cid = getattr(node, "id", None)
        if not (isinstance(cid, dict) and cid.get("bench") == "knob"
                and cid.get("part") == "row"):
            continue
        path = str(cid.get("path"))
        if plotly_only and path.startswith(bench_app.MAPPING_PREFIX):
            continue
        for inner in node._traverse():
            if getattr(inner, "children", None) == "●":
                out.append(path)
                break
    return out


def _editors_read_only(component) -> tuple[int, int]:
    """(editors on screen, how many are read-only).

    controls.py's toggle is a `dcc.RadioItems`, which carries `disabled` per
    option rather than on the component itself, so both spellings count.
    """
    total = off = 0
    for node in component._traverse():
        cid = getattr(node, "id", None)
        if not (isinstance(cid, dict) and cid.get("bench") == "knob"
                and cid.get("part") in ("value", "hex")):
            continue
        total += 1
        options = getattr(node, "options", None)
        per_option = bool(options) and all(
            isinstance(o, dict) and o.get("disabled") for o in options)
        off += bool(getattr(node, "disabled", False)) or per_option
    return total, off


class Screen:
    """The Bench with one spec on it, and the pane that spec produced.

    Deliberately thin. It holds what the browser would hold - the spec, the two
    echoes, the code text and the widget values - and nothing else.

    The knob pane is lazy (SPEC section 4.3, wired through `controls.accordion`),
    so a real first paint materialises Tier 0 only. This harness stands in for a
    human who has already clicked "show everything" on all six buckets, which
    puts exactly the widgets on screen the eager pane used to - same ids, same
    values, same order. `open_all=False` is the honest first paint.
    """

    def __init__(self, spec: dict | None = None, open_all: bool = True):
        self.spec = spec or bench_app.blank_spec()
        self.open_all = open_all
        self.opened: dict = {}
        self.echo = {"code": ""}
        self.knob_echo = {"knobs": {}, "sig": None, "vals": None}
        self.code = ""
        self.figure: go.Figure | None = None
        self.pane = None
        self.ids: list[dict] = []
        self.values: list = []
        self.message = ""
        self.build_msg = ""
        self.pane_rebuilds = 0
        self.draw()

    # -- derive everything from the spec (callbacks 2 and 3) -----------
    def draw(self) -> "Screen":
        self.opened = ({"key": bench_app.open_key(self.spec),
                        "tokens": list(bench_app.ALL_TIERS_OPEN)}
                       if self.open_all else {})
        (fig, code, _status, build_msg, _mode, echo) = bench_app.render_chart(
            self.spec, self.echo)
        pane, knob_echo = bench_app.render_knobs(self.spec, "", self.opened,
                                                 self.knob_echo)
        self.figure = fig
        if code is not no_update:
            self.code = code
        if pane is not no_update:
            self.pane = pane
            self.ids, self.values = _widgets(pane)
            self.pane_rebuilds += 1
        self.build_msg = build_msg
        if echo is not no_update:
            self.echo = echo
        if knob_echo is not no_update:
            self.knob_echo = knob_echo
        return self

    # -- the four things a human can do (callback 1's handlers) --------
    def turn(self, path: str, value) -> "Screen":
        """Move one widget and hand the whole pane back, as the browser does."""
        for i, cid in enumerate(self.ids):
            if cid.get("path") == path and cid.get("part") == "value":
                self.values[i] = value
                break
        else:
            raise AssertionError(f"no widget for {path!r}")
        spec, self.message, _echo = bench_app._apply_knobs(
            self._copy(), self.ids, self.values, self.knob_echo)
        self.spec = spec
        return self.draw()

    def report_unchanged(self):
        """Tell the server what the widgets say, having touched nothing."""
        return bench_app._apply_knobs(self._copy(), self.ids, self.values,
                                      self.knob_echo)

    def type_code(self, text: str) -> "Screen":
        self.spec, self.message = bench_app._apply_code(self._copy(), text,
                                                        self.echo)
        return self.draw()

    def click(self, chart: str) -> "Screen":
        self.spec, self.message = bench_app._apply_chart(self._copy(), chart)
        return self.draw()

    def reset(self) -> "Screen":
        self.spec, self.message = bench_app._apply_reset(self._copy())
        return self.draw()

    # -- readers -------------------------------------------------------
    def _copy(self) -> dict:
        return json.loads(json.dumps(self.spec))

    def widget(self, path: str, part: str = "value"):
        for cid, value in zip(self.ids, self.values):
            if cid.get("path") == path and cid.get("part") == part:
                return value
        raise AssertionError(f"no widget for {path!r}")

    def has_widget(self, path: str, part: str = "value") -> bool:
        return any(cid.get("path") == path and cid.get("part") == part
                   for cid in self.ids)

    @property
    def knobs(self) -> dict:
        return self.spec.get("knobs") or {}

    @property
    def custom(self) -> bool:
        return isinstance(self.spec.get("custom_code"), str)


@pytest.fixture()
def screen():
    return Screen()


DEMO_SOURCE = {"kind": "demo", "name": "category"}
DEMO_COLUMNS = ["agency", "region", "spend", "date"]


def _frame():
    return bench_app.get_frame(DEMO_SOURCE)


# =====================================================================
# 1. SPEC 10, ITEM 3 - THE KNOB PANEL IS GENERATED AND TIERED
# ---------------------------------------------------------------------
# One registry key per distinct trace type. SPEC section 10 item 7 asks
# for twenty; this install has forty-eight, so we do all of them - there
# is no reason to test a sample when the whole population runs in two
# seconds.
# =====================================================================


def _one_chart_per_trace_type() -> dict[str, str]:
    """{trace type: the first registry key that draws it}. 48 on this install."""
    out: dict[str, str] = {}
    for template in registry.TEMPLATES:
        out.setdefault(template.trace_type, template.key)
    return out


TRACE_TYPES: dict[str, str] = _one_chart_per_trace_type()
CHART_KEYS: list[str] = sorted(TRACE_TYPES.values())


def test_the_trace_type_battery_is_big_enough():
    """SPEC section 10 item 7 asks for twenty trace types. Count them."""
    assert len(TRACE_TYPES) >= 20, TRACE_TYPES
    assert len(CHART_KEYS) == len(TRACE_TYPES)


@pytest.mark.parametrize("key", CHART_KEYS)
def test_the_tree_holds_every_property_plotly_declares(key):
    """Re-derive the top level from the live library. Nothing may be missing.

    This is the "generated, never hand-written" proof from the other side:
    the expectation is built here, off `go.<Trace>` and `go.Layout`, without
    asking knobs.py anything. A hand-maintained panel drifts the day Plotly
    adds a property; this notices on the next run.
    """
    tree = knobs.tree(key, DEMO_COLUMNS)
    paths = {k.path for b in knobs.BUCKETS for t in knobs.TIERS for k in tree[b][t]}

    live = knobs.trace_type_for(key)
    trace = getattr(go, knobs.TRACE_CLASS_NAMES[live])()
    for obj, prefix in ((trace, "trace"), (go.Layout(), "layout")):
        for name in obj._valid_props:
            try:
                validator = obj._get_validator(name)
            except Exception:          # pragma: no cover - a broken install
                continue
            if type(validator).__name__ in knobs.SKIP_VALIDATORS:
                continue
            assert f"{prefix}.{name}" in paths, f"{key}: {prefix}.{name} is missing"


@pytest.mark.parametrize("key", CHART_KEYS)
def test_every_knob_traces_back_to_a_live_plotly_validator(key):
    """Hand each path back to Plotly. It has to recognise every one.

    A path somebody typed by hand comes back None here, and a Knob claiming
    the wrong validator class comes back with a different class name - so
    this catches both a fabricated knob and a mislabelled one.

    Sampled every 37th knob rather than all ~2,000, because building the
    intermediate objects for a deep path is the slow part and 37 is coprime
    with nothing in particular - it just walks the whole tree evenly.
    """
    flat = knobs.flat(key, DEMO_COLUMNS)
    assert len(flat) > 200, f"{key}: only {len(flat)} knobs, that cannot be right"
    for knob in flat[::37]:
        validator = knobs.validator_for(knob.path, key)
        assert validator is not None, f"{key}: Plotly does not know {knob.path}"
        assert type(validator).__name__ == knob.validator, knob.path


@pytest.mark.parametrize("key", CHART_KEYS)
def test_the_tree_is_tiered_exactly_the_way_the_spec_says(key):
    """SPEC section 4.3, checked as three rules rather than as a count.

    Tier 0 is the ATLAS twenty plus this chart's own data channels. Tier 1 is
    depth 1-2. Tier 2 is depth 3 and below. Every bucket and every tier is
    present even when empty, so the UI never has to check for a hole.
    """
    tree = knobs.tree(key, DEMO_COLUMNS)
    assert set(tree) == set(knobs.BUCKETS)
    for bucket in knobs.BUCKETS:
        assert set(tree[bucket]) == set(knobs.TIERS), bucket
        for knob in tree[bucket][0]:
            assert knob.path in knobs.TIER0 or bucket == knobs.DATA, knob.path
        for knob in tree[bucket][1]:
            assert knob.depth <= 2, knob.path
        for knob in tree[bucket][2]:
            assert knob.depth >= 3, knob.path


@pytest.mark.parametrize("key", CHART_KEYS)
def test_the_tree_comes_out_in_the_same_order_every_time(key):
    """Two builds, one order. The echo store compares values by position, so
    a tree that shuffled would make the no-loop guard unreliable."""
    first = [k.path for k in knobs.flat(key, DEMO_COLUMNS)]
    second = [k.path for k in knobs.flat(key, DEMO_COLUMNS)]
    assert first == second
    assert len(set(first)) == len(first), "a path appears twice"


@pytest.mark.parametrize("key", CHART_KEYS)
def test_the_data_bucket_is_this_chart_s_own_mapping_slots(key):
    """app.py swaps knobs.py's DATA bucket for the template's slots.

    That is a decision, not an omission - `trace.x` bound through
    update_traces would set x to the letters of the column name, not to the
    column. So the DATA bucket you see is what registry.py can actually build
    from, and every declared slot has to be there.
    """
    template = registry.CHARTS[key]
    tree = bench_app.knob_tree({"chart": key}, DEMO_COLUMNS)
    slots = {k.path for k in tree[knobs.DATA][0]}
    for slot in template.slots:
        assert f"{bench_app.MAPPING_PREFIX}{slot.name}" in slots, (key, slot.name)
    for path in slots:
        assert path.startswith(bench_app.MAPPING_PREFIX), path


def test_the_panel_is_big_and_none_of_it_was_typed_by_hand():
    """The headline number, and the reason nobody hand-writes this panel."""
    pane_knobs = knobs.flat("bar", DEMO_COLUMNS)
    assert len(pane_knobs) > 1500, len(pane_knobs)
    assert len({k.validator for k in pane_knobs}) > 8
    # every control name controls.py knows how to draw, or a section/list
    for knob in pane_knobs:
        assert controls.kind(knob) in controls.CONTROL_KINDS, knob.path


# =====================================================================
# 2. SPEC 10, ITEM 4 - TURNING A KNOB UPDATES THE CHART AND THE CODE
# ---------------------------------------------------------------------
# Each row is (path, what you type, how to read it back off the figure,
# what you should see). One from every bucket that emits code, plus the
# awkward ones - a colour, a list, a list of dicts, a template name.
# =====================================================================

KNOB_TURNS = [
    ("layout.title.text", "Spend by agency",
     lambda f: f.layout.title.text, "Spend by agency"),
    ("layout.barmode", "group", lambda f: f.layout.barmode, "group"),
    ("layout.xaxis.categoryorder", "total descending",
     lambda f: f.layout.xaxis.categoryorder, "total descending"),
    ("layout.xaxis.type", "log", lambda f: f.layout.xaxis.type, "log"),
    ("layout.yaxis.tickformat", ",.0f",
     lambda f: f.layout.yaxis.tickformat, ",.0f"),
    ("layout.yaxis.range", [0, 100],
     lambda f: list(f.layout.yaxis.range), [0, 100]),
    ("layout.yaxis.showgrid", False, lambda f: f.layout.yaxis.showgrid, False),
    ("layout.hovermode", "x unified", lambda f: f.layout.hovermode, "x unified"),
    ("layout.dragmode", "pan", lambda f: f.layout.dragmode, "pan"),
    ("layout.showlegend", False, lambda f: f.layout.showlegend, False),
    ("layout.legend.orientation", "h",
     lambda f: f.layout.legend.orientation, "h"),
    ("layout.margin.l", 120, lambda f: f.layout.margin.l, 120),
    ("layout.width", 900, lambda f: f.layout.width, 900),
    ("layout.font.size", 15, lambda f: f.layout.font.size, 15),
    ("layout.paper_bgcolor", "#0d1117",
     lambda f: f.layout.paper_bgcolor, "#0d1117"),
    ("layout.colorway", ["#ff0000", "#00ff00"],
     lambda f: list(f.layout.colorway), ["#ff0000", "#00ff00"]),
    # the one that used to store 13,670 characters of stringified Template
    ("layout.template", "plotly_dark",
     lambda f: f.layout.template.layout.paper_bgcolor, "rgb(17,17,17)"),
    ("layout.transition.duration", 400,
     lambda f: f.layout.transition.duration, 400),
    ("trace.marker.opacity", 0.8, lambda f: f.data[0].marker.opacity, 0.8),
    ("trace.orientation", "h", lambda f: f.data[0].orientation, "h"),
    # layout.shapes / layout.annotations are no longer typed as lists into a
    # text box - they have the add/remove compound editor now, and their
    # widget-to-figure trip is proven in tests/test_bench_compound.py.
]


@pytest.mark.parametrize("path,typed,read,expected",
                         KNOB_TURNS, ids=[t[0] for t in KNOB_TURNS])
def test_turning_a_knob_reaches_the_spec_the_code_and_the_figure(
        screen, path, typed, read, expected):
    """One knob, all the way through. SPEC section 10 item 4.

    Three things have to happen and all three are checked here: the value
    lands in SPEC["knobs"], the line appears in the code panel, and the
    FIGURE actually changes. The third is the one that catches a knob that
    stores cleanly and then quietly fails to apply.
    """
    screen.turn(path, typed)
    assert path in screen.knobs, f"{path} never reached the spec: {screen.message}"

    keyword_form = codegen._flatten(path)
    assert f"{keyword_form}=" in screen.code, f"{keyword_form} is not in the code"

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        df, meta = _frame()
        fig, why = bench_app.figure_for(screen.spec, df, meta)
    assert not why, why
    assert not caught, f"{path} did not apply: {caught[0].message}"
    assert read(fig) == expected


@pytest.mark.parametrize("path,typed,read,expected",
                         KNOB_TURNS, ids=[t[0] for t in KNOB_TURNS])
def test_a_turned_knob_survives_the_round_trip(screen, path, typed, read, expected):
    """Whatever a knob turn stores has to be readable back out of the code."""
    screen.turn(path, typed)
    assert codegen.parse(screen.code) == screen.spec


def test_every_tier0_knob_survives_the_whole_chain():
    """The ATLAS twenty, swept: store -> code -> parse -> figure.

    Values are taken from Plotly's own option lists where there is one, so
    nothing here is a value somebody imagined. A knob that stores but does
    not apply raises a warning inside registry._apply_knobs, and a warning
    fails this test - that is exactly how `layout.template` was caught.
    """
    df, meta = _frame()
    tree = knobs.tree("bar", bench_app._columns(df))
    tier0 = [k for b in knobs.BUCKETS if b != knobs.DATA for k in tree[b][0]]
    assert len(tier0) >= 25, len(tier0)

    hand_written = {
        "layout.yaxis.range": [0, 100],
        "layout.colorway": ["#ff0000", "#00ff00"],
        "layout.annotations": [{"text": "hi", "x": 1, "y": 2}],
        "layout.shapes": [{"type": "line", "x0": 0, "x1": 1, "y0": 0, "y1": 1}],
    }
    checked = 0
    for knob in tier0:
        if knob.path in hand_written:
            value = hand_written[knob.path]
        elif knob.options:
            value = next((o for o in knob.options if isinstance(o, str) and o),
                         knob.options[0])
        elif knob.control in ("number", "slider", "integer", "angle"):
            value = 12
        elif knob.control == "color":
            value = "#123456"
        elif knob.control == "toggle":
            value = False
        else:
            value = "hello"

        ok, coerced = knobs.validate(knob.path, value, "bar")
        assert ok, f"{knob.path}: Plotly refused its own option {value!r}: {coerced}"
        stored = bench_app._jsonable(coerced)
        spec = {**bench_app.blank_spec(), "knobs": {knob.path: stored}}

        code = bench_app.render_code(spec)
        assert codegen.parse(code) == spec, knob.path
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            fig, why = bench_app.figure_for(spec, df, meta)
        assert not why, (knob.path, why)
        assert not caught, f"{knob.path} did not apply: {caught[0].message}"
        assert isinstance(fig, go.Figure)
        checked += 1
    assert checked == len(tier0)


def test_a_template_name_stays_a_template_name(screen):
    """Regression: `layout.template` is the one knob Plotly answers oddly.

    `BaseTemplateValidator.validate_coerce("plotly_dark")` hands back the whole
    expanded Template object - 13,670 characters on plotly 6.9.0. Stored, that
    became a 14 KB code panel and a figure that quietly kept its old template,
    because Plotly then refuses the stringified object. knobs.validate keeps
    the name instead. See knobs._json_safe.
    """
    screen.turn("layout.template", "plotly_dark")
    assert screen.knobs["layout.template"] == "plotly_dark"
    assert len(screen.code) < 1000, "the template expanded into the code panel"
    assert 'template="plotly_dark"' in screen.code


def test_a_mapping_slot_is_not_a_knob(screen):
    """Which column goes where lives in `mapping`, never in `knobs`.

    SPEC section 3 keeps them apart because the mapping's legal values come
    from the data and every other bucket's come from Plotly.
    """
    screen.turn(f"{bench_app.MAPPING_PREFIX}color", "region")
    assert screen.spec["mapping"]["color"] == "region"
    assert not any(k.startswith(bench_app.MAPPING_PREFIX) for k in screen.knobs)
    assert 'color="region"' in screen.code


def test_a_knob_plotly_refuses_is_a_sentence_not_a_broken_chart(screen):
    """A bad value comes back as a message and the spec is left alone."""
    screen.turn("layout.barmode", "sideways")
    assert "layout.barmode" not in screen.knobs
    assert "layout.barmode" in screen.message
    assert isinstance(screen.figure, go.Figure)


# =====================================================================
# 3. SPEC 10, ITEM 7 - THE ROUND TRIP:  parse(render(spec)) == spec
# ---------------------------------------------------------------------
# Two halves. The hand-written half goes after the awkward values - a
# quote, a newline, a lone minus sign, an empty dict, a list of dicts.
# The generated half takes real registry charts with real auto-mapped
# columns, so the battery cannot drift away from what the app produces.
# =====================================================================


def _spec(chart="bar", source=None, mapping=None, knobs_=None, custom=None):
    return {
        "chart": chart,
        "source": DEMO_SOURCE if source is None else source,
        "mapping": {} if mapping is None else mapping,
        "knobs": {} if knobs_ is None else knobs_,
        "custom_code": custom,
    }


def _hand_written_battery() -> list[tuple[str, dict]]:
    """The awkward corners, named one by one."""
    return [
        ("bare minimum", _spec()),
        ("px-pure chart with a mapping",
         _spec("bar", mapping={"x": "agency", "y": "spend", "color": None})),
        ("registry-built chart",
         _spec("sankey", mapping={"source": "src", "target": "tgt", "value": "amt"})),
        ("a px name that is not px-pure",
         _spec("pie", mapping={"names": "agency", "values": "spend"})),
        ("every bucket at once",
         _spec("bar", mapping={"x": "agency", "y": "spend"}, knobs_={
             "trace.marker.opacity": 0.8,
             "layout.xaxis.categoryorder": "total descending",
             "layout.barmode": "group",
             "layout.hovermode": "x unified",
             "layout.transition.duration": 300,
         })),
        ("a title with an em dash and an emoji",
         _spec(knobs_={"layout.title.text": "Spend — by agency 📊"})),
        ("a title with quotes and a backslash",
         _spec(knobs_={"layout.title.text": 'she said "no" \\ twice'})),
        ("a title with a newline and a tab",
         _spec(knobs_={"layout.title.text": "line one\nline two\tindented"})),
        ("negative numbers",
         _spec(knobs_={"layout.margin.l": -0, "layout.xaxis.tickangle": -45,
                       "layout.legend.x": -1.5})),
        ("floats that do not round nicely",
         _spec(knobs_={"trace.marker.opacity": 0.1 + 0.2,
                       "layout.legend.y": 1.0000000000000002})),
        ("False is not zero",
         _spec(knobs_={"layout.showlegend": False, "layout.width": 0})),
        ("True is not one",
         _spec(knobs_={"layout.xaxis.showgrid": True, "layout.height": 1})),
        ("an empty mapping", _spec("bar", mapping={})),
        ("a mapping that is all None",
         _spec("bar", mapping={"x": None, "y": None, "color": None})),
        ("a many-slot mapping",
         _spec("corr_matrix", mapping={"values": ["a", "b", "c"]})),
        ("an eight-slot mapping",
         _spec("candlestick", mapping={"x": "date", "open": "o", "high": "h",
                                       "low": "l", "close": "c"})),
        ("a nested list value",
         _spec(knobs_={"layout.yaxis.range": [0, 100],
                       "layout.xaxis.range": [-1.5, 1.5]})),
        ("a list of dicts",
         _spec(knobs_={"layout.annotations": [{"text": "a", "x": 1},
                                              {"text": "b", "y": 2}]})),
        ("a dict value", _spec(knobs_={"layout.grid": {"rows": 2, "columns": 1}})),
        ("an empty list", _spec(knobs_={"layout.shapes": []})),
        ("an empty dict", _spec(knobs_={"layout.grid": {}})),
        ("an empty string", _spec(knobs_={"layout.title.text": ""})),
        ("a hundred numbers",
         _spec(knobs_={"layout.xaxis.tickvals": list(range(100))})),
        ("the underscore names",
         _spec(knobs_={"layout.paper_bgcolor": "#0d1117",
                       "layout.plot_bgcolor": "#161b22",
                       "trace.error_y.visible": True})),
        ("a deep path", _spec(knobs_={"layout.xaxis.title.font.size": 11})),
        ("MOTION on its own", _spec(knobs_={"layout.transition.easing": "linear"})),
        ("INTERACTION on its own", _spec(knobs_={"layout.clickmode": "event+select"})),
        ("trace knobs only",
         _spec(knobs_={"trace.marker.line.width": 2,
                       "trace.marker.line.color": "#ffffff"})),
        ("enough knobs to force the wrap",
         _spec(knobs_={f"layout.margin.{side}": 40 + i
                       for i, side in enumerate(("l", "r", "t", "b"))}
               | {"layout.title.text": "a title long enough that the call has "
                                       "to wrap one argument per line"})),
        ("a warehouse source",
         _spec(source={"kind": "warehouse",
                       "sql": "SELECT \"STATE\", SUM(x)\nFROM t\nWHERE a='b'\n"
                              "GROUP BY 1",
                       "limit_rows": 5000})),
        ("an empty source", _spec(source={})),
        ("a source with an odd key",
         _spec(source={"kind": "demo", "name": "category", "note": "hand-made"})),
    ]


def _generated_battery() -> list[tuple[str, dict]]:
    """Real charts, auto-mapped against a real demo frame.

    This half exists so the battery cannot quietly stop resembling what the
    app actually produces. Every spec here is one a picker click would make.
    """
    out = []
    df, _meta = _frame()
    for key in ["bar", "bar_sorted", "box_compare", "violin", "heatmap",
                "treemap", "sunburst", "waterfall", "funnel", "indicator",
                "table", "icicle", "histogram_groupby", "corr_matrix"]:
        template = registry.CHARTS[key]
        out.append((f"auto-mapped {key}",
                    _spec(key, mapping=registry.auto_map(df, template))))
    return out


BATTERY: list[tuple[str, dict]] = _hand_written_battery() + _generated_battery()
BATTERY_IDS = [label for label, _ in BATTERY]


def test_the_round_trip_battery_is_big_enough():
    """SPEC section 10 item 7 asks for a battery. Count it."""
    assert len(BATTERY) >= 30, len(BATTERY)
    assert len(set(BATTERY_IDS)) == len(BATTERY), "two specs share a name"


@pytest.mark.parametrize("label,spec", BATTERY, ids=BATTERY_IDS)
def test_round_trip_is_exact(label, spec):
    """parse(render(spec)) == spec, through the app's own render.

    `app.render_code` narrows codegen's PX_CHARTS to the four registry keys
    that really are one bare `px` call, so this is the round trip as the code
    panel actually prints it - not as codegen would print it on its own.
    """
    code = bench_app.render_code(spec)
    assert codegen.parse(code) == spec


@pytest.mark.parametrize("label,spec", BATTERY, ids=BATTERY_IDS)
def test_the_generated_code_is_real_python(label, spec):
    """It has to compile. A code panel that will not run teaches nothing."""
    compile(bench_app.render_code(spec), "<battery>", "exec")


@pytest.mark.parametrize("label,spec", BATTERY, ids=BATTERY_IDS)
def test_rendering_is_deterministic(label, spec):
    """Same spec, same characters. The two-way sync rests on this - a render
    that wobbled would fight the person typing in the box."""
    assert bench_app.render_code(spec) == bench_app.render_code(spec)


@pytest.mark.parametrize("label,spec", BATTERY, ids=BATTERY_IDS)
def test_a_second_pass_changes_nothing(label, spec):
    """render -> parse -> render lands on the same text. No drift over time."""
    once = bench_app.render_code(spec)
    twice = bench_app.render_code(codegen.parse(once))
    assert once == twice


@pytest.mark.parametrize("label,spec", BATTERY, ids=BATTERY_IDS)
def test_the_spec_is_json(label, spec):
    """SPEC section 3: the state object has to survive a dcc.Store."""
    assert json.loads(json.dumps(spec)) == spec


def test_every_mapping_slot_name_is_a_safe_python_keyword():
    """A slot called `class` or `lambda` would render code that will not parse.

    63 distinct slot names across the 145 templates on this install, and the
    round trip needs every one of them to be a plain identifier.
    """
    names = sorted({s.name for t in registry.TEMPLATES for s in t.slots})
    assert len(names) > 40, len(names)
    for name in names:
        assert name.isidentifier(), name
        assert not keyword.iskeyword(name), name


def test_the_chart_key_comes_back_whichever_form_it_was_printed_in():
    """Four charts print as `px.<key>(df, ...)`; the rest go through the
    registry. `parse` has to recover the same key either way."""
    assert registry.PX_PURE, "no chart is a bare px call - that cannot be right"
    for key in sorted(registry.PX_PURE):
        code = bench_app.render_code(_spec(key))
        assert f"px.{key}(df" in code
        assert codegen.parse(code)["chart"] == key
    for key in ("sankey", "bar_sorted", "ridgeline"):
        code = bench_app.render_code(_spec(key))
        assert f'bench.registry.build("{key}", df' in code
        assert codegen.parse(code)["chart"] == key


def test_rendering_leaves_codegen_exactly_as_it_found_it():
    """`render_code` narrows another module's global and must put it back.

    It is done under a lock and in a `finally`, because leaking that set is
    how the first build of app.py turned two tests in test_bench_codegen.py
    red from three files away.
    """
    before = set(codegen.PX_CHARTS)
    bench_app.render_code(_spec("bar"))
    assert set(codegen.PX_CHARTS) == before
    try:
        bench_app.render_code(_spec(chart=None))     # render raises on this
    except (ValueError, TypeError):
        pass
    assert set(codegen.PX_CHARTS) == before, "a raised render leaked the set"


# =====================================================================
# 4. SPEC 10, ITEM 5 - THE CODE MOVES THE KNOBS, OR DROPS TO CUSTOM
# =====================================================================


def test_editing_the_code_moves_the_knob_widgets(screen):
    """Type a canonical line, and the widget on the right has to move.

    This is the half of the two-way contract that is easy to skip: it is
    obvious that a knob writes code, and much less obvious that code writes
    knobs. SPEC section 10 item 5 asks for both.
    """
    typed = {"layout.title.text": "typed by hand",
             "layout.barmode": "stack",
             "layout.hovermode": "x unified",
             "trace.marker.opacity": 0.35}
    wanted = {**screen.spec, "knobs": typed}
    screen.type_code(bench_app.render_code(wanted))

    assert screen.knobs == typed, screen.message
    for path, value in typed.items():
        assert screen.widget(path) == value, path
    assert sorted(_marked_changed(screen.pane, plotly_only=True)) == sorted(typed)
    assert screen.figure.layout.title.text == "typed by hand"


def test_editing_the_code_can_change_the_chart_and_the_mapping(screen):
    """The code panel is the whole state object, not just the knobs."""
    other = {**screen.spec, "chart": "bar_horizontal",
             "mapping": {"x": "spend", "y": "agency", "color": None}}
    screen.type_code(bench_app.render_code(other))
    assert screen.spec["chart"] == "bar_horizontal"
    assert screen.spec["mapping"]["x"] == "spend"
    assert not screen.custom


# --- the malformed battery -------------------------------------------
# SPEC section 1: CUSTOM mode is a feature. Every one of these has to
# land there cleanly - chart still drawn, knobs read-only, Reset home.

_CANON = ('df = bench.data.frame({"kind": "demo", "name": "category"})\n'
          'fig = px.bar(df, x="agency", y="spend")\n')

MALFORMED: list[tuple[str, str]] = [
    ("an import", "import os"),
    ("a loop", "for i in range(3): pass"),
    ("a function", "def f(): return 1"),
    ("half a line", "1 +"),
    ("a lambda", "lambda: 1"),
    ("a walrus", "(x := 1)"),
    ("an f-string", 'f"{1}"'),
    ("a class", "class C: pass\nfig = 1"),
    ("a comment on its own", "# just a comment"),
    ("something that raises", "raise ValueError('boom')"),
    ("a call we do not know", "df = evil()"),
    ("one statement only", "fig = px.bar(df)"),
    ("no df line", "fig = px.bar(df, x='agency', y='spend')\nfig.show()"),
    ("a statement after fig.show()", _CANON + "fig.show()\nx = 1"),
    ("**kwargs on a bucket call",
     _CANON + 'fig.update_layout(**{"barmode": "group"})'),
    ("a positional arg on a bucket call",
     _CANON + 'fig.update_layout({"barmode": "group"})'),
    ("a fig method we do not know", _CANON + "fig.add_hline(y=1)"),
    ("arithmetic in a mapping", _CANON.replace('y="spend"', "y=1+1")),
    ("bytes in a mapping", _CANON.replace('y="spend"', "y=b'bytes'")),
    ("the wrong arity on the registry call", "fig = bench.registry.build(df)"),
    ("two args to the source call",
     "df = bench.data.frame({'kind':'demo','name':'category'}, 2)"),
    ("a non-ascii name", "éà = 1\nfig = 2"),
]
MALFORMED_IDS = [label for label, _ in MALFORMED]


def test_the_malformed_battery_is_big_enough():
    """SPEC section 10 item 7 asks for deliberately malformed code."""
    assert len(MALFORMED) >= 15, len(MALFORMED)
    assert len(set(MALFORMED_IDS)) == len(MALFORMED)


@pytest.mark.parametrize("label,src", MALFORMED, ids=MALFORMED_IDS)
def test_parse_returns_none_and_never_raises(label, src):
    """`parse` promises a return value, not an exception. SPEC section 5.1."""
    assert codegen.parse(src) is None


@pytest.mark.parametrize("label,src", MALFORMED, ids=MALFORMED_IDS)
def test_malformed_code_drops_to_custom_mode_cleanly(label, src):
    """The full CUSTOM-mode contract, on one piece of broken code.

    Four things, and all four are the point of the escape hatch: the code is
    kept verbatim, the banner says why, the chart pane still shows something
    rather than dying, and Reset brings the canonical form back untouched.
    """
    screen = Screen()
    before_code = screen.code
    before_spec = json.loads(json.dumps(screen.spec))

    screen.type_code(src)
    assert screen.custom, label
    assert screen.spec["custom_code"] == src
    assert screen.message.startswith("CUSTOM mode"), screen.message
    assert screen.code == src, "the code panel must keep exactly what you typed"

    assert isinstance(screen.figure, go.Figure)

    total, off = _editors_read_only(screen.pane)
    assert total > 100 and off == total, f"{off} of {total} editors are read-only"

    screen.reset()
    assert not screen.custom
    assert screen.code == before_code
    assert screen.spec == before_spec


@pytest.mark.parametrize("label,src", MALFORMED, ids=MALFORMED_IDS)
def test_custom_code_is_handed_back_untouched(label, src):
    """While CUSTOM is on, the code panel IS the state. render must not
    rewrite a single character of it."""
    spec = _spec(custom=src)
    assert bench_app.render_code(spec) == src


def test_an_empty_box_is_not_custom_mode(screen):
    """Clearing the box is a slip, not an escape hatch. Say so and wait."""
    screen.type_code("   \n  \n")
    assert not screen.custom
    assert "empty" in screen.message
    assert screen.knobs == {}


def test_code_naming_a_chart_that_does_not_exist_is_custom(screen):
    """It parses perfectly and still cannot be built. That is CUSTOM too."""
    screen.type_code(bench_app.render_code(_spec("no_such_chart")))
    assert screen.custom
    assert "no_such_chart" in screen.message


def test_the_echo_stops_the_code_panel_answering_itself(screen):
    """Handing back the exact text we just wrote is not an edit.

    Rule 2 of the no-loop contract. Without it the panel and the knobs write
    to each other forever.
    """
    before = json.loads(json.dumps(screen.spec))
    for _ in range(5):
        screen.type_code(screen.code)
        assert screen.spec == before
        assert not screen.custom
        assert screen.message == ""


def test_reset_on_canonical_code_says_there_was_nothing_to_do(screen):
    assert not screen.custom
    screen.reset()
    assert "nothing to reset" in screen.message


# =====================================================================
# 5. SPEC SECTION 3 - A KNOB AT ITS DEFAULT IS ABSENT
# ---------------------------------------------------------------------
# "knobs holds only non-default values." Everything readable about the
# generated code rests on this: 2,000 settings exist, and the panel only
# ever writes down the handful you moved.
# =====================================================================


def test_the_opening_screen_has_no_knobs_at_all(screen):
    """Nothing has been touched, so nothing is written down."""
    assert screen.knobs == {}
    assert screen.spec["custom_code"] is None
    assert len(screen.ids) > 1000, "the pane did not build"


def test_no_row_is_marked_changed_until_you_change_one(screen):
    """SPEC section 8: a knob at its default renders greyed, a changed one lit.

    Counting the dots is the cheapest read of that rule, and it is the same
    thing a human does at a glance. Two thousand Plotly settings, none of them
    lit - and the two mapping slots the picker filled in for you, which are
    lit because they really do hold a column.
    """
    assert _marked_changed(screen.pane, plotly_only=True) == []
    lit_mapping = _marked_changed(screen.pane)
    assert lit_mapping and all(p.startswith(bench_app.MAPPING_PREFIX)
                               for p in lit_mapping), lit_mapping
    assert sorted(lit_mapping) == sorted(
        f"{bench_app.MAPPING_PREFIX}{slot}"
        for slot, column in screen.spec["mapping"].items() if column)

    screen.turn("layout.title.text", "one knob")
    assert _marked_changed(screen.pane, plotly_only=True) == ["layout.title.text"]


def test_reporting_every_widget_back_writes_nothing(screen):
    """~4,000 widgets report in and the spec must not gain a single key.

    This is the invariant that makes "absent means default" true in practice:
    the pane is full of widgets showing something, and none of that showing
    counts as a value.
    """
    spec, message, echo = screen.report_unchanged()
    assert spec["knobs"] == {}
    assert spec == screen.spec
    assert message == ""
    assert echo is no_update, "nothing moved, so the echo should not be rewritten"


def test_no_widget_shows_a_value_the_spec_does_not_already_imply(screen):
    """What the echo is actually holding back, measured rather than assumed.

    Take the echo away entirely and ask the same widgets again. A few of them
    do write something, and every one has to be a widget displaying the very
    default the spec is silent about:

      * a slider parked at its own minimum. controls.py has to put the handle
        somewhere, and a slider with no position is not a slider.
      * a list-shaped knob whose blank default really is `[]` - `shapes`,
        `annotations`, `map.layers` - rendered as a text box reading "[]".

    Neither is a setting you chose, and the echo store is what stops them
    being recorded as one.

    A failure here means some control has started displaying a value that is
    NOT the recorded default, and "absent from knobs means at default" has a
    new hole in it. Counting them is deliberately avoided: the count moves
    whenever controls.py learns a new widget, and the invariant does not.
    """
    spec, _message, _echo = bench_app._apply_knobs(
        json.loads(json.dumps(screen.spec)), screen.ids, screen.values,
        {"knobs": {}})           # deliberately no echo at all
    index = bench_app._knob_index("bar", tuple(bench_app._columns(_frame()[0])))
    for path, value in spec["knobs"].items():
        knob = index.get(path)
        assert knob is not None, path
        if value == knob.default:
            continue
        assert controls.kind(knob) == "slider", (path, value, knob.control,
                                                 knob.default)
        assert knob.min is not None and float(value) == float(knob.min), (
            path, value, knob.min)
    assert spec["mapping"] == screen.spec["mapping"]


def test_clearing_a_knob_removes_the_key_rather_than_storing_none(screen):
    """Cleared means gone. A `None` left behind would render as `x=None`."""
    screen.turn("layout.title.text", "here for a moment")
    assert screen.knobs == {"layout.title.text": "here for a moment"}
    screen.turn("layout.title.text", None)
    assert "layout.title.text" not in screen.knobs
    assert screen.knobs == {}
    assert "title_text" not in screen.code


def test_an_empty_text_box_clears_a_knob_too(screen):
    """A text box hands back "" rather than None when you delete its contents."""
    screen.turn("layout.yaxis.tickformat", ",.0f")
    assert "layout.yaxis.tickformat" in screen.knobs
    screen.turn("layout.yaxis.tickformat", "")
    assert "layout.yaxis.tickformat" not in screen.knobs


def test_a_new_chart_keeps_the_knobs_it_can_hold(screen):
    """A picker click carries over knobs the new chart also has - ten minutes
    of styling no longer dies on a misclick. Layout knobs are universal
    (go.Layout is shared by every trace type), so barmode rides along;
    trace.* knobs are the ones that get dropped when they have no home."""
    screen.turn("layout.barmode", "group")
    assert screen.knobs
    screen.click("violin")
    assert screen.knobs.get("layout.barmode") == "group"
    assert screen.spec["chart"] == "violin"
    assert screen.spec["mapping"], "a picker click should guess a mapping"


def test_an_empty_knobs_dict_emits_no_bucket_sections():
    """SPEC section 5, rule 1: an empty bucket emits nothing at all.

    Not an empty call, not a lonely comment. Three chunks - the source line,
    the chart line, and fig.show().
    """
    code = bench_app.render_code(_spec("bar", mapping={"x": "agency"}))
    for bucket in codegen.BUCKET_ORDER:
        assert f"# --- {bucket}" not in code, bucket
    assert "update_layout" not in code and "update_traces" not in code
    assert code.count("# ---") == 2


def test_the_code_only_ever_names_the_knobs_you_moved(screen):
    """Two knobs out of two thousand, and the panel is five lines long."""
    screen.turn("layout.title.text", "Spend by agency")
    screen.turn("trace.marker.opacity", 0.8)
    body = [line for line in screen.code.splitlines()
            if line.strip() and not line.startswith("#")]
    assert len(body) == 5, screen.code
    assert screen.code.count("update_layout") == 1
    assert screen.code.count("update_traces") == 1


def test_a_knob_at_default_is_absent_across_a_whole_session(screen):
    """The long way round: turn six knobs, clear them all, end up empty.

    Turning and clearing is the loop a human actually does, and the spec has
    to come back to exactly where it started - not to six keys holding None.
    """
    start = json.loads(json.dumps(screen.spec))
    turns = [("layout.title.text", "a"), ("layout.barmode", "group"),
             ("layout.hovermode", "x unified"), ("trace.marker.opacity", 0.5),
             ("layout.showlegend", False), ("layout.margin.t", 60)]
    for path, value in turns:
        screen.turn(path, value)
    assert set(screen.knobs) == {p for p, _ in turns}
    assert codegen.parse(screen.code) == screen.spec

    for path, _value in turns:
        screen.turn(path, None)
    assert screen.knobs == {}
    assert screen.spec == start
    assert screen.code == bench_app.render_code(start)


# =====================================================================
# printed run, for a human
# =====================================================================


def main() -> int:
    import time

    t0 = time.time()
    print(f"trace types covered   : {len(TRACE_TYPES)}  "
          f"(SPEC section 10 item 7 asks for 20)")
    print(f"round-trip battery    : {len(BATTERY)} specs  (asks for 30)")
    print(f"malformed battery     : {len(MALFORMED)} pieces of code  (asks for 15)")

    flat = knobs.flat("bar", DEMO_COLUMNS)
    print(f"knobs generated for a bar : {len(flat)} across "
          f"{len({k.validator for k in flat})} validator classes")

    s = Screen()
    print(f"opening screen        : {len(s.ids)} widgets, knobs={s.knobs}, "
          f"{len(_marked_changed(s.pane))} marked changed")

    s.turn("layout.template", "plotly_dark")
    print(f"turn the template     : stored {s.knobs['layout.template']!r}, "
          f"code is {len(s.code)} chars, figure paper bg "
          f"{s.figure.layout.template.layout.paper_bgcolor}")

    s.turn("layout.title.text", "Spend by agency")
    print(f"turn a knob           : figure title "
          f"{s.figure.layout.title.text!r}, round trip "
          f"{codegen.parse(s.code) == s.spec}")

    s.type_code(s.code.replace('barmode', 'barmode'))    # the same text back
    print(f"hand the code back    : spec unchanged, custom={s.custom}")

    s.type_code("import os\nfig = 1\n")
    total, off = _editors_read_only(s.pane)
    print(f"break the code        : custom={s.custom}, {off}/{total} editors "
          f"read-only, msg={s.message[:44]!r}")
    s.reset()
    print(f"press Reset           : custom={s.custom}, knobs={list(s.knobs)}")

    print(f"\nall of that in {time.time() - t0:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
