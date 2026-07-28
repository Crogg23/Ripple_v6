{{ config(materialized='table', schema='ECONOMICS') }}

-- GRAIN: one row per foreign assistance record
-- Answers: Where does US foreign aid money go, how much, for what purpose?
-- Source: ForeignAssistance.gov (~3.97M records)
-- Key joins: country → geography; implementing_agency → government entities

with source as (
    select * from {{ source('ripple_raw', 'FED_FOREIGNASSISTANCE') }}
)

select
    trim("FISCAL_YEAR") as fiscal_year,
    trim("FUNDING_AGENCY_NAME") as funding_agency,
    trim("IMPLEMENTING_AGENCY_NAME") as implementing_agency,
    trim("ACTIVITY_NAME") as activity_name,
    trim("COUNTRY_NAME") as country_name,
    trim("DAC_SECTOR_NAME") as dac_sector,
    trim("CATEGORY_NAME") as category_name,
    trim("ASSISTANCE_CATEGORY_NAME") as assistance_category,
    try_to_double("CONSTANT_AMOUNT") as constant_amount,
    try_to_double("CURRENT_AMOUNT") as current_amount,
    trim("TRANSACTION_TYPE_NAME") as transaction_type,
    "_INGESTED_AT" as _loaded_at,
    "_SOURCE_RUN_ID" as _source_run_id
from source
qualify row_number() over (
    partition by "FISCAL_YEAR", "FUNDING_AGENCY_NAME", "ACTIVITY_NAME", "COUNTRY_NAME"
    order by "_INGESTED_AT" desc
) = 1
