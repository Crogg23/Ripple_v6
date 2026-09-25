-- Normalize the same-rule peer test by each plant's own regulator: NOVs since 2019 vs its jurisdiction's operating majors (CA split by district); registry-level sum; tag
with f as (select PGM_SYS_ID, REGISTRY_ID, FACILITY_NAME, STATE, NAICS_CODES, AIR_POLLUTANT_CLASS_CODE cls, AIR_OPERATING_STATUS_CODE op,
     case when STATE='CA' then coalesce(LOCAL_CONTROL_REGION_NAME,'CA other') else STATE end jur from {F}),
inf as (select PGM_SYS_ID, count(distinct ACTIVITY_ID) n from {I} where ACHIEVED_DATE between '2019-01-01' and '2026-07-31' group by 1),
fn as (select f.*, coalesce(inf.n,0) n from f left join inf on inf.PGM_SYS_ID=f.PGM_SYS_ID),
reg as (select REGISTRY_ID, sum(n) n_reg, count(*) ids_reg from fn where REGISTRY_ID is not null group by 1),
maj as (select PGM_SYS_ID, n mn, percent_rank() over (partition by jur order by n) pr, rank() over (partition by jur order by n desc) rk from fn where cls='MAJ' and op='OPR'),
jd as (select jur, count(*) n_maj, avg(n) mean_n, median(n) med_n, percentile_cont(0.9) within group (order by n) p90, max(n) max_n from fn where cls='MAJ' and op='OPR' group by 1),
sub as (select distinct PGM_SYS_ID from {S} where AIR_PROGRAM_SUBPART_CODE like 'CAAMACTIIII%')
select fn.PGM_SYS_ID, left(fn.FACILITY_NAME,45) nm, fn.STATE, left(fn.jur,20) jur, fn.cls, fn.n, reg.n_reg, reg.ids_reg, maj.rk, round(maj.pr,3) pr,
  jd.n_maj, round(jd.mean_n,2) mean_n, jd.med_n, jd.p90, jd.max_n, round(fn.n/nullif(jd.mean_n,0),1) x_mean,
  iff(fn.PGM_SYS_ID in (select PGM_SYS_ID from sub),'IIII','untagged') tag
from fn left join reg on reg.REGISTRY_ID=fn.REGISTRY_ID left join maj on maj.PGM_SYS_ID=fn.PGM_SYS_ID left join jd on jd.jur=fn.jur
where fn.op='OPR' and (fn.NAICS_CODES like '%33611%' or fn.NAICS_CODES like '%336120%')
order by fn.n desc, fn.PGM_SYS_ID
