-- s05: the natural cut. Operating facilities with an HPV begun before 2024-07-01 and unresolved: how many have NO formal action ON OR AFTER day zero
-- (vs the builder's "no formal action at any date"), and did the facility later pass a stack test or get a full compliance evaluation (fixed but never closed?).
with v as (select PGM_SYS_ID, min(HPV_DAYZERO_DATE) dz from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY
           where ENF_RESPONSE_POLICY_CODE = 'HPV' and HPV_RESOLVED_DATE is null and HPV_DAYZERO_DATE < '2024-07-01' group by 1),
p as (select PGM_SYS_ID, max(iff(PROGRAM_CODE = 'CAATVP' and AIR_OPERATING_STATUS_CODE = 'OPR', 1, 0)) tv_opr, max(iff(AIR_OPERATING_STATUS_CODE = 'OPR', 1, 0)) any_opr
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAMS group by 1),
f as (select PGM_SYS_ID, any_value(STATE) st, any_value(FACILITY_NAME) nm from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES group by 1),
b as (select v.PGM_SYS_ID, v.dz, coalesce(f.st, '??') st, f.nm, p.tv_opr from v join p on v.PGM_SYS_ID = p.PGM_SYS_ID left join f on v.PGM_SYS_ID = f.PGM_SYS_ID where p.any_opr = 1),
fa as (select b.PGM_SYS_ID, count(a.ACTIVITY_ID) n_all, count_if(a.SETTLEMENT_ENTERED_DATE >= b.dz) n_since
       from b left join LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS a on a.PGM_SYS_ID = b.PGM_SYS_ID group by 1),
stk as (select b.PGM_SYS_ID, count_if(s.AIR_STACK_TEST_STATUS_DESC ilike '%pass%') pass_after, count_if(s.AIR_STACK_TEST_STATUS_DESC ilike '%fail%') fail_after,
          max(s.ACTUAL_END_DATE) last_test, count(s.POLLUTANT_DESCS) pdesc_filled, count(s.POLLUTANT_CODES) pcode_filled
        from b left join LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_STACK_TESTS s on s.PGM_SYS_ID = b.PGM_SYS_ID and s.ACTUAL_END_DATE > b.dz group by 1),
fce as (select b.PGM_SYS_ID, count(c.ACTIVITY_ID) fce_after, max(c.ACTUAL_END_DATE) last_fce
        from b left join LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FCES_PCES c on c.PGM_SYS_ID = b.PGM_SYS_ID and c.ACTUAL_END_DATE > b.dz group by 1),
j as (select b.*, fa.n_all, fa.n_since, stk.pass_after, stk.fail_after, stk.last_test, stk.pdesc_filled, stk.pcode_filled, fce.fce_after, fce.last_fce
      from b join fa on b.PGM_SYS_ID = fa.PGM_SYS_ID join stk on b.PGM_SYS_ID = stk.PGM_SYS_ID join fce on b.PGM_SYS_ID = fce.PGM_SYS_ID)
select 'state' k, coalesce(st, 'ALL') a, count(*)::text open_old_opr, count_if(n_all = 0)::text no_fa_ever, count_if(n_since = 0)::text no_fa_since_dz,
  count_if(n_since = 0 and tv_opr = 1)::text no_fa_since_tv, count_if(n_since = 0 and pass_after > 0)::text nofa_passed_test_after, count_if(n_since = 0 and fce_after > 0)::text nofa_fce_after,
  median(iff(n_since = 0, datediff('day', dz, '2026-09-24'::date), null))::text med_days_open, sum(pdesc_filled)::text || '/' || sum(pcode_filled)::text stk_pdesc_pcode
from j group by rollup(st) having count_if(n_since = 0) >= 2 or st is null
union all
select * from (select 'ne', PGM_SYS_ID, nm, dz::text, n_all::text || '/' || n_since::text, tv_opr::text, pass_after::text || 'p/' || fail_after::text || 'f last ' || coalesce(last_test::text, '-'),
  fce_after::text || ' last ' || coalesce(last_fce::text, '-'), null, null from j where st = 'NE' order by dz)
order by 1 desc, 5 desc;
