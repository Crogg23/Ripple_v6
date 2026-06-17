{{ config(materialized='table') }}

with base as (

    select * from {{ ref('stg_fed_fara_bulk__fara_registrations') }}

),

final as (

    select
        -- primary key
        fara_registration_key,

        -- cross-source join identifiers
        registration_number,
        person_name,
        company_name                                               as company_id,
        state,
        registration_date                                          as date,

        -- registration details
        termination_date,
        registrant_name,
        registrant_date,
        document_type,
        doc_url,

        -- address
        address_1,
        address_2,
        city,
        zip,

        -- short form details
        short_form_name,
        short_form_last_name,
        short_form_first_name,
        short_form_date,
        short_form_termination_date,

        -- foreign principal details
        foreign_principal,
        foreign_principal_name,
        foreign_principal_country,
        foreign_principal_registration_date,
        foreign_principal_termination_date,
        country_location_represented,

        -- status flags derived
        case
            when termination_date is not null
                and termination_date <= current_date()
            then false
            else true
        end                                                        as is_active_registration,

        case
            when foreign_principal_termination_date is not null
                and foreign_principal_termination_date <= current_date()
            then false
            else true
        end                                                        as is_active_foreign_principal,

        -- source provenance
        source_file,
        source_link,
        date_stamped,
        _ingested_at,
        _source_run_id

    from base

)

select * from final
