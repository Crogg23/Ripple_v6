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
    order by case legislator_set when 'current' then 1 when 'historical' then 2 else 3 end,
             -- tie-breakers 2026-09-18: the row's own values, so the same row wins every run
             bioguide nulls last, icpsr nulls last, govtrack nulls last, opensecrets nulls last,
             votesmart nulls last, lis nulls last, thomas nulls last, cspan nulls last,
             wikidata nulls last, ballotpedia nulls last, wikipedia nulls last, house_history nulls last,
             maplight nulls last, google_entity_id nulls last, fec_ids nulls last, full_name nulls last,
             name_first nulls last, name_last nulls last, birthday nulls last, gender nulls last,
             last_term_type nulls last, last_party nulls last, last_state nulls last,
             last_district nulls last, senate_class nulls last, first_term_start nulls last,
             last_term_end nulls last, n_terms nulls last
) = 1
