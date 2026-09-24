-- deep-7: coverage deep pass, 2026-09-24. Read-only. Python door, QUERY_TAG coverage-b-2026-09-24.
-- Each statement ran after ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300 and QUERY_TAG.

-- [1] counts_all_five
SELECT 'RELIEF' t, COUNT(*) n FROM LIBRARY_MARTS.HEALTH.HEALTH__NURSING_HOME_RELIEF_BY_CHAIN
UNION ALL SELECT 'MEAL', COUNT(*) FROM LIBRARY_MARTS.HEALTH.HEALTH__PHARMA_MEAL_CAP_FINGERPRINT
UNION ALL SELECT 'HOSPICE', COUNT(*) FROM LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS
UNION ALL SELECT 'AGREEMENTS', COUNT(*) FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DISCLOSURE_AGREEMENTS
UNION ALL SELECT 'DEBTS', COUNT(*) FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DISCLOSURE_DEBTS;

-- [2] sample_relief
SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__NURSING_HOME_RELIEF_BY_CHAIN LIMIT 5;

-- [3] sample_meal
SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__PHARMA_MEAL_CAP_FINGERPRINT LIMIT 5;

-- [4] sample_hospice
SELECT * FROM LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS LIMIT 5;

-- [5] sample_agreements
SELECT * FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DISCLOSURE_AGREEMENTS LIMIT 5;

-- [6] sample_debts
SELECT * FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DISCLOSURE_DEBTS LIMIT 5;

-- [7] relief_bands_by_rating_fines_and_relief_decile
WITH c AS (
  SELECT r.*,
    TOTAL_CERTIFIED_BEDS / NULLIF(HOMES_IN_ROSTER, 0) AS beds_per_home,
    MATCHED_RELIEF_DOLLARS - PAYEE_SHORTER_DOLLARS AS strict_dollars,
    MATCHED_HOMES - PAYEE_SHORTER_HOMES AS strict_homes,
    CASE WHEN CHAIN_AVG_OVERALL_RATING < 2.5 THEN 'r1 stars <2.5'
         WHEN CHAIN_AVG_OVERALL_RATING < 3.0 THEN 'r2 stars 2.5-3'
         WHEN CHAIN_AVG_OVERALL_RATING < 3.5 THEN 'r3 stars 3-3.5'
         WHEN CHAIN_AVG_OVERALL_RATING >= 3.5 THEN 'r4 stars 3.5+'
         ELSE 'r5 unrated' END AS rating_band,
    'f' || NTILE(4) OVER (ORDER BY FINES_PER_BED) || ' fines/bed quartile' AS fines_band,
    IFF(NTILE(10) OVER (ORDER BY MATCHED_RELIEF_DOLLARS / NULLIF(TOTAL_CERTIFIED_BEDS, 0)) = 10, 'd10 top relief-per-bed decile', 'd1-9 rest') AS relief_band
  FROM LIBRARY_MARTS.HEALTH.HEALTH__NURSING_HOME_RELIEF_BY_CHAIN r
),
u AS (
  SELECT rating_band AS grp, * FROM c UNION ALL
  SELECT fines_band, * FROM c UNION ALL
  SELECT relief_band, * FROM c
)
SELECT grp, COUNT(*) chains, SUM(HOMES_IN_ROSTER) homes, SUM(TOTAL_CERTIFIED_BEDS) beds,
  COUNT_IF(MATCHED_HOMES = 0) zero_match_chains,
  ROUND(SUM(MATCHED_HOMES) / SUM(HOMES_IN_ROSTER), 3) home_match_share,
  ROUND(SUM(MATCHED_RELIEF_DOLLARS) / 1e6, 1) matched_musd,
  ROUND(SUM(MATCHED_RELIEF_DOLLARS) / NULLIF(SUM(TOTAL_CERTIFIED_BEDS), 0)) floor_per_bed_all_beds,
  ROUND(SUM(MATCHED_RELIEF_DOLLARS) / NULLIF(SUM(MATCHED_HOMES * beds_per_home), 0)) per_matched_bed_est,
  ROUND(SUM(strict_dollars) / NULLIF(SUM(strict_homes * beds_per_home), 0)) strict_per_matched_bed_est,
  ROUND(SUM(TOTAL_FINES_DOLLARS) / NULLIF(SUM(TOTAL_CERTIFIED_BEDS), 0)) fines_per_bed,
  ROUND(SUM(ABUSE_ICON_HOMES) / SUM(HOMES_IN_ROSTER), 3) abuse_share,
  ROUND(SUM(ONE_STAR_HOMES) / SUM(HOMES_IN_ROSTER), 3) one_star_share,
  ROUND(AVG(CHAIN_AVG_OVERALL_RATING), 2) avg_stars
FROM u GROUP BY 1 ORDER BY 1;

-- [8] relief_top_chains_by_dollars
SELECT CHAIN_NAME, HOMES_IN_ROSTER, MATCHED_HOMES, MATCHED_HOME_SHARE, ROUND(MATCHED_RELIEF_DOLLARS/1e6,1) musd,
  ROUND(EXACT_MATCH_DOLLARS/1e6,1) exact_musd, ROUND(PAYEE_SHORTER_DOLLARS/1e6,1) payee_shorter_musd, ROUND(PRF_CONTAINS_HOME_DOLLARS/1e6,1) contains_musd,
  ROUND(RELIEF_PER_MATCHED_HOME) per_matched_home, ROUND(TOTAL_CERTIFIED_BEDS/HOMES_IN_ROSTER) beds_per_home,
  CHAIN_AVG_OVERALL_RATING stars, FINES_PER_BED, ROUND(ABUSE_ICON_HOMES/HOMES_IN_ROSTER,2) abuse_share, ONE_STAR_HOMES
FROM LIBRARY_MARTS.HEALTH.HEALTH__NURSING_HOME_RELIEF_BY_CHAIN
ORDER BY MATCHED_RELIEF_DOLLARS DESC LIMIT 15;

-- [9] meal_industry_by_year
SELECT PROGRAM_YEAR, COUNT(*) makers, SUM(TOTAL_FB_PAYMENTS) meals, ROUND(SUM(TOTAL_FB_AMOUNT_USD)/1e6,1) musd,
  SUM(N_MEAL_CAP) n_124_00_to_124_99, SUM(N_EXACTLY_124_99) n_124_99, SUM(N_EXACTLY_125_00) n_125_00, SUM(N_JUST_ABOVE) n_125_01_to_126_00,
  ROUND(SUM(N_MEAL_CAP)/NULLIF(SUM(N_JUST_ABOVE),0),2) cliff, COUNT_IF(IS_PRONOUNCED_FINGERPRINT) pronounced_rows,
  COUNT_IF(TOTAL_FB_PAYMENTS >= 1000) makers_1000plus
FROM LIBRARY_MARTS.HEALTH.HEALTH__PHARMA_MEAL_CAP_FINGERPRINT GROUP BY 1 ORDER BY 1;

-- [10] meal_makers_ranked_1000plus
WITH m AS (
  SELECT PAYMENT_MAKER_NAME, COUNT(*) yrs, LISTAGG(PROGRAM_YEAR, ',') WITHIN GROUP (ORDER BY PROGRAM_YEAR) years,
    SUM(TOTAL_FB_PAYMENTS) meals, SUM(N_MEAL_CAP) cap, SUM(N_JUST_ABOVE) above, SUM(N_EXACTLY_124_99) n12499, SUM(N_EXACTLY_125_00) n12500,
    COUNT_IF(IS_PRONOUNCED_FINGERPRINT) yrs_pronounced, ROUND(AVG(MEDIAN_FB_AMOUNT_USD),1) med_amt
  FROM LIBRARY_MARTS.HEALTH.HEALTH__PHARMA_MEAL_CAP_FINGERPRINT GROUP BY 1 HAVING SUM(TOTAL_FB_PAYMENTS) >= 3000
)
SELECT PAYMENT_MAKER_NAME, years, meals, med_amt, cap, above, n12499, n12500,
  ROUND(cap/meals*1000,1) cap_per_1000_meals, ROUND(cap/NULLIF(above,0),1) cliff, yrs_pronounced,
  RANK() OVER (ORDER BY cap/meals DESC) rank_cap_share, RANK() OVER (ORDER BY meals DESC) rank_meals,
  COUNT(*) OVER () makers_in_pool,
  ROUND(MEDIAN(cap/meals*1000) OVER (), 2) pool_median_cap_per_1000
FROM m
QUALIFY rank_cap_share <= 20 OR PAYMENT_MAKER_NAME ILIKE ANY ('abbvie%', 'novo nordisk%', 'astrazeneca%', 'pfizer%', 'eli lilly%', 'boehringer%', 'janssen%')
ORDER BY rank_cap_share;

-- [11] hospice_npis_with_many_enrollments
WITH n AS (
  SELECT NPI, COUNT(*) enrollments, COUNT(DISTINCT CCN) ccns, COUNT(DISTINCT ENROLLMENT_STATE) states,
    COUNT(DISTINCT ORGANIZATION_NAME) orgs, COUNT(DISTINCT ADDRESS_LINE_1 || ZIP_CODE) addresses,
    COUNT(DISTINCT ASSOCIATE_ID) associate_ids, MIN(ORGANIZATION_NAME) org_example, MAX(DOING_BUSINESS_AS_NAME) dba_example,
    LISTAGG(DISTINCT MULTIPLE_NPI_FLAG, ',') npi_flag, MIN(ENROLLMENT_STATE) st_example, MIN(CITY) city_example
  FROM LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS GROUP BY NPI
)
SELECT *, COUNT_IF(enrollments > 1) OVER () npis_with_2plus, SUM(enrollments) OVER () all_rows, COUNT(*) OVER () distinct_npis
FROM n ORDER BY enrollments DESC LIMIT 12;

-- [12] hospice_metro_peers
WITH h AS (
  SELECT *, LEFT(REGEXP_REPLACE(ZIP_CODE, '[^0-9]', ''), 5) zip5, TRY_TO_NUMBER(LEFT(REGEXP_REPLACE(ZIP_CODE, '[^0-9]', ''), 3)) z3,
    UPPER(REGEXP_REPLACE(TRIM(ADDRESS_LINE_1), '\\s+', ' ')) addr
  FROM LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS
),
a AS (SELECT addr, zip5, COUNT(*) n_at_addr FROM h GROUP BY 1, 2),
g AS (
  SELECT h.*, a.n_at_addr,
    CASE WHEN z3 BETWEEN 900 AND 918 OR z3 = 935 THEN 'LA County (zip3 900-918,935)'
         WHEN z3 BETWEEN 770 AND 775 THEN 'Houston (770-775)'
         WHEN z3 BETWEEN 750 AND 753 THEN 'Dallas (750-753)'
         WHEN z3 BETWEEN 850 AND 853 THEN 'Phoenix (850-853)'
         WHEN z3 BETWEEN 889 AND 891 THEN 'Las Vegas (889-891)'
         WHEN z3 BETWEEN 919 AND 921 THEN 'San Diego (919-921)'
         WHEN z3 BETWEEN 600 AND 608 THEN 'Chicago (600-608)'
         WHEN z3 BETWEEN 330 AND 332 THEN 'Miami (330-332)'
         WHEN z3 BETWEEN 300 AND 303 THEN 'Atlanta (300-303)'
         WHEN ENROLLMENT_STATE = 'CA' THEN 'CA outside LA/SD'
         ELSE 'rest of US' END metro
  FROM h JOIN a ON a.addr = h.addr AND a.zip5 = h.zip5
)
SELECT metro, COUNT(*) enrollments,
  COUNT_IF(INCORPORATION_DATE IS NOT NULL) inc_filled,
  COUNT_IF(INCORPORATION_DATE >= '2019-01-01') inc_2019_plus,
  ROUND(COUNT_IF(INCORPORATION_DATE >= '2019-01-01') / NULLIF(COUNT_IF(INCORPORATION_DATE IS NOT NULL), 0), 3) share_inc_2019_plus,
  COUNT_IF(ENROLLMENT_ID >= 'O2019') enrolled_2019_plus_by_id,
  COUNT_IF(n_at_addr >= 2) at_shared_addr, COUNT_IF(n_at_addr >= 3) at_addr_3plus,
  ROUND(COUNT_IF(n_at_addr >= 2) / COUNT(*), 3) share_shared_addr,
  ROUND(COUNT_IF(PROPRIETARY_NONPROFIT = 'P') / COUNT(*), 3) share_for_profit
FROM g GROUP BY 1 ORDER BY enrollments DESC;

-- [13] debts_by_type_and_size
WITH fd AS (
  SELECT ID, PERSON_ID, TRY_TO_NUMBER(YEAR_COL::VARCHAR) yr
  FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_FINANCIAL_DISCLOSURES
  QUALIFY ROW_NUMBER() OVER (PARTITION BY ID ORDER BY DATE_MODIFIED DESC) = 1
),
d AS (
  SELECT x.*, fd.PERSON_ID, fd.yr,
    CASE WHEN DESCRIPTION ILIKE ANY ('%mortg%', '%mtg%', '%residence%', '%home loan%') THEN 'mortgage'
         WHEN DESCRIPTION ILIKE ANY ('%equity%', '%heloc%') THEN 'home equity'
         WHEN DESCRIPTION ILIKE ANY ('%credit card%', '%card%', '%visa%', '%revolving%') THEN 'credit card'
         WHEN DESCRIPTION ILIKE ANY ('%line of cred%', '%loc%') THEN 'line of credit'
         WHEN DESCRIPTION ILIKE ANY ('%student%', '%educat%') THEN 'student loan'
         WHEN DESCRIPTION ILIKE ANY ('%auto%', '%car loan%', '%vehicle%') THEN 'auto'
         WHEN DESCRIPTION ILIKE ANY ('%margin%') THEN 'margin'
         ELSE 'other' END kind,
    CASE WHEN VALUE_CODE IN ('J', 'K') THEN 'J-K up to $50K' WHEN VALUE_CODE IN ('L', 'M') THEN 'L-M $50K-250K'
         WHEN VALUE_CODE IN ('N', 'O') THEN 'N-O $250K-1M' WHEN VALUE_CODE LIKE 'P%' THEN 'P over $1M'
         WHEN VALUE_CODE = '-1' THEN '-1 placeholder' ELSE 'other: ' || COALESCE(VALUE_CODE, 'null') END size_band
  FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DISCLOSURE_DEBTS x
  LEFT JOIN fd ON fd.ID = x.FINANCIAL_DISCLOSURE_ID
)
SELECT kind, size_band, COUNT(*) rows_, COUNT(DISTINCT PERSON_ID) judges, COUNT_IF(PERSON_ID IS NULL) no_judge,
  COUNT_IF(yr BETWEEN 1990 AND 2030) has_year, MIN(IFF(yr BETWEEN 1990 AND 2030, yr, NULL)) y0, MAX(IFF(yr BETWEEN 1990 AND 2030, yr, NULL)) y1,
  COUNT_IF(CREDITOR_NAME ILIKE ANY ('%wells%', '%chase%', '%bank of america%', '%citi%', '%pnc%', '%u.s. bank%', '%us bank%', '%truist%', '%suntrust%', '%capital one%')) big_bank_rows
FROM d GROUP BY GROUPING SETS ((kind), (size_band), ()) ORDER BY kind NULLS LAST, size_band NULLS LAST;

-- [14] agreements_classified
WITH fd AS (
  SELECT ID, PERSON_ID, TRY_TO_NUMBER(YEAR_COL::VARCHAR) yr
  FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_FINANCIAL_DISCLOSURES
  QUALIFY ROW_NUMBER() OVER (PARTITION BY ID ORDER BY DATE_MODIFIED DESC) = 1
),
a AS (
  SELECT x.*, fd.PERSON_ID, fd.yr,
    CASE WHEN PARTIES_AND_TERMS ILIKE ANY ('%llp%', '%l.l.p%', '% p.c.%', '% pc %', '% pc', '%pllc%', '%law firm%', '%attorneys%', '%capital account%', '%former firm%', '%former law%', '% partnership%', '%& %')
              AND NOT PARTIES_AND_TERMS ILIKE ANY ('%state of%', '%judicial retirement%', '%thrift%', '%county%', '%city of%', '%public employee%', '%teachers%')
           THEN 'firm-like'
         WHEN PARTIES_AND_TERMS ILIKE ANY ('%state%', '%judicial%', '%public%', '%county%', '%city%', '%thrift%', '%tsp%', '%federal%', '%fers%', '%csrs%', '%teacher%', '%government%', '%military%', '%army%', '%navy%', '%air force%', '%university%')
           THEN 'government or public plan'
         ELSE 'other (company plans, leave, misc)' END kind,
    PARTIES_AND_TERMS ILIKE ANY ('%deferred%', '%capital account%', '%buyout%', '%buy-out%', '%payout%', '%pay out%', '%installment%', '%return of capital%') money_back_words
  FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DISCLOSURE_AGREEMENTS x
  LEFT JOIN fd ON fd.ID = x.FINANCIAL_DISCLOSURE_ID
)
SELECT kind, money_back_words, COUNT(*) rows_, COUNT(DISTINCT PERSON_ID) judges, COUNT_IF(PERSON_ID IS NULL) no_judge,
  MIN(IFF(yr BETWEEN 1990 AND 2030, yr, NULL)) y0, MAX(IFF(yr BETWEEN 1990 AND 2030, yr, NULL)) y1,
  COUNT_IF(yr BETWEEN 1990 AND 2030) has_year, ANY_VALUE(LEFT(PARTIES_AND_TERMS, 90)) example
FROM a GROUP BY 1, 2 ORDER BY 1, 2;

-- [15] hospice_stacked_addresses_with_suites
WITH h AS (
  SELECT *, LEFT(REGEXP_REPLACE(ZIP_CODE, '[^0-9]', ''), 5) zip5,
    TRY_TO_NUMBER(LEFT(REGEXP_REPLACE(ZIP_CODE, '[^0-9]', ''), 3)) z3,
    UPPER(REGEXP_REPLACE(TRIM(ADDRESS_LINE_1), '\\s+', ' ')) addr,
    REGEXP_REPLACE(UPPER(COALESCE(ADDRESS_LINE_2, '')), '[^A-Z0-9]', '') suite
  FROM LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS
),
s AS (SELECT addr, zip5, suite, MIN(z3) z3, COUNT(*) n_suite FROM h GROUP BY 1, 2, 3),
a AS (
  SELECT h.addr, h.zip5, MIN(h.CITY) city, MIN(h.ENROLLMENT_STATE) st, COUNT(*) n, COUNT(DISTINCT h.suite) suites,
    MAX(s.n_suite) max_same_suite, COUNT(DISTINCT h.ORGANIZATION_NAME) orgs, COUNT(DISTINCT h.ASSOCIATE_ID) assoc_ids,
    COUNT_IF(h.INCORPORATION_DATE >= '2019-01-01') inc_2019p, MIN(h.INCORPORATION_DATE) inc_min, MAX(h.INCORPORATION_DATE) inc_max,
    MIN(h.ENROLLMENT_ID) first_enroll_id, MAX(h.ENROLLMENT_ID) last_enroll_id,
    LISTAGG(DISTINCT LEFT(h.ORGANIZATION_NAME, 28), ' | ') orgs_list
  FROM h JOIN s ON s.addr = h.addr AND s.zip5 = h.zip5 AND s.suite = h.suite
  GROUP BY 1, 2
)
SELECT a.addr, a.zip5, a.city, a.st, a.n, a.suites, a.max_same_suite, a.orgs, a.assoc_ids, a.inc_2019p, a.inc_min, a.inc_max,
  a.first_enroll_id, a.last_enroll_id, LEFT(a.orgs_list, 140) orgs_list,
  (SELECT COUNT(*) FROM LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS WHERE NPI::VARCHAR IN ('1013548734', '1447931134', '1487748646')) facts_npi_rows_now,
  (SELECT SUM(n_suite) FROM s WHERE n_suite >= 2 AND (z3 BETWEEN 900 AND 918 OR z3 = 935)) la_enrollments_sharing_exact_suite,
  (SELECT SUM(n_suite) FROM s WHERE n_suite >= 2 AND NOT (z3 BETWEEN 900 AND 918 OR z3 = 935)) rest_enrollments_sharing_exact_suite
FROM a WHERE a.n >= 4 ORDER BY a.n DESC LIMIT 20;

-- [16] agreements_firm_keys_by_judges
WITH fd AS (
  SELECT ID, PERSON_ID, TRY_TO_NUMBER(YEAR_COL::VARCHAR) yr
  FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_FINANCIAL_DISCLOSURES
  QUALIFY ROW_NUMBER() OVER (PARTITION BY ID ORDER BY DATE_MODIFIED DESC) = 1
),
a AS (
  SELECT x.PARTIES_AND_TERMS p, fd.PERSON_ID, fd.yr,
    TRIM(REGEXP_REPLACE(UPPER(SPLIT_PART(SPLIT_PART(SPLIT_PART(SPLIT_PART(x.PARTIES_AND_TERMS, ' - ', 1), '(', 1), ',', 1), CHR(59), 1)), '[^A-Z& ]', '')) k0
  FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DISCLOSURE_AGREEMENTS x
  LEFT JOIN fd ON fd.ID = x.FINANCIAL_DISCLOSURE_ID
  WHERE x.PARTIES_AND_TERMS ILIKE ANY ('%llp%', '%l.l.p%', '% p.c.%', '% pc %', '%pllc%', '%law firm%', '%attorneys%', '%capital account%', '%former firm%', '%& %', '% partners%', '%deferred comp%')
)
SELECT REGEXP_SUBSTR(k0, '^[^ ]+( [^ ]+)?( [^ ]+)?') firm_key, COUNT(*) rows_, COUNT(DISTINCT PERSON_ID) judges, MIN(yr) y0, MAX(yr) y1,
  ANY_VALUE(LEFT(p, 100)) example
FROM a GROUP BY 1 ORDER BY judges DESC, rows_ DESC LIMIT 60;

-- [17] meal_raw_price_points_by_year
WITH f AS (
  SELECT PROGRAM_YEAR py, TRY_TO_DECIMAL(TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS::VARCHAR, 14, 2) amt
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS
  WHERE NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE = 'Food and Beverage'
)
SELECT py, COUNT(*) meals, COUNT_IF(amt IS NULL) bad_amt,
  COUNT_IF(amt < 100) under_100, COUNT_IF(amt >= 100 AND amt < 115) b100_115, COUNT_IF(amt >= 115 AND amt < 125) b115_125,
  COUNT_IF(amt = 125) at_125_00, COUNT_IF(amt > 125 AND amt < 135) b125_135_excl, COUNT_IF(amt >= 135 AND amt < 150) b135_150,
  COUNT_IF(amt >= 150 AND amt < 200) b150_200, COUNT_IF(amt >= 200) at_or_over_200,
  COUNT_IF(amt = 75) at_75, COUNT_IF(amt = 99.99) at_99_99, COUNT_IF(amt = 100) at_100, COUNT_IF(amt = 123.99) at_123_99,
  COUNT_IF(amt = 124.50) at_124_50, COUNT_IF(amt = 124.99) at_124_99, COUNT_IF(amt = 126) at_126, COUNT_IF(amt = 149.99) at_149_99,
  COUNT_IF(amt = 150) at_150, COUNT_IF(amt = 200) at_200, COUNT_IF(amt = 250) at_250
FROM f GROUP BY 1 ORDER BY 1;

-- [18] debts_bank_creditor_vs_bank_party_dockets
WITH fd AS (
  SELECT ID, PERSON_ID, TRY_TO_NUMBER(YEAR_COL::VARCHAR) yr
  FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_FINANCIAL_DISCLOSURES
  WHERE PERSON_ID IS NOT NULL
  QUALIFY ROW_NUMBER() OVER (PARTITION BY ID ORDER BY DATE_MODIFIED DESC) = 1
),
b AS (
  SELECT * FROM VALUES
    ('WELLS FARGO', '.*wells fargo.*', '.*wells fargo.*'),
    ('CHASE/JPMORGAN', '.*(chase|jp ?morgan|j\\.p\\. ?morgan).*', '.*(jpmorgan chase|j\\.p\\. morgan chase|chase bank|chase home finance|chase manhattan|chase auto).*'),
    ('BANK OF AMERICA', '.*(bank of america|bofa|countrywide).*', '.*(bank of america|countrywide).*'),
    ('CITI', '.*(citibank|citicard|citimortgage|citi card|citigroup|citifinancial|citi ).*', '.*(citibank|citimortgage|citigroup|citicorp|citifinancial).*'),
    ('AMERICAN EXPRESS', '.*(american express|amex|amcrican express).*', '.*american express.*'),
    ('CAPITAL ONE', '.*capital one.*', '.*capital one.*'),
    ('DISCOVER', '.*discover.*', '.*discover (bank|financial|card|products).*'),
    ('US BANK', '.*(u\\.s\\. bank|us bank|usbank).*', '.*(u\\.s\\. bank|us bank n).*'),
    ('PNC', '.*pnc.*', '.*pnc bank.*'),
    ('SUNTRUST/TRUIST/BBT', '.*(suntrust|truist|bb&t|branch banking).*', '.*(suntrust|truist|bb&t|branch banking).*'),
    ('NAVIENT/SALLIE MAE', '.*(navient|sallie mae).*', '.*(navient|sallie mae).*'),
    ('SYNCHRONY/GE', '.*(synchrony|ge money|ge capital).*', '.*(synchrony|ge money bank|ge capital).*'),
    ('HSBC', '.*hsbc.*', '.*hsbc.*'),
    ('OCWEN', '.*ocwen.*', '.*ocwen.*'),
    ('NATIONSTAR', '.*(nationstar|mr\\.? cooper).*', '.*nationstar.*'),
    ('USAA', '.*usaa.*', '.*(usaa|united services automobile).*'),
    ('SANTANDER', '.*santander.*', '.*santander.*')
  AS t(bank, cred_re, case_re)
),
d AS (
  SELECT fd.PERSON_ID, fd.yr, b.bank, b.case_re, x.VALUE_CODE,
    CASE WHEN x.DESCRIPTION ILIKE ANY ('%mortg%', '%mtg%', '%residence%', '%home loan%', '%equity%', '%heloc%') THEN 'home'
         WHEN x.DESCRIPTION ILIKE ANY ('%card%', '%visa%', '%revolving%', '%charge%') THEN 'card' ELSE 'other' END kind
  FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DISCLOSURE_DEBTS x
  JOIN fd ON fd.ID = x.FINANCIAL_DISCLOSURE_ID
  JOIN b ON REGEXP_LIKE(x.CREDITOR_NAME, b.cred_re, 'i')
  WHERE fd.yr BETWEEN 2003 AND 2021
),
pairs AS (
  SELECT PERSON_ID, bank, case_re, yr, BOOLOR_AGG(kind = 'home') has_home, BOOLOR_AGG(kind = 'card') has_card,
    BOOLOR_AGG(VALUE_CODE IN ('M', 'N', 'O') OR VALUE_CODE LIKE 'P%') over_100k
  FROM d GROUP BY 1, 2, 3, 4
),
judges AS (SELECT DISTINCT PERSON_ID FROM pairs),
dk AS (
  SELECT k.ID docket_id, k.ASSIGNED_TO_ID, YEAR(k.DATE_FILED) fy, k.CASE_NAME, k.NATURE_OF_SUIT
  FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS k
  JOIN judges j ON j.PERSON_ID = k.ASSIGNED_TO_ID
  WHERE k.DATE_FILED BETWEEN '2003-01-01' AND '2022-12-31' AND k.MDL_STATUS IS NULL
    AND k.CASE_NAME ILIKE ANY ('%wells fargo%', '%chase%', '%morgan%', '%bank of america%', '%countrywide%', '%citi%', '%american express%',
      '%capital one%', '%discover%', '%u.s. bank%', '%us bank%', '%pnc%', '%suntrust%', '%truist%', '%bb&t%', '%branch banking%', '%navient%',
      '%sallie mae%', '%synchrony%', '%ge money%', '%ge capital%', '%hsbc%', '%ocwen%', '%nationstar%', '%usaa%', '%united services automobile%', '%santander%')
),
hits AS (
  SELECT DISTINCT p.PERSON_ID, p.bank, p.has_home, p.has_card, p.over_100k, dk.docket_id, dk.fy,
    CASE WHEN dk.NATURE_OF_SUIT ILIKE ANY ('%foreclos%', '220%', '%real prop%', '%mortgage%') THEN 'foreclosure/real property'
         WHEN dk.NATURE_OF_SUIT ILIKE ANY ('%truth in lending%', '371%', '%consumer credit%', '480%', '%fair debt%', '%fair credit%') THEN 'lending/consumer credit'
         WHEN NULLIF(TRIM(dk.NATURE_OF_SUIT), '') IS NULL THEN 'suit type blank'
         ELSE 'other suit type' END suit
  FROM dk JOIN pairs p ON p.PERSON_ID = dk.ASSIGNED_TO_ID AND dk.fy BETWEEN p.yr AND p.yr + 1 AND REGEXP_LIKE(dk.CASE_NAME, p.case_re, 'i')
)
SELECT COALESCE(bank, 'ALL BANKS') bank, COALESCE(suit, 'ALL SUITS') suit, COUNT(DISTINCT docket_id) dockets, COUNT(DISTINCT PERSON_ID) judges,
  COUNT(DISTINCT IFF(has_home, docket_id, NULL)) dk_judge_had_home_loan_there, COUNT(DISTINCT IFF(has_card, docket_id, NULL)) dk_judge_had_card_there,
  COUNT(DISTINCT IFF(over_100k, docket_id, NULL)) dk_debt_over_100k, MIN(fy) fy0, MAX(fy) fy1,
  (SELECT COUNT(*) FROM pairs) judge_bank_year_pairs, (SELECT COUNT(DISTINCT PERSON_ID) FROM pairs) judges_with_bank_debt
FROM hits GROUP BY GROUPING SETS ((bank), (suit), ()) ORDER BY dockets DESC;

-- [19] agreements_firm_as_counsel_before_same_judge
WITH fd AS (
  SELECT ID, PERSON_ID, TRY_TO_NUMBER(YEAR_COL::VARCHAR) yr
  FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_FINANCIAL_DISCLOSURES
  WHERE PERSON_ID IS NOT NULL
  QUALIFY ROW_NUMBER() OVER (PARTITION BY ID ORDER BY DATE_MODIFIED DESC) = 1
),
f AS (
  SELECT * FROM VALUES
  ('STROOCK','stroock'),('FOLEY & LARDNER','foley (&|and) lardner'),('DEBEVOISE','debevoise'),('HAYNES AND BOONE','haynes (&|and) boone'),
  ('BURR & FORMAN','burr (&|and) forman'),('JONES DAY','jones,? day'),('PIERCE ATWOOD','pierce,? atwood'),('BARNES & THORNBURG','b[ae]r?[nm]es (&|and) thornburg'),
  ('POTTER ANDERSON','potter,? anderson'),('MINER BARNHILL','miner,? barnhill'),('O MELVENY','o.?melveny'),('MILLER & CHEVALIER','miller (&|and) chevalier'),
  ('BUCHANAN INGERSOLL','buchanan,? ingersoll'),('WEIL GOTSHAL','weil,? gotshal'),('CLEARY GOTTLIEB','cleary,? gottlieb'),('MESCH CLARK','mesch,? clark'),
  ('STEPTOE & JOHNSON','steptoe (&|and) johnson'),('LISKOW & LEWIS','liskow (&|and) lewis'),('SIDLEY','sidley'),('DAY PITNEY','day,? pitney'),
  ('DORSEY & WHITNEY','dorsey (&|and) whitney'),('HUGHES HUBBARD','hughes,? hubbard'),('SHEPPARD MULLIN','sheppard,? mullin'),('MCDONALD CARANO','mcdonald,? carano'),
  ('TRENAM','trenam'),('MEYER SUOZZI','meyer,? suozzi'),('THOMPSON COBURN','thompson,? coburn'),('BAKER DONELSON','baker,? donelson'),('BRYAN CAVE','bryan,? cave'),
  ('DAVIS GRAHAM','davis,? graham'),('VENABLE','venable'),('WILLKIE','willkie'),('WILLIAMS & CONNOLLY','williams (&|and) connolly'),('FRASER STRYKER','fraser,? stryker'),
  ('SHEARMAN','shearman'),('SQUIRE','squire,? (sanders|patton)'),('BALCH & BINGHAM','balch (&|and) bingham'),('COZEN','cozen'),('ATLAS & HALL','atlas (&|and) hall'),
  ('LEWIS BABCOCK','lewis,? babcock'),('ROSEN HARWOOD','rosen,? harwood'),('KIRKLAND','kirkland (&|and) ellis'),('LATHAM','latham (&|and) watkins'),
  ('COVINGTON','covington (&|and) burling'),('WILMER','wilmer,? cutler'),('GIBSON DUNN','gibson,? dunn'),('SKADDEN','skadden'),('SULLIVAN & CROMWELL','sullivan (&|and) cromwell'),
  ('PAUL WEISS','paul,? weiss'),('CRAVATH','cravath'),('DAVIS POLK','davis,? polk'),('MUNGER TOLLES','munger,? tolles'),('ARNOLD & PORTER','arnold (&|and) porter'),
  ('KING & SPALDING','king (&|and) spalding'),('ALSTON & BIRD','alston (&|and) bird'),('VINSON & ELKINS','vinson (&|and) elkins'),('BAKER BOTTS','baker,? botts'),
  ('AKIN GUMP','akin,? gump'),('MAYER BROWN','mayer,? brown'),('MORGAN LEWIS','morgan,? lewis (&|and) bockius'),('ROPES & GRAY','ropes (&|and) gray'),
  ('HOLLAND & KNIGHT','holland (&|and) knight'),('GREENBERG TRAURIG','greenberg,? traurig'),('BRADLEY ARANT','bradley,? arant'),('JENNER & BLOCK','jenner (&|and) block'),
  ('WINSTON & STRAWN','winston (&|and) strawn'),('PERKINS COIE','perkins,? coie'),('HOGAN','hogan (&|and) hartson|hogan lovells'),('FULBRIGHT','fulbright (&|and) jaworski'),
  ('BRACEWELL','bracewell'),('BALLARD SPAHR','ballard,? spahr'),('DECHERT','dechert'),('DRINKER BIDDLE','drinker,? biddle'),('REED SMITH','reed,? smith'),
  ('MCGUIREWOODS','mcguire,? ?woods'),('HUNTON','hunton (&|and) williams|hunton andrews'),('TROUTMAN','troutman'),('KILPATRICK','kilpatrick'),('NELSON MULLINS','nelson,? mullins'),
  ('BUTLER SNOW','butler,? snow'),('BASS BERRY','bass,? berry'),('FROST BROWN TODD','frost,? brown,? todd'),('DINSMORE','dinsmore (&|and) shohl'),('TAFT','taft,? stettinius'),
  ('THOMPSON HINE','thompson,? hine'),('VORYS','vorys'),('FAEGRE','faegre'),('QUARLES & BRADY','quarles (&|and) brady'),('SNELL & WILMER','snell (&|and) wilmer'),
  ('PHELPS DUNBAR','phelps,? dunbar'),('JONES WALKER','jones,? walker'),('ADAMS AND REESE','adams (&|and) reese'),('MAYNARD COOPER','maynard,? cooper'),
  ('LATHROP','lathrop (&|and) gage'),('HUSCH','husch'),('POLSINELLI','polsinelli'),('PORTER WRIGHT','porter,? wright'),('BRICKER','bricker (&|and) eckler'),
  ('ICE MILLER','ice,? miller'),('WYATT TARRANT','wyatt,? tarrant'),('STITES','stites (&|and) harbison'),('DUANE MORRIS','duane,? morris'),('BLANK ROME','blank,? rome'),
  ('PEPPER HAMILTON','pepper,? hamilton'),('ORRICK','orrick'),('MORRISON & FOERSTER','morrison (&|and) foerster'),('PILLSBURY','pillsbury'),('WILSON SONSINI','wilson,? sonsini'),
  ('QUINN EMANUEL','quinn,? emanuel'),('SUSMAN GODFREY','susman,? godfrey'),('LOCKE LORD','locke,? lord'),('ANDREWS KURTH','andrews,? kurth'),('WOMBLE','womble'),
  ('ROBINSON BRADSHAW','robinson,? bradshaw'),('SCHIFF HARDIN','schiff,? hardin'),('SHOOK HARDY','shook,? hardy'),('ARMSTRONG TEASDALE','armstrong,? teasdale'),
  ('SPENCER FANE','spencer,? fane'),('LEWIS RICE','lewis,? rice'),('CADWALADER','cadwalader'),('MILBANK','milbank'),('PROSKAUER','proskauer'),('FRIED FRANK','fried,? frank'),
  ('SIMPSON THACHER','simpson,? thacher'),('WACHTELL','wachtell'),('KRAMER LEVIN','kramer,? levin'),('PATTERSON BELKNAP','patterson,? belknap'),('GOODWIN PROCTER','goodwin,? procter'),
  ('CHOATE','choate,? hall'),('FOLEY HOAG','foley,? hoag'),('NIXON PEABODY','nixon,? peabody'),('HINCKLEY ALLEN','hinckley,? allen'),('ROBINSON & COLE','robinson (&|and) cole'),
  ('WIGGIN','wiggin (&|and) dana'),('MINTZ LEVIN','mintz,? levin'),('BROWNSTEIN','brownstein'),('HOLLAND & HART','holland (&|and) hart'),('SHERMAN & HOWARD','sherman (&|and) howard'),
  ('DAVIS WRIGHT','davis,? wright'),('LANE POWELL','lane,? powell'),('STOEL RIVES','stoel,? rives'),('MILLER NASH','miller,? nash'),('FREDRIKSON','fredrikson'),
  ('BRIGGS AND MORGAN','briggs (&|and) morgan'),('GODFREY & KAHN','godfrey (&|and) kahn'),('MICHAEL BEST','michael,? best'),('HONIGMAN','honigman'),('DICKINSON WRIGHT','dickinson,? wright'),
  ('DYKEMA','dykema'),('MILLER CANFIELD','miller,? canfield'),('WARNER NORCROSS','warner,? norcross'),('KIRKPATRICK','kirkpatrick'),('BALCH','balch (&|and) bingham')
  AS t(firm, re)
),
ag AS (
  SELECT fd.PERSON_ID, f.firm, f.re,
    MIN(IFF(fd.yr BETWEEN 1990 AND 2030, fd.yr, NULL)) y0, MAX(IFF(fd.yr BETWEEN 1990 AND 2030, fd.yr, NULL)) y1, COUNT(*) n_rows,
    ANY_VALUE(LEFT(x.PARTIES_AND_TERMS, 80)) agreement_text
  FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DISCLOSURE_AGREEMENTS x
  JOIN fd ON fd.ID = x.FINANCIAL_DISCLOSURE_ID
  JOIN f ON REGEXP_LIKE(x.PARTIES_AND_TERMS, '.*(' || f.re || ').*', 'is')
  GROUP BY 1, 2, 3
),
jn AS (SELECT ag.*, j.NAME_FIRST, j.NAME_LAST FROM ag JOIN LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_JUDGES j ON j.ID = ag.PERSON_ID),
fi AS (SELECT DISTINCT firm, re FROM ag),
pat AS (SELECT '.*(' || LISTAGG(re, '|') || ').*' p FROM fi),
cl AS (
  SELECT c.ID cluster_id, c.DOCKET_ID, c.DATE_FILED, c.CASE_NAME, c.JUDGES, c.ATTORNEYS
  FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_OPINION_CLUSTERS c JOIN pat ON REGEXP_LIKE(c.ATTORNEYS, pat.p, 'is')
),
clf AS (SELECT cl.*, fi.firm FROM cl JOIN fi ON REGEXP_LIKE(cl.ATTORNEYS, '.*(' || fi.re || ').*', 'is')),
m AS (
  SELECT jn.PERSON_ID, jn.NAME_FIRST, jn.NAME_LAST, jn.firm, jn.y0, jn.y1, jn.agreement_text, clf.cluster_id, clf.DATE_FILED, clf.CASE_NAME, clf.JUDGES, clf.ATTORNEYS,
    k.COURT_ID, (k.ASSIGNED_TO_ID = jn.PERSON_ID) by_id
  FROM clf JOIN jn ON jn.firm = clf.firm
  LEFT JOIN LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS k ON k.ID = clf.DOCKET_ID
  WHERE k.ASSIGNED_TO_ID = jn.PERSON_ID
     OR (LENGTH(jn.NAME_LAST) >= 4 AND REGEXP_LIKE(clf.JUDGES, '.*\\b' || jn.NAME_LAST || '\\b.*', 'is'))
),
pairs AS (
  SELECT PERSON_ID, NAME_FIRST || ' ' || NAME_LAST judge, firm, y0, y1, ANY_VALUE(agreement_text) agreement_text,
    COUNT(DISTINCT cluster_id) opinions_all_time,
    COUNT(DISTINCT IFF(YEAR(DATE_FILED) BETWEEN y0 - 2 AND y1 + 1, cluster_id, NULL)) opinions_in_window,
    COUNT_IF(by_id) by_assigned_id, MIN(DATE_FILED) first_op, MAX(DATE_FILED) last_op, LISTAGG(DISTINCT COURT_ID, ',') courts,
    ANY_VALUE(CASE_NAME) example_case, ANY_VALUE(LEFT(JUDGES, 60)) example_judges
  FROM m GROUP BY 1, 2, 3, 4, 5
)
SELECT pairs.*, COUNT(*) OVER () pairs_with_any_opinion, SUM(opinions_all_time) OVER () total_opinions,
  COUNT_IF(opinions_in_window > 0) OVER () pairs_in_window, SUM(opinions_in_window) OVER () total_in_window,
  (SELECT COUNT(*) FROM ag) judge_firm_pairs_in_agreements, (SELECT COUNT(DISTINCT PERSON_ID) FROM ag) judges_with_named_firm,
  (SELECT COUNT(*) FROM cl) clusters_naming_any_firm
FROM pairs ORDER BY opinions_in_window DESC, opinions_all_time DESC LIMIT 40;

-- [20] debts_top_judge_bank_pairs
WITH fd AS (
  SELECT ID, PERSON_ID, TRY_TO_NUMBER(YEAR_COL::VARCHAR) yr
  FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_FINANCIAL_DISCLOSURES
  WHERE PERSON_ID IS NOT NULL
  QUALIFY ROW_NUMBER() OVER (PARTITION BY ID ORDER BY DATE_MODIFIED DESC) = 1
),
b AS (
  SELECT * FROM VALUES
    ('WELLS FARGO', '.*wells fargo.*', '.*wells fargo.*'),
    ('CHASE/JPMORGAN', '.*(chase|jp ?morgan|j\\.p\\. ?morgan).*', '.*(jpmorgan chase|j\\.p\\. morgan chase|chase bank|chase home finance|chase manhattan|chase auto).*'),
    ('BANK OF AMERICA', '.*(bank of america|bofa|countrywide).*', '.*(bank of america|countrywide).*'),
    ('CITI', '.*(citibank|citicard|citimortgage|citi card|citigroup|citifinancial|citi ).*', '.*(citibank|citimortgage|citigroup|citicorp|citifinancial).*'),
    ('AMERICAN EXPRESS', '.*(american express|amex|amcrican express).*', '.*american express.*'),
    ('CAPITAL ONE', '.*capital one.*', '.*capital one.*')
  AS t(bank, cred_re, case_re)
),
d AS (
  SELECT fd.PERSON_ID, fd.yr, b.bank, b.case_re, x.VALUE_CODE, x.CREDITOR_NAME, x.DESCRIPTION,
    CASE WHEN x.DESCRIPTION ILIKE ANY ('%mortg%', '%mtg%', '%residence%', '%home loan%', '%equity%', '%heloc%') THEN 'home'
         WHEN x.DESCRIPTION ILIKE ANY ('%card%', '%visa%', '%revolving%', '%charge%') THEN 'card' ELSE 'other' END kind
  FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DISCLOSURE_DEBTS x
  JOIN fd ON fd.ID = x.FINANCIAL_DISCLOSURE_ID
  JOIN b ON REGEXP_LIKE(x.CREDITOR_NAME, b.cred_re, 'i')
  WHERE fd.yr BETWEEN 2003 AND 2021
),
pairs AS (
  SELECT PERSON_ID, bank, case_re, yr, LISTAGG(DISTINCT kind, ',') kinds, MAX(VALUE_CODE) max_code, ANY_VALUE(CREDITOR_NAME || ' / ' || DESCRIPTION) debt_example
  FROM d GROUP BY 1, 2, 3, 4
),
judges AS (SELECT DISTINCT PERSON_ID FROM pairs),
dk AS (
  SELECT k.ID docket_id, k.ASSIGNED_TO_ID, YEAR(k.DATE_FILED) fy, k.CASE_NAME, k.NATURE_OF_SUIT, k.COURT_ID
  FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS k
  JOIN judges j ON j.PERSON_ID = k.ASSIGNED_TO_ID
  WHERE k.DATE_FILED BETWEEN '2003-01-01' AND '2022-12-31' AND k.MDL_STATUS IS NULL
    AND k.CASE_NAME ILIKE ANY ('%wells fargo%', '%chase%', '%morgan%', '%bank of america%', '%countrywide%', '%citi%', '%american express%', '%capital one%')
),
hits AS (
  SELECT DISTINCT p.PERSON_ID, p.bank, p.kinds, p.max_code, p.debt_example, dk.docket_id, dk.fy, dk.CASE_NAME, dk.NATURE_OF_SUIT, dk.COURT_ID
  FROM dk JOIN pairs p ON p.PERSON_ID = dk.ASSIGNED_TO_ID AND dk.fy BETWEEN p.yr AND p.yr + 1 AND REGEXP_LIKE(dk.CASE_NAME, p.case_re, 'i')
)
SELECT j.NAME_FIRST || ' ' || j.NAME_LAST judge, h.bank, COUNT(DISTINCT h.docket_id) dockets,
  COUNT(DISTINCT IFF(h.NATURE_OF_SUIT ILIKE ANY ('%foreclos%', '220%', '%real prop%', '%mortgage%', '%truth in lending%', '371%', '%consumer credit%', '480%'), h.docket_id, NULL)) housing_or_lending_suits,
  LISTAGG(DISTINCT h.kinds, ',') debt_kinds, MAX(h.max_code) max_code, MIN(h.fy) fy0, MAX(h.fy) fy1, LISTAGG(DISTINCT h.COURT_ID, ',') courts,
  ANY_VALUE(LEFT(h.debt_example, 60)) debt_example, ANY_VALUE(LEFT(h.CASE_NAME, 70)) case_example, ANY_VALUE(LEFT(h.NATURE_OF_SUIT, 40)) suit_example,
  SUM(COUNT(DISTINCT h.docket_id)) OVER () sum_pair_dockets
FROM hits h JOIN LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_JUDGES j ON j.ID = h.PERSON_ID
GROUP BY 1, 2 ORDER BY dockets DESC LIMIT 20;

-- [21] hospice_cfhc_and_la_stack_still_certified
WITH e AS (
  SELECT *, TRY_TO_NUMBER(LEFT(REGEXP_REPLACE(ZIP_CODE, '[^0-9]', ''), 3)) z3,
    LEFT(REGEXP_REPLACE(ZIP_CODE, '[^0-9]', ''), 5) zip5, UPPER(REGEXP_REPLACE(TRIM(ADDRESS_LINE_1), '\\s+', ' ')) addr
  FROM LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS
),
a AS (SELECT addr, zip5, COUNT(*) n FROM e GROUP BY 1, 2),
c AS (SELECT LPAD(TRIM(CCN), 6, '0') ccn, MIN(CERTIFICATION_DATE) cert, MIN(OWNERSHIP_TYPE) own FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPICE GROUP BY 1),
g AS (
  SELECT e.*, a.n n_at_addr, c.ccn cert_ccn, c.cert,
    CASE WHEN e.ORGANIZATION_NAME ILIKE 'CFHC%' THEN 'CFHC-named' WHEN (e.z3 BETWEEN 900 AND 918 OR e.z3 = 935) AND a.n >= 3 THEN 'LA 3+ per address'
         WHEN (e.z3 BETWEEN 900 AND 918 OR e.z3 = 935) THEN 'LA other' ELSE 'rest' END grp
  FROM e JOIN a ON a.addr = e.addr AND a.zip5 = e.zip5
  LEFT JOIN c ON c.ccn = LPAD(TRIM(e.CCN), 6, '0')
)
SELECT grp, COUNT(*) enrollments, COUNT_IF(cert_ccn IS NOT NULL) ccn_in_certified_list, COUNT_IF(NULLIF(TRIM(CCN), '') IS NULL) ccn_blank,
  MIN(cert) cert_min, MAX(cert) cert_max, COUNT_IF(cert >= '2019-01-01') certified_2019_plus,
  COUNT(DISTINCT addr || zip5) addresses, LISTAGG(DISTINCT IFF(grp = 'CFHC-named', ORGANIZATION_NAME || ' @ ' || addr || ' ' || CITY, NULL), ' | ') cfhc_list,
  MAX(ENROLLMENT_ID) newest_enrollment_id
FROM g GROUP BY 1 ORDER BY 1;

-- [22] hospice_cfhc_numbered_corps_list
SELECT e.ORGANIZATION_NAME, e.DOING_BUSINESS_AS_NAME, e.ADDRESS_LINE_1, e.ADDRESS_LINE_2, e.CITY, e.ENROLLMENT_STATE, e.ENROLLMENT_ID, e.INCORPORATION_DATE,
  e.ASSOCIATE_ID, e.CCN, h.CERTIFICATION_DATE, h.OWNERSHIP_TYPE
FROM LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS e
LEFT JOIN LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPICE h ON LPAD(TRIM(h.CCN), 6, '0') = LPAD(TRIM(e.CCN), 6, '0')
WHERE e.ORGANIZATION_NAME ILIKE 'CFHC%' OR e.DOING_BUSINESS_AS_NAME ILIKE 'CFHC%'
ORDER BY e.ORGANIZATION_NAME;

-- [23] debts_non_ordinary_loans_and_eye_sample
WITH fd AS (
  SELECT ID, PERSON_ID, TRY_TO_NUMBER(YEAR_COL::VARCHAR) yr
  FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_FINANCIAL_DISCLOSURES
  WHERE PERSON_ID IS NOT NULL
  QUALIFY ROW_NUMBER() OVER (PARTITION BY ID ORDER BY DATE_MODIFIED DESC) = 1
),
b AS (
  SELECT * FROM VALUES
    ('WELLS FARGO', '.*wells fargo.*', '.*wells fargo.*'),
    ('CHASE/JPMORGAN', '.*(chase|jp ?morgan|j\\.p\\. ?morgan).*', '.*(jpmorgan chase|j\\.p\\. morgan chase|chase bank|chase home finance|chase manhattan|chase auto).*'),
    ('BANK OF AMERICA', '.*(bank of america|bofa|countrywide).*', '.*(bank of america|countrywide).*'),
    ('CITI', '.*(citibank|citicard|citimortgage|citi card|citigroup|citifinancial|citi ).*', '.*(citibank|citimortgage|citigroup|citicorp|citifinancial).*'),
    ('AMERICAN EXPRESS', '.*(american express|amex|amcrican express).*', '.*american express.*'),
    ('CAPITAL ONE', '.*capital one.*', '.*capital one.*')
  AS t(bank, cred_re, case_re)
),
d AS (
  SELECT fd.PERSON_ID, fd.yr, b.bank, b.case_re, x.VALUE_CODE, x.CREDITOR_NAME, x.DESCRIPTION,
    (x.DESCRIPTION ILIKE ANY ('%guarant%', '%invest%', '%rental%', '%business%', '%commercial%', '%farm%', '%llc%', '%partnership%', '%second home%', '%vacation%', '%condo%')
      OR x.VALUE_CODE IN ('N', 'O') OR x.VALUE_CODE LIKE 'P%') non_ordinary
  FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DISCLOSURE_DEBTS x
  JOIN fd ON fd.ID = x.FINANCIAL_DISCLOSURE_ID
  JOIN b ON REGEXP_LIKE(x.CREDITOR_NAME, b.cred_re, 'i')
  WHERE fd.yr BETWEEN 2003 AND 2021
),
pairs AS (
  SELECT PERSON_ID, bank, case_re, yr, BOOLOR_AGG(non_ordinary) non_ordinary,
    ANY_VALUE(IFF(non_ordinary, CREDITOR_NAME || ' / ' || DESCRIPTION || ' / ' || VALUE_CODE, NULL)) non_ordinary_example,
    ANY_VALUE(CREDITOR_NAME || ' / ' || DESCRIPTION || ' / ' || VALUE_CODE) debt_example
  FROM d GROUP BY 1, 2, 3, 4
),
judges AS (SELECT DISTINCT PERSON_ID FROM pairs),
dk AS (
  SELECT k.ID docket_id, k.ASSIGNED_TO_ID, YEAR(k.DATE_FILED) fy, k.CASE_NAME, k.NATURE_OF_SUIT, k.COURT_ID
  FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS k
  JOIN judges j ON j.PERSON_ID = k.ASSIGNED_TO_ID
  WHERE k.DATE_FILED BETWEEN '2003-01-01' AND '2022-12-31' AND k.MDL_STATUS IS NULL
    AND k.CASE_NAME ILIKE ANY ('%wells fargo%', '%chase%', '%morgan%', '%bank of america%', '%countrywide%', '%citi%', '%american express%', '%capital one%')
),
hits AS (
  SELECT DISTINCT p.PERSON_ID, p.bank, p.non_ordinary, p.non_ordinary_example, p.debt_example, dk.docket_id, dk.fy, dk.CASE_NAME, dk.COURT_ID,
    REGEXP_LIKE(dk.COURT_ID, '.*b$') bankruptcy_court
  FROM dk JOIN pairs p ON p.PERSON_ID = dk.ASSIGNED_TO_ID AND dk.fy BETWEEN p.yr AND p.yr + 1 AND REGEXP_LIKE(dk.CASE_NAME, p.case_re, 'i')
),
summ AS (
  SELECT 'summary' kind,
    'dockets=' || COUNT(DISTINCT docket_id) || ' judges=' || COUNT(DISTINCT PERSON_ID)
    || ' | bankruptcy-court dockets=' || COUNT(DISTINCT IFF(bankruptcy_court, docket_id, NULL)) || ' judges=' || COUNT(DISTINCT IFF(bankruptcy_court, PERSON_ID, NULL))
    || ' | non-ordinary-debt dockets=' || COUNT(DISTINCT IFF(non_ordinary, docket_id, NULL)) || ' judges=' || COUNT(DISTINCT IFF(non_ordinary, PERSON_ID, NULL))
    || ' | non-ordinary in district courts dockets=' || COUNT(DISTINCT IFF(non_ordinary AND NOT bankruptcy_court, docket_id, NULL)) || ' judges=' || COUNT(DISTINCT IFF(non_ordinary AND NOT bankruptcy_court, PERSON_ID, NULL)) detail
  FROM hits
),
samp AS (
  SELECT 'sample' kind, h.bank || ' | ' || h.COURT_ID || ' ' || h.fy || ' | ' || LEFT(h.CASE_NAME, 70) || ' | debt: ' || LEFT(COALESCE(h.non_ordinary_example, h.debt_example), 70) || ' | judge: ' || j.NAME_LAST detail
  FROM hits h JOIN LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_JUDGES j ON j.ID = h.PERSON_ID
  WHERE h.non_ordinary AND NOT h.bankruptcy_court
  ORDER BY HASH(h.docket_id) LIMIT 12
)
SELECT * FROM summ UNION ALL SELECT * FROM samp;

-- [24] debts_non_ordinary_summary_rerun_untruncated
WITH fd AS (
  SELECT ID, PERSON_ID, TRY_TO_NUMBER(YEAR_COL::VARCHAR) yr
  FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_FINANCIAL_DISCLOSURES
  WHERE PERSON_ID IS NOT NULL
  QUALIFY ROW_NUMBER() OVER (PARTITION BY ID ORDER BY DATE_MODIFIED DESC) = 1
),
b AS (
  SELECT * FROM VALUES
    ('WELLS FARGO', '.*wells fargo.*', '.*wells fargo.*'),
    ('CHASE/JPMORGAN', '.*(chase|jp ?morgan|j\\.p\\. ?morgan).*', '.*(jpmorgan chase|j\\.p\\. morgan chase|chase bank|chase home finance|chase manhattan|chase auto).*'),
    ('BANK OF AMERICA', '.*(bank of america|bofa|countrywide).*', '.*(bank of america|countrywide).*'),
    ('CITI', '.*(citibank|citicard|citimortgage|citi card|citigroup|citifinancial|citi ).*', '.*(citibank|citimortgage|citigroup|citicorp|citifinancial).*'),
    ('AMERICAN EXPRESS', '.*(american express|amex|amcrican express).*', '.*american express.*'),
    ('CAPITAL ONE', '.*capital one.*', '.*capital one.*')
  AS t(bank, cred_re, case_re)
),
d AS (
  SELECT fd.PERSON_ID, fd.yr, b.bank, b.case_re, x.VALUE_CODE, x.CREDITOR_NAME, x.DESCRIPTION,
    (x.DESCRIPTION ILIKE ANY ('%guarant%', '%invest%', '%rental%', '%business%', '%commercial%', '%farm%', '%llc%', '%partnership%', '%second home%', '%vacation%', '%condo%')
      OR x.VALUE_CODE IN ('N', 'O') OR x.VALUE_CODE LIKE 'P%') non_ordinary
  FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DISCLOSURE_DEBTS x
  JOIN fd ON fd.ID = x.FINANCIAL_DISCLOSURE_ID
  JOIN b ON REGEXP_LIKE(x.CREDITOR_NAME, b.cred_re, 'i')
  WHERE fd.yr BETWEEN 2003 AND 2021
),
pairs AS (
  SELECT PERSON_ID, bank, case_re, yr, BOOLOR_AGG(non_ordinary) non_ordinary,
    ANY_VALUE(IFF(non_ordinary, CREDITOR_NAME || ' / ' || DESCRIPTION || ' / ' || VALUE_CODE, NULL)) non_ordinary_example,
    ANY_VALUE(CREDITOR_NAME || ' / ' || DESCRIPTION || ' / ' || VALUE_CODE) debt_example
  FROM d GROUP BY 1, 2, 3, 4
),
judges AS (SELECT DISTINCT PERSON_ID FROM pairs),
dk AS (
  SELECT k.ID docket_id, k.ASSIGNED_TO_ID, YEAR(k.DATE_FILED) fy, k.CASE_NAME, k.NATURE_OF_SUIT, k.COURT_ID
  FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS k
  JOIN judges j ON j.PERSON_ID = k.ASSIGNED_TO_ID
  WHERE k.DATE_FILED BETWEEN '2003-01-01' AND '2022-12-31' AND k.MDL_STATUS IS NULL
    AND k.CASE_NAME ILIKE ANY ('%wells fargo%', '%chase%', '%morgan%', '%bank of america%', '%countrywide%', '%citi%', '%american express%', '%capital one%')
),
hits AS (
  SELECT DISTINCT p.PERSON_ID, p.bank, p.non_ordinary, p.non_ordinary_example, p.debt_example, dk.docket_id, dk.fy, dk.CASE_NAME, dk.COURT_ID,
    REGEXP_LIKE(dk.COURT_ID, '.*b$') bankruptcy_court
  FROM dk JOIN pairs p ON p.PERSON_ID = dk.ASSIGNED_TO_ID AND dk.fy BETWEEN p.yr AND p.yr + 1 AND REGEXP_LIKE(dk.CASE_NAME, p.case_re, 'i')
),
summ AS (
  SELECT 'summary' kind,
    'dockets=' || COUNT(DISTINCT docket_id) || ' judges=' || COUNT(DISTINCT PERSON_ID)
    || ' | bankruptcy-court dockets=' || COUNT(DISTINCT IFF(bankruptcy_court, docket_id, NULL)) || ' judges=' || COUNT(DISTINCT IFF(bankruptcy_court, PERSON_ID, NULL))
    || ' | non-ordinary-debt dockets=' || COUNT(DISTINCT IFF(non_ordinary, docket_id, NULL)) || ' judges=' || COUNT(DISTINCT IFF(non_ordinary, PERSON_ID, NULL))
    || ' | non-ordinary in district courts dockets=' || COUNT(DISTINCT IFF(non_ordinary AND NOT bankruptcy_court, docket_id, NULL)) || ' judges=' || COUNT(DISTINCT IFF(non_ordinary AND NOT bankruptcy_court, PERSON_ID, NULL)) detail
  FROM hits
),
samp AS (
  SELECT 'sample' kind, h.bank || ' | ' || h.COURT_ID || ' ' || h.fy || ' | ' || LEFT(h.CASE_NAME, 70) || ' | debt: ' || LEFT(COALESCE(h.non_ordinary_example, h.debt_example), 70) || ' | judge: ' || j.NAME_LAST detail
  FROM hits h JOIN LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_JUDGES j ON j.ID = h.PERSON_ID
  WHERE h.non_ordinary AND NOT h.bankruptcy_court
  ORDER BY HASH(h.docket_id) LIMIT 12
)
SELECT * FROM summ;
