-- S11 LEIE people WITHOUT a usable NPI -> Open Payments roster by first+last (or alternate last) name AND city AND state
--     -> PY2024 industry payments dated after the exclusion. The NPI path was done 2026-09-05 (F-113..F-118); this is the name path it missed.
WITH l AS (
  SELECT UPPER(TRIM(last_name)) ln, UPPER(TRIM(first_name)) fn, UPPER(TRIM(city)) city, UPPER(TRIM(state)) st,
         exclusion_type, TRY_TO_DATE(exclusion_date::string) exdt, specialty, general_category, npi lnpi
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE
  WHERE NOT COALESCE(is_entity_not_individual, FALSE) AND NOT COALESCE(npi_is_real, FALSE)
    AND NULLIF(TRIM(last_name),'') IS NOT NULL AND NULLIF(TRIM(first_name),'') IS NOT NULL),
r AS (
  SELECT profile_id::string pid, npi, UPPER(TRIM(first_name)) fn, UPPER(TRIM(last_name)) ln, UPPER(TRIM(alternate_last_name)) aln,
         UPPER(TRIM(city)) city, UPPER(TRIM(state)) st, primary_specialty
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_PROFILE_SUPPLEMENT),
m AS (
  SELECT DISTINCT l.*, r.pid, r.npi rnpi, r.primary_specialty, IFF(r.ln = l.ln, 'last', 'alt_last') via
  FROM l JOIN r ON r.fn = l.fn AND r.city = l.city AND r.st = l.st AND (r.ln = l.ln OR r.aln = l.ln)),
p AS (
  SELECT covered_recipient_profile_id::string pid, TRY_TO_DATE(date_of_payment::string) dt, total_amount_of_payment_usdollars amt,
         applicable_manufacturer_or_applicable_gpo_making_payment_name mfr, nature_of_payment_or_transfer_of_value nat
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS
  WHERE covered_recipient_profile_id::string IN (SELECT pid FROM m))
SELECT m.ln, m.fn, m.city, m.st, m.exclusion_type, m.exdt, m.specialty leie_specialty, m.general_category, m.lnpi,
       m.rnpi, m.primary_specialty, m.via,
       COUNT(p.pid) pays_all, COUNT_IF(p.dt > m.exdt) pays_after, ROUND(SUM(IFF(p.dt > m.exdt, p.amt, 0)),2) amt_after,
       MIN(IFF(p.dt > m.exdt, p.dt, NULL)) first_after, COUNT(DISTINCT IFF(p.dt > m.exdt, p.mfr, NULL)) mfrs_after,
       LISTAGG(DISTINCT IFF(p.dt > m.exdt, p.nat, NULL), '; ') natures
FROM m LEFT JOIN p ON p.pid = m.pid
GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12
ORDER BY amt_after DESC NULLS LAST
