{{ config(materialized='table') }}

-- GRAIN: one row per prescriber (NPI) × drug (generic name)
-- Answers: which prescribers prescribe which drugs, in what volume and cost?
-- Source: CMS Part D Prescriber Drug dataset (25.9M rows)
-- Key joins: NPI → LIBRARY_META.CONNECT.ENTITY_GOLDEN (spine_entity='provider')

with source as (

    select * from {{ source('ripple_raw', 'FED_CMS_PARTD_PRESCRIBER_DRUG') }}

),

cleaned as (

    select
        Prscrbr_NPI as npi,
        Prscrbr_Last_Org_Name as prescriber_last_org_name,
        Prscrbr_First_Name as prescriber_first_name,
        Prscrbr_City as prescriber_city,
        Prscrbr_State_Abrvtn as prescriber_state,
        Prscrbr_State_FIPS as prescriber_state_fips,
        Prscrbr_Type as prescriber_type,
        Brnd_Name as brand_name,
        Gnrc_Name as generic_name,
        try_to_number(Tot_Clms) as total_claims,
        try_to_number(Tot_30day_Fills) as total_30day_fills,
        try_to_number(Tot_Day_Suply) as total_day_supply,
        try_to_double(Tot_Drug_Cst) as total_drug_cost,
        try_to_number(Tot_Benes) as total_beneficiaries,
        try_to_number(GE65_Tot_Clms) as ge65_total_claims,
        try_to_double(GE65_Tot_Drug_Cst) as ge65_total_drug_cost,
        try_to_number(GE65_Tot_Benes) as ge65_total_beneficiaries,
        _INGESTED_AT as _loaded_at

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
    qualify row_number() over (partition by npi, generic_name order by _loaded_at desc) = 1

)

select * from final
