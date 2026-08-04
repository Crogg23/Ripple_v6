"""
THE BENCH - does it actually run?

    python -m pytest tests/test_bench_runs.py -q
    python tests/test_bench_runs.py               (same checks, prints as it goes)

tests/test_bench_app.py drives the callbacks as ordinary Python functions. That
is the right way to test the logic, and it is also the way a callback that only
works in-process can pass a green suite and still hand you a 500 in the browser.

So this file does the other half. It starts `python bench/app.py` as a real
subprocess, waits for it to serve, and then talks to it over HTTP the way the
browser does - POSTing to /_dash-update-component with the exact body Dash's own
renderer sends. A callback that is registered under a different name, returns
something that will not serialise, or blows up only under the Flask threading
model fails here and cannot fail anywhere else.

It checks the three items of SPEC section 10 that are about the thing running
rather than about the logic being right:

    rule 1  `python bench/app.py` opens the three panes
    rule 2  pick any of the charts -> it renders on demo data, or says exactly why not
    rule 6  warehouse mode runs real SQL through viz.sqlrun, lane badge visible

Plus the sweep that rule 2 really means: every chart against every demo frame,
3,190 combinations, asserting that `drawable` and the builder tell the same
story. That is the check that found the negative-size bug this file now pins.

WHAT NEEDS A NETWORK AND WHAT DOES NOT
--------------------------------------
Everything here runs on a plane except `test_a_live_select_runs_through_the_read_lane`,
which skips itself when there is no warehouse to reach. The refusal test does
NOT skip: viz.sqlrun's text guard rejects a DROP before it opens a connection,
so "the guard still says no" is checkable with the wire unplugged.
"""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import time
import warnings
from pathlib import Path

import plotly.graph_objects as go
import pytest
import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from bench import app as bench_app  # noqa: E402
from bench import codegen, controls, data, registry  # noqa: E402

# How long to wait for a Dash dev server to come up. It imports plotly, wall.py
# and 145 chart templates first, so this is generous on purpose.
BOOT_TIMEOUT_S = 180


# =====================================================================
# THE SERVER - started once, shared by every test that talks HTTP
# =====================================================================


def _free_port() -> int:
    """Ask the OS for a port nobody is using, so two test runs cannot collide."""
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class Server:
    """A running `python bench/app.py`, and the two ways to talk to it."""

    def __init__(self, port: int, proc: subprocess.Popen, log: Path):
        self.port = port
        self.proc = proc
        self.log = log
        self.base = f"http://127.0.0.1:{port}"
        self.deps = requests.get(f"{self.base}/_dash-dependencies", timeout=60).json()

    # -- the two GETs a browser does before it draws anything ----------

    def get(self, path: str, timeout: int = 120) -> requests.Response:
        return requests.get(self.base + path, timeout=timeout)

    # -- the POST it does for every interaction ------------------------

    def output_for(self, first_output: str) -> str:
        """The callback registration string that starts with this output.

        Read off /_dash-dependencies rather than retyped: Dash's spelling of a
        multi-output key is Dash's business, and a test that guesses it wrong
        gets a 500 that looks like an app bug.
        """
        for dep in self.deps:
            if dep["output"].lstrip(".").startswith(first_output):
                return dep["output"]
        raise AssertionError(
            f"no callback outputs {first_output}. Registered: "
            + ", ".join(d["output"] for d in self.deps))

    def fire(self, outputs: str, inputs, state=(), changed=None):
        """One /_dash-update-component call. Returns (parsed response, seconds)."""
        body = {
            "output": outputs,
            "outputs": _output_spec(outputs),
            "inputs": list(inputs),
            "changedPropIds": list(changed) if changed is not None else
                              [f"{_prop_id(i)}.{i['property']}" for i in inputs],
            "state": list(state),
        }
        t0 = time.time()
        r = requests.post(f"{self.base}/_dash-update-component", json=body, timeout=300)
        took = time.time() - t0
        assert r.status_code == 200, (
            f"HTTP {r.status_code} from the running app.\n{r.text[:600]}\n"
            f"--- server log tail ---\n{self.tail()}")
        return r.json()["response"], took

    def tail(self, lines: int = 25) -> str:
        text = self.log.read_text(encoding="utf-8", errors="replace")
        return "\n".join(text.splitlines()[-lines:])


def _prop_id(entry) -> str:
    """A component id as Dash writes it in changedPropIds - dicts get JSON."""
    return (entry["id"] if isinstance(entry["id"], str)
            else json.dumps(entry["id"], sort_keys=True))


def _output_spec(spec: str):
    """'..a.b...c.d' -> the list of {id, property} dicts Dash's renderer posts."""
    def one(part: str) -> dict:
        cut = part.rindex(".")
        return {"id": part[:cut], "property": part[cut + 1:]}
    if spec.startswith(".."):
        return [one(p) for p in spec.strip(".").split("...") if p]
    return one(spec)


@pytest.fixture(scope="module")
def server(tmp_path_factory):
    """Start bench/app.py for real, hand out a Server, then shut it down."""
    port = _free_port()
    log = tmp_path_factory.mktemp("bench") / "server.log"
    handle = log.open("w", encoding="utf-8")
    proc = subprocess.Popen(
        [sys.executable, "bench/app.py"],
        cwd=str(ROOT), stdout=handle, stderr=subprocess.STDOUT,
        env={**os.environ, "BENCH_PORT": str(port), "PYTHONUNBUFFERED": "1"},
    )
    started = time.time()
    try:
        while True:
            if proc.poll() is not None:
                handle.flush()
                pytest.fail("bench/app.py exited on its own, code "
                            f"{proc.returncode}:\n"
                            + log.read_text(encoding='utf-8', errors='replace'))
            if time.time() - started > BOOT_TIMEOUT_S:
                pytest.fail(f"bench/app.py never served in {BOOT_TIMEOUT_S}s")
            try:
                requests.get(f"http://127.0.0.1:{port}/", timeout=5)
                break
            except requests.exceptions.ConnectionError:
                time.sleep(0.3)
        yield Server(port, proc, log)
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=15)
        except subprocess.TimeoutExpired:
            proc.kill()
        handle.close()


# =====================================================================
# SPEC section 10, rule 1 - `python bench/app.py` opens the three panes
# =====================================================================


def test_the_app_serves_a_page(server):
    page = server.get("/")
    assert page.status_code == 200
    assert b"react-entry-point" in page.content
    # controls.PANEL_CSS is inlined by hand because dcc.Dropdown renders its own
    # markup that a style= dict cannot reach. Without it the dropdowns are white
    # boxes on a dark pane, which is a broken page, not a cosmetic one.
    assert b".bench-dd" in page.content


def test_the_served_layout_really_has_three_panes(server):
    layout = server.get("/_dash-layout")
    assert layout.status_code == 200
    ids = _all_ids(layout.json())
    for pane in ("bench-picker",      # LEFT - the 145 charts
                 "bench-figure",      # MIDDLE - the chart
                 "bench-code",        # MIDDLE - the editable code
                 "bench-knobs",       # RIGHT - the generated knobs
                 "bench-src-kind",    # the source bar
                 "bench-status"):     # the badges SPEC section 8 never lets off screen
        assert pane in ids, f"{pane} is not in the layout the server sent"


def test_the_callbacks_are_registered_on_the_running_server(server):
    """Seven server-side callbacks and the one clientside debounce."""
    clientside = [d for d in server.deps if d.get("clientside_function")]
    assert len(server.deps) == 8, [d["output"] for d in server.deps]
    assert len(clientside) == 1, "the 600ms code debounce is not registered"


def test_the_run_button_says_what_it_is_doing_while_a_query_is_in_flight(server):
    """A 9.4s query behind a button that still looks pressable is a query you
    fire twice. Dash swaps these props for the life of the call, so the proof
    is that the running spec really reached the browser."""
    dep = next(d for d in server.deps if d["output"].startswith("..bench-spec.data"))
    running = dep.get("running")
    assert running, "sync_spec has no `running` spec, so RUN never changes"
    text = json.dumps(running)
    assert "bench-src-run.disabled" in text, running
    assert "RUNNING SQL" in text, running


def test_the_server_logged_no_traceback(server):
    """Booting and serving a page must not print a stack trace."""
    text = server.log.read_text(encoding="utf-8", errors="replace")
    assert "Traceback" not in text, text[-2000:]


def _all_ids(tree) -> set[str]:
    """Every string component id in a served Dash layout."""
    found, stack = set(), [tree]
    while stack:
        node = stack.pop()
        if isinstance(node, dict):
            props = node.get("props") or {}
            if isinstance(props.get("id"), str):
                found.add(props["id"])
            stack.extend(v for v in props.values() if isinstance(v, (list, dict)))
        elif isinstance(node, list):
            stack.extend(node)
    return found


# =====================================================================
# SPEC section 10, rule 2 - pick any chart: it draws, or it says why
# =====================================================================

# One demo frame per section, so a sample of 30 is not 30 bar charts. Each is
# the shape that section's charts are actually FOR.
FRAME_FOR_SECTION = {
    "COMPARE": "category", "DISTRIBUTE": "long", "RELATE": "scatter",
    "COMPOSE": "hierarchy", "FLOW": "flow", "RANK": "rank_over_time",
    "LOCATE": "geo_points", "CHANGE": "timeseries", "CONNECT": "flow",
    "SINGLE VALUE": "category",
}


def _sample_across_sections(per_section: int = 3) -> list[tuple[str, str]]:
    """(section, chart key) pairs, spread evenly through every section."""
    out = []
    for section, _question in registry.SECTIONS:
        charts = registry.BY_SECTION[section]
        step = max(1, len(charts) // per_section)
        out.extend((section, t.key) for t in charts[::step][:per_section])
    return out


SAMPLE = _sample_across_sections()


def _spec_for(key: str, frame_name: str) -> dict:
    df, _meta = data.frame({"kind": "demo", "name": frame_name})
    return {"chart": key,
            "source": {"kind": "demo", "name": frame_name},
            "mapping": registry.auto_map(df, registry.CHARTS[key]),
            "knobs": {}, "custom_code": None}


def _render_over_http(server, spec):
    """THE FAST LANE over the wire: figure, code, status, message, mode.

    This used to be one callback with eight Outputs, so one POST brought the
    whole screen. It is three now - the chart must not have to wait on the
    knob pane - so the two panes below have their own helpers.
    """
    return server.fire(
        server.output_for("bench-figure.figure"),
        [{"id": "bench-spec", "property": "data", "value": spec}],
        state=[{"id": "bench-echo", "property": "data", "value": None}],
        changed=["bench-spec.data"])


def _knobs_over_http(server, spec, opened=None, query=""):
    """THE SLOW LANE: the right-hand pane and the widget echo."""
    return server.fire(
        server.output_for("bench-knobs.children"),
        [{"id": "bench-spec", "property": "data", "value": spec},
         {"id": controls.panel_id("search"), "property": "value", "value": query},
         {"id": "bench-open", "property": "data", "value": opened or {}}],
        state=[{"id": "bench-knob-echo", "property": "data", "value": None}],
        changed=["bench-spec.data"])


def _picker_over_http(server, spec, query=""):
    return server.fire(
        server.output_for("bench-picker.children"),
        [{"id": "bench-spec", "property": "data", "value": spec},
         {"id": "bench-picker-search", "property": "value", "value": query}],
        state=[{"id": "bench-picker-sig", "property": "data", "value": None}],
        changed=["bench-spec.data"])


def test_the_sample_covers_every_section():
    """The sample this file drives is at least 25 charts, all ten sections."""
    assert len(SAMPLE) >= 25, SAMPLE
    assert {s for s, _ in SAMPLE} == {name for name, _ in registry.SECTIONS}


@pytest.mark.parametrize("section,key", SAMPLE, ids=[k for _s, k in SAMPLE])
def test_a_chart_drawn_over_http_draws_or_says_why(server, section, key):
    """Through the real dispatcher: a figure with traces, or an honest sentence."""
    body, _took = _render_over_http(server, _spec_for(key, FRAME_FOR_SECTION[section]))

    figure = body["bench-figure"]["figure"]
    message = body["bench-build-msg"]["children"]
    code = body["bench-code"]["value"]

    if not figure.get("data"):
        # SPEC section 6: grey-out-with-a-reason, applied to the middle pane.
        said = (message or "") + " ".join(
            a.get("text", "") for a in (figure.get("layout") or {}).get("annotations", []))
        assert said.strip(), f"{key} came back blank and said nothing"
        assert registry.CHARTS[key].name in said or "cannot" in said, said

    # The code panel is a pane, not a decoration - it must show the chart line.
    assert isinstance(code, str)
    assert "px." in code or "registry.build" in code, code[:200]
    # And the badges are rebuilt on every render, so they cannot go missing.
    assert "lane" in json.dumps(body["bench-status"]["children"])


def test_the_chart_comes_back_without_the_pane_or_the_picker(server):
    """The split, over the wire. The fast lane owns five Outputs, not eight.

    The old callback returned the figure, the code, the pane, the picker, the
    status, the message, the mode and the echo together - 268ms and 4,128 KB
    for a chart click, and the chart could not appear until the 3.8 MB pane
    had been built. This asserts it no longer can.
    """
    spec = _spec_for("bar", "category")
    body, took = _render_over_http(server, spec)
    for pane in ("bench-figure", "bench-code", "bench-status", "bench-build-msg",
                 "bench-code-mode", "bench-echo"):
        assert pane in body, sorted(body)
    assert "bench-knobs" not in body, "the chart is still waiting on the knob pane"
    assert "bench-picker" not in body, "the chart is still waiting on the picker"
    assert took < 60, f"one chart render took {took:.1f}s"


def test_the_picker_and_the_knob_pane_come_back_on_their_own_lanes(server):
    """Both panes still arrive - they just arrive without holding the chart up."""
    spec = _spec_for("bar", "category")

    knobs_body, knobs_took = _knobs_over_http(server, spec)
    assert set(knobs_body) >= {"bench-knobs", "bench-knob-echo"}, sorted(knobs_body)
    lazy = json.dumps(knobs_body["bench-knobs"]["children"])
    assert 5_000 < len(lazy) < 400_000, (
        f"the lazy pane came back at {len(lazy)} bytes - too small is an empty "
        "pane, too big means it is not lazy any more")
    assert '"path": "mapping.x"' in lazy or '"path":"mapping.x"' in lazy, (
        "Tier 0 did not render")

    # ...and opening every tier really does bring the rest of it.
    everything = [f"{b}:{t}" for b in controls.BUCKET_ORDER for t in (1, 2)]
    opened_body, _ = _knobs_over_http(
        server, spec, opened={"key": bench_app.open_key(spec),
                              "tokens": everything})
    full = json.dumps(opened_body["bench-knobs"]["children"])
    assert len(full) > 10 * len(lazy), (
        f"opening every tier only grew the pane from {len(lazy)} to {len(full)}")
    assert knobs_took < 60, f"the knob pane took {knobs_took:.1f}s"

    picker_body, _ = _picker_over_http(server, spec)
    assert "bench-picker" in picker_body, sorted(picker_body)


# =====================================================================
# THE SWEEP - what rule 2 means when you stop sampling
# ---------------------------------------------------------------------
# Every chart against every demo frame. No browser, because 3,190 HTTP
# round trips is a coffee break; the point here is the agreement between
# `drawable` and the builder, and that is pure Python.
# =====================================================================


def _demo_frames() -> dict:
    return {name: data.frame({"kind": "demo", "name": name})[0]
            for name in data.demo_names()}


@pytest.mark.parametrize("frame_name", data.demo_names())
def test_drawable_and_the_builder_tell_the_same_story(frame_name):
    """A yes must draw. A no must be a sentence naming the chart and the data.

    This is the check that matters most in the whole file. `drawable` saying
    yes and the builder then raising is the worst failure the Bench has: you
    click a chart the UI told you was fine and get a stack trace.
    """
    df, _meta = data.frame({"kind": "demo", "name": frame_name})
    df_roles = registry.roles(df)
    broke = []
    for key in sorted(registry.CHARTS):
        template = registry.CHARTS[key]
        ok, why = registry.drawable(df_roles, template)
        assert why.strip(), f"{key}: drawable gave no reason at all"
        if not ok:
            # The reason has to name the chart AND say what this result holds.
            assert template.name in why, f"{key}: {why}"
            assert template.blocked or "this result has" in why, f"{key}: {why}"
            continue
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                fig = template.builder(df, registry.auto_map(df_roles, template), {})
            assert isinstance(fig, go.Figure)
        except Exception as exc:  # noqa: BLE001 - collect them all, then report
            broke.append(f"{key}: {type(exc).__name__}: {str(exc).strip()[:160]}")
    assert not broke, (
        f"{len(broke)} chart(s) said they were drawable on the {frame_name!r} "
        "frame and then raised:\n  " + "\n  ".join(broke))


@pytest.mark.parametrize("frame_name", data.demo_names())
def test_the_middle_pane_never_goes_blank_and_quiet(frame_name):
    """figure_for over every chart: always a Figure, never a silent blank."""
    spec = bench_app.blank_spec(demo=frame_name)
    df, meta = bench_app.get_frame(spec["source"])
    df_roles = registry.roles(df)
    for key in sorted(registry.CHARTS):
        template = registry.CHARTS[key]
        one = dict(spec, chart=key, mapping=registry.auto_map(df_roles, template))
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            fig, message = bench_app.figure_for(one, df, meta)
        assert isinstance(fig, go.Figure), f"{key} on {frame_name}: {type(fig)}"
        if fig.data:
            continue
        note = " ".join(a.text or "" for a in fig.layout.annotations)
        assert note.strip(), f"{key} on {frame_name}: blank figure, nothing said"
        assert message or template.blocked, f"{key} on {frame_name}: silent blank"


@pytest.mark.parametrize("frame_name", data.demo_names())
def test_the_code_panel_round_trips_for_every_chart(frame_name):
    """render -> parse -> the same chart and the same mapping. Every chart."""
    spec = bench_app.blank_spec(demo=frame_name)
    df, _meta = bench_app.get_frame(spec["source"])
    df_roles = registry.roles(df)
    for key in sorted(registry.CHARTS):
        one = dict(spec, chart=key,
                   mapping=registry.auto_map(df_roles, registry.CHARTS[key]))
        source = bench_app.render_code(one)
        back = codegen.parse(source)
        assert back is not None, f"{key} on {frame_name}: own code will not parse\n{source}"
        assert back["chart"] == key, f"{key} -> {back['chart']}"
        assert back["mapping"] == one["mapping"], f"{key}: {back['mapping']}"


def test_the_grey_out_reason_says_it_once():
    """SPEC section 6 and the Beer Rule: one sentence, not the same one twice.

    The reason used to name the chart three times - once in the headline, once
    in the builder's "still needs" error and once in `drawable`'s sentence.
    All three said the same thing, so the reader read it three times.
    """
    spec = bench_app.blank_spec()                 # one category column, one number
    df, meta = bench_app.get_frame(spec["source"])
    one = dict(spec, chart="sankey",
               mapping=registry.auto_map(df, registry.CHARTS["sankey"]))
    fig, message = bench_app.figure_for(one, df, meta)
    assert message.count("Sankey diagram") == 1, message
    assert "source column" in message and "this result has" in message
    body = " ".join(a.text or "" for a in fig.layout.annotations)
    assert body.count("Sankey diagram") == 1, body


# =====================================================================
# THE BUG THIS SWEEP FOUND - a negative number on a size slot
# ---------------------------------------------------------------------
# Plotly's marker.size is a radius, so it refuses anything below zero -
# not a warning, a ValueError. Any signed column (a change, a delta, a
# swing) killed five charts outright. registry._magnitude plots how big
# the number is and renames the column so the hover says so.
# =====================================================================

SIZED_CHARTS = [t.key for t in registry.TEMPLATES if t.slot("size") is not None]


def _signed_frame():
    """The frame a real query returns: places, counts, and a change that falls."""
    import pandas as pd
    return pd.DataFrame({
        "lat": [40.7, 34.0, 41.9, 29.8, 39.7],
        "lon": [-74.0, -118.2, -87.6, -95.4, -105.0],
        "entity": ["a", "b", "c", "d", "e"],
        "year": [2020, 2021, 2022, 2023, 2024],
        "change": [-12.0, 5.0, -3.0, 8.0, -1.0],
        "count": [10.0, 20.0, 30.0, 40.0, 50.0],
    })


def test_there_are_charts_with_a_size_slot():
    """If this ever hits zero the test below is testing nothing."""
    assert len(SIZED_CHARTS) >= 5, SIZED_CHARTS


@pytest.mark.parametrize("key", SIZED_CHARTS)
def test_a_negative_number_on_a_size_slot_draws_instead_of_raising(key):
    df = _signed_frame()
    template = registry.CHARTS[key]
    mapping = registry.auto_map(registry.roles(df), template)
    mapping["size"] = "change"                     # the column that goes down
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fig = template.builder(df, mapping, {})
    assert isinstance(fig, go.Figure)
    # `or []` would ask a numpy array whether it is truthy, which raises. The
    # explicit None check is the only safe way to read a Plotly array property.
    raw = fig.data[0].marker.size
    assert raw is not None, "nothing landed on marker.size at all"
    sizes = [float(v) for v in raw]
    assert sizes and min(sizes) >= 0, sizes
    # And it says so rather than quietly showing a fall as a small bubble.
    assert "|change|" in (fig.data[0].hovertemplate or ""), fig.data[0].hovertemplate


def test_a_positive_size_column_is_left_completely_alone():
    """The magnitude swap is for signed columns only - nothing else changes."""
    df = _signed_frame()
    fig = registry.CHARTS["bubble"].builder(
        df, {"x": "lat", "y": "lon", "size": "count", "color": None}, {})
    assert "count=" in (fig.data[0].hovertemplate or "")
    assert "|count|" not in (fig.data[0].hovertemplate or "")


def test_a_pure_px_chart_never_declares_a_size_slot():
    """Because `_magnitude` may rewrite the frame, and pure-px prints as a bare call."""
    for key in registry.PX_PURE:
        assert registry.CHARTS[key].slot("size") is None, key


# =====================================================================
# SPEC section 10, rule 6 - warehouse mode, through viz.sqlrun,
#                           with the lane badge on screen
# =====================================================================


def _source_change(server, sql: str, trigger: str = "bench-src-kind.value"):
    """Flip the source bar to warehouse with this SQL, over HTTP."""
    start = {"chart": "bar", "source": {"kind": "demo", "name": "category"},
             "mapping": {"x": "agency", "y": "spend", "color": None},
             "knobs": {}, "custom_code": None}
    return server.fire(
        server.output_for("bench-spec.data"),
        [{"id": {"bench": "chart", "key": "bar"}, "property": "n_clicks", "value": 0},
         {"id": {"bench": "knob", "part": "value", "path": "layout.title.text"},
          "property": "value", "value": None},
         {"id": "bench-code-draft", "property": "data", "value": None},
         {"id": "bench-code", "property": "n_blur", "value": 0},
         {"id": "bench-reset", "property": "n_clicks", "value": 0},
         {"id": "bench-src-kind", "property": "value", "value": "warehouse"},
         {"id": "bench-src-demo", "property": "value", "value": "category"},
         {"id": "bench-src-run", "property": "n_clicks", "value": 1}],
        state=[{"id": "bench-code", "property": "value", "value": ""},
               {"id": "bench-src-sql", "property": "value", "value": sql},
               {"id": "bench-spec", "property": "data", "value": start},
               {"id": "bench-echo", "property": "data", "value": {"code": ""}},
               {"id": "bench-knob-echo", "property": "data",
                "value": {"knobs": {}, "sig": None, "vals": None}}],
        changed=[trigger])


def test_switching_to_warehouse_reveals_the_sql_box(server):
    body, _took = server.fire(
        server.output_for("bench-src-demo-box.style"),
        [{"id": "bench-src-kind", "property": "value", "value": "warehouse"}],
        state=[{"id": "bench-src-sql", "property": "style", "value": {}}])
    assert body["bench-src-sql"]["style"]["display"] == "block"
    assert body["bench-src-sql-tools"]["style"]["display"] == "flex"
    assert body["bench-src-demo-box"]["style"]["display"] == "none"


def test_the_read_guard_refuses_a_drop_and_the_ui_says_so(server):
    """No connection needed - sqlrun's text guard says no before it dials out."""
    body, took = _source_change(server, "DROP TABLE x")
    said = str((body.get("bench-knob-msg") or {}).get("children") or "")
    assert said.strip(), "a refused query said nothing at all"
    assert "DROP" in said or "not allowed" in said, said
    assert took < 30, f"a refusal should be instant, took {took:.1f}s"


def test_a_refusal_still_shows_the_lane_and_the_row_count(server):
    """SPEC section 8: those badges are non-negotiable, especially when it broke."""
    body, _ = _source_change(server, "DROP TABLE x")
    spec = (body.get("bench-spec") or {}).get("data")
    assert spec, "the refused query never reached the SPEC store"
    rendered, _ = _render_over_http(server, spec)
    chips = json.dumps(rendered["bench-status"]["children"])
    for word in ("lane", "rows", "data as of", "took"):
        assert word in chips, f"the status bar lost `{word}`: {chips[:300]}"
    assert "refused" in chips, chips[:300]


def test_the_bench_never_passes_the_claim_table_override():
    """data.py must never hand sqlrun `unsafe_claims`. Read off the source."""
    source = (ROOT / "bench" / "data.py").read_text(encoding="utf-8")
    # The docstring says `sqlrun.run()` too, so look for the real call - the one
    # with arguments in it - not the first mention of the name.
    calls = [line.strip() for line in source.splitlines()
             if "sqlrun.run(" in line and "=" in line]
    assert calls == ["df, meta = sqlrun.run(sql, limit_rows)"], calls
    # It is mentioned twice - in the docstring that explains why we never pass
    # it, and in the self-test that prints its default. Neither PASSES it, and
    # passing it would have to look like `unsafe_claims=`.
    assert "unsafe_claims=" not in source, "the Bench passed the claim-table override"


@pytest.mark.snowflake
def test_a_live_select_runs_through_the_read_lane():
    """The real thing: a SELECT, the guarded lane, and a lane the badge can show."""
    lane = data.lane()
    if lane.get("lane") in (None, "offline"):
        pytest.skip(f"no warehouse from this machine: {lane.get('notes')}")
    df, meta = data.frame({"kind": "warehouse", "sql": "SELECT 1 AS a, 2 AS b"})
    assert meta["ok"], meta.get("error")
    assert meta["lane"] in ("enforced", "client-guard"), meta["lane"]
    assert meta["rows"] == len(df) == 1
    assert "as_of" in meta and "elapsed_s" in meta
    assert meta["lane"] in bench_app.LANE_COLOUR, "the badge has no colour for this lane"


@pytest.mark.snowflake
def test_the_badge_on_screen_names_the_live_lane(server):
    """SPEC section 10 rule 6, end to end: real SQL in, lane badge out."""
    if data.lane().get("lane") in (None, "offline"):
        pytest.skip("no warehouse from this machine")
    body, _ = _source_change(server, "SELECT 1 AS a, 2 AS b",
                             trigger="bench-src-run.n_clicks")
    spec = (body.get("bench-spec") or {}).get("data")
    assert spec and spec["source"]["kind"] == "warehouse", spec

    rendered, _ = _render_over_http(server, spec)
    chips = _chip_text(rendered["bench-status"]["children"])
    assert any(c.startswith("lane") for c in chips), chips
    assert any("enforced" in c or "client-guard" in c for c in chips), chips
    assert any(c.startswith("rows") for c in chips), chips


def _chip_text(chips) -> list[str]:
    """The status bar as plain strings - each chip is a label span + a value span."""
    out = []
    for chip in chips:
        spans = chip["props"]["children"]
        out.append("".join(str(s["props"]["children"]) for s in spans))
    return out


# =====================================================================
# RUN IT BY HAND - `python tests/test_bench_runs.py`
# =====================================================================

if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q", "--no-header"]))
