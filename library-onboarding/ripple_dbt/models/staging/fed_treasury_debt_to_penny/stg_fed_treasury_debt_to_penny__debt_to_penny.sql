{{ config(materialized='view') }}

with source as (

    select * from {{ source('ripple_raw', 'FED_TREASURY_DEBT_TO_PENNY') }}

),

casted as (

    select
        try_to_date(record_date, 'YYYY-MM-DD')          as record_date,
        try_to_double(debt_held_public_amt)              as debt_held_public_amt,
        try_to_double(intragov_hold_amt)                 as intragov_hold_amt,
        try_to_double(tot_pub_debt_out_amt)              as tot_pub_debt_out_amt,
        try_to_number(src_line_nbr)                      as src_line_nbr,
        record_fiscal_yr                                 as record_fiscal_yr,
        record_fiscal_qtr                                as record_fiscal_qtr,
        record_calendar_yr                               as record_calendar_yr,
        record_calendar_qtr                              as record_calendar_qtr,
        record_calendar_month                            as record_calendar_month,
        record_calendar_day                              as record_calendar_day,
        _ingested_at,
        _source_run_id
    from source

),

deduped as (

    select *,
        row_number() over (
            partition by record_date
            order by _ingested_at desc
        ) as _row_num
    from casted

)

select
    record_date,
    debt_held_public_amt,
    intragov_hold_amt,
    tot_pub_debt_out_amt,
    src_line_nbr,
    record_fiscal_yr,
    record_fiscal_qtr,
    record_calendar_yr,
    record_calendar_qtr,
    record_calendar_month,
    record_calendar_day,
    _ingested_at,
    _source_run_id
from deduped
where _row_num = 1
