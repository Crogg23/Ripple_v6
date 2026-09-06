"""Offline tests for scripts/coverage_probe.py. No warehouse connection.

Cases here are the defects the 2026-09-06 skeptic pass found in the first cut:
sentinel years, interior holes, load stamps counted as coverage, and a
hand-rolled column picker that missed most of the real date columns.
"""
import importlib.util
import json
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "library-onboarding"))
sys.path.insert(0, str(_REPO / "scripts"))

_spec = importlib.util.spec_from_file_location("cp", _REPO / "scripts" / "coverage_probe.py")
cp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cp)


def test_mapping_loads_and_is_the_ledgers_own():
    m = cp.load_mapping()
    assert len(m) >= 100
    assert all("source_id" in v for v in m.values())


def test_sentinel_years_are_excluded_from_the_scan():
    m = {"source_id": "x", "recency_col": "RPT_DATE", "recency_kind": "date"}
    sql = cp.years_sql(m)
    assert f"BETWEEN {cp.YEAR_FLOOR} AND {cp.year_ceiling()}" in sql


def test_scan_is_grouped_by_year_not_min_max():
    # min/max cannot see an interior hole; a per-year count can.
    m = {"source_id": "x", "recency_col": "FILED", "recency_kind": "mixed"}
    sql = cp.years_sql(m)
    assert "GROUP BY 1" in sql
    assert "COUNT(*)" in sql
    assert "MIN(" not in sql and "MAX(" not in sql


def test_prose_mapping_values_are_skipped_not_guessed():
    m = {"source_id": "x", "recency_col": "derived from two columns", "recency_kind": "mixed"}
    assert cp.years_sql(m) is None


def test_source_with_no_recency_column_is_skipped():
    assert cp.years_sql({"source_id": "x"}) is None


def test_parser_is_the_ledgers_not_a_second_copy():
    import build_freshness_ledger as ledger
    assert cp.recency_inner is ledger.recency_inner


def test_epoch_trap_guard_survives_the_reuse():
    # A bare year must not parse as seconds-since-epoch and land in 1970.
    sql = cp.years_sql({"source_id": "x", "recency_col": "YEAR", "recency_kind": "year_text"})
    assert "DATE_FROM_PARTS" in sql
    assert "TRY_TO_DATE(NULLIF" not in sql


def test_span_marks_interior_holes():
    # The lobby case: 1999-2021 on paper, 2011-2019 absent.
    years = {y: 10 for y in list(range(1999, 2011)) + list(range(2020, 2022))}
    out = cp._span(years)
    assert out.startswith("1999-2021")
    assert "missing 9" in out


def test_span_says_so_when_there_are_no_holes():
    assert cp._span({2020: 1, 2021: 1, 2022: 1}) == "2020-2022"


def test_span_of_nothing_is_not_measured():
    assert cp._span({}) == "not measured"


def test_landing_fqn_defaults_to_the_landing_schema():
    assert cp.fqn_of({"source_id": "fed_x"}) == "LIBRARY_RAW.LANDING.FED_X"
    assert cp.fqn_of({"source_id": "fed_x", "landing_fqn": "A.B.C"}) == "A.B.C"


def test_every_mapped_source_either_scans_or_says_why():
    # The first cut silently found no date column on 73% of these.
    m = cp.load_mapping()
    scannable = [s for s, v in m.items() if cp.years_sql(v) is not None]
    assert len(scannable) / len(m) > 0.75, f"only {len(scannable)} of {len(m)} scan"


def test_no_shared_years_is_reported_as_none():
    trades = {y: 100 for y in range(2012, 2021)}
    bills = {y: 100 for y in range(2023, 2027)}
    shared, spans = cp.shared_spans(trades, bills)
    assert shared == [] and spans == ""


def test_a_hole_on_one_side_removes_that_year():
    lobby = {y: 5 for y in list(range(1999, 2011)) + list(range(2020, 2022))}
    rules = {y: 5 for y in range(2005, 2026)}
    shared, spans = cp.shared_spans(lobby, rules)
    assert 2015 not in shared
    assert spans == "2005-2010, 2020-2021"


def test_contiguous_overlap_collapses_to_one_run():
    a = {y: 1 for y in range(2010, 2021)}
    b = {y: 1 for y in range(2015, 2031)}
    shared, spans = cp.shared_spans(a, b)
    assert spans == "2015-2020"
    assert len(shared) == 6


def test_a_single_shared_year_prints_without_a_dash():
    _, spans = cp.shared_spans({2020: 1}, {2020: 1, 2021: 1})
    assert spans == "2020"


# --- the shared parser, after the 2026-09-06 repairs -------------------------

def _inner(col="C", kind="mixed"):
    import build_freshness_ledger as ledger
    return ledger.recency_inner(col, kind)


def test_new_patterns_are_whole_string_matches():
    # Snowflake REGEXP_LIKE matches the entire string. A prefix-style pattern
    # silently fails on any longer value, which cost four date shapes. The
    # four repaired branches must all describe the whole string.
    sql = _inner()
    for marker in ("MM/DD/YYYY", "MMMM DD, YYYY", "DD MON YYYY"):
        assert marker in sql
    assert "(19|20)[0-9]{2}.*" in sql          # us_dt
    assert "[A-Za-z]{3,9} [0-9]{1,2}, (19|20)[0-9]{2}" in sql


def test_the_year_branch_refuses_longer_digit_strings():
    # With a bare .* an id like 1234567, or a yyyymmdd like 20240108, parsed
    # to a year and cleared every downstream clamp.
    sql = _inner(kind="year_text")
    assert "([^0-9].*)?" in sql
    assert "(1[0-9]{3}|20[0-9]{2}).*'" not in sql


def test_the_four_repaired_shapes_have_a_branch():
    sql = _inner()
    assert "MM/DD/YYYY" in sql          # 5/1/2000 12:00:00 AM
    assert "MMMM DD, YYYY" in sql       # September 29, 2025
    assert "DD MON YYYY" in sql         # Oct 2025
    assert "YYYY-MM-DD" in sql          # 2023-09


def test_explicit_year_kinds_reach_before_1900():
    assert "1[0-9]{3}" in _inner(kind="year_text")
    assert "1[0-9]{3}" in _inner(kind="year_int")


def test_mixed_keeps_the_narrow_year_rule():
    # A stray four-digit id must never be read as a year on a mixed column.
    assert "1[0-9]{3}" not in _inner(kind="mixed")


def test_a_quoted_mapping_value_is_taken_as_a_column_name():
    import build_freshness_ledger as ledger
    assert ledger.col_ref('"Date received"') == '"Date received"'


def test_an_unquoted_string_with_spaces_is_still_prose():
    import build_freshness_ledger as ledger
    assert ledger.col_ref("Date received") is None
    assert ledger.col_ref("derived from two columns") is None


def test_the_year_floor_reaches_the_oldest_real_data():
    # SlaveVoyages starts 1550; OWID life expectancy reaches 1543.
    assert cp.YEAR_FLOOR <= 1543



def test_edge_strays_are_trimmed_but_interior_holes_are_not():
    # CA_LOBBY_COVER: 17 rows scattered 1927-1999 against 568,988 from 2000 on.
    ca = {1927: 1, 1931: 1, 1933: 1, 1950: 1, 1971: 2, 1992: 1, 1993: 1, 1999: 5}
    ca.update({y: 20000 for y in range(2000, 2027)})
    ca[2028] = 3
    assert cp._span(ca).startswith("2000-2026")
    assert "stray" in cp._span(ca)


def test_an_interior_hole_survives_trimming():
    lda = {y: 5000 for y in list(range(1999, 2011)) + list(range(2020, 2022))}
    assert cp._span(lda) == "1999-2021, missing 9"


def test_trimming_never_empties_a_table():
    assert cp.dense_years({2020: 1}) == {2020: 1}
    assert cp.dense_years({}) == {}


def test_overlap_math_runs_on_trimmed_years():
    # A stray 1927 row must not make a lobby table overlap a 1920s table.
    ca = {1927: 1}
    ca.update({y: 20000 for y in range(2000, 2027)})
    old = {y: 100 for y in range(1920, 1935)}
    shared, _ = cp.shared_spans(cp.dense_years(ca), cp.dense_years(old))
    assert shared == []
