-- Plant: shape, filler locations, and every combination of the ash-pond fields, regulatory status, sector, FERC flags, storage flags
with t as (select * from LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_2_PLANT)
select 'ash' k, ASH_IMPOUNDMENT a, ASH_IMPOUNDMENT_LINED b, ASH_IMPOUNDMENT_STATUS c, count(*)::text n, count(distinct STATE)::text x from t group by 1,2,3,4
union all select 'profile', count(*)::text, count(distinct PLANT_CODE)::text, count_if(LATITUDE is null or LATITUDE=0)::text, count_if(ZIP is null or ZIP in ('00000','UNKNO','-'))::text, listagg(distinct _SRC_FILE,'|') from t
union all select 'reg', REGULATORY_STATUS, SECTOR, SECTOR_NAME, count(*)::text, null from t group by 2,3,4
union all select 'ferc', FERC_COGENERATION_STATUS, FERC_SMALL_POWER_PRODUCER_STATUS, FERC_EXEMPT_WHOLESALE_GENERATOR_STATUS, count(*)::text, null from t group by 2,3,4
union all select 'storage', ENERGY_STORAGE, NATURAL_GAS_STORAGE, LIQUEFIED_NATURAL_GAS_STORAGE, count(*)::text, null from t group by 2,3,4
