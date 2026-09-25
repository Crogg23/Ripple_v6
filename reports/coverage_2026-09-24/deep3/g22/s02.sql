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
FROM j GROUP BY 1,2 ORDER BY 1,2
