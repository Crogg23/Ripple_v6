{{ config(materialized='table') }}

with base as (

    select * from {{ ref('stg_intl_ch_zefix__companies') }}

)

select

    -- key identifiers (exposed for cross-source joins)
    company_id,
    country,
    uid,
    ehraid,
    chid,

    -- descriptive attributes
    business_name,
    legal_form,
    seat,
    canton_rc,
    cantonal_excerpt,

    -- metadata
    _ingested_at,
    _source_run_id,

    -- audit columns
    current_timestamp()  as _mart_updated_at

from base
