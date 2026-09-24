-- deep-15: coverage round 2, hand queries, 2026-09-24
-- Tables: POLITICS__IRS527_DIRECTORS_OFFICERS, POLITICS__TX_LOBBY_COVER, POLITICS__TX_LOBBY_ENTERTAINMENT,
--         POLITICS__TX_LOBBY_FOOD_BEVERAGE, POLITICS__TX_LOBBY_TRANSPORTATION
-- Join partners touched: FINANCE__FED_IRS527_SCHEDULE_B_EXPENDITURES, POLITICS__IRS527_8871_ORGS,
--         POLITICS__TX_LOBBY_INDIVIDUAL_REPORTING (client lines)
-- Door: Python (connect/db.py). Every connection opened with:
--   ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
--   ALTER SESSION SET QUERY_TAG = 'coverage-r2-2026-09-24';
-- Read-only. 34 statements, numbered in the order run. [25] failed to compile (bad column name) and was rerun as [26].

-- [1] IRS527 D&O: size, distinct EINs, forms, names, addresses, titles
select count(*) n, count(distinct EIN) eins, count(distinct FORM_ID_NUMBER) forms,
 count(distinct upper(trim(ENTITY_NAME))) names, count(distinct upper(trim(ENTITY_ADDR1))) addrs,
 count_if(nullif(trim(ENTITY_NAME),'') is null) blank_name, count(distinct ENTITY_TITLE) titles,
 count(distinct _SOURCE_RUN_ID) runs
from LIBRARY_MARTS.POLITICS.POLITICS__IRS527_DIRECTORS_OFFICERS;

-- [2] IRS527 D&O: sample 5
select * from LIBRARY_MARTS.POLITICS.POLITICS__IRS527_DIRECTORS_OFFICERS limit 5;

-- [3] IRS527 D&O: top officer names by distinct EIN (name = upper, letters/spaces only), with their top address and title
with p as (
 select regexp_replace(upper(trim(ENTITY_NAME)),'[^A-Z ]','') nm0, EIN, upper(trim(ENTITY_ADDR1)) a1, upper(trim(ENTITY_TITLE)) t, upper(trim(ENTITY_CITY)) city, ENTITY_STATE st
 from LIBRARY_MARTS.POLITICS.POLITICS__IRS527_DIRECTORS_OFFICERS
), q as (select regexp_replace(nm0,' +',' ') nm, * exclude nm0 from p where length(nm0)>3)
select nm, count(distinct EIN) eins, count(*) rows_, count(distinct a1) addrs, mode(a1) top_addr, mode(city) city, mode(st) st, mode(t) top_title
from q group by nm order by eins desc limit 40;

-- [4] IRS527 D&O: top addresses by distinct EIN and distinct officer names
select upper(trim(ENTITY_ADDR1)) a1, mode(upper(trim(ENTITY_CITY))) city, mode(ENTITY_STATE) st, count(distinct EIN) eins, count(distinct upper(trim(ENTITY_NAME))) people, count(*) rows_, mode(upper(trim(ENTITY_NAME))) top_person
from LIBRARY_MARTS.POLITICS.POLITICS__IRS527_DIRECTORS_OFFICERS
where nullif(trim(ENTITY_ADDR1),'') is not null
group by 1 order by eins desc limit 30;

-- [5] find the other IRS 527 tables (Schedule A / B, 8871 header)
select table_schema, table_name, row_count from LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES where table_name ilike '%527%' order by 2;

-- [6] IRS527 join: top-12 officer addresses -> Schedule B spending (deduped on EIN+date+recipient+amount), land rate vs all 527s
with cl as (
 select upper(trim(ENTITY_ADDR1)) a1, lpad(trim(EIN),9,'0') ein
 from LIBRARY_MARTS.POLITICS.POLITICS__IRS527_DIRECTORS_OFFICERS
 where upper(trim(ENTITY_ADDR1)) in ('1103 HAYS STREET','527 EAST PARK AVENUE','455 CAPITOL MALL, SUITE 600','610 S. BOULEVARD','1787 TRIBUTE ROAD, SUITE K','1127 11TH STREET','1700 TRIBUTE ROAD, SUITE 201','POST OFFICE BOX 1701','5429 MADISON AVENUE','2350 KERNER BLVD., SUITE 250','8489 CABIN HILL ROAD','312 CLAY STREET, SUITE 300')
 group by 1,2
 union all
 select '_ALL 527s IN D&O', lpad(trim(EIN),9,'0') from LIBRARY_MARTS.POLITICS.POLITICS__IRS527_DIRECTORS_OFFICERS group by 2
), b as (
 select ein, sum(EXPENDITURE_AMOUNT) amt, count(*) n, min(y) y0, max(y) y1 from (
  select distinct lpad(trim(EIN::string),9,'0') ein, EXPENDITURE_DATE, upper(trim(RECIPIENT_NAME)) r, EXPENDITURE_AMOUNT, year(EXPENDITURE_DATE) y
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS527_SCHEDULE_B_EXPENDITURES) group by 1
)
select a1, count(distinct cl.ein) eins, count(distinct b.ein) eins_in_schedb, round(100*count(distinct b.ein)/count(distinct cl.ein),1) land_pct,
 round(sum(b.amt)/1e6,1) schedb_musd, sum(b.n) lines, min(b.y0) y0, max(b.y1) y1
from cl left join b on b.ein = cl.ein group by 1 order by eins desc;

-- [7] IRS527: why the clusters miss Schedule B. Share that told the IRS they are exempt from 8872 (they report to a state), by cluster vs all; Fenner spellings merged
with d as (
 select lpad(trim(EIN),9,'0') ein, upper(trim(ENTITY_ADDR1)) a1, regexp_replace(upper(ENTITY_NAME),'[^A-Z]','') nm
 from LIBRARY_MARTS.POLITICS.POLITICS__IRS527_DIRECTORS_OFFICERS
), g as (
 select 'FENNER, NOREEN (any spelling)' grp, ein from d where nm like 'NOREEN%FENNER' group by 2
 union all select 'WATKINS, NANCY (any spelling)', ein from d where nm like 'NANCY%WATKINS' group by 2
 union all select a1, ein from d where a1 in ('1103 HAYS STREET','527 EAST PARK AVENUE','455 CAPITOL MALL, SUITE 600','610 S. BOULEVARD','1787 TRIBUTE ROAD, SUITE K') group by 1,2
 union all select '_ALL 527s IN D&O', ein from d group by 2
), o as (
 select lpad(trim(EIN),9,'0') ein, max(EXEMPT_8872_IND::string) ex, min(try_to_date(ESTABLISHED_DATE::string)) est, mode(MAILING_STATE) st
 from LIBRARY_MARTS.POLITICS.POLITICS__IRS527_8871_ORGS group by 1
)
select grp, count(distinct g.ein) eins, count(distinct o.ein) in_8871, listagg(distinct o.ex,'|') flag_vals,
 count_if(o.ex='1') exempt_8872, round(100*count_if(o.ex='1')/nullif(count(o.ein),0),1) exempt_pct,
 min(year(o.est)) est_min, median(year(o.est)) est_med, max(year(o.est)) est_max, mode(o.st) top_state
from g left join o on o.ein=g.ein group by grp order by eins desc;

-- [8] IRS527 Schedule B trap check: same payment (EIN+date+recipient+amount) repeated across filings (amended 8872s) vs inside one filing
with k as (
 select lpad(trim(EIN::string),9,'0') ein, EXPENDITURE_DATE d, upper(trim(RECIPIENT_NAME)) r, EXPENDITURE_AMOUNT a,
  count(*) n, count(distinct FORM_ID_NUMBER) forms, count(distinct SCHEDULE_ID) sids
 from LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS527_SCHEDULE_B_EXPENDITURES group by 1,2,3,4
)
select count(*) keys, sum(n) raw_rows, round(sum(a*n)/1e9,2) raw_busd, round(sum(a)/1e9,2) dedup_busd,
 count_if(forms>1) keys_in_2plus_filings, round(sum(iff(forms>1, a*(forms-1),0))/1e9,2) busd_repeated_across_filings,
 count_if(forms=1 and n>1) keys_repeated_in_one_filing, round(sum(iff(forms=1 and n>1, a*(n-1),0))/1e9,2) busd_repeated_in_one_filing,
 max(n) max_copies
from k;

-- [9] TX COVER: size, report ids, filers, load shape, years, category totals (text -> number)
select count(*) n, count(distinct REPORT_INFO_IDENT) reports, count(distinct FILER_IDENT) filers,
 count(distinct REPORT_INFO_IDENT||'~'||FILER_IDENT) report_filer_pairs, count(distinct _SOURCE_URL) urls, count(distinct _LOADED_AT) loads,
 min(APPLICABLE_YEAR) y0, max(APPLICABLE_YEAR) y1, listagg(distinct FORM_TYPE_CD,'|') forms,
 round(sum(try_to_number(TOTAL_EXPEND_FOOD,18,2))/1e6,2) food_m, round(sum(try_to_number(TOTAL_EXPEND_TRANSPORTATION,18,2))/1e6,2) tran_m,
 round(sum(try_to_number(TOTAL_EXPEND_ENTERTAINMENT,18,2))/1e6,2) ent_m, round(sum(try_to_number(TOTAL_EXPEND_GIFT,18,2))/1e6,2) gift_m,
 round(sum(try_to_number(TOTAL_EXPEND_AWARD,18,2))/1e6,2) award_m, round(sum(try_to_number(TOTAL_EXPEND_EVENT,18,2))/1e6,2) event_m, round(sum(try_to_number(TOTAL_EXPEND_MEDIA,18,2))/1e6,2) media_m,
 count_if(try_to_number(TOTAL_EXPEND_FOOD,18,2)>0) food_nz, count_if(TOTAL_EXPEND_FOOD is not null and try_to_number(TOTAL_EXPEND_FOOD,18,2) is null) food_unparsed
from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER;

-- [10] TX COVER: sample 5
select * from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER limit 5;

-- [11] TX COVER: why does one REPORT_INFO_IDENT hold ~1K rows? top 5 ids: filers, years, periods, distinct totals
select REPORT_INFO_IDENT, count(*) n, count(distinct FILER_IDENT) filers, count(distinct APPLICABLE_YEAR) years, min(APPLICABLE_YEAR) y0, max(APPLICABLE_YEAR) y1,
 count(distinct PERIOD_START_DT) periods, count(distinct FORM_TYPE_CD) forms, count(distinct TOTAL_EXPEND_FOOD) food_vals, count(distinct FILED_DT) filed_dts, mode(FILER_NAME) top_filer
from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER group by 1 order by n desc limit 8;

-- [12] TX COVER: by year, raw vs deduped (keep last-filed per filer+year+report type; corrections replace originals). Odd years = regular session
with r as (
 select REPORT_INFO_IDENT, FILER_IDENT, APPLICABLE_YEAR y, REPORT_TYPE_CD, FORM_TYPE_CD, FILED_DT,
  coalesce(try_to_number(TOTAL_EXPEND_FOOD,18,2),0) food, coalesce(try_to_number(TOTAL_EXPEND_MEDIA,18,2),0) media,
  coalesce(try_to_number(TOTAL_EXPEND_TRANSPORTATION,18,2),0)+coalesce(try_to_number(TOTAL_EXPEND_ENTERTAINMENT,18,2),0)+coalesce(try_to_number(TOTAL_EXPEND_GIFT,18,2),0)+coalesce(try_to_number(TOTAL_EXPEND_AWARD,18,2),0)+coalesce(try_to_number(TOTAL_EXPEND_EVENT,18,2),0) other
 from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER
), d as (select * from r qualify row_number() over (partition by FILER_IDENT, y, REPORT_TYPE_CD order by FILED_DT desc nulls last, REPORT_INFO_IDENT desc)=1)
select y, (select count(*) from r where r.y=d.y) raw_reports, count(*) dedup_reports, count(distinct FILER_IDENT) filers,
 round((select sum(food+media+other) from r where r.y=d.y)/1e6,2) raw_total_m, round(sum(food+media+other)/1e6,2) dedup_total_m,
 round(sum(food)/1e6,2) food_m, round(sum(media)/1e6,2) media_m, round(sum(other)/1e6,2) other_m, count_if(FORM_TYPE_CD='CORLOBBYACT') kept_corrections
from d group by y order by y;

-- [13] TX COVER: top filer-years by MEDIA spending (deduped), with each filer's share of that year's media total
with r as (
 select REPORT_INFO_IDENT, FILER_IDENT, FILER_NAME, APPLICABLE_YEAR y, REPORT_TYPE_CD, FILED_DT,
  coalesce(try_to_number(TOTAL_EXPEND_MEDIA,18,2),0) media, coalesce(try_to_number(TOTAL_EXPEND_FOOD,18,2),0) food
 from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER
 qualify row_number() over (partition by FILER_IDENT, APPLICABLE_YEAR, REPORT_TYPE_CD order by FILED_DT desc nulls last, REPORT_INFO_IDENT desc)=1
), fy as (
 select FILER_IDENT, max(FILER_NAME) nm, y, sum(media) media, sum(food) food, count(*) reports, max(media) max_one_report, count_if(media>0) media_reports
 from r group by 1,3
)
select y, nm, FILER_IDENT, round(media/1e6,2) media_m, round(100*media/sum(media) over (partition by y),1) pct_of_year_media, round(max_one_report/1e6,2) biggest_report_m, media_reports, reports, round(food) food
from fy qualify row_number() over (order by media desc) <= 25 order by media desc;

-- [14] TX COVER: top 15 filers by FOOD across all years (deduped), session-year (odd) vs off-year average
with r as (
 select FILER_IDENT, FILER_NAME, APPLICABLE_YEAR y, coalesce(try_to_number(TOTAL_EXPEND_FOOD,18,2),0) food
 from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER
 qualify row_number() over (partition by FILER_IDENT, APPLICABLE_YEAR, REPORT_TYPE_CD order by FILED_DT desc nulls last, REPORT_INFO_IDENT desc)=1
), fy as (select FILER_IDENT, max(FILER_NAME) nm, y, sum(food) food from r group by 1,3)
select FILER_IDENT, max(nm) nm, round(sum(food)) food_total, min(y) y0, max(y) y1, count_if(food>0) yrs_with_food, round(max(food)) peak_year_food, max_by(y, food) peak_year,
 round(avg(iff(mod(y,2)=1, food, null))) odd_yr_avg, round(avg(iff(mod(y,2)=0, food, null))) even_yr_avg
from fy group by 1 order by food_total desc limit 15;

-- [15] TX COVER join: the big media filers' reports -> client lines (INDIVIDUAL_REPORTING on REPORT_ID). Land rate and client names
with m as (
 select REPORT_INFO_IDENT::string rid, FILER_IDENT, FILER_NAME, APPLICABLE_YEAR y, REPORT_TYPE_CD, try_to_number(TOTAL_EXPEND_MEDIA,18,2) media
 from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER
 where FILER_IDENT in ('00085404','00061287','00033418','00012659','00014952','00015457','00013211') and try_to_number(TOTAL_EXPEND_MEDIA,18,2) > 0
), c as (
 select REPORT_ID::string rid, listagg(distinct upper(trim(ONBEHALFNAME)),' | ') clients
 from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_INDIVIDUAL_REPORTING group by 1
)
select m.FILER_NAME, count(*) media_reports, round(sum(media)/1e6,2) media_m, min(y) y0, max(y) y1, count(c.rid) reports_with_client_line,
 round(100*count(c.rid)/count(*),0) land_pct, left(listagg(distinct c.clients,' || '),220) clients, round(max(media)/1e6,2) biggest_m, max_by(REPORT_TYPE_CD||' '||y, media) biggest_rpt
from m left join c on c.rid=m.rid group by 1 order by media_m desc;

-- [16] TX detail tables: counts, recipient fill, amount fill (ENT, FOOD; TRAN has no amount column), years, filers, reports, corrected-form share
select 'ENT' t, count(*) n, count(distinct ACTIVITY_ID) acts, count(distinct REPORT_ID) reports, count(distinct FILER_ID) filers,
 count_if(nullif(trim(RECIPIENTNAMELAST),'') is not null) recip_named, count(distinct upper(trim(RECIPIENTNAMELAST))||','||upper(trim(RECIPIENTNAMEFIRST))) recips,
 count_if(ACTIVITYEXACTAMOUNT is not null) exact_filled, round(sum(ACTIVITYEXACTAMOUNT)) exact_sum, round(sum(ACTIVITYAMOUNTRANGELOW)) low_sum, round(sum(ACTIVITYAMOUNTRANGEHIGH)) high_sum,
 min(APPLICABLEYEAR) y0, max(APPLICABLEYEAR) y1, count_if(FORMTYPECD='CORLOBBYACT') corr, listagg(distinct RECIPIENTPERSENTTYPECD,'|') rtypes
from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_ENTERTAINMENT
union all
select 'FOOD', count(*), count(distinct ACTIVITY_ID), count(distinct REPORT_ID), count(distinct FILER_ID),
 count_if(nullif(trim(RECIPIENTNAMELAST),'') is not null), count(distinct upper(trim(RECIPIENTNAMELAST))||','||upper(trim(RECIPIENTNAMEFIRST))),
 count_if(ACTIVITYEXACTAMOUNT is not null), round(sum(ACTIVITYEXACTAMOUNT)), round(sum(ACTIVITYAMOUNTRANGELOW)), round(sum(ACTIVITYAMOUNTRANGEHIGH)),
 min(APPLICABLEYEAR), max(APPLICABLEYEAR), count_if(FORMTYPECD='CORLOBBYACT'), listagg(distinct RECIPIENTPERSENTTYPECD,'|')
from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_FOOD_BEVERAGE
union all
select 'TRAN', count(*), count(distinct TRAVEL_ID), count(distinct REPORT_ID), count(distinct FILER_ID),
 count_if(nullif(trim(RECIPIENTNAMELAST),'') is not null), count(distinct upper(trim(RECIPIENTNAMELAST))||','||upper(trim(RECIPIENTNAMEFIRST))),
 null, null, null, null, min(APPLICABLEYEAR), max(APPLICABLEYEAR), count_if(FORMTYPECD='CORLOBBYACT'), listagg(distinct RECIPIENTPERSENTTYPECD,'|')
from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_TRANSPORTATION;

-- [17] TX ENT: sample 5
select * from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_ENTERTAINMENT limit 5;

-- [18] TX ENT: top recipients (last,first) by exact-or-range-high; items, lobbyists, years, top venue, top lobbyist
with e as (
 select upper(trim(RECIPIENTNAMELAST))||', '||upper(trim(RECIPIENTNAMEFIRST)) who, upper(trim(RECIPIENTNAMEPREFIXCD)) pfx, FILERNAME, APPLICABLEYEAR y, upper(trim(ENTERTAINMENTNAME)) venue,
  coalesce(ACTIVITYEXACTAMOUNT, ACTIVITYAMOUNTRANGEHIGH) hi, coalesce(ACTIVITYEXACTAMOUNT, ACTIVITYAMOUNTRANGELOW) lo
 from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_ENTERTAINMENT
)
select who, mode(pfx) pfx, count(*) items, round(sum(lo)) low_sum, round(sum(hi)) high_sum, count(distinct FILERNAME) lobbyists, min(y) y0, max(y) y1, mode(venue) top_venue, mode(FILERNAME) top_lobbyist
from e group by who order by high_sum desc limit 15;

-- [19] TX FOOD: sample 5
select * from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_FOOD_BEVERAGE limit 5;

-- [20] TX FOOD: top 12 single rows by amount, with how many rows share the same report+date+restaurant (is it one dinner split across officials?)
select REPORT_ID, APPLICABLEYEAR y, FILERNAME, ACTIVITYDATE, ACTIVITYAMOUNTCD cd, ACTIVITYEXACTAMOUNT exact, ACTIVITYAMOUNTRANGELOW lo, ACTIVITYAMOUNTRANGEHIGH hi,
 RECIPIENTNAMEPREFIXCD pfx, RECIPIENTNAMEFIRST||' '||RECIPIENTNAMELAST who, RESTAURANTNAME, RESTAURANTSTREETCITY city,
 count(*) over (partition by REPORT_ID, ACTIVITYDATE, upper(RESTAURANTNAME)) same_meal_rows
from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_FOOD_BEVERAGE
qualify row_number() over (order by coalesce(ACTIVITYEXACTAMOUNT, ACTIVITYAMOUNTRANGEHIGH) desc nulls last) <= 12
order by coalesce(exact, hi) desc;

-- [21] TX FOOD: the $78.7K row's report-day in full, plus every row where the amount equals the restaurant ZIP (zip typed into the money field)
select 'report 604419 same day' what, ACTIVITYDATE, ACTIVITYAMOUNTCD cd, ACTIVITYEXACTAMOUNT exact, RECIPIENTNAMEFIRST||' '||RECIPIENTNAMELAST who, RESTAURANTNAME, RESTAURANTSTREETPOSTALCODE zip
from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_FOOD_BEVERAGE where REPORT_ID::string='604419' and ACTIVITYDATE='2014-01-26'
union all
select 'amount = zip', ACTIVITYDATE, ACTIVITYAMOUNTCD, ACTIVITYEXACTAMOUNT, RECIPIENTNAMEFIRST||' '||RECIPIENTNAMELAST, RESTAURANTNAME, RESTAURANTSTREETPOSTALCODE
from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_FOOD_BEVERAGE where ACTIVITYEXACTAMOUNT >= 10000 and try_to_number(left(trim(RESTAURANTSTREETPOSTALCODE),5)) = floor(ACTIVITYEXACTAMOUNT);

-- [22] TX FOOD: top officials by food (exact, else range low / range high); rows >= $10K dropped as events or typos; 2015+ split
with f as (
 select upper(trim(RECIPIENTNAMELAST))||', '||upper(trim(RECIPIENTNAMEFIRST)) who, upper(trim(RECIPIENTNAMEPREFIXCD)) pfx, FILERNAME, APPLICABLEYEAR::int y,
  coalesce(ACTIVITYEXACTAMOUNT, ACTIVITYAMOUNTRANGELOW) lo, coalesce(ACTIVITYEXACTAMOUNT, ACTIVITYAMOUNTRANGEHIGH) hi
 from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_FOOD_BEVERAGE where coalesce(ACTIVITYEXACTAMOUNT,0) < 10000
)
select who, mode(pfx) pfx, count(*) meals, round(sum(lo)) low_sum, round(sum(hi)) high_sum, round(sum(iff(y>=2015,hi,0))) high_2015on, count(distinct FILERNAME) lobbyists, min(y) y0, max(y) y1, mode(FILERNAME) top_lobbyist,
 round(median(hi)) med_hi
from f group by who order by high_sum desc limit 15;

-- [23] TX FOOD: meals paid by filers that are firms (LLC, INC, SECURITIES, CAPITAL, MANAGEMENT, PARTNERS, L.P., BANK, & CO) vs people; top recipients of firm-paid meals
with f as (
 select upper(trim(RECIPIENTNAMELAST))||', '||upper(trim(RECIPIENTNAMEFIRST)) who, FILERNAME, APPLICABLEYEAR::int y,
  coalesce(ACTIVITYEXACTAMOUNT, ACTIVITYAMOUNTRANGEHIGH) hi, coalesce(ACTIVITYEXACTAMOUNT, ACTIVITYAMOUNTRANGELOW) lo, upper(trim(RESTAURANTSTREETCITY)) city,
  regexp_like(upper(FILERNAME), '.*(LLC|L\.L\.C|INC\.?$|INC |SECURITIES|CAPITAL|MANAGEMENT|PARTNERS|L\.P\.|\bLP\b|BANK|& CO|ADVISORS|INVESTMENT).*') firm
 from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_FOOD_BEVERAGE where coalesce(ACTIVITYEXACTAMOUNT,0) < 10000
)
select who, count(*) meals, round(sum(lo)) low_sum, round(sum(hi)) high_sum, count(distinct FILERNAME) firms, min(y) y0, max(y) y1, mode(city) city,
 left(listagg(distinct FILERNAME, '; '), 200) firm_list,
 (select count_if(firm) from f) all_firm_rows, (select count(*) from f) all_rows, (select round(sum(iff(firm,hi,0))) from f) all_firm_high
from f where firm group by who order by high_sum desc limit 12;

-- [24] TX TRAN: sample 5
select REPORT_ID, APPLICABLEYEAR, FILERNAME, TRAVEL_ID, RECIPIENTNAMEPREFIXCD, RECIPIENTNAMEFIRST, RECIPIENTNAMELAST, LODGINGNAME, LODGINGSTREETCITY, LODGINGSTREETSTATECD, LODGINGSTREETCOUNTRYCD,
 CHECKINDT, CHECKOUTDT, TRANSPORTATIONTYPECD, TRANSPORTATIONTYPEDESCR, DEPARTURECITY, DEPARTUREDT, ARRIVALCITY, ARRIVALDT, TRAVELPURPOSE
from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_TRANSPORTATION limit 5;

-- [25] TX TRAN: top officials by trips (a trip = one report + one recipient + one purpose), with lines, private-air lines, foreign lodging, nights, top purpose, top lobbyist
with t as (
 select upper(trim(RECIPIENTNAMELAST))||', '||upper(trim(RECIPIENTNAMEFIRST)) who, upper(trim(RECIPIENTNAMEPREFIXCD)) pfx, REPORT_ID, FILERNAME, APPLICABLEYEAR::int y,
  upper(trim(TRAVELPURPOSE)) purpose, TRANSPORTATIONTYPECD tcd, LODGINGSTREETCOUNTRYCD ctry, LODGINGSTREETSTATECD st, datediff('day', try_to_date(CHECKINDT::string), try_to_date(CHECKOUTDT::string)) nights
 from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_TRANSPORTATION
)
select who, mode(pfx) pfx, count(*) lines, count(distinct REPORT_ID||'~'||coalesce(purpose,'')) trips, count_if(tcd='PRIVAIR') privair_lines,
 count_if(ctry is not null and ctry<>'USA') foreign_lodging, sum(iff(nights between 0 and 30, nights, 0)) nights, count(distinct FILERNAME) lobbyists, min(y) y0, max(y) y1,
 left(mode(purpose),50) top_purpose, mode(FILERNAME) top_lobbyist, (select listagg(distinct TRANSPORTATIONTYPECD,'|') from t) all_tcodes
from t group by who order by trips desc limit 15;

-- [26] TX TRAN (rerun, fixed column name): top officials by trips (report + recipient + purpose), lines, private-air lines, foreign lodging, nights, top purpose, top lobbyist
with t as (
 select upper(trim(RECIPIENTNAMELAST))||', '||upper(trim(RECIPIENTNAMEFIRST)) who, upper(trim(RECIPIENTNAMEPREFIXCD)) pfx, REPORT_ID, FILERNAME, APPLICABLEYEAR::int y,
  upper(trim(TRAVELPURPOSE)) purpose, TRANSPORTATIONTYPECD tcd, LODGINGSTREETCOUNTRYCD ctry, datediff('day', try_to_date(CHECKINDT::string), try_to_date(CHECKOUTDT::string)) nights
 from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_TRANSPORTATION
)
select who, mode(pfx) pfx, count(*) lines, count(distinct REPORT_ID||'~'||coalesce(purpose,'')) trips, count_if(tcd='PRIVAIR') privair_lines,
 count_if(ctry is not null and ctry<>'USA') foreign_lodging, sum(iff(nights between 0 and 30, nights, 0)) nights, count(distinct FILERNAME) lobbyists, min(y) y0, max(y) y1,
 left(mode(purpose),50) top_purpose, mode(FILERNAME) top_lobbyist, (select listagg(distinct tcd,'|') from t) all_tcodes, (select count_if(tcd='PRIVAIR') from t) all_privair, (select count_if(ctry<>'USA') from t) all_foreign
from t group by who order by trips desc limit 15;

-- [27] TX TRAN: every private-air line grouped by recipient and payer: lines, reports, years, routes, purposes
select upper(trim(RECIPIENTNAMEPREFIXCD)) pfx, RECIPIENTNAMEFIRST||' '||RECIPIENTNAMELAST who, FILERNAME, count(*) lines, count(distinct REPORT_ID) reports, min(APPLICABLEYEAR) y0, max(APPLICABLEYEAR) y1,
 count(distinct DEPARTUREDT) flight_days, left(listagg(distinct upper(trim(DEPARTURECITY))||'>'||upper(trim(ARRIVALCITY)), '; '), 160) routes,
 left(listagg(distinct upper(trim(TRAVELPURPOSE)), '; '), 260) purposes
from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_TRANSPORTATION where TRANSPORTATIONTYPECD='PRIVAIR'
group by 1,2,3 order by lines desc limit 20;

-- [28] TX TRAN join: private-air reports -> cover sheet transport dollars (REPORT_INFO_IDENT) and client lines (INDIVIDUAL_REPORTING). Land rates
with p as (
 select REPORT_ID::string rid, max(FILERNAME) filer, max(APPLICABLEYEAR) y, count(*) privair_lines, listagg(distinct RECIPIENTNAMELAST, ', ') within group (order by RECIPIENTNAMELAST) recips
 from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_TRANSPORTATION where TRANSPORTATIONTYPECD='PRIVAIR' group by 1
), cv as (
 select REPORT_INFO_IDENT::string rid, try_to_number(TOTAL_EXPEND_TRANSPORTATION,18,2) tran, try_to_number(TOTAL_EXPEND_FOOD,18,2) food, REPORT_TYPE_CD
 from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER
), cl as (
 select REPORT_ID::string rid, listagg(distinct upper(trim(ONBEHALFNAME)), ' | ') clients from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_INDIVIDUAL_REPORTING group by 1
)
select p.y, p.filer, p.rid, cv.REPORT_TYPE_CD, p.privair_lines, cv.tran report_transport_usd, left(cl.clients,120) clients, left(p.recips,120) recips
from p left join cv on cv.rid=p.rid left join cl on cl.rid=p.rid order by p.privair_lines desc, p.y desc limit 30;

-- [29] TX COVER peers: biggest single-report transportation totals ever, and where the 2026 Success Academy report ranks among reports with transport > 0
with c as (
 select REPORT_INFO_IDENT::string rid, FILER_NAME, APPLICABLE_YEAR y, REPORT_TYPE_CD, try_to_number(TOTAL_EXPEND_TRANSPORTATION,18,2) tran
 from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER where try_to_number(TOTAL_EXPEND_TRANSPORTATION,18,2) > 0
)
select rank() over (order by tran desc) rnk, y, FILER_NAME, rid, REPORT_TYPE_CD, tran, (select count(*) from c) reports_with_transport, (select median(tran) from c) median_transport
from c qualify rnk <= 12 or rid='101046715' order by rnk;

-- [30] TX TRAN: the 2026 Minnehan report line by line (who, mode, route, dates, lodging, purpose)
select RECIPIENTNAMEPREFIXCD pfx, RECIPIENTNAMEFIRST||' '||RECIPIENTNAMELAST who, TRANSPORTATIONTYPECD mode_, DEPARTURECITY||'>'||ARRIVALCITY route, DEPARTUREDT, ARRIVALDT, LODGINGNAME, CHECKINDT, CHECKOUTDT, TRAVELPURPOSE
from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_TRANSPORTATION where REPORT_ID::string='101046715' order by who, DEPARTUREDT;

-- [31] TX peers: what sits behind the #1 (2024 Bionat $156K) and #2 (2011 Mendelsohn $131K) transport reports: detail lines, recipients, modes, purposes, clients
with t as (
 select REPORT_ID::string rid, count(*) lines, count(distinct RECIPIENTNAMELAST||RECIPIENTNAMEFIRST) people, listagg(distinct TRANSPORTATIONTYPECD,'|') modes,
  left(listagg(distinct RECIPIENTNAMEPREFIXCD||' '||RECIPIENTNAMELAST, ', '),200) recips, left(listagg(distinct upper(TRAVELPURPOSE),'; '),160) purposes,
  left(listagg(distinct upper(LODGINGSTREETCITY)||' '||LODGINGSTREETCOUNTRYCD,'; '),100) lodging, min(DEPARTUREDT) d0, max(ARRIVALDT) d1
 from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_TRANSPORTATION where REPORT_ID::string in ('100949336','496959','461822','348382') group by 1
), cl as (select REPORT_ID::string rid, listagg(distinct upper(trim(ONBEHALFNAME)),' | ') clients from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_INDIVIDUAL_REPORTING where REPORT_ID::string in ('100949336','496959','461822','348382') group by 1)
select v.rid, t.lines, t.people, t.modes, t.d0, t.d1, t.lodging, cl.clients, t.recips, t.purposes
from (select column1 rid from values ('100949336'),('496959'),('461822'),('348382')) v left join t on t.rid=v.rid left join cl on cl.rid=v.rid;

-- [32] TX coverage, years lined up (2005-2026): cover-sheet category dollars vs what the itemized detail tables hold; and detail reports that land on a client line
with cv as (
 select sum(try_to_number(TOTAL_EXPEND_FOOD,18,2)) food, sum(try_to_number(TOTAL_EXPEND_ENTERTAINMENT,18,2)) ent, sum(try_to_number(TOTAL_EXPEND_TRANSPORTATION,18,2)) tran
 from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER where APPLICABLE_YEAR between 2005 and 2026
), cl as (select distinct REPORT_ID::string rid from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_INDIVIDUAL_REPORTING),
d as (
 select 'FOOD' t, REPORT_ID::string rid, coalesce(ACTIVITYEXACTAMOUNT, ACTIVITYAMOUNTRANGELOW) lo, coalesce(ACTIVITYEXACTAMOUNT, ACTIVITYAMOUNTRANGEHIGH) hi from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_FOOD_BEVERAGE where APPLICABLEYEAR::int between 2005 and 2026 and REPORT_ID::string <> '604419'
 union all select 'ENT', REPORT_ID::string, coalesce(ACTIVITYEXACTAMOUNT, ACTIVITYAMOUNTRANGELOW), coalesce(ACTIVITYEXACTAMOUNT, ACTIVITYAMOUNTRANGEHIGH) from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_ENTERTAINMENT where APPLICABLEYEAR::int between 2005 and 2026
 union all select 'TRAN', REPORT_ID::string, null, null from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_TRANSPORTATION where APPLICABLEYEAR::int between 2005 and 2026
)
select d.t, count(*) rows_, round(sum(lo)) detail_low, round(sum(hi)) detail_high,
 round(max(iff(d.t='FOOD',cv.food,iff(d.t='ENT',cv.ent,cv.tran)))) cover_usd,
 round(100*sum(hi)/max(iff(d.t='FOOD',cv.food,iff(d.t='ENT',cv.ent,cv.tran))),1) detail_high_pct_of_cover,
 count(distinct d.rid) reports, count(distinct cl.rid) reports_with_client_line, round(100*count(distinct cl.rid)/count(distinct d.rid),1) client_land_pct
from d cross join cv left join cl on cl.rid=d.rid group by d.t order by 1;

-- [33] TX COVER: the #1 transport report (2024 Bionat, $156,254) in full, plus its client lines
select c.FILER_NAME, c.FILER_IDENT, c.REPORT_TYPE_CD, c.FORM_TYPE_CD, c.PERIOD_START_DT, c.PERIOD_END_DT, c.TOTAL_EXPEND_TRANSPORTATION, c.TOTAL_EXPEND_FOOD, c.TOTAL_EXPEND_ENTERTAINMENT, c.TOTAL_EXPEND_GIFT, c.TOTAL_EXPEND_EVENT, c.TOTAL_EXPEND_MEDIA,
 (select listagg(distinct upper(trim(ONBEHALFNAME)),' | ') from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_INDIVIDUAL_REPORTING i where i.REPORT_ID::string='100949336') clients
from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER c where c.REPORT_INFO_IDENT::string='100949336';

-- [34] TX COVER second-field check on Sands: every 2021-2026 report with media > 0, by filer, with its clients; is Sands money reported by more than one lobbyist?
with m as (
 select REPORT_INFO_IDENT::string rid, FILER_NAME, APPLICABLE_YEAR y, try_to_number(TOTAL_EXPEND_MEDIA,18,2) media
 from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER where APPLICABLE_YEAR between 2021 and 2026 and try_to_number(TOTAL_EXPEND_MEDIA,18,2) > 0
), cl as (select REPORT_ID::string rid, listagg(distinct upper(trim(ONBEHALFNAME)),' | ') clients from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_INDIVIDUAL_REPORTING group by 1)
select m.FILER_NAME, count(*) reports, round(sum(media)) media_usd, round(sum(iff(y=2025,media,0))) media_2025, round(sum(iff(y=2023,media,0))) media_2023, min(y) y0, max(y) y1,
 count(cl.rid) with_client, left(listagg(distinct cl.clients,' || '),150) clients, (select round(sum(media)) from m) all_media_2021_26
from m left join cl on cl.rid=m.rid group by 1 order by media_usd desc limit 10;
