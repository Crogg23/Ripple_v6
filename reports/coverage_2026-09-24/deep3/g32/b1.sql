-- @cols
select table_schema, table_name, row_count, (select listagg(column_name, ',') within group (order by ordinal_position) from LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS c where c.table_schema = t.table_schema and c.table_name = t.table_name) cols
from LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES t
where table_name like 'FINANCE__FED_SEC_DERA_SUB_%' or table_name like '%CFTC_COT%' or table_name = 'FINANCE__FED_FINRA_MPID_LIST' or table_name like 'FINANCE__FED_SEC_INSIDER%' or table_name = 'FINANCE__FED_SEC_EDGAR_FINANCIALS'
order by 2
-- @sub_2025q3_all
select * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2025Q3
-- @sub_2025q4_all
select * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2025Q4
-- @sub_2026q1_all
select * from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2026Q1
-- @cot_fin_hist_all
select * from LIBRARY_MARTS.FINANCE.FINANCE__FED_CFTC_COT_FINANCIAL_HIST
-- @finra_mpid_all
select * from LIBRARY_MARTS.FINANCE.FINANCE__FED_FINRA_MPID_LIST
