-- @senate_delegation_party_118_119
select CONGRESS, STATE_ABBREV, PARTY_CODE, count(distinct ICPSR) senators, listagg(distinct BIONAME, ' | ') names
from LIBRARY_MARTS.POLITICS.POLITICS__FED_VOTEVIEW_MEMBERS
where CONGRESS in (118,119) and CHAMBER = 'Senate'
group by 1,2,3 order by 1,2,3
