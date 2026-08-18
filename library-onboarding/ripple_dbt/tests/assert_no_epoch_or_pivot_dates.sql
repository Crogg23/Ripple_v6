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
--
-- Extended 2026-08-18 (epoch-1970 census follow-up, reports/census_grid_2026-08-12):
-- same mechanism, 3 more confirmed cases -- a fiscal-year number, a
-- precision-code enum, and a messy union-election date field all got fed to
-- a bare TRY_TO_DATE and epoch-mangled. Fixed with try_to_number() or
-- strict-format try_to_date(); guards added below so the shape can't return
-- silently. The CourtListener disclosure family's *_RAW columns (also part of
-- this batch) are OCR text, not dates, and are no longer cast at all -- no
-- date-shaped guard applies to them.

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

UNION ALL

-- action_date_fiscal_year is now try_to_number(), not a date -- guard that it
-- stays in a sane fiscal-year range (2000-2035). A number wildly outside this
-- band is the epoch-mangled-then-recast shape coming back some other way.
SELECT 'economics__fed_usaspending_contracts_full',
       'action_date_fiscal_year out of sane FY range', COUNT(*)
FROM {{ ref('economics__fed_usaspending_contracts_full') }}
WHERE action_date_fiscal_year IS NOT NULL
  AND (action_date_fiscal_year < 2000 OR action_date_fiscal_year > 2035)
HAVING COUNT(*) > 0

UNION ALL

SELECT 'economics__fed_irs_990_efile_index', 'sub_date epoch pile-up', COUNT(*)
FROM {{ ref('economics__fed_irs_990_efile_index') }}
WHERE sub_date = '1970-01-01'
HAVING COUNT(*) > 100

UNION ALL

SELECT 'economics__fed_irs_990_efile_index', 'sub_date in the future', COUNT(*)
FROM {{ ref('economics__fed_irs_990_efile_index') }}
WHERE sub_date > CURRENT_DATE()
HAVING COUNT(*) > 0

UNION ALL

-- date_prec is now try_to_number(), the UCDP precision code (1-5 per the
-- codebook). Anything outside that tiny domain means a date got in there again.
SELECT 'justice__intl_ucdp_ged', 'date_prec out of the 1-5 code domain', COUNT(*)
FROM {{ ref('justice__intl_ucdp_ged') }}
WHERE date_prec IS NOT NULL
  AND (date_prec < 1 OR date_prec > 5)
HAVING COUNT(*) > 0

UNION ALL

SELECT 'labor__fed_dol_olms', 'next_election_date epoch pile-up', COUNT(*)
FROM {{ ref('labor__fed_dol_olms') }}
WHERE next_election_date = '1970-01-01'
HAVING COUNT(*) > 100
