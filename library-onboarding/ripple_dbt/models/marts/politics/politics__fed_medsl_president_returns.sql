{{ config(materialized='table', schema='POLITICS') }}

-- GRAIN: one row per candidate-state-year-party combination (presidential popular vote)
-- Answers: How did presidential candidates perform in each state?
-- Source: MIT Election Data + Science Lab (MEDSL) â€” U.S. Presidential returns
-- Key joins: state_fips â†’ geography; candidate â†’ party/national totals

with base as (
    select * from {{ ref('stg_fed_medsl_president_returns__records') }}
)

select
    try_to_number(year)                  as election_year,
    trim(state)                          as state_name,
    trim(state_po)                       as state_abbr,
    trim(state_fips)                     as state_fips,
    trim(candidate)                      as candidate_name,
    trim(party)                          as party,
    (trim(writein) = 'TRUE')             as is_writein,
    try_to_number(candidatevotes)        as candidate_votes,
    try_to_number(totalvotes)            as total_votes,
    round(try_to_double(candidatevotes) / nullif(try_to_double(totalvotes), 0), 4) as vote_share,
    _loaded_at
from base
where trim(candidate) is not null
