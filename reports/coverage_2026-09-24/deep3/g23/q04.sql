-- Pull the whole raw medians table (text), with circuit medians
select t.*, count(*) over () n_rows from LIBRARY_MARTS.POLITICS.POLITICS__XC_JCS_MEDIANS t
