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
FROM x WHERE congress >= 80 GROUP BY 1,2 ORDER BY 2,1
