-- EOIR: shape of the one loaded column. Rows grouped by number of tab separators; distinct rows, distinct first field, lengths, two samples
select regexp_count(CASE_TYPE, '\t') tabs, count(*) n, count(distinct CASE_TYPE) distinct_rows,
  count(distinct split_part(CASE_TYPE, '\t', 1)) distinct_f1,
  min(length(CASE_TYPE)) minlen, max(length(CASE_TYPE)) maxlen, avg(length(CASE_TYPE))::int avglen,
  count_if(CASE_TYPE like '%' || char(0) || '%') has_nul,
  min(CASE_TYPE) samp_min, max(CASE_TYPE) samp_max
from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EOIR_CASE_DATA
group by 1 order by 2 desc
