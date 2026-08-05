"""
THE BENCH - app.py, driven headlessly.

    python -m pytest tests/test_bench_app.py -q
    python tests/test_bench_app.py                (same checks, prints as it goes)

There is no browser here. Dash callbacks are ordinary functions once you hand
them a callback context, so this file calls `app.sync_spec` and the three render
lanes directly with the arguments Dash would have handed them, and asserts that
every transition SPEC section 8 promises actually happens.

The one that matters most is `test_two_way_sync_converges`. Turn a knob, redraw,
feed the redraw straight back in as if the browser had reported it, and the app
has to go quiet. An app that answers "changed!" to its own output is an app that
spins forever, and that is the single most likely bug in a two-way panel.

TWO THINGS THE HARNESS MODELS THAT IT DID NOT HAVE TO BEFORE
------------------------------------------------------------
1. THREE RENDER CALLBACKS, NOT ONE. `render_chart`, `render_knobs` and
   `render_picker` all fan out from the `bench-spec` store. `Bench.render`
   calls all three, in the order the browser would apply them.
2. THE KNOB PANE IS LAZY. A real first paint materialises Tier 0 and nothing
   else - 39 rows instead of 1,895 - so a Tier 1 knob like
   `trace.marker.opacity` has no widget until you open its bucket. `Bench`
   therefore defaults to `open_all=True`: a pretend browser that has already
   clicked "show everything" on all six buckets, which is the state almost
   every test below is really about. `Bench(open_all=False)` is the honest
   first paint, and the tests that are about the first paint use it.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import plotly.graph_objects as go
import pytest
from dash import no_update
from dash._callback_context import context_value
from dash._utils import AttributeDict

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bench import app as bench_app  # noqa: E402
from bench import codegen, controls, registry  # noqa: E402


# =====================================================================
# THE HARNESS - one screen's worth of Bench state, driven by hand
# =====================================================================


def _widgets(component):
    """Every knob widget in a rendered pane, exactly as Dash would report it.

    Dash hands a pattern-matching callback one entry per component whose id
    matches - including the wrapper Divs, which have no `value` prop and come
    back as None. We reproduce that faithfully, because those Nones are one of
    the ways a naive guard gets fooled.
    """
    ids, values = [], []
    for node in component._traverse():
        cid = getattr(node, "id", None)
        if isinstance(cid, dict) and cid.get("bench") == "knob":
            ids.append(dict(cid))
            values.append(getattr(node, "value", None))
    return ids, values


def _says(component, needle: str) -> bool:
    """Is this string anywhere in the rendered text of a component tree?

    Walking the tree rather than JSON-dumping it, because a dump escapes the
    em dash in the CUSTOM banner and the assertion then lies about why it failed.
    """
    for node in [component, *component._traverse()]:
        kids = getattr(node, "children", None)
        if isinstance(kids, str) and needle in kids:
            return True
        if isinstance(kids, (list, tuple)):
            if any(isinstance(k, str) and needle in k for k in kids):
                return True
    return False


def _editors_disabled(component) -> tuple[int, int]:
    """(how many editors, how many of them are read-only).

    controls.py's toggle is a `dcc.RadioItems`, which carries `disabled` on
    each option rather than on the component, so both spellings count.
    """
    total = off = 0
    for node in component._traverse():
        cid = getattr(node, "id", None)
        if isinstance(cid, dict) and cid.get("bench") == "knob" \
                and cid.get("part") in ("value", "hex"):
            total += 1
            options = getattr(node, "options", None)
            per_option = bool(options) and all(
                isinstance(o, dict) and o.get("disabled") for o in options)
            off += bool(getattr(node, "disabled", False)) or per_option
    return total, off


class Bench:
    """A pretend browser: holds the stores and the widget values on screen.

    `open_all` is the one piece of state the browser now has that it did not
    before. The knob pane is lazy: with nothing opened it materialises Tier 0
    only. `open_all=True` (the default here) stands in for a human who has
    clicked "show everything" on all six buckets, which puts exactly the same
    widgets on screen as the old eager pane - checked: same ids, same values,
    same order.
    """

    def __init__(self, spec=None, open_all=True):
        self.spec = spec or bench_app.blank_spec()
        self.open_all = open_all
        self.opened: dict = {}
        self.echo = {"code": ""}
        self.knob_echo = {"knobs": {}, "sig": None, "vals": None}
        self.picker_sig = None
        self.code = ""
        self.figure = None
        self.pane = None
        self.picker = None
        self.ids: list = []
        self.values: list = []
        self.build_msg = ""
        self.mode = ""
        self.knob_msg = ""
        self.status = []
        self.knob_query = ""
        self.picker_query = ""
        self.renders = 0
        self.pane_rebuilds = 0
        self.render()

    # -- callbacks 2, 3 and 4 -----------------------------------------
    def render(self):
        """Run the three render lanes and apply them the way the browser does."""
        self.opened = ({"key": bench_app.open_key(self.spec),
                        "tokens": list(bench_app.ALL_TIERS_OPEN)}
                       if self.open_all else {})

        (fig, code, status, build_msg, mode, echo) = bench_app.render_chart(
            self.spec, self.echo)
        pane, knob_echo = bench_app.render_knobs(
            self.spec, self.knob_query, self.opened, self.knob_echo)
        pick, picker_sig = bench_app.render_picker(
            self.spec, self.picker_query, self.picker_sig)

        self.renders += 1
        self.figure = fig
        if code is not no_update:
            self.code = code
        if pane is not no_update:
            self.pane = pane
            self.ids, self.values = _widgets(pane)
            self.pane_rebuilds += 1
        if pick is not no_update:
            self.picker = pick
        if picker_sig is not no_update:
            self.picker_sig = picker_sig
        self.status = status
        self.build_msg = build_msg
        self.mode = mode
        if echo is not no_update:
            self.echo = echo
        if knob_echo is not no_update:
            self.knob_echo = knob_echo
        return self

    # -- callback 5: a bucket expander --------------------------------
    def open_bucket(self, bucket, tier=1):
        """Click a bucket's 'show more' / 'show everything', then redraw.

        `open_all` has to go off first, or the next `render` would put every
        token straight back and the click would prove nothing.
        """
        self.open_all = False
        key = bench_app.open_key(self.spec)
        tokens = controls.opened_with(
            bench_app.open_tokens(self.opened, key),
            controls.bucket_id(bucket, controls.PART_BY_TIER[tier]))
        self.opened = {"key": key, "tokens": list(tokens)}
        # A bucket click writes `bench-open` and nothing else, so only the
        # knob lane fires. The chart does not repaint - that is the split.
        pane, knob_echo = bench_app.render_knobs(
            self.spec, self.knob_query, self.opened, self.knob_echo)
        if pane is not no_update:
            self.pane = pane
            self.ids, self.values = _widgets(pane)
            self.pane_rebuilds += 1
        if knob_echo is not no_update:
            self.knob_echo = knob_echo
        return self

    # -- callback 1 ---------------------------------------------------
    def _fire(self, prop_id, **overrides):
        """Call `sync_spec` with a faked callback context, then apply its output.

        Returns the raw (spec, echo, message) so a test can assert on
        `no_update` directly.
        """
        args = dict(
            _chart_clicks=[0] * len(registry.TEMPLATES),
            knob_values=list(self.values),
            draft=None, _blur=None, _reset=None,
            src_kind=self.spec["source"].get("kind", "demo"),
            src_demo=self.spec["source"].get("name", bench_app.START_DEMO),
            _run=None,
            code_value=self.code,
            sql=self.spec["source"].get("sql", ""),
            spec=self.spec, echo=self.echo, knob_echo=self.knob_echo,
        )
        args.update(overrides)
        # Input index 1 is the knob pattern; app.py reads its ids from here.
        inputs_list = [
            [{"id": {"bench": "chart", "key": t.key}, "property": "n_clicks",
              "value": 0} for t in registry.TEMPLATES],
            [{"id": cid, "property": "value", "value": v}
             for cid, v in zip(self.ids, self.values)],
        ]
        context_value.set(AttributeDict(
            triggered_inputs=[{"prop_id": prop_id, "value": None}],
            inputs_list=inputs_list,
        ))
        try:
            spec, echo, message = bench_app.sync_spec(**args)
        finally:
            context_value.set({})

        self.knob_msg = message
        if echo is not no_update:          # sync_spec stamps the KNOB echo
            self.knob_echo = echo
        if spec is not no_update:
            self.spec = spec
            self.render()
        return spec, echo, message

    # -- the four flows, as a human would do them ---------------------
    def click_chart(self, key):
        return self._fire(json.dumps({"bench": "chart", "key": key},
                                     sort_keys=True) + ".n_clicks")

    def set_knob(self, path, value, part="value"):
        """Move one widget, then report every widget the way the browser does."""
        for i, cid in enumerate(self.ids):
            if cid.get("path") == path and cid.get("part") == part:
                self.values[i] = value
                break
        else:
            raise AssertionError(f"no widget for {path!r} part={part!r}")
        return self._fire(
            json.dumps({"bench": "knob", "part": part, "path": path},
                       sort_keys=True) + ".value")

    def report_knobs(self):
        """Tell the server what the widgets say, having changed nothing."""
        return self._fire('{"bench":"knob","part":"value","path":"x"}.value')

    def edit_code(self, text):
        return self._fire("bench-code-draft.data", draft=text)

    def reset(self):
        return self._fire("bench-reset.n_clicks")

    def set_source(self, kind="demo", name=None, sql=None):
        return self._fire("bench-src-demo.value" if kind == "demo"
                          else "bench-src-run.n_clicks",
                          src_kind=kind, src_demo=name, sql=sql)

    # -- readers ------------------------------------------------------
    def widget(self, path, part="value"):
        for cid, value in zip(self.ids, self.values):
            if cid.get("path") == path and cid.get("part") == part:
                return value
        raise AssertionError(f"no widget for {path!r}")

    def has_widget(self, path, part="value"):
        return any(cid.get("path") == path and cid.get("part") == part
                   for cid in self.ids)

    def status_text(self):
        return json.dumps(self.status, default=str)

    def figure_json(self):
        return self.figure.to_dict()


@pytest.fixture()
def bench():
    return Bench()


# =====================================================================
# 0. IT STARTS
# =====================================================================


def test_layout_builds_and_ids_are_unique():
    """A duplicate id is a silent, undebuggable Dash failure. Prove there is none."""
    from dash import _validate

    _validate.validate_layout(bench_app.app.layout, bench_app.app.layout)
    ids = [str(getattr(n, "id", None)) for n in bench_app.app.layout._traverse()
           if getattr(n, "id", None) is not None]
    assert len(ids) == len(set(ids)), "duplicate component ids in the layout"
    # The pane in the layout is the LAZY first paint - Tier 0 and nothing else -
    # so counting ids no longer proves it rendered. Naming what has to be in it
    # does, and it is the better check: this used to pass on 14,720 ids without
    # ever asking whether the mapping slots were among them.
    assert len(ids) > 200, f"only {len(ids)} ids - the pane did not render"
    for path in ("mapping.x", "layout.title.text", "layout.barmode"):
        assert any(f"'path': '{path}'" in i for i in ids), path
    for pane in ("bench-picker", "bench-figure", "bench-code", "bench-knobs",
                 "bench-status", "bench-src-run"):
        assert pane in ids, pane


def test_the_chart_line_is_honest_and_leaves_codegen_alone():
    """Only the four genuinely-bare px charts print as `px.<name>(df, ...)`.

    And `codegen.PX_CHARTS` is exactly where we found it afterwards - app.py
    narrows it for the length of a render and puts it back, rather than
    rewriting another module's global on import.
    """
    before = set(codegen.PX_CHARTS)
    spec = bench_app.blank_spec()
    assert "fig = px.bar(df" in bench_app.render_code(spec)
    for key, expected in [("violin_split", 'bench.registry.build("violin_split"'),
                          ("sankey", 'bench.registry.build("sankey"'),
                          ("pie", 'bench.registry.build("pie"')]:
        code = bench_app.render_code({**spec, "chart": key, "mapping": {}})
        assert expected in code, f"{key} printed a px call it was not built with"
    assert set(codegen.PX_CHARTS) == before, "codegen's global was left rewritten"
    assert registry.PX_PURE == {"area", "bar", "density_contour", "strip"}


def test_every_callback_is_registered():
    """Eight server callbacks and the one clientside debounce.

    Named rather than counted, because the whole point of the split is WHICH
    callback owns which pane. A count alone would have gone green on a
    render lane that quietly grew a second Output back.
    """
    from dash import _callback

    outputs = {str(k) for k in bench_app.app.callback_map}
    assert len(outputs) == 8, sorted(outputs)
    for owns in ("bench-spec.data",                 # sync_spec, the one writer
                 "bench-figure.figure",             # render_chart, the fast lane
                 "bench-knobs.children",            # render_knobs, the slow lane
                 "bench-picker.children",           # render_picker
                 "bench-open.data",                 # grow_open
                 "bench-src-demo-box.style",        # source_face
                 "bench-src-table.options",         # find_tables
                 "bench-download.data"):            # export_chart
        assert any(owns in key for key in outputs), owns
    assert len(_callback.GLOBAL_CALLBACK_LIST) == 1   # plus the clientside debounce


def test_the_chart_does_not_wait_on_the_knob_pane():
    """The split, stated as a test: the fast lane owns no expensive Output.

    `render_chart` must not be able to return the figure only once the pane
    and the picker are built. That was the bug - eight Outputs off one Input,
    268ms and 4,128 KB for a chart click, 94% of it Output 3.
    """
    fast = next(cb for key, cb in bench_app.app.callback_map.items()
                if "bench-figure.figure" in key)
    fast_outputs = {str(o) for o in fast["output"]}
    for slow in ("bench-knobs.children", "bench-picker.children"):
        assert not any(slow in o for o in fast_outputs), fast_outputs


def test_opening_screen_is_coherent(bench):
    """The first paint: a real figure, canonical code, and a full knob pane."""
    assert isinstance(bench.figure, go.Figure)
    assert bench.figure.data, "the opening chart drew nothing"
    assert bench.code.startswith("# --- data")
    assert codegen.parse(bench.code) is not None, "the opening code is not canonical"
    assert bench.pane_rebuilds == 1
    assert len(bench.ids) > 500, f"only {len(bench.ids)} knob widgets"
    assert bench.has_widget("mapping.x") and bench.has_widget("mapping.y")


def test_the_real_first_paint_is_tier_zero_and_nothing_else():
    """No `open_all`: what a browser actually receives when the page opens.

    This is the payload fix, asserted rather than described. The eager pane
    was 1,895 knob rows and 3,808 KB of JSON on every repaint; the lazy one is
    Tier 0. Tier 1 and Tier 2 are not hidden behind a shut <details> - they do
    not exist as components, which is why they stop being shipped.
    """
    from dash._utils import to_json

    first = Bench(open_all=False)
    everything = Bench(open_all=True)
    assert 0 < len(first.ids) < len(everything.ids) / 10, (
        f"{len(first.ids)} widgets on a first paint vs "
        f"{len(everything.ids)} with everything open")

    # the mapping slots and the twenty ATLAS knobs are Tier 0, so they are there
    for path in ("mapping.x", "mapping.y", "layout.title.text", "layout.barmode",
                 "layout.hovermode", "layout.template"):
        assert first.has_widget(path), path
    # and a Tier 1 knob is genuinely absent until you ask for it
    assert not first.has_widget("trace.marker.opacity")
    first.open_bucket("MARK", tier=1)
    assert first.has_widget("trace.marker.opacity"), (
        "opening MARK did not materialise its Tier 1")

    small = len(to_json(Bench(open_all=False).pane).encode())
    big = len(to_json(everything.pane).encode())
    assert small < big / 10, f"{small:,} bytes vs {big:,}"


# =====================================================================
# 1. PICKER CLICK  (SPEC section 8, callback 1)
# =====================================================================


def test_picker_click_changes_chart_mapping_and_code(bench):
    bench.click_chart("box_compare")
    assert bench.spec["chart"] == "box_compare"
    assert bench.spec["knobs"] == {}, "the old chart's knobs were carried over"
    assert bench.spec["mapping"].get("y"), "auto_map left the chart undrawable"
    assert 'bench.registry.build("box_compare"' in bench.code
    assert isinstance(bench.figure, go.Figure)
    assert bench.pane_rebuilds == 2, "the knob pane was not rebuilt for a new chart"


def test_picker_click_on_an_undrawable_chart_says_why(bench):
    """SPEC section 6: grey-out-with-a-reason, all the way through to the pane."""
    bench.click_chart("sankey")            # the demo frame has one category column
    assert bench.spec["chart"] == "sankey"
    assert "source column" in bench.knob_msg, bench.knob_msg
    assert "this result has" in bench.knob_msg
    # the middle pane says it too, rather than going blank
    assert bench.build_msg, "the chart pane went quiet about an undrawable chart"
    assert isinstance(bench.figure, go.Figure)


@pytest.mark.parametrize("key", sorted(registry.CHARTS))
def test_every_chart_either_draws_or_explains_itself(key):
    """All 145. None of them may raise, ever - SPEC section 10, rule 2."""
    spec = bench_app.blank_spec()
    df, meta = bench_app.get_frame(spec["source"])
    spec["chart"] = key
    spec["mapping"] = registry.auto_map(df, registry.CHARTS[key])
    fig, message = bench_app.figure_for(spec, df, meta)
    assert isinstance(fig, go.Figure)
    if not fig.data:
        # An empty figure is only allowed when it carries an explanation.
        assert fig.layout.annotations, f"{key}: blank figure with nothing said"
        assert message or registry.CHARTS[key].blocked, f"{key}: silent blank"


# =====================================================================
# 2. KNOB TURN  (SPEC section 8, callback 2)
# =====================================================================


def test_turning_a_knob_writes_the_spec_the_code_and_the_figure(bench):
    bench.set_knob("layout.title.text", "Spend by agency")
    assert bench.spec["knobs"]["layout.title.text"] == "Spend by agency"
    assert 'title_text="Spend by agency"' in bench.code
    assert bench.figure.layout.title.text == "Spend by agency"


def test_turning_a_knob_does_not_rebuild_the_knob_pane(bench):
    """SPEC section 8, rule 2, word for word: '(not the knob panel)'."""
    before = bench.pane_rebuilds
    bench.set_knob("layout.title.text", "one")
    bench.set_knob("layout.title.text", "two")
    assert bench.pane_rebuilds == before, (
        "the pane was rebuilt under the control the user is holding")


def test_clearing_a_knob_removes_it_from_the_spec(bench):
    """SPEC section 3: only non-default values live in `knobs`."""
    bench.set_knob("layout.title.text", "temporary")
    assert "layout.title.text" in bench.spec["knobs"]
    bench.set_knob("layout.title.text", "")
    assert "layout.title.text" not in bench.spec["knobs"], (
        "a cleared knob stayed in the spec, so the code will never shrink again")
    assert "title_text" not in bench.code


def test_a_bad_knob_value_is_a_sentence_not_a_broken_chart(bench):
    bench.set_knob("layout.hovermode", "sideways")
    assert "layout.hovermode" not in bench.spec["knobs"]
    assert "hovermode" in bench.knob_msg and bench.knob_msg
    assert bench.figure.data, "a rejected value took the chart down with it"


def test_a_mapping_slot_is_a_mapping_not_a_knob(bench):
    """SPEC section 3: `mapping` is separate because its values come from the data."""
    bench.set_knob("mapping.color", "agency")
    assert bench.spec["mapping"]["color"] == "agency"
    assert "mapping.color" not in bench.spec["knobs"]
    assert 'color="agency"' in bench.code


def test_a_many_slot_takes_a_list_of_columns(bench):
    """A correlation matrix wants ALL the numbers, so its slot is a multi-select.

    `controls.coerce` would join a list into Plotly's 'a+b+c' flaglist string
    here, which a mapping slot is not - so app.py coerces mapping slots itself.
    """
    bench.set_source("demo", "numeric_block")
    bench.click_chart("corr_matrix")
    assert isinstance(bench.spec["mapping"]["values"], list)
    assert len(bench.spec["mapping"]["values"]) >= 2
    picked = ["inspections", "violations", "fines"]
    bench.set_knob("mapping.values", picked)
    assert bench.spec["mapping"]["values"] == picked
    assert "+" not in json.dumps(bench.spec["mapping"]), "a list got flaglist-joined"
    assert bench.figure.data


def test_the_knob_search_box_cuts_every_tier(bench):
    """SPEC section 4.3's real answer to 'I know there's a setting for X'."""
    everything = len(bench.ids)
    bench.knob_query = "gridcolor"
    bench.render()
    assert bench.pane_rebuilds == 2, "the search did not rebuild the pane"
    assert 0 < len(bench.ids) < everything / 4
    assert bench.has_widget("layout.yaxis.gridcolor"), (
        "a Tier 1 knob did not surface in the search")
    bench.knob_query = ""
    bench.render()
    assert len(bench.ids) == everything, "clearing the search lost knobs"


def test_the_picker_search_narrows_the_chart_list(bench):
    def buttons(node):
        return sum(1 for n in node._traverse()
                   if isinstance(getattr(n, "id", None), dict)
                   and getattr(n, "id").get("bench") == "chart")

    everything = buttons(bench.picker)
    assert everything == len(registry.TEMPLATES)
    bench.picker_query = "sankey"
    bench.render()
    assert 0 < buttons(bench.picker) < 10, "the chart search did not narrow anything"


def test_one_pattern_callback_covers_every_knob(bench):
    """There is exactly one knob Input, and it catches thousands of widgets."""
    knob_inputs = [i for cb in bench_app.app.callback_map.values()
                   for i in cb["inputs"] if "knob" in str(i.get("id"))]
    assert len(knob_inputs) == 1, knob_inputs
    assert len(bench.ids) > 500


def test_the_all_input_only_carries_what_is_on_screen(bench):
    """The payload fix, from the other end: ALL matches components, not knobs.

    `Input({"bench": "knob", "path": ALL, "part": ALL}, "value")` catches every
    matching component that EXISTS. With the pane lazy, an unopened tier has
    no components, so the browser stops posting its ~4,000 entries - which was
    668 KB of request body on every single knob turn.
    """
    first = Bench(open_all=False)
    assert len(first.ids) < len(bench.ids) / 10
    # and what it does carry is exactly what controls.py says it materialised
    on_screen = set(controls.materialised(first.pane))
    carried = {cid["path"] for cid in first.ids
               if cid.get("part") in ("value", "hex")}
    assert carried == on_screen, carried ^ on_screen


# =====================================================================
# 3. CODE EDIT  (SPEC section 8, callback 3)
# =====================================================================


def test_editing_the_code_moves_the_knobs(bench):
    """SPEC section 10, rule 5: editing the code updates chart AND knobs."""
    edited = bench.code.replace(
        "\nfig.show()",
        '\n# --- FRAME ---\nfig.update_layout(title_text="typed by hand")'
        "\n\nfig.show()")
    bench.edit_code(edited)
    assert bench.spec["custom_code"] is None, "canonical code was read as custom"
    assert bench.spec["knobs"]["layout.title.text"] == "typed by hand"
    assert bench.figure.layout.title.text == "typed by hand"
    # and the widget itself moved
    assert bench.widget("layout.title.text") == "typed by hand", (
        "the code changed the spec but the knob pane still shows the old value")


def test_broken_code_drops_to_custom_mode_and_still_draws(bench):
    """SPEC section 1: CUSTOM mode is a feature, not a failure."""
    custom = (
        "df = bench.data.frame({'kind': 'demo', 'name': 'category'})\n"
        "import plotly.graph_objects as G\n"          # an import: not canonical
        "fig = G.Figure(G.Bar(x=df['agency'], y=df['spend'], marker_color='red'))\n"
        "fig.show()\n"
    )
    bench.edit_code(custom)
    assert bench.spec["custom_code"] == custom
    assert "CUSTOM" in bench.knob_msg
    assert bench.figure.data, "CUSTOM mode stopped drawing"
    assert bench.figure.data[0].marker.color == "red", "it drew the wrong thing"
    # the knobs go read-only, behind the banner SPEC section 1 names
    assert _says(bench.pane, bench_app.CUSTOM_BANNER), "no CUSTOM banner on the pane"
    total, disabled = _editors_disabled(bench.pane)
    assert total > 100 and disabled == total, (
        f"{disabled} of {total} knob editors are read-only; all of them should be")


def test_reset_returns_to_canonical(bench):
    bench.edit_code("fig = 1 +\n")             # a syntax error
    assert bench.spec["custom_code"] is not None
    bench.reset()
    assert bench.spec["custom_code"] is None
    assert codegen.parse(bench.code) is not None
    assert bench.figure.data, "Reset left the chart empty"
    assert not _says(bench.pane, bench_app.CUSTOM_BANNER)
    total, disabled = _editors_disabled(bench.pane)
    assert total > 100 and disabled == 0, "the knobs stayed read-only after Reset"


def test_code_naming_an_unknown_chart_is_custom_not_a_crash(bench):
    bench.edit_code(bench.code.replace("px.bar(", "px.nonsense("))
    assert bench.spec["custom_code"] is not None
    assert "not a chart in the registry" in bench.knob_msg


def test_an_empty_code_box_is_ignored_and_says_so(bench):
    before = json.dumps(bench.spec, sort_keys=True)
    spec, _echo, message = bench.edit_code("   \n  ")
    assert spec is no_update
    assert "Reset" in message
    assert json.dumps(bench.spec, sort_keys=True) == before


def test_hostile_code_never_raises(bench):
    for source in ["", "]]]", "def f(:", "\x00", "fig = ", "lambda: 1", "0/0",
                   "raise SystemExit(1)", "fig = 'not a figure'"]:
        bench.spec = bench_app.blank_spec()
        bench.render()
        bench.edit_code(source)                # must not raise
        assert isinstance(bench.figure, go.Figure)


def test_an_endless_loop_in_the_code_panel_is_stopped(bench):
    """CUSTOM mode runs your code, so `while True:` has to be survivable.

    The panel re-runs 600ms after you stop typing, so without a deadline one
    stray loop takes the whole app with it. Five seconds, then it is killed and
    the pane says so.
    """
    import time as _time

    t0 = _time.time()
    bench.edit_code("while True:\n    pass\n")
    elapsed = _time.time() - t0
    assert elapsed < bench_app.CUSTOM_TIMEOUT_S + 5, f"took {elapsed:.1f}s"
    assert "TimeoutError" in bench.build_msg, bench.build_msg
    assert isinstance(bench.figure, go.Figure)
    bench.reset()
    assert bench.figure.data, "Reset did not bring the chart back"


# =====================================================================
# 4. SOURCE CHANGE  (SPEC section 8, callback 4)
# =====================================================================


def test_changing_the_source_revalidates_the_mapping_and_says_what_it_cleared(bench):
    bench.set_source("demo", "flow")           # source/target/amount, no 'agency'
    assert bench.spec["source"] == {"kind": "demo", "name": "flow"}
    assert bench.knob_msg, "columns vanished and nothing was said about it"
    assert "cleared" in bench.knob_msg
    for slot, column in bench.spec["mapping"].items():
        if isinstance(column, str):
            assert column in bench.spec and True or True  # placeholder, see below
    df, _meta = bench_app.get_frame(bench.spec["source"])
    for column in bench.spec["mapping"].values():
        if isinstance(column, str):
            assert column in list(df.columns), f"{column} is not in the new result"
    assert bench.pane_rebuilds >= 2, "the pane kept the old columns in its dropdowns"


def test_a_refused_warehouse_query_shows_the_reason_and_the_lane(bench):
    """The guarded read lane is never routed around - a refusal is a message."""
    bench.set_source("warehouse", sql="DROP TABLE x")
    assert bench.spec["source"]["kind"] == "warehouse"
    assert bench.knob_msg, "a refused query said nothing"
    status = bench.status_text()
    assert "refused" in status, status
    assert isinstance(bench.figure, go.Figure)


def test_the_status_bar_never_loses_lane_rows_or_as_of(bench):
    """SPEC section 8's non-negotiables, checked on every kind of outcome."""
    for source in [{"kind": "demo", "name": "category"},
                   {"kind": "demo", "name": "nope"},
                   {"kind": "warehouse", "sql": ""},
                   {"kind": "sideways"}]:
        _df, meta = bench_app.get_frame(source)
        text = json.dumps(bench_app.status_bar(meta), default=str)
        assert "lane" in text and "rows" in text and "data as of" in text, source


def test_truncation_is_shouted_about():
    text = json.dumps(bench_app.status_bar(
        {"ok": True, "lane": "enforced", "rows": 10000, "truncated": True}),
        default=str)
    assert "TRUNCATED" in text and "10,000" in text


# =====================================================================
# THE FRAME CACHE - a knob turn must not re-run your SQL
# ---------------------------------------------------------------------
# Nothing here opens a connection. `viz.sqlrun.run` is stood up as a
# counting stub and put straight back, which is the only honest way to
# prove "it did not re-query" with no warehouse to not-query.
# =====================================================================


@pytest.fixture()
def counted_warehouse():
    """A fake read lane that counts calls. Yields (source, the counter)."""
    import pandas as pd

    from bench import data
    from viz import sqlrun

    calls = {"n": 0}
    source = {"kind": "warehouse", "sql": "SELECT AGENCY, SPEND FROM T"}

    def fake_run(sql, limit_rows=sqlrun.DEFAULT_LIMIT_ROWS):
        calls["n"] += 1
        return (pd.DataFrame({"AGENCY": ["a", "b", "c"], "SPEND": [1.0, 2.0, 3.0]}),
                {"rows": 3, "truncated": False, "elapsed_s": 9.4,
                 "warehouse": "SERVE_WH", "lane": "enforced",
                 "as_of": "2026-08-01 00:00:00", "budget": "", "claim_refs": []})

    real_run, real_lane = sqlrun.run, sqlrun.lane_status
    sqlrun.run = fake_run
    sqlrun.lane_status = lambda: {"lane": "enforced", "notes": []}
    data.invalidate(source)
    try:
        yield source, calls
    finally:
        sqlrun.run = real_run
        sqlrun.lane_status = real_lane
        data.invalidate(source)


def test_turning_a_knob_causes_zero_warehouse_round_trips(counted_warehouse):
    """A bare SELECT 1 measured at 9.4s on this box. Twenty turns is 3 minutes."""
    source, calls = counted_warehouse
    bench = Bench(spec={**bench_app.blank_spec(), "source": source,
                        "mapping": {"x": "AGENCY", "y": "SPEND", "color": None}})
    assert calls["n"] == 1, "the first paint did not run the query at all"
    assert bench.figure.data, "the warehouse chart drew nothing"

    calls["n"] = 0
    for i in range(20):
        bench.set_knob("layout.title.text", f"turn {i}")
    assert calls["n"] == 0, (
        f"{calls['n']} warehouse round trip(s) for 20 knob turns — "
        "at 9.4s each that is the whole afternoon")


def test_pressing_run_really_re_runs_the_same_sql(counted_warehouse):
    """The cache moved into data.py, so `refresh` has to be FORWARDED.

    `app.get_frame` used to hold its own dict and pop it on refresh. It does
    not any more, so a `get_frame` that swallowed `refresh=` would leave RUN
    serving the cached answer forever - a button that visibly does nothing.
    No live-warehouse test catches this; they all skip.
    """
    source, calls = counted_warehouse
    bench_app.get_frame(source)
    calls["n"] = 0
    bench_app.get_frame(source)
    assert calls["n"] == 0, "the cache is not in front of the read lane at all"
    bench_app.get_frame(source, refresh=True)
    assert calls["n"] == 1, "RUN did not reach the read lane"


def test_the_status_bar_never_claims_a_query_it_did_not_run(counted_warehouse):
    """SPEC section 7.1: a cached hit keeps the ORIGINAL elapsed_s and says so."""
    source, _calls = counted_warehouse
    _df, first = bench_app.get_frame(source)
    _df, again = bench_app.get_frame(source)
    assert first["cached"] is False and again["cached"] is True
    assert again["elapsed_s"] == first["elapsed_s"] == 9.4

    fresh = json.dumps(bench_app.status_bar(first), default=str)
    cached = json.dumps(bench_app.status_bar(again), default=str)
    assert "9.40s" in fresh and "cached" not in fresh, fresh
    assert "9.40s" in cached and "cached" in cached, cached
    assert "ORIGINAL" in cached, "the chip does not explain the 9.40s it just showed"


def test_drawing_every_chart_leaves_the_cached_frame_untouched():
    """`get_frame` hands out the cached frame ITSELF (copy=False).

    That is the right call on a render path - a copy of a 100k-row result is
    1.4ms per repaint for nobody's benefit - but it only holds while every
    builder copies before it mutates. 145 charts against one frame, and the
    frame has to come out the other side identical.
    """
    source = {"kind": "demo", "name": "category"}
    df, meta = bench_app.get_frame(source)
    before = df.copy(deep=True)
    for key in sorted(registry.CHARTS):
        spec = dict(bench_app.blank_spec(), chart=key,
                    mapping=registry.auto_map(df, registry.CHARTS[key]))
        bench_app.figure_for(spec, df, meta)
    after, _meta = bench_app.get_frame(source)
    assert before.equals(after), "a chart builder edited the cached frame"


def test_the_custom_code_panel_cannot_poison_the_cached_frame(bench):
    """The render path reads the cached frame in place. Custom code must not."""
    bench.edit_code(
        "df = bench.data.frame({'kind': 'demo', 'name': 'category'})\n"
        "import plotly.express as PX\n"
        "df['agency'] = 'POISONED'\n"
        "fig = PX.bar(df, x='agency', y='spend')\n")
    assert bench.spec["custom_code"] is not None
    after, _meta = bench_app.get_frame({"kind": "demo", "name": "category"})
    assert "POISONED" not in list(after["agency"]), (
        "custom code edited the frame the cache is holding")


# =====================================================================
# LOADING FEEDBACK - slow has to read as WORKING, not as BROKEN
# =====================================================================


def _find(component, **props):
    """Every node in the layout whose props all match."""
    out = []
    for node in [component, *component._traverse()]:
        if all(getattr(node, k, None) == v for k, v in props.items()):
            out.append(node)
    return out


def test_the_figure_and_the_knob_pane_both_sit_in_a_spinner():
    """A repaint that takes longer than a blink must show something moving."""
    from dash import dcc as _dcc

    spinners = [n for n in bench_app.app.layout._traverse()
                if isinstance(n, _dcc.Loading)]
    ids = {getattr(n, "id", None) for n in spinners}
    assert "bench-figure-loading" in ids, ids
    assert "bench-knobs-loading" in ids, ids
    for node in spinners:
        assert node.delay_show and node.delay_show <= 400, (
            f"{node.id} waits {node.delay_show}ms before it admits it is working")
    # and the thing being waited on really is inside it
    inside = {str(getattr(n, "id", "")) for s in spinners for n in s._traverse()}
    assert "bench-figure" in inside and "bench-knobs" in inside, inside


def test_the_run_button_disables_itself_and_says_what_it_is_doing():
    """A 9.4s query behind a live-looking button is a query you fire twice."""
    # `running` rides on the DEPENDENCY, not on callback_map - it is applied in
    # the browser, which is the only place that knows a call is still in flight.
    dep = next(d for d in bench_app.app._callback_list
               if "bench-spec.data" in str(d.get("output")))
    running = dep.get("running")
    assert running, "sync_spec has no `running` spec, so RUN never changes"
    text = json.dumps(running, default=str)
    assert "bench-src-run" in text and "disabled" in text, running
    assert "RUNNING SQL" in text, running
    assert "'RUN'" in text or '"RUN"' in text, "the button never says RUN again"


def test_a_bug_in_a_render_lane_lands_on_the_screen_not_in_the_terminal(monkeypatch):
    """The pane going dark with the reason only in a server log is the failure
    mode this app was reported for. Every lane has to answer with words."""
    def boom(*_a, **_k):
        raise RuntimeError("deliberate")

    spec = bench_app.blank_spec()

    monkeypatch.setattr(bench_app, "figure_for", boom)
    fig, _code, status, msg, mode, _echo = bench_app.render_chart(spec, {})
    assert isinstance(fig, go.Figure)
    assert "deliberate" in msg and "RuntimeError" in msg, msg
    assert "deliberate" in json.dumps(fig.to_dict(), default=str)
    assert json.dumps(status, default=str), "the badges vanished with the error"
    assert json.dumps(mode, default=str)
    monkeypatch.undo()

    monkeypatch.setattr(bench_app, "knob_pane", boom)
    pane, echo = bench_app.render_knobs(spec, "", {}, {})
    # The signature is CLEARED, not kept. It used to be `no_update`, which is
    # what made the error sticky - see the test below.
    assert echo == {"knobs": {}, "sig": None, "vals": None}
    assert "deliberate" in json.dumps(pane, default=str)
    monkeypatch.undo()

    monkeypatch.setattr(bench_app, "picker", boom)
    pick, sig = bench_app.render_picker(spec, "", None)
    assert sig is None
    assert "deliberate" in json.dumps(pick, default=str)


def test_an_error_in_a_render_lane_is_not_sticky(monkeypatch):
    """You have to be able to get OUT of the red box.

    Both slow lanes skip their work when the state they are handed matches the
    signature of what they last drew. On the error path they used to leave that
    signature alone - so the store still described the pane that BUILT, and
    coming back to that exact state matched, returned `no_update`, and left the
    error where the knobs should be while the chart drew perfectly beside it.

    Reproduced with a pane that raises for one chart: draw `bar`, break on
    `box_compare`, click `bar` again - and the red box stayed. Clearing the
    signature is the fix, and this is the receipt.
    """
    def boom(*_a, **_k):
        raise RuntimeError("deliberate")

    good = bench_app.blank_spec()
    bad = dict(good, chart="box_compare")

    # --- the knob pane ------------------------------------------------
    pane, echo = bench_app.render_knobs(good, "", {}, {})
    assert pane is not no_update and echo["sig"] is not None

    monkeypatch.setattr(bench_app, "knob_pane", boom)
    err_pane, err_echo = bench_app.render_knobs(bad, "", {}, echo)
    monkeypatch.undo()
    assert "deliberate" in json.dumps(err_pane, default=str)

    # the browser applies what the lane wrote - that IS the bug or the fix
    back, _echo = bench_app.render_knobs(good, "", {}, err_echo)
    assert back is not no_update, "the knob pane is stuck showing an error"
    assert "deliberate" not in json.dumps(back, default=str)

    # --- the picker ---------------------------------------------------
    pick, sig = bench_app.render_picker(good, "", None)
    assert pick is not no_update and sig is not None

    monkeypatch.setattr(bench_app, "picker", boom)
    err_pick, err_sig = bench_app.render_picker(bad, "", sig)
    monkeypatch.undo()
    assert "deliberate" in json.dumps(err_pick, default=str)

    back_pick, _sig = bench_app.render_picker(good, "", err_sig)
    assert back_pick is not no_update, "the picker is stuck showing an error"
    assert "deliberate" not in json.dumps(back_pick, default=str)


def test_a_bug_in_sync_spec_is_a_sentence_not_a_500(monkeypatch):
    def boom(*_a, **_k):
        raise RuntimeError("deliberate")

    monkeypatch.setattr(bench_app, "_apply_reset", boom)
    bench = Bench()
    spec, _echo, message = bench.reset()
    assert spec is no_update
    assert "deliberate" in message and "RuntimeError" in message, message


# =====================================================================
# THE LAZY PANE - opening a tier, and the echo that has to come with it
# =====================================================================


def test_opening_a_tier_does_not_read_as_a_human_turning_every_knob():
    """A materialised tier arrives full of widgets showing their defaults.

    If the echo were not stamped in the SAME return as the pane, every one of
    those would report in as a value the human chose, and the spec would gain
    a hundred knobs nobody touched.
    """
    bench = Bench(open_all=False)
    assert bench.spec["knobs"] == {}
    bench.open_bucket("MARK", tier=1)
    assert bench.has_widget("trace.marker.opacity"), "MARK Tier 1 did not appear"
    spec, _echo, message = bench.report_knobs()
    assert spec is no_update, "opening a tier was read as a hundred knob turns"
    assert message == ""
    assert bench.spec["knobs"] == {}


def test_the_open_token_set_belongs_to_one_pane():
    """Tokens from the chart you left must not silently re-inflate the next one."""
    spec = bench_app.blank_spec()
    store = {"key": bench_app.open_key(spec),
             "tokens": list(bench_app.ALL_TIERS_OPEN)}
    assert bench_app.open_tokens(store, bench_app.open_key(spec))
    other = dict(spec, chart="violin")
    assert bench_app.open_tokens(store, bench_app.open_key(other)) == ()
    custom = dict(spec, custom_code="fig = 1")
    assert bench_app.open_tokens(store, bench_app.open_key(custom)) == ()


def _bucket_click(cid, store, spec, query=""):
    """Fire `grow_open` the way a click on one bucket id would."""
    context_value.set(AttributeDict(
        triggered_inputs=[{"prop_id": f"{json.dumps(cid, sort_keys=True)}"
                                      ".n_clicks", "value": 1}],
        triggered_prop_ids={"x.n_clicks": cid},
        inputs_list=[[]]))
    try:
        return bench_app.grow_open([1], store, spec, query)
    finally:
        context_value.set({})


def test_a_bucket_click_grows_the_open_set_and_a_body_click_does_not():
    """`grow_open` is the only writer of the store, so it has to be exact."""
    spec = bench_app.blank_spec()
    key = bench_app.open_key(spec)

    def click(cid, store):
        return _bucket_click(cid, store, spec)

    store = click(controls.bucket_id("MARK", "section"), {})
    assert store == {"key": key, "tokens": ["MARK:1"]}
    store = click(controls.bucket_id("SCALE", "all"), store)
    # "show everything" implies "show more" - an unbuilt Tier 1 under a built
    # Tier 2 would be a hole you could see through
    assert store["tokens"] == ["MARK:1", "SCALE:1", "SCALE:2"]
    assert click(controls.bucket_id("MARK", "body"), store) is no_update


def test_clicking_a_widget_inside_data_does_not_rebuild_the_pane():
    """The click that used to get eaten, and why it is this one.

    `html.Details` renders `<details onClick={n_clicks + 1}>` - checked against
    the installed bundle - and React's onClick bubbles, so opening the
    `mapping.x` dropdown fires n_clicks on the DATA bucket wrapped around it.
    DATA is the only bucket open on a first paint, so this is the FIRST thing
    anybody does with the pane.

    It used to add "DATA:1" - a tier `knob_tree` leaves empty on purpose,
    because DATA holds the chart's own mapping slots and nothing behind them -
    change `bench-open`, and rebuild a pane that came back with the same 70
    widgets holding the same values. The menu closed, the click did nothing,
    and the second click worked.
    """
    spec = bench_app.blank_spec()
    assert "DATA" in controls.OPEN_BY_DEFAULT, "this test is about an open bucket"
    tree = bench_app.knob_tree(spec, ["agency", "spend"])
    assert not tree["DATA"][1] and not tree["DATA"][2], (
        "DATA grew deeper tiers - the premise of this test moved")

    assert _bucket_click(controls.bucket_id("DATA", "section"), {}, spec) is no_update

    # and belt-and-braces: even if a token for an empty tier did arrive, the
    # pane it produces is the pane that is already on screen
    pane, echo = bench_app.render_knobs(spec, "", {}, {})
    stale = {"key": bench_app.open_key(spec), "tokens": ["DATA:1"]}
    again, _echo = bench_app.render_knobs(spec, "", stale, echo)
    assert _widgets(again if again is not no_update else pane) == _widgets(pane)


def test_a_bucket_click_while_searching_asks_for_nothing():
    """A search draws no tier expanders at all, so every bucket id under one
    is a <details> that a click on a row bubbled up to.

    `controls.accordion` folds every hit from every tier into Tier 0 when a
    query is on and never reads `opened` - so a token arriving mid-search
    rebuilt a byte-identical pane and took the open dropdown with it.
    Reproduced on a search for "grid": 136 widgets in, the same 136 out.
    """
    spec = bench_app.blank_spec()
    query = "grid"

    # nothing on screen under a search is a tier expander
    pane = bench_app.knob_pane(spec, ["agency", "spend"], query, ())
    parts = {n.id.get("part") for n in pane._traverse()
             if isinstance(getattr(n, "id", None), dict)
             and n.id.get("bench") == "bucket"}
    assert parts <= {"section", "body"}, f"a search drew a tier expander: {parts}"

    assert _bucket_click(controls.bucket_id("SCALE", "section"), {}, spec,
                         query) is no_update

    # ...and the second guard: `opened` is not in the signature under a search,
    # so even a token that got there another way cannot rebuild the pane
    first, echo = bench_app.render_knobs(spec, query, {}, {})
    assert first is not no_update
    opened = {"key": bench_app.open_key(spec), "tokens": ["SCALE:1"]}
    again, _echo = bench_app.render_knobs(spec, query, opened, echo)
    assert again is no_update, "a searched pane rebuilt for an open-tier token"


def test_materialisable_names_only_tiers_that_hold_knobs():
    """The filter that makes the DATA click a no-op, stated directly."""
    for chart in ("bar", "scatter", "violin"):
        tokens = bench_app.materialisable({"chart": chart})
        assert tokens, chart
        assert "DATA:1" not in tokens and "DATA:2" not in tokens, chart
        tree = bench_app.knob_tree({"chart": chart}, ["a", "b"])
        for bucket in controls.BUCKET_ORDER:
            for tier in (1, 2):
                token = controls.open_token(bucket, tier)
                has = bool(tree[bucket][tier])
                assert (token in tokens) is has, f"{chart} {token} {has}"
    # a chart nobody has heard of is "no opinion", never a swallowed click
    assert bench_app.materialisable({"chart": "not_a_chart"}) is None


# =====================================================================
# THE ONE THAT MATTERS - the two-way sync cannot loop
# =====================================================================


def test_two_way_sync_converges(bench):
    """Feed the app its own output. It has to go quiet.

    This is the infinite-loop test. After any change we redraw, and the redraw
    puts new text in the code box and new values in the knob widgets. The
    browser then reports those back. If the app treats its own writing as a
    human edit, it writes again, and the two panes shout at each other forever.
    """
    bench.set_knob("layout.title.text", "Spend by agency")

    for round_trip in range(5):
        # the browser reports the code box, unchanged since we wrote it
        spec, _echo, _msg = bench.edit_code(bench.code)
        assert spec is no_update, f"round {round_trip}: the code echo was re-applied"
        # the browser reports every knob widget, unchanged since we wrote it
        spec, _echo, _msg = bench.report_knobs()
        assert spec is no_update, f"round {round_trip}: the knob echo was re-applied"

    assert bench.spec["knobs"] == {"layout.title.text": "Spend by agency"}


def test_the_echo_guard_still_lets_a_real_edit_through(bench):
    """The guard has to be tight, not deaf. Same widget, different value."""
    bench.set_knob("layout.title.text", "first")
    assert bench.spec["knobs"]["layout.title.text"] == "first"
    spec, _echo, _msg = bench.report_knobs()
    assert spec is no_update                        # nothing changed: quiet
    bench.set_knob("layout.title.text", "second")   # something changed: heard
    assert bench.spec["knobs"]["layout.title.text"] == "second"
    bench.set_knob("layout.title.text", None)       # and cleared again
    assert "layout.title.text" not in bench.spec["knobs"]


def test_render_is_a_pure_function_of_the_spec(bench):
    """Two renders of the same spec produce the same code. No wobble, no drift."""
    bench.set_knob("layout.title.text", "stable")
    first = bench.code
    bench.echo = {"code": "", "knobs": {}, "sig": None, "vals": None}
    bench.render()
    assert bench.code == first
    assert codegen.parse(first) == {**bench.spec, "custom_code": None}


def test_the_whole_round_trip_holds_for_a_pile_of_knobs(bench):
    """render -> parse -> render, over one knob from each bucket that emits."""
    for path, value in [("layout.title.text", "A title"),
                        ("layout.barmode", "group"),
                        ("layout.xaxis.categoryorder", "total descending"),
                        ("layout.hovermode", "x unified"),
                        ("trace.marker.opacity", 0.8),
                        ("layout.transition.duration", 300)]:
        bench.set_knob(path, value)
        assert bench.spec["knobs"].get(path) == value, path
    assert codegen.parse(bench.code) == {**bench.spec, "custom_code": None}
    for bucket in ("MARK", "SCALE", "FRAME", "INTERACTION", "MOTION"):
        assert f"# --- {bucket}" in bench.code, bucket


# =====================================================================
# quick wins: parse_why in the banner, export, the table cap
# =====================================================================


def test_a_bad_code_edit_names_its_line():
    """The CUSTOM banner carries codegen.parse_why's reason, not a shrug."""
    spec = bench_app.blank_spec()
    _spec, msg = bench_app._apply_code(spec, "x = 1\nfig = px.bar(df)\n", {})
    assert "CUSTOM mode" in msg
    assert "line 1:" in msg and "df = " in msg


def test_a_stray_statement_after_show_names_its_line_too():
    spec = bench_app.blank_spec()
    code = bench_app.render_code(spec) + "\nprint('x')\n"
    _spec, msg = bench_app._apply_code(spec, code, {})
    assert "line " in msg and "fig.show()" in msg


def _fire(trigger_id):
    context_value.set(AttributeDict(
        triggered_inputs=[{"prop_id": f"{trigger_id}.n_clicks", "value": 1}]))


def test_export_py_hands_over_the_canonical_code():
    spec = bench_app.blank_spec()
    _fire("bench-export-py")
    try:
        got = bench_app.export_chart(1, 0, spec)
    finally:
        context_value.set({})
    assert got["filename"].endswith(".py")
    assert bench_app.render_code(spec) in got["content"]
    assert "import bench.data" in got["content"]


def test_export_py_in_custom_mode_hands_over_the_custom_text():
    spec = bench_app.blank_spec()
    spec["custom_code"] = "fig = px.bar(df)\n"
    _fire("bench-export-py")
    try:
        got = bench_app.export_chart(1, 0, spec)
    finally:
        context_value.set({})
    assert "fig = px.bar(df)" in got["content"]


def test_export_html_is_a_standalone_interactive_page():
    spec = bench_app.blank_spec()
    _fire("bench-export-html")
    try:
        got = bench_app.export_chart(0, 1, spec)
    finally:
        context_value.set({})
    assert got["filename"].endswith(".html")
    assert "<html" in got["content"].lower()
    assert "plotly" in got["content"].lower()


def test_find_tables_says_when_the_cap_trips(monkeypatch):
    from bench import data as bench_data

    fake = [{"fqn": f"DB.S.T{i}", "rows": i} for i in range(bench_app.TABLE_CAP + 50)]
    monkeypatch.setattr(bench_data, "tables", lambda term: fake)
    context_value.set(AttributeDict(
        triggered_inputs=[{"prop_id": "bench-src-find.n_clicks", "value": 1}]))
    try:
        options, _sql, note = bench_app.find_tables(1, None, "t")
    finally:
        context_value.set({})
    assert len(options) == bench_app.TABLE_CAP
    assert f"first {bench_app.TABLE_CAP} of {len(fake)}" in note


# =====================================================================
# the deadline gate: straight-line custom code never pays for the tracer
# =====================================================================


def test_needs_deadline_tells_loops_from_straight_lines():
    assert not bench_app._needs_deadline("fig = px.bar(df)\n")
    assert not bench_app._needs_deadline("fig = px.bar(df, x='A')\nfig.update_layout(title_text='t')\n")
    assert bench_app._needs_deadline("while True:\n    pass\n")
    assert bench_app._needs_deadline("for i in range(3):\n    pass\n")
    assert bench_app._needs_deadline("xs = [i for i in range(3)]\n")
    assert bench_app._needs_deadline("f = lambda: f()\n")
    assert bench_app._needs_deadline("def f():\n    return f()\n")
    assert not bench_app._needs_deadline("fig = (")   # will not compile -> cannot loop


def test_straight_line_custom_code_never_installs_a_tracer(monkeypatch):
    import sys as real_sys

    calls = []
    original = real_sys.settrace
    monkeypatch.setattr(bench_app.sys, "settrace",
                        lambda fn: (calls.append(fn), original(fn)))
    import pandas as pd

    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    fig, why = bench_app.run_custom("fig = px.bar(df, x='A', y='B')\n", df)
    assert why == ""
    assert not calls, "the deadline tracer ran on loop-free code"


def test_a_loop_still_hits_the_deadline():
    import pandas as pd

    df = pd.DataFrame({"A": [1]})
    t0 = time.time()
    fig, why = bench_app.run_custom("while True:\n    pass\n", df)
    assert "stopped" in why or "TimeoutError" in why
    assert time.time() - t0 < bench_app.CUSTOM_TIMEOUT_S + 5


# =====================================================================
# printed run, for a human
# =====================================================================


def main() -> int:
    import time

    t0 = time.time()
    b = Bench()
    print(f"opening screen        : {len(b.ids)} knob widgets, "
          f"{len(b.code.splitlines())} lines of code, "
          f"figure has {len(b.figure.data)} trace(s)")

    b.set_knob("layout.title.text", "Spend by agency")
    print(f"turn a knob           : spec={b.spec['knobs']}  "
          f"figure.title={b.figure.layout.title.text!r}  "
          f"code has title_text: {'title_text' in b.code}")

    rebuilds = b.pane_rebuilds
    for _ in range(5):
        s1, _, _ = b.edit_code(b.code)
        s2, _, _ = b.report_knobs()
        assert s1 is no_update and s2 is no_update
    print(f"echo it back x5       : spec untouched, pane rebuilt "
          f"{b.pane_rebuilds - rebuilds} more times  -> no loop")

    b.edit_code(b.code.replace("\nfig.show()",
                               '\nfig.update_layout(title_text="typed")\n\nfig.show()'))
    print(f"edit the code         : knob widget now {b.widget('layout.title.text')!r}")

    b.edit_code("import os\nfig = 1\n")
    print(f"break the code        : custom={b.spec['custom_code'] is not None}  "
          f"msg={b.knob_msg[:60]!r}")
    b.reset()
    print(f"press Reset           : custom={b.spec['custom_code'] is not None}  "
          f"canonical={codegen.parse(b.code) is not None}")

    b.click_chart("sankey")
    print(f"click an impossible   : {b.knob_msg[:100]}")

    b.set_source("demo", "flow")
    print(f"switch the source     : mapping={b.spec['mapping']}  msg={b.knob_msg[:50]!r}")

    chips = [f"{c.children[0].children.strip()}={c.children[1].children}"
             for c in b.status]
    print(f"\nstatus bar            : {'  '.join(chips)}")
    print(f"\nall of that in {time.time() - t0:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
