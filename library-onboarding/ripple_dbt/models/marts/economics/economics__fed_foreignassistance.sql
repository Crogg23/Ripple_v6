{{ config(materialized='table', schema='ECONOMICS') }}

-- GRAIN: one row per foreign assistance transaction

with source as (
    select * from {{ source('ripple_raw', 'FED_FOREIGNASSISTANCE') }}
)

select
    COUNTRY,
    MANAGING_AGENCY,
    FUNDING_AGENCY,
    USG_SECTOR,
    DAC_CATEGORY,
    OBLIGATION_AMOUNT,
    DISBURSEMENT_AMOUNT,
    FISCAL_YEAR,
    EIN,
    TRANSACTION_TYPE
from source
