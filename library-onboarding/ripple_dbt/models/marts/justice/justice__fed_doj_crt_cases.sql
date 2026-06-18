{{ config(materialized='table') }}

with

staging as (

    select * from {{ ref('stg_fed_doj_crt_cases__crt_cases') }}

),

final as (

    select

        -- surrogate / natural key
        {{ dbt_utils.generate_surrogate_key(['company_id', 'person_name', 'date', 'state']) }}
                                                          as crt_case_key,

        -- key identifiers for cross-source joins
        company_id,
        person_name,
        date,
        state,

        -- core case attributes
        case_title,
        section,
        case_type,
        status,

        -- reference
        document_url,
        description,

        -- pipeline metadata
        _ingested_at,
        _source_run_id

    from staging

)

select * from final
