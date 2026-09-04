"""Party mix per quiet PAC, reconciled to degree; plus CCN name lookups the report cites."""
import sys; sys.path.insert(0,'.')
from connect import db
c=db.connect()
def q(s):
    print("\n## "+s.strip().splitlines()[0][:110])
    for r in db.rows(c,s): print(r)
ids="'C00545202','C00720649','C00630012','C00027342','C00252940','C00002089'"
q(f"""with x as (select distinct VALUE_A cand, VALUE_B cmte from LIBRARY_META."CONNECT".ENTITY_XREF where KEY_B='FEC_CMTE_ID' and VALUE_B in ({ids})),
n as (select C1 cand, max(C3) pty from LIBRARY_RAW.LANDING.FED_FEC_CANDIDATES group by 1)
select x.cmte, count(distinct x.cand) degree, count(distinct case when pty='DEM' then x.cand end) dem, count(distinct case when pty='REP' then x.cand end) rep,
 count(distinct case when pty is not null and pty not in ('DEM','REP') then x.cand end) other, count(distinct case when pty is null then x.cand end) not_in_cand_file
from x left join n on n.cand=x.cand group by 1 order by 2""")
q("""select KEY_VALUE, max(CANONICAL_NAME), max(CANONICAL_ADDR) from LIBRARY_META."CONNECT".ENTITY_GOLDEN where KEY_TYPE='CCN' and KEY_VALUE in ('113301','150179','381559','758004','113300','110079') group by 1 order by 1""")
c.close()
