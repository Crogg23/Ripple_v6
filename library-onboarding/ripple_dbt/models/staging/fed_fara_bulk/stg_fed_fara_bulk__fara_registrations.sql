{{ config(materialized='view') }}

-- HAND-EDITED 2026-09-19: dedupe is a whole-raw-row hash (_row_hash), see the
-- comment in deduped. The staging generator skips files carrying this marker.

with source as (

    -- _row_hash: hash of every landing column except the load stamps, so two
    -- rows share it only when they are exact copies of each other.
    select *, hash(* exclude (_INGESTED_AT, _SOURCE_RUN_ID, _SRC_SHA256)) as _row_hash
    from {{ source('ripple_raw', 'FED_FARA_BULK') }}
    -- 2026-08-25: one row in FARA_All_ForeignPrincipals.csv is column-shifted in
    -- DOJ's own bulk export -- a date ("03/20/2024") sits in registration_number
    -- while name/business_name/city/state/document_type are all blank and an
    -- address (Kyiv, Ukraine) has bled into registrant_name/address_2 instead.
    -- Verified live against the raw file: every other one of the 221,900 rows
    -- has a pure-digit registration_number, so this allowlist drops exactly
    -- that one garbled row (no real registration data survives in it anyway)
    -- before it reaches the ripple_num() cast downstream that would otherwise
    -- silently null the join key.
    where trim(registration_number) rlike '^[0-9]+$'

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
        source_file                                                as _source_run_id,

        -- whole-raw-row hash, carried for the dedupe + surrogate key only
        _row_hash                                                  as _row_hash

    from source

),

deduped as (

    -- 2026-07-28 fix: the original key (registration_number, person_name, state,
    -- registration_date) omitted foreign_principal_name/document_type -- a single
    -- registrant can list multiple foreign principals, or file both long-form and
    -- short-form docs, on the same date. Confirmed live: widening the key recovers
    -- 21,326 -> 48,104 distinct registrations (real rows, not just theoretical --
    -- still short of the 221,900 raw rows, so some further true duplication likely
    -- remains; this is a confirmed improvement, not necessarily the final grain).
    -- 2026-09-19: the 2026-07-28 note above is superseded. That six-column
    -- partition (registration_number, person_name, state, registration_date,
    -- foreign_principal_name, document_type) still hid 173,797 of 221,900
    -- landing rows on a single load -- the key does not identify a row. The
    -- dedupe is now the whole-raw-row hash, so only exact copies are dropped
    -- (444 exact copies in landing).
    select *,
        row_number() over (
            partition by _row_hash
            order by _ingested_at desc nulls last
        ) as _row_num
    from renamed

)

select
    -- surrogate / natural key -- widened 2026-07-28 alongside the dedup partition
    -- above (see comment there); must match or the widened dedup produces
    -- multiple rows sharing one "unique" key, silently breaking the mart's own
    -- unique/not_null tests on fara_registration_key.
    -- 2026-09-19: _row_hash added to the key so it stays one-per-row now that
    -- the dedupe is whole-row (the six business columns alone repeat).
    {{ dbt_utils.generate_surrogate_key([
        'registration_number',
        'person_name',
        'registration_date',
        'state',
        'foreign_principal_name',
        'document_type',
        '_row_hash'
    ]) }}                                                         as fara_registration_key,

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
