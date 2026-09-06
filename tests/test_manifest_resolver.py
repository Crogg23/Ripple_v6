"""Offline tests for the server-side manifest resolver. No network, no warehouse.

Written 2026-09-06 after both USAspending specs 404'd: their manifests were literal
lists of URLs stamped 20260706, and the publisher had swept that month's archive.
"""
import importlib.util
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "library-onboarding"))
sys.path.insert(0, str(_REPO / "scripts"))

_spec = importlib.util.spec_from_file_location("ssl_", _REPO / "scripts" / "server_side_load.py")
ssl_ = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ssl_)

STAMP = r"_(\d{8})\.zip$"


def _u(year, stamp, kind="Contracts"):
    return f"https://x/FY{year}_All_{kind}_Full_{stamp}.zip"


def test_only_the_newest_snapshot_survives():
    urls = [_u(2007, "20260706"), _u(2008, "20260706"),
            _u(2007, "20260806"), _u(2008, "20260806")]
    kept = ssl_._keep_latest(urls, STAMP)
    assert kept == [_u(2007, "20260806"), _u(2008, "20260806")]


def test_one_snapshot_is_left_alone():
    urls = [_u(y, "20260806") for y in range(2007, 2027)]
    assert ssl_._keep_latest(urls, STAMP) == urls


def test_unstamped_urls_are_not_silently_dropped():
    urls = ["https://x/all.zip", "https://x/more.zip"]
    assert ssl_._keep_latest(urls, STAMP) == urls


def test_a_mid_sweep_publisher_says_what_it_dropped(capsys):
    # Half swept to the new stamp is the dangerous case: it loads clean and the
    # table quietly misses years.
    urls = [_u(y, "20260906") for y in range(2007, 2016)] + \
           [_u(y, "20260806") for y in range(2016, 2027)]
    kept = ssl_._keep_latest(urls, STAMP)
    assert len(kept) == 9
    said = capsys.readouterr().out
    assert "kept 9 of 20" in said
    assert "20260806" in said


def test_a_short_manifest_is_refused_when_the_spec_says_how_many(capsys):
    import pytest
    m = {"expect_files": 20}
    with pytest.raises(RuntimeError, match="expects 20"):
        ssl_._check_expected([_u(y, "20260906") for y in range(2007, 2016)], m)
    assert ssl_._check_expected(["a"] * 20, m) == ["a"] * 20


def test_a_spec_without_expect_files_is_left_alone():
    assert ssl_._check_expected(["a", "b"], {}) == ["a", "b"]


def test_stamps_compare_left_to_right_so_padding_matters():
    # 20261001 must beat 20260906. String compare only works zero-padded.
    urls = [_u(2026, "20260906"), _u(2026, "20261001")]
    assert ssl_._keep_latest(urls, STAMP) == [_u(2026, "20261001")]


class _Resp:
    def __init__(self, text):
        self.text = text

    def raise_for_status(self):
        pass


def _page(keys, truncated):
    body = "".join(f"<Key>{k}</Key>" for k in keys)
    flag = "<IsTruncated>true</IsTruncated>" if truncated else "<IsTruncated>false</IsTruncated>"
    return _Resp(f"<ListBucketResult>{flag}{body}</ListBucketResult>")


def test_a_truncated_listing_is_walked_to_the_end(monkeypatch):
    # The real listing caps at 1000 keys; the files we need sat past position 4000.
    pages = [_page([f"k{i}" for i in range(1000)], True),
             _page([f"k{i}" for i in range(1000, 1700)], False)]
    calls = []

    def fake_get(url, **kw):
        calls.append(url)
        return pages[len(calls) - 1]

    import requests
    monkeypatch.setattr(requests, "get", fake_get)
    out = ssl_._fetch_listing_pages("https://x/archive/", "s3")
    assert len(out) == 2
    assert "marker=k999" in calls[1]


def test_without_the_paginate_flag_only_one_page_is_read(monkeypatch):
    calls = []

    def fake_get(url, **kw):
        calls.append(url)
        return _page(["k1"], True)

    import requests
    monkeypatch.setattr(requests, "get", fake_get)
    ssl_._fetch_listing_pages("https://x/archive/", None)
    assert len(calls) == 1


def test_a_listing_that_never_ends_is_refused(monkeypatch):
    import pytest

    def fake_get(url, **kw):
        return _page([f"k{i}" for i in range(1000)], True)

    import requests
    monkeypatch.setattr(requests, "get", fake_get)
    with pytest.raises(RuntimeError, match="100k"):
        ssl_._fetch_listing_pages("https://x/archive/", "s3")


def test_neither_usaspending_spec_carries_dated_urls_any_more():
    import server_side_specs as specs
    for sid in ("FED_USASPENDING_CONTRACTS_FULL", "FED_USASPENDING_ASSISTANCE_FULL"):
        d = next(x for x in specs.SPECS if x["source_id"] == sid)
        m = d["manifest"]
        assert not isinstance(m, list), f"{sid} is a frozen list again"
        assert m.get("paginate") == "s3"
        assert m.get("latest_re")


def test_no_spec_holds_a_frozen_monthly_dated_list():
    # Narrow on purpose. Several specs still freeze quarter or cycle URLs, e.g.
    # FED_SEC_INSIDER on 2016q3 and the FEC cycle files. Those rot on a slower
    # clock and are a separate decision. This guards only the monthly YYYYMMDD
    # species that broke both USAspending specs.
    import re
    import server_side_specs as specs
    bad = []
    for d in specs.SPECS:
        m = d.get("manifest")
        if isinstance(m, list) and any(re.search(r"\d{8}", u) for u in m):
            bad.append(d["source_id"])
    assert not bad, f"monthly-dated URLs frozen into: {bad}"


def test_the_staged_path_for_a_zip_member_carries_the_filename():
    # An index-only staged path let --reuse-staged serve last month's parts.
    src = (_REPO / "scripts" / "server_side_load.py").read_text()
    assert "part_{i:04d}.gz" not in src
