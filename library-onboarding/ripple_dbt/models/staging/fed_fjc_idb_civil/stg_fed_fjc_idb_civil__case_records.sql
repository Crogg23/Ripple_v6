{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_FJC_IDB_CIVIL') }}

),

keyed as (

    -- The composite (CIRCUIT, DISTRICT, OFFICE, DOCKET, FILEDATE, TAPEYEAR) is
    -- NEAR-unique (10,854,529 distinct of 10,857,396 rows). The 2,867 collisions
    -- are genuinely distinct records differing in other fields, NOT exact dupes,
    -- so a row_number() over the full-row hash is appended as a deterministic
    -- provenance tiebreaker to make case_record_id fully unique.
    select
        source.*,
        {{ dbt_utils.generate_surrogate_key(['CIRCUIT', 'DISTRICT', 'OFFICE', 'DOCKET', 'FILEDATE', 'TAPEYEAR']) }}
            || '-'
            || row_number() over (
                   partition by CIRCUIT, DISTRICT, OFFICE, DOCKET, FILEDATE, TAPEYEAR
                   order by hash(*)
               ) as case_record_id
    from source

),

renamed as (

    select

        -- identifiers
        case_record_id,
        trim(CIRCUIT)                                  as circuit,
        trim(DISTRICT)                                 as district,
        trim(OFFICE)                                   as office,
        trim(DOCKET)                                   as docket,
        trim(TAPEYEAR)                                 as tape_year,

        -- case characteristics
        trim(ORIGIN)                                   as origin,
        try_to_date(nullif(trim(FILEDATE), '01/01/1900'))                    as file_date,
        trim(FDATEUSE)                                 as file_date_use,
        trim(JURIS)                                    as jurisdiction,
        trim(NOS)                                      as nature_of_suit,
        trim(TITL)                                     as statute_title,
        trim(SECTION)                                  as statute_section,
        trim(SUBSECT)                                  as statute_subsection,
        trim(RESIDENC)                                 as residence,
        trim(JURY)                                     as jury_demand,
        trim(CLASSACT)                                 as class_action,
        try_to_number(trim(DEMANDED))                  as amount_demanded,
        trim(FILEJUDG)                                 as filing_judge,
        trim(FILEMAG)                                  as filing_magistrate,
        trim(COUNTY)                                   as county,
        trim(ARBIT)                                    as arbitration,
        trim(MDLDOCK)                                  as mdl_docket,
        trim(PLT)                                      as plaintiff,
        trim(DEF)                                      as defendant,

        -- transfer
        try_to_date(nullif(trim(TRANSDAT), '01/01/1900'))                    as transfer_date,
        trim(TRANSOFF)                                 as transfer_office,
        trim(TRANSDOC)                                 as transfer_docket,
        trim(TRANSORG)                                 as transfer_origin,

        -- termination
        try_to_date(nullif(trim(TERMDATE), '01/01/1900'))                    as term_date,
        trim(TDATEUSE)                                 as term_date_use,
        trim(TRCLACT)                                  as term_class_action,
        trim(TERMJUDG)                                 as term_judge,
        trim(TERMMAG)                                  as term_magistrate,
        trim(PROCPROG)                                 as procedural_progress,
        trim(DISP)                                     as disposition,
        trim(NOJ)                                      as nature_of_judgment,
        try_to_number(trim(AMTREC))                    as amount_received,
        trim(JUDGMENT)                                 as judgment,

        -- milestones
        try_to_date(nullif(trim(DJOINED), '01/01/1900'))                     as issue_joined_date,
        try_to_date(nullif(trim(PRETRIAL), '01/01/1900'))                    as pretrial_date,
        try_to_date(nullif(trim(TRIBEGAN), '01/01/1900'))                    as trial_began_date,
        try_to_date(nullif(trim(TRIALEND), '01/01/1900'))                    as trial_end_date,
        trim(TRMARB)                                   as term_arbitration,
        trim(PROSE)                                    as pro_se,
        trim(IFP)                                      as in_forma_pauperis,
        trim(STATUSCD)                                 as status_code,

        -- metadata
        _ingested_at,
        _source_run_id

    from keyed

)

select * from renamed
