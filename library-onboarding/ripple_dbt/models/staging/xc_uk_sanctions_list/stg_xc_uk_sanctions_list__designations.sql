{{ config(materialized='view') }}

/*
  Hand-built 2026-08-09 (73-source backlog, wave 2). UK OFSI Consolidated
  List of Financial Sanctions Targets.
  Grain: one row = one name variant (primary name or alias) of a designated
  person/entity/ship. UNIQUE_ID identifies the designation (6,315 distinct
  over 57,883 rows); OFSI_GROUP_ID groups name variants the same way.
  Neither is row-unique by design -- no unique test.
  Dates are DD/MM/YYYY.
*/

with source as (
    select * from {{ source('ripple_raw', 'XC_UK_SANCTIONS_LIST') }}
),

renamed as (
    select
        nullif(trim(UNIQUE_ID), '')                              as designation_id,
        nullif(trim(OFSI_GROUP_ID), '')                          as ofsi_group_id,
        nullif(trim(UN_REFERENCE_NUMBER), '')                    as un_reference_number,
        nullif(trim(NAME_6), '')                                 as name_primary,
        nullif(trim(NAME_1), '')                                 as name_1,
        nullif(trim(NAME_2), '')                                 as name_2,
        nullif(trim(NAME_3), '')                                 as name_3,
        nullif(trim(NAME_4), '')                                 as name_4,
        nullif(trim(NAME_5), '')                                 as name_5,
        nullif(trim(NAME_TYPE), '')                              as name_type,
        nullif(trim(ALIAS_STRENGTH), '')                         as alias_strength,
        nullif(trim(TITLE), '')                                  as title,
        nullif(trim(NAME_NON_LATIN_SCRIPT), '')                  as name_non_latin,
        nullif(trim(REGIME_NAME), '')                            as regime_name,
        nullif(trim(DESIGNATION_TYPE), '')                       as designation_type,
        nullif(trim(DESIGNATION_SOURCE), '')                     as designation_source,
        nullif(trim(SANCTIONS_IMPOSED), '')                      as sanctions_imposed,
        nullif(trim(OTHER_INFORMATION), '')                      as other_information,
        nullif(trim(UK_STATEMENT_OF_REASONS), '')                as uk_statement_of_reasons,
        nullif(trim(ADDRESS_LINE_1), '')                         as address_line_1,
        nullif(trim(ADDRESS_LINE_2), '')                         as address_line_2,
        nullif(trim(ADDRESS_COUNTRY), '')                        as address_country,
        nullif(trim(ADDRESS_POSTAL_CODE), '')                    as address_postal_code,
        try_to_date(nullif(trim(DATE_DESIGNATED), ''), 'DD/MM/YYYY') as date_designated,
        try_to_date(nullif(trim(LAST_UPDATED), ''), 'DD/MM/YYYY')    as last_updated,
        nullif(trim(D_O_B), '')                                  as date_of_birth_raw,
        nullif(trim(NATIONALITY_IES), '')                        as nationalities,
        nullif(trim(PASSPORT_NUMBER), '')                        as passport_number,
        nullif(trim(NATIONAL_IDENTIFIER_NUMBER), '')             as national_identifier,
        nullif(trim(POSITION), '')                               as position,
        nullif(trim(GENDER), '')                                 as gender,
        nullif(trim(TOWN_OF_BIRTH), '')                          as town_of_birth,
        nullif(trim(COUNTRY_OF_BIRTH), '')                       as country_of_birth,
        nullif(trim(TYPE_OF_ENTITY), '')                         as type_of_entity,
        nullif(trim(SUBSIDIARIES), '')                           as subsidiaries,
        nullif(trim(PARENT_COMPANY), '')                         as parent_company,
        nullif(trim(BUSINESS_REGISTRATION_NUMBER_S), '')         as business_registration_numbers,
        nullif(trim(IMO_NUMBER), '')                             as imo_number,
        nullif(trim(CURRENT_OWNER_OPERATOR_S), '')               as current_owner_operator,
        nullif(trim(CURRENT_BELIEVED_FLAG_OF_SHIP), '')          as current_flag_of_ship,
        nullif(trim(TYPE_OF_SHIP), '')                           as type_of_ship,
        to_timestamp_ntz(_INGESTED_AT, 6)                        as _ingested_at,
        nullif(trim(_SOURCE_RUN_ID), '')                         as _source_run_id
    from source
)

select * from renamed
