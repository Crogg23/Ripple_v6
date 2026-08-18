{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_FJC_IDB_CRIMINAL') }}

),

keyed as (

    -- The composite (DEFLGKY, FISCALYR, REOPSEQ, TAPEYEAR) is NEAR-unique
    -- (6,283,938 distinct of 6,299,908 rows). The collisions are genuinely
    -- distinct records differing in other fields, NOT exact dupes, so a
    -- row_number() over the full-row hash is appended as a deterministic
    -- provenance tiebreaker to make defendant_record_id fully unique.
    select
        source.*,
        {{ dbt_utils.generate_surrogate_key(['DEFLGKY', 'FISCALYR', 'REOPSEQ', 'TAPEYEAR']) }}
            || '-'
            || row_number() over (
                   partition by DEFLGKY, FISCALYR, REOPSEQ, TAPEYEAR
                   order by hash(*)
               ) as defendant_record_id
    from source

),

renamed as (

    select

        -- identifiers
        defendant_record_id,
        trim(DEFLGKY)                                  as defendant_link_key,
        trim(CASLGKY)                                  as case_link_key,
        trim(FISCALYR)                                 as fiscal_year,
        trim(REOPSEQ)                                  as reopen_sequence,
        trim(TAPEYEAR)                                 as tape_year,
        trim(CIRCUIT)                                  as circuit,
        trim(DISTRICT)                                 as district,
        trim(OFFICE)                                   as office,
        trim(DOCKET)                                   as docket,
        trim(DEFNO)                                    as defendant_number,
        trim(CTDEF)                                    as ct_defendants,
        trim(NAME)                                     as defendant_name,

        -- case characteristics
        trim(TYPEREG)                                  as type_reg,
        trim(TYPETRN)                                  as type_trn,
        trim(TYPEMAG)                                  as type_mag,
        trim(MAGDOCK)                                  as magistrate_docket,
        trim(MAGDEF)                                   as magistrate_defendant_number,
        trim(STATUSCD)                                 as status_code,
        trim(FUGSTAT)                                  as fugitive_status,
        try_to_date(trim(FGSTRTDATE))                  as fugitive_start_date,
        try_to_date(trim(FGENDDATE))                   as fugitive_end_date,
        -- NOT A BUG (epoch-1970 investigation, 2026-08-18): file_date/proceeding_date
        -- drive 6,731-of-6,299,908 (0.1%) 1970 rows (confirmed live), spread across
        -- many distinct 1970 dates -- expected, since 1970 is literally the
        -- historical start year of FJC's federal criminal case coverage. LATENT
        -- RISK noted, not fixed: these two casts have no explicit format string,
        -- same shape as the bugs fixed elsewhere in this batch. They happen to be
        -- clean today (source dates already come pre-formatted so the implicit
        -- parse succeeds), but a future source-format change could silently
        -- reintroduce the epoch trap here. Left as-is per the no-guess rule --
        -- there is no live defect to fix.
        try_to_date(trim(FILEDATE))                    as file_date,
        try_to_date(trim(PROCDATE))                    as proceeding_date,
        trim(PROCCD)                                   as proceeding_code,
        try_to_date(trim(APPDATE))                     as app_date,
        trim(APPCD)                                    as app_code,
        trim(FJUDGE)                                   as filing_judge,
        trim(FCOUNSEL)                                 as filing_counsel,

        -- offenses charged at filing (up to 5)
        trim(FTITLE1)                                  as filing_title_1,
        trim(FOFFLVL1)                                 as filing_offense_level_1,
        trim(FOFFCD1)                                  as filing_offense_code_1,
        trim(D2FOFFCD1)                                as d2_filing_offense_code_1,
        trim(FSEV1)                                    as filing_severity_1,
        trim(FTITLE2)                                  as filing_title_2,
        trim(FOFFLVL2)                                 as filing_offense_level_2,
        trim(FOFFCD2)                                  as filing_offense_code_2,
        trim(D2FOFFCD2)                                as d2_filing_offense_code_2,
        trim(FSEV2)                                    as filing_severity_2,
        trim(FTITLE3)                                  as filing_title_3,
        trim(FOFFLVL3)                                 as filing_offense_level_3,
        trim(FOFFCD3)                                  as filing_offense_code_3,
        trim(D2FOFFCD3)                                as d2_filing_offense_code_3,
        trim(FSEV3)                                    as filing_severity_3,
        trim(FTITLE4)                                  as filing_title_4,
        trim(FOFFLVL4)                                 as filing_offense_level_4,
        trim(FOFFCD4)                                  as filing_offense_code_4,
        trim(D2FOFFCD4)                                as d2_filing_offense_code_4,
        trim(FSEV4)                                    as filing_severity_4,
        trim(FTITLE5)                                  as filing_title_5,
        trim(FOFFLVL5)                                 as filing_offense_level_5,
        trim(FOFFCD5)                                  as filing_offense_code_5,
        trim(D2FOFFCD5)                                as d2_filing_offense_code_5,
        trim(FSEV5)                                    as filing_severity_5,

        -- geography / transfer
        trim(COUNTY)                                   as county,
        trim(TRANDIST)                                 as transfer_district,
        trim(TRANOFF)                                  as transfer_office,
        trim(TRANDOCK)                                 as transfer_docket,
        trim(TRANDEF)                                  as transfer_defendant_number,
        trim(C_UPDATE)                                 as c_update,

        -- termination
        try_to_date(trim(DISPDATE))                    as disposition_date,
        try_to_date(trim(SENTDATE))                    as sentence_date,
        try_to_date(trim(TERMDATE))                    as term_date,
        trim(INT1)                                     as int_1,
        trim(INT2)                                     as int_2,
        trim(INT3)                                     as int_3,
        trim(TERMOFF)                                  as term_office,
        trim(TJUDGE)                                   as term_judge,
        trim(TCOUNSEL)                                 as term_counsel,

        -- offenses and sentences at termination (up to 5)
        trim(TTITLE1)                                  as term_title_1,
        trim(TOFFLVL1)                                 as term_offense_level_1,
        trim(TOFFCD1)                                  as term_offense_code_1,
        trim(D2TOFFCD1)                                as d2_term_offense_code_1,
        trim(TSEV1)                                    as term_severity_1,
        trim(DISP1)                                    as disposition_1,
        trim(PRISTIM1)                                 as prison_time_1,
        trim(PRISCD1)                                  as prison_code_1,
        trim(PROBMON1)                                 as probation_months_1,
        trim(PROBCD1)                                  as probation_code_1,
        trim(SUPVREL1)                                 as supervised_release_1,
        try_to_number(trim(FINEAMT1))                  as fine_amount_1,
        trim(TTITLE2)                                  as term_title_2,
        trim(TOFFLVL2)                                 as term_offense_level_2,
        trim(TOFFCD2)                                  as term_offense_code_2,
        trim(D2TOFFCD2)                                as d2_term_offense_code_2,
        trim(TSEV2)                                    as term_severity_2,
        trim(DISP2)                                    as disposition_2,
        trim(PRISTIM2)                                 as prison_time_2,
        trim(PRISCD2)                                  as prison_code_2,
        trim(PROBMON2)                                 as probation_months_2,
        trim(PROBCD2)                                  as probation_code_2,
        trim(SUPVREL2)                                 as supervised_release_2,
        try_to_number(trim(FINEAMT2))                  as fine_amount_2,
        trim(TTITLE3)                                  as term_title_3,
        trim(TOFFLVL3)                                 as term_offense_level_3,
        trim(TOFFCD3)                                  as term_offense_code_3,
        trim(D2TOFFCD3)                                as d2_term_offense_code_3,
        trim(TSEV3)                                    as term_severity_3,
        trim(DISP3)                                    as disposition_3,
        trim(PRISTIM3)                                 as prison_time_3,
        trim(PRISCD3)                                  as prison_code_3,
        trim(PROBMON3)                                 as probation_months_3,
        trim(PROBCD3)                                  as probation_code_3,
        trim(SUPVREL3)                                 as supervised_release_3,
        try_to_number(trim(FINEAMT3))                  as fine_amount_3,
        trim(TTITLE4)                                  as term_title_4,
        trim(TOFFLVL4)                                 as term_offense_level_4,
        trim(TOFFCD4)                                  as term_offense_code_4,
        trim(D2TOFFCD4)                                as d2_term_offense_code_4,
        trim(TSEV4)                                    as term_severity_4,
        trim(DISP4)                                    as disposition_4,
        trim(PRISTIM4)                                 as prison_time_4,
        trim(PRISCD4)                                  as prison_code_4,
        trim(PROBMON4)                                 as probation_months_4,
        trim(PROBCD4)                                  as probation_code_4,
        trim(SUPVREL4)                                 as supervised_release_4,
        try_to_number(trim(FINEAMT4))                  as fine_amount_4,
        trim(TTITLE5)                                  as term_title_5,
        trim(TOFFLVL5)                                 as term_offense_level_5,
        trim(TOFFCD5)                                  as term_offense_code_5,
        trim(D2TOFFCD5)                                as d2_term_offense_code_5,
        trim(TSEV5)                                    as term_severity_5,
        trim(DISP5)                                    as disposition_5,
        trim(PRISTIM5)                                 as prison_time_5,
        trim(PRISCD5)                                  as prison_code_5,
        trim(PROBMON5)                                 as probation_months_5,
        trim(PROBCD5)                                  as probation_code_5,
        trim(SUPVREL5)                                 as supervised_release_5,
        try_to_number(trim(FINEAMT5))                  as fine_amount_5,

        -- sentence totals
        try_to_number(trim(PRISTOT))                   as prison_total,
        try_to_number(trim(PROBTOT))                   as probation_total,
        try_to_number(trim(FINETOT))                   as fine_total,

        -- count columns
        trim(CTFILTRN)                                 as ct_fil_trn,
        trim(CTFIL)                                    as ct_fil,
        trim(CTFILWOR)                                 as ct_fil_wor,
        trim(CTFILR)                                   as ct_fil_r,
        trim(CTTRTRN)                                  as ct_tr_trn,
        trim(CTTR)                                     as ct_tr,
        trim(CTTRWOR)                                  as ct_tr_wor,
        trim(CTTRR)                                    as ct_tr_r,
        trim(CTPN)                                     as ct_pn,
        trim(CTPNWOF)                                  as ct_pn_wof,

        -- file provenance
        trim(SOURCE)                                   as source_code,
        trim(VER)                                      as file_version,
        try_to_date(trim(LOADDATE))                    as load_date,

        -- metadata
        _ingested_at,
        _source_run_id

    from keyed

)

select * from renamed
