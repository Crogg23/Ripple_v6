{{ config(materialized='view') }}

-- GRAIN: one row = one reported contribution transaction. The composite
-- (RECIPID, COMMITTEE, FILING, REFNO) is EXACTLY unique (197,968 rows =
-- 197,968 distinct, verified live by the orchestrator). contribution_record_id
-- is a surrogate key over that composite.
-- NOTE: this table's ingestion metadata columns have NO leading underscore in
-- the source (INGESTED_AT epoch NUMBER / SOURCE_RUN_ID / SRC_SHA256); renamed
-- to house style here. Dates arrive as TEXT in a non-fixed format, so a
-- permissive try_to_date (no format string) is used.

with source as (

    select * from {{ source('ripple_raw', 'ST_NYC_CFB_CAMPAIGN_2013_CONTRIBUTION') }}

),

keyed as (

    select
        source.*,
        {{ dbt_utils.generate_surrogate_key(['RECIPID', 'COMMITTEE', 'FILING', 'REFNO']) }}
            as contribution_record_id
    from source

),

renamed as (

    select

        -- surrogate key
        contribution_record_id,

        -- business columns
        trim(ELECTION)                                 as election_cycle,
        trim(OFFICECD)                                 as office_code,
        trim(RECIPID)                                  as recipient_id,
        trim(CANCLASS)                                 as candidate_class,
        trim(RECIPNAME)                                as recipient_name,
        trim(COMMITTEE)                                as committee_id,
        trim(FILING)                                   as filing_id,
        trim(SCHEDULE)                                 as schedule,
        PAGENO                                         as page_number,
        SEQUENCENO                                     as sequence_number,
        trim(REFNO)                                    as reference_number,
        try_to_date(trim(DATE))                        as contribution_date,
        try_to_date(trim(REFUNDDATE))                  as refund_date,
        trim(NAME)                                     as contributor_name,
        trim(C_CODE)                                   as contributor_code,
        trim(STRNO)                                    as street_number,
        trim(STRNAME)                                  as street_name,
        trim(APARTMENT)                                as apartment,
        trim(BOROUGHCD)                                as borough_code,
        trim(CITY)                                     as city,
        trim(STATE)                                    as state,
        trim(ZIP)                                      as zip,
        trim(OCCUPATION)                               as occupation,
        trim(EMPNAME)                                  as employer_name,
        trim(EMPSTRNO)                                 as employer_street_number,
        trim(EMPSTRNAME)                               as employer_street_name,
        trim(EMPCITY)                                  as employer_city,
        trim(EMPSTATE)                                 as employer_state,
        try_to_number(trim(AMNT), 18, 2)               as amount,
        try_to_number(trim(MATCHAMNT), 18, 2)          as match_amount,
        try_to_number(trim(PREVAMNT), 18, 2)           as previous_amount,
        trim(PAY_METHOD)                               as payment_method,
        trim(INTERMNO)                                 as intermediary_number,
        trim(INTERMNAME)                               as intermediary_name,
        trim(INTSTRNO)                                 as intermediary_street_number,
        trim(INTSTRNM)                                 as intermediary_street_name,
        trim(INTAPTNO)                                 as intermediary_apartment,
        trim(INTCITY)                                  as intermediary_city,
        trim(INTST)                                    as intermediary_state,
        trim(INTZIP)                                   as intermediary_zip,
        trim(INTEMPNAME)                               as intermediary_employer_name,
        trim(INTEMPSTNO)                               as intermediary_employer_street_number,
        trim(INTEMPSTNM)                               as intermediary_employer_street_name,
        trim(INTEMPCITY)                               as intermediary_employer_city,
        trim(INTEMPST)                                 as intermediary_employer_state,
        trim(INTOCCUPA)                                as intermediary_occupation,
        trim(PURPOSECD)                                as purpose_code,
        trim(EXEMPTCD)                                 as exempt_code,
        trim(ADJTYPECD)                                as adjustment_type_code,
        trim(RR_IND)                                   as rr_indicator,
        trim(SEG_IND)                                  as segregated_indicator,
        trim(INT_C_CODE)                               as intermediary_contributor_code,

        -- metadata (no leading underscore in the source columns for this table)
        to_timestamp_ntz(INGESTED_AT, 6)               as _ingested_at,
        SOURCE_RUN_ID                                  as _source_run_id,
        SRC_SHA256                                     as _src_sha256

    from keyed

)

select * from renamed
