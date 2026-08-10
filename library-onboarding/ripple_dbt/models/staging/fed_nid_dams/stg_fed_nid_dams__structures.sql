{{ config(materialized='view') }}

/*
  Hand-built 2026-08-09 (73-source backlog, wave 2). USACE National Inventory
  of Dams (NID): every inventoried dam/structure in the US with hazard
  potential, condition assessment, and inspection dates.
  Grain: one row = one structure. NID_ID is NOT unique (92,766 rows /
  91,978 distinct ids): a dam's associated structures (saddle dams, dikes)
  share its NID_ID, and 2 rows carry no NID_ID at all, as published by
  USACE. No full-row duplicates exist. Kept as published.
  Dates are MM/DD/YYYY. Only analytically load-bearing numerics are cast.
*/

with source as (
    select * from {{ source('ripple_raw', 'FED_NID_DAMS') }}
),

renamed as (
    select
        nullif(trim(NID_ID), '')                                   as nid_id,
        nullif(trim(OTHER_STRUCTURE_ID), '')                       as other_structure_id,
        nullif(trim(FEDERAL_ID), '')                               as federal_id,
        nullif(trim(DAM_NAME), '')                                 as dam_name,
        nullif(trim(OTHER_NAMES), '')                              as other_names,
        nullif(trim(FORMER_NAMES), '')                             as former_names,
        nullif(trim(OWNER_NAMES), '')                              as owner_names,
        nullif(trim(OWNER_TYPES), '')                              as owner_types,
        nullif(trim(PRIMARY_OWNER_TYPE), '')                       as primary_owner_type,
        (upper(trim(IS_ASSOCIATED_STRUCTURE)) = 'YES')             as is_associated_structure,
        nullif(trim(PRIMARY_PURPOSE), '')                          as primary_purpose,
        nullif(trim(PURPOSES), '')                                 as purposes,
        nullif(trim(SOURCE_AGENCY), '')                            as source_agency,
        try_to_double(LATITUDE)                                    as latitude,
        try_to_double(LONGITUDE)                                   as longitude,
        nullif(trim(STATE), '')                                    as state,
        nullif(trim(COUNTY), '')                                   as county,
        nullif(trim(CITY), '')                                     as city,
        nullif(trim(RIVER_OR_STREAM_NAME), '')                     as river_or_stream,
        nullif(trim(CONGRESSIONAL_DISTRICT), '')                   as congressional_district,
        (upper(trim(STATE_REGULATED_DAM)) = 'YES')                 as is_state_regulated,
        (upper(trim(FEDERALLY_REGULATED_DAM)) = 'YES')             as is_federally_regulated,
        nullif(trim(STATE_REGULATORY_AGENCY), '')                  as state_regulatory_agency,
        nullif(trim(FEDERAL_AGENCY_OWNERS), '')                    as federal_agency_owners,
        nullif(trim(PRIMARY_DAM_TYPE), '')                         as primary_dam_type,
        try_to_number(NID_HEIGHT_FT)                               as nid_height_ft,
        nullif(trim(NID_HEIGHT_CATEGORY), '')                      as nid_height_category,
        try_to_number(DAM_LENGTH_FT)                               as dam_length_ft,
        try_to_number(YEAR_COMPLETED)                              as year_completed,
        try_to_double(NID_STORAGE_ACRE_FT)                         as nid_storage_acre_ft,
        try_to_double(MAX_STORAGE_ACRE_FT)                         as max_storage_acre_ft,
        try_to_double(NORMAL_STORAGE_ACRE_FT)                      as normal_storage_acre_ft,
        try_to_double(SURFACE_AREA_ACRES)                          as surface_area_acres,
        try_to_double(DRAINAGE_AREA_SQ_MILES)                      as drainage_area_sq_miles,
        try_to_double(MAX_DISCHARGE_CUBIC_FT_SECOND)               as max_discharge_cfs,
        nullif(trim(SPILLWAY_TYPE), '')                            as spillway_type,
        try_to_date(nullif(trim(DATA_LAST_UPDATED), ''), 'MM/DD/YYYY')     as data_last_updated,
        try_to_date(nullif(trim(LAST_INSPECTION_DATE), ''), 'MM/DD/YYYY')  as last_inspection_date,
        nullif(trim(INSPECTION_FREQUENCY), '')                     as inspection_frequency,
        nullif(trim(HAZARD_POTENTIAL_CLASSIFICATION), '')          as hazard_potential,
        nullif(trim(CONDITION_ASSESSMENT), '')                     as condition_assessment,
        try_to_date(nullif(trim(CONDITION_ASSESSMENT_DATE), ''), 'MM/DD/YYYY') as condition_assessment_date,
        nullif(trim(OPERATIONAL_STATUS), '')                       as operational_status,
        (upper(trim(EAP_PREPARED)) = 'YES')                        as has_emergency_action_plan,
        try_to_date(nullif(trim(EAP_LAST_REVISION_DATE), ''), 'MM/DD/YYYY') as eap_last_revision_date,
        to_timestamp_ntz(_INGESTED_AT, 6)                          as _ingested_at,
        nullif(trim(_SOURCE_RUN_ID), '')                           as _source_run_id
    from source
)

select * from renamed
