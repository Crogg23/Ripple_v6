-- Slave voyages: name the 1850s-60s US departure ports. Famous late voyages (Erie, Wanderer, Clotilda, Nightingale) show which code is which port;
-- plus every North American port code with voyages arriving 1850-1866
select 'famous' k, SHIPNAME, CAPTAINA, YEARAM, PTDEPIMP, MJSLPTIMP, SLAXIMP, SLAMIMP, FATE4, VOYAGEID
from LIBRARY_MARTS.HISTORY.HISTORY__FED_SLAVEVOYAGES_TRANSATLANTIC
where try_to_number(YEARAM) >= 1850 and (SHIPNAME ilike any ('Erie%','Wanderer%','Clotild%','Nightingale%') or CAPTAINA ilike any ('Gordon, Nath%','Foster, Wil%','Corrie%'))
union all
select 'port', PTDEPIMP, max(DEPTREGIMP), count(*)::varchar, round(sum(try_to_number(SLAXIMP)))::varchar, min(YEARAM), max(YEARAM), count_if(FATE4='3')::varchar, count_if(FATE4='1')::varchar, listagg(distinct SHIPNAME, ', ')
from LIBRARY_MARTS.HISTORY.HISTORY__FED_SLAVEVOYAGES_TRANSATLANTIC
where try_to_number(YEARAM) between 1850 and 1866 and left(PTDEPIMP,1)='2' group by PTDEPIMP
order by 1, 4 desc;
