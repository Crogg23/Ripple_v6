"""Offline match-quality regression — score the frozen gold fixture and assert the
scorer separates same-person pairs from different-person pairs.

The fixture is produced by `python -m connect eval` (labels from hard-ID ground
truth). This is CI-able: pure Python, no Snowflake.
"""

import csv
from pathlib import Path

import pytest

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "gold_pairs_sample.csv"


def _rows():
    if not FIXTURE.exists():
        pytest.skip("no gold fixture; run `python -m connect eval` to generate it")
    return list(csv.DictReader(FIXTURE.open(encoding="utf-8")))


def _score(jw, r):
    return 0.70 * jw(r["l_last"], r["r_last"]) + 0.30 * jw(r["l_first"], r["r_first"])


def test_scorer_separates_positives_from_negatives():
    rows = _rows()
    rf = pytest.importorskip("rapidfuzz")
    from rapidfuzz.distance import JaroWinkler

    def jw(a, b):
        return JaroWinkler.similarity(a or "", b or "")

    pos = [_score(jw, r) for r in rows if r["label"] == "1"]
    neg = [_score(jw, r) for r in rows if r["label"] == "0"]
    assert pos and neg, "fixture must contain both labels"
    # Same-person pairs must score higher on average. The margin is small by design:
    # the fixture's negatives are the HARDEST cases (same name + same ZIP, different
    # person) — that small gap is exactly why fuzzy auto-merge stays gated.
    assert (sum(pos) / len(pos)) > (sum(neg) / len(neg)) + 0.01


def test_high_threshold_has_meaningful_precision():
    rows = _rows()
    pytest.importorskip("rapidfuzz")
    from rapidfuzz.distance import JaroWinkler

    def jw(a, b):
        return JaroWinkler.similarity(a or "", b or "")

    sel = [r for r in rows if _score(jw, r) >= 0.95]
    if not sel:
        pytest.skip("no pairs over threshold in this fixture")
    prec = sum(1 for r in sel if r["label"] == "1") / len(sel)
    # name+ZIP fuzzy is a lead generator, not auto-merge — a loose floor guards regressions
    assert prec >= 0.40
