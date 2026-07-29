{{ config(materialized='table', schema='POLITICS') }}

-- GRAIN: one row per committee (cmte_id is unique â€” latest filing period kept)
-- Answers: How much money does each PAC/party committee raise, spend, and give away?
-- Source: FEC PAC and Party Summary (~48K committees)
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
