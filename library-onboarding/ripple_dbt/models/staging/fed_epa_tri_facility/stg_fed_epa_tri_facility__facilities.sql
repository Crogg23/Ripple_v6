{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_EPA_TRI_FACILITY') }}

),

renamed as (

    select

        trim(TRI_FACILITY_ID)                          as tri_facility_id,
        trim(FACILITY_NAME)                            as facility_name,
        trim(STREET_ADDRESS)                           as street_address,
        trim(CITY_NAME)                                as city_name,
        trim(COUNTY_NAME)                              as county_name,
        trim(STATE_COUNTY_FIPS_CODE)                   as state_county_fips_code,
        trim(STATE_ABBR)                               as state_abbr,
        trim(ZIP_CODE)                                 as zip_code,
        trim(REGION)                                   as region,
        trim(FAC_CLOSED_IND)                           as fac_closed_ind,
        trim(MAIL_NAME)                                as mail_name,
        trim(MAIL_STREET_ADDRESS)                      as mail_street_address,
        trim(MAIL_CITY)                                as mail_city,
        trim(MAIL_STATE_ABBR)                          as mail_state_abbr,
        trim(MAIL_PROVINCE)                            as mail_province,
        trim(MAIL_COUNTRY)                             as mail_country,
        trim(MAIL_ZIP_CODE)                            as mail_zip_code,
        trim(ASGN_FEDERAL_IND)                         as asgn_federal_ind,
        trim(ASGN_AGENCY)                              as asgn_agency,
        FRS_ID                                         as frs_id,
        trim(PARENT_CO_DB_NUM)                         as parent_co_db_num,
        trim(PARENT_CO_NAME)                           as parent_co_name,
        try_to_number(trim(FAC_LATITUDE))              as fac_latitude,
        try_to_number(trim(FAC_LONGITUDE))             as fac_longitude,
        try_to_number(trim(PREF_LATITUDE))             as pref_latitude,
        try_to_number(trim(PREF_LONGITUDE))            as pref_longitude,
        trim(PREF_ACCURACY)                            as pref_accuracy,
        trim(PREF_COLLECT_METH)                        as pref_collect_meth,
        trim(PREF_DESC_CATEGORY)                       as pref_desc_category,
        trim(PREF_HORIZONTAL_DATUM)                    as pref_horizontal_datum,
        trim(PREF_SOURCE_SCALE)                        as pref_source_scale,
        trim(PREF_QA_CODE)                             as pref_qa_code,
        trim(ASGN_PARTIAL_IND)                         as asgn_partial_ind,
        trim(ASGN_PUBLIC_CONTACT)                      as asgn_public_contact,
        trim(ASGN_PUBLIC_PHONE)                        as asgn_public_phone,
        trim(ASGN_PUBLIC_CONTACT_EMAIL)                as asgn_public_contact_email,
        trim(BIA_CODE)                                 as bia_code,
        trim(STANDARDIZED_PARENT_COMPANY)              as standardized_parent_company,
        trim(ASGN_PUBLIC_PHONE_EXT)                    as asgn_public_phone_ext,
        trim(EPA_REGISTRY_ID)                          as epa_registry_id,
        ASGN_TECHNICAL_CONTACT                         as asgn_technical_contact,
        ASGN_TECHNICAL_PHONE                           as asgn_technical_phone,
        ASGN_TECHNICAL_PHONE_EXT                       as asgn_technical_phone_ext,
        MAIL                                           as mail,
        ASGN_TECHNICAL_CONTACT_EMAIL                   as asgn_technical_contact_email,
        trim(FOREIGN_PARENT_CO_NAME)                   as foreign_parent_co_name,
        trim(FOREIGN_PARENT_CO_DB_NUM)                 as foreign_parent_co_db_num,
        trim(STANDARDIZED_FOREIGN_PARENT_COMPANY)      as standardized_foreign_parent_company,
        INGESTED_AT                                    as _loaded_at,
        SOURCE_RUN_ID                                  as _source_run_id,
        SRC_SHA256                                     as _src_sha256

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by tri_facility_id
            order by _loaded_at desc
        ) as _row_num
    from renamed
    where tri_facility_id is not null

)

select * exclude (_row_num) from deduped
where _row_num = 1
