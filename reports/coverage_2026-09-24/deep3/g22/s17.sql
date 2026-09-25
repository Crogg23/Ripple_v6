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
FROM bl GROUP BY congress ORDER BY 1
