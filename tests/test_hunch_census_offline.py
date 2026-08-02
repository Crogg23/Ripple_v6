"""Offline locks for the Hunch Engine lattice census — no network, no
Snowflake. What they hold:

  * tier truth is KEY_TOKENS and nothing else — a drifted fingerprint tier
    RAISES; emitted tiers stay inside the known vocabulary
  * D17: NAICS/SIC/NCES never become lattice members, but their foregone
    pairs are counted in blind spots
  * pair math is exact (C(n,2), column-pair products, canonical a<b dedup,
    strongest-tier rollup) and the gate boundary is >= MIN_POP_PCT
  * bridges are 2-hop only where no direct edge exists; rejected crosswalks
    are skipped
  * the verified 663-edge overlay must sit INSIDE the lattice (an edge the
    census can't see = census bug, reported loudly)
  * the sample is seeded and byte-reproducible; trap flags ride every row
  * hunch/census.py stays pure: no SQL, no snowflake, no file writes
  * the CLI degrades honestly offline: registry fields are null, never made up
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from hunch import census  # noqa: E402

FIX = REPO / "tests" / "fixtures"
FP = json.loads((FIX / "hunch_fp_sample.json").read_text())
GRAPH = json.loads((FIX / "hunch_graph_sample.json").read_text())


def _xref_rows():
    import csv
    with open(FIX / "hunch_xref_sample.csv", newline="") as fh:
        return list(csv.DictReader(fh))


# ── tier truth ──────────────────────────────────────────────────────────────

def test_tiers_come_from_key_tokens_and_drift_raises():
    m = census.build_key_membership(FP)
    from connect.keys import KEY_TOKENS
    for key, slot in m.items():
        assert slot["tier"] == KEY_TOKENS[key][0]
    bad = {"T1": {"rows": 1, "keys": [
        {"column": "NPI", "key": "NPI", "tier": "STRONG", "populated_pct": 100.0}]}}
    with pytest.raises(ValueError, match="tier drift"):
        census.build_key_membership(bad)
    unknown = {"T1": {"rows": 1, "keys": [
        {"column": "X", "key": "NOT_A_KEY", "tier": "STEEL", "populated_pct": 100.0}]}}
    with pytest.raises(ValueError, match="not in KEY_TOKENS"):
        census.build_key_membership(unknown)


def test_emitted_tiers_stay_in_vocabulary():
    c = census.build_census(FP, GRAPH, _xref_rows(), sample_n=10, seed=1)
    allowed = {"STEEL", "STRONG", "GEO", "PROBABILISTIC", "BRIDGE", "CORROBORATED"}
    for row in c["sample"]:
        assert row["tier"] in allowed
    assert set(c["rollup"]["distinct_pairs_strongest_tier"]) <= allowed


# ── D17 ─────────────────────────────────────────────────────────────────────

def test_vocab_keys_banned_from_lattice_but_counted():
    m = census.build_key_membership(FP)
    assert "NAICS" not in m and "SIC" not in m and "NCES" not in m
    vb = census.vocab_banned(FP)
    assert vb["NAICS"] == {"tables": 2, "foregone_table_pairs": 1}


# ── pair math ───────────────────────────────────────────────────────────────

def test_scope_mirrors_connect_edge_universe():
    m = census.build_key_membership(FP)
    npi = m["NPI"]["members"]
    assert "PORTAL_SOCRATA_X" not in npi          # prefix exclusion
    assert "FED_FEC_BULK" not in m.get("FEC_CMTE_ID", {"members": {}})["members"] \
        if "FEC_CMTE_ID" in m else True
    scoped = census.scoped_out_tables(FP)
    assert scoped["portal_crawl"] == ["PORTAL_SOCRATA_X"]
    assert scoped["abandoned_duplicates"] == ["FED_FEC_BULK"]


def test_summary_counts_exact():
    m = census.build_key_membership(FP)
    s = census.summarize(m)
    npi = s["per_key"]["NPI"]
    assert npi["gated"] == {"tables": 4, "table_pairs": 6, "column_pairs": 9}
    assert npi["ungated"] == {"tables": 5, "table_pairs": 10, "column_pairs": 14}
    assert s["per_key"]["FIPS"]["gated"]["table_pairs"] == 1
    assert s["per_key"]["ZIP"]["gated"]["table_pairs"] == 0


def test_gate_boundary_is_min_pop_pct():
    m = census.build_key_membership(FP)
    assert m["NPI"]["members"]["TAB_NPI_LOW"]["gated"] is False   # 0.5 < 1.0
    exactly = {"T1": {"rows": 1, "keys": [
        {"column": "NPI", "key": "NPI", "tier": "STEEL", "populated_pct": 1.0}]}}
    assert census.build_key_membership(exactly)["NPI"]["members"]["T1"]["gated"] is True


def test_strongest_tier_rollup_dedups():
    m = census.build_key_membership(FP)
    direct = census.direct_pair_tiers(m)
    # canonical ordering, no reversed dupes
    assert all(a < b for a, b in direct)
    # GEO_A/GEO_B share FIPS (GEO) and NAME (PROBABILISTIC) -> one pair, GEO wins
    assert direct[("TAB_GEO_A", "TAB_GEO_B")] == "GEO"
    assert len(direct) == 8          # 6 NPI pairs + 1 CCN pair + 1 GEO pair
    tiers = sorted(direct.values())
    assert tiers.count("STEEL") == 7 and tiers.count("GEO") == 1


# ── bridges ─────────────────────────────────────────────────────────────────

def test_bridge_math_mirrors_connect_bridge():
    m = census.build_key_membership(FP)
    direct = census.direct_pair_tiers(m)
    b = census.bridge_pairs(FP, m, direct, _xref_rows())
    # relations derived from fingerprints (dual-hard-ID tables), like bridge.py
    assert len(b["crosswalks"]) == 1
    cw = b["crosswalks"][0]
    assert cw["crosswalk"] == "TAB_XWALK"
    assert (cw["key_a"], cw["key_b"]) == ("CCN", "NPI")
    assert cw["pair_count"] == 3          # CCN_ONLY x {NPI_A, NPI_B, NPPES}
    assert cw["copop_pct"] == 99.0        # evidence merged from xref CSV
    assert len(b["pairs"]) == 3
    assert not (set(b["pairs"]) & set(direct))            # never shadows direct


def test_bridge_evidence_skips_rejected_xref_rows():
    m = census.build_key_membership(FP)
    direct = census.direct_pair_tiers(m)
    rejected_only = [r for r in _xref_rows() if (r.get("reject_reason") or "").strip()]
    b = census.bridge_pairs(FP, m, direct, rejected_only)
    assert b["crosswalks"][0]["copop_pct"] is None        # rejected row never annotates


# ── corroborated candidates ─────────────────────────────────────────────────

def test_corroborated_candidates_need_name_plus_shared_geo():
    m = census.build_key_membership(FP)
    direct = census.direct_pair_tiers(m)
    cand = census.corroborated_candidates(m, direct)
    assert cand == {("TAB_GEO_A", "TAB_GEO_B")}


# ── verified overlay ────────────────────────────────────────────────────────

def test_overlay_finds_edges_inside_lattice():
    c = census.build_census(FP, GRAPH, _xref_rows(), sample_n=5, seed=7)
    ov = c["verified_overlay"]
    assert ov["verified_edges"] == 1
    assert ov["verified_in_lattice"] == 1
    assert ov["verified_missing_from_lattice"] == []
    assert ov["prior_gated_out_total"] == 3
    assert ov["never_tested"] == 10                      # 11 lattice pairs - 1 verified
    assert c["rollup"]["total_distinct_pairs"] == 11


def test_overlay_reports_missing_edge_as_bug():
    ghost = {"meta": {"gated_out": 0},
             "edges": [{"a": "NOWHERE_1", "b": "NOWHERE_2", "key": "NPI",
                        "tier": "STEEL", "matched": 9, "confidence": 0.9}]}
    c = census.build_census(FP, ghost, [], sample_n=1, seed=1)
    assert c["verified_overlay"]["verified_missing_from_lattice"] == [("NOWHERE_1", "NOWHERE_2")]
    assert "CENSUS BUG" in census.render_report(c)


# ── sample ──────────────────────────────────────────────────────────────────

def test_sample_is_seeded_and_reproducible():
    a = census.build_census(FP, GRAPH, _xref_rows(), sample_n=5, seed=42)["sample"]
    b = census.build_census(FP, GRAPH, _xref_rows(), sample_n=5, seed=42)["sample"]
    c = census.build_census(FP, GRAPH, _xref_rows(), sample_n=5, seed=43)["sample"]
    assert json.dumps(a) == json.dumps(b)
    assert json.dumps(a) != json.dumps(c)
    assert len(a) == 5
    for row in a:
        assert row["a"] < row["b"]
        assert row["provenance"] == "measured-fingerprint" or row["provenance"].startswith("bridge:")


def test_sample_rows_carry_traps_and_priors():
    m = census.build_key_membership(FP)
    row = census.expand_pair("FED_CMS_NPPES", "TAB_NPI_A", "NPI", m, {})
    assert "trap_nppes_ein_masked" in row["a_traps"]
    assert row["key_domain"] == 10 ** 10
    assert row["spine_entity"] is not None
    assert row["verified"] is None
    assert row["time_comparable"] is None                # never fabricated offline


# ── blind spots ─────────────────────────────────────────────────────────────

def test_blind_spots_offline_are_null_not_fabricated():
    c = census.build_census(FP, GRAPH, _xref_rows(), sample_n=3, seed=1)
    bs = c["blind_spots"]
    assert bs["landing_universe"] is None
    assert bs["time_only_universe"] is None
    assert bs["zero_key_tables"] == ["TAB_ZERO_KEYS"]
    assert bs["vocab_only_tables"] == ["TAB_VOCAB", "TAB_VOCAB_2"]
    assert "FED_CMS_NPPES" in bs["trap_flagged_members"]
    assert bs["scoped_out"] == {"portal_crawl": 1, "abandoned_duplicates": 1}
    assert c["meta"]["registry_pass"] is False


# ── purity lock ─────────────────────────────────────────────────────────────

def test_census_module_stays_pure():
    src = (REPO / "hunch" / "census.py").read_text()
    for banned in ("sqlrun", "snowflake", "SELECT ", "open(", "write_text",
                   "load_dotenv", "import streamlit"):
        assert banned not in src, f"purity lock: {banned!r} found in hunch/census.py"


# ── script contract ─────────────────────────────────────────────────────────

def _load_script():
    spec = importlib.util.spec_from_file_location(
        "hunch_census_script", REPO / "scripts" / "hunch_census.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _run(mod, argv):
    old = sys.argv
    sys.argv = ["hunch_census.py"] + argv
    try:
        return mod.main()
    finally:
        sys.argv = old


def test_script_offline_writes_complete_json(tmp_path, capsys):
    mod = _load_script()
    out = tmp_path / "lattice.json"
    rep = tmp_path / "report.md"
    rc = _run(mod, ["--fingerprints", str(FIX / "hunch_fp_sample.json"),
                    "--graph", str(FIX / "hunch_graph_sample.json"),
                    "--xref", str(FIX / "hunch_xref_sample.csv"),
                    "--out", str(out), "--report", str(rep),
                    "--sample", "3", "--seed", "9"])
    assert rc == 0
    data = json.loads(out.read_text())
    for k in ("meta", "key_membership", "bridges", "summary", "rollup",
              "verified_overlay", "sample", "blind_spots"):
        assert k in data
    assert data["meta"]["registry_pass"] is False
    assert data["blind_spots"]["landing_universe"] is None
    assert "Lattice Census" in rep.read_text()
    assert "distinct comparable" in capsys.readouterr().out.lower()
