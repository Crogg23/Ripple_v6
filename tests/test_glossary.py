"""Locks on the shared plain-English glossary.

  * coverage: every tier, verdict, decision word, governed key name, and
    pack-referenced FEC column has an entry
  * the Reading Room's tier/verdict dicts ARE glossary lookups (single
    source of truth — no drift possible)
  * ASCII only; passes the reading_room ai-free regex (belt and braces —
    glossary/ sits outside that test's globs, so this one runs it here)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "reading_room"))

import glossary  # noqa: E402
from glossary.column_gloss import COLUMN_GLOSS  # noqa: E402


def test_covers_every_tier_and_verdict():
    import queries as rr_queries  # reading_room
    for tier in rr_queries.TIERS:
        assert glossary.gloss(tier), f"tier {tier} has no gloss"
    for v in ("PAID_ON_OR_AFTER_EXCLUSION", "PAYMENTS_PREDATE_EXCLUSION",
              "TIMELINE_UNKNOWN", "NOT_EVALUATED"):
        assert glossary.gloss(v), f"verdict {v} has no gloss"
    for d in ("confirmed", "rejected", "needs_work", "retracted", "stale",
              "published"):
        assert glossary.gloss(d), f"decision {d} has no gloss"


def test_covers_key_names_and_fec_columns():
    for k in ("BIOGUIDE", "ICPSR", "FEC_CAND_ID", "FEC_CMTE_ID", "NPI",
              "EIN", "UEI", "CIK", "IMO", "STEEL", "STRONG",
              "PROBABILISTIC", "GEO"):
        assert glossary.gloss(k), f"key/tier {k} has no gloss"
    for c in ("TTL_RECEIPTS", "TRANS_FROM_AUTH", "TTL_INDIV_CONTRIB",
              "CAND_ID", "CMTE_ID", "DART", "FOLD"):
        assert glossary.gloss(c), f"column/term {c} has no gloss"


def test_reading_room_reads_from_the_glossary():
    import render as rr_render  # reading_room
    for k, v in rr_render.TIER_DEFS.items():
        assert v == glossary.GLOSSARY[k]
    for k, v in rr_render.VERDICT_TEXT.items():
        assert v == glossary.GLOSSARY[k]


def test_ascii_only_and_ai_free():
    ai_re = re.compile(
        r"anthropic|openai|claude|gpt|llm|api\.anthropic|completion",
        re.IGNORECASE)
    for py in sorted((REPO / "glossary").glob("*.py")):
        text = py.read_text(encoding="utf-8")
        assert text.isascii(), f"{py.name} contains non-ASCII"
        assert not ai_re.search(text), f"{py.name} fails the ai-free regex"


def test_heuristic_gloss_is_deterministic_and_honest():
    g = glossary.heuristic_gloss("TOTAL_PAYMENT_USD", None, "numeric")
    assert "looks like" in g
    assert glossary.heuristic_gloss("BIOGUIDE") == glossary.GLOSSARY["BIOGUIDE"]
    assert glossary.heuristic_gloss("SOME_COL") == glossary.heuristic_gloss("SOME_COL")


def test_column_gloss_keys_are_upper_and_ascii():
    for (fqn, col), text in COLUMN_GLOSS.items():
        assert col == col.upper(), f"column key {col!r} must be UPPER"
        assert text.isascii()
