-- FEMA gap, the dull explanation: did FEMA announce a new way of publishing declarations? Every FEMA disaster-type notice since Jan 2025 that is not a single-state declaration or amendment, with its abstract
select PUBLICATION_DATE, DOCUMENT_NUMBER, TITLE, left(ABSTRACT, 700) abstract, left(DOCKET_IDS, 200) dockets, left(EXCERPTS, 300) excerpts
from LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS
where AGENCY_NAMES ilike '%Federal Emergency Management Agency%' and PUBLICATION_DATE >= '2025-01-01'
  and (TITLE ilike '%declaration%' or TITLE ilike '%disaster%' or ABSTRACT ilike '%declaration%')
  and TITLE not ilike '%Amendment No%' and TITLE not ilike '%; Major Disaster and Related Determinations%' and TITLE not ilike '%; Emergency and Related Determinations%'
order by PUBLICATION_DATE
