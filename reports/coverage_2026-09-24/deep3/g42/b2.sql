-- @S09 ROR exact name repeats: the glance used APPROX_TOP_K; count the top names exactly
SELECT display_name, COUNT(*) n, COUNT(DISTINCT country_code) countries, COUNT(DISTINCT ror_id) rors,
       LISTAGG(DISTINCT country_code, ',') WITHIN GROUP (ORDER BY country_code) country_list
FROM LIBRARY_MARTS.REFERENCE.REFERENCE__XC_ROR_RESEARCH_ORGANIZATIONS
GROUP BY 1 ORDER BY n DESC LIMIT 8;

-- @S10 ROR status: does "inactive" mean closed, or merged into a successor? US vs rest, by type
SELECT IFF(country_code = 'US', 'US', 'rest') place, status, COUNT(*) n,
       COUNT_IF(relationships ILIKE '%successor%') has_successor, COUNT_IF(relationships ILIKE '%parent%') has_parent,
       COUNT_IF(org_types ILIKE '%education%') education, COUNT_IF(org_types ILIKE '%company%') company,
       COUNT_IF(org_types ILIKE '%healthcare%') healthcare, COUNT_IF(established_year IS NULL OR TRIM(established_year::string) IN ('', 'None')) no_founding_year,
       MIN(record_last_modified_date)::string mod0, MAX(record_last_modified_date)::string mod1
FROM LIBRARY_MARTS.REFERENCE.REFERENCE__XC_ROR_RESEARCH_ORGANIZATIONS
GROUP BY 1, 2 ORDER BY 1, 2;

-- @S11 ITIS publications trap check: text 'None' in place of blanks, Jan-1 placeholder dates, printed vs actual date
SELECT COUNT(*) n, COUNT_IF(title = 'None') title_none, COUNT_IF(publisher = 'None') publisher_none,
       COUNT_IF(pub_place = 'None') place_none, COUNT_IF(isbn = 'None') isbn_none, COUNT_IF(issn = 'None') issn_none,
       COUNT_IF(pub_comment = 'None') comment_none, COUNT_IF(title IS NULL) title_null,
       COUNT_IF(MONTH(listed_pub_date) = 1 AND DAY(listed_pub_date) = 1) listed_jan1,
       COUNT_IF(listed_pub_date IS NULL) listed_null, COUNT_IF(actual_pub_date IS NULL) actual_null,
       COUNT_IF(actual_pub_date <> listed_pub_date) actual_differs, COUNT_IF(YEAR(listed_pub_date) < 1753) before_1753,
       COUNT_IF(YEAR(listed_pub_date) = 1753) in_1753, SYSTEM$TYPEOF(MAX(listed_pub_date)) date_type,
       COUNT_IF(pub_comment ILIKE '%doi%') has_doi
FROM LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_PUBLICATIONS;
