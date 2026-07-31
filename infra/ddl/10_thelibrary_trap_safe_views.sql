-- THE_LIBRARY trap-safe companion views (2026-07-30).
--
-- Two of the friendly, easy-to-query names in THE_LIBRARY quietly pointed at
-- a known data landmine documented in build-state.md's STANDING POLICY:
--   * PHARMA_PAYMENTS_TO_DOCTORS -> only the base Open Payments file (misses
--     the 2022 and 2023 supplemental years entirely; trap_open_payments_split)
--   * FEDERAL_CONTRACTS -> transaction-grain, not award-grain (a single award
--     repeats up to 174x; naive dollar sums overcount ~90x; trap_usaspending_grain)
-- Both underlying clean/correct versions already existed as dbt intermediate
-- models (int_open_payments_all_years, int_fed_usaspending__awards) but had
-- no friendly, easy-to-find name pointing at them. These two views ARE that
-- name. The original two friendly views are left untouched (something may
-- already depend on their exact shape) — these are additive, not replacements.
--
-- Idempotent: CREATE OR REPLACE VIEW, safe to re-run any time after the
-- underlying dbt intermediate models have been built
-- (dbt build --select int_open_payments_all_years int_fed_usaspending__awards).

CREATE OR REPLACE VIEW THE_LIBRARY.HEALTH.PHARMA_PAYMENTS_TO_DOCTORS_ALL_YEARS
COMMENT = 'Complete Open Payments (pharma/device industry payments to doctors), ALL years unioned -- base file + 2022 + 2023 supplemental files. PHARMA_PAYMENTS_TO_DOCTORS (no suffix) only covers the base file and silently undercounts by missing 2022/2023. Use this one for anything that needs the full picture.'
AS SELECT * FROM LIBRARY_STAGING.DBT_CROGERS.INT_OPEN_PAYMENTS_ALL_YEARS;

CREATE OR REPLACE VIEW THE_LIBRARY.GOVERNMENT_SPENDING.FEDERAL_CONTRACTS_BY_AWARD
COMMENT = 'Federal contracts rolled up to ONE ROW PER AWARD (not per transaction). FEDERAL_CONTRACTS is transaction-grain -- a single award can repeat up to 174x, and summing its dollar columns directly overcounts spend by roughly 90x. This view does the correct rollup: obligation dollars summed only from the incremental per-transaction field, cumulative snapshot fields taken via MAX not SUM. Use this one for any contractor/agency spend ranking.'
AS SELECT * FROM LIBRARY_STAGING.DBT_CROGERS.INT_FED_USASPENDING__AWARDS;
