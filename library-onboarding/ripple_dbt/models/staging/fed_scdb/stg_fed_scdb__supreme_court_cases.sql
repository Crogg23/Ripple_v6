{{ config(materialized='view') }}

with

source as (

    select * from {{ source('ripple_raw', 'FED_SCDB') }}

),

renamed as (

    select

        -- identifiers
        CASEID                                              as case_id,
        DOCKETID                                            as docket_id,
        CASEISSUESID                                        as case_issues_id,
        VOTEID                                              as vote_id,

        -- dates
        -- NOT A BUG (epoch-1970 investigation, 2026-08-18): already uses an
        -- explicit 'MM/DD/YYYY' format, so it never hit the bare-try_to_date
        -- epoch trap. Its 2,245-of-83,644 (2.7%) 1970 rows (confirmed live)
        -- spread across many distinct 1970 days -- real Supreme Court 1970-term
        -- decisions, not sentinel garbage. Left as-is.
        try_to_date(DATEDECISION, 'MM/DD/YYYY')             as date_decision,
        try_to_date(DATEARGUMENT, 'MM/DD/YYYY')             as date_argument,
        try_to_date(DATEREARG,    'MM/DD/YYYY')             as date_reargument,

        -- term / court composition
        {{ stg_int('TERM') }}                                 as term,
        {{ stg_int('NATURALCOURT') }}                         as natural_court,
        CHIEF                                               as chief_justice,
        DOCKET                                              as docket,

        -- case identity
        CASENAME                                            as case_name,
        USCITE                                              as us_citation,
        SCTCITE                                             as sct_citation,
        LEDCITE                                             as led_citation,
        LEXISCITE                                           as lexis_citation,

        -- parties
        {{ stg_int('PETITIONER') }}                           as petitioner_code,
        {{ stg_int('PETITIONERSTATE') }}                      as petitioner_state_code,
        {{ stg_int('RESPONDENT') }}                           as respondent_code,
        {{ stg_int('RESPONDENTSTATE') }}                      as respondent_state_code,

        -- jurisdiction & origin
        {{ stg_int('JURISDICTION') }}                         as jurisdiction_code,
        {{ stg_int('ADMINACTION') }}                          as admin_action_code,
        {{ stg_int('ADMINACTIONSTATE') }}                     as admin_action_state_code,
        {{ stg_int('THREEJUDGEFDC') }}                        as three_judge_fdc,
        {{ stg_int('CASEORIGIN') }}                           as case_origin_code,
        {{ stg_int('CASEORIGINSTATE') }}                      as case_origin_state_code,
        {{ stg_int('CASESOURCE') }}                           as case_source_code,
        {{ stg_int('CASESOURCESTATE') }}                      as case_source_state_code,

        -- cert & lower court disposition
        {{ stg_int('LCDISAGREEMENT') }}                       as lc_disagreement,
        {{ stg_int('CERTREASON') }}                           as cert_reason_code,
        {{ stg_int('LCDISPOSITION') }}                        as lc_disposition_code,
        {{ stg_int('LCDISPOSITIONDIRECTION') }}               as lc_disposition_direction_code,

        -- case disposition
        {{ stg_int('DECLARATIONUNCON') }}                     as declaration_unconstitutional,
        {{ stg_int('CASEDISPOSITION') }}                      as case_disposition_code,
        {{ stg_int('CASEDISPOSITIONUNUSUAL') }}               as case_disposition_unusual,
        {{ stg_int('PARTYWINNING') }}                         as party_winning,
        {{ stg_int('PRECEDENTALTERATION') }}                  as precedent_alteration,
        {{ stg_int('VOTEUNCLEAR') }}                          as vote_unclear,

        -- issue
        {{ stg_int('ISSUE') }}                                as issue_code,
        {{ stg_int('ISSUEAREA') }}                            as issue_area_code,

        -- decision direction
        {{ stg_int('DECISIONTYPE') }}                         as decision_type_code,
        {{ stg_int('DECISIONDIRECTION') }}                    as decision_direction_code,
        {{ stg_int('DECISIONDIRECTIONDISSENT') }}             as decision_direction_dissent,

        -- authority
        {{ stg_int('AUTHORITYDECISION1') }}                   as authority_decision_1,
        {{ stg_int('AUTHORITYDECISION2') }}                   as authority_decision_2,
        {{ stg_int('LAWTYPE') }}                              as law_type_code,
        {{ stg_int('LAWSUPP') }}                              as law_supp_code,
        LAWMINOR                                            as law_minor,

        -- opinion authorship
        {{ stg_int('MAJOPINWRITER') }}                        as maj_opin_writer_code,
        {{ stg_int('MAJOPINASSIGNER') }}                      as maj_opin_assigner_code,

        -- vote counts
        {{ stg_int('SPLITVOTE') }}                            as split_vote,
        {{ stg_int('MAJVOTES') }}                             as maj_votes,
        {{ stg_int('MINVOTES') }}                             as min_votes,

        -- justice-level vote record
        {{ stg_int('JUSTICE') }}                              as justice_code,
        JUSTICENAME                                         as justice_name,
        {{ stg_int('VOTE') }}                                 as vote_code,
        {{ stg_int('OPINION') }}                              as opinion_code,
        {{ stg_int('DIRECTION') }}                            as direction_code,
        {{ stg_int('MAJORITY') }}                             as majority_code,
        {{ stg_int('FIRSTAGREEMENT') }}                       as first_agreement_code,
        {{ stg_int('SECONDAGREEMENT') }}                      as second_agreement_code,

        -- metadata
        _ingested_at,
        _source_run_id

    from source

),

deduped as (

    select *
    from renamed
    qualify row_number() over (
        partition by vote_id
        order by _ingested_at desc
    ) = 1

)

select * from deduped
