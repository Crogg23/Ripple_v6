-- Miss test for filed-before-audit: search Form AP by ISSUER NAME (any CIK, any version) for an audit report dated on/before each original 10-K
with t as (select column1 k, column2 pat, column3::date k_filed, column4::date pd from values
  ('ECD','%ECD AUTO%','2024-05-03','2023-12-31'),('ARTISAN','%ARTISAN CONSUMER%','2024-08-16','2024-06-30'),
  ('SINGULARITY','%SINGULARITY FUTURE%','2024-10-15','2024-06-30'),('GEV','%GENERAL ENTERPRISE VENTURES%','2024-04-15','2023-12-31'),
  ('CANNONAU','%CANNONAU%','2024-04-12','2023-12-31'),('BIOSTAX','%BIOSTAX%','2024-04-16','2023-12-31'),
  ('HCTI','%HEALTHCARE TRIANGLE%','2024-03-18','2023-12-31'),('YONGBAI','%YONG BAI%','2025-04-10','2024-12-31'),
  ('BIMERGEN','%BIMERGEN%','2025-05-30','2024-12-31'),('ITC','ITC HOLDINGS%','2025-02-14','2024-12-31'),
  ('BANCORP','%BANCORP, INC%','2025-03-03','2024-12-31'),('1895','1895 BANCORP%','2024-03-29','2023-12-31'))
select t.k, t.k_filed, a.ISSUER_NAME, a.ISSUER_CIK, a.FIRM_NAME, a.FISCAL_PERIOD_END_DATE, a.AUDIT_REPORT_DATE, a.LATEST_FORM_AP_FILING,
  iff(a.AUDIT_REPORT_DATE <= t.k_filed, 'ON/BEFORE 10-K', 'after') timing
from t left join LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS a
  on upper(a.ISSUER_NAME) like t.pat and abs(datediff(day, a.FISCAL_PERIOD_END_DATE, t.pd)) <= 7
order by t.k, a.AUDIT_REPORT_DATE
