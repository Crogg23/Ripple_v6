-- GLEIF x OFAC SDN only (via OpenSanctions DATASETS text): SDN-listed parents with an LEI, and the companies GLEIF says they consolidate
with s as (
  select f.value::string lei, any_value(NAME) os_name, max(iff(DATASETS::text ilike '%EU Financial Sanctions%' or DATASETS::text ilike '%EU Council Official Journal%', 1, 0)) eu,
         max(iff(DATASETS::text ilike '%UK HMT%' or DATASETS::text ilike '%UK FCDO%' or DATASETS::text ilike '%OFSI%', 1, 0)) uk
  from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS_DEFAULT,
       lateral flatten(input => regexp_substr_all(IDENTIFIERS::text, '[A-Z0-9]{18}[0-9]{2}')) f
  where DATASETS::text ilike '%US OFAC Specially Designated Nationals (SDN) List%'
  group by 1
),
g as (select LEI, ENTITY_LEGALNAME nm, ENTITY_LEGALADDRESS_COUNTRY ctry, REGISTRATION_REGISTRATIONSTATUS rst, REGISTRATION_MANAGINGLOU lou,
             REGISTRATION_LASTUPDATEDATE::text lupd, REGISTRATION_NEXTRENEWALDATE::text nren
      from LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_GLEIF),
sg as (select s.*, g.nm, g.ctry, g.rst from s join g on g.LEI = s.lei),
r as (select RELATIONSHIP_STARTNODE_NODEID child, RELATIONSHIP_ENDNODE_NODEID parent, RELATIONSHIP_RELATIONSHIPTYPE rtype
      from LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_GLEIF_RELATIONSHIPS
      where RELATIONSHIP_RELATIONSHIPTYPE in ('IS_ULTIMATELY_CONSOLIDATED_BY','IS_DIRECTLY_CONSOLIDATED_BY')),
kids as (select r.child, r.parent, r.rtype, sg.nm pnm, sg.ctry pctry, c.nm cnm, c.ctry cctry, c.rst crst, c.lou clou, c.lupd, c.nren,
           iff(s2.lei is null, 0, 1) child_sdn
         from r join sg on sg.lei = r.parent left join g c on c.LEI = r.child left join s s2 on s2.lei = r.child)
select 'summary' k, (select count(*) from s)::text a, (select count(*) from sg)::text b,
  (select count(distinct parent) from kids)::text c, (select count(distinct child) from kids)::text d,
  (select count(distinct child) from kids where child_sdn = 0)::text e,
  (select count(distinct child) from kids where child_sdn = 0 and crst = 'ISSUED')::text f,
  (select listagg(ctry || ':' || n, ',') within group (order by n desc) from (select ctry, count(*) n from sg group by 1))::text g1,
  null h, null i, null j
union all
select 'kid', child, cnm, cctry, crst, lupd, nren, clou, parent, pnm || ' [' || pctry || ']', rtype
from kids where child_sdn = 0
qualify row_number() over (order by iff(cctry in ('RU','BY'), 1, 0), iff(crst = 'ISSUED', 0, 1), cctry, cnm) <= 150
