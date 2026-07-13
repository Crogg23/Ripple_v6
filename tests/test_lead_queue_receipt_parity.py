"""Receipt parity lock: the SQL-ported verdicts in the LEAD_QUEUE mart must
match scripts/lead_receipt.py — the Python script IS the spec (Reading Room
plan, test 1.4.5). Any divergence is a stop-and-reconcile defect.

How it works, per sampled banned_but_paid lead:
  1. Pull the mart row (confidence_tier + receipt_verdict).
  2. Run the receipt script's own SQL for that NPI and feed the row through
     its actual receipt() function — not a reimplementation.
  3. Map both sides to a common enum and compare.

Mapping (the mart adds one honest extra state the script lumps in):
  script '✅ PAID ON/AFTER EXCLUSION'  <-> mart PAID_ON_OR_AFTER_EXCLUSION
  script '⚠️ payments predate'         <-> mart PAYMENTS_PREDATE_EXCLUSION
                                            or TIMELINE_UNKNOWN
  script '✅ FACT-grade'               <-> mart FACT_GRADE_3_SOURCE
  script '🚩 CONFLICT'                 <-> mart NPPES_CONFLICT
  script '🟡 2-SOURCE'                 <-> mart TWO_SOURCE
  script returns NO ROW (source drift) <-> mart LEIE_ROW_MISSING
                                            or TIMELINE_UNKNOWN

Sample: every NPPES_CONFLICT and TWO_SOURCE lead first, then top-priority
FACT-grade leads, 40 total (>= 25 required by the plan).

Requires a live connection (reader lane suffices) — self-skips offline, like
every @pytest.mark.snowflake test in this suite. Until LEAD_QUEUE is
materialized (pending action: scoped write PAT + dbt build --select
marts.review), it falls back to the compiled preview SQL if present.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
for p in (REPO / "library-onboarding", REPO / "scripts"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

COMPILED = (REPO / "library-onboarding/ripple_dbt/target/compiled/ripple/"
                   "models/marts/review/lead_queue.sql")

pytestmark = pytest.mark.snowflake


def _connect():
    try:
        import snow
        return snow.connect()
    except Exception as exc:  # no creds / offline — never fail, always skip
        pytest.skip(f"no Snowflake connection: {exc}")


def _queue_sql(cur) -> str:
    """FROM-able source for the queue: the materialized mart if it exists,
    else the compiled model SQL (receipt columns stubbed — the safe view
    gains them when scripts/refresh_v_leads_published.sql is applied)."""
    try:
        cur.execute("SELECT 1 FROM LIBRARY_MARTS.DBT_CROGERS.LEAD_QUEUE LIMIT 1")
        return "LIBRARY_MARTS.DBT_CROGERS.LEAD_QUEUE"
    except Exception:
        pass
    if not COMPILED.exists():
        pytest.skip("LEAD_QUEUE not materialized and no compiled SQL found "
                    "(run: dbt compile --select lead_queue)")
    sql = COMPILED.read_text()
    for col, typ in (("compiled_sql", "VARCHAR"), ("sql_sha256", "VARCHAR"),
                     ("as_of_date", "DATE")):
        sql, n = re.subn(rf"^[ \t]*{col},[ \t]*$",
                         f"CAST(NULL AS {typ}) AS {col},", sql,
                         count=1, flags=re.M)
        if n != 1:
            pytest.skip(f"compiled SQL shape changed (stub {col} matched {n})")
    return f"({sql})"


def _spec_verdicts(cur, npi: str):
    """Run lead_receipt.py's own SQL + receipt() for one NPI; return the
    (timeline, confidence) markers from the spec's rendered text."""
    import lead_receipt

    sql, params = lead_receipt._build_query(npi, None, 1)
    cur.execute(sql, params)
    cols = [d[0] for d in cur.description]
    rows = [dict(zip(cols, r)) for r in cur.fetchall()]
    if not rows:
        return None
    text = lead_receipt.receipt(rows[0])
    timeline = ("PAID_ON_OR_AFTER" if "PAID ON/AFTER EXCLUSION" in text
                else "WEAKER")
    if "FACT-grade" in text:
        conf = "FACT_GRADE_3_SOURCE"
    elif "CONFLICT" in text:
        conf = "NPPES_CONFLICT"
    else:
        conf = "TWO_SOURCE"
    return timeline, conf


def test_receipt_parity():
    conn = _connect()
    try:
        cur = conn.cursor()
        q = _queue_sql(cur)

        cur.execute(f"""
            SELECT lead_id, entity_a_key_value, confidence_tier, receipt_verdict
            FROM {q}
            WHERE detector = 'banned_but_paid'
            QUALIFY ROW_NUMBER() OVER (
                ORDER BY IFF(confidence_tier IN ('NPPES_CONFLICT','TWO_SOURCE'), 0, 1),
                         priority_rank) <= 40
        """)
        sample = cur.fetchall()
        assert len(sample) >= 25, f"sample too small: {len(sample)}"

        mismatches, checked = [], 0
        for lead_id, npi, mart_tier, mart_verdict in sample:
            spec = _spec_verdicts(cur, npi)
            if spec is None:
                # The receipt script INNER-joins LEIE and Open Payments — a
                # row that vanished since detection (monthly OIG refresh, OP
                # re-land) returns nothing. The mart's ONLY honest states for
                # that are LEIE_ROW_MISSING (exclusion gone) or
                # TIMELINE_UNKNOWN (payments gone). Anything else = the mart
                # claims a receipt the spec cannot reproduce.
                checked += 1
                if not (mart_tier == "LEIE_ROW_MISSING"
                        or mart_verdict == "TIMELINE_UNKNOWN"):
                    mismatches.append((lead_id, npi, "spec query returned no row",
                                       mart_tier, mart_verdict))
                continue
            spec_timeline, spec_conf = spec
            mart_timeline = ("PAID_ON_OR_AFTER"
                             if mart_verdict == "PAID_ON_OR_AFTER_EXCLUSION"
                             else "WEAKER")
            checked += 1
            if spec_timeline != mart_timeline or spec_conf != mart_tier:
                mismatches.append((lead_id, npi,
                                   f"spec=({spec_timeline},{spec_conf})",
                                   f"mart=({mart_timeline},{mart_tier})"))

        assert checked >= 25, f"only {checked} leads fully checked"
        assert not mismatches, (
            f"{len(mismatches)} parity mismatch(es) — the Python script is "
            f"the spec; stop and reconcile:\n" +
            "\n".join(str(m) for m in mismatches[:10]))
    finally:
        conn.close()
