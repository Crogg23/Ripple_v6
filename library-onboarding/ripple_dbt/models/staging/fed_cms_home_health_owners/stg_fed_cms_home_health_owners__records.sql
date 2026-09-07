-- GRAIN: one row per (enrollment, owner, role) -- ENROLLMENT_ID repeats, one agency has many owners
-- and one owner can hold several roles. No single natural key; the mart keeps every row.
-- Source landed 2026-09-07 by scripts/cms_hha_owners_load.py (CMS HHA All Owners, quarterly).
-- Casts kept as landed (TEXT); the mart types the date, the percentage and the Y/N flags.

with source as (

    select * from {{ source('ripple_raw', 'FED_CMS_HOME_HEALTH_OWNERS') }}

),

renamed as (

    select
        "ENROLLMENT_ID" as enrollment_id,
        "ASSOCIATE_ID" as associate_id,
        "ORGANIZATION_NAME" as organization_name,
        "ASSOCIATE_ID_OWNER" as associate_id_owner,
        "TYPE_OWNER" as type_owner,
        "ROLE_CODE_OWNER" as role_code_owner,
        "ROLE_TEXT_OWNER" as role_text_owner,
        "ASSOCIATION_DATE_OWNER" as association_date_owner,
        "FIRST_NAME_OWNER" as first_name_owner,
        "MIDDLE_NAME_OWNER" as middle_name_owner,
        "LAST_NAME_OWNER" as last_name_owner,
        "TITLE_OWNER" as title_owner,
        "ORGANIZATION_NAME_OWNER" as organization_name_owner,
        "DOING_BUSINESS_AS_NAME_OWNER" as doing_business_as_name_owner,
        "ADDRESS_LINE_1_OWNER" as address_line_1_owner,
        "ADDRESS_LINE_2_OWNER" as address_line_2_owner,
        "CITY_OWNER" as city_owner,
        "STATE_OWNER" as state_owner,
        "ZIP_CODE_OWNER" as zip_code_owner,
        "PERCENTAGE_OWNERSHIP" as percentage_ownership,
        "CREATED_FOR_ACQUISITION_OWNER" as created_for_acquisition_owner,
        "CORPORATION_OWNER" as corporation_owner,
        "LLC_OWNER" as llc_owner,
        "MEDICAL_PROVIDER_SUPPLIER_OWNER" as medical_provider_supplier_owner,
        "MANAGEMENT_SERVICES_COMPANY_OWNER" as management_services_company_owner,
        "MEDICAL_STAFFING_COMPANY_OWNER" as medical_staffing_company_owner,
        "HOLDING_COMPANY_OWNER" as holding_company_owner,
        "INVESTMENT_FIRM_OWNER" as investment_firm_owner,
        "FINANCIAL_INSTITUTION_OWNER" as financial_institution_owner,
        "CONSULTING_FIRM_OWNER" as consulting_firm_owner,
        "FOR_PROFIT_OWNER" as for_profit_owner,
        "NON_PROFIT_OWNER" as non_profit_owner,
        "PRIVATE_EQUITY_COMPANY_OWNER" as private_equity_company_owner,
        "REIT_OWNER" as reit_owner,
        "CHAIN_HOME_OFFICE_OWNER" as chain_home_office_owner,
        "OTHER_TYPE_OWNER" as other_type_owner,
        "OTHER_TYPE_TEXT_OWNER" as other_type_text_owner,
        "OWNED_BY_ANOTHER_ORG_OR_IND_OWNER" as owned_by_another_org_or_ind_owner,
        -- unprefixed on this table: written by write_pandas, not land()
        "INGESTED_AT" as _loaded_at,
        "_SOURCE_RUN_ID" as _source_run_id

    from source

)

select * from renamed
