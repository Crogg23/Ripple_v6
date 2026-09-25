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
select 'lou', REGISTRATION_MANAGINGLOU, null, null, count(*)::text, null, null from t group by 2 qualify row_number() over (order by count(*) desc) <= 12
