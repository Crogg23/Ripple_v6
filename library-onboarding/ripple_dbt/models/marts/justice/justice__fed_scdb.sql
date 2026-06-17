{{ config(materialized='table') }}

with

base as (

    select * from {{ ref('stg_fed_scdb__supreme_court_cases') }}

),

final as (

    select

        -- -------------------------------------------------------
        -- Key identifiers exposed for cross-source joins
        -- -------------------------------------------------------
        vote_id                             as vote_id,          -- primary key (one row = one justice vote)
        case_id                             as case_id,
        docket_id                           as docket_id,
        case_issues_id                      as case_issues_id,
        docket                              as docket,
        us_citation                         as us_citation,      -- citation
        sct_citation                        as sct_citation,
        led_citation                        as led_citation,
        lexis_citation                      as lexis_citation,
        natural_court                       as court,            -- court composition id
        justice_code                        as justice_code,     -- person identifier (numeric)
        justice_name                        as justice_name,     -- person identifier (string)

        -- -------------------------------------------------------
        -- Temporal
        -- -------------------------------------------------------
        date_decision,
        date_argument,
        date_reargument,
        term,

        -- -------------------------------------------------------
        -- Case metadata
        -- -------------------------------------------------------
        case_name,
        chief_justice,
        petitioner_code,
        petitioner_state_code,
        respondent_code,
        respondent_state_code,
        jurisdiction_code,
        admin_action_code,
        admin_action_state_code,
        three_judge_fdc,
        case_origin_code,
        case_origin_state_code,
        case_source_code,
        case_source_state_code,

        -- -------------------------------------------------------
        -- Cert / lower-court
        -- -------------------------------------------------------
        lc_disagreement,
        cert_reason_code,
        lc_disposition_code,
        lc_disposition_direction_code,

        -- -------------------------------------------------------
        -- Decision outcome
        -- -------------------------------------------------------
        decision_type_code,
        declaration_unconstitutional,
        case_disposition_code,
        case_disposition_unusual,
        party_winning,
        precedent_alteration,
        vote_unclear,
        decision_direction_code,
        decision_direction_dissent,

        -- -------------------------------------------------------
        -- Issue classification
        -- -------------------------------------------------------
        issue_code,
        issue_area_code,

        -- -------------------------------------------------------
        -- Legal authority
        -- -------------------------------------------------------
        authority_decision_1,
        authority_decision_2,
        law_type_code,
        law_supp_code,
        law_minor,

        -- -------------------------------------------------------
        -- Opinion authorship
        -- -------------------------------------------------------
        maj_opin_writer_code,
        maj_opin_assigner_code,

        -- -------------------------------------------------------
        -- Vote aggregates
        -- -------------------------------------------------------
        split_vote,
        maj_votes,
        min_votes,

        -- -------------------------------------------------------
        -- Justice-level vote details
        -- -------------------------------------------------------
        vote_code,
        opinion_code,
        direction_code,
        majority_code,
        first_agreement_code,
        second_agreement_code,

        -- -------------------------------------------------------
        -- Derived / convenience flags
        -- -------------------------------------------------------
        case when party_winning = 1 then true
             when party_winning = 0 then false
             else null
        end                                 as is_petitioner_winning,

        case when precedent_alteration = 1 then true
             else false
        end                                 as is_precedent_altered,

        case when declaration_unconstitutional > 0 then true
             else false
        end                                 as is_unconstitutional_declaration,

        maj_votes + coalesce(min_votes, 0)  as total_votes,

        -- -------------------------------------------------------
        -- Metadata
        -- -------------------------------------------------------
        _ingested_at,
        _source_run_id

    from base

)

select * from final
