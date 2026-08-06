{{ config(tags=['spine_generated']) }}

-- GRAIN: one row per Form 8871 registration submission (SUBMISSION_ID is the natural
-- key). A section-527 political org files a NEW 8871 record on registration and again
-- on amendment, so EIN is NOT unique here -- multiple rows per org are expected
-- (58,916 distinct EIN vs 77,591 total rows landed). Use latest-by-filed-date per EIN
-- downstream if only the current registration is wanted.
-- SPINE_ENTITY: not determined -- EIN is a candidate join key to fed_irs_eo_bmf / fed_irs_bmf.

with source as (

    select * from {{ source('ripple_raw', 'FED_IRS_527_ORGS') }}

),

renamed as (

    select
        SUBMISSION_ID as submission_id,
        EIN as ein,
        ORG_NAME as org_name,
        MAIL_ADDR1 as mail_address1,
        MAIL_ADDR2 as mail_address2,
        MAIL_CITY as mail_city,
        MAIL_STATE as mail_state,
        MAIL_ZIP as mail_zip,
        EMAIL as email,
        CUSTODIAN_NAME as custodian_name,
        CUSTODIAN_CITY as custodian_city,
        CUSTODIAN_STATE as custodian_state,
        CONTACT_NAME as contact_name,
        CONTACT_CITY as contact_city,
        CONTACT_STATE as contact_state,
        PURPOSE as purpose,
        try_to_timestamp(FILED_DATE, 'YYYY-MM-DD HH24:MI:SS') as filed_date,
        AMENDED_FLAG as amended_flag,
        STATUS_FLAG as status_flag,
        _INGESTED_AT as _loaded_at,
        'https://forms.irs.gov/app/pod/dataDownload/fullData' as _source_url

    from source
    where REC_TYPE = '1'

)

select * from renamed
qualify row_number() over (partition by submission_id order by _loaded_at desc) = 1
