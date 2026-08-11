{{ config(materialized='table', schema='JUSTICE') }}

-- Source: Ransomware.live — global ransomware victim tracker.
-- Re-pulled in full 2026-08-11: 30,661 rows (old capped table held 29,193).
-- GRAIN: one row per victim post — (post_title, group_name, discovered).
-- post_url is NOT unique in the publisher data (10,394 records lack one; 469
-- URLs repeat because groups reuse one onion homepage across posts), so the
-- old unique-post_url test was wrong even before the re-pull (460 dups on the
-- capped data). No dedupe on post_url — those rows are distinct victim posts.

with source as (
    select * from {{ source('ripple_raw', 'XC_RANSOMWARELIVE_VICTIMS_FULL_R2') }}
)

select
    POST_TITLE as post_title,
    GROUP_NAME as group_name,
    DISCOVERED as discovered,
    PUBLISHED as published,
    WEBSITE as website,
    COUNTRY as country,
    ACTIVITY as activity,
    DESCRIPTION as description,
    POST_URL as post_url
from source
