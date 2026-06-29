{{ config(materialized='view', schema='POLITICS') }}

-- Members of Congress + executives (current/historical/executive), one row per
-- legislator: the cleaned id crosswalk + bio + most-recent term. Canonical copy
-- is built by politics/loaders/build_skeleton.py; this mirrors it for dbt.

with source as (

    select * from {{ source('ripple_raw', 'FED_CONGRESS_LEGISLATORS') }}

)

select
    nullif(trim(BIOGUIDE), '')                       as bioguide,
    try_to_number(nullif(trim(ICPSR), ''))           as icpsr,
    nullif(trim(GOVTRACK), '')                       as govtrack,
    nullif(trim(OPENSECRETS), '')                    as opensecrets,
    nullif(trim(VOTESMART), '')                      as votesmart,
    nullif(trim(LIS), '')                            as lis,
    nullif(trim(THOMAS), '')                         as thomas,
    nullif(trim(CSPAN), '')                          as cspan,
    nullif(trim(WIKIDATA), '')                       as wikidata,
    nullif(trim(BALLOTPEDIA), '')                    as ballotpedia,
    nullif(trim(WIKIPEDIA), '')                      as wikipedia,
    nullif(trim(HOUSE_HISTORY), '')                  as house_history,
    nullif(trim(MAPLIGHT), '')                       as maplight,
    nullif(trim(GOOGLE_ENTITY_ID), '')               as google_entity_id,
    try_parse_json(FEC_IDS)                           as fec_ids,
    nullif(trim(NAME_FIRST), '')                     as name_first,
    nullif(trim(NAME_LAST), '')                      as name_last,
    coalesce(nullif(trim(NAME_OFFICIAL_FULL), ''),
             nullif(trim(NAME_FIRST || ' ' || NAME_LAST), '')) as full_name,
    nullif(trim(BIRTHDAY), '')                       as birthday,
    nullif(trim(GENDER), '')                         as gender,
    nullif(trim(TERM_TYPE), '')                      as last_term_type,
    nullif(trim(PARTY), '')                          as last_party,
    nullif(trim(STATE), '')                          as last_state,
    nullif(trim(DISTRICT), '')                       as last_district,
    nullif(trim(SENATE_CLASS), '')                   as senate_class,
    nullif(trim(TERM_START), '')                     as first_term_start,
    nullif(trim(TERM_END), '')                       as last_term_end,
    try_to_number(nullif(trim(N_TERMS), ''))         as n_terms,
    LEGISLATOR_SET                                   as legislator_set,
    _ingested_at,
    _source_run_id
from source
