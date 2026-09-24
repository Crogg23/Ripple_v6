# Sweep 2026-09-24: sweep3-d

25 rows: 15 place, 5 names, 5 time. All 25 are marked.
**0 live · 15 probed · 10 dead · 0 skip.**
Statements: **28 of 120**, all SELECT or WITH, plus the allowed `ALTER SESSION` timeout once per connection. None failed. The R2 names scan took 160 s; everything else ran under 3 s.
Queries are in `sweep3-d.sql`.

**Reused data.** Most county and state work reuses the scratch extracts saved by sweep-d and sweep2-d, joined locally against `CORE.DIM_COUNTY.POPULATION_2020`:
- sweep-d: `d_assist_pc`, `d_contracts_pc`, `d_fema_county`, `d_hrsa_county`, `d_cdc_injury`, `d_dim`
- sweep2-d: `sweep2-d_arcos`, `sweep2-d_sod`, `sweep2-d_sodcert`, `sweep2-d_fdicord`, `sweep2-d_wapo`, `sweep2-d_mpv`

Only counties with 10,000+ people count. SOD FIPS were padded to 5 digits and 2025 deposits were used. Overdose is the 2019-24 mean, taken only where all six years are unsuppressed (`COUNT_SUP` not null, `RATE >= 0`), which leaves 791 counties. FEMA `GROSS_INCOME` is empty, so I used FEMA IHP dollars per person instead. HRSA counts only `Designated` rows.

## Every row

| id | status | the number that mattered |
|---|---|---|
| G:JUSTICE__FED_FDIC_ENFORCEMENT_ORDERS | probed | Per person just shows where banks are chartered: DE $186 (Discover $150M). Cease-and-desist orders per 1,000 SOD bank-years: UT 58, HI 58, CA 48 vs IA 2.6 (national 15) |
| G:JUSTICE__XC_WAPO_FATAL_FORCE | probed | Per million per year: NM 10.3, AK 9.4 vs RI 0.7. Biggest rises: MT +3.1, UT +2.6. CA fell from 4.1 to 3.2. Same ranking as MPV (WaPo = 0.91x MPV) |
| G:HOUSING__FED_HUD_PUBLIC_HOUSING_AUTHORITIES | probed | A single snapshot, dated 2025-07-16. PR's statewide authority is booked to San Juan, which makes it $778 per person. Operating fund per unit: New Haven $20.2k, Pittsburgh $18.5k vs a $4.2k median. Troubled: NM 20% vs 1.7% nationally |
| G:JUSTICE__FED_FJC_ARTICLE_III_JUDGES | dead | The lead metric `C_2_ND_SERVICE_AS_CHIEF_JUDGE_BEGIN_2` is empty on all 4,074 rows. Birth state per capita reflects migration: DC 46/M, NV 1.6/M |
| G2 assistance ~ FEMA IA | dead | Spearman 0.16. Top counties are Gulf hurricane parishes, and disaster money sits in both tables, so the link is circular |
| G2 contracts ~ DEA ARCOS | dead | Spearman −0.02. The top pairs are VA mail-order pharmacies (Charleston SC, Leavenworth KS) |
| G2 contracts ~ FEMA IA | dead | Spearman −0.07 |
| G:JUSTICE__INTL_HUDOC | probed | **JUDGMENT_DATE and JUDGMENT_YEAR are blank on 100% of rows.** Violations found: UKR 96.5%, SWE 37%. No per-person rate, because there's no country population table |
| G:TRANSPORT__FED_FRA_EQUIPMENT_ACCIDENTS | probed | 182,512 accidents after dedupe ($13.9B, not $17.6B). WY tops per person at $8.8/yr. From 2000-04 to 2020-24, GA is the only state where accidents rose (396 → 411); the nation fell to 0.62x |
| G2 ECHO ~ CDC injury | dead | Spearman 0.05 on penalty dollars, 0.19 on penalized facilities per 100k |
| G2 ECHO ~ HRSA shortage | dead | Spearman 0.15 on HPSA count, 0.03 on score |
| G2 SOD ~ CDC injury | dead | Spearman −0.15. Deposits pile up in big cities |
| G2 SOD ~ HRSA shortage | dead | Spearman −0.03 both ways |
| G2 CDC injury ~ FEMA IA | probed | Spearman 0.24, within-state 0.29. Median FEMA $ per person: $49.6 in the top overdose decile vs $14.8 in the bottom |
| G2 HRSA shortage ~ FEMA IA | dead | Spearman 0.15 (score), −0.02 (count) |
| N:JUSTICE__INTL_HUDOC | probed | Top names are anonymised ("X", blank, "M.A."). OpenSanctions: 212 of 6,481 two-word names hit, and the country agrees on 75%. Two hits are OFAC-listed BGR firms |
| N:TRANSPORT__FED_FRA_EQUIPMENT_ACCIDENTS | probed | Name bridge to FRA casualties: 945 of 1,030 names hit, and the code agrees 99.3% |
| N:ECONOMICS__FED_SBA_PPP | probed | Top repeats are churches. "NEW APPLICATION" appears 37 times ($24.3M). EO BMF name+state bridge: 2.7% of keys hit, city agrees 84.6% |
| N:ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2 | probed | Of 582,657 UEIs, 130 have more than one name. Lockheed's name spans 114 UEIs. Amy Gilliland is officer 1 on 63 UEIs |
| N:TRANSPORT__FED_FRA_CASUALTIES | probed | UP 7,834 deaths. 15 short-line railroads took PPP loans, and the state agrees 15/15 |
| T:LABOR__FED_OSHA_ITA_CASE_DETAIL_2023 | probed | 890,934 cases, 282 deaths, flat by month. 22 of 229 EINs with a death had another death in 2024-25 |
| T:LABOR__FED_OSHA_ITA_CASE_DETAIL_2024 | probed | 201 deaths. USPS 15, UPS 9. 60,355 rows have a blank EIN |
| T:JUSTICE__FED_FJC_ARTICLE_III_JUDGES | probed | Median days from nomination to confirmation: 42 (1980s) → 159 (2010s) → 99 (2020s) |
| T:LABOR__FED_OSHA_ITA_CASE_DETAIL_2025 | probed | 330,447 cases, about half of 2024's in every month: a partial load |
| T:HEALTH__FQHC_SITE_PEOPLE | dead | 88 excluded NPIs. After exclusion: 0 Part D rows, 4 Open Payments meals ($24-61). The addresses are stale |

## Top three rows, walked (none reached live)

### 1. Overdose counties and FEMA housing aid (G2 CDC injury ~ FEMA IA)
- **Checked:** the 2019-24 overdose rate (791 counties with all six years unsuppressed) against FEMA IHP dollars per person, all years. I ranked counties nationally and also inside their own state.
- **Number:** Spearman 0.24 nationally and 0.29 within state. The median is $49.6 per person in the top overdose decile vs $14.8 in the bottom. Top pairs: Orleans, St. Bernard and Livingston LA; Floyd KY; Greenbrier WV.
- **Hit means:** hard-hit overdose counties are also the ones that keep flooding. That's a double burden a map could show.
- **Miss means:** the pattern is Louisiana plus the 2016-22 Appalachian floods, not a general link.
- **Boring explanation:** poor, low-lying and river-valley counties get both. IHP covers every year, but overdose only covers 2019-24.

### 2. FDIC cease-and-desist orders, rated against peers (G:FDIC_ENFORCEMENT_ORDERS)
- **Checked:** per-person dollars first. They just track where banks are chartered: DE $186 per person, which is Discover's $150M, then SD and UT. So I switched the denominator to bank-years in SOD (1994-2025) in the same state.
- **Number:** cease-and-desist orders per 1,000 bank-years: UT 58, HI 58, CA 48, NV 36 vs IA 2.6, VA 3.4, national 15.
- **Hit means:** some state banking systems draw orders at 20x the rate of others.
- **Miss means:** the gap comes from which banks the FDIC supervises, not from bank behaviour.
- **Boring explanation:** Utah's industrial banks, plus the 2008 bust states. Also, SOD bank-years include OCC and Fed banks the FDIC doesn't supervise. Next step: restrict to state nonmember banks.

### 3. Georgia rail accidents didn't fall (G:FRA_EQUIPMENT_ACCIDENTS)
- **Checked:** accidents deduped on `INCIDENT_KEY`, comparing 2000-04 with 2020-24 by state.
- **Number:** nationally, 2020-24 is 0.62x the 2000-04 level. GA went from 396 to 411 (1.04x) and is the only state that rose. MS (0.33x) and OR (0.35x) fell most.
- **Hit means:** a state where rail safety stopped improving. Next step: split GA by railroad and cause.
- **Miss means:** traffic grew in GA while it shrank elsewhere.
- **Boring explanation:** Port of Savannah intermodal growth. Also check the yard vs mainline mix before anything else.

## New data traps

1. **HUDOC `JUDGMENT_DATE` and `JUDGMENT_YEAR` are blank on 100% of 211,778 rows,** not just on the top document types. No time series is possible from this table.
2. **ECHO `TOTAL_PENALTIES` repeats a shared case penalty on every facility in it.** Five NM Permian sites each carry the same $40.3M (`LAST_PENALTY_SHARED_FACILITY_N` = 5). The same UPS $5.3M sits on many UPS facilities. National settlements land at a headquarters address: Cummins' $1.675B is on an office building in Bartholomew County IN. County penalty dollars are HQ geography. Divide by the shared count, or count penalized facilities instead. Also, `DATE_LAST_PENALTY` goes back to 1900-01-01, and 293,591 rows have no FIPS.
3. **OSHA ITA EIN is typed in by the employer and drifts between years.** USPS is `41760000` in 2023 and `417600000` in 2024-25. Blank-EIN rows (76,808 in 2023, 60,355 in 2024, 37,119 in 2025) roll up under junk names such as "test" and "wilson mcginley", and they carry 23-24 deaths a year. Cross-year EIN joins lose the biggest employer.
4. **The OSHA ITA 2025 case file is a partial load:** 330k rows, about half of 2024 in every month. Don't read it as a safer year.
5. **FJC `C_2_ND_SERVICE_AS_CHIEF_JUDGE_*` columns are empty on all 4,074 rows,** and they are the ledger's lead metric for this table.
6. **HUD PHA county roll-ups:** statewide authorities are booked to one county (PR → San Juan, and HI and VI too). CT PHAs use old county codes, so $97.7M of operating fund lands nowhere in DIM_COUNTY. `ANNUAL_EXPENSE_AMOUNT` and `SPENDING_PER_MONTH` hold negative codes on 182 rows.
7. **FRA casualties `DATE` is blank before 1997.** Conrail's 98,608 rows show dates only for 1997-99.

## Housekeeping
- My scratch files are prefixed `sweep3-d_`. I only read the `d_*` and `sweep2-d_*` files.
