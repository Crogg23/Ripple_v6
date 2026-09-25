-- independent file: Home Health Compare CERTIFICATION_DATE and its own ZIP/state. (a) Valley share by cert era, (b) are 2019+ enrollment IDs new agencies or old CCNs re-enrolled, (c) Compare CCNs missing from the enrollment file (survivorship lens)
with e as (select lpad(trim(CCN),6,'0') ccn, STATE est, left(trim(ZIP_CODE),3) ez3, try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD') ed
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS),
h as (select lpad(trim(CCN),6,'0') ccn, STATE hst, left(trim(ZIP_CODE),3) hz3, CERTIFICATION_DATE cd from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH),
j as (select coalesce(e.ccn,h.ccn) ccn, e.ccn is not null in_enr, h.ccn is not null in_hc, est, ez3, hst, hz3, ed, cd,
        iff(coalesce(est,hst)='CA' and coalesce(ez3,hz3) between '912' and '916','valley','rest') rg,
        iff(hst='CA' and hz3 between '912' and '916','valley','rest') hrg
      from e full outer join h on e.ccn=h.ccn)
select 'hc_cert_era_own_zip' k, hrg a, case when cd is null then 'z_null' when year(cd)<2013 then 'a_pre2013' when year(cd)<2019 then 'b_2013_18' else 'c_2019on' end b,
  count(*) n, count_if(in_enr) c, count_if(not in_enr) d from j where in_hc group by 2,3
union all
select 'enr2019_vs_cert', rg, case when not in_hc then 'not_in_hc' when cd is null then 'cert_null' when cd < '2019-01-01' then 'cert_pre2019'
  when cd < dateadd(day,-365,ed) then 'cert_gt1y_before_enr' else 'cert_after_or_near_enr' end, count(*), null, null
from j where in_enr and year(ed)>=2019 group by 2,3
union all select 'hc_rows_vs_ccn', null, null, count(*), count(distinct ccn), null from h
union all select 'zip3_disagree', rg, null, count_if(in_enr and in_hc), count_if(in_enr and in_hc and ez3<>hz3), count_if(in_enr and in_hc and (ez3 between '912' and '916') <> (hz3 between '912' and '916')) from j group by 2
union all select 'hc_max_cert', max(cd)::text, null, count_if(year(cd)>=2025), null, null from h
order by 1,2,3
