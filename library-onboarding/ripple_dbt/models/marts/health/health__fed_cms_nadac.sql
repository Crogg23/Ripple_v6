{{ config(materialized='table') }}

-- GRAIN: one row per drug (NDC) × effective_date
-- Answers: national average drug acquisition costs over time, brand vs. generic pricing
-- Source: CMS NADAC survey data (1.5M rows)
-- Key joins: NDC → Part D prescriber drug data for cost-paid vs. cost-acquired comparison

with source as (

    select * from {{ source('ripple_raw', 'FED_CMS_NADAC') }}

),

cleaned as (

    select
        NDC as ndc,
        NDC_DESCRIPTION as drug_description,
        try_to_double(NADAC_PER_UNIT) as nadac_per_unit,
        try_to_date(EFFECTIVE_DATE) as effective_date,
        PRICING_UNIT as pricing_unit,
        PHARMACY_TYPE_INDICATOR as pharmacy_type,
        OTC as is_otc,
        EXPLANATION_CODE as explanation_code,
        CLASSIFICATION_FOR_RATE_SETTING as rate_classification,
        try_to_double(CORRESPONDING_GENERIC_DRUG_NADAC_PER_UNIT) as generic_nadac_per_unit,
        try_to_date(CORRESPONDING_GENERIC_DRUG_EFFECTIVE_DATE) as generic_effective_date,
        try_to_date(AS_OF_DATE) as as_of_date,
        INGESTED_AT as _loaded_at

    from source

),

final as (

    select
        *,
        case
            when nadac_per_unit > 0 and generic_nadac_per_unit > 0
            then round(nadac_per_unit / generic_nadac_per_unit, 2)
        end as brand_to_generic_ratio

    from cleaned
    qualify row_number() over (partition by ndc, effective_date order by _loaded_at desc) = 1

)

select * from final
