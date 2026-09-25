-- Federal Register: profile. Uniqueness, type mix, fill rates of the flag and date columns, per-year counts
select 'profile' k, count(*)::text a, count(distinct DOCUMENT_NUMBER)::text b, count(distinct CITATION)::text c,
  count_if(IS_SIGNIFICANT is not null)::text d, count_if(IS_SIGNIFICANT)::text e, count_if(EFFECTIVE_ON is not null)::text f,
  count_if(COMMENTS_CLOSE_ON is not null)::text g, count_if(COMMENT_WINDOW_DAYS is not null)::text h,
  count(distinct PRESIDENT)::text i, count_if(PAGE_LENGTH<>DERIVED_PAGE_COUNT)::text j
from LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS
union all
select 'year', PUBLICATION_YEAR::text, count(*)::text, count_if(TYPE='Rule')::text, count_if(TYPE='Proposed Rule')::text,
  count_if(TYPE='Notice')::text, count_if(TYPE='Presidential Document')::text, count_if(IS_SIGNIFICANT)::text,
  count_if(IS_SIGNIFICANT is not null)::text, count_if(COMMENT_WINDOW_DAYS is not null)::text, max(PUBLICATION_DATE)::text
from LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS group by 2
union all
select 'type', TYPE, count(*)::text, null,null,null,null,null,null,null,null
from LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS group by 2
union all
select 'president', PRESIDENT, count(*)::text, min(PUBLICATION_DATE)::text, max(PUBLICATION_DATE)::text,null,null,null,null,null,null
from LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS group by 2
