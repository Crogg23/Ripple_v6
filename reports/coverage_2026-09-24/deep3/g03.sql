-- deep3/g03: deep pass 3, 2026-09-24. Python door, QUERY_TAG 'deep3-2026-09-24'.
-- Every connection first ran: ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300; ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'.
-- Tables: OPEN_PAYMENTS_PROFILE_SUPPLEMENT, HRSA_UDS_SERVICE_DELIVERY_SITES, MEDICARE_INPATIENT_HOSPITALS_BY_PROVIDER, FDA_GUDID, CMS_FACILITY_AFFILIATION.
-- Small tables were pulled whole in one statement and ranked locally in Python (g03/*.py); that is not extra warehouse statements.

-- S01  (1 rows, 1.8s)
-- S01 GUDID shape: duplicate check on the device barcode, load runs, status, dates
SELECT COUNT(*) n, COUNT(DISTINCT primary_di) dis, COUNT(DISTINCT public_device_record_key) keys,
       COUNT(DISTINCT primary_di, public_version_date) di_ver, COUNT(DISTINCT _source_run_id) runs,
       COUNT(DISTINCT labeler_duns_number) duns, COUNT(DISTINCT company_name) cos,
       MIN(publish_date) p0, MAX(publish_date) p1, MIN(public_version_date) v0, MAX(public_version_date) v1,
       COUNT_IF(primary_di IS NULL OR primary_di='') di_blank,
       ARRAY_AGG(DISTINCT record_status) rs, ARRAY_AGG(DISTINCT commercial_distribution_status) cds,
       ARRAY_AGG(DISTINCT is_kit) kit, ARRAY_AGG(DISTINCT is_combination_product) combo,
       SYSTEM$TYPEOF(MAX(publish_date)) ptype, SYSTEM$TYPEOF(MAX(_ingested_at)) itype,
       COUNT(DISTINCT _ingested_at) ingest_stamps
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_GUDID;

-- S02  (6 rows, 1.3s)
-- S02 MAUDE -> GUDID land rate on the device barcode (MAUDE.UDI_DI = GUDID.PRIMARY_DI), by event type
WITH m AS (
  SELECT NULLIF(TRIM(udi_di),'') di, event_type, YEAR(TRY_TO_DATE(date_received::string)) yr
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_MAUDE),
g AS (SELECT DISTINCT primary_di FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_GUDID)
SELECT m.event_type, MIN(yr) y0, MAX(yr) y1, COUNT(*) reports, COUNT(m.di) with_di,
       COUNT(g.primary_di) landed, COUNT(DISTINCT m.di) distinct_di, COUNT(DISTINCT g.primary_di) distinct_landed
FROM m LEFT JOIN g ON g.primary_di = m.di
GROUP BY 1 ORDER BY reports DESC;

-- S03  (3044 rows, 1.1s)
-- S03 Inpatient by provider: pull the whole 3,044-row table for local peer ranking
SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_INPATIENT_HOSPITALS_BY_PROVIDER;

-- S04  (5432 rows, 0.7s)
-- S04 Hospital general info: pull whole (5,432 rows) for type, ownership, readmission measures by CCN
SELECT ccn, facility_name, city_town, state, hospital_type, hospital_ownership, emergency_services, hospital_overall_rating,
       count_of_facility_readm_measures, count_of_readm_measures_better, count_of_readm_measures_worse,
       count_of_facility_mort_measures, count_of_mort_measures_worse, count_of_safety_measures_worse
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_GENERAL;

-- S05  (19038 rows, 1.6s)
-- S05 UDS service delivery sites: pull whole (19,038 rows) for local peer ranking
SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES;

-- S06  (13302 rows, 1.0s)
-- S06 Inpatient by provider AND DRG, California only: DRG mix of Oroville vs its state peers
SELECT rndrng_prvdr_ccn ccn, rndrng_prvdr_org_name nm, drg_cd, drg_desc, tot_dschrgs, avg_mdcr_pymt_amt
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_INPATIENT_HOSPITALS_BY_PROVIDER_AND_SERVICE
WHERE rndrng_prvdr_state_abrvtn = 'CA';

-- S07  (1356 rows, 0.8s)
-- S07 UDS health-center patient totals (Table 3A line 39 = total, cols a+b) with name, state, year
SELECT i.bhcmisid, i.grantnumber, i.reportingyear, i.healthcentername, i.healthcenterstate, i.urbanruralflag,
       TRY_TO_NUMBER(t.t3a_l39_ca) l39a, TRY_TO_NUMBER(t.t3a_l39_cb) l39b,
       TRY_TO_NUMBER(t.t3a_l1_ca) l1a, TRY_TO_NUMBER(t.t3a_l38_ca) l38a, TRY_TO_NUMBER(t.t3a_l38_cb) l38b
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_UDS_HEALTH_CENTER_INFO i
LEFT JOIN LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_UDS_TABLE3A_PATIENTS t ON t.bhcmisid = i.bhcmisid;

-- S08  (6048 rows, 1.2s)
-- S08 UDS site NPIs -> NPPES: is the NPI a person or an org, active or deactivated, which state, which name
WITH s AS (SELECT DISTINCT fqhc_site_npi_number npi FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES
           WHERE fqhc_site_npi_number IS NOT NULL AND fqhc_site_npi_number <> '')
SELECT s.npi, n.entity_type_code, n.provider_organization_name_legal_business_name org, n.provider_last_name_legal_name ln,
       n.provider_first_name fn, n.provider_business_practice_location_address_state_name pst,
       n.provider_business_practice_location_address_city_name pcity, n.healthcare_provider_taxonomy_code_1 tax1,
       n.provider_enumeration_date enum_dt, n.npi_deactivation_date deact, n.npi_reactivation_date react
FROM s LEFT JOIN LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES n ON n.npi = s.npi;

-- S09  (1 rows, 1.5s)
-- S09 Open Payments profile roster shape: is it a one-row-per-person crosswalk? duplicate NPIs, blank NPIs, alternate names
WITH r AS (SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_PROFILE_SUPPLEMENT),
d AS (SELECT npi, COUNT(*) k, COUNT(DISTINCT profile_id) p FROM r WHERE NULLIF(TRIM(npi),'') IS NOT NULL GROUP BY 1)
SELECT (SELECT COUNT(*) FROM r) n, (SELECT COUNT(DISTINCT profile_id) FROM r) profiles,
       (SELECT COUNT_IF(npi IS NULL) FROM r) npi_null, (SELECT COUNT_IF(TRIM(npi)='') FROM r) npi_empty,
       (SELECT COUNT(*) FROM d) npis, (SELECT COUNT_IF(k>1) FROM d) npis_multi_row, (SELECT COUNT_IF(p>1) FROM d) npis_multi_profile,
       (SELECT MAX(p) FROM d) max_profiles_per_npi,
       (SELECT COUNT_IF(NULLIF(TRIM(alternate_last_name),'') IS NOT NULL) FROM r) alt_last,
       (SELECT COUNT_IF(NULLIF(TRIM(alternate_last_name),'') IS NOT NULL AND UPPER(alternate_last_name)<>UPPER(last_name)) FROM r) alt_last_diff,
       (SELECT COUNT_IF(NULLIF(TRIM(associated_profile_id_1),'') IS NOT NULL) FROM r) assoc1,
       (SELECT COUNT_IF(NULLIF(TRIM(license_state_code_5),'') IS NOT NULL) FROM r) lic5,
       (SELECT COUNT(DISTINCT source_run_id) FROM r) runs, (SELECT ARRAY_AGG(DISTINCT profile_type) FROM r) types,
       (SELECT COUNT_IF(npi IS NULL OR TRIM(npi)='') FROM r WHERE profile_type ILIKE '%Non-Physician%') npp_blank_npi;

-- S10  (2 rows, 1.6s)
-- S10 Open Payments PY2024 x profile roster on profile ID: do blank-NPI payment rows recover an NPI, and do NPIs agree?
WITH p AS (
  SELECT NULLIF(TRIM(npi),'') npi, covered_recipient_profile_id::string pid, total_amount_of_payment_usdollars amt
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS
  WHERE covered_recipient_type NOT ILIKE '%Teaching Hospital%'),
r AS (SELECT profile_id::string pid, NULLIF(TRIM(npi),'') npi FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_PROFILE_SUPPLEMENT)
SELECT IFF(p.npi IS NULL,'pay_npi_blank','pay_npi_present') side,
       COUNT(*) rows_, ROUND(SUM(p.amt)) dollars, COUNT_IF(p.pid IS NULL OR p.pid='') pid_blank,
       COUNT_IF(r.pid IS NOT NULL) pid_landed, COUNT_IF(r.npi IS NOT NULL) roster_has_npi,
       ROUND(SUM(IFF(p.npi IS NULL AND r.npi IS NOT NULL, p.amt, 0))) recovered_dollars,
       COUNT_IF(p.npi IS NOT NULL AND r.npi IS NOT NULL AND p.npi<>r.npi) npi_disagree,
       COUNT(DISTINCT IFF(p.npi IS NULL AND r.npi IS NOT NULL, r.npi, NULL)) recovered_npis
FROM p LEFT JOIN r ON r.pid = p.pid
GROUP BY 1;

-- S11  (434 rows, 2.0s)
-- S11 LEIE people WITHOUT a usable NPI -> Open Payments roster by first+last (or alternate last) name AND city AND state
--     -> PY2024 industry payments dated after the exclusion. The NPI path was done 2026-09-05 (F-113..F-118); this is the name path it missed.
WITH l AS (
  SELECT UPPER(TRIM(last_name)) ln, UPPER(TRIM(first_name)) fn, UPPER(TRIM(city)) city, UPPER(TRIM(state)) st,
         exclusion_type, TRY_TO_DATE(exclusion_date::string) exdt, specialty, general_category, npi lnpi
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE
  WHERE NOT COALESCE(is_entity_not_individual, FALSE) AND NOT COALESCE(npi_is_real, FALSE)
    AND NULLIF(TRIM(last_name),'') IS NOT NULL AND NULLIF(TRIM(first_name),'') IS NOT NULL),
r AS (
  SELECT profile_id::string pid, npi, UPPER(TRIM(first_name)) fn, UPPER(TRIM(last_name)) ln, UPPER(TRIM(alternate_last_name)) aln,
         UPPER(TRIM(city)) city, UPPER(TRIM(state)) st, primary_specialty
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_PROFILE_SUPPLEMENT),
m AS (
  SELECT DISTINCT l.*, r.pid, r.npi rnpi, r.primary_specialty, IFF(r.ln = l.ln, 'last', 'alt_last') via
  FROM l JOIN r ON r.fn = l.fn AND r.city = l.city AND r.st = l.st AND (r.ln = l.ln OR r.aln = l.ln)),
p AS (
  SELECT covered_recipient_profile_id::string pid, TRY_TO_DATE(date_of_payment::string) dt, total_amount_of_payment_usdollars amt,
         applicable_manufacturer_or_applicable_gpo_making_payment_name mfr, nature_of_payment_or_transfer_of_value nat
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS
  WHERE covered_recipient_profile_id::string IN (SELECT pid FROM m))
SELECT m.ln, m.fn, m.city, m.st, m.exclusion_type, m.exdt, m.specialty leie_specialty, m.general_category, m.lnpi,
       m.rnpi, m.primary_specialty, m.via,
       COUNT(p.pid) pays_all, COUNT_IF(p.dt > m.exdt) pays_after, ROUND(SUM(IFF(p.dt > m.exdt, p.amt, 0)),2) amt_after,
       MIN(IFF(p.dt > m.exdt, p.dt, NULL)) first_after, COUNT(DISTINCT IFF(p.dt > m.exdt, p.mfr, NULL)) mfrs_after,
       LISTAGG(DISTINCT IFF(p.dt > m.exdt, p.nat, NULL), '; ') natures
FROM m LEFT JOIN p ON p.pid = m.pid
GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12
ORDER BY amt_after DESC NULLS LAST;

-- S12  (15 rows, 1.1s)
-- S12 GUDID labelers: top 15 by distinct barcodes, with name spellings, share no longer sold, kit share, first/last publish
SELECT labeler_duns_number duns, ANY_VALUE(company_name) nm, COUNT(DISTINCT company_name) spellings,
       COUNT(DISTINCT primary_di) dis, ROUND(COUNT(DISTINCT primary_di)/5061910*100,2) pct_all,
       ROUND(AVG(IFF(commercial_distribution_status='Not in Commercial Distribution',1,0))*100,1) pct_not_sold,
       ROUND(AVG(IFF(is_kit,1,0))*100,1) pct_kit, COUNT(DISTINCT primary_product_code) codes,
       MIN(publish_date) p0, MAX(publish_date) p1,
       MODE(primary_product_code) top_code
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_GUDID
GROUP BY 1 ORDER BY dis DESC LIMIT 15;

-- S13  (14 rows, 0.5s)
-- S13 GUDID time: barcodes first published per year and share now not sold, plus the duplicate-row split
SELECT YEAR(publish_date) yr, COUNT(*) rows_, COUNT(DISTINCT primary_di) dis,
       ROUND(AVG(IFF(commercial_distribution_status='Not in Commercial Distribution',1,0))*100,1) pct_not_sold,
       COUNT(DISTINCT labeler_duns_number) labelers
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_GUDID GROUP BY 1 ORDER BY 1;

-- S14  (18 rows, 1.2s)
-- S14 MAUDE barcodes that miss GUDID: what they look like (length, prefix), top makers; tests whether the miss is format or absence
WITH m AS (SELECT NULLIF(TRIM(udi_di),'') di, manufacturer_name mfr, event_type FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_MAUDE),
g AS (SELECT DISTINCT primary_di FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_GUDID),
x AS (SELECT m.* FROM m LEFT JOIN g ON g.primary_di = m.di WHERE m.di IS NOT NULL AND g.primary_di IS NULL)
SELECT 'len' k, LENGTH(di)::string v, COUNT(*) n, COUNT(DISTINCT di) d, ANY_VALUE(di) eg FROM x GROUP BY 1,2
UNION ALL SELECT 'mfr', mfr, COUNT(*), COUNT(DISTINCT di), ANY_VALUE(di) FROM x GROUP BY 1,2 QUALIFY ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) <= 12
UNION ALL SELECT 'strip_lead0_hits', NULL, COUNT(*), COUNT(DISTINCT x.di), ANY_VALUE(x.di) FROM x JOIN g ON LTRIM(g.primary_di,'0') = LTRIM(x.di,'0')
ORDER BY 1, 3 DESC;

-- S15  (7 rows, 2.0s)
-- S15 Facility affiliation shape by facility type: rows, distinct pairs (duplicate check), clinicians, facilities, widest clinician
WITH a AS (SELECT NULLIF(TRIM(npi),'') npi, ccn, facility_type, ind_pac_id, facility_type_certification_number ftcn
           FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_AFFILIATION),
w AS (SELECT facility_type, npi, COUNT(DISTINCT ccn) k FROM a GROUP BY 1,2)
SELECT a.facility_type, COUNT(*) rows_, COUNT(DISTINCT a.npi, a.ccn) pairs, COUNT(DISTINCT a.npi) npis, COUNT(DISTINCT a.ccn) ccns,
       COUNT_IF(a.npi IS NULL) npi_blank, COUNT(DISTINCT a.ind_pac_id) pacs, COUNT_IF(NULLIF(TRIM(a.ftcn),'') IS NOT NULL) ftcn_filled,
       ANY_VALUE(a.ccn) eg_ccn,
       (SELECT MAX(k) FROM w WHERE w.facility_type = a.facility_type) max_fac_per_npi,
       (SELECT MEDIAN(k) FROM w WHERE w.facility_type = a.facility_type) med_fac_per_npi,
       (SELECT COUNT_IF(k >= 10) FROM w WHERE w.facility_type = a.facility_type) npis_10plus
FROM a GROUP BY a.facility_type ORDER BY rows_ DESC;

-- S16  (25 rows, 1.3s)
-- S16 Affiliated clinicians whose NPI NPPES lists as deactivated and not reactivated, by deactivation year; plus NPIs missing from NPPES
WITH a AS (SELECT npi, MAX(provider_last_name) ln, MAX(provider_first_name) fn, COUNT(*) k,
                  LISTAGG(DISTINCT facility_type, '|') types
           FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_AFFILIATION GROUP BY 1),
n AS (SELECT npi, TRY_TO_DATE(npi_deactivation_date::string) dd, TRY_TO_DATE(npi_reactivation_date::string) rd, entity_type_code et,
             provider_last_name_legal_name nln
      FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES WHERE npi IN (SELECT npi FROM a)),
j AS (SELECT a.*, n.dd, n.rd, n.et, n.nln, (n.npi IS NULL) missing FROM a LEFT JOIN n ON n.npi = a.npi)
SELECT IFF(missing, 'not_in_nppes', IFF(dd IS NOT NULL AND (rd IS NULL OR rd < dd), 'deactivated', 'active')) status,
       YEAR(dd) dyear, COUNT(*) npis, SUM(k) rows_, COUNT_IF(types ILIKE '%Hospital%') in_hospital,
       COUNT_IF(et = '2') org_npi, ANY_VALUE(npi || ' ' || fn || ' ' || ln) eg
FROM j GROUP BY 1,2 ORDER BY 1,2;

-- S17  (5 rows, 1.3s)
-- S17 Dialysis-affiliated clinicians x clinic chain (Dialysis Facility Compare, CCN) x PY2024 industry payments from Fresenius (NPI)
--     Peer test: do doctors listed at Fresenius clinics get Fresenius money at a different rate than doctors at DaVita or other clinics?
WITH a AS (SELECT DISTINCT npi, ccn FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_AFFILIATION WHERE facility_type = 'Dialysis facility'),
d AS (SELECT ccn, CASE WHEN chain_organization ILIKE '%fresenius%' THEN 'FRESENIUS' WHEN chain_organization ILIKE '%davita%' THEN 'DAVITA'
                       WHEN chain_organization IS NULL OR TRIM(chain_organization) = '' THEN 'NONE_LISTED' ELSE 'OTHER' END grp
      FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_DIALYSIS),
an AS (SELECT a.npi, IFF(COUNT(DISTINCT COALESCE(d.grp,'NO_CCN_MATCH')) > 1, 'MIXED', MAX(COALESCE(d.grp,'NO_CCN_MATCH'))) grp, COUNT(*) clinics
       FROM a LEFT JOIN d ON d.ccn = a.ccn GROUP BY 1),
p AS (SELECT NULLIF(TRIM(npi),'') npi,
             SUM(total_amount_of_payment_usdollars) tot,
             SUM(IFF(applicable_manufacturer_or_applicable_gpo_making_payment_name ILIKE '%fresenius%', total_amount_of_payment_usdollars, 0)) fres,
             SUM(IFF(applicable_manufacturer_or_applicable_gpo_making_payment_name ILIKE '%fresenius%'
                     AND nature_of_payment_or_transfer_of_value NOT ILIKE '%food%', total_amount_of_payment_usdollars, 0)) fres_nonfood,
             LISTAGG(DISTINCT IFF(applicable_manufacturer_or_applicable_gpo_making_payment_name ILIKE '%fresenius%', nature_of_payment_or_transfer_of_value, NULL), '; ') fres_natures
      FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS
      WHERE NULLIF(TRIM(npi),'') IN (SELECT npi FROM an) GROUP BY 1)
SELECT an.grp, COUNT(*) npis, ROUND(AVG(an.clinics),2) avg_clinics, COUNT(p.npi) any_pay, COUNT_IF(p.fres > 0) fres_paid,
       ROUND(COUNT_IF(p.fres > 0)/COUNT(*)*100,1) pct_fres, COUNT_IF(p.fres_nonfood > 0) fres_nonfood_paid,
       ROUND(SUM(p.fres)) fres_dollars, ROUND(SUM(p.fres_nonfood)) fres_nonfood_dollars,
       ROUND(MEDIAN(IFF(p.fres > 0, p.fres, NULL)),2) med_fres_paid, ROUND(MAX(p.fres)) max_fres, ROUND(SUM(p.tot)) all_industry_dollars,
       ANY_VALUE(p.fres_natures) eg_natures
FROM an LEFT JOIN p ON p.npi = an.npi GROUP BY 1 ORDER BY npis DESC;

-- S18  (41141 rows, 1.2s)
-- S18 Affiliation: (a) the per-type cap - how many clinicians sit at exactly 1..5 facilities of one type; (b) clinicians listed per facility CCN
WITH a AS (SELECT DISTINCT facility_type, npi, ccn FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_AFFILIATION),
w AS (SELECT facility_type, npi, COUNT(*) k FROM a GROUP BY 1,2)
SELECT 'cap' part, facility_type, k::string key_, COUNT(*) n FROM w GROUP BY 1,2,3
UNION ALL
SELECT 'ccn', facility_type, ccn, COUNT(*) FROM a GROUP BY 1,2,3;

-- S19  (5411 rows, 0.6s)
-- S19 HCRIS cost reports, California hospitals, every fiscal year: beds, all discharges, Medicare (Title XVIII) discharges and days
--     Time check for the Oroville lead: was its Medicare admission rate always high, or did it jump?
SELECT provider_ccn ccn, hospital_name, fiscal_year_end_date fye, source_file_year, number_of_beds beds,
       total_discharges_all dis_all, total_discharges_title_xviii dis_mcr, total_days_title_xviii days_mcr, total_days_all days_all
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS
WHERE state_code = 'CA';

-- S20  (0 rows, 0.5s)
-- S20 DOJ press-release link text (Wayback replay of justice.gov listings) for the top stays-per-patient hospitals
SELECT 'listing' src, link_text, resolved_url, captured_at FROM LIBRARY_MARTS.INVESTIGATIONS.INVESTIGATIONS__XC_WAYBACK_REPLAY_DOJ_LISTING
WHERE link_text ILIKE ANY ('%oroville%', '%north vista%', '%larkin%', '%alliancehealth%', '%meritus%', '%enloe%', '%sepsis%')
UNION ALL
SELECT 'deep', link_text, resolved_url, captured_at FROM LIBRARY_MARTS.INVESTIGATIONS.INVESTIGATIONS__XC_WAYBACK_REPLAY_DOJ_DEEP_PAGES
WHERE link_text ILIKE ANY ('%oroville%', '%north vista%', '%larkin%', '%alliancehealth%', '%meritus%', '%enloe%', '%sepsis%');

-- S21  (1 rows, 0.2s)
-- S21 Is the DOJ link table complete enough for a miss to mean anything? Size, date span, and known hospital cases
SELECT COUNT(*) n, COUNT(DISTINCT link_text) texts, MIN(captured_at) c0, MAX(captured_at) c1,
       COUNT_IF(link_text ILIKE '%hospital%') hospital_links, COUNT_IF(link_text ILIKE '%prime healthcare%') prime,
       COUNT_IF(link_text ILIKE '%community health systems%') chs, COUNT_IF(link_text ILIKE '%false claims%') fca,
       COUNT_IF(link_text ILIKE '%medically unnecessary%' OR link_text ILIKE '%unnecessary inpatient%') unnecessary
FROM LIBRARY_MARTS.INVESTIGATIONS.INVESTIGATIONS__XC_WAYBACK_REPLAY_DOJ_LISTING;

-- S22  (8426 rows, 1.4s)
-- S22 UDS site Medicare billing numbers -> CMS Provider of Services (POS other) on CCN: category, termination code and date, name, state
WITH s AS (SELECT DISTINCT TRIM(fqhc_site_medicare_billing_number) ccn FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES
           WHERE NULLIF(TRIM(fqhc_site_medicare_billing_number),'') IS NOT NULL)
SELECT s.ccn, p.prvdr_ctgry_cd, p.prvdr_ctgry_sbtyp_cd, p.pgm_trmntn_cd, p.trmntn_exprtn_dt, p.fac_name, p.city_name, p.state_cd,
       p.crtfctn_dt, p.orgnl_prtcptn_dt, p.fed_fundd_fqhc_sw
FROM s LEFT JOIN LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER p ON p.ccn = s.ccn;

-- S23  (2906 rows, 0.6s)
-- S23 Every hospital's sepsis share (DRG 871/872) of its listed Medicare discharges, national, for the two-signal screen
SELECT rndrng_prvdr_ccn ccn, SUM(tot_dschrgs) dis_listed,
       SUM(IFF(drg_cd IN ('871','872'), tot_dschrgs, 0)) sepsis,
       SUM(IFF(drg_cd IN ('312','313'), tot_dschrgs, 0)) syncope_chestpain
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_INPATIENT_HOSPITALS_BY_PROVIDER_AND_SERVICE
GROUP BY 1;

-- S24  (9 rows, 1.1s)
-- S24 GUDID barcodes that repeat: top repeaters, how many record keys and version dates each, who labels them
WITH r AS (SELECT primary_di, COUNT(*) n FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_GUDID GROUP BY 1 HAVING COUNT(*) > 1)
SELECT 'summary' k, NULL di, COUNT(*) n_dis, SUM(n) rows_, MAX(n) max_rows, NULL keys_, NULL vers, NULL cos, NULL eg_desc FROM r
UNION ALL
SELECT 'top', g.primary_di, NULL, COUNT(*), NULL, COUNT(DISTINCT g.public_device_record_key), COUNT(DISTINCT g.public_version_date),
       ANY_VALUE(g.company_name), ANY_VALUE(LEFT(g.device_description, 60))
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_GUDID g JOIN (SELECT primary_di FROM r ORDER BY n DESC LIMIT 8) t ON t.primary_di = g.primary_di
GROUP BY 1,2 ORDER BY 1, 4 DESC;

