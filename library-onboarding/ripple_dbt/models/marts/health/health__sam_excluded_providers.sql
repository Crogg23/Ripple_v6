{{ config(materialized='table', schema='HEALTH') }}

-- GRAIN: one row per SAM exclusion row (sam_number) whose excluding agency is
-- not HHS, OFAC or OPM. The match never adds or drops a row.
-- Docket line E73. Built 2026-09-07 from reports/dead_ends_scope_A_bridges_2026-09-07.md.
--
-- The docket had this line as "dead end, basically no overlap." That measured
-- NPI = NPI on a column SAM fills on 3% of rows (88.6% blank, 7.1% the
-- '0000000000' sentinel). Where SAM does hold a real NPI it is right: 4,854
-- of 4,866 hit NPPES. The rest need a name.
--
-- WHY THREE AGENCIES ARE OUT: HHS rows are the OIG LEIE mirrored into SAM, so
-- a doctor there is a doctor banned for being a doctor, which is the LEIE
-- line, not a crossover. OFAC is the sanctions list, OPM is federal-employee
-- debarments; neither is a contractor ban. The crossover the docket wants, a
-- construction or defense debarment that turns out to be a doctor, lives in
-- the other 16,144 rows, and only 10 of those carry a real NPI.
--
-- THE MATCH, two steps, walked once per row:
--   1. SAM npi is real (not blank, not '0000000000') -> NPPES on NPI.
--   2. else an individual with first, last and state -> NPPES persons on
--      upper(first) + upper(last) + practice state. Exactly one hit lands;
--      more than one lands NULL with match_note 'ambiguous: N people share
--      it', the same shape finance__senate_trades uses. Zero hits lands NULL
--      with the reason.
-- Entities never get a name match; the entity name is not a person.
--
-- STILL TRUE: a one-hit name match is a lead, not a proof. The SAM address
-- is the only tiebreaker and it is not used here. Single-word matching was
-- measured at 74% "hit" with a median 20 people per name and is not offered.
-- The mart is Active-only upstream, so purged past bans are invisible.

with sam as (

    select
        sam_number,
        uei,
        excluding_agency,
        exclusion_type,
        exclusion_program,
        classification,
        entity_name,
        first_name,
        last_name,
        city,
        state,
        activation_date,
        termination_date_raw,
        is_currently_excluded,
        is_entity_not_individual,
        iff(nullif(trim(npi), '') is not null and trim(npi) <> '0000000000', trim(npi), null)
                                                               as sam_npi,
        upper(trim(first_name))                                as first_key,
        upper(trim(last_name))                                 as last_key,
        upper(trim(state))                                     as state_key
    from {{ ref('procurement__fed_sam_exclusions') }}
    where coalesce(upper(trim(excluding_agency)), '') not in ('HHS', 'OFAC', 'OPM')

),

nppes_people as (

    select
        npi,
        upper(trim(provider_first_name))                       as first_key,
        upper(trim(provider_last_name_legal_name))             as last_key,
        upper(trim(provider_business_practice_location_address_state_name))
                                                               as state_key,
        provider_last_name_legal_name || ', ' || provider_first_name
                                                               as nppes_name,
        healthcare_provider_taxonomy_code_1                    as taxonomy_code_1,
        provider_credential_text                               as credential
    from {{ ref('health__fed_cms_nppes') }}
    where entity_type_code = '1'

),

nppes_any as (

    select
        npi,
        entity_type_code,
        coalesce(nullif(provider_organization_name_legal_business_name, ''),
                 provider_last_name_legal_name || ', ' || provider_first_name)
                                                               as nppes_name,
        healthcare_provider_taxonomy_code_1                    as taxonomy_code_1,
        provider_credential_text                               as credential
    from {{ ref('health__fed_cms_nppes') }}

),

-- step 1: the id
by_npi as (

    select
        s.sam_number,
        n.npi,
        n.nppes_name,
        n.taxonomy_code_1,
        n.credential
    from sam s
    join nppes_any n
        on n.npi = s.sam_npi

),

-- step 2: the name, one candidate set per distinct (first, last, state)
name_keys as (

    select distinct first_key, last_key, state_key
    from sam
    where sam_npi is null
      and not is_entity_not_individual
      and first_key is not null and first_key <> ''
      and last_key  is not null and last_key  <> ''
      and state_key is not null and state_key <> ''

),

name_hits as (

    select
        k.first_key,
        k.last_key,
        k.state_key,
        count(n.npi)                                           as n_hits,
        max(n.npi)                                             as npi,
        max(n.nppes_name)                                      as nppes_name,
        max(n.taxonomy_code_1)                                 as taxonomy_code_1,
        max(n.credential)                                      as credential
    from name_keys k
    left join nppes_people n
        on n.first_key = k.first_key
       and n.last_key  = k.last_key
       and n.state_key = k.state_key
    group by 1, 2, 3

)

select
    s.sam_number,
    s.uei,
    s.excluding_agency,
    s.exclusion_type,
    s.exclusion_program,
    s.classification,
    s.is_entity_not_individual,
    s.entity_name,
    s.first_name,
    s.last_name,
    s.city,
    s.state,
    s.activation_date,
    s.termination_date_raw,
    s.is_currently_excluded,
    s.sam_npi,
    case
        when b.npi is not null                                 then b.npi
        when s.sam_npi is null and h.n_hits = 1                then h.npi
    end                                                        as npi,
    case
        when b.npi is not null                                 then b.nppes_name
        when s.sam_npi is null and h.n_hits = 1                then h.nppes_name
    end                                                        as nppes_name,
    case
        when b.npi is not null                                 then b.taxonomy_code_1
        when s.sam_npi is null and h.n_hits = 1                then h.taxonomy_code_1
    end                                                        as taxonomy_code_1,
    case
        when b.npi is not null                                 then b.credential
        when s.sam_npi is null and h.n_hits = 1                then h.credential
    end                                                        as credential,
    case
        when b.npi is not null                                 then 'npi'
        when s.sam_npi is null and h.n_hits = 1                then 'first+last+state'
    end                                                        as match_method,
    case
        when b.npi is not null
            then 'SAM npi found in NPPES'
        when s.sam_npi is not null
            then 'SAM npi not in NPPES'
        when s.is_entity_not_individual
            then 'entity, no person match attempted'
        when h.first_key is null
            then 'no first name, last name or state to match on'
        when h.n_hits = 1
            then 'one NPPES person with that first, last and practice state'
        when h.n_hits = 0
            then 'no NPPES person with that first, last and practice state'
        else 'ambiguous: ' || h.n_hits || ' people share it'
    end                                                        as match_note
from sam s
left join by_npi b
    on b.sam_number = s.sam_number
left join name_hits h
    on  s.sam_npi is null
    and not s.is_entity_not_individual
    and h.first_key = s.first_key
    and h.last_key  = s.last_key
    and h.state_key = s.state_key
