{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_DOL_OLMS') }}

),

keyed as (

    -- RPT_ID is NEAR-unique (617,553 distinct of 617,710 rows). The handful of
    -- collisions are genuinely distinct records, NOT exact dupes, so a
    -- row_number() over the full-row hash is appended as a deterministic
    -- provenance tiebreaker to make filing_record_id fully unique.
    select
        source.*,
        {{ dbt_utils.generate_surrogate_key(['RPT_ID']) }}
            || '-'
            || row_number() over (
                   partition by RPT_ID
                   order by hash(*)
               ) as filing_record_id
    from source

),

renamed as (

    select

        -- identifiers
        filing_record_id,
        trim(RPT_ID)                                   as rpt_id,
        -- F_NUM is the OLMS file number: the stable union-entity key that
        -- links a union's filings across years.
        trim(F_NUM)                                    as file_number,
        trim(FORM_TYPE)                                as form_type,
        trim(REPORT_YEAR)                              as report_year_raw,
        try_to_number(trim(YR_COVERED))                as year_covered,

        -- union identity
        trim(UNION_NAME)                               as union_name,
        trim(AFF_ABBR)                                 as affiliation_abbr,
        trim(UNIT_NAME)                                as unit_name,
        trim(DESIQ_PRE)                                as designation_prefix,
        trim(DESIG_NUM)                                as designation_number,
        trim(DESIG_SUF)                                as designation_suffix,
        trim(DESIG_NAME)                               as designation_name,
        trim(SUBSIDIARY)                               as subsidiary,

        -- filing period / lifecycle dates
        trim(FYE)                                      as fiscal_year_end,
        try_to_date(trim(PD_COVERED_FROM))             as period_covered_from,
        try_to_date(trim(PD_COVERED_TO))               as period_covered_to,
        try_to_date(trim(EST_DATE))                    as established_date,
        try_to_date(trim(TERM_DATE))                   as termination_date,
        try_to_date(trim(REGISTER_DATE))               as register_date,
        try_to_date(trim(RECEIVE_DATE))                as receive_date,
        try_to_date(trim(NEXT_ELECTION))               as next_election_date,

        -- financial totals
        try_to_number(trim(TTL_ASSETS))                as total_assets,
        try_to_number(trim(TTL_LIABILITIES))           as total_liabilities,
        try_to_number(trim(TTL_RECEIPTS))              as total_receipts,
        try_to_number(trim(TTL_DISBURSEMENTS))         as total_disbursements,
        try_to_number(trim(MEMBERS))                   as members,
        try_to_number(trim(SHORTAGE))                  as shortage_amount,
        try_to_number(trim(MAXIMUM_BOND))              as maximum_bond,
        try_to_number(trim(NUM_ATTACHMENTS))           as num_attachments,

        -- filing flags / attributes
        trim(CONSTITUTION_BYLAW)                       as constitution_bylaw,
        trim(TERMINATE)                                as terminate_flag,
        trim(AMENDED)                                  as amended_flag,
        trim(AMENDMENT)                                as amendment,
        trim(HARDSHIP)                                 as hardship_flag,
        trim(HAS_TRUST)                                as has_trust,
        trim(PAC_FUNDS)                                as pac_funds,
        trim(OUTSIDE_AUDIT)                            as outside_audit,
        trim(HAS_PROPERTY_CHANGE)                      as has_property_change,
        trim(ASSETS_PLEDGED)                           as assets_pledged,
        trim(CONTINGENT)                               as contingent_liabilities,
        trim(HAS_LIQUIDATED_LIABILITIES)               as has_liquidated_liabilities,
        trim(HAS_EXTENDED_LOAN_CREDIT)                 as has_extended_loan_credit,
        trim(HAS_LIQUIDATED_RECEIVABLES)               as has_liquidated_receivables,
        trim(HAS_SUBSIDIARY)                           as has_subsidiary,
        trim(RECORD_KEPT)                              as records_kept_at,

        -- mailing address / contact
        trim(ADR_ID)                                   as address_id,
        trim(ADDRESS_TYPE)                             as address_type,
        trim(MAIL_FIRSTNAME)                           as mail_first_name,
        trim(MAIL_LASTNAME)                            as mail_last_name,
        trim(BUILD_NUM)                                as building_number,
        trim(STREET_ADR)                               as street_address,
        trim(CITY)                                     as city,
        trim(STATE)                                    as state,
        trim(ZIP)                                      as zip,
        trim(VOICE)                                    as phone,

        -- source-system modification tracking
        try_to_date(trim(MOD_DATE))                    as modified_date,
        trim(MOD_ID)                                   as modified_by_id,

        -- metadata
        _INGESTED_AT                                   as _loaded_at,
        _SOURCE_RUN_ID                                 as _source_run_id,
        _SRC_SHA256                                    as _src_sha256

    from keyed

)

select * from renamed
