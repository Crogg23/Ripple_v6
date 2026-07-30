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
--
-- The 5 *_DATE columns land as TEXT in MM/DD/YYYY format (blank string, not
-- NULL, when absent) -- these are the only unambiguous date/numeric columns in
-- the 333-column NPPES schema; everything else (NPI, taxonomy/license codes,
-- names, addresses) is a genuine identifier or free text and stays TEXT on
-- purpose so leading zeros and formatting survive.
select * replace (
    nullif(nullif(trim(EMPLOYER_IDENTIFICATION_NUMBER_EIN), ''), '<UNAVAIL>')
        as EMPLOYER_IDENTIFICATION_NUMBER_EIN,
    try_to_date(PROVIDER_ENUMERATION_DATE, 'MM/DD/YYYY') as PROVIDER_ENUMERATION_DATE,
    try_to_date(LAST_UPDATE_DATE, 'MM/DD/YYYY') as LAST_UPDATE_DATE,
    try_to_date(NPI_DEACTIVATION_DATE, 'MM/DD/YYYY') as NPI_DEACTIVATION_DATE,
    try_to_date(NPI_REACTIVATION_DATE, 'MM/DD/YYYY') as NPI_REACTIVATION_DATE,
    try_to_date(CERTIFICATION_DATE, 'MM/DD/YYYY') as CERTIFICATION_DATE
)
from deduped
