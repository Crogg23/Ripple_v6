{{ config(materialized='table', schema='POLITICS') }}

-- DELIVERABLE #2 (spine): bioguide-keyed member table with a DW-NOMINATE ideology
-- score. Joins the crosswalk (bioguide<->icpsr) to Voteview (icpsr) so voting
-- ideology lands on the same key as everything else. LEFT JOIN: members with no
-- Voteview match keep has_ideology = false rather than dropping out.

with vv as (

    select
        icpsr,
        bioguide_id,
        congress,
        chamber,
        party_code,
        state_abbrev,
        nominate_dim1,
        nominate_dim2,
        bioname,
        row_number() over (partition by icpsr order by congress desc nulls last) as rn
    from {{ ref('stg_fed_voteview_members__ideology') }}
    where icpsr is not null

)

select
    x.member_key,
    x.bioguide,
    x.icpsr,
    x.full_name,
    x.last_party        as party,
    x.last_state        as state,
    x.last_term_type,
    x.senate_class,
    x.n_terms,
    x.first_term_start,
    x.last_term_end,
    x.legislator_set,
    v.nominate_dim1     as dw_nominate_dim1,
    v.nominate_dim2     as dw_nominate_dim2,
    v.congress          as latest_voteview_congress,
    v.chamber           as voteview_chamber,
    case
        when v.nominate_dim1 is null then 'unknown'
        when v.nominate_dim1 < 0     then 'left/liberal'
        when v.nominate_dim1 > 0     then 'right/conservative'
        else 'centrist'
    end                 as ideology_label,
    (v.icpsr is not null)         as has_voteview_match,  -- matched a Voteview member row
    (v.nominate_dim1 is not null) as has_ideology         -- carries a USABLE DW-NOMINATE score
from {{ ref('politics__member_crosswalk') }} x
left join vv v
    on v.rn = 1
   and v.icpsr = x.icpsr
