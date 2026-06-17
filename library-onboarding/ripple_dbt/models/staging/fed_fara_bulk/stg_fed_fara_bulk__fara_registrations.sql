{{ config(materialized='view') }}

with source as (

    select * from {{ source('ripple_raw', 'FED_FARA_BULK') }}

),

renamed as (

    select
        -- identifiers
        registration_number                                        as registration_number,
        name                                                       as person_name,
        business_name                                              as company_name,
        state                                                      as state,

        -- dates
        try_to_date(registration_date, 'MM/DD/YYYY')               as registration_date,
        try_to_date(termination_date, 'MM/DD/YYYY')                as termination_date,
        try_to_date(date_stamped, 'MM/DD/YYYY')                    as date_stamped,
        try_to_date(registrant_date, 'MM/DD/YYYY')                 as registrant_date,
        try_to_date(short_form_date, 'MM/DD/YYYY')                 as short_form_date,
        try_to_date(short_form_termination_date, 'MM/DD/YYYY')     as short_form_termination_date,
        try_to_date(foreign_principal_registration_date,
                    'MM/DD/YYYY')                                  as foreign_principal_registration_date,
        try_to_date(foreign_principal_termination_date,
                    'MM/DD/YYYY')                                  as foreign_principal_termination_date,

        -- address fields
        address_1                                                  as address_1,
        address_2                                                  as address_2,
        city                                                       as city,
        zip                                                        as zip,

        -- document / form fields
        document_type                                              as document_type,
        doc_url                                                    as doc_url,
        source_file                                                as source_file,
        source_link                                                as source_link,

        -- registrant fields
        registrant_name                                            as registrant_name,

        -- short form fields
        short_form_name                                            as short_form_name,
        short_form_last_name                                       as short_form_last_name,
        short_form_first_name                                      as short_form_first_name,

        -- foreign principal fields
        foreign_principal_name                                     as foreign_principal_name,
        foreign_principal_country                                  as foreign_principal_country,
        foreign_principal                                          as foreign_principal,
        country_location_represented                               as country_location_represented,

        -- metadata
        coalesce(
            try_to_date(date_stamped, 'MM/DD/YYYY'),
            current_timestamp()
        )                                                          as _ingested_at,
        source_file                                                as _source_run_id

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by
                registration_number,
                coalesce(person_name, ''),
                coalesce(state, ''),
                coalesce(registration_date::text, '')
            order by _ingested_at desc nulls last
        ) as _row_num
    from renamed

)

select
    -- surrogate / natural key
    {{ dbt_utils.generate_surrogate_key([
        'registration_number',
        'person_name',
        'registration_date',
        'state'
    ]) }}                                                          as fara_registration_key,

    registration_number,
    person_name,
    company_name,
    state,
    registration_date,
    termination_date,
    date_stamped,
    registrant_date,
    short_form_date,
    short_form_termination_date,
    foreign_principal_registration_date,
    foreign_principal_termination_date,
    address_1,
    address_2,
    city,
    zip,
    document_type,
    doc_url,
    source_file,
    source_link,
    registrant_name,
    short_form_name,
    short_form_last_name,
    short_form_first_name,
    foreign_principal_name,
    foreign_principal_country,
    foreign_principal,
    country_location_represented,
    _ingested_at,
    _source_run_id

from deduped
where _row_num = 1
