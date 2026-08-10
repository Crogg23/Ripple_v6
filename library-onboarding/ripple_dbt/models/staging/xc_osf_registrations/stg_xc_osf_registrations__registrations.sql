{{ config(materialized='view') }}

-- SAMPLE ONLY: the landing table holds a 10-row proof slice of the much larger
-- OSF registrations registry. The landing table has 370 columns; this staging
-- model keeps a curated useful subset (id, type, title/description/category,
-- dates, tags, registration-state flags, relationship/link ids). The remaining
-- ~300 columns (per-schema ATTRIBUTES_REGISTRATION_RESPONSES_* answer blobs,
-- current-user API context, deep link URLs) were dropped as API-noise; they
-- remain available in the landing table.

with

source as (

    select * from {{ source('ripple_raw', 'XC_OSF_REGISTRATIONS') }}

),

renamed as (

    select

        -- identifiers
        trim(ID)                                              as osf_id,
        trim(TYPE)                                            as record_type,

        -- core attributes
        trim(ATTRIBUTES_TITLE)                                as title,
        trim(ATTRIBUTES_DESCRIPTION)                          as description,
        trim(ATTRIBUTES_CATEGORY)                             as category,
        trim(ATTRIBUTES_TAGS)                                 as tags,
        trim(ATTRIBUTES_REGISTRATION_SUPPLEMENT)              as registration_supplement,
        trim(ATTRIBUTES_REGISTRATION_RESPONSES_SUMMARY)       as registration_responses_summary,
        trim(ATTRIBUTES_REGISTRATION_RESPONSES_UPLOADER)      as registration_responses_uploader,

        -- dates
        try_to_timestamp_ntz(trim(ATTRIBUTES_DATE_CREATED))   as date_created,
        try_to_timestamp_ntz(trim(ATTRIBUTES_DATE_MODIFIED))  as date_modified,
        try_to_timestamp_ntz(trim(ATTRIBUTES_DATE_REGISTERED)) as date_registered,
        ATTRIBUTES_DATE_WITHDRAWN                             as date_withdrawn_raw,
        try_to_timestamp_ntz(trim(ATTRIBUTES_EMBARGO_END_DATE)) as embargo_end_date,

        -- registration state
        ATTRIBUTES_REGISTRATION                               as is_registration,
        ATTRIBUTES_PUBLIC                                     as is_public,
        ATTRIBUTES_FORK                                       as is_fork,
        ATTRIBUTES_WITHDRAWN                                  as is_withdrawn,
        ATTRIBUTES_PENDING_WITHDRAWAL                         as is_pending_withdrawal,
        ATTRIBUTES_PENDING_REGISTRATION_APPROVAL              as is_pending_registration_approval,
        ATTRIBUTES_EMBARGOED                                  as is_embargoed,
        ATTRIBUTES_PENDING_EMBARGO_APPROVAL                   as is_pending_embargo_approval,
        ATTRIBUTES_PENDING_EMBARGO_TERMINATION_APPROVAL       as is_pending_embargo_termination_approval,
        ATTRIBUTES_ARCHIVING                                  as is_archiving,
        trim(ATTRIBUTES_REVIEWS_STATE)                        as reviews_state,
        trim(ATTRIBUTES_REVISION_STATE)                       as revision_state,
        ATTRIBUTES_WITHDRAWAL_JUSTIFICATION                   as withdrawal_justification_raw,

        -- relationship ids (join keys back into the OSF graph)
        trim(RELATIONSHIPS_ROOT_DATA_ID)                      as root_id,
        trim(RELATIONSHIPS_REGISTERED_FROM_DATA_ID)           as registered_from_id,
        trim(RELATIONSHIPS_REGISTERED_BY_DATA_ID)             as registered_by_id,
        trim(RELATIONSHIPS_REGISTRATION_SCHEMA_DATA_ID)       as registration_schema_id,
        trim(RELATIONSHIPS_PROVIDER_DATA_ID)                  as provider_id,
        trim(RELATIONSHIPS_REGION_DATA_ID)                    as region_id,
        trim(RELATIONSHIPS_LICENSE_DATA_ID)                   as license_id,
        trim(RELATIONSHIPS_CITATION_DATA_ID)                  as citation_id,
        trim(RELATIONSHIPS_STORAGE_DATA_ID)                   as storage_id,
        trim(RELATIONSHIPS_ORIGINAL_RESPONSE_DATA_ID)         as original_response_id,
        trim(RELATIONSHIPS_LATEST_RESPONSE_DATA_ID)           as latest_response_id,

        -- canonical links
        trim(LINKS_HTML)                                      as html_url,
        trim(LINKS_SELF)                                      as api_url,
        trim(LINKS_IRI)                                       as iri,

        -- metadata (INGESTED_AT is a NUMBER epoch in microseconds)
        to_timestamp_ntz(INGESTED_AT, 6)                      as _loaded_at,
        SOURCE_RUN_ID                                         as _source_run_id,
        SRC_SHA256                                            as _src_sha256

    from source

)

select * from renamed
where osf_id is not null
