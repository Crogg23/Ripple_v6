{{ config(materialized='view') }}

with source as (

    select * from {{ source('ripple_raw', 'XC_UK_SANCTIONS_LIST') }}

),

renamed_cast as (

    select

        -- metadata
        try_to_timestamp(LAST_UPDATED, 'DD/MM/YYYY')            as last_updated_at,

        -- key identifiers
        UNIQUE_ID                                               as unique_id,
        OFSI_GROUP_ID                                          as ofsi_group_id,
        UN_REFERENCE_NUMBER                                    as un_reference_number,

        -- name fields
        NAME_6                                                  as name_6,
        NAME_1                                                  as name_1,
        NAME_2                                                  as name_2,
        NAME_3                                                  as name_3,
        NAME_4                                                  as name_4,
        NAME_5                                                  as name_5,
        NAME_TYPE                                               as name_type,
        ALIAS_STRENGTH                                         as alias_strength,
        TITLE                                                   as title,
        NAME_NON_LATIN_SCRIPT                                  as name_non_latin_script,
        NON_LATIN_SCRIPT_TYPE                                  as non_latin_script_type,
        NON_LATIN_SCRIPT_LANGUAGE                              as non_latin_script_language,

        -- regime / designation
        REGIME_NAME                                             as regime_name,
        DESIGNATION_TYPE                                        as designation_type,
        DESIGNATION_SOURCE                                      as designation_source,
        SANCTIONS_IMPOSED                                       as sanctions_imposed,
        OTHER_INFORMATION                                       as other_information,
        UK_STATEMENT_OF_REASONS                                as uk_statement_of_reasons,

        -- address
        ADDRESS_LINE_1                                          as address_line_1,
        ADDRESS_LINE_2                                          as address_line_2,
        ADDRESS_LINE_3                                          as address_line_3,
        ADDRESS_LINE_4                                          as address_line_4,
        ADDRESS_LINE_5                                          as address_line_5,
        ADDRESS_LINE_6                                          as address_line_6,
        ADDRESS_POSTAL_CODE                                    as address_postal_code,
        ADDRESS_COUNTRY                                         as address_country,

        -- contact
        PHONE_NUMBER                                            as phone_number,
        WEBSITE                                                 as website,
        EMAIL_ADDRESS                                           as email_address,

        -- individual attributes
        try_to_date(DATE_DESIGNATED, 'DD/MM/YYYY')              as date_designated,
        try_to_date(D_O_B, 'DD/MM/YYYY')                        as date_of_birth,
        NATIONALITY_IES                                         as nationalities,
        NATIONAL_IDENTIFIER_NUMBER                             as national_identifier_number,
        NATIONAL_IDENTIFIER_ADDITIONAL_INFORMATION             as national_identifier_additional_information,
        PASSPORT_NUMBER                                         as passport_number,
        PASSPORT_ADDITIONAL_INFORMATION                        as passport_additional_information,
        POSITION                                                as position,
        GENDER                                                  as gender,
        TOWN_OF_BIRTH                                           as town_of_birth,
        COUNTRY_OF_BIRTH                                        as country_of_birth,

        -- entity attributes
        TYPE_OF_ENTITY                                          as type_of_entity,
        SUBSIDIARIES                                            as subsidiaries,
        PARENT_COMPANY                                          as parent_company,
        BUSINESS_REGISTRATION_NUMBER_S                         as business_registration_numbers,

        -- vessel attributes
        IMO_NUMBER                                              as imo_number,
        CURRENT_OWNER_OPERATOR_S                               as current_owner_operators,
        PREVIOUS_OWNER_OPERATOR_S                              as previous_owner_operators,
        CURRENT_BELIEVED_FLAG_OF_SHIP                          as current_believed_flag_of_ship,
        PREVIOUS_FLAGS                                          as previous_flags,
        TYPE_OF_SHIP                                            as type_of_ship,
        try_to_number(TONNAGE_OF_SHIP)                          as tonnage_of_ship,
        try_to_double(LENGTH_OF_SHIP)                           as length_of_ship,
        try_to_number(YEAR_BUILT)                               as year_built,
        HULL_IDENTIFICATION_NUMBER_HIN                         as hull_identification_number,

        -- ingestion metadata
        _ingested_at,
        _source_run_id

    from source

),

deduped as (

    select *
    from renamed_cast
    qualify row_number() over (
        partition by unique_id, ofsi_group_id, name_type
        order by last_updated_at desc nulls last
    ) = 1

)

select * from deduped
