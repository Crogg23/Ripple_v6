"""Hunch 77 probe: every query, in the order run (discovery, pass 1 wide, pass 2 tightened, pass 3 kinds/years, pass 4 stock-only eye check)."""
import sys, json
from _shared.q import run, open_log
open_log("reports/politics_probe_2026-09-05/77_judges_stock_vs_parties/probe.log")
r = run("""
select table_schema, table_name, row_count
from LIBRARY_RAW.information_schema.tables
where table_name like 'FED_COURTLISTENER%' or table_name like 'FED_FJC%'
   or table_name = 'FED_SEC_EDGAR_COMPANY_TICKERS' or table_name like 'FED_FEC_INDIV%'
order by 2,1""", "tables")
for x in r: print(x['TABLE_SCHEMA'], x['TABLE_NAME'], x['ROW_COUNT'])
r = run("""
select table_name, column_name, data_type
from LIBRARY_RAW.information_schema.columns
where table_schema='LANDING' and table_name in ('FED_COURTLISTENER_INVESTMENTS','FED_COURTLISTENER_POSITIONS','FED_COURTLISTENER_PEOPLE','FED_COURTLISTENER_JUDGES','FED_COURTLISTENER_FINANCIAL_DISCLOSURES','FED_COURTLISTENER_COURTS','FED_FJC_SERVICE','FED_FJC_IDB_CIVIL','FED_SEC_EDGAR_COMPANY_TICKERS','FED_COURTLISTENER_JUDGE_POLITICAL_AFFILIATIONS','FED_COURTLISTENER_DISCLOSURE_GIFTS','FED_COURTLISTENER_DISCLOSURE_REIMBURSEMENTS','FED_COURTLISTENER_DISCLOSURE_DEBTS','FED_COURTLISTENER_DOCKETS','FED_FJC_JUDGES','FED_FJC_DEMOGRAPHICS')
order by 1, ordinal_position""", "columns")
cur=None
for x in r:
    if x['TABLE_NAME']!=cur: cur=x['TABLE_NAME']; print("\n##",cur)
    print(" ", x['COLUMN_NAME'], x['DATA_TYPE'])


# ===== SECTION =====
from _shared.q import run, open_log
open_log("reports/politics_probe_2026-09-05/77_judges_stock_vs_parties/probe.log")
L="LIBRARY_RAW.LANDING."
def show(r):
    for x in r: print({k:(str(v)[:90] if v is not None else None) for k,v in x.items()})
show(run(f"select column_name from LIBRARY_RAW.information_schema.columns where table_schema='LANDING' and table_name='FED_COURTLISTENER_FJC_IDB_CL_LINKED' order by ordinal_position","linked_cols"))
show(run(f"select * from {L}FED_COURTLISTENER_FJC_IDB_CL_LINKED limit 3","linked_sample"))
show(run(f"""select count(*) n, count(distinct FINANCIAL_DISCLOSURE_ID) fds, count_if(REDACTED='True' or REDACTED='t' or REDACTED='true') redacted,
  count_if(nullif(trim(DESCRIPTION),'') is not null) has_desc from {L}FED_COURTLISTENER_INVESTMENTS""","inv_counts"))
show(run(f"select DESCRIPTION, GROSS_VALUE_CODE, TRANSACTION_DURING_REPORTING_PERIOD, REDACTED from {L}FED_COURTLISTENER_INVESTMENTS sample (20 rows)","inv_sample"))
show(run(f"""select count(*) n, count(distinct ID) ids, count(distinct PERSON_ID) persons, min(YEAR) y0, max(YEAR) y1, count(distinct YEAR) yrs from {L}FED_COURTLISTENER_FINANCIAL_DISCLOSURES""","fd_counts"))
show(run(f"select YEAR, count(*) n from {L}FED_COURTLISTENER_FINANCIAL_DISCLOSURES group by 1 order by 1","fd_years"))
show(run(f"""select count(*) n, count_if(nullif(ASSIGNED_TO_ID,'') is not null) assigned, count(distinct nullif(ASSIGNED_TO_ID,'')) judges,
  count_if(nullif(IDB_DATA_ID,'') is not null) has_idb, min(nullif(DATE_FILED,'')) d0, max(nullif(DATE_FILED,'')) d1 from {L}FED_COURTLISTENER_DOCKETS""","dockets_counts"))
show(run(f"select count(*) n, count(distinct TITLE) titles, count(distinct CIK_STR) ciks from {L}FED_SEC_EDGAR_COMPANY_TICKERS","tickers"))
show(run(f"select TITLE, TICKER from {L}FED_SEC_EDGAR_COMPANY_TICKERS sample (8 rows)","tickers_sample"))
show(run(f"select DISTRICT, FILEJUDG, count(*) n from {L}FED_FJC_IDB_CIVIL group by 1,2 order by 3 desc limit 5","idb_judge_codes"))


# ===== SECTION =====
"""Hunch 77: judges holding stock in a party before them.
Leg: INVESTMENTS -> FINANCIAL_DISCLOSURES (PERSON_ID, YEAR) -> EDGAR TITLE (2-word key)
     -> DOCKETS where ASSIGNED_TO_ID = judge and CASE_NAME carries the key and the case was open in the disclosure year.
IDB FILEJUDG is blank on the biggest districts, so the FJC route is skipped; dockets carry the CL person id directly."""
import sys, json
from _shared.q import run, open_log
open_log("reports/politics_probe_2026-09-05/77_judges_stock_vs_parties/probe.log")
L = "LIBRARY_RAW.LANDING."
def show(r, n=40):
    for x in r[:n]: print({k:(str(v)[:100] if v is not None else None) for k,v in x.items()})

SUFFIX = "INC|INCORPORATED|CORP|CORPORATION|CO|COMPANY|LTD|LIMITED|LLC|PLC|LP|HOLDINGS|HOLDING|GROUP|ADR|ADS|COM|COMMON|STOCK|STK|SHARES|SHS|NEW|CL|CLASS|A|B|C|THE|DE|NV|SA|AG|NA|N|TRUST|FUND|ETF|INDEX|MUTUAL|BOND|BONDS|NOTE|NOTES|PFD|PREFERRED|ORD|ORDINARY|USA|US"
GENERIC_FIRST = "('UNITED','FIRST','AMERICAN','NATIONAL','GENERAL','BANK','STATE','NORTH','SOUTH','EAST','WEST','NEW','GLOBAL','INTERNATIONAL','UNIVERSAL','CAPITAL','FEDERAL','ROYAL','PACIFIC','ATLANTIC','CENTRAL','SOUTHERN','NORTHERN','WESTERN','EASTERN','UNION','STANDARD','CONTINENTAL','CITY','HOME','LIFE','PUBLIC','SECURITY','MUTUAL','LIBERTY','FIDELITY','INDEPENDENCE','COMMUNITY','PEOPLES','CITIZENS','FARMERS','MERCHANTS','SUN','STAR','WORLD','GREAT','GOLDEN','BLUE','GREEN','RED','BLACK','WHITE','SILVER','ONE','TWO','TRI','MID','ALL','BIG','TRUE','BEST','SMART','SUPER','SIMPLY','ALPHA','OMEGA','DELTA','SIGMA','GAMMA','BETA','APEX','SUMMIT','PRIME','PREMIER','ADVANCED','APPLIED','INTEGRATED','ALLIED','ASSOCIATED','CONSOLIDATED','DIVERSIFIED','SELECT','SPECIALTY','STRATEGIC','ULTRA','MEGA','MICRO','NANO','META','NET','WEB','DIGITAL','DATA','TECH','MEDICAL','HEALTH','ENERGY','POWER','OIL','GAS','GOLD','SOLAR','WATER','AIR','LAND','SEA','REAL','ESTATE','INSURANCE','FINANCIAL','INVESTORS','INVESTMENT','EQUITY','INCOME','GROWTH','VALUE','TOTAL','CORE','MAIN','MAJOR','MODERN','NEXT','FUTURE','LEGACY','HERITAGE','PIONEER','FRONTIER','EMPIRE','KING','QUEEN','CROWN','EAGLE','LION','TIGER','BEAR','BULL','PHOENIX','TITAN','ATLAS','ORION','APOLLO','MERCURY','JUPITER','SATURN','NEPTUNE','PLUTO','MARS','VENUS','EARTH','TERRA','AQUA','SOLAR','LUNAR','STELLAR','COSMOS','GALAXY','NOVA','QUANTUM','FUSION','VECTOR','MATRIX','VERTEX','ZENITH','HORIZON','VISTA','VISION','INSIGHT','FOCUS','CLEAR','BRIGHT','PURE','FRESH','FINE','GOOD','SAFE','SECURE','SURE','TRUST','JOHNSON','SMITH','WILLIAMS','BROWN','JONES','MILLER','DAVIS','WILSON','ANDERSON','TAYLOR','THOMAS','MOORE','MARTIN','JACKSON','THOMPSON','WHITE','HARRIS','CLARK','LEWIS','ROBINSON','WALKER','YOUNG','ALLEN','KING','WRIGHT','SCOTT','HILL','GREEN','ADAMS','BAKER','NELSON','CARTER','MITCHELL','ROBERTS','TURNER','PHILLIPS','CAMPBELL','PARKER','EVANS','EDWARDS','COLLINS','STEWART','MORRIS','MURPHY','COOK','ROGERS','MORGAN','COOPER','PETERSON','REED','BAILEY','BELL','KELLY','HOWARD','WARD','COX','RICHARDSON','WOOD','WATSON','BROOKS','BENNETT','GRAY','JAMES','HUGHES','PRICE','SANDERS','MYERS','LONG','ROSS','FOSTER','POWELL','JENKINS','PERRY','RUSSELL','SULLIVAN','FISHER','HENDERSON','COLEMAN','SIMMONS','PATTERSON','JORDAN','REYNOLDS','HAMILTON','GRAHAM','WALLACE','WOODS','COLE','WEST','STONE','HAWKINS','DUNN','PERKINS','HUDSON','SPENCER','GARDNER','STEPHENS','PAYNE','PIERCE','BERRY','MATTHEWS','ARNOLD','WAGNER','WILLIS','RAY','WATKINS','OLSON','CARROLL','DUNCAN','SNYDER','HART','CUNNINGHAM','BRADLEY','LANE','ANDREWS','RUIZ','HARPER','FOX','RILEY','ARMSTRONG','CARPENTER','WEAVER','GREENE','LAWRENCE','ELLIOTT','CHAVEZ','SIMS','AUSTIN','PETERS','KELLEY','FRANKLIN','LAWSON','FIELDS','GUTIERREZ','RYAN','SCHMIDT','CARR','VASQUEZ','CASTILLO','WHEELER','CHAPMAN','OLIVER','MONTGOMERY','RICHARDS','WILLIAMSON','JOHNSTON','BANKS','MEYER','BISHOP','MCCOY','HOWELL','ALVAREZ','MORRISON','HANSEN','FERNANDEZ','GARZA','HARVEY','LITTLE','BURTON','STANLEY','NGUYEN','GEORGE','JACOBS','REID','KIM','FULLER','LYNCH','DEAN','GILBERT','GARRETT','ROMERO','WELCH','LARSON','FRAZIER','BURKE','HANSON','DAY','MENDOZA','MORENO','BOWMAN','MEDINA','FOWLER','BREWER','HOFFMAN','CARLSON','SILVA','PEARSON','HOLLAND','DOUGLAS','FLEMING','JENSEN','VARGAS','BYRD','DAVIDSON','HOPKINS','MAY','TERRY','HERRERA','WADE','SOTO','WALTERS','CURTIS','NEAL','CALDWELL','LOWE','JENNINGS','BARNETT','GRAVES','JIMENEZ','HORTON','SHELTON','BARRETT','OBRIEN','CASTRO','SUTTON','GREGORY','MCKINNEY','LUCAS','MILES','CRAIG','RODRIQUEZ','CHAMBERS','HOLT','LAMBERT','FLETCHER','WATTS','BATES','HALE','RHODES','PENA','BECK','NEWMAN','HAYNES','MCDANIEL','MENDEZ','BUSH','VAUGHN','PARKS','DAWSON','SANTIAGO','NORRIS','HARDY','LOVE','STEELE','CURRY','POWERS','SCHULTZ','BARKER','GUZMAN','PAGE','MUNOZ','BALL','KELLER','CHANDLER','WEBER','LEONARD','WALSH','LYONS','RAMSEY','WOLFE','SCHNEIDER','MULLINS','BENSON','SHARP','BOWEN','DANIEL','BARBER','CUMMINGS','HINES','BALDWIN','GRIFFITH','VALDEZ','HUBBARD','SALAZAR','REEVES','WARNER','STEVENSON','BURGESS','SANTOS','TATE','CROSS','GARNER','MANN','MACK','MOSS','THORNTON','DENNIS','MCGEE','FARMER','DELGADO','AGUILAR','VEGA','GLOVER','MANNING','COHEN','HARMON','RODGERS','ROBBINS','NEWTON','TODD','BLAIR','HIGGINS','INGRAM','REESE','CANNON','STRICKLAND','TOWNSEND','POTTER','GOODWIN','WALTON','ROWE','HAMPTON','ORTEGA','PATTON','SWANSON','JOSEPH','FRANCIS','GOODMAN','MALDONADO','YATES','BECKER','ERICKSON','HODGES','RIOS','CONNER','ADKINS','WEBSTER','NORMAN','MALONE','HAMMOND','FLOWERS','COBB','MOODY','QUINN','BLAKE','MAXWELL','POPE','FLOYD','OSBORNE','PAUL','MCCARTHY','GUERRERO','LINDSEY','ESTRADA','SANDOVAL','GIBBS','TYLER','GROSS','FITZGERALD','STOKES','DOYLE','SHERMAN','SAUNDERS','WISE','COLON','GILL','ALVARADO','GREER','PADILLA','SIMON','WATERS','NUNEZ','BALLARD','SCHWARTZ','MCBRIDE','HOUSTON','CHRISTENSEN','KLEIN','PRATT','BRIGGS','PARSONS','MCLAUGHLIN','ZIMMERMAN','FRENCH','BUCHANAN','MORAN','COPELAND','ROY','PITTMAN','BRADY','MCCORMICK','HOLLOWAY','BROCK','POOLE','FRANK','LOGAN','OWEN','BASS','MARSH','DRAKE','WONG','JEFFERSON','PARK','MORTON','ABBOTT','SPARKS','PATRICK','NORTON','HUFF','CLAYTON','MASSEY','LLOYD','FIGUEROA','CARSON','BOWERS','ROBERSON','BARTON','TRAN','LAMB','HARRINGTON','CASEY','BOONE','CORTEZ','CLARKE','MATHIS','SINGLETON','WILKINS','CAIN','BRYAN','UNDERWOOD','HOGAN','MCKENZIE','COLLIER','LUNA','PHELPS','MCGUIRE','ALLISON','BRIDGES','WILKERSON','NASH','SUMMERS','ATKINS')"

def norm(col):
    # upper, punctuation to space, drop suffix tokens, squeeze
    return f"""regexp_replace(trim(regexp_replace(regexp_replace(upper({col}), '[^A-Z0-9 ]', ' '), '\\\\b({SUFFIX})\\\\b', ' ')), ' +', ' ')"""

def key(col):
    n = norm(col)
    return f"regexp_substr({n}, '^[A-Z0-9]+ [A-Z0-9]+')"

# Q1: disclosure YEAR pollution
show(run(f"""select count(*) n, count_if(try_to_number(YEAR) between 1990 and 2030) good_year, count(distinct PERSON_ID) persons
  from {L}FED_COURTLISTENER_FINANCIAL_DISCLOSURES""", "fd_year_check"))

# Q2: EDGAR keys, ambiguity
show(run(f"""with k as (select {key('TITLE')} k, TITLE from {L}FED_SEC_EDGAR_COMPANY_TICKERS)
select count(*) n, count_if(k is not null) keyed, count(distinct k) keys,
  (select count(*) from (select k from k where k is not null group by k having count(distinct TITLE) > 1)) ambiguous_keys
from k""", "edgar_keys"))

# Q3: investment descriptions deduped and keyed
show(run(f"""with inv as (select distinct upper(DESCRIPTION) d from {L}FED_COURTLISTENER_INVESTMENTS where nullif(trim(DESCRIPTION),'') is not null)
select count(*) distinct_desc, count_if({key('d')} is not null) keyed from inv""", "inv_keys"))

PAIRS = f"""
edgar as (
  select k, min(TITLE) title from (select {key('TITLE')} k, TITLE from {L}FED_SEC_EDGAR_COMPANY_TICKERS) where k is not null
  group by k having count(distinct TITLE) = 1 and split_part(k,' ',1) not in {GENERIC_FIRST} and split_part(k,' ',2) not in {GENERIC_FIRST}
    and length(k) >= 8 and split_part(k,' ',2) not rlike '^[0-9]+$'
),
inv as (
  select i.DESCRIPTION, {key('i.DESCRIPTION')} k, i.FINANCIAL_DISCLOSURE_ID
  from {L}FED_COURTLISTENER_INVESTMENTS i
  where nullif(trim(i.DESCRIPTION),'') is not null
    and upper(i.DESCRIPTION) not rlike '.*(FUND|ETF|INDEX|MUNI|IRA|401|TRUST|BOND|ANNUITY|PORTFOLIO|MONEY MARKET|CASH|SAVINGS|CHECKING|CD\\\\b|TREASURY|BROKERAGE|ACCOUNT|REAL ESTATE|RENTAL|FARM|PARTNERSHIP).*'
),
fd as (
  select ID, PERSON_ID, try_to_number(YEAR) yr from {L}FED_COURTLISTENER_FINANCIAL_DISCLOSURES
  where try_to_number(YEAR) between 1990 and 2030 and nullif(PERSON_ID,'') is not null
  qualify row_number() over (partition by ID order by DATE_MODIFIED desc) = 1
),
pairs as (
  select distinct fd.PERSON_ID, fd.yr, edgar.k, edgar.title, inv.DESCRIPTION
  from inv join edgar on inv.k = edgar.k join fd on fd.ID = inv.FINANCIAL_DISCLOSURE_ID
)
"""
# Q4: pair counts
show(run(f"""with {PAIRS} select count(*) pair_rows, count(distinct PERSON_ID) judges, count(distinct k) companies, count(distinct PERSON_ID||'|'||yr||'|'||k) judge_year_company from pairs""", "pairs"))
show(run(f"""with {PAIRS} select k, title, DESCRIPTION from pairs sample (12 rows)""", "pairs_sample"))

# Q5: the number — dockets assigned to that judge, naming that company, open in the disclosure year
HITS = f"""
{PAIRS},
pj as (select distinct PERSON_ID from pairs),
dk as (
  select d.ID docket_id, d.ASSIGNED_TO_ID, d.COURT_ID, d.CASE_NAME, d.DOCKET_NUMBER, try_to_date(d.DATE_FILED) filed, try_to_date(d.DATE_TERMINATED) term
  from {L}FED_COURTLISTENER_DOCKETS d join pj on d.ASSIGNED_TO_ID = pj.PERSON_ID
  where nullif(d.CASE_NAME,'') is not null
),
hits as (
  select distinct p.PERSON_ID, p.yr, p.k, p.title, p.DESCRIPTION, dk.docket_id, dk.COURT_ID, dk.CASE_NAME, dk.DOCKET_NUMBER, dk.filed, dk.term
  from dk join (select distinct PERSON_ID, yr, k, title, min(DESCRIPTION) DESCRIPTION from pairs group by 1,2,3,4) p
    on dk.ASSIGNED_TO_ID = p.PERSON_ID
   and regexp_like(upper(dk.CASE_NAME), '.*\\\\b' || p.k || '\\\\b.*')
   and dk.filed <= to_date(p.yr || '-12-31')
   and coalesce(dk.term, to_date('2100-01-01')) >= to_date(p.yr || '-01-01')
)
"""
show(run(f"""with {HITS} select count(*) hit_rows, count(distinct docket_id) dockets, count(distinct PERSON_ID) judges, count(distinct k) companies,
  count(distinct PERSON_ID||'|'||yr||'|'||k) judge_year_company, min(yr) y0, max(yr) y1 from hits""", "hits"))
show(run(f"""with {HITS} select PERSON_ID, k, title, count(distinct docket_id) dockets, min(yr) y0, max(yr) y1, min(CASE_NAME) example, min(DESCRIPTION) holding
  from hits group by 1,2,3 order by 4 desc limit 15""", "hits_top"))
show(run(f"""with {HITS} select PERSON_ID, yr, k, title, DESCRIPTION, COURT_ID, CASE_NAME, DOCKET_NUMBER, filed, term from hits sample (12 rows)""", "hits_sample"))

# ===== SECTION =====
"""Hunch 77, pass 2: tighten. Drop geo keys (LAS VEGAS), drop fund/bond/deposit-looking holdings, break out by company."""
import re
from _shared.q import run, open_log
open_log("reports/politics_probe_2026-09-05/77_judges_stock_vs_parties/probe.log")
src = open("reports/politics_probe_2026-09-05/77_judges_stock_vs_parties/probe.py").read()
FUNDISH = "(FD|FUND|FDS|ADV|ADVANTAGE|ADVISORS|ADVISOR|CLASS|CL A|CL B|RTN|RETURN|CAP|GROWTH|INCOME|VALUE|EQUITY|SECURITIES|BD|BOND|CREDIT|NOTE|NOTES|DEP|DEPOSIT|ACCT|ACCOUNT|CHECKING|SAVINGS|MORTGAGE|MTG|CD|IRA|401|403|529|ANNUITY|PENSION|RETIREMENT|PLAN|MM|MONEY|MARKET|TREASURY|MUNI|PORTFOLIO|INDEX|ETF|TRUST|GA|TX|CA|NY|NC|SC|VA|FL|IL|PA|OH|MI|MN|WI|MO|TN|KY|AL|MS|LA|AR|OK|KS|NE|IA|SD|ND|MT|WY|CO|UT|NV|AZ|NM|ID|OR|WA|AK|HI|ME|NH|VT|MA|RI|CT|NJ|DE|MD|DC|WV|IN)"
PAIRS = f"""
edgar as (
  select k, min(TITLE) title from (select {key('TITLE')} k, TITLE from {L}FED_SEC_EDGAR_COMPANY_TICKERS) where k is not null
  group by k having count(distinct TITLE) = 1 and split_part(k,' ',1) not in {GENERIC_FIRST} and split_part(k,' ',2) not in {GENERIC_FIRST}
    and length(k) >= 8 and split_part(k,' ',2) not rlike '^[0-9]+$'
    and k not in ('LAS VEGAS','NEW YORK','SAN FRANCISCO','SAN DIEGO','SANTA FE','SALT LAKE','LOS ANGELES','KANSAS CITY','SAINT LOUIS','ST LOUIS','PUERTO RICO','SOUTH DAKOTA','NORTH DAKOTA','WEST VIRGINIA','RHODE ISLAND','NEW JERSEY','NEW MEXICO','NEW HAMPSHIRE','NEW ORLEANS','LONG ISLAND','FORT WORTH','SAN ANTONIO','EL PASO','GRAND RAPIDS','BATON ROUGE','LITTLE ROCK','DES MOINES','SIOUX FALLS','SANTA MONICA','BEVERLY HILLS','PALM BEACH','MIAMI BEACH','VIRGINIA BEACH','LAKE CHARLES','CORPUS CHRISTI','ATLANTIC CITY','JERSEY CITY','OKLAHOMA CITY','SALT LAKE')
),
inv as (
  select i.DESCRIPTION, {key('i.DESCRIPTION')} k, i.FINANCIAL_DISCLOSURE_ID
  from {L}FED_COURTLISTENER_INVESTMENTS i
  where nullif(trim(i.DESCRIPTION),'') is not null
    and not regexp_like(upper(i.DESCRIPTION), '.*\\\\b{FUNDISH}\\\\b.*')
),
fd as (
  select ID, PERSON_ID, try_to_number(YEAR) yr from {L}FED_COURTLISTENER_FINANCIAL_DISCLOSURES
  where try_to_number(YEAR) between 1990 and 2030 and nullif(PERSON_ID,'') is not null
  qualify row_number() over (partition by ID order by DATE_MODIFIED desc) = 1
),
pairs as (
  select distinct fd.PERSON_ID, fd.yr, edgar.k, edgar.title, inv.DESCRIPTION
  from inv join edgar on inv.k = edgar.k join fd on fd.ID = inv.FINANCIAL_DISCLOSURE_ID
)
"""
HITS = f"""
{PAIRS},
pj as (select distinct PERSON_ID from pairs),
dk as (
  select d.ID docket_id, d.ASSIGNED_TO_ID, d.COURT_ID, d.CASE_NAME, d.DOCKET_NUMBER, try_to_date(d.DATE_FILED) filed, try_to_date(d.DATE_TERMINATED) term
  from {L}FED_COURTLISTENER_DOCKETS d join pj on d.ASSIGNED_TO_ID = pj.PERSON_ID
  where nullif(d.CASE_NAME,'') is not null
),
hits as (
  select distinct p.PERSON_ID, p.yr, p.k, p.title, p.DESCRIPTION, dk.docket_id, dk.COURT_ID, dk.CASE_NAME, dk.DOCKET_NUMBER, dk.filed, dk.term
  from dk join (select PERSON_ID, yr, k, title, min(DESCRIPTION) DESCRIPTION from pairs group by 1,2,3,4) p
    on dk.ASSIGNED_TO_ID = p.PERSON_ID
   and regexp_like(upper(dk.CASE_NAME), '.*\\\\b' || p.k || '\\\\b.*')
   and dk.filed <= to_date(p.yr || '-12-31')
   and coalesce(dk.term, to_date('2100-01-01')) >= to_date(p.yr || '-01-01')
)
"""
show(run(f"""with {PAIRS} select count(*) pair_rows, count(distinct PERSON_ID) judges, count(distinct k) companies from pairs""", "pairs_strict"))
show(run(f"""with {HITS} select count(*) hit_rows, count(distinct docket_id) dockets, count(distinct PERSON_ID) judges, count(distinct k) companies,
  count(distinct PERSON_ID||'|'||yr||'|'||k) judge_year_company, count(distinct PERSON_ID||'|'||k) judge_company, min(yr) y0, max(yr) y1 from hits""", "hits_strict"))
show(run(f"""with {HITS} select k, title, count(distinct docket_id) dockets, count(distinct PERSON_ID) judges, min(CASE_NAME) example, min(DESCRIPTION) holding
  from hits group by 1,2 order by 3 desc limit 25""", "hits_by_company"), 25)
show(run(f"""with {HITS} select PERSON_ID, yr, k, DESCRIPTION, COURT_ID, CASE_NAME, DOCKET_NUMBER, filed, term from hits where k <> 'WELLS FARGO' sample (15 rows)""", "hits_sample_nonwf"), 15)
show(run(f"""with {HITS} select yr, count(distinct docket_id) dockets, count(distinct PERSON_ID) judges from hits group by 1 order by 1""", "hits_by_year"), 25)

# ===== SECTION =====
"""Hunch 77, pass 3: eye-check sample outside Wells Fargo, split holdings by kind, by year."""
from _shared.q import run, open_log
open_log("reports/politics_probe_2026-09-05/77_judges_stock_vs_parties/probe.log")
show(run(f"""with {HITS} select PERSON_ID, yr, k, DESCRIPTION, COURT_ID, CASE_NAME, DOCKET_NUMBER, filed, term from hits where k not in ('WELLS FARGO','1ST SOURCE','GULF COAST') order by random() limit 15""", "hits_sample_nonwf"), 15)
show(run(f"""with {HITS} select k, DESCRIPTION, count(distinct docket_id) dockets, count(distinct PERSON_ID) judges from hits where k = 'WELLS FARGO' group by 1,2 order by 3 desc limit 15""", "wf_holdings"), 15)
show(run(f"""with {HITS} select iff(regexp_like(upper(DESCRIPTION), '.*(STOCK|COMMON|SHARES|SHS|COM\\\\b|WFC|& CO|&CO|CORP|INC).*'), 'stock-looking', 'bare name') kind,
  count(distinct docket_id) dockets, count(distinct PERSON_ID) judges, count(distinct PERSON_ID||'|'||k) judge_company from hits where k not in ('1ST SOURCE','GULF COAST') group by 1""", "hits_by_kind"))
show(run(f"""with {HITS} select yr, count(distinct docket_id) dockets, count(distinct PERSON_ID) judges from hits where k not in ('1ST SOURCE','GULF COAST') group by 1 order by 1""", "hits_by_year"), 25)

# ===== SECTION =====
"""Hunch 77, pass 4: eye-check the stock-looking hits (the honest number)."""
from _shared.q import run, open_log
open_log("reports/politics_probe_2026-09-05/77_judges_stock_vs_parties/probe.log")
STOCK = "regexp_like(upper(DESCRIPTION), '.*(STOCK|COMMON|SHARES|SHS|COM\\\\b|WFC|& CO|&CO|CORP|INC).*') and k not in ('1ST SOURCE','GULF COAST')"
show(run(f"""with {HITS} select k, count(distinct docket_id) dockets, count(distinct PERSON_ID) judges from hits where {STOCK} group by 1 order by 2 desc""", "stock_by_company"), 30)
show(run(f"""with {HITS} select PERSON_ID, yr, k, DESCRIPTION, COURT_ID, CASE_NAME, DOCKET_NUMBER, filed, term from hits where {STOCK} order by random() limit 12""", "stock_sample"), 12)