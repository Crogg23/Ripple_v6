-- GRAIN: OBJECTID -- one row per Superfund site boundary feature, verified
-- exactly unique (2,114 = 2,114) live 2026-08-10. EPA_ID is NOT unique here
-- (1,908 distinct): one site can carry several boundary features (extent of
-- contamination, operable units, etc.) -- EPA_ID is the join key to FRS and
-- enforcement corpora, not the grain.

with source as (

    select * from {{ source('ripple_raw', 'FED_EPA_SUPERFUND_SITE_BOUNDARIES') }}

),

renamed as (

    select
        try_to_number(OBJECTID)                          as boundary_feature_id,
        trim(EPA_ID)                                     as epa_id,
        trim(SITE_NAME)                                  as site_name,
        trim(EPA_PROGRAM)                                as epa_program,
        trim(REGION_CODE)                                as epa_region_code,
        trim(SITE_FEATURE_CLASS)                         as site_feature_class,
        trim(SITE_FEATURE_TYPE)                          as site_feature_type,
        trim(SITE_FEATURE_NAME)                          as site_feature_name,
        trim(SITE_FEATURE_DESCRIPTION)                   as site_feature_description,
        trim(NPL_STATUS_CODE)                            as npl_status_code,
        trim(FEDERAL_FACILITY_DETER_CODE)                as federal_facility_code,
        -- epoch-milliseconds strings
        to_timestamp_ntz(try_to_number(LAST_CHANGE_DATE) / 1000)      as last_change_at,
        to_timestamp_ntz(try_to_number(ORIGINAL_CREATION_DATE) / 1000) as originally_created_at,
        trim(SITE_FEATURE_SOURCE)                        as site_feature_source,
        trim(STREET_ADDR_TXT)                            as street_address,
        trim(ADDR_COMMENT)                               as address_comment,
        trim(CITY_NAME)                                  as city,
        trim(COUNTY)                                     as county,
        trim(STATE_CODE)                                 as state_code,
        trim(ZIP_CODE)                                   as zip_code,
        trim(SITE_CONTACT_NAME)                          as site_contact_name,
        trim(PRIMARY_TELEPHONE_NUM)                      as site_contact_phone,
        trim(SITE_CONTACT_EMAIL)                         as site_contact_email,
        trim(URL_ALIAS_TXT)                              as site_url,
        trim(FEATURE_INFO_URL)                           as feature_info_url,
        try_to_double(GIS_AREA)                          as gis_area,
        trim(GIS_AREA_UNITS)                             as gis_area_units,
        trim(PROJECTION)                                 as projection,

        to_timestamp_ntz(INGESTED_AT, 6)                 as _loaded_at,
        SOURCE_RUN_ID                                    as _source_run_id,
        SRC_SHA256                                       as _src_sha256

    from source

)

select * from renamed
