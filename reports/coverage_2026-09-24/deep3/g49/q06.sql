-- Parentheticals: the 20 most-described opinion IDs, tried against OPINION_CLUSTERS.ID. Do the names make sense?
with p as (select DESCRIBED_OPINION_ID::string id, count(*) n, count(distinct DESCRIBING_OPINION_ID) n_citing,
             any_value(left(TEXT,160)) sample
           from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_PARENTHETICALS group by 1 order by n desc limit 20)
select p.*, c.CASE_NAME, c.DATE_FILED, c.CITATION_COUNT
from p left join LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_OPINION_CLUSTERS c on c.ID::string = p.id
order by p.n desc
