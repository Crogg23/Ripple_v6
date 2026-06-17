{{ config(materialized='view') }}

with source as (

    select * from {{ source('ripple_raw', 'INTL_CH_ZEFIX') }}

),

renamed as (

    select

        -- primary / surrogate key
        {{ dbt_utils.generate_surrogate_key(['UID', 'BUSINESS_NAME', 'CANTON_RC']) }} as company_id,

        -- hard-coded country for cross-source joins
        'CH'                                        as country,

        -- identifiers
        nullif(trim(UID), '')                        as uid,
        nullif(trim(CANTONAL_EXCERPT), '')           as ehraid,
        nullif(trim(CANTONAL_EXCERPT), '')           as chid,

        -- core attributes
        nullif(trim(BUSINESS_NAME), '')              as business_name,
        nullif(trim(LEGAL_FORM), '')                 as legal_form,
        nullif(trim(SEAT), '')                       as seat,
        nullif(trim(CANTON_RC), '')                  as canton_rc,
        nullif(trim(CANTONAL_EXCERPT), '')           as cantonal_excerpt,

        -- metadata
        _ingested_at,
        _source_run_id

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by uid, business_name, canton_rc
            order by _ingested_at desc
        ) as _row_num
    from renamed

)

select
    company_id,
    country,
    uid,
    ehraid,
    chid,
    business_name,
    legal_form,
    seat,
    canton_rc,
    cantonal_excerpt,
    _ingested_at,
    _source_run_id
from deduped
where _row_num = 1
