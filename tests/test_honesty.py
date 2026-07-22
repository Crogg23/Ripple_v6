"""Offline tests for the honesty engine (pure logic — no Snowflake, no dbt run)."""

from pathlib import Path

import pytest

from honesty.compose import BlendRefusal, MeasureInput, assert_composable, disclosures, effective_grade
from honesty.grading import (
    FACT,
    LEAD,
    UNVERIFIED,
    analyze_model_sql,
    classify_join_clause,
    grade_model,
)
from honesty.traps import SOURCE_TRAPS, TRAPS, traps_for_source

REPO = Path(__file__).resolve().parents[1]


# ── join taxonomy ────────────────────────────────────────────────────────────

def test_hard_id_join_is_hard():
    assert classify_join_clause("a.npi = b.npi") == "hard"
    assert classify_join_clause("o.recipient_uei = s.uei") == "hard"
    assert classify_join_clause("t.cik_str = c.cik") == "hard"


def test_composite_hard_plus_name_stays_hard_anchored():
    # extra name predicates only RESTRICT a hard-anchored join
    assert classify_join_clause("o.npi = l.npi AND o.lname = l.lname") == "hard"


def test_pure_name_join_is_name():
    assert classify_join_clause("upper(a.entity_name) = upper(b.recipient_name)") == "name"
    assert classify_join_clause("a.lname = b.lastname and a.state = b.state") == "name"


def test_neutral_conformed_dims():
    assert classify_join_clause("a.state = b.state and a.year = b.year") == "neutral"


def test_empty_clause_fails_closed():
    assert classify_join_clause("") == "unparseable"
    assert classify_join_clause("   ") == "unparseable"


def test_analyze_using_and_cross_join():
    sql = """
    select * from {{ ref('a') }} x
    join {{ ref('b') }} using (icpsr, congress, chamber)
    cross join calendar
    """
    kinds = [k for k, _ in analyze_model_sql(sql)]
    assert kinds == ["hard", "neutral"]


def test_analyze_left_function_in_on_clause_does_not_fail_open():
    # LEFT( is a function here, not a join keyword — the name predicate after
    # the conformed-dim equality must still be seen.
    sql = "select * from a join b on a.state = b.state and LEFT(a.borrname,3) = LEFT(b.name,3)"
    kinds = [k for k, _ in analyze_model_sql(sql)]
    assert kinds == ["name"]


def test_comments_and_jinja_are_stripped():
    sql = """
    -- join on name would be bad, this comment must not count
    select * from {{ ref('a') }} join {{ ref('b') }} on a.npi = b.npi /* name note */
    """
    assert [k for k, _ in analyze_model_sql(sql)] == ["hard"]


def test_jinja_hash_comments_do_not_create_phantom_joins():
    # caught live 2026-07-21: a {# … #} comment containing the word "join"
    # produced a phantom unparseable finding in int_sanctioned_vessels
    sql = "{# vessels joined to AIS #} select * from {{ ref('a') }} x join {{ ref('b') }} y on x.imo = y.imo"
    assert [k for k, _ in analyze_model_sql(sql)] == ["hard"]


def test_subquery_join_is_parsed_not_truncated():
    # caught live 2026-07-21: `join (select …)` truncated at the select boundary
    sql = "select * from m join (select icpsr, congress from v) s on s.icpsr = m.icpsr"
    assert [k for k, _ in analyze_model_sql(sql)] == ["hard"]


def test_name_join_inside_subquery_cannot_hide():
    sql = ("select * from m join "
           "(select * from a join b on a.lname = b.entity_name) s "
           "on s.npi = m.npi")
    kinds = sorted(k for k, _ in analyze_model_sql(sql))
    assert kinds == ["hard", "name"]   # outer hard AND the buried name-join


def test_string_literal_parens_do_not_unbalance():
    sql = "select * from a join b on a.npi = b.npi and a.note = '(open'"
    assert [k for k, _ in analyze_model_sql(sql)] == ["hard"]


# ── the 2026-07-21 adversarial-review holes, pinned closed ───────────────────

def test_comma_join_with_name_predicate_in_where_demotes():
    # no JOIN keyword anywhere — the review's demonstrated fail-open
    sql = ("select * from {{ ref('stg_a') }} a, {{ ref('stg_b') }} b "
           "where upper(a.entity_name) = upper(b.recipient_name)")
    kinds = [k for k, _ in analyze_model_sql(sql)]
    assert "name" in kinds            # the WHERE identity predicate is seen
    assert "unparseable" in kinds     # and the bare comma-join fails closed


def test_lateral_flatten_comma_is_neutral_not_blind():
    sql = ("select f.value from base, lateral flatten("
           "input => try_parse_json(secondary_ids), outer => true ) f "
           "where lower(f.value) like '%x%'")
    kinds = [k for k, _ in analyze_model_sql(sql)]
    assert kinds == ["neutral"]       # recorded, and correctly non-demoting


def test_in_subquery_name_anchor_demotes():
    sql = ("select * from {{ ref('stg_a') }} p "
           "where p.physician_name in (select excluded_name from {{ ref('stg_b') }})")
    assert "name" in [k for k, _ in analyze_model_sql(sql)]


def test_in_subquery_hard_anchor_is_fine():
    sql = "select * from {{ ref('a') }} p where p.npi in (select npi from {{ ref('b') }})"
    kinds = [k for k, _ in analyze_model_sql(sql)]
    assert "name" not in kinds and "unparseable" not in kinds


def test_jinja_inside_on_clause_fails_closed():
    assert classify_join_clause("{{ var('join_cond') }}".replace("{{ var('join_cond') }}", "JINJA_REF")) == "unparseable"
    sql = "select * from a join b on {{ var('join_cond') }}"
    assert [k for k, _ in analyze_model_sql(sql)] == ["unparseable"]


def test_id_prefixed_name_column_is_a_name_not_an_id():
    # NPI_NAME is a name that mentions a register — must NOT upgrade to hard
    assert classify_join_clause("a.npi_name = b.npi_name") == "name"


def test_ghost_dependency_fails_closed():
    manifest = _mini_manifest()
    manifest["nodes"]["model.r.mart_ghost"] = {
        "resource_type": "model", "raw_code": "select 1",
        "depends_on": {"nodes": ["model.r.does_not_exist"]},
        "original_file_path": "models/marts/x.sql",
    }
    g = grade_model(manifest, "model.r.mart_ghost")
    assert g.grade == UNVERIFIED
    assert any(r.kind == "unknown_ancestor" for r in g.reasons)


def test_claim_name_inside_string_or_jinja_comment_does_not_demote():
    manifest = _mini_manifest()
    manifest["nodes"]["model.r.mart_talky"] = {
        "resource_type": "model",
        "raw_code": ("{# context: see LIBRARY_META.CONNECT.LEADS #} "
                     "select 'docs: CONNECT.LEADS has the claims' as note "
                     "from {{ ref('stg_a') }}"),
        "depends_on": {"nodes": ["model.r.stg_a"]},
        "original_file_path": "models/marts/x.sql",
    }
    g = grade_model(manifest, "model.r.mart_talky")
    assert g.grade == FACT and g.reasons == []


def test_natural_join_fails_closed_with_clear_receipt():
    out = analyze_model_sql("select * from a natural join b")
    assert out[0][0] == "unparseable" and "NATURAL" in out[0][1]


def test_alias_ending_in_cross_is_not_a_cross_join():
    # 't_across join b' with no predicate must fail closed, not read as CROSS
    out = analyze_model_sql("select * from t_across join b")
    assert out[0][0] == "unparseable"


def test_measure_input_for_mart_ties_labels_to_derived_grades(tmp_path):
    import json as _json

    from honesty.compose import measure_input_for_mart

    grades_file = tmp_path / "mart_grades.json"
    grades_file.write_text(_json.dumps({
        "grades": {"model.r.lead_queue": {"grade": "lead", "traps": ["trap_ais_snapshot"]}}
    }))
    mi = measure_input_for_mart("lead_queue", grades_file)
    assert mi.grade == LEAD and mi.traps == ("trap_ais_snapshot",)
    with pytest.raises(KeyError):
        measure_input_for_mart("nope", grades_file)


# ── lineage grading (synthetic mini-manifest) ────────────────────────────────

def _mini_manifest():
    def model(raw, deps=()):
        return {"resource_type": "model", "raw_code": raw,
                "depends_on": {"nodes": list(deps)}, "original_file_path": "models/marts/x.sql"}

    return {
        "nodes": {
            "model.r.stg_a": model("select * from {{ source('raw','T_A') }}", ["source.r.raw.T_A"]),
            "model.r.stg_b": model("select * from {{ source('raw','T_B') }}", ["source.r.raw.T_B"]),
            "model.r.stg_ais": model("select * from {{ source('raw','FED_NOAA_AIS') }}",
                                     ["source.r.raw.FED_NOAA_AIS"]),
            "model.r.mart_hard": model(
                "select * from {{ ref('stg_a') }} a join {{ ref('stg_b') }} b "
                "on a.npi = b.npi and a.lname = b.lname",
                ["model.r.stg_a", "model.r.stg_b"]),
            "model.r.mart_name": model(
                "select * from {{ ref('stg_a') }} a join {{ ref('stg_b') }} b "
                "on upper(a.entity_name) = upper(b.recipient_name)",
                ["model.r.stg_a", "model.r.stg_b"]),
            "model.r.mart_claims": model(
                "select * from {{ source('meta','V_LEADS_PUBLISHED') }}",
                ["source.r.meta.V_LEADS_PUBLISHED"]),
            "model.r.mart_empty": model("", ["model.r.stg_a"]),
            "model.r.mart_child_of_name": model(
                "select * from {{ ref('mart_name') }}", ["model.r.mart_name"]),
            "model.r.mart_ais": model(
                "select imo, count(*) n from {{ ref('stg_ais') }} group by 1",
                ["model.r.stg_ais"]),
        },
        "sources": {
            "source.r.raw.T_A": {"identifier": "T_A"},
            "source.r.raw.T_B": {"identifier": "T_B"},
            "source.r.raw.FED_NOAA_AIS": {"identifier": "FED_NOAA_AIS"},
            "source.r.meta.V_LEADS_PUBLISHED": {"identifier": "V_LEADS_PUBLISHED"},
        },
    }


def test_hard_join_lineage_is_fact():
    g = grade_model(_mini_manifest(), "model.r.mart_hard")
    assert g.grade == FACT and g.reasons == []


def test_name_join_fails_closed_to_unverified():
    g = grade_model(_mini_manifest(), "model.r.mart_name")
    assert g.grade == UNVERIFIED
    assert any(r.kind == "name_join" for r in g.reasons)


def test_claim_ancestry_grades_lead():
    g = grade_model(_mini_manifest(), "model.r.mart_claims")
    assert g.grade == LEAD
    assert any(r.kind == "claim_ancestry" for r in g.reasons)


def test_missing_sql_fails_closed():
    g = grade_model(_mini_manifest(), "model.r.mart_empty")
    assert g.grade == UNVERIFIED
    assert any(r.kind == "no_sql" for r in g.reasons)


def test_grade_inherits_weakest_ancestor():
    # a clean SELECT over a name-joined parent is still unverified
    g = grade_model(_mini_manifest(), "model.r.mart_child_of_name")
    assert g.grade == UNVERIFIED


def test_traps_travel_without_changing_grade():
    g = grade_model(_mini_manifest(), "model.r.mart_ais")
    assert g.grade == FACT                       # provenance is clean...
    assert "trap_ais_snapshot" in g.traps        # ...but the poison label travels


# ── the refusal ──────────────────────────────────────────────────────────────

def test_refuses_fact_lead_blend_into_one_scalar():
    with pytest.raises(BlendRefusal):
        assert_composable([MeasureInput("payments", FACT), MeasureInput("leads", LEAD)])


def test_same_grade_blends_pass():
    grade, _ = assert_composable([MeasureInput("a", FACT), MeasureInput("b", FACT)])
    assert grade == FACT
    grade, _ = assert_composable([MeasureInput("a", LEAD), MeasureInput("b", UNVERIFIED)])
    assert grade == UNVERIFIED                   # weakest wins; never pretended to be fact


def test_side_by_side_render_is_allowed():
    grade, _ = assert_composable(
        [MeasureInput("a", FACT), MeasureInput("b", LEAD)], single_scalar=False)
    assert grade == LEAD


def test_traps_union_and_disclosures():
    _, traps = assert_composable(
        [MeasureInput("a", FACT, ("trap_ais_snapshot",)),
         MeasureInput("b", FACT, ("trap_usaspending_grain",))])
    assert traps == ("trap_ais_snapshot", "trap_usaspending_grain")
    texts = disclosures(traps)
    assert len(texts) == 2 and "stale 8-day snapshot" in texts[0]


def test_effective_grade_orders_correctly():
    assert effective_grade([MeasureInput("a", FACT), MeasureInput("b", UNVERIFIED)]) == UNVERIFIED


# ── the trap mirror tripwire ─────────────────────────────────────────────────

def test_traps_mirror_registry_seeds():
    """honesty/traps.py mirrors scripts/build_registry_setup.py POLICY seeds.
    A distinctive single-line fragment of each statement must appear in the
    seed file — if a seed changes, this fires and the mirror gets re-synced."""
    seed = (REPO / "scripts" / "build_registry_setup.py").read_text()
    fragments = {
        "trap_open_payments_split": "THREE landing tables",
        "trap_ais_snapshot": "58,106,517 rows spanning exactly",
        "trap_leie_npi_and_dates": "NPI='0000000000' on 74,780/83,464 rows",
        "trap_ofac_sdn_type": "literal sentinel '-0- '",
        "trap_usaspending_grain": "one row per TRANSACTION, not per award",
    }
    assert set(fragments) == set(TRAPS)
    for key, frag in fragments.items():
        assert f'key="{key}"' in seed, f"{key} missing from registry seeds"
        assert frag in seed, f"seed text drifted for {key}"
        assert frag in TRAPS[key], f"mirror text drifted for {key}"
    for table, keys in SOURCE_TRAPS.items():
        assert all(k in TRAPS for k in keys)
        assert traps_for_source(table.lower()) == keys   # case-insensitive
