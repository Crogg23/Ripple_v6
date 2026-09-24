-- deep-4: coverage deep pass, 2026-09-24
-- Tables: FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS, HEALTH__ADDICTION_PRESCRIBERS_PAID,
--         HEALTH__FED_CLINICALTRIALS, HEALTH__FED_CMS_DIALYSIS, HEALTH__FED_CMS_HCRIS
-- Door: Python (connect/db.py). Every connection first ran:
--   ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
--   ALTER SESSION SET QUERY_TAG = 'coverage-b-2026-09-24';
-- Read-only: SELECT / WITH only.

-- Q1 counts+samples
-- SEC nonderiv: size and junk profile
SELECT COUNT(*) n, COUNT(DISTINCT ACCESSION_NUMBER) filings,
  MIN(TRANSACTION_DATE) dmin, MAX(TRANSACTION_DATE) dmax,
  SUM(IFF(TRANSACTION_DATE BETWEEN '2000-01-01' AND '2026-09-24',1,0)) n_sane_date,
  SUM(IFF(YEAR(TRANSACTION_DATE)=2022,1,0)) y22, SUM(IFF(YEAR(TRANSACTION_DATE)=2023,1,0)) y23,
  SUM(IFF(YEAR(TRANSACTION_DATE)=2024,1,0)) y24, SUM(IFF(YEAR(TRANSACTION_DATE)=2025,1,0)) y25, SUM(IFF(YEAR(TRANSACTION_DATE)=2026,1,0)) y26,
  SUM(IFF(YEAR(TRANSACTION_DATE)<2022,1,0)) pre22,
  SUM(IFF(TRANSACTION_CODE='S',1,0)) n_s, SUM(IFF(TRANSACTION_CODE='P',1,0)) n_p,
  SUM(IFF(TRANSACTION_VALUE>1e10,1,0)) n_over10b, SUM(IFF(PRICE_PER_SHARE=0,1,0)) n_price0
FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS;

-- Q2 counts+samples
-- SEC nonderiv: sample
SELECT ACCESSION_NUMBER, SECURITY_TITLE, TRANSACTION_DATE, TRANSACTION_CODE, SHARES, PRICE_PER_SHARE, TRANSACTION_VALUE, ACQUIRED_DISPOSED, SHARES_OWNED_AFTER, OWNERSHIP_FORM, FORM_TYPE
FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS LIMIT 5;

-- Q3 counts+samples
-- Addiction prescribers: size and profile
SELECT COUNT(*) n, COUNT(DISTINCT NPI) npis, MIN(DATA_YEAR) y0, MAX(DATA_YEAR) y1,
  SUM(IFF(WAS_PAID_2022,1,0)) n_paid, SUM(IFF(TOTAL_PAYMENTS>0,1,0)) n_pay_gt0,
  SUM(ADDICTION_DRUG_COST) cost, MEDIAN(ADDICTION_DRUG_COST) med_cost,
  COUNT(DISTINCT TOP_MANUFACTURER) n_mfr, COUNT(DISTINCT ADDICTION_DRUGS) n_druglists,
  SUM(IFF(ADDICTION_DRUGS ILIKE '%vivitrol%',1,0)) n_vivitrol, SUM(IFF(ADDICTION_DRUGS ILIKE '%sublocade%',1,0)) n_sublocade,
  SUM(IFF(ADDICTION_DRUGS ILIKE '%methadone%',1,0)) n_methadone
FROM LIBRARY_MARTS.HEALTH.HEALTH__ADDICTION_PRESCRIBERS_PAID;

-- Q4 counts+samples
-- Addiction prescribers: sample
SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__ADDICTION_PRESCRIBERS_PAID LIMIT 5;

-- Q5 counts+samples
-- Clinical trials: size and profile
SELECT COUNT(*) n, COUNT(DISTINCT NCT_ID) ncts,
  SUM(IFF(HAS_RESULTS,1,0)) n_has_results, SUM(IFF(RESULTS_FIRST_POSTED_DATE IS NOT NULL,1,0)) n_res_date,
  SUM(IFF(DAYS_TO_RESULTS_POSTING IS NOT NULL,1,0)) n_days_res,
  SUM(IFF(HAS_RESULTS AND RESULTS_FIRST_POSTED_DATE IS NULL,1,0)) n_flag_nodate,
  SUM(IFF(IS_FDA_REGULATED_DRUG IS NULL,1,0)) n_fdadrug_null,
  SUM(IFF(IS_FDA_REGULATED_DRUG OR IS_FDA_REGULATED_DEVICE,1,0)) n_fda_reg,
  MAX(RESULTS_FIRST_POSTED_DATE) max_res, MAX(LAST_UPDATE_POSTED_DATE) max_upd,
  COUNT(DISTINCT PHASE) n_phase, COUNT(DISTINCT OVERALL_STATUS) n_status
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CLINICALTRIALS;

-- Q6 counts+samples
-- Clinical trials: sample
SELECT NCT_ID, OVERALL_STATUS, PHASE, STUDY_TYPE, PRIMARY_COMPLETION_DATE, COMPLETION_DATE, RESULTS_FIRST_POSTED_DATE, DAYS_TO_RESULTS_POSTING, HAS_RESULTS, ENROLLMENT, LEAD_SPONSOR_NAME, LEAD_SPONSOR_CLASS, IS_FDA_REGULATED_DRUG, IS_FDA_REGULATED_DEVICE, LEFT(LOCATIONS,120) loc
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CLINICALTRIALS LIMIT 5;

-- Q7 counts+samples
-- Dialysis: size and chain profile (COUNT by chain)
SELECT CHAIN_ORGANIZATION, COUNT(*) n, COUNT(DISTINCT CCN) ccns, AVG(FIVE_STAR) stars,
  SUM(IFF(MORTALITY_RATE_FACILITY IS NULL,1,0)) mort_null, MIN(MORTALITY_RATE_FACILITY) mmin, MAX(MORTALITY_RATE_FACILITY) mmax
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_DIALYSIS GROUP BY 1 ORDER BY 2 DESC LIMIT 25;

-- Q8 counts+samples
-- Dialysis: sample
SELECT CCN, FACILITY_NAME, STATE, CHAIN_ORGANIZATION, PROFIT_OR_NON_PROFIT, FIVE_STAR, PATIENT_SURVIVAL_CATEGORY_TEXT, MORTALITY_RATE_FACILITY, HOSPITALIZATION_RATE_FACILITY, READMISSION_RATE_FACILITY, STANDARD_INFECTION_RATIO, NUMBER_OF_PATIENTS_INCLUDED_IN_SURVIVAL_SUMMARY
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_DIALYSIS LIMIT 5;

-- Q9 counts+samples
-- HCRIS: size, duplicate reports, S-10 fill
SELECT COUNT(*) n, COUNT(DISTINCT PROVIDER_CCN) ccns, COUNT(DISTINCT RPT_REC_NUM) rpts,
  COUNT(DISTINCT PROVIDER_CCN||YEAR(FISCAL_YEAR_END_DATE)) ccn_years,
  SUM(IFF(FISCAL_YEAR_LENGTH_DAYS<300,1,0)) short_rpts,
  COUNT(DISTINCT TYPE_OF_CONTROL) n_ctrl, MIN(SOURCE_FILE_YEAR) sy0, MAX(SOURCE_FILE_YEAR) sy1,
  MAX(TOTAL_BAD_DEBT_EXPENSE) max_bd, MAX(COST_OF_CHARITY_CARE) max_cc,
  SUM(IFF(COST_OF_CHARITY_CARE IS NOT NULL,1,0)) cc_filled, SUM(IFF(TOTAL_BAD_DEBT_EXPENSE IS NOT NULL,1,0)) bd_filled
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS;

-- Q10 counts+samples
-- HCRIS: sample
SELECT RPT_REC_NUM, PROVIDER_CCN, HOSPITAL_NAME, STATE_CODE, TYPE_OF_CONTROL, CCN_FACILITY_TYPE, FISCAL_YEAR_BEGIN_DATE, FISCAL_YEAR_END_DATE, FISCAL_YEAR_LENGTH_DAYS, SOURCE_FILE_YEAR, COST_OF_CHARITY_CARE, TOTAL_BAD_DEBT_EXPENSE, TOTAL_COSTS, COST_TO_CHARGE_RATIO
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS LIMIT 5;

-- Q11 SEC insider
-- SEC: top open-market sellers (code S), 2015-2026, price 0.01-10,000, value <= $10B; aggregate per filing first, then attach issuer + first owner
WITH s AS (
  SELECT ACCESSION_NUMBER, SUM(SHARES*PRICE_PER_SHARE) v, SUM(TRANSACTION_VALUE) tv, COUNT(*) n,
         MIN(TRANSACTION_DATE) d0, MAX(TRANSACTION_DATE) d1, MIN(PRICE_PER_SHARE) pmin, MAX(PRICE_PER_SHARE) pmax
  FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS
  WHERE TRANSACTION_CODE='S' AND TRANSACTION_DATE BETWEEN '2015-01-01' AND '2026-09-24'
    AND PRICE_PER_SHARE BETWEEN 0.01 AND 10000 AND TRANSACTION_VALUE <= 1e10
  GROUP BY 1),
o AS (SELECT ACCESSION_NUMBER, MIN(OWNER_NAME) owner, COUNT(*) n_owners, MIN(RELATIONSHIP) rel
      FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_REPORTINGOWNER GROUP BY 1),
sub AS (SELECT ACCESSION_NUMBER, MIN(ISSUER_NAME) issuer, MIN(ISSUER_TICKER) tkr
        FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION GROUP BY 1)
SELECT sub.issuer, sub.tkr, o.owner, MAX(o.n_owners) max_owners, MIN(o.rel) rel,
       ROUND(SUM(s.v)/1e6,1) sale_musd, ROUND(SUM(s.tv)/1e6,1) tv_musd, SUM(s.n) trades, COUNT(*) filings,
       MIN(s.d0) first_d, MAX(s.d1) last_d, MIN(s.pmin) pmin, MAX(s.pmax) pmax,
       (SELECT COUNT(*) FROM s) all_s_filings, (SELECT ROUND(SUM(v)/1e9,1) FROM s) all_s_busd
FROM s JOIN sub ON sub.ACCESSION_NUMBER=s.ACCESSION_NUMBER LEFT JOIN o ON o.ACCESSION_NUMBER=s.ACCESSION_NUMBER
GROUP BY 1,2,3 ORDER BY sale_musd DESC LIMIT 30;

-- Q12 SEC insider
-- Is the 10b5-1 plan checkbox (AFF10B5ONE) or the footnotes file anywhere in the warehouse?
SELECT 'RAW' db, TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME FROM LIBRARY_RAW.INFORMATION_SCHEMA.COLUMNS
 WHERE COLUMN_NAME ILIKE '%10B5%' OR (TABLE_NAME ILIKE '%INSIDER%' AND (COLUMN_NAME ILIKE '%FOOTNOTE%' OR COLUMN_NAME ILIKE 'AFF%'))
UNION ALL
SELECT 'MARTS', TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME FROM LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS
 WHERE COLUMN_NAME ILIKE '%10B5%' OR (TABLE_NAME ILIKE '%INSIDER%' AND (COLUMN_NAME ILIKE '%FOOTNOTE%' OR COLUMN_NAME ILIKE 'AFF%'));

-- Q13 SEC insider
-- SEC x FDA Class I recalls: insider sales in the 30 days before a recall starts vs the control window 90-60 days before, same issuer.
-- Issuer and recalling firm matched on a normalized full name (suffixes stripped); match list printed for eyeballing.
WITH norm_iss AS (
  SELECT DISTINCT ACCESSION_NUMBER, ISSUER_NAME,
    TRIM(REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(UPPER(ISSUER_NAME),'[^A-Z0-9 ]',' '),
      '\b(INC|INCORPORATED|CORP|CORPORATION|CO|COMPANY|LTD|LLC|LP|PLC|HOLDINGS|HOLDING|THE|SA|NV|AG|DE|NEW)\b',' '),' +',' ')) k
  FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION),
sales AS (
  SELECT i.k, MIN(i.ISSUER_NAME) issuer, t.TRANSACTION_DATE d, SUM(t.SHARES*t.PRICE_PER_SHARE) v
  FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS t JOIN norm_iss i ON i.ACCESSION_NUMBER=t.ACCESSION_NUMBER
  WHERE t.TRANSACTION_CODE='S' AND t.TRANSACTION_DATE BETWEEN '2015-01-01' AND '2025-12-31'
    AND t.PRICE_PER_SHARE BETWEEN 0.01 AND 10000 AND t.TRANSACTION_VALUE <= 1e10
  GROUP BY 1,3),
rec AS (
  SELECT DISTINCT TRIM(REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(UPPER(RECALLING_FIRM),'[^A-Z0-9 ]',' '),
      '\b(INC|INCORPORATED|CORP|CORPORATION|CO|COMPANY|LTD|LLC|LP|PLC|HOLDINGS|HOLDING|THE|SA|NV|AG|DE|NEW)\b',' '),' +',' ')) k,
    RECALL_INITIATION_DATE ev
  FROM (SELECT RECALLING_FIRM, RECALL_INITIATION_DATE, CLASSIFICATION FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DRUG_ENFORCEMENT
        UNION ALL SELECT RECALLING_FIRM, RECALL_INITIATION_DATE, CLASSIFICATION FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DEVICE_ENFORCEMENT)
  WHERE CLASSIFICATION='Class I' AND RECALL_INITIATION_DATE BETWEEN '2015-04-01' AND '2025-12-31'),
m AS (SELECT DISTINCT k FROM rec WHERE k IN (SELECT k FROM sales) AND k LIKE '% %'),
per AS (
  SELECT r.k, r.ev,
    SUM(IFF(DATEDIFF('day', s.d, r.ev) BETWEEN 1 AND 30, s.v, 0)) pre30,
    SUM(IFF(DATEDIFF('day', s.d, r.ev) BETWEEN 61 AND 90, s.v, 0)) ctl30,
    SUM(IFF(DATEDIFF('day', r.ev, s.d) BETWEEN 0 AND 29, s.v, 0)) post30
  FROM rec r JOIN m ON m.k=r.k JOIN sales s ON s.k=r.k
  GROUP BY 1,2)
SELECT k, COUNT(*) events, ROUND(SUM(pre30)/1e6,1) pre30_m, ROUND(SUM(ctl30)/1e6,1) ctl30_m, ROUND(SUM(post30)/1e6,1) post30_m,
  (SELECT COUNT(*) FROM m) n_matched_issuers,
  (SELECT ROUND(SUM(pre30)/1e6,1) FROM per) all_pre_m, (SELECT ROUND(SUM(ctl30)/1e6,1) FROM per) all_ctl_m, (SELECT ROUND(SUM(post30)/1e6,1) FROM per) all_post_m
FROM per GROUP BY 1 ORDER BY pre30_m DESC LIMIT 30;

-- Q14 SEC insider
-- SEC: who sold big in a month, and where was the stock 4-9 months later? Price series = the issuer's own insider
-- open-market trade prices (codes S and P), monthly median. Price 1-10,000, value <= $10B, 2015-2025.
-- Split guard: ratio within 4% of 1/2,1/3,1/4,1/5,1/10,1/20,1/50 is flagged SPLIT? (a split looks like a crash here).
WITH t AS (
  SELECT ACCESSION_NUMBER, TRANSACTION_DATE d, TRANSACTION_CODE c, SHARES sh, PRICE_PER_SHARE p
  FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS
  WHERE TRANSACTION_CODE IN ('S','P') AND TRANSACTION_DATE BETWEEN '2015-01-01' AND '2025-12-31'
    AND PRICE_PER_SHARE BETWEEN 1 AND 10000 AND TRANSACTION_VALUE <= 1e10),
sub AS (SELECT ACCESSION_NUMBER, MIN(LTRIM(ISSUER_CIK,'0')) cik, MIN(ISSUER_NAME) issuer, MIN(ISSUER_TICKER) tkr
        FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION GROUP BY 1),
own AS (SELECT ACCESSION_NUMBER, MIN(OWNER_NAME) owner, MIN(RELATIONSHIP) rel, MIN(TITLE) title
        FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_REPORTINGOWNER GROUP BY 1),
tt AS (SELECT t.*, sub.cik, sub.issuer, sub.tkr, own.owner, own.rel, own.title
       FROM t JOIN sub ON sub.ACCESSION_NUMBER=t.ACCESSION_NUMBER LEFT JOIN own ON own.ACCESSION_NUMBER=t.ACCESSION_NUMBER),
px AS (SELECT cik, DATE_TRUNC('month', d) m, MEDIAN(p) mp FROM tt GROUP BY 1,2),
sells AS (SELECT cik, MIN(issuer) issuer, MIN(tkr) tkr, owner, MIN(rel) rel, MIN(title) title, DATE_TRUNC('month', d) m,
                 SUM(sh*p) v, MEDIAN(p) sp
          FROM tt WHERE c='S' GROUP BY cik, owner, DATE_TRUNC('month', d) HAVING SUM(sh*p) >= 5e6),
fw AS (SELECT s.cik, s.owner, s.m, MEDIAN(px.mp) later_p, COUNT(*) later_months
       FROM sells s JOIN px ON px.cik=s.cik AND px.m BETWEEN DATEADD('month',4,s.m) AND DATEADD('month',9,s.m)
       GROUP BY 1,2,3),
j AS (SELECT s.*, fw.later_p, fw.later_months, fw.later_p/NULLIF(s.sp,0) r FROM sells s JOIN fw ON fw.cik=s.cik AND fw.owner=s.owner AND fw.m=s.m)
SELECT issuer, tkr, owner, rel, LEFT(title,30) title, TO_CHAR(m,'YYYY-MM') mon, ROUND(v/1e6,1) sold_m, ROUND(sp,2) sale_px, ROUND(later_p,2) later_px, ROUND(r,3) ratio, later_months,
  IFF(ABS(r-0.5)<0.02 OR ABS(r-0.3333)<0.0133 OR ABS(r-0.25)<0.01 OR ABS(r-0.2)<0.008 OR ABS(r-0.1)<0.004 OR ABS(r-0.05)<0.002 OR ABS(r-0.02)<0.0008,'SPLIT?','') split_flag,
  (SELECT COUNT(*) FROM j) n_sell_months, (SELECT COUNT_IF(r<=0.5) FROM j) n_drop50, (SELECT ROUND(SUM(IFF(r<=0.5,v,0))/1e9,2) FROM j) drop50_busd, (SELECT ROUND(SUM(v)/1e9,1) FROM j) all_busd
FROM j WHERE r <= 0.5 ORDER BY v DESC LIMIT 40;

-- Q15 addiction
-- Addiction: which brands sit under the generic names? Part D 2022, brand x generic totals for buprenorphine / naltrexone / methadone / lofexidine
SELECT BRAND_NAME, GENERIC_NAME, COUNT(DISTINCT NPI) npis, SUM(TOTAL_CLAIMS) claims, ROUND(SUM(TOTAL_DRUG_COST)/1e6,1) cost_m
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PARTD_PRESCRIBERS
WHERE GENERIC_NAME ILIKE '%buprenorphine%' OR GENERIC_NAME ILIKE '%naltrexone%' OR GENERIC_NAME ILIKE '%methadone%' OR GENERIC_NAME ILIKE '%lofexidine%'
GROUP BY 1,2 ORDER BY cost_m DESC;

-- Q16 addiction
-- Addiction: payment buckets inside each prescriber type (peers), median claims and cost
WITH b AS (
  SELECT IFF(PRESCRIBER_TYPE IN (SELECT PRESCRIBER_TYPE FROM LIBRARY_MARTS.HEALTH.HEALTH__ADDICTION_PRESCRIBERS_PAID GROUP BY 1 ORDER BY COUNT(*) DESC LIMIT 6), PRESCRIBER_TYPE, 'Other') ptype,
    CASE WHEN TOTAL_PAYMENTS=0 THEN '0 none' WHEN TOTAL_PAYMENTS<100 THEN '1 <100' WHEN TOTAL_PAYMENTS<1000 THEN '2 100-1K'
         WHEN TOTAL_PAYMENTS<10000 THEN '3 1K-10K' ELSE '4 10K+' END bucket, *
  FROM LIBRARY_MARTS.HEALTH.HEALTH__ADDICTION_PRESCRIBERS_PAID)
SELECT ptype, bucket, COUNT(*) n, MEDIAN(ADDICTION_CLAIMS) med_claims, ROUND(MEDIAN(ADDICTION_DRUG_COST)) med_cost, ROUND(SUM(ADDICTION_DRUG_COST)/1e6,1) cost_m,
  ROUND(AVG(IFF(ADDICTION_DRUGS ILIKE '%methadone%',1,0)),2) share_methadone
FROM b GROUP BY 1,2 ORDER BY 1,2;

-- Q17 addiction
-- Addiction: does a maker's money line up with its own brand's share? Open Payments 2022 by NPI and maker, Part D 2022 by NPI and brand.
-- Classes: OUD bup = all Bup/Naloxone + brand 'Buprenorphine Hcl' (mono tabs) + Sublocade; naltrexone = Naltrexone Hcl + Vivitrol; pain bup = Belbuca + Butrans + brand 'Buprenorphine' (generic patch).
WITH op AS (
  SELECT NPI,
    SUM(IFF(APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME ILIKE '%INDIVIOR%', TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS,0)) indivior,
    SUM(IFF(APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME ILIKE '%ALKERMES%', TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS,0)) alkermes,
    SUM(IFF(APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME ILIKE '%OREXO%', TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS,0)) orexo,
    SUM(IFF(APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME ILIKE '%BIODELIVERY%' OR APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME ILIKE '%COLLEGIUM%', TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS,0)) bdsi
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_2022
  WHERE (APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME ILIKE ANY ('%INDIVIOR%','%ALKERMES%','%OREXO%','%BIODELIVERY%','%COLLEGIUM%')) AND NPI IS NOT NULL AND NPI <> ''
  GROUP BY 1),
pd AS (
  SELECT NPI,
    SUM(IFF(GENERIC_NAME='Buprenorphine Hcl/Naloxone Hcl' OR BRAND_NAME IN ('Buprenorphine Hcl','Sublocade'), TOTAL_CLAIMS,0)) oud_cl,
    SUM(IFF(BRAND_NAME IN ('Suboxone','Sublocade'), TOTAL_CLAIMS,0)) indiv_cl,
    SUM(IFF(BRAND_NAME='Zubsolv', TOTAL_CLAIMS,0)) orexo_cl,
    SUM(IFF(BRAND_NAME IN ('Naltrexone Hcl','Vivitrol'), TOTAL_CLAIMS,0)) ntx_cl,
    SUM(IFF(BRAND_NAME='Vivitrol', TOTAL_CLAIMS,0)) viv_cl,
    SUM(IFF(BRAND_NAME IN ('Belbuca','Butrans','Buprenorphine'), TOTAL_CLAIMS,0)) pain_cl,
    SUM(IFF(BRAND_NAME='Belbuca', TOTAL_CLAIMS,0)) belb_cl
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PARTD_PRESCRIBERS
  WHERE GENERIC_NAME ILIKE '%buprenorphine%' OR BRAND_NAME IN ('Naltrexone Hcl','Vivitrol')
  GROUP BY 1),
j AS (SELECT pd.*, COALESCE(op.indivior,0) indivior, COALESCE(op.alkermes,0) alkermes, COALESCE(op.orexo,0) orexo, COALESCE(op.bdsi,0) bdsi
      FROM pd LEFT JOIN op ON op.NPI=pd.NPI)
SELECT 'Indivior: Suboxone+Sublocade / OUD bup' test, IFF(indivior>0,'paid','not paid') grp, COUNT(*) n, ROUND(SUM(indiv_cl)/NULLIF(SUM(oud_cl),0),3) pooled_share, ROUND(MEDIAN(indiv_cl/NULLIF(oud_cl,0)),3) med_share, MEDIAN(oud_cl) med_class_claims, ROUND(SUM(indivior)) money FROM j WHERE oud_cl>0 GROUP BY 1,2
UNION ALL
SELECT 'Orexo: Zubsolv / OUD bup', IFF(orexo>0,'paid','not paid'), COUNT(*), ROUND(SUM(orexo_cl)/NULLIF(SUM(oud_cl),0),3), ROUND(MEDIAN(orexo_cl/NULLIF(oud_cl,0)),3), MEDIAN(oud_cl), ROUND(SUM(orexo)) FROM j WHERE oud_cl>0 GROUP BY 1,2
UNION ALL
SELECT 'Alkermes: Vivitrol / naltrexone', IFF(alkermes>0,'paid','not paid'), COUNT(*), ROUND(SUM(viv_cl)/NULLIF(SUM(ntx_cl),0),3), ROUND(MEDIAN(viv_cl/NULLIF(ntx_cl,0)),3), MEDIAN(ntx_cl), ROUND(SUM(alkermes)) FROM j WHERE ntx_cl>0 GROUP BY 1,2
UNION ALL
SELECT 'BDSI/Collegium: Belbuca / pain bup', IFF(bdsi>0,'paid','not paid'), COUNT(*), ROUND(SUM(belb_cl)/NULLIF(SUM(pain_cl),0),3), ROUND(MEDIAN(belb_cl/NULLIF(pain_cl,0)),3), MEDIAN(pain_cl), ROUND(SUM(bdsi)) FROM j WHERE pain_cl>0 GROUP BY 1,2
ORDER BY 1,2;

-- Q18 addiction
-- Addiction: top 20 prescribers by money from the four makers, with their own brand claims (NPI join, last name checked against the addiction table)
WITH op AS (
  SELECT NPI, MIN(COVERED_RECIPIENT_LAST_NAME) op_last,
    SUM(TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS) maker_usd,
    SUM(IFF(NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE ILIKE '%speaker%' OR NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE ILIKE '%faculty%', TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS,0)) speaker_usd,
    LISTAGG(DISTINCT SPLIT_PART(APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME,',',1), '; ') makers
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_2022
  WHERE APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME ILIKE ANY ('%INDIVIOR%','%ALKERMES%','%OREXO%','%BIODELIVERY%','%COLLEGIUM%') AND NPI IS NOT NULL AND NPI <> ''
  GROUP BY 1),
pd AS (
  SELECT NPI, SUM(IFF(BRAND_NAME IN ('Suboxone','Sublocade'), TOTAL_CLAIMS,0)) indiv_cl, SUM(IFF(BRAND_NAME='Zubsolv', TOTAL_CLAIMS,0)) zub_cl,
    SUM(IFF(BRAND_NAME='Vivitrol', TOTAL_CLAIMS,0)) viv_cl, SUM(IFF(BRAND_NAME='Belbuca', TOTAL_CLAIMS,0)) belb_cl, SUM(TOTAL_CLAIMS) all_cl
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PARTD_PRESCRIBERS
  WHERE GENERIC_NAME ILIKE '%buprenorphine%' OR BRAND_NAME IN ('Naltrexone Hcl','Vivitrol') GROUP BY 1)
SELECT a.PRESCRIBER_NAME, a.PRESCRIBER_TYPE, a.STATE, op.op_last, ROUND(op.maker_usd) maker_usd, ROUND(op.speaker_usd) speaker_usd, op.makers,
  ROUND(a.TOTAL_PAYMENTS) all_pay, a.TOP_MANUFACTURER, a.ADDICTION_CLAIMS, ROUND(a.ADDICTION_DRUG_COST) addiction_cost,
  pd.indiv_cl, pd.zub_cl, pd.viv_cl, pd.belb_cl, pd.all_cl,
  (SELECT COUNT(*) FROM op) n_npis_paid_by_makers, (SELECT ROUND(SUM(maker_usd)) FROM op) all_maker_usd
FROM op JOIN LIBRARY_MARTS.HEALTH.HEALTH__ADDICTION_PRESCRIBERS_PAID a ON a.NPI=op.NPI LEFT JOIN pd ON pd.NPI=op.NPI
ORDER BY op.maker_usd DESC LIMIT 20;

-- Q19 clinical trials
-- Trials: FDAAA-shaped set = interventional, phase 2/3/4 (any list holding PHASE2/3/4), a US site, completed or terminated,
-- primary completion 2017-01-18 to 2022-06-30 (1-year deadline plus a 2-year delay cert has passed). Split by FDA-regulated flag and sponsor class.
WITH t AS (
  SELECT *, CASE WHEN IS_FDA_REGULATED_DRUG OR IS_FDA_REGULATED_DEVICE THEN 'fda_reg' WHEN IS_FDA_REGULATED_DRUG IS NULL AND IS_FDA_REGULATED_DEVICE IS NULL THEN 'flag_null' ELSE 'not_fda_reg' END fda
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CLINICALTRIALS
  WHERE STUDY_TYPE='INTERVENTIONAL' AND (PHASE ILIKE '%PHASE2%' OR PHASE ILIKE '%PHASE3%' OR PHASE ILIKE '%PHASE4%')
    AND LOCATIONS ILIKE '%"country": "United States"%' AND OVERALL_STATUS IN ('COMPLETED','TERMINATED')
    AND PRIMARY_COMPLETION_DATE BETWEEN '2017-01-18' AND '2022-06-30')
SELECT fda, LEAD_SPONSOR_CLASS, COUNT(*) trials, SUM(IFF(HAS_RESULTS,0,1)) no_results, ROUND(AVG(IFF(HAS_RESULTS,0,1)),3) share_none,
  SUM(IFF(HAS_RESULTS AND DATEDIFF('day',PRIMARY_COMPLETION_DATE,RESULTS_FIRST_POSTED_DATE)>365,1,0)) posted_late,
  SUM(IFF(NOT HAS_RESULTS AND ENROLLMENT<=1e6, ENROLLMENT,0)) enrolled_no_results, MAX(ENROLLMENT) max_enr,
  SUM(IFF(OVERALL_STATUS='TERMINATED',1,0)) terminated
FROM t GROUP BY ROLLUP(fda, LEAD_SPONSOR_CLASS) HAVING COUNT(*) >= 50 ORDER BY fda NULLS FIRST, trials DESC;

-- Q20 clinical trials
-- Trials: sponsors with 20+ FDA-regulated trials in that set, ranked by trials with no results posted (as of the 2026-09-04 snapshot)
WITH t AS (
  SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CLINICALTRIALS
  WHERE STUDY_TYPE='INTERVENTIONAL' AND (PHASE ILIKE '%PHASE2%' OR PHASE ILIKE '%PHASE3%' OR PHASE ILIKE '%PHASE4%')
    AND LOCATIONS ILIKE '%"country": "United States"%' AND OVERALL_STATUS IN ('COMPLETED','TERMINATED')
    AND PRIMARY_COMPLETION_DATE BETWEEN '2017-01-18' AND '2022-06-30' AND (IS_FDA_REGULATED_DRUG OR IS_FDA_REGULATED_DEVICE))
SELECT LEAD_SPONSOR_NAME, MIN(LEAD_SPONSOR_CLASS) cls, COUNT(*) trials, SUM(IFF(HAS_RESULTS,0,1)) no_results, ROUND(AVG(IFF(HAS_RESULTS,0,1)),3) share_none,
  SUM(IFF(NOT HAS_RESULTS AND ENROLLMENT<=1e6, ENROLLMENT,0)) enrolled_no_results,
  SUM(IFF(NOT HAS_RESULTS AND OVERALL_STATUS='TERMINATED',1,0)) none_terminated,
  SUM(IFF(NOT HAS_RESULTS AND PHASE ILIKE '%PHASE4%',1,0)) none_phase4
FROM t GROUP BY 1 HAVING COUNT(*) >= 20 ORDER BY no_results DESC LIMIT 30;

-- Q21 clinical trials
-- Trials: same FDA-regulated set, no size floor: who holds the most trials with no results posted, and when did they last touch the record?
WITH t AS (
  SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CLINICALTRIALS
  WHERE STUDY_TYPE='INTERVENTIONAL' AND (PHASE ILIKE '%PHASE2%' OR PHASE ILIKE '%PHASE3%' OR PHASE ILIKE '%PHASE4%')
    AND LOCATIONS ILIKE '%"country": "United States"%' AND OVERALL_STATUS IN ('COMPLETED','TERMINATED')
    AND PRIMARY_COMPLETION_DATE BETWEEN '2017-01-18' AND '2022-06-30' AND (IS_FDA_REGULATED_DRUG OR IS_FDA_REGULATED_DEVICE))
SELECT LEAD_SPONSOR_NAME, MIN(LEAD_SPONSOR_CLASS) cls, COUNT(*) trials, SUM(IFF(HAS_RESULTS,0,1)) no_results,
  SUM(IFF(NOT HAS_RESULTS AND ENROLLMENT<=1e6, ENROLLMENT,0)) enrolled_no_results,
  MAX(IFF(NOT HAS_RESULTS, LAST_UPDATE_POSTED_DATE, NULL)) last_touch_no_res,
  SUM(IFF(NOT HAS_RESULTS AND OVERALL_STATUS='TERMINATED',1,0)) none_terminated,
  (SELECT COUNT(DISTINCT LEAD_SPONSOR_NAME) FROM t WHERE NOT HAS_RESULTS) sponsors_with_any_missing,
  (SELECT COUNT(*) FROM (SELECT LEAD_SPONSOR_NAME FROM t WHERE NOT HAS_RESULTS GROUP BY 1 HAVING COUNT(*)=1)) sponsors_with_one_missing
FROM t GROUP BY 1 HAVING SUM(IFF(HAS_RESULTS,0,1)) >= 4 ORDER BY no_results DESC, enrolled_no_results DESC LIMIT 25;

-- Q22 dialysis
-- Dialysis: chain group vs peers. Raw patient-weighted rates, plus each clinic minus its own state's clinic mean (same-state peers).
-- Rates are CMS risk-adjusted (per 100 patient-years for death / hospital stays; ratios near 1 for infection, waitlist, home switch).
WITH c AS (
  SELECT CASE WHEN CHAIN_ORGANIZATION='DaVita' THEN '1 DaVita' WHEN CHAIN_ORGANIZATION='Fresenius Medical Care' THEN '2 Fresenius'
              WHEN CHAIN_ORGANIZATION='Independent' THEN IFF(PROFIT_OR_NON_PROFIT='Profit','5 Indep for-profit','6 Indep non-profit')
              ELSE IFF(PROFIT_OR_NON_PROFIT='Profit','3 Other chain for-profit','4 Other chain non-profit') END grp,
    STATE, FIVE_STAR, PATIENT_SURVIVAL_CATEGORY_TEXT surv_cat,
    TRY_TO_DOUBLE(MORTALITY_RATE_FACILITY::varchar) mort, TRY_TO_DOUBLE(NUMBER_OF_PATIENTS_INCLUDED_IN_SURVIVAL_SUMMARY::varchar) mort_n,
    TRY_TO_DOUBLE(HOSPITALIZATION_RATE_FACILITY::varchar) hosp, TRY_TO_DOUBLE(NUMBER_OF_PATIENTS_INCLUDED_IN_HOSPITALIZATION_SUMMARY::varchar) hosp_n,
    TRY_TO_DOUBLE(STANDARD_INFECTION_RATIO::varchar) sir,
    TRY_TO_DOUBLE(PERCENTAGE_OF_PREVALENT_PATIENTS_WAITLISTED_FOR_KIDNEY_TRANSPLANT::varchar) pppw,
    TRY_TO_DOUBLE(FIRST_YEAR_STANDARDIZED_KIDNEY_TRANSPLANT_WAITLIST_RATIO::varchar) fyswr,
    TRY_TO_DOUBLE(SMOSR_STANDARDIZED_MODALITY_SWITCH_RATIO_FACILITY::varchar) smosr,
    TRY_TO_DOUBLE(PERCENTAGE_OF_ADULT_PATIENTS_WITH_LONG_TERM_CATHETER_IN_USE::varchar) cath
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_DIALYSIS),
s AS (SELECT c.*, mort - AVG(mort) OVER (PARTITION BY STATE) d_mort, hosp - AVG(hosp) OVER (PARTITION BY STATE) d_hosp,
             pppw - AVG(pppw) OVER (PARTITION BY STATE) d_pppw, smosr - AVG(smosr) OVER (PARTITION BY STATE) d_smosr,
             FIVE_STAR - AVG(FIVE_STAR) OVER (PARTITION BY STATE) d_star
      FROM c)
SELECT grp, COUNT(*) clinics, COUNT(mort) n_mort, ROUND(SUM(mort*mort_n)/SUM(IFF(mort IS NULL,NULL,mort_n)),2) mort_w,
  ROUND(SUM(hosp*hosp_n)/SUM(IFF(hosp IS NULL,NULL,hosp_n)),1) hosp_w, ROUND(AVG(sir),2) sir,
  ROUND(AVG(IFF(FIVE_STAR<=2,1,0)),3) share_1_2_star, ROUND(AVG(FIVE_STAR),2) stars, SUM(IFF(FIVE_STAR IS NULL,1,0)) star_null,
  ROUND(AVG(IFF(surv_cat='Worse than Expected',1,0)),3) share_surv_worse, ROUND(AVG(IFF(surv_cat='Better than Expected',1,0)),3) share_surv_better,
  ROUND(AVG(pppw),1) pppw, ROUND(AVG(fyswr),2) fyswr, ROUND(AVG(smosr),2) smosr, ROUND(AVG(cath),1) cath,
  ROUND(AVG(d_mort),2) d_mort_vs_state, ROUND(AVG(d_hosp),1) d_hosp_vs_state, ROUND(AVG(d_pppw),1) d_pppw_vs_state, ROUND(AVG(d_smosr),2) d_smosr_vs_state, ROUND(AVG(d_star),2) d_star_vs_state,
  SUM(mort_n) patients_mort
FROM s GROUP BY ROLLUP(grp) ORDER BY grp NULLS LAST;

-- Q23 dialysis
-- Dialysis: name the independent for-profit clinics CMS rates Worse than Expected on survival; with each state's count of such clinics
WITH c AS (
  SELECT CCN, FACILITY_NAME, CITY_TOWN, STATE, FIVE_STAR, PATIENT_SURVIVAL_CATEGORY_TEXT surv_cat, PATIENT_HOSPITALIZATION_CATEGORY_TEXT hosp_cat,
    TRY_TO_DOUBLE(MORTALITY_RATE_FACILITY::varchar) mort, TRY_TO_DOUBLE(NUMBER_OF_PATIENTS_INCLUDED_IN_SURVIVAL_SUMMARY::varchar) mort_n,
    TRY_TO_DOUBLE(HOSPITALIZATION_RATE_FACILITY::varchar) hosp, OF_DIALYSIS_STATIONS, CERTIFICATION_DATE,
    CHAIN_ORGANIZATION, PROFIT_OR_NON_PROFIT
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_DIALYSIS),
w AS (SELECT *, COUNT_IF(surv_cat='Worse than Expected') OVER (PARTITION BY STATE) state_worse_all,
             COUNT_IF(CHAIN_ORGANIZATION='Independent' AND PROFIT_OR_NON_PROFIT='Profit') OVER (PARTITION BY STATE) state_indfp,
             COUNT_IF(CHAIN_ORGANIZATION='Independent' AND PROFIT_OR_NON_PROFIT='Profit' AND surv_cat='Worse than Expected') OVER (PARTITION BY STATE) state_indfp_worse,
             COUNT(*) OVER (PARTITION BY STATE) state_all
      FROM c)
SELECT CCN, FACILITY_NAME, CITY_TOWN, STATE, FIVE_STAR, mort, hosp, hosp_cat, mort_n, OF_DIALYSIS_STATIONS stations, CERTIFICATION_DATE,
  state_all, state_indfp, state_indfp_worse, state_worse_all
FROM w WHERE CHAIN_ORGANIZATION='Independent' AND PROFIT_OR_NON_PROFIT='Profit' AND surv_cat='Worse than Expected'
ORDER BY state_indfp_worse DESC, STATE, mort DESC;

-- Q24 HCRIS
-- HCRIS: by fiscal year: reports, S-10 fill, sums, impossible rows (bad debt or charity above total costs), biggest bad-debt filer,
-- and the median charity share of total costs for short-term hospitals (the trend peers get compared to)
SELECT YEAR(FISCAL_YEAR_END_DATE) fy, COUNT(*) rpts, COUNT(DISTINCT PROVIDER_CCN) ccns,
  SUM(IFF(COST_OF_CHARITY_CARE IS NOT NULL,1,0)) cc_n, ROUND(SUM(COST_OF_CHARITY_CARE)/1e9,1) cc_b, ROUND(SUM(TOTAL_BAD_DEBT_EXPENSE)/1e9,1) bd_b,
  SUM(IFF(TOTAL_BAD_DEBT_EXPENSE > TOTAL_COSTS,1,0)) bd_gt_costs, SUM(IFF(COST_OF_CHARITY_CARE > TOTAL_COSTS,1,0)) cc_gt_costs,
  ROUND(MAX(TOTAL_BAD_DEBT_EXPENSE)/1e9,2) max_bd_b, MAX_BY(HOSPITAL_NAME, TOTAL_BAD_DEBT_EXPENSE) max_bd_name, MAX_BY(PROVIDER_CCN, TOTAL_BAD_DEBT_EXPENSE) max_bd_ccn,
  ROUND(MEDIAN(IFF(CCN_FACILITY_TYPE='STH' AND TOTAL_COSTS>0, COST_OF_CHARITY_CARE/TOTAL_COSTS, NULL)),4) sth_med_cc_share,
  ROUND(MEDIAN(IFF(CCN_FACILITY_TYPE='STH' AND TOTAL_COSTS>0, TOTAL_BAD_DEBT_EXPENSE*COST_TO_CHARGE_RATIO/TOTAL_COSTS, NULL)),4) sth_med_bdcost_share
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS GROUP BY 1 ORDER BY 1;

-- Q25 HCRIS
-- HCRIS: FY2022, latest report per short-term hospital: bad debt vs charity by ownership type (peers)
WITH r AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY PROVIDER_CCN ORDER BY FISCAL_YEAR_END_DATE DESC, RPT_REC_NUM DESC) rn
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS WHERE YEAR(FISCAL_YEAR_END_DATE)=2022 AND CCN_FACILITY_TYPE='STH'),
x AS (SELECT *, CASE WHEN TRY_TO_NUMBER(TYPE_OF_CONTROL::varchar) IN (1,2) THEN 'nonprofit' WHEN TRY_TO_NUMBER(TYPE_OF_CONTROL::varchar) BETWEEN 3 AND 6 THEN 'for-profit'
                     WHEN TRY_TO_NUMBER(TYPE_OF_CONTROL::varchar) BETWEEN 7 AND 13 THEN 'government' ELSE 'other' END ctl,
        TOTAL_BAD_DEBT_EXPENSE*COST_TO_CHARGE_RATIO bd_cost FROM r WHERE rn=1)
SELECT ctl, COUNT(*) hospitals, SUM(IFF(COST_OF_CHARITY_CARE IS NULL,1,0)) cc_null, SUM(IFF(TOTAL_BAD_DEBT_EXPENSE IS NULL,1,0)) bd_null,
  ROUND(MEDIAN(COST_OF_CHARITY_CARE/NULLIF(TOTAL_COSTS,0)),4) med_cc_share, ROUND(MEDIAN(bd_cost/NULLIF(TOTAL_COSTS,0)),4) med_bdcost_share,
  ROUND(MEDIAN(TOTAL_BAD_DEBT_EXPENSE/NULLIF(COST_OF_CHARITY_CARE,0)),2) med_bd_to_cc_raw, ROUND(MEDIAN(bd_cost/NULLIF(COST_OF_CHARITY_CARE,0)),2) med_bdcost_to_cc,
  ROUND(SUM(COST_OF_CHARITY_CARE)/1e9,2) cc_b, ROUND(SUM(bd_cost)/1e9,2) bdcost_b, ROUND(SUM(TOTAL_COSTS)/1e9,1) costs_b,
  SUM(IFF(bd_cost > 20e6 AND bd_cost > 5*COALESCE(COST_OF_CHARITY_CARE,0),1,0)) n_bdcost20m_5x_cc
FROM x GROUP BY ROLLUP(ctl) ORDER BY ctl NULLS LAST;

-- Q26 HCRIS
-- HCRIS: FY2022 short-term hospitals with bad debt at cost over $20M, ranked by bad debt at cost / charity care cost; current enrolled owner by CCN
WITH r AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY PROVIDER_CCN ORDER BY FISCAL_YEAR_END_DATE DESC, RPT_REC_NUM DESC) rn
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS WHERE YEAR(FISCAL_YEAR_END_DATE)=2022 AND CCN_FACILITY_TYPE='STH'),
e AS (SELECT CCN, MIN(ORGANIZATION_NAME) org, MIN(PROPRIETARY_NONPROFIT) pn, COUNT(*) n_enr FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS GROUP BY 1)
SELECT r.PROVIDER_CCN, r.HOSPITAL_NAME, r.STATE_CODE, r.TYPE_OF_CONTROL, ROUND(r.TOTAL_BAD_DEBT_EXPENSE/1e6,1) bd_m, ROUND(r.COST_TO_CHARGE_RATIO,3) ccr,
  ROUND(r.TOTAL_BAD_DEBT_EXPENSE*r.COST_TO_CHARGE_RATIO/1e6,1) bdcost_m, ROUND(r.COST_OF_CHARITY_CARE/1e6,2) cc_m,
  ROUND(r.TOTAL_BAD_DEBT_EXPENSE*r.COST_TO_CHARGE_RATIO/NULLIF(r.COST_OF_CHARITY_CARE,0),1) ratio, ROUND(r.TOTAL_COSTS/1e6) costs_m,
  ROUND(r.NET_INCOME/1e6,1) net_income_m, e.org enrolled_org, e.pn
FROM r LEFT JOIN e ON e.CCN=r.PROVIDER_CCN
WHERE r.rn=1 AND r.TOTAL_BAD_DEBT_EXPENSE*r.COST_TO_CHARGE_RATIO > 20e6
ORDER BY r.TOTAL_BAD_DEBT_EXPENSE*r.COST_TO_CHARGE_RATIO/NULLIF(r.COST_OF_CHARITY_CARE,0) DESC NULLS FIRST LIMIT 25;

-- Q27 HCRIS
-- HCRIS: short-term hospitals that flip from nonprofit or government control to for-profit (TYPE_OF_CONTROL 3-6) between two back-to-back
-- fiscal years, stay for-profit the next 2 years, and were the old type the 2 years before. Charity care share of total costs (percent),
-- 2 years before vs 2 years after. Peers = median share of every short-term hospital that never changed type, same years.
-- Reports inside one CCN-year are summed. Current enrolled owner by CCN from HOSPITAL_ENROLLMENTS.
WITH y AS (
  SELECT PROVIDER_CCN ccn, YEAR(FISCAL_YEAR_END_DATE) fy, MAX_BY(TRY_TO_NUMBER(TYPE_OF_CONTROL::varchar), FISCAL_YEAR_END_DATE) ctl_code,
    MAX_BY(HOSPITAL_NAME, FISCAL_YEAR_END_DATE) name, MAX_BY(STATE_CODE, FISCAL_YEAR_END_DATE) st, COUNT(*) n_rpts,
    SUM(COST_OF_CHARITY_CARE) cc, SUM(TOTAL_COSTS) tc
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS WHERE CCN_FACILITY_TYPE='STH' GROUP BY 1,2),
yc AS (SELECT *, CASE WHEN ctl_code IN (1,2) THEN 'NP' WHEN ctl_code BETWEEN 3 AND 6 THEN 'FP' WHEN ctl_code BETWEEN 7 AND 13 THEN 'GOV' END cat,
         100*cc/NULLIF(tc,0) pct FROM y),
stable AS (SELECT ccn FROM yc GROUP BY 1 HAVING COUNT(DISTINCT cat)=1),
peer_y AS (SELECT fy, MEDIAN(pct) med FROM yc WHERE ccn IN (SELECT ccn FROM stable) GROUP BY 1),
lagged AS (SELECT *, LAG(cat) OVER (PARTITION BY ccn ORDER BY fy) prev_cat, LAG(fy) OVER (PARTITION BY ccn ORDER BY fy) prev_fy FROM yc),
conv AS (SELECT ccn, fy conv_fy, prev_cat FROM lagged WHERE cat='FP' AND prev_cat IN ('NP','GOV') AND fy-prev_fy=1),
win AS (SELECT c.ccn, c.conv_fy, c.prev_cat,
    AVG(IFF(y.fy BETWEEN c.conv_fy-2 AND c.conv_fy-1, y.pct, NULL)) before_pct, AVG(IFF(y.fy BETWEEN c.conv_fy+1 AND c.conv_fy+2, y.pct, NULL)) after_pct,
    SUM(IFF(y.fy BETWEEN c.conv_fy-2 AND c.conv_fy-1, y.cc, 0))/2 before_cc_yr, SUM(IFF(y.fy BETWEEN c.conv_fy+1 AND c.conv_fy+2, y.cc, 0))/2 after_cc_yr,
    COUNT_IF(y.fy BETWEEN c.conv_fy+1 AND c.conv_fy+2 AND y.cat='FP') after_fp, COUNT_IF(y.fy BETWEEN c.conv_fy-2 AND c.conv_fy-1 AND y.cat=c.prev_cat) before_same,
    MAX(IFF(y.fy=c.conv_fy, y.n_rpts, NULL)) conv_rpts, MAX_BY(y.name, y.fy) name, MAX_BY(y.st, y.fy) st,
    MAX(IFF(y.fy=c.conv_fy-1, y.ctl_code, NULL)) ctl_before, MAX(IFF(y.fy=c.conv_fy, y.ctl_code, NULL)) ctl_after
  FROM conv c JOIN yc y ON y.ccn=c.ccn GROUP BY 1,2,3),
k AS (SELECT w.*, (SELECT AVG(med) FROM peer_y p WHERE p.fy BETWEEN w.conv_fy-2 AND w.conv_fy-1) peer_before,
                  (SELECT AVG(med) FROM peer_y p WHERE p.fy BETWEEN w.conv_fy+1 AND w.conv_fy+2) peer_after
      FROM win w WHERE after_fp=2 AND before_same=2 AND before_pct IS NOT NULL AND after_pct IS NOT NULL),
e AS (SELECT CCN, MIN(ORGANIZATION_NAME) org FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS GROUP BY 1)
SELECT k.ccn, k.name, k.st, k.conv_fy, k.prev_cat, k.ctl_before, k.ctl_after, k.conv_rpts, ROUND(k.before_pct,2) before_pct, ROUND(k.after_pct,2) after_pct,
  ROUND(k.before_cc_yr/1e6,2) before_cc_m_yr, ROUND(k.after_cc_yr/1e6,2) after_cc_m_yr, e.org enrolled_org_now,
  (SELECT COUNT(*) FROM win) n_flips_raw, (SELECT COUNT(*) FROM k) n_clean,
  (SELECT ROUND(MEDIAN(before_pct),2) FROM k) med_before, (SELECT ROUND(MEDIAN(after_pct),2) FROM k) med_after,
  (SELECT ROUND(MEDIAN(after_pct-before_pct),2) FROM k) med_change, (SELECT ROUND(MEDIAN(peer_after-peer_before),3) FROM k) peer_change,
  (SELECT COUNT_IF(after_pct < before_pct) FROM k) n_down, (SELECT ROUND(SUM(before_cc_yr-after_cc_yr)/1e6,1) FROM k) total_drop_m_yr
FROM k LEFT JOIN e ON e.CCN=k.ccn
ORDER BY (k.before_cc_yr-k.after_cc_yr) DESC LIMIT 25;

-- Q28 HCRIS + dialysis
-- HCRIS: same clean for-profit conversions, split by who holds the enrollment today (Prime Healthcare vs Prospect vs everyone else)
WITH y AS (
  SELECT PROVIDER_CCN ccn, YEAR(FISCAL_YEAR_END_DATE) fy, MAX_BY(TRY_TO_NUMBER(TYPE_OF_CONTROL::varchar), FISCAL_YEAR_END_DATE) ctl_code,
    SUM(COST_OF_CHARITY_CARE) cc, SUM(TOTAL_COSTS) tc
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS WHERE CCN_FACILITY_TYPE='STH' GROUP BY 1,2),
yc AS (SELECT *, CASE WHEN ctl_code IN (1,2) THEN 'NP' WHEN ctl_code BETWEEN 3 AND 6 THEN 'FP' WHEN ctl_code BETWEEN 7 AND 13 THEN 'GOV' END cat, 100*cc/NULLIF(tc,0) pct FROM y),
lagged AS (SELECT *, LAG(cat) OVER (PARTITION BY ccn ORDER BY fy) prev_cat, LAG(fy) OVER (PARTITION BY ccn ORDER BY fy) prev_fy FROM yc),
conv AS (SELECT ccn, fy conv_fy, prev_cat FROM lagged WHERE cat='FP' AND prev_cat IN ('NP','GOV') AND fy-prev_fy=1),
win AS (SELECT c.ccn, c.conv_fy,
    AVG(IFF(y.fy BETWEEN c.conv_fy-2 AND c.conv_fy-1, y.pct, NULL)) b, AVG(IFF(y.fy BETWEEN c.conv_fy+1 AND c.conv_fy+2, y.pct, NULL)) a,
    SUM(IFF(y.fy BETWEEN c.conv_fy-2 AND c.conv_fy-1, y.cc, 0))/2 bcc, SUM(IFF(y.fy BETWEEN c.conv_fy+1 AND c.conv_fy+2, y.cc, 0))/2 acc,
    COUNT_IF(y.fy BETWEEN c.conv_fy+1 AND c.conv_fy+2 AND y.cat='FP') after_fp, COUNT_IF(y.fy BETWEEN c.conv_fy-2 AND c.conv_fy-1 AND y.cat=c.prev_cat) before_same
  FROM conv c JOIN yc y ON y.ccn=c.ccn GROUP BY 1,2),
e AS (SELECT CCN, MIN(ORGANIZATION_NAME) org FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS GROUP BY 1),
k AS (SELECT w.*, CASE WHEN e.org ILIKE '%PRIME HEALTHCARE%' THEN 'Prime Healthcare' WHEN e.org ILIKE '%PROSPECT%' THEN 'Prospect' WHEN e.org IS NULL THEN 'no enrollment match' ELSE 'other buyers' END buyer
      FROM win w LEFT JOIN e ON e.CCN=w.ccn WHERE after_fp=2 AND before_same=2 AND b IS NOT NULL AND a IS NOT NULL)
SELECT buyer, COUNT(*) hospitals, ROUND(MEDIAN(b),2) med_before_pct, ROUND(MEDIAN(a),2) med_after_pct, ROUND(MEDIAN(a-b),2) med_change_pp,
  COUNT_IF(a<b) n_down, ROUND(SUM(bcc)/1e6,1) before_m_yr, ROUND(SUM(acc)/1e6,1) after_m_yr, MIN(conv_fy) fy0, MAX(conv_fy) fy1
FROM k GROUP BY ROLLUP(buyer) ORDER BY hospitals DESC;

-- Q29 HCRIS + dialysis
-- Dialysis: nursing-home dialysis brands (names hold Dialyze Direct, Dialysis Direct, Concerto, Home Dialysis Services) vs the rest of the independent for-profits
SELECT CASE WHEN FACILITY_NAME ILIKE ANY ('%DIALYZE DIRECT%','%DIALYSIS DIRECT%','%CONCERTO%','%HOME DIALYSIS SERVICES%') THEN 'NH dialysis brand'
            WHEN CHAIN_ORGANIZATION='Independent' AND PROFIT_OR_NON_PROFIT='Profit' THEN 'other indep for-profit'
            ELSE 'everyone else' END grp,
  COUNT(*) clinics, LISTAGG(DISTINCT CHAIN_ORGANIZATION, '; ') chain_labels, COUNT(DISTINCT STATE) states,
  COUNT_IF(PATIENT_SURVIVAL_CATEGORY_TEXT='Worse than Expected') n_worse, ROUND(AVG(IFF(PATIENT_SURVIVAL_CATEGORY_TEXT='Worse than Expected',1,0)),3) share_worse,
  COUNT_IF(PATIENT_SURVIVAL_CATEGORY_TEXT IN ('As Expected','Better than Expected','Worse than Expected')) n_rated,
  ROUND(SUM(TRY_TO_DOUBLE(MORTALITY_RATE_FACILITY::varchar)*TRY_TO_DOUBLE(NUMBER_OF_PATIENTS_INCLUDED_IN_SURVIVAL_SUMMARY::varchar))
       /SUM(IFF(TRY_TO_DOUBLE(MORTALITY_RATE_FACILITY::varchar) IS NULL,NULL,TRY_TO_DOUBLE(NUMBER_OF_PATIENTS_INCLUDED_IN_SURVIVAL_SUMMARY::varchar))),2) mort_w,
  ROUND(MEDIAN(OF_DIALYSIS_STATIONS),1) med_stations, SUM(TRY_TO_DOUBLE(NUMBER_OF_PATIENTS_INCLUDED_IN_SURVIVAL_SUMMARY::varchar)) patients
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_DIALYSIS GROUP BY 1 ORDER BY 1;

-- Q30 HCRIS
-- HCRIS: same clean conversions, now net of the SAME-STATE trend (median charity share of short-term hospitals in that state that never
-- changed ownership type, same before/after years). Rows: each Prime / Prospect hospital, plus one summary row per buyer group.
WITH y AS (
  SELECT PROVIDER_CCN ccn, YEAR(FISCAL_YEAR_END_DATE) fy, MAX_BY(TRY_TO_NUMBER(TYPE_OF_CONTROL::varchar), FISCAL_YEAR_END_DATE) ctl_code,
    MAX_BY(STATE_CODE, FISCAL_YEAR_END_DATE) st, MAX_BY(HOSPITAL_NAME, FISCAL_YEAR_END_DATE) name, SUM(COST_OF_CHARITY_CARE) cc, SUM(TOTAL_COSTS) tc
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS WHERE CCN_FACILITY_TYPE='STH' GROUP BY 1,2),
yc AS (SELECT *, CASE WHEN ctl_code IN (1,2) THEN 'NP' WHEN ctl_code BETWEEN 3 AND 6 THEN 'FP' WHEN ctl_code BETWEEN 7 AND 13 THEN 'GOV' END cat, 100*cc/NULLIF(tc,0) pct FROM y),
stable AS (SELECT ccn FROM yc GROUP BY 1 HAVING COUNT(DISTINCT cat)=1),
sp AS (SELECT st, fy, MEDIAN(pct) med FROM yc WHERE ccn IN (SELECT ccn FROM stable) GROUP BY 1,2),
lagged AS (SELECT *, LAG(cat) OVER (PARTITION BY ccn ORDER BY fy) prev_cat, LAG(fy) OVER (PARTITION BY ccn ORDER BY fy) prev_fy FROM yc),
conv AS (SELECT ccn, fy conv_fy, prev_cat, st FROM lagged WHERE cat='FP' AND prev_cat IN ('NP','GOV') AND fy-prev_fy=1),
win AS (SELECT c.ccn, c.conv_fy, c.st, MAX_BY(y.name, y.fy) name,
    AVG(IFF(y.fy BETWEEN c.conv_fy-2 AND c.conv_fy-1, y.pct, NULL)) b, AVG(IFF(y.fy BETWEEN c.conv_fy+1 AND c.conv_fy+2, y.pct, NULL)) a,
    SUM(IFF(y.fy BETWEEN c.conv_fy-2 AND c.conv_fy-1, y.cc, 0))/2 bcc, SUM(IFF(y.fy BETWEEN c.conv_fy+1 AND c.conv_fy+2, y.cc, 0))/2 acc,
    COUNT_IF(y.fy BETWEEN c.conv_fy+1 AND c.conv_fy+2 AND y.cat='FP') after_fp, COUNT_IF(y.fy BETWEEN c.conv_fy-2 AND c.conv_fy-1 AND y.cat=c.prev_cat) before_same
  FROM conv c JOIN yc y ON y.ccn=c.ccn GROUP BY 1,2,3),
e AS (SELECT CCN, MIN(ORGANIZATION_NAME) org FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS GROUP BY 1),
k AS (SELECT w.*, CASE WHEN e.org ILIKE '%PRIME HEALTHCARE%' THEN 'Prime Healthcare' WHEN e.org ILIKE '%PROSPECT%' THEN 'Prospect' WHEN e.org IS NULL THEN 'no enrollment match' ELSE 'other buyers' END buyer,
        (SELECT AVG(med) FROM sp WHERE sp.st=w.st AND sp.fy BETWEEN w.conv_fy-2 AND w.conv_fy-1) pb,
        (SELECT AVG(med) FROM sp WHERE sp.st=w.st AND sp.fy BETWEEN w.conv_fy+1 AND w.conv_fy+2) pa
      FROM win w LEFT JOIN e ON e.CCN=w.ccn WHERE after_fp=2 AND before_same=2 AND b IS NOT NULL AND a IS NOT NULL),
kk AS (SELECT *, (a-b) chg, (pa-pb) state_chg, (a-b)-(pa-pb) net FROM k)
SELECT buyer, name, st, conv_fy::varchar fy, ROUND(b,2) before_pct, ROUND(a,2) after_pct, ROUND(chg,2) chg_pp, ROUND(state_chg,2) state_chg_pp, ROUND(net,2) net_pp,
  ROUND(bcc/1e6,2) before_m_yr, ROUND(acc/1e6,2) after_m_yr, 1 n
FROM kk WHERE buyer IN ('Prime Healthcare','Prospect')
UNION ALL
SELECT buyer, 'ALL (medians)', NULL, MIN(conv_fy)||'-'||MAX(conv_fy), ROUND(MEDIAN(b),2), ROUND(MEDIAN(a),2), ROUND(MEDIAN(chg),2), ROUND(MEDIAN(state_chg),2), ROUND(MEDIAN(net),2),
  ROUND(SUM(bcc)/1e6,1), ROUND(SUM(acc)/1e6,1), COUNT(*)
FROM kk GROUP BY buyer
ORDER BY 1, 2;

-- NOTE on Q13: Snowflake regex has no \b word boundary, so the suffix strip did nothing; issuer and recall firm matched on the
-- full upper-cased name (INC etc. kept). 25 issuers matched. Q14 split flag proved useless (flags Unity/Snowflake, misses Tesla/Walmart).
-- Total: 30 SQL statements (Q1-Q30), plus 2 ALTER SESSION lines per connection (13 connections).
