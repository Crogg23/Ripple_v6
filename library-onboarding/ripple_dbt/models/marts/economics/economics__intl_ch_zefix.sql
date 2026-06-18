{{ config(materialized='table') }}

with base as (

    select * from {{ ref('stg_intl_ch_zefix__companies') }}

)

select
    -- key identifiers (exposed for cross-source joins)
    company_id,
    uid,
    ehraid,
    chid,
    country,

    -- descriptive
    name,
    legal_form,
    status,

    -- address
    address_street,
    address_house_number,
    address_zip,
    address_city,
    address_canton,

    -- registration & publication
    registry_of_commerce,
    old_names,
    sogc_publication_date,
    mutation_type,
    community_bfs_id,

    -- metadata
    _ingested_at,
    _source_run_id

from base
