{{ config(materialized='table', schema='HEALTH') }}

-- Built 2026-08-10 (backlog wave 4). FDA Purple Book biologics licenses
-- (monthly changes report, June 2026): BLA products with applicant,
-- names, licensure, approval and exclusivity dates. Loader-embedded
-- title/preamble/section/header rows filtered out in staging (numeric
-- BLA-number filter); columns renamed positionally onto the real header.
-- Grain: purple_book_record_id — surrogate over (bla_number, product_number,
-- supplement_number) with row_number tiebreaker; natural grain not
-- pre-verified post-filter. 2-digit source years make pre-1970 dates
-- century-ambiguous.

select * from {{ ref('stg_fed_fda_purple_book__licenses') }}
