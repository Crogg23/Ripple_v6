-- Federal Register trap check: the comment-window median is exactly 45 every year. Is COMMENT_WINDOW_DAYS real? Top values, and a recompute from the two date columns
select 'top' k, COMMENT_WINDOW_DAYS::text v, count(*) n,
  count_if(datediff(day, PUBLICATION_DATE, COMMENTS_CLOSE_ON) = COMMENT_WINDOW_DAYS) agrees, null x
from LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS
where TYPE = 'Proposed Rule' and COMMENT_WINDOW_DAYS is not null
group by 2 qualify row_number() over (order by count(*) desc) <= 12
union all
select 'recompute', PUBLICATION_YEAR::text, count(*), median(datediff(day, PUBLICATION_DATE, COMMENTS_CLOSE_ON)),
  count_if(datediff(day, PUBLICATION_DATE, COMMENTS_CLOSE_ON) < 30)
from LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS
where TYPE = 'Proposed Rule' and COMMENTS_CLOSE_ON is not null and PUBLICATION_YEAR >= 2022
group by 2
