# The 125 wonders, reviewed 2026-09-18

Chris's ask, verbatim: "go through those 125 and really think if these are the top 125 that we can
start with. Really evaluate, optimize, enhance the ideas. Come back to me with a list of things we
can add/change/tweak."

Nothing here was run against data. No wonder was tested. Nothing in THE_IDEA_BOOK.md was edited.

## What was checked

| check | how | what a hit means | what a miss means |
|---|---|---|---|
| each wonder's gap | status column of all 125 rows in the wonder extract, written 2026-09-09 | the wonder named a missing table or key | it was clean on 09-09 |
| gap closed since | `reports/phase5_probe_2026-09-10.md`, the "Landed" table, 09-10 to 09-11 | the missing table now exists in LANDING | gap still open |
| real columns | INFORMATION_SCHEMA through the Python door, 6 new tables, 2026-09-18 | the column the wonder needs is there by name | still a guess |
| better ideas left out | wonder rankings rows WN-126 to WN-155, score 240 and up | verified, scored, and not among the 125 | the 125 already hold it |

Columns confirmed by name on 2026-09-18:
- `FED_CMS_SNF_OWNERSHIP`: ASSOCIATION_DATE_OWNER, PRIVATE_EQUITY_COMPANY_OWNER, REIT_OWNER, HOLDING_COMPANY_OWNER, PERCENTAGE_OWNERSHIP, owner names and addresses.
- `FED_EOIR_PROCEEDING`: IJ_CODE, NAT, DEC_CODE, DEC_TYPE, COMP_DATE, ABSENTIA, CUSTODY, BASE_CITY_CODE.
- `FED_DOL_WHD_ENFORCEMENT`: H1B_VIOLTN_CNT, H2A_VIOLTN_CNT, FLSA_REPEAT_VIOLATOR, FLSA_CL_MINOR_CNT, legal name, street, ZIP, NAICS.
- `FED_HUD_MF_PROPERTIES_OWNERS`: IS_NURSING_HOME_IND, OWNERSHIP_EFFECTIVE_DATE, owner names, COUNTY_CODE.
- `FED_CENSUS_COUNTY_2020`: names and FIPS only. No population column.
- `FED_CENSUS_ZCTA_COUNTY_2020`: ZCTA, county GEOID, land area of the overlap.

## The headline

The 125 came from one riff session. They were never scored.
The 30 scored and verified wonders, WN-126 to WN-155, are a separate pile.
Only one of the scored top 31 sits in the 125: wonder 79, unpaid mine fines, rank 1.
So the 125 is not the top 125. It is a good wide list missing its own best rows.

| verdict | count | meaning |
|---|---|---|
| KEEP | 41 | fine as worded |
| UNLOCKED | 36 | the gap named on 09-09 was landed on 09-10 or 09-11; book status is stale |
| REWORD | 15 | the question is good, the wording asks for something the data cannot show |
| MERGE | 10 | a twin of another wonder in the same list; the seat opens up |
| SWAP OUT | 23 | dead, circular, or no data landed |

33 seats open: 10 merges plus 23 swap-outs.

## SWAP OUT, 23

| # | wonder | why |
|---|---|---|
| 17 | Discharge permits upstream of poorest water systems | no coordinates on water systems, no flow network |
| 19 | Highway deaths where trauma centers closed | no crash file by county, no trauma-center list |
| 20 | For-profit colleges near bases and vets | no base table, no vet population |
| 21 | Counties lost hospital and community college | no college closure dates |
| 22 | Elections on smallest budget per voter | EAVS has no budget question and no year |
| 24 | Plants run dirtiest on hottest days | no temperature series |
| 25 | Plant-county water violations after hot summer | no temperature series |
| 31 | Hospices in chains discharge alive more | no hospice quality or claims file, no chain id |
| 38 | Hospital mergers precede Part B price rises | outpatient is one year, no series |
| 43 | Adverse events cluster by prescriber state | FAERS has no state and no prescriber; ends 2014q2 |
| 52 | Congressional trades around hearings | trades 2012-2020, votes and bills 2023 on, zero overlap; no hearing table |
| 57 | Banks finance most polluting sites | no loan-to-facility edge anywhere in public data |
| 64 | Failed banks financed polluting sites | same hole as 57 |
| 94 | Foreign agent filings track arms sales | no arms-sales table |
| 100 | Universities patent on federal money, license to donor | no patent table, no donor names |
| 106 | Drug price spike after generic count drops to one | only one table carries NDC; generic count impossible |
| 108 | Ships visit sanctioned ports then US ports | AIS is US waters only; SDN has no designation date |
| 109 | Rail crashes where rail owner fined | no rail enforcement table |
| 110 | Shell-owned aircraft fly contractor routes | no flight-track table |
| 112 | Ships loiter before a spill report | spill mart has no location or vessel id |
| 114 | UK controllers share address with sanctions | sanctions lists carry no US address; past name matches were 100% noise |
| 118 | Student-loan complaints where servicer changed | circular: the change is inferred from the complaints themselves |
| 119 | Research patents track federal or donor money | twin of 100, same hole |

These stay in the book. They leave the starting list only.

## MERGE, 10 seats freed

| drop | into | why |
|---|---|---|
| 4 | 122 | aided three times and flood-rebuild-flood are one county repeat count |
| 14 | 30 | both are water violations where a hospital closed |
| 27 | 40 | "bad-air day" cannot be seen in annual claims; 40 is the annual version |
| 41 | 26 | pills per resident by county is the first frame of 26 |
| 42 | 26 | distributor counties versus deaths is the scatter of 26 |
| 54 | 86 | complaint spike leads enforcement, and the lag by bank, are one measure |
| 93 | 92 | foreign-owned by agency already splits defense from health |
| 101 | 125 | injuries after a buyout and injuries by owner share one table and one key |
| 105 | 102 | visa sponsors and wage violations, map and network of the same join |
| 116 | 98 | offshore names; the property half has no table, the rest is 98 |

Wonder 81, votes drift toward donors, stays, tied to M-056, the money-before-the-vote pick.

## UNLOCKED, 36

The book row for each still reads "not checked" with a gap. The gap is closed.

| # | wonder | what landed that closes the gap |
|---|---|---|
| 1 | Flood aid then mortgage denials | HMDA 2018-2024 with county and tract; FEMA declarations |
| 2 | Redline maps predict water violations | county FIPS now on the water areas mart; redline mart is still 11% of polygons |
| 5 | Lenders pull out after the first big storm | HMDA now runs 2007-2024 |
| 6 | Counties that lost doctors, banks, factories | NPPES deactivation file, 351,912 doctors with dates |
| 8 | One doctor per thousand and shrinking | deactivation dates; still no county population table |
| 10 | Rural counties send most, get least | assistance no longer capped; contracts carry county FIPS |
| 11 | Rural water systems violate more | county FIPS on water areas |
| 13 | Counties host plants, get least money | eGRID 2019-2023; full assistance |
| 16 | Fracking counties, water violations climb | county FIPS on water areas |
| 23 | Coal plants closed, respiratory claims fell | EIA-860 2019-2023 shows retirements; health side still one year |
| 26 | 2010 pill counties become overdose counties | county FIPS on 178M ARCOS rows; CDC county overdose 2019-2024 is numeric |
| 28 | Homes chart sicker after a chain buys them | owner file has ASSOCIATION_DATE_OWNER and a private-equity flag |
| 29 | Dialysis chains arrive, kidney doctors fall | deactivation dates give the exits |
| 30 | Water violations where hospitals closed | county FIPS on water areas |
| 36 | Nonprofit hospitals, least charity per surplus | hospital CCN-to-EIN crosswalk, 4,003 CCNs |
| 37 | Hospitals closed, where doctors went | deactivation dates; affiliation is still a snapshot |
| 45 | Antipsychotics per bed track ownership | owner file replaces the chain id that is blank on 4,551 homes |
| 53 | Zips give most, get least back | assistance cap gone; ZCTA-to-county bridge |
| 55 | Disaster contractors win same counties | declarations table plus county FIPS on contracts; both holes closed |
| 59 | Denial rates diverge between neighbor counties | HMDA 2007-2024 |
| 67 | Nonprofit revenue spikes after a declaration | declarations table, no more distinct-ing 26M rows |
| 68 | Nonprofits win grants and register lobbyists | LDA holds every year but 2017; assistance full; still no EIN on either side |
| 70 | After population, which counties get more contracts | county FIPS on contracts; still no county population table |
| 71 | After income, which lenders deny more | HMDA 2018 on carries LEI, a clean lender key |
| 76 | Immigration judge grant rate drifts | 16.8M proceedings with judge code, nationality, decision, date |
| 82 | Bills lobbied hardest before markup | LDA years filled, now overlaps the 2023 bills |
| 87 | Lobbying spikes before agency rules | was dead on zero overlap; LDA now overlaps the Federal Register; grain is quarters, not weeks |
| 90 | Detention contracts grow where detainers grow | county FIPS on contracts |
| 92 | Foreign-owned contractors by agency | archive tables carry the domestic-or-foreign code and agency code |
| 97 | Doctors also donors, contractors, nursing owners | nursing-home owner file names the people |
| 102 | Visa sponsors carry unpaid wage judgments | WHD enforcement landed, and it counts H-1B and H-2A violations itself |
| 103 | Union locals shrink where contracts grow | county FIPS on contracts |
| 113 | UK shell controls a US nursing home | owner file names the owning companies with addresses |
| 122 | Counties flood, rebuild, flood again | declarations table; full assistance |
| 123 | Hospital charity rises where wages fall | cost reports answer it; crosswalk adds the 990 side |
| 124 | After plant count, which operators dirtier | eGRID five years instead of one |

LDA 2017 was mid-rerun on 2026-09-11. Its state today was not checked.

## REWORD, 15

| # | now | reword to | why |
|---|---|---|---|
| 3 | PE landlords and CFPB complaints rise together | Biggest HUD multifamily owners, and what their buildings' inspection and finance records show | CFPB takes complaints on lenders, not landlords; HUD owner file is the real table |
| 15 | Unsafe dams upstream of nursing homes or schools | High-hazard dams within ten miles of a nursing home | no school table, no flow direction; distance is honest |
| 39 | Hospitals own the home health agency they refer to most | Hospitals that own a home health agency, and how many | referral file is yes/no, no volume |
| 44 | Drugs leading cost growth, who prescribes most | The costliest drugs of one year, and who prescribes them | the by-drug file is one year |
| 48 | Dinners precede prescribing shifts by a quarter | Doctors paid in 2022, what they prescribed that year versus unpaid peers | prescribing is annual |
| 49 | Excluded, reinstated, and paid again | Excluded and still paid | the exclusion list holds active exclusions only |
| 51 | 13F shifts the quarter before a contract lands | same, matched on issuer name, multi-word names only | 13F list gives CUSIP to name; CUSIP to CIK still missing |
| 56 | Banks under orders keep lending in same zips | Banks under orders keep lending in same counties | mortgage file has no ZIP; has county, tract and LEI |
| 62 | 13F holders exit before the first big fine | same, fine side from EPA and mine penalties, not the SEC | no SEC enforcement table; other fine tables are landed |
| 69 | Hospital foundations donate to members | Hospital PACs and hospital employees donate to members | a charity cannot give to a candidate |
| 75 | NIH grants land where pharma dinners land, by NPI | same, by county | only ZIP is shared, and ZIP identifies nothing |
| 89 | Lobbyists who were regulators | Which agency jobs appear most in lobbyists' covered-position text | the table lists jobs, not people |
| 91 | Immigration judges who reverse most, who appointed | Immigration judges furthest from their own court's average | judges landed; appeals and appointer did not |
| 99 | Hospital execs on boards of their own suppliers | Hospital execs who are also insiders at public companies | private suppliers are invisible; insider filings are not |
| 111 | Recalls hit models sold in poorer states | Recalled models with the most complaints per state | no sales or registration table |

## ADD, 27 scored wonders that belong in the starting list

All verified against live data when scored. None sit in the 125.

| book id | wonder | score | note |
|---|---|---|---|
| H-106 | Citation severity depends on which state inspected | 625 | measured: 9.5x spread across states |
| P-146 | Mine deaths without a paper trail | 500 | |
| P-147 | Mine changes hands, violation rate changes | 500 | top-3 pick, SQL mapped |
| P-148 | A death at one mine changes the operator's other mines | 500 | |
| P-081 | More-minority communities inspected less | 500 | measured: 2.90 to 1.46 inspections |
| H-094 | Staffing predicts the next deficiency | 500 | |
| H-107 | Nursing-home fines per owner, not per location | 400 | the new owner file fixes the 28.7% blank chain name |
| M-239 | Templated CFPB narratives | 400 | one narrative appears 27,510 times |
| H-105 | Stars lost after a fine, or fines after lost stars | 400 | |
| M-245 | Complaint spike at one bureau appears at the others | 400 | |
| P-159 | OSHA injury counts bunch on round numbers | 400 | |
| M-240 | Companies with one canned complaint response | 400 | |
| P-160 | After a reported death, do hours and injuries change | 400 | |
| WN-136 | Same-owner co-spike, controlling for district and calendar | 400 | the open follow-on from 2026-08-21 |
| P-149 | Mine inspection has a season, accidents fill the gaps | 320 | 26 years |
| H-110 | Inspection records too clean for their peers | 320 | |
| WN-143 | CFPB filing language collapses over 14 years | 320 | |
| WN-144 | Injury rates cluster by industry and state | 320 | |
| H-104 | Does a fine change behaviour, before versus after | 300 | |
| WN-147 | Predicted versus actual inspection outcomes | 300 | |
| WN-149 | Does special-focus status change a home | 300 | |
| H-111 | Surveys bunch at the end of the window | 256 | |
| WN-150 | Low-entropy inspection outcomes | 256 | |
| M-056 | Money arrives right before the vote | 240 | top-3 pick, SQL mapped; absorbs wonder 81's chain |
| WN-152 | The donor in the most networks | 240 | 268 committees |
| WN-154 | Homes that act like a chain without being one | 240 | |
| WN-155 | Money before votes versus after, two rivers | 240 | |

Left out on purpose: WN-134, WN-148 and WN-145 are already answered; they live in the findings chapter.

## ADD, 6 new wonders nobody wrote yet

Each leans on a column confirmed by name on 2026-09-18. None were run.

| new | wonder | table and column | picture |
|---|---|---|---|
| N1 | Employers caught with child-labor violations that hold federal contracts | WHD FLSA_CL_MINOR_CNT, to contracts by multi-word name plus ZIP | RANK |
| N2 | Removal orders given with nobody in the room, by court and year | EOIR ABSENTIA, BASE_CITY_CODE, COMP_DATE | ANIM |
| N3 | Private-equity and REIT owned homes versus the rest: fines, stars, staffing | SNF owner flags, to CCN through ENROLLMENT_ID | SCAT |
| N4 | Taxpayer-insured nursing homes and their citation record | HUD IS_NURSING_HOME_IND, to CMS homes by address plus ZIP | RANK |
| N5 | Repeat wage violators that keep winning contracts | WHD FLSA_REPEAT_VIOLATOR, to contracts FY2008-2026 | RANK |
| N6 | Recipients that appear only in FY2020 and FY2021 assistance, then vanish | 45.8M of the 128.2M assistance rows sit in those two years | RANK |

27 plus 6 is 33, the same number of seats opened.

## TWEAK, five list-wide changes

1. **Nine wonders hub on ZIP.** ZIP tops the reach list and identifies nothing. Three leave the list anyway (20, 27, 105). Restate the six that stay on county through the ZCTA bridge: 1, 3, 40, 53, 56, 121.
2. **Twenty-four NET wonders join on a name.** Multi-word names cleared 92%, single-word 8%. Every name wonder gets "multi-word names only" written into it.
3. **Time words the data cannot honour.** "by a quarter", "day", "weeks" on annual or quarterly files: 27, 48, 87. Reworded above.
4. **Five "after X explains Y" wonders need a denominator that is not landed**: 46, 47, 70, plus 8 and 34. The 2020 county table has no population column. One county population, poverty and age table unlocks all five.
5. **The book's status column is stale for 36 rows.** Each needs its gap line replaced with the landed table's name.

## Where to start inside the list

| # | wonder | why first |
|---|---|---|
| 18 | Water systems violate yearly, never enforced | the one row with "gap none, trap none", one key |
| 79 | Mine fines unpaid | already measured, $548M never collected |
| 76 | Immigration judge grant rates | went from "no data" to 16.8M rows in one landing |
| 28 | Homes after a buyout | went from no purchase date to a dated owner file with a PE flag |
| 55 | Disaster contractors | both named holes closed on 09-10 |

---

# Skeptic pass, 2026-09-18: DISAGREE

A fresh-context reviewer attacked this file through the Python door. Nothing above was rewritten; the breaks are listed here so both views stand side by side.
The blind spot it found: six columns were "confirmed by name" and none were checked for being filled.

## Broken

| item | what this file says | what the skeptic found |
|---|---|---|
| N4 | taxpayer-insured nursing homes, HUD IS_NURSING_HOME_IND | the column is 'N' on all 23,612 rows. Empty set. N4 is dead |
| N3, wonder 28, "start here" row | owner file has a private-equity flag | PRIVATE_EQUITY_COMPANY_OWNER is 'Y' on 196 of 295,083 rows, 97 of 14,410 enrollments, 0.67%. REIT_OWNER 'Y' on 587 enrollments. Both flags are blank, not 'N', on 198,546 rows, 67%. So "the rest" is two-thirds unknown. N3 is a study of about 684 homes, not a population split |
| wonder 52 | SWAP OUT, trades and votes have zero overlap | true only of the Senate trades mart. L.FED_HOUSE_PTR holds 27,286 House trades, filing years 2021-2026, with ticker and date. L.FED_SENATE_EFD_PTR runs to 2025-12-31. Overlap exists. 52 is a REWORD: trades around votes, since no hearing table exists |
| tweak 4, wonders 8, 46, 47, 70 | no county population table | M.HEALTH.HEALTH__FED_CDC_DRUG_POISONING_COUNTY has FIPS, YEAR, POPULATION, 3,141 counties, 1999-2015. The honest line is "no county population after 2015" |
| KEEP, 41 rows | "fine as worded", never listed | the numbers: 7, 9, 12, 18, 32, 33, 34, 35, 40, 46, 47, 50, 58, 60, 61, 63, 65, 66, 72, 73, 74, 77, 78, 79, 80, 81, 83, 84, 85, 86, 88, 95, 96, 98, 104, 107, 115, 117, 120, 121, 125. Five spot-checks, four fail "fine as worded": 60 has no "before" for 2008-2012 failures; 117 has no sector column; 120 sees only the last penalty per EPA site; 46 and 47 are blocked on a denominator by this file's own tweak 4 |
| wonder 81, M-056, WN-155 | all three hold seats | one money-to-votes chain, three seats. The merge rule was applied to the 125 and not to the adds |
| LDA, wonders 68, 82, 87 | "every year but 2017, rerun state not checked" | L.FED_SENATE_LDA_FILINGS holds 1999-2026, all 28 years; 2017 has 77,223 rows. The rerun finished |
| ASSOCIATION_DATE_OWNER, wonders 28, 45 | treated as a purchase date | filled on every row, but free text in mixed formats, three 1800 sentinels, and the file is one vintage so only current owners show. It is an association record date; nothing shows it tracks a sale |
| wonder 45 | UNLOCKED | the owner file fixes the blank chain id, the lesser hole. The binding limit is still facility affiliation: 35.5% of homes list one doctor |

## Tried to break, held

| claim | check |
|---|---|
| 41+36+15+10+23 = 125, each number once | clean partition |
| N6, 45.8M of 128.2M rows in FY2020-21 | 45,820,068 of 128,155,142, exact |
| county FIPS on the contracts year tables | column present on FY2008 and FY2024 |
| domestic-or-foreign and agency code, wonder 92 | both present on FY2008 and FY2024 |
| wonder 71, an income column on HMDA 2018 on | INCOME, DEBT_TO_INCOME_RATIO, LEI, COUNTY_CODE present |
| LDA overlaps the Federal Register, wonders 82, 87 | 1999-2026 against 2023-01 to 2026-06 |
| wonder 26, pills then overdoses | ARCOS is 2006-2012, CDC county overdose 2019-2024; a lag question, both ends exist |
| N3 join path | ENROLLMENT_ID reaches CCN through the SNF enrollments table |
| nine ZIP-hub wonders | exactly 1, 3, 20, 27, 40, 53, 56, 105, 121 |

## The author's view of the skeptic

Agreed on every break. None is a matter of taste; each is a count or a table that exists.
Net effect on the seats: N4 out, wonder 52 back in as a reword, 81 folds into M-056 and WN-155 folds into M-056. Two seats reopen.
