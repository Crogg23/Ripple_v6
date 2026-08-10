{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_USGS_ORPHANED_OIL_GAS_WELLS') }}

),

keyed as (

    -- WELL_IDENTIFIER is NEAR-unique (117,669 distinct of 117,672 rows). The 3
    -- collisions are genuinely distinct records, not exact dupes, so a
    -- row_number() over the full-row hash is appended as a deterministic
    -- provenance tiebreaker (fed_fjc_idb_civil idiom).
    select
        source.*,
        {{ dbt_utils.generate_surrogate_key(['WELL_IDENTIFIER']) }}
            || '-'
            || row_number() over (
                   partition by WELL_IDENTIFIER
                   order by hash(*)
               ) as well_record_id
    from source

),

renamed as (

    select

        well_record_id,
        trim(WELL_IDENTIFIER)                          as well_identifier,
        trim(STATE)                                    as state,
        trim(COUNTY)                                   as county,
        trim(WELL_NAME)                                as well_name,
        trim(WELL_NUMBER)                              as well_number,
        trim(TYPE)                                     as type,
        trim(STATUS)                                   as status,
        try_to_number(trim(LATITUDE))                  as latitude,
        try_to_number(trim(LONGITUDE))                 as longitude,
        trim(PRIME_MERIDIAN)                           as prime_meridian,
        trim(TOWNSHIP)                                 as township,
        trim(T_DIR)                                    as t_dir,
        trim(RANGE)                                    as range,
        trim(R_DIR)                                    as r_dir,
        trim(SECTION)                                  as section,
        trim(QTR)                                      as qtr,
        trim(QTR_QTR)                                  as qtr_qtr,
        trim(QTR_QTR_QTR)                              as qtr_qtr_qtr,
        trim(SOURCE)                                   as source,
        try_to_date(trim(DATA_FILE_DATE), 'MM/DD/YYYY') as data_file_date,
        trim(WELL_INFO_NOTES)                          as well_info_notes,
        trim(LOCATION_NOTES)                           as location_notes,
        trim(OTHER_NOTES)                              as other_notes,
        INGESTED_AT                                    as _loaded_at,
        SOURCE_RUN_ID                                  as _source_run_id,
        SRC_SHA256                                     as _src_sha256

    from keyed

)

select * from renamed
