-- Every dataset in the warehouse, counted by month.
-- Reads the pre-built shared timeline (1.16M rows), not the 720M underlying rows,
-- so this is one small scan no matter how big the sources are.
--
-- ripple_grain matters: a year-only source lands entirely on 1 January.
-- ripple_clock matters: 'happened' and 'reported' answer different questions.
select
    ripple_source,
    ripple_clock,
    ripple_grain,
    date_trunc('month', ripple_day)::date as month,
    sum(n_rows)                            as n_rows
from LIBRARY_MARTS.TIMELINE.TIMELINE__WAREHOUSE
group by 1, 2, 3, 4
