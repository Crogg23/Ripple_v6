-- payee_shorter_than_home must fire on at least one row (a constant-false flag
-- passes accepted_values, traps 2026-09-07), and must agree with the method:
-- shorter payee <=> home_starts_with_prf. Any row where the two disagree fails.
select ccn, match_method, payee_shorter_than_home
from {{ ref('int_nursing_home_prf_match') }}
where payee_shorter_than_home <> (match_method = 'home_starts_with_prf')
union all
select null, 'no_flagged_rows', null
from (select count_if(payee_shorter_than_home) as n from {{ ref('int_nursing_home_prf_match') }})
where n = 0
