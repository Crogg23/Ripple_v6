{{ config(materialized='view') }}

-- LOADER DEFECT (documented, not fixable here): the spreadsheet title row was
-- consumed as the header, so the landing columns are the title
-- (IHS_TRIBAL_URBAN_INDIAN_HEALTH_FACILITIES_LIST_RELEASED_JUNE_2023) plus
-- UNNAMED_1..28, and the preamble rows + the real header row are embedded as
-- DATA rows. Columns are renamed POSITIONALLY onto the real header found in
-- the data, and preamble/header rows are filtered out by keeping only rows
-- whose first column is a numeric ASUFAC code.

with

source as (

    select * from {{ source('ripple_raw', 'FED_IHS_FACILITIES') }}
    -- keep only real facility rows (numeric ASUFAC in position 1); drops the
    -- embedded title / preamble / header rows
    where regexp_like(trim(IHS_TRIBAL_URBAN_INDIAN_HEALTH_FACILITIES_LIST_RELEASED_JUNE_2023), '^[0-9]+$')

),

keyed as (

    -- (asufac, asufac & modifier) is the natural grain but not pre-verified
    -- unique post-filter, so a row_number() over the full-row hash is appended
    -- as a deterministic provenance tiebreaker to make ihs_facility_id fully
    -- unique.
    select
        source.*,
        {{ dbt_utils.generate_surrogate_key(['IHS_TRIBAL_URBAN_INDIAN_HEALTH_FACILITIES_LIST_RELEASED_JUNE_2023', 'UNNAMED_1']) }}
            || '-'
            || row_number() over (
                   partition by IHS_TRIBAL_URBAN_INDIAN_HEALTH_FACILITIES_LIST_RELEASED_JUNE_2023, UNNAMED_1
                   order by hash(*)
               ) as ihs_facility_id
    from source

),

renamed as (

    select

        -- identifiers (positional rename onto the real embedded header)
        ihs_facility_id,
        trim(IHS_TRIBAL_URBAN_INDIAN_HEALTH_FACILITIES_LIST_RELEASED_JUNE_2023)
                                                       as asufac,
        trim(UNNAMED_1)                                as asufac_and_modifier,

        -- dimensions
        trim(UNNAMED_2)                                as area,
        trim(UNNAMED_3)                                as service_unit,
        trim(UNNAMED_4)                                as facility_name,
        trim(UNNAMED_5)                                as facility_type,
        trim(UNNAMED_6)                                as street,
        trim(UNNAMED_7)                                as city,
        trim(UNNAMED_8)                                as state,
        trim(UNNAMED_9)                                as zip,
        trim(UNNAMED_10)                               as phone,
        trim(UNNAMED_11)                               as facility_type_code,
        trim(UNNAMED_12)                               as apc_flag,
        trim(UNNAMED_13)                               as behavioral_health_flag,
        trim(UNNAMED_14)                               as dental_flag,
        trim(UNNAMED_15)                               as pharmacy_flag,
        try_to_number(trim(UNNAMED_16))                as workload,
        trim(UNNAMED_17)                               as status,
        trim(UNNAMED_18)                               as itu_code,
        trim(UNNAMED_19)                               as location_type,
        try_to_number(trim(UNNAMED_20))                as bed_count,
        trim(UNNAMED_21)                               as facility_operated_by,
        trim(UNNAMED_22)                               as facility_owned_by,
        trim(UNNAMED_23)                               as org_type,
        trim(UNNAMED_24)                               as type_of_provider,
        try_to_number(trim(UNNAMED_25), 12, 8)         as latitude,
        try_to_number(trim(UNNAMED_26), 12, 8)         as longitude,
        trim(UNNAMED_27)                               as website,
        trim(UNNAMED_28)                               as comments,

        -- metadata
        to_timestamp_ntz(INGESTED_AT, 6)               as _ingested_at,
        SOURCE_RUN_ID                                  as _source_run_id,
        SRC_SHA256                                     as _src_sha256

    from keyed

)

select * from renamed
