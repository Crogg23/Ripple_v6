{{ config(materialized='table', schema='ECONOMICS') }}

-- GRAIN: one row per county (AREA_FIPS) Ã— industry (INDUSTRY_CODE) Ã— ownership (OWN_CODE) Ã— year Ã— quarter
-- Answers: employment levels, wages, and establishment counts by geography and industry
-- Source: BLS Quarterly Census of Employment and Wages (3.6M rows)
-- Key joins: AREA_FIPS â†’ DIM_COUNTY (first 5 digits = county FIPS)

with source as (

    select * from {{ source('ripple_raw', 'FED_BLS_QCEW') }}

),

cleaned as (

    select
        AREA_FIPS as area_fips,
        left(AREA_FIPS, 2) as state_fips,
        OWN_CODE as ownership_code,
        INDUSTRY_CODE as industry_code,
        AGGLVL_CODE as aggregation_level_code,
        SIZE_CODE as size_code,
        try_to_number(YEAR) as year,
        try_to_number(QTR) as quarter,
        DISCLOSURE_CODE as disclosure_code,
        try_to_number(ANNUAL_AVG_ESTABS) as annual_avg_establishments,
        try_to_number(ANNUAL_AVG_EMPLVL) as annual_avg_employment,
        try_to_number(TOTAL_ANNUAL_WAGES) as total_annual_wages,
        try_to_number(ANNUAL_AVG_WKLY_WAGE) as annual_avg_weekly_wage,
        try_to_number(AVG_ANNUAL_PAY) as avg_annual_pay,
        try_to_double(OTY_ANNUAL_AVG_EMPLVL_PCT_CHG) as yoy_employment_pct_change,
        try_to_double(OTY_TOTAL_ANNUAL_WAGES_PCT_CHG) as yoy_wages_pct_change

    from source

),

final as (

    select *
    from cleaned
    where area_fips is not null and year is not null
    qualify row_number() over (
        partition by area_fips, industry_code, ownership_code, year, quarter
        order by area_fips
    ) = 1

)

select * from final
