"""Offline gate tests for scripts/publish_pattern.py — no Snowflake needed.

The pattern publisher must refuse bad input BEFORE it ever reaches for a
credential, mirroring publish_lead.py's guard order.
"""

import importlib.util
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]


def _load():
    spec = importlib.util.spec_from_file_location(
        "publish_pattern", _REPO / "scripts" / "publish_pattern.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _run(argv):
    mod = _load()
    old = sys.argv
    sys.argv = ["publish_pattern.py"] + argv
    try:
        return mod.main()
    finally:
        sys.argv = old


def test_refuses_empty_cohort_id(capsys):
    assert _run(["  ", "--by", "chris"]) == 2
    assert "not a publishable cohort id" in capsys.readouterr().out


def test_refuses_smoke_test(capsys):
    assert _run(["SMOKE_TEST", "--by", "chris"]) == 2
    assert "not a publishable cohort id" in capsys.readouterr().out


def test_apply_requires_reason(capsys):
    assert _run(["3363|100-249", "--by", "chris", "--apply"]) == 2
    assert "requires --reason" in capsys.readouterr().out


def test_halts_without_review_pat(capsys, monkeypatch):
    # With valid args but no publish-lane credential, it must HALT (never
    # fall back to another credential) — and must not have connected.
    # Load first: the module's load_dotenv(override=True) runs at import and
    # would clobber a pre-set monkeypatch value with the real .env PAT.
    mod = _load()
    monkeypatch.setenv("RIPPLE_REVIEW_PAT", "")
    old = sys.argv
    sys.argv = ["publish_pattern.py", "3363|100-249", "--by", "chris"]
    try:
        assert mod.main() == 2
    finally:
        sys.argv = old
    assert "RIPPLE_REVIEW_PAT is not set" in capsys.readouterr().out
