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
ORDER BY 1, 2
