-- SEC insider submission: filings per quarter by document type; filing lag vs period of report
select date_trunc('quarter', FILING_DATE)::date q, count(*) n,
  count_if(DOCUMENT_TYPE='4') f4, count_if(DOCUMENT_TYPE='3') f3, count_if(DOCUMENT_TYPE='5') f5, count_if(DOCUMENT_TYPE like '%/A') amend,
  count_if(DOCUMENT_TYPE='4' and datediff('day', PERIOD_OF_REPORT, FILING_DATE) > 5) f4_gt5d,
  count_if(DOCUMENT_TYPE='4' and datediff('day', PERIOD_OF_REPORT, FILING_DATE) > 30) f4_gt30d,
  count_if(DOCUMENT_TYPE='4' and datediff('day', PERIOD_OF_REPORT, FILING_DATE) < 0) f4_neg,
  count_if(NO_SECURITIES_OWNED) no_sec, count_if(NOT_SUBJECT_TO_SECTION16) not16, count_if(PERIOD_OF_REPORT is null) por_null,
  count(distinct ISSUER_CIK) issuers
from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION
group by 1 order by 1
