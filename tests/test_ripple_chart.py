"""ripple/chart.py — the verb must be stdlib-only at import time (the dispatcher
imports every verb eagerly; offline CI collects without plotly)."""

import argparse
import builtins
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


def test_import_chart_with_plotly_blocked(monkeypatch):
    for mod in list(sys.modules):
        if mod.startswith(("ripple.chart", "plotly")):
            monkeypatch.delitem(sys.modules, mod, raising=False)
    real_import = builtins.__import__

    def block_plotly(name, *a, **kw):
        if name.startswith("plotly"):
            raise ImportError("plotly blocked for this test")
        return real_import(name, *a, **kw)

    monkeypatch.setattr(builtins, "__import__", block_plotly)
    import importlib
    mod = importlib.import_module("ripple.chart")
    assert hasattr(mod, "add_arguments") and hasattr(mod, "run")


def test_dispatcher_knows_chart():
    from ripple.__main__ import VERBS, build_parser
    assert "chart" in VERBS
    build_parser()  # wiring the subparsers must not raise


def test_add_arguments_on_bare_parser():
    from ripple import chart
    p = argparse.ArgumentParser()
    chart.add_arguments(p)
    args = p.parse_args(["find", "fec", "--portals"])
    assert args.args == ["find", "fec"] and args.portals


def test_unknown_action_treated_as_sql():
    from ripple import chart
    p = argparse.ArgumentParser()
    chart.add_arguments(p)
    args = p.parse_args(["SELECT 1"])
    tokens = list(args.args)
    action = tokens.pop(0) if tokens and tokens[0] in chart.ACTIONS else "run"
    assert action == "run"


def test_bom_sniffing(tmp_path):
    from ripple.chart import _read_sql_file
    utf16 = tmp_path / "q16.sql"
    utf16.write_bytes("SELECT 1".encode("utf-16"))          # PowerShell default
    assert _read_sql_file(str(utf16)).strip() == "SELECT 1"
    utf8sig = tmp_path / "q8.sql"
    utf8sig.write_bytes(b"\xef\xbb\xbfSELECT 2")
    assert _read_sql_file(str(utf8sig)).strip() == "SELECT 2"


def test_coerce_arg_values():
    from ripple.chart import _coerce
    assert _coerce("true") is True and _coerce("false") is False
    assert _coerce("42") == 42 and _coerce("4.2") == 4.2
    assert _coerce("STATE") == "STATE"


# ---- the libel firewall extends to every rendering surface -------------------- #
def test_no_raw_claim_table_sql_in_viz_or_chart():
    """No module may SELECT from LIBRARY_META."CONNECT".LEADS directly — reads go
    through viz.sqlrun (which blocks and reroutes to V_LEADS_PUBLISHED)."""
    import re
    offenders = []
    for path in list((REPO / "viz").glob("*.py")) + [REPO / "ripple" / "chart.py"]:
        text = path.read_text(encoding="utf-8")
        if re.search(r'FROM\s+LIBRARY_META\."?CONNECT"?\.(LEADS|ENTITY_LINKS|ENTITY_MAP)\b',
                     text, re.IGNORECASE):
            offenders.append(path.name)
    assert not offenders, f"raw claim-table SQL in: {offenders}"


def test_run_question_routes_through_sqlrun():
    text = (REPO / "ripple" / "chart.py").read_text(encoding="utf-8")
    assert "sqlrun.run(" in text


# ---- review regressions (2026-07-03) ------------------------------------------ #
def test_wrap_limit_survives_trailing_line_comment():
    from viz import sqlrun
    wrapped = sqlrun.wrap_limit("SELECT 1 FROM t -- top states", 10)
    # the closing paren must be on its own line, out of the comment's reach
    assert "\n) LIMIT 11" in wrapped


def test_wrap_limit_leaves_show_alone():
    from viz import sqlrun
    assert sqlrun.wrap_limit("SHOW WAREHOUSES", 10) == "SHOW WAREHOUSES"
