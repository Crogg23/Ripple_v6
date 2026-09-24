-- deep2/deep-0: coverage round 2 hand-query pass, 2026-09-24. Python door, QUERY_TAG 'coverage-r2-2026-09-24'.
-- Every connection first ran: ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300; ALTER SESSION SET QUERY_TAG = 'coverage-r2-2026-09-24'.
-- Tables: NHTSA_INVESTIGATIONS, ICIJ_OFFSHORELEAKS_OFFICERS, ICIJ_OFFSHORELEAKS_RELATIONSHIPS, IRS_AUTO_REVOCATIONS, PBGC_TRUSTEED_PENSION_PLANS.

-- S01 NHTSA investigations: count + profile
SELECT COUNT(*) n, COUNT(DISTINCT nhtsa_action_number) probes, MIN(open_date) o0, MAX(open_date) o1,
       MIN(close_date) c0, MAX(close_date) c1, COUNT_IF(close_date IS NULL) close_null,
       ARRAY_AGG(DISTINCT resulted_in_recall) rir_vals, ARRAY_AGG(DISTINCT is_closed) closed_vals,
       ARRAY_AGG(DISTINCT LEFT(nhtsa_action_number,2)) prefixes, COUNT(DISTINCT recall_number) recalls,
       SYSTEM$TYPEOF(MAX(open_date)) otype, SYSTEM$TYPEOF(MAX(resulted_in_recall)) rtype
FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_INVESTIGATIONS;

-- S02 NHTSA investigations: sample 5
SELECT nhtsa_action_number, mfr_name, make, model, model_year, component, open_date, close_date, is_closed, resulted_in_recall, recall_number, subject, LEFT(summary,90) s
FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_INVESTIGATIONS LIMIT 5;

-- S03 ICIJ officers: count + profile
SELECT COUNT(*) n, COUNT(DISTINCT node_id) nodes, COUNT(DISTINCT name) names,
       COUNT_IF(country_codes ILIKE '%USA%') usa_rows, COUNT(DISTINCT IFF(country_codes ILIKE '%USA%', UPPER(TRIM(name)), NULL)) usa_names,
       COUNT(DISTINCT IFF(country_codes ILIKE '%USA%' AND ARRAY_SIZE(SPLIT(TRIM(REGEXP_REPLACE(name,'\s+',' ')),' '))>=2, UPPER(TRIM(name)), NULL)) usa_multiword,
       COUNT_IF(name ILIKE '%bearer%' OR name ILIKE '%portador%') bearer_rows,
       COUNT(DISTINCT source_leak) leaks
FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_OFFICERS;

-- S04 ICIJ officers: sample 5 (US-tagged)
SELECT node_id, name, countries, country_codes, source_leak, valid_until, note
FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_OFFICERS WHERE country_codes ILIKE '%USA%' LIMIT 5;

-- S05 ICIJ relationships: count by type, with duplicate-link rate
SELECT rel_type, COUNT(*) n, COUNT(DISTINCT node_id_start, node_id_end, rel_type) distinct_links,
       COUNT(DISTINCT source_leak) leaks, MIN(start_date) sd0, MAX(start_date) sd1
FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_RELATIONSHIPS
GROUP BY ROLLUP(rel_type) ORDER BY n DESC;

-- S06 ICIJ relationships: sample 5
SELECT node_id_start, node_id_end, rel_type, link, status, start_date, end_date, source_leak
FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_RELATIONSHIPS LIMIT 5;

-- S07 IRS auto revocations: count + profile
SELECT COUNT(*) n, COUNT(DISTINCT ein) eins, MIN(revocation_date) r0, MAX(revocation_date) r1,
       COUNT_IF(reinstatement_date IS NOT NULL) reinst, COUNT_IF(LENGTH(ein)=9) ein9, COUNT_IF(LENGTH(ein)<9) ein_short,
       COUNT_IF(ein='000000000') ein_zero, SYSTEM$TYPEOF(MAX(revocation_date)) rtype, SYSTEM$TYPEOF(MAX(reinstatement_date)) itype,
       COUNT_IF(exemption_type='03') c3
FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_AUTO_REVOCATIONS;

-- S08 IRS auto revocations: sample 5
SELECT ein, legal_name, doing_business_as, city, state, zip_code, exemption_type, revocation_date, revocation_posting_date, reinstatement_date
FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_AUTO_REVOCATIONS LIMIT 5;

-- S09 PBGC "trusteed" pension plans: count + profile
SELECT COUNT(*) n, COUNT(DISTINCT ein) eins, COUNT(DISTINCT plan_id) plans, SUM(participant_count) parts,
       MEDIAN(participant_count) med, MAX(participant_count) mx, MIN(plan_effective_date) e0, MAX(plan_effective_date) e1,
       COUNT_IF(participant_count >= 1000) big, COUNT_IF(LENGTH(ein)<9) ein_short
FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_PBGC_TRUSTEED_PENSION_PLANS;

-- S10 PBGC pension plans: sample 5
SELECT plan_id, ein, pn, plan_name, plan_sponsor_name, admin_city, admin_state, plan_effective_date, participant_count, contact_phone_number
FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_PBGC_TRUSTEED_PENSION_PLANS LIMIT 5;

-- S11 NHTSA: one row per probe (PE/EA only, opened 2010+), then by maker: probes, recall share, median days to close, still open
WITH p AS (
  SELECT nhtsa_action_number a, LEFT(nhtsa_action_number,2) typ, MIN(open_date) od, MAX(close_date) cd,
         BOOLOR_AGG(resulted_in_recall) rec, BOOLAND_AGG(is_closed) closed, COUNT(DISTINCT mfr_name) nmfr, MIN(mfr_name) mfr
  FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_INVESTIGATIONS
  WHERE LEFT(nhtsa_action_number,2) IN ('PE','EA') AND open_date >= '2010-01-01'
  GROUP BY 1,2)
SELECT COALESCE(mfr,'__ALL__') mfr, COUNT(*) probes, COUNT_IF(nmfr>1) multi_mfr,
       COUNT_IF(closed) closed, COUNT_IF(NOT closed) still_open, COUNT_IF(cd IS NULL) cd_null,
       COUNT_IF(closed AND rec) closed_recall, ROUND(COUNT_IF(closed AND rec)/NULLIF(COUNT_IF(closed),0),3) recall_share_closed,
       MEDIAN(IFF(closed, DATEDIFF('day',od,cd), NULL)) med_days_closed,
       MEDIAN(IFF(closed AND NOT rec, DATEDIFF('day',od,cd), NULL)) med_days_norecall,
       MAX(IFF(NOT closed, DATEDIFF('day',od,'2026-09-24'), NULL)) oldest_open_days
FROM p GROUP BY ROLLUP(mfr) HAVING COUNT(*) >= 15 ORDER BY probes DESC;

-- S12 NHTSA: oldest still-open probes (any type), one row per probe
SELECT nhtsa_action_number, MIN(mfr_name) mfr, MIN(open_date) od, MAX(close_date) cd, BOOLAND_AGG(is_closed) closed,
       DATEDIFF('day', MIN(open_date), '2026-09-24') age_days, COUNT(*) rows_, COUNT(DISTINCT make||model||model_year) mmy, MIN(subject) subj
FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_INVESTIGATIONS
GROUP BY 1 HAVING NOT BOOLAND_AGG(is_closed) ORDER BY od LIMIT 30;

-- S13 PBGC "trusteed" plans: top 15 by participants
SELECT ein, pn, plan_sponsor_name, plan_name, admin_city, admin_state, plan_effective_date, participant_count
FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_PBGC_TRUSTEED_PENSION_PLANS ORDER BY participant_count DESC NULLS LAST LIMIT 15;

-- S14 PBGC: overlap with the real trusteed list (LABOR__FED_PBGC_TRUSTEED_PLANS), padded EIN, plus plan-type words in names
WITH e AS (SELECT LPAD(REGEXP_REPLACE(ein,'[^0-9]',''),9,'0') ein, pn, plan_name, participant_count, plan_effective_date FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_PBGC_TRUSTEED_PENSION_PLANS),
     t AS (SELECT DISTINCT LPAD(REGEXP_REPLACE(ein,'[^0-9]',''),9,'0') ein FROM LIBRARY_MARTS.LABOR.LABOR__FED_PBGC_TRUSTEED_PLANS WHERE ein IS NOT NULL)
SELECT COUNT(*) plans, COUNT_IF(t.ein IS NOT NULL) ein_in_trusteed, SUM(IFF(t.ein IS NOT NULL, participant_count,0)) parts_in_trusteed,
       COUNT_IF(plan_name ILIKE '%cash balance%') cash_bal, COUNT_IF(plan_effective_date >= '2015-01-01') eff_2015plus,
       COUNT_IF(plan_effective_date = '1903-01-01') eff_1903, (SELECT COUNT(*) FROM t) trusteed_eins
FROM e LEFT JOIN t ON e.ein = t.ein;

-- S15 IRS revocations x FAC single audits: federal-money fiscal years that start after revocation and before any reinstatement
WITH rev AS (SELECT LPAD(ein,9,'0') ein, legal_name, revocation_date, reinstatement_date, exemption_type
             FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_AUTO_REVOCATIONS),
fac AS (SELECT report_id, LPAD(REGEXP_REPLACE(auditee_ein,'[^0-9]',''),9,'0') ein, auditee_name, entity_type, audit_year, fy_start_date, fy_end_date, total_amount_expended
        FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FAC_SINGLE_AUDIT WHERE REGEXP_REPLACE(auditee_ein,'[^0-9]','') <> ''),
anyrev AS (SELECT DISTINCT ein FROM rev),
hit AS (SELECT f.*, r.legal_name, r.revocation_date, r.reinstatement_date, r.exemption_type
        FROM fac f JOIN rev r ON f.ein = r.ein AND f.fy_start_date >= r.revocation_date
             AND (r.reinstatement_date IS NULL OR r.reinstatement_date > f.fy_end_date)
        QUALIFY ROW_NUMBER() OVER (PARTITION BY f.report_id ORDER BY r.revocation_date DESC) = 1)
SELECT f.entity_type, COUNT(DISTINCT f.report_id) reports, COUNT(DISTINCT f.ein) eins,
       COUNT(DISTINCT IFF(a.ein IS NOT NULL, f.ein, NULL)) eins_ever_revoked,
       COUNT(DISTINCT h.report_id) hit_reports, COUNT(DISTINCT h.ein) hit_eins,
       SUM(h.total_amount_expended) hit_dollars,
       COUNT(DISTINCT IFF(JAROWINKLER_SIMILARITY(UPPER(h.auditee_name), UPPER(h.legal_name)) >= 85, h.ein, NULL)) hit_eins_name_agree
FROM fac f LEFT JOIN anyrev a ON f.ein = a.ein LEFT JOIN hit h ON f.report_id = h.report_id
GROUP BY ROLLUP(f.entity_type) ORDER BY reports DESC;

-- S16 NHTSA: every Tesla PE/EA probe since 2010 plus every still-open PE/EA probe since 2010, one row per probe
SELECT nhtsa_action_number, MIN(mfr_name) mfr, COUNT(DISTINCT mfr_name) nmfr, MIN(open_date) od, MAX(close_date) cd, BOOLAND_AGG(is_closed) closed,
       BOOLOR_AGG(resulted_in_recall) rec, COUNT(DISTINCT recall_number) nrecalls,
       DATEDIFF('day', MIN(open_date), COALESCE(MAX(close_date), '2026-09-24'::date)) days, MIN(subject) subj
FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_INVESTIGATIONS
WHERE LEFT(nhtsa_action_number,2) IN ('PE','EA') AND open_date >= '2010-01-01'
GROUP BY 1 HAVING MIN(mfr_name) ILIKE 'Tesla%' OR NOT BOOLAND_AGG(is_closed)
ORDER BY closed, od;

-- S17 PBGC: the 13 EINs in both the 21.6K-plan list and the real trusteed list
WITH e AS (SELECT LPAD(REGEXP_REPLACE(ein,'[^0-9]',''),9,'0') ein, plan_sponsor_name, plan_name, participant_count, plan_effective_date FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_PBGC_TRUSTEED_PENSION_PLANS),
     t AS (SELECT LPAD(REGEXP_REPLACE(ein,'[^0-9]',''),9,'0') ein, sponsor_name, plan_name, date_of_plan_termination, date_of_pbgc_trusteeship, number_of_paricipants_at_date_of_plan_termination np FROM LIBRARY_MARTS.LABOR.LABOR__FED_PBGC_TRUSTEED_PLANS)
SELECT e.ein, e.plan_sponsor_name live_sponsor, e.plan_name live_plan, e.participant_count live_parts,
       t.sponsor_name trusteed_sponsor, t.plan_name trusteed_plan, t.date_of_plan_termination term, t.np trusteed_parts
FROM e JOIN t ON e.ein = t.ein ORDER BY e.participant_count DESC;

-- S18 IRS revocations x FAC, non-profits only: per EIN, the audited years that fall after revocation, with IRS master-file check
WITH rev AS (SELECT LPAD(ein,9,'0') ein, legal_name, revocation_date, reinstatement_date FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_AUTO_REVOCATIONS),
fac AS (SELECT report_id, LPAD(REGEXP_REPLACE(auditee_ein,'[^0-9]',''),9,'0') ein, auditee_name, auditee_state, audit_year, fy_start_date, fy_end_date, total_amount_expended
        FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FAC_SINGLE_AUDIT WHERE entity_type = 'non-profit' AND REGEXP_REPLACE(auditee_ein,'[^0-9]','') <> ''),
hit AS (SELECT f.*, r.legal_name, r.revocation_date, r.reinstatement_date FROM fac f JOIN rev r ON f.ein = r.ein AND f.fy_start_date >= r.revocation_date
             AND (r.reinstatement_date IS NULL OR r.reinstatement_date > f.fy_end_date)
        QUALIFY ROW_NUMBER() OVER (PARTITION BY f.report_id ORDER BY r.revocation_date DESC) = 1),
bmf AS (SELECT LPAD(ein,9,'0') ein, MAX(ruling_yyyymm) ruling, MAX(subsection_code) sub, MAX(status_code) st FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF GROUP BY 1),
per AS (SELECT h.ein, MIN(auditee_name) fac_name, MIN(legal_name) irs_name, MIN(auditee_state) st, MIN(revocation_date) rev, MIN(reinstatement_date) reinst,
               COUNT(*) yrs, MIN(audit_year) y0, MAX(audit_year) y1, SUM(total_amount_expended) dollars,
               MAX(JAROWINKLER_SIMILARITY(UPPER(auditee_name), UPPER(legal_name))) sim, MAX(b.ruling) bmf_ruling, MAX(b.st) bmf_status, MAX(b.sub) bmf_sub, BOOLOR_AGG(b.ein IS NOT NULL) in_bmf
        FROM hit h LEFT JOIN bmf b ON h.ein = b.ein GROUP BY h.ein)
SELECT per.*, COUNT(*) OVER () n_eins, SUM(IFF(sim>=85,1,0)) OVER () n_name_agree, SUM(IFF(in_bmf,1,0)) OVER () n_in_bmf,
       SUM(IFF(sim>=85 AND NOT in_bmf,1,0)) OVER () n_agree_not_bmf, SUM(IFF(sim>=85 AND NOT in_bmf, dollars, 0)) OVER () usd_agree_not_bmf,
       SUM(IFF(sim>=85 AND in_bmf AND bmf_ruling >= TO_CHAR(rev,'YYYYMM'),1,0)) OVER () n_rerecognized
FROM per ORDER BY dollars DESC LIMIT 30;

-- S19 IRS revocations x PPP $150K+ loans: name + ZIP5 match, loan approved after revocation and before any reinstatement; successor check in master file
WITH rev AS (SELECT LPAD(ein,9,'0') ein, revocation_date, reinstatement_date, UPPER(city) city,
               TRIM(REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(UPPER(legal_name),'[^A-Z0-9 ]',' '),'\b(INC|INCORPORATED|CORP|CORPORATION|THE|LLC|CO)\b',' '),'\s+',' ')) nm, LEFT(zip_code,5) z
             FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_AUTO_REVOCATIONS),
ppp AS (SELECT loannumber, TRY_TO_DATE(dateapproved,'MM/DD/YYYY') ad, currentapprovalamount amt, forgivenessamount fgv, UPPER(borrowercity) city,
               (nonprofit = 'Y' OR businesstype ILIKE 'Non-Profit%') np,
               TRIM(REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(UPPER(borrowername),'[^A-Z0-9 ]',' '),'\b(INC|INCORPORATED|CORP|CORPORATION|THE|LLC|CO)\b',' '),'\s+',' ')) nm, LEFT(borrowerzip,5) z
        FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS),
bmfk AS (SELECT DISTINCT LPAD(ein,9,'0') ein,
               TRIM(REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(UPPER(org_name),'[^A-Z0-9 ]',' '),'\b(INC|INCORPORATED|CORP|CORPORATION|THE|LLC|CO)\b',' '),'\s+',' ')) nm, LEFT(zip,5) z
         FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF),
m AS (SELECT p.*, r.ein, r.revocation_date, r.reinstatement_date, (p.city = r.city) city_ok,
             (p.ad > r.revocation_date AND (r.reinstatement_date IS NULL OR r.reinstatement_date > p.ad)) in_window
      FROM ppp p JOIN rev r ON p.nm = r.nm AND p.z = r.z WHERE LENGTH(p.nm) >= 8),
m2 AS (SELECT m.*, EXISTS (SELECT 1 FROM bmfk b WHERE b.nm = m.nm AND b.z = m.z AND b.ein <> m.ein) successor,
              EXISTS (SELECT 1 FROM bmfk b WHERE b.ein = m.ein) same_ein_in_bmf FROM m)
SELECT np, (SELECT COUNT_IF(np) FROM ppp) all_np_loans, (SELECT COUNT(*) FROM ppp) all_loans,
       COUNT(DISTINCT loannumber) matched_loans, COUNT(DISTINCT IFF(in_window, loannumber, NULL)) window_loans,
       COUNT(DISTINCT IFF(in_window AND city_ok, loannumber, NULL)) window_city_ok,
       COUNT(DISTINCT IFF(in_window AND city_ok AND NOT successor AND NOT same_ein_in_bmf, loannumber, NULL)) window_clean,
       SUM(IFF(in_window AND city_ok AND NOT successor AND NOT same_ein_in_bmf, amt, 0)) clean_amt,
       SUM(IFF(in_window AND city_ok AND NOT successor AND NOT same_ein_in_bmf, fgv, 0)) clean_forgiven
FROM m2 GROUP BY np;

-- S20 ICIJ officers x SEC insider reporting owners: US-tagged person names, key = LAST|FIRST, funnel with middle-initial and address-city checks
WITH co AS (SELECT '.*\b(INC|LLC|LP|LTD|LIMITED|FUND|CAPITAL|PARTNERS|TRUST|TRUSTEE|TRUSTEES|CORP|CORPORATION|HOLDINGS|GROUP|MANAGEMENT|BANK|ADVISORS|INVESTMENTS|COMPANY|FOUNDATION|BEARER|NOMINEES|NOMINEE|SERVICES|INTERNATIONAL|ENTERPRISES|ASSOCIATES|VENTURES|SA|AG|GMBH|BV|NV|PLC|ESTATE)\b.*' rx),
ic AS (SELECT node_id, name, source_leak,
         ARRAY_EXCEPT(SPLIT(TRIM(REGEXP_REPLACE(REGEXP_REPLACE(UPPER(name),'[^A-Z ]',' '),'\s+',' ')),' '), ARRAY_CONSTRUCT('JR','SR','II','III','IV','MR','MRS','MS','DR','')) t
       FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_OFFICERS, co
       WHERE country_codes ILIKE '%USA%' AND NOT REGEXP_LIKE(UPPER(name), co.rx)),
ic2 AS (SELECT node_id, name, source_leak, t[ARRAY_SIZE(t)-1]::string || '|' || t[0]::string k, IFF(ARRAY_SIZE(t)>=3, LEFT(t[1]::string,1), NULL) mi
        FROM ic WHERE ARRAY_SIZE(t) >= 2 AND LENGTH(t[0]::string) >= 2 AND LENGTH(t[ARRAY_SIZE(t)-1]::string) >= 2),
so AS (SELECT owner_cik, MIN(owner_name) nm, ARRAY_AGG(DISTINCT UPPER(TRIM(city))) cities, MIN(state) st
       FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_REPORTINGOWNER, co WHERE NOT REGEXP_LIKE(UPPER(owner_name), co.rx) GROUP BY owner_cik),
sk AS (SELECT owner_cik, nm, cities, st, t[0]::string || '|' || t[1]::string k, IFF(ARRAY_SIZE(t)>=3, LEFT(t[2]::string,1), NULL) mi
       FROM (SELECT so.*, ARRAY_EXCEPT(SPLIT(TRIM(REGEXP_REPLACE(REGEXP_REPLACE(UPPER(nm),'[^A-Z ]',' '),'\s+',' ')),' '), ARRAY_CONSTRUCT('JR','SR','II','III','IV','MR','MRS','MS','DR','')) t FROM so)
       WHERE ARRAY_SIZE(t) >= 2),
ku AS (SELECT k, COUNT(DISTINCT owner_cik) ncik FROM sk GROUP BY k),
m AS (SELECT i.node_id, i.name, i.k, i.mi imi, s.owner_cik, s.nm, s.mi smi, s.cities, ku.ncik
      FROM ic2 i JOIN sk s ON i.k = s.k JOIN ku ON ku.k = i.k),
addr AS (SELECT r.node_id_start node_id, a.address FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_RELATIONSHIPS r
         JOIN LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_ADDRESSES a ON a.node_id = r.node_id_end
         WHERE r.rel_type = 'registered_address' AND r.node_id_start IN (SELECT node_id FROM ic2)),
cityok AS (SELECT DISTINCT m.node_id, m.owner_cik FROM m JOIN addr ON addr.node_id = m.node_id, LATERAL FLATTEN(input => m.cities) f
           WHERE LENGTH(f.value::string) >= 4 AND CONTAINS(UPPER(addr.address), f.value::string))
SELECT (SELECT COUNT(*) FROM ic2) us_person_nodes, (SELECT COUNT(DISTINCT k) FROM ic2) us_keys,
       (SELECT COUNT(DISTINCT node_id) FROM addr) us_nodes_with_address,
       (SELECT COUNT(DISTINCT k) FROM sk) sec_keys,
       COUNT(DISTINCT m.k) matched_keys, COUNT(DISTINCT m.node_id) matched_nodes,
       COUNT(DISTINCT IFF(ncik = 1, m.k, NULL)) keys_unique_cik,
       COUNT(DISTINCT IFF(ncik = 1 AND imi = smi, m.k, NULL)) keys_uniq_mi_agree,
       COUNT(DISTINCT IFF(ncik = 1 AND imi <> smi, m.k, NULL)) keys_uniq_mi_conflict,
       COUNT(DISTINCT IFF(ncik = 1 AND (imi IS NULL OR smi IS NULL), m.k, NULL)) keys_uniq_mi_missing,
       COUNT(DISTINCT IFF(c.node_id IS NOT NULL, m.k, NULL)) keys_city_agree,
       COUNT(DISTINCT IFF(c.node_id IS NOT NULL AND ncik = 1 AND (imi = smi OR imi IS NULL OR smi IS NULL), m.k, NULL)) keys_strong
FROM m LEFT JOIN cityok c ON c.node_id = m.node_id AND c.owner_cik = m.owner_cik;

-- S21 IRS revocations trap check: rows with no reinstatement date whose EIN sits in the current IRS exempt master file
WITH rev AS (SELECT LPAD(ein,9,'0') ein, MAX(revocation_date) rev, BOOLOR_AGG(reinstatement_date IS NOT NULL) has_reinst FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_AUTO_REVOCATIONS GROUP BY 1),
bmf AS (SELECT LPAD(ein,9,'0') ein, MAX(ruling_yyyymm) ruling FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF GROUP BY 1)
SELECT has_reinst, COUNT(*) eins, COUNT(b.ein) in_bmf, COUNT_IF(b.ruling >= TO_CHAR(rev,'YYYYMM')) bmf_ruling_after_rev,
       COUNT_IF(b.ruling < TO_CHAR(rev,'YYYYMM')) bmf_ruling_before_rev, COUNT_IF(b.ruling = '000000') bmf_ruling_zero
FROM rev LEFT JOIN bmf b ON rev.ein = b.ein GROUP BY has_reinst;

-- S22 NHTSA: PE/EA probes opened 2010+ still open over 2 years; complaints on the same make/model/year and component, before vs after the open date
WITH pr AS (SELECT DISTINCT nhtsa_action_number a, make, model, model_year, SPLIT_PART(component, ':', 1) comp, open_date od
            FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_INVESTIGATIONS
            WHERE LEFT(nhtsa_action_number,2) IN ('PE','EA') AND open_date >= '2010-01-01' AND open_date < '2024-09-24' AND NOT is_closed),
cp AS (SELECT odino, make, model, model_year, component, date_received, injured, deaths FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_COMPLAINTS
       WHERE date_received >= '2005-01-01')
SELECT pr.a, MIN(pr.od) od, COUNT(DISTINCT pr.make||pr.model||pr.model_year) mmy, MIN(pr.comp) comp,
       COUNT(DISTINCT IFF(cp.date_received < pr.od, cp.odino, NULL)) cmpl_before,
       COUNT(DISTINCT IFF(cp.date_received >= pr.od, cp.odino, NULL)) cmpl_after,
       COUNT(DISTINCT IFF(cp.date_received >= pr.od AND cp.injured > 0, cp.odino, NULL)) inj_cmpl_after,
       COUNT(DISTINCT IFF(cp.date_received >= pr.od AND cp.deaths > 0, cp.odino, NULL)) death_cmpl_after,
       MAX(cp.date_received) last_cmpl
FROM pr LEFT JOIN cp ON cp.make = pr.make AND cp.model = pr.model AND cp.model_year = pr.model_year AND CONTAINS(cp.component, pr.comp)
GROUP BY pr.a ORDER BY od;

-- S23 ICIJ x SEC: the strong matches (unique CIK, middle initial not in conflict, SEC city found in the ICIJ registered address), with offshore links and SEC issuers
WITH co AS (SELECT '.*\b(INC|LLC|LP|LTD|LIMITED|FUND|CAPITAL|PARTNERS|TRUST|TRUSTEE|TRUSTEES|CORP|CORPORATION|HOLDINGS|GROUP|MANAGEMENT|BANK|ADVISORS|INVESTMENTS|COMPANY|FOUNDATION|BEARER|NOMINEES|NOMINEE|SERVICES|INTERNATIONAL|ENTERPRISES|ASSOCIATES|VENTURES|SA|AG|GMBH|BV|NV|PLC|ESTATE)\b.*' rx),
ic AS (SELECT node_id, name, source_leak,
         ARRAY_EXCEPT(SPLIT(TRIM(REGEXP_REPLACE(REGEXP_REPLACE(UPPER(name),'[^A-Z ]',' '),'\s+',' ')),' '), ARRAY_CONSTRUCT('JR','SR','II','III','IV','MR','MRS','MS','DR','')) t
       FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_OFFICERS, co
       WHERE country_codes ILIKE '%USA%' AND NOT REGEXP_LIKE(UPPER(name), co.rx)),
ic2 AS (SELECT node_id, name, source_leak, t[ARRAY_SIZE(t)-1]::string || '|' || t[0]::string k, IFF(ARRAY_SIZE(t)>=3, LEFT(t[1]::string,1), NULL) mi
        FROM ic WHERE ARRAY_SIZE(t) >= 2 AND LENGTH(t[0]::string) >= 2 AND LENGTH(t[ARRAY_SIZE(t)-1]::string) >= 2),
so AS (SELECT owner_cik, MIN(owner_name) nm, ARRAY_AGG(DISTINCT UPPER(TRIM(city))) cities, MIN(state) st, MAX(relationship) rel, MAX(title) title
       FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_REPORTINGOWNER, co WHERE NOT REGEXP_LIKE(UPPER(owner_name), co.rx) GROUP BY owner_cik),
sk AS (SELECT owner_cik, nm, cities, st, rel, title, t[0]::string || '|' || t[1]::string k, IFF(ARRAY_SIZE(t)>=3, LEFT(t[2]::string,1), NULL) mi
       FROM (SELECT so.*, ARRAY_EXCEPT(SPLIT(TRIM(REGEXP_REPLACE(REGEXP_REPLACE(UPPER(nm),'[^A-Z ]',' '),'\s+',' ')),' '), ARRAY_CONSTRUCT('JR','SR','II','III','IV','MR','MRS','MS','DR','')) t FROM so)
       WHERE ARRAY_SIZE(t) >= 2),
ku AS (SELECT k, COUNT(DISTINCT owner_cik) ncik FROM sk GROUP BY k),
m AS (SELECT i.node_id, i.name, i.source_leak, i.k, i.mi imi, s.owner_cik, s.nm, s.mi smi, s.cities, s.st, s.rel, s.title, ku.ncik
      FROM ic2 i JOIN sk s ON i.k = s.k JOIN ku ON ku.k = i.k WHERE ku.ncik = 1 AND (i.mi IS NULL OR s.mi IS NULL OR i.mi = s.mi)),
addr AS (SELECT r.node_id_start node_id, a.address FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_RELATIONSHIPS r
         JOIN LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_ADDRESSES a ON a.node_id = r.node_id_end
         WHERE r.rel_type = 'registered_address' AND r.node_id_start IN (SELECT node_id FROM m)),
strong AS (SELECT DISTINCT m.node_id, m.name, m.source_leak, m.owner_cik, m.nm, m.st, m.rel, m.title, f.value::string city, LEFT(addr.address, 70) addr
           FROM m JOIN addr ON addr.node_id = m.node_id, LATERAL FLATTEN(input => m.cities) f
           WHERE LENGTH(f.value::string) >= 4 AND CONTAINS(UPPER(addr.address), f.value::string)),
ents AS (SELECT r.node_id_start node_id, COUNT(DISTINCT r.node_id_end) n_ent, ARRAY_AGG(DISTINCT r.link) links
         FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_RELATIONSHIPS r
         WHERE r.rel_type = 'officer_of' AND r.node_id_start IN (SELECT node_id FROM strong) GROUP BY 1),
iss AS (SELECT ro.owner_cik, COUNT(DISTINCT s.issuer_cik) n_iss, LEFT(LISTAGG(DISTINCT s.issuer_name, '; '), 90) issuers
        FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_REPORTINGOWNER ro JOIN LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION s ON s.accession_number = ro.accession_number
        WHERE ro.owner_cik IN (SELECT owner_cik FROM strong) GROUP BY 1)
SELECT st.name icij_name, st.nm sec_name, st.owner_cik, st.city, st.addr, MIN(st.source_leak) leak, SUM(e.n_ent) offshore_entities, MIN(e.links::string) links,
       MIN(st.rel) rel, MIN(st.title) title, MIN(i.n_iss) n_issuers, MIN(i.issuers) issuers
FROM strong st LEFT JOIN ents e ON e.node_id = st.node_id LEFT JOIN iss i ON i.owner_cik = st.owner_cik
GROUP BY 1,2,3,4,5 ORDER BY offshore_entities DESC NULLS LAST LIMIT 70;

-- S24 ICIJ relationships: US-address intermediaries by distinct offshore entities set up (deduped across leaks)
SELECT i.name, i.countries, COUNT(DISTINCT r.node_id_end) entities, COUNT(*) link_rows, ARRAY_AGG(DISTINCT r.source_leak) leaks, MIN(r.start_date) first_d, MAX(r.start_date) last_d
FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_RELATIONSHIPS r
JOIN LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_INTERMEDIARIES i ON i.node_id = r.node_id_start
WHERE r.rel_type = 'intermediary_of' AND i.country_codes ILIKE '%USA%'
GROUP BY 1,2 ORDER BY entities DESC LIMIT 20;

-- S25 IRS x FAC clean set: non-profit auditees, name agrees (Jaro-Winkler >= 85), EIN absent from the current master file and the Puerto Rico file
WITH rev AS (SELECT LPAD(ein,9,'0') ein, legal_name, revocation_date, reinstatement_date FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_AUTO_REVOCATIONS),
fac AS (SELECT report_id, LPAD(REGEXP_REPLACE(auditee_ein,'[^0-9]',''),9,'0') ein, auditee_name, auditee_state, audit_year, fy_start_date, fy_end_date, total_amount_expended
        FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FAC_SINGLE_AUDIT WHERE entity_type = 'non-profit' AND REGEXP_REPLACE(auditee_ein,'[^0-9]','') <> ''),
hit AS (SELECT f.*, r.legal_name, r.revocation_date, r.reinstatement_date FROM fac f JOIN rev r ON f.ein = r.ein AND f.fy_start_date >= r.revocation_date
             AND (r.reinstatement_date IS NULL OR r.reinstatement_date > f.fy_end_date)
        QUALIFY ROW_NUMBER() OVER (PARTITION BY f.report_id ORDER BY r.revocation_date DESC) = 1),
bmf AS (SELECT DISTINCT LPAD(ein,9,'0') ein FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF),
pr AS (SELECT DISTINCT LPAD(ein::string,9,'0') ein FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_EO_PR),
per AS (SELECT h.ein, MIN(auditee_name) fac_name, MIN(auditee_state) st, MIN(revocation_date) rev, COUNT(*) yrs, MIN(audit_year) y0, MAX(audit_year) y1,
               SUM(total_amount_expended) dollars, MAX(JAROWINKLER_SIMILARITY(UPPER(auditee_name), UPPER(legal_name))) sim
        FROM hit h GROUP BY h.ein)
SELECT per.*, (pr.ein IS NOT NULL) in_pr_file, COUNT(*) OVER () n, SUM(dollars) OVER () usd
FROM per LEFT JOIN bmf b ON b.ein = per.ein LEFT JOIN pr ON pr.ein = per.ein
WHERE per.sim >= 85 AND b.ein IS NULL ORDER BY dollars DESC;

-- S26 NHTSA: "open" probes by decade opened (is the open flag trustworthy?), all probe types, one row per probe
WITH p AS (SELECT nhtsa_action_number a, MIN(open_date) od, MAX(close_date) cd, BOOLAND_AGG(is_closed) closed
           FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_INVESTIGATIONS GROUP BY 1)
SELECT FLOOR(YEAR(od)/10)*10 decade, COUNT(*) probes, COUNT_IF(NOT closed) open_flag, COUNT_IF(cd IS NULL) no_close_date,
       COUNT_IF(closed AND cd IS NULL) closed_no_date, COUNT_IF(NOT closed AND cd IS NOT NULL) open_with_date
FROM p GROUP BY 1 ORDER BY 1;

-- S27 NHTSA: recall share by maker after folding PE-to-EA upgrades (a PE that closed within 30 days of an EA opening at the same maker counts as upgraded, not as closed-without-recall); PE/EA opened 2010+
WITH p AS (SELECT nhtsa_action_number a, LEFT(nhtsa_action_number,2) typ, MIN(mfr_name) mfr, MIN(open_date) od, MAX(close_date) cd,
                  BOOLOR_AGG(resulted_in_recall) rec, BOOLAND_AGG(is_closed) closed
           FROM LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_INVESTIGATIONS
           WHERE LEFT(nhtsa_action_number,2) IN ('PE','EA') AND open_date >= '2010-01-01' GROUP BY 1,2),
up AS (SELECT DISTINCT pe.a FROM p pe JOIN p ea ON ea.typ = 'EA' AND pe.typ = 'PE' AND ea.mfr = pe.mfr AND pe.cd IS NOT NULL
         AND ea.od BETWEEN DATEADD('day',-30,pe.cd) AND DATEADD('day',30,pe.cd))
SELECT COALESCE(p.mfr,'__ALL__') mfr, COUNT_IF(p.closed) closed_raw, COUNT_IF(p.closed AND up.a IS NOT NULL) upgraded_pes,
       COUNT_IF(p.closed AND up.a IS NULL) closed_final, COUNT_IF(p.closed AND up.a IS NULL AND p.rec) final_recall,
       ROUND(COUNT_IF(p.closed AND up.a IS NULL AND p.rec)/NULLIF(COUNT_IF(p.closed AND up.a IS NULL),0),3) recall_share_final
FROM p LEFT JOIN up ON up.a = p.a GROUP BY ROLLUP(p.mfr) HAVING COUNT_IF(p.closed) >= 12 ORDER BY closed_raw DESC;

-- S28 IRS x FAC clean set x HUD Section 8 contracts: do the revoked housing-looking auditees hold HUD rent contracts? (name match, Jaro-Winkler >= 92 on cleaned names, same first word)
WITH rev AS (SELECT LPAD(ein,9,'0') ein, legal_name, revocation_date, reinstatement_date FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_AUTO_REVOCATIONS),
fac AS (SELECT report_id, LPAD(REGEXP_REPLACE(auditee_ein,'[^0-9]',''),9,'0') ein, auditee_name, audit_year, fy_start_date, fy_end_date, total_amount_expended
        FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FAC_SINGLE_AUDIT WHERE entity_type = 'non-profit' AND REGEXP_REPLACE(auditee_ein,'[^0-9]','') <> ''),
hit AS (SELECT f.*, r.legal_name FROM fac f JOIN rev r ON f.ein = r.ein AND f.fy_start_date >= r.revocation_date
             AND (r.reinstatement_date IS NULL OR r.reinstatement_date > f.fy_end_date)
        QUALIFY ROW_NUMBER() OVER (PARTITION BY f.report_id ORDER BY r.revocation_date DESC) = 1),
bmf AS (SELECT DISTINCT LPAD(ein,9,'0') ein FROM LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF),
per AS (SELECT h.ein, MIN(auditee_name) fac_name, COUNT(*) yrs, MAX(total_amount_expended) max_year_usd, SUM(total_amount_expended) usd,
               MAX(JAROWINKLER_SIMILARITY(UPPER(auditee_name), UPPER(legal_name))) sim FROM hit h GROUP BY h.ein),
clean AS (SELECT per.*, TRIM(REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(UPPER(REGEXP_SUBSTR(fac_name,'^[^#0-9(]+')),'[^A-Z ]',' '),'\b(INC|INCORPORATED|CORP|CORPORATION|THE|HDFC|HOUSING DEVELOPMENT FUND|OF|DBA)\b',' '),'\s+',' ')) nn
          FROM per LEFT JOIN bmf b ON b.ein = per.ein WHERE per.sim >= 85 AND b.ein IS NULL),
s8 AS (SELECT property_name, program_type_name, tracs_status_name, assisted_units_count, tracs_overall_expiration_date,
              TRIM(REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(UPPER(property_name),'[^A-Z ]',' '),'\b(INC|INCORPORATED|CORP|CORPORATION|THE|HDFC|HOUSING DEVELOPMENT FUND|OF|DBA)\b',' '),'\s+',' ')) nn
       FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_MF_SECTION8_CONTRACTS)
SELECT c.ein, c.fac_name, c.yrs, c.max_year_usd, c.usd, s8.property_name, s8.program_type_name, s8.tracs_status_name, s8.assisted_units_count, s8.tracs_overall_expiration_date,
       JAROWINKLER_SIMILARITY(c.nn, s8.nn) jw
FROM clean c JOIN s8 ON SPLIT_PART(c.nn,' ',1) = SPLIT_PART(s8.nn,' ',1) AND JAROWINKLER_SIMILARITY(c.nn, s8.nn) >= 92
ORDER BY c.usd DESC;

-- S29 Redirect: the REAL trusteed list (LABOR__FED_PBGC_TRUSTEED_PLANS), top 25 by participants at termination, and whether the sponsor EIN still files Form 5500 (padded EINs)
WITH t AS (SELECT LPAD(REGEXP_REPLACE(ein,'[^0-9]',''),9,'0') ein, sponsor_name, plan_name, date_of_plan_termination term, number_of_paricipants_at_date_of_plan_termination::number np
           FROM LIBRARY_MARTS.LABOR.LABOR__FED_PBGC_TRUSTEED_PLANS WHERE REGEXP_REPLACE(ein,'[^0-9]','') NOT IN ('', '000000000')),
f AS (SELECT LPAD(REGEXP_REPLACE(sponsor_dfe_ein::string,'[^0-9]',''),9,'0') ein, COUNT(*) filings, MIN(form_year) fy0, MAX(form_year) fy1,
             SUM(tot_partcp_boy_cnt) partcp, MIN(sponsor_dfe_name) f_name
      FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_DOL_FORM5500 GROUP BY 1)
SELECT t.ein, t.sponsor_name, t.plan_name, t.term, t.np, f.filings, f.fy0, f.fy1, f.partcp, f.f_name,
       COUNT(*) OVER () trusteed_plans, SUM(IFF(f.ein IS NOT NULL,1,0)) OVER () with_5500, (SELECT MIN(form_year)||'-'||MAX(form_year) FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_DOL_FORM5500) f5500_years
FROM t LEFT JOIN f ON f.ein = t.ein ORDER BY t.np DESC NULLS LAST LIMIT 25;

-- S30 Redo S29 on the right column: Form 5500 employer is SPONS_DFE_EIN (trap file says EIN is empty); plan year from PLAN_YEAR_BEGIN_DATE; also fill counts of the three EIN-ish columns
WITH t AS (SELECT LPAD(REGEXP_REPLACE(ein,'[^0-9]',''),9,'0') ein, sponsor_name, plan_name, date_of_plan_termination term, number_of_paricipants_at_date_of_plan_termination::number np
           FROM LIBRARY_MARTS.LABOR.LABOR__FED_PBGC_TRUSTEED_PLANS WHERE REGEXP_REPLACE(ein,'[^0-9]','') NOT IN ('', '000000000')),
raw AS (SELECT * FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_DOL_FORM5500),
fill AS (SELECT COUNT(*) n, COUNT_IF(NULLIF(TRIM(ein::string),'') IS NOT NULL) ein_filled, COUNT_IF(NULLIF(TRIM(sponsor_dfe_ein::string),'') IS NOT NULL) sponsor_dfe_ein_filled,
                COUNT_IF(NULLIF(TRIM(spons_dfe_ein::string),'') IS NOT NULL) spons_dfe_ein_filled, MIN(plan_year_begin_date) py0, MAX(plan_year_begin_date) py1 FROM raw),
f AS (SELECT LPAD(REGEXP_REPLACE(spons_dfe_ein::string,'[^0-9]',''),9,'0') ein, COUNT(*) filings, MAX(plan_year_begin_date) last_py, SUM(tot_partcp_boy_cnt) partcp, MIN(sponsor_dfe_name) f_name
      FROM raw WHERE NULLIF(TRIM(spons_dfe_ein::string),'') IS NOT NULL GROUP BY 1)
SELECT t.ein, t.sponsor_name, t.term, t.np, f.filings, f.last_py, f.partcp, f.f_name,
       COUNT(*) OVER () trusteed_plans, SUM(IFF(f.ein IS NOT NULL,1,0)) OVER () plans_sponsor_still_files,
       fill.n f5500_rows, fill.ein_filled, fill.sponsor_dfe_ein_filled, fill.spons_dfe_ein_filled, fill.py0, fill.py1
FROM t LEFT JOIN f ON f.ein = t.ein CROSS JOIN fill ORDER BY (f.ein IS NOT NULL) DESC, t.np DESC NULLS LAST LIMIT 30;
