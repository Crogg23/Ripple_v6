-- g54 deep pass 3, 2026-09-24. Every statement run, in order. Python door (connect/db.py). Read-only.
-- Tables: JUSTICE__XC_OWID_NUCLEAR_WARHEADS, JUSTICE__FED_JPML_PENDING_MDLS, ECONOMICS__FED_IRS_EO_PR,
--   ECONOMICS__FED_IRS_SOI_CHARITIES, ECONOMICS__INTL_IT_ISTAT (all LIBRARY_MARTS).
-- Join partners read: FJC_IDB_CIVIL, CORPORATE_REGISTRY__FED_IRS_EO_BMF, FED_IRS_BMF, FED_IRS_990_EFILE_INDEX,
--   FED_IRS_AUTO_REVOCATIONS, SEC_13F_FILERS, SEC_13F_HOLDINGS, FED_FAC_SINGLE_AUDIT.
-- Count: 19 SELECT/WITH statements + 8 session-setup statements (4 connections x 2) = 27 of 35.
-- Raw results: g54/out_<label>.json


-- ===== connection: a.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- [a1_nuke_all] (0.4s)
select entity, code, year, number_of_nuclear_warheads
from LIBRARY_MARTS.JUSTICE.JUSTICE__XC_OWID_NUCLEAR_WARHEADS
order by entity, year;

-- [a2_jpml_all] (0.3s)
select *
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_JPML_PENDING_MDLS;

-- [a3_eopr_all] (1.0s)
select *
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_EO_PR;

-- [a4_soi_all] (0.8s)
select *
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_SOI_CHARITIES;

-- [a5_istat_flows] (1.0s)
select dataflow_id, freq, count(*) n, count(distinct series_key) series,
  count(distinct series_key, date) series_dates, min(date) d0, max(date) d1,
  count(distinct date) dates, count_if(is_missing_value) missing, count_if(obs_value is null) null_val,
  count_if(obs_status is not null and obs_status <> '') status_set, listagg(distinct obs_status, ',') statuses,
  count(distinct country) countries, any_value(country) a_country, count(distinct _source_run_id) runs,
  count(distinct istat_obs_id) ids, count_if(unit_mult is not null) unit_mult_set,
  count_if(unit_measure is not null and unit_measure <> '') unit_set, count_if(is_normal_value) normal_true,
  count_if(obs_value_absolute <> abs(obs_value)) abs_mismatch, count_if(obs_value < 0) negatives,
  any_value(dimension_keys) sample_dims, any_value(series_key) sample_series
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_IT_ISTAT
group by 1, 2
order by n desc;

-- [a6_istat_years] (0.5s)
select dataflow_id, obs_year, count(*) n, count(distinct series_key) series, count(distinct date) dates,
  min(date) d0, max(date) d1, round(median(obs_value), 2) med_val
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_IT_ISTAT
group by 1, 2
order by 1, 2;

-- [a7_fjc_mdl_probe] (2.0s)
select count(*) n, count_if(mdl_docket is not null and trim(mdl_docket) <> '') mdl_set,
  count(distinct mdl_docket) mdl_vals, count(distinct case_record_id) ids,
  count(distinct district, office, docket, file_date) case_keys,
  min(file_date) f0, max(file_date) f1, max(tape_year) max_tape, min(tape_year) min_tape,
  count(distinct tape_year) tapes,
  (select listagg(v || ':' || c, ' | ') from (select mdl_docket v, count(*) c from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CIVIL
     where mdl_docket is not null and trim(mdl_docket) <> '' group by 1 order by 2 desc limit 25)) top_mdl,
  (select listagg(l || ':' || c, ' | ') from (select length(mdl_docket) l, count(*) c from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CIVIL
     where mdl_docket is not null group by 1 order by 1)) mdl_lengths,
  (select listagg(t || ':' || c, ' | ') from (select tape_year t, count(*) c from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CIVIL
     group by 1 order by 1 desc limit 8)) tapes_top
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CIVIL;

-- [a8_bmf_pr_presence] (1.2s)
select 'ECON_BMF' src, count(*) n, count_if(state = 'PR') pr_rows, count(distinct ein) eins,
  max(try_to_number(tax_period)) max_tax_period, max(ruling_date) max_ruling, count(distinct _source_url) urls,
  listagg(distinct _source_url, ' ; ') within group (order by _source_url) url_list
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_BMF
union all
select 'CR_EO_BMF', count(*), count_if(state = 'PR'), count(distinct ein),
  max(try_to_number(tax_period_yyyymm)), max(ruling_yyyymm), count(distinct _source_run_id), null
from LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF;

-- ===== connection: b.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- [b1_mdl_fjc] (0.9s)
with c as (
  select try_to_number(mdl_docket) mdl, district, office, docket,
    min(file_date) fd, max(term_date) td, max(tape_year) ty, count(*) n
  from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CIVIL
  where mdl_docket is not null and mdl_docket <> '-8'
  group by 1, 2, 3, 4),
f as (
  select mdl, count(*) cases, sum(n) fjc_rows, count_if(td is null) open_cases, count_if(ty = '2099') ty2099,
    count_if(td is null and ty = '2099') open_2099, count_if(td is not null and ty = '2099') closed_2099,
    count_if(td is null and fd < '2021-04-01') open_5y, count_if(td is null and fd < '2016-04-01') open_10y,
    min(fd) first_file, max(fd) last_file,
    median(iff(td is null, datediff('day', fd, '2026-03-31'), null)) med_open_days,
    count(distinct district) dists
  from c group by 1)
select j.mdl_no, j.district, j.judge, left(j.litigation, 80) lit, j.pending_cases, j.total_cases, f.*
from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_JPML_PENDING_MDLS j
left join f on f.mdl = try_to_number(j.mdl_no)
order by try_to_number(j.mdl_no);

-- [b2_ein_land] (1.3s)
select 'EO_PR' src, count(*) n, count(b.ein) in_cr_bmf, count(e.ein) in_econ_bmf,
  count_if(b.state = 'PR') cr_state_pr, count_if(b.state is null or b.state = '') cr_state_blank,
  count_if(b.asset_amt = try_to_number(nullif(p.asset_amt, ''))) same_assets,
  count_if(b.ruling_yyyymm = p.ruling) same_ruling,
  count_if(b.tax_period_yyyymm > nullif(p.tax_period, '')) cr_newer_tax,
  count_if(b.org_name = p.name) same_name
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_EO_PR p
left join LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF b on b.ein = lpad(p.ein, 9, '0')
left join LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_BMF e on lpad(e.ein, 9, '0') = lpad(p.ein, 9, '0')
union all
select 'SOI', count(*), count(b.ein), count(e.ein),
  count_if(b.state = 'PR'), count_if(b.state is null or b.state = ''),
  count_if(b.asset_amt = s.asset_amt), count_if(b.ruling_yyyymm = s.ruling),
  count_if(try_to_number(b.tax_period_yyyymm) > s.tax_period), count_if(b.org_name = s.name)
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_SOI_CHARITIES s
left join LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF b on b.ein = lpad(s.ein, 9, '0')
left join LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_BMF e on lpad(e.ein, 9, '0') = lpad(s.ein, 9, '0')
union all
select 'CR_BMF_PR_not_in_EO_PR', count(*), null, null, null, null, null, null, null, null
from LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF
where state = 'PR' and ein not in (select lpad(ein, 9, '0') from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_EO_PR)
union all
select 'CR_BMF_state_blank', count(*), count_if(ein like '98%'), null, null, null, null, null, null, null
from LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF
where state is null or state = '';

-- [b3_c4_top] (1.0s)
select b.ein, b.org_name, b.city, b.state, b.ruling_yyyymm, b.subsection_code, b.classification_code, b.foundation_code,
  b.filing_req_code, b.asset_amt, b.revenue_amt, b.ntee_code,
  iff(s.ein is not null and s.state is null, 'FOREIGN', 'US') loc
from LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF b
left join LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_SOI_CHARITIES s on lpad(s.ein, 9, '0') = b.ein
where b.subsection_code = '04'
qualify row_number() over (order by b.asset_amt desc nulls last) <= 30
order by b.asset_amt desc;

-- [b4_bigorg_eras] (0.5s)
with base as (
  select b.ein, b.subsection_code sub, b.foundation_code fnd, b.asset_amt a, year(b.ruling_date) ry,
    iff(s.ein is not null and s.state is null, 'FOREIGN', 'US') loc
  from LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF b
  left join LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_SOI_CHARITIES s on lpad(s.ein, 9, '0') = b.ein
  where b.asset_amt >= 100000000)
select loc, case when sub = '04' then 'c4' when sub = '03' and fnd in ('02','03','04') then 'c3_private_fdn'
                 when sub = '03' then 'c3_public' else 'other' end kind,
  count(*) n, round(sum(a) / 1e9, 1) assets_b, count_if(a >= 1e9) n_1b,
  count_if(ry < 2000) r_pre2000, count_if(ry between 2000 and 2009) r_2000s, count_if(ry between 2010 and 2018) r_2010_18,
  count_if(ry >= 2019) r_2019p, round(sum(iff(ry >= 2019, a, 0)) / 1e9, 1) assets_2019p_b
from base group by 1, 2 order by 1, 2;

-- [b5_efile_foreign_big] (0.6s)
select s.ein, left(s.name, 45) name, s.city country, s.subsection, s.ruling, s.asset_amt,
  i.return_type, count(i.ein) filings, min(i.tax_period) first_tp, max(i.tax_period) last_tp, max(i.sub_date) last_sub
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_SOI_CHARITIES s
left join LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_990_EFILE_INDEX i on lpad(i.ein, 9, '0') = lpad(s.ein, 9, '0')
where s.state is null and s.asset_amt >= 1000000000
group by 1, 2, 3, 4, 5, 6, 7
order by s.asset_amt desc, 7;

-- [b6_revocations_by_state] (1.2s)
with r as (
  select upper(trim(state)) st, count(*) rev_all, count(distinct ein) rev_eins,
    count_if(year(revocation_date) between 2010 and 2011) rev_2010_11,
    count_if(year(revocation_date) between 2012 and 2018) rev_2012_18,
    count_if(year(revocation_date) >= 2019) rev_2019p,
    count_if(reinstatement_date is not null) reinst, max(revocation_date) last_rev
  from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_AUTO_REVOCATIONS group by 1),
b as (
  select state st, count(*) cur, count_if(subsection_code = '03') cur_c3
  from LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF group by 1)
select coalesce(r.st, b.st) st, b.cur, b.cur_c3, r.rev_all, r.rev_eins, r.rev_2010_11, r.rev_2012_18, r.rev_2019p, r.reinst, r.last_rev
from r full outer join b on r.st = b.st
order by b.cur desc nulls last;

-- [b7_state_ruling_eras] (0.2s)
select state, iff(foundation_code in ('02','03','04'), 'PF', 'other') k, count(*) cur,
  count_if(ruling_date between '2005-01-01' and '2011-12-31') r0511,
  count_if(ruling_date between '2012-01-01' and '2018-12-31') r1218,
  count_if(ruling_date between '2019-01-01' and '2025-12-31') r1925,
  count_if(ruling_date between '2019-01-01' and '2025-12-31' and asset_amt >= 1000000) r1925_1m,
  round(sum(iff(ruling_date >= '2012-01-01', asset_amt, 0))) assets_new
from LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF
group by 1, 2
order by 1, 2;

-- ===== connection: c.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- [c1_c4_shares] (0.9s)
with base as (
  select b.ein, b.subsection_code sub, b.foundation_code fnd, coalesce(b.asset_amt, 0) a,
    iff(s.ein is not null and s.state is null, 'FOREIGN', 'US') loc
  from LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF b
  left join LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_SOI_CHARITIES s on lpad(s.ein, 9, '0') = b.ein)
select loc, case when sub = '04' then 'c4' when sub = '03' and fnd in ('02','03','04') then 'c3_private_fdn'
                 when sub = '03' then 'c3_public' else 'other' end kind,
  count(*) n, round(sum(a) / 1e9, 1) assets_b, count_if(a >= 1e8) n_100m,
  round(median(iff(a >= 1e8, a, null)) / 1e6, 0) median_100m_plus_musd,
  round(sum(iff(a >= 1e8, a, 0)) / 1e9, 1) assets_100m_plus_b
from base group by 1, 2 order by 1, 2;

-- [c2_13f_foreign_c4] (1.6s)
with f as (
  select accession_number, filingmanager_name, filingmanager_city, filingmanager_stateorcountry,
    reportcalendarorquarter, try_to_date(reportcalendarorquarter, 'DD-MON-YYYY') q, isamendment
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_FILERS
  where filingmanager_name ilike any ('%novo holdings%', '%mastercard foundation%', '%novo nordisk fond%', '%realdania%',
    '%arab fund%', '%federation internationale de football%', '%international olympic%', '%cassa di risparmio di firenze%',
    '%university of queensland%', '%duck pond%', '%vendome foundation%', '%natasha foundation%', '%makivik%'))
select f.filingmanager_name, f.filingmanager_city, f.filingmanager_stateorcountry, f.reportcalendarorquarter, f.q, f.isamendment,
  f.accession_number, count(h.accession_number) positions, round(sum(h.value_usd)) value_usd,
  max_by(h.nameofissuer, h.value_usd) top_issuer, round(max(h.value_usd)) top_value
from f
left join LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_HOLDINGS h on h.accession_number = f.accession_number
group by 1, 2, 3, 4, 5, 6, 7
order by 1, 5 desc;

-- [c3_fac_pr_movers] (0.9s)
select lpad(regexp_replace(auditee_ein, '[^0-9]', ''), 9, '0') ein, audit_year, left(auditee_name, 40) name, auditee_city, auditee_state,
  left(auditee_address_line_1, 35) addr, total_amount_expended
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FAC_SINGLE_AUDIT
where lpad(regexp_replace(auditee_ein, '[^0-9]', ''), 9, '0') in
  ('650216638', '134038907', '237259899', '237409172', '133801234', '820474867', '882305550', '995031732')
order by 1, 2;

-- ===== connection: d.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- [d1_istat_measures] (0.6s)
select dataflow_id, freq, split_part(dimension_keys, '.', -1) measure, count(*) n, count(distinct series_key) series,
  count_if(obs_value < 0) negatives, min(obs_value) min_v, round(median(obs_value), 2) med_v, max(obs_value) max_v,
  count(distinct obs_year) years, min(date) d0, max(date) d1
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_IT_ISTAT
group by 1, 2, 3
order by 1, 2, n desc;
