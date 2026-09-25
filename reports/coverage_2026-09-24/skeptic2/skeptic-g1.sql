-- skeptic2 / g1: fresh-context skeptic pass on deep-0 leads 1 (IRS auto-revocations) and 2 (NHTSA investigations), 2026-09-24.
-- Python door. Each connection first ran: ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300; ALTER SESSION SET QUERY_TAG = 'skeptic-r2-2026-09-24'.
-- Lead 1 used 11 statements (A01-A10, incl. one A09 that failed to compile and was rerun as A09b). Lead 2 used 8 (B01-B08). All SELECT/WITH.
-- A09 original (failed to compile: 'Unsupported subquery type'; the NOT IN (... ORDER BY ... LIMIT 60) was replaced by a ROW_NUMBER CTE in A09b).

-- A01 columns of FAC, HUD S8, EO BMF (IRS lead)
SELECT table_name, LISTAGG(column_name||':'||data_type, ', ') WITHIN GROUP (ORDER BY ordinal_position) cols
FROM LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS
WHERE table_name IN ('ECONOMICS__FED_FAC_SINGLE_AUDIT','HOUSING__FED_HUD_MF_SECTION8_CONTRACTS','CORPORATE_REGISTRY__FED_IRS_EO_BMF')
   OR (table_schema='ECONOMICS' AND table_name ILIKE '%FAC%') OR (table_schema='HOUSING' AND table_name ILIKE '%HUD%')
GROUP BY 1;
-- B01 columns of NHTSA tables
SELECT table_name, LISTAGG(column_name||':'||data_type, ', ') WITHIN GROUP (ORDER BY ordinal_position) cols
FROM LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS
WHERE table_name ILIKE '%NHTSA%'
GROUP BY 1;

-- A02 FAC grain and BMF snapshot size (is "not in BMF" meaningful?)
SELECT (SELECT COUNT(*) FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FAC_SINGLE_AUDIT) fac_rows,
       (SELECT COUNT(DISTINCT report_id) FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FAC_SINGLE_AUDIT) fac_reports,
       (SELECT MIN(audit_year)||'-'||MAX(audit_year) FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FAC_SINGLE_AUDIT) fac_years,
       (SELECT COUNT(*) FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF) bmf_rows,
       (SELECT COUNT(DISTINCT ein) FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF) bmf_eins,
       (SELECT COUNT(DISTINCT state) FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF) bmf_states,
       (SELECT MAX(_ingested_at) FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF) bmf_loaded,
       (SELECT MAX(revocation_posting_date) FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_AUTO_REVOCATIONS) rev_last_post;
-- A03 find HUD tables with a property id + state (for a second-field check on the Section 8 name match)
SELECT table_schema, table_name, LISTAGG(column_name, ', ') cols
FROM LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS
WHERE table_name ILIKE '%HUD%' AND table_name NOT ILIKE '%SECTION8_CONTRACTS%'
  AND (column_name ILIKE '%PROPERTY%' OR column_name ILIKE '%STATE%' OR column_name ILIKE '%OWNER%' OR column_name ILIKE '%TIN%')
GROUP BY 1,2;
-- B02 NHTSA investigations file freshness
SELECT MAX(open_date) newest_open, MAX(close_date) newest_close, MAX(_loaded_at) loaded,
       COUNT(DISTINCT IFF(open_date >= '2025-01-01', nhtsa_action_number, NULL)) probes_opened_2025plus,
       COUNT(DISTINCT IFF(close_date >= '2025-01-01', nhtsa_action_number, NULL)) probes_closed_2025plus,
       COUNT(DISTINCT IFF(close_date >= '2026-01-01', nhtsa_action_number, NULL)) probes_closed_2026
FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_INVESTIGATIONS;
-- B03 PE19010 and EA18003 in full: rows, scope, flags consistent across rows?
SELECT nhtsa_action_number, COUNT(*) rows_, COUNT(DISTINCT make||model||model_year) mmy, LISTAGG(DISTINCT model, '/') models,
       MIN(model_year) my0, MAX(model_year) my1, LISTAGG(DISTINCT component, ' / ') comps, MIN(open_date) od, MAX(close_date) cd,
       BOOLAND_AGG(is_closed) all_closed, BOOLOR_AGG(is_closed) any_closed, BOOLOR_AGG(resulted_in_recall) any_recall,
       COUNT(DISTINCT recall_number) recalls, MIN(subject) subj, LEFT(MIN(summary), 400) summ
FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_INVESTIGATIONS
WHERE nhtsa_action_number IN ('PE19010','EA18003') GROUP BY 1;

-- A04 rebuild the 64-EIN clean set, plus: max single year, revocation rows per EIN, exemption type, successor under a new EIN (same name + state in BMF)
WITH rev AS (SELECT LPAD(ein,9,'0') ein, legal_name, revocation_date, reinstatement_date, exemption_type FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_AUTO_REVOCATIONS),
revn AS (SELECT ein, COUNT(*) rev_rows, COUNT(reinstatement_date) reinst_rows, LISTAGG(DISTINCT exemption_type, ',') ex FROM rev GROUP BY 1),
fac AS (SELECT report_id, LPAD(REGEXP_REPLACE(auditee_ein,'[^0-9]',''),9,'0') ein, auditee_name, auditee_state, auditee_city, audit_year, fy_start_date, fy_end_date, total_amount_expended
        FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FAC_SINGLE_AUDIT WHERE entity_type = 'non-profit' AND REGEXP_REPLACE(auditee_ein,'[^0-9]','') <> ''),
hit AS (SELECT f.*, r.legal_name, r.revocation_date FROM fac f JOIN rev r ON f.ein = r.ein AND f.fy_start_date >= r.revocation_date
             AND (r.reinstatement_date IS NULL OR r.reinstatement_date > f.fy_end_date)
        QUALIFY ROW_NUMBER() OVER (PARTITION BY f.report_id ORDER BY r.revocation_date DESC) = 1),
bmf AS (SELECT DISTINCT LPAD(ein,9,'0') ein FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF),
bmfn AS (SELECT LPAD(ein,9,'0') ein, UPPER(REGEXP_REPLACE(org_name,'[^A-Za-z]','')) nk, state FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF),
pr AS (SELECT DISTINCT LPAD(ein::string,9,'0') ein FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_EO_PR),
per AS (SELECT h.ein, MIN(auditee_name) fac_name, MIN(legal_name) irs_name, MIN(auditee_state) st, MIN(revocation_date) rev, COUNT(*) yrs, MIN(audit_year) y0, MAX(audit_year) y1,
               SUM(total_amount_expended) dollars, MAX(total_amount_expended) max_yr, MAX(JAROWINKLER_SIMILARITY(UPPER(auditee_name), UPPER(legal_name))) sim,
               UPPER(REGEXP_REPLACE(MIN(auditee_name),'[^A-Za-z]','')) nk
        FROM hit h GROUP BY h.ein),
clean AS (SELECT per.* FROM per LEFT JOIN bmf b ON b.ein = per.ein WHERE per.sim >= 85 AND b.ein IS NULL)
SELECT c.ein, c.fac_name, c.st, c.rev, c.y0, c.y1, c.yrs, ROUND(c.dollars/1e6,2) usd_m, ROUND(c.max_yr/1e6,2) max_yr_m, c.sim,
       rn.rev_rows, rn.reinst_rows, rn.ex, (pr.ein IS NOT NULL) in_pr,
       (SELECT LISTAGG(DISTINCT bn.ein, ',') FROM bmfn bn WHERE bn.nk = c.nk AND bn.state = c.st) successor_ein,
       COUNT(*) OVER () n_all, SUM(c.dollars) OVER () usd_all
FROM clean c JOIN revn rn ON rn.ein = c.ein LEFT JOIN pr ON pr.ein = c.ein
ORDER BY c.dollars DESC;

-- A05 revocation rows for the EINs with 2 rows or a reinstatement (Jaycee, Dalewood, Winchester)
SELECT ein, legal_name, city, state, exemption_type, revocation_date, revocation_posting_date, reinstatement_date
FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_AUTO_REVOCATIONS
WHERE LPAD(ein,9,'0') IN ('310944715','202233073','753007074') ORDER BY ein, revocation_date;
-- A06 HUD second field: the six Section 8 name hits in HUD Picture of Subsidized Households (has state) vs the FAC state
SELECT name, state, program_label, sub_program, total_units, quarter, sumlevel
FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_ASSISTED_HOUSING_PROJECTS
WHERE (name ILIKE '%CAMELLIA MANOR%' OR name ILIKE '%JAYCEE ESTATES%' OR name ILIKE '%HOOVER SENIOR%' OR name ILIKE '%HILLSIDE GULFPORT%'
       OR name ILIKE '%TUPQICH%' OR name ILIKE '%WINCHESTER SENIOR%')
ORDER BY name, quarter DESC LIMIT 60;
-- A07 Section 8 contract rows for the six names (every row, to see duplicates/generic hits)
SELECT property_id, property_name, program_type_name, tracs_status_name, assisted_units_count, tracs_effective_date, tracs_overall_expiration_date
FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_MF_SECTION8_CONTRACTS
WHERE property_name ILIKE '%CAMELLIA MANOR%' OR property_name ILIKE '%JAYCEE ESTATES%' OR property_name ILIKE '%HOOVER SENIOR%' OR property_name ILIKE '%HILLSIDE%GULFPORT%'
   OR property_name ILIKE '%TUPQICH%' OR property_name ILIKE '%WINCHESTER SENIOR%' OR property_name ILIKE '%HOOVER%'
ORDER BY property_name;

-- A08 all 64 clean-set EINs: loose successor check (BMF org in same state, name JW>=92 on cleaned name, other EIN) and FAC filings of the same name under another EIN
WITH rev AS (SELECT LPAD(ein,9,'0') ein, legal_name, revocation_date, reinstatement_date FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_AUTO_REVOCATIONS),
fac0 AS (SELECT report_id, LPAD(REGEXP_REPLACE(auditee_ein,'[^0-9]',''),9,'0') ein, auditee_name, auditee_state, audit_year, fy_start_date, fy_end_date, total_amount_expended, entity_type,
                TRIM(REGEXP_REPLACE(REGEXP_REPLACE(UPPER(auditee_name),'[^A-Z ]',' '),'\s+',' ')) nn
         FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FAC_SINGLE_AUDIT WHERE REGEXP_REPLACE(auditee_ein,'[^0-9]','') <> ''),
fac AS (SELECT * FROM fac0 WHERE entity_type = 'non-profit'),
hit AS (SELECT f.*, r.legal_name FROM fac f JOIN rev r ON f.ein = r.ein AND f.fy_start_date >= r.revocation_date
             AND (r.reinstatement_date IS NULL OR r.reinstatement_date > f.fy_end_date)
        QUALIFY ROW_NUMBER() OVER (PARTITION BY f.report_id ORDER BY r.revocation_date DESC) = 1),
bmf AS (SELECT DISTINCT LPAD(ein,9,'0') ein FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF),
per AS (SELECT h.ein, MIN(auditee_name) fac_name, MIN(nn) nn, MIN(auditee_state) st, MAX(audit_year) y1, SUM(total_amount_expended) usd, MAX(total_amount_expended) max_yr,
               MAX(JAROWINKLER_SIMILARITY(UPPER(auditee_name), UPPER(legal_name))) sim FROM hit h GROUP BY h.ein),
clean AS (SELECT per.* FROM per LEFT JOIN bmf b ON b.ein = per.ein WHERE per.sim >= 85 AND b.ein IS NULL),
bm AS (SELECT LPAD(ein,9,'0') ein, org_name, state, subsection_code, ruling_yyyymm, TRIM(REGEXP_REPLACE(REGEXP_REPLACE(UPPER(org_name),'[^A-Z ]',' '),'\s+',' ')) nn
       FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF WHERE state IN (SELECT st FROM clean)),
succ AS (SELECT c.ein, LISTAGG(DISTINCT bm.ein||' '||bm.org_name||' sub'||bm.subsection_code||' rul'||bm.ruling_yyyymm, ' ; ') s
         FROM clean c JOIN bm ON bm.state = c.st AND bm.ein <> c.ein AND LEFT(bm.nn,4) = LEFT(c.nn,4) AND JAROWINKLER_SIMILARITY(bm.nn, c.nn) >= 92 GROUP BY 1),
othr AS (SELECT c.ein, LISTAGG(DISTINCT f.ein||' y'||f.audit_year, ' ; ') o
         FROM clean c JOIN fac0 f ON f.auditee_state = c.st AND f.ein <> c.ein AND JAROWINKLER_SIMILARITY(f.nn, c.nn) >= 95 GROUP BY 1)
SELECT c.ein, c.fac_name, c.st, c.y1, ROUND(c.usd/1e6,2) usd_m, ROUND(c.max_yr/1e6,2) max_yr_m, succ.s bmf_lookalike, othr.o fac_other_ein
FROM clean c LEFT JOIN succ ON succ.ein = c.ein LEFT JOIN othr ON othr.ein = c.ein
ORDER BY c.usd DESC;

-- A09b (A09 failed to compile, rerun) housing subset of the clean set, recomputed: count, summed $, max-single-year $, filed 2024+, minus the Hunters Woods successor-EIN case; plus every clean row not shown before (Tupqich)
WITH rev AS (SELECT LPAD(ein,9,'0') ein, legal_name, revocation_date, reinstatement_date FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_AUTO_REVOCATIONS),
fac AS (SELECT report_id, LPAD(REGEXP_REPLACE(auditee_ein,'[^0-9]',''),9,'0') ein, auditee_name, auditee_state, audit_year, fy_start_date, fy_end_date, total_amount_expended
        FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FAC_SINGLE_AUDIT WHERE entity_type = 'non-profit' AND REGEXP_REPLACE(auditee_ein,'[^0-9]','') <> ''),
hit AS (SELECT f.*, r.legal_name, r.reinstatement_date FROM fac f JOIN rev r ON f.ein = r.ein AND f.fy_start_date >= r.revocation_date
             AND (r.reinstatement_date IS NULL OR r.reinstatement_date > f.fy_end_date)
        QUALIFY ROW_NUMBER() OVER (PARTITION BY f.report_id ORDER BY r.revocation_date DESC) = 1),
bmf AS (SELECT DISTINCT LPAD(ein,9,'0') ein FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF),
per AS (SELECT h.ein, MIN(auditee_name) fac_name, MIN(auditee_state) st, MAX(audit_year) y1, SUM(total_amount_expended) usd, MAX(total_amount_expended) max_yr,
               MAX(JAROWINKLER_SIMILARITY(UPPER(auditee_name), UPPER(legal_name))) sim, MAX(reinstatement_date) reinst FROM hit h GROUP BY h.ein),
clean AS (SELECT per.*, REGEXP_LIKE(UPPER(fac_name), '.*(HOUSING|HDFC|ESTATES|MANOR|APARTMENTS|APTS|SENIOR|ELDERLY|HOMES|HILLSIDE|TUPQICH|ANNEX|INDEPENDENT LIVING|WELLNESS HOUSE|-EE-|-HH).*')
                             AND NOT UPPER(fac_name) LIKE '%HOUSING AUTHORITY%' AND st <> 'PR' housing
          FROM per LEFT JOIN bmf b ON b.ein = per.ein WHERE per.sim >= 85 AND b.ein IS NULL),
rk AS (SELECT clean.*, ROW_NUMBER() OVER (ORDER BY usd DESC) r FROM clean)
SELECT 'SUMMARY' k, housing::string fac_name, NULL st, COUNT(*) n, ROUND(SUM(usd)/1e6,1) usd_m, ROUND(SUM(max_yr)/1e6,1) max_yr_m,
       COUNT_IF(y1 >= 2024) filed_2024plus, COUNT_IF(reinst IS NOT NULL) reinstated_later
FROM clean WHERE ein <> '541502432' GROUP BY housing
UNION ALL
SELECT ein, fac_name, st, y1, ROUND(usd/1e6,2), ROUND(max_yr/1e6,2), housing::int, r FROM rk
WHERE UPPER(fac_name) LIKE '%TUPQICH%' OR r > 60 OR housing ORDER BY 1;

-- A10 year-by-year federal expended for the five HUD-active names: flat numbers = capital-advance balance carried each year, not new spending
SELECT LPAD(REGEXP_REPLACE(auditee_ein,'[^0-9]',''),9,'0') ein, MIN(auditee_name) nm, MIN(auditee_city)||' '||MIN(auditee_state) place,
       LISTAGG(audit_year||':'||ROUND(total_amount_expended/1e3)||'k', '  ') WITHIN GROUP (ORDER BY audit_year) by_year
FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FAC_SINGLE_AUDIT
WHERE LPAD(REGEXP_REPLACE(auditee_ein,'[^0-9]',''),9,'0') IN ('204761103','310944715','954651580','141864848','020736815','200584160')
GROUP BY 1;

-- B04 recall_number carried on the two probes, and recalls in the recall file on the same make/model/year and component
WITH pr AS (SELECT DISTINCT nhtsa_action_number a, make, model, model_year, open_date od, recall_number FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_INVESTIGATIONS
            WHERE nhtsa_action_number IN ('PE19010','EA18003'))
SELECT pr.a, MIN(pr.recall_number) probe_recall_no, r.campno, MIN(r.notification_date) notif, MIN(r.component) comp, LEFT(MIN(r.desc_defect),160) defect,
       COUNT(DISTINCT pr.make||pr.model||pr.model_year) mmy_hit, SUM(r.potentially_affected_units) units_rows_summed
FROM pr LEFT JOIN LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_RECALLS r
  ON r.make = pr.make AND r.model = pr.model AND r.model_year = pr.model_year
 AND ( (pr.a = 'PE19010' AND (r.component ILIKE '%COLLISION%' OR r.component ILIKE '%BRAK%' OR r.desc_defect ILIKE '%emergency braking%'))
    OR (pr.a = 'EA18003' AND (r.component ILIKE '%AIR BAG%' OR r.desc_defect ILIKE '%clockspring%' OR r.desc_defect ILIKE '%clock spring%')) )
GROUP BY pr.a, r.campno ORDER BY pr.a, notif;
-- B05 median open-to-close by probe type (PE vs EA), closed probes opened 2010+; and how many PEs opened 2010-2021 are still open
WITH p AS (SELECT nhtsa_action_number a, LEFT(nhtsa_action_number,2) typ, MIN(open_date) od, MAX(close_date) cd, BOOLAND_AGG(is_closed) closed
           FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_INVESTIGATIONS
           WHERE LEFT(nhtsa_action_number,2) IN ('PE','EA','RQ','DP','AQ') AND open_date >= '2010-01-01' GROUP BY 1,2)
SELECT typ, COUNT(*) probes, COUNT_IF(closed) closed, MEDIAN(IFF(closed, DATEDIFF('day',od,cd), NULL)) med_days,
       PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY IFF(closed, DATEDIFF('day',od,cd), NULL)) p90_days,
       MAX(IFF(closed, DATEDIFF('day',od,cd), NULL)) max_closed_days,
       COUNT_IF(NOT closed AND od < '2022-01-01') open_opened_pre2022, LISTAGG(IFF(NOT closed AND od < '2022-01-01', a, NULL), ',') which
FROM p GROUP BY typ ORDER BY probes DESC;
-- B06 later probes on the same make (Nissan AEB / VW air bag) that could be an upgrade or successor of PE19010 / EA18003
SELECT nhtsa_action_number, MIN(mfr_name) mfr, MIN(open_date) od, MAX(close_date) cd, BOOLAND_AGG(is_closed) closed, BOOLOR_AGG(resulted_in_recall) rec,
       LISTAGG(DISTINCT model, '/') models, MIN(subject) subj
FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_INVESTIGATIONS
WHERE ((make = 'NISSAN' AND (component ILIKE '%COLLISION%' OR subject ILIKE '%brak%')) OR (make = 'VOLKSWAGEN' AND component ILIKE '%AIR BAG%'))
  AND open_date >= '2015-01-01'
GROUP BY 1 ORDER BY od;

-- B07 PE19010: matching complaints by year received (component = forward collision avoidance), plus text-only matches that name the brakes, plus undated rows
WITH cp AS (SELECT DISTINCT odino, date_received, component, injured, crash, complaint_description d
            FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_COMPLAINTS
            WHERE make = 'NISSAN' AND model = 'ROGUE' AND model_year BETWEEN 2017 AND 2019)
SELECT COALESCE(YEAR(date_received)::string, 'NO DATE') yr,
       COUNT(DISTINCT IFF(component ILIKE '%FORWARD COLLISION AVOIDANCE%', odino, NULL)) fca_component,
       COUNT(DISTINCT IFF(NOT component ILIKE '%FORWARD COLLISION AVOIDANCE%' AND (d ILIKE '%emergency brak%' OR d ILIKE '%AEB%' OR d ILIKE '%phantom brak%' OR d ILIKE '%brakes on its own%' OR d ILIKE '%slammed on the brakes%' OR d ILIKE '%collision avoid%'), odino, NULL)) text_only,
       COUNT(DISTINCT IFF(component ILIKE '%FORWARD COLLISION AVOIDANCE%' AND injured > 0, odino, NULL)) fca_injury,
       COUNT(DISTINCT odino) all_rogue_1719
FROM cp GROUP BY 1 ORDER BY 1;
-- B08 EA18003: of the air-bag complaints on the probe's make/model/years, how many actually describe the clockspring / air-bag warning light vs inflator
WITH pr AS (SELECT DISTINCT make, model, model_year FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_INVESTIGATIONS WHERE nhtsa_action_number = 'EA18003'),
cp AS (SELECT DISTINCT c.odino, c.date_received, c.component, c.injured, c.deaths, c.complaint_description d
       FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_COMPLAINTS c JOIN pr ON c.make = pr.make AND c.model = pr.model AND c.model_year = pr.model_year
       WHERE c.component ILIKE '%AIR BAG%' AND c.date_received >= '2005-01-01')
SELECT IFF(date_received < '2018-04-18', 'before', 'after') win, COUNT(DISTINCT odino) airbag_all,
       COUNT(DISTINCT IFF(d ILIKE '%clock%spring%' OR d ILIKE '%clockspring%' OR d ILIKE '%spiral%' OR component ILIKE '%CLOCKSPRING%', odino, NULL)) clockspring,
       COUNT(DISTINCT IFF(d ILIKE '%light%' OR d ILIKE '%warning%' OR d ILIKE '%indicator%', odino, NULL)) light_mention,
       COUNT(DISTINCT IFF(d ILIKE '%inflator%' OR d ILIKE '%takata%' OR d ILIKE '%shrapnel%' OR d ILIKE '%rupture%' OR d ILIKE '%recall%', odino, NULL)) inflator_or_recall,
       COUNT(DISTINCT IFF(date_received >= '2018-04-18' AND (d ILIKE '%clock%spring%' OR d ILIKE '%clockspring%' OR component ILIKE '%CLOCKSPRING%') AND injured > 0, odino, NULL)) clock_inj_after,
       COUNT(DISTINCT IFF(deaths > 0, odino, NULL)) any_death
FROM cp GROUP BY 1;

