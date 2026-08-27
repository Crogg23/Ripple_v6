"""Live canary on the human sign-off gate (CLAUDE.md §7: sign-off on every
finding, auto-publish blocked, no exceptions).

Found 2026-08-26: the gate machinery is wired correctly but has never recorded
a real decision — LIBRARY_META.REVIEW.DECISIONS holds only the two SMOKE_TEST
rows, and every downstream view filters those out, so the gate's healthy output
today (0 effective decisions) is INDISTINGUISHABLE from its broken output.
Nothing would notice if the append-only wall, the filters, or the views broke.
This canary makes breakage visible:

  (1) the decision wall still exists and still holds its delete-proof smoke rows
      (their absence means the append-only guarantee failed or someone wiped it);
  (2) every downstream gate view still compiles and still filters smoke rows;
  (3) the lead queue actually feeds the gate (a non-trivial queue with a broken
      gate is the silent-auto-publish nightmare scenario).

All read-only. Skips (not fails) if the warehouse is unreachable, matching the
other live tests.
"""

import pytest

from connect import db


def _cur():
    try:
        return db.connect().cursor()
    except Exception as e:  # pragma: no cover - offline dev boxes
        pytest.skip(f"warehouse unreachable: {e}")


def test_decision_wall_holds_its_delete_proof_rows():
    cur = _cur()
    cur.execute(
        "select count(*) from LIBRARY_META.\"REVIEW\".DECISIONS"
        " where TARGET_ID = 'SMOKE_TEST'"
    )
    smoke = cur.fetchone()[0]
    assert smoke >= 2, (
        "The append-only decision wall lost its SMOKE_TEST rows — either the "
        "delete-proofing failed or the table was recreated. The publish gate "
        "can no longer be trusted until this is explained."
    )


def test_gate_views_compile_and_filter_smoke_rows():
    cur = _cur()
    # The views expose the target under per-grain names (LEAD_ID / COHORT_ID),
    # not the wall's TARGET_ID.
    for view, id_col in (("V_LATEST_DECISIONS", "LEAD_ID"),
                         ("V_LATEST_COHORT_DECISIONS", "COHORT_ID"),
                         ("V_EFFECTIVE_LEAD_DECISIONS", "LEAD_ID")):
        cur.execute(
            f"select count(*) from LIBRARY_META.\"REVIEW\".{view}"
            f" where {id_col} = 'SMOKE_TEST'"
        )
        leaked = cur.fetchone()[0]
        assert leaked == 0, (
            f"{view} is leaking SMOKE_TEST rows — its filter broke, so its "
            "row counts no longer mean 'real human decisions'."
        )


def test_lead_queue_feeds_a_working_gate():
    cur = _cur()
    cur.execute("select count(*) from LIBRARY_MARTS.\"REVIEW\".LEAD_QUEUE")
    queued = cur.fetchone()[0]
    assert queued > 0, (
        "LEAD_QUEUE is empty — either the queue build broke or the gate has "
        "nothing to gate. Both need a human look."
    )
    # V_LEADS_PUBLISHED intentionally carries pending leads too; the gate lives
    # in its PUBLISHED stamp. No lead may carry the stamp without an effective
    # human decision behind it.
    cur.execute(
        "select count(*) from LIBRARY_META.\"REVIEW\".V_EFFECTIVE_LEAD_DECISIONS"
    )
    decided = cur.fetchone()[0]
    cur.execute(
        "select count(*) from LIBRARY_META.\"CONNECT\".V_LEADS_PUBLISHED"
        " where PUBLISHED"
    )
    stamped = cur.fetchone()[0]
    assert stamped <= decided, (
        f"{stamped} leads carry the PUBLISHED stamp but only {decided} effective "
        "human decisions exist — something is publishing around the gate."
    )
    cur.execute(
        "select count(*) from LIBRARY_META.\"CONNECT\".V_LEADS_PUBLISHED"
        " where PUBLISHED and REVIEW_STATE = 'pending'"
    )
    leaked = cur.fetchone()[0]
    assert leaked == 0, (
        f"{leaked} pending (never human-reviewed) leads carry the PUBLISHED "
        "stamp — the two-step gate is broken."
    )
