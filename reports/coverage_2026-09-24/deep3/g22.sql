-- deep3/g22: 2026-09-24 deep pass. Python door, QUERY_TAG 'deep3-2026-09-24'.
-- Every connection first ran: ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300; ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'.
-- Those two lines are not counted. Every statement below is a read (SELECT / WITH).
-- Tables: VOTEVIEW_ROLLCALLS, FEC_CAND_CMTE_LINK, INTL_OWID_MILSPEND, XC_OWID_CPI, FED_DOJ_EPSTEIN_LIBRARY (all LIBRARY_MARTS.POLITICS).

-- S01 column names and types
-- S01 column names and types for the 5 tables plus the join partners
SELECT table_schema, table_name, LISTAGG(column_name || ':' || data_type, ', ') WITHIN GROUP (ORDER BY ordinal_position) cols
FROM LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS
WHERE table_name IN ('POLITICS__VOTEVIEW_ROLLCALLS','POLITICS__FEC_CAND_CMTE_LINK','POLITICS__INTL_OWID_MILSPEND','POLITICS__XC_OWID_CPI',
  'POLITICS__FED_DOJ_EPSTEIN_LIBRARY','POLITICS__FED_VOTEVIEW_ROLLCALL_META','POLITICS__FEC_COMMITTEE','FINANCE__FED_FEC_CAND_CMTE_LINKAGE',
  'POLITICS__FEC_CANDIDATE','POLITICS__INTL_FREEDOMHOUSE','POLITICS__FEC_CANDIDATE_SUMMARY')
GROUP BY 1,2 ORDER BY 1,2;

-- S02 rollcalls profile vs META
-- S02 ROLLCALLS profile per Congress/chamber, and a row-by-row match to the full Voteview META table
WITH r AS (SELECT * FROM LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_ROLLCALLS),
m AS (SELECT congress, chamber, TRY_TO_NUMBER(rollnumber) rn, TRY_TO_DATE(date) d, yea_count, nay_count, vote_result, vote_question, bill_number
      FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_VOTEVIEW_ROLLCALL_META WHERE congress IN (118,119)),
j AS (SELECT r.congress, r.chamber, r.rollnumber, r.vote_date, r.yea_count ry, r.nay_count rn_, r.vote_result rr, r.vote_question rq, r.bill_number rb,
             m.rn, m.d, m.yea_count my, m.nay_count mn, m.vote_result mr, m.vote_question mq, m.bill_number mb
      FROM r FULL OUTER JOIN m ON r.congress = m.congress AND r.chamber = m.chamber AND r.rollnumber = m.rn)
SELECT COALESCE(j.congress, 0) congress, j.chamber,
  COUNT(j.rollnumber) r_rows, COUNT(DISTINCT j.rollnumber) r_rolls, MIN(j.vote_date) r_first, MAX(j.vote_date) r_last,
  COUNT(j.rn) m_rows, MAX(j.d) m_last, COUNT_IF(j.rollnumber IS NOT NULL AND j.rn IS NOT NULL) matched,
  COUNT_IF(j.rollnumber IS NULL) only_meta, COUNT_IF(j.rn IS NULL) only_r,
  COUNT_IF(j.vote_date <> j.d) date_diff, COUNT_IF(j.ry <> j.my OR j.rn_ <> j.mn) tally_diff,
  COUNT_IF(NULLIF(TRIM(j.rr),'') IS NULL AND j.rollnumber IS NOT NULL) r_result_blank, COUNT_IF(NULLIF(TRIM(j.rq),'') IS NULL AND j.rollnumber IS NOT NULL) r_question_blank,
  COUNT_IF(NULLIF(TRIM(j.rb),'') IS NULL AND j.rollnumber IS NOT NULL) r_bill_blank,
  COUNT_IF(COALESCE(j.rr,'') <> COALESCE(j.mr,'') AND j.rn IS NOT NULL AND j.rollnumber IS NOT NULL) result_diff,
  COUNT_IF(j.ry + j.rn_ = 0) zero_tally,
  COUNT_IF(j.rr ILIKE '%fail%' OR j.rr ILIKE '%reject%' OR j.rr ILIKE '%not%') r_failed_like,
  (SELECT OBJECT_AGG(COALESCE(vote_result,'(null)'), c) FROM (SELECT vote_result, COUNT(*) c FROM r GROUP BY 1 ORDER BY 2 DESC LIMIT 14)) top_results_all
FROM j GROUP BY 1,2 ORDER BY 1,2;

-- S03 META history by Congress, day-538 window
-- S03 Voteview META history: roll calls per Congress and chamber by day 538 (the ROLLCALLS window), nomination votes, failed votes, fill rates
WITH m AS (SELECT congress, chamber, TRY_TO_NUMBER(rollnumber) rn, TRY_TO_DATE(date) d, vote_result, vote_question, bill_number, vote_desc, dtl_desc
           FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_VOTEVIEW_ROLLCALL_META),
s AS (SELECT congress, MIN(d) start_d FROM m GROUP BY 1),
x AS (SELECT m.*, DATEDIFF(day, s.start_d, m.d) dayn,
        (bill_number ILIKE 'PN%' OR vote_question ILIKE '%nomination%') nom,
        (vote_result ILIKE '%fail%' OR vote_result ILIKE '%reject%' OR vote_result ILIKE '%not agreed%' OR vote_result ILIKE '%not sustained%') failed,
        (chamber = 'House' AND bill_number ILIKE 'HRES%' AND (vote_question ILIKE '%agreeing to the resolution%' OR vote_question ILIKE '%previous question%')) rule_vote
      FROM m JOIN s USING (congress))
SELECT congress, chamber, MIN(d) first_d, MAX(d) last_d, COUNT(*) rolls, COUNT(DISTINCT rn) rolls_nd, COUNT_IF(d IS NULL) d_null,
  COUNT_IF(dayn <= 538) by_d538,
  COUNT_IF(dayn <= 538 AND nom) nom_by_d538,
  COUNT_IF(nom) nom_all,
  COUNT_IF(NULLIF(TRIM(vote_result),'') IS NOT NULL) result_filled, COUNT_IF(NULLIF(TRIM(vote_question),'') IS NOT NULL) question_filled,
  COUNT_IF(NULLIF(TRIM(bill_number),'') IS NOT NULL) bill_filled,
  COUNT_IF(failed) failed_all, COUNT_IF(failed AND dayn <= 538) failed_by_d538,
  COUNT_IF(rule_vote) rule_votes, COUNT_IF(rule_vote AND failed) rule_failed
FROM x WHERE congress >= 80 GROUP BY 1,2 ORDER BY 2,1;

-- S04 House composition + longest gap, day 538
-- S04 House, Congress 101-119, first 538 days: what kind of votes, the longest gap with no vote, and failed rules (desc says "providing for consideration")
WITH m AS (SELECT congress, chamber, TRY_TO_NUMBER(rollnumber) rn, TRY_TO_DATE(date) d, vote_result, vote_question q, bill_number, vote_desc, dtl_desc
           FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_VOTEVIEW_ROLLCALL_META WHERE congress >= 101),
s AS (SELECT congress, MIN(d) start_d FROM m GROUP BY 1),
h AS (SELECT m.*, DATEDIFF(day, s.start_d, m.d) dayn FROM m JOIN s USING (congress) WHERE chamber = 'House'),
w AS (SELECT * FROM h WHERE dayn <= 538),
days AS (SELECT congress, d, LAG(d) OVER (PARTITION BY congress ORDER BY d) prev_d FROM (SELECT DISTINCT congress, d FROM w)),
gap AS (SELECT congress, MAX(DATEDIFF(day, prev_d, d)) max_gap, MAX_BY(prev_d, DATEDIFF(day, prev_d, d)) gap_from, COUNT(*) vote_days FROM days GROUP BY 1)
SELECT w.congress, COUNT(*) rolls, g.vote_days, g.max_gap, g.gap_from,
  COUNT_IF(q ILIKE '%suspend%') suspension,
  COUNT_IF(q ILIKE '%amendment%') amendment,
  COUNT_IF(q ILIKE '%passage%') passage,
  COUNT_IF(q ILIKE '%previous question%' OR (bill_number ILIKE 'HRES%' AND q ILIKE '%agreeing to the resolution%' AND (vote_desc ILIKE '%providing for%consideration%' OR dtl_desc ILIKE '%providing for%consideration%'))) rule_or_pq,
  COUNT_IF(q ILIKE '%table%') to_table,
  COUNT_IF(q ILIKE '%recommit%') recommit,
  COUNT_IF(q ILIKE '%journal%' OR q ILIKE '%adjourn%' OR q ILIKE '%quorum%') journal_adjourn_quorum,
  COUNT_IF(q ILIKE '%election of the speaker%' OR q ILIKE '%speaker%') speaker,
  COUNT_IF(bill_number ILIKE 'HRES%' AND q ILIKE '%agreeing to the resolution%' AND (vote_desc ILIKE '%providing for%consideration%' OR dtl_desc ILIKE '%providing for%consideration%')
           AND (vote_result ILIKE '%fail%' OR vote_result ILIKE '%not agreed%')) rule_failed_w,
  COUNT_IF(q ILIKE '%previous question%' AND (vote_result ILIKE '%fail%' OR vote_result ILIKE '%not agreed%')) pq_failed_w,
  COUNT_IF(vote_result ILIKE '%fail%' AND q ILIKE '%suspend%') susp_failed_w,
  COUNT_IF(NULLIF(TRIM(vote_desc),'') IS NULL AND NULLIF(TRIM(dtl_desc),'') IS NULL) no_desc
FROM w JOIN gap g USING (congress) GROUP BY w.congress, g.vote_days, g.max_gap, g.gap_from ORDER BY 1;

-- S05 House amendment roll calls 118 vs 119
-- S05 House amendment roll calls, 118th vs 119th, first 538 days: which bills, and by month (ROLLCALLS table itself)
WITH r AS (SELECT congress, rollnumber, vote_date, vote_question q, vote_result, bill_number, vote_desc,
                  DATEDIFF(day, IFF(congress = 118, '2023-01-03'::DATE, '2025-01-03'::DATE), vote_date) dayn
           FROM LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_ROLLCALLS WHERE chamber = 'House'),
a AS (SELECT * FROM r WHERE dayn <= 538 AND q ILIKE '%amendment%'),
bills AS (SELECT congress, bill_number, COUNT(*) n, MIN(vote_date) d0, MAX(vote_date) d1, ANY_VALUE(LEFT(vote_desc, 60)) descr,
                 ROW_NUMBER() OVER (PARTITION BY congress ORDER BY COUNT(*) DESC) k
          FROM a GROUP BY 1,2),
qs AS (SELECT congress, q, COUNT(*) n, ROW_NUMBER() OVER (PARTITION BY congress ORDER BY COUNT(*) DESC) k FROM a GROUP BY 1,2)
SELECT 'bill' kind, congress, bill_number item, n, d0::VARCHAR d0, d1::VARCHAR d1, descr FROM bills WHERE k <= 10
UNION ALL SELECT 'question', congress, q, n, NULL, NULL, NULL FROM qs WHERE k <= 6
UNION ALL SELECT 'month', congress, TO_CHAR(DATE_TRUNC(month, vote_date), 'YYYY-MM'), COUNT(*), NULL, NULL, NULL FROM a GROUP BY 2,3
UNION ALL SELECT 'bills_with_amdt_votes', congress, NULL, COUNT(DISTINCT bill_number), NULL, NULL, NULL FROM a GROUP BY 2
ORDER BY 1, 2, 4 DESC;

-- S06 delegate check + clerk completeness
-- S06 Two independent checks on the House amendment drop:
--   (a) roll calls where any delegate (AS GU PR MP VI DC) cast a yea/nay: delegates vote only in Committee of the Whole, where amendments are voted
--   (b) completeness: META roll calls per calendar year vs the Clerk's highest roll number that year
WITH del AS (SELECT DISTINCT TRY_TO_NUMBER(icpsr) icpsr, congress FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_VOTEVIEW_MEMBERS
             WHERE chamber = 'House' AND state_abbrev IN ('AS','GU','PR','MP','VI','DC') AND congress IN (118,119)),
dv AS (SELECT v.congress, v.rollnumber FROM LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_VOTES v JOIN del ON del.icpsr = v.icpsr AND del.congress = v.congress
       WHERE v.chamber = 'House' AND v.cast_code BETWEEN 1 AND 6 GROUP BY 1,2),
r AS (SELECT congress, rollnumber, vote_question q, DATEDIFF(day, IFF(congress = 118, '2023-01-03'::DATE, '2025-01-03'::DATE), vote_date) dayn
      FROM LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_ROLLCALLS WHERE chamber = 'House'),
a AS (SELECT r.congress, COUNT(*) rolls_d538, COUNT(dv.rollnumber) delegate_voted, COUNT_IF(dv.rollnumber IS NOT NULL AND r.q ILIKE '%amendment%') delegate_and_amdt,
             COUNT_IF(dv.rollnumber IS NULL AND r.q ILIKE 'On Agreeing to the Amendment%') amdt_no_delegate,
             COUNT_IF(dv.rollnumber IS NOT NULL AND NOT r.q ILIKE '%amendment%') delegate_not_amdt
      FROM r LEFT JOIN dv ON dv.congress = r.congress AND dv.rollnumber = r.rollnumber WHERE r.dayn <= 538 GROUP BY 1),
c AS (SELECT congress, YEAR(TRY_TO_DATE(date)) yr, COUNT(*) n, MAX(TRY_TO_NUMBER(clerk_rollnumber)) clerk_max, COUNT(DISTINCT clerk_rollnumber) clerk_nd
      FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_VOTEVIEW_ROLLCALL_META WHERE chamber = 'House' AND congress IN (117,118,119) GROUP BY 1,2)
SELECT 'delegate' kind, congress, rolls_d538 a1, delegate_voted a2, delegate_and_amdt a3, amdt_no_delegate a4, delegate_not_amdt a5 FROM a
UNION ALL SELECT 'clerk_' || yr, congress, n, clerk_max, clerk_nd, NULL, NULL FROM c
ORDER BY 1, 2;

-- S07 Senate 119 by month and failed votes
-- S07 Senate 119th by month (ROLLCALLS): nomination votes, cloture, amendments, failed, en bloc; plus what the failed votes were
WITH r AS (SELECT vote_date, vote_question q, vote_result res, bill_number b, vote_desc,
                  (b ILIKE 'PN%' OR q ILIKE '%nomination%') nom,
                  (res ILIKE '%fail%' OR res ILIKE '%reject%' OR res ILIKE '%not agreed%' OR res ILIKE '%not sustained%') failed
           FROM LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_ROLLCALLS WHERE chamber = 'Senate' AND congress = 119)
SELECT 'month' kind, TO_CHAR(DATE_TRUNC(month, vote_date), 'YYYY-MM') k, COUNT(*) n, COUNT_IF(nom) nom, COUNT_IF(res = 'Nomination Confirmed') confirmed,
       COUNT_IF(q ILIKE '%cloture%') cloture, COUNT_IF(q ILIKE '%amendment%') amdt, COUNT_IF(failed) failed,
       COUNT_IF(vote_desc ILIKE '%en bloc%' OR b ILIKE 'SRES%') en_bloc_or_sres
FROM r GROUP BY 1,2
UNION ALL
SELECT 'failed_by_question', LEFT(q, 60), COUNT(*), COUNT_IF(nom), NULL, NULL, NULL, COUNT(DISTINCT b), NULL FROM r WHERE failed GROUP BY 1,2
UNION ALL
SELECT 'failed_by_bill', b || ' ' || LEFT(COALESCE(ANY_VALUE(vote_desc), ''), 50), COUNT(*), NULL, NULL, NULL, NULL, NULL, NULL FROM r WHERE failed GROUP BY 1, b QUALIFY ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) <= 8
ORDER BY 1, 2;

-- S08 FEC link shape and overlaps
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
) o;

-- S09 shared principal committees: same person or not
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
ORDER BY 1, 2, 8 DESC NULLS LAST;

-- S10 milspend shape, zeros, repeats
-- S10 OWID military spending: shape, units, zeros, repeated values, series that stop
WITH t AS (SELECT entity, NULLIF(TRIM(code),'') code, year, military_expenditure raw, TRY_TO_DOUBLE(military_expenditure) v, world_region_according_to_owid reg
           FROM LIBRARY_MARTS.POLITICS.POLITICS__INTL_OWID_MILSPEND),
e AS (SELECT entity, code, MIN(year) y0, MAX(year) y1, COUNT(*) n, COUNT_IF(v = 0) zeros, MAX_BY(v, year) last_v FROM t GROUP BY 1,2),
rep AS (SELECT entity, v, COUNT(*) n, MIN(year) y0, MAX(year) y1 FROM t WHERE v > 0 GROUP BY 1,2 HAVING COUNT(*) >= 3)
SELECT OBJECT_CONSTRUCT(
 'rows', (SELECT COUNT(*) FROM t), 'entities', (SELECT COUNT(DISTINCT entity) FROM t), 'with_code', (SELECT COUNT(DISTINCT entity) FROM t WHERE code IS NOT NULL),
 'dup_entity_year', (SELECT COUNT(*) - COUNT(DISTINCT entity, year) FROM t),
 'year_range', (SELECT MIN(year) || '-' || MAX(year) FROM t), 'rows_by_decade', (SELECT OBJECT_AGG(dec::VARCHAR, n) FROM (SELECT FLOOR(year/10)*10 dec, COUNT(*) n FROM t GROUP BY 1)),
 'non_numeric', (SELECT COUNT(*) FROM t WHERE v IS NULL), 'non_numeric_sample', (SELECT ARRAY_AGG(DISTINCT raw) WITHIN GROUP (ORDER BY raw) FROM (SELECT raw FROM t WHERE v IS NULL LIMIT 20)),
 'no_code_entities', (SELECT ARRAY_AGG(entity || ' ' || y0 || '-' || y1) FROM e WHERE code IS NULL),
 'zeros_total', (SELECT COUNT_IF(v = 0) FROM t), 'zeros_top', (SELECT ARRAY_AGG(entity || ':' || zeros || ' (' || y0 || '-' || y1 || ')') FROM (SELECT * FROM e WHERE zeros > 0 ORDER BY zeros DESC LIMIT 12)),
 'repeated_values', (SELECT COUNT(*) FROM rep), 'repeated_rows', (SELECT SUM(n) FROM rep),
 'repeated_top', (SELECT ARRAY_AGG(entity || ' ' || v || ' x' || n || ' ' || y0 || '-' || y1) FROM (SELECT * FROM rep ORDER BY n DESC LIMIT 12)),
 'series_stop_before_2020', (SELECT ARRAY_AGG(entity || ' ' || y1) FROM (SELECT * FROM e WHERE code IS NOT NULL AND y1 < 2020 ORDER BY y1 DESC LIMIT 25)),
 'n_stop_before_2020', (SELECT COUNT(*) FROM e WHERE code IS NOT NULL AND y1 < 2020),
 'entities_in_max_year', (SELECT COUNT(*) FROM t WHERE year = (SELECT MAX(year) FROM t)),
 'usa', (SELECT ARRAY_AGG(year || ':' || raw) WITHIN GROUP (ORDER BY year DESC) FROM (SELECT * FROM t WHERE code = 'USA' ORDER BY year DESC LIMIT 6)),
 'world', (SELECT ARRAY_AGG(year || ':' || raw) WITHIN GROUP (ORDER BY year DESC) FROM (SELECT * FROM t WHERE entity = 'World' ORDER BY year DESC LIMIT 4)),
 'usa_1950_1970', (SELECT ARRAY_AGG(year || ':' || raw) WITHIN GROUP (ORDER BY year) FROM t WHERE code = 'USA' AND year IN (1949,1950,1960,1968,1980,2000)),
 'regions', (SELECT OBJECT_AGG(COALESCE(reg,'(null)'), n) FROM (SELECT reg, COUNT(DISTINCT entity) n FROM t GROUP BY 1))
) o;

-- S11 milspend 2021-2025 growth by region
-- S11 Military spending 2021 -> 2025 (constant dollars) by country, ranked inside its OWID region; region medians; 2024 -> 2025 fallers
WITH t AS (SELECT entity, NULLIF(TRIM(code),'') code, year, TRY_TO_DOUBLE(military_expenditure) v, NULLIF(world_region_according_to_owid,'') reg
           FROM LIBRARY_MARTS.POLITICS.POLITICS__INTL_OWID_MILSPEND),
p AS (SELECT entity, reg, MAX(IFF(year = 2021, v, NULL)) v21, MAX(IFF(year = 2024, v, NULL)) v24, MAX(IFF(year = 2025, v, NULL)) v25
      FROM t WHERE code IS NOT NULL AND code NOT LIKE 'OWID%' GROUP BY 1,2),
g AS (SELECT *, v25 / NULLIF(v21, 0) - 1 g2125, v25 / NULLIF(v24, 0) - 1 g2425,
             MEDIAN(v25 / NULLIF(v21, 0) - 1) OVER (PARTITION BY reg) reg_med, COUNT(v25 / NULLIF(v21, 0)) OVER (PARTITION BY reg) reg_n,
             RANK() OVER (PARTITION BY reg ORDER BY v25 / NULLIF(v21, 0) DESC NULLS LAST) rk,
             v25 / SUM(v25) OVER () share25
      FROM p WHERE v21 > 0 AND v25 > 0)
SELECT 'top_in_region' kind, reg, entity, rk, ROUND(v21/1e9, 2) b21, ROUND(v24/1e9, 2) b24, ROUND(v25/1e9, 2) b25, ROUND(g2125*100, 1) pct_21_25, ROUND(reg_med*100, 1) reg_med_pct, reg_n, ROUND(g2425*100,1) pct_24_25
FROM g WHERE rk <= 5
UNION ALL
SELECT 'biggest_2425_fall', reg, entity, NULL, ROUND(v21/1e9,2), ROUND(v24/1e9,2), ROUND(v25/1e9,2), ROUND(g2125*100,1), ROUND(reg_med*100,1), reg_n, ROUND(g2425*100,1)
FROM g WHERE v24 > 5e9 QUALIFY ROW_NUMBER() OVER (ORDER BY g2425) <= 8
UNION ALL
SELECT 'top_share_2025', reg, entity, ROW_NUMBER() OVER (ORDER BY v25 DESC), NULL, ROUND(v24/1e9,2), ROUND(v25/1e9,2), ROUND(g2125*100,1), ROUND(share25*100,1), NULL, ROUND(g2425*100,1)
FROM g QUALIFY ROW_NUMBER() OVER (ORDER BY v25 DESC) <= 8
UNION ALL
SELECT 'counts', 'all', NULL, COUNT(*), NULL, NULL, NULL, ROUND(MEDIAN(g2125)*100,1), NULL, COUNT_IF(g2425 < 0), ROUND(MEDIAN(g2425)*100,1) FROM g
ORDER BY 1, 2, 4;

-- S12 CPI shape, drops within region, new lows
-- S12 CPI: shape, then change from first comparable year to latest inside each OWID region; who hit a series low in the latest year
WITH t AS (SELECT entity, NULLIF(TRIM(code),'') code, year, corruption_perceptions_index s, NULLIF(world_region_according_to_owid,'') reg
           FROM LIBRARY_MARTS.POLITICS.POLITICS__XC_OWID_CPI),
shape AS (SELECT OBJECT_CONSTRUCT('rows', COUNT(*), 'entities', COUNT(DISTINCT entity), 'no_code', COUNT(DISTINCT IFF(code IS NULL, entity, NULL)),
            'years', MIN(year) || '-' || MAX(year), 'dup', COUNT(*) - COUNT(DISTINCT entity, year), 'null_score', COUNT_IF(s IS NULL),
            'min', MIN(s), 'max', MAX(s), 'non_integer', COUNT_IF(s <> ROUND(s)),
            'per_year', (SELECT OBJECT_AGG(year::VARCHAR, n) FROM (SELECT year, COUNT(*) n FROM t GROUP BY 1)),
            'no_code_list', (SELECT ARRAY_AGG(DISTINCT entity) FROM t WHERE code IS NULL),
            'usa', (SELECT ARRAY_AGG(year || ':' || s) WITHIN GROUP (ORDER BY year) FROM t WHERE code = 'USA')) o FROM t),
lastyr AS (SELECT MAX(year) y FROM t),
p AS (SELECT entity, reg, MAX(IFF(year = 2012, s, NULL)) s12, MAX(IFF(year = (SELECT y FROM lastyr), s, NULL)) sl,
             MIN(IFF(year < (SELECT y FROM lastyr), s, NULL)) prior_min, MAX(s) best, MAX_BY(year, s) best_yr
      FROM t WHERE code IS NOT NULL AND year >= 2012 GROUP BY 1,2),
g AS (SELECT *, sl - s12 d, MEDIAN(sl - s12) OVER (PARTITION BY reg) reg_med, COUNT(sl - s12) OVER (PARTITION BY reg) reg_n,
             RANK() OVER (PARTITION BY reg ORDER BY sl - s12) rk_drop FROM p WHERE s12 IS NOT NULL AND sl IS NOT NULL)
SELECT 'shape' kind, NULL reg, NULL entity, NULL a, NULL b, NULL c, NULL d, NULL e, (SELECT o FROM shape)::VARCHAR note FROM dual
UNION ALL SELECT 'drop_in_region', reg, entity, s12, sl, d, reg_med, reg_n, 'best ' || best || ' in ' || best_yr FROM g WHERE rk_drop <= 4
UNION ALL SELECT 'new_low_latest', reg, entity, s12, sl, d, prior_min, NULL, 'best ' || best || ' in ' || best_yr FROM g WHERE sl < prior_min AND s12 >= 60
UNION ALL SELECT 'counts', NULL, NULL, COUNT(*), COUNT_IF(sl < prior_min), COUNT_IF(d < 0), MEDIAN(d), COUNT_IF(d <= -10), NULL FROM g
ORDER BY 1, 2, 6;

-- S13 Epstein crawl pages and links
-- S13 DOJ Epstein library crawl: pages, link kinds, file links per page, EFTA number range per page (tests the page-1-only cap)
WITH t AS (SELECT page_url, href, resolved_url, link_text, fetched_at_utc, _loaded_at,
                  CASE WHEN resolved_url ILIKE '%/epstein/files/%' THEN 'file'
                       WHEN resolved_url ILIKE '%/media/%' THEN 'media'
                       WHEN resolved_url ILIKE '%facebook%' OR resolved_url ILIKE '%twitter%' OR resolved_url ILIKE '%x.com%' OR resolved_url ILIKE '%linkedin%' THEN 'share'
                       WHEN resolved_url ILIKE '%justice.gov%' THEN 'doj_other' ELSE 'other' END kind,
                  TRY_TO_NUMBER(REGEXP_SUBSTR(resolved_url, 'EFTA0*([0-9]+)', 1, 1, 'ie', 1)) efta
           FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_DOJ_EPSTEIN_LIBRARY)
SELECT 'page' k, REGEXP_REPLACE(page_url, '^https?://[^/]+', '') item, COUNT(*) n, COUNT_IF(kind = 'file') files, COUNT_IF(kind = 'media') media,
       COUNT_IF(kind = 'share') share, MIN(efta) efta_min, MAX(efta) efta_max, COUNT(DISTINCT efta) efta_nd, MIN(fetched_at_utc)::VARCHAR t0, MAX(fetched_at_utc)::VARCHAR t1
FROM t GROUP BY 1,2
UNION ALL
SELECT 'kind', kind, COUNT(*), COUNT(DISTINCT resolved_url), COUNT(DISTINCT page_url), NULL, NULL, NULL, NULL,
       ANY_VALUE(LEFT(resolved_url, 90)), NULL FROM t GROUP BY 1,2
UNION ALL
SELECT 'file_ext', LOWER(REGEXP_SUBSTR(resolved_url, '\.([a-zA-Z0-9]{2,4})(\?|$)', 1, 1, 'e', 1)), COUNT(*), COUNT(DISTINCT resolved_url), NULL, NULL, NULL, NULL, NULL, NULL, NULL
FROM t WHERE kind = 'file' GROUP BY 1,2
UNION ALL
SELECT 'loads', NULL, COUNT(*), COUNT(DISTINCT _loaded_at), COUNT(DISTINCT fetched_at_utc), COUNT(DISTINCT page_url, href), NULL, NULL, NULL, MIN(_loaded_at)::VARCHAR, MAX(_loaded_at)::VARCHAR FROM t
ORDER BY 1, 2;
-- S13 FAILED: Snowflake rejected the regex escape; no rows returned. Rerun as S14.

-- S14 Epstein crawl pages and links (rerun)
-- S14 (rerun of S13, which failed on a regex escape) DOJ Epstein library crawl: pages, link kinds, file links per page, EFTA number range per page (tests the page-1-only cap)
WITH t AS (SELECT page_url, href, resolved_url, link_text, fetched_at_utc, _loaded_at,
                  CASE WHEN resolved_url ILIKE '%/epstein/files/%' THEN 'file'
                       WHEN resolved_url ILIKE '%/media/%' THEN 'media'
                       WHEN resolved_url ILIKE '%facebook%' OR resolved_url ILIKE '%twitter%' OR resolved_url ILIKE '%x.com%' OR resolved_url ILIKE '%linkedin%' THEN 'share'
                       WHEN resolved_url ILIKE '%justice.gov%' THEN 'doj_other' ELSE 'other' END kind,
                  TRY_TO_NUMBER(REGEXP_SUBSTR(resolved_url, 'EFTA0*([0-9]+)', 1, 1, 'ie', 1)) efta
           FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_DOJ_EPSTEIN_LIBRARY)
SELECT 'page' k, REGEXP_REPLACE(page_url, '^https?://[^/]+', '') item, COUNT(*) n, COUNT_IF(kind = 'file') files, COUNT_IF(kind = 'media') media,
       COUNT_IF(kind = 'share') share, MIN(efta) efta_min, MAX(efta) efta_max, COUNT(DISTINCT efta) efta_nd, MIN(fetched_at_utc)::VARCHAR t0, MAX(fetched_at_utc)::VARCHAR t1
FROM t GROUP BY 1,2
UNION ALL
SELECT 'kind', kind, COUNT(*), COUNT(DISTINCT resolved_url), COUNT(DISTINCT page_url), NULL, NULL, NULL, NULL,
       ANY_VALUE(LEFT(resolved_url, 90)), NULL FROM t GROUP BY 1,2
UNION ALL
SELECT 'file_ext', LOWER(REGEXP_SUBSTR(resolved_url, '[.]([a-zA-Z0-9]{2,4})([?]|$)', 1, 1, 'e', 1)), COUNT(*), COUNT(DISTINCT resolved_url), NULL, NULL, NULL, NULL, NULL, NULL, NULL
FROM t WHERE kind = 'file' GROUP BY 1,2
UNION ALL
SELECT 'loads', NULL, COUNT(*), COUNT(DISTINCT _loaded_at), COUNT(DISTINCT fetched_at_utc), COUNT(DISTINCT page_url, href), NULL, NULL, NULL, MIN(_loaded_at)::VARCHAR, MAX(_loaded_at)::VARCHAR FROM t
ORDER BY 1, 2;

-- S15 bills with passage votes vs amendment votes, NDAA peer
-- S15 Inside the group: of House bills that reached a passage vote by day 538, how many got any recorded amendment vote? Plus the NDAA as a like-for-like peer
WITH m AS (SELECT congress, TRY_TO_DATE(date) d, vote_question q, UPPER(REPLACE(bill_number, ' ', '')) b, COALESCE(vote_desc, '') || ' ' || COALESCE(dtl_desc, '') descr
           FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_VOTEVIEW_ROLLCALL_META WHERE chamber = 'House' AND congress >= 104),
s AS (SELECT congress, MIN(d) start_d FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_VOTEVIEW_ROLLCALL_META WHERE congress >= 104 GROUP BY 1),
w AS (SELECT m.* FROM m JOIN s USING (congress) WHERE DATEDIFF(day, s.start_d, m.d) <= 538 AND b IS NOT NULL AND b <> ''),
bl AS (SELECT congress, b, COUNT_IF(q ILIKE 'On Passage%') pass_v, COUNT_IF(q ILIKE 'On Agreeing to the Amendment%') amdt_v,
              MAX(IFF(descr ILIKE '%national defense authorization%', 1, 0)) ndaa
       FROM w GROUP BY 1,2)
SELECT congress,
  COUNT_IF(pass_v > 0) bills_with_passage_vote,
  COUNT_IF(pass_v > 0 AND amdt_v > 0) of_which_had_amdt_vote,
  ROUND(100 * COUNT_IF(pass_v > 0 AND amdt_v > 0) / NULLIF(COUNT_IF(pass_v > 0), 0), 1) pct_with_amdt_vote,
  SUM(IFF(pass_v > 0, amdt_v, 0)) amdt_votes_on_passed_bills,
  MEDIAN(IFF(pass_v > 0 AND amdt_v > 0, amdt_v, NULL)) median_amdt_votes_when_any,
  SUM(IFF(ndaa = 1, amdt_v, 0)) ndaa_amdt_votes, LISTAGG(DISTINCT IFF(ndaa = 1, b, NULL), ',') ndaa_bills
FROM bl GROUP BY 1 ORDER BY 1;
-- S15 FAILED: compile error (used column D on the raw META table). Rerun as S16.

-- S16 bills with passage votes vs amendment votes, NDAA peer (rerun)
-- S16 (rerun of S15, which failed: wrong column name) Inside the group: of House bills that reached a passage vote by day 538, how many got any recorded amendment vote? Plus the NDAA as a like-for-like peer
WITH m AS (SELECT congress, TRY_TO_DATE(date) d, vote_question q, UPPER(REPLACE(bill_number, ' ', '')) b, COALESCE(vote_desc, '') || ' ' || COALESCE(dtl_desc, '') descr
           FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_VOTEVIEW_ROLLCALL_META WHERE chamber = 'House' AND congress >= 104),
s AS (SELECT congress, MIN(d) start_d FROM m GROUP BY 1),
w AS (SELECT m.* FROM m JOIN s USING (congress) WHERE DATEDIFF(day, s.start_d, m.d) <= 538 AND b IS NOT NULL AND b <> ''),
bl AS (SELECT congress, b, COUNT_IF(q ILIKE 'On Passage%') pass_v, COUNT_IF(q ILIKE 'On Agreeing to the Amendment%') amdt_v,
              MAX(IFF(descr ILIKE '%national defense authorization%', 1, 0)) ndaa
       FROM w GROUP BY 1,2)
SELECT congress,
  COUNT_IF(pass_v > 0) bills_with_passage_vote,
  COUNT_IF(pass_v > 0 AND amdt_v > 0) of_which_had_amdt_vote,
  ROUND(100 * COUNT_IF(pass_v > 0 AND amdt_v > 0) / NULLIF(COUNT_IF(pass_v > 0), 0), 1) pct_with_amdt_vote,
  SUM(IFF(pass_v > 0, amdt_v, 0)) amdt_votes_on_passed_bills,
  MEDIAN(IFF(pass_v > 0 AND amdt_v > 0, amdt_v, NULL)) median_amdt_votes_when_any,
  SUM(IFF(ndaa = 1, amdt_v, 0)) ndaa_amdt_votes, LISTAGG(DISTINCT IFF(ndaa = 1, b, NULL), ',') ndaa_bills
FROM bl GROUP BY 1 ORDER BY 1;

-- S17 H.R. bills only: passage vs amendment votes
-- S17 Dull-explanation test for S16: count only H.R. bills (drops H.J.Res. such as Congressional Review Act resolutions, which allow no amendments, and Senate bills). Of House bills that reached a passage vote by day 538, how many got any recorded amendment vote?
WITH m AS (SELECT congress, TRY_TO_DATE(date) d, vote_question q, UPPER(REPLACE(bill_number, ' ', '')) b, COALESCE(vote_desc, '') || ' ' || COALESCE(dtl_desc, '') descr
           FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_VOTEVIEW_ROLLCALL_META WHERE chamber = 'House' AND congress >= 104),
s AS (SELECT congress, MIN(d) start_d FROM m GROUP BY 1),
w AS (SELECT m.* FROM m JOIN s USING (congress) WHERE DATEDIFF(day, s.start_d, m.d) <= 538 AND REGEXP_LIKE(b, 'HR[0-9]+')),
bl AS (SELECT congress, b, COUNT_IF(q ILIKE 'On Passage%') pass_v, COUNT_IF(q ILIKE 'On Agreeing to the Amendment%') amdt_v,
              MAX(IFF(descr ILIKE '%national defense authorization%', 1, 0)) ndaa
       FROM w GROUP BY 1,2)
SELECT congress,
  COUNT_IF(pass_v > 0) bills_with_passage_vote,
  COUNT_IF(pass_v > 0 AND amdt_v > 0) of_which_had_amdt_vote,
  ROUND(100 * COUNT_IF(pass_v > 0 AND amdt_v > 0) / NULLIF(COUNT_IF(pass_v > 0), 0), 1) pct_with_amdt_vote,
  SUM(IFF(pass_v > 0, amdt_v, 0)) amdt_votes_on_passed_bills,
  MEDIAN(IFF(pass_v > 0 AND amdt_v > 0, amdt_v, NULL)) median_amdt_votes_when_any,
  COUNT(*) hr_bills_any_vote,
  COUNT_IF(pass_v = 0 AND amdt_v > 0) amdt_but_no_passage
FROM bl GROUP BY congress ORDER BY 1;

-- S18 CPI new lows by year
-- S18 CPI time check: in each year, how many countries scored below every earlier year since 2012 (a new low)? Is 2024 unusual?
WITH t AS (SELECT entity, year, corruption_perceptions_index s FROM LIBRARY_MARTS.POLITICS.POLITICS__XC_OWID_CPI WHERE year >= 2012),
f AS (SELECT entity, MAX(IFF(year = 2012, s, NULL)) s12 FROM t GROUP BY 1),
x AS (SELECT t.entity, t.year, t.s, f.s12,
             MIN(t.s) OVER (PARTITION BY t.entity ORDER BY t.year ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) prior_min,
             MAX(t.s) OVER (PARTITION BY t.entity ORDER BY t.year ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) prior_max,
             t.s - LAG(t.s) OVER (PARTITION BY t.entity ORDER BY t.year) yoy
      FROM t JOIN f USING (entity))
SELECT year, COUNT(*) n, COUNT_IF(s < prior_min) new_low, COUNT_IF(s > prior_max) new_high,
       COUNT_IF(s < prior_min AND s12 >= 60) new_low_s12_60plus, COUNT_IF(s12 >= 60) n_s12_60plus,
       MEDIAN(yoy) med_yoy, MEDIAN(IFF(s12 >= 60, yoy, NULL)) med_yoy_60plus, COUNT_IF(yoy <= -3) drop3plus
FROM x WHERE year >= 2014 GROUP BY 1 ORDER BY 1;

-- S19 milspend breaks over 40 percent
-- S19 Military spending breaks: year-on-year swings over 40% for countries spending over $5B, 2010-2025, plus Mexico's full recent series
WITH t AS (SELECT entity, NULLIF(TRIM(code),'') code, year, TRY_TO_DOUBLE(military_expenditure) v FROM LIBRARY_MARTS.POLITICS.POLITICS__INTL_OWID_MILSPEND),
x AS (SELECT entity, year, v, LAG(v) OVER (PARTITION BY entity ORDER BY year) pv, LEAD(v) OVER (PARTITION BY entity ORDER BY year) nv FROM t WHERE code IS NOT NULL)
SELECT 'swing' k, entity, year, ROUND(pv/1e9, 2) prev_b, ROUND(v/1e9, 2) b, ROUND(nv/1e9, 2) next_b, ROUND(100*(v/pv - 1), 1) pct_yoy,
       IFF(nv IS NOT NULL AND ABS(nv/pv - 1) < 0.15, 'spike-and-back', '') shape
FROM x WHERE year >= 2010 AND GREATEST(v, pv) > 5e9 AND pv > 0 AND ABS(v/pv - 1) > 0.40
UNION ALL
SELECT 'mexico', entity, year, NULL, ROUND(v/1e9, 2), NULL, ROUND(100*(v/pv - 1), 1), NULL FROM x WHERE entity = 'Mexico' AND year >= 2015
ORDER BY 1, 2, 3;

-- S20 eyeball 119th bills with and without amendment votes
-- S20 Eyeball: 119th House H.R. bills with a passage vote (ROLLCALLS): the 14 with amendment votes, and the 10 closest passages with none. Titles from GovInfo bill status.
WITH r AS (SELECT rollnumber, vote_date, vote_question q, UPPER(REPLACE(bill_number, ' ', '')) b, yea_count, nay_count, vote_result
           FROM LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_ROLLCALLS WHERE chamber = 'House' AND congress = 119 AND vote_date <= '2026-06-25'),
bl AS (SELECT b, COUNT_IF(q ILIKE 'On Agreeing to the Amendment%') amdt_v,
              MAX_BY(vote_date, IFF(q ILIKE 'On Passage%', rollnumber, NULL)) pass_date,
              MAX_BY(yea_count || '-' || nay_count, IFF(q ILIKE 'On Passage%', rollnumber, NULL)) pass_tally,
              MAX_BY(ABS(yea_count - nay_count), IFF(q ILIKE 'On Passage%', rollnumber, NULL)) margin,
              COUNT_IF(q ILIKE 'On Passage%') pass_v
       FROM r WHERE REGEXP_LIKE(b, 'HR[0-9]+') GROUP BY 1),
bs AS (SELECT TRY_TO_NUMBER(bill_number) n, ANY_VALUE(title) title FROM LIBRARY_MARTS.POLITICS.POLITICS__FED_GOVINFO_BILLSTATUS
       WHERE congress = 119 AND UPPER(bill_type) = 'HR' GROUP BY 1)
SELECT IFF(amdt_v > 0, 'with_amdt_votes', 'closest_no_amdt') k, b, amdt_v, pass_date, pass_tally, margin, LEFT(bs.title, 80) title
FROM bl LEFT JOIN bs ON bs.n = TRY_TO_NUMBER(SUBSTR(b, 3))
WHERE pass_v > 0
QUALIFY amdt_v > 0 OR ROW_NUMBER() OVER (PARTITION BY (amdt_v > 0) ORDER BY margin) <= 10
ORDER BY 1 DESC, 3 DESC, 6;
