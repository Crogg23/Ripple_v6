{{ config(materialized='table', schema='POLITICS') }}

-- Roll-call metadata, keyed (congress, chamber, rollnumber). The denominator +
-- context (date, yea/nay counts, question, bill) for the votes matrix.
-- Re-pulled in full 2026-08-11: staging now covers all congresses
-- (113,512 landing rows; was 118th-119th only).

select
    congress, chamber, rollnumber, vote_date, session,
    yea_count, nay_count, vote_result, vote_question, bill_number, vote_desc
from {{ ref('stg_fed_voteview_rollcall_meta__rollcalls') }}
qualify row_number() over (partition by congress, chamber, rollnumber
                           order by vote_date nulls last) = 1
