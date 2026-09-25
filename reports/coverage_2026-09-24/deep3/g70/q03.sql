-- ICE facility codes: confirm lookup; land rate of detention-stint codes; stints by facility type
with s as (select DETENTION_FACILITY_CODE code, count(*) n, min(BOOK_IN_AT) mn, max(BOOK_IN_AT) mx from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_STINTS group by 1),
f as (select * from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_FACILITY_CODES)
select 'profile' k, count(*)::text a, count(distinct DETENTION_FACILITY_CODE)::text b, count(distinct TYPE_GROUPED)::text c, count(distinct TYPE_DETAILED)::text d from f
union all select 'land', count(*)::text, count_if(f.DETENTION_FACILITY_CODE is not null)::text, sum(n)::text, sum(iff(f.DETENTION_FACILITY_CODE is not null, n, 0))::text from s left join f on f.DETENTION_FACILITY_CODE = s.code
union all select 'type', f.TYPE_GROUPED||' / '||coalesce(f.TYPE_DETAILED, '(null)'), count(distinct f.DETENTION_FACILITY_CODE)::text, count(distinct s.code)::text, coalesce(sum(s.n), 0)::text from f left join s on s.code = f.DETENTION_FACILITY_CODE group by 2
union all select 'stint_range', min(mn)::text, max(mx)::text, null, null from s
union all select * from (select 'unmatched_top', s.code, s.n::text, null, null from s left join f on f.DETENTION_FACILITY_CODE = s.code where f.DETENTION_FACILITY_CODE is null order by s.n desc limit 10)
