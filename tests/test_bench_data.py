"""bench/data.py - the DataFrame seam.

Offline only. Nothing here touches Snowflake: the warehouse path is proven by
importing the read lane and checking the call signature we rely on, plus the
guard refusal that comes back before any connection is attempted.
"""

from __future__ import annotations

import inspect
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from bench import data  # noqa: E402
from viz import sqlrun  # noqa: E402


# --------------------------------------------------------------------------- #
# isolation
# --------------------------------------------------------------------------- #
@pytest.fixture(autouse=True)
def _a_cold_cache_for_every_test():
    """`data.frame` caches. Every test here starts from an empty one.

    Not a workaround - it is the honest way to test a caching module. Two tests
    in this file deliberately hand DIFFERENT answers back for the same source
    ({"kind": "warehouse", "sql": "SELECT 1"}): one stubs a good result, the
    next stubs a dead connection. Sharing a process-wide cache between them
    would mean the second one was silently reading the first one's answer and
    asserting nothing at all.
    """
    data.invalidate()
    yield
    data.invalidate()


# --------------------------------------------------------------------------- #
# demo frames
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("name", data.demo_names())
def test_every_demo_frame_builds_and_has_rows(name):
    df, meta = data.frame({"kind": "demo", "name": name})
    assert meta["ok"] is True
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0, f"{name} produced an empty frame"
    assert meta["rows"] == len(df)
    assert meta["lane"] == "demo"
    assert meta["truncated"] is False
    assert meta["as_of"] is None
    assert meta["notes"], "every demo frame should say it is fake data"


def test_demo_frames_are_reproducible_from_a_cold_cache():
    """Same slug, same numbers - a chart that jitters under your hands is unusable."""
    data.clear_demo_cache()
    first, _ = data.frame({"kind": "demo", "name": "scatter"})
    data.clear_demo_cache()
    second, _ = data.frame({"kind": "demo", "name": "scatter"})
    assert first.equals(second)


def test_editing_a_returned_frame_cannot_poison_the_cache():
    df, _ = data.frame({"kind": "demo", "name": "category"})
    df.loc[0, "spend"] = -999.0
    again, _ = data.frame({"kind": "demo", "name": "category"})
    assert again.loc[0, "spend"] != -999.0


def test_demo_catalogue_describes_shape_and_columns():
    cat = data.demo_catalogue()
    assert len(cat) == len(data.DEMO)
    for entry in cat:
        assert entry["shape"], f"{entry['name']} has no shape sentence"
        assert entry["columns"]
        assert entry["roles_line"].startswith("this result has")


def test_geojson_demo_carries_its_polygons_on_meta():
    df, meta = data.frame({"kind": "demo", "name": "geojson_zones"})
    assert "geojson" in meta
    assert meta["geojson"]["type"] == "FeatureCollection"
    assert len(meta["geojson"]["features"]) == len(df)


# --------------------------------------------------------------------------- #
# failure paths - errors are return values, never exceptions
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("source", [
    {"kind": "demo", "name": "does_not_exist"},
    {"kind": "sideways"},
    {},
    {"kind": "warehouse", "sql": "   "},
    "not a dict",
    None,
])
def test_bad_sources_return_an_error_instead_of_raising(source):
    df, meta = data.frame(source)
    assert meta["ok"] is False
    assert meta["error"]
    assert meta["rows"] == 0
    assert df.empty


def test_unknown_demo_name_lists_the_real_ones():
    _df, meta = data.frame({"kind": "demo", "name": "nope"})
    assert "category" in meta["error"] and "timeseries" in meta["error"]


def test_guard_refusal_comes_back_with_the_lanes_own_reason():
    """A write statement is refused by viz.guard before any connection opens."""
    _df, meta = data.frame({"kind": "warehouse", "sql": "DROP TABLE x"})
    assert meta["ok"] is False
    assert meta["lane"] == "refused"
    assert "DROP" in meta["error"]


def test_claim_table_read_is_refused_and_points_at_the_safe_view():
    """The libel firewall reaches ad-hoc SQL. The Bench never passes
    unsafe_claims, so a raw claim read has no way through."""
    _df, meta = data.frame({
        "kind": "warehouse",
        "sql": 'SELECT * FROM LIBRARY_META."CONNECT".LEADS',
    })
    assert meta["ok"] is False
    assert "V_LEADS_PUBLISHED" in meta["error"]


# --------------------------------------------------------------------------- #
# the warehouse lane is called, not reimplemented
# --------------------------------------------------------------------------- #
def test_we_call_sqlrun_run_the_way_it_is_actually_declared():
    sig = inspect.signature(sqlrun.run)
    assert list(sig.parameters)[:2] == ["sql", "limit_rows"]
    assert sig.parameters["unsafe_claims"].default is False


def test_warehouse_path_passes_sql_and_limit_straight_through(monkeypatch):
    """No guard is re-implemented here: sqlrun gets the SQL untouched, and its
    meta comes back with our labels added, never its values overwritten."""
    seen = {}

    def fake_run(sql, limit_rows=sqlrun.DEFAULT_LIMIT_ROWS):
        seen["sql"] = sql
        seen["limit_rows"] = limit_rows
        return (
            pd.DataFrame({"STATE": ["CA", "TX"], "TOTAL": [3, 4]}),
            {"rows": 2, "truncated": True, "elapsed_s": 0.42, "warehouse": "SERVE_WH",
             "lane": "enforced", "as_of": "2026-08-01 00:00:00", "budget": "x",
             "claim_refs": []},
        )

    monkeypatch.setattr(sqlrun, "run", fake_run)
    monkeypatch.setattr(sqlrun, "lane_status", lambda: {"lane": "enforced", "notes": []})

    df, meta = data.frame({"kind": "warehouse", "sql": "SELECT 1", "limit_rows": 55})
    assert seen == {"sql": "SELECT 1", "limit_rows": 55}
    assert meta["ok"] is True and meta["kind"] == "warehouse"
    # sqlrun's own numbers survive verbatim
    assert meta["rows"] == 2 and meta["elapsed_s"] == 0.42
    assert meta["lane"] == "enforced" and meta["as_of"] == "2026-08-01 00:00:00"
    assert meta["truncated"] is True
    assert any("truncated" in n for n in meta["notes"])
    assert len(df) == 2


def test_a_missing_as_of_is_said_out_loud_not_invented(monkeypatch):
    monkeypatch.setattr(sqlrun, "run", lambda sql, limit_rows=10_000: (
        pd.DataFrame({"A": [1]}),
        {"rows": 1, "truncated": False, "elapsed_s": 0.1, "lane": "client-guard",
         "as_of": None, "warehouse": "COMPUTE_WH", "budget": "", "claim_refs": []},
    ))
    monkeypatch.setattr(sqlrun, "lane_status", lambda: {"lane": "client-guard", "notes": []})
    _df, meta = data.frame({"kind": "warehouse", "sql": "SELECT 1"})
    assert meta["as_of"] is None
    assert any("as_of is None" in n for n in meta["notes"])
    assert any("NOT server-side enforced" in n for n in meta["notes"])


def test_a_dead_connection_is_an_error_not_a_traceback(monkeypatch):
    def boom(sql, limit_rows=10_000):
        raise RuntimeError("250001 could not connect")

    monkeypatch.setattr(sqlrun, "run", boom)
    _df, meta = data.frame({"kind": "warehouse", "sql": "SELECT 1"})
    assert meta["ok"] is False
    assert "could not connect" in meta["error"]


# --------------------------------------------------------------------------- #
# column roles
# --------------------------------------------------------------------------- #
def test_all_digit_strings_stay_numeric_never_dates():
    """The live trap: '15020000001' is an FEC image number, not an epoch."""
    df = pd.DataFrame({"IMAGE_NUM": ["15020000001", "15020000002", "15020000003"]})
    roles = data.column_roles(df)
    assert roles["numeric"] == ["IMAGE_NUM"]
    assert roles["date"] == []


def test_an_all_text_landing_result_still_classifies():
    """Landing tables arrive with every column as TEXT. Roles are sniffed from
    the values, not from the dtype."""
    df = pd.DataFrame({
        "AMOUNT": ["1200.50", "980.00", "44.10"],
        "FILED_DATE": ["2024-01-05", "2024-02-11", "2024-03-02"],
        "STATE": ["CA", "TX", "NY"],
        "PARTY": ["DEM", "REP", "DEM"],
    })
    roles = data.column_roles(df)
    assert roles["numeric"] == ["AMOUNT"]
    assert roles["date"] == ["FILED_DATE"]
    assert roles["geo_state"] == ["STATE"]
    assert roles["category"] == ["PARTY"]


def test_a_real_datetime_column_is_a_date_not_a_number():
    """dtype is proof. pandas will happily turn datetime64 into nanoseconds,
    which is how a genuine date column used to come back classified numeric."""
    df = pd.DataFrame({
        "when": pd.date_range("2024-01-01", periods=5, freq="D"),
        "n": [1, 2, 3, 4, 5],
    })
    roles = data.column_roles(df)
    assert roles["date"] == ["when"]
    assert roles["numeric"] == ["n"]


def test_the_timeseries_demo_has_a_date_axis():
    df, _ = data.frame({"kind": "demo", "name": "timeseries"})
    roles = data.column_roles(df)
    assert roles["date"] == ["date"]
    assert roles["numeric"] == ["claims"]
    assert roles["category"] == ["region"]


def test_state_codes_and_a_share_column_named_state_do_not_collide():
    states, _ = data.frame({"kind": "demo", "name": "states"})
    ternary, _ = data.frame({"kind": "demo", "name": "ternary"})
    assert data.column_roles(states)["geo_state"] == ["state"]
    assert "state" in data.column_roles(ternary)["numeric"]
    assert data.column_roles(ternary)["geo_state"] == []


def test_provenance_stamps_are_never_offered_as_axes():
    df = pd.DataFrame({"A": [1, 2], "_INGESTED_AT": ["2026-01-01", "2026-01-02"]})
    roles = data.column_roles(df)
    flat = [c for cols in roles.values() for c in cols]
    assert "_INGESTED_AT" not in flat


def test_an_all_null_column_is_named_not_silently_lost():
    df = pd.DataFrame({"A": [1, 2], "B": [None, None]})
    roles = data.column_roles(df)
    assert roles["empty"] == ["B"]


def test_a_year_column_is_its_own_role():
    df = pd.DataFrame({"YEAR": [2019, 2020, 2021], "n": [1, 2, 3]})
    assert data.column_roles(df)["year"] == ["YEAR"]


def test_non_string_column_names_do_not_blow_up():
    """A numpy grid has integer column names; plugs upper-cases names."""
    df = pd.DataFrame(np.arange(9).reshape(3, 3))
    roles = data.column_roles(df)
    assert sorted(str(c) for c in roles["numeric"]) == ["0", "1", "2"]


def test_column_roles_on_an_empty_frame_is_empty_not_an_error():
    roles = data.column_roles(pd.DataFrame())
    assert all(v == [] for v in roles.values())


# --------------------------------------------------------------------------- #
# role substitution + the plain-English line
# --------------------------------------------------------------------------- #
def test_columns_for_allows_the_honest_substitutions():
    df = pd.DataFrame({
        "STATE": ["CA", "TX", "NY"],
        "YEAR": [2020, 2021, 2022],
        "TOTAL": [1.0, 2.0, 3.0],
        "PARTY": ["DEM", "REP", "IND"],
    })
    roles = data.column_roles(df)
    # a year is a number and a category; a state code is a category
    assert set(data.columns_for(roles, "numeric")) == {"TOTAL", "YEAR"}
    assert set(data.columns_for(roles, "category")) == {"PARTY", "STATE", "YEAR"}
    assert data.columns_for(roles, "date") == []
    assert data.columns_for(roles, "geo_state") == ["STATE"]
    assert len(data.columns_for(roles, "any")) == 4


def test_describe_roles_reads_like_a_sentence():
    df, _ = data.frame({"kind": "demo", "name": "category_2way"})
    line = data.describe_roles(data.column_roles(df))
    assert line == "this result has 1 number column, 2 category columns"


def test_role_of_is_the_inverse_view():
    df, _ = data.frame({"kind": "demo", "name": "states"})
    assert data.role_of(df)["state"] == "geo_state"
    assert data.role_of(df)["rate"] == "numeric"


# --------------------------------------------------------------------------- #
# discovery helpers degrade quietly when there is no warehouse
# --------------------------------------------------------------------------- #
def test_discovery_helpers_return_empty_when_offline(monkeypatch):
    import viz.catalog as catalog

    def boom(*a, **k):
        raise RuntimeError("no connection")

    monkeypatch.setattr(catalog, "find", boom)
    monkeypatch.setattr(catalog, "columns", boom)
    monkeypatch.setattr(catalog, "profile", boom)
    monkeypatch.setattr(catalog, "cast_sql", boom)
    monkeypatch.setattr(sqlrun, "lane_status", boom)

    assert data.tables("fec") == []
    assert data.table_columns("A.B.C") == []
    assert data.table_profile("A.B.C") == []
    assert data.starter_sql("A.B.C").startswith("SELECT *")
    assert data.lane()["lane"] == "offline"


def test_data_py_does_not_import_dash():
    """SPEC section 2: app.py is the only module allowed to import Dash."""
    src = (_REPO / "bench" / "data.py").read_text(encoding="utf-8")
    assert "import dash" not in src


# --------------------------------------------------------------------------- #
# the frame cache
# --------------------------------------------------------------------------- #
def _counting_lane(monkeypatch, frames=None):
    """Stand a counting stub in front of the read lane. Returns the counter.

    `frames` is an iterable of DataFrames to hand back in order, so a test can
    prove the SECOND fetch really was a second fetch. Exhausted -> the last one
    repeats.
    """
    calls = {"n": 0, "sql": [], "limit_rows": []}
    made = list(frames or [pd.DataFrame({"N": [1]})])

    def fake_run(sql, limit_rows=sqlrun.DEFAULT_LIMIT_ROWS):
        calls["n"] += 1
        calls["sql"].append(sql)
        calls["limit_rows"].append(limit_rows)
        df = made[min(calls["n"], len(made)) - 1]
        return df.copy(), {"rows": len(df), "truncated": False, "elapsed_s": 9.4,
                           "warehouse": "SERVE_WH", "lane": "enforced",
                           "as_of": "2026-08-01 00:00:00", "budget": "",
                           "claim_refs": []}

    monkeypatch.setattr(sqlrun, "run", fake_run)
    monkeypatch.setattr(sqlrun, "lane_status", lambda: {"lane": "enforced", "notes": []})
    return calls


def test_two_identical_requests_hit_the_read_lane_once(monkeypatch):
    """The whole point: a knob turn must not re-run your SQL."""
    calls = _counting_lane(monkeypatch)
    source = {"kind": "warehouse", "sql": "SELECT 1"}
    for _ in range(5):
        data.frame(source)
    assert calls["n"] == 1


def test_a_different_source_is_a_different_entry(monkeypatch):
    calls = _counting_lane(monkeypatch)
    data.frame({"kind": "warehouse", "sql": "SELECT 1"})
    data.frame({"kind": "warehouse", "sql": "SELECT 2"})
    data.frame({"kind": "warehouse", "sql": "SELECT 1", "limit_rows": 55})
    assert calls["n"] == 3


def test_refresh_bypasses_and_replaces_the_entry(monkeypatch):
    """RUN on the same SQL has to genuinely run it again, and the NEW answer
    is the one everybody gets afterwards."""
    calls = _counting_lane(monkeypatch, frames=[pd.DataFrame({"N": [1]}),
                                                pd.DataFrame({"N": [2]})])
    source = {"kind": "warehouse", "sql": "SELECT 1"}
    first, _ = data.frame(source)
    again, _ = data.frame(source)
    fresh, meta = data.frame(source, refresh=True)
    after, _ = data.frame(source)

    assert calls["n"] == 2
    assert int(first["N"][0]) == int(again["N"][0]) == 1
    assert int(fresh["N"][0]) == int(after["N"][0]) == 2
    assert meta["cached"] is False


def test_invalidate_drops_one_source_or_all(monkeypatch):
    calls = _counting_lane(monkeypatch)
    a = {"kind": "warehouse", "sql": "SELECT 1"}
    b = {"kind": "warehouse", "sql": "SELECT 2"}
    data.frame(a)
    data.frame(b)
    assert data.invalidate(a) == 1
    data.frame(a)
    assert calls["n"] == 3          # a re-ran, b did not
    assert data.invalidate() == 2
    assert data.cache_stats()["entries"] == 0


def test_the_demo_generator_does_not_run_twice_for_one_source(monkeypatch):
    """A cached demo frame is not regenerated - wall.RNG is not touched again."""
    data.clear_demo_cache()
    built = {"n": 0}
    real = data._build_demo

    def counting(d):
        built["n"] += 1
        return real(d)

    monkeypatch.setattr(data, "_build_demo", counting)
    for _ in range(4):
        data.frame({"kind": "demo", "name": "scatter"})
    assert built["n"] == 1


def test_meta_survives_the_cache_whole_and_says_it_was_cached(monkeypatch):
    """SPEC section 7's meta, plus the honesty flag: elapsed_s is the ORIGINAL."""
    _counting_lane(monkeypatch)
    source = {"kind": "warehouse", "sql": "SELECT 1"}
    _df, first = data.frame(source)
    _df, again = data.frame(source)

    for key in ("ok", "kind", "lane", "rows", "truncated", "as_of", "elapsed_s",
                "warehouse", "budget", "sql", "limit_rows"):
        assert again[key] == first[key], key
    assert first["elapsed_s"] == again["elapsed_s"] == 9.4
    assert first["cached"] is False
    assert again["cached"] is True
    assert again["cache_age_s"] >= 0.0
    assert any("frame cache" in n for n in again["notes"])
    # and the un-cached notes are still all there
    assert set(first["notes"]) <= set(again["notes"])


def test_a_cached_frame_cannot_be_poisoned_by_its_caller(monkeypatch):
    _counting_lane(monkeypatch)
    source = {"kind": "warehouse", "sql": "SELECT 1"}
    df, _ = data.frame(source)
    df.loc[0, "N"] = -999
    again, _ = data.frame(source)
    assert int(again["N"][0]) != -999


def test_copy_false_hands_back_the_cached_frame_itself(monkeypatch):
    """The repaint path's opt-out. Documented read-only; this proves it is the
    same object, which is exactly why it is documented that way."""
    _counting_lane(monkeypatch)
    source = {"kind": "warehouse", "sql": "SELECT 1"}
    a, _ = data.frame(source, copy=False)
    b, _ = data.frame(source, copy=False)
    assert a is b
    c, _ = data.frame(source)
    assert c is not a


def test_the_cache_evicts_least_recently_used_at_the_entry_cap():
    names = data.demo_names()[: data.CACHE_MAX_ENTRIES + 3]
    for name in names:
        data.frame({"kind": "demo", "name": name})
    stats = data.cache_stats()
    assert stats["entries"] == data.CACHE_MAX_ENTRIES
    kept = [f["source"]["name"] for f in stats["frames"]]
    assert kept == names[-data.CACHE_MAX_ENTRIES:]
    assert stats["evictions"] >= 3


def test_reading_an_entry_makes_it_the_last_to_be_evicted():
    names = data.demo_names()[: data.CACHE_MAX_ENTRIES]
    for name in names:
        data.frame({"kind": "demo", "name": name})
    data.frame({"kind": "demo", "name": names[0]})          # touch the oldest
    data.frame({"kind": "demo", "name": data.demo_names()[data.CACHE_MAX_ENTRIES]})
    kept = [f["source"]["name"] for f in data.cache_stats()["frames"]]
    assert names[0] in kept
    assert names[1] not in kept


def test_the_byte_cap_evicts_before_the_entry_cap_does(monkeypatch):
    """A 100k-row result is real. Three of them must not all be kept."""
    big = pd.DataFrame({"A": np.arange(100_000, dtype="float64"),
                        "B": np.arange(100_000, dtype="float64")})
    _counting_lane(monkeypatch, frames=[big])
    one, _ = data.frame({"kind": "warehouse", "sql": "SELECT 0"}, copy=False)
    per = data.cache_stats()["bytes"]
    assert per > 1_000_000, per                     # ~1.6 MB, measured

    monkeypatch.setattr(data, "CACHE_MAX_BYTES", int(per * 2.5))
    for i in range(1, 5):
        data.frame({"kind": "warehouse", "sql": f"SELECT {i}"})
    stats = data.cache_stats()
    assert stats["entries"] == 2, stats["entries"]   # 2.5 caps means two fit
    assert stats["bytes"] <= int(per * 2.5)


def test_one_result_bigger_than_the_whole_budget_is_still_cached(monkeypatch):
    """Refusing it would mean re-running the most expensive query in the app on
    every knob turn - the exact thing this cache exists to stop."""
    big = pd.DataFrame({"A": np.arange(50_000, dtype="float64")})
    calls = _counting_lane(monkeypatch, frames=[big])
    monkeypatch.setattr(data, "CACHE_MAX_BYTES", 1024)
    source = {"kind": "warehouse", "sql": "SELECT 1"}
    data.frame(source)
    data.frame(source)
    assert calls["n"] == 1
    assert data.cache_stats()["entries"] == 1


def test_a_failed_source_is_cached_too_and_refresh_is_the_way_back(monkeypatch):
    """A dead connection is the slowest thing in the building; retrying it on
    every repaint is worse than showing the error until RUN is pressed."""
    calls = {"n": 0}

    def boom(sql, limit_rows=10_000):
        calls["n"] += 1
        raise RuntimeError("250001 could not connect")

    monkeypatch.setattr(sqlrun, "run", boom)
    source = {"kind": "warehouse", "sql": "SELECT 1"}
    for _ in range(3):
        _df, meta = data.frame(source)
        assert meta["ok"] is False
    assert calls["n"] == 1
    data.frame(source, refresh=True)
    assert calls["n"] == 2


def test_the_cache_key_is_stable_and_order_independent():
    a = data.source_key({"kind": "warehouse", "sql": "SELECT 1", "limit_rows": 10})
    b = data.source_key({"limit_rows": 10, "sql": "SELECT 1", "kind": "warehouse"})
    assert a == b
    assert a != data.source_key({"kind": "warehouse", "sql": "SELECT  1",
                                 "limit_rows": 10})
    # a source that is not even a dict still keys, rather than raising
    assert data.source_key("nonsense") and data.source_key(None)


def test_the_cache_is_thread_safe_and_fetches_once(monkeypatch):
    """Dash serves callbacks concurrently. Ten threads, one fetch."""
    import threading

    calls = {"n": 0}
    started = threading.Event()

    def slow_run(sql, limit_rows=sqlrun.DEFAULT_LIMIT_ROWS):
        calls["n"] += 1
        started.set()
        time.sleep(0.2)          # a warehouse round trip, in miniature
        return (pd.DataFrame({"N": [1]}),
                {"rows": 1, "truncated": False, "elapsed_s": 9.4, "lane": "enforced",
                 "as_of": None, "warehouse": "SERVE_WH", "budget": "",
                 "claim_refs": []})

    monkeypatch.setattr(sqlrun, "run", slow_run)
    monkeypatch.setattr(sqlrun, "lane_status", lambda: {"lane": "enforced", "notes": []})

    source = {"kind": "warehouse", "sql": "SELECT 1"}
    seen: list = []
    threads = [threading.Thread(target=lambda: seen.append(data.frame(source)[1]))
               for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=30)

    assert calls["n"] == 1, "ten callbacks asking at once fired more than one query"
    assert len(seen) == 10
    assert all(m["ok"] and m["elapsed_s"] == 9.4 for m in seen)
    assert sum(1 for m in seen if m["cached"] is False) == 1


def test_a_slow_fetch_does_not_block_a_different_source(monkeypatch):
    """The cache lock is never held across a fetch - one slow query must not
    freeze every other callback in the process."""
    import threading

    gate = threading.Event()

    def blocking_run(sql, limit_rows=sqlrun.DEFAULT_LIMIT_ROWS):
        gate.wait(timeout=10)
        return (pd.DataFrame({"N": [1]}),
                {"rows": 1, "truncated": False, "elapsed_s": 9.4, "lane": "enforced",
                 "as_of": None, "warehouse": "SERVE_WH", "budget": "",
                 "claim_refs": []})

    monkeypatch.setattr(sqlrun, "run", blocking_run)
    monkeypatch.setattr(sqlrun, "lane_status", lambda: {"lane": "enforced", "notes": []})

    slow = threading.Thread(target=data.frame,
                            args=({"kind": "warehouse", "sql": "SELECT 1"},))
    slow.start()
    try:
        t0 = time.perf_counter()
        df, meta = data.frame({"kind": "demo", "name": "category"})
        took = time.perf_counter() - t0
        assert meta["ok"] and took < 2.0, f"a demo frame waited {took:.2f}s"
    finally:
        gate.set()
        slow.join(timeout=10)


# --------------------------------------------------------------------------- #
# the columns-and-roles accessor
# --------------------------------------------------------------------------- #
def test_frame_info_says_the_same_thing_as_the_long_way_round():
    source = {"kind": "demo", "name": "states"}
    df, meta = data.frame(source)
    info = data.frame_info(source)
    assert list(info.columns) == [str(c) for c in df.columns]
    assert info.rows == len(df) == meta["rows"]
    assert info.roles == data.column_roles(df)
    assert info.role_of == data.role_of(df)
    assert info.roles_line == data.describe_roles(data.column_roles(df))
    assert info.columns_for("category") == data.columns_for(info.roles, "category")
    assert info.ok is True


def test_frame_info_chart_roles_is_exactly_what_the_picker_computes():
    from bench import registry

    source = {"kind": "demo", "name": "scatter"}
    df, _ = data.frame(source)
    assert data.frame_info(source).chart_roles == registry.roles(df)


def test_frame_info_derives_roles_once(monkeypatch):
    """The picker asks on every repaint. It must cost one derivation, not N."""
    calls = {"n": 0}
    real = data.column_roles

    def counting(df):
        calls["n"] += 1
        return real(df)

    monkeypatch.setattr(data, "column_roles", counting)
    source = {"kind": "demo", "name": "long"}
    for _ in range(25):
        data.frame_info(source).roles
    assert calls["n"] == 1


def test_frame_info_and_frame_share_one_entry(monkeypatch):
    calls = _counting_lane(monkeypatch)
    source = {"kind": "warehouse", "sql": "SELECT 1"}
    info = data.frame_info(source)
    df, _meta = data.frame(source, copy=False)
    assert calls["n"] == 1
    assert info.df is df


def test_frame_info_refresh_rebuilds_the_roles_too(monkeypatch):
    calls = _counting_lane(monkeypatch, frames=[
        pd.DataFrame({"A": [1, 2]}),
        pd.DataFrame({"STATE": ["CA", "TX"], "TOTAL": [1.0, 2.0]}),
    ])
    source = {"kind": "warehouse", "sql": "SELECT 1"}
    assert list(data.frame_info(source).columns) == ["A"]
    assert list(data.frame_info(source, refresh=True).columns) == ["STATE", "TOTAL"]
    assert data.frame_info(source).roles["geo_state"] == ["STATE"]
    assert calls["n"] == 2


def test_frame_info_on_a_refused_query_is_empty_not_an_error():
    info = data.frame_info({"kind": "warehouse", "sql": "DROP TABLE x"})
    assert info.ok is False
    assert info.columns == ()
    assert info.chart_roles == {}
    assert info.roles_line == "this result has no chartable columns"


def test_clear_demo_cache_clears_the_demo_half_only(monkeypatch):
    _counting_lane(monkeypatch)
    data.frame({"kind": "warehouse", "sql": "SELECT 1"})
    data.frame({"kind": "demo", "name": "category"})
    assert data.cache_stats()["entries"] == 2
    data.clear_demo_cache()
    kinds = [f["kind"] for f in data.cache_stats()["frames"]]
    assert kinds == ["warehouse"]


def test_cache_stats_reports_what_is_actually_held():
    data.frame({"kind": "demo", "name": "category"})
    data.frame({"kind": "demo", "name": "category"})
    stats = data.cache_stats()
    assert stats["entries"] == 1
    assert stats["max_entries"] == data.CACHE_MAX_ENTRIES
    assert stats["max_bytes"] == data.CACHE_MAX_BYTES
    assert stats["hits"] >= 1 and stats["misses"] >= 1
    entry = stats["frames"][0]
    assert entry["kind"] == "demo" and entry["rows"] == 6
    assert entry["bytes"] > 0 and entry["serves"] == 2
