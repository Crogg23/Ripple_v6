"""The docket holds every idea, so a silent drift in it is expensive.

These run offline against docket/docket.csv.
"""
import csv
import importlib.util
import re
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "scripts"))
_spec = importlib.util.spec_from_file_location(
    "bic", _REPO / "scripts" / "build_docket.py")
bic = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bic)

ROWS = list(csv.DictReader((_REPO / "docket" / "docket.csv").open()))


def test_every_original_idea_survived_the_import():
    old = list(csv.DictReader(
        (_REPO / "reports" / "hunch_master_spreadsheet_2026-09-05.csv").open()))
    assert {r["#"] for r in old} == {r["id"] for r in ROWS}
    assert len(ROWS) == 150


def test_ids_are_unique():
    ids = [r["id"] for r in ROWS]
    assert len(ids) == len(set(ids))


def test_status_is_one_of_six():
    assert {r["where_it_stands"] for r in ROWS} <= set(bic.STANDS)


def test_not_checked_yet_is_open_not_confirmed():
    # "Not checked yet" contains "checked"; the first cut read 62 of them as done.
    assert bic.read_where_it_stands("Not checked yet") == "not started"
    assert bic.read_where_it_stands("Not checked yet, and the data is thin") == "not started"


def test_a_negative_result_is_a_finish_not_an_untouched_idea():
    for s in ("No pattern found", "No difference found", "None found so far",
              "Checked, came back clean — none found", "Checked, no clear pattern"):
        assert bic.read_where_it_stands(s) == "nothing there", s


def test_a_missing_piece_is_not_the_same_as_nothing_there():
    # One means stop. The other means come back when the data lands.
    assert bic.read_where_it_stands("Dead end — the detailed trial data isn't loaded") \
        == "missing a piece"
    assert bic.read_where_it_stands("Dead end — that bank ID field is empty everywhere") \
        == "missing a piece"
    assert bic.read_where_it_stands("Dead end — no real relationship found") == "nothing there"


def test_no_label_needs_a_glossary():
    # Every state has to read as plain English on its own.
    for word in bic.STANDS:
        assert " " in word or word.isalpha(), word
        assert word == word.lower()


def test_a_real_finding_is_confirmed():
    assert bic.read_where_it_stands("Confirmed — 39 homes did exactly this") == "found something"
    assert bic.read_where_it_stands("CONFIRMED — worst-graded areas have 18x more") == "found something"


def test_partial_work_is_not_a_finish():
    assert bic.read_where_it_stands("Partially checked, needs a full run") == "part done"
    assert bic.read_where_it_stands("Found 4 so far, confirmed") == "part done"


def test_every_row_has_a_question():
    blank = [r["id"] for r in ROWS if not r["question"].strip()]
    assert not blank, f"no question on {blank}"


def test_probe_links_point_at_a_real_directory():
    for r in ROWS:
        if r["probe"]:
            assert (_REPO / r["probe"]).is_dir(), r["probe"]


def test_probe_directory_matches_the_id_it_is_linked_to():
    for r in ROWS:
        if r["probe"]:
            lead = re.match(r"(E?\d+)_", Path(r["probe"]).name).group(1)
            assert lead == r["id"], f"{r['id']} linked to {r['probe']}"


def test_needs_names_a_hole_from_the_data_holes_plan():
    # The docket and the backfill plan must point at the same holes, or one
    # of them is quietly wrong.
    plan = (_REPO / "reports" / "politics_probe_2026-09-05" / "DATA_HOLES.md").read_text().lower()
    named = {h.strip().lower() for r in ROWS if r["needs"] for h in r["needs"].split(";")}
    assert named, "no entry names a hole"
    missing = [h for h in named if h.split()[0] not in plan]
    assert not missing, missing


def test_a_confirmed_entry_may_still_need_more_data():
    # E43 confirmed on one HCRIS vintage; more years would widen it, not
    # invalidate it. The column has to stay honest for both cases.
    e43 = next(r for r in ROWS if r["id"] == "E43")
    assert e43["where_it_stands"] == "found something"
    assert "HCRIS" in e43["needs"]


def test_the_open_view_only_holds_pickable_work():
    open_rows = list(csv.DictReader(
        (_REPO / "docket" / "docket_open.csv").open()))
    assert {r["where_it_stands"] for r in open_rows} <= set(bic.OPEN_STATES)
    assert len(open_rows) == sum(1 for r in ROWS if r["where_it_stands"] in bic.OPEN_STATES)
