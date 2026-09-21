{{ config(materialized='view', schema='POLITICS') }}

-- Voteview roll-call METADATA (one row per roll-call), ALL congresses since
-- the 2026-08-11 full re-pull (113,512 rows; previously 118th + 119th only).
-- Source = fed_voteview_rollcall_meta_full (HSall_rollcalls.csv).

with source as (

    select * from {{ source('ripple_raw', 'FED_VOTEVIEW_ROLLCALL_META_FULL') }}

)

select
    {{ stg_int('CONGRESS') }}            as congress,
    CHAMBER                            as chamber,
    {{ stg_int('ROLLNUMBER') }}          as rollnumber,
    -- DATE lands as 'YYYY-MM-DD' (sampled 2026-08-11) — explicit format
    try_to_date(nullif(trim(DATE), ''), 'YYYY-MM-DD') as vote_date,
    {{ stg_int('SESSION') }}             as session,
    {{ stg_int('YEA_COUNT') }}           as yea_count,
    {{ stg_int('NAY_COUNT') }}           as nay_count,
    nullif(trim(VOTE_RESULT), '')      as vote_result,
    nullif(trim(VOTE_QUESTION), '')    as vote_question,
    nullif(trim(BILL_NUMBER), '')      as bill_number,
    nullif(trim(VOTE_DESC), '')        as vote_desc
from source
where {{ stg_int('ROLLNUMBER') }} is not null
