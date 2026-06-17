{{ config(materialized='view') }}

with source as (

    select * from {{ source('ripple_raw', 'FED_CMS_HCRIS') }}

),

renamed_cast as (

    select

        -- identifiers
        provider_number                                         as provider_number,
        npi                                                     as npi,

        -- facility info
        hospital_name                                           as hospital_name,
        street_address                                          as street_address,
        city                                                    as city,
        state                                                   as state,
        zip_code                                                as zip_code,
        county                                                  as county,

        -- fiscal year dates
        try_to_date(fiscal_year_begin_date)                     as fiscal_year_begin_date,
        try_to_date(fiscal_year_end_date)                       as fiscal_year_end_date,
        year(try_to_date(fiscal_year_end_date))                 as fiscal_year,

        -- report metadata
        report_status                                           as report_status,
        rural_versus_urban                                      as rural_versus_urban,
        type_of_control                                         as type_of_control,

        -- utilization metrics
        try_to_number(number_of_beds)                           as number_of_beds,
        try_to_number(total_discharges)                         as total_discharges,
        try_to_number(total_patient_days)                       as total_patient_days,
        try_to_number(medicare_discharges)                      as medicare_discharges,
        try_to_number(medicare_days)                            as medicare_days,
        try_to_number(medicaid_days)                            as medicaid_days,
        try_to_double(fte_employees)                            as fte_employees,

        -- financial metrics
        try_to_double(total_charges)                            as total_charges,
        try_to_double(net_revenue)                              as net_revenue,
        try_to_double(total_costs)                              as total_costs,

        -- dsh
        try_to_double(dsh_percent)                              as dsh_percent,

        -- metadata
        _ingested_at,
        _source_run_id

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by provider_number, fiscal_year
            order by _ingested_at desc
        ) as _row_num
    from renamed_cast

)

select
    -- surrogate key
    {{ dbt_utils.generate_surrogate_key(['provider_number', 'fiscal_year']) }} as hospital_cost_report_key,

    provider_number,
    npi,
    hospital_name,
    street_address,
    city,
    state,
    zip_code,
    county,
    fiscal_year_begin_date,
    fiscal_year_end_date,
    fiscal_year,
    report_status,
    rural_versus_urban,
    type_of_control,
    number_of_beds,
    total_discharges,
    total_patient_days,
    medicare_discharges,
    medicare_days,
    medicaid_days,
    fte_employees,
    total_charges,
    net_revenue,
    total_costs,
    dsh_percent,
    _ingested_at,
    _source_run_id

from deduped
where _row_num = 1
