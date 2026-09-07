{{ config(materialized='table', schema='POLITICS') }}

-- GRAIN: one row per lobbyist per filing per general issue.
--
-- THIS IS THE REVOLVING DOOR. covered_position is free text naming the
-- government job the lobbyist held before lobbying: "Chief of Staff, Rep.
-- Donald McEachin", "Professional Staff, Senate Appropriations Cmte". It comes
-- from lobbying_activities[].lobbyists[].covered_position in the Senate LDA
-- API, which the old loader read for names and then dropped.
--
-- GOVERNANCE__FED_REVOLVINGDOOR_PROJECT IS NOT THIS. Its 406 rows are
-- government job SLOTS and the industry sectors each touches. There is no
-- person in it, which is why its PERSON_NAME reads 'nan' on 405 of 406 rows.
-- Use this table for question 90, not that one.
--
-- covered_position is FREE TEXT and multi-valued: several jobs arrive in one
-- string separated by ';' or '/'. Parse downstream, never assume one job.
-- has_covered_position is the cheap filter.
--
-- The meta column here is _INGESTED_AT with the leading underscore. Landing
-- carries BOTH conventions: the IRS527 and FEC tables lost the underscore to
-- ingest._sf_col, these did not. Match the target table, never assume.

with source as (
    select * from {{ source('ripple_raw', 'FED_SENATE_LDA_LOBBYIST_POSITIONS') }}
)

select
    FILING_UUID                                     as filing_uuid,
    FILING_YEAR                                     as filing_year,
    FILING_TYPE                                     as filing_type,
    DT_POSTED                                       as dt_posted,
    REGISTRANT_ID                                   as registrant_id,
    REGISTRANT_NAME                                 as registrant_name,
    CLIENT_ID                                       as client_id,
    CLIENT_NAME                                     as client_name,
    LOBBYIST_ID                                     as lobbyist_id,
    LOBBYIST_FIRST_NAME                             as lobbyist_first_name,
    LOBBYIST_MIDDLE_NAME                            as lobbyist_middle_name,
    LOBBYIST_LAST_NAME                              as lobbyist_last_name,
    LOBBYIST_SUFFIX                                 as lobbyist_suffix,
    GENERAL_ISSUE                                   as general_issue,
    COVERED_POSITION                                as covered_position,
    HAS_COVERED_POSITION                            as has_covered_position,
    IS_NEW_LOBBYIST                                 as is_new_lobbyist,
    'fed_senate_lda_lobbyist_positions'             as source_id,
    _INGESTED_AT                                    as _loaded_at
from source
