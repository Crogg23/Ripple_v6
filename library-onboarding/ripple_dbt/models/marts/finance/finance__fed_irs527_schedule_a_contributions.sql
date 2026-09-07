{{ config(materialized='table', schema='FINANCE') }}

-- GRAIN: one row per itemized contribution to a 527 political organization.
-- 9,701,952 rows. Landed 2026-09-06; the first 527 pass deferred this.
--
-- FORM_ID_NUMBER + SCHEDULE_ID is the natural key. There is no dedupe here
-- because the source is a snapshot replace, not an append log.
--
-- CONTRIBUTION_DATE is YYYYMMDD TEXT and is filled on 98.4% of rows. Parse it,
-- never sort it as a string across a century boundary.
--
-- PERSON_NAME is the CONTRIBUTOR. The mirror-image table
-- FINANCE__FED_IRS527_SCHEDULE_B_EXPENDITURES uses the same column name for the
-- RECIPIENT. Same shape, opposite direction; the table name is what tells them
-- apart, so never union them without a side flag.

with source as (
    select * from {{ source('ripple_raw', 'IRS527_SCHEDULE_A_CONTRIBUTIONS') }}
)

select
    FORM_ID_NUMBER                                  as form_id_number,
    SCHEDULE_ID                                     as schedule_id,
    ORG_NAME                                        as org_name,
    EIN                                             as ein,
    PERSON_NAME                                     as contributor_name,
    ADDR1                                           as contributor_addr1,
    ADDR2                                           as contributor_addr2,
    CITY                                            as contributor_city,
    STATE                                           as contributor_state,
    ZIP                                             as contributor_zip,
    ZIP_EXT                                         as contributor_zip_ext,
    EMPLOYER                                        as contributor_employer,
    OCCUPATION                                      as contributor_occupation,
    {{ ripple_num('AMOUNT') }}                      as contribution_amount,
    {{ ripple_num('AGG_CONTRIBUTION_YTD') }}        as agg_contribution_ytd,
    try_to_date(nullif(trim(CONTRIBUTION_DATE), ''), 'YYYYMMDD') as contribution_date,
    CONTRIBUTION_DATE                               as contribution_date_raw,
    'irs527_schedule_a_contributions'               as source_id,
    INGESTED_AT                                     as _loaded_at
from source
