-- payee_shorter_* is a subset of matched_*, never more.
select chain_id
from {{ ref('health__nursing_home_relief_by_chain') }}
where payee_shorter_homes > matched_homes
   or payee_shorter_dollars > matched_relief_dollars
