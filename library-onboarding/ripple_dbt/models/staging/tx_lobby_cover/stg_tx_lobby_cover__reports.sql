{{ config(tags=['spine_generated']) }}

-- GRAIN: one row per filed lobby activity cover-sheet report (REPORTINFOIDENT is
-- unique and the natural key). SPINE_ENTITY: not determined -- no registry hint.

with source as (

    select * from {{ source('ripple_raw', 'TX_LOBBY_COVER') }}

),

renamed as (

    select
        REPORTINFOIDENT as report_info_ident,
        FILERIDENT as filer_ident,
        FILERTYPECD as filer_type_cd,
        FILERNAME as filer_name,
        FORMTYPECD as form_type_cd,
        REPORTTYPECD as report_type_cd,
        APPLICABLEYEAR as applicable_year,
        try_to_date(DUEDT, 'YYYYMMDD') as due_dt,
        try_to_date(RECEIVEDDT, 'YYYYMMDD') as received_dt,
        try_to_date(PERIODSTARTDT, 'YYYYMMDD') as period_start_dt,
        try_to_date(PERIODENDDT, 'YYYYMMDD') as period_end_dt,
        try_to_date(FILEDDT, 'YYYYMMDD') as filed_dt,
        TOTALEXPENDTRANSPORTATION as total_expend_transportation,
        TOTALEXPENDFOOD as total_expend_food,
        TOTALEXPENDENTERTAINMENT as total_expend_entertainment,
        TOTALEXPENDGIFT as total_expend_gift,
        TOTALEXPENDAWARD as total_expend_award,
        TOTALEXPENDEVENT as total_expend_event,
        TOTALEXPENDMEDIA as total_expend_media,
        INGESTED_AT as _loaded_at,
        'https://www.ethics.state.tx.us/search/lobby/' as _source_url

    from source

)

select * from renamed
qualify row_number() over (partition by report_info_ident order by _loaded_at desc) = 1
