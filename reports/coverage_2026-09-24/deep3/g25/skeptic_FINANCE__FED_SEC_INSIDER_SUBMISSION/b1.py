import sys, json, datetime, decimal
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, r"C:\Code\Ripple_v6")
from connect import db
SUB="LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION"
ND="LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS"
RAW="LIBRARY_RAW.LANDING.FED_SEC_INSIDER_NONDERIV_TRANS"
RO="LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_REPORTINGOWNER"
TK="LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE"
def chk(s):
    h=s.strip().split(None,1)[0].upper(); assert h in ("SELECT","WITH"), h
    return s
CORE=f"""
t as (select ACCESSION_NUMBER acc, min(TRANSACTION_DATE) s_min, max(TRANSACTION_DATE) s_max, round(sum(SHARES)) sh
      from {ND} where TRANSACTION_CODE='S' group by 1),
fl as (select trim(ACCESSION_NUMBER) acc, max(iff(trim(TRANS_TIMELINESS)='L',1,0)) any_l,
         min(coalesce(try_to_date(DEEMED_EXECUTION_DATE,'DD-MON-YYYY'), try_to_date(TRANS_DATE,'DD-MON-YYYY'))) s_min_eff
       from {RAW} where trim(TRANS_CODE)='S' group by 1),
o as (select ACCESSION_NUMBER acc, min(OWNER_CIK) owner from {RO} group by 1),
f as (select sub.ISSUER_CIK ic, sub.ISSUER_NAME nm, sub.ACCESSION_NUMBER acc, sub.FILING_DATE fd, sub.PERIOD_OF_REPORT por,
         sub.NOT_SUBJECT_TO_SECTION16 ns16, t.s_min, t.s_max, t.sh,
         datediff('day', t.s_min, sub.FILING_DATE) lag, datediff('day', t.s_max, sub.FILING_DATE) lagx,
         datediff('day', fl.s_min_eff, sub.FILING_DATE) lag_eff, coalesce(fl.any_l,0) any_l, o.owner
      from {SUB} sub join t on t.acc=sub.ACCESSION_NUMBER left join fl on fl.acc=sub.ACCESSION_NUMBER
      left join o on o.acc=sub.ACCESSION_NUMBER where sub.DOCUMENT_TYPE='4'),
lt as (select f.*, exists(select 1 from f f2 where f2.ic=f.ic and f2.s_min=f.s_min and f2.sh=f.sh
          and f2.lag between 0 and 5 and f2.acc<>f.acc) mir from f where lag between 11 and 365)
"""
Q={}
Q['s1_integrity']=f"""
select 'sub' k, count(*)::text a, count(distinct ACCESSION_NUMBER)::text b, count_if(DOCUMENT_TYPE='4')::text c,
  count_if(DOCUMENT_TYPE='4/A')::text d, min(FILING_DATE)::text e, max(FILING_DATE)::text g from {SUB}
union all
select 'raw_nd', count(*)::text, count(distinct ACCESSION_NUMBER, NONDERIV_TRANS_SK)::text, count_if(trim(TRANS_CODE)='S')::text,
  (select count(*) from {ND})::text, count(distinct ACCESSION_NUMBER)::text, null from {RAW}
union all
select 'tl', coalesce(nullif(trim(TRANS_TIMELINESS),''),'<blank>'), count(*)::text, count_if(trim(TRANS_CODE)='S')::text, null, null, null
from {RAW} group by 2
union all
select 'yr', year(s.FILING_DATE)::text, count(*)::text, count_if(n.acc is not null)::text,
  round(100*count_if(n.acc is not null)/count(*),1)::text, sum(n.nrows)::text, round(sum(n.nrows)/nullif(count_if(n.acc is not null),0),2)::text
from {SUB} s left join (select ACCESSION_NUMBER acc, count(*) nrows from {ND} group by 1) n on n.acc=s.ACCESSION_NUMBER
where s.DOCUMENT_TYPE='4' group by 2
"""
Q['s2_issuers']=f"""
with {CORE},
lt2 as (select acc, row_number() over (partition by ic, s_min, sh order by fd, acc) rn from lt where not mir),
ow as (select ic, owner, count(*) n from lt where not mir group by 1,2),
owm as (select ic, max(n) top_owner_late from ow group by 1),
x as (select try_to_number(CIK) c, max(EXCHANGE) ex from {TK} group by 1),
iss as (select f.ic, max(f.nm) nm, count(*) sale_f,
  count_if(lt.acc is not null) late_all,
  count_if(lt.acc is not null and not lt.mir) a_late,
  count_if(lt.acc is not null and not lt.mir and f.lagx between 11 and 365) b_late,
  count_if(lt.acc is not null and not lt.mir and not coalesce(f.ns16,false)) c_late,
  count_if(lt2.rn=1) d_late,
  count_if(lt.acc is not null and not lt.mir and f.any_l=1) e_late,
  count_if(lt.acc is not null and not lt.mir and f.por=f.s_min) g_late,
  count_if(lt.acc is not null and not lt.mir and f.lag_eff between 11 and 365) h_late,
  count(distinct iff(lt.acc is not null and not lt.mir, f.owner, null)) late_owners,
  count(distinct f.owner) sale_owners
  from f left join lt on lt.acc=f.acc left join lt2 on lt2.acc=f.acc group by 1)
select iss.*, owm.top_owner_late, x.ex from iss left join owm on owm.ic=iss.ic left join x on x.c=try_to_number(iss.ic)
where sale_f>=30
"""
Q['s3_lags']=f"""
with {CORE}
select count(*) sale_f, count_if(lag<0) neg, count_if(lag between 0 and 2) d0_2, count_if(lag between 3 and 10) d3_10,
  count_if(lag between 11 and 365) d11_365, count_if(lag>365) gt365, count_if(lag is null) nul,
  count_if(lag between 11 and 365 and any_l=1) late_L, count_if(lag between 0 and 10 and any_l=1) ontime_L, count_if(lag>365 and any_l=1) gt365_L,
  count_if(any_l=1) all_L,
  count_if(lag between 11 and 365 and ns16) late_ns16, count_if(ns16) all_ns16,
  count_if(lag between 11 and 365 and por=s_min) late_por_eq, count_if(lag between 11 and 365 and por is null) late_por_null,
  count_if(lag between 11 and 365 and por>s_min) late_por_after, count_if(lag between 11 and 365 and por<s_min) late_por_before,
  count_if(lag between 11 and 365 and lagx between 0 and 10) late_but_last_ontime,
  count_if(lag between 11 and 365 and lag_eff < 11) late_rescued_by_deemed,
  (select count(*) from lt) n_lt, (select count_if(mir) from lt) n_mir
from f
"""
Q['s4_named']=f"""
with pick as (
  select ACCESSION_NUMBER a from {SUB} where ACCESSION_NUMBER between '0000929638-22-000360' and '0000929638-22-000385'
  union select ACCESSION_NUMBER from {SUB} where ACCESSION_NUMBER in ('0001437749-20-012379','0001437749-20-012378')
  union select s.ACCESSION_NUMBER from {SUB} s join {RO} r on r.ACCESSION_NUMBER=s.ACCESSION_NUMBER
        where s.ISSUER_CIK='0001562088' and r.OWNER_NAME ilike '%capitalg%'
  union select ACCESSION_NUMBER from {SUB} where ISSUER_CIK in ('0001562088','0000834365','0001624512')
        and DOCUMENT_TYPE in ('4/A','5','5/A') and FILING_DATE >= '2019-01-01'),
fl as (select trim(ACCESSION_NUMBER) acc, max(iff(trim(TRANS_TIMELINESS)='L',1,0)) any_l, listagg(distinct trim(TRANS_CODE), ',') codes,
         min(TRANS_DATE) tmin, count(*) n from {RAW} where trim(ACCESSION_NUMBER) in (select a from pick) group by 1)
select s.ACCESSION_NUMBER, s.DOCUMENT_TYPE, left(s.ISSUER_NAME,22) iss, s.FILING_DATE, s.PERIOD_OF_REPORT, s.DATE_OF_ORIGINAL_SUBMISSION,
  s.NOT_SUBJECT_TO_SECTION16, fl.any_l, fl.codes, fl.tmin, fl.n, left(s.REMARKS,70) rem
from {SUB} s join pick p on p.a=s.ACCESSION_NUMBER left join fl on fl.acc=s.ACCESSION_NUMBER order by 3,4,1
"""
def conv(v):
    if isinstance(v,(datetime.date,datetime.datetime)): return v.isoformat()
    if isinstance(v,decimal.Decimal): return float(v)
    return v
c=db.connect(); cur=c.cursor()
cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-skeptic-2026-09-24'")
out={}
for k,s in Q.items():
    try:
        cur.execute(chk(s)); cols=[d[0] for d in cur.description]
        rows=[[conv(v) for v in r] for r in cur.fetchall()]
        out[k]={"cols":cols,"rows":rows}; print("OK",k,len(rows))
    except Exception as e:
        print("ERR",k,e); out[k]={"err":str(e)}
(HERE/"b1.json").write_text(json.dumps(out,default=str),encoding="utf-8")
cur.close(); c.close()
