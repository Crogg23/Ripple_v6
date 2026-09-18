# Idea Book extract — LB family (The Laboratory and the viz lane)

Extracted 2026-09-13. Family prefix LB. Six files read in full, no warehouse queries.

**Files read (line counts):**
- docs/The_Laboratory.md — 190
- docs/Laboratory_Warehouse_Map.md — 787
- reports/viz_ideas_inventory.md — 114
- reports/viz_join_catalog_2026-09-04.md — 126
- docs/DEEPFIELD_ATLAS_BLUEPRINT.md — 480
- docs/RIPPLE_DESIGN_BRIEF.md — 170

**Row counts:**
- IDEAS — 178
- METHODS — 88
- RULES — 52
- FINDINGS — 74
- DEAD ENDS — 17
- LOOSE — 22

Source shorthand in the last column: LAB = The_Laboratory.md · MAP = Laboratory_Warehouse_Map.md · INV = viz_ideas_inventory.md · CAT = viz_join_catalog_2026-09-04.md · BLU = DEEPFIELD_ATLAS_BLUEPRINT.md · BRF = RIPPLE_DESIGN_BRIEF.md

---

## IDEAS

| id | idea, one plain line | subject | tables or hubs named | join key | picture | status or result | source file § section |
|---|---|---|---|---|---|---|---|
| LB-001 | Every county coloured by morphine-equivalent dose per resident per year | opioids | HEALTH__FED_DEA_ARCOS, DIM_COUNTY | county name (ARCOS has no FIPS) | choropleth | BUILT — The Rate Map ✅ | INV § A.1; MAP § Aggregate first |
| LB-002 | ZIP-to-ZIP shipment routes over time, distributor to pharmacy | opioids | ARCOS | ZIP → XWALK_ZCTA_COUNTY → DIM_COUNTY centroid | flow arcs | BUILT — Pill Rivers ✅; county resolution only until DIM_ZIP_POINT | INV § A.2; MAP § Flow maps |
| LB-003 | Rank pharmacies by dose received vs county population; outliers are the story (the 9M-pill WV town) | opioids | ARCOS, DIM_COUNTY | county | scatter, pharmacy size vs town size | open ✅ | INV § A.3 |
| LB-004 | Stacked share of national dose by distributor per quarter — consolidation, who owned the peak | opioids | ARCOS | REPORTER_DEA_NO | share river | open ✅ | INV § A.4 |
| LB-005 | Oxycodone vs hydrocodone vs rest, share per year per state; spot states whose mix flips | opioids | ARCOS | state | small-multiple states | open ✅ | INV § A.5 |
| LB-006 | One pharmacy: drugs down the side, 84 months across, cell = dose | opioids | ARCOS (BUYER_DEA_NO × DRUG_NAME × TRANSACTION_DATE) | none | spectrogram heat grid | open ✅; substrate confirmed, no join, 2006-01-01 to 2012-12-31 | INV § A.6; MAP § Music/Audio; LAB § Other Domains |
| LB-007 | Drop weak shipment routes threshold by threshold; watch the national network shatter into islands; snap threshold is the finding | opioids | ARCOS (QUANTITY / TOTAL_MME FLOAT) | REPORTER_DEA_NO→BUYER_DEA_NO | percolation dial | open; valid today on ARCOS, invalid on CONNECT_EDGES | INV § A.7; MAP § Percolation theory |
| LB-008 | Which distributors bridge the most pharmacy communities — betweenness on the real shipment graph | opioids | ARCOS | DEA numbers | leaderboard | open ✅ | INV § A.8; MAP § Network centrality |
| LB-009 | % still detained at day 7/30/90/180/365 by year booked in | immigration | IMMIGRATION__FED_ICE_DETENTION_STINTS | none | survival curves | BUILT — The Waiting Room ✅ | INV § B.9 |
| LB-010 | Country → state → outcome: where from, who held them, how it ended | immigration | ICE_DETENTION_STINTS | none | Sankey | BUILT — Detention Rivers ✅ | INV § B.10 |
| LB-011 | Median stay per facility vs facility volume with uncertainty bands, so tiny facilities can't top on noise | immigration | ICE_DETENTION_STINTS (facility field) | none | funnel plot league table | open ✅ | INV § B.11 |
| LB-012 | Distribution of bond set vs posted; where the "can't afford $5,000" wall sits | immigration | ICE_DETENTION_STINTS bond columns | none | bond ladder histogram | open; fill rate unverified — check first | INV § B.12 |
| LB-013 | People with multiple stints: gap between release and re-booking | immigration | ICE_DETENTION_STINTS (PERSON_HASH repeats) | PERSON_HASH | histogram | open ✅ | INV § B.13 |
| LB-014 | Denial rate by race across income bands | mortgages | HOUSING__FED_CFPB_HMDA_HISTORIC | none | dot plot | BUILT — The Denial Gap ✅ | INV § C.14 |
| LB-015 | Tract denial rate for Black applicants vs 1930s redlining grades | mortgages | HMDA_HISTORIC, HOUSING__FED_MAPPING_INEQUALITY | tract / FIPS | map overlay | open ⚠️ redlining mart is a 1,155-row sample (10,154 raw) — city case study, not national | INV § C.15; MAP § Moran's I |
| LB-016 | Which lenders show the widest same-income racial gap; funnel guard for small lenders | mortgages | HMDA_HISTORIC (respondent) | respondent id | funnel plot | open ✅ | INV § C.16 |
| LB-017 | Denial reason mix by race per state; "collateral" vs "credit history" reads differently | mortgages | HMDA_HISTORIC | state | fingerprint bars | open ✅ | INV § C.17 |
| LB-018 | Application volume + denial rate 2007–2012 national — the market's heartbeat through the crash | mortgages | HMDA_HISTORIC | AS_OF_YEAR (TEXT, year grain only) | timeline | open ✅ | INV § C.18; MAP § Entropy |
| LB-019 | Bank branches: deposit glow, density, desert — three views | banking | FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS | none | map ×3 | BUILT — Bank Deserts ✅ | INV § D.19 |
| LB-020 | Assign every tract centroid to nearest branch; rank catchments by people per branch — Voronoi stats, no polygon | banking | FDIC_SOD_BRANCH_DEPOSITS, DIM_TRACT | nearest point | ranked catchments | open ✅; plain nearest-point join, drawn cells blocked by no outline | INV § D.20; MAP § Voronoi |
| LB-021 | Branches that vanish year over year, mapped as departures per county per year | banking | FDIC_SOD_BRANCH_DEPOSITS (SURVEY_YEAR) | BRANCH_COUNTY_FIPS | map by year | open ⚠️ verify all survey years loaded first | INV § D.21 |
| LB-022 | Deposits booked to HQ vs street branches — the accounting artifact is the story | banking | FDIC_SOD_BRANCH_DEPOSITS | none | log-scale strip plot | open ✅ | INV § D.22 |
| LB-023 | Ownership links switching on and off over time, growing web | corporate ownership | ECONOMICS__INTL_GLEIF_RELATIONSHIPS | LEI | clock + growing web | BUILT — The Ownership Clock ✅ | INV § E.23 |
| LB-024 | How deep do ownership chains go — parent-of-parent-of-parent; longest-chain gallery with names | corporate ownership | GLEIF_RELATIONSHIPS | LEI | histogram + gallery | open ✅ | INV § E.24 |
| LB-025 | Country-of-child × country-of-parent; offshore corridors light up | corporate ownership | GLEIF_RELATIONSHIPS + LEI entity table | LEI | heatmap matrix | open ✅ | INV § E.25 |
| LB-026 | Links switched OFF with no replacement parent — corporate abandonment timeline | corporate ownership | GLEIF_RELATIONSHIPS | LEI | timeline | open ✅ | INV § E.26 |
| LB-027 | Which states' complaint mix is unusual vs the national mix | consumer complaints | CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS | STATE | entropy map | open ✅ textbook entropy table | INV § F.27; MAP § Entropy |
| LB-028 | Response type mix per company, top 100 — who closes with relief vs without | consumer complaints | CFPB_COMPLAINTS (COMPANY_RESPONSE) | COMPANY | fingerprint | open ✅ | INV § F.28 |
| LB-029 | New issue categories appearing and exploding month over month | consumer complaints | CFPB_COMPLAINTS (ISSUE, RECEIVED_MONTH) | none | changepoint tracker | open ✅ | INV § F.29 |
| LB-030 | Do complaints with narratives get different responses — two-rate comparison, no NLP | consumer complaints | CFPB_COMPLAINTS (HAS_NARRATIVE) | none | two-rate bars | open ✅ | INV § F.30 |
| LB-031 | Every source's monthly pulse on one wall | warehouse clocks | TIMELINE__WAREHOUSE (403 sources) | RIPPLE_DAY | heartbeat wall | BUILT ✅ | INV § G.31 |
| LB-032 | Which sources beat together | warehouse clocks | TIMELINE__WAREHOUSE | RIPPLE_DAY | correlation grid | BUILT — The Pulse Grid ✅ | INV § G.32; MAP § Finance correlation |
| LB-033 | September fiscal-year-end spikes, election-cycle money wobble, weekend gaps, via the calendar dimension | warehouse clocks | calendar dimension (155,593 rows: fiscal year, election cycle, congress, weekend/month-end flags) + 403 clocked tables | date | calendar-effect scanner | open ⚠️ calendar table present, join untested | INV § G.33; MAP § Six shapes nobody claimed |
| LB-034 | For each source, the single month its line snapped hardest — wall of before/after breaks; collection-artifact x-ray | warehouse clocks | TIMELINE__WAREHOUSE (1.16M rows) | none | changepoint gallery | open ✅ | INV § G.34; MAP § Seven families |
| LB-035 | Benford digits, magnet amounts, threshold bunching, election river | political money | FINANCE__FED_FEC_INDIV_CONTRIBUTIONS | none | money shape panels | BUILT — The Shape of Money ✅ | INV § H.35 |
| LB-036 | Recurring-amount donor clusters; the July sweep found one making a fifth of rows at $23 each | political money | FEC_INDIV_CONTRIBUTIONS | none | treemap of exact-amount colonies | open ✅; found by hand, no technique behind it | INV § H.36; MAP § Six shapes (shape of money) |
| LB-037 | How the just-under-the-limit spike migrated as limits rose era over era | political money | FEC_INDIV_CONTRIBUTIONS | none | animated histogram | open ✅ | INV § H.37 |
| LB-038 | ZIP money vs ZIP denial — contributions joined to mortgage table by geography | political money × mortgages | FEC_INDIV_CONTRIBUTIONS, HMDA_HISTORIC | ZIP / geography | cross-table | PARKED 🅿️ design later | INV § H.38 |
| LB-039 | 1.3M providers × 49 measures projected to 2D; clusters = practice styles, outliers = billing anomalies | health providers | HEALTH__FED_CMS_MEDICARE_PROVIDER | none | PCA / t-SNE atlas | open ⚠️ exclude the identical twin table or every point doubles | INV § I.39; MAP § Dimension reduction |
| LB-040 | 6,103 hospitals × 107 cost-report measures with volume-based uncertainty bands; the honest "worst in America" guard | health providers | HEALTH__FED_CMS_HCRIS | none | funnel plots | open ✅ | INV § I.40; MAP § Seven families |
| LB-041 | ~35 chronic-condition percentages averaged by county — disease-burden maps with no new data | health providers | MEDICARE_PROVIDER (state / ZIP) | ZIP → county | maps | open ✅ | INV § I.41 |
| LB-042 | Politics money ↔ votes: member → committee linkage → contributions | politics | POLITICS__MEMBER_CROSSWALK (12,794), FEC_INDIV_CONTRIBUTIONS, roll-call votes (945k), cosponsorships (368k) | campaign-finance id array | money-to-votes graph | UNPARKED; 1,530 of 12,794 members carry ids, matches source (1,530 of 12,768); 16,451,066 contributions ($2.14B) reachable; caveat "modern members only" | INV § Parked; MAP § Opportunity 4 |
| LB-043 | Flatten the member crosswalk's campaign-finance id array; re-point the four starved money tables | politics | MEMBER_CROSSWALK; downstream tables hold 1,050–1,715 rows | member id | wiring unlock | open; effort hours; array fill not readable from metadata | MAP § Opportunity 4 |
| LB-044 | Opioid shipments ↔ county overdose deaths (NCHS 1999–2015) | opioids × mortality | ARCOS, NCHS county drug-poisoning mortality (53,387 rows, 3,141 counties) | FIPS to county spine; county name to ARCOS | map / scatter | UNPARKED; landed 2026-08-22, verified vs source; death rate is a BANDED estimate ("12.1–14 per 100k") | INV § Parked |
| LB-045 | Opioid Part D scripts vs county deaths | opioids × mortality | Part D, CDC county file | Part D →zip→ county ←FIPS CDC | cross-layer hunt | wired | LAB § Five cross-layer hunts |
| LB-046 | EPA facility ↔ corporate parent bridge — register the crosswalk as a spine edge source | environment × corporate | ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK (5,300,149 rows) | REGISTRY_ID → corporate id → LEI / SEC / UEI | fuses corporate island | MEASURED, decision pending: fill 1.4% — 73,948 of 5,300,149 matched; 22,736 companies; 10,297 with ultimate parent; 8,442 with SEC id; confidence avg 0.96; "fuses 5.3M island" oversold ~70×; spine rebuild ~4.5 h, $10–15 | INV § Parked; MAP § Opportunity 3; MAP § Connectome |
| LB-047 | Batch 2 candidates never compiled: EPA facility families, water violation spans (14.4M, survival), storm events, injuries with hours-worked, ER injury narratives (text), court case durations, AIS point cloud, FracFocus chemicals, GLEIF×SEC overlap | mixed | as named | mixed | mixed | not checked — "say next batch" | INV § Batch 2 candidates |
| LB-048 | A weirdness score per entity — "that is the whole thing" | method → product | every hub | any key | score | open; product idea | LAB § How to Find Things |
| LB-049 | The slot machine: random entity button → full dossier → weirdness score → next; one player, Chris | method → product | dossier over ~10 tables | any key | button + dossier | open | LAB § The slot machine |
| LB-050 | Contractors with high injury rates | labor × federal money | OSHA → FAC → USAspending | OSHA →EIN→ FAC →UEI→ USAspending | cross-layer hunt | wired; 441 employers match | LAB § Five cross-layer hunts |
| LB-051 | PAC money → committee seat → bills | politics | FEC → FEC_IDS → Congress → GovInfo | FEC_IDS | cross-layer hunt | column exists, no edge yet (see LB-042 for the array unlock) | LAB § Five cross-layer hunts |
| LB-052 | Water violators vs who drinks it | environment | SDWA → ECHO → county | SDWA →PWSID→ ECHO →FIPS→ county | cross-layer hunt | wired | LAB § Five cross-layer hunts |
| LB-053 | Polluter parents | environment × corporate | ECHO → crosswalk → GLEIF | ECHO →FRS→ crosswalk →LEI→ GLEIF | cross-layer hunt | wired; 22,743 LEIs | LAB § Five cross-layer hunts |
| LB-054 | Open Payments × Part D on NPI: do paid prescribers cost more per claim | health | Open Payments, Part D | NPI | scatter within specialty | probed: $10k+ prescribers cost 1.6x–7x more per claim within specialty; skeptic: drug mix not behaviour, ProPublica did it years ago | LAB § Tried 2026-09-04 |
| LB-055 | SAM exclusions × USAspending on UEI: paid while debarred | federal money | SAM, USAspending | UEI | list | probed: 22 firms, $1.86M while debarred; skeptic: UEI predates 2022 only via unvalidated backfill; mods on old awards are lawful | LAB § Tried 2026-09-04 |
| LB-056 | SAM NPI × Part D: excluded prescribers still prescribing | health | SAM, Part D 2024 | NPI | count | probed: zero hits; either CMS works or the NPI column is empty-shaped; unchecked | LAB § Tried 2026-09-04 |
| LB-057 | Does the ripple animation live in the Catalog (for Chris) or Publishing (for readers) | design | — | — | — | open question | LAB § Open / Tabled |
| LB-058 | Which 2–3 techniques across all categories to prototype first | design | — | — | — | open question | LAB § Open / Tabled |
| LB-059 | ARCOS pills per day 2006–2019; CFPB complaints per week | time series | ARCOS, CFPB_COMPLAINTS | none | one line over time | shape named, not built | LAB § Time series shapes |
| LB-060 | Pharma payments per month vs Part D scripts | time series | Open Payments, Part D | NPI | two lines one axis | shape named | LAB § Time series shapes |
| LB-061 | MSHA violations 12 months either side of an accident | time series | MSHA_VIOLATIONS, MSHA_ACCIDENTS | mine / controller | before-and-after | shape named; "build it first" | LAB § Time series shapes |
| LB-062 | One water system, 20 years, one sparkline | time series | SDWA violations | PWSID | sparkline | shape named | LAB § Time series shapes |
| LB-063 | FAERS reported vs happened — the lag is the chart | time series | FAERS (both clocks) | none | two-clock lag | shape named; FAERS is on the excluded list for column-shift | LAB § Time series shapes; INV § Trust legend |
| LB-064 | Open Payments dollars per prescriber relative to Part D claim volume | health | Open Payments, Part D | NPI | X per Y rel. Z | catalog shape 1 | CAT § Health providers |
| LB-065 | Opioid Part D claims per NPI relative to opioid-maker payments | health | Part D, Open Payments | NPI | ratio | catalog shape 2 | CAT § Health providers |
| LB-066 | Medicare Part B payments per provider relative to specialty peers by state | health | Part B | NPI | peer comparison | catalog shape 3 | CAT § Health providers |
| LB-067 | Order-and-referring volume per NPI relative to enrollment status | health | order/referring, PECOS | NPI | ratio | catalog shape 4 | CAT § Health providers |
| LB-068 | Home health NPIs per agency CCN relative to county population | health | home health, DIM_COUNTY | CCN, FIPS | rate | catalog shape 5 | CAT § Health providers |
| LB-069 | Nursing home deficiencies per CCN relative to ownership type | health | nursing home | CCN | grouped rate | catalog shape 6 | CAT § Health providers |
| LB-070 | Deficiencies per nursing home relative to MDS resident-days | health | nursing home, MDS | CCN | rate | catalog shape 7 | CAT § Health providers |
| LB-071 | SNF enrollments per PECOS PAC relative to facility affiliations count | health | PECOS, FACILITY_AFFILIATION | PECOS_PAC_ID | ratio | catalog shape 8; PECOS in keyset, no edges yet | CAT § Health providers |
| LB-072 | Hospitals per physician affiliation relative to hospital enrollment size | health | FACILITY_AFFILIATION | NPI, CCN | ratio | catalog shape 9 | CAT § Health providers |
| LB-073 | Providers per zip relative to HPSA shortage designation | health | NPPES, HRSA_SHORTAGE_AREAS | ZIP | rate | catalog shape 10 | CAT § Health providers |
| LB-074 | 990 e-filings per EIN relative to BMF asset class | nonprofits | IRS 990, BMF | EIN | grouped | catalog shape 11 | CAT § Nonprofits |
| LB-075 | Revocations per state relative to active nonprofits | nonprofits | IRS revocations, BMF | state | rate | catalog shape 12 (see LB-166 trap) | CAT § Nonprofits |
| LB-076 | Pub78 eligibility per subsection code relative to BMF total | nonprofits | Pub78, BMF | EIN | share | catalog shape 13 | CAT § Nonprofits |
| LB-077 | OSHA injuries per employer EIN relative to NAICS peer rate, 3 years | labor | OSHA ITA | EIN, NAICS | peer rate | catalog shape 14 | CAT § Nonprofits and employers |
| LB-078 | Federal assistance dollars per nonprofit relative to reported revenue | nonprofits | USAspending assistance, 990 | EIN | ratio | catalog shape 15 | CAT § Nonprofits |
| LB-079 | Single audits per auditee relative to award dollars received | nonprofits | FAC, USAspending | EIN / UEI | ratio | catalog shape 16 | CAT § Nonprofits |
| LB-080 | Contract dollars per vendor relative to assistance dollars | federal money | USAspending contracts, assistance | UEI | ratio | catalog shape 17 | CAT § Federal money |
| LB-081 | Subawards per prime relative to prime contract value | federal money | subawards, contracts | AWARD_KEY | ratio | catalog shape 18; subawards stub is 5,000 rows | CAT § Federal money; MAP § Ecology |
| LB-082 | NIH grants per org relative to SBIR awards | federal money | NIH, SBIR | UEI / DUNS | ratio | catalog shape 19 | CAT § Federal money |
| LB-083 | Exclusions per vendor relative to active contract dollars | federal money | SAM, USAspending | UEI | ratio | catalog shape 20 (see LB-055) | CAT § Federal money |
| LB-084 | Awards per agency relative to recipients per state | federal money | USAspending | agency, state | grouped | catalog shape 21 | CAT § Federal money |
| LB-085 | Auditor engagements per PCAOB firm relative to filer size | public companies | PCAOB, SEC | CIK | ratio | catalog shape 22 | CAT § Public companies |
| LB-086 | Insider filings per company relative to market cap | public companies | SEC Form 4 | CIK | ratio | catalog shape 23 | CAT § Public companies |
| LB-087 | 13F holdings per manager relative to filer count | public companies | SEC 13F | CIK | ratio | catalog shape 24; 13F dollars excluded (scale split) | CAT § Public companies; INV § Trust legend |
| LB-088 | OSHA injury rate per public company relative to revenue | public companies × labor | OSHA, SEC | CIK~EIN | ratio | catalog shape 25, thin (2–16% match) | CAT § Public companies |
| LB-089 | Violations per NPDES permit relative to inspections | environment | NPDES / ICIS | NPDES_ID | ratio | catalog shape 26 | CAT § Environment |
| LB-090 | Enforcement actions per facility relative to NAICS sector | environment | ECHO, FRS NAICS table | FRS_ID, NAICS | peer rate | catalog shape 27 | CAT § Environment |
| LB-091 | Quarterly noncompliance per permit relative to SIC code | environment | NPDES | NPDES_ID, SIC | grouped | catalog shape 28 | CAT § Environment |
| LB-092 | SDWA violations per water system relative to population served | environment | SDWA violations, PUB_WATER_SYSTEMS (POPULATION_SERVED_COUNT) | PWSID | rate | catalog shape 29 | CAT § Environment; MAP § Six shapes |
| LB-093 | Site visits per water system relative to violations | environment | SDWA | PWSID | ratio | catalog shape 30 | CAT § Environment |
| LB-094 | Lead sample exceedances per PWSID relative to service area | environment | SDWA | PWSID | rate | catalog shape 31 | CAT § Environment |
| LB-095 | Air emissions per FRS facility relative to corporate parent | environment | AIR_EMISSIONS, XC_EPA_CORPORATE_CROSSWALK | FRS_ID | grouped | catalog shape 32 | CAT § Environment |
| LB-096 | TRI releases per facility relative to county | environment | TRI, DIM_COUNTY | FRS_ID, FIPS | rate | catalog shape 33 | CAT § Environment |
| LB-097 | Generators per plant relative to utility owner | energy | EIA | EIA_PLANT_ID / UTILITY_ID | grouped | catalog shape 34; in keyset, no edges yet | CAT § Environment |
| LB-098 | eGRID emissions per plant relative to owner share | energy | eGRID | EIA_PLANT_ID | ratio | catalog shape 35 | CAT § Environment |
| LB-099 | MSHA violations per mine relative to accidents | labor | MSHA_VIOLATIONS, MSHA_ACCIDENTS | mine id | ratio | catalog shape 36 | CAT § Environment |
| LB-100 | EPA facilities per county relative to QCEW employment | counties | FRS_FACILITIES, BLS_QCEW | FIPS | rate | catalog shape 37; QCEW holds only 2022 | CAT § Counties |
| LB-101 | Drug poisoning deaths per county relative to HPSA shortage | counties | NCHS/CDC, HRSA | FIPS | scatter | catalog shape 38 | CAT § Counties |
| LB-102 | Incarceration rate per county relative to injury deaths | counties | incarceration, CDC injury | FIPS | scatter | catalog shape 39 | CAT § Counties |
| LB-103 | FEMA housing registrations per county relative to population | counties | FEMA_IA_HOUSING_REGISTRATIONS, DIM_COUNTY | FIPS | rate | catalog shape 40 | CAT § Counties |
| LB-104 | Health shortage areas per county relative to provider count | counties | HRSA, NPPES | FIPS | ratio | catalog shape 41 | CAT § Counties |
| LB-105 | Individual contributions per committee relative to candidate | politics | FEC | FEC_CMTE_ID / CAND_ID | grouped | catalog shape 42 | CAT § Politics |
| LB-106 | PAC receipts per committee relative to individual contributions | politics | FEC | FEC_CMTE_ID | ratio | catalog shape 43 | CAT § Politics |
| LB-107 | Leadership PACs per candidate relative to committees linked | politics | FEC | CAND_ID | count | catalog shape 44 | CAT § Politics |
| LB-108 | Committee-to-candidate transfers per PAC relative to PAC summary | politics | FEC | FEC_CMTE_ID | ratio | catalog shape 45 | CAT § Politics |
| LB-109 | Bills cosponsored per legislator relative to Voteview ideology | politics | Congress, Voteview | BIOGUIDE / ICPSR | scatter | catalog shape 46 | CAT § Politics |
| LB-110 | Committee memberships per legislator relative to bills sponsored | politics | Congress | BIOGUIDE | scatter | catalog shape 47 | CAT § Politics |
| LB-111 | Positions per judge relative to political affiliation | courts | CourtListener | CL_PERSON_ID | grouped | catalog shape 48 | CAT § Courts |
| LB-112 | Financial disclosures per judge relative to positions held | courts | CourtListener | CL_PERSON_ID | ratio | catalog shape 49 | CAT § Courts |
| LB-113 | Judges per court relative to dockets filed | courts | CourtListener | CL_COURT_ID | ratio | catalog shape 50 | CAT § Courts |
| LB-114 | Opinions per docket relative to FJC case type | courts | CourtListener, FJC IDB | DOCKET | grouped | catalog shape 51; DOCKET mostly unproven | CAT § Courts |
| LB-115 | Oral arguments per case relative to opinion count | courts | CourtListener | DOCKET | ratio | catalog shape 52 | CAT § Courts |
| LB-116 | Subsidiaries per GLEIF parent relative to EPA facilities | corporate registries | GLEIF, FRS | LEI | ratio | catalog shape 53 | CAT § Corporate registries |
| LB-117 | PSC owners per UK company relative to SIC code | corporate registries | UK_COMPANIES_HOUSE_PSC | COMPANY_NO, SIC | grouped | catalog shape 54; PSC likely truncated at 7,000,000 | CAT § Corporate registries; MAP § Ripples |
| LB-118 | HMDA loans per lender LEI relative to GLEIF entity | housing × corporate | HMDA, GLEIF | LEI | ratio | catalog shape 55 | CAT § Corporate registries |
| LB-119 | 13F positions per manager relative to CUSIP issuer | public companies | FED_SEC_13F_HOLDINGS × FTD_CUSIP_BRIDGE | CUSIP | ratio | catalog shape 56; zero edges built | CAT § Added after code sweep |
| LB-120 | Branch deposits per bank relative to FHLB membership | banking | FDIC SOD, FHLB | FDIC_CERT / RSSD | ratio | catalog shape 57; zero edges | CAT § Added after code sweep |
| LB-121 | Mines per controller relative to violations per operator | labor | MSHA | MSHA_CONTROLLER_ID / OPERATOR_ID | ratio | catalog shape 58; zero edges | CAT § Added after code sweep |
| LB-122 | Contract dollars per CAGE code relative to SAM exclusions | federal money | USAspending, SAM | CAGE | ratio | catalog shape 59; zero edges | CAT § Added after code sweep |
| LB-123 | Vessels per owner relative to port calls | maritime | 2 tables | IMO / MMSI | ratio | catalog shape 60; zero edges | CAT § Added after code sweep |
| LB-124 | Any county metric relative to population | counties | DIM_COUNTY.POPULATION_2020 (3,222 rows) | FIPS | rate | catalog shape 61 | CAT § Added after code sweep |
| LB-125 | Any zip metric rolled to county | counties | XWALK_ZCTA_COUNTY (46,960 rows) | ZIP → FIPS | rollup | catalog shape 62 | CAT § Added after code sweep |
| LB-126 | Build DIM_ZIP_POINT: every ZIP joined to its dominant county centroid, tie-break for straddlers | geography | XWALK_ZCTA_COUNTY, DIM_COUNTY | ZCTA5 → COUNTY_FIPS | unlock: ZIP-grain arcs, rates, heat, hotspots | open; hours, one dbt model; lights ARCOS flows + 3.08M FEMA displacement; ~33,000 ZIPs vs 3,222 counties | MAP § Opportunity 1; MAP § Flow maps |
| LB-127 | Day-two ZIP centroids: average coords on ~12.9M geocoded ZIP-stamped facility and branch rows | geography | FRS, FDIC etc. | ZIP | finer centroids | open; ~a day; facility-weighted, holes where no regulated site | MAP § Opportunity 1 |
| LB-128 | Cast GLEIF's five TEXT period start/end pairs to dates, filter PERIODTYPE = 'RELATIONSHIP_PERIOD' first — the ripple animation goes live and crosses sources | corporate ownership | GLEIF_RELATIONSHIPS | LEI (appears in nine other mart tables) | dated ripple | open; hours, one cast in an existing model; span measured 1832–2035, filter junk | MAP § Opportunity 2; MAP § Ripples |
| LB-129 | Ingest Census cartographic boundary files for state, county, tract, ZIP (~89,000 polygon rows) | geography | DIM_STATE, DIM_COUNTY, DIM_TRACT, XWALK_ZCTA_COUNTY | FIPS codes | unlock: filled maps for zoom, Voronoi, choropleth, mass, KDE, hotspot, Moran | open; 1–2 days; the only item needing a file from outside; widest blast radius | MAP § Opportunity 5; MAP § Sample or tier by zoom |
| LB-130 | How long does a water system stay in violation before anyone acts | environment | SDWA violation spans (14.4M) | PWSID | survival curve | open; 56 span tables and 70 lag tables already scored | MAP § Seven families (survival) |
| LB-131 | Inspection-to-action lag survival (565k lags) | environment | ECHO / inspection tables | facility id | survival | open | MAP § Seven families (survival) |
| LB-132 | Rate ratios between demographic groups on mortgage denials with same-row tract denominators | mortgages | HMDA_HISTORIC (race, ethnicity, sex, income, denial reason, tract pop and minority pop); disparity mart 128,507 rows | tract | group-disparity rates | open; disparity mart already computes per-race rates, ratios, gaps | MAP § Seven families (group disparity) |
| LB-133 | Topic maps, phrase shift, near-duplicate detection over ~29M narratives, each with place and clock | text | CFPB narratives 17.2M, ER injury 9.79M, device adverse events 2.74M, rail casualties 1.15M, workplace incidents 1.58M, mine accidents 274k | none | text analytics | open; no technique touches text | MAP § Seven families (text) |
| LB-134 | Sankey of 6.3M criminal cases from origin district to transfer district — no geography needed | courts | JUSTICE__FED_FJC_IDB_CRIMINAL | district | Sankey | open; court districts have no geography, so Sankey not map | MAP § Seven families (Sankey); MAP § Flow maps |
| LB-135 | Sankey of ARCOS shipments by business-activity tier on both ends | opioids | ARCOS (REPORTER/BUYER_BUSINESS_ACTIVITY) | DEA numbers | Sankey | open | MAP § Seven families (Sankey) |
| LB-136 | Sankey of 3.08M FEMA displacement moves with dollar amounts | housing | FEMA_IA_HOUSING_REGISTRATIONS (damaged ZIP → rental ZIP, RENTAL_ASSISTANCE_AMOUNT) | tract / ZIP | Sankey or flow | open; row count exactly 3,080,000 = load cap signature | MAP § Seven families; MAP § Flow maps |
| LB-137 | Which shares moved — mix-shift over 687 precomputed table-column mix rulings | warehouse | mix rulings (687, with snapshot-risk and survivorship-risk flags) | none | compositional chart | open | MAP § Seven families (mix-shift) |
| LB-138 | Workplace funnel plot: 398,620 workplaces with hours-worked as exposure denominator | labor | OSHA ITA | EIN | funnel | open | MAP § Seven families (funnel) |
| LB-139 | Facility funnel: 44,429 facilities × 204 measures | health | HEALTH__FED_CMS_POS_OTHER | CCN | funnel | open | MAP § Seven families (funnel) |
| LB-140 | Use better denominators: county-by-year population with age-adjusted death rate, hours worked, population served on 434,040 water systems, ECHO population density | denominators | county health table, OSHA, SDWA_PUB_WATER_SYSTEMS, EPA_ECHO.POPULATION_DENSITY | varies | any rate | open; every technique reached for 2020 county pop | MAP § Six shapes nobody claimed |
| LB-141 | Industry as an axis: "is this employer unusually bad vs others doing the same work" | peer groups | 916 tables carry an industry code | NAICS / SIC | peer comparison | open; no lookup table decodes or nests codes to sector | MAP § Six shapes nobody claimed |
| LB-142 | Look at the distribution of 656 numeric amount columns: digit tests, round-number bunching, under-threshold clustering, concentration curves | money | finished marts | none | money-shape panels | open (LB-035 built one instance) | MAP § Six shapes nobody claimed |
| LB-143 | Train a record-linkage model on the 6.5M-row labelled name-match set (pairs, verdict, score) — start dissolving islands | linkage | name-match pair table | none | supervised model | open; nothing in the catalog is supervised | MAP § Six shapes nobody claimed |
| LB-144 | Project ENTITY_MAP one way: honest map of which sources describe the same population | warehouse | ENTITY_MAP (33.3M, MEMBER_TABLES) | entity | bipartite projection | open; needs nothing built | MAP § Six shapes (bipartite) |
| LB-145 | Project ENTITY_MAP the other way: visibility-anomaly detector — things in an unusual combination of files | warehouse | ENTITY_MAP | entity | anomaly list | open; needs nothing built (cousin of LB-048) | MAP § Six shapes (bipartite); MAP § Entropy |
| LB-146 | Contact tracing on ICE stints: same facility, overlapping book-in/book-out | immigration | ICE_DETENTION_STINTS (PERSON_HASH, BOOK_IN_AT / BOOK_OUT_AT TIMESTAMP_NTZ) | PERSON_HASH | contact graph | ready; filter unrated clock, future-dated releases (max 2027-02-01), DUPLICATE_* flags first | MAP § Epidemiology |
| LB-147 | Doctor-shares-a-building graph, NPI↔CCN | health | HEALTH__FED_CMS_FACILITY_AFFILIATION (2,260,193) | NPI, CCN | bipartite graph | ready; zero date columns | MAP § Epidemiology; MAP § Network centrality |
| LB-148 | Run a connectome / centrality inside ARCOS: 178.6M edges, one DEA namespace | opioids | ARCOS | DEA numbers | centrality | ready inside; cannot cross warehouse | MAP § Connectome; MAP § Network centrality |
| LB-149 | Centrality over ICIJ Offshore Leaks: 3,339,267 typed edges over ~2.01M named nodes | offshore | ICIJ_OFFSHORELEAKS_RELATIONSHIPS + 5 node tables | NODE_ID | graph | ready; only 21% of edges dated | MAP § Network centrality |
| LB-150 | Cascade knock-out down GLEIF ownership tree using QUANTIFIERAMOUNT share | corporate ownership | GLEIF_RELATIONSHIPS (484,142) | LEI | trophic cascade | ready | MAP § Ecology |
| LB-151 | Shock a mine controller: same CONTROLLER_ID repeats on mines, violations, accidents | labor | LABOR__FED_MSHA_MINES (91,906), MSHA_VIOLATIONS, MSHA_ACCIDENTS | CURRENT_CONTROLLER_ID | cascade | ready | MAP § Ecology |
| LB-152 | Nursing home chain cascade | health | HEALTH__FED_CMS_NURSING_HOME (CHAIN_ID, NUMBER_OF_FACILITIES_IN_CHAIN) | CHAIN_ID | cascade | named, not built | MAP § Ecology |
| LB-153 | Contract action to parent award hop | federal money | USASPENDING_CONTRACTS_FULL (PARENT_AWARD_ID_PIID) | PIID | cascade | named; raw sits at exactly 20,000,000 rows (cap) | MAP § Ecology |
| LB-154 | Check subawards RECORD_JSON VARIANT for the prime-award key | federal money | PROCUREMENT__FED_USASPENDING_SUBAWARDS (5,000 rows) | AWARD_KEY | unlock | not checked | MAP § Ecology |
| LB-155 | Nursing home spectrogram: CCN by MDS quality measure by quarter, cell = percent | health | FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY (31,403,215) | CCN | heat grid, quarterly | ready; ~4 buckets a year not daily | MAP § Music/Audio |
| LB-156 | Pollution fingerprint per site: facility × pollutant × year 2008–2024 | environment | EPA_AIR_EMISSIONS_POLL_RPT_COMBINED_EMISSIONS (10,411,826) | REGISTRY_ID | heat grid, yearly | ready after casting TEXT year and TEXT emission | MAP § Music/Audio |
| LB-157 | Company × product × issue monthly series, ~175 buckets, clustered correlation | consumer complaints | CFPB_COMPLAINTS (RECEIVED_MONTH precomputed) | COMPANY | correlation heatmap | ready; replaces the dead QCEW panel | MAP § Finance correlation |
| LB-158 | Within-record correlation across 204 numeric columns | health | POS_OTHER (44,429 rows) | none | correlation matrix | ready | MAP § Finance correlation |
| LB-159 | Cluster sources on SOURCE_REGISTRY's own feature columns (five ARRAYs + GRAIN, SPINE_ENTITY, JOIN_KEY_TIER, HAS_EVENTS) and project to 2D | warehouse | LIBRARY_META.REGISTRY.SOURCE_REGISTRY (2,778) | none | cluster map | ready; not off CONNECT_EDGES | MAP § Distance |
| LB-160 | Map hexbin of 58.1M ship pings, binned server-side on the GEOGRAPHY column | maritime | MARITIME__FED_NOAA_AIS | none | hexbin | ready; one week of Jan 2024 only | MAP § Aggregate first; MAP § Astronomy |
| LB-161 | Heat surface plus people underneath from one table: ECHO lat/lon + POPULATION_DENSITY | environment | ENVIRONMENT__FED_EPA_ECHO (3,135,554) | none | KDE | ready; map counts, not dollars | MAP § KDE |
| LB-162 | Hotspot test on 5.3M EPA facilities per county with distance-band neighbours | environment | FRS_FACILITIES (FIPS_CODE unflagged), DIM_COUNTY | FIPS | Getis-Ord Gi* | ready | MAP § Hotspot |
| LB-163 | Hotspot / Moran on bank deposits per county per year | banking | FDIC_SOD_BRANCH_DEPOSITS (BRANCH_COUNTY_FIPS, SURVEY_YEAR) | FIPS | Gi* / Moran's I | ready; verdict OK in defect review | MAP § Hotspot |
| LB-164 | Moran's I on HPSA score as points, not on its broken FIPS | health | HRSA_SHORTAGE_AREAS (165,531; LAT/LON FLOAT, HPSA_SCORE) | coordinates | spatial autocorrelation | ready; reuse the 20-draw shuffle code from ripples_neighbor_rule_2026-08-21 | MAP § Moran's I |
| LB-165 | County-to-county federal assistance flow: recipient FIPS vs place-of-performance FIPS | federal money | USASPENDING_ASSISTANCE_FULL (19,902,879) | FIPS | flow map | drawable; all 112 columns TEXT, cast amounts and dates first | MAP § Flow maps |
| LB-166 | IRS auto-revocations × FAC × assistance: revoked nonprofits still funded | nonprofits | IRS revocations, FAC, USAspending | EIN | list | TRAP — tribes, transit agencies, housing authorities auto-revoke because they never file; $13.4B of nothing | LAB § Tried 2026-09-04 |
| LB-167 | Lead-detail dossier card: two source rows side by side, matched key, evidence, score, first/last seen, review state | design | LIBRARY_META.CONNECT.LEADS (~1,030) | bridge_key | card | NOT built | BRF § D3 NOT built |
| LB-168 | Entity corkboard: one person/org/vessel, every record across all sources on one card | design | ENTITY_MAP; `connect dossier --id ENT_… --html` bare v0 | hard IDs | card | bare v0 renders; designed version NOT built | BRF § D3 NOT built |
| LB-169 | The Plane CARD altitude + v1/v2: dataset profile cards, lifecycle+domain colours, search/filter/minimap | design | plane.html | — | zoomed ER | NOT built; CARD is the deliverable | BRF § D3, D5 |
| LB-170 | Lead-review UI: confirm/reject/retract — web, or Slack + Sheet | design | DECISIONS table | LEAD_ID | UI | CLI only today (`connect review --id LEAD_xxx --decision confirmed`); undecided | BRF § D3, D6 call 3 |
| LB-171 | Treatment for the 82 keyless/isolated nodes: hide, gray, or label with a reason ("NOAA AIS is IMO/MMSI only; IMO→OFAC bridge unbuilt"); "show only >0 join keys" filter | design | connect_graph.json | — | gutter treatment | default: show but gray, no filter | BRF § D3, D6 call 1 |
| LB-172 | Detector ideation: sketch what an EIN (revoked-org), NAICS (polluter), DOCKET (regulatory), ZIP (county-burden) detector looks like | detectors | backlog 37 STEEL / 39 CCN~NPI / 21 NPI edges with zero detectors | EIN, NAICS, DOCKET, ZIP | templates | out of scope unless wanted | BRF § D6 call 7 |
| LB-173 | Which single confirmed lead becomes the first public story, and what does that page look like | publishing | LEADS | — | scrollytelling page | open; Phase 2 question | BRF § D1 |
| LB-174 | Trace mode: pick two tables, pathfind over the verified mesh, rank routes by weakest-tier link ("FEC money to OSHA injuries, which hop is shakiest") | atlas | connect_graph.json | any | lit path | Phase II, not built | BLU § 4.3 |
| LB-175 | The absence queue: lensing layer's ranked hunt list, sorted by gap vs expectation; does it auto-rank? | atlas | hunch_absence_verdicts.json | — | ranked panel | Phase III; auto-rank is a taste call | BLU § 3.6, § 7 call 4 |
| LB-176 | Atlas over time: diff this month's atlas vs last month's, watch the unlit ring shrink; tables migrate in over a ~2s glide as edges are earned | atlas | atlas.json | — | animation / diff | Phase III | BLU § 3.5, § 5.1, § 6 |
| LB-177 | HYPOTHESIS_CATALOG surprise scores as a heat channel on atlas glyphs | atlas | HYPOTHESIS_CATALOG (pending infra/ddl/07) | — | heat overlay | Phase III, table not yet created | BLU § 6 Phase III |
| LB-178 | Is the atlas ever public? A Deepfield of the public record's shape, no findings, may be the best explanation of Ripple | publishing | deepfield.html | — | — | open call | BLU § 7 call 5 |

---

## METHODS

| id | name | what it is, plain | when to use it | source |
|---|---|---|---|---|
| LB-M01 | Aggregate first | Histograms, heatmaps, hexbins — plot group summaries, not every point | Any table too big to draw; 252 tables over 1M rows, 79 over 10M; ✅ Ready | LAB § Massive Scatter; MAP § Aggregate first |
| LB-M02 | Encode density, not position | Colour a spot by how many records landed there | Overplotted coordinate pairs; 122 tables have numeric lat; ✅ Ready | LAB § Massive Scatter; MAP § Encode density |
| LB-M03 | Dimension reduction (PCA / t-SNE) | Squash 20+ measures per row into 2D | One row = one thing with many real numbers; 10 tables qualify; ✅ Ready, watch the twin | LAB § Massive Scatter; MAP § Dimension reduction |
| LB-M04 | Sample or tier by zoom | Show a subset at first glance, more on zoom, like map tiles | Ladder exists (56 states, 3,222 counties, 85,391 tracts, 46,960 ZIP rows); 🟡 Partial — no polygons, so bigger dots not filled areas | LAB § Massive Scatter; MAP § Sample or tier by zoom |
| LB-M05 | Mass (organism) | Density, heatmaps, bubble size, contours — "where is there a lot?" | Coordinates or place code plus a population denominator; ✅ Ready at county and tract | LAB § Organism; MAP § Mass |
| LB-M06 | Distance (organism) | Clustering, dim reduction over join-key relatedness — "what's similar to what?" | Cluster the registry feature vector, not CONNECT_EDGES; ✅ Ready | LAB § Organism; MAP § Distance |
| LB-M07 | Circulation (organism) | Network / force-directed graphs — "what connects to what?" | Real edge lists: ARCOS, ICIJ, PSC, GLEIF, FACILITY_AFFILIATION, ENTITY_XREF; ✅ Ready, biggest two are sealed | LAB § Organism; MAP § Circulation |
| LB-M08 | Ripples (organism) | Diffusion / propagation animation — "what happens if this changes?"; reverse peel made visual | Needs dated edges; 🟡 Partial — only GLEIF can carry a ripple out of its source | LAB § Organism; MAP § Ripples |
| LB-M09 | Anatomy vs physiology | Mass and distance = anatomy; circulation and ripples = how it lives | Framing the four organism families | LAB § Organism core sentence |
| LB-M10 | Ripple animation style | Easing not snapping; muted palette + soft glow; only the ripple moves, map stays still | If the ripple animation is built | LAB § Organism style notes |
| LB-M11 | Topological Data Analysis | Finds loops, holes, clumps in a point cloud that averages miss | Dense numeric clouds: HCRIS 6,103×107, POS_OTHER 44,429×204, QPP 503,917×62; ✅ Ready | LAB § Physics; MAP § TDA |
| LB-M12 | Percolation theory | Turn a link-strength dial; find where islands snap into one blob | Only on a real physical network (ARCOS); 🟡 Partial — invalid on the 0.1%-sampled connection map | LAB § Physics; MAP § Percolation |
| LB-M13 | Network centrality | Which nodes are secretly important — a 2-link bridge can beat a 50-link hub | Thing-to-thing edge lists; SOURCE_COUNT on ENTITY_MAP is degree already; ✅ Ready | LAB § Physics; MAP § Network centrality |
| LB-M14 | Entropy / information density | How spread or piled a distribution is; entropy drops flag where pattern snapped into order | Counts across buckets; 403 tables share one clock; ✅ Ready | LAB § Physics; MAP § Entropy |
| LB-M15 | Hotspot analysis (Getis-Ord Gi*) | Confirms a cluster is significantly denser than chance | Value per place + distance-band neighbour rule from centroids; ✅ Ready | LAB § GIS; MAP § Hotspot |
| LB-M16 | Kernel Density Estimation | Scattered points to a smooth heat surface | Numeric lat/lon; ✅ Ready, needs nothing built — check row grain first | LAB § GIS; MAP § KDE |
| LB-M17 | Spatial autocorrelation (Moran's I) | Do nearby things behave alike (cluster) or opposite (disperse); works on similarity distance too | Value per place + shuffle test; shuffle code already exists; ✅ Ready | LAB § GIS; MAP § Moran's I |
| LB-M18 | Voronoi diagrams | Zones of influence around each point | Only where a point genuinely owns ground — bank branches, water systems; ✅ Ready on numbers, drawn cells blocked | LAB § GIS; MAP § Voronoi |
| LB-M19 | Flow maps | Movement between places, origin to destination | Same-row from/to with amount and date; 🟡 Partial — county resolution today, ZIP after DIM_ZIP_POINT | LAB § GIS; MAP § Flow maps |
| LB-M20 | Epidemiology → contact tracing graphs | Who touched whom, how far it spread | Two parties, same place, same time, stable ID, start/end; ✅ Ready via ICE stints | LAB § Other Domains; MAP § Epidemiology |
| LB-M21 | Astronomy → sky surveys / N-body | Gravity-like attraction clusters billions of points; force-directed's big sibling | Millions of points + a pull measure; ✅ Ready on AIS, but one week and no stored similarity | LAB § Other Domains; MAP § Astronomy |
| LB-M22 | Neuroscience → connectome mapping | Millions of connections, find the important circuits | Same shape as the Catalog; 🟡 Partial — runs inside ARCOS, islands don't touch across | LAB § Other Domains; MAP § Connectome |
| LB-M23 | Ecology → food web / trophic cascade | Remove one node, watch the cascade; built around removal not spread — maybe the best ripple template | Directed multi-hop chains in one namespace; ✅ Ready (ARCOS, GLEIF, MSHA controllers) | LAB § Other Domains; MAP § Ecology |
| LB-M24 | Music/Audio → spectrograms | Categories down the side, time across, intensity per cell; a static ripple image | One thing with many categories and many time buckets; ✅ Ready on ARCOS | LAB § Other Domains; MAP § Music/Audio |
| LB-M25 | Finance → correlation matrices / heatmap clustering | Score every pair of lines, reorder so co-movers clump; same math as distance | Many series on one clock; ✅ Ready via TIMELINE__WAREHOUSE | LAB § Other Domains; MAP § Finance correlation |
| LB-M26 | Look for weird, then read the weird | Don't look for things; questions are the wrong start — you need the answer to ask a good one | Every hunt | LAB § How to Find Things |
| LB-M27 | The atom is an entity, not a question | Pick a key → busiest value → pull every row (dossier ~10 tables) → read like a story → count who else does that | Starting any investigation; the joins already built the dossier | LAB § The atom is an entity |
| LB-M28 | Weirdness pass 1 — shape | What normal looks like per column; distribution per column | Run over every table | LAB § Five weirdness passes |
| LB-M29 | Weirdness pass 2 — outlier | Who sits far from normal within their group; ranked top 50 | Run over every entity | LAB § Five weirdness passes |
| LB-M30 | Weirdness pass 3 — coverage | Who is in way more tables than peers; ranked list | Run over every entity | LAB § Five weirdness passes |
| LB-M31 | Weirdness pass 4 — residual | Who should join but doesn't, or double-joins; orphans and collisions; the sneaky one (a nonprofit with 40 UEIs) | Run over every key | LAB § Five weirdness passes |
| LB-M32 | Weirdness pass 5 — change | Where a time series breaks; dates per entity | Run over every clocked entity | LAB § Five weirdness passes |
| LB-M33 | Breadth by machine, depth by human | Same SQL over 2,000 tables, no thinking per table; read only the top 50 of each list; five passes, one evening | Running the passes | LAB § Five weirdness passes |
| LB-M34 | Rank tables by leverage first | rows × keys × clock; top 30 tables carry most of the surprise | Before the passes | LAB § Five weirdness passes |
| LB-M35 | Time-series shape: one line over time | Single series | e.g. ARCOS pills per day | LAB § Time series shapes |
| LB-M36 | Time-series shape: two lines, one axis | Compare two series on one clock | e.g. payments vs scripts | LAB § Time series shapes |
| LB-M37 | Time-series shape: before and after a date | Window either side of an event; cleanest visual there is — build first | e.g. MSHA 12 months either side of an accident | LAB § Time series shapes |
| LB-M38 | Time-series shape: same entity, many years | One sparkline per entity | e.g. one water system, 20 years | LAB § Time series shapes |
| LB-M39 | Time-series shape: reported vs happened | Two clocks; the lag is the chart | Sources carrying both clocks | LAB § Time series shapes |
| LB-M40 | X per Y relative to Z | Shape of every cross-join item: Y is the join key, Z is the second table's attribute | Writing any join idea | CAT § header |
| LB-M41 | Trust legend | ✅ CLEAN = verified this month; ⚠️ CAVEAT = usable with a named limit that must appear on the visual; 🚫 excluded | Grading any viz substrate | INV § Trust legend |
| LB-M42 | BUILT flag | A working prototype page exists from the 2026-08-22 sprint | Reading the inventory | INV § header |
| LB-M43 | Readiness grades | ✅ Ready · 🟡 Partial · 🔴 Needs new data · 🛠️ Needs cleanup; plus Needs / What exists / Gap / Distance to ready / Candidate tables / one blockquote line | Scoring a technique against the warehouse | MAP § How to read a technique entry |
| LB-M44 | Score then refute | One pass scores; a second pass is told to refute — check every table, hunt tier inflation and deflation, catch name trusted as contents; two more passes sweep for contradictions and unclaimed shapes | Any metadata sweep; four tier calls changed this way | MAP § Method |
| LB-M45 | Completeness pass the other way | Which shapes exist at scale that no technique claims | After scoring a catalog | MAP § What the Laboratory doesn't have |
| LB-M46 | Rank opportunities by capability unlocked per unit of effort | Not by what should be built first — that call is Chris's | Listing next steps | MAP § Biggest Opportunities |
| LB-M47 | Survival / time-to-event | How long until something happens, and to whom; censoring, backwards dates, cohort comparability already scored | Spans and lags; 56 span + 70 lag tables scored | MAP § Seven families |
| LB-M48 | Group-disparity testing | Rate ratios between demographic groups with a denominator per group | "Who gets hurt, and does the data show it" | MAP § Seven families |
| LB-M49 | Text analytics | Topic maps, phrase shift over time, near-duplicate detection | ~29M narrative rows, the closest thing to a human voice | MAP § Seven families |
| LB-M50 | Changepoint detection | When did this line break | Any clocked series; TIMELINE__WAREHOUSE is the exact input | MAP § Seven families |
| LB-M51 | Funnel plots / uncertainty-aware benchmarking | Volume-based bands so a tiny facility isn't "worst in America" on two bad months | Any league table | MAP § Seven families |
| LB-M52 | Sankey / alluvial / chord | Flow without geography | Every from/to flow the map can't draw | MAP § Seven families |
| LB-M53 | Compositional / mix-shift | Which shares moved, not just how spread | 687 mix rulings already computed | MAP § Seven families |
| LB-M54 | Bipartite two-mode projection | Entities × source files; project either way | Source overlap map, or visibility-anomaly detector | MAP § Six shapes nobody claimed |
| LB-M55 | Fact vs lead | Fact = two records share a hard government ID; lead = share a name, no ID — a hunch | Governs everything; facts publishable, leads need a human | BRF § primer, D0 |
| LB-M56 | The six detectors | Rules that surface where two datasets contradict in a story-shaped way (banned doctors still paid, sanctioned ships still broadcasting); flag sources LEIE/OFAC/SAM vs active sources OpenPayments/AIS/USASpending; ~1,030 leads, 773 on one edge | Finding smells; the human decides | BRF § primer, D3 leads_overlay |
| LB-M57 | Confidence ladder | STEEL (hard ID) > STRONG (domain ID) > BRIDGE (via 3rd dataset key) > CORROBORATED (name + place) > GEO (location) > PROBABILISTIC (fuzzy name); meaning and ordering sacred, palette free | Every edge drawn; never draw weak like strong | BRF § D2; BLU § 3.3 |
| LB-M58 | Selective tier visibility | Let the 350-edge STEEL spine surface from 20,696 edges; default view overwhelming on purpose, signal pullable | The central UX challenge | BRF § D2 |
| LB-M59 | Node size = degree, not row count | Sizing by rows buried everything under a few giant tables | Any map of tables | BRF § D2 |
| LB-M60 | Edge width = match count | Records that actually intersect | Any map of tables | BRF § D2 |
| LB-M61 | Red-string board | Detector edges, width = lead count, colour = bridge key (NPI #f4a23a, IMO #3ab0c4, UEI #b07cf0) | Leads overview | BRF § D2, D3 |
| LB-M62 | Entity tiers and golden name | provider (NPI) / facility (CCN) / organization (EIN/CIK/UEI) / vessel (IMO/MMSI); golden name by authority rank, NPPES rank 1 beats LEIE rank 4 | Dossiers | BRF § D2, D4 |
| LB-M63 | Phase it: private workbench first, newsroom site second | Phase 1 dense Bloomberg-terminal for Chris; Phase 2 scrollytelling one investigation at a time, gated on safety layer | Who the viz is for | BRF § D1 |
| LB-M64 | The Plane — four altitudes | ORBIT (join-key bubbles, hubs >50 degree at zoom >8×) → REGION (638 datasets, STEEL/STRONG lit, ~0.55× extent) → STREET (viewport-culled edges, key on hover, ~0.12× extent) → CARD (one dataset + ranked neighbours); hysteresis stops flapping | Warehouse from altitude, offline | BRF § D5 |
| LB-M65 | The lensing method | We can't see the thing; we find it by what it bends — pairs that should overlap and measurably don't become the hunt list | The atlas's spine; "we think something is out there, and we're going to look based on what we see it affecting" | BLU § 1 |
| LB-M66 | Four states, not two | LIT (≥1 verified edge) / DARK (real key, matches nothing — the hunt list) / KEYLESS (no identity column — acquisition problem) / UNCHARTED (never entered discovery — a parked decision) | Any map of tables; three different jobs | BLU § 2.1 |
| LB-M67 | Absence as a first-class layer | Not a toggle or filter; its own ink, on by default, under the verified mesh like a gravity map under a star chart | Atlas rest state | BLU § 1, § 3.6 |
| LB-M68 | Identity gravity | 22 fixed anchor wells, one per key family; each table at the weighted barycenter of the families it carries (fill rate × distinct ratio); collision relaxation; deterministic seed | Layout that reads out of the data — monolingual tables orbit tight, polyglots sit in the straits | BLU § 3.1 |
| LB-M69 | Four honest node channels | Luminosity = log(rows) + degree; hue = dominant key family; form = state (LIT filled+glow, DARK hollow ring, KEYLESS bare tick, UNCHARTED faint outer dot); halo = best proof tier | Drawing a table | BLU § 3.2 |
| LB-M70 | The DARK ring | Hollow ring placed in lit territory beside its well, with no corridor reaching it — the most important mark; never banished to a margin | Drawing measured absence | BLU § 3.2 |
| LB-M71 | Edges as bundled corridors | Force-directed edge bundling per key family, computed at build; hover a well and its edges ignite as one river | Macro view instead of a hairball | BLU § 3.3 |
| LB-M72 | Tier line grammar | STEEL solid heaviest; CORROBORATED solid half; GEO dashed; BRIDGE dotted arcs routed visibly through the crosswalk node; STRONG thin solid | Drawing edges; never more certain than proven | BLU § 3.3 |
| LB-M73 | Spectral barcodes | One stripe per ID column: hue = key family, brightness = fill rate, solidity = distinct ratio; a 100%-populated sentinel column shows as bright with a hollow hatched core | A table's face; the trap that fooled a null-check twice can't fool an eyeball | BLU § 3.4 |
| LB-M74 | The unlit census HUD | Four state counts always on screen, "85.1% of the Library is unconnected"; each row is also a filter | Atlas chrome | BLU § 3.5 |
| LB-M75 | The Foundry projection | Same nodes reorganised left-to-right: LANDING → CONNECT → HUNCH lattice → HYPOTHESIS_CATALOG → Pattern Desk → Reading Room; ~900ms morph, identity persists | Where things live vs how things flow | BLU § 3.7 |
| LB-M76 | Semantic zoom Z0–Z3 | Z0 Field (all glyphs, wells, corridors) → Z1 Precinct (one well, 20–80 tables, all labelled) → Z2 Station (isometric slabs, height = rows, face = barcode) → Z3 Schema (columns with fill/distinct microbars, lifecycle, edge endpoints with counts and samples); zoom is disclosure, hard thresholds, crossfades | Atlas navigation | BLU § 4.1 |
| LB-M77 | The camera | 2.5D orthographic dolly, parallax, scroll = altitude, drag = pan, no roll no tumble — north stays north | Atlas | BLU § 4.2 |
| LB-M78 | Focus dive | Double-click: dolly in, rest dims and desaturates, band transitions fire mid-flight | Atlas | BLU § 4.2 |
| LB-M79 | The flight recorder | Every dive appends a breadcrumb; Esc flies back along it; always answers "where am I and how did I get here" | Atlas; the question that kills other large-graph tools | BLU § 4.2 |
| LB-M80 | The compass rose | Fixed radar of wells + viewport; hover a family and its corridors ignite everywhere ("show me everything money touches") | Atlas | BLU § 4.2 |
| LB-M81 | Search is teleport with a contrail | ~500ms arc, never a hard cut, fading contrail keeps the spatial model | Atlas | BLU § 4.2 |
| LB-M82 | The URL is the state | Camera, band, projection, pins, highlights serialize; a pasted link is a receipt | Atlas | BLU § 4.2 |
| LB-M83 | The receipt panel | Click an edge → key, tier, matched, match rate, distinct both sides, sample values | Every line produces its evidence on demand | BLU § 4.3 |
| LB-M84 | Pins | Right-click drops a survey pin; pinned glyphs stay lit through dimming, band change, morph | Keeping a working set | BLU § 4.3 |
| LB-M85 | The scope law, by camera | Every dive ends in receipts; every Esc ends at the whole field; UI resists collapsing into "one nice little story" | Atlas resting state | BLU § 4.4 |
| LB-M86 | Heavy thinking at build time, dumb speed at runtime | Compiler emits static atlas.json (layout, bundling, label lists); browser renders a file; Snowflake only for live receipts on registry tables | Any big viz | BLU § 5 |
| LB-M87 | Text is the performance boss | Labels, not lines, limit scale; per-band priority lists cap live labels at ~120 | Rendering thousands of nodes | BLU § 5.2 |
| LB-M88 | Lineage: organs not costumes | Octopus → bundled corridors; star map → deep field; isometric platforms → station interiors; manufacturing schematic → Foundry; fractal tree → zoom registers | Where prior concepts went | BLU § Lineage |

---

## RULES

| id | rule, plain | why | source |
|---|---|---|---|
| LB-R01 | AIS is one 24-hour snapshot — never draw a time series from it | Trap 1 of four | BRF § primer |
| LB-R02 | Same name ≠ same person — never merge in a viz | Trap 2 of four | BRF § primer |
| LB-R03 | Top-contractor rankings are floors, not truth | Trap 3 of four; USAspending FULL is zip-truncated | BRF § primer; CAT § Traps |
| LB-R04 | LEIE's all-zero NPI drawn as a confirmed fact is libel risk | Trap 4 of four | BRF § primer |
| LB-R05 | Honest encoding: trust = connection strength, never topic | Confidence ladder is load-bearing | BRF § D0 |
| LB-R06 | Never auto-publish a person's name; unconfirmed lead card must read INTERNAL/UNCONFIRMED — watermark, draft chrome, no shareable URL | `confirmed → publishable` is the most ethically load-bearing state change | BRF § D0, D4 |
| LB-R07 | Never let a viz blur fact and lead | Facts publishable, leads need a human | BRF § primer |
| LB-R08 | Keep three things sacred: ladder meaning + ordering, fact-vs-lead boundary, unconfirmed-name draft rule; everything else reinvent | Designer's latitude | BRF § closing |
| LB-R09 | No name matching in the identity layer — hard IDs only; NAME@ZIP / NAME@FIPS live only in the discover edge lane, tiered CORROBORATED, never merged into ENTITY_MAP | The safety guarantee made visible | BRF § D4 |
| LB-R10 | Excluded from viz entirely: contract trends (truncated sample), FAERS (column-shift), MSHA deaths, EPA penalty dollars (phantom-fines stamping), SEC 13F dollars (scale split), NHTSA (dup risk), UK ownership timelines (PSC edge dates unverified since 8/22 fix), debarment list | Substrate not trustworthy | INV § Trust legend |
| LB-R11 | A ⚠️ CAVEAT limit must appear on the visual | Honesty | INV § Trust legend |
| LB-R12 | GEO_IN edges to INTL_FR_DATA_GOUV_FULL match 100% on 22 tables — fake, skip | Trap | CAT § Traps; LAB § Traps met |
| LB-R13 | NAME@ZIP is fuzzy; multi-word names only; single-word 8% real | 2,512 edges, 38M rows, fuzzy | CAT § Key families, Traps |
| LB-R14 | CIK~EIN and EIN~UEI match 2–16%; show as a sample, never a rate | Thin crosswalks | CAT § Traps |
| LB-R15 | USAspending FULL tables are zip-truncated; counts are floors | Zip loads keep largest member | CAT § Traps |
| LB-R16 | Portal tables cap at 10,000 rows | Counts are floors | CAT § Traps |
| LB-R17 | Bridge rule: hard keys cross, code keys never do; NAICS/SIC/FIPS/ZIP/NCES/DOCKET/PATENT only group; only HARD×HARD crosswalks (NPI, EIN, CIK, DUNS, CCN, IMO, MMSI, UEI, LEI) are materialized | In code, connect/bridge.py | CAT § Bridge rule; LAB § What the joins allow |
| LB-R18 | Registry VOLUME is prose, not a count; quote `"CONNECT"` as a schema name | Trap | LAB § Traps met |
| LB-R19 | USAspending assistance columns are lowercase; quote them | Trap | LAB § Traps met |
| LB-R20 | Government units in IRS auto-revocation lists are noise, not findings | Tribes, transit, housing authorities never file | LAB § Traps met; LAB § Tried |
| LB-R21 | Most weirdness hits are data bugs; save them as traps | Expected outcome of the passes | LAB § Five weirdness passes |
| LB-R22 | Metadata cannot see contents: a numeric coordinate can be mostly null; a hard ID can be sentinel-masked (bitten twice); nothing in the map was value-checked | Hard limit of a metadata sweep | MAP § Method; MAP § Caveats |
| LB-R23 | Never trust a column name as proof of a column's contents | Refute-pass rule | MAP § Method |
| LB-R24 | Pick one of the Medicare provider twins or every point doubles — MEDICARE_PROVIDER and MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER are the same 1,296,739 rows, 81 columns, NPI vs RNDRNG_NPI | Exact duplicate load | MAP § Dimension reduction, TDA |
| LB-R25 | Check row grain before plotting: FracFocus's 7,200,550 rows are ingredient records, not wells | A talkative operator looks like a drilling hotspot | MAP § KDE |
| LB-R26 | Loaders wrote the text 'nan' into coordinate cells — the corruption lives in the 686 TEXT latitude columns, not the 122 numeric ones | Use numeric-typed coordinates only | MAP § Encode density, KDE |
| LB-R27 | Cluster off SOURCE_REGISTRY features, not CONNECT_EDGES; a missing pair means "never measured," not "no overlap" | 4,910 of ~4.6M possible pairs ≈ 0.1% | MAP § Distance, Percolation |
| LB-R28 | MATCH_PAIRS rows say a key value appeared in two TABLES, not that entity A links entity B — not an entity edge list | 181,002,484 rows, columns KEY_TYPE, KEY_VALUE, TABLE_A, TABLE_B | MAP § Connectome, Astronomy, Percolation |
| LB-R29 | Don't build on Companies House PSC without checking — exactly 7,000,000 rows in raw and mart, load-cap signature | Sibling UK table is unrounded 5,734,780 | MAP § Ripples |
| LB-R30 | Round row counts are load caps: 3,080,000 FEMA (vs 21,730,000 raw), 5,000 subawards, 20,000,000 contracts raw; 18 tables confirmed | Treat as truncated slices | MAP § Flow maps, Ecology, Caveats |
| LB-R31 | GLEIF period columns are TEXT and a flattened repeating group — filter RELATIONSHIP_PERIOD_1_PERIODTYPE = 'RELATIONSHIP_PERIOD' first; span 1832–2035 has junk and future dates | Slot 1 is not the same kind of period on every row | MAP § Ecology, Ripples, Opportunity 2 |
| LB-R32 | ICE stints: book-in/book-out clock never rated (index uses STAY_BOOK_OUT_DATE, MEDIUM); some book-outs are future-dated scheduled releases (max 2027-02-01); filter DUPLICATE_LIKELY / _SAMEDAY / _BOND / DUPLICATE_DROP_ROW before counting overlaps | Unfiltered rows double-count co-presence | MAP § Epidemiology |
| LB-R33 | HRSA_SHORTAGE_AREAS: use LAT/LON, never its county/FIPS columns — all seven are bad casts | Aug-10 defect review | MAP § Moran's I |
| LB-R34 | 88 of 610 mart models push county/FIPS through try_to_number (29 COUNTY, 16 COUNTY_NAME, 12 COUNTY_CODE, 6 COUNTY_FIPS) — leading zeros wiped; only 9 of 318 defect-clean models carry county FIPS | The join key is the thing most likely broken | MAP § Hotspot |
| LB-R35 | HMDA_HISTORIC has no DATE column — only AS_OF_YEAR as TEXT; no FIPS, compose STATE_CODE + COUNTY_CODE + CENSUS_TRACT_NUMBER | Year grain at best | MAP § Entropy |
| LB-R36 | Part D prescribers has no time axis — only _LOADED_AT, one value (2026-07-23 22:44:38) on all 25,869,521 rows | Load-stamp trap | MAP § Music/Audio |
| LB-R37 | BLS QCEW holds only YEAR = 2022; QUARTER is a bare 1–4 ordinal — at most four buckets | Dead as a time panel | MAP § Finance correlation |
| LB-R38 | Most movement in the warehouse is about how data was COLLECTED (crawl schedules, partial-year files, bulk backfills), not what happened; settle the denominator before building on a changing line | 2026-08-20 trend sweep headline | MAP § Finance correlation, Caveats |
| LB-R39 | Documented defects still stand: destroyed workplace-inspection table; three-quarters of a 62M-row drug-safety corpus column-shifted; EPA penalty column stamping one settlement on hundreds of facilities; debarment list under 9% loaded with fabricated status flags | Excluded substrates | MAP § Caveats |
| LB-R40 | Row counts are Snowflake metadata — exact for base tables, absent for views | Reading counts | MAP § Caveats |
| LB-R41 | ARCOS carries no FIPS in any of 33 columns — county joins are county-NAME matches | Rate map mechanics | MAP § Aggregate first |
| LB-R42 | ARCOS public window is 2006–2012, not 2006–2026 | Span limit | MAP § Flow maps; INV § A |
| LB-R43 | AIS clock is CLEAN but spans only 2024-01-01 to 2024-01-08; IMO_NUMBER sentinel-masked — use MMSI or IMO_NORMALIZED | A photograph, not a survey | MAP § Astronomy |
| LB-R44 | EPA ECHO money column is the phantom-fines defect — map counts, not dollars | Defect | MAP § Mass |
| LB-R45 | ICIJ has FIVE node tables, not four — leaving OTHERS (2,989) out orphans edges | ENTITIES 814,344, OFFICERS 771,315, ADDRESSES 402,246, INTERMEDIARIES 26,768, OTHERS 2,989 | MAP § Circulation |
| LB-R46 | Severity (312) and outcome (81) signal counts are column-name matches — upper bounds, like the 3,341 | Loose rules over-count | MAP § Entropy |
| LB-R47 | Copying RIPPLE_TS into ENTITY_XREF / MATCH_PAIRS does not work — one key value has many source rows with many dates | No single timestamp to copy | MAP § Ripples |
| LB-R48 | Never trust a number typed in prose; re-read outputs/connect_graph.json | House rule inherited from RIPPLE.md | BLU § header |
| LB-R49 | Never reorder the WELLS list in viz/compile_atlas.py — it rotates the map and burns spatial memory | Position is memory | BLU § 3.1 |
| LB-R50 | The chart never draws a connection as more certain than the engine proved | Confidence-ladder rule, non-negotiable | BLU § 3.3 |
| LB-R51 | "We never looked" and "we looked and found nothing" are different claims; the map must not blur them | Uncharted vs dark | BLU § 3.5 |
| LB-R52 | Publishing a Deepfield of the record's shape is not the same question as publishing a finding | Keep the two decisions apart | BLU § 7 call 5 |

---

## FINDINGS

| id | finding | number | tables | source |
|---|---|---|---|---|
| LB-F01 | Display keyset size | 96.4M keys DISPLAY_KEYSET_LIVE; 290M KEYSET_LIVE | keysets | LAB § Organism |
| LB-F02 | Proven table pairs in the edge table | 4,512 pairs, 30 key types; keyset 41 key types | CONNECT_EDGES, KEYSET_LIVE | LAB § What the joins allow; CAT § header |
| LB-F03 | NPI joins | 34 tables, 364 edges, 117M matched rows, steel ~100% | NPI family | LAB § joins; CAT § Key families |
| LB-F04 | EIN joins | 34 tables, 366 edges, 10.4M rows, steel 86–100% | EIN family | LAB; CAT |
| LB-F05 | FRS_ID / NPDES / PWSID joins | combined 37 tables, 226 edges, 67.8M; split: FRS_ID 17/136/54.6M, NPDES_ID 10/45/4.7M, PWSID 10/45/8.5M | environment keys | LAB; CAT |
| LB-F06 | CIK joins | 19 tables, 128 edges, 0.4M, 90–100% | CIK | LAB; CAT |
| LB-F07 | CCN joins | 25 tables, 78 edges, 0.5M, ~100% | CCN | CAT |
| LB-F08 | FIPS county joins | 15 tables, 78 edges, 0.2M, 73–100% | FIPS | LAB; CAT |
| LB-F09 | FEC committee / candidate joins | 19 tables (10 / 9), 81 edges, 0.5M, 72–100% | FEC_CMTE_ID, CAND_ID | LAB; CAT |
| LB-F10 | UEI / DUNS joins | 14 tables (9 / 5), 21 edges, 0.1M, 10–80%, sparse | UEI, DUNS | LAB; CAT |
| LB-F11 | LEI / COMPANY_NO joins | 9 tables, 22 edges, 8.8M; LEI alone 7/21/3.2M | LEI | LAB; CAT |
| LB-F12 | Courts and Congress joins | 13 tables, 47 edges, 0.2M; CL_PERSON_ID 8/28/0.1M; DOCKET 17 tables, 2 edges, 8K | courts | LAB; CAT |
| LB-F13 | NAME@ZIP joins | 122 tables, 2,512 edges, 38M, fuzzy | NAME@ZIP | LAB; CAT |
| LB-F14 | Cross-key crosswalks CIK~EIN, EIN~UEI, DUNS~UEI | 139 edges, 2–16% match | crosswalks | CAT |
| LB-F15 | In keyset, no edges yet | EIA_PLANT_ID 10 / UTILITY_ID 12 tables; PECOS_PAC_ID 9 / ENRLMT_ID 8; AWARD_KEY 4 tables, 94.7M rows; NAICS 16 / SIC 17; CUSIP, FDIC/RSSD, CAGE, IMO/MMSI | keyset | LAB; CAT |
| LB-F16 | Time registry classified | 643 sources; happened/day 123 sources 598M rows; happened/year 102 / 72M; reported/day 81 / 64M; reported/quarter 6 / 54M; decided/day 29 / 17M; none 241 / 83M | RIPPLE_TIME_REGISTRY | LAB § Time series shapes |
| LB-F17 | Heaviest day-grain streams | ARCOS 179M, FEC individual 84M, CourtListener dockets 72M, AIS 58M | as named | LAB § Time series shapes |
| LB-F18 | Contractors with high injury rates chain | 441 employers match | OSHA → FAC → USAspending | LAB § Five hunts |
| LB-F19 | Polluter parents chain | 22,743 LEIs | ECHO → crosswalk → GLEIF | LAB § Five hunts |
| LB-F20 | Paid prescribers cost more per claim | 1.6x to 7x within specialty for $10k+ recipients; skeptic says drug mix | Open Payments × Part D | LAB § Tried |
| LB-F21 | Paid while debarred | 22 firms, $1.86M; skeptic: backfill and lawful mods | SAM × USAspending | LAB § Tried |
| LB-F22 | Politics money ↔ votes chain verified | 1,530 of 12,794 members carry ids = source 1,530 of 12,768; 16,451,066 contributions, $2.14B reachable | MEMBER_CROSSWALK → FEC | INV § Parked |
| LB-F23 | NCHS county mortality landed | 53,387 rows, 3,141 counties, 1999–2015, verified vs source | NCHS drug poisoning | INV § Parked |
| LB-F24 | EPA corporate crosswalk fill | 73,948 of 5,300,149 (1.4%); 22,736 companies; 10,297 ultimate parent; 8,442 SEC id; confidence 0.96; zero review flags | XC_EPA_CORPORATE_CROSSWALK | INV § Parked |
| LB-F25 | Techniques scored | 23; 18 ready, 5 partial, 0 need new data, 0 need cleanup | — | MAP § One-screen picture |
| LB-F26 | Warehouse is text | 149,003 of 162,750 columns TEXT (91.6%); 7,558 NUMBER; 2,064 FLOAT | INFORMATION_SCHEMA | MAP § One-screen; TDA |
| LB-F27 | Coordinates typed as numbers | 122 tables numeric lat of 801 named (686 TEXT); 120 have both numeric; 54 in mart domain schemas, 21 with 100k+ rows | — | MAP § One-screen, Encode density, KDE |
| LB-F28 | Money and dates typed | 322 of 948 money tables numeric; 1,058 of 3,517 date-ish tables typed date; canonical clock cast 403 tables | — | MAP § One-screen |
| LB-F29 | Geospatial types | 2 of 162,750 columns, both the AIS POSITION_GEOGRAPHY point; zero polygons; 2,331 of 2,346 geometric-named columns are TEXT; all GEOMETRY/SHAPE_WKT/THE_GEOM are city ArcGIS pulls in LIBRARY_RAW.LANDING | — | MAP § One-screen, Sample or tier |
| LB-F30 | Official map links | 4,910 in CONNECT_EDGES (columns A, B, KEY, TIER, A_COL, B_COL, MATCHED, A_DISTINCT, B_DISTINCT, MATCH_RATE, CONFIDENCE, SAMPLE, RUN_ID, BUILT_AT); ~a quarter hard-ID; CONNECT_EDGES_INC 3,182 | LIBRARY_META.CONNECT | MAP § One-screen, Percolation |
| LB-F31 | Source tables carrying clean dated edge lists | ARCOS 178,598,026; ICIJ relationships 3,339,267; FACILITY_AFFILIATION 2,260,193; GLEIF 484,142 | as named | MAP § One-screen |
| LB-F32 | Entity table sizes (corrects "~12.88M across 31 spine tables") | ENTITY_GOLDEN and ENTITY_MAP 33,312,349; ENTITY_INDEX and CONNECT_NODES 84,382,504 | LIBRARY_META.CONNECT | MAP § Corrections |
| LB-F33 | FIPS bad-cast defect repaired 2026-08-10; columns TEXT with leading zeros today | — | marts | MAP § Corrections |
| LB-F34 | ARCOS bad-cast claim was read off the backup copy; live TRANSACTION_DATE is the cleanest big event clock (happened/day/HIGH, 2006-01-01 to 2012-12-31, 178,598,021 of 178,598,026 populated) | — | ARCOS | MAP § Corrections, Ecology |
| LB-F35 | Big tables | 252 objects 1M+; 79 10M+; ARCOS 33 columns with QUANTITY, DOSAGE_UNITS, BASE_WEIGHT_GRAMS, TOTAL_MME FLOAT; FEC indiv 84,172,112 rows | — | MAP § Aggregate first |
| LB-F36 | Hand-made rollups | exactly 14 in LIBRARY_MARTS.PUBLIC; none carries county, zip, tract, FIPS or lat/lon | LIBRARY_MARTS.PUBLIC | MAP § Aggregate first |
| LB-F37 | Biggest code-keyed county fact table | MDS frequency 31,403,215 rows with FIPS_COUNTY_CODE | FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY | MAP § Aggregate first |
| LB-F38 | Numeric-lat tables over 500k | AIS 58,104,610; FRACFOCUS 7,200,550; USGS_WATER 6,694,816; FRS_FACILITIES 5,300,149; FRS_FRS_FACILITIES 3,277,557; ECHO 3,135,554; FDIC_SOD 2,823,000; STORM_EVENTS 1,780,730; RCRA 1,613,224; NPDES_ICIS 1,213,737; FRA_CASUALTIES 1,150,788 | as named | MAP § Encode density |
| LB-F39 | Numeric width census | 4,847 objects; 3,076 zero numeric; 261 with 8+; 81 with 20+; 30 with 50+ (29 non-backup); of 252 1M+ tables zero have 50+, 110 have none; 34 real base tables 20+, 13 with 50+, 9 with 100k+ rows | — | MAP § Dimension reduction, TDA |
| LB-F40 | Wide measure tables | MEDICARE_PROVIDER 1,296,739 × 49 (48 real); QPP 503,917 × 62 (~30 usable); DME_BY_REFER 381,228 × 52 (51 real); OFLC 664,616 × 22; SCDB 83,644 × 47; POS_OTHER 44,429 × 204 of 473; HCRIS 6,103 × 107 of 125; NURSING_HOME 14,700 × 61 | as named | MAP § Dimension reduction, TDA |
| LB-F41 | FEMA IA housing | 3,080,000 rows with 31 real measures vs 21,730,000 raw (~14%) | FEMA_IA_HOUSING_REGISTRATIONS | MAP § Dimension reduction |
| LB-F42 | Zoom ladder rungs | DIM_STATE 56 (no pop, no centroid); DIM_COUNTY 3,222; DIM_TRACT 85,391; XWALK_ZCTA_COUNTY 46,960; TIMELINE 436 views; 136 objects with tract/GEOID/block-group | LIBRARY_MARTS.CORE | MAP § Sample or tier |
| LB-F43 | HMDA sizes | HMDA_LAR 17,474; HMDA and _DC_ONLY 28,301 each (stubs); HMDA_HISTORIC 19,136,434 with STATE_CODE, COUNTY_CODE, CENSUS_TRACT_NUMBER | HOUSING marts | MAP § Sample or tier |
| LB-F44 | Mart-layer geo dedup | 91 point-geo, 279 ZIP, 174 county, 80 place+clock, 27 place+harm; 683 of 805 lat tables TEXT | marts | MAP § Mass |
| LB-F45 | No population by ZIP anywhere; XWALK_ZCTA_COUNTY has no population column | — | CORE | MAP § Mass |
| LB-F46 | Registry feature matrix | SOURCE_REGISTRY 2,778 rows; ARRAYs DOMAIN_SECONDARY, ENTITY_TYPES, JOIN_KEYS_STD, THEMES, NATURAL_KEY; plus GRAIN, SPINE_ENTITY, JOIN_KEY_TIER, HAS_EVENTS, SOURCE_ROLE, DOMAIN_PRIMARY | LIBRARY_META.REGISTRY | MAP § Distance |
| LB-F47 | Pre-chewed answer tables | SOURCE_OVERLAP_MATRIX 36; DOMAIN_OVERLAP_MATRIX 7; CLUSTER_ASSIGNMENTS 23; BRIDGE_ENTITIES 0 | LIBRARY_META.CONNECT | MAP § Distance, Connectome |
| LB-F48 | Real-world graphs | ARCOS reporter→buyer; ICIJ 3,339,267 over 2,017,662 nodes; PSC 7,000,000 (COMPANY_NUMBER → person, NATURES_OF_CONTROL); GLEIF 484,142 vs 3,382,301 LEI entities; FACILITY_AFFILIATION 2,260,193; ENTITY_XREF 2,672,384 with RELATION, FANOUT; MATCH_PAIRS 181,002,484 | as named | MAP § Circulation |
| LB-F49 | Member crosswalk | 12,794 rows, fifteen parallel ids + campaign-finance id array; consumers hold 1,050–1,715 rows | POLITICS__MEMBER_CROSSWALK | MAP § Circulation, Opportunity 4 |
| LB-F50 | Sealed islands | REPORTER/BUYER_DEA_NO only in ARCOS; NODE_ID only in ICIJ; COMPANY_NUMBER only in two UK tables; LEI in nine other mart tables across four domains | — | MAP § Circulation, Ripples |
| LB-F51 | Spine edge tables carry only BUILT_AT and RUN_ID; ENTITY_LINKS only CREATED_AT; 66 of 436 TIMELINE views carry a hard entity id | LIBRARY_META.CONNECT, TIMELINE | MAP § Ripples |
| LB-F52 | ICIJ edge dating | 704,064 of 3,339,267 have start date (21%); 238,130 end date; range 1759 to 2029 | ICIJ relationships | MAP § Connectome |
| LB-F53 | Court citation edges | FED_COURTLISTENER_CITATION_MAP exists with 0 rows; citation table is ID/VOLUME/REPORTER/PAGE/CLUSTER_ID | CourtListener | MAP § Network centrality |
| LB-F54 | No precomputed graph metric anywhere (DEGREE/CENTRALITY/BETWEENNESS/PAGERANK/COMPONENT_ID); no VECTOR columns; no stored similarity | — | MAP § Network centrality, Astronomy, TDA |
| LB-F55 | Timeline layer | 436 views; 435 with RIPPLE_SOURCE/GRAIN/CLOCK; 403 with RIPPLE_TS; 32 without are index roll-ups; TIMELINE__WAREHOUSE 1,161,122 rows (RIPPLE_SOURCE, RIPPLE_CLOCK, RIPPLE_GRAIN, RIPPLE_DAY, N_ROWS); RIPPLE_TIME_REGISTRY 647; series 371 measured, 307 scored, 136 with 100k+ rows, 953 listed | LIBRARY_MARTS.TIMELINE | MAP § Entropy, Finance correlation |
| LB-F56 | Domain rollups nearly empty | CRIMINAL_JUSTICE 1, HISTORY 2, MONEY_FINANCE 7, MARITIME 8, INVESTIGATIONS 16, JUDICIARY 21; big ones ENVIRONMENT_INDEX 274,313, JUSTICE_INDEX 236,956, HEALTH_INDEX 131,105 | TIMELINE | MAP § Finance correlation |
| LB-F57 | CFPB complaints | 17,168,287 rows; PRODUCT, SUB_PRODUCT, ISSUE, SUB_ISSUE, COMPANY_RESPONSE, SUBMITTED_VIA, TAGS; DATE_RECEIVED 100% day-grain 2011-12-01 to 2026-07-23; IS_TIMELY, HAS_NARRATIVE, IS_CLOSED BOOLEAN | CFPB_COMPLAINTS | MAP § Entropy, Finance correlation |
| LB-F58 | SDWA violations | 15,432,737 rows, 13 real DATE columns (not four), VIOLATION_CODE, VIOLATION_CATEGORY_CODE, CONTAMINANT_CODE, IS_HEALTH_BASED_IND | SDWA_VIOLATIONS_ENFORCEMENT | MAP § Entropy |
| LB-F59 | FRS FACILITIES has no NAICS; NAICS lives in a separate 2,179,702-row table whose header says 500,000 | FRS | MAP § KDE |
| LB-F60 | Water system tables | PUB_WATER_SYSTEMS 434,040 with POPULATION_SERVED_COUNT, SERVICE_CONNECTIONS_COUNT, no coords; GEOGRAPHIC_AREAS 578,198 with COUNTY_SERVED bad-cast and header 500,000; SDWA_SERVICE_AREAS 422,464 (type code only, misfiled under IMMIGRATION) | SDWA | MAP § Voronoi |
| LB-F61 | Origin/destination shape index debunked | top "origin" names are SOURCE_RUN_ID 1,884, _SOURCE_URL 1,100, _SOURCE_RUN_ID 948; only 32 columns literally ORIGIN; ~six real flow families | — | MAP § Flow maps |
| LB-F62 | USAspending assistance FULL all 112 columns TEXT; contracts twin has money as FLOAT | 19,902,879 rows | USASPENDING_ASSISTANCE_FULL | MAP § Flow maps |
| LB-F63 | ICE stints clock | STAY_BOOK_OUT_DATE, MEDIUM, 2022-10-01 to 2026-03-11, 2,397,989 of 2,571,975 populated | ICE_DETENTION_STINTS | MAP § Epidemiology |
| LB-F64 | Person keys thin | 387 tables, dominated by LAST_NAME 80 / FIRST_NAME 68; PERSON_ID 14 tables; PERSON_HASH 2 marts (both ICE); 1,622 address-named tables (513 plain ADDRESS) | — | MAP § Epidemiology |
| LB-F65 | Air emissions | 10,411,826 rows, REGISTRY_ID × POLLUTANT_NAME × REPORTING_YEAR, 2008–2024, both TEXT | AIR_EMISSIONS_POLL_RPT_COMBINED | MAP § Music/Audio |
| LB-F66 | "Per person served" parked 1,426 times in the census grid | 1,426 | — | MAP § Opportunity 1 |
| LB-F67 | Industry codes | 916 tables carry one; no lookup decodes or nests them | — | MAP § Six shapes |
| LB-F68 | Numeric amount columns in marts | 656 | — | MAP § Six shapes |
| LB-F69 | Labelled name-match training set | 6.5M rows with verdict and score | — | MAP § Six shapes |
| LB-F70 | Atlas census 2026-08-02 | 1,043 tables; LIT 155 (14.9%); DARK 82 (7.9%); KEYLESS 131 (12.6%, 219M rows); UNCHARTED 675 (64.7%, 668 PORTAL_*, 672 carry a real key); 888 unconnected (85.1%, 429M rows); 2,694 edges from 2,664,155 pairs tested | connect_graph.json | BLU § 1, 2 |
| LB-F71 | Atlas edge families | NAME@ZIP 1,242; CCN~NPI 318; NPI 258; EIN 201; FIPS 190; CIK 94; FRS_ID 91; CCN 78; ZIP 50; PWSID 36; CIK~EIN 36; COUNTRY 16; EIN~UEI 16; FEC_CAND_ID 15; GEO_IN 15 | connect_graph.json | BLU § 2.2 |
| LB-F72 | Atlas tiers | CORROBORATED 1,246; STEEL 806; BRIDGE 370; GEO 271; STRONG 1; top hubs MEDICARE_PROVIDER 105, EPA_FRS_FULL 104, PHYSICIAN_OTHER_PRACTITIONERS 102, PART_D_PRESCRIBERS 89, OSHA_ITA_300A_SUMMARY_2025 89 | connect_graph.json | BLU § 2.3, 3.1 |
| LB-F73 | Design brief map state 2026-06-28 | 720 nodes (660 domain=other); 20,696 edges; STRONG 9,396 + GEO 5,633 = 73%; STEEL 350; 82 keyless; 638 connected datasets; bbox x [-6.74, 7.82], y [-7.43, 5.47], extent ≈ 14.5 | connection_explorer, connect_graph.json | BRF § D2, D3, D4, D5 |
| LB-F74 | Spine entities | 9,678,735 entities; ~953k multi-source; ~1,030 leads all pending/unpublished; 338/353 then 773 on one detector edge; 4 then 6 detectors | ENTITY_MAP, LEADS | BRF § D3, D4 |

---

## DEAD ENDS

| id | what was tried | why it died | source |
|---|---|---|---|
| LB-D01 | IRS auto-revocations × FAC × assistance | Tribes, transit agencies, housing authorities auto-revoke because they never file; $13.4B of nothing | LAB § Tried 2026-09-04 |
| LB-D02 | Open Payments × Part D per-claim cost | Survived the run; skeptic: drug mix not behaviour, and ProPublica did this join years ago | LAB § Tried 2026-09-04 |
| LB-D03 | SAM exclusions × USAspending paid-while-debarred | 22 firms found; UEI predates 2022 only via unvalidated backfill; mods on old awards are lawful | LAB § Tried 2026-09-04 |
| LB-D04 | SAM NPI × Part D 2024 | Zero hits; unclear if CMS works or NPI column is empty-shaped; unchecked | LAB § Tried 2026-09-04 |
| LB-D05 | Percolation on the connection map | Measures the sampler: 0.1% of ~4.6M pairs ever measured; snap threshold is an artifact | MAP § Percolation |
| LB-D06 | MATCH_PAIRS as an attraction / entity edge measure | Rows link TABLE_A to TABLE_B, not entity to entity | MAP § Astronomy, Connectome |
| LB-D07 | Court citation network | FED_COURTLISTENER_CITATION_MAP holds 0 rows | MAP § Network centrality |
| LB-D08 | BLS QCEW as the clean correlation panel | Only YEAR 2022; QUARTER is an ordinal; four buckets max | MAP § Finance correlation |
| LB-D09 | Copy RIPPLE_TS onto ENTITY_XREF / MATCH_PAIRS to clock the spine | One key value has many dated source rows; no single timestamp | MAP § Ripples |
| LB-D10 | HRSA county/FIPS columns for Moran's I | All seven bad casts; use lat/lon instead | MAP § Moran's I |
| LB-D11 | HMDA_LAR / HMDA / HMDA_DC_ONLY as tract sources | Stubs of 17,474 / 28,301 / 28,301 rows | MAP § Sample or tier |
| LB-D12 | Shape index's 558 origin-destination tables | Loader bookkeeping columns, not flows | MAP § Flow maps |
| LB-D13 | "Nothing can place a ZIP on a map" as a flow-map blocker | Wrong; ZIP → county → centroid is a two-hop join over existing tables | MAP § Corrections, Flow maps |
| LB-D14 | Part D prescribers as a spectrogram | Only _LOADED_AT, one value on all rows | MAP § Music/Audio |
| LB-D15 | Spectrogram for ripples, Voronoi | LAB flagged both as possible duds; MAP overturned Voronoi (bank branches own ground) and confirmed spectrogram on ARCOS | LAB § Other Domains, GIS; MAP § Voronoi, Music/Audio |
| LB-D16 | Original Laboratory figure "~12.88M entities across 31 spine tables" | Stale by ~4×; real 33,312,349 / 84,382,504 | MAP § Corrections |
| LB-D17 | leads_overlay.html as current | Built 6/27 with 4 detectors, 338/353 on one edge; live is 6 detectors, ~1,030 leads, 773 — re-render first | BRF § D3 |

---

## LOOSE

| id | item | source |
|---|---|---|
| LB-L01 | "Don't look for things. Look for weird, then read the weird." | LAB § How to Find Things |
| LB-L02 | "The computer does breadth, you do depth." | LAB § Five weirdness passes |
| LB-L03 | "Find the story by playing, not by planning." | LAB § The slot machine |
| LB-L04 | "Before-and-after is the cleanest visual there is. Build it first." | LAB § Time series shapes |
| LB-L05 | "The single widest constraint: value is present, type is wrong. The single widest unlock is one boundary-file ingest." | MAP § One-screen picture |
| LB-L06 | "This is a menu, not a plan." | MAP § header |
| LB-L07 | "The rollups already exist — 14 of them — and every single one is blind below the state line." | MAP § Aggregate first |
| LB-L08 | "The spine links things to files, not to each other." | MAP § Network centrality |
| LB-L09 | "Things moving together here usually means they were downloaded together." | MAP § Finance correlation |
| LB-L10 | Evidence folder for the map: reports/lab_map/ (metadata dump, shape index, per-signal candidates, verified-facts file) | MAP § footer |
| LB-L11 | Receipts for the 09-04 joins: reports/join_proof_2026-09-04.md; shuffle code: reports/ripples_neighbor_rule_2026-08-21.md | LAB § Tried; MAP § Moran's I |
| LB-L12 | "This is not a diagramming tool. It is an instrument for finding things that aren't there." | BLU § 1 |
| LB-L13 | Cosmology analogy: real universe ~5% ordinary, 27% dark matter, 68% dark energy; Library 14.9% lit, 20.5% dark-but-charted, 64.7% never looked at | BLU § 1 |
| LB-L14 | "The organizing force is already in the data — the job is to draw it, not invent one." | BLU § 2.2 |
| LB-L15 | "So the beauty and the truth are the same object." | BLU § Lineage |
| LB-L16 | Migration glide of a newly-connected table is "the single most motivating pixel in the design" | BLU § 3.5 |
| LB-L17 | Deepfield stack (for reference, not a spec here): WebGL2/Three.js orthographic, instanced SDF quads, prebaked ribbon VBO, troika SDF labels, GPU colour-pick, HTML chrome, zustand + URL, shader mix() morphs; ~4 draw calls, <200k triangles; holds past 10,000 tables | BLU § 5 |
| LB-L18 | Design brief palette reference: STEEL #f4a23a, BRIDGE #b07cf0, STRONG blue, CORROBORATED cyan, GEO green, PROBABILISTIC gray; bg #0d1117, text #e8eaed, danger #e5534b, accent #4c9aff | BRF § D2 |
| LB-L19 | LEAD shape: LEAD_ID, title, detector, score 0–1, bridge_key, evidence rows, first_seen, last_seen, review_state (pending/confirmed/rejected/retracted/stale), published bool. ENTITY_ID = 'ENT_' + LEFT(MD5(key_type + '|' + val), 16) | BRF § D4 |
| LB-L20 | Ethos: "we show our work"; credibility through honesty; the smells raise their own hand, the human decides; editorial desk / data terminal, monospace-adjacent, evidence-forward, not a rounded consumer app | BRF § D8 |
| LB-L21 | Existing surfaces: connection_explorer.html (~17MB, CDN Plotly), plane.html (offline, ~5.3MB with vendored mermaid, CARD unbuilt), leads_overlay.html (stale, CDN), connect_graph.json (~7.3MB, data behind every map), PLANE_handoff.md; vendored outputs/plotly.min.js 4.8MB not wired in | BRF § D3 |
| LB-L22 | Design-brief open defaults: domain colour deferred to v1 (660/720 are `other`); pre-render + vendor mermaid; lifecycle colours (9 trust-gated stubs) in v1; dossier timing undecided | BRF § D6 calls 2, 4, 5, 6 |
