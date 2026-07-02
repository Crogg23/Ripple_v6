{{ config(materialized='table') }}

with base as (

    select *
    from {{ ref('stg_fed_bjs_data__bjs_data_collections') }}

),

final as (

    select
        -- surrogate / natural keys exposed for cross-source joins
        fips_code                                        as fips,
        nacjd_id,

        -- collection metadata
        collection_name,
        topic,
        description,
        geographic_level,
        unit_of_enumeration,
        access_level,

        -- temporal
        publication_date,
        years_available,

        -- access / download
        download_url,
        data_tool_url,

        -- pipeline lineage
        _ingested_at,
        _source_run_id

    from base

)

select * from final
