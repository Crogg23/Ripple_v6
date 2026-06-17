{{ config(materialized='table') }}

with base as (

    select * from {{ ref('stg_fed_nara_aad__archival_records') }}

),

final as (

    select

        -- surrogate / natural key
        {{ dbt_utils.generate_surrogate_key(['dataset_id', 'record_id']) }}
                                                          as archival_record_sk,

        -- natural key components
        dataset_id,
        record_id,

        -- cross-source join identifiers
        date                                              as record_date,
        person_name,
        geo_location,
        -- geo_location doubles as the FIPS/geo identifier for cross-source joins;
        -- expose a dedicated alias for FIPS-based joins
        geo_location                                      as fips_geo,

        record_group_number,

        -- descriptive context
        dataset_name,
        series_title,
        description_text,

        -- semi-structured raw payload
        raw_fields_json,

        -- pipeline metadata
        _ingested_at,
        _source_run_id

    from base

)

select * from final
