"""Wave-2 hardening tests — all offline (no Snowflake).

Covers: receipt byte-stability of compile_sql, the optional date_gate capability,
the dashboard safety chokepoint (reads route through leads.published semantics),
the overlay deriving its detectors from leads_specs.JOBS, archive-honest vessel
titles, lead_receipt SQL parameterization, and rung display honesty.
"""

import hashlib
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
# SHA256 of compile_sql output per live rule, captured 2026-07-02 BEFORE the date_gate
# capability landed, as_of frozen to 2026-01-01. If any of these move, persisted
# SQL_SHA256 receipts churn for rules that never asked for the new feature — that is
# the exact regression this test exists to catch.
GOLDEN_SQL_SHA256 = {
    "banned_but_operating": "5779967ca32aacd4166441e172657c5be5992a44e50b9e7d831bfdcf3a24c82f",
    "sanctioned_vessel_broadcasting": "2712127fd0ce1da6e2f3cc2008a7a0910f93d6e21ebaa96877bd1b0e513d1e89",
    "debarred_but_funded": "58116f2f7526c577aafbcd0c4cd2222e1128b3ad4ff6482fa175639dfd508c1d",
    "banned_but_paid": "3d4a4b56892bf11e07d2493c789c74079028445344990498820efbd856e4e4fc",
    "excluded_but_billing": "4119e84c250089fbdaf1d18f21e3bae86339d15ac075700f81f0d05a4b238120",
    "sanctioned_vessel_broadcasting_v2": "4339d5c832a1e26c145ab600194bfc8284cbe9e8f6e53673573249ecc04ecd7e",
}


def test_compile_sql_byte_stable_for_existing_specs():
    assert set(GOLDEN_SQL_SHA256) == set(JOBS), "new/renamed rule: capture its golden hash"
    for rule, want in GOLDEN_SQL_SHA256.items():
        sql = leads.compile_sql(JOBS[rule], as_of="2026-01-01")
        got = hashlib.sha256(sql.encode()).hexdigest()
        assert got == want, f"{rule}: compiled SQL changed (receipt hashes would churn)"


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
    fig = ov.build_figure(dict(ov.FALLBACK_COUNTS))
    # one line trace per firing rule + 2 node traces + legend traces
    n_edges = sum(1 for t in fig.data if t.mode == "lines" and t.x and t.x[0] is not None)
    assert n_edges == len(JOBS)


def test_overlay_unknown_table_autostacks_instead_of_keyerror(monkeypatch):
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
