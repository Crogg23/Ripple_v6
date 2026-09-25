-- Google creative ID crosswalk: is it 1-to-1, why do IDs repeat 1.8K times, and does it land in CREATIVE_STATS?
with m as (select OLDCREATIVEID o, NEWCREATIVEID nw from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_GOOGLE_POLADS_CREATIVE_ID_MAPPING),
oc as (select o, count(*) c, count(distinct nw) dn from m group by 1),
cs as (select distinct AD_ID from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_GOOGLE_POLADS_CREATIVE_STATS)
select (select count(*) from m) n, (select count(distinct o) from m) d_old, (select count(distinct nw) from m) d_new,
  (select count(distinct o||'|'||coalesce(nw,'')) from m) d_pairs,
  (select count_if(nw is null or trim(nw)='') from m) new_blank,
  (select count(*) from oc where c>1) old_repeated, (select max(c) from oc) max_rows_one_old, (select max(dn) from oc) max_new_per_old,
  (select count(*) from oc where c between 1700 and 1900) old_ids_near_1800,
  (select count(distinct nw) from m join cs on cs.AD_ID = m.nw) new_in_stats,
  (select count(distinct o) from m join cs on cs.AD_ID = m.o) old_in_stats,
  (select count(*) from cs) stats_ads
