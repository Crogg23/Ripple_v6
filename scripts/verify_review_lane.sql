-- ============================================================================
-- Verify the review write lane (CHRIS RUNS, in Snowsight, statement by
-- statement — NOT "Run All": statements [2]/[3] are DESIGNED to error and
-- Run All stops at the first error, leaving the wall half-proven).
--
-- THE "PERMISSION DENIED" FAILURES ARE THE POINT: they are the database
-- proving append-only. If [2], [3], or [4a/4b] SUCCEEDS, stop — the lane
-- is mis-provisioned; re-check the grants in provision_review_lane.sql.
--
-- SECONDARY ROLES: `USE ROLE` sets only the PRIMARY role — with secondary
-- roles active (Snowflake default is often ALL), your session would union
-- in ACCOUNTADMIN and every check below would "pass" wrongly. The clamp on
-- the next line makes this session test THE ROLE. The authoritative test is
-- the minted PAT itself (role-restricted PATs carry no secondary roles) —
-- re-run these statements over the PAT connection if in doubt.
-- ============================================================================

USE ROLE RIPPLE_REVIEW_WRITER;
USE SECONDARY ROLES NONE;
USE WAREHOUSE SERVE_WH;

-- [1] INSERT — expect: SUCCESS (1 row inserted)
INSERT INTO LIBRARY_META.REVIEW.DECISIONS
    (TARGET_KIND, TARGET_ID, DECISION, REVIEWER, REASON)
VALUES
    ('lead', 'SMOKE_TEST', 'needs_work', 'provisioning-check', 'delete-proof row');

-- [2] UPDATE — expect: PERMISSION DENIED  <- this failure is the point
UPDATE LIBRARY_META.REVIEW.DECISIONS
SET REASON = 'x'
WHERE TARGET_ID = 'SMOKE_TEST';

-- [3] DELETE — expect: PERMISSION DENIED  <- this failure is the point
DELETE FROM LIBRARY_META.REVIEW.DECISIONS
WHERE TARGET_ID = 'SMOKE_TEST';

-- [4a] The NEAREST wall — sibling schemas in the SAME database the role has
--      USAGE on. This is the exposure that matters; both must fail.
--      expect: not authorized
SELECT COUNT(*) FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY;
-- expect: not authorized (the claim table itself)
SELECT COUNT(*) FROM LIBRARY_META."CONNECT".LEADS;

-- [4b] Cross-database read — expect: does not exist / not authorized
SELECT COUNT(*) FROM LIBRARY_RAW.LANDING.FED_HHS_OIG_LEIE;

-- [5] The proof row is readable and stays forever (the app filters
--     TARGET_ID='SMOKE_TEST' out of every view) — expect: >= 1 row
SELECT DECISION_ID, TARGET_ID, DECISION, REVIEWER, DECIDED_AT
FROM LIBRARY_META.REVIEW.DECISIONS
WHERE TARGET_ID = 'SMOKE_TEST';
