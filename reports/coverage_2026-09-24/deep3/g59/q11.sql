-- GLEIF follow-up: snapshot date; are the 11 still-ISSUED foreign subsidiaries listed anywhere themselves (OFAC by name, any OpenSanctions list by LEI);
-- peer base rate: foreign subsidiaries of Russian parents, SDN parent vs not, share still ISSUED
with g as (select LEI, ENTITY_LEGALNAME nm, ENTITY_LEGALADDRESS_COUNTRY ctry, REGISTRATION_REGISTRATIONSTATUS rst, REGISTRATION_LASTUPDATEDATE lupd
           from LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_GLEIF),
sdn as (select distinct f.value::string lei
        from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS_DEFAULT,
             lateral flatten(input => regexp_substr_all(IDENTIFIERS::text, '[A-Z0-9]{18}[0-9]{2}')) f
        where DATASETS::text ilike '%US OFAC Specially Designated Nationals (SDN) List%'),
kids11 as (select column1 lei from values ('5299007PQV6X4DPL9Y20'),('K80PJMCDA9MAE5C8IO91'),('213800FXBZXOXNXKWP95'),('391200PKEUF3Y2NUMW25'),
   ('72450024EGZK2K8NAG02'),('724500LG1GUKJ5TOIW61'),('724500UTYUSS56QEBB66'),('724500IVNQ6LF8OFIO42'),('7872006AZAFVTVIQ3G32'),
   ('254900YJTZ2JT3ZSZS32'),('253400QD4JHES5PGDR15')),
r as (select distinct RELATIONSHIP_STARTNODE_NODEID child, RELATIONSHIP_ENDNODE_NODEID parent
      from LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_GLEIF_RELATIONSHIPS
      where RELATIONSHIP_RELATIONSHIPTYPE in ('IS_ULTIMATELY_CONSOLIDATED_BY','IS_DIRECTLY_CONSOLIDATED_BY')),
ru as (select r.child, max(iff(s.lei is not null, 1, 0)) sdn_parent, any_value(c.rst) crst
       from r join g p on p.LEI = r.parent and p.ctry = 'RU'
              join g c on c.LEI = r.child and c.ctry not in ('RU','BY')
              left join sdn s on s.lei = r.parent
       group by 1)
select 'snapshot' k, max(lupd)::text a, count_if(rst='ISSUED')::text b, count(*)::text c, null d from g
union all
select 'ofac_name', SDN_NAME, PROGRAM, left(REMARKS, 200), null from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_OFAC_SDN
where SDN_NAME ilike any ('%LITASCO%', '%LUKOIL%', '%ROSNEFT DEUTSCHLAND%', '%PETROTEL%', '%SISTEMA ASIA%', '%DEGA RETAIL%', '%LUKOIL INTERNATIONAL%')
union all
select 'os_by_lei', k.lei, o.NAME, left(o.DATASETS::text, 250), left(o.SANCTIONS::text, 250)
from kids11 k join LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS_DEFAULT o on o.IDENTIFIERS::text ilike '%' || k.lei || '%'
union all
select 'peer', iff(sdn_parent = 1, 'SDN parent', 'other RU parent'), count(*)::text, count_if(crst = 'ISSUED')::text, round(count_if(crst = 'ISSUED') / count(*), 3)::text
from ru group by sdn_parent
