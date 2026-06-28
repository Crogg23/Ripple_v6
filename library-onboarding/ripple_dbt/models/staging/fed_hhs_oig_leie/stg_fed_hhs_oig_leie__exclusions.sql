{{ config(materialized='view') }}

{#
    OIG LEIE -- List of Excluded Individuals/Entities (current-exclusions file).
    Two landmines from the 2026-06-27 discovery sweep (findings #1, #15):

      (1) EXCLDATE / REINDATE / WAIVERDATE are 'YYYYMMDD' TEXT. TRY_CAST(... AS
          DATE) reads the 8-digit string as an epoch-day INT and collapses all
          83,464 rows into ~7 garbage 1970 dates. Parse with parse_yyyymmdd(),
          which uses TO_DATE(...,'YYYYMMDD').

      (2) NPI is the literal placeholder '0000000000' on 89.6% of rows (74,780 of
          83,464). A naive [0-9]{10} regex PASSES the placeholder and would falsely
          promote name-only matches to FACT-grade NPI joins. clean_npi() nulls it,
          so a non-null npi means a real, hard-ID-grade NPI (8,684 rows / 8,503
          distinct). The remaining ~90% can only be name/EIN/address matched =>
          LEAD-grade joins only (see npi_is_real flag below).

    Structural note (#15): REINDATE is '00000000' on 100% of rows -- this is the
    CURRENT exclusions snapshot, it records zero reinstatements. WAIVERDATE is real
    on only 3 rows; WVRSTATE is set on only 4. Carried through anyway so downstream
    can stay waiver-aware.

    LEIE has NO single clean unique key (NPI is mostly placeholder; no row id).
    Dedup on the full business key NPI+LASTNAME+FIRSTNAME+BUSNAME+EXCLDATE -- that
    leaves 95 true duplicate rows across 83,464 (verified), which we collapse to
    the most-recently-ingested copy. A surrogate hash of that key (exclusion_sk) is
    unique post-dedup and is the model's primary key.
#}

with source as (

    select * from {{ source('ripple_raw', 'FED_HHS_OIG_LEIE') }}

),

renamed_cast as (

    select

        -- entity name / type fields
        nullif(trim(LASTNAME), '')                          as last_name,
        nullif(trim(FIRSTNAME), '')                         as first_name,
        nullif(trim(MIDNAME), '')                           as middle_name,
        nullif(trim(BUSNAME), '')                           as business_name,
        nullif(trim(GENERAL), '')                           as general_category,
        nullif(trim(SPECIALTY), '')                         as specialty,

        -- identifiers
        nullif(trim(UPIN), '')                              as upin,
        {{ clean_npi('NPI') }}                              as npi,
        nullif(trim(DOB), '')                               as date_of_birth_raw,

        -- address
        nullif(trim(ADDRESS), '')                           as address,
        nullif(trim(CITY), '')                              as city,
        nullif(trim(STATE), '')                             as state,
        nullif(trim(ZIP), '')                               as zip,

        -- exclusion detail
        nullif(trim(EXCLTYPE), '')                          as exclusion_type,
        {{ parse_yyyymmdd('EXCLDATE') }}                    as exclusion_date,

        -- reinstatement / waiver (mostly placeholder in the current file)
        {{ parse_yyyymmdd('REINDATE') }}                    as reinstatement_date,
        {{ parse_yyyymmdd('WAIVERDATE') }}                  as waiver_date,
        nullif(trim(WVRSTATE), '')                          as waiver_state,

        -- raw key parts retained for the business key / dedup
        nullif(trim(EXCLDATE), '')                          as exclusion_date_raw,

        -- pipeline audit columns
        to_timestamp_ntz(_INGESTED_AT)                      as _ingested_at,
        nullif(trim(_SOURCE_RUN_ID), '')                    as _source_run_id

    from source

),

flagged as (

    select
        *,

        -- TRUE only when a real (non-placeholder, non-blank) NPI is present.
        -- npi_is_real = FALSE  =>  row can ONLY be name/EIN/address matched
        -- downstream (LEAD-grade joins). Do NOT join on npi when this is FALSE.
        (npi is not null)                                   as npi_is_real,

        -- waiver-aware: a granted waiver exists for this exclusion
        (waiver_date is not null or waiver_state is not null) as has_waiver,

        -- surrogate primary key over the full business key. LEIE has no native
        -- unique id, so we hash the natural key. Unique after dedup below.
        {{ dbt_utils.generate_surrogate_key([
            'npi',
            'last_name',
            'first_name',
            'business_name',
            'exclusion_date_raw'
        ]) }}                                               as exclusion_sk

    from renamed_cast

),

deduped as (

    select
        *,
        row_number() over (
            partition by exclusion_sk
            order by _ingested_at desc nulls last
        ) as _row_num
    from flagged

)

select * exclude (_row_num)
from deduped
where _row_num = 1
