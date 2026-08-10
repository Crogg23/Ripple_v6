{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_HRSA_UDS_SERVICE_DELIVERY_SITES') }}

),

renamed as (

    select

        -- identifiers
        trim(BPHC_ASSIGNED_NUMBER)                             as bphc_assigned_number,
        trim(HEALTH_CENTER_NUMBER)                             as health_center_number,
        trim(BHCMIS_ORGANIZATION_IDENTIFICATION_NUMBER)        as bhcmis_organization_id,
        trim(FQHC_SITE_MEDICARE_BILLING_NUMBER)                as fqhc_site_medicare_billing_number,
        trim(FQHC_SITE_NPI_NUMBER)                             as fqhc_site_npi_number,

        -- site
        trim(SITE_NAME)                                        as site_name,
        trim(SITE_ADDRESS)                                     as site_address,
        trim(SITE_CITY)                                        as site_city,
        trim(SITE_STATE_ABBREVIATION)                          as site_state_abbreviation,
        trim(SITE_POSTAL_CODE)                                 as site_postal_code,
        trim(SITE_TELEPHONE_NUMBER)                            as site_telephone_number,
        trim(SITE_WEB_ADDRESS)                                 as site_web_address,
        try_to_number(trim(OPERATING_HOURS_PER_WEEK), 8, 2)    as operating_hours_per_week,
        trim(HEALTH_CENTER_LOCATION_SETTING_IDENTIFICATION_NUMBER)
                                                               as location_setting_id,
        trim(HEALTH_CENTER_SERVICE_DELIVERY_SITE_LOCATION_SETTING_DESCRIPTION)
                                                               as location_setting_description,
        trim(HEALTH_CENTER_STATUS_IDENTIFICATION_NUMBER)       as site_status_id,
        trim(SITE_STATUS_DESCRIPTION)                          as site_status_description,
        trim(HEALTH_CENTER_LOCATION_IDENTIFICATION_NUMBER)     as location_type_id,
        trim(HEALTH_CENTER_LOCATION_TYPE_DESCRIPTION)          as location_type_description,
        trim(HEALTH_CENTER_TYPE_IDENTIFICATION_NUMBER)         as site_type_id,
        trim(HEALTH_CENTER_TYPE_DESCRIPTION)                   as site_type_description,
        trim(HEALTH_CENTER_OPERATOR_IDENTIFICATION_NUMBER)     as operator_id,
        trim(HEALTH_CENTER_OPERATOR_DESCRIPTION)               as operator_description,
        trim(HEALTH_CENTER_OPERATING_SCHEDULE_IDENTIFICATION_NUMBER)
                                                               as operating_schedule_id,
        trim(HEALTH_CENTER_OPERATIONAL_SCHEDULE_DESCRIPTION)   as operating_schedule_description,
        trim(HEALTH_CENTER_OPERATING_CALENDAR_SURROGATE_KEY)   as operating_calendar_id,
        trim(HEALTH_CENTER_OPERATING_CALENDAR)                 as operating_calendar,
        try_to_date(trim(SITE_ADDED_TO_SCOPE_THIS_DATE), 'MM/DD/YYYY')
                                                               as site_added_to_scope_date,

        -- parent health center
        trim(HEALTH_CENTER_TYPE)                               as health_center_type,
        trim(HEALTH_CENTER_NAME)                               as health_center_name,
        trim(HEALTH_CENTER_ORGANIZATION_STREET_ADDRESS)        as health_center_street_address,
        trim(HEALTH_CENTER_ORGANIZATION_CITY)                  as health_center_city,
        trim(HEALTH_CENTER_ORGANIZATION_STATE)                 as health_center_state,
        trim(HEALTH_CENTER_ORGANIZATION_ZIP_CODE)              as health_center_zip_code,
        trim(GRANTEE_ORGANIZATION_TYPE_DESCRIPTION)            as grantee_organization_type,

        -- geography
        try_to_number(trim(GEOCODING_ARTIFACT_ADDRESS_PRIMARY_X_COORDINATE), 12, 8)
                                                               as longitude,
        try_to_number(trim(GEOCODING_ARTIFACT_ADDRESS_PRIMARY_Y_COORDINATE), 12, 8)
                                                               as latitude,
        trim(U_S_MEXICO_BORDER_100_KILOMETER_INDICATOR)        as us_mexico_border_100km_indicator,
        trim(U_S_MEXICO_BORDER_COUNTY_INDICATOR)               as us_mexico_border_county_indicator,
        trim(STATE_AND_COUNTY_FEDERAL_INFORMATION_PROCESSING_STANDARD_CODE)
                                                               as state_county_fips_code,
        trim(COMPLETE_COUNTY_NAME)                             as complete_county_name,
        trim(COUNTY_EQUIVALENT_NAME)                           as county_equivalent_name,
        trim(COUNTY_DESCRIPTION)                               as county_description,
        trim(HHS_REGION_CODE)                                  as hhs_region_code,
        trim(HHS_REGION_NAME)                                  as hhs_region_name,
        trim(STATE_FIPS_CODE)                                  as state_fips_code,
        trim(STATE_NAME)                                       as state_name,
        trim(STATE_FIPS_AND_CONGRESSIONAL_DISTRICT_NUMBER_CODE)
                                                               as state_fips_congressional_district_code,
        trim(CONGRESSIONAL_DISTRICT_NUMBER)                    as congressional_district_number,
        trim(CONGRESSIONAL_DISTRICT_NAME)                      as congressional_district_name,
        trim(CONGRESSIONAL_DISTRICT_CODE)                      as congressional_district_code,
        trim(U_S_CONGRESSIONAL_REPRESENTATIVE_NAME)            as us_representative_name,
        trim(NAME_OF_U_S_SENATOR_NUMBER_ONE)                   as us_senator_one_name,
        trim(NAME_OF_U_S_SENATOR_NUMBER_TWO)                   as us_senator_two_name,

        -- record dates
        try_to_date(trim(DATA_WAREHOUSE_RECORD_CREATE_DATE), 'MM/DD/YYYY')
                                                               as record_create_date,

        -- metadata
        to_timestamp_ntz(INGESTED_AT, 6)                       as _ingested_at,
        SOURCE_RUN_ID                                          as _source_run_id,
        SRC_SHA256                                             as _src_sha256

    from source

)

select * from renamed
