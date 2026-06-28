{{ config(materialized='view') }}

-- ============================================================================
-- THE #1 OPEN PAYMENTS TRAP FIX (2026-06-27 discovery sweep, findings #23/#21)
-- ============================================================================
-- FED_CMS_OPEN_PAYMENTS is NOT "all years" -- it is 2024-ONLY (15,385,047 rows,
-- 100% PROGRAM_YEAR=2024, MIN=MAX=2024). FED_CMS_OPEN_PAYMENTS_2023 is the
-- 2023-only sibling (14,700,786 rows, 100% PROGRAM_YEAR=2023). The unsuffixed
-- base name is a half-the-data landmine: anything pointed at it silently reports
-- only ~51% of 2023-2024 payment volume, and the ~338 LEIE x Open Payments leads
-- that hit the unsuffixed table are missing all of 2023.
--
-- WHY A UNION ALL IS SAFE (not a double-count):
--   * RECORD_ID is CMS's hard unique payment key. Verified live:
--       - 2024: 15,385,047 rows = 15,385,047 distinct RECORD_IDs (0 dupes)
--       - 2023: 14,700,786 rows = 14,700,786 distinct RECORD_IDs (0 dupes)
--       - INTERSECT of RECORD_IDs across the two tables = 0 (record-disjoint).
--     So RECORD_ID is globally unique ACROSS years -> UNION ALL cannot
--     double-count, and the unioned record_id stays a true primary key.
--   * Both tables are IDENTICAL 94-column schemas: same column names, same
--     ordinal positions, zero differences (verified via INFORMATION_SCHEMA).
--     That makes `select *` UNION-compatible and position-aligned -- no need
--     for an explicit aligned column list.
--   * PROGRAM_YEAR already distinguishes the years (2024 vs 2023), so NO
--     synthetic year column is added.
--
-- DESIGN: thin passthrough VIEW (no casting). This is the canonical all-years
-- model every Open Payments detector should point at INSTEAD of the raw
-- unsuffixed landing table. Detectors cast TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS,
-- NPI, dates, etc. as needed downstream (see findings #8/#40/#75 -- the
-- $124.99/$125 meal-cap clusters and the just-below-$125 threshold fingerprint
-- live in this combined population; this model is the correct base for them).
--
-- GOTCHA preserved for downstream casters (do NOT "fix" here -- raw passthrough):
--   * DATE_OF_PAYMENT carries 73 garbage values like '11/30/0002' in the 2024
--     table. PROGRAM_YEAR (not DATE_OF_PAYMENT) is the reliable year partition.
--   * TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS is TEXT; 100% castable to DOUBLE with
--     0 blanks in both tables, but cast with try_to_double downstream anyway.
-- ============================================================================

select * from {{ source('ripple_raw', 'FED_CMS_OPEN_PAYMENTS') }}

union all

select * from {{ source('ripple_raw', 'FED_CMS_OPEN_PAYMENTS_2023') }}

union all

-- 2022 backfill (discovery sweep #23, landed 2026-06-28). Same 94-col schema,
-- record-disjoint by RECORD_ID -> still dup-safe. Turns the union into a true
-- 3-year (2022-2024) time series for the meal-cap / $125-threshold trend work.
select * from {{ source('ripple_raw', 'FED_CMS_OPEN_PAYMENTS_2022') }}
