-- The card catalog: one row per dataset in the reading room (~232 rows).
select
    shelf,
    dataset,
    what_it_is,
    row_count,
    status,
    source_id,
    last_updated
from THE_LIBRARY.PUBLIC.START_HERE
order by shelf, dataset
