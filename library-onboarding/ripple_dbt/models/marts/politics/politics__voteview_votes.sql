{{ config(materialized='table', schema='POLITICS') }}

-- The cast matrix, keyed (congress, chamber, rollnumber, icpsr), with a derived
-- vote_position. Cast codes (confirmed from Voteview data): 1/2/3=yea, 4/5/6=nay,
-- 7/8=present, 9=not_voting (the missed vote), 0=not_member (excluded downstream).

select
    congress,
    chamber,
    rollnumber,
    icpsr,
    cast_code,
    case
        when cast_code in (1, 2, 3) then 'yea'
        when cast_code in (4, 5, 6) then 'nay'
        when cast_code in (7, 8)    then 'present'
        when cast_code = 9          then 'not_voting'
        when cast_code = 0          then 'not_member'
        else 'other'
    end as vote_position,
    prob
from {{ ref('stg_fed_voteview_rollcalls__votes') }}
qualify row_number() over (partition by congress, chamber, rollnumber, icpsr
                           order by prob desc nulls last) = 1
