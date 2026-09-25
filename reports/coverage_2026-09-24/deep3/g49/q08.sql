-- Judge party ties: where the party label comes from (SOURCE a/o/b) by party; dates filled
select SOURCE, POLITICAL_PARTY, count(*) n, count(distinct PERSON_ID) people,
  count(DATE_START) has_start, count(DATE_END) has_end, min(DATE_CREATED) first_created, max(DATE_CREATED) last_created
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_JUDGE_POLITICAL_AFFILIATIONS
group by 1,2 order by n desc
