{{ config(materialized='table', schema='POLITICS') }}

-- GRAIN: one row per (committee, election-cycle coverage period). Fixed 2026-07-31 --
-- was silently keeping only the LATEST cycle per committee (see staging model header
-- for the root cause and the 25,496 rows of multi-cycle history that recovered).
-- COUNT(*) is committee-cycles, not committees -- filter/group by coverage_end_date
-- for a single-cycle view, or by cmte_id for a committee's full history.
-- Answers: How much money does each PAC/party committee raise, spend, and give away,
-- IN EACH ELECTION CYCLE?
-- Source: FEC PAC and Party Summary (48,395 committee-cycle records)
-- Key joins: cmte_id â†’ fec_cand_cmte_linkage â†’ candidates; cmte_id â†’ individual contributions

select
    cmte_id,
    cmte_nm                                as committee_name,
    cmte_tp                                as committee_type,
    cmte_dsgn                              as committee_designation,
    cmte_filing_freq                       as filing_frequency,
    ttl_receipts                           as total_receipts,
    ttl_disb                               as total_disbursements,
    indv_contrib                           as individual_contributions,
    other_pol_cmte_contrib                 as pac_contributions,
    trans_from_aff                         as transfers_from_affiliates,
    tranf_to_aff                           as transfers_to_affiliates,
    contrib_to_other_cmte                  as contributions_to_other_committees,
    ind_exp                                as independent_expenditures,
    coh_bop                                as cash_beginning_of_period,
    coh_cop                                as cash_close_of_period,
    debts_owed_by,
    nonfed_trans_received                   as nonfederal_transfers_received,
    cvg_end_dt                             as coverage_end_date,
    round(indv_contrib / nullif(ttl_receipts, 0), 4) as pct_from_individuals,
    round(contrib_to_other_cmte / nullif(ttl_disb, 0), 4) as pct_disbursed_to_others,
    _loaded_at,
    _source_run_id
from {{ ref('stg_fed_fec_pac_summary__records') }}
