"""apply-config (2026-08-29): a keys.py / DISPLAY_SPECS change is a BOUNDED change,
classified per config unit, never an automatic full rebuild. Pure-function tests
over classify_config_drift + _config_units; no warehouse."""
from __future__ import annotations

from connect import incremental as inc

SPECS = {
    "T_NPI_A": {"key": "NPI", "key_col": "NPI", "authority": 5},
    "T_NPI_B": {"key": "NPI", "key_col": "NPI", "extra_keys": [{"key": "EIN", "key_col": "EIN"}]},
    "T_EIN": {"key": "EIN", "key_col": "EIN"},
}


def _units(norms: dict[str, str], specs: dict, tck: dict[str, str] | None = None):
    u = {("norm", k): v for k, v in norms.items()}
    u.update({("spec", t): repr(sorted(s.items())) for t, s in specs.items()})
    u.update({("tck", t): v for t, v in (tck or {}).items()})
    return u


def _pins(units):
    return {k: inc._digest(v) for k, v in units.items()}


def test_no_drift_is_a_noop():
    cur = _units({"NPI": "pad10", "EIN": "pad9"}, SPECS)
    plan = inc.classify_config_drift(_pins(cur), cur, SPECS)
    assert plan["changes"] == [] and plan["reslice"] == [] and plan["retract"] == []


def test_new_key_family_reslices_only_the_tables_that_carry_it():
    old = _units({"NPI": "pad10"}, {"T_NPI_A": SPECS["T_NPI_A"]})
    new_specs = {"T_NPI_A": SPECS["T_NPI_A"], "T_CAGE": {"key": "CAGE", "key_col": "CAGE_CODE"}}
    cur = _units({"NPI": "pad10", "CAGE": "fixed5"}, new_specs)
    plan = inc.classify_config_drift(_pins(old), cur, new_specs)
    assert ("norm", "CAGE", "added") in plan["changes"]
    assert ("spec", "T_CAGE", "added") in plan["changes"]
    assert plan["reslice"] == ["T_CAGE"]        # NOT T_NPI_A
    assert plan["retract"] == []


def test_changed_normalizer_reslices_every_table_carrying_that_family():
    old = _units({"NPI": "pad10", "EIN": "pad9"}, SPECS)
    cur = _units({"NPI": "pad10", "EIN": "pad9-NEW"}, SPECS)
    plan = inc.classify_config_drift(_pins(old), cur, SPECS)
    assert plan["changes"] == [("norm", "EIN", "changed")]
    assert plan["reslice"] == ["T_EIN", "T_NPI_B"]   # extra_keys counts as carrying


def test_extra_key_added_to_existing_table_reslices_that_table_only():
    old = _units({"NPI": "pad10", "EIN": "pad9"},
                 {**SPECS, "T_NPI_B": {"key": "NPI", "key_col": "NPI"}})
    cur = _units({"NPI": "pad10", "EIN": "pad9"}, SPECS)
    plan = inc.classify_config_drift(_pins(old), cur, SPECS)
    assert plan["changes"] == [("spec", "T_NPI_B", "changed")]
    assert plan["reslice"] == ["T_NPI_B"]


def test_removed_spec_is_retracted_not_resliced():
    old = _units({"NPI": "pad10", "EIN": "pad9"}, SPECS)
    fewer = {t: s for t, s in SPECS.items() if t != "T_EIN"}
    cur = _units({"NPI": "pad10", "EIN": "pad9"}, fewer)
    plan = inc.classify_config_drift(_pins(old), cur, fewer)
    assert plan["retract"] == ["T_EIN"]
    assert "T_EIN" not in plan["reslice"]


def test_scoped_graph_key_on_non_spec_table_goes_to_discover():
    old = _units({"NPI": "pad10"}, {"T_NPI_A": SPECS["T_NPI_A"]})
    cur = _units({"NPI": "pad10"}, {"T_NPI_A": SPECS["T_NPI_A"]},
                 {"T_GRAPH_ONLY": "[('PLANT_CODE','EIA_PLANT_ID','STEEL')]",
                  "T_NPI_A": "[('X','NPI','STEEL')]"})
    plan = inc.classify_config_drift(_pins(old), cur, {"T_NPI_A": SPECS["T_NPI_A"]})
    assert plan["discover"] == ["T_GRAPH_ONLY"]
    assert plan["reslice"] == ["T_NPI_A"]      # spec table: spine reslice covers discover too


def test_config_units_cover_every_norm_rule_spec_and_scoped_table():
    from connect import keys
    from connect.entity_index_specs import DISPLAY_SPECS
    units = inc._config_units()
    assert {n for k, n in units if k == "norm"} == set(keys.NORM_RULES)
    assert {n for k, n in units if k == "spec"} == set(DISPLAY_SPECS)
    assert {n for k, n in units if k == "tck"} == {t for t, _ in keys.TABLE_COLUMN_KEYS}


def test_legacy_fingerprint_still_deterministic_alongside_units():
    assert inc._config_fingerprint() == inc._config_fingerprint()


def test_symmetric_difference_sql_is_parenthesized():
    """Snowflake evaluates MINUS/UNION left-to-right at equal precedence; without
    parentheses the symmetric difference collapses to OLD - NEW and every ADDED key
    is dropped from the membership merge (live-verified 2026-08-29: new table,
    54,406 keys, affected=0)."""
    sql = " ".join(inc.AFFECTED_SQL.split())
    assert "(SELECT KEY_TYPE, VAL FROM _NEW MINUS SELECT KEY_TYPE, VAL FROM _OLD) UNION (SELECT KEY_TYPE, VAL FROM _OLD MINUS SELECT KEY_TYPE, VAL FROM _NEW)" in sql
