{{ config(materialized='table', schema='POLITICS') }}

-- Roll-call metadata, keyed (congress, chamber, rollnumber). The denominator +
-- context (date, yea/nay counts, question, bill) for the votes matrix.

select
    congress, chamber, rollnumber, vote_date, session,
    yea_count, nay_count, vote_result, vote_question, bill_number, vote_desc
from {{ ref('stg_fed_voteview_rollcall_meta__rollcalls') }}
qualify row_number() over (partition by congress, chamber, rollnumber
                           order by vote_date nulls last) = 1
