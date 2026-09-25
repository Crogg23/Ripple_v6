-- SEC deriv x insider submission (ACCESSION_NUMBER): days from trade to filing on original Form 4s, per issuer per trade year. Late = filed more than 6 calendar days after the trade (the rule is 2 business days, so this undercounts).
WITH d AS (SELECT ACCESSION_NUMBER, TRANS_CODE, TRANS_TIMELINESS,
                  COALESCE(TRY_TO_DATE(TRANS_DATE::varchar, 'DD-MON-YYYY'), TRY_TO_DATE(TRANS_DATE::varchar)) td,
                  TRY_TO_DOUBLE(CONV_EXERCISE_PRICE::varchar) px
           FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_DERIV_TRANS WHERE TRANS_FORM_TYPE = '4')
, s AS (SELECT ACCESSION_NUMBER, COALESCE(TRY_TO_DATE(FILING_DATE::varchar, 'DD-MON-YYYY'), TRY_TO_DATE(FILING_DATE::varchar)) fd,
               DOCUMENT_TYPE, TRY_TO_NUMBER(ISSUER_CIK::varchar) cik, ISSUER_NAME, ISSUER_TICKER
        FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION)
, j AS (SELECT d.*, s.fd, s.DOCUMENT_TYPE, s.cik, s.ISSUER_NAME, s.ISSUER_TICKER, DATEDIFF(day, d.td, s.fd) lag,
               (d.TRANS_CODE = 'A' AND d.px > 0) is_grant
        FROM d JOIN s ON s.ACCESSION_NUMBER = d.ACCESSION_NUMBER)
SELECT cik, YEAR(td) yr, MAX(ISSUER_NAME) issuer, MAX(ISSUER_TICKER) ticker, DOCUMENT_TYPE doc,
       COUNT(*) n, COUNT(DISTINCT ACCESSION_NUMBER) filings,
       COUNT_IF(lag > 6) late6, COUNT_IF(lag > 30) late30, COUNT_IF(lag < 0) neg_lag, COUNT_IF(TRANS_TIMELINESS = 'L') self_late, COUNT_IF(lag > 6 AND TRANS_TIMELINESS = 'L') late6_self,
       COUNT_IF(is_grant) grants, COUNT_IF(is_grant AND lag > 6) grants_late6, COUNT_IF(is_grant AND lag > 30) grants_late30,
       COUNT(DISTINCT IFF(is_grant AND lag > 6, ACCESSION_NUMBER, NULL)) grant_filings_late6, MEDIAN(IFF(is_grant, lag, NULL)) grant_med_lag, MAX(IFF(is_grant, lag, NULL)) grant_max_lag
FROM j WHERE td BETWEEN '2014-01-01' AND '2025-12-31'
GROUP BY 1, 2, 5
