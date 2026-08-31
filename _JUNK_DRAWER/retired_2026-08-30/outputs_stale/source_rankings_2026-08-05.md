# Source Rankings — 2026-08-05

Every confirmed-buildable source from the recon, hand-ranked. The 145-row shortlist
dedupes to ~120 unique builds (AccessGUDID, ICIJ, UK PSC, UN sanctions, FATCA, VAERS,
TRI, MAUDE and a few others each appeared under 2–3 domains — counted once here).

**How to read the columns:**
- **Harm** — does a human get hurt somewhere in this data, visibly? The mission filter.
  High = injuries/deaths/discrimination/detention are literally rows. Med = harm is one
  join away. Low = reference/scaffolding data, no one bleeds in it.
- **Cost** — Trivial = one small file, an afternoon. Easy = a few files, one loader.
  Moderate = big multi-year files or annoying formats. Chunky = paginated API or
  streaming-scale, needs a real loader with checkpoints.
- **Joins** — what it connects to that Ripple already holds or is getting in this batch.

**Tiers:** S = build first. A = build soon. B = worth it, not first. C = scaffolding /
grab when a story needs it. D = skip for now.

---

## S-TIER — build these first (harm is in the rows, cost is low, joins are real)

| Dataset | What it is, in bar words | Harm | Cost | Why this rank |
|---|---|---|---|---|
| CFPB Consumer Complaint Database | Every consumer complaint filed against a financial company, with company name and narrative | High | Easy | Harm with names attached, one big CSV, joins straight to every bank/lender source below. Cheapest harm-per-row in the whole list. |
| ICE Detention Stints + Detainers (Deportation Data Project) | 1.3M individual detention book-ins + 147k detainer requests, FOIA'd out of ICE | High | Easy | People in cells, row by row. Bulk files, no login. Bundle the facility-code file (Vera) in the same build — it's the join key. |
| VAERS data files | Every vaccine adverse-event report, yearly CSV zips | High | Easy | Injuries as rows, trivially easy format, joins drug/manufacturer IDs from the FDA pile. |
| FDA FAERS (openFDA drug events) | Every reported drug side-effect case — the "this medication hurt me" database | High | Chunky | The single richest harm dataset in the sweep. API pagination is the only reason it's not the easiest build too. |
| FDA MAUDE (openFDA device events) | Every reported medical-device malfunction/injury/death | High | Chunky | Same story as FAERS but for devices. Pairs with GUDID so a broken device resolves to its maker. |
| EPA ICIS-Air + ICIS-NPDES (ECHO downloads) | Who's violating clean-air and clean-water permits, facility by facility | High | Moderate | Violations + enforcement, national, bulk. The backbone of any "polluter still operating" story. |
| EPA TRI Basic Data Files | What toxic chemicals every industrial facility released, by year, since 1987 | High | Easy | Simple CSVs, facility IDs join to ECHO/RCRA/GHGRP, harm is the entire point of the dataset. |
| openFDA Enforcement Reports (recalls) | Every FDA recall of food, drugs, devices — what was pulled and why | High | Moderate | The receipt when adverse events turn into action. Links FAERS/MAUDE patterns to outcomes. |
| NHTSA Recalls API | Every vehicle recall campaign | High | Moderate | Defects that injured people, clean API, joins to FMCSA world already in the warehouse. |
| SBA PPP loan-level data | Every PPP loan: borrower name, amount, lender, forgiveness | High | Moderate | The best fraud sandbox in public data. Names join to the corporate spine and to every enforcement list. |
| HMDA Historic LAR flat files | Every mortgage application ever reported — approved or denied, where, to whom | High | Moderate | Redlining and lending discrimination live here. Big files, but flat and documented. Joins FHA/Ginnie/CFPB. |

## A-TIER — build soon (spine or harm, modest cost)

| Dataset | What it is | Harm | Cost | Why |
|---|---|---|---|---|
| OpenSanctions default dataset | 4M+ sanctioned/PEP/criminal-context entities, consolidated worldwide, one download | Med | Easy | The single best entity-spine enrichment available. One file replaces a dozen separate sanctions loaders. |
| ICIJ Offshore Leaks | Panama/Paradise/Pandora Papers — 810k offshore shells and who's behind them | Med | Easy | Story-grade beneficial ownership, free CSV. Joins names to everything. |
| Consolidated Screening List (trade.gov) | US export ban lists (Entity List, Denied Persons) in one file | Med | Trivial | "Banned but still operating" needs exactly this. Tiny build. |
| UN Security Council Consolidated List | The UN's master sanctions list | Med | Trivial | XML, small, covered by OpenSanctions too — grab it as the authoritative original. |
| UK Sanctions List (FCDO) | The UK's sanctions list | Med | Trivial | Same logic as above. |
| USSC Individual Offender Datafiles | Every federal criminal sentence FY2002–2025, person-level | High | Moderate | Sentencing disparity is a mapped-harm story waiting to happen. Formats are statistical-package style — mildly annoying. |
| PBGC Trusteed Plans | Pension plans that failed and got taken over by the government | High | Easy | Joins directly to DOL Form 5500 already in the warehouse — failed-pension patterns become queryable almost immediately. |
| RCRAInfo Handlers (ECHO) | Every hazardous-waste handler in the country | Med | Moderate | Completes the EPA facility picture with TRI + ICIS. Same ID family. |
| Superfund SEMS | Every Superfund contamination site | High | Easy | Contaminated ground + responsible parties. Joins EPA facility IDs. |
| National Response Center incidents | Every reported chemical/oil spill call since the 90s | High | Moderate | Raw harm-event stream; joins facilities and vessels (NOAA AIS is already in the warehouse). |
| UK Companies House PSC | Who really controls every UK company — 10M records | Med | Moderate | The best free beneficial-ownership file on earth. UK-centric, but shells route through the UK constantly. |
| Federal Audit Clearinghouse | Single-audit results for every org spending $750k+ of federal money | Med | Moderate | Audit findings = pre-packaged fraud leads with EINs attached. |
| JPML Pending MDLs | Every mass-litigation cluster (multidistrict litigation) currently open | High | Trivial | A one-page index of "thousands of people say this product hurt them." Cheap harm-radar. |
| ATF Federal Firearms Licensees | Every licensed gun dealer | Med | Easy | License data that pairs with inspection/violation reporting for a classic oversight story. |

## B-TIER — worth building, not first (harm one join away, or great spine at real cost)

| Dataset | What it is | Harm | Cost | Why |
|---|---|---|---|---|
| NPDB Public Use File | De-identified malpractice payouts and doctor discipline | High | Easy | Harm-rich but anonymized — pattern analysis only, can't name anyone. Still maps *systems* that hide bad doctors. |
| NLRB Cases | Union-busting and labor-practice charges by employer | Med | Moderate | Employer names join the corporate spine; access mechanics need one verification pass. |
| College Scorecard | Outcomes and debt for every college, by OPEID | Med | Easy | Predatory-college patterns; OPEID is the join key for the education realm. |
| EIA-860 (plants/generators/utilities) | Who owns every power plant in America | Low | Easy | The ownership half of the pollution story — ORISPL joins to EPA emissions data. |
| FDA CAERS (food adverse events) | Reported harm from food and supplements | High | Moderate | Smaller sibling of FAERS. Same loader pattern, do it right after. |
| AccessGUDID | Registry of 5M+ medical devices and their makers | Low | Moderate | No harm in it, but MAUDE injuries resolve to manufacturers through it. Build alongside MAUDE. |
| FDA 510(k) + PMA clearances | How every device got approved (or grandfathered in) | Med | Moderate | The "cleared via loophole, later injured people" pipeline needs this half. |
| FDA Establishment Reg. & Listing (FEI) | Every registered drug/device factory | Low | Moderate | FEI is the establishment join key across FDA datasets. |
| HUD Multifamily Assistance & Section 8 | Subsidized-housing contracts and owners | Med | Easy | Landlords taking federal money — joins inspections/complaints later. |
| FHA Single Family Snapshot + lender IDs | FHA-insured loans by originating lender | Med | Easy | Lender ID links HUD world to HMDA world. |
| FHFA Suspended Counterparty List | Firms banned from doing business with Fannie/Freddie | Med | Trivial | Tiny "banned list" — another cheap radar. |
| ASC Appraiser + AMC registries | Every licensed appraiser and appraisal company | Med | Easy | Appraisal-bias stories key off this registry. |
| BJS PREA Audit Directory | Sexual-victimization audits of prisons and jails | High | Easy | 3,800 facility audit records. Small, dark, mission-true. |
| NIH RePORTER + NSF Awards | Every federal research grant, PI and institution | Low | Chunky | Funder-researcher graph; pairs with Retraction Watch for misconduct-vs-funding. |
| Retraction Watch | ~50k retracted papers and why | Med | Easy | Research misconduct receipts. Small CSV. |
| USAspending Assistance Awards (FAIN) | Every federal grant payment | Med | Chunky | **Check first** — warehouse may already hold USAspending. Don't double-load. |
| DOT National Address Database | Authoritative address points nationwide | Low | Moderate | Not a story — an entity-resolution weapon. Addresses are how shells get linked. |
| SBIR/STTR Awards | Small-business research grants | Med | Easy | Grant-fraud adjacent; joins corporate spine. |
| GLEIF Level 2 (LEI parents) | Corporate parent-child relationships worldwide | Low | Moderate | Ownership edges for the entity spine — valuable if LEI Level 1 is loaded, check that first. |
| State lobbyist registrations (CAL-ACCESS, TX) | Who's lobbying whom, state level | Med | Moderate | Money-in-politics joins; start with CA + TX bulk files only. |
| FCC Political File API | Broadcast political ad buys | Med | Chunky | Dark-money ad spending; real API work. |
| IRS 527 filings (8871/8872) | Political org registrations and donors | Med | Moderate | Pairs with lobbying and FEC data. |
| NTSB Aviation Accidents | Every aviation accident investigation | High | Easy | Harm events; joins carrier codes. Smallish. |
| National Inventory of Dams | Every dam, with condition and hazard ratings | High | Easy | "High-hazard, poor-condition, people downstream" is a ready-made map. |
| FracFocus | Chemicals injected at every fracking well | Med | Moderate | Joins API well numbers; chemical-exposure geography. |
| GHGRP | Big facilities' greenhouse-gas emissions | Low | Easy | Rounds out the EPA facility file. |
| HRSA UDS + HPSA | Community health centers + care-shortage areas | Med | Easy | The "who has no doctor" geography layer. |
| FEMA Individual Assistance (aggregated) | Disaster-aid grants by area | Med | Chunky | Disaster-recovery inequity patterns; de-identified. |
| PCAOB AuditorSearch | Which audit partner signed which public company's books | Low | Easy | Audit-failure stories key off this. |
| Sex offender registries (FL exemplar) | State registry bulk download | — | Easy | **Ranked B for buildability, but this is a RED-lane call before anything loads — publishing risk and ethics are Chris's decision, not a data question.** |

## C-TIER — scaffolding and reference (grab when something upstream needs them)

| Dataset | What it is | Cost | When you'd want it |
|---|---|---|---|
| DailyMed SPL | Every drug label | Moderate | Drug-name normalization for FAERS work |
| FDA UNII / GSRS | Ingredient identifiers | Moderate | Same — ingredient-level joins |
| FDA Device Classification | Device category codes | Easy | Classifying MAUDE/510k output |
| Health Canada DPD | Canadian drug registry | Easy | Cross-border drug checks only |
| OEHHA Prop 65 | California's harmful-chemicals list | Trivial | Chemical flagging enrichment |
| EPA AQS AirData | Air-quality monitor readings | Moderate | Exposure context around facilities |
| EPA CAMPD | Power-plant emissions detail | Easy | Deepens EIA-860 + ECHO joins |
| Water Quality Portal | Water monitoring samples | Chunky | Huge, low signal density — only for a specific water story |
| Watershed Boundaries (WBD) / GNIS / ITIS | Geo + taxonomy references | Easy | Mapping layers, name normalization |
| BOEM Offshore Leases | Offshore drilling leases | Easy | Offshore-spill story support |
| Pesticide Producing Establishments | EPA-registered pesticide makers | Trivial | Pesticide-story support |
| FEMA NFIP Community Status | Which towns are in flood insurance | Easy | Flood-exposure context |
| NCUA / OCC / FHLB institution lists | Bank + credit-union charters | Trivial–Easy | Financial entity spine filler |
| FATCA FFI List | Foreign banks registered with IRS | Easy | Offshore-banking spine filler |
| OSFI (Canada) institution list | Canadian regulated financials | Trivial | Cross-border only |
| SIREN/SIRET (France), Japan Corporate Number | Foreign company registries | Moderate | Only when a story crosses those borders — big files, low US relevance today |
| ISO MIC, FINRA MPID, OpenFIGI | Market/instrument identifiers | Trivial–Chunky | Securities plumbing, no current use case |
| Treasury TAS/CGAC codes | Federal account codes | Easy | USAspending decoding |
| Grants.gov XML Extract | Grant opportunities (not awards) | Easy | Low value — it's listings, not money |
| Crossref Funder Registry / DOI API | Publication + funder metadata | Chunky | Only with a research-integrity push |
| ORCID / OpenAlex / PubMed / PMC / arXiv / OSTI / OSF | The academic-paper universe | Chunky | Enormous, near-zero harm content — only if research integrity becomes a lane |
| FJC Federal Judges Directory | Every federal judge, biographical | Trivial | Judge-level joins for court stories |
| CIP Codes, OCD-IDs, ICAO types, BTS carrier codes | Classification code tables | Trivial | Pure lookup tables |
| IHS Facilities + Standard Code Book | Indian Health Service facilities | Trivial | Native-health story support |
| HUD CoC / PHA lists, USDA 515 housing, Ginnie Mae layouts | Housing program reference lists | Trivial–Easy | Housing-story support filler |
| Elections Canada, NYC CFB | Non-US / municipal campaign finance | Easy | Narrow-scope stories only |
| FAA Airports (ADIP), FMC OTI list, SATCAT | Airports, ocean freight brokers, satellites | Easy | No current mission hook |
| CelesTrak SATCAT | Satellite catalog | Easy | None yet — it's satellites |

## D-TIER — skip for now

Nothing lands here outright — everything above C-tier earned its confirmation. The
skips already happened upstream: the 83 critic-downgraded rows, the 247 unverified
"inferred" rows, and the 30 not-founds are excluded from this file entirely.

---

## The build order I'd actually run (YELLOW lane — my call, your veto)

1. **CFPB complaints + VAERS + ICE detention** — three loaders, one sitting each, immediate harm data.
2. **EPA block** (TRI → ECHO ICIS → RCRA → SEMS) — one facility-ID family, four sources, the whole polluter map.
3. **FDA block** (FAERS → MAUDE → GUDID → recalls → 510k) — one openFDA loader pattern reused five times.
4. **Money block** (PPP → HMDA → Federal Audit Clearinghouse → PBGC) — fraud + lending discrimination + pension failures.
5. **Spine block** (OpenSanctions → ICIJ → CSL → PSC) — entity enrichment that makes every earlier block smarter.

Two RED flags for Chris before any of this runs: the sex-offender-registry source
(ethics call), and whether ICE individual-level detention data crosses any line you
want to hold on person-level records. Everything else is YELLOW at most.
