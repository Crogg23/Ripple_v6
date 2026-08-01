{{ config(materialized='table', schema='HEALTH') }}

-- GRAIN: one row per prescriber (NPI) x drug (generic name) x BRAND. Fixed
-- 2026-07-31: the key was missing brand_name, so a prescriber writing claims under
-- two different brand/formulation names for the same generic (e.g. 64 claims for
-- "Divalproex Sodium" at $1,807 AND 63 separate claims for "Divalproex Sodium Er"
-- at $4,427) had one of the two SILENTLY DISCARDED, arbitrarily -- undercounting
-- both total claims and total drug cost for every affected prescriber. Found via
-- tests/test_mart_duplication.py, which caught this mart (24,530,894 rows)
-- disagreeing with an auto-generated raw duplicate (25,869,521). brand_name now
-- joins the key; verified live: COUNT(DISTINCT full 3-column key) == 25,869,521
-- exactly, matching the raw source with zero further collapsing.
-- Answers: which prescribers prescribe which drugs (by generic AND brand), in what
-- volume and cost?
-- Source: CMS Part D Prescriber Drug dataset (25,869,521 rows — exact, verified 2026-07-31)
-- Key joins: NPI -> LIBRARY_META."CONNECT".ENTITY_GOLDEN (spine_entity='provider')
--
-- BUG FIXED 2026-07-29: every column in this landing table was created as a quoted
-- mixed-case identifier ("Prscrbr_NPI", "Tot_Clms", ...). The model referenced them
-- bare, so Snowflake upper-cased them to PRSCRBR_NPI etc. and the build died with
-- "invalid identifier 'PRSCRBR_NPI'". All source columns are now quoted exactly.

with source as (

    select * from {{ source('ripple_raw', 'FED_CMS_PARTD_PRESCRIBER_DRUG') }}

),

cleaned as (

    select
        "Prscrbr_NPI"                          as npi,
        "Prscrbr_Last_Org_Name"                as prescriber_last_org_name,
        "Prscrbr_First_Name"                   as prescriber_first_name,
        "Prscrbr_City"                         as prescriber_city,
        "Prscrbr_State_Abrvtn"                 as prescriber_state,
        "Prscrbr_State_FIPS"                   as prescriber_state_fips,
        "Prscrbr_Type"                         as prescriber_type,
        "Brnd_Name"                            as brand_name,
        "Gnrc_Name"                            as generic_name,
        try_to_number("Tot_Clms")              as total_claims,
        try_to_number("Tot_30day_Fills")       as total_30day_fills,
        try_to_number("Tot_Day_Suply")         as total_day_supply,
        try_to_double("Tot_Drug_Cst")          as total_drug_cost,
        try_to_number("Tot_Benes")             as total_beneficiaries,
        try_to_number("GE65_Tot_Clms")         as ge65_total_claims,
        try_to_double("GE65_Tot_Drug_Cst")     as ge65_total_drug_cost,
        try_to_number("GE65_Tot_Benes")        as ge65_total_beneficiaries,
        "_INGESTED_AT"                         as _loaded_at

    from source

),

final as (

    select
        *,
        case
            when total_drug_cost > 0 and total_claims > 0
            then round(total_drug_cost / total_claims, 2)
        end as cost_per_claim,
        case
            when total_beneficiaries > 0 and total_claims > 0
            then round(total_claims / total_beneficiaries, 1)
        end as claims_per_beneficiary

    from cleaned
    qualify row_number() over (partition by npi, generic_name, brand_name order by _loaded_at desc) = 1

)

select * from final
