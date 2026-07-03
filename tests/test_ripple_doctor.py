"""Offline unit tests for ripple/doctor.py -- the go/no-go health check.

Everything here is pure: no live Snowflake, no real scheduled-task query, no disk
writes beyond a tmp_path DR dir. We pin:
  - verdict()            : results -> (exit_code, headline) aggregation. BAD blocks,
                           WARN never does, empty is vacuously GREEN.
  - check_dr_export_age  : given a fake backups/dr path + a fixed clock.
  - check_freshness      : given sample grouped rows (dead -> BAD, pile -> WARN, None
                           -> 'ledger not deployed').
  - check_budget         : headroom to the suspend line.
  - check_deps / check_keys : injected import_module / getenv so no real env needed.
"""
import datetime as dt
import os

from ripple import doctor as D

UTC = dt.timezone.utc
NOW = dt.datetime(2026, 7, 2, 12, 0, 0, tzinfo=UTC)


# =========================================================================== #
# verdict -- the pure aggregation at the core
# =========================================================================== #
def test_verdict_all_ok_is_green_exit_0():
    code, headline = D.verdict([(D.OK, "a", "d"), (D.OK, "b", "d")])
    assert code == 0
    assert headline.startswith("GREEN")


def test_verdict_warn_never_blocks():
    code, headline = D.verdict([(D.OK, "a", "d"), (D.WARN, "b", "advisory")])
    assert code == 0
    assert "GREEN" in headline


def test_verdict_single_bad_is_red_exit_1_singular():
    code, headline = D.verdict([(D.OK, "a", "d"), (D.BAD, "b", "boom")])
    assert code == 1
    assert "1 blocking problem" in headline
    assert "problems" not in headline   # singular, no trailing 's'


def test_verdict_multiple_bad_pluralizes():
    code, headline = D.verdict([(D.BAD, "a", "x"), (D.BAD, "b", "y"), (D.WARN, "c", "z")])
    assert code == 1
    assert "2 blocking problems" in headline


def test_verdict_empty_is_vacuously_green():
    code, headline = D.verdict([])
    assert code == 0 and "GREEN" in headline


# =========================================================================== #
# check_dr_export_age -- fake path + fixed clock
# =========================================================================== #
def test_dr_missing_dir_warns(tmp_path):
    status, name, _ = D.check_dr_export_age(tmp_path / "nope", NOW)
    assert status == D.WARN and name == "dr_export_age"


def test_dr_empty_dir_warns(tmp_path):
    root = tmp_path / "dr"
    root.mkdir()
    status, _, detail = D.check_dr_export_age(root, NOW)
    assert status == D.WARN
    assert "no export subdirs" in detail


def test_dr_recent_export_is_ok(tmp_path):
    root = tmp_path / "dr"
    (root / "20260702_091350").mkdir(parents=True)
    # mtime is 'now' -> age ~0 -> OK. Clock is 'now' too.
    status, _, _ = D.check_dr_export_age(root, D.C.now())
    assert status == D.OK


def test_dr_stale_export_warns(tmp_path):
    root = tmp_path / "dr"
    old = root / "20260101_000000"
    old.mkdir(parents=True)
    # Push the clock 30 days past the dir's real mtime -> stale WARN.
    from datetime import datetime, timezone
    mtime = datetime.fromtimestamp(old.stat().st_mtime, tz=timezone.utc)
    status, _, detail = D.check_dr_export_age(root, mtime + dt.timedelta(days=30))
    assert status == D.WARN
    assert "old" in detail


def test_dr_picks_newest_of_several(tmp_path):
    import time
    root = tmp_path / "dr"
    root.mkdir()
    (root / "20250101_000000").mkdir()
    time.sleep(0.01)
    newest = root / "20260702_091350"
    newest.mkdir()
    status, _, detail = D.check_dr_export_age(root, D.C.now())
    assert status == D.OK
    assert "20260702_091350" in detail


# =========================================================================== #
# check_freshness -- sample grouped rows
# =========================================================================== #
def test_freshness_none_means_ledger_not_deployed():
    status, name, detail = D.check_freshness(None)
    assert status == D.WARN
    assert "not deployed" in detail


def test_freshness_any_dead_is_bad():
    rows = [("fresh", 30), ("dead", 2), ("stale", 5)]
    status, _, detail = D.check_freshness(rows)
    assert status == D.BAD
    assert "DEAD" in detail


def test_freshness_large_overdue_stale_pile_warns():
    rows = [("fresh", 10), ("overdue", 12), ("stale", 20)]  # 32 >= threshold
    status, _, detail = D.check_freshness(rows)
    assert status == D.WARN
    assert "overdue+stale" in detail


def test_freshness_healthy_is_ok():
    rows = [("fresh", 32), ("due", 3), ("overdue", 2), ("stale", 4)]  # 6 < threshold, no dead
    status, _, _ = D.check_freshness(rows)
    assert status == D.OK


def test_freshness_dead_beats_large_pile():
    # A dead source must dominate even when the overdue+stale pile is huge.
    rows = [("dead", 1), ("overdue", 40), ("stale", 40)]
    status, _, _ = D.check_freshness(rows)
    assert status == D.BAD


def test_freshness_tolerates_none_state_and_empty():
    assert D.check_freshness([])[0] == D.OK
    # a None/blank state label shouldn't crash -- it buckets as 'unknown'
    assert D.check_freshness([(None, 3)])[0] == D.OK


# =========================================================================== #
# check_budget -- headroom to the suspend line
# =========================================================================== #
def test_budget_unreadable_warns():
    assert D.check_budget(None, None)[0] == D.WARN
    assert D.check_budget(100, None)[0] == D.WARN


def test_budget_thin_headroom_warns():
    # quota 100 -> ceiling 90; used 80 -> headroom 10 < 15 -> WARN
    status, _, detail = D.check_budget(100.0, 80.0)
    assert status == D.WARN
    assert "suspend line" in detail


def test_budget_fat_headroom_is_ok():
    # quota 100 -> ceiling 90; used 20 -> headroom 70 -> OK
    status, _, _ = D.check_budget(100.0, 20.0)
    assert status == D.OK


def test_budget_headroom_boundary():
    # ceiling 90; used 75 -> headroom exactly 15 -> NOT under 15 -> OK
    assert D.check_budget(100.0, 75.0)[0] == D.OK
    # used 75.1 -> headroom 14.9 < 15 -> WARN
    assert D.check_budget(100.0, 75.1)[0] == D.WARN


# =========================================================================== #
# check_deps -- injected import_module
# =========================================================================== #
def test_deps_all_present_is_ok():
    status, _, _ = D.check_deps(import_module=lambda name: object())
    assert status == D.OK


def test_deps_missing_one_is_bad():
    def fake_import(name):
        if name == "plotly":
            raise ImportError("no plotly")
        return object()
    status, _, detail = D.check_deps(import_module=fake_import)
    assert status == D.BAD
    assert "plotly" in detail


# =========================================================================== #
# check_keys -- injected getenv
# =========================================================================== #
def _env(**overrides):
    base = {}
    def getenv(name, default=""):
        return overrides.get(name, default)
    return getenv


def test_keys_missing_snowflake_creds_is_bad():
    status, _, detail = D.check_keys(getenv=_env())  # nothing set
    assert status == D.BAD
    assert "SNOWFLAKE_ACCOUNT" in detail


def test_keys_missing_auth_only_is_bad():
    getenv = _env(SNOWFLAKE_ACCOUNT="acct", SNOWFLAKE_USER="me")  # no PAT/password
    status, _, detail = D.check_keys(getenv=getenv)
    assert status == D.BAD
    assert "PAT/PASSWORD" in detail


def test_keys_creds_present_optional_unset_warns():
    getenv = _env(SNOWFLAKE_ACCOUNT="acct", SNOWFLAKE_USER="me", SNOWFLAKE_PAT="tok")
    status, _, detail = D.check_keys(getenv=getenv)
    assert status == D.WARN
    assert "optional key" in detail


def test_keys_all_present_is_ok():
    kw = {"SNOWFLAKE_ACCOUNT": "a", "SNOWFLAKE_USER": "u", "SNOWFLAKE_PASSWORD": "p"}
    for k in D.OPTIONAL_KEYS:
        kw[k] = "set"
    status, _, _ = D.check_keys(getenv=_env(**kw))
    assert status == D.OK


def test_keys_password_counts_as_auth():
    getenv = _env(SNOWFLAKE_ACCOUNT="a", SNOWFLAKE_USER="u", SNOWFLAKE_PASSWORD="p")
    # missing PAT is fine as long as PASSWORD is present -> not BAD
    assert D.check_keys(getenv=getenv)[0] != D.BAD


# =========================================================================== #
# run() smoke -- verify it never crashes and honors --json, with checks stubbed
# =========================================================================== #
class _Args:
    def __init__(self, as_json=False):
        self.json = as_json


def test_run_json_path_with_stubbed_gather(monkeypatch, capsys):
    stub = [(D.OK, "deps", "ok"), (D.WARN, "keys", "advisory")]
    monkeypatch.setattr(D, "gather_checks", lambda: stub)
    code = D.run(_Args(as_json=True))
    assert code == 0
    out = capsys.readouterr().out
    import json
    payload = json.loads(out)
    assert payload["verdict"] == "GREEN"
    assert len(payload["checks"]) == 2


def test_run_table_path_reports_red_on_bad(monkeypatch, capsys):
    stub = [(D.OK, "deps", "ok"), (D.BAD, "snowflake_reachable", "down")]
    monkeypatch.setattr(D, "gather_checks", lambda: stub)
    code = D.run(_Args(as_json=False))
    assert code == 1
    out = capsys.readouterr().out
    assert "RED" in out
    assert "STATUS" in out   # the table header rendered
