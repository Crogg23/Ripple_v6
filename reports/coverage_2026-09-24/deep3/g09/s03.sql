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
FROM t
