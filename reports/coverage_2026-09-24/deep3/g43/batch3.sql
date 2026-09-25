-- [12] frs_source_labels_big_counties  (the FRS rows behind 5 big mislabeled dim rows: which state and county names they carry)
select lpad(trim("FIPS_CODE"),5,'0') fips, trim("STATE_CODE") st, count(*) n,
       array_slice(array_agg(distinct upper(trim("COUNTY_NAME"))),0,5) names
from LIBRARY_RAW.LANDING.FED_EPA_FRS_FULL
where regexp_like(trim("FIPS_CODE"),'^[0-9]{4,5}$')
  and lpad(trim("FIPS_CODE"),5,'0') in ('06073','48201','06085','34029','12057')
group by 1,2 order by 1, 3 desc;

-- [13] dim_label_vs_frs_majority  (is the dim's state label the majority state among its own FRS rows?)
with f as (select lpad(trim("FIPS_CODE"),5,'0') fips, coalesce(trim("STATE_CODE"),'?') st
           from LIBRARY_RAW.LANDING.FED_EPA_FRS_FULL where regexp_like(trim("FIPS_CODE"),'^[0-9]{4,5}$')),
s as (select fips, st, count(*) n from f group by 1,2),
m as (select fips, st maj_st, n, sum(n) over (partition by fips) tot from s
      qualify row_number() over (partition by fips order by n desc)=1),
d as (select FIPS_CODE, coalesce(STATE_ABBR,'?') STATE_ABBR, FACILITY_COUNT from LIBRARY_MARTS.REFERENCE.REF__DIM_GEOGRAPHY
      where regexp_like(FIPS_CODE,'^[0-9]{5}$') and left(FIPS_CODE,2)<>'00')
select count(*) dim_rows, count(m.fips) in_frs, count_if(d.STATE_ABBR = m.maj_st) label_is_majority,
       count_if(d.STATE_ABBR <> m.maj_st) label_not_majority, sum(iff(d.STATE_ABBR <> m.maj_st, d.FACILITY_COUNT,0)) fac_on_wrong_label,
       sum(m.n)/sum(m.tot) frs_majority_share,
       array_slice(array_agg(iff(d.STATE_ABBR<>m.maj_st, d.FIPS_CODE||' dim='||d.STATE_ABBR||' frs_major='||m.maj_st||' '||m.n||'/'||m.tot, null))
                   within group (order by m.tot desc),0,15) worst
from d left join m on m.fips=d.FIPS_CODE;
