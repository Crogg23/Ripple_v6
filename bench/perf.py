#!/usr/bin/env python
"""
THE BENCH - perf.py.  Where the time actually goes.

    python bench/perf.py                 print the table
    python bench/perf.py --json out.json  save it too, for diffing
    python bench/perf.py --no-http        skip the live-server section
    python bench/perf.py --only knobs     run one section (see SECTIONS)

WHAT THIS MEASURES, AND WHY THOSE THINGS
----------------------------------------
Five things, in the order a human feels them:

  1. COLD START  - building `app.layout` once, and how many bytes that layout is
     when Dash serialises it. That payload is shipped on every page load.
  2. KNOB PANE   - the right-hand pane, for a small / medium / big chart. Time,
     component count and bytes, because the pane is most of the layout.
  3. CALLBACKS   - the four flows in SPEC section 8 (pick a chart, turn a knob,
     edit code, change source), called DIRECTLY with the arguments Dash would
     have handed them, plus each render lane priced on its own so you can see
     what the human is actually waiting for.
  4. FRAMES      - `get_frame()` for every demo frame, cold and warm, and the
     count that matters: how many times a repaint reaches the warehouse.
  5. HTTP        - the same flows over the wire, against a real server this
     script starts on a spare port and then kills BY PID. Request bytes,
     response bytes and wall time, which is the number a human actually waits.

HOW A NUMBER IS TAKEN - read this before you quote one
------------------------------------------------------
Every measurement warms up first, then takes a MEDIAN of several runs:

    under 100ms  -> 7 runs      under 1s -> 5 runs
    under 2s     -> 3 runs      over 2s  -> 1 run, and the row says so

The median, not the mean: one GC pause in the middle of a run should not be
allowed to become "the number". `n` is printed on every row, so a row with
n=1 can never quietly pass for a repeated measurement.

WHAT IT DOES NOT DO
-------------------
No browser, so nothing here measures React rendering, layout or paint. The
browser's share of a slow knob turn is real and this file cannot see it. What
it CAN see is everything up to the point the JSON leaves the server, plus the
size of what leaves - and on this app that is where the weight is.

Nothing here opens a warehouse connection. Every source is a demo frame, so
this file runs on a plane and the numbers do not move with the network. The
warehouse rows in section 4 stand a COUNTING STUB in front of `viz.sqlrun.run`
and put it straight back - which is the only honest way to prove "a knob turn
did not re-query" with no warehouse to not-query. Read those rows as counts of
9.4-second round trips, which is what a bare `SELECT 1` measured on this box.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import socket
import statistics
import subprocess
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable

# Anchor to the repo root so `python bench/perf.py` works from anywhere.
_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from dash import no_update  # noqa: E402
from dash._callback_context import context_value  # noqa: E402
from dash._utils import AttributeDict, to_json  # noqa: E402


# =====================================================================
# THE MEASUREMENT
# ---------------------------------------------------------------------
# One dataclass for a row, one function for a timing. Everything in this
# file produces Rows, the printer prints Rows, and --json dumps Rows. So
# two runs are diffable field by field.
# =====================================================================


@dataclass
class Row:
    """One measured thing.

    section  which of the five parts of the report it belongs to
    name     what was measured, in words
    ms       the MEDIAN wall time in milliseconds, or None when the row is
             only carrying a size
    fast     the FASTEST of the same runs. Print both, always. On Windows the
             dev server's own wakeups quantise to the 15.625ms scheduler tick,
             so a 1ms request measures as either ~1ms or ~15.6ms depending on
             which side of a tick it lands. A median alone would report 15ms
             of "work" that is really 1ms of work and a sleeping thread.
    n        how many timed runs the median came from. n=1 means one run.
    kb       serialised size, in kilobytes, when the thing has a size
    count    a countable: components, knobs, rows, whatever the note says
    note     the one line that stops the number being misread
    """

    section: str
    name: str
    ms: float | None = None
    fast: float | None = None
    n: int = 0
    kb: float | None = None
    count: int | None = None
    note: str = ""

    def as_dict(self) -> dict:
        return {"section": self.section, "name": self.name, "ms": self.ms,
                "fast": self.fast, "n": self.n, "kb": self.kb,
                "count": self.count, "note": self.note}


def _one(fn: Callable[[], Any]) -> float:
    t0 = time.perf_counter()
    fn()
    return time.perf_counter() - t0


def timed(fn: Callable[[], Any], *, warmup: int = 1,
          n: int | None = None) -> tuple[float, float, int]:
    """(median seconds, fastest seconds, how many runs).

    Warms up, then sizes the sample off the FIRST timed run, so a fast thing
    gets seven runs and a slow thing does not hold the report up for a minute.
    """
    for _ in range(warmup):
        fn()
    first = _one(fn)
    if n is None:
        n = 7 if first < 0.1 else 5 if first < 1.0 else 3 if first < 2.0 else 1
    if n <= 1:
        return first, first, 1
    samples = [first] + [_one(fn) for _ in range(n - 1)]
    return statistics.median(samples), min(samples), len(samples)


def measure(section: str, name: str, fn: Callable[[], Any], *,
            warmup: int = 1, n: int | None = None, kb: float | None = None,
            count: int | None = None, note: str = "") -> Row:
    """Time `fn` and hand back the Row."""
    median_s, fast_s, runs = timed(fn, warmup=warmup, n=n)
    return Row(section, name, ms=median_s * 1000.0, fast=fast_s * 1000.0,
               n=runs, kb=kb, count=count,
               note=note + ("" if runs > 1 else
                            ("  " if note else "") + "single run"))


def kbytes(obj: Any) -> float:
    """How big this is once Dash has serialised it, in KB.

    `dash._utils.to_json` is the exact encoder the server uses for the layout
    and for every callback response, so this is the number that goes on the
    wire and not an approximation of it.
    """
    return len(to_json(obj).encode("utf-8")) / 1024.0


def components(component: Any) -> int | None:
    """How many Dash components are in this tree, including the root.

    None when the thing is not a component tree at all - a go.Figure has a
    size but no component count, and printing 0 there would read as "empty".
    """
    if not hasattr(component, "_traverse"):
        return None
    try:
        return 1 + sum(1 for _ in component._traverse())
    except Exception:
        return None


# =====================================================================
# SECTION 1 - COLD START
# =====================================================================


def section_cold(app_mod) -> list[Row]:
    """What it costs to have a page to serve at all.

    Two different "cold"s, and they are not the same number:

      * a fresh interpreter importing `bench.app` - what `python bench/app.py`
        pays before it can answer anything. Measured in a subprocess, because
        you cannot un-import a module.
      * re-running app.py's module body in THIS process (importlib.reload),
        which rebuilds the layout with every cache already hot. That is the
        honest cost of the layout construction on its own.
    """
    import importlib

    rows: list[Row] = []

    code = (
        "import time, sys;"
        f"sys.path.insert(0, r'{_REPO}');"
        "t0 = time.perf_counter();"
        "import bench.app;"
        "print(time.perf_counter() - t0)"
    )

    def cold_import() -> float:
        out = subprocess.run([sys.executable, "-c", code], capture_output=True,
                             text=True, cwd=str(_REPO))
        return float(out.stdout.strip().splitlines()[-1])

    samples = [cold_import() for _ in range(3)]
    rows.append(Row("cold", "import bench.app (fresh interpreter)",
                    ms=statistics.median(samples) * 1000.0, n=len(samples),
                    note="includes plotly, pandas, registry's 145 templates AND "
                         "the first layout build"))

    rows.append(measure("cold", "rebuild app.py module body (reload, warm caches)",
                        lambda: importlib.reload(app_mod), n=5,
                        note="the layout construction with every cache hot"))
    app_mod = sys.modules[app_mod.__name__]

    layout = app_mod.app.get_layout()
    rows.append(Row("cold", "app.layout size", kb=kbytes(layout),
                    count=components(layout),
                    note="count = Dash components; this is the /_dash-layout body"))
    rows.append(measure("cold", "serialise app.layout (dash to_json)",
                        lambda: to_json(layout), n=5,
                        note="what serve_layout does on every page load"))

    # --- what the layout is MADE of ----------------------------------
    spec = app_mod.blank_spec()
    df, meta = app_mod.get_frame(spec["source"])
    cols = app_mod._columns(df)
    pane = app_mod.knob_pane(spec, cols)
    every = app_mod.ALL_TIERS_OPEN
    whole = app_mod.knob_pane(spec, cols, "", every)
    for name, fn, obj in (
        ("knob_pane(bar)", lambda: app_mod.knob_pane(spec, cols), pane),
        ("knob_pane(bar) every tier open",
         lambda: app_mod.knob_pane(spec, cols, "", every), whole),
        ("picker(145 charts)", lambda: app_mod.picker(spec, df), app_mod.picker(spec, df)),
        ("source_bar", lambda: app_mod.source_bar(spec, meta),
         app_mod.source_bar(spec, meta)),
        ("render_code", lambda: app_mod.render_code(spec), None),
        ("knob_echo(pane)", lambda: app_mod.knob_echo(pane), None),
    ):
        rows.append(measure("cold", "  piece: " + name, fn,
                            kb=None if obj is None else kbytes(obj),
                            count=None if obj is None else components(obj)))
    return rows


# =====================================================================
# SECTION 2 - THE KNOB PANE
# =====================================================================

# Three registry keys, deliberately spread. `indicator` is the smallest trace
# in the library (24 trace properties); `parcoords` and `scatter` are at the
# other end. All three carry the same ~1,980 layout knobs, which is the point.
PANE_CHARTS: tuple[str, ...] = ("indicator", "bar", "scatter", "parcoords")


def section_knobs(app_mod) -> list[Row]:
    """The right-hand pane, for a small, a medium and two big charts."""
    from bench import knobs

    rows: list[Row] = []
    spec = app_mod.blank_spec()
    df, _meta = app_mod.get_frame(spec["source"])
    cols = app_mod._columns(df)

    for chart in PANE_CHARTS:
        chart_spec = dict(spec, chart=chart, knobs={}, custom_code=None)
        chart_spec["mapping"] = {}
        n_knobs = sum(len(v) for tiers in knobs.tree(chart, cols).values()
                      for v in tiers.values())

        # Cold means "this trace type has never been walked". The walk is
        # lru_cached per trace type in knobs._raw_tree, so a chart you have
        # already clicked once is never cold again. knobs.tree() itself now
        # has a second cache in front of that walk (knobs._tree_cached, keyed
        # on trace type + columns) - clearing only _raw_tree would leave a
        # warm _tree_cached hit in place (this exact chart was already built
        # once at import time, in app.py's module-level _START_PANE), which
        # would silently turn this row into a warm measurement wearing a cold
        # label. Both have to be cleared for "cold" to mean cold.
        def cold() -> None:
            knobs._raw_tree.cache_clear()
            knobs._tree_cached.cache_clear()
            knobs.tree(chart, cols)

        rows.append(measure("knobs", f"{chart}: knobs.tree COLD (cache cleared)",
                            cold, n=3, count=n_knobs, note="count = knobs"))
        rows.append(measure("knobs", f"{chart}: knobs.tree warm",
                            lambda c=chart: knobs.tree(c, cols), count=n_knobs))

        every = app_mod.ALL_TIERS_OPEN
        pane = app_mod.knob_pane(chart_spec, cols)
        whole = app_mod.knob_pane(chart_spec, cols, "", every)
        rows.append(measure("knobs", f"{chart}: knob_pane -> components",
                            lambda s=chart_spec: app_mod.knob_pane(s, cols),
                            kb=kbytes(pane), count=components(pane),
                            note="count = Dash components; LAZY, Tier 0 only"))
        rows.append(measure("knobs", f"{chart}: knob_pane, every tier open",
                            lambda s=chart_spec: app_mod.knob_pane(s, cols, "", every),
                            kb=kbytes(whole), count=components(whole),
                            note="what the pane used to cost on EVERY repaint"))
        rows.append(measure("knobs", f"{chart}: serialise that pane",
                            lambda p=pane: to_json(p), kb=kbytes(pane)))
        rows.append(measure("knobs", f"{chart}: knob_echo(pane)",
                            lambda p=pane: app_mod.knob_echo(p),
                            count=len(app_mod.knob_echo(pane)),
                            note="count = widgets whose value is echoed"))

        # How many components the ONE pattern-matching Input actually catches.
        # It matches on path+part, so the wrapper rows and section bodies come
        # too, and every one of them is shipped on every knob turn. ALL only
        # matches components that EXIST, so this is the lazy number now.
        for label, built in (("", pane), (" (every tier open)", whole)):
            matched = sum(1 for node in built._traverse()
                          if isinstance(getattr(node, "id", None), dict)
                          and node.id.get("bench") == "knob")
            rows.append(Row("knobs",
                            f"{chart}: ids matching the knob Input{label}",
                            count=matched,
                            note="every one is serialised into every "
                                 "knob-turn request"))
    return rows


# =====================================================================
# SECTION 3 - THE CALLBACKS, CALLED DIRECTLY
# ---------------------------------------------------------------------
# `@app.callback` hands the module back the ORIGINAL function (dash 4.4.1
# `register_callback` ends with `return func`), so app.sync_spec and
# app.render_chart are ordinary functions. sync_spec reads `ctx`, so it gets a
# faked callback context - the same one tests/test_bench_app.py uses.
# =====================================================================


@dataclass
class Screen:
    """One screen's worth of Bench state, driven with no browser.

    Mirrors what the browser holds: the two stores, the code text, and the
    id/value pair for every knob widget on screen. Everything the perf run
    needs to fire a realistic callback comes off this.
    """

    app_mod: Any
    spec: dict = field(default_factory=dict)
    echo: dict = field(default_factory=dict)
    knob_echo: dict = field(default_factory=dict)
    picker_sig: Any = None
    opened: dict = field(default_factory=dict)
    code: str = ""
    ids: list = field(default_factory=list)
    values: list = field(default_factory=list)
    pane: Any = None
    open_all: bool = False

    def __post_init__(self) -> None:
        if not self.spec:
            self.spec = self.app_mod.blank_spec()
        self.echo = {"code": ""}
        self.knob_echo = {"knobs": {}, "sig": None, "vals": None}
        self.render()

    def render(self) -> tuple:
        """All three render lanes, the way the browser fans them out."""
        self.opened = ({"key": self.app_mod.open_key(self.spec),
                        "tokens": list(self.app_mod.ALL_TIERS_OPEN)}
                       if self.open_all else {})
        fig, code, status, msg, mode, echo = self.app_mod.render_chart(
            self.spec, self.echo)
        pane, knob_echo = self.app_mod.render_knobs(
            self.spec, "", self.opened, self.knob_echo)
        pick, picker_sig = self.app_mod.render_picker(
            self.spec, "", self.picker_sig)
        if code is not no_update:
            self.code = code
        if pane is not no_update:
            self.pane = pane
            self.ids, self.values = _widgets(pane)
        if echo is not no_update:
            self.echo = echo
        if knob_echo is not no_update:
            self.knob_echo = knob_echo
        if picker_sig is not no_update:
            self.picker_sig = picker_sig
        return fig, code, pane, pick, status, msg, mode, echo

    def sync_args(self, **overrides) -> dict:
        from bench import registry
        args = dict(
            _chart_clicks=[0] * len(registry.TEMPLATES),
            knob_values=list(self.values),
            draft=None, _blur=None, _reset=None,
            src_kind=self.spec["source"].get("kind", "demo"),
            src_demo=self.spec["source"].get("name", self.app_mod.START_DEMO),
            _run=None, _row_clicks=[], _undo=None, _redo=None,
            load_contents=None, restore_data=None,
            code_value=self.code,
            sql=self.spec["source"].get("sql", ""),
            spec=self.spec, echo=self.echo, knob_echo=self.knob_echo,
            history={"past": [], "future": []},
        )
        args.update(overrides)
        return args

    def set_context(self, prop_id: str) -> None:
        from bench import registry
        inputs_list = [
            [{"id": {"bench": "chart", "key": t.key}, "property": "n_clicks",
              "value": 0} for t in registry.TEMPLATES],
            [{"id": cid, "property": "value", "value": v}
             for cid, v in zip(self.ids, self.values)],
        ]
        context_value.set(AttributeDict(
            triggered_inputs=[{"prop_id": prop_id, "value": None}],
            inputs_list=inputs_list))


def _widgets(component) -> tuple[list, list]:
    """Every knob id and value in a pane, exactly as Dash reports them."""
    ids, values = [], []
    for node in component._traverse():
        cid = getattr(node, "id", None)
        if isinstance(cid, dict) and cid.get("bench") == "knob":
            ids.append(dict(cid))
            values.append(getattr(node, "value", None))
    return ids, values


def _prop_id(cid: dict, prop: str) -> str:
    return json.dumps(cid, sort_keys=True, separators=(",", ":")) + "." + prop


def _actions(app_mod, screen: Screen) -> list[tuple[str, str, dict]]:
    """The four flows from SPEC section 8, as (name, prop_id, sync_spec kwargs).

    Every one of them is a thing a human does with one gesture, so every one
    of them is a thing that has to feel instant.
    """
    # 2. turn a knob - move one widget's value, the way the browser would
    values = list(screen.values)
    for i, cid in enumerate(screen.ids):
        if cid.get("path") == "layout.barmode" and cid.get("part") == "value":
            values[i] = "stack"
            knob_prop = _prop_id(cid, "value")
            break
    else:                                   # pragma: no cover - bar always has it
        knob_prop = _prop_id(screen.ids[0], "value")

    # 3. edit the code - a canonical edit, so it parses and the knobs move
    edited = app_mod.render_code(dict(screen.spec, knobs={"layout.barmode": "stack"}))

    return [
        ("pick a chart (bar -> scatter)",
         _prop_id({"bench": "chart", "key": "scatter"}, "n_clicks"), {}),
        ("turn a knob (layout.barmode)", knob_prop, {"knob_values": values}),
        ("edit the code (canonical)", "bench-code-draft.data", {"draft": edited}),
        ("change source (demo -> long)", "bench-src-demo.value", {"src_demo": "long"}),
    ]


def section_callbacks(app_mod) -> list[Row]:
    """Each flow: sync_spec, then the three render lanes, together and apart."""
    rows: list[Row] = []
    screen = Screen(app_mod)

    for name, prop_id, overrides in _actions(app_mod, screen):
        args = screen.sync_args(**overrides)
        screen.set_context(prop_id)
        try:
            rows.append(measure("callbacks", f"sync_spec: {name}",
                                lambda a=args: app_mod.sync_spec(**a)))
            spec, echo, _msg, _hist, _persist = app_mod.sync_spec(**args)
        finally:
            context_value.set({})
        if spec is no_update:
            spec = screen.spec
        knob_echo = screen.knob_echo if echo is no_update else echo

        rows.append(measure(
            "callbacks", f"all three lanes after: {name}",
            lambda s=spec, e=screen.echo, k=knob_echo, p=screen.picker_sig: (
                app_mod.render_chart(s, e),
                app_mod.render_knobs(s, "", {}, k),
                app_mod.render_picker(s, "", p)),
            note="what the OLD single callback made you wait for, all of it"))
        rows.extend(_attribute_render(app_mod, name, spec, screen.echo,
                                      knob_echo, screen.picker_sig))
    return rows


def _attribute_render(app_mod, name: str, spec: dict, echo: dict,
                      knob_echo: dict, picker_sig: Any) -> list[Row]:
    """The three lanes, priced one at a time.

    This used to be ONE callback with EIGHT Outputs off ONE Input, so the
    chart could not repaint until the knob pane and the picker were built.
    The rows below are why that mattered and whether it still does: the fast
    lane is what a human is actually waiting for, and it must not move when
    the pane gets more expensive.
    """
    rows: list[Row] = []
    df, meta = app_mod.get_frame(spec.get("source") or {})
    columns = app_mod._columns(df)
    custom = isinstance(spec.get("custom_code"), str)
    signature = [spec.get("chart"), columns, custom, "", []]
    values_sig = app_mod.knob_values_signature(spec)
    rebuilds = signature != knob_echo.get("sig") or values_sig != knob_echo.get("vals")

    fast = app_mod.render_chart(spec, echo)
    pane = app_mod.knob_pane(spec, columns) if rebuilds else None
    pick = app_mod.picker(spec, df, "")

    pieces: list[tuple[str, Callable[[], Any], Any]] = [
        ("get_frame", lambda: app_mod.get_frame(spec.get("source") or {}), None),
        ("FAST LANE render_chart", lambda: app_mod.render_chart(spec, echo),
         list(fast)),
        ("  of which: figure", lambda: app_mod.figure_for(spec, df, meta), fast[0]),
        ("  of which: code", lambda: app_mod.code_and_mode(spec), None),
        ("  of which: status", lambda: app_mod.status_bar(meta), None),
        ("SLOW LANE render_knobs",
         lambda: app_mod.render_knobs(spec, "", {}, knob_echo), None),
        ("picker (own lane, guarded)",
         lambda: app_mod.render_picker(spec, "", picker_sig), pick),
    ]
    if rebuilds:
        pieces.append(("  of which: knob_pane",
                       lambda: app_mod.knob_pane(spec, columns), pane))
        pieces.append(("  of which: knob_echo",
                       lambda: app_mod.knob_echo(pane), None))

    for label, fn, obj in pieces:
        rows.append(measure("callbacks", f"    {name} | {label}", fn,
                            kb=None if obj is None else kbytes(obj),
                            count=None if obj is None else components(obj)))
    if not rebuilds:
        rows.append(Row("callbacks", f"    {name} | knob pane",
                        note="no_update - the pane is NOT rebuilt for a knob turn"))
    return rows


# =====================================================================
# SECTION 4 - THE FRAMES
# =====================================================================


def section_frames(app_mod) -> list[Row]:
    """`get_frame` for every demo frame, cold and warm.

    One cache now, and it lives in data.py (SPEC section 7.1). `app.get_frame`
    is a door onto it, not a second store. Cold means both the demo builder
    cache and the frame cache are empty, which is what the FIRST use of a
    source costs; warm is what every later callback pays - and every repaint
    pays it, so it is the one that matters.
    """
    from bench import data

    rows: list[Row] = []
    for name in data.demo_names():
        source = {"kind": "demo", "name": name}

        def cold() -> None:
            data.clear_demo_cache()
            data.invalidate()
            app_mod.get_frame(source)

        rows.append(measure("frames", f"{name}: cold (both caches empty)", cold, n=3))
        df, _meta = app_mod.get_frame(source)
        rows.append(measure("frames", f"{name}: warm (data frame-cache hit)",
                            lambda s=source: app_mod.get_frame(s),
                            count=len(df),
                            note=f"count = rows, {len(df.columns)} columns"))

    rows.extend(_frame_calls_per_repaint(app_mod))
    rows.extend(_warehouse_round_trips(app_mod))
    return rows


def _frame_calls_per_repaint(app_mod) -> list[Row]:
    """How many times a repaint really reaches the FETCH behind the cache.

    `data.frame` is the cache's own front door, so counting calls to it counts
    nothing. `data._fetch` is the thing that talks to `viz.sqlrun`, so that is
    what is wrapped here - and it is put straight back afterwards.
    """
    from bench import data

    rows: list[Row] = []
    real = data._fetch
    calls = {"n": 0}

    def counting(source):
        calls["n"] += 1
        return real(source)

    screen = Screen(app_mod)
    sources = [{"kind": "demo", "name": n} for n in data.demo_names()[:5]]

    try:
        data._fetch = counting                     # type: ignore[assignment]

        calls["n"] = 0
        for _ in range(5):
            screen.render()
        rows.append(Row("frames", "data._fetch calls: 5 repaints, one source",
                        count=calls["n"],
                        note="0 = the frame cache absorbed them; a warehouse "
                             "source is NOT re-queried"))

        data.invalidate()
        calls["n"] = 0
        for _ in range(2):
            for source in sources:
                app_mod.get_frame(source)
        rows.append(Row("frames", "data._fetch calls: 5 sources x 2 rounds",
                        count=calls["n"],
                        note=f"CACHE_MAX_ENTRIES is {data.CACHE_MAX_ENTRIES}, so "
                             "all five fit and the second round is free"))
    finally:
        data._fetch = real                         # type: ignore[assignment]
        data.invalidate()
    return rows


def _warehouse_round_trips(app_mod) -> list[Row]:
    """THE ROW THIS WHOLE FILE EXISTS FOR: knob turns per Snowflake call.

    Nothing here opens a connection. `viz.sqlrun.run` is stood up as a
    counting stub for the length of the count and put straight back, which is
    the only honest way to prove "it did not re-query" with no warehouse to
    not-query. A bare `SELECT 1` measured at 9.4s on this box, so every call
    counted below is 9.4 seconds a human would have been sitting through.
    """
    import pandas as pd

    from bench import data
    from viz import sqlrun

    rows: list[Row] = []
    calls = {"n": 0}

    def fake_run(sql, limit_rows=sqlrun.DEFAULT_LIMIT_ROWS):
        calls["n"] += 1
        return (pd.DataFrame({"AGENCY": ["a", "b", "c"], "SPEND": [1.0, 2.0, 3.0]}),
                {"rows": 3, "truncated": False, "elapsed_s": 9.4,
                 "warehouse": "SERVE_WH", "lane": "enforced",
                 "as_of": "2026-08-01 00:00:00", "budget": "", "claim_refs": []})

    real_run, real_lane = sqlrun.run, sqlrun.lane_status
    source = {"kind": "warehouse", "sql": "SELECT AGENCY, SPEND FROM T"}
    try:
        sqlrun.run = fake_run                      # type: ignore[assignment]
        sqlrun.lane_status = lambda: {"lane": "enforced", "notes": []}  # type: ignore
        data.invalidate(source)

        screen = Screen(app_mod)
        screen.spec = dict(screen.spec, source=source)
        screen.spec["mapping"] = {"x": "AGENCY", "y": "SPEND", "color": None}
        calls["n"] = 0
        screen.render()
        rows.append(Row("frames", "warehouse: first paint of a new query",
                        count=calls["n"], note="1 = the query really ran"))

        calls["n"] = 0
        for i in range(20):
            screen.spec = dict(screen.spec,
                               knobs={"layout.title.text": f"turn {i}"})
            screen.render()
        rows.append(Row("frames", "warehouse: 20 knob turns after that",
                        count=calls["n"],
                        note="MUST be 0. At 9.4s a round trip, 1 here is "
                             "3 minutes of a human's afternoon"))

        calls["n"] = 0
        app_mod.get_frame(source, refresh=True)
        rows.append(Row("frames", "warehouse: pressing RUN on the same SQL",
                        count=calls["n"],
                        note="MUST be 1 - refresh has to reach the read lane, "
                             "or RUN is a button that does nothing"))

        _df, meta = app_mod.get_frame(source)
        chips = to_json(app_mod.status_bar(meta))
        rows.append(Row("frames", "warehouse: the status bar admits it cached",
                        count=1 if "cached" in chips else 0,
                        note="1 = the `took` chip says the 9.40s is the "
                             "ORIGINAL fetch, not one it just paid again"))
    finally:
        sqlrun.run = real_run                      # type: ignore[assignment]
        sqlrun.lane_status = real_lane             # type: ignore[assignment]
        data.invalidate(source)
    return rows


# =====================================================================
# SECTION 5 - OVER REAL HTTP
# ---------------------------------------------------------------------
# We start `python bench/app.py` on a spare port as a subprocess we own,
# talk to it, and then kill THAT PID and nothing else. No wildcard kill
# lives in this file and none is ever allowed to.
# =====================================================================


# Eleven, not five. The dev server's wakeups quantise to Windows' 15.625ms
# scheduler tick, so a cheap request lands on either ~1ms or ~15.6ms and the
# sample is genuinely bimodal. Eleven runs make the median stable and the
# `fast` column shows the un-quantised side.
HTTP_RUNS = 11


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


class Client:
    """One keep-alive HTTP connection, so we time the SERVER and not TCP.

    urllib opens a fresh socket per call, and on this machine that alone was a
    ~15ms floor under every request - which is not what a browser pays, because
    a browser holds the connection open. This reconnects only when the server
    drops the socket.
    """

    def __init__(self, host: str, port: int, timeout: float = 300.0):
        self.host, self.port, self.timeout = host, port, timeout
        self.conn: Any = None

    def _connect(self):
        import http.client
        self.conn = http.client.HTTPConnection(self.host, self.port,
                                               timeout=self.timeout)

    def request(self, method: str, path: str,
                body: bytes | None = None) -> tuple[int, bytes, float]:
        headers = {"Accept": "application/json"}
        if body is not None:
            headers["Content-Type"] = "application/json"
        for attempt in (1, 2):
            if self.conn is None:
                self._connect()
            t0 = time.perf_counter()
            try:
                self.conn.request(method, path, body=body, headers=headers)
                resp = self.conn.getresponse()
                data = resp.read()
                return resp.status, data, time.perf_counter() - t0
            except Exception:
                self.close()
                if attempt == 2:
                    raise
        raise RuntimeError("unreachable")

    def close(self) -> None:
        if self.conn is not None:
            try:
                self.conn.close()
            except Exception:
                pass
            self.conn = None


def _split_output_key(key: str) -> list[dict]:
    """'..a.b...c.d..' -> [{'id': 'a', 'property': 'b'}, ...].

    The browser sends this list back with every request; Dash reads it to know
    which slots the answer fills. A single-output callback is the bare 'a.b'.
    """
    parts = key[2:-2].split("...") if key.startswith("..") and key.endswith("..") \
        else [key]
    out = []
    for part in parts:
        if part.startswith("{"):
            close = part.rfind("}")
            cid: Any = json.loads(part[:close + 1])
            prop = part[close + 2:]
        else:
            cid, _, prop = part.rpartition(".")
        out.append({"id": cid, "property": prop})
    return out


def _wire_values(app_mod, screen: Screen) -> dict:
    """{(component id string, property): value} for every input on the page.

    Built from the Screen, so what we POST is exactly what a browser holding
    that screen would POST - including all ~4,000 knob-widget entries, which
    is the whole reason this section exists.
    """
    from bench import registry

    chart_pattern = [
        {"id": {"bench": "chart", "key": t.key}, "property": "n_clicks", "value": 0}
        for t in registry.TEMPLATES]
    knob_pattern = [
        {"id": cid, "property": "value", "value": v}
        for cid, v in zip(screen.ids, screen.values)]

    return {
        ('{"bench":"chart","key":["ALL"]}', "n_clicks"): chart_pattern,
        ('{"bench":"knob","part":["ALL"],"path":["ALL"]}', "value"): knob_pattern,
        ('{"bench":"bucket","bucket":["ALL"],"part":["ALL"]}', "n_clicks"): [],
        ("bench-code-draft", "data"): None,
        ("bench-code", "n_blur"): None,
        ("bench-code", "value"): screen.code,
        ("bench-reset", "n_clicks"): 0,
        ("bench-src-kind", "value"): "demo",
        ("bench-src-demo", "value"): screen.spec["source"].get("name"),
        ("bench-src-run", "n_clicks"): 0,
        ("bench-src-sql", "value"): "",
        ("bench-src-sql", "style"): {},
        ("bench-cat-open", "n_clicks"): 0,
        ("bench-cat-domain", "value"): None,
        ("bench-cat-filter", "value"): "",
        ("bench-cat-refresh", "n_clicks"): 0,
        ("bench-cat-picked", "data"): None,
        ("bench-src-draft", "n_clicks"): 0,
        ('{"fqn":["ALL"],"type":"bench-cat-row"}', "n_clicks"): [],
        ("bench-spec", "data"): screen.spec,
        ("bench-echo", "data"): screen.echo,
        ("bench-knob-echo", "data"): screen.knob_echo,
        ("bench-open", "data"): screen.opened,
        ("bench-picker-sig", "data"): screen.picker_sig,
        ("bench-picker-search", "value"): "",
        ('{"bench":"panel","part":"search"}', "value"): "",
    }


def _body(app_mod, key: str, changed: list[str], wire: dict,
          override: dict | None = None) -> dict:
    """The JSON body dash-renderer would POST for one callback."""
    cb = app_mod.app.callback_map[key]
    override = override or {}

    def entry(spec: dict):
        cid, prop = spec["id"], spec["property"]
        value = override.get((cid, prop), wire.get((cid, prop)))
        if isinstance(value, list) and value and isinstance(value[0], dict) \
                and "id" in value[0]:
            return value            # a pattern-matching input: a list of entries
        return {"id": cid, "property": prop, "value": value}

    return {
        "output": key,
        "outputs": _split_output_key(key),
        "inputs": [entry(s) for s in cb["inputs"]],
        "changedPropIds": changed,
        "state": [entry(s) for s in cb["state"]],
    }


def section_http(app_mod) -> list[Row]:
    """The same four flows, over the wire, against a server we start and kill."""
    import tempfile

    rows: list[Row] = []
    port = _free_port()
    env = dict(os.environ, BENCH_PORT=str(port))
    # The server's own stdout goes to a temp file, not into the repo, and not
    # into a PIPE - a pipe nobody drains fills its buffer and deadlocks the
    # very process we are timing.
    log_path = Path(tempfile.gettempdir()) / f"bench-perf-{port}.log"
    log = open(log_path, "w", encoding="utf-8", errors="replace")
    proc = subprocess.Popen(
        [sys.executable, str(_REPO / "bench" / "app.py")],
        cwd=str(_REPO), env=env, stdout=log, stderr=subprocess.STDOUT)
    base = f"http://127.0.0.1:{port}"

    client = Client("127.0.0.1", port)
    try:
        t0 = time.perf_counter()
        boot = None
        while time.perf_counter() - t0 < 180:
            if proc.poll() is not None:
                raise RuntimeError(
                    f"the server exited with code {proc.returncode} - see "
                    f"{log.name}")
            try:
                status, _body_bytes, _e = client.request("GET", "/")
                if status == 200:
                    boot = time.perf_counter() - t0
                    break
            except Exception:
                time.sleep(0.25)
        if boot is None:
            raise RuntimeError("the server never answered on " + base)
        rows.append(Row("http", "server boot to first 200 on /", ms=boot * 1000.0,
                        n=1, note=f"pid {proc.pid}, port {port}"))

        for label, path in (("GET /_dash-layout", "/_dash-layout"),
                            ("GET /_dash-dependencies", "/_dash-dependencies")):
            sizes: list[float] = []
            times: list[float] = []
            for _ in range(HTTP_RUNS + 1):
                _s, body, elapsed = client.request("GET", path)
                sizes.append(len(body) / 1024.0)
                times.append(elapsed)
            times = times[1:]                      # first one is the warm-up
            rows.append(Row("http", label, ms=statistics.median(times) * 1000.0,
                            fast=min(times) * 1000.0, n=len(times),
                            kb=statistics.median(sizes),
                            note="first request dropped as warm-up"))

        # --- the four flows, plus a repaint and a trivial control --------
        screen = Screen(app_mod)
        wire = _wire_values(app_mod, screen)
        opened = Screen(app_mod, open_all=True)
        sync_key = next(k for k in app_mod.app.callback_map if "bench-knob-msg" in k)
        chart_key = next(k for k in app_mod.app.callback_map if "bench-figure" in k)
        knobs_key = next(k for k in app_mod.app.callback_map
                         if "bench-knobs.children" in k)
        picker_key = next(k for k in app_mod.app.callback_map
                          if "bench-picker.children" in k)
        face_key = next(k for k in app_mod.app.callback_map
                        if "bench-src-demo-box" in k)

        def knob_turn(scr):
            """(the prop_id of one moved widget, every widget's entry)."""
            values = list(scr.values)
            prop = None
            for i, cid in enumerate(scr.ids):
                if cid.get("path") == "layout.barmode" \
                        and cid.get("part") == "value":
                    values[i] = "stack"
                    prop = _prop_id(cid, "value")
                    break
            return prop, [{"id": cid, "property": "value", "value": v}
                          for cid, v in zip(scr.ids, values)]

        knob_prop, knob_entries = knob_turn(screen)
        open_prop, open_entries = knob_turn(opened)
        edited = app_mod.render_code(dict(screen.spec,
                                          knobs={"layout.barmode": "stack"}))

        # The second half of a chart click: the spec store has changed, so the
        # browser fires the render lanes - and the echo it still holds is the
        # OLD one, which is exactly what makes the knob pane rebuild.
        picked = dict(screen.spec, chart="scatter", knobs={}, custom_code=None)
        pattern = '{"bench":"knob","part":["ALL"],"path":["ALL"]}'

        calls: list[tuple[str, str, list[str], dict]] = [
            ("POST pick a chart (sync_spec)", sync_key,
             [_prop_id({"bench": "chart", "key": "scatter"}, "n_clicks")], {}),
            ("POST turn a knob (sync_spec)", sync_key, [knob_prop],
             {(pattern, "value"): knob_entries}),
            ("POST turn a knob, every tier open (sync_spec)", sync_key,
             [open_prop], {(pattern, "value"): open_entries,
                           ("bench-echo", "data"): opened.echo,
                           ("bench-knob-echo", "data"): opened.knob_echo}),
            ("POST edit the code (sync_spec)", sync_key, ["bench-code-draft.data"],
             {("bench-code-draft", "data"): edited}),
            ("POST change source (sync_spec)", sync_key, ["bench-src-demo.value"],
             {("bench-src-demo", "value"): "long"}),
            ("POST repaint the chart (render_chart)", chart_key,
             ["bench-spec.data"], {}),
            ("POST repaint the chart after a pick (render_chart)", chart_key,
             ["bench-spec.data"], {("bench-spec", "data"): picked}),
            ("POST the knob pane, pane NOT rebuilt (render_knobs)", knobs_key,
             ["bench-spec.data"], {}),
            ("POST the knob pane after a pick (render_knobs)", knobs_key,
             ["bench-spec.data"], {("bench-spec", "data"): picked}),
            ("POST the knob pane, every tier open (render_knobs)", knobs_key,
             ["bench-spec.data"],
             {("bench-spec", "data"): picked,
              ("bench-open", "data"): {
                  "key": app_mod.open_key(picked),
                  "tokens": list(app_mod.ALL_TIERS_OPEN)}}),
            ("POST the picker after a pick (render_picker)", picker_key,
             ["bench-spec.data"], {("bench-spec", "data"): picked}),
            ("POST source_face (trivial callback)", face_key,
             ["bench-src-kind.value"], {}),
        ]

        for label, key, changed, override in calls:
            payload = json.dumps(_body(app_mod, key, changed, wire, override)).encode()
            status, body, _first = client.request(
                "POST", "/_dash-update-component", payload)      # warm-up
            times = []
            for _ in range(HTTP_RUNS):
                status, body, elapsed = client.request(
                    "POST", "/_dash-update-component", payload)
                times.append(elapsed)
            note = f"request {len(payload) / 1024.0:,.0f} KB, HTTP {status}"
            if status != 200:
                note += f": {body[:160]!r}"
            rows.append(Row("http", label,
                            ms=statistics.median(times) * 1000.0,
                            fast=min(times) * 1000.0, n=len(times),
                            kb=len(body) / 1024.0, note=note))
    finally:
        client.close()
        _kill(proc)
        log.close()
    return rows


def _kill(proc: subprocess.Popen) -> None:
    """Kill ONE process - the one we started - and nothing else.

    There is no pattern here, no image name, no /IM. A previous agent on this
    machine ran a wildcard kill and took every python process with it. This
    function only ever holds one PID.
    """
    if proc.poll() is not None:
        return
    proc.terminate()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=10)


# =====================================================================
# THE REPORT
# =====================================================================

SECTIONS: dict[str, Callable[[Any], list[Row]]] = {
    "cold": section_cold,
    "knobs": section_knobs,
    "callbacks": section_callbacks,
    "frames": section_frames,
    "http": section_http,
}

SECTION_TITLES = {
    "cold": "1. COLD START - building and shipping the layout",
    "knobs": "2. THE KNOB PANE - per chart",
    "callbacks": "3. THE CALLBACKS - called directly, no browser",
    "frames": "4. get_frame() - every demo frame",
    "http": "5. OVER REAL HTTP - a server we start, then kill by PID",
}


def _say(text: str = "") -> None:
    """Print, surviving a cp1252 console. Same trick knobs.py uses."""
    enc = sys.stdout.encoding or "utf-8"
    sys.stdout.write(text.encode(enc, errors="replace").decode(enc, errors="replace")
                     + "\n")


def print_table(rows: Iterable[Row], meta: dict) -> None:
    rows = list(rows)
    _say("=" * 118)
    _say("THE BENCH - perf baseline")
    _say("=" * 118)
    for key in ("when", "label", "python", "platform", "packages"):
        if meta.get(key):
            _say(f"  {key:<10} {meta[key]}")
    _say("")
    _say("  ms = MEDIAN wall time of n runs after a warm-up; fast = the quickest "
         "of those runs.")
    _say("  KB = serialised size (dash to_json). count = whatever the note says "
         "it counts.")
    _say("")

    width = max((len(r.name) for r in rows), default=40) + 2
    for section in SECTIONS:
        here = [r for r in rows if r.section == section]
        if not here:
            continue
        _say("")
        _say(SECTION_TITLES[section])
        _say("-" * 118)
        _say(f"{'what':<{width}} {'ms':>10} {'fast':>9} {'n':>3} {'KB':>10} "
             f"{'count':>8}  note")
        for r in here:
            ms = f"{r.ms:,.2f}" if r.ms is not None else ""
            fast = f"{r.fast:,.2f}" if r.fast is not None else ""
            kb = f"{r.kb:,.1f}" if r.kb is not None else ""
            count = f"{r.count:,}" if r.count is not None else ""
            _say(f"{r.name:<{width}} {ms:>10} {fast:>9} {r.n or '':>3} {kb:>10} "
                 f"{count:>8}  {r.note}")

    timed_rows = [r for r in rows if r.ms is not None]
    if timed_rows:
        _say("")
        _say("=" * 118)
        _say("THE FIVE MOST EXPENSIVE MEASURED OPERATIONS")
        _say("=" * 118)
        for r in sorted(timed_rows, key=lambda x: -(x.ms or 0))[:5]:
            _say(f"  {r.ms:>9,.1f} ms  {'[' + r.section + ']':<12} {r.name}"
                 + (f"   ({r.kb:,.1f} KB)" if r.kb else ""))
        interactions = [r for r in timed_rows
                        if r.section in ("callbacks", "http")
                        and "boot" not in r.name]
        if interactions:
            worst = max(interactions, key=lambda r: r.ms or 0)
            _say("")
            _say(f"  Worst thing a human waits for: {worst.name} - "
                 f"{worst.ms:,.1f} ms"
                 + (f", {worst.kb:,.1f} KB on the wire" if worst.kb else ""))
        _say("=" * 118)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Profile The Bench.")
    parser.add_argument("--json", metavar="PATH",
                        help="also write the rows to this file, for diffing")
    parser.add_argument("--only", metavar="A,B",
                        help="run only these sections: " + ", ".join(SECTIONS))
    parser.add_argument("--no-http", action="store_true",
                        help="skip the section that starts a real server")
    parser.add_argument("--label", default="",
                        help="a name for this run, e.g. 'baseline'")
    args = parser.parse_args(argv)

    wanted = list(SECTIONS)
    if args.only:
        wanted = [s.strip() for s in args.only.split(",") if s.strip() in SECTIONS]
    if args.no_http and "http" in wanted:
        wanted.remove("http")

    import dash
    import numpy
    import pandas
    import plotly

    from bench import app as app_mod

    meta = {
        "when": time.strftime("%Y-%m-%d %H:%M:%S"),
        "label": args.label,
        "python": sys.version.split()[0],
        "platform": f"{platform.system()} {platform.release()} "
                    f"{platform.machine()}, {os.cpu_count()} cpus",
        "packages": f"dash {dash.__version__}, plotly {plotly.__version__}, "
                    f"pandas {pandas.__version__}, numpy {numpy.__version__}",
        "sections": wanted,
    }

    rows: list[Row] = []
    for name in wanted:
        t0 = time.perf_counter()
        rows.extend(SECTIONS[name](sys.modules[app_mod.__name__]))
        _say(f"[{name}] done in {time.perf_counter() - t0:,.1f}s")

    print_table(rows, meta)

    if args.json:
        out = Path(args.json)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({"meta": meta,
                                   "rows": [r.as_dict() for r in rows]},
                                  indent=2), encoding="utf-8")
        _say(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
