-- Supreme Court cases decided per term (SCDB, typed curated mart).
select
    term,
    chief_justice,
    count(distinct case_id) as cases
from THE_LIBRARY.JUSTICE.SCOTUS_CASES_AND_VOTES
where term is not null
group by 1, 2
order by 1
