{{ config(materialized='table', schema='HEALTH') }}

-- GRAIN: one row per line of the HHS Provider Relief Fund public file.
-- 419,846 rows, $135,063,804,375 on the 2026-09-07 load. File dated 2025-03-28.
--
-- What this is: every provider that attested to accepting a PRF payment, with
-- the total that provider took. Name, state, city, amount. That is all HHS
-- publishes. No EIN, NPI, CCN or program phase, so a payee cannot be joined by
-- id to anything; name_key + city + state is the bridge, and it is only as
-- good as the payee spelling its own name the way the regulator does.
--
-- The payee is who cashed the cheque. For a nursing home that is usually the
-- operating LLC ('WELLBRIDGE OF FENTON LLC'), sometimes the parent, sometimes
-- a hospital that owns a SNF wing ('COLUSA MEDICAL CENTER' with the home listed
-- as 'COLUSA MEDICAL CENTER - SNF'). Hospital money attributed to a home that
-- shares its name is the known way this over-counts.

select
    prf_row_id,
    provider_name,
    state,
    city,
    payment_amount,
    payment_raw,
    name_key,
    name_words,
    _loaded_at,
    _source_run_id
from {{ ref('stg_fed_hrsa_provider_relief_fund__payments') }}
