"""Offline locks for the sieve row builder — no network, no Snowflake.
What they hold:

  * one row per (gated pair, key), canonical a<b, tier from the lattice
  * probabilistic keys are never chance-scored (stage stays metadata)
  * verified connect/ edges feed matched ONLY on the same key
  * measured pairs get band + family-fluke annotation; promotable follows
    the rule (S > band AND expected flukes < 1)
  * traps ride both sides; hunch/sieve.py stays pure
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from hunch import census, sieve  # noqa: E402

FIX = REPO / "tests" / "fixtures"
FP = json.loads((FIX / "hunch_fp_sample.json").read_text())
GRAPH = json.loads((FIX / "hunch_graph_sample.json").read_text())


def _setup():
    membership = census.build_key_membership(FP)
    edge_map = {}
    for e in GRAPH["edges"]:
        edge_map.setdefault(census._canon(e["a"], e["b"]), []).append(e)
    return membership, edge_map


def test_rows_canonical_and_tiered():
    membership, edge_map = _setup()
    rows = sieve.build_rows(membership, FP, edge_map)
    assert rows
    for r in rows:
        assert r["pair_a"] < r["pair_b"]
        assert r["tier"] == membership[r["key"]]["tier"]


def test_probabilistic_keys_never_chance_scored():
    membership, edge_map = _setup()
    rows = sieve.build_rows(membership, FP, edge_map)
    for r in rows:
        if r["key"] in ("NAME", "ADDRESS"):
            assert r["s_chance"] is None and r["stage"] == "metadata"
            assert "probabilistic" in r["range_reason"]


def test_verified_edge_feeds_matched_same_key_only():
    membership, edge_map = _setup()
    rows = sieve.build_rows(membership, FP, edge_map)
    row = next(r for r in rows if (r["pair_a"], r["pair_b"], r["key"])
               == ("TAB_NPI_A", "TAB_NPI_B", "NPI"))
    assert row["matched"] == 400                  # from the fixture edge
    assert row["verified_tier"] == "STEEL"
    assert row["stage"] == "measured"
    # ZIP pairing between the same tables must NOT inherit the NPI matched
    zips = [r for r in rows if r["key"] == "ZIP"
            and {r["pair_a"], r["pair_b"]} == {"TAB_NPI_A", "TAB_NPI_B"}]
    for r in zips:
        assert r["matched"] is None


def test_measured_dict_scores_and_annotates_flukes():
    membership, edge_map = _setup()
    measured = {("FED_CMS_NPPES", "TAB_NPI_A", "NPI"): 850}
    rows = sieve.build_rows(membership, FP, edge_map, measured)
    row = next(r for r in rows if (r["pair_a"], r["pair_b"], r["key"])
               == ("FED_CMS_NPPES", "TAB_NPI_A", "NPI"))
    assert row["stage"] == "measured"
    assert row["band"] == "excess" and row["s_chance"] > 2
    assert row["expected_flukes"] is not None
    assert row["promotable"] is True
    assert "trap_nppes_ein_masked" in row["traps"]


def test_floor_from_discover_scores_hard_pairs_as_zero():
    membership, edge_map = _setup()
    rows = sieve.build_rows(membership, FP, edge_map, floor_hard_unmeasured=True)
    # a hard-ID pair with no fixture edge gets matched=0 + the inference note
    row = next(r for r in rows if (r["pair_a"], r["pair_b"], r["key"])
               == ("FED_CMS_NPPES", "TAB_NPI_A", "NPI"))
    assert row["matched"] == 0 and row["stage"] == "measured"
    assert "discover found < MIN_MATCH" in row["range_reason"]
    # the verified edge keeps its real matched, not the floor
    edge_row = next(r for r in rows if (r["pair_a"], r["pair_b"], r["key"])
                    == ("TAB_NPI_A", "TAB_NPI_B", "NPI"))
    assert edge_row["matched"] == 400
    # probabilistic keys never floored
    for r in rows:
        if r["key"] in ("NAME", "ADDRESS"):
            assert r["matched"] is None


def test_sieve_module_stays_pure():
    src = (REPO / "hunch" / "sieve.py").read_text()
    for banned in ("sqlrun", "snowflake", "SELECT ", "open(", "write_text",
                   "load_dotenv", "import streamlit"):
        assert banned not in src, f"purity lock: {banned!r} found in hunch/sieve.py"
