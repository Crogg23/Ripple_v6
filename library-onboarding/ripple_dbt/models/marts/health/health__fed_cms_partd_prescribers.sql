{{ config(materialized='table', schema='HEALTH') }}

-- GRAIN: one row per prescriber (NPI) x drug (generic name) x BRAND. Fixed
-- 2026-07-31: the key was missing brand_name, so a prescriber writing claims under
-- two different brand/formulation names for the same generic (e.g. 64 claims for
-- "Divalproex Sodium" at $1,807 AND 63 separate claims for "Divalproex Sodium Er"
-- at $4,427) had one of the two SILENTLY DISCARDED, arbitrarily -- undercounting
-- both total claims and total drug cost for every affected prescriber. Found via
-- tests/test_mart_duplication.py, which caught this mart (25,869,521 rows)  [row count re-verified against the live table 2026-08-11; header had said 24,530,894]
-- disagreeing with an auto-generated raw duplicate (25,869,521). brand_name now
-- joins the key; verified live: COUNT(DISTINCT full 3-column key) == 25,869,521
-- exactly, matching the raw source with zero further collapsing.
-- Answers: which prescribers prescribe which drugs (by generic AND brand), in what
-- volume and cost?
-- Source: CMS Part D Prescriber Drug dataset (25,869,521 rows — exact, verified 2026-07-31)
-- Key joins: NPI -> LIBRARY_META."CONNECT".ENTITY_GOLDEN (spine_entity='provider')
--
-- VINTAGE: DY2022, one year, no year column in the landing table (checked live
-- 2026-09-20, FED_CMS_PARTD_PRESCRIBER_DRUG carries none). NPPES, Part B, and
-- the unsuffixed QPP and Open Payments marts are 2024 vintage -- any join from
-- this mart to those needs the ~2-year gap accounted for by hand.
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
        {{ stg_int('"Tot_Clms"') }}              as total_claims,
        {{ stg_float('"Tot_30day_Fills"') }}       as total_30day_fills,
        {{ stg_int('"Tot_Day_Suply"') }}         as total_day_supply,
        {{ stg_float('"Tot_Drug_Cst"') }}          as total_drug_cost,
        {{ stg_int('"Tot_Benes"') }}             as total_beneficiaries,
        {{ stg_int('"GE65_Tot_Clms"') }}         as ge65_total_claims,
        {{ stg_float('"GE65_Tot_Drug_Cst"') }}     as ge65_total_drug_cost,
        {{ stg_int('"GE65_Tot_Benes"') }}        as ge65_total_beneficiaries,
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
    qualify row_number() over (partition by npi, generic_name, brand_name order by _loaded_at desc,
             -- tie-breakers 2026-09-18: the row's own values, so the same row wins every run
             prescriber_last_org_name nulls last, prescriber_first_name nulls last,
             prescriber_city nulls last, prescriber_state nulls last, prescriber_state_fips nulls last,
             prescriber_type nulls last, total_claims nulls last, total_30day_fills nulls last,
             total_day_supply nulls last, total_drug_cost nulls last, total_beneficiaries nulls last,
             ge65_total_claims nulls last, ge65_total_drug_cost nulls last,
             ge65_total_beneficiaries nulls last
) = 1

)

-- THE LOCK (2026-09-21): the vintage rides on every row, so a join across Part D files can test it.
select *, 2022 as data_year from final
