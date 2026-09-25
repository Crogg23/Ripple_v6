-- Column names and types for my 5 tables plus the join partners (Google advertiser stats, FEC committee dim, FEC PAC summary)
select table_schema, table_name, count(*) ncols,
  listagg(column_name || ':' || left(data_type,4), ', ') within group (order by ordinal_position) cols
from LIBRARY_MARTS.information_schema.columns
where table_name in ('EDUCATION__FED_FRB_H15_SELECTED_RATES','EDUCATION__FED_GOOGLE_POLADS_CREATIVE_ID_MAPPING',
 'EDUCATION__FED_ED_NCES_CIP_CODES','EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_WEEKLY_SPEND','EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_STATS',
 'FINANCE__FED_FEC_COMMITTEES_DIM','POLITICS__FED_FEC_PAC_SUMMARY','EDUCATION__FED_GOOGLE_POLADS_CREATIVE_STATS')
 or (table_name = 'EDUCATION__FED_CFTC_COT_FUTURES' and (column_name like '\_%' or column_name like 'CONC%' or column_name like 'TRADERS_TOTAL%' or column_name like 'OPEN_INT%' or column_name like 'CFTC%' or column_name like 'AS_OF%' or column_name like 'MARKET%'))
group by 1,2 order by 1,2
