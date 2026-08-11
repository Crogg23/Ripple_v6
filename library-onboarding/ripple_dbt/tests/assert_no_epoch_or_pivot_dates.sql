-- Date-cast guard (verification 2026-08-11, defect class: epoch sentinels and
-- century pivots). Two real failures motivated this:
--   1. Year-only birth-date strings ('1997') fed to a bare TRY_TO_DATE were
--      read as epoch SECONDS, piling ~6.8k sanctions targets onto 1970-01-01.
--   2. Two-digit source years ('2-Jan-59') pivoted forward, putting biologics
--      APPROVAL dates in 2059-2069 - the past parsed as the future.
-- This test fails the build if either shape ever comes back:
--   - a suspicious concentration (>100 rows) on exactly 1970-01-01, or
--   - any row where a can't-be-future date column is after today.
-- Returns the offending groups.

SELECT 'justice__intl_opensanctions' AS model,
       'birth_date epoch pile-up'    AS defect,
       COUNT(*)                      AS n
FROM {{ ref('justice__intl_opensanctions') }}
WHERE birth_date = '1970-01-01'
HAVING COUNT(*) > 100

UNION ALL

SELECT 'justice__intl_opensanctions', 'birth_date in the future', COUNT(*)
FROM {{ ref('justice__intl_opensanctions') }}
WHERE birth_date > CURRENT_DATE()
HAVING COUNT(*) > 0

UNION ALL

-- COT data starts decades after 1970 but the series holds nothing older
-- than 1986; any pre-1980 parse is the epoch bug back again.
SELECT 'education__fed_cftc_cot_futures', 'report date epoch pile-up', COUNT(*)
FROM {{ ref('education__fed_cftc_cot_futures') }}
WHERE as_of_date_in_form_yymmdd < '1980-01-01'
HAVING COUNT(*) > 0

UNION ALL

SELECT 'education__fed_cftc_cot_financial', 'report date epoch pile-up', COUNT(*)
FROM {{ ref('education__fed_cftc_cot_financial') }}
WHERE as_of_date_in_form_yymmdd < '1980-01-01'
HAVING COUNT(*) > 0

UNION ALL

SELECT 'stg_fed_fda_purple_book__licenses', 'approval date in the future', COUNT(*)
FROM {{ ref('stg_fed_fda_purple_book__licenses') }}
WHERE approval_date > CURRENT_DATE()
   OR interchangeable_approval_date > CURRENT_DATE()
   OR date_of_first_licensure > CURRENT_DATE()
HAVING COUNT(*) > 0
