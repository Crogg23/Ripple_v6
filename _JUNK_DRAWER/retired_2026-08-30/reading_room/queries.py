"""ALL SQL for the Reading Room lives here — parameterized, bind variables
only. User input NEVER lands in SQL text (no f-strings over values); the
offline tests assert it.

Read surfaces: LIBRARY_MARTS.REVIEW.LEAD_QUEUE / CASE_QUEUE (Case Desk) /
COHORT_QUEUE (Pattern Desk), LIBRARY_META.REVIEW.V_EFFECTIVE_LEAD_DECISIONS
(decisions truth — lead-level, else inherited cohort-level),
LIBRARY_META.REVIEW.V_LATEST_COHORT_DECISIONS,
LIBRARY_META."CONNECT".V_LEADS_PUBLISHED (evidence payload — the SAFE view,
never raw LEADS), plus per-lead source-record pulls from LANDING.
Write surface: exactly two parameterized INSERTs into
LIBRARY_META.REVIEW.DECISIONS — TARGET_KIND hard-coded 'lead' or 'cohort' in
the SQL text, never app-supplied. Neither can write 'published'.
"""
from __future__ import annotations

import json

QUEUE_TABLE = "LIBRARY_MARTS.REVIEW.LEAD_QUEUE"
CASE_QUEUE_TABLE = "LIBRARY_MARTS.REVIEW.CASE_QUEUE"
COHORT_QUEUE_TABLE = "LIBRARY_MARTS.REVIEW.COHORT_QUEUE"
EFFECTIVE_DECISIONS_VIEW = "LIBRARY_META.REVIEW.V_EFFECTIVE_LEAD_DECISIONS"

# Case Desk detectors only: osha_cohort_outlier_2024 is reviewed on the
# Pattern Desk (cohort grain), and sanctioned_vessel_broadcasting v1 was
# retired to STATUS='stale' (audit F3 — all 4 leads duplicated v2).
DETECTORS = [
    "banned_but_paid",
    "excluded_but_billing",
    "banned_but_operating",
    "debarred_but_funded",
    "sanctioned_vessel_broadcasting_v2",
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
# 'published' (two-step gate, 2026-07-20) is decided-and-then-some — it must
# never re-enter the review queue. Since 2026-08-01 the anti-join reads the
# EFFECTIVE decision (lead-level, else inherited cohort-level) so a Pattern
# Desk verdict hides its member leads live, between mart rebuilds too.
_QUEUE_FILTER = (
    "COALESCE(d.decision, 'pending') NOT IN "
    "('confirmed', 'rejected', 'retracted', 'stale', 'published')"
)

# QUEUE_DEPTH is a COUNT(*) OVER() — computed over the full filtered set in
# THIS SAME query, before LIMIT truncates the rows returned. That makes the
# "showing N of depth" header an atomic snapshot instead of two separate
# round-trips that a concurrent decision could land between (the depth could
# previously disagree with the rows actually shown).
_QUEUE_SELECT = f"""
SELECT
    q.lead_id, q.detector, q.priority_rank, q.priority_score, q.headline,
    q.confidence_tier, q.receipt_verdict, q.caveat,
    d.decision AS latest_decision, d.decided_at AS latest_decided_at,
    COUNT(*) OVER () AS queue_depth
FROM {QUEUE_TABLE} q
LEFT JOIN {EFFECTIVE_DECISIONS_VIEW} d
       ON d.lead_id = q.lead_id
WHERE {_QUEUE_FILTER}
  AND q.detector NOT IN ('osha_cohort_outlier_2024',
                         'sanctioned_vessel_broadcasting')
"""


def queue_sql(detector: str | None = None, tier: str | None = None,
              limit: int = 20) -> tuple[str, tuple]:
    """Top-of-queue pull, with the full-filter depth riding along on every
    row (see QUEUE_DEPTH note above). Filters are optional; values are BOUND."""
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


CASE_SQL = f"""
SELECT q.*, d.decision AS latest_decision, d.reason AS latest_reason,
       d.reviewer AS latest_reviewer, d.decided_at AS latest_decided_at,
       d.decision_level AS latest_decision_level
FROM {QUEUE_TABLE} q
LEFT JOIN {EFFECTIVE_DECISIONS_VIEW} d
       ON d.lead_id = q.lead_id
WHERE q.lead_id = %s
"""

# Every reviewable lead about ONE person/entity (the Case Desk unit),
# best-first, each with its effective decision state.
PERSON_LEADS_SQL = f"""
SELECT q.*, d.decision AS latest_decision, d.reason AS latest_reason,
       d.reviewer AS latest_reviewer, d.decided_at AS latest_decided_at,
       d.decision_level AS latest_decision_level
FROM {QUEUE_TABLE} q
LEFT JOIN {EFFECTIVE_DECISIONS_VIEW} d
       ON d.lead_id = q.lead_id
WHERE q.entity_a_key_type = %s AND q.entity_a_key_value = %s
ORDER BY q.priority_score DESC, q.lead_id
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
# Scoped by REVIEWER too (not just TARGET_ID): DECISIONS is append-only and
# unscoped-by-reviewer, "latest row for this lead" can read back a DIFFERENT
# reviewer's concurrent verdict on the same lead and flash it as if it
# confirmed the current click. The caller must still compare the returned
# DECISION against the verdict it just wrote (this narrows, but cannot fully
# close, the case of the SAME reviewer double-clicking across two tabs).
CONFIRM_DECISION_SQL = """
SELECT DECISION, REVIEWER, DECIDED_AT
FROM LIBRARY_META.REVIEW.DECISIONS
WHERE TARGET_KIND = 'lead' AND TARGET_ID = %s AND REVIEWER = %s
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


# ===========================================================================
# The Case Desk — person/entity units over the hard-ID detectors.
# A unit stays in the queue while ANY of its member leads is undecided
# (effective decision, so a cohort verdict elsewhere never bleeds in here —
# these detectors have no cohorts).
# ===========================================================================

_CASE_QUEUE_SELECT = f"""
SELECT
    c.unit_id, c.unit_rank, c.unit_name, c.entity_a_key_type,
    c.entity_a_key_value, c.n_leads, c.detectors, c.best_tier,
    c.max_priority_score, c.n_needs_work, c.n_name_conflicts,
    c.top_lead_id, c.top_headline, c.lead_ids,
    COUNT(*) OVER () AS queue_depth
FROM {CASE_QUEUE_TABLE} c
WHERE EXISTS (
    SELECT 1
    FROM {QUEUE_TABLE} q
    LEFT JOIN {EFFECTIVE_DECISIONS_VIEW} d ON d.lead_id = q.lead_id
    WHERE q.entity_a_key_type = c.entity_a_key_type
      AND q.entity_a_key_value = c.entity_a_key_value
      AND {_QUEUE_FILTER}
)
"""


def case_queue_sql(detector: str | None = None, tier: str | None = None,
                   limit: int = 20) -> tuple[str, tuple]:
    """Top of the Case Desk queue (person/entity units). Filters are
    optional; values are BOUND. Detector filter = the unit has at least one
    lead from that detector; tier filter = the unit's best lead's tier."""
    sql, params = _CASE_QUEUE_SELECT, []
    if detector:
        sql += " AND ARRAY_CONTAINS(%s::VARIANT, c.detectors)"
        params.append(detector)
    if tier:
        sql += " AND c.best_tier = %s"
        params.append(tier)
    sql += " ORDER BY c.unit_rank LIMIT %s"
    params.append(int(limit))
    return sql, tuple(params)


# ===========================================================================
# The Pattern Desk — cohort-grain review of the statistical detector.
# The verdict target is the COHORT (TARGET_KIND='cohort'); member leads with
# no individual decision inherit it (specific-beats-general, enforced by
# LIBRARY_META.REVIEW.V_EFFECTIVE_LEAD_DECISIONS). Decided cohorts drop out;
# needs_work stays visible and flagged, same contract as leads.
# ===========================================================================

_COHORT_QUEUE_SELECT = f"""
SELECT
    c.cohort_id, c.priority_rank, c.priority_score, c.headline,
    c.naics, c.industry, c.size_band, c.cohort_n, c.cohort_pooled_dart,
    c.n_outliers, c.n_implausible, c.n_deaths_total, c.worst_fold,
    c.worst_fold_plausible, c.median_fold, c.states, c.n_rejoin_failures,
    c.n_needs_work, c.caveat,
    d.decision AS latest_decision, d.decided_at AS latest_decided_at,
    COUNT(*) OVER () AS queue_depth
FROM {COHORT_QUEUE_TABLE} c
LEFT JOIN LIBRARY_META.REVIEW.V_LATEST_COHORT_DECISIONS d
       ON d.cohort_id = c.cohort_id
WHERE {_QUEUE_FILTER}
"""


def cohort_queue_sql(limit: int = 20) -> tuple[str, tuple]:
    """Top of the Pattern Desk queue, depth riding along on every row."""
    return (_COHORT_QUEUE_SELECT
            + " ORDER BY c.priority_rank LIMIT %s"), (int(limit),)


COHORT_CASE_SQL = f"""
SELECT c.*, d.decision AS latest_decision, d.reason AS latest_reason,
       d.reviewer AS latest_reviewer, d.decided_at AS latest_decided_at
FROM {COHORT_QUEUE_TABLE} c
LEFT JOIN LIBRARY_META.REVIEW.V_LATEST_COHORT_DECISIONS d
       ON d.cohort_id = c.cohort_id
WHERE c.cohort_id = %s
"""

# receipts_sample carries lead_ids; the desk drills into any receipt via the
# existing CASE_SQL. This pulls the full member list when the analyst wants
# to page beyond the sample.
COHORT_MEMBERS_SQL = f"""
SELECT q.lead_id, q.headline, q.priority_rank, q.caveat,
       d.decision AS latest_decision, d.decision_level AS latest_decision_level
FROM {QUEUE_TABLE} q
LEFT JOIN {EFFECTIVE_DECISIONS_VIEW} d ON d.lead_id = q.lead_id
JOIN LIBRARY_META.REVIEW.V_LEAD_COHORT_MAP m ON m.lead_id = q.lead_id
WHERE m.cohort_id = %s
ORDER BY q.priority_rank
LIMIT %s
"""

# ---------------------------------------------------------------------------
# The cohort write path — one parameterized INSERT, TARGET_KIND is the
# HARD-CODED literal 'cohort' (never a bind param, mirroring the lead insert:
# app input can choose the verdict, never the kind). 'published' is not in
# VERDICTS, so no desk can ever write it — the two-step gate holds.
# ---------------------------------------------------------------------------
INSERT_COHORT_DECISION_SQL = """
INSERT INTO LIBRARY_META.REVIEW.DECISIONS
    (TARGET_KIND, TARGET_ID, DECISION, REASON, REVIEWER, QUEUE_SNAPSHOT)
SELECT 'cohort', %s, %s, %s, %s, PARSE_JSON(%s)
"""

# Read-back scoped by reviewer, same race semantics as CONFIRM_DECISION_SQL.
CONFIRM_COHORT_DECISION_SQL = """
SELECT DECISION, REVIEWER, DECIDED_AT
FROM LIBRARY_META.REVIEW.DECISIONS
WHERE TARGET_KIND = 'cohort' AND TARGET_ID = %s AND REVIEWER = %s
QUALIFY ROW_NUMBER() OVER (PARTITION BY TARGET_ID ORDER BY DECIDED_AT DESC) = 1
"""


def cohort_decision_params(cohort_id: str, button: str, reviewer: str,
                           note: str, cohort_row: dict) -> tuple:
    """Map a Pattern Desk button press to the INSERT bind params. Raises on
    an unknown button or blank reviewer — the caller shows the error, nothing
    writes. Same VERDICTS map as the Case Desk: confirm/reject/needs_work."""
    verdict = VERDICTS.get(button)
    if verdict is None:
        raise ValueError(f"unknown button {button!r} — no write performed")
    if not (reviewer or "").strip():
        raise ValueError("reviewer name is required — no write performed")
    return (cohort_id, verdict, (note or "").strip() or None, reviewer.strip(),
            cohort_snapshot_json(cohort_row))


def cohort_snapshot_json(cohort_row: dict) -> str:
    """QUEUE_SNAPSHOT for a cohort verdict: what the analyst saw, INCLUDING
    the blast radius (n_outliers = how many member leads the verdict covers
    unless individually decided)."""
    keep = ("cohort_id", "headline", "priority_rank", "priority_score",
            "naics", "industry", "size_band", "cohort_n", "n_outliers",
            "n_implausible", "worst_fold_plausible", "caveat")
    snap = {k: cohort_row.get(k) for k in keep}
    return json.dumps(snap, default=str)


# ---------------------------------------------------------------------------
# Portfolio header — one round trip, both desks' open workloads.
# ---------------------------------------------------------------------------
PORTFOLIO_SQL = f"""
SELECT
    (SELECT COUNT(*) FROM {CASE_QUEUE_TABLE})                    AS case_units,
    (SELECT COUNT(*) FROM {QUEUE_TABLE}
      WHERE detector NOT IN ('osha_cohort_outlier_2024',
                             'sanctioned_vessel_broadcasting')) AS case_leads,
    (SELECT COUNT(*) FROM {COHORT_QUEUE_TABLE})                  AS pattern_cohorts,
    (SELECT COALESCE(SUM(n_outliers), 0) FROM {COHORT_QUEUE_TABLE})
                                                                 AS pattern_leads
"""
