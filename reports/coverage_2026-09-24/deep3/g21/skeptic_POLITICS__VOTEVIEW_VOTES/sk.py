"""Skeptic pass on g21 Voteview lead. Read-only SELECT/WITH. Usage: python sk.py <label> [<label> ...]"""
import sys, json
from pathlib import Path
REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))
from connect import db
HERE = Path(__file__).resolve().parent
M = "LIBRARY_MARTS.POLITICS."
Q = {}
Q["A_tables"] = f"""
select table_catalog, table_schema, table_name, row_count, last_altered
from LIBRARY_RAW.INFORMATION_SCHEMA.TABLES
where table_name ilike '%VOTEVIEW%' or table_name ilike '%ROLLCALL%' or table_name ilike '%SENATE%VOTE%'
union all
select table_catalog, table_schema, table_name, row_count, last_altered
from LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES
where table_name ilike '%VOTE%' or table_name ilike '%ROLLCALL%'
order by 1, 2, 3"""
Q["B_raw_votes"] = f"""
with f as (select distinct try_to_double(ICPSR) icpsr from {M}POLITICS__FED_VOTEVIEW_MEMBERS
           where CONGRESS = 119 and CHAMBER = 'Senate' and BIONAME ilike 'FETTERMAN%'),
r as (select try_to_double(CONGRESS) cg, CHAMBER ch, try_to_double(ROLLNUMBER) rn, try_to_double(ICPSR) ic, try_to_double(CAST_CODE) cc
      from LIBRARY_RAW.LANDING.FED_VOTEVIEW_ROLLCALLS where try_to_double(CONGRESS) in (118, 119)),
k as (select cg, ch, rn, ic, count(*) n, count(distinct cc) ncc from r group by 1, 2, 3, 4)
select r.cg, r.ch, count(*) n, count(distinct r.rn || '|' || r.ic) keys, count(distinct r.rn) rolls, max(r.rn) maxroll,
  (select count(*) from k where k.cg = r.cg and k.ch = r.ch and k.n > 1) dup_keys,
  (select count(*) from k where k.cg = r.cg and k.ch = r.ch and k.ncc > 1) conflicting_keys,
  listagg(iff(f.icpsr is not null and r.rn in (328, 777, 833, 851, 866, 875), r.rn || ':' || r.cc, null), ',') fett
from r left join f on f.icpsr = r.ic group by 1, 2 order by 1, 2"""
Q["C_rederive"] = f"""
with m as (select try_to_double(ICPSR)::number icpsr, count(distinct PARTY_CODE) np, any_value(PARTY_CODE) pc,
                  any_value(BIONAME) nm, any_value(STATE_ABBREV) st
           from {M}POLITICS__FED_VOTEVIEW_MEMBERS where CONGRESS = 119 and CHAMBER = 'Senate' group by 1),
meta as (select try_to_number(to_varchar(ROLLNUMBER)) rn, DATE d, BILL_NUMBER b, VOTE_QUESTION q, VOTE_RESULT res,
                YEA_COUNT yc, NAY_COUNT nc
         from {M}POLITICS__FED_VOTEVIEW_ROLLCALL_META
         where try_to_number(to_varchar(CONGRESS)) = 119 and CHAMBER = 'Senate'
           and VOTE_DESC ilike '%hostilities%' and VOTE_DESC ilike '%Iran%'),
v as (select v.ROLLNUMBER rn, v.ICPSR ic, v.CAST_CODE cc, m.nm, m.st, m.np,
             case when m.icpsr is null then 'X' when try_to_number(to_varchar(m.pc)) = 200 then 'R'
                  when try_to_number(to_varchar(m.pc)) in (100, 328) then 'D' else 'O' end p
      from {M}POLITICS__VOTEVIEW_VOTES v left join m on m.icpsr = v.ICPSR
      where v.CONGRESS = 119 and v.CHAMBER = 'Senate')
select meta.rn, meta.d, meta.b, meta.q, meta.res, meta.yc, meta.nc,
  count(v.rn) rows_n, count(distinct v.ic) ics,
  sum(iff(v.p = 'D' and v.cc in (1,2,3), 1, 0)) dy, sum(iff(v.p = 'D' and v.cc in (4,5,6), 1, 0)) dn,
  sum(iff(v.p = 'D' and v.cc not in (1,2,3,4,5,6), 1, 0)) dnv,
  sum(iff(v.p = 'R' and v.cc in (1,2,3), 1, 0)) ry, sum(iff(v.p = 'R' and v.cc in (4,5,6), 1, 0)) rnay,
  sum(iff(v.p = 'R' and v.cc not in (1,2,3,4,5,6), 1, 0)) rnv,
  listagg(iff(v.p in ('X', 'O'), v.ic || ':' || v.cc, null), ',') other_rows,
  max(v.np) max_party_codes,
  max(iff(v.nm ilike 'FETTERMAN%', v.cc, null)) fett_cc,
  listagg(iff(v.p = 'D' and v.cc in (4,5,6), v.nm || '/' || v.st, null), '; ') d_nays,
  listagg(iff(v.p = 'R' and v.cc in (1,2,3), split_part(v.nm, ',', 1), null), '; ') r_yeas,
  listagg(iff(v.p in ('D','R') and v.cc not in (1,2,3,4,5,6), split_part(v.nm, ',', 1) || '(' || v.p || ')', null), '; ') nv
from meta left join v on v.rn = meta.rn
group by 1, 2, 3, 4, 5, 6, 7 order by 1"""

def main(labels):
    c = db.connect(); cur = c.cursor()
    cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
    cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-skeptic-2026-09-24'")
    for lab in labels:
        sql = Q[lab]
        assert sql.lstrip().lower().startswith(("select", "with"))
        try:
            cur.execute(sql); cols = [d[0] for d in cur.description]; rows = cur.fetchall(); err = None
        except Exception as e:
            cols, rows, err = [], [], str(e)
        (HERE / f"{lab}.json").write_text(json.dumps({"cols": cols, "rows": [[None if x is None else str(x) for x in r] for r in rows], "err": err}), encoding="utf-8")
        print("==", lab, err or f"{len(rows)} rows")
        if not err:
            print(" | ".join(cols))
            for r in rows[:80]: print(" | ".join("" if x is None else str(x) for x in r))
    cur.close(); c.close()

if __name__ == "__main__":
    main(sys.argv[1:])
