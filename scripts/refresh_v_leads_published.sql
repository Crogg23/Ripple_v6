-- ============================================================================
-- A12 — Refresh V_LEADS_PUBLISHED (CHRIS APPLIES, in Snowsight, as the view
-- owner / ACCOUNTADMIN). Idempotent; run top to bottom.
-- ============================================================================
-- WHY: the safe view was created 2026-07-03 with l.* — but COMPILED_SQL,
-- SQL_SHA256, AS_OF_DATE and SOURCE_SNAPSHOTS were ALTER-added to LEADS
-- later, and a view's star-list freezes at creation. Recreating the view
-- (same semantics, byte-identical filter logic) lets the star-list pick up
-- the receipt columns, so the enforced read lane can serve receipts and the
-- Reading Room LEAD_QUEUE mart can read evidence_sql from the SAFE view
-- instead of raw LEADS.
--
-- COPY GRANTS per POLICY copy_grants_library_meta: without it this rebuild
-- would silently strip RIPPLE_READER's SELECT. No new privileges are granted.
--
-- VERIFY (expected: one row, COMPILED_SQL):
--   SELECT COLUMN_NAME FROM LIBRARY_META.INFORMATION_SCHEMA.COLUMNS
--   WHERE TABLE_SCHEMA='CONNECT' AND TABLE_NAME='V_LEADS_PUBLISHED'
--     AND COLUMN_NAME='COMPILED_SQL';
-- ============================================================================

CREATE OR REPLACE VIEW LIBRARY_META."CONNECT".V_LEADS_PUBLISHED
COPY GRANTS
COMMENT = 'The SAFE way to read leads in SQL: published()-semantics as a view. Drops leads whose latest human verdict is rejected/retracted/stale, drops leads absent from the latest run (STATUS<>active), and stamps every survivor with REVIEW_STATE + PUBLISHED so an unreviewed lead can never read as fact. Built by the Investigator Instrument 2026-07-03; refreshed 2026-07-12 (A12) so the star-list includes the receipt columns (COMPILED_SQL etc.). Mirrors connect/leads.py published(). Regenerable.'
AS
WITH latest_verdict AS (
    SELECT TARGET_ID, DECISION
    FROM LIBRARY_META."CONNECT".DECISIONS
    WHERE TARGET_KIND = 'lead'
    QUALIFY ROW_NUMBER() OVER (PARTITION BY TARGET_ID ORDER BY DECIDED_AT DESC) = 1
)
SELECT
    l.*,
    COALESCE(v.DECISION, 'pending')                    AS REVIEW_STATE,
    COALESCE(v.DECISION, 'pending') = 'confirmed'      AS PUBLISHED
FROM LIBRARY_META."CONNECT".LEADS l
LEFT JOIN latest_verdict v ON v.TARGET_ID = l.LEAD_ID
WHERE COALESCE(l.STATUS, 'active') = 'active'
  AND COALESCE(v.DECISION, 'pending') NOT IN ('rejected', 'retracted', 'stale');
