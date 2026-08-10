{{ config(materialized='table', schema='JUSTICE') }}

-- Built 2026-08-09 (73-source backlog, wave 2c). FHFA Suspended Counterparty Program: individuals/companies banned from doing business with Fannie Mae, Freddie Mac and the FHLBanks. SUSPENSION_END_DATE is 'Indefinite' on most rows (nulls after date-cast; raw kept).
-- Grain: one row = one suspension order line. Reads the pre-existing staging model.

select * from {{ ref('stg_fed_fhfa_suspended_counterparty_program__suspended_counterparty') }}
