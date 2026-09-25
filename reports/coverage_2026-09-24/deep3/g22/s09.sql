-- S09 Principal committees (DSGN P) linked to 2+ candidate IDs in one cycle: same person or different people? any money?
WITH l AS (SELECT * FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_CAND_CMTE_LINK WHERE cmte_dsgn = 'P'),
sh AS (SELECT cycle, cmte_id FROM l GROUP BY 1,2 HAVING COUNT(DISTINCT cand_id) > 1),
x AS (SELECT l.cycle, l.cmte_id, l.cand_id, c.cand_name, c.office, c.office_state, c.office_district, c.party,
             REGEXP_REPLACE(UPPER(SPLIT_PART(c.cand_name, ',', 1)), '[^A-Z]', '') last_nm,
             s.ttl_receipts
      FROM l JOIN sh USING (cycle, cmte_id)
      LEFT JOIN LIBRARY_MARTS.POLITICS.POLITICS__FEC_CANDIDATE c ON c.cand_id = l.cand_id AND c.cycle = l.cycle
      LEFT JOIN LIBRARY_MARTS.POLITICS.POLITICS__FEC_CANDIDATE_SUMMARY s ON s.cand_id = l.cand_id AND s.cycle = l.cycle),
g AS (SELECT cycle, cmte_id, COUNT(DISTINCT cand_id) n_ids, COUNT(DISTINCT last_nm) n_last, COUNT(DISTINCT office_state) n_states, COUNT(DISTINCT office) n_offices,
             SUM(ttl_receipts) receipts, LISTAGG(DISTINCT cand_name || ' ' || office || '-' || office_state || COALESCE(office_district,''), '; ') who
      FROM x GROUP BY 1,2)
SELECT 'summary' kind, cycle, COUNT(*) committees, COUNT_IF(n_last = 1) same_last_name, COUNT_IF(n_last > 1) diff_last_names,
       COUNT_IF(n_states > 1) multi_state, COUNT_IF(n_offices > 1) multi_office, SUM(receipts) receipts, NULL who, NULL cmte_nm
FROM g GROUP BY 1,2
UNION ALL
SELECT 'diff_people_top', g.cycle, g.n_ids, g.n_last, g.n_states, g.n_offices, NULL, g.receipts, LEFT(g.who, 300), k.cmte_nm
FROM g LEFT JOIN LIBRARY_MARTS.POLITICS.POLITICS__FEC_COMMITTEE k ON k.cmte_id = g.cmte_id AND k.cycle = g.cycle
WHERE g.n_last > 1 QUALIFY ROW_NUMBER() OVER (PARTITION BY g.cycle ORDER BY g.receipts DESC NULLS LAST, g.n_ids DESC) <= 8
ORDER BY 1, 2, 8 DESC NULLS LAST
