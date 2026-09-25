WITH t AS (SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_PURPLE_BOOK)
SELECT COUNT(*) n, COUNT(DISTINCT bla_number) blas, COUNT(DISTINCT bla_number || '-' || product_number) bla_products,
       COUNT(DISTINCT purple_book_record_id) rec_ids, COUNT(DISTINCT _source_run_id) runs, COUNT(DISTINCT _src_sha256) files,
       (SELECT OBJECT_AGG(COALESCE(license_type,'(null)'), c) FROM (SELECT license_type, COUNT(*) c FROM t GROUP BY 1)) lic_type,
       (SELECT OBJECT_AGG(COALESCE(marketing_status,'(null)'), c) FROM (SELECT marketing_status, COUNT(*) c FROM t GROUP BY 1)) mkt,
       (SELECT OBJECT_AGG(COALESCE(licensure,'(null)'), c) FROM (SELECT licensure, COUNT(*) c FROM t GROUP BY 1)) licensure,
       (SELECT OBJECT_AGG(COALESCE(center,'(null)'), c) FROM (SELECT center, COUNT(*) c FROM t GROUP BY 1)) center,
       (SELECT OBJECT_AGG(COALESCE(submission_type,'(null)'), c) FROM (SELECT submission_type, COUNT(*) c FROM t GROUP BY 1)) subm,
       COUNT_IF(license_type LIKE '351(k)%' AND approval_date < '2015-03-01') k_before_first_us_biosimilar,
       COUNT_IF(approval_date < '1970-01-01') pre1970, COUNT_IF(approval_date > CURRENT_DATE) future,
       COUNT_IF(approval_date BETWEEN '1970-01-01' AND '1979-12-31') y1970s,
       (SELECT ARRAY_AGG(d || ' ' || lt || ' ' || LEFT(pn,30) || ' / ' || LEFT(ap,30)) FROM (SELECT approval_date d, license_type lt, proper_name pn, applicant ap FROM t WHERE approval_date < '1970-01-01' ORDER BY approval_date LIMIT 12)) pre1970_rows,
       (SELECT ARRAY_AGG(lic || ' | ' || ap || ' | ' || LEFT(pn,40) || ' | ' || COALESCE(d::VARCHAR,'')) FROM (SELECT licensure lic, applicant ap, proper_name pn, approval_date d FROM t WHERE licensure NOT ILIKE 'licensed' ORDER BY licensure, applicant LIMIT 40)) not_licensed_rows
FROM t
