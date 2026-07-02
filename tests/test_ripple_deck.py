"""Offline unit tests for ripple/deck.py -- the Morning Deck.

Everything here is pure: no live Snowflake, no disk beyond tmp_path. We pin the
helpers that carry the load:
  - parse_pour_tally  : onboarding_log dict -> header counts (done/failed/need-keys)
  - pour_position     : last '[N of TOTAL]' marker out of a pour log's text
  - freshness_rollup  : V_SOURCE_FRESHNESS rows -> state counts (all keys present)
  - worst_rotting     : overdue+stale, worst DATA_AGE_DAYS first, limited
  - since_diff        : prev vs cur snapshot -> newly landed/failed + metric deltas
  - leads_active_total: sum of leads.<rule>.active out of a V_STATE dict
  - _build_json       : the --json shape has the sections it promises
  - run(--json)       : end to end with a stubbed connect() (Snowflake never touched)
"""
import json

from ripple import deck as DK


# =========================================================================== #
# parse_pour_tally
# =========================================================================== #
def test_pour_tally_buckets_all_statuses():
    log = {
        "A": {"status": "complete"},
        "B": {"status": "complete"},
        "C": {"status": "failed"},
        "D": {"status": "needs_key"},
        "E": {"status": "empty"},
        "F": {"status": "already_cataloged"},
        "G": {"status": "weird_new_status"},
    }
    t = DK.parse_pour_tally(log)
    assert t["done"] == 3          # complete + complete + already_cataloged
    assert t["failed"] == 1
    assert t["need_keys"] == 1
    assert t["empty"] == 1
    assert t["other"] == 1
    assert t["total"] == 7


def test_pour_tally_empty_is_all_zero():
    t = DK.parse_pour_tally({})
    assert t == {"done": 0, "failed": 0, "need_keys": 0, "empty": 0, "other": 0, "total": 0}


def test_pour_tally_survives_junk_entries():
    t = DK.parse_pour_tally({"X": None, "Y": {}})
    assert t["total"] == 2
    assert t["other"] == 2


# =========================================================================== #
# pour_position
# =========================================================================== #
def test_pour_position_takes_the_last_marker():
    text = "banner\nCHECKPOINT [1 of 720]\nstuff\nCHECKPOINT [72 of 720]\n"
    assert DK.pour_position(text) == (72, 720)


def test_pour_position_none_when_absent():
    assert DK.pour_position("no markers here") is None
    assert DK.pour_position("") is None


# =========================================================================== #
# freshness_rollup / worst_rotting
# =========================================================================== #
def _fr(sid, state, age, cadence="weekly"):
    return {"SOURCE_ID": sid, "FRESHNESS_STATE": state,
            "DATA_AGE_DAYS": age, "CADENCE_BUCKET": cadence}


def test_freshness_rollup_counts_and_keeps_all_keys():
    rows = [_fr("a", "fresh", 1), _fr("b", "stale", 400),
            _fr("c", "stale", 90), _fr("d", "overdue", 30), _fr("e", "unknown", None)]
    roll = DK.freshness_rollup(rows)
    assert roll["fresh"] == 1
    assert roll["stale"] == 2
    assert roll["overdue"] == 1
    assert roll["unknown"] == 1
    # dead/due always present even at zero, so the rollup line never has a hole
    assert roll["dead"] == 0
    assert roll["due"] == 0


def test_freshness_rollup_empty():
    roll = DK.freshness_rollup([])
    assert set(roll) == {"fresh", "due", "overdue", "stale", "dead", "unknown"}
    assert sum(roll.values()) == 0


def test_worst_rotting_orders_by_age_and_limits():
    rows = [_fr("young", "overdue", 10), _fr("ancient", "stale", 900),
            _fr("mid", "stale", 100), _fr("fresh", "fresh", 1)]
    rot = DK.worst_rotting(rows, limit=2)
    assert [r["SOURCE_ID"] for r in rot] == ["ancient", "mid"]
    # 'fresh' is never rotting; only overdue+stale qualify
    all_rot = DK.worst_rotting(rows, limit=None)
    assert [r["SOURCE_ID"] for r in all_rot] == ["ancient", "mid", "young"]


def test_worst_rotting_handles_missing_age():
    rows = [_fr("a", "stale", None), _fr("b", "overdue", 5)]
    rot = DK.worst_rotting(rows, limit=None)
    # None age sorts as 0 -> ends last; no crash
    assert [r["SOURCE_ID"] for r in rot] == ["b", "a"]


# =========================================================================== #
# since_diff
# =========================================================================== #
def test_since_diff_first_run():
    d = DK.since_diff({}, {"metrics": {}, "success_ids": ["x"]})
    assert d["first_run"] is True
    assert d["newly_landed"] == []


def test_since_diff_detects_new_landed_failed_and_deltas():
    prev = {"metrics": {"taps.landed": "100", "connect.edges": "50"},
            "success_ids": ["a", "b"], "failed_ids": ["z"]}
    cur = {"metrics": {"taps.landed": "103", "connect.edges": "50"},
           "success_ids": ["a", "b", "c", "d"], "failed_ids": ["z", "y"]}
    d = DK.since_diff(prev, cur)
    assert d["first_run"] is False
    assert d["newly_landed"] == ["c", "d"]
    assert d["newly_failed"] == ["y"]
    assert d["deltas"]["taps.landed"] == 3
    # unchanged metric doesn't appear
    assert "connect.edges" not in d["deltas"]


def test_since_diff_no_change_is_empty():
    snap = {"metrics": {"taps.landed": "5"}, "success_ids": ["a"], "failed_ids": []}
    d = DK.since_diff(snap, snap)
    assert d["newly_landed"] == []
    assert d["newly_failed"] == []
    assert d["deltas"] == {}


# =========================================================================== #
# leads_active_total
# =========================================================================== #
def test_leads_active_total_sums_per_rule():
    vs = {"leads.banned_but_operating.active": "10",
          "leads.debarred_but_funded.active": "5",
          "leads.foo.other": "99",          # not .active -> ignored
          "taps.landed": "100"}             # not a leads metric -> ignored
    assert DK.leads_active_total(vs) == 15


def test_leads_active_total_empty():
    assert DK.leads_active_total({}) == 0


# =========================================================================== #
# _build_json shape
# =========================================================================== #
def test_build_json_has_all_sections():
    vs = {"taps.landed": "10", "landing.tables": "5"}
    fresh = [_fr("a", "stale", 300)]
    q = {"leads_pending": 3, "review_queue": 661, "unclassified": 0}
    diff = {"first_run": False, "newly_landed": ["x"], "newly_failed": [], "deltas": {}}
    budget = {"quota": 300, "used": 30, "headroom": 240, "suspend_at": 270}
    health = {"pat_msg": "good", "pat_ok": True, "dead": 0}
    d = DK._build_json("onboard.py --batch", DK.parse_pour_tally({"A": {"status": "complete"}}),
                       (72, 720), vs, fresh, q, diff, budget, health)
    for key in ("generated_at", "pour", "scale", "freshness", "queues", "since", "budget", "health"):
        assert key in d
    assert d["pour"]["position"] == [72, 720]
    assert d["scale"]["taps.landed"] == "10"
    assert d["freshness"]["rollup"]["stale"] == 1
    assert d["queues"]["review_queue"] == 661
    # round-trips through json cleanly
    assert json.loads(json.dumps(d, default=str))


def test_build_json_pour_null_when_no_pour():
    d = DK._build_json(None, DK.parse_pour_tally({}), None, {}, [], {}, {}, None, {})
    assert d["pour"] is None


# =========================================================================== #
# _fmt_pour_header
# =========================================================================== #
def test_fmt_pour_header_uses_position_and_tally():
    tally = {"done": 39, "failed": 29, "need_keys": 4, "empty": 0, "other": 0, "total": 72}
    line = DK._fmt_pour_header("onboard.py --batch", tally, (72, 720))
    assert "POUR LIVE: 72/720" in line
    assert "39 done" in line
    assert "29 failed" in line
    assert "4 need-keys" in line


# =========================================================================== #
# run(--json) end to end with a stubbed connection (Snowflake never touched)
# =========================================================================== #
# Column headers per query so C.dicts() builds the right keys (it reads cur.description).
_COLS = {
    "V_SOURCE_FRESHNESS": ["SOURCE_ID", "FRESHNESS_STATE", "DATA_AGE_DAYS", "CADENCE_BUCKET"],
    "INGEST_RUNS": ["SOURCE_ID", "STATUS"],
}


class _FakeCur:
    def __init__(self, answers):
        self._answers = answers
        self._last = None
        self.description = [("C",)]

    def execute(self, sql, params=None):
        self._last = sql
        for needle, cols in _COLS.items():
            if needle in sql:
                self.description = [(c,) for c in cols]
                break
        else:
            self.description = [("C",)]
        return self

    def fetchall(self):
        for needle, rows in self._answers.items():
            if needle in self._last:
                return rows
        return []

    def close(self):
        pass


class _FakeConn:
    def __init__(self, answers):
        self._answers = answers

    def cursor(self):
        return _FakeCur(self._answers)

    def close(self):
        pass


class _Args:
    json = True
    full = False


def test_run_json_smoke_with_stubbed_conn(monkeypatch, tmp_path, capsys):
    # Point the state file at tmp so we don't touch the real one, and so it's a first run.
    state_file = tmp_path / "_ripple_state.json"
    monkeypatch.setattr(DK.C, "STATE_PATH", state_file, raising=False)
    monkeypatch.setattr(DK.C, "load_state", lambda: {}, raising=False)
    saved = {}
    monkeypatch.setattr(DK.C, "save_state", lambda d: saved.update(d), raising=False)

    # No live pour; no pour logs found.
    monkeypatch.setattr(DK.C, "pour_running", lambda: None)
    monkeypatch.setattr(DK, "_newest_pour_log", lambda: None)
    monkeypatch.setattr(DK, "_read_json", lambda p: {})

    answers = {
        "V_STATE": [("taps.landed", "76"), ("landing.tables", "101"),
                    ("leads.banned_but_operating.active", "12")],
        "V_SOURCE_FRESHNESS": [("s1", "stale", 300, "weekly")],
        "DECISIONS": [(0,)],
        "V_REVIEW_QUEUE": [(661,)],
        "CATALOG": [(0,)],
        "INGEST_RUNS": [],
    }
    monkeypatch.setattr(DK.C, "connect", lambda *a, **k: _FakeConn(answers))
    # Budget + PAT helpers may import loadkit; stub them so the test is hermetic.
    monkeypatch.setattr(DK, "_fetch_budget", lambda conn: None)
    monkeypatch.setattr(DK, "_fetch_health", lambda rows: {"pat_msg": None, "pat_ok": None, "dead": 0})

    rc = DK.run(_Args())
    assert rc == 0
    out = capsys.readouterr().out
    d = json.loads(out)
    assert d["scale"]["taps.landed"] == "76"
    assert d["freshness"]["rollup"]["stale"] == 1
    assert d["queues"]["review_queue"] == 661
    assert d["since"]["first_run"] is True


def test_run_json_survives_dead_snowflake(monkeypatch, capsys):
    # connect() blows up -> deck still emits valid JSON with empty sections.
    monkeypatch.setattr(DK.C, "connect", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("no net")))
    monkeypatch.setattr(DK.C, "load_state", lambda: {})
    monkeypatch.setattr(DK.C, "save_state", lambda d: None)
    monkeypatch.setattr(DK.C, "pour_running", lambda: None)
    monkeypatch.setattr(DK, "_newest_pour_log", lambda: None)
    monkeypatch.setattr(DK, "_read_json", lambda p: {})

    rc = DK.run(_Args())
    assert rc == 0
    d = json.loads(capsys.readouterr().out)
    assert d["scale"]["taps.landed"] is None
    assert d["freshness"]["rollup"]["stale"] == 0
