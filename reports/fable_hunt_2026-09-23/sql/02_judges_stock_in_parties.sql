with cos as (
  select * from values
   ('pfizer','pfizer inc'),('exxon','exxon'),('wells fargo','wells fargo'),('johnson & johnson','johnson & johnson'),('bank of america','bank of america'),
   ('jpmorgan','jpmorgan'),('walmart','wal-mart'),('walmart','walmart'),('amazon','amazon.com'),('microsoft','microsoft corp'),('apple','apple inc'),
   ('boeing','boeing co'),('chevron','chevron'),('citigroup','citigroup'),('citigroup','citibank'),('home depot','home depot'),('verizon','verizon'),
   ('at&t','at&t'),('comcast','comcast'),('general electric','general electric'),('ford motor','ford motor'),('general motors','general motors'),
   ('merck','merck & co'),('merck','merck sharp'),('abbvie','abbvie'),('bristol','bristol-myers'),('eli lilly','eli lilly'),('unitedhealth','unitedhealth'),('cvs','cvs pharmacy'),('cvs','cvs health'),
   ('walgreen','walgreen'),('procter','procter & gamble'),('coca-cola','coca-cola co'),('pepsico','pepsico'),('goldman sachs','goldman sachs'),('morgan stanley','morgan stanley'),
   ('honeywell','honeywell'),('lockheed','lockheed martin'),('raytheon','raytheon'),('caterpillar','caterpillar inc'),('intel','intel corp'),
   ('cisco','cisco systems'),('oracle','oracle corp'),('oracle','oracle america'),('nvidia','nvidia'),('tesla','tesla, inc'),('tesla','tesla motors'),('facebook','facebook, inc'),('google','google llc'),('google','google inc'),('netflix','netflix'),
   ('starbucks','starbucks corp'),('mcdonald','mcdonald''s corp'),('nike','nike, inc'),('target','target corp'),('costco','costco wholesale'),('fedex','fedex corp'),('united parcel','united parcel'),
   ('union pacific','union pacific'),('csx','csx transportation'),('norfolk southern','norfolk southern'),('duke energy','duke energy'),('dominion','dominion energy'),
   ('altria','altria'),('philip morris','philip morris'),('anheuser','anheuser-busch'),('kraft','kraft heinz'),('medtronic','medtronic'),
   ('abbott','abbott laboratories'),('amgen','amgen inc'),('gilead','gilead sciences'),('humana','humana inc'),('anthem','anthem, inc'),('cigna','cigna'),
   ('aetna','aetna'),('allstate','allstate'),('travelers','travelers'),('prudential','prudential insurance'),('metlife','metlife'),('aflac','aflac'),
   ('capital one','capital one'),('american express','american express'),('discover','discover bank'),('mastercard','mastercard'),('paypal','paypal'),
   ('u.s. bancorp','u.s. bank'),('pnc','pnc bank'),('truist','truist'),('bb&t','bb&t'),('suntrust','suntrust'),('fifth third','fifth third'),('keycorp','keybank'),
   ('regions','regions bank'),('huntington','huntington national bank'),('synchrony','synchrony'),('santander','santander'),('hsbc','hsbc'),('barclays','barclays'),('deutsche','deutsche bank'),
   ('halliburton','halliburton'),('schlumberger','schlumberger'),('conocophillips','conocophillips'),('occidental','occidental petroleum'),('marathon','marathon oil'),('marathon','marathon petroleum'),('valero','valero'),
   ('phillips 66','phillips 66'),('kinder morgan','kinder morgan'),('dupont','dupont'),('dow','dow chemical'),('monsanto','monsanto'),('bayer','bayer'),
   ('deere','deere & co'),('emerson','emerson electric'),('danaher','danaher'),('thermo fisher','thermo fisher'),('stryker','stryker corp'),
   ('zimmer','zimmer biomet'),('zimmer','zimmer, inc'),('boston scientific','boston scientific'),('baxter','baxter international'),('baxter','baxter healthcare'),('becton','becton dickinson'),('hca','hca health'),('tenet','tenet health'),
   ('davita','davita'),('fresenius','fresenius'),('mckesson','mckesson'),('cardinal health','cardinal health'),('amerisourcebergen','amerisourcebergen'),('teva','teva pharmaceutical'),
   ('mylan','mylan'),('endo','endo pharmaceuticals'),('mallinckrodt','mallinckrodt'),('allergan','allergan'),('celgene','celgene'),('biogen','biogen'),
   ('uber','uber technologies'),('lyft','lyft, inc'),('twitter','twitter, inc'),('salesforce','salesforce'),('adobe','adobe'),('ibm','international business machines'),
   ('hewlett','hewlett'),('dell','dell inc'),('dell','dell technologies'),('qualcomm','qualcomm'),('broadcom','broadcom'),('micron','micron technology'),('texas instruments','texas instruments'),('amd','advanced micro devices'),
   ('delta air','delta air'),('american airlines','american airlines'),('united airlines','united airlines'),('southwest','southwest airlines'),
   ('marriott','marriott'),('hilton','hilton'),('carnival','carnival corp'),('royal caribbean','royal caribbean'),('disney','walt disney'),
   ('viacom','viacom'),('cbs','cbs corp'),('fox','fox corp'),('news corp','news corp'),('charter','charter communications'),
   ('t-mobile','t-mobile'),('sprint','sprint corp'),('centurylink','centurylink'),('dish','dish network'),('sirius','sirius xm')
  as t(inv_pat, case_pat)),
inv as (
  select distinct d.PERSON_ID, d.YEAR_COL yr, c.inv_pat co, i.DESCRIPTION,
    case when i.TRANSACTION_DURING_REPORTING_PERIOD ilike 'sold%' and i.TRANSACTION_DURING_REPORTING_PERIOD not ilike '%part%' or i.TRANSACTION_DURING_REPORTING_PERIOD ilike 'redeem%' then coalesce(i.TRANSACTION_DATE, to_date(d.YEAR_COL||'-01-01')) else to_date((d.YEAR_COL+1)||'-12-31') end hold_end
  from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_INVESTMENTS i
  join LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_FINANCIAL_DISCLOSURES d on d.ID=i.FINANCIAL_DISCLOSURE_ID
  join cos c on regexp_like(i.DESCRIPTION, '.*\\b'||c.inv_pat||'\\b.*', 'i')
  where d.PERSON_ID is not null and d.YEAR_COL between 2010 and 2020
    and regexp_like(i.DESCRIPTION, '.*(common|stock|shares|\\bshs\\b|\\bcom\\b|\\bcl a\\b|\\bcl b\\b|\\([A-Z]{2,5}\\)).*', 'i')
    and not regexp_like(i.DESCRIPTION, '.*(fund|advantage|advisors|acct|account|checking|saving|cash|deposit|money market|mortgage|etf|index|\\bira\\b|401|brokerage|bond|\\bnote|\\bcd\\b|certificate|annuity|trust|pension|preferred|\\bpfd\\b|\\btr\\b|\\bval\\b|\\bcap\\b|stable|header|hasbro|\\bfd\\b|\\badv\\b|cking|\\bmtg\\b|\\bln\\b|depo|ultra short|\\bcre\\b|\\bcd\\b|savings|jen).*', 'i')),
holders as (select distinct PERSON_ID from inv),
dk0 as (
  select k.ASSIGNED_TO_ID, year(k.DATE_FILED) yr, k.ID docket_id, k.CASE_NAME, k.COURT_ID, k.DATE_FILED, k.NATURE_OF_SUIT, k.DOCKET_NUMBER
  from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS k
  join holders h on h.PERSON_ID = k.ASSIGNED_TO_ID
  where k.DATE_FILED between '2010-01-01' and '2021-12-31' and k.CASE_NAME ilike '% v. %' and k.CASE_NAME not ilike '%account%' and k.CASE_NAME not ilike 'united states v.%' and k.MDL_STATUS is null and k.ASSIGNED_TO_STR not ilike '%mdl%'),
dk as (select dk0.*, c.inv_pat co from dk0 join cos c on dk0.CASE_NAME ilike '%'||c.case_pat||'%'),
hits as (
  select inv.PERSON_ID, inv.co, dk.docket_id, dk.CASE_NAME, dk.COURT_ID, dk.DATE_FILED, dk.NATURE_OF_SUIT, dk.DOCKET_NUMBER, inv.yr disc_yr, inv.DESCRIPTION
  from inv join dk on dk.ASSIGNED_TO_ID = inv.PERSON_ID and dk.co = inv.co and dk.yr between inv.yr and inv.yr + 1 and dk.DATE_FILED < inv.hold_end)
select j.NAME_FIRST, j.NAME_LAST, hits.co, count(distinct hits.docket_id) cases, min(hits.DATE_FILED) first_case, max(hits.DATE_FILED) last_case, count(distinct hits.disc_yr) yrs_held, listagg(distinct hits.COURT_ID, ',') courts,
  any_value(hits.CASE_NAME) example_case, any_value(hits.DESCRIPTION) example_holding
from hits join LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_JUDGES j on j.ID = hits.PERSON_ID
group by 1,2,3 order by cases desc limit 80;
with cos as (
  select * from values
   ('pfizer','pfizer inc'),('exxon','exxon'),('wells fargo','wells fargo'),('johnson & johnson','johnson & johnson'),('bank of america','bank of america'),
   ('jpmorgan','jpmorgan'),('walmart','wal-mart'),('walmart','walmart'),('amazon','amazon.com'),('microsoft','microsoft corp'),('apple','apple inc'),
   ('boeing','boeing co'),('chevron','chevron'),('citigroup','citigroup'),('citigroup','citibank'),('home depot','home depot'),('verizon','verizon'),
   ('at&t','at&t'),('comcast','comcast'),('general electric','general electric'),('ford motor','ford motor'),('general motors','general motors'),
   ('merck','merck & co'),('merck','merck sharp'),('abbvie','abbvie'),('bristol','bristol-myers'),('eli lilly','eli lilly'),('unitedhealth','unitedhealth'),('cvs','cvs pharmacy'),('cvs','cvs health'),
   ('walgreen','walgreen'),('procter','procter & gamble'),('coca-cola','coca-cola co'),('pepsico','pepsico'),('goldman sachs','goldman sachs'),('morgan stanley','morgan stanley'),
   ('honeywell','honeywell'),('lockheed','lockheed martin'),('raytheon','raytheon'),('caterpillar','caterpillar inc'),('intel','intel corp'),
   ('cisco','cisco systems'),('oracle','oracle corp'),('oracle','oracle america'),('nvidia','nvidia'),('tesla','tesla, inc'),('tesla','tesla motors'),('facebook','facebook, inc'),('google','google llc'),('google','google inc'),('netflix','netflix'),
   ('starbucks','starbucks corp'),('mcdonald','mcdonald''s corp'),('nike','nike, inc'),('target','target corp'),('costco','costco wholesale'),('fedex','fedex corp'),('united parcel','united parcel'),
   ('union pacific','union pacific'),('csx','csx transportation'),('norfolk southern','norfolk southern'),('duke energy','duke energy'),('dominion','dominion energy'),
   ('altria','altria'),('philip morris','philip morris'),('anheuser','anheuser-busch'),('kraft','kraft heinz'),('medtronic','medtronic'),
   ('abbott','abbott laboratories'),('amgen','amgen inc'),('gilead','gilead sciences'),('humana','humana inc'),('anthem','anthem, inc'),('cigna','cigna'),
   ('aetna','aetna'),('allstate','allstate'),('travelers','travelers'),('prudential','prudential insurance'),('metlife','metlife'),('aflac','aflac'),
   ('capital one','capital one'),('american express','american express'),('discover','discover bank'),('mastercard','mastercard'),('paypal','paypal'),
   ('u.s. bancorp','u.s. bank'),('pnc','pnc bank'),('truist','truist'),('bb&t','bb&t'),('suntrust','suntrust'),('fifth third','fifth third'),('keycorp','keybank'),
   ('regions','regions bank'),('huntington','huntington national bank'),('synchrony','synchrony'),('santander','santander'),('hsbc','hsbc'),('barclays','barclays'),('deutsche','deutsche bank'),
   ('halliburton','halliburton'),('schlumberger','schlumberger'),('conocophillips','conocophillips'),('occidental','occidental petroleum'),('marathon','marathon oil'),('marathon','marathon petroleum'),('valero','valero'),
   ('phillips 66','phillips 66'),('kinder morgan','kinder morgan'),('dupont','dupont'),('dow','dow chemical'),('monsanto','monsanto'),('bayer','bayer'),
   ('deere','deere & co'),('emerson','emerson electric'),('danaher','danaher'),('thermo fisher','thermo fisher'),('stryker','stryker corp'),
   ('zimmer','zimmer biomet'),('zimmer','zimmer, inc'),('boston scientific','boston scientific'),('baxter','baxter international'),('baxter','baxter healthcare'),('becton','becton dickinson'),('hca','hca health'),('tenet','tenet health'),
   ('davita','davita'),('fresenius','fresenius'),('mckesson','mckesson'),('cardinal health','cardinal health'),('amerisourcebergen','amerisourcebergen'),('teva','teva pharmaceutical'),
   ('mylan','mylan'),('endo','endo pharmaceuticals'),('mallinckrodt','mallinckrodt'),('allergan','allergan'),('celgene','celgene'),('biogen','biogen'),
   ('uber','uber technologies'),('lyft','lyft, inc'),('twitter','twitter, inc'),('salesforce','salesforce'),('adobe','adobe'),('ibm','international business machines'),
   ('hewlett','hewlett'),('dell','dell inc'),('dell','dell technologies'),('qualcomm','qualcomm'),('broadcom','broadcom'),('micron','micron technology'),('texas instruments','texas instruments'),('amd','advanced micro devices'),
   ('delta air','delta air'),('american airlines','american airlines'),('united airlines','united airlines'),('southwest','southwest airlines'),
   ('marriott','marriott'),('hilton','hilton'),('carnival','carnival corp'),('royal caribbean','royal caribbean'),('disney','walt disney'),
   ('viacom','viacom'),('cbs','cbs corp'),('fox','fox corp'),('news corp','news corp'),('charter','charter communications'),
   ('t-mobile','t-mobile'),('sprint','sprint corp'),('centurylink','centurylink'),('dish','dish network'),('sirius','sirius xm')
  as t(inv_pat, case_pat)),
inv as (
  select distinct d.PERSON_ID, d.YEAR_COL yr, c.inv_pat co, i.DESCRIPTION,
    case when i.TRANSACTION_DURING_REPORTING_PERIOD ilike 'sold%' and i.TRANSACTION_DURING_REPORTING_PERIOD not ilike '%part%' or i.TRANSACTION_DURING_REPORTING_PERIOD ilike 'redeem%' then coalesce(i.TRANSACTION_DATE, to_date(d.YEAR_COL||'-01-01')) else to_date((d.YEAR_COL+1)||'-12-31') end hold_end
  from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_INVESTMENTS i
  join LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_FINANCIAL_DISCLOSURES d on d.ID=i.FINANCIAL_DISCLOSURE_ID
  join cos c on regexp_like(i.DESCRIPTION, '.*\\b'||c.inv_pat||'\\b.*', 'i')
  where d.PERSON_ID is not null and d.YEAR_COL between 2010 and 2020
    and regexp_like(i.DESCRIPTION, '.*(common|stock|shares|\\bshs\\b|\\bcom\\b|\\bcl a\\b|\\bcl b\\b|\\([A-Z]{2,5}\\)).*', 'i')
    and not regexp_like(i.DESCRIPTION, '.*(fund|advantage|advisors|acct|account|checking|saving|cash|deposit|money market|mortgage|etf|index|\\bira\\b|401|brokerage|bond|\\bnote|\\bcd\\b|certificate|annuity|trust|pension|preferred|\\bpfd\\b|\\btr\\b|\\bval\\b|\\bcap\\b|stable|header|hasbro|\\bfd\\b|\\badv\\b|cking|\\bmtg\\b|\\bln\\b|depo|ultra short|\\bcre\\b|\\bcd\\b|savings|jen).*', 'i')),
holders as (select distinct PERSON_ID from inv),
dk0 as (
  select k.ASSIGNED_TO_ID, year(k.DATE_FILED) yr, k.ID docket_id, k.CASE_NAME, k.COURT_ID, k.DATE_FILED
  from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS k
  join holders h on h.PERSON_ID = k.ASSIGNED_TO_ID
  where k.DATE_FILED between '2010-01-01' and '2021-12-31' and k.CASE_NAME ilike '% v. %' and k.CASE_NAME not ilike '%account%' and k.CASE_NAME not ilike 'united states v.%' and k.MDL_STATUS is null and k.ASSIGNED_TO_STR not ilike '%mdl%'),
dk as (select dk0.*, c.inv_pat co from dk0 join cos c on dk0.CASE_NAME ilike '%'||c.case_pat||'%'),
hits as (
  select distinct inv.PERSON_ID, inv.co, dk.docket_id
  from inv join dk on dk.ASSIGNED_TO_ID = inv.PERSON_ID and dk.co = inv.co and dk.yr between inv.yr and inv.yr + 1 and dk.DATE_FILED < inv.hold_end)
select count(distinct PERSON_ID) judges, count(distinct docket_id) cases, count(distinct co) companies from hits
