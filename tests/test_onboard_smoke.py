"""Pour-path safety-net tests (offline).

Guards the two batch-resilience/config behaviors the pour depends on, WITHOUT the
LLM or Snowflake. Driven by patching the settings singleton directly -- NOT env
vars, because config.py's load_dotenv(override=True) + a blank .env line would
clobber an env override.
"""
from __future__ import annotations

import sys
from pathlib import Path

_LIB = Path(__file__).resolve().parents[1] / "library-onboarding"
sys.path.insert(0, str(_LIB))

import config  # noqa: E402
import ingest  # noqa: E402
import onboard  # noqa: E402
import recon  # noqa: E402


def test_blank_model_coalesces_to_default(monkeypatch):
    """A present-but-blank ANTHROPIC_MODEL must fall back to the default, never ''."""
    monkeypatch.setenv("ANTHROPIC_MODEL", "")
    assert config.Config().anthropic_model == "claude-sonnet-4-6"
    monkeypatch.setenv("ANTHROPIC_MODEL", "claude-opus-4-8")
    assert config.Config().anthropic_model == "claude-opus-4-8"


def test_batch_continues_past_a_crashing_source(monkeypatch, tmp_path):
    """One source raising an uncaught error must NOT kill the whole pour (B5)."""
    srcs = [{"name": f"S{i}", "url": f"http://x/{i}"} for i in range(3)]
    monkeypatch.setattr(onboard, "SOURCES", srcs)
    monkeypatch.setattr(onboard, "LOG_PATH", tmp_path / "log.json")
    monkeypatch.setattr(onboard.settings, "auto_approve", True)  # bypass the TTY gate

    seen = []

    def fake_onboard(source, position=None):
        seen.append(source["name"])
        if source["name"] == "S1":
            raise RuntimeError("boom")
        return {"status": "complete", "source_id": source["name"]}

    monkeypatch.setattr(onboard, "onboard_source", fake_onboard)
    rc = onboard.run_batch()

    assert rc == 0
    assert seen == ["S0", "S1", "S2"]  # did not stop at the crash
    log = onboard.load_log()
    assert log["S0"]["status"] == "complete"
    assert log["S1"]["status"] == "failed"
    assert log["S2"]["status"] == "complete"


def test_batch_halts_on_human_abort(monkeypatch, tmp_path):
    """A real foreman abort inside a stage still stops the batch (resume later)."""
    srcs = [{"name": f"S{i}", "url": f"http://x/{i}"} for i in range(3)]
    monkeypatch.setattr(onboard, "SOURCES", srcs)
    monkeypatch.setattr(onboard, "LOG_PATH", tmp_path / "log.json")
    monkeypatch.setattr(onboard.settings, "auto_approve", True)

    def fake_onboard(source, position=None):
        return {"status": "aborted"} if source["name"] == "S1" else {"status": "complete"}

    monkeypatch.setattr(onboard, "onboard_source", fake_onboard)
    onboard.run_batch()
    log = onboard.load_log()
    assert "S2" not in log  # stopped at the abort, did not process S2


def test_auto_repair_exhaustion_is_failed_not_abort(monkeypatch):
    """Unattended auto-repair giving up returns FAILED (skip source), not ABORT."""
    monkeypatch.setattr(onboard.settings, "auto_approve", True)
    monkeypatch.setattr(onboard.settings, "auto_repair", 1)

    def always_raises(_fb):
        raise RuntimeError("nope")

    action, artifact = onboard._run_stage(always_raises, lambda a: None)
    assert action == onboard.FAILED
    assert artifact is None


def test_oom_guard_upgrades_large_snapshot_to_chunked():
    """A large/unknown snapshot fails toward chunked streaming; small stays snapshot;
    a foreman pin is respected."""
    src = {"name": "Big", "url": "http://x", "layer": "us_federal", "identifiers": []}
    assert recon._resolve(src, {"volume": "~50 million rows", "load_mode": "snapshot"}, None)["load_mode"] == "chunked"
    assert recon._resolve(src, {"volume": "unknown"}, None)["load_mode"] == "snapshot"  # unknown stays snapshot
    assert recon._resolve(src, {"volume": "500 rows"}, None)["load_mode"] == "snapshot"
    pinned = {**src, "load_mode": "snapshot"}
    assert recon._resolve(pinned, {"volume": "50 million"}, None)["load_mode"] == "snapshot"
    assert recon._resolve(src, {"volume": "50 million", "load_mode": "incremental"}, None)["load_mode"] == "incremental"


def test_quarantine_skips_a_source_at_max_attempts(monkeypatch, tmp_path):
    """A source that already failed max_attempts times is skipped (not re-attempted)."""
    srcs = [{"name": "Dead", "url": "http://x/dead"}, {"name": "Live", "url": "http://x/live"}]
    monkeypatch.setattr(onboard, "SOURCES", srcs)
    logp = tmp_path / "log.json"
    logp.write_text('{"Dead": {"status": "failed", "attempts": 3}}', encoding="utf-8")
    monkeypatch.setattr(onboard, "LOG_PATH", logp)
    monkeypatch.setattr(onboard.settings, "auto_approve", True)
    monkeypatch.setattr(onboard.settings, "max_attempts", 3)

    seen = []

    def fake_onboard(source, position=None):
        seen.append(source["name"])
        return {"status": "complete"}

    monkeypatch.setattr(onboard, "onboard_source", fake_onboard)
    onboard.run_batch()
    assert seen == ["Live"]  # Dead was quarantined, never re-attempted


def test_stringify_blanks_null_string_tokens():
    """A loader's df.astype(str) turns nulls into 'nan'/'None'/'<NA>' text; those must
    land as '' (not corrupt data / defeat the density gate)."""
    import pandas as pd
    df = pd.DataFrame({"a": ["nan", "NaN", "real", "None", "<NA>"], "b": list("12345")})
    out = ingest._stringify(df.copy())
    assert out["A"].tolist() == ["", "", "real", "", ""]


def test_stringify_column_level_int_no_mixed_format():
    """Integer-like float column -> all ints (join keys survive); a genuine decimal
    column keeps decimals (no mixed '2'/'2.5')."""
    import pandas as pd
    df = pd.DataFrame({"key": [1001.0, 2002.0, None], "measure": [2.0, 2.5, None]})
    out = ingest._stringify(df.copy())
    assert out["KEY"].tolist() == ["1001", "2002", ""]
    assert out["MEASURE"].tolist() == ["2.0", "2.5", ""]


def test_dedupe_cols_are_unique_even_with_existing_suffix():
    for cols in (["a", "a", "a_2"], ["Name", "name", "NAME", "name_2"]):
        out = ingest._dedupe_cols(cols)
        assert len(set(out)) == len(out), out


def test_density_flags_all_null_token_frame_empty():
    """An all-'nan'-text frame (the astype(str) failure class) is demoted to empty."""
    import pandas as pd
    df = pd.DataFrame({"a": ["nan", "nan", "nan"], "b": ["NaN", "None", "<NA>"]})
    d = ingest.assess_density(ingest._stringify(df.copy()), sample_rows=None)
    assert d["empty"] is True


def test_looks_large_only_on_positive_signal():
    assert recon._looks_large("2 million rows") is True
    assert recon._looks_large("3 GB CSV") is True
    assert recon._looks_large("1,500,000 records") is True
    assert recon._looks_large("unknown") is False   # no longer forces chunked
    assert recon._looks_large("") is False
    assert recon._looks_large("500 rows") is False


def test_batch_limit_paces_and_resumes(monkeypatch, tmp_path):
    """--limit onboards at most N not-yet-complete sources per run; a re-run resumes
    past the completed ones (the wave-pacing mechanism for the keyless pour)."""
    monkeypatch.setattr(onboard, "LOG_PATH", tmp_path / "log.json")
    monkeypatch.setattr(onboard.settings, "auto_approve", True)
    monkeypatch.setattr(onboard, "_budget_preflight", lambda: None)

    q = [{"name": f"K{i}", "url": f"http://x/{i}", "source_id": f"xc_k{i}"} for i in range(3)]
    seen = []
    monkeypatch.setattr(onboard, "onboard_source",
                        lambda source, position=None: seen.append(source["name"]) or {"status": "complete"})

    onboard.run_batch(sources=q, limit=2)          # wave 1
    assert seen == ["K0", "K1"]                     # stopped at the limit
    seen.clear()
    onboard.run_batch(sources=q, limit=2)          # wave 2 resumes
    assert seen == ["K2"]                           # K0/K1 skipped as complete
    log = onboard.load_log()
    assert len(log) == 3 and all(v["status"] == "complete" for v in log.values())


def test_load_queue_validates(tmp_path):
    """External queue must be a non-empty list of {name,url,...} with unique names."""
    import json
    import pytest

    def write(obj):
        p = tmp_path / "q.json"
        p.write_text(json.dumps(obj), encoding="utf-8")
        return str(p)

    with pytest.raises(SystemExit):
        onboard._load_queue(write([]))                                   # empty
    with pytest.raises(SystemExit):
        onboard._load_queue(write([{"name": "a"}]))                      # missing url
    with pytest.raises(SystemExit):
        onboard._load_queue(write([{"name": "a", "url": "u"},
                                   {"name": "a", "url": "u2"}]))         # dup name
    good = [{"name": "a", "url": "u"}, {"name": "b", "url": "u2"}]
    assert onboard._load_queue(write(good)) == good
    with pytest.raises(SystemExit):
        onboard._load_queue(str(tmp_path / "nope.json"))                 # missing file
