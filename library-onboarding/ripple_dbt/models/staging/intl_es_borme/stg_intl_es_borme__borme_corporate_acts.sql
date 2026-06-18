{{ config(materialized='view') }}

with source as (

    select *
    from {{ source('ripple_raw', 'INTL_ES_BORME') }}

),

renamed as (

    select
        -- key identifiers
        COMPANY_ID                                         as company_id,
        COUNTRY                                            as country,
        try_to_date(DATE, 'YYYY-MM-DD')                    as date,

        -- descriptive attributes
        BORME_ISSUE_NUMBER                                 as borme_issue_number,
        SECTION                                            as section,
        COMPANY_NAME                                       as company_name,
        ACT_TYPE                                           as act_type,
        ACT_DESCRIPTION                                    as act_description,
        PROVINCE                                           as province,
        CVE                                                as cve,
        PDF_URL                                            as pdf_url,

        -- metadata
        _ingested_at,
        _source_run_id

    from source

),

deduped as (

    select *
    from renamed
    qualify row_number() over (
        partition by company_id, country, date, act_type, cve
        order by _ingested_at desc
    ) = 1

)

select * from deduped
