-- deep3 / g69: proper look at five glance-only immigration tables, 2026-09-24
-- Tables: IMMIGRATION__FED_DHS_YEARBOOK, IMMIGRATION__FED_ICE_STATISTICS, IMMIGRATION__FED_USCIS_DATA,
--         IMMIGRATION__FED_EOIR_CASE_DATA, IMMIGRATION__XC_OWID_REFUGEES
-- Door: Python (connect/db.py) via g69/run.py. Every connection first ran:
--   ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
--   ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';
-- Read-only: the runner refuses anything that is not SELECT / WITH. Raw results in g69/<label>.json.
-- Statement numbers below count only SELECT/WITH statements against the 35 budget.

-- [q01] statement 1
-- All columns of the 5 tables, with type and the table row counts
select c.TABLE_NAME, c.ORDINAL_POSITION, c.COLUMN_NAME, c.DATA_TYPE, t.ROW_COUNT, t.BYTES, t.LAST_ALTERED::date la
from LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS c
join LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES t on t.TABLE_SCHEMA=c.TABLE_SCHEMA and t.TABLE_NAME=c.TABLE_NAME
where c.TABLE_SCHEMA='IMMIGRATION' and c.TABLE_NAME in ('IMMIGRATION__FED_DHS_YEARBOOK','IMMIGRATION__FED_ICE_STATISTICS','IMMIGRATION__FED_USCIS_DATA','IMMIGRATION__FED_EOIR_CASE_DATA','IMMIGRATION__XC_OWID_REFUGEES')
order by 1,2;

-- [q02] statement 2
-- EOIR: shape of the one loaded column. Rows grouped by number of tab separators; distinct rows, distinct first field, lengths, two samples
select regexp_count(CASE_TYPE, '\t') tabs, count(*) n, count(distinct CASE_TYPE) distinct_rows,
  count(distinct split_part(CASE_TYPE, '\t', 1)) distinct_f1,
  min(length(CASE_TYPE)) minlen, max(length(CASE_TYPE)) maxlen, avg(length(CASE_TYPE))::int avglen,
  count_if(CASE_TYPE like '%' || char(0) || '%') has_nul,
  min(CASE_TYPE) samp_min, max(CASE_TYPE) samp_max
from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EOIR_CASE_DATA
group by 1 order by 2 desc;

-- [q03] statement 3
-- DHS yearbook: all 27 rows (tiny table, pull whole)
select * from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_DHS_YEARBOOK order by YEARBOOK_EDITION;

-- [q04] statement 4
-- ICE statistics: all 204 rows (tiny table, pull whole)
select * from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_STATISTICS;

-- [q05] statement 5
-- USCIS data: all 177 rows (tiny table, pull whole)
select * from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_USCIS_DATA;

-- [q06] statement 6
-- EOIR: identify the 39 tab fields on a 2% row sample (38-tab rows only). Per field: filled share, distinct, top values
with s as (select CASE_TYPE from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EOIR_CASE_DATA sample bernoulli (2)
           where regexp_count(CASE_TYPE, '\t') = 38),
f as (select x.index + 1 fld, trim(replace(x.value::string, char(0), '')) v from s, lateral flatten(input => split(s.CASE_TYPE, '\t')) x)
select fld, count(*) n, count_if(v <> '') filled, approx_count_distinct(nullif(v,'')) nd,
  approx_top_k(nullif(v,''), 8) top, min(nullif(v,'')) mn, max(nullif(v,'')) mx
from f group by 1 order by 1;

-- [q07] statement 7
-- EOIR (A_TblCase layout, 39 tab fields; fields named from the sample profile q06): cases by month of DATE_DETAINED (field 32), 2018-01 to 2026-05.
-- Per month: cases, still detained now, entry-to-detention gap buckets (DATE_OF_ENTRY field 24), LPR flag, priority codes, age at detention (birth M/YYYY field 26), sex, attorney notice (E_28 field 11)
with p as (
  select split_part(CASE_TYPE, '\t', 1) idn, split_part(CASE_TYPE, '\t', 7) nat, split_part(CASE_TYPE, '\t', 9) cust,
    trim(split_part(CASE_TYPE, '\t', 11)) e28, split_part(CASE_TYPE, '\t', 14) site,
    try_to_date(left(split_part(CASE_TYPE, '\t', 24), 10), 'YYYY-MM-DD') entry,
    trim(split_part(CASE_TYPE, '\t', 26)) birth, split_part(CASE_TYPE, '\t', 31) sex,
    try_to_date(left(split_part(CASE_TYPE, '\t', 32), 10), 'YYYY-MM-DD') det,
    split_part(CASE_TYPE, '\t', 34) lpr, trim(split_part(CASE_TYPE, '\t', 39)) prio
  from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EOIR_CASE_DATA
  where regexp_count(CASE_TYPE, '\t') = 38),
q as (select *, case when birth like '%/%' then datediff(month, date_from_parts(try_to_number(split_part(birth,'/',2)), try_to_number(split_part(birth,'/',1)), 1), det)/12.0 end age,
             datediff(day, entry, det) gap from p where det >= '2018-01-01' and det < '2026-06-01')
select date_trunc(month, det)::date mo, count(*) n, count_if(cust='D') still_d, count_if(cust='R') rel, count_if(cust='N') never,
  count_if(entry is not null) entry_known, count_if(gap between 0 and 30) g_0_30d, count_if(gap between 31 and 730) g_1m_2y,
  count_if(gap between 731 and 3652) g_2_10y, count_if(gap > 3652) g_10y_plus, count_if(gap < 0) g_neg,
  count_if(lpr='1') lpr1, count_if(prio='AWC/D') awc_d, count_if(prio='RBC/D') rbc_d, count_if(prio='UC') uc, count_if(prio='AWC/ATD') awc_atd,
  count_if(age is not null) age_known, count_if(age < 18) minor, count_if(age < 6) under6, count_if(sex='F') female,
  count_if(e28 <> '') has_e28, count_if(nat='MX') mx, count_if(nat in ('GT','HO','ES')) nt, count_if(nat='VE') ve
from q group by 1 order by 1;

-- [q08] statement 8
-- EOIR: how old was the court case when the person was detained? IDNCASE (field 1) is a sequence number.
-- Calendar: median IDNCASE of "fresh" cases (entry-to-detention gap 0-30 days) per detention quarter = the number being handed out then.
-- A detained case is "old" if its IDNCASE is below the calendar marker 8 quarters (2 years) before its detention quarter.
with p as (
  select try_to_number(split_part(CASE_TYPE, '\t', 1)) idn, trim(split_part(CASE_TYPE, '\t', 11)) e28,
    try_to_date(left(split_part(CASE_TYPE, '\t', 11), 10), 'YYYY-MM-DD') e28d,
    try_to_date(left(split_part(CASE_TYPE, '\t', 24), 10), 'YYYY-MM-DD') entry,
    try_to_date(left(split_part(CASE_TYPE, '\t', 32), 10), 'YYYY-MM-DD') det
  from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EOIR_CASE_DATA
  where regexp_count(CASE_TYPE, '\t') = 38),
d as (select *, date_trunc(quarter, det)::date qtr, datediff(day, entry, det) gap from p where det >= '2012-01-01' and det < '2026-06-01'),
cal as (select qtr, count(*) fresh_n, median(idn) med_idn, min(idn) min_idn, max(idn) max_idn from d where gap between 0 and 30 group by 1)
select d.qtr, c.fresh_n, c.med_idn, c.min_idn, c.max_idn, c8.med_idn marker_2y_before, count(*) detained,
  count_if(d.idn < c8.med_idn) old_case_2y, count_if(d.idn < c8.med_idn and d.gap > 730) old_case_2y_entry_2y,
  count_if(d.idn < c8.med_idn and d.e28d < d.det) old_case_lawyer_before_det,
  count_if(d.e28 <> '') has_e28, count_if(d.e28d < d.det) e28_before_det
from d join cal c on c.qtr = d.qtr
left join cal c8 on c8.qtr = dateadd(quarter, -8, d.qtr)
group by 1,2,3,4,5,6 order by 1;

-- [q09] statement 9
-- EOIR: "old case" detentions (case number 2+ years old at detention, per the q08 calendar) in Jan-May 2019, 2024, 2026.
-- Totals per window plus by nationality (field 7). Checks: hearing on/after detention (field 15), future hearing, lawyer before detention, 10y+ in US, custody now, case type
with p as (
  select try_to_number(split_part(CASE_TYPE, '\t', 1)) idn, split_part(CASE_TYPE, '\t', 7) nat, split_part(CASE_TYPE, '\t', 9) cust,
    split_part(CASE_TYPE, '\t', 13) ctype, split_part(CASE_TYPE, '\t', 14) site,
    try_to_date(left(split_part(CASE_TYPE, '\t', 11), 10), 'YYYY-MM-DD') e28d,
    try_to_date(left(split_part(CASE_TYPE, '\t', 15), 10), 'YYYY-MM-DD') hear,
    try_to_date(left(split_part(CASE_TYPE, '\t', 24), 10), 'YYYY-MM-DD') entry,
    try_to_date(left(split_part(CASE_TYPE, '\t', 32), 10), 'YYYY-MM-DD') det
  from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EOIR_CASE_DATA
  where regexp_count(CASE_TYPE, '\t') = 38),
d as (select *, date_trunc(quarter, det)::date qtr, datediff(day, entry, det) gap from p where det >= '2012-01-01' and det < '2026-06-01'),
cal as (select qtr, median(idn) med_idn from d where gap between 0 and 30 group by 1),
o as (select d.*, year(d.det) yr from d join cal c8 on c8.qtr = dateadd(quarter, -8, d.qtr)
      where d.idn < c8.med_idn and month(d.det) <= 5 and year(d.det) in (2019, 2024, 2026)),
g as (select yr, grouping(nat) is_total, iff(grouping(nat)=1, 'ALL', nat) nat, count(*) n,
        count_if(hear >= det) hear_on_after_det, count_if(hear > '2026-05-31') hear_future, count_if(e28d < det) lawyer_before,
        count_if(gap > 3652) in_us_10y, count_if(cust='D') cust_d, count_if(cust='R') cust_r, count_if(ctype='RMV') rmv,
        median(idn) med_idn, min(det) first_det
      from o group by grouping sets ((yr), (yr, nat)))
select * from g qualify is_total = 1 or row_number() over (partition by yr, is_total order by n desc) <= 12
order by yr, is_total desc, n desc;

-- [q10] statement 10
-- EOIR: monthly check of the old-case rise, 2023-01 to 2026-05. Adds the courthouse signature: latest hearing date (field 15) = detention date (field 32).
-- Artifact checks: busiest single day per month, weekend share (a batch data fix would pile on few days)
with p as (
  select try_to_number(split_part(CASE_TYPE, '\t', 1)) idn,
    try_to_date(left(split_part(CASE_TYPE, '\t', 15), 10), 'YYYY-MM-DD') hear,
    split_part(CASE_TYPE, '\t', 17) caltype,
    try_to_date(left(split_part(CASE_TYPE, '\t', 24), 10), 'YYYY-MM-DD') entry,
    try_to_date(left(split_part(CASE_TYPE, '\t', 32), 10), 'YYYY-MM-DD') det
  from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EOIR_CASE_DATA
  where regexp_count(CASE_TYPE, '\t') = 38),
d as (select *, date_trunc(quarter, det)::date qtr, datediff(day, entry, det) gap from p where det >= '2012-01-01' and det < '2026-06-01'),
cal as (select qtr, median(idn) med_idn from d where gap between 0 and 30 group by 1),
m as (select d.*, (d.idn < c8.med_idn) old from d join cal c8 on c8.qtr = dateadd(quarter, -8, d.qtr) where d.det >= '2023-01-01'),
dd as (select det, count(*) n_day, count_if(old) old_day from m group by 1)
select date_trunc(month, m.det)::date mo, count(*) detained, count_if(old) old_case, count_if(hear = det) hear_eq_det,
  count_if(old and hear = det) old_hear_eq_det, count_if(old and hear = det and caltype = 'M') old_eq_master, count_if(old and hear = det and caltype = 'I') old_eq_indiv,
  count_if(dayofweekiso(det) >= 6) weekend, count_if(old and dayofweekiso(det) >= 6) old_weekend,
  (select max(old_day) from dd where date_trunc(month, dd.det) = date_trunc(month, m.det)) max_old_one_day,
  (select count(*) from dd where date_trunc(month, dd.det) = date_trunc(month, m.det) and old_day > 0) days_with_old
from m group by 1 order by 1;

-- [q10b] statement 11
-- (q10 retry; q10 failed to compile) EOIR: monthly check of the old-case rise, 2023-01 to 2026-05. Adds the courthouse signature: latest hearing date (field 15) = detention date (field 32).
-- Artifact checks: busiest single day per month, weekend share (a batch data fix would pile on few days)
with p as (
  select try_to_number(split_part(CASE_TYPE, '\t', 1)) idn,
    try_to_date(left(split_part(CASE_TYPE, '\t', 15), 10), 'YYYY-MM-DD') hear,
    split_part(CASE_TYPE, '\t', 17) caltype,
    try_to_date(left(split_part(CASE_TYPE, '\t', 24), 10), 'YYYY-MM-DD') entry,
    try_to_date(left(split_part(CASE_TYPE, '\t', 32), 10), 'YYYY-MM-DD') det
  from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EOIR_CASE_DATA
  where regexp_count(CASE_TYPE, '\t') = 38),
d as (select *, date_trunc(quarter, det)::date qtr, datediff(day, entry, det) gap from p where det >= '2012-01-01' and det < '2026-06-01'),
cal as (select qtr, median(idn) med_idn from d where gap between 0 and 30 group by 1),
m as (select d.*, (d.idn < c8.med_idn) old from d join cal c8 on c8.qtr = dateadd(quarter, -8, d.qtr) where d.det >= '2023-01-01'),
dd as (select date_trunc(month, det)::date mo, det, count_if(old) old_day from m group by 1, 2),
dm as (select mo, max(old_day) max_old_one_day, count_if(old_day > 0) days_with_old from dd group by 1),
mm as (select date_trunc(month, det)::date mo, count(*) detained, count_if(old) old_case, count_if(hear = det) hear_eq_det,
  count_if(old and hear = det) old_hear_eq_det, count_if(old and hear = det and caltype = 'M') old_eq_master, count_if(old and hear = det and caltype = 'I') old_eq_indiv,
  count_if(dayofweekiso(det) >= 6) weekend, count_if(old and dayofweekiso(det) >= 6) old_weekend
  from m group by 1)
select mm.*, dm.max_old_one_day, dm.days_with_old from mm join dm using (mo) order by mo;

-- [q11] statement 12
-- Cross-check against an independent source: ICE detention stays (FED_ICE_DETENTION_STINTS) by month of stay book-in, 2023-01 to 2026-05.
-- Aggregate only (no row join; the tables share no key). Stays, stays whose entry date is 2+ years before book-in, stays whose current ICE case category is [3] (under adjudication by an immigration judge)
with s as (
  select STAY_ID, try_to_date(left(STAY_BOOK_IN_AT::string, 10), 'YYYY-MM-DD') bin,
    try_to_date(left(ENTRY_DATE::string, 10), 'YYYY-MM-DD') entry, CASE_CATEGORY cc, FINAL_PROGRAM fp
  from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_STINTS)
select date_trunc(month, bin)::date mo, count(distinct STAY_ID) stays,
  count(distinct iff(datediff(day, entry, bin) > 730, STAY_ID, null)) stays_entry_2y,
  count(distinct iff(cc like '[3]%', STAY_ID, null)) stays_cat3_ij,
  count(distinct iff(fp ilike '%border patrol%', STAY_ID, null)) stays_bp,
  (select max(try_to_date(left(STAY_BOOK_IN_AT::string, 10), 'YYYY-MM-DD')) from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_STINTS) max_bin
from s where bin >= '2023-01-01' and bin < '2026-06-01'
group by 1 order by 1;

-- [q12] statement 13
-- EOIR: denominator test by nationality. Band = cases opened 2-4 years before the window, by IDNCASE, using q08 calendar medians:
--   2026 window (Jan-May 2026): IDNCASE in [10,441,284 (Q1 2022), 13,639,610 (Q1 2024))
--   2024 window (Jan-May 2024): IDNCASE in [9,441,378 (Q1 2020), 10,441,284 (Q1 2022))
--   2019 window (Jan-May 2019): IDNCASE in [7,636,140 (Q1 2015), 8,145,229 (Q1 2017))
-- Rate = band cases logged detained in the window per 1,000 band cases. Top 14 nationalities by 2026 detained + ALL.
with p as (
  select try_to_number(split_part(CASE_TYPE, '\t', 1)) idn, split_part(CASE_TYPE, '\t', 7) nat,
    try_to_date(left(split_part(CASE_TYPE, '\t', 11), 10), 'YYYY-MM-DD') e28d,
    try_to_date(left(split_part(CASE_TYPE, '\t', 32), 10), 'YYYY-MM-DD') det
  from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EOIR_CASE_DATA
  where regexp_count(CASE_TYPE, '\t') = 38),
b as (select *, case when idn >= 10441284 and idn < 13639610 then 2026 when idn >= 9441378 and idn < 10441284 then 2024
                     when idn >= 7636140 and idn < 8145229 then 2019 end w from p),
g as (select iff(grouping(nat)=1, 'ALL', nat) nat,
  count_if(w=2019) band19, count_if(w=2019 and det between '2019-01-01' and '2019-05-31') det19,
  count_if(w=2024) band24, count_if(w=2024 and det between '2024-01-01' and '2024-05-31') det24,
  count_if(w=2026) band26, count_if(w=2026 and det between '2026-01-01' and '2026-05-31') det26,
  count_if(w=2026 and det between '2026-01-01' and '2026-05-31' and e28d < det) det26_lawyer_before
  from b where w is not null group by grouping sets ((), (nat)))
select nat, band19, det19, round(1000*det19/nullif(band19,0),2) r19, band24, det24, round(1000*det24/nullif(band24,0),2) r24,
  band26, det26, round(1000*det26/nullif(band26,0),2) r26, det26_lawyer_before
from g qualify nat = 'ALL' or row_number() over (order by det26 desc) <= 16
order by det26 desc;

-- [q13] statement 14
-- EOIR eyeball: 6 random old-band cases (IDNCASE 10,441,284-13,639,609, opened ~2022-2024) logged detained Jan-May 2026 with a lawyer notice dated before detention. Parsed fields side by side.
with p as (
  select try_to_number(split_part(CASE_TYPE, '\t', 1)) idn, split_part(CASE_TYPE, '\t', 2) city, split_part(CASE_TYPE, '\t', 3) st, split_part(CASE_TYPE, '\t', 4) zip,
    split_part(CASE_TYPE, '\t', 7) nat, split_part(CASE_TYPE, '\t', 8) lang, split_part(CASE_TYPE, '\t', 9) cust,
    left(split_part(CASE_TYPE, '\t', 11), 10) e28, split_part(CASE_TYPE, '\t', 13) ctype, split_part(CASE_TYPE, '\t', 14) site,
    left(split_part(CASE_TYPE, '\t', 15), 10) hear, split_part(CASE_TYPE, '\t', 17) cal, left(split_part(CASE_TYPE, '\t', 24), 10) entry,
    split_part(CASE_TYPE, '\t', 26) birth, left(split_part(CASE_TYPE, '\t', 29), 10) addr_changed, split_part(CASE_TYPE, '\t', 31) sex,
    left(split_part(CASE_TYPE, '\t', 32), 10) det, left(split_part(CASE_TYPE, '\t', 33), 10) rel, split_part(CASE_TYPE, '\t', 39) prio
  from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EOIR_CASE_DATA
  where regexp_count(CASE_TYPE, '\t') = 38 and CASE_TYPE like '%\t2026-0%')
select * from p where idn >= 10441284 and idn < 13639610 and det between '2026-01-01' and '2026-05-31' and e28 < det
order by hash(idn) limit 6;

-- [q14] statement 15
-- OWID refugees: whole table (7,442 rows x 5 columns), analyzed locally in owid.py
select ENTITY, CODE, YEAR, REFUGEES_BY_COUNTRY_OF_ORIGIN, WORLD_REGION_ACCORDING_TO_OWID from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__XC_OWID_REFUGEES;

-- [q15] statement 16
-- EOIR: where are the Jan-May 2026 old-band detainees (IDNCASE 10,441,284-13,639,609, cases opened ~Q1 2022-Q1 2024)?
-- Top address places (city/state/ZIP on file, usually the jail for custody D) and top courts (UPDATE_SITE, field 14)
with p as (
  select try_to_number(split_part(CASE_TYPE, '\t', 1)) idn, upper(trim(split_part(CASE_TYPE, '\t', 2))) city, split_part(CASE_TYPE, '\t', 3) st,
    left(split_part(CASE_TYPE, '\t', 4), 5) zip, split_part(CASE_TYPE, '\t', 9) cust, split_part(CASE_TYPE, '\t', 14) site,
    try_to_date(left(split_part(CASE_TYPE, '\t', 32), 10), 'YYYY-MM-DD') det
  from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EOIR_CASE_DATA
  where regexp_count(CASE_TYPE, '\t') = 38),
o as (select * from p where idn >= 10441284 and idn < 13639610 and det between '2026-01-01' and '2026-05-31'),
a as (select 'place' k, city || ', ' || st || ' ' || zip v, count(*) n, count_if(cust='D') d from o group by 2),
b as (select 'court' k, site v, count(*) n, count_if(cust='D') d from o group by 2),
t as (select 'total' k, 'all' v, count(*) n, count_if(cust='D') d from o)
select * from t
union all select * from (select * from a order by n desc limit 15)
union all select * from (select * from b order by n desc limit 12);

-- [q16] statement 17
-- Join: EOIR address ZIP (field 4) of Jan-May 2026 old-band detainees (custody D) -> ICE detention facility code list by 5-digit ZIP.
-- Aggregate EOIR to ZIP first. Land rate, then top 15 ZIPs with facility name(s) and type.
with p as (
  select try_to_number(split_part(CASE_TYPE, '\t', 1)) idn, left(split_part(CASE_TYPE, '\t', 4), 5) zip, split_part(CASE_TYPE, '\t', 9) cust,
    try_to_date(left(split_part(CASE_TYPE, '\t', 11), 10), 'YYYY-MM-DD') e28d,
    try_to_date(left(split_part(CASE_TYPE, '\t', 32), 10), 'YYYY-MM-DD') det
  from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EOIR_CASE_DATA
  where regexp_count(CASE_TYPE, '\t') = 38),
z as (select zip, count(*) n, count_if(e28d < det) lawyer_before from p
      where idn >= 10441284 and idn < 13639610 and det between '2026-01-01' and '2026-05-31' and cust = 'D' group by 1),
f as (select left(trim(ZIP::string), 5) zip, count(*) nfac, listagg(distinct DETENTION_FACILITY_NAME, ' | ') names, listagg(distinct TYPE_GROUPED, '|') types
      from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_FACILITY_CODES group by 1),
j as (select z.*, f.nfac, f.names, f.types from z left join f on f.zip = z.zip)
select 'land' k, null zip, sum(n) n, sum(iff(nfac is not null, n, 0)) landed, count(*) zips, count_if(nfac is not null) zips_landed, null names, null types, sum(lawyer_before) lawyer_before from j
union all
select * from (select 'top', zip, n, lawyer_before, null, nfac, left(names, 150), types, null from j order by n desc limit 15);

-- Notes
-- q10 (statement 10) failed to compile (correlated subquery on a non-grouped column) and returned nothing; q10b is the retry. Both count against the budget.
-- q13 compares E28 as text in its final filter; one of its six sample rows has a blank E28 that slipped through. The counts in q08/q09/q12/q16 use try_to_date, so blanks are NULL there.
-- q16 "top" rows: the LANDED column holds lawyer_before and ZIPS_LANDED holds the number of ICE facility codes at that ZIP (column reuse in the UNION).
-- OWID refugees (q14) was pulled whole and analyzed locally in g69/owid.py; no extra statements.
-- Total: 17 SELECT/WITH statements of 35.
