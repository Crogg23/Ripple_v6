{{ config(materialized='table', schema='POLITICS') }}

-- THE PAYOFF STAT: money raised per SITTING member per cycle, keyed (bioguide, cycle).
-- Closes member -> candidate -> committee. The join on (cand_id, cycle) naturally
-- restricts to the CAND_IDs active in each cycle (a member's stale House id has no
-- summary row in a Senate cycle), so it does NOT blindly sum historical IDs.
-- money_raised_net sums net_receipts (already net of inter-committee transfers).

with member_cand as (

    select distinct
        s.bioguide, s.full_name, s.party, s.state, s.last_term_type, b.fec_id as cand_id
    from {{ ref('politics__member_spine') }} s
    join {{ ref('politics__member_fec_id') }} b on b.bioguide = s.bioguide
    where s.legislator_set = 'current'

),

joined as (

    select
        mc.bioguide, mc.full_name, mc.party, mc.state, mc.last_term_type, mc.cand_id,
        fs.cycle, fs.ttl_receipts, fs.trans_from_auth, fs.net_receipts, fs.cash_on_hand_close
    from member_cand mc
    join {{ ref('politics__fec_candidate_summary') }} fs on fs.cand_id = mc.cand_id

)

select
    bioguide,
    cycle,
    any_value(full_name)      as full_name,
    any_value(party)          as party,
    any_value(state)          as state,
    any_value(last_term_type) as chamber,
    count(distinct cand_id)   as n_candidate_ids,
    array_agg(distinct cand_id) within group (order by cand_id) as cand_ids,
    sum(ttl_receipts)         as ttl_receipts_gross,
    sum(trans_from_auth)      as trans_from_auth,
    sum(net_receipts)         as money_raised_net,
    sum(cash_on_hand_close)   as cash_on_hand_close
from joined
group by bioguide, cycle
