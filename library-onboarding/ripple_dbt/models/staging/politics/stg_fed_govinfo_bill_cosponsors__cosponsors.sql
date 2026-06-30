{{ config(materialized='view', schema='POLITICS') }}

-- Cleaned GovInfo BILLSTATUS cosponsor extract, one row per
-- (congress, bill_type, bill_number, cosponsor_bioguide). is_withdrawn is true when
-- the source carries a sponsorshipWithdrawnDate. A member who withdrew then re-cosponsored
-- is collapsed to one row, preferring the NOT-withdrawn state.

select
    try_to_number(CONGRESS)                            as congress,
    upper(nullif(trim(BILL_TYPE), ''))                 as bill_type,
    try_to_number(BILL_NUMBER)                         as bill_number,
    nullif(trim(COSPONSOR_BIOGUIDE), '')               as cosponsor_bioguide,
    nullif(trim(COSPONSOR_NAME), '')                   as cosponsor_name,
    nullif(trim(COSPONSOR_PARTY), '')                  as cosponsor_party,
    nullif(trim(COSPONSOR_STATE), '')                  as cosponsor_state,
    (upper(trim(IS_ORIGINAL)) = 'TRUE')                as is_original,
    (nullif(trim(SPONSORSHIP_WITHDRAWN_DATE), '') is not null) as is_withdrawn,
    try_to_date(nullif(trim(SPONSORSHIP_DATE), ''))            as sponsorship_date,
    try_to_date(nullif(trim(SPONSORSHIP_WITHDRAWN_DATE), ''))  as sponsorship_withdrawn_date
from {{ source('ripple_raw', 'FED_GOVINFO_BILL_COSPONSORS') }}
where nullif(trim(COSPONSOR_BIOGUIDE), '') is not null
  and try_to_number(BILL_NUMBER) is not null
qualify row_number() over (partition by congress, bill_type, bill_number, cosponsor_bioguide
                           order by is_withdrawn asc, sponsorship_date desc nulls last) = 1
