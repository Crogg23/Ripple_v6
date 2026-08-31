# What the warehouse holds — every noun and event, in plain English

*Built 2026-08-18. Every number below comes from the census fill finished 2026-08-17,
which measured all 589 shelf tables (1,227,375,627 rows total). Each line names its
own receipt. Two counting methods appear:*

- ***"Aug 11 scan"** = the row was counted by scanning the actual table during the
  Aug 11 full-warehouse verification, reused unchanged in the Aug 17 census.*
- ***"Aug 17 scan"** = a fresh row-by-row count run Aug 17 (the new court tables and
  a few others).*

*A row is not always a real-world thing — where the table's grain means "rows ≠
things," the line says so. Where a count is an exactly-round number, it's flagged
as a probable download cap, not a real total.*

---

# NOUNS (things that exist)

## People

- **Judges (federal + state)** — 16,191 — counted rows in the judge roster (Aug 17 scan); a dedup check found 16,057 distinct people (394 thin alias rows, zero false merges).
- **Judges' schools attended** — 12,777 education records + 6,542 race records — attribute rows about the judges above, counted in two fresh Aug 17 scans (not extra people).
- **Members of Congress (historical)** — 51,061 — counted rows in the congressional-member roster (Aug 11 scan); one row is a member *per Congress served*, so distinct people are far fewer (not measured).
- **Current/recent legislators** — 12,847 — counted rows in the legislator biographical file (Aug 11 scan); likely one row per legislator-term, distinct people fewer. Plus 3,879 committee-seat rows counted in the committee-membership file.
- **Federal candidates** — 33,506 — counted rows in the FEC candidate master (Aug 11 scan); **19% of rows are exact duplicates**, so real count is nearer ~27k.
- **Political committee ↔ candidate rows** — 866,730 — counted in the committee-to-candidate money ledger (Aug 11 scan); these are money-transfer rows, listed again under EVENTS where they belong.
- **Dark-money group officers/directors** — 189,593 — counted rows in the 527-organization directors file (Aug 11 scan); one row per person per form filed.
- **People with significant control of UK companies** — 7,000,000 — counted rows in the UK beneficial-ownership file (Aug 11 scan); **exactly round — almost certainly a download cap, treat as "at least."**
- **Taxonomy experts** — 197 — counted rows in the species-database expert list (Aug 11 scan).

## Companies & organizations

- **UK companies** — 5,734,780 — counted rows in the UK company register (Aug 11 scan).
- **Global legal entities (LEI)** — 3,382,301 — counted rows in the international legal-entity register (Aug 11 scan). A second table of 6,259,489 rows is *reporting exceptions* (entities explaining why they didn't name a parent), not extra entities — counted separately (Aug 11 scan).
- **Irish companies** — 821,693 — counted rows in the Irish company register (Aug 11 scan).
- **Offshore-leaks entities** — 814,344 — counted rows in the leaked offshore-entity table (Aug 11 scan). Plus 26,768 intermediaries, 2,989 "other" parties, and 402,246 addresses, each counted in its own table (Aug 11 scan).
- **Spanish company gazette entries** — 3 — counted (Aug 11 scan); effectively an empty load.
- **Foreign financial institutions (tax-compliance register)** — 516,298 — counted rows in the offshore-bank registration list (Aug 11 scan).
- **US banks** — 27,836 — counted rows in the bank-data table (Aug 11 scan); may be bank-per-quarter rows, distinct banks fewer (grain unstated). Plus 3,584 failed banks and 724 nationally-chartered banks + 218 thrifts, each counted in its own list (Aug 11 scan).
- **Credit unions** — 4,250 — counted rows in the federally-insured credit-union list (Aug 11 scan); two quarterly financial-report tables of 4,336 rows each counted alongside.
- **Institutional investment filers** — 344,109 — counted rows in the quarterly-holdings filer list (Aug 11 scan).
- **Stock tickers / listed companies** — 10,414 — counted rows in the ticker map (Aug 11 scan); a second exchange-annotated copy holds 10,398 (Aug 11 scan).
- **Registered investment funds** — 1,206 money-market + 973 closed-end + 43,123 fund series/class records — each counted in its own registry (Aug 11 scan). **Warning: two fund tables carry garbage year-0095/0099 dates — date parsing broken.**
- **Municipal-securities dealers** — 925 — counted rows in the registrant list (Aug 11 scan).
- **Canadian regulated financial institutions** — 343 — counted (Aug 11 scan).
- **Electric utilities** — 6,643 — counted rows in the utility file of the federal generator census (Aug 11 scan); ~4,900 more utility-per-state rows in three related tables counted alongside.
- **Balancing authorities (grid operators)** — 189 — counted rows, one per authority-per-state (Aug 11 scan).
- **Largest US companies (reference list)** — 100 — counted (Aug 11 scan); a scraped top-100 list, not a registry.
- **Federal agencies** — 111 — counted rows in the top-tier agency list (Aug 11 scan).
- **Railroads (reporting)** — 224,941 rows — counted in the equipment-accident file (Aug 11 scan); **one row is a railroad-per-accident, not a railroad** — the real railroad universe is tiny; listed again under EVENTS.
- **Licensed firearms dealers** — 77,514 — counted rows in the federal firearms-license list (Aug 11 scan).
- **Lobbying employers (California)** — 1,730 — counted, one row per employer per legislative session (Aug 11 scan). Plus 256 lobbying firms, same file family.
- **Drug/device manufacturers (payment-program)** — 2,462 — counted, one row per manufacturer per program year (Aug 11 scan).
- **Research organizations (global registry)** — 135,710 — counted rows in the research-org registry (Aug 11 scan).
- **Research funders (registry)** — 45,661 — counted rows in the funder registry (Aug 11 scan).
- **Universities/colleges** — 6,273 — counted rows in the college-scorecard institution table (Aug 11 scan). **Its staging view is broken** (the raw table it points at no longer exists — likely re-pulled under a new name).
- **Law schools & universities (judge-linked)** — 6,011 — counted rows in the court-data schools table (Aug 17 scan).
- **Public housing authorities** — 3,787 — counted (Aug 11 scan).

## Charities & nonprofits

- **Tax-exempt organizations (IRS master file)** — 1,983,563 — counted rows in the exempt-org business master file (Aug 11 scan). A second near-twin load of 1,974,830 rows also exists — counted separately (Aug 11 scan); **same dataset landed twice.**
- **Charities eligible for deductible donations** — 1,435,544 — counted rows in the eligible-donee publication (Aug 11 scan).
- **Orgs that lost tax-exempt status** — 1,187,367 — counted rows in the revocation list (Aug 11 scan); a near-twin "auto-revocation" table holds 1,207,295 (Aug 11 scan) — **likely the same list twice; not verified.**
- **Charity financial summaries (research sample)** — 2,450 — counted rows in the charity statistics extract (Aug 11 scan).
- **Dark-money (527) organizations** — 77,591 — counted rows in the 527 registration file (Aug 11 scan).
- **Political committees** — 78,039 — counted rows in the committee master (Aug 11 scan); **23% exact-duplicate rows**, so real count nearer ~60k. A second bulk load holds 20,007 (Aug 11 scan).
- **Union financial filings (with assets/members)** — 617,710 — counted rows in the union annual-report file (Aug 11 scan); one row per filing, not per union.

## Health care providers & facilities

- **All US health providers (national registry)** — 9,606,683 — counted rows in the national provider registry (Aug 11 scan); one row per provider ID. Known trap: its employer-tax-ID column is ~100% masked — never join on it.
- **Medicare-enrolled providers** — 2,978,925 — counted rows in the Medicare enrollment file (Aug 11 scan). (Miscataloged under the immigration schema — cosmetic, flagged.)
- **Prescribers** — ~1.4M distinct — the summary prescriber table holds 1,416,883 rows (Aug 11 scan); the big 25,869,521-row table is **prescriber-by-drug lines, not people** (Aug 11 scan).
- **Doctors billing Medicare (by service)** — 9,781,673 rows — counted (Aug 11 scan); **one row is provider-by-service-by-year, not a person**; the per-provider summary holds 1,296,739 rows (counted twice under two table names — twin loads, Aug 11 scan).
- **Hospitals** — 5,432 — counted rows in the hospital quality table (Aug 11 scan); an identical-size general-info twin also counted (Aug 11 scan).
- **Nursing homes** — 14,700 — counted rows in the nursing-home registry (Aug 11 scan).
- **Community health centers** — 1,356 centers + 19,038 delivery sites — each counted in its own federally-funded health-center table (Aug 11 scan).
- **Opioid treatment programs** — 1,558 — counted (Aug 11 scan).
- **Providers pending Medicare approval** — 7,240 physicians + 6,880 non-physicians — counted in two pending-enrollment tables (Aug 11 scan).
- **Specialty-model participants** — 6,637 — counted (Aug 11 scan).
- **Health professional shortage areas** — 165,531 area rows + 79,158 score rows — counted in the shortage-area and scoring tables (Aug 11 scan); rows are area-by-component, not unique places.
- **Medical device registry (unique device IDs)** — 5,083,948 — counted rows in the device-identifier registry (Aug 11 scan).
- **Cleared/approved medical devices** — 175,686 clearances + 56,853 approvals — counted in the two device-review tables (Aug 11 scan).
- **Drugs (adverse-event drug list)** — 20,914,284 rows — counted (Aug 11 scan); **one row is a drug-per-case mention, not a distinct drug.** The drug-price reference table holds 359,514 rows (Aug 11 scan).
- **Drug master files** — 41,253 — counted rows in the manufacturing-file list (Aug 11 scan).
- **Drug label map** — 158,452 — counted rows in the label-document index (Aug 11 scan).

## Environmental facilities, water systems, energy

- **EPA-registered facilities (master registry)** — 3,277,557 — counted rows in the facility registry (Aug 11 scan); verified 100% usable as a spine key in the Aug 17 batch. A larger 5,300,149-row copy with program links also counted (Aug 11 scan) — **two loads of the registry family, not distinct facilities.**
- **EPA-tracked regulated facilities (compliance snapshot)** — 3,135,554 — counted rows in the enforcement/compliance snapshot (Aug 11 scan).
- **Hazardous-waste sites** — 1,613,224 — counted rows in the hazardous-waste facility file (Aug 11 scan).
- **Water-discharge permit holders** — 1,213,737 — counted rows in the discharge-permit facility file (Aug 11 scan); verified 100% referenced by all seven of its event tables (Aug 17 batch check).
- **Drinking-water systems** — 434,040 — counted rows in the public-water-system inventory (Aug 11 scan). Plus 1,554,832 rows of water-system facility components counted separately (Aug 11 scan).
- **Air-program facilities** — 457,581 — counted rows in the air-compliance program file (Aug 11 scan).
- **Greenhouse-gas reporting facilities** — 136,005 — counted (Aug 11 scan).
- **Toxics-release facilities (2023)** — 78,647 — counted (Aug 11 scan).
- **Air-quality monitoring sites** — 20,994 — counted (Aug 11 scan).
- **Water-quality monitoring stations** — 5,818 — counted (Aug 11 scan).
- **Superfund site boundaries** — 2,114 — counted (Aug 11 scan).
- **A 5,000-row facility sampler** — 5,000 — counted (Aug 11 scan); **exactly 5,000 = download cap, a sample not a universe.**
- **Dams** — 92,766 — counted rows in the national dam inventory (Aug 11 scan).
- **Orphaned oil & gas wells** — 117,672 — counted (Aug 11 scan).
- **Mines** — 91,906 — counted rows in the mine registry (Aug 11 scan).
- **Power plants** — 16,132 plant rows + 11,974 emissions-profile rows + 26,855 generator rows + smaller solar/wind/multifuel/boiler files — each counted in its own table of the federal generator census (Aug 11 scan).

## Places & geography

- **US counties (economic panel)** — 3,619,437 rows — counted in the county employment/wages panel (Aug 11 scan); **rows are county-by-industry-by-quarter, not counties.** Smaller county health tables (132,000 injury, 53,387 drug-poisoning rows) counted alongside.
- **Named places (national gazetteer)** — 1,249,624 — counted rows in the geographic-names file (Aug 11 scan).
- **Water-service and geographic areas** — 578,198 + 422,464 — counted in the two drinking-water area tables (Aug 11 scan).
- **Flood-program communities** — 25,122 — counted (Aug 11 scan).
- **Utility service territories** — 11,775 — counted (Aug 11 scan). States/territories reference: 56 rows.
- **Watersheds** — 2,456 — counted rows in the watershed-boundary index (Aug 11 scan).
- **Subsidized-housing project locations** — 13,550 — counted rows in the rural-development active-projects file (Aug 11 scan).

## Vehicles, aircraft, other assets

- **Registered aircraft** — 315,447 — counted rows in the aircraft registry (Aug 11 scan); a second registry load holds 314,417 (Aug 11 scan) — **twin loads; also the known epoch-date trap: its newest "date" reads 1970.**
- **Sanctioned ships / sex-offender registry (state)** — 33,828 UK-sanction entries incl. hulls; 28,185 registry rows — each counted in its own list (Aug 11 scan).
- **Futures-market positions (reference)** — 287,053 — counted rows in the trader-commitment file (Aug 11 scan); rows are market-by-week report lines.

## Documents, datasets, registries (bookkeeping nouns)

- **Federal rule-making documents** — 94,731 — counted rows in the federal-register document index (Aug 11 scan).
- **Retracted scientific papers** — 71,591 — counted (Aug 11 scan); a near-twin second load holds 71,388 — **same database twice.**
- **Scientific publications (species database)** — 30,772 — counted (Aug 11 scan).
- **DOJ Epstein-library page links** — 777 index links + 2,542 deep-page links + 1,537,352 archived-capture rows — each counted in its own scrape table (Aug 11 scan); rows are link-per-page, duplicates by design.
- **Open-data catalog entries (France, CDC, FTC, etc.)** — 130,431 French + 1,471 CDC + 1,200 FTC (16% dup) — each counted in its own catalog dump (Aug 11 scan). Ten foreign portal dumps of ≤5,000 rows each — **the exactly-5,000 ones are capped samples** (Aug 11 scan).
- **Government records samplers** — 10 rows across two archival tables — counted (Aug 11 scan); effectively empty loads.
- **Screening/watch lists** — 25,918 consolidated-screening entries, 19,115 sanctions designations, 1,011 UN sanctions entries, 952 chemical-hazard listings, 4,215 broker IDs — each counted in its own list (Aug 11 scan).
- **Housing-loan portfolio snapshot** — 61,647 — counted (Aug 11 scan).

---

# EVENTS (things that happened)

## Money moved

- **Opioid pill shipments** — attached to pharmacies/distributors/manufacturers — 178,598,026 — counted rows in the controlled-substance transaction ledger (Aug 11 scan).
- **Individual campaign contributions** — attached to donors → committees — 84,172,112 — counted rows in the federal contribution ledger (Aug 11 scan). Plus ~1.25M NYC contribution rows across seven election-cycle tables and 12,646,465 Canadian contributions, each counted in its own table (Aug 11 scan).
- **Committee-to-candidate transfers** — attached to committees → candidates — 866,730 — counted (Aug 11 scan).
- **Drug/device-company payments to doctors** — attached to doctors and hospitals — 43,335,833 across three program-year loads (15.4M + 14.7M + 13.25M) — each counted in its own table (Aug 11 scan). **The 13,250,000 is exactly round — probable load cap.** Plus 1,697,025 recipient-profile rows counted separately.
- **Federal assistance awards (grants, loans, aid)** — attached to recipient organizations — 19,902,879 transaction rows — counted (Aug 11 scan).
- **Federal contracts** — attached to contractor companies — 20,000,000 rows in the full ledger — counted (Aug 11 scan); **exactly round = capped load, AND all 20M rows carry at least one bogus-1970 date column.** A second 6,325,622-row transaction table counted alongside (Aug 11 scan). Smaller: 49,613 bulk award rows, 5,000 subawards (**capped**), 300 API-sample rows, 100 grants-portal rows (**capped**).
- **Research grants** — attached to universities/researchers — 2,122,611 — counted rows in the federal research-grant file (Aug 11 scan); **2.1M rows carry far-future dates — date trap, flagged.** Plus 219,503 small-business research awards + 125 science-foundation sample rows (8% dup).
- **Small-business loans** — attached to borrower businesses — 2,174,502 regular + 968,524 pandemic loans — counted in the two loan tables (Aug 11 scan).
- **Mortgage applications** — attached to lenders/census tracts — 19,136,434 historic + 28,301 recent + 17,474 loan-detail rows — each counted in its own table (Aug 11 scan).
- **Bank branch deposits** — attached to bank branches — 2,823,000 — counted (Aug 11 scan); **exactly round — probable cap.**
- **Disaster-aid registrations** — attached to households — 3,080,000 — counted (Aug 11 scan); **exactly round — probable cap.**
- **Government daily cash flows** — 478,149 deposit rows + 7,490 receipt rows + small debt tables — each counted (Aug 11 scan).
- **Political ad spending (one platform)** — attached to advertisers — 914,251 rows across three spend tables — counted (Aug 11 scan).
- **Lobbying spending on individuals (Texas)** — attached to lobbyists → officials — 38,662 expenditure rows + ~21k gift/food/event rows — counted (Aug 11 scan).

## Courts & justice

- **Court cases (dockets)** — attached to courts — 71,677,647 — counted rows in the national docket table (Aug 17 scan); docket IDs verified ~unique, and 100.0% match to the 3,361-court roster (Aug 17 batch check).
- **Case citations** — attached to opinions — 18,123,788 — counted (Aug 17 scan); 7.8M distinct cited opinion clusters underneath.
- **Court opinions (clustered)** — attached to dockets — 10,070,727 — counted (Aug 17 scan); references 9.9M distinct dockets.
- **Federal case outcomes (research file)** — attached to courts — 10,857,396 civil + 6,965,441 bankruptcy + 6,299,908 criminal — each counted in its own table (Aug 11 scan). A 10,323,280-row linked copy joins these to dockets — counted Aug 17; **overlaps the civil file, don't sum.**
- **Judge financial disclosures** — attached to judges — 66,287 filings — counted (Aug 11 scan); the money chain beneath (1.9M investment lines, 33,472 reimbursements, 2,025 gifts) counted in fresh Aug 17 scans, 99.4–99.8% verified linkage to judges. **Stale: newest disclosure is 2023-08 — likely source-side lag.**
- **Supreme Court justice votes** — attached to justices — 83,644 — counted rows in the courts database (Aug 11 scan).
- **Multistate settlements / false-claims settlements** — 882 + 12 — counted in the two settlement tables (Aug 11 scan).
- **Immigration court cases** — attached to immigrants — 12,631,225 — counted (Aug 11 scan).
- **Fatal police encounters** — attached to people killed — 10,430 — counted rows in the fatal-force tally (Aug 11 scan).
- **County incarceration measures** — attached to counties — 128,507 county-year rows — counted (Aug 11 scan).
- **Ransomware attacks** — attached to victim companies — 30,661 victim posts — counted (Aug 11 scan).
- **Crime victimization sample** — 1,000 rows — counted (Aug 11 scan); **exactly round — a capped sample.**

## Health & safety harm

- **Drug adverse-event reports** — attached to drugs/patients — 37,400,547 rows across four case tables (reactions 20.6M, indications 9.8M, demographics 5.8M, outcomes 1.1M) — each counted (Aug 11 + Aug 17 scans). **Trap: the reactions table is 76% exact-duplicate rows — real reaction count nearer 5M.** Distinct cases ≈ the 5.8M demographics rows.
- **Medical-device adverse events** — attached to devices — 2,743,561 — counted (Aug 11 scan).
- **Consumer-product injuries (ER sample)** — attached to products — 9,794,971 — counted (Aug 11 scan); **carries the far-future-date trap.**
- **Consumer finance complaints** — attached to financial companies — 17,168,287 — counted (Aug 11 scan).
- **Vehicle safety complaints** — attached to vehicles — 2,227,941 — counted (Aug 11 scan); 334k rows have literal placeholder text where the vehicle ID should be.
- **Vehicle recalls** — attached to vehicles — 242,993 — counted (Aug 11 scan). Drug recalls 17,816, device recalls 39,635 — each counted in its own table (Aug 11 scan).
- **Malpractice & disciplinary reports** — attached to practitioners — 1,911,185 — counted rows in the practitioner data bank (Aug 11 scan).
- **Nursing-home deficiencies** — attached to nursing homes — 418,479 health + 200,030 fire-safety — counted in the two deficiency tables (Aug 11 scan). Penalties: 16,180 rows counted alongside.
- **Nursing-home resident assessments (frequency)** — attached to facilities — 31,403,215 rows — counted (Aug 11 scan); pre-summarized measure rows, not individual assessments.
- **Dialysis facility quality rows** — attached to facilities — 12,456,456 — counted (Aug 11 scan); **one row is facility-by-measure, not a facility.**
- **Overdose death statistics** — attached to counties — 83,790 rows — counted (Aug 11 scan); statistical rows, not individual deaths.
- **Disease case counts (weekly)** — 1,932,840 rows — counted (Aug 11 scan); jurisdiction-by-disease-by-week counts.
- **Provider exclusions from federal programs** — attached to providers — 83,369 + 167,928 contractor exclusions — counted in the two exclusion lists (Aug 11 scan).
- **Provider license-mask warning** — the provider registry's license column carries 9.6M masked values — from the Aug 17 sentinel check, receipt in the fill file.

## Workplace, mines, transport

- **Mine safety violations** — attached to mines — 3,087,265 — counted (Aug 11 scan).
- **Mine accidents** — attached to mines — 273,623 — counted (Aug 11 scan).
- **Workplace injury summaries** — attached to employers — 890,934 (2023) + 688,649 (2024) — counted in the two annual tables (Aug 11 scan). **The OSHA inspections staging view is broken** — its raw table vanished (probable re-pull under a new name).
- **Railroad casualties** — attached to railroads — 1,150,788 — counted (Aug 11 scan).
- **Rail crossing incidents** — 251,149 — counted (Aug 11 scan). Equipment accidents: 224,941 rows, one per reporting-railroad-per-accident — the same accident repeats.
- **Aviation accidents** — attached to aircraft — 30,968 events + 31,503 aircraft-involved rows + 179,179 injury rows — each counted in its own table (Aug 11 scan).
- **Ship position pings** — attached to vessels — 58,104,610 — counted rows in the vessel-tracking dump (Aug 11 scan); known trap: the hull-ID column is ~56% placeholder text.
- **Union financial filings** — attached to unions — 33,484 pension filings + 41,802 actuarial schedules — counted (Aug 11 scan); **the big pension filing family carries the epoch-1970 date trap (589k rows).**

## Environment: violations, enforcement, inspections

- **Drinking-water violations (with enforcement)** — attached to water systems — 15,432,737 — counted (Aug 11 scan).
- **Water-permit compliance history (quarterly)** — attached to permit holders — 7,951,656 — counted (Aug 11 scan).
- **Hazardous-waste violations** — attached to sites — 708,114 + 2,675,581 violation-history rows — counted in the two tables (Aug 11 scan).
- **Water-discharge violations** — attached to permit holders — 397,615 + 305,478 (two violation types) — counted (Aug 11 scan); all seven water-event tables verified 100.0% linked to the permit roster (Aug 17 batch check).
- **Air violations history** — 102,037 — counted (Aug 11 scan).
- **Environmental enforcement actions** — attached to facilities — 478,855 informal + 112,373 formal (water), 175,736 informal + 106,009 formal (air), 383,519 hazardous-waste enforcements — each counted in its own table (Aug 11 scan).
- **Environmental inspections** — attached to facilities — 1,900,067 water + 260,556 fee-related + 1,166,410 hazardous-waste evaluations + 1,779,096 air compliance evaluations + 620,302 stack tests + 2,495,249 drinking-water site visits — each counted in its own table (Aug 11 scan).
- **A "penalty gap" screen** — 93,808 facility rows meeting a penalty-anomaly rule — counted (Aug 11 scan); a built screen, not raw events.
- **Pollution/spill release calls** — 1,029,020 — counted rows in the national-response-center log (Aug 11 scan); plus 116,662 incident-report rows.
- **Air emissions measurements** — attached to facilities — 10,411,826 — counted (Aug 11 scan); plus 346,683 greenhouse-gas emission rows.
- **Water measurements** — 6,694,816 stream-gauge readings + 927,415 lead/copper samples — counted (Aug 11 scan).
- **Storm events** — 1,780,730 — counted (Aug 11 scan). Earthquakes: 443,274 — counted (Aug 11 scan). Weather-station sample: 287. Global-hazard sample: 12.
- **Environmental-defender killings** — attached to people — 232 — counted (Aug 11 scan).
- **Fracking chemical disclosures** — attached to wells — 7,200,550 ingredient-line rows + 248,835 disclosure-list rows + 23,747 water-source rows — each counted (Aug 11 scan); one row is an ingredient line, not a well.

## Immigration

- **Detention stints** — attached to detention facilities — 2,571,975 — counted (Aug 11 scan); verified 100.0% linked to the 1,470-facility roster (Aug 17 batch check).
- **Detainer requests** — 609,769 — counted (Aug 11 scan); **carries the far-future-date trap.**
- **Foreign-labor certifications** — attached to employers — 664,616 — counted (Aug 11 scan).
- **Border encounter stats** — 9 summary rows — counted (Aug 11 scan); effectively empty.
- **Two immigration stat tables poisoned by duplicates** — 3,204 rows at 94% dup and 50,740 rows at 77% dup — counted (Aug 11 scan); **treat both as ~unusable until deduped.**

## Filings, registrations, licenses

- **Corporate insider-trade filings** — attached to companies/insiders — 1,772,088 filings, 2,672,841 open-market transaction rows, 1,049,121 derivative-transaction rows — each counted in its own table (Aug 11 scan).
- **Quarterly institutional-holdings filings** — 3,822,885 + a 336,124-row second load — counted (Aug 11 scan); the holdings themselves (101M rows ×2 twin tables) sit in the relationships section below.
- **Company financial-statement filings** — ~174,078 rows across four filing-index tables + ~60k quarterly submission rows across eight quarter tables — each counted (Aug 11 scan).
- **Nonprofit e-filing index** — 5,544,626 — counted (Aug 11 scan); **stale — newest entry 2020-01-28; also 3.2M epoch-date rows.**
- **Federal lobbying filings** — attached to lobbying firms/clients — 174,871 — counted (Aug 11 scan); **known short load: coverage stops 2021, roughly 9% of the real total.**
- **Foreign-agent registrations** — 48,104 — counted (Aug 11 scan).
- **State lobbying filings** — California: 524,828 + 206,493 cover rows + 85,765 change-log rows; Texas: 283,803 cover rows + 209,957 subject rows + 1,207 docket lines — each counted in its own table (Aug 11 scan).
- **Dark-money (527) money reports** — 55,579 — counted (Aug 11 scan).
- **Broadcast/spectrum licenses** — attached to companies — 1,689,338 — counted (Aug 11 scan); known trap: its employer-tax-ID column is fully masked — unusable as a join key.
- **Medicare facility enrollments** — ~57,767 rows across six facility-type tables — counted (Aug 11 scan).
- **Single audits of federal-money recipients** — attached to grantee orgs — 411,638 — counted (Aug 11 scan).
- **Utility annual filings** — ~5,001 rows across five report tables + 1,724 short forms + 3,412 frame rows — counted (Aug 11 scan); one frame table's column headers were destroyed at load.
- **Housing subsidy contracts & commitments** — 24,309 rent-subsidy contracts + 25,557 loan commitments + 35,601 assisted-housing project rows (8% dup) — each counted (Aug 11 scan).

## Politics: votes & bills

- **Congressional roll-call votes** — attached to members — 945,523 member-vote rows over 3,364 roll calls + 113,512 roll-call metadata rows — each counted (Aug 11 scan). **Standing issue: this vote mart disagrees with its independently-built twin — under repair.**
- **UN General Assembly votes** — attached to countries — 1,823,352 — counted (Aug 11 scan).
- **Bills & cosponsorships** — 36,465 bills + 367,735 cosponsor rows — counted (Aug 11 scan).
- **Election-administration survey** — 6,460 jurisdiction rows — counted (Aug 11 scan).

## Measurements & statistics (event-shaped numbers about the world)

- **County employment/wages panel** — 3,619,437 county-industry-quarter rows — counted (Aug 11 scan).
- **House-price index** — 184,807 rows — counted (Aug 11 scan).
- **Food-security stats** — 279,470 + 735 rows — counted (Aug 11 scan).
- **Interest/suicide/inequality series** — 16,848 + 6,390 + 4,961 + 2,389 rows — each counted in its own series table (Aug 11 scan).
- **Web-archive captures** — 1,537,352 + 24,897 rows — counted (Aug 11 scan); scrape bookkeeping as much as evidence.
- **Historical slave voyages** — 36,108 transatlantic + 11,521 intra-American — counted (Aug 11 scan). Historical-archive samplers: ~279 rows across four collections.
- **Missile-test trackers** — 340 + 303 rows, two databases — counted (Aug 11 scan).
- **Foreign-influence operations tracker** — 153 — counted (Aug 11 scan).
- **AI incidents (annual)** — 14 — counted (Aug 11 scan).

---

# RELATIONSHIPS (who's tied to whom — not asked for, but too big to hide)

- **Institutional stock holdings** — investor ↔ company — 101,261,252 rows, **loaded twice under two names (202.5M rows total)** — counted (Aug 11 scan).
- **Offshore-leaks relationships** — entity ↔ officer/intermediary — 3,339,267 — counted (Aug 11 scan); **3.3M rows carry far-future dates — trap.** Corporate-parent links: 484,142 (Aug 11 scan).
- **Doctor ↔ facility affiliations** — 2,260,193 — counted (Aug 11 scan).
- **Case-summary snippets (courts)** — 6,408,887 — counted (Aug 17 scan).
- **EPA program links + corporate crosswalk** — 4,406,498 + 5,300,149 — counted (Aug 11 scan); the corporate crosswalk measured 98.6% unmatched/fuzzy — kept as an overlay, never a spine merge.
- **Everything else in this class** — 29 link families, 230.3M rows total — summed from the same census fill; full list on request.

# WHAT'S DELIBERATELY NOT LISTED (so nothing is silently dropped)

- **Code lists** (industry codes, species taxonomy, etc.): 28 tables, 12,468,103 rows — summed from the census fill.
- **Pre-summed aggregate tables**: 34 tables, 3,869,337 rows — summed from the census fill.
- **One unclassified table**: 705 rows.
- **9 tables the census couldn't classify at all** and **235 classified only by column shape** — their rows ARE included above under "unresolved" groupings where countable; the census file lists each by name.
- **674 tables state no grain** ("one row = one what") — for those, counts above are row counts only, and any line above that says "rows, not things" is flagging exactly this.

*Source of every number: the census fill table (one row per shelf table: rows, dates,
duplicate ratio, key health, and which scan produced it) at
`reports/census_grid_2026-08-12/fill/fill_tables.csv`, plus the thing-classification
map beside it. Verification receipts for the court/spine claims:
`fill/courtlistener_edges.json` and `fill/spine_batch_verification.jsonl`.*
