"""Resolver tests — banding, config, and the gating invariant."""

import inspect

from connect import resolve


def test_band_thresholds():
    assert resolve._band(0.99) == "AUTO"
    assert resolve._band(0.92) == "AUTO"
    assert resolve._band(0.85) == "REVIEW"
    assert resolve._band(0.50) == "WEAK"


def test_pairs_are_wellformed():
    for spec in resolve.PAIRS.values():
        for side in ("left", "right"):
            for field in ("table", "last", "first", "zip", "id"):
                assert field in spec[side]


def test_resolver_is_gated_off_spine():
    """resolve writes ENTITY_LINKS only; it must never mutate the hard-ID spine."""
    src = inspect.getsource(resolve)
    assert "ENTITY_MAP" not in src
    assert "ENTITY_GOLDEN" not in src
