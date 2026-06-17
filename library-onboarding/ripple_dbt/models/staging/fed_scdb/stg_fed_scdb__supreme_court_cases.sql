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
        try_to_date(DATEDECISION, 'MM/DD/YYYY')             as date_decision,
        try_to_date(DATEARGUMENT, 'MM/DD/YYYY')             as date_argument,
        try_to_date(DATEREARG,    'MM/DD/YYYY')             as date_reargument,

        -- term / court composition
        try_to_number(TERM)                                 as term,
        try_to_number(NATURALCOURT)                         as natural_court,
        CHIEF                                               as chief_justice,
        DOCKET                                              as docket,

        -- case identity
        CASENAME                                            as case_name,
        USCITE                                              as us_citation,
        SCTCITE                                             as sct_citation,
        LEDCITE                                             as led_citation,
        LEXISCITE                                           as lexis_citation,

        -- parties
        try_to_number(PETITIONER)                           as petitioner_code,
        try_to_number(PETITIONERSTATE)                      as petitioner_state_code,
        try_to_number(RESPONDENT)                           as respondent_code,
        try_to_number(RESPONDENTSTATE)                      as respondent_state_code,

        -- jurisdiction & origin
        try_to_number(JURISDICTION)                         as jurisdiction_code,
        try_to_number(ADMINACTION)                          as admin_action_code,
        try_to_number(ADMINACTIONSTATE)                     as admin_action_state_code,
        try_to_number(THREEJUDGEFDC)                        as three_judge_fdc,
        try_to_number(CASEORIGIN)                           as case_origin_code,
        try_to_number(CASEORIGINSTATE)                      as case_origin_state_code,
        try_to_number(CASESOURCE)                           as case_source_code,
        try_to_number(CASESOURCESTATE)                      as case_source_state_code,

        -- cert & lower court disposition
        try_to_number(LCDISAGREEMENT)                       as lc_disagreement,
        try_to_number(CERTREASON)                           as cert_reason_code,
        try_to_number(LCDISPOSITION)                        as lc_disposition_code,
        try_to_number(LCDISPOSITIONDIRECTION)               as lc_disposition_direction_code,

        -- case disposition
        try_to_number(DECLARATIONUNCON)                     as declaration_unconstitutional,
        try_to_number(CASEDISPOSITION)                      as case_disposition_code,
        try_to_number(CASEDISPOSITIONUNUSUAL)               as case_disposition_unusual,
        try_to_number(PARTYWINNING)                         as party_winning,
        try_to_number(PRECEDENTALTERATION)                  as precedent_alteration,
        try_to_number(VOTEUNCLEAR)                          as vote_unclear,

        -- issue
        try_to_number(ISSUE)                                as issue_code,
        try_to_number(ISSUEAREA)                            as issue_area_code,

        -- decision direction
        try_to_number(DECISIONTYPE)                         as decision_type_code,
        try_to_number(DECISIONDIRECTION)                    as decision_direction_code,
        try_to_number(DECISIONDIRECTIONDISSENT)             as decision_direction_dissent,

        -- authority
        try_to_number(AUTHORITYDECISION1)                   as authority_decision_1,
        try_to_number(AUTHORITYDECISION2)                   as authority_decision_2,
        try_to_number(LAWTYPE)                              as law_type_code,
        try_to_number(LAWSUPP)                              as law_supp_code,
        LAWMINOR                                            as law_minor,

        -- opinion authorship
        try_to_number(MAJOPINWRITER)                        as maj_opin_writer_code,
        try_to_number(MAJOPINASSIGNER)                      as maj_opin_assigner_code,

        -- vote counts
        try_to_number(SPLITVOTE)                            as split_vote,
        try_to_number(MAJVOTES)                             as maj_votes,
        try_to_number(MINVOTES)                             as min_votes,

        -- justice-level vote record
        try_to_number(JUSTICE)                              as justice_code,
        JUSTICENAME                                         as justice_name,
        try_to_number(VOTE)                                 as vote_code,
        try_to_number(OPINION)                              as opinion_code,
        try_to_number(DIRECTION)                            as direction_code,
        try_to_number(MAJORITY)                             as majority_code,
        try_to_number(FIRSTAGREEMENT)                       as first_agreement_code,
        try_to_number(SECONDAGREEMENT)                      as second_agreement_code,

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
