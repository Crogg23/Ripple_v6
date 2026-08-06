"""Evidence smoke lock (Reading Room plan, test 1.4.6): for the top 10 leads
by priority, the stored evidence_sql (the lead's frozen COMPILED_SQL receipt)
must execute and return >= 1 row.

KNOWN, DOCUMENTED exception: banned_but_operating receipts reference
FED_CMS_FACILITY_AFFILIATION, which was dropped from LANDING (verified
2026-07-12, registered in LIBRARY_META.BUILD). Those receipts are expected to
fail with 'does not exist' — any OTHER failure mode on them still fails this
test. Hiding them entirely would make the queue look healthier than it is.

Requires the materialized LEAD_QUEUE (evidence_sql only reaches the safe view
once scripts/refresh_v_leads_published.sql is applied) — skips before that.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
if str(REPO / "library-onboarding") not in sys.path:
    sys.path.insert(0, str(REPO / "library-onboarding"))

pytestmark = pytest.mark.snowflake

DROPPED_TABLE = "FED_CMS_FACILITY_AFFILIATION"


def _connect():
    try:
        import snow
        return snow.connect(session_parameters={"STATEMENT_TIMEOUT_IN_SECONDS": 300})
    except Exception as exc:
        pytest.skip(f"no Snowflake connection: {exc}")


def test_top10_evidence_sql_reproduces():
    conn = _connect()
    try:
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT lead_id, detector, priority_rank, evidence_sql
                FROM LIBRARY_MARTS.REVIEW.LEAD_QUEUE
                WHERE priority_rank <= 10
                ORDER BY priority_rank
            """)
        except Exception as exc:
            # Only a genuinely-absent mart is a skip; any other failure
            # (grants, timeout) must FAIL, not silently un-enforce the lock.
            if "does not exist" in str(exc):
                pytest.skip(f"LEAD_QUEUE not materialized yet: {exc}")
            raise
        top10 = cur.fetchall()
        if not top10:
            pytest.skip("queue is empty (every lead decided) — nothing to smoke-test")
        assert len(top10) <= 10

        failures = []
        for lead_id, detector, rank, evidence_sql in top10:
            if not evidence_sql or not evidence_sql.strip():
                failures.append((rank, lead_id, detector, "evidence_sql empty"))
                continue
            try:
                cur.execute(evidence_sql)
                rows = cur.fetchmany(1)
                if not rows:
                    failures.append((rank, lead_id, detector,
                                     "ran clean but returned 0 rows"))
            except Exception as exc:
                msg = str(exc)
                known_dropped = (detector == "banned_but_operating"
                                 and DROPPED_TABLE in msg
                                 and "does not exist" in msg)
                if not known_dropped:
                    failures.append((rank, lead_id, detector, msg[:200]))

        assert not failures, (
            "evidence_sql smoke failures (a lead whose receipt can't be "
            "re-run must not sit in the top 10 unexplained):\n" +
            "\n".join(str(f) for f in failures))
    finally:
        conn.close()
