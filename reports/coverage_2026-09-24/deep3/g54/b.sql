-- [b1_mdl_fjc]
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
order by try_to_number(j.mdl_no)

-- [b2_ein_land]
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
where state is null or state = ''

-- [b3_c4_top]
select b.ein, b.org_name, b.city, b.state, b.ruling_yyyymm, b.subsection_code, b.classification_code, b.foundation_code,
  b.filing_req_code, b.asset_amt, b.revenue_amt, b.ntee_code,
  iff(s.ein is not null and s.state is null, 'FOREIGN', 'US') loc
from LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF b
left join LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_SOI_CHARITIES s on lpad(s.ein, 9, '0') = b.ein
where b.subsection_code = '04'
qualify row_number() over (order by b.asset_amt desc nulls last) <= 30
order by b.asset_amt desc

-- [b4_bigorg_eras]
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
from base group by 1, 2 order by 1, 2

-- [b5_efile_foreign_big]
select s.ein, left(s.name, 45) name, s.city country, s.subsection, s.ruling, s.asset_amt,
  i.return_type, count(i.ein) filings, min(i.tax_period) first_tp, max(i.tax_period) last_tp, max(i.sub_date) last_sub
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_SOI_CHARITIES s
left join LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_990_EFILE_INDEX i on lpad(i.ein, 9, '0') = lpad(s.ein, 9, '0')
where s.state is null and s.asset_amt >= 1000000000
group by 1, 2, 3, 4, 5, 6, 7
order by s.asset_amt desc, 7

-- [b6_revocations_by_state]
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
order by b.cur desc nulls last

-- [b7_state_ruling_eras]
select state, iff(foundation_code in ('02','03','04'), 'PF', 'other') k, count(*) cur,
  count_if(ruling_date between '2005-01-01' and '2011-12-31') r0511,
  count_if(ruling_date between '2012-01-01' and '2018-12-31') r1218,
  count_if(ruling_date between '2019-01-01' and '2025-12-31') r1925,
  count_if(ruling_date between '2019-01-01' and '2025-12-31' and asset_amt >= 1000000) r1925_1m,
  round(sum(iff(ruling_date >= '2012-01-01', asset_amt, 0))) assets_new
from LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF
group by 1, 2
order by 1, 2
