# The wish list and the words

148 wishes and 159 words, merged from 334 extract loose rows across five families.

Part 1 lists every dataset the papers wanted and do not hold, one row each, with the warehouse table it would sit beside and any rescue score the hunch expansion gave it; rows marked held or landed were wishes when written and are on the shelf now.
Part 2 keeps the glossary, the ids, the framing lines, Chris's own words, and the pointers and receipts a later session will need to find things; sources are short-named as in the other chapters.

## Part 1: datasets not yet held

#### Ranked by the hunch expansion (score = hunches it rescues)

| id | dataset | who publishes it | what it would pair with | sources |
|---|---|---|---|---|
| W-001 | CMS Revalidation Reassignment List + Clinic Group Practice Reassignment | CMS | the org-to-person bridge; rescues hunches 7, 14, 16 to tier 1 and 4 to tier 2; ~1.2M rows/month, 81 vintages 2022-03 to 2026-05; score 8; NOT LANDED at column level; wanted by Hub B and Hub X | expansion |
| W-002 | HCRIS cost report series FY2011-FY2022 + SNF (13 files), HHA (4), hospice; forms 2552-10 FY2018-2024, SNF 2540-10, HHA 1728-94, hospice 1984-14 | CMS | promotes hunches 28, 11, 21, 29, 12, fat margins, hazardous-waste hospitals; score 7; PARTLY LANDED, docket says 13 years 2011-2023 now (80,077 rows) | expansion; docket combined |
| W-003 | BLS QCEW annual single files 2010-2024 (~3.6M rows/yr) | BLS | VERA jail rates, ICIS-AIR violators, hunches 21, 9; score 4; warehouse holds only YEAR 2022 with QUARTER as an ordinal; also frontier round 1 | expansion; lab map; frontier list |
| W-004 | Part D Prescribers longitudinal DY2013-DY2024 (~25M rows/yr drug file); by provider DY2022/DY2023; by provider and drug DY2023/DY2024 | CMS | Open Payments by year, pharma per head, hunch 19, 4 nearest-live wonders; score 3; wonder 44 cost growth dies without it | expansion; table map |
| W-005 | CMS PECOS All Owners (SNF 89 vintages, Hospital 85, HHA 27, Hospice 27, FQHC 23, RHC 23) + SNF/Hospital CHOW files | CMS | rescues HHA/hospice ownership change (hunch 74); score 2; HHA owners landed 2026-09-07; no dialysis or DME owners file exists | expansion; docket combined |
| W-006 | PBJ Daily Nurse Staffing (73 quarterly files, 1.3M rows each) | CMS | nursing-home deficiencies; Wonder Wall E8 staffing predicts the next deficiency | expansion |
| W-007 | Hospice PAC PUF by provider (21 vintages); Hospice Utilization and Payment PUF | CMS | the Frank file: no hospice utilization file landed today | expansion |
| W-008 | OpenFEMA Disaster Declarations Summaries v2 (~68k rows) | FEMA | the disaster clock for SDWA, overdose, provider-startup hunches | expansion |
| W-009 | HUD-USPS ZIP-County crosswalk, ratio-weighted; HUD ZIP-Tract-County-District crosswalk | HUD | replaces XWALK_ZCTA_COUNTY's one-county-per-ZIP guess (79.8% agree on DIM_ZIP_POINT) | expansion; frontier list |
| W-010 | CMS Medicare Monthly Enrollment by county | CMS | denominators for Part B, Part D, dialysis county rates | expansion |
| W-011 | CDC PLACES county 2020-2025 | CDC | health denominators for the county hub | expansion |
| W-012 | BJS Census of Jails 2019 + Annual Survey 2020-2024, or refreshed VERA; Vera 50-year incarceration; DOJ Deaths in Custody | BJS; Vera; DOJ | jail-rate hunches (52, 67) currently ride a stale VERA table with impossible rates | expansion; frontier list |
| W-013 | ECHO case-level enforcement history with dates | EPA | penalty deserts need dated enforcement, not facility snapshots | expansion |
| W-014 | ACS 5-year county tables + PEP annual population; county population by year pre-2020; Census/ACS tract-level demographics | Census | every per-head rate; "per person served" parked 1,426 times; no population by ZIP anywhere | expansion; docket v2 notes; tool box; frontier list |
| W-015 | SDWIS quarterly snapshots | EPA | violations jumped 18,287 in 2024 from 11,380; need the snapshot to tell load from world | expansion |
| W-016 | Part B DY2022/DY2023 | CMS | newborn-NPI and top-biller hunches want a second year | expansion |
| W-017 | Open Payments Ownership/Investment file OWNRSHP_PGYR2022-2024 | CMS | doctors who own the device company that pays them | expansion |
| W-018 | State medical board discipline with license numbers; Delaware licensing-board discipline | state boards | joins NPPES PROVIDER_LICENSE_NUMBER_1; NPDB is the only discipline signal today | expansion; frontier list |
| W-019 | DEA ARCOS retail summary by registrant | DEA | runner-up for Hub B; ARCOS_FULL ends 2014 | expansion |
| W-020 | Full POS file (02 SNF, 05 HHA, 08 hospice, 09 ESRD with CHOW_DT, PGM_TRMNTN_CD) | CMS | sale-then-close (hunch 48) sits at a 3.4-15.0% floor for want of dated CHOWs; POS_OTHER has 0 HHA/hospice CCNs | expansion |
| W-021 | Care Compare archived releases 2019-2026 | CMS | last star before termination (0 of 762 remain today); Kirkland 2020 miss | expansion; tool box |
| W-022 | HRSA PRF recipient-level payments | HRSA | nursing-home chains; PRF name match sits at 14% | expansion |
| W-023 | IRS 990 Schedule H e-file extract | IRS | hospital charity care vs HCRIS margins | expansion |
| W-024 | CDC WONDER county overdose 2016-2024 or SUDORS | CDC | closes the gap between DRUG_POISONING 1999-2015 and CDC injury 2019-2024 | expansion |
| W-025 | FAC federal_awards and findings tables | FAC | material-weakness grantees by award, not by grantee | expansion |

#### Wanted by the docket and the matrix

| id | dataset | who publishes it | what it would pair with | sources |
|---|---|---|---|---|
| W-026 | Ticker-to-industry lookup | SEC / exchanges | EDGAR_COMPANY_TICKERS_EXCHANGE has no industry | docket v2 notes; tool box |
| W-027 | FTD_CUSIP_BRIDGE | — | named in the catalog, not in the inventory; CUSIP is in keyset with zero edges | docket v2 notes; tool box |
| W-028 | FAERS report-ID key; FDA FAERS adverse events, current | FDA | today's FAERS ends 2014q2 with a column shift; any post-2014 drug has no trail | docket v2 notes; tool box; frontier list |
| W-029 | EIA plant and utility edges; EIA-861 utility territories | EIA | EIA_PLANT_ID 10 tables, UTILITY_ID 12 tables in keyset, zero edges | docket v2 notes; tool box; frontier list |
| W-030 | Full HMDA post-2018; HMDA mortgage records | CFPB | HMDA_HISTORIC is 2015-2017 only | docket v2 notes; tool box; frontier list |
| W-031 | Full FEMA IA | FEMA | table map says the mart is now full (26,250,920); docket still lists it | docket v2 notes; tool box |
| W-032 | Judge code to FJC crosswalk; FJC IDB codebooks (hunches 133, 134, 94) | FJC | 50 years of IDB with no judge name; DOCKET key has 2 edges | docket v2 notes; tool box; matrix |
| W-033 | Tract-level HMDA geocode | CFPB | HOLC, TRI and tract shapes | docket v2 notes; tool box |
| W-034 | HHCAHPS stars | CMS | home-health patient experience beside HOME_HEALTH | tool box |
| W-035 | House disbursement and PTR detail lines (hunches 91, 92); congressional stock trades (STOCK Act) | House Clerk | FED_HOUSE_FD_PTR_INDEX counts filings, not trades; HOUSE_DISBURSEMENTS has no mart | matrix; frontier list |
| W-036 | EAVS codebook (hunch 93) | EAC | EAVS table needs a YEAR column (table map fix 15) | matrix |
| W-037 | FRA crossing inventory (hunch 105); FRA grade-crossing incidents | FRA | FRA_CASUALTIES, FRA_EQUIPMENT_ACCIDENTS | matrix; frontier list |
| W-038 | IRS 527 Schedule A/B 17.9M (hunches 88, 125) | IRS | since landed; IRS527_SCHED_A 9,701,952, _B 8,191,177 | matrix; frontier list |
| W-039 | EOIR column split (hunches 144, 119); EOIR cases + ICE detention stays, parsed | DOJ EOIR | now 39 typed columns, still no judge or outcome; needs B_TblProceeding | matrix; docket combined; frontier list |
| W-040 | AACT clinical trials (hunches 143, 113); ClinicalTrials.gov + FDAAA TrialsTracker | CT.gov | full CT.gov landed 2026-09-07 with NPI blank; needs a PI name bridge | matrix; frontier list |

#### Frontier list, round 1 (2026-06-30)

| id | dataset | who publishes it | what it would pair with | sources |
|---|---|---|---|---|
| W-041 | Census TIGER/Line boundary shapes | Census | "the single widest unlock is one boundary-file ingest"; zero polygons in the warehouse today | frontier list; lab map |
| W-042 | OSHA enforcement (inspections, violations) | OSHA | wonder #28 died for want of it; OSHA 300A is the injury side only | frontier list |
| W-043 | EPA EJScreen (Harvard mirror); EDGI rescued EJScreen/CEJST | EPA / Harvard / EDGI | EPA_PENALTY_GAP PCT_MINORITY is null on 32% | frontier list |
| W-044 | NIH RePORTER + Drugs@FDA approvals | NIH; FDA | NIH_REPORTER is held (Lieber row); Drugs@FDA is not | frontier list |
| W-045 | CMS Hospital Price Transparency files | CMS | HCRIS margins, INPATIENT_BY_PROVIDER | frontier list |
| W-046 | SBA PPP loan-level, all sizes | SBA | Kabbage fake farms are under the 150K+ floor | frontier list |
| W-047 | SEC Form ADV private-fund filings | SEC | 13F, EDGAR CIK | frontier list |
| W-048 | County parcel + assessor records | counties | HOLC, nursing-home owners, address stacking | frontier list |
| W-049 | Federal lobbying disclosures (LDA) | Senate / House | held as SENATE_LDA_FILINGS (misfiled under EDUCATION); no years shared with Federal Register | frontier list |
| W-050 | State campaign finance + Open States | states | FEC is federal only; TX and CA lobbying already mini-warehouses | frontier list |
| W-051 | IRS 990 dark-money grant schedules | IRS | IRS_990_EFILE_INDEX has no amounts; officer pay came from XML | frontier list |
| W-052 | NASA nighttime lights | NASA | county and ZIP hubs | frontier list |
| W-053 | FEMA NFIP flood claims | FEMA | NFIP held but has no FIPS and a '/'-joined county name (Hub A seed 7) | frontier list; expansion |
| W-054 | DoD 1033 police militarization | DoD | JUSTICE__RACIAL_JAIL_DISPARITY, VERA | frontier list |
| W-055 | FAA registrations + flight tracks | FAA | — | frontier list |
| W-056 | FHWA National Bridge Inventory | FHWA | county hub | frontier list |
| W-057 | FMCSA carrier safety | FMCSA | OSHA 300A by EIN | frontier list |
| W-058 | US Customs bills of lading | CBP | AIS IMO/MMSI, UK sanctions | frontier list |
| W-059 | OFAC sanctioned crypto wallets | Treasury | XC_UN sanctions | frontier list |
| W-060 | US foreign aid + AidData Chinese loans | USAID; AidData | FARA / FOREIGN_INFLUENCE | frontier list |
| W-061 | OONI internet-censorship measurements | OONI | — | frontier list |

#### Frontier list, round 2

| id | dataset | who publishes it | what it would pair with | sources |
|---|---|---|---|---|
| W-062 | IPUMS full-count census 1850-1940 | IPUMS | HOLC maps, history shelf | frontier list |
| W-063 | Chronicling America 20M newspaper pages | LoC | — | frontier list |
| W-064 | SlaveVoyages + Freedmen's Bureau | Emory; NARA | history shelf | frontier list |
| W-065 | CDC WONDER mortality 1968-2016 | CDC | DRUG_POISONING_COUNTY 1999-2015 | frontier list |
| W-066 | FDA Orange Book | FDA | Part D by drug | frontier list |
| W-067 | USPTO PatentsView | USPTO | Waco patent surge (FJC IDB NOS 830) | frontier list |
| W-068 | OpenAlex + Unpaywall | OpenAlex | NIH_REPORTER PI names | frontier list |
| W-069 | FFIEC Summary of Deposits back to 1994 | FFIEC | held: FDIC_SOD_BRANCH_DEPOSITS 1994-2025 | frontier list |
| W-070 | MSRB EMMA muni disclosures | MSRB | stadium bonds, Census of Governments | frontier list |
| W-071 | SEC Form 4 insider trades + 13F | SEC | 13F held (101,261,252 rows landing); Form 4 not | frontier list |
| W-072 | Public Plans Database | CRR | — | frontier list |
| W-073 | NVDRS violent deaths | CDC | VERA jail, CDC injury | frontier list |
| W-074 | NEMSIS 60M ambulance runs a year | NHTSA | overdose county series | frontier list |
| W-075 | Daily tract PM2.5 surfaces | EPA / academic | AIR_EMISSIONS, ICIS-AIR | frontier list |
| W-076 | DOI ONRR royalties by company | DOI | BLM claims, GLEIF parents | frontier list |
| W-077 | USGS NWIS groundwater | USGS | USGS_WATER held (6,694,816 numeric-lat rows); SDWA | frontier list |
| W-078 | BLM mining claims | BLM | MSHA mines | frontier list |
| W-079 | BLM General Land Office patents | BLM | history shelf | frontier list |
| W-080 | FCC political ad files | FCC | GOOGLE_POLADS_* held | frontier list |
| W-081 | Medill news-desert + Media Cloud | Medill | county hub | frontier list |
| W-082 | EU DSA takedown database | EU | — | frontier list |
| W-083 | 287(g) roster | ICE | ICE_DETENTION_STINTS | frontier list |
| W-084 | CBP/IOM border-death points | CBP; IOM | — | frontier list |
| W-085 | ORR child-placement geography | HHS ORR | Southwest Key (FAC) | frontier list |
| W-086 | FCC broadband map | FCC | county hub | frontier list |
| W-087 | InSAR land-subsidence rasters | USGS / NASA | Oklahoma injection wells, FRACFOCUS | frontier list |
| W-088 | Census of Governments special districts | Census | MSRB EMMA | frontier list |

#### Frontier list, round 3

| id | dataset | who publishes it | what it would pair with | sources |
|---|---|---|---|---|
| W-089 | OpenSanctions | OpenSanctions | XC_UN sanctions; sanctioned-name matches were 100% noise on eye check | frontier list; table map |
| W-090 | UK Companies House PSC | Companies House | held now: 15,804,611 rows | frontier list |
| W-091 | Global Fishing Watch encounters | GFW | AIS (one week only) | frontier list |
| W-092 | Paris MOU ship detentions | Paris MOU | AIS IMO | frontier list |
| W-093 | First Street climate risk | First Street | FEMA IA, HUD | frontier list |
| W-094 | Climate Impact Lab county mortality | CIL | county hub | frontier list |
| W-095 | WRI Aqueduct water futures | WRI | SDWA, USGS water | frontier list |
| W-096 | Climate Central Billion-Dollar Disasters | Climate Central | STORM_EVENTS, FEMA declarations | frontier list |
| W-097 | EFF Atlas of Surveillance | EFF | DoD 1033, police index | frontier list |
| W-098 | Leaked ShotSpotter sensor locations | — | JUSTICE hub | frontier list |
| W-099 | Palantir deployment corpus | — | USAspending contracts | frontier list |
| W-100 | ICIJ Offshore Leaks graph | ICIJ | held now: 3,339,267 edges | frontier list |
| W-101 | FinCEN SAR Stats + GTO counties | FinCEN | county parcels, HMDA | frontier list |
| W-102 | WY/NV/DE registered-agent data | states | UK mailbox-address finding, US twin | frontier list |
| W-103 | OPTN/SRTR transplant registry | HRSA | CMS_DIALYSIS | frontier list |
| W-104 | FDA plasma-center registry | FDA | county hub | frontier list |
| W-105 | March of Dimes maternity deserts (AHRF) | March of Dimes; HRSA | HPSA_PRIMARY_CARE | frontier list |
| W-106 | Stadium bond issuances | MSRB / press | MSRB EMMA | frontier list |
| W-107 | State cannabis license + sales | states | — | frontier list |
| W-108 | Lottery retailer + sales | states | county hub | frontier list |
| W-109 | FERC Form 1 | FERC | EIA plant and utility edges | frontier list |
| W-110 | LBNL interconnection queue | LBNL | EIA plants | frontier list |
| W-111 | BIS Entity List | Commerce | XC_UN, OFAC | frontier list |
| W-112 | TeleGeography submarine cables | TeleGeography | — | frontier list |
| W-113 | Epoch AI model/compute | Epoch | — | frontier list |
| W-114 | DOE Section 117 foreign gifts | Dept of Education | FARA / FOREIGN_INFLUENCE, NIH_REPORTER (Lieber) | frontier list |
| W-115 | IRS DAF filings (Schedule D) | IRS | IRS_EO_BMF, 990 | frontier list |
| W-116 | FACA advisory-committee database | GSA | LDA filings | frontier list |
| W-117 | OSC/MSPB whistleblower records | OSC; MSPB | — | frontier list |

#### Frontier list, rounds 4 and 5

| id | dataset | who publishes it | what it would pair with | sources |
|---|---|---|---|---|
| W-118 | SBA 8(a) Tribe/ANC flag | SBA | USAspending contracts | frontier list |
| W-119 | Cobell Land Buy-Back ledger | DOI | — | frontier list |
| W-120 | IJ Policing for Profit + DOJ equitable sharing | IJ; DOJ | JUSTICE hub, VERA | frontier list |
| W-121 | CFPB complaints + prison-fintech enforcement | CFPB | CFPB_COMPLAINTS held, 17,168,287 rows | frontier list |
| W-122 | WaPo Fatal Force ORI crosswalk | WaPo | police index, DoD 1033 | frontier list |
| W-123 | Campaign Zero union-contract protections | Campaign Zero | police index | frontier list |
| W-124 | National Police Index | — | JUSTICE hub | frontier list |
| W-125 | FWS Section 7 Biological Opinions | FWS | ECHO, FRS | frontier list |
| W-126 | CITES trade database | CITES | US Customs bills of lading | frontier list |
| W-127 | NOAA tide-gauge trends | NOAA | First Street, FEMA | frontier list |
| W-128 | Oklahoma injection-well volumes | OCC | FRACFOCUS, InSAR | frontier list |
| W-129 | Dialysis facility file + reports | CMS | landed 2026-09-05: MEDICARE_DIALYSIS_FACILITIES, YEAR 2021-2024 | frontier list; expansion |
| W-130 | MA prior-auth denial + overturn | CMS | HOME_HEALTH, hospital stars | frontier list |
| W-131 | PEN America book-ban index | PEN | — | frontier list |
| W-132 | 60 years of NEH/NEA/CPB grants | NEH; NEA; CPB | USAspending assistance | frontier list |
| W-133 | Wikimedia pageviews + protection logs | Wikimedia | — | frontier list |
| W-134 | Virginia court dispositions 33.5M | Virginia courts | CL_PERSON_ID, DOCKET | frontier list |
| W-135 | Cook County felony charges | Cook County | JUSTICE hub | frontier list |
| W-136 | New York case-level bail | NY courts | JUSTICE hub | frontier list |
| W-137 | Tyler Odyssey deployments 600+ counties | Tyler / counties | JUSTICE hub | frontier list |
| W-138 | Deportation Data Project | UC Berkeley | ICE_DETENTION_STINTS, EOIR | frontier list |
| W-139 | House Epstein estate files | House Oversight | Epstein link scrapes already in the inventory | frontier list; docket v2 notes |
| W-140 | NYC Class-C violations by owner | NYC HPD | HUD projects, owners | frontier list |
| W-141 | Cook County scavenger tax sale | Cook County | county parcels | frontier list |
| W-142 | State AG multistate roster | NAAG | FDIC_ENFORCEMENT_ORDERS, CFPB | frontier list |
| W-143 | State False Claims Act recoveries | states | LEIE, SAM exclusions | frontier list |
| W-144 | FracFocus | FracFocus | held now: 7,200,550 rows | frontier list; lab map |
| W-145 | EPA UST/LUST | EPA | FRS, RCRA | frontier list |
| W-146 | EU procurement / Opentender | Opentender | USAspending twin abroad | frontier list |
| W-147 | IATI aid flows | IATI | US foreign aid | frontier list |
| W-148 | World Bank debt-by-creditor | World Bank | AidData | frontier list |

## Part 2: the words

#### Glossary: the words the book uses

| id | word or line | what it means or why it is kept | sources |
|---|---|---|---|
| W-149 | warehouse, schema, table, key, bridge, chain, turn, move, lens, hit, miss, docket, trap | the tool box vocabulary; docket lives in docket/docket.csv, traps in .claude/traps.md | tool box |
| W-150 | steel key | a 98-100% join key: NPI, CCN, FRS_ID, PWSID, NPDES_ID, LEI, CL_PERSON_ID | join depth; docket v2 notes |
| W-151 | turn | a chain hop where the entity kind changes (doctor to facility to company) | join depth |
| W-152 | pivot / bridge | a table carrying two keys | join depth |
| W-153 | crawl / walk / run | docket v2 effort tiers: describe a table / join two / chain many | docket v2 notes |
| W-154 | tier 1 / 2 / 3 | whether a hunch's chain is live and testable, not whether it came out true; a killed claim with a dated before/after is still Tier 1 | expansion #33 |
| W-155 | hub A, B, C, X | county, clinician, facility, cross-hub — the expansion's four seed families | expansion |
| W-156 | DiD | difference-in-differences: treated change minus control change | expansion |
| W-157 | floor | an undercount by construction; every count on a capped table is one | expansion |
| W-158 | carbon-dating | infer a CMS file's vintage from the newest NPPES enumeration date in it | expansion |
| W-159 | the Frank shape | one owner across SNF and hospice; 7,127 physicians have the three-facility version | expansion; frank hospice |
| W-160 | "Ripple" | means exactly one thing: the platform | ripples |
| W-161 | stations | the real things watched (a doctor, a mine, a water system) | ripples |
| W-162 | readings | the same simple measurements taken at every station | ripples |
| W-163 | fronts | connections: shared owner, address, officer | ripples |
| W-164 | seasons | the shared timeline; each pull is one observation | ripples |
| W-165 | instruments | a dumb question mounted once and run everywhere | ripples |
| W-166 | blip | passed the luck check, unconfirmed; a queue, not a claim | ripples |
| W-167 | warning | answered loudly, worth a human's time | ripples |
| W-168 | leading indicator | a stream that moves before another | ripples |
| W-169 | finding | a warning that survived resemblance, fronts, and Chris's sign-off | ripples |
| W-170 | dead air | the hand-off that should happen but does not | ripples |
| W-171 | false readings | wrong explanations; there is no forbidden data | ripples |
| W-172 | the climate | the shared background rhythm every series rides | ripples |
| W-173 | older strata keep their names | entity spine, connection tiers, clock lanes, detectors, 52-lens catalogue, queue-vs-finding law | ripples |
| W-174 | Reading Room tiers and timelines | FACT_GRADE_3_SOURCE, NPPES_CONFLICT, LEIE_ROW_MISSING; PAID_ON_OR_AFTER_EXCLUSION, PAYMENTS_PREDATE_EXCLUSION | hour dossier |
| W-175 | LEAD shape | LEAD_ID, title, detector, score 0-1, bridge_key, evidence rows, first_seen, last_seen, review_state (pending/confirmed/rejected/retracted/stale), published bool; ENTITY_ID = 'ENT_' + LEFT(MD5(key_type, a pipe, val), 16) | design brief |
| W-176 | Wonder Wall effort scale | E1 core result under half a session; second half-session to split appeals from non-collection; watch AMOUNT_PAID zero-not-null; exclude trailing 24 months in the appeal window | tool box |
| W-177 | Statute glosses | 1128a1 program-related crime; 1128a2 patient abuse/neglect; 1128b7 fraud/kickbacks | frank; pharma paid |
| W-178 | Hunch numbering | 1-31 matrix; 76-144 matrix appendix 2; A32-A37 appendix 1; E32-E75 expansion; appendix-1 cards 32-37 collide with expansion #32-#75, so the master CSV uses A- and E- prefixes | matrix |
| W-179 | Top-50 portfolio buckets | Instant wow (1-12); Reader looks up their own (13-20); The shape is the story (21-33); Already has a number (34-40); Money and power (41-50) | top50 |

#### The ids that do the joining, and the source names

| id | word or line | what it means or why it is kept | sources |
|---|---|---|---|
| W-180 | NPI clinician; CCN facility; EIN organisation; CIK SEC company; LEI legal entity; UEI/DUNS contractor; FRS_ID EPA facility; PWSID water system; NPDES_ID discharge permit; BIOGUIDE member of Congress; FIPS county/state; ZCTA zip area; CL_PERSON_ID court person; IMO/MMSI ship | the fourteen ids; HEALTH, FINANCE, ECONOMICS, ENVIRONMENT, CORPORATE_REGISTRY carry the deepest lens coverage because they anchor the four real bridges NPI, EIN, FRS_ID, CCN/UEI | tool box |
| W-181 | NPPES clinician registry; HCRIS hospital cost reports; LEIE Medicare ban list; LDA lobbying disclosure; ECHO EPA enforcement history; TRI toxic release inventory | the source nicknames | tool box |
| W-182 | Only 14 connection families are rock-solid | next tier is name+zip; politics has zero hard links (since corrected by the member chain); courts, sanctions, ARCOS, ICIJ are graph dark matter | ripples |
| W-183 | Healthcare has the cleanest IDs; environment and corporate ownership mostly do not | why the health shelf is richest | pitch deck |
| W-184 | Thin or absent domains | energy, agriculture, insurance, Social Security | capabilities |
| W-185 | "The DEA number connects to nothing." | REPORTER/BUYER_DEA_NO live only in ARCOS | graph bridges |
| W-186 | FRS_ID to LEI is "the sleeper" | 73,948 same-row pairs, 100% match, the only facility-to-company bridge | graph bridges |
| W-187 | "The CCN is what held." | name-only matching would have missed both of Frank's facilities | frank hospice |
| W-188 | Rule-change dates are constants, not tables | PDPM 2019-10-01 | table map |

#### Framing lines: what the project is

| id | word or line | what it means or why it is kept | sources |
|---|---|---|---|
| W-189 | "Put two files side by side that were never meant to meet, and see what falls out." | the whole project in one line | tool box |
| W-190 | "The EPA tracks the pipe, Medicare tracks the patients, nobody joins them; the tax form says what the CEO earns, the Medicare report says what the hospital gave away." | the pitch in two joins | tool box |
| W-191 | "Has anyone ever just... put those two lists next to each other?" | the dumb question | pitch deck |
| W-192 | "Not sophisticated analysis. Not AI making predictions. Just: is this entity on List A and also on List B." | the idea, stated flat | pitch deck |
| W-193 | "The joins are just... sitting there." | why it might matter | pitch deck |
| W-194 | "Either I'm onto something, or I'm missing a reason why nobody does this." | the open doubt | pitch deck |
| W-195 | "No funding. No team. No proprietary data. Just public records and a question that wouldn't leave me alone." | the close | pitch deck |
| W-196 | Is this a product? | undecided: journalists, oversight, dataset, portfolio | pitch deck |
| W-197 | "A census of the public record, not a search for one target." | the script's frame | the script |
| W-198 | "A single anecdote only matters if the data proves the pattern is real and repeated." | the script's bar | the script |
| W-199 | "Credibility is the product." | honest limits over reach | capabilities |
| W-200 | Zero false merges | the spine never guesses two similar names are one | capabilities |
| W-201 | "We show our work." | credibility through honesty; the smells raise their own hand, the human decides; editorial desk / data terminal, monospace-adjacent, evidence-forward, not a rounded consumer app | design brief |
| W-202 | "Simple pieces. Honestly measured. Allowed to touch. Then the patterns draw themselves." | the Ripples core idea | ripples |
| W-203 | "Complicated pieces can't do this. The moment a piece gets clever, it gets incompatible." | why atoms stay simple | ripples |
| W-204 | "That pattern exists in no single row anywhere." | the worked example's point | ripples |
| W-205 | "It's a lens, not a checklist." | new Ripples welcome; State, Neighbors, Flow are the first three | ripples |
| W-206 | "It is a thinking tool, not a checklist. Skim for a hunch, not a recipe." | how to use the tool box | tool box |
| W-207 | Most people walk in one way: "do these two things correlate?" There are twenty-seven ways | the moves | tool box |
| W-208 | "This is a menu, not a plan." | the lab map header | lab map |
| W-209 | "This is not a diagramming tool. It is an instrument for finding things that aren't there." | the atlas | blueprint |
| W-210 | Cosmology analogy | real universe ~5% ordinary, 27% dark matter, 68% dark energy; Library 14.9% lit, 20.5% dark-but-charted, 64.7% never looked at | blueprint |
| W-211 | "The organizing force is already in the data — the job is to draw it, not invent one." | atlas layout principle | blueprint |
| W-212 | "So the beauty and the truth are the same object." | atlas lineage | blueprint |
| W-213 | Migration glide of a newly-connected table | "the single most motivating pixel in the design" | blueprint |
| W-214 | "Pie in the Sky" | the tabled project that will score novelty | wonder rank |
| W-215 | "The case serves the map." | a top-10 review is a receipt check, not the deliverable | hour dossier |
| W-216 | "v1 asks is someone cheating. v2 asks what would a stranger stare at." | the docket's turn | docket v2 vs v1 |
| W-217 | "542 ideas. Three moves." / "The 542 lines are not wrong. They are one move repeated." | the honest count | idea moves |
| W-218 | "A catalog of 934 questions is a way of never starting. The data raising its own hand is faster and more honest." | Chris rejected this framing: "You do not tell me what the moves are... Fuck off with that." | how to hunt; handoff 09-08 |

#### How to hunt, and how to doubt

| id | word or line | what it means or why it is kept | sources |
|---|---|---|---|
| W-219 | "Don't look for things. Look for weird, then read the weird." | the lab's first rule | lab |
| W-220 | "The computer does breadth, you do depth." | five weirdness passes | lab |
| W-221 | "Find the story by playing, not by planning." | the slot machine | lab |
| W-222 | "Before-and-after is the cleanest visual there is. Build it first." | time series shapes | lab |
| W-223 | "You found something. Now assume you're wrong." | most exciting findings are load bugs, duplicate joins, or one person's note taken too seriously | tool box |
| W-224 | Fighting is the interesting answer; numbers that do not follow Benford were probably typed, not counted | tool box Part 2 | tool box |
| W-225 | "A stranger feels a turn; nobody feels a seventh join." | what makes a chain impressive | tool box; join depth |
| W-226 | "A chain survives by multiplying its per-hop match rate. Depth is not the constraint. The kind of key is." | the mechanic | join depth |
| W-227 | Money traceable from one doctor's pocket to a county's morgue | Chain A hit | tool box |
| W-228 | "Untimed numbers are not findings." | the FEMA-contract lesson | matrix #15 |
| W-229 | "Nothing here is a finding yet. These are seeds with a first number attached." | matrix intro | matrix |
| W-230 | "Refine means hone in. Nothing was dropped." | matrix intro | matrix |
| W-231 | "What the skeptics fixed was the reading, not the arithmetic." | 43 of 44 numbers reproduced within 1% | expansion |
| W-232 | "The base rate wearing a hat." | a sprinkler flag that is 99.58% Yes | expansion #62 |
| W-233 | "Landed is not loaded; check a fill rate before calling a table the bridge you need." | PRF, TAGGS | expansion #75 |
| W-234 | "dead covers two endings. One: there is no pattern. Two: the years do not line up. Both mean stop." | docket README | docket readme |
| W-235 | "It tells you the tables are on the shelf. That is all it tells you." | the data check | docket data |
| W-236 | "The single widest constraint: value is present, type is wrong. The single widest unlock is one boundary-file ingest." | lab map one-screen | lab map |
| W-237 | "The rollups already exist — 14 of them — and every single one is blind below the state line." | aggregate first | lab map |
| W-238 | "The spine links things to files, not to each other." | network centrality | lab map |
| W-239 | "Things moving together here usually means they were downloaded together." | finance correlation | lab map |
| W-240 | "a mechanism with a body attached" | a death with no enforcement record | wonder rank |
| W-241 | "MSHA is the healthiest source on this wall, by a distance" | four of the top seven are MSHA and that is a finding, not a bias | wonder rank |
| W-242 | "The Narrative lens is not dead — it is pointed at the wrong tables" | MSHA narrative is what #66 should have asked for | wonder rank |
| W-243 | "One dot is a receipt, not a map" / "A single line is a receipt, not a map" | the scope-law failure mode in wonder form | wonder rank |
| W-244 | "the finding would describe the ingest, not the institution" | loaders all starting 2023 | wonder rank |
| W-245 | "One fix, many wonders. Same gap hit by several arcs independently." | gap ledger | table map |
| W-246 | "Dead in public data, say so in the wonder" | table map rule | table map |
| W-247 | "The 'interesting question' takes five minutes. Making sure the answer is actually correct takes days." | problem 3 | pitch deck |
| W-248 | "That's not ideology — that's access purchasing." | both-sides PACs | pitch deck |
| W-249 | "I hold everything loosely." | one person doing QA on own work | pitch deck |
| W-250 | "That is a lead of unusual quality. It is not a conclusion." | Frank | frank |
| W-251 | "$468.77 does not buy $406,124. The payments show who was in the building." | Frank step 6 | frank |
| W-252 | "A finding about the join, not about American industry" | EPA contractor view | findings views |
| W-253 | "A headline without a body" | the SpaceX ratio | findings views |
| W-254 | "This is not a discovery about Caterpillar. It is a discovery about the SEC, which publishes quarterly." | table-count artifact | graph hunt |
| W-255 | "The naive join reads the arrow backwards." | exclusion after the file year | ghost doctors |
| W-256 | "A publication rule, not a corporate structure." | Part B by provider has no payee | ghost partb |
| W-257 | "Devices pay royalties and consulting fees; drugs buy lunch." | Open Payments nature split | pharma paid |
| W-258 | "None of them cross-checked a free, public, monthly-updated federal list before writing the cheque." | 141 manufacturers | pharma paid |
| W-259 | "The largest single transfer of value in this company's 2024 filing went to a doctor the government barred the following year." | Skye and Frank | molina |
| W-260 | "Cheap unit price against a high unit count is the consumables shape, not the fraud shape." | Frank DME | frank dme |
| W-261 | "A percentile inside a distribution with a hole in it" | censored dementia column | frank dme |
| W-262 | "The ratio is a flag, not a verdict." | recert ratio | frank hospice |
| W-263 | Censoring cuts both ways on the recert measure | low-volume vanish (flatters); low-cert high-recert drop (damns) | frank hospice |
| W-264 | Junk signature vs good signature | junk: predates exclusion + tiny dollars + name conflict + gutting caveat; good: three-source + paid-after + continuing activity | hour dossier |
| W-265 | All-rejects still counts | a finding about detector precision | hour dossier |
| W-266 | "Treats 'it looks complete' as a hypothesis to test." | the script | the script |
| W-267 | "Loaded" and "trustworthy" are two tracked states | the script | the script |

#### Chris's words

| id | word or line | what it means or why it is kept | sources |
|---|---|---|---|
| W-268 | "organize all of these into an easy to read, understand, and reference, singular source. We are going to call it The Idea Book"; "no information or ideas lost, but I dont want redundancy" | the brief for this book | brief |
| W-269 | "I want you to do a full 'mapping' of real world things that have come to light and whether or not my data would corroborate or 'discover' the same thing... Go looking" | the news-corroboration ask | tool box |
| W-270 | A real hunt through the warehouse using TOOL_BOX.md, not brainstorming: run queries, chase candidates, walk the chain, one file back | the hunt ask, near-verbatim | session 09-08 |
| W-271 | Chris picked C: sweep for the traps a machine can find, hunt for the ones that need a hunch | the split | session 09-08 |
| W-272 | "stop being lazy and make sure you actually follow through on what you say. You're messing me up and my timelines now." | correction | handoff 09-08 |
| W-273 | Chris directs, you figure out how | pushback wanted only when something is factually wrong (say so with the number) or he asks for a dissection | handoff 09-08 |
| W-274 | Riff mode | widen the field, bring three more angles, name a wilder version, answer at his altitude, follow through; do not narrow, rank and cut, explain why the wild one is hard, drop to plumbing unasked, substitute a task | handoff 09-08 |
| W-275 | Opus hunt prompt | no quotas, depth over breadth, five findings that survive beat twenty that don't; "not anomaly pipeline, duplicate NPIs at one P.O. box" | opus prompt |
| W-276 | Crossjoin story lines | "Two filings that never meet"; "FDA registry and CMS payments are two agencies with no reason to talk"; "Army Corps, CMS and HUD, three agencies, one physical fact"; "A 90-year-old map and an annual bank survey on the same ground" | crossjoin 25 |

#### Pointers, receipts, status

| id | word or line | what it means or why it is kept | sources |
|---|---|---|---|
| W-277 | Box contents claimed | 61 lenses, 27 moves, 5 checks, 934 questions, 25 cross-joins, 93 ranked wonders, 41 viz ideas, 24 corroboration tests, ~175 traps; last touched 2026-09-08 | tool box |
| W-278 | Wonder Wall top 5 on deck, excluded from the wow list | E1 the vanished $548M; E2 the state inspector spread (9.5x); #55 deaths with no paper trail; E7 the minority-community inspection gradient; E8 staffing predicts the next deficiency; #26/#72 same-owner co-spike answered 2026-08-21 | wow ideas; tool box |
| W-279 | Wonder Wall run 2026-08-22 | 93 ranked: 75 from The_Wonder_Wall.md plus 18 expansion; The_Wonder_Wall.md is gone from the repo, wonder_rankings.md is the surviving copy and restates wonders as one-line questions; wonder list and table map dated 2026-09-09; the list is "ideas only. No status, no results." | tool box; wonder rank; wonder list; table map |
| W-280 | Repeat-offender traps named by the table map | HMDA historic originations only; FEC itoth memo double-count; Part B suppressed subset; portal 10k cap; INGESTED_AT epoch micros | table map |
| W-281 | Standing traps recalled in the docket | registry VOLUME free text; registry notes stale; landing name ≠ UPPER(SOURCE_ID); zip loads keep largest member; warehouse MCP dead; Utah portal names facility not owner; watermark vs keyset; 'never landed' needs LIKE search; FEC itoth 93% memos; portal tables cap at 10,000; INGESTED_AT two names three types; single-word matches 8% real; HMDA two families; ZIP reach is not a join; NPPES EIN empty; USASpending assistance 1M/yr; CDC injury has overdose; Part B suppressed subset; facility affiliation under-reports; ANTPSYCT spelling; percentiles need common cohort; DME referrer lies three ways; CKAN package is a folder; no org-to-person bridge; NH CHOW flag constant, TRI coords DDMMSS | memory index |
| W-282 | Reports these files contradict and flag | reports/partb_carbon_date_2026-09-05.md (DY2022 wrong, is DY2024); .claude/traps.md line 83 (injury file has overdose), 84 (HCRIS not one FY), 89 (LEIE 8,660 distinct not 8,661), 30 (ASSISTANCE_FULL is a cap); graph_bridges 68.5% FAC-to-ASSISTANCE edge is a floor | expansion |
| W-283 | Nine trap-log entries written 2026-09-08 from the hunt | seven under the dated heading, two late ones after the sweep, not skeptic-checked | hunt 09-08 |
| W-284 | Hunt queries kept for re-run | F1.1-F1.9 OSHA, F2.1-F2.7 PPP, F3.1-F3.3 FRS, F4.1-F4.6 EIN bridge, F5.1-F5.10 skeptic re-checks incl. shuffle placebo; Finding 5 block and whole-file queries; all in toolbox_hunt_2026-09-08.md | hunt 09-08 |
| W-285 | Findings 2, 3, 4 of the hunt are shippable and unbuilt | no chart, no page; nothing published anywhere | session 09-08 |
| W-286 | Per-subject recon notes | HEALTH richest shelf, NPI steel; POLITICS member card ready on Bioguide, TX and CA lobbying are mini-warehouses; ENVIRONMENT three facility pages; JUSTICE judge card and 50 years of IDB; FINANCE company card, cross-key legs thin; ECONOMICS EIN second steel key, Treasury pure timelines; ENERGY 2024-only except generators, several 861 tables lost a header row; HOUSING HMDA 2015-2017 only, FEMA 12% partial (since corrected to full); IMMIGRATION person ids anonymized; TIMELINE charts the warehouse not the world; REFERENCE ITIS and GNIS are single-table wow | tool box |
| W-287 | Probe receipts | matrix probes in scratchpad dab9ca80-.../hunch_probes*.py; expansion in ee9da5e0-.../hubA hubB hubC hubX, verify/<id>/, wish/; results JSON hunch_expansion_32_75_2026-09-05.results.json beside the report | matrix; expansion |
| W-288 | hunch_plain_english is superseded | 2026-09-06 by catalog/investigations.csv with a controlled status vocabulary; do not edit it | plain english |
| W-289 | Docket v1 status vocabulary had grown to 89 phrasings for six states | four 2026-09-05 spreadsheets held the same 150 rows | docket readme |
| W-290 | Docket rebuild commands | python scripts/build_docket.py; python scripts/docket_data_check.py; page ranks by table count then rows, a guess not a promise | docket readme |
| W-291 | Expansion directive asked for #32 to #50 | sweep returned 44, numbered #32-#75 tier 1 first | expansion |
| W-292 | Session skeptic vs hunch skeptic disagreement | #60 tier 1 vs tier 2; held at 2 until the yearly dialysis file is run | expansion |
| W-293 | Evidence folder for the lab map | reports/lab_map/ (metadata dump, shape index, per-signal candidates, verified-facts file) | lab map |
| W-294 | Receipts for the 09-04 joins | reports/join_proof_2026-09-04.md; shuffle code reports/ripples_neighbor_rule_2026-08-21.md | lab; lab map |
| W-295 | Deepfield stack (reference, not a spec) | WebGL2/Three.js orthographic, instanced SDF quads, prebaked ribbon VBO, troika SDF labels, GPU colour-pick, HTML chrome, zustand + URL, shader mix() morphs; ~4 draw calls, <200k triangles; holds past 10,000 tables | blueprint |
| W-296 | Design brief palette | STEEL #f4a23a, BRIDGE #b07cf0, STRONG blue, CORROBORATED cyan, GEO green, PROBABILISTIC gray; bg #0d1117, text #e8eaed, danger #e5534b, accent #4c9aff | design brief |
| W-297 | Existing surfaces | connection_explorer.html (~17MB, CDN Plotly); plane.html (offline, ~5.3MB with vendored mermaid, CARD unbuilt); leads_overlay.html (stale, CDN); connect_graph.json (~7.3MB, data behind every map); PLANE_handoff.md; vendored outputs/plotly.min.js 4.8MB not wired in | design brief |
| W-298 | Design-brief open defaults | domain colour deferred to v1 (660/720 are `other`); pre-render + vendor mermaid; lifecycle colours (9 trust-gated stubs) in v1; dossier timing undecided | design brief |
| W-299 | Reading Room | http://127.0.0.1:8890; reads on RIPPLE_READER via SNOWFLAKE_SERVE_PAT; writes on RIPPLE_REVIEW_WRITER; done = V_STATE decisions.total >= 10, then export decisions to git; detector batch 2026-06-26 to 28; queue mart recomputes fresh, never trusts capped evidence | hour dossier |
| W-300 | Vessel AIS is a Jan 1-8 2024 snapshot; SAM table is a 1,000-row capped sample with no dates | hour-dossier caveats | hour dossier |
| W-301 | SDWIS sample periods may sit a step late | skeptic suspicion left open | news map |
| W-302 | Frontier list | 137 datasets across 5 rounds, 2026-06-30 to 07-01; pairings live in the per-round briefs | frontier list |
| W-303 | Hiring-manager skills list | 875M-row warehouse; 1,378 dbt models; ETL with atomic loads; graph entity resolution; temporal SQL | pitch deck |
| W-304 | AI helped build it; the finished system runs on plain SQL; loaders checkpoint so multi-hour jobs resume | the script | the script |
| W-305 | THE_SCRIPT is a pull-from bank, not one block; general-adult reading level | the script | the script |
| W-306 | Skye's 30 write-offs listed in full with NPI, entity, state, amount, date | in the Molina report | molina |
| W-307 | Receipts for the capabilities census | reports/noun_event_inventory_2026-08-18.md; reports/census_grid_2026-08-12/ | capabilities |
