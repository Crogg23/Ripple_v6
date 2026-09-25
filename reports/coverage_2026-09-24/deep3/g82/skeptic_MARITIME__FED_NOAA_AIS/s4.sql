-- Global context: sanctioned hull IMOs worldwide by age band (binding lists vs UA-only); OFAC vessels by type (is cargo 0/1,732 by design?); was SCF NEVA's owner Sovcomflot already listed in Jan 2024?
with os as (select o.ID, o.DATASETS, o.FIRST_SEEN, regexp_replace(t.value::string,'[^0-9]','') d
            from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS_DEFAULT o, lateral flatten(input => split(o.IDENTIFIERS, ';')) t
            where o.ENTITY_TYPE = 'Vessel' and t.value::string ilike 'IMO%' and length(regexp_replace(t.value::string,'[^0-9]','')) = 7),
g as (select d imo,
        max(iff(DATASETS ilike '%OFAC%' or DATASETS ilike '%EU Council%' or DATASETS ilike '%UK FCDO%' or DATASETS ilike '%Canad%' or DATASETS ilike '%Australia%', 1, 0)) gov,
        max(iff(DATASETS ilike '%Ukraine War%', 1, 0)) ua, min(FIRST_SEEN) fs from os group by 1)
select 'global_imo' k, iff(imo < '9400000', 'old', 'new') a, count_if(gov=1)::text b, count_if(gov=0 and ua=1)::text c,
  count_if(gov=1 and fs < '2024-01-09')::text d, count(*)::text e
from g group by 2
union all
select 'ofac_vessel_type', coalesce(VESSEL_TYPE,'(null)'), count(*)::text, null, null, null
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_OFAC_SDN where IS_VESSEL group by 2
union all
(select 'sovcomflot', NAME, ENTITY_TYPE, FIRST_SEEN::text, left(DATASETS,200), left(SANCTIONS,500)
 from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS_DEFAULT where NAME ilike '%sovcomflot%' and ENTITY_TYPE <> 'Vessel' order by FIRST_SEEN limit 6)
