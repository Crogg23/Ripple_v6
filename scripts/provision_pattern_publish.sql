-- ============================================================================
-- provision_pattern_publish.sql — make PATTERN-grain publishing safe & readable
-- (2026-08-01 ruling: the systemic pattern is the headline and publishes FIRST;
--  individual leads are receipts and publish separately, if ever.)
--
-- CHRIS runs this in Snowsight as ACCOUNTADMIN, AFTER provision_pattern_desk.sql.
-- Idempotent. Two parts:
--
--   Part 1  V_EFFECTIVE_LEAD_DECISIONS v2 — the inheritance guard.
--           Publishing a cohort must NOT flip its member leads to
--           PUBLISHED=TRUE in V_LEADS_PUBLISHED. An inherited cohort
--           'published' is downgraded to 'confirmed' at the lead grain, so the
--           original invariant ("published can only ever appear at
--           DECISION_LEVEL=lead") stays true even though cohorts can now
--           carry a 'published' row of their own.
--
--   Part 2  V_PATTERNS_PUBLISHED — the pattern-grain safe read: one row per
--           cohort whose latest verdict is 'published', with its verdict trail.
--           (Cohort stats — member counts, rates — live in the COHORT_QUEUE
--           mart; join on COHORT_ID when writing the story.)
--
-- VERIFY (run by hand after):
--   SELECT * FROM LIBRARY_META.REVIEW.V_PATTERNS_PUBLISHED;
--   -- after publishing a cohort, prove no member lead leaked to published:
--   SELECT COUNT(*) FROM LIBRARY_META."CONNECT".V_LEADS_PUBLISHED
--    WHERE PUBLISHED AND LEAD_ID IN (
--          SELECT LEAD_ID FROM LIBRARY_META.REVIEW.V_LEAD_COHORT_MAP
--           WHERE COHORT_ID = '<the cohort you published>');   -- expect 0
-- ============================================================================

-- ── Part 1: inheritance guard — cohort 'published' inherits as 'confirmed' ──

CREATE OR REPLACE VIEW LIBRARY_META.REVIEW.V_EFFECTIVE_LEAD_DECISIONS
COPY GRANTS
COMMENT = 'The effective verdict per lead: COALESCE(lead-level, inherited cohort-level). SPECIFIC BEATS GENERAL — a lead decision always wins for that lead; the cohort verdict fills in only where no lead decision exists. DECISION_LEVEL says which applied. A cohort-level published (scripts/publish_pattern.py) inherits DOWNGRADED to confirmed: published can only ever appear at DECISION_LEVEL=lead, so publishing a pattern never publishes its member leads. Leads with no decision at either level are absent (readers COALESCE to pending).'
AS
WITH base AS (
    SELECT l.LEAD_ID, m.COHORT_ID
    FROM LIBRARY_META."CONNECT".LEADS l
    LEFT JOIN LIBRARY_META.REVIEW.V_LEAD_COHORT_MAP m
           ON m.LEAD_ID = l.LEAD_ID
)
SELECT
    b.LEAD_ID,
    COALESCE(ld.DECISION,
             -- the guard: an inherited cohort 'published' is only a confirm
             -- at the lead grain (the pattern is the headline; the member is
             -- a receipt that still needs its own publish_lead.py pass).
             IFF(cd.DECISION = 'published', 'confirmed', cd.DECISION))
                                                AS DECISION,
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

-- ── Part 2: the pattern-grain safe read ─────────────────────────────────────

CREATE OR REPLACE VIEW LIBRARY_META.REVIEW.V_PATTERNS_PUBLISHED
COPY GRANTS
COMMENT = 'The SAFE way to read published PATTERNS: one row per cohort whose latest human verdict is published (written only by scripts/publish_pattern.py after a Pattern Desk confirm — same two-step gate as leads). Member leads are NOT published by this; see V_EFFECTIVE_LEAD_DECISIONS. Join COHORT_ID to the COHORT_QUEUE mart for cohort stats. Regenerable.'
AS
SELECT
    cd.COHORT_ID,
    cd.REASON       AS PUBLISH_REASON,
    cd.REVIEWER     AS PUBLISHED_BY,
    cd.DECIDED_AT   AS PUBLISHED_AT
FROM LIBRARY_META.REVIEW.V_LATEST_COHORT_DECISIONS cd
WHERE cd.DECISION = 'published';

-- ── Grants ──────────────────────────────────────────────────────────────────

GRANT SELECT ON VIEW LIBRARY_META.REVIEW.V_PATTERNS_PUBLISHED TO ROLE RIPPLE_READER;
