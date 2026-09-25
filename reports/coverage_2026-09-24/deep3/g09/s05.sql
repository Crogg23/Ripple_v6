WITH t AS (SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_PURPLE_BOOK),
k AS (SELECT LOWER(TRIM(ref_product_proper_name)) ref, * FROM t WHERE license_type LIKE '351(k)%'),
a AS (SELECT LOWER(TRIM(proper_name)) pn, MIN(approval_date) ref_first_approval, LISTAGG(DISTINCT proprietary_name, '/') ref_brands,
             LISTAGG(DISTINCT applicant, '/') ref_makers
      FROM t WHERE license_type = '351(a)' GROUP BY 1)
SELECT k.ref, a.ref_brands, a.ref_makers, a.ref_first_approval,
       COUNT(DISTINCT k.bla_number) biosimilar_blas,
       COUNT(DISTINCT IFF(k.license_type ILIKE '%interchangeable%', k.bla_number, NULL)) interchangeable_blas,
       MIN(k.approval_date) first_biosimilar, MAX(k.approval_date) last_biosimilar,
       COUNT(DISTINCT IFF(k.marketing_status ILIKE 'disc%', k.bla_number, NULL)) blas_with_disc_row,
       COUNT(DISTINCT IFF(k.marketing_status NOT ILIKE 'disc%', k.bla_number, NULL)) blas_with_rx_row,
       LISTAGG(DISTINCT LOWER(k.proper_name), ',') biosimilar_proper_names
FROM k LEFT JOIN a ON a.pn = k.ref
GROUP BY 1,2,3,4 ORDER BY biosimilar_blas DESC, k.ref
