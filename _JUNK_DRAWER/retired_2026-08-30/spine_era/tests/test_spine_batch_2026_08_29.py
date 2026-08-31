"""The 2026-08-29 bucket-B batch (CAGE / award key / PECOS / FDIC cert / RSSD /
EIA plant + utility), end to end.

The batch is live in code (flag True); it reaches the warehouse through
`python -m connect apply-config` (bounded reslices), not a full rebuild. The
fixture re-applies the staged dicts on a COPY so the assertions hold whether
the flag is on or off.
"""
from __future__ import annotations

import pytest

from connect import discover, keys
from connect import entity_index_specs as specs

BATCH_KEYS = set(keys._BATCH_2026_08_29_NORM_RULES)


@pytest.fixture
def flag_on(monkeypatch):
    monkeypatch.setattr(keys, "ENABLE_SPINE_BATCH_2026_08_29", True)
    for key, rule in keys._BATCH_2026_08_29_NORM_RULES.items():
        monkeypatch.setitem(keys.NORM_RULES, key, rule)
    for tc, kt in keys._BATCH_2026_08_29_TABLE_COLUMN_KEYS.items():
        monkeypatch.setitem(keys.TABLE_COLUMN_KEYS, tc, kt)
    # Patch a COPY of DISPLAY_SPECS so the module-level dict stays dark.
    snapshot = {t: dict(s, extra_keys=list(s.get("extra_keys", [])))
                for t, s in specs.DISPLAY_SPECS.items()}
    monkeypatch.setattr(specs, "DISPLAY_SPECS", snapshot)
    specs._maybe_enable_spine_batch_2026_08_29()
    return snapshot


def test_batch_is_live():
    # Flipped 2026-08-29 once apply-config made config drift a bounded change.
    assert keys.ENABLE_SPINE_BATCH_2026_08_29 is True
    assert BATCH_KEYS <= set(keys.NORM_RULES)
    assert "FED_FDIC_BANK_DATA" in specs.DISPLAY_SPECS


def test_every_batch_key_is_joinable_and_tiered(flag_on):
    for key in BATCH_KEYS:
        assert keys.tier_for(key) == "STEEL", key
        sql = keys.normalize_sql(key, '"X"')
        assert "X" in sql
    assert BATCH_KEYS <= set(discover.KEY_DOMAIN)


def test_batch_norm_shapes(flag_on):
    # widths read off live values 2026-08-29; guard against a silent edit
    assert keys.NORM_RULES["CAGE"] == ("fixed", 5)
    assert keys.NORM_RULES["PECOS_PAC_ID"] == ("pad", 10)
    assert keys.NORM_RULES["FDIC_CERT"] == ("pad", 6)
    assert keys.NORM_RULES["RSSD"] == ("pad", 8)
    assert keys.NORM_RULES["EIA_PLANT_ID"] == ("pad", 6)
    assert keys.NORM_RULES["EIA_UTILITY_ID"] == ("pad", 6)


def test_every_batch_spec_key_col_is_map_visible(flag_on):
    problems = []
    for tbl, spec in flag_on.items():
        cols = [(spec["key"], spec["key_col"])]
        cols += [(e["key"], e["key_col"]) for e in spec.get("extra_keys", [])]
        for key, col in cols:
            if key not in BATCH_KEYS:
                continue
            scoped = keys.TABLE_COLUMN_KEYS.get((tbl, col))
            seen = scoped or keys.detect_key(col)
            if seen[0] != key:
                problems.append((tbl, col, key, seen))
    assert not problems, problems


def test_patches_land_on_existing_specs(flag_on):
    contracts = flag_on["FED_USASPENDING_CONTRACTS_FULL_R2"]["extra_keys"]
    assert {"key": "CAGE", "key_col": "CAGE_CODE"} in contracts
    assert {"key": "DUNS", "key_col": "RECIPIENT_DUNS"} in contracts  # untouched
    for t in keys._CMS_FACILITY_ENROLLMENT_TABLES:
        assert {"key": "PECOS_PAC_ID", "key_col": "ASSOCIATE_ID"} in flag_on[t]["extra_keys"], t


def test_patch_is_idempotent(flag_on):
    before = len(flag_on["FED_CMS_FACILITY_AFFILIATION"]["extra_keys"])
    specs._maybe_enable_spine_batch_2026_08_29()
    assert len(flag_on["FED_CMS_FACILITY_AFFILIATION"]["extra_keys"]) == before


def test_document_keys_are_graph_only_never_entities(flag_on):
    # An award and an enrollment record are documents (the CUSIP ruling).
    for key in ("AWARD_KEY", "PECOS_ENRLMT_ID"):
        assert key not in specs.ENTITY_TYPE_BY_KEY
        for spec in flag_on.values():
            assert spec["key"] != key
            assert all(e["key"] != key for e in spec.get("extra_keys", []))


def test_float_text_bank_tables_are_excluded():
    # FED_FDIC_FAILED_BANKS / FED_OCC_* carry CERT as '19117.0' / 'nan';
    # _alnum would mint '191170'. They stay out until the text is repaired.
    for t in ("FED_FDIC_FAILED_BANKS", "FED_OCC_NATIONAL_BANKS", "FED_OCC_THRIFTS"):
        assert not any(tbl == t for tbl, _ in keys._BATCH_2026_08_29_TABLE_COLUMN_KEYS)
