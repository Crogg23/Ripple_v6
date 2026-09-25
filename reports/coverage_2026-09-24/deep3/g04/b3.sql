-- S14 carbon-date both lists: newest NPPES enumeration months on each list, and NPIs deactivated per month on each list vs all of NPPES (decay curve)
WITH n AS (SELECT npi, provider_enumeration_date ed, npi_deactivation_date dd, npi_reactivation_date rd FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES),
lists AS (
  SELECT DISTINCT 'O' lst, npi FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_ORDER_AND_REFERRING
  UNION ALL
  SELECT DISTINCT 'F', npi FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FISCAL_INTERMEDIARY_SHARED_SYSTEM_ATTENDING_AND_RENDERING
),
j AS (SELECT lists.lst, n.ed, n.dd, n.rd FROM lists JOIN n ON n.npi = lists.npi)
SELECT 'enum' kind, lst, TO_CHAR(DATE_TRUNC('month', ed), 'YYYY-MM') m, COUNT(*) n FROM j WHERE ed >= '2025-01-01' GROUP BY 1, 2, 3
UNION ALL
SELECT 'enum_max', lst, TO_CHAR(MAX(ed)), COUNT_IF(ed >= '2026-01-01') FROM j GROUP BY 1, 2
UNION ALL
SELECT 'deact', lst, TO_CHAR(DATE_TRUNC('month', dd), 'YYYY-MM'), COUNT(*) FROM j WHERE dd >= '2024-07-01' AND (rd IS NULL OR rd < dd) GROUP BY 1, 2, 3
UNION ALL
SELECT 'deact', 'NPPES', TO_CHAR(DATE_TRUNC('month', dd), 'YYYY-MM'), COUNT(*) FROM n WHERE dd >= '2024-07-01' AND (rd IS NULL OR rd < dd) GROUP BY 1, 2, 3
ORDER BY 1, 3, 2;

-- S15 order/refer NPIs by NPPES deactivation status: still on FISS, billed Part B in 2024 (name agreeing), referred DME in 2024, service flags
WITH n AS (
  SELECT npi, npi_deactivation_date dd FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES
  WHERE npi_deactivation_date IS NOT NULL AND (npi_reactivation_date IS NULL OR npi_reactivation_date < npi_deactivation_date)
),
o AS (SELECT npi, ANY_VALUE(UPPER(TRIM(last_name))) ln, ANY_VALUE(partb || dme || hha || pmd || hospice) flags
      FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_ORDER_AND_REFERRING GROUP BY npi),
f AS (SELECT DISTINCT npi FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FISCAL_INTERMEDIARY_SHARED_SYSTEM_ATTENDING_AND_RENDERING),
b AS (SELECT rndrng_npi npi, UPPER(TRIM(rndrng_prvdr_last_org_name)) bln, tot_mdcr_alowd_amt amt
      FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER),
r AS (SELECT rfrg_npi npi, suplr_mdcr_alowd_amt ramt FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_REFER),
j AS (
  SELECT o.*, n.dd,
         CASE WHEN n.npi IS NULL THEN 'a_not_deactivated' WHEN n.dd < '2025-01-01' THEN 'b_deact_pre2025'
              WHEN n.dd < '2026-02-01' THEN 'c_deact_2025-01_to_2026-01' ELSE 'd_deact_2026-02+' END grp,
         IFF(f.npi IS NULL, 0, 1) in_f, b.bln, b.amt, r.ramt
  FROM o LEFT JOIN n ON n.npi = o.npi LEFT JOIN f ON f.npi = o.npi LEFT JOIN b ON b.npi = o.npi LEFT JOIN r ON r.npi = o.npi
)
SELECT grp, COUNT(*) npis, SUM(in_f) in_fiss, COUNT(bln) in_partb24, COUNT_IF(bln = ln) partb_last_agrees,
       ROUND(SUM(amt)) partb24_allowed, COUNT(ramt) in_dme_ref24, ROUND(SUM(ramt)) dme_ref24_allowed,
       COUNT_IF(flags = 'YYYYY') all5, COUNT_IF(SUBSTR(flags, 3, 1) = 'Y') hha_y, COUNT_IF(SUBSTR(flags, 5, 1) = 'Y') hospice_y,
       MIN(dd) dmin, MAX(dd) dmax
FROM j GROUP BY grp ORDER BY grp;

-- S16 eyeball: order/refer NPIs deactivated 2025-01 to 2026-01 and gone from FISS; 10 by hash plus the 5 biggest DME referrers in 2024
WITH n AS (
  SELECT npi, npi_deactivation_date dd FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES
  WHERE npi_deactivation_date >= '2025-01-01' AND npi_deactivation_date < '2026-02-01'
    AND (npi_reactivation_date IS NULL OR npi_reactivation_date < npi_deactivation_date)
),
o AS (SELECT npi, last_name, first_name, partb || dme || hha || pmd || hospice flags FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_ORDER_AND_REFERRING),
f AS (SELECT DISTINCT npi FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FISCAL_INTERMEDIARY_SHARED_SYSTEM_ATTENDING_AND_RENDERING),
b AS (SELECT rndrng_npi npi, rndrng_prvdr_last_org_name bln, rndrng_prvdr_first_name bfn, rndrng_prvdr_city bcity, rndrng_prvdr_state_abrvtn bst,
             rndrng_prvdr_type btype, tot_benes FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER),
r AS (SELECT rfrg_npi npi, suplr_mdcr_alowd_amt ramt, tot_suplr_benes rbenes FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_REFER),
j AS (
  SELECT o.npi, o.last_name, o.first_name, o.flags, n.dd, b.bln, b.bfn, b.bcity, b.bst, b.btype, b.tot_benes, r.ramt, r.rbenes
  FROM o JOIN n ON n.npi = o.npi LEFT JOIN f ON f.npi = o.npi LEFT JOIN b ON b.npi = o.npi LEFT JOIN r ON r.npi = o.npi
  WHERE f.npi IS NULL
)
SELECT * FROM (SELECT 'hash' kind, j.* FROM j ORDER BY HASH(npi) LIMIT 10)
UNION ALL
SELECT * FROM (SELECT 'top_dme', j.* FROM j WHERE ramt IS NOT NULL ORDER BY ramt DESC LIMIT 5);

-- S17 SNF: operator incorporation era, for-profit homes only, each home against its state's for-profit average; split by chain membership; top chains in the 2022+ group
WITH s AS (
  SELECT ccn s_ccn, incorporation_date inc, NULLIF(TRIM(affiliation_entity_name), '') aff
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS
),
n AS (
  SELECT cms_certification_number_ccn n_ccn, state n_state, overall_rating rating, health_inspection_rating hir,
         adjusted_total_nurse_staffing_hours_per_resident_per_day hprd, total_nursing_staff_turnover turnover,
         total_amount_of_fines_in_dollars / NULLIF(number_of_certified_beds, 0) fpb, IFF(abuse_icon = 'Y', 1, 0) abuse
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME WHERE ownership_type ILIKE 'for profit%'
),
st AS (SELECT n_state, AVG(rating) m_rating, AVG(hir) m_hir, AVG(hprd) m_hprd, AVG(turnover) m_turn, AVG(fpb) m_fpb, AVG(abuse) m_abuse FROM n GROUP BY n_state),
j AS (
  SELECT s.*, n.*, st.m_rating, st.m_hir, st.m_hprd, st.m_turn, st.m_fpb, st.m_abuse,
         CASE WHEN s.inc IS NULL THEN 'z_null' WHEN s.inc < '1900-01-01' THEN 'y_sentinel'
              WHEN s.inc >= '2022-01-01' THEN 'a_2022+' WHEN s.inc >= '2018-01-01' THEN 'b_2018-21' ELSE 'c_pre2018' END grp
  FROM s JOIN n ON n.n_ccn = s.s_ccn JOIN st ON st.n_state = n.n_state
)
SELECT 'grp' kind, grp, IFF(aff IS NULL, 'no_chain', 'chain') sub, COUNT(*) homes,
       ROUND(AVG(rating - m_rating), 3) d_rating, ROUND(MEDIAN(rating - m_rating), 2) d_rating_med,
       ROUND(AVG(hir - m_hir), 3) d_inspection, ROUND(AVG(hprd - m_hprd), 3) d_hprd, ROUND(MEDIAN(hprd - m_hprd), 3) d_hprd_med,
       ROUND(AVG(turnover - m_turn), 2) d_turnover, ROUND(AVG(fpb - m_fpb), 1) d_fines_per_bed, ROUND(AVG(abuse - m_abuse), 3) d_abuse,
       ROUND(AVG(IFF(rating = 1, 1, 0)), 3) one_star
FROM j GROUP BY ROLLUP(grp, IFF(aff IS NULL, 'no_chain', 'chain'))
UNION ALL
SELECT * FROM (
  SELECT 'chain_2022+', grp, aff, COUNT(*), ROUND(AVG(rating - m_rating), 3), ROUND(MEDIAN(rating - m_rating), 2), ROUND(AVG(hir - m_hir), 3),
         ROUND(AVG(hprd - m_hprd), 3), ROUND(MEDIAN(hprd - m_hprd), 3), ROUND(AVG(turnover - m_turn), 2), ROUND(AVG(fpb - m_fpb), 1),
         ROUND(AVG(abuse - m_abuse), 3), ROUND(AVG(IFF(rating = 1, 1, 0)), 3)
  FROM j WHERE grp = 'a_2022+' AND aff IS NOT NULL GROUP BY grp, aff ORDER BY COUNT(*) DESC LIMIT 12
)
ORDER BY kind DESC, grp, sub;

-- S18 SNF before/after test: for-profit homes whose operator company formed 2022+, health citations per year in up to 2 years before vs after that date, against same-state stable for-profit homes (operator formed pre-2018) over the same calendar windows
WITH d AS (
  SELECT cms_certification_number_ccn ccn, survey_date sd, UPPER(TRIM(scope_severity_code)) ss
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES
),
rng AS (SELECT MIN(sd) d0, MAX(sd) d1, ARRAY_AGG(DISTINCT ss) ss_vals FROM d),
nh AS (SELECT cms_certification_number_ccn ccn, state FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME WHERE ownership_type ILIKE 'for profit%'),
s AS (SELECT ccn, incorporation_date inc FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS),
t AS (
  SELECT s.ccn, nh.state, s.inc,
         GREATEST(DATEADD(day, -730, s.inc), rng.d0) b0, s.inc b1, LEAST(DATEADD(day, 730, s.inc), rng.d1) a1
  FROM s JOIN nh ON nh.ccn = s.ccn CROSS JOIN rng
  WHERE s.inc >= '2022-01-01' AND DATEDIFF(day, rng.d0, s.inc) >= 365 AND DATEDIFF(day, s.inc, rng.d1) >= 365
),
p AS (SELECT s.ccn, nh.state FROM s JOIN nh ON nh.ccn = s.ccn WHERE s.inc >= '1900-01-01' AND s.inc < '2018-01-01'),
pn AS (SELECT state, COUNT(*) n_peer FROM p GROUP BY state),
pd AS (SELECT p.state, d.sd, COUNT(*) n_all, COUNT_IF(d.ss >= 'G') n_harm FROM d JOIN p ON p.ccn = d.ccn GROUP BY 1, 2),
td AS (
  SELECT t.ccn,
         COUNT_IF(d.sd >= t.b0 AND d.sd < t.b1) tb_all, COUNT_IF(d.sd >= t.b0 AND d.sd < t.b1 AND d.ss >= 'G') tb_harm,
         COUNT_IF(d.sd >= t.b1 AND d.sd <= t.a1) ta_all, COUNT_IF(d.sd >= t.b1 AND d.sd <= t.a1 AND d.ss >= 'G') ta_harm
  FROM t LEFT JOIN d ON d.ccn = t.ccn GROUP BY t.ccn
),
tp AS (
  SELECT t.ccn,
         SUM(IFF(pd.sd >= t.b0 AND pd.sd < t.b1, pd.n_all, 0)) / ANY_VALUE(pn.n_peer) pb_all,
         SUM(IFF(pd.sd >= t.b0 AND pd.sd < t.b1, pd.n_harm, 0)) / ANY_VALUE(pn.n_peer) pb_harm,
         SUM(IFF(pd.sd >= t.b1 AND pd.sd <= t.a1, pd.n_all, 0)) / ANY_VALUE(pn.n_peer) pa_all,
         SUM(IFF(pd.sd >= t.b1 AND pd.sd <= t.a1, pd.n_harm, 0)) / ANY_VALUE(pn.n_peer) pa_harm
  FROM t JOIN pd ON pd.state = t.state JOIN pn ON pn.state = t.state GROUP BY t.ccn
),
x AS (
  SELECT t.*, td.tb_all, td.tb_harm, td.ta_all, td.ta_harm, tp.pb_all, tp.pb_harm, tp.pa_all, tp.pa_harm,
         DATEDIFF(day, t.b0, t.b1) / 365.25 yb, DATEDIFF(day, t.b1, t.a1) / 365.25 ya
  FROM t JOIN td ON td.ccn = t.ccn JOIN tp ON tp.ccn = t.ccn
)
SELECT COUNT(*) homes, MIN(inc) inc_min, MAX(inc) inc_max, (SELECT d0 FROM rng) data_start, (SELECT d1 FROM rng) data_end,
       (SELECT ss_vals FROM rng) ss_vals,
       ROUND(SUM(tb_all) / SUM(yb), 2) treated_before_py, ROUND(SUM(ta_all) / SUM(ya), 2) treated_after_py,
       ROUND(SUM(pb_all) / SUM(yb), 2) peer_before_py, ROUND(SUM(pa_all) / SUM(ya), 2) peer_after_py,
       ROUND(SUM(tb_harm) / SUM(yb), 3) treated_harm_before_py, ROUND(SUM(ta_harm) / SUM(ya), 3) treated_harm_after_py,
       ROUND(SUM(pb_harm) / SUM(yb), 3) peer_harm_before_py, ROUND(SUM(pa_harm) / SUM(ya), 3) peer_harm_after_py,
       ROUND(MEDIAN(tb_all / yb - pb_all / yb), 2) med_gap_before, ROUND(MEDIAN(ta_all / ya - pa_all / ya), 2) med_gap_after,
       COUNT_IF(tb_all = 0) treated_zero_before, COUNT_IF(ta_all = 0) treated_zero_after,
       ROUND(AVG(yb), 2) avg_years_before, ROUND(AVG(ya), 2) avg_years_after
FROM x;

-- S19 CDC: full series for Hawaii flu/pneumonia and Mississippi Alzheimer's with the US, plus the 15 biggest one-year jumps in any state-cause (50+ deaths both years)
WITH c AS (SELECT state, cause_name, year, age_adjusted_death_rate r, deaths FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_LEADING_CAUSES_STATE),
l AS (SELECT c.*, LAG(r) OVER (PARTITION BY state, cause_name ORDER BY year) pr, LAG(deaths) OVER (PARTITION BY state, cause_name ORDER BY year) pdths FROM c)
SELECT 'series' kind, state, cause_name, year, r, deaths, NULL jump
FROM c WHERE (state IN ('Hawaii', 'United States') AND cause_name = 'Influenza and pneumonia')
          OR (state IN ('Mississippi', 'United States') AND cause_name = 'Alzheimer''s disease')
UNION ALL
SELECT * FROM (
  SELECT 'jump', state, cause_name, year, r, deaths, ROUND(r / pr, 2)
  FROM l WHERE pdths >= 50 AND deaths >= 50 AND cause_name <> 'All causes' AND pr > 0
  ORDER BY ABS(LN(r / pr)) DESC LIMIT 15
)
ORDER BY kind DESC, cause_name, state, year;
