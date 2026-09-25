"""Skeptic runner, read-only. 2 session lines + SELECT/WITH statements only."""
import sys, re, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
from connect import db  # noqa

T = """t as (select coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, trim(DRUG_SEQ) seq, upper(trim(ROLE_COD)) role,
   case when upper(DRUGNAME) like 'FENTORA%' then 'FENTORA' else 'ACTIQ' end brand
   from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DRUG where upper(trim(ROLE_COD)) in ('PS','SS') and (upper(DRUGNAME) like 'ACTIQ%' or upper(DRUGNAME) like 'FENTORA%'))"""
D = """d0 as (select coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, coalesce(nullif(trim(C_CASE),''),nullif(trim(CASEID),'')) cs, SRC_QUARTER q,
   upper(trim(OCCP_COD)) occ, upper(trim(MFR_SNDR)) snd, upper(trim(REPT_COD)) rept, trim(MFR_NUM) mfr, EVENT_DT evt, trim(AGE) age, trim(GNDR_COD) sex,
   upper(trim(coalesce(REPORTER_COUNTRY, OCCR_COUNTRY))) ctry from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DEMO),
d as (select * from d0 where id in (select id from t))"""
I = """i as (select coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, coalesce(nullif(trim(DRUG_SEQ),''),trim(INDI_DRUG_SEQ)) seq, upper(trim(INDI_PT)) ip
   from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_INDI where coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) in (select id from t)),
ic as (select *, case when ip is null or ip like '%UNKNOWN%' then 'unknown'
  when regexp_like(ip,'.*(CANCER|CARCINOMA|NEOPLASM|TUMOU?R|LYMPHOMA|LEUK|MYELOMA|METASTA|MALIGNAN|SARCOMA|MELANOMA|BLASTOMA|MESOTHELIOMA|ONCO).*') then 'cancer'
  when ip in ('PAIN','BREAKTHROUGH PAIN','ANALGESIC THERAPY','PAIN MANAGEMENT','ANALGESIA','DRUG USE FOR UNKNOWN INDICATION') then 'generic_pain'
  else 'named_noncancer' end cls,
  iff(regexp_like(coalesce(ip,''),'.*(ABUSE|MISUSE|DEPENDENCE|ADDICTION|OVERDOSE|EXPOSURE|WITHDRAWAL|SUICID|RECREATIONAL|ACCIDENTAL|INTENTIONAL|SEDATION|ANAESTHE|ANESTHE|PREMEDICATION|PROCEDURAL|POSTOPERATIVE|OPIOID|OPIATE|OFF LABEL|DETOX|HOSPICE|PALLIATIVE|CHEMOTHERAPY|RADIOTHERAPY|PRODUCT USED).*'),1,0) not_dx
  from i)"""
X = """x as (select t.brand, t.role, d.id, d.cs, d.q, d.occ, d.snd, d.rept, d.mfr, d.evt, d.age, d.sex, d.ctry, ic.ip, ic.cls, ic.not_dx
   from t join d on d.id=t.id left join ic on ic.id=t.id and ic.seq=t.seq),
a as (select cs, max(iff(cls='cancer',1,0)) ca, max(iff(cls='named_noncancer',1,0)) nc, max(iff(cls='named_noncancer' and not_dx=0,1,0)) nc_dx,
   max(iff(cls='generic_pain',1,0)) gp, count(distinct brand) nb, min(q) qmin, max(q) qmax, max(iff(role='PS',1,0)) ps,
   max(occ) occ, max(snd) snd, max(rept) rept, max(mfr) mfr, max(evt) evt, max(age) age, max(sex) sex, max(ctry) ctry,
   max(iff(brand='ACTIQ',1,0)) is_a, max(iff(brand='FENTORA',1,0)) is_f from x group by 1)"""
CAN = "'.*(CANCER|CARCINOMA|NEOPLASM|TUMOU?R|LYMPHOMA|LEUK|MYELOMA|METASTA|MALIGNAN|SARCOMA|MELANOMA|BLASTOMA|MESOTHELIOMA|ONCO|CHEMOTHERAPY|RADIOTHERAPY|PALLIATIVE|HOSPICE|HODGKIN|GLIOMA|MYELODYSPLAS).*'"
ONC = "'.*(TAXOL|PACLITAXEL|DOCETAXEL|TAXOTERE|CISPLATIN|CARBOPLATIN|GEMCITABINE|GEMZAR|AVASTIN|BEVACIZUMAB|TARCEVA|ERLOTINIB|XELODA|CAPECITABINE|FLUOROURACIL|CYCLOPHOSPHAMIDE|DOXORUBICIN|TAMOXIFEN|ANASTROZOLE|ARIMIDEX|LETROZOLE|FEMARA|ZOMETA|XGEVA|RITUX|HERCEPTIN|GLEEVEC|GLIVEC|IRINOTECAN|OXALIPLATIN|ELOXATIN|ETOPOSIDE|VINCRISTINE|NEULASTA|PEGFILGRASTIM|FILGRASTIM|NEUPOGEN|ERBITUX|CETUXIMAB|ALIMTA|PEMETREXED|VELCADE|REVLIMID|THALOMID|TEMODAR|SUTENT|NEXAVAR|CASODEX|LUPRON|ZOLADEX|FASLODEX|AROMASIN|IRESSA|TYKERB|ABRAXANE|CAMPTOSAR|ADRIAMYCIN).*'"
TRIAL = "'.*(PLACEBO|BLINDED|STUDY|INVESTIGATIONAL|UNBLIND).*'"
SIG = """,
ncc as (select * from a where nc=1),
ids as (select distinct d0.id, d0.cs from d0 join ncc on ncc.cs=d0.cs),
oi as (select ids.cs, max(iff(regexp_like(upper(trim(n.INDI_PT)),__CAN__),1,0)) ind_ca
   from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_INDI n join ids on ids.id=coalesce(nullif(trim(n.ISR),''),nullif(trim(n.PRIMARYID),'')) group by 1),
rr as (select ids.cs, max(iff(regexp_like(upper(trim(r.PT)),__CAN__),1,0)) reac_ca
   from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_REAC r join ids on ids.id=coalesce(nullif(trim(r.ISR),''),nullif(trim(r.PRIMARYID),'')) group by 1),
dd as (select ids.cs, max(iff(regexp_like(upper(g.DRUGNAME),__ONC__),1,0)) onc_drug,
   max(iff(regexp_like(upper(g.DRUGNAME),__TRIAL__),1,0)) trial_drug
   from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DRUG g join ids on ids.id=coalesce(nullif(trim(g.ISR),''),nullif(trim(g.PRIMARYID),'')) group by 1),
s as (select ncc.*, coalesce(oi.ind_ca,0) ind_ca, coalesce(rr.reac_ca,0) reac_ca, coalesce(dd.onc_drug,0) onc_drug, coalesce(dd.trial_drug,0) trial_drug,
   iff(ncc.ca=1 or oi.ind_ca=1 or rr.reac_ca=1 or dd.onc_drug=1,1,0) any_ca,
   case when qmin<='2011q4' then '1 pre2012' when qmin<='2012q3' then '2 2012q1-3' else '3 new fmt' end per,
   case when occ in ('MD','PH','OT','HP') then 'HP' when occ='CN' then 'CN' when occ='LW' then 'LW' else 'blank' end who
   from ncc left join oi on oi.cs=ncc.cs left join rr on rr.cs=ncc.cs left join dd on dd.cs=ncc.cs)"""
SIG = SIG.replace("__CAN__", CAN).replace("__ONC__", ONC).replace("__TRIAL__", TRIAL)
W = "with " + T + ",\n" + D + ",\n" + I + ",\n" + X
STMTS = {}
STMTS["s03_rederive"] = W + """
select 'brand' k, brand v, count(*) cases, sum(ca) ca, sum(nc) nc, count_if(ca=1 and nc=1) both_, count_if(nc=1 and ps=1) nc_ps, count_if(qmin<='2012q3' and qmax>='2012q4') cross_fmt
from (select brand, cs, max(iff(cls='cancer',1,0)) ca, max(iff(cls='named_noncancer',1,0)) nc, max(iff(role='PS',1,0)) ps, min(q) qmin, max(q) qmax from x group by 1,2) group by 2
union all select 'combined', 'A+F', count(*), sum(ca), sum(nc), count_if(ca=1 and nc=1), count_if(nc=1 and ps=1), count_if(qmin<='2012q3' and qmax>='2012q4') from a
union all select 'both_brands', 'nb=2', count_if(nb=2), sum(iff(nb=2,ca,0)), sum(iff(nb=2,nc,0)), count_if(nb=2 and ca=1 and nc=1), null, null from a
union all select 'nc_dx', 'named noncancer minus abuse/exposure/procedural etc', count_if(nc_dx=1), count_if(nc_dx=1 and ca=1), null, null, null, null from a
union all select 'versions', 'cases with more than 1 report id', count(*), null, null, null, null, null from (select cs from d group by cs having count(distinct id)>1)
union all select 'nullcase', 'ids with null case', count_if(cs is null), count(*), null, null, null, null from d"""

STMTS["s04_terms"] = W + """
select cls, not_dx, ip, count(distinct cs) cases, count(distinct iff(brand='ACTIQ',cs,null)) actiq, count(distinct iff(brand='FENTORA',cs,null)) fentora,
  count(distinct iff(occ in ('MD','PH','OT','HP') and q<='2011q4',cs,null)) hp_pre2012
from x where cls in ('named_noncancer','cancer') group by 1,2,3 order by 1 desc, 4 desc"""

STMTS["s05_cancer_elsewhere"] = W + SIG + """
select coalesce(per,'ALL') per, coalesce(who,'ALL') who, count(*) nc_cases, sum(ca) line_ca, sum(ind_ca) any_indi_ca, sum(reac_ca) reac_ca, sum(onc_drug) onc_drug,
  sum(any_ca) any_ca_signal, count_if(any_ca=0) nc_no_ca_signal, count_if(any_ca=0 and nc_dx=1) nc_dx_no_ca_signal, sum(trial_drug) trial_drug
from s group by rollup(per, who) order by 1,2"""

STMTS["s06_concentration"] = W + """
select 'q' k, qmin v, count(*) n, sum(ca) n2 from a where nc=1 group by 2
union all select 'q_all', qmin, count(*), sum(nc) from a group by 2
union all select * from (select 'snd', snd, count(*), sum(ca) from a where nc=1 group by 2 order by 3 desc limit 12)
union all select 'rept', rept, count(*), sum(ca) from a where nc=1 group by 2
union all select 'yr_who_nc', left(qmin,4)||' '||case when occ in ('MD','PH','OT','HP') then 'HP' when occ='CN' then 'CN' else coalesce(occ,'blank') end, count(*), null from a where nc=1 group by 2
union all select 'yr_who_ca', left(qmin,4)||' '||case when occ in ('MD','PH','OT','HP') then 'HP' when occ='CN' then 'CN' else coalesce(occ,'blank') end, count(*), null from a where ca=1 group by 2
union all select 'ctry', coalesce(ctry,'(null)'), count(*), sum(ca) from a where nc=1 group by 2
union all select 'neardup', 'nc cases w event date; in groups sharing age+sex+evt+ctry', (select count(*) from a where nc=1 and evt is not null),
   (select coalesce(sum(n),0) from (select age, sex, evt, ctry, count(*) n from a where nc=1 and evt is not null group by 1,2,3,4 having count(*)>1))"""
SEP = "' | '"
STMTS["s07_mfrnum_and_sample"] = W + """,
pat as (select iff(nc=1,'nc',iff(ca=1,'ca','other')) cls, left(regexp_replace(upper(coalesce(mfr,'(null)')),'[0-9]+','9'),40) p, count(*) n from a group by 1,2),
samp as (select cs from a where nc=1 and occ in ('MD','PH','OT','HP') and qmin between '2007q1' and '2010q4' order by hash(cs) limit 15),
sid as (select distinct d.id, d.cs from d join samp on samp.cs=d.cs),
od as (select sid.cs, left(listagg(distinct upper(trim(g.DRUGNAME))||':'||upper(trim(g.ROLE_COD)), __SEP__),500) drugs from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DRUG g join sid on sid.id=coalesce(nullif(trim(g.ISR),''),nullif(trim(g.PRIMARYID),'')) group by 1),
oi as (select sid.cs, left(listagg(distinct upper(trim(n.INDI_PT)), __SEP__),400) inds from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_INDI n join sid on sid.id=coalesce(nullif(trim(n.ISR),''),nullif(trim(n.PRIMARYID),'')) group by 1)
select * from (select 'pat' k, cls a, p b, n::varchar c, null e, null f, null g from pat qualify row_number() over (partition by cls order by n desc) <= 12)
union all
select 'sample', a.cs, a.qmin||' '||coalesce(a.snd,'')||' '||coalesce(a.rept,'')||' '||coalesce(a.occ,'')||' '||coalesce(a.ctry,''), coalesce(a.mfr,''), coalesce(a.age,'')||'/'||coalesce(a.sex,''), oi.inds, od.drugs
from a join samp on samp.cs=a.cs left join oi on oi.cs=a.cs left join od on od.cs=a.cs
order by 1,2""".replace("__SEP__", SEP)
STMTS["s08_name_variants"] = """
with v as (select upper(trim(DRUGNAME)) nm, upper(trim(ROUTE)) rt, coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, SRC_QUARTER q
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DRUG where upper(trim(ROLE_COD)) in ('PS','SS')
  and ( upper(DRUGNAME) like '%ACTIQ%' or upper(DRUGNAME) like '%FENTORA%' or upper(DRUGNAME) like '%ONSOLIS%' or upper(DRUGNAME) like '%SUBSYS%'
     or (upper(DRUGNAME) like '%FENTANYL%' and (regexp_like(upper(DRUGNAME),'.*(LOZENGE|TRANSMUCOSAL|BUCCAL|SUBLINGUAL|NASAL|LOLLI|TROCHE|ORAL|EFFERVESCENT|SPRAY|FILM|STICK|OTFC).*')
          or upper(trim(ROUTE)) in ('BUCCAL','SUBLINGUAL','TRANSMUCOSAL','ORAL','NASAL','OROMUCOSAL','OROPHARINGEAL','INTRANASAL')))))
select nm, rt, count(distinct id) ids, min(q) qmin, max(q) qmax,
  iff(nm like 'ACTIQ%' or nm like 'FENTORA%' or nm like 'ONSOLIS%' or nm like 'SUBSYS%','caught','missed') caught
from v group by 1,2 order by 3 desc limit 60"""

STMTS["s09_peers"] = """
with t as (select coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, trim(DRUG_SEQ) seq, iff(upper(DRUGNAME) like 'ONSOLIS%','ONSOLIS','SUBSYS') brand
   from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DRUG where upper(trim(ROLE_COD)) in ('PS','SS') and (upper(DRUGNAME) like 'ONSOLIS%' or upper(DRUGNAME) like 'SUBSYS%')),
d as (select coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, coalesce(nullif(trim(C_CASE),''),nullif(trim(CASEID),'')) cs, SRC_QUARTER q, upper(trim(OCCP_COD)) occ, upper(trim(MFR_SNDR)) snd, upper(trim(REPT_COD)) rept, trim(MFR_NUM) mfr
   from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DEMO where coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) in (select id from t)),
i as (select coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, coalesce(nullif(trim(DRUG_SEQ),''),trim(INDI_DRUG_SEQ)) seq, upper(trim(INDI_PT)) ip
   from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_INDI where coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) in (select id from t)),
j as (select t.brand, d.cs, min(d.q) q, max(d.occ) occ, max(d.snd) snd, max(d.rept) rept, max(d.mfr) mfr,
   max(iff(regexp_like(ip,'.*(CANCER|CARCINOMA|NEOPLASM|TUMOU?R|LYMPHOMA|LEUK|MYELOMA|METASTA|MALIGNAN|SARCOMA|MELANOMA|BLASTOMA|MESOTHELIOMA|ONCO).*'),1,0)) ca
   from t join d on d.id=t.id left join i on i.id=t.id and i.seq=t.seq group by 1,2)
select brand, q, coalesce(occ,'blank') occ, coalesce(snd,'') snd, coalesce(rept,'') rept, count(*) cases, sum(ca) ca,
  left(regexp_replace(upper(coalesce(min(mfr),'')),'[0-9]+','9'),30) mfr_pat
from j group by 1,2,3,4,5 order by 1,2,3"""

STMTS["s10_sensitivity"] = """
with t as (select coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, trim(DRUG_SEQ) seq,
   case when upper(DRUGNAME) like 'ACTIQ%' or upper(DRUGNAME) like 'FENTORA%' then 'brand' else 'generic_or_eu' end grp
   from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DRUG where upper(trim(ROLE_COD)) in ('PS','SS')
   and (upper(DRUGNAME) like 'ACTIQ%' or upper(DRUGNAME) like 'FENTORA%' or upper(DRUGNAME) like 'EFFENTORA%' or upper(DRUGNAME) like '%ORAVESCENT%'
        or upper(DRUGNAME) like 'OTFC%' or upper(DRUGNAME) like '%ORAL TRANSMUCOSAL FENTANYL%'
        or (upper(trim(DRUGNAME)) like 'FENTANYL CITRATE%' and upper(trim(ROUTE)) in ('BUCCAL','ORAL','SUBLINGUAL','OROPHARINGEAL','TRANSMUCOSAL')))),
d as (select coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, coalesce(nullif(trim(C_CASE),''),nullif(trim(CASEID),'')) cs, SRC_QUARTER q, upper(trim(OCCP_COD)) occ
   from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_DEMO where coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) in (select id from t)),
i as (select coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) id, coalesce(nullif(trim(DRUG_SEQ),''),trim(INDI_DRUG_SEQ)) seq, upper(trim(INDI_PT)) ip
   from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_FAERS_INDI where coalesce(nullif(trim(ISR),''),nullif(trim(PRIMARYID),'')) in (select id from t)),
ic as (select *, case when ip is null or ip like '%UNKNOWN%' then 'unknown'
  when regexp_like(ip,'.*(CANCER|CARCINOMA|NEOPLASM|TUMOU?R|LYMPHOMA|LEUK|MYELOMA|METASTA|MALIGNAN|SARCOMA|MELANOMA|BLASTOMA|MESOTHELIOMA|ONCO).*') then 'cancer'
  when ip = 'BREAKTHROUGH PAIN' then 'btp'
  when ip in ('PAIN','ANALGESIC THERAPY','PAIN MANAGEMENT','ANALGESIA') then 'generic_pain'
  else 'named_noncancer' end cls from i),
j as (select t.grp, d.cs, min(d.q) q, max(d.occ) occ, max(iff(cls='cancer',1,0)) ca, max(iff(cls='named_noncancer',1,0)) nc, max(iff(cls='btp',1,0)) btp,
   max(iff(cls in ('generic_pain'),1,0)) gp, max(iff(cls='unknown',1,0)) uk, count(ic.ip) nind
   from t join d on d.id=t.id left join ic on ic.id=t.id and ic.seq=t.seq group by 1,2),
k as (select 'ALL' grp, cs, min(q) q, max(occ) occ, max(ca) ca, max(nc) nc, max(btp) btp, max(gp) gp, max(uk) uk, sum(nind) nind from j group by 2
      union all select grp, cs, q, occ, ca, nc, btp, gp, uk, nind from j)
select grp, iff(q<='2011q4' and occ in ('MD','PH','OT','HP'),'HP pre2012','other') slice, count(*) cases, count_if(nind>0) with_reason,
  sum(nc) nc, sum(ca) ca, count_if(ca=1 or btp=1) ca_or_btp, count_if(nc=1 and ca=0 and btp=0) nc_only,
  count_if(nind>0 and nc=0 and ca=0 and btp=0) neither
from k group by rollup(grp, slice) order by 1,2"""

if __name__ == "__main__":
    names = sys.argv[1:] or list(STMTS)
    if names == ["--dry"]:
        for k, v in STMTS.items():
            print("--", k, len(v)); print(v[-400:])
        raise SystemExit
    c = db.connect(); cur = c.cursor()
    cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
    cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-skeptic-2026-09-24'")
    with open(HERE / "skeptic.sql", "a", encoding="utf-8") as log:
        for nm in names:
            sql = STMTS[nm]
            assert re.match(r"^\s*(with|select)\b", sql, re.I), nm
            log.write(f"-- {nm}\n{sql};\n\n")
            t0 = time.time()
            try:
                cur.execute(sql)
                cols = [x[0] for x in cur.description]; rows = cur.fetchall()
                txt = "\t".join(cols) + "\n" + "\n".join("\t".join("" if v is None else str(v) for v in r) for r in rows)
                print(f"== {nm} ({len(rows)} rows, {time.time()-t0:.1f}s)", flush=True)
            except Exception as e:
                txt = f"ERROR {e}"; print(f"== {nm} ERROR {e}", flush=True)
            (HERE / f"{nm}.txt").write_text(txt, encoding="utf-8")
    cur.close(); c.close()
