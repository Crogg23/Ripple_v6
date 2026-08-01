-- Encoding guard (audit F1, 2026-08-01): dbt on Windows once compiled the
-- UTF-8 model files as cp1252, shipping every em-dash to analysts as the
-- two-character mojibake prefix a-circumflex + euro-sign. The sanctioned
-- build path forces UTF-8 (build_review wrapper, PYTHONUTF8=1); THIS test
-- makes a bare mis-encoded build fail loudly instead of shipping garbled
-- text. The pattern is built with CHR() so this file is pure ASCII and the
-- test itself cannot be corrupted by the encoding bug it hunts.
-- CHR(226) = a-circumflex, CHR(8364) = euro sign. Returns offending rows.

WITH probe AS (
    SELECT '%' || CHR(226) || CHR(8364) || '%' AS pat
)

SELECT 'lead_queue' AS model, q.lead_id AS id, q.headline AS text
FROM {{ ref('lead_queue') }} q, probe p
WHERE q.headline LIKE p.pat OR q.caveat LIKE p.pat

UNION ALL

SELECT 'cohort_queue', c.cohort_id, c.headline
FROM {{ ref('cohort_queue') }} c, probe p
WHERE c.headline LIKE p.pat OR c.caveat LIKE p.pat
