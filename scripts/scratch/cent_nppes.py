import sys; sys.path.insert(0,'.')
from connect import db
c=db.connect()
def q(s):
    print("\n## "+s.strip().splitlines()[0][:110])
    for r in db.rows(c,s): print(r)
T='LIBRARY_RAW.LANDING.FED_CMS_NPPES'
q(f"""select count(*), count(nullif(trim(EMPLOYER_IDENTIFICATION_NUMBER_EIN),'')), count(distinct nullif(trim(EMPLOYER_IDENTIFICATION_NUMBER_EIN),'')), count(nullif(trim(PARENT_ORGANIZATION_TIN),'')), count(distinct nullif(trim(PARENT_ORGANIZATION_TIN),'')) from {T}""")
q(f"""select EMPLOYER_IDENTIFICATION_NUMBER_EIN, count(*) from {T} where nullif(trim(EMPLOYER_IDENTIFICATION_NUMBER_EIN),'') is not null group by 1 order by 2 desc limit 8""")
q(f"""select PARENT_ORGANIZATION_TIN, count(*) from {T} where nullif(trim(PARENT_ORGANIZATION_TIN),'') is not null group by 1 order by 2 desc limit 8""")
q(f"""select ENTITY_TYPE_CODE, count(*), count(nullif(trim(EMPLOYER_IDENTIFICATION_NUMBER_EIN),'')), count(nullif(trim(PARENT_ORGANIZATION_TIN),'')) from {T} group by 1 order by 2 desc""")
# does the populated EIN actually hit the money world?
q(f"""select count(distinct n.EIN) from (select distinct nullif(trim(EMPLOYER_IDENTIFICATION_NUMBER_EIN),'') EIN from {T}) n join (select distinct EIN from LIBRARY_RAW.LANDING.FED_IRS_BMF) b on n.EIN=b.EIN""")
q(f"""select count(distinct n.EIN) from (select distinct nullif(trim(PARENT_ORGANIZATION_TIN),'') EIN from {T}) n join (select distinct EIN from LIBRARY_RAW.LANDING.FED_IRS_BMF) b on n.EIN=b.EIN""")
c.close()
