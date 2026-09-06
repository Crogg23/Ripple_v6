"""Hunch 95 probe: every query in the order run."""
from _shared.q import run, open_log
open_log("reports/politics_probe_2026-09-05/95_judge_gifts_vs_parties/probe.log")
L="LIBRARY_RAW.LANDING."
def show(r,n=40):
    for x in r[:n]: print({k:(str(v)[:90] if v is not None else None) for k,v in x.items()})
for t,c in [("DISCLOSURE_GIFTS","SOURCE"),("DISCLOSURE_REIMBURSEMENTS","SOURCE"),("DISCLOSURE_DEBTS","CREDITOR_NAME")]:
    show(run(f"""select count(*) n, count(distinct ID) ids, count(distinct FINANCIAL_DISCLOSURE_ID) fds, count_if(nullif(trim({c}),'') is not null) has_name,
      count(distinct upper({c})) names, count_if(REDACTED in ('t','True','true')) redacted from {L}FED_COURTLISTENER_{t}""", f"{t}_counts"))
    show(run(f"select upper({c}) nm, count(*) n from {L}FED_COURTLISTENER_{t} group by 1 order by 2 desc limit 12", f"{t}_top"), 12)


# ===== SECTION =====
"""Hunch 95: gift source / reimbursement source / creditor appearing as a party before the same judge in the disclosure year.
Leg: DISCLOSURE_{GIFTS,REIMBURSEMENTS,DEBTS} -> FINANCIAL_DISCLOSURES (PERSON_ID, YEAR) -> DOCKETS ASSIGNED_TO_ID + CASE_NAME word match, case open in that year."""
from _shared.q import run, open_log

open_log("reports/politics_probe_2026-09-05/95_judge_gifts_vs_parties/probe.log")
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

open_log("reports/politics_probe_2026-09-05/95_judge_gifts_vs_parties/probe.log")
def nm(col):
    return f"""regexp_replace(trim(regexp_replace(regexp_replace(upper({col}), '[^A-Z0-9 ]', ' '), '\\\\b(INC|INCORPORATED|CORP|CORPORATION|CO|COMPANY|LTD|LLC|LLP|PLC|LP|NA|N A|THE|PC|PA|PLLC)\\\\b', ' ')), ' +', ' ')"""
SRC = f"""
src as (
  select 'gift' kind, FINANCIAL_DISCLOSURE_ID, SOURCE raw from {L}FED_COURTLISTENER_DISCLOSURE_GIFTS
  union all select 'reimbursement', FINANCIAL_DISCLOSURE_ID, SOURCE from {L}FED_COURTLISTENER_DISCLOSURE_REIMBURSEMENTS
  union all select 'debt', FINANCIAL_DISCLOSURE_ID, CREDITOR_NAME from {L}FED_COURTLISTENER_DISCLOSURE_DEBTS
),
named as (
  select kind, FINANCIAL_DISCLOSURE_ID, raw, {nm('raw')} n from src where nullif(trim(raw),'') is not null
),
ok as (
  select * from named
  where regexp_count(n, ' ') >= 1 and length(n) >= 8
    and (regexp_count(n, ' ') >= 2 or split_part(n,' ',1) not in {GENERIC_FIRST})
    and split_part(n,' ',1) not in ('MR','MRS','MS','DR','JUDGE','HON','ESTATE','TRUST','STATE','UNIVERSITY','COLLEGE','SCHOOL','LAW','FEDERAL','AMERICAN','NATIONAL','US','U','UNITED','DEPARTMENT','DEPT','BANK','FIRST','INTERNAL','INTERNATIONAL')
),
fd as (
  select ID, PERSON_ID, try_to_number(YEAR) yr from {L}FED_COURTLISTENER_FINANCIAL_DISCLOSURES
  where try_to_number(YEAR) between 1990 and 2030 and nullif(PERSON_ID,'') is not null
  qualify row_number() over (partition by ID order by DATE_MODIFIED desc) = 1
),
pairs as (select distinct ok.kind, fd.PERSON_ID, fd.yr, ok.n, ok.raw from ok join fd on fd.ID = ok.FINANCIAL_DISCLOSURE_ID)
"""
show(run(f"""with {SRC} select kind, count(*) rows_named, count(distinct n) names from named group by 1 union all select 'OK '||kind, count(*), count(distinct n) from ok group by 1""", "name_funnel"))
show(run(f"""with {SRC} select kind, count(*) pair_rows, count(distinct PERSON_ID) judges, count(distinct n) names from pairs group by 1""", "pairs"))
HITS = f"""
{SRC},
pj as (select distinct PERSON_ID from pairs),
dk as (
  select d.ID docket_id, d.ASSIGNED_TO_ID, d.COURT_ID, d.CASE_NAME, {nm('d.CASE_NAME')} cn, d.DOCKET_NUMBER, try_to_date(d.DATE_FILED) filed, try_to_date(d.DATE_TERMINATED) term
  from {L}FED_COURTLISTENER_DOCKETS d join pj on d.ASSIGNED_TO_ID = pj.PERSON_ID
  where nullif(d.CASE_NAME,'') is not null
),
hits as (
  select distinct p.kind, p.PERSON_ID, p.yr, p.n, p.raw, dk.docket_id, dk.COURT_ID, dk.CASE_NAME, dk.DOCKET_NUMBER, dk.filed, dk.term
  from dk join (select kind, PERSON_ID, yr, n, min(raw) raw from pairs group by 1,2,3,4) p
    on dk.ASSIGNED_TO_ID = p.PERSON_ID
   and regexp_like(dk.cn, '.*\\\\b' || p.n || '\\\\b.*')
   and dk.filed <= to_date(p.yr || '-12-31')
   and coalesce(dk.term, to_date('2100-01-01')) >= to_date(p.yr || '-01-01')
)
"""
show(run(f"""with {HITS} select kind, count(*) hit_rows, count(distinct docket_id) dockets, count(distinct PERSON_ID) judges, count(distinct n) names,
  count(distinct PERSON_ID||'|'||n) judge_name, min(yr) y0, max(yr) y1 from hits group by 1""", "hits"))
show(run(f"""with {HITS} select kind, n, count(distinct docket_id) dockets, count(distinct PERSON_ID) judges, min(CASE_NAME) example, min(raw) raw from hits group by 1,2 order by 3 desc limit 25""", "hits_by_name"), 25)
show(run(f"""with {HITS} select kind, PERSON_ID, yr, raw, COURT_ID, CASE_NAME, DOCKET_NUMBER, filed, term from hits where kind <> 'debt' order by random() limit 12""", "hits_sample_nondebt"), 12)
show(run(f"""with {HITS} select kind, PERSON_ID, yr, raw, COURT_ID, CASE_NAME, DOCKET_NUMBER, filed, term from hits where kind = 'debt' order by random() limit 8""", "hits_sample_debt"), 8)