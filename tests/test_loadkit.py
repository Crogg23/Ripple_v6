"""Offline unit tests for loadkit -- the load-safety scaffolding. Pure Python, no
Snowflake, no network. conftest.py puts the repo root on sys.path so `from loadkit
import ...` works.

These pin the behaviours the stress-test demanded:
  - fec_parse  : a shifted row is QUARANTINED, never padded into the money columns
  - preflight  : a load whose worst-case crosses the PAT expiry is BLOCKED before start
  - windowed   : a window over the page ceiling is SUBDIVIDED, never silently truncated
  - checkpoint : an interrupted window resumes at the next page
  - atomic_load: the live table is only ever swapped, never half-written
  - smoke      : money that doesn't reconcile to the cent raises (no wrong figure ships)
"""
import datetime as dt

import pandas as pd
import pytest

from loadkit import atomic_load, checkpoint, fec_parse, preflight, smoke, windowed


# =========================================================================== #
# fec_parse -- the "no silently-wrong money" parser
# =========================================================================== #
COLS = ["CMTE_ID", "NAME", "TRANSACTION_AMT", "SUB_ID"]


def test_pipe_clean_rows_parse():
    raw = "C001|SMITH, JOHN|250.00|4081|\nC002|DOE, JANE|500.00|4082|"
    # note: trailing pipe -> 5 fields; use exact-width rows here
    raw = "C001|SMITH, JOHN|250.00|4081\nC002|DOE, JANE|500.00|4082"
    r = fec_parse.parse_pipe(raw, COLS)
    assert r.n_good == 2 and r.n_bad == 0
    assert list(r.good["TRANSACTION_AMT"]) == ["250.00", "500.00"]
    assert list(r.good["SUB_ID"]) == ["4081", "4082"]


def test_pipe_embedded_pipe_row_is_quarantined_not_shifted():
    # An UNQUOTED embedded pipe in NAME makes 5 fields. The old loader padded/truncated
    # and shipped a shifted money column. Here that row is quarantined; the clean row
    # is untouched and its SUB_ID/AMT stay correct.
    raw = "C001|SMITH|JOHN|250.00|4081\nC002|DOE, JANE|500.00|4082"
    r = fec_parse.parse_pipe(raw, COLS)
    assert r.n_good == 1 and r.n_bad == 1
    assert r.quarantine[0]["n_fields"] == 5
    # the surviving good row is the clean one, with money intact
    assert r.good.iloc[0]["TRANSACTION_AMT"] == "500.00"
    assert r.good.iloc[0]["SUB_ID"] == "4082"


def test_pipe_quoted_embedded_pipe_is_kept_whole():
    # A properly QUOTED field with an embedded pipe stays one field (csv quote-aware).
    raw = 'C001|"SMITH|JOHN"|250.00|4081'
    r = fec_parse.parse_pipe(raw, COLS)
    assert r.n_good == 1 and r.n_bad == 0
    assert r.good.iloc[0]["NAME"] == "SMITH|JOHN"
    assert r.good.iloc[0]["TRANSACTION_AMT"] == "250.00"


def test_pipe_blank_lines_skipped():
    raw = "C001|A|1|9\n\n   \nC002|B|2|10"
    r = fec_parse.parse_pipe(raw, COLS)
    assert r.n_good == 2 and r.n_bad == 0


def test_require_clean_passes_under_threshold_and_raises_over():
    good = "\n".join(f"C{i}|N{i}|1|{i}" for i in range(1000))
    r = fec_parse.parse_pipe(good, COLS)
    assert r.require_clean(0.001) is r            # 0 bad -> fine
    raw = "C1|S|M|I|TH|1|9\n" + "\n".join(f"C{i}|N{i}|1|{i}" for i in range(10))
    r2 = fec_parse.parse_pipe(raw, COLS)
    assert r2.n_bad == 1
    with pytest.raises(fec_parse.FecParseError):
        r2.require_clean(0.001)                   # ~9% bad -> stop the load


def test_quarantine_fraction_math():
    raw = "a|b|c|d\nx|y\nC|D|E|F"   # 2 good (4 fields), 1 bad (2 fields)
    r = fec_parse.parse_pipe(raw, COLS)
    assert r.n_good == 2 and r.n_bad == 1
    assert abs(r.quarantine_fraction - (1 / 3)) < 1e-9


def test_parse_csv_header_text_and_validation():
    raw = "CAN_ID,SPE_ID,SUP_OPP,EXP_AMO\nH1,C1,S,1000\nH2,C2,O,2000"
    df = fec_parse.parse_csv(raw, expected_columns=["CAN_ID", "SUP_OPP", "EXP_AMO"])
    assert list(df.columns) == ["CAN_ID", "SPE_ID", "SUP_OPP", "EXP_AMO"]
    assert df.iloc[0]["EXP_AMO"] == "1000"        # stayed TEXT
    assert df.iloc[1]["SUP_OPP"] == "O"


def test_parse_csv_missing_expected_column_raises():
    raw = "CAN_ID,EXP_AMO\nH1,1000"
    with pytest.raises(fec_parse.FecParseError):
        fec_parse.parse_csv(raw, expected_columns=["CAN_ID", "SUP_OPP"])


def test_looks_misparsed():
    one_col = pd.DataFrame({"everything": ["a|b|c"]})
    assert fec_parse.looks_misparsed(one_col) is True
    ok = pd.DataFrame({"a": ["1"], "b": ["2"]})
    assert fec_parse.looks_misparsed(ok) is False


# =========================================================================== #
# preflight -- refuse to start a load that would die mid-stream
# =========================================================================== #
NOW = dt.datetime(2026, 6, 30, 12, 0)
PAT_EXPIRY = dt.datetime(2026, 7, 5, 0, 0)   # the real 5-day cliff


def test_pat_short_load_far_from_expiry_passes():
    c = preflight.pat_check(PAT_EXPIRY, NOW, est_hours=6)   # worst-case 12h
    assert c.ok is True


def test_pat_long_load_crossing_expiry_blocks():
    c = preflight.pat_check(PAT_EXPIRY, NOW, est_hours=72)  # worst-case 144h -> past 07-05
    assert c.ok is False
    assert "rotate" in c.detail.lower()


def test_pat_within_buffer_blocks_even_a_short_load():
    near = dt.datetime(2026, 7, 4, 12, 0)
    c = preflight.pat_check(PAT_EXPIRY, near, est_hours=1)  # finish 07-04 14:00 > deadline 07-04 00:00
    assert c.ok is False


def test_pat_unknown_expiry_blocks():
    assert preflight.pat_check(None, NOW, est_hours=1).ok is False


def test_budget_check_blocks_at_suspend_ceiling():
    assert preflight.budget_check(30, 26, 1).ok is False     # 27 >= 27 (90% of 30)
    assert preflight.budget_check(30, 20, 1).ok is True       # 21 < 27
    assert preflight.budget_check(None, 20, 1).ok is False    # unknown -> block


def test_key_check_expiry_buffer():
    assert preflight.key_check("SAM", dt.datetime(2026, 9, 22), dt.datetime(2026, 9, 21)).ok is False
    assert preflight.key_check("SAM", dt.datetime(2026, 9, 22), dt.datetime(2026, 8, 1)).ok is True
    assert preflight.key_check("SAM", None, NOW).ok is True


def test_dep_check():
    assert preflight.dep_check("committee_master", True).ok is True
    assert preflight.dep_check("committee_master", False).ok is False


def test_preflight_aggregate_and_raise():
    ok = preflight.preflight(
        preflight.pat_check(PAT_EXPIRY, NOW, 6),
        preflight.budget_check(30, 20, 1),
        preflight.dep_check("ccl", True),
    )
    assert ok.ok is True
    ok.raise_if_blocked()  # no raise

    blocked = preflight.preflight(
        preflight.pat_check(PAT_EXPIRY, NOW, 72),
        preflight.budget_check(30, 20, 1),
    )
    assert blocked.ok is False
    with pytest.raises(preflight.PreflightError):
        blocked.raise_if_blocked()


# =========================================================================== #
# windowed -- subdivide below the page ceiling, never silently truncate
# =========================================================================== #
def _count_fn(counts):
    def fn(key):
        return counts.get(tuple(sorted(key.items())), 0)
    return fn


def _subdivide(key):
    # year -> year+quarter; can't split a quarter further
    if "q" not in key and "y" in key:
        return [{**key, "q": q} for q in ("Q1", "Q2")]
    return None


def test_window_small_root_is_one_pageable_leaf():
    counts = {(("y", 2024),): 100}
    leaves, overflow = windowed.plan_windows([{"y": 2024}], _count_fn(counts), _subdivide)
    assert len(leaves) == 1 and leaves[0].pageable and leaves[0].count == 100
    assert overflow == []


def test_window_big_root_subdivides_until_pageable():
    counts = {
        (("y", 2024),): 5000,
        (("q", "Q1"), ("y", 2024)): 1000,
        (("q", "Q2"), ("y", 2024)): 1000,
    }
    leaves, overflow = windowed.plan_windows([{"y": 2024}], _count_fn(counts), _subdivide)
    assert overflow == []
    assert {l.label for l in leaves} == {"y=2024&q=Q1", "y=2024&q=Q2"}
    assert all(l.pageable for l in leaves)


def test_window_unsplittable_overflow_is_surfaced_not_dropped():
    counts = {(("q", "Q1"), ("y", 2024)): 5000}      # already a quarter, can't split
    leaves, overflow = windowed.plan_windows([{"y": 2024, "q": "Q1"}], _count_fn(counts), _subdivide)
    assert len(overflow) == 1 and overflow[0].unsplittable_overflow
    assert leaves[0].pageable is False               # flagged, NOT silently pageable


def test_reconcile_and_assert_complete():
    assert windowed.reconcile(100, 25, 2500) is True      # 2500 >= 2500
    assert windowed.reconcile(99, 25, 2500) is False      # 2475 < 2500
    w = windowed.Window(key={"y": 2024})
    windowed.assert_window_complete(w, 100, 25, 2500)     # no raise
    with pytest.raises(windowed.WindowError):
        windowed.assert_window_complete(w, 99, 25, 2500)


# =========================================================================== #
# checkpoint -- resumable per-window progress
# =========================================================================== #
def test_checkpoint_resume_and_done():
    cs = checkpoint.CheckpointSet("fed_senate_lda")
    cs.mark("y=2024&q=Q1", last_page=2, status="in_progress", envelope_count=50)
    assert cs.resume_page("y=2024&q=Q1") == 3        # next page after the last committed
    assert cs.is_done("y=2024&q=Q1") is False
    cs.mark("y=2024&q=Q1", status="done")
    assert cs.is_done("y=2024&q=Q1") is True
    assert cs.resume_page("y=2024&q=Q1") == 0        # done windows don't resume mid-way


def test_checkpoint_pending_skips_done_in_order():
    cs = checkpoint.CheckpointSet("x")
    cs.mark("w1", status="done")
    cs.mark("w3", status="in_progress", last_page=1)
    assert cs.pending(["w1", "w2", "w3"]) == ["w2", "w3"]


def test_checkpoint_last_page_is_monotonic():
    cs = checkpoint.CheckpointSet("x")
    cs.mark("w", last_page=5, status="in_progress")
    cs.mark("w", last_page=2, status="in_progress")   # a stale lower page must not regress
    assert cs.state["w"]["last_page"] == 5


def test_checkpoint_fresh_window_resumes_at_zero():
    cs = checkpoint.CheckpointSet("x")
    assert cs.resume_page("never-seen") == 0


def test_checkpoint_ddl_is_idempotent_sql():
    assert "CREATE TABLE IF NOT EXISTS" in checkpoint.CHECKPOINT_DDL
    assert checkpoint.CHECKPOINT_TABLE in checkpoint.CHECKPOINT_DDL


# =========================================================================== #
# atomic_load -- only ever swap a fully-built table over the live one
# =========================================================================== #
def test_staging_name():
    assert atomic_load.staging_name("FED_FEC_PAS2") == "FED_FEC_PAS2__STAGING"


def test_swap_plan_statements():
    plan = atomic_load.swap_plan("FED_FEC_PAS2", database="LIBRARY_RAW", schema="LANDING")
    assert "SWAP WITH" in plan["swap_if_exists"]
    assert '"LIBRARY_RAW"."LANDING"."FED_FEC_PAS2"' in plan["swap_if_exists"]
    assert '"LIBRARY_RAW"."LANDING"."FED_FEC_PAS2__STAGING"' in plan["swap_if_exists"]
    assert "RENAME TO" in plan["rename_if_absent"]
    assert plan["drop_staging"].startswith("DROP TABLE IF EXISTS")


# =========================================================================== #
# smoke -- a load isn't "done" until its numbers tie to the cent
# =========================================================================== #
def test_reconcile_within_and_outside_tolerance():
    smoke.reconcile(100, 100, label="exact")
    smoke.reconcile(100, 99, label="tol_abs", tol_abs=1)
    smoke.reconcile(100, 90, label="tol_pct", tol_pct=0.2)     # allowed 18, diff 10
    with pytest.raises(smoke.SmokeFailure):
        smoke.reconcile(100, 90, label="too_far")


def test_penny_reconcile_exact_and_off_by_a_cent():
    smoke.penny_reconcile(8840571.03, 8840571.03, label="warren_2024")   # the real figure
    with pytest.raises(smoke.SmokeFailure):
        smoke.penny_reconcile(8840571.03, 8840571.04, label="warren_off_by_cent")


def test_smoke_result_fields():
    res = smoke.reconcile(5.0, 5.0, label="ok")
    assert res.ok is True and res.measured == 5.0 and res.expected == 5.0
