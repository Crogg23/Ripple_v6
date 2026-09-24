-- deep-10: coverage round 2 deep pass, 2026-09-24. Python door, QUERY_TAG 'coverage-r2-2026-09-24'.
-- Tables: FHA_SF_PORTFOLIO_SNAPSHOT, MF_FIRM_COMMITMENTS, MF_SECTION8_CONTRACTS, MAPPING_INEQUALITY, USDA_RD_MFH_ACTIVE_PROJECTS.
-- Each connection also ran ALTER SESSION timeout 300 + query tag (not counted).

-- S01 FHA SF snapshot: count + profile
SELECT COUNT(*) n, COUNT(DISTINCT loan_record_id) ids, COUNT(DISTINCT originating_mortgagee_name) lenders,
  SYSTEM$TYPEOF(MAX(interest_rate)) rate_type, MIN(TRY_TO_DOUBLE(TO_VARCHAR(interest_rate))) r_min,
  MEDIAN(TRY_TO_DOUBLE(TO_VARCHAR(interest_rate))) r_med, MAX(TRY_TO_DOUBLE(TO_VARCHAR(interest_rate))) r_max,
  COUNT_IF(TRY_TO_DOUBLE(TO_VARCHAR(interest_rate)) IS NULL OR TRY_TO_DOUBLE(TO_VARCHAR(interest_rate)) = 0) r_bad,
  LISTAGG(DISTINCT loan_purpose, '|') purposes, LISTAGG(DISTINCT property_type, '|') ptypes,
  LISTAGG(DISTINCT product_type, '|') products, LISTAGG(DISTINCT down_payment_source, '|') dps,
  LISTAGG(DISTINCT endorsement_year || '-' || endorsement_month, '|') ym,
  COUNT(DISTINCT property_state || property_county) counties, COUNT_IF(property_county IS NULL OR property_county = '') cty_blank
FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_FHA_SF_PORTFOLIO_SNAPSHOT;

-- S02 FHA SF snapshot: sample 5
SELECT * EXCLUDE (_ingested_at, _source_run_id, _src_sha256) FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_FHA_SF_PORTFOLIO_SNAPSHOT LIMIT 5;

-- S03 MF firm commitments: count + profile
SELECT COUNT(*) n, COUNT(DISTINCT fha_number) fha_nums, COUNT(DISTINCT lender_name) lenders,
  MIN(fiscal_year_at_firm_activity) fy0, MAX(fiscal_year_at_firm_activity) fy1, SUM(mortgage_amount)/1e9 mort_b,
  LISTAGG(DISTINCT current_status, '|') statuses, LISTAGG(DISTINCT firm_activity, '|') acts,
  LISTAGG(DISTINCT activity_group, '|') groups, COUNT_IF(project_name ILIKE 'PACT%') pact_rows,
  SYSTEM$TYPEOF(MAX(total_units)) units_type, COUNT_IF(lender_name IS NULL OR lender_name = '') lender_blank
FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_MF_FIRM_COMMITMENTS;

-- S04 MF firm commitments: sample 5
SELECT * EXCLUDE (_ingested_at, _source_run_id, _src_sha256) FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_MF_FIRM_COMMITMENTS LIMIT 5;

-- S05 Section 8 contracts: count + profile
SELECT COUNT(*) n, COUNT(DISTINCT contract_number) contracts, COUNT(DISTINCT property_id) props, SUM(assisted_units_count) units,
  LISTAGG(DISTINCT tracs_status_name, '|') statuses, LISTAGG(DISTINCT program_type_group_name, '|') groups,
  SYSTEM$TYPEOF(MAX(rent_to_fmr_ratio)) ratio_type, COUNT_IF(rent_to_fmr_ratio = 0) ratio0, COUNT_IF(rent_to_fmr_ratio IS NULL) ratio_null,
  COUNT_IF(rent_to_fmr_ratio > 150) over150, SUM(IFF(rent_to_fmr_ratio > 150, assisted_units_count, 0)) units150,
  MAX(rent_to_fmr_ratio) rmax, LISTAGG(DISTINCT rent_to_fmr_description, '|') bands
FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_MF_SECTION8_CONTRACTS;

-- S06 Section 8 contracts: sample 5
SELECT * EXCLUDE (_ingested_at, _source_run_id, _src_sha256) FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_MF_SECTION8_CONTRACTS LIMIT 5;

-- S07 Mapping inequality: count + profile
SELECT COUNT(*) n, COUNT(DISTINCT holc_neighborhood_key) keys, COUNT(DISTINCT city || state) cities,
  COUNT_IF(geometry IS NOT NULL AND TO_VARCHAR(geometry) <> '') geom_ok, AVG(LENGTH(TO_VARCHAR(geometry))) geom_len,
  COUNT_IF(lat IS NOT NULL) lat_ok, COUNT(DISTINCT fips) fips_vals, COUNT_IF(holc_id IS NOT NULL AND holc_id <> '') holc_id_ok,
  COUNT_IF(year_mapped IS NOT NULL) yr_ok, COUNT(DISTINCT TO_VARCHAR(area_description_data)) adesc_vals,
  LISTAGG(DISTINCT holc_grade, '|') grades, SYSTEM$TYPEOF(MAX(geometry)) geom_type
FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_MAPPING_INEQUALITY;

-- S08 Mapping inequality: sample 5
SELECT holc_neighborhood_key, city, state, fips, holc_grade, holc_grade_rank, lat, lon, LEFT(TO_VARCHAR(geometry), 160) geom
FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_MAPPING_INEQUALITY LIMIT 5;

-- S09 USDA RD MFH: count + profile
SELECT COUNT(*) n, COUNT(DISTINCT borrower_id || '-' || project_id) projs, SUM(project_size_units) units, SUM(vacant_units) vac,
  SUM(rental_assistance_units) ra, SYSTEM$TYPEOF(MAX(date_restrictive_clause_expires)) dtype,
  MIN(date_restrictive_clause_expires) rc0, MAX(date_restrictive_clause_expires) rc1, COUNT_IF(date_restrictive_clause_expires IS NULL) rc_null,
  COUNT_IF(YEAR(date_restrictive_clause_expires) BETWEEN 2026 AND 2030) rc_26_30,
  LISTAGG(DISTINCT rental_code, '|') rcodes, LISTAGG(DISTINCT profit_type_code, '|') ptypes, LISTAGG(DISTINCT tax_status_indicator, '|') tax,
  MIN(date_of_operation) op0, MAX(date_of_operation) op1
FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_USDA_RD_MFH_ACTIVE_PROJECTS;

-- S10 USDA RD MFH: sample 5
SELECT * EXCLUDE (_ingested_at, _source_run_id, _src_sha256, main_address_line2, main_address_line3) FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_USDA_RD_MFH_ACTIVE_PROJECTS LIMIT 5;

-- S11 Join partners: find SAM exclusions, HUD owners, EPA facility and census tract tables
SELECT table_schema, table_name, row_count FROM LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES
WHERE table_name ILIKE ANY ('%SAM%EXCL%', '%HUD%OWNER%', '%HUD_MF_PROP%', '%ECHO%FAC%', '%FRS%', '%USDA_RD%', '%HUD%', '%EGRID%', '%TRI_%BASIC%')
ORDER BY table_name;

-- S12 FHA SF: builder-captive lenders vs everyone else, national and same-county medians
WITH b AS (
  SELECT property_state || '|' || property_county cty, originating_mortgagee_name nm,
    CASE
      WHEN nm ILIKE 'DHI MORTGAGE%' THEN 'DR Horton'
      WHEN nm ILIKE ANY ('LENNAR MORTGAGE%', 'CALATLANTIC%') THEN 'Lennar'
      WHEN nm ILIKE 'PULTE MORTGAGE%' THEN 'Pulte'
      WHEN nm ILIKE 'NVR MORTGAGE%' THEN 'NVR'
      WHEN nm ILIKE 'TAYLOR MORRISON%' THEN 'Taylor Morrison'
      WHEN nm ILIKE 'INSPIRE HOME LOANS%' THEN 'Century'
      WHEN nm ILIKE 'M/I FINANCIAL%' THEN 'M/I Homes'
      WHEN nm ILIKE 'KBHS%' THEN 'KB Home'
      WHEN nm ILIKE 'TOLL BROTHERS%' THEN 'Toll'
      WHEN nm ILIKE ANY ('K. HOVNANIAN%', 'K HOVNANIAN%') THEN 'Hovnanian'
      WHEN nm ILIKE 'JET HOMELOANS%' THEN 'Dream Finders'
      WHEN nm ILIKE 'SHEA MORTGAGE%' THEN 'Shea'
      WHEN nm ILIKE 'TRI POINTE%' THEN 'Tri Pointe'
      WHEN nm ILIKE 'ASHTON WOODS%' THEN 'Ashton Woods'
      WHEN nm ILIKE 'HIGHLAND HOMELOANS%' THEN 'Highland'
      WHEN nm ILIKE 'BRIGHTLAND%' THEN 'Brightland'
      ELSE 'ALL OTHER LENDERS' END builder,
    interest_rate r, original_mortgage_amount amt, down_payment_source dps, property_type pt
  FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_FHA_SF_PORTFOLIO_SNAPSHOT
  WHERE property_county <> ''),
nat AS (
  SELECT builder, COUNT(*) loans, MEDIAN(r) med_rate, AVG(r) avg_rate, MEDIAN(amt) med_amt,
    ROUND(100 * COUNT_IF(dps IN ('Gov Asst', 'Non Profit')) / COUNT(*), 1) pct_dpa,
    ROUND(100 * COUNT_IF(r < 5) / COUNT(*), 1) pct_under5, LISTAGG(DISTINCT IFF(builder = 'ALL OTHER LENDERS', NULL, nm), ' / ') names
  FROM b GROUP BY 1),
cs AS (SELECT cty, builder, COUNT(*) n, MEDIAN(r) mr, MEDIAN(amt) ma FROM b GROUP BY 1, 2),
m AS (
  SELECT x.builder, SUM(x.n) cm_loans, COUNT(*) cm_counties,
    ROUND(SUM(x.n * (x.mr - o.mr)) / SUM(x.n), 3) rate_gap, ROUND(SUM(x.n * (x.ma - o.ma)) / SUM(x.n), 0) amt_gap
  FROM cs x JOIN cs o ON o.cty = x.cty AND o.builder = 'ALL OTHER LENDERS' AND o.n >= 10
  WHERE x.builder <> 'ALL OTHER LENDERS' GROUP BY 1)
SELECT nat.*, m.cm_loans, m.cm_counties, m.rate_gap, m.amt_gap
FROM nat LEFT JOIN m USING (builder) ORDER BY loans DESC;

-- S13 FHA SF: counties where builder-captive lenders made the biggest share of FHA purchase loans (min 100 loans)
WITH b AS (
  SELECT property_state st, property_county cty, originating_mortgagee_name nm,
    nm ILIKE ANY ('DHI MORTGAGE%', 'LENNAR MORTGAGE%', 'PULTE MORTGAGE%', 'NVR MORTGAGE%', 'TAYLOR MORRISON%', 'INSPIRE HOME LOANS%',
      'M/I FINANCIAL%', 'KBHS%', 'TOLL BROTHERS%', 'K. HOVNANIAN%', 'JET HOMELOANS%', 'SHEA MORTGAGE%', 'TRI POINTE%', 'ASHTON WOODS%',
      'HIGHLAND HOMELOANS%', 'BRIGHTLAND%') is_b,
    interest_rate r
  FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_FHA_SF_PORTFOLIO_SNAPSHOT WHERE property_county <> ''),
c AS (
  SELECT st, cty, COUNT(*) loans, COUNT_IF(is_b) b_loans, ROUND(100 * COUNT_IF(is_b) / COUNT(*), 1) b_pct,
    MEDIAN(IFF(is_b, r, NULL)) b_rate, MEDIAN(IFF(is_b, NULL, r)) o_rate,
    MODE(IFF(is_b, nm, NULL)) top_b
  FROM b GROUP BY 1, 2)
SELECT *, (SELECT ROUND(100 * COUNT_IF(is_b) / COUNT(*), 1) FROM b) nat_b_pct,
  (SELECT COUNT(*) FROM c WHERE loans >= 100) counties_100plus
FROM c WHERE loans >= 100 ORDER BY b_pct DESC LIMIT 20;

-- S14 MF firm: status x activity counts, rows and distinct FHA numbers
SELECT current_status, firm_activity, COUNT(*) n, COUNT(DISTINCT fha_number) fha, ROUND(SUM(mortgage_amount) / 1e9, 2) mort_b
FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_MF_FIRM_COMMITMENTS GROUP BY 1, 2 ORDER BY n DESC;

-- S15 MF firm: lender share of Finally Endorsed deals FY2020-2026, one row per FHA number (latest activity)
WITH d AS (
  SELECT * FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_MF_FIRM_COMMITMENTS
  WHERE current_status = 'Finally Endorsed' AND fiscal_year_at_firm_activity >= 2020
  QUALIFY ROW_NUMBER() OVER (PARTITION BY fha_number ORDER BY firm_activity_date DESC) = 1)
SELECT lender_name, COUNT(*) deals, ROUND(SUM(mortgage_amount) / 1e9, 2) mort_b, SUM(total_units) units,
  ROUND(100 * RATIO_TO_REPORT(SUM(mortgage_amount)) OVER (), 1) pct_dollars,
  ROUND(100 * SUM(SUM(mortgage_amount)) OVER (ORDER BY SUM(mortgage_amount) DESC ROWS UNBOUNDED PRECEDING) / SUM(SUM(mortgage_amount)) OVER (), 1) cum_pct,
  COUNT(*) OVER () lenders_all, SUM(COUNT(*)) OVER () deals_all, ROUND(SUM(SUM(mortgage_amount)) OVER () / 1e9, 1) mort_all_b
FROM d GROUP BY 1 ORDER BY mort_b DESC LIMIT 15;

-- S16 MF firm: every PACT-named row plus NYC total, and lender/project names vs SAM exclusions
WITH f AS (SELECT * FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_MF_FIRM_COMMITMENTS),
s AS (
  SELECT DISTINCT UPPER(REGEXP_REPLACE(entity_name, '[^A-Za-z0-9 ]', '')) nm, state
  FROM LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS
  WHERE is_entity_not_individual AND entity_name IS NOT NULL),
lend AS (SELECT DISTINCT UPPER(REGEXP_REPLACE(lender_name, '[^A-Za-z0-9 ]', '')) nm FROM f WHERE lender_name <> ''),
proj AS (SELECT DISTINCT UPPER(REGEXP_REPLACE(project_name, '[^A-Za-z0-9 ]', '')) nm, project_state st FROM f)
SELECT 'pact' kind, project_name label, lender_name extra, fiscal_year_at_firm_activity fy, current_status status,
  ROUND(mortgage_amount / 1e6, 1) mort_m, total_units units
FROM f WHERE project_name ILIKE '%PACT%'
UNION ALL
SELECT 'lender_in_sam', l.nm, NULL, NULL, NULL, NULL, (SELECT COUNT(*) FROM lend) FROM lend l JOIN s ON s.nm = l.nm
UNION ALL
SELECT 'project_in_sam_same_state', p.nm, p.st, NULL, NULL, NULL, (SELECT COUNT(*) FROM proj) FROM proj p JOIN s ON s.nm = p.nm AND s.state = p.st
ORDER BY kind, mort_m DESC NULLS LAST;

-- S17 Section 8: rent-to-FMR by program family, Active contracts; est. dollars over FMR = (ratio/100 - 1) x sum(units x FMR) x 12
WITH a AS (
  SELECT *, (units_0br_count * fmr_0br + units_1br_count * fmr_1br + units_2br_count * fmr_2br + units_3br_count * fmr_3br + units_4br_count * fmr_4br) fmr_month
  FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_MF_SECTION8_CONTRACTS WHERE tracs_status_name = 'Active' AND rent_to_fmr_ratio > 0)
SELECT program_type_group_name grp, COUNT(*) contracts, SUM(assisted_units_count) units,
  ROUND(MEDIAN(rent_to_fmr_ratio), 0) p50, ROUND(PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY rent_to_fmr_ratio), 0) p90,
  COUNT_IF(rent_to_fmr_ratio > 150) c150, SUM(IFF(rent_to_fmr_ratio > 150, assisted_units_count, 0)) u150,
  ROUND(100 * COUNT_IF(rent_to_fmr_ratio > 150) / COUNT(*), 1) pct_c150,
  ROUND(SUM(IFF(rent_to_fmr_ratio > 150, (rent_to_fmr_ratio / 100 - 1) * fmr_month * 12, 0)) / 1e6, 1) over150_excess_m_yr,
  ROUND(SUM(IFF(rent_to_fmr_ratio > 100, (rent_to_fmr_ratio / 100 - 1) * fmr_month * 12, 0)) / 1e6, 1) over100_excess_m_yr,
  COUNT_IF(fmr_month = 0) fmr0
FROM a GROUP BY ROLLUP(1) ORDER BY units DESC NULLS FIRST;

-- S18 Section 8: top 25 Active contracts over 150% FMR by est. dollars over FMR per year
WITH a AS (
  SELECT *, (units_0br_count * fmr_0br + units_1br_count * fmr_1br + units_2br_count * fmr_2br + units_3br_count * fmr_3br + units_4br_count * fmr_4br) fmr_month
  FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_MF_SECTION8_CONTRACTS WHERE tracs_status_name = 'Active' AND rent_to_fmr_ratio > 150)
SELECT property_id, property_name, LEFT(contract_number, 2) st, program_type_name prog, assisted_units_count units,
  ROUND(rent_to_fmr_ratio, 0) ratio, fmr_1br, fmr_2br, ROUND((rent_to_fmr_ratio / 100 - 1) * fmr_month * 12 / 1e6, 2) excess_m_yr,
  tracs_effective_date eff, contract_term_months_qty term
FROM a ORDER BY excess_m_yr DESC LIMIT 25;

-- S19 Section 8 join partner: HUD MF property owners landing table, 3-row peek
SELECT OBJECT_CONSTRUCT(*) o FROM LIBRARY_RAW.LANDING.FED_HUD_MF_PROPERTIES_OWNERS LIMIT 2;

-- S20 Section 8 join partner: HUD MF owners landing table column names and row count
SELECT COUNT(*) OVER () n_peek, ARRAY_TO_STRING(OBJECT_KEYS(OBJECT_CONSTRUCT(*)), ',') cols
FROM LIBRARY_RAW.LANDING.FED_HUD_MF_PROPERTIES_OWNERS LIMIT 1;

-- S21 MF firm: PACT rows with FHA number and program (duplicate check) + the one SAM project-name hit
SELECT 'pact' kind, fha_number k, project_name nm, program_subcategory prog, activity_description act, firm_activity_date dt,
  current_status st, ROUND(mortgage_amount / 1e6, 1) mort_m, commitment_record_id extra
FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_MF_FIRM_COMMITMENTS WHERE project_name ILIKE 'PACT%'
UNION ALL
SELECT 'mf_lake_village', fha_number, project_name, program_subcategory, activity_description, firm_activity_date, current_status,
  ROUND(mortgage_amount / 1e6, 1), lender_name
FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_MF_FIRM_COMMITMENTS WHERE project_name ILIKE 'LAKE VILLAGE OF AUBURN%'
UNION ALL
SELECT 'sam_lake_village', uei, entity_name, exclusion_type, excluding_agency, activation_date, TO_VARCHAR(is_currently_excluded),
  NULL, city || ' ' || state || ' ' || exclusion_program
FROM LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS WHERE entity_name ILIKE 'LAKE VILLAGE OF AUBURN%'
ORDER BY kind, dt;

-- S22 Redlining x TRI 2023: point-in-polygon, facilities and pounds released per km2 by HOLC grade, plus land rate
WITH poly AS (
  SELECT holc_neighborhood_key k, city, state, holc_grade_rank g, TRY_TO_GEOGRAPHY(geometry) geo
  FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_MAPPING_INEQUALITY),
p2 AS (
  SELECT k, city, state, g, geo, ST_XMIN(geo) x0, ST_XMAX(geo) x1, ST_YMIN(geo) y0, ST_YMAX(geo) y1, ST_AREA(geo) / 1e6 km2
  FROM poly WHERE geo IS NOT NULL),
fac AS (
  SELECT c_2_trifd id, MAX(TRY_TO_DOUBLE(TO_VARCHAR(c_12_latitude))) lat, MAX(-ABS(TRY_TO_DOUBLE(TO_VARCHAR(c_13_longitude)))) lon,
    SUM(IFF(c_50_unit_of_measure = 'Pounds', TRY_TO_DOUBLE(TO_VARCHAR(c_107_total_releases)), 0)) lbs
  FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023 GROUP BY 1
  HAVING lat BETWEEN 17 AND 72 AND lon BETWEEN -180 AND -60),
hits AS (
  SELECT p2.k, p2.g, fac.id, fac.lbs FROM p2 JOIN fac
    ON fac.lon BETWEEN p2.x0 AND p2.x1 AND fac.lat BETWEEN p2.y0 AND p2.y1
   AND ST_CONTAINS(p2.geo, ST_MAKEPOINT(fac.lon, fac.lat))
  WHERE p2.km2 < 500),
byg AS (
  SELECT p2.g, COUNT(*) polys, ROUND(SUM(p2.km2), 0) km2, MAX(p2.km2) max_km2 FROM p2 GROUP BY 1)
SELECT byg.g, byg.polys, byg.km2, ROUND(byg.max_km2, 1) max_km2, COUNT(DISTINCT h.id) facs, ROUND(SUM(h.lbs) / 1e6, 2) mlbs,
  ROUND(100 * COUNT(DISTINCT h.id) / NULLIF(byg.km2, 0), 2) facs_per_100km2, ROUND(SUM(h.lbs) / NULLIF(byg.km2, 0), 0) lbs_per_km2,
  (SELECT COUNT(*) FROM fac) tri_facs, (SELECT COUNT(*) FROM poly WHERE geo IS NULL) bad_geo,
  (SELECT COUNT(DISTINCT id) FROM hits) facs_in_any
FROM byg LEFT JOIN hits h ON h.g = byg.g GROUP BY 1, 2, 3, 4 ORDER BY 1;

-- S23 USDA RD MFH: units by restrictive-clause bucket x 50-year-from-opening bucket (maturity proxy)
SELECT
  CASE WHEN date_restrictive_clause_expires IS NULL THEN '0 none' WHEN date_restrictive_clause_expires < '2026-09-24' THEN '1 already past'
       WHEN YEAR(date_restrictive_clause_expires) <= 2030 THEN '2 2026-2030' WHEN YEAR(date_restrictive_clause_expires) <= 2035 THEN '3 2031-2035'
       ELSE '4 after 2035' END rc,
  CASE WHEN date_of_operation IS NULL THEN '0 none' WHEN YEAR(date_of_operation) + 50 < 2026 THEN '1 opened before 1976'
       WHEN YEAR(date_of_operation) + 50 <= 2030 THEN '2 opened 1976-1980' WHEN YEAR(date_of_operation) + 50 <= 2035 THEN '3 opened 1981-1985'
       ELSE '4 opened 1986+' END op50,
  COUNT(*) projects, SUM(project_size_units) units, SUM(rental_assistance_units) ra_units, SUM(vacant_units) vac,
  ROUND(100 * SUM(vacant_units) / NULLIF(SUM(project_size_units), 0), 1) vac_pct,
  ROUND(AVG(DATEDIFF(year, date_of_operation, date_restrictive_clause_expires)), 1) avg_rc_years
FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_USDA_RD_MFH_ACTIVE_PROJECTS GROUP BY 1, 2 ORDER BY 1, 2;

-- S24 USDA RD MFH: data vintage + sentinels: newest opening years, tax-credit date oddities, vacancy spread
SELECT YEAR(date_of_operation) yr, COUNT(*) projects, SUM(project_size_units) units,
  COUNT_IF(YEAR(date_tax_credit_expires) < 1987 OR YEAR(date_tax_credit_expires) > 2080) tc_sentinel,
  COUNT_IF(vacant_units > project_size_units) vac_gt_units, COUNT_IF(vacant_units = project_size_units AND project_size_units > 0) fully_vacant,
  COUNT_IF(rental_assistance_units > project_size_units) ra_gt_units,
  (SELECT COUNT_IF(YEAR(date_tax_credit_expires) < 1987 OR YEAR(date_tax_credit_expires) > 2080) FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_USDA_RD_MFH_ACTIVE_PROJECTS) tc_sentinel_all,
  (SELECT COUNT_IF(vacant_units = project_size_units AND project_size_units > 0) FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_USDA_RD_MFH_ACTIVE_PROJECTS) fully_vacant_all,
  (SELECT COUNT_IF(vacant_units >= 0.5 * project_size_units AND project_size_units > 0) FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_USDA_RD_MFH_ACTIVE_PROJECTS) half_vacant_all,
  (SELECT MAX(_ingested_at)::string FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_USDA_RD_MFH_ACTIVE_PROJECTS) ingested
FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_USDA_RD_MFH_ACTIVE_PROJECTS
WHERE YEAR(date_of_operation) >= 2008 GROUP BY 1 ORDER BY 1;

-- S25 Redlining x TRI 2023 v2: ungraded polygons kept (grade 0), same-city D vs B density, top D-polygon facilities
WITH poly AS (
  SELECT holc_neighborhood_key k, city, state, COALESCE(holc_grade_rank, 0) g, TRY_TO_GEOGRAPHY(geometry) geo
  FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_MAPPING_INEQUALITY),
p2 AS (
  SELECT k, city, state, g, geo, ST_XMIN(geo) x0, ST_XMAX(geo) x1, ST_YMIN(geo) y0, ST_YMAX(geo) y1, ST_AREA(geo) / 1e6 km2
  FROM poly WHERE geo IS NOT NULL AND ST_AREA(geo) / 1e6 < 500),
fac AS (
  SELECT c_2_trifd id, ANY_VALUE(c_4_facility_name) nm, ANY_VALUE(c_23_industry_sector) sector,
    MAX(TRY_TO_DOUBLE(TO_VARCHAR(c_12_latitude))) lat, MAX(-ABS(TRY_TO_DOUBLE(TO_VARCHAR(c_13_longitude)))) lon,
    SUM(IFF(c_50_unit_of_measure = 'Pounds', TRY_TO_DOUBLE(TO_VARCHAR(c_107_total_releases)), 0)) lbs
  FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023 GROUP BY 1
  HAVING lat BETWEEN 17 AND 72 AND lon BETWEEN -180 AND -60),
hits AS (
  SELECT p2.k, p2.city, p2.state, p2.g, fac.id, fac.nm, fac.sector, fac.lbs FROM p2 JOIN fac
    ON fac.lon BETWEEN p2.x0 AND p2.x1 AND fac.lat BETWEEN p2.y0 AND p2.y1 AND ST_CONTAINS(p2.geo, ST_MAKEPOINT(fac.lon, fac.lat))),
byg AS (
  SELECT p2.g, COUNT(*) polys, SUM(p2.km2) km2 FROM p2 GROUP BY 1),
hg AS (SELECT g, COUNT(DISTINCT id) facs, SUM(lbs) lbs FROM hits GROUP BY 1),
cg AS (SELECT city, state, g, SUM(km2) km2 FROM p2 GROUP BY 1, 2, 3),
ch AS (SELECT city, state, g, COUNT(DISTINCT id) f FROM hits GROUP BY 1, 2, 3),
cd AS (
  SELECT cg.city, cg.state,
    SUM(IFF(cg.g = 4, COALESCE(ch.f, 0), 0)) / NULLIF(SUM(IFF(cg.g = 4, cg.km2, 0)), 0) d_dens,
    SUM(IFF(cg.g = 2, COALESCE(ch.f, 0), 0)) / NULLIF(SUM(IFF(cg.g = 2, cg.km2, 0)), 0) b_dens
  FROM cg LEFT JOIN ch ON ch.city = cg.city AND ch.state = cg.state AND ch.g = cg.g GROUP BY 1, 2)
SELECT 'grade' kind, TO_VARCHAR(byg.g) label, byg.polys a, ROUND(byg.km2, 0) b, COALESCE(hg.facs, 0) c, ROUND(hg.lbs / 1e6, 2) d,
  ROUND(100 * COALESCE(hg.facs, 0) / byg.km2, 2) e
FROM byg LEFT JOIN hg ON hg.g = byg.g
UNION ALL
SELECT 'cities_with_B_and_D', 'D>B | D<B | tie(both 0) | tie(equal>0)', COUNT_IF(d_dens > b_dens), COUNT_IF(d_dens < b_dens),
  COUNT_IF(d_dens = 0 AND b_dens = 0), COUNT_IF(d_dens = b_dens AND d_dens > 0), COUNT(*)
FROM cd WHERE d_dens IS NOT NULL AND b_dens IS NOT NULL
UNION ALL
SELECT 'land', 'tri facs | in any polygon | distinct facility-polygon hits', (SELECT COUNT(*) FROM fac), (SELECT COUNT(DISTINCT id) FROM hits),
  (SELECT COUNT(*) FROM hits), NULL, NULL
UNION ALL
SELECT * FROM (
  SELECT 'top_D_facility', nm || ' | ' || city || ' ' || state || ' | ' || sector, NULL, NULL, NULL, ROUND(lbs / 1e6, 2), NULL
  FROM hits WHERE g = 4 QUALIFY ROW_NUMBER() OVER (PARTITION BY id ORDER BY k) = 1 ORDER BY lbs DESC LIMIT 12)
ORDER BY kind, label;

-- S26 Section 8 over-150% contracts joined to HUD MF owners on PROPERTY_ID: land rate, name agreement, top owners with their whole-portfolio base
WITH a AS (
  SELECT *, (units_0br_count * fmr_0br + units_1br_count * fmr_1br + units_2br_count * fmr_2br + units_3br_count * fmr_3br + units_4br_count * fmr_4br) fmr_month
  FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_MF_SECTION8_CONTRACTS WHERE tracs_status_name = 'Active' AND rent_to_fmr_ratio > 0),
o AS (
  SELECT TRY_TO_NUMBER(TO_VARCHAR(property_id)) pid, ANY_VALUE(property_name_text) pname,
    ANY_VALUE(COALESCE(NULLIF(TRIM(owner_organization_name), ''), owner_individual_full_name)) owner, ANY_VALUE(mgmt_agent_org_name) mgr
  FROM LIBRARY_RAW.LANDING.FED_HUD_MF_PROPERTIES_OWNERS GROUP BY 1),
j AS (SELECT a.*, o.pid, o.pname, o.owner, o.mgr FROM a LEFT JOIN o ON o.pid = TRY_TO_NUMBER(TO_VARCHAR(a.property_id))),
own AS (
  SELECT owner, COUNT(*) all_contracts, COUNT_IF(rent_to_fmr_ratio > 150) c150, SUM(IFF(rent_to_fmr_ratio > 150, assisted_units_count, 0)) u150,
    ROUND(SUM(IFF(rent_to_fmr_ratio > 150, (rent_to_fmr_ratio / 100 - 1) * fmr_month * 12, 0)) / 1e6, 1) excess_m
  FROM j WHERE owner IS NOT NULL GROUP BY 1)
SELECT 'land' kind, NULL owner, COUNT_IF(rent_to_fmr_ratio > 150) all_contracts, COUNT_IF(rent_to_fmr_ratio > 150 AND pid IS NOT NULL) c150,
  COUNT_IF(rent_to_fmr_ratio > 150 AND pid IS NOT NULL AND UPPER(LEFT(REGEXP_REPLACE(pname, '[^A-Za-z]', ''), 6)) = UPPER(LEFT(REGEXP_REPLACE(property_name, '[^A-Za-z]', ''), 6))) u150,
  COUNT_IF(pid IS NOT NULL) / COUNT(*) excess_m
FROM j
UNION ALL
SELECT * FROM (SELECT 'owner', owner, all_contracts, c150, u150, excess_m FROM own ORDER BY excess_m DESC LIMIT 15)
UNION ALL
SELECT * FROM (SELECT 'owner_by_count', owner, all_contracts, c150, u150, excess_m FROM own WHERE c150 >= 3 ORDER BY c150 DESC LIMIT 10);

-- S27 Section 8: over-150% contracts in cheap markets (1BR FMR under $1,300), with owner and manager
WITH a AS (
  SELECT *, (units_0br_count * fmr_0br + units_1br_count * fmr_1br + units_2br_count * fmr_2br + units_3br_count * fmr_3br + units_4br_count * fmr_4br) fmr_month
  FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_MF_SECTION8_CONTRACTS
  WHERE tracs_status_name = 'Active' AND rent_to_fmr_ratio > 150 AND fmr_1br BETWEEN 1 AND 1299),
o AS (
  SELECT TRY_TO_NUMBER(TO_VARCHAR(property_id)) pid, ANY_VALUE(COALESCE(NULLIF(TRIM(owner_organization_name), ''), owner_individual_full_name)) owner,
    ANY_VALUE(mgmt_agent_org_name) mgr, ANY_VALUE(city_name_text) city
  FROM LIBRARY_RAW.LANDING.FED_HUD_MF_PROPERTIES_OWNERS GROUP BY 1)
SELECT property_name, o.city, LEFT(contract_number, 2) st, program_type_name prog, assisted_units_count units, ROUND(rent_to_fmr_ratio, 0) ratio,
  fmr_1br, ROUND((rent_to_fmr_ratio / 100 - 1) * fmr_month * 12 / 1e6, 2) excess_m, o.owner, o.mgr,
  COUNT(*) OVER () n_cheap, SUM(assisted_units_count) OVER () units_cheap
FROM a LEFT JOIN o ON o.pid = TRY_TO_NUMBER(TO_VARCHAR(a.property_id))
ORDER BY excess_m DESC LIMIT 15;

-- S28 USDA RD MFH: by state, units in projects opened by 1980 with no live restrictive clause (none or already past), and vacancy vs national
WITH p AS (
  SELECT state_abbreviation st, project_size_units u, rental_assistance_units ra, vacant_units v,
    (YEAR(date_of_operation) <= 1980 AND (date_restrictive_clause_expires IS NULL OR date_restrictive_clause_expires < '2026-09-24')) exposed
  FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_USDA_RD_MFH_ACTIVE_PROJECTS)
SELECT st, COUNT(*) projects, SUM(u) units, SUM(IFF(exposed, u, 0)) exp_units, ROUND(100 * SUM(IFF(exposed, u, 0)) / SUM(u), 1) exp_pct,
  SUM(IFF(exposed, ra, 0)) exp_ra_units, ROUND(100 * SUM(v) / SUM(u), 1) vac_pct,
  ROUND(100 * SUM(SUM(IFF(exposed, u, 0))) OVER () / SUM(SUM(u)) OVER (), 1) nat_exp_pct, ROUND(100 * SUM(SUM(v)) OVER () / SUM(SUM(u)) OVER (), 1) nat_vac_pct,
  SUM(SUM(IFF(exposed, u, 0))) OVER () nat_exp_units, SUM(SUM(IFF(exposed, ra, 0))) OVER () nat_exp_ra
FROM p GROUP BY 1 ORDER BY exp_units DESC LIMIT 15;

-- S29 MF firm: deduped dollar total (latest row per FHA number) vs raw row sum; FHA SF: exact-rate clustering by builder lender
SELECT 'mf_raw_vs_dedup' kind, NULL k, ROUND(SUM(mortgage_amount) / 1e9, 2) a, NULL b, NULL c
FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_MF_FIRM_COMMITMENTS
UNION ALL
SELECT 'mf_dedup_latest_per_fha', NULL, ROUND(SUM(mortgage_amount) / 1e9, 2), COUNT(*), NULL FROM (
  SELECT mortgage_amount FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_MF_FIRM_COMMITMENTS
  QUALIFY ROW_NUMBER() OVER (PARTITION BY fha_number ORDER BY firm_activity_date DESC, commitment_record_id) = 1)
UNION ALL
SELECT 'fha_modal_rate', nm, r, n, ROUND(100 * c / n, 1) FROM (
  SELECT originating_mortgagee_name nm, interest_rate r, COUNT(*) c, SUM(COUNT(*)) OVER (PARTITION BY originating_mortgagee_name) n,
    ROW_NUMBER() OVER (PARTITION BY originating_mortgagee_name ORDER BY COUNT(*) DESC) rn
  FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_FHA_SF_PORTFOLIO_SNAPSHOT
  WHERE originating_mortgagee_name IN ('DHI MORTGAGE COMPANY LTD', 'LENNAR MORTGAGE, LLC', 'CROSSCOUNTRY MORTGAGE, LLC', 'ROCKET MORTGAGE, LLC', 'UNITED WHOLESALE MORTGAGE, LLC')
  GROUP BY 1, 2)
WHERE rn = 1;

-- S30 Section 8: the 766 over-150% Active contracts split by cheap market (1BR FMR under $1,300) and program family, plus top state prefixes
WITH a AS (
  SELECT *, IFF(fmr_1br BETWEEN 1 AND 1299 OR (fmr_1br = 0 AND fmr_2br BETWEEN 1 AND 1499), 'cheap', 'not cheap') mkt,
    CASE WHEN program_type_group_name IN ('Sec. 202', 'PRAC 202/811', 'PAC 202/811') THEN 'elderly/disabled 202-811'
         WHEN program_type_name ILIKE '%Preserv%' OR program_type_group_name = 'S8 Preservation' THEN 'preservation'
         ELSE 'other S8 (family + mixed)' END fam
  FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_MF_SECTION8_CONTRACTS WHERE tracs_status_name = 'Active' AND rent_to_fmr_ratio > 150)
SELECT 'mkt_x_family' kind, mkt || ' / ' || fam label, COUNT(*) contracts, SUM(assisted_units_count) units, ROUND(MEDIAN(rent_to_fmr_ratio), 0) med_ratio
FROM a GROUP BY 1, 2
UNION ALL
SELECT * FROM (SELECT 'state_prefix', LEFT(contract_number, 2), COUNT(*), SUM(assisted_units_count), ROUND(MEDIAN(rent_to_fmr_ratio), 0)
  FROM a GROUP BY 1, 2 ORDER BY 3 DESC LIMIT 10)
ORDER BY kind, contracts DESC;

-- S31 Second-field check: HUD Picture of Subsidized Households spending per unit per month for the top over-FMR buildings, and the Section 8 peer median
SELECT 'row' kind, name, states, std_city, program_label, code, total_units, spending_per_month, rent_per_month, quarter
FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_ASSISTED_HOUSING_PROJECTS
WHERE (name ILIKE ANY ('WHITE BIRCH%', 'GATEWAY PLAZA%', 'MANHATTAN PLAZA%', 'BICENTENNIAL TOWERS%', 'MELVILLE TOWERS%', 'MARSHALL FIELD%', 'LANDS END II%', 'B%NAI B%RITH APARTMENTS%', 'HARBORVIEW APTS%', 'BRINTON MANOR%'))
UNION ALL
SELECT 'peer_median', program_label, NULL, NULL, NULL, NULL, COUNT(*), MEDIAN(IFF(spending_per_month > 0, spending_per_month, NULL)),
  MEDIAN(IFF(rent_per_month > 0, rent_per_month, NULL)), MAX(quarter)
FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_ASSISTED_HOUSING_PROJECTS
WHERE program_label ILIKE '%Section 8%' GROUP BY program_label
ORDER BY kind DESC, name;

-- S32 USDA RD MFH: the fully vacant "active" projects, with manager and dates
SELECT state_abbreviation st, city, project_name, management_name, project_size_units units, vacant_units vac, rental_assistance_units ra,
  rental_code, date_of_operation, date_restrictive_clause_expires rc_exp, revitalization_indicator revit
FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_USDA_RD_MFH_ACTIVE_PROJECTS
WHERE vacant_units = project_size_units AND project_size_units > 0 ORDER BY units DESC;

-- S33 Section 8 x HUD Picture of Subsidized Households (Dec 2025) on property ID: real HUD spending for over-150% contracts vs the rest, cheap markets outside Puerto Rico
WITH psh AS (
  SELECT TRY_TO_NUMBER(SPLIT_PART(TRIM(code), ' ', 1)) pid, MAX(total_units) psh_units, MAX(spending_per_month) spend
  FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_ASSISTED_HOUSING_PROJECTS
  WHERE program_label = 'Project Based Section 8' AND spending_per_month > 0 GROUP BY 1),
c AS (
  SELECT TRY_TO_NUMBER(TO_VARCHAR(property_id)) pid, MAX(rent_to_fmr_ratio) ratio, SUM(assisted_units_count) units,
    MAX(fmr_1br) fmr1, MAX(LEFT(contract_number, 2)) st
  FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_MF_SECTION8_CONTRACTS WHERE tracs_status_name = 'Active' AND rent_to_fmr_ratio > 0 GROUP BY 1),
j AS (SELECT c.*, psh.psh_units, psh.spend FROM c LEFT JOIN psh USING (pid)),
med AS (SELECT MEDIAN(spend) m FROM psh)
SELECT IFF(ratio > 150, 'over 150%', '150% or under') band,
  IFF(fmr1 BETWEEN 1 AND 1299 AND st <> 'RQ', 'cheap, not PR', 'other') mkt,
  COUNT(*) props, COUNT(spend) props_in_psh, SUM(units) units,
  COUNT_IF(spend IS NOT NULL AND ABS(psh_units - units) <= 0.1 * units) units_agree,
  ROUND(MEDIAN(spend), 0) med_spend, (SELECT ROUND(m, 0) FROM med) all_psh_med,
  COUNT_IF(spend > 2 * (SELECT m FROM med)) props_over_2x_med,
  ROUND(SUM(spend * psh_units * 12) / 1e6, 1) psh_spend_m_yr
FROM j GROUP BY 1, 2 ORDER BY 1 DESC, 2;
