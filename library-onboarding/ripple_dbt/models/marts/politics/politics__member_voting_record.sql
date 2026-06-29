{{ config(materialized='table', schema='POLITICS') }}

-- THE STAT GROUP: votes cast / missed votes / party unity, keyed (bioguide, congress).
--
-- DEFINITIONS (definition-bound -- reconciled to GovTrack by definition, not decimals):
--   votes_eligible  = roll-calls where the member was in the chamber (cast_code <> 0).
--   votes_cast      = recorded a position yea/nay/present (cast_code 1-8).
--   missed_votes    = cast_code = 9 (Not Voting / absent).
--   missed_vote_pct = 100 * missed_votes / votes_eligible.
--   party_unity     = on party-unity roll-calls (a majority of Democrats opposed a
--                     majority of Republicans -- the CQ definition), the share of the
--                     member's yea/nay votes cast with their OWN party's majority.
--                     Computed only for the two major parties (100=D, 200=R).
-- bioguide + party resolved via Voteview's own members file (same icpsr space). A
-- member with multiple icpsr in one congress (party switch) is summed to one
-- (bioguide, congress) row. 119th counts are PARTIAL (congress in progress).

with v as (

    select * from {{ ref('politics__voteview_votes') }} where cast_code <> 0

),

mem as (

    select
        try_to_number(ICPSR)      as icpsr,
        try_to_number(CONGRESS)   as congress,
        CHAMBER                   as chamber,
        try_to_number(PARTY_CODE) as party_code,
        nullif(trim(BIOGUIDE_ID), '') as bioguide,
        nullif(trim(BIONAME), '')     as bioname,
        nullif(trim(STATE_ABBREV), '') as state
    from {{ source('ripple_raw', 'FED_VOTEVIEW_MEMBERS') }}
    where CONGRESS in ('118', '119') and CHAMBER in ('House', 'Senate')
    qualify row_number() over (partition by icpsr, congress, chamber order by PARTY_CODE) = 1

),

elig as (

    select
        icpsr, congress, chamber,
        count(*)                                              as votes_eligible,
        sum(iff(vote_position in ('yea','nay','present'), 1, 0)) as votes_cast,
        sum(iff(vote_position = 'not_voting', 1, 0))          as missed_votes
    from v
    group by icpsr, congress, chamber

),

party_maj as (

    select
        congress, chamber, rollnumber, m.party_code,
        case when sum(iff(v.vote_position='yea',1,0)) > sum(iff(v.vote_position='nay',1,0)) then 'yea'
             when sum(iff(v.vote_position='nay',1,0)) > sum(iff(v.vote_position='yea',1,0)) then 'nay'
        end as maj
    from v
    join mem m using (icpsr, congress, chamber)
    where m.party_code in (100, 200) and v.vote_position in ('yea', 'nay')
    group by congress, chamber, rollnumber, m.party_code

),

pu as (

    select d.congress, d.chamber, d.rollnumber, d.maj as d_maj, r.maj as r_maj
    from (select * from party_maj where party_code = 100) d
    join (select * from party_maj where party_code = 200) r using (congress, chamber, rollnumber)
    where d.maj is not null and r.maj is not null and d.maj <> r.maj

),

member_pu as (

    select
        v.icpsr, v.congress, v.chamber,
        count(*) as party_unity_votes,
        sum(iff((m.party_code=100 and v.vote_position=pu.d_maj)
             or (m.party_code=200 and v.vote_position=pu.r_maj), 1, 0)) as party_unity_with
    from v
    join mem m using (icpsr, congress, chamber)
    join pu using (congress, chamber, rollnumber)
    where v.vote_position in ('yea', 'nay') and m.party_code in (100, 200)
    group by v.icpsr, v.congress, v.chamber

),

joined as (

    select
        e.icpsr, e.congress, e.chamber, e.votes_eligible, e.votes_cast, e.missed_votes,
        m.bioguide, m.bioname, m.state, m.party_code,
        mp.party_unity_votes, mp.party_unity_with
    from elig e
    left join mem m using (icpsr, congress, chamber)
    left join member_pu mp using (icpsr, congress, chamber)

)

select
    bioguide,
    congress,
    any_value(chamber)                                       as chamber,
    array_agg(distinct icpsr) within group (order by icpsr)  as icpsrs,
    any_value(bioname)                                       as bioname,
    any_value(state)                                         as state,
    case any_value(party_code) when 100 then 'Democrat' when 200 then 'Republican'
         else 'Other/Independent' end                        as party,
    sum(votes_eligible)                                      as votes_eligible,
    sum(votes_cast)                                          as votes_cast,
    sum(missed_votes)                                        as missed_votes,
    round(100.0 * sum(missed_votes) / nullif(sum(votes_eligible), 0), 2)      as missed_vote_pct,
    sum(party_unity_votes)                                   as party_unity_votes,
    sum(party_unity_with)                                    as party_unity_with,
    round(100.0 * sum(party_unity_with) / nullif(sum(party_unity_votes), 0), 2) as party_unity_pct,
    (congress = 119)                                         as congress_partial
from joined
where bioguide is not null
group by bioguide, congress
