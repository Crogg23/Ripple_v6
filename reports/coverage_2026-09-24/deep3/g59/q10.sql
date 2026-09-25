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
left join o on o.lei = p.lei left join os on os.lei = p.lei
