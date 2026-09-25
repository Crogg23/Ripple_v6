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
SELECT * FROM pb UNION ALL SELECT * FROM pd ORDER BY src, ref, nm, id
