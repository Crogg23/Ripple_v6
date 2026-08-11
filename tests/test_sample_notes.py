"""Guards on the SAMPLE-ONLY declaration parser (scripts/build_sample_notes.py).

Seventeen mart models state in their own header that the table is a slice, not
the full source. That statement is what the catalog surfaces to anyone browsing
or building a chart, so a parser that silently finds nothing is worse than no
parser at all -- the catalog would just quietly stop warning. The first version
of this parser did exactly that: it treated the leading `{{ config(...) }}` line
as the end of the header and returned zero declarations from files that plainly
contain them.
"""
import importlib.util
import os

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SCRIPT = os.path.join(REPO, "scripts", "build_sample_notes.py")


def _mod():
    spec = importlib.util.spec_from_file_location("_build_sample_notes", _SCRIPT)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


bsn = _mod()


def _write(tmp_path, body):
    p = tmp_path / "marts" / "finance"
    p.mkdir(parents=True, exist_ok=True)
    f = p / "finance__fed_thing.sql"
    f.write_text(body, encoding="utf-8")
    return str(f)


def test_header_survives_a_leading_jinja_config_line(tmp_path):
    path = _write(tmp_path, "{{ config(materialized='table') }}\n\n"
                            "-- SAMPLE ONLY -- NOT the full dataset. 10 of 900 rows.\n"
                            "select 1\n")
    assert "SAMPLE ONLY" in bsn.header_of(path)


def test_header_stops_at_the_sql(tmp_path):
    path = _write(tmp_path, "-- a normal header\n"
                            "select 1 -- SAMPLE ONLY appears below the header\n")
    assert "SAMPLE ONLY" not in bsn.header_of(path)


@pytest.mark.parametrize("text,expected", [
    ("SAMPLE ONLY -- not the full thing", True),
    ("a 10-row proof slice of the corpus", True),
    ("sample only", True),
    # Must NOT fire on ordinary prose -- branding a complete dataset as partial
    # is a worse error than missing one.
    ("values are sampled at source every 15 minutes", False),
    ("one row per water sample taken", False),
    ("complete national download", False),
    # A model that has BEEN fixed often explains what it used to say. That
    # sentence must not put the source straight back on the sample list --
    # the FDIC institution directory tripped exactly this when its full pull
    # landed and its new header described the label it had carried before.
    ("this replaced a slice that had carried a sample-only label", False),
    ("no longer a partial load", False),
])
def test_declaration_pattern_is_deliberate(text, expected):
    assert bool(bsn.DECLARATION_RE.search(text)) is expected


def test_live_repo_still_yields_the_known_declarations():
    """If this drops to zero, the catalog silently stops warning about slices."""
    rows = bsn.scan()
    assert len(rows) >= 14, f"only {len(rows)} declarations found"
    ids = {r["source_id"] for r in rows}
    # Sources still known to be slices. FED_FDIC_BANK_DATA deliberately is NOT in
    # this list any more: its full 27,836-institution pull landed 2026-08-11, so
    # dropping off the sample list is the correct outcome, not a regression.
    for known in ("FED_CFPB_HMDA", "FED_DHS_HIFLD", "FED_USASPENDING_SUBAWARDS"):
        assert known in ids, f"{known} no longer detected"
    assert all(r["note"].upper().startswith(("SAMPLE ONLY", "PROOF SLICE")) for r in rows)
