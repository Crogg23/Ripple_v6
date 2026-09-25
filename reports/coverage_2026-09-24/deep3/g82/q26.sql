-- Federal Register: meeting notices government-wide, Feb-Aug by year 2017-2026, and the offices with the biggest drop (advisory committees, study sections)
with d as (select PUBLICATION_YEAR y, coalesce(try_parse_json(AGENCY_NAMES)[array_size(try_parse_json(AGENCY_NAMES))-1]::string, AGENCY) ag
           from LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS
           where TYPE = 'Notice' and TITLE ilike '%meeting%' and PUBLICATION_MONTH between 2 and 8 and PUBLICATION_YEAR >= 2017)
select 'all' k, null ag, count_if(y=2017) y17, count_if(y=2018) y18, count_if(y=2019) y19, count_if(y=2020) y20, count_if(y=2021) y21, count_if(y=2022) y22,
  count_if(y=2023) y23, count_if(y=2024) y24, count_if(y=2025) y25, count_if(y=2026) y26 from d
union all
(select 'ag', ag, count_if(y=2017), count_if(y=2018), count_if(y=2019), count_if(y=2020), count_if(y=2021), count_if(y=2022),
   count_if(y=2023), count_if(y=2024), count_if(y=2025), count_if(y=2026)
 from d group by ag having count_if(y between 2021 and 2024) >= 80
 order by (count_if(y=2025) + count_if(y=2026)) / (count_if(y between 2021 and 2024)/2.0) asc limit 25)
