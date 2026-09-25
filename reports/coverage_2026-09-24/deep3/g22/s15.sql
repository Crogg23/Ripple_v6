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
FROM bl GROUP BY 1 ORDER BY 1
