-- SEC deriv: option awards deduped v3 = v2 plus a count of late awards the filer marked E ('early': the filer treats it as Form 5-eligible), to test that dull explanation. Key drops exercise price (stock-dividend re-reports change it) = issuer + owner + trade date + expiration + title. Awards dated before the issuer's first filing in the insider table are dropped (pre-IPO / pre-registration awards). Trades 2017-01-01 to 2024-09-30.
WITH s AS (SELECT ACCESSION_NUMBER, COALESCE(TRY_TO_DATE(FILING_DATE::varchar, 'DD-MON-YYYY'), TRY_TO_DATE(FILING_DATE::varchar)) fd,
                  DOCUMENT_TYPE, TRY_TO_NUMBER(ISSUER_CIK::varchar) cik, ISSUER_NAME, ISSUER_TICKER
           FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION)
, f AS (SELECT cik, MIN(fd) issuer_first_fd FROM s GROUP BY 1)
, o AS (SELECT ACCESSION_NUMBER, MIN(TRY_TO_NUMBER(OWNER_CIK::varchar)) owner_cik FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_REPORTINGOWNER GROUP BY 1)
, d AS (SELECT ACCESSION_NUMBER, COALESCE(TRY_TO_DATE(TRANS_DATE::varchar, 'DD-MON-YYYY'), TRY_TO_DATE(TRANS_DATE::varchar)) td,
               UPPER(REGEXP_REPLACE(SECURITY_TITLE, '[^A-Za-z]', '')) ttl, EXPIRATION_DATE::varchar exp, TRANS_TIMELINESS tl
        FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_DERIV_TRANS WHERE TRANS_CODE = 'A' AND TRY_TO_DOUBLE(CONV_EXERCISE_PRICE::varchar) > 0)
, a AS (SELECT s.cik, o.owner_cik, d.td, d.exp, d.ttl, MIN(s.fd) first_fd, MAX(s.ISSUER_NAME) issuer, MAX(s.ISSUER_TICKER) ticker, COUNT(*) lines, MAX(IFF(d.tl = 'E', 1, 0)) e_flag
        FROM d JOIN s ON s.ACCESSION_NUMBER = d.ACCESSION_NUMBER LEFT JOIN o ON o.ACCESSION_NUMBER = d.ACCESSION_NUMBER
        WHERE d.td BETWEEN '2017-01-01' AND '2024-09-30' AND s.DOCUMENT_TYPE IN ('4', '5')
        GROUP BY 1, 2, 3, 4, 5)
SELECT a.cik, YEAR(a.td) yr, MAX(a.issuer) issuer, MAX(a.ticker) ticker, MAX(f.issuer_first_fd) issuer_first_fd,
       COUNT_IF(a.td < f.issuer_first_fd) pre_first_dropped,
       COUNT_IF(a.td >= f.issuer_first_fd) awards, SUM(IFF(a.td >= f.issuer_first_fd, lines, 0)) lines,
       COUNT_IF(a.td >= f.issuer_first_fd AND DATEDIFF(day, a.td, a.first_fd) > 6) late6,
       COUNT_IF(a.td >= f.issuer_first_fd AND DATEDIFF(day, a.td, a.first_fd) > 30) late30,
       COUNT_IF(a.td >= f.issuer_first_fd AND DATEDIFF(day, a.td, a.first_fd) > 365) late365,
       COUNT_IF(a.td >= f.issuer_first_fd AND DATEDIFF(day, a.td, a.first_fd) > 30 AND a.e_flag = 1) late30_e,
       COUNT_IF(a.td >= f.issuer_first_fd AND a.e_flag = 1) awards_e,
       COUNT(DISTINCT IFF(a.td >= f.issuer_first_fd, a.owner_cik, NULL)) owners,
       COUNT(DISTINCT IFF(a.td >= f.issuer_first_fd AND DATEDIFF(day, a.td, a.first_fd) > 30, a.owner_cik, NULL)) owners_late30,
       MEDIAN(IFF(a.td >= f.issuer_first_fd, DATEDIFF(day, a.td, a.first_fd), NULL)) med_lag,
       MAX(IFF(a.td >= f.issuer_first_fd, DATEDIFF(day, a.td, a.first_fd), NULL)) max_lag
FROM a JOIN f ON f.cik = a.cik GROUP BY 1, 2
