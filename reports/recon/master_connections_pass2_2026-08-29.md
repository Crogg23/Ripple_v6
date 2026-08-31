# Master Connections List — PASS 2: value-checked leftovers, pointers, and the 747 catalog (2026-08-29, late)

Scope: everything pass 1 left open — bucket-B rows the 08-29 inventory never value-checked, tables landed after
the 08-20 snapshot (GUDID, NDC directory, GLEIF Level 2, SAM, USCG, FMCSA, CAMPD), the 08-05 web-research
catalog's 254 "might already have it" rows, and parent / owner / successor pointer columns.
Method: 200 columns profiled live (rows / filled / distinct non-blank / junk / sample), 82 + 24 overlap or
resolution joins. Raw: `reports/recon/pass2/pass2_live_check_2026-08-29.json`; script:
`scripts/pass2_connections_check_2026_08_29.py`. Warehouse time 5 min + follow-ups; ~$1.

Pass-1 corrections first (section A), then new verified families (B), pointer resolution (C), dead/masked (D),
the catalog reconciliation (E), and what is genuinely not held (F).

## A. Pass-1 claims that were wrong or sloppy

| Pass-1 said | Pass-2 found |
|---|---|
| "TRI facility FRS column dead" | The `FRS_ID` column is dead, but `EPA_REGISTRY_ID` on the same table is live: 64,728 distinct, **99.9% resolve into the FRS registry** (3.4M). TRI ↔ FRS is a solid edge. |
| "ISIN — 0 non-blank on the EDGAR table" (checked a 200-row XBRL flag) | Confirmed on the right table this time: 48,990 rows, 100% blank. ISIN is not held. |
| "UDI — portal only" | GUDID is held: 5,182,695 devices (primary DI) + 6,767,219 package-level device ids. |
| "FDA FEI" matched FARA / UK registration numbers | FEI is not held. FDA establishment registration is a 166-row stub. |
| "BIS denied" matched court `DATE_CERT_DENIED` | Not held as its own table; BIS parties live inside the consolidated screening list (source column). |
| "SNF affiliation entity id — not verified" | It is the **nursing-home chain id** (635 distinct, identical count to CHAIN_ID); 0% match to PECOS. |
| "FDIC LEI empty" (08-17) | 8.1% filled, 2,241 distinct — already flagged in pass 1; stands. |
| Catalog said 37 systems were "not held" | They are (section E). |

## B. Newly value-verified ID systems (pass 2)

Distinct = distinct non-blank. "Edge" = share of left distinct values found on the right, measured live.

### B1. Health / pharma / devices

| ID system | Where | Distinct | Edge measured | Read |
|---|---|---:|---|---|
| GUDID primary DI (UDI-DI) | GUDID device + identifiers | 5,182,695 | device ↔ identifiers 100% | device identity — solid; partner (MAUDE / recalls) not yet loaded |
| GUDID package device ids | GUDID identifiers | 6,696,187 | — | package level of the same key |
| GUDID labeler DUNS | GUDID device | 12,272 | → contracts recipient DUNS 17.1%; → TRI parent DUNS 1.1%; → SBIR 3.3% | device makers ↔ federal contractors |
| NDC directory product NDC | FDA NDC directory | 114,649 | NADAC (11-digit) → directory (9-digit) **82.1%** | drug price ↔ drug label — solid after 5-4 normalization |
| FDA application # (NDA / ANDA / BLA) | FDA NDC directory | 13,093 | — | approval identity: ANDA 9,642 · NDA 2,561 · BLA 686; partner (Orange Book / approvals) not held |
| FDA drug master file # | FDA DMF | 41,253 | — | one table; holder is a name |
| HIOS issuer / product / component / plan | CMS marketplace PUF | 359 / 906 / 5,144 / 22,059 | → FHLB NAIC id 0.6% (sanity) | the first health-plan key; no partner table yet |
| HRSA health-center # (grant) | UDS sites + center info | 1,526 / 1,356 | sites ↔ center info (BHCMIS) 88.1% | grantee ↔ sites |
| HRSA site NPI | UDS sites | 6,048 | → NPPES **99.3%** | FQHC sites ↔ NPI world (32% of sites carry one) |
| HRSA site Medicare billing # | UDS sites | 8,426 | → POS CCN **89.8%**; → facility-affiliation CCN 0.2% | FQHC sites ↔ CMS provider-of-services (not the hospital affiliation file) |
| NPDB practitioner # | NPDB | 985,019 | — | anonymized per-practitioner key inside NPDB only (1.9M reports) |
| PECOS associate id (hospice) | hospice enrollments | 5,372 | → PECOS PAC id **93.1%** | hospices join the PECOS ownership axis |
| POS cross-ref provider # | CMS POS | 5,557 | → POS CCN **97.3%** | predecessor-CCN pointer (facility lineage) |
| Nursing-home chain id | CMS nursing home / 411 / SNF enrollments | 635 / 617 / 635 | CMS ↔ 411 90.7% | chain = owner group; no chain master table |
| Medicaid vendor # (POS) | CMS POS | 4,374 | — | 10% filled; state-issued; no partner |

### B2. Environment

| ID system | Where | Distinct | Edge | Read |
|---|---|---:|---|---|
| TRI EPA registry id | TRI facility | 64,728 | → FRS registry **99.9%** | TRI ↔ FRS solid (use this column, not FRS_ID) |
| TRI parent-company DUNS | TRI facility / basic 2023 | 10,736 / 3,792 | → contracts DUNS 19.6%; → subawardee DUNS 10.1%; → assistance DUNS 5.4%; → FMCSA 4.5% | polluter's parent ↔ federal money — the DUNS universe now has 7 carriers |
| NRC incident seq # | USCG NRC incidents / reports | 1,029,020 / 116,662 | reports → incidents **100%** | spill/incident ↔ report detail |
| NFIP community id | NFIP status book (2 twins) | 25,122 | twins | community ↔ flood-program status; joins FEMA disasters by place, not id |
| EPA AQS site (state+county+site) | AQS sites | 20,994 composite | — | monitor identity; joins by place |
| WQP monitoring location id | WQP stations | 5,818 | — | USGS-prefixed; ↔ USGS site # (same namespace) |
| CAMPD / GHGRP parent (text) | CAMPD facility / GHGRP facility | 4,858 / 14,012 | — | owner names with % shares — name overlay only |

### B3. Banking / housing

| ID system | Where | Distinct | Edge | Read |
|---|---|---:|---|---|
| FDIC UNINUM | FDIC institutions | 27,836 | — | 1:1 with CERT |
| FDIC NEWCERT / ULTCERT / PARCERT | FDIC institutions | 7,953 / 5,199 / 50 | → CERT 99.9% / 99.8% / 100% | successor and ultimate-parent bank pointers resolve — bank lineage is joinable |
| FDIC RSSDHCR (holding co) | FDIC institutions / SOD | 8,736 / 9,729 | → bank RSSD 0.0%; FDIC ↔ SOD 82.9% | holding companies are NOT banks: 8.7K parent RSSDs with **no holding-company table held** |
| FHLB member ids | FHFA FHLB membership | FHFA 6,327 · CERT 3,984 · RSSD 3,984 · NCUA 1,638 · **NAIC 618** | → FDIC CERT 100%; → FDIC RSSD 99.8%; → NCUA charter **98.8%** | a 4-way bank/credit-union crosswalk; NAIC ids = first insurance key in-house (622 insurers) |
| SBA lender FDIC # / NCUA # | SBA 7(a)/504 loans | 3,950 / 589 | → FDIC CERT **99.7%**; → NCUA **96.8%** | lender ↔ bank — SBA loans join the bank axis |
| PPP lender location ids | PPP (2 twins) | 5,037 / 4,533 | — | SBA-internal lender key; no partner |
| HMDA legacy respondent id (+ agency) | HMDA historic (19.1M rows) | 6,936 | agencies 1–3 (bank regulators) → FDIC CERT **69.8%**; agency 7 (HUD) is EIN-shaped: → BMF 0.3%, → Form 5500 EIN 6.2% | half the pre-2018 HMDA rows (HUD-regulated lenders) key on EIN; bank rows key on CERT. Namespace by agency. |
| HMDA ARID→LEI crosswalk | CFPB xref | 5,399 | LEI → GLEIF **100%**; ARID (agency stripped) → FDIC CERT 47.4%; → HMDA LEI 8.6% | the official legacy→LEI bridge is held and resolves |
| FHA mortgagee # / sponsor # | HUD FHA snapshot | 962 / 148 | sponsor → mortgagee 81.6% | HUD lender ids; no partner |
| HUD Section 8 contract # / property id | HUD MF contracts | 24,308 / 23,610 | — | property ↔ contract (internal) |
| USDA RD borrower id | RD multifamily | 12,397 | — | one table |

### B4. Securities / corporate

| ID system | Where | Distinct | Edge | Read |
|---|---|---:|---|---|
| SEC series id / class id | investment-company series-class; MMF | 19,340 / 43,121; 320 / 1,048 | MMF → series-class 98.1% | fund identity; class ticker 28,844 (fund tickers are NOT in the company-tickers file: 0.02%) |
| SEC 1940-Act / 13F / insider file # | series-class 2,038; 13F 16,341; insider 10,904 | — | registrant filing series across three SEC files (untested pairwise) |
| FINRA CRD # | 13F filers (13.7% fill) | 6,229 | — | first CRD in-house; partner (IAPD/BrokerCheck) not held |
| PCAOB firm / issuer / partner ids | Form AP | 737 / 33,323 / 9,305 | issuer CIK → insider issuer CIK 34.2%; → DERA quarterly 20.1% | audit firm ↔ issuer ↔ engagement partner; CIK bridge works |
| ISO MIC | MIC registry | 2,864 | LEI → GLEIF 99.8% | venue identity |
| GLEIF registration-authority entity id | GLEIF | 3,007,097 | UK subset (110,426) → Companies House **85.7%**; US-DE 132,901 Delaware file numbers | national company numbers for 3M entities; only the UK registry is held to receive them |
| GLEIF successor LEI | GLEIF | 27,279 | → GLEIF 100% | entity lineage |
| GLEIF Level-2 parent links | GLEIF relationships | 301,482 children → 77,251 parents | start → GLEIF 99.3%; end → 99.8% | ultimate-consolidated 132.6K · direct 126.4K · fund-managed 149.4K · subfund 73.2K · branch 1.9K — **the corporate parent tree, already held** |
| FARA registration # | FARA bulk | 7,060 | — | registrant identity |
| IRS group exemption # | BMF | 3,990 | — | nonprofit umbrella groups (churches, chapters) |
| FMCSA MC / FF / MX docket | FMCSA census | 1,718,406 / 27,749 / 24,082 | — | operating-authority number, 40% of carriers |
| FMCSA prior-revoked USDOT | FMCSA census | 557 | → USDOT 99.8% | reincorporation pointer (tiny) |
| FMCSA DUNS | FMCSA census | 372,261 | → contracts DUNS 3.5%; → assistance 1.3% | 7th DUNS carrier |
| SAM exclusion NPI | SAM exclusions | 4,867 | → NPPES **99.7%**; → LEIE **96.3%** | SAM ↔ LEIE ↔ NPPES three-way on NPI |
| SAM exclusion UEI | SAM exclusions | 38,427 | → SAM entity registry 0.3% | excluded parties are not registered entities — expected, not broken |
| SAM DoDAAC | SAM entity | 579 | → contracts office code 0% | different namespace |
| USCG party id / HIN | USCG documentation | 301,539 / 120,004 | UK sanctions HIN → 0 (UK column empty) | vessel owner key; HIN partner not held |
| CSL entity # | consolidated screening list | 19,637 | → OFAC SDN ent # **96.7%** | same number — CSL is SDN + others |
| UK sanctions IMO | UK list | 663 | → SDN IMO 43.9%; → AIS 1.4%; → USCG 0% | UK ↔ US sanctioned fleets overlap by half |
| OpenSanctions ids | default (1.28M) | 1,281,846 | identifiers blob: wikidata Q 364K, IMO 6.6K | cross-regime identity; the blob needs parsing to become keys |
| EU ref # / UK OFSI group / UN ref | EU 5,994 / UK 5,127 / 995 | — | regime-native ids |

### B5. Labor / justice / transport / procurement

| ID system | Where | Distinct | Edge | Read |
|---|---|---:|---|---|
| OSHA ITA establishment id | 300A summaries 2023/24/25 | ~395K/yr | 2024 → 2023 55.2% | establishment persists ~half year-to-year |
| OSHA ITA EIN | 300A 2024 | 114,606 | → Form 5500 EIN 27.8%; → BMF 5.6% | injury logs ↔ benefit plans by EIN — a new EIN carrier |
| OSHA host establishment key | inspections | 1,546,481 | — | 55% fill; inspection ↔ establishment |
| Form 5500 sponsor EIN (FULL) | 4.3M rows | 466,446 | → BMF 6.2%; → OSHA EIN 6.8% | (the 33K sample's sponsor-EIN column is empty — use FULL) |
| ICE detention facility code | stints / codes | 707 / 1,490 | stints → codes **99.7%** | 2.6M stints · 1.01M people · 1.09M stays |
| MPV ORI / WaPo / Fatal Encounters ids | Mapping Police Violence | 4,878 / 10,381 / 9,851 | — | ORI present, no ORI master held |
| CourtListener predecessor / supervisor / parent court | positions / courts | 139 / 130 / 128 | → judges 100%; → courts 100% | tiny but perfect |
| FAA N-number / Mode S / registry id | FAA registry | 315,447 each | NTSB N-number → FAA **44.7%** (registry is current-only) | crash ↔ current owner |
| NTSB operator cert # / code / airport ids | NTSB aircraft | 740 / 1,123 / 6,881 | — | mostly blank (96%) |
| FRA accident # / parent railroad code | FRA | 174,438 / 1,091 | parent → reporting code 70.6% | railroad lineage |
| AIS MMSI | NOAA AIS (58M pings) | 22,759 | — | no MMSI partner held |
| CPSC NEISS case # / CFPB complaint id | 9.8M / 17.2M | — | event identity, no partner |
| Subaward number / SAM report id | subawards | 2.1M / 4.7M | prime FAIN → assistance 55.9% | |
| Subawardee UEI / parent UEI | subawards | 220,704 / 74,245 | → SAM **67.2% / 67.9%** | |
| Recipient parent UEI | contracts R2 / assistance | 563,618 / 53,380 | → SAM 31.6% / **73.9%** | parent-company pointers resolve for grants, half-resolve for contracts (historic UEIs) |
| NIH org UEI / DUNS / PI profile | RePORTER | 12,050 / 15,054 / 262,757 | UEI → SAM **80.0%** | research orgs ↔ SAM |
| SBIR UEI / contract # / tracking # | SBIR-STTR | 17,161 / 156,779 / 171,228 | UEI → SAM 70.8%; contract → PIID 9.3%; tracking → NIH core 9.8% | |
| Contracts parent award PIID (IDV) | contracts 20M copy | 386,831 | → contracts PIID 0.2%; → subaward parent PIID 2.7% | **IDV (umbrella contract) file is not held** — 387K parent ids point nowhere |
| EIA transmission-owner id / ownership id | EIA 860 | 1,080 / 1,945 | → utility id 51.2% / 15.7% | owners are often non-utilities; no owner master |
| EIA FERC dockets (QF / EWG) | EIA 860 plant | 4,550 / 1,197 / 440 | — | first FERC ids; no FERC table |
| FEC committee → candidate | committees | 6,921 | → candidates 99.8% | |
| Bill sponsor / cosponsor bioguide | govinfo | 632 / 635 | → VoteView 100% | |

## C. Parent / owner pointer resolution — summary

| Pointer | Fill | Resolves to | Rate | What it buys |
|---|---:|---|---:|---|
| GLEIF L2 child → parent LEI | 100% | GLEIF | 99%+ | 301K-company parent tree |
| FDIC successor / ultimate cert | 100% / 97% | FDIC CERT | ~100% | bank merger lineage |
| FDIC holding-company RSSD | 61% | (nothing held) | 0% | needs the Fed NIC holding-company file |
| Assistance recipient parent UEI | 21% | SAM | 74% | grant recipient → parent |
| Contracts recipient parent UEI | 94% | SAM | 32% | contract recipient → parent (older UEIs missing from current SAM) |
| Subawardee parent UEI | 52% | SAM | 68% | |
| TRI parent DUNS | 58% | contracts DUNS | 20% | polluter → parent → federal money |
| POS cross-ref provider # | 13% | POS CCN | 97% | facility predecessor |
| Hospice associate id | 100% | PECOS PAC | 93% | |
| Nursing-home chain id | 71% | (no master) | — | 635 chains, names only |
| CourtListener predecessor / supervisor / parent court | <1% / 84% | judges / courts | 100% | |
| CourtListener parent docket | 0% | — | — | column empty on 71.7M rows |
| FMCSA prior-revoked USDOT | 0.01% | USDOT | 99.8% | |
| FRA parent railroad code | 100% | railroad codes | 71% | |
| EPA corporate crosswalk parent LEI / CIK / UEI | 0.7% / 2.3% / 8.1% | GLEIF / CIK / SAM | 100% / 94% / 55% | fuzzy overlay, but its pointers are real ids |
| NPPES parent org TIN | — | masked | — | LBN name only (56K) |
| NIH org IPF code | 0% | — | — | empty |
| Treasury MTS parent id | 86% | self | 100% | receipts hierarchy (trivia) |

## D. Verified DEAD, empty, or stub (add to the pass-1 list)

| Column / table | Finding |
|---|---|
| ISIN (US SEC EDGAR table) | 48,990 rows, 100% blank |
| CourtListener PARENT_DOCKET_ID | empty on 71.7M rows |
| NIH ORG_IPF_CODE | empty on 2.1M rows |
| Form 5500 (33K sample) SPONSOR_DFE_EIN | empty; the FULL table's SPONS_DFE_EIN is the real one |
| UK sanctions HIN | empty |
| NSF awards EIN | 125-row stub, all blank |
| TRI FRS_ID | dead (use EPA_REGISTRY_ID) |
| SNF affiliation entity id | it is CHAIN_ID, not a PECOS id |
| FDA 510(k) / PMA / establishment / enforcement / CAERS | 88 / 29 / 166 / 20 / 1-row RAW stubs |
| BTS carrier code, ED FSA datacenter, grants.gov | 21 / 1 / 100-row stubs |
| NTSB operator cert #, operator code | 96% blank |
| SEC class ticker → company tickers | 0.02% — fund tickers are a different universe (not dead, just no partner) |

## E. The 08-05 catalog, reconciled

- 747 candidates: 493 marked "not held", 254 marked "might have".
- Of the 254 "might have": every one with a plausible column was value-checked across pass 1 + pass 2; ~120 resolved to real columns (sections B here + G1 in pass 1), the rest are either classification codes, stubs, or genuinely absent.
- Of the 493 "not held": **37 are wrong** — held today: GUDID, NPDB, FAERS, DMF, NID dams, USCG official #, WQP/STORET, CRD (thin), UK PSC (15.8M), OpenSanctions, PBGC plans, LDA ids, IRS 527 reports, NTSB event #, FMCSA MC #, FAC single-audit ids (411K), EIA plant/utility ids, PHMSA operator id, GIIN, Retraction Watch (71,608 rows incl. DOI + PubMed ids). Parsed catalog: `reports/recon/pass2/catalog747_parsed.csv`.

## F. Genuinely NOT held — the acquisition ledger that survives value-checking

Ranked by how many held tables it would light up. Free bulk unless noted.

| # | Missing key / file | Would connect | Held side waiting |
|---|---|---|---|
| 1 | **IDV / parent-award file** (USAspending IDV download) | 387K umbrella contracts → their task orders | contracts (20M + 93M rows) point at it |
| 2 | **Fed NIC holding-company file** (RSSD attributes + relationships) | 8.7K bank holding companies → banks | FDIC RSSDHCR, SOD RSSDHCR, FHLB FED_ID |
| 3 | **Delaware / state SoS registries** | 132,901 Delaware file numbers already on GLEIF | GLEIF RA entity id (3.0M) |
| 4 | **MAUDE + device recalls** (overnight load unchecked) | 5.2M GUDID devices → adverse events / recalls | GUDID DI, FDA application # |
| 5 | **Orange Book / Drugs@FDA approvals** | 13,093 NDA/ANDA/BLA numbers → sponsors, patents, exclusivity | NDC directory application # |
| 6 | **FINRA IAPD / BrokerCheck (Form ADV bulk)** | 6,229 CRDs on 13F filers → adviser discipline | 13F filers CRD |
| 7 | **ORI master (LEAIC / FBI CDE agencies)** | 4,878 police ORIs → agency attributes, UCR/NIBRS | MPV ORI column |
| 8 | **NAIC company master / state insurer lists** | 618 insurer NAIC ids → the insurance domain | FHLB membership NAIC id, HIOS issuer id |
| 9 | **MMSI registry (ITU MARS / FCC ship stations)** | 22,759 AIS MMSIs → owners | AIS, USCG (no MMSI) |
| 10 | **FERC eLibrary / EQR respondent ids** | 4,550 QF dockets + 1,197 EWG dockets | EIA 860 plant |
| 11 | HUD chain / nursing-home ownership (PECOS ownership file) | 635 nursing-home chains → owners | CMS nursing home CHAIN_ID |
| 12 | SEC company-tickers for FUNDS (or CRSP mutual fund map) | 28,844 fund class tickers | series/class table |
| 13 | ATF FFL list | unknown status — loader exists, table not confirmed | — |
| 14 | OCC charter #, USPTO trademarks, VA facility ids, API well #, GSA MAS #, Ginnie/GSE loan ids, NLRB case #, FSIS est #, CompTox DTXSID, 340B ids, OLMS LM file #, PBGC case #, EA #, ROR / OpenAlex / PMID / DOI, IARD, ASR #, USAC SPIN, PHMSA hazmat report # | (catalog STEEL + free bulk, confirmed absent) | various |

Closed by design (no bulk): SSN / MBI / HICN, FinCEN id, EEOC charge #, USCIS numbers, CDLIS, NCIC, CODIS, POST decertification (state-by-state), MERS MIN, CRD disciplinary docs, IBAN/UETR.

## G. Contradiction / trap flags from this pass

- HMDA legacy respondent id is **two namespaces in one column**: bank-regulator rows = FDIC cert (70% resolve), HUD rows = EIN-shaped for-profit lenders. Register with agency code as part of the key.
- NADAC NDC (11-digit 5-4-2) vs NDC directory (labeler-product with dash, 4/5-3/4): only joins after zero-padding to 5-4; raw string join gives 0%.
- FMCSA DUNS shows 3.85M "junk" because 86% of carriers report 0 — the 372K real values are fine.
- SAM exclusions UEI not resolving into the SAM entity file is expected (excluded parties are people and defunct firms), not a load failure.
- Contracts "parent award PIID" is an IDV id; joining it to the contracts PIID column is the wrong test — the IDV file is a separate download.

## H. Level-3 precision check (2026-08-29, 23:14) — are the matched pairs the same real thing?

Method: 60 random matched key pairs per edge (41 edges), names normalized (corporate suffixes dropped) and compared by
token overlap / containment; state codes compared where both sides carry one. Script:
`scripts/pass2_precision_check_2026_08_29.py`; raw with mismatch examples: `reports/recon/pass2/pass2_precision_2026-08-29.json`.
Name agreement is a floor, not the precision: lineage edges, site-vs-org keys, and renamed firms score low on names while the key
is right. Verdicts below account for that by reading the mismatch examples.

| Edge | pairs | names agree % | states agree % | verdict | why |
|---|---:|---:|---:|---|---|
| Drug price NDC -> drug label NDC | 60 | 86.7 | — | **SOLID** | brand vs generic naming; every mismatch is the same molecule |
| Clinic NPI -> provider registry | 60 | 35.6 | — | **SOLID (site->org key)** | clinic row carries the PARENT org's NPI; names differ site vs org, org family matches on inspection |
| Clinic Medicare billing # -> provider-of-services CCN | 60 | 58.3 | 100.0 | **SOLID (site->org key)** | same: site name vs org name; states 100% |
| Hospice associate id -> PECOS PAC id | 60 | 100.0 | 98.3 | **SOLID** |  |
| Predecessor CCN -> CCN (lineage; names may differ) | 60 | 56.7 | 100.0 | **SOLID (lineage)** | names differ by design; states 100% |
| Nursing-home chain id CMS -> 411 | 60 | 100.0 | — | **SOLID** |  |
| TRI EPA registry id -> FRS registry | 60 | 70.0 | 100.0 | **SOLID (site key, name drift)** | mismatches are ownership changes at the same site; states 100% |
| TRI parent DUNS -> contract recipient DUNS | 60 | 73.3 | — | **SOLID** | mismatches are abbreviations / post-merger names of the same firm |
| FDIC successor cert -> cert (lineage; state) | 60 | 25.0 | 90.0 | **SOLID (lineage)** | successor is a different bank by definition; states 90% |
| FHLB member cert -> FDIC cert | 60 | 93.2 | 100.0 | **SOLID** |  |
| FHLB member Fed id -> FDIC Fed RSSD | 60 | 96.7 | 96.7 | **SOLID** |  |
| FHLB member NCUA id -> credit-union charter | 60 | 98.3 | 100.0 | **SOLID** |  |
| SBA lender FDIC # -> FDIC cert | 60 | 98.3 | 100.0 | **SOLID** |  |
| SBA lender NCUA # -> credit-union charter | 60 | 98.3 | 100.0 | **SOLID** |  |
| HMDA legacy id (agency-stripped) -> FDIC cert | 60 | 56.7 | — | **SUSPECT** | ~half the pairs are different banks (e.g. 'Community National Bank' vs 'Citizens State Bank of Nevada, MO'); the stripped id is not a cert for every agency |
| HMDA xref LEI -> global LEI registry | 60 | 93.3 | — | **SOLID** | the few misses are the xref's own name-column errors |
| Market-venue LEI -> global LEI registry | 60 | 91.2 | — | **SOLID** |  |
| LEI national company # (UK) -> Companies House | 60 | 100.0 | — | **SOLID** |  |
| Screening-list entity # -> OFAC SDN # | 60 | 100.0 | — | **SOLID** |  |
| UK-sanctioned ship IMO -> OFAC IMO | 60 | 71.7 | — | **SOLID (hull key, name drift)** | sanctioned ships rename; IMO is the immutable hull number |
| SAM exclusion NPI -> provider registry (people) | 60 | 96.2 | — | **SOLID** | 2 of 52 surnames differ (name change or NPI reuse) |
| SAM exclusion NPI -> health exclusion list | 60 | 100.0 | 100.0 | **SOLID** |  |
| ICE stint facility code -> facility codes | 60 | 95.0 | 100.0 | **SOLID** | name mismatches are facility aliases; states 100% |
| Crash N-number -> FAA registry (serial #) | 60 | 90.0 | — | **SOLID** | serial numbers agree 90%; N-numbers get reassigned, so the 10% are reissued tail numbers |
| Rail parent code -> reporting railroad code | 60 | 100.0 | — | **SOLID** |  |
| Subawardee UEI -> SAM registrant | 60 | 96.7 | 98.3 | **SOLID** |  |
| Grant recipient parent UEI -> SAM registrant | 60 | 100.0 | — | **SOLID** |  |
| Contract recipient parent UEI -> SAM registrant | 60 | 100.0 | — | **SOLID** |  |
| Contract CAGE -> SAM CAGE (pass-1 edge) | 60 | 98.3 | 93.1 | **SOLID** | 1 of 60 is a CAGE reassigned to a new firm |
| NIH org UEI -> SAM registrant | 60 | 82.5 | — | **SOLID** | misses are affiliates registered under a sibling legal name |
| SBIR UEI -> SAM registrant | 60 | 98.3 | 0.0 | **SOLID** | names 98%; the SBIR 'state' column is not a state code (0% agreement) — column-semantics flag, not a key problem |
| Device-maker DUNS -> contract recipient DUNS | 60 | 96.7 | — | **SOLID** |  |
| Trucker DUNS -> contract recipient DUNS | 60 | 88.3 | 80.0 | **SOLID** | states 80% (HQ vs place of performance) |
| Transmission owner id -> EIA utility id | 60 | 100.0 | — | **SOLID** |  |
| Plant owner id -> EIA utility id | 60 | 100.0 | — | **SOLID** |  |
| Bill sponsor bioguide -> member roster | 60 | 76.7 | — | **SOLID** | nickname vs legal first name |
| Audit issuer CIK -> insider-filing issuer CIK | 60 | 93.3 | — | **SOLID** | misses are corporate renames under the same CIK |
| EPA crosswalk parent UEI -> SAM registrant | 60 | 100.0 | — | **SOLID (n=6)** | tiny sample |
| US-documented vessel IMO -> AIS IMO (pass-1 edge) | 60 | 100.0 | — | **SOLID** |  |
| US-documented call sign -> AIS call sign (pass-1 edge) | 60 | 93.3 | — | **SOLID** |  |
| Committee's candidate id -> FEC candidate (office state) | 60 | 25.0 | 90.0 | **SOLID (by construction)** | committee names aren't candidate names; office state 90% |

**Net:** 40 of 41 edges hold at level 3. **One is downgraded: the legacy HMDA respondent id → FDIC cert edge** (agency-stripped
form) is ~half wrong — the pre-2018 respondent id maps to a cert for some agencies and to something else (likely RSSD or an OCC
charter) for others. Keep it out of the map until it is split by agency and re-tested. The official ARID→LEI crosswalk (edge 16)
is the safe route into that data instead.

Column-semantics flag: the SBIR awards "state" column is not a state code (0% agreement with SAM on 60 true-name matches).

## PARKED for later passes

- Time / place joins (1,275 date columns; place columns: the 2026-08-30 value scan verified 2,238 live-measured — see reports/location_index/LOCATION_VALUES.md; 2,244 was the earlier name-scan figure and includes 36 false coordinate hits).
- Parsing the OpenSanctions and CSL `IDENTIFIERS` blobs into typed keys (IMO, tax ids, USCC, wikidata).
- Pairwise tests among the three SEC file-number columns and the four FDIC/FHLB/SBA/NCUA bank ids.
- Registering the pass-2 families in the spine (a spec batch, not a rebuild — apply-config handles it).
