"""Wave-2 hardening tests — all offline (no Snowflake).

Covers: receipt byte-stability of compile_sql, the optional date_gate capability,
the dashboard safety chokepoint (reads route through leads.published semantics),
the overlay deriving its detectors from leads_specs.JOBS, archive-honest vessel
titles, lead_receipt SQL parameterization, and rung display honesty.
"""

import hashlib
import json
import importlib.util
import sys
from pathlib import Path

import pytest

from connect import leads
from connect import leads_overlay as ov
from connect.leads_specs import JOBS

ROOT = Path(__file__).resolve().parents[1]


def _load_script(name: str, rel: str):
    """Import a scripts/*.py file (scripts/ is not a package)."""
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


# ---- receipt byte-stability -----------------------------------------------------
# SHA256 of compile_sql output per live rule, as_of frozen to 2026-01-01. If any
# of these move, persisted SQL_SHA256 receipts churn for rules that never asked
# for a new feature — that is the exact regression this test exists to catch.
#
# 2026-07-30: 3 of these 7 values (banned_but_operating, banned_but_paid,
# excluded_but_billing) were failing on HEAD. Traced compile_sql/leads_specs.py
# history (git log) and confirmed neither has changed since a324a7df, the
# commit that introduced date_gate and originally captured these goldens --
# so the recorded hashes were miscalculated/wrong from the moment they were
# committed, not broken by later drift. Recomputed and verified live against
# the current (unchanged, correct) compile_sql output.
#
# 2026-07-31: banned_but_operating's hash moved AGAIN, this time for a real,
# intentional reason -- leads_specs.py's _FACILITY_NAME_TABLES was missing 3
# CCN-keyed facility rosters (FED_NURSINGHOME411, FED_CMS_HCRIS,
# FED_CMS_NURSING_HOME) wired onto the spine after this list was written; a
# lead whose facility only existed in one of those three fired with a blank
# facility name. Fixed by adding them (leads_specs.py, leads.py's enrich_name
# join). This is exactly the kind of change this test exists to make visible,
# not silently pass through -- recomputed and re-pinned deliberately.
#
# 2026-08-11 (spine audit): five hashes moved for two deliberate, measured reasons.
# (a) The pad-mode normalizer now NULLs placeholder IDs -- EIN '999999999' had fused
#     CVS, SK Telecom, Kingsway Financial, Enstar and a literal 'TEST Company' into
#     one spine entity across 16 sources -- so every pad-key lens re-compiles.
# (b) debarred_but_funded was repointed from the 9,000-row capped SAM sample to the
#     full 167,928-row list (2,940 -> 38,425 distinct UEIs). Recomputed and re-pinned
#     on purpose; the vessel lenses are unchanged because IMO is not a pad key.
GOLDEN_SQL_SHA256 = {
    "banned_but_operating": "37c7cebedf41ccdc3c03458e222617244896403604b68616be7e09f806ddc198",
    "sanctioned_vessel_broadcasting": "2712127fd0ce1da6e2f3cc2008a7a0910f93d6e21ebaa96877bd1b0e513d1e89",
    "debarred_but_funded": "a5d76197f82de9db2b2e445da109f4c921426ec8083c2a42b9fdc20bde8fb8d8",
    "banned_but_paid": "dc3203e6ec371c096de3a45bd7aa51f0857ccdd01bf1d4b46aadd7561a8f1954",
    "excluded_but_billing": "d06a6b4f4e9a35f1441206cc30e1ae9437dbce3c94f755309c52ab004d4698fc",
    "sanctioned_vessel_broadcasting_v2": "4339d5c832a1e26c145ab600194bfc8284cbe9e8f6e53673573249ecc04ecd7e",
    "sec_filer_in_irs_bmf": "5718caaf82c98b2654934f6d26a28faa4baf9bb6d5a6ab42bb306d53d2b8f846",
}


def test_compile_sql_byte_stable_for_existing_specs():
    assert set(GOLDEN_SQL_SHA256) == set(JOBS), "new/renamed rule: capture its golden hash"
    for rule, want in GOLDEN_SQL_SHA256.items():
        sql = leads.compile_sql(JOBS[rule], as_of="2026-01-01")
        got = hashlib.sha256(sql.encode()).hexdigest()
        assert got == want, f"{rule}: compiled SQL changed (receipt hashes would churn)"


def test_all_person_vs_person_specs_require_surname():
    """No live spec should ever ship without this -- it's the only name-based
    sanity check on a person-vs-person join. Locks in the current (correct)
    state so a future copy-pasted spec can't silently regress it."""
    for name, spec in JOBS.items():
        lkind = "person" if "name_cols" in spec.get("left", {}) else None
        rkind = "person" if "name_cols" in spec.get("right", {}) else None
        if lkind == rkind == "person":
            assert spec.get("require_surname") is True, f"{name}: person-vs-person without require_surname"


def test_compile_sql_refuses_a_person_pair_without_require_surname():
    spec = {
        "rule_name": "t_no_surname_guard",
        "title_template": "{l_last}: {count}",
        "left": {"table": "L_TBL", "key": "NPI", "key_col": "NPI",
                 "name_cols": ["LAST", "FIRST"]},
        "right": {"table": "R_TBL", "key": "NPI", "key_col": "NPI",
                  "name_cols": ["R_LAST", "R_FIRST"]},
        "score": {"breadth_w": 1.0, "breadth_div": 10.0},
        "no_fanout_guard": True,
        # require_surname deliberately omitted
    }
    with pytest.raises(ValueError, match="require_surname"):
        leads.compile_sql(spec, as_of="2026-01-01")


# ---- date_gate capability --------------------------------------------------------

def _mini_spec(**extra):
    spec = {
        "rule_name": "t_dategate",
        "title_template": "{l_name}: {count}",
        "left": {"table": "L_TBL", "key": "NPI", "key_col": "NPI", "name_col": "NM"},
        "right": {"table": "R_TBL", "key": "NPI", "key_col": "NPI",
                  "carry": {"X": "XCOL"}},
        "score": {"breadth_w": 1.0, "breadth_div": 10.0},
        "no_fanout_guard": True,
    }
    spec.update(extra)
    return spec


def test_gate_mode_adds_predicate_and_timeline():
    sql = leads.compile_sql(_mini_spec(
        date_mode="gate",
        left_date_field={"col": "EXCLDATE", "format": "YYYYMMDD"},
        right_date_field={"col": "PAY_DATE", "format": "MM/DD/YYYY"},
    ), as_of="2026-01-01")
    assert ("TRY_TO_DATE(a.R_DATEGATE, 'MM/DD/YYYY') >= "
            "TRY_TO_DATE(l.L_DATEGATE, 'YYYYMMDD')") in sql
    assert "'timeline', OBJECT_CONSTRUCT('left_date', l.L_DATEGATE" in sql


def test_gate_mode_year_field_compares_years():
    sql = leads.compile_sql(_mini_spec(
        date_mode="gate",
        left_date_field={"col": "EXCLDATE", "format": "YYYYMMDD"},
        right_year_field="PROGRAM_YEAR",
    ), as_of="2026-01-01")
    assert "TRY_TO_NUMBER(a.R_DATEGATE) >= YEAR(TRY_TO_DATE(l.L_DATEGATE, 'YYYYMMDD'))" in sql


def test_annotate_mode_has_timeline_but_no_predicate():
    sql = leads.compile_sql(_mini_spec(
        date_mode="annotate",
        left_date_field="EXCLDATE",
        right_date_field="PAY_DATE",
    ), as_of="2026-01-01")
    assert "'timeline'" in sql
    assert ">= TRY_TO_DATE(l.L_DATEGATE" not in sql and ">= YEAR(" not in sql


def test_spec_without_date_fields_emits_no_dategate_artifacts():
    sql = leads.compile_sql(_mini_spec(), as_of="2026-01-01")
    assert "DATEGATE" not in sql and "timeline" not in sql


def test_date_mode_validation():
    with pytest.raises(ValueError):
        leads.compile_sql(_mini_spec(date_mode="bogus", left_date_field="A",
                                     right_date_field="B"))
    with pytest.raises(ValueError):   # gate declared but no right-side date
        leads.compile_sql(_mini_spec(date_mode="gate", left_date_field="A"))


# ---- dashboard chokepoint (pure parts) --------------------------------------------

dash = _load_script("_dash_srv_under_test", "scripts/dashboard_server.py")


def test_dashboard_never_queries_leads_table_directly():
    """The libel firewall is only real if the ONLY read path is leads.published()."""
    for rel in ("scripts/dashboard_server.py", "scripts/build_dashboard.py"):
        src = (ROOT / rel).read_text(encoding="utf-8")
        assert '"CONNECT".LEADS' not in src, f"{rel} bypasses the chokepoint"
        assert "published(" in src


def test_insights_shape_from_gated_rows(monkeypatch):
    rows = [{"LEAD_ID": "LEAD_x", "RULE_NAME": "banned_but_paid", "LEFT_KEY_TYPE": "NPI",
             "LEFT_KEY_VALUE": "123", "TITLE": "t", "SCORE": 0.5,
             "EVIDENCE": '[{"payer": "ACME PHARMA", "npi": "123"}]',
             "STATUS": "active", "REVIEW_STATE": "pending", "PUBLISHED": False}]
    monkeypatch.setattr(dash, "_published", lambda: rows)
    out = dash.insights()
    assert out[0]["lead_id"] == "LEAD_x"
    assert out[0]["review"] == "pending" and out[0]["published"] is False
    assert out[0]["evidence"] == ["ACME PHARMA"]   # id fields never shown as labels


def test_insight_detail_refuses_ungated_lead(monkeypatch):
    """A rejected/stale lead's detail page must refuse to render — and must not leave a
    cache entry that a later call could serve."""
    dash._cache.clear()
    monkeypatch.setattr(dash, "_published", lambda: [])
    out = dash.insight_detail("LEAD_suppressed")
    assert "error" in out
    assert not any(k.startswith("ins:LEAD_suppressed") for k in dash._cache)


def test_insight_detail_cache_key_carries_review_state(monkeypatch):
    """Same lead, verdict flips pending->confirmed: the second call must not be served
    the page cached under the first verdict."""
    dash._cache.clear()
    monkeypatch.setattr(dash, "q", lambda sql, params=None: ([], []))  # no live warehouse
    lead = {"LEAD_ID": "LEAD_y", "RULE_NAME": "banned_but_paid", "LEFT_KEY_VALUE": "1",
            "TITLE": "t", "REVIEW_STATE": "pending"}
    monkeypatch.setattr(dash, "_published", lambda: [lead])
    dash._cache["ins:LEAD_y:pending"] = {"title": "cached-under-pending"}
    assert dash.insight_detail("LEAD_y") == {"title": "cached-under-pending"}
    lead2 = dict(lead, REVIEW_STATE="confirmed")
    monkeypatch.setattr(dash, "_published", lambda: [lead2])
    out = dash.insight_detail("LEAD_y")
    assert out != {"title": "cached-under-pending"}
    assert out.get("review") == "confirmed"


def test_dashboard_labels_and_detail_cover_all_rules():
    assert set(dash.RULE_LABEL) == set(JOBS)
    assert set(dash.DETAIL) == set(JOBS)


def test_ensure_leads_table_runs_ddl_once_per_process(monkeypatch):
    calls = []
    monkeypatch.setattr(leads.db, "rows", lambda conn, sql, params=None: calls.append(sql))
    monkeypatch.setattr(leads, "_LEADS_TABLE_READY", False)
    leads._ensure_leads_table(object())
    n = len(calls)
    assert n >= 1
    leads._ensure_leads_table(object())
    assert len(calls) == n, "read path must not re-run DDL per request"


def test_published_source_filters_active_status():
    """published() is the chokepoint: it must SQL-filter STATUS='active' (staleness)
    on top of the DECISIONS gate."""
    import inspect
    src = inspect.getsource(leads.published)
    assert "COALESCE(STATUS, 'active') = 'active'" in src


# ---- overlay derives from JOBS -----------------------------------------------------

def test_overlay_detectors_derive_from_jobs():
    assert {d[0] for d in ov.DETECTORS} == set(JOBS)
    for _, lt, rt, _ in ov.DETECTORS:
        assert "." not in lt and "." not in rt   # staging FQNs mapped to bare ids


def test_overlay_fallback_counts_cover_all_rules():
    assert set(ov.FALLBACK_COUNTS) == set(JOBS)


def test_overlay_builds_figure_for_all_rules():
    pytest.importorskip("plotly")  # rendering needs the viz dep; pure logic tests below don't
    fig = ov.build_figure(dict(ov.FALLBACK_COUNTS))
    # one line trace per firing rule + 2 node traces + legend traces
    n_edges = sum(1 for t in fig.data if t.mode == "lines" and t.x and t.x[0] is not None)
    assert n_edges == len(JOBS)


def test_overlay_unknown_table_autostacks_instead_of_keyerror(monkeypatch):
    pytest.importorskip("plotly")  # rendering needs the viz dep
    fake = ov.DETECTORS + [("brand_new_rule", "FED_NEVER_SEEN_FLAGS",
                            "FED_NEVER_SEEN_ACTIVITY", "EIN")]
    monkeypatch.setattr(ov, "DETECTORS", fake)
    counts = dict(ov.FALLBACK_COUNTS, brand_new_rule=3)
    fig = ov.build_figure(counts)   # must not raise
    assert fig is not None


def test_overlay_concentration_annotation_is_derived_not_frozen():
    src = Path(ov.__file__).read_text(encoding="utf-8")
    assert "338 of 353" not in src


# ---- archive-honest vessel titles ---------------------------------------------------

def test_vessel_titles_never_claim_current_broadcasting():
    for rule in ("sanctioned_vessel_broadcasting", "sanctioned_vessel_broadcasting_v2"):
        t = JOBS[rule]["title_template"]
        assert "appears in" in t and "archive" in t, rule
        assert "broadcasting AIS in" not in t, rule


# ---- lead_receipt parameterization ---------------------------------------------------

lr = _load_script("_lead_receipt_under_test", "scripts/lead_receipt.py")


def test_receipt_query_binds_user_input():
    inj = "x' OR '1'='1"
    sql, params = lr._build_query(inj, None, 5)
    assert inj not in sql and params == (inj, 5)
    sql2, params2 = lr._build_query(None, "o'hara", 3)
    assert "O'HARA" not in sql2 and params2 == ("O'HARA", 3)
    sql3, params3 = lr._build_query(None, None, 7)
    assert params3 == (7,) and "LIMIT %s" in sql3


def test_receipt_file_has_no_fstring_sql():
    src = (ROOT / "scripts" / "lead_receipt.py").read_text(encoding="utf-8")
    assert "f\"WHERE" not in src and "f'WHERE" not in src
    assert "LIMIT {" not in src


# ---- rung display honesty -------------------------------------------------------------

def test_rung_display_carries_measured_precision():
    s = leads.rung_display("CONFIRMED", 0.876)
    assert "CONFIRMED" in s and "87.6% measured precision" in s
    assert "health-provider calibration only" in s


def test_rung_display_without_measurement_never_implies_confidence():
    s = leads.rung_display("STRONG")
    assert "no measured precision" in s and "uncalibrated" in s


# ---- EIN detector: SEC filer ⋈ IRS exempt-org master file (Wave-6 lever) --------------

def test_ein_spec_compiles_as_ein_intersection():
    """The EIN detector is a hard-key intersection on the 9-digit EIN — both sides
    normalized pad-9, joined on the canonical key K_N."""
    spec = JOBS["sec_filer_in_irs_bmf"]
    sql = leads.compile_sql(spec, as_of="2026-01-01")
    # EIN pad-9 normalization (keys.py 'pad' 9 -> LPAD to 9) on BOTH sides, joined on K_N
    assert "LPAD" in sql and "9, '0'" in sql
    assert "a.K_N = l.K_N" in sql
    # right table is the IRS BMF; left is the GOOD SEC financials table
    assert "LIBRARY_RAW.LANDING.FED_SEC_EDGAR_FINANCIALS" in sql
    assert "LIBRARY_RAW.LANDING.FED_IRS_BMF" in sql


def test_ein_spec_never_touches_the_poisoned_sec_table():
    """FED_US_SEC_EDGAR's EIN column is junk (25 distinct EINs on 48,990 rows) — the
    detector must use FED_SEC_EDGAR_FINANCIALS instead, never the poisoned table."""
    spec = JOBS["sec_filer_in_irs_bmf"]
    assert spec["left"]["table"] != "FED_US_SEC_EDGAR"
    sql = leads.compile_sql(spec, as_of="2026-01-01")
    assert "FED_US_SEC_EDGAR" not in sql


def test_ein_spec_uses_org_display_no_surname_gate():
    """Both sides are org lists -> single-name display; require_surname is person-only,
    so no surname corroboration predicate must appear."""
    spec = JOBS["sec_filer_in_irs_bmf"]
    assert "name_col" in spec["left"] and "name_cols" not in spec["left"]
    assert not spec.get("require_surname")
    sql = leads.compile_sql(spec, as_of="2026-01-01")
    assert "L_NAME" in sql            # org single-name display
    assert "R_LAST" not in sql        # no person columns on the right
    assert "l.L_LAST = a.R_LAST" not in sql   # no surname gate


def test_ein_spec_carries_evidence_and_neutral_title():
    """Evidence carries SEC CIK (left) + IRS name/state/ntee (right); the title is a
    neutral co-occurrence claim, never a violation assertion."""
    spec = JOBS["sec_filer_in_irs_bmf"]
    sql = leads.compile_sql(spec, as_of="2026-01-01")
    assert "'cik'" in sql                                   # left CIK in title fields
    assert "'irs_name'" in sql and "'state'" in sql and "'ntee'" in sql
    t = spec["title_template"]
    assert "also appears in" in t                           # co-occurrence phrasing
    for banned in ("violat", "illegal", "fraud", "banned", "crime"):
        assert banned not in t.lower(), f"title overclaims: {banned!r}"


# ---- the detector backlog: derived, never frozen prose ---------------------- #
def test_detector_backlog_excludes_keys_a_detector_already_covers(tmp_path, monkeypatch):
    """The caption was hardcoded on 2026-06-27 ("STEEL 37 · CCN~NPI 39 · NPI 21 ·
    CIK 1") and was materially wrong by 2026-07-31 -- CCN~NPI had gone 39 -> 67 and
    NPI had since GAINED a detector, so listing it as backlog was doubly wrong. The
    point of the caption is "where to aim next", so a key that already has a rule
    must never appear in it."""
    covered = sorted({k for *_, k in ov.DETECTORS})
    assert covered, "DETECTORS should derive at least one key from JOBS"
    graph = {"edges": [
        {"a": "T1", "b": "T2", "key": covered[0], "tier": "STEEL"},   # covered -> excluded
        {"a": "T3", "b": "T4", "key": "ZZ_UNCOVERED", "tier": "STEEL"},
        {"a": "T5", "b": "T6", "key": "ZZ_UNCOVERED", "tier": "BRIDGE"},
        {"a": "T7", "b": "T8", "key": "ZZ_GEOKEY", "tier": "GEO"},    # geo -> excluded
        {"a": "T9", "b": "TA", "key": "ZZ_NAMEKEY", "tier": "CORROBORATED"},
    ]}
    p = tmp_path / "connect_graph.json"
    p.write_text(json.dumps(graph))
    monkeypatch.setattr(ov, "GRAPH", p)

    backlog = dict(ov._detector_backlog())
    assert backlog == {"ZZ_UNCOVERED": 2}, (
        f"backlog should count only uncovered HARD-ID edges, got {backlog}")
    assert covered[0] not in backlog       # a key with a rule is not backlog
    assert "ZZ_GEOKEY" not in backlog      # GEO is context, not identity
    assert "ZZ_NAMEKEY" not in backlog     # name-tier would propose merging strangers


def test_detector_backlog_fails_closed_when_the_graph_is_missing(tmp_path, monkeypatch):
    """No graph -> no claim. The caller omits the caption entirely rather than
    render a stale one, which is the whole failure this replaced."""
    monkeypatch.setattr(ov, "GRAPH", tmp_path / "does_not_exist.json")
    assert ov._detector_backlog() == []
