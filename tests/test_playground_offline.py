"""Offline locks for the Playground — no network, no Snowflake.

  * every pack references only tables that exist in the committed inventory
    snapshot (or are explicitly declared PENDING with a shipping loader)
  * every trap key resolves; joins stay in-pack; tier vocab is fixed
  * observations are English pointers, never SQL drafts
  * no SQL strings outside playground/queries.py
  * session-state keys are pg_-prefixed (no collisions with other apps)
  * dictionary.py stays pure (no streamlit / snowflake imports)
  * queries.py refuses hostile FQNs (guard-validated, injection-impossible)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from playground import dictionary, packs  # noqa: E402
from playground import queries as pg_queries  # noqa: E402
from honesty.traps import TRAPS  # noqa: E402

INVENTORY = set(json.loads(
    (REPO / "tests" / "fixtures" / "playground_inventory.json")
    .read_text(encoding="utf-8"))["fqns"])

TIER_VOCAB = {"STEEL", "STRONG", "PROBABILISTIC", "GEO"}


# ── pack schema locks ───────────────────────────────────────────────────────

def test_pack_ids_unique_and_slug_safe():
    ids = packs.pack_ids()
    assert len(ids) == len(set(ids))
    for i in ids:
        assert re.fullmatch(r"[a-z0-9_]+", i), i


def test_every_pack_fqn_exists_or_is_declared_pending():
    for p in packs.PACKS:
        for t in p["tables"]:
            assert t["fqn"] in INVENTORY or t["fqn"] in packs.PENDING_FQNS, (
                f"pack {p['id']}: {t['fqn']} is neither in the committed "
                "inventory snapshot nor declared in PENDING_FQNS")


def test_every_trap_key_resolves():
    for p in packs.PACKS:
        for t in p["tables"]:
            for k in t.get("traps", []):
                assert k in TRAPS or k in packs.PACK_TRAPS, (
                    f"pack {p['id']}: unknown trap key {k}")
                assert not dictionary.trap_text(k).startswith("[unknown")


def test_joins_are_in_pack_and_tier_vocab_fixed():
    for p in packs.PACKS:
        in_pack = {t["fqn"] for t in p["tables"]}
        for t in p["tables"]:
            for j in t.get("joins", []):
                assert j["to"] in in_pack, (
                    f"pack {p['id']}: join target {j['to']} not in the pack")
                assert j["tier"] in TIER_VOCAB, j["tier"]


def test_observations_are_english_not_sql():
    # 'join' alone is ordinary English in this domain — only actual query
    # shapes count as drafting SQL.
    sql_shapes = re.compile(r"\b(SELECT|GROUP BY|INNER JOIN|LEFT JOIN)\b")
    for p in packs.PACKS:
        for ob in p.get("observations", []):
            assert not sql_shapes.search(ob.upper()), (
                f"pack {p['id']}: observation drafts SQL — packs describe, "
                f"never draft: {ob!r}")


def test_no_rotting_numbers_in_pack_prose():
    """v_state_numbers_only, structurally: no 4+-digit number (except years)
    in any pack prose — counts come live from the warehouse at render."""
    year = re.compile(r"^(19|20)\d{2}$")
    num = re.compile(r"\d{4,}")
    for p in packs.PACKS:
        prose = [p["question"], p["why"], *p.get("observations", [])] + [
            t["role"] for t in p["tables"]]
        for text in prose:
            for m in num.findall(text.replace(",", "")):
                assert year.match(m) or m == "13107" or m == "200000", (
                    f"pack {p['id']}: number {m!r} baked into prose — "
                    f"pull counts live instead: {text!r}")


# ── code hygiene locks ──────────────────────────────────────────────────────

def test_no_sql_outside_queries_module():
    for py in sorted((REPO / "playground").glob("*.py")):
        if py.name == "queries.py":
            continue
        text = py.read_text(encoding="utf-8")
        for token in ("SELECT ", "INSERT ", "UPDATE ", "DELETE ", "MERGE "):
            assert token not in text, (
                f"SQL ({token.strip()}) leaked into playground/{py.name}")


def test_session_keys_are_pg_prefixed():
    pat = re.compile(r"session_state\[[\"']([^\"']+)[\"']\]|key=[\"']([^\"']+)[\"']")
    for py in sorted((REPO / "playground").glob("*.py")):
        text = py.read_text(encoding="utf-8")
        for m in pat.finditer(text):
            key = m.group(1) or m.group(2)
            if key.startswith("decision_") or key.startswith("cohort_"):
                continue
            assert key.startswith("pg_"), (
                f"playground/{py.name}: session key {key!r} must be "
                "pg_-prefixed")


def test_dictionary_module_is_pure():
    text = (REPO / "playground" / "dictionary.py").read_text(encoding="utf-8")
    for banned in ("import streamlit", "import snowflake", "sqlrun"):
        assert banned not in text, (
            f"dictionary.py must stay pure — found {banned!r}")


def test_queries_refuse_hostile_fqns():
    with pytest.raises(Exception):
        pg_queries.column_catalog_sql(["x'; DROP TABLE LEADS; --"])
    with pytest.raises(Exception):
        pg_queries.live_count_sql("evil; DELETE FROM t")
    sql = pg_queries.column_catalog_sql(
        ["LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_SPINE"])
    assert "POLITICS__MEMBER_SPINE" in sql and "DROP" not in sql


def test_restricted_table_detection():
    assert dictionary.mentions_restricted(
        "select * from library_raw.landing.fed_senate_stock_watcher")
    assert not dictionary.mentions_restricted("select 1")
    assert not dictionary.mentions_restricted(None)


def test_pending_fqns_have_a_shipping_loader():
    """PENDING is a bridge, not a loophole: every pending table must be
    named in the trades loader that ships with it."""
    loader = (REPO / "politics" / "loaders" / "build_senate_trades.py") \
        .read_text(encoding="utf-8")
    for fqn in packs.PENDING_FQNS:
        assert fqn.rsplit(".", 1)[-1] in loader, (
            f"{fqn} is PENDING but no shipping loader mentions it")
