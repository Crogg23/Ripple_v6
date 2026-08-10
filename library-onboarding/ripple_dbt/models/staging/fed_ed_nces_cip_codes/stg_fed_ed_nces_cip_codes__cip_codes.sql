{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_ED_NCES_CIP_CODES') }}

),

renamed as (

    select

        -- identifiers
        -- codes arrive Excel-armored as ="01.0000" — strip the =" wrapper
        trim(CIPCODE, ' ="')                           as cip_code,
        trim(CIPFAMILY, ' ="')                         as cip_family,

        -- dimensions
        trim(CIPTITLE)                                 as cip_title,
        trim(CIPDEFINITION)                            as cip_definition,
        trim(ACTION)                                   as action,
        trim(TEXTCHANGE)                               as text_change,
        trim(CROSSREFERENCES)                          as cross_references,
        trim(EXAMPLES)                                 as examples,

        -- metadata (INGESTED_AT is a NUMBER epoch in microseconds)
        to_timestamp_ntz(INGESTED_AT, 6)               as _loaded_at,
        SOURCE_RUN_ID                                  as _source_run_id,
        SRC_SHA256                                     as _src_sha256

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by cip_code
            order by _loaded_at desc
        ) as _row_num
    from renamed
    where cip_code is not null

)

select * exclude (_row_num)
from deduped
where _row_num = 1
