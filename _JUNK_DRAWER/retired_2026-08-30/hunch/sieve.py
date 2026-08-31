"""Sieve row builder — turns the lattice + scores into HYPOTHESIS_CATALOG
rows. Pure functions: no SQL text, no warehouse client, no file writes
(scaffold SQL is added by scripts/hunch_sieve.py, the only SQL holder).

Stage discipline (the cost sieve from the handoff):
  metadata — free: every direct pair gets a row with expected/range verdict;
             matched stays NULL unless connect/ already verified the pair on
             this exact key.
  measured — costed: pairs whose matched count was measured live get scored,
             banded, ranked, and family-fluke-annotated.
Keys without a KEY_DOMAIN entry (NAME/ADDRESS — the probabilistic tier) are
never chance-scored; their rows stay stage=metadata until a dedicated
probabilistic model exists. GEO keys have domains and can be measured later.
"""
from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from connect.discover import KEY_DOMAIN  # noqa: E402
from honesty.traps import traps_for_source  # noqa: E402

from hunch import score as hscore  # noqa: E402
from hunch.census import _canon, _gated_members  # noqa: E402


def best_col_entry(membership: dict, key: str, table: str, fingerprints: dict) -> dict:
    """The fmt-2 fingerprint entry for a table's best (most populated) column
    of a key — the scorer needs distinct/min/max/prefixes, which live in the
    fingerprint entry, not the membership summary."""
    cols = membership[key]["members"][table]["cols"]
    best = max(cols, key=lambda c: (c["populated_pct"] or 0))["col"]
    return next(e for e in fingerprints[table]["keys"]
                if e["column"] == best and e["key"] == key)


def edge_matched(edge_map: dict, a: str, b: str, key: str) -> int | None:
    """matched from a verified connect/ edge — only if the edge is on the SAME
    key (an edge on another key says nothing about this pairing's overlap)."""
    for e in edge_map.get(_canon(a, b), []):
        if e.get("key") == key:
            return e.get("matched")
    return None


HARD_TIERS = ("STEEL", "STRONG")


def build_rows(membership: dict, fingerprints: dict, edge_map: dict,
               measured: dict | None = None, run_id: str = "",
               floor_hard_unmeasured: bool = False) -> list[dict]:
    """One row per (pair, key) over the gated direct lattice.

    measured: {(a, b, key): matched} from the live measurement stage.
    floor_hard_unmeasured: set ONLY when edge_map comes from a discover run
    that POST-DATES the fingerprints — discover tests every co-occurring
    value pair, so a hard-ID pair with no edge overlapped below the fluke
    floor (< MIN_MATCH distinct values). Those pairs are scored as matched=0
    with the inference recorded, instead of paying a live query each.
    Rows are canonical (a < b); scored rows get band/S/coverage; the ranked
    fluke annotation is applied across ALL scored rows at the end.
    """
    measured = measured or {}
    rows = []
    for key, slot in sorted(membership.items()):
        gated = sorted(_gated_members(slot))
        domained = key in KEY_DOMAIN
        for i, a in enumerate(gated):
            for b in gated[i + 1:]:
                m = measured.get((a, b, key))
                floored = False
                if m is None:
                    m = edge_matched(edge_map, a, b, key)
                if (m is None and floor_hard_unmeasured
                        and slot["tier"] in HARD_TIERS and domained):
                    m, floored = 0, True
                a_e = best_col_entry(membership, key, a, fingerprints)
                b_e = best_col_entry(membership, key, b, fingerprints)
                if domained:
                    sc = hscore.score_pair(key, a_e, b_e, m)
                    if floored:
                        sc["range"] = dict(sc["range"])
                        sc["range"]["reason"] = ("discover found < MIN_MATCH overlap | "
                                                 + sc["range"]["reason"])
                else:
                    sc = {"expected_chance": None, "matched": m, "s": None,
                          "band": "unmeasured", "coverage": None,
                          "range": {"reason": "no value-space model (probabilistic key)"},
                          "absence_valid": False}
                ver = [e["tier"] for e in edge_map.get(_canon(a, b), [])
                       if e.get("key") == key]
                fam_a, fam_b = "_".join(a.split("_")[:2]), "_".join(b.split("_")[:2])
                rows.append({
                    "pair_a": a, "pair_b": b, "key": key, "tier": slot["tier"],
                    "a_col": a_e["column"], "b_col": b_e["column"],
                    "a_distinct": a_e.get("distinct"), "b_distinct": b_e.get("distinct"),
                    "matched": sc["matched"],
                    "expected_chance": sc["expected_chance"],
                    "s_chance": sc["s"], "band": sc["band"],
                    "coverage": sc["coverage"],
                    "range_reason": sc["range"]["reason"],
                    "absence_valid": sc["absence_valid"],
                    "expected_flukes": None, "promotable": None,
                    "same_family": fam_a == fam_b,
                    "traps": list(traps_for_source(a) + traps_for_source(b)),
                    "verified_tier": ver[0] if ver else None,
                    "stage": "measured" if sc["s"] is not None else "metadata",
                    "run_id": run_id,
                })
    _annotate_flukes(rows)
    return rows


def _annotate_flukes(rows: list[dict]) -> None:
    scored = [r for r in rows if r["s_chance"] is not None]
    expecteds = [r["expected_chance"] for r in scored]
    for r in scored:
        ef = hscore.expected_flukes(expecteds, r["s_chance"])
        r["expected_flukes"] = round(ef, 3)
        r["promotable"] = bool(r["s_chance"] > hscore.CHANCE_BAND and ef < 1.0)
