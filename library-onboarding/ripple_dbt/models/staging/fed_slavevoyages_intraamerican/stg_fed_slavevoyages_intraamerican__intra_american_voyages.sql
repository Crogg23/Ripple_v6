{{ config(materialized='view') }}

with source as (

    select *
    from {{ source('ripple_raw', 'FED_SLAVEVOYAGES_INTRAAMERICAN') }}

),

renamed as (

    select
        -- surrogate / source keys
        VOYAGE_ID                                                        as voyage_id,

        -- dates
        try_to_number(YEAR_OF_DEPARTURE)                                 as year_of_departure,
        try_to_date(DATE_OF_DEPARTURE)                                   as date_of_departure,

        -- geography
        PORT_OF_DEPARTURE                                                as port_of_departure,
        PORT_OF_ARRIVAL                                                  as port_of_arrival,
        COUNTRY_OF_DEPARTURE                                             as country_of_departure,
        COUNTRY_OF_ARRIVAL                                               as country_of_arrival,

        -- measures
        try_to_number(NUM_ENSLAVED_EMBARKED)                             as num_enslaved_embarked,
        try_to_number(NUM_ENSLAVED_DISEMBARKED)                          as num_enslaved_disembarked,

        -- descriptive
        VESSEL_NAME                                                      as vessel_name,
        CAPTAIN_NAME                                                     as captain_name,
        SLAVE_TRADE_COMPANY                                              as slave_trade_company,
        SOURCE_CITATION                                                  as source_citation,

        -- raw / audit
        DOCTYPE_HTML                                                     as doctype_html,
        current_timestamp()                                              as _ingested_at,
        cast(null as varchar)                                            as _source_run_id

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by voyage_id
            order by _ingested_at desc
        ) as _row_num
    from renamed

)

select
    voyage_id,
    year_of_departure,
    date_of_departure,
    port_of_departure,
    port_of_arrival,
    country_of_departure,
    country_of_arrival,
    num_enslaved_embarked,
    num_enslaved_disembarked,
    vessel_name,
    captain_name,
    slave_trade_company,
    source_citation,
    doctype_html,
    _ingested_at,
    _source_run_id
from deduped
where _row_num = 1
