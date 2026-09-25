-- France: ARCHIVED raw values (top 15) to learn the format before parsing
select ARCHIVED, count(*) n from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_FR_DATA_GOUV group by 1 order by 2 desc limit 15
