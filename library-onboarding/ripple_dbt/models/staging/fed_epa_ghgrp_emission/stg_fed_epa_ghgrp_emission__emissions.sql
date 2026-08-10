{{ config(materialized='view') }}

/*
  Generated 2026-08-10 (backlog wave 4) from live-verified specs.
  EPA Greenhouse Gas Reporting Program: facility-level CO2e emissions by gas,
  sector, and subsector, 2010+.
  Grain: one row = one facility x year x sector x subsector x gas emission record.
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_EPA_GHGRP_EMISSION') }}
),

keyed as (
    -- The composite (FACILITY_ID, YEAR, SECTOR_ID, SUBSECTOR_ID, GAS_ID) is
    -- NEAR-unique (346,602 distinct of 346,683 rows; 81 collisions). The
    -- collisions are distinct records differing in other fields, so a
    -- row_number() over the full-row hash is appended as a deterministic
    -- provenance tiebreaker to make emission_record_id fully unique.
    select
        source.*,
        {{ dbt_utils.generate_surrogate_key(['FACILITY_ID', 'YEAR', 'SECTOR_ID', 'SUBSECTOR_ID', 'GAS_ID']) }}
            || '-'
            || row_number() over (
                   partition by FACILITY_ID, YEAR, SECTOR_ID, SUBSECTOR_ID, GAS_ID
                   order by hash(*)
               ) as emission_record_id
    from source
),

renamed as (
    select
        -- identifiers
        emission_record_id,
        try_to_number(trim(FACILITY_ID))                           as facility_id,
        try_to_number(trim(YEAR))                                  as reporting_year,
        try_to_number(trim(SECTOR_ID))                             as sector_id,
        try_to_number(trim(SUBSECTOR_ID))                          as subsector_id,
        try_to_number(trim(GAS_ID))                                as gas_id,

        -- measures
        try_to_number(trim(CO2E_EMISSION), 38, 10)                 as co2e_emission,

        -- metadata
        _ingested_at,
        _source_run_id
    from keyed
)

select * from renamed
