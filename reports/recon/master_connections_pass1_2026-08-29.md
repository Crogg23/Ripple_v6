# Master Connections List — PASS 1: beyond reasonable doubt (2026-08-29)

Scope: NOUN connections only (IDs, keys, crosswalks, ownership pointers). Time and geography
links are parked in a separate section at the end. "Beyond reasonable doubt" = value-verified
against live warehouse data in a prior session (live SQL, COUNT DISTINCT, measured overlap).
Name-scan-only candidates and web-research candidates are NOT in this pass (see Pass 2 scope).

Evidence sources: join-layer audit 2026-08-27; measured edge table snapshot 2026-08-28/29;
bucket-B live verification 2026-08-29; value-shape sniffer 2026-08-18; CourtListener edge
verification 2026-08-17; spine connection audit 2026-08-11; 2026-08-05 sweep section 1; bridge-fuel
memory 2026-06-24; unregistered-ID recon 2026-08-28.

Note on match %: share of the left table's ID values found in the right table. For one-to-many
crosswalks (facility to provider) the rate can exceed 100 — a counting artifact, not an error.

## A. Hard-ID families — wired, measured, connecting today (22)

| ID system | Issuer | Links what | Tables | Measured edges | Median match % | Edges >=80% | Verdict |
|---|---|---|---|---|---:|---:|---|
| NPI | CMS | health providers (people + orgs) | 34 | 364 | 59 | 137 | solid — biggest connector (117M matched pairs) |
| EIN | IRS | employers / nonprofits / orgs | 34 | 366 | 7.5 | 69 | solid where it fires; low median = many small-overlap pairs |
| CCN | CMS | certified facilities | 25 | 78 | 98.5 | 72 | solid |
| CIK | SEC | SEC filers | 19 | 128 | 82 | 69 | solid |
| FRS_ID | EPA | regulated facilities | 18 | 136 | 83 | 70 | solid (56.9M matches) |
| FEC_CMTE_ID | FEC | political committees | 11 | 45 | 67 | 15 | solid |
| FEC_CAND_ID | FEC | candidates | 10 | 36 | 75 | 16 | solid |
| PWSID | EPA | public water systems | 10 | 45 | 99.3 | 42 | solid |
| NPDES_ID | EPA | water discharge permits | 10 | 45 | 75 | 22 | solid |
| UEI | SAM.gov | federal award recipients | 7 | 18 | 10 | 1 | solid ID, thin overlaps |
| LEI | GLEIF | legal entities (global finance) | 7 | 21 | 81 | 11 | solid |
| CL_PERSON_ID | CourtListener | judges | 8 | 28 | 92 | 17 | solid (99.2–100% referential, 19/20 surfaces) |
| BIOGUIDE | Congress | members of Congress | 5 | 10 | 100 | 10 | solid |
| CL_COURT_ID | CourtListener | courts | 4 | 6 | 100 | 5 | solid (100% on 71.7M dockets) |
| NCUA_CHARTER | NCUA | credit unions | 4 | 6 | 100 | 6 | solid |
| ICPSR | VoteView | legislators (historical) | 3 | 3 | 100 | 2 | solid, small |
| MINE_ID | MSHA | mines | 3 | 3 | 100 | 3 | solid (quote-wrapped values, normalizer handles) |
| ICE_FACILITY | ICE | detention facilities | 3 | 3 | 84 | 2 | solid |
| COMPANY_NO | UK Companies House | UK companies | 2 | 1 | 97 | 1 | solid, closed 2-table island |
| DUNS | D&B | orgs pre-2022 awards | 3 | 3 | 46 | 0 | real ID; 94% of values orphaned (assistance-table DUNS never ingested) |
| DEA_NO | DEA | controlled-substance registrants | 1 | 0 | — | — | real ID (148.6K distinct); one-sided, no second table |
| IMO | IMO | ships | 2 | 0 | — | — | real ID (8.7K); indexed, 0 edges built |

Registered but NOT in this pass: PATENT (0 carrying columns — dead), MMSI (one-sided, not indexed).

## B. Hard-ID families — value-verified 2026-08-29, wired in code, not yet in the map (8 + 3)

| ID system | Issuer | Links what | Live evidence |
|---|---|---|---|
| CAGE | DLA | defense contractors: contracts to SAM exclusions | 246,832 distinct; 55.4M of 93.2M contract rows filled; 46% of exclusion CAGEs found in contracts |
| AWARD_KEY | USAspending | prime award to subaward to assistance | 74.5M / 14.25M / 280K distinct; subawards to contracts 39.4% (contracts copy stops FY2021) |
| PECOS_PAC_ID | CMS | provider enrollment to facility affiliation to hospital/SNF enrollment | 2.46M distinct; 98.6–99.7% overlap |
| PECOS_ENRLMT_ID | CMS | enrollment record to hospital enrollment file | 2.98M; 99.2% |
| FDIC_CERT | FDIC | banks: institution master to branches to FHLB members | 27,830; 99.9% / 99.97% (after zero-pad) |
| RSSD | Federal Reserve | banks to holding companies | 26,576; 98.5%; parent column 74–83% |
| EIA_PLANT_ID | EIA | power plants to generators to owners to eGRID emissions | 16,128; 100% / 100% / 98.6% |
| EIA_UTILITY_ID | EIA | utilities to plants to eGRID | 6,643; 100% / 94.6% / 22% (861 = different universe) |
| MSHA_CONTROLLER_ID | MSHA | parent company behind mines / violations / accidents | 41,050 distinct; 93–99% filled; 4,686 cross-match live (verified 08-05, registered 08-28) |
| MSHA_OPERATOR_ID | MSHA | mine operator to violations | 100% filled on violations (verified 08-05, registered 08-28) |
| CUSIP | CUSIP Global | securities across 13F holdings / positions / fails-to-deliver | registered 08-28, edges unmeasured |

## C. Translations / crosswalks — verified to exist

| Crosswalk | Held as | Evidence | Honest read |
|---|---|---|---|
| CCN to NPI (facility to provider) | CMS facility-affiliation table, 2.24M rows | 938K NPIs x 41K CCNs, 0 masked; 373 bridged edges, 244 >=80% | SOLID — the one crosswalk that really fires |
| CIK to EIN | derived from SEC filings carrying both | 85 bridged edges, median 0.1% | exists, thin coverage |
| EIN to UEI | derived from award tables carrying both | 52 bridged edges, median 1.2% | exists, thin coverage |
| DUNS to UEI | derived from award tables carrying both | 2 edges, 0.1% | exists, near-empty (DUNS ingestion gap) |
| FJC court ID on CourtListener courts (200 rows) | column on courts table | verified 08-17 | bridge OUT of the CourtListener namespace, unwired |

## D. Value-verified ID columns not yet registered as families

| Column family | Table | Live evidence | Links what |
|---|---|---|---|
| NPPES "other provider identifier" slots (200 cols) | NPPES | slot 1: 1,559,317 filled / 1,343,026 distinct (type 05 = state Medicaid IDs) | NPI-world to state Medicaid / legacy Medicare IDs |
| State license number + state (15 slots) | NPPES | slot 1: 5,777,222 filled / 3,909,402 distinct | provider to state licensing boards (composite key only) |
| OFLC case number | DOL foreign labor | 664,616 rows, 100% filled, 100% distinct | H-1B / PERM / H-2A case identity |
| Plan number (SPONS_DFE_PN) + EIN | DOL Form 5500 | 100% filled, 266 distinct; PLAN_NUM is 0% (trap) | EIN+PN = one specific benefit plan (DOL/PBGC standard) |
| UPIN | LEIE exclusions | 474 distinct | retired Medicare ID to NPPES UPIN slots |
| Ticker | Senate stock watcher | 1,029 distinct | name-only trades to CIK via public ticker-to-CIK map |
| LDA registrant / client IDs | Senate lobbying | 9,245 / 2,057 distinct | lobbying registrant to client to filing |
| FJC judge NID | FJC judge + appointment | 2-table match | judge to appointment |
| FEC near-miss columns (FEC_ID, CAND_IDS, CMTE_IDS JSON arrays, MEMBER_KEY) | politics marts | formats unambiguous | same FEC / Bioguide families under other names |
| FEC positional-header columns (C1/C4/C10/C15) | 4 multi-cycle FEC history tables | wired 08-18 (51–58% in spine) | committee / candidate IDs in the bigger twins |
| OpenSanctions consolidated list | 71,011 rows | live, blends OFAC + UN + EU + UK + PEP | sanctions identity across regimes |

## E. Verified DEAD or masked (do not count, do not re-try)

| Column | Why |
|---|---|
| NPPES EIN / parent TIN | masked (UNAVAIL / blank, 2 distinct over 9.6M) |
| FCC licensing EIN | 100% non-null, 1 distinct (empty) — redacted; FRN on the same table is real (1.2M distinct) |
| Nursing-home NPI + provider number | empty |
| FDIC LEI | empty |
| TRI facility FRS column | dead |
| Form 5500 PLAN_NUM | 0% filled |
| CourtListener APPOINTER_ID | 47% match — not a person reference |
| Open Payments RECORD_ID, FAERS ISR | NPI-shaped, fail Luhn — sequence IDs, not NPIs |
| Senate LDA registrant IDs vs SEC CIK | below chance |
| DOCKET (as one family) | ~40% wrong — FDIC cert numbers collide with SCOTUS dockets; needs issuer namespace |
| EPA corporate crosswalk table | fuzzy name matching — overlay, never a key |

## F. Confident non-ID matches (measured precision)

| Method | Measured precision | Where |
|---|---|---|
| Name + ZIP / name + county corroboration | 75–85% precise where it fires; median match rate 0.7% across all pairs | 2,513 edges; 26 tables reachable only this way |
| UEI debarment x contracts, name-checked | 99 / 102 | spine audit 08-11 |
| NPI exclusions x open payments, surname-checked | 336 / 350 exact (rest hyphen variants) | spine audit 08-11 |

## G. Live check run 2026-08-29 (this session) — the 08-05 sweep's "probably already have" list + bucket B, value-checked

Method: 95 candidate ID systems name-matched against 78,694 live landing columns (391 columns hit);
every hit got COUNT(*), COUNT(col), COUNT(DISTINCT non-blank) and a 3-value sample. Raw results:
reports/recon/sweep_live_check_2026-08-29.json. Portal-crawl tables ignored. ~$1 compute.

### G1. VERIFIED LIVE — real ID columns, high distinct counts (new to pass 1)

| ID system | Where (landing) | Distinct non-blank | Cross-table? | Links what |
|---|---|---:|---|---|
| PIID (contract number) | contracts R2 / contracts / 20M copy | 63.1M / 5.7M / 14.0M | 3 copies of the same source | contract identity (award key already registered) |
| FAIN / URI (grant numbers) | assistance | 10.3M / 8.0M | one table | grant identity |
| EDGAR accession # | 6 quarterly DERA submission tables | 6–7.7K each | 6 twins | filing identity |
| Ticker → CIK map | SEC company-tickers (2 tables) + FTD CUSIP bridge + Senate trades | 10,414 / 14,881 / 1,009 | YES — the public ticker→CIK map is already in-house | name-only Senate trades → CIK |
| SEC file number | insider reporting-owner table | 10,904 | one table | registrant filing series |
| FEC filing id (FILE_NUM) | individual contributions / committee-to-candidate / independent expenditures | 105,649 / 49,031 / 16,980 | 3 FEC tables | filing ↔ transactions |
| Aircraft serial number (MSN) | FAA registry + NTSB aircraft | 247,464 / 25,027 | YES — FAA registry ↔ NTSB events | aircraft identity across crash and ownership |
| FRA grade-crossing id | FRA crossing incidents + equipment accidents | 100,886 / 8,460 | YES | crossing ↔ incidents |
| Railroad reporting code (AAR mark) | FRA casualties + crossing incidents | 1,288 / 1,066 | YES | railroad company across FRA files |
| Call sign (ships/radio) | FCC licensing 1.6M; NOAA AIS 17,437; OFAC SDN 899; screening list 921 | see left | YES — AIS ↔ OFAC ↔ FCC candidate ship bridge (overlap not yet measured) | vessel / licensee identity |
| FCC FRN | FCC licensing | 1,198,925 | one table | licensee identity (the real column next to the masked EIN) |
| Benefit plan number (EIN+PN) | Form 5500 FULL (4.3M rows) 999 distinct; PBGC trusteed plans PN 127 | composite | YES — DOL 5500 ↔ PBGC | one specific pension/benefit plan |
| GHGRP facility id | GHGRP facility + emission | 11,358 / 11,277 | YES (2 GHGRP tables) | emitter across GHGRP files |
| SDWA facility id | SDWA facilities 224,130; violations/enforcement 50,362 (37% fill) | | YES | water facility ↔ violations |
| TRI facility id | TRI facility 64,990; ECHO TRI_IDS 64,274 | | YES — TRI ↔ ECHO | toxic-release site ↔ enforcement |
| RCRA handler id | ECHO RCRA_IDS 1.5M; Superfund site boundaries EPA_ID 1,908 | | YES | hazardous-waste handler ↔ superfund |
| ICIS program-system ids | FRS program links 4.4M; air facilities 279,728; air compliance 148,280; NAICS/SIC link tables | | YES (EPA internal) | program record ↔ FRS |
| HUC8 watershed / USGS site | HUC8 2,456; USGS water sites 3,767 | | — | watershed / gauge identity |
| NIH application id / project # / core project # | NIH RePORTER | 2.12M / 1.74M / 439K | one table (+ SBIR untested) | research award identity |
| NIH PI profile id | NIH RePORTER | 262,757 | one table | investigator identity |
| Grants.gov opportunity # | NIH RePORTER 19,997 (70% fill); assistance 32,727 (many "NOT APPLICABLE") | | YES | grant ↔ funding opportunity |
| Agency codes / CFDA program # | toptier agencies 111; assistance CFDA 3,191; NIH CFDA 473 | | YES | program grouping (code, not identity) |
| IRS 990 object id / DLN | 990 e-file index | 5.54M / 5.54M | one table | filing identity |
| LDA client / registrant ids | Senate lobbying filings | 88,607 / 11,723 | one table (bigger than the catalog said) | lobbying client ↔ registrant |
| Congressional committee code | committee membership | 228 | one table | member ↔ committee |
| Bill number | govinfo bill status 10,564; cosponsors 10,025; VoteView roll-call meta 16,221 | | YES (composite with congress #) | bill ↔ sponsor ↔ vote |
| FJC judge NID / JID | FJC judges, Article III judges, service | 4,074 / 4,067 | YES (3 FJC tables) | judge ↔ appointment ↔ service |
| CourtListener docket id / cluster id / PACER case id | opinion clusters 9.8M; citations 7.8M; dockets 2.25M PACER ids; oral arguments | | YES (internal glue) | opinion ↔ docket ↔ citation |
| SCDB justice code | SCDB 40; JCS scores 49 | | YES | justice ↔ vote ↔ ideology |
| OSHA inspection id (activity nr) | OSHA inspections | 5,196,412 | one table (violations table untested) | inspection identity |
| PHMSA operator id | PHMSA flagged incidents | 262 | one table | pipeline operator |
| NTSB event id / NTSB # | NTSB events, aircraft, injury | 30,968 across 3 | YES | crash ↔ aircraft ↔ injuries |
| IPEDS UNITID / OPEID | College Scorecard | 6,273 / 6,222 | one table | school identity |
| Open Payments profile id | Open Payments 2022/2023/current + profile supplement | 868K–984K / 1.7M | YES (4 tables) | payment recipient across years |
| HCRIS report record # | HCRIS | 6,103 | one table | cost report identity |
| FEMA disaster # | IA housing registrations (26M rows) | 626 | one table | disaster grouping |
| CVE id | CISA KEV | 1,674 | one table | vulnerability identity |
| HMDA LEI | HMDA 538; HMDA LAR 478; FDIC bank data 2,241 (8% fill); GLEIF 3.38M | | YES — HMDA ↔ GLEIF ↔ FDIC | lender identity (LEI already a family; HMDA carrying it is new) |
| Credit-union RSSD | NCUA call reports | 4,336 | YES — NCUA ↔ Fed RSSD family | credit unions get a Fed id too |
| NID dam id | NID dams (2 twins) | 91,978 | twins | dam identity |
| JPML MDL number | pending MDLs | 161 | one table | multidistrict litigation |
| DEA registrant # | ARCOS buyer 148,588 / reporter 656 | | one table | pharmacy ↔ distributor (internal) |
| FAERS ISR / case id | 5 FAERS tables | 4.27M / 1.52M | YES (internal glue) | adverse-event report across files |
| SBA PPP loan # | PPP (2 twins) | 968,524 | twins | loan identity |
| HUD PHA participant code | public housing authorities | 3,787 | one table | housing authority identity |
| PCAOB firm id | Form AP filings | 737 | one table | audit firm ↔ engagements |
| FATCA GIIN | FATCA FFI list (2 twins) | 516,298 | twins | foreign financial institution identity |
| ICIJ node id | 5 offshore-leaks tables | 814K entities / 771K officers / 402K addresses | YES (internal glue) | offshore entity ↔ officer ↔ address |
| UNII (chemical) | GSRS substances | 168,046 | one table | substance identity |
| NDC | NADAC | 32,881 | one table | drug package identity |
| UPIN | LEIE | 5,786 (not 474) | one table (NPPES UPIN slots untested) | retired Medicare id |
| Product/service code (PSC) | contracts | 3,296 | classification | grouping, not identity |

### G2. Checked — DEAD, stub, or not an identity

| Candidate | Finding |
|---|---|
| FinCEN id | 1 row, value N/A — dead |
| ISIN | column exists on the EDGAR table, 0 non-blank — dead |
| CFTC trader id | only trader COUNTS exist, no ids |
| ATF FFL number | regex hit only offense-level columns; FFL table not confirmed — unknown |
| NSF award id | 125-row stub |
| Grants.gov table | 100-row stub |
| FDIC failed banks / OCC CERT + RSSD | live but float-text (30965.0) — repair before use (known) |
| SAM exclusions CAGE (full R2) | only 0.3% filled (392) — the exclusions side of the CAGE bridge is thin |

### G3. Not found in the warehouse (name scan of 78,694 landing columns)

FMCSA MC/MX/USDOT · EPA ORISPL · CINS · SEC Reg A / Reg CF / municipal-advisor file numbers ·
CAS registry # (portal tables only) · UDI device id (portal only) · FDA 510(k)/PMA (stubs per 08-29 inventory) ·
airport ids (FAA table is a 4-row stub) · LIHTC / HUD project ids · legacy HMDA respondent id ·
OFAC SDN id-document fields and GLEIF registration-authority id (not resolved by this scan — unknown, not absent) ·
FRA accident/incident number (not resolved — unknown).

### G4. Contradiction flag

The 08-17 batch rejected "FDIC LEI" as empty. Today: FDIC bank data LEI = 8.1% filled, 2,241 distinct
(GLEIF-shaped values). Not empty — thin. Worth a second look before it stays rejected.


## H. Landed 2026-08-29 (this session) — the "no-brainer" acquisitions, with measured overlap

Loader: scripts/nobrainer_bulk_load_2026_08_29.py. All raw VARCHAR, provenance stamps, quality gate PASS.

| New table | Rows | Key columns (distinct) | Measured connection to what we already hold |
|---|---:|---|---|
| SAM Entity Management public extract (Aug 2026) | 895,429 | UEI 887,310; CAGE 794,845; **legacy DUNS 0 (column empty — SAM stopped publishing DUNS in the public file)** | contracts CAGE 85,857 / 92,530 found (92.8%); contracts UEI 85,832 / 92,833 found (92.5%) |
| USCG Merchant Vessels (Dec 2025 release, via Wayback) | 391,684 | official # 391,676; IMO 6,304; call sign 75,450 | AIS IMO 2,313 / 6,934 found (33%); AIS call sign 5,759 / 17,437 (33%); OFAC vessel IMOs 0 / 2,030 (sanctioned ships are foreign-flagged — expected) |
| FMCSA Company Census | 4,493,662 | USDOT 4,493,662; DUNS non-zero 372,260 | no DUNS partner in-house (SAM public DUNS empty); name/address only for now |
| EPA CAMPD facility attributes 1995–2025 | 128,525 unit-years | facility id (ORISPL) 1,959 | 1,587 / 1,959 match EIA plant codes (81%); EIA side: 1,587 of 16,132 plants are CAMPD-monitored (fossil units only — expected) |
| EPA CAMPD daily unit emissions 2015–2025 | 16,513,971 | facility id + unit id + date | joins EIA via facility id as above |

### H1. What this did and did not fix

- CAGE↔UEI crosswalk: DONE — 795K CAGE codes with their UEI on one row; 93% of contract CAGEs resolve.
- DUNS orphan problem (478K historic grant recipients): NOT fixed — the public SAM extract no longer carries DUNS.
  Paths that still exist: the USAspending assistance table's own UEI column for post-2022 rows; the FOUO SAM extract
  (needs a role); or the historical SAM monthly files from before April 2022 (Wayback may hold them).
- Ship axis: partially revived — one third of AIS vessels (by IMO and by call sign) now resolve to a documented US vessel
  with owner name/address. Sanctioned vessels stay dark (foreign flag).
- Trucking: new domain landed; connects by place/time and by name until a DUNS/UEI partner exists.
- Power plants: emissions now attach to 81% of CAMPD plants via EIA plant id.

## PARKED for a later pass — TIME and GEOGRAPHY links

Time: 1,275 verified date columns / 453 tables (reports/time_index/DATE_COLUMNS_ALL.md).
Place: 2,238 value-verified place columns / 386 marts (reports/location_index/LOCATION_VALUES.md, 2026-08-30 scan; supersedes the earlier 2,244 name-scan figure — the scan both dropped false hits, incl. 36 false "coordinates", and re-classified others, so the totals don't subtract cleanly).
Both are joins by Chris's 2026-08-29 decision; excluded here only because they apply to most tables.

## Pass 2 scope (not done)

- Bucket B rows 9–52 of the 08-29 inventory (name-scan only): NDC, FDA FEI/510k, CAS/UNII, HMDA respondent,
  OSHA establishment, TRI facility ID, RCRA handler, NTSB event, FEMA disaster #, ICIJ node IDs, etc.
- The 2026-08-05 web-research catalog (747 candidates; 73 free-bulk acquisitions; 40 "likely already
  have" of which 5 verified) — agent research, unverified.
- Parent / owner pointer columns (170 cols, 76 tables) beyond MSHA / RSSD.
