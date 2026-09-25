-- S08 FEC candidate-committee link: shape, duplicates, overlap with the FINANCE copy, land rates, shared principal committees
WITH l AS (SELECT * FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_CAND_CMTE_LINK),
f AS (SELECT * FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_CAND_CMTE_LINKAGE),
c AS (SELECT DISTINCT cand_id, cycle FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_CANDIDATE),
k AS (SELECT DISTINCT cmte_id, cycle FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_COMMITTEE),
pshare AS (SELECT cycle, cmte_id, COUNT(DISTINCT cand_id) nc, LISTAGG(DISTINCT cand_id, ',') cands FROM l WHERE cmte_dsgn = 'P' GROUP BY 1,2 HAVING COUNT(DISTINCT cand_id) > 1),
pmulti AS (SELECT cycle, cand_id, COUNT(DISTINCT cmte_id) np FROM l WHERE cmte_dsgn = 'P' GROUP BY 1,2 HAVING COUNT(DISTINCT cmte_id) > 1)
SELECT OBJECT_CONSTRUCT(
 'rows', (SELECT COUNT(*) FROM l), 'linkage_nd', (SELECT COUNT(DISTINCT linkage_id) FROM l),
 'triple_nd', (SELECT COUNT(DISTINCT cand_id, cmte_id, cycle) FROM l),
 'cycles', (SELECT OBJECT_AGG(cycle, n) FROM (SELECT cycle, COUNT(*) n FROM l GROUP BY 1)),
 'cand_yr_minus_cycle', (SELECT OBJECT_AGG(dy::VARCHAR, n) FROM (SELECT cand_election_yr - TRY_TO_NUMBER(cycle) dy, COUNT(*) n FROM l GROUP BY 1)),
 'fec_yr_eq_cycle', (SELECT COUNT_IF(fec_election_yr = TRY_TO_NUMBER(cycle)) FROM l),
 'fin_rows', (SELECT COUNT(*) FROM f), 'fin_years', (SELECT OBJECT_AGG(fec_election_yr::VARCHAR, n) FROM (SELECT fec_election_yr, COUNT(*) n FROM f GROUP BY 1)),
 'in_both_by_linkage', (SELECT COUNT(*) FROM l WHERE linkage_id IN (SELECT linkage_id FROM f)),
 'cand_lands_fec_candidate', (SELECT COUNT(*) FROM l JOIN c USING (cand_id, cycle)),
 'cmte_lands_fec_committee', (SELECT COUNT(*) FROM l JOIN k USING (cmte_id, cycle)),
 'p_cmte_shared_by_2plus_cands', (SELECT COUNT(*) FROM pshare), 'p_shared_examples', (SELECT ARRAY_AGG(cycle || ':' || cmte_id || '>' || cands) FROM (SELECT * FROM pshare ORDER BY nc DESC LIMIT 6)),
 'cands_with_2plus_p', (SELECT COUNT(*) FROM pmulti), 'max_p_per_cand', (SELECT MAX(np) FROM pmulti),
 'top_cand', (SELECT ARRAY_AGG(x) FROM (SELECT l.cycle || ' ' || l.cmte_dsgn || l.cmte_tp || ' ' || l.cmte_id || ' ' || COALESCE(LEFT(k2.cmte_nm, 45), '?') x
      FROM l LEFT JOIN LIBRARY_MARTS.POLITICS.POLITICS__FEC_COMMITTEE k2 ON k2.cmte_id = l.cmte_id AND k2.cycle = l.cycle WHERE l.cand_id = 'H6NY21173' ORDER BY 1 LIMIT 16)),
 'top_cand_name', (SELECT ANY_VALUE(cand_name || ' | ' || office_state || '-' || office_district || ' | ' || party) FROM LIBRARY_MARTS.POLITICS.POLITICS__FEC_CANDIDATE WHERE cand_id = 'H6NY21173')
) o
