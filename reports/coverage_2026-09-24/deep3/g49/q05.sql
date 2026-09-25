-- Warehouse: every CourtListener table and its row count. Is there an OPINIONS table to name a parenthetical's opinion?
select table_schema, table_name, row_count, last_altered
from LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES
where table_name ilike '%COURTLISTENER%' order by 2
