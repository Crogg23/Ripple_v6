{{ config(materialized='table', schema='TRANSPORT') }}

-- Built 2026-08-09 (73-source backlog, wave 2). FAA Civil Aircraft Registry,
-- 2026-08 vintage. Supersedes transport__fed_faa_registry (July snapshot on
-- the retired twin landing table -- queued for the orphan drop list).
-- Grain: one row = one registered aircraft (N-number unique).
-- Key joins: registrant name/address -> entity spine; MODE_S_CODE_HEX -> ADS-B.

select * from {{ ref('stg_fed_faa_aircraft_registry__aircraft') }}
