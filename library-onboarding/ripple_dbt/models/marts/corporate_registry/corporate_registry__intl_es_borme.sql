{{ config(materialized='table') }}

with base as (

    select *
    from {{ ref('stg_intl_es_borme__borme_corporate_acts') }}

),

final as (

    select
        -- primary / cross-source join keys
        company_id,
        country,
        date,

        -- issue metadata
        borme_issue_number,
        section,
        cve,

        -- company attributes
        company_name,
        province,

        -- corporate act detail
        act_type,
        act_description,

        -- source document
        pdf_url,

        -- pipeline metadata
        _ingested_at,
        _source_run_id,

        -- derived convenience columns
        date_trunc('month', date)                          as act_month,
        date_trunc('year',  date)                          as act_year,
        'intl_es_borme'                                    as source_id

    from base

)

select * from final
