{{ config(materialized='table') }}

with staged as (

    select *
    from {{ ref('stg_intl_hudoc__echr_cases') }}

),

final as (

    select
        -- surrogate / natural keys exposed for cross-source joins
        {{ dbt_utils.generate_surrogate_key(['case_id', 'appno', 'ecli']) }}
                                                        as echr_case_sk,
        case_id,
        appno,
        ecli,
        country,
        person_name,
        date                                            as judgment_date,

        -- descriptive dimensions
        case_title,
        doc_type,
        importance,
        originating_body,
        respondent,
        language,

        -- structured outcome fields
        articles,
        violation,
        nonviolation,
        conclusion,
        keywords,

        -- reference
        url,

        -- calendar helpers
        year(date)                                      as judgment_year,
        month(date)                                     as judgment_month,
        date_trunc('quarter', date)                     as judgment_quarter,

        -- pipeline metadata
        _ingested_at,
        _source_run_id

    from staged

)

select *
from final
