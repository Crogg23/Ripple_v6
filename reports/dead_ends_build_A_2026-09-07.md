# Dead ends, build A: the three bridges as dbt marts — 2026-09-07

Follows reports/dead_ends_scope_A_bridges_2026-09-07.md. That report measured the joins for docket lines 4, 7, E73. This one builds them.
Line 17 was ruled not buildable there and is not touched here.

## What was built, one table

| Docket line | Mart | Grain | Rows | Scope said | Match |
|---|---|---|---|---|---|
| 4 | `LIBRARY_MARTS.HEALTH.HEALTH__ADDICTION_PRESCRIBERS_PAID` | one row per Part D prescriber of bupe / naltrexone / methadone, DY2022 | 44,846; 26,645 paid (59.4%) | 44,846; 26,645 paid (59%) | exact |
| 7 | `LIBRARY_MARTS.HEALTH.HEALTH__FQHC_SITE_PEOPLE` | one row per (person NPI, UDS site) sharing street line + 5-digit ZIP | 239,265 pairs; 173,813 people; 11,110 sites | 173,813 people; 11,110 sites | exact on people and sites |
| 7, LEIE flag | same | | 88 people at 112 sites | 90 at 114 | **off by 2, explained below** |
| 7, opt-out flag | same | | 521 people at 515 sites | 75 | **different method, explained below** |
| E73 | `LIBRARY_MARTS.HEALTH.HEALTH__SAM_EXCLUDED_PROVIDERS` | one row per SAM row, agency not HHS / OFAC / OPM | 16,144; 10 matched by NPI, 804 by name, 660 ambiguous | 16,144 non-HHS/OFAC/OPM ("13,000-odd" in prose) | exact on rows |

All three are transient tables, built by dbt, 17 tests, 17 pass.
Files: `library-onboarding/ripple_dbt/models/marts/health/health__addiction_prescribers_paid.sql`, `health__fqhc_site_people.sql`, `health__sam_excluded_providers.sql`, and `schema_dead_ends_bridges.yml` beside them.

---

## Line 4 — HEALTH__ADDICTION_PRESCRIBERS_PAID

**Left side:** `LANDING.FED_CMS_PARTD_PRESCRIBER_DRUG`, `"Gnrc_Name" ilike` buprenorphine / naltrexone / methadone, grouped by `"Prscrbr_NPI"`. Same three words the scope used.
**Right side:** `HEALTH__FED_CMS_OPEN_PAYMENTS_2022`, blank NPI dropped, summed per NPI. Top manufacturer = the payer with the most dollars to that NPI, names folded to upper.

Columns: npi, last_name, first_name, prescriber_name, state, prescriber_type, addiction_claims, addiction_drug_cost, addiction_drug_count, addiction_drugs, was_paid_2022, total_payments, payment_count, manufacturer_count, top_manufacturer, top_manufacturer_payments, data_year.

Counts through the Python door:
```sql
select count(*), count_if(was_paid_2022), round(100*count_if(was_paid_2022)/count(*),1), sum(total_payments)
  from LIBRARY_MARTS.HEALTH.HEALTH__ADDICTION_PRESCRIBERS_PAID;
-- 44,846 | 26,645 | 59.4 | $63,073,242
```

Top five by claims, against the scope's sample:

| NPI | Name | St | claims, all three drugs | paid 2022 | top manufacturer |
|---|---|---|---|---|---|
| 1134167455 | Kelly, Stephen | OK | 5,168 | $1,760 | Salix |
| 1588613020 | Sullivan, James | AL | 3,902 | $3,250 | AstraZeneca |
| 1336222504 | Morton, Robert | OK | 3,244 | $245,976 | Neurocrine |
| 1235220468 | Mekhail, Mounir | TX | 3,178 | $898 | Scilex |
| 1144227596 | Haber, Irving | IN | 2,821 | $1,698 | Radius |

Kelly reads 5,168 here and 4,377 in the scope. The scope's sample was buprenorphine claims only; the mart sums all three drugs. Not a mismatch. Morton was not in the scope's sample because he was outside the top five on buprenorphine alone.

Still true: one year each side. Targeting, never before/after. Every nature of payment is in total_payments.

---

## Line 7 — HEALTH__FQHC_SITE_PEOPLE

**Bridge:** `HEALTH__FED_CMS_NPPES` persons (ENTITY_TYPE_CODE = '1') joined to `HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES` on `upper(trim(street line 1))` and `left(zip, 5)`.
**Flags:** `HEALTH__FED_HHS_OIG_LEIE` by NPI where NPI_IS_REAL, one row per NPI (earliest exclusion); `HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS` by NPI, one row per NPI (latest end date).

Columns: npi, last_name, first_name, credential, taxonomy_code_1, bphc_assigned_number, site_name, health_center_name, site_address, site_city, site_state, site_zip5, people_at_site, nppes_last_update_date, npi_deactivation_date, is_excluded, exclusion_date, exclusion_type, leie_specialty, is_opted_out, optout_effective_date, optout_end_date, match_note.

```sql
select count(*), count(distinct npi), count(distinct bphc_assigned_number) from LIBRARY_MARTS.HEALTH.HEALTH__FQHC_SITE_PEOPLE;
-- 239,265 | 173,813 | 11,110

select count(distinct iff(is_excluded,npi,null)), count(distinct iff(is_excluded,bphc_assigned_number,null)),
       count(distinct iff(is_opted_out,npi,null)), count(distinct iff(is_opted_out,bphc_assigned_number,null)) from ...;
-- 88 | 112 | 521 | 515

select left(match_note,60), count(*) from ... group by 1;
-- address match only                                      239,148
-- excluded; NPPES address predates the exclusion            116
-- excluded; NPPES address updated on or after the exclusion   1

select max(p), median(p), count_if(p>=200) from (select bphc_assigned_number, max(people_at_site) p from ... group by 1);
-- 4,727 | 5 | 142      (same as the scope's leak check)
```

**Mismatch 1, LEIE: 88 / 112 here, 90 / 114 in the scope.** The scope's LEIE query joined NPPES with no person filter. Re-ran it split by entity type:
```sql
select n.entity_type_code, count(distinct l.npi), count(distinct u.bphc_assigned_number)
  from LEIE l join NPPES n on n.npi=l.npi join UDS u on <address join> where l.npi_is_real group by 1;
-- '1' 88 / 112   |   '2' 2 / 2
```
The two missing are org NPIs that LEIE lists (an excluded business whose NPPES row is type 2). This mart is people only, on purpose. 88 is right for "banned people"; 90 was "banned NPIs".

**Mismatch 2, opt-out: 521 here, 75 in the scope.** Not the same measurement. The scope joined the opt-out file's own street address to the UDS address and never went through NPPES. This mart flags the person-site pair by NPI, so an opted-out doctor whose opt-out affidavit lists a home address but whose NPPES practice address is the clinic now counts. Re-ran the scope's address method today: still 75. Both numbers stand; they answer different questions. 521 is "opted-out doctors whose NPPES practice address is an FQHC"; 75 is "opt-out affidavits filed from an FQHC address."

**One row contradicts the scope's "every address predates its exclusion":** NPI 1639122930, JOINER, Bolinas Community Health Center CA, excluded 2016-10-20 under 1128b4, NPPES last updated 2023-03-07. One of 117 excluded rows. The scope looked at five. match_note carries it.

Still true: an address bridge, not a roster. LEIE carries a real NPI on 10% of rows, so 88 is a floor. 142 sites carry 200+ people; people_at_site is on every row to cap them.

---

## Line E73 — HEALTH__SAM_EXCLUDED_PROVIDERS

**Left side:** `PROCUREMENT__FED_SAM_EXCLUSIONS` where `coalesce(upper(excluding_agency),'') not in ('HHS','OFAC','OPM')`. Null agency (2,397 upstream) is kept.
**Match:** SAM NPI real (not blank, not '0000000000') → NPPES on NPI. Else individual with first, last, state → NPPES persons on `upper(first) + upper(last) + practice state`. One hit lands; more than one lands null with `'ambiguous: N people share it'`, same shape as `finance__senate_trades`. Entities get no name match.

Columns: sam_number, uei, excluding_agency, exclusion_type, exclusion_program, classification, is_entity_not_individual, entity_name, first_name, last_name, city, state, activation_date, termination_date_raw, is_currently_excluded, sam_npi, npi, nppes_name, taxonomy_code_1, credential, match_method, match_note.

```sql
select match_method, count(*) from LIBRARY_MARTS.HEALTH.HEALTH__SAM_EXCLUDED_PROVIDERS group by 1;
-- null 15,330 | first+last+state 804 | npi 10

select regexp_replace(match_note,'[0-9]+','N'), count(*) from ... group by 1;
-- no NPPES person with that first, last and practice state   10,066
-- entity, no person match attempted                            4,239
-- one NPPES person with that first, last and practice state      804
-- ambiguous: N people share it                                   660
-- no first name, last name or state to match on                  365
-- SAM npi found in NPPES                                          10

select excluding_agency, count(*), count_if(npi is not null) from ... group by 1 order by 2 desc limit 8;
-- DOJ 3,219 / 240 | null 2,397 / 151 | HUD 2,315 / 110 | EPA 2,164 / 100 | USN 831 / 26 | ICE 814 / 26 | DLA 617 / 17 | USA 544 / 21
```

**Held against the scope's name numbers.** The scope reported first+last+state on all 85,218 individual names: 14,085 matched, 9,591 one-hit. Re-ran that on all individuals with the mart's key today: 85,225 names, 14,085 matched, 9,591 one-hit. Same match counts; the 7-name difference in the denominator is not explained, and it moves nothing because both hit counts are identical. The mart's 804 is that same rule on the 16,144-row agency-filtered slice, so it is smaller by construction.

The 10 NPI matches: the scope said 4,854 real-NPI hits across all of SAM. 4,844 of those sit on HHS, OFAC or OPM rows and are out by design. 10 remain.

**Bad news, marked:** 814 of 16,144 rows land a person, 5%. 10,066 rows have a first, last and state and hit nobody in NPPES, which is the honest answer for most contractors: they are not health providers. The 804 one-hit names are leads, not matches. Sample: WARREN, ANNE, TN, agency null, NPI 1215413562, taxonomy 183500000X (pharmacist); BURKE, ROBERT, FL, USN, 2085R0202X (radiology). A common name in a big state is a coin flip until the SAM address is checked.

Still true: SAM address is not used as a tiebreaker. Upstream mart is Active-only, so purged bans are invisible.

---

## Every command, in order

```
# read-only column check, Python door
python <scratchpad>/cols.py        # information_schema.columns on the 7 input tables
python <scratchpad>/probe.py       # SAM agency counts, non-HHS/OFAC/OPM slice = 16,144 rows / 11,903 individuals / 10 real NPIs

# dbt, pinned engine
cd library-onboarding/ripple_dbt; export PYTHONUTF8=1
../../.dbt-venv/Scripts/dbt.exe parse
   -> 0 errors, 2 deprecation warnings (both predate this work, same two as the closeout report)
../../.dbt-venv/Scripts/dbt.exe run --select health__addiction_prescribers_paid health__fqhc_site_people health__sam_excluded_providers
   -> PASS=3, 23.2s total (5.6s / 5.9s / 6.8s)
../../.dbt-venv/Scripts/dbt.exe test --select health__addiction_prescribers_paid health__fqhc_site_people health__sam_excluded_providers
   -> PASS=17 WARN=0 ERROR=0

# counts, Python door
python <scratchpad>/counts.py      # the row counts, flag counts, note shapes and transient check above
python <scratchpad>/gap.py         # the 90-vs-88 split by entity type, the one post-exclusion row, the 85,218-vs-85,225 denominator
```

No hook refused anything. `dbt run` is classed `rebuild` by the warehouse gate; it went through, so a rebuild greenlight was already open for this session.
Nothing dropped, nothing truncated. The three tables are new names; no existing table was replaced.

## Docket

`docket/docket.csv` rows 4, 7, E73: where_it_stands now says built, with the mart name and the count; watch_out now says what is still true after the build.
`docket/docket_open.csv` does not carry rows 4, 7 or E73 (it holds the 62 "not started" and 11 "part done" lines only), so nothing to change there.

## Cost
Three dbt runs and roughly ten read-only queries. dbt logged 23 seconds of build; the closeout report priced a sibling single-mart run at 0.0002 credits. No real number from the query log was pulled for these three; call it "no real number for this" until priced.

parked: the docket's effort column still reads "Skip — already ruled out" on all three rows. It was not in the ask, and it now contradicts where_it_stands.

## Skeptic pass and fixes, 2026-09-07 15:40

Skeptic verdict: marts right, docket bookkeeping wrong. Four findings, all fixed.

| finding | fix |
|---|---|
| `%naltrexone%` caught methylnaltrexone (constipation) and naltrexone/bupropion (Contrave); 511 prescribers had nothing else | two `not ilike` clauses added; mart rebuilt: 44,335 prescribers, 26,193 paid (was 44,846 / 26,645); 5/5 tests pass |
| docket rows 4, 7, E73 had free-text `where_it_stands`, so build_docket.py dropped them from DOCKET.md | set to `found something`; build note moved to `probe`; effort now "Small — mart built" |
| DOCKET.md written as cp1252, six 0x97 bytes, not valid UTF-8 | build_docket.py opens and writes with encoding="utf-8" on all five file handles; regenerated, verified |
| "804 name matches" reads as people; it is 804 rows, 634 distinct NPIs | noted here; one NPI is claimed by 8 SAM rows |

Not changed: opt-out 521 by NPI vs scope's 75 by address, both stand as different questions. Lucemyra/lofexidine, 10 rows, left out.
