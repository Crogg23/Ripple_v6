-- skeptic g4, 2026-09-24, Python door, tag skeptic-r2-2026-09-24. Each connection first ran the two ALTER SESSION lines (not counted).
-- S2.2 and first S3.2/S3.5 failed on compile; reruns follow.

-- ===== from q1.sql
-- [S4.1] column lists for the six tables
select table_name, listagg(column_name, ',') within group (order by ordinal_position) cols from LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS where table_name in ('FINANCE__FED_SENATE_EFD_PTR','POLITICS__FED_CONGRESS_LEGISLATORS','FINANCE__FED_PCAOB_FORM_AP_FILINGS','POLITICS__TX_LOBBY_COVER','POLITICS__TX_LOBBY_TRANSPORTATION','POLITICS__TX_LOBBY_INDIVIDUAL_REPORTING') group by 1;

-- ===== from q4.sql
-- [S4.2] Armstrong in the legislators table: term start decides whether March 2026 trades belong on a PTR
select BIOGUIDE, NAME_FIRST, NAME_LAST, NAME_OFFICIAL_FULL, STATE, PARTY, TERM_TYPE, TERM_START, TERM_END, N_TERMS, LEGISLATOR_SET from LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_LEGISLATORS where upper(NAME_LAST) like '%ARMSTRONG%' or upper(NAME_LAST) like 'MULLIN%';
-- [S4.3] Armstrong filings in EFD: every filing, kind, amendment flag, filed date, lines, trade date range, owner mix
select FILING_ID, SENATOR, FILING_KIND, IS_AMENDMENT, left(FILED_DATE::string,19) filed, count(*) lines, min(TRANSACTION_DATE) td_min, max(TRANSACTION_DATE) td_max, count(distinct TRANSACTION_DATE) n_dates, listagg(distinct OWNER,'|') owners, count(distinct TICKER) tickers, count(distinct PTR_LINK) links, max(left(COMMENT,200)) cmt from LIBRARY_MARTS.FINANCE.FINANCE__FED_SENATE_EFD_PTR where FILER_LAST_CLEAN='ARMSTRONG' or SENATOR ilike '%armstrong%' group by 1,2,3,4,5 order by filed;
-- [S4.4] raw date strings on Armstrong lines: are TRANSACTION_DATE and FILED_DATE parsed right (MM/DD vs DD/MM)?
select TRANSACTION_DATE::string td_raw, try_to_date(TRANSACTION_DATE::string) td, FILED_DATE::string fd_raw, count(*) n, listagg(distinct TRANSACTION_TYPE,'|') types, listagg(distinct OWNER,'|') owners from LIBRARY_MARTS.FINANCE.FINANCE__FED_SENATE_EFD_PTR where FILER_LAST_CLEAN='ARMSTRONG' group by 1,2,3 order by 2;
-- [S4.5] duplicate lines inside the Armstrong filing: same date+ticker+type+amount repeated
select count(*) lines, count(distinct TRANSACTION_DATE||'|'||coalesce(TICKER,'')||'|'||coalesce(ASSET_DESCRIPTION,'')||'|'||TRANSACTION_TYPE||'|'||AMOUNT_RANGE||'|'||OWNER) distinct_lines, count(distinct LINE_NO) line_nos, count(distinct AMOUNT_RANGE) ranges, mode(AMOUNT_RANGE) top_range, count_if(AMOUNT_RANGE ilike '$1,001 - $15,000%') smallest_bucket from LIBRARY_MARTS.FINANCE.FINANCE__FED_SENATE_EFD_PTR where FILER_LAST_CLEAN='ARMSTRONG';
-- [S4.6] every senator who files lines with the same FILED_DATE shape: is FILED_DATE a real date on other new senators' first PTRs (Husted, Moody sworn in Jan 2025)?
select FILER_LAST_CLEAN, min(try_to_date(left(FILED_DATE::string,10))) first_filed, min(try_to_date(TRANSACTION_DATE::string)) first_trade, count(*) lines from LIBRARY_MARTS.FINANCE.FINANCE__FED_SENATE_EFD_PTR where FILER_LAST_CLEAN in ('HUSTED','MOODY','ARMSTRONG','SHEEHY','MCCORMICK','JUSTICE','BANKS','CURTIS') group by 1 order by 2;

-- ===== from q4b.sql
-- [S4.7] Armstrong full filing comment, and any Armstrong rows in the combined SENATE_TRADES table from another source or filing
select 'efd' src, max(COMMENT) cmt, null n from LIBRARY_MARTS.FINANCE.FINANCE__FED_SENATE_EFD_PTR where FILER_LAST_CLEAN='ARMSTRONG' and COMMENT is not null
union all
select SOURCE_ID, max(FILED_DATE::string)||' / '||min(FILED_DATE::string), count(*) from LIBRARY_MARTS.FINANCE.FINANCE__SENATE_TRADES where SENATOR_NAME ilike '%armstrong%' group by 1;
-- [S4.8] Armstrong value by line: lower and upper bound sums, March lines only, and the smallest-bucket share
select count(*) lines, sum(try_to_number(regexp_replace(split_part(AMOUNT_RANGE,'-',1),'[^0-9]',''))) lo, sum(try_to_number(regexp_replace(split_part(AMOUNT_RANGE,'-',2),'[^0-9]',''))) hi, count_if(datediff('day', try_to_date(TRANSACTION_DATE::string), try_to_date(left(FILED_DATE::string,10))) between 112 and 119) late_112_119 from LIBRARY_MARTS.FINANCE.FINANCE__FED_SENATE_EFD_PTR where FILER_LAST_CLEAN='ARMSTRONG' and TRANSACTION_DATE::string like '2026-03%';

-- ===== from q3.sql
-- [S3.1] PCAOB report types: rows, newest-version rows, rows carrying a fund series
select AUDIT_REPORT_TYPE, count(*) n, count_if(LATEST_FORM_AP_FILING::string='1') latest, count_if(AUDIT_FUND_SERIES is not null and AUDIT_FUND_SERIES::string not in ('','[]')) fund_series_rows, count(distinct ENGAGEMENT_PARTNER_ID) partners from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS group by 1 order by 2 desc;
-- [S3.2] Borgers partner 0504100001 by audit-report year: newest rows, distinct issuer ids, distinct CIKs, distinct names, no-CIK rows, fund-series rows, issuers with 2+ reports in the year
with b as (select year(try_to_date(AUDIT_REPORT_DATE::string)) yr, ISSUER_ID, ISSUER_CIK, ISSUER_NAME, ISSUER_CIK_NONE, AUDIT_FUND_SERIES, AUDIT_REPORT_TYPE from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS where ENGAGEMENT_PARTNER_ID::string='0504100001' and LATEST_FORM_AP_FILING::string='1')
select yr, count(*) rows_, count(distinct ISSUER_ID) issuers, count(distinct ISSUER_CIK) ciks, count(distinct upper(ISSUER_NAME)) names, count_if(ISSUER_CIK is null) no_cik, count_if(AUDIT_FUND_SERIES is not null and AUDIT_FUND_SERIES::string not in ('','[]')) fund_rows, listagg(distinct AUDIT_REPORT_TYPE,'|') types,
 (select count(*) from (select ISSUER_ID from b b2 where b2.yr=b.yr group by 1 having count(*)>1)) multi_report_issuers
from b group by yr order by yr;
-- [S3.3] Peer check, same filter as the claim: partner-year issuer counts, 2019-2023, median / p90 / p99 / max, and rank of the Borgers id
with a as (select ENGAGEMENT_PARTNER_ID::string pid, year(try_to_date(AUDIT_REPORT_DATE::string)) yr, count(distinct ISSUER_ID) n from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS where AUDIT_REPORT_TYPE ilike 'Issuer, other%' and LATEST_FORM_AP_FILING::string='1' and ENGAGEMENT_PARTNER_ID is not null group by 1,2)
select yr, count(*) partner_years, median(n) med, percentile_cont(0.9) within group (order by n) p90, percentile_cont(0.99) within group (order by n) p99, max(n) mx, max_by(pid,n) top_pid, max(iff(pid='0504100001',n,null)) borgers, count_if(n>=50) n50plus from a where yr between 2017 and 2025 group by 1 order by 1;
-- [S3.4] Is the partner ID one person? names and firms carried by 0504100001, and other IDs used at the Borgers firm
select ENGAGEMENT_PARTNER_ID::string pid, FIRM_ID, max(FIRM_NAME) firm, listagg(distinct ENGAGEMENT_PARTNER_FIRST_NAME||' '||ENGAGEMENT_PARTNER_LAST_NAME,' | ') names, count(*) n from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS where FIRM_NAME ilike '%borgers%' or ENGAGEMENT_PARTNER_ID::string='0504100001' group by 1,2 order by n desc;
-- [S3.5] Borgers 2023 issuers: sample 25 names, and share whose name reads as a shell / SPAC / holding (Acquisition, Holdings, Capital, Inc only)
select count(distinct ISSUER_ID) issuers, count(distinct iff(ISSUER_NAME ilike '%acquisition%',ISSUER_ID,null)) acq_named, count(distinct iff(ISSUER_NAME ilike '%trust%' or ISSUER_NAME ilike '%fund%' or ISSUER_NAME ilike '%series%',ISSUER_ID,null)) trust_fund_named, left(listagg(distinct ISSUER_NAME,' ; '),1500) sample from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS where ENGAGEMENT_PARTNER_ID::string='0504100001' and LATEST_FORM_AP_FILING::string='1' and year(try_to_date(AUDIT_REPORT_DATE::string))=2023;

-- ===== from q3b.sql
-- [S3.2b] Borgers partner 0504100001, operating-company newest rows, by audit-report year: rows, issuer ids, CIKs, names, no-CIK rows, issuers with 2+ reports, rows NOT under a Borgers-spelled name
with b as (select year(try_to_date(AUDIT_REPORT_DATE::string)) yr, ISSUER_ID, ISSUER_CIK, ISSUER_NAME, ENGAGEMENT_PARTNER_FIRST_NAME||' '||ENGAGEMENT_PARTNER_LAST_NAME pn from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS where ENGAGEMENT_PARTNER_ID::string='0504100001' and LATEST_FORM_AP_FILING::string='1' and AUDIT_REPORT_TYPE ilike 'Issuer, other%'),
m as (select yr, count(*) k from (select yr, ISSUER_ID from b group by 1,2 having count(*)>1) group by 1)
select b.yr, count(*) rows_, count(distinct ISSUER_ID) issuers, count(distinct ISSUER_CIK) ciks, count(distinct upper(ISSUER_NAME)) names, count_if(ISSUER_CIK is null) no_cik, max(m.k) multi_report_issuers,
 count_if(not (pn ilike '%borg%' or pn ilike '%brger%' or pn ilike '%orgers%' or pn ilike '%brogers%')) other_person_rows, listagg(distinct iff(pn ilike '%borg%' or pn ilike '%brger%' or pn ilike '%orgers%' or pn ilike '%brogers%', null, pn),' | ') other_names
from b left join m on m.yr=b.yr group by b.yr order by b.yr;
-- [S3.5b] Borgers 2023 issuers: acquisition-named share, fund/trust-named share, a name sample
select count(distinct ISSUER_ID) issuers, count(distinct iff(ISSUER_NAME ilike '%acquisition%',ISSUER_ID,null)) acq_named, count(distinct iff(ISSUER_NAME ilike '%trust%' or ISSUER_NAME ilike '%fund%',ISSUER_ID,null)) trust_fund_named, left(listagg(distinct ISSUER_NAME,' ; '),1200) name_sample from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS where ENGAGEMENT_PARTNER_ID::string='0504100001' and LATEST_FORM_AP_FILING::string='1' and AUDIT_REPORT_TYPE ilike 'Issuer, other%' and year(try_to_date(AUDIT_REPORT_DATE::string))=2023;
-- [S3.6] The 2020 top partner 0068800121 (beat Borgers that year): who and which firm, by year
select year(try_to_date(AUDIT_REPORT_DATE::string)) yr, max(FIRM_NAME) firm, listagg(distinct ENGAGEMENT_PARTNER_FIRST_NAME||' '||ENGAGEMENT_PARTNER_LAST_NAME,' | ') names, count(distinct ISSUER_ID) issuers, count(distinct iff(ISSUER_NAME ilike '%acquisition%',ISSUER_ID,null)) acq_named from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS where ENGAGEMENT_PARTNER_ID::string='0068800121' and LATEST_FORM_AP_FILING::string='1' and AUDIT_REPORT_TYPE ilike 'Issuer, other%' group by 1 order by 1;

-- ===== from q1t.sql
-- [S1.1] Cover rows for the NY-trip report and every other 2026 report by the same filer: form type, period, filed date, transport and other totals
select c.REPORT_INFO_IDENT::string rid, c.FILER_IDENT, c.FILER_NAME, c.FORM_TYPE_CD, c.REPORT_TYPE_CD, c.APPLICABLE_YEAR, c.PERIOD_START_DT, c.PERIOD_END_DT, c.FILED_DT, c.TOTAL_EXPEND_TRANSPORTATION tran, c.TOTAL_EXPEND_FOOD food, c.TOTAL_EXPEND_ENTERTAINMENT ent, c.TOTAL_EXPEND_EVENT ev from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER c where c.FILER_IDENT in (select FILER_IDENT from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER where REPORT_INFO_IDENT::string='101046715') and c.APPLICABLE_YEAR::string >= '2025' order by c.FILED_DT;
-- [S1.2] Trip lines on report 101046715: lines, distinct TRAVEL_ID, distinct people, modes, and duplicate legs (same person+date+route)
select count(*) lines, count(distinct TRAVEL_ID) travel_ids, count(distinct ACTIVITY_ID) activity_ids, count(distinct upper(RECIPIENTNAMELAST||RECIPIENTNAMEFIRST)) people, listagg(distinct TRANSPORTATIONTYPECD,'|') modes, count(distinct upper(RECIPIENTNAMELAST||RECIPIENTNAMEFIRST)||DEPARTUREDT||DEPARTURECITY||ARRIVALCITY) distinct_legs, listagg(distinct RECIPIENTNAMEPREFIXCD||' '||RECIPIENTNAMEFIRST||' '||RECIPIENTNAMELAST||' ['||coalesce(RECIPIENTPERSENTTYPECD,'')||']',' ; ') who, listagg(distinct FORMTYPECD||'/'||REPORTTYPECD,'|') forms from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_TRANSPORTATION where REPORT_ID::string='101046715';
-- [S1.3] Client lines on report 101046715 (and duplicates)
select ONBEHALFNAME, ON_BEHALF_ID, count(*) n, max(ONBEHALFMAILINGCITY) city from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_INDIVIDUAL_REPORTING where REPORT_ID::string='101046715' group by 1,2;
-- [S1.4] Rank check with corrections: top 12 transport reports, form type, and whether the same filer has another report the same year+report type (original vs correction)
with c as (select REPORT_INFO_IDENT::string rid, FILER_IDENT, FILER_NAME, APPLICABLE_YEAR y, REPORT_TYPE_CD rt, FORM_TYPE_CD ft, FILED_DT, try_to_number(TOTAL_EXPEND_TRANSPORTATION,18,2) tran from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER),
s as (select FILER_IDENT, y, rt, count(*) same_period_reports, listagg(ft||':'||coalesce(tran,0)::string,' , ') versions from c group by 1,2,3)
select c.rid, c.FILER_NAME, c.y, c.rt, c.ft, c.FILED_DT, c.tran, s.same_period_reports, left(s.versions,200) versions, (select count(*) from c where tran>0) n_pos, (select median(tran) from c where tran>0) med from c join s using (FILER_IDENT, y, rt) where c.tran>0 qualify row_number() over (order by c.tran desc) <= 12 order by c.tran desc;
-- [S1.5] Transport rank after dedupe: keep one report per filer+year+report type (latest filed); where does 79,647.58 land and how many reports are left
with c as (select REPORT_INFO_IDENT::string rid, FILER_IDENT, APPLICABLE_YEAR y, REPORT_TYPE_CD rt, FILED_DT, try_to_number(TOTAL_EXPEND_TRANSPORTATION,18,2) tran from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER qualify row_number() over (partition by FILER_IDENT, APPLICABLE_YEAR, REPORT_TYPE_CD order by FILED_DT desc, REPORT_INFO_IDENT desc)=1)
select count_if(tran>0) n_pos, median(iff(tran>0,tran,null)) med, count_if(tran>79647.58) above_ny, max(iff(rid='101046715',1,0)) ny_kept from c;

-- ===== from q1u.sql
-- [S1.6] NY-trip legs per person: title, entity type, legs, dates, routes, lodging, purpose text (does everyone actually fly?)
select coalesce(RECIPIENTNAMEPREFIXCD,'-') pfx, RECIPIENTNAMEFIRST||' '||RECIPIENTNAMELAST who, count(*) legs, listagg(DEPARTURECITY||'>'||ARRIVALCITY||' '||DEPARTUREDT::string,' ; ') within group (order by DEPARTUREDT) route, max(LODGINGNAME) lodging, max(left(TRAVELPURPOSE,90)) purpose, max(left(TRANSPORTATIONTYPEDESCR,60)) descr from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_TRANSPORTATION where REPORT_ID::string='101046715' group by 1,2 order by 1,2;
-- [S1.7] Do the other 2026 lobbyists for Success Academy or Kleinheinz report the same trip (same travelers, March 30-31)? Any transport line naming these 8 people in 2026 on another report
select REPORT_ID::string rid, FILERNAME, FORMTYPECD, REPORTTYPECD, count(*) legs, listagg(distinct RECIPIENTNAMELAST,'|') who, min(DEPARTUREDT) d0 from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_TRANSPORTATION where APPLICABLEYEAR::string='2026' and upper(RECIPIENTNAMELAST) in ('PAXTON','BUCKLEY','FAIRLY','LEACH','DUKE','DIEM','SALVATO','HARRINGTON') group by 1,2,3,4 order by 1;

-- ===== from q2.sql
-- [S2.1] Abboud: every report with media > 0: form type, report type, period, filed date, media amount; flags periods filed twice
with a as (select REPORT_INFO_IDENT::string rid, FILER_IDENT, FILER_NAME, FORM_TYPE_CD ft, REPORT_TYPE_CD rt, APPLICABLE_YEAR y, PERIOD_START_DT ps, PERIOD_END_DT pe, FILED_DT, try_to_number(TOTAL_EXPEND_MEDIA,18,2) media from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER where FILER_NAME ilike 'Abboud%')
select rid, ft, rt, y, ps, pe, FILED_DT, media, count(*) over (partition by FILER_IDENT, y, rt) same_period, count(*) over (partition by FILER_IDENT, ps) same_start from a where media > 0 order by ps, rid;
-- [S2.2] Abboud media: raw sum, sum after keeping one report per filer+year+report type, sum after one per period start; count of distinct amounts; round-thousand amounts
with a as (select REPORT_INFO_IDENT rid, FILER_IDENT, APPLICABLE_YEAR y, REPORT_TYPE_CD rt, PERIOD_START_DT ps, FILED_DT, try_to_number(TOTAL_EXPEND_MEDIA,18,2) media from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER where FILER_NAME ilike 'Abboud%' and APPLICABLE_YEAR::string between '2021' and '2026')
select sum(media) raw_, (select sum(media) from a qualify row_number() over (partition by FILER_IDENT,y,rt order by FILED_DT desc, rid desc)=1) dedup_rt, (select sum(media) from a qualify row_number() over (partition by FILER_IDENT,ps order by FILED_DT desc, rid desc)=1) dedup_ps, count_if(media>0) n_pos, count(distinct media) n_amounts, count_if(media>0 and mod(media,1000)=0) round_thousand from a;
-- [S2.3] Denominator 2021-2026: all TX media dollars raw vs deduped (one per filer+year+report type), and the Abboud share both ways
with a as (select REPORT_INFO_IDENT rid, FILER_IDENT, FILER_NAME, APPLICABLE_YEAR y, REPORT_TYPE_CD rt, FILED_DT, try_to_number(TOTAL_EXPEND_MEDIA,18,2) media from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER where APPLICABLE_YEAR::string between '2021' and '2026'),
d as (select * from a qualify row_number() over (partition by FILER_IDENT,y,rt order by FILED_DT desc, rid desc)=1)
select 'raw' v, sum(media) total, sum(iff(FILER_NAME ilike 'Abboud%',media,0)) abboud, round(100*abboud/total,1) pct from a
union all select 'dedup', sum(media), sum(iff(FILER_NAME ilike 'Abboud%',media,0)), round(100*sum(iff(FILER_NAME ilike 'Abboud%',media,0))/sum(media),1) from d;
-- [S2.4] Do other Sands lobbyists' reports carry media too (would double-count the same ad buy)? media>0 reports 2021-26 whose client lines name Sands, by filer
select c.FILER_NAME, count(distinct c.REPORT_INFO_IDENT) reports, sum(try_to_number(c.TOTAL_EXPEND_MEDIA,18,2)) media from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER c where c.APPLICABLE_YEAR::string between '2021' and '2026' and try_to_number(c.TOTAL_EXPEND_MEDIA,18,2)>0 and c.REPORT_INFO_IDENT::string in (select REPORT_ID::string from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_INDIVIDUAL_REPORTING where ONBEHALFNAME ilike '%sands%') group by 1 order by 3 desc;
-- [S2.5] Sands lobbyist roster size 2021-26 (how many registrants list Sands as a client) and how many report any media
select count(distinct r.FILER_ID) sands_lobbyists, count(distinct iff(try_to_number(c.TOTAL_EXPEND_MEDIA,18,2)>0, r.FILER_ID, null)) with_media from LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_INDIVIDUAL_REPORTING r left join LIBRARY_MARTS.POLITICS.POLITICS__TX_LOBBY_COVER c on c.REPORT_INFO_IDENT::string = r.REPORT_ID::string where r.ONBEHALFNAME ilike '%sands%' and r.APPLICABLEYEAR::string between '2021' and '2026';

-- ===== from q5.sql
-- [S3.7] Borgers 2023-24 operating clients: how many have any newer Form AP (any firm incl. Borgers) after 2024-05-03, and how many from a different firm; plus how many were already gone before (last AP dated 2023)
with b as (select ISSUER_ID, max(try_to_date(AUDIT_REPORT_DATE::string)) last_borgers from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS where FIRM_ID::string='5041' and AUDIT_REPORT_TYPE ilike 'Issuer, other%' and LATEST_FORM_AP_FILING::string='1' and year(try_to_date(AUDIT_REPORT_DATE::string)) in (2023,2024) group by 1),
n as (select ISSUER_ID, min(try_to_date(AUDIT_REPORT_DATE::string)) first_new from LIBRARY_MARTS.FINANCE.FINANCE__FED_PCAOB_FORM_AP_FILINGS where FIRM_ID::string<>'5041' and AUDIT_REPORT_TYPE ilike 'Issuer, other%' and try_to_date(AUDIT_REPORT_DATE::string) >= '2024-01-01' group by 1)
select count(*) borgers_clients, count(n.ISSUER_ID) moved, count(*)-count(n.ISSUER_ID) no_new_ap, count_if(n.first_new < '2024-05-03') moved_before_bar from b left join n using (ISSUER_ID);
-- [S1.8/S2.6] Other Texas political tables that could carry the next join
select table_schema, table_name, row_count from LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES where table_name ilike '%TX%' and (table_name ilike '%CAMPAIGN%' or table_name ilike '%CONTRIB%' or table_name ilike '%LOBBY%' or table_name ilike '%TEC%' or table_name ilike '%EXPEND%') order by 2;
