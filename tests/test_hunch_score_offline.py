"""Offline locks for the Hunch Engine surprise scorer — no network, no
Snowflake. What they hold:

  * the null constants come from connect (KEY_DOMAIN) — an un-domained key
    RAISES, never defaults
  * absence is only surprising when value spaces meet: partitioned prefix
    sets / disjoint ranges clamp S to 0 ("partitioned"), missing range data
    makes absence UNSCORABLE (None) — never fabricated either way
  * truncated prefix sets fall back to the range test and say so
  * the calibration bands reproduce: verified-real >> chance, and the
    CCN-style partitioned zero lands at 0, not at dramatic absence
  * Poisson fluke math is exact on hand-checkable cases; ranked rows carry
    expected-flukes-at-rank and the promotable rule (S > band AND flukes < 1)
  * hunch/score.py stays pure (same lock as census.py)
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from hunch import score  # noqa: E402


def _entry(distinct, mn=None, mx=None, prefixes=None, prefix_count=None):
    e = {"distinct": distinct}
    if mn is not None:
        e.update({"min": mn, "max": mx,
                  "prefixes": prefixes or [], "prefix_count": prefix_count or len(prefixes or [])})
    return e


# ── null constants ──────────────────────────────────────────────────────────

def test_undomained_key_raises():
    with pytest.raises(KeyError):
        score.expected_chance(10, 10, "NOT_A_KEY")


def test_expected_chance_matches_discover_math():
    from connect.discover import KEY_DOMAIN
    assert score.expected_chance(1000, 2000, "NPI") == 1000 * 2000 / KEY_DOMAIN["NPI"]


# ── range conditioning ──────────────────────────────────────────────────────

def test_partitioned_prefixes_clamp_absence_to_zero():
    # CCN facility-type shape: ranges interleave but prefixes are disjoint
    a = _entry(5000, "300001", "349999", ["30", "31", "32", "33", "34"])
    b = _entry(8000, "550001", "559999", ["55"])
    r = score.score_pair("CCN", a, b, matched=0)
    assert r["band"] == "partitioned"
    assert r["s"] == 0.0
    assert r["absence_valid"] is False


def test_disjoint_ranges_detected_without_prefixes():
    a = _entry(100, "0000001", "0999999", ["00", "01"])
    b = _entry(100, "5000000", "5999999", ["50"])
    ro = score.range_overlap(a, b)
    assert ro["meets"] is False and ro["conditioned"] is True


def test_missing_range_data_makes_absence_unscorable_not_boring():
    a = _entry(500_000)                          # pre-fmt-2 entry: no min/max
    b = _entry(500_000)
    r = score.score_pair("CCN", a, b, matched=0)
    assert r["band"] == "absence-unscorable"
    assert r["s"] is None                        # never fabricated


def test_truncated_prefixes_fall_back_to_range_test():
    from connect.fingerprint import PREFIX_CAP
    dense = [f"{i:02d}" for i in range(PREFIX_CAP)]
    a = _entry(10_000, "A", "Z", dense, prefix_count=500)
    b = _entry(10_000, "M", "Q", ["55"], prefix_count=1)
    ro = score.range_overlap(a, b)
    assert ro["meets"] is True
    assert "truncated" in ro["reason"]


# ── calibration bands reproduce ─────────────────────────────────────────────

def test_verified_real_scores_high_and_chance_scores_low():
    shared = {"min": "0000000001", "max": "9999999999", "prefixes": ["10", "11"],
              "prefix_count": 2}
    a = {**_entry(9_606_683), **shared}
    b = {**_entry(1_416_883), **shared}
    real = score.score_pair("NPI", a, b, matched=1_416_881)     # the NPPES edge
    assert real["band"] == "excess" and real["s"] > 3.0
    tiny = score.score_pair("NPI", {**_entry(200), **shared},
                            {**_entry(300), **shared}, matched=0)
    assert tiny["band"] == "chance" and abs(tiny["s"]) < 0.1


def test_valid_absence_scores_negative():
    shared = {"min": "000001", "max": "999999",
              "prefixes": ["10", "20"], "prefix_count": 2}
    a = {**_entry(300_000), **shared}
    b = {**_entry(300_000), **shared}
    r = score.score_pair("CCN", a, b, matched=0)                # E = 9e4
    assert r["band"] == "absence" and r["s"] < -3


# ── fluke math ──────────────────────────────────────────────────────────────

def test_poisson_tail_exact_cases():
    assert score.poisson_tail(1.0, 0) == 1.0
    assert score.poisson_tail(0.0, 5) == 0.0
    # P(X>=1) = 1 - e^-lam
    assert math.isclose(score.poisson_tail(2.0, 1), 1 - math.exp(-2.0), rel_tol=1e-9)
    # P(X>=2 | lam=1) = 1 - 2/e
    assert math.isclose(score.poisson_tail(1.0, 2), 1 - 2 / math.e, rel_tol=1e-9)


def test_poisson_tail_fast_and_correct_for_huge_k():
    import time
    t0 = time.perf_counter()
    v = score.poisson_tail(0.001, 10**7)      # froze the 2026-08-01 sieve run
    assert time.perf_counter() - t0 < 0.1
    assert v == 0.0 or v < 1e-12
    # early exit must not distort a normal case
    assert math.isclose(score.poisson_tail(5.0, 3),
                        1 - math.exp(-5) * (1 + 5 + 12.5), rel_tol=1e-9)


def test_matched_needed_inverts_surprise():
    for e in (0.01, 1.0, 42.0):
        k = score.matched_needed(e, 1.0)
        assert score.surprise(k, e) >= 1.0
        assert score.surprise(k - 1, e) < 1.0


def test_rank_annotates_flukes_and_promotable():
    shared = {"min": "0", "max": "z", "prefixes": ["aa"], "prefix_count": 1}
    rows = [
        score.score_pair("NPI", {**_entry(1000), **shared}, {**_entry(1000), **shared}, 900),
        score.score_pair("NPI", {**_entry(1000), **shared}, {**_entry(1000), **shared}, 0),
    ]
    ranked = score.rank_with_fluke_counts(rows)
    assert ranked[0]["s"] > ranked[-1]["s"]
    assert all("expected_flukes_at_rank" in r for r in ranked)
    assert ranked[0]["promotable"] is True       # huge S, ~0 expected flukes
    assert ranked[-1]["promotable"] is False


# ── absence verification (bucket histograms) ────────────────────────────────

def test_interleaved_subranges_detected_as_partitioned():
    # CCN shape: same state prefixes, disjoint facility-type buckets
    a = {1: 500, 2: 300, 3: 200}          # hospitals: low buckets
    b = {30: 400, 31: 350, 32: 100}       # home health: high buckets
    v = score.verify_absence(a, b)
    assert v["verdict"] == "partitioned" and v["shared_buckets"] == 0


def test_shared_buckets_confirm_credible_absence():
    a = {1: 10, 2: 10, 3: 10}
    b = {2: 5, 3: 5, 4: 5}
    assert score.verify_absence(a, b)["verdict"] == "credible"


def test_sparse_histogram_is_unverifiable_never_confirmed():
    a = {1: 10}                            # non-numeric key nulled out
    b = {30: 400, 31: 350, 32: 100}
    assert score.verify_absence(a, b)["verdict"] == "unverifiable"


# ── purity lock ─────────────────────────────────────────────────────────────

def test_score_module_stays_pure():
    src = (REPO / "hunch" / "score.py").read_text()
    for banned in ("sqlrun", "snowflake", "SELECT ", "open(", "write_text",
                   "load_dotenv", "import streamlit"):
        assert banned not in src, f"purity lock: {banned!r} found in hunch/score.py"
