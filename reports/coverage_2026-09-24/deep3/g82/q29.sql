-- Federal Register midnight rules by agency: final rules in the Nov 8 - Jan 19 window of the three handover years vs the same agency average over 11 ordinary windows
with d as (select PUBLICATION_DATE dt, IS_SIGNIFICANT sig,
             coalesce(try_parse_json(AGENCY_NAMES)[array_size(try_parse_json(AGENCY_NAMES))-1]::string, AGENCY) ag
           from LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS where TYPE = 'Rule'),
w as (select *, case when dt >= date_from_parts(year(dt),11,8) then year(dt) when dt <= date_from_parts(year(dt),1,19) then year(dt)-1 end wy from d),
g as (select ag, count_if(wy=2016) r16, count_if(wy=2020) r20, count_if(wy=2024) r24,
        count_if(wy=2016 and sig) s16, count_if(wy=2020 and sig) s20, count_if(wy=2024 and sig) s24,
        count_if(wy in (2010,2011,2013,2014,2015,2017,2018,2019,2021,2022,2023)) / 11.0 r_base,
        count_if(wy in (2010,2011,2013,2014,2015,2017,2018,2019,2021,2022,2023) and sig) / 11.0 s_base
      from w where wy is not null group by 1)
(select 'sig24' k, ag, r16, r20, r24, round(r_base,1) r_base, s16, s20, s24, round(s_base,1) s_base from g order by s24 - s_base desc limit 12)
union all
(select 'sig16', ag, r16, r20, r24, round(r_base,1), s16, s20, s24, round(s_base,1) from g order by s16 - s_base desc limit 8)
union all
(select 'sig20', ag, r16, r20, r24, round(r_base,1), s16, s20, s24, round(s_base,1) from g order by s20 - s_base desc limit 8)
