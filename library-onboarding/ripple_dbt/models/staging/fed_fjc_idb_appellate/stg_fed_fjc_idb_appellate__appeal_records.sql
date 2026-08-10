{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_FJC_IDB_APPELLATE') }}

),

renamed as (

    select

        -- identifiers: (CIRCUIT, DOCKET, REOPEN, TAPEYEAR, DKTDATE) is exactly
        -- unique in the landing data, so no tiebreaker is needed. The key is
        -- built on the raw text values before any date parsing.
        {{ dbt_utils.generate_surrogate_key(['CIRCUIT', 'DOCKET', 'REOPEN', 'TAPEYEAR', 'DKTDATE']) }} as appeal_record_id,
        trim(CIRCUIT)                                  as circuit,
        trim(DOCKET)                                   as docket,
        trim(REOPEN)                                   as reopen,
        trim(TAPEYEAR)                                 as tape_year,
        try_to_date(trim(DKTDATE))                     as docket_date,

        -- parties
        trim(USAPT)                                    as us_appellant,
        trim(APPELLAN)                                 as appellant,
        trim(USAPE)                                    as us_appellee,
        trim(APPELLEE)                                 as appellee,

        -- appeal characteristics
        trim(APPTYPE)                                  as appeal_type,
        trim(ORGPROC)                                  as originating_proceeding,
        trim(AGENCY)                                   as agency,
        trim(JURIS)                                    as jurisdiction,
        trim(NOS)                                      as nature_of_suit,
        trim(OFFENSE)                                  as offense,

        -- originating district case
        trim(DCIRC)                                    as district_circuit,
        trim(DDIST)                                    as district_court,
        trim(DOFFICE)                                  as district_office,
        trim(DDOCKET)                                  as district_docket,
        trim(DDEFNUM)                                  as district_defendant_number,
        trim(FEDCAP)                                   as federal_capacity,
        try_to_date(trim(DDKTDATE))                    as district_docket_date,
        try_to_date(trim(APPDATE))                     as appeal_date,
        try_to_date(trim(TRANSDATE))                   as transfer_date,
        trim(TRANSCODE)                                as transfer_code,
        trim(DJUDGE)                                   as district_judge,
        trim(FILEFEE)                                  as filing_fee_status,

        -- disposition
        trim(DISP)                                     as disposition,
        trim(OUTCOME)                                  as outcome,
        trim(PROCTERM)                                 as procedural_termination,
        trim(METHOD)                                   as method,
        trim(PUBSTAT)                                  as publication_status,
        trim(OPDISP)                                   as opinion_disposition,
        trim(JOINAPP)                                  as joint_appeal,
        trim(CONSDKT)                                  as consolidated_docket,

        -- milestones
        try_to_date(trim(CRECDATE))                    as court_record_date,
        trim(BRFILED)                                  as briefs_filed,
        try_to_date(trim(SUBDATE))                     as submission_date,
        try_to_date(trim(HEARDATE))                    as hearing_date,
        try_to_date(trim(JUDGDATE))                    as judgment_date,
        trim(OPINION)                                  as opinion,

        -- panel judges
        trim(JDGCODE1)                                 as judge_code_1,
        trim(JDG1INV)                                  as judge_1_involvement,
        trim(JDGCODE2)                                 as judge_code_2,
        trim(JDG2INV)                                  as judge_2_involvement,
        trim(JDGCODE3)                                 as judge_code_3,
        trim(JDG3INV)                                  as judge_3_involvement,

        -- status
        trim(PROSEFLE)                                 as pro_se_filed,
        trim(PROSETRM)                                 as pro_se_terminated,
        trim(STATUSCD)                                 as status_code,
        trim(ENBANC)                                   as en_banc,
        trim(TRMTYPE)                                  as termination_type,
        trim(TORPROCSUB)                               as termination_or_procedural_submission,
        trim(TRMFEE)                                   as termination_fee_status,

        -- metadata
        _ingested_at,
        _source_run_id

    from source

)

select * from renamed
