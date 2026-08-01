-- ============================================================================
-- A15 — Provision the Pattern Desk decision lane (CHRIS APPLIES, in Snowsight,
-- as ACCOUNTADMIN, top to bottom; every statement is idempotent or
-- CREATE OR REPLACE ... COPY GRANTS). Companion to provision_review_lane.sql
-- (A14) — run AFTER it; requires LIBRARY_META.REVIEW.DECISIONS to exist.
-- ============================================================================
-- WHAT THIS BUILDS (Reading Room v2, two-desk redesign, 2026-08-01)
--   Part 1  V_LATEST_DECISIONS v2 — same view, deterministic tie-break
--           (DECIDED_AT ties were previously non-deterministic).
--   Part 2  V_LATEST_COHORT_DECISIONS — latest verdict per COHORT
--           (TARGET_KIND='cohort', TARGET_ID = naics||'|'||size_band).
--   Part 3  V_LEAD_COHORT_MAP — lead_id -> cohort_id for the OSHA cohort
--           detector, derived from the frozen evidence.
--   Part 4  V_EFFECTIVE_LEAD_DECISIONS — the inheritance truth:
--           COALESCE(lead verdict, cohort verdict). SPECIFIC BEATS GENERAL:
--           a lead-level decision always wins for that lead; the cohort
--           verdict fills in only for members with no individual decision.
--           'published' can only arrive at DECISION_LEVEL='lead' by
--           construction — cohort verdicts can never publish anything.
--   Part 5  V_LEADS_PUBLISHED v3 — reads the effective view (replacing its
--           inline latest-verdict CTE): a cohort rejection now suppresses
--           member leads; a cohort confirm marks them confirmed (nomination
--           only — the two-step publish gate is untouched); needs_work stays
--           visible and flagged at both levels.
--   Part 6  Retire the superseded sanctioned_vessel_broadcasting v1 leads
--           (audit F3: all 4 duplicate v2 leads on the same hulls) via
--           STATUS='stale' — the safe view already drops non-active leads;
--           the append-only DECISIONS table is not touched.
--   Part 7  Grants: new views + the three review marts to RIPPLE_READER
--           (also fixes the stale DBT_CROGERS grant from
--           provision_review_lane.sql line 223 — the mart moved to the
--           REVIEW schema).
--
-- DESIGN RULINGS (Chris, 2026-08-01 — recorded in CHRIS_DECISIONS.md)
--   * Pattern-desk cohort review is REVIEW, not publishing: it does not
--     breach POLICY foundation_before_detectives (which defers the publishing
--     layer). Cohort verdicts cannot produce 'published'.
--   * Inheritance precedence is specific-beats-general (COALESCE), NOT
--     latest-timestamp-wins-across-kinds: a later blanket cohort verdict must
--     never silently override a deliberate per-lead exception.
--
-- VERIFY (copy out and run by hand — comments, so Run All never executes):
--   -- v1 vessel leads gone from the safe view (expect 0):
--   SELECT COUNT(*) FROM LIBRARY_META."CONNECT".V_LEADS_PUBLISHED
--     WHERE RULE_NAME = 'sanctioned_vessel_broadcasting';
--   -- every reviewable OSHA lead maps to a cohort (expect 0):
--   SELECT COUNT(*) FROM LIBRARY_META.REVIEW.V_LEAD_COHORT_MAP
--     WHERE COHORT_ID IS NULL;
--   -- inheritance smoke (AFTER writing a needs_work cohort verdict via the
--   -- Pattern Desk): members with no lead decision inherit it (expect > 0):
--   SELECT COUNT(*) FROM LIBRARY_META.REVIEW.V_EFFECTIVE_LEAD_DECISIONS
--     WHERE DECISION_LEVEL = 'cohort' AND DECISION = 'needs_work';
-- ============================================================================

-- ── Part 1: V_LATEST_DECISIONS v2 — deterministic tie-break ────────────────
-- DECIDED_AT defaults to CURRENT_TIMESTAMP(); two rows in one second tied
-- non-deterministically. DECISION_ID (UUID) breaks the tie stably.

CREATE OR REPLACE VIEW LIBRARY_META.REVIEW.V_LATEST_DECISIONS
COPY GRANTS
COMMENT = 'Latest verdict per lead (append-only means corrections are new rows; this view is the truth). SMOKE_TEST excluded. LEAD_ID aliased for the Reading Room app. Tie-break on DECISION_ID (deterministic) since 2026-08-01.'
AS
SELECT
    TARGET_ID                                   AS LEAD_ID,
    DECISION,
    REASON,
    REVIEWER,
    QUEUE_SNAPSHOT,
    DECIDED_AT,
    DECISION_ID
FROM LIBRARY_META.REVIEW.DECISIONS
WHERE TARGET_KIND = 'lead'
  AND TARGET_ID != 'SMOKE_TEST'
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY TARGET_ID ORDER BY DECIDED_AT DESC, DECISION_ID DESC) = 1;

-- ── Part 2: latest COHORT verdicts ─────────────────────────────────────────

CREATE OR REPLACE VIEW LIBRARY_META.REVIEW.V_LATEST_COHORT_DECISIONS
COPY GRANTS
COMMENT = 'Latest verdict per cohort (Pattern Desk; TARGET_KIND=cohort, TARGET_ID = naics||''|''||size_band). SMOKE_TEST excluded. Same append-only, latest-wins, deterministic tie-break semantics as V_LATEST_DECISIONS.'
AS
SELECT
    TARGET_ID                                   AS COHORT_ID,
    DECISION,
    REASON,
    REVIEWER,
    QUEUE_SNAPSHOT,
    DECIDED_AT,
    DECISION_ID
FROM LIBRARY_META.REVIEW.DECISIONS
WHERE TARGET_KIND = 'cohort'
  AND TARGET_ID != 'SMOKE_TEST'
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY TARGET_ID ORDER BY DECIDED_AT DESC, DECISION_ID DESC) = 1;

-- ── Part 3: lead -> cohort map ─────────────────────────────────────────────
-- Reads raw LEADS inside LIBRARY_META provisioning — the same trust zone that
-- defines V_LEADS_PUBLISHED itself; consumers only ever see it through the
-- effective-decisions view below. The cohort key derivation must stay
-- IDENTICAL to cohort_queue.sql (naics||'|'||size_band from evidence[0]).

CREATE OR REPLACE VIEW LIBRARY_META.REVIEW.V_LEAD_COHORT_MAP
COPY GRANTS
COMMENT = 'lead_id -> cohort_id (naics||''|''||size_band from frozen evidence) for the osha_cohort_outlier_2024 detector. The join spine of Pattern Desk decision inheritance.'
AS
SELECT
    LEAD_ID,
    EVIDENCE[0]:naics::STRING || '|' || EVIDENCE[0]:size_band::STRING
                                                AS COHORT_ID
FROM LIBRARY_META."CONNECT".LEADS
WHERE RULE_NAME = 'osha_cohort_outlier_2024';

-- ── Part 4: the inheritance truth ──────────────────────────────────────────

CREATE OR REPLACE VIEW LIBRARY_META.REVIEW.V_EFFECTIVE_LEAD_DECISIONS
COPY GRANTS
COMMENT = 'The effective verdict per lead: COALESCE(lead-level, inherited cohort-level). SPECIFIC BEATS GENERAL — a lead decision always wins for that lead; the cohort verdict fills in only where no lead decision exists. DECISION_LEVEL says which applied. published can only ever appear at DECISION_LEVEL=lead (cohort verdicts cannot publish). Leads with no decision at either level are absent (readers COALESCE to pending).'
AS
WITH base AS (
    SELECT l.LEAD_ID, m.COHORT_ID
    FROM LIBRARY_META."CONNECT".LEADS l
    LEFT JOIN LIBRARY_META.REVIEW.V_LEAD_COHORT_MAP m
           ON m.LEAD_ID = l.LEAD_ID
)
SELECT
    b.LEAD_ID,
    COALESCE(ld.DECISION,   cd.DECISION)        AS DECISION,
    COALESCE(ld.REASON,     cd.REASON)          AS REASON,
    COALESCE(ld.REVIEWER,   cd.REVIEWER)        AS REVIEWER,
    COALESCE(ld.DECIDED_AT, cd.DECIDED_AT)      AS DECIDED_AT,
    IFF(ld.LEAD_ID IS NOT NULL, 'lead', 'cohort')
                                                AS DECISION_LEVEL,
    b.COHORT_ID
FROM base b
LEFT JOIN LIBRARY_META.REVIEW.V_LATEST_DECISIONS ld
       ON ld.LEAD_ID = b.LEAD_ID
LEFT JOIN LIBRARY_META.REVIEW.V_LATEST_COHORT_DECISIONS cd
       ON cd.COHORT_ID = b.COHORT_ID
WHERE ld.LEAD_ID IS NOT NULL
   OR cd.COHORT_ID IS NOT NULL;

-- ── Part 5: V_LEADS_PUBLISHED v3 — reads the effective view ────────────────
-- Same published() semantics as v2 (provision_review_lane.sql Part 3b), with
-- the inline latest-verdict CTE replaced by V_EFFECTIVE_LEAD_DECISIONS so
-- cohort verdicts inherit. The two-step publish gate is UNCHANGED: PUBLISHED
-- still requires an explicit lead-level 'published' verdict, which the
-- effective view can only ever carry at DECISION_LEVEL='lead'.

CREATE OR REPLACE VIEW LIBRARY_META."CONNECT".V_LEADS_PUBLISHED
COPY GRANTS
COMMENT = 'The SAFE way to read leads in SQL: published()-semantics as a view. Drops leads whose latest EFFECTIVE human verdict (lead-level, else inherited cohort-level — see LIBRARY_META.REVIEW.V_EFFECTIVE_LEAD_DECISIONS) is rejected/retracted/stale, drops leads absent from the latest run (STATUS<>active), and stamps every survivor with REVIEW_STATE + PUBLISHED so an unreviewed lead can never read as fact. Two-step publish gate unchanged. Regenerable.'
AS
SELECT
    l.*,
    COALESCE(v.DECISION, 'pending')                    AS REVIEW_STATE,
    -- Two-step gate (2026-07-20, beta ruling B1): Confirm = private nomination.
    -- PUBLISHED needs an explicit lead-level 'published' verdict
    -- (scripts/publish_lead.py, which refuses unless the latest verdict is
    -- 'confirmed'). Cohort inheritance cannot produce it.
    COALESCE(v.DECISION, 'pending') = 'published'      AS PUBLISHED
FROM LIBRARY_META."CONNECT".LEADS l
LEFT JOIN LIBRARY_META.REVIEW.V_EFFECTIVE_LEAD_DECISIONS v
       ON v.LEAD_ID = l.LEAD_ID
WHERE COALESCE(l.STATUS, 'active') = 'active'
  AND COALESCE(v.DECISION, 'pending') NOT IN ('rejected', 'retracted', 'stale');

-- ── Part 6: retire the superseded v1 vessel detector (audit F3) ────────────
-- All 4 sanctioned_vessel_broadcasting leads duplicate v2 leads on the same
-- IMO hulls; the caveat has called the detector SUPERSEDED since it shipped.
-- STATUS='stale' drops them from the safe view (and so from every mart and
-- queue) without touching the append-only DECISIONS table. Idempotent.

UPDATE LIBRARY_META."CONNECT".LEADS
   SET STATUS = 'stale'
 WHERE RULE_NAME = 'sanctioned_vessel_broadcasting'
   AND COALESCE(STATUS, 'active') = 'active';

-- ── Part 7: grants ─────────────────────────────────────────────────────────

GRANT SELECT ON VIEW LIBRARY_META.REVIEW.V_LATEST_COHORT_DECISIONS TO ROLE RIPPLE_READER;
GRANT SELECT ON VIEW LIBRARY_META.REVIEW.V_LEAD_COHORT_MAP         TO ROLE RIPPLE_READER;
GRANT SELECT ON VIEW LIBRARY_META.REVIEW.V_EFFECTIVE_LEAD_DECISIONS TO ROLE RIPPLE_READER;

-- The review-writer lane confirms its own cohort write via read-back; it
-- already holds SELECT on DECISIONS (the table), which is sufficient — no
-- new writer grants are needed or wanted.

-- ── Part 8 (LAST, may error harmlessly before the first build_review run) ──
-- The three review marts live in LIBRARY_MARTS.REVIEW (custom dbt schema
-- routing). This corrects provision_review_lane.sql's stale line-223 grant,
-- which pointed at LIBRARY_MARTS.DBT_CROGERS (the pre-routing location).
-- copy_grants=true on the models keeps these across dbt rebuilds. If any
-- line errors with 'does not exist', run build_review first, then re-run
-- just these three lines.

GRANT USAGE ON SCHEMA LIBRARY_MARTS.REVIEW TO ROLE RIPPLE_READER;
GRANT SELECT ON TABLE LIBRARY_MARTS.REVIEW.LEAD_QUEUE   TO ROLE RIPPLE_READER;
GRANT SELECT ON TABLE LIBRARY_MARTS.REVIEW.COHORT_QUEUE TO ROLE RIPPLE_READER;
GRANT SELECT ON VIEW  LIBRARY_MARTS.REVIEW.CASE_QUEUE   TO ROLE RIPPLE_READER;
