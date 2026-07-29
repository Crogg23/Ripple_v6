{{ config(materialized='table', schema='HEALTH') }}

select *
from {{ ref('stg_fed_cms_nppes__npi_providers') }}
