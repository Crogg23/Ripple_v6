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
-- SRC says which source labeled the row. CYCLE is null on cm rows (55%).
-- IS_AMBIGUOUS marks ids whose cm duplicate rows disagree on
-- name/type/party/designation/state/cand_id -- applied to BOTH sources
-- (wrap skeptic 2026-09-01: the first version hardcoded false on bulk rows,
-- which flagged only 0.07% of money rows while 14.1% sit on conflicted ids;
-- a bulk row is an unambiguous PICK, but the id's history still conflicts,
-- and spend-by-attribute charts must know that).

with bulk_raw as (
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
        'bulk_cm26'              as src
    from {{ ref('stg_fed_fec_bulk_committees__records') }}
),

cm_source as (
    select * from {{ source('ripple_raw', 'FED_FEC_COMMITTEES') }}
),

conflict_ids as (
    select C1 as cmte_id
    from cm_source
    group by C1
    having count(distinct C2) > 1 or count(distinct C10) > 1
        or count(distinct C11) > 1 or count(distinct C9) > 1
        or count(distinct C7) > 1 or count(distinct C15) > 1
),

bulk as (
    select
        b.* exclude src,
        b.cmte_id in (select cmte_id from conflict_ids) as is_ambiguous,
        b.src
    from bulk_raw b
),

cm_flagged as (
    select
        s.*,
        s.C1 in (select cmte_id from conflict_ids) as is_ambiguous
    from cm_source s
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
