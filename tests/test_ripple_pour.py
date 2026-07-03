"""Offline unit tests for ripple/pour.py — the deterministic-first router (#5),
the live meter parse (#3), and the refuse-when-a-pour-is-live guard.

No live DB, no real pour: SPECS are stubbed, C.pour_running is monkeypatched, and
subprocess is patched so `run --run` never actually launches anything.
"""
import json
import types

import pytest

from ripple import pour
from ripple import common as C


# --------------------------------------------------------------- fixtures
def _stub_specs(ids):
    """A fake specs module exposing a .SPECS list like scripts/bridge_fuel_specs.py."""
    return types.SimpleNamespace(SPECS=[{"source_id": s} for s in ids])


SAMPLE_QUEUE = [
    {"name": "CMS Facility Affiliation", "source_id": "fed_cms_facility_affiliation",
     "url": "https://data.cms.gov/provider-data/dataset/27ea-46a8"},          # spec -> deterministic
    {"name": "City Budget", "source_id": "loc_city_budget",
     "url": "https://data.cityofx.gov/resource/abcd-1234.json"},              # /resource/ -> portal
    {"name": "BIA Geo", "source_id": "fed_bia_tribal_geo",
     "url": "https://opendata-1-bia-geospatial.hub.arcgis.com/"},             # arcgis -> portal
    {"name": "Some Novel API", "source_id": "fed_novel_api",
     "url": "https://novel.example.gov/api/docs"},                            # novel -> LLM
]


# --------------------------------------------------------------- classify (#5)
def test_known_spec_ids_reads_stub_modules():
    ids = pour.known_spec_ids([_stub_specs(["a", "b"]), _stub_specs(["c"])])
    assert ids == {"a", "b", "c"}


def test_classify_splits_deterministic_vs_llm():
    spec_ids = {"fed_cms_facility_affiliation"}
    split = pour.classify(SAMPLE_QUEUE, spec_ids)
    det_ids = {e["source_id"] for e in split["deterministic"]}
    llm_ids = {e["source_id"] for e in split["llm"]}

    assert det_ids == {"fed_cms_facility_affiliation", "loc_city_budget", "fed_bia_tribal_geo"}
    assert llm_ids == {"fed_novel_api"}


def test_classify_reason_tags():
    split = pour.classify(SAMPLE_QUEUE, {"fed_cms_facility_affiliation"})
    by_id = {e["source_id"]: e["route_reason"] for e in split["deterministic"] + split["llm"]}
    assert by_id["fed_cms_facility_affiliation"] == "bridge_fuel spec"
    assert by_id["loc_city_budget"] == "portal loader"
    assert by_id["fed_bia_tribal_geo"] == "portal loader"
    assert by_id["fed_novel_api"] == "novel"


def test_is_portal_detects_identifiers_too():
    assert pour.is_portal({"url": "https://x.gov", "identifiers": ["Socrata"]}) is True
    assert pour.is_portal({"url": "https://x.gov/api", "identifiers": ["FIPS"]}) is False


# --------------------------------------------------------------- meter parse (#3)
def test_parse_position_takes_latest_marker():
    text = "Onboarding A\n[1 of 720]\n...\n[99 of 720]\nOnboarding B"
    assert pour.parse_position(text) == (99, 720)


def test_parse_position_none_when_absent():
    assert pour.parse_position("no markers here") is None


def test_tally_log_counts_by_status():
    log = {
        "A": {"status": "complete", "source_id": "a"},
        "B": {"status": "failed"},
        "C": {"status": "failed"},
        "D": {"status": "needs_key"},
        "E": {"status": "empty"},
        "F": {"status": "already_cataloged"},
        "G": {"status": "weird_new_status"},   # unknown -> 'other'
    }
    counts = pour.tally_log(log)
    assert counts["complete"] == 1
    assert counts["failed"] == 2
    assert counts["needs_key"] == 1
    assert counts["empty"] == 1
    assert counts["already_cataloged"] == 1
    assert counts["other"] == 1


def test_render_meter_shape_running():
    counts = {"complete": 39, "failed": 29, "needs_key": 4, "empty": 2,
              "already_cataloged": 0, "other": 0}
    line = pour.render_meter(counts, pos=(72, 720), total=720,
                             last_fail="fed_bls_qcew (404)", running=True)
    assert line.startswith("POUR [72/720] 10%")
    assert "done 39" in line and "failed 29" in line
    assert "need-key 4" in line and "empty 2" in line
    assert "last fail: fed_bls_qcew (404)" in line


def test_render_meter_ended_marker():
    counts = {"complete": 5, "failed": 0, "needs_key": 0, "empty": 0,
              "already_cataloged": 0, "other": 0}
    line = pour.render_meter(counts, pos=None, total=None, last_fail=None, running=False)
    assert line.startswith("POUR (ended)")
    assert "done 5" in line


def test_queue_total_from_cmdline(tmp_path):
    q = tmp_path / "q.json"
    q.write_text(json.dumps([{"source_id": "a"}, {"source_id": "b"}]), encoding="utf-8")
    cmd = f'python onboard.py --batch --yes --queue {q}'
    assert pour.queue_total_from_cmdline(cmd) == 2


def test_queue_total_from_cmdline_none_when_no_flag():
    assert pour.queue_total_from_cmdline("python onboard.py --batch") is None


# --------------------------------------------------------------- run guard (#5)
def test_run_refuses_when_pour_live(tmp_path, monkeypatch, capsys):
    q = tmp_path / "q.json"
    q.write_text(json.dumps(SAMPLE_QUEUE), encoding="utf-8")
    monkeypatch.setattr(pour.C, "pour_running", lambda: "python onboard.py --batch")

    args = types.SimpleNamespace(action="run", queue=str(q), run=True, interval=5, once=False)
    rc = pour.run(args)

    out = capsys.readouterr().out
    assert rc == 1
    assert "REFUSING" in out


def test_run_dry_does_not_execute(tmp_path, monkeypatch, capsys):
    q = tmp_path / "q.json"
    q.write_text(json.dumps(SAMPLE_QUEUE), encoding="utf-8")
    monkeypatch.setattr(pour.C, "pour_running", lambda: None)
    monkeypatch.setattr(pour, "known_spec_ids", lambda *a, **k: {"fed_cms_facility_affiliation"})

    # If run tried to execute, this would blow up — DRY must never call subprocess.
    def _boom(*a, **k):
        raise AssertionError("subprocess.run must not be called in a DRY plan")
    monkeypatch.setattr(pour.subprocess, "run", _boom)

    args = types.SimpleNamespace(action="run", queue=str(q), run=False, interval=5, once=False)
    rc = pour.run(args)

    out = capsys.readouterr().out
    assert rc == 0
    assert "DRY plan" in out
    assert "bridge_fuel_load.py --spec fed_cms_facility_affiliation" in out


def test_run_run_launches_both_stages(tmp_path, monkeypatch, capsys):
    q = tmp_path / "q.json"
    q.write_text(json.dumps(SAMPLE_QUEUE), encoding="utf-8")
    monkeypatch.setattr(pour.C, "pour_running", lambda: None)
    monkeypatch.setattr(pour, "known_spec_ids", lambda *a, **k: {"fed_cms_facility_affiliation"})

    calls = []

    class _Res:
        returncode = 0

    def _fake_run(cmd, **k):
        calls.append(cmd)
        return _Res()

    monkeypatch.setattr(pour.subprocess, "run", _fake_run)

    args = types.SimpleNamespace(action="run", queue=str(q), run=True, interval=5, once=False)
    rc = pour.run(args)

    assert rc == 0
    # two launches: bridge_fuel for deterministic, onboard batch for the LLM remainder
    assert any("bridge_fuel_load.py" in " ".join(c) for c in calls)
    assert any("onboard.py" in " ".join(c) for c in calls)
    # remainder queue was written next to the source queue, LLM-only, no route_reason tag
    remainder = q.with_name(q.stem + "_remainder.json")
    assert remainder.exists()
    data = json.loads(remainder.read_text(encoding="utf-8"))
    assert [e["source_id"] for e in data] == ["fed_novel_api"]
    assert all("route_reason" not in e for e in data)


# --------------------------------------------------------------- plan smoke (#5)
def test_run_plan_prints_split(tmp_path, monkeypatch, capsys):
    q = tmp_path / "q.json"
    q.write_text(json.dumps(SAMPLE_QUEUE), encoding="utf-8")
    monkeypatch.setattr(pour, "known_spec_ids", lambda *a, **k: {"fed_cms_facility_affiliation"})

    args = types.SimpleNamespace(action="plan", queue=str(q), run=False, interval=5, once=False)
    rc = pour.run(args)

    out = capsys.readouterr().out
    assert rc == 0
    assert "DETERMINISTIC: 3" in out
    assert "LLM AGENT: 1" in out


# --------------------------------------------------------------- watch degrade
def test_watch_once_no_pour(monkeypatch, capsys):
    monkeypatch.setattr(pour.C, "pour_running", lambda: None)
    monkeypatch.setattr(pour, "read_onboard_log", lambda: {})
    monkeypatch.setattr(pour, "read_pour_log_text", lambda: "")
    monkeypatch.setattr(pour, "last_failures_from_db", lambda *a, **k: [])

    args = types.SimpleNamespace(action="watch", queue=None, run=False, interval=5, once=True)
    rc = pour.run(args)

    out = capsys.readouterr().out
    assert rc == 0
    assert "no pour running" in out
