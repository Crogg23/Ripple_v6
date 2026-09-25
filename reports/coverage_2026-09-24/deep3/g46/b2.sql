-- [i3_itis_comment_contents]
select count(*) n,
  sum(iff(exp_comment ilike '%@%',1,0)) n_email,
  sum(iff(regexp_like(exp_comment, '.*[0-9]{3}[) .-]+[0-9]{3}[ .-][0-9]{4}.*', 's'),1,0)) n_phone,
  sum(iff(exp_comment ilike '%univ%' or exp_comment ilike '%college%',1,0)) n_univ,
  sum(iff(exp_comment ilike '%museum%' or exp_comment ilike '%smithsonian%',1,0)) n_museum,
  sum(iff(exp_comment ilike '%usgs%' or exp_comment ilike '%geological survey%' or exp_comment ilike '%noaa%' or exp_comment ilike '%usda%' or exp_comment ilike '%fish and wildlife%' or exp_comment ilike '%national marine fisheries%',1,0)) n_fed,
  max(iff(exp_comment ilike '%@%', year(update_date), null)) newest_email_yr,
  min(iff(exp_comment ilike '%@%', year(update_date), null)) oldest_email_yr
from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_EXPERTS

-- [t2_battery_flat_topk_exact_check]
select 'SEC DERIV_TRANS_SK (battery top 2,102)' col, count(*) n_rows, count(distinct v) n_distinct, max(c) exact_max
  from (select deriv_trans_sk v, count(*) over (partition by deriv_trans_sk) c from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_DERIV_TRANS)
union all select 'FATCA GIIN (battery top 3,797)', count(*), count(distinct v), max(c)
  from (select giin v, count(*) over (partition by giin) c from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_FATCA_FFI_LIST)
union all select 'GUDID PRIMARY_DI (battery top 4,909)', count(*), count(distinct v), max(c)
  from (select primary_di v, count(*) over (partition by primary_di) c from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_GUDID)
union all select 'control: CDC_OVERDOSE STATE (battery top 1,596)', count(*), count(distinct v), max(c)
  from (select state v, count(*) over (partition by state) c from LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_OVERDOSE)
