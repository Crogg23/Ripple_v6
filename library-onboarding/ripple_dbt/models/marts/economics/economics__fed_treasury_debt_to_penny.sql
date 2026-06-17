{{ config(materialized='table') }}

with base as (

    select * from {{ ref('stg_fed_treasury_debt_to_penny__debt_to_penny') }}

)

select
    -- key identifiers
    record_date,

    -- fiscal period dimensions
    record_fiscal_yr,
    record_fiscal_qtr,

    -- calendar period dimensions
    record_calendar_yr,
    record_calendar_qtr,
    record_calendar_month,
    record_calendar_day,

    -- source metadata
    src_line_nbr,

    -- debt measures (in dollars)
    debt_held_public_amt,
    intragov_hold_amt,
    tot_pub_debt_out_amt,

    -- derived metrics
    case
        when tot_pub_debt_out_amt > 0
            then round(debt_held_public_amt / tot_pub_debt_out_amt * 100, 4)
        else null
    end                                                    as pct_debt_held_public,

    case
        when tot_pub_debt_out_amt > 0
            then round(intragov_hold_amt / tot_pub_debt_out_amt * 100, 4)
        else null
    end                                                    as pct_intragov_hold,

    -- lineage
    _ingested_at,
    _source_run_id

from base
