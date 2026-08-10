{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_MSRB_REGISTRANTS') }}

),

renamed as (

    select

        trim(MSRB_ID) || '-' || trim(REGISTRANT_TYPE)  as msrb_registrant_id,
        trim(FIRM_NAME)                                as firm_name,
        trim(MSRB_ID)                                  as msrb_id,
        trim(STATE)                                    as state,
        trim(REGISTRANT_TYPE)                          as registrant_type,
        INGESTED_AT                                    as _loaded_at,
        SOURCE_RUN_ID                                  as _source_run_id,
        SRC_SHA256                                     as _src_sha256

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by msrb_registrant_id
            order by _loaded_at desc
        ) as _row_num
    from renamed
    where msrb_registrant_id is not null

)

select * exclude (_row_num) from deduped
where _row_num = 1
