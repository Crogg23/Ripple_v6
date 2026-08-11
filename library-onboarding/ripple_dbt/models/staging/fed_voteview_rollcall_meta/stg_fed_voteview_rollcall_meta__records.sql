{{ config(tags=['minimal_staging']) }}

-- GRAIN: one row per roll-call — (congress, chamber, rollnumber) unique
-- (verified 2026-08-11 on the full pull). Re-pulled in full 2026-08-11 into
-- FED_VOTEVIEW_ROLLCALL_META_FULL (113,512 rows, all congresses; column set
-- unchanged from the capped table). Passthrough staging view.

with source as (

    select * from {{ source('ripple_raw', 'FED_VOTEVIEW_ROLLCALL_META_FULL') }}

),

renamed as (

    select
        CONGRESS as congress,
        CHAMBER as chamber,
        ROLLNUMBER as rollnumber,
        DATE as date,
        SESSION as session,
        CLERK_ROLLNUMBER as clerk_rollnumber,
        YEA_COUNT as yea_count,
        NAY_COUNT as nay_count,
        NOMINATE_MID_1 as nominate_mid_1,
        NOMINATE_MID_2 as nominate_mid_2,
        NOMINATE_SPREAD_1 as nominate_spread_1,
        NOMINATE_SPREAD_2 as nominate_spread_2,
        NOMINATE_LOG_LIKELIHOOD as nominate_log_likelihood,
        BILL_NUMBER as bill_number,
        VOTE_RESULT as vote_result,
        VOTE_DESC as vote_desc,
        VOTE_QUESTION as vote_question,
        DTL_DESC as dtl_desc,
        _INGESTED_AT as _loaded_at,
        'https://voteview.com/static/data/out/rollcalls/HSall_rollcalls.csv' as _source_url

    from source

)

select * from renamed
