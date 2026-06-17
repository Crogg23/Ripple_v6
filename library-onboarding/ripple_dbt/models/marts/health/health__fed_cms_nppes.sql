{{ config(materialized='table') }}

with base as (

    select * from {{ ref('stg_fed_cms_nppes__npi_providers') }}

),

final as (

    select

        -- key identifiers
        npi,
        ein,
        entity_type_code,
        replacement_npi,

        -- provider display name (works for both individual and org)
        coalesce(
            provider_organization_name_legal_business_name,
            trim(
                coalesce(provider_first_name, '') || ' ' ||
                coalesce(provider_middle_name, '') || ' ' ||
                coalesce(provider_last_name, '')
            )
        )                                                              as provider_display_name,

        -- individual name parts
        provider_last_name,
        provider_first_name,
        provider_middle_name,
        provider_name_prefix,
        provider_name_suffix,
        provider_credential,
        provider_sex_code,

        -- organization
        provider_organization_name_legal_business_name,
        provider_other_organization_name,
        is_sole_proprietor,
        is_organization_subpart,
        parent_organization_lbn,
        parent_organization_tin,

        -- mailing address
        mailing_address_line_1,
        mailing_address_line_2,
        mailing_city,
        mailing_state,
        mailing_zip,
        mailing_country_code,
        mailing_phone,
        mailing_fax,

        -- practice location address (primary join key for geo analysis)
        practice_address_line_1,
        practice_address_line_2,
        practice_city,
        practice_state,
        practice_zip,
        practice_country_code,
        practice_phone,
        practice_fax,

        -- primary taxonomy (slot 1 where primary switch = Y)
        taxonomy_code_1                                                as primary_taxonomy_code,
        taxonomy_group_1                                               as primary_taxonomy_group,
        license_number_1                                               as primary_license_number,
        license_state_1                                                as primary_license_state,

        -- all taxonomy slots
        taxonomy_code_1,  taxonomy_code_2,  taxonomy_code_3,
        taxonomy_code_4,  taxonomy_code_5,  taxonomy_code_6,
        taxonomy_code_7,  taxonomy_code_8,  taxonomy_code_9,
        taxonomy_code_10, taxonomy_code_11, taxonomy_code_12,
        taxonomy_code_13, taxonomy_code_14, taxonomy_code_15,

        primary_taxonomy_switch_1,  primary_taxonomy_switch_2,
        primary_taxonomy_switch_3,  primary_taxonomy_switch_4,
        primary_taxonomy_switch_5,

        -- enumeration dates
        provider_enumeration_date,
        last_update_date,
        npi_deactivation_date,
        npi_reactivation_date,
        npi_deactivation_reason_code,
        certification_date,

        -- derived flags
        case when npi_deactivation_date is not null
             and npi_reactivation_date is null
             then true else false end                                  as is_deactivated,

        -- authorized official
        authorized_official_last_name,
        authorized_official_first_name,
        authorized_official_title,
        authorized_official_phone,

        -- metadata
        _ingested_at,
        _source_run_id

    from base

)

select * from final
