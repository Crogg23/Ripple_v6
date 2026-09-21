{{ config(materialized='table', schema='HEALTH') }}

-- Source: NPDB (National Practitioner Data Bank) Public Use Data File (1,911,185 rows)
-- Landed via a click-through Data Use Agreement POST to npdb.hrsa.gov (no login).
-- Grain: one row per disclosable report (adverse action or malpractice payment).
-- De-identified by design -- no practitioner name/NPI in the public file.
-- SEQNO verified unique across all 1,911,185 rows.

with source as (
    select * from {{ source('ripple_raw', 'FED_HRSA_NPDB') }}
)

select
    SEQNO as seqno,
    RECTYPE as rec_type,
    REPTYPE as report_type_code,
    {{ stg_int('ORIGYEAR') }} as orig_year,
    WORKSTAT as work_state,
    WORKCTRY as work_country,
    HOMESTAT as home_state,
    HOMECTRY as home_country,
    LICNSTAT as license_state,
    LICNFELD as license_field_code,
    {{ stg_int('PRACTAGE') }} as practitioner_age,
    {{ stg_int('GRAD') }} as grad_year,
    ALGNNATR as allegation_nature,
    ALEGATN1 as allegation_1,
    ALEGATN2 as allegation_2,
    OUTCOME as outcome_code,
    {{ stg_int('MALYEAR1') }} as malpractice_year_1,
    {{ stg_int('MALYEAR2') }} as malpractice_year_2,
    PAYMENT as payment_flag,
    {{ stg_float('TOTALPMT') }} as total_payment,
    PAYNUMBR as payment_number,
    {{ stg_int('NUMBPRSN') }} as num_persons,
    PAYTYPE as pay_type,
    PYRRLTNS as payer_relationship,
    {{ stg_int('PTAGE') }} as patient_age,
    PTSEX as patient_sex,
    PTTYPE as patient_type,
    {{ stg_int('AAYEAR') }} as adverse_action_year,
    AACLASS1 as aa_class_1,
    AACLASS2 as aa_class_2,
    AACLASS3 as aa_class_3,
    AACLASS4 as aa_class_4,
    AACLASS5 as aa_class_5,
    BASISCD1 as basis_code_1,
    BASISCD2 as basis_code_2,
    BASISCD3 as basis_code_3,
    BASISCD4 as basis_code_4,
    BASISCD5 as basis_code_5,
    AALENTYP as aa_length_type,
    {{ stg_float('AALENGTH') }} as aa_length,
    {{ stg_int('AAEFYEAR') }} as aa_effective_year,
    {{ stg_int('AASIGYR') }} as aa_signed_year,
    TYPE as practitioner_type_code,
    PRACTNUM as practitioner_report_seq,
    {{ stg_int('ACCRRPTS') }} as accrued_report_count,
    {{ stg_int('NPMALRPT') }} as prior_malpractice_reports,
    {{ stg_int('NPLICRPT') }} as prior_license_reports,
    {{ stg_int('NPCLPRPT') }} as prior_clinical_privilege_reports,
    {{ stg_int('NPPSMRPT') }} as prior_society_membership_reports,
    {{ stg_int('NPDEARPT') }} as prior_dea_reports,
    {{ stg_int('NPEXCRPT') }} as prior_exclusion_reports,
    {{ stg_int('NPGARPT') }} as prior_ga_reports,
    {{ stg_int('NPCTMRPT') }} as prior_ctm_reports,
    FUNDPYMT as fund_payment_flag
from source
