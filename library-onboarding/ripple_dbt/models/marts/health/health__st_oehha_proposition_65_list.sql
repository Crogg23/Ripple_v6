{{ config(materialized='table', schema='HEALTH') }}

-- Built 2026-08-09 (73-source backlog, wave 2c). California OEHHA Proposition 65 list of chemicals known to cause cancer or reproductive toxicity. 3 chemicals relisted under multiple toxicity types share rows -- row grain kept.
-- Grain: one row = one chemical-toxicity listing. Reads the pre-existing staging model.

select * from {{ ref('stg_st_oehha_proposition_65_list__chemical') }}
