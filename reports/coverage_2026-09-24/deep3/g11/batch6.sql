-- S25 TRI 2023 trap check: same site + same CAS on more than one row (rerun of S22, which failed on the reserved word SAMPLE)
WITH d AS (SELECT c_2_trifd trifd, TRIM(c_40_cas) cas, COUNT(*) n, COUNT(DISTINCT c_36_doc_ctrl_num) docs, MAX(c_4_facility_name) name, MAX(c_8_st) st,
                  ARRAY_AGG(c_37_chemical||' '||c_49_form_type||' '||ROUND(c_107_total_releases::float)||' air '||ROUND(COALESCE(TRY_TO_DOUBLE(c_51_5_1_fugitive_air::string),0)+COALESCE(TRY_TO_DOUBLE(c_52_5_2_stack_air::string),0))) forms
           FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023 GROUP BY 1,2 HAVING COUNT(*) > 1)
SELECT (SELECT COUNT(*) FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023) all_rows, COUNT(*) dup_pairs, SUM(n) dup_rows, SUM(docs) dup_docs, COUNT_IF(st='CA') ca_dup_pairs,
       COUNT_IF(cas='100-42-5') styrene_dup_pairs,
       ARRAY_SLICE(ARRAY_AGG(name||' ['||st||'] '||cas||' :: '||ARRAY_TO_STRING(forms,' / ')) WITHIN GROUP (ORDER BY st='CA' DESC, n DESC),0,10) examples
FROM d;

-- S26 California air pounds the CAS join cannot see: unmatched TRI rows that are metal/PAC/isocyanate groups or carry TRI's own carcinogen flag (upper bound on what the styrene share misses)
WITH p65 AS (SELECT DISTINCT TRIM(cas_no) cas FROM LIBRARY_MARTS.HEALTH.HEALTH__ST_OEHHA_PROPOSITION_65_LIST
       WHERE cas_no NOT LIKE '--%' AND NULLIF(TRIM(cas_no),'') IS NOT NULL AND date_listed IS NOT NULL AND chemical NOT ILIKE '%delisted%')
SELECT COUNT(*) forms, COUNT(DISTINCT c_2_trifd) sites, ROUND(SUM(COALESCE(TRY_TO_DOUBLE(c_51_5_1_fugitive_air::string),0)+COALESCE(TRY_TO_DOUBLE(c_52_5_2_stack_air::string),0))) air,
       ARRAY_SLICE(ARRAY_AGG(c_37_chemical||' '||ROUND(COALESCE(TRY_TO_DOUBLE(c_51_5_1_fugitive_air::string),0)+COALESCE(TRY_TO_DOUBLE(c_52_5_2_stack_air::string),0))) WITHIN GROUP (ORDER BY COALESCE(TRY_TO_DOUBLE(c_51_5_1_fugitive_air::string),0)+COALESCE(TRY_TO_DOUBLE(c_52_5_2_stack_air::string),0) DESC),0,10) top_rows
FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023 t LEFT JOIN p65 ON p65.cas = TRIM(t.c_40_cas)
WHERE t.c_8_st='CA' AND t.c_50_unit_of_measure ILIKE 'Pounds' AND p65.cas IS NULL
  AND (t.c_46_carcinogen='YES' OR t.c_37_chemical ILIKE ANY ('%lead%','%nickel%','%arsenic%','%cadmium%','%chromium%','%cobalt%','%mercury%','%polycyclic%','%beryllium%','%antimony%','%diisocyanate%'));
