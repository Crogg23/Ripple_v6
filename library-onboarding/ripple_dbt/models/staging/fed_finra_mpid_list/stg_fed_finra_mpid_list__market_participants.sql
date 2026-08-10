{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_FINRA_MPID_LIST') }}

),

keyed as (

    -- The composite (MPID, MP_TYPE, NAME, LOCATION) is NEAR-unique (4,091
    -- distinct of 4,215 rows). Colliding rows are kept and disambiguated with
    -- a row_number() over the full-row hash appended as a deterministic
    -- provenance tiebreaker (fed_fjc_idb_civil idiom).
    select
        source.*,
        {{ dbt_utils.generate_surrogate_key(['MPID', 'MP_TYPE', 'NAME', 'LOCATION']) }}
            || '-'
            || row_number() over (
                   partition by MPID, MP_TYPE, NAME, LOCATION
                   order by hash(*)
               ) as mpid_record_id
    from source

),

renamed as (

    select

        mpid_record_id,
        trim(MPID)                                     as mpid,
        trim(MP_TYPE)                                  as mp_type,
        trim(NAME)                                     as name,
        trim(LOCATION)                                 as location,
        trim(TELEPHONE)                                as telephone,
        trim(NASDAQ_MEMBER)                            as nasdaq_member,
        trim(FINRA_MEMBER)                             as finra_member,
        trim(NASDAQ_BX_MEMBER)                         as nasdaq_bx_member,
        trim(PSX_PARTICIPANT)                          as psx_participant,
        INGESTED_AT                                    as _loaded_at,
        SOURCE_RUN_ID                                  as _source_run_id,
        SRC_SHA256                                     as _src_sha256

    from keyed

)

select * from renamed
