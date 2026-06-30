{{ config(materialized='view', schema='POLITICS') }}

-- Cleaned GovInfo BILLSTATUS bills, one row per (congress, bill_type, bill_number).
-- Light cleaning only: cast types, UPPER the bill_type, SPLIT the pipe-delimited
-- action-type list into an array, dedup to the bill grain. All stat/derivation
-- logic (law-eligibility, became_law, advanced_past_committee, latest_stage) lives
-- in the mart (politics__bills), not here.

select
    try_to_number(CONGRESS)                         as congress,
    upper(nullif(trim(BILL_TYPE), ''))              as bill_type,
    try_to_number(BILL_NUMBER)                      as bill_number,
    nullif(trim(SPONSOR_BIOGUIDE), '')              as sponsor_bioguide,
    nullif(trim(SPONSOR_NAME), '')                  as sponsor_name,
    nullif(trim(TITLE), '')                         as title,
    nullif(trim(LAW_TYPE), '')                      as law_type,
    nullif(trim(LAW_NUMBER), '')                    as law_number,
    split(nullif(trim(ACTION_TYPES), ''), '|')      as action_types,
    try_to_number(N_ACTIONS)                        as n_actions,
    try_to_date(nullif(trim(INTRODUCED_DATE), ''))  as introduced_date,
    nullif(trim(LATEST_ACTION_DATE), '')            as latest_action_date,
    nullif(trim(LATEST_ACTION_TEXT), '')            as latest_action_text
    -- n_cosponsors is derived in politics__bills as the DISTINCT cosponsor count (the raw
    -- landing N_COSPONSORS over-counts the rare member double-listed as cosponsor on a bill).
from {{ source('ripple_raw', 'FED_GOVINFO_BILLSTATUS') }}
where try_to_number(BILL_NUMBER) is not null
  and upper(nullif(trim(BILL_TYPE), '')) is not null
qualify row_number() over (partition by congress, bill_type, bill_number
                           order by introduced_date nulls last) = 1
