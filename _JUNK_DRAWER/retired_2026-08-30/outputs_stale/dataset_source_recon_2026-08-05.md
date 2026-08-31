# Dataset Source Recon — 2026-08-05

Research-only census of where the 747-candidate ID sweep's surviving 571 in-scope
candidates actually live in the public record. No downloads, no Snowflake, nothing
staged — this is a map of the acquisition surface, not a build. Queryable data is in
`dataset_source_recon_2026-08-05.csv` (one row per candidate, same 571 rows as here).

## 1. Coverage arithmetic

**Scope:** 747 total candidates from the exhaustive ID sweep, minus 138
restricted/legally-walled, minus 40 mapped to "likely already have" (Section 4 of
`exhaustive_id_sweep_synthesis_2026-08-05.md` — not re-listed here, that's a separate
Track-3 column-check task) = **571 in scope**. This is 2 higher than the ~569 estimate
in the original task brief: 2 candidates (FinCEN Identifier, CINS) sit on *both* the
restricted list and the likely-already-have list, so excluding them once each (not
twice) nets 571, not 569. Verified by parsing both source docs programmatically, not
by hand — the domain-table row count came back exactly 747 before any exclusions.

**Dispatch vs. return, per domain — 571/571, zero gaps, zero silent drops:**

| Domain | Dispatched | Returned | Missing | Critic-checked | Downgraded |
|---|---:|---:|---:|---:|---:|
| Agriculture & Food Safety | 24 | 24 | 0 | 5 | 4 |
| Banking & Depository Institutions | 18 | 18 | 0 | 12 | 4 |
| Consumer Protection & Product Safety | 25 | 25 | 0 | 22 | 9 |
| Corporate Registration & Beneficial Ownership | 29 | 29 | 0 | 20 | 3 |
| Criminal Justice & Court Systems | 13 | 13 | 0 | 10 | 2 |
| Education | 21 | 21 | 0 | 6 | 2 |
| Energy, Utilities & Pipeline Safety | 31 | 31 | 0 | 12 | 4 |
| Environment & Natural Resources | 29 | 29 | 0 | 23 | 2 |
| Federal Benefits & Safety Net / Veterans | 22 | 22 | 0 | 5 | 1 |
| Federal Procurement & Grants | 21 | 21 | 0 | 10 | 1 |
| Financial Crimes, Sanctions & AML | 20 | 20 | 0 | 14 | 5 |
| Healthcare & Clinical | 21 | 21 | 0 | 11 | 4 |
| Housing, Real Estate & Mortgage Lending | 30 | 30 | 0 | 17 | 1 |
| Immigration & Border | 19 | 19 | 0 | 10 | 4 |
| Insurance | 27 | 27 | 0 | 13 | 5 |
| International & Cross-Border Identifiers | 21 | 21 | 0 | 17 | 2 |
| Labor, Workplace Safety & Benefits | 19 | 19 | 0 | 6 | 1 |
| Law Enforcement & Corrections | 14 | 14 | 0 | 13 | 2 |
| Pharma, Biologics & Medical Devices | 31 | 31 | 0 | 14 | 2 |
| Politics, Elections & Lobbying | 20 | 20 | 0 | 10 | 1 |
| Science, Research Grants & Research Integrity | 30 | 30 | 0 | 24 | 1 |
| Securities, Investment Funds & Markets | 20 | 20 | 0 | 10 | 5 |
| Telecom & Media | 27 | 27 | 0 | 12 | 11 |
| Transportation -- Aviation & Rail | 29 | 29 | 0 | 17 | 3 |
| Transportation -- Motor Carrier & Maritime | 10 | 10 | 0 | 6 | 4 |
| **TOTAL** | **571** | **571** | **0** | **319** | **83** |

25 research agents, one per domain, each handed its literal ID list. Every domain
came back complete on the first pass — no re-dispatch was needed. 319 of the 571 rows
(56%) qualified for the critic pass (confirmed *and* claimed bulk-file-or-no-auth);
83 of those 319 (26%) got downgraded on re-check — see Section 5.

## 2. The board

**By confidence**

| Confidence | Count | Share |
|---|---:|---:|
| confirmed | 294 | 51.5% |
| inferred | 247 | 43.3% |
| not-found | 30 | 5.3% |

**By access shape**

| Access Shape | Count | Share |
|---|---:|---:|
| bulk-file | 216 | 37.8% |
| api-open | 47 | 8.2% |
| api-key | 17 | 3.0% |
| scrape-only | 240 | 42.0% |
| foia-only | 12 | 2.1% |
| none-found | 39 | 6.8% |

**By auth**

| Auth | Count | Share |
|---|---:|---:|
| none | 488 | 85.5% |
| free-key | 23 | 4.0% |
| paid | 15 | 2.6% |
| login | 45 | 7.9% |

**By size class** (labelled guesses where noted in the CSV; unknown means no basis for even a guess)

| Size Class | Count | Share |
|---|---:|---:|
| small (<10k rows) | 161 | 28.2% |
| medium (10k-1M) | 199 | 34.9% |
| large (>1M / streaming) | 162 | 28.4% |
| unknown | 49 | 8.6% |

**By domain**

| Domain | Count |
|---|---:|
| Agriculture & Food Safety | 24 |
| Banking & Depository Institutions | 18 |
| Consumer Protection & Product Safety | 25 |
| Corporate Registration & Beneficial Ownership | 29 |
| Criminal Justice & Court Systems | 13 |
| Education | 21 |
| Energy, Utilities & Pipeline Safety | 31 |
| Environment & Natural Resources | 29 |
| Federal Benefits & Safety Net / Veterans | 22 |
| Federal Procurement & Grants | 21 |
| Financial Crimes, Sanctions & AML | 20 |
| Healthcare & Clinical | 21 |
| Housing, Real Estate & Mortgage Lending | 30 |
| Immigration & Border | 19 |
| Insurance | 27 |
| International & Cross-Border Identifiers | 21 |
| Labor, Workplace Safety & Benefits | 19 |
| Law Enforcement & Corrections | 14 |
| Pharma, Biologics & Medical Devices | 31 |
| Politics, Elections & Lobbying | 20 |
| Science, Research Grants & Research Integrity | 30 |
| Securities, Investment Funds & Markets | 20 |
| Telecom & Media | 27 |
| Transportation -- Aviation & Rail | 29 |
| Transportation -- Motor Carrier & Maritime | 10 |

**Read of the shape:** more scrape-only (240) than clean bulk-file (216) — a lot of
this surface is "load a search/lookup tool," not "download a file." 85.5% need no
credential at all, which is the good news; the 7.9% behind a login skew toward
research-restricted federal microdata (ICPSR/NACJD, dbGaP, CMS RIF files) rather than
paywalls. Confidence split roughly half confirmed / half inferred, which is expected
for a one-pass shallow sweep at this scale — see the Honesty section for what that
means practically.

## 3. Source roll-up

571 candidate IDs resolve to **470 unique sources** (deduped by normalized URL —
host + path, query strings and fragments stripped; rows with no usable URL, i.e. the
"holes" in Section 4, are excluded from this count). **49 of those 470 sources carry
more than one candidate ID** — this is the real cost object: Ripple would be standing
up 470 new acquisitions at most, not 571, and less than that in practice since several
of the 470 are themselves fragmented state-level clusters counted once.

**Lower-bound footprint:** summing one conservative size floor per unique source
(small→5k rows, medium→100k, large→2M, taking the largest size class claimed by any
candidate riding that source) gives **~307.4 million rows, lower bound**. 18 of the
470 sources have no size information at all (unknown), so the real number is higher —
this is a floor, not an estimate of the true total.

**Sources carrying more than one candidate ID** (top 20 by count — full list of 49 in
the CSV, groupable by normalized URL):

| # IDs | Source | Domains it bridges |
|---:|---|---|
| 4 | IRS FATCA Foreign Financial Institution (FFI) List (irs.gov) | Banking, Securities, Fin. Crimes, International |
| 3 | NFA BASIC — Background Affiliation Status Info Center (nfa.futures.org) | Securities, Fin. Crimes |
| 3 | UK Companies House PSC bulk data (download.companieshouse.gov.uk) | Fin. Crimes, Corp. Registration, International |
| 3 | ICIJ Offshore Leaks Database (offshoreleaks.icij.org) | Fin. Crimes, Corp. Registration, International |
| 3 | OFLC Foreign Labor Certification Disclosure Data (catalog.data.gov) | Immigration (LCA/PERM/H-2A all ride one dataset) |
| 3 | ICE Detention Stints/Stays Data — Deportation Data Project (deportationdata.org) | Immigration |
| 3 | FAA Airworthiness Directives / Dynamic Regulatory System (drs.faa.gov) | Aviation & Rail |
| 3 | EIA-860 Annual Electric Generator Report (eia.gov) | Energy |
| 2 | FDA HCT/P Establishment Registration (fda.gov) | Healthcare, Pharma |
| 2 | CMS PECOS Medicare Provider Enrollment (data.cms.gov) | Healthcare, Corp. Registration |
| 2 | HRSA Health Center Program UDS Awardee data (data.hrsa.gov) | Healthcare (two IDs, one file) |
| 2 | VAERS Data Sets (vaers.hhs.gov) | Healthcare, Pharma |
| 2 | AccessGUDID (accessgudid.nlm.nih.gov) | Pharma, Consumer Safety |
| 2 | FDA 510(k) Premarket Notification (open.fda.gov) | Pharma, Consumer Safety |
| 2 | FDA MAUDE (open.fda.gov) | Pharma, Consumer Safety |
| 2 | FDA FAERS (open.fda.gov) | Pharma, Consumer Safety |
| 2 | EPA TRI Basic Data Files (epa.gov) | Environment, Consumer Safety |
| 2 | EPA Pesticide Product and Label System / PPLS (ordspub.epa.gov) | Environment, Consumer Safety |
| 2 | OCC Financial Institution Lists (occ.treas.gov) | Banking, Corp. Registration |
| 2 | HMDA LAR data via FFIEC HMDA Platform (ffiec.cfpb.gov) | Banking, Housing |

Full 49-source overlap list, and every individual candidate→source mapping, is in the
CSV — group by `dataset_name`/`url` to reconstruct it.

## 4. The holes

Every `not-found`, every `foia-only`, every `fragmented` — the places the public
record isn't actually public, or isn't actually one thing.

### not-found — 30 candidates, 15 domains

No locatable source this pass. A real finding, not a failure.

- **Agriculture & Food Safety** (1): State Livestock Brand Registration
- **Banking & Depository Institutions** (2): Fannie Mae/Freddie Mac Seller-Servicer Number; RTC Institution/Case Number (legacy, defunct 1995)
- **Consumer Protection & Product Safety** (2): GTIN/UPC/EAN (GS1 US Data Hub is private, not government); EPA Pesticide Chemical Code
- **Education** (1): FICE Code (legacy, superseded by OPEID/IPEDS)
- **Energy, Utilities & Pipeline Safety** (1): BSEE Incident Report Number/Facility ID
- **Federal Benefits & Safety Net / Veterans** (5): VA Loan Guaranty Number; SSA ALJ ID/OHO Hearing Office Code; FHA Case Number (Single-Family); SNAP State Recipient/Case Number; RRB Claim Number
- **Federal Procurement & Grants** (2): DBE Certification Number; Contract Line Item Number (CLIN/SLIN)
- **Housing, Real Estate & Mortgage Lending** (1): RTC/FSLIC Legacy Asset Control Number
- **Immigration & Border** (1): CBP SEACATS Seizure/Forfeiture Case Number
- **Insurance** (3): Enrolled Actuary (EA) Number; State Certificate of Authority Number; CMS TPMO ID
- **Labor, Workplace Safety & Benefits** (1): RRB Employer BA Number
- **Pharma, Biologics & Medical Devices** (1): National Health Related Item Code (legacy)
- **Science, Research Grants & Research Integrity** (2): NIH eRA Institution Profile File (IPF) Number; NSF ID (person identifier)
- **Telecom & Media** (4): USAC SPIN; Robocall Mitigation Database Filer ID; FAA OE/AAA Case Number; NANPA Central Office Code/NXX
- **Transportation -- Aviation & Rail** (3): FAA Air Carrier Operating Certificate Number; FRA Enforcement/Civil Penalty Case Number; Standard Transportation Commodity Code (STCC)

### foia-only — 12 candidates, 9 domains

- **Agriculture & Food Safety**: Packers and Stockyards Act (P&SA) Registration/Bond Number
- **Banking & Depository Institutions**: OTS Docket Number (legacy); RTC Institution/Case Number (legacy)
- **Environment & Natural Resources**: USDA NRCS/FSA Conservation Program Contract/Tract Number (protected under 7 U.S.C. 1619)
- **Federal Benefits & Safety Net / Veterans**: IRS PTIN (directory is search-only, no confirmed bulk file)
- **Federal Procurement & Grants**: OFCCP Compliance Evaluation Record
- **Housing, Real Estate & Mortgage Lending**: HUD Fair Housing (FHEO) Case Number
- **Immigration & Border**: EOIR Immigration Judge Identifier; ISAP/SmartLINK Participant ID; EOIR Immigration Court Code/Hearing Location Code
- **Labor, Workplace Safety & Benefits**: OSHA Whistleblower Program Case Number
- **Law Enforcement & Corrections**: DOJ/Treasury Asset Forfeiture Case or Tracking Number

### fragmented — 73 candidates, 21 domains

State-by-state with no single federal aggregator (or only a partial one). Federal
aggregator status: 2 yes, 26 partial, 44 no, 1 n/a. Heaviest domains: **Insurance**
(12 of its 27 candidates are fragmented — the whole domain runs state-by-state),
**Energy/Environment** (6 each — oil & gas, PUC dockets, radioactive material
licensing), **Law Enforcement & Corrections** (7), **Corporate Registration** (6).
Full per-candidate list with exemplar states is in the CSV
(`fragmented`/`federal_aggregator`/`fragmented_exemplars` columns) — 73 rows is too
long to repeat here without burying the rest of the report.

## 5. Corrections punch-list

Everything the prior sweep's rows called free/bulk/no-auth that the critic pass could
not stand behind on re-check: paywalled, key-gated, actually a search tool not a bulk
file, dead/moved URL, JS-rendered page that couldn't be verified, or evidence quoted
from a different page than the one cited. 83 of 319 critic-checked rows (26%)
downgraded. One line each below; full critic reasoning is in the CSV's `critic_note`
column for every row (not just downgrades).

| ID name | Domain | What the critic found |
|---|---|---|
| EPA Pesticide Registration Number / EPA Company Number (FIFRA) | Agriculture & Food Safety | The row's own URL (epa.gov/pesticide-registration/pesticide-product-and-label-system-ppls) returns HTTP 404 — dead link. |
| National Poultry Improvement Plan (NPIP) Participant Number | Agriculture & Food Safety | Fetched the exact cited URL (poultryimprovement.org/NPIPDatabase/index.cfm) directly — it's a login form, not an open database. |
| State Livestock Brand Registration | Agriculture & Food Safety | wlsb.state.wy.us loads and the quoted mission-statement line is accurate, but no actual lookup/download tool could be located. |
| USDA Rural Development Loan/Grant Recipient ID | Agriculture & Food Safety | Quoted JSON evidence is real but from a different URL than the one cited; proves USDA exists in USASpending, not that a Rural Development recipient-ID field exists. |
| FHA Lender ID | Banking & Depository Institutions | The cited PDF is a user manual for the FHA Connection portal, not lender data — wrong dataset entirely. |
| FinCEN MSB Registration Number | Banking & Depository Institutions | Confirmed search-by-criteria tool, not a standing bulk-file export. |
| Ginnie Mae Issuer ID | Banking & Depository Institutions | data.gov catalog page has no bulk file attached; flagged "restricted public," only links out to a JS-rendered directory tool. |
| HMDA Universal Loan Identifier (ULI) | Banking & Depository Institutions | Cited URL is a JS SPA; quoted evidence is actually from an unrelated LEI FAQ page. |
| CPSC Accepted/Accredited Testing Laboratory Number | Consumer Protection & Product Safety | cpsc.gov 403'd every attempt (known bot-block); first pass's own evidence leans on a stale 2021 third-party mirror. |
| CPSC NEISS Case Number | Consumer Protection & Product Safety | cpsc.gov 403'd every attempt this session — can't independently confirm. |
| CPSC SaferProducts.gov Report Number | Consumer Protection & Product Safety | saferproducts.gov 403'd at root and /PublicSearch — can't independently confirm. |
| EPA Pesticide Chemical Code | Consumer Protection & Product Safety | Cited URL is a dead link (404); correct page never located this session. |
| FCC Equipment Authorization ID | Consumer Protection & Product Safety | Both the cited URL and an alternate FCC ID search page 403'd — can't independently confirm. |
| FDA FAERS Case / Safety Report ID | Consumer Protection & Product Safety | Cited URL is openFDA API docs (api-open), not the separate bulk quarterly-extract file the row claims. |
| FMCSA Motor Carrier Number | Consumer Protection & Product Safety | Cited URL (safer.fmcsa.dot.gov) is a search-only portal, not a bulk-file host. |
| NHTSA Office of Defects Investigation Complaint Number | Consumer Protection & Product Safety | www.nhtsa.gov 403'd (whole-domain block distinct from the api.nhtsa.gov subdomain that works fine elsewhere). |
| USDA/FSIS Establishment Number | Consumer Protection & Product Safety | fsis.usda.gov 403'd on every attempt, including the bare homepage — whole-domain block. |
| CMS PECOS PAC ID / Enrollment ID | Corporate Registration & Beneficial Ownership | data.cms.gov is a JS SPA; six fetch attempts never rendered real content. |
| Open Ownership Register / Beneficial Ownership Data Standard (BODS) | Corporate Registration & Beneficial Ownership | The old bulk register redirect 403'd; OO's current site reads as repositioned toward standards/advocacy, not a live bulk dataset. |
| USPTO Trademark Serial Number / Registration Number | Corporate Registration & Beneficial Ownership | Real bulk downloads exist (Daily/XML, assignment, TTAB, image files) but the specific "Trademark Case Files Dataset" named in the row could not be located anywhere. |
| BJS Facility ID (Census of State & Federal Adult Correctional Facilities) | Criminal Justice & Court Systems | Metadata (DOI, license) checks out, but nothing in the quoted evidence actually establishes the "login required" claim; ICPSR's known gate is inferred, not directly observed this session. |
| OJJDP Juvenile Residential Facility Census (JRFC) Facility ID | Criminal Justice & Court Systems | Cited URL is pure methodology narrative — no bulk file and no login gate visible on that page at all. |
| ABET Accreditation ID (engineering/computing/technology programs) | Education | amspub.abet.org/aps is a bare JS app shell — no data reachable via plain fetch. |
| NC-SARA Participating Institution ID | Education | nc-sara.org directory returns only a page title across 5 attempts — heavy JS rendering, nothing independently confirmed. |
| BSEE Incident Report Number / Facility ID | Energy, Utilities & Pipeline Safety | Page is real, no login — but only offers annual aggregate counts, not incident-level records with the claimed ID fields. |
| FERC Electric Quarterly Report (EQR) Seller ID | Energy, Utilities & Pipeline Safety | Real, no login, but generates one PDF per manual query — not bulk-file. |
| IAEA PRIS Reactor Unit ID | Energy, Utilities & Pipeline Safety | Old URL now redirects to a JS dashboard; no visible API, reactor-unit-level access unconfirmed. |
| ISO/RTO Interconnection Queue Position ID | Energy, Utilities & Pipeline Safety | Cited page is process/guidance documentation only — no queue data, no ID list. |
| BLM Serial Number (LR2000 / MLRS Case Number) | Environment & Natural Resources | Cited page explicitly requires creating an MLRS account to work with cases/serial numbers — account-gated, not open. |
| USGS Site Number (NWIS) | Environment & Natural Resources | Legacy bulk-query tool retired; real access is now the live REST API (api-open, still no-auth) — access shape was mislabeled, not the auth. |
| FHA Case Number (Single-Family mortgage insurance) | Federal Benefits & Safety Net / Veterans | Full-page grep for every download-link pattern turned up nothing — content-free placeholder page, no report anywhere on it. |
| DBE (Disadvantaged Business Enterprise) Certification Number | Federal Procurement & Grants | transportation.gov 403'd (WAF block); Wayback snapshot shows a policy-overview page, not a certification directory — and the first pass's own evidence was sourced from Wikipedia, not this URL. |
| CBP Customs Broker License Number | Financial Crimes, Sanctions & AML | cbp.gov 403'd on every attempt — can't independently confirm. |
| EU Consolidated Financial Sanctions List reference number | Financial Crimes, Sanctions & AML | JS SPA with a session-cookie redirect loop that exceeded 10 hops — unreachable this session. |
| EUID (European Unique Identifier) | Financial Crimes, Sanctions & AML | Cited page is purely informational; "EUID" doesn't appear on it, and several member-state registries charge fees for full extracts despite free basic search. |
| OFAC-listed digital currency (cryptocurrency) addresses | Financial Crimes, Sanctions & AML | Cited URL is a search-only lookup tool; the real bulk-file/no-auth data lives at a different, unquoted Treasury URL. |
| OpenOwnership Beneficial Ownership Data Standard (BODS) statement ID | Financial Crimes, Sanctions & AML | Cited URL is spec/schema documentation only — no dataset, no download link. |
| CHPL Product/Developer ID (ONC Certified Health IT Product List) | Healthcare & Clinical | Cited URL is a JS SPA fragment route that never renders server-side; first pass's evidence was actually from an unrelated mirror page. |
| HHS OCR Breach Portal record (HIPAA Breach of Unsecured PHI) | Healthcare & Clinical | Both fetches returned only landing content — the actual breach-record data grid was never directly observed. |
| Nursys ID (NCSBN nurse licensure database) | Healthcare & Clinical | QuickConfirm is a one-record-at-a-time lookup (must already know name/license/state) — not a browsable/crawlable listing despite technically being "scrape-only." |
| SAMHSA Facility ID (Behavioral Health Treatment Locator / N-SSATS) | Healthcare & Clinical | Cited URL redirects to a different, JS-rendered host — stale URL, nothing independently confirmed. |
| HMDA Universal Loan Identifier | Housing, Real Estate & Mortgage Lending | Cited URL is a JS SPA; quoted evidence is actually from an unrelated check-digit calculator page, and CFPB's published Modified-LAR policy masks the real ULI anyway. |
| DOL LCA Case Number (Labor Condition Application) | Immigration & Border | Substance of the claim holds (OFLC data.gov page confirms case-level Excel releases), but the quoted "six foreign labor certification categories" phrase doesn't actually appear on the page, and the terminal dol.gov download page 403'd. |
| DOL PERM Case Number (Permanent Labor Certification) | Immigration & Border | Same underlying page/finding as the LCA row above. |
| DOL Temporary Labor Certification Case Number (H-2A / H-2B) | Immigration & Border | Same underlying page/finding as the LCA row above. |
| ICE ERO Field Office / Area of Responsibility (AOR) Code | Immigration & Border | Cited URL is dead (404); real data confirmed live at a restructured URL on the same site, downloadable, no login. |
| CMS Medicaid Managed Care Plan ID (T-MSIS MCO ID) | Insurance | File description matches, but it's classified a "Research Identifiable File" routed through CMS/ResDAC's formal Data Use Agreement process — "login" undersells the real barrier. |
| EIOPA Register Code (EU/EEA insurance undertakings) | Insurance | Cited page is a landing/directory page only; the actual register link 403'd — no API access confirmed. |
| NFIP Write-Your-Own (WYO) Company Code | Insurance | Page is genuinely public and scrapeable, but the actual "Company Code" field claimed isn't visible on it — likely lives in a separate FEMA manual appendix. |
| State Certificate of Authority Number | Insurance | Cited page describes an application *process* (with a login-gated electronic portal) — no bulk or scrapeable listing of actual issued CoA numbers. |
| USDA RMA Approved Insurance Provider (AIP) Code | Insurance | Client-rendered SPA; plain fetch returns only a page title, no table. |
| Additional uncovered EU national business registries (NL/BE/LU/Nordics) | International & Cross-Border Identifiers | Mixed bag flattened into one claim — Netherlands' KVK is actually paid per-lookup, not free; Belgium and Norway do check out as claimed. |
| EU Financial Sanctions Files (EU consolidated sanctions list) | International & Cross-Border Identifiers | JS SPA with a >10-hop redirect loop — unreachable, can't confirm or disprove. |
| WHD Case ID (WHISARD) | Labor, Workplace Safety & Benefits | Metadata description checks out on catalog.data.gov, but the actual download portal (dataportal.dol.gov) never rendered — bulk-download mechanics unconfirmed. |
| Census of Juveniles in Residential Placement (CJRP) Facility ID | Law Enforcement & Corrections | First pass overstated badly — every CJRP study year on NACJD (1997-2021) is flagged Restricted Use, requiring an in-person ICPSR Data Enclave visit plus IRB approval; public access is a crosstab tool only. |
| HIFLD Prison Boundaries / Law Enforcement & Corrections Facility ID | Law Enforcement & Corrections | Cited catalog.data.gov URL is a bare metadata stub with zero download links; the real ArcGIS feature layer is confirmed public/downloadable but at a different URL. |
| Administrative Controlled Substances Code Number | Pharma, Biologics & Medical Devices | Cited URL is dead (404); correct URL located and confirmed to host real no-login PDFs (not structured data). |
| CAS Registry Number | Pharma, Biologics & Medical Devices | Web search UI is genuinely free/open, but the API specifically requires a free API-key token — row was filed as fully open when only the human-facing search is. |
| UK Electoral Commission Political Party / Regulated Donee registration number | Politics, Elections & Lobbying | Cited URL is a blank record template with no query parameters — proves nothing concrete; the real search tool does check out separately as public/no-login. |
| dbGaP Study Accession Number | Science, Research Grants & Research Integrity | Public stats describe the metadata/ID layer only; actual genotype/phenotype data requires an eRA Commons account and Data Access Committee approval. |
| Classification of Financial Instruments Code | Securities, Investment Funds & Markets | Cited URL never mentions CFI at all — only describes an unrelated ISIN lookup tool. |
| EDGAR Filing Agent CIK | Securities, Investment Funds & Markets | sec.gov 403'd on every URL tried this session (blanket bot-block); separately, the cited endpoint is a per-company search form, not a bulk file, regardless. |
| Investment Adviser Registration Depository Number | Securities, Investment Funds & Markets | JS SPA; three fetch attempts never rendered a download link. |
| MSRB Dealer Executing Broker Symbol | Securities, Investment Funds & Markets | Registrant list itself is real and downloadable, but the specific "executing broker symbol" field claimed isn't present in the table or export. |
| SEC Litigation Release Number / Administrative Proceeding File Number | Securities, Investment Funds & Markets | sec.gov 403'd; original evidence was sourced from a third-party site, not the official page either. |
| Broadband Data Collection Provider ID | Telecom & Media | Same JS SPA issue as the Fabric ID row below — only a page title renders. |
| Broadband Serviceable Location Fabric ID | Telecom & Media | bdc.fcc.gov is a JS SPA; the page title is literally all either pass could confirm. |
| Broadcast Facility ID | Telecom & Media | Confirmed: publicfiles.fcc.gov is a per-station search portal, not a bulk-file download. |
| FAA Obstruction Evaluation / Airport Airspace Analysis Case Number | Telecom & Media | Site was serving a government-shutdown status notice instead of the normal application UI at check time. |
| FCC Form 499 Filer ID | Telecom & Media | Quote is real, but describes USF-fund filer registration, not a public bulk dataset of Filer IDs. |
| Mobile Country Code / Mobile Network Code | Telecom & Media | mcc-mnc.com is JS-rendered — only a page title came through twice, no pricing/access details confirmed. |
| NANPA Central Office Code / NXX | Telecom & Media | nationalnanpa.com failed DNS resolution both attempts — couldn't reach the site at all this session. |
| Robocall Mitigation Database Filer ID | Telecom & Media | ServiceNow-hosted app never finished rendering — only loading-shell chrome returned. |
| Study Area Code / USF High-Cost recipient ID | Telecom & Media | Cited URL is USAC's Lifeline page, not the High-Cost program page the row is actually about. |
| US Copyright Office Registration Number | Telecom & Media | Quote is real but describes CPRS as a search portal, not a bulk dataset. |
| USAC Service Provider Identification Number | Telecom & Media | usac.org homepage doesn't mention SPIN anywhere — quoted phrase doesn't appear on the page. |
| FAA Repair Station Certificate Number | Transportation -- Aviation & Rail | Quoted "5035 Repair Stations in Database" figure could not be independently reproduced. |
| FAA Service Difficulty Report (SDR) Control Number | Transportation -- Aviation & Rail | sdrs.faa.gov offers only an interactive search tool — not bulk-file. |
| PHMSA Hazardous Materials Incident Report Number | Transportation -- Aviation & Rail | Cited URL and the whole PHMSA domain 403'd — bot-block, not proof either way. |
| NTSB Accident / Investigation Case Number | Transportation -- Motor Carrier & Maritime | CAROL confirmed real, public, no login, cross-mode search tool — access shape/auth downgraded only in the sense of clarifying it's a search tool, not a bulk file. |
| State Intrastate Motor Carrier Permit Number (CA DMV MCP) | Transportation -- Motor Carrier & Maritime | Page loads and title matches, but no further access-mechanics detail could be confirmed beyond that. |
| UN/LOCODE (UN Code for Trade and Transport Locations) | Transportation -- Motor Carrier & Maritime | unece.org 403'd on every URL tried, including the bare domain root — site-wide bot-block, not evidence against the claim. |
| Unified Carrier Registration (UCR) Number | Transportation -- Motor Carrier & Maritime | ucr.gov is fully client-rendered — plain fetch returns nothing, including on /robots.txt. |

## 6. Honesty section

**What the critic pass actually caught**, in rough order of frequency:

1. **Evidence quoted from a different page than the one cited** (~15 rows) — the
   first-pass researcher's "confirmed" quote was real, but sourced from a mirror,
   FAQ, or unrelated page, not the URL in the row. This is the single most common
   failure mode and the exact thing the confidence rules were designed to catch.
2. **JS-rendered single-page apps that a plain fetch can't see through** (~15 rows) —
   FCC's Broadband Data Collection, several SEC tools, ABET, NC-SARA, EIOPA, USDA RMA
   AIP Listing, IAEA PRIS. These aren't necessarily wrong, just unverifiable by the
   method available this session; a headless-browser pass would resolve most of them.
3. **Government sites bot-blocking automated fetches** (~12 rows) — cpsc.gov,
   fsis.usda.gov, sec.gov, cbp.gov, unece.org, phmsa.dot.gov all 403'd site-wide, not
   just on the cited page. This matches the CPSC TLS-blocking behavior already in
   Ripple's loader-trap memory — the pattern generalizes to more agencies than
   previously known.
4. **"Search tool" claimed as "bulk-file"** (~15 rows) — FMCSA SAFER, FERC EQR
   viewer, MSRB Registrant list (partial), NTSB CAROL, sdrs.faa.gov, Broadcast Facility
   ID, and others are real, public, no-login tools that return one record or one
   report per query, not a standing downloadable file.
5. **Dead or moved URLs** (~8 rows) — EPA Pesticide Chemical Code, DEA schedules page,
   ICE ERO field-office data, HIFLD Prison Boundaries, DBE certification page — the
   underlying dataset is often still real and locatable, just not at the address the
   first pass cited.
6. **Real barrier understated** (~5 rows) — CMS T-MSIS Research Identifiable Files,
   dbGaP, CJRP/NACJD restricted-use studies: these were called "login" when the
   actual gate is a formal Data Use Agreement, IRB approval, or in-person data-enclave
   access — a meaningfully higher bar than a free account.

**Domains to trust least** (highest critic downgrade rate among checked rows):
**Telecom & Media** (11 of 12 checked, 92%) — almost every FCC/USAC tool in this
domain turned out to be a search portal or JS SPA rather than a bulk file.
**Agriculture & Food Safety** (4 of 5, 80%) and **Transportation -- Motor Carrier &
Maritime** (4 of 6, 67%) follow. At the other end, **Science, Research Grants &
Research Integrity** (1 of 24, 4%), **Housing, Real Estate & Mortgage Lending** (1 of
17, 6%), and **Environment & Natural Resources** (2 of 23, 9%) held up best under
adversarial re-check.

**What's still probably incomplete after the critic pass:** the critic pass only
re-checked the 319 rows claiming the best-case combination (confirmed + bulk/no-auth)
— it did not re-verify the 247 `inferred` rows or the 30 `not-found` rows, so
`inferred` should be read as "plausible, unverified" rather than "checked and holding
up." The bot-blocking pattern hit hard enough (cpsc.gov, fsis.usda.gov, sec.gov,
unece.org, phmsa.dot.gov, cbp.gov all site-wide 403 to automated fetch) that several
domains leaning on those agencies — Consumer Protection & Product Safety in
particular — likely have real sources sitting behind what looks like "unverifiable"
in this recon, not "doesn't exist." A second pass with a headless-browser-capable
fetch tool would likely resolve most of the JS-SPA and bot-block gaps without
needing new research, just a better tool.
