{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_CFPB_HMDA_ARID2017_LEI_XREF') }}

),

renamed as (

    select

        -- identifiers
        trim(ARID_2017)                                  as arid_2017,
        trim(RESPONDENT_NAME)                            as respondent_name,

        -- LEI crosswalk (per reporting year)
        trim(LEI_2018)                                   as lei_2018,
        trim(LEI_2019)                                   as lei_2019,
        trim(LEI_2020)                                   as lei_2020,

        -- metadata
        to_timestamp_ntz(INGESTED_AT, 6)                 as _ingested_at,
        SOURCE_RUN_ID                                    as _source_run_id,
        SRC_SHA256                                       as _src_sha256

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by arid_2017
            order by _ingested_at desc
        ) as _row_num
    from renamed
    where arid_2017 is not null

)

select * exclude _row_num
from deduped
where _row_num = 1
