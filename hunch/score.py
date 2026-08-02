"""Surprise scoring — Hunch Engine step 4 (the sieve's math). Pure functions.

Implements the null models from reports/hunch_null_models_2026-08-01.md with
the calibration fix from reports/hunch_calibration_2026-08-01.md:

  * ONE score: S = log10((observed+1) / (expected-under-null+1)), signed.
    Excess overlap is positive, credible absence is negative, chance is ~0.
  * expected-under-null for a hard-key pairing = a_distinct * b_distinct /
    KEY_DOMAIN[key] — imported from connect.discover, never re-derived.
  * ABSENCE IS ONLY SURPRISING WHEN THE VALUE SPACES ACTUALLY MEET. fmt-2
    fingerprints carry each key column's normalized min/max and 2-char prefix
    set; if the two sides' ranges/prefixes are disjoint (CCN facility-type
    ranges, per-court dockets), a zero overlap is boring-by-construction and
    S is clamped to 0 with the reason recorded. Truncated prefix sets
    (prefix_count > cap) fall back to the min/max range test alone and are
    marked unconditioned — never silently trusted.
  * Family-wide fluke control: the census fixed the family of comparisons, so
    every threshold carries its expected count of chance survivors (Poisson
    tail on each pair's expected overlap, summed). A feed rank is shown WITH
    the number of rows luck alone would put above it.

Purity contract: same as hunch/census.py — no SQL execution, no warehouse
client, no file writes; locked by tests/test_hunch_score_offline.py.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from connect.discover import KEY_DOMAIN  # noqa: E402
from connect.fingerprint import PREFIX_CAP  # noqa: E402

# S below this magnitude is "chance" for banding purposes (calibration showed
# verified-real >= +2.7 and chance within +/-0.35 on the hard-ID frontier).
CHANCE_BAND = 0.5


def surprise(observed: float, expected: float) -> float:
    """Signed log10 distance from the null. ~0 = boring."""
    return math.log10((observed + 1.0) / (expected + 1.0))


def expected_chance(a_distinct: int, b_distinct: int, key: str) -> float:
    """Chance overlap under independence over the key's honest value space.
    Raises on an un-domained key — a silent default would re-open the exact
    hole validate_key_config() exists to close."""
    return (a_distinct * b_distinct) / KEY_DOMAIN[key]


def range_overlap(a_entry: dict, b_entry: dict) -> dict:
    """Do two fmt-2 key columns' value spaces actually meet?

    Returns {meets, conditioned, reason}. conditioned=False means the inputs
    couldn't support the test (pre-fmt-2 entry, or prefix set truncated at
    PREFIX_CAP on either side AND ranges inconclusive) — callers must treat
    absence as unscorable, not boring and not surprising.
    """
    amn, amx = a_entry.get("min"), a_entry.get("max")
    bmn, bmx = b_entry.get("min"), b_entry.get("max")
    if None in (amn, amx, bmn, bmx):
        return {"meets": None, "conditioned": False, "reason": "no range data (pre-fmt-2)"}
    if amx < bmn or bmx < amn:
        return {"meets": False, "conditioned": True,
                "reason": f"ranges disjoint: [{amn}..{amx}] vs [{bmn}..{bmx}]"}
    apx, bpx = set(a_entry.get("prefixes") or []), set(b_entry.get("prefixes") or [])
    a_trunc = (a_entry.get("prefix_count") or 0) > PREFIX_CAP or len(apx) >= PREFIX_CAP
    b_trunc = (b_entry.get("prefix_count") or 0) > PREFIX_CAP or len(bpx) >= PREFIX_CAP
    if a_trunc or b_trunc:
        # dense space, prefix set incomplete: ranges overlap is all we know
        return {"meets": True, "conditioned": True,
                "reason": "ranges overlap (prefix set truncated — dense space)"}
    if not apx or not bpx:
        return {"meets": None, "conditioned": False, "reason": "no prefix data"}
    shared = apx & bpx
    if not shared:
        return {"meets": False, "conditioned": True,
                "reason": "prefix sets disjoint (partitioned ID space)"}
    return {"meets": True, "conditioned": True,
            "reason": f"{len(shared)} shared prefixes"}


def score_pair(key: str, a_entry: dict, b_entry: dict,
               matched: int | None) -> dict:
    """Score one measured pairing. matched=None means not yet measured
    (metadata stage) — expected + range verdict only, S stays None.
    """
    a_d, b_d = a_entry.get("distinct") or 0, b_entry.get("distinct") or 0
    exp = expected_chance(a_d, b_d, key)
    ro = range_overlap(a_entry, b_entry)
    out = {"key": key, "a_distinct": a_d, "b_distinct": b_d,
           "expected_chance": exp, "range": ro,
           "matched": matched, "s": None, "band": "unmeasured",
           "coverage": None, "absence_valid": ro["meets"] is True}
    if matched is None:
        return out
    s = surprise(matched, exp)
    cov = matched / max(min(a_d, b_d), 1)
    if s < -CHANCE_BAND and ro["meets"] is False:
        # boring-by-construction: partitioned spaces can never overlap
        out.update({"s": 0.0, "band": "partitioned", "coverage": cov})
        return out
    if s < -CHANCE_BAND and ro["meets"] is not True:
        out.update({"s": None, "band": "absence-unscorable", "coverage": cov})
        return out
    band = ("excess" if s > CHANCE_BAND
            else "absence" if s < -CHANCE_BAND
            else "chance")
    out.update({"s": round(s, 3), "band": band, "coverage": round(cov, 4)})
    return out


# ── family-wide fluke control ───────────────────────────────────────────────

def poisson_tail(lam: float, k: int) -> float:
    """P(X >= k) for X ~ Poisson(lam). Iterative sum with early exit — once
    i passes lam the terms shrink geometrically, so we stop when the remaining
    mass is negligible instead of walking all k terms (k can be millions for
    a high-S pair; walking them froze a whole sieve run on 2026-08-01)."""
    if k <= 0:
        return 1.0
    if lam <= 0:
        return 0.0
    # P(X >= k) = 1 - sum_{i<k} e^-lam lam^i / i!
    log_term = -lam                      # log of i=0 term
    acc = math.exp(log_term)
    for i in range(1, k):
        log_term += math.log(lam) - math.log(i)
        term = math.exp(log_term)
        acc += term
        if acc >= 1.0:
            return 0.0
        if i > lam and term < 1e-17:     # tail beyond here can't reach 1e-15
            return max(0.0, 1.0 - acc)
    return max(0.0, 1.0 - acc)


def matched_needed(expected: float, s_threshold: float) -> int:
    """Smallest matched count whose surprise clears the threshold."""
    return max(0, math.ceil((expected + 1.0) * (10.0 ** s_threshold) - 1.0))


def expected_flukes(expecteds: list[float], s_threshold: float) -> float:
    """Across the family of pairings, how many would clear s_threshold by
    chance alone (each pair's overlap ~ Poisson(expected))."""
    return sum(poisson_tail(e, matched_needed(e, s_threshold)) for e in expecteds)


def verify_absence(a_hist: dict, b_hist: dict, min_side_buckets: int = 3) -> dict:
    """Second absence check: do the two sides OCCUPY the same sub-ranges?

    Leading-prefix analysis misses middle-digit partitions (CCN = 2-digit
    state + 4-digit facility ID whose RANGES encode facility type — the two
    sides share every state prefix yet can never share a value). Inputs are
    bucket histograms of TRY_TO_NUMBER(normalized value) over the pair's
    common bounds ({bucket_index: count}), collected by ONE cheap grouped
    query per side, only for pairs already in the absence band.

    Returns {verdict: 'partitioned'|'credible'|'unverifiable', shared_buckets,
    reason}. Sparse histograms (fewer than min_side_buckets on either side,
    e.g. non-numeric IDs where TRY_TO_NUMBER nulled out) are unverifiable —
    the absence stays flagged, never silently confirmed.
    """
    a_b, b_b = {k for k, v in a_hist.items() if v}, {k for k, v in b_hist.items() if v}
    if len(a_b) < min_side_buckets or len(b_b) < min_side_buckets:
        return {"verdict": "unverifiable", "shared_buckets": len(a_b & b_b),
                "reason": "histogram too sparse (non-numeric or tiny side)"}
    shared = a_b & b_b
    if not shared:
        return {"verdict": "partitioned", "shared_buckets": 0,
                "reason": f"interleaved sub-ranges: {len(a_b)} vs {len(b_b)} "
                          "occupied buckets, zero shared"}
    return {"verdict": "credible", "shared_buckets": len(shared),
            "reason": f"{len(shared)} shared occupied buckets"}


def rank_with_fluke_counts(scored: list[dict]) -> list[dict]:
    """Sort measured pairs by S desc; annotate each row with the expected
    number of chance survivors at (>= its S). The promotion rule from the
    design note: promotable only when expected_flukes_at_rank < 1."""
    expecteds = [r["expected_chance"] for r in scored if r["matched"] is not None]
    ranked = sorted((r for r in scored if r["s"] is not None),
                    key=lambda r: r["s"], reverse=True)
    for r in ranked:
        ef = expected_flukes(expecteds, r["s"])
        r["expected_flukes_at_rank"] = round(ef, 3)
        r["promotable"] = bool(r["s"] > CHANCE_BAND and ef < 1.0)
    return ranked
