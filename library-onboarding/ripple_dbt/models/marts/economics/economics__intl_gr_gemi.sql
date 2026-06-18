{{ config(materialized='table') }}

with base as (

    select * from {{ ref('stg_intl_gr_gemi__greek_companies') }}

),

final as (

    select

        -- surrogate / primary key
        {{ dbt_utils.generate_surrogate_key(['gemi_number']) }}  as company_id,

        -- key identifiers (exposed for cross-source joins)
        gemi_number,
        afm,

        -- descriptive attributes
        company_name,
        distinctive_title,
        legal_form,
        status,
        registration_suspension,
        special_designations,
        local_gemi_office,

        -- dates
        formation_date,
        closure_date,
        kak_change_date,

        -- derived convenience flags
        case
            when closure_date is not null          then true
            else false
        end                                                        as is_closed,

        case
            when lower(status) = 'active'          then true
            else false
        end                                                        as is_active,

        -- location
        city,
        postal_code,

        -- source metadata
        'intl_gr_gemi'                                             as source_id,
        _ingested_at,
        _source_run_id

    from base

)

select * from final
