-- skeptic-g2, round 2, 2026-09-24. Python door, QUERY_TAG 'skeptic-r2-2026-09-24'.
-- Each connection opened with ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300 and the query tag (not counted).
-- 15 statements: lead 1 = 6, lead 2 = 4, lead 3 = 5. All SELECT/WITH.

-- ===== LEAD 1: HOUSING__FED_HUD_MF_SECTION8_CONTRACTS =====

-- L1-1 White Birch: every Section 8 contract row on property 800245270 or named White Birch
SELECT property_id, property_name, contract_number, tracs_status_name, program_type_name, assisted_units_count, rent_to_fmr_ratio,
  units_0br_count, units_1br_count, units_2br_count, units_3br_count, units_4br_count, fmr_0br, fmr_1br, fmr_2br, fmr_3br, fmr_4br,
  tracs_effective_date, contract_term_months_qty
FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_MF_SECTION8_CONTRACTS
WHERE TO_VARCHAR(property_id) = '800245270' OR property_name ILIKE '%WHITE BIRCH%';

-- L1-2 White Birch in HUD Picture of Subsidized Households: full rows
SELECT OBJECT_CONSTRUCT(*) o FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_ASSISTED_HOUSING_PROJECTS
WHERE name ILIKE '%WHITE BIRCH%' OR TRIM(code) ILIKE '800245270%';

-- L1-3 White Birch in HUD MF owners file: all rows on the property
SELECT OBJECT_CONSTRUCT(*) o FROM LIBRARY_RAW.LANDING.FED_HUD_MF_PROPERTIES_OWNERS WHERE TO_VARCHAR(property_id) = '800245270';

-- L1-4 PSH Project Based Section 8 (Dec 2025): per-unit HUD spending medians national / WI / Milwaukee CBSA, and White Birch's rank
WITH p AS (
  SELECT TRIM(code) code, name, state, cbsa, total_units, total_occupied, pct_occupied, spending_per_month s, rent_per_month r, quarter
  FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_ASSISTED_HOUSING_PROJECTS
  WHERE program_label = 'Project Based Section 8' AND spending_per_month > 0)
SELECT COUNT(*) n, COUNT(DISTINCT code) codes, LISTAGG(DISTINCT quarter, ',') qtrs, MEDIAN(s) nat_med,
  MEDIAN(IFF(state='WI', s, NULL)) wi_med, COUNT_IF(state='WI') wi_n,
  MEDIAN(IFF(cbsa='33340', s, NULL)) mke_med, COUNT_IF(cbsa='33340') mke_n,
  COUNT_IF(cbsa='33340' AND s >= 2574) mke_ge_wb, COUNT_IF(state='WI' AND s >= 2574) wi_ge_wb, COUNT_IF(s >= 2574) nat_ge_wb,
  COUNT_IF(s >= 2 * 859) nat_ge_2x, ROUND(MEDIAN(pct_occupied), 0) med_occ,
  ROUND(SUM(s * total_units * 12) / 1e9, 2) bn_yr_units, ROUND(SUM(s * total_occupied * 12) / 1e9, 2) bn_yr_occupied
FROM p;

-- L1-5 Milwaukee CBSA top 10 project-based Section 8 by per-unit spending, with occupancy
SELECT TRIM(code) code, name, std_city, sub_program, total_units, total_occupied, pct_occupied, spending_per_month, rent_per_month, pct_age62plus, pct_disabled_all
FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_ASSISTED_HOUSING_PROJECTS
WHERE program_label = 'Project Based Section 8' AND cbsa = '33340' AND spending_per_month > 0
ORDER BY spending_per_month DESC LIMIT 10;

-- L1-6 Recheck report totals: over-150 count, PSH-matched spending share (units x spend vs occupied x spend), ratio-to-spend correlation
WITH psh AS (
  SELECT TRY_TO_NUMBER(SPLIT_PART(TRIM(code), ' ', 1)) pid, MAX(total_units) u, MAX(total_occupied) occ, MAX(spending_per_month) spend
  FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_ASSISTED_HOUSING_PROJECTS
  WHERE program_label = 'Project Based Section 8' AND spending_per_month > 0 GROUP BY 1),
c AS (
  SELECT TRY_TO_NUMBER(TO_VARCHAR(property_id)) pid, MAX(rent_to_fmr_ratio) ratio, COUNT(*) nc
  FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_MF_SECTION8_CONTRACTS WHERE tracs_status_name = 'Active' AND rent_to_fmr_ratio > 0 GROUP BY 1),
j AS (SELECT c.*, psh.u, psh.occ, psh.spend FROM c JOIN psh USING (pid))
SELECT (SELECT COUNT_IF(rent_to_fmr_ratio > 150) FROM LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_MF_SECTION8_CONTRACTS WHERE tracs_status_name = 'Active') c150_contracts,
  COUNT(*) matched_props, COUNT_IF(ratio > 150) matched_over150, COUNT_IF(nc > 1) multi_contract_props,
  ROUND(100 * SUM(IFF(ratio > 150, u, 0)) / SUM(u), 1) pct_units_over150,
  ROUND(100 * SUM(IFF(ratio > 150, u * spend, 0)) / SUM(u * spend), 1) pct_spend_units,
  ROUND(SUM(IFF(ratio > 150, u * spend * 12, 0)) / 1e9, 2) bn_over150_units,
  ROUND(SUM(IFF(ratio > 150, occ * spend * 12, 0)) / 1e9, 2) bn_over150_occupied,
  ROUND(MEDIAN(IFF(ratio > 150, spend, NULL)), 0) med_over150, ROUND(MEDIAN(IFF(ratio <= 150, spend, NULL)), 0) med_rest,
  CORR(ratio, spend) corr_ratio_spend
FROM j;

-- ===== LEAD 2: TRANSPORT__FED_NTSB_AVIATION_AIRCRAFT =====

-- L2-1 FAA registry: full rows for the B-17 N93012 and Bering Air N321BA, to see every column
SELECT OBJECT_CONSTRUCT(*) o FROM LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FAA_AIRCRAFT_REGISTRY WHERE UPPER(TRIM(n_number)) IN ('93012', '321BA');

-- L2-2 Recompute the 420: rows vs distinct events vs distinct tails, deaths per distinct event, registry key uniqueness, post-crash activity
WITH d AS (
  SELECT DISTINCT ac.ev_id, UPPER(TRIM(ac.regis_no)) tail, UPPER(REGEXP_REPLACE(ac.acft_serial_no,'[^A-Za-z0-9]','')) ser, e.ev_date,
    TRY_TO_NUMBER(TO_VARCHAR(e.inj_tot_f)) f
  FROM LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_AIRCRAFT ac
  JOIN LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_EVENTS e ON e.ev_id = ac.ev_id
  WHERE ac.damage='DEST' AND e.ev_country='USA' AND ac.regis_no ILIKE 'N%' AND ac.acft_serial_no NOT IN ('None','')),
r AS (SELECT 'N'||UPPER(TRIM(n_number)) tail, UPPER(REGEXP_REPLACE(serial_number,'[^A-Za-z0-9]','')) rser, status_code,
  TRY_TO_DATE(TO_VARCHAR(last_action_date)) lad, TRY_TO_DATE(TO_VARCHAR(cert_issue_date)) cid, TRY_TO_DATE(TO_VARCHAR(expiration_date)) exd,
  TRY_TO_DATE(TO_VARCHAR(airworthiness_date)) awd
  FROM LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FAA_AIRCRAFT_REGISTRY),
s AS (SELECT d.*, r.lad, r.cid, r.exd, r.awd FROM d JOIN r ON r.tail = d.tail AND r.rser = d.ser WHERE r.status_code = 'V' AND r.cid < d.ev_date),
ev AS (SELECT ev_id, MAX(f) f, COUNT(*) acft FROM s GROUP BY 1)
SELECT (SELECT COUNT(*) FROM r) reg_rows, (SELECT COUNT(DISTINCT tail) FROM r) reg_tails,
  COUNT(*) stale_rows, COUNT(DISTINCT s.ev_id) stale_events, COUNT(DISTINCT s.tail) stale_tails,
  COUNT_IF(s.f > 0) fatal_rows, SUM(IFF(s.f > 0, s.f, 0)) deaths_rowsum,
  (SELECT COUNT_IF(f > 0) FROM ev) fatal_events, (SELECT SUM(IFF(f > 0, f, 0)) FROM ev) deaths_eventsum, (SELECT COUNT_IF(acft > 1) FROM ev) multi_acft_events,
  COUNT_IF(s.exd > '2026-09-24') unexpired, COUNT_IF(s.exd <= '2026-09-24') expired_but_v,
  COUNT_IF(s.lad > s.ev_date) touched_after_crash, COUNT_IF(s.awd > s.ev_date) airworthy_after_crash,
  COUNT_IF(s.lad > s.ev_date AND s.lad BETWEEN '2023-01-01' AND '2023-02-28') touched_in_jan_feb_2023,
  COUNT_IF(s.lad > s.ev_date AND YEAR(s.ev_date) <= 2023) touched_after_crash_pre2024,
  ROUND(MEDIAN(DATEDIFF('month', s.ev_date, '2026-08-09'::date)), 0) med_months_since_crash,
  ROUND(MEDIAN(DATEDIFF('month', s.cid, s.exd)), 0) med_term_months
FROM s;

-- L2-3 All destroyed same-serial tails by time since crash: still V with pre-crash cert, and how many of those the FAA touched after the crash
WITH d AS (
  SELECT DISTINCT ac.ev_id, UPPER(TRIM(ac.regis_no)) tail, UPPER(REGEXP_REPLACE(ac.acft_serial_no,'[^A-Za-z0-9]','')) ser, e.ev_date
  FROM LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_AIRCRAFT ac
  JOIN LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_EVENTS e ON e.ev_id = ac.ev_id
  WHERE ac.damage='DEST' AND e.ev_country='USA' AND ac.regis_no ILIKE 'N%' AND ac.acft_serial_no NOT IN ('None','')),
r AS (SELECT 'N'||UPPER(TRIM(n_number)) tail, UPPER(REGEXP_REPLACE(serial_number,'[^A-Za-z0-9]','')) rser, status_code,
  TRY_TO_DATE(TO_VARCHAR(last_action_date)) lad, TRY_TO_DATE(TO_VARCHAR(cert_issue_date)) cid, TRY_TO_DATE(TO_VARCHAR(expiration_date)) exd
  FROM LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FAA_AIRCRAFT_REGISTRY)
SELECT CASE WHEN DATEDIFF('month', d.ev_date, '2026-08-09'::date) < 24 THEN 'a <2y' WHEN DATEDIFF('month', d.ev_date, '2026-08-09'::date) < 48 THEN 'b 2-4y'
            WHEN DATEDIFF('month', d.ev_date, '2026-08-09'::date) < 84 THEN 'c 4-7y' ELSE 'd 7y+' END since_crash,
  COUNT(*) destroyed, COUNT_IF(r.tail IS NOT NULL AND r.rser = d.ser) same_ser_on_reg,
  COUNT_IF(r.status_code = 'V' AND r.rser = d.ser AND r.cid < d.ev_date) stale_v,
  COUNT_IF(r.status_code = 'V' AND r.rser = d.ser AND r.cid < d.ev_date AND r.lad > d.ev_date) stale_v_touched_after,
  COUNT_IF(r.status_code = 'V' AND r.rser = d.ser AND r.cid >= d.ev_date) v_new_cert_after_crash,
  COUNT_IF(r.status_code <> 'V' AND r.rser = d.ser) other_status,
  LISTAGG(DISTINCT IFF(r.rser = d.ser AND r.status_code <> 'V', r.status_code, NULL), ',') other_codes
FROM d LEFT JOIN r ON r.tail = d.tail GROUP BY 1 ORDER BY 1;

-- L2-4 The 177 stale records touched after the crash: batch days vs spread-out dates, and how far expiry sits past the touch
WITH d AS (
  SELECT DISTINCT ac.ev_id, UPPER(TRIM(ac.regis_no)) tail, UPPER(REGEXP_REPLACE(ac.acft_serial_no,'[^A-Za-z0-9]','')) ser, e.ev_date,
    TRY_TO_NUMBER(TO_VARCHAR(e.inj_tot_f)) f
  FROM LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_AIRCRAFT ac
  JOIN LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_NTSB_AVIATION_EVENTS e ON e.ev_id = ac.ev_id
  WHERE ac.damage='DEST' AND e.ev_country='USA' AND ac.regis_no ILIKE 'N%' AND ac.acft_serial_no NOT IN ('None','')),
r AS (SELECT 'N'||UPPER(TRIM(n_number)) tail, UPPER(REGEXP_REPLACE(serial_number,'[^A-Za-z0-9]','')) rser, status_code,
  TRY_TO_DATE(TO_VARCHAR(last_action_date)) lad, TRY_TO_DATE(TO_VARCHAR(cert_issue_date)) cid, TRY_TO_DATE(TO_VARCHAR(expiration_date)) exd
  FROM LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FAA_AIRCRAFT_REGISTRY),
s AS (SELECT d.*, r.lad, r.cid, r.exd FROM d JOIN r ON r.tail = d.tail AND r.rser = d.ser
      WHERE r.status_code = 'V' AND r.cid < d.ev_date AND r.lad > d.ev_date)
SELECT 'summary' k, COUNT(*) n, COUNT(DISTINCT lad) distinct_days, ROUND(MEDIAN(DATEDIFF('month', lad, exd)), 0) med_months_touch_to_exp,
  COUNT_IF(DATEDIFF('month', lad, exd) BETWEEN 80 AND 88) exp_7y_after_touch, COUNT_IF(f > 0) fatal, NULL x
FROM s
UNION ALL
SELECT * FROM (SELECT 'year', YEAR(lad), COUNT(*), NULL, NULL, COUNT_IF(f > 0), NULL FROM s GROUP BY 2 ORDER BY 2)
UNION ALL
SELECT * FROM (SELECT 'top_day', NULL, COUNT(*), NULL, NULL, NULL, lad::string FROM s GROUP BY lad ORDER BY 3 DESC LIMIT 8);

-- ===== LEAD 3: HEALTH__FED_DEA_ARCOS =====

-- L3-1 ARCOS: one Food City #674 row, every column
SELECT OBJECT_CONSTRUCT(*) o FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_DEA_ARCOS WHERE BUYER_DEA_NO = 'BF7000526' LIMIT 1;

-- L3-2 Food City #674: totals, transaction codes, measure, duplicate rows (same reporter, date, product, quantity, transaction id), row-key suffixes
WITH b AS (SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_DEA_ARCOS WHERE BUYER_DEA_NO = 'BF7000526'),
dup AS (SELECT REPORTER_DEA_NO, TRANSACTION_DATE, PRODUCT_NAME, QUANTITY, TRANSACTION_ID, COUNT(*) n, SUM(DOSAGE_UNITS) du
        FROM b WHERE TRANSACTION_CODE = 'S' GROUP BY 1,2,3,4,5 HAVING COUNT(*) > 1)
SELECT COUNT(*) rows_all, COUNT_IF(TRANSACTION_CODE = 'S') rows_s, LISTAGG(DISTINCT TRANSACTION_CODE, ',') codes,
  LISTAGG(DISTINCT MEASURE, ',') measures, SUM(IFF(TRANSACTION_CODE='S', DOSAGE_UNITS, 0)) du_s,
  SUM(IFF(TRANSACTION_CODE='S' AND DRUG_NAME='OXYCODONE' AND DOSAGE_STRENGTH >= 30, DOSAGE_UNITS, 0)) oxy30_s,
  SUM(IFF(TRANSACTION_CODE='S' AND DRUG_NAME='OXYCODONE' AND DOSAGE_STRENGTH >= 30 AND MEASURE <> 'TAB', DOSAGE_UNITS, 0)) oxy30_not_tab,
  COUNT_IF(ARCOS_ROW_KEY NOT LIKE '%-1') rowkey_suffix_not_1,
  (SELECT COUNT(*) FROM dup) dup_groups, (SELECT SUM(n - 1) FROM dup) dup_extra_rows, (SELECT SUM(du * (n - 1) / n) FROM dup) dup_extra_du,
  MIN(TRANSACTION_DATE) d0, MAX(TRANSACTION_DATE) d1, LISTAGG(DISTINCT BUYER_NAME, ' | ') names
FROM b;

-- L3-3 Food City #674: strong oxycodone by product and strength (immediate-release 30mg vs long-acting 40-80mg)
SELECT PRODUCT_NAME, DOSAGE_STRENGTH, MEASURE, SUM(DOSAGE_UNITS) du, COUNT(*) n
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_DEA_ARCOS
WHERE BUYER_DEA_NO = 'BF7000526' AND TRANSACTION_CODE = 'S' AND DRUG_NAME = 'OXYCODONE' AND DOSAGE_STRENGTH >= 30
GROUP BY 1,2,3 ORDER BY du DESC LIMIT 15;

-- L3-4 ARCOS pharmacies (retail + chain, code S) rolled up by buyer: top 15 on oxycodone 30mg+, IR-30 rank, universe, TN and FL shares, ZIP 37919
WITH b AS (
  SELECT BUYER_DEA_NO id, ANY_VALUE(BUYER_NAME) nm, ANY_VALUE(BUYER_CITY) city, ANY_VALUE(BUYER_STATE) st, ANY_VALUE(BUYER_ZIP) zip,
    SUM(DOSAGE_UNITS) du, SUM(IFF(DRUG_NAME = 'OXYCODONE' AND DOSAGE_STRENGTH >= 30, DOSAGE_UNITS, 0)) o30,
    SUM(IFF(DRUG_NAME = 'OXYCODONE' AND DOSAGE_STRENGTH = 30 AND PRODUCT_NAME NOT ILIKE '%CONTIN%' AND PRODUCT_NAME NOT ILIKE '%CR %' AND PRODUCT_NAME NOT ILIKE '%ER %', DOSAGE_UNITS, 0)) o30ir,
    COUNT(DISTINCT YEAR(TRANSACTION_DATE)) yrs
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_DEA_ARCOS
  WHERE TRANSACTION_CODE = 'S' AND BUYER_BUSINESS_ACTIVITY IN ('RETAIL PHARMACY', 'CHAIN PHARMACY')
  GROUP BY 1)
SELECT * FROM (
  SELECT 'top' k, id, nm, city, st, zip, du, o30, o30ir, ROUND(100 * o30 / du, 1) pct, yrs,
    ROW_NUMBER() OVER (ORDER BY o30 DESC) rk_o30, ROW_NUMBER() OVER (ORDER BY o30ir DESC) rk_ir
  FROM b QUALIFY rk_o30 <= 15 OR id = 'BF7000526' OR rk_ir <= 5)
UNION ALL
SELECT 'universe', NULL, NULL, NULL, NULL, NULL, SUM(du), SUM(o30), SUM(o30ir), ROUND(100 * SUM(o30) / SUM(du), 1), COUNT(*),
  NULL, NULL FROM b WHERE id NOT IN (SELECT id FROM b WHERE st IN ('SC','KS') AND du > 1e8)
UNION ALL
SELECT 'state', NULL, NULL, NULL, st, NULL, SUM(du), SUM(o30), NULL, ROUND(100 * SUM(o30) / SUM(du), 1), COUNT(*),
  ROUND(MEDIAN(du)), ROUND(MEDIAN(100 * o30 / NULLIF(du, 0)), 1) FROM b WHERE st IN ('TN','FL') GROUP BY st
UNION ALL
SELECT 'knox_zip37919', NULL, NULL, NULL, NULL, zip, SUM(du), SUM(o30), NULL, ROUND(100 * SUM(o30) / SUM(du), 1), COUNT(*), NULL, NULL
FROM b WHERE zip = '37919' GROUP BY zip
ORDER BY k, rk_o30;

-- L3-5 Food City chain peers: every buyer named FOOD CITY, share of pills that are oxycodone 30mg+, by store and by state
WITH b AS (
  SELECT BUYER_DEA_NO id, ANY_VALUE(BUYER_NAME) nm, ANY_VALUE(BUYER_CITY) city, ANY_VALUE(BUYER_STATE) st, ANY_VALUE(BUYER_ZIP) zip,
    SUM(DOSAGE_UNITS) du, SUM(IFF(DRUG_NAME = 'OXYCODONE' AND DOSAGE_STRENGTH >= 30, DOSAGE_UNITS, 0)) o30,
    SUM(IFF(YEAR(TRANSACTION_DATE) = 2012 AND DRUG_NAME = 'OXYCODONE' AND DOSAGE_STRENGTH >= 30, DOSAGE_UNITS, 0)) o30_2012
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_DEA_ARCOS
  WHERE TRANSACTION_CODE = 'S' AND BUYER_NAME ILIKE 'FOOD CITY%' AND BUYER_BUSINESS_ACTIVITY IN ('RETAIL PHARMACY', 'CHAIN PHARMACY')
  GROUP BY 1)
SELECT * FROM (SELECT 'store' k, id, nm, city, st, zip, du, o30, ROUND(100 * o30 / du, 1) pct, o30_2012, NULL n
  FROM b ORDER BY pct DESC LIMIT 6)
UNION ALL
SELECT 'chain', NULL, NULL, NULL, st, NULL, SUM(du), SUM(o30), ROUND(MEDIAN(100 * o30 / NULLIF(du, 0)), 1), NULL, COUNT(*) FROM b GROUP BY st
UNION ALL
SELECT 'chain_all', NULL, NULL, NULL, NULL, NULL, SUM(du), SUM(o30), ROUND(MEDIAN(100 * o30 / NULLIF(du, 0)), 1), NULL, COUNT(*) FROM b;
