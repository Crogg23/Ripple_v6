-- deep3 / g59: proper look at five glance-only tables, 2026-09-24
-- Tables: ECONOMICS__INTL_GLEIF_RELATIONSHIPS, ECONOMICS__INTL_FAO_FAOSTAT_FOOD_SECURITY,
--         ECONOMICS__INTL_IPC_FOOD_INSECURITY_GLOBAL, ECONOMICS__FED_SEC_EDGAR_COMPANY_TICKERS,
--         ECONOMICS__XC_OWID_GINI
-- Door: Python (connect/db.py) via g59/run.py. Every connection first ran:
--   ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
--   ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';
-- Read-only: the runner refuses anything that is not SELECT / WITH. Raw results in g59/<label>.json.
-- Statement numbers below count only SELECT/WITH statements against the 35 budget.

-- [q01] statement 1
-- GLEIF relationships: profile. Types, statuses, validation, quantifier units, date sentinels, duplicate edges
with t as (select * from LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_GLEIF_RELATIONSHIPS)
select 'type' k, RELATIONSHIP_RELATIONSHIPTYPE a, RELATIONSHIP_RELATIONSHIPSTATUS b, REGISTRATION_REGISTRATIONSTATUS c, count(*)::text n,
  count(distinct RELATIONSHIP_STARTNODE_NODEID)::text d, count(distinct RELATIONSHIP_ENDNODE_NODEID)::text e
from t group by 2,3,4
union all
select 'valid', REGISTRATION_VALIDATIONSOURCES, RELATIONSHIP_RELATIONSHIPTYPE, null, count(*)::text, null, null from t group by 2,3
union all
select 'quant', RELATIONSHIP_QUANTIFIERS_1_MEASUREMENTMETHOD, RELATIONSHIP_QUANTIFIERS_1_QUANTIFIERUNITS, RELATIONSHIP_RELATIONSHIPTYPE, count(*)::text,
  count_if(try_to_double(RELATIONSHIP_QUANTIFIERS_1_QUANTIFIERAMOUNT::text) > 100)::text, median(try_to_double(RELATIONSHIP_QUANTIFIERS_1_QUANTIFIERAMOUNT::text))::text
from t where RELATIONSHIP_QUANTIFIERS_1_QUANTIFIERAMOUNT is not null group by 2,3,4
union all
select 'dates', RELATIONSHIP_PERIOD_1_PERIODTYPE, null, null, count(*)::text,
  count_if(try_to_date(left(RELATIONSHIP_PERIOD_1_STARTDATE::text,10)) > '2026-09-24')::text || ' future',
  count_if(try_to_date(left(RELATIONSHIP_PERIOD_1_STARTDATE::text,10)) < '1900-01-01')::text || ' pre1900'
from t group by 2
union all
select 'dupedge', null, null, null, count(*)::text, count(distinct RELATIONSHIP_STARTNODE_NODEID||'>'||RELATIONSHIP_ENDNODE_NODEID||'>'||RELATIONSHIP_RELATIONSHIPTYPE)::text,
  count(distinct RELATIONSHIP_STARTNODE_NODEID||'>'||RELATIONSHIP_RELATIONSHIPTYPE)::text
from t
union all
select 'lou', REGISTRATION_MANAGINGLOU, null, null, count(*)::text, null, null from t group by 2 qualify row_number() over (order by count(*) desc) <= 12;

-- [q02] statement 2
-- FAO food security: profile of measures, elements, years, flags, text values
with t as (select * from LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_FAO_FAOSTAT_FOOD_SECURITY)
select ITEM_CODE, ITEM, UNIT, count(*) n, count(distinct AREA_CODE) areas, count(distinct YEAR_CODE) years,
  min(YEAR_CODE) y0, max(YEAR_CODE) y1, listagg(distinct ELEMENT, '|') elems,
  count_if(VALUE like '<%') lt_vals, count_if(try_to_double(VALUE) is null and VALUE is not null and VALUE not like '<%') nonnum,
  count_if(VALUE is null or VALUE='') blank, listagg(distinct FLAG, '|') flags
from t group by 1,2,3 order by 1;

-- [q03] statement 3
-- IPC: whole table (735 rows), analyzed locally
select * from LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_IPC_FOOD_INSECURITY_GLOBAL;

-- [q04] statement 4
-- OWID Gini: whole table (2,389 rows), analyzed locally
select * from LIBRARY_MARTS.ECONOMICS.ECONOMICS__XC_OWID_GINI;

-- [q05] statement 5
-- SEC tickers (ECONOMICS copy) vs the FINANCE copy g30 already checked: lookup shape, load runs, overlap
with e as (select CIK, TICKER, COMPANY_TITLE, _SOURCE_RUN_ID, _INGESTED_AT from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SEC_EDGAR_COMPANY_TICKERS),
f as (select CIK, TICKER from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE)
select 'e_profile' k, count(*)::text a, count(distinct CIK)::text b, count(distinct CIK||'|'||TICKER)::text c, count(distinct TICKER)::text d,
  count(distinct _SOURCE_RUN_ID)::text e1, min(_INGESTED_AT)::text f1, max(_INGESTED_AT)::text g1 from e
union all
select 'top_ticker', TICKER, count(*)::text, null, null, null, null, null from e group by TICKER qualify row_number() over (order by count(*) desc) <= 3
union all
select 'top_cik', CIK::text, count(*)::text, any_value(COMPANY_TITLE), listagg(TICKER, ',') within group (order by TICKER), null, null, null from e group by CIK qualify row_number() over (order by count(*) desc) <= 3
union all
select 'overlap', (select count(*) from e where (CIK, TICKER) in (select CIK, TICKER from f))::text,
  (select count(*) from e where (CIK, TICKER) not in (select CIK, TICKER from f))::text,
  (select count(*) from f where (CIK, TICKER) not in (select CIK, TICKER from e))::text, null, null, null, null;

-- [q06] statement 6
-- FAO: pull the headline hunger series (point values only, not the confidence bounds) for local analysis
select AREA_CODE, AREA_CODE_M49, AREA, ITEM_CODE, YEAR_CODE, YEAR, VALUE, FLAG, NOTE
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_FAO_FAOSTAT_FOOD_SECURITY
where ELEMENT = 'Value'
  and ITEM_CODE in ('210041','210011','210091','210401','210081','210071','210090','210400','210040','21025','210010');

-- [q07] statement 7
-- GLEIF join prep: do the OpenSanctions tables carry LEIs? Count LEI-shaped tokens and sample the IDENTIFIERS text
with a as (
  select 'OPENSANCTIONS' src, SCHEMA typ, DATASET ds, (SANCTIONS is not null and SANCTIONS::text not in ('','[]')) has_sanc, IDENTIFIERS::text ids
  from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS
  union all
  select 'DEFAULT', ENTITY_TYPE, DATASETS::text, (SANCTIONS is not null and SANCTIONS::text not in ('','[]')), IDENTIFIERS::text
  from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS_DEFAULT
)
select src, typ, has_sanc, count(*) n, count_if(regexp_like(ids, '.*[A-Z0-9]{18}[0-9]{2}.*', 's')) lei_shaped,
  any_value(iff(regexp_like(ids, '.*[A-Z0-9]{18}[0-9]{2}.*', 's'), left(ids, 300), null)) sample_ids,
  any_value(left(ds, 200)) sample_ds
from a group by 1,2,3 order by 1, n desc;

-- [q08] statement 8
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
qualify row_number() over (order by count(distinct iff(child_listed=0, child, null)) desc) <= 60;

-- [q09] statement 9
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
qualify row_number() over (order by iff(cctry in ('RU','BY'), 1, 0), iff(crst = 'ISSUED', 0, 1), cctry, cnm) <= 150;

-- [q10] statement 10
-- Verify the SDN-LEI set against the primary OFAC table (REMARKS "Legal Entity Number ..."), and pull listing details for the 16 parents
with o as (
  select ENT_NUM, SDN_NAME, PROGRAM, f.value::string lei
  from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_OFAC_SDN,
       lateral flatten(input => regexp_substr_all(REMARKS, 'Legal Entity Number ([A-Z0-9]{20})', 1, 1, 'e', 1)) f
),
os as (
  select f.value::string lei, NAME, FIRST_SEEN::text fs, left(SANCTIONS::text, 600) sanc, left(DATASETS::text, 300) ds
  from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS_DEFAULT,
       lateral flatten(input => regexp_substr_all(IDENTIFIERS::text, '[A-Z0-9]{18}[0-9]{2}')) f
  where DATASETS::text ilike '%US OFAC Specially Designated Nationals (SDN) List%'
),
g as (select LEI from LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_GLEIF)
select 'summary' k, (select count(*) from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_OFAC_SDN where REMARKS ilike '%Legal Entity Number%')::text a,
  (select count(distinct lei) from o)::text b, (select count(distinct o.lei) from o join g on g.LEI = o.lei)::text c,
  (select count(distinct lei) from os)::text d, (select count(distinct o.lei) from o join os on os.lei = o.lei)::text e,
  null f, null h
union all
select 'parent', p.lei, o.SDN_NAME, o.PROGRAM, os.NAME, os.fs, os.sanc, os.ds
from (select column1 lei from values ('549300LCJ1UJXHYBWI24'),('5493009YJ817TFZ7IY48'),('253400DYLWR5A6YAWJ69'),('253400V1H6ART1UQ0N98'),
   ('549300WE6TAF5EEWQS81'),('213800OKDPTV6K4ONO53'),('3358008I6IEH1VUCXE19'),('213800JSZ2UUK4QQK694'),('253400JT3MQWNDKMJE44'),
   ('2549001I42I6G4P13T82'),('213800HE6VDVJWT85874'),('25340076UP17XECUF417'),('549300KBNGV4NYY3GE68'),('253400WSS48YWMBUA688'),
   ('253400QWEQNERA6RJS29'),('52990049IEUGB01L0409')) p
left join o on o.lei = p.lei left join os on os.lei = p.lei;

-- [q11] statement 11
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
from ru group by sdn_parent;

-- [q12] statement 12
-- Eyeball the 11 still-ISSUED foreign subsidiaries: the ownership link records themselves, plus registry numbers (Sistema Asia vs the SDN's 201218988Z)
with k as (select column1 lei from values ('5299007PQV6X4DPL9Y20'),('K80PJMCDA9MAE5C8IO91'),('213800FXBZXOXNXKWP95'),('391200PKEUF3Y2NUMW25'),
   ('72450024EGZK2K8NAG02'),('724500LG1GUKJ5TOIW61'),('724500UTYUSS56QEBB66'),('724500IVNQ6LF8OFIO42'),('7872006AZAFVTVIQ3G32'),
   ('254900YJTZ2JT3ZSZS32'),('253400QD4JHES5PGDR15'))
select k.lei, g.ENTITY_LEGALNAME, g.ENTITY_LEGALADDRESS_CITY, g.ENTITY_REGISTRATIONAUTHORITY_REGISTRATIONAUTHORITYENTITYID reg_no,
  g.ENTITY_ENTITYSTATUS, g.REGISTRATION_INITIALREGISTRATIONDATE::text first_reg, g.REGISTRATION_VALIDATIONSOURCES,
  r.RELATIONSHIP_RELATIONSHIPTYPE, r.RELATIONSHIP_RELATIONSHIPSTATUS, r.REGISTRATION_REGISTRATIONSTATUS rel_rst,
  r.REGISTRATION_LASTUPDATEDATE::text rel_lupd, r.REGISTRATION_VALIDATIONSOURCES rel_valid, r.RELATIONSHIP_QUANTIFIERS_1_QUANTIFIERAMOUNT pct,
  r.RELATIONSHIP_PERIOD_1_STARTDATE::text p1_start, r.RELATIONSHIP_ENDNODE_NODEID parent
from k left join LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_GLEIF g on g.LEI = k.lei
left join LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_GLEIF_RELATIONSHIPS r on r.RELATIONSHIP_STARTNODE_NODEID = k.lei
order by 1, r.RELATIONSHIP_RELATIONSHIPTYPE;
