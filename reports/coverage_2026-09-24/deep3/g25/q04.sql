-- ISO MIC registry: confirm it's a lookup: status x category, expiry years, comments words
select 'status' k, STATUS a, OPRT_SGMT b, count(*) n, count(distinct ISO_COUNTRY_CODE_ISO_3166) c from LIBRARY_MARTS.FINANCE.FINANCE__INTL_ISO_MIC_REGISTRY group by 2,3
union all select 'cat', MARKET_CATEGORY_CODE, null, count(*), count_if(STATUS='EXPIRED') from LIBRARY_MARTS.FINANCE.FINANCE__INTL_ISO_MIC_REGISTRY group by 2
union all select 'expyr', year(EXPIRY_DATE)::text, null, count(*), count(distinct ISO_COUNTRY_CODE_ISO_3166) from LIBRARY_MARTS.FINANCE.FINANCE__INTL_ISO_MIC_REGISTRY where EXPIRY_DATE is not null group by 2
union all select 'crtyr', year(CREATION_DATE)::text, null, count(*), count_if(STATUS='EXPIRED') from LIBRARY_MARTS.FINANCE.FINANCE__INTL_ISO_MIC_REGISTRY group by 2
union all select 'rows', count(*)::text, count(distinct MIC)::text, count(distinct LEI), count(distinct _SOURCE_RUN_ID) from LIBRARY_MARTS.FINANCE.FINANCE__INTL_ISO_MIC_REGISTRY
order by 1, 4 desc
