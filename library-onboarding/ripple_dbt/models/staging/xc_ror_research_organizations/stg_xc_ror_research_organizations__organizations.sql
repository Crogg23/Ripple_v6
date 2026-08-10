{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'XC_ROR_RESEARCH_ORGANIZATIONS') }}

),

renamed as (

    select

        -- identifiers
        trim(ID)                                              as ror_id,
        trim(EXTERNAL_IDS_TYPE_GRID_PREFERRED)                as grid_id,
        trim(EXTERNAL_IDS_TYPE_GRID_ALL)                      as grid_ids_all,
        trim(EXTERNAL_IDS_TYPE_ISNI_PREFERRED)                as isni_id,
        trim(EXTERNAL_IDS_TYPE_ISNI_ALL)                      as isni_ids_all,
        trim(EXTERNAL_IDS_TYPE_WIKIDATA_PREFERRED)            as wikidata_id,
        trim(EXTERNAL_IDS_TYPE_WIKIDATA_ALL)                  as wikidata_ids_all,
        trim(EXTERNAL_IDS_TYPE_FUNDREF_PREFERRED)             as fundref_id,
        trim(EXTERNAL_IDS_TYPE_FUNDREF_ALL)                   as fundref_ids_all,
        trim(LOCATIONS_GEONAMES_ID)                           as geonames_id,

        -- names
        trim(NAMES_TYPES_ROR_DISPLAY)                         as display_name,
        trim(ROR_DISPLAY_LANG)                                as display_name_lang,
        trim(NAMES_TYPES_LABEL)                               as name_labels,
        trim(NAMES_TYPES_ALIAS)                               as name_aliases,
        trim(NAMES_TYPES_ACRONYM)                             as name_acronyms,

        -- organization attributes
        trim(STATUS)                                          as status,
        trim(TYPES)                                           as org_types,
        try_to_number(trim(ESTABLISHED))                      as established_year,
        trim(DOMAINS)                                         as web_domains,
        trim(LINKS_TYPE_WEBSITE)                              as website_url,
        trim(LINKS_TYPE_WIKIPEDIA)                            as wikipedia_url,
        trim(RELATIONSHIPS)                                   as relationships,

        -- location
        trim(LOCATIONS_GEONAMES_DETAILS_NAME)                 as location_name,
        trim(LOCATIONS_GEONAMES_DETAILS_COUNTRY_CODE)         as country_code,
        trim(LOCATIONS_GEONAMES_DETAILS_COUNTRY_NAME)         as country_name,
        trim(LOCATIONS_GEONAMES_DETAILS_COUNTRY_SUBDIVISION_CODE) as subdivision_code,
        trim(LOCATIONS_GEONAMES_DETAILS_COUNTRY_SUBDIVISION_NAME) as subdivision_name,
        trim(LOCATIONS_GEONAMES_DETAILS_CONTINENT_CODE)       as continent_code,
        trim(LOCATIONS_GEONAMES_DETAILS_CONTINENT_NAME)       as continent_name,
        try_to_double(trim(LOCATIONS_GEONAMES_DETAILS_LAT))   as latitude,
        try_to_double(trim(LOCATIONS_GEONAMES_DETAILS_LNG))   as longitude,

        -- registry admin
        try_to_date(trim(ADMIN_CREATED_DATE))                 as record_created_date,
        try_to_date(trim(ADMIN_LAST_MODIFIED_DATE))           as record_last_modified_date,
        trim(ADMIN_CREATED_SCHEMA_VERSION)                    as created_schema_version,
        trim(ADMIN_LAST_MODIFIED_SCHEMA_VERSION)              as last_modified_schema_version,

        -- metadata (INGESTED_AT is a NUMBER epoch in microseconds)
        to_timestamp_ntz(INGESTED_AT, 6)                      as _loaded_at,
        SOURCE_RUN_ID                                         as _source_run_id,
        SRC_SHA256                                            as _src_sha256

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by ror_id
            order by _loaded_at desc
        ) as _row_num
    from renamed
    where ror_id is not null

)

select * exclude (_row_num)
from deduped
where _row_num = 1
