{{ config(materialized='table') }}

with

staging as (

    select * from {{ ref('stg_fed_treasury_avg_interest_rates__avg_interest_rates') }}

),

final as (

    select

        -- surrogate / natural key
        {{ dbt_utils.generate_surrogate_key(['record_date', 'security_type_desc', 'security_desc']) }}
                                                         as avg_interest_rate_key,

        -- key identifiers (exposed for cross-source joins)
        record_date,
        security_type_desc,
        security_desc,

        -- measures
        avg_interest_rate_amt,

        -- report ordering
        src_line_nbr,

        -- fiscal period
        record_fiscal_year,
        record_fiscal_quarter,

        -- calendar period
        record_calendar_year,
        record_calendar_quarter,
        record_calendar_month,

        -- derived convenience columns
        date_trunc('month', record_date)                 as report_month,
        date_trunc('year',  record_date)                 as report_year,

        -- lineage
        _ingested_at,
        _source_run_id

    from staging

)

select * from final
