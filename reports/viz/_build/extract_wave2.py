"""Wave-2 extractions: mortgage disparity, detention survival+flows, ownership clock."""
import json, os, sys
sys.path.insert(0, r"c:\Code\Ripple_v6")
from scripts._snowflake_conn import connect
OUT = os.path.dirname(os.path.abspath(__file__))
conn = connect(); cur = conn.cursor()
def q(sql):
    cur.execute(sql); return cur.fetchall()

# ---------- 1. Mortgage denial gap ----------
print("hmda...", flush=True)
rows = q("""
select AS_OF_YEAR, STATE_ABBR,
       case
         when APPLICANT_RACE_NAME_1 = 'White' and APPLICANT_ETHNICITY_NAME = 'Not Hispanic or Latino' then 'White'
         when APPLICANT_RACE_NAME_1 = 'Black or African American' then 'Black'
         when APPLICANT_ETHNICITY_NAME = 'Hispanic or Latino' then 'Hispanic'
         when APPLICANT_RACE_NAME_1 = 'Asian' then 'Asian'
         when APPLICANT_RACE_NAME_1 = 'American Indian or Alaska Native' then 'Native American'
         when APPLICANT_RACE_NAME_1 = 'Native Hawaiian or Other Pacific Islander' then 'Pacific Islander'
         else null end as grp,
       case when APPLICANT_INCOME_000S < 50 then '<50k'
            when APPLICANT_INCOME_000S < 100 then '50-100k'
            when APPLICANT_INCOME_000S < 150 then '100-150k'
            else '150k+' end as inc,
       count(*) as apps,
       sum(iff(ACTION_TAKEN = '3', 1, 0)) as denied
from LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_HISTORIC
where LOAN_PURPOSE = '1' and ACTION_TAKEN in ('1','2','3')
  and APPLICANT_INCOME_000S is not null and STATE_ABBR is not null
group by 1,2,3,4
having grp is not null
""")
json.dump([[r[0], r[1], r[2], r[3], int(r[4]), int(r[5])] for r in rows],
          open(os.path.join(OUT, "hmda_gap.json"), "w"), separators=(",", ":"))
print(f"  {len(rows)} cells", flush=True)

# top denial reasons by group
rows = q("""
select case
         when APPLICANT_RACE_NAME_1 = 'White' and APPLICANT_ETHNICITY_NAME = 'Not Hispanic or Latino' then 'White'
         when APPLICANT_RACE_NAME_1 = 'Black or African American' then 'Black'
         when APPLICANT_ETHNICITY_NAME = 'Hispanic or Latino' then 'Hispanic'
         when APPLICANT_RACE_NAME_1 = 'Asian' then 'Asian'
         else null end as grp,
       DENIAL_REASON_NAME_1, count(*)
from LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_HISTORIC
where LOAN_PURPOSE = '1' and ACTION_TAKEN = '3'
  and DENIAL_REASON_NAME_1 is not null and DENIAL_REASON_NAME_1 <> ''
group by 1,2 having grp is not null
""")
json.dump([[r[0], r[1], int(r[2])] for r in rows],
          open(os.path.join(OUT, "hmda_reasons.json"), "w"), separators=(",", ":"))

# ---------- 2. Detention: survival + flows ----------
print("detention survival...", flush=True)
rows = q("""
with s as (
  select datediff('day', BOOK_IN_AT, BOOK_OUT_AT) as los,
         year(BOOK_IN_AT) as yr,
         coalesce(nullif(trim(CITIZENSHIP_COUNTRY),''),'UNKNOWN') as ctry
  from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_STINTS
  where BOOK_IN_AT is not null and BOOK_OUT_AT is not null
    and DUPLICATE_DROP_ROW is distinct from 'Y'
    and datediff('day', BOOK_IN_AT, BOOK_OUT_AT) between 0 and 2000
)
select yr, ctry, count(*),
  avg(los), median(los),
  percentile_cont(0.75) within group (order by los),
  percentile_cont(0.90) within group (order by los),
  sum(iff(los >= 7,1,0)), sum(iff(los >= 30,1,0)), sum(iff(los >= 90,1,0)),
  sum(iff(los >= 180,1,0)), sum(iff(los >= 365,1,0))
from s group by 1,2
""")
json.dump([[int(r[0]), r[1], int(r[2]), round(float(r[3]),1), float(r[4]),
            float(r[5]), float(r[6]), int(r[7]), int(r[8]), int(r[9]), int(r[10]), int(r[11])]
           for r in rows],
          open(os.path.join(OUT, "det_survival.json"), "w"), separators=(",", ":"))
print(f"  {len(rows)} yr-country cells", flush=True)

print("detention flows...", flush=True)
rows = q("""
select coalesce(nullif(trim(CITIZENSHIP_COUNTRY),''),'UNKNOWN'),
       coalesce(nullif(trim(STATE),''),'?'),
       coalesce(nullif(trim(STAY_RELEASE_REASON),''),'(still held / unrecorded)'),
       count(*)
from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_STINTS
where DUPLICATE_DROP_ROW is distinct from 'Y'
group by 1,2,3
""")
json.dump([[r[0], r[1], r[2], int(r[3])] for r in rows],
          open(os.path.join(OUT, "det_flows.json"), "w"), separators=(",", ":"))
print(f"  {len(rows)} flow cells", flush=True)

# ---------- 3. Ownership clock ----------
print("gleif monthly switches...", flush=True)
rows = q("""
with p as (
  select case when RELATIONSHIP_PERIOD_1_PERIODTYPE='RELATIONSHIP_PERIOD' then RELATIONSHIP_PERIOD_1_STARTDATE
              when RELATIONSHIP_PERIOD_2_PERIODTYPE='RELATIONSHIP_PERIOD' then RELATIONSHIP_PERIOD_2_STARTDATE
              when RELATIONSHIP_PERIOD_3_PERIODTYPE='RELATIONSHIP_PERIOD' then RELATIONSHIP_PERIOD_3_STARTDATE
              when RELATIONSHIP_PERIOD_4_PERIODTYPE='RELATIONSHIP_PERIOD' then RELATIONSHIP_PERIOD_4_STARTDATE
              when RELATIONSHIP_PERIOD_5_PERIODTYPE='RELATIONSHIP_PERIOD' then RELATIONSHIP_PERIOD_5_STARTDATE end as sd,
         case when RELATIONSHIP_PERIOD_1_PERIODTYPE='RELATIONSHIP_PERIOD' then RELATIONSHIP_PERIOD_1_ENDDATE
              when RELATIONSHIP_PERIOD_2_PERIODTYPE='RELATIONSHIP_PERIOD' then RELATIONSHIP_PERIOD_2_ENDDATE
              when RELATIONSHIP_PERIOD_3_PERIODTYPE='RELATIONSHIP_PERIOD' then RELATIONSHIP_PERIOD_3_ENDDATE
              when RELATIONSHIP_PERIOD_4_PERIODTYPE='RELATIONSHIP_PERIOD' then RELATIONSHIP_PERIOD_4_ENDDATE
              when RELATIONSHIP_PERIOD_5_PERIODTYPE='RELATIONSHIP_PERIOD' then RELATIONSHIP_PERIOD_5_ENDDATE end as ed,
         RELATIONSHIP_RELATIONSHIPTYPE as rt
  from LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_GLEIF_RELATIONSHIPS
)
select to_char(date_trunc('month', sd),'YYYY-MM') as mon, rt,
       count(*) as switched_on,
       sum(iff(ed is not null,1,0)) as later_off
from p
where sd between '1995-01-01' and '2026-08-01'
group by 1,2
""")
json.dump([[r[0], r[1], int(r[2]), int(r[3])] for r in rows],
          open(os.path.join(OUT, "gleif_monthly.json"), "w"), separators=(",", ":"))
print(f"  {len(rows)} month cells", flush=True)

print("gleif network...", flush=True)
rows = q("""
with e as (
  select RELATIONSHIP_STARTNODE_NODEID as child, RELATIONSHIP_ENDNODE_NODEID as parent,
         RELATIONSHIP_RELATIONSHIPTYPE as rt,
         coalesce(RELATIONSHIP_PERIOD_1_STARTDATE, RELATIONSHIP_PERIOD_2_STARTDATE) as sd,
         coalesce(RELATIONSHIP_PERIOD_1_ENDDATE, RELATIONSHIP_PERIOD_2_ENDDATE) as ed
  from LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_GLEIF_RELATIONSHIPS
  where RELATIONSHIP_RELATIONSHIPTYPE in ('IS_DIRECTLY_CONSOLIDATED_BY','IS_ULTIMATELY_CONSOLIDATED_BY')
),
deg as (
  select parent as lei, count(*) as n from e group by 1
  order by n desc limit 400
),
keep as (
  select e.* from e join deg on e.parent = deg.lei
  where e.rt = 'IS_DIRECTLY_CONSOLIDATED_BY'
  qualify row_number() over (partition by e.parent order by e.sd) <= 60
)
select k.child, k.parent, to_char(k.sd,'YYYY-MM'), to_char(k.ed,'YYYY-MM'),
       cn.ENTITY_LEGALNAME, cn.ENTITY_LEGALADDRESS_COUNTRY,
       pn.ENTITY_LEGALNAME, pn.ENTITY_LEGALADDRESS_COUNTRY
from keep k
left join LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_GLEIF cn on cn.LEI = k.child
left join LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_GLEIF pn on pn.LEI = k.parent
""")
json.dump([[r[0][:8], r[1][:8], r[2], r[3], r[4], r[5], r[6], r[7]] for r in rows],
          open(os.path.join(OUT, "gleif_net.json"), "w"), separators=(",", ":"))
print(f"  {len(rows)} edges", flush=True)
conn.close()
print("DONE")
