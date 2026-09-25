-- SEC deriv: option awards deduped to first report. Key = issuer + owner + trade date + expiration + exercise price + title; lag = first original Form 4 filing date minus trade date. Trades 2017-01-01 to 2024-09-30 only, so a first report falls inside the loaded filing window.
WITH s AS (SELECT ACCESSION_NUMBER, COALESCE(TRY_TO_DATE(FILING_DATE::varchar, 'DD-MON-YYYY'), TRY_TO_DATE(FILING_DATE::varchar)) fd,
                  DOCUMENT_TYPE, TRY_TO_NUMBER(ISSUER_CIK::varchar) cik, ISSUER_NAME, ISSUER_TICKER
           FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION)
, o AS (SELECT ACCESSION_NUMBER, MIN(TRY_TO_NUMBER(OWNER_CIK::varchar)) owner_cik FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_REPORTINGOWNER GROUP BY 1)
, d AS (SELECT ACCESSION_NUMBER, COALESCE(TRY_TO_DATE(TRANS_DATE::varchar, 'DD-MON-YYYY'), TRY_TO_DATE(TRANS_DATE::varchar)) td,
               TRY_TO_DOUBLE(CONV_EXERCISE_PRICE::varchar) px, UPPER(REGEXP_REPLACE(SECURITY_TITLE, '[^A-Za-z]', '')) ttl, EXPIRATION_DATE::varchar exp
        FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_DERIV_TRANS WHERE TRANS_CODE = 'A' AND TRY_TO_DOUBLE(CONV_EXERCISE_PRICE::varchar) > 0)
, a AS (SELECT s.cik, o.owner_cik, d.td, d.exp, d.px, d.ttl, MIN(s.fd) first_fd, MAX(s.ISSUER_NAME) issuer, MAX(s.ISSUER_TICKER) ticker, COUNT(*) lines
        FROM d JOIN s ON s.ACCESSION_NUMBER = d.ACCESSION_NUMBER LEFT JOIN o ON o.ACCESSION_NUMBER = d.ACCESSION_NUMBER
        WHERE d.td BETWEEN '2017-01-01' AND '2024-09-30' AND s.DOCUMENT_TYPE IN ('4', '5')
        GROUP BY 1, 2, 3, 4, 5, 6)
SELECT cik, YEAR(td) yr, MAX(issuer) issuer, MAX(ticker) ticker, COUNT(*) awards, SUM(lines) lines,
       COUNT_IF(DATEDIFF(day, td, first_fd) > 6) late6, COUNT_IF(DATEDIFF(day, td, first_fd) > 30) late30, COUNT_IF(DATEDIFF(day, td, first_fd) > 365) late365,
       COUNT(DISTINCT owner_cik) owners, COUNT(DISTINCT IFF(DATEDIFF(day, td, first_fd) > 30, owner_cik, NULL)) owners_late30,
       MEDIAN(DATEDIFF(day, td, first_fd)) med_lag, MAX(DATEDIFF(day, td, first_fd)) max_lag
FROM a GROUP BY 1, 2
