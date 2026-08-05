"""The bench catalog snapshot: written on purpose, read for free.

The contract under test is the transparency promise itself:
  - snapshot_read is pure disk. It must never open a warehouse connection,
    even when the file is missing or corrupt.
  - snapshot_write is the ONE discovery call allowed to cost warehouse time,
    and what it writes round-trips exactly.
"""

from __future__ import annotations

import json

import pytest

from viz import catalog, sqlrun


FAKE_TABLES = [
    {"fqn": "LIBRARY_MARTS.HEALTH.MART_A", "name": "Hospital Money",
     "one_liner": "who pays whom", "domain": "health", "rows": 5,
     "lifecycle": "modeled", "is_sample": False},
]
FAKE_SHELVES = [{"arm": "catalog", "DOMAIN": "health", "SOURCES": 1,
                 "TOTAL_ROWS": 5}]


def test_snapshot_round_trips(tmp_path, monkeypatch):
    monkeypatch.setattr(catalog, "find", lambda term, refresh=False: FAKE_TABLES)
    monkeypatch.setattr(catalog, "shelves", lambda: FAKE_SHELVES)
    monkeypatch.setattr(sqlrun, "budget_line",
                        lambda refresh=False: "SERVE_MON: 1.00/10 cr used")
    path = tmp_path / "bench_catalog.json"
    written = catalog.snapshot_write(path)
    read = catalog.snapshot_read(path)
    assert read == json.loads(json.dumps(written, default=str))
    assert read["tables"] == FAKE_TABLES
    assert read["shelves"] == FAKE_SHELVES
    assert read["built_at"] and read["budget"].startswith("SERVE_MON")


def test_snapshot_read_never_connects(tmp_path, monkeypatch):
    def boom(*a, **k):
        raise AssertionError("snapshot_read opened a warehouse connection")

    monkeypatch.setattr(sqlrun, "connect", boom)

    assert catalog.snapshot_read(tmp_path / "missing.json") is None

    corrupt = tmp_path / "corrupt.json"
    corrupt.write_text("{not json", encoding="utf-8")
    assert catalog.snapshot_read(corrupt) is None

    good = tmp_path / "good.json"
    good.write_text(json.dumps({"built_at": "x", "tables": []}),
                    encoding="utf-8")
    assert catalog.snapshot_read(good) == {"built_at": "x", "tables": []}


def test_snapshot_write_is_atomic(tmp_path, monkeypatch):
    """A failed write must not leave a half-written file behind."""
    monkeypatch.setattr(catalog, "find", lambda term, refresh=False: FAKE_TABLES)
    monkeypatch.setattr(catalog, "shelves", lambda: FAKE_SHELVES)
    monkeypatch.setattr(sqlrun, "budget_line", lambda refresh=False: "ok")
    path = tmp_path / "snap.json"
    catalog.snapshot_write(path)
    first = catalog.snapshot_read(path)

    def boom():
        raise ConnectionError("warehouse gone")

    monkeypatch.setattr(catalog, "shelves", boom)
    with pytest.raises(ConnectionError):
        catalog.snapshot_write(path)
    assert catalog.snapshot_read(path) == first, "the old snapshot was clobbered"


def test_bench_data_wrappers_swallow_offline(monkeypatch):
    from bench import data as bench_data

    def boom(*a, **k):
        raise ConnectionError("no warehouse")

    monkeypatch.setattr(catalog, "snapshot_write", boom)
    assert bench_data.catalog_refresh() is None
    assert bench_data.LAST_CATALOG_ERROR and "ConnectionError" in bench_data.LAST_CATALOG_ERROR

    monkeypatch.setattr(catalog, "snapshot_read", lambda: {"tables": []})
    assert bench_data.catalog_snapshot() == {"tables": []}
