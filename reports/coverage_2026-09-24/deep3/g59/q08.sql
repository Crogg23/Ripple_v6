-- GLEIF x OpenSanctions: LEIs on sanctions lists (verified by landing in the GLEIF entity table), then the companies GLEIF says they consolidate
with s as (
  select f.value::string lei,
    max(iff(DATASETS::text ilike '%OFAC%', 1, 0)) ofac, max(iff(DATASETS::text ilike '%EU %' or DATASETS::text ilike '%EU Council%' or DATASETS::text ilike '%European%', 1, 0)) eu,
    max(iff(DATASETS::text ilike '%UK %' or DATASETS::text ilike '%OFSI%' or DATASETS::text ilike '%HM Treasury%', 1, 0)) uk,
    max(iff(DATASETS::text ilike '%China Sanctions%' or DATASETS::text ilike '%Russia%Unfriendly%' or DATASETS::text ilike '%Russian%countermeasures%', 1, 0)) counter,
    any_value(NAME) os_name
  from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS_DEFAULT,
       lateral flatten(input => regexp_substr_all(IDENTIFIERS::text, '[A-Z0-9]{18}[0-9]{2}')) f
  where SANCTIONS is not null and SANCTIONS::text not in ('', '[]')
  group by 1
),
g as (select LEI, ENTITY_LEGALNAME nm, ENTITY_LEGALADDRESS_COUNTRY ctry, ENTITY_ENTITYSTATUS est, REGISTRATION_REGISTRATIONSTATUS rst
      from LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_GLEIF),
sg as (select s.*, g.nm, g.ctry, g.rst from s join g on g.LEI = s.lei),
r as (select RELATIONSHIP_STARTNODE_NODEID child, RELATIONSHIP_ENDNODE_NODEID parent, RELATIONSHIP_RELATIONSHIPTYPE rtype, REGISTRATION_REGISTRATIONSTATUS rel_rst
      from LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_GLEIF_RELATIONSHIPS
      where RELATIONSHIP_RELATIONSHIPTYPE in ('IS_ULTIMATELY_CONSOLIDATED_BY','IS_DIRECTLY_CONSOLIDATED_BY')),
kids as (select r.*, sg.nm pnm, sg.ctry pctry, sg.ofac, sg.eu, sg.uk, sg.counter, c.nm cnm, c.ctry cctry, c.rst crst, c.est cest,
           (select count(*) from s s2 where s2.lei = r.child) child_listed
         from r join sg on sg.lei = r.parent left join g c on c.LEI = r.child)
select 'summary' k, (select count(*) from s)::text a, (select count(*) from sg)::text b,
  (select count(*) from sg where ofac=1)::text c, (select count(*) from sg where counter=1 and ofac=0 and eu=0 and uk=0)::text d,
  (select count(distinct parent) from kids)::text e, (select count(distinct child) from kids)::text f,
  (select count(distinct child) from kids where child_listed=0)::text g1, null h, null i
union all
select 'parent', parent, any_value(pnm), any_value(pctry), any_value(ofac||'/'||eu||'/'||uk||'/'||counter),
  count(distinct child)::text, count(distinct iff(child_listed=0, child, null))::text,
  count(distinct iff(child_listed=0 and crst='ISSUED', child, null))::text,
  listagg(distinct iff(child_listed=0, cctry, null), ',') within group (order by iff(child_listed=0, cctry, null)),
  left(listagg(distinct iff(child_listed=0 and cctry not in ('RU','BY','IR','KP','CN','SY','VE'), cnm || ' [' || cctry || ',' || crst || ']', null), ' | '), 700)
from kids group by parent
qualify row_number() over (order by count(distinct iff(child_listed=0, child, null)) desc) <= 60
