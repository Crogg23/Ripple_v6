# The Wonder Handbook

A catalog of 125 questions a public-records warehouse can answer, and the exact data behind each one.

Assembled 2026-09-18. Every table name and column name in this book was checked against the warehouse's own table and column lists on that day. Row counts are the warehouse's metadata counts. Date ranges and fill rates come from a column-by-column profile run on 2026-09-08; tables landed after that date are marked "not yet measured" rather than guessed.

Nothing in this book is a finding unless its Status line says "measured". Everything else is a question with its data mapped, its join named, and its limits written down before any query is run.

## How to read an entry

| field | what it tells you |
|---|---|
| The physical thing | the concrete object in the world the question is about |
| Status | never run, or measured with the number and the date |
| Data grade | A a real shared id across tables, or one table that needs no join; every side measured; years overlap. B works with a stated limit. C proxy or partial answer. D cannot be answered as worded with the data held |
| the table | exact warehouse name, row count, what one row is, years covered, key used |
| Columns that carry it | the exact columns read, with fill rate where measured |
| The join, hop by hop | one hop per line, column to column |
| A hit means / A miss means | what yes looks like, what no looks like, decided before running |
| Limits, said out loud | the traps and gaps that bear on this question, with their numbers |
| The picture | the chart that would show it |
| First cheap check | the smallest count that proves the join before anything big is run |

## Sources named inside the entries

| name in the text | what it is |
|---|---|
| the fact file | built 2026-09-18 for this book: the live column list and metadata row count of every warehouse table, joined to the 2026-09-08 column profile |
| the 2026-09-08 profile | a column-by-column scan of 650 tables: fill rate, distinct count, minimum, maximum, top values |
| traps.md, the traps log | the project's running log of data traps: columns that look usable and are not, with the date each was found |
| the wonder extract, wonder_rankings | the working files where each question was first written and scored; measured numbers dated 2026-08-21 and 2026-08-22 come from runs recorded there |
| the 09-09 table map | a first mapping of questions to tables, written 2026-09-09 from catalogs alone; several of its gaps were closed by later loads, and entries say where it was wrong |
| the phase 5 probe | the load report for tables landed 2026-09-10 and 2026-09-11, with verified counts |

## The book in numbers

| what | count |
|---|---|
| questions | 125 |
| distinct warehouse tables behind them | 266 |
| grade A | 10 |
| grade B | 77 |
| grade C | 34 |
| grade D | 4 |
| already measured, in whole or part | 19 |

## Index


### Place: where you live decides

| id | question | grade | tables | status |
|---|---|---|---|---|
| W1 | Flood-aid zips denied mortgages more the next year | B | 10 | never run |
| W2 | 1930s redline maps predict today's water violations | C | 4 | never run |
| W3 | Biggest HUD multifamily owners, and what their buildings' records show | B | 2 | never run |
| W5 | Lenders pull out of a county after the first big storm | B | 4 | never run |
| W6 | Counties that lost doctors, banks, factories same decade | C | 6 | never run |
| W7 | Single P.O. box hosts clinics, PACs, contractors | B | 4 | never run |
| W8 | Counties with one doctor per thousand and shrinking | C | 5 | never run |
| W9 | Rural clinics close where the only bank branch closed | B | 2 | never run |
| W10 | Rural counties send most to DC, get least back | B | 5 | never run |
| W11 | Rural water systems violate more per capita than urban | B | 3 | never run |
| W12 | Mine closed, overdoses rose within three years | B | 4 | never run |
| W13 | Counties host most plants, get least federal money | B | 6 | never run |
| W15 | High-hazard dams within ten miles of a nursing home | B | 2 | never run |
| W16 | Fracking counties see water violations climb after boom | B | 5 | never run |
| W18 | Water systems violate yearly, never enforced | A | 2 | never run |
| W23 | Where coal plants closed, respiratory claims fell | C | 5 | never run |
| P-081 | More-minority communities get inspected less | B | 1 | measured on 2026-08-22: inspections per facility fall from 2.90 in the whitest t |

### Body: what happens to your health

| id | question | grade | tables | status |
|---|---|---|---|---|
| W26 | 2010 pill counties become 2024 overdose counties, or not | B | 4 | never run. Absorbs wonders 41 and 42 (pills per resident by county; distributor  |
| W28 | Nursing homes chart sicker right after a chain buys them | D | 4 | never run. |
| W29 | Dialysis chains arrive, local kidney doctor count falls | B | 5 | never run. |
| W30 | Water violations cluster where hospitals closed | B | 3 | never run. |
| W32 | Hospice agencies open where nursing home census drops | C | 4 | never run. |
| W33 | Sickest-charted homes also carry most fire violations | B | 2 | never run. |
| W34 | Counties with more nursing beds than doctors to staff | B | 4 | never run. |
| W35 | Dementia charting jumps after reimbursement rule change | D | 1 | never run. Check first: which assessment item is the dementia item is unknown. |
| W36 | Nonprofit hospitals pay least charity per surplus dollar | B | 5 | never run. |
| W37 | Hospitals closed, where doctors showed up next year | C | 4 | never run. |
| W39 | Hospitals that own a home health agency, and how many | A | 2 | partially measured. the fact file records 411 entity ids shared between the home |
| W40 | Hospitals near pollution bill more respiratory per patient | C | 4 | never run. |
| W44 | Drugs leading Part D cost growth, and who prescribes them most | B | 3 | never run. |
| W45 | Antipsychotic scripts per nursing bed track chain ownership | C | 5 | never run. |
| W46 | After pill volume explains overdoses, which counties stand out | B | 3 | never run. |
| W47 | After patient age explains prescribing, which counties prescribe more | B | 4 | never run. |
| W48 | Pharma payments precede prescribing shifts by a year | B | 7 | never run. |
| W49 | Doctors excluded and still paid by pharma | B | 2 | never run. |
| W50 | Device recalls follow surgeon royalty payments by product | C | 6 | never run. |
| H-106 | Nursing-home citation severity depends on which state inspected | A | 2 | measured on 2026-08-22: harm-level share (G-L) 12.50% KY, 12.07% IL down to 1.32 |
| H-094 | Staffing predicts the next deficiency | B | 3 | never run. |
| H-107 | Nursing-home fines per owner, not per location | B | 4 | never run. |
| H-105 | Stars lost after a fine, or fines after lost stars | C | 3 | never run. |
| H-110 | Inspection records too clean for their peers | B | 2 | never run. |
| H-104 | Does a fine change behaviour, before versus after | B | 3 | partially measured: the book records 6,628 of 14,700 homes fined, 3,722 homes wi |
| WN-147 | Predicted versus actual inspection outcomes | B | 2 | never run. |
| WN-149 | Does special-focus status change a home | C | 3 | partially measured: 88 current special-focus homes, 440 candidates, no designati |
| H-111 | Surveys bunch at the end of the window | B | 1 | never run. |
| WN-150 | Low-entropy inspection outcomes | B | 1 | never run. |
| WN-154 | Homes that act like a chain without being one | B | 2 | never run. |
| N3 | The roughly 684 homes CMS flags as PE or REIT owned, against matched peers | C | 5 | partially measured on 2026-09-18: `PRIVATE_EQUITY_COMPANY_OWNER` is 'Y' on 196 o |

### Money: who gets it, who gives it

| id | question | grade | tables | status |
|---|---|---|---|---|
| W51 | 13F ownership shifts the quarter before a contract lands, matched on multi-word issuer name | B | 5 | never run |
| W52 | Congressional trades cluster around roll-call votes, House 2021-2026 | B | 5 | never run |
| W53 | Zips give most to politics, get least back | B | 5 | never run |
| W55 | Disaster contractors win same counties every storm | B | 3 | never run |
| W56 | Banks under orders keep lending in the same counties | B | 5 | never run |
| W58 | Small-business loans dry up where local bank absorbed | B | 5 | never run |
| W59 | Denial rates diverge most between neighboring counties | B | 3 | never run |
| W60 | Banks that failed after 2012: did complaints rise first | B | 3 | never run |
| W61 | Grant recipients with going-concern doubt in their audit keep winning awards | B | 2 | never run |
| W62 | 13F holders exit before the first big EPA or mine fine | B | 7 | never run |
| W63 | Pension plans that collapsed, and who sponsored them | B | 3 | never run |
| W65 | Parents hide behind most subsidiaries per contract | B | 2 | never run |
| W66 | Charities pay top officer most per revenue dollar | C | 3 | never run |
| W67 | Nonprofit revenues spike after disaster declaration | D | 5 | never run |
| W68 | Nonprofits win grants and register lobbyists | B | 3 | never run |
| W69 | Hospital PACs and hospital employees donate to members | B | 6 | never run |
| W70 | After population explains contracts, which counties get more | B | 2 | never run |
| W71 | After income explains denials, which lenders deny more | B | 3 | never run |
| W72 | Contractors suspended and win again under a new name | B | 4 | never run |
| W73 | Pandemic loans went to firms already excluded | B | 3 | never run |
| W74 | Universities hold NIH grants and pharma-paid faculty | C | 5 | never run |
| W75 | NIH grants land where pharma dinners land, by county | B | 6 | never run |
| M-239 | Templated CFPB narratives | A | 1 | partially measured on 2026-08-22 (run date of reports/wonder_rankings.md): the m |
| M-245 | Complaint spike at one credit bureau shows at the others | A | 1 | partially measured on 2026-08-22 (run date of reports/wonder_rankings.md): Trans |
| M-240 | Companies with one canned complaint response | A | 1 | partially measured on 2026-08-22 (run date of reports/wonder_rankings.md): Exper |
| WN-143 | CFPB filing language collapses over 14 years | B | 1 | partially measured on 2026-08-22 (run date of reports/wonder_rankings.md): 2.57M |
| WN-152 | The donor in the most networks | B | 1 | partially measured on 2026-08-22 (run date of reports/wonder_rankings.md): the t |
| N6 | Recipients that appear only in FY2020 and FY2021 assistance, then vanish | B | 3 | partially measured on 2026-09-18: FY2020 holds 25,183,037 assistance rows and FY |

### Power: who decides, who watches

| id | question | grade | tables | status |
|---|---|---|---|---|
| W76 | Immigration judge grant rate drifts with administration | B | 2 | Never run. The tables landed 2026-09-10. |
| W77 | Judges hold stock in companies on their own docket | C | 6 | Never run. |
| W78 | Court filings against a chain rise before Medicare fines | C | 3 | Never run. |
| W79 | Mine fines unpaid longer under certain operators | B | 3 | Measured (date not given in the source row; listed as already measured on 2026-0 |
| W80 | Detention contractors donate where they house detainees | C | 7 | Never run. |
| W82 | Bills lobbied hardest before markup, and by whom | B | 4 | Never run. The gap named on 2026-09-09 (lobbying years missing) closed on 2026-0 |
| W83 | 527 groups spend most per registered voter | C | 2 | Never run. |
| W84 | Foreign agents register before trade or arms votes | C | 3 | Never run. |
| W85 | Plant owners donate to regulators' overseers by state | C | 6 | Never run. |
| W86 | Lag from complaint spike to enforcement, by bank | C | 2 | Never run. Absorbs wonder 54. |
| W87 | Lobbying spikes before agency rules, by how many weeks | C | 3 | Never run. Was dead on 2026-09-09 with zero overlapping years; the lobbying back |
| W88 | Judges' former firms appear most on their dockets | C | 3 | Never run. |
| W89 | Which agency jobs appear most in lobbyists' covered-position text | B | 2 | Never run. Reworded on 2026-09-18 because the second table lists job slots, not  |
| W90 | Detention contracts grow where ICE detainers grow | B | 5 | Never run. The gap named on 2026-09-09 (no county code on contracts) closed on 2 |
| W91 | Immigration judges furthest from their own court's average | B | 2 | Never run. Reworded on 2026-09-18: judges landed 2026-09-10; the appeals table a |
| W92 | Foreign-owned contractors win more in certain agencies | B | 2 | Never run. The gap named on 2026-09-09 (no foreign-entity code, no agency code)  |
| W95 | Political nonprofits share addresses with PACs | B | 3 | Never run. |
| W96 | Years from redline map to shortage-area designation | C | 3 | Never run. |
| W97 | Doctors also donors, contractors, nursing owners | C | 6 | Never run. The gap named on 2026-09-09 (no table naming nursing-home owners) clo |
| W98 | Offshore-leak names in US federal contracts | C | 3 | Never run. Absorbs wonder 116. |
| W99 | Hospital execs who are also insiders at public companies | C | 3 | Never run. Reworded on 2026-09-18: private suppliers cannot be seen; insider fil |
| M-056 | Money arrives right before the vote | B | 5 | Partially measured. The chain was verified end to end: 54.2M contributions ($6.8 |
| M-015 | Out-of-state money flooding small races | B | 3 | Never run. The book records "chain works; 2023-2026 window", measured on an olde |
| M-007 | Donations spike on filing-deadline eves | B | 2 | Never run. Listed in the book as a known artefact to be measured so that M-056 c |
| N2 | Removal orders given with nobody in the room, by court and year | B | 1 | Never run. New on 2026-09-18. The fill of `ABSENTIA`, `BASE_CITY_CODE` and `COMP |

### Work and things: the machine running

| id | question | grade | tables | status |
|---|---|---|---|---|
| W102 | Visa sponsors carry unpaid wage judgments | C | 2 | never run. The wage-case table landed 2026-09-10; before that the question had n |
| W103 | Union locals shrink where county contracts grow | B | 4 | never run. The 2026-09-09 gap (no county on contracts) closed on 2026-09-10 when |
| W104 | Mines delinquent on fines, injuries climb next year | B | 4 | never run. The unpaid-fine side was measured on its own for another row: $1.82B  |
| W107 | Fast-track devices recall more than standard | D | 4 | never run. |
| W111 | Recalled models with the most complaints, by state | B | 3 | never run. Reworded on 2026-09-18: the old wording asked where models were sold, |
| W113 | UK shell controls a US nursing home | C | 4 | never run. The 2026-09-09 gap (no owner-level file) closed on 2026-09-10 when th |
| W115 | UK controllers also control US contractors | C | 3 | never run. |
| W117 | US doctors who control UK companies, and how many | C | 4 | never run. Reworded on 2026-09-18: the old wording asked "what sector", and the  |
| W120 | Mine operators fined, paid, fined again for the same section of the Act | B | 3 | never run. Reworded on 2026-09-18 to mines only: the EPA enforcement summary kee |
| W121 | Zips file same complaint against same firm yearly | B | 1 | never run. The final list marks it "check masked ZIPs first". |
| W122 | Counties flood, rebuild, flood again on federal money | B | 4 | never run. The 2026-09-09 gaps (no declarations table, assistance capped at 1M r |
| W123 | 990 hospital charity rises where wages fall | C | 4 | never run. The final list marks the gap closed on 2026-09-10/11: the cost report |
| W124 | After plant count explains emissions, which operators dirtier | B | 6 | never run. The 2026-09-09 gap (one emissions year) closed on 2026-09-10 when fou |
| W125 | Workplaces with the highest injury rates by owner, three years | B | 5 | never run. Reworded on 2026-09-18: three years cannot show "rising". |
| P-146 | Mine deaths without a paper trail | A | 3 | partially measured. The inputs were verified when the row was scored: 1,208 fata |
| P-147 | A mine changes hands, its violation rate changes | A | 2 | partially measured. Verified when scored: 6,358 mines saw 2 controllers, 2,091 s |
| P-148 | A death at one mine changes the operator's other mines | A | 3 | partially measured. Verified when scored: 1,208 fatalities, 6,082 controllers wi |
| P-159 | OSHA injury counts bunch on round numbers | A | 3 | never run. The repo holds a bunching detector; it has not been pointed at these  |
| P-160 | After a reported death, do hours and injuries change | B | 3 | partially measured. Verified when scored: 219,860 establishments appear in both  |
| WN-136 | Same-owner co-spike, controlling for district and calendar | B | 3 | partially measured. The uncontrolled version ran on 2026-08-21: mines under one  |
| P-149 | Mine inspection has a season, accidents fill the gaps | B | 3 | never run. Verified when scored: citations 1994 to 2026, 3.09M rows, 31,277 mine |
| WN-144 | Injury rates cluster by industry and state | B | 3 | never run. Verified when scored: 1,218 industry codes, 3 years, about 1.18M esta |
| N1 | Employers caught with child-labor violations that hold federal contracts | C | 3 | never run. New on 2026-09-18. The final list marks it "fill-check the minor-coun |
| N5 | Repeat wage violators that keep winning contracts | C | 3 | never run. New on 2026-09-18. The final list marks it "fill-check the repeat fla |

---


# Place: where you live decides

### W1 · Flood-aid zips denied mortgages more the next year

**The physical thing.** A household files a FEMA aid claim after a flood. The next year, people in the same county apply for mortgages, and a bank says no.

**Status.** never run

**Data grade.** B. County FIPS sits on both sides and the years overlap 2015-2024, but the mortgage files carry no ZIP, so the question runs on county, not ZIP; the seven 2018-2024 mortgage tables are unprofiled.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS | 26,250,920 | one household's aid registration for one disaster | 2002-2026 (`DECLARATION_DATE`) | `FIPS`, `DISASTER_NUMBER` |
| LIBRARY_RAW.LANDING.FED_FEMA_DISASTER_DECLARATIONS | 70,402 | one disaster in one designated area (5,264 disasters) | not yet measured | `DISASTERNUMBER`, `FIPSSTATECODE` + `FIPSCOUNTYCODE` |
| LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_HISTORIC | 44,992,667 | one mortgage application and what the lender did with it | 2015-2017 (`AS_OF_YEAR`) | `STATE_CODE` + `COUNTY_CODE` |
| LIBRARY_RAW.LANDING.FED_CFPB_HMDA_LAR_2018 | 15,140,471 | one mortgage application | 2018 | `STATE_CODE`, `COUNTY_CODE` |
| LIBRARY_RAW.LANDING.FED_CFPB_HMDA_LAR_2019 | 17,573,984 | same | 2019 | same |
| LIBRARY_RAW.LANDING.FED_CFPB_HMDA_LAR_2020 | 25,699,043 | same | 2020 | same |
| LIBRARY_RAW.LANDING.FED_CFPB_HMDA_LAR_2021 | 26,269,980 | same | 2021 | same |
| LIBRARY_RAW.LANDING.FED_CFPB_HMDA_LAR_2022 | 16,125,975 | same | 2022 | same |
| LIBRARY_RAW.LANDING.FED_CFPB_HMDA_LAR_2023 | 11,564,178 | same | 2023 | same |
| LIBRARY_RAW.LANDING.FED_CFPB_HMDA_LAR_2024 | 12,259,199 | same | 2024 | same |

**Columns that carry it.**
- FEMA registrations: `DISASTER_NUMBER` (100%), `DECLARATION_DATE` (100%), `FIPS` (74.21%, 3,379 distinct), `DAMAGED_ZIP_CODE` (100%), `CENSUS_GEOID` (73.75%), `FLOOD_DAMAGE`, `FLOOD_DAMAGE_AMOUNT`, `IHP_AMOUNT`, `HA_AMOUNT` (fill on the last four not yet measured).
- Declarations: `DISASTERNUMBER`, `INCIDENTTYPE`, `DECLARATIONDATE`, `FIPSSTATECODE`, `FIPSCOUNTYCODE`. Fill rate not yet measured.
- HMDA 2015-2017: `AS_OF_YEAR` (100%), `STATE_CODE` (98.4%), `COUNTY_CODE` (98.17%), `ACTION_TAKEN`, `LOAN_PURPOSE`, `DENIAL_REASON_1`.
- HMDA 2018-2024: `ACTIVITY_YEAR`, `STATE_CODE`, `COUNTY_CODE`, `CENSUS_TRACT`, `ACTION_TAKEN`, `LOAN_PURPOSE`, `DENIAL_REASON_1`. Fill rate not yet measured.

**The join, hop by hop.**
```
FED_FEMA_DISASTER_DECLARATIONS.DISASTERNUMBER ➔ HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS.DISASTER_NUMBER   (overlap not yet measured; picks flood disasters by INCIDENTTYPE)
HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS.FIPS (left-padded to 5) ➔ HOUSING__FED_CFPB_HMDA_HISTORIC.STATE_CODE + COUNTY_CODE (both left-padded)   (overlap not yet measured)
HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS.FIPS ➔ FED_CFPB_HMDA_LAR_2018..2024.COUNTY_CODE   (format and overlap not yet measured)
```

**A hit means.** Counties with flood-aid registrations in year N show a higher mortgage denial share in year N+1 than in year N-1, and the rise is larger than in same-state counties with no flood declaration that year.

**A miss means.** Denial share in flooded counties moves the same as in their unflooded neighbors. That would say lenders did not tighten after the aid year, at county scale.

**Limits, said out loud.**
- No ZIP on any mortgage table. "Zips" becomes counties. Tract is the only finer option (`CENSUS_TRACT`, `CENSUS_GEOID` 73.75% filled), not yet tested.
- FEMA `FIPS` is unpadded text for states 01-09: '1097' and '01097' both exist, 636 distinct values fall to 601 after padding (traps 2026-09-05). Unpadded, nine states silently drop out.
- HMDA 2015-2017 has no date, only a year. County-null rows hold 19,331 denials and land in any control group unless `COUNTY_CODE` is not null is on every query. It has two file families; group by `ACTION_TAKEN` first.
- 2018 and 2019 carry placeholder rows with `ACTION_TAKEN` '-1': 1,961 and 21. Filter them before any count.
- The file layout changes at 2018 (82 columns before, 102 after). A before/after pair that straddles 2017-2018, such as Harvey, Irma and Maria, compares two layouts and needs the action codes checked by hand.

**The picture.** Scatter: x = flood-aid registrations per county in year N, y = change in denial share from N-1 to N+1; one dot is one county-disaster.

**First cheap check.** Count distinct padded `FIPS` values in the FEMA table for 2016 declarations that also appear as `STATE_CODE`+`COUNTY_CODE` in the 2017 HMDA rows.

---

### W2 · 1930s redline maps predict today's water violations

**The physical thing.** A 1930s federal lending map coloured some city neighborhoods red. Today a public water system serving that city racks up drinking-water violations, or does not.

**Status.** never run

**Data grade.** C. The full map is landed, 10,154 neighborhood polygons, but a water system has no coordinates and serves a whole city, so the data compares cities by how much of them was graded D, not neighborhoods; the full map is unprofiled and its county code has no measured fill.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_RAW.LANDING.FED_MAPPING_INEQUALITY | 10,154 | one graded neighborhood polygon on a 1930s city map (the full map) | not yet measured (`YEAR_MAPPED`) | `CITY` + `STATE`; `FIPS` if filled |
| LIBRARY_MARTS.HOUSING.HOUSING__FED_MAPPING_INEQUALITY | 1,155 | one merged polygon per city and grade (a summary of the full map) | not yet measured (`YEAR_MAPPED`) | `CITY` + `STATE` |
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS | 578,198 | one area (county, city, ZIP) served by one water system | 1995-2026 (`LAST_REPORTED_DATE`) | `PWSID`, `CITY_SERVED` + `STATE_SERVED`, `COUNTY_FIPS` |
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT | 15,432,737 | one violation with its enforcement fields | to 2026-06-09 (`NON_COMPL_PER_BEGIN_DATE`; minimum 1900-01-01 is a placeholder) | `PWSID` |

**Columns that carry it.**
- Full map (landing): `CITY`, `STATE`, `FIPS`, `HOLC_GRADE`, `YEAR_MAPPED`, `GEOMETRY`, `LAT`, `LON`. Fill rate not yet measured on any of them. `HOLC_ID` is not an id (one distinct value, traps 2026-09-05).
- Summary mart: `CITY`, `STATE`, `HOLC_GRADE`, `HOLC_GRADE_RANK`, `GEOMETRY`. Its `FIPS` is blank on all 1,155 rows.
- Water areas: `PWSID` (100%, 418,885 distinct), `AREA_TYPE_CODE`, `CITY_SERVED`, `STATE_SERVED`, `COUNTY_FIPS` (404,823 of 405,396 named county rows, phase 5 report).
- Violations: `PWSID` (100%, 265,738 distinct), `VIOLATION_ID`, `IS_HEALTH_BASED_IND`, `VIOLATION_CODE`, `NON_COMPL_PER_BEGIN_DATE` (93.5%).

**The join, hop by hop.**
```
FED_MAPPING_INEQUALITY.CITY + STATE ➔ ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS.CITY_SERVED + STATE_SERVED   (name join; overlap not yet measured)
or, only if the landing FIPS proves filled: FED_MAPPING_INEQUALITY.FIPS ➔ ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS.COUNTY_FIPS   (fill and format not yet measured)
ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS.PWSID ➔ ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT.PWSID   (direct overlap not yet measured; each side matches the SDWA facilities table at 100%)
```

**A hit means.** Cities where a larger share of the mapped area was graded D carry more health-based violations per water system than cities graded mostly A and B.

**A miss means.** No slope between a city's D-share and its violation count. That says little about neighborhoods, because the water data never reaches neighborhood scale.

**Limits, said out loud.**
- Use the landing table for any area or polygon count. The mart is 1,155 rows against the map's 10,154, 11% of the polygons, so a spatial count off the mart is on a fraction of the map (traps 2026-09-05).
- The landing `GEOMETRY` is GeoJSON text; it parsed to a shape on 10,153 of 10,154 rows when tested (traps 2026-09-05). 814 rows have a blank grade and there are 3 trailing-space spellings of the grades.
- The mart's `FIPS` is blank on every row. The landing `FIPS` is unmeasured: it may be filled, blank, or an empty string. Do not plan on it until counted.
- No water-system coordinates or service-area shapes are landed. A system cannot be placed inside a red or green polygon; it can only be tied to a city or county. This is the limit that holds the grade at C.
- Every mapped city was redlined somewhere, so there is no unmapped control group in this table. Water system ids starting 04 to 10 are EPA regions and never match a place.

**The picture.** Scatter: x = share of a city's mapped area graded D, y = health-based violations per water system; one dot is one city.

**First cheap check.** On LIBRARY_RAW.LANDING.FED_MAPPING_INEQUALITY, count rows where `FIPS` is non-null and not an empty string, out of 10,154.

---

### W3 · Biggest HUD multifamily owners, and what their buildings' records show

**The physical thing.** One landlord, many HUD-backed apartment buildings, each filed under its own LLC. The roll-up shows who really holds the most buildings, and the rent-subsidy contracts sitting on them.

**Status.** never run

**Data grade.** B. The owner file and the Section 8 contract file share HUD's own `PROPERTY_ID`, so each building's subsidy record attaches by id; the limits are that "biggest owner" needs names and addresses folded by hand, the owner file is unprofiled, and no HUD inspection-score table is landed.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_RAW.LANDING.FED_HUD_MF_PROPERTIES_OWNERS | 23,612 | one HUD-assisted or insured apartment property with its owner and manager | one snapshot, landed 2026-09-11; date range not yet measured | `PROPERTY_ID`; `OWNER_ORGANIZATION_NAME` + `OWNER_ADDRESS_LINE1`; `MGMT_AGENT_PARTICIPANT_ID` |
| LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_MF_SECTION8_CONTRACTS | 24,309 | one Section 8 rent-subsidy contract on one property | contracts effective 1977-2027 (`TRACS_EFFECTIVE_DATE`) | `PROPERTY_ID` |

**Columns that carry it.**
- HUD owners: `PROPERTY_ID`, `PROPERTY_TOTAL_UNIT_COUNT`, `OWNER_PARTICIPANT_ID`, `OWNER_ORGANIZATION_NAME`, `OWNER_ADDRESS_LINE1`, `OWNER_ZIP_CODE`, `OWNER_COMPANY_TYPE`, `OWNERSHIP_EFFECTIVE_DATE`, `MGMT_AGENT_PARTICIPANT_ID`, `MGMT_AGENT_ORG_NAME`, `PRIMARY_FINANCING_TYPE`, `IS_INSURED_IND`, `IS_HUD_HELD_IND`, `COUNTY_CODE`. Fill rate not yet measured on any of them.
- Section 8 contracts: `PROPERTY_ID`, `CONTRACT_NUMBER`, `TRACS_STATUS_NAME`, `ASSISTED_UNITS_COUNT`, `RENT_TO_FMR_RATIO`, `RENT_TO_FMR_DESCRIPTION`, `PROGRAM_TYPE_NAME`, `TRACS_EFFECTIVE_DATE` (100%), `TRACS_OVERALL_EXPIRATION_DATE` (100%). `PROPERTY_ID` fill not yet measured.

**The join, hop by hop.**
```
group FED_HUD_MF_PROPERTIES_OWNERS by folded OWNER_ORGANIZATION_NAME + OWNER_ADDRESS_LINE1 (owner roll-up), or by MGMT_AGENT_PARTICIPANT_ID (operator roll-up)
FED_HUD_MF_PROPERTIES_OWNERS.PROPERTY_ID ➔ HOUSING__FED_HUD_MF_SECTION8_CONTRACTS.PROPERTY_ID   (overlap not yet measured)
```

**A hit means.** After folding, a short list of owners or managers holds hundreds of buildings, and their buildings show a pattern in the contract file: rents well above the local fair-market rent, or many contracts expiring in the same few years.

**A miss means.** Ownership stays flat after folding, or the big holders' contracts look like everyone else's. That would say HUD multifamily is held by many small owners, or that the real owner sits behind LLC names this file cannot link.

**Limits, said out loud.**
- `OWNER_PARTICIPANT_ID` is nearly one id per building: 22,352 ids on 23,612 properties, biggest id 21 buildings (traps 2026-09-11). Grouping on it finds no chains. 54 organization names sit on more than one id.
- The manager side shows the operator: 5,209 manager ids, biggest block 136 buildings under Michaels Management-Affordable LLC.
- Every text cell in the owner file is space-padded; blanks are a single space, not NULL. TRIM before any compare, `PROPERTY_ID` included. 37 rows carry owner id 0 with a blank name.
- `IS_NURSING_HOME_IND` is 'N' on all 23,612 rows. The other flags whose names begin with IS have no measured fill; count distinct values before using any of them.
- "Records" here means subsidy contracts and financing flags. No HUD physical-inspection score table is landed, so building condition cannot be shown. The HUD loan-commitment table names the lender, not the owner, and carries no `PROPERTY_ID`. Scope is HUD-assisted or insured buildings only, not the private rental market. `TRACS_CURRENT_EXPIRATION_DATE` has a minimum of 1900-01-02, a placeholder; bound the dates.

**The picture.** Ranked bars: x = buildings held, y = folded owner name; one bar is one owner, shaded by the share of its assisted units with rent above fair-market rent.

**First cheap check.** Count distinct TRIM(`PROPERTY_ID`) values in the owner file that also appear in the Section 8 contract table.

---

### W5 · Lenders pull out of a county after the first big storm

**The physical thing.** A storm does heavy property damage in a county. In the years after, a given bank takes fewer mortgage applications there, or stops showing up at all.

**Status.** never run

**Data grade.** B. County FIPS joins storms to mortgages and the years overlap 2015-2024, but the lender id changes from `RESPONDENT_ID` to `LEI` at 2018 and the 2018-2024 tables are unprofiled.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_NOAA_STORM_EVENTS | 1,780,730 | one storm event in one county or forecast zone | 1996-2025 (`YEAR`) | `STATE_FIPS` + `CZ_FIPS` |
| LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_HISTORIC | 44,992,667 | one mortgage application | 2015-2017 | `STATE_CODE` + `COUNTY_CODE`, `RESPONDENT_ID` |
| LIBRARY_RAW.LANDING.FED_CFPB_HMDA_LAR_2018 through FED_CFPB_HMDA_LAR_2024 (7 tables) | 124,632,830 | one mortgage application | 2018-2024 | `COUNTY_CODE`, `LEI` |
| LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_ARID2017_LEI_XREF | 5,399 | one lender's 2017 id and its later LEI | 2017-2020 | `ARID_2017` ➔ `LEI_2018` |

**Columns that carry it.**
- Storms: `YEAR` (100%), `STATE_FIPS` (100%), `CZ_FIPS` (100%), `CZ_TYPE`, `EVENT_TYPE`, `DAMAGE_PROPERTY`, `EPISODE_ID`.
- HMDA 2015-2017: `RESPONDENT_ID` (100%, 7,391 distinct), `AGENCY_CODE`, `ACTION_TAKEN`, `STATE_CODE` (98.4%), `COUNTY_CODE` (98.17%).
- HMDA 2018-2024: `LEI`, `COUNTY_CODE`, `ACTION_TAKEN`, `ACTIVITY_YEAR`. Fill rate not yet measured.
- Lender bridge: `ARID_2017`, `RESPONDENT_NAME`, `LEI_2018` (100%), `LEI_2019` (93.91%), `LEI_2020` (76.5%).

**The join, hop by hop.**
```
ENVIRONMENT__FED_NOAA_STORM_EVENTS.STATE_FIPS + CZ_FIPS (rows with CZ_TYPE = 'C') ➔ HOUSING__FED_CFPB_HMDA_HISTORIC.STATE_CODE + COUNTY_CODE   (overlap not yet measured)
same county key ➔ FED_CFPB_HMDA_LAR_2018..2024.COUNTY_CODE   (format not yet measured)
HOUSING__FED_CFPB_HMDA_HISTORIC.RESPONDENT_ID ➔ HOUSING__FED_CFPB_HMDA_ARID2017_LEI_XREF.ARID_2017 ➔ LEI_2018 ➔ FED_CFPB_HMDA_LAR_2018.LEI   (RESPONDENT_ID to ARID_2017 format unverified; bridge to the sampled LAR table measured at 84%)
```

**A hit means.** A lender active in a county before its first large-damage storm (first since 1996) files far fewer applications there in the two years after, while its volume in untouched counties of the same state holds.

**A miss means.** Lender counts and volumes per county track the state trend through the storm year. That says exit, if it happens, is not visible at county-year grain.

**Limits, said out loud.**
- Mortgage coverage is 2015-2024 only. A first storm before 2015 has no "before" lending to compare.
- `DAMAGE_PROPERTY` is text with K and M suffixes and must be parsed. Rows with `CZ_TYPE` 'Z' are forecast zones, not counties, and drop out of the join.
- The lender key breaks at 2018. The bridge table holds 5,399 lenders against 7,391 distinct `RESPONDENT_ID`s, and `RESPONDENT_ID` may need its agency code attached before it matches `ARID_2017`. HMDA 2015-2017 carries no lender name.
- HMDA codes are unpadded in 2015-2017; 2018 and 2019 carry 1,961 and 21 placeholder rows with `ACTION_TAKEN` '-1'.

**The picture.** Small multiples: x = years from the storm (-2 to +3), y = distinct lenders filing in the county; one line is one storm county.

**First cheap check.** Count counties with at least one `CZ_TYPE` 'C' storm row in 2016 that also appear as a padded `STATE_CODE`+`COUNTY_CODE` in the 2016 HMDA rows.

---

### W6 · Counties that lost doctors, banks, factories same decade

**The physical thing.** One county, ten years: the doctor's office closes, the bank branch closes, the plant closes.

**Status.** never run

**Data grade.** C. Two of the three legs now have a decade: bank branches by county 1994-2025, and Medicare-billing clinicians by office ZIP 2013-2024. The factory table is one year (2022) with a one-year change column, so the factory leg cannot show a decade of loss.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS | 2,822,977 | one bank branch in one survey year | 1994-2025 (`SURVEY_YEAR`) | `BRANCH_STATE_COUNTY_FIPS` |
| LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_DY2013 through FED_CMS_PARTB_PROVIDER_DY2024 (12 tables) | 13,528,933 | one clinician who billed Medicare Part B in one year | 2013-2024 | `NPI`, `RNDRNG_PRVDR_ZIP5` |
| LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY | 46,960 | one ZIP-area and county pair | 2020 vintage | `ZCTA5` ➔ `COUNTY_FIPS` |
| LIBRARY_RAW.LANDING.FED_CMS_NPPES_DEACTIVATED | 351,912 | one deactivated provider id and its date | not yet measured | `NPI` |
| LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_BLS_QCEW | 3,619,437 | one area, industry and ownership cell | 2022 only (`YEAR`) | `AREA_FIPS` |
| LIBRARY_RAW.LANDING.FED_BLS_QCEW | 3,619,437 | same cells, raw, with year-over-year change columns | same row count as the mart; years not yet measured | `AREA_FIPS` |

**Columns that carry it.**
- Branches: `SURVEY_YEAR` (100%), `BRANCH_STATE_COUNTY_FIPS` (100%, 3,329 distinct), `BRANCH_UNINUM`, `FDIC_CERT` (100%), `BRANCH_DEPOSITS_THOUSANDS`.
- Part B by provider: `NPI`, `RNDRNG_PRVDR_ENT_CD`, `RNDRNG_PRVDR_TYPE`, `RNDRNG_PRVDR_ZIP5`, `RNDRNG_PRVDR_STATE_FIPS`, `RNDRNG_PRVDR_RUCA`, `TOT_BENES`. Fill rate not yet measured.
- Deactivations: `NPI`, `NPPES_DEACTIVATION_DATE` (text MM/DD/YYYY). Fill rate not yet measured.
- QCEW mart: `AREA_FIPS` (100%), `INDUSTRY_CODE`, `ANNUAL_AVG_ESTABLISHMENTS`, `ANNUAL_AVG_EMPLOYMENT`, `YEAR` (2022 on every row).
- QCEW landing: `AREA_FIPS`, `INDUSTRY_CODE`, `OTY_ANNUAL_AVG_ESTABS_CHG`, `OTY_ANNUAL_AVG_EMPLVL_CHG`. Fill rate not yet measured.

**The join, hop by hop.**
```
FED_CMS_PARTB_PROVIDER_DY*.RNDRNG_PRVDR_ZIP5 ➔ XWALK_ZCTA_COUNTY.ZCTA5 ➔ COUNTY_FIPS   (overlap not yet measured)
XWALK_ZCTA_COUNTY.COUNTY_FIPS ➔ FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS.BRANCH_STATE_COUNTY_FIPS   (overlap not yet measured)
same county key ➔ ECONOMICS__FED_BLS_QCEW.AREA_FIPS   (overlap not yet measured)
FED_CMS_PARTB_PROVIDER_DY*.NPI ➔ FED_CMS_NPPES_DEACTIVATED.NPI   (optional: tells a doctor who quit from one who moved; overlap not yet measured)
```

**A hit means.** Counties where the count of distinct Medicare-billing clinicians fell from 2014 to 2024 and the branch count fell over the same years, and where 2022 factory establishments also dropped against the year before.

**A miss means.** The two ten-year declines do not land in the same counties. That would say doctor loss and bank loss follow different maps; it would say nothing about factories.

**Limits, said out loud.**
- The factory leg is one year. The QCEW mart holds 2022 only; the raw copy adds over-the-year change columns, which is one year of movement, not a decade.
- The doctor count is clinicians who appear in the Medicare Part B file, not all doctors. A pediatrician who bills no Medicare is never counted. The series changes shape at 2017 (59 columns, then 84), but the id, ZIP and type columns are in all twelve years.
- The national provider registry cannot do this job: it blanks every deactivated doctor, address included, on all 346,179 rows (traps 2026-09-05). The yearly Part B files are what place a departed doctor in a county.
- In the Part B year tables a blank is an empty string, not NULL (traps 2026-09-10).
- ZIP-area to county is uncertain where a ZIP-area crosses a county line: 10,186 of 33,791 do, and the largest-land-area pick agreed with a known county 47.1% of the time on those. Single-building ZIPs of big hospitals have no ZIP-area and drop out.

**The picture.** Scatter: x = change in branch count 2014-2024, y = change in distinct Medicare-billing clinicians 2014-2024; one dot is one county, coloured by the one-year change in factory establishments.

**First cheap check.** Count distinct `RNDRNG_PRVDR_ZIP5` values in DY2014 that match a `ZCTA5`.

---

### W7 · Single P.O. box hosts clinics, PACs, contractors

**The physical thing.** One mailing address. A medical provider, a political committee and a federal contractor all receive mail there.

**Status.** never run

**Data grade.** B. There is no shared id; the join is a cleaned address line plus 5-digit ZIP, and the contractor tables are unprofiled.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES | 9,606,683 | one provider id (NPI), person or organization | enumerated 2005-2026 | mailing address line + ZIP |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES | 60,031 | one committee in one election-cycle file | no year column | `CMTE_ST1` + `CMTE_ZIP` |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_BULK_COMMITTEES | 20,007 | one committee in one cycle | `CYCLE`, range not yet measured | `CMTE_ST1` + `CMTE_ZIP` |
| LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 through FED_USASPENDING_CONTRACTS_FY2026 (20 tables) | 96,976,021 | one contract transaction | FY2007-FY2026 | `RECIPIENT_ADDRESS_LINE_1` + `RECIPIENT_ZIP_4_CODE` |

**Columns that carry it.**
- NPPES: `NPI` (100%, unique), `PROVIDER_ORGANIZATION_NAME_LEGAL_BUSINESS_NAME`, `PROVIDER_FIRST_LINE_BUSINESS_MAILING_ADDRESS`, `PROVIDER_BUSINESS_MAILING_ADDRESS_CITY_NAME`, `PROVIDER_BUSINESS_MAILING_ADDRESS_STATE_NAME`, `PROVIDER_BUSINESS_MAILING_ADDRESS_POSTAL_CODE`. Address fill not yet measured.
- FEC committees: `CMTE_ID` (100%), `CMTE_NM`, `CMTE_ST1`, `CMTE_CITY`, `CMTE_ST`, `CMTE_ZIP` (50 blank), `CMTE_TP`.
- FEC bulk committees: `FEC_CMTE_ID` (100%), `CMTE_ST1`, `CMTE_ZIP` (9 blank), `CYCLE`.
- Contracts: `RECIPIENT_UEI`, `RECIPIENT_NAME`, `RECIPIENT_ADDRESS_LINE_1`, `RECIPIENT_CITY_NAME`, `RECIPIENT_ZIP_4_CODE`. Fill rate not yet measured.

**The join, hop by hop.**
```
cleaned(HEALTH__FED_CMS_NPPES.PROVIDER_FIRST_LINE_BUSINESS_MAILING_ADDRESS) + ZIP5 ➔ cleaned(FINANCE__FED_FEC_COMMITTEES.CMTE_ST1) + CMTE_ZIP (first 5)   (overlap not yet measured)
same address key ➔ cleaned(FED_USASPENDING_CONTRACTS_FY*.RECIPIENT_ADDRESS_LINE_1) + RECIPIENT_ZIP_4_CODE (first 5)   (overlap not yet measured)
```

**A hit means.** An address line that starts with a box number appears in all three files, under three different names, in the same ZIP.

**A miss means.** No box address reaches all three files. That would say the three worlds use different mail drops, or that address spelling differs too much for a string match.

**Limits, said out loud.**
- A shared street address is often one big institution. One hospital's address is reused as the billing address of thousands of its doctors (traps 2026-09-03). Restrict to lines that are P.O. boxes or suite-level, and read the names.
- FEC committee ids repeat across cycles with no cycle column: 60,031 rows, 38,693 ids (traps 2026-09-05). Count committees, never rows.
- No cleaned-address column exists on any table. The cleaning rule is part of the analysis and decides the result.
- The older contracts table named by the 2026-09-09 map was a 20,000,000-row cap; the year tables replace it.

**The picture.** Ranked table: one row is one address, columns are counts of distinct NPIs, committees and contractor ids at it.

**First cheap check.** Count distinct `CMTE_ST1`+`CMTE_ZIP` values starting 'PO BOX' or 'P.O. BOX' that match an NPPES mailing line in the same ZIP.

---

### W8 · Counties with one doctor per thousand and shrinking

**The physical thing.** A county with about one practicing doctor for every thousand residents, and fewer each year.

**Status.** never run

**Data grade.** C. "Shrinking" can now be counted, from twelve yearly Medicare files 2013-2024, but "per thousand" cannot be kept current: county population ends at 2015, so the ratio exists for 2013-2015 only and later years are a doctor count with no denominator. The doctors counted are Medicare billers, not all doctors.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_DY2013 through FED_CMS_PARTB_PROVIDER_DY2024 (12 tables) | 13,528,933 | one clinician who billed Medicare Part B in one year | 2013-2024 | `NPI`, `RNDRNG_PRVDR_ZIP5` |
| LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY | 46,960 | one ZIP-area and county pair | 2020 vintage | `ZCTA5` ➔ `COUNTY_FIPS` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_DRUG_POISONING_COUNTY | 53,387 | one county in one year, with its population | 1999-2015 (`YEAR`) | `FIPS` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_HPSA_PRIMARY_CARE | 79,158 | one component of one primary-care shortage designation | designated 1970-2026 | `COMMON_STATE_COUNTY_FIPS_CODE` |
| LIBRARY_RAW.LANDING.FED_CMS_NPPES_DEACTIVATED | 351,912 | one deactivated provider id and its date | not yet measured | `NPI` |

**Columns that carry it.**
- Part B by provider: `NPI`, `RNDRNG_PRVDR_ENT_CD`, `RNDRNG_PRVDR_TYPE`, `RNDRNG_PRVDR_ZIP5`, `RNDRNG_PRVDR_RUCA`, `TOT_BENES`. Fill rate not yet measured.
- CDC county file: `FIPS` (100%, 3,149 distinct), `YEAR` (100%), `POPULATION`.
- Shortage areas: `COMMON_STATE_COUNTY_FIPS_CODE` (100%, 3,268 distinct), `DESIGNATION_DATE` (100%), `WITHDRAWN_DATE` (61.28%), `HPSA_STATUS`, `HPSA_FTE`, `DESIGNATION_POPULATION`, `FORMAL_RATIO`, `RURAL_STATUS`.
- Deactivations: `NPI`, `NPPES_DEACTIVATION_DATE`. Fill rate not yet measured.

**The join, hop by hop.**
```
FED_CMS_PARTB_PROVIDER_DY*.RNDRNG_PRVDR_ZIP5 ➔ XWALK_ZCTA_COUNTY.ZCTA5 ➔ COUNTY_FIPS   (overlap not yet measured)
XWALK_ZCTA_COUNTY.COUNTY_FIPS ➔ HEALTH__FED_CDC_DRUG_POISONING_COUNTY.FIPS (years 2013-2015)   (overlap not yet measured)
XWALK_ZCTA_COUNTY.COUNTY_FIPS ➔ HEALTH__FED_HRSA_HPSA_PRIMARY_CARE.COMMON_STATE_COUNTY_FIPS_CODE   (overlap not yet measured)
```

**A hit means.** Counties at or under one Medicare-billing physician per 1,000 residents in 2015 whose physician count then kept falling through 2024, most of them holding a shortage designation never withdrawn.

**A miss means.** Low-ratio counties held steady or grew after 2015. That would say thin counties are thin but stable, at least among doctors who bill Medicare.

**Limits, said out loud.**
- County population ends at 2015. After that the ratio has no denominator; a falling doctor count in a county losing people faster is not a worsening ratio, and this data cannot tell the two apart.
- The count is clinicians in the Medicare Part B file, not all doctors. `RNDRNG_PRVDR_TYPE` must be read to keep physicians and drop nurse practitioners, labs and suppliers; its values are not yet measured.
- The national provider registry cannot show decline: it blanks every deactivated doctor, address included, on all 346,179 rows. The deactivation file adds the exit date only.
- The shortage-ratio columns were wiped once by a numeric cast keyed on the column name; the raw value is text like "3500:1" (traps 2026-09-07). Read `FORMAL_RATIO` values before trusting them.
- In the Part B year tables a blank is an empty string, not NULL. ZIP-area to county is a coin flip on the 10,186 ZIP-areas that cross a county line (47.1% agreement).

**The picture.** Slope chart: x = 2015 and 2024, y = Medicare-billing physicians in the county; one line is one county that sat at or under one per 1,000 in 2015.

**First cheap check.** Count distinct `NPI` in DY2015, grouped by `RNDRNG_PRVDR_ENT_CD`, whose `RNDRNG_PRVDR_ZIP5` matches a `ZCTA5`.

---

### W9 · Rural clinics close where the only bank branch closed

**The physical thing.** A rural county's last bank branch drops out of the FDIC survey. In the same county, a Medicare-certified clinic's participation ends.

**Status.** never run

**Data grade.** B. Both sides carry county FIPS and both are profiled, but the clinic file keeps only each facility's latest record, and the code that marks a rural health clinic has not been looked up.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER | 44,429 | one Medicare-certified non-hospital facility, latest record | terminations 1963-2026 (`TRMNTN_EXPRTN_DT`) | `FIPS_STATE_CD` + `FIPS_CNTY_CD` |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS | 2,822,977 | one bank branch in one survey year | 1994-2025 (`SURVEY_YEAR`) | `BRANCH_STATE_COUNTY_FIPS` |

**Columns that carry it.**
- Facilities: `CCN` (100%), `PRVDR_CTGRY_CD`, `PRVDR_CTGRY_SBTYP_CD`, `FAC_NAME`, `CBSA_URBN_RRL_IND`, `TRMNTN_EXPRTN_DT` (40.92%), `PGM_TRMNTN_CD`, `FIPS_STATE_CD` (316 blank), `FIPS_CNTY_CD` (99.29%, a number, unpadded).
- Branches: `SURVEY_YEAR` (100%), `BRANCH_STATE_COUNTY_FIPS` (100%, 3,329 distinct), `BRANCH_UNINUM`, `FDIC_CERT` (100%), `BRANCH_NAME`.

**The join, hop by hop.**
```
HEALTH__FED_CMS_POS_OTHER.FIPS_STATE_CD + FIPS_CNTY_CD (left-padded to 3) ➔ FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS.BRANCH_STATE_COUNTY_FIPS   (overlap not yet measured)
```

**A hit means.** Counties that fell from one branch to zero show a clinic termination within a few years more often than rural counties that kept their one branch.

**A miss means.** Clinic terminations are no more common in counties that lost their last branch. That would say the two closures do not travel together at county scale.

**Limits, said out loud.**
- The facility file keeps only the latest record per `CCN`. A clinic that closed and reopened under the same number shows one state.
- `TRMNTN_EXPRTN_DT` is a termination-or-expiration date. `PGM_TRMNTN_CD` must be read to separate a closed door from a merger or a paperwork lapse; its values are not yet measured.
- Which `PRVDR_CTGRY_CD` value means rural health clinic is not yet measured. No category in this file is a nursing home.
- `CHOW_SW` is blank on all 44,429 rows; ownership change cannot be used as a control.
- A branch missing from the next survey year can be a merger or renumbering.

**The picture.** Timeline dots: x = year, one row per county; a square marks the last branch leaving, a circle marks a clinic termination.

**First cheap check.** Count county-years in the branch table with exactly one `BRANCH_UNINUM`, then count how many have zero the next year.

---

### W10 · Rural counties send most to DC, get least back

**The physical thing.** Federal income tax paid by a county's residents, set against the federal grants, loans and contracts performed in that county.

**Status.** never run

**Data grade.** B. It works for one year only: the tax file holds tax year 2016 and is keyed on ZIP, so it needs the ZIP-area to county bridge; the 40 spending tables are unprofiled and no rural flag is county-native.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS_SOI | 179,796 | one ZIP in one income bracket | 2016 only (`TAX_YEAR`) | `ZIP_CODE` |
| LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY | 46,960 | one ZIP-area and county pair | 2020 vintage | `ZCTA5` ➔ `COUNTY_FIPS` |
| LIBRARY_RAW.LANDING.FED_USASPENDING_ASSISTANCE_FY2007 through FED_USASPENDING_ASSISTANCE_FY2026 (20 tables) | 128,155,142 | one grant, loan or direct-payment transaction | FY2007-FY2026 | `PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE` |
| LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 through FED_USASPENDING_CONTRACTS_FY2026 (20 tables) | 96,976,021 | one contract transaction | FY2007-FY2026 | `PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE` |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS | 2,822,977 | one bank branch in one survey year | 1994-2025 | `BRANCH_STATE_COUNTY_FIPS` (borrowed metro flag) |

**Columns that carry it.**
- Tax file: `ZIP_CODE` (100%, 29,922 distinct), `AGI_STUB`, `TOTAL_TAX`, `AGI`, `N_RETURNS`, `TAX_YEAR` (2016 on every row). `AGI` and `N_RETURNS` are text.
- Bridge: `ZCTA5`, `COUNTY_FIPS` (100%, 3,266 distinct), `XWALK_TYPE`.
- Assistance: `FEDERAL_ACTION_OBLIGATION`, `FACE_VALUE_OF_LOAN`, `ASSISTANCE_TYPE_CODE`, `ACTION_DATE_FISCAL_YEAR`, the place-of-performance county FIPS column. Fill rate not yet measured by the fact helper; the traps log puts county FIPS at 71% in FY2007 to 99% in FY2020.
- Contracts: `FEDERAL_ACTION_OBLIGATION`, `ACTION_DATE_FISCAL_YEAR`, the place-of-performance county FIPS column (93% filled, 2,894 distinct counties, on FY2024).
- Branches: `BRANCH_METRO_FLAG`, `BRANCH_MICRO_FLAG`. Fill rate not yet measured.

**The join, hop by hop.**
```
FINANCE__FED_IRS_SOI.ZIP_CODE ➔ XWALK_ZCTA_COUNTY.ZCTA5 ➔ COUNTY_FIPS   (overlap not yet measured)
XWALK_ZCTA_COUNTY.COUNTY_FIPS ➔ FED_USASPENDING_ASSISTANCE_FY2016.PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE   (overlap not yet measured)
XWALK_ZCTA_COUNTY.COUNTY_FIPS ➔ FED_USASPENDING_CONTRACTS_FY2016.PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE   (overlap not yet measured)
XWALK_ZCTA_COUNTY.COUNTY_FIPS ➔ FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS.BRANCH_STATE_COUNTY_FIPS   (rural proxy; overlap not yet measured)
```

**A hit means.** Non-metro counties show a lower ratio of federal dollars received to income tax paid in 2016 than metro counties do.

**A miss means.** The ratio is flat or runs the other way. That would say rural counties get back as much or more per tax dollar, for that one year.

**Limits, said out loud.**
- One tax year, 2016. There is no trend.
- The bridge is ZIP-area, not postal ZIP, and 10,186 of 33,791 ZIP-areas cross a county line. A ZIP's tax has to be split or assigned, and either choice moves the county total.
- Loans carry no obligation: assistance types 07 and 08 sum `FEDERAL_ACTION_OBLIGATION` to $0.00 on 11,788,945 rows; the money is in `FACE_VALUE_OF_LOAN`. Decide loans in or out before summing.
- Obligations are signed. De-obligations are negative rows and belong in the sum.
- Spending is placed where the work is performed, not where the recipient lives. Payments to individuals, such as Social Security, are not in these files, so "get back" is grants, loans and contracts only.

**The picture.** Scatter, log axes: x = 2016 income tax paid by county, y = FY2016 federal obligations performed in county; one dot is one county, coloured metro or non-metro.

**First cheap check.** Count distinct `ZIP_CODE` values in the tax file that match a `ZCTA5`.

---

### W11 · Rural water systems violate more per capita than urban

**The physical thing.** A public water system and the people it serves. Count its violations, divide by the population on its pipes, and compare small country systems with city ones.

**Status.** never run

**Data grade.** B. The water system id joins all three tables and all are profiled, but no table carries a rural flag, so "rural" is a proxy: population served, or a flag borrowed by county.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS | 434,040 | one public water system | first reported 1979-2026 | `PWSID` |
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT | 15,432,737 | one violation with its enforcement fields | to 2026-06-09 (minimum 1900-01-01 is a placeholder) | `PWSID` |
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS | 578,198 | one area served by one water system | 1995-2026 | `PWSID`, `COUNTY_FIPS` |

**Columns that carry it.**
- Systems: `PWSID` (100%), `POPULATION_SERVED_COUNT`, `POP_CAT_5_CODE`, `PWS_TYPE_CODE`, `PWS_ACTIVITY_CODE`, `OWNER_TYPE_CODE`, `SERVICE_CONNECTIONS_COUNT`. Fill on the non-key columns not yet measured.
- Violations: `PWSID` (100%, 265,738 distinct), `VIOLATION_ID`, `IS_HEALTH_BASED_IND`, `VIOLATION_CATEGORY_CODE`, `NON_COMPL_PER_BEGIN_DATE` (93.5%).
- Areas: `PWSID` (100%), `AREA_TYPE_CODE`, `COUNTY_SERVED`, `COUNTY_FIPS` (404,823 of 405,396 named county rows).

**The join, hop by hop.**
```
ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT.PWSID ➔ ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS.PWSID   (direct overlap not yet measured; each side matches the SDWA facilities table at 100%)
ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS.PWSID ➔ ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS.PWSID ➔ COUNTY_FIPS   (only if a county-level rural flag is borrowed)
```

**A hit means.** Active community systems in the smallest population bands carry more distinct violations per 1,000 people served than systems in the largest bands, and the gap holds for health-based violations alone.

**A miss means.** The rate is flat across bands, or the gap vanishes once monitoring and paperwork violations are set aside. That would say small systems miss reports, not that their water is worse.

**Limits, said out loud.**
- No rural or urban flag exists on any of the three tables. Population served is a size proxy, not a rural measure.
- Count distinct `VIOLATION_ID`, never rows. The row grain of the violations table has not been measured and one violation may repeat per enforcement action.
- Dividing by population makes tiny systems look extreme: one violation at a 25-person system is a large rate. Band the systems; do not rank them.
- 6,255 county-type rows have a blank county name, 4,262 of them in New Jersey and 581 in Florida. Water system ids starting 04 to 10 are EPA regions and never match a state.
- The date columns carry 1900-01-01 placeholders; bound every date filter.

**The picture.** Bars: x = population-served band, y = distinct health-based violations per 1,000 people served; one bar is one band.

**First cheap check.** Count distinct `PWSID` in the violations table that also exist in the water systems table.

---

### W12 · Mine closed, overdoses rose within three years

**The physical thing.** A mine's status flips to abandoned in a given year. The county's overdose death rate over the next three years.

**Status.** never run

**Data grade.** B. County FIPS can be built on the mine side and both sides are profiled, but each mine shows only its current status, and the overdose data is two files with a hole at 2016-2018.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES | 91,906 | one mine, current status | status dates 1925-2026 (`CURRENT_STATUS_DT`) | `STATE` + `FIPS_CNTY_CD` |
| LIBRARY_MARTS.REFERENCE.REF__DIM_STATE | 56 | one state or territory | no year | `STATE_ABBR` ➔ `STATE_FIPS` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_DRUG_POISONING_COUNTY | 53,387 | one county in one year | 1999-2015 (`YEAR`) | `FIPS` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY | 132,000 | one county, one cause, one period | 2019-2024 (traps log) | `GEOID` |

**Columns that carry it.**
- Mines: `MINE_ID` (100%), `CURRENT_MINE_STATUS`, `CURRENT_STATUS_DT` (100%), `COAL_METAL_IND`, `NO_EMPLOYEES`, `STATE`, `FIPS_CNTY_CD` (100%, 298 distinct).
- States: `STATE_ABBR`, `STATE_FIPS` (100%).
- CDC 1999-2015: `FIPS` (100%), `YEAR` (100%), `POPULATION`, `ESTIMATED_AGE_ADJUSTED_DEATH_RATE_11_CATEGORIES_IN_RANGES`.
- CDC 2019-2024: `GEOID` (100%, 3,153 distinct), `INTENT`, `PERIOD`, `RATE`, `RATE_M`, `COUNT_SUP`, `TTM_DATE_RANGE`.

**The join, hop by hop.**
```
LABOR__FED_MSHA_MINES.STATE ➔ REF__DIM_STATE.STATE_ABBR ➔ STATE_FIPS
STATE_FIPS + LABOR__FED_MSHA_MINES.FIPS_CNTY_CD (left-padded to 3) ➔ HEALTH__FED_CDC_DRUG_POISONING_COUNTY.FIPS   (overlap not yet measured)
same 5-digit key ➔ HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY.GEOID   (overlap not yet measured; the two CDC files match each other on county at 100%)
```

**A hit means.** Counties where a mine with a real workforce closed show overdose rates climbing faster over the next three years than same-state mining counties with no closure in that window.

**A miss means.** Closure counties track their neighbors. That would say the closure year does not mark a turn in overdose deaths at county scale.

**Limits, said out loud.**
- The mines table holds current status and its date only: one closure per mine, no history. A mine that closed, reopened and closed again shows the last date.
- 1999-2015 rates are one of 11 ranges, not numbers. A rise inside one range is invisible.
- No overdose data is landed for 2016-2018. Closures in 2013-2018 have no clean three-year "after". Usable windows: closures 1999-2012 on ranges, closures 2019-2021 on numeric rates.
- In the 2019-2024 file, `RATE` -999 is a placeholder, `RATE_M` is a text flag, and small counts are suppressed (`COUNT_SUP`).
- `NO_EMPLOYEES` is null on 39,735 of 91,906 mines, so "a closure that mattered" cannot be sized for those mines.

**The picture.** Event-study lines: x = years from closure (-3 to +3), y = county overdose rate; one line is closure counties, one is matched mining counties.

**First cheap check.** Count distinct state-plus-county keys built from the mines table that match a `GEOID` in the 2019-2024 CDC file.

---

### W13 · Counties host most plants, get least federal money

**The physical thing.** Power plants standing in a county, counted and sized. Federal grant and loan dollars performed in the same county.

**Status.** never run

**Data grade.** B. County FIPS is on both sides and the years overlap 2019-2023, but four of the five plant tables and all the money tables are unprofiled, and no county population after 2015 is landed for a per-person version.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_EGRID_PLANT_2022 | 11,974 | one power plant | 2022 | `PLANT_FIPS_STATE_CODE` + `PLANT_FIPS_COUNTY_CODE` |
| LIBRARY_RAW.LANDING.FED_EPA_EGRID_PLANT_2019 | 11,865 | one power plant | 2019 | `FIPSST` + `FIPSCNTY` |
| LIBRARY_RAW.LANDING.FED_EPA_EGRID_PLANT_2020 | 12,668 | one power plant | 2020 | same |
| LIBRARY_RAW.LANDING.FED_EPA_EGRID_PLANT_2021 | 11,393 | one power plant | 2021 | same |
| LIBRARY_RAW.LANDING.FED_EPA_EGRID_PLANT_2023 | 12,612 | one power plant | 2023 | same |
| LIBRARY_RAW.LANDING.FED_USASPENDING_ASSISTANCE_FY2007 through FED_USASPENDING_ASSISTANCE_FY2026 (20 tables) | 128,155,142 | one grant, loan or direct-payment transaction | FY2007-FY2026 | `PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE` |

**Columns that carry it.**
- Plants 2022: `DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE`, `PLANT_FIPS_STATE_CODE` (100%), `PLANT_FIPS_COUNTY_CODE` (99.71%), `PLANT_PRIMARY_FUEL_CATEGORY`, `PLANT_NAMEPLATE_CAPACITY_MW` (text), `PLANT_ANNUAL_NOX_EMISSIONS_TONS`.
- Plants 2019-2021 and 2023: `ORISPL`, `FIPSST`, `FIPSCNTY`, `PLFUELCT`, `NAMEPCAP`, `PLNOXAN`. Fill rate not yet measured.
- Assistance: `FEDERAL_ACTION_OBLIGATION`, `FACE_VALUE_OF_LOAN`, `ASSISTANCE_TYPE_CODE`, `ACTION_DATE_FISCAL_YEAR`, the place-of-performance county FIPS column (71% filled in FY2007 to 99% in FY2020, traps log).

**The join, hop by hop.**
```
ENVIRONMENT__FED_EPA_EGRID_PLANT_2022.PLANT_FIPS_STATE_CODE + PLANT_FIPS_COUNTY_CODE ➔ FED_USASPENDING_ASSISTANCE_FY2022.PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE   (overlap not yet measured)
FED_EPA_EGRID_PLANT_2019/2020/2021/2023.FIPSST + FIPSCNTY ➔ the same column on the matching fiscal-year table   (overlap not yet measured)
```

**A hit means.** Counties in the top tenth by plant capacity sit in the bottom half by assistance dollars, year after year.

**A miss means.** Plant-heavy counties get average or above-average dollars. That would say hosting generation does not go with being passed over.

**Limits, said out loud.**
- Without a current population table, a big plant-heavy county and a small one cannot be put on a per-person footing. County population ends 2015.
- The 2022 table uses long caption column names; the other four years use short codes. A five-year union needs a hand-written column map.
- Capacity is text in the 2022 mart and must be cast. eGRID revises its files: 2020 is version 2, 2023 is revision 2.
- Loans carry $0.00 in `FEDERAL_ACTION_OBLIGATION` on 11,788,945 rows; the money is in `FACE_VALUE_OF_LOAN`.
- The older assistance table was capped at 1M rows a year and read 5x to 25x low. Use the year tables only.

**The picture.** Scatter: x = plant capacity in county (MW), y = assistance dollars performed in county that fiscal year; one dot is one county.

**First cheap check.** Count distinct 5-digit county keys in the 2022 plant mart that appear in the FY2022 assistance table.

---

### W15 · High-hazard dams within ten miles of a nursing home

**The physical thing.** A dam rated high hazard, meaning people would likely die if it failed. A nursing home full of people who cannot leave fast, inside a ten-mile circle around it.

**Status.** never run

**Data grade.** B. Both tables are profiled and both carry latitude and longitude, but there is no shared id; the join is straight-line distance, and coordinate fill is not yet measured on either side.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_NID_DAMS | 92,766 | one dam | snapshot, updated 2015-2026 (`DATA_LAST_UPDATED`) | `LATITUDE`, `LONGITUDE` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME | 14,700 | one nursing home | snapshot, no year column | `LATITUDE`, `LONGITUDE` |

**Columns that carry it.**
- Dams: `NID_ID`, `DAM_NAME`, `HAZARD_POTENTIAL`, `CONDITION_ASSESSMENT`, `CONDITION_ASSESSMENT_DATE` (43.84%), `LAST_INSPECTION_DATE` (62.71%), `HAS_EMERGENCY_ACTION_PLAN`, `NID_STORAGE_ACRE_FT`, `LATITUDE`, `LONGITUDE`, `STATE`. Coordinate fill not yet measured.
- Nursing homes: `CMS_CERTIFICATION_NUMBER_CCN` (100%), `PROVIDER_NAME`, `NUMBER_OF_CERTIFIED_BEDS`, `AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY`, `LATITUDE`, `LONGITUDE`, `GEOCODING_FOOTNOTE`. Coordinate fill not yet measured.

**The join, hop by hop.**
```
ENVIRONMENT__FED_NID_DAMS.LATITUDE, LONGITUDE ➔ HEALTH__FED_CMS_NURSING_HOME.LATITUDE, LONGITUDE   (distance under 10 miles; pair count not yet measured)
```

**A hit means.** A list of high-hazard dams, rated poor or never assessed, each with one or more nursing homes and a bed count inside ten miles.

**A miss means.** Few or no pairs. That would say high-hazard dams and nursing homes rarely sit close, or that coordinates are missing on too many rows to tell.

**Limits, said out loud.**
- Ten miles is a circle, not a flood path. The data has no flow direction and no elevation, so a home uphill of the dam counts the same as one below it.
- Condition is thin: `CONDITION_ASSESSMENT_DATE` is filled on 43.84% of dams. A dam with no rating is unknown, not safe.
- `LAST_INSPECTION_DATE` runs to the year 5023 and `YEAR_COMPLETED` has zeros. Bound dates before using them.
- The nursing-home `COUNTY_FIPS` column is blank on all 14,700 rows; distance is the only way in. The HUD property file named for this row in the tables list adds nothing: its nursing-home flag is 'N' on all 23,612 rows.
- No school table is landed, which is why schools left the wording.

**The picture.** Map: one red triangle is one high-hazard dam, one dot is one nursing home within ten miles, dot size is certified beds.

**First cheap check.** Count dams by `HAZARD_POTENTIAL` value with non-null `LATITUDE`, and nursing homes with non-null `LATITUDE`.

---

### W16 · Fracking counties see water violations climb after boom

**The physical thing.** Hydraulic fracturing jobs disclosed well by well in a county. Drinking-water violations at the public water systems serving that same county, before and after the wells arrived.

**Status.** never run

**Data grade.** B. The water side now carries county FIPS, but the fracking side has only state and county names, so one hop is a name join, and the fracking date range is not yet measured.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_FRACFOCUS_DISCLOSURE_LIST | 248,835 | one fracturing job disclosure at one well | not yet measured (`JOB_START_DATE`) | `STATE_NAME` + `COUNTY_NAME` |
| LIBRARY_MARTS.REFERENCE.REF__DIM_STATE | 56 | one state or territory | no year | `STATE_NAME` ➔ `STATE_FIPS` |
| LIBRARY_RAW.LANDING.FED_CENSUS_COUNTY_2020 | 3,235 | one county | 2020 | `STATEFP` + `COUNTYNAME` ➔ `COUNTYFP` |
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS | 578,198 | one area served by one water system | 1995-2026 | `COUNTY_FIPS`, `PWSID` |
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT | 15,432,737 | one violation with its enforcement fields | to 2026-06-09 | `PWSID` |

**Columns that carry it.**
- Fracking: `DISCLOSURE_ID`, `API_NUMBER`, `STATE_NAME`, `COUNTY_NAME`, `JOB_START_DATE`, `TOTAL_BASE_WATER_VOLUME`, `LATITUDE`, `LONGITUDE`, `OPERATOR_NAME`. Fill rate not yet measured.
- States: `STATE_NAME`, `STATE_FIPS` (100%).
- Counties: `STATEFP`, `COUNTYFP`, `COUNTYNAME`. Fill rate not yet measured; the phase 5 report verified 3,235 unique FIPS.
- Water areas: `PWSID` (100%), `COUNTY_FIPS` (404,823 of 405,396 named county rows).
- Violations: `PWSID` (100%), `VIOLATION_ID`, `CONTAMINANT_CODE`, `IS_HEALTH_BASED_IND`, `NON_COMPL_PER_BEGIN_DATE` (93.5%).

**The join, hop by hop.**
```
ENVIRONMENT__FED_FRACFOCUS_DISCLOSURE_LIST.STATE_NAME ➔ REF__DIM_STATE.STATE_NAME ➔ STATE_FIPS
STATE_FIPS + folded COUNTY_NAME ➔ FED_CENSUS_COUNTY_2020.STATEFP + folded COUNTYNAME ➔ STATEFP + COUNTYFP   (name join; match rate not yet measured)
STATEFP + COUNTYFP ➔ ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS.COUNTY_FIPS ➔ PWSID
ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS.PWSID ➔ ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT.PWSID
```

**A hit means.** In counties where yearly disclosures jump from near zero, distinct violations per water system rise in the following years, faster than in same-state counties with no wells.

**A miss means.** Violation rates in drilling counties follow the state line. That would say public systems' reported violations did not move with drilling, which is not the same as saying private wells were unaffected.

**Limits, said out loud.**
- County names must be folded the same way on both sides: suffix stripped, St. and Saint made equal, independent cities kept apart. Bare county names with no " County" suffix slip past simple filters.
- FracFocus is operator self-disclosure and its start year is not yet measured. A boom that began before disclosure began has no "before".
- Public water systems are what EPA tracks. Private household wells, the ones nearest to drilling, are not in any landed table.
- Count distinct `VIOLATION_ID`, never rows; bound dates to drop the 1900-01-01 placeholders. 6,255 county-type water rows have a blank county name.

**The picture.** Event-study lines: x = years from the county's first boom year, y = distinct violations per water system; one line is drilling counties, one is same-state others.

**First cheap check.** Count distinct `STATE_NAME`+`COUNTY_NAME` pairs in the fracking table that resolve to a county FIPS through the Census county file.

---

### W18 · Water systems violate yearly, never enforced

**The physical thing.** One public water system with a violation on the books every year for years, and no enforcement action ever recorded against it.

**Status.** never run

**Data grade.** A. One shared id, `PWSID`, filled 100% on both profiled tables, with violation dates running to 2026; the one thing to check first is whether an empty enforcement field is a true blank.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT | 15,432,737 | one violation with its enforcement fields | to 2026-06-09 (`NON_COMPL_PER_BEGIN_DATE`; minimum 1900-01-01 is a placeholder) | `PWSID` |
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS | 434,040 | one public water system | first reported 1979-2026 | `PWSID` |

**Columns that carry it.**
- Violations: `PWSID` (100%, 265,738 distinct), `VIOLATION_ID`, `IS_HEALTH_BASED_IND`, `VIOLATION_STATUS`, `NON_COMPL_PER_BEGIN_DATE` (93.5%), `ENFORCEMENT_ID`, `ENFORCEMENT_DATE`, `ENFORCEMENT_ACTION_TYPE_CODE`, `ENF_ACTION_CATEGORY`. Fill on the four enforcement columns not yet measured.
- Systems: `PWSID` (100%), `PWS_NAME`, `POPULATION_SERVED_COUNT`, `OWNER_TYPE_CODE`, `PRIMACY_AGENCY_CODE`, `PWS_ACTIVITY_CODE`, `STATE_CODE` (96.67%).

**The join, hop by hop.**
```
ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT.PWSID ➔ ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS.PWSID   (direct overlap not yet measured; each side matches the SDWA facilities table at 100%)
group by PWSID: distinct years of NON_COMPL_PER_BEGIN_DATE, count of non-blank ENFORCEMENT_ID
```

**A hit means.** A list of active systems with a violation in five or more separate years and zero enforcement records, each with a name, a state and a population served.

**A miss means.** Every repeat violator has at least one enforcement record. That would say the enforcement trail is complete, or that informal notices are logged as enforcement.

**Limits, said out loud.**
- "Never enforced" rests on `ENFORCEMENT_ID` being empty, and its fill is not yet measured. This warehouse has text columns that hold empty strings, not NULLs; test both before counting.
- Enforcement categories include informal actions. A reminder letter counts as enforced unless `ENF_ACTION_CATEGORY` is split.
- The row grain is not yet measured. Count distinct `VIOLATION_ID` per year, never rows.
- Date columns carry 1900-01-01 placeholders and `NON_COMPL_PER_BEGIN_DATE` is filled on 93.5% of rows; the rest cannot be placed in a year.
- 67.07% of systems carry a deactivation date. Filter to active systems, or the list fills with systems that no longer exist.

**The picture.** Ranked strip chart: one row is one water system, one tick is one year with a violation, ordered by population served.

**First cheap check.** Count rows where `ENFORCEMENT_ID` is NULL, where it is an empty string, and where it is filled.

---

### W23 · Where coal plants closed, respiratory claims fell

**The physical thing.** A coal-fired generator is retired. In the years after, Medicare patients seen by doctors near the plant carry fewer lung-disease diagnoses.

**Status.** never run

**Data grade.** C. Retirements 2019-2023 and a yearly Medicare file 2017-2024 now give a before and after, but the measure is a proxy: the share of a doctor's patients with COPD or asthma, placed by the doctor's office ZIP, not respiratory claims placed where patients live; every table in the chain but one is unprofiled.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_RAW.LANDING.FED_EIA860_GENERATOR_Y2019 through FED_EIA860_GENERATOR_Y2023 (5 tables) | 156,087 | one generator on one sheet (operable, proposed, retired) | 2019-2023 | `PLANT_CODE` |
| LIBRARY_RAW.LANDING.FED_EIA860_PLANT_Y2019 through FED_EIA860_PLANT_Y2023 (5 tables) | 67,231 | one power plant | 2019-2023 | `PLANT_CODE`, `ZIP` |
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_EGRID_PLANT_2022 | 11,974 | one power plant | 2022 | `DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE`, county FIPS |
| LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_DY2017 through FED_CMS_PARTB_PROVIDER_DY2024 (8 tables) | 9,512,690 | one clinician's Medicare Part B year | 2017-2024 | `RNDRNG_PRVDR_ZIP5`, `NPI` |
| LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_DY2013 through FED_CMS_PARTB_PROVIDER_DY2016 (4 tables) | 4,016,243 | same, older 59-column layout | 2013-2016 | not usable here: no lung-disease columns |

**Columns that carry it.**
- Generators 2019-2023: `SHEET_NAME`, `PLANT_CODE`, `GENERATOR_ID`, `ENERGY_SOURCE_1`, `STATUS`, `NAMEPLATE_CAPACITY_MW`, `RETIREMENT_YEAR`, `RETIREMENT_MONTH`. Fill rate not yet measured.
- Plants 2019-2023: `PLANT_CODE`, `ZIP`, `COUNTY`, `STATE`, `LATITUDE`, `LONGITUDE`. Fill rate not yet measured.
- eGRID 2022: `DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE`, `PLANT_FIPS_STATE_CODE` (100%), `PLANT_FIPS_COUNTY_CODE` (99.71%), `PLANT_ANNUAL_COAL_NET_GENERATION_MWH`.
- Part B by provider, DY2017-DY2024: `NPI`, `RNDRNG_PRVDR_ZIP5`, `RNDRNG_PRVDR_STATE_FIPS`, `RNDRNG_PRVDR_RUCA`, `TOT_BENES`, `BENE_AVG_AGE`, `BENE_AVG_RISK_SCRE`, `BENE_CC_PH_COPD_V2_PCT`, `BENE_CC_PH_ASTHMA_V2_PCT`. Fill rate not yet measured on any of them.

**The join, hop by hop.**
```
FED_EIA860_GENERATOR_Y*.PLANT_CODE ➔ FED_EIA860_PLANT_Y*.PLANT_CODE (same year)   (overlap not yet measured)
FED_EIA860_PLANT_Y*.ZIP ➔ FED_CMS_PARTB_PROVIDER_DY2017..DY2024.RNDRNG_PRVDR_ZIP5   (overlap not yet measured; ZIP places a doctor's office, not a patient's home)
FED_EIA860_PLANT_Y*.PLANT_CODE ➔ ENVIRONMENT__FED_EPA_EGRID_PLANT_2022.DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE ➔ county FIPS   (optional county version; overlap not yet measured)
```

**A hit means.** Around plants whose coal units retired in 2019-2023, the patient-weighted COPD share among nearby clinicians drops in the years after retirement, more than it does around plants that kept burning coal over the same years.

**A miss means.** The two groups move together. That would say a retirement leaves no mark on this measure within one to five years, which fits a slow disease as easily as it fits no effect.

**Limits, said out loud.**
- The measure is not claims. `BENE_CC_PH_COPD_V2_PCT` is the share of a clinician's Medicare patients flagged with COPD, a chronic label that does not clear when the air does. The by-service Part B family could count respiratory procedures, but it is a suppressed subset: rows under 11 beneficiaries are deleted (traps log).
- The lung columns exist only from DY2017. The series changes shape at 2017, 59 columns before and 84 after, so DY2013-DY2016 cannot serve as "before". A 2019 retirement has two before-years; a 2023 retirement has one after-year.
- In these twelve tables a blank is an empty string, not NULL (traps 2026-09-10). `IS NULL` finds nothing; use NULLIF(col, '') before averaging, or blanks break the cast. How often the lung columns are blank is not yet measured; CMS blanks small patient counts.
- Office ZIP is not where patients breathe, and ZIP identifies nothing on its own. Clinicians move and retire between years, so the group near a plant is not the same people each year.
- Each generator table unions three sheets. Footer rows land with every field NULL but `SHEET_NAME` on 12 of 15 sheet-years; filter `PLANT_CODE` is not null. `PLANT_CODE` repeats and is not a row key. A plant retired before 2019 appears in none of these tables.

**The picture.** Event-study lines: x = years from retirement (-2 to +4), y = patient-weighted COPD share among clinicians in the plant's ZIP; one line is retired-coal plants, one is still-burning plants.

**First cheap check.** Count distinct `PLANT_CODE` on the retired sheet with a coal `ENERGY_SOURCE_1` and `RETIREMENT_YEAR` 2019-2023 whose plant `ZIP` matches at least one `RNDRNG_PRVDR_ZIP5` in DY2018.

---

### P-081 · More-minority communities get inspected less

**The physical thing.** An EPA-regulated facility out of compliance. How many times an inspector has visited it, set against the minority share of the people living around it.

**Status.** measured on 2026-08-22: inspections per facility fall from 2.90 in the whitest tenth of communities to 1.46 in the most-minority tenth (book row P-081, extract row WN-130; run date from `reports/wonder_rankings.md`)

**Data grade.** B. One profiled table answers it and the number is already measured, but 32% of facilities have no minority share and the counts are one snapshot with no stated time window.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__EPA_PENALTY_GAP | 93,808 | one EPA-registered facility with its compliance, inspection and penalty counts | snapshot; last inspections 1978-2026 (`DATE_LAST_INSPECTION`) | `PCT_MINORITY` (grouping) |

**Columns that carry it.**
- `FRS_ID` (100%), `PCT_MINORITY` (missing on 29,702 rows, 32%), `TOTAL_INSPECTION_COUNT`, `QUARTERS_WITH_NONCOMPLIANCE`, `FORMAL_ACTION_COUNT`, `TOTAL_PENALTIES`, `CHRONIC_NO_PENALTY`, `NEVER_INSPECTED_NONCOMPLIANT`, `IN_MAJORITY_MINORITY_COMMUNITY`, `POPULATION_DENSITY`, `STATE`, `DATE_LAST_INSPECTION` (55.96%), `HAS_AIR_PROGRAM`, `HAS_WATER_PROGRAM`, `HAS_HAZWASTE_PROGRAM`.

**The join, hop by hop.**
```
one table, no join
cut PCT_MINORITY into ten equal groups; average TOTAL_INSPECTION_COUNT and QUARTERS_WITH_NONCOMPLIANCE per group
```

**A hit means.** Already seen: inspections fall 2.90 to 1.46 from the whitest to the most-minority tenth, while quarters out of compliance rise 8.24 to 8.85. The open test is whether the slope survives holding state, program type and population density fixed.

**A miss means.** The slope flattens once state and program are held fixed. That would say the gap is about which states and which kinds of facility sit in minority areas, not about inspectors' choices inside a state.

**Limits, said out loud.**
- 29,702 of 93,808 facilities (32%) have no `PCT_MINORITY`; 5,653 have no location. The result describes only the facilities that have both.
- Penalty dollars run the other way: higher in high-minority groups. The finding is about inspections, not fines.
- 86,963 facilities (92.7%) have zero penalties and 53,587 (57.1%) were never inspected while out of compliance, so the averages sit on a mass of zeros.
- The counts are totals in one snapshot; the period they cover is not yet measured. `DATE_LAST_INSPECTION` is empty on 44% of rows. No trend over time can be drawn.
- The table is a built mart of facilities with a compliance record, not every EPA site. How it was filtered is not in the sources, so the base population is "not yet measured".

**The picture.** Line with points: x = minority-share tenth (1 to 10), y = mean inspections per facility; one point is one tenth, a second line for quarters out of compliance.

**First cheap check.** Count rows with non-null `PCT_MINORITY`; it should be 93,808 minus 29,702.

---


# Body: what happens to your health

### W26 · 2010 pill counties become 2024 overdose counties, or not

**The physical thing.** Opioid pills shipped to pharmacies in one county between 2006 and 2012, counted pill by pill from the DEA shipment ledger. Drug overdose deaths in that same county, 2019 to 2024, from the CDC county file.

**Status.** never run. Absorbs wonders 41 and 42 (pills per resident by county; distributor counties versus deaths).

**Data grade.** B. Both sides carry a five-digit county FIPS, but it is a lag question by design: the pill years and the death years do not overlap, and the death-side table that keeps its counts intact is unprofiled.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.HEALTH.HEALTH__FED_DEA_ARCOS | 178,598,026 | one shipment of one opioid product from a reporter to a buyer | 2006-2012 | `BUYER_COUNTY_FIPS` |
| LIBRARY_RAW.LANDING.FED_CDC_INJURY_VIOLENCE_COUNTY | 132,000 | one county, one intent (overdose, suicide, homicide, firearm), one period | 2019-2024 plus one trailing-12-month row (source: data-trap note 2026-09-05; the fact file has no date range) | `GEOID` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY | 132,000 | the same file with `COUNT_SUP` cast to a number; used here only for its profiled key | same | `GEOID` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_DRUG_POISONING_COUNTY | 53,387 | one county, one year, with population | 1999-2015 | `FIPS` |

**Columns that carry it.**
- HEALTH__FED_DEA_ARCOS: `BUYER_COUNTY_FIPS` (fill not profiled by the fact file; traps.md 2026-09-10 counts 178,338,557 filled rows of 178,598,026), `TRANSACTION_DATE` (100%), `DOSAGE_UNITS`, `TOTAL_MME`, `DRUG_NAME`, `BUYER_BUSINESS_ACTIVITY`, `BUYER_STATE`.
- LANDING.FED_CDC_INJURY_VIOLENCE_COUNTY: `GEOID`, `INTENT`, `PERIOD`, `RATE`, `RATE_M`, `COUNT_SUP` (text; real counts plus the range strings '1-9' and '10-50'). Unprofiled: fill not yet measured on this copy. The mart copy of the same 132,000 rows reads `GEOID` 100% filled, 3,153 distinct.
- HEALTH__FED_CDC_DRUG_POISONING_COUNTY: `FIPS` (100%, 3,149 distinct), `YEAR` (100%), `POPULATION` (fill not yet measured).

**The join, hop by hop.**
```
HEALTH__FED_DEA_ARCOS.BUYER_COUNTY_FIPS ➔ HEALTH__FED_CDC_DRUG_POISONING_COUNTY.FIPS   (same year, 2006-2012, gives pills per resident; overlap not yet measured)
HEALTH__FED_DEA_ARCOS.BUYER_COUNTY_FIPS ➔ LANDING.FED_CDC_INJURY_VIOLENCE_COUNTY.GEOID   (overlap not yet measured)
HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY.GEOID ➔ HEALTH__FED_CDC_DRUG_POISONING_COUNTY.FIPS   (measured on the mart copy: 100%)
```

**A hit means.** Counties in the top tenth for pills per resident in 2006-2012 sit in the top tenth for overdose death rate in 2019-2024 far more often than chance. The "or not" half is a named list of high-pill counties that did not become high-death counties.

**A miss means.** The rank of a county on pills says little about its rank on deaths a decade later. That would say the later wave of deaths moved to different places than the pills went.

**Limits, said out loud.**
- Use the landing CDC table, not the mart. The mart cast `COUNT_SUP` to a number and nulled 61,400 of 132,000 rows, because suppressed counts are range strings. In landing the column is text and the ranges survive: a county with '1-9' deaths is known to have had deaths, which the mart hides. A range is still not a count; it bounds the small counties, it does not measure them.
- `RATE` holds -999 as a suppression marker on 822 overdose rows; a bare average reads negative. Filter `RATE` >= 0. `RATE_M` is a 0/1 flag stored as 15-decimal text, and it marks the same rows as the '1-9' counts, so filtering on it selects on the outcome.
- The two sources disagree on how many ARCOS rows got a buyer FIPS: phase5 probe says 178,344,793, traps.md says 178,338,557. The misses are Virginia independent cities written without "city", Dona Ana, Juneau and Puerto Rico, so those places drop out.
- `TRANSACTION_ID` is not a row key: 11,678,713 distinct values over 178,598,026 rows. Never count or dedupe on it.
- No county overdose data is landed for 2016-2018, and no county population after 2015. The pill side can be per resident; the death side must use the CDC's own published rate. The landing CDC table writes its audit columns without a leading underscore (`INGESTED_AT`).

**The picture.** Scatter, x = opioid dosage units per resident 2006-2012, y = overdose death rate 2019-2024, one dot per county; suppressed-range counties drawn hollow at their range.

**First cheap check.** Count distinct `BUYER_COUNTY_FIPS` values that also appear as `GEOID` in the landing CDC table where `INTENT` = 'Drug_OD'; it should be close to 3,144 counties.

---

### W28 · Nursing homes chart sicker right after a chain buys them

**The physical thing.** A nursing home fills in a federal assessment form for each resident. After a new owner takes over, do the forms start describing the same kind of residents as sicker, which raises what Medicare pays?

**Status.** never run.

**Data grade.** D. The question needs a sale date and a before-and-after series of resident assessments; the owner file holds no sale date, and the one probed source says the assessment table holds a single quarter.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP | 295,083 | one enrollment, one owner, one role | one vintage; not yet measured | `ENROLLMENT_ID` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS | 14,425 | one Medicare enrollment of a nursing home | snapshot; record dates run to 2026-02-12 | `ENROLLMENT_ID`, `CCN` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY | 31,403,215 | one home, one report date, one assessment item, one answer | not yet measured; THE_IDEA_BOOK.md row H-085 probed it as one quarter, Q2 2026 | `CCN` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_NURSINGHOME411 | 14,713 | one nursing home, snapshot dated 2025-12-01 | 2025-12-01 | `CMS_CERTIFICATION_NUMBER_CCN` |

**Columns that carry it.**
- FED_CMS_SNF_OWNERSHIP: `ENROLLMENT_ID`, `ASSOCIATE_ID_OWNER`, `ORGANIZATION_NAME_OWNER`, `ROLE_TEXT_OWNER`, `ASSOCIATION_DATE_OWNER` (filled on every row, free text in mixed formats), `PERCENTAGE_OWNERSHIP`, `PRIVATE_EQUITY_COMPANY_OWNER`, `REIT_OWNER`. Table not profiled; fills other than those stated are not yet measured.
- HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS: `ENROLLMENT_ID` (100%), `CCN` (100%), `AFFILIATION_ENTITY_ID`, `AFFILIATION_ENTITY_NAME`, `PROPRIETARY_NONPROFIT`.
- HEALTH__FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY: `CCN` (100%, 14,318 distinct), `REPORT_DATE`, `MDS_ITEM_QUESTION_DESCRIPTION`, `MDS_ITEM_RESPONSE`, `OVERALL_PERCENT`, `TOTAL_RESIDENTS`.
- HEALTH__FED_NURSINGHOME411: `PROVIDER_CHANGED_OWNERSHIP_IN_LAST_12_MONTHS` ('Y' on 55 rows), `NURSING_CASE_MIX_INDEX`, `CHAIN_ID`.

**The join, hop by hop.**
```
FED_CMS_SNF_OWNERSHIP.ENROLLMENT_ID ➔ HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS.ENROLLMENT_ID   (measured: 288,550 of 295,083 owner rows join)
HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS.CCN ➔ HEALTH__FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY.CCN   (measured: 100%)
HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS.CCN ➔ HEALTH__FED_NURSINGHOME411.CMS_CERTIFICATION_NUMBER_CCN   (overlap not yet measured; both join the nursing-home roster at 100%)
```

**A hit means.** For homes with a known recent change of owner, the share of residents charted in the high-payment answers rises in the report dates after the change, and does not rise in homes with no change.

**A miss means.** The charted shares move the same way in changed and unchanged homes. With the data as landed, a miss is the expected result because there is likely no "before" to compare.

**Limits, said out loud.**
- `ASSOCIATION_DATE_OWNER` is a record date, not a sale date. It is free text in mixed formats with three 1800 placeholder values, and the file is one vintage, so it lists current owners only. Nothing shows it tracks a sale. There is no sale history.
- The private-equity flag cannot split the population. `PRIVATE_EQUITY_COMPANY_OWNER` is 'Y' on 196 of 295,083 rows, 97 of 14,410 enrollments, 0.67%. `REIT_OWNER` is 'Y' on 587 enrollments. Both flags are blank, not 'N', on 198,546 rows, 67%. Blank means unknown, never "not private equity".
- The only dated change-of-owner signal is small: 55 homes flagged 'Y' in the 2025-12-01 roster. The enrollment id encodes a record-creation date (O + YYYYMMDD + 6 digits, all 14,425 parse); 54 of 54 flagged homes have a record dated on or after 2024-08-31. It is a record-creation date, not a purchase date.
- The assessment table's time span is the hinge. A probed idea-book row (H-085) says one quarter, Q2 2026, 551 items, 14,695 homes. If that holds, there is no before and no after. the fact file has no date range for `REPORT_DATE`.
- 6,533 owner rows name enrollments that the enrollment snapshot does not carry. The same flag on the other nursing-home roster is 'N' on all 14,700 rows; only the NURSINGHOME411 copy carries the 55.

**The picture.** Two lines per group, x = report date, y = share of residents in the high-payment answer, one line for the 55 changed homes and one for the rest. Only drawable if more than one report date exists.

**First cheap check.** Count distinct `REPORT_DATE` values in the assessment table. One value ends the question as worded.

---

### W29 · Dialysis chains arrive, local kidney doctor count falls

**The physical thing.** A chain-owned dialysis clinic gets certified in a county. In the years after, does the number of kidney doctors billing Medicare from that county go down?

**Status.** never run.

**Data grade.** B. Twelve yearly Medicare billing files give a kidney-doctor head count by ZIP for 2013-2024, and clinic certification dates are fully filled; but the yearly files are unprofiled, the clinic's chain is the chain today, and county comes through a ZIP bridge.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_DIALYSIS | 7,557 | one dialysis clinic, current directory | certification dates 1968-01-01 to 2026-02-09 | `CCN`, `ZIP_CODE` |
| LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_DY2013..DY2024 (12 tables) | 956,251 in DY2013; 1,296,739 in DY2024; family total not yet measured | one clinician, one year of Medicare Part B billing totals | 2013-2024, the year is in the table name | `NPI`, `RNDRNG_PRVDR_ZIP5` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DIALYSIS_FACILITIES | 12,456,456 | one clinic, one quality measure, one year | 2021-2024 | `CCN` |
| LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY | 46,960 | one ZIP-area and county overlap | 2020 vintage | `ZCTA5`, `COUNTY_FIPS` |
| LIBRARY_RAW.LANDING.FED_CMS_NPPES_DEACTIVATED | 351,912 | one deactivated provider id with its deactivation date | not yet measured (date is text) | `NPI` |

**Columns that carry it.**
- HEALTH__FED_CMS_DIALYSIS: `CCN` (100%), `CHAIN_OWNED`, `CHAIN_ORGANIZATION`, `CERTIFICATION_DATE` (100%), `OF_DIALYSIS_STATIONS`, `ZIP_CODE` (100%, 5,361 distinct), `COUNTY_PARISH`, `STATE`.
- FED_CMS_PARTB_PROVIDER_DY*: `NPI`, `RNDRNG_PRVDR_TYPE`, `RNDRNG_PRVDR_ZIP5`, `RNDRNG_PRVDR_ENT_CD`, `TOT_BENES`, `TOT_SRVCS`. Unprofiled: fill not yet measured.
- HEALTH__FED_CMS_MEDICARE_DIALYSIS_FACILITIES: `CCN` (100%, 8,235 distinct), `CHAIN`, `OWNERSHIP_TYPE`, `YEAR_COL` (93.3%).
- XWALK_ZCTA_COUNTY: `ZCTA5`, `COUNTY_FIPS` (100%, 3,266 distinct).
- FED_CMS_NPPES_DEACTIVATED: `NPI`, `NPPES_DEACTIVATION_DATE` (text, MM/DD/YYYY). Not profiled.

**The join, hop by hop.**
```
HEALTH__FED_CMS_DIALYSIS.ZIP_CODE ➔ XWALK_ZCTA_COUNTY.ZCTA5 ➔ COUNTY_FIPS   (overlap not yet measured)
FED_CMS_PARTB_PROVIDER_DY<year>.RNDRNG_PRVDR_ZIP5 ➔ XWALK_ZCTA_COUNTY.ZCTA5 ➔ COUNTY_FIPS   (overlap not yet measured); count distinct NPI where RNDRNG_PRVDR_TYPE is the kidney specialty, per county per year
HEALTH__FED_CMS_DIALYSIS.CCN ➔ HEALTH__FED_CMS_MEDICARE_DIALYSIS_FACILITIES.CCN   (measured: 99%; gives the chain name as reported in 2021-2024)
FED_CMS_PARTB_PROVIDER_DY<year>.NPI ➔ FED_CMS_NPPES_DEACTIVATED.NPI   (overlap not yet measured; tells a retirement from a move)
```

**A hit means.** In counties where a chain clinic was certified between 2014 and 2022, the count of kidney doctors billing from the county falls in the following years, while counties that got a non-chain clinic or none hold steady.

**A miss means.** The kidney-doctor count follows the same path in both kinds of county. That would say chain arrival and doctor supply move independently.

**Limits, said out loud.**
- The earlier version of this entry used the doctor registry, which blanks every deactivated provider (entity type '' on all 346,179 deactivated ids), so a doctor who left had no specialty and no address. The yearly billing files fix that: a doctor is counted in each year they billed, with that year's specialty and ZIP.
- A doctor leaving the billing file is not the same as leaving town. They may have dropped below Medicare's publishing threshold, moved to a hospital's billing id, or retired. Whether low-volume clinicians are withheld from these files is not yet measured here. The deactivation list separates retirements from the rest.
- `CHAIN_ORGANIZATION` is the chain today. A clinic certified as an independent in 2015 and bought by a chain in 2019 reads as a 2015 chain arrival. The yearly dialysis file carries `CHAIN` only for 2021-2024, so the ownership history before 2021 is not recorded anywhere landed.
- The Part B family changes shape at 2017: 59 columns for 2013-2016, 84 for 2017-2024. The columns used here exist in both shapes, but a stacked query needs an explicit column list. Blanks in this family are empty strings, not NULL.
- The exact text of the kidney specialty in `RNDRNG_PRVDR_TYPE` is not in the sources; read the distinct values first. The ZIP bridge is uncertain for the 10,186 of 33,791 ZIP areas that cross a county line, and hospital-campus ZIPs with no ZIP area drop out. `FIVE_STAR_DATE` on the clinic directory is one range string on every row, not a date.

**The picture.** Small-multiple lines, x = years since the first chain clinic certification in the county, y = kidney doctors billing from the county, one line per county group.

**First cheap check.** In the DY2024 table, count distinct `NPI` per `RNDRNG_PRVDR_TYPE` value containing "Neph"; a national count in the thousands confirms the specialty label exists.

---

### W30 · Water violations cluster where hospitals closed

**The physical thing.** A county lost its hospital, shown by a termination date in the Medicare provider file. The public water systems serving that same county, and how many health-based violations they logged. Absorbs wonder 14.

**Status.** never run.

**Data grade.** B. Both sides now reach a five-digit county FIPS, but the hospital file keeps only the latest status per provider and its county code needs padding.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT | 15,432,737 | one violation and enforcement action pair for one water system | begin dates 1900-01-01 (placeholder) to 2026-06-09 | `PWSID` |
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS | 578,198 | one water system and one area it serves | last reported 1995-07-22 to 2026-06-30 | `PWSID`, `COUNTY_FIPS` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER | 44,429 | one Medicare-certified provider, latest status | termination dates 1963-05-07 to 2026-03-19 | `FIPS_STATE_CD` + `FIPS_CNTY_CD` |

**Columns that carry it.**
- SDWA_VIOLATIONS_ENFORCEMENT: `PWSID` (100%, 265,738 distinct), `VIOLATION_ID`, `IS_HEALTH_BASED_IND`, `VIOLATION_CATEGORY_CODE`, `NON_COMPL_PER_BEGIN_DATE` (93.5%).
- SDWA_GEOGRAPHIC_AREAS: `PWSID` (100%, 418,885 distinct), `AREA_TYPE_CODE`, `COUNTY_SERVED`, `STATE_SERVED`, `COUNTY_FIPS` (the fact file has no fill; phase5 probe: 404,823 of 405,396 named county rows), `ZIP_CODE_SERVED` (1.24%, do not use).
- HEALTH__FED_CMS_POS_OTHER: `CCN` (100%), `PRVDR_CTGRY_CD`, `PGM_TRMNTN_CD`, `TRMNTN_EXPRTN_DT` (40.92%), `FIPS_STATE_CD` (316 blank strings), `FIPS_CNTY_CD` (99.29%, a NUMBER, unpadded).

**The join, hop by hop.**
```
SDWA_VIOLATIONS_ENFORCEMENT.PWSID ➔ SDWA_GEOGRAPHIC_AREAS.PWSID   (overlap between these two not yet measured; each joins the SDWA facilities table at 100%)
SDWA_GEOGRAPHIC_AREAS.COUNTY_FIPS ➔ HEALTH__FED_CMS_POS_OTHER.FIPS_STATE_CD || FIPS_CNTY_CD padded to 3   (overlap not yet measured)
```

**A hit means.** Counties with a hospital termination show more health-based violations per water system in the years after the closure than matched counties that kept their hospital.

**A miss means.** Violation rates look the same in both groups. That would say hospital loss and water trouble do not share a county pattern, or that both track something else such as county size.

**Limits, said out loud.**
- The provider file keeps only the latest status per `CCN`. A hospital that closed and whose number was reused, or closures older than the file remembers, are invisible. Every closure count is a floor.
- Which `PRVDR_CTGRY_CD` value means hospital is not in the sources; read the distinct values first. No category in this table is a nursing home.
- `VIOLATION_ID` repeats across enforcement actions, because one row is a violation and enforcement pair. Count distinct violations, not rows.
- Violation dates carry 1900 placeholders at the low end. Bound the date range before charting.
- 6,255 county-type area rows have a blank county name (New Jersey 4,262, Florida 581) and got no FIPS. Water-system ids starting 04 to 10 are EPA regions, not states.

**The picture.** Map of counties, fill = health-based violations per water system after the closure year, outline = counties with a hospital termination; one mark per county.

**First cheap check.** Count distinct five-digit county codes built from the provider file that also appear in `COUNTY_FIPS` on the water areas table.

---

### W32 · Hospice agencies open where nursing home census drops

**The physical thing.** The number of residents sleeping in a county's nursing homes, and the dates new hospice agencies in that county were certified by Medicare.

**Status.** never run.

**Data grade.** C. Hospice opening dates are good, but the resident count table is probably a single quarter, so a "drop" cannot be seen; only a today's-occupancy stand-in is available, and the hospice side joins by county name.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPICE | 6,852 | one hospice agency, current directory | certification dates 1983-11-01 to 2025-10-15 | `COUNTY_PARISH` + `STATE` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY | 31,403,215 | one home, one report date, one assessment item, one answer | not yet measured; THE_IDEA_BOOK.md row H-085 probed it as one quarter, Q2 2026 | `STATE` + `FIPS_COUNTY_CODE` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME | 14,700 | one nursing home, snapshot (landing copy dated 2026-05-01) | 2026 snapshot | `COUNTY_PARISH` + `STATE` |
| LIBRARY_RAW.LANDING.FED_CENSUS_COUNTY_2020 | 3,235 | one county with its name and FIPS parts | 2020 | `STATE` + `COUNTYNAME`, `STATEFP` + `COUNTYFP` |

**Columns that carry it.**
- HEALTH__FED_CMS_HOSPICE: `CCN` (100%), `CERTIFICATION_DATE` (100%), `OWNERSHIP_TYPE`, `COUNTY_PARISH`, `STATE`.
- MINIMUM_DATA_SET_FREQUENCY: `CCN` (100%), `REPORT_DATE`, `TOTAL_RESIDENTS` (stored as text), `STATE`, `FIPS_COUNTY_CODE` (100%, 298 distinct, so a within-state code, not a five-digit FIPS).
- HEALTH__FED_CMS_NURSING_HOME: `NUMBER_OF_CERTIFIED_BEDS`, `AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY` (fill not yet measured), `COUNTY_PARISH`, `STATE`.
- FED_CENSUS_COUNTY_2020: `STATE`, `STATEFP`, `COUNTYFP`, `COUNTYNAME`. Not profiled; phase5 probe verified 3,235 rows with unique FIPS.

**The join, hop by hop.**
```
HEALTH__FED_CMS_HOSPICE.STATE + COUNTY_PARISH ➔ FED_CENSUS_COUNTY_2020.STATE + COUNTYNAME ➔ STATEFP || COUNTYFP   (name join; match rate not yet measured)
MINIMUM_DATA_SET_FREQUENCY.STATE + FIPS_COUNTY_CODE ➔ FED_CENSUS_COUNTY_2020.STATE + COUNTYFP   (not yet measured; padding of the code unknown)
HEALTH__FED_CMS_NURSING_HOME.STATE + COUNTY_PARISH ➔ FED_CENSUS_COUNTY_2020.STATE + COUNTYNAME   (name join; not yet measured)
```

**A hit means.** Counties whose nursing homes run emptiest, residents per certified bed, are the counties with the most hospice certifications in the last five years per existing home.

**A miss means.** Recent hospice openings are spread without regard to how full the local nursing homes are. That would say hospice growth follows something else, such as population or state rules.

**Limits, said out loud.**
- "Census drops" needs resident counts at two dates. The one probed source says the assessment table is one quarter. If so, this entry measures empty beds today, not a fall over time.
- No patient-level hospice enrollment is landed anywhere. `CERTIFICATION_DATE` is the day an agency opened, not a count of patients.
- The hospice table is a current directory. Whether closed agencies remain in it is not yet measured, so openings may be survivors only.
- `COUNTY_FIPS` on the nursing-home roster is blank on all 14,700 rows (the fact file), so that side must also go through the county name. County names need the suffix stripped and St./Saint folded; Virginia independent cities miss without "city".
- `TOTAL_RESIDENTS` is text and repeats on every item row for a home and date; take one value per home per date before summing.

**The picture.** Scatter, x = residents per certified bed in the county, y = hospice agencies certified since 2020 per nursing home, one dot per county.

**First cheap check.** Count hospice rows whose `STATE` + `COUNTY_PARISH` finds exactly one row in the 2020 county list.

---

### W33 · Sickest-charted homes also carry most fire violations

**The physical thing.** A nursing home's case-mix index, the federal score for how sick its residents are on paper, set beside the fire-safety citations inspectors wrote for that same building.

**Status.** never run.

**Data grade.** B. One real shared id with a measured 100% match, but the sickness score is a single snapshot laid against ten years of fire surveys, and its fill is not yet measured.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME | 14,700 | one nursing home, snapshot (landing copy dated 2026-05-01) | 2026 snapshot | `CMS_CERTIFICATION_NUMBER_CCN` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_FIRE_DEFICIENCIES | 200,030 | one fire-safety citation from one survey | 2016-07-28 to 2026-05-21 | `CMS_CERTIFICATION_NUMBER_CCN` |

**Columns that carry it.**
- HEALTH__FED_CMS_NURSING_HOME: `CMS_CERTIFICATION_NUMBER_CCN` (100%, 14,328 distinct by the fact file), `NURSING_CASE_MIX_INDEX` (fill not yet measured), `NUMBER_OF_CERTIFIED_BEDS`, `TOTAL_NUMBER_OF_FIRE_SAFETY_DEFICIENCIES`, `AUTOMATIC_SPRINKLER_SYSTEMS_IN_ALL_REQUIRED_AREAS`, `STATE`.
- HEALTH__FED_CMS_NURSING_HOME_FIRE_DEFICIENCIES: `CMS_CERTIFICATION_NUMBER_CCN` (100%, 13,603 distinct), `SURVEY_DATE` (100%), `DEFICIENCY_TAG_NUMBER`, `SCOPE_SEVERITY_CODE`, `DEFICIENCY_CORRECTED`, `INSPECTION_CYCLE`.

**The join, hop by hop.**
```
HEALTH__FED_CMS_NURSING_HOME_FIRE_DEFICIENCIES.CMS_CERTIFICATION_NUMBER_CCN ➔ HEALTH__FED_CMS_NURSING_HOME.CMS_CERTIFICATION_NUMBER_CCN   (measured: 100%)
```

**A hit means.** Homes in the top fifth on case-mix index carry more fire citations per survey, or more severe ones, than homes in the bottom fifth, inside the same state.

**A miss means.** Fire citations per survey are flat across case-mix fifths. That would say paper sickness and building safety are unrelated.

**Limits, said out loud.**
- The case-mix score is one snapshot. A home's score in 2017 is not known, so old fire citations are compared with today's score. Restrict to the latest inspection cycle to keep the two close in time.
- Citation counts track how often a home is surveyed: repeat-tag rate tracked survey frequency at r = 0.84 across chains. Count per distinct `SURVEY_DATE`, not raw totals.
- `DEFICIENCY_CORRECTED` is a status, not yes/no. 'Waiver has been granted' means open by permission. `CORRECTION_DATE` is a promise; four post-date the file's own publication.
- K0351 is the only no-sprinkler tag; a text search on "sprinkler" inflates the count 4x. The mart's `PROCESSING_DATE` is null on all 14,700 roster rows.
- the fact file counts 14,328 distinct ids on 14,700 roster rows. Whether that is repeated homes or an approximate count is not yet measured; dedupe before joining. State inspection habits differ widely, so compare within state.

**The picture.** Scatter, x = case-mix index, y = fire citations per survey date, one dot per nursing home, coloured by state.

**First cheap check.** Count roster rows where `NURSING_CASE_MIX_INDEX` is filled, and count distinct homes in the fire table that match one.

---

### W34 · Counties with more nursing beds than doctors to staff

**The physical thing.** Certified nursing-home beds in a county, set beside the number of doctors who wrote Medicare prescriptions from an address in that county.

**Status.** never run.

**Data grade.** B. Both sides reach a county only through a ZIP-to-county bridge that is a coin flip for ZIP areas crossing a county line; the county code that should have made this easy is blank.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME | 14,700 | one nursing home, snapshot (landing copy dated 2026-05-01) | 2026 snapshot | `ZIP_CODE` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS | 1,416,883 | one prescriber, one year of Medicare Part D totals | DY2024 (no year column; dated by a data-trap note 2026-09-05) | `PRSCRBR_ZIP5` |
| LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY | 46,960 | one ZIP-area and county overlap | 2020 vintage | `ZCTA5`, `COUNTY_FIPS` |
| LIBRARY_RAW.LANDING.FED_CENSUS_ZCTA_COUNTY_2020 | 47,863 | one ZIP-area and county overlap, with land area of the overlap | 2020 | `GEOID_ZCTA5_20`, `GEOID_COUNTY_20` |

**Columns that carry it.**
- HEALTH__FED_CMS_NURSING_HOME: `NUMBER_OF_CERTIFIED_BEDS`, `ZIP_CODE` (100%, 9,229 distinct), `COUNTY_PARISH`, `STATE`. `COUNTY_FIPS` is blank on all 14,700 rows; do not use it.
- HEALTH__FED_CMS_PART_D_PRESCRIBERS: `NPI` (100%), `PRSCRBR_TYPE`, `PRSCRBR_ZIP5` (54 blank strings), `PRSCRBR_STATE_FIPS` (1,234 blank strings), `PRSCRBR_ENT_CD`.
- XWALK_ZCTA_COUNTY: `ZCTA5`, `COUNTY_FIPS` (100%, 3,266 distinct), `COUNTY_NAME`.
- FED_CENSUS_ZCTA_COUNTY_2020: `GEOID_ZCTA5_20`, `GEOID_COUNTY_20`, `AREALAND_PART`. Not profiled.

**The join, hop by hop.**
```
HEALTH__FED_CMS_NURSING_HOME.ZIP_CODE ➔ XWALK_ZCTA_COUNTY.ZCTA5 ➔ COUNTY_FIPS   (overlap not yet measured)
HEALTH__FED_CMS_PART_D_PRESCRIBERS.PRSCRBR_ZIP5 ➔ XWALK_ZCTA_COUNTY.ZCTA5 ➔ COUNTY_FIPS   (overlap not yet measured)
tie-break for a ZIP area in several counties: FED_CENSUS_ZCTA_COUNTY_2020.AREALAND_PART, largest wins
```

**A hit means.** A ranked list of counties where beds per prescribing doctor is many times the national figure, including counties with beds and no prescriber at all.

**A miss means.** Beds per doctor is tight around one number everywhere. That would say doctor supply already follows bed supply.

**Limits, said out loud.**
- The table map of 2026-09-09 named `COUNTY_FIPS` as the bed-side key. the fact file shows it is an empty string on all 14,700 rows. The bed side has to go through ZIP or county name.
- The ZIP bridge: 33,791 ZIP areas, 10,186 cross a county line. Largest-land-area agrees with a known county 99.5% of the time on single-county areas and 47.1% on the crossing ones. About a third of ZIP areas are uncertain.
- Census gives no ZIP area to a single-building ZIP, so large hospital campuses (Cleveland Clinic 44195, Duke 27710) drop out. The doctor registry loses 4.7% of rows this way, and they are the big employers of doctors.
- The prescriber file is anyone who wrote Part D scripts in 2024: doctors, nurse practitioners, dentists. Filter on `PRSCRBR_TYPE`. A prescriber's address is a billing or practice address, not proof they see nursing-home residents.
- One year on each side. It is a map of 2024-2026, not a trend. No county population after 2015 is landed, so "per resident" is not available.

**The picture.** County map, fill = certified beds per prescribing physician, one mark per county.

**First cheap check.** Count nursing homes whose `ZIP_CODE` finds a row in the ZIP-to-county table; it should be near 14,700.

---

### W35 · Dementia charting jumps after reimbursement rule change

**The physical thing.** The share of a nursing home's residents whose federal assessment form records dementia, before and after Medicare changed how it pays nursing homes on 2019-10-01.

**Status.** never run. Check first: which assessment item is the dementia item is unknown.

**Data grade.** D. The question needs assessment data on both sides of 2019-10-01; the one probed source says the table holds a single quarter in 2026, and the fact file holds no date range to say otherwise.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY | 31,403,215 | one home, one report date, one assessment item, one answer | not yet measured; THE_IDEA_BOOK.md row H-085 probed it as one quarter, Q2 2026, 551 items, 14,695 homes | `CCN` |

**Columns that carry it.**
- MINIMUM_DATA_SET_FREQUENCY: `CCN` (100%, 14,318 distinct), `REPORT_DATE`, `MDS_ITEM_QUESTION_DESCRIPTION`, `MDS_ITEM_RESPONSE`, `OVERALL_PERCENT`, `LONG_STAY_PERCENT`, `SHORT_STAY_PERCENT`, `TOTAL_RESIDENTS` (text), `STATE`. Fill on the percent columns not yet measured.

**The join, hop by hop.**
```
one table, no join
group by REPORT_DATE, MDS_ITEM_QUESTION_DESCRIPTION, MDS_ITEM_RESPONSE; split the series at 2019-10-01
```

**A hit means.** The share of long-stay residents charted with dementia steps up in the report dates right after 2019-10-01 and stays up, while items that do not affect payment stay flat.

**A miss means.** No step at the rule date. With one quarter of data there is no series at all, and the entry can only describe how dementia charting varies between homes in 2026.

**Limits, said out loud.**
- Time span is the whole question. A probed idea-book row says one quarter. Another idea-book row (H-118) calls the table "quarterly, about 4 buckets a year" without a probe. The two disagree; the probed one is the safer reading. 31.4M rows over 14,695 homes and 551 items is about four answer rows per item per home, which fits one period.
- Which of the 551 item descriptions is the dementia item is unknown until the distinct values of `MDS_ITEM_QUESTION_DESCRIPTION` are read.
- The rule date 2019-10-01 is a constant taken from the 2026-09-09 table map, not a table in the warehouse.
- A sweep found 54,245 rows where the three percent columns all read 100; small homes produce blocks of identical values. Weight by `TOTAL_RESIDENTS` after casting it from text.

**The picture.** Line, x = report date, y = share of long-stay residents with the dementia answer, one line per ownership group, vertical rule at 2019-10-01.

**First cheap check.** Select distinct `REPORT_DATE` with row counts. If no date falls before 2019-10-01, stop.

---

### W36 · Nonprofit hospitals pay least charity per surplus dollar

**The physical thing.** A nonprofit hospital's cost report to Medicare: one line is what it spent on free care for poor patients, another line is what it had left over at year end. The ratio of the two, hospital by hospital, set beside what the same organization paid its top executives.

**Status.** never run.

**Data grade.** B. The cost reports answer the ratio alone on one real id across thirteen file years; the tax-return side now reaches executive pay and revenue for 3,962 hospital tax ids, but only through a name-and-ZIP crosswalk, and no landed tax table carries a charity-care dollar figure.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS | 80,077 | one hospital cost report (grain is `RPT_REC_NUM`) | fiscal years ending 2011-04-30 to 2024-09-30; file years 2011-2023 | `PROVIDER_CCN` |
| LIBRARY_MARTS.CORE.XWALK_HOSPITAL_CCN_EIN | 4,003 | one hospital id matched to one tax id, with a match tier | built 2026-09-11 | `CCN`, `EIN` |
| LIBRARY_MARTS.HEALTH.HEALTH__HOSPITAL_OFFICER_PAY | 526,374 | one person on one hospital organization's Form 990, one tax year | tax years 2016-2025 | `EIN` |
| LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF | 1,983,563 | one tax-exempt organization, current master file | snapshot; ruling dates to 2026-06-01 | `EIN` |
| LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_990_EFILE_INDEX | 5,544,626 | one e-filed return: who filed, which period, when | filed 2017-01-03 to 2026-01-01 | `EIN`, `OBJECT_ID` |

**Columns that carry it.**
- HEALTH__FED_CMS_HCRIS: `PROVIDER_CCN` (100%, 7,057 distinct), `RPT_REC_NUM`, `TYPE_OF_CONTROL`, `COST_OF_CHARITY_CARE`, `NET_INCOME`, `TOTAL_COSTS`, `FISCAL_YEAR_END_DATE` (100%), `FISCAL_YEAR_LENGTH_DAYS` (100%, 14 to 472), `SOURCE_FILE_YEAR`. Fill on the two money columns not yet measured on the 13-year load.
- XWALK_HOSPITAL_CCN_EIN: `CCN`, `EIN`, `MATCH_TIER`, `MATCH_RULE`, `EIN_NTEE`, `PROPRIETARY_NONPROFIT`. Not profiled by the fact file.
- HEALTH__HOSPITAL_OFFICER_PAY: `EIN` (100%, 3,962 distinct), `TAX_YEAR` (100%), `PERSON_NAME`, `TITLE`, `TOTAL_COMPENSATION`, `IS_SCHEDULE_J_POINTER`, `IS_GROUP_RETURN`, `BMF_REVENUE_AMT`, `BMF_ASSET_AMT`.
- CORPORATE_REGISTRY__FED_IRS_EO_BMF: `EIN` (100%), `NTEE_CODE`, `REVENUE_AMT`, `ASSET_AMT`, `INCOME_AMT`.
- ECONOMICS__FED_IRS_990_EFILE_INDEX: `EIN` (100%, 893,074 distinct), `TAX_PERIOD`, `RETURN_TYPE`, `OBJECT_ID`. No money columns; it says a return exists, not what is in it.

**The join, hop by hop.**
```
core answer: one table, group HEALTH__FED_CMS_HCRIS by PROVIDER_CCN and fiscal year, filter TYPE_OF_CONTROL to nonprofit
HEALTH__FED_CMS_HCRIS.PROVIDER_CCN ➔ XWALK_HOSPITAL_CCN_EIN.CCN   (crosswalk covers 3,891 of 6,703 nonprofit hospital ids, 58%)
XWALK_HOSPITAL_CCN_EIN.EIN ➔ HEALTH__HOSPITAL_OFFICER_PAY.EIN   (overlap not yet measured)
HEALTH__HOSPITAL_OFFICER_PAY.EIN ➔ CORPORATE_REGISTRY__FED_IRS_EO_BMF.EIN   (measured: 3,914 shared values)
HEALTH__HOSPITAL_OFFICER_PAY.EIN ➔ ECONOMICS__FED_IRS_990_EFILE_INDEX.EIN   (measured: 3,918 shared values)
```

**A hit means.** A ranked list of nonprofit hospitals with a large positive `NET_INCOME` year after year and charity care that is a few cents per surplus dollar, well under their peers; and, for the ones with a tax-id match, top executive pay that is larger than the whole charity-care line.

**A miss means.** Charity care scales with surplus across nonprofits. That would say the tax break and the free care move together.

**Limits, said out loud.**
- The earlier version of this entry had only a 200-row Form 990 table for the tax side. The fuller tables are the officer-pay table (526,374 rows, 3,962 hospital tax ids, 2016-2025) and the exempt-organization master file. Neither holds the Form 990 charity-care schedule; the charity dollar figure still comes only from the cost report.
- Officer pay repeats: one executive appears on every affiliate's return with the same dollars, and 239 person-returns carry a pointer line that restates a separate payout. Rank with `IS_SCHEDULE_J_POINTER` false, drop `IS_GROUP_RETURN` rows (61), and take the maximum per person per tax year, never the sum. Tax years before 2017 are absent from the underlying pay file.
- The crosswalk's tax id is the system that files the return, not the building: 1,293 tax ids cover 3,222 rows; Kaiser's one id sits on 35 hospitals. Compare a system's pay with the sum of its hospitals' charity care, not with one building. Tiers 1 and 2 are name plus ZIP, tier 3 name plus state, tier 4 address; read `MATCH_TIER` before trusting a row.
- The cost-report mart stores the text 'nan' as a floating NaN, not null; 89 `NET_INCOME` rows were counted this way on 2026-09-05, before the 13-year reload. Filter `FISCAL_YEAR_LENGTH_DAYS` >= 300: short reports are seller stubs and lose money 65% of the time against 34% for full years.
- `PROVIDER_CCN` plus `SOURCE_FILE_YEAR` is not unique (1,186 hospital-years carry more than one report), and the file year is a label, not the fiscal period; group on `FISCAL_YEAR_END_DATE`. A surplus of zero or less makes the ratio meaningless, so rank only positive `NET_INCOME` and say how many were dropped. `NET_MARGIN_RATIO` flips sign on 164 rows; do not use it.

**The picture.** Ranked bars, y = hospital, x = charity care cents per dollar of surplus over full-length fiscal years, with a dot on each bar for top executive pay as a share of charity care where a tax id matched.

**First cheap check.** Count distinct `EIN` values in the crosswalk that also appear in the officer-pay table.

---

### W37 · Hospitals closed, where doctors showed up next year

**The physical thing.** The doctors billing Medicare from a hospital's ZIP code in the year it closed, and the ZIP code each one billed from the year after.

**Status.** never run.

**Data grade.** C. Twelve yearly billing files give every doctor a ZIP for each year 2013-2024, so a move can be seen; but no landed table lists who worked at the hospital, so "its doctors" is everyone billing from its ZIP, which is a stand-in.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER | 44,429 | one Medicare-certified provider, latest status | termination dates 1963-05-07 to 2026-03-19 | `CCN`, `ZIP_CD` |
| LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_DY2013..DY2024 (12 tables) | 956,251 in DY2013; 1,296,739 in DY2024; family total not yet measured | one clinician, one year of Medicare Part B billing totals | 2013-2024, the year is in the table name | `NPI`, `RNDRNG_PRVDR_ZIP5` |
| LIBRARY_RAW.LANDING.FED_CMS_NPPES_DEACTIVATED | 351,912 | one deactivated provider id with its date | not yet measured (date is text) | `NPI` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_AFFILIATION | 2,260,193 | one clinician tied to one facility, current snapshot | snapshot; not yet measured | `CCN`, `NPI` |

**Columns that carry it.**
- HEALTH__FED_CMS_POS_OTHER: `CCN` (100%, 43,797 distinct), `PRVDR_CTGRY_CD`, `PGM_TRMNTN_CD`, `TRMNTN_EXPRTN_DT` (40.92%), `ZIP_CD` (270 blank strings), `FAC_NAME`, `ST_ADR`.
- FED_CMS_PARTB_PROVIDER_DY*: `NPI`, `RNDRNG_PRVDR_ZIP5`, `RNDRNG_PRVDR_ST1`, `RNDRNG_PRVDR_CITY`, `RNDRNG_PRVDR_STATE_ABRVTN`, `RNDRNG_PRVDR_TYPE`, `RNDRNG_PRVDR_ENT_CD`, `TOT_BENES`. Unprofiled: fill not yet measured.
- FED_CMS_NPPES_DEACTIVATED: `NPI`, `NPPES_DEACTIVATION_DATE` (text MM/DD/YYYY). Not profiled.
- HEALTH__FED_CMS_FACILITY_AFFILIATION: `NPI` (100%), `CCN` (100%), `FACILITY_TYPE`. Used only to show it cannot answer this.

**The join, hop by hop.**
```
HEALTH__FED_CMS_POS_OTHER (hospital rows with TRMNTN_EXPRTN_DT in 2013-2023).ZIP_CD ➔ FED_CMS_PARTB_PROVIDER_DY<closure year>.RNDRNG_PRVDR_ZIP5   (overlap not yet measured)
FED_CMS_PARTB_PROVIDER_DY<closure year>.NPI ➔ FED_CMS_PARTB_PROVIDER_DY<closure year + 1>.NPI   (overlap not yet measured; compare RNDRNG_PRVDR_ZIP5 across the two years)
NPIs missing the next year ➔ FED_CMS_NPPES_DEACTIVATED.NPI   (overlap not yet measured; separates retired from not billing)
for reference: HEALTH__FED_CMS_POS_OTHER.CCN ➔ HEALTH__FED_CMS_FACILITY_AFFILIATION.CCN   (measured: 14% of provider-file ids appear in the affiliation file)
```

**A hit means.** For each closed hospital, the doctors billing from its ZIP split three ways the next year: same ZIP, a new ZIP (with the towns that gained them named), or gone from the file. Closure ZIPs lose far more doctors than matched ZIPs where no hospital closed.

**A miss means.** Doctors in closure ZIPs stay or leave at the same rate as doctors anywhere. That would say the hospital closing did not move the local doctors, or that the ZIP stand-in is too loose to see it.

**Limits, said out loud.**
- There is still no roster of who worked at a hospital in the past. The affiliation file is a current snapshot and forgets closed hospitals; it also under-reports open ones (35.5% of nursing homes list exactly one clinician). "The hospital's doctors" here means everyone billing from its ZIP, including unrelated offices. Matching on `RNDRNG_PRVDR_ST1` against the hospital's `ST_ADR` narrows it, with a match rate not yet measured.
- The earlier version of this entry graded D because the doctor registry keeps only today's address. The yearly billing files replace it: one address per doctor per year, 2013-2024. Closures before 2013 and after 2023 have no before-and-after pair.
- The billing address is where claims are filed from, which for employed doctors is often the health system's office, not the clinic. A doctor gone from the file may have fallen under the publishing threshold, moved onto a group's billing, or retired; whether low-volume clinicians are withheld is not yet measured.
- The provider file keeps only the latest status per `CCN`, so closure counts are a floor. Which `PRVDR_CTGRY_CD` value means hospital is not in the sources; read the distinct values first.
- The Part B family changes shape at 2017 (59 columns, then 84); the columns used here exist in both. Blanks are empty strings, not NULL. `NPPES_DEACTIVATION_DATE` is text; parse before sorting.

**The picture.** Flow map, one line per doctor from the closed hospital's ZIP to the next year's billing ZIP, line colour = stayed in county, left county, gone from file.

**First cheap check.** Pick one known closure year, count hospital rows terminated that year, and count distinct `NPI` billing from those ZIPs in that year's table and in the next year's.

---

### W39 · Hospitals that own a home health agency, and how many

**The physical thing.** A hospital's legal entity listed on Medicare's ownership paperwork as an owner of a home health agency, or enrolled under the same entity id as one.

**Status.** partially measured. the fact file records 411 entity ids shared between the home health owner file's agency side and hospital enrollments. The owner-side match has not been run.

**Data grade.** A. Both tables carry Medicare's own entity id, both are profiled at 100% fill on that id, and both are current enrollment snapshots of the same program.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_OWNERS | 101,188 | one home health agency enrollment, one owner, one role | snapshot; owner record dates 1800-01-01 (placeholder) to 2026-10-31 | `ASSOCIATE_ID_OWNER`, `ASSOCIATE_ID` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS | 9,175 | one Medicare enrollment of a hospital | snapshot | `ASSOCIATE_ID` |

**Columns that carry it.**
- HEALTH__FED_CMS_HOME_HEALTH_OWNERS: `ENROLLMENT_ID` (100%, 11,510 distinct), `ASSOCIATE_ID` (100%, 10,230 distinct), `ASSOCIATE_ID_OWNER` (100%, 33,323 distinct), `CCN` (98.12%), `ORGANIZATION_NAME`, `ORGANIZATION_NAME_OWNER`, `OWNER_KIND`, `ROLE_TEXT_OWNER`, `PERCENTAGE_OWNERSHIP` (fill not yet measured), `AGENCY_STATE`.
- HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS: `ASSOCIATE_ID` (100%, 5,162 distinct), `CCN` (100%, 9,201 distinct), `ORGANIZATION_NAME`, `PROPRIETARY_NONPROFIT`, `ENROLLMENT_STATE`.

**The join, hop by hop.**
```
HEALTH__FED_CMS_HOME_HEALTH_OWNERS.ASSOCIATE_ID_OWNER ➔ HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS.ASSOCIATE_ID   (hospital entity named as an owner; overlap not yet measured)
HEALTH__FED_CMS_HOME_HEALTH_OWNERS.ASSOCIATE_ID ➔ HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS.ASSOCIATE_ID   (same entity enrolls both; measured: 411 shared values)
```

**A hit means.** A count of hospital entities with at least one home health agency, and a ranked list of the hospital systems holding the most agencies, with ownership percent where filed.

**A miss means.** Few matches on the owner side. That would say hospitals hold agencies through a holding company between them, which this one-hop join does not follow.

**Limits, said out loud.**
- The original wording asked which agency a hospital refers to most. No referral-volume file is landed; the only referral file is a yes/no eligibility list. This entry counts ownership only.
- One hop only. A hospital system that owns an agency through a parent company shows up only if the parent's entity id is also the hospital's. Counts are a floor.
- 95 agency enrollment rows carry a 7-character `CCN` with a letter suffix (branch offices). A 6-character match drops them. Count agencies on `ENROLLMENT_ID` or full `CCN`.
- The entity id links organizations to organizations. It does not reach individual doctors.
- `ASSOCIATION_DATE_OWNER` runs from an 1800 placeholder to a future date, 2026-10-31. Do not use it to date a purchase. The hospital file has 9,175 rows for 5,162 entities, so count distinct entities, not rows.

**The picture.** Ranked bars, y = hospital legal entity, x = number of distinct home health agencies it owns or co-enrolls, one bar per entity.

**First cheap check.** Count distinct `ASSOCIATE_ID_OWNER` values that appear as `ASSOCIATE_ID` in hospital enrollments.

---

### W40 · Hospitals near pollution bill more respiratory per patient

**The physical thing.** Pounds of chemicals released to the air by factories in a county in 2023, and the share of each local hospital's Medicare inpatient stays that were for breathing problems. Absorbs wonder 27.

**Status.** never run.

**Data grade.** C. "Near" is only county-level through a ZIP bridge, each side is a single year, and a hospital's location stands in for where its patients live. The twelve-year Medicare families do not change this grade: neither side of this question is in them.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023 | 78,647 | one facility, one chemical, reporting year 2023 | 2023 | `C_9_ZIP` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_INPATIENT_HOSPITALS_BY_PROVIDER_AND_SERVICE | 145,879 | one hospital, one diagnosis group, one year | one data year; which year not yet measured (no year column) | `RNDRNG_PRVDR_ZIP5`, `RNDRNG_PRVDR_CCN` |
| LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY | 46,960 | one ZIP-area and county overlap | 2020 vintage | `ZCTA5`, `COUNTY_FIPS` |
| LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_SERVICE_DY2013..DY2024 (12 tables; DY2024 holds 9,781,673 rows) | family total not yet measured | one clinician, one billing code, one place of service, one year | 2013-2024, the year is in the table name | `RNDRNG_PRVDR_ZIP5` |

**Columns that carry it.**
- TRI_BASIC_2023: `C_1_YEAR` (100%), `C_2_TRIFD`, `C_9_ZIP` (100%, 8,931 distinct), `C_7_COUNTY`, `C_8_ST`, `C_12_LATITUDE`, `C_13_LONGITUDE`, `C_37_CHEMICAL`, `C_42_CLEAN_AIR_ACT_CHEMICAL`, `C_50_UNIT_OF_MEASURE`, `C_51_5_1_FUGITIVE_AIR`, `C_52_5_2_STACK_AIR`.
- MEDICARE_INPATIENT_HOSPITALS_BY_PROVIDER_AND_SERVICE: `RNDRNG_PRVDR_CCN` (100%, 2,855 distinct), `RNDRNG_PRVDR_ZIP5` (100%, 2,752 distinct), `DRG_CD`, `DRG_DESC`, `TOT_DSCHRGS`, `AVG_MDCR_PYMT_AMT`.
- XWALK_ZCTA_COUNTY: `ZCTA5`, `COUNTY_FIPS` (100%).
- FED_CMS_PARTB_PROVIDER_SERVICE_DY* (optional second outcome, outpatient; columns read from DY2024): `NPI`, `RNDRNG_PRVDR_ZIP5`, `RNDRNG_PRVDR_TYPE`, `HCPCS_CD`, `HCPCS_DESC`, `TOT_BENES`, `TOT_SRVCS`. Unprofiled: fill not yet measured.

**The join, hop by hop.**
```
ENVIRONMENT__FED_EPA_TRI_BASIC_2023.C_9_ZIP (first 5) ➔ XWALK_ZCTA_COUNTY.ZCTA5 ➔ COUNTY_FIPS   (overlap not yet measured)
HEALTH__FED_CMS_MEDICARE_INPATIENT_HOSPITALS_BY_PROVIDER_AND_SERVICE.RNDRNG_PRVDR_ZIP5 ➔ XWALK_ZCTA_COUNTY.ZCTA5 ➔ COUNTY_FIPS   (overlap not yet measured)
optional: FED_CMS_PARTB_PROVIDER_SERVICE_DY2023.RNDRNG_PRVDR_ZIP5 ➔ XWALK_ZCTA_COUNTY.ZCTA5 ➔ COUNTY_FIPS   (overlap not yet measured)
```

**A hit means.** Hospitals in the counties with the most air releases show a higher share of respiratory discharges than hospitals in low-release counties, after grouping by rural or urban.

**A miss means.** The respiratory share is flat across release levels. That would say annual county totals are too blunt to show the effect, not that there is none.

**Limits, said out loud.**
- What the twelve-year landing changes: a Part B table for data year 2023 now exists, so an outpatient breathing-care measure (lung-doctor visits and breathing-test billing codes per patient, by clinician ZIP) can be lined up with the same year as the pollution file. What it does not change: the pollution side is still one year, 2023; the inpatient file is still one year; so there is still no before-and-after and no trend on the question as worded.
- The Part B service table is a suppressed subset: rows under 11 patients are deleted at the source (data-trap note; it removed 90% of one oncologist's drug money). Small rural practices lose the most rows. Which billing codes count as respiratory is not in the sources; read `HCPCS_DESC`.
- Annual totals only. A bad-air day cannot be seen; that is why wonder 27 folded into this one. "Per patient" is respiratory discharges over all discharges at the hospital, Medicare fee-for-service only, and patients cross county lines to hospitals.
- ZIP identifies nothing on its own; it tops the warehouse's shared-column list at 129 tables. The 2026-09-18 review says to restate this on county through the ZIP bridge, where 10,186 of 33,791 ZIP areas cross a county line and single-building hospital ZIPs miss entirely.
- Which `DRG_CD` values are respiratory is not in the sources; read `DRG_DESC`. Releases mix units, so check `C_50_UNIT_OF_MEASURE` before summing pounds. The inpatient file's data year is not recorded in any source; if it is not 2023 the two sides are different years.

**The picture.** Scatter, x = pounds of air releases in the county in 2023 (log scale), y = respiratory share of Medicare discharges, one dot per hospital.

**First cheap check.** Count distinct hospitals whose `RNDRNG_PRVDR_ZIP5` lands in a county that has at least one TRI facility.

---

### W44 · Drugs leading Part D cost growth, and who prescribes them most

**The physical thing.** Twelve years of Medicare Part D claims, one line per prescriber per drug per year: which drugs' total cost climbed the most between 2013 and 2024, and the named prescribers behind the largest share of each.

**Status.** never run.

**Data grade.** B. Twelve same-shaped yearly tables on the national prescriber id make growth testable, but none of the twelve is profiled, and drug names are free text that can change between years.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DRUG_DY2013..DY2024 (12 tables) | 304,308,167 (23,645,873 in DY2013; 28,023,892 in DY2024) | one prescriber, one drug, one year of claims | 2013-2024, the year is in the table name | `NPI`, `GNRC_NAME` |
| LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DY2013..DY2024 (12 tables) | 1,049,299 in DY2013; 1,416,883 in DY2024; family total not yet measured | one prescriber, one year of totals | 2013-2024 | `NPI` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PARTD_PRESCRIBERS | 25,869,521 | the DY2022 year alone, renamed columns; same row count as the DY2022 landing table | DY2022 | `NPI` |

**Columns that carry it.**
- FED_CMS_PARTD_PRESCRIBER_DRUG_DY*: `NPI`, `BRND_NAME`, `GNRC_NAME`, `TOT_DRUG_CST`, `TOT_CLMS`, `TOT_BENES`, `TOT_30DAY_FILLS`, `PRSCRBR_TYPE`, `PRSCRBR_STATE_ABRVTN`, `PRSCRBR_CITY`, `GE65_SPRSN_FLAG`. All twelve carry 25 columns. Unprofiled: fill not yet measured.
- FED_CMS_PARTD_PRESCRIBER_DY*: `NPI`, `PRSCRBR_TYPE`, `PRSCRBR_ZIP5`, `TOT_DRUG_CST`, `TOT_BENES`, `BENE_AVG_RISK_SCRE`. All twelve carry 87 columns. Unprofiled.
- HEALTH__FED_CMS_PARTD_PRESCRIBERS (profiled cross-check for one year): `NPI` (100%, 1,038,177 distinct), `GENERIC_NAME`, `TOTAL_DRUG_COST`.

**The join, hop by hop.**
```
stack the 12 by-drug tables with the year taken from the table name; group by GNRC_NAME and year   (no join)
FED_CMS_PARTD_PRESCRIBER_DRUG_DY<year>.NPI ➔ FED_CMS_PARTD_PRESCRIBER_DY<year>.NPI   (same year; overlap not yet measured; adds ZIP and the prescriber's all-drug total)
cross-check: FED_CMS_PARTD_PRESCRIBER_DRUG_DY2022 row count 25,869,521 = HEALTH__FED_CMS_PARTD_PRESCRIBERS row count 25,869,521
```

**A hit means.** A short list of drugs whose total cost multiplied over the twelve years, and for each a small set of prescribers whose share of that drug's cost is far above their share of its patients, year after year.

**A miss means.** The fastest-growing drugs are spread thinly over thousands of prescribers with nobody standing out. That would say the growth is the price and the patient count, not a few heavy prescribers.

**Limits, said out loud.**
- The 2026-09-18 review reworded this to a one-year question because it knew only the DY2022 mart. The twelve-year landing series was already there (traps.md 2026-09-10). The original growth wording is restored.
- Blanks differ by family: the big by-drug tables store a blank as NULL, the small by-prescriber tables store it as an empty string. Measured: the 2013 by-drug `GE65_TOT_CLMS` has 0 empty strings and 9.8M NULLs; the 2013 by-prescriber `PRSCRBR_MI` has 273,815 empty strings and 0 NULLs. Wrap every column in a blank-to-null guard across the series.
- Cost is dollars of the year, not adjusted for inflation. Whether the cost column is before or after manufacturer rebates is not stated in any source here; treat it as the billed program cost and say so.
- A drug's name is text. A renamed or reformulated product splits into two lines, and a drug launched mid-series has no 2013 base. Rank growth on `GNRC_NAME`, show the first year each drug appears, and check the top names by eye.
- Whether low-volume prescriber and drug pairs are withheld is not yet measured on these tables; CMS withholds small cells in sister files. If so, totals are floors, and a rise in a drug's row count can be prescribers crossing the threshold, not new prescribers. A high-cost prescriber is often a specialist whose drugs are costly by nature; compare within `PRSCRBR_TYPE`.

**The picture.** Slope chart, x = 2013 and 2024, y = total cost per drug (log scale), one line per drug for the top 20 by dollar growth; beside it, ranked bars of each drug's top ten prescribers in 2024.

**First cheap check.** Sum `TOT_DRUG_CST` per table for the twelve by-drug tables: twelve totals that rise without a broken year prove the stack is sound.

---

### W45 · Antipsychotic scripts per nursing bed track chain ownership

**The physical thing.** Antipsychotic prescriptions written for patients 65 and over by the doctors tied to a nursing home, divided by that home's beds, compared across homes that share an owner.

**Status.** never run.

**Data grade.** C. Every hop has a real id, but the doctor-to-home link lists one doctor for 35.5% of homes, and a doctor's prescription count covers all their patients, not that home's residents.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS | 1,416,883 | one prescriber, one year of totals | DY2024 (no year column) | `NPI` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_AFFILIATION | 2,260,193 | one clinician tied to one facility, current snapshot | snapshot; not yet measured | `NPI`, `CCN` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_NURSINGHOME411 | 14,713 | one nursing home, snapshot | 2025-12-01 | `CMS_CERTIFICATION_NUMBER_CCN` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS | 14,425 | one Medicare enrollment of a nursing home | snapshot | `CCN`, `ENROLLMENT_ID` |
| LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP | 295,083 | one enrollment, one owner, one role | one vintage; not yet measured | `ENROLLMENT_ID`, `ASSOCIATE_ID_OWNER` |

**Columns that carry it.**
- HEALTH__FED_CMS_PART_D_PRESCRIBERS: `NPI` (100%), `ANTPSYCT_GE65_TOT_CLMS` (text), `ANTPSYCT_GE65_SPRSN_FLAG`, `ANTPSYCT_GE65_TOT_BENES`, `GE65_TOT_CLMS`, `PRSCRBR_TYPE`. Fill on the antipsychotic columns not yet measured.
- HEALTH__FED_CMS_FACILITY_AFFILIATION: `NPI` (100%), `CCN` (100%), `FACILITY_TYPE`.
- HEALTH__FED_NURSINGHOME411: `CMS_CERTIFICATION_NUMBER_CCN` (100%), `NUMBER_OF_CERTIFIED_BEDS`, `CHAIN_ID`, `CHAIN_NAME`, `OWNERSHIP_TYPE`, `STATE`.
- HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS: `CCN` (100%), `ENROLLMENT_ID` (100%), `AFFILIATION_ENTITY_ID`.
- FED_CMS_SNF_OWNERSHIP: `ENROLLMENT_ID`, `ASSOCIATE_ID_OWNER`, `ORGANIZATION_NAME_OWNER`, `ROLE_TEXT_OWNER`, `PERCENTAGE_OWNERSHIP`. Not profiled.

**The join, hop by hop.**
```
HEALTH__FED_CMS_PART_D_PRESCRIBERS.NPI ➔ HEALTH__FED_CMS_FACILITY_AFFILIATION.NPI   (measured: 706,276 shared values)
HEALTH__FED_CMS_FACILITY_AFFILIATION.CCN ➔ HEALTH__FED_NURSINGHOME411.CMS_CERTIFICATION_NUMBER_CCN   (measured: 91%)
HEALTH__FED_NURSINGHOME411.CMS_CERTIFICATION_NUMBER_CCN ➔ HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS.CCN   (not yet measured directly; both match the nursing-home roster at 100%)
HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS.ENROLLMENT_ID ➔ FED_CMS_SNF_OWNERSHIP.ENROLLMENT_ID   (measured: 288,550 of 295,083 owner rows join)
```

**A hit means.** Homes grouped under one owner id show antipsychotic claims per bed that sit close together and well above, or below, the state figure: one owner, forty homes, the same prescribing level.

**A miss means.** Claims per bed scatter as widely inside an owner group as across all homes. That would say prescribing follows the individual doctor, not the owner.

**Limits, said out loud.**
- The binding limit is the doctor-to-home link. Across 14,501 nursing homes in the affiliation file, 5,148 (35.5%) list exactly one clinician and the median is two. "Scripts per bed" for a third of homes is one person's name.
- A doctor's antipsychotic count is for all their Part D patients 65 and over, in any setting. A doctor tied to three homes and an office has the same number counted at each. This is a proxy for the home, not a measurement of it.
- A blank in `ANTPSYCT_GE65_TOT_CLMS` is a withheld count of 1 to 10, not zero; '0' is the real zero. The column is text. A search for "ANTIPSYCH" finds nothing; CMS spells it without the I.
- Owner grouping: `CHAIN_ID` is blank on 4,551 homes, and named chains include hospital systems. The owner file fixes the blanks by grouping on `ASSOCIATE_ID_OWNER`, but it has no CCN, 6,533 rows do not reach an enrollment, and it lists current owners only.
- Do not split by private equity. `PRIVATE_EQUITY_COMPANY_OWNER` is 'Y' on 97 of 14,410 enrollments, 0.67%, and blank on 67% of rows. `ASSOCIATION_DATE_OWNER` is a record date on one vintage, not a purchase date, so "after the chain bought it" cannot be tested.

**The picture.** Strip plot, x = owner group (owners with ten or more homes), y = antipsychotic claims per certified bed, one dot per home, state median as a reference line.

**First cheap check.** Count nursing homes with two or more affiliated clinicians who also appear in the Part D file; that is the usable population.

---

### W46 · After pill volume explains overdoses, which counties stand out

**The physical thing.** For each county, the overdose death rate you would expect from how many opioid pills were shipped there, and the counties whose real death rate sits far above or below that line.

**Status.** never run.

**Data grade.** B. County FIPS on both sides, but the pills are 2006-2012 and the deaths 2019-2024, the smallest counties have only a range for deaths, and the final wording's table list is inferred because no source file maps it.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.HEALTH.HEALTH__FED_DEA_ARCOS | 178,598,026 | one shipment of one opioid product from a reporter to a buyer | 2006-2012 | `BUYER_COUNTY_FIPS` |
| LIBRARY_RAW.LANDING.FED_CDC_INJURY_VIOLENCE_COUNTY | 132,000 | one county, one intent, one period | 2019-2024 plus one trailing-12-month row (data-trap note 2026-09-05) | `GEOID` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_DRUG_POISONING_COUNTY | 53,387 | one county, one year, with population | 1999-2015 | `FIPS` |

**Columns that carry it.**
- HEALTH__FED_DEA_ARCOS: `BUYER_COUNTY_FIPS` (traps.md: 178,338,557 of 178,598,026 rows filled), `TRANSACTION_DATE` (100%), `DOSAGE_UNITS`, `TOTAL_MME`.
- LANDING.FED_CDC_INJURY_VIOLENCE_COUNTY: `GEOID`, `INTENT`, `PERIOD`, `RATE`, `COUNT_SUP` (text, counts and range strings). Unprofiled: fill not yet measured; the mart copy of the same rows reads `GEOID` 100% filled, 3,153 distinct.
- HEALTH__FED_CDC_DRUG_POISONING_COUNTY: `FIPS` (100%), `YEAR`, `POPULATION` (fill not yet measured).

**The join, hop by hop.**
```
HEALTH__FED_DEA_ARCOS.BUYER_COUNTY_FIPS ➔ HEALTH__FED_CDC_DRUG_POISONING_COUNTY.FIPS   (same year; gives pills per resident; overlap not yet measured)
HEALTH__FED_DEA_ARCOS.BUYER_COUNTY_FIPS ➔ LANDING.FED_CDC_INJURY_VIOLENCE_COUNTY.GEOID   (overlap not yet measured)
LANDING.FED_CDC_INJURY_VIOLENCE_COUNTY.GEOID ➔ HEALTH__FED_CDC_DRUG_POISONING_COUNTY.FIPS   (measured on the mart copy of the same rows: 100%)
```

**A hit means.** A short list of counties whose death rate is far from what their pill volume predicts, in both directions: heavy-pill counties with few deaths, and light-pill counties with many.

**A miss means.** Nearly every county sits close to the line. That would say pill volume alone accounts for the geography of deaths a decade later.

**Limits, said out loud.**
- The final list rewords this from "after poverty explains overdoses". The tables file still lists the poverty version, built on a shortage-area table that covers designated areas only and is not an all-county poverty measure. The pill tables here are taken from W26, which uses the same two sides.
- This is the residual view of W26. Run W26 first; this entry is its leftover, not a separate data pull.
- Use the landing CDC table. The mart nulled 61,400 of 132,000 `COUNT_SUP` values because suppressed counts are range strings ('1-9', '10-50'); in landing they survive as text. That lets the fit keep small counties as bounded points instead of dropping them, but a range is not a count: a standout among '1-9' counties cannot be named.
- `RATE` holds -999 on 822 overdose rows. Filter `RATE` >= 0 before fitting. The named-standouts list is for counties with a published rate.
- One predictor is a thin model. A county can stand out because of age, fentanyl supply or a border with a high-pill county, none of which is controlled here. No county population after 2015 and no all-county poverty or age table is landed.

**The picture.** Scatter with a fitted line, x = pills per resident 2006-2012, y = overdose death rate 2019-2024, one dot per county, the 25 largest residuals labelled.

**First cheap check.** Count counties with both a pills-per-resident figure and an unsuppressed 2019-2024 overdose rate in the landing CDC table.

---

### W47 · After patient age explains prescribing, which counties prescribe more

**The physical thing.** Medicare Part D prescriptions per patient written from addresses in a county, compared with what the age of those doctors' patients would predict, for each year from 2013 to 2024.

**Status.** never run.

**Data grade.** B. Twelve yearly tables carry the prescribing, the patients' age and a ZIP, so a standout county can be checked for staying power; but none of the twelve is profiled, and county still comes through a ZIP bridge that is uncertain for a third of ZIP areas.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DY2013..DY2024 (12 tables) | 1,049,299 in DY2013; 1,416,883 in DY2024; family total not yet measured | one prescriber, one year of totals | 2013-2024, the year is in the table name | `PRSCRBR_ZIP5` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS | 1,416,883 | the DY2024 year alone, profiled; same row count as the DY2024 landing table | DY2024 | `PRSCRBR_ZIP5` |
| LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY | 46,960 | one ZIP-area and county overlap | 2020 vintage | `ZCTA5`, `COUNTY_FIPS` |
| LIBRARY_RAW.LANDING.FED_CENSUS_ZCTA_COUNTY_2020 | 47,863 | one ZIP-area and county overlap, with land area | 2020 | `GEOID_ZCTA5_20`, `GEOID_COUNTY_20` |

**Columns that carry it.**
- FED_CMS_PARTD_PRESCRIBER_DY*: `NPI`, `PRSCRBR_ZIP5`, `PRSCRBR_TYPE`, `TOT_CLMS`, `TOT_BENES`, `TOT_30DAY_FILLS`, `BENE_AVG_AGE`, `BENE_AGE_LT_65_CNT`, `BENE_AGE_65_74_CNT`, `BENE_AGE_75_84_CNT`, `BENE_AGE_GT_84_CNT`, `BENE_AVG_RISK_SCRE`. All twelve carry 87 columns. Unprofiled: fill not yet measured.
- HEALTH__FED_CMS_PART_D_PRESCRIBERS (profiled, 2024 only): `NPI` (100%), `PRSCRBR_ZIP5` (54 blank strings, 21,041 distinct).
- XWALK_ZCTA_COUNTY: `ZCTA5`, `COUNTY_FIPS` (100%, 3,266 distinct), `COUNTY_NAME`, `STATE_USPS`.
- FED_CENSUS_ZCTA_COUNTY_2020: `GEOID_ZCTA5_20`, `GEOID_COUNTY_20`, `AREALAND_PART`. Not profiled.

**The join, hop by hop.**
```
FED_CMS_PARTD_PRESCRIBER_DY<year>.PRSCRBR_ZIP5 ➔ XWALK_ZCTA_COUNTY.ZCTA5 ➔ COUNTY_FIPS   (overlap not yet measured, any year)
tie-break for a ZIP area in several counties: FED_CENSUS_ZCTA_COUNTY_2020.AREALAND_PART, largest wins
fit claims per patient on patient age inside each year; carry each county's residual across the twelve years
```

**A hit means.** A list of counties where claims per patient run well above what the patients' average age predicts in most of the twelve years, holding up when the county's largest prescriber is removed.

**A miss means.** Claims per patient follow patient age closely everywhere, or the standout counties change every year. The first would say the map of heavy prescribing is a map of old patients; the second would say the standouts are noise.

**Limits, said out loud.**
- What twelve years changes: a county that stands out once can be told from one that stands out every year, and one prescriber moving or retiring stops driving a county's number. What it does not change: the age control is still the age of each prescriber's own Part D patients, not the age of the county's residents; no county age table and no county population after 2015 is landed.
- The ZIP bridge is 2020 vintage applied to 2013-2024. 10,186 of 33,791 ZIP areas cross a county line, and the largest-land-area pick is right 47.1% of the time on those. Single-building ZIPs get no ZIP area, so big hospital campuses drop out in every year; the doctor registry loses 4.7% of rows that way.
- Blanks in this family are empty strings, not NULL (measured: 2013 `PRSCRBR_MI` has 273,815 empty strings and 0 NULLs). An "is null" test finds nothing; use a blank-to-null guard on every column across the series.
- The county is where the prescriber's address is, not where the patient lives. A regional medical centre makes its county look heavy in every year, so persistence alone does not prove heavy prescribing.
- Whether the age-band counts are withheld below 11 is not yet measured on these tables; the same CMS rule is documented on the equipment-referrer file, where it deletes the middle of the distribution. Prefer `BENE_AVG_AGE` and `BENE_AVG_RISK_SCRE`, which are not banded. The original table list used a geography table that is not a county dimension; it is replaced here by the ZIP-to-county table.

**The picture.** Heat grid, rows = the 50 counties with the largest average residual, columns = 2013 to 2024, cell = claims per patient above or below the age-predicted figure.

**First cheap check.** For DY2013 and DY2024, count prescriber rows whose `PRSCRBR_ZIP5` finds a row in the ZIP-to-county table, against 1,049,299 and 1,416,883.

---

### W48 · Pharma payments precede prescribing shifts by a year

**The physical thing.** A drug company buys a doctor meals or pays speaking fees in one calendar year. The next year, the same doctor's Medicare Part D claims for that company's brand go up, or they do not. The check is doctor by doctor, against doctors of the same type and state who took nothing.

**Status.** never run.

**Data grade.** B, because NPI is a real shared id, the three payment years are profiled (NPI 100.0% filled) and they overlap Part D years 2021 through 2024, but the Part D year tables are unprofiled and only two payment-then-next-year pairs exist.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_2022 | 13,306,564 | one payment or transfer of value from a maker to a recipient | 2022 (`PROGRAM_YEAR` min 2022, max 2022) | `NPI` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_2023 | 14,700,786 | same | 2023 | `NPI` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS | 15,385,047 | same | 2024 | `NPI` |
| LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DRUG_DY2021 | 25,231,862 | one prescriber x one drug, one year of Part D claims | 2021, from the table name | `NPI`, fill rate not yet measured |
| LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DRUG_DY2022 | 25,869,521 | same | 2022 | `NPI`, fill rate not yet measured |
| LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DRUG_DY2023 | 26,794,878 | same | 2023 | `NPI`, fill rate not yet measured |
| LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DRUG_DY2024 | 28,023,892 | same | 2024 | `NPI`, fill rate not yet measured |

The Part D by-drug family runs DY2013 through DY2024, twelve tables. Only 2021 through 2024 touch the payment years.

**Columns that carry it.**
- The three payment marts, same 22 columns each: `NPI` (100.0% filled; 864,648 distinct in 2022, 934,128 in 2023, 974,632 in 2024; empty string on 51,584, 44,233 and 48,059 rows), `PROGRAM_YEAR` (100.0%), `TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS`, `NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE`, `APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME`, `DATE_OF_PAYMENT`, `COVERED_RECIPIENT_SPECIALTY_1`, `RECIPIENT_STATE`. Fill on the non-key columns not yet measured.
- The four Part D by-drug year tables, same 25 columns each: `NPI`, `BRND_NAME`, `GNRC_NAME`, `TOT_CLMS`, `TOT_DRUG_CST`, `TOT_BENES`, `PRSCRBR_TYPE`, `PRSCRBR_STATE_ABRVTN`, `GE65_SPRSN_FLAG`. Tables not profiled; no fill measured on any column.

**The join, hop by hop.**
```
HEALTH__FED_CMS_OPEN_PAYMENTS_2022.NPI ➔ FED_CMS_PARTD_PRESCRIBER_DRUG_DY2021.NPI and _DY2022.NPI (the before) ➔ _DY2023.NPI (the after)   (overlap not yet measured)
HEALTH__FED_CMS_OPEN_PAYMENTS_2023.NPI ➔ FED_CMS_PARTD_PRESCRIBER_DRUG_DY2022.NPI and _DY2023.NPI (the before) ➔ _DY2024.NPI (the after)   (overlap not yet measured)
HEALTH__FED_CMS_OPEN_PAYMENTS.NPI (2024) ➔ _DY2024.NPI   (same-year only; no DY2025 is landed)
unpaid peers = Part D NPIs with no payment row in any of the three years, same PRSCRBR_TYPE and PRSCRBR_STATE_ABRVTN
```

**A hit means.** Doctors first paid by a maker in year T raise their claims for that maker's brands from T to T+1 by more than unpaid doctors of the same type and state do, and the rise grows with the dollars.

**A miss means.** Paid and unpaid doctors move the same way year over year. That would say the money follows prescribing already in place, which the same tables can show by looking at the year before the payment.

**Limits, said out loud.**
- Both sides are annual. A payment in January and a payment in December of one year look the same. "By a quarter", the original wording, cannot be tested with these tables; a year is the smallest step.
- Only two payment-then-next-year pairs exist: 2022 into 2023, and 2023 into 2024. Payments from 2024 have no following Part D year landed.
- Blank `NPI` is an empty string, not null: 51,584 rows in 2022, 44,233 in 2023, 48,059 in 2024. A null filter misses them. The three payment tables have zero `RECORD_ID` overlap; stack them, never join them (traps.md 2026-09-05).
- 73 rows in the 2024 table carry year-0002 `DATE_OF_PAYMENT`; use `PROGRAM_YEAR` for the year, not the date. The count for 2022 and 2023 is not yet measured.
- The payment marts drop the drug-name columns, so a payment ties to a brand through the maker's name, not the product; payer names split on case ('ABBVIE INC.' / 'AbbVie Inc.'). Natures "Debt forgiveness" ($40.8M) and "Acquisitions" ($213M) put people in the top money decile with no cheque cut (traps.md 2026-09-05, measured on 2024).
- The by-drug year tables store a blank as NULL (traps.md 2026-09-10: `GE65_TOT_CLMS` 2013 has 9.8M NULL). A suppressed small count is not a zero. Whether a doctor-drug pair missing from one year is truly zero or was held back for low volume is not yet measured, so a brand that "appears" in T+1 may only have crossed a reporting floor.

**The picture.** Slope chart: x is year T and T+1, y is brand share of a doctor's claims, one line for newly paid doctors and one for unpaid peers, per specialty; one mark is a group-year.

**First cheap check.** Count distinct non-blank `NPI` in HEALTH__FED_CMS_OPEN_PAYMENTS_2022 that appear in both FED_CMS_PARTD_PRESCRIBER_DRUG_DY2022 and FED_CMS_PARTD_PRESCRIBER_DRUG_DY2023.

---

### W49 · Doctors excluded and still paid by pharma

**The physical thing.** A doctor is on the federal exclusion list, barred from billing federal health programs. A drug or device maker reports paying that same doctor after the exclusion date.

**Status.** never run.

**Data grade.** B, because NPI is a real shared id and both tables are profiled, but only 10.55% of exclusion rows carry an NPI, so every count is a floor.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE | 83,747 | one active exclusion of a person or business | `EXCLUSION_DATE` 1977-07-01 to 2026-08-20 | `NPI` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS | 15,385,047 | one payment or transfer of value from a maker to a recipient | 2024 only | `NPI` |

**Columns that carry it.**
- LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE: `NPI` (10.55% filled, 8,935 distinct), `NPI_IS_REAL` (100.0%), `EXCLUSION_DATE` (100.0%), `EXCLUSION_TYPE`, `LAST_NAME`, `FIRST_NAME`, `SPECIALTY`, `STATE`, `IS_ENTITY_NOT_INDIVIDUAL`.
- LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS: `NPI` (100.0% filled, 48,059 empty strings), `DATE_OF_PAYMENT`, `TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS`, `NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE`, `APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME`.

**The join, hop by hop.**
```
HEALTH__FED_HHS_OIG_LEIE.NPI (NPI_IS_REAL = true) ➔ HEALTH__FED_CMS_OPEN_PAYMENTS.NPI   (overlap not yet measured)
keep rows where OPEN_PAYMENTS.DATE_OF_PAYMENT is after LEIE.EXCLUSION_DATE
```

**A hit means.** A named NPI with an exclusion date before 2024 and one or more 2024 payments dated after it. The output is a list of doctors, payers and amounts.

**A miss means.** Zero excluded NPIs show in 2024 payments. That would say makers screen the list, at least for the tenth of it that carries an NPI.

**Limits, said out loud.**
- Only 8,839 of 83,747 rows (10.6%, 8,660 distinct) carry a real NPI (traps.md 2026-09-05). The join sees a tenth of the ban list. Every hit count is a floor.
- The file is active exclusions only. `WAS_REINSTATED` is false and `REINSTATEMENT_DATE` is blank on 100% of rows (traps.md 2026-09-05). "Reinstated and paid again" cannot be seen; that is why the row was reworded.
- The mart blanks the '0000000000' sentinel to an empty string on 74,908 rows. Filter on `NPI_IS_REAL` or non-blank, not on the sentinel value.
- Payments are program year 2024 only. A doctor excluded during or after 2024 needs the date comparison row by row; 73 payment rows carry year-0002 dates.
- Being excluded does not make a maker's payment illegal. The exclusion bars federal program billing. The output shows the overlap, not a violation.

**The picture.** Ranked bar: one bar per excluded doctor, length is 2024 dollars received after the exclusion date; one mark is one doctor.

**First cheap check.** Count distinct `NPI` where `NPI_IS_REAL` is true in LEIE that appear in OPEN_PAYMENTS.

---

### W50 · Device recalls follow surgeon royalty payments by product

**The physical thing.** A device maker pays a surgeon royalties on an implant. Later the FDA logs a recall of that implant. The question is whether royalty-bearing products get recalled more than the maker's other products.

**Status.** never run.

**Data grade.** C, because the product-code hop into the recall table is empty (`PRODUCT_CODE` is 0.0% filled), so the link falls back to a text match on firm and product description, and the payment side is unprofiled.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_RAW.LANDING.FED_CMS_OPEN_PAYMENTS | 15,385,047 | one payment, with up to five product slots | not yet measured on this table; the mart copy of the same rows is program year 2024 | `ASSOCIATED_DEVICE_OR_MEDICAL_SUPPLY_PDI_1`, fill rate not yet measured |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_GUDID | 5,083,948 | one device record in the FDA device identifier database | `PUBLISH_DATE` 2013-02-20 to 2026-04-22 | `PRIMARY_DI`, fill rate not yet measured |
| LIBRARY_RAW.LANDING.FED_FDA_GUDID_FULL_IDENTIFIERS | 6,767,219 | one identifier (primary or package) for one device | not yet measured | `DEVICEID`, `PRIMARYDI`, fill rate not yet measured |
| LIBRARY_RAW.LANDING.FED_FDA_GUDID_FULL_DEVICE | 5,182,695 | one device record, full 37-column file | not yet measured | `PRIMARYDI`, fill rate not yet measured |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DEVICE_ENFORCEMENT | 39,635 | one device recall | `RECALL_INITIATION_DATE` 1930-12-11 to 2026-07-07; `REPORT_DATE` 2012-06-20 to 2026-07-29 | `RECALLING_FIRM`, `PRODUCT_DESCRIPTION` (text) |

**Columns that carry it.**
- LIBRARY_RAW.LANDING.FED_CMS_OPEN_PAYMENTS: `NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE`, `NAME_OF_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_1`, `ASSOCIATED_DEVICE_OR_MEDICAL_SUPPLY_PDI_1`, `INDICATE_DRUG_OR_BIOLOGICAL_OR_DEVICE_OR_MEDICAL_SUPPLY_1`, `APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME`, `TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS`, `DATE_OF_PAYMENT`, `NPI`. Table not profiled; no fill measured on any of these.
- LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_GUDID: `PRIMARY_DI`, `BRAND_NAME`, `COMPANY_NAME` (100.0% filled, 11,851 distinct), `PRIMARY_PRODUCT_CODE` (99.38% filled, 5,145 distinct).
- LIBRARY_RAW.LANDING.FED_FDA_GUDID_FULL_IDENTIFIERS: `DEVICEID`, `DEVICEIDTYPE`, `PRIMARYDI`. LIBRARY_RAW.LANDING.FED_FDA_GUDID_FULL_DEVICE: `PRIMARYDI`, `BRANDNAME`, `COMPANYNAME`, `VERSIONMODELNUMBER`, `CATALOGNUMBER`. Neither is profiled. They hold more rows than the mart and also list package-level identifiers, so a payment that cites a box code can still reach its device. Neither carries a product code.
- LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DEVICE_ENFORCEMENT: `RECALL_NUMBER`, `RECALLING_FIRM`, `PRODUCT_DESCRIPTION`, `CLASSIFICATION`, `RECALL_INITIATION_DATE` (100.0%), `PRODUCT_CODE` (0.0% filled, 0 distinct).

**The join, hop by hop.**
```
FED_CMS_OPEN_PAYMENTS.ASSOCIATED_DEVICE_OR_MEDICAL_SUPPLY_PDI_1 ➔ HEALTH__FED_FDA_GUDID.PRIMARY_DI   (overlap not yet measured)
wider net for the same hop: PDI_1 ➔ FED_FDA_GUDID_FULL_IDENTIFIERS.DEVICEID ➔ PRIMARYDI ➔ FED_FDA_GUDID_FULL_DEVICE.PRIMARYDI   (overlap not yet measured)
HEALTH__FED_FDA_GUDID.PRIMARY_PRODUCT_CODE ➔ HEALTH__FED_FDA_DEVICE_ENFORCEMENT.PRODUCT_CODE   (dead: PRODUCT_CODE is 0.0% filled)
fallback: GUDID.COMPANY_NAME + BRAND_NAME ➔ DEVICE_ENFORCEMENT.RECALLING_FIRM + PRODUCT_DESCRIPTION, text match, multi-word names only
```

**A hit means.** Products that carry royalty payments show up in recalls at a higher rate than the same maker's products with no royalties, with the recall dated after the payments.

**A miss means.** Royalty products are recalled at the same rate as the rest. Or the product identifier column turns out empty and nothing links, which is a data answer, not a finding.

**Limits, said out loud.**
- `PRODUCT_CODE` and `K_NUMBER_LIST` in the recall mart are 0.0% filled. The clean code-to-code hop named in the 2026-09-09 table map does not exist in the landed mart. The landing copy of the recall file, LIBRARY_RAW.LANDING.FED_FDA_DEVICE_ENFORCEMENT, is 20 rows of raw text in one `RAW` column, so there is no fuller recall table to fall back on. The payment-to-device half of the chain is solid ids; the device-to-recall half is a text match.
- Royalty rows carry a blank NPI on 43% of all royalty dollars (traps.md 2026-09-05). The surgeon side is missing for that share; the product side may still be there.
- Product columns live only in the LANDING copy; the mart drops them (traps.md 2026-09-05). The LANDING copy is unprofiled.
- `APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_ID` is a 12-digit id. Any sum over columns matching 'PAYMENT' reads $1.5 quadrillion (traps.md 2026-09-02). Sum only `TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS`.
- Payments are one program year, 2024. "Recalls follow royalties" has room only for recalls from 2024 to 2026-07-07. Single-word name matches were 8% real in this warehouse; multi-word cleared 92%.

**The picture.** Timeline per product: x is date, royalty payments as ticks, recalls as flags; one mark is one payment or one recall.

**First cheap check.** Count LANDING royalty rows where `ASSOCIATED_DEVICE_OR_MEDICAL_SUPPLY_PDI_1` is non-blank, then how many of those values match a `PRIMARY_DI`.

---

### H-106 · Nursing-home citation severity depends on which state inspected

**The physical thing.** A state surveyor walks a nursing home and writes a citation with a letter grade, A through L, for how bad and how widespread the problem is. The federal rulebook is the same in every state. The share of citations graded at harm level (G through L) is not.

**Status.** measured on 2026-08-22: harm-level share (G-L) 12.50% KY, 12.07% IL down to 1.32% NV, 1.85% MD, a 9.5x spread across states with 2,000+ citations; CA 57,877 citations at 2.54%.

**Data grade.** A, because both tables share the CMS certification number, both are profiled, the measured link is 100%, and the raw spread is already measured; the controlled version has not been run.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES | 418,479 | one health citation at one home on one survey | `SURVEY_DATE` 2017-03-23 to 2026-05-20; real coverage 2023-2026 | `CMS_CERTIFICATION_NUMBER_CCN` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME | 14,700 | one nursing home, current snapshot | one snapshot; the landing copy carries processing date 2026-05-01 (traps.md 2026-09-05) | `CMS_CERTIFICATION_NUMBER_CCN` |

**Columns that carry it.**
- LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES: `CMS_CERTIFICATION_NUMBER_CCN` (100.0% filled, 14,275 distinct), `STATE`, `SCOPE_SEVERITY_CODE`, `DEFICIENCY_TAG_NUMBER`, `SURVEY_DATE` (100.0%), `SURVEY_TYPE`.
- LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME: `CMS_CERTIFICATION_NUMBER_CCN` (100.0% filled, 14,328 distinct), `NUMBER_OF_CERTIFIED_BEDS`, `OWNERSHIP_TYPE`, `CHAIN_NAME`, `REPORTED_TOTAL_NURSE_STAFFING_HOURS_PER_RESIDENT_PER_DAY`. Fill on these not yet measured by the profile.

**The join, hop by hop.**
```
HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES.CMS_CERTIFICATION_NUMBER_CCN ➔ HEALTH__FED_CMS_NURSING_HOME.CMS_CERTIFICATION_NUMBER_CCN   (measured 100%)
group by DEFICIENCIES.STATE, then within DEFICIENCY_TAG_NUMBER, bed-size band and OWNERSHIP_TYPE
```

**A hit means.** The spread survives the controls: the same tag, at homes of the same size and ownership type, is graded harm-level several times more often in one state than another.

**A miss means.** The 9.5x gap shrinks toward nothing once tag mix, size and ownership are held fixed. That would say states cite different problems, not the same problem differently.

**Limits, said out loud.**
- The table is a rolling window with a tail, not a 2017-2026 series: 273 rows in 2017 against 121,925 in 2024, 40 homes in 2017 (traps.md 2026-09-05). Use 2023-2026 only.
- Citation volumes differ 25x across states. Use rates and a minimum-volume floor; the measured spread used states with 2,000+ citations.
- `COMPLAINT_DEFICIENCY` is 'N' on 100% of rows before April 2023 and switches on in Q2 2023. Do not split by complaint flag before then.
- The home table is one snapshot. Beds, staffing and ownership are today's values laid over citations back to 2023.
- The home table has 14,700 rows and 14,328 distinct certification numbers, so some numbers repeat. Dedupe before joining or citations double.

**The picture.** Dot plot: one row per state, x is harm-level share of citations, dot size is citation count; one mark is one state.

**First cheap check.** Count deficiency rows since 2023-01-01 by `STATE` and confirm KY lands at 12.50% harm-level.

---

### H-094 · Staffing predicts the next deficiency

**The physical thing.** A nursing home reports nurse hours per resident per day and how many nurses quit in a year. An inspector later walks in and writes citations. The question is whether thin or churning staff come before the citations.

**Status.** never run.

**Data grade.** B, because an older copy of the home file, processed 2025-12-01, gives a staffing reading that comes before the citations written from then to 2026-05-20, on a shared certification number measured at 100%; the limit is that the forward window is under six months.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.HEALTH.HEALTH__FED_NURSINGHOME411 | 14,713 | one nursing home, earlier snapshot; staffing at time T | `PROCESSING_DATE` 2025-12-01 (min and max) | `CMS_CERTIFICATION_NUMBER_CCN` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES | 418,479 | one health citation at one home on one survey | `SURVEY_DATE` 2017-03-23 to 2026-05-20; real coverage 2023-2026 | `CMS_CERTIFICATION_NUMBER_CCN` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME | 14,700 | one nursing home, later snapshot | one snapshot; landing copy processing date 2026-05-01 (traps.md 2026-09-05) | `CMS_CERTIFICATION_NUMBER_CCN` |

**Columns that carry it.**
- LIBRARY_MARTS.HEALTH.HEALTH__FED_NURSINGHOME411: `CMS_CERTIFICATION_NUMBER_CCN` (100.0% filled, 14,345 distinct), `PROCESSING_DATE` (100.0%), `TOTAL_NURSING_STAFF_TURNOVER`, `REGISTERED_NURSE_TURNOVER`, `NUMBER_OF_ADMINISTRATORS_WHO_HAVE_LEFT_THE_NURSING_HOME`, `REPORTED_RN_STAFFING_HOURS_PER_RESIDENT_PER_DAY`, `REPORTED_TOTAL_NURSE_STAFFING_HOURS_PER_RESIDENT_PER_DAY`, `DEVIATION_FROM_EXPECTED_TOTAL_NURSE_HOURS_PER_RESIDENT_PER_DAY`, `TOTAL_NUMBER_OF_NURSE_STAFF_HOURS_PER_RESIDENT_PER_DAY_ON_THE_WEEKEND`, `NUMBER_OF_CERTIFIED_BEDS`, `OWNERSHIP_TYPE`, `STATE`. Fill on the staffing columns not yet measured.
- LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES: `CMS_CERTIFICATION_NUMBER_CCN` (100.0% filled, 14,275 distinct), `SURVEY_DATE` (100.0%), `SCOPE_SEVERITY_CODE`, `DEFICIENCY_TAG_NUMBER`.
- LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME: `CMS_CERTIFICATION_NUMBER_CCN` (100.0%), `TOTAL_NURSING_STAFF_TURNOVER`, `REPORTED_TOTAL_NURSE_STAFFING_HOURS_PER_RESIDENT_PER_DAY`. Used only to see whether staffing moved between the two snapshots.

**The join, hop by hop.**
```
HEALTH__FED_NURSINGHOME411.CMS_CERTIFICATION_NUMBER_CCN ➔ HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES.CMS_CERTIFICATION_NUMBER_CCN   (CCN to the home table measured 100% on both sides)
keep citations with SURVEY_DATE after 2025-12-01; compare within STATE and bed-size band
HEALTH__FED_NURSINGHOME411.CMS_CERTIFICATION_NUMBER_CCN ➔ HEALTH__FED_CMS_NURSING_HOME.CMS_CERTIFICATION_NUMBER_CCN   (measured 100%)
```

**A hit means.** Within one state and size band, homes in the top turnover quarter on 2025-12-01 draw clearly more citations, and more harm-level ones, in the months after than homes in the bottom quarter.

**A miss means.** Citations after 2025-12-01 are flat across staffing levels once size and state are fixed. That would say the inspection record does not track the staffing numbers homes report.

**Limits, said out loud.**
- The forward window runs from 2025-12-01 to 2026-05-20. Many homes will have no survey inside it. The test runs only on homes that were surveyed in the window; how many is not yet measured.
- Staffing in the snapshot is already a look-back figure reported by the home. Test turnover first; the source ranking calls it the hardest measure to hide.
- Staffing column fill is not yet measured on either snapshot. Homes with blank staffing drop out, and those may be the worst-run homes.
- The earlier snapshot has 14,713 rows and 14,345 distinct certification numbers. Dedupe before joining or citations double.
- Repeat-tag rate tracks survey frequency at r=0.84 across chains (traps.md 2026-09-05). Count citations per survey date, not per home.

**The picture.** Scatter: x is total nursing staff turnover on 2025-12-01, y is citations per survey after that date, one colour per bed-size band; one mark is one home.

**First cheap check.** Count distinct `CMS_CERTIFICATION_NUMBER_CCN` in the citation table with a `SURVEY_DATE` after 2025-12-01.

---

### H-107 · Nursing-home fines per owner, not per location

**The physical thing.** Medicare fines a nursing home. The home is owned by a company that owns other homes. Add up the fines by owner: one owner, forty homes, the same fine over and over.

**Status.** never run.

**Data grade.** B, because the chain is real ids end to end (certification number, then enrollment id) and 288,550 of 295,083 owner rows join, but the owner file is unprofiled and shows current owners only, laid over fines back to 2023.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES | 16,180 | one fine or payment denial against one home | `PENALTY_DATE` 2023-06-17 to 2026-05-13 | `CMS_CERTIFICATION_NUMBER_CCN` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME | 14,700 | one nursing home, current snapshot | one snapshot | `CMS_CERTIFICATION_NUMBER_CCN` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS | 14,425 | one Medicare enrollment of one skilled nursing facility | one snapshot; enrollment ids run to 2026-02-12 (traps.md 2026-09-05) | `CCN`, `ENROLLMENT_ID` |
| LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP | 295,083 | one enrollment x one owner x one role | one vintage, file dated 2026-07-31 (phase5 probe) | `ENROLLMENT_ID` |

**Columns that carry it.**
- LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES: `CMS_CERTIFICATION_NUMBER_CCN` (100.0% filled, 6,771 distinct), `PENALTY_DATE` (100.0%), `PENALTY_TYPE`, `FINE_AMOUNT`, `FINE_ID`.
- LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME: `CMS_CERTIFICATION_NUMBER_CCN` (100.0%), `CHAIN_NAME`, `CHAIN_ID`, `NUMBER_OF_CERTIFIED_BEDS`, `STATE`.
- LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS: `ENROLLMENT_ID` (100.0%), `CCN` (100.0% filled, 14,026 distinct), `ORGANIZATION_NAME`.
- LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP: `ENROLLMENT_ID`, `ASSOCIATE_ID_OWNER`, `ORGANIZATION_NAME_OWNER`, `ROLE_TEXT_OWNER`, `PERCENTAGE_OWNERSHIP` (filled on 96,823 rows per the phase5 probe), `TYPE_OWNER`. Table not profiled; other fills not yet measured.

**The join, hop by hop.**
```
HEALTH__FED_CMS_NURSING_HOME_PENALTIES.CMS_CERTIFICATION_NUMBER_CCN ➔ HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS.CCN   (CCN to the home table measured 100%; to enrollments not yet measured)
HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS.ENROLLMENT_ID ➔ FED_CMS_SNF_OWNERSHIP.ENROLLMENT_ID   (288,550 of 295,083 owner rows join; 14,410 of 14,425 enrollments have owner rows)
group by FED_CMS_SNF_OWNERSHIP.ASSOCIATE_ID_OWNER
side path: PENALTIES.CMS_CERTIFICATION_NUMBER_CCN ➔ NURSING_HOME.CMS_CERTIFICATION_NUMBER_CCN ➔ CHAIN_ID
```

**A hit means.** A short list of owner ids carries a large share of all fine dollars, and their fines per bed sit well above other owners in the same states.

**A miss means.** Fine dollars per bed look the same across owners once state is held fixed. That would say fines follow the state, not the owner.

**Limits, said out loud.**
- `CHAIN_NAME` is blank on 4,221 of 14,700 homes (28.7%). That is why the owner file is the main path and the chain name is the side path.
- The owner file is one vintage: current owners only, not a sale history (traps.md 2026-09-18). A home bought in 2025 hands its 2023 fines to the new owner.
- One home has many owner rows: grain is enrollment x owner x role, 89,543 distinct owner ids, top role "ADP OF THE SNF" at 93,015 rows. Pick roles and an ownership floor first, or one fine is counted once per officer.
- Only `PENALTY_TYPE`='Fine' carries `FINE_AMOUNT`. 2,470 payment-denial rows have blank `FINE_ID`; count(distinct `FINE_ID`) drops them silently (traps.md 2026-09-05).
- Illinois fines $825 per bed against $261 for the rest of the US (traps.md 2026-09-05). An Illinois-heavy owner looks bad mostly for being in Illinois. 6,533 owner rows name enrollments the enrollments snapshot does not carry.

**The picture.** Ranked bar: one bar per owner, length is fine dollars per certified bed, labelled with home count; one mark is one owner.

**First cheap check.** Count distinct `CCN` in the enrollments table that match a `CMS_CERTIFICATION_NUMBER_CCN` in the penalties table.

---

### H-105 · Stars lost after a fine, or fines after lost stars

**The physical thing.** A nursing home has a one-to-five star rating on a public website and a record of federal fines with dates. The question is which comes first: the lost star or the fine.

**Status.** never run.

**Data grade.** C, because there are only two star readings per home, five months apart (2025-12-01 and 2026-05-01): "stars lost after a fine" can be read directly for fines before December 2025, but "fines after lost stars" has under two weeks of fines after the second reading, so that half rests on the dated rating-cycle inspection counts as a stand-in.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES | 16,180 | one fine or payment denial against one home | `PENALTY_DATE` 2023-06-17 to 2026-05-13 | `CMS_CERTIFICATION_NUMBER_CCN` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_NURSINGHOME411 | 14,713 | one nursing home, earlier snapshot with stars and two rating cycles | `PROCESSING_DATE` 2025-12-01; cycle 1 survey dates 2019-09-05 to 2025-12-10; cycle 2 2018-01-19 to 2025-05-23 | `CMS_CERTIFICATION_NUMBER_CCN` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME | 14,700 | one nursing home, later snapshot with stars | one snapshot; landing copy processing date 2026-05-01 (traps.md 2026-09-05) | `CMS_CERTIFICATION_NUMBER_CCN` |

**Columns that carry it.**
- LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES: `CMS_CERTIFICATION_NUMBER_CCN` (100.0% filled, 6,771 distinct), `PENALTY_DATE` (100.0%), `PENALTY_TYPE`, `FINE_AMOUNT`.
- LIBRARY_MARTS.HEALTH.HEALTH__FED_NURSINGHOME411: `CMS_CERTIFICATION_NUMBER_CCN` (100.0% filled, 14,345 distinct), `OVERALL_RATING`, `HEALTH_INSPECTION_RATING`, `RATING_CYCLE_1_STANDARD_SURVEY_HEALTH_DATE` (100.0%), `RATING_CYCLE_2_STANDARD_HEALTH_SURVEY_DATE` (99.69%), `RATING_CYCLE_1_TOTAL_NUMBER_OF_HEALTH_DEFICIENCIES`, `RATING_CYCLE_2_3_TOTAL_NUMBER_OF_HEALTH_DEFICIENCIES`. Fill on the rating columns not yet measured.
- LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME: `CMS_CERTIFICATION_NUMBER_CCN` (100.0% filled, 14,328 distinct), `OVERALL_RATING`, `HEALTH_INSPECTION_RATING`, `RATING_CYCLE_1_TOTAL_HEALTH_SCORE`, `RATING_CYCLE_2_3_TOTAL_HEALTH_SCORE`. Fill not yet measured.

**The join, hop by hop.**
```
HEALTH__FED_NURSINGHOME411.CMS_CERTIFICATION_NUMBER_CCN ➔ HEALTH__FED_CMS_NURSING_HOME.CMS_CERTIFICATION_NUMBER_CCN   (measured 100%); star change = later OVERALL_RATING minus earlier
HEALTH__FED_CMS_NURSING_HOME_PENALTIES.CMS_CERTIFICATION_NUMBER_CCN ➔ both snapshots on the same column   (measured 100%)
fine-first test: homes fined before 2025-12-01 against unfined homes, star change across the two snapshots
star-first test: order each PENALTY_DATE against the home's two rating-cycle survey dates
```

**A hit means.** Homes fined in the year before December 2025 lose stars across the two snapshots more often than unfined homes that started at the same rating. Or, the other way, most fines land just after the worse of the two rating-cycle surveys.

**A miss means.** Fined and unfined homes change stars at the same rate, and fines fall evenly around the survey dates. That would say fines and ratings move on separate tracks.

**Limits, said out loud.**
- Two star readings, five months apart. Most homes may show no change at all. That is a direction check, not a trend.
- Penalties end 2026-05-13 and the later snapshot is dated 2026-05-01. There is almost no record of fines after the second star reading, so "fines follow lost stars" cannot be tested on stars. It rests on rating-cycle survey dates and citation counts, which feed the stars but are not the stars.
- Fines usually come out of an inspection, and the same inspection moves the health-inspection star. A fine and a lost star close together are one event seen twice. Separate fines tied to a cycle survey from fines that are not.
- 2,470 of 16,180 penalty rows (15%) have no fine amount; they are payment denials.
- Both snapshots repeat some certification numbers (14,345 distinct in 14,713 rows; 14,328 in 14,700). Dedupe before comparing.

**The picture.** Dumbbell: one row per star level in December 2025, two dots for the share of homes that lost a star by May 2026, fined against unfined; one mark is a group of homes.

**First cheap check.** Count homes present in both snapshots whose `OVERALL_RATING` differs between them.

---

### H-110 · Inspection records too clean for their peers

**The physical thing.** A nursing home with many beds, thin staff and a for-profit owner in a heavy-citing state, and almost no citations in three years. The question is which homes have a record far cleaner than homes like them.

**Status.** never run.

**Data grade.** B, because the id is real and the link is measured at 100%, but the peer features are a current snapshot with unmeasured fill, and a home with zero citations has no rows in the citation table at all.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME | 14,700 | one nursing home, current snapshot | one snapshot | `CMS_CERTIFICATION_NUMBER_CCN` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES | 418,479 | one health citation at one home on one survey | `SURVEY_DATE` 2017-03-23 to 2026-05-20; real coverage 2023-2026 | `CMS_CERTIFICATION_NUMBER_CCN` |

**Columns that carry it.**
- LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME: `CMS_CERTIFICATION_NUMBER_CCN` (100.0% filled, 14,328 distinct), `STATE`, `NUMBER_OF_CERTIFIED_BEDS`, `AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY`, `OWNERSHIP_TYPE`, `REPORTED_TOTAL_NURSE_STAFFING_HOURS_PER_RESIDENT_PER_DAY`, `TOTAL_NURSING_STAFF_TURNOVER`, `DATE_OF_MOST_RECENT_HEALTH_INSPECTION`, `MOST_RECENT_HEALTH_INSPECTION_MORE_THAN_2_YEARS_AGO`, `TOTAL_NUMBER_OF_HEALTH_DEFICIENCIES`. Fill on these not yet measured.
- LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES: `CMS_CERTIFICATION_NUMBER_CCN` (100.0% filled, 14,275 distinct), `SURVEY_DATE`, `SCOPE_SEVERITY_CODE`, `SURVEY_TYPE`.

**The join, hop by hop.**
```
HEALTH__FED_CMS_NURSING_HOME.CMS_CERTIFICATION_NUMBER_CCN ➔ HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES.CMS_CERTIFICATION_NUMBER_CCN   (measured 100%; left join, so homes with no citations stay in)
peer group = same STATE, bed-size band, OWNERSHIP_TYPE
```

**A hit means.** A named list of homes whose citation count sits far below their peer group, and which were inspected on schedule. Clean and inspected is the odd case.

**A miss means.** Every low-count home is explained by size, state or a missing inspection. Then "too clean" is just "not inspected", which is its own list.

**Limits, said out loud.**
- A clean record and a skipped inspection look the same in the citation table: no rows. Check `MOST_RECENT_HEALTH_INSPECTION_MORE_THAN_2_YEARS_AGO` first and split the two groups.
- The citation window is 2023-2026 with a straggler tail (273 rows in 2017, 121,925 in 2024). A home that opened in 2025 looks clean because it is new; use `DATE_FIRST_APPROVED_TO_PROVIDE_MEDICARE_AND_MEDICAID_SERVICES`.
- State sets the baseline. Harm-level share runs 9.5x across states (H-106), so peers must be in-state.
- "Too clean" points at a weak inspection or at a good home. The data cannot tell them apart. The output is a list to look at, not a verdict.

**The picture.** Scatter: x is citations expected from peers, y is citations found, diagonal drawn; one mark is one home, the far-below points labelled.

**First cheap check.** Count homes in the home table with zero rows in the citation table since 2023-01-01.

---

### H-104 · Does a fine change behaviour, before versus after

**The physical thing.** Medicare fines a nursing home on a known date. Inspectors keep coming. The question is whether the home's citations drop after the fine, compared with a similar home that was not fined.

**Status.** partially measured: the book records 6,628 of 14,700 homes fined, 3,722 homes with 2+ penalties, 2,470 of 16,180 penalties with no amount, window 2 years 11 months. The before-and-after test itself has never been run.

**Data grade.** B, because all three tables share the certification number with measured 100% links and the dates are real, but the window is under three years, so each home has a short "before" and a short "after".

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES | 16,180 | one fine or payment denial against one home | `PENALTY_DATE` 2023-06-17 to 2026-05-13 | `CMS_CERTIFICATION_NUMBER_CCN` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES | 418,479 | one health citation at one home on one survey | `SURVEY_DATE` 2017-03-23 to 2026-05-20; real coverage 2023-2026 | `CMS_CERTIFICATION_NUMBER_CCN` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME | 14,700 | one nursing home, current snapshot; the control pool | one snapshot | `CMS_CERTIFICATION_NUMBER_CCN` |

**Columns that carry it.**
- LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES: `CMS_CERTIFICATION_NUMBER_CCN` (100.0% filled, 6,771 distinct), `PENALTY_DATE` (100.0%), `PENALTY_TYPE`, `FINE_AMOUNT`.
- LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES: `CMS_CERTIFICATION_NUMBER_CCN` (100.0%), `SURVEY_DATE` (100.0%), `SCOPE_SEVERITY_CODE`, `DEFICIENCY_TAG_NUMBER`.
- LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME: `CMS_CERTIFICATION_NUMBER_CCN` (100.0%), `STATE`, `NUMBER_OF_CERTIFIED_BEDS`, `OWNERSHIP_TYPE`, `LATITUDE`, `LONGITUDE`, staffing columns. Feature fill not yet measured.

**The join, hop by hop.**
```
HEALTH__FED_CMS_NURSING_HOME_PENALTIES.CMS_CERTIFICATION_NUMBER_CCN ➔ HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES.CMS_CERTIFICATION_NUMBER_CCN   (both measured 100% to the home table)
split each home's citations at its first PENALTY_DATE
HEALTH__FED_CMS_NURSING_HOME.CMS_CERTIFICATION_NUMBER_CCN supplies the matched unfined home: same STATE, bed band, OWNERSHIP_TYPE
```

**A hit means.** Fined homes' citations per survey fall after the fine by more than their unfined twins' do over the same months.

**A miss means.** Fined homes and their twins move the same way, or fined homes get worse. That would say the fine is a bill, not a correction.

**Limits, said out loud.**
- The penalty window is 2023-06-17 to 2026-05-13. A home fined in 2023 has almost no "before"; a home fined in 2026 has almost no "after".
- 3,722 homes have 2+ penalties. "First fine" inside this window may not be the home's first fine ever; earlier fines are not landed.
- A fined home gets inspected more. More visits mean more citations. Count per survey date; repeat-tag rate tracks survey frequency at r=0.84 (traps.md 2026-09-05).
- The control features are today's snapshot, not the values at the time of the fine.
- 2,470 of 16,180 penalties are payment denials with no dollar amount. Decide up front whether they count as a fine.

**The picture.** Two lines: x is months from the fine (negative to positive), y is citations per survey, one line fined homes and one their twins; one mark is a month-average.

**First cheap check.** Count homes with a Fine-type penalty between 2024-06-01 and 2025-06-01 that have at least one survey date on each side of it.

---

### WN-147 · Predicted versus actual inspection outcomes

**The physical thing.** Fit a plain model that guesses each home's citation count from its size, staffing, owner type and state. Then list the homes where the guess was confident and wrong, high or low.

**Status.** never run.

**Data grade.** B, because the id link is measured at 100% and the inputs exist by name, but the inputs are one current snapshot with unmeasured fill, and the outcome window is three years.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME | 14,700 | one nursing home, current snapshot; the model inputs | one snapshot | `CMS_CERTIFICATION_NUMBER_CCN` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES | 418,479 | one health citation; the outcome | `SURVEY_DATE` 2017-03-23 to 2026-05-20; real coverage 2023-2026 | `CMS_CERTIFICATION_NUMBER_CCN` |

**Columns that carry it.**
- LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME: `CMS_CERTIFICATION_NUMBER_CCN` (100.0%), `STATE`, `NUMBER_OF_CERTIFIED_BEDS`, `AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY`, `OWNERSHIP_TYPE`, `URBAN`, `PROVIDER_RESIDES_IN_HOSPITAL`, `REPORTED_RN_STAFFING_HOURS_PER_RESIDENT_PER_DAY`, `REPORTED_TOTAL_NURSE_STAFFING_HOURS_PER_RESIDENT_PER_DAY`, `NURSING_CASE_MIX_INDEX`, `TOTAL_NURSING_STAFF_TURNOVER`, `REGISTERED_NURSE_TURNOVER`. Fill not yet measured.
- LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES: `CMS_CERTIFICATION_NUMBER_CCN` (100.0%), `SURVEY_DATE`, `SCOPE_SEVERITY_CODE`.

**The join, hop by hop.**
```
HEALTH__FED_CMS_NURSING_HOME.CMS_CERTIFICATION_NUMBER_CCN ➔ HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES.CMS_CERTIFICATION_NUMBER_CCN   (measured 100%; left join)
outcome = citations per survey date since 2023; residual = found minus predicted
```

**A hit means.** A short tail of homes sits far off the prediction, and the misses share something: one state agency, one owner, one inspection season.

**A miss means.** The residuals are small and scattered with no shared trait. That would say size, staffing and state already explain the inspection record.

**Limits, said out loud.**
- Do not feed the model the home table's own citation and rating columns (`TOTAL_NUMBER_OF_HEALTH_DEFICIENCIES`, `HEALTH_INSPECTION_RATING`, `OVERALL_RATING`). They are built from the outcome. The prediction would be circular.
- Inputs are today's snapshot; citations run back to 2023. Staffing may be a result of past citations, not a cause.
- This is H-110 with a model behind it. The two lists will overlap; run them together, not as two findings.
- Citation window 2023-2026 only; the 2017-2022 rows are a straggler tail (273 rows in 2017, 121,925 in 2024).
- A large residual says "unexplained by these inputs". It does not say what the explanation is.

**The picture.** Scatter: x is predicted citations per survey, y is found, diagonal drawn; one mark is one home, largest misses labelled.

**First cheap check.** Count homes with all chosen input columns non-blank; that is the model's real sample.

---

### WN-149 · Does special-focus status change a home

**The physical thing.** Medicare puts the worst nursing homes on a named watch list, the Special Focus Facility list. A second group are "candidates", just as bad but not picked. The question is whether being picked changes anything.

**Status.** partially measured: 88 current special-focus homes, 440 candidates, no designation date. The comparison has never been run.

**Data grade.** C, because the file carries no designation date; two snapshots (2025-12-01 and 2026-05-01) can bracket the homes that joined or left the list between them, but how many did is not yet measured, and for the rest only listed homes against candidates can be compared.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME | 14,700 | one nursing home, later snapshot | one snapshot; landing copy processing date 2026-05-01 (traps.md 2026-09-05) | `CMS_CERTIFICATION_NUMBER_CCN` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_NURSINGHOME411 | 14,713 | one nursing home, earlier snapshot | `PROCESSING_DATE` 2025-12-01 (min and max) | `CMS_CERTIFICATION_NUMBER_CCN` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES | 418,479 | one health citation at one home on one survey | `SURVEY_DATE` 2017-03-23 to 2026-05-20; real coverage 2023-2026 | `CMS_CERTIFICATION_NUMBER_CCN` |

**Columns that carry it.**
- LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME: `CMS_CERTIFICATION_NUMBER_CCN` (100.0%), `SPECIAL_FOCUS_STATUS` (fill not measured by the profile; the source ranking counted 88 and 440), `STATE`, `NUMBER_OF_CERTIFIED_BEDS`.
- LIBRARY_MARTS.HEALTH.HEALTH__FED_NURSINGHOME411: `CMS_CERTIFICATION_NUMBER_CCN` (100.0% filled, 14,345 distinct), `SPECIAL_FOCUS_STATUS`, `PROBLEM_FACILITIES_SFFS_CANDIDATES_ONE_STAR`, `PROCESSING_DATE` (100.0%). Fill on the status columns not yet measured.
- LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES: `CMS_CERTIFICATION_NUMBER_CCN` (100.0%), `SURVEY_DATE` (100.0%), `SCOPE_SEVERITY_CODE`.

**The join, hop by hop.**
```
HEALTH__FED_NURSINGHOME411.CMS_CERTIFICATION_NUMBER_CCN ➔ HEALTH__FED_CMS_NURSING_HOME.CMS_CERTIFICATION_NUMBER_CCN   (measured 100%); compare SPECIAL_FOCUS_STATUS across the two to find homes that joined or left
HEALTH__FED_CMS_NURSING_HOME.CMS_CERTIFICATION_NUMBER_CCN (SPECIAL_FOCUS_STATUS set) ➔ HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES.CMS_CERTIFICATION_NUMBER_CCN   (measured 100%)
compare the 88 listed homes with the 440 candidates, citations per survey by quarter
```

**A hit means.** The 88 listed homes' harm-level citations per survey fall across 2023-2026 faster than the 440 candidates' do, and homes listed in both snapshots improve more than candidates who stayed candidates.

**A miss means.** Listed homes and candidates track each other. That would say the list changes nothing that the citation record can show.

**Limits, said out loud.**
- There is no designation date. The two snapshots only say a home joined or left between 2025-12-01 and 2026-05-01. For a home already listed in December, the listing could be from any earlier year.
- A home that joined the list inside that window has, at most, citations up to 2026-05-20 as its "after". That is too short to show a change. The number of such homes is not yet measured.
- Homes that graduated before December 2025, or closed, are in neither group. The 88 lean toward the ones that did not improve.
- 88 homes is a small group. One state with several listed homes can move the whole result.
- If listed homes are surveyed more often than candidates, they collect more citations for that reason alone. Compare per survey, never per home.

**The picture.** Two lines: x is quarter 2023-2026, y is harm-level citations per survey, one line for the 88, one for the 440; one mark is a group-quarter.

**First cheap check.** Count rows by `SPECIAL_FOCUS_STATUS` in each snapshot, then count homes whose value differs between the two.

---

### H-111 · Surveys bunch at the end of the window

**The physical thing.** Every nursing home must get a standard inspection within a fixed certification window. If inspectors show up mostly in the last weeks of that window, the visit date is set by the calendar, not by how risky the home is.

**Status.** never run.

**Data grade.** B, because it is one profiled table with a 100% filled date, but the table only holds surveys that produced a citation, so a clean survey leaves no date behind.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES | 418,479 | one health citation at one home on one survey | `SURVEY_DATE` 2017-03-23 to 2026-05-20; real coverage 2023-2026 | `CMS_CERTIFICATION_NUMBER_CCN` |

**Columns that carry it.**
- LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES: `CMS_CERTIFICATION_NUMBER_CCN` (100.0% filled, 14,275 distinct), `SURVEY_DATE` (100.0%), `INSPECTION_CYCLE`, `SURVEY_TYPE`, `STANDARD_DEFICIENCY`, `STATE`. Fill on `INSPECTION_CYCLE` and `SURVEY_TYPE` not yet measured.

**The join, hop by hop.**
```
one table, no join
distinct (CMS_CERTIFICATION_NUMBER_CCN, SURVEY_DATE) where STANDARD_DEFICIENCY marks a standard survey
gap in days between a home's consecutive standard surveys, grouped by STATE
```

**A hit means.** The gaps between a home's standard surveys pile up just under one fixed length, and the pile looks the same for high-citation and low-citation homes.

**A miss means.** Gaps are spread out, and homes with worse records get shorter gaps. That would say inspectors go where the risk is.

**Limits, said out loud.**
- One row is a citation. A standard survey that found nothing has no row, so its date is missing and the gap across it reads double. This biases gaps long for clean homes.
- Real coverage is 2023-2026, room for two or three standard surveys per home. Surveys before 2023 are a straggler tail (40 homes in 2017).
- Complaint visits are not scheduled by the window. `COMPLAINT_DEFICIENCY` is 'N' on 100% of rows before April 2023, so use `STANDARD_DEFICIENCY` and `SURVEY_TYPE` to pick standard surveys, and check their values first.
- The home table carries two rating-cycle survey date columns that do not depend on a citation being written. Their fill is not yet measured; they are the better source if filled.

**The picture.** Histogram: x is days between consecutive standard surveys, y is count of gaps, one panel per state; one mark is one gap.

**First cheap check.** Count distinct (`CMS_CERTIFICATION_NUMBER_CCN`, `SURVEY_DATE`) pairs since 2023-01-01, and how many homes have two or more.

---

### WN-150 · Low-entropy inspection outcomes

**The physical thing.** Some homes get the same two or three citation tags at the same letter grade on every visit, whatever else changed. A record that never varies says more about the inspection than the home.

**Status.** never run.

**Data grade.** B, because it is one profiled table with filled keys, but the usable window is three years, so most homes have only a few surveys to measure sameness over.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES | 418,479 | one health citation at one home on one survey | `SURVEY_DATE` 2017-03-23 to 2026-05-20; real coverage 2023-2026 | `CMS_CERTIFICATION_NUMBER_CCN` |

**Columns that carry it.**
- LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES: `CMS_CERTIFICATION_NUMBER_CCN` (100.0% filled, 14,275 distinct), `SURVEY_DATE` (100.0%), `DEFICIENCY_TAG_NUMBER`, `SCOPE_SEVERITY_CODE`, `DEFICIENCY_CATEGORY`, `STATE`. Fill on the tag and severity columns not yet measured.

**The join, hop by hop.**
```
one table, no join
per CMS_CERTIFICATION_NUMBER_CCN: the spread of (DEFICIENCY_TAG_NUMBER, SCOPE_SEVERITY_CODE) across SURVEY_DATE values
compare within STATE
```

**A hit means.** A set of homes, often sharing a state or district, where every survey returns nearly the same tags at the same grade, far more alike than other homes with the same number of surveys.

**A miss means.** Sameness tracks only the number of citations: homes with few citations look repetitive because there is little to vary. That would say the measure is a count in disguise.

**Limits, said out loud.**
- 2017-2022 rows are a straggler tail: 273 rows in 2017 against 121,925 in 2024. Use 2023-2026.
- With three years of data a home has few surveys. Sameness over two surveys means little. Set a floor on survey count and compare only homes with equal counts.
- A few tags are cited almost everywhere. Sameness on a common tag is not odd. Weight by how rare the tag is in that state.
- A home with a real, unfixed problem also repeats. `DEFICIENCY_CORRECTED` is a status text, not a yes/no (traps.md 2026-09-05). The data cannot separate "same problem" from "same checklist".

**The picture.** Scatter: x is number of surveys, y is sameness score, one mark is one home; the low-variety, many-survey corner is the list.

**First cheap check.** Count homes with four or more distinct `SURVEY_DATE` values since 2023-01-01.

---

### WN-154 · Homes that act like a chain without being one

**The physical thing.** Nursing homes in a chain tend to look alike on paper: same staffing ratios, same turnover, same citation pattern. Some homes with no chain name look just like one chain's homes. The question is which ones.

**Status.** never run.

**Data grade.** B, because it is one profiled table with about 50 numeric features, but feature fill is not measured and the chain label used as ground truth is blank on 28.7% of homes.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME | 14,700 | one nursing home, current snapshot | one snapshot; landing copy processing date 2026-05-01 | `CMS_CERTIFICATION_NUMBER_CCN` |

**Columns that carry it.**
- LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME: `CMS_CERTIFICATION_NUMBER_CCN` (100.0% filled, 14,328 distinct), `CHAIN_NAME`, `CHAIN_ID`, `NUMBER_OF_FACILITIES_IN_CHAIN`, `STATE`, `NUMBER_OF_CERTIFIED_BEDS`, `REPORTED_NURSE_AIDE_STAFFING_HOURS_PER_RESIDENT_PER_DAY`, `REPORTED_LPN_STAFFING_HOURS_PER_RESIDENT_PER_DAY`, `REPORTED_RN_STAFFING_HOURS_PER_RESIDENT_PER_DAY`, `REGISTERED_NURSE_HOURS_PER_RESIDENT_PER_DAY_ON_THE_WEEKEND`, `NURSING_CASE_MIX_INDEX`, `TOTAL_NURSING_STAFF_TURNOVER`, `REGISTERED_NURSE_TURNOVER`, `TOTAL_WEIGHTED_HEALTH_SURVEY_SCORE`, `TOTAL_AMOUNT_OF_FINES_IN_DOLLARS`. Fill on the numeric features not yet measured.

**The join, hop by hop.**
```
one table, no join
cluster homes on the numeric staffing, turnover, case-mix and survey-score columns
then lay CHAIN_ID over the clusters; look at homes with blank CHAIN_ID inside a one-chain cluster
```

**A hit means.** A tight cluster that is mostly one chain, plus several no-chain homes that sit inside it. Those homes are candidates for shared management that the chain label does not show.

**A miss means.** Clusters follow state and bed count, not chain. That would say chains do not run their homes alike, and behaviour cannot find hidden ones.

**Limits, said out loud.**
- `CHAIN_NAME` is blank on 4,221 of 14,700 homes (28.7%). Blank means "no chain reported", which is the very thing under test, so the ground truth is weakest where the question looks.
- "Chains" in this label include hospital systems (traps.md 2026-09-05, measured on the sister roster table). A hospital-based cluster is not a nursing chain.
- State drives staffing rules and citation rates. Without holding state fixed, clusters are maps. Pin chains on `CHAIN_ID`; name matching gave 5 of 15 substring false positives.
- A lookalike is a lead, not proof of common ownership. The owner file (LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP) is the check; it is not part of this single-table run.
- `COUNTY_FIPS` in this table is an empty string on all 14,700 rows. Do not use it as a feature or a key.

**The picture.** 2-D cluster map: each dot a home placed by similarity, coloured by chain, no-chain homes in grey; one mark is one home.

**First cheap check.** Count homes with every chosen feature non-blank, split by blank and non-blank `CHAIN_ID`.

---

### N3 · The roughly 684 homes CMS flags as PE or REIT owned, against matched peers

**The physical thing.** In the Medicare owner file, 97 nursing-home enrollments have an owner flagged as a private-equity company and 587 have an owner flagged as a real-estate investment trust. Take those homes, find unflagged homes of the same size, state and owner type, and compare fines, citations, stars and staffing.

**Status.** partially measured on 2026-09-18: `PRIVATE_EQUITY_COMPANY_OWNER` is 'Y' on 196 of 295,083 rows, 97 of 14,410 enrollments (0.67%); `REIT_OWNER` is 'Y' on 587 enrollments; both flags are blank on 198,546 rows (67%). The comparison has never been run.

**Data grade.** C, because the flags are blank, not 'N', on 67% of rows, so "not PE" is unknown for two-thirds of the file; this is a study of about 684 flagged homes against matched peers, not a split of all homes into PE and the rest.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP | 295,083 | one enrollment x one owner x one role | one vintage, file dated 2026-07-31 (phase5 probe) | `ENROLLMENT_ID` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS | 14,425 | one Medicare enrollment of one skilled nursing facility | one snapshot; enrollment ids run to 2026-02-12 | `ENROLLMENT_ID`, `CCN` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME | 14,700 | one nursing home, current snapshot | one snapshot | `CMS_CERTIFICATION_NUMBER_CCN` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES | 418,479 | one health citation at one home on one survey | `SURVEY_DATE` 2017-03-23 to 2026-05-20; real coverage 2023-2026 | `CMS_CERTIFICATION_NUMBER_CCN` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES | 16,180 | one fine or payment denial against one home | `PENALTY_DATE` 2023-06-17 to 2026-05-13 | `CMS_CERTIFICATION_NUMBER_CCN` |

**Columns that carry it.**
- LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP: `ENROLLMENT_ID`, `PRIVATE_EQUITY_COMPANY_OWNER` ('Y' on 196 rows), `REIT_OWNER` ('Y' on 587 enrollments), `ORGANIZATION_NAME_OWNER`, `ASSOCIATE_ID_OWNER`, `ROLE_TEXT_OWNER`, `PERCENTAGE_OWNERSHIP` (filled on 96,823 rows), `ASSOCIATION_DATE_OWNER`. Table not profiled.
- LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS: `ENROLLMENT_ID` (100.0%), `CCN` (100.0% filled, 14,026 distinct), `PROPRIETARY_NONPROFIT`.
- LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME: `CMS_CERTIFICATION_NUMBER_CCN` (100.0%), `STATE`, `NUMBER_OF_CERTIFIED_BEDS`, `OWNERSHIP_TYPE`, `OVERALL_RATING`, `STAFFING_RATING`, `REPORTED_TOTAL_NURSE_STAFFING_HOURS_PER_RESIDENT_PER_DAY`, `TOTAL_NURSING_STAFF_TURNOVER`. Fill not yet measured.
- LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES: `CMS_CERTIFICATION_NUMBER_CCN` (100.0%), `SURVEY_DATE`, `SCOPE_SEVERITY_CODE`.
- LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES: `CMS_CERTIFICATION_NUMBER_CCN` (100.0%), `PENALTY_DATE`, `PENALTY_TYPE`, `FINE_AMOUNT`.

**The join, hop by hop.**
```
FED_CMS_SNF_OWNERSHIP.ENROLLMENT_ID ➔ HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS.ENROLLMENT_ID   (288,550 of 295,083 rows join; 14,410 of 14,425 enrollments have owner rows)
HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS.CCN ➔ HEALTH__FED_CMS_NURSING_HOME.CMS_CERTIFICATION_NUMBER_CCN   (CCN measured 100%)
HEALTH__FED_CMS_NURSING_HOME.CMS_CERTIFICATION_NUMBER_CCN ➔ NURSING_HOME_DEFICIENCIES and NURSING_HOME_PENALTIES on the same column   (both measured 100%)
peers = unflagged homes, same STATE, bed band, OWNERSHIP_TYPE
```

**A hit means.** The flagged homes show lower nurse hours, higher turnover and more fine dollars per bed than their matched peers, and the gap holds inside single states.

**A miss means.** Flagged homes and peers look the same. That says little about private equity in general, because the peer group may itself hold unflagged PE homes.

**Limits, said out loud.**
- Both flags are blank on 198,546 of 295,083 rows (67%). Blank is unknown, never "not PE" (traps.md 2026-09-18). Peers drawn from blank rows may be PE-owned, which pulls any real gap toward zero.
- 97 plus 587 is the 684. Whether any enrollment carries both flags is not yet measured, so the count of distinct homes is "about 684". The PE group alone is 97 enrollments, 0.67%: too small to split by state.
- The flag is self-reported by the home on its enrollment form. It marks who told Medicare they are PE-owned, not who is.
- `ASSOCIATION_DATE_OWNER` is free text in mixed formats with 1800 sentinels, and the file is one vintage: current owners only. There is no purchase date, so no before-and-after the buyout.
- Penalties start 2023-06-17 and the home table is one snapshot. Today's owner is laid over up to three years of record that may belong to a prior owner. The owner file is cp1252, not UTF-8, and has no CCN of its own.

**The picture.** Paired dot plot: one row per measure (nurse hours, turnover, fine dollars per bed, citations per survey, stars), two dots per row for flagged homes and peers; one mark is a group average.

**First cheap check.** Count distinct `ENROLLMENT_ID` with `PRIVATE_EQUITY_COMPANY_OWNER`='Y' or `REIT_OWNER`='Y', then how many reach a `CMS_CERTIFICATION_NUMBER_CCN` in the home table.

---


# Money: who gets it, who gives it

### W51 · 13F ownership shifts the quarter before a contract lands, matched on multi-word issuer name

**The physical thing.** A big investment manager files a quarterly list of the stocks it holds. A company on that list wins a federal contract the next quarter. The question is whether the share count moved first.

**Status.** never run

**Data grade.** B. It works only as a company-name match, because the 13F issuer side carries a CUSIP and no company id, and neither the holdings view nor the contract tables have measured fill.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_HOLDINGS | view, no count | one stock position on one manager's quarterly filing | not yet measured | `ACCESSION_NUMBER`, `NAMEOFISSUER` |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_SUBMISSIONS | 336,124 | one 13F filing by one manager | not yet measured | `ACCESSION_NUMBER`, `CIK` |
| LIBRARY_RAW.LANDING.FED_SEC_13F_SECURITIES_LIST | 25,333 | one line of the SEC's official 13F securities list | one list quarter, 2026 Q2 (phase5 probe) | `CUSIP` |
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK | 5,300,149 | one EPA facility matched to a corporate parent | no date column | `PARENT_LEGAL_NAME`, `PARENT_UEI` |
| LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 through FY2026 (20 tables) | 96,976,021 | one contract transaction | FY2007-FY2026 | `RECIPIENT_PARENT_NAME`, `RECIPIENT_PARENT_UEI` |

**Columns that carry it.**
- 13F_HOLDINGS: `ACCESSION_NUMBER`, `NAMEOFISSUER`, `CUSIP`, `VALUE_USD`, `SSHPRNAMT`, `PUTCALL`. Fill not yet measured (unprofiled view).
- 13F_SUBMISSIONS: `ACCESSION_NUMBER`, `CIK` (100.0% filled, 16,205 distinct managers), `PERIODOFREPORT`, `FILING_DATE`.
- 13F_SECURITIES_LIST: `CUSIP`, `ISSUER_NAME`, `STATUS`. Fill not yet measured.
- XC_EPA_CORPORATE_CROSSWALK: `PARENT_LEGAL_NAME`, `PARENT_CIK` (2.25% filled, 705 distinct), `PARENT_UEI` (8.07% filled, 30,969 distinct, 389,581 blank strings).
- CONTRACTS_FY tables: `RECIPIENT_NAME`, `RECIPIENT_PARENT_NAME`, `RECIPIENT_UEI`, `RECIPIENT_PARENT_UEI`, `ACTION_DATE`, `FEDERAL_ACTION_OBLIGATION`. Fill rate not yet measured.

**The join, hop by hop.**
```
13F_HOLDINGS.ACCESSION_NUMBER ➔ 13F_SUBMISSIONS.ACCESSION_NUMBER   (gives the quarter, PERIODOFREPORT; overlap not yet measured)
13F_HOLDINGS.CUSIP ➔ 13F_SECURITIES_LIST.CUSIP                     (official issuer name; dedupe the list on CUSIP first)
13F_HOLDINGS.NAMEOFISSUER ➔ CONTRACTS_FY.RECIPIENT_PARENT_NAME     (name match, names of two or more words only; overlap not yet measured)
side route, EPA parents only:
13F_HOLDINGS.NAMEOFISSUER ➔ XC_EPA_CORPORATE_CROSSWALK.PARENT_LEGAL_NAME ➔ PARENT_UEI ➔ CONTRACTS_FY.RECIPIENT_PARENT_UEI
```

**A hit means.** For issuers that win a large new award, total shares held across managers rises in the quarter before the award more often than in other quarters of the same issuer.

**A miss means.** Share counts before an award look like any other quarter. That says contract wins are not visible in advance in quarterly holdings, or the name match is too thin to see it.

**Limits, said out loud.**
- There is no CUSIP-to-CIK table and no CIK-to-UEI table among the verified tables. The join is a name match. Measured elsewhere in this warehouse: multi-word name matches held up 92% of the time, single-word matches 8%.
- The 13F load missed 7 of 53 source zips while its checksum still matched (traps 2026-08-31). Some quarters may be absent; count filings per `PERIODOFREPORT` before reading any change as real.
- 13F_SECURITIES_LIST is 25,333 lines but 23,277 distinct CUSIPs, about 2,000 verbatim repeats, and no CIK anywhere in it.
- 13F is quarterly. "The quarter before" is the finest grain possible; a move inside a quarter cannot be seen.
- `FEDERAL_ACTION_OBLIGATION` is signed. Filter to values above zero or award totals read wrong.

**The picture.** Event-study line: x is quarters relative to the award quarter (-4 to +4), y is percent change in shares held; one mark is one issuer-quarter averaged across awards.

**First cheap check.** Count distinct multi-word `NAMEOFISSUER` values that equal any `RECIPIENT_PARENT_NAME` in FY2024 alone.

---

### W52 · Congressional trades cluster around roll-call votes, House 2021-2026

**The physical thing.** A member of Congress reports buying or selling a stock on a given date. The same member casts a recorded floor vote on a nearby date. The question is whether trades bunch up in the days around votes.

**Status.** never run

**Data grade.** B. Trades and votes overlap from 2023-01-03 to 2026-06-25, but the House trades table has no member id, so members are matched by name and district, and the House table has no measured fill.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_RAW.LANDING.FED_HOUSE_PTR | 27,286 | one trade line parsed from a House periodic transaction report PDF | filing years 2021-2026 | `FILER_LAST`, `FILER_FIRST`, `STATE_DISTRICT` |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_SENATE_EFD_PTR | 6,855 | one trade line on a Senate periodic transaction report | 2020-02-07 to 2026-08-19 by `TRANSACTION_DATE` | `FILER_LAST_CLEAN` |
| LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_CROSSWALK | 12,794 | one member of Congress, all of history, with every id | no date range measured | `NAME_LAST`, `NAME_FIRST`, `ICPSR` |
| LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_VOTES | 945,523 | one member's vote on one roll call | follows roll calls, 2023-2026 | `ICPSR`, `CONGRESS`, `CHAMBER`, `ROLLNUMBER` |
| LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_ROLLCALLS | 3,364 | one roll-call vote | 2023-01-03 to 2026-06-25 | `CONGRESS`, `CHAMBER`, `ROLLNUMBER` |

**Columns that carry it.**
- FED_HOUSE_PTR: `FILER_LAST`, `FILER_FIRST`, `STATE_DISTRICT`, `TRANSACTION_DATE`, `TRANSACTION_TYPE`, `TICKER`, `AMOUNT_RANGE`, `IS_SCAN`, `FILING_YEAR`. Fill rate not yet measured.
- FED_SENATE_EFD_PTR: `FILER_LAST_CLEAN`, `TRANSACTION_DATE` (98.54% filled), `TICKER` (991 distinct, 100 blank strings), `TRANSACTION_TYPE`, `AMOUNT_RANGE`, `FILING_ID`.
- MEMBER_CROSSWALK: `NAME_LAST`, `NAME_FIRST`, `LAST_STATE`, `LAST_DISTRICT`, `LAST_TERM_TYPE`, `ICPSR` (96.12% filled), `BIOGUIDE` (99.9% filled).
- VOTEVIEW_VOTES: `ICPSR` (100.0% filled, 639 distinct), `CAST_CODE`, `VOTE_POSITION`.
- VOTEVIEW_ROLLCALLS: `VOTE_DATE` (100.0% filled), `BILL_NUMBER`, `VOTE_QUESTION`, `VOTE_DESC`.

**The join, hop by hop.**
```
FED_HOUSE_PTR.FILER_LAST + FILER_FIRST + STATE_DISTRICT ➔ MEMBER_CROSSWALK.NAME_LAST + NAME_FIRST + LAST_STATE + LAST_DISTRICT   (name match; overlap not yet measured)
FED_SENATE_EFD_PTR.FILER_LAST_CLEAN ➔ MEMBER_CROSSWALK.NAME_LAST   (measured 2026-09-06: of 62 filers, a plain last-name join lands 26 clean, 29 ambiguous, 7 missed)
MEMBER_CROSSWALK.ICPSR ➔ VOTEVIEW_VOTES.ICPSR
VOTEVIEW_VOTES.CONGRESS + CHAMBER + ROLLNUMBER ➔ VOTEVIEW_ROLLCALLS.CONGRESS + CHAMBER + ROLLNUMBER   (gives VOTE_DATE)
```

**A hit means.** A member's trades fall within a few days of that member's recorded votes more often than they would if the same trades were spread evenly over the same months.

**A miss means.** Trade dates sit no closer to vote dates than chance. With votes happening most weeks in session, that is a real possibility, and it would say timing against floor votes is not the signal.

**Limits, said out loud.**
- There is no hearing table in the warehouse. This entry tests floor votes only. Committee hearings and markups, where information often arrives first, cannot be seen.
- An older Senate trades table runs 2012-06 to 2020-12 and does not overlap the votes at all. Only FED_HOUSE_PTR and FED_SENATE_EFD_PTR reach the vote window, which starts 2023-01-03.
- The vote tables carry no industry or subject code. A trade in a drug stock cannot be tied to a health vote without hand-coding `BILL_NUMBER` or `VOTE_DESC`.
- House reports that were filed as scans could not be read at all; no OCR tool was available. Those filings carry no trade lines. Neither chamber reports a dollar figure, only a range, so any total is a bounded estimate.
- The Senate mart's `SENATOR` column holds the literal word 'Senator' on 98 rows. Match on `FILER_LAST_CLEAN`. "Scott" still matches two sitting senators.

**The picture.** Histogram: x is days from a trade to that member's nearest roll-call vote (-30 to +30), y is count of trades; one mark is one day bucket, with a shuffled-date baseline drawn over it.

**First cheap check.** Count distinct (`FILER_LAST`, `FILER_FIRST`, `STATE_DISTRICT`) in FED_HOUSE_PTR that match exactly one MEMBER_CROSSWALK row.

---

### W53 · Zips give most to politics, get least back

**The physical thing.** People in one ZIP code write checks to federal campaigns. Federal contracts and grants are paid to recipients in that same ZIP. The question is which ZIPs send a lot and receive little.

**Status.** never run

**Data grade.** B. All three sides share a five-digit ZIP, but the contribution table's date window is not re-measured, the income table is one tax year, and a ZIP identifies a place, not a payer.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS | 283,771,819 | one itemized contribution from one person to one committee | not yet re-measured (see limits) | `ZIP_CODE` |
| LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 through FY2026 (20 tables) | 96,976,021 | one contract transaction | FY2007-FY2026 | `RECIPIENT_ZIP_4_CODE` |
| LIBRARY_RAW.LANDING.FED_USASPENDING_ASSISTANCE_FY2007 through FY2026 (20 tables) | 128,155,142 | one grant, loan or direct-payment transaction | FY2007-FY2026 | `RECIPIENT_ZIP_CODE` |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS_SOI | 179,796 | one ZIP by income bracket, tax return totals | 2016 only | `ZIP_CODE` |
| LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY | 46,960 | one ZIP-area to county pairing | 2020 vintage | `ZCTA5`, `COUNTY_FIPS` |

**Columns that carry it.**
- FEC_INDIV_CONTRIBUTIONS: `ZIP_CODE` (100.0% filled, 321,021 blank strings, 5,757,830 distinct so it mixes 5 and 9 digit forms), `TRANSACTION_AMT`, `TRANSACTION_DATE` (99.98% filled), `TRANSACTION_TYPE`, `STATE`.
- CONTRACTS_FY tables: `RECIPIENT_ZIP_4_CODE`, `FEDERAL_ACTION_OBLIGATION`, `ACTION_DATE_FISCAL_YEAR`. Fill rate not yet measured.
- ASSISTANCE_FY tables: `RECIPIENT_ZIP_CODE`, `FEDERAL_ACTION_OBLIGATION`, `FACE_VALUE_OF_LOAN`, `ASSISTANCE_TYPE_CODE`, `ACTION_DATE_FISCAL_YEAR`. Fill rate not yet measured.
- IRS_SOI: `ZIP_CODE` (100.0% filled, 29,922 distinct), `N_RETURNS`, `AGI`, `AGI_STUB`, `TAX_YEAR`.
- XWALK_ZCTA_COUNTY: `ZCTA5`, `COUNTY_FIPS` (100.0% filled, 3,266 distinct).

**The join, hop by hop.**
```
left 5 of FEC_INDIV_CONTRIBUTIONS.ZIP_CODE ➔ left 5 of CONTRACTS_FY.RECIPIENT_ZIP_4_CODE   (overlap not yet measured)
left 5 of FEC_INDIV_CONTRIBUTIONS.ZIP_CODE ➔ ASSISTANCE_FY.RECIPIENT_ZIP_CODE               (overlap not yet measured)
left 5 of FEC_INDIV_CONTRIBUTIONS.ZIP_CODE ➔ IRS_SOI.ZIP_CODE                               (per-return denominator)
optional rollup: ZIP5 ➔ XWALK_ZCTA_COUNTY.ZCTA5 ➔ COUNTY_FIPS
```

**A hit means.** A ranked list of ZIPs where dollars given per tax return are in the top tenth and federal dollars received per tax return are in the bottom tenth.

**A miss means.** Giving and receiving rise together by ZIP. That would say the places that fund campaigns are also the places where contractors and grantees sit, which is its own finding.

**Limits, said out loud.**
- The contribution table holds 283,771,819 rows today. Older notes describe an 84.2M-row copy that was 99.99% 2023-2026. The window on the current table is not yet re-measured: the fact helper shows `TRANSACTION_DATE` running 0031-04-10 to 9206-07-02, which are junk end dates, not a range.
- Earmarked pass-through rows are `TRANSACTION_TYPE` 15E. Left in, the same dollar can count twice.
- Loans carry no obligation. Assistance types 07 and 08 sum `FEDERAL_ACTION_OBLIGATION` to exactly $0.00 on 11,788,945 rows; the money sits in `FACE_VALUE_OF_LOAN`. A trap note dated 2026-09-11 says a total on obligation alone drops 47% of rows.
- Recipient ZIP is where the recipient's office sits, not where the work or the benefit lands. A headquarters ZIP collects money spent elsewhere.
- IRS_SOI is tax year 2016 only. It is a fixed denominator, not a matching year.

**The picture.** Scatter: x is contributions per tax return, y is federal dollars received per tax return, both log scale; one mark is one ZIP.

**First cheap check.** Count distinct left-5 `ZIP_CODE` values in the contribution table that also appear in IRS_SOI `ZIP_CODE`.

---

### W55 · Disaster contractors win same counties every storm

**The physical thing.** After a declared disaster, federal contracts are performed in the hit county. The question is whether the same few companies collect that work in the same county, disaster after disaster.

**Status.** never run

**Data grade.** B. County FIPS is a real shared id on both sides and the years overlap, but neither the declarations table nor the contract year tables have been profiled by the fact helper; county fill was measured on one year only.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_RAW.LANDING.FED_FEMA_DISASTER_DECLARATIONS | 70,402 | one disaster by one designated area (county) | not yet measured | `FIPSSTATECODE` + `FIPSCOUNTYCODE` |
| LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 through FY2026 (20 tables) | 96,976,021 | one contract transaction | FY2007-FY2026 | `PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE` |
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_NOAA_STORM_EVENTS | 1,780,730 | one storm event in one county or forecast zone | 1996-2025 | `STATE_FIPS` + `CZ_FIPS` |

**Columns that carry it.**
- FED_FEMA_DISASTER_DECLARATIONS: `DISASTERNUMBER`, `DECLARATIONDATE`, `INCIDENTTYPE`, `INCIDENTBEGINDATE`, `FIPSSTATECODE`, `FIPSCOUNTYCODE`, `DESIGNATEDAREA`. Fill rate not yet measured.
- CONTRACTS_FY tables: `RECIPIENT_UEI`, `RECIPIENT_NAME`, `RECIPIENT_PARENT_UEI`, `ACTION_DATE`, `FEDERAL_ACTION_OBLIGATION`, `AWARDING_SUB_AGENCY_NAME`, `NATIONAL_INTEREST_ACTION`, `PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE`. County FIPS measured on FY2024 only: filled on 93% of rows, 5 wide, 2,894 distinct counties.
- NOAA_STORM_EVENTS: `YEAR` (100.0% filled), `EVENT_TYPE`, `CZ_TYPE`, `STATE_FIPS` (100.0%), `CZ_FIPS` (100.0%), `DAMAGE_PROPERTY`.

**The join, hop by hop.**
```
FED_FEMA_DISASTER_DECLARATIONS.FIPSSTATECODE || FIPSCOUNTYCODE ➔ CONTRACTS_FY.PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE   (overlap not yet measured)
   with CONTRACTS_FY.ACTION_DATE inside a window after DECLARATIONDATE
then group by county + RECIPIENT_UEI, count distinct DISASTERNUMBER
optional severity: NOAA_STORM_EVENTS.STATE_FIPS || CZ_FIPS where CZ_TYPE = 'C' ➔ same county FIPS
```

**A hit means.** In counties with three or more declared disasters, one recipient takes post-disaster contract dollars after most of them, and its share is far above its share in quiet years.

**A miss means.** The winners change from disaster to disaster. That would say disaster work in a county is not held by a standing set of firms.

**Limits, said out loud.**
- FED_FEMA_DISASTER_DECLARATIONS is one row per disaster per designated area: 70,402 rows over 5,264 disasters. Count disasters with a distinct on `DISASTERNUMBER`. Its dates are ISO text with a Z suffix, not a date type.
- A contract performed in a disaster county after a declaration is not proven to be disaster work. `NATIONAL_INTEREST_ACTION` and `AWARDING_SUB_AGENCY_NAME` narrow it; the fill of both is not yet measured.
- NOAA rows are counties only when `CZ_TYPE` is 'C'. Forecast-zone rows do not map to a county.
- `FEDERAL_ACTION_OBLIGATION` is signed; filter above zero. One firm can appear under several UEIs; `RECIPIENT_PARENT_UEI` fill is not yet measured.

**The picture.** Ranked bars: one bar per county-and-contractor pair, length is the number of separate disasters after which that contractor was paid in that county.

**First cheap check.** Count distinct five-digit county codes in the declarations table that also appear in FY2024 place-of-performance county FIPS.

---

### W56 · Banks under orders keep lending in the same counties

**The physical thing.** The FDIC issues a formal enforcement order against a named bank. That bank takes mortgage applications county by county. The question is whether its county footprint changes after the order.

**Status.** never run

**Data grade.** B. The order-to-bank key is a real FDIC certificate number, but the mortgage files carry no certificate; the bridge to 2018-2024 lending runs through an LEI that is filled on only 8.09% of bank records.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FDIC_ENFORCEMENT_ORDERS | 10,838 | one FDIC enforcement order | 1975-2026 | `CERT_NUMBER` |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_BANK_DATA | 27,836 | one FDIC-insured institution | reports to 2026-03-31 | `CERT`, `LEI` |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS | 2,822,977 | one branch in one survey year | 1994-2025 | `FDIC_CERT` |
| LIBRARY_RAW.LANDING.FED_CFPB_HMDA_LAR_2018 through 2024 (7 tables) | 124,632,830 | one mortgage application | 2018-2024 | `LEI` |
| LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_HISTORIC | 44,992,667 | one mortgage application, old layout | 2015-2017 | `RESPONDENT_ID` + `AGENCY_CODE` |

**Columns that carry it.**
- FDIC_ENFORCEMENT_ORDERS: `CERT_NUMBER` (97.86% filled, 4,326 distinct), `ORDER_DATE` (99.79%), `ORDER_TYPE`, `TERMINATION_DATE` (20.94%), `BANK_RSSD_ID`, `INSTITUTION_NAME`.
- FDIC_BANK_DATA: `CERT` (100.0% filled), `LEI` (8.09% filled, 2,236 distinct), `NAME`, `RSSDID`.
- FDIC_SOD_BRANCH_DEPOSITS: `FDIC_CERT` (100.0%, 15,752 distinct), `SURVEY_YEAR`, `BRANCH_STATE_COUNTY_FIPS` (100.0%, 3,329 distinct), `BRANCH_DEPOSITS_THOUSANDS`.
- HMDA_LAR year tables: `LEI`, `STATE_CODE`, `COUNTY_CODE`, `ACTION_TAKEN`, `LOAN_AMOUNT`, `ACTIVITY_YEAR`. Fill rate not yet measured.
- HMDA_HISTORIC: `RESPONDENT_ID` (100.0%), `AGENCY_CODE`, `STATE_CODE` (98.4%), `COUNTY_CODE` (98.17%), `ACTION_TAKEN`, `AS_OF_YEAR`.

**The join, hop by hop.**
```
FDIC_ENFORCEMENT_ORDERS.CERT_NUMBER ➔ FDIC_BANK_DATA.CERT                     (overlap not yet measured)
FDIC_BANK_DATA.LEI ➔ HMDA_LAR_2018..2024.LEI                                  (overlap not yet measured; LEI filled on 8.09% of bank rows)
FDIC_BANK_DATA.CERT ➔ HMDA_HISTORIC.RESPONDENT_ID, split by AGENCY_CODE        (fact helper records this pair as measured, 70%)
FDIC_ENFORCEMENT_ORDERS.CERT_NUMBER ➔ FDIC_SOD_BRANCH_DEPOSITS.FDIC_CERT       (branch-county footprint; overlap not yet measured)
```

**A hit means.** For banks under an order, the set of counties with originations in the two years after `ORDER_DATE` is nearly the same as the two years before, and volume does not fall relative to peer banks.

**A miss means.** Lending shrinks or moves after an order. That would say orders bite.

**Limits, said out loud.**
- The mortgage files have no ZIP. The original wording asked for ZIPs; county and tract are the finest place the data allows.
- Only FDIC orders are here. Banks supervised by the OCC or the Federal Reserve have no order rows, so large national banks are mostly absent.
- HMDA_HISTORIC `STATE_CODE` and `COUNTY_CODE` are unpadded text and there is no date column, only a year. 19,331 denial rows have a null county. The fact helper shows 2015-2017; the 2026-09-10 probe file calls the same table 2007-2017. This entry uses the fact helper.
- HMDA_LAR_2018 carries 1,961 placeholder rows with `ACTION_TAKEN` '-1' and 2019 carries 21. Filter them before any count.
- "National Association" bank names are one charter. Count by `CERT_NUMBER`, never by bank name.

**The picture.** Small multiples: one panel per bank, x is year relative to the order (-3 to +3), y is count of counties with at least one origination; one mark is one bank-year.

**First cheap check.** Count distinct `CERT_NUMBER` in the orders table that reach a non-blank `LEI` in FDIC_BANK_DATA.

---

### W58 · Small-business loans dry up where local bank absorbed

**The physical thing.** A local bank fails or is merged into another bank. SBA-backed loans keep being approved, or stop being approved, for businesses in that county. The question is what happens to the county's SBA loan count after its bank disappears.

**Status.** never run

**Data grade.** B. Bank events carry a county FIPS and SBA loans run 1991-2026, but SBA names the county in words, so one leg is a county-name join.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_LOANS | 2,174,502 | one SBA-guaranteed loan approval | 1990-10-01 to 2026-03-31 | `PROJECT_COUNTY` + `PROJECT_STATE` |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_BANK_DATA | 27,836 | one FDIC-insured institution, open or closed | end dates 1970-2026 | `CERT`, `FIPS` |
| LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FDIC_FAILED_BANKS | 3,584 | one bank failure | 1970-02-22 to 2026-05-01 | `FDIC_CERT` |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS | 2,822,977 | one branch in one survey year | 1994-2025 | `FDIC_CERT`, `BRANCH_STATE_COUNTY_FIPS` |
| LIBRARY_RAW.LANDING.FED_CENSUS_COUNTY_2020 | 3,235 | one county, name and FIPS | 2020 vintage | `STATE` + `COUNTYNAME` |

**Columns that carry it.**
- FED_SBA_LOANS: `PROJECT_COUNTY`, `PROJECT_STATE`, `APPROVAL_DATE` (100.0% filled), `APPROVAL_FISCAL_YEAR` (100.0%), `GROSS_APPROVAL_AMOUNT`, `LENDER_NAME`, `LENDER_STATE`.
- FDIC_BANK_DATA: `CERT` (100.0%), `FIPS` (100.0%, 2,980 distinct), `ENDEFYMD` (84.62% filled), `SUCCESSOR_CERT` (100.0% filled, 7,943 distinct), `ACTIVE`, `NAME`.
- FDIC_FAILED_BANKS: `FDIC_CERT` (100.0%), `FAIL_DATE` (100.0%), `ACQUIRING_INSTITUTION`, `CITY`, `STATE_ABBR`. `FIPS` is a blank string on all 3,584 rows.
- FDIC_SOD_BRANCH_DEPOSITS: `FDIC_CERT`, `SURVEY_YEAR`, `BRANCH_STATE_COUNTY_FIPS` (100.0%), `SIMS_ACQUIRED_DATE` (50.41% filled), `HOLDING_COMPANY_NAME` (87.37%).
- FED_CENSUS_COUNTY_2020: `STATE`, `STATEFP`, `COUNTYFP`, `COUNTYNAME`. Fill rate not yet measured.

**The join, hop by hop.**
```
FDIC_BANK_DATA (ENDEFYMD filled, SUCCESSOR_CERT present) ➔ the list of absorbed banks, with FIPS
FDIC_FAILED_BANKS.FDIC_CERT ➔ FDIC_BANK_DATA.CERT                            (puts a county on each failure; overlap not yet measured)
FDIC_BANK_DATA.CERT ➔ FDIC_SOD_BRANCH_DEPOSITS.FDIC_CERT                     (branch counties the year before the end date)
FED_SBA_LOANS.PROJECT_COUNTY + PROJECT_STATE ➔ FED_CENSUS_COUNTY_2020.COUNTYNAME + STATE ➔ STATEFP || COUNTYFP   (name join; overlap not yet measured)
county FIPS ➔ county FIPS, SBA loan count by APPROVAL_FISCAL_YEAR before and after the bank's end date
```

**A hit means.** In counties where the absorbed bank held a large share of branch deposits, SBA approvals per year fall after the end date and stay down, while matched counties with no bank exit do not fall.

**A miss means.** SBA approvals hold steady or rise. That would say the acquiring bank or outside lenders filled the gap.

**Limits, said out loud.**
- The failed-banks table's `FIPS` column exists and is empty on every row. County for a failure must come from FDIC_BANK_DATA by certificate number, or from city and state.
- What value `SUCCESSOR_CERT` holds for a bank that is still open has not been checked. Confirm it before treating every filled row as a merger.
- The 2026-09-09 table map calls FDIC_BANK_DATA a 10,000-row sample. The fact helper shows 27,836 rows and 28,119 distinct certificates. This entry uses the fact helper.
- SBA `PROJECT_COUNTY` is a county name. County names repeat across states and spellings vary; the unmatched share is not yet measured.
- SBA loans are one slice of small-business credit. A fall in SBA approvals is not a fall in all lending.

**The picture.** Event-study line: x is years from the bank's end date (-5 to +5), y is SBA approvals per year indexed to 100; one mark is one county-year, with a line for matched control counties.

**First cheap check.** Count distinct `PROJECT_COUNTY` + `PROJECT_STATE` pairs that match exactly one `COUNTYNAME` + `STATE` row.

---

### W59 · Denial rates diverge most between neighboring counties

**The physical thing.** Two counties share a border. Mortgage applicants in one are turned down far more often than applicants next door. The question is which neighbor pairs differ most.

**Status.** never run

**Data grade.** B. County FIPS is a real shared key and the county shapes are profiled, but the 2018-2024 mortgage tables have no measured fill and the neighbor list has to be computed from shapes.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_RAW.LANDING.FED_CFPB_HMDA_LAR_2018 through 2024 (7 tables) | 124,632,830 | one mortgage application | 2018-2024 | `COUNTY_CODE` |
| LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_HISTORIC | 44,992,667 | one mortgage application, old layout | 2015-2017 | `STATE_CODE` + `COUNTY_CODE` |
| LIBRARY_MARTS.REFERENCE.REFERENCE__CENSUS_CB_COUNTY | 3,235 | one county with its boundary shape | one vintage | `GEOID` |

**Columns that carry it.**
- HMDA_LAR year tables: `COUNTY_CODE`, `STATE_CODE`, `ACTION_TAKEN`, `INCOME`, `LOAN_PURPOSE`, `LOAN_AMOUNT`, `ACTIVITY_YEAR`. Fill rate not yet measured.
- HMDA_HISTORIC: `STATE_CODE` (98.4% filled), `COUNTY_CODE` (98.17% filled, 329 distinct, so it is the 3-digit county part), `ACTION_TAKEN`, `APPLICANT_INCOME_000S`, `LOAN_PURPOSE`, `AS_OF_YEAR`.
- CENSUS_CB_COUNTY: `GEOID` (100.0% filled), `NAME`, `STUSPS`, `GEOMETRY`.

**The join, hop by hop.**
```
CENSUS_CB_COUNTY.GEOMETRY touches CENSUS_CB_COUNTY.GEOMETRY ➔ the list of neighbor pairs (self-join, computed; no adjacency table exists)
HMDA_LAR.COUNTY_CODE ➔ CENSUS_CB_COUNTY.GEOID                                              (overlap not yet measured)
lpad(HMDA_HISTORIC.STATE_CODE,2) || lpad(HMDA_HISTORIC.COUNTY_CODE,3) ➔ CENSUS_CB_COUNTY.GEOID   (overlap not yet measured)
```

**A hit means.** A ranked list of bordering county pairs where the denial rate differs by a wide margin in most years, after holding loan purpose and income band the same.

**A miss means.** Neighbors deny at close to the same rate once income and loan purpose are held equal. That would say the gaps on a map are applicant mix, not place.

**Limits, said out loud.**
- HMDA_HISTORIC codes are unpadded text; pad before joining. 19,331 denial rows have a null county and will fall out.
- The review file says the mortgage data runs 2007-2024. The fact helper shows HMDA_HISTORIC at 2015-2017, so the verified span is 2015-2024.
- HMDA_LAR_2018 has 1,961 placeholder rows with `ACTION_TAKEN` '-1', and 2019 has 21. Filter them.
- Small counties have few applications. A pair with a handful of denials will top the list by noise; set a minimum application count.
- The public file has no credit score. A gap that survives income and purpose can still be credit mix.

**The picture.** Map: county borders drawn as lines, line thickness is the denial-rate gap across that border; one mark is one neighbor pair.

**First cheap check.** Count distinct `COUNTY_CODE` values in HMDA_LAR_2024 that match a `GEOID`.

---

### W60 · Banks that failed after 2012: did complaints rise first

**The physical thing.** A bank fails on a known date. Before that date, customers may have filed complaints against it with the CFPB. The question is whether complaint counts climbed in the year before the failure.

**Status.** never run

**Data grade.** B. Both tables are profiled and the dates overlap from 2011-12-01 on, but the only link is the bank's name against the complaint's company name.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FDIC_FAILED_BANKS | 3,584 | one bank failure | 1970-02-22 to 2026-05-01 | `BANK_NAME`, `FDIC_CERT` |
| LIBRARY_MARTS.CONSUMER_PROTECTION.CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS | 17,168,287 | one consumer complaint | 2011-12-01 to 2026-07-23 | `COMPANY` |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS | 2,822,977 | one branch in one survey year | 1994-2025 | `FDIC_CERT` |

**Columns that carry it.**
- FDIC_FAILED_BANKS: `BANK_NAME`, `FDIC_CERT` (100.0% filled), `FAIL_DATE` (100.0%), `STATE_ABBR`, `TOTAL_ASSETS_THOUSANDS`, `ACQUIRING_INSTITUTION`.
- CFPB_COMPLAINTS: `COMPANY` (100.0% filled, 8,088 distinct), `DATE_RECEIVED` (100.0%), `RECEIVED_MONTH`, `PRODUCT`, `STATE`.
- FDIC_SOD_BRANCH_DEPOSITS: `FDIC_CERT`, `INSTITUTION_NAME`, `HOLDING_COMPANY_NAME` (87.37% filled).

**The join, hop by hop.**
```
FDIC_FAILED_BANKS (FAIL_DATE after 2012) .BANK_NAME ➔ CFPB_COMPLAINTS.COMPANY          (name match, multi-word names only; overlap not yet measured)
fallback: FDIC_FAILED_BANKS.FDIC_CERT ➔ FDIC_SOD_BRANCH_DEPOSITS.FDIC_CERT ➔ HOLDING_COMPANY_NAME ➔ CFPB_COMPLAINTS.COMPANY
then count complaints by RECEIVED_MONTH in the 24 months before FAIL_DATE
```

**A hit means.** For failed banks that appear in the complaint file, monthly complaints in the last 12 months run well above the 12 months before that.

**A miss means.** Either complaints stay flat before failure, or the failed banks do not appear in the complaint file at all. The second case says the CFPB file does not reach small failing banks, which ends the question.

**Limits, said out loud.**
- Complaints start 2011-12-01. Most failures in the table cluster in 2008-2012 and have no "before" period; that is why the wording stops at failures after 2012. The count of failures after 2012 is not yet measured.
- The failed-banks `FIPS` column is blank on all 3,584 rows. A place-based version of this question is not possible from this table.
- 77% of the 17.17M complaints are three credit bureaus (TransUnion 4.60M, Equifax 4.51M, Experian 4.12M). Bank complaints are a minority of the file.
- Single-word name matches were measured at 8% real in this warehouse. Use names of two or more words and check the state.

**The picture.** Line chart: x is months before failure (-24 to 0), y is complaints per month; one mark is one bank-month, one line per matched bank.

**First cheap check.** Count failed banks with `FAIL_DATE` after 2012 whose `BANK_NAME` equals any `COMPANY` value.

---

### W61 · Grant recipients with going-concern doubt in their audit keep winning awards

**The physical thing.** An auditor writes in a recipient's federal single audit that the organization may not survive the year. The same organization then receives a new federal grant. The question is how often that happens and to whom.

**Status.** never run

**Data grade.** B. Both sides carry the federal UEI, a real shared id, and the years overlap 2016-2026, but the assistance tables have no measured fill and the going-concern flag's fill has not been measured.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FAC_SINGLE_AUDIT | 411,638 | one single-audit report for one auditee and year | audit years 2016-2026 | `AUDITEE_UEI` |
| LIBRARY_RAW.LANDING.FED_USASPENDING_ASSISTANCE_FY2007 through FY2026 (20 tables) | 128,155,142 | one grant, loan or direct-payment transaction | FY2007-FY2026 | `RECIPIENT_UEI` |

**Columns that carry it.**
- FAC_SINGLE_AUDIT: `AUDITEE_UEI` (100.0% filled, 60,680 distinct), `AUDITEE_EIN` (100.0%), `AUDIT_YEAR` (100.0%), `IS_GOING_CONCERN_INCLUDED` (fill rate not yet measured), `FAC_ACCEPTED_DATE` (100.0%), `TOTAL_AMOUNT_EXPENDED`, `ENTITY_TYPE`, `AUDITEE_NAME`.
- ASSISTANCE_FY tables: `RECIPIENT_UEI`, `RECIPIENT_NAME`, `ACTION_DATE`, `FEDERAL_ACTION_OBLIGATION`, `ASSISTANCE_TYPE_CODE`, `ACTION_TYPE_CODE`, `AWARDING_AGENCY_NAME`. Fill rate not yet measured.

**The join, hop by hop.**
```
FAC_SINGLE_AUDIT (IS_GOING_CONCERN_INCLUDED = yes) .AUDITEE_UEI ➔ ASSISTANCE_FY.RECIPIENT_UEI   (overlap not yet measured)
   with ASSISTANCE_FY.ACTION_DATE after FAC_SINGLE_AUDIT.FAC_ACCEPTED_DATE
```

**A hit means.** A list of auditees flagged for going-concern doubt that received new award actions, with positive obligations, dated after the audit was accepted.

**A miss means.** Flagged auditees get little or nothing new. That would say agencies read the audits, or that flagged auditees are too small to matter.

**Limits, said out loud.**
- `IS_GOING_CONCERN_INCLUDED` is found by name only. Its values and fill are not measured. Two other flags in this warehouse exist by name and are constant on every row; count this one's distinct values first.
- Single audits are filed by nonprofits, governments and universities that spend federal money. Companies that file with the SEC are not in it. This is why the wording moved from "firms win contracts" to "grant recipients win awards".
- A new transaction row is not always a new award. Continuations and modifications of an old grant also appear; `ACTION_TYPE_CODE` separates them, fill not yet measured.
- Loans carry no obligation: assistance types 07 and 08 sum to exactly $0.00 on 11,788,945 rows. Use `FACE_VALUE_OF_LOAN` for those.

**The picture.** Ranked bars: one bar per flagged auditee, length is dollars obligated after the audit's acceptance date.

**First cheap check.** Count distinct values of `IS_GOING_CONCERN_INCLUDED`, then count flagged `AUDITEE_UEI` values that appear in FY2024 assistance.

---

### W62 · 13F holders exit before the first big EPA or mine fine

**The physical thing.** A company's mine or plant is hit with a large federal penalty on a known date. Investment managers held that company's stock the quarter before. The question is whether they sold ahead of the fine.

**Status.** never run

**Data grade.** B. Both fine sides now have one dated row per penalty, mine violations and EPA air enforcement actions, so a company's first big fine can be found; the link to 13F is still a company-name match, and the 13F holdings view has no measured fill.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_HOLDINGS | view, no count | one stock position on one manager's quarterly filing | not yet measured | `ACCESSION_NUMBER`, `NAMEOFISSUER` |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_SUBMISSIONS | 336,124 | one 13F filing | not yet measured | `ACCESSION_NUMBER` |
| LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS | 3,087,265 | one mine-safety violation with its penalty | 1994-09-09 to 2026-07-18 | `CONTROLLER_NAME` |
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS | 106,009 | one formal Clean Air Act enforcement action with its penalty | 1972-10-25 to 2026-07-30 | `PGM_SYS_ID` |
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_PROGRAM_LINKS | 4,406,498 | one EPA program id tied to one facility registry id | no date column | `PGM_SYS_ID`, `REGISTRY_ID` |
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK | 5,300,149 | one EPA facility matched to a corporate parent | no date column | `EPA_REGISTRY_ID`, `PARENT_LEGAL_NAME` |
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__EPA_PENALTY_GAP | 93,808 | one EPA-regulated facility with penalty totals | last action dates to 2026-06-18 | `FRS_ID` |

**Columns that carry it.**
- 13F_HOLDINGS: `ACCESSION_NUMBER`, `NAMEOFISSUER`, `CUSIP`, `SSHPRNAMT`, `VALUE_USD`. Fill not yet measured.
- 13F_SUBMISSIONS: `ACCESSION_NUMBER`, `CIK` (100.0% filled), `PERIODOFREPORT`.
- MSHA_VIOLATIONS: `CONTROLLER_ID` (93.24% filled, 19,855 distinct), `CONTROLLER_NAME`, `VIOLATION_ISSUE_DATE` (100.0%), `PROPOSED_PENALTY`, `AMOUNT_DUE`, `AMOUNT_PAID`.
- ICIS_AIR_FORMAL_ACTIONS: `PGM_SYS_ID`, `ACTIVITY_ID`, `SETTLEMENT_ENTERED_DATE` (99.96% filled), `PENALTY_AMOUNT`, `ENF_TYPE_DESC`, `STATE_EPA_FLAG`. `PGM_SYS_ID` fill rate not yet measured.
- FRS_PROGRAM_LINKS: `PGM_SYS_ACRNM`, `PGM_SYS_ID`, `REGISTRY_ID` (100.0% filled, 3,400,861 distinct).
- XC_EPA_CORPORATE_CROSSWALK: `EPA_REGISTRY_ID` (100.0%), `PARENT_LEGAL_NAME`, `PARENT_CIK` (2.25% filled, 705 distinct).
- EPA_PENALTY_GAP: `FRS_ID` (100.0% filled), `TOTAL_PENALTIES`, `LAST_PENALTY_AMT`, `DATE_LAST_FORMAL_ACTION` (39.47% filled). Used only as a cross-check on totals.

**The join, hop by hop.**
```
mine side:  MSHA_VIOLATIONS.CONTROLLER_NAME ➔ 13F_HOLDINGS.NAMEOFISSUER              (name match, multi-word only; overlap not yet measured)
EPA side:   ICIS_AIR_FORMAL_ACTIONS.PGM_SYS_ID ➔ FRS_PROGRAM_LINKS.PGM_SYS_ID ➔ REGISTRY_ID   (overlap not yet measured)
            FRS_PROGRAM_LINKS.REGISTRY_ID ➔ XC_EPA_CORPORATE_CROSSWALK.EPA_REGISTRY_ID ➔ PARENT_LEGAL_NAME ➔ 13F_HOLDINGS.NAMEOFISSUER   (last hop is a name match; overlap not yet measured)
quarter:    13F_HOLDINGS.ACCESSION_NUMBER ➔ 13F_SUBMISSIONS.ACCESSION_NUMBER ➔ PERIODOFREPORT
first fine: per parent, the earliest SETTLEMENT_ENTERED_DATE or VIOLATION_ISSUE_DATE with a penalty above the chosen floor
```

**A hit means.** For companies whose first penalty above a set size lands in quarter Q, total shares held across managers drops in Q-1 by more than it drops in ordinary quarters.

**A miss means.** Holdings are flat into the fine. That would say fines of this size are not something managers trade on, or not something they see coming.

**Limits, said out loud.**
- There is no SEC enforcement table. The fine side is EPA and mine penalties only, as the rewording says.
- The EPA side with dates is Clean Air Act actions only. Water and hazardous-waste penalties are not in this chain. EPA_PENALTY_GAP covers all programs but holds one row per site with the last penalty only, so it cannot date a first fine.
- `STATE_EPA_FLAG` splits state actions from federal ones. Decide once whether a state fine counts.
- 500,990 of 3,087,265 mine violations carry the standard $100 minimum fine. Set a dollar floor or the "first big fine" is noise.
- Most mine controllers and many plant parents are private and will match no 13F issuer. `PARENT_CIK` is filled on 2.25% of crosswalk rows, 705 parents, which hints at the size of the listed set. The matched count is not yet measured.
- The 13F load missed 7 of 53 source zips while its checksum matched. A missing quarter looks exactly like a sell-off.

**The picture.** Event-study line: x is quarters relative to the fine (-4 to +2), y is shares held indexed to 100; one mark is one company-quarter.

**First cheap check.** Count distinct `PGM_SYS_ID` in ICIS_AIR_FORMAL_ACTIONS with `PENALTY_AMOUNT` above the floor that reach a crosswalk row with a filled `PARENT_CIK`.

---

### W63 · Pension plans that collapsed, and who sponsored them

**The physical thing.** A company's pension plan runs out of money and the federal pension insurer takes it over. Each takeover has a sponsor name, a date and a count of workers in the plan. The question is who the sponsors were and how many people were in the plans.

**Status.** never run

**Data grade.** B. The core answer sits in one profiled table with full dates; adding plan history depends on an EIN join to a filing table that has no measured fill.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.LABOR.LABOR__FED_PBGC_TRUSTEED_PLANS | 5,176 | one pension plan taken over by the federal insurer | 1972-04-01 to 2026-04-30 by termination date | `EIN` |
| LIBRARY_RAW.LANDING.FED_DOL_FORM5500_FULL | 4,299,671 | one annual plan filing | not yet measured | `SPONS_DFE_EIN` |
| LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_DOL_FORM5500 | 33,484 | one annual plan filing, a slice | received 2026-01-02 to 2026-06-24 | `SPONS_DFE_EIN` |

**Columns that carry it.**
- PBGC_TRUSTEED_PLANS: `SPONSOR_NAME`, `PLAN_NAME`, `EIN` (100.0% filled, 4,447 distinct), `DATE_OF_PLAN_TERMINATION` (100.0%), `DATE_OF_PBGC_TRUSTEESHIP` (100.0%), `NUMBER_OF_PARICIPANTS_AT_DATE_OF_PLAN_TERMINATION`, `STATE`.
- FED_DOL_FORM5500_FULL: `SPONS_DFE_EIN`, `SPONSOR_DFE_NAME`, `LAST_RPT_SPONS_EIN`, `LAST_RPT_SPONS_NAME`, `TOT_PARTCP_BOY_CNT`, `FORM_PLAN_YEAR_BEGIN_DATE`, `BUSINESS_CODE`. Fill rate not yet measured.
- FED_DOL_FORM5500 mart: `SPONS_DFE_EIN` (29,301 distinct). Its `EIN` and `SPONSOR_DFE_EIN` columns are blank strings on all 33,484 rows.

**The join, hop by hop.**
```
core: one table, PBGC_TRUSTEED_PLANS grouped by SPONSOR_NAME / EIN, by year of DATE_OF_PLAN_TERMINATION
history: PBGC_TRUSTEED_PLANS.EIN ➔ FED_DOL_FORM5500_FULL.SPONS_DFE_EIN   (overlap not yet measured)
sponsor change: FED_DOL_FORM5500_FULL.LAST_RPT_SPONS_EIN differs from SPONS_DFE_EIN   (a proxy for a change of owner)
```

**A hit means.** A ranked list of sponsors by workers left in collapsed plans, by year, with the sponsors that appear more than once called out.

**A miss means.** Not applicable for the ranking; the table will produce it. For the sponsor-change add-on, a miss means few collapsed plans show a changed sponsor EIN in the years before, or the EIN join finds too few filings to tell.

**Limits, said out loud.**
- There is no buyout or merger table. The original wording asked about collapse "after a buyout"; that cannot be shown. A changed sponsor EIN on the annual filing is a proxy, and private buyers leave no other trace here.
- The Form 5500 mart is a 33,484-row slice received in the first half of 2026, and two of its three EIN columns are empty. Use the 4,299,671-row landing table for history.
- In the mart, `LAST_RPT_SPONS_EIN` is a blank string on 32,680 of 33,484 rows. Expect the same sparseness in the full table until measured.
- The SEC filings mart named in the 2026-09-09 map holds 200 rows for 20 companies. It is left out of this entry because it cannot carry a takeover signal at that size.
- The participant count column is spelled `NUMBER_OF_PARICIPANTS_AT_DATE_OF_PLAN_TERMINATION` in the table, without the T.

**The picture.** Ranked bars: one bar per sponsor, length is workers in collapsed plans, colored by decade of termination.

**First cheap check.** Count distinct PBGC `EIN` values that appear as `SPONS_DFE_EIN` in the full Form 5500 table.

---

### W65 · Parents hide behind most subsidiaries per contract

**The physical thing.** A contract names the company that signed it and, in a second field, that company's ultimate parent. One parent can collect contracts through dozens of differently named subsidiaries. The question is which parents use the most names.

**Status.** never run

**Data grade.** B. Parent and child ids sit on the same row, so there is no join, but the parent id's fill rate has never been measured on these tables.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 through FY2026 (20 tables) | 96,976,021 | one contract transaction | FY2007-FY2026 | `RECIPIENT_PARENT_UEI`, `RECIPIENT_UEI` |
| LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_GLEIF_RELATIONSHIPS | 485,285 | one parent-child link between two legal-entity ids | start dates filled 99.94% | `RELATIONSHIP_STARTNODE_NODEID` |

**Columns that carry it.**
- CONTRACTS_FY tables: `RECIPIENT_PARENT_UEI`, `RECIPIENT_PARENT_NAME`, `RECIPIENT_UEI`, `RECIPIENT_NAME`, `AWARD_ID_PIID`, `FEDERAL_ACTION_OBLIGATION`, `ACTION_DATE_FISCAL_YEAR`. Fill rate not yet measured.
- GLEIF_RELATIONSHIPS: `RELATIONSHIP_STARTNODE_NODEID`, `RELATIONSHIP_ENDNODE_NODEID`, `RELATIONSHIP_RELATIONSHIPTYPE`, `RELATIONSHIP_PERIOD_1_STARTDATE` (99.94% filled). Not joined; see limits.

**The join, hop by hop.**
```
one table family, no join: union the 20 year tables,
group by RECIPIENT_PARENT_UEI, count distinct RECIPIENT_UEI and distinct AWARD_ID_PIID, sum FEDERAL_ACTION_OBLIGATION where above zero
```

**A hit means.** A ranked list of parents with the highest count of distinct subsidiary ids per contract, where the subsidiary names do not contain the parent's name.

**A miss means.** Subsidiary counts track plain company size and the names are obvious variants of the parent. That would say the parent field shows corporate structure, not concealment.

**Limits, said out loud.**
- `RECIPIENT_PARENT_UEI` fill is not yet measured. If it is blank for older years, the ranking is a recent-years ranking.
- The parent field is self-reported in the federal registration system. A parent that does not declare itself is invisible here.
- The ownership-tree table uses LEI. No UEI-to-LEI table exists among the verified tables, so the tree cannot be attached and depth beyond one level cannot be seen.
- The ownership-tree source drops ended relationships from each new release, so it shows current links only.
- "Hide" is a reading, not a measurement. The data shows the count of names; intent is not in the file.

**The picture.** Scatter: x is distinct contracts, y is distinct subsidiary ids, log scale; one mark is one parent.

**First cheap check.** Count rows in FY2024 where `RECIPIENT_PARENT_UEI` is filled and differs from `RECIPIENT_UEI`.

---

### W66 · Charities pay top officer most per revenue dollar

**The physical thing.** A nonprofit's tax return lists each officer by name with total pay. The same filer has a revenue figure. The question is which filers pay their top person the most for each dollar that comes in.

**Status.** never run

**Data grade.** C. Named officer pay exists only for nonprofit hospitals, 3,962 of them; the general charity return table holds 200 rows, so "charities" as a whole cannot be ranked.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.HEALTH.HEALTH__HOSPITAL_OFFICER_PAY | 526,374 | one person listed on one nonprofit hospital's tax return | tax years 2016-2025 | `EIN` |
| LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_BMF | 1,974,830 | one tax-exempt organization on the IRS master file | one snapshot | `EIN` |
| LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_990 | 200 | one nonprofit tax return | tax periods 202312-202512 | `EIN` |

**Columns that carry it.**
- HOSPITAL_OFFICER_PAY: `EIN` (100.0% filled, 3,962 distinct), `TAX_YEAR` (100.0%), `PERSON_NAME`, `TITLE`, `TOTAL_COMPENSATION`, `REPORTABLE_COMP_FROM_RELATED_ORGS`, `IS_SCHEDULE_J_POINTER`, `IS_GROUP_RETURN`, `BMF_REVENUE_AMT`, `HOSPITAL_NAME`.
- FED_IRS_BMF: `EIN` (100.0% filled), `NTEE_CODE`, `REVENUE_AMT`, `ORGANIZATION_NAME`.
- FED_IRS_990: `EIN`, `OFFICER_COMPENSATION_AMT`, `TOTAL_REVENUE_AMT`. 200 rows only.

**The join, hop by hop.**
```
HOSPITAL_OFFICER_PAY.EIN ➔ FED_IRS_BMF.EIN   (fact helper: 3,914 shared values measured against the sister table CORPORATE_REGISTRY__FED_IRS_EO_BMF; against this table not yet measured)
per EIN and TAX_YEAR: max TOTAL_COMPENSATION where IS_SCHEDULE_J_POINTER is false and IS_GROUP_RETURN is false, divided by revenue
```

**A hit means.** A ranked list of nonprofit hospitals where the top person's pay is an outsized share of revenue, stable across more than one tax year.

**A miss means.** Pay per revenue dollar falls smoothly with size and no filer stands out. That would say top pay at nonprofit hospitals scales with the organization.

**Limits, said out loud.**
- The general return table is 200 rows. It cannot rank charities. This entry covers nonprofit hospitals only.
- There is no program-spending column anywhere. The original wording said "per program dollar"; revenue is the only denominator available.
- The revenue figure on the pay table, `BMF_REVENUE_AMT`, is one snapshot from the master file, not the revenue of each tax year. Ratios for older years use the wrong year's revenue.
- A tax return repeats an executive on every affiliate's return with the same dollars. Group by person and tax year and take the max, or one person counts up to five times.
- 239 person-returns carry a pointer line that restates a payout already listed. Rank with `IS_SCHEDULE_J_POINTER` false. 61 rows are group returns that put a whole system's pay on one line. Tax years before 2017 are absent from the source.

**The picture.** Scatter: x is revenue (log), y is top officer pay (log), with a fitted line; one mark is one hospital filer-year, outliers labeled.

**First cheap check.** Count distinct `EIN` in the pay table with `BMF_REVENUE_AMT` above zero.

---

### W67 · Nonprofit revenues spike after disaster declaration

**The physical thing.** A county is declared a federal disaster area. Charities based there file tax returns with a revenue line each year. The question is whether their revenue jumps in the year after the declaration.

**Status.** never run

**Data grade.** D. The only nonprofit return table holds 200 rows, all from tax periods 202312-202512, with a ZIP column that is blank on every row, so there is no revenue history and no place to join on.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_990 | 200 | one nonprofit tax return | tax periods 202312-202512 | `STATE` |
| LIBRARY_RAW.LANDING.FED_FEMA_DISASTER_DECLARATIONS | 70,402 | one disaster by one designated area | not yet measured | `FIPSSTATECODE` + `FIPSCOUNTYCODE` |
| LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS | 26,250,920 | one household's disaster-aid registration | declarations 2002-10-24 to 2026-08-03 | `DAMAGED_ZIP_CODE`, `FIPS` |

**Columns that carry it.**
- FED_IRS_990: `EIN` (100.0% filled, 200 distinct), `TAX_YEAR`, `TOTAL_REVENUE_AMT`, `STATE`, `ZIP_CODE` (blank string on all 200 rows).
- FED_FEMA_DISASTER_DECLARATIONS: `DISASTERNUMBER`, `DECLARATIONDATE`, `STATE`, `FIPSSTATECODE`, `FIPSCOUNTYCODE`, `INCIDENTTYPE`. Fill rate not yet measured.
- FEMA_IA_HOUSING_REGISTRATIONS: `DISASTER_NUMBER` (100.0%, 620 distinct), `DECLARATION_DATE` (100.0%), `DAMAGED_ZIP_CODE` (100.0%), `FIPS` (74.21% filled).

**The join, hop by hop.**
```
FED_IRS_990.STATE ➔ FED_FEMA_DISASTER_DECLARATIONS.STATE   (the only shared place field; state grain)
FED_IRS_990.ZIP_CODE ➔ (blank on every row; no ZIP or county join is possible)
```

**A hit means.** It cannot be produced with the landed return table. With a full return series, a hit would be charities in declared counties showing revenue above their own prior trend the year after.

**A miss means.** Not testable today. 200 returns from one or two tax periods give no before and no after.

**Limits, said out loud.**
- FED_IRS_990 is 200 rows and 200 organizations. Each appears once. A spike needs at least two years per organization.
- Its `ZIP_CODE` column exists and is blank on all 200 rows, so the returns cannot be placed in a county.
- The declarations side is ready: 70,402 rows over 5,264 disasters with padded county FIPS. The gap is entirely on the nonprofit side.
- The master file of tax-exempt organizations has one revenue snapshot per organization and no history, so it cannot stand in.
- Fuller sibling tables exist and do not close the gap. LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_990_EFILE_INDEX (5,544,626 rows, 893,074 distinct `EIN`, submissions 2017-01-03 to 2026-01-01) says who filed for which `TAX_PERIOD` but has no revenue column. LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF (1,983,563 rows) has `ZIP` and `REVENUE_AMT`, one snapshot per organization, no history. Together they can place a filer in a county; they cannot show its revenue by year.
- What would unlock it: the revenue line parsed out of each indexed return, keyed on `OBJECT_ID`, the index's unique column.

**The picture.** Not drawable today. Intended: event-study line, x is tax years from the declaration, y is revenue indexed to 100; one mark is one charity-year.

**First cheap check.** Count `EIN` values in FED_IRS_990 that appear in more than one `TAX_YEAR`. The fact helper's 200 distinct in 200 rows says the answer is zero.

---

### W68 · Nonprofits win grants and register lobbyists

**The physical thing.** A nonprofit receives federal grant money. The same nonprofit is named as the client on a lobbying disclosure filed with the Senate. The question is which organizations do both, and in what order.

**Status.** never run

**Data grade.** B. Both sides cover 1999/2007 through 2026 and overlap FY2007-FY2026, but neither carries an EIN or a shared id, so the link is organization name plus state, and neither landing table has measured fill.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_RAW.LANDING.FED_USASPENDING_ASSISTANCE_FY2007 through FY2026 (20 tables) | 128,155,142 | one grant, loan or direct-payment transaction | FY2007-FY2026 | `RECIPIENT_NAME` + `RECIPIENT_STATE_CODE` |
| LIBRARY_RAW.LANDING.FED_SENATE_LDA_FILINGS | 1,976,696 | one lobbying registration or quarterly report | filing years 1999-2026, all 28 years (review file, checked 2026-09-18) | `CLIENT_NAME` + `CLIENT_STATE` |
| LIBRARY_MARTS.EDUCATION.EDUCATION__FED_SENATE_LDA_FILINGS | 819,649 | one lobbying filing, older partial build | filing years 1999-2021 | `CLIENT_NAME` |

**Columns that carry it.**
- ASSISTANCE_FY tables: `RECIPIENT_NAME`, `RECIPIENT_UEI`, `RECIPIENT_STATE_CODE`, `BUSINESS_TYPES_DESCRIPTION`, `ACTION_DATE`, `FEDERAL_ACTION_OBLIGATION`, `ASSISTANCE_TYPE_CODE`, `AWARDING_AGENCY_NAME`. Fill rate not yet measured.
- FED_SENATE_LDA_FILINGS (landing): `CLIENT_ID`, `CLIENT_NAME`, `CLIENT_STATE`, `FILING_YEAR`, `FILING_PERIOD`, `REGISTRANT_NAME`, `INCOME`, `EXPENSES`, `GOVERNMENT_ENTITIES`, `LOBBYING_ISSUES`. Fill rate not yet measured.

**The join, hop by hop.**
```
ASSISTANCE_FY (BUSINESS_TYPES_DESCRIPTION names a nonprofit) .RECIPIENT_NAME + RECIPIENT_STATE_CODE ➔ FED_SENATE_LDA_FILINGS.CLIENT_NAME + CLIENT_STATE   (name match, multi-word names only; overlap not yet measured)
then order by date: first FILING_YEAR against first ACTION_DATE, and grant dollars by year after the first filing
```

**A hit means.** A list of nonprofits that appear on both sides, with grant dollars by year lined up against lobbying spend by year, and a visible rise in grants after lobbying starts.

**A miss means.** Few nonprofits match, or grant dollars do not move after lobbying begins. That would say nonprofit lobbying is mostly large institutions that were already funded.

**Limits, said out loud.**
- No EIN on either side. The federal spending source publishes no recipient EIN in any file, and lobbying filings carry none. Name plus state is the only link.
- Use the landing table. The older mart stops at 2021 and an earlier note measured it as holding 1999-2010 and 2020-2021 only.
- The review file's body says lobbying filings hold every year but 2017. Its own later check found 2017 present with 77,223 rows. This entry uses the later check.
- `INCOME` and `EXPENSES` are text, and a filing fills one or the other depending on who filed. Cast and combine before summing.
- Universities and hospital systems lobby under a system name and receive grants under a campus name. Those pairs will be missed by an exact name match.

**The picture.** Scatter: x is total lobbying spend, y is total grant dollars, log scale; one mark is one matched nonprofit.

**First cheap check.** Count distinct multi-word `CLIENT_NAME` + `CLIENT_STATE` pairs for filing year 2024 that equal a `RECIPIENT_NAME` + `RECIPIENT_STATE_CODE` pair in FY2024.

---

### W69 · Hospital PACs and hospital employees donate to members

**The physical thing.** A hospital system runs a political committee, and its executives and doctors write personal checks. The money goes to a sitting member's campaign committee. The question is which members receive it and what committees they sit on.

**Status.** never run

**Data grade.** B. Committee, candidate and member ids chain cleanly, but "hospital employee" is a free-text employer field and the contribution table's date window is not re-measured.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS | 283,771,819 | one itemized contribution from one person to one committee | not yet re-measured | `CMTE_ID`, `EMPLOYER` |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES_DIM | view, no count | one political committee, de-duplicated across cycles | cycle column partly null | `CMTE_ID`, `CAND_ID` |
| LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_FEC_ID | 1,715 | one member-to-FEC-candidate-id pairing | no date column | `FEC_ID`, `BIOGUIDE` |
| LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP | 26,970 | one member's seat on one committee in one congress | by congress number | `BIOGUIDE` |
| LIBRARY_MARTS.CORE.XWALK_HOSPITAL_CCN_EIN | 4,003 | one hospital matched to a tax-exempt filer | built 2026-09-11 | `CCN_NAME`, `EIN_NAME` |
| LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_BMF | 1,974,830 | one tax-exempt organization | one snapshot | `ORGANIZATION_NAME`, `NTEE_CODE` |

**Columns that carry it.**
- FEC_INDIV_CONTRIBUTIONS: `CMTE_ID` (100.0% filled, 40,294 distinct), `EMPLOYER`, `OCCUPATION`, `DONOR_NAME`, `TRANSACTION_AMT`, `TRANSACTION_DATE` (99.98%), `TRANSACTION_TYPE`.
- FEC_COMMITTEES_DIM: `CMTE_ID`, `CMTE_NM`, `CONNECTED_ORG_NM`, `ORG_TP`, `CAND_ID`, `CYCLE`, `IS_AMBIGUOUS`. Fill not yet measured by the fact helper.
- MEMBER_FEC_ID: `FEC_ID`, `BIOGUIDE` (99.94% filled, 1,512 distinct), `FULL_NAME`.
- CONGRESS_COMMITTEE_MEMBERSHIP: `BIOGUIDE` (100.0% filled, 1,010 distinct), `CONGRESS`, `COMMITTEE_CODE`, `COMMITTEE_NAME`, `IS_SUBCOMMITTEE`.
- XWALK_HOSPITAL_CCN_EIN: `CCN_NAME`, `EIN_NAME`, `MATCH_TIER`. Fill rate not yet measured.
- FED_IRS_BMF: `ORGANIZATION_NAME`, `NTEE_CODE`, `STATE`.

**The join, hop by hop.**
```
employee leg: FEC_INDIV_CONTRIBUTIONS.EMPLOYER ➔ hospital name list from XWALK_HOSPITAL_CCN_EIN.CCN_NAME / EIN_NAME and FED_IRS_BMF.ORGANIZATION_NAME where NTEE_CODE starts with E2   (text match; overlap not yet measured)
PAC leg:      FEC_COMMITTEES_DIM.CONNECTED_ORG_NM ➔ the same hospital name list   (text match)
FEC_INDIV_CONTRIBUTIONS.CMTE_ID ➔ FEC_COMMITTEES_DIM.CMTE_ID      (measured: 25,960 shared values)
FEC_COMMITTEES_DIM.CAND_ID ➔ MEMBER_FEC_ID.FEC_ID ➔ BIOGUIDE      (overlap not yet measured)
MEMBER_FEC_ID.BIOGUIDE ➔ CONGRESS_COMMITTEE_MEMBERSHIP.BIOGUIDE
```

**A hit means.** Hospital-linked dollars concentrate on members who sit on the health and tax-writing committees, at a rate well above those members' share of all itemized money.

**A miss means.** Hospital money spreads across members about the way all money does. That would say hospital giving follows geography or party, not committee seats.

**Limits, said out loud.**
- A tax-exempt hospital foundation cannot give to a candidate. That is why the wording changed. The signal is the hospital's PAC and the employer line on personal checks.
- This table holds gifts from people. It shows what people gave to a hospital PAC and what hospital employees gave to candidates. The PAC's own checks to candidates are in a different filing that is not among this entry's verified tables.
- The contribution table holds 283,771,819 rows. Older notes describe an 84.2M-row copy that was 99.99% 2023-2026. The window on the current table is not yet re-measured; the fact helper's date range ends in junk values.
- `CYCLE` on the committee view is null on 55% of rows; never filter on it. 14.1% of real money rows (270,519) carry `IS_AMBIGUOUS` true. Both measured 2026-09-01 on the older copy.
- The committee roster is one snapshot per congress and misses about 4% of members per congress, skewed toward people who left mid-term. Dedupe it before joining money, or dollars multiply by seat count.

**The picture.** Ranked bars: one bar per member, length is hospital-linked dollars, colored by whether the member sits on a health or tax committee.

**First cheap check.** Count committees in FEC_COMMITTEES_DIM whose `CONNECTED_ORG_NM` contains HOSPITAL or HEALTH SYSTEM.

---

### W70 · After population explains contracts, which counties get more

**The physical thing.** Federal contract work is performed in a county, and each county has a head count. Bigger counties get more contract dollars. The question is which counties get far more, or far less, than their population predicts.

**Status.** never run

**Data grade.** B. County FIPS is a real shared key, but the only county population landed ends in 2015, so the honest window is FY2007-FY2015.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 through FY2026 (20 tables) | 96,976,021 | one contract transaction | FY2007-FY2026 | `PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_DRUG_POISONING_COUNTY | 53,387 | one county in one year, with population | 1999-2015 | `FIPS` |

**Columns that carry it.**
- CONTRACTS_FY tables: `PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE`, `FEDERAL_ACTION_OBLIGATION`, `ACTION_DATE_FISCAL_YEAR`, `AWARDING_AGENCY_NAME`. County FIPS measured on FY2024 only: 93% filled, 2,894 distinct counties. Other years not yet measured.
- CDC_DRUG_POISONING_COUNTY: `FIPS` (100.0% filled, 3,149 distinct), `YEAR` (100.0%), `POPULATION`, `STATE`, `COUNTY`.

**The join, hop by hop.**
```
CONTRACTS_FY.PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE ➔ CDC_DRUG_POISONING_COUNTY.FIPS, matching fiscal year to YEAR   (overlap not yet measured)
fit log(dollars) on log(POPULATION), rank counties by residual
```

**A hit means.** A short list of counties sitting far above the fitted line year after year, and another far below it, that are not explained by a military base or a national lab.

**A miss means.** Residuals are small or jump around from year to year. That would say population plus a handful of known installations explains county contract flow.

**Limits, said out loud.**
- Population comes from a CDC overdose file, 3,141 counties by the review's count, 1999-2015. There is no county population after 2015. Using 2015 population against FY2016-FY2026 dollars is a stated approximation, not a match.
- The 2020 county names table has no population column. It cannot fill the gap.
- A 300-row contract sample named in the 2026-09-09 map has blank county FIPS on every row. It is not used.
- Fiscal year runs October to September; population is calendar year. The mismatch is small but real.
- `FEDERAL_ACTION_OBLIGATION` is signed; filter above zero or net it on purpose. Place of performance is self-reported by the contracting office.

**The picture.** Scatter: x is county population (log), y is contract dollars (log), fitted line; one mark is one county, outliers labeled.

**First cheap check.** Count distinct place-of-performance county FIPS in FY2015 that match a `FIPS` with `YEAR` 2015.

---

### W71 · After income explains denials, which lenders deny more

**The physical thing.** A lender receives a mortgage application with the applicant's income on it and approves or denies it. Lower incomes are denied more everywhere. The question is which lenders deny more than the incomes they see would predict.

**Status.** never run

**Data grade.** B. From 2018 on the lender id is a clean LEI on every application, but the seven year tables have no measured fill, and lender names come from a 2017-vintage list.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_RAW.LANDING.FED_CFPB_HMDA_LAR_2018 through 2024 (7 tables) | 124,632,830 | one mortgage application | 2018-2024 | `LEI` |
| LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_ARID2017_LEI_XREF | 5,399 | one lender, its 2017 id, its name, its LEI | 2017 vintage | `LEI_2018` |
| LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_HISTORIC | 44,992,667 | one mortgage application, old layout | 2015-2017 | `RESPONDENT_ID` + `AGENCY_CODE` |

**Columns that carry it.**
- HMDA_LAR year tables: `LEI`, `ACTION_TAKEN`, `INCOME`, `DEBT_TO_INCOME_RATIO`, `LOAN_AMOUNT`, `LOAN_PURPOSE`, `LOAN_TYPE`, `STATE_CODE`, `COUNTY_CODE`, `DENIAL_REASON_1`. Fill rate not yet measured. `LEI` has 5,730 distinct values in 2018 (probe file).
- HMDA_ARID2017_LEI_XREF: `ARID_2017`, `RESPONDENT_NAME`, `LEI_2018` (100.0% filled), `LEI_2019` (93.91%), `LEI_2020` (76.5%).
- HMDA_HISTORIC: `RESPONDENT_ID` (100.0% filled, 7,391 distinct), `AGENCY_CODE`, `ACTION_TAKEN`, `APPLICANT_INCOME_000S`, `LOAN_AMOUNT_000S`.

**The join, hop by hop.**
```
core: one table family, no join: HMDA_LAR grouped by LEI, denial share by INCOME band, LOAN_PURPOSE and LOAN_TYPE
names: HMDA_LAR.LEI ➔ HMDA_ARID2017_LEI_XREF.LEI_2018 ➔ RESPONDENT_NAME   (fact helper: 84% measured against a small sample mortgage table, not against the year tables)
older years: HMDA_HISTORIC.RESPONDENT_ID ➔ HMDA_ARID2017_LEI_XREF.ARID_2017   (format match unverified)
```

**A hit means.** A ranked list of lenders whose denial rate, within the same income band, loan type and purpose, sits well above the all-lender rate, year after year.

**A miss means.** Once income, loan type and purpose are held equal, lenders bunch close together. That would say denial gaps between lenders are applicant mix.

**Limits, said out loud.**
- The public file has no credit score. A lender that serves weaker-credit applicants will look harsh. `DEBT_TO_INCOME_RATIO` helps; it is a banded text value and its fill is not measured.
- HMDA_LAR_2018 carries 1,961 placeholder rows with `ACTION_TAKEN` '-1' and a null `LEI`; 2019 carries 21. Filter them.
- Lender names come from a 2017 list. `LEI_2020` is filled on 76.5% of it, and lenders that started after 2017 have no name here.
- The review file says mortgage data runs 2007-2024. The fact helper shows the old-layout table at 2015-2017. Verified span: 2015-2024, with a lender-id change between 2017 and 2018.
- Count people-facing actions only. Purchased loans and withdrawn files are not approvals or denials.

**The picture.** Dot plot: one row per lender, x is denial rate minus the expected rate for its applicant mix; one mark is one lender-year.

**First cheap check.** Count distinct `LEI` in HMDA_LAR_2024 that match `LEI_2018`, `LEI_2019` or `LEI_2020`.

---

### W72 · Contractors suspended and win again under a new name

**The physical thing.** The government bars a company from federal contracts on a known date. A differently named company at the same street address then registers to do federal business and wins a contract. The question is how often that happens.

**Status.** never run

**Data grade.** B. The full exclusion file carries a street address and the federal vendor registry carries a street address, a registration date and a UEI for 895,429 entities, so the chain runs on real fields; "same people" is still inferred from a shared address, and none of the three landing tables has measured fill.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_RAW.LANDING.FED_SAM_EXCLUSIONS_FULL_R2 | 168,328 | one exclusion of one person or firm, full source layout | not yet measured | `ADDRESS_1` + `ZIP_CODE`, `UNIQUE_ENTITY_ID` |
| LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS | 168,328 | the same exclusions, cleaned, without the street | activation dates 93.46% filled, with junk end values | `SAM_NUMBER`, `UEI` |
| LIBRARY_RAW.LANDING.FED_SAM_ENTITY_PUBLIC | 895,429 | one entity registered to do business with the government | not yet measured | `PHYSICAL_ADDRESS_LINE_1` + `PHYSICAL_ADDRESS_ZIP`, `UEI_SAM` |
| LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 through FY2026 (20 tables) | 96,976,021 | one contract transaction | FY2007-FY2026 | `RECIPIENT_UEI` |

**Columns that carry it.**
- FED_SAM_EXCLUSIONS_FULL_R2: `NAME`, `ADDRESS_1`, `CITY`, `STATE_PROVINCE`, `ZIP_CODE`, `UNIQUE_ENTITY_ID`, `CAGE`, `SAM_NUMBER`, `ACTIVE_DATE`, `TERMINATION_DATE`, `EXCLUSION_TYPE`, `CLASSIFICATION`, `CROSS_REFERENCE`. Fill rate not yet measured.
- FED_SAM_EXCLUSIONS (mart): `SAM_NUMBER`, `UEI` (28.33% filled, 38,360 distinct), `ACTIVATION_DATE` (93.46% filled), `IS_ENTITY_NOT_INDIVIDUAL`, `ENTITY_NAME`.
- FED_SAM_ENTITY_PUBLIC: `UEI_SAM`, `CAGE_CODE`, `LEGAL_BUSINESS_NAME`, `DBA_NAME`, `PHYSICAL_ADDRESS_LINE_1`, `PHYSICAL_ADDRESS_CITY`, `PHYSICAL_ADDRESS_ZIP`, `INITIAL_REGISTRATION_DATE`, `ENTITY_START_DATE`, `ELEC_BUS_POC_FIRST_NAME`, `ELEC_BUS_POC_LAST_NAME`, `EXCLUSION_STATUS_FLAG`. Fill rate not yet measured.
- CONTRACTS_FY tables: `RECIPIENT_UEI`, `RECIPIENT_NAME`, `ACTION_DATE`, `FEDERAL_ACTION_OBLIGATION`, `HIGHLY_COMPENSATED_OFFICER_1_NAME`. Fill rate not yet measured.

**The join, hop by hop.**
```
hop 1: FED_SAM_EXCLUSIONS_FULL_R2 (firms only) .ADDRESS_1 + left 5 of ZIP_CODE ➔ FED_SAM_ENTITY_PUBLIC.PHYSICAL_ADDRESS_LINE_1 + PHYSICAL_ADDRESS_ZIP   (address match; overlap not yet measured)
        keep entities whose UEI_SAM differs from UNIQUE_ENTITY_ID, whose LEGAL_BUSINESS_NAME differs from NAME, and whose INITIAL_REGISTRATION_DATE is after ACTIVE_DATE
hop 2: FED_SAM_ENTITY_PUBLIC.UEI_SAM ➔ CONTRACTS_FY.RECIPIENT_UEI, with ACTION_DATE after ACTIVE_DATE   (overlap not yet measured)
second signal: FED_SAM_ENTITY_PUBLIC.ELEC_BUS_POC_LAST_NAME or CONTRACTS_FY.HIGHLY_COMPENSATED_OFFICER_1_NAME shared between the barred firm and the new one
cleaned dates and the firm-or-person flag: FED_SAM_EXCLUSIONS_FULL_R2.SAM_NUMBER ➔ FED_SAM_EXCLUSIONS.SAM_NUMBER
```

**A hit means.** A list of addresses where firm A is barred, firm B registers at the same street address afterward under a different name and id, and firm B then receives contract dollars.

**A miss means.** No second registrant shows up at barred firms' addresses, or none of them wins work. That would say the bar holds, or that successors move address and cannot be seen here.

**Limits, said out loud.**
- A shared office building is not shared ownership. Every address hit needs a second signal, such as a shared contact or officer name, before it is called the same people. Addresses are free text; unit numbers and spelling will break exact matches.
- The vendor registry is a current extract. An entity that registered, won work and let its registration lapse before the extract date may be missing; how far back lapsed entities are kept is not yet measured.
- Exclusions fan out: 1,798 UEIs have three or more overlapping exclusion windows. Use an exists test, not a join, before summing contract dollars.
- In the cleaned mart, `ACTIVATION_DATE` carries sentinel years 1908, 2084 and 2099, and 11,016 nulls, and `TERMINATION_DATE` starts 2026-03-02. The raw `ACTIVE_DATE` has not been profiled; expect the same junk. Whether ended exclusions are kept is not yet measured.
- In the full file, `NPI` holds '0000000000' on 12,027 of 19,238 non-blank rows. It is not used here, but it shows the file's blanks are not always blank.
- `FEDERAL_ACTION_OBLIGATION` is signed; filter above zero or totals during an exclusion window read negative.

**The picture.** Timeline rows: one row per address, a red bar for firm A's exclusion window, a tick for firm B's registration date and dots for firm B's contract actions; one mark is one contract action.

**First cheap check.** Count firm-type exclusion rows whose `ADDRESS_1` + left-5 `ZIP_CODE` equal the `PHYSICAL_ADDRESS_LINE_1` + `PHYSICAL_ADDRESS_ZIP` of a registry entity with a different UEI.

---

### W73 · Pandemic loans went to firms already excluded

**The physical thing.** A business was on a federal do-not-pay list: barred from contracts, or barred from Medicare. It then received a pandemic payroll loan of $150,000 or more. The question is how many did, and for how much.

**Status.** never run

**Data grade.** B. All three tables are landed and the exclusion dates are well filled, but none of them carries an EIN, so the match is business name plus ZIP.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS | 968,524 | one pandemic payroll loan | approval dates not yet measured | `BORROWERNAME` + `BORROWERZIP` |
| LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS | 168,328 | one exclusion from federal contracting | activation dates 93.46% filled | `ENTITY_NAME` + `ZIP` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE | 83,747 | one active exclusion from federal health programs | 1977-07-01 to 2026-08-20 | `BUSINESS_NAME` + `ZIP` |

**Columns that carry it.**
- SBA_PPP_LOANS_150K_PLUS: `BORROWERNAME`, `BORROWERADDRESS`, `BORROWERCITY`, `BORROWERSTATE`, `BORROWERZIP`, `DATEAPPROVED`, `INITIALAPPROVALAMOUNT`, `FORGIVENESSAMOUNT`, `PROCESSINGMETHOD`. Fill rate not yet measured.
- FED_SAM_EXCLUSIONS: `ENTITY_NAME`, `ZIP` (81.9% filled), `ACTIVATION_DATE` (93.46%), `TERMINATION_DATE` (5.5%), `IS_ENTITY_NOT_INDIVIDUAL`, `EXCLUSION_TYPE`.
- FED_HHS_OIG_LEIE: `BUSINESS_NAME`, `ZIP` (100.0% filled), `EXCLUSION_DATE` (100.0%), `ADDRESS`, `IS_ENTITY_NOT_INDIVIDUAL`.

**The join, hop by hop.**
```
SBA_PPP_LOANS_150K_PLUS.BORROWERNAME + left 5 of BORROWERZIP ➔ FED_SAM_EXCLUSIONS.ENTITY_NAME + left 5 of ZIP, with ACTIVATION_DATE before DATEAPPROVED   (name match, multi-word only; overlap not yet measured)
SBA_PPP_LOANS_150K_PLUS.BORROWERNAME + left 5 of BORROWERZIP ➔ FED_HHS_OIG_LEIE.BUSINESS_NAME + ZIP, with EXCLUSION_DATE before DATEAPPROVED      (overlap not yet measured)
```

**A hit means.** A list of borrowers whose name and ZIP match a firm that was already excluded on the day the loan was approved, with loan and forgiveness amounts.

**A miss means.** Near-zero matches. That would say lender screening against the exclusion lists worked for loans of this size, or that barred firms borrowed under another name.

**Limits, said out loud.**
- No EIN on any side. Name plus ZIP is the identity. Multi-word names held up 92% of the time in this warehouse; single-word names 8%.
- The health exclusion list is active exclusions only. A firm excluded in 2019 and reinstated since is gone from the file, so every count is a floor.
- The loan file is labeled 150K-plus but holds 4,092 loans under $150,000. Loans below that size are otherwise not in this table. Split by `PROCESSINGMETHOD`: second-draw loans are capped at exactly $2,000,000.
- The contracting exclusion list's `ACTIVATION_DATE` carries sentinel years 1908, 2084 and 2099, and 11,016 nulls. Drop them before the date test.
- An exclusion of an owner as a person does not show as the business name. Owner-level matches are out of reach; the loan file names the business only.

**The picture.** Ranked bars: one bar per matched borrower, length is loan amount, split by which exclusion list matched.

**First cheap check.** Count rows in the health exclusion list with `IS_ENTITY_NOT_INDIVIDUAL` true whose `BUSINESS_NAME` + `ZIP` equal a `BORROWERNAME` + left-5 `BORROWERZIP`.

---

### W74 · Universities hold NIH grants and pharma-paid faculty

**The physical thing.** A university medical center holds federal research grants, each with named lead scientists. Drug and device makers report payments to named doctors and to named teaching hospitals. The question is which institutions have the most people on both lists.

**Status.** never run

**Data grade.** C. The grant table carries no doctor id and the payment table carries no university, so the link is a person's name plus state, which is a proxy, and the payment table is one year.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_NIH_REPORTER | 2,122,611 | one NIH project in one fiscal year | FY2000-FY2026 | `PI_NAMES`, `ORG_NAME`, `ORG_STATE` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS | 15,385,047 | one payment from a maker to a doctor or teaching hospital | program year 2024 only | `COVERED_RECIPIENT_LAST_NAME` + `COVERED_RECIPIENT_FIRST_NAME`, `NPI` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES | 9,606,683 | one provider id record | enumerated 2005-05-23 to 2026-06-06 | `NPI` |

**Columns that carry it.**
- NIH_REPORTER: `ORG_NAME`, `ORG_UEI` (93.41% filled, 12,286 distinct), `ORG_CITY`, `ORG_STATE`, `PI_NAMES`, `PI_PROFILE_IDS`, `FISCAL_YEAR` (100.0%), `AWARD_AMOUNT`. `ORG_ZIP` and `ORG_FIPS` are 0.0% filled.
- CMS_OPEN_PAYMENTS: `NPI` (974,632 distinct, 48,059 blank strings), `COVERED_RECIPIENT_FIRST_NAME`, `COVERED_RECIPIENT_LAST_NAME`, `RECIPIENT_STATE`, `RECIPIENT_CITY`, `TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS`, `NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE`, `TEACHING_HOSPITAL_NAME`, `CCN` (blank string on 15,350,656 rows).
- CMS_NPPES: `NPI` (100.0% filled), `PROVIDER_LAST_NAME_LEGAL_NAME`, `PROVIDER_FIRST_NAME`, `PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_CITY_NAME`, `PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME`.

**The join, hop by hop.**
```
person leg: NIH_REPORTER.PI_NAMES (FISCAL_YEAR 2024, split to first + last) + ORG_STATE ➔ CMS_OPEN_PAYMENTS.COVERED_RECIPIENT_FIRST_NAME + COVERED_RECIPIENT_LAST_NAME + RECIPIENT_STATE   (name match; overlap not yet measured)
confirm:    CMS_OPEN_PAYMENTS.NPI ➔ CMS_NPPES.NPI, compare practice city to NIH_REPORTER.ORG_CITY
org leg:    NIH_REPORTER.ORG_NAME ➔ CMS_OPEN_PAYMENTS.TEACHING_HOSPITAL_NAME   (name match; overlap not yet measured)
```

**A hit means.** A ranked list of institutions by the number of 2024 grant leads who also appear, same name and same city, as paid doctors in 2024, with dollars on both sides.

**A miss means.** Few grant leads match. Many lead scientists hold a PhD and have no doctor id at all, so a low count would partly reflect who can be paid, not who is.

**Limits, said out loud.**
- There is no doctor id on the grant side and no employer on the payment side. A common name in a large state will match the wrong person. Require the same city and a multi-word, uncommon surname, and treat every count as an estimate.
- The payment table named here is program year 2024 only. 2022 and 2023 sit in separate tables, LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_2022 (13,306,564 rows) and LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_2023 (14,700,786 rows), with zero record overlap. Adding them gives three years, not a long series.
- Payments typed "Debt forgiveness" ($40.8M) and "Acquisitions" ($213M) put people at the top with no check cut. Split by `NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE` before naming anyone as paid.
- Maker names split on letter case ('ABBVIE INC.' and 'AbbVie Inc.'). Fold case before ranking makers.
- The provider registry's EIN column is 0.0% filled. No employer link can be built from it.

**The picture.** Scatter: x is NIH dollars in 2024, y is industry dollars to matched people in 2024; one mark is one institution.

**First cheap check.** Count FY2024 projects where `PI_NAMES` holds exactly one name, then count how many of those names match exactly one paid doctor in the same state.

---

### W75 · NIH grants land where pharma dinners land, by county

**The physical thing.** Research grants are paid to institutions with a registered street address. Drug makers buy meals for doctors who practice in a ZIP code. The question is whether the counties that get the most grant money are the counties where the most meals are bought.

**Status.** never run

**Data grade.** B. The grant table's own ZIP and county columns are empty, but its institution id reaches the federal vendor registry's ZIP on a measured 80% match, and both sides then reach a county through the same ZIP-to-county table; the payment side is one year.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_NIH_REPORTER | 2,122,611 | one NIH project in one fiscal year | FY2000-FY2026 | `ORG_UEI` |
| LIBRARY_RAW.LANDING.FED_SAM_ENTITY_PUBLIC | 895,429 | one entity registered to do business with the government | not yet measured | `UEI_SAM`, `PHYSICAL_ADDRESS_ZIP` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS | 15,385,047 | one payment from a maker to a doctor or teaching hospital | program year 2024 only | `RECIPIENT_ZIP_CODE` |
| LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY | 46,960 | one ZIP-area to county pairing | 2020 vintage | `ZCTA5`, `COUNTY_FIPS` |

**Columns that carry it.**
- NIH_REPORTER: `ORG_UEI` (93.41% filled, 12,286 distinct), `ORG_NAME`, `ORG_CITY`, `ORG_STATE`, `FISCAL_YEAR`, `AWARD_AMOUNT`. `ORG_ZIP` 0.0% filled. `ORG_FIPS` 0.0% filled.
- FED_SAM_ENTITY_PUBLIC: `UEI_SAM`, `LEGAL_BUSINESS_NAME`, `PHYSICAL_ADDRESS_CITY`, `PHYSICAL_ADDRESS_STATE`, `PHYSICAL_ADDRESS_ZIP`. Fill rate not yet measured.
- CMS_OPEN_PAYMENTS: `RECIPIENT_ZIP_CODE` (100.0% filled, 464 blank strings), `NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE`, `TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS`, `PROGRAM_YEAR`.
- XWALK_ZCTA_COUNTY: `ZCTA5`, `COUNTY_FIPS` (100.0% filled, 3,266 distinct).

**The join, hop by hop.**
```
grant side:   NIH_REPORTER.ORG_UEI ➔ FED_SAM_ENTITY_PUBLIC.UEI_SAM                         (fact helper: measured, 80%)
              left 5 of FED_SAM_ENTITY_PUBLIC.PHYSICAL_ADDRESS_ZIP ➔ XWALK_ZCTA_COUNTY.ZCTA5 ➔ COUNTY_FIPS   (overlap not yet measured)
payment side: left 5 of CMS_OPEN_PAYMENTS.RECIPIENT_ZIP_CODE ➔ XWALK_ZCTA_COUNTY.ZCTA5 ➔ COUNTY_FIPS         (overlap not yet measured)
county FIPS ➔ county FIPS, FISCAL_YEAR 2024 against PROGRAM_YEAR 2024
```

**A hit means.** Across counties, grant dollars and food-and-beverage payment dollars rise together more tightly than either does with the count of doctors alone.

**A miss means.** Meal money follows where doctors practice and grant money follows a few research campuses, with little relation between them. That is the likely outcome and is still worth showing.

**Limits, said out loud.**
- The grant table has ZIP and county columns by name and both are empty. The 2026-09-09 map planned to join on them. That plan does not work; the vendor registry supplies the ZIP instead.
- The registry address is the institution's registered office. A university system registered at one address collects grants performed on several campuses, so its home county is overstated.
- The measured match from grant institutions to the registry is 80%, and 6.59% of grant rows have no `ORG_UEI`. Those dollars fall out. `ORG_CITY` plus `ORG_STATE` can place some of them by hand.
- This cannot be done by doctor id. The grant table has no doctor id. The rewording to county is the only honest grain.
- A ZIP area that crosses a county line is a coin flip: 10,186 of 33,791 ZIP areas cross a line, and picking the largest-land county agreed with a known county on 47.1% of those. Census gives no ZIP area to single-building ZIPs, so large medical centers such as Cleveland Clinic 44195, UCSF 94143 and Duke 27710 can miss.
- The payment table named here is 2024 only. Two more years exist as separate tables, LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_2022 (13,306,564 rows) and LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_2023 (14,700,786 rows). As written this is one cross-section, no trend.

**The picture.** Scatter: x is NIH dollars per county in FY2024 (log), y is meal payment dollars per county in 2024 (log); one mark is one county.

**First cheap check.** Count distinct `ORG_UEI` for FISCAL_YEAR 2024 that match a `UEI_SAM` with a filled `PHYSICAL_ADDRESS_ZIP`.

---

### M-239 · Templated CFPB narratives

**The physical thing.** A consumer complaint to the CFPB can include a written story. The same exact story, word for word, shows up on thousands of separate complaints. The question is which texts repeat, how often, and against which companies.

**Status.** partially measured on 2026-08-22 (run date of reports/wonder_rankings.md): the most-repeated narrative appears 27,510 times; the next five appear 24,241 / 18,431 / 15,803 / 12,204 / 10,903 times; 2.57M distinct texts across 3.83M narratives, 67.3% distinct. The by-company breakdown has never been run.

**Data grade.** A. One profiled table, one text column, dates filled 100.0%, and the headline count is already measured.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.CONSUMER_PROTECTION.CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS | 17,168,287 | one consumer complaint | 2011-12-01 to 2026-07-23 | `COMPLAINT_NARRATIVE` |

**Columns that carry it.**
- CFPB_COMPLAINTS: `COMPLAINT_NARRATIVE`, `HAS_NARRATIVE`, `COMPANY` (100.0% filled, 8,088 distinct), `DATE_RECEIVED` (100.0%), `PRODUCT`, `ISSUE`, `SUBMITTED_VIA`, `ZIP_CODE` (99.99%). Narrative fill by the fact helper: not yet measured; the source count is 3.83M narratives.

**The join, hop by hop.**
```
one table, no join: group by COMPLAINT_NARRATIVE (exact text), count rows; then by COMPLAINT_NARRATIVE + COMPANY, and by RECEIVED_MONTH
```

**A hit means.** A short list of exact texts each filed thousands of times, concentrated on a few companies and arriving in bursts on a few dates.

**A miss means.** Already ruled out at the top level: the 27,510-copy text exists. A miss on the second step would be repeats spread evenly over companies and years, which would point to a form letter from the CFPB's own site, not a filing mill.

**Limits, said out loud.**
- There is no complainant id. The data cannot say whether 27,510 copies came from 27,510 people or from one sender.
- 77% of the 17.17M complaints are three credit bureaus (TransUnion 4.60M, Equifax 4.51M, Experian 4.12M). Any by-company ranking of templates will be a ranking of those three unless shown as a share.
- The CFPB blanks personal details in published narratives. Two different stories can look alike after blanking, and one template can split into variants. Exact-match counts are a floor on templating.
- Narratives are published only when the consumer agrees. 3.83M of 17.17M complaints have one; the rest cannot be tested.

**The picture.** Ranked bars: one bar per repeated text (top 50), length is copies, colored by the company it names most.

**First cheap check.** Count rows where `COMPLAINT_NARRATIVE` equals the single most common text, and confirm 27,510.

---

### M-245 · Complaint spike at one credit bureau shows at the others

**The physical thing.** On some days complaints against one credit bureau jump far above normal. The question is whether the other two bureaus jump on the same days, which would point to one sender filing against all three.

**Status.** partially measured on 2026-08-22 (run date of reports/wonder_rankings.md): TransUnion 4.60M, Equifax 4.51M, Experian 4.12M = 77% of 17.17M complaints. The day-by-day spike comparison has never been run.

**Data grade.** A. One profiled table with a daily date filled 100.0% across 2011-12-01 to 2026-07-23, and the company field is filled 100.0%.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.CONSUMER_PROTECTION.CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS | 17,168,287 | one consumer complaint | 2011-12-01 to 2026-07-23 | `COMPANY`, `DATE_RECEIVED` |

**Columns that carry it.**
- CFPB_COMPLAINTS: `COMPANY` (100.0% filled, 8,088 distinct), `DATE_RECEIVED` (100.0%), `PRODUCT`, `ISSUE`, `SUBMITTED_VIA`, `COMPLAINT_NARRATIVE`, `ZIP_CODE` (99.99%).

**The join, hop by hop.**
```
one table, no join: filter COMPANY to the three bureaus, count by COMPANY + DATE_RECEIVED,
flag days above each bureau's own trailing baseline, compare flagged days across the three at lags of -7 to +7 days
```

**A hit means.** Most spike days at one bureau are spike days at the other two within a day or so. That pattern says the driver is outside the companies: a filing service or a campaign.

**A miss means.** Spikes are bureau-specific. That would point to company events, such as an outage or a breach, and each spike could then be dated to a cause.

**Limits, said out loud.**
- The three bureaus can be spelled more than one way in `COMPANY`. List the distinct spellings before filtering; the count of variants is not yet measured.
- `DATE_RECEIVED` is when the CFPB got the complaint, not when the problem happened. Batch uploads and weekends shape the daily series.
- One consumer disputing one report often files against all three bureaus the same day. Same-day movement is the normal baseline, so the test has to be on spikes above that baseline, not on raw correlation.
- There is no complainant id, so the sender behind a shared spike cannot be named from this table. Repeated narrative text (see M-239) is the only fingerprint.

**The picture.** Three stacked daily line charts, one per bureau, x is date, y is complaints per day, with shared spike days shaded; one mark is one bureau-day.

**First cheap check.** Count distinct `COMPANY` spellings containing TRANSUNION, EQUIFAX or EXPERIAN, and confirm the three totals near 4.60M, 4.51M and 4.12M.

---

### M-240 · Companies with one canned complaint response

**The physical thing.** Every complaint gets a closing response from the company, picked from a short list of categories. Some companies close nearly every complaint with the same category. The question is which companies, and which category.

**Status.** partially measured on 2026-08-22 (run date of reports/wonder_rankings.md): Experian 79.2% one category across 4.12M complaints, JPMorgan 79.4%, Wells Fargo 78.9%, Capital One 77.4%. The full top-100 table has never been run.

**Data grade.** A. One profiled table; the response field is 96.92% filled with 8 distinct values, and four companies are already measured.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.CONSUMER_PROTECTION.CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS | 17,168,287 | one consumer complaint | 2011-12-01 to 2026-07-23 | `COMPANY`, `COMPANY_RESPONSE` |

**Columns that carry it.**
- CFPB_COMPLAINTS: `COMPANY` (100.0% filled, 8,088 distinct), `COMPANY_RESPONSE` (96.92% filled, 8 distinct), `COMPANY_PUBLIC_RESPONSE` (52.78% filled, 11 distinct), `IS_TIMELY`, `PRODUCT`, `DATE_RECEIVED` (100.0%).

**The join, hop by hop.**
```
one table, no join: group by COMPANY + COMPANY_RESPONSE, take each company's largest category as a share of its complaints; top 100 companies by volume
```

**A hit means.** A ranked table of the 100 largest companies showing the share of complaints closed with their single most-used category, and how many were closed with any relief.

**A miss means.** Not a yes-or-no question; the table will produce a ranking. The finding would be weak if every large company sits near the same share, which would say the category list, not the company, drives the number.

**Limits, said out loud.**
- The ceiling is bounded. There are only 8 response categories, and "closed with explanation" is the common one for everyone. A 79% share is less strange than it sounds; compare companies within the same product.
- Product mix drives the share. Credit-report disputes close differently from mortgage complaints. Rank within `PRODUCT` or the list just sorts companies by line of business.
- The category is chosen by the company. It records what the company said it did, not what the consumer got.
- 3.08% of rows have no response value. The share of those that are still open is not yet measured.

**The picture.** Stacked horizontal bars: one bar per company, segments are response categories as a share of that company's complaints; one mark is one company-category.

**First cheap check.** List the 8 distinct `COMPANY_RESPONSE` values with their row counts.

---

### WN-143 · CFPB filing language collapses over 14 years

**The physical thing.** In the early years each complaint story was written by a person in their own words. Over time more of them are copies of a template. The question is how the share of unique texts changes year by year from 2011 to 2026.

**Status.** partially measured on 2026-08-22 (run date of reports/wonder_rankings.md): 2.57M distinct texts across 3.83M narratives, 67.3% distinct, all years pooled. The year-by-year series has never been run.

**Data grade.** B. One profiled table with full dates, but how many narratives exist in each year has not been measured, and early years may hold few or none.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.CONSUMER_PROTECTION.CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS | 17,168,287 | one consumer complaint | 2011-12-01 to 2026-07-23 | `COMPLAINT_NARRATIVE`, `RECEIVED_YEAR` |

**Columns that carry it.**
- CFPB_COMPLAINTS: `COMPLAINT_NARRATIVE`, `HAS_NARRATIVE`, `RECEIVED_YEAR` (100.0% filled, 2011-01-01 to 2026-01-01), `RECEIVED_MONTH` (100.0%), `COMPANY` (100.0%), `PRODUCT`. Narrative fill per year: not yet measured.

**The join, hop by hop.**
```
one table, no join: where HAS_NARRATIVE is true, group by RECEIVED_YEAR,
count narratives, count distinct COMPLAINT_NARRATIVE, and the share of narratives held by that year's top 100 texts
```

**A hit means.** The share of distinct texts falls year after year, and a rising share of each year's narratives sits in a small number of repeated texts.

**A miss means.** The distinct share is flat across years. That would say templating is a constant feature of the complaint system, not something that arrived.

**Limits, said out loud.**
- `RECEIVED_YEAR` is stored as a date, the first of January of each year, not as a number. Group on it as is or take its year.
- Narrative counts per year are not measured. If the first years have few narratives, their distinct share will read near 100% from small numbers alone. Show the count beside the share.
- The three credit bureaus are 77% of all complaints. A falling distinct share may be the bureaus' growing share of the file, not a change in how people write. Run the series with and without them.
- Exact-text matching undercounts templating, because the CFPB blanks personal details and templates get lightly edited. The series is a floor.
- 2026 is a partial year, ending 2026-07-23.

**The picture.** Line chart: x is year 2011-2026, y is percent of narratives that are unique texts, with a second line excluding the three bureaus; one mark is one year.

**First cheap check.** Count rows with `HAS_NARRATIVE` true by `RECEIVED_YEAR`.

---

### WN-152 · The donor in the most networks

**The physical thing.** One person, identified by name and ZIP code, writes itemized checks to many different political committees. The question is who gives to the largest number of separate committees, and whether that person gives small amounts everywhere.

**Status.** partially measured on 2026-08-22 (run date of reports/wonder_rankings.md): the top donor by name plus ZIP gave to 268 distinct committees, measured on the older copy of the table with a 2023-2026 window. Not re-run on the current 283,771,819-row table.

**Data grade.** B. One profiled table, but a donor is a name plus a ZIP, not an id, and the current table's date window is not re-measured.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS | 283,771,819 | one itemized contribution from one person to one committee | not yet re-measured | `DONOR_NAME` + `ZIP_CODE` |

**Columns that carry it.**
- FEC_INDIV_CONTRIBUTIONS: `DONOR_NAME`, `ZIP_CODE` (100.0% filled, 321,021 blank strings), `CMTE_ID` (100.0% filled, 40,294 distinct), `TRANSACTION_AMT`, `TRANSACTION_TYPE`, `TRANSACTION_DATE` (99.98%), `EMPLOYER`, `OCCUPATION`, `CYCLE_FILE`.

**The join, hop by hop.**
```
one table, no join: group by DONOR_NAME + left 5 of ZIP_CODE, count distinct CMTE_ID, sum and median TRANSACTION_AMT
```

**A hit means.** A ranked list of donors by distinct committees reached, with the top of the list giving small median amounts to hundreds of committees.

**A miss means.** Not a yes-or-no question; the ranking exists and its top was 268 on the older copy. It would be uninteresting if the top names turn out to be common names in big ZIPs, which is two or more people merged.

**Limits, said out loud.**
- Name plus ZIP is not an id. A common name in a dense ZIP merges different people, and one person who moves or varies their name splits in two. The 268 figure is for a name-ZIP pair, not a proven individual.
- The table holds 283,771,819 rows today. Older notes describe an 84.2M-row copy that was 99.99% 2023-2026. The window on the current table is not yet re-measured; the fact helper's `TRANSACTION_DATE` range runs 0031-04-10 to 9206-07-02, which are junk end dates. The 268 count will likely change on the larger table.
- Gifts routed through a conduit platform appear as earmarked rows, `TRANSACTION_TYPE` 15E. Decide once whether the conduit committee counts as a committee the donor reached; it inflates the count by one and can double the dollars.
- `ZIP_CODE` mixes 5 and 9 digit forms (5,757,830 distinct values). Truncate to 5 before grouping.
- Only itemized gifts are in the file. Small gifts below the itemization threshold, given directly, are not there.

**The picture.** Scatter: x is distinct committees reached (log), y is median gift size (log); one mark is one donor, top 20 labeled by rank only.

**First cheap check.** Count distinct `CMTE_ID` for the single top `DONOR_NAME` + left-5 `ZIP_CODE` pair, and compare with 268.

---

### N6 · Recipients that appear only in FY2020 and FY2021 assistance, then vanish

**The physical thing.** In fiscal 2020 and 2021 the federal assistance ledger swelled with pandemic loans and payments. Some recipients show up in those two years and in no other year from 2007 to 2026. The question is who they are and how much they got.

**Status.** partially measured on 2026-09-18: FY2020 holds 25,183,037 assistance rows and FY2021 holds 20,637,031, together 45,820,068 of 128,155,142. The recipient-level question has never been run.

**Data grade.** B. Twenty year tables with verified row counts and a recipient id on each, but the fill rate of that id has never been measured on any of them.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_RAW.LANDING.FED_USASPENDING_ASSISTANCE_FY2020 | 25,183,037 | one grant, loan or direct-payment transaction | FY2020 | `RECIPIENT_UEI` |
| LIBRARY_RAW.LANDING.FED_USASPENDING_ASSISTANCE_FY2021 | 20,637,031 | one grant, loan or direct-payment transaction | FY2021 | `RECIPIENT_UEI` |
| LIBRARY_RAW.LANDING.FED_USASPENDING_ASSISTANCE_FY2007 through FY2019 and FY2022 through FY2026 (18 tables) | 82,335,074 (128,155,142 minus 45,820,068) | same | FY2007-FY2019, FY2022-FY2026 | `RECIPIENT_UEI` |

**Columns that carry it.**
- ASSISTANCE_FY tables (same 115 columns each): `RECIPIENT_UEI`, `RECIPIENT_DUNS`, `RECIPIENT_NAME`, `RECIPIENT_ADDRESS_LINE_1`, `RECIPIENT_ZIP_CODE`, `ACTION_DATE_FISCAL_YEAR`, `ASSISTANCE_TYPE_CODE`, `FEDERAL_ACTION_OBLIGATION`, `FACE_VALUE_OF_LOAN`, `CFDA_NUMBER`, `CFDA_TITLE`, `BUSINESS_TYPES_DESCRIPTION`, `DISASTER_EMERGENCY_FUND_CODES_FOR_OVERALL_AWARD`. Fill rate not yet measured on any of them.

**The join, hop by hop.**
```
one table family, no join:
set A = distinct RECIPIENT_UEI in FY2020 and FY2021
set B = distinct RECIPIENT_UEI in the other 18 year tables
answer = A minus B, with row counts, FEDERAL_ACTION_OBLIGATION and FACE_VALUE_OF_LOAN summed, grouped by CFDA_TITLE
```

**A hit means.** A large set of recipients seen only in those two years, with their dollars concentrated in a few pandemic programs, and a tail of large recipients with no federal footprint before or since.

**A miss means.** Most two-year recipients also appear in other years. That would say the surge went mainly to organizations the government already knew.

**Limits, said out loud.**
- Loans carry no obligation. Assistance types 07 and 08 sum `FEDERAL_ACTION_OBLIGATION` to exactly $0.00 on 11,788,945 rows; the money sits in `FACE_VALUE_OF_LOAN`, $1.243T in FY2020 alone. A total on obligation drops the whole pandemic-loan story.
- The tables carry two recipient ids, `RECIPIENT_UEI` and the older `RECIPIENT_DUNS`. If older rows were not back-filled with a UEI, a long-standing recipient will look new in 2020. Check `RECIPIENT_UEI` fill by year, and fall back to `RECIPIENT_DUNS` or name plus ZIP, before calling anyone a newcomer.
- Aggregated rows hide individuals. Payments to people are often reported as one county-level row with a generic recipient name. Those are not organizations that vanished; filter them by `RECORD_TYPE_CODE`, fill not yet measured.
- FY2026 is a partial year, and some of its actions are dated ahead, to 2026-09-30, although the archive is stamped 2026-08-06. "Then vanish" has at most four full years of after.
- Most pandemic borrowers were one-time by design. Appearing once is expected; the finding is in the large ones and in clusters at one address.

**The picture.** Ranked bars: one bar per program (`CFDA_TITLE`), length is dollars to two-year-only recipients, with a second bar for recipient count.

**First cheap check.** Count rows with a non-blank `RECIPIENT_UEI` in FY2019, FY2020 and FY2022, to see whether the id is filled on both sides of the surge.

---


# Power: who decides, who watches

### W76 · Immigration judge grant rate drifts with administration

**The physical thing.** One immigration judge, one courtroom, and the share of that judge's completed cases that end in relief instead of a removal order, counted year by year across changes of president.

**Status.** Never run. The tables landed 2026-09-10.

**Data grade.** B, a real shared judge code joins the two tables, but neither table has been profiled, so fill and date range are not yet measured.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_RAW.LANDING.FED_EOIR_PROCEEDING | 16,817,265 | one proceeding in one immigration case | not yet measured | `IJ_CODE` |
| LIBRARY_RAW.LANDING.FED_EOIR_JUDGE | 1,785 | one judge code in the EOIR lookup | no date axis | `JUDGE_CODE` |

**Columns that carry it.**
- LIBRARY_RAW.LANDING.FED_EOIR_PROCEEDING: `IJ_CODE`, `DEC_CODE`, `DEC_TYPE`, `COMP_DATE`, `NAT`, `CASE_TYPE`, `CUSTODY`, `BASE_CITY_CODE`. Fill rate not yet measured on any of them, except the `DEC_CODE` blanks counted below.
- LIBRARY_RAW.LANDING.FED_EOIR_JUDGE: `JUDGE_CODE`, `JUDGE_NAME`. Fill rate not yet measured.

**The join, hop by hop.**
```
FED_EOIR_PROCEEDING.IJ_CODE ➔ FED_EOIR_JUDGE.JUDGE_CODE   (33,135 proceeding rows carry an IJ_CODE absent from the judge table)
group by JUDGE_CODE, year of COMP_DATE, DEC_CODE
```

**A hit means.** The same judge's share of relief decisions moves by a clear step in the year a new administration starts, and the step shows on many judges at once, after holding `NAT` and `CASE_TYPE` constant.

**A miss means.** Each judge's rate is flat across the changeover, or moves only as the mix of nationalities on the docket moves. That says the judge is stable and the caseload changed.

**Limits, said out loud.**
- `DEC_CODE` is blank three ways: NULL on 5.32M rows, a NUL byte on 1.45M, a single space on 729K. A filter of `DEC_CODE IS NOT NULL` keeps 2.18M rows that decided nothing. Use NULLIF(NULLIF(TRIM(col), ''), CHR(0)).
- No lookup table for what each `DEC_CODE` value means is landed. Which codes count as a grant is not yet measured and must be read from EOIR's own code list.
- Judge code AAA is the placeholder "All Judges", not a person.
- The source counted 16,817,336 rows; 71 rows with a stray tab were quarantined, so the table holds 16,817,265.
- The appeals table was not landed and no table says who appointed a judge. "Administration" here is a calendar date, nothing more.

**The picture.** Small-multiple line charts, x = year of `COMP_DATE`, y = relief share, one line per judge, shaded bands per presidential term.

**First cheap check.** Count distinct `IJ_CODE` in the proceeding table that match a `JUDGE_CODE`, and the min and max of `COMP_DATE`.

---

### W77 · Judges hold stock in companies on their own docket

**The physical thing.** A federal judge's yearly financial disclosure lists a company's stock, and the same company's name sits in the caption of a case assigned to that judge.

**Status.** Never run.

**Data grade.** C, the judge id is shared, but the company is matched by free text on both sides and the docket view has never been profiled.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_INVESTMENTS | 1,901,599 | one line on one disclosure form | `TRANSACTION_DATE` 1969-12-31 to 2022-12-27, 36.09% filled | `FINANCIAL_DISCLOSURE_ID` |
| LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_FINANCIAL_DISCLOSURES | 66,287 | one disclosure form | `YEAR_COL` 0 to 14423, 51.3% filled, not usable as is | `PERSON_ID` |
| LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS | view, no count | one court docket | not yet measured | `ASSIGNED_TO_ID` |
| LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_FJC_IDB_CL_LINKED | 10,323,280 | one federal case record with its named parties | `DATE_FILED` 1901-01-01 to 2022-03-31, 100% filled | `ID`, `PLAINTIFF`, `DEFENDANT` |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE | 10,398 | one listed ticker | no date axis | `COMPANY_NAME` |

**Columns that carry it.**
- INVESTMENTS: `DESCRIPTION`, `GROSS_VALUE_CODE`, `FINANCIAL_DISCLOSURE_ID` (fill not yet measured), `TRANSACTION_DATE` (36.09%).
- FINANCIAL_DISCLOSURES: `ID`, `PERSON_ID` (43.8% filled, 3,375 distinct), `YEAR_COL` (51.3%).
- DOCKETS: `ASSIGNED_TO_ID`, `IDB_DATA_ID`, `CASE_NAME`, `DATE_FILED`, `COURT_ID`. Fill rate not yet measured.
- FJC_IDB_CL_LINKED: `ID`, `PLAINTIFF`, `DEFENDANT`, `DATE_FILED` (100%), `NATURE_OF_SUIT`. Fill of the party fields not yet measured.
- COMPANY_TICKERS_EXCHANGE: `COMPANY_NAME` (100%, 7,920 distinct), `CIK` (100%, 8,052 distinct), `TICKER`.

**The join, hop by hop.**
```
INVESTMENTS.FINANCIAL_DISCLOSURE_ID ➔ FINANCIAL_DISCLOSURES.ID            (overlap not yet measured)
FINANCIAL_DISCLOSURES.PERSON_ID ➔ DOCKETS.ASSIGNED_TO_ID                  (overlap not yet measured)
DOCKETS.IDB_DATA_ID ➔ FJC_IDB_CL_LINKED.ID                                (overlap not yet measured; gives party fields instead of a caption)
INVESTMENTS.DESCRIPTION ~ COMPANY_TICKERS_EXCHANGE.COMPANY_NAME ~ FJC_IDB_CL_LINKED.PLAINTIFF / DEFENDANT, or DOCKETS.CASE_NAME   (text match, multi-word names only)
```

**A hit means.** A named judge, a named listed company in that judge's disclosure for year N, and a docket assigned to that judge, filed in year N, with the company in the caption.

**A miss means.** After cash accounts are removed, no judge and company pair lands in the same year. That would say recusal screening works, or that the text match is too weak to see it.

**Limits, said out loud.**
- Rows reading "X Bank Accounts" are cash deposits, not stock; they are 93% of the wide judge-versus-party number. Remove them first.
- The party fields hold the first-named party on each side only, and the linked case file stops at 2022-03-31. The landing copy of the disclosures, LIBRARY_RAW.LANDING.FED_COURTLISTENER_FINANCIAL_DISCLOSURES, holds 70,776 rows against the mart's 66,287; it is unprofiled.
- The disclosure year is column-shifted text on 38,530 of 70,776 rows, and `PERSON_ID` is filled on 43.8% of disclosure rows. More than half the forms cannot be tied to a judge or a year.
- No CIK on the investment side or the docket side. Single-word name matches were 8% real in a checked sample; multi-word names cleared 92%.
- Creditor and asset names are OCR text ("AMCRICAN EXPRESS" on 167 rows), so exact matching misses.
- Holding a stock while a case is assigned is not proof the judge sat on it; the docket does not show recusal.

**The picture.** Network, judges on one side and companies on the other, one edge per judge, company and year where both a holding and a docket exist.

**First cheap check.** Count distinct `PERSON_ID` in FINANCIAL_DISCLOSURES that appear as `ASSIGNED_TO_ID` in DOCKETS.

---

### W78 · Court filings against a chain rise before Medicare fines

**The physical thing.** Federal civil suits naming a nursing-home chain as defendant, counted by month, set next to the dates Medicare fined that chain's homes.

**Status.** Never run.

**Data grade.** C, the court side has no facility id, so the chain is matched by name, and the fine file only covers three years.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CIVIL | 10,857,396 | one federal civil case | `FILE_DATE` 1901-01-01 to 2026-03-31, 100% filled | `DEFENDANT` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME | 14,700 | one nursing home | one snapshot, no date axis | `CMS_CERTIFICATION_NUMBER_CCN` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES | 16,180 | one penalty on one home | `PENALTY_DATE` 2023-06-17 to 2026-05-13, 100% filled | `CMS_CERTIFICATION_NUMBER_CCN` |

**Columns that carry it.**
- FJC_IDB_CIVIL: `DEFENDANT`, `NATURE_OF_SUIT`, `FILE_DATE` (100%), `DISTRICT`. Fill of `DEFENDANT` not yet measured.
- NURSING_HOME: `CMS_CERTIFICATION_NUMBER_CCN` (100%, 14,328 distinct), `CHAIN_ID`, `CHAIN_NAME`, `LEGAL_BUSINESS_NAME`.
- NURSING_HOME_PENALTIES: `CMS_CERTIFICATION_NUMBER_CCN` (100%, 6,771 distinct), `PENALTY_DATE` (100%), `PENALTY_TYPE`, `FINE_AMOUNT`.

**The join, hop by hop.**
```
NURSING_HOME_PENALTIES.CMS_CERTIFICATION_NUMBER_CCN ➔ NURSING_HOME.CMS_CERTIFICATION_NUMBER_CCN   (measured 100%)
NURSING_HOME.CHAIN_NAME / LEGAL_BUSINESS_NAME ~ FJC_IDB_CIVIL.DEFENDANT                           (name match, multi-word names only, overlap not yet measured)
```

**A hit means.** For a chain, suits per quarter climb in the quarters before its first large fine, and the climb is not there for matched chains that were never fined.

**A miss means.** Suit counts are flat before fines, or the name match finds too few cases to count. The second outcome says the court file cannot see chains, not that nothing happened.

**Limits, said out loud.**
- `DEFENDANT` holds the first-named party only. A suit that names the chain second is invisible.
- Fines run 2023-06-17 to 2026-05-13 and court filings stop at 2026-03-31. The window for "before" is under three years.
- `CHAIN_ID` is blank on 4,551 homes in the sibling roster table; count the blank share on this table before grouping. Chain names include hospital systems.
- Only `PENALTY_TYPE` = 'Fine' carries `FINE_AMOUNT`; 2,470 payment-denial rows have a blank `FINE_ID`.
- `COUNTY_FIPS` on the nursing-home table is blank on all 14,700 rows, so a county fallback join does not exist. `JUDGMENT` is filled on 21% of civil cases, so outcomes are mostly unknown.

**The picture.** Timeline per chain, x = month, bars = suits filed, markers = fines, one mark per suit or fine.

**First cheap check.** Count IDB rows whose `DEFENDANT` contains the ten largest multi-word `CHAIN_NAME` values.

---

### W79 · Mine fines unpaid longer under certain operators

**The physical thing.** A mine safety citation with a dollar penalty proposed, the date the penalty became a final order, and the amount the mine's controlling company has paid since.

**Status.** Measured (date not given in the source row; listed as already measured on 2026-09-13): $1.82B proposed vs $1.27B paid across 3.02M penalised violations, 69.9% collected, $548M never collected. Worst named operators paid 7.7%, 7.8%, 9.1%, 14.3%, 17.3%, 19.7%. One holds 1,801 violations, $5.62M proposed, $432,710 paid. The timing half, how long a balance has stayed open, has never been run.

**Data grade.** B, the mine id is shared and the measured half stands on profiled tables, but the date columns that time a debt live only on the unprofiled landing table, and no column dates a payment.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS | 3,087,265 | one citation; the table the measured numbers came from | `VIOLATION_ISSUE_DATE` 1994-09-09 to 2026-07-18, 100% filled | `MINE_ID`, `CONTROLLER_ID` |
| LIBRARY_RAW.LANDING.FED_MSHA_VIOLATIONS | 3,087,266 | one citation, all 64 source columns | not profiled; not yet measured | `VIOLATION_NO`, `MINE_ID`, `CONTROLLER_ID` |
| LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES | 91,906 | one mine | `CURRENT_STATUS_DT` 1925-01-01 to 2026-07-17 | `MINE_ID` |

**Columns that carry it.**
- MSHA_VIOLATIONS (mart): `VIOLATION_NO`, `MINE_ID` (100%, 32,133 distinct), `CONTROLLER_ID` (93.24%, 19,855 distinct), `CONTROLLER_NAME`, `VIOLATION_ISSUE_DATE` (100%), `PROPOSED_PENALTY`, `AMOUNT_DUE`, `AMOUNT_PAID`, `SIG_SUB`, `NEGLIGENCE`. The mart has 27 columns and none of the order, bill or contest dates.
- LANDING.FED_MSHA_VIOLATIONS: `VIOLATION_NO`, `CONTROLLER_ID`, `VIOLATION_ISSUE_DT`, `FINAL_ORDER_ISSUE_DT`, `BILL_PRINT_DT`, `LAST_ACTION_CD`, `LAST_ACTION_DT`, `CONTESTED_IND`, `CONTESTED_DT`, `DOCKET_NO`, `DOCKET_STATUS_CD`, `VACATE_DT`, `PROPOSED_PENALTY`, `AMOUNT_DUE`, `AMOUNT_PAID`. Not profiled; fill rate not yet measured on any of them.
- MSHA_MINES: `MINE_ID` (100%), `CURRENT_OPERATOR_NAME`, `CURRENT_CONTROLLER_ID` (98.88%), `STATE`, `FIPS_CNTY_CD` (100%).

**The join, hop by hop.**
```
MSHA_VIOLATIONS.MINE_ID ➔ MSHA_MINES.MINE_ID   (measured 31,277 shared values)
group by CONTROLLER_ID / CONTROLLER_NAME; sum PROPOSED_PENALTY, sum AMOUNT_PAID            (the measured half)
LANDING.FED_MSHA_VIOLATIONS alone for timing: rows with an unpaid balance, age = today minus FINAL_ORDER_ISSUE_DT, by CONTROLLER_ID   (never run)
LANDING.FED_MSHA_VIOLATIONS.CONTESTED_IND splits the unpaid dollars into contested and not contested   (never run)
```

**A hit means.** A short list of controllers whose paid share sits far below the 69.9% overall rate, and whose unpaid balances sit on final orders that are years old and were never contested. That is a debt left open, not a fine under appeal.

**A miss means.** Paid share is about the same for every controller, or the unpaid dollars are mostly contested or not yet final. Then the $548M gap is the appeal process at work and no operator stands out.

**Limits, said out loud.**
- No column dates a payment. `FINAL_ORDER_ISSUE_DT` is the day the penalty became final and `BILL_PRINT_DT` the day a bill was printed; neither is the day money arrived. What can be timed is how long a balance has been open since the final order. How many days a paid fine took to be paid cannot be shown.
- `LAST_ACTION_DT` dates the last action on the penalty and `LAST_ACTION_CD` says what kind. No code list is landed, so whether any code means "paid" is not yet measured. Until the codes are counted and read against MSHA's own list, do not treat the last action date as a payment date.
- The landing table is unprofiled: fill and date range of every column above are not yet measured. Every value in the MSHA violations data carries literal double quotes; strip them before any compare or date cast.
- `CONTESTED_IND` and `CONTESTED_DT` can answer the open question of whether the gap is contested penalties or plain non-collection, which changes what 69.9% means. Their fill is not yet measured. `VACATE_DT` by name marks citations that were thrown out; those should leave the unpaid count.
- The mines table holds the current operator only. Who ran the mine when it was cited comes from `CONTROLLER_ID` on the violation row, filled on 93.24% of mart rows.
- 500,990 rows carry the standard $100 minimum fine; that is the rulebook, not copy-paste. `AMOUNT_PAID` is zero, not null, when unpaid, so use sums. The last 24 months are inside the appeal window and were excluded from the measured numbers.
- Source notes: an older map gave 13,338+ shared `MINE_ID` values; that figure is the violations-to-accidents overlap, and violations-to-mines is 31,277. The landing table holds one more row than the mart, 3,087,266 against 3,087,265.

**The picture.** Ranked bar chart, x = share of proposed dollars paid, one bar per controller with 100 or more penalised violations; beside it, a dot per controller for the median age in years of its unpaid final orders.

**First cheap check.** On the landing table, with quotes stripped: fill of `FINAL_ORDER_ISSUE_DT`, the count of rows by `CONTESTED_IND`, and the count of rows by `LAST_ACTION_CD`.

---

### W80 · Detention contractors donate where they house detainees

**The physical thing.** A company paid by ICE to run a detention site in a state, and cheques from that company's employees to candidates running in that same state.

**Status.** Never run.

**Data grade.** C, contractor to donor is a name match on the employer field, and no table says which contractor runs which detention site.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 through FED_USASPENDING_CONTRACTS_FY2026 (20 tables) | 96,976,021 | one contract transaction | FY2007-FY2026 | `RECIPIENT_NAME`, `PRIMARY_PLACE_OF_PERFORMANCE_STATE_CODE` |
| LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_FACILITY_CODES | 1,490 | one detention site code | no date axis | `STATE` |
| LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_STINTS | 2,571,975 | one person's stay at one detention site | `BOOK_IN_AT` 2004-12-05 to 2026-03-11, 100% filled; `STAY_BOOK_OUT_DATE` 2022-10-01 to 2026-03-11, 93.24% filled | `DETENTION_FACILITY_CODE`, `STATE` |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS | 283,771,819 | one contribution by one person | window on the current table not yet re-measured | `EMPLOYER`, `CMTE_ID` |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_CAND_CMTE_LINKAGE | 30,536 | one candidate-committee link | not yet measured | `CMTE_ID`, `CAND_ID` |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_CANDIDATES | 27,095 | one candidate in one cycle | not yet measured | `CAND_ID` |

**Columns that carry it.**
- Contract year tables: `RECIPIENT_NAME`, `RECIPIENT_PARENT_NAME`, `RECIPIENT_UEI`, `AWARDING_SUB_AGENCY_NAME`, `ACTION_DATE`, `FEDERAL_ACTION_OBLIGATION`, `PRIMARY_PLACE_OF_PERFORMANCE_STATE_CODE`. Fill not yet measured.
- ICE_DETENTION_FACILITY_CODES: `DETENTION_FACILITY_NAME`, `STATE`, `COUNTY`, `TYPE_DETAILED`.
- ICE_DETENTION_STINTS: `STINT_ID`, `DETENTION_FACILITY`, `DETENTION_FACILITY_CODE`, `STATE`, `COUNTY`, `BOOK_IN_AT` (100%), `DUPLICATE_DROP_ROW`. Fill of the facility code, state and county not yet measured.
- FEC_INDIV_CONTRIBUTIONS: `EMPLOYER`, `DONOR_NAME`, `CMTE_ID` (100%), `TRANSACTION_DATE` (99.98%), `TRANSACTION_AMT`, `TRANSACTION_TYPE`.
- CAND_CMTE_LINKAGE: `CMTE_ID` (100%), `CAND_ID` (100%). FEC_CANDIDATES: `CAND_ID` (100%), `CAND_OFFICE_ST`, `CAND_OFFICE`.

**The join, hop by hop.**
```
contracts.RECIPIENT_NAME ~ FEC_INDIV_CONTRIBUTIONS.EMPLOYER          (name match; first-8-letters rule, overlap not yet measured)
FEC_INDIV_CONTRIBUTIONS.CMTE_ID ➔ CAND_CMTE_LINKAGE.CMTE_ID          (measured 9,217 shared values)
CAND_CMTE_LINKAGE.CAND_ID ➔ FEC_CANDIDATES.CAND_ID                   (measured 14,768 shared values)
contracts.PRIMARY_PLACE_OF_PERFORMANCE_STATE_CODE = FEC_CANDIDATES.CAND_OFFICE_ST
ICE_DETENTION_STINTS grouped by STATE gives the count of people actually held per state, to weight the states   (no key to a contractor)
```

**A hit means.** Employees of a detention contractor give a larger share of their money to candidates in the states where the contractor performs ICE work than to candidates elsewhere.

**A miss means.** The giving follows the company's headquarters state or national party lines, with no pull toward the detention states.

**Limits, said out loud.**
- No contractor-to-facility key exists. The facility-code table, the 163-row LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_FACILITY_LIST and the stints table all carry a facility type and no operator column. The stints table shows how many people were held in each state; it cannot say which company held them.
- The contribution table's `TRANSACTION_DATE` reads 0031-04-10 to 9206-07-02, which are typo dates. An older 84.2M-row copy was 99.99% 2023-2026; the window on the current 283,771,819-row table is not yet re-measured.
- Employer is typed by the donor. Matching the first eight letters of the employer to a firm was 0 of 3 false in a small check; a name-only join inflated counts 9x.
- Earmark pass-through rows are `TRANSACTION_TYPE` 15E and must be excluded.
- Contract dollars are `FEDERAL_ACTION_OBLIGATION`, which is signed. Filter to positive amounts.

**The picture.** Network, contractor on the left, state on the right, edge width = dollars given by the contractor's employees to that state's candidates.

**First cheap check.** Count contribution rows whose `EMPLOYER` starts with the first eight letters of the top five ICE detention `RECIPIENT_NAME` values.

---

### W82 · Bills lobbied hardest before markup, and by whom

**The physical thing.** A quarterly lobbying report that names a bill number in its issue text, and the bill's own record in Congress.

**Status.** Never run. The gap named on 2026-09-09 (lobbying years missing) closed on 2026-09-10/11.

**Data grade.** B, the years now overlap, but the bill number has to be parsed out of free text and there is no markup date column.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_RAW.LANDING.FED_SENATE_LDA_FILINGS | 1,976,696 | one lobbying filing | 1999-2026, all 28 years; 2017 has 77,223 rows | bill number parsed from `SPECIFIC_ISSUES` |
| LIBRARY_MARTS.POLITICS.POLITICS__BILLS | 36,465 | one bill | `INTRODUCED_DATE` 2023-01-03 to 2026-06-26, 100% filled | `CONGRESS` + `BILL_TYPE` + `BILL_NUMBER` |
| LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_SPINE | 12,794 | one member of Congress | no date axis used | `BIOGUIDE` |

**Columns that carry it.**
- LANDING.FED_SENATE_LDA_FILINGS: `FILING_UUID`, `FILING_YEAR`, `FILING_PERIOD`, `CLIENT_NAME`, `REGISTRANT_NAME`, `SPECIFIC_ISSUES`, `INCOME`, `EXPENSES`. Table not profiled; fill rate not yet measured.
- POLITICS__BILLS: `CONGRESS`, `BILL_TYPE`, `BILL_NUMBER`, `TITLE`, `INTRODUCED_DATE` (100%), `ADVANCED_PAST_COMMITTEE`, `LATEST_ACTION_DATE`, `SPONSOR_BIOGUIDE` (100%, 634 distinct).
- MEMBER_SPINE: `BIOGUIDE` (99.9%), `STATE`, `PARTY`.

**The join, hop by hop.**
```
bill reference parsed from LDA.SPECIFIC_ISSUES ➔ BILLS.BILL_TYPE + BILL_NUMBER + CONGRESS   (overlap not yet measured)
BILLS.SPONSOR_BIOGUIDE ➔ MEMBER_SPINE.BIOGUIDE
```

**A hit means.** A ranked list of 2023-2026 bills by count of filings and clients naming them, with the heaviest lobbying falling in the quarters before the bill advanced past committee.

**A miss means.** Bill numbers appear in too few filings to rank, or lobbying volume is no higher before a bill advances than after. The first says the text does not carry bill numbers often enough.

**Limits, said out loud.**
- There is no markup date. The only signals are the `ADVANCED_PAST_COMMITTEE` flag and `LATEST_ACTION_DATE`, so "before markup" becomes "before the quarter of the latest action".
- Lobbying filings are quarterly. Nothing finer than a quarter can be shown.
- The mart copy, LIBRARY_MARTS.EDUCATION.EDUCATION__FED_SENATE_LDA_FILINGS, holds 819,649 rows with `FILING_YEAR` 1999 to 2021 and cannot overlap the 2023-2026 bills. Use the LANDING table.
- `INCOME` and `EXPENSES` are text and mutually exclusive by filer type; a dollar ranking needs both cast and added.
- A bill number like "H.R. 1" repeats every Congress. The parse must pin the Congress from `FILING_YEAR`.

**The picture.** Ranked bar chart, one bar per bill, length = distinct clients naming it, colored by whether it advanced past committee.

**First cheap check.** Count LANDING filings with `FILING_YEAR` 2023 or later whose `SPECIFIC_ISSUES` matches a bill-number pattern.

---

### W83 · 527 groups spend most per registered voter

**The physical thing.** A cheque written by a 527 political group to a payee in a state, divided by the number of registered voters in that state.

**Status.** Never run.

**Data grade.** C, the voter count is one survey vintage with no year column and its registration field is assumed, not documented.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS527_SCHEDULE_B_EXPENDITURES | 8,191,177 | one itemized expenditure by a 527 group | `EXPENDITURE_DATE` 2001-01-01 to 2026-08-27, 99.79% filled | `RECIPIENT_STATE` |
| LIBRARY_MARTS.POLITICS.POLITICS__FED_EAC_EAVS | 6,460 | one election jurisdiction in one survey | one vintage, no year column | `STATE_ABBR` |

**Columns that carry it.**
- IRS527_SCHEDULE_B_EXPENDITURES: `ORG_NAME`, `EIN` (100%, 3,247 distinct), `EXPENDITURE_AMOUNT`, `EXPENDITURE_DATE` (99.79%), `EXPENDITURE_PURPOSE`, `RECIPIENT_STATE` (fill not yet measured).
- FED_EAC_EAVS: `STATE_ABBR`, `FIPSCODE`, `JURISDICTION_NAME`, `A1A`. Fill not yet measured.

**The join, hop by hop.**
```
IRS527_SCHEDULE_B_EXPENDITURES.RECIPIENT_STATE = FED_EAC_EAVS.STATE_ABBR   (state roll-up; sum A1A per state first)
```

**A hit means.** A few small states where 527 dollars per registered voter run several times the national figure, driven by named groups.

**A miss means.** Dollars per voter are about even across states, or the top states are just where political vendors have their offices.

**Limits, said out loud.**
- The voter survey has no year column and one vintage. Spending from 2001 to 2026 is divided by a single registration count.
- No codebook is landed. `A1A` is assumed to be total registered voters. The values -99 and -88 are sentinels on 231 rows.
- Wisconsin reports by municipality, 1,851 rows, so state sums must add them rather than expect one row per county.
- `RECIPIENT_STATE` is where the payee is, not where the ad ran or the voters live. A media buyer in Virginia counts as Virginia.
- Schedule A and Schedule B differ at field 15; this table is Schedule B only, so the date column is the expenditure date.

**The picture.** State map, shade = 527 dollars per registered voter, one mark per state.

**First cheap check.** Sum `A1A` by `STATE_ABBR` with sentinels removed and compare three states to their published registration totals.

---

### W84 · Foreign agents register before trade or arms votes

**The physical thing.** The date a US firm registers as an agent of a foreign government, set against the dates Congress votes on trade or arms measures.

**Status.** Never run.

**Data grade.** C, the two tables share only a calendar date; the country and the subject of a vote must be pulled from vote description text.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.FOREIGN_INFLUENCE.FOREIGN_INFLUENCE__FED_FARA_BULK | 48,103 | one record from the foreign-agent filings | `FOREIGN_PRINCIPAL_REGISTRATION_DATE` 1942-07-03 to 2026-06-11, 17.21% filled | date |
| LIBRARY_RAW.LANDING.FED_FARA_BULK | 221,900 | one record from the foreign-agent filings, the fuller copy | not profiled; not yet measured | date |
| LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_ROLLCALLS | 3,364 | one roll-call vote | `VOTE_DATE` 2023-01-03 to 2026-06-25, 100% filled | date |

**Columns that carry it.**
- FARA_BULK: `REGISTRATION_NUMBER`, `REGISTRANT_NAME`, `FOREIGN_PRINCIPAL_NAME`, `FOREIGN_PRINCIPAL_COUNTRY`, `FOREIGN_PRINCIPAL_REGISTRATION_DATE` (17.21%), `DATE_STAMPED`, `DOCUMENT_TYPE`.
- LANDING.FED_FARA_BULK: `REGISTRATION_NUMBER`, `REGISTRATION_DATE`, `REGISTRANT_NAME`, `FOREIGN_PRINCIPAL_COUNTRY`, `FOREIGN_PRINCIPAL_REGISTRATION_DATE`, `DATE_STAMPED`, `DOCUMENT_TYPE`. Not profiled; fill rate not yet measured.
- VOTEVIEW_ROLLCALLS: `CONGRESS`, `CHAMBER`, `ROLLNUMBER`, `VOTE_DATE` (100%), `BILL_NUMBER`, `VOTE_DESC`, `VOTE_QUESTION`.

**The join, hop by hop.**
```
keyword filter on VOTEVIEW_ROLLCALLS.VOTE_DESC picks trade and arms votes and the country named
FARA_BULK.FOREIGN_PRINCIPAL_COUNTRY = country named in VOTE_DESC   (text match, overlap not yet measured)
FARA_BULK.FOREIGN_PRINCIPAL_REGISTRATION_DATE within N days before VOTEVIEW_ROLLCALLS.VOTE_DATE
```

**A hit means.** New registrations for a country bunch in the 90 days before a vote naming that country, above that country's usual registration pace.

**A miss means.** Registrations show no bunching before votes. Agents register on their own clock, or the votes that matter never name a country in their description.

**Limits, said out loud.**
- Roll calls cover 2023-01-03 to 2026-06-25 only. Foreign-agent registrations dated 1942 to 2022 have no votes to meet.
- There is no vote subject code. "Trade or arms" is a keyword list applied to `VOTE_DESC`; the list decides the answer.
- The principal registration date is filled on 17.21% of rows. Short-form rows keep the date only in `DATE_STAMPED` and the person only in `SHORT_FORM_NAME`; one registration number carries 1,281 rows.
- The mart is 48,103 rows and the landing copy is 221,900. Which records the mart dropped is not yet measured. Count rows dated 2023 or later in both before choosing; the landing copy may hold more registrations inside the vote window, and its date fill is not yet measured.
- No table of arms sales is landed, so an arms vote is only what the vote text says it is.

**The picture.** Timeline, x = date, vertical lines = country-named votes, dots = new foreign-principal registrations for that country.

**First cheap check.** Count roll calls since 2023 whose `VOTE_DESC` contains a country name that also appears in `FOREIGN_PRINCIPAL_COUNTRY`.

---

### W85 · Plant owners donate to regulators' overseers by state

**The physical thing.** A company that owns part of a power plant in a state, and cheques from its employees to members of Congress from that state who sit on the energy committees.

**Status.** Never run.

**Data grade.** C, owner to donor is a name match on the employer field, the owner file is one year, and only congressional committees are landed, not state utility commissions.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_4_OWNER | 5,495 | one owner's share of one generator | one vintage, 2024 per source notes | `PLANT_CODE`, `OWNER_NAME` |
| LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_2_PLANT | 16,132 | one power plant | one vintage | `PLANT_CODE` |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS | 283,771,819 | one contribution by one person | window on the current table not yet re-measured | `EMPLOYER`, `CMTE_ID` |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_CAND_CMTE_LINKAGE | 30,536 | one candidate-committee link | not yet measured | `CMTE_ID`, `CAND_ID` |
| LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_FEC_ID | 1,715 | one member and one FEC candidate id | no date axis | `FEC_ID`, `BIOGUIDE` |
| LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP | 26,970 | one committee seat in one Congress | congresses 113-119 | `BIOGUIDE` |

**Columns that carry it.**
- EIA860_4_OWNER: `PLANT_CODE` (100%, 2,369 distinct), `OWNER_NAME`, `OWNER_STATE`, `PERCENT_OWNED`.
- EIA860_2_PLANT: `PLANT_CODE` (100%, 15,830 distinct), `STATE`, `COUNTY`.
- FEC_INDIV_CONTRIBUTIONS: `EMPLOYER`, `CMTE_ID` (100%), `TRANSACTION_DATE` (99.98%), `TRANSACTION_AMT`, `TRANSACTION_TYPE`.
- CAND_CMTE_LINKAGE: `CMTE_ID`, `CAND_ID`. MEMBER_FEC_ID: `FEC_ID`, `BIOGUIDE` (99.94%), `STATE`.
- COMMITTEE_MEMBERSHIP: `BIOGUIDE` (100%, 1,010 distinct), `COMMITTEE_NAME`, `CONGRESS`, `SNAPSHOT_DATE`.

**The join, hop by hop.**
```
EIA860_4_OWNER.PLANT_CODE ➔ EIA860_2_PLANT.PLANT_CODE                 (measured 100%)
EIA860_4_OWNER.OWNER_NAME ~ FEC_INDIV_CONTRIBUTIONS.EMPLOYER          (name match, overlap not yet measured)
FEC_INDIV_CONTRIBUTIONS.CMTE_ID ➔ CAND_CMTE_LINKAGE.CMTE_ID           (measured 9,217 shared values)
CAND_CMTE_LINKAGE.CAND_ID ➔ MEMBER_FEC_ID.FEC_ID                      (overlap not yet measured)
MEMBER_FEC_ID.BIOGUIDE ➔ COMMITTEE_MEMBERSHIP.BIOGUIDE, COMMITTEE_NAME filtered to energy committees
EIA860_2_PLANT.STATE = MEMBER_FEC_ID.STATE
```

**A hit means.** Employees of plant owners give more to energy-committee members from the states where the owner holds plants than to other members from those states.

**A miss means.** The money goes to energy-committee members regardless of state, or to home-state members regardless of committee. Either way the plant's location adds nothing.

**Limits, said out loud.**
- State utility commissioners are not landed. "Overseers" here means congressional committee seats only.
- The committee roster is one row per Congress per seat. Joining it to money without select distinct multiplied dollars 5.7x in a past check. Dedupe the roster first.
- The roster misses 14 to 35 members per Congress, about 4%, skewed toward members who left mid-term. Its `PARTY` column holds 'majority' and 'minority', not a party.
- The owner file is one year with no time axis. The current contribution table's date window is not yet re-measured; an older 84.2M-row copy was 99.99% 2023-2026.
- The owner file lists 2,369 distinct plants against 15,830 in the plant file. Why the other plants have no owner row is not yet measured; `UTILITY_NAME` on the plant table is the only owner-like field for them.

**The picture.** Network, plant owners to members, edge = dollars, members colored by whether they hold an energy-committee seat.

**First cheap check.** Count distinct `OWNER_NAME` values whose first eight letters match any `EMPLOYER` in the contribution table.

---

### W86 · Lag from complaint spike to enforcement, by bank

**The physical thing.** Consumer complaints about one bank piling up month by month, and the date a federal regulator issued an order against that bank.

**Status.** Never run. Absorbs wonder 54.

**Data grade.** C, the bank is matched by name, and the enforcement table is FDIC only, so the banks that draw the most complaints have no enforcement side here.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.CONSUMER_PROTECTION.CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS | 17,168,287 | one consumer complaint | `DATE_RECEIVED` 2011-12-01 to 2026-07-23, 100% filled | `COMPANY` |
| LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FDIC_ENFORCEMENT_ORDERS | 10,838 | one FDIC enforcement order | `ORDER_DATE` 1975-06-11 to 2026-07-31, 99.79% filled | `BANK_NAME`, `INSTITUTION_NAME` |

**Columns that carry it.**
- CFPB_COMPLAINTS: `COMPLAINT_ID`, `COMPANY` (100%, 8,088 distinct), `DATE_RECEIVED` (100%), `RECEIVED_MONTH` (100%), `PRODUCT`, `ISSUE`, `STATE`.
- FDIC_ENFORCEMENT_ORDERS: `ORDER_ID`, `ORDER_DATE` (99.79%), `ORDER_TYPE`, `INSTITUTION_NAME`, `BANK_NAME`, `BANK_RSSD_ID`, `CERT_NUMBER` (97.86%, 4,326 distinct), `CMP_AMOUNT_TOTAL`, `BANK_STATE`.

**The join, hop by hop.**
```
CFPB_COMPLAINTS.COMPANY ~ FDIC_ENFORCEMENT_ORDERS.BANK_NAME / INSTITUTION_NAME   (name match, multi-word names only, overlap not yet measured)
per bank: month of complaint peak ➔ months until next ORDER_DATE
```

**A hit means.** For banks with both a complaint spike and a later order, the gap clusters around a number of months, and banks with spikes get orders more often than banks without.

**A miss means.** Orders arrive with no relation to complaint volume, or the matched set is too small to say. A small matched set is the likely outcome and says the two files cover different banks.

**Limits, said out loud.**
- The complaint table has no bank id of any kind. The match is on the company name string.
- FDIC orders cover state banks that are not Federal Reserve members. Orders from the OCC, the Federal Reserve and the CFPB itself are not landed. The large national banks that draw most complaints are outside this enforcement file.
- Overlap window is 2011-12-01 to 2026-07-23. Orders before 2011 have no complaint side.
- Bank names ending "National Association" are one entity each and must not be split; generic bank names need `BANK_STATE` to tell apart.
- Three credit bureaus are 77% of complaints per an earlier check and are not banks; filter `PRODUCT` first.

**The picture.** Ranked dot plot, one row per bank, x = months from complaint peak to order, one mark per bank-order pair.

**First cheap check.** Count distinct `BANK_NAME` values that equal a `COMPANY` value after upper-casing and trimming.

---

### W87 · Lobbying spikes before agency rules, by how many weeks

**The physical thing.** Quarterly lobbying reports that list a federal agency as contacted, and the dates that agency published rules in the Federal Register.

**Status.** Never run. Was dead on 2026-09-09 with zero overlapping years; the lobbying backfill of 2026-09-10/11 created the overlap.

**Data grade.** C, lobbying filings are quarterly, so the lead can be shown in quarters and never in weeks as the question asks. A fuller rules table does not change that.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_RAW.LANDING.FED_SENATE_LDA_FILINGS | 1,976,696 | one lobbying filing | 1999-2026, all 28 years; 2017 has 77,223 rows | `GOVERNMENT_ENTITIES` |
| LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS | 94,731 | one Federal Register document | `PUBLICATION_DATE` 2023-01-03 to 2026-06-16, 100% filled | `AGENCY` |
| LIBRARY_RAW.LANDING.FED_FEDERAL_REGISTER_DOCUMENTS | 485,594 | one Federal Register document, the fuller copy | not profiled; `PUBLICATION_DATE` range not yet measured | `AGENCY_NAMES` |

**Columns that carry it.**
- LANDING.FED_SENATE_LDA_FILINGS: `FILING_YEAR`, `FILING_PERIOD`, `CLIENT_NAME`, `GOVERNMENT_ENTITIES`, `LOBBYING_ISSUES`, `SPECIFIC_ISSUES`. Table not profiled; fill rate not yet measured.
- FEDERAL_REGISTER_DOCUMENTS: `DOCUMENT_NUMBER`, `AGENCY`, `AGENCIES`, `TYPE`, `PUBLICATION_DATE` (100%), `PUBLICATION_QUARTER` (100%), `IS_SIGNIFICANT`, `REGULATION_ID_NUMBERS`.
- LANDING.FED_FEDERAL_REGISTER_DOCUMENTS: `DOCUMENT_NUMBER`, `AGENCIES`, `AGENCY_NAMES`, `TYPE`, `PUBLICATION_DATE`, `SIGNIFICANT`, `REGULATION_ID_NUMBERS`. It has no `AGENCY`, `IS_SIGNIFICANT` or `PUBLICATION_QUARTER` column; the mart builds those. Fill rate not yet measured.

**The join, hop by hop.**
```
agency names split out of LDA.GOVERNMENT_ENTITIES text = FEDERAL_REGISTER_DOCUMENTS.AGENCY   (text match, overlap not yet measured)
LDA.FILING_YEAR + FILING_PERIOD (quarter) ➔ FEDERAL_REGISTER_DOCUMENTS.PUBLICATION_QUARTER
```

**A hit means.** Filings naming an agency rise in the one or two quarters before that agency publishes a significant rule, above the agency's own baseline.

**A miss means.** Filing counts per agency are flat around rule dates. Lobbying volume follows the congressional calendar, not the rule docket.

**Limits, said out loud.**
- Grain is a quarter. "By how many weeks" cannot be answered with this data.
- On the mart the overlap is 2023-01-03 to 2026-06-16, a short series for any lead-lag claim. The landing copy holds 485,594 rows against the mart's 94,731, so it may reach back before 2023 and lengthen the series, but its date range is not yet measured. Measure it before choosing the table.
- `GOVERNMENT_ENTITIES` is a free-text list per filing and the Federal Register uses its own agency names. The match needs a hand-built alias list, and a filing that names ten agencies counts toward all ten.
- The mart copy of the lobbying table stops at `FILING_YEAR` 2021 and has zero overlap. Use the LANDING table.
- A filing naming an agency does not say which rule was discussed; `REGULATION_ID_NUMBERS` has no partner on the lobbying side.

**The picture.** Small multiples per agency, x = quarter, bars = filings naming the agency, markers = significant rules published.

**First cheap check.** Min and max of `PUBLICATION_DATE` on the landing Federal Register table; then count LANDING lobbying filings from 2023 on, and list the top 20 distinct agency strings inside `GOVERNMENT_ENTITIES` beside the top 20 `AGENCY` values.

---

### W88 · Judges' former firms appear most on their dockets

**The physical thing.** The law firm a judge worked at before the bench, and that firm's name in the attorney block of opinions from cases assigned to that judge.

**Status.** Never run.

**Data grade.** C, attorney names exist only on opinion records, which are a small slice of all dockets, and the firm is matched by text.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_POSITIONS | 51,290 | one job held by one judge | `DATE_START` not profiled; fill not yet measured | `PERSON_ID` |
| LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS | view, no count | one court docket | not yet measured | `ASSIGNED_TO_ID`, `ID` |
| LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_OPINION_CLUSTERS | 10,070,727 | one decided opinion group | `DATE_FILED` 0019-01-31 to 2028-04-13, contains typo dates | `DOCKET_ID` |

**Columns that carry it.**
- POSITIONS: `PERSON_ID` (100%, 15,524 distinct), `POSITION_TYPE`, `SECTOR`, `ORGANIZATION_NAME`, `DATE_START`, `DATE_TERMINATION`, `LOCATION_STATE`.
- DOCKETS: `ID`, `ASSIGNED_TO_ID`, `DATE_FILED`, `COURT_ID`. Fill not yet measured.
- OPINION_CLUSTERS: `DOCKET_ID` (100%, 9,924,437 distinct), `ATTORNEYS` (fill not yet measured), `DATE_FILED` (100%).

**The join, hop by hop.**
```
POSITIONS.PERSON_ID ➔ DOCKETS.ASSIGNED_TO_ID              (overlap not yet measured; an earlier note counts 3,350 judges on ASSIGNED_TO_ID)
DOCKETS.ID ➔ OPINION_CLUSTERS.DOCKET_ID                   (overlap not yet measured)
POSITIONS.ORGANIZATION_NAME ~ text inside OPINION_CLUSTERS.ATTORNEYS   (multi-word firm names only)
```

**A hit means.** For a judge, the former firm appears in the attorney block more often than it does before other judges of the same court.

**A miss means.** Former firms appear no more often than chance, or `ATTORNEYS` is too sparsely filled to test. The second would end the question on this data.

**Limits, said out loud.**
- No docket-level attorney table exists. Attorney text lives only on opinion records, so cases that settled or ended without an opinion are invisible.
- Fill of `ATTORNEYS` is not yet measured. It must be counted, by year, before anything else.
- `DATE_FILED` on opinions runs from year 0019 to 2028. Bound dates before use.
- Firm names change and merge. A text match on the old name misses the firm's later names.
- An appearance is not by itself a conflict. `DATE_TERMINATION` of the firm job must be compared with the case date, and the data does not show whether the judge recused.

**The picture.** Ranked bar chart, one bar per judge, length = share of that judge's opinions where the former firm appears, with the court's average as a reference line.

**First cheap check.** Share of OPINION_CLUSTERS rows where `ATTORNEYS` is non-blank, by decade of `DATE_FILED`.

---

### W89 · Which agency jobs appear most in lobbyists' covered-position text

**The physical thing.** The line on a lobbying form where a lobbyist writes the government job they used to hold, such as "Chief of Staff, Senate Finance Committee".

**Status.** Never run. Reworded on 2026-09-18 because the second table lists job slots, not people.

**Data grade.** B, one table carries the whole answer, but the field is free text and the profiled copy holds a single filing year.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.POLITICS.POLITICS__FED_SENATE_LDA_LOBBYIST_POSITIONS | 140,463 | one lobbyist on one filing | `FILING_YEAR` min 2011, max 2011 when profiled 2026-09-08 | `COVERED_POSITION` |
| LIBRARY_MARTS.GOVERNANCE.GOVERNANCE__FED_REVOLVINGDOOR_PROJECT | 405 | one government job slot | no date axis | `AGENCY`, `POSITION_NAME` |

**Columns that carry it.**
- LDA_LOBBYIST_POSITIONS: `LOBBYIST_ID`, `LOBBYIST_FIRST_NAME`, `LOBBYIST_LAST_NAME`, `COVERED_POSITION`, `HAS_COVERED_POSITION`, `REGISTRANT_NAME`, `CLIENT_NAME`, `FILING_YEAR` (100%). Fill of `COVERED_POSITION` not yet measured.
- REVOLVINGDOOR_PROJECT: `AGENCY`, `POSITION_NAME`, `POSITION_TYPE`, `INDUSTRY_SECTOR`, `IS_SENATE_CONFIRMED`.

**The join, hop by hop.**
```
one table carries it: group by agency keywords found in LDA_LOBBYIST_POSITIONS.COVERED_POSITION, count distinct LOBBYIST_ID
optional label: agency keyword ~ REVOLVINGDOOR_PROJECT.AGENCY   (job text to job slot, not person to person)
```

**A hit means.** A ranked list of agencies and offices by how many distinct lobbyists name them as a past job, with a clear top tier.

**A miss means.** After junk text is removed, too few real positions are left to rank, or they spread evenly. That says the field is not filled well enough to use.

**Limits, said out loud.**
- `HAS_COVERED_POSITION` is a not-null test, and old years fill the blank with text. In 1999, 205,142 of 213,881 rows hold the literal 'N/A'. Null out 'N/A', 'n/a', 'NA', 'NONE' and 'See prior filing' first; 1999 then drops to about 8,700 rows, 4%.
- Sources disagree on what the table holds. The 2026-09-08 profile shows 140,463 rows, all `FILING_YEAR` 2011. A 2026-09-11 note counts 213,881 rows for 1999 alone and calls 1999-2010 lobbyist seats "never walked". Count rows per year before trusting any trend.
- The job-slot table has no person names and no year. Its two appointee flags were false on every row and were replaced by `IS_SENATE_CONFIRMED`, true on 190 of 405. It can label an agency; it cannot confirm a person held a job.
- "Vice versa", regulators who used to be lobbyists, has no table at all.
- The same lobbyist repeats across filings and quarters. Count distinct `LOBBYIST_ID`, not rows.

**The picture.** Ranked bar chart, one bar per agency or congressional office, length = distinct lobbyists naming it.

**First cheap check.** Count rows per `FILING_YEAR`, and the top 20 raw `COVERED_POSITION` strings.

---

### W90 · Detention contracts grow where ICE detainers grow

**The physical thing.** Detainer requests ICE sends to local jails, counted by county and year, next to federal contract dollars for detention work performed in the same county.

**Status.** Never run. The gap named on 2026-09-09 (no county code on contracts) closed on 2026-09-10.

**Data grade.** B, both sides reach county, but the detainer side gets there through a county name, and detainers cover under four years.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETAINERS | 609,769 | one detainer request | `DETAINER_PREPARE_DATE` 2022-10-01 to 2026-08-25, 100% filled | `DETENTION_FACILITY_CODE` |
| LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_FACILITY_CODES | 1,490 | one detention site code | no date axis | `DETENTION_FACILITY_CODE`, `COUNTY`, `STATE` |
| LIBRARY_RAW.LANDING.FED_CENSUS_COUNTY_2020 | 3,235 | one county | 2020 | `STATE`, `COUNTYNAME` ➔ `STATEFP` + `COUNTYFP` |
| LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 through FED_USASPENDING_CONTRACTS_FY2026 (20 tables; FY2023-FY2026 overlap the detainers) | 96,976,021 | one contract transaction | FY2007-FY2026 | `PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE` |

**Columns that carry it.**
- ICE_DETAINERS: `DETAINER_PREPARE_DATE` (100%), `DETENTION_FACILITY_CODE`, `FACILITY_STATE`, `DUPLICATE_LIKELY`. Fill of the facility code not yet measured.
- ICE_DETENTION_FACILITY_CODES: `DETENTION_FACILITY_CODE`, `COUNTY`, `STATE`, `TYPE_DETAILED`.
- FED_CENSUS_COUNTY_2020: `STATE`, `STATEFP`, `COUNTYFP`, `COUNTYNAME`. Not profiled.
- Contract year tables: `AWARDING_SUB_AGENCY_NAME`, `PRODUCT_OR_SERVICE_CODE`, `ACTION_DATE`, `FEDERAL_ACTION_OBLIGATION`, `PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE` (filled on 93% of FY2024 rows, 2,894 distinct counties; other years not yet measured).

**The join, hop by hop.**
```
ICE_DETAINERS.DETENTION_FACILITY_CODE ➔ ICE_DETENTION_FACILITY_CODES.DETENTION_FACILITY_CODE   (overlap not yet measured)
ICE_DETENTION_FACILITY_CODES.COUNTY + STATE ➔ FED_CENSUS_COUNTY_2020.COUNTYNAME + STATE ➔ STATEFP||COUNTYFP   (name match, overlap not yet measured)
STATEFP||COUNTYFP = contracts.PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE, filtered to ICE as awarding sub-agency
```

**A hit means.** Counties where detainers rose most between fiscal 2023 and 2026 also show the largest growth in ICE detention contract dollars.

**A miss means.** Contract dollars sit in a few fixed counties no matter where detainers rise. That says detention capacity is bought where the beds already are.

**Limits, said out loud.**
- Detainers run 2022-10-01 to 2026-08-25. Only FY2023 through FY2026 overlap, and FY2026 is partial on both sides.
- The county on the detention side is a name, not a code. County names repeat across states and spell "Saint" several ways; the match must use state plus name and will drop some rows.
- A detainer is a request to a jail, not a person held. The facility code on a detainer names the ICE site tied to the request, not a contract.
- Do not use LIBRARY_MARTS.REFERENCE.REF__DIM_GEOGRAPHY for county codes: it holds two code forms per county and drops counties with no EPA facility. Do not use the 36-column contracts view; it has no county code.
- The facility-code table has a type column and no operator or contract column. Nothing ties a contract row to a named detention site; the county is the only meeting point.

**The picture.** County scatter, x = change in detainers, y = change in ICE detention contract dollars, one mark per county.

**First cheap check.** Count detainer rows whose `DETENTION_FACILITY_CODE` finds a row in the facility-code table with a non-blank `COUNTY`.

---

### W91 · Immigration judges furthest from their own court's average

**The physical thing.** One immigration judge's share of removal orders, compared with the other judges hearing cases in the same court city in the same years.

**Status.** Never run. Reworded on 2026-09-18: judges landed 2026-09-10; the appeals table and any record of who appointed a judge did not.

**Data grade.** B, a real shared judge code and a court code on every row, but neither table has been profiled.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_RAW.LANDING.FED_EOIR_PROCEEDING | 16,817,265 | one proceeding in one immigration case | not yet measured | `IJ_CODE`, `BASE_CITY_CODE` |
| LIBRARY_RAW.LANDING.FED_EOIR_JUDGE | 1,785 | one judge code in the EOIR lookup | no date axis | `JUDGE_CODE` |

**Columns that carry it.**
- FED_EOIR_PROCEEDING: `IJ_CODE`, `BASE_CITY_CODE`, `DEC_CODE`, `DEC_TYPE`, `COMP_DATE`, `NAT`, `CASE_TYPE`, `CUSTODY`, `ABSENTIA`. Fill rate not yet measured.
- FED_EOIR_JUDGE: `JUDGE_CODE`, `JUDGE_NAME`, `BLNACTIVE`. Fill rate not yet measured.

**The join, hop by hop.**
```
FED_EOIR_PROCEEDING.IJ_CODE ➔ FED_EOIR_JUDGE.JUDGE_CODE   (33,135 proceeding rows carry an IJ_CODE absent from the judge table)
per BASE_CITY_CODE and year of COMP_DATE: judge's decision mix minus the court's decision mix
```

**A hit means.** A short list of judges whose removal share sits far from their court's figure year after year, with enough completed cases that it is not noise, and with `NAT` and `CUSTODY` held constant.

**A miss means.** Judges inside a court sit close together once the mix of nationality and custody is held constant. The spread across the country is between courts, not between judges.

**Limits, said out loud.**
- `DEC_CODE` is blank three ways: NULL 5.32M rows, NUL byte 1.45M, single space 729K. A plain not-null filter keeps 2.18M rows that decided nothing.
- No lookup for `DEC_CODE` meanings or for `BASE_CITY_CODE` names is landed as a table. The source zip holds a judge-by-base-city lookup of 12,566 rows that was not landed.
- Judge code AAA is the placeholder "All Judges". Exclude it.
- The data does not show how cases are assigned to judges inside a court. Without `CUSTODY`, `CASE_TYPE` and `NAT` held constant, an outlier may be a kind of docket, not a judge.
- Reversal on appeal and the appointing official cannot be shown; neither was landed.

**The picture.** Strip plot per court, x = removal share, one dot per judge, the court average as a vertical line.

**First cheap check.** Count judges with 500 or more non-blank `DEC_CODE` rows, and the number of distinct `BASE_CITY_CODE` values.

---

### W92 · Foreign-owned contractors win more in certain agencies

**The physical thing.** A federal contract payment to a company flagged as foreign-owned, tallied by the agency that signed it.

**Status.** Never run. The gap named on 2026-09-09 (no foreign-entity code, no agency code) closed on 2026-09-10. Absorbs wonder 93, defense versus health.

**Data grade.** B, one table family with the flag and the agency code on the same row, but the fill of the flag has not been measured.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 through FED_USASPENDING_CONTRACTS_FY2026 (20 tables) | 96,976,021 | one contract transaction | FY2007-FY2026 | `AWARDING_AGENCY_CODE` |
| LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_TOPTIER_AGENCIES | 111 | one top-tier agency | `ACTIVE_FY` 2026 only | `TOPTIER_CODE` |

**Columns that carry it.**
- Contract year tables: `RECIPIENT_UEI`, `RECIPIENT_NAME`, `RECIPIENT_PARENT_NAME`, `RECIPIENT_COUNTRY_NAME`, `FOREIGN_OWNED`, `DOMESTIC_OR_FOREIGN_ENTITY`, `DOMESTIC_OR_FOREIGN_ENTITY_CODE`, `AWARDING_AGENCY_CODE`, `AWARDING_AGENCY_NAME`, `NUMBER_OF_OFFERS_RECEIVED`, `FEDERAL_ACTION_OBLIGATION`, `ACTION_DATE`. Columns confirmed present on FY2008 and FY2024; fill rate not yet measured on any.
- TOPTIER_AGENCIES: `TOPTIER_CODE`, `AGENCY_NAME`, `OBLIGATED_AMOUNT`.

**The join, hop by hop.**
```
one table family, union the 20 year tables; group by AWARDING_AGENCY_CODE and DOMESTIC_OR_FOREIGN_ENTITY
contracts.AWARDING_AGENCY_CODE ➔ TOPTIER_AGENCIES.TOPTIER_CODE   (label only; overlap not yet measured)
```

**A hit means.** A few agencies where foreign-owned firms take a share of positive obligations several times the government-wide share, steady across years.

**A miss means.** The foreign-owned share is about the same everywhere, or the differences are one or two giant awards. Then agency is not the story.

**Limits, said out loud.**
- A column that exists by name is not proof it is filled. Count the distinct values of `DOMESTIC_OR_FOREIGN_ENTITY` and `FOREIGN_OWNED` per year before anything else; two flags in this warehouse exist and are empty.
- "Win more" needs bids lost. The data has `NUMBER_OF_OFFERS_RECEIVED` per award and no losing bidders, so this shows share of dollars, not win rate.
- Money is `FEDERAL_ACTION_OBLIGATION`, which is signed. `CURRENT_TOTAL_VALUE_OF_AWARD` changes per transaction and must not be summed.
- Column names in these landing tables can be case-sensitive; an unquoted name may miss.
- The agency lookup table is fiscal 2026 only. Agency codes from 2007 may not all be in it.

**The picture.** Ranked bar chart, one bar per agency, length = foreign-owned share of positive contract dollars, with defense and health highlighted.

**First cheap check.** On FY2024, count rows by `DOMESTIC_OR_FOREIGN_ENTITY` value, blanks included.

---

### W95 · Political nonprofits share addresses with PACs

**The physical thing.** One street address and suite that is the mailing address of a 527 political organization and also the address of a registered federal PAC.

**Status.** Never run.

**Data grade.** B, both sides carry a full street address and ZIP with measured fill on the ZIP, but the PAC table repeats ids across election cycles and the 527 table leaves out 501(c)(4) groups.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.POLITICS.POLITICS__IRS527_8871_ORGS | 77,591 | one 527 registration notice | `ESTABLISHED_DATE` 1808-01-01 to 2026-07-24, 91.21% filled, contains typo dates | `MAILING_ADDR1` + `MAILING_ZIP` |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES | 60,031 | one committee in one cycle file | no year column | `CMTE_ST1` + `CMTE_ZIP` |

**Columns that carry it.**
- IRS527_8871_ORGS: `FORM_ID_NUMBER`, `EIN` (100%, 58,251 distinct), `ORGANIZATION_NAME`, `MAILING_ADDR1`, `MAILING_CITY`, `MAILING_STATE`, `MAILING_ZIP` (100%, 15,155 distinct), `ESTABLISHED_DATE` (91.21%), `CUSTODIAN_NAME`.
- FED_FEC_COMMITTEES: `CMTE_ID` (100%, 37,886 distinct), `CMTE_NM`, `CMTE_ST1`, `CMTE_CITY`, `CMTE_ST`, `CMTE_ZIP` (100%, 50 blank strings), `CMTE_TP`, `TRES_NM`.

**The join, hop by hop.**
```
normalize(IRS527_8871_ORGS.MAILING_ADDR1) + left(MAILING_ZIP,5) = normalize(FED_FEC_COMMITTEES.CMTE_ST1) + left(CMTE_ZIP,5)   (overlap not yet measured)
dedupe FED_FEC_COMMITTEES on CMTE_ID first
```

**A hit means.** Addresses that host one 527 and one PAC with different names and the same treasurer or custodian, outside the known compliance-firm buildings.

**A miss means.** Every shared address is a law firm, a compliance vendor or a mail drop serving dozens of clients. Then the address says who does the paperwork, not who controls the groups.

**Limits, said out loud.**
- The PAC table repeats 16,943 ids across cycles with no cycle column; 60,031 rows hold 37,886 distinct ids. Count organizations, never pairs. The deduped view, LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES_DIM, has no street or ZIP column, so the address has to come from this table.
- The 527 table holds 527 groups only. 501(c)(4) nonprofits, the larger "political nonprofit" world, are not in it.
- A bare building address clusters unrelated tenants. Keep the suite number in the match and treat any address with many tenants as a vendor.
- The 527 table is one row per notice, so amended notices repeat an organization; dedupe on `EIN`.
- `ESTABLISHED_DATE` starts at 1808. Bound it before charting.

**The picture.** Network, one node per address, edges to the 527s and PACs registered there, node size = count of groups.

**First cheap check.** Count distinct normalized street plus ZIP5 values that appear in both tables.

---

### W96 · Years from redline map to shortage-area designation

**The physical thing.** A neighborhood graded "hazardous" on a 1930s federal lending map, and the year the federal government first declared the same place short of primary-care doctors.

**Status.** Never run.

**Data grade.** C, the full map is landed with a place code and a shape on every row by name, but the table is unprofiled, so whether that code is filled, and whether it is a county code, is not yet measured.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_RAW.LANDING.FED_MAPPING_INEQUALITY | 10,154 | one graded polygon on one city's map; the full map | `YEAR_MAPPED` not profiled; not yet measured | `FIPS` if filled, else `GEOMETRY` |
| LIBRARY_MARTS.HOUSING.HOUSING__FED_MAPPING_INEQUALITY | 1,155 | one merged polygon per city and grade; not used for counts | `YEAR_MAPPED` not profiled; not yet measured | none usable: `FIPS` is blank on all 1,155 rows |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_HPSA_PRIMARY_CARE | 79,158 | one component of one shortage-area designation | `DESIGNATION_DATE` 1970-01-01 to 2026-08-05, 100% filled | `STATE_COUNTY_FIPS_CODE` |

**Columns that carry it.**
- LANDING.FED_MAPPING_INEQUALITY: `CITY`, `STATE`, `FIPS`, `HOLC_GRADE`, `YEAR_MAPPED`, `GEOMETRY`, `LAT`, `LON`. Table not profiled; fill rate not yet measured on any of them.
- HOUSING__FED_MAPPING_INEQUALITY (mart): `FIPS` is filled with a blank string on all 1,155 rows. Named here only so the limit is visible.
- HPSA_PRIMARY_CARE: `HPSA_ID`, `HPSA_NAME`, `DESIGNATION_TYPE`, `DESIGNATION_DATE` (100%), `WITHDRAWN_DATE` (61.28%), `STATE_COUNTY_FIPS_CODE` (100%, 3,269 distinct), `HPSA_CITY`, `STATE_ABBREVIATION`, `LATITUDE`, `LONGITUDE`, `COMPONENT_TYPE_DESCRIPTION`. Fill of the coordinates not yet measured.

**The join, hop by hop.**
```
if filled and county-level: LANDING.FED_MAPPING_INEQUALITY.FIPS ➔ HPSA_PRIMARY_CARE.STATE_COUNTY_FIPS_CODE   (overlap not yet measured)
finer option: HPSA_PRIMARY_CARE.LATITUDE, LONGITUDE point inside LANDING.FED_MAPPING_INEQUALITY.GEOMETRY   (the GeoJSON parsed on 10,153 of 10,154 rows)
fallback: LANDING.FED_MAPPING_INEQUALITY.CITY + STATE ~ HPSA_PRIMARY_CARE.HPSA_CITY + STATE_ABBREVIATION   (name match, overlap not yet measured)
years = year of min(DESIGNATION_DATE) minus YEAR_MAPPED
```

**A hit means.** Places whose maps carried D-grade areas were designated as shortage areas earlier, or more often, than mapped places graded A or B, and at the polygon level the designated points fall inside the D-grade shapes.

**A miss means.** Designation timing is the same regardless of grade. If only the county or city join could be run, that is a weak no, because the question is about neighborhoods.

**Limits, said out loud.**
- `FIPS` on the landing table has no measured fill. On the mart the same column is a blank string on every row. Do not assume the landing copy is better or worse; count it first. What level the code is (county or place) is also unstated in the source notes.
- The mart holds one polygon per city and grade, 1,155 rows against 10,154 in the landing table. Any spatial count off the mart covers 11% of the map. Use the landing table for counts.
- `HOLC_ID` is one distinct value, not an id. 814 grades are blank and there are 3 trailing-space spellings of the grade.
- `DESIGNATION_DATE` minimum is 1970-01-01, which may be a default. Count how many rows sit on that exact day before computing any span of years.
- Shortage areas are designated by tract, place or facility. A county or city match cannot say the designated area is the redlined area; only the point-in-polygon hop can, and it depends on coordinates whose fill is not yet measured.

**The picture.** Scatter, x = year mapped, y = years from map to first designation, one mark per graded polygon (or per city if only the fallback join runs), colored by grade.

**First cheap check.** On LIBRARY_RAW.LANDING.FED_MAPPING_INEQUALITY, count rows where `FIPS` is non-blank after trimming, with its distinct count and value lengths, out of 10,154.

---

### W97 · Doctors also donors, contractors, nursing owners

**The physical thing.** One person's name and ZIP that shows up as a licensed doctor, as a political donor, as an owner on a nursing home's Medicare enrollment, and as a federal contractor.

**Status.** Never run. The gap named on 2026-09-09 (no table naming nursing-home owners) closed on 2026-09-10.

**Data grade.** C, no id crosses any of these worlds, so every hop is a name plus ZIP match.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES | 9,606,683 | one provider id | `PROVIDER_ENUMERATION_DATE` 2005-05-23 to 2026-06-06, 96.4% filled | name + ZIP |
| LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP | 295,083 | one owner in one role on one nursing-home enrollment | one vintage, current owners only | name + `ZIP_CODE_OWNER` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS | 14,425 | one nursing-home Medicare enrollment | one snapshot | `ENROLLMENT_ID`, `CCN` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_OWNERS | 101,188 | one owner in one role on one home health enrollment | one vintage | name + `ZIP_CODE_OWNER` |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS | 283,771,819 | one contribution by one person | window on the current table not yet re-measured | `DONOR_NAME` + `ZIP_CODE` |
| LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 through FED_USASPENDING_CONTRACTS_FY2026 (20 tables) | 96,976,021 | one contract transaction | FY2007-FY2026 | `RECIPIENT_NAME` + `RECIPIENT_ZIP_4_CODE` |

**Columns that carry it.**
- NPPES: `NPI` (100%), `PROVIDER_LAST_NAME_LEGAL_NAME`, `PROVIDER_FIRST_NAME`, `PROVIDER_CREDENTIAL_TEXT`, `PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_POSTAL_CODE`, `ENTITY_TYPE_CODE`.
- FED_CMS_SNF_OWNERSHIP: `ENROLLMENT_ID`, `FIRST_NAME_OWNER`, `LAST_NAME_OWNER`, `ROLE_TEXT_OWNER`, `ZIP_CODE_OWNER`, `PERCENTAGE_OWNERSHIP`, `TYPE_OWNER`. Not profiled; fill rate not yet measured.
- SNF_ENROLLMENTS: `ENROLLMENT_ID` (100%), `CCN` (100%, 14,026 distinct).
- HOME_HEALTH_OWNERS: `FIRST_NAME_OWNER`, `LAST_NAME_OWNER`, `ZIP_CODE_OWNER` (20.93%), `ROLE_TEXT_OWNER`.
- FEC_INDIV_CONTRIBUTIONS: `DONOR_NAME`, `OCCUPATION`, `ZIP_CODE` (100%, 321,021 blank strings), `TRANSACTION_AMT`.
- Contract year tables: `RECIPIENT_NAME`, `RECIPIENT_ZIP_4_CODE`. Fill not yet measured.

**The join, hop by hop.**
```
NPPES last + first name + ZIP5 ~ SNF_OWNERSHIP.LAST_NAME_OWNER + FIRST_NAME_OWNER + ZIP_CODE_OWNER   (overlap not yet measured)
SNF_OWNERSHIP.ENROLLMENT_ID ➔ SNF_ENROLLMENTS.ENROLLMENT_ID ➔ CCN   (288,550 of 295,083 owner rows join)
NPPES name + ZIP5 ~ FEC_INDIV_CONTRIBUTIONS.DONOR_NAME + ZIP_CODE   (overlap not yet measured)
NPPES name + ZIP5 ~ contracts.RECIPIENT_NAME + RECIPIENT_ZIP_4_CODE   (overlap not yet measured)
```

**A hit means.** A list of people with a distinctive multi-word name who appear in three or four of the worlds at the same ZIP, such as a physician who owns a share of four nursing homes and gives to the state's delegation.

**A miss means.** Matches are all common names in dense ZIPs. Then name plus ZIP is too weak and the question needs a real person id that public data does not carry.

**Limits, said out loud.**
- The provider file's EIN column is '<UNAVAIL>' on every populated row. No id links a doctor to a company, a donor record or a contractor.
- Single-word name matches were 8% real in a checked sample. A common surname in one ZIP is many people. Use first plus last plus ZIP, and hand-check.
- A doctor's practice ZIP, a donor's home ZIP and an owner's business ZIP are often three different ZIPs for one person. Real matches will be missed.
- Home health owner ZIP is filled on 20.93% of rows. The nursing-home owner file is one vintage, cp1252 text, and 6,533 of its rows name enrollments the snapshot does not carry.
- Contract recipients are almost all companies. The contractor leg will mostly find sole proprietors and named practices.

**The picture.** Network, one node per person, edges to each world they appear in, one mark per person with three or more worlds.

**First cheap check.** Count `TYPE_OWNER` values in the nursing-home owner file to see how many owner rows are individuals, then count those whose last name, first name and ZIP5 find one NPPES row.

---

### W98 · Offshore-leak names in US federal contracts

**The physical thing.** A company or officer named in the ICIJ offshore leaks, and the same name as the recipient of a US federal contract.

**Status.** Never run. Absorbs wonder 116.

**Data grade.** C, the two sides share a name and nothing else: no id, no US address on the leak side, no year on the officers.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_ENTITIES | 814,344 | one offshore entity | `INCORPORATION_DATE` 0199-04-25 to 2812-12-18, 96.82% filled, contains typo dates | `NAME` |
| LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_OFFICERS | 771,315 | one officer or shareholder | no date column | `NAME` |
| LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 through FED_USASPENDING_CONTRACTS_FY2026 (20 tables) | 96,976,021 | one contract transaction | FY2007-FY2026 | `RECIPIENT_NAME` |

**Columns that carry it.**
- ICIJ ENTITIES: `NODE_ID`, `NAME`, `FORMER_NAME`, `JURISDICTION`, `INCORPORATION_DATE` (96.82%), `COUNTRY_CODES`, `SOURCE_LEAK`. Fill of `NAME` not yet measured.
- ICIJ OFFICERS: `NODE_ID`, `NAME`, `COUNTRY_CODES`, `SOURCE_LEAK`. Table has no profiled key or date columns.
- Contract year tables: `RECIPIENT_NAME`, `RECIPIENT_PARENT_NAME`, `RECIPIENT_UEI`, `RECIPIENT_COUNTRY_NAME`, `HIGHLY_COMPENSATED_OFFICER_1_NAME`, `ACTION_DATE`, `FEDERAL_ACTION_OBLIGATION`. Fill not yet measured.

**The join, hop by hop.**
```
ICIJ ENTITIES.NAME ~ contracts.RECIPIENT_NAME / RECIPIENT_PARENT_NAME               (exact match after folding, multi-word names only, overlap not yet measured)
ICIJ OFFICERS.NAME ~ contracts.HIGHLY_COMPENSATED_OFFICER_1_NAME                    (person name match, overlap not yet measured)
filter ICIJ rows to COUNTRY_CODES containing USA to cut coincidences
```

**A hit means.** A distinctive multi-word company name that is both an offshore entity tied to a US address and a federal contract recipient, confirmed by country and by date order.

**A miss means.** Every match is a generic name such as "GLOBAL SERVICES LTD". That says name matching cannot carry this and the question waits for a shared company id.

**Limits, said out loud.**
- Being in the leaks is not wrongdoing. A match is a lead to check, not a finding.
- Single-word name matches were 8% real in a checked sample; multi-word names cleared 92%. Common officer names are many people.
- Officers have no year and no US place. The leak address table exists but links only through a relationships table not used here.
- Incorporation dates run from year 0199 to 2812. Bound them before any before-and-after test.
- The eight ICIJ copies in the warehouse were one snapshot with different blank spellings. Use this one mart and do not count the others as extra vintages.

**The picture.** Network, offshore entity to contract recipient, edge labeled with contract dollars, one mark per matched name.

**First cheap check.** Count distinct multi-word entity names with a US country code that equal a distinct `RECIPIENT_NAME` in FY2024.

---

### W99 · Hospital execs who are also insiders at public companies

**The physical thing.** A person listed as an officer or trustee on a nonprofit hospital's tax return who also files insider stock reports as a director or officer of a listed company.

**Status.** Never run. Reworded on 2026-09-18: private suppliers cannot be seen; insider filings can.

**Data grade.** C, the person is matched by name alone, with state as the only tiebreak.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.HEALTH.HEALTH__HOSPITAL_OFFICER_PAY | 526,374 | one person on one hospital tax return | `TAX_YEAR` 2016 to 2025, 100% filled | `PERSON_NAME` |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_REPORTINGOWNER | 1,934,673 | one reporting owner on one insider filing | no date column; date comes from the submission | `OWNER_NAME`, `ACCESSION_NUMBER` |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION | 1,772,088 | one insider filing | `FILING_DATE` 2016-07-01 to 2025-03-31, 100% filled | `ACCESSION_NUMBER` |

**Columns that carry it.**
- HOSPITAL_OFFICER_PAY: `EIN` (100%, 3,962 distinct), `HOSPITAL_NAME`, `HOSPITAL_STATE`, `PERSON_NAME`, `TITLE`, `IS_OFFICER`, `IS_TRUSTEE_OR_DIRECTOR`, `IS_SCHEDULE_J_POINTER`, `IS_GROUP_RETURN`, `TAX_YEAR` (100%), `TOTAL_COMPENSATION`.
- INSIDER_REPORTINGOWNER: `ACCESSION_NUMBER`, `OWNER_CIK` (100%, 139,905 distinct), `OWNER_NAME`, `RELATIONSHIP`, `TITLE`, `STATE`.
- INSIDER_SUBMISSION: `ACCESSION_NUMBER`, `FILING_DATE` (100%), `ISSUER_CIK` (100%, 10,676 distinct), `ISSUER_NAME`, `ISSUER_TICKER`.

**The join, hop by hop.**
```
HOSPITAL_OFFICER_PAY.PERSON_NAME ~ INSIDER_REPORTINGOWNER.OWNER_NAME, with HOSPITAL_STATE = STATE   (name match, overlap not yet measured)
INSIDER_REPORTINGOWNER.ACCESSION_NUMBER ➔ INSIDER_SUBMISSION.ACCESSION_NUMBER ➔ ISSUER_CIK, ISSUER_NAME   (overlap not yet measured)
```

**A hit means.** A list of hospital officers and trustees who are also insiders at named public companies in the same years, with the companies that sell to hospitals, such as device, drug and staffing firms, flagged by hand.

**A miss means.** The matched people are trustees who are local business leaders with no tie to health suppliers. That says board overlap exists and the supplier angle does not.

**Limits, said out loud.**
- No table of what a hospital buys is landed. The data can show a person sits in both seats; it cannot show the hospital bought from that company.
- Private companies file no insider reports. Only listed issuers can appear.
- The tax return repeats an executive on every affiliate's return and adds pointer lines that restate pay. Filter `IS_SCHEDULE_J_POINTER` false and `IS_GROUP_RETURN` false, and count each person once per `TAX_YEAR`.
- Name formats on the two sides have not been compared. Single-word or very common names are noise; require first name, last name and state to agree.
- Overlap window is 2016-07-01 to 2025-03-31. Tax years before 2017 are absent from the officer source.

**The picture.** Network, hospital on one side, listed company on the other, one edge per person who holds both seats.

**First cheap check.** Look at 20 sample values of `PERSON_NAME` and `OWNER_NAME` to learn the two formats, then count folded names that agree within the same state.

---

### M-056 · Money arrives right before the vote

**The physical thing.** A cheque to a sitting member's campaign committee dated in the seven days before that member casts a roll-call vote.

**Status.** Partially measured. The chain was verified end to end: 54.2M contributions ($6.86B) reach 695 sitting members, 1.07M votes reach 635 members, windows overlap exactly. The timing test itself has never been run; its SQL was mapped on 2026-09-13. Absorbs W81 and WN-155.

**Data grade.** B, real ids carry every hop and every table is profiled, but the window is two Congresses, and the date range of the current contribution table has not been re-measured.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS | 283,771,819 | one contribution by one person | window on the current table not yet re-measured | `CMTE_ID` |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_CAND_CMTE_LINKAGE | 30,536 | one candidate-committee link | not yet measured | `CMTE_ID`, `CAND_ID` |
| LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_CROSSWALK | 12,794 | one member of Congress, all id systems | no date axis used | `FEC_IDS`, `ICPSR` |
| LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_VOTES | 945,523 | one member's vote on one roll call | congresses 118 and 119 per the mapped query | `ICPSR`, `CONGRESS`, `CHAMBER`, `ROLLNUMBER` |
| LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_ROLLCALLS | 3,364 | one roll-call vote | `VOTE_DATE` 2023-01-03 to 2026-06-25, 100% filled | `CONGRESS`, `CHAMBER`, `ROLLNUMBER` |

**Columns that carry it.**
- FEC_INDIV_CONTRIBUTIONS: `CMTE_ID` (100%, 40,294 distinct), `TRANSACTION_DATE` (99.98%), `TRANSACTION_AMT`, `TRANSACTION_TYPE`, `EMPLOYER`.
- CAND_CMTE_LINKAGE: `CMTE_ID` (100%), `CAND_ID` (100%), `CMTE_TP`, `CMTE_DSGN`.
- MEMBER_CROSSWALK: `FEC_IDS` (an array; must be flattened; fill not yet measured), `ICPSR` (96.12%, 12,182 distinct), `BIOGUIDE` (99.9%).
- VOTEVIEW_VOTES: `ICPSR` (100%, 639 distinct), `CONGRESS`, `CHAMBER`, `ROLLNUMBER`, `CAST_CODE`.
- VOTEVIEW_ROLLCALLS: `VOTE_DATE` (100%), `BILL_NUMBER`, `VOTE_DESC`.

**The join, hop by hop.**
```
FEC_INDIV_CONTRIBUTIONS.CMTE_ID ➔ CAND_CMTE_LINKAGE.CMTE_ID                     (measured 9,217 shared values)
CAND_CMTE_LINKAGE.CAND_ID ➔ MEMBER_CROSSWALK.FEC_IDS (flattened) ➔ ICPSR        (54.2M contributions reach 695 sitting members)
MEMBER_CROSSWALK.ICPSR ➔ VOTEVIEW_VOTES.ICPSR                                   (votes reach 635 members)
VOTEVIEW_VOTES.CONGRESS + CHAMBER + ROLLNUMBER ➔ VOTEVIEW_ROLLCALLS ➔ VOTE_DATE
```

**A hit means.** For the typical member, dollars per day in the seven days before a vote-day run well above that member's own daily average, after the last days of each quarter are dropped. The mapped readout treats a median lift above about 1.15 as the story.

**A miss means.** The week before a vote looks like any other week. Money follows the fundraising calendar, not the floor schedule.

**Limits, said out loud.**
- Two Congresses only, 118 and 119. Roll calls run 2023-01-03 to 2026-06-25.
- `TRANSACTION_DATE` on the contribution table reads 0031-04-10 to 9206-07-02, which are typo dates; 51,555 rows do not parse. The mapped query bounds dates to 2023-01-03 through 2026-06-30. An older 84.2M-row copy was 99.99% 2023-2026; the window on the current table is not yet re-measured.
- Congress votes most weeks it sits, so many days are "pre-vote" days. The test has power only if enough ordinary days are left; the mapped query requires 60.
- Filing-deadline eves are a known spike (M-007) and are subtracted first. Earmark rows, `TRANSACTION_TYPE` 15E, are excluded. Several roll calls on one day collapse to one vote-day.
- Individual contributions only; PAC money is a separate table. The test says nothing about what the vote was on. Tying money to a bill's subject needs a donor-industry code and a bill-subject code, and neither is landed.
- Source note: the book counts 1.07M votes reaching 635 members; the votes table today holds 945,523 rows and 639 distinct `ICPSR`. Recount before quoting either.

**The picture.** Two overlaid area charts per chamber, x = days from the nearest vote (minus 30 to plus 30), y = dollars per day, one line before votes and one after.

**First cheap check.** Re-run the first hop only: count contribution rows dated 2023-01-03 to 2026-06-30 whose `CMTE_ID` reaches an `ICPSR`, and compare with 54.2M.

---

### M-015 · Out-of-state money flooding small races

**The physical thing.** A cheque from a donor whose address is in one state to a House or Senate candidate running in another, counted race by race.

**Status.** Never run. The book records "chain works; 2023-2026 window", measured on an older 84.2M-row copy of the contribution table.

**Data grade.** B, real committee and candidate ids join the tables and the keys are profiled, but the date window on the current contribution table has not been re-measured.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS | 283,771,819 | one contribution by one person | window on the current table not yet re-measured | `CMTE_ID` |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_CAND_CMTE_LINKAGE | 30,536 | one candidate-committee link | not yet measured | `CMTE_ID`, `CAND_ID` |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_CANDIDATES | 27,095 | one candidate in one cycle | `CAND_ELECTION_YR` not profiled; not yet measured | `CAND_ID` |

**Columns that carry it.**
- FEC_INDIV_CONTRIBUTIONS: `CMTE_ID` (100%), `STATE` (fill not yet measured), `ZIP_CODE` (100%, 321,021 blank strings), `TRANSACTION_DATE` (99.98%), `TRANSACTION_AMT`, `TRANSACTION_TYPE`, `CYCLE_FILE`.
- CAND_CMTE_LINKAGE: `CMTE_ID` (100%, 15,853 distinct), `CAND_ID` (100%, 15,092 distinct), `CMTE_TP`, `CMTE_DSGN`, `CAND_ELECTION_YR`.
- FEC_CANDIDATES: `CAND_ID` (100%, 19,063 distinct), `CAND_NAME`, `CAND_OFFICE`, `CAND_OFFICE_ST`, `CAND_OFFICE_DISTRICT`, `CAND_ELECTION_YR`.

**The join, hop by hop.**
```
FEC_INDIV_CONTRIBUTIONS.CMTE_ID ➔ CAND_CMTE_LINKAGE.CMTE_ID   (measured 9,217 shared values)
CAND_CMTE_LINKAGE.CAND_ID ➔ FEC_CANDIDATES.CAND_ID            (measured 14,768 shared values)
compare FEC_INDIV_CONTRIBUTIONS.STATE with FEC_CANDIDATES.CAND_OFFICE_ST, per CAND_OFFICE_ST + CAND_OFFICE_DISTRICT
```

**A hit means.** A list of House districts and small-state Senate races where most itemized individual dollars came from other states, far above the typical race.

**A miss means.** The out-of-state share is about the same everywhere, or it is high only for party leaders and national names. Then it tracks fame, not the size of the race.

**Limits, said out loud.**
- The candidate table has 27,095 rows for 19,063 distinct ids, one row per cycle. Join on `CAND_ID` plus election year or every dollar repeats.
- This is the itemized individual contributions file. Money a committee did not itemize is not in it, so every share is a share of itemized dollars only.
- Earmark rows are `TRANSACTION_TYPE` 15E. Exclude them or the same dollar can count twice.
- The date column holds typo years from 0031 to 9206 and 51,555 rows that do not parse. Bound dates. The window on the current 283,771,819-row table is not yet re-measured.
- No district geometry is landed. "Small race" has to be defined from total dollars raised or from the office and state, not from voters in the district.

**The picture.** Flow map, donor state to candidate state, with a ranked side list of races by out-of-state share, one mark per race.

**First cheap check.** For one known 2024 Senate race, sum dollars by donor `STATE` and compare the in-state share with a published figure.

---

### M-007 · Donations spike on filing-deadline eves

**The physical thing.** The count and dollar total of individual campaign contributions dated on the last days of a reporting quarter, against an ordinary day.

**Status.** Never run. Listed in the book as a known artefact to be measured so that M-056 can subtract it.

**Data grade.** B, one profiled table with a real date column, but the usable date window on the current table has not been re-measured.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS | 283,771,819 | one contribution by one person | window on the current table not yet re-measured | `TRANSACTION_DATE` |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_CAND_CMTE_LINKAGE | 30,536 | one candidate-committee link | not yet measured | `CMTE_ID` |

**Columns that carry it.**
- FEC_INDIV_CONTRIBUTIONS: `TRANSACTION_DATE` (99.98%), `TRANSACTION_AMT`, `TRANSACTION_TYPE`, `CMTE_ID` (100%), `CYCLE_FILE`.
- CAND_CMTE_LINKAGE: `CMTE_ID` (100%), `CMTE_TP`, `CMTE_DSGN`. Used only to split candidate committees from the rest.

**The join, hop by hop.**
```
one table, no join for the core count: group by TRANSACTION_DATE; flag day-of-month 29 or later in months 3, 6, 9, 12
optional split: FEC_INDIV_CONTRIBUTIONS.CMTE_ID ➔ CAND_CMTE_LINKAGE.CMTE_ID   (measured 9,217 shared values)
```

**A hit means.** Dollars per day on the last three days of March, June, September and December run at a clear multiple of the daily average, in every year. That multiple becomes the correction M-056 subtracts.

**A miss means.** Quarter-end days look like any other day. Then M-056 needs no deadline correction, and the fundraising-email folklore does not show in itemized money.

**Limits, said out loud.**
- `TRANSACTION_DATE` reads 0031-04-10 to 9206-07-02. Those are typo years. 51,555 rows do not parse at all and at least one parses to 2106-08-27. Bound the dates before any daily series.
- An older 84.2M-row copy had 583 null dates and was 99.99% 2023-2026. The current table is 283,771,819 rows and its window is not yet re-measured; run the year count first.
- The date is the day the committee says it received the money. Committees batch their data entry, so part of any quarter-end spike is bookkeeping, not donor behavior. The data cannot separate the two.
- Monthly filers and pre-election reports have other deadlines. The quarter-end flag catches the main one only.
- Earmark memo rows, `TRANSACTION_TYPE` 15E, repeat dollars already counted and must be excluded.

**The picture.** Calendar heat strip, x = day of year, one row per year, shade = dollars received that day.

**First cheap check.** Count rows by year of `TRANSACTION_DATE` between 1990 and 2030, and count what falls outside.

---

### N2 · Removal orders given with nobody in the room, by court and year

**The physical thing.** An immigration judge orders a person removed at a hearing the person did not attend, counted by court city and by the year the case was completed.

**Status.** Never run. New on 2026-09-18. The fill of `ABSENTIA`, `BASE_CITY_CODE` and `COMP_DATE` is not yet measured.

**Measured 2026-09-18.** `ABSENTIA` on 16,817,265 rows: N on 10.76M, Y on 2.46M, NULL on 3.58M, a null byte on 7,834, a single space on 6,126, and the digit 5 on one row. Non-null on 13,234,928.

**Data grade.** B, one table carries all three columns, but the table is unprofiled and the answer depends on a flag whose fill and values nobody has counted.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_RAW.LANDING.FED_EOIR_PROCEEDING | 16,817,265 | one proceeding in one immigration case | not yet measured | `BASE_CITY_CODE` |

**Columns that carry it.**
- FED_EOIR_PROCEEDING: `ABSENTIA`, `BASE_CITY_CODE`, `COMP_DATE`, `DEC_CODE`, `DEC_TYPE`, `CUSTODY`, `CASE_TYPE`, `NAT`, `HEARING_LOC_CODE`. Fill rate not yet measured on any of them, except the `DEC_CODE` blanks counted below.

**The join, hop by hop.**
```
one table, no join
group by BASE_CITY_CODE, year of COMP_DATE; count rows where ABSENTIA marks an in-absentia order, over rows with a real DEC_CODE
```

**A hit means.** Some courts order removal in absentia at several times the rate of others in the same year, and the rate moves in steps that line up with docket or policy changes.

**A miss means.** The in-absentia share is about level across courts and years, or `ABSENTIA` turns out to be blank or a constant. The second outcome ends the question on this table.

**Limits, said out loud.**
- A column found by name is not proof it is filled. Two flags in this warehouse exist and select nothing. Count the distinct values of `ABSENTIA` before any chart.
- Blanks in this table come three ways: NULL, a NUL byte, and a single space. They were counted on `DEC_CODE` at 5.32M, 1.45M and 729K rows. Expect the same in `ABSENTIA` and clean it the same way.
- No lookup table names the court behind each `BASE_CITY_CODE`, and no lookup gives the meaning of `DEC_CODE` values. Both must be read from EOIR's own code lists.
- A person can have several proceedings. Counting rows counts proceedings, not people; `IDNCASE` is the case id for counting cases.
- The table cannot show why a person was absent, whether a hearing notice reached them, or whether the order was later reopened.

**The picture.** Animated bar chart, one bar per court city, length = in-absentia share of completed proceedings, one frame per year of `COMP_DATE`.

**First cheap check.** Count rows by distinct `ABSENTIA` value, blanks split three ways, and the min and max of `COMP_DATE`.

---


# Work and things: the machine running

### W102 · Visa sponsors carry unpaid wage judgments

**The physical thing.** One employer name on two federal papers: a Labor Department application to bring in foreign workers, and a Wage and Hour Division case that found the same employer owed back wages. This entry absorbs the old row 105 (visa sponsors in wage-violation ZIPs), which was the same join drawn as a map.

**Status.** never run. The wage-case table landed 2026-09-10; before that the question had no second table.

**Data grade.** C, because the two tables share no id and join on employer name plus ZIP, the wage-case table is unprofiled, the visa table covers one fiscal year, and neither table says whether the back wages were ever paid.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_RAW.LANDING.FED_DOL_WHD_ENFORCEMENT | 367,890 | one closed wage-and-hour case against one employer | not yet measured (date columns carry typo years 0200 and 3021) | `LEGAL_NAME` + `ZIP_CD` |
| LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_DOL_OFLC | 664,616 | one labor-condition application by one employer | `DECISION_DATE` 2018-10-01 to 2019-09-30 | `EMPLOYER_NAME` + `EMPLOYER_POSTAL_CODE` |

**Columns that carry it.**
- LIBRARY_RAW.LANDING.FED_DOL_WHD_ENFORCEMENT: `LEGAL_NAME`, `TRADE_NM`, `ZIP_CD`, `ST_CD`, `H1B_VIOLTN_CNT`, `H1B_BW_ATP_AMT`, `H1B_EE_ATP_CNT`, `H1B_CMP_ASSD_AMT`, `H2A_VIOLTN_CNT`, `H2A_BW_ATP_AMT`, `H2B_VIOLTN_CNT`, `BW_ATP_AMT`, `CASE_VIOLTN_CNT`, `FINDINGS_START_DATE`, `FINDINGS_END_DATE`. Fill rate not yet measured on any of them; the table has not been profiled.
- LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_DOL_OFLC: `EMPLOYER_NAME`, `EMPLOYER_POSTAL_CODE`, `EMPLOYER_STATE`, `VISA_CLASS`, `TOTAL_WORKER_POSITIONS`, `WILLFUL_VIOLATOR`, `DECISION_DATE` (100.0% filled). Fill of the name, ZIP and `WILLFUL_VIOLATOR` columns not yet measured.

**The join, hop by hop.**
```
Step 0, one table, no join:
FED_DOL_WHD_ENFORCEMENT where H1B_VIOLTN_CNT > 0 or H2A_VIOLTN_CNT > 0   (the wage table counts visa-program violations itself)
Step 1, name join:
IMMIGRATION__FED_DOL_OFLC.EMPLOYER_NAME + left(EMPLOYER_POSTAL_CODE,5)
  ➔ FED_DOL_WHD_ENFORCEMENT.LEGAL_NAME + left(ZIP_CD,5)      overlap not yet measured
```

**A hit means.** Employers that filed visa applications in fiscal 2019 also appear, under the same multi-word legal name at the same ZIP, in wage cases with back wages owed. The strongest rows are the ones where the wage case itself counts H-1B or H-2A violations.

**A miss means.** Few or no visa sponsors match a wage case. That would say either sponsors are rarely cited, or the name-plus-ZIP join is too strict for employers that file from a head office and get cited at a worksite.

**Limits, said out loud.**
- "Unpaid" cannot be seen. The wage table holds back wages the employer agreed to pay (`BW_ATP_AMT`). It has no payment or collection column.
- The visa table is one fiscal year, 2018-10-01 to 2019-09-30. A sponsor from any other year is invisible.
- Name joins: multi-word names cleared 92% real in the 2026-09-03 test, single words 8%. Use multi-word names only.
- 3,612 wage rows have a blank `LEGAL_NAME` and 19 a blank `ZIP_CD`, so the join misses about 1% before it starts (trap 2026-09-10).
- `H1B_VIOLTN_CNT` and `H2A_VIOLTN_CNT` were confirmed by name only. Two flags found the same way in this warehouse turned out empty (traps 2026-09-18). Count non-zero rows first.

**The picture.** Ranked bar: employers on the vertical axis, back wages agreed in dollars on the horizontal, one bar per matched employer, labelled with visa positions requested.

**First cheap check.** Count rows in FED_DOL_WHD_ENFORCEMENT where `H1B_VIOLTN_CNT` > 0, and where `H2A_VIOLTN_CNT` > 0. If both are zero the columns are empty shells.

---

### W103 · Union locals shrink where county contracts grow

**The physical thing.** A union local's membership number on its yearly Labor Department report, set beside the federal contract dollars performed in the county where that local keeps its office.

**Status.** never run. The 2026-09-09 gap (no county on contracts) closed on 2026-09-10 when the contract year tables landed with county FIPS.

**Data grade.** B, because the union table has a ZIP and no county, so every local reaches a county through a ZIP-to-county bridge that picks the right county 86.2% of the time, and the contract tables are unprofiled.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.LABOR.LABOR__FED_DOL_OLMS | 617,710 | one annual financial report by one union body | `YEAR_COVERED` 2000-2026 | `ZIP` |
| LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY | 46,960 | one ZIP-area and county pair | 2020 geography | `ZCTA5` ➔ `COUNTY_FIPS` |
| LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 through LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2026 (20 tables) | 96,976,021 | one contract transaction | FY2007-FY2026 | `PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE` |

**Columns that carry it.**
- LABOR__FED_DOL_OLMS: `FILE_NUMBER`, `UNION_NAME`, `DESIGNATION_NUMBER`, `MEMBERS`, `YEAR_COVERED` (99.97% filled), `ZIP` (99.97% filled, 56,870 distinct), `STATE`. Fill of `MEMBERS` not yet measured.
- XWALK_ZCTA_COUNTY: `ZCTA5`, `COUNTY_FIPS` (100.0% filled, 3,266 distinct), `XWALK_TYPE`.
- Contract year tables: `PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE`, `FEDERAL_ACTION_OBLIGATION`, `ACTION_DATE_FISCAL_YEAR`. On FY2024 the county code is filled on 93% of rows, 5 wide, 2,894 distinct counties (trap 2026-09-10). Other years not yet measured.

**The join, hop by hop.**
```
LABOR__FED_DOL_OLMS.ZIP (first 5) ➔ XWALK_ZCTA_COUNTY.ZCTA5                      overlap not yet measured
XWALK_ZCTA_COUNTY.COUNTY_FIPS ➔ FED_USASPENDING_CONTRACTS_FY*.PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE   overlap not yet measured
then group by county and year: sum(MEMBERS) against sum(FEDERAL_ACTION_OBLIGATION)
```

**A hit means.** Across counties, the years when contract dollars rise are the years when total reported membership falls, and the pattern holds after dropping the biggest metro counties.

**A miss means.** No relation, or the opposite sign. That would say contract growth and union membership move on separate clocks at county scale.

**Limits, said out loud.**
- The ZIP on a union report is the office address, not where members work. A national headquarters ZIP puts all its members in one county.
- The bridge is ZIP-area to county by largest land share. It agrees with a known county on 86.2% of test addresses, 99.5% where the ZIP sits in one county and 47.1% on the 5,933 ZIP areas that cross a line (trap 2026-09-11).
- `FEDERAL_ACTION_OBLIGATION` is signed; de-obligations are negative rows (trap 2026-09-05). Sum it as is for net dollars, never filter to positive for a county total.
- `SHORTAGE_AMOUNT` on the union table is junk, 78 column-shifted rows (trap 2026-09-05). Those same 78 rows have a numeric `UNION_NAME` and null `YEAR_COVERED`; drop them.
- The older contract views are not used: the full view is capped at exactly 20,000,000 rows and the 93M-row curated view has no county column.

**The picture.** Scatter: change in contract dollars per county on the horizontal axis, change in reported members on the vertical, one dot per county.

**First cheap check.** Count distinct first-5 `ZIP` values in LABOR__FED_DOL_OLMS that find a row in XWALK_ZCTA_COUNTY.

---

### W104 · Mines delinquent on fines, injuries climb next year

**The physical thing.** A mine with penalty dollars still owed to the Mine Safety and Health Administration, and the injury reports that mine files in the following calendar year.

**Status.** never run. The unpaid-fine side was measured on its own for another row: $1.82B proposed against $1.27B paid across 3.02M penalised violations, $548M never collected (wonder extract WN-079).

**Data grade.** B, because the mine id is a real shared key (13,338 mine ids appear in both tables) and the years overlap 2000 to 2026, but the only columns that could date a fine going delinquent (`FINAL_ORDER_ISSUE_DT`, `LAST_ACTION_CD`, `LAST_ACTION_DT`) sit on the unprofiled landing copy with no measured fill, and none of them is labelled a payment date.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS | 3,087,265 | one citation or order written at one mine | `VIOLATION_ISSUE_DATE` 1994-09-09 to 2026-07-18 | `MINE_ID` |
| LIBRARY_RAW.LANDING.FED_MSHA_VIOLATIONS | 3,087,266 | one citation or order, full 64-column file | not yet measured | `VIOLATION_NO`; `MINE_ID` |
| LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_ACCIDENTS | 273,623 | one reported accident or injury | `ACCIDENT_DATE` 2000-01-01 to 2026-07-14 | `MINE_ID` |
| LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES | 91,906 | one mine, current state | `CURRENT_STATUS_DT` 1925-01-01 to 2026-07-17 | `MINE_ID` |

**Columns that carry it.**
- LABOR__FED_MSHA_VIOLATIONS: `MINE_ID` (100.0% filled, 32,133 distinct), `CONTROLLER_ID` (93.24% filled), `PROPOSED_PENALTY`, `AMOUNT_DUE`, `AMOUNT_PAID`, `CAL_YR`, `VIOLATION_ISSUE_DATE` (100.0% filled). Fill of the three money columns not yet measured by the table profile.
- LIBRARY_RAW.LANDING.FED_MSHA_VIOLATIONS: `VIOLATION_NO`, `MINE_ID`, `FINAL_ORDER_ISSUE_DT`, `BILL_PRINT_DT`, `LAST_ACTION_CD`, `LAST_ACTION_DT`, `CONTESTED_IND`, `CONTESTED_DT`, `DOCKET_STATUS_CD`, `PROPOSED_PENALTY`, `AMOUNT_DUE`, `AMOUNT_PAID`. The mart drops the seven columns from `FINAL_ORDER_ISSUE_DT` to `DOCKET_STATUS_CD`. Fill not yet measured on any of them.
- LABOR__FED_MSHA_ACCIDENTS: `MINE_ID` (100.0% filled, 13,708 distinct), `CAL_YR`, `NO_INJURIES`, `DAYS_LOST`, `DEGREE_INJURY`, `IS_FATALITY`, `ACCIDENT_DATE` (100.0% filled).
- LABOR__FED_MSHA_MINES: `MINE_ID` (100.0% filled), `NO_EMPLOYEES`, `COAL_METAL_IND`, `CURRENT_MINE_STATUS`.

**The join, hop by hop.**
```
LABOR__FED_MSHA_VIOLATIONS.MINE_ID ➔ LABOR__FED_MSHA_ACCIDENTS.MINE_ID     measured: 13,338 shared mine ids
LABOR__FED_MSHA_VIOLATIONS.MINE_ID ➔ LABOR__FED_MSHA_MINES.MINE_ID         measured: 31,277 shared mine ids
dating the debt: LIBRARY_RAW.LANDING.FED_MSHA_VIOLATIONS.FINAL_ORDER_ISSUE_DT = the day the fine became final; delinquent in year t = final before t and AMOUNT_DUE > 0   (strip quotes; fill not yet measured)
per mine and CAL_YR t: unpaid share = 1 - sum(AMOUNT_PAID)/sum(PROPOSED_PENALTY); compare to injuries in CAL_YR t+1
```

**A hit means.** Mines in the top band of unpaid share in year t report more injuries per worker in year t+1 than mines of the same type and size that paid.

**A miss means.** Injury counts next year look the same for payers and non-payers. Not paying would then be a money habit, not a safety signal.

**Limits, said out loud.**
- The mart has no date for a fine after it is issued. The landing copy narrows that: `FINAL_ORDER_ISSUE_DT` says when a fine became final and owed, and `LAST_ACTION_CD` with `LAST_ACTION_DT` records the last thing that happened to it. No column is labelled a payment date, the meaning of the action codes is not in the warehouse, and the fill of all three is not yet measured. Until the codes are read, `AMOUNT_PAID` is still today's balance and a fine paid five years late looks like one paid on time.
- Contested fines are not delinquent fines. `CONTESTED_IND` and `CONTESTED_DT` on the landing copy let them be set aside row by row, which is better than the blunt rule of dropping the last 24 months that the mapped SQL for P-147 uses. Fill not yet measured.
- `NO_EMPLOYEES` is null on 39,735 of 91,906 mines (wonder extract WN-127) and is a current value, not a yearly one. Injuries per worker is only possible on the mines that carry it.
- 500,990 of 3,087,265 violation rows carry the standard $100 minimum fine (trap 2026-09-08). That is the penalty schedule, not duplication; it drags any per-row average down.
- The landing copy wraps every value in literal double quotes (warehouse topo map), so every landing date and amount must be stripped before casting, and an empty value is a pair of quotes, not a NULL. Whether the mart copy is stripped is not yet measured. The landing copy holds 3,087,266 rows against the mart's 3,087,265.

**The picture.** Two-line chart: years since the unpaid year on the horizontal axis, injuries per 100 workers on the vertical, one line for non-payers and one for payers.

**First cheap check.** On LIBRARY_RAW.LANDING.FED_MSHA_VIOLATIONS, count rows where `FINAL_ORDER_ISSUE_DT`, `LAST_ACTION_DT` and `CONTESTED_IND` are non-empty after stripping quotes, and list the distinct `LAST_ACTION_CD` values with counts.

---

### W107 · Fast-track devices recall more than standard

**The physical thing.** A medical device cleared by the FDA through an expedited or third-party review, and the recall notice later filed against that same device.

**Status.** never run.

**Data grade.** D, because the recall table's two link columns, `K_NUMBER_LIST` and `PRODUCT_CODE`, are both 0.0% filled, so no recall can be tied to a clearance or to a review route.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DEVICE_510K | 175,686 | one 510(k) clearance decision | `DECISION_DATE` 1976-07-15 to 2026-07-26 | `K_NUMBER` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DEVICE_PMA | 56,853 | one premarket approval or supplement | `DECISION_DATE` 1960-10-14 to 2026-07-26 | `PMA_NUMBER` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DEVICE_ENFORCEMENT | 39,635 | one device recall | `RECALL_INITIATION_DATE` 1930-12-11 to 2026-07-07; `REPORT_DATE` 2012-06-20 to 2026-07-29 | none usable |

**Columns that carry it.**
- HEALTH__FED_FDA_DEVICE_510K: `K_NUMBER` (100.0% filled, 172,884 distinct), `EXPEDITED_REVIEW_FLAG`, `THIRD_PARTY_FLAG`, `CLEARANCE_TYPE`, `PRODUCT_CODE` (1,442 blank strings), `APPLICANT`, `DECISION_DATE` (100.0% filled). Fill of the two flags not yet measured.
- HEALTH__FED_FDA_DEVICE_PMA: `PMA_NUMBER`, `EXPEDITED_REVIEW_FLAG`, `PRODUCT_CODE` (768 blank strings), `APPLICANT`, `DECISION_DATE` (100.0% filled).
- HEALTH__FED_FDA_DEVICE_ENFORCEMENT: `K_NUMBER_LIST` (0.0% filled, 0 distinct), `PRODUCT_CODE` (0.0% filled, 0 distinct), `CLASSIFICATION`, `RECALLING_FIRM`, `RECALL_INITIATION_DATE` (100.0% filled), `OPENFDA`.

**The join, hop by hop.**
```
planned: HEALTH__FED_FDA_DEVICE_510K.K_NUMBER ➔ one element of HEALTH__FED_FDA_DEVICE_ENFORCEMENT.K_NUMBER_LIST    dead: right side 0.0% filled
fallback: HEALTH__FED_FDA_DEVICE_510K.PRODUCT_CODE ➔ HEALTH__FED_FDA_DEVICE_ENFORCEMENT.PRODUCT_CODE               dead: right side 0.0% filled
left over: APPLICANT ➔ RECALLING_FIRM by name   reaches a company, not a device, so it cannot separate review routes
```

**A hit means.** Devices cleared with `EXPEDITED_REVIEW_FLAG` or `THIRD_PARTY_FLAG` set would show more recalls per clearance than standard ones in the same product code and decision year. This cannot be produced from the mart today.

**A miss means.** Equal recall rates across routes. This also cannot be produced today. A zero-match result from the current mart is an empty column, not an answer.

**Limits, said out loud.**
- Both join columns on the recall table are empty in the mart. The 2026-09-09 table map planned the join on them; the table profile, profiled 2026-09-08, shows 0.0% fill.
- The landing copy is no help. LIBRARY_RAW.LANDING.FED_FDA_DEVICE_ENFORCEMENT is 20 rows and 4 columns, a single `RAW` column plus lineage: the API envelope, not a per-recall table. The landing 510(k) and PMA copies are the same shape, 88 and 29 rows. No other device-recall table is landed.
- The `OPENFDA` column on the recall mart may hold the clearance numbers inside it. Its contents are not yet measured.
- The recall table has no PMA-number list column at all, so the premarket-approval route has no path even if the 510(k) path is repaired.
- A company-name match would mix every device a firm makes. One firm holds both fast-track and standard clearances, so the comparison falls apart.

**The picture.** Paired bars: review route on the horizontal axis, recalls per 1,000 clearances on the vertical, one bar per route.

**First cheap check.** Count rows in HEALTH__FED_FDA_DEVICE_ENFORCEMENT where `OPENFDA` is not null and contains a k_number. If that is zero, the fix is a reload, not a query.

---

### W111 · Recalled models with the most complaints, by state

**The physical thing.** One make, model and model year of car that is under a safety recall, and the owner complaints filed about that same car, counted by the owner's state.

**Status.** never run. Reworded on 2026-09-18: the old wording asked where models were sold, and no sales or registration table exists.

**Data grade.** B, because both tables are profiled and their years overlap, but the join is three text columns with no measured overlap, and complaints count people who complained, not cars on the road.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_RECALLS | 241,861 | one recall campaign applied to one make, model and model year | `NOTIFICATION_DATE` 1111-11-11 to 2027-08-16 (sentinels at both ends); `MODEL_YEAR` 1965 to 9999 | `MAKE` + `MODEL` + `MODEL_YEAR` |
| LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_COMPLAINTS | 2,227,941 | one owner complaint | `DATE_RECEIVED` 1995-01-01 to 2026-07-22 | `MAKE` + `MODEL` + `MODEL_YEAR` |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS_SOI | 179,796 | one ZIP and income band of tax returns | `TAX_YEAR` 2016 only | `STATE` (optional income context) |

**Columns that carry it.**
- CONSUMER_SAFETY__FED_NHTSA_RECALLS: `CAMPNO`, `MAKE`, `MODEL`, `MODEL_YEAR` (100.0% filled), `COMPONENT`, `POTENTIALLY_AFFECTED_UNITS`, `NOTIFICATION_DATE` (98.36% filled).
- CONSUMER_SAFETY__FED_NHTSA_COMPLAINTS: `CMPLID`, `MAKE`, `MODEL`, `MODEL_YEAR` (100.0% filled), `STATE`, `COMPONENT`, `DATE_RECEIVED` (100.0% filled), `CRASH`, `FIRE`, `INJURED`, `DEATHS`. Fill of `STATE` not yet measured.
- FINANCE__FED_IRS_SOI: `STATE`, `AGI`, `N_RETURNS`, `TAX_YEAR` (100.0% filled, single value 2016).

**The join, hop by hop.**
```
CONSUMER_SAFETY__FED_NHTSA_RECALLS.(MAKE, MODEL, MODEL_YEAR)
  ➔ CONSUMER_SAFETY__FED_NHTSA_COMPLAINTS.(MAKE, MODEL, MODEL_YEAR)     overlap not yet measured
group by STATE; optional: STATE ➔ FINANCE__FED_IRS_SOI.STATE for 2016 income per return
```

**A hit means.** A short list of recalled models carries most of the complaints, and the state ranking for those models differs from the state ranking for all complaints.

**A miss means.** Complaints on recalled models spread across states in the same shares as all complaints. Then state adds nothing and the finding is only the model list.

**Limits, said out loud.**
- No sales or registration table exists. A state with many complaints may simply have many of those cars.
- `MODEL_YEAR` uses 9999 as unknown in both tables. Drop it before joining or every unknown-year recall matches every unknown-year complaint.
- Model text is free-typed by the public on the complaint side. Spelling variants will split one model into several; the overlap has never been counted.
- The income table is tax year 2016 only. It can rank states by income once; it cannot follow them over time.
- The complaints mart is 2,227,941 rows, not the 2.6M an earlier draft quoted (table map 2026-09-09).

**The picture.** Small-multiple ranked bars: one panel per top recalled model, states on the vertical axis, complaint count on the horizontal, one bar per state.

**First cheap check.** Count distinct (`MAKE`, `MODEL`, `MODEL_YEAR`) in the recalls table, with `MODEL_YEAR` not 9999, that find at least one complaint row.

---

### W113 · UK shell controls a US nursing home

**The physical thing.** A company on the UK register of persons with significant control whose name is also printed as an owner on a US nursing home's Medicare ownership record.

**Status.** never run. The 2026-09-09 gap (no owner-level file) closed on 2026-09-10 when the nursing-home ownership file landed with owner names and addresses.

**Data grade.** C, because the only link between the UK register and the US owner file is a company name, there is no shared id and no shared address country column, so the output is a list of candidates to check by hand.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC | 15,804,611 | one controller of one UK company | `NOTIFIED_ON` 1083-01-01 to 2026-12-31 (sentinels) | `NAME` |
| LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP | 295,083 | one owner in one role on one nursing-home enrollment | one vintage, date range not yet measured | `ORGANIZATION_NAME_OWNER`; `ENROLLMENT_ID` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS | 14,425 | one nursing-home Medicare enrollment | snapshot | `ENROLLMENT_ID` ➔ `CCN` |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME | 14,700 | one nursing home, current state | snapshot | `CMS_CERTIFICATION_NUMBER_CCN` |

**Columns that carry it.**
- CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC: `COMPANY_NUMBER` (100.0% filled, 10,679,125 distinct), `NAME`, `KIND`, `ADDRESS_COUNTRY`, `COUNTRY_REGISTERED`, `REGISTRATION_NUMBER`, `NATURES_OF_CONTROL`, `NOTIFIED_ON` (100.0% filled), `CEASED_ON` (16.51% filled).
- FED_CMS_SNF_OWNERSHIP: `ENROLLMENT_ID`, `ORGANIZATION_NAME`, `ORGANIZATION_NAME_OWNER`, `TYPE_OWNER`, `ROLE_TEXT_OWNER`, `PERCENTAGE_OWNERSHIP`, `ADDRESS_LINE_1_OWNER`, `CITY_OWNER`, `STATE_OWNER`, `ZIP_CODE_OWNER`, `HOLDING_COMPANY_OWNER`. Fill not yet measured; the table is unprofiled.
- HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS: `ENROLLMENT_ID` (100.0% filled), `CCN` (100.0% filled, 14,026 distinct), `ORGANIZATION_NAME`.
- HEALTH__FED_CMS_NURSING_HOME: `CMS_CERTIFICATION_NUMBER_CCN` (100.0% filled, 14,328 distinct), `PROVIDER_NAME`, `STATE`, `NUMBER_OF_CERTIFIED_BEDS`, `OVERALL_RATING`.

**The join, hop by hop.**
```
CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC.NAME ➔ FED_CMS_SNF_OWNERSHIP.ORGANIZATION_NAME_OWNER     name only, overlap not yet measured
FED_CMS_SNF_OWNERSHIP.ENROLLMENT_ID ➔ HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS.ENROLLMENT_ID   measured: 288,550 of 295,083 owner rows join
HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS.CCN ➔ HEALTH__FED_CMS_NURSING_HOME.CMS_CERTIFICATION_NUMBER_CCN   measured: 100% on the landing pair
```

**A hit means.** A multi-word company name appears both as a controller or controlled company in the UK register and as an organization owner of a named US home, and the owner's address or the UK record's `COUNTRY_REGISTERED` gives a second reason to believe it is one company.

**A miss means.** No multi-word name survives. That says foreign parents sit one layer above what the US file prints, not that they do not exist.

**Limits, said out loud.**
- Name only. Multi-word names cleared 92% real and single words 8% in the 2026-09-03 test, and that test was inside the US; a UK and a US company can share a name legally.
- The owner file has no country column. `STATE_OWNER` and `ZIP_CODE_OWNER` are US-style fields; a UK address, if any, would sit in free text.
- The owner file is one vintage and shows current owners only (trap 2026-09-18). A shell that sold last year is gone.
- 6,533 owner rows name enrollments that the enrollment snapshot does not carry (trap 2026-09-10); those homes cannot be reached.
- Sources disagree on how complete the UK table is. The trap log on 2026-09-07 says the load stopped near 7M of an expected 10M+ rows; the table profile shows 15,804,611 rows. Treat every count as a floor until that is settled.

**The picture.** Network diagram: UK company on the left, US owner entity in the middle, nursing homes on the right, one line per ownership row.

**First cheap check.** Count distinct multi-word `ORGANIZATION_NAME_OWNER` values that equal, after upper-casing and trimming, any `NAME` in the UK table where `KIND` marks a corporate entity.

---

### W115 · UK controllers also control US contractors

**The physical thing.** A person or company named as a controller on the UK register whose name also appears as the parent, or as a top-paid officer, of a firm holding US federal contracts.

**Status.** never run.

**Data grade.** C, because there is no bridge from a UK company number to a US contractor id, so the link is a name match that yields candidates only.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC | 15,804,611 | one controller of one UK company | `NOTIFIED_ON` 1083-01-01 to 2026-12-31 (sentinels) | `NAME` |
| LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 through LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2026 (20 tables) | 96,976,021 | one contract transaction | FY2007-FY2026 | `RECIPIENT_PARENT_NAME`; `HIGHLY_COMPENSATED_OFFICER_1_NAME` |

**Columns that carry it.**
- CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC: `NAME`, `NAME_FORENAME`, `NAME_SURNAME`, `KIND`, `COMPANY_NUMBER` (100.0% filled), `COUNTRY_OF_RESIDENCE`, `COUNTRY_REGISTERED`, `NATURES_OF_CONTROL`, `CEASED_ON` (16.51% filled).
- Contract year tables: `RECIPIENT_UEI`, `RECIPIENT_NAME`, `RECIPIENT_PARENT_NAME`, `RECIPIENT_PARENT_UEI`, `RECIPIENT_COUNTRY_CODE`, `FOREIGN_OWNED`, `DOMESTIC_OR_FOREIGN_ENTITY_CODE`, `HIGHLY_COMPENSATED_OFFICER_1_NAME` to `HIGHLY_COMPENSATED_OFFICER_5_NAME`, `FEDERAL_ACTION_OBLIGATION`, `ACTION_DATE`. Fill not yet measured; the tables are unprofiled.

**The join, hop by hop.**
```
CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC.NAME (corporate kinds) ➔ FED_USASPENDING_CONTRACTS_FY*.RECIPIENT_PARENT_NAME      name only, overlap not yet measured
CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC.NAME (person kinds)    ➔ FED_USASPENDING_CONTRACTS_FY*.HIGHLY_COMPENSATED_OFFICER_n_NAME   name only, overlap not yet measured
narrow first: FOREIGN_OWNED set, or RECIPIENT_COUNTRY_CODE of the United Kingdom
```

**A hit means.** A multi-word UK corporate controller name equals the parent name of a contractor that the contract file itself flags as foreign owned. Two independent signs point the same way.

**A miss means.** Matches appear only on common names with no foreign flag. That is coincidence, and the honest count is zero confirmed.

**Limits, said out loud.**
- No company-number-to-UEI crosswalk exists. The 2026-09-09 map noted GLEIF could bridge by LEI, but the UK controller table carries no LEI.
- Person-name matches are the weakest kind here: single-word and common surnames were 8% real in the 2026-09-03 test. Officer-name hits need a second fact before they count.
- The curated 93M-row contract view is not used. It has 36 curated columns and is about 4% short of the archive for FY2024 (6,431,562 of 6,692,568 transactions matched, trap 2026-09-10).
- A 2026-08-31 trap says USAspending landing tables can carry case-sensitive lowercase column names. The table profile lists these year tables in upper case; confirm on one table before writing the union.
- UK table completeness is disputed between the trap log (about 7M of 10M+) and the table profile (15,804,611 rows). Counts are floors.

**The picture.** Ranked bar: matched parent names on the vertical axis, contract dollars on the horizontal, one bar per parent, coloured by whether `FOREIGN_OWNED` is set.

**First cheap check.** On FY2024 alone, count distinct `RECIPIENT_PARENT_NAME` where `FOREIGN_OWNED` is set, then count how many equal a UK `NAME`.

---

### W117 · US doctors who control UK companies, and how many

**The physical thing.** A person registered as controlling a UK company, resident in the United States, whose first and last name match a licensed US clinician in the national provider file.

**Status.** never run. Reworded on 2026-09-18: the old wording asked "what sector", and the UK company table has no industry code.

**Data grade.** C, because a first-name-plus-surname match between two countries identifies nobody on its own; the provider file has no birth year to check against the UK record's `DOB_YEAR`.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES | 9,606,683 | one provider id, person or organization | `PROVIDER_ENUMERATION_DATE` 2005-05-23 to 2026-06-06 | `PROVIDER_FIRST_NAME` + `PROVIDER_LAST_NAME_LEGAL_NAME` |
| LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC | 15,804,611 | one controller of one UK company | `NOTIFIED_ON` 1083-01-01 to 2026-12-31 (sentinels) | `NAME_FORENAME` + `NAME_SURNAME` |
| LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__INTL_UK_COMPANIES_HOUSE | 5,734,780 | one UK company | `INCORPORATION_DATE` 1327-01-01 to 2026-06-30 | `COMPANY_NUMBER` |

**Columns that carry it.**
- HEALTH__FED_CMS_NPPES: `NPI` (100.0% filled), `ENTITY_TYPE_CODE`, `PROVIDER_FIRST_NAME`, `PROVIDER_MIDDLE_NAME`, `PROVIDER_LAST_NAME_LEGAL_NAME`, `PROVIDER_CREDENTIAL_TEXT`, `PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME`, `HEALTHCARE_PROVIDER_TAXONOMY_CODE_1`, `PROVIDER_ENUMERATION_DATE` (96.4% filled).
- CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC: `NAME_FORENAME`, `NAME_MIDDLE`, `NAME_SURNAME`, `NAME_TITLE`, `DOB_YEAR` (87.26% filled), `COUNTRY_OF_RESIDENCE`, `NATIONALITY`, `COMPANY_NUMBER` (100.0% filled), `CEASED_ON` (16.51% filled).
- CORPORATE_REGISTRY__INTL_UK_COMPANIES_HOUSE: `COMPANY_NUMBER` (100.0% filled, 5,716,497 distinct), `COMPANY_NAME`, `COMPANY_CATEGORY` (100.0% filled, 28 distinct), `COMPANY_STATUS` (100.0% filled, 14 distinct).

**The join, hop by hop.**
```
CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC where COUNTRY_OF_RESIDENCE is the United States
  .(NAME_FORENAME, NAME_SURNAME) ➔ HEALTH__FED_CMS_NPPES.(PROVIDER_FIRST_NAME, PROVIDER_LAST_NAME_LEGAL_NAME)   name only, overlap not yet measured
CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC.COMPANY_NUMBER ➔ CORPORATE_REGISTRY__INTL_UK_COMPANIES_HOUSE.COMPANY_NUMBER   measured: 5,582,726 shared values
```

**A hit means.** A rare full name, middle name included, with a `NAME_TITLE` of Dr on the UK side, matches exactly one provider id on the US side. The count of such one-to-one matches is the answer to "how many".

**A miss means.** Every match is a common name hitting dozens of provider ids. Then the count is unknowable from names and the row needs a birth year or address on the US side.

**Limits, said out loud.**
- The provider file has 9,606,683 rows. Any common name matches many people. Keep only UK names that hit exactly one provider id, and say the count is a floor of candidates, not a count of doctors.
- No birth year on the US side, so `DOB_YEAR` on the UK side cannot confirm a match.
- The provider mart blanks deactivated ids: 346,179 rows have empty name fields (trap 2026-09-05). A retired doctor cannot match.
- The old "what sector" half is answerable after all, from the landing copy. LIBRARY_RAW.LANDING.INT_UK_COMPANIES_HOUSE (5,734,780 rows, 58 columns, unprofiled) carries `SICCode.SicText_1` to `SICCode.SicText_4`; the mart keeps only `COMPANY_CATEGORY`, a legal form. The 2026-09-09 table map said no SIC column exists; that was the mart. Fill of the SIC columns is not yet measured, and the landing column names are mixed case with dots, so they must be double-quoted in SQL.
- UK controller table completeness is disputed: about 7M of 10M+ per the 2026-09-07 trap, 15,804,611 rows per the table profile. The company table covers 5,582,726 of the controller table's 10,679,125 distinct company numbers.

**The picture.** Histogram: number of provider ids matched per UK name on the horizontal axis, count of UK names on the vertical; the one-match bar is the candidate pool.

**First cheap check.** Count rows in the UK controller table where `COUNTRY_OF_RESIDENCE` names the United States. That is the ceiling before any matching.

---

### W120 · Mine operators fined, paid, fined again for the same section of the Act

**The physical thing.** One mine controller cited under one section of the Mine Act, the fine paid, and then the same controller cited again under the same section.

**Status.** never run. Reworded on 2026-09-18 to mines only: the EPA enforcement summary keeps just the last penalty per site, so a repeat cannot be seen there.

**Data grade.** B, because the controller id is real and the citations run 32 years on a profiled table, but putting "paid" before "fined again" depends on `LAST_ACTION_CD` and `LAST_ACTION_DT` on the unprofiled landing copy, whose fill and code meanings are not yet measured.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS | 3,087,265 | one citation or order written at one mine | `VIOLATION_ISSUE_DATE` 1994-09-09 to 2026-07-18 | `CONTROLLER_ID` + `SECTION_OF_ACT` |
| LIBRARY_RAW.LANDING.FED_MSHA_VIOLATIONS | 3,087,266 | one citation or order, full 64-column file | not yet measured | `VIOLATION_NO`; `CONTROLLER_ID` + `PART_SECTION` |

**Columns that carry it.**
- LABOR__FED_MSHA_VIOLATIONS: `CONTROLLER_ID` (93.24% filled, 19,855 distinct), `CONTROLLER_NAME`, `VIOLATOR_ID`, `MINE_ID` (100.0% filled, 32,133 distinct), `SECTION_OF_ACT`, `VIOLATION_NO`, `VIOLATION_ISSUE_DATE` (100.0% filled), `PROPOSED_PENALTY`, `AMOUNT_DUE`, `AMOUNT_PAID`, `SIG_SUB`. Fill of `SECTION_OF_ACT` and of the money columns not yet measured.
- LIBRARY_RAW.LANDING.FED_MSHA_VIOLATIONS: `VIOLATION_NO`, `CONTROLLER_ID`, `SECTION_OF_ACT`, `SECTION_OF_ACT_1`, `SECTION_OF_ACT_2`, `PART_SECTION`, `CIT_ORD_SAFE`, `INITIAL_VIOL_NO`, `LAST_ACTION_CD`, `LAST_ACTION_DT`, `FINAL_ORDER_ISSUE_DT`, `CONTESTED_IND`, `TERMINATION_DT`, `VIOLATION_ISSUE_DT`. The mart keeps only `VIOLATION_NO`, `CONTROLLER_ID` and `SECTION_OF_ACT` of these. Fill not yet measured on any of them.

**The join, hop by hop.**
```
first pass, mart only, no join: group by CONTROLLER_ID, SECTION_OF_ACT; order citations by VIOLATION_ISSUE_DATE
sharper pass: LABOR__FED_MSHA_VIOLATIONS.VIOLATION_NO ➔ LIBRARY_RAW.LANDING.FED_MSHA_VIOLATIONS.VIOLATION_NO (strip quotes)    overlap not yet measured; 3,087,265 rows against 3,087,266
  same thing = same PART_SECTION, the regulation cited, not just the section of the Act
  repeat = a citation with AMOUNT_PAID >= PROPOSED_PENALTY and LAST_ACTION_DT earlier than the VIOLATION_ISSUE_DT of a later citation, same CONTROLLER_ID, same PART_SECTION
```

**A hit means.** A named set of controllers shows long chains, the same section cited year after year with each fine paid in full, while controllers of similar size show the section once or twice. Paying is then a running cost, not a correction.

**A miss means.** Repeat chains track mine count and inspection days and nothing else. Big operators repeat because they are big.

**Limits, said out loud.**
- The mart has no date after issue, so on the mart alone "paid, then fined again" is assumed from today's `AMOUNT_PAID`. The landing copy narrows this: `LAST_ACTION_DT` dates the last action on each fine. It is a payment date only if `LAST_ACTION_CD` says the last action was payment; the code meanings are not in the warehouse and the fill is not yet measured.
- "The same thing" gets sharper on the landing copy. The mart offers only `SECTION_OF_ACT`, which can cover many hazards. The landing copy adds `PART_SECTION`, the specific regulation cited. Neither copy has a violation narrative, so two citations under one regulation can still be different physical faults.
- Contested citations muddy "paid". `CONTESTED_IND` on the landing copy lets them be split out. Fill not yet measured.
- Every landing value is wrapped in literal double quotes (warehouse topo map). Strip before comparing `PART_SECTION` or casting `LAST_ACTION_DT`; an empty value is a pair of quotes, not a NULL.
- `CONTROLLER_ID` is empty on 6.76% of rows. Those citations fall out of every chain.
- 500,990 of 3,087,265 rows carry the standard $100 minimum fine (trap 2026-09-08). Small fines are the norm; rank by count of repeats, not by dollars alone.
- The EPA side was dropped on purpose. LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO holds one `DATE_LAST_PENALTY` per facility, filled on 3.89% of 3,135,554 rows, so it cannot show a first fine and a second.

**The picture.** Ranked bar: controllers on the vertical axis, number of paid-then-cited-again repeats on the horizontal, one bar per controller, top section labelled.

**First cheap check.** On LIBRARY_RAW.LANDING.FED_MSHA_VIOLATIONS, count rows where `PART_SECTION` and `LAST_ACTION_DT` are non-empty after stripping quotes, and list the distinct `LAST_ACTION_CD` values with counts.

---

### W121 · Zips file same complaint against same firm yearly

**The physical thing.** Consumers in one ZIP code filing the same kind of complaint about the same financial company, year after year, in the Consumer Financial Protection Bureau's complaint log.

**Status.** never run. The final list marks it "check masked ZIPs first".

**Data grade.** B, because it is one profiled table covering 2011 to 2026, but the public file masks part of its ZIP codes and how many has not been measured.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.CONSUMER_PROTECTION.CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS | 17,168,287 | one consumer complaint | `DATE_RECEIVED` 2011-12-01 to 2026-07-23 | `ZIP_CODE` + `COMPANY` + `ISSUE` |

**Columns that carry it.**
- CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS: `COMPLAINT_ID`, `ZIP_CODE` (99.99% filled, 36,864 distinct), `COMPANY` (100.0% filled, 8,088 distinct), `PRODUCT`, `ISSUE`, `SUB_ISSUE`, `RECEIVED_YEAR` (100.0% filled), `STATE`, `COMPANY_RESPONSE` (96.92% filled).

**The join, hop by hop.**
```
one table, no join
group by ZIP_CODE, COMPANY, ISSUE; count distinct RECEIVED_YEAR
a repeat cell = the same three values present in 5 or more distinct years
```

**A hit means.** A set of ZIP-and-company cells recur in most years, and their count is well above what the ZIP's population and the company's national volume would give by chance.

**A miss means.** Recurring cells are just the biggest companies in the biggest ZIPs. Then the pattern is size, and the entry closes with that stated.

**Limits, said out loud.**
- The public file masks ZIPs, as XXXXX or as three digits plus XX (table map 2026-09-09). The 36,864 distinct values include the masked forms. The masked share is not yet measured.
- A ZIP is a place, not a person. Repeats in a ZIP can be different people each year; the file has no consumer id.
- One narrative appears 27,510 times in this table (final list, M-239). Templated bulk filings can fake a local repeat; check `SUBMITTED_VIA` and narrative duplication on any top cell.
- The three national credit bureaus dominate volume. Run the ranking with and without them.
- `RECEIVED_YEAR` is stored as a date, the first of January of each year, 2011-01-01 to 2026-01-01; 2011 holds one month and 2026 is partial.

**The picture.** Heat grid: years across the horizontal axis, top ZIP-and-company cells down the vertical, one square per cell-year shaded by complaint count.

**First cheap check.** Count rows where `ZIP_CODE` contains the letter X, and count rows where it is five digits. That sizes the usable table.

---

### W122 · Counties flood, rebuild, flood again on federal money

**The physical thing.** One county that receives a federal flood disaster declaration, gets individual housing aid and other federal assistance, and then receives another flood declaration a few years later. This entry absorbs the old row 4 (counties aided three times).

**Status.** never run. The 2026-09-09 gaps (no declarations table, assistance capped at 1M rows a year) both closed on 2026-09-10 and 09-11.

**Data grade.** B, because county FIPS is a real shared key across all three sources, but the declarations and assistance tables are unprofiled and the housing-aid table has FIPS on only 74.21% of rows.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_RAW.LANDING.FED_FEMA_DISASTER_DECLARATIONS | 70,402 | one disaster and one designated area (5,264 disasters) | not yet measured | `FIPSSTATECODE` + `FIPSCOUNTYCODE` |
| LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS | 26,250,920 | one household's aid registration | `DECLARATION_DATE` 2002-10-24 to 2026-08-03 | `FIPS`; `DISASTER_NUMBER` |
| LIBRARY_RAW.LANDING.FED_USASPENDING_ASSISTANCE_FY2007 through LIBRARY_RAW.LANDING.FED_USASPENDING_ASSISTANCE_FY2026 (20 tables) | 128,155,142 | one assistance transaction | FY2007-FY2026 | `PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE` |

**Columns that carry it.**
- FED_FEMA_DISASTER_DECLARATIONS: `DISASTERNUMBER`, `INCIDENTTYPE`, `DECLARATIONDATE`, `INCIDENTBEGINDATE`, `FIPSSTATECODE`, `FIPSCOUNTYCODE`, `DESIGNATEDAREA`, `IHPROGRAMDECLARED`, `IAPROGRAMDECLARED`. Fill not yet measured; the table is unprofiled.
- HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS: `DISASTER_NUMBER` (100.0% filled, 620 distinct), `FIPS` (74.21% filled, 3,379 distinct), `DECLARATION_DATE` (100.0% filled), `INCIDENT_TYPE_CODE`, `FLOOD_DAMAGE`, `FLOOD_DAMAGE_AMOUNT`, `FLOOD_INSURANCE`, `IHP_AMOUNT`, `REPAIR_AMOUNT`, `REPLACEMENT_AMOUNT`.
- Assistance year tables: `PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE`, `CFDA_NUMBER`, `CFDA_TITLE`, `FEDERAL_ACTION_OBLIGATION`, `FACE_VALUE_OF_LOAN`, `ASSISTANCE_TYPE_CODE`, `AWARDING_AGENCY_NAME`, `ACTION_DATE_FISCAL_YEAR`. County code fill runs 71% in FY2007 to 99% in FY2020 (trap 2026-09-11).

**The join, hop by hop.**
```
FED_FEMA_DISASTER_DECLARATIONS.(FIPSSTATECODE || FIPSCOUNTYCODE) where INCIDENTTYPE is a flood   ➔ county list with COUNT(DISTINCT DISASTERNUMBER) >= 2
  ➔ HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS.FIPS (left-pad to 5) and DISASTER_NUMBER = DISASTERNUMBER     overlap not yet measured
  ➔ FED_USASPENDING_ASSISTANCE_FY*.PRIME_AWARD_TRANSACTION_PLACE_OF_PERFORMANCE_COUNTY_FIPS_CODE              overlap not yet measured
```

**A hit means.** A ranked list of counties with three or more separate flood declarations, where housing repair aid and disaster-program assistance dollars arrive after each one, and the dollars per event do not fall.

**A miss means.** Repeat-flood counties are few, or aid shrinks with each event. That would say the money does not keep rebuilding the same ground.

**Limits, said out loud.**
- The housing-aid `FIPS` column is unpadded text for states 01 to 09 ('1097' and '01097' both exist) and null on 69,662 rows by the 2026-09-05 trap; left-pad before grouping. The declarations table comes padded, 2 and 3 wide (trap 2026-09-10).
- Count disasters with COUNT(DISTINCT `DISASTERNUMBER`). The declarations table has one row per disaster and area, so a plain row count overstates events.
- Loans carry no obligation: assistance types 07 and 08 sum `FEDERAL_ACTION_OBLIGATION` to exactly $0.00 on 11,788,945 rows; the money sits in `FACE_VALUE_OF_LOAN` (trap 2026-09-11). A total on obligation alone misses disaster loans.
- No flood-insurance claims table is landed, only a participation roster (table map 2026-09-09). Insured rebuilding is invisible.
- Sources disagree on the housing-aid mart. The 2026-09-09 map calls it a sample, 12% of the file; the table profile shows 26,250,920 rows in the mart. The old capped assistance view (19,902,879 rows, 1M a year) is not used.

**The picture.** Map plus timeline: counties shaded by number of flood declarations; for the top ten, a strip with one tick per declaration and a bar of aid dollars under each tick.

**First cheap check.** In the declarations table alone, count counties with 3 or more distinct `DISASTERNUMBER` where `INCIDENTTYPE` is a flood.

---

### W123 · 990 hospital charity rises where wages fall

**The physical thing.** The charity-care cost a hospital reports on its Medicare cost report, set beside the change in average weekly wages in the hospital's county.

**Status.** never run. The final list marks the gap closed on 2026-09-10/11: the cost reports answer the charity side, and a hospital-to-tax-id crosswalk adds the 990 side.

**Data grade.** C, because the county wage table holds one year, 2022, so "wages fall" can only be that year's year-over-year change, and the charity figure comes from the cost report, not from a 990.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS | 80,077 | one hospital cost report | `FISCAL_YEAR_END_DATE` 2011-04-30 to 2024-09-30 | `PROVIDER_CCN`; `ZIP_CODE` |
| LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY | 46,960 | one ZIP-area and county pair | 2020 geography | `ZCTA5` ➔ `COUNTY_FIPS` |
| LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_BLS_QCEW | 3,619,437 | one area, ownership and industry cell of jobs and wages | `YEAR` 2022 only | `AREA_FIPS` |
| LIBRARY_MARTS.CORE.XWALK_HOSPITAL_CCN_EIN | 4,003 | one hospital certification number matched to one tax id | built 2026-09-11 | `CCN` ➔ `EIN` |

**Columns that carry it.**
- HEALTH__FED_CMS_HCRIS: `RPT_REC_NUM`, `PROVIDER_CCN` (100.0% filled, 7,057 distinct), `FISCAL_YEAR_END_DATE` (100.0% filled), `FISCAL_YEAR_LENGTH_DAYS`, `COST_OF_CHARITY_CARE`, `COST_OF_UNCOMPENSATED_CARE`, `TOTAL_BAD_DEBT_EXPENSE`, `TOTAL_COSTS`, `TYPE_OF_CONTROL`, `ZIP_CODE` (100.0% filled), `COUNTY`, `STATE_CODE`. Fill of the charity columns not yet measured by the table profile.
- XWALK_ZCTA_COUNTY: `ZCTA5`, `COUNTY_FIPS` (100.0% filled, 3,266 distinct).
- ECONOMICS__FED_BLS_QCEW: `AREA_FIPS` (100.0% filled, 4,532 distinct), `OWNERSHIP_CODE`, `INDUSTRY_CODE`, `AGGREGATION_LEVEL_CODE`, `ANNUAL_AVG_WEEKLY_WAGE`, `AVG_ANNUAL_PAY`, `YOY_WAGES_PCT_CHANGE`, `YEAR` (100.0% filled, 2022 only).
- XWALK_HOSPITAL_CCN_EIN: `CCN`, `EIN`, `MATCH_TIER`, `MATCH_RULE`, `EIN_NTEE`, `PROPRIETARY_NONPROFIT`. Unprofiled.

**The join, hop by hop.**
```
HEALTH__FED_CMS_HCRIS.ZIP_CODE (first 5) ➔ XWALK_ZCTA_COUNTY.ZCTA5                 overlap not yet measured
XWALK_ZCTA_COUNTY.COUNTY_FIPS ➔ ECONOMICS__FED_BLS_QCEW.AREA_FIPS                 overlap not yet measured
optional: HEALTH__FED_CMS_HCRIS.PROVIDER_CCN ➔ XWALK_HOSPITAL_CCN_EIN.CCN          4,003 hospital numbers to 2,075 tax ids; 3,891 of 6,703 nonprofit hospitals, 58%
```

**A hit means.** Among nonprofit hospitals, charity-care cost as a share of total cost in fiscal 2022 is higher in counties where `YOY_WAGES_PCT_CHANGE` was negative, after holding hospital size and state fixed.

**A miss means.** No relation between the county's wage change and the hospital's charity share. Charity care would then follow hospital policy or state rules, not local hardship.

**Limits, said out loud.**
- One wage year. The county wage table is 2022 only; the only "fall" it can show is the year-over-year column for that year. Thirteen years of cost reports have one year to pair with.
- The charity number is Worksheet S-10 of the cost report, not a 990 line. The landed 990 table has totals and no charity-care column (table map 2026-09-09).
- The cost-report grain is `RPT_REC_NUM`, unique on all 80,077 rows. Hospital plus year is not unique: 1,186 hospital-years carry more than one report (trap 2026-09-06). Filter `FISCAL_YEAR_LENGTH_DAYS` >= 300 to drop sale-day stubs (trap 2026-09-05).
- The text 'nan' was typed into float NaN, not NULL; `is not null` passes it (trap 2026-09-05). For-profit hospitals leave S-10 mostly blank, 1,120 of 1,841 reports, so compare nonprofits with nonprofits.
- The tax-id crosswalk is a name-and-address match, not an id join. The tax id is the system that files, not the building: 1,293 tax ids cover 3,222 rows (trap 2026-09-11). Read `MATCH_TIER` before trusting a row.

**The picture.** Scatter: county wage change in percent on the horizontal axis, charity-care cost as a share of total cost on the vertical, one dot per nonprofit hospital.

**First cheap check.** Count distinct `PROVIDER_CCN` with a fiscal year ending in 2022 whose first-5 `ZIP_CODE` reaches an `AREA_FIPS` present in the wage table.

---

### W124 · After plant count explains emissions, which operators dirtier

**The physical thing.** One power company's smokestack output, tons of carbon dioxide, sulfur dioxide and nitrogen oxides per megawatt-hour, compared with what its number and type of plants would predict.

**Status.** never run. The 2026-09-09 gap (one emissions year) closed on 2026-09-10 when four more emissions years landed.

**Data grade.** B, because the federal plant code is a real shared id and emissions now span five years, but four of the five emissions tables and the join overlap are unmeasured, and the owner table is a single vintage.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_RAW.LANDING.FED_EPA_EGRID_PLANT_2019 | 11,865 | one power plant, one year | 2019 | `ORISPL` |
| LIBRARY_RAW.LANDING.FED_EPA_EGRID_PLANT_2020 | 12,668 | one power plant, one year | 2020 | `ORISPL` |
| LIBRARY_RAW.LANDING.FED_EPA_EGRID_PLANT_2021 | 11,393 | one power plant, one year | 2021 | `ORISPL` |
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_EGRID_PLANT_2022 | 11,974 | one power plant, one year | `DATA_YEAR` 2022 | `DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE` |
| LIBRARY_RAW.LANDING.FED_EPA_EGRID_PLANT_2023 | 12,612 | one power plant, one year | 2023 | `ORISPL` |
| LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_4_OWNER | 5,495 | one owner's share of one generator | one vintage, no year column | `PLANT_CODE` |

**Columns that carry it.**
- FED_EPA_EGRID_PLANT_2019, 2020, 2021, 2023: `ORISPL`, `PNAME`, `OPRNAME`, `UTLSRVNM`, `PLPRMFL`, `PLFUELCT`, `NAMEPCAP`, `PLNGENAN`, `PLCO2AN`, `PLSO2AN`, `PLNOXAN`, `PSTATABB`. Fill not yet measured; the tables are unprofiled.
- ENVIRONMENT__FED_EPA_EGRID_PLANT_2022: `DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE`, `PLANT_NAME`, `UTILITY_NAME`, `PLANT_PRIMARY_FUEL`, `PLANT_NAMEPLATE_CAPACITY_MW`, `PLANT_ANNUAL_NET_GENERATION_MWH`, `PLANT_ANNUAL_CO2_EMISSIONS_TONS`, `PLANT_ANNUAL_SO2_EMISSIONS_TONS`, `PLANT_ANNUAL_NOX_EMISSIONS_TONS`, `DATA_YEAR` (99.99% filled).
- ENERGY__FED_EIA860_4_OWNER: `PLANT_CODE` (100.0% filled, 2,369 distinct), `GENERATOR_ID`, `OWNER_NAME`, `OWNERSHIP_ID`, `PERCENT_OWNED`, `UTILITY_ID`, `UTILITY_NAME`.

**The join, hop by hop.**
```
union the five emissions years on plant code: ORISPL (2019, 2020, 2021, 2023) = DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE (2022)
plant code ➔ ENERGY__FED_EIA860_4_OWNER.PLANT_CODE (cast text to number)       overlap not yet measured
operator route, no join: group the emissions tables by OPRNAME directly
fit emissions on plant count, fuel and generation; rank operators by what is left over
```

**A hit means.** A handful of operators sit well above the fitted line in all five years, with the same fuel mix as cleaner peers. The excess is per megawatt-hour, not per plant.

**A miss means.** Once fuel and generation are in the fit, nothing is left over that repeats across years. Dirtier would then just mean "burns more coal".

**Limits, said out loud.**
- The header style differs by year. 2019, 2020, 2021 and 2023 use short code names; 2022 was landed by another path with long captions (trap 2026-09-10). The union needs a column map, and 2022 has no column named operator; whether its `PLANT_TRANSMISSION_OR_DISTRIBUTION_SYSTEM_OWNER_NAME` is the same field as `OPRNAME` is not yet checked.
- The owner table names 2,369 distinct plants against 11,974 plants in the 2022 emissions table. Most plants have no owner row; for them the operator name on the emissions table is the only name.
- The owner table is one vintage, which the 2026-09-09 map gives as 2024, with no year column. Owners in 2024 are applied to emissions from 2019; a plant sold in between is credited to the wrong company.
- The emissions files get revised: 2020 is the v2 file and 2023 is rev2 (trap 2026-09-10). Note the revision with any published number.
- Operator names are free text. One company can appear under several spellings across years.

**The picture.** Scatter: predicted tons on the horizontal axis, actual tons on the vertical, one dot per operator-year, the 45-degree line drawn in.

**First cheap check.** Count distinct `ORISPL` in the 2023 table that equal a `PLANT_CODE` in the owner table.

---

### W125 · Workplaces with the highest injury rates by owner, three years

**The physical thing.** Work sites that file OSHA's yearly injury summary, grouped by the employer tax id printed on the form, ranked by injuries per hours worked across 2023, 2024 and 2025. This entry absorbs the old row 101 (injuries after a buyout), which had no acquisition table.

**Status.** never run. Reworded on 2026-09-18: three years cannot show "rising".

**Data grade.** B, because the establishment id and the employer tax id are real ids on profiled tables, but the tax id reaches an owner name for only a minority of sites and the hours column is wrong for multi-site filers.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2023 | 394,234 | one establishment's yearly injury summary | 2023 | `ESTABLISHMENT_ID`; `EIN` |
| LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2024 | 398,620 | same | 2024 | `ESTABLISHMENT_ID`; `EIN` |
| LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2025 | 383,283 | same | 2025 | `ESTABLISHMENT_ID`; `EIN` |
| LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF | 1,983,563 | one tax-exempt organization | `RULING_DATE` 1900-01-01 to 2026-06-01 | `EIN` |
| LIBRARY_RAW.LANDING.FED_DOL_FORM5500_FULL | 4,299,671 | one benefit-plan annual filing | not yet measured | `SPONS_DFE_EIN` |

**Columns that carry it.**
- The three OSHA tables: `ESTABLISHMENT_ID` (100.0% filled), `EIN` (89.62% filled in 2023, 89.15% in 2024, 88.7% in 2025), `ESTABLISHMENT_NAME`, `COMPANY_NAME` (95.09%, 95.1%, 95.03% filled), `NAICS_CODE`, `STATE`, `ANNUAL_AVERAGE_EMPLOYEES`, `TOTAL_HOURS_WORKED`, `TOTAL_INJURIES`, `TOTAL_DAFW_CASES`, `TOTAL_DJTR_CASES`, `TOTAL_DEATHS`, `YEAR_FILING_FOR` (100.0% filled).
- CORPORATE_REGISTRY__FED_IRS_EO_BMF: `EIN` (100.0% filled), `ORG_NAME`, `STATE`, `NTEE_CODE`.
- FED_DOL_FORM5500_FULL: `SPONS_DFE_EIN`, `SPONSOR_DFE_NAME`, `SPONS_DFE_MAIL_US_STATE`, `BUSINESS_CODE`. Fill not yet measured; the table is unprofiled.

**The join, hop by hop.**
```
LABOR__FED_OSHA_ITA_300A_SUMMARY_2023.ESTABLISHMENT_ID ➔ ..._2024.ESTABLISHMENT_ID     measured: 219,860 shared values
LABOR__FED_OSHA_ITA_300A_SUMMARY_2024.ESTABLISHMENT_ID ➔ ..._2025.ESTABLISHMENT_ID     measured: 223,271 shared values
group by EIN (left-pad to 9) = the owner
EIN ➔ CORPORATE_REGISTRY__FED_IRS_EO_BMF.EIN        measured: 6,930 shared (2023), 6,414 (2024), 6,455 (2025); names nonprofits only
EIN ➔ FED_DOL_FORM5500_FULL.SPONS_DFE_EIN           measured: 20,756 of 109,146 OSHA tax ids in 2024, 19.0%
```

**A hit means.** A named set of tax ids whose sites run several times their industry's injury rate in all three years, across more than one site. The same owner, the same rate, different buildings.

**A miss means.** High rates belong to single sites and do not travel with the tax id. Then the owner is the wrong unit and the building is the right one.

**Limits, said out loud.**
- `TOTAL_HOURS_WORKED` is not per site for multi-site filers. Caltrans files 470 rows in 2024 carrying 14 distinct hour values (trap 2026-09-08). Hours sum to 1,065B against 138.8M employees, about 7,672 hours per employee (wonder extract WN-138). Keep rows where hours per employee falls between 800 and 3,000 (88% of rows) before any rate.
- `COMPANY_NAME` is not the company; on the Caltrans rows it reads 'Facility 982' (trap 2026-09-08). Group on `EIN`, never on the name.
- `EIN` is blank on 43,260 of 398,620 rows in 2024 and leading zeros are stripped on 14,083 rows; pad before joining. It does not carry the all-zeros filler other tables use.
- An owner name exists for a minority. The benefit-plan table matches 19.0% of OSHA tax ids because only plan sponsors file it; the nonprofit table matches 6,414 tax ids in 2024. The rest stay a nine-digit number.
- Three years. The question ranks level, not trend. The buyout version (old row 101) has no acquisition table; a changed `EIN` on the same `ESTABLISHMENT_ID` is the only proxy.

**The picture.** Ranked dot plot: owners on the vertical axis, injuries per 200,000 hours on the horizontal, three dots per owner, one per year.

**First cheap check.** Count distinct padded `EIN` values in the 2024 table that carry 5 or more distinct `ESTABLISHMENT_ID`.

---

### P-146 · Mine deaths without a paper trail

**The physical thing.** A mine operator whose workers died on the job while the inspectors' citation book for that operator stayed thin: many deaths per thousand citations, against what operators of the same size and mine type show.

**Status.** partially measured. The inputs were verified when the row was scored: 1,208 fatalities, 3.09M violations, 19,430 controllers with violations, 6,634 with accidents, 26 years of overlap (wonder extract WN-127). The ratio itself has never been run.

**Data grade.** A, because mine id and controller id are real shared keys on three profiled tables, with measured overlap, and the two event tables overlap from 2000 to 2026.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_ACCIDENTS | 273,623 | one reported accident or injury | `ACCIDENT_DATE` 2000-01-01 to 2026-07-14 | `CONTROLLER_ID`; `MINE_ID` |
| LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS | 3,087,265 | one citation or order | `VIOLATION_ISSUE_DATE` 1994-09-09 to 2026-07-18 | `CONTROLLER_ID`; `MINE_ID` |
| LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES | 91,906 | one mine, current state | `CURRENT_STATUS_DT` 1925-01-01 to 2026-07-17 | `MINE_ID` |

**Columns that carry it.**
- LABOR__FED_MSHA_ACCIDENTS: `MINE_ID` (100.0% filled, 13,708 distinct), `CONTROLLER_ID` (99.74% filled, 6,722 distinct), `CONTROLLER_NAME`, `IS_FATALITY`, `DEGREE_INJURY`, `NARRATIVE`, `ACCIDENT_DATE` (100.0% filled), `COAL_METAL_IND`.
- LABOR__FED_MSHA_VIOLATIONS: `MINE_ID` (100.0% filled), `CONTROLLER_ID` (93.24% filled, 19,855 distinct), `VIOLATION_NO`, `SIG_SUB`, `IS_SIGNIFICANT_AND_SUBSTANTIAL`, `VIOLATION_OCCUR_DATE` (100.0% filled), `EVENT_NO`.
- LABOR__FED_MSHA_MINES: `MINE_ID` (100.0% filled), `NO_EMPLOYEES`, `CURRENT_MINE_TYPE`, `COAL_METAL_IND`, `CURRENT_MINE_STATUS`.

**The join, hop by hop.**
```
LABOR__FED_MSHA_ACCIDENTS.CONTROLLER_ID ➔ LABOR__FED_MSHA_VIOLATIONS.CONTROLLER_ID     measured: 6,565 shared controller ids
LABOR__FED_MSHA_ACCIDENTS.MINE_ID ➔ LABOR__FED_MSHA_VIOLATIONS.MINE_ID                 measured: 13,338 shared mine ids
LABOR__FED_MSHA_ACCIDENTS.MINE_ID ➔ LABOR__FED_MSHA_MINES.MINE_ID                      measured: 13,489 shared mine ids
per controller, fixed window: deaths per 1,000 citations, and deaths per employee-year; residual against size and COAL_METAL_IND
```

**A hit means.** A short list of controllers with several deaths and a citation count far below peers of the same size and mine type. The deaths are on file; the warnings before them are not.

**A miss means.** Deaths per citation is flat once size and mine type are held fixed. Citations then track danger about as well as a count can.

**Limits, said out loud.**
- 1,208 deaths spread over thousands of controllers. Most controllers have zero or one; a ratio on one death is noise. Set a floor, such as two or more deaths, and say how many controllers clear it.
- A thin citation book has two readings: an operator nobody inspected, or a clean operator with bad luck. The table cannot tell them apart without inspection days; `VIOLATOR_INSPECTION_DAY_CNT` exists and its fill is not yet measured.
- `NO_EMPLOYEES` is null on 39,735 of 91,906 mines and 48% of mines have no latitude or longitude (wonder extract WN-127). The per-worker rate covers only part of the field.
- Citations start in 1994 and accidents in 2000. Use 2000 onward for both.
- The same 20-draw random control used on P-147 is needed here (mapped SQL file, 2026-09-13). Without it a ranked list is just a list.

**The picture.** Scatter on log axes: citations per controller on the horizontal, deaths on the vertical, one dot per controller, outliers above the fitted band labelled.

**First cheap check.** Count rows in LABOR__FED_MSHA_ACCIDENTS where `IS_FATALITY` is true. It should return 1,208.

---

### P-147 · A mine changes hands, its violation rate changes

**The physical thing.** The same hole in the ground with a new company name on the citation. The controller id is printed on every citation, so the day the name changes can be read off the citations themselves.

**Status.** partially measured. Verified when scored: 6,358 mines saw 2 controllers, 2,091 saw 3, one had 11; a later probe counted 9,504 mines that changed controller (idea book P-147). The before-and-after rate has never been run; the full SQL is mapped in the 2026-09-13 top-three file.

**Data grade.** A, because everything rides on one profiled table with a controller id on 93.24% of 3,087,265 citations across 32 years, and the mine table joins on a measured shared id.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS | 3,087,265 | one citation or order | `VIOLATION_ISSUE_DATE` 1994-09-09 to 2026-07-18 | `MINE_ID` + `CONTROLLER_ID` |
| LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES | 91,906 | one mine, current state | `CURRENT_STATUS_DT` 1925-01-01 to 2026-07-17 | `MINE_ID` |

**Columns that carry it.**
- LABOR__FED_MSHA_VIOLATIONS: `MINE_ID` (100.0% filled, 32,133 distinct), `CONTROLLER_ID` (93.24% filled, 19,855 distinct), `VIOLATION_NO`, `EVENT_NO`, `VIOLATION_ISSUE_DATE` (100.0% filled), `SIG_SUB`, `IS_SIGNIFICANT_AND_SUBSTANTIAL`, `_LOADED_AT`.
- LABOR__FED_MSHA_MINES: `MINE_ID` (100.0% filled), `COAL_METAL_IND`, `STATE`, `NO_EMPLOYEES`, `CURRENT_CONTROLLER_ID` (98.88% filled).

**The join, hop by hop.**
```
LABOR__FED_MSHA_VIOLATIONS, ordered by VIOLATION_ISSUE_DATE within MINE_ID
  ➔ handover = first citation whose CONTROLLER_ID differs from the one before it, same MINE_ID
  ➔ 24 months before against 24 months after: serious citations (SIG_SUB) per inspection event (distinct EVENT_NO)
LABOR__FED_MSHA_VIOLATIONS.MINE_ID ➔ LABOR__FED_MSHA_MINES.MINE_ID        measured: 31,277 shared mine ids
control: a random date on each never-sold mine, 20 draws
```

**A hit means.** Serious citations per inspection event drop hard in the 24 months after a handover, and the drop is larger than at matched mines that never changed hands. The follow-up names the old controllers that show up as new controllers elsewhere within a year.

**A miss means.** The rate is flat across the handover. New name, same mine, same citations.

**Limits, said out loud.**
- The handover date is the first citation under the new name, not the sale date. A mine with no citations for a year after a sale gets a late handover date.
- The mine table holds the current controller only. It cannot supply the history; the citations table has to.
- `CONTROLLER_ID` is empty on 6.76% of citations. An empty value between two real ones must not be read as a change of hands.
- Sources disagree on 500,990 rows. The mapped SQL file calls them copy-paste duplicates to remove on `VIOLATION_NO`; the trap log (2026-09-08) says 500,990 rows carry the standard $100 minimum fine and are the penalty schedule at work. Count distinct `VIOLATION_NO` against the row count before deleting anything.
- The last 24 months of citations are inside the appeal window and are left out. The landing copy of this file wraps values in literal double quotes (warehouse topo map); whether the mart is stripped is not yet measured, so the mapped SQL strips quotes on every key.
- The table profile reports 92,336 distinct `MINE_ID` on a 91,906-row mine table. Both cannot be true; recount before treating `MINE_ID` as unique there.

**The picture.** Event-study line: months from handover on the horizontal axis, minus 24 to plus 24, serious citations per inspection event on the vertical, one line for sold mines and one for the random-date control.

**First cheap check.** Count `MINE_ID` values with 2 or more distinct non-empty `CONTROLLER_ID`. The sources say roughly 9,500.

---

### P-148 · A death at one mine changes the operator's other mines

**The physical thing.** A worker dies at one mine. The question is what the citation record looks like, in the months after, at the other mines run by the same controller.

**Status.** partially measured. Verified when scored: 1,208 fatalities, 6,082 controllers with 2 or more mines, 6,634 controllers with accidents, 26-year overlap (wonder extract WN-129). The before-and-after at sister mines has never been run.

**Data grade.** A, because controller id and mine id are real shared keys on profiled tables with measured overlap, and the trigger, a death, is dated to the day.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_ACCIDENTS | 273,623 | one reported accident or injury | `ACCIDENT_DATE` 2000-01-01 to 2026-07-14 | `CONTROLLER_ID`; `MINE_ID` |
| LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS | 3,087,265 | one citation or order | `VIOLATION_ISSUE_DATE` 1994-09-09 to 2026-07-18 | `CONTROLLER_ID`; `MINE_ID` |
| LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES | 91,906 | one mine, current state | `CURRENT_STATUS_DT` 1925-01-01 to 2026-07-17 | `MINE_ID` |

**Columns that carry it.**
- LABOR__FED_MSHA_ACCIDENTS: `IS_FATALITY`, `ACCIDENT_DATE` (100.0% filled), `MINE_ID` (100.0% filled), `CONTROLLER_ID` (99.74% filled, 6,722 distinct).
- LABOR__FED_MSHA_VIOLATIONS: `CONTROLLER_ID` (93.24% filled), `MINE_ID` (100.0% filled), `VIOLATION_ISSUE_DATE` (100.0% filled), `EVENT_NO`, `SIG_SUB`, `VIOLATION_NO`.
- LABOR__FED_MSHA_MINES: `MINE_ID` (100.0% filled), `STATE`, `COAL_METAL_IND`, `NO_EMPLOYEES`.

**The join, hop by hop.**
```
LABOR__FED_MSHA_ACCIDENTS where IS_FATALITY ➔ (CONTROLLER_ID, MINE_ID, ACCIDENT_DATE) = the trigger
trigger.CONTROLLER_ID ➔ LABOR__FED_MSHA_VIOLATIONS.CONTROLLER_ID, keeping MINE_ID <> the trigger mine     measured: 6,565 shared controller ids
compare citations per inspection event, 12 months before against 12 months after ACCIDENT_DATE
LABOR__FED_MSHA_VIOLATIONS.MINE_ID ➔ LABOR__FED_MSHA_MINES.MINE_ID for state and mine type               measured: 31,277 shared mine ids
```

**A hit means.** Citations at the sister mines jump after the death, more than at same-state, same-type mines under other controllers over the same months. Either inspectors follow the owner, or the owner's other sites were in the same shape.

**A miss means.** Sister mines look like everyone else's after the death. A fatality stays a one-site event in the record.

**Limits, said out loud.**
- More citations can mean more inspecting, not more danger. Divide by distinct `EVENT_NO`, the inspection event, and show both the numerator and the denominator.
- The controller on a citation is the controller at that time; the mine table gives only today's. Build the sister list from the citations table as of the death date.
- Only controllers with 2 or more mines count: 6,082 of them. Deaths at single-mine controllers drop out, and how many of the 1,208 deaths survive that cut is not yet measured.
- The earlier run on 2026-08-21 found mines spike together under one owner, plus 34.3% over a 20-draw control. It did not control for the regulator's district; that open question is entry WN-136 and applies here too.
- Landing-copy values carry literal double quotes (warehouse topo map); mart state not yet measured. Strip before joining.

**The picture.** Event-study line: months from the death on the horizontal axis, citations per inspection event at sister mines on the vertical, with a second line for matched control mines.

**First cheap check.** Count fatal accidents whose `CONTROLLER_ID` appears on citations at 2 or more distinct `MINE_ID` in the same calendar year.

---

### P-159 · OSHA injury counts bunch on round numbers

**The physical thing.** The injury total an employer types into OSHA's yearly summary form. If employers estimate instead of count, totals ending in 0 and 5 show up more often than they should, and the question is whether that grows with employer size.

**Status.** never run. The repo holds a bunching detector; it has not been pointed at these tables (wonder extract WN-138).

**Data grade.** A, because it needs no join: three profiled tables of the same form, one per year, read column by column.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2023 | 394,234 | one establishment's yearly injury summary | 2023 | none, single table |
| LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2024 | 398,620 | same | 2024 | none, single table |
| LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2025 | 383,283 | same | 2025 | none, single table |

**Columns that carry it.**
- All three tables: `TOTAL_INJURIES`, `TOTAL_DAFW_CASES`, `TOTAL_DJTR_CASES`, `TOTAL_OTHER_CASES`, `TOTAL_DAFW_DAYS`, `TOTAL_HOURS_WORKED`, `ANNUAL_AVERAGE_EMPLOYEES`, `SIZE`, `NAICS_CODE`, `ESTABLISHMENT_ID` (100.0% filled), `YEAR_FILING_FOR` (100.0% filled). Fill of the count columns not yet measured by the table profile.

**The join, hop by hop.**
```
one table per year, no join; stack the three years
group by SIZE band and by last digit of TOTAL_INJURIES (for totals of 10 or more)
compare the share ending in 0 or 5 with the 20% a smooth count would give
```

**A hit means.** Totals ending in 0 or 5 are clearly over 20% of filings, and the excess climbs with each size band. Bigger employers round more.

**A miss means.** Last digits are flat at every size. The counts look counted.

**Limits, said out loud.**
- Most sites report small numbers. Totals under 10 have no meaningful last digit; the test runs only on the larger filers, and how many rows that leaves is not yet measured.
- Multi-site filers stamp one number on many rows. Caltrans files 470 rows in 2024 with 14 distinct hour values (trap 2026-09-08). Collapse identical (hours, employees, state, industry) blocks first or one rounded parent number is counted hundreds of times.
- `TOTAL_HOURS_WORKED` is the natural second test and has a junk tail: 117 rows over 100M hours in 2024, and a total of 1,065B hours against 138.8M employees (wonder extract WN-138). Trim to 800 to 3,000 hours per employee.
- Bunching shows estimating, not hiding. A round number is not proof of under-reporting.
- Day counts (`TOTAL_DAFW_DAYS`, `TOTAL_DJTR_DAYS`) may bunch for reasons set by the form's own rules. Those rules are not in the warehouse; read them before flagging those columns.

**The picture.** Bar chart: last digit 0 to 9 on the horizontal axis, share of filings on the vertical, one panel per employer size band, with a line at 10%.

**First cheap check.** In the 2024 table, count rows with `TOTAL_INJURIES` of 10 or more, then count how many of those end in 0.

---

### P-160 · After a reported death, do hours and injuries change

**The physical thing.** A work site that wrote a death on its OSHA summary one year, and what the same site wrote for hours worked and injuries the next year. The point is to separate a safety change from a reporting change.

**Status.** partially measured. Verified when scored: 219,860 establishments appear in both 2023 and 2024; reported deaths run 859, then 812, then 778 across the three years (wonder extract WN-140). The before-and-after has never been run.

**Data grade.** B, because the establishment id is a real key with measured overlap between years, but three years give at most two before-and-after pairs per site.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2023 | 394,234 | one establishment's yearly injury summary | 2023 | `ESTABLISHMENT_ID` |
| LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2024 | 398,620 | same | 2024 | `ESTABLISHMENT_ID` |
| LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2025 | 383,283 | same | 2025 | `ESTABLISHMENT_ID` |

**Columns that carry it.**
- All three tables: `ESTABLISHMENT_ID` (100.0% filled; 388,245, 391,778 and 381,794 distinct), `TOTAL_DEATHS`, `TOTAL_INJURIES`, `TOTAL_DAFW_CASES`, `TOTAL_HOURS_WORKED`, `ANNUAL_AVERAGE_EMPLOYEES`, `NAICS_CODE`, `STATE`, `YEAR_FILING_FOR` (100.0% filled).

**The join, hop by hop.**
```
LABOR__FED_OSHA_ITA_300A_SUMMARY_2023.ESTABLISHMENT_ID ➔ ..._2024.ESTABLISHMENT_ID     measured: 219,860 shared values
LABOR__FED_OSHA_ITA_300A_SUMMARY_2024.ESTABLISHMENT_ID ➔ ..._2025.ESTABLISHMENT_ID     measured: 223,271 shared values
LABOR__FED_OSHA_ITA_300A_SUMMARY_2023.ESTABLISHMENT_ID ➔ ..._2025.ESTABLISHMENT_ID     measured: 174,093 shared values
treated = TOTAL_DEATHS > 0 in year t; outcome = change in injuries per hour and in hours, t to t+1; control = same industry and state, no death
```

**A hit means.** Sites with a death report fewer injuries per hour the next year while hours hold steady: a safety change. Or they stop filing, or hours collapse: a reporting or shutdown change. Either pattern, clearly apart from the controls, is a finding.

**A miss means.** Death sites move the same as their peers the next year. A death on the form changes nothing visible in the next form.

**Limits, said out loud.**
- Small numbers. Deaths are 859, 812 and 778 a year, and only the sites that file again the next year can be followed. How many death sites reappear is not yet measured.
- Dropping out of the file is itself an outcome. A site that closes or falls under the filing threshold after a death vanishes; count the vanished, do not just drop them.
- Join on `ESTABLISHMENT_ID`, not `EIN`. `EIN` has a minimum length of 1 and is blank on 43,260 rows in 2024 (wonder extract WN-140).
- `ESTABLISHMENT_ID` is not quite unique within a year: 388,245 distinct on 394,234 rows in 2023. Decide how to handle the repeats before pairing years.
- `TOTAL_HOURS_WORKED` is wrong for multi-site filers and has a junk tail (trap 2026-09-08). A change in hours at such a site is a change in the parent's number.

**The picture.** Slope chart: year t on the left, year t+1 on the right, injuries per 200,000 hours on the vertical, one faint line per death site and one bold line for the control median.

**First cheap check.** Count `ESTABLISHMENT_ID` values with `TOTAL_DEATHS` > 0 in the 2023 table that also appear in the 2024 table.

---

### WN-136 · Same-owner co-spike, controlling for district and calendar

**The physical thing.** Two mines with the same controller get a burst of citations in the same month. The question is whether the owner explains that, or whether it is one MSHA district office working through its territory on its own calendar.

**Status.** partially measured. The uncontrolled version ran on 2026-08-21: mines under one owner spike together 34.3% more often than a 20-draw random control (wonder extract WN-134). The district-and-calendar control has never been run.

**Data grade.** B, because the landing copy of the mine file carries the MSHA district and field office for every mine row, which is the control the question asks for, but that copy is unprofiled, so the fill of `DISTRICT` is not yet measured, and it records today's district only.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS | 3,087,265 | one citation or order | `VIOLATION_ISSUE_DATE` 1994-09-09 to 2026-07-18 | `MINE_ID`; `CONTROLLER_ID` |
| LIBRARY_RAW.LANDING.FED_MSHA_MINES | 91,906 | one mine, current state, 62 columns | not yet measured | `MINE_ID`; `DISTRICT` |
| LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES | 91,906 | one mine, current state, 23 columns | `CURRENT_STATUS_DT` 1925-01-01 to 2026-07-17 | `MINE_ID` |

**Columns that carry it.**
- LABOR__FED_MSHA_VIOLATIONS: `MINE_ID` (100.0% filled), `CONTROLLER_ID` (93.24% filled, 19,855 distinct), `VIOLATION_ISSUE_DATE` (100.0% filled), `EVENT_NO`, `COAL_METAL_IND`.
- LIBRARY_RAW.LANDING.FED_MSHA_MINES: `MINE_ID`, `DISTRICT`, `OFFICE_CD`, `OFFICE_NAME`, `STATE`, `FIPS_CNTY_CD`, `COAL_METAL_IND`, `CURRENT_CONTROLLER_BEGIN_DT`. Fill not yet measured on any of them.
- LABOR__FED_MSHA_MINES: `MINE_ID` (100.0% filled), `STATE`, `FIPS_CNTY_CD` (100.0% filled, 298 distinct), `COAL_METAL_IND`. The mart drops `DISTRICT`, `OFFICE_CD` and `OFFICE_NAME`; it is kept here only for its measured join.

**The join, hop by hop.**
```
LABOR__FED_MSHA_VIOLATIONS.MINE_ID ➔ LABOR__FED_MSHA_MINES.MINE_ID        measured: 31,277 shared mine ids
LABOR__FED_MSHA_VIOLATIONS.MINE_ID ➔ LIBRARY_RAW.LANDING.FED_MSHA_MINES.MINE_ID (strip quotes)   overlap not yet measured; same 91,906 rows as the mart
spike = a mine-month far above that mine's own average
co-spike rate for pairs sharing CONTROLLER_ID, against pairs sharing DISTRICT (or OFFICE_CD) but not CONTROLLER_ID, same month
```

**A hit means.** Same-owner pairs still spike together more than same-district, different-owner pairs in the same month. The owner effect survives the inspector's calendar.

**A miss means.** Same-district pairs spike together just as often. The 34.3% was the district office's route, not the owner.

**Limits, said out loud.**
- `DISTRICT`, `OFFICE_CD` and `OFFICE_NAME` exist by name on the landing mine file. Their fill is not yet measured, and two columns found by name in this warehouse turned out empty (traps 2026-09-18). Count distinct values first.
- The district is today's. A mine moved between districts over 32 years is filed under its current one for every month.
- Every value in the landing MSHA files is wrapped in literal double quotes (warehouse topo map). Strip them before joining or grouping, or `DISTRICT` reads as quoted text and `MINE_ID` matches nothing.
- The wonder extract (WN-136) says "no district column, derive from mine state and county". That was true of the mart and the violations table; the landing mine file has the column.
- The mine table holds today's controller. Build owner pairs from the `CONTROLLER_ID` on the citations, as of the month in question. An owner whose mines all sit in one district gives the test no power; report how many same-owner pairs cross a district line.
- The row also names nursing homes. That half is not in these tables and is left out here.

**The picture.** Paired bars: pair type on the horizontal axis (same owner, same district different owner, random), share of spikes that are co-spikes on the vertical.

**First cheap check.** On LIBRARY_RAW.LANDING.FED_MSHA_MINES, count rows with a non-empty `DISTRICT` after stripping quotes, and list its distinct values.

---

### P-149 · Mine inspection has a season, accidents fill the gaps

**The physical thing.** The calendar of when inspectors write citations at mines, month by month for 26 years, laid over the calendar of when miners get hurt.

**Status.** never run. Verified when scored: citations 1994 to 2026, 3.09M rows, 31,277 mines; accidents 2000 to 2026, 273,623 rows; 26 years of overlap, the longest on the list (wonder extract WN-141).

**Data grade.** B, because the citation and accident dates are fully filled with a measured shared mine id, and the landing copy adds each inspection's begin and end dates, but those two columns have no measured fill and there is still no inspections table: an inspection that found nothing leaves no row in any copy.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS | 3,087,265 | one citation or order | `VIOLATION_ISSUE_DATE` 1994-09-09 to 2026-07-18 | `VIOLATION_ISSUE_DATE`; `MINE_ID` |
| LIBRARY_RAW.LANDING.FED_MSHA_VIOLATIONS | 3,087,266 | one citation or order, full 64-column file | not yet measured | `EVENT_NO`; `INSPECTION_BEGIN_DT` |
| LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_ACCIDENTS | 273,623 | one reported accident or injury | `ACCIDENT_DATE` 2000-01-01 to 2026-07-14 | `ACCIDENT_DATE`; `MINE_ID` |

**Columns that carry it.**
- LABOR__FED_MSHA_VIOLATIONS: `VIOLATION_ISSUE_DATE` (100.0% filled), `EVENT_NO`, `MINE_ID` (100.0% filled), `COAL_METAL_IND`, `MINE_TYPE`.
- LIBRARY_RAW.LANDING.FED_MSHA_VIOLATIONS: `EVENT_NO`, `INSPECTION_BEGIN_DT`, `INSPECTION_END_DT`, `MINE_ID`, `VIOLATION_ISSUE_DT`, `COAL_METAL_IND`. The mart drops the two inspection dates. Fill not yet measured on any of them.
- LABOR__FED_MSHA_ACCIDENTS: `ACCIDENT_DATE` (100.0% filled), `MINE_ID` (100.0% filled), `DEGREE_INJURY`, `IS_FATALITY`, `NO_INJURIES`, `COAL_METAL_IND`.

**The join, hop by hop.**
```
season, mart version: count distinct EVENT_NO by month of VIOLATION_ISSUE_DATE; count accidents by month of ACCIDENT_DATE
season, landing version: one row per distinct EVENT_NO with its INSPECTION_BEGIN_DT and INSPECTION_END_DT (strip quotes); count citing inspections under way in each month, and inspector-days as end minus begin
for the gap test: LABOR__FED_MSHA_ACCIDENTS.MINE_ID ➔ LABOR__FED_MSHA_VIOLATIONS.MINE_ID      measured: 13,338 shared mine ids
  days since that mine's last INSPECTION_END_DT, at each accident; and whether the accident fell inside an open inspection
```

**A hit means.** Inspection events dip in the same months every year, and accidents per active mine rise in those months; at the mine level, accidents come disproportionately late in the gap between inspection events.

**A miss means.** Both calendars are flat, or they rise and fall together with mining activity. Then the season is the work, not the oversight.

**Limits, said out loud.**
- Clean inspections are invisible, in the mart and in the landing copy alike. Both are citation files: an `EVENT_NO` appears only when an inspection wrote at least one citation. `INSPECTION_BEGIN_DT` and `INSPECTION_END_DT` fix when a citing inspection started and how long it ran, which the mart could only guess from citation dates. They do not add the inspections that found nothing, so "gap between inspections" is still "gap between citing inspections", and a well-run mine looks uninspected.
- The two inspection dates exist by name on an unprofiled table. Fill is not yet measured, and two columns found by name in this warehouse were empty (traps 2026-09-18). If they are empty the entry falls back to the mart version.
- Surface mines shut for winter in many states. A winter dip in both calendars is activity; split by `COAL_METAL_IND` and mine type before reading a season.
- Use 2000 onward; the accident table starts there. The final months of 2026 are partial in both.
- 13,708 mines have an accident row and 32,133 have a citation row. Most cited mines never report an accident; the gap test runs on the 13,338 shared mines.
- Every landing value is wrapped in literal double quotes (warehouse topo map). Strip before casting the inspection dates; an empty value is a pair of quotes, not a NULL. Mart state not yet measured. The landing copy holds 3,087,266 rows against the mart's 3,087,265.

**The picture.** Twelve-month cycle chart: month on the horizontal axis, index of the monthly average on the vertical, one line for inspection events and one for accidents, 2000 to 2025 pooled.

**First cheap check.** On LIBRARY_RAW.LANDING.FED_MSHA_VIOLATIONS, count rows where `INSPECTION_BEGIN_DT` and `INSPECTION_END_DT` are non-empty after stripping quotes. If filled, count distinct `EVENT_NO` by month of `INSPECTION_BEGIN_DT`: twelve numbers, and if they are flat there is no season.

---

### WN-144 · Injury rates cluster by industry and state

**The physical thing.** Work sites in the same industry and the same state reporting alike, higher or lower injury rates than the same industry elsewhere, beyond what employer size explains.

**Status.** never run. Verified when scored: 1,218 industry codes, 3 years, about 1.18M establishment-years (wonder extract WN-144; the three tables sum to 1,176,137 rows).

**Data grade.** B, because it is a single profiled table family with no join, but the window is three years, the fill of the industry and state columns is not yet measured, and the hours column needs trimming before any rate.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2023 | 394,234 | one establishment's yearly injury summary | 2023 | `NAICS_CODE` + `STATE` |
| LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2024 | 398,620 | same | 2024 | `NAICS_CODE` + `STATE` |
| LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2025 | 383,283 | same | 2025 | `NAICS_CODE` + `STATE` |

**Columns that carry it.**
- All three tables: `NAICS_CODE`, `NAICS_YEAR`, `STATE`, `SIZE`, `ANNUAL_AVERAGE_EMPLOYEES`, `TOTAL_HOURS_WORKED`, `TOTAL_INJURIES`, `TOTAL_DAFW_CASES`, `TOTAL_DJTR_CASES`, `ESTABLISHMENT_ID` (100.0% filled), `YEAR_FILING_FOR` (100.0% filled). Fill of `NAICS_CODE` and `STATE` not yet measured.

**The join, hop by hop.**
```
one table per year, no join; stack the three years
group by NAICS_CODE, STATE: injuries per hour, after fitting out SIZE
variance between industry-state cells against variance inside them
```

**A hit means.** Specific industry-and-state cells sit far from their industry's national rate in all three years. Something local, the state plan, the dominant employer, the reporting culture, moves the whole cell.

**A miss means.** Once industry and size are fitted, state adds nothing. Injury rates are an industry fact.

**Limits, said out loud.**
- Hours are unreliable: 1,065B hours against 138.8M employees, about 7,672 hours per employee (wonder extract WN-138). Keep rows between 800 and 3,000 hours per employee, 88% of rows (trap 2026-09-08).
- Multi-site filers repeat one parent number on many rows and report zero injuries 49 to 79% of the time against 6.7% for ordinary rows (trap 2026-09-08). A state with one big public filer looks safe for that reason alone.
- `NAICS_YEAR` runs from 0 to 180175 in the 2025 table. The industry code vintage is mixed and partly junk; map codes to one vintage or use the first 4 digits.
- Only sites above OSHA's filing thresholds are in the file. A low cell rate can mean the dangerous small shops are not required to file.
- The tables carry no flag for state-run OSHA programs, so a state effect cannot be split from a reporting-rule effect.

**The picture.** Heat grid: states across the horizontal axis, top industries down the vertical, one square per cell shaded by its distance from the industry's national rate.

**First cheap check.** Count distinct (`NAICS_CODE`, `STATE`) cells with 30 or more rows in the 2024 table after the hours trim.

---

### N1 · Employers caught with child-labor violations that hold federal contracts

**The physical thing.** An employer that a Wage and Hour investigator found working minors illegally, whose legal name and ZIP also appear as the recipient of a federal contract.

**Status.** never run. New on 2026-09-18. The final list marks it "fill-check the minor-count column first".

**Measured 2026-09-18.** `FLSA_CL_MINOR_CNT` is filled on all 367,890 rows with 113 distinct values. The column is real, not an empty constant. How many rows are above zero is not yet measured.

**Data grade.** C, because the column the whole question rests on, `FLSA_CL_MINOR_CNT`, was confirmed by name only with no measured fill, both tables are unprofiled, and the join is employer name plus ZIP with no shared id.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_RAW.LANDING.FED_DOL_WHD_ENFORCEMENT | 367,890 | one closed wage-and-hour case against one employer | not yet measured (date columns carry typo years 0200 and 3021) | `LEGAL_NAME` + `ZIP_CD` |
| LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 through LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2026 (20 tables) | 96,976,021 | one contract transaction | FY2007-FY2026 | `RECIPIENT_NAME` + `RECIPIENT_ZIP_4_CODE` |

**Columns that carry it.**
- FED_DOL_WHD_ENFORCEMENT: `CASE_ID`, `LEGAL_NAME`, `TRADE_NM`, `ZIP_CD`, `ST_CD`, `NAIC_CD`, `FLSA_CL_VIOLTN_CNT`, `FLSA_CL_MINOR_CNT`, `FLSA_CL_CMP_ASSD_AMT`, `FINDINGS_START_DATE`, `FINDINGS_END_DATE`. Fill not yet measured on any of them.
- Contract year tables: `RECIPIENT_NAME`, `RECIPIENT_UEI`, `RECIPIENT_PARENT_NAME`, `RECIPIENT_ZIP_4_CODE`, `FEDERAL_ACTION_OBLIGATION`, `ACTION_DATE`, `AWARDING_AGENCY_NAME`, `AWARD_ID_PIID`. Fill not yet measured.

**The join, hop by hop.**
```
FED_DOL_WHD_ENFORCEMENT where FLSA_CL_MINOR_CNT > 0
  .LEGAL_NAME (multi-word, upper, trimmed) + left(ZIP_CD,5)
  ➔ FED_USASPENDING_CONTRACTS_FY*.RECIPIENT_NAME + left(RECIPIENT_ZIP_4_CODE,5)      overlap not yet measured
keep contract actions with FEDERAL_ACTION_OBLIGATION > 0 and ACTION_DATE after FINDINGS_END_DATE
```

**A hit means.** A named list of employers with minors counted in a closed case and positive contract dollars obligated after the case findings ended.

**A miss means.** No matches, or matches only before the case. Either child-labor cases land on firms too small to contract, or the contract goes to a parent under another name and ZIP.

**Limits, said out loud.**
- The column is unproven. It exists by name; two flags found the same way in this warehouse were empty (traps 2026-09-18). If the first cheap check returns zero, this entry drops to D.
- Name plus ZIP misses the common case: the violation is at a franchise or a plant, the contract is with headquarters in another ZIP. Misses are expected and do not mean "clean".
- Multi-word names only. Single-word matches were 8% real in the 2026-09-03 test, multi-word 92%.
- 3,612 case rows have a blank `LEGAL_NAME` and 19 a blank `ZIP_CD`. Case dates carry typo years, 0200 and 3021, and 954 rows have no parseable start date; bound dates to 1990 to 2030 (trap 2026-09-10).
- `FEDERAL_ACTION_OBLIGATION` is signed; de-obligations are negative rows (trap 2026-09-05). Filter to positive before saying a firm "holds" a contract. A 2026-08-31 trap says USAspending landing columns can be case-sensitive lowercase; confirm on one year table.

**The picture.** Ranked bar: employers on the vertical axis, contract dollars obligated after the case on the horizontal, one bar per employer, labelled with minors counted.

**First cheap check.** Count rows in FED_DOL_WHD_ENFORCEMENT where `FLSA_CL_MINOR_CNT` > 0, and list its distinct values.

---

### N5 · Repeat wage violators that keep winning contracts

**The physical thing.** An employer the Wage and Hour Division has flagged as a repeat violator of the federal wage law, whose legal name and ZIP keep showing up as the recipient of new federal contract dollars.

**Status.** never run. New on 2026-09-18. The final list marks it "fill-check the repeat flag first".

**Measured 2026-09-18.** `FLSA_REPEAT_VIOLATOR` is filled on all 367,890 rows with four values: N/A on 346,361, R on 15,146, W on 4,381, RW on 2,002. So 21,529 cases carry a repeat or willful mark, 5.85% of the file.

**Data grade.** C, because the flag column, `FLSA_REPEAT_VIOLATOR`, was confirmed by name only with no measured fill or value list, both tables are unprofiled, and the join is employer name plus ZIP.

| table | rows | one row is | years | key used |
|---|---|---|---|---|
| LIBRARY_RAW.LANDING.FED_DOL_WHD_ENFORCEMENT | 367,890 | one closed wage-and-hour case against one employer | not yet measured (date columns carry typo years 0200 and 3021) | `LEGAL_NAME` + `ZIP_CD` |
| LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 through LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2026 (20 tables) | 96,976,021 | one contract transaction | FY2007-FY2026 | `RECIPIENT_NAME` + `RECIPIENT_ZIP_4_CODE` |

**Columns that carry it.**
- FED_DOL_WHD_ENFORCEMENT: `CASE_ID`, `LEGAL_NAME`, `TRADE_NM`, `ZIP_CD`, `ST_CD`, `FLSA_REPEAT_VIOLATOR`, `FLSA_VIOLTN_CNT`, `FLSA_BW_ATP_AMT`, `FLSA_CMP_ASSD_AMT`, `SCA_VIOLTN_CNT`, `DBRA_VIOLTN_CNT`, `FINDINGS_START_DATE`, `FINDINGS_END_DATE`. Fill not yet measured on any of them.
- Contract year tables: `RECIPIENT_NAME`, `RECIPIENT_UEI`, `RECIPIENT_ZIP_4_CODE`, `FEDERAL_ACTION_OBLIGATION`, `ACTION_DATE`, `ACTION_DATE_FISCAL_YEAR`, `AWARDING_AGENCY_NAME`, `AWARD_ID_PIID`. Fill not yet measured.

**The join, hop by hop.**
```
FED_DOL_WHD_ENFORCEMENT where FLSA_REPEAT_VIOLATOR is set
  .LEGAL_NAME (multi-word, upper, trimmed) + left(ZIP_CD,5)
  ➔ FED_USASPENDING_CONTRACTS_FY*.RECIPIENT_NAME + left(RECIPIENT_ZIP_4_CODE,5)      overlap not yet measured
per employer: distinct fiscal years with FEDERAL_ACTION_OBLIGATION > 0 after the flagged case's FINDINGS_END_DATE
second route, no flag needed: employers with 2 or more CASE_ID under one LEGAL_NAME + ZIP_CD
```

**A hit means.** Employers carrying the repeat flag, or two or more separate cases, that receive positive contract dollars in several fiscal years after the flagged case closed. The two wage laws written for contractors, counted in `SCA_VIOLTN_CNT` and `DBRA_VIOLTN_CNT`, make the sharpest rows.

**A miss means.** Flagged employers do not appear among contract recipients. Repeat violators would then be mostly small local employers outside federal contracting, or the name-and-ZIP join cannot see through to the contracting entity.

**Limits, said out loud.**
- The flag is unproven. Its fill and its values ('Y', 'R', blank, something else) are not yet measured; two flags in this warehouse exist and are empty (traps 2026-09-18). The second route, counting cases per employer, does not depend on it.
- "Winning" is not visible. The contract tables show dollars obligated, including add-ons to old awards. Use new `AWARD_ID_PIID` values first seen after the case to mean a new award.
- Name plus ZIP misses parents, subsidiaries and worksites in other ZIPs. Multi-word names only: 92% real against 8% for single words (test of 2026-09-03).
- 3,612 blank `LEGAL_NAME` rows, 19 blank `ZIP_CD`, date typos at years 0200 and 3021, 954 rows with no parseable start date (trap 2026-09-10).
- `FEDERAL_ACTION_OBLIGATION` is signed; filter to positive (trap 2026-09-05). The source review wrote this row against FY2008 to FY2026; twenty year tables, FY2007 to FY2026, are landed and listed here.

**The picture.** Ranked bar: employers on the vertical axis, contract dollars obligated after the flagged case on the horizontal, one bar per employer, labelled with number of wage cases.

**First cheap check.** List the distinct values of `FLSA_REPEAT_VIOLATOR` with a row count for each.

---


# The datasets

Every table named in this book, most-used first. Year families are shown as one row.

| table | rows | columns | years | key columns, fill | profiled | used by |
|---|---|---|---|---|---|---|
| LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FY2007 to 2026, 20 tables | 96,976,021 | 300 | 2007-2026 | RECIPIENT_UEI, RECIPIENT_PARENT_UEI, PRIME_AWARD_TRANSACTION_RECIPIENT_COUNTY_FIPS_CODE, PRIME_AWARD_TRANSACTION_RECIPIENT_STATE_FIPS_CODE | no | N1, N5, W10, W103, W115, W51, W53, W55, W65, W7, W70, W72, W80, W90, W92, W97, W98 |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME | 14,700 | 97 | not yet measured | CMS_CERTIFICATION_NUMBER_CCN 100.0%, COUNTY_FIPS 100.0%, PROVIDER_SSA_COUNTY_CODE 100.0%, ZIP_CODE 100.0% | yes | H-094, H-104, H-105, H-106, H-107, H-110, N3, W113, W15, W32, W33, W34, W78, WN-147, WN-149, WN-154 |
| LIBRARY_MARTS.CORE.XWALK_ZCTA_COUNTY | 46,960 | 7 | not yet measured | COUNTY_FIPS 100.0%, STATE_FIPS 100.0% | yes | W10, W103, W123, W29, W34, W40, W47, W53, W6, W75, W8 |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_INDIV_CONTRIBUTIONS | 283,771,819 | 16 | 0031-9206 on TRANSACTION_DATE | CMTE_ID 100.0%, ZIP_CODE 100.0% | yes | M-007, M-015, M-056, W53, W69, W80, W85, W97, WN-152 |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES | 418,479 | 23 | 2017-2026 on SURVEY_DATE | CMS_CERTIFICATION_NUMBER_CCN 100.0%, ZIP_CODE 100.0% | yes | H-094, H-104, H-106, H-110, H-111, N3, WN-147, WN-149, WN-150 |
| LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS | 3,087,265 | 27 | 1994-2026 on VIOLATION_OCCUR_DATE | MINE_ID 100.0%, CONTROLLER_ID 93.24% | yes | P-146, P-147, P-148, P-149, W104, W120, W62, W79, WN-136 |
| LIBRARY_MARTS.CONSUMER_PROTECTION.CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS | 17,168,287 | 24 | 2011-2026 on DATE_RECEIVED | ZIP_CODE 99.99%, COMPANY 100.0%, DATE_SENT_TO_COMPANY 99.32%, DAYS_RECEIVED_TO_COMPANY 99.32% | yes | M-239, M-240, M-245, W121, W60, W86, WN-143 |
| LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_MINES | 91,906 | 23 | 1925-2026 on CURRENT_STATUS_DT | MINE_ID 100.0%, CURRENT_CONTROLLER_ID 98.88%, FIPS_CNTY_CD 100.0%, FIPS_CNTY_NM 100.0% | yes | P-146, P-147, P-148, W104, W12, W79, WN-136 |
| LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP | 295,083 | 43 | not yet measured | ENROLLMENT_ID, ASSOCIATE_ID, ASSOCIATE_ID_OWNER, ZIP_CODE_OWNER | no | H-107, N3, W113, W28, W45, W97, WN-154 |
| LIBRARY_RAW.LANDING.FED_USASPENDING_ASSISTANCE_FY2007 to 2026, 20 tables | 128,155,142 | 115 | 2007-2026 | RECIPIENT_UEI, RECIPIENT_PARENT_UEI, PRIME_AWARD_TRANSACTION_RECIPIENT_COUNTY_FIPS_CODE, PRIME_AWARD_TRANSACTION_RECIPIENT_STATE_FIPS_CODE | no | N6, W10, W122, W13, W53, W61, W68 |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS | 2,822,977 | 85 | 1994-2025 on BRANCH_YEAR_KEY | FDIC_CERT 100.0%, HOLDING_COMPANY_RSSD 100.0%, BRANCH_ZIP 100.0%, BRANCH_STATE_FIPS 100.0% | yes | W10, W56, W58, W6, W60, W9 |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS | 14,425 | 23 | 1800-2024 on INCORPORATION_DATE | ENROLLMENT_ID 100.0%, NPI 100.0%, MULTIPLE_NPI_FLAG 100.0%, CCN 100.0% | yes | H-107, N3, W113, W28, W45, W97 |
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT | 15,432,737 | 38 | 1900-2026 on COMPL_PER_BEGIN_DATE | PWSID 100.0% | yes | W11, W16, W18, W2, W30 |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_CAND_CMTE_LINKAGE | 30,536 | 7 | not yet measured | CAND_ID 100.0%, CMTE_ID 100.0% | yes | M-007, M-015, M-056, W80, W85 |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_DRUG_POISONING_COUNTY | 53,387 | 8 | 1999-2015 on YEAR | FIPS 100.0%, FIPS_STATE 100.0% | yes | W12, W26, W46, W70, W8 |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES | 16,180 | 14 | 2023-2026 on PENALTY_DATE | CMS_CERTIFICATION_NUMBER_CCN 100.0%, ZIP_CODE 100.0% | yes | H-104, H-105, H-107, N3, W78 |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_NURSINGHOME411 | 14,713 | 71 | 1967-2025 on DATE_FIRST_APPROVED_TO_PROVIDE_MEDICARE_AND_MEDICAID_SERVICES | CMS_CERTIFICATION_NUMBER_CCN 100.0% | yes | H-094, H-105, W28, W45, WN-149 |
| LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_HISTORIC | 44,992,667 | 82 | 2015-2017 on AS_OF_YEAR | RESPONDENT_ID 100.0%, STATE_CODE 98.4%, COUNTY_CODE 98.17% | yes | W1, W5, W56, W59, W71 |
| LIBRARY_RAW.LANDING.FED_CFPB_HMDA_LAR_2018 to 2024, 7 tables | 124,632,830 | 102 | 2018-2024 | LEI, STATE_CODE, COUNTY_CODE | no | W1, W5, W56, W59, W71 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_DY2013 | 956,251 | 59 | not yet measured | NPI, RNDRNG_PRVDR_STATE_FIPS, RNDRNG_PRVDR_ZIP5 | no | W23, W29, W37, W6, W8 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_DY2014 | 986,657 | 59 | not yet measured | NPI, RNDRNG_PRVDR_STATE_FIPS, RNDRNG_PRVDR_ZIP5 | no | W23, W29, W37, W6, W8 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_DY2015 | 1,019,377 | 59 | not yet measured | NPI, RNDRNG_PRVDR_STATE_FIPS, RNDRNG_PRVDR_ZIP5 | no | W23, W29, W37, W6, W8 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_DY2016 | 1,053,958 | 59 | not yet measured | NPI, RNDRNG_PRVDR_STATE_FIPS, RNDRNG_PRVDR_ZIP5 | no | W23, W29, W37, W6, W8 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_DY2017 | 1,088,687 | 84 | not yet measured | NPI, RNDRNG_PRVDR_STATE_FIPS, RNDRNG_PRVDR_ZIP5 | no | W23, W29, W37, W6, W8 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_DY2018 | 1,121,462 | 84 | not yet measured | NPI, RNDRNG_PRVDR_STATE_FIPS, RNDRNG_PRVDR_ZIP5 | no | W23, W29, W37, W6, W8 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_DY2019 | 1,155,870 | 84 | not yet measured | NPI, RNDRNG_PRVDR_STATE_FIPS, RNDRNG_PRVDR_ZIP5 | no | W23, W29, W37, W6, W8 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_DY2020 | 1,161,542 | 84 | not yet measured | NPI, RNDRNG_PRVDR_STATE_FIPS, RNDRNG_PRVDR_ZIP5 | no | W23, W29, W37, W6, W8 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_DY2021 | 1,198,754 | 84 | not yet measured | NPI, RNDRNG_PRVDR_STATE_FIPS, RNDRNG_PRVDR_ZIP5 | no | W23, W29, W37, W6, W8 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_DY2022 | 1,230,293 | 84 | not yet measured | NPI, RNDRNG_PRVDR_STATE_FIPS, RNDRNG_PRVDR_ZIP5 | no | W23, W29, W37, W6, W8 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_DY2023 | 1,259,343 | 84 | not yet measured | NPI, RNDRNG_PRVDR_STATE_FIPS, RNDRNG_PRVDR_ZIP5 | no | W23, W29, W37, W6, W8 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_DY2024 | 1,296,739 | 84 | not yet measured | NPI, RNDRNG_PRVDR_STATE_FIPS, RNDRNG_PRVDR_ZIP5 | no | W23, W29, W37, W6, W8 |
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS | 578,198 | 12 | 1995-2026 on LAST_REPORTED_DATE | PWSID 100.0%, ZIP_CODE_SERVED 1.24%, COUNTY_FIPS | yes | W11, W16, W2, W30 |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES | 9,606,683 | 333 | 2005-2026 on PROVIDER_ENUMERATION_DATE | NPI 100.0%, REPLACEMENT_NPI 100.0%, EMPLOYER_IDENTIFICATION_NUMBER_EIN 0.0%, NPI_DEACTIVATION_REASON_CODE 100.0% | yes | W117, W7, W74, W97 |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS | 15,385,047 | 22 | 2024-2024 on PROGRAM_YEAR | NPI 100.0%, RECIPIENT_ZIP_CODE 100.0%, CCN 100.0% | yes | W48, W49, W74, W75 |
| LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_ACCIDENTS | 273,623 | 26 | 2000-2026 on ACCIDENT_DATE | MINE_ID 100.0%, CONTROLLER_ID 99.74%, FIPS_STATE_CD 100.0% | yes | P-146, P-148, P-149, W104 |
| LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2023 to 2025, 3 tables | 1,176,137 | 32 | 2023-2025 | ESTABLISHMENT_ID 100.0%, EIN 89.62%, COMPANY_NAME 95.09%, ZIP_CODE 100.0% | yes | P-159, P-160, W125, WN-144 |
| LIBRARY_RAW.LANDING.FED_CENSUS_COUNTY_2020 | 3,235 | 10 | not yet measured | none flagged | no | W16, W32, W58, W90 |
| LIBRARY_RAW.LANDING.FED_CMS_NPPES_DEACTIVATED | 351,912 | 5 | not yet measured | NPI | no | W29, W37, W6, W8 |
| LIBRARY_RAW.LANDING.FED_FEMA_DISASTER_DECLARATIONS | 70,402 | 32 | not yet measured | none flagged | no | W1, W122, W55, W67 |
| LIBRARY_RAW.LANDING.FED_MSHA_VIOLATIONS | 3,087,266 | 64 | not yet measured | CONTROLLER_ID, MINE_ID | no | P-149, W104, W120, W79 |
| LIBRARY_MARTS.CORE.XWALK_HOSPITAL_CCN_EIN | 4,003 | 11 | not yet measured | CCN, EIN, CCN_NAME, CCN_ZIP5 | no | W123, W36, W69 |
| LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_IRS_EO_BMF | 1,983,563 | 32 | 1900-2026 on RULING_DATE | EIN 100.0%, ZIP 100.0% | yes | W125, W36, W67 |
| LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC | 15,804,611 | 27 | 1-9998 on DOB_YEAR | COMPANY_NUMBER 100.0% | yes | W113, W115, W117 |
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_EGRID_PLANT_2022 | 11,974 | 141 | 2022-2022 on DATA_YEAR | PLANT_FIPS_STATE_CODE 100.0%, PLANT_FIPS_COUNTY_CODE 99.71% | yes | W124, W13, W23 |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS_SOI | 179,796 | 150 | 2016-2016 on TAX_YEAR | STATE_FIPS 100.0%, ZIP_CODE 100.0% | yes | W10, W111, W53 |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY | 31,403,215 | 16 | not yet measured | CCN 100.0%, ZIP_CODE 100.0%, FIPS_COUNTY_CODE 100.0% | yes | W28, W32, W35 |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_2022 | 13,306,564 | 22 | 2022-2022 on PROGRAM_YEAR | NPI 100.0%, RECIPIENT_ZIP_CODE 100.0%, CCN 100.0% | yes | W48, W74, W75 |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_2023 | 14,700,786 | 22 | 2023-2023 on PROGRAM_YEAR | NPI 100.0%, RECIPIENT_ZIP_CODE 100.0%, CCN 100.0% | yes | W48, W74, W75 |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS | 1,416,883 | 84 | not yet measured | NPI 100.0%, PRSCRBR_STATE_FIPS 100.0%, PRSCRBR_ZIP5 100.0% | yes | W34, W45, W47 |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER | 44,429 | 473 | 1973-2026 on CHOW_DT | CCN 100.0%, ZIP_CD 100.0%, FIPS_STATE_CD 100.0%, FIPS_CNTY_CD 99.29% | yes | W30, W37, W9 |
| LIBRARY_MARTS.HEALTH.HEALTH__HOSPITAL_OFFICER_PAY | 526,374 | 32 | 2016-2025 on TAX_YEAR | EIN 100.0%, SOURCE_ZIP 100.0% | yes | W36, W66, W99 |
| LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS | 26,250,920 | 103 | 0003-2026 on APPLIED_DATE | DISASTER_NUMBER 100.0%, DAMAGED_ZIP_CODE 100.0%, FIPS 74.21%, CENSUS_GEOID 73.75% | yes | W1, W122, W67 |
| LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_ROLLCALLS | 3,364 | 11 | 2023-2026 on VOTE_DATE | none flagged | yes | M-056, W52, W84 |
| LIBRARY_RAW.LANDING.FED_DOL_WHD_ENFORCEMENT | 367,890 | 113 | not yet measured | CASE_ID, ZIP_CD | no | N1, N5, W102 |
| LIBRARY_RAW.LANDING.FED_EOIR_PROCEEDING | 16,817,265 | 41 | not yet measured | IDNCASE, IJ_CODE, PREV_IJ_CODE | no | N2, W76, W91 |
| LIBRARY_RAW.LANDING.FED_SENATE_LDA_FILINGS | 1,976,696 | 28 | not yet measured | none flagged | no | W68, W82, W87 |
| LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_BLS_QCEW | 3,619,437 | 16 | 2022-2022 on YEAR | AREA_FIPS 100.0%, STATE_FIPS 100.0% | yes | W123, W6 |
| LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FDIC_FAILED_BANKS | 3,584 | 25 | 1970-2026 on FAIL_DATE | FDIC_CERT 100.0%, FIPS 100.0% | yes | W58, W60 |
| LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_990 | 200 | 18 | 2023-2025 on TAX_YEAR | EIN 100.0%, ZIP_CODE 100.0% | yes | W66, W67 |
| LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_990_EFILE_INDEX | 5,544,626 | 10 | 2017-2026 on SUB_DATE | EIN 100.0% | yes | W36, W67 |
| LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_BMF | 1,974,830 | 25 | not yet measured | EIN 100.0%, ZIP 100.0% | yes | W66, W69 |
| LIBRARY_MARTS.EDUCATION.EDUCATION__FED_SENATE_LDA_FILINGS | 819,649 | 26 | 1999-2021 on FILING_YEAR | none flagged | yes | W68, W82 |
| LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_4_OWNER | 5,495 | 17 | not yet measured | PLANT_CODE 100.0%, OWNER_ZIP 98.34% | yes | W124, W85 |
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__EPA_PENALTY_GAP | 93,808 | 31 | 1978-2026 on DATE_LAST_INSPECTION | FRS_ID 100.0%, FIPS_CODE 100.0% | yes | P-081, W62 |
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS | 434,040 | 51 | 1900-2026 on PWS_DEACTIVATION_DATE | PWSID 100.0%, ZIP_CODE 94.44%, STATE_CODE 96.67% | yes | W11, W18 |
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_NOAA_STORM_EVENTS | 1,780,730 | 51 | 1996-2025 on YEAR | STATE_FIPS 100.0%, CZ_FIPS 100.0%, TOR_OTHER_CZ_FIPS 100.0% | yes | W5, W55 |
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK | 5,300,149 | 11 | not yet measured | EPA_REGISTRY_ID 100.0%, MATCHED_LEI 5.28%, ULTIMATE_PARENT_LEI 0.71%, PARENT_CIK 2.25% | yes | W51, W62 |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_BANK_DATA | 27,836 | 48 | 1975-2026 on DATEUPDT | CERT 100.0%, ZIP 100.0%, FIPS 100.0%, LEI 8.09% | yes | W56, W58 |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_CANDIDATES | 27,095 | 15 | not yet measured | CAND_ID 100.0%, CAND_ZIP 100.0% | yes | M-015, W80 |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES | 60,031 | 15 | not yet measured | CMTE_ID 100.0%, CMTE_ZIP 100.0%, CAND_ID 100.0% | yes | W7, W95 |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES_DIM | view | 14 | not yet measured | CMTE_ID, CAND_ID | no | W69, W95 |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_HOLDINGS | view | 18 | not yet measured | CUSIP | no | W51, W62 |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_13F_SUBMISSIONS | 336,124 | 6 | not yet measured | CIK 100.0% | yes | W51, W62 |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY | 132,000 | 12 | not yet measured | GEOID 100.0%, ST_GEOID 100.0% | yes | W12, W26 |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_AFFILIATION | 2,260,193 | 9 | not yet measured | NPI 100.0%, CCN 100.0% | yes | W37, W45 |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS | 80,077 | 126 | 2011-2024 on FISCAL_YEAR_END_DATE | PROVIDER_CCN 100.0%, STATE_CODE 100.0%, ZIP_CODE 100.0%, CCN_FACILITY_TYPE 100.0% | yes | W123, W36 |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_OWNERS | 101,188 | 45 | 1800-2026 on ASSOCIATION_DATE_OWNER | ENROLLMENT_ID 100.0%, ASSOCIATE_ID 100.0%, CCN 98.12%, NPI 98.12% | yes | W39, W97 |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_DEA_ARCOS | 178,598,026 | 35 | 2006-2012 on TRANSACTION_DATE | REPORTER_ZIP 100.0%, REPORTER_COUNTY_FIPS, BUYER_ZIP 100.0%, BUYER_COUNTY_FIPS | yes | W26, W46 |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DEVICE_ENFORCEMENT | 39,635 | 29 | 1930-2026 on RECALL_INITIATION_DATE | PRODUCT_CODE 0.0%, K_NUMBER_LIST 0.0% | yes | W107, W50 |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE | 83,747 | 22 | 1977-2026 on EXCLUSION_DATE | NPI 10.55%, ZIP 100.0%, NPI_IS_REAL 100.0% | yes | W49, W73 |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_HPSA_PRIMARY_CARE | 79,158 | 69 | 1970-2026 on DESIGNATION_DATE | PRIMARY_STATE_FIPS_CODE 100.0%, STATE_FIPS_CODE 100.0%, COMMON_STATE_FIPS_CODE 100.0%, COMMON_STATE_COUNTY_FIPS_CODE 100.0% | yes | W8, W96 |
| LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_ARID2017_LEI_XREF | 5,399 | 8 | not yet measured | LEI_2018 100.0%, LEI_2019 93.91%, LEI_2020 76.5% | yes | W5, W71 |
| LIBRARY_MARTS.HOUSING.HOUSING__FED_MAPPING_INEQUALITY | 1,155 | 18 | not yet measured | FIPS 100.0% | yes | W2, W96 |
| LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_FACILITY_CODES | 1,490 | 15 | not yet measured | ZIP 100.0% | yes | W80, W90 |
| LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_DOCKETS | view | 54 | not yet measured | DATE_CERT_GRANTED, DATE_CERT_DENIED, PACER_CASE_ID, PARENT_DOCKET_ID | no | W77, W88 |
| LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FDIC_ENFORCEMENT_ORDERS | 10,838 | 35 | 1975-2026 on ORDER_DATE | CERT_NUMBER 97.86%, CERT_ATTACHED 100.0%, BANK_HOLDING_COMPANY 74.09% | yes | W56, W86 |
| LIBRARY_MARTS.POLITICS.POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP | 26,970 | 11 | not yet measured | BIOGUIDE 100.0% | yes | W69, W85 |
| LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_CROSSWALK | 12,794 | 30 | not yet measured | BIOGUIDE 99.9%, ICPSR 96.12% | yes | M-056, W52 |
| LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_FEC_ID | 1,715 | 7 | not yet measured | BIOGUIDE 99.94% | yes | W69, W85 |
| LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_VOTES | 945,523 | 7 | not yet measured | ICPSR 100.0% | yes | M-056, W52 |
| LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS | 168,328 | 22 | 1908-2099 on ACTIVATION_DATE | UEI 28.33%, NPI 11.43%, ZIP 81.9% | yes | W72, W73 |
| LIBRARY_MARTS.REFERENCE.REF__DIM_STATE | 56 | 5 | not yet measured | STATE_FIPS 100.0% | yes | W12, W16 |
| LIBRARY_MARTS.SCIENCE_RESEARCH.SCIENCE_RESEARCH__FED_NIH_REPORTER | 2,122,611 | 48 | 2000-2026 on FISCAL_YEAR | ORG_UEI 93.41%, ORG_ZIP 0.0%, ORG_FIPS 0.0% | yes | W74, W75 |
| LIBRARY_RAW.LANDING.FED_CDC_INJURY_VIOLENCE_COUNTY | 132,000 | 15 | not yet measured | GEOID, ST_GEOID | no | W26, W46 |
| LIBRARY_RAW.LANDING.FED_CENSUS_ZCTA_COUNTY_2020 | 47,863 | 21 | not yet measured | GEOID_ZCTA5_20, GEOID_COUNTY_20 | no | W34, W47 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DRUG_DY2021 | 25,231,862 | 25 | not yet measured | NPI, PRSCRBR_STATE_FIPS | no | W44, W48 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DRUG_DY2022 | 25,869,521 | 25 | not yet measured | NPI, PRSCRBR_STATE_FIPS | no | W44, W48 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DRUG_DY2023 | 26,794,878 | 25 | not yet measured | NPI, PRSCRBR_STATE_FIPS | no | W44, W48 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DRUG_DY2024 | 28,023,892 | 25 | not yet measured | NPI, PRSCRBR_STATE_FIPS | no | W44, W48 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DY2013 | 1,049,299 | 87 | not yet measured | NPI, PRSCRBR_STATE_FIPS, PRSCRBR_ZIP5 | no | W44, W47 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DY2014 | 1,072,978 | 87 | not yet measured | NPI, PRSCRBR_STATE_FIPS, PRSCRBR_ZIP5 | no | W44, W47 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DY2015 | 1,102,253 | 87 | not yet measured | NPI, PRSCRBR_STATE_FIPS, PRSCRBR_ZIP5 | no | W44, W47 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DY2016 | 1,131,550 | 87 | not yet measured | NPI, PRSCRBR_STATE_FIPS, PRSCRBR_ZIP5 | no | W44, W47 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DY2017 | 1,162,898 | 87 | not yet measured | NPI, PRSCRBR_STATE_FIPS, PRSCRBR_ZIP5 | no | W44, W47 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DY2018 | 1,204,935 | 87 | not yet measured | NPI, PRSCRBR_STATE_FIPS, PRSCRBR_ZIP5 | no | W44, W47 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DY2019 | 1,240,595 | 87 | not yet measured | NPI, PRSCRBR_STATE_FIPS, PRSCRBR_ZIP5 | no | W44, W47 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DY2020 | 1,255,175 | 87 | not yet measured | NPI, PRSCRBR_STATE_FIPS, PRSCRBR_ZIP5 | no | W44, W47 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DY2021 | 1,287,454 | 87 | not yet measured | NPI, PRSCRBR_STATE_FIPS, PRSCRBR_ZIP5 | no | W44, W47 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DY2022 | 1,332,309 | 87 | not yet measured | NPI, PRSCRBR_STATE_FIPS, PRSCRBR_ZIP5 | no | W44, W47 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DY2023 | 1,380,665 | 87 | not yet measured | NPI, PRSCRBR_STATE_FIPS, PRSCRBR_ZIP5 | no | W44, W47 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DY2024 | 1,416,883 | 87 | not yet measured | NPI, PRSCRBR_STATE_FIPS, PRSCRBR_ZIP5 | no | W44, W47 |
| LIBRARY_RAW.LANDING.FED_DOL_FORM5500_FULL | 4,299,671 | 144 | not yet measured | SPONS_DFE_MAIL_US_ZIP, SPONS_DFE_LOC_US_ZIP, SPONS_DFE_EIN, ADMIN_US_ZIP | no | W125, W63 |
| LIBRARY_RAW.LANDING.FED_EOIR_JUDGE | 1,785 | 21 | not yet measured | JUDGE_ZIP_1, JUDGE_ZIP_2 | no | W76, W91 |
| LIBRARY_RAW.LANDING.FED_EPA_EGRID_PLANT_2019 to 2023, 4 tables | 48,538 | 143 | 2019-2023 | ORISPL | no | W124, W13 |
| LIBRARY_RAW.LANDING.FED_FDA_DEVICE_ENFORCEMENT | 20 | 4 | not yet measured | none flagged | no | W107, W50 |
| LIBRARY_RAW.LANDING.FED_MAPPING_INEQUALITY | 10,154 | 15 | not yet measured | FIPS | no | W2, W96 |
| LIBRARY_RAW.LANDING.FED_SAM_ENTITY_PUBLIC | 895,429 | 146 | not yet measured | UEI_SAM, UEI_DUNS, PHYSICAL_ADDRESS_ZIP, MAILING_ADDRESS_ZIP | no | W72, W75 |
| LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_COMPLAINTS | 2,227,941 | 29 | 1949-9999 on MODEL_YEAR | none flagged | yes | W111 |
| LIBRARY_MARTS.CONSUMER_SAFETY.CONSUMER_SAFETY__FED_NHTSA_RECALLS | 241,861 | 20 | 1965-9999 on MODEL_YEAR | none flagged | yes | W111 |
| LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_ENTITIES | 814,344 | 23 | 0199-2812 on INCORPORATION_DATE | COMPANY_TYPE 17.04% | yes | W98 |
| LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_OFFICERS | 771,315 | 9 | not yet measured | none flagged | yes | W98 |
| LIBRARY_MARTS.CORPORATE_REGISTRY.CORPORATE_REGISTRY__INTL_UK_COMPANIES_HOUSE | 5,734,780 | 19 | 1327-2026 on INCORPORATION_DATE | COMPANY_NUMBER 100.0%, COMPANY_NAME 100.0%, COMPANY_CATEGORY 100.0%, COMPANY_STATUS 100.0% | yes | W117 |
| LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_DOL_FORM5500 | 33,484 | 152 | 2026-2026 on DATE_RECEIVED | EIN 100.0%, SPONSOR_DFE_EIN 100.0%, PREPARER_EIN 100.0%, SPONS_DFE_MAIL_US_ZIP 100.0% | yes | W63 |
| LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_FAC_SINGLE_AUDIT | 411,638 | 28 | 2016-2026 on AUDIT_YEAR | AUDITEE_UEI 100.0%, AUDITEE_EIN 100.0%, AUDITEE_ZIP 100.0%, AUDITOR_EIN 100.0% | yes | W61 |
| LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_LOANS | 2,174,502 | 30 | 1990-2026 on APPROVAL_DATE | BORROWER_ZIP 100.0% | yes | W58 |
| LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS | 968,524 | 53 | not yet measured | none flagged | yes | W73 |
| LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_TOPTIER_AGENCIES | 111 | 13 | 2026-2026 on ACTIVE_FY | none flagged | yes | W92 |
| LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_GLEIF_RELATIONSHIPS | 485,285 | 54 | 1832-2070 on RELATIONSHIP_PERIOD_1_STARTDATE | none flagged | yes | W65 |
| LIBRARY_MARTS.ENERGY.ENERGY__FED_EIA860_2_PLANT | 16,132 | 45 | not yet measured | PLANT_CODE 100.0%, ZIP 100.0% | yes | W85 |
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO | 3,135,554 | 44 | 1016-2026 on DATE_LAST_INSPECTION | FRS_ID 100.0%, ZIP 100.0%, FIPS_CODE 100.0% | yes | W120 |
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_PROGRAM_LINKS | 4,406,498 | 13 | not yet measured | REGISTRY_ID 100.0%, FIPS_CODE 66.24%, STATE_CODE 90.08% | yes | W62 |
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS | 106,009 | 10 | 1972-2026 on SETTLEMENT_ENTERED_DATE | none flagged | yes | W62 |
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023 | 78,647 | 122 | 2023-2023 on C_1_YEAR | C_3_FRS_ID 99.82%, C_9_ZIP 100.0% | yes | W40 |
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_FRACFOCUS_DISCLOSURE_LIST | 248,835 | 20 | not yet measured | none flagged | yes | W16 |
| LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_NID_DAMS | 92,766 | 47 | 0-2026 on YEAR_COMPLETED | none flagged | yes | W15 |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_BULK_COMMITTEES | 20,007 | 16 | not yet measured | FEC_CMTE_ID 100.0%, CMTE_ZIP 100.0%, FEC_CAND_ID 100.0% | yes | W7 |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS527_SCHEDULE_B_EXPENDITURES | 8,191,177 | 19 | 2001-2026 on EXPENDITURE_DATE | EIN 100.0%, RECIPIENT_ZIP 100.0%, RECIPIENT_ZIP_EXT 100.0% | yes | W83 |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE | 10,398 | 8 | not yet measured | CIK 100.0%, TICKER 100.0%, CIK_TICKER 100.0%, COMPANY_NAME 100.0% | yes | W77 |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_REPORTINGOWNER | 1,934,673 | 10 | not yet measured | OWNER_CIK 100.0%, ZIP_CODE 100.0% | yes | W99 |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_SUBMISSION | 1,772,088 | 12 | 2016-2025 on FILING_DATE | ISSUER_CIK 100.0%, ISSUER_TICKER 100.0% | yes | W99 |
| LIBRARY_MARTS.FINANCE.FINANCE__FED_SENATE_EFD_PTR | 6,855 | 19 | 2021-2026 on FILING_YEAR | TICKER 100.0% | yes | W52 |
| LIBRARY_MARTS.FOREIGN_INFLUENCE.FOREIGN_INFLUENCE__FED_FARA_BULK | 48,103 | 33 | 1942-2026 on DATE | COMPANY_ID 100.0%, ZIP 100.0% | yes | W84 |
| LIBRARY_MARTS.GOVERNANCE.GOVERNANCE__FED_REVOLVINGDOOR_PROJECT | 405 | 44 | not yet measured | none flagged | yes | W89 |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_DIALYSIS | 7,557 | 142 | 1968-2026 on CERTIFICATION_DATE | CCN 100.0%, ZIP_CODE 100.0% | yes | W29 |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPICE | 6,852 | 12 | 1983-2025 on CERTIFICATION_DATE | CCN 100.0%, ZIP_CODE 100.0% | yes | W32 |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS | 9,175 | 39 | 1800-2024 on INCORPORATION_DATE | ENROLLMENT_ID 100.0%, NPI 100.0%, MULTIPLE_NPI_FLAG 100.0%, CCN 100.0% | yes | W39 |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DIALYSIS_FACILITIES | 12,456,456 | 14 | 2021-2024 on YEAR_COL | CCN 100.0%, NPI 99.64% | yes | W29 |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_INPATIENT_HOSPITALS_BY_PROVIDER_AND_SERVICE | 145,879 | 15 | not yet measured | RNDRNG_PRVDR_CCN 100.0%, RNDRNG_PRVDR_STATE_FIPS 100.0%, RNDRNG_PRVDR_ZIP5 100.0% | yes | W40 |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_FIRE_DEFICIENCIES | 200,030 | 24 | 2016-2026 on SURVEY_DATE | CMS_CERTIFICATION_NUMBER_CCN 100.0%, ZIP_CODE 100.0% | yes | W33 |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PARTD_PRESCRIBERS | 25,869,521 | 20 | not yet measured | NPI 100.0%, PRESCRIBER_STATE_FIPS 100.0% | yes | W44 |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DEVICE_510K | 175,686 | 25 | 1976-2026 on DATE_RECEIVED | K_NUMBER 100.0%, PRODUCT_CODE 100.0%, ZIP_CODE 100.0% | yes | W107 |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DEVICE_PMA | 56,853 | 25 | 1900-2026 on DATE_RECEIVED | PRODUCT_CODE 100.0%, ZIP 100.0%, ZIP_EXT 100.0% | yes | W107 |
| LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_GUDID | 5,083,948 | 19 | 2013-2026 on PUBLISH_DATE | COMPANY_NAME 100.0%, PRIMARY_PRODUCT_CODE 99.38% | yes | W50 |
| LIBRARY_MARTS.HOUSING.HOUSING__FED_HUD_MF_SECTION8_CONTRACTS | 24,309 | 35 | 1977-2027 on TRACS_EFFECTIVE_DATE | none flagged | yes | W3 |
| LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_DOL_OFLC | 664,616 | 260 | 2018-2019 on DECISION_DATE | ORIGINAL_CERT_DATE 7.06% | yes | W102 |
| LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETAINERS | 609,769 | 66 | 2022-2026 on DETAINER_PREPARE_DATE | none flagged | yes | W90 |
| LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_FACILITY_LIST | 163 | 7 | not yet measured | none flagged | yes | W80 |
| LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_STINTS | 2,571,975 | 70 | 2004-2026 on STAY_BOOK_IN_AT | none flagged | yes | W80 |
| LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_FINANCIAL_DISCLOSURES | 66,287 | 16 | 0009-2023 on DATE_CREATED | PERSON_ID 43.8% | yes | W77 |
| LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_FJC_IDB_CL_LINKED | 10,323,280 | 39 | 2017-2022 on DATE_CREATED | none flagged | yes | W77 |
| LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_INVESTMENTS | 1,901,599 | 18 | 2020-2023 on DATE_CREATED | none flagged | yes | W77 |
| LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_OPINION_CLUSTERS | 10,070,727 | 36 | 2014-2026 on DATE_CREATED | DOCKET_ID 100.0% | yes | W88 |
| LIBRARY_MARTS.JUSTICE.JUSTICE__FED_COURTLISTENER_POSITIONS | 51,290 | 38 | 2016-2025 on DATE_CREATED | PERSON_ID 100.0% | yes | W88 |
| LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FJC_IDB_CIVIL | 10,857,396 | 49 | 1988-2099 on TAPE_YEAR | none flagged | yes | W78 |
| LIBRARY_MARTS.LABOR.LABOR__FED_DOL_OLMS | 617,710 | 61 | 2000-2026 on REPORT_YEAR_RAW | ZIP 99.97% | yes | W103 |
| LIBRARY_MARTS.LABOR.LABOR__FED_PBGC_TRUSTEED_PLANS | 5,176 | 12 | 1972-2026 on DATE_OF_PLAN_TERMINATION | EIN 100.0% | yes | W63 |
| LIBRARY_MARTS.POLITICS.POLITICS__BILLS | 36,465 | 18 | 2023-2026 on INTRODUCED_DATE | SPONSOR_BIOGUIDE 100.0% | yes | W82 |
| LIBRARY_MARTS.POLITICS.POLITICS__FED_EAC_EAVS | 6,460 | 428 | not yet measured | none flagged | yes | W83 |
| LIBRARY_MARTS.POLITICS.POLITICS__FED_SENATE_LDA_LOBBYIST_POSITIONS | 140,463 | 19 | 2011-2011 on FILING_YEAR | none flagged | yes | W89 |
| LIBRARY_MARTS.POLITICS.POLITICS__IRS527_8871_ORGS | 77,591 | 20 | 1808-2026 on ESTABLISHED_DATE | EIN 100.0%, MAILING_ZIP 100.0% | yes | W95 |
| LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_SPINE | 12,794 | 19 | not yet measured | BIOGUIDE 99.9%, ICPSR 96.12% | yes | W82 |
| LIBRARY_MARTS.REFERENCE.REFERENCE__CENSUS_CB_COUNTY | 3,235 | 17 | not yet measured | GEOID 100.0% | yes | W59 |
| LIBRARY_MARTS.REFERENCE.REF__DIM_GEOGRAPHY | 6,988 | 10 | not yet measured | FIPS_CODE 100.0%, STATE_FIPS 100.0%, COUNTY_FIPS_SUFFIX 100.0% | yes | W90 |
| LIBRARY_MARTS.REGULATORY.REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS | 94,731 | 38 | 2023-2026 on PUBLICATION_DATE | none flagged | yes | W87 |
| LIBRARY_RAW.LANDING.FED_BLS_QCEW | 3,619,437 | 41 | not yet measured | AREA_FIPS | no | W6 |
| LIBRARY_RAW.LANDING.FED_CMS_OPEN_PAYMENTS | 15,385,047 | 94 | not yet measured | CCN, NPI, RECIPIENT_ZIP_CODE, ASSOCIATED_DRUG_OR_BIOLOGICAL_NDC_1 | no | W50 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_SERVICE_DY2013 | 9,286,633 | 31 | not yet measured | NPI, RNDRNG_PRVDR_STATE_FIPS, RNDRNG_PRVDR_ZIP5 | no | W40 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_SERVICE_DY2014 | 9,316,209 | 31 | not yet measured | NPI, RNDRNG_PRVDR_STATE_FIPS, RNDRNG_PRVDR_ZIP5 | no | W40 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_SERVICE_DY2015 | 9,496,848 | 31 | not yet measured | NPI, RNDRNG_PRVDR_STATE_FIPS, RNDRNG_PRVDR_ZIP5 | no | W40 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_SERVICE_DY2016 | 9,714,896 | 31 | not yet measured | NPI, RNDRNG_PRVDR_STATE_FIPS, RNDRNG_PRVDR_ZIP5 | no | W40 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_SERVICE_DY2017 | 9,847,443 | 31 | not yet measured | NPI, RNDRNG_PRVDR_STATE_FIPS, RNDRNG_PRVDR_ZIP5 | no | W40 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_SERVICE_DY2018 | 9,961,865 | 31 | not yet measured | NPI, RNDRNG_PRVDR_STATE_FIPS, RNDRNG_PRVDR_ZIP5 | no | W40 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_SERVICE_DY2019 | 10,140,228 | 31 | not yet measured | NPI, RNDRNG_PRVDR_STATE_FIPS, RNDRNG_PRVDR_ZIP5 | no | W40 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_SERVICE_DY2020 | 9,449,361 | 31 | not yet measured | NPI, RNDRNG_PRVDR_STATE_FIPS, RNDRNG_PRVDR_ZIP5 | no | W40 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_SERVICE_DY2021 | 9,886,177 | 31 | not yet measured | NPI, RNDRNG_PRVDR_STATE_FIPS, RNDRNG_PRVDR_ZIP5 | no | W40 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_SERVICE_DY2022 | 9,755,427 | 31 | not yet measured | NPI, RNDRNG_PRVDR_STATE_FIPS, RNDRNG_PRVDR_ZIP5 | no | W40 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_SERVICE_DY2023 | 9,660,647 | 31 | not yet measured | NPI, RNDRNG_PRVDR_STATE_FIPS, RNDRNG_PRVDR_ZIP5 | no | W40 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTB_PROVIDER_SERVICE_DY2024 | 9,781,673 | 31 | not yet measured | NPI, RNDRNG_PRVDR_STATE_FIPS, RNDRNG_PRVDR_ZIP5 | no | W40 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DRUG_DY2013 | 23,645,873 | 25 | not yet measured | NPI, PRSCRBR_STATE_FIPS | no | W44 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DRUG_DY2014 | 24,120,618 | 25 | not yet measured | NPI, PRSCRBR_STATE_FIPS | no | W44 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DRUG_DY2015 | 24,524,894 | 25 | not yet measured | NPI, PRSCRBR_STATE_FIPS | no | W44 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DRUG_DY2016 | 24,964,300 | 25 | not yet measured | NPI, PRSCRBR_STATE_FIPS | no | W44 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DRUG_DY2017 | 25,209,130 | 25 | not yet measured | NPI, PRSCRBR_STATE_FIPS | no | W44 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DRUG_DY2018 | 25,311,600 | 25 | not yet measured | NPI, PRSCRBR_STATE_FIPS | no | W44 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DRUG_DY2019 | 25,401,870 | 25 | not yet measured | NPI, PRSCRBR_STATE_FIPS | no | W44 |
| LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DRUG_DY2020 | 25,209,729 | 25 | not yet measured | NPI, PRSCRBR_STATE_FIPS | no | W44 |
| LIBRARY_RAW.LANDING.FED_COURTLISTENER_FINANCIAL_DISCLOSURES | 70,776 | 19 | not yet measured | PERSON_ID | no | W77 |
| LIBRARY_RAW.LANDING.FED_EIA860_GENERATOR_Y2019 to 2023, 5 tables | 156,087 | 84 | 2019-2023 | PLANT_CODE | no | W23 |
| LIBRARY_RAW.LANDING.FED_EIA860_PLANT_Y2019 to 2023, 5 tables | 67,231 | 45 | 2019-2023 | PLANT_CODE, ZIP | no | W23 |
| LIBRARY_RAW.LANDING.FED_FARA_BULK | 221,900 | 31 | not yet measured | ZIP | no | W84 |
| LIBRARY_RAW.LANDING.FED_FDA_GUDID_FULL_DEVICE | 5,182,695 | 37 | not yet measured | none flagged | no | W50 |
| LIBRARY_RAW.LANDING.FED_FDA_GUDID_FULL_IDENTIFIERS | 6,767,219 | 12 | not yet measured | none flagged | no | W50 |
| LIBRARY_RAW.LANDING.FED_FEDERAL_REGISTER_DOCUMENTS | 485,594 | 32 | not yet measured | none flagged | no | W87 |
| LIBRARY_RAW.LANDING.FED_HOUSE_PTR | 27,286 | 22 | not yet measured | TICKER | no | W52 |
| LIBRARY_RAW.LANDING.FED_HUD_MF_PROPERTIES_OWNERS | 23,612 | 77 | not yet measured | STATE_CODE, ZIP_CODE, COUNTY_CODE, OWNER_COMPANY_TYPE | no | W3 |
| LIBRARY_RAW.LANDING.FED_MSHA_MINES | 91,906 | 62 | not yet measured | MINE_ID, CURRENT_CONTROLLER_ID, FIPS_CNTY_CD, FIPS_CNTY_NM | no | WN-136 |
| LIBRARY_RAW.LANDING.FED_SAM_EXCLUSIONS_FULL_R2 | 168,328 | 34 | not yet measured | ZIP_CODE, NPI | no | W72 |
| LIBRARY_RAW.LANDING.FED_SEC_13F_SECURITIES_LIST | 25,333 | 10 | not yet measured | CUSIP | no | W51 |
| LIBRARY_RAW.LANDING.INT_UK_COMPANIES_HOUSE | 5,734,780 | 58 | not yet measured | none flagged | no | W117 |
