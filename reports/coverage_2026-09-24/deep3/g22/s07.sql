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
ORDER BY 1, 2
