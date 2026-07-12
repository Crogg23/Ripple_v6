---
title: The Library
---

```sql totals
select
    count(*) as datasets,
    count(distinct shelf) as shelves,
    sum(row_count) as total_rows
from library.catalog
```

```sql shelves
select
    shelf,
    count(*) as datasets,
    sum(row_count) as rows
from library.catalog
group by shelf
order by rows desc
```

```sql catalog
select shelf, dataset, what_it_is, row_count, status
from library.catalog
order by shelf, dataset
```

The reading room of the Ripple Library — every dataset below is live in Snowflake,
landed and cataloged by the onboarding agent. This site reads the curated
`THE_LIBRARY` views. Pick a shelf, or search the card catalog.

<BigValue data={totals} value=datasets title="Datasets on the shelves" />
<BigValue data={totals} value=shelves title="Topic shelves" />
<BigValue data={totals} value=total_rows title="Rows across the reading room" fmt="#,##0" />

## First exhibits

A handful of datasets, straight off the shelves:

- [The national debt, daily since 2001](/national-debt) — Treasury's Debt to the Penny
- [Banned healthcare providers](/banned-providers) — the OIG exclusion list (LEIE)
- [Gun background checks](/gun-checks) — FBI NICS, monthly since 1998
- [Fatal police shootings](/fatal-force) — Washington Post Fatal Force database
- [Foreign agents](/foreign-agents) — FARA registrations by country represented
- [The Supreme Court](/scotus) — every case and vote since 1946 (SCDB)

## Shelves by volume

<BarChart
    data={shelves}
    x=shelf
    y=rows
    swapXY=true
    title="Rows per shelf"
    fmt="#,##0"
/>

## The card catalog

Every dataset in the reading room. `status = curated` means a typed, cleaned mart
sits behind the view; `raw` means the view still reads the as-landed text table
(numbers and dates in raw views need casting — the typed layer is being built out).

<DataTable data={catalog} search=true rows=25>
    <Column id=shelf />
    <Column id=dataset />
    <Column id=what_it_is title="What it is" />
    <Column id=row_count fmt="#,##0" />
    <Column id=status />
</DataTable>

<!-- BEGIN GENERATED BROWSE -->

## Browse all shelves

Every dataset in the reading room, auto-generated from the card catalog.

### Campaign Finance

- [Candidate Finance Summary](/candidate-finance-summary) — How much each federal candidate raised and spent per cycle -- the money-raised stat.
- [Fec Candidates](/fec-candidates) — Everyone who ran for federal office per the FEC -- 17,900 candidate-cycle records with party, office, and stat...
- [Fec Candidates Fed Fec Bulk Candidates](/fec-candidates-fed-fec-bulk-candidates) — Every federal candidate who filed with the FEC -- ID, office, party, state, incumbent or challenger.
- [Fec Candidate Committee Link](/fec-candidate-committee-link) — The bridge tying candidates to their campaign committees -- 16,229 links between CAND_ID and CMTE_ID.
- [Fec Candidate Committee Links](/fec-candidate-committee-links) — The official bridge tying FEC candidates to their committees -- which committee raises money for whom.
- [Fec Candidate Finances](/fec-candidate-finances) — Federal candidates' campaign money per cycle: total raised, spent, cash on hand, and debt.
- [Fec Committees](/fec-committees) — Every FEC-registered political committee (PACs, party, campaign) with type and affiliation.
- [Fec Committees 2026](/fec-committees-2026) — Every FEC-registered political committee for the 2026 cycle -- name, treasurer, type, linked candidate.
- [Fec Committees Fed Fec Bulk](/fec-committees-fed-fec-bulk) — Every federal political committee registered with the FEC for 2024 -- PACs, party orgs, campaign committees.
- [Fec Contributions By Committee And Cycle](/fec-contributions-by-committee-and-cycle) — FEC individual contributions rolled to recipient COMMITTEE (CMTE_ID) x CYCLE_YEAR.
- [Fec Contributions By State And Cycle](/fec-contributions-by-state-and-cycle) — FEC individual contributions rolled to contributor STATE x CYCLE_YEAR (calendar year of the transaction).
- [Foreign Agent Registrations](/foreign-agent-registrations) — FARA filings -- who's registered as an agent of a foreign government, for whom, and the money involved (30-row...
- [Individual Donations](/individual-donations) — The 84M-row firehose: every itemized donation individuals gave to federal committees. The rawest follow-the-mo...
- [Member Individual Donations](/member-individual-donations) — Where each member of Congress's individual donor money came from -- direct, earmarked, and self-funded.
- [Member Money Raised](/member-money-raised) — How much each member of Congress raised -- gross receipts, net, and cash on hand, by cycle.
- [Member Pac Money](/member-pac-money) — Per member of Congress, per cycle: PAC money raised and outside spending for and against them.
- [Member To Fec Id](/member-to-fec-id) — Bridge from a member of Congress to their FEC candidate ID, unrolled one row per ID.
- [Outside Spending](/outside-spending) — Money spent FOR or AGAINST candidates by outside groups -- who, how much, which side.
- [Pac Contributions To Candidates](/pac-contributions-to-candidates) — PAC and party money to (and spent for/against) federal candidates -- 867k transactions.

### Companies

- [Beneficial Ownership Registry](/beneficial-ownership-registry) — FinCEN beneficial ownership registry (1-row stub -- and domestic US companies were exempted in 2025).
- [Greek Companies](/greek-companies) — Heads up: 40-row sample of Greece's official company registry (GEMI) -- shape only, not the full country.
- [Intl Gleif](/intl-gleif) — Global registry of Legal Entity Identifiers (LEI) mapping companies and legal entities worldwide to standardiz...
- [Ireland Companies](/ireland-companies) — Irish CRO company register -- every registered company, status, type, address, NACE code.
- [Largest Us Companies](/largest-us-companies) — The 100 biggest US companies by revenue -- rank, industry, headcount, HQ.
- [Nonprofits By State And Ntee](/nonprofits-by-state-and-ntee) — IRS Business Master File (tax-exempt orgs) rolled to STATE x 501(c) SUBSECTION x NTEE_MAJOR (first letter of t...
- [Nonprofit 990 Filings](/nonprofit-990-filings) — Index of nonprofit Form 990 e-filings -- EIN, org name, tax year, revenue, assets (200-row probe).
- [Nonprofit Organizations](/nonprofit-organizations) — Every US tax-exempt organization -- 1.97 million nonprofits with EIN, type, and finances.
- [Nonprofit Revocations By State And Year](/nonprofit-revocations-by-state-and-year) — IRS automatic revocations of tax-exempt status rolled to org STATE x REVOCATION_YEAR.
- [Revoked Nonprofits](/revoked-nonprofits) — Nonprofits that lost their tax-exempt status -- 1.2M orgs the IRS auto-revoked, keyed by EIN.
- [Sec Edgar Filings](/sec-edgar-filings) — 49K SEC EDGAR filings -- company, ticker, form type, filing date, SIC code, and document links.
- [Sec Edgar Filings Api](/sec-edgar-filings-api) — Structured SEC filing metadata from the data.sec.gov API -- CIK, EIN, form type, dates (200-row probe).
- [Spain Company Filings](/spain-company-filings) — Spanish BORME company filings -- one row per registry act (company, act type, province, CVE, PDF).
- [Swiss Companies](/swiss-companies) — Heads up: thin 18-row sample of Switzerland's official company registry (Zefix) -- shape only, not the full co...

### Crime Security

- [Armed Conflict Events](/armed-conflict-events) — Every dated, mapped event of organized violence worldwide since 1989 -- 386K events with death tolls.
- [Europol Threat Reports](/europol-threat-reports) — Europol's SOCTA and IOCTA organized-crime and cybercrime threat assessments -- one row per published report.
- [Fbi Crime Incidents](/fbi-crime-incidents) — FBI Crime Data Explorer incident schema (1-row stub -- needs a real pour before it's usable).
- [Homicide Rate By Country](/homicide-rate-by-country) — Homicides per 100,000 people, per country per year (UN data) -- the global violence trend line.
- [North Korea Missile Tests](/north-korea-missile-tests) — Every North Korean missile test since 1984 -- date, missile, range, launch site, outcome.
- [North Korea Missile Tests Xc Nagix Dprk Missile Tests](/north-korea-missile-tests-xc-nagix-dprk-missile-tests) — Every known North Korean missile test -- date, missile, apogee, distance, and outcome.
- [Nuclear Warhead Stockpiles](/nuclear-warhead-stockpiles) — How many nuclear warheads each nuclear-armed country holds, year by year.
- [Ransomware Victims](/ransomware-victims) — Organizations worldwide hit by ransomware gangs -- victim name, gang, sector, country, date.
- [Terrorism Deaths](/terrorism-deaths) — Annual deaths from terrorism by country, from the Global Terrorism Database.

### Economy

- [Failed Banks](/failed-banks) — Every U.S. bank that has failed since 1934 -- when it collapsed, who bought it, and what it cost.
- [Famine Food Insecurity](/famine-food-insecurity) — How many people are in famine or emergency-level hunger, by country and analysis period.
- [Fed Bls Qcew](/fed-bls-qcew) — County-level quarterly and annual employment and wage statistics by industry (NAICS) and ownership sector, der...
- [Food Security Indicators](/food-security-indicators) — Chronic-hunger stats by country over 60+ years -- undernourishment and food-insecurity scales.
- [Global Food Agriculture Stats](/global-food-agriculture-stats) — FAOSTAT food and agriculture statistics (4-row stub -- raw content only, dead probe).
- [Illicit Financial Flows](/illicit-financial-flows) — GFI estimates of trade-related illicit financial flows by country and year (25 rows).
- [Income Inequality Gini](/income-inequality-gini) — The Gini index by country and year -- one number for how unequal each country's incomes are.
- [Italy Statistics](/italy-statistics) — 56,096 official Italian statistics -- economy, jobs, trade, population -- pulled from Istat's data feeds.
- [Pension Insurance Stats](/pension-insurance-stats) — 150K rows of PBGC pension insurance statistics -- claims, payments, and program finances by year.
- [Retirement Plan Filings](/retirement-plan-filings) — Form 5500 filings for 33K employer retirement and benefit plans -- sponsor, EIN, participants, and plan type.
- [Sec Company Tickers](/sec-company-tickers) — Every SEC-registered company mapped to its CIK number and stock ticker symbol.
- [Treasury Interest Rates](/treasury-interest-rates) — Monthly average interest rate the US government pays on its debt, by security type.

### Education

- [School Performance Data](/school-performance-data) — EDFacts K-12 school performance and enrollment data by state, district, and school (33-row probe).

### Elections

- [Election Administration Survey](/election-administration-survey) — The EAVS survey: how every US election jurisdiction actually runs voting -- registration, mail ballots, poll w...
- [Election Winners](/election-winners) — Who won every federal election -- office, year, state, vote share, and the margin over the runner-up.
- [House Election Results](/house-election-results) — Who won every US House race by district -- votes per candidate per district per year.
- [Presidential Results By State](/presidential-results-by-state) — Who got how many votes for president in each state, each election year.
- [Senate Election Results](/senate-election-results) — Who won every US Senate race, 1976-2024 -- votes per candidate per state per year.

### Energy Environment

- [Co2 Emissions Annual](/co2-emissions-annual) — Total annual CO2 emissions for every country, going back over two centuries.
- [Earthquake Hazard Model](/earthquake-hazard-model) — Global seismic hazard scores (PGA) by location from the GEM OpenQuake mosaic (12-row probe).
- [Electricity By Country](/electricity-by-country) — Yearly electricity generation, capacity, emissions, and demand for 200+ countries.
- [Environmental Defender Attacks](/environmental-defender-attacks) — Global Witness records of killings and attacks on land and environmental defenders worldwide, since 2012.
- [Fossil Fuel Energy Share](/fossil-fuel-energy-share) — Share of each country's primary energy that comes from fossil fuels, by year.
- [Global Temperature Anomaly](/global-temperature-anomaly) — How far each year's temperature ran above or below the historical baseline -- the climate-change line.
- [Mineral Production By Country](/mineral-production-by-country) — Global mineral commodity statistics -- production, reserves, and US import reliance by country, commodity, and...
- [Pollution Enforcement](/pollution-enforcement) — Every EPA-regulated facility -- inspections, violations, and fines, 3.2M sites.
- [Storm Events](/storm-events) — Every US severe-weather event -- deaths, injuries, property/crop damage, location -- 1.8M records.
- [Storm Events By State And Type](/storm-events-by-state-and-type) — NOAA Storm Events rolled to STATE x EVENT_YEAR x EVENT_TYPE.
- [Water Monitoring Readings](/water-monitoring-readings) — 6.7M sensor readings from USGS water monitoring stations -- streamflow, groundwater, and water quality by site...
- [Weather Alerts](/weather-alerts) — Active National Weather Service alerts -- event, severity, urgency, and affected area (287-row snapshot).

### Geography

- [Calendar Dates](/calendar-dates) — One row per calendar day (31,411 days) with year, quarter, month, weekday, and fiscal year.
- [Census Tracts](/census-tracts) — All 85,391 US census tracts with 2020 population and a center point -- the geographic backbone.
- [Egypt Statistics](/egypt-statistics) — Egyptian national statistics -- indicator, year, value (150-row probe).
- [Eurostat Indicators](/eurostat-indicators) — EU statistical indicators from Eurostat -- geo, time, value across domains (450-row probe).
- [Fertility Rate By Country](/fertility-rate-by-country) — Children born per woman, per country per year -- the birth-rate trend behind aging populations.
- [Global News Events](/global-news-events) — GDELT global news event records -- who did what to whom, where, per 15-minute news scan (1,015-row probe).
- [Historical Topo Maps](/historical-topo-maps) — USGS historical topographic map catalog -- title, date, and download links (250-row probe).
- [Tribal Lands Geo](/tribal-lands-geo) — Bureau of Indian Affairs geospatial records of tribal lands and boundaries (100-row probe).
- [Us Counties](/us-counties) — Every US county (3,222) with FIPS code, name, 2020 population, and center point.
- [Us States Reference](/us-states-reference) — The master list of US states and territories: FIPS code, postal abbreviation, and full name.
- [Zip To County Crosswalk](/zip-to-county-crosswalk) — A bridge from ZIP code areas to counties -- so ZIP-level data can roll up to the right county.

### Government

- [Appeals Judge Ideology](/appeals-judge-ideology) — Ideology score for every US Court of Appeals judge, by circuit -- how left/right they lean.
- [Bill Cosponsors](/bill-cosponsors) — 367K links between bills and the members of Congress who cosponsored them.
- [Bill Cosponsors Fed Govinfo Bill Cosponsors](/bill-cosponsors-fed-govinfo-bill-cosponsors) — Who cosponsored which bill in Congress -- 368K links between members and bills.
- [Congressional Bills](/congressional-bills) — Every bill in Congress -- sponsor, cosponsors, action history, and if it became law.
- [Congressional Rollcall Votes](/congressional-rollcall-votes) — Every recorded floor vote in Congress: what the question was, the yea/nay count, and whether it passed.
- [Congressional Rollcall Votes Fed Voteview Rollcall Meta](/congressional-rollcall-votes-fed-voteview-rollcall-meta) — Every recorded House and Senate roll-call vote -- date, question, bill, yea/nay counts, result.
- [Congress Bills](/congress-bills) — Every bill introduced in Congress: sponsor, subject, how far it got, and whether it became law.
- [Congress Committee Membership](/congress-committee-membership) — Who sits on and chairs each committee in Congress -- the map of who holds real power.
- [Congress Ideology Scores](/congress-ideology-scores) — A liberal-conservative score for every member of Congress, every Congress -- the DW-NOMINATE stat.
- [Congress Members](/congress-members) — The master list of every member of Congress with party, state, tenure, and ideology score.
- [Congress Members Fed Congress Legislators](/congress-members-fed-congress-legislators) — Every member of Congress, past and present, plus the ID crosswalk that links them everywhere.
- [Congress Member Id Crosswalk](/congress-member-id-crosswalk) — The Rosetta Stone linking each member of Congress across every ID system (FEC, ICPSR, Wikidata, etc.).
- [Congress Rollcall Votes](/congress-rollcall-votes) — Every recorded congressional vote, member-by-member -- 945K rows of how each one voted.
- [Congress Roll Call Votes](/congress-roll-call-votes) — 945,523 individual votes cast by members of Congress -- who voted yes, no, or abstained, per roll call.
- [Consumer Finance Complaints](/consumer-finance-complaints) — Consumer complaints about banks, lenders, and credit companies filed with the federal CFPB.
- [Corruption Perceptions Index](/corruption-perceptions-index) — Transparency International's yearly corruption score for each country (0 = worst, 100 = clean).
- [Country Freedom Scores](/country-freedom-scores) — Freedom House's yearly Free / Partly Free / Not Free grade for every country, with the sub-scores behind it.
- [Epstein File Manifest](/epstein-file-manifest) — A monthly index of every file the DOJ's Epstein Library lists publicly.
- [Fcc Licenses By State And Service](/fcc-licenses-by-state-and-service) — FCC ULS license records rolled to STATE x RADIO_SERVICE_CODE x LICENSE_STATUS x GRANT_YEAR.
- [Fcc Radio Licenses](/fcc-radio-licenses) — 1.7M FCC radio and wireless licenses -- call sign, licensee, status, grant and expiry dates.
- [Federal Judges](/federal-judges) — Every Article III federal judge since 1789 -- who appointed them, when, and their record.
- [Federal Judge Appointments](/federal-judge-appointments) — Every US federal judge's appointment -- who nominated them, the Senate vote, and when they left.
- [Federal Register Documents](/federal-register-documents) — US Federal Register documents -- rules, notices, proclamations, executive orders with agencies, citations, dat...
- [Institution Ideology Medians](/institution-ideology-medians) — Yearly left-right ideology score for the Supreme Court, every circuit, House, Senate and president since 1937.
- [Member Legislative Record](/member-legislative-record) — Each member of Congress's lawmaking scorecard -- bills sponsored, passed, and how far they got.
- [Member Voting Record](/member-voting-record) — Each member of Congress scored: how often they show up to vote and how often they toe the party line.
- [Military Spending By Country](/military-spending-by-country) — Military spending per country per year in constant USD (SIPRI data) -- the arms-race trend line.
- [Revolving Door Appointees](/revolving-door-appointees) — 406 federal appointees mapped to the industries they came from -- the government-to-industry revolving door.
- [State Cannabis Laws](/state-cannabis-laws) — State-by-year cannabis law details -- what each state approved and actually implemented, medical and rec.
- [Supreme Court Justice Ideology](/supreme-court-justice-ideology) — Ideology score for every Supreme Court justice by year, 1937-2022 -- how left/right they leaned.
- [Un Vote Agreement Pairs](/un-vote-agreement-pairs) — How often every pair of countries voted the same way at the UN General Assembly -- 1.8M pairs.

### Government Spending

- [Contracts By Agency And Naics](/contracts-by-agency-and-naics) — USASpending federal contract transactions rolled to AWARDING_AGENCY x NAICS_CODE (industry) x ACTION_YEAR.
- [Contracts By Agency And State](/contracts-by-agency-and-state) — USASpending federal contracts rolled to AWARDING_AGENCY x recipient STATE x ACTION_YEAR.
- [Federal Agency Budgets](/federal-agency-budgets) — The top 111 federal agencies with their budget, obligations, and actual outlays this fiscal year.
- [Federal Award Spending](/federal-award-spending) — Federal awards from the USAspending API -- contracts, grants, loans -- with recipient, agency, and dollars (30...
- [Federal Contracts](/federal-contracts) — Every federal prime contract award for FY2025 -- who got paid, how much, for what.
- [Fed Sba Ppp](/fed-sba-ppp) — Loan-level records of Paycheck Protection Program (PPP) loans of $150,000 or more, including borrower, lender,...
- [Foreign Aid Transactions](/foreign-aid-transactions) — 4M transaction-level US foreign assistance records -- who got aid money, from which agency, for what, by count...
- [Grant Opportunities](/grant-opportunities) — Federal grant opportunities listed on Grants.gov -- agency, category, eligibility, and status (100-row probe s...
- [Sba Loans By State And Program](/sba-loans-by-state-and-program) — SBA 7(a)/504 loan approvals rolled to borrower STATE x PROGRAM x approval fiscal year.
- [Sba Small Business Loans](/sba-small-business-loans) — 2.2M SBA 7(a) and 504 loans since 1991 -- borrower name, address, lender, and amount, released under FOIA.

### Health

- [Anxiety Depression Rates](/anxiety-depression-rates) — CDC survey estimates of Americans reporting anxiety or depression, by state, group, and time.
- [Cdc Health Indicators](/cdc-health-indicators) — 15K public-health indicator records from the CDC open data portal -- topic, place, year, value.
- [Cdc Mortality Queries](/cdc-mortality-queries) — CDC WONDER mortality/health query results (1-row stub -- needs a real pour).
- [Clinical Trials](/clinical-trials) — Registered clinical studies -- who sponsors them, the drug/condition, phase, and whether results were posted.
- [Cms Dataset Catalog](/cms-dataset-catalog) — Index of datasets on the CMS data portal -- title, publisher, update cadence, access URL (158 rows).
- [Dialysis Facilities](/dialysis-facilities) — Every Medicare dialysis center in the U.S. with quality, mortality, and infection stats.
- [Drug Acquisition Costs](/drug-acquisition-costs) — What pharmacies actually pay per unit for each drug (by NDC) -- the true-cost benchmark for the markup story.
- [Drug Overdose Deaths](/drug-overdose-deaths) — CDC provisional drug-overdose death counts by state, month, and drug type -- the epidemic in numbers.
- [Drug Overdose Death Rates By County](/drug-overdose-death-rates-by-county) — Drug-poisoning (overdose) death rates for every US county, year by year, from the CDC.
- [Drug Recalls](/drug-recalls) — FDA drug recalls: which product, made by whom, why it was pulled, and how dangerous it was.
- [Fed Cms Open Payments 2022](/fed-cms-open-payments-2022) — CMS Open Payments - General Payments Detail (PY2022)
- [Healthcare Providers](/healthcare-providers) — Every US healthcare provider with an NPI -- all 9.6M. The backbone of the health data.
- [Healthcare Shortage Areas](/healthcare-shortage-areas) — 166K HRSA designations of health professional shortage areas -- where the US lacks doctors, dentists, and ment...
- [Health Insurance Coverage](/health-insurance-coverage) — CDC estimates of how many Americans have health insurance, by state and demographic group over time.
- [Home Health Agencies](/home-health-agencies) — Every Medicare home health agency -- services, ownership, quality ratings.
- [Hospices](/hospices) — Every Medicare-certified hospice in America -- name, address, owner type.
- [Hospitals](/hospitals) — Every hospital in America -- type, ownership, ER, and overall star rating.
- [Hospital Cost Reports](/hospital-cost-reports) — Annual financial reports every Medicare hospital files: revenue, costs, beds, charity care, margins.
- [Hospital Price Transparency](/hospital-price-transparency) — Hospital standard-charge (price transparency) file schema (1-row stub).
- [Hospital Quality Ratings](/hospital-quality-ratings) — CMS Hospital Compare: 5,432 hospitals with type, ownership, emergency services, and quality designations.
- [Injury Violence Death Rates](/injury-violence-death-rates) — County-level death rates from injury, overdose, and violence (including guns), by intent.
- [Inpatient Rehab Facilities](/inpatient-rehab-facilities) — Every inpatient rehab facility in America -- name, address, owner type.
- [Life Expectancy](/life-expectancy) — Life expectancy at birth for every country, by year.
- [Long Term Care Hospitals](/long-term-care-hospitals) — Every long-term care hospital in America -- name, address, beds, owner.
- [Medicare Drug Prescribers](/medicare-drug-prescribers) — What every Medicare Part D prescriber wrote -- 1.4M providers, including opioid prescribing rates.
- [Medicare Facilities](/medicare-facilities) — Master file of every Medicare-certified facility -- beds, staff, services.
- [Medicare Providers By State And Type](/medicare-providers-by-state-and-type) — CMS Medicare provider utilization rolled to rendering-provider STATE x provider TYPE.
- [Medicare Provider Billing](/medicare-provider-billing) — What every Medicare provider billed and got paid, 1.3M rows -- follow the money by NPI.
- [Monthly Abortion Counts](/monthly-abortion-counts) — Monthly estimated abortion counts by US state, with low/high uncertainty bounds.
- [Nursing Homes](/nursing-homes) — Every Medicare/Medicaid nursing home: star ratings, staffing, inspections, fines, and abuse flags.
- [Nursing Home Watchdog Data](/nursing-home-watchdog-data) — LTCCC's compiled nursing-home data -- staffing, inspections, penalties, and ownership for 14.7K facilities.
- [Open Payments By Manufacturer And Nature](/open-payments-by-manufacturer-and-nature) — CMS Open Payments (industry payments to physicians/hospitals), 2022-2024 combined, rolled to paying MANUFACTUR...
- [Open Payments By Specialty And State](/open-payments-by-specialty-and-state) — CMS Open Payments 2022-2024 rolled to recipient SPECIALTY x PROGRAM_YEAR x recipient STATE.
- [Part D Prescribing By State And Type](/part-d-prescribing-by-state-and-type) — CMS Medicare Part D prescribers rolled to prescriber STATE x prescriber TYPE (specialty).
- [Pharma Meal Cap Gaming](/pharma-meal-cap-gaming) — Drug/device makers whose meals for doctors bunch suspiciously just under the $125 reporting cap.
- [Pharma Payments To Doctors](/pharma-payments-to-doctors) — Every payment drug and device makers gave doctors and hospitals in 2024 -- 15.4M records of industry money.
- [Pharma Payments To Doctors 2023](/pharma-payments-to-doctors-2023) — Every 2023 payment drug and device makers gave to US doctors and hospitals -- 14.7 million records.
- [Providers By Taxonomy And State](/providers-by-taxonomy-and-state) — NPPES national provider registry rolled to primary TAXONOMY_CODE x practice STATE x ENTITY_TYPE_CODE (1=indivi...
- [Provider Facility Links](/provider-facility-links) — Which doctors work at which facilities -- the NPI-to-CCN crosswalk, 2.2M links.
- [Suicide Death Rates](/suicide-death-rates) — US suicide death rates by year, age, sex and race from the CDC -- the national trend line.
- [Veteran Mortality Appendix](/veteran-mortality-appendix) — VA all-cause death figures for veterans, 2018-2023, as extracted from a report appendix.
- [Veteran Suicide Rates](/veteran-suicide-rates) — VA's official veteran suicide death counts and rates by sex, 2001-2023 -- a small summary table.

### History

- [American South Texts](/american-south-texts) — Full-text corpora from Documenting the American South -- slave narratives, Southern literature, church records...
- [Densho Incarceration Archive](/densho-incarceration-archive) — Densho's digital archive of Japanese American WWII incarceration -- photos, documents, and oral histories (25-...
- [Fed Slavevoyages Transatlantic](/fed-slavevoyages-transatlantic) — Voyage-level dataset of transatlantic slave trading expeditions, including ships, nationalities, ports, dates,...
- [Historical Map Collection](/historical-map-collection) — Metadata for digitized historical maps from the David Rumsey collection -- title, date, author, and IIIF image...
- [Intra American Slave Voyages](/intra-american-slave-voyages) — SlaveVoyages Intra-American database -- one row per documented voyage (ship, captain, owners, ports, dates, co...
- [Japanese Internment Records](/japanese-internment-records) — Records of Japanese Americans interned in WWII camps -- person, age, camp, county.
- [National Archives Records](/national-archives-records) — A catalog of high-value electronic records the National Archives put online -- military, diplomatic, personnel...
- [Slave Narratives 1936 1938](/slave-narratives-1936-1938) — First-person interviews with formerly enslaved Americans, recorded by the WPA in 1936-1938.

### Housing

- [Fed Fhfa Nmdb](/fed-fhfa-nmdb) — Aggregate statistics on new, outstanding, and performance characteristics of US residential mortgages drawn fr...
- [House Price Index](/house-price-index) — The official US house-price trend, free and keyless, down to the census tract -- the price side of affordabili...
- [Hud Dataset Catalog](/hud-dataset-catalog) — Index of HUD open datasets on huduser.gov -- what exists, where to get it (77 catalog rows).
- [Mortgage Applications](/mortgage-applications) — Loan-level HMDA mortgage records -- who applied, race/ethnicity/sex, census tract, and what happened (28K-row ...
- [Redlining Maps](/redlining-maps) — 1930s federal redlining grades (A-D) for ~200 US cities, with the racist reasons written down.

### Immigration

- [Border Encounters Monthly](/border-encounters-monthly) — CBP nationwide encounter totals in pivoted month columns (9 rows -- awkward shape, thin so far).
- [Border Enforcement Monthly](/border-enforcement-monthly) — 51K monthly DHS enforcement records -- CBP encounters, ICE arrests/detentions/removals, by citizenship and reg...
- [Foreign Worker Visa Applications](/foreign-worker-visa-applications) — 665K employer applications for foreign workers -- H-1B, PERM, H-2A/B -- with employer, job, wage, and outcome.
- [Ice Enforcement Stats](/ice-enforcement-stats) — ICE arrests, detentions, removals, and monitoring stats by quarter, country, and criminal history (221 rows).
- [Immigration Application Stats](/immigration-application-stats) — USCIS application volumes by form type -- receipts, approvals, denials, backlogs, and processing times (3,204 ...
- [Immigration Court Cases](/immigration-court-cases) — 12.6M immigration court case rows -- but only the case-type column landed. Big row count, thin substance; need...
- [Immigration Yearbook Tables](/immigration-yearbook-tables) — DHS Yearbook tables -- green cards, admissions, refugees, naturalizations by year and country (27 table-rows).
- [Refugees By Origin Country](/refugees-by-origin-country) — How many refugees fled each country each year -- the size of every displacement crisis over time.

### Investigations

- [Doj Archived Pages](/doj-archived-pages) — Raw: 2,542 archived Justice Dept web pages pulled from the Wayback Machine.
- [Doj Archived Page Snapshots](/doj-archived-page-snapshots) — 24,897 Wayback Machine snapshots of DOJ web pages -- an archive trail of what Justice published, and when.
- [Epstein Files Size History](/epstein-files-size-history) — A time-lapse of Epstein document pages: how many files each page held, snapshot by snapshot.
- [Epstein Files Tracker](/epstein-files-tracker) — A watch-list of Epstein-related document files: which ones exist, and when we first/last saw them.
- [Russian Operations Against Europe](/russian-operations-against-europe) — Catalog of Russian hybrid-warfare operations against Europe -- sabotage, spying, influence ops.
- [Web Page Changes](/web-page-changes) — 203K archived-webpage snapshots flagging when a page appeared, changed, or went dead.

### Justice

- [Ag Multistate Settlements](/ag-multistate-settlements) — NAAG multistate settlements -- one row per multistate AG settlement (defendants, amounts, participating states...
- [Appeals Judge Ideology Scores](/appeals-judge-ideology-scores) — Ideology scores for 703 federal appeals-court judges -- how liberal or conservative each one leans.
- [Australasian Case Law](/australasian-case-law) — AustLII/WorldLII legal database records (1-row stub -- schema probe only).
- [County Overdose Jail Burden](/county-overdose-jail-burden) — Every US county scored on two crises at once: drug overdose deaths and jail incarceration.
- [Doj Civil Rights Cases](/doj-civil-rights-cases) — Heads up: 1-row scrape stub of DOJ Civil Rights Division cases -- not the real dataset yet.
- [Echr Court Cases](/echr-court-cases) — European Court of Human Rights rulings: who sued which country, over what right, and who won.
- [Eu Legal Acts](/eu-legal-acts) — EU legal acts and case-law records from EUR-Lex -- CELEX ID, type, dates, and in-force status (53-row probe).
- [Fdic Enforcement Actions](/fdic-enforcement-actions) — Heads up: a thin 14-row scrape of FDIC enforcement orders against banks -- shape only, not the full source.
- [Federal Court Caseloads](/federal-court-caseloads) — US federal court caseload statistics tables -- filings, terminations, and pending cases by court (50 table-row...
- [Federal Judges](/federal-judges-federal-judges) — Every federal judge in U.S. history -- name, birth/death, gender, race -- the who's-who of the bench.
- [Federal Judge Appointments](/federal-judge-appointments-federal-judge-appointments) — Every federal judge appointment: who, which court, which president, and the confirmation vote.
- [Federal Prison Stats](/federal-prison-stats) — Bureau of Prisons aggregate statistics -- inmate population, staffing, and facilities (50 metric rows).
- [Fraud Settlements](/fraud-settlements) — DOJ False Claims Act settlements -- defendant, amount, qui tam / relator, fraud type, agency defrauded, distri...
- [Ftc Enforcement Actions](/ftc-enforcement-actions) — FTC enforcement actions and cases -- respondent, date filed, case type, and status (1,200 rows).
- [Government Ideology Medians](/government-ideology-medians) — By year: the ideological midpoint of the President, House, Senate, and Supreme Court on one scale.
- [Incarceration Trends By County](/incarceration-trends-by-county) — Jail and prison populations for every US county over time, broken out by race and sex.
- [Jail Racial Disparity By County](/jail-racial-disparity-by-county) — County-by-year jail rates by race -- how much more often Black residents are jailed than white ones.
- [Scotus Justices](/scotus-justices) — 40 Supreme Court justices with their terms and how many cases and votes they've cast.
- [Scotus Justice Ideology](/scotus-justice-ideology) — Each Supreme Court justice's ideology score (JCS/Martin-Quinn style) by term.
- [Supreme Court Cases](/supreme-court-cases) — U.S. Supreme Court cases: who argued, how each justice voted, the ruling, plus audio/transcripts.
- [Supreme Court Justices Crosswalk](/supreme-court-justices-crosswalk) — A bridge that ties each Supreme Court justice to their official federal-judiciary ID.

### Misc

- [Exploited Vulnerabilities](/exploited-vulnerabilities) — The US government's list of software flaws known to be actively exploited by hackers.

### Money

- [Bank Call Reports](/bank-call-reports) — Quarterly financial condition reports for US banks -- assets, deposits, loans, capital -- keyed on RSSD ID (30...
- [Country Debt Repayment](/country-debt-repayment) — How much each country owes each year in debt payments -- and which years are dangerous repayment spikes.
- [Credit Union Call Reports](/credit-union-call-reports) — 122K quarterly call-report records for federally insured credit unions -- the financial vitals, 1994 to presen...
- [Irs Income Stats By Zip](/irs-income-stats-by-zip) — IRS Statistics of Income by ZIP code -- returns filed, income brackets, and totals per ZIP (180K rows).
- [Sec Filing Submissions](/sec-filing-submissions) — Header details for company financial filings to the SEC -- who filed, when, and what form.
- [Sovereign Debt By Creditor](/sovereign-debt-by-creditor) — How much each developing country owes, and to whom -- World Bank external-debt panel, 1970-2032.

### Open Data

- [Argentina Open Data Catalog](/argentina-open-data-catalog) — Catalog of 3,556 datasets on Argentina's national open-data portal, plus time-series samples.
- [Brazil Open Data Catalog](/brazil-open-data-catalog) — Catalog sample from Brazil's national open-data portal (10 rows).
- [Doj Epstein Page Captures](/doj-epstein-page-captures) — Every archived snapshot of the DOJ Epstein document pages -- proof, by digest, of when the page changed.
- [France Open Data Catalog](/france-open-data-catalog) — Catalog of 2,765 datasets on France's national open-data portal -- title, publisher, license, freshness.
- [Georgia Open Data Catalog](/georgia-open-data-catalog) — Catalog stub from Georgia's (country) open-data portal (1 row).
- [Ghana Open Data Catalog](/ghana-open-data-catalog) — Catalog sample from Ghana's open-data portal (10 rows).

### Procurement

- [Asian Development Bank Projects](/asian-development-bank-projects) — ADB development projects and economic indicators for Asia-Pacific -- project, country, sector, loan amount (41...
- [Ecuador Gov Contracts](/ecuador-gov-contracts) — Ecuador's government contracts -- 133K records of who bought what, from which company, for how much.

### Sanctions

- [Eu Sanctions List](/eu-sanctions-list) — The EU's consolidated financial sanctions list -- 42K records of persons and entities under asset freezes.
- [Money Laundering Country Ratings](/money-laundering-country-ratings) — FATF ratings of every country's anti-money-laundering regime -- compliance and effectiveness, by recommendatio...
- [Sanctioned Parties](/sanctioned-parties) — The U.S. Treasury sanctions blacklist: every person, company, and ship Americans are barred from dealing with.
- [Sanctions Targets](/sanctions-targets) — Everyone and everything under sanctions worldwide -- 71K people, companies, and vessels, consolidated.

### Science

- [Ai Incidents Annual Count](/ai-incidents-annual-count) — Count of reported AI incidents and controversies per year -- one number a year, the trend line.
- [Earthquakes](/earthquakes) — Every recorded earthquake magnitude 2.5+ worldwide -- 443K events with time, place, and depth.
- [Genome Annotations](/genome-annotations) — Genome annotation records from Ensembl -- genes, variants, and features across species (643-row probe).
- [Nasa Api Samples](/nasa-api-samples) — Sample responses from NASA's open APIs -- imagery, asteroids, space weather (54 rows).
- [Nsf Research Grants](/nsf-research-grants) — NSF research awards -- who got funded, at which institution, for what, and how much (125-row probe).
- [Preprints](/preprints) — Biology and medical preprints from bioRxiv/medRxiv: authors, funders, and download counts.

### Spending

- [Hhs Grant Awards](/hhs-grant-awards) — HHS TAGGS grant awards -- award number, recipient (name/EIN/geo), amount, assistance-listing (CFDA) number.

### Transport

- [Aircraft Registry](/aircraft-registry) — The FAA registry of all 314K US civil aircraft -- N-number, owner name and address, make/model, registration d...
- [Faa Dataset Catalog](/faa-dataset-catalog) — Index of FAA public datasets (4-row stub).
- [Railroad Accidents](/railroad-accidents) — FRA railroad accident and incident records (1-row stub -- needs a real pour).
- [Ship Positions](/ship-positions) — 7.3M GPS pings from ships in US waters in 2024 -- where, when, how fast, and what they were carrying.
- [Transportation Data Catalog](/transportation-data-catalog) — Index of BTS TranStats transportation databases -- aviation, freight, rail, transit (21 rows).

<!-- END GENERATED BROWSE -->
