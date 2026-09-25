-- #20 interpret the court/DOJ misses: FJC criminal name fill, DOJ-listing capture window, and CourtListener for the other unbanned high billers
select 'FJC_CRIM_name_fill' k, count(*)::varchar a, count(nullif(trim(DEFENDANT_NAME),''))::varchar b, max(FILE_DATE)::varchar c from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CRIMINAL
union all
select 'DOJ_listing_window', count(*)::varchar, min(CAPTURED_AT)::varchar, max(CAPTURED_AT)::varchar from LIBRARY_MARTS.INVESTIGATIONS.INVESTIGATIONS__XC_WAYBACK_REPLAY_DOJ_LISTING
union all
select 'DOJ_listing_health_fraud_2025_26', count(*)::varchar, min(LINK_TEXT), max(LINK_TEXT) from LIBRARY_MARTS.INVESTIGATIONS.INVESTIGATIONS__XC_WAYBACK_REPLAY_DOJ_LISTING where CAPTURED_AT >= '2025-01-01' and LINK_TEXT ilike any ('%health care fraud%','%medicare%','%durable medical%')
union all
select 'CL_'||COURT_ID, DATE_FILED::varchar, CASE_NAME, DOCKET_NUMBER from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS
 where CASE_NAME ilike any ('%ND MEDICAL SOLUTIONS%','%HAWKEYE MEDICAL%','%MAIN STREET DME%','%JL WEBB DME%','%SOUTHEASTERN MEDEQUIP%','%LIFELINE MEDICAL SUPPLY%','%GUGAVA%')
