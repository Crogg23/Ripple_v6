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
FROM w JOIN gap g USING (congress) GROUP BY w.congress, g.vote_days, g.max_gap, g.gap_from ORDER BY 1
