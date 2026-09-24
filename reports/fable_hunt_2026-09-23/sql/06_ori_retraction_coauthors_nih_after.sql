with nih as (
  select APPL_ID, FISCAL_YEAR, ORG_NAME, PROJECT_TITLE, AWARD_AMOUNT, AWARD_NOTICE_DATE, trim(p.value::string) pi, trim(split_part(PI_PROFILE_IDS, ';', p.index)) profile_id
  from LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_NIH_REPORTER, lateral split_to_table(PI_NAMES, ';') p
  where FISCAL_YEAR between 2010 and 2026 and PI_PROFILE_IDS is not null),
nihn as (
  select *, upper(regexp_substr(regexp_replace(pi,'\\s*\\(contact\\)',''), '[A-Za-z\\-]+$')) last_nm, upper(split_part(pi,' ',1)) first_nm from nih where array_size(split(pi,' ')) >= 2 and profile_id <> ''),
namekey as (
  select last_nm, first_nm, count(distinct profile_id) profiles from nihn where length(first_nm) >= 3 and length(last_nm) >= 4 group by 1,2),
rw as (
  select RECORD_ID, RETRACTION_DATE, ORIGINAL_PAPER_DATE, JOURNAL, REASONS, INSTITUTIONS, trim(a.value::string) author
  from LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_RETRACTION_WATCH, lateral split_to_table(AUTHORS, ';') a
  where COUNTRIES ilike '%united states%' and RETRACTION_DATE between '2010-01-01' and '2025-12-31' and REASONS ilike '%Investigation by ORI%'),
rwn as (
  select *, upper(regexp_substr(author, '[A-Za-z\\-]+$')) last_nm, upper(split_part(author,' ',1)) first_nm from rw where array_size(split(author,' ')) >= 2)
select rwn.author, nihn.profile_id, count(distinct rwn.RECORD_ID) ori_retractions, min(rwn.RETRACTION_DATE) first_retraction, max(rwn.RETRACTION_DATE) last_retraction,
  count(distinct iff(nihn.AWARD_NOTICE_DATE > rwn.RETRACTION_DATE, nihn.APPL_ID, null)) nih_awards_after, round(sum(iff(nihn.AWARD_NOTICE_DATE > rwn.RETRACTION_DATE, nihn.AWARD_AMOUNT, 0))/1e6,2) nih_usd_after_m,
  count(distinct iff(nihn.AWARD_NOTICE_DATE <= rwn.RETRACTION_DATE, nihn.APPL_ID, null)) nih_awards_before,
  max(iff(nihn.AWARD_NOTICE_DATE > rwn.RETRACTION_DATE, nihn.ORG_NAME, null)) org_after, max(rwn.INSTITUTIONS) rw_institution, max(rwn.REASONS) reasons
from rwn join namekey nk on nk.last_nm = rwn.last_nm and nk.first_nm = rwn.first_nm and nk.profiles = 1
join nihn on nihn.last_nm = rwn.last_nm and nihn.first_nm = rwn.first_nm
group by 1,2 having nih_usd_after_m > 0 order by nih_usd_after_m desc limit 40;
with nih as (
  select APPL_ID, AWARD_AMOUNT, AWARD_NOTICE_DATE, trim(p.value::string) pi, trim(split_part(PI_PROFILE_IDS, ';', p.index)) profile_id
  from LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_NIH_REPORTER, lateral split_to_table(PI_NAMES, ';') p
  where FISCAL_YEAR between 2010 and 2026 and PI_PROFILE_IDS is not null),
nihn as (select *, upper(regexp_substr(regexp_replace(pi,'\\s*\\(contact\\)',''), '[A-Za-z\\-]+$')) last_nm, upper(split_part(pi,' ',1)) first_nm from nih where array_size(split(pi,' ')) >= 2 and profile_id <> ''),
namekey as (select last_nm, first_nm, count(distinct profile_id) profiles from nihn where length(first_nm) >= 3 and length(last_nm) >= 4 group by 1,2),
rw as (
  select RECORD_ID, RETRACTION_DATE, trim(a.value::string) author
  from LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_RETRACTION_WATCH, lateral split_to_table(AUTHORS, ';') a
  where COUNTRIES ilike '%united states%' and RETRACTION_DATE between '2010-01-01' and '2025-12-31' and REASONS ilike '%Investigation by ORI%'),
rwn as (select distinct upper(regexp_substr(author, '[A-Za-z\\-]+$')) last_nm, upper(split_part(author,' ',1)) first_nm, author from rw where array_size(split(author,' ')) >= 2),
m as (
  select rwn.author, nihn.profile_id, sum(iff(nihn.AWARD_NOTICE_DATE > (select min(RETRACTION_DATE) from rw r2 where r2.author = rwn.author), nihn.AWARD_AMOUNT, 0)) usd_after
  from rwn join namekey nk on nk.last_nm = rwn.last_nm and nk.first_nm = rwn.first_nm and nk.profiles = 1
  join nihn on nihn.last_nm = rwn.last_nm and nihn.first_nm = rwn.first_nm group by 1,2)
select (select count(distinct author) from rwn) ori_authors, count(*) matched_unique_pi, sum(iff(usd_after>0,1,0)) with_money_after, round(sum(usd_after)/1e6,1) usd_after_m from m
