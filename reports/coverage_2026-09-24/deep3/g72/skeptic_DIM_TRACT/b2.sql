-- @@ s8_lahaina_code_vintage
select coalesce(nullif(trim(f.CENSUS_YEAR),''),'blank') cy, year(f.DECLARATION_DATE) dy, f.DISASTER_NUMBER dn, left(f.CENSUS_GEOID,11) tr,
  count(*) n, max(iff(d.TRACT_GEOID is not null,1,0)) in_dim, mode(f.DAMAGED_CITY) city
from LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS f
left join LIBRARY_MARTS.CORE.DIM_TRACT d on d.TRACT_GEOID = left(f.CENSUS_GEOID,11)
where left(f.CENSUS_GEOID,8) = '15009031'
group by 1,2,3,4 order by 2,3,1,4;
