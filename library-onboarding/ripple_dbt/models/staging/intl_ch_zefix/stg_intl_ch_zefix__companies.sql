{{ config(materialized='view') }}

with source as (

    select * from {{ source('ripple_raw', 'INTL_CH_ZEFIX') }}

),

renamed as (

    select
        -- primary / surrogate key
        {{ dbt_utils.generate_surrogate_key(['UID', 'EHRAID', 'CHID']) }} as company_id,

        -- identifiers
        UID                                          as uid,
        EHRAID                                       as ehraid,
        CHID                                         as chid,

        -- core attributes
        NAME                                         as name,
        LEGAL_FORM                                   as legal_form,
        STATUS                                       as status,

        -- address
        ADDRESS_STREET                               as address_street,
        ADDRESS_HOUSE_NUMBER                         as address_house_number,
        ADDRESS_ZIP                                  as address_zip,
        ADDRESS_CITY                                 as address_city,
        ADDRESS_CANTON                               as address_canton,

        -- registration
        REGISTRY_OF_COMMERCE                         as registry_of_commerce,
        OLD_NAMES                                    as old_names,
        try_to_date(SOGC_PUBLICATION_DATE)           as sogc_publication_date,
        MUTATION_TYPE                                as mutation_type,
        try_to_number(COMMUNITY_BFS_ID)              as community_bfs_id,

        -- geography
        COUNTRY                                      as country,

        -- metadata
        _ingested_at,
        _source_run_id

    from source

),

deduped as (

    select *,
        row_number() over (
            partition by company_id
            order by _ingested_at desc
        ) as _row_num
    from renamed

)

select * exclude (_row_num)
from deduped
where _row_num = 1
