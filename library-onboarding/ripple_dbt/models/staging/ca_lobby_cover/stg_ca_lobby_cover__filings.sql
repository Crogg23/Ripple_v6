{{ config(tags=['spine_generated']) }}

-- GRAIN: one row per lobbying disclosure filing (FILING_ID is the natural key).
-- SPINE_ENTITY: not determined -- no registry hint. FILER_ID prefix (L/E/F/C)
-- distinguishes individual lobbyist / employer / firm / committee filer types.

with source as (

    select * from {{ source('ripple_raw', 'CA_LOBBY_COVER') }}

),

renamed as (

    select
        FILING_ID as filing_id,
        AMEND_ID as amend_id,
        REC_TYPE as rec_type,
        FORM_TYPE as form_type,
        FILER_ID as filer_id,
        ENTITY_CD as entity_cd,
        FILER_NAML as filer_naml,
        FILER_NAMF as filer_namf,
        REPORT_NUM as report_num,
        try_to_timestamp(RPT_DATE, 'MM/DD/YYYY HH12:MI:SS AM') as rpt_date,
        try_to_timestamp(FROM_DATE, 'MM/DD/YYYY HH12:MI:SS AM') as from_date,
        try_to_timestamp(THRU_DATE, 'MM/DD/YYYY HH12:MI:SS AM') as thru_date,
        FIRM_ID as firm_id,
        FIRM_NAME as firm_name,
        FIRM_CITY as firm_city,
        FIRM_ST as firm_st,
        LBY_ACTVTY as lobbying_activity,
        INGESTED_AT as _loaded_at,
        'https://www.sos.ca.gov/campaign-lobbying/cal-access-resources/raw-data-campaign-finance-and-lobbying-activity' as _source_url

    from source

)

select * from renamed
qualify row_number() over (partition by filing_id order by _loaded_at desc) = 1
