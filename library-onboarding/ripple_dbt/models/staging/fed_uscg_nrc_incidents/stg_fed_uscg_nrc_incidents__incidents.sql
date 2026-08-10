{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_USCG_NRC_INCIDENTS') }}

),

renamed as (

    select

        -- identifiers
        trim(SEQNOS)                                   as seqnos,

        -- dimensions
        trim(CALLTYPE)                                 as call_type,
        trim(RESPONSIBLE_COMPANY)                      as responsible_company,
        trim(RESPONSIBLE_ORG_TYPE)                     as responsible_org_type,
        trim(RESPONSIBLE_CITY)                         as responsible_city,
        trim(RESPONSIBLE_STATE)                        as responsible_state,
        trim(RESPONSIBLE_ZIP)                          as responsible_zip,
        trim(SOURCE)                                   as source,
        trim(SRC_YEAR)                                 as src_year,

        -- dates
        try_to_timestamp(trim(DATE_TIME_RECEIVED))     as date_time_received,
        try_to_timestamp(trim(DATE_TIME_COMPLETE))     as date_time_complete,

        -- metadata
        _INGESTED_AT                                   as _ingested_at,
        _SOURCE_RUN_ID                                 as _source_run_id,
        _SRC_SHA256                                    as _src_sha256

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by seqnos
            order by _ingested_at desc
        ) as _row_num
    from renamed
    where seqnos is not null

)

select
    seqnos,
    call_type,
    responsible_company,
    responsible_org_type,
    responsible_city,
    responsible_state,
    responsible_zip,
    source,
    src_year,
    date_time_received,
    date_time_complete,
    _ingested_at,
    _source_run_id,
    _src_sha256
from deduped
where _row_num = 1
