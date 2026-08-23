{{ config(materialized='table', schema='ECONOMICS') }}

-- GRAIN: one row per foreign assistance transaction
-- DEDUP (2026-08-11 verification): the landing load came from a runaway
-- generated pager (3.97M landed rows, 95,658 real, 97.6% exact duplicates).
-- Exact data rows are collapsed here so the mart is correct even before
-- the landing table itself is swapped clean.

with source as (
    select * from {{ source('ripple_raw', 'FED_FOREIGNASSISTANCE') }}
    qualify row_number() over (
        partition by COUNTRY, MANAGING_AGENCY, FUNDING_AGENCY, USG_SECTOR,
                     DAC_CATEGORY, OBLIGATION_AMOUNT, DISBURSEMENT_AMOUNT,
                     FISCAL_YEAR, EIN, TRANSACTION_TYPE
        order by _INGESTED_AT) = 1
)

select
    COUNTRY,
    MANAGING_AGENCY,
    FUNDING_AGENCY,
    USG_SECTOR,
    DAC_CATEGORY,
    OBLIGATION_AMOUNT,
    DISBURSEMENT_AMOUNT,
    {{ ripple_num('FISCAL_YEAR') }} as FISCAL_YEAR,
    EIN,
    TRANSACTION_TYPE
from source
