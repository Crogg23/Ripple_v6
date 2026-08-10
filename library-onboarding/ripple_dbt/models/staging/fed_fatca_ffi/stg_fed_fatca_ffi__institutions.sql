{{ config(materialized='view') }}

/*
  Hand-built 2026-08-09 (73-source backlog, wave 2). IRS FATCA Foreign
  Financial Institution (FFI) list: every foreign financial institution
  registered with the IRS for FATCA reporting, with its GIIN.
  Grain: one row = one registered institution; GIIN verified unique
  (516,298 = 516,298).
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_FATCA_FFI') }}
),

renamed as (
    select
        nullif(trim(GIIN), '')          as giin,
        nullif(trim(FI_NAME), '')       as institution_name,
        nullif(trim(COUNTRY_NAME), '')  as country_name,
        to_timestamp_ntz(INGESTED_AT, 6) as _ingested_at,
        nullif(trim(SOURCE_RUN_ID), '') as _source_run_id
    from source
)

select * from renamed
