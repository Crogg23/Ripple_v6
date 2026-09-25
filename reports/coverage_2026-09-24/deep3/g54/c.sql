-- [c1_c4_shares]
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
from base group by 1, 2 order by 1, 2

-- [c2_13f_foreign_c4]
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
order by 1, 5 desc

-- [c3_fac_pr_movers]
select lpad(regexp_replace(auditee_ein, '[^0-9]', ''), 9, '0') ein, audit_year, left(auditee_name, 40) name, auditee_city, auditee_state,
  left(auditee_address_line_1, 35) addr, total_amount_expended
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FAC_SINGLE_AUDIT
where lpad(regexp_replace(auditee_ein, '[^0-9]', ''), 9, '0') in
  ('650216638', '134038907', '237259899', '237409172', '133801234', '820474867', '882305550', '995031732')
order by 1, 2
