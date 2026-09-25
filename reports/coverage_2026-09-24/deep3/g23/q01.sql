-- Pull the whole appeals-judge score table, plus a row count and distinct row-number count
select t.*, count(*) over () n_rows, count(distinct UNNAMED_0) over () n_rownum
from LIBRARY_MARTS.POLITICS.POLITICS__XC_JCS_COA t
