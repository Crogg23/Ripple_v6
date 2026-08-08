# Non-ID Blind Spot Recon — 2026-08-07

Companion to `dataset_source_recon_2026-08-05.md`. That census started from a literal
list of 747 identifier types (NPI, CIK, license numbers, etc.) and asked "where does
each one live in the public record." This document does the opposite: 8 independent
research passes went looking for valuable public datasets **without** starting from an
ID, using the methods an ID-first search structurally can't use — browsing an agency's
site page by page, browsing an open-data catalog's raw listing, borrowing the source
lists other journalism orgs (ICIJ, ProPublica, OCCRP, IRE/NICAR) already trust, and
following FOIA-release logs (MuckRock, watchdog archives, agency reading rooms).

## What this is

- A **first, non-exhaustive pass** at the complement of the ID-first census — the
  blind spot, not the whole map.
- A **relay of what 8 research agents actually found and verified in their own
  sessions**, organized and de-duplicated where obvious, but not independently
  re-checked by whoever compiled this document. Where a pass flagged something as
  unconfirmed/403'd/dead-end, that flag is carried through here as-is.
- Honest about thin patches: some passes (state ag/environment, borrowed ICIJ/
  ProPublica lists, MuckRock) came back deep and concrete. Others (state catalog
  browsing, j-school training-org lists) hit real paywalls and 403s and are reported
  thinner, not padded to look even.

## What this isn't

- Not exhaustive. 8 passes, not 25 domain agents like the ID-first sweep — this is a
  reconnaissance sample of the method, not full coverage of it.
- Not independently verified in this compilation step. No new fetches were run to
  re-confirm URLs; everything below is exactly what each pass's raw findings claimed,
  including their own dead-end/caveat language.
- Not deduplicated against Ripple's existing warehouse. A few items below almost
  certainly already exist in some form in the marts referenced in the repo's git
  status (CMS, EPA FRS/SDWA, Open Payments, CFPB HMDA, sanctioned vessels) — flagged
  where the source pass itself noticed the overlap, not verified against the actual
  dbt models here.
- Not a build plan or a recommendation to ingest anything. Pure research inventory.

---

## 1. By-agency deep dive — state insurance regulators (WA, OH, VT, WY)

**Method:** picked 2 large / 2 small state insurance regulator sites, live-fetched
each one page by page instead of searching for an ID. **Cross-state pattern:** none of
these datasets use a national identifier (NAIC code, CIK) as the surfaced key — always
company name or a state-internal docket/slug. Real content sits behind bot-hostile
403s (Ohio) and an entire document library sits behind Google Drive (Wyoming) — both
would silently defeat a naive crawler even though a human browser gets through fine.

| Dataset | URL | Format | Identifier | Investigative value |
|---|---|---|---|---|
| WA Market Conduct Exam Orders search | fortress.wa.gov/oic/consumertoolkit/search.aspx?searchtype=ord | Search tool, no bulk export | Company name + WA order # only | Enforcement orders back to 2010: cease & desist, fines, revocations, suspensions |
| WA Complaint Comparison Tool | insurance.wa.gov/complaint-comparison-tool | Search tool, no download | Company name only, deliberately not unified across underwriting brands | Per-company complaint counts vs. confirmed complaints vs. market share |
| WA Data Calls and Reporting hub | insurance.wa.gov/insurers-regulated-entities/data-calls-and-reporting | ~9 PDF submission forms | None — submission templates, not registries | Whole taxonomy of recurring regulatory data collections (fire loss, disaster, prior-auth, title insurer, etc.) |
| WA Long-Term Care Annual Reports | insurance.wa.gov/insurers-regulated-entities/market-conduct-and-oversight/long-term-care-annual-reports | PDF forms | None | 4 required LTC filings; unclear if OIC republishes aggregated results — flagged as possible dead end, not confirmed |
| WA Market Information Reports | insurance.wa.gov/about-us/reports/market-information-reports | PDF, prose/table | Company name only | Annual narrative on WA's largest insurers, market share, financials |
| WA OIC Annual Reports | insurance.wa.gov/about-us/reports/oic-annual-reports | PDF | None, agency-level | Whole-agency narrative enforcement/market stats |
| OH Complaint Ratios | insurance.ohio.gov/about-us/complaint-center/complaint-ratios | Static per-line PDFs | Company name only | Complaint-index score, top ~40-50 companies per line; newest indexed copies found were 2019 — possible staleness, needs manual check |
| OH Market Conduct Exam Reports | insurance.ohio.gov/companies/market-conduct | Full narrative PDF exams | Company-name folder path, not NAIC code | Exam reports by year/company |
| OH Market Conduct Annual Statement resource page | insurance.ohio.gov/companies/market-conduct/resources/market-conduct-annual-statement | N/A | N/A | Dead end at state level — data flows into NAIC's national system, not published by Ohio directly |
| OH Market Share Reports | insurance.ohio.gov/companies/product-regulation-and-actuarial-services/resources/marketsharereport | Unconfirmed | Unconfirmed | Confirmed to exist via search index; 404'd to automated fetch — real, unverified content |
| OH Unauthorized Assuming Reinsurer Lists | insurance.ohio.gov/wps/portal/gov/odi/about-us/divisions/risk-assessment/resources/unauthorized-assuming-reinsurer-lists | Likely PDF/table, unconfirmed | Company name only | Who's operating without reinsurance authorization in Ohio; 403'd to fetch bot (WAF-blocked) but indexed/real |
| VT Regulations, Orders, Bulletins, Market Conduct Exams hub | dfr.vermont.gov/view/regbul | Index | N/A | 403'd to fetch bot but real/indexed |
| VT enforcement order example (Progressive, docket #25-015) | dfr.vermont.gov/sites/finreg/files/regbul/dfr-order-docket-25-015-i-progressive.pdf | PDF | VT docket # + company name only | Narrative document, no clean joinable ID — the exact case type this recon targets |
| VT Financial Exam Reports | dfr.vermont.gov/industry/insurance/company-licensing/financial-exams | PDF, ad hoc filename slug | DFR's own filename slug, not externally joinable | Per-company financial exam reports (examples: Noetic Specialty Insurance, Delta Dental of VT) |
| VT Rates and Forms | dfr.vermont.gov/industry/insurance/rates-and-forms | N/A | N/A | Likely just hands off to the national SERFF system — portal-to-portal, not a direct dataset |
| VT Public Information page | dfr.vermont.gov/about-us/public-information | Contact info | N/A | Records officer contact; signals Vermont leans on direct/FOIA requests, structurally thinner than WA/OH |
| WY Companies hub | doi.wyo.gov/companies | Landing page | N/A | Central index to financial summaries, exams, reinsurers, Form A notices |
| WY Financial Summary Information | linked from doi.wyo.gov/companies | Google Sheets (~16 separate sheets) | Company name only | Per-year, per-line (Health/Life/P&C/Title) financial summaries, 2022-2025 confirmed |
| WY Domestic Insurer Exam Reports | linked from doi.wyo.gov/companies | PDF, paired with company's own response letter | Company name only | Rare paired document: regulator finding + company rebuttal, both public |
| WY Certified Reinsurers list | doi.wyo.gov/companies/certified-reinsurers | Google Sheets | Company name + rating, no NAIC code confirmed | Certified reinsurers w/ ratings, pending applications, rating requirements |
| WY Form A Notices | linked from doi.wyo.gov/companies | Google Sheets | N/A | Change-of-control filings — tracks who's trying to acquire a WY-licensed insurer |
| WY NAIC Filing Checklists | Google-Drive-hosted | PDF | N/A | Not data itself, but confirms WY's entire document library sits behind Google Drive |

**Dead ends this pass named honestly:** OH Market Share Reports and Unauthorized
Assuming Reinsurer Lists (real per indexing, blocked to automated fetch); WA LTC
annual report aggregates (filing requirement confirmed, public republication not
confirmed); VT Rates and Forms (likely a SERFF handoff, not a direct dataset).

---

## 2. By-agency deep dive — state agriculture/environment (IA, NC, WI, NE)

**Method:** same live-fetch approach, applied to state ag/environmental agencies.
Turned up a genuine structural finding of its own: Nebraska's environmental agency
renamed and re-platformed mid-transition, and the old domain (`dee.ne.gov`) now fails
TLS validation — an entire state agency's legacy URL space went dark, meaning anyone
else's old bookmarks or citations to Nebraska ag-runoff data are currently broken too.

| Dataset | URL | Format | Identifier | Investigative value |
|---|---|---|---|---|
| IA Licensed Companion Animal Facilities | data.iowaagriculture.gov/licensing_lists/animal_welfare/ | Filterable HTML table, 667 records | State license number (not federal APHIS) | Iowa's commercial breeder/kennel/dealer roster with enforcement-action flags |
| IA Licensed Meat & Poultry Plants | data.iowaagriculture.gov/licensing_lists/meatpoultry/ | HTML table, 277 plants | Plant Class code only (functional category, not joinable) | State-inspected plant universe, distinct from federal FSIS establishment list |
| IA Century and Heritage Farms Directory | centuryfarms.iowaagriculture.gov | Searchable table | None | Multi-generational farm ownership record since 1976 — land-consolidation baseline |
| IA Sensitive Crop / Apiary / Deer-Elk Registry (DriftWatch/BeeCheck) | iowaagriculture.gov/agricultural-diversification-market-development-bureau/sensitive-crop-registry | Map + partial paywall ($100/yr for CSV/shapefile export) | None — self-registered, no entity ID | Cross-reference against pesticide-drift complaints |
| IA Licensed Grain Dealers / Warehouses | data.iowaagriculture.gov/licensing_lists/graindealers/ and .../grainwarehouse/ | HTML table, 102+ records | State license number | Licensing/bonding backbone behind grain-elevator bankruptcies that wipe out farmers |
| IA Nutrient Reduction Strategy Dashboard | nrstracking.cals.iastate.edu/tracking-iowa-nutrient-reduction-strategy | Dashboard | None — county/watershed level | Only public accounting of whether Iowa's voluntary farm-runoff program is working |
| IA Historic Grain Reports | iowaagriculture.gov/agricultural-diversification-market-development-bureau/historic-grain-reports | Monthly PDF back to 1974 | None (market data) | Long clean price time series with no equivalent public source at this granularity |
| NC Animal Feeding Operations Facility Map + permit export | deq.nc.gov/cafo-map | Excel export | Permit-number-based (exact fields unconfirmed) | Current hog/poultry/cattle CAFO permit roster — spine of the lagoon/spray-field environmental-justice story |
| NC "Animal Operation Permits" ArcGIS layer (older) | data-ncdenr.opendata.arcgis.com/datasets/animal-operation-permits- | 404'd | N/A | Dead end — looks abandoned since Oct 2018, superseded by the cafo-map export above |
| NC Drinking Water Watch | pwss.enr.state.nc.us/NCDWW2/ | Search tool | PWSID (federal SDWIS ID) — genuinely joinable | 403'd to fetch tool but confirmed real/public; state violation/sample detail finer-grained than federal SDWIS extracts |
| NC Hazardous Waste Electronic Filing Search (Laserfiche) | edocs.deq.nc.gov/WasteManagement/Search.aspx | Search/preview/download, no login per DEQ | Unconfirmed | "Cookies not enabled" on fetch — real per DEQ's own documentation, not scriptable as tried |
| NC Specialized Waste Management GIS layers | data-ncdenr.opendata.arcgis.com | GIS layers | Mixed/unconfirmed | UST tanks, hazardous waste sites, manufactured gas plants, pre-regulatory landfills, brownfields — pre-Superfund sites that rarely have any federal ID |
| WI Dog Sellers & Dog Facility Operators list | mydatcp.wi.gov (ServiceDetails page) | License lookup | License-based, schema unconfirmed | Licensed breeders/dealers/shelters selling 25+ dogs/3+ litters a year |
| WI Data Breach Reports Database | datcp.wi.gov/Pages/Programs_Services/DataBreachDatabase.aspx | On-page searchable table | None — company name only, no bulk export confirmed | State-level breach-notification archive with company names attached (off-thesis for ag/env but novel) |
| WI Licensed Grain Dealers and Warehouse Keepers (static PDF) | datcp.wi.gov/Documents/LicensedGrainDealersAndWarehouseKeepers.pdf | PDF | License-based per statute | Dated "as of 8/3/2017" — likely stale; live version should come from MyDATCP license services instead |
| WI Commonly Requested Public GIS Data portal | gis-widatcp.opendata.arcgis.com | Shapefile/geodatabase | Varies by layer | County-level layers confirmed; portal catalog is JS-heavy, full list unconfirmed |
| WI MyDATCP license-category index | mydatcp.wi.gov (BrowseService page) | Excel-exportable per category | License-based per category | Umbrella of separate registries: pesticide applicators, farm-raised deer (CWD surveillance), fish farms, animal dealers, milk/dairy, vet licensure |
| NE Groundwater Quality Clearinghouse | clearinghouse.nebraska.gov | Explorer tools | Clearinghouse Number per well, links to DNR well registration | 1.6M+ groundwater samples, 200K+ nitrate results across 34,000 wells — likely largest state nitrate dataset in the country |
| NE Registered Groundwater Wells database | dwee-data.nebraska.gov/dynamic/Wells/Wells and nebraskamap.gov GIS layer | Data retrieval + GIS | Well registration number, cross-links to Clearinghouse | 250,000+ well records including geologic strata |
| NE SARA Title III / Tier II Chemical Storage Reporting search | deq-iis.ne.gov/tier2/ | Per-facility PDF lookup | Facility-based, not confirmed as stable numeric ID | EPCRA hazardous chemical storage/inventory reports; bulk export not confirmed |
| NE DWEE Permitted Facility Search (cross-program) | deq-iis.ne.gov/zs/permit/main_search.php | Search tool with a Download button (format unconfirmed) | Facility name/address based | Single cross-program permit index — livestock waste/feedlot permits alongside air/water/waste |

**Dead ends this pass named honestly:** old `dee.ne.gov` (cert mismatch, effectively
unreachable — agency moved to `dwee.nebraska.gov`); NC Laserfiche hazardous waste
search (blocked the fetch tool); NC Drinking Water Watch (403'd, not independently
verified field-by-field); NC older ArcGIS CAFO layer (404'd, abandoned since 2018); WI
and NC ArcGIS Hub catalog pages (JS-rendered, existence confirmed via search indexing
only, no verified full inventory).

---

## 3. Catalog browse — catalog.data.gov (federal) + California CKAN

**Method note worth keeping:** catalog.data.gov's on-page search is now a
client-rendered JS app and the old CKAN API 404s — the only way to browse the raw
catalog mechanically is its sitemap (110 shards, 548,742 dataset URLs), grepped by
slug keyword. California's `data.ca.gov` still runs classic CKAN with a live
`package_search` API, so state browsing worked cleanly there. Neither column-level
identifier presence nor overlap with Ripple's existing marts (CMS, EPA FRS/SDWA, CFPB
HMDA, sanctioned vessels, Open Payments) was independently verified — catalog metadata
only.

| Dataset | URL | Format | Identifier | Investigative value |
|---|---|---|---|---|
| Director of USC Center Pleads Guilty to Fraud | catalog.data.gov/dataset/director-of-the-university-of-south-carolina-center-pleads-guilty-to-fraud | Single HTML link to DOJ press release | None | Evidence that OIG offices dump one-off case narratives into data.gov as "datasets" — likely a whole undiscovered class, org by org |
| OIG Testimony — Contract Misconduct at NWS | catalog.data.gov/dataset/oig-testimony-on-investigationg-contract-misconduct-at-the-national-weather-service | PDF testimony | None | Direct revolving-door/procurement-capture lead, pre-written |
| FDA Warning Letters | catalog.data.gov/dataset/warning-letters (+ near-dupe listing) | Searchable portal | None — company/firm name only, no FEI/DUNS in catalog record | "Who's warned but not stopped" accountability set |
| Radiation-Emitting Product Corrective Actions and Recalls | catalog.data.gov/dataset/radiation-emitting-product-corrective-actions-and-recalls | Search tool | None — manufacturer/product name only | Niche FDA CDRH recall database most platforms skip |
| Consent Decrees / Proposed Consent Decrees | catalog.data.gov/dataset/consent-decrees, .../proposed-consent-decrees | CSV of case links | No persistent facility/company ID confirmed | Actual legal settlement text of EPA CAA/CWA cases; EPA itself calls this "a subset of national interest" — a coverage-gap finding in its own right |
| Bureau of Competition Civil Penalty Actions (FY96-19) + Bureau of Consumer Protection sibling | catalog.data.gov/dataset/bureau-of-competition-civil-penalty-actions, .../bureau-of-consumer-protection-civil-penalty-actions | CSV + data dictionary | No persistent company ID — name + case-page URL | 20+ years of FTC antitrust/consumer-protection penalties |
| Medicaid Fraud Control Units Annual Spending and Performance Stats | catalog.data.gov/dataset/medicaid-fraud-control-units-mfcu-annual-spending-and-performance-statistics | State rollup | State-level, no provider key | Measures enforcement capacity itself — "who's not even looking" layer |
| SSA ALJ Public Alleged Misconduct Complaints System | catalog.data.gov/dataset/administrative-law-judge-public-alleged-misconduct-complaints-system | N/A | N/A | Dead end — cataloged but marked non-public (PII/FTI), never released |
| SSA Fugitive Felon Fraud Operational Data Store (FODS) | catalog.data.gov/dataset/fugitive-felon-fraud-operational-data-store-fods | N/A | N/A | Dead end — same story, marked "cannot be provided to the public" |
| 21st Century Corporate Financial Fraud in the US, 2005-2010 | doi.org/10.3886/ICPSR37328.v1 (via catalog.data.gov, hosted on ICPSR) | Academic dataset | Company name + SEC enforcement-release linkage, no persistent CIK confirmed | ~10,000 public companies, fraud-confirmed vs. matched non-violators, linked exec-characteristics database; access needs free ICPSR account/data-use agreement |
| NYC DOB Disciplinary Actions | catalog.data.gov/dataset/dob-disciplinary-actions | Table | License-number-style fields — real join key | Missed by ID-first sweep because it's framed as a disciplinary-history table, not a "license registry" |
| NYPD Officer Disciplinary History — Charges / Summary | catalog.data.gov/dataset/nypd-officer-profile-disciplinary-history-charges, .../-summary | Table | Officer-level, no confirmed cross-agency ID | Individual-accountability layer for use-of-force/misconduct pattern |
| Seattle Police Disciplinary Appeals | catalog.data.gov/dataset/seattle-police-disciplinary-appeals | Table | OPA case number, local not cross-jurisdiction joinable | Shows not just discipline but how much gets appealed/overturned |
| CA Health Facilities State Enforcement Actions (+ LTC Citation Narratives resource) | data.ca.gov/dataset/health-facilities-state-enforcement-actions | XLSX/PDF/ACCDB + free-text narrative resource | State license number, narrative resource unkeyed | Inspector's actual write-up as the downloadable file, not just a code |
| CA Provider Suspended and Ineligible List (S&I List) | data.ca.gov/dataset/provider-suspended-and-ineligible-list-si-list | Table | Likely NPI/license-bearing, unverified column-level | State complement to federal LEIE exclusion list — different timeline/threshold |
| CA Retailers That Sold Tobacco to Underage Youth/Young Adults | data.ca.gov/dataset/retailers-that-sold-tobacco-to-underage-youth-and-young-adults | Table + narrative PDF, 1997-2018 | None — address-level at best | Retailer-level public-health compliance data |
| CA Water Rights Enforcement Actions / Violations / Complaints / Investigations (4 linked datasets) | data.ca.gov/dataset/california-water-rights-enforcement-actions (+ siblings) | Linked tables | Water rights ID — real but state-specific key | Complaint → investigation → violation → enforcement chain, different grain than EPA ECHO |
| CA Quarterly Provider Complaints | data.ca.gov/dataset/quarterly-provider-complaints | Table | None confirmed — plan name level | Provider-side complaints against health plans (since Jan 2019) — reverse direction of the usual patient-complaint sets |

**Honest gaps:** only two catalogs covered (federal + California) — a second state
catalog (NY Socrata, Texas) was confirmed reachable but not pursued in this pass;
California alone produced enough depth to make a second state feel redundant. Column-
level identifier presence was not verified inside any file, only catalog metadata.

---

## 4. Catalog browse — state open-data portals (CA, NY, TX, VA, PA)

**Method:** CKAN `package_search` and Socrata catalog APIs, which actually work for
raw browsing (generic web search surfaces almost nothing on these JS single-page
portals). Covered 5 states after Virginia underperformed; checked but skipped two
ArcGIS Hub portals (Arizona AZGeo, New Mexico Environment Dept) after confirming by
search that both are GIS-layer clearinghouses (boundaries/hydrology/imagery),
structurally document-poor for this angle.

| Dataset | URL | Format | Identifier | Investigative value |
|---|---|---|---|---|
| CA LTC Citation Narratives, 1998-2017 | data.ca.gov/dataset/health-facilities-state-enforcement-actions (CSV: `ltccitationnarratives19982017.csv`) | CSV, free text | None — CA-specific license number only, no CMS CCN link | Inspector's actual write-up of each LTC facility violation, 2012-2017; portal warns against Excel download (truncates text) |
| CA Health Facilities State Enforcement Actions, 1997-2024 | data.ca.gov/dataset/health-facilities-state-enforcement-actions | XLSX/PDF/ACCDB | CDPH-internal facility ID/license only | 27 years of facility-level enforcement history |
| CA Water Rights Complaints (EWRIMS) | data.ca.gov/dataset/california-water-rights-complaints | Table | Has `CID_NUMBER` — EWRIMS-internal, no meaning outside that one state system (flagged as near-miss, not clean) | Century-long complaint history against water-right holders |
| NY Enforcement Actions by JCOPE and predecessor agencies | data.ny.gov/d/vsmx-hgi8 | Socrata table | None — name field only | Named officials/lobbyists formally charged with violating state ethics law |
| NY OpenNY Reports (meta-index) | data.ny.gov/d/jabi-xxkk | 52-row index of PDF links | None | Directory of where actual narrative reports live across NY state government — a crawl target, not a dataset itself |
| TX Custodial Deaths Report | data.texas.gov/d/ypvi-69jj | Socrata table, 37,656 rows | None — no NPI, no resolvable case number | Every reported death in TX law-enforcement/jail custody since dataset began; named individuals — strongest single find of this pass |
| TX Waste Registration & Reporting Incoming Document Search Portal (TCEQ) | data.texas.gov/d/qnwp-dbpj | Live search index | None surfaced | Regulatory-filing tracking system exposed as an open dataset |
| TX OCS 1.1 Abuse/Neglect Child Fatalities, FY2016-25 | data.texas.gov/d/92um-beyd | Aggregated table, 1,645 rows | None | Aggregated (not case-level) confirmed abuse/neglect child-death counts by year/county/region |
| TX Emergency Response Spills — Reported Timeline (TCEQ) | data.texas.gov/d/dku4-zwmg (raw table `xagr-a3x2`) | Table | Internal Incident Tracking Number, system-internal only | Chemical/hazmat spill incident stream since 2015 |
| VA DJJ Data Resource Guides, FY2016-2024 (9 datasets) | data.virginia.gov/dataset/fy2024-data-resource-guide (+ per-year slugs) | XLSX dashboards | None | Statutorily-mandated annual juvenile-justice dashboards, not built for API querying |
| PA Kennel Inspections, 2003-current | data.pa.gov/d/6kvs-ck8u | Socrata table, 89,105 records | Has a License Number, PA-specific, not cross-referenceable | Two decades of facility-level welfare-inspection outcomes with a plain-text result field |
| PA Public Food Inspections, last 24 months by county | data.pa.gov/d/etb6-jzdg | Socrata table | Facility name/address only, no clean key surfaced | Rolling restaurant-inspection outcomes; narrow window, ages out |

**Dead ends/near-misses this pass named honestly:** NY "audit" keyword search on the
Socrata catalog API returns only unrelated NYSERDA energy-audit data — the real OSC
audit archive lives off-portal at osc.ny.gov/reports; VA keyword searches for
"restaurant inspection," "DBHDS," "eviction," and health-professions licensing
discipline all returned zero results; NY Bulk Storage Facilities and CA Community
Care Licensing Facilities both looked promising but turned out to carry real internal
program/license IDs, so excluded from the "no ID" claim; Virginia's portal overall
skewed toward re-posted federal HealthData.gov content and a hackathon-sourced
"Datathon 2025" org (flagged as not authoritative agency data).

---

## 5. Borrowed source lists — ICIJ / OCCRP / ProPublica

**Method:** pulled directly from each org's own methodology/data pages, GitHub repos,
and data-store archives — URLs fetched and verified live in that pass's session.

| Dataset | URL | Format | Identifier | Investigative value |
|---|---|---|---|---|
| ICIJ Offshore Leaks Database | offshoreleaks.icij.org/pages/data | CSV / Neo4j dump | None clean — name/address matching only | 810,000+ offshore entities across 6 combined leaks (Panama Papers, Pandora Papers, etc.) — the canonical shell-company/beneficial-ownership map |
| ICIJ FinCEN Files transaction data | icij.org/investigations/fincen-files/download-fincen-files-transaction-data | Zip of structured spreadsheets | Transaction/bank-pair level, no persistent public entity ID | 200,000+ structured records from 2,100+ leaked SARs, $2T, 1999-2017 |
| ICIJ International Medical Devices Database (Implant Files) | medicaldevices.icij.org | Database | Device/manufacturer name-based, not a clean cross-country ID | 120,000+ device recall/safety records from 46 countries |
| ICIJ Luanda Leaks | icij.org/investigations/luanda-leaks | Raw documents | None | 715,000 leaked documents on Isabel dos Santos's companies |
| ICIJ Cyprus Confidential | icij.org/investigations/cyprus-confidential | Raw documents | None clean | 3.6M documents, sanctions-evasion/Russia-money hub angle |
| ICIJ China Cables | icij.org/investigations/china-cables | Narrative documents | None | Leaked Xinjiang internment-camp operating manuals |
| ICIJ Uber Files | icij.org/investigations/uber-files | Raw documents | None | 18.69GB of internal Uber emails/records on lobbying-vs-regulator playbook |
| Pegasus Project | forbiddenstories.org/about-the-pegasus-project (OCCRP angle: occrp.org) | Reporting, not a downloadable table | Phone numbers exist as a key but target list never fully published | 50,000+ phone numbers selected for NSO spyware surveillance by government clients |
| OCCRP Aleph / data.occrp.org | data.occrp.org | Searchable meta-source | Varies wildly by underlying dataset (FollowTheMoney entity model) | 250+ public datasets across 180+ countries, a pointer to hundreds of foreign-country registries a US-centric census would miss entirely |
| OCCRP ID / Catalogue of Research Databases | id.occrp.org/databases | Directory | None — directory, not a dataset | Country-by-country index of 1,000+ source registries reporters actually use |
| OCCRP #29Leaks (Formations House data) | occrp.org/en/29leaks/about-the-data | Raw email/CRM dump | None | 131GB leak, shell-company-formation-industry internals; partially paywalled to vetted journalists |
| OCCRP Russian Asset Tracker | occrp.org/en/project/russian-asset-tracker | Published map | Name-matched, no clean ID | $19.8B in identified oligarch assets; frozen snapshot, stopped updating Aug 2022 |
| OCCRP Troika Laundromat | occrp.org/en/project/the-troika-laundromat | Leaked ledger data | None clean | 1.3M leaked transactions, 238,000 companies, $4.6B flagged flows |
| OCCRP Azerbaijani Laundromat | occrp.org/en/project/the-azerbaijani-laundromat | Leaked data | None | 16,000+ transactions, $2.9B, tied to named European politicians as recipients |
| The Daphne Project | en.wikipedia.org/wiki/The_Daphne_Project (via OCCRP network) | Loose collection of leads | None | Continuing murdered journalist Daphne Caruana Galizia's unfinished investigations; flagged as thin/soft lead, not a packaged dataset |
| ProPublica Nonprofit Explorer (Form 990) | projects.propublica.org/nonprofits, API at .../nonprofits/api | Free API, full-text/line-item extraction | EIN exists, but value-add is the PDF extraction itself | 1.8M+ digitized Form 990/990-PF filings since 2001 |
| ProPublica Documenting Hate | projects.propublica.org/graphics/hatecrimes (+ GitHub News Index) | Crowdsourced incident data | None | Built because no reliable federal hate-crime dataset exists |
| ProPublica/GitHub COMPAS Recidivism Risk Score Data | github.com/propublica/compas-analysis | sqlite (compas.db) | Case-level, county-specific only | The dataset behind "Machine Bias" — primary source for any algorithmic-bias-in-criminal-justice angle |
| ProPublica Credibly Accused Priests | projects.propublica.org/credibly-accused | Searchable list | None — name/diocese only | Clergy publicly named as credibly accused, compiled from diocese disclosures; no master registry exists to reconcile against |
| ProPublica Cook County Regional Gang Intelligence Database (snapshot) | projects.propublica.org/datastore/#cook-county-regional-gang-intelligence-database | Excel, 25,063 entries | None — that's the story | People added to a "gang" list with no charge/conviction required; database is being legislated out of existence — this snapshot may be the only surviving public copy |
| ProPublica Federal Air Marshal Misconduct Database | projects.propublica.org/datastore | 5,214 case records | None — no badge/employee ID | TSA air marshal misconduct/discipline, 2002-2012, FOIA'd |
| ProPublica Chicken Checker (poultry Salmonella testing) | projects.propublica.org/datastore | Table | Plant name/establishment number — worth checking overlap with FSIS establishment IDs Ripple may already have | Plant-level Salmonella test results, 2000-2020, FOIA'd from USDA |
| ProPublica Commander's Emergency Response Program (CERP) Data | projects.propublica.org/datastore | Table | None | US military cash payments to Afghan civilians, FOIA'd |
| ProPublica Bryan (TX) ISD OCR investigation emails | projects.propublica.org/datastore | Raw Mbox email files | None whatsoever | Purest "PDF/email dump nobody thought to search for" example in this whole census |

**Dead ends / overlaps this pass named honestly:** ProPublica Congress API/"Represent"
confirmed discontinued; ProPublica Dollars for Docs likely superseded by CMS Open
Payments data already in Ripple's warehouse per git status; ProPublica Surgeon
Scorecard/Prescriber Checkup are re-derivations of CMS Medicare claims data Ripple
likely already sources more directly, and Prescriber Checkup is unmaintained;
ProPublica Nursing Home Inspect may be genuinely new (no nursing-home mart visible
yet) but needs an overlap check against the underlying CMS data first; West Africa
Leaks is not a new dataset, just a regional re-analysis of Offshore Leaks/Panama
Papers/Swiss Leaks already covered above; an OCCRP wildlife-trafficking "database"
could not be confirmed to exist — what surfaced was an unrelated academic paper,
treated as a genuine dead end.

---

## 6. Borrowed source lists — J-school / IRE-NICAR training orgs

**Method:** IRE/NICAR's own library, ProPublica's Data Store (cross-checked against
Section 5 for overlap), the Data Liberation Project, and academic data-journalism
libguides. This pass hit the heaviest paywall/403 rate of the eight.

| Dataset | URL | Format | Identifier | Investigative value |
|---|---|---|---|---|
| NICAR Data Library — FDA MAUDE | ire.org/nicar/database-library/databases/medical-device-reports-maude (live source: accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/search.cfm, open.fda.gov/data/maude) | ~3M reports, free-text narrative field | MDR report number is a record ID, not an entity key; manufacturer is free-text | Narrative "memo" field describing what happened — the NICAR copy is a stale 2013 snapshot ($ fee); live free version is openFDA |
| IRE & NICAR Federal Data Directory | ire.org/ire-nicar-federal-data-directory | Catalog, JS-loaded | Unknown per entry | Meta-index of federal datasets rescued/archived via DataRefuge; entry list itself needs a live browser visit to enumerate |
| IRE Resource Center "Data" product category | ire.org/product-category/resource/data | Paywalled tipsheets, $0-$100/item | N/A | Where NICAR conference "hidden gem dataset" tipsheets live — genuinely paywalled to non-members |
| ProPublica Credibly Accused Priests (duplicate of Section 5 #19) | propublica.org/datastore/dataset/credibly-accused-priests | List | None | ~6,700 clergy hand-compiled from ~180 diocesan disclosure lists |
| ProPublica Bryan ISD OCR Investigation Emails (duplicate of Section 5 #24) | projects.propublica.org/datastore | Mbox files | None | Same finding as Section 5 |
| ProPublica Interim COVID-19 Vaccine Distribution Plans | propublica.org/datastore/dataset/interim-covid-19-vaccine-distribution-plans | PDFs | None | Draft state/territory rollout plans submitted to CDC, Oct-Nov 2020 |
| ProPublica Commander's Emergency Response Program Data (duplicate of Section 5) | projects.propublica.org/datastore | Table | None | Same finding as Section 5 |
| ProPublica Defense Environmental Restoration Program Sites | projects.propublica.org/datastore | Oracle DB snapshot (2015), FOIA'd | Weak/none confirmed — internal DoD site codes | DoD's own military-site contamination cleanup database, no public API or clean facility ID |
| ProPublica Federal Air Marshal Misconduct Database (duplicate of Section 5) | projects.propublica.org/datastore | Table | None | Same finding as Section 5 |
| Data Liberation Project — USCG Boating Accident Report Database (BARD) | data-liberation-project.org/datasets/uscg-boating-accident-report-database | Raw MS Access files, FOIA'd | None documented | 58,430 accidents 2009-2023 (8,935 deaths, 36,773 injuries), never published as an open dataset |
| Data Liberation Project — NIOSH Commercial Fishing Incident Database | data-liberation-project.org/datasets/niosh-commercial-fishing-incident-database | FOIA'd, 157 columns | None — PII stripped | 3,559 person-level fatality/disaster records, one of the deadliest US industries, tracked only internally until this release |
| Data Liberation Project — EPA Risk Management Program Database | data-liberation-project.org/datasets/epa-risk-management-program-database | Raw FOIA release + DLP-built custom viewer | Uncertain — no standardized public facility ID confirmed | Chemical-accident-risk data for regulated facilities; DLP built its own viewer because no usable public tool exists |
| Data Liberation Project — PHMSA Hazmat Transportation Incident Reports | data-liberation-project.org/datasets/phmsa-hazmat-incident-reports | FOIA'd | Unconfirmed, likely weak (carrier name, not ID) | Hazardous-materials transportation incident reports |
| Data Liberation Project — DEA Theft/Loss of Controlled Substances | data-liberation-project.org/datasets/dea-theft-and-loss-counts | Spreadsheets | None documented | Pharma-supply-chain theft/loss data reported to DEA |
| NIOSH FACE Program (Fatality Assessment and Control Evaluation) | wwwn.cdc.gov/NIOSH-FACE (also archived at CDC Stacks) | 3,400+ full-text narrative PDFs since 1989 | None | The purest "narrative report, no ID" case: each report is a standalone writeup of one worker's death, never rolled into a structured national database |
| OSHA Severe Injury Reports | osha.gov/severe-injury-reports (bulk zip e.g. osha.gov/sites/default/files/January2015toNovember2025.zip) | Bulk zip, narrative + structured fields | Confirmed none — filter fields are Event Date/NAICS/City/State/Establishment Name, no company ID | Every employer-reported amputation, hospitalization, or eye loss since Jan 2015 — a strong, concrete match for the exact gap this recon is hunting |
| Investigative Reporting Workshop (American University) — The Accountability Project | investigativereportingworkshop.org | Unifying tool | None native — that's the point | A university newsroom's own attempt to patch the "no shared ID across siloed government data" problem — direct confirmation from inside a J-school that this is a known, named pain point |
| FOIA Mapper | foiamapper.com | Directory | N/A — directory of data, not a dataset | Knight-funded catalog of what record systems each federal agency actually holds internally |
| Bellingcat/Guardian "Attacks on Journalists" tracker | docs.google.com/spreadsheets/d/1F7Q-XoCoHzb_cX28ARCL4BMsuxp3EpkouUDJ2cRSjOQ | Crowdsourced Google Sheet | None | 140+ incidents against journalists during 2020 US protests, hand-built from news reports; cited in an active university course guide |

**Dead ends this pass named honestly:** Poynter has no maintained "recommended
datasets" list, defers to NICAR/ProPublica; journalistsresource.org's "Dataset digest"
403'd both attempts, unverified secondhand only; IRE Educators Center syllabi page
403'd; NICAR 2026 tipsheets page is JS-rendered ("Loading…"), couldn't extract the
actual tipsheet list; most university course GitHub repos (mattwaite JOUR407, Lede
Program) reference general categories in public READMEs, not specific niche datasets.

---

## 7. FOIA release logs — MuckRock archive

**Method:** live-fetched requests directly from muckrock.com by domain (housing,
environment, healthcare, labor, corporate accountability). Almost none of these carry
a clean join key — the identifier is usually a property address, a one-off case number
good for exactly one FOIA thread, or nothing at all.

| Dataset | URL | Format | Identifier | Investigative value |
|---|---|---|---|---|
| HUD Bad Landlord Complaints | muckrock.com/foi/united-states-of-america-10/hud-bad-landlord-complaints-5938 | 4,000+ pages of scanned PDF printouts | Property street address only | 10-year national tenant-complaint database against federal-housing landlords; HUD refused native format, took 4 years and a fee fight |
| HUD Complaints about Cambridge Housing Authority | muckrock.com/foi/united-states-of-america-10/hud-complaints-about-cambridge-housing-authority-25167 | Narrative PDF | None | Same complaint-line data as above, scoped to one housing authority |
| BSEED Inspection Reports (Detroit) | muckrock.com/foi/detroit-314/bseed-inspection-reports-212229 | Redacted PDFs | Street address only | Certificate-of-Compliance inspections for three named Detroit buildings |
| Lead Paint Notice of Violation / Stop Work Order / Inspection Logs (Oakland) | muckrock.com/foi/oakland-96/lead-paint-notice-of-violation-stop-work-order-inspection-logscity-of-oakland-138129 | Photos + redacted logs | Address + one-off local case number | Photographic/narrative proof of a lead-contamination enforcement action |
| Flint Water Contamination | muckrock.com/foi/united-states-of-america-10/flint-water-contamination-23514 | ~50,000+ pages: emails, reports, one audio file | None | EPA↔Flint/Michigan internal deliberation and cover-up communications, not sampling numbers |
| EPA Lead Paint Warning Letters — 262 Athol Ave, Oakland | muckrock.com/foi/united-states-of-america-10/epa-lead-paint-warning-letters-lead-disclosure-and-rrp-rule-137990 | Zip archive | Address only, tied to a non-reusable case number | EPA doesn't publish a searchable warning-letter archive; must know the address to ask |
| Semora Roxboro Plant (Duke Energy) Environmental Compliance and Inspection Records | muckrock.com/foi/north-carolina-153/semora-roxboro-plant-environmental-compliance-and-inspection-records-department-of-environmental-quality-197598 | Records release | Multiple state permit numbers, none shared with a national scheme | Cross-walks several disconnected state permit IDs together in one release — the cross-walk is the value |
| DOJ — Michigan COVID-19 Nursing Home Response Inquiry | muckrock.com/foi/united-states-of-america-10/doj-michigan-covid-19-nursing-home-response-inquiry-116623 | Narrative binder | None | Michigan's own internal self-defense narrative to a federal civil-rights inquiry |
| Nevada DOC Inspection and Health Reports | muckrock.com/foi/nevada-301/nevada-department-of-corrections-inspection-and-health-reports-nevada-department-of-corrections-206088 | Reports | None | Prison/jail facility inspection and health reports; no national corrections-health database exists |
| Inspections Jail (LA County Dept. of Public Health) | muckrock.com/foi/los-angeles-county-358/inspections-jail-212868 | Reports | None | County jail water/sanitation inspections, never surface in CMS or EPA data |
| "3 Deaths Later, ICE Puts CoreCivic in Charge of Healthcare at Stewart Detention Center" | muckrock.com/foi/united-states-of-america-10/3-deaths-later-ice-puts-corecivic-in-charge-of-healthcare-at-the-stewart-detention-center-immigration-and-customs-enforcement-ice-enforcement-and-removal-operations-ero-72901 | Password-protected zip, heavily redacted | None | Direct evidence of a privatization handoff at a facility with a documented death pattern; took ~3 years to obtain |
| Chaofeng Ge Death Records (ICE, Moshannon Valley) | muckrock.com/foi/united-states-of-america-10/ge-death-records-199919 | In litigation, not yet released | None | Named-detainee death-in-custody file; flagged honestly as unresolved/contested, not yet usable |
| Tobacco Farmworkers Complaints (OSHA), two sequential requests | muckrock.com/foi/united-states-of-america-10/tobacco-farmworkers-complaints-122480 (+ follow-up) | Spreadsheets | NAICS code (111910) — a real, if coarse, structured field | OSHA complaint stream for an undercovered agricultural workforce; not published in industry-filterable form otherwise |
| Wage Theft — "Home Healthcare" Complaints (Massachusetts AG) | muckrock.com/foi/massachusetts-1/wage-theft-content-of-home-healthcare-complaints-mass-ag-22869 | Single PDF | None | Wage-theft complaints against 11 named home-healthcare employers |
| Fair Labor Wage Theft Case Examples (Massachusetts AG) | muckrock.com/foi/massachusetts-1/fair-labor-wage-theft-case-examples-76077 | Narrative case docs, fee-gated ($37.50) | None | Four named wage-theft enforcement cases, including one utility with 3,000 underpaid workers |
| Civil Investigatory Demands (DOJ Antitrust, Aug 2022) | muckrock.com/foi/united-states-of-america-10/civil-investigatory-demands-antitrust-aug-22-134034 | Raw demand letters | None | Reveals which companies DOJ is quietly investigating before any public case exists — pre-public-record signal |

**Meta-finding (infrastructure, not a single dataset):** MuckRock's **FOIA Log
Explorer** (muckrock.com/foi/logs) indexes ~170,000 logged requests imported from
federal agency FOIA logs (EPA alone ~66,000) — a bulk-searchable index of what other
people have already asked for and gotten, a higher-leverage target than one-by-one
keyword search. MuckRock + POGO also archived ~34,000 documents / 110GB from the
shuttered FOIAonline (7 agencies) onto DocumentCloud — a static dump worth checking
for bulk ingestion.

**Dead ends this pass named honestly (MuckRock's own site search, zero results):**
"OSHA fatality," "meatpacking," "jail medical care" (exact phrase), "public housing
conditions," "consent order bank," "chemical plant explosion." Flagged as not proof
nothing exists in those domains — the search is keyword-literal, not semantic; a real
sweep would need per-agency and per-company query passes.

---

## 8. FOIA release logs — newsroom & watchdog archives beyond MuckRock

**Method:** surveyed independent-journalist FOIA clearinghouses, litigation-driven
watchdog archives, civil-liberties FOIA indexes, and official government reading
rooms, looking specifically for two things: raw document volume, and the rare cases
where a FOIA-built archive produced a real joinable identifier.

| Dataset | URL | Format | Identifier | Investigative value |
|---|---|---|---|---|
| The Black Vault | theblackvault.com/documentarchive | 3,861,432 pages (live counter) | None — agency-tagged only | Largest civilian FOIA clearinghouse in the world, run solo since 1996 |
| Bloomberg "FOIA Files" newsletter (Jason Leopold) | bloomberg.com/account/newsletters/foia-files | Weekly document drops | None | 13,000+ FOIA requests over two decades; partially paywalled behind a Bloomberg account |
| ProPublica "Free the Files" | projects.propublica.org/free-the-files | Crowdsourced, cross-posted to DocumentCloud | FCC call sign only, no cross-domain key | Confirmed dead end — frozen at Dec 2018 data, 2012 election cycle only, not maintained |
| American Oversight Requests & Records Archive | americanoversight.org/our-work/requests-records-archive | Filterable archive | Internal request number + agency tag, no universal ID | 10,000+ document sets, 1M+ pages since 2017 |
| CREW FOIA Requests archive | citizensforethics.org/reports-investigations/foia-requests/foia-requests | Chronological log, scroll-only | None | Back to 2020, request PDFs + agency + sometimes received records |
| Property of the People | (no independently verified stable URL this pass) | Unverified | Unverified | National-security FOIA specialist confirmed real via search, but no stable archive URL independently verified — flagged as needing direct verification |
| Judicial Watch | judicialwatch.org | Press releases about lawsuits, not a document archive | N/A | Dead end for a consolidated document library specifically; would need per-release scraping |
| National Security Archive (GWU) — Electronic Briefing Books | nsarchive.gwu.edu, nsarchive2.gwu.edu/NSAEBB | 900+ briefing books, 20,000+ annotated declassified documents | None, but each briefing book has a stable URL | 40+ years, 70,000+ FOIA/declassification requests; deep foreign-policy/intelligence/nuclear-history coverage |
| EFF FOIA document index | eff.org/document/index-foia-documents (hub: eff.org/foia) | Documents from ~200 requests + a dozen-plus lawsuits | None | FBI National Security Letter abuse, DHS Traveler Redress complaints, government-Google digitization contracts |
| ACLU Torture Database | thetorturedatabase.org | 100,000+ pages | None, though detainee names recur (name-based matching possible) | One of the deepest single-topic FOIA document sets on Guantánamo/Iraq/Afghanistan torture |
| CIA CREST / FOIA Reading Room | cia.gov/readingroom (unofficial full-text mirror: declassdb.com/crest) | 13M+ declassified pages; no bulk download on official site | None | Cold War/covert-action/sci-tech intelligence; official site is view-only, mirror allows full-text search |
| FBI Vault | vault.fbi.gov | ~7,000 scanned files | None, agency-curated topic tags only | Organized-crime, celebrity surveillance, UFO files |
| DOJ OIP FOIA Library | justice.gov/oip/available-documents-oip | Index of component reading rooms | N/A | Map-of-maps for the DOJ family, not a document set itself |
| State Department FOIA Library | foia.state.gov/FOIALIBRARY/FOIALIB2.aspx | Reading room | None | Includes Clinton-email release infrastructure, ongoing diplomatic-cable-adjacent logs |
| Invisible Institute — Citizens Police Data Project (CPDP) | invisible.institute/police-data | Database, expanding to a multi-state "National Police Index" (23 states) | Chicago PD officer star/badge numbers — genuinely joinable | 240,000+ misconduct allegations, 22,000+ individual officers, 1988-2023; the strongest proof-of-concept in this whole census that "narrative FOIA archive → structured ID-bearing dataset" is possible |
| TRAC (Syracuse University) | tracreports.org (note: moved off syr.edu domain Feb 2025, old URLs may 404) | Structured, queryable case/docket-level data | Real docket identifiers likely, though bulk/detailed access is partially paywalled | 30+ years of FOIA litigation vs. DOJ/DHS/IRS/ATF/DEA converted into queryable immigration-court, IRS, DEA, ATF enforcement datasets |
| DocumentCloud public catalog | documentcloud.org | Reported 1M+ documents (not independently confirmed this pass — page needs login/specific search URL to see totals) | DocumentCloud-internal doc ID only | Platform 1,300+ newsrooms use to host/annotate primary-source documents |
| MuckRock request archive + FOIA Log Explorer (cross-reference to Section 7) | muckrock.com/foi/list, muckrock.com/foi/logs | 120,690 total requests + ~170,000 log entries across 20 agencies | Internal MR-#### request number + agency/jurisdiction tag | Closest thing to a true index of FOIA releases across many newsrooms/requesters, not just MuckRock's own staff |

**Dead ends / adjacent-but-wrong-bucket this pass named honestly:** DDoSecrets
(ddosecrets.com) is real and large, but explicitly leaked/hacked material, not
FOIA-obtained — different legal chain of custody, likely wrong fit for a
defensible-provenance platform. Government Attic (governmentattic.org) is confirmed
real and frequently cited, but its internal listing pages 404'd on direct guessed
URLs and it uses an old frames-based layout resistant to deep-linking. Reporters
Committee's FOIA Wiki (foia.wiki) is a how-to-FOIA reference, not a document set, so
excluded from the list above.

---

## 9. Patterns across all 8 passes

**Domains that kept surfacing ID-less-but-valuable, across multiple independent
passes:** housing/landlord accountability (HUD complaint lines, lead-paint
enforcement — Sections 3, 7); immigration detention deaths and healthcare
privatization (Section 7); corrections/policing misconduct (Sections 3, 8 — with the
one clean-identifier exception being Chicago's CPDP badge-number system); state
insurance market-conduct enforcement (Section 1, entirely name-keyed across all 4
states checked); worker-safety narrative reports (OSHA Severe Injury Reports, NIOSH
FACE, Section 6 — both confirmed to carry zero entity ID by design); environmental
enforcement narratives tying together disconnected state permit numbers (Section 2's
NC CAFO data, Section 7's Duke Energy plant record). If Chris wants one sentence: the
places with the most human harm signal are consistently the places state and federal
agencies never bothered to give a joinable ID — that's not a coincidence, it's most of
why an ID-first sweep would miss them.

**Structural access traps that recurred across passes, independent of domain:**
JS-rendered single-page-app state/federal portals that a plain fetch can't see through
(ArcGIS Hub catalogs in NC/WI/AZ/NM, MuckRock and catalog.data.gov's own search UI,
several FCC/SEC tools referenced secondhand); entire document libraries hosted on
Google Drive or Google Sheets instead of the agency's own site (Wyoming's insurance
regulator, Section 1); site-wide bot-blocking of automated fetchers on real, indexed,
human-browsable content (Ohio insurance, Vermont DFR, NC DEQ's Laserfiche search); and
one outright agency identity crisis (Nebraska's environmental agency renamed and
re-platformed mid-transition, leaving the old domain TLS-broken and every old citation
to it dead).

**Which method was most productive vs. thinnest, read honestly:** the two by-agency
state deep-dives (Sections 1-2) and the borrowed ICIJ/ProPublica/OCCRP list (Section
5) came back the deepest and most concretely verified — live-fetching real agency
pages one by one, or trusting an established journalism org's own already-vetted
source list, both beat generic search. The state open-data catalog browse (Section 4)
was the thinnest of the eight — Virginia in particular returned zero results on
several plausible search terms and skewed toward re-posted federal data rather than
native state records, which is itself a finding (not every state catalog is equally
populated) rather than a failure of the method. The j-school/training-org pass
(Section 6) hit the heaviest paywall and 403 rate of any pass — IRE/NICAR's own
member-priced tipsheet archive and several JS-rendered syllabus/tipsheet pages
couldn't be read at all in this session.

**Overlap to dedupe before anyone acts on this:** the ProPublica Data Store appears in
both Section 5 and Section 6 with several identical entries (Credibly Accused Priests,
Bryan ISD OCR emails, CERP data, Federal Air Marshal Misconduct Database) — those are
the same underlying dataset found twice by two different passes, not four separate
finds. Section 8's MuckRock references are a deliberate cross-reference back to
Section 7, not a new find.

**Two genuine bridge candidates worth flagging on their own:** Invisible Institute's
CPDP (Chicago officer badge/star numbers) and TRAC's case/docket-level immigration and
federal-enforcement data (Section 8) are the only two sources across all 150+ raw
findings in this pass that were found via a non-ID discovery method but turned out to
carry a real, joinable identifier anyway — meaning they're candidates for actually
bridging into Ripple's entity spine, not just standalone narrative reference material.

**Honest limitations of this compilation, stated plainly:** this document relays what
8 independent research passes found and verified in their own sessions — it does not
re-fetch or re-verify any URL, does not check column-level identifier presence inside
any file beyond what each pass itself reported, and does not check any of these 150+
raw findings against Ripple's actual current dbt models (only against what each
individual pass happened to notice was probably already covered). Anything marked
"unconfirmed," "403'd," or "dead end" above is carried through exactly as the source
pass reported it, not independently re-tested. This is a first pass at a big
complement space, not a closed inventory.
