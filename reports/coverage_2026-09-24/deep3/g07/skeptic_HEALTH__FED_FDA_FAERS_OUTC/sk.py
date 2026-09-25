"""Skeptic runner, read-only. SELECT/WITH only. Usage: python sk.py q1 q2 ..."""
import sys, time
from pathlib import Path
REPO = Path(r"C:/Code/Ripple_v6")
sys.path.insert(0, str(REPO))
from connect import db
HERE = Path(__file__).resolve().parent
D = "LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DEMO"
DR = "LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DRUG"
O = "LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_OUTC"
ID = "coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),''))"
CS = "coalesce(nullif(trim(C_CASE),''),nullif(trim(CASEID),''))"
FIVE = "('TARCEVA','ERLOTINIB TABLET','AVASTIN','XELODA','RITUXAN','HERCEPTIN')"
Q = {}
Q["q1"] = f"""
with d as (select {ID} id, {CS} cs, SRC_QUARTER q, MFR_DT mfr, coalesce(try_to_date(FDA_DT,'YYYYMMDD'), INIT_FDA_DT) fda, INIT_FDA_DT ifd,
   upper(coalesce(nullif(trim(I_F_CODE),''), nullif(trim(I_F_COD),''))) ifc from {D} where SRC_QUARTER between '2010q1' and '2014q2'),
dr as (select distinct {ID} id, iff(upper(trim(DRUGNAME)) in ('TARCEVA','ERLOTINIB TABLET'),'TARCEVA',upper(trim(DRUGNAME))) drug from {DR}
   where SRC_QUARTER between '2010q1' and '2014q2' and upper(trim(ROLE_COD))='PS' and upper(trim(DRUGNAME)) in {FIVE}),
de as (select distinct {ID} id from {O} where SRC_QUARTER between '2010q1' and '2014q2' and upper(coalesce(nullif(trim(OUTC_COD),''),trim(OUTC_CODE)))='DE'),
pc as (select dr.drug, d.q, d.cs, min(d.mfr) mfr, min(d.fda) fda, min(d.ifd) ifd, min(d.ifc) ifc, max(iff(de.id is not null,1,0)) died
   from d join dr on dr.id=d.id left join de on de.id=d.id group by 1,2,3),
a as (select q, sum(died) death_drug_pairs from pc group by 1),
qc as (select q, cs, min(mfr) mfr, min(fda) fda, min(ifd) ifd, min(ifc) ifc, max(died) died, count(distinct drug) ndrug from pc group by 1,2),
b as (select q, count(*) cases, sum(died) death_cases, count_if(died=1 and ndrug>1) death_multi_drug,
   count_if(died=1 and ifc='I') death_ifc_i, count_if(died=1 and ifc='F') death_ifc_f,
   count_if(died=1 and ifd is not null) death_has_ifd,
   count_if(died=1 and ifd >= date_from_parts(left(q,4)::int,(right(q,1)::int-1)*3+1,1)) death_ifd_in_q,
   count_if(died=1 and ifd < '2012-09-01') death_ifd_pre_sep2012,
   median(iff(died=1, datediff(day,mfr,fda), null)) med_mfr_fda,
   median(iff(died=1, datediff(day,ifd,fda), null)) med_ifd_fda,
   median(iff(died=1, datediff(day,mfr,ifd), null)) med_mfr_ifd,
   count_if(died=1 and datediff(day,mfr,fda)>365) death_lag_1y,
   count_if(died=1 and mfr is null) death_no_mfr
 from qc group by 1)
select b.*, a.death_drug_pairs from b join a on a.q=b.q order by b.q
"""
Q["q2"] = f"""
with c as (select SRC_QUARTER q, {CS} cs, max(upper(trim(MFR_SNDR))) snd, min(MFR_DT) mfr, min(coalesce(try_to_date(FDA_DT,'YYYYMMDD'), INIT_FDA_DT)) fda
   from {D} where SRC_QUARTER in ('2012q2','2012q3','2012q4','2013q1','2013q2') group by 1,2),
g as (select q, snd, count(*) n, count(mfr) n_mfr, count_if(datediff(day,mfr,fda)>365) y1 from c group by 1,2),
grp as (select q, case when snd like '%ROCHE%' or snd like '%GENENTECH%' or snd like 'GNE%' then 'ROCHE/GNE' when snd like '%ASTELLAS%' then 'ASTELLAS'
     when snd like '%NOVARTIS%' then 'NOVARTIS' else 'ALL OTHER' end k, sum(n) n, sum(n_mfr) n_mfr, sum(y1) y1 from g group by 1,2
   union all select q, 'TOTAL', sum(n), sum(n_mfr), sum(y1) from g group by 1),
top as (select snd from g where q='2012q4' order by y1 desc limit 15)
select 'grp' t, k, q, n, n_mfr, y1, round(100*y1/nullif(n_mfr,0),2) pct_y1 from grp
union all
select 'snd', g.snd, g.q, g.n, g.n_mfr, g.y1, round(100*g.y1/nullif(g.n_mfr,0),2) from g join top on top.snd=g.snd
order by 1,2,3
"""
Q["q3"] = f"""
with d as (select {ID} id, {CS} cs, MFR_DT mfr, try_to_date(FDA_DT,'YYYYMMDD') fda, INIT_FDA_DT ifd, upper(trim(REPT_COD)) rept, upper(trim(E_SUB)) esub,
   regexp_replace(upper(trim(MFR_NUM)),'[0-9]','#') mshape, upper(trim(MFR_SNDR)) snd from {D} where SRC_QUARTER='2012q4'),
dr as (select distinct {ID} id from {DR} where SRC_QUARTER='2012q4' and upper(trim(ROLE_COD))='PS' and upper(trim(DRUGNAME)) in {FIVE}),
de as (select distinct {ID} id from {O} where SRC_QUARTER='2012q4' and upper(coalesce(nullif(trim(OUTC_COD),''),trim(OUTC_CODE)))='DE'),
x as (select d.* from d join dr on dr.id=d.id join de on de.id=d.id)
select * from (select 'fda_dt' k, fda::varchar v, count(*) n from x group by 2 order by 3 desc limit 8)
union all select * from (select 'mfr_dt', mfr::varchar, count(*) from x group by 2 order by 3 desc limit 8)
union all select 'mfr_year', year(mfr)::varchar, count(*) from x group by 2
union all select 'ifd_year', year(ifd)::varchar, count(*) from x group by 2
union all select 'rept|esub', rept||'|'||coalesce(esub,''), count(*) from x group by 2
union all select * from (select 'mfrnum_shape', snd||' '||left(mshape,30), count(*) from x group by 2 order by 3 desc limit 8)
union all select 'distinct', 'rows='||count(*)||' ids='||count(distinct id)||' cases='||count(distinct cs)||' fda_days='||count(distinct fda)||' mfr_days='||count(distinct mfr)||' mfr_jan1='||count_if(month(mfr)=1 and day(mfr)=1), null from x
order by 1,3 desc
"""
Q["q4"] = f"""
with leg as (select distinct nullif(trim(C_CASE),'') cs from {D} where SRC_QUARTER <= '2012q3' and nullif(trim(C_CASE),'') is not null),
n4 as (select distinct {ID} id, nullif(trim(CASEID),'') cs, INIT_FDA_DT ifd from {D} where SRC_QUARTER='2012q4'),
dr as (select distinct {ID} id from {DR} where SRC_QUARTER='2012q4' and upper(trim(ROLE_COD))='PS' and upper(trim(DRUGNAME)) in {FIVE}),
de as (select distinct {ID} id from {O} where SRC_QUARTER='2012q4' and upper(coalesce(nullif(trim(OUTC_COD),''),trim(OUTC_CODE)))='DE'),
f as (select n4.cs, max(iff(dr.id is not null and de.id is not null,1,0)) five_death, min(n4.ifd) ifd from n4 left join dr on dr.id=n4.id left join de on de.id=n4.id group by 1)
select iff(five_death=1,'five-drug death','all other 2012q4') grp, count(*) cases,
  count(leg.cs) in_legacy_aers, count_if(ifd < '2012-09-01') ifd_before_sep2012, count_if(ifd < '2012-09-01' and leg.cs is null) old_ifd_not_in_legacy
from f left join leg on leg.cs=f.cs group by 1
"""
Q["q5"] = f"""
with d as (select {ID} id, {CS} cs, MFR_DT mfr, coalesce(try_to_date(FDA_DT,'YYYYMMDD'), INIT_FDA_DT) fda, INIT_FDA_DT ifd, upper(trim(MFR_SNDR)) snd from {D} where SRC_QUARTER='2012q4'),
dr as (select distinct {ID} id, upper(trim(DRUGNAME)) drug from {DR} where SRC_QUARTER='2012q4' and upper(trim(ROLE_COD))='PS'),
de as (select distinct {ID} id from {O} where SRC_QUARTER='2012q4' and upper(coalesce(nullif(trim(OUTC_COD),''),trim(OUTC_CODE)))='DE'),
c as (select dr.drug, d.cs, max(d.snd) snd, min(d.mfr) mfr, min(d.fda) fda, min(d.ifd) ifd from d join dr on dr.id=d.id join de on de.id=d.id group by 1,2)
select drug, mode(snd) snd, count(*) death_cases, count(mfr) has_mfr, median(datediff(day,mfr,fda)) med_mfr_fda, count_if(datediff(day,mfr,fda)>365) over_1y,
  count_if(ifd < '2012-09-01') ifd_old
from c group by 1 having count(*) >= 150 order by death_cases desc
"""
Q["q6"] = f"""
with d as (select {ID} id, {CS} cs, MFR_DT mfr, try_to_date(FDA_DT,'YYYYMMDD') fda, EVENT_DT evt, upper(trim(MFR_SNDR)) snd,
   upper(trim(coalesce(REPORTER_COUNTRY, OCCR_COUNTRY))) ctry, upper(trim(OCCP_COD)) occ from {D} where SRC_QUARTER='2012q4'),
dr as (select distinct {ID} id, upper(trim(DRUGNAME)) drug from {DR} where SRC_QUARTER='2012q4' and upper(trim(ROLE_COD))='PS' and upper(trim(DRUGNAME)) in {FIVE}),
de as (select distinct {ID} id from {O} where SRC_QUARTER='2012q4' and upper(coalesce(nullif(trim(OUTC_COD),''),trim(OUTC_CODE)))='DE'),
x as (select dr.drug, d.* from d join dr on dr.id=d.id join de on de.id=d.id),
ap as (select column1 drug, column2::date apd from values ('TARCEVA','2004-11-18'),('ERLOTINIB TABLET','2004-11-18'),('AVASTIN','2004-02-26'),('XELODA','1998-04-30'),('HERCEPTIN','1998-09-25'),('RITUXAN','1997-11-26'))
select x.drug, x.snd, count(*) n, count_if(mfr='2012-01-12') mfr_0112, median(datediff(day,mfr,fda)) med_lag,
 median(iff(mfr='2012-01-12',null,datediff(day,mfr,fda))) med_lag_ex0112, count_if(datediff(day,mfr,fda)>365) over_1y,
 count_if(mfr < ap.apd) mfr_pre_approval, count(evt) has_evt, count_if(mfr < evt) mfr_before_evt,
 count_if(ctry in ('US','UNITED STATES')) us, mode(occ) top_occ, count_if(occ='CN') cn, count_if(fda in ('2012-11-21','2012-12-12')) two_days
from x join ap on ap.drug=x.drug group by 1,2 having count(*)>=20 order by 1,3 desc
"""
Q["q7"] = f"""
with d as (select {ID} id, {CS} cs, upper(trim(MFR_SNDR)) snd, AGE age, upper(trim(GNDR_COD)) sx, WT wt, EVENT_DT evt from {D} where SRC_QUARTER='2012q4'),
dr as (select distinct {ID} id, iff(upper(trim(DRUGNAME)) in ('TARCEVA','ERLOTINIB TABLET'),'TARCEVA',upper(trim(DRUGNAME))) drug from {DR}
   where SRC_QUARTER='2012q4' and upper(trim(ROLE_COD))='PS' and upper(trim(DRUGNAME)) in {FIVE}),
de as (select distinct {ID} id from {O} where SRC_QUARTER='2012q4' and upper(coalesce(nullif(trim(OUTC_COD),''),trim(OUTC_CODE)))='DE'),
x as (select dr.drug, d.* from d join dr on dr.id=d.id join de on de.id=d.id),
oth as (select distinct {ID} id, case when upper(DRUGNAME) like '%TARCEVA%' or upper(DRUGNAME) like '%ERLOTINIB%' then 'TARCEVA'
     when upper(DRUGNAME) like '%AVASTIN%' or upper(DRUGNAME) like '%BEVACIZUMAB%' then 'AVASTIN'
     when upper(DRUGNAME) like '%XELODA%' or upper(DRUGNAME) like '%CAPECITABIN%' then 'XELODA'
     when upper(DRUGNAME) like '%RITUXAN%' or upper(DRUGNAME) like '%RITUXIMAB%' then 'RITUXAN'
     when upper(DRUGNAME) like '%HERCEPTIN%' or upper(DRUGNAME) like '%TRASTUZUMAB%' then 'HERCEPTIN' end fam
   from {DR} where SRC_QUARTER='2012q4' and upper(trim(ROLE_COD))<>'PS'
   and regexp_like(upper(DRUGNAME), '.*(TARCEVA|ERLOTINIB|AVASTIN|BEVACIZUMAB|XELODA|CAPECITABIN|RITUXAN|RITUXIMAB|HERCEPTIN|TRASTUZUMAB).*')),
co as (select x.drug, oth.fam, count(distinct x.cs) n from x join oth on oth.id=x.id and oth.fam<>x.drug group by 1,2),
tup as (select age, sx, wt, evt, count(distinct cs) ncs, count(distinct snd) nsnd, count(distinct drug) ndrug from x
   where evt is not null and nullif(trim(wt),'') is not null and nullif(trim(age),'') is not null group by 1,2,3,4)
select 'co_mention' k, drug||' also lists '||fam v, n from co
union all select 'dup_tuple', 'tuples age+sex+wt+event_dt with 2+ cases / cross-sender / cross-drug', null from dual
union all select 'dup_tuple_n', 'tuples_with_2plus', count_if(ncs>1) from tup
union all select 'dup_tuple_cases', 'cases_in_those', sum(iff(ncs>1,ncs,0)) from tup
union all select 'dup_tuple_x', 'cross_sender_or_drug', count_if(ncs>1 and (nsnd>1 or ndrug>1)) from tup
union all select 'dup_tuple_base', 'cases_with_full_tuple', sum(ncs) from tup
order by 1,3 desc
"""
keys = sys.argv[1:]
c = db.connect(); cur = c.cursor()
cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-skeptic-2026-09-24'")
for k in keys:
    sql = Q[k].strip()
    assert sql.upper().startswith(("SELECT", "WITH")), k
    t0 = time.time()
    try:
        cur.execute(sql)
        cols = [x[0] for x in cur.description]; rows = cur.fetchall()
        lines = ["\t".join(cols)] + ["\t".join("" if v is None else str(v) for v in r) for r in rows]
    except Exception as e:
        lines = [f"ERROR {e}"]
    (HERE / f"{k}.txt").write_text("\n".join(lines), encoding="utf-8")
    print(f"== {k} ({time.time()-t0:.1f}s)"); print("\n".join(lines[:90]))
cur.close(); c.close()
