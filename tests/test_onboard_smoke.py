"""Pour-path safety-net tests (offline).

Guards the two batch-resilience/config behaviors the pour depends on, WITHOUT the
LLM or Snowflake. Driven by patching the settings singleton directly -- NOT env
vars, because config.py's load_dotenv(override=True) + a blank .env line would
clobber an env override.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

_LIB = Path(__file__).resolve().parents[1] / "library-onboarding"
sys.path.insert(0, str(_LIB))

import config  # noqa: E402
import ingest  # noqa: E402
import onboard  # noqa: E402
import recon  # noqa: E402
import scaffold_dbt  # noqa: E402


def _cfg(sid: str = "xc_test", auth: dict | None = None) -> dict:
    """Minimal recon profile shaped like _resolve's output (what the gates and
    later checkpoints actually read)."""
    return {
        "name": "Test Source",
        "url": "http://x",
        "source_id": sid,
        "landing_table": sid.upper(),
        "entity": "records",
        "staging_model": f"stg_{sid}__records",
        "mart_model": f"gov__{sid}",
        "auth": auth or {"type": "none", "env_var": "", "notes": ""},
    }


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

    assert rc == 1  # a source FAILED this run -> nonzero exit (but the pour continued)
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
    with pytest.raises(SystemExit):
        onboard._load_queue(write([{"name": "a", "url": "u", "source_id": "xc_a"},
                                   {"name": "b", "url": "u2", "source_id": "xc_a"}]))  # dup sid


# ---------------------------------------------------------------------------
# Wave 1 hardening: gates, resume semantics, exit codes, log keying
# ---------------------------------------------------------------------------
def test_empty_gate_skips_dbt_and_registry(monkeypatch):
    """A density-demoted load must NOT ride into DBT/REGISTRY as 'complete'."""
    monkeypatch.setattr(onboard.settings, "auto_approve", True)
    monkeypatch.setattr(onboard.settings, "fake_llm", True)  # bypass the SF gates
    monkeypatch.setattr(onboard, "run_recon", lambda source, feedback=None: _cfg())
    monkeypatch.setattr(onboard, "generate_ingest_script", lambda config, feedback=None: "code")
    monkeypatch.setattr(onboard, "run_ingest",
                        lambda config, code: {"empty": True, "run_id": "r1", "rows": 5,
                                              "status": "EMPTY -- all source columns blank"})
    called = []
    monkeypatch.setattr(onboard, "generate_dbt_models", lambda *a, **k: called.append("dbt"))
    monkeypatch.setattr(onboard, "register_source", lambda *a, **k: called.append("registry"))

    rec = onboard.onboard_source({"name": "T", "url": "http://x"})
    assert rec["status"] == "empty"
    assert rec["run_id"] == "r1"
    assert "blank" in rec["message"]
    assert called == []  # neither DBT nor REGISTRY ran


def test_empty_counts_toward_quarantine(monkeypatch, tmp_path):
    """'empty' retries like 'failed' and quarantines at max_attempts; empty alone
    does NOT force a nonzero exit."""
    monkeypatch.setattr(onboard, "LOG_PATH", tmp_path / "log.json")
    monkeypatch.setattr(onboard.settings, "auto_approve", True)
    monkeypatch.setattr(onboard.settings, "max_attempts", 2)
    monkeypatch.setattr(onboard, "_budget_preflight", lambda: None)
    q = [{"name": "E", "url": "http://x"}]
    seen = []
    monkeypatch.setattr(onboard, "onboard_source",
                        lambda source, position=None: seen.append(1) or {"status": "empty"})

    assert onboard.run_batch(sources=q) == 0
    assert onboard.load_log()["E"]["attempts"] == 1
    onboard.run_batch(sources=q)
    assert onboard.load_log()["E"]["attempts"] == 2
    onboard.run_batch(sources=q)  # at max_attempts now -> quarantined
    assert len(seen) == 2


def test_auth_gate_skips_before_codegen(monkeypatch):
    """Missing key -> needs_key BEFORE any codegen burn, recording the env var."""
    monkeypatch.setattr(onboard.settings, "auto_approve", True)
    monkeypatch.setattr(onboard.settings, "fake_llm", False)
    monkeypatch.setattr(onboard.settings, "snowflake_ready", lambda: False)  # writeback no-op
    cfg = _cfg(auth={"type": "free API key", "env_var": "RIPPLE_TEST_FAKE_KEY", "notes": ""})
    monkeypatch.setattr(onboard, "run_recon", lambda source, feedback=None: cfg)
    monkeypatch.delenv("RIPPLE_TEST_FAKE_KEY", raising=False)
    burned = []
    monkeypatch.setattr(onboard, "generate_ingest_script",
                        lambda *a, **k: burned.append(1) or "code")

    rec = onboard.onboard_source({"name": "K", "url": "http://x"})
    assert rec["status"] == "needs_key"
    assert rec["needs_env_var"] == "RIPPLE_TEST_FAKE_KEY"
    assert burned == []

    # Key present -> the gate passes and the flow proceeds to SCRIPT.
    monkeypatch.setenv("RIPPLE_TEST_FAKE_KEY", "sekrit")
    monkeypatch.setattr(onboard, "run_ingest",
                        lambda config, code: {"rows": 0, "run_id": "r", "status": "ok"})
    monkeypatch.setattr(onboard, "SKIP_DBT", True)
    monkeypatch.setattr(onboard, "register_source", lambda config: {"ok": True})
    rec = onboard.onboard_source({"name": "K", "url": "http://x"})
    assert rec["status"] == "complete"
    assert burned == [1]


def test_needs_key_resume_retries_only_when_key_present(monkeypatch, tmp_path):
    logp = tmp_path / "log.json"
    logp.write_text(json.dumps(
        {"K": {"status": "needs_key", "needs_env_var": "RIPPLE_TEST_FAKE_KEY"}}),
        encoding="utf-8")
    monkeypatch.setattr(onboard, "LOG_PATH", logp)
    monkeypatch.setattr(onboard.settings, "auto_approve", True)
    monkeypatch.setattr(onboard, "_budget_preflight", lambda: None)
    seen = []
    monkeypatch.setattr(onboard, "onboard_source",
                        lambda source, position=None: seen.append(source["name"]) or {"status": "complete"})
    q = [{"name": "K", "url": "http://x"}]

    monkeypatch.delenv("RIPPLE_TEST_FAKE_KEY", raising=False)
    assert onboard.run_batch(sources=q) == 0  # needs_key does NOT force nonzero
    assert seen == []                          # key absent -> still skipped

    monkeypatch.setenv("RIPPLE_TEST_FAKE_KEY", "sekrit")
    onboard.run_batch(sources=q)
    assert seen == ["K"]                       # key present -> retried


class _FakeCur:
    def __init__(self, rows=None):
        self._rows = rows or []
    def execute(self, *a, **k):
        pass
    def fetchall(self):
        return self._rows
    def close(self):
        pass


class _FakeConn:
    def __init__(self, rows=None):
        self._rows = rows
    def cursor(self):
        return _FakeCur(self._rows)
    def close(self):
        pass


def test_collision_gate_skips_landed_sid_and_include_landed_escapes(monkeypatch):
    monkeypatch.setattr(onboard.settings, "auto_approve", True)
    monkeypatch.setattr(onboard.settings, "fake_llm", False)
    monkeypatch.setattr(onboard.settings, "snowflake_ready", lambda: True)
    monkeypatch.setattr(onboard, "run_recon", lambda source, feedback=None: _cfg("fed_dupe_data"))
    monkeypatch.setattr(onboard.snow, "connect", lambda: _FakeConn())
    monkeypatch.setattr(onboard.snow, "fetch_scalar", lambda conn, sql, params=None: 1)
    scripted = []
    monkeypatch.setattr(onboard, "generate_ingest_script",
                        lambda *a, **k: scripted.append(1) or "code")

    rec = onboard.onboard_source({"name": "D", "url": "http://x"})
    assert rec["status"] == "already_cataloged"
    assert rec["source_id"] == "fed_dupe_data"
    assert scripted == []  # skipped BEFORE SCRIPT

    # --include-landed escape: the gate stands down for a deliberate re-land.
    monkeypatch.setattr(onboard, "INCLUDE_LANDED", True)
    monkeypatch.setattr(onboard, "run_ingest",
                        lambda config, code: {"rows": 0, "run_id": "r", "status": "ok"})
    monkeypatch.setattr(onboard, "SKIP_DBT", True)
    monkeypatch.setattr(onboard, "register_source", lambda config: {"ok": True})
    rec = onboard.onboard_source({"name": "D", "url": "http://x"})
    assert rec["status"] == "complete"


def test_collision_gate_is_non_raising(monkeypatch):
    """A broken collision check must let the source PROCEED, not crash the pour."""
    monkeypatch.setattr(onboard.settings, "fake_llm", False)
    monkeypatch.setattr(onboard.settings, "snowflake_ready", lambda: True)
    def _boom():
        raise RuntimeError("warehouse offline")
    monkeypatch.setattr(onboard.snow, "connect", _boom)
    assert onboard._collision_gate({"name": "X"}, _cfg("xc_x")) is None


def test_already_cataloged_is_terminal_on_resume(monkeypatch, tmp_path):
    logp = tmp_path / "log.json"
    logp.write_text(json.dumps({"A": {"status": "already_cataloged"}}), encoding="utf-8")
    monkeypatch.setattr(onboard, "LOG_PATH", logp)
    monkeypatch.setattr(onboard.settings, "auto_approve", True)
    monkeypatch.setattr(onboard, "_budget_preflight", lambda: None)
    seen = []
    monkeypatch.setattr(onboard, "onboard_source",
                        lambda source, position=None: seen.append(1) or {"status": "complete"})
    onboard.run_batch(sources=[{"name": "A", "url": "http://x"}])
    assert seen == []  # never re-attempted


def test_exit_code_reflects_this_run_only(monkeypatch, tmp_path):
    """Old failures in the shared log (skipped this run) must not poison the rc."""
    logp = tmp_path / "log.json"
    logp.write_text(json.dumps({"Old": {"status": "failed", "attempts": 9}}), encoding="utf-8")
    monkeypatch.setattr(onboard, "LOG_PATH", logp)
    monkeypatch.setattr(onboard.settings, "auto_approve", True)
    monkeypatch.setattr(onboard.settings, "max_attempts", 3)
    monkeypatch.setattr(onboard, "_budget_preflight", lambda: None)
    q = [{"name": "Old", "url": "http://x"}, {"name": "New", "url": "http://y"}]

    monkeypatch.setattr(onboard, "onboard_source",
                        lambda source, position=None: {"status": "complete"})
    assert onboard.run_batch(sources=q) == 0  # Old quarantined, New complete -> 0

    # needs_key + empty this run -> still 0 (actionable outcomes, not breakage)
    (tmp_path / "log.json").write_text("{}", encoding="utf-8")
    outcomes = iter([{"status": "needs_key", "needs_env_var": "X_KEY"}, {"status": "empty"}])
    monkeypatch.setattr(onboard, "onboard_source",
                        lambda source, position=None: next(outcomes))
    assert onboard.run_batch(sources=q) == 0

    # a real failure this run -> 1
    (tmp_path / "log.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(onboard, "onboard_source",
                        lambda source, position=None: {"status": "failed"})
    assert onboard.run_batch(sources=q) == 1


def test_failed_record_carries_truncated_error_text(monkeypatch):
    monkeypatch.setattr(onboard.settings, "auto_approve", True)
    monkeypatch.setattr(onboard.settings, "auto_repair", 0)
    def boom(source, feedback=None):
        raise RuntimeError("recon exploded: " + "x" * 600)
    monkeypatch.setattr(onboard, "run_recon", boom)
    rec = onboard.onboard_source({"name": "B", "url": "http://x"})
    assert rec["status"] == "failed"
    assert rec["error"].startswith("recon exploded")
    assert len(rec["error"]) <= 500


def test_safe_env_blocklist_is_anchored(monkeypatch):
    """Platform creds stripped; PATH/DBT_PROJECT_PATH/data tokens survive."""
    for k in ("SNOWFLAKE_PAT", "ANTHROPIC_API_KEY", "GH_TOKEN", "GITHUB_TOKEN",
              "AWS_ACCESS_KEY_ID", "MY_APP_PASSWORD", "CLIENT_SECRET_KEY"):
        monkeypatch.setenv(k, "s3cret")
    monkeypatch.setenv("COURTLISTENER_TOKEN", "data-key")
    monkeypatch.setenv("DBT_PROJECT_PATH", "c:/somewhere")

    env = ingest._safe_env()
    assert "PATH" in env                    # '_PAT' suffix match must NOT strip PATH
    assert "DBT_PROJECT_PATH" in env
    assert "COURTLISTENER_TOKEN" in env     # _TOKEN is a data key, stays allowed
    for k in ("SNOWFLAKE_PAT", "ANTHROPIC_API_KEY", "GH_TOKEN", "GITHUB_TOKEN",
              "AWS_ACCESS_KEY_ID", "MY_APP_PASSWORD", "CLIENT_SECRET_KEY"):
        assert k not in env, k


def test_codegen_fence_retry_then_success(monkeypatch):
    """No fence -> ONE re-ask demanding a fenced block; second answer is used."""
    calls = []
    answers = [
        "Sure! Here's an outline of what I'd do...",  # chatty, no fence
        "```python\nimport pandas as pd\n\ndef fetch_data(context):\n    return pd.DataFrame()\n```",
    ]
    def fake_call(user, system="", kind="", fake_context=None, max_tokens=0):
        calls.append({"user": user, "max_tokens": max_tokens})
        return answers[len(calls) - 1]
    monkeypatch.setattr(ingest, "call_claude", fake_call)

    code = ingest.generate_ingest_script({"name": "X", "url": "http://x"})
    assert "def fetch_data" in code
    assert len(calls) == 2
    assert "Return ONLY a fenced python code block." in calls[1]["user"]
    assert calls[0]["max_tokens"] == 8192  # truncation headroom bump


def test_codegen_syntax_error_fails_at_script_time(monkeypatch):
    """Truncated/garbled code raises HERE (feeding auto-repair), not at LOAD."""
    bad = "```python\ndef fetch_data(context:\n    return None\n```"
    monkeypatch.setattr(ingest, "call_claude",
                        lambda user, system="", kind="", fake_context=None, max_tokens=0: bad)
    with pytest.raises(RuntimeError, match="does not compile"):
        ingest.generate_ingest_script({"name": "X", "url": "http://x"})


def test_watermark_orderable():
    assert ingest._watermark_orderable("2024-01-02") is True
    assert ingest._watermark_orderable("2024-01-02T10:00:00Z") is True
    assert ingest._watermark_orderable("1717171717") is True       # epoch
    assert ingest._watermark_orderable("1717171717.5") is True
    assert ingest._watermark_orderable("07/01/2024") is False       # MM/DD/YYYY
    assert ingest._watermark_orderable("13-JAN-2024") is False
    assert ingest._watermark_orderable("") is False


def test_run_ingest_rejects_non_iso_watermark(monkeypatch):
    """A lexicographically-wrong TEXT watermark must fail LOUDLY, not mis-append."""
    monkeypatch.setattr(ingest.settings, "fake_llm", False)
    monkeypatch.setattr(ingest.settings, "snowflake_ready", lambda: True)
    monkeypatch.setattr(ingest.snow, "connect", lambda: _FakeConn())
    monkeypatch.setattr(ingest, "_watermark", lambda conn, table, cursor_field: "07/01/2024")
    cfg = {"source_id": "xc_t", "landing_table": "XC_T", "url": "http://x",
           "load_mode": "incremental", "cursor_field": "date"}
    with pytest.raises(RuntimeError, match="ISO-orderable"):
        ingest.run_ingest(cfg, "def fetch_data(context):\n    return None")


def test_save_log_atomic_and_corrupt_load_fails_loudly(monkeypatch, tmp_path):
    logp = tmp_path / "log.json"
    monkeypatch.setattr(onboard, "LOG_PATH", logp)

    onboard.save_log({"a": {"status": "complete"}})
    assert json.loads(logp.read_text(encoding="utf-8")) == {"a": {"status": "complete"}}
    assert not list(tmp_path.glob("*.tmp"))  # temp file replaced, not left behind

    logp.write_text("{this is not json", encoding="utf-8")
    with pytest.raises(RuntimeError, match="corrupt"):
        onboard.load_log()
    assert not logp.exists()                          # moved aside, not deleted
    assert (tmp_path / "log.json.corrupt").exists()   # evidence preserved


def test_log_keys_on_pinned_sid_with_name_fallback_and_carryover(monkeypatch, tmp_path):
    """New entries key on the queue-pinned sid; a legacy name-keyed entry still
    drives resume decisions and its attempts carry over to the sid key."""
    logp = tmp_path / "log.json"
    logp.write_text(json.dumps({"Foo Portal": {"status": "failed", "attempts": 2}}),
                    encoding="utf-8")
    monkeypatch.setattr(onboard, "LOG_PATH", logp)
    monkeypatch.setattr(onboard.settings, "auto_approve", True)
    monkeypatch.setattr(onboard.settings, "max_attempts", 5)
    monkeypatch.setattr(onboard, "_budget_preflight", lambda: None)
    q = [{"name": "Foo Portal", "url": "http://x", "source_id": "xc_foo"}]

    monkeypatch.setattr(onboard, "onboard_source",
                        lambda source, position=None: {"status": "failed"})
    onboard.run_batch(sources=q)
    log = onboard.load_log()
    assert log["xc_foo"]["attempts"] == 3        # carried over from the name key
    assert log["Foo Portal"]["attempts"] == 2    # legacy entry left untouched

    # Next run must read the sid-keyed entry (attempts=3 >= max 3 -> quarantined).
    monkeypatch.setattr(onboard.settings, "max_attempts", 3)
    seen = []
    monkeypatch.setattr(onboard, "onboard_source",
                        lambda source, position=None: seen.append(1) or {"status": "complete"})
    onboard.run_batch(sources=q)
    assert seen == []


def test_resolve_carries_auth_env_var():
    src = {"name": "X", "url": "http://x", "layer": "us_federal", "identifiers": []}
    out = recon._resolve(
        src, {"auth": {"type": "free API key", "env_var": "CENSUS_API_KEY", "notes": "n"}}, None)
    assert out["auth"]["env_var"] == "CENSUS_API_KEY"
    # Old recon outputs (no env_var) keep working -- the gate sees "" and passes.
    out = recon._resolve(src, {"auth": {"type": "free API key", "notes": "n"}}, None)
    assert out["auth"]["env_var"] == ""


def test_browser_https_errors_default_off(monkeypatch):
    """Evidence platform: untrusted TLS is opt-in, never the default."""
    monkeypatch.delenv("ONBOARD_BROWSER_IGNORE_HTTPS_ERRORS", raising=False)
    assert config.Config().browser_ignore_https_errors is False
    monkeypatch.setenv("ONBOARD_BROWSER_IGNORE_HTTPS_ERRORS", "1")
    assert config.Config().browser_ignore_https_errors is True


def test_fake_llm_dbt_writes_go_to_temp(monkeypatch, tmp_path):
    """FAKE_LLM can never scaffold into the real dbt project (env guards can't
    protect it -- .env sets DBT_PROJECT_PATH with override=True)."""
    import tempfile
    monkeypatch.setattr(scaffold_dbt.settings, "fake_llm", True)
    monkeypatch.setattr(scaffold_dbt.settings, "dbt_project_path", str(tmp_path / "real_dbt"))
    models = {"staging_sql": "select 1", "intermediate_sql": "",
              "mart_sql": "select 1", "schema_yml": "version: 2"}

    out = scaffold_dbt.write_dbt_models(_cfg("xc_fake_demo"), models)
    temp_root = str(Path(tempfile.gettempdir()) / "ripple_fake_dbt")
    assert out["written"], "fake mode should still exercise the file writes"
    assert all(p.startswith(temp_root) for p in out["written"]), out["written"]
    assert not (tmp_path / "real_dbt").exists()  # the real project was never touched
