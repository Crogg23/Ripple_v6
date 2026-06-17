{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_FJC_IDB') }}

),

renamed_cast as (

    select

        -- identifiers
        circuit                                         as circuit,
        district                                        as district,
        office                                          as office,
        docket                                          as docket,
        judge                                           as judge,

        -- derived case_id (surrogate on stable business fields)
        {{ dbt_utils.generate_surrogate_key(['circuit', 'district', 'office', 'docket']) }}
                                                        as case_id,

        -- dates
        try_to_date(filedate, 'YYYYMMDD')               as file_date,
        try_to_date(termdate, 'YYYYMMDD')               as term_date,

        -- numeric fields
        try_to_number(origin)                           as origin_code,
        try_to_number(judgment)                         as judgment_code,
        try_to_number(nos)                              as nature_of_suit_code,
        try_to_number(juris)                            as jurisdiction_code,
        try_to_number(prose)                            as prose_code,
        try_to_number(gender)                           as gender_code,
        try_to_number(criminal_count)                   as criminal_count,
        try_to_number(stat_year)                        as stat_year,
        try_to_number(tapeyear)                         as tape_year,
        try_to_number(disp)                             as disposition_code,
        try_to_double(amtrec)                           as amount_received,
        try_to_number(section)                          as section_code,
        try_to_number(subsection)                       as subsection_code,

        -- metadata
        _ingested_at,
        _source_run_id

    from source

),

deduped as (

    select *
    from renamed_cast
    qualify row_number() over (
        partition by case_id
        order by _ingested_at desc
    ) = 1

)

select * from deduped
