{{ config(materialized='table', schema='POLITICS') }}

-- THE STAT GROUP: legislative output per (bioguide, congress). Sponsor + cosponsor both
-- carry bioguide, so they join straight to the member spine -- the last clean leg.
--
-- The raw bills_sponsored count is NEVER shown alone (it rewards spam); it ships only
-- alongside its qualifiers:
--   bills_sponsored_substantive vs resolutions_sponsored  -- the mandatory type split.
--   bills_enacted + enacted_rate                          -- rate over LAW-ELIGIBLE bills only
--                                                            (resolutions can't become law -> excluded
--                                                             from the denominator; NULL if 0 substantive).
--   advanced_past_committee_count + advanced_rate         -- documented rule (see politics__bills).
--   cosponsored_count                                     -- SEPARATE figure, withdrawn excluded
--                                                            (authoring a bill != signing on to one).
-- 119th is partial (congress_partial=true) -- fewer enacted laws mid-cycle; don't compare externally.

with spon as (

    select
        sponsor_bioguide                            as bioguide,
        congress,
        count(*)                                    as bills_sponsored,
        sum(iff(is_law_eligible, 1, 0))             as bills_sponsored_substantive,
        sum(iff(not is_law_eligible, 1, 0))         as resolutions_sponsored,
        sum(iff(became_law, 1, 0))                  as bills_enacted,
        sum(iff(is_law_eligible and advanced_past_committee, 1, 0)) as advanced_past_committee_count
    from {{ ref('politics__bills') }}
    where sponsor_bioguide is not null
    group by 1, 2

),

cospon as (

    select
        cosponsor_bioguide                          as bioguide,
        congress,
        count(*)                                    as cosponsored_count   -- withdrawn excluded below
    from {{ ref('politics__bill_cosponsors') }}
    where not is_withdrawn and cosponsor_bioguide is not null
    group by 1, 2

),

keys as (

    select bioguide, congress from spon
    union
    select bioguide, congress from cospon

)

select
    k.bioguide,
    k.congress,
    s.full_name,
    s.party,
    s.state,
    s.last_term_type                                as chamber,
    s.ideology_label,
    coalesce(sp.bills_sponsored, 0)                 as bills_sponsored,
    coalesce(sp.bills_sponsored_substantive, 0)     as bills_sponsored_substantive,
    coalesce(sp.resolutions_sponsored, 0)           as resolutions_sponsored,
    coalesce(sp.bills_enacted, 0)                   as bills_enacted,
    round(100.0 * sp.bills_enacted / nullif(sp.bills_sponsored_substantive, 0), 2)  as enacted_rate,
    coalesce(sp.advanced_past_committee_count, 0)   as advanced_past_committee_count,
    round(100.0 * sp.advanced_past_committee_count / nullif(sp.bills_sponsored_substantive, 0), 2) as advanced_rate,
    coalesce(cp.cosponsored_count, 0)               as cosponsored_count,
    (k.congress = 119)                              as congress_partial,
    (s.bioguide is not null)                        as has_spine_match
from keys k
left join spon   sp using (bioguide, congress)
left join cospon cp using (bioguide, congress)
left join {{ ref('politics__member_spine') }} s on s.bioguide = k.bioguide
