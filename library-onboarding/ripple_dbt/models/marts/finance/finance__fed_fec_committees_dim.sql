{{ config(materialized='view', schema='FINANCE') }}

-- Labeling dimension: exactly ONE row per committee id, for joining names
-- onto money tables without fan-out. Built 2026-09-01 after the readiness
-- skeptic proved a raw join inflates the itoth money layer 2.14x
-- (1,920,089 rows -> 4,116,351): the FED_FEC_COMMITTEES landing file is
-- multi-cycle with no cycle column, so repeated CMTE_IDs multiply dollars.
--
-- UNION build (Chris greenlit 2026-09-01, "both"): two sources, best wins.
--   1. stg_fed_fec_bulk_committees -- cm26 bulk, one row per id, real CYCLE
--      column, current and authoritative. Wins wherever present.
--   2. FED_FEC_COMMITTEES (cm multi-cycle) -- fills ids the 2026 file no
--      longer lists. No cycle column, single _INGESTED_AT, so the pick
--      across its duplicate rows is forced-arbitrary: name desc.
-- SRC says which source labeled the row. CYCLE is null on cm rows.
-- IS_AMBIGUOUS (cm rows only) marks ids whose duplicate rows disagree on
-- name/type/party/designation/state/cand_id -- skeptic sized 210,872 real
-- itoth money rows (11.0%) landing on such ids. Bulk rows are single-source
-- current-cycle truth: is_ambiguous = false by construction.

with bulk as (
    select
        fec_cmte_id              as cmte_id,
        cmte_nm,
        tres_nm,
        cmte_city,
        cmte_st,
        cmte_dsgn,
        cmte_tp,
        cmte_pty_affiliation,
        org_tp,
        connected_org_nm,
        fec_cand_id              as cand_id,
        cycle,
        false                    as is_ambiguous,
        'bulk_cm26'              as src
    from {{ ref('stg_fed_fec_bulk_committees__records') }}
),

cm_source as (
    select * from {{ source('ripple_raw', 'FED_FEC_COMMITTEES') }}
),

cm_flagged as (
    select
        *,
        count(distinct C2)  over (partition by C1) > 1
        or count(distinct C10) over (partition by C1) > 1
        or count(distinct C11) over (partition by C1) > 1
        or count(distinct C9)  over (partition by C1) > 1
        or count(distinct C7)  over (partition by C1) > 1
        or count(distinct C15) over (partition by C1) > 1 as is_ambiguous
    from cm_source
),

cm as (
    select
        C1  as cmte_id,
        C2  as cmte_nm,
        C3  as tres_nm,
        C6  as cmte_city,
        C7  as cmte_st,
        C9  as cmte_dsgn,
        C10 as cmte_tp,
        C11 as cmte_pty_affiliation,
        C13 as org_tp,
        C14 as connected_org_nm,
        C15 as cand_id,
        null::number as cycle,
        is_ambiguous,
        'cm_multicycle' as src
    from cm_flagged
    qualify row_number() over (
        partition by C1
        order by C2 desc nulls last, C3 desc nulls last, C15 desc nulls last
    ) = 1
)

select * from bulk
union all
select * from cm
where cmte_id not in (select cmte_id from bulk)
