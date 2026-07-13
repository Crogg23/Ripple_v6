"""ALL SQL for the Reading Room lives here — parameterized, bind variables
only. User input NEVER lands in SQL text (no f-strings over values); the
offline tests assert it.

Read surfaces: LIBRARY_MARTS.DBT_CROGERS.LEAD_QUEUE (the triage mart),
LIBRARY_META.REVIEW.V_LATEST_DECISIONS (decisions truth),
LIBRARY_META."CONNECT".V_LEADS_PUBLISHED (evidence payload — the SAFE view,
never raw LEADS), plus per-lead source-record pulls from LANDING.
Write surface: exactly one INSERT into LIBRARY_META.REVIEW.DECISIONS.
"""
from __future__ import annotations

import json

QUEUE_TABLE = "LIBRARY_MARTS.DBT_CROGERS.LEAD_QUEUE"

DETECTORS = [
    "banned_but_paid",
    "excluded_but_billing",
    "banned_but_operating",
    "debarred_but_funded",
    "sanctioned_vessel_broadcasting_v2",
    "sanctioned_vessel_broadcasting",
    "sec_filer_in_irs_bmf",
]

TIERS = ["FACT_GRADE_3_SOURCE", "TWO_SOURCE", "NPPES_CONFLICT",
         "LEIE_ROW_MISSING", "HARD_ID_ONLY"]

# Button -> verdict vocabulary (the existing lowercase contract + needs_work;
# needs_work is non-suppressing, so the lead stays visible and flagged).
VERDICTS = {
    "confirm": "confirmed",
    "reject": "rejected",
    "needs_work": "needs_work",
}

# Decided leads drop out of the queue; needs_work stays (flagged).
_QUEUE_FILTER = (
    "COALESCE(d.decision, 'pending') NOT IN "
    "('confirmed', 'rejected', 'retracted', 'stale')"
)

_QUEUE_SELECT = f"""
SELECT
    q.lead_id, q.detector, q.priority_rank, q.priority_score, q.headline,
    q.confidence_tier, q.receipt_verdict, q.caveat,
    d.decision AS latest_decision, d.decided_at AS latest_decided_at
FROM {QUEUE_TABLE} q
LEFT JOIN LIBRARY_META.REVIEW.V_LATEST_DECISIONS d
       ON d.lead_id = q.lead_id
WHERE {_QUEUE_FILTER}
"""


def queue_sql(detector: str | None = None, tier: str | None = None,
              limit: int = 20) -> tuple[str, tuple]:
    """Top-of-queue pull. Filters are optional; values are BOUND."""
    sql, params = _QUEUE_SELECT, []
    if detector:
        sql += " AND q.detector = %s"
        params.append(detector)
    if tier:
        sql += " AND q.confidence_tier = %s"
        params.append(tier)
    sql += " ORDER BY q.priority_rank LIMIT %s"
    params.append(int(limit))
    return sql, tuple(params)


def queue_depth_sql(detector: str | None = None,
                    tier: str | None = None) -> tuple[str, tuple]:
    """How many reviewable leads match the current filter ('20 of N')."""
    sql = (f"SELECT COUNT(*) FROM {QUEUE_TABLE} q "
           "LEFT JOIN LIBRARY_META.REVIEW.V_LATEST_DECISIONS d "
           "ON d.lead_id = q.lead_id "
           f"WHERE {_QUEUE_FILTER}")
    params = []
    if detector:
        sql += " AND q.detector = %s"
        params.append(detector)
    if tier:
        sql += " AND q.confidence_tier = %s"
        params.append(tier)
    return sql, tuple(params)


CASE_SQL = f"""
SELECT q.*, d.decision AS latest_decision, d.reason AS latest_reason,
       d.reviewer AS latest_reviewer, d.decided_at AS latest_decided_at
FROM {QUEUE_TABLE} q
LEFT JOIN LIBRARY_META.REVIEW.V_LATEST_DECISIONS d
       ON d.lead_id = q.lead_id
WHERE q.lead_id = %s
"""

# The evidence payload comes from the SAFE view (never raw LEADS) —
# TITLE + the frozen EVIDENCE array the detector recorded.
EVIDENCE_SQL = """
SELECT title, TO_JSON(evidence) AS evidence_json, evidence_count
FROM LIBRARY_META."CONNECT".V_LEADS_PUBLISHED
WHERE lead_id = %s
"""

# Side-by-side source records for NPI leads:
#   LEIE_SQL  — every LEIE field for one NPI (the ban, source [2])
#   NPPES_SQL — the registry record for one NPI (the corroborating source [1])
LEIE_SQL = """
SELECT LASTNAME, FIRSTNAME, MIDNAME, EXCLTYPE, EXCLDATE, REINDATE,
       CITY, STATE, SPECIALTY, GENERAL, NPI, WVRSTATE
FROM LIBRARY_RAW.LANDING.FED_HHS_OIG_LEIE
WHERE REGEXP_REPLACE(NPI, '[^0-9]', '') = %s
LIMIT 10
"""

NPPES_SQL = """
SELECT NPI, PROVIDER_LAST_NAME_LEGAL_NAME, PROVIDER_FIRST_NAME,
       PROVIDER_MIDDLE_NAME, PROVIDER_CREDENTIAL_TEXT, ENTITY_TYPE_CODE,
       PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_CITY_NAME AS PRACTICE_CITY,
       PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME AS PRACTICE_STATE,
       NPI_DEACTIVATION_DATE, NPI_REACTIVATION_DATE
FROM LIBRARY_RAW.LANDING.FED_CMS_NPPES
WHERE NPI = %s
LIMIT 3
"""

# ---------------------------------------------------------------------------
# The write path — one parameterized INSERT, nothing else.
# ---------------------------------------------------------------------------
INSERT_DECISION_SQL = """
INSERT INTO LIBRARY_META.REVIEW.DECISIONS
    (TARGET_KIND, TARGET_ID, DECISION, REASON, REVIEWER, QUEUE_SNAPSHOT)
SELECT 'lead', %s, %s, %s, %s, PARSE_JSON(%s)
"""

# Post-insert confirmation reads the writer's OWN table grant (latest wins);
# the queue's anti-join uses V_LATEST_DECISIONS on the reader lane.
CONFIRM_DECISION_SQL = """
SELECT DECISION, REVIEWER, DECIDED_AT
FROM LIBRARY_META.REVIEW.DECISIONS
WHERE TARGET_KIND = 'lead' AND TARGET_ID = %s
QUALIFY ROW_NUMBER() OVER (PARTITION BY TARGET_ID ORDER BY DECIDED_AT DESC) = 1
"""


def decision_params(lead_id: str, button: str, reviewer: str, note: str,
                    queue_row: dict) -> tuple:
    """Map a button press to the INSERT bind params. Raises on an unknown
    button or blank reviewer — the caller shows the error, nothing writes."""
    verdict = VERDICTS.get(button)
    if verdict is None:
        raise ValueError(f"unknown button {button!r} — no write performed")
    if not (reviewer or "").strip():
        raise ValueError("reviewer name is required — no write performed")
    return (lead_id, verdict, (note or "").strip() or None, reviewer.strip(),
            snapshot_json(queue_row))


def snapshot_json(queue_row: dict) -> str:
    """QUEUE_SNAPSHOT: what the analyst was shown at decision time, so the
    decision stays interpretable after the queue is rebuilt."""
    keep = ("lead_id", "detector", "priority_rank", "priority_score",
            "headline", "confidence_tier", "receipt_verdict", "caveat")
    snap = {k: queue_row.get(k) for k in keep}
    return json.dumps(snap, default=str)
