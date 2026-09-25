-- S08 GUDID staging: what the raw blocks hold (rerun of S04, which failed on the reserved word SAMPLE)
SELECT COUNT(*) n, SYSTEM$TYPEOF(ANY_VALUE(raw)) raw_type, MIN(LEN(raw::string)) len_min, MAX(LEN(raw::string)) len_max,
       COUNT(DISTINCT raw::string) distinct_raw,
       ARRAY_SLICE(ARRAY_AGG(DISTINCT ARRAY_TO_STRING(OBJECT_KEYS(TRY_PARSE_JSON(raw::string)),',')),0,10) keysets,
       ANY_VALUE(LEFT(raw::string, 1200)) raw_sample
FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_GUDID__STAGING;

-- S09 UDS Table 3A: per age line, '--' vs zero vs counts, smallest shown count (rerun of S06 with a working line regex)
WITH t AS (SELECT bhcmisid, T3A_L1_CA, T3A_L1_CB, T3A_L2_CA, T3A_L2_CB, T3A_L3_CA, T3A_L3_CB, T3A_L4_CA, T3A_L4_CB, T3A_L5_CA, T3A_L5_CB, T3A_L6_CA, T3A_L6_CB, T3A_L7_CA, T3A_L7_CB, T3A_L8_CA, T3A_L8_CB, T3A_L9_CA, T3A_L9_CB, T3A_L10_CA, T3A_L10_CB, T3A_L11_CA, T3A_L11_CB, T3A_L12_CA, T3A_L12_CB, T3A_L13_CA, T3A_L13_CB, T3A_L14_CA, T3A_L14_CB, T3A_L15_CA, T3A_L15_CB, T3A_L16_CA, T3A_L16_CB, T3A_L17_CA, T3A_L17_CB, T3A_L18_CA, T3A_L18_CB, T3A_L19_CA, T3A_L19_CB, T3A_L20_CA, T3A_L20_CB, T3A_L21_CA, T3A_L21_CB, T3A_L22_CA, T3A_L22_CB, T3A_L23_CA, T3A_L23_CB, T3A_L24_CA, T3A_L24_CB, T3A_L25_CA, T3A_L25_CB, T3A_L26_CA, T3A_L26_CB, T3A_L27_CA, T3A_L27_CB, T3A_L28_CA, T3A_L28_CB, T3A_L29_CA, T3A_L29_CB, T3A_L30_CA, T3A_L30_CB, T3A_L31_CA, T3A_L31_CB, T3A_L32_CA, T3A_L32_CB, T3A_L33_CA, T3A_L33_CB, T3A_L34_CA, T3A_L34_CB, T3A_L35_CA, T3A_L35_CB, T3A_L36_CA, T3A_L36_CB, T3A_L37_CA, T3A_L37_CB, T3A_L38_CA, T3A_L38_CB, T3A_L39_CA, T3A_L39_CB FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_UDS_TABLE3A_PATIENTS),
long AS (SELECT bhcmisid, col, val FROM t UNPIVOT(val FOR col IN (T3A_L1_CA, T3A_L1_CB, T3A_L2_CA, T3A_L2_CB, T3A_L3_CA, T3A_L3_CB, T3A_L4_CA, T3A_L4_CB, T3A_L5_CA, T3A_L5_CB, T3A_L6_CA, T3A_L6_CB, T3A_L7_CA, T3A_L7_CB, T3A_L8_CA, T3A_L8_CB, T3A_L9_CA, T3A_L9_CB, T3A_L10_CA, T3A_L10_CB, T3A_L11_CA, T3A_L11_CB, T3A_L12_CA, T3A_L12_CB, T3A_L13_CA, T3A_L13_CB, T3A_L14_CA, T3A_L14_CB, T3A_L15_CA, T3A_L15_CB, T3A_L16_CA, T3A_L16_CB, T3A_L17_CA, T3A_L17_CB, T3A_L18_CA, T3A_L18_CB, T3A_L19_CA, T3A_L19_CB, T3A_L20_CA, T3A_L20_CB, T3A_L21_CA, T3A_L21_CB, T3A_L22_CA, T3A_L22_CB, T3A_L23_CA, T3A_L23_CB, T3A_L24_CA, T3A_L24_CB, T3A_L25_CA, T3A_L25_CB, T3A_L26_CA, T3A_L26_CB, T3A_L27_CA, T3A_L27_CB, T3A_L28_CA, T3A_L28_CB, T3A_L29_CA, T3A_L29_CB, T3A_L30_CA, T3A_L30_CB, T3A_L31_CA, T3A_L31_CB, T3A_L32_CA, T3A_L32_CB, T3A_L33_CA, T3A_L33_CB, T3A_L34_CA, T3A_L34_CB, T3A_L35_CA, T3A_L35_CB, T3A_L36_CA, T3A_L36_CB, T3A_L37_CA, T3A_L37_CB, T3A_L38_CA, T3A_L38_CB, T3A_L39_CA, T3A_L39_CB))),
p AS (SELECT bhcmisid, TO_NUMBER(REGEXP_SUBSTR(col,'L([0-9]+)_',1,1,'e',1)) line, RIGHT(col,1) sex, val,
             TRY_TO_NUMBER(REPLACE(val,',','')) num FROM long)
SELECT line,
       COUNT_IF(sex='A' AND val='--') m_dash, COUNT_IF(sex='B' AND val='--') f_dash,
       COUNT_IF(num=0) zero_cells, COUNT_IF(num IS NULL AND val<>'--') other_text,
       ARRAY_SLICE(ARRAY_AGG(DISTINCT IFF(num IS NULL AND val<>'--', val, NULL)),0,6) other_vals,
       MIN(IFF(num>0,num,NULL)) min_pos, SUM(IFF(sex='A',num,0)) male_sum, SUM(IFF(sex='B',num,0)) female_sum
FROM p GROUP BY line ORDER BY line;

-- S10 UDS Table 3A: does lines 1-38 add up to the line 39 total, and how big is the gap each '--' hides
WITH t AS (SELECT bhcmisid, T3A_L1_CA, T3A_L1_CB, T3A_L2_CA, T3A_L2_CB, T3A_L3_CA, T3A_L3_CB, T3A_L4_CA, T3A_L4_CB, T3A_L5_CA, T3A_L5_CB, T3A_L6_CA, T3A_L6_CB, T3A_L7_CA, T3A_L7_CB, T3A_L8_CA, T3A_L8_CB, T3A_L9_CA, T3A_L9_CB, T3A_L10_CA, T3A_L10_CB, T3A_L11_CA, T3A_L11_CB, T3A_L12_CA, T3A_L12_CB, T3A_L13_CA, T3A_L13_CB, T3A_L14_CA, T3A_L14_CB, T3A_L15_CA, T3A_L15_CB, T3A_L16_CA, T3A_L16_CB, T3A_L17_CA, T3A_L17_CB, T3A_L18_CA, T3A_L18_CB, T3A_L19_CA, T3A_L19_CB, T3A_L20_CA, T3A_L20_CB, T3A_L21_CA, T3A_L21_CB, T3A_L22_CA, T3A_L22_CB, T3A_L23_CA, T3A_L23_CB, T3A_L24_CA, T3A_L24_CB, T3A_L25_CA, T3A_L25_CB, T3A_L26_CA, T3A_L26_CB, T3A_L27_CA, T3A_L27_CB, T3A_L28_CA, T3A_L28_CB, T3A_L29_CA, T3A_L29_CB, T3A_L30_CA, T3A_L30_CB, T3A_L31_CA, T3A_L31_CB, T3A_L32_CA, T3A_L32_CB, T3A_L33_CA, T3A_L33_CB, T3A_L34_CA, T3A_L34_CB, T3A_L35_CA, T3A_L35_CB, T3A_L36_CA, T3A_L36_CB, T3A_L37_CA, T3A_L37_CB, T3A_L38_CA, T3A_L38_CB, T3A_L39_CA, T3A_L39_CB FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_UDS_TABLE3A_PATIENTS),
long AS (SELECT bhcmisid, col, val FROM t UNPIVOT(val FOR col IN (T3A_L1_CA, T3A_L1_CB, T3A_L2_CA, T3A_L2_CB, T3A_L3_CA, T3A_L3_CB, T3A_L4_CA, T3A_L4_CB, T3A_L5_CA, T3A_L5_CB, T3A_L6_CA, T3A_L6_CB, T3A_L7_CA, T3A_L7_CB, T3A_L8_CA, T3A_L8_CB, T3A_L9_CA, T3A_L9_CB, T3A_L10_CA, T3A_L10_CB, T3A_L11_CA, T3A_L11_CB, T3A_L12_CA, T3A_L12_CB, T3A_L13_CA, T3A_L13_CB, T3A_L14_CA, T3A_L14_CB, T3A_L15_CA, T3A_L15_CB, T3A_L16_CA, T3A_L16_CB, T3A_L17_CA, T3A_L17_CB, T3A_L18_CA, T3A_L18_CB, T3A_L19_CA, T3A_L19_CB, T3A_L20_CA, T3A_L20_CB, T3A_L21_CA, T3A_L21_CB, T3A_L22_CA, T3A_L22_CB, T3A_L23_CA, T3A_L23_CB, T3A_L24_CA, T3A_L24_CB, T3A_L25_CA, T3A_L25_CB, T3A_L26_CA, T3A_L26_CB, T3A_L27_CA, T3A_L27_CB, T3A_L28_CA, T3A_L28_CB, T3A_L29_CA, T3A_L29_CB, T3A_L30_CA, T3A_L30_CB, T3A_L31_CA, T3A_L31_CB, T3A_L32_CA, T3A_L32_CB, T3A_L33_CA, T3A_L33_CB, T3A_L34_CA, T3A_L34_CB, T3A_L35_CA, T3A_L35_CB, T3A_L36_CA, T3A_L36_CB, T3A_L37_CA, T3A_L37_CB, T3A_L38_CA, T3A_L38_CB, T3A_L39_CA, T3A_L39_CB))),
p AS (SELECT bhcmisid, TO_NUMBER(REGEXP_SUBSTR(col,'L([0-9]+)_',1,1,'e',1)) line, RIGHT(col,1) sex, val,
             TRY_TO_NUMBER(REPLACE(val,',','')) num FROM long),
c AS (SELECT bhcmisid, SUM(IFF(line<=38, COALESCE(num,0), 0)) sum138, SUM(IFF(line=39, num, 0)) tot39,
             COUNT_IF(line<=38 AND val='--') dash138, COUNT_IF(line=39 AND num IS NULL) tot_missing
      FROM p GROUP BY 1)
SELECT COUNT(*) centers, COUNT_IF(tot_missing>0) tot39_missing, COUNT_IF(tot_missing=0 AND sum138=tot39) exact,
       COUNT_IF(tot_missing=0 AND sum138<tot39) sum_under, COUNT_IF(tot_missing=0 AND sum138>tot39) sum_over,
       SUM(IFF(tot_missing=0, tot39, 0)) total_patients, SUM(IFF(tot_missing=0, tot39-sum138, 0)) total_gap,
       SUM(IFF(tot_missing=0, dash138, 0)) dash_cells,
       MIN(IFF(tot_missing=0 AND dash138>0, (tot39-sum138)/dash138, NULL)) min_gap_per_dash,
       MEDIAN(IFF(tot_missing=0 AND dash138>0, (tot39-sum138)/dash138, NULL)) med_gap_per_dash,
       MAX(IFF(tot_missing=0 AND dash138>0, (tot39-sum138)/dash138, NULL)) max_gap_per_dash,
       COUNT_IF(tot_missing=0 AND dash138=0 AND sum138<>tot39) nodash_mismatch,
       MEDIAN(IFF(tot_missing=0, tot39, NULL)) median_center, MAX(tot39) max_center, MIN(IFF(tot_missing=0, tot39, NULL)) min_center
FROM c;

-- S11 Prop 65: listings per year, mechanism, safe-harbor fill; names of the null-date rows
SELECT YEAR(date_listed) y, COUNT(*) n, COUNT(DISTINCT chemical) chems,
       COUNT_IF(type_of_toxicity ILIKE '%cancer%') cancer, COUNT_IF(type_of_toxicity ILIKE '%developmental%' OR type_of_toxicity ILIKE '%male%') repro,
       COUNT_IF(listing_mechanism ILIKE '%SQE%') sqe, COUNT_IF(listing_mechanism ILIKE '%AB%') ab,
       COUNT_IF(listing_mechanism ILIKE '%FR%') fr, COUNT_IF(listing_mechanism ILIKE '%LC%') lc,
       COUNT_IF(NULLIF(TRIM(nsrl_or_madl_g_day::string),'') IS NOT NULL) nsrl,
       ARRAY_SLICE(ARRAY_AGG(IFF(date_listed IS NULL, chemical, NULL)),0,12) null_date_names,
       ARRAY_SLICE(ARRAY_AGG(DISTINCT col_6::string),0,3) col6_vals
FROM LIBRARY_MARTS.HEALTH.HEALTH__ST_OEHHA_PROPOSITION_65_LIST GROUP BY 1 ORDER BY 1;

-- S12 Prop 65 x TRI 2023 on CAS: land rate and pounds, split by TRI's own carcinogen flag
WITH p65 AS (SELECT TRIM(cas_no) cas, MIN(chemical) p65_name,
         BOOLOR_AGG(type_of_toxicity ILIKE '%cancer%') p65_cancer,
         BOOLOR_AGG(type_of_toxicity ILIKE '%developmental%' OR type_of_toxicity ILIKE '%male%') p65_repro,
         MIN(date_listed) first_listed
       FROM LIBRARY_MARTS.HEALTH.HEALTH__ST_OEHHA_PROPOSITION_65_LIST WHERE cas_no NOT LIKE '--%' AND NULLIF(TRIM(cas_no),'') IS NOT NULL GROUP BY 1),
tri AS (SELECT TRIM(c_40_cas) cas, MAX(c_37_chemical) tri_name, MAX(c_46_carcinogen) tri_carc,
               COUNT(*) forms, COUNT(DISTINCT c_2_trifd) facs, SUM(TRY_TO_NUMBER(c_107_total_releases)) lbs,
               SUM(IFF(c_8_st='CA', TRY_TO_NUMBER(c_107_total_releases), 0)) ca_lbs
        FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023 WHERE c_50_unit_of_measure ILIKE 'Pounds' GROUP BY 1)
SELECT tri.tri_carc, (p65.cas IS NOT NULL) on_p65, COALESCE(p65.p65_cancer,FALSE) p65_cancer, COALESCE(p65.p65_repro,FALSE) p65_repro,
       COUNT(*) chems, SUM(forms) forms, SUM(lbs) lbs, SUM(ca_lbs) ca_lbs,
       ARRAY_SLICE(ARRAY_AGG(tri_name) WITHIN GROUP (ORDER BY lbs DESC),0,8) top_chems
FROM tri LEFT JOIN p65 ON p65.cas = tri.cas
GROUP BY ROLLUP(1,2,3,4) ORDER BY 1,2,3,4;

-- S13 Prop 65 x TRI 2023: which Prop 65 chemicals carry the pounds; TRI flag vs Prop 65 listing
WITH p65 AS (SELECT TRIM(cas_no) cas, MIN(chemical) p65_name,
         BOOLOR_AGG(type_of_toxicity ILIKE '%cancer%') p65_cancer,
         BOOLOR_AGG(type_of_toxicity ILIKE '%developmental%' OR type_of_toxicity ILIKE '%male%') p65_repro,
         MIN(date_listed) first_listed
       FROM LIBRARY_MARTS.HEALTH.HEALTH__ST_OEHHA_PROPOSITION_65_LIST WHERE cas_no NOT LIKE '--%' AND NULLIF(TRIM(cas_no),'') IS NOT NULL GROUP BY 1),
tri AS (SELECT TRIM(c_40_cas) cas, MAX(c_37_chemical) tri_name, MAX(c_46_carcinogen) tri_carc, MAX(c_43_classification) cls,
               COUNT(DISTINCT c_2_trifd) facs, SUM(TRY_TO_NUMBER(c_107_total_releases)) lbs,
               SUM(IFF(c_8_st='CA', TRY_TO_NUMBER(c_107_total_releases), 0)) ca_lbs,
               COUNT(DISTINCT IFF(c_8_st='CA', c_2_trifd, NULL)) ca_facs
        FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023 WHERE c_50_unit_of_measure ILIKE 'Pounds' GROUP BY 1)
SELECT tri.cas, tri_name, p65_name, tri_carc, p65_cancer, p65_repro, first_listed, facs, ROUND(lbs) lbs, ca_facs, ROUND(ca_lbs) ca_lbs
FROM tri JOIN p65 ON p65.cas = tri.cas
ORDER BY lbs DESC LIMIT 40;
