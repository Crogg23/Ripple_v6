{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_CMS_OPEN_PAYMENTS_PROFILE_SUPPLEMENT') }}

),

renamed as (

    select

        -- identifiers
        trim(COVERED_RECIPIENT_PROFILE_ID)                        as profile_id,
        trim(ASSOCIATED_COVERED_RECIPIENT_PROFILE_ID_1)           as associated_profile_id_1,
        trim(ASSOCIATED_COVERED_RECIPIENT_PROFILE_ID_2)           as associated_profile_id_2,
        trim(COVERED_RECIPIENT_NPI)                               as npi,

        -- dimensions
        trim(COVERED_RECIPIENT_PROFILE_TYPE)                      as profile_type,
        trim(COVERED_RECIPIENT_PROFILE_FIRST_NAME)                as first_name,
        trim(COVERED_RECIPIENT_PROFILE_MIDDLE_NAME)               as middle_name,
        trim(COVERED_RECIPIENT_PROFILE_LAST_NAME)                 as last_name,
        trim(COVERED_RECIPIENT_PROFILE_SUFFIX)                    as suffix,
        trim(COVERED_RECIPIENT_PROFILE_ALTERNATE_FIRST_NAME)      as alternate_first_name,
        trim(COVERED_RECIPIENT_PROFILE_ALTERNATE_MIDDLE_NAME)     as alternate_middle_name,
        trim(COVERED_RECIPIENT_PROFILE_ALTERNATE_LAST_NAME)       as alternate_last_name,
        trim(COVERED_RECIPIENT_PROFILE_ALTERNATE_SUFFIX)          as alternate_suffix,
        trim(COVERED_RECIPIENT_PROFILE_ADDRESS_LINE_1)            as address_line_1,
        trim(COVERED_RECIPIENT_PROFILE_ADDRESS_LINE_2)            as address_line_2,
        trim(COVERED_RECIPIENT_PROFILE_CITY)                      as city,
        trim(COVERED_RECIPIENT_PROFILE_STATE)                     as state,
        trim(COVERED_RECIPIENT_PROFILE_ZIPCODE)                   as zipcode,
        trim(COVERED_RECIPIENT_PROFILE_COUNTRY_NAME)              as country_name,
        trim(COVERED_RECIPIENT_PROFILE_PROVINCE_NAME)             as province_name,
        trim(COVERED_RECIPIENT_PROFILE_PRIMARY_SPECIALTY)         as primary_specialty,
        trim(COVERED_RECIPIENT_PROFILE_OPS_TAXONOMY_1)            as ops_taxonomy_1,
        trim(COVERED_RECIPIENT_PROFILE_OPS_TAXONOMY_2)            as ops_taxonomy_2,
        trim(COVERED_RECIPIENT_PROFILE_OPS_TAXONOMY_3)            as ops_taxonomy_3,
        trim(COVERED_RECIPIENT_PROFILE_OPS_TAXONOMY_4)            as ops_taxonomy_4,
        trim(COVERED_RECIPIENT_PROFILE_OPS_TAXONOMY_5)            as ops_taxonomy_5,
        trim(COVERED_RECIPIENT_PROFILE_OPS_TAXONOMY_6)            as ops_taxonomy_6,
        trim(COVERED_RECIPIENT_PROFILE_LICENSE_STATE_CODE_1)      as license_state_code_1,
        trim(COVERED_RECIPIENT_PROFILE_LICENSE_STATE_CODE_2)      as license_state_code_2,
        trim(COVERED_RECIPIENT_PROFILE_LICENSE_STATE_CODE_3)      as license_state_code_3,
        trim(COVERED_RECIPIENT_PROFILE_LICENSE_STATE_CODE_4)      as license_state_code_4,
        trim(COVERED_RECIPIENT_PROFILE_LICENSE_STATE_CODE_5)      as license_state_code_5,

        -- metadata
        INGESTED_AT                                               as ingested_at,
        SOURCE_RUN_ID                                             as source_run_id,
        SRC_SHA256                                                as src_sha256

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by profile_id
            order by ingested_at desc
        ) as _row_num
    from renamed
    where profile_id is not null

)

select
    profile_id,
    associated_profile_id_1,
    associated_profile_id_2,
    npi,
    profile_type,
    first_name,
    middle_name,
    last_name,
    suffix,
    alternate_first_name,
    alternate_middle_name,
    alternate_last_name,
    alternate_suffix,
    address_line_1,
    address_line_2,
    city,
    state,
    zipcode,
    country_name,
    province_name,
    primary_specialty,
    ops_taxonomy_1,
    ops_taxonomy_2,
    ops_taxonomy_3,
    ops_taxonomy_4,
    ops_taxonomy_5,
    ops_taxonomy_6,
    license_state_code_1,
    license_state_code_2,
    license_state_code_3,
    license_state_code_4,
    license_state_code_5,
    ingested_at,
    source_run_id,
    src_sha256
from deduped
where _row_num = 1
