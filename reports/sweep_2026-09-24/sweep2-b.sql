-- [1]
-- SAM excluded providers: distinct UEIs, and how many land in each of the five partner tables (RECIPIENT_UEI or parent UEI)
WITH ep AS (SELECT DISTINCT TRIM(UEI) u FROM LIBRARY_MARTS.HEALTH.HEALTH__SAM_EXCLUDED_PROVIDERS WHERE LENGTH(TRIM(UEI))=12)
SELECT 'EP_distinct_uei' t, COUNT(*) n FROM ep
UNION ALL SELECT 'EP_uei_in_SAM_EXCLUSIONS', COUNT(*) FROM ep WHERE u IN (SELECT TRIM(UEI) FROM LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS)
UNION ALL SELECT 'CONTRACTS_FULL_recip', COUNT(DISTINCT TRIM(RECIPIENT_UEI)) FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL WHERE TRIM(RECIPIENT_UEI) IN (SELECT u FROM ep)
UNION ALL SELECT 'CONTRACTS_FULL_parent', COUNT(DISTINCT TRIM(RECIPIENT_PARENT_UEI)) FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL WHERE TRIM(RECIPIENT_PARENT_UEI) IN (SELECT u FROM ep)
UNION ALL SELECT 'CONTRACTS_FY25_recip', COUNT(DISTINCT TRIM(RECIPIENT_UEI)) FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS WHERE TRIM(RECIPIENT_UEI) IN (SELECT u FROM ep)
UNION ALL SELECT 'BULK_rows', COUNT(*) FROM LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_USASPENDING_BULK
UNION ALL SELECT 'BULK_recip', COUNT(DISTINCT TRIM(RECIPIENT_UEI)) FROM LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_USASPENDING_BULK WHERE TRIM(RECIPIENT_UEI) IN (SELECT u FROM ep)
UNION ALL SELECT 'BULK_parent', COUNT(DISTINCT TRIM(RECIPIENT_PARENT_UEI)) FROM LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_USASPENDING_BULK WHERE TRIM(RECIPIENT_PARENT_UEI) IN (SELECT u FROM ep)
UNION ALL SELECT 'NIH_org_uei', COUNT(DISTINCT TRIM(ORG_UEI)) FROM LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_NIH_REPORTER WHERE TRIM(ORG_UEI) IN (SELECT u FROM ep)
UNION ALL SELECT 'SBIR_uei', COUNT(DISTINCT TRIM(UEI)) FROM LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_SBIR_STTR_AWARDS WHERE TRIM(UEI) IN (SELECT u FROM ep)
;

-- [2]
-- CCN: hospice CCN shape (last four digits range) and overlap with the four facility tables
WITH h AS (SELECT DISTINCT LPAD(TRIM(CCN),6,'0') c FROM LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS WHERE NULLIF(TRIM(CCN),'') IS NOT NULL),
hh AS (SELECT DISTINCT LPAD(TRIM(CCN::string),6,'0') c FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH),
nh AS (SELECT DISTINCT LPAD(TRIM(CMS_CERTIFICATION_NUMBER_CCN::string),6,'0') c FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME),
n4 AS (SELECT DISTINCT LPAD(TRIM(CMS_CERTIFICATION_NUMBER_CCN::string),6,'0') c FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_NURSINGHOME411),
pe AS (SELECT DISTINCT LPAD(TRIM(CMS_CERTIFICATION_NUMBER_CCN::string),6,'0') c FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES)
SELECT 'hospice' t, COUNT(*) n, MIN(SUBSTR(c,3,4)) lo4, MAX(SUBSTR(c,3,4)) hi4, COUNT_IF(SUBSTR(c,3,1) IN ('1')) third_digit_1, (SELECT COUNT(*) FROM LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS) rows_, NULL x FROM h
UNION ALL SELECT 'home_health', COUNT(*), MIN(SUBSTR(c,3,4)), MAX(SUBSTR(c,3,4)), COUNT_IF(c IN (SELECT c FROM h)), NULL, NULL FROM hh
UNION ALL SELECT 'nursing_home', COUNT(*), MIN(SUBSTR(c,3,4)), MAX(SUBSTR(c,3,4)), COUNT_IF(c IN (SELECT c FROM h)), NULL, NULL FROM nh
UNION ALL SELECT 'nh411', COUNT(*), MIN(SUBSTR(c,3,4)), MAX(SUBSTR(c,3,4)), COUNT_IF(c IN (SELECT c FROM h)), NULL, NULL FROM n4
UNION ALL SELECT 'nh_penalties', COUNT(*), MIN(SUBSTR(c,3,4)), MAX(SUBSTR(c,3,4)), COUNT_IF(c IN (SELECT c FROM h)), NULL, NULL FROM pe
;

-- [3]
-- CourtListener schools: EIN fill, widths, and overlap with Form 5500 EIN columns, IRS527 Schedule A and hospital officer pay
WITH s AS (SELECT DISTINCT LPAD(REGEXP_REPLACE(EIN,'[^0-9]',''),9,'0') e FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_SCHOOLS WHERE LENGTH(REGEXP_REPLACE(EIN,'[^0-9]','')) BETWEEN 7 AND 9 AND LPAD(REGEXP_REPLACE(EIN,'[^0-9]',''),9,'0')<>'000000000'),
f AS (SELECT LPAD(REGEXP_REPLACE(x,'[^0-9]',''),9,'0') e, col FROM (SELECT SPONS_DFE_EIN::string a, SPONSOR_DFE_EIN::string b, ADMIN_EIN::string c2, PREPARER_EIN::string d, LAST_RPT_SPONS_EIN::string g FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_DOL_FORM5500) UNPIVOT (x FOR col IN (a,b,c2,d,g)))
SELECT 'schools_rows' t, (SELECT COUNT(*) FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_SCHOOLS)::string n, (SELECT COUNT_IF(NULLIF(TRIM(EIN),'') IS NOT NULL) FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_SCHOOLS)::string m
UNION ALL SELECT 'schools_distinct_ein', COUNT(*)::string, NULL FROM s
UNION ALL SELECT 'f5500_'||col, COUNT(DISTINCT e)::string, NULL FROM f WHERE e IN (SELECT e FROM s) GROUP BY col
UNION ALL SELECT 'irs527A', COUNT(DISTINCT LPAD(REGEXP_REPLACE(EIN,'[^0-9]',''),9,'0'))::string, NULL FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS527_SCHEDULE_A_CONTRIBUTIONS WHERE LPAD(REGEXP_REPLACE(EIN,'[^0-9]',''),9,'0') IN (SELECT e FROM s)
UNION ALL SELECT 'hosp_officer_pay', COUNT(DISTINCT LPAD(REGEXP_REPLACE(EIN::string,'[^0-9]',''),9,'0'))::string, NULL FROM LIBRARY_MARTS.HEALTH.HEALTH__HOSPITAL_OFFICER_PAY WHERE LPAD(REGEXP_REPLACE(EIN::string,'[^0-9]',''),9,'0') IN (SELECT e FROM s)
;

-- [4]
-- Senate trades vs member tables: distinct bioguides, overlap, cycles, trade date range
SELECT 'trades' t, COUNT(DISTINCT BIOGUIDE)::string n, COUNT_IF(NULLIF(TRIM(BIOGUIDE),'') IS NULL)::string blank, MIN(TRANSACTION_DATE)::string lo, MAX(TRANSACTION_DATE)::string hi FROM LIBRARY_MARTS.FINANCE.FINANCE__SENATE_TRADES
UNION ALL SELECT 'indiv', COUNT(DISTINCT BIOGUIDE)::string, LISTAGG(DISTINCT CYCLE::string, ',')::string, LISTAGG(DISTINCT CHAMBER, ','), COUNT(DISTINCT IFF(BIOGUIDE IN (SELECT BIOGUIDE FROM LIBRARY_MARTS.FINANCE.FINANCE__SENATE_TRADES), BIOGUIDE, NULL))::string FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_INDIV_DONATIONS
UNION ALL SELECT 'raised', COUNT(DISTINCT BIOGUIDE)::string, LISTAGG(DISTINCT CYCLE::string, ',')::string, LISTAGG(DISTINCT CHAMBER, ','), COUNT(DISTINCT IFF(BIOGUIDE IN (SELECT BIOGUIDE FROM LIBRARY_MARTS.FINANCE.FINANCE__SENATE_TRADES), BIOGUIDE, NULL))::string FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_MONEY_RAISED
UNION ALL SELECT 'indiv_senate_rows', COUNT(DISTINCT BIOGUIDE)::string, NULL, NULL, NULL FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_INDIV_DONATIONS WHERE CHAMBER ILIKE 'S%'
;

-- [5]
-- EIN: OSHA case detail 2023 and 2024 vs EO BMF, IRS BMF, IRS527 Schedule B: distinct normalized EINs each side and overlap
WITH o AS (
  SELECT '2023' y, LPAD(REGEXP_REPLACE(EIN,'[^0-9]',''),9,'0') e FROM LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_CASE_DETAIL_2023 WHERE LENGTH(REGEXP_REPLACE(EIN,'[^0-9]','')) BETWEEN 7 AND 9
  UNION SELECT '2024', LPAD(REGEXP_REPLACE(EIN,'[^0-9]',''),9,'0') FROM LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_CASE_DETAIL_2024 WHERE LENGTH(REGEXP_REPLACE(EIN,'[^0-9]','')) BETWEEN 7 AND 9),
o2 AS (SELECT DISTINCT y, e FROM o WHERE e<>'000000000'),
eo AS (SELECT DISTINCT LPAD(REGEXP_REPLACE(EIN::string,'[^0-9]',''),9,'0') e FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF),
bm AS (SELECT DISTINCT LPAD(REGEXP_REPLACE(EIN::string,'[^0-9]',''),9,'0') e FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_BMF),
sb AS (SELECT DISTINCT LPAD(REGEXP_REPLACE(EIN::string,'[^0-9]',''),9,'0') e FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS527_SCHEDULE_B_EXPENDITURES)
SELECT y, COUNT(*) osha_ein, COUNT_IF(e IN (SELECT e FROM eo)) in_eo_bmf, COUNT_IF(e IN (SELECT e FROM bm)) in_irs_bmf, COUNT_IF(e IN (SELECT e FROM sb)) in_527b, (SELECT COUNT(*) FROM eo) eo_n, (SELECT COUNT(*) FROM bm) bm_n, (SELECT COUNT(*) FROM sb) sb_n FROM o2 GROUP BY y ORDER BY y
;

-- [6]
-- Docket samples: FJC IDB as carried by CourtListener
SELECT DOCKET_NUMBER, DISTRICT_ID, CIRCUIT_ID, OFFICE, DATASET_SOURCE, DATE_FILED::string df, NATURE_OF_SUIT, PLAINTIFF, DEFENDANT, AMOUNT_RECEIVED, ID, MULTIDISTRICT_LITIGATION_DOCKET_NUMBER, TRANSFER_DOCKET_NUMBER FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_FJC_IDB_CL_LINKED LIMIT 5
;

-- [7]
-- Docket samples: FJC criminal
SELECT DISTRICT, OFFICE, DOCKET, DEFENDANT_NUMBER, FILE_DATE::string fd, FISCAL_YEAR, CASE_LINK_KEY, MAGISTRATE_DOCKET, TRANSFER_DOCKET, DEFENDANT_NAME FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CRIMINAL LIMIT 5
;

-- [8]
-- Docket samples: originating court info and CourtListener dockets
SELECT 'orig' t, DOCKET_NUMBER, DOCKET_NUMBER_RAW, ID::string id, DATE_FILED::string df, ASSIGNED_TO_STR x1, NULL x2, NULL x3 FROM (SELECT * FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_ORIGINATING_COURT_INFO LIMIT 5)
UNION ALL SELECT 'dock', DOCKET_NUMBER, DOCKET_NUMBER_CORE, ID::string, DATE_FILED::string, COURT_ID, IDB_DATA_ID::string, ORIGINATING_COURT_INFORMATION_ID::string FROM (SELECT * FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS LIMIT 5)
;

-- [9]
-- FJC IDB (CourtListener copy): rows by dataset source, distinct court+office+docket, blank dockets
SELECT DATASET_SOURCE::string src, COUNT(*) n, COUNT(DISTINCT DISTRICT_ID, OFFICE, DOCKET_NUMBER) keys_, COUNT_IF(NULLIF(TRIM(DOCKET_NUMBER),'') IS NULL) blank_dkt, COUNT(DISTINCT DISTRICT_ID) courts, MIN(DATE_FILED)::string lo, MAX(DATE_FILED)::string hi, SUM(IFF(AMOUNT_RECEIVED>0,1,0)) amt_pos FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_FJC_IDB_CL_LINKED GROUP BY 1 ORDER BY 2 DESC
;

-- [10]
-- CourtListener dockets: rows, IDB_DATA_ID fill and how many land on an FJC-linked ID, originating-court id fill
SELECT COUNT(*) n, COUNT(IDB_DATA_ID) idb_filled, COUNT(DISTINCT IDB_DATA_ID) idb_distinct,
  (SELECT COUNT(*) FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_FJC_IDB_CL_LINKED l WHERE l.ID IN (SELECT IDB_DATA_ID FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS WHERE IDB_DATA_ID IS NOT NULL)) idb_lands_in_linked,
  COUNT(ORIGINATING_COURT_INFORMATION_ID) orig_filled, COUNT(DISTINCT COURT_ID) courts, COUNT_IF(NULLIF(TRIM(DOCKET_NUMBER_CORE),'') IS NOT NULL) core_filled
FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS
;

-- [11]
-- FJC linked vs FJC criminal: does office + docket + filing date line up, and which FJC district code maps to which CourtListener court (one-to-one share)
WITH l AS (SELECT DISTRICT_ID, OFFICE::string o, DOCKET_NUMBER d, DATE_FILED::date f FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_FJC_IDB_CL_LINKED GROUP BY 1,2,3,4),
c AS (SELECT DISTRICT, OFFICE::string o, DOCKET d, FILE_DATE::date f FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CRIMINAL GROUP BY 1,2,3,4),
m AS (SELECT c.DISTRICT, l.DISTRICT_ID, COUNT(*) n FROM c JOIN l ON c.o=l.o AND c.d=l.d AND c.f=l.f GROUP BY 1,2),
top AS (SELECT DISTRICT, DISTRICT_ID, n, SUM(n) OVER (PARTITION BY DISTRICT) tot, ROW_NUMBER() OVER (PARTITION BY DISTRICT ORDER BY n DESC) rk FROM m)
SELECT (SELECT COUNT(*) FROM l) l_keys, (SELECT COUNT(*) FROM c) c_keys, SUM(tot) raw_matches, SUM(n) top_map_matches, COUNT(*) fjc_districts, COUNT(DISTINCT DISTRICT_ID) cl_courts, LISTAGG(DISTRICT||'='||DISTRICT_ID, ',') WITHIN GROUP (ORDER BY DISTRICT) mapping FROM top WHERE rk=1
;

-- [12]
-- FJC criminal (district code mapped to CourtListener court) vs FJC linked: land rate by linked dataset source on court + office + docket, filing-date agreement, fine on matched vs unmatched
WITH mp AS (SELECT column1 fjc, column2 cl FROM VALUES ('00','med'),('01','mad'),('02','nhd'),('03','rid'),('04','prd'),('05','ctd'),('06','nynd'),('07','nyed'),('08','nysd'),('09','nywd'),('10','vtd'),('11','ded'),('12','njd'),('13','paed'),('14','pamd'),('15','pawd'),('16','mdd'),('17','nced'),('18','ncmd'),('19','ncwd'),('20','scd'),('22','vaed'),('23','vawd'),('24','wvnd'),('25','wvsd'),('26','alnd'),('27','almd'),('28','alsd'),('29','flnd'),('36','lawd'),('37','msnd'),('38','mssd'),('39','txnd'),('3A','flmd'),('3C','flsd'),('3E','gand'),('3G','gamd'),('3J','gasd'),('3L','laed'),('3N','lamd'),('40','txed'),('41','txsd'),('42','txwd'),('43','kyed'),('44','kywd'),('45','mied'),('46','miwd'),('47','ohnd'),('48','ohsd'),('49','tned'),('50','tnmd'),('51','tnwd'),('52','ilnd'),('53','ilcd'),('54','ilsd'),('55','innd'),('56','insd'),('57','wied'),('58','wiwd'),('60','ared'),('61','arwd'),('62','iand'),('63','iasd'),('64','mnd'),('65','moed'),('66','mowd'),('67','ned'),('68','ndd'),('69','sdd'),('7-','akd'),('70','azd'),('71','cand'),('72','caed'),('73','cacd'),('74','casd'),('75','hid'),('76','idd'),('77','mtd'),('78','nvd'),('79','ord'),('80','waed'),('81','wawd'),('82','cod'),('83','ksd'),('84','nmd'),('85','oknd'),('86','oked'),('87','okwd'),('88','utd'),('89','wyd'),('90','dcd'),('91','vid'),('93','gud'),('94','nmid')),
c AS (SELECT mp.cl court, OFFICE::string o, DOCKET d, MIN(FILE_DATE::date) f, MAX(TRY_TO_NUMBER(FINE_AMOUNT_1::string)) fine FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CRIMINAL JOIN mp ON DISTRICT=mp.fjc GROUP BY 1,2,3),
l AS (SELECT DISTRICT_ID court, OFFICE::string o, DOCKET_NUMBER d, DATASET_SOURCE::string src, MIN(DATE_FILED::date) f, MAX(AMOUNT_RECEIVED) amt FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_FJC_IDB_CL_LINKED GROUP BY 1,2,3,4)
SELECT l.src, COUNT(*) l_keys, COUNT(c.d) matched, COUNT_IF(c.f=l.f) same_date, COUNT_IF(ABS(DATEDIFF(day,c.f,l.f))<=31) within_31d, (SELECT COUNT(*) FROM c) c_keys, (SELECT COUNT(*) FROM c WHERE (court,o,d) IN (SELECT court,o,d FROM l)) c_matched, (SELECT AVG(fine) FROM c WHERE fine>0 AND (court,o,d) IN (SELECT court,o,d FROM l)) fine_avg_matched, (SELECT AVG(fine) FROM c WHERE fine>0 AND (court,o,d) NOT IN (SELECT court,o,d FROM l)) fine_avg_unmatched
FROM l LEFT JOIN c ON c.court=l.court AND c.o=l.o AND c.d=l.d GROUP BY 1 ORDER BY 2 DESC
;

-- [13]
-- CourtListener dockets IDB_DATA_ID bridge: does court, docket core and filing date agree on the linked FJC row; amount received and view count, docket-linked vs not
WITH d AS (SELECT IDB_DATA_ID id, COURT_ID, DOCKET_NUMBER_CORE core, DATE_FILED::date f, VIEW_COUNT v FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS WHERE IDB_DATA_ID IS NOT NULL)
SELECT IFF(d.id IS NULL,'fjc_no_docket','fjc_with_docket') side, COUNT(*) n, COUNT_IF(d.COURT_ID=l.DISTRICT_ID) court_agree, COUNT_IF(d.core=l.DOCKET_NUMBER) core_agree, COUNT_IF(d.f=l.DATE_FILED::date) date_agree, COUNT_IF(l.AMOUNT_RECEIVED>0) amt_pos, ROUND(AVG(IFF(l.AMOUNT_RECEIVED>0 AND l.AMOUNT_RECEIVED<9999,l.AMOUNT_RECEIVED,NULL)),1) avg_amt_k_under_cap, COUNT_IF(l.AMOUNT_RECEIVED>=9999) amt_capped, ROUND(AVG(d.v),2) avg_views, MIN(l.DATE_FILED)::string lo, MAX(l.DATE_FILED)::string hi
FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_FJC_IDB_CL_LINKED l LEFT JOIN d ON d.id=l.ID GROUP BY 1
;

-- [14]
-- CourtListener criminal dockets (-cr- in the 94 district courts) vs FJC criminal on court + office + docket core; filing date agreement
WITH mp AS (SELECT column1 fjc, column2 cl FROM VALUES ('00','med'),('01','mad'),('02','nhd'),('03','rid'),('04','prd'),('05','ctd'),('06','nynd'),('07','nyed'),('08','nysd'),('09','nywd'),('10','vtd'),('11','ded'),('12','njd'),('13','paed'),('14','pamd'),('15','pawd'),('16','mdd'),('17','nced'),('18','ncmd'),('19','ncwd'),('20','scd'),('22','vaed'),('23','vawd'),('24','wvnd'),('25','wvsd'),('26','alnd'),('27','almd'),('28','alsd'),('29','flnd'),('36','lawd'),('37','msnd'),('38','mssd'),('39','txnd'),('3A','flmd'),('3C','flsd'),('3E','gand'),('3G','gamd'),('3J','gasd'),('3L','laed'),('3N','lamd'),('40','txed'),('41','txsd'),('42','txwd'),('43','kyed'),('44','kywd'),('45','mied'),('46','miwd'),('47','ohnd'),('48','ohsd'),('49','tned'),('50','tnmd'),('51','tnwd'),('52','ilnd'),('53','ilcd'),('54','ilsd'),('55','innd'),('56','insd'),('57','wied'),('58','wiwd'),('60','ared'),('61','arwd'),('62','iand'),('63','iasd'),('64','mnd'),('65','moed'),('66','mowd'),('67','ned'),('68','ndd'),('69','sdd'),('7-','akd'),('70','azd'),('71','cand'),('72','caed'),('73','cacd'),('74','casd'),('75','hid'),('76','idd'),('77','mtd'),('78','nvd'),('79','ord'),('80','waed'),('81','wawd'),('82','cod'),('83','ksd'),('84','nmd'),('85','oknd'),('86','oked'),('87','okwd'),('88','utd'),('89','wyd'),('90','dcd'),('91','vid'),('93','gud'),('94','nmid')),
c AS (SELECT mp.cl court, OFFICE::string o, DOCKET d, MIN(FILE_DATE::date) f FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CRIMINAL JOIN mp ON DISTRICT=mp.fjc GROUP BY 1,2,3),
k AS (SELECT COURT_ID court, SPLIT_PART(DOCKET_NUMBER,':',1) o, DOCKET_NUMBER_CORE d, MIN(DATE_FILED::date) f, MAX(VIEW_COUNT) v, MAX(IFF(IDB_DATA_ID IS NULL,0,1)) has_idb FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS WHERE COURT_ID IN (SELECT cl FROM mp) AND DOCKET_NUMBER ILIKE '%-cr-%' AND DOCKET_NUMBER LIKE '%:%' GROUP BY 1,2,3)
SELECT COUNT(*) cl_cr_keys, COUNT(c.d) matched, COUNT_IF(c.f=k.f) same_date, COUNT_IF(ABS(DATEDIFF(day,c.f,k.f))<=31) within_31d, COUNT_IF(has_idb=1) cl_has_idb, (SELECT COUNT(*) FROM c) fjc_keys, (SELECT COUNT(*) FROM c WHERE f>='2000-01-01') fjc_keys_2000on, MIN(k.f)::string cl_lo, ROUND(AVG(IFF(c.d IS NULL,NULL,k.v)),2) views_matched, ROUND(AVG(IFF(c.d IS NULL,k.v,NULL)),2) views_unmatched
FROM k LEFT JOIN c ON c.court=k.court AND c.o=k.o AND c.d=k.d
;

-- [15]
-- Originating court info: reach the appeal's origin court through dockets, parse the lower docket into office + yy + seq, match to FJC linked and FJC criminal
WITH mp AS (SELECT column1 fjc, column2 cl FROM VALUES ('00','med'),('01','mad'),('02','nhd'),('03','rid'),('04','prd'),('05','ctd'),('06','nynd'),('07','nyed'),('08','nysd'),('09','nywd'),('10','vtd'),('11','ded'),('12','njd'),('13','paed'),('14','pamd'),('15','pawd'),('16','mdd'),('17','nced'),('18','ncmd'),('19','ncwd'),('20','scd'),('22','vaed'),('23','vawd'),('24','wvnd'),('25','wvsd'),('26','alnd'),('27','almd'),('28','alsd'),('29','flnd'),('36','lawd'),('37','msnd'),('38','mssd'),('39','txnd'),('3A','flmd'),('3C','flsd'),('3E','gand'),('3G','gamd'),('3J','gasd'),('3L','laed'),('3N','lamd'),('40','txed'),('41','txsd'),('42','txwd'),('43','kyed'),('44','kywd'),('45','mied'),('46','miwd'),('47','ohnd'),('48','ohsd'),('49','tned'),('50','tnmd'),('51','tnwd'),('52','ilnd'),('53','ilcd'),('54','ilsd'),('55','innd'),('56','insd'),('57','wied'),('58','wiwd'),('60','ared'),('61','arwd'),('62','iand'),('63','iasd'),('64','mnd'),('65','moed'),('66','mowd'),('67','ned'),('68','ndd'),('69','sdd'),('7-','akd'),('70','azd'),('71','cand'),('72','caed'),('73','cacd'),('74','casd'),('75','hid'),('76','idd'),('77','mtd'),('78','nvd'),('79','ord'),('80','waed'),('81','wawd'),('82','cod'),('83','ksd'),('84','nmd'),('85','oknd'),('86','oked'),('87','okwd'),('88','utd'),('89','wyd'),('90','dcd'),('91','vid'),('93','gud'),('94','nmid')),
o AS (SELECT oc.ID, oc.DOCKET_NUMBER dn, d.APPEAL_FROM_ID court FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_ORIGINATING_COURT_INFO oc LEFT JOIN (SELECT ORIGINATING_COURT_INFORMATION_ID oid, ANY_VALUE(APPEAL_FROM_ID) APPEAL_FROM_ID FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS WHERE ORIGINATING_COURT_INFORMATION_ID IS NOT NULL GROUP BY 1) d ON d.oid=oc.ID),
p AS (SELECT o.*, REGEXP_SUBSTR(dn,'^(\\d+):(\\d{2})-([a-zA-Z]{2})-(\\d+)',1,1,'e',1) off, REGEXP_SUBSTR(dn,'^(\\d+):(\\d{2})-([a-zA-Z]{2})-(\\d+)',1,1,'e',2) yy, LOWER(REGEXP_SUBSTR(dn,'^(\\d+):(\\d{2})-([a-zA-Z]{2})-(\\d+)',1,1,'e',3)) typ, REGEXP_SUBSTR(dn,'^(\\d+):(\\d{2})-([a-zA-Z]{2})-(\\d+)',1,1,'e',4) seq FROM o),
q AS (SELECT p.*, yy||LPAD(seq,5,'0') core FROM p),
l AS (SELECT DISTINCT DISTRICT_ID court, OFFICE::string o, DOCKET_NUMBER d FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_FJC_IDB_CL_LINKED),
c AS (SELECT DISTINCT mp.cl court, OFFICE::string o, DOCKET d FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CRIMINAL JOIN mp ON DISTRICT=mp.fjc)
SELECT COUNT(*) orig_rows, COUNT(court) has_court, COUNT_IF(court IN (SELECT cl FROM mp)) federal_district, COUNT_IF(court IN (SELECT cl FROM mp) AND seq IS NOT NULL) parsed, COUNT_IF(typ='cr' AND court IN (SELECT cl FROM mp)) parsed_cr,
  COUNT_IF((court,off,core) IN (SELECT court,o,d FROM l)) in_linked, COUNT_IF(typ='cr' AND (court,off,core) IN (SELECT court,o,d FROM c)) cr_in_fjc_criminal
FROM q
;

-- [16]
-- Senate trades vs member money tables, senators only: name agreement on the 60 matched, receipts and self-funding for trading vs non-trading senators
WITH t AS (SELECT BIOGUIDE, MODE(SENATOR_NAME) nm, COUNT(*) trades, MAX(TRANSACTION_DATE) last_trade FROM LIBRARY_MARTS.FINANCE.FINANCE__SENATE_TRADES GROUP BY 1),
r AS (SELECT BIOGUIDE, CYCLE, CHAMBER, FULL_NAME, TTL_RECEIPTS_GROSS FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_MONEY_RAISED),
i AS (SELECT BIOGUIDE, CYCLE, SELF_CONTRIB_15C, ITEMIZED_INDIV FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_INDIV_DONATIONS)
SELECT r.CHAMBER, r.CYCLE::string cyc, IFF(t.BIOGUIDE IS NULL,'no_trades','trades') side, COUNT(*) members, COUNT_IF(t.BIOGUIDE IS NOT NULL AND JAROWINKLER_SIMILARITY(UPPER(SPLIT_PART(t.nm,' ',-1)),UPPER(SPLIT_PART(r.FULL_NAME,',',1)))>=85) lastname_agree, ROUND(MEDIAN(r.TTL_RECEIPTS_GROSS)) med_receipts, ROUND(MEDIAN(i.SELF_CONTRIB_15C)) med_self, COUNT_IF(i.SELF_CONTRIB_15C>0) any_self, ANY_VALUE(t.nm||' / '||r.FULL_NAME) ex
FROM r LEFT JOIN t ON t.BIOGUIDE=r.BIOGUIDE LEFT JOIN i ON i.BIOGUIDE=r.BIOGUIDE AND i.CYCLE=r.CYCLE GROUP BY 1,2,3 ORDER BY 1,2,3
;

-- [17]
-- OSHA case detail 2023/2024 vs IRS EO BMF (the IRS BMF copy matched the same EINs): name and state agreement, assets and employees matched vs unmatched
WITH o AS (SELECT YEAR_FILING_FOR::string y, LPAD(REGEXP_REPLACE(EIN,'[^0-9]',''),9,'0') e, MODE(UPPER(COMPANY_NAME)) cn, MODE(UPPER(ESTABLISHMENT_NAME)) en, MODE(STATE) st, COUNT(*) cases, COUNT(DISTINCT ESTABLISHMENT_ID) sites, MAX(TRY_TO_NUMBER(ANNUAL_AVERAGE_EMPLOYEES::string)) emp, COUNT_IF(INCIDENT_OUTCOME::string='1') deaths
  FROM (SELECT YEAR_FILING_FOR, EIN, COMPANY_NAME, ESTABLISHMENT_NAME, STATE, ESTABLISHMENT_ID, ANNUAL_AVERAGE_EMPLOYEES, INCIDENT_OUTCOME FROM LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_CASE_DETAIL_2023 UNION ALL SELECT YEAR_FILING_FOR, EIN, COMPANY_NAME, ESTABLISHMENT_NAME, STATE, ESTABLISHMENT_ID, ANNUAL_AVERAGE_EMPLOYEES, INCIDENT_OUTCOME FROM LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_CASE_DETAIL_2024)
  WHERE LENGTH(REGEXP_REPLACE(EIN,'[^0-9]','')) BETWEEN 7 AND 9 AND LPAD(REGEXP_REPLACE(EIN,'[^0-9]',''),9,'0')<>'000000000' GROUP BY 1,2),
b AS (SELECT LPAD(REGEXP_REPLACE(EIN::string,'[^0-9]',''),9,'0') e, UPPER(ORG_NAME) bn, STATE bst, TRY_TO_NUMBER(ASSET_AMT::string) assets, SUBSECTION_CODE::string sub FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF QUALIFY ROW_NUMBER() OVER (PARTITION BY 1 ORDER BY 1)=1)
SELECT o.y, IFF(b.e IS NULL,'unmatched','matched') side, COUNT(*) eins, COUNT_IF(o.st=b.bst) state_agree, COUNT_IF(GREATEST(JAROWINKLER_SIMILARITY(o.cn,b.bn),JAROWINKLER_SIMILARITY(o.en,b.bn))>=85) name_agree, SUM(cases) cases, SUM(deaths) deaths, ROUND(MEDIAN(emp)) med_emp, ROUND(MEDIAN(cases/NULLIF(emp,0))*100,2) med_cases_per100emp, ROUND(MEDIAN(assets)) med_assets, MODE(sub) top_subsection
FROM o LEFT JOIN b ON b.e=o.e GROUP BY 1,2 ORDER BY 1,2
;

-- [18]
-- OSHA x EO BMF: top 15 matched nonprofits by 2023+2024 cases, with deaths, sites and assets
WITH o AS (SELECT LPAD(REGEXP_REPLACE(EIN,'[^0-9]',''),9,'0') e, MODE(UPPER(COMPANY_NAME)) cn, COUNT(*) cases, COUNT(DISTINCT ESTABLISHMENT_ID) sites, COUNT_IF(INCIDENT_OUTCOME::string='1') deaths, LISTAGG(DISTINCT YEAR_FILING_FOR::string, ',') yrs
  FROM (SELECT YEAR_FILING_FOR, EIN, COMPANY_NAME, ESTABLISHMENT_ID, INCIDENT_OUTCOME FROM LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_CASE_DETAIL_2023 UNION ALL SELECT YEAR_FILING_FOR, EIN, COMPANY_NAME, ESTABLISHMENT_ID, INCIDENT_OUTCOME FROM LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_CASE_DETAIL_2024)
  WHERE LENGTH(REGEXP_REPLACE(EIN,'[^0-9]','')) BETWEEN 7 AND 9 AND LPAD(REGEXP_REPLACE(EIN,'[^0-9]',''),9,'0')<>'000000000' GROUP BY 1)
SELECT o.e, o.cn, b.ORG_NAME, b.STATE, b.SUBSECTION_CODE::string sub, o.cases, o.deaths, o.sites, o.yrs, TRY_TO_NUMBER(b.ASSET_AMT::string) assets FROM o JOIN LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF b ON LPAD(REGEXP_REPLACE(b.EIN::string,'[^0-9]',''),9,'0')=o.e ORDER BY o.cases DESC LIMIT 15
;

-- [19]
-- EO BMF vs IRS BMF: are they the same list
SELECT COUNT(*) eo_ein, COUNT_IF(e IN (SELECT LPAD(REGEXP_REPLACE(EIN::string,'[^0-9]',''),9,'0') FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_BMF)) in_irs_bmf FROM (SELECT DISTINCT LPAD(REGEXP_REPLACE(EIN::string,'[^0-9]',''),9,'0') e FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF)
;

-- [20]
-- CourtListener schools EIN matches in Form 5500 (sponsor EIN) and hospital officer pay: names side by side
WITH s AS (SELECT LPAD(REGEXP_REPLACE(EIN,'[^0-9]',''),9,'0') e, MODE(NAME) sn, COUNT(*) n FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_SCHOOLS WHERE LENGTH(REGEXP_REPLACE(EIN,'[^0-9]','')) BETWEEN 7 AND 9 GROUP BY 1),
f AS (SELECT LPAD(REGEXP_REPLACE(SPONS_DFE_EIN::string,'[^0-9]',''),9,'0') e, MODE(SPONSOR_DFE_NAME) fn, SUM(TRY_TO_NUMBER(TOT_ACTIVE_PARTCP_CNT::string)) partcp FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_DOL_FORM5500 GROUP BY 1),
h AS (SELECT LPAD(REGEXP_REPLACE(EIN::string,'[^0-9]',''),9,'0') e, MODE(FILER_NAME) hn, MAX(TRY_TO_NUMBER(OTHER_COMPENSATION::string)) max_other FROM LIBRARY_MARTS.HEALTH.HEALTH__HOSPITAL_OFFICER_PAY GROUP BY 1)
SELECT 'f5500' src, COUNT(*) n, COUNT_IF(JAROWINKLER_SIMILARITY(UPPER(s.sn),UPPER(f.fn))>=85) name_agree, COUNT_IF(UPPER(f.fn) LIKE '%UNIVERSITY%' OR UPPER(f.fn) LIKE '%COLLEGE%' OR UPPER(f.fn) LIKE '%SCHOOL%') edu_name, LISTAGG(s.sn||' = '||f.fn, ' | ') WITHIN GROUP (ORDER BY f.partcp DESC) ex FROM s JOIN f ON f.e=s.e
UNION ALL SELECT 'hop', COUNT(*), COUNT_IF(JAROWINKLER_SIMILARITY(UPPER(s.sn),UPPER(h.hn))>=85), COUNT_IF(UPPER(h.hn) LIKE '%UNIVERSITY%' OR UPPER(h.hn) LIKE '%COLLEGE%'), LISTAGG(s.sn||' = '||h.hn, ' | ') FROM s JOIN h ON h.e=s.e
;

-- [21]
-- OSHA case detail 2023/2024 vs IRS EO BMF (the IRS BMF copy matched the same EINs): name and state agreement, assets and employees matched vs unmatched
WITH o AS (SELECT YEAR_FILING_FOR::string y, LPAD(REGEXP_REPLACE(EIN,'[^0-9]',''),9,'0') e, MODE(UPPER(COMPANY_NAME)) cn, MODE(UPPER(ESTABLISHMENT_NAME)) en, MODE(STATE) st, COUNT(*) cases, COUNT(DISTINCT ESTABLISHMENT_ID) sites, MAX(TRY_TO_NUMBER(ANNUAL_AVERAGE_EMPLOYEES::string)) emp, COUNT_IF(INCIDENT_OUTCOME::string='1') deaths
  FROM (SELECT '2023' YEAR_FILING_FOR, EIN, COMPANY_NAME, ESTABLISHMENT_NAME, STATE, ESTABLISHMENT_ID, ANNUAL_AVERAGE_EMPLOYEES, INCIDENT_OUTCOME FROM LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_CASE_DETAIL_2023 UNION ALL SELECT '2024', EIN, COMPANY_NAME, ESTABLISHMENT_NAME, STATE, ESTABLISHMENT_ID, ANNUAL_AVERAGE_EMPLOYEES, INCIDENT_OUTCOME FROM LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_CASE_DETAIL_2024)
  WHERE LENGTH(REGEXP_REPLACE(EIN,'[^0-9]','')) BETWEEN 7 AND 9 AND LPAD(REGEXP_REPLACE(EIN,'[^0-9]',''),9,'0')<>'000000000' GROUP BY 1,2),
b AS (SELECT LPAD(REGEXP_REPLACE(EIN::string,'[^0-9]',''),9,'0') e, UPPER(ORG_NAME) bn, STATE bst, TRY_TO_NUMBER(ASSET_AMT::string) assets, SUBSECTION_CODE::string sub FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF QUALIFY ROW_NUMBER() OVER (PARTITION BY 1 ORDER BY 1)=1)
SELECT o.y, IFF(b.e IS NULL,'unmatched','matched') side, COUNT(*) eins, COUNT_IF(o.st=b.bst) state_agree, COUNT_IF(GREATEST(JAROWINKLER_SIMILARITY(o.cn,b.bn),JAROWINKLER_SIMILARITY(o.en,b.bn))>=85) name_agree, SUM(cases) cases, SUM(deaths) deaths, ROUND(MEDIAN(emp)) med_emp, ROUND(MEDIAN(cases/NULLIF(emp,0))*100,2) med_cases_per100emp, ROUND(MEDIAN(assets)) med_assets, MODE(sub) top_subsection
FROM o LEFT JOIN b ON b.e=o.e GROUP BY 1,2 ORDER BY 1,2
;

-- [22]
-- OSHA x EO BMF: top 15 matched nonprofits by 2023+2024 cases, with deaths, sites and assets
WITH o AS (SELECT LPAD(REGEXP_REPLACE(EIN,'[^0-9]',''),9,'0') e, MODE(UPPER(COMPANY_NAME)) cn, COUNT(*) cases, COUNT(DISTINCT ESTABLISHMENT_ID) sites, COUNT_IF(INCIDENT_OUTCOME::string='1') deaths, LISTAGG(DISTINCT YEAR_FILING_FOR::string, ',') yrs
  FROM (SELECT '2023' YEAR_FILING_FOR, EIN, COMPANY_NAME, ESTABLISHMENT_ID, INCIDENT_OUTCOME FROM LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_CASE_DETAIL_2023 UNION ALL SELECT '2024', EIN, COMPANY_NAME, ESTABLISHMENT_ID, INCIDENT_OUTCOME FROM LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_CASE_DETAIL_2024)
  WHERE LENGTH(REGEXP_REPLACE(EIN,'[^0-9]','')) BETWEEN 7 AND 9 AND LPAD(REGEXP_REPLACE(EIN,'[^0-9]',''),9,'0')<>'000000000' GROUP BY 1)
SELECT o.e, o.cn, b.ORG_NAME, b.STATE, b.SUBSECTION_CODE::string sub, o.cases, o.deaths, o.sites, o.yrs, TRY_TO_NUMBER(b.ASSET_AMT::string) assets FROM o JOIN LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF b ON LPAD(REGEXP_REPLACE(b.EIN::string,'[^0-9]',''),9,'0')=o.e ORDER BY o.cases DESC LIMIT 15
;

-- [23]
-- Senate trades: full-name agreement for senators matched to the member money table
WITH t AS (SELECT BIOGUIDE, MODE(SENATOR_NAME) nm FROM LIBRARY_MARTS.FINANCE.FINANCE__SENATE_TRADES GROUP BY 1),
r AS (SELECT BIOGUIDE, ANY_VALUE(FULL_NAME) fn FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_MONEY_RAISED GROUP BY 1)
SELECT COUNT(*) matched, COUNT_IF(JAROWINKLER_SIMILARITY(UPPER(t.nm),UPPER(r.fn))>=85) name_agree, LISTAGG(IFF(JAROWINKLER_SIMILARITY(UPPER(t.nm),UPPER(r.fn))<85, t.nm||' / '||r.fn, NULL), ' | ') misses FROM t JOIN r ON r.BIOGUIDE=t.BIOGUIDE
;

-- [24]
-- (rerun, fixed dedupe) OSHA case detail 2023/2024 vs IRS EO BMF (the IRS BMF copy matched the same EINs): name and state agreement, assets and employees matched vs unmatched
WITH o AS (SELECT YEAR_FILING_FOR::string y, LPAD(REGEXP_REPLACE(EIN,'[^0-9]',''),9,'0') e, MODE(UPPER(COMPANY_NAME)) cn, MODE(UPPER(ESTABLISHMENT_NAME)) en, MODE(STATE) st, COUNT(*) cases, COUNT(DISTINCT ESTABLISHMENT_ID) sites, MAX(TRY_TO_NUMBER(ANNUAL_AVERAGE_EMPLOYEES::string)) emp, COUNT_IF(INCIDENT_OUTCOME::string='1') deaths
  FROM (SELECT '2023' YEAR_FILING_FOR, EIN, COMPANY_NAME, ESTABLISHMENT_NAME, STATE, ESTABLISHMENT_ID, ANNUAL_AVERAGE_EMPLOYEES, INCIDENT_OUTCOME FROM LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_CASE_DETAIL_2023 UNION ALL SELECT '2024', EIN, COMPANY_NAME, ESTABLISHMENT_NAME, STATE, ESTABLISHMENT_ID, ANNUAL_AVERAGE_EMPLOYEES, INCIDENT_OUTCOME FROM LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_CASE_DETAIL_2024)
  WHERE LENGTH(REGEXP_REPLACE(EIN,'[^0-9]','')) BETWEEN 7 AND 9 AND LPAD(REGEXP_REPLACE(EIN,'[^0-9]',''),9,'0')<>'000000000' GROUP BY 1,2),
b AS (SELECT LPAD(REGEXP_REPLACE(EIN::string,'[^0-9]',''),9,'0') e, UPPER(ORG_NAME) bn, STATE bst, TRY_TO_NUMBER(ASSET_AMT::string) assets, SUBSECTION_CODE::string sub FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF QUALIFY ROW_NUMBER() OVER (PARTITION BY LPAD(REGEXP_REPLACE(EIN::string,'[^0-9]',''),9,'0') ORDER BY TRY_TO_NUMBER(ASSET_AMT::string) DESC NULLS LAST)=1)
SELECT o.y, IFF(b.e IS NULL,'unmatched','matched') side, COUNT(*) eins, COUNT_IF(o.st=b.bst) state_agree, COUNT_IF(GREATEST(JAROWINKLER_SIMILARITY(o.cn,b.bn),JAROWINKLER_SIMILARITY(o.en,b.bn))>=85) name_agree, SUM(cases) cases, SUM(deaths) deaths, ROUND(MEDIAN(emp)) med_emp, ROUND(MEDIAN(cases/NULLIF(emp,0))*100,2) med_cases_per100emp, ROUND(MEDIAN(assets)) med_assets, MODE(sub) top_subsection
FROM o LEFT JOIN b ON b.e=o.e GROUP BY 1,2 ORDER BY 1,2
;

-- [25]
-- SAM excluded providers x CONTRACTS_FULL (capped table): EP rows' ban windows taken from SAM_EXCLUSIONS by SAM_NUMBER; in-window actions split into base awards (mod 0) and mods; top 12 by base-award dollars in window
WITH x AS (SELECT TRIM(UEI) uei, ACTIVATION_DATE::date act, COALESCE(TERMINATION_DATE,'2999-12-31'::date) term, UPPER(COALESCE(ENTITY_NAME, FIRST_NAME||' '||LAST_NAME)) nm, EXCLUDING_AGENCY ag FROM LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS WHERE LENGTH(TRIM(UEI))=12 AND SAM_NUMBER IN (SELECT SAM_NUMBER FROM LIBRARY_MARTS.HEALTH.HEALTH__SAM_EXCLUDED_PROVIDERS)),
t AS (SELECT CONTRACT_TRANSACTION_UNIQUE_KEY k, TRY_TO_DATE(ACTION_DATE::string) d, TRY_TO_NUMBER(FEDERAL_ACTION_OBLIGATION::string,38,2) amt, TRIM(RECIPIENT_UEI) u, UPPER(RECIPIENT_NAME) rn, TRIM(MODIFICATION_NUMBER::string) modn, AWARDING_AGENCY_NAME aa FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL WHERE TRIM(RECIPIENT_UEI) IN (SELECT uei FROM x)),
tf AS (SELECT t.k, ANY_VALUE(t.u) u, ANY_VALUE(t.rn) rn, ANY_VALUE(t.d) d, ANY_VALUE(t.amt) amt, ANY_VALUE(t.modn) modn, ANY_VALUE(t.aa) aa, COUNT(x.uei) inwin, MIN(x.act) act, ANY_VALUE(x.nm) xnm, ANY_VALUE(x.ag) xag FROM t LEFT JOIN x ON x.uei=t.u AND t.d BETWEEN x.act AND x.term GROUP BY 1),
per AS (SELECT u, ANY_VALUE(rn) rn, MAX(xnm) xnm, MAX(xag) xag, MIN(act) act, COUNT(*) n, SUM(amt) amt, COUNT_IF(inwin>0) n_in, SUM(IFF(inwin>0 AND modn IN ('0','00','000','P00000'),amt,0)) base_in, SUM(IFF(inwin>0 AND modn NOT IN ('0','00','000','P00000') AND amt>0,amt,0)) mod_pos_in, MAX(IFF(inwin>0,d,NULL)) last_in, LISTAGG(DISTINCT IFF(inwin>0,aa,NULL), ',') ags FROM tf GROUP BY 1)
SELECT * FROM (SELECT 'SUMMARY' u, NULL rn, NULL xnm, NULL xag, NULL act, COUNT(*)::string n, ROUND(SUM(amt))::string amt, COUNT_IF(n_in>0)::string n_in, ROUND(SUM(base_in))::string base_in, ROUND(SUM(mod_pos_in))::string mod_pos_in, COUNT_IF(base_in>0)::string last_in, (SELECT LISTAGG(DISTINCT modn, ',') FROM (SELECT modn FROM t LIMIT 2000)) ags FROM per)
UNION ALL SELECT * FROM (SELECT u, rn, xnm, xag, act::string, n::string, ROUND(amt)::string, n_in::string, ROUND(base_in)::string, ROUND(mod_pos_in)::string, last_in::string, ags FROM per WHERE n_in>0 ORDER BY base_in DESC, mod_pos_in DESC LIMIT 12)
;

-- [26]
-- SAM excluded providers x CONTRACTS (FY2025): same split
WITH x AS (SELECT TRIM(UEI) uei, ACTIVATION_DATE::date act, COALESCE(TERMINATION_DATE,'2999-12-31'::date) term, UPPER(COALESCE(ENTITY_NAME, FIRST_NAME||' '||LAST_NAME)) nm, EXCLUDING_AGENCY ag FROM LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS WHERE LENGTH(TRIM(UEI))=12 AND SAM_NUMBER IN (SELECT SAM_NUMBER FROM LIBRARY_MARTS.HEALTH.HEALTH__SAM_EXCLUDED_PROVIDERS)),
t AS (SELECT CONTRACT_TRANSACTION_UNIQUE_KEY k, TRY_TO_DATE(ACTION_DATE::string) d, TRY_TO_NUMBER(FEDERAL_ACTION_OBLIGATION::string,38,2) amt, TRIM(RECIPIENT_UEI) u, UPPER(RECIPIENT_NAME) rn, TRIM(MODIFICATION_NUMBER::string) modn, AWARDING_AGENCY_NAME aa FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS WHERE TRIM(RECIPIENT_UEI) IN (SELECT uei FROM x)),
tf AS (SELECT t.k, ANY_VALUE(t.u) u, ANY_VALUE(t.rn) rn, ANY_VALUE(t.d) d, ANY_VALUE(t.amt) amt, ANY_VALUE(t.modn) modn, ANY_VALUE(t.aa) aa, COUNT(x.uei) inwin, MIN(x.act) act, ANY_VALUE(x.nm) xnm, ANY_VALUE(x.ag) xag FROM t LEFT JOIN x ON x.uei=t.u AND t.d BETWEEN x.act AND x.term GROUP BY 1),
per AS (SELECT u, ANY_VALUE(rn) rn, MAX(xnm) xnm, MAX(xag) xag, MIN(act) act, COUNT(*) n, SUM(amt) amt, COUNT_IF(inwin>0) n_in, SUM(IFF(inwin>0 AND modn IN ('0','00','000','P00000'),amt,0)) base_in, SUM(IFF(inwin>0 AND modn NOT IN ('0','00','000','P00000') AND amt>0,amt,0)) mod_pos_in, MAX(IFF(inwin>0,d,NULL)) last_in, LISTAGG(DISTINCT IFF(inwin>0,aa,NULL), ',') ags FROM tf GROUP BY 1)
SELECT * FROM (SELECT 'SUMMARY' u, NULL rn, NULL xnm, NULL xag, NULL act, COUNT(*)::string n, ROUND(SUM(amt))::string amt, COUNT_IF(n_in>0)::string n_in, ROUND(SUM(base_in))::string base_in, ROUND(SUM(mod_pos_in))::string mod_pos_in, COUNT_IF(base_in>0)::string last_in, NULL ags FROM per)
UNION ALL SELECT * FROM (SELECT u, rn, xnm, xag, act::string, n::string, ROUND(amt)::string, n_in::string, ROUND(base_in)::string, ROUND(mod_pos_in)::string, last_in::string, ags FROM per WHERE n_in>0 ORDER BY base_in DESC, mod_pos_in DESC LIMIT 12)
;

-- [27]
-- SAM excluded providers x SBIR and x USAspending BULK sample: which firms, address, award years vs exclusion date
WITH x AS (SELECT TRIM(UEI) uei, MIN(ACTIVATION_DATE::date) act, ANY_VALUE(EXCLUDING_AGENCY) ag, ANY_VALUE(UPPER(COALESCE(ENTITY_NAME, FIRST_NAME||' '||LAST_NAME))) nm FROM LIBRARY_MARTS.HEALTH.HEALTH__SAM_EXCLUDED_PROVIDERS WHERE LENGTH(TRIM(UEI))=12 GROUP BY 1)
SELECT 'SBIR' src, s.UEI u, x.nm, ANY_VALUE(s.COMPANY) co, ANY_VALUE(s.ADDRESS1||', '||s.CITY||' '||s.STATE) addr, x.ag, x.act::string act, COUNT(*) n, ROUND(SUM(TRY_TO_NUMBER(s.AWARD_AMOUNT::string,38,2))) amt, MIN(s.AWARD_YEAR)::string lo, MAX(s.AWARD_YEAR)::string hi, COUNT_IF(TRY_TO_DATE(s.PROPOSAL_AWARD_DATE::string)>=x.act) after_ban
FROM LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_SBIR_STTR_AWARDS s JOIN x ON x.uei=TRIM(s.UEI) GROUP BY 1,2,3,6,7
UNION ALL
SELECT 'BULK', b.RECIPIENT_UEI, x.nm, ANY_VALUE(b.RECIPIENT_NAME), NULL, x.ag, x.act::string, COUNT(*), ROUND(SUM(TRY_TO_NUMBER(b.FEDERAL_ACTION_OBLIGATION::string,38,2))), MIN(b.ACTION_DATE)::string, MAX(b.ACTION_DATE)::string, COUNT_IF(TRY_TO_DATE(b.ACTION_DATE::string)>=x.act)
FROM LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_USASPENDING_BULK b JOIN x ON x.uei=TRIM(b.RECIPIENT_UEI) GROUP BY 1,2,3,6,7
ORDER BY 1, 9 DESC
;

-- [28]
-- (rerun, row key) SAM excluded providers x CONTRACTS (FY2025): same split
WITH x AS (SELECT TRIM(UEI) uei, ACTIVATION_DATE::date act, COALESCE(TERMINATION_DATE,'2999-12-31'::date) term, UPPER(COALESCE(ENTITY_NAME, FIRST_NAME||' '||LAST_NAME)) nm, EXCLUDING_AGENCY ag FROM LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS WHERE LENGTH(TRIM(UEI))=12 AND SAM_NUMBER IN (SELECT SAM_NUMBER FROM LIBRARY_MARTS.HEALTH.HEALTH__SAM_EXCLUDED_PROVIDERS)),
t AS (SELECT SEQ8() k, TRY_TO_DATE(ACTION_DATE::string) d, TRY_TO_NUMBER(FEDERAL_ACTION_OBLIGATION::string,38,2) amt, TRIM(RECIPIENT_UEI) u, UPPER(RECIPIENT_NAME) rn, TRIM(MODIFICATION_NUMBER::string) modn, AWARDING_AGENCY_NAME aa FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS WHERE TRIM(RECIPIENT_UEI) IN (SELECT uei FROM x)),
tf AS (SELECT t.k, ANY_VALUE(t.u) u, ANY_VALUE(t.rn) rn, ANY_VALUE(t.d) d, ANY_VALUE(t.amt) amt, ANY_VALUE(t.modn) modn, ANY_VALUE(t.aa) aa, COUNT(x.uei) inwin, MIN(x.act) act, ANY_VALUE(x.nm) xnm, ANY_VALUE(x.ag) xag FROM t LEFT JOIN x ON x.uei=t.u AND t.d BETWEEN x.act AND x.term GROUP BY 1),
per AS (SELECT u, ANY_VALUE(rn) rn, MAX(xnm) xnm, MAX(xag) xag, MIN(act) act, COUNT(*) n, SUM(amt) amt, COUNT_IF(inwin>0) n_in, SUM(IFF(inwin>0 AND modn IN ('0','00','000','P00000'),amt,0)) base_in, SUM(IFF(inwin>0 AND modn NOT IN ('0','00','000','P00000') AND amt>0,amt,0)) mod_pos_in, MAX(IFF(inwin>0,d,NULL)) last_in, LISTAGG(DISTINCT IFF(inwin>0,aa,NULL), ',') ags FROM tf GROUP BY 1)
SELECT * FROM (SELECT 'SUMMARY' u, NULL rn, NULL xnm, NULL xag, NULL act, COUNT(*)::string n, ROUND(SUM(amt))::string amt, COUNT_IF(n_in>0)::string n_in, ROUND(SUM(base_in))::string base_in, ROUND(SUM(mod_pos_in))::string mod_pos_in, COUNT_IF(base_in>0)::string last_in, NULL ags FROM per)
UNION ALL SELECT * FROM (SELECT u, rn, xnm, xag, act::string, n::string, ROUND(amt)::string, n_in::string, ROUND(base_in)::string, ROUND(mod_pos_in)::string, last_in::string, ags FROM per WHERE n_in>0 ORDER BY base_in DESC, mod_pos_in DESC LIMIT 12)
;

-- [29]
-- (rerun) SAM excluded providers x CONTRACTS (FY2025): no mod number, so 'new' = award period of performance starts on or after the ban
WITH x AS (SELECT TRIM(UEI) uei, ACTIVATION_DATE::date act, COALESCE(TERMINATION_DATE,'2999-12-31'::date) term, UPPER(COALESCE(ENTITY_NAME, FIRST_NAME||' '||LAST_NAME)) nm, EXCLUDING_AGENCY ag FROM LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS WHERE LENGTH(TRIM(UEI))=12 AND SAM_NUMBER IN (SELECT SAM_NUMBER FROM LIBRARY_MARTS.HEALTH.HEALTH__SAM_EXCLUDED_PROVIDERS)),
t AS (SELECT SEQ8() k, TRY_TO_DATE(ACTION_DATE::string) d, TRY_TO_NUMBER(FEDERAL_ACTION_OBLIGATION::string,38,2) amt, TRIM(RECIPIENT_UEI) u, UPPER(RECIPIENT_NAME) rn, TRY_TO_DATE(PERIOD_OF_PERFORMANCE_START_DATE::string) pop, AWARDING_AGENCY_NAME aa FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS WHERE TRIM(RECIPIENT_UEI) IN (SELECT uei FROM x)),
tf AS (SELECT t.k, ANY_VALUE(t.u) u, ANY_VALUE(t.rn) rn, ANY_VALUE(t.d) d, ANY_VALUE(t.amt) amt, ANY_VALUE(t.pop) pop, ANY_VALUE(t.aa) aa, COUNT(x.uei) inwin, MIN(x.act) act, ANY_VALUE(x.nm) xnm, ANY_VALUE(x.ag) xag FROM t LEFT JOIN x ON x.uei=t.u AND t.d BETWEEN x.act AND x.term GROUP BY 1),
per AS (SELECT u, ANY_VALUE(rn) rn, MAX(xnm) xnm, MAX(xag) xag, MIN(act) act, COUNT(*) n, SUM(amt) amt, COUNT_IF(inwin>0) n_in, SUM(IFF(inwin>0 AND pop>=act AND amt>0,amt,0)) base_in, SUM(IFF(inwin>0 AND (pop<act OR pop IS NULL) AND amt>0,amt,0)) mod_pos_in, MAX(IFF(inwin>0,d,NULL)) last_in, LISTAGG(DISTINCT IFF(inwin>0,aa,NULL), ',') ags FROM tf GROUP BY 1)
SELECT * FROM (SELECT 'SUMMARY' u, NULL rn, NULL xnm, NULL xag, NULL act, COUNT(*)::string n, ROUND(SUM(amt))::string amt, COUNT_IF(n_in>0)::string n_in, ROUND(SUM(base_in))::string base_in, ROUND(SUM(mod_pos_in))::string mod_pos_in, COUNT_IF(base_in>0)::string last_in, NULL ags FROM per)
UNION ALL SELECT * FROM (SELECT u, rn, xnm, xag, act::string, n::string, ROUND(amt)::string, n_in::string, ROUND(base_in)::string, ROUND(mod_pos_in)::string, last_in::string, ags FROM per WHERE n_in>0 ORDER BY base_in DESC, mod_pos_in DESC LIMIT 12)
;

-- [30]
-- FJC criminal cases matched to the CourtListener FJC copy (dataset source 4 only) by filing year band; fine on matched vs unmatched, cap value excluded
WITH mp AS (SELECT column1 fjc, column2 cl FROM VALUES ('00','med'),('01','mad'),('02','nhd'),('03','rid'),('04','prd'),('05','ctd'),('06','nynd'),('07','nyed'),('08','nysd'),('09','nywd'),('10','vtd'),('11','ded'),('12','njd'),('13','paed'),('14','pamd'),('15','pawd'),('16','mdd'),('17','nced'),('18','ncmd'),('19','ncwd'),('20','scd'),('22','vaed'),('23','vawd'),('24','wvnd'),('25','wvsd'),('26','alnd'),('27','almd'),('28','alsd'),('29','flnd'),('36','lawd'),('37','msnd'),('38','mssd'),('39','txnd'),('3A','flmd'),('3C','flsd'),('3E','gand'),('3G','gamd'),('3J','gasd'),('3L','laed'),('3N','lamd'),('40','txed'),('41','txsd'),('42','txwd'),('43','kyed'),('44','kywd'),('45','mied'),('46','miwd'),('47','ohnd'),('48','ohsd'),('49','tned'),('50','tnmd'),('51','tnwd'),('52','ilnd'),('53','ilcd'),('54','ilsd'),('55','innd'),('56','insd'),('57','wied'),('58','wiwd'),('60','ared'),('61','arwd'),('62','iand'),('63','iasd'),('64','mnd'),('65','moed'),('66','mowd'),('67','ned'),('68','ndd'),('69','sdd'),('7-','akd'),('70','azd'),('71','cand'),('72','caed'),('73','cacd'),('74','casd'),('75','hid'),('76','idd'),('77','mtd'),('78','nvd'),('79','ord'),('80','waed'),('81','wawd'),('82','cod'),('83','ksd'),('84','nmd'),('85','oknd'),('86','oked'),('87','okwd'),('88','utd'),('89','wyd'),('90','dcd'),('91','vid'),('93','gud'),('94','nmid')),
c AS (SELECT mp.cl court, OFFICE::string o, DOCKET d, MIN(FILE_DATE::date) f, MAX(TRY_TO_NUMBER(FINE_AMOUNT_1::string)) fine FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CRIMINAL JOIN mp ON DISTRICT=mp.fjc GROUP BY 1,2,3),
l AS (SELECT DISTINCT DISTRICT_ID court, OFFICE::string o, DOCKET_NUMBER d FROM LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_FJC_IDB_CL_LINKED WHERE DATASET_SOURCE::string='4')
SELECT FLOOR(YEAR(c.f)/5)*5 yr5, COUNT(*) fjc_cases, COUNT(l.d) in_cl_copy, ROUND(COUNT(l.d)/COUNT(*)*100,1) pct, COUNT_IF(fine>0 AND fine<99999999 AND l.d IS NOT NULL) fined_m, ROUND(AVG(IFF(fine>0 AND fine<99999999 AND l.d IS NOT NULL,fine,NULL))) avg_fine_m, COUNT_IF(fine>0 AND fine<99999999 AND l.d IS NULL) fined_u, ROUND(AVG(IFF(fine>0 AND fine<99999999 AND l.d IS NULL,fine,NULL))) avg_fine_u
FROM c LEFT JOIN l ON l.court=c.court AND l.o=c.o AND l.d=c.d GROUP BY 1 ORDER BY 1
;

