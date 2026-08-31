-- One row per dataset on the shared timeline: how much, how long, how precise.
select
    ripple_source,
    ripple_clock,
    ripple_grain,
    min(ripple_day)                                  as first_day,
    max(ripple_day)                                  as last_day,
    datediff('year', min(ripple_day), max(ripple_day)) as years,
    count(*)                                         as n_days,
    sum(n_rows)                                      as n_rows
from LIBRARY_MARTS.TIMELINE.TIMELINE__WAREHOUSE
group by 1, 2, 3
