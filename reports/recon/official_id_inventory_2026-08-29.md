# Official ID Inventory — HAVE vs. STILL OUT THERE — 2026-08-29

Question: every government / official identifier that can connect public data, split into
(A) wired into the spine, (B) sitting in the warehouse but not wired, (C) not held at all.

Method (all repo-side, no warehouse compute):
- Spine registry: `connect/keys.py` (KEY_TOKENS + EXACT_TOKEN_KEYS + TABLE_COLUMN_KEYS + NORM_RULES).
- Wiring health: `reports/connections_audit_2026-08-27/join_layer.md` §3 (edge counts per family).
- Warehouse presence: name scan of `reports/_all_columns.csv` (20,732 mart columns, snapshot 2026-08-20)
  against 115 known ID-system name patterns → `reports/id_system_scan_2026-08-29.csv`.
- Prior recon: `reports/recon/unregistered_id_candidates_2026-08-28.md` (value-verified counts for CAGE,
  NPPES legacy IDs, license numbers).

Caveats (positional, at the end of each section): the column scan is NAME-based. "Present" means a
column with that name exists in a mart; fill/distinctness is only verified where a prior session checked
it (marked ✓). The 08-20 snapshot predates MAUDE / subawards / LDA loads still running.

---

## A. HAVE + WIRED (in the spine today)

### A1. Hard-ID families (STEEL) — 26 registered

| ID system | Issuer | What it identifies | Tables | Health (08-27 audit) |
|---|---|---|---|---|
| NPI | CMS | health providers (people + orgs) | 34 | ✓ healthy — biggest connector, 117M matched pairs |
| EIN | IRS | employers / orgs | 34 | ✓ healthy |
| CCN | CMS | certified facilities (hospitals, SNFs…) | 25 | ✓ healthy |
| CIK | SEC | filers (companies, funds, insiders) | 19 | ✓ healthy |
| FRS_ID | EPA | regulated facilities (registry) | 18 | ✓ healthy, 56.9M matches |
| FEC_CMTE_ID | FEC | political committees | 11 | ✓ healthy |
| FEC_CAND_ID | FEC | candidates | 10 | ✓ healthy |
| PWSID | EPA | public water systems | 10 | ✓ healthy |
| NPDES_ID | EPA | water-discharge permits | 10 | ✓ healthy |
| UEI | SAM.gov | federal award recipients | 7 | ✓ healthy |
| LEI | GLEIF | legal entities (global finance) | 7 | ✓ healthy |
| CL_PERSON_ID | CourtListener | judges / court people | 8 | ✓ healthy |
| BIOGUIDE | Congress | members of Congress | 5 | ✓ healthy |
| CL_COURT_ID | CourtListener | courts | 4 | ✓ healthy |
| NCUA_CHARTER | NCUA | credit unions | 4 | ✓ healthy |
| ICPSR | VoteView | legislators (historical) | 3 | ✓ healthy, small |
| MINE_ID | MSHA | mines | 3 | ✓ healthy |
| ICE_FACILITY | ICE | detention facilities | 3 | ✓ healthy |
| MSHA_CONTROLLER_ID | MSHA | mine controllers | 3 | registered 08-28 — edges not yet measured |
| MSHA_OPERATOR_ID | MSHA | mine operators | 2 | registered 08-28 — edges not yet measured |
| CUSIP | CUSIP Global | securities | 4 | registered 08-28 — edges not yet measured |
| DUNS | D&B | orgs (pre-2022 federal awards) | 3 | ⚠ 94% orphaned — assistance-table DUNS never ingested |
| COMPANY_NO | UK Companies House | UK companies | 2 | works, closed 2-table island |
| IMO | IMO | ships | 2 | ⚠ indexed, ZERO edges |
| MMSI | ITU | ship radios | 1 | ⚠ one-sided, connects nothing |
| DEA_NO | DEA | controlled-substance registrants | 1 | ⚠ one-sided (ARCOS only) |
| PATENT | USPTO | patents | 0 | ✗ DEAD — zero carrying columns |

### A2. Softer registered families

| Family | Tier | Notes |
|---|---|---|
| DOCKET | STRONG | ⚠ FDIC cert numbers collide with SCOTUS dockets; ~40% precision; needs issuer namespace |
| NAICS / SIC / NCES | STRONG | classification codes, not identities — group, don't identify |
| FIPS / ZIP / COUNTRY / LATLON / GEOM | GEO | place, not identity; some families match on 2-digit codes |
| NAME / PERSON / ADDRESS | PROBABILISTIC | fuzzy; CORROBORATED tier (name@zip) is 75–85% precise |

---

## B. HAVE IN WAREHOUSE, NOT WIRED (columns exist, spine ignores them)

Ranked by connective value. "Tables" = mart tables carrying a column with that name (name scan);
✓ = value-verified by a prior session.

| # | ID system | Issuer | Tables | Where it lives | What it would connect | Verified |
|---|---|---|---|---|---|---|
| 1 | CAGE code | DLA | 4 | USAspending contracts (landing + econ/procurement marts) | defense contractors ↔ SAM ↔ DoD data | ✓ 6.32M/6.33M filled, 92,530 distinct |
| 2 | PIID / FAIN / award unique key | USAspending | 11 | contracts, assistance, subawards, NIH, SBIR | prime ↔ sub-award, award ↔ recipient ↔ agency | catalog only |
| 3 | PECOS enrollment ID / PAC ID | CMS | 8 | provider enrollment, Care Compare, Open Payments-adjacent | enrollment ↔ ownership ↔ NPI-world; the ownership axis | not verified |
| 4 | Medicaid / legacy provider IDs (other-identifier block) | states / Medicare | 1 (200 cols) | NPPES | NPI-world ↔ state Medicaid data (the bridge to state health data) | ✓ slot 1: 1.56M filled / 1.34M distinct |
| 5 | State professional license # (+state) | state boards | 8 | NPPES (15 slots), portal tables | provider ↔ state discipline/board actions | ✓ slot 1: 5.78M / 3.91M distinct |
| 6 | UPIN | Medicare (retired) | 1 | LEIE exclusions | old exclusions ↔ NPPES UPIN slots | catalog (474 distinct) |
| 7 | FDIC certificate # | FDIC | 5 (finance) | FDIC institutions / branches / failures | banks across FDIC files ↔ HMDA ↔ FHLB; also the DOCKET collision culprit | not verified |
| 8 | RSSD ID | Federal Reserve | 5 | FDIC / holding-company tables | banks ↔ holding companies ↔ Fed data | not verified |
| 9 | HMDA respondent ID / ARID | CFPB / FFIEC | 2 | HMDA (19M-row keyless giant) | mortgage lenders ↔ FDIC/RSSD/LEI | not verified |
| 10 | NDC | FDA | 2 | drug product tables | drugs ↔ Part D ↔ FAERS ↔ ARCOS ↔ Open Payments products | verified-unregistered per STATUS |
| 11 | FDA FEI / registration # | FDA | 3 (health) + list cols | drug/device establishment tables | manufacturing sites ↔ inspections ↔ recalls ↔ warning letters | not verified |
| 12 | FDA application # (510k / PMA / NDA / BLA) | FDA | 7 | device + drug approval tables | product ↔ approval ↔ recall ↔ MAUDE | not verified |
| 13 | UDI-DI (device identifier) | FDA GUDID | 2 | device tables | device ↔ MAUDE ↔ recalls | not verified |
| 14 | CAS / UNII (chemical) | CAS / FDA | 4 | TRI, chemical, drug ingredient tables | chemical ↔ release ↔ product ↔ adverse event | not verified |
| 15 | Ticker | exchanges | 12 | SEC, senate trades, econ | name-only senate trades ↔ CIK (via public ticker→CIK map) | catalog (1,029 distinct) |
| 16 | ISIN | ISO | 2 (econ) | XBRL-linked tables | securities ↔ CUSIP/LEI | not verified |
| 17 | SEC file # | SEC | 6 | filings, broker tables | filing series ↔ registrant | not verified |
| 18 | OFAC SDN entity # | Treasury | 1+ | sanctions list | sanctioned entities ↔ IMO/LEI/UK sanctions | not verified |
| 19 | ICIJ node ID | ICIJ | 6 | offshore leaks tables | offshore entities ↔ officers ↔ addresses (internal glue; edge to spine is name-only) | not verified |
| 20 | IRS 990 object ID / DLN | IRS | 3 | 990 e-file index | 990 filings ↔ EIN | not verified |
| 21 | TAS / agency codes (CGAC, toptier, subtier) | Treasury / OMB | 4 / 10 | USAspending tables | money ↔ account ↔ agency | not verified |
| 22 | CFDA / assistance listing # | GSA | 5 | grants tables | grant ↔ program | not verified |
| 23 | NIH project # / APPL ID | NIH | 2 | RePORTER, SBIR | research awards ↔ recipients ↔ subawards | not verified |
| 24 | LDA registrant / client ID | Senate | 2 (+MSRB) | lobbying filings | lobbyist ↔ client ↔ filing (the lobbying spine) | catalog (9,245 / 2,057 distinct) |
| 25 | Committee code | Congress | 1 | committee membership | member ↔ committee ↔ bill referral | catalog |
| 26 | Bill # / public law # | Congress | 4 | bills, cosponsors | bill ↔ sponsor ↔ law | catalog |
| 27 | FJC judge NID | FJC | 6 | judge / appointment tables | judge ↔ appointment ↔ president ↔ court | catalog |
| 28 | CourtListener cluster / opinion / PACER case ID | CourtListener | 11 / 2 | opinions, dockets, RECAP | opinion ↔ docket ↔ judge (internal glue for the ~38M-row block) | not verified |
| 29 | SCDB justice code | Supreme Court Database | 4 | SCOTUS tables | justice ↔ vote ↔ case | catalog |
| 30 | Docket / case number (all issuers) | courts, agencies | 27 | JUSTICE 11, FINANCE 4, LABOR 4, CONSUMER_SAFETY… | case ↔ party — only after issuer namespacing | registered STRONG, ⚠ broken |
| 31 | DOL 5500 ACK ID / plan # (EIN+PN) | DOL EBSA | 6 | Form 5500 tables | plan ↔ sponsor ↔ service provider ↔ PBGC | verified-unregistered per STATUS |
| 32 | OSHA establishment ID | OSHA | 6 (labor) | inspections, violations, accidents | inspection ↔ violation ↔ accident ↔ establishment | not verified |
| 33 | OFLC case # (H-1B / PERM) | DOL OFLC | in docket scan | foreign labor cert tables | employer ↔ visa case | verified-unregistered per STATUS |
| 34 | EIA plant / utility / generator ID | EIA | 10 (ENERGY) | EIA 860/923/861 tables | plant ↔ utility ↔ generator ↔ emissions — the whole dead ENERGY domain | not verified |
| 35 | FERC docket / CID | FERC | 2 | energy tables | filing ↔ company | not verified |
| 36 | PHMSA operator ID (OPID) | PHMSA | 2–3 | pipeline incident tables | operator ↔ incident ↔ mileage | not verified |
| 37 | TRI facility ID | EPA | 2 | Toxic Release Inventory | TRI ↔ FRS (needs the FRS crosswalk) | not verified |
| 38 | RCRA handler ID / EPA ID | EPA | 3 | hazardous waste tables | handler ↔ violations ↔ FRS | not verified |
| 39 | ICIS facility interest / program-system IDs | EPA | 15 | ECHO tables | program record ↔ FRS | not verified |
| 40 | HUC8 / USGS site # | USGS | 3 | water tables | watershed ↔ facility | not verified |
| 41 | NCES / IPEDS UNITID / OPEID | ED | 3 (EDUCATION) | school / college tables | school ↔ college scorecard ↔ loans — dead EDUCATION domain | not verified |
| 42 | Open Payments profile ID | CMS | 4 | Open Payments | recipient ↔ payment (internal; bridge to NPI exists on-table) | not verified |
| 43 | HCRIS report record # | CMS | 1 | cost reports | cost report ↔ CCN | not verified |
| 44 | NTSB event ID / NTSB # | NTSB | 3 (TRANSPORT) | aviation events | event ↔ aircraft ↔ operator | not verified |
| 45 | Airport ID | FAA | 2 | transport tables | airport ↔ event | not verified |
| 46 | VIN | NHTSA | 1 | consumer safety | vehicle ↔ complaint ↔ recall | not verified |
| 47 | FEMA disaster # | FEMA | 2 | disaster declarations | disaster ↔ county ↔ housing assistance (FEMA 26M keyless giant) | not verified |
| 48 | LIHTC / HUD participant code | HUD | 2 | housing tables | project ↔ owner | not verified |
| 49 | FCC FRN / ULS file # | FCC | 1 | politics-adjacent FCC table | licensee ↔ filings | not verified |
| 50 | ORI (law-enforcement agency) | FBI | 1 | one justice table | agency ↔ crime reports | not verified |
| 51 | CVE ID | MITRE | 2 | ransomware / breach tables | vuln ↔ incident | not verified |
| 52 | BIS denied-persons | Commerce | 1–2 | export enforcement | denied party ↔ entities (name-only unless ID present) | not verified |

Caveat: rows 7–52 are name-scan hits; a handful will be false friends (e.g. the scan's "CERT" pattern
also catches aircraft certification columns in TRANSPORT — excluded above by hand). Nothing here was
value-checked this session.

---

## C. NOT IN THE WAREHOUSE AT ALL (still out there)

Official ID systems with zero matching columns in the 08-20 mart inventory. Public source that would
bring each one in is named. Ranked by how many existing tables it would light up.

| # | ID system | Issuer | Public source that carries it | Would connect to (what we already hold) | Openness |
|---|---|---|---|---|---|
| 1 | Vessel official # / USCG doc # | USCG | PSIX / USCG documentation bulk | IMO + MMSI (both dead axes) + OFAC vessels | public |
| 2 | Patent # / application # | USPTO | PatentsView bulk | revives the dead PATENT family; ↔ CIK/assignee names | public |
| 3 | USDOT # / MC # | FMCSA | FMCSA census + SAFER + crash/inspection bulk | carriers ↔ crashes ↔ OSHA ↔ EIN (name) | public |
| 4 | CRD # | FINRA / SEC | BrokerCheck / IAPD bulk (Form ADV) | advisers ↔ CIK ↔ enforcement | public |
| 5 | NMLS ID | CSBS | NMLS Consumer Access; HMDA LEI crosswalk | mortgage lenders ↔ HMDA (19M keyless) ↔ CFPB complaints | public (bulk is scraped) |
| 6 | ORIS / plant code | EPA CAMPD | Clean Air Markets bulk | EIA plants ↔ emissions ↔ FRS | public |
| 7 | GHGRP facility ID | EPA | GHGRP bulk (Envirofacts) | emitters ↔ FRS ↔ TRI | public |
| 8 | Superfund / SEMS site ID | EPA | SEMS bulk | sites ↔ FRS ↔ RCRA ↔ counties | public |
| 9 | NRC docket / license # | NRC | ADAMS / NRC datasets | reactors ↔ EIA plants ↔ events | public |
| 10 | FAA N-number / registrant | FAA | aircraft registry bulk | NTSB events ↔ owners ↔ airports | public |
| 11 | DOT airline / carrier ID | BTS | T-100, On-Time bulk | airlines ↔ NTSB ↔ airports ↔ CIK | public |
| 12 | SBA loan # (PPP / EIDL / 7a) | SBA | SBA FOIA bulk | borrowers ↔ EIN? (no — name+zip only) ↔ NAICS | public |
| 13 | NFIP policy / claim ID | FEMA | OpenFEMA NFIP redacted | flood claims ↔ counties ↔ FEMA disasters | public (redacted) |
| 14 | HUD PHA code | HUD | PHA contact/scorecards | housing authorities ↔ LIHTC ↔ counties | public |
| 15 | NLRB case # | NLRB | NLRB case API | employers ↔ ULP charges ↔ EIN (name) | public |
| 16 | EEOC charge # | EEOC | not bulk-public (litigation only) | — | closed |
| 17 | WHD case ID | DOL WHD | WHD enforcement bulk (loader status unknown — check) | employers ↔ back-wage cases ↔ OSHA | public |
| 18 | OPM agency subelement code | OPM | FedScope | federal workforce ↔ agency codes | public |
| 19 | DoDAAC / NSN | DoD | DAAS / FLIS | contracts ↔ activity ↔ item | semi-public |
| 20 | VA station # | VA | VA facility list | VA facilities ↔ CCN ↔ NPI | public |
| 21 | Federal Register doc # / RIN | GPO / OMB | federalregister.gov API | rules ↔ agencies ↔ dockets | public |
| 22 | Regulations.gov docket / document ID | GSA | regulations.gov API | comments ↔ commenters (name) ↔ rules | public |
| 23 | Trademark serial / reg # | USPTO | TM bulk | brands ↔ owners (name) | public |
| 24 | BOP register # | BOP | inmate locator (no bulk) | — | closed |
| 25 | USCIS receipt # / A-number | DHS | never published | — | closed |
| 26 | NOAA station IDs (WBAN / GHCN) | NOAA | NCEI bulk | weather ↔ events ↔ counties | public |
| 27 | Foreign company registry # (SIREN, KVK, ABN, OpenCorporates ID) | national registries | OpenCorporates (paid), national open data | ↔ LEI ↔ ICIJ ↔ UK Companies House | mixed |
| 28 | SWIFT BIC | SWIFT | GLEIF BIC↔LEI mapping (free) | banks ↔ LEI | public |
| 29 | ABA routing # | ABA / Fed | Fed E-Payments directory | banks ↔ RSSD ↔ FDIC | public |
| 30 | State SoS corporate file # | 50 states | state open-data portals (uneven) | the missing US company axis; ↔ EIN via 990/5500 names | mixed |
| 31 | County parcel / APN | counties | uneven | property ↔ owners ↔ LIHTC ↔ FEMA | mixed |
| 32 | Medicare PTAN / HICN / SSN / TIN-as-SSN | CMS / SSA | never public | — | closed (and must stay out) |

---

## D. What this changes about the next step

- **26 hard-ID families are wired; 5 of them are dead or one-sided** (PATENT, IMO, MMSI, DEA, DUNS).
- **~50 official ID systems are already in the warehouse and ignored.** The biggest by rows:
  CAGE (6.3M), award keys (contracts+assistance+subawards), PECOS enrollment (8 tables),
  EIA plant IDs (10 ENERGY tables — the whole dead domain has keys, they're just unregistered),
  FDIC cert + RSSD (5 tables each — the bank axis has hard keys and the spine only sees names).
- **~30 systems are not held at all.** Only three of them unlock existing dead axes cheaply:
  USCG vessel registry (IMO/MMSI), PatentsView (PATENT), FMCSA census (TRANSPORT domain).
- Wiring a family from bucket B costs one spec entry + a spine rebuild pass; landing a bucket-C
  source costs a loader + storage + the same wiring.
