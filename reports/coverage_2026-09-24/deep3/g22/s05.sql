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
ORDER BY 1, 2, 4 DESC
