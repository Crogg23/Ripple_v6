-- Spain: re-parse the Spanish text dates properly (year is the 4 digits after the month abbreviation), issued and modified
with t as (select regexp_substr(ISSUED, '[0-9]{1,2} [a-z]{3} ([0-9]{4})', 1, 1, 'e', 1) iy,
                  regexp_substr(MODIFIED, '[0-9]{1,2} [a-z]{3} ([0-9]{4})', 1, 1, 'e', 1) my, SECTOR, PUBLISHER
           from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_ES_DATOSGOB)
select 'issued' k, coalesce(iy,'unparsed') yr, count(*) n from t group by 2
union all select 'modified', coalesce(my,'unparsed'), count(*) from t group by 2
order by 1,2;
