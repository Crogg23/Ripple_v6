{{ config(materialized='table', schema='CORPORATE_REGISTRY') }}

-- GRAIN: one row per company (CompanyNumber is unique)
-- Answers: What companies are registered in the UK, what's their status?
-- Source: UK Companies House (~5.7M companies)
-- Key joins: company_number â†’ UK-specific cross-references

with source as (
    select * from {{ source('ripple_raw', 'INT_UK_COMPANIES_HOUSE') }}
)

select
    trim("CompanyNumber")                              as company_number,
    trim("CompanyName")                                as company_name,
    trim("RegAddress.AddressLine1")                    as address_line_1,
    trim("RegAddress.AddressLine2")                    as address_line_2,
    trim("RegAddress.PostTown")                        as post_town,
    trim("RegAddress.County")                          as county,
    trim("RegAddress.Country")                         as country,
    trim("RegAddress.PostCode")                        as post_code,
    trim("CompanyCategory")                            as company_category,
    trim("CompanyStatus")                              as company_status,
    trim("CountryOfOrigin")                            as country_of_origin,
    try_to_date(trim("DissolutionDate"), 'DD/MM/YYYY') as dissolution_date,
    try_to_date(trim("IncorporationDate"), 'DD/MM/YYYY') as incorporation_date,
    trim("Accounts.AccountCategory")                   as account_category,
    try_to_number("Mortgages.NumMortCharges")          as num_mortgage_charges,
    try_to_number("Mortgages.NumMortOutstanding")      as num_mortgages_outstanding,
    (trim("CompanyStatus") = 'Active') as is_active,
    "_INGESTED_AT" as _loaded_at,
    "_SOURCE_RUN_ID" as _source_run_id
from source
qualify row_number() over (
    partition by "CompanyNumber"
    order by "_INGESTED_AT" desc
) = 1
