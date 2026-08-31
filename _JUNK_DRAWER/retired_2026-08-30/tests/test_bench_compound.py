"""The annotations/shapes editor: add/remove rows, field folding, round trip.

    python -m pytest tests/test_bench_compound.py -q

layout.annotations and layout.shapes used to render as a dead type-a-list
text box. They now carry controls' "compound" editor: one bordered group per
row with the fields that matter, plus add / remove buttons. The value in the
spec stays a plain list of dicts, so codegen, the figure builder and the
one-writer flow needed no changes - these tests prove that stayed true.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bench import app as bench_app  # noqa: E402
from bench import codegen, controls, knobs  # noqa: E402

ANN = "layout.annotations"
SHP = "layout.shapes"


# ---------------------------------------------------------------- rows


def test_add_appends_a_default_row_that_draws_anywhere():
    spec = bench_app.blank_spec()
    spec, _ = bench_app._apply_compound_row(
        spec, {"bench": "knobrow", "path": ANN, "op": "add", "index": -1})
    rows = spec["knobs"][ANN]
    assert len(rows) == 1
    assert rows[0]["xref"] == "paper" and rows[0]["yref"] == "paper"


def test_remove_deletes_the_named_row_and_an_empty_list_leaves_the_spec():
    spec = bench_app.blank_spec()
    for _ in range(2):
        spec, _ = bench_app._apply_compound_row(
            spec, {"bench": "knobrow", "path": ANN, "op": "add", "index": -1})
    spec["knobs"][ANN][0]["text"] = "first"
    spec, _ = bench_app._apply_compound_row(
        spec, {"bench": "knobrow", "path": ANN, "op": "remove", "index": 0})
    assert len(spec["knobs"][ANN]) == 1
    assert spec["knobs"][ANN][0]["text"] != "first"
    spec, _ = bench_app._apply_compound_row(
        spec, {"bench": "knobrow", "path": ANN, "op": "remove", "index": 0})
    assert ANN not in spec["knobs"]      # empty -> back to Plotly's default


def test_an_unknown_path_or_bad_index_changes_nothing():
    spec = bench_app.blank_spec()
    out, _ = bench_app._apply_compound_row(
        spec, {"bench": "knobrow", "path": "layout.sliders", "op": "add",
               "index": -1})
    assert out["knobs"] == {}
    out, _ = bench_app._apply_compound_row(
        spec, {"bench": "knobrow", "path": ANN, "op": "remove", "index": 5})
    assert out["knobs"] == {}


# ---------------------------------------------------------------- folding


def _one_annotation():
    spec = bench_app.blank_spec()
    spec, _ = bench_app._apply_compound_row(
        spec, {"bench": "knobrow", "path": ANN, "op": "add", "index": -1})
    return spec


def test_field_edits_fold_back_into_the_row():
    spec = _one_annotation()
    bench_app._fold_compound_field(spec, ANN, 0, "text", "the subpoena landed")
    bench_app._fold_compound_field(spec, ANN, 0, "x", "0.25")
    bench_app._fold_compound_field(spec, ANN, 0, "showarrow", "yes")
    row = spec["knobs"][ANN][0]
    assert row["text"] == "the subpoena landed"
    assert row["x"] == 0.25 and isinstance(row["x"], float)
    assert row["showarrow"] is True


def test_a_category_coordinate_stays_a_string():
    spec = _one_annotation()
    bench_app._fold_compound_field(spec, ANN, 0, "x", "March")
    assert spec["knobs"][ANN][0]["x"] == "March"


def test_a_dotted_field_reaches_the_nested_dict():
    spec = bench_app.blank_spec()
    spec, _ = bench_app._apply_compound_row(
        spec, {"bench": "knobrow", "path": SHP, "op": "add", "index": -1})
    bench_app._fold_compound_field(spec, SHP, 0, "line.color", "#00ff00")
    assert spec["knobs"][SHP][0]["line"]["color"] == "#00ff00"


def test_a_numeric_looking_annotation_text_stays_text():
    spec = _one_annotation()
    bench_app._fold_compound_field(spec, ANN, 0, "text", "42")
    assert spec["knobs"][ANN][0]["text"] == "42"


def test_out_of_range_fold_is_a_no_op():
    spec = _one_annotation()
    before = [dict(r) for r in spec["knobs"][ANN]]
    bench_app._fold_compound_field(spec, ANN, 7, "text", "ghost")
    assert spec["knobs"][ANN] == before


# ---------------------------------------------------------------- round trip


def test_annotations_survive_render_parse_and_draw():
    spec = _one_annotation()
    bench_app._fold_compound_field(spec, ANN, 0, "text", "receipt")
    code = bench_app.render_code(spec)
    back, why = codegen.parse_why(code)
    assert back is not None, why
    assert back["knobs"][ANN] == spec["knobs"][ANN]

    df, meta = bench_app.get_frame(spec["source"])
    fig, err = bench_app.figure_for(spec, df, meta)
    assert err == ""
    assert len(fig.layout.annotations) == 1
    assert fig.layout.annotations[0].text == "receipt"


def test_shapes_survive_the_same_trip():
    spec = bench_app.blank_spec()
    spec, _ = bench_app._apply_compound_row(
        spec, {"bench": "knobrow", "path": SHP, "op": "add", "index": -1})
    code = bench_app.render_code(spec)
    back, why = codegen.parse_why(code)
    assert back is not None, why
    df, meta = bench_app.get_frame(spec["source"])
    fig, err = bench_app.figure_for(spec, df, meta)
    assert err == ""
    assert len(fig.layout.shapes) == 1


# ---------------------------------------------------------------- widgets


def _annotation_knob():
    return next(k for k in knobs.flat("bar", ["a", "b"])
                if k.path == ANN)


def test_the_knob_is_marked_compound():
    assert _annotation_knob().control == "compound"
    assert next(k for k in knobs.flat("bar", ["a"])
                if k.path == SHP).control == "compound"


def _ids(component):
    for node in component._traverse():
        cid = getattr(node, "id", None)
        if isinstance(cid, dict):
            yield cid


def test_the_editor_renders_indexed_field_widgets_and_buttons():
    value = [{"text": "hi", "x": 0.5, "y": 0.5, "showarrow": False}]
    comp = controls.control(_annotation_knob(), value)
    ids = list(_ids(comp))
    knob_paths = {c["path"] for c in ids if c.get("bench") == "knob"}
    assert f"{ANN}[0].text" in knob_paths
    assert f"{ANN}[0].x" in knob_paths
    ops = {(c.get("op"), c.get("index")) for c in ids
           if c.get("bench") == "knobrow"}
    assert ("add", -1) in ops
    assert ("remove", 0) in ops


def test_an_empty_editor_still_offers_add():
    comp = controls.control(_annotation_knob(), None)
    ops = {c.get("op") for c in _ids(comp) if c.get("bench") == "knobrow"}
    assert ops == {"add"}


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
