-- S17 Pub 78 vs the IRS master file: does the master file agree gifts are deductible? status x subsection x deductibility code
WITH p AS (SELECT LPAD(REGEXP_REPLACE(EIN, '[^0-9]', ''), 9, '0') ein, DEDUCTIBILITY_STATUS st
           FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_PUB78_ELIGIBLE_DONEES),
b AS (SELECT LPAD(REGEXP_REPLACE(EIN, '[^0-9]', ''), 9, '0') ein, MAX(SUBSECTION_CODE) sub, MAX(DEDUCTIBILITY_CODE) dc, MAX(STATUS_CODE) sc, MAX(FOUNDATION_CODE) fc
      FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF GROUP BY 1)
SELECT p.st, b.sub, b.dc, b.sc, COUNT(*) n, COUNT_IF(b.fc IN ('02', '03', '04')) bmf_pf_codes
FROM p LEFT JOIN b ON p.ein = b.ein
GROUP BY 1, 2, 3, 4 ORDER BY n DESC;
