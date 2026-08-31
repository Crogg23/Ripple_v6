"""Offline locks for the Senate trades leg — parser units over a committed
fixture, plus the legal-restriction paper trail. No network, no Snowflake.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "politics" / "loaders"))
sys.path.insert(0, str(REPO / "library-onboarding"))

import build_senate_trades as bst  # noqa: E402

FIXTURE = json.loads(
    (REPO / "tests" / "fixtures" / "senate_trades_sample.json")
    .read_text(encoding="utf-8"))


def test_to_frame_maps_fields_and_orders_columns():
    df = bst.to_frame(FIXTURE)
    assert list(df.columns) == bst.COLS
    assert len(df) == 3
    row = df.iloc[0]
    assert row["SENATOR"] == "Ron L Wyden"
    assert row["TICKER"] == "BYND"
    assert row["TRANSACTION_DATE"] == "11/10/2020"


def test_amount_band_is_untouched():
    df = bst.to_frame(FIXTURE)
    assert df.iloc[0]["AMOUNT"] == "$50,001 - $100,000", (
        "the disclosure band must land verbatim — never parsed, never "
        "midpointed")


def test_missing_fields_become_null_not_crash():
    # the third record has no 'ticker' and no 'comment'
    df = bst.to_frame(FIXTURE)
    row = df.iloc[2]
    assert row["SENATOR"] == "Tommy Tuberville"
    assert row["TICKER"] is None or row["TICKER"] != row["TICKER"]  # None/NaN
    assert row["COMMENT"] is None or row["COMMENT"] != row["COMMENT"]


def test_mart_ddl_is_honest_about_the_name_match():
    assert "match_method" in bst.MART_DDL.lower()
    assert "'unmatched'" in bst.MART_DDL
    assert "MEMBER_CROSSWALK" in bst.MART_DDL
    # amount stays the band
    assert "amount_band" in bst.MART_DDL.lower()


def test_registry_spec_carries_the_legal_restriction():
    spec_text = (REPO / "politics" / "registry" / "political_sources.py") \
        .read_text(encoding="utf-8")
    assert "fed_senate_stock_watcher" in spec_text
    assert "13107" in spec_text, (
        "the registry row must cite 5 USC 13107(c)(1) — journalism use only")
    assert "JOURNALISM USE ONLY" in spec_text


def test_loader_declares_journalism_only():
    src = (REPO / "politics" / "loaders" / "build_senate_trades.py") \
        .read_text(encoding="utf-8")
    assert "13107" in src
