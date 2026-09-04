import sys; sys.path.insert(0,'.')
from connect import db
c = db.connect()
def q(s, label):
    print("\n## " + label)
    for r in db.rows(c, s):
        print(r)

BANNED = """
select distinct nullif(trim(UNIQUE_ENTITY_ID),'') as UEI
from LIBRARY_RAW.LANDING.FED_SAM_EXCLUSIONS_FULL_R2
where nullif(trim(UNIQUE_ENTITY_ID),'') is not null
"""

q(f"""
with banned as ({BANNED})
select
  s.NAME, s.CLASSIFICATION, s.EXCLUSION_TYPE, s.EXCLUDING_AGENCY,
  b.UEI,
  count(*) as n_awards,
  sum(a.FEDERAL_ACTION_OBLIGATION) as total_obligated,
  min(a.ACTION_DATE) as earliest_award,
  max(a.ACTION_DATE) as latest_award
from banned b
join LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS a
  on a.RECIPIENT_UEI = b.UEI
join LIBRARY_RAW.LANDING.FED_SAM_EXCLUSIONS_FULL_R2 s
  on nullif(trim(s.UNIQUE_ENTITY_ID),'') = b.UEI
group by 1,2,3,4,5
order by total_obligated desc
limit 30
""", "contracts: top 30 banned companies by $ obligated")

q(f"""
with banned as ({BANNED})
select
  s.NAME, s.CLASSIFICATION, s.EXCLUSION_TYPE, s.EXCLUDING_AGENCY,
  b.UEI,
  count(*) as n_awards,
  sum(a."total_obligated_amount") as total_obligated,
  min(a."action_date") as earliest_award,
  max(a."action_date") as latest_award
from banned b
join LIBRARY_RAW.LANDING.FED_USASPENDING_ASSISTANCE_FULL a
  on a."recipient_uei" = b.UEI
join LIBRARY_RAW.LANDING.FED_SAM_EXCLUSIONS_FULL_R2 s
  on nullif(trim(s.UNIQUE_ENTITY_ID),'') = b.UEI
group by 1,2,3,4,5
order by total_obligated desc
limit 30
""", "assistance: top 30 banned companies by $ obligated")

q(f"""
with banned as ({BANNED})
select count(distinct b.UEI) from banned b
join LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS a on a.RECIPIENT_UEI = b.UEI
""", "distinct banned UEIs in contracts")

q(f"""
with banned as ({BANNED})
select count(distinct b.UEI) from banned b
join LIBRARY_RAW.LANDING.FED_USASPENDING_ASSISTANCE_FULL a on a."recipient_uei" = b.UEI
""", "distinct banned UEIs in assistance")

c.close()
