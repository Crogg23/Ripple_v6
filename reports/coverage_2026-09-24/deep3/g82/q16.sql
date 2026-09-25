-- Federal Register: which issuing offices went quiet. Documents Feb-Aug by year 2021-2026, most specific agency (last name in the list)
with d as (select PUBLICATION_DATE dt, TYPE,
             coalesce(try_parse_json(AGENCY_NAMES)[array_size(try_parse_json(AGENCY_NAMES))-1]::string, AGENCY) ag
           from LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS
           where month(PUBLICATION_DATE) between 2 and 8 and year(PUBLICATION_DATE) >= 2021),
g as (select ag, count_if(year(dt)=2021) y21, count_if(year(dt)=2022) y22, count_if(year(dt)=2023) y23, count_if(year(dt)=2024) y24,
        count_if(year(dt)=2025) y25, count_if(year(dt)=2026) y26, count_if(year(dt)=2024 and TYPE='Rule') r24, count_if(year(dt)=2025 and TYPE='Rule') r25,
        count_if(year(dt)=2026 and TYPE='Rule') r26
      from d group by 1)
select 'total' k, null ag, sum(y21) y21, sum(y22) y22, sum(y23) y23, sum(y24) y24, sum(y25) y25, sum(y26) y26, sum(r24) r24, sum(r25) r25, sum(r26) r26, null pct from g
union all
(select 'drop', ag, y21, y22, y23, y24, y25, y26, r24, r25, r26, round(100*(y25+y26)/(2.0*((y21+y22+y23+y24)/4.0))) from g
 where (y21+y22+y23+y24)/4.0 >= 100 order by (y25+y26)/((y21+y22+y23+y24)/4.0) asc limit 30)
union all
(select 'rise', ag, y21, y22, y23, y24, y25, y26, r24, r25, r26, round(100*(y25+y26)/(2.0*((y21+y22+y23+y24)/4.0))) from g
 where (y21+y22+y23+y24)/4.0 >= 100 order by (y25+y26)/((y21+y22+y23+y24)/4.0) desc limit 10)
