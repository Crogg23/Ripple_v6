{{ config(materialized='table') }}

select series_id, observation_date, value
from {{ ref('stg_fed_smoke_fred__series') }}
