"""Offline tests for making BIOGUIDE + ICPSR first-class spine keys (Step-K politics).

Making a key first-class takes FIVE coordinated edits. These tests pin the ones that
silently no-op if half-done: the entity-type map must AGREE across all three sites
(spine._ENTITY_TYPE_SQL, incremental._entity_type_sql, entity_index_specs.
ENTITY_TYPE_BY_KEY), the DISPLAY_SPECS entries must be shaped so members become
'person' entities, validate_key_config must pass with the new keys present, and the
KEYSET_LIVE refactor must be called from BOTH reslice paths.
"""
from __future__ import annotations  # D38: `str | None` (PEP 604) needs this under Python 3.9 or pytest aborts collection for the whole suite

import inspect
import re

import pytest

from connect import discover, incremental, spine
from connect.entity_index_specs import DISPLAY_SPECS, ENTITY_TYPE_BY_KEY

NEW_KEYS = ("BIOGUIDE", "ICPSR")


# ---- validate_key_config passes with the new keys wired -------------------- #
def test_validate_key_config_passes_with_politician_keys():
    # BIOGUIDE + ICPSR are STEEL value keys; both need NORM_RULES + KEY_DOMAIN.
    discover.validate_key_config()
    for k in NEW_KEYS:
        assert k in discover.KEY_DOMAIN, f"{k} missing from KEY_DOMAIN (collision math)"


# ---- entity-type map agrees across all three sites ------------------------- #
def _sql_maps_key(sql: str, key: str) -> str | None:
    m = re.search(rf"WHEN '{key}' THEN '(\w+)'", sql)
    return m.group(1) if m else None


def test_entity_type_person_across_all_three_sites():
    inc_sql = incremental._entity_type_sql("key_type")
    spine_sql = spine._ENTITY_TYPE_SQL
    for k in NEW_KEYS:
        assert ENTITY_TYPE_BY_KEY[k] == "person", f"{k} not 'person' in ENTITY_TYPE_BY_KEY"
        assert _sql_maps_key(spine_sql, k) == "person", f"{k} not 'person' in spine SQL"
        assert _sql_maps_key(inc_sql, k) == "person", f"{k} not 'person' in incremental SQL"


def test_the_two_entity_type_sql_sites_are_consistent():
    # Every explicit WHEN mapping must match between the two hardcoded SQL sites.
    inc_sql = incremental._entity_type_sql("key_type")
    spine_sql = spine._ENTITY_TYPE_SQL
    keys = set(re.findall(r"WHEN '(\w+)' THEN", inc_sql)) | set(re.findall(r"WHEN '(\w+)' THEN", spine_sql))
    for k in keys:
        assert _sql_maps_key(inc_sql, k) == _sql_maps_key(spine_sql, k), f"drift on {k}"


# ---- DISPLAY_SPECS make members first-class entities ----------------------- #
def test_display_specs_carry_the_new_keys_with_names():
    # A spine table needs key/key_col + a person or org name + a bare-int authority.
    by_key = {}
    for tbl, spec in DISPLAY_SPECS.items():
        by_key.setdefault(spec["key"], []).append((tbl, spec))
    for k in NEW_KEYS:
        assert k in by_key, f"no DISPLAY_SPECS table keyed on {k}"
        for tbl, spec in by_key[k]:
            assert spec.get("key_col"), f"{tbl}: no key_col"
            assert spec.get("org") or spec.get("person"), f"{tbl}: no name column"
            assert isinstance(spec["authority"], int), f"{tbl}: authority must be a bare int"


def test_golden_source_for_bioguide_is_legislators():
    # FED_CONGRESS_LEGISLATORS is the authoritative BIOGUIDE source (lowest rank).
    spec = DISPLAY_SPECS["FED_CONGRESS_LEGISLATORS"]
    assert spec["key"] == "BIOGUIDE" and spec["person"] == ["NAME_LAST", "NAME_FIRST"]
    bioguide_specs = [s for s in DISPLAY_SPECS.values() if s["key"] == "BIOGUIDE"]
    assert spec["authority"] == min(s["authority"] for s in bioguide_specs)


def test_itcont_is_not_in_display_specs():
    # The 84M-row donations table must NOT be a spine table (scan cost).
    assert "FED_FEC_ITCONT" not in DISPLAY_SPECS
    for tbl in DISPLAY_SPECS:
        assert "ITCONT" not in tbl


# ---- the KEYSET_LIVE refactor is shared by both reslice paths -------------- #
def test_reslice_helper_called_from_both_paths():
    disc_src = inspect.getsource(incremental.reslice_discover)
    spine_src = inspect.getsource(incremental.reslice_spine)
    assert "_refresh_discover_keyset" in disc_src, "reslice_discover must use the shared helper"
    assert "_refresh_discover_keyset" in spine_src, \
        "reslice_spine must refresh the discover KEYSET_LIVE partition via the shared helper"


def test_reslice_spine_never_derives_keyset_from_spine_slice():
    # The helper must derive from the fingerprint (full key surface), never from the
    # single-key _NEW spine slice — that would wipe the other KEYSET_LIVE partitions.
    helper_src = inspect.getsource(incremental._refresh_discover_keyset)
    assert "_discover_keyset_inserts" in helper_src
    # it must DELETE its own KEYSET_LIVE partition then INSERT the full derived key set
    assert "DELETE FROM {KEYSET_FQN} WHERE TABLE_NAME" in helper_src
    assert "SELECT DISTINCT '{lit}', '{key}', {expr}" in helper_src
    # the spine slice (_NEW) must NEVER be the source of the discover partition
    assert "_NEW" not in helper_src
