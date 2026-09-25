-- Pull the whole Supreme Court justice-by-term score table
select t.*, count(*) over () n_rows, count(distinct UNNAMED_0) over () n_rownum
from LIBRARY_MARTS.POLITICS.POLITICS__XC_JCS_SCOTUS t
