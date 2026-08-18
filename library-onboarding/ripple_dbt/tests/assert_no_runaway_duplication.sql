-- Runaway-pager guard (verification 2026-08-11). Two landing tables were
-- inflated by a generated pager that re-fetched the same page in a loop:
-- the mortgage database (19M rows, 11,648 real, ~1,636x) and foreign-aid
-- spending (3.97M rows, 95,658 real, 97.6% duplicates). The existing
-- degenerate-load detector can't catch this shape - the rows are varied
-- and dense, just repeated - so this test pins the fixed marts: if exact
-- full-row duplicates ever exceed 1% again, the build fails.
--
-- EXTENDED 2026-08-18 (dup-batch investigation): 7 more marts confirmed as
-- the same single-load-run exact-duplication shape (portal-crawl boilerplate
-- rows or a double-fetch, all deduped with a QUALIFY on the full data-column
-- set) -- pinned here the same way: immigration__fed_uscis_data (3,204 ->
-- 177), reference__intl_eg_capmas (150 -> 52), transport__fed_faa_data_portal
-- (4 -> 3), justice__fed_ftc_datasets (1,200 -> 1,004), science__fed_nsf_awards
-- (125 -> 115), housing__fed_hud_data (77 -> 71), immigration__fed_ice_statistics
-- (221 -> 204). NOT extended to finance__fed_fec_committees / _fec_candidates or
-- health__fed_fda_faers_reac -- those still carry real exact-row duplication
-- (23%, 19%, 76%) that was deliberately left unfixed pending a human/loader
-- call (see the DUP INVESTIGATION notes in those model files); wiring this
-- guard onto them would just fail every build, not catch a regression.

{% set guarded = ['housing__fed_fhfa_nmdb', 'economics__fed_foreignassistance',
                   'immigration__fed_uscis_data', 'reference__intl_eg_capmas',
                   'transport__fed_faa_data_portal', 'justice__fed_ftc_datasets',
                   'science__fed_nsf_awards', 'housing__fed_hud_data',
                   'immigration__fed_ice_statistics'] %}

{% for m in guarded %}
SELECT model, n_rows, n_distinct
FROM (
    SELECT '{{ m }}' AS model,
           COUNT(*) AS n_rows,
           COUNT(DISTINCT HASH(*)) AS n_distinct
    FROM {{ ref(m) }}
)
WHERE n_rows > n_distinct * 1.01
{% if not loop.last %}UNION ALL{% endif %}
{% endfor %}
