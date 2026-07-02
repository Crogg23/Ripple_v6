"""Offline unit tests for ripple/review.py -- the batch review cockpit.

Everything here is pure: no live Snowflake, no real input(). We pin the four load-bearing
pure pieces the interactive loop leans on:
  - recommend()             : rule + title + evidence -> (verdict, why). The whole heuristic.
  - exclusion_date_from_title / evidence_years : the timeline parsing recommend() rests on.
  - decision_record_args()  : keystroke -> the positional args for safety.record (or None = no write).
  - leads_fetch_sql / domains_fetch_sql : the queue-fetch SQL builders (shape + params).
  - suggest_domain()        : title/id keyword -> governed domain guess.
  - the interactive loops    : with a stubbed conn + stubbed safety + monkeypatched input(),
                               confirming a human keystroke is required for every write and that
                               'q' stops, 's'/junk writes nothing, and staging vs --apply branch.
"""
import datetime as dt
import json

import pytest

from ripple import review as R


# =========================================================================== #
# exclusion_date_from_title + evidence_years -- the timeline parse
# =========================================================================== #
def test_exclusion_date_parsed_from_title():
    d = R.exclusion_date_from_title("Sam Pierce - OIG-excluded (1128a1, 2014-01-20); 1 record")
    assert d == dt.date(2014, 1, 20)


def test_exclusion_date_none_when_absent():
    assert R.exclusion_date_from_title("no date here") is None
    assert R.exclusion_date_from_title("") is None


def test_exclusion_date_bad_date_returns_none():
    # 2014-13-40 is not a real date -> must not raise.
    assert R.exclusion_date_from_title("excluded 2014-13-40") is None


def test_evidence_years_from_json_string():
    ev = json.dumps([{"year": "2022", "payer": "X"}, {"year": "2019"}])
    assert sorted(R.evidence_years(ev)) == [2019, 2022]


def test_evidence_years_from_already_parsed_list():
    ev = [{"year": 2021}, {"note": "paid in 2023 and 2024"}]
    assert sorted(R.evidence_years(ev)) == [2021, 2023, 2024]


def test_evidence_years_handles_junk():
    assert R.evidence_years(None) == []
    assert R.evidence_years("not json") == []
    assert R.evidence_years([{"nature": "Food"}]) == []


# =========================================================================== #
# recommend -- the core heuristic
# =========================================================================== #
def test_recommend_confirm_when_activity_at_or_after_exclusion():
    title = "Brian S - OIG-excluded (1128a3, 2019-06-19); 6 records"
    ev = json.dumps([{"year": "2022", "payer": "Sanofi"}])
    verdict, why = R.recommend("banned_but_paid", title, ev)
    assert verdict == "confirm"
    assert "timeline supports" in why


def test_recommend_confirm_on_exact_year_boundary():
    # activity year == exclusion year still counts as on/after.
    title = "X - excluded 2022-03-01"
    ev = [{"year": 2022}]
    verdict, _ = R.recommend("excluded_but_billing", title, ev)
    assert verdict == "confirm"


def test_recommend_skip_when_activity_predates_exclusion():
    title = "Y - OIG-excluded (1128a1, 2024-01-20)"
    ev = [{"year": 2019}, {"year": 2021}]
    verdict, why = R.recommend("banned_but_paid", title, ev)
    assert verdict == "skip"
    assert "later-excluded" in why


def test_recommend_skip_for_vessel_and_archive_rules():
    v1, _ = R.recommend("sanctioned_vessel_broadcasting", "vessel IMO123 2020-01-01", [{"year": 2025}])
    v2, _ = R.recommend("sanctioned_vessel_broadcasting_v2", "vessel", [{"year": 2025}])
    assert v1 == "skip" and v2 == "skip"


def test_recommend_review_when_no_date_or_no_years():
    v1, _ = R.recommend("banned_but_paid", "no date at all", [{"year": 2022}])
    v2, _ = R.recommend("banned_but_paid", "excluded 2020-01-01", [{"nature": "Food"}])
    assert v1 == "review" and v2 == "review"


# =========================================================================== #
# decision_record_args -- keystroke -> safety.record args (or None)
# =========================================================================== #
def test_decision_args_confirm_maps_to_confirmed():
    args = R.decision_record_args("LEAD_1", "c", "chris", "looks solid")
    assert args == ("lead", "LEAD_1", "confirmed", "chris", "looks solid")


def test_decision_args_reject_maps_to_rejected():
    args = R.decision_record_args("LEAD_2", "R", "", "")
    assert args == ("lead", "LEAD_2", "rejected", "", "")


def test_decision_args_skip_and_junk_are_no_write():
    assert R.decision_record_args("LEAD_3", "s", "chris", "") is None
    assert R.decision_record_args("LEAD_3", "q", "chris", "") is None
    assert R.decision_record_args("LEAD_3", "", "chris", "") is None
    assert R.decision_record_args("LEAD_3", "x", "chris", "") is None


def test_decision_args_are_valid_for_safety_record():
    # The mapped decision must be one connect.safety accepts, or record() would raise.
    from connect import safety
    _, _, decision, _, _ = R.decision_record_args("L", "c", "", "")
    assert decision in safety.VALID


# =========================================================================== #
# queue-fetch SQL builders
# =========================================================================== #
def test_leads_fetch_sql_no_rule():
    sql, params = R.leads_fetch_sql(None, 20)
    assert params == ()
    assert 'FROM LIBRARY_META."CONNECT".LEADS' in sql
    assert "STATUS = 'active'" in sql
    assert "RULE_NAME = %s" not in sql
    assert "LIMIT 80" in sql   # over-fetch 20*4


def test_leads_fetch_sql_with_rule_binds_param():
    sql, params = R.leads_fetch_sql("banned_but_paid", 5)
    assert params == ("banned_but_paid",)
    assert "RULE_NAME = %s" in sql


def test_leads_fetch_sql_overfetch_capped():
    sql, _ = R.leads_fetch_sql(None, 1000)
    assert "LIMIT 2000" in sql   # capped, not 4000


def test_domains_fetch_sql_shape():
    sql = R.domains_fetch_sql(15)
    assert "LIBRARY_META.REGISTRY.CATALOG" in sql
    assert "UNCLASSIFIED" in sql
    assert "lifecycle IN ('landed','modeled')" in sql
    assert "LIMIT 15" in sql


# =========================================================================== #
# suggest_domain -- keyword guess against the governed 22
# =========================================================================== #
@pytest.mark.parametrize("sid,name,expected", [
    ("fed_fec_bulk", "FEC campaign finance committees", "money_in_politics"),
    ("fed_cms_open_payments", "Medicare provider payments", "health_medicine"),
    ("xc_wapo_fatal_force", "police shooting fatalities", "crime_security"),
    ("intl_opensanctions", "consolidated sanctions targets", "sanctions_enforcement"),
    ("xc_vera_incarceration", "prison incarceration trends", "justice_courts"),
    ("xc_owid_refugees", "refugee population by country", "immigration_migration"),
    ("xc_owid_co2", "CO2 emissions", "energy_environment"),
])
def test_suggest_domain_hits(sid, name, expected):
    dom, _ = R.suggest_domain(sid, name)
    assert dom == expected


def test_suggest_domain_all_suggestions_are_governed():
    # every domain the keyword table can emit must be in the governed 22.
    for _rx, dom in R.DOMAIN_KEYWORDS:
        assert dom in R.FACET_DOMAINS


def test_suggest_domain_no_match_returns_blank():
    dom, why = R.suggest_domain("portal_random_xyz", "Assorted Facility Listing 42")
    assert dom == ""
    assert "human call" in why


# =========================================================================== #
# render_evidence -- console safety
# =========================================================================== #
def test_render_evidence_compact_and_truncates():
    ev = [{"year": y, "payer": f"P{y}"} for y in range(2010, 2020)]
    out = R.render_evidence(ev, max_rows=3)
    assert out.count("\n") == 3   # 3 rows + the '... more' line
    assert "more" in out


def test_render_evidence_empty():
    assert "no structured evidence" in R.render_evidence(None)


# =========================================================================== #
# interactive leads loop -- stubbed conn + safety + input()
# =========================================================================== #
class _StubConn:
    def commit(self):
        pass


class _StubSafety:
    """Stands in for connect.safety: latest() returns the anti-join set, record() logs calls."""
    VALID = {"confirmed", "rejected", "retracted", "stale"}

    def __init__(self, already=None):
        self._already = already or {}
        self.recorded = []

    def latest(self, conn, kind):
        return dict(self._already)

    def record(self, conn, kind, target_id, decision, reviewer="", reason="", model_version=""):
        self.recorded.append((kind, target_id, decision, reviewer, reason))


class _Args:
    def __init__(self, **kw):
        self.__dict__.update(kw)


def _wire_leads(monkeypatch, rows, already=None, keys=None):
    """Patch review's conn, safety import, C.dicts (the fetch), and input()."""
    stub_safety = _StubSafety(already)
    monkeypatch.setattr(R.C, "connect", lambda *a, **k: _StubConn())
    monkeypatch.setattr(R.C, "pour_running", lambda: None)
    monkeypatch.setattr(R.C, "dicts", lambda conn, sql, params=(): list(rows))
    # the true-pending-count query (so `review` agrees with `status`) — stub it to the row count
    monkeypatch.setattr(R.C, "scalar", lambda conn, sql, params=(): len(list(rows)))
    # inject our stub safety module in place of `from connect import safety`
    import sys
    import types
    mod = types.ModuleType("connect.safety")
    mod.latest = stub_safety.latest
    mod.record = stub_safety.record
    mod.VALID = stub_safety.VALID
    monkeypatch.setitem(sys.modules, "connect.safety", mod)
    # `from connect import safety` binds via the connect package attribute (set at real import),
    # so replacing only sys.modules isn't enough once connect.safety was imported earlier.
    import connect
    monkeypatch.setattr(connect, "safety", mod, raising=False)
    if keys is not None:
        it = iter(keys)
        monkeypatch.setattr("builtins.input", lambda *a, **k: next(it))
    return stub_safety


LEAD = {"LEAD_ID": "LEAD_a", "RULE_NAME": "banned_but_paid",
        "TITLE": "Sam P - OIG-excluded (1128a1, 2019-01-20); 1 record",
        "EVIDENCE": json.dumps([{"year": "2022", "payer": "AbbVie"}]),
        "EVIDENCE_COUNT": 1, "LEFT_KEY_VALUE": "123",
        "FIRST_SEEN": None, "LAST_SEEN": None}


def test_leads_confirm_writes_one_verdict(monkeypatch):
    stub = _wire_leads(monkeypatch, [LEAD], keys=["c good case"])
    rc = R._run_leads(_Args(limit=20, rule=None, by="chris", auto_suggest=False))
    assert rc == 0
    assert stub.recorded == [("lead", "LEAD_a", "confirmed", "chris", "good case")]


def test_leads_skip_writes_nothing(monkeypatch):
    stub = _wire_leads(monkeypatch, [LEAD], keys=["s"])
    R._run_leads(_Args(limit=20, rule=None, by="chris", auto_suggest=False))
    assert stub.recorded == []


def test_leads_quit_stops_before_writing(monkeypatch):
    two = [LEAD, dict(LEAD, LEAD_ID="LEAD_b")]
    stub = _wire_leads(monkeypatch, two, keys=["q"])
    R._run_leads(_Args(limit=20, rule=None, by="chris", auto_suggest=False))
    assert stub.recorded == []


def test_leads_already_ruled_are_anti_joined(monkeypatch):
    # LEAD_a already has a verdict -> it must not even be shown; input() never called.
    stub = _wire_leads(monkeypatch, [LEAD], already={"LEAD_a": "rejected"}, keys=[])
    rc = R._run_leads(_Args(limit=20, rule=None, by="chris", auto_suggest=False))
    assert rc == 0
    assert stub.recorded == []


def test_leads_auto_suggest_never_writes(monkeypatch):
    # --auto-suggest must print + write nothing even though input() would say confirm.
    stub = _wire_leads(monkeypatch, [LEAD], keys=["c"])
    rc = R._run_leads(_Args(limit=20, rule=None, by="chris", auto_suggest=True))
    assert rc == 0
    assert stub.recorded == []


def test_leads_degrades_when_snowflake_down(monkeypatch, capsys):
    def boom(*a, **k):
        raise RuntimeError("no route to host")
    monkeypatch.setattr(R.C, "connect", boom)
    rc = R._run_leads(_Args(limit=20, rule=None, by="", auto_suggest=False))
    assert rc == 1
    assert "can't reach Snowflake" in capsys.readouterr().out


# =========================================================================== #
# interactive domains loop -- staging (default) vs --apply
# =========================================================================== #
ROW = {"SOURCE_ID": "fed_fec_bulk", "NAME": "FEC campaign finance committees",
       "DOMAIN_PRIMARY": None, "LIFECYCLE": "landed"}


def _wire_domains(monkeypatch, tmp_path, rows, keys):
    monkeypatch.setattr(R.C, "connect", lambda *a, **k: _StubConn())
    monkeypatch.setattr(R.C, "pour_running", lambda: None)
    monkeypatch.setattr(R.C, "dicts", lambda conn, sql, params=(): list(rows))
    # redirect the approvals JSON into tmp so we never touch the real outputs file.
    monkeypatch.setattr(R, "APPROVALS_PATH", tmp_path / "_appr.json")
    it = iter(keys)
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(it))


def test_domains_staging_writes_json_not_registry(monkeypatch, tmp_path):
    writes = []
    monkeypatch.setattr(R.C, "rows", lambda *a, **k: writes.append(a))
    _wire_domains(monkeypatch, tmp_path, [ROW], keys=["a"])
    rc = R._run_domains(_Args(limit=20, apply=False))
    assert rc == 0
    assert writes == []   # no registry UPDATE in staging mode
    staged = json.loads((tmp_path / "_appr.json").read_text())
    assert staged["fed_fec_bulk"]["domain"] == "money_in_politics"


def test_domains_edit_rejects_non_vocab_domain(monkeypatch, tmp_path):
    _wire_domains(monkeypatch, tmp_path, [ROW], keys=["e not_a_domain"])
    R._run_domains(_Args(limit=20, apply=False))
    staged = json.loads((tmp_path / "_appr.json").read_text())
    assert staged == {}   # bad domain skipped, nothing staged


def test_domains_edit_accepts_governed_domain(monkeypatch, tmp_path):
    _wire_domains(monkeypatch, tmp_path, [ROW], keys=["e justice_courts"])
    R._run_domains(_Args(limit=20, apply=False))
    staged = json.loads((tmp_path / "_appr.json").read_text())
    assert staged["fed_fec_bulk"]["domain"] == "justice_courts"


def test_domains_apply_writes_one_targeted_update(monkeypatch, tmp_path):
    writes = []
    monkeypatch.setattr(R.C, "rows", lambda conn, sql, params=(): writes.append((sql, params)))
    _wire_domains(monkeypatch, tmp_path, [ROW], keys=["a"])
    rc = R._run_domains(_Args(limit=20, apply=True))
    assert rc == 0
    assert len(writes) == 1
    sql, params = writes[0]
    assert "UPDATE LIBRARY_META.REGISTRY.SOURCE_REGISTRY" in sql
    assert "DOMAIN_SOURCE='human'" in sql
    assert params == ("money_in_politics", "fed_fec_bulk")


def test_domains_quit_stops(monkeypatch, tmp_path):
    writes = []
    monkeypatch.setattr(R.C, "rows", lambda *a, **k: writes.append(a))
    _wire_domains(monkeypatch, tmp_path, [ROW, dict(ROW, SOURCE_ID="x")], keys=["q"])
    R._run_domains(_Args(limit=20, apply=True))
    assert writes == []


def test_domains_degrades_when_snowflake_down(monkeypatch, capsys):
    monkeypatch.setattr(R.C, "connect", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("down")))
    rc = R._run_domains(_Args(limit=20, apply=False))
    assert rc == 1
    assert "can't reach Snowflake" in capsys.readouterr().out
