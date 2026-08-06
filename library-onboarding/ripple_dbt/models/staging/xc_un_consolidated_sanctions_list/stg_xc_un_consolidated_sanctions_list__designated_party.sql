{{ config(materialized='view') }}

with source as (

    select * from {{ source('ripple_raw', 'XC_UN_CONSOLIDATED_SANCTIONS_LIST') }}

),

renamed_cast as (

    select
        -- key identifiers
        DATAID                                              as dataid,
        REFERENCE_NUMBER                                    as reference_number,

        -- descriptive fields
        RECORD_TYPE                                         as record_type,
        try_to_number(VERSIONNUM)                           as version_num,
        FIRST_NAME                                          as first_name,
        SECOND_NAME                                         as second_name,
        THIRD_NAME                                          as third_name,
        FOURTH_NAME                                         as fourth_name,
        NAME_ORIGINAL_SCRIPT                                as name_original_script,
        TITLE                                               as title,
        GENDER                                              as gender,
        UN_LIST_TYPE                                        as un_list_type,
        LIST_TYPE                                           as list_type,
        DESIGNATION                                         as designation,
        NATIONALITY                                         as nationality,
        COMMENTS1                                           as comments,

        -- interpol
        case
            when upper(trim(HAS_INTERPOL_LINK)) in ('TRUE','YES','1','Y') then true
            when upper(trim(HAS_INTERPOL_LINK)) in ('FALSE','NO','0','N') then false
            else null
        end                                                 as has_interpol_link,
        INTERPOL_LINK                                       as interpol_link,

        -- dates
        try_to_date(LISTED_ON)                              as listed_on,
        try_to_date(LAST_DAY_UPDATED)                       as last_day_updated,
        try_to_date(LAST_REVIEWED_ON)                       as last_reviewed_on,

        -- sort keys
        SORT_KEY                                            as sort_key,
        SORT_KEY_LAST_MOD                                   as sort_key_last_mod,

        -- semi-structured / multi-value text fields (stored as JSON strings in source)
        INDIVIDUAL_ALIAS                                    as individual_alias,
        INDIVIDUAL_ADDRESS                                  as individual_address,
        INDIVIDUAL_DATE_OF_BIRTH                            as individual_date_of_birth,
        INDIVIDUAL_PLACE_OF_BIRTH                           as individual_place_of_birth,
        INDIVIDUAL_DOCUMENT                                 as individual_document,
        ENTITY_ALIAS                                        as entity_alias,
        ENTITY_ADDRESS                                      as entity_address,

        -- pipeline metadata
        _ingested_at                                        as _ingested_at,
        _source_run_id                                      as _source_run_id,

        -- dedup helper
        row_number() over (
            partition by DATAID, REFERENCE_NUMBER
            order by _ingested_at desc
        )                                                   as _row_num

    from source

),

deduped as (

    select * from renamed_cast
    where _row_num = 1

)

select
    dataid,
    reference_number,
    record_type,
    version_num,
    first_name,
    second_name,
    third_name,
    fourth_name,
    name_original_script,
    title,
    gender,
    un_list_type,
    list_type,
    designation,
    nationality,
    comments,
    has_interpol_link,
    interpol_link,
    listed_on,
    last_day_updated,
    last_reviewed_on,
    sort_key,
    sort_key_last_mod,
    individual_alias,
    individual_address,
    individual_date_of_birth,
    individual_place_of_birth,
    individual_document,
    entity_alias,
    entity_address,
    _ingested_at,
    _source_run_id
from deduped
