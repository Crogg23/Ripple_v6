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
ORDER BY 1 DESC, 3 DESC, 6
