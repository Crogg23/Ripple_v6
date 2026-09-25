-- @S12 ROR status vs known closures: for-profit college chains that shut 2015-2019, is ROR still calling them active?
SELECT CASE WHEN display_name ILIKE 'Argosy University%' THEN 'Argosy (closed 2019)'
            WHEN display_name ILIKE 'ITT Technical Institute%' OR display_name ILIKE 'ITT Educational%' THEN 'ITT Tech (closed 2016)'
            WHEN display_name ILIKE 'Corinthian College%' OR display_name ILIKE 'Everest College%' OR display_name ILIKE 'Everest University%'
                 OR display_name ILIKE 'Heald College%' OR display_name ILIKE 'WyoTech%' THEN 'Corinthian chain (closed 2015)'
            WHEN display_name ILIKE 'Virginia College%' OR display_name ILIKE 'Brightwood%' THEN 'ECA chain (closed 2018)'
            WHEN display_name ILIKE 'Art Institute of%' OR display_name ILIKE 'The Art Institute%' THEN 'Art Institutes (closed 2023)'
       END chain,
       status, COUNT(*) n, MIN(display_name) name_a, MAX(display_name) name_z,
       MIN(record_created_date)::string created0, MAX(record_last_modified_date)::string modified1
FROM LIBRARY_MARTS.REFERENCE.REFERENCE__XC_ROR_RESEARCH_ORGANIZATIONS
WHERE country_code = 'US' AND chain IS NOT NULL
GROUP BY 1, 2 ORDER BY 1, 2;
