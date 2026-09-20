{{ config(materialized='table', schema='PROCUREMENT') }}

-- GRAIN: one row per exclusion record (sam_number — unique in the source file).
-- Answers: Who has been debarred/suspended from federal contracting, and for how long?
-- Source: SAM.gov Exclusions, re-pulled in full 2026-08-11 — 168,328 rows (live-reverified 2026-09-20)
-- (old capped table held ~9K). NOTE the grain change from the capped era: the
-- full file carries multiple exclusion records per entity, so UEI is NOT unique
-- here and the mart no longer dedupes on it. TERMINATION_DATE is the literal
-- text 'Indefinite' on ~95% of rows — those parse to NULL dates and count as
-- currently excluded.
-- Key joins: entity_name/cage -> USAspending contracts; npi -> health providers
--
-- KEY RE-PROOF (2026-09-20 -- this is the exact "proven once, not re-proven"
-- failure mode f41ebff9 closed in staging: 289 views deduped on a key proven
-- unique ONCE, then silently stopped identifying a row after a reload while
-- `unique` stayed green forever, because the test only checked the ALREADY-
-- DEDUPED output. This model's own header above used to make the SAME one-time
-- claim -- "verified unique across all 167,928 landing rows" -- as a fact fixed
-- in time, never re-checked. key_proof below re-runs
-- scripts/generate_staging_models.py's key_is_unique_within_each_load() math
-- live, every build instead: COUNT(*) vs COUNT(DISTINCT HASH(sam_number)),
-- grouped by _SOURCE_RUN_ID when that column is a genuine load id (>= 100
-- rows/run average -- some CMS tables stamp a per-ROW uuid there instead, which
-- would make ANY key "prove" unique; MIN_ROWS_PER_LOAD=100 mirrors the
-- generator exactly). The staging ref this model reads from is a pure
-- trim/nullif passthrough (no filter, no dedup), so this checks the LANDING
-- table directly -- same row set, and the only place _SOURCE_RUN_ID survives
-- (the staging passthrough drops it).
-- Live-verified 2026-09-20: 168,328 rows, 168,328 distinct SAM_NUMBER, 1 load to
-- date, zero collision -- proven, so the QUALIFY below partitions by sam_number
-- alone. If a future reload ever breaks that, would_collapse > 0 and the SAME
-- QUALIFY automatically falls back to a whole-row partition (every data column,
-- so only exact copies collapse) -- schema.yml's `unique` test should be
-- dropped the day this ever shows would_collapse > 0.

with base as (
    select * from {{ ref('stg_fed_sam_exclusions__records') }}
),

key_load_shape as (

    select count(*) as total_rows, count(distinct _SOURCE_RUN_ID) as n_runs
    from {{ source('ripple_raw', 'FED_SAM_EXCLUSIONS_FULL_R2') }}

),

key_proof as (

    select coalesce(sum(n - d), 0) as would_collapse
    from (
        select
            case when ls.n_runs > 0 and ls.total_rows / ls.n_runs >= 100
                 then s._SOURCE_RUN_ID else '__ALL__' end    as _load_id,
            count(*)                                          as n,
            count(distinct hash(s.SAM_NUMBER))                as d
        from {{ source('ripple_raw', 'FED_SAM_EXCLUSIONS_FULL_R2') }} s
        cross join key_load_shape ls
        group by 1
    )

),

renamed as (

select
    sam_number,
    uei,
    cage                                           as cage_code,
    npi,
    entity_name,
    first_name,
    last_name,
    classification,
    exclusion_type,
    exclusion_program,
    excluding_agency,
    try_to_date(activation_date, 'YYYY-MM-DD')     as activation_date,
    termination_date                               as termination_date_raw,
    try_to_date(termination_date, 'YYYY-MM-DD')    as termination_date,
    record_status,
    city,
    state,
    zip,
    country,
    coalesce(
        termination_date is null
        or upper(termination_date) = 'INDEFINITE'
        or try_to_date(termination_date, 'YYYY-MM-DD') > current_date(),
        true)                                      as is_currently_excluded,
    (entity_name is not null and last_name is null) as is_entity_not_individual,
    _loaded_at
from base

)

select
    r.sam_number, r.uei, r.cage_code, r.npi, r.entity_name, r.first_name, r.last_name,
    r.classification, r.exclusion_type, r.exclusion_program, r.excluding_agency,
    r.activation_date, r.termination_date_raw, r.termination_date, r.record_status,
    r.city, r.state, r.zip, r.country, r.is_currently_excluded, r.is_entity_not_individual,
    r._loaded_at
from renamed r
cross join key_proof kp
-- partition: sam_number is unconditional; every other column only engages (goes
-- non-null) when kp.would_collapse != 0, i.e. the key is NOT proven -- at that
-- point this IS a whole-row partition, same shape as
-- generate_staging_models.py's fallback.
qualify row_number() over (
    partition by
        r.sam_number,
        case when kp.would_collapse != 0 then r.uei else null end,
        case when kp.would_collapse != 0 then r.cage_code else null end,
        case when kp.would_collapse != 0 then r.npi else null end,
        case when kp.would_collapse != 0 then r.entity_name else null end,
        case when kp.would_collapse != 0 then r.first_name else null end,
        case when kp.would_collapse != 0 then r.last_name else null end,
        case when kp.would_collapse != 0 then r.classification else null end,
        case when kp.would_collapse != 0 then r.exclusion_type else null end,
        case when kp.would_collapse != 0 then r.exclusion_program else null end,
        case when kp.would_collapse != 0 then r.excluding_agency else null end,
        case when kp.would_collapse != 0 then r.activation_date else null end,
        case when kp.would_collapse != 0 then r.termination_date_raw else null end,
        case when kp.would_collapse != 0 then r.record_status else null end,
        case when kp.would_collapse != 0 then r.city else null end,
        case when kp.would_collapse != 0 then r.state else null end,
        case when kp.would_collapse != 0 then r.zip else null end,
        case when kp.would_collapse != 0 then r.country else null end
    order by r._loaded_at desc,
             -- tie-breakers 2026-09-18: the row's own values, so the same row wins every run
             r.uei nulls last, r.cage_code nulls last, r.npi nulls last, r.entity_name nulls last,
             r.first_name nulls last, r.last_name nulls last, r.classification nulls last,
             r.exclusion_type nulls last, r.exclusion_program nulls last, r.excluding_agency nulls last,
             r.activation_date nulls last, r.termination_date_raw nulls last, r.record_status nulls last,
             r.city nulls last, r.state nulls last, r.zip nulls last, r.country nulls last
) = 1
