{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_FJC_IDB_BANKRUPTCY') }}

),

renamed as (

    select

        -- identifiers
        {{ dbt_utils.generate_surrogate_key(['CASEKEY', 'SNAPSHOT']) }}         as case_snapshot_id,
        trim(CASEKEY)                                  as case_key,
        trim(SNAPSHOT)                                 as snapshot,
        trim(SNAPFILE)                                 as snapshot_filed_flag,
        trim(SNAPPEND)                                 as snapshot_pending_flag,
        trim(SNAPCLOS)                                 as snapshot_closed_flag,
        trim(CIRCUIT)                                  as circuit,
        trim(DISTRICT)                                 as district,
        trim(OFFICE)                                   as office,
        trim(DOCKET)                                   as docket,
        trim(GEN)                                      as docket_generation,
        trim(SEQ)                                      as docket_sequence,

        -- filing
        trim(ORIGIN)                                   as origin,
        try_to_date(trim(ORGFLDT))                     as original_filing_date,
        try_to_date(trim(FILEDATE))                    as file_date,
        trim(FILECY)                                   as filing_calendar_year,
        trim(FILEFY)                                   as filing_fiscal_year,
        trim(ORGFLCHP)                                 as original_filing_chapter,
        trim(ORGFLSUBCHP)                              as original_filing_subchapter,
        trim(CRNTCHP)                                  as current_chapter,
        trim(CRNTFLSUBCHP)                             as current_subchapter,
        trim(ORGNTRDBT)                                as original_nature_of_debt,
        trim(NTRDBT)                                   as nature_of_debt,
        trim(JOINT)                                    as joint_filing,

        -- debtors
        trim(D1ZIP)                                    as debtor1_zip,
        trim(D1CNTY)                                   as debtor1_county,
        trim(ORGD1FPRSE)                               as original_debtor1_filing_pro_se,
        trim(D1FPRSE)                                  as debtor1_filing_pro_se,
        try_to_date(trim(D1CHGDT))                     as debtor1_change_date,
        trim(D2ZIP)                                    as debtor2_zip,
        trim(D2CNTY)                                   as debtor2_county,
        trim(ORGD2FPRSE)                               as original_debtor2_filing_pro_se,
        trim(D2FPRSE)                                  as debtor2_filing_pro_se,
        try_to_date(trim(D2CHGDT))                     as debtor2_change_date,

        -- case attributes
        trim(ORGFEESTS)                                as original_fee_status,
        trim(FEESTS)                                   as fee_status,
        trim(CASETYP)                                  as case_type,
        trim(ORGDBTRTYP)                               as original_debtor_type,
        trim(DBTRTYP)                                  as debtor_type,
        trim(NOB)                                      as nature_of_business,
        trim(PRFILE)                                   as prior_filing,
        trim(ORGEASST)                                 as original_estimated_assets,
        trim(EASST)                                    as estimated_assets,
        trim(ORGELBLTS)                                as original_estimated_liabilities,
        trim(ELBLTS)                                   as estimated_liabilities,
        trim(ORGECRDTRS)                               as original_estimated_creditors,
        trim(ECRDTRS)                                  as estimated_creditors,
        trim(ORGASSTCASE)                              as original_asset_case,
        trim(ASSTCASE)                                 as asset_case,
        trim(SMLLBUS)                                  as small_business,
        trim(PREPACK)                                  as prepackaged,

        -- reported dollar figures
        try_to_number(trim(TOTASSTS))                  as total_assets,
        try_to_number(trim(REALPROP))                  as real_property,
        try_to_number(trim(PERSPROP))                  as personal_property,
        try_to_number(trim(TOTLBLTS))                  as total_liabilities,
        try_to_number(trim(SECURED))                   as secured_claims,
        try_to_number(trim(UNSECPR))                   as unsecured_priority_claims,
        try_to_number(trim(UNSECNPR))                  as unsecured_nonpriority_claims,
        try_to_number(trim(DSCHRGD))                   as debt_discharged,
        try_to_number(trim(NDSCHRGD))                  as debt_not_discharged,
        try_to_number(trim(TOTDBT))                    as total_debt,
        trim(CNTMNTHI)                                 as count_monthly_income,
        try_to_number(trim(AVGMNTHI))                  as avg_monthly_income,
        try_to_number(trim(AVGMNTHE))                  as avg_monthly_expenses,

        -- transfers / related cases
        trim(SRCCASE)                                  as source_case,
        trim(DSTNCASE)                                 as destination_case,
        trim(CNSLLEAD)                                 as consolidation_lead,
        trim(JNTLEAD)                                  as joint_administration_lead,
        trim(FLCMECFV)                                 as filing_cmecf_version,

        -- closing / disposition
        try_to_date(trim(CLOSEDT))                     as close_date,
        trim(CLOSECY)                                  as closing_calendar_year,
        trim(CLOSEFY)                                  as closing_fiscal_year,
        trim(CLCHPT)                                   as closing_chapter,
        trim(CLSUBCHPT)                                as closing_subchapter,
        trim(D1CPRSE)                                  as debtor1_closing_pro_se,
        trim(D1FDSP)                                   as debtor1_final_disposition,
        try_to_date(trim(D1FDSPDT))                    as debtor1_final_disposition_date,
        trim(D1FDSPCY)                                 as debtor1_final_disposition_calendar_year,
        trim(D1FDSPFY)                                 as debtor1_final_disposition_fiscal_year,
        trim(D2CPRSE)                                  as debtor2_closing_pro_se,
        trim(D2FDSP)                                   as debtor2_final_disposition,
        try_to_date(trim(D2FDSPDT))                    as debtor2_final_disposition_date,
        trim(D2FDSPCY)                                 as debtor2_final_disposition_calendar_year,
        trim(D2FDSPFY)                                 as debtor2_final_disposition_fiscal_year,
        trim(C11DVDND)                                 as chapter11_dividend,
        trim(C11FTRPAY)                                as chapter11_future_payments,
        trim(CLCMECFV)                                 as closing_cmecf_version,
        trim(TAXEXEMPT)                                as tax_exempt,

        -- metadata
        _ingested_at,
        _source_run_id

    from source

)

select * from renamed
