{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_TREASURY_AVG_INTEREST_RATES') }}

),

renamed_cast as (

    select

        -- primary key components
        {{ stg_date('record_date') }}                         as record_date,
        security_type_desc                               as security_type_desc,
        security_desc                                    as security_desc,

        -- measures
        {{ stg_float('avg_interest_rate_amt') }}             as avg_interest_rate_amt,

        -- ordering / report metadata
        {{ stg_int('src_line_nbr') }}                      as src_line_nbr,

        -- fiscal / calendar period attributes
        record_fiscal_year                               as record_fiscal_year,
        record_fiscal_quarter                            as record_fiscal_quarter,
        record_calendar_year                             as record_calendar_year,
        record_calendar_quarter                          as record_calendar_quarter,
        record_calendar_month                            as record_calendar_month,

        -- landing metadata (carry through if present)
        _ingested_at,
        _source_run_id

    from source

),

deduped as (

    select *
    from renamed_cast
    qualify row_number() over (
        partition by record_date, security_type_desc, security_desc
        order by _ingested_at desc
    ) = 1

)

select * from deduped
