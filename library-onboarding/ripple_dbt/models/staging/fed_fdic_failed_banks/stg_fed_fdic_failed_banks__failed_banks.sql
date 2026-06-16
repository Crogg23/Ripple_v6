{{ config(materialized='view') }}

with source as (

    select * from {{ source('ripple_raw', 'FED_FDIC_FAILED_BANKS') }}

),

renamed_cast as (

    select

        -- primary / foreign keys
        trim(cert)                                              as fdic_cert,
        trim(cert_fips)                                         as fips,

        -- identifiers & descriptors
        trim(id)                                                as fdic_failure_record_id,
        trim(fin)                                               as financial_institution_number,
        trim(name)                                              as bank_name,
        trim(city)                                              as city,
        trim(stalp)                                             as state_abbr,
        trim(stname)                                            as state_name,
        trim(cityst)                                            as city_state,
        trim(charter)                                           as charter_type,
        trim(acqinst)                                           as acquiring_institution,

        -- supervisory / resolution
        trim(savr)                                              as supervisory_agency_code,
        trim(restype)                                           as resolution_type,
        trim(restype1)                                          as resolution_type_detail,

        -- dates
        coalesce(
            try_to_date(trim(faildate), 'YYYY-MM-DD'),
            try_to_date(trim(faildate), 'MM/DD/YYYY')
        )                                                       as fail_date,

        coalesce(
            try_to_date(trim(insdate), 'YYYY-MM-DD'),
            try_to_date(trim(insdate), 'MM/DD/YYYY')
        )                                                       as insured_date,

        -- financial figures (in thousands)
        try_to_number(regexp_replace(trim(qbfasset), '[^0-9.\-]', ''))  as total_assets_thousands,
        try_to_number(regexp_replace(trim(qbfdep),   '[^0-9.\-]', ''))  as total_deposits_thousands,
        try_to_number(regexp_replace(trim(cost),     '[^0-9.\-]', ''))  as estimated_loss_thousands,

        -- metadata
        current_timestamp()                                     as _ingested_at,
        null::varchar                                           as _source_run_id

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by fdic_cert
            order by fail_date desc nulls last
        ) as _row_num
    from renamed_cast

)

select
    fdic_cert,
    fips,
    fdic_failure_record_id,
    financial_institution_number,
    bank_name,
    city,
    state_abbr,
    state_name,
    city_state,
    charter_type,
    acquiring_institution,
    supervisory_agency_code,
    resolution_type,
    resolution_type_detail,
    fail_date,
    insured_date,
    total_assets_thousands,
    total_deposits_thousands,
    estimated_loss_thousands,
    _ingested_at,
    _source_run_id
from deduped
where _row_num = 1
