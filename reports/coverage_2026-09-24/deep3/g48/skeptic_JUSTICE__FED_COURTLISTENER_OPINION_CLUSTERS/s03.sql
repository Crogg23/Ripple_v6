-- CourtListener re-derivation: 13 circuits x 2018-2025, published rows/dockets/docket numbers/name+date (builder method and blank-safe), blank names, unpublished, other
with c as (select ID, DOCKET_ID, year(DATE_FILED) yr, DATE_FILED, CASE_NAME, PRECEDENTIAL_STATUS st, SOURCE, JUDGES
           from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_OPINION_CLUSTERS
           where DATE_FILED >= '2018-01-01' and DATE_FILED < '2026-01-01'),
d as (select ID, COURT_ID, DOCKET_NUMBER from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS
      where COURT_ID in ('ca1','ca2','ca3','ca4','ca5','ca6','ca7','ca8','ca9','ca10','ca11','cadc','cafc'))
select d.COURT_ID, c.yr, count(*) n_all,
  sum(iff(c.st='Published',1,0)) pub_rows,
  sum(iff(c.st='Unpublished',1,0)) unpub_rows,
  sum(iff(c.st is null or c.st not in ('Published','Unpublished'),1,0)) other_rows,
  count(distinct iff(c.st='Published', c.DOCKET_ID, null)) pub_dockets,
  count(distinct iff(c.st='Published', d.DOCKET_NUMBER, null)) pub_docketnum,
  count(distinct iff(c.st='Published', c.CASE_NAME||'|'||to_char(c.DATE_FILED), null)) pub_name_date_builder,
  count(distinct iff(c.st='Published' and nullif(trim(c.CASE_NAME),'') is not null and c.CASE_NAME <> 'None', c.CASE_NAME||'|'||to_char(c.DATE_FILED), null)) pub_name_date_real,
  sum(iff(c.st='Published' and (nullif(trim(c.CASE_NAME),'') is null or c.CASE_NAME='None'),1,0)) pub_blank_name,
  count(distinct iff(c.st='Published', upper(c.CASE_NAME), null)) pub_distinct_name,
  count(distinct iff(c.st='Unpublished', c.DOCKET_ID, null)) unpub_dockets,
  count(distinct iff(c.st='Unpublished', c.CASE_NAME||'|'||to_char(c.DATE_FILED), null)) unpub_name_date,
  sum(iff(c.st='Published' and c.SOURCE='C',1,0)) pub_src_c,
  sum(iff(c.st='Published' and nullif(trim(c.JUDGES),'') is not null,1,0)) pub_judges_filled,
  min(d.DOCKET_NUMBER) ex_dn_min, max(d.DOCKET_NUMBER) ex_dn_max
from c join d on d.ID = c.DOCKET_ID
group by 1,2 order by 1,2;
