{{ config(materialized='view') }}

with source as (

    select * from {{ source('ripple_raw', 'INTL_GR_GEMI') }}

),

renamed as (

    select

        -- key identifiers
        GEMI_NUMBER                                    as gemi_number,
        AFM                                            as afm,

        -- company attributes
        COMPANY_NAME                                   as company_name,
        DISTINCTIVE_TITLE                              as distinctive_title,
        LEGAL_FORM                                     as legal_form,
        STATUS                                         as status,
        REGISTRATION_SUSPENSION                        as registration_suspension,
        SPECIAL_DESIGNATIONS                           as special_designations,
        LOCAL_GEMI_OFFICE                              as local_gemi_office,

        -- dates
        try_to_date(FORMATION_DATE)                    as formation_date,
        try_to_date(CLOSURE_DATE)                      as closure_date,
        try_to_date(KAK_CHANGE_DATE)                   as kak_change_date,

        -- location
        CITY                                           as city,
        POSTAL_CODE                                    as postal_code,

        -- metadata
        _ingested_at,
        _source_run_id

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by gemi_number
            order by _ingested_at desc
        ) as _row_num
    from renamed
    where gemi_number is not null

)

select
    gemi_number,
    afm,
    company_name,
    distinctive_title,
    legal_form,
    status,
    registration_suspension,
    special_designations,
    local_gemi_office,
    formation_date,
    closure_date,
    kak_change_date,
    city,
    postal_code,
    _ingested_at,
    _source_run_id
from deduped
where _row_num = 1
