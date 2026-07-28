{{ config(tags=['minimal_staging']) }}

-- GRAIN: one row per holding line (accession_number + infotable_sk)
-- Fix: (1) correct dedup grain (was CUSIP-only, collapsed millions of rows)
--      (2) normalize VALUE: pre-2023 files report in $thousands, post-2023 in $whole
--      SEC rule change effective Jan 2023; file naming pattern is the discriminant.

with source as (

    select * from {{ source('ripple_raw', 'FED_SEC_13F_POSITIONS') }}

),

cleaned as (

    select
        ACCESSION_NUMBER                                as sec_accession_number,
        INFOTABLE_SK                                    as infotable_sk,
        nullif(trim(NAMEOFISSUER), '')                  as issuer_name,
        nullif(trim(TITLEOFCLASS), '')                  as title_of_class,
        nullif(trim(CUSIP), '')                         as cusip,
        nullif(trim(FIGI), '')                          as figi,
        -- Unit normalization: old-format filenames (YYYYqN) = thousands; new = whole dollars
        case
            when _SRC_FILE like '20__q%'
            then try_to_number(VALUE) * 1000
            else try_to_number(VALUE)
        end                                             as value_dollars,
        try_to_number(SSHPRNAMT)                        as shares_or_principal_amount,
        nullif(trim(SSHPRNAMTTYPE), '')                 as shares_or_principal_type,
        nullif(trim(PUTCALL), '')                       as put_call,
        nullif(trim(INVESTMENTDISCRETION), '')          as investment_discretion,
        nullif(trim(OTHERMANAGER), '')                  as other_manager,
        try_to_number(VOTING_AUTH_SOLE)                 as voting_auth_sole,
        try_to_number(VOTING_AUTH_SHARED)               as voting_auth_shared,
        try_to_number(VOTING_AUTH_NONE)                 as voting_auth_none,
        _SRC_FILE                                       as _src_file,
        _INGESTED_AT                                    as _loaded_at,
        _SOURCE_RUN_ID                                  as _source_run_id

    from source

)

select * from cleaned
qualify row_number() over (
    partition by sec_accession_number, infotable_sk
    order by _loaded_at desc
) = 1
