{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_IHS_SCB_FACILITY') }}

),

keyed as (

    -- ASUFAC_CODE is NEAR-unique (8,731 distinct of 8,733 rows). The two
    -- collisions are genuinely distinct records, so a row_number() over the
    -- full-row hash is appended as a deterministic provenance tiebreaker to
    -- make scb_facility_id fully unique.
    select
        source.*,
        {{ dbt_utils.generate_surrogate_key(['ASUFAC_CODE']) }}
            || '-'
            || row_number() over (
                   partition by ASUFAC_CODE
                   order by hash(*)
               ) as scb_facility_id
    from source

),

renamed as (

    select

        -- identifiers
        scb_facility_id,
        trim(ASUFAC_CODE)                              as asufac_code,

        -- dimensions
        trim(AREA)                                     as area,
        trim(SERVICE_UNIT)                             as service_unit,
        trim(FACILITY)                                 as facility_name,
        nullif(trim(FACILITY_TYPE), '?')               as facility_type,
        nullif(trim(LOCATION_TYPE), '?')               as location_type,
        try_to_number(trim(BED_COUNT))                 as bed_count,
        trim(STATUS)                                   as status,
        nullif(trim(APC_FLAG), '?')                    as apc_flag,
        trim(ITU_CODE)                                 as itu_code,

        -- metadata
        to_timestamp_ntz(INGESTED_AT, 6)               as _ingested_at,
        SOURCE_RUN_ID                                  as _source_run_id,
        SRC_SHA256                                     as _src_sha256

    from keyed

)

select * from renamed
