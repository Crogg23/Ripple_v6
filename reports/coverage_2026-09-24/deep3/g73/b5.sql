-- S14 XWALK_HOSPITAL_CCN_EIN: do units and suffixed CCNs carry the same EIN as their parent hospital row in the table?
WITH x AS (SELECT CCN, EIN FROM LIBRARY_MARTS.CORE.XWALK_HOSPITAL_CCN_EIN),
k AS (SELECT CCN, EIN,
             CASE WHEN REGEXP_LIKE(CCN, '^[0-9]{6}$') THEN 'plain'
                  WHEN REGEXP_LIKE(CCN, '^[0-9]{2}[A-Z][0-9]{3}$') THEN 'unit_' || SUBSTR(CCN, 3, 1)
                  ELSE 'suffixed' END kind,
             CASE WHEN REGEXP_LIKE(CCN, '^[0-9]{2}[A-Z][0-9]{3}$')
                  THEN LEFT(CCN, 2) || IFF(SUBSTR(CCN, 3, 1) IN ('Z', 'M', 'R'), '1', '0') || SUBSTR(CCN, 4, 3)
                  WHEN NOT REGEXP_LIKE(CCN, '^[0-9]{6}$') THEN LEFT(CCN, 6) END parent
      FROM x)
SELECT IFF(GROUPING(k.kind) = 1, 'ALL', k.kind) kind, COUNT(*) ccns, COUNT_IF(p.CCN IS NOT NULL) parent_in_xwalk,
       COUNT_IF(p.EIN = k.EIN) same_ein_as_parent, COUNT_IF(p.CCN IS NOT NULL AND p.EIN <> k.EIN) other_ein,
       COUNT(DISTINCT k.EIN) eins
FROM k LEFT JOIN x p ON p.CCN = k.parent
GROUP BY ROLLUP (k.kind) ORDER BY 2 DESC
