"""EIN-normalization parity lock (audit F6 + the serve_queries drift lesson
of 2026-07-31: never re-implement key normalization freehand).

cohort_queue.sql needs connect/keys.py's EIN normalization in pure dbt SQL,
so it carries a CHARACTER-FOR-CHARACTER copy. This test regenerates the
expression from connect.keys (the single source of truth) and fails the
moment the copy drifts — same convention as the serve_queries parity test.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from connect import keys  # noqa: E402

MART = (REPO / "library-onboarding" / "ripple_dbt" / "models" / "marts" /
        "review" / "cohort_queue.sql").read_text(encoding="utf-8")


def test_raw_side_ein_normalization_is_verbatim_keys_py():
    assert keys.normalize_sql("EIN", "ein") in MART, (
        "cohort_queue.sql's raw-side EIN normalization has drifted from "
        "connect/keys.py normalize_sql('EIN', 'ein') — regenerate the copy, "
        "never hand-edit it")


def test_lead_side_ein_normalization_is_verbatim_keys_py():
    assert keys.normalize_sql("EIN", "m.ein_raw") in MART, (
        "cohort_queue.sql's lead-side EIN normalization has drifted from "
        "connect/keys.py normalize_sql('EIN', 'm.ein_raw') — regenerate the "
        "copy, never hand-edit it")


def test_both_sides_use_the_same_rule():
    """Belt-and-braces: the two copies must be the same expression modulo
    the column reference."""
    raw = keys.normalize_sql("EIN", "COL")
    lead = keys.normalize_sql("EIN", "COL")
    assert raw == lead
