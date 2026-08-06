{{ config(tags=['spine_generated']) }}

-- GRAIN: one row per Form 8871 submission (FORM_ID_NUMBER is unique and the natural
-- key). SPINE_ENTITY: not determined -- no registry hint. EIN is the join key to
-- other IRS/EIN-keyed sources but is NOT unique per row (an org can refile).

with source as (

    select * from {{ source('ripple_raw', 'IRS527_8871_ORGS') }}

),

renamed as (

    select
        FORM_ID_NUMBER as form_id_number,
        EIN as ein,
        ORGANIZATION_NAME as organization_name,
        INITIAL_REPORT_IND as initial_report_ind,
        AMENDED_REPORT_IND as amended_report_ind,
        FINAL_REPORT_IND as final_report_ind,
        try_to_date(ESTABLISHED_DATE, 'YYYYMMDD') as established_date,
        MAILING_ADDR1 as mailing_addr1,
        MAILING_CITY as mailing_city,
        MAILING_STATE as mailing_state,
        MAILING_ZIP as mailing_zip,
        EMAIL_ADDRESS as email_address,
        CUSTODIAN_NAME as custodian_name,
        CONTACT_NAME as contact_name,
        EXEMPT_8872_IND as exempt_8872_ind,
        EXEMPT_990_IND as exempt_990_ind,
        PURPOSE as purpose,
        try_to_timestamp(INSERT_DATETIME, 'YYYY-MM-DD HH24:MI:SS') as insert_datetime,
        INGESTED_AT as _loaded_at,
        'https://www.irs.gov/charities-non-profits/political-organizations/political-organization-filing-and-disclosure' as _source_url

    from source

)

select * from renamed
qualify row_number() over (partition by form_id_number order by _loaded_at desc) = 1
