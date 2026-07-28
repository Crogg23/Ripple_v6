{{ config(materialized='table', schema='POLITICS') }}

-- GRAIN: one row per candidate-state-district-year-stage-mode combination
-- Answers: How many votes did each House candidate receive, by mode and stage?
-- Source: MIT Election Data + Science Lab (MEDSL) — U.S. House returns
-- Key joins: state_fips → geography; candidate → member crosswalk (fuzzy)

with base as (
    select * from {{ ref('stg_fed_medsl_house_returns__records') }}
)

select
    try_to_number(year)                  as election_year,
    trim(state)                          as state_name,
    trim(state_po)                       as state_abbr,
    trim(state_fips)                     as state_fips,
    trim(office)                         as office,
    trim(district)                       as district,
    trim(stage)                          as stage,
    trim(candidate)                      as candidate_name,
    trim(party)                          as party,
    (trim(writein) = 'TRUE')             as is_writein,
    trim(mode)                           as vote_mode,
    try_to_number(candidatevotes)        as candidate_votes,
    try_to_number(totalvotes)            as total_votes,
    round(try_to_double(candidatevotes) / nullif(try_to_double(totalvotes), 0), 4) as vote_share,
    (trim(special) = 'TRUE')             as is_special_election,
    (trim(runoff) = 'TRUE')              as is_runoff,
    _loaded_at
from base
where trim(candidate) is not null
