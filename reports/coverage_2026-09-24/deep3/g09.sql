-- deep3/g09: 2026-09-24 deep pass. Python door, QUERY_TAG 'deep3-2026-09-24'.
-- Every connection first ran: ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300; ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24'.
-- Those two lines are not counted. Every statement below is a read (SELECT / WITH).
-- Tables: FDA_DEVICE_CLASSIFICATION, FDA_PURPLE_BOOK, FDA_UNII_GSRS_SUBSTANCES, NLM_DAILYMED_SPL_SETID_MAP, CMS_IRF (all LIBRARY_MARTS.HEALTH).

-- S01 UNII lookup confirm + battery top-K check
WITH t AS (SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_UNII_GSRS_SUBSTANCES)
SELECT COUNT(*) n, COUNT(DISTINCT unii) unii_nd, COUNT(DISTINCT gsrs_uuid) uuid_nd, COUNT(DISTINCT display_name) name_nd,
       (SELECT MAX(c) FROM (SELECT COUNT(*) c FROM t GROUP BY unii)) max_rows_per_unii,
       COUNT_IF(unii = 'XTN6536VE6') rows_battery_top_unii,
       COUNT_IF(NULLIF(TRIM(cas_rn),'') IS NOT NULL) cas_filled,
       (SELECT MAX(c) FROM (SELECT COUNT(*) c FROM t WHERE NULLIF(TRIM(cas_rn),'') IS NOT NULL GROUP BY cas_rn)) max_rows_per_cas,
       COUNT_IF(cas_rn = '48126-51-8') rows_battery_top_cas,
       COUNT(ec_number) ec_nn, COUNT_IF(NULLIF(TRIM(rxcui),'') IS NOT NULL) rxcui_filled,
       COUNT_IF(NULLIF(TRIM(dailymed_name),'') IS NOT NULL) dailymed_name_filled, MAX(dailymed_name) dailymed_name_max,
       COUNT(DISTINCT _source_run_id) runs,
       (SELECT OBJECT_AGG(COALESCE(substance_type,'(null)'), c) FROM (SELECT substance_type, COUNT(*) c FROM t GROUP BY 1)) by_type
FROM t;

-- S02 DailyMed lookup confirm + battery top-K check
WITH t AS (SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_NLM_DAILYMED_SPL_SETID_MAP)
SELECT COUNT(*) n, COUNT(DISTINCT setid) setid_nd, COUNT(DISTINCT zip_file_name) zip_nd,
       (SELECT MAX(c) FROM (SELECT COUNT(*) c FROM t GROUP BY setid)) max_rows_per_setid,
       COUNT_IF(setid = 'f435e79d-dea3-49dc-8268-146c60ba52a1') rows_battery_top_setid,
       MIN(upload_date) d0, MAX(upload_date) d1, COUNT_IF(upload_date > CURRENT_DATE) future,
       MAX(spl_version) max_ver, MEDIAN(spl_version) med_ver, COUNT_IF(spl_version = 1) ver1,
       COUNT_IF(NULLIF(TRIM(title),'') IS NULL) title_blank, COUNT(DISTINCT _source_run_id) runs,
       (SELECT OBJECT_AGG(y::VARCHAR, c) FROM (SELECT YEAR(upload_date) y, COUNT(*) c FROM t GROUP BY 1)) by_year,
       (SELECT ARRAY_AGG(v || ' | ' || d || ' | ' || LEFT(ti, 70)) FROM (SELECT spl_version v, upload_date d, title ti FROM t ORDER BY spl_version DESC LIMIT 6)) top_versions
FROM t;

-- S03 Device classification flags + GMP-exempt risky combos
WITH t AS (SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DEVICE_CLASSIFICATION)
SELECT COUNT(*) n, COUNT(DISTINCT product_code) code_nd,
       (SELECT MAX(c) FROM (SELECT COUNT(*) c FROM t GROUP BY product_code)) max_rows_per_code,
       COUNT_IF(product_code = 'GKP') rows_battery_top_code,
       (SELECT OBJECT_AGG(COALESCE(device_class,'(null)'), c) FROM (SELECT device_class, COUNT(*) c FROM t GROUP BY 1)) by_class,
       (SELECT OBJECT_AGG(COALESCE(gmp_exempt_flag,'(null)'), c) FROM (SELECT gmp_exempt_flag, COUNT(*) c FROM t GROUP BY 1)) gmp,
       (SELECT OBJECT_AGG(COALESCE(implant_flag,'(null)'), c) FROM (SELECT implant_flag, COUNT(*) c FROM t GROUP BY 1)) implant,
       (SELECT OBJECT_AGG(COALESCE(life_sustain_support_flag,'(null)'), c) FROM (SELECT life_sustain_support_flag, COUNT(*) c FROM t GROUP BY 1)) life,
       (SELECT OBJECT_AGG(COALESCE(NULLIF(third_party_flag,''),'(blank)'), c) FROM (SELECT third_party_flag, COUNT(*) c FROM t GROUP BY 1)) third_party,
       COUNT_IF(gmp_exempt_flag = 'Y' AND implant_flag = 'Y') gmp_exempt_implant,
       COUNT_IF(gmp_exempt_flag = 'Y' AND life_sustain_support_flag = 'Y') gmp_exempt_life,
       COUNT_IF(gmp_exempt_flag = 'Y' AND device_class = '3') gmp_exempt_class3,
       COUNT_IF(NULLIF(TRIM(medical_specialty),'') IS NULL) specialty_blank,
       (SELECT ARRAY_AGG(product_code || ' c' || device_class || ' imp' || implant_flag || ' life' || life_sustain_support_flag || ' ' || LEFT(device_name, 60))
          FROM (SELECT * FROM t WHERE gmp_exempt_flag = 'Y' AND (implant_flag = 'Y' OR life_sustain_support_flag = 'Y' OR device_class = '3') ORDER BY device_class DESC, product_code LIMIT 40)) gmp_exempt_risky
FROM t;

-- S04 Purple Book profile: license, status, date traps
WITH t AS (SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_PURPLE_BOOK)
SELECT COUNT(*) n, COUNT(DISTINCT bla_number) blas, COUNT(DISTINCT bla_number || '-' || product_number) bla_products,
       COUNT(DISTINCT purple_book_record_id) rec_ids, COUNT(DISTINCT _source_run_id) runs, COUNT(DISTINCT _src_sha256) files,
       (SELECT OBJECT_AGG(COALESCE(license_type,'(null)'), c) FROM (SELECT license_type, COUNT(*) c FROM t GROUP BY 1)) lic_type,
       (SELECT OBJECT_AGG(COALESCE(marketing_status,'(null)'), c) FROM (SELECT marketing_status, COUNT(*) c FROM t GROUP BY 1)) mkt,
       (SELECT OBJECT_AGG(COALESCE(licensure,'(null)'), c) FROM (SELECT licensure, COUNT(*) c FROM t GROUP BY 1)) licensure,
       (SELECT OBJECT_AGG(COALESCE(center,'(null)'), c) FROM (SELECT center, COUNT(*) c FROM t GROUP BY 1)) center,
       (SELECT OBJECT_AGG(COALESCE(submission_type,'(null)'), c) FROM (SELECT submission_type, COUNT(*) c FROM t GROUP BY 1)) subm,
       COUNT_IF(license_type LIKE '351(k)%' AND approval_date < '2015-03-01') k_before_first_us_biosimilar,
       COUNT_IF(approval_date < '1970-01-01') pre1970, COUNT_IF(approval_date > CURRENT_DATE) future,
       COUNT_IF(approval_date BETWEEN '1970-01-01' AND '1979-12-31') y1970s,
       (SELECT ARRAY_AGG(d || ' ' || lt || ' ' || LEFT(pn,30) || ' / ' || LEFT(ap,30)) FROM (SELECT approval_date d, license_type lt, proper_name pn, applicant ap FROM t WHERE approval_date < '1970-01-01' ORDER BY approval_date LIMIT 12)) pre1970_rows,
       (SELECT ARRAY_AGG(lic || ' | ' || ap || ' | ' || LEFT(pn,40) || ' | ' || COALESCE(d::VARCHAR,'')) FROM (SELECT licensure lic, applicant ap, proper_name pn, approval_date d FROM t WHERE licensure NOT ILIKE 'licensed' ORDER BY licensure, applicant LIMIT 40)) not_licensed_rows
FROM t;

-- S05 Purple Book biosimilars per reference product
WITH t AS (SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_PURPLE_BOOK),
k AS (SELECT LOWER(TRIM(ref_product_proper_name)) ref, * FROM t WHERE license_type LIKE '351(k)%'),
a AS (SELECT LOWER(TRIM(proper_name)) pn, MIN(approval_date) ref_first_approval, LISTAGG(DISTINCT proprietary_name, '/') ref_brands,
             LISTAGG(DISTINCT applicant, '/') ref_makers
      FROM t WHERE license_type = '351(a)' GROUP BY 1)
SELECT k.ref, a.ref_brands, a.ref_makers, a.ref_first_approval,
       COUNT(DISTINCT k.bla_number) biosimilar_blas,
       COUNT(DISTINCT IFF(k.license_type ILIKE '%interchangeable%', k.bla_number, NULL)) interchangeable_blas,
       MIN(k.approval_date) first_biosimilar, MAX(k.approval_date) last_biosimilar,
       COUNT(DISTINCT IFF(k.marketing_status ILIKE 'disc%', k.bla_number, NULL)) blas_with_disc_row,
       COUNT(DISTINCT IFF(k.marketing_status NOT ILIKE 'disc%', k.bla_number, NULL)) blas_with_rx_row,
       LISTAGG(DISTINCT LOWER(k.proper_name), ',') biosimilar_proper_names
FROM k LEFT JOIN a ON a.pn = k.ref
GROUP BY 1,2,3,4 ORDER BY biosimilar_blas DESC, k.ref;

-- S06 Purple Book x Part D prescribers: spend on reference vs biosimilar by molecule
WITH pb AS (SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_PURPLE_BOOK),
refs AS (SELECT DISTINCT LOWER(TRIM(ref_product_proper_name)) ref FROM pb WHERE license_type LIKE '351(k)%' AND ref_product_proper_name IS NOT NULL),
kname AS (SELECT LOWER(TRIM(proper_name)) pn, MIN(approval_date) k_first FROM pb WHERE license_type LIKE '351(k)%' GROUP BY 1),
pd AS (SELECT data_year, LOWER(TRIM(generic_name)) g, brand_name b, COUNT(*) prescriber_rows,
              SUM(total_claims) claims, SUM(total_drug_cost) cost
       FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PARTD_PRESCRIBERS GROUP BY 1,2,3),
yr AS (SELECT data_year, SUM(prescriber_rows) rows_all, SUM(cost) cost_all FROM pd GROUP BY 1)
SELECT r.ref, pd.data_year, IFF(k.pn IS NOT NULL, 'biosimilar', 'reference/other') role, pd.g, pd.b,
       pd.prescriber_rows, pd.claims, ROUND(pd.cost) cost, k.k_first, yr.rows_all, ROUND(yr.cost_all) cost_all
FROM pd JOIN refs r ON pd.g = r.ref OR pd.g LIKE r.ref || '-%' OR pd.g LIKE r.ref || ',%' OR pd.g LIKE r.ref || ' %'
LEFT JOIN kname k ON k.pn = pd.g
JOIN yr ON yr.data_year = pd.data_year
ORDER BY r.ref, pd.data_year, pd.cost DESC;

-- S07 Eyeball: etanercept/adalimumab 351(k) rows + Part D brand search for biosimilar names
WITH pb AS (
  SELECT 'PB' src, LOWER(ref_product_proper_name) ref, proprietary_name nm, LOWER(proper_name) generic, applicant who, bla_number || '/' || product_number id,
         license_type || ' | ' || marketing_status || ' | ' || COALESCE(submission_type,'') || ' | appr ' || COALESCE(approval_date::VARCHAR,'') || ' | interch ' || COALESCE(interchangeable_approval_date::VARCHAR,'') detail
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_PURPLE_BOOK
  WHERE license_type LIKE '351(k)%' AND LOWER(ref_product_proper_name) IN ('etanercept','adalimumab')),
pd AS (
  SELECT 'PARTD' src, NULL ref, brand_name nm, LOWER(generic_name) generic, NULL who, data_year::VARCHAR id,
         'rows ' || COUNT(*) || ' | cost ' || ROUND(SUM(total_drug_cost)) detail
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PARTD_PRESCRIBERS
  WHERE brand_name ILIKE ANY ('%amjevita%','%cyltezo%','%hyrimoz%','%hadlima%','%yusimry%','%hulio%','%idacio%','%yuflyma%','%simlandi%','%erelzi%','%eticovo%','%semglee%','%rezvoglar%')
     OR generic_name ILIKE ANY ('%etanercept%', '%adalimumab%')
  GROUP BY 1,2,3,4,5,6)
SELECT * FROM pb UNION ALL SELECT * FROM pd ORDER BY src, ref, nm, id;

-- S08 IRF profile: CCN kind x ownership, cert-date windows, physician-owned and future-dated rows
WITH t AS (
  SELECT *, CASE WHEN SUBSTR(ccn,3,1) = 'T' THEN 'unit_in_hospital' WHEN SUBSTR(ccn,3,1) = 'R' THEN 'unit_in_CAH'
                 WHEN TRY_TO_NUMBER(SUBSTR(ccn,3,4)) BETWEEN 3025 AND 3099 THEN 'freestanding' ELSE 'other:' || SUBSTR(ccn,3,2) END kind
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_IRF)
SELECT kind, ownership_type, COUNT(*) n, COUNT(DISTINCT ccn) ccns, MIN(certification_date) c0, MAX(certification_date) c1,
       COUNT_IF(certification_date > CURRENT_DATE) future_dated, COUNT_IF(certification_date >= '2019-07-01') since_2019h2,
       COUNT_IF(certification_date >= '2014-07-01' AND certification_date < '2019-07-01') y2014h2_2019h1,
       COUNT_IF(provider_name ILIKE '%ENCOMPASS%') encompass_named, COUNT_IF(state = 'FL') fl,
       COUNT_IF(TRIM(telephone_number) IN ('-','')) phone_dash,
       ARRAY_AGG(IFF(ownership_type = 'Physician' OR certification_date > CURRENT_DATE,
                     ccn || ' ' || state || ' ' || certification_date || ' ' || LEFT(provider_name,45), NULL)) odd_rows
FROM t GROUP BY 1,2 ORDER BY 1,2;

-- S09 IRF certifications by year: freestanding vs unit, for-profit, FL
WITH t AS (
  SELECT *, CASE WHEN SUBSTR(ccn,3,1) IN ('T','R') THEN 'unit'
                 WHEN TRY_TO_NUMBER(SUBSTR(ccn,3,4)) BETWEEN 3025 AND 3099 THEN 'freestanding' ELSE 'other' END kind
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_IRF)
SELECT YEAR(certification_date) y, COUNT(*) all_irf,
       COUNT_IF(kind = 'freestanding' AND ownership_type = 'For profit') fs_forprofit,
       COUNT_IF(kind = 'freestanding' AND ownership_type <> 'For profit') fs_other,
       COUNT_IF(kind = 'unit' AND ownership_type = 'For profit') unit_forprofit,
       COUNT_IF(kind = 'unit' AND ownership_type <> 'For profit') unit_other,
       COUNT_IF(provider_name ILIKE '%ENCOMPASS%') encompass_named,
       COUNT_IF(state = 'FL') fl_all, COUNT_IF(state = 'FL' AND kind = 'freestanding') fl_fs,
       COUNT_IF(state = 'FL' AND kind = 'unit') fl_unit, COUNT_IF(state = 'TX') tx_all,
       COUNT_IF(state NOT IN ('FL')) not_fl
FROM t WHERE certification_date >= '2008-01-01'
GROUP BY 1 ORDER BY 1;

-- S10 IRF new certifications by state: 5y before vs 5y after 2019-07-01
WITH t AS (
  SELECT *, CASE WHEN SUBSTR(ccn,3,1) IN ('T','R') THEN 'unit'
                 WHEN TRY_TO_NUMBER(SUBSTR(ccn,3,4)) BETWEEN 3025 AND 3099 THEN 'freestanding' ELSE 'other' END kind
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_IRF)
SELECT state, COUNT(*) now_total,
       COUNT_IF(certification_date < '2019-07-01') before_2019h2,
       COUNT_IF(certification_date >= '2014-07-01' AND certification_date < '2019-07-01') new_5y_before,
       COUNT_IF(certification_date >= '2019-07-01' AND certification_date < '2024-07-01') new_5y_after,
       COUNT_IF(certification_date >= '2024-07-01') new_since_2024h2,
       COUNT_IF(certification_date >= '2019-07-01' AND kind = 'freestanding') new_fs_after,
       COUNT_IF(certification_date >= '2019-07-01' AND kind = 'unit') new_unit_after,
       COUNT_IF(certification_date >= '2019-07-01' AND ownership_type = 'For profit') new_fp_after,
       COUNT_IF(certification_date >= '2019-07-01' AND provider_name ILIKE '%ENCOMPASS%') new_enc_after,
       ROUND(COUNT_IF(certification_date >= '2019-07-01') / NULLIF(COUNT_IF(certification_date < '2019-07-01'),0), 2) growth_ratio
FROM t GROUP BY 1 ORDER BY COUNT_IF(certification_date >= '2019-07-01') DESC, 1;

-- S11 IRF x POS_OTHER on CCN (units via parent CCN): land rate, date agreement, beds, CHOW
WITH irf AS (
  SELECT i.*, k.kind, IFF(k.kind = 'unit', SUBSTR(i.ccn,1,2) || '0' || SUBSTR(i.ccn,4,3), i.ccn) pos_ccn
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_IRF i,
       LATERAL (SELECT CASE WHEN SUBSTR(i.ccn,3,1) IN ('T','R') THEN 'unit'
                            WHEN TRY_TO_NUMBER(SUBSTR(i.ccn,3,4)) BETWEEN 3025 AND 3099 THEN 'freestanding' ELSE 'other' END kind) k),
posall AS (SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER),
scope AS (SELECT COUNT(*) pos_rows, COUNT(DISTINCT ccn) pos_ccns, COUNT_IF(prvdr_ctgry_cd = '01') pos_hosp_rows,
                 COUNT_IF(rehab_unit_sw = 'Y') pos_rehab_sw_y, MAX(crtfctn_dt) pos_max_cert, MAX(rehab_unit_efctv_dt) pos_max_rehab_eff,
                 MAX(chow_dt) pos_max_chow FROM posall),
pos AS (SELECT * FROM posall QUALIFY ROW_NUMBER() OVER (PARTITION BY ccn ORDER BY crtfctn_dt DESC NULLS LAST) = 1)
SELECT irf.kind, irf.state = 'FL' is_fl, irf.certification_date >= '2019-07-01' is_new, COUNT(*) n, COUNT(pos.ccn) landed,
       COUNT_IF(pos.pgm_trmntn_cd = '00') pos_active,
       COUNT_IF(irf.certification_date = pos.orgnl_prtcptn_dt) eq_orig_particip,
       COUNT_IF(irf.certification_date = pos.crtfctn_dt) eq_pos_cert,
       COUNT_IF(irf.certification_date = pos.rehab_unit_efctv_dt) eq_rehab_unit_eff,
       COUNT_IF(pos.rehab_unit_sw = 'Y') parent_rehab_sw_y,
       COUNT_IF(pos.chow_cnt > 0) chow_any, COUNT_IF(pos.chow_dt >= '2019-07-01') chow_since_2019h2,
       SUM(IFF(irf.kind = 'unit', pos.rehab_unit_bed_cnt, NULL)) unit_rehab_beds, SUM(IFF(irf.kind = 'freestanding', pos.bed_cnt, NULL)) fs_beds,
       ANY_VALUE(scope.pos_rows) pos_rows, ANY_VALUE(scope.pos_ccns) pos_ccns, ANY_VALUE(scope.pos_hosp_rows) pos_hosp_rows,
       ANY_VALUE(scope.pos_rehab_sw_y) pos_rehab_sw_y, ANY_VALUE(scope.pos_max_cert) pos_max_cert, ANY_VALUE(scope.pos_max_rehab_eff) pos_max_rehab_eff,
       ANY_VALUE(scope.pos_max_chow) pos_max_chow,
       ARRAY_SLICE(ARRAY_AGG(irf.ccn || ' ' || irf.certification_date || ' pos:' || COALESCE(pos.orgnl_prtcptn_dt::VARCHAR,'-') || '/' || COALESCE(pos.crtfctn_dt::VARCHAR,'-') || '/' || COALESCE(pos.rehab_unit_efctv_dt::VARCHAR,'-') || ' ' || LEFT(COALESCE(pos.fac_name, irf.provider_name),30)), 0, 3) eyeball
FROM irf LEFT JOIN pos ON pos.ccn = irf.pos_ccn CROSS JOIN scope
GROUP BY 1,2,3 ORDER BY 1,2,3;

-- S12 POS rehab-unit universe: FL vs rest, terminated units, active units missing from IRF list
WITH irfp AS (SELECT DISTINCT SUBSTR(ccn,1,2) || '0' || SUBSTR(ccn,4,3) pccn FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_IRF WHERE SUBSTR(ccn,3,1) = 'T'),
pos AS (SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER QUALIFY ROW_NUMBER() OVER (PARTITION BY ccn ORDER BY crtfctn_dt DESC NULLS LAST) = 1),
p AS (SELECT pos.*, irfp.pccn IS NOT NULL in_irf FROM pos LEFT JOIN irfp ON irfp.pccn = pos.ccn
      WHERE pos.rehab_unit_sw = 'Y' OR pos.rehab_unit_efctv_dt IS NOT NULL OR pos.rehab_unit_trmntn_dt IS NOT NULL)
SELECT state_cd = 'FL' is_fl, COUNT(*) any_rehab_unit_history,
       COUNT_IF(rehab_unit_sw = 'Y') sw_y, COUNT_IF(rehab_unit_sw = 'Y' AND pgm_trmntn_cd = '00') sw_y_hosp_active,
       COUNT_IF(rehab_unit_trmntn_dt IS NOT NULL) unit_term_dated, COUNT_IF(rehab_unit_sw = 'Y' AND rehab_unit_trmntn_dt IS NOT NULL) sw_y_but_term_dated,
       COUNT_IF(rehab_unit_efctv_dt < '2021-01-01') eff_pre2021, COUNT_IF(rehab_unit_efctv_dt < '2021-01-01' AND rehab_unit_sw = 'Y') eff_pre2021_sw_y,
       COUNT_IF(in_irf) in_irf_list,
       COUNT_IF(rehab_unit_sw = 'Y' AND pgm_trmntn_cd = '00' AND rehab_unit_trmntn_dt IS NULL AND NOT in_irf) active_unit_missing_from_irf,
       (SELECT OBJECT_AGG(COALESCE(v::VARCHAR,'null'), c) FROM (SELECT rehab_unit_trmntn_cd v, COUNT(*) c FROM p GROUP BY 1)) term_codes_all_states,
       ARRAY_SLICE(ARRAY_AGG(IFF(NOT in_irf AND rehab_unit_sw = 'Y' AND pgm_trmntn_cd = '00', ccn || ' ' || COALESCE(rehab_unit_efctv_dt::VARCHAR,'-') || ' term:' || COALESCE(rehab_unit_trmntn_dt::VARCHAR,'-') || ' beds:' || COALESCE(rehab_unit_bed_cnt::VARCHAR,'-') || ' ' || LEFT(fac_name,30), NULL)), 0, 8) sample_missing,
       (SELECT OBJECT_AGG(y::VARCHAR, c) FROM (SELECT YEAR(rehab_unit_trmntn_dt) y, COUNT(*) c FROM p WHERE rehab_unit_trmntn_dt >= '2010-01-01' GROUP BY 1)) unit_terms_by_year_all_states
FROM p GROUP BY 1 ORDER BY 1;

-- S13 FL + NC IRFs certified since 2019-07: names, owners, POS chain, beds
WITH irf AS (
  SELECT i.*, CASE WHEN SUBSTR(i.ccn,3,1) IN ('T','R') THEN 'unit'
                   WHEN TRY_TO_NUMBER(SUBSTR(i.ccn,3,4)) BETWEEN 3025 AND 3099 THEN 'fs' ELSE 'other' END kind
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_IRF i WHERE i.state IN ('FL','NC') AND i.certification_date >= '2019-07-01'),
pos AS (SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER QUALIFY ROW_NUMBER() OVER (PARTITION BY ccn ORDER BY crtfctn_dt DESC NULLS LAST) = 1)
SELECT irf.state, irf.certification_date, irf.kind, irf.ccn, irf.ownership_type, LEFT(irf.provider_name, 55) name, irf.city_town,
       pos.mlt_fac_org_name chain_in_pos, IFF(irf.kind = 'unit', pos.rehab_unit_bed_cnt, pos.bed_cnt) beds,
       pos.chow_dt last_chow
FROM irf LEFT JOIN pos ON pos.ccn = IFF(irf.kind = 'unit', SUBSTR(irf.ccn,1,2) || '0' || SUBSTR(irf.ccn,4,3), irf.ccn)
ORDER BY irf.state, irf.certification_date;

-- S14 FL POS detail: rehab-hospital CCNs (all statuses) and hospitals with rehab-unit dates
WITH pos AS (SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER QUALIFY ROW_NUMBER() OVER (PARTITION BY ccn ORDER BY crtfctn_dt DESC NULLS LAST) = 1),
irf AS (SELECT ccn, certification_date FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_IRF)
SELECT IFF(TRY_TO_NUMBER(SUBSTR(pos.ccn,3,4)) BETWEEN 3025 AND 3099, 'rehab_hospital_ccn', 'parent_with_unit') what,
       pos.ccn, LEFT(pos.fac_name, 40) fac_name, pos.city_name, pos.orgnl_prtcptn_dt, pos.pgm_trmntn_cd, pos.trmntn_exprtn_dt,
       pos.rehab_unit_efctv_dt, pos.rehab_unit_trmntn_dt, pos.rehab_unit_trmntn_cd, pos.rehab_unit_bed_cnt, pos.bed_cnt,
       COALESCE(i1.certification_date, i2.certification_date) irf_cert, pos.chow_dt
FROM pos
LEFT JOIN irf i1 ON i1.ccn = pos.ccn
LEFT JOIN irf i2 ON SUBSTR(i2.ccn,3,1) = 'T' AND SUBSTR(i2.ccn,1,2) || '0' || SUBSTR(i2.ccn,4,3) = pos.ccn
WHERE pos.state_cd = 'FL' AND pos.prvdr_ctgry_cd = '01'
  AND (TRY_TO_NUMBER(SUBSTR(pos.ccn,3,4)) BETWEEN 3025 AND 3099 OR pos.rehab_unit_efctv_dt IS NOT NULL OR pos.rehab_unit_trmntn_dt IS NOT NULL)
ORDER BY what DESC, COALESCE(pos.rehab_unit_efctv_dt, pos.orgnl_prtcptn_dt);

-- S15 Reset test: HCRIS non-acute (subprovider) beds at parent hospitals before vs after each new IRF unit date
WITH n AS (SELECT ccn, state, certification_date cd, SUBSTR(ccn,1,2) || '0' || SUBSTR(ccn,4,3) pccn
           FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_IRF WHERE SUBSTR(ccn,3,1) = 'T' AND certification_date >= '2019-07-01'),
pos AS (SELECT ccn, rehab_unit_bed_cnt ub, IFF(psych_unit_trmntn_dt IS NULL, psych_unit_bed_cnt, 0) pb
        FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER QUALIFY ROW_NUMBER() OVER (PARTITION BY ccn ORDER BY crtfctn_dt DESC NULLS LAST) = 1),
h AS (SELECT provider_ccn, fiscal_year_end_date fye, number_of_beds_total_all_subproviders - number_of_beds sub
      FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS WHERE provider_ccn IN (SELECT pccn FROM n))
SELECT n.state, n.ccn, n.cd, pos.ub unit_beds, pos.pb psych_beds,
       COUNT(h.fye) hcris_reports, MAX(h.fye) last_fye,
       ROUND(AVG(IFF(h.fye < n.cd AND h.fye >= DATEADD(year, -3, n.cd), h.sub, NULL)), 1) sub_beds_3y_before,
       ROUND(AVG(IFF(h.fye >= DATEADD(year, 1, n.cd), h.sub, NULL)), 1) sub_beds_after_1y
FROM n LEFT JOIN pos ON pos.ccn = n.pccn LEFT JOIN h ON h.provider_ccn = n.pccn
GROUP BY 1,2,3,4,5 ORDER BY n.state, n.cd;

-- S16 Freestanding rehab hospitals by state: before vs since 2019-07, with POS beds
WITH fs AS (SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_IRF WHERE TRY_TO_NUMBER(SUBSTR(ccn,3,4)) BETWEEN 3025 AND 3099),
pos AS (SELECT ccn, bed_cnt FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER QUALIFY ROW_NUMBER() OVER (PARTITION BY ccn ORDER BY crtfctn_dt DESC NULLS LAST) = 1)
SELECT fs.state, COUNT_IF(fs.certification_date < '2019-07-01') fs_before, COUNT_IF(fs.certification_date >= '2019-07-01') fs_new,
       COUNT_IF(fs.certification_date >= '2014-07-01' AND fs.certification_date < '2019-07-01') fs_new_5y_before,
       SUM(IFF(fs.certification_date < '2019-07-01', pos.bed_cnt, 0)) beds_before, SUM(IFF(fs.certification_date >= '2019-07-01', pos.bed_cnt, 0)) beds_new,
       ROUND(COUNT_IF(fs.certification_date >= '2019-07-01') / NULLIF(COUNT_IF(fs.certification_date < '2019-07-01'), 0), 2) growth
FROM fs LEFT JOIN pos ON pos.ccn = fs.ccn
GROUP BY 1 ORDER BY fs_new DESC, growth DESC;

-- S17 Conversions: new freestanding IRFs opened within 180 days of a same-city hospital rehab unit closing
WITH fs AS (SELECT ccn, state, UPPER(TRIM(city_town)) city, certification_date cd, provider_name, ownership_type
            FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_IRF
            WHERE TRY_TO_NUMBER(SUBSTR(ccn,3,4)) BETWEEN 3025 AND 3099 AND certification_date >= '2019-07-01'),
pos AS (SELECT ccn, state_cd, UPPER(TRIM(city_name)) city, fac_name, rehab_unit_trmntn_dt, rehab_unit_bed_cnt
        FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER
        WHERE rehab_unit_trmntn_dt IS NOT NULL
        QUALIFY ROW_NUMBER() OVER (PARTITION BY ccn ORDER BY crtfctn_dt DESC NULLS LAST) = 1),
m AS (SELECT fs.*, pos.ccn unit_parent, pos.fac_name unit_parent_name, pos.rehab_unit_trmntn_dt unit_closed, pos.rehab_unit_bed_cnt unit_beds
      FROM fs LEFT JOIN pos ON pos.state_cd = fs.state AND pos.city = fs.city AND ABS(DATEDIFF(day, pos.rehab_unit_trmntn_dt, fs.cd)) <= 180)
SELECT state = 'FL' is_fl, COUNT(DISTINCT ccn) new_fs, COUNT(DISTINCT IFF(unit_parent IS NOT NULL, ccn, NULL)) with_same_city_unit_close_180d,
       ARRAY_AGG(IFF(unit_parent IS NOT NULL, state || ' ' || cd || ' ' || LEFT(provider_name,35) || ' <- ' || unit_closed || ' ' || LEFT(unit_parent_name,30) || ' ' || unit_beds || 'b', NULL)) pairs
FROM m GROUP BY 1 ORDER BY 1;
