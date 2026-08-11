-- Runaway-pager guard (verification 2026-08-11). Two landing tables were
-- inflated by a generated pager that re-fetched the same page in a loop:
-- the mortgage database (19M rows, 11,648 real, ~1,636x) and foreign-aid
-- spending (3.97M rows, 95,658 real, 97.6% duplicates). The existing
-- degenerate-load detector can't catch this shape - the rows are varied
-- and dense, just repeated - so this test pins the fixed marts: if exact
-- full-row duplicates ever exceed 1% again, the build fails.

{% set guarded = ['housing__fed_fhfa_nmdb', 'economics__fed_foreignassistance'] %}

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
