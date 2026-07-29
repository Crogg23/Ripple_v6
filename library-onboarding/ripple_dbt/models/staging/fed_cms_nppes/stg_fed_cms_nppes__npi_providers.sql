{{ config(materialized='view') }}

with source as (

    select *
    from {{ source('ripple_raw', 'FED_CMS_NPPES') }}

),

deduped as (

    select *
    from source
    qualify row_number() over (
        partition by NPI
        order by _ingested_at desc
    ) = 1

)

-- EMPLOYER_IDENTIFICATION_NUMBER_EIN reads as 100% populated by a bare null
-- check, but is not wired as a spine key anywhere -- 2026-07-28 audit found it's
-- actually ~100% sentinel-masked (79.8% blank string, 20.2% the literal text
-- '<UNAVAIL>'). Nulling both here so a naive COUNT() never lies about this
-- column again, including for anyone who later wires EIN as a spine key.
select * replace (
    nullif(nullif(trim(EMPLOYER_IDENTIFICATION_NUMBER_EIN), ''), '<UNAVAIL>')
        as EMPLOYER_IDENTIFICATION_NUMBER_EIN
)
from deduped
