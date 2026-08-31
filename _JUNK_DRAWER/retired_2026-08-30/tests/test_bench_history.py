"""Never lose work: undo/redo, save/load, restore-on-reload, knob carry-over.

    python -m pytest tests/test_bench_history.py -q

Headless, same style as tests/test_bench_app.py: `sync_spec` is called with a
faked callback context and the raw outputs are asserted on directly.
"""

from __future__ import annotations

import base64
import json
import sys
from pathlib import Path

import pytest
from dash import no_update
from dash._callback_context import context_value
from dash._utils import AttributeDict

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bench import app as bench_app  # noqa: E402
from bench import registry  # noqa: E402


def _fire(prop_id, *, spec, history=None, **overrides):
    """Call sync_spec once. Returns (spec, echo, message, history, persist)."""
    args = dict(
        _chart_clicks=[0] * len(registry.TEMPLATES),
        knob_values=[],
        _row_clicks=[],
        draft=None, _blur=None, _reset=None,
        src_kind=spec["source"].get("kind", "demo"),
        src_demo=spec["source"].get("name", bench_app.START_DEMO),
        _run=None,
        _undo=None, _redo=None, load_contents=None, restore_data=None,
        code_value="", sql=spec["source"].get("sql", ""),
        spec=spec, echo={"code": ""}, knob_echo={"knobs": {}},
        history=history or {"past": [], "future": []},
    )
    args.update(overrides)
    inputs_list = [
        [{"id": {"bench": "chart", "key": t.key}, "property": "n_clicks",
          "value": 0} for t in registry.TEMPLATES],
        [],
    ]
    context_value.set(AttributeDict(
        triggered_inputs=[{"prop_id": prop_id, "value": None}],
        inputs_list=inputs_list,
    ))
    try:
        return bench_app.sync_spec(**args)
    finally:
        context_value.set({})


def _spec_with(**over):
    spec = bench_app.blank_spec()
    spec.update(over)
    return spec


# ---------------------------------------------------------------- history


def test_a_real_change_pushes_the_old_spec_onto_the_undo_stack():
    spec = bench_app.blank_spec()
    key = json.dumps({"bench": "chart", "key": "scatter"}, sort_keys=True)
    new, _e, _m, history, persist = _fire(f"{key}.n_clicks", spec=spec)
    assert new is not no_update and new["chart"] == "scatter"
    assert history["past"][-1]["chart"] == spec["chart"]
    assert history["future"] == []
    assert persist == new                     # the localStorage mirror rides along


def test_undo_restores_and_redo_comes_back():
    old = bench_app.blank_spec()
    now = _spec_with(knobs={"layout.title.text": "hello"})
    history = {"past": [old], "future": []}

    back, _e, _m, h2, p2 = _fire("bench-undo.n_clicks", spec=now, history=history)
    assert back == old
    assert h2["future"][-1] == now and h2["past"] == []
    assert p2 == old

    fwd, _e, _m, h3, p3 = _fire("bench-redo.n_clicks", spec=back, history=h2)
    assert fwd == now
    assert h3["past"][-1] == old and h3["future"] == []


def test_undo_with_nothing_to_undo_says_so_and_writes_nothing():
    spec = bench_app.blank_spec()
    out, _e, msg, hist, persist = _fire("bench-undo.n_clicks", spec=spec)
    assert out is no_update and hist is no_update and persist is no_update
    assert "nothing to undo" in msg


def test_the_undo_stack_is_capped():
    spec = bench_app.blank_spec()
    history = {"past": [bench_app.blank_spec()] * bench_app.HISTORY_CAP,
               "future": []}
    key = json.dumps({"bench": "chart", "key": "scatter"}, sort_keys=True)
    _new, _e, _m, h2, _p = _fire(f"{key}.n_clicks", spec=spec, history=history)
    assert len(h2["past"]) == bench_app.HISTORY_CAP


def test_a_new_edit_clears_the_redo_stack():
    spec = bench_app.blank_spec()
    history = {"past": [], "future": [_spec_with(chart="scatter")]}
    key = json.dumps({"bench": "chart", "key": "line_chart"}, sort_keys=True)
    if "line_chart" not in registry.CHARTS:      # key name varies by registry
        key = json.dumps({"bench": "chart", "key": "scatter"}, sort_keys=True)
    _new, _e, _m, h2, _p = _fire(f"{key}.n_clicks", spec=spec, history=history)
    assert h2["future"] == []


# ---------------------------------------------------------------- save/load


def _as_upload(payload: dict) -> str:
    raw = base64.b64encode(json.dumps(payload).encode("utf-8")).decode("ascii")
    return f"data:application/json;base64,{raw}"


def test_a_saved_spec_loads_back_exactly():
    saved = _spec_with(knobs={"layout.title.text": "from disk"})
    spec = bench_app.blank_spec()
    new, _e, msg, _h, persist = _fire("bench-load.contents", spec=spec,
                                      load_contents=_as_upload(saved))
    assert new == saved
    assert persist == saved
    assert "loaded" in msg


def test_save_produces_the_json_the_load_gate_accepts():
    spec = _spec_with(knobs={"trace.marker.opacity": 0.5})
    context_value.set(AttributeDict(
        triggered_inputs=[{"prop_id": "bench-save.n_clicks", "value": 1}]))
    try:
        got = bench_app.export_chart(0, 0, 1, spec)
    finally:
        context_value.set({})
    assert got["filename"].endswith(".json")
    loaded, why = bench_app._valid_spec(json.loads(got["content"]))
    assert loaded == spec and why == ""


def test_a_garbage_file_is_refused_with_a_reason():
    spec = bench_app.blank_spec()
    out, _e, msg, hist, _p = _fire("bench-load.contents", spec=spec,
                                   load_contents="data:text/plain;base64,bm9wZQ==")
    assert out is no_update
    assert msg


def test_a_spec_naming_an_unknown_chart_is_refused():
    bad = _spec_with(chart="chart_that_never_was")
    spec = bench_app.blank_spec()
    out, _e, msg, _h, _p = _fire("bench-load.contents", spec=spec,
                                 load_contents=_as_upload(bad))
    assert out is no_update
    assert "not a chart in this registry" in msg


# ---------------------------------------------------------------- restore


def test_restore_adopts_a_valid_persisted_spec():
    persisted = _spec_with(knobs={"layout.title.text": "last night"})
    spec = bench_app.blank_spec()
    new, _e, msg, _h, _p = _fire("bench-restore-req.data", spec=spec,
                                 restore_data=persisted)
    assert new == persisted
    assert "restored" in msg


def test_restore_of_garbage_is_silent():
    spec = bench_app.blank_spec()
    out, _e, msg, _h, _p = _fire("bench-restore-req.data", spec=spec,
                                 restore_data={"not": "a spec"})
    assert out is no_update
    assert msg == ""


def test_a_restored_warehouse_spec_never_touches_snowflake_by_itself():
    """The deferred flag makes bench.data answer 'press RUN' instead of running."""
    persisted = _spec_with(source={"kind": "warehouse",
                                   "sql": "SELECT 1 AS X"})
    spec = bench_app.blank_spec()
    new, _e, msg, _h, _p = _fire("bench-restore-req.data", spec=spec,
                                 restore_data=persisted)
    assert new["source"]["deferred"] is True
    assert "RUN" in msg

    from bench import data

    df, meta = data.frame(new["source"])
    assert meta["ok"] is False
    assert meta["lane"] == "idle"
    assert "press RUN" in meta["error"]
    assert len(df) == 0


def test_the_idle_lane_has_a_badge_colour_and_a_meaning():
    assert "idle" in bench_app.LANE_COLOUR
    assert "idle" in bench_app.LANE_MEANING


# ---------------------------------------------------------------- carry-over


def test_a_chart_switch_keeps_the_knobs_the_new_chart_also_has():
    spec = _spec_with(knobs={"layout.title.text": "kept",
                             "trace.marker.opacity": 0.5})
    key = json.dumps({"bench": "chart", "key": "scatter"}, sort_keys=True)
    new, _e, _m, _h, _p = _fire(f"{key}.n_clicks", spec=spec)
    assert new["chart"] == "scatter"
    assert new["knobs"].get("layout.title.text") == "kept"


def test_a_chart_switch_drops_knobs_with_no_home_and_says_so():
    spec = _spec_with(knobs={"trace.connector.line.width": 3})  # waterfall-only
    key = json.dumps({"bench": "chart", "key": "scatter"}, sort_keys=True)
    new, _e, msg, _h, _p = _fire(f"{key}.n_clicks", spec=spec)
    assert "trace.connector.line.width" not in new["knobs"]
    assert "dropped" in msg


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
