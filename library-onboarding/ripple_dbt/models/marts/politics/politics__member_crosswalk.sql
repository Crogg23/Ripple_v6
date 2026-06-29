{{ config(materialized='table', schema='POLITICS') }}

-- DELIVERABLE #1 (keystone): one row per member, keyed on bioguide, carrying every
-- alternate ID. The table that lets voting (Voteview/icpsr) join money (FEC/fec_id)
-- join everything else. A member can appear in both historical and executive sets
-- (e.g. a senator who became president) -- dedup prefers current > historical >
-- executive. member_key is a never-null surrogate (bioguide, else govtrack/etc).

select
    coalesce(bioguide, 'gt:' || govtrack, 'os:' || opensecrets, 'name:' || full_name) as member_key,
    bioguide,
    icpsr,
    govtrack,
    opensecrets,
    votesmart,
    lis,
    thomas,
    cspan,
    wikidata,
    ballotpedia,
    wikipedia,
    house_history,
    maplight,
    google_entity_id,
    fec_ids,
    full_name,
    name_first,
    name_last,
    birthday,
    gender,
    last_term_type,
    last_party,
    last_state,
    last_district,
    senate_class,
    first_term_start,
    last_term_end,
    n_terms,
    legislator_set
from {{ ref('stg_fed_congress_legislators__members') }}
qualify row_number() over (
    partition by coalesce(bioguide, 'gt:' || govtrack, 'os:' || opensecrets, 'name:' || full_name)
    order by case legislator_set when 'current' then 1 when 'historical' then 2 else 3 end
) = 1
