-- S07 UK Companies House: live companies by incorporation month since 2017 (status, accounts, default address, legal form, busiest postcode), plus weeks around 18 Nov 2025 and the same weeks a year earlier
WITH t AS (
  SELECT COMPANY_NUMBER, INCORPORATION_DATE d, COMPANY_STATUS s, ACCOUNT_CATEGORY a, COMPANY_CATEGORY c, UPPER(REPLACE(POST_CODE,' ','')) pc
  FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__INTL_UK_COMPANIES_HOUSE
  WHERE INCORPORATION_DATE >= '2017-01-01'),
pm AS (SELECT DATE_TRUNC('month', d) m, pc, COUNT(*) k FROM t WHERE NULLIF(pc,'') IS NOT NULL GROUP BY 1,2),
top AS (SELECT m, MAX(k) top_pc_n, MAX_BY(pc, k) top_pc FROM pm GROUP BY 1),
agg AS (
  SELECT 'month' g, DATE_TRUNC('month', d) p, COUNT(*) n,
         COUNT_IF(s = 'Active - Proposal to Strike off') strike, COUNT_IF(s = 'Liquidation') liq,
         COUNT_IF(a = 'NO ACCOUNTS FILED') noacc, COUNT_IF(a = 'DORMANT') dormant, COUNT_IF(a = 'MICRO ENTITY') micro,
         COUNT_IF(pc = 'CF148LH') dflt, COUNT_IF(c = 'Limited Partnership') lp, COUNT_IF(c = 'Limited Liability Partnership') llp,
         COUNT_IF(c = 'Overseas Entity') oe, COUNT_IF(LEFT(COMPANY_NUMBER,2) = 'SC') sc, COUNT_IF(LEFT(COMPANY_NUMBER,2) = 'NI') ni
  FROM t GROUP BY 1,2
  UNION ALL
  SELECT 'week', DATE_TRUNC('week', d), COUNT(*),
         COUNT_IF(s = 'Active - Proposal to Strike off'), COUNT_IF(s = 'Liquidation'),
         COUNT_IF(a = 'NO ACCOUNTS FILED'), COUNT_IF(a = 'DORMANT'), COUNT_IF(a = 'MICRO ENTITY'),
         COUNT_IF(pc = 'CF148LH'), COUNT_IF(c = 'Limited Partnership'), COUNT_IF(c = 'Limited Liability Partnership'),
         COUNT_IF(c = 'Overseas Entity'), COUNT_IF(LEFT(COMPANY_NUMBER,2) = 'SC'), COUNT_IF(LEFT(COMPANY_NUMBER,2) = 'NI')
  FROM t WHERE d BETWEEN '2024-09-01' AND '2025-03-31' OR d BETWEEN '2025-09-01' AND '2026-03-31' GROUP BY 1,2)
SELECT agg.g, agg.p::date p, agg.n, agg.strike, agg.liq, agg.noacc, agg.dormant, agg.micro, agg.dflt, agg.lp, agg.llp, agg.oe, agg.sc, agg.ni,
       IFF(agg.g = 'month', top.top_pc, NULL) top_pc, IFF(agg.g = 'month', top.top_pc_n, NULL) top_pc_n
FROM agg LEFT JOIN top ON agg.g = 'month' AND top.m = agg.p
ORDER BY 1, 2;

-- S08 UK Companies House: every postcode hosting 1,000+ live companies, with strike-off, overdue-accounts, dormant, newcomer and same-day-burst counts (peer table)
WITH t AS (
  SELECT UPPER(REPLACE(POST_CODE,' ','')) pc, UPPER(TRIM(ADDRESS_LINE_1)) a1, POST_TOWN town, COMPANY_STATUS s, ACCOUNT_CATEGORY a,
         INCORPORATION_DATE d, COMPANY_CATEGORY c
  FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__INTL_UK_COMPANIES_HOUSE
  WHERE NULLIF(TRIM(POST_CODE),'') IS NOT NULL),
big AS (SELECT pc FROM t GROUP BY 1 HAVING COUNT(*) >= 1000),
day AS (SELECT t.pc, d, COUNT(*) k FROM t JOIN big USING (pc) GROUP BY 1,2),
dm AS (SELECT pc, MAX(k) maxday, MAX_BY(d, k) peakday FROM day GROUP BY 1),
agg AS (
  SELECT t.pc, COUNT(*) n, COUNT(DISTINCT a1) a1s, MODE(a1) top_a1, MODE(town) town,
         COUNT_IF(s = 'Active - Proposal to Strike off') strike, COUNT_IF(s = 'Liquidation') liq,
         COUNT_IF(d < '2024-07-01') old_n, COUNT_IF(d < '2024-07-01' AND a = 'NO ACCOUNTS FILED') old_noacc,
         COUNT_IF(a = 'DORMANT') dormant, COUNT_IF(a = 'MICRO ENTITY') micro,
         COUNT_IF(d >= '2025-01-01') new25, COUNT_IF(d >= '2025-11-18') post_idv, COUNT_IF(d BETWEEN '2024-11-18' AND '2025-06-30') prior_idv,
         COUNT_IF(c = 'Limited Partnership') lp, COUNT_IF(c = 'Overseas Entity') oe,
         MIN(d) d0, MAX(d) d1
  FROM t JOIN big USING (pc) GROUP BY 1)
SELECT agg.*, dm.maxday, dm.peakday FROM agg JOIN dm USING (pc) ORDER BY n DESC;

-- S09 Ireland CRO: companies by incorporation year, status, and share formed at addresses that host 300+ / 1,000+ companies (address = first two parts, letters and digits only)
WITH t AS (
  SELECT COMPANY_ID, YEAR(INCORPORATION_DATE) y, COMPANY_STATUS s,
         REGEXP_REPLACE(UPPER(SPLIT_PART(REGISTERED_ADDRESS, ',', 1) || SPLIT_PART(REGISTERED_ADDRESS, ',', 2)), '[^A-Z0-9]', '') a2
  FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__INTL_IE_CRO
  WHERE INCORPORATION_DATE IS NOT NULL AND INCORPORATION_DATE <> '1901-01-01' AND REGISTERED_ADDRESS NOT ILIKE '%NO ADDRESS%'),
ac AS (SELECT a2, COUNT(*) an FROM t GROUP BY 1)
SELECT y, COUNT(*) n, COUNT_IF(s = 'Normal') normal, COUNT_IF(s ILIKE 'Dissolved%') diss, COUNT_IF(s = 'Strike Off Listed') sol,
       COUNT_IF(s ILIKE 'Liquidation%') liq, COUNT_IF(an >= 300) at300, COUNT_IF(an >= 1000) at1000, COUNT(DISTINCT a2) addrs
FROM t JOIN ac USING (a2) WHERE y >= 1960 GROUP BY 1 ORDER BY 1;

-- S10 Ireland CRO: every normalised address hosting 250+ companies, with status, decade spread, 2025+ newcomers and biggest single day
WITH t AS (
  SELECT COMPANY_ID, INCORPORATION_DATE d, COMPANY_STATUS s, COMPANY_TYPE ty, REGISTERED_ADDRESS ra,
         REGEXP_REPLACE(UPPER(SPLIT_PART(REGISTERED_ADDRESS, ',', 1) || SPLIT_PART(REGISTERED_ADDRESS, ',', 2)), '[^A-Z0-9]', '') a2
  FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__INTL_IE_CRO
  WHERE REGISTERED_ADDRESS NOT ILIKE '%NO ADDRESS%'),
big AS (SELECT a2 FROM t GROUP BY 1 HAVING COUNT(*) >= 250),
day AS (SELECT t.a2, d, COUNT(*) k FROM t JOIN big USING (a2) WHERE d IS NOT NULL GROUP BY 1,2),
dm AS (SELECT a2, MAX(k) maxday, MAX_BY(d, k) peakday FROM day GROUP BY 1)
SELECT t.a2, MODE(UPPER(ra)) addr, COUNT(*) n, COUNT_IF(s = 'Normal') normal, COUNT_IF(s ILIKE 'Dissolved%') diss, COUNT_IF(s = 'Strike Off Listed') sol,
       COUNT_IF(YEAR(d) < 1990) pre1990, COUNT_IF(YEAR(d) BETWEEN 1990 AND 1999) y1990s, COUNT_IF(YEAR(d) BETWEEN 2000 AND 2014) y2000_14,
       COUNT_IF(YEAR(d) BETWEEN 2015 AND 2024) y2015_24, COUNT_IF(d >= '2025-01-01') y2025p, MIN(d) d0, MAX(d) d1, ANY_VALUE(dm.maxday) maxday, ANY_VALUE(dm.peakday) peakday
FROM t JOIN big USING (a2) JOIN dm USING (a2)
GROUP BY 1 ORDER BY n DESC;

-- S11 ICIJ entities: incorporations, inactivations and strike-offs by year, leak and jurisdiction; plus Panama Papers and Offshore Leaks formations by month 2003-2007
WITH t AS (
  SELECT SOURCE_LEAK l, JURISDICTION j, INCORPORATION_DATE i, INACTIVATION_DATE x, STRUCK_OFF_DATE so
  FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_ENTITIES)
SELECT 'inc' k, l, j, YEAR(i) p, COUNT(*) n FROM t WHERE YEAR(i) BETWEEN 1970 AND 2020 GROUP BY 1,2,3,4
UNION ALL SELECT 'inact', l, j, YEAR(x), COUNT(*) FROM t WHERE x IS NOT NULL GROUP BY 1,2,3,4
UNION ALL SELECT 'struck', l, j, YEAR(so), COUNT(*) FROM t WHERE so IS NOT NULL GROUP BY 1,2,3,4
UNION ALL SELECT 'incm', l, 'ALL', YEAR(i) * 100 + MONTH(i), COUNT(*) FROM t WHERE l IN ('Panama Papers', 'Offshore Leaks') AND i BETWEEN '2003-01-01' AND '2007-12-31' GROUP BY 1,2,3,4
ORDER BY 1, 2, 3, 4;

-- S12 ICIJ intermediaries tied to the United Kingdom: do they appear on the live UK company register (name match), and does the postcode agree?
WITH i AS (
  SELECT NODE_ID, NAME, ADDRESS, SOURCE_LEAK, STATUS, COUNTRIES,
         TRIM(REGEXP_REPLACE(REGEXP_REPLACE(UPPER(NAME), '[^A-Z0-9 ]', ''), ' (LIMITED|LTD|PLC|LLP)$', '')) nn,
         REPLACE(REGEXP_SUBSTR(UPPER(ADDRESS), '[A-Z]{1,2}[0-9][A-Z0-9]? ?[0-9][A-Z]{2}'), ' ', '') pc
  FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_INTERMEDIARIES
  WHERE COUNTRIES ILIKE '%United Kingdom%'),
c AS (
  SELECT COMPANY_NUMBER, COMPANY_NAME, UPPER(REPLACE(POST_CODE,' ','')) cpc, COMPANY_STATUS, INCORPORATION_DATE, ACCOUNT_CATEGORY, NUM_MORTGAGES_OUTSTANDING,
         TRIM(REGEXP_REPLACE(REGEXP_REPLACE(UPPER(COMPANY_NAME), '[^A-Z0-9 ]', ''), ' (LIMITED|LTD|PLC|LLP)$', '')) nn
  FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__INTL_UK_COMPANIES_HOUSE)
SELECT i.NODE_ID, i.NAME, i.SOURCE_LEAK, i.STATUS, i.COUNTRIES, i.pc, LEFT(i.ADDRESS, 120) addr,
       c.COMPANY_NUMBER, c.COMPANY_NAME, c.cpc, c.COMPANY_STATUS, c.INCORPORATION_DATE, c.ACCOUNT_CATEGORY,
       IFF(c.COMPANY_NUMBER IS NULL, NULL, IFF(i.pc = c.cpc, 1, 0)) pc_agree
FROM i LEFT JOIN c ON i.nn = c.nn AND LENGTH(i.nn) >= 4
ORDER BY pc_agree DESC NULLS LAST, i.NAME;
