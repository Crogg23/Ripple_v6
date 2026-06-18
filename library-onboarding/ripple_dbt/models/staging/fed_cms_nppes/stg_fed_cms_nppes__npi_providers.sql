{{ config(materialized='view') }}

with source as (

    select *
    from {{ source('ripple_raw', 'FED_CMS_NPPES') }}

),

deduped as (

    select *
    from source
    qualify row_number() over (
        partition by NPI
        order by _ingested_at desc
    ) = 1

)

select *
from deduped
