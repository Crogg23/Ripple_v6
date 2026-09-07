-- GRAIN: one row per line of the HHS Provider Relief Fund public file,
-- newest load only. 419,846 rows on the 2026-09-07 load.
--
-- The file has four columns and no id. prf_row_id is the file line order
-- inside the newest _SOURCE_RUN_ID, so it is stable for one load and nothing
-- more. Seven lines are exact duplicates of another line; they are kept,
-- because the file does not say whether they are two payments or one typed
-- twice. Payment is a '$1,234' string in landing; payment_amount is the number.
--
-- name_norm: upper, punctuation to spaces, single-spaced. name_key goes one
-- step further and drops a trailing legal suffix (LLC, INC, CORP, CO, LP,
-- LTD, PC, LLP, OPCO, OPERATING, HOLDINGS, THE) so 'FAIRWAY OAKS CENTER, LLC'
-- keys as 'FAIRWAY OAKS CENTER'. name_words counts the words in name_key;
-- the match downstream refuses to trust a one-word key.

with newest as (

    select max(_SOURCE_RUN_ID) as run_id
    from {{ source('ripple_raw', 'FED_HRSA_PROVIDER_RELIEF_FUND') }}
    where _INGESTED_AT = (select max(_INGESTED_AT)
                          from {{ source('ripple_raw', 'FED_HRSA_PROVIDER_RELIEF_FUND') }})

),

source as (

    select s.*
    from {{ source('ripple_raw', 'FED_HRSA_PROVIDER_RELIEF_FUND') }} s
    join newest n on s._SOURCE_RUN_ID = n.run_id

),

renamed as (

    select
        row_number() over (order by STATE, CITY, PROVIDER_NAME, PAYMENT)   as prf_row_id,
        PROVIDER_NAME                                                      as provider_name,
        upper(trim(STATE))                                                 as state,
        upper(trim(CITY))                                                  as city,
        PAYMENT                                                            as payment_raw,
        try_to_number(replace(replace(PAYMENT, '$', ''), ',', ''))         as payment_amount,
        {{ prf_name_norm('PROVIDER_NAME') }}                               as name_norm,
        {{ prf_name_key('PROVIDER_NAME') }}                                as name_key,
        regexp_count({{ prf_name_key('PROVIDER_NAME') }}, ' ') + 1         as name_words,
        _INGESTED_AT                                                       as _loaded_at,
        _SOURCE_RUN_ID                                                     as _source_run_id,
        _SRC_SHA256                                                        as _src_sha256
    from source

)

select * from renamed
