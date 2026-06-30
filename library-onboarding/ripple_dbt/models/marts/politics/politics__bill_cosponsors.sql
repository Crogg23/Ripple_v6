{{ config(materialized='table', schema='POLITICS') }}

-- One row per (congress, bill_type, bill_number, cosponsor_bioguide). Kept as a
-- SEPARATE table so the cosponsor list never inflates the one-row-per-bill grain.
-- is_withdrawn marks cosponsorships the member later withdrew (excluded from the
-- member box-score's cosponsored_count). Pass-through of the deduped staging view.

select
    congress,
    bill_type,
    bill_number,
    cosponsor_bioguide,
    cosponsor_name,
    cosponsor_party,
    cosponsor_state,
    is_original,
    is_withdrawn,
    sponsorship_date,
    sponsorship_withdrawn_date
from {{ ref('stg_fed_govinfo_bill_cosponsors__cosponsors') }}
