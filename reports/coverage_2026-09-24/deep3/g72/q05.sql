-- Georgia (1 row) and Ghana (10 rows): print every row whole
select 'GE' k, to_json(object_construct_keep_null(*))::text row_json from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_GE_DATAGOV
union all
select 'GH', to_json(object_construct_keep_null(*))::text from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_GH_DATAGOVGH;
