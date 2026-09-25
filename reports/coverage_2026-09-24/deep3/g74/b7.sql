-- S23 UK PSC x Companies House: companies numbered in three windows (6 Oct-16 Nov 2025, 17 Nov-21 Dec 2025, 5 Jan-1 Feb 2026). Which ones are gone from the live register, and who controlled them (nationality, UK residence, person, PSC postcode)?
WITH p AS (
  SELECT COMPANY_NUMBER, TO_NUMBER(COMPANY_NUMBER) n, KIND, UPPER(TRIM(NATIONALITY)) nat, UPPER(TRIM(COUNTRY_OF_RESIDENCE)) res, CEASED_ON,
         UPPER(REPLACE(ADDRESS_POSTAL_CODE,' ','')) ppc, REGEXP_REPLACE(UPPER(TRIM(NAME)), '^(MR|MRS|MS|MISS|DR) ', '') || ' | ' || COALESCE(DOB_YEAR::string, '') person
  FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC
  WHERE COMPANY_NUMBER RLIKE '[0-9]{8}' AND TRY_TO_NUMBER(COMPANY_NUMBER) BETWEEN 16764035 AND 17005537),
w AS (
  SELECT p.*, CASE WHEN n <= 16858916 THEN 'a_oct' WHEN n BETWEEN 16858919 AND 16924562 THEN 'b_idv5wk' WHEN n BETWEEN 16941281 AND 17005537 THEN 'c_jan' ELSE 'x' END win
  FROM p),
c AS (
  SELECT COMPANY_NUMBER FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__INTL_UK_COMPANIES_HOUSE
  WHERE COMPANY_NUMBER RLIKE '[0-9]{8}' AND TO_NUMBER(COMPANY_NUMBER) BETWEEN 16764035 AND 17005537),
co AS (
  SELECT w.COMPANY_NUMBER, w.win, IFF(c.COMPANY_NUMBER IS NULL, 'gone', 'live') st, MODE(nat) nat,
         MAX(IFF(res IN ('UNITED KINGDOM','ENGLAND','SCOTLAND','WALES','NORTHERN IRELAND','UK','GREAT BRITAIN','U.K.','BRITAIN') OR res LIKE '%ENGLAND%' OR res LIKE '%UNITED KINGDOM%', 1, 0)) ukres,
         MAX(IFF(KIND ILIKE 'individual%', 1, 0)) ind, MAX(IFF(CEASED_ON IS NOT NULL, 1, 0)) any_ceased, MODE(ppc) ppc, MODE(person) person
  FROM w LEFT JOIN c USING (COMPANY_NUMBER) WHERE win <> 'x' GROUP BY 1,2,3)
SELECT * FROM (
  SELECT 'sum' k, win, st, 'all' v, COUNT(*) cos, SUM(ukres) ukres, SUM(ind) ind, SUM(any_ceased) ceased FROM co GROUP BY 1,2,3,4
  UNION ALL SELECT 'nat', win, st, COALESCE(nat, '(none)'), COUNT(*), SUM(ukres), SUM(ind), SUM(any_ceased) FROM co GROUP BY 1,2,3,4
  UNION ALL SELECT 'person', win, st, COALESCE(person, '(none)'), COUNT(*), SUM(ukres), SUM(ind), SUM(any_ceased) FROM co GROUP BY 1,2,3,4
  UNION ALL SELECT 'ppc', win, st, COALESCE(ppc, '(none)'), COUNT(*), SUM(ukres), SUM(ind), SUM(any_ceased) FROM co GROUP BY 1,2,3,4
) QUALIFY k = 'sum' OR ROW_NUMBER() OVER (PARTITION BY k, win, st ORDER BY cos DESC) <= 15
ORDER BY k, win, st, cos DESC;
