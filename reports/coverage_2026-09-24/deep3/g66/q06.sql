-- Google weekly spend profile: duplicates, key, rounding, zeros, week start day, name drift per ID
with w as (select *, hash(*) h from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_WEEKLY_SPEND),
nm as (select ADVERTISER_ID, count(distinct ADVERTISER_NAME) k from w group by 1)
select count(*) n, count(distinct h) distinct_rows, count(distinct ADVERTISER_ID||'|'||WEEK_START_DATE) id_week,
  count(distinct ADVERTISER_ID) ids, count(distinct ADVERTISER_NAME) names,
  (select count(*) from nm where k>1) ids_multi_name,
  count_if(try_to_number(SPEND_USD) is null) usd_unparsed, count_if(try_to_number(SPEND_USD)=0) usd_zero,
  count_if(mod(try_to_number(SPEND_USD),100)<>0) usd_not_100_step,
  sum(try_to_number(SPEND_USD)) usd_total, max(try_to_number(SPEND_USD)) usd_max_week,
  count_if(try_to_number(SPEND_USD)=0 and (try_to_number(SPEND_EUR)>0 or try_to_number(SPEND_INR)>0 or try_to_number(SPEND_GBP)>0 or try_to_number(SPEND_BRL)>0 or try_to_number(SPEND_AUD)>0 or try_to_number(SPEND_MXN)>0)) usd0_other_ccy_pos,
  count_if(try_to_number(SPEND_USD)>0 and try_to_number(SPEND_EUR)=0 and try_to_number(SPEND_INR)=0 and try_to_number(SPEND_GBP)=0) usd_only_pos,
  listagg(distinct dayname(WEEK_START_DATE), ',') week_start_days,
  min(WEEK_START_DATE) w0, max(WEEK_START_DATE) w1, count(distinct WEEK_START_DATE) weeks
from w
