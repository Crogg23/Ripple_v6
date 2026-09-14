# Dead ends

174 rows, merged from 188 extract dead ends across five families.

Read the first column to recognise the attempt before repeating it; the second column is the mechanic that killed it, with the number that proves it.
The third column points at what still lives: a corrected finding in the F chapter, a wish-list dataset, or none.

Source short names: tool box = TOOL_BOX.md; hunt 09-08 = toolbox_hunt_2026-09-08; wow probe / wow ideas / how to hunt / session 09-08 / handoff 09-08 / opus prompt = the 2026-09-08 papers; wonder rank / wonder list / table map = wonder_rankings, wonder_list_2026-09-09, wonder_table_map_2026-09-09; matrix / expansion = hunch_matrix_refined, hunch_expansion_32_75 (2026-09-05); docket * = docket/ folder files of 2026-09-07; lab / lab map / viz inv / viz catalog / blueprint / design brief = The_Laboratory, Laboratory_Warehouse_Map, viz_ideas_inventory, viz_join_catalog_2026-09-04, DEEPFIELD_ATLAS_BLUEPRINT, RIPPLE_DESIGN_BRIEF; ripples / pitch deck / frontier list / capabilities / hour dossier / the script = RIPPLES.md, ripple_pitch_deck, ripple_frontier_MASTER_LIST, warehouse_capabilities_2026-08-18, HOUR_DOSSIER, THE_SCRIPT; the rest are reports/*_2026-09-05.md by name.


#### Claims struck by a skeptic or a re-run

| id | what was tried | why it died | nearest live version, if any | sources |
|---|---|---|---|---|
| D-001 | Big employers under-report injuries; tell is a zero rate that stops falling with size | the turn-up was multi-site filers repeating one page; after tuple dedupe the curve falls straight 67.7% to 2.4% | the deduped curve (F chapter, OSHA) | hunt 09-08 |
| D-002 | Peer-group outlier: construction at 30.4% zero | one filer, Caltrans, 470 rows | Caltrans copy-paste finding | hunt 09-08 |
| D-003 | "$1,000 multiples run 116x chance, $1M 2,210x" | uniform-digit baseline; the file's own 52.3% mod-100 rate refutes it; real per-digit excess 2-3x; struck | PPP ladder at constant precision | hunt 09-08 |
| D-004 | "The biggest PPP loans are the roundest" | fixed-modulus artifact; flat at 2 sig figs, falls by half above $1M at 3; struck | roundness by size row | hunt 09-08 |
| D-005 | "The floor is Truist at 1.42%" | floor of the 15 displayed, not the 205 measured; true min 0.23%, 12 of 205 under 1%; struck | lender mod-100 spread | hunt 09-08 |
| D-006 | "$100 clustering at 52.3%" as a finding | lender convention, 1.2% to 100.0% across lenders | the $10,000 rounding survives the lender control | hunt 09-08 |
| D-007 | Regression discontinuity at $150k on PPP | the spike is one round number, 6,596 of 11,597 in the first bucket | none | hunt 09-08 |
| D-008 | Regression discontinuity at the $2M SBA audit line | the cliff is the second-draw statutory cap; vanishes on PROCESSINGMETHOD split | none | hunt 09-08 |
| D-009 | Lender rounding convention explains the $10k rounding | 4,117 lenders, only 7 of 205 big ones over 10%, carrying 9% of round loans | open: what does explain $10k | hunt 09-08 |
| D-010 | "There is no complete list of EPA facilities in the warehouse" | went past the evidence; two tables compared, seven other REGISTRY_ID tables unchecked; retitled | two FRS tables, neither contains the other | hunt 09-08 |
| D-011 | FRS orphan state rollup | FAC_STATE NULL on 61,485 rows joined away; fixed with null-safe count | null-safe count | hunt 09-08 |
| D-012 | Median headcount ratio 1.01 as evidence of agreement | shuffle placebo gives 1.19; the median is nearly free | within-2x share with placebo (74.0% vs 32.6%) | hunt 09-08 |
| D-013 | All-zeros EIN sentinel asserted in OSHA from memory of LEIE | zero rows in 2023, 2024, 2025; never counted before being written | count first | hunt 09-08; session 09-08 |
| D-014 | Staffing-company EIN leak as a systematic effect | real mechanic, 2 rows in the whole 2024 file | none | hunt 09-08 |
| D-015 | Site-count scope effect on the Form 5500 tail | median flat at 1.00 from 1 site to 11+ | none | hunt 09-08 |
| D-016 | "57% of American doctors are graded as a crowd" (hunt Finding 5) | PARTICIPATION_OPTION already labels it; 91.4% non-individual; heuristic undercounted by 34 points; grain is PROVIDER_KEY not NPI; killed by session-close skeptic | QPP group-level finding | hunt 09-08 |
| D-017 | "Under one credit" sweep cost | derived from wall clock; metered figure is about 1.7 credits | sweep totals | session 09-08 |
| D-018 | Sweep S3 "one value in every row" in the 09-08 CSV | APPROX_TOP_K returns pairs, script read objects in a bare try/except; zero flags looked clean; fixed, 41 flags on 12 LABOR tables; S4 bare-year guard dead the same way, 506 rows unguarded; CSV predates the fix | re-run sweep after fix | session 09-08 |
| D-019 | Sweep on four tables | MARITIME__FED_NOAA_AIS, REFERENCE__CENSUS_CB_ZCTA, _CB_COUNTY, _CB_STATE fail with Invalid argument types for HLL, almost certainly a GEOGRAPHY column; not investigated | skip GEOGRAPHY columns | session 09-08 |
| D-020 | The 46-table "whole huntable warehouse" framing | a hand-typed 18-id filter over ~36,000 columns; dropped PROVIDER_ID, PERMIT_NO, DOCKET, CASE_NUMBER keys; required typed DATE while 27,653 columns are TEXT; treat how_to_hunt Parts 1 and 3 as suspect | rebuild the filter from the keyset | handoff 09-08 |
| D-021 | Wall's guess that Density and Structure were the rich lenses | scored second- and third-worst (31.9, 32.3); display lenses recover population and size | Combos, Surprise, Causal lead | wonder rank |
| D-022 | #73 Anomaly + Structure combo | both legs weak (#8 D2, #52 M2); flagged do not build | none | wonder rank |
| D-023 | Original Laboratory figure "~12.88M entities across 31 spine tables" | stale by ~4x; real 33,312,349 / 84,382,504 | entity counts row | lab map |
| D-024 | Carried note that FEMA IA mart was a 12% load (3.08M of 25.9M) | stale; mart holds 26,250,920 | full FEMA IA | table map |
| D-025 | Five agents searched THE_CATALOG.csv for a ZIP-to-county crosswalk | it lives in CORE, which THE_CATALOG does not list; "no crosswalk" was wrong | XWALK_ZCTA_COUNTY | table map |
| D-026 | "Nothing can place a ZIP on a map" as a flow-map blocker | wrong; ZIP > county > centroid is a two-hop join over existing tables | XWALK + DIM_COUNTY | lab map |
| D-027 | leads_overlay.html as current | built 6/27 with 4 detectors, 338/353 on one edge; live is 6 detectors, ~1,030 leads, 773; re-render first | re-render from live LEADS | design brief |

#### News stories the warehouse could not corroborate

| id | what was tried | why it died | nearest live version, if any | sources |
|---|---|---|---|---|
| D-028 | Life Care Center Kirkland 2020 survey (news 13) | CMS deficiencies file is a rolling ~3-year window; 2020 gone; vintage not load bug | archived Care Compare releases (wish list) | tool box; news map |
| D-029 | Ozempic FAERS 2023 (news 15) | FAERS stops 2014q2, semaglutide approved 2017; any post-2014 drug has no trail | current FAERS (wish list) | tool box; news map |
| D-030 | Kabbage fake farms in PPP (news 17) | only the 150K+ file landed (968,524 rows); the ~$20k loans are absent | address stacking works on the slice; loan-level all sizes (wish list) | news map; tool box |
| D-031 | Thomas and Crow gifts (news 21) | no people table to tie a disclosure to a judge; SOURCE is OCR with 58 nulls | Douglass bust row is on file | news map |
| D-032 | Upper Big Branch by raw violation count | ranks 10th; the story was withdrawal orders and S&S density | S&S share, not raw count | news map |
| D-033 | HMDA morning echo of the Reveal story | 19.1M rows all "Loan originated", zero denials; loader had taken the first-lien owner-occupied family; fixed same day with --family all | 44,992,667-row reload | tool box; news map |
| D-034 | "Reproduces Reveal" | raw rate ratio 3.4x / OR 4.35 vs Reveal's adjusted 2.7; a different statistic | same direction, say which statistic | news map; see F-312 |
| D-035 | Takedown "5 of 5" | Aquino tops out at 86th; it is 4 of 5 | 4 of 5 row | news map |
| D-036 | Lieber $13M; FEC donors by name+zip9; FJC TAPEYEAR | skeptic: $11.4M; zip9 splits people, use name+state; TAPEYEAR lags, use FILEDATE; also Thomas downgraded to miss, SAM caveat restored, three top-N lists non-contiguous, PWSIDs name-checked, SDWIS period lag left open | fixed rows in F chapter | news map; tool box |
| D-037 | Negative controls on the 24 stories | never run; every grade rests on one query | open | news map |

#### Wow ideas and wonders that hit a wall

| id | what was tried | why it died | nearest live version, if any | sources |
|---|---|---|---|---|
| D-038 | Wow 1 lie ledger via EIN, OSHA to SEC | only 648 EINs bridge; EDGAR_FINANCIALS is a DERA extract of 8,112 filers; a load question, not an idea question; pivoted to in-row OSHA contradictions | OSHA rows that contradict themselves | wow probe |
| D-039 | Wow 3 US contractor leg, USASpending address collision | exactly one ZIP with 100+ distinct recipients | UK mailbox addresses | wow probe |
| D-040 | Wow 4 / wonders #17, #38, #43: CMS nursing-home ownership change | PROVIDER_CHANGED_OWNERSHIP_IN_LAST_12_MONTHS 'N' on all 14,700; no ownership history table | NH411 'Y' on 55 rows; HHA owners file; PECOS All Owners (wish) | wow probe; wow ideas; wonder rank |
| D-041 | Wow 5 HMDA 2007-2017 as the long arc | span is 2015-2017, three years not eleven | FDIC branches 1994-2025 as the long spine | wow probe |
| D-042 | Wow 6 nursing-home fine bunching | 2.0% end in 00, the null result | MSHA round hundreds | wow probe |
| D-043 | Wow 7 OSHA leg, regulator as the variable | deaths per million hours 0.01 to 0.02 in every state, no spread | MSHA collection by state | wow probe |
| D-044 | Wow 10 government heartbeat as a finding | TIMELINE is 405 views over 36 tables; views carry no row count and freeze columns | none | wow probe |
| D-045 | Wow 14 AIS seasonality, cadence, before-after | one week of data, 2024-01-01 to 2024-01-08 | none | wow probe |
| D-046 | Wow 15 GLEIF ownership to FEC donors | no key: GLEIF speaks LEI, FEC speaks committee id and donor name; park until an LEI-to-employer bridge exists | none | wow probe |
| D-047 | Cosponsorship network as a wow piece | scale and name yes, stake no; nobody is harmed by the answer | none | how to hunt |
| D-048 | #66 inspection notes as topics | DEFICIENCY_DESCRIPTION is 260 canned labels, not notes | MSHA accident NARRATIVE, 273,621 rows | wonder rank |
| D-049 | #68 model legislation across states | no state legislation in the warehouse; federal bills TITLE only | none | wonder rank |
| D-050 | #69 FAERS dialects, #70 enforcement sentiment | no FAERS narrative, reporter type column shifted; no dated document corpus | none | wonder rank |
| D-051 | E15 shared-clinician contagion | 273 pairs share 5+ clinicians; too sparse | none | wonder rank |
| D-052 | #8 hidden bridge entity | 0.32% of entities span two domains; taxonomy 78% 'other' | none | wonder rank |
| D-053 | #42 regulator staffing cuts | no staffing/headcount table anywhere | none | wonder rank |
| D-054 | #4 inspector territories | no MSHA inspector identifier | none | wonder rank |
| D-055 | #28 OSHA violation epidemic | no OSHA violations landed; inspections re-pull mid-flight | OSHA enforcement (wish list) | wonder rank |
| D-056 | #5, #25, #49, #69 FAERS wonders | column shift in landing and marts | none until FAERS reloads | wonder rank |
| D-057 | #6, #13, #35 portal-index wonders | capped crawl, 76.8% missing column metadata | none | wonder rank |
| D-058 | #50 career fundraising rhythm; #45 money after the seat | FEC 2023-2026 only at ranking time; committee membership has no clock | 283.8M FEC load now spans 2000-2026 | wonder rank |
| D-059 | #20 politics percolation date | artefact of loaders all starting 2023 | none | wonder rank |
| D-060 | #51 warehouse growth curve | CREATED dates reset on rebuild | none | wonder rank |
| D-061 | Wonder 43 FAERS by prescriber state | no state or prescriber in FAERS | none | table map |
| D-062 | Wonders 57, 64 and docket v1 3, 17, 123: banks financing polluters | lender-to-facility edge not published at facility grain; only banks' own buildings; bank ID field empty everywhere; FDIC LEI column 0 of 27,836 filled | banks' own sites via the LEI bridge; HMDA denial rate by county vs TRI density | table map; tool box; docket v2 vs v1; matrix |
| D-063 | Wonder 69 hospital foundations donating | 501(c)(3) cannot donate | reframe to hospital PAC | table map |
| D-064 | Wonder 108 sanctioned-port calls | NOAA AIS is US waters only | none | table map |
| D-065 | Wonders 120, 121 the "gap" hunt | no gap; join through program links; check masked ZIP first | program-link join | table map |
| D-066 | Wonder 87 lobbying vs rules by week | LDA and Federal Register share no years | none | table map |
| D-067 | Wonder 44 Part D cost growth by drug | only DY22 by-drug file; growth untestable | Part D longitudinal (wish list) | table map |
| D-068 | Wonder 48 "by a quarter" | no quarter grain anywhere in prescribing | none | table map |
| D-069 | Wonder 49 reinstated doctors | LEIE is active exclusions only; REINDATE constant 00000000 | none | table map; ghost doctors |
| D-070 | Wonder 118 servicer change from complaints | circular, no servicer roster | none | table map |
| D-071 | Sanctioned-name matches into US files | 100% noise on eye check (2026-09-05) | IMO_NUMBER shared with UK sanctions | table map |

#### Hunches that died on the run

| id | what was tried | why it died | nearest live version, if any | sources |
|---|---|---|---|---|
| D-072 | Hunch 4 bribed opiate pipeline via OTP NPIs | OTP rows are organizations, 0 of 1,340 in Part D | DY2022 buprenorphine share x Open Payments 2022, OTP as county flag | matrix |
| D-073 | Hunch 7 ghost clinics via UDS site NPI | site NPI is the org; opt-out is people; FFS holds zero practitioners under FQHC IDs; later rescued by address bridge (58%) | HEALTH__FQHC_SITE_PEOPLE | matrix; docket combined |
| D-074 | Hunch 14 RHC harvesters | same missing org-to-doctor bridge | RHC ZIP RUCA vs enrollment address | matrix |
| D-075 | Hunch 16 diabetes mills | MDPP ∩ LEIE = 0 of 1,037 (0 of 307 distinct); park | none | matrix |
| D-076 | Hunch 26 storm arbitrage on NOAA_WEATHER_API | 287 alert rows, not storm history | storm events mart, tier 2 | matrix |
| D-077 | Hunch 143 clinical trial sponsors paying PIs | FED_CLINICALTRIALS was 500 rows, AACT not landed; full CT.gov landed 2026-09-07, NPI blank, name bridge needed | name bridge to NPPES | matrix; docket combined |
| D-078 | Hunch 144 immigration court outcomes by judge | FED_EOIR_CASE_DATA was one unparsed column; now 39 columns, still no judge or outcome; needs B_TblProceeding | EOIR column split (wish list) | matrix; docket combined |
| D-079 | Hunch 118 SBA lenders vs FDIC enforcement | FED_FDIC_ENFORCEMENT 14 rows; orders reloaded 2026-09-07 (10,838), SBA has no cert | charge-off rate vs failed banks | matrix; docket combined |
| D-080 | Hunch 124 officer pay via the 990 stub | FED_IRS_990 200 rows, e-file index has no amounts | done via XML parse, 526,374 rows | matrix; docket combined |
| D-081 | FEMA contract untimed all-agency figure | summed lifetime TOTAL_DOLLARS_OBLIGATED per action; $314M over 154 rows withdrawn | net obligated $22,066,026 | matrix |
| D-082 | #32 water violations after floods, general claim | gap is entirely OK+TX rule-220 national phase-in; other 873 counties 0.758 | none beyond the phase-in | expansion |
| D-083 | #33 sewage noncompliance after storms, pooled | 94% of permits are stormwater; Q+1 SNC 10.8% vs 12.9% | lives on 4,776 sewage plants | expansion |
| D-084 | #34 hazardous waste vs drug poisoning | r 0.007; every quintile rose alike; five disproof attempts failed | none | expansion |
| D-085 | #36 disaster counties and overdose | heavy-hit -1.07; null manufactured partly by RATE_M filter and peak-straddling endpoints | re-run without RATE_M filter | expansion |
| D-086 | #37 industry money jump moving Medicare behaviour | growers match the field: QPP 85.11 vs 84.95; jumps are buyouts, royalties, consulting | none | expansion |
| D-087 | #39 rural leg of opioid reps | nonmetro paid NPs 19.1% vs metro 39.1%; QPP combined flag flipped the sign | the prescribing leg stands | expansion |
| D-088 | #45 E-tags after storms | placebo +32.2% vs hit +33.8%; raw direction was right-censoring | none | expansion |
| D-089 | #46 triple owners as good actors | 65% nonprofit; within-class gap 0.03-0.41 not significant; Liberty Healthcare worse than comparison | none | expansion |
| D-090 | #48 sale-then-close within 24 months | 44 of 1,299 (3.4%) but 255 undated CHOWs; floor 3.4% to 15.0%; unproven, not dead | full POS with CHOW_DT (wish list) | expansion |
| D-091 | #50 post-disaster provider startups | per-pair DiD 1.14; LA boom predates its declaration; hurricane hospice 1.000 | none | expansion |
| D-092 | #51 HPSA designation pulling clinics | 0.90 was right-censoring; placebo band 0.82-1.12 swallows it; 272 counties dropped by inner join | none | expansion |
| D-093 | #52 jail vs violent death (Pearson) | r -0.09 / -0.03 driven by impossible jail rates; flips +0.14 / +0.11 trimmed; overdose +61% was unbalanced cohorts | jail quintiles and wages | expansion |
| D-094 | #53 penalty deserts by jail and minority share | flat across jail quintiles; minority gradient runs opposite; EPA_PENALTY_GAP already shows it; deserts are state primacy | state primacy angle | expansion |
| D-095 | #54 air violators and factory wages | gradient is permitted-source density (refineries, oil wells); manufacturing-only flat; per facility reverses | none | expansion |
| D-096 | #55 subsidized housing beside noncompliance | HUD units double-counted; partial r after ln(pop) 0.013/0.058; reverses in three of four bands; zero-HUD counties highest | none | expansion |
| D-097 | #56 quality bonus vs industry money (also docket v1 19, E56) | 10.2% vs 10.1%; gap smaller than tie-assignment noise; zero band is a hardship cohort; nothing there twice | none | expansion; docket v2 vs v1; tool box |
| D-098 | #58 state malpractice backdrop | shared QPP denominator induced the co-movement; MA rank 1 > 19; Maine's 3.4 is redaction | none | expansion |
| D-099 | #59 top-paid hospitals, low stars | corr -0.0111 on rated cohort; risk-adjusted decile selects unrated small hospitals; not academic centers | none | expansion |
| D-100 | #61 hazardous-waste hospitals and margins, as stated | 74% of zero group never inspected; inspected-only p=0.47; Virginia Hospital Center exemplar came from a loose match | inspected-only comparison | expansion |
| D-101 | #62 sprinkler flag contradiction (1,500) | flag is 99.58% Yes, zero lift; 1,436 of 1,500 closed before snapshot; 70% scope B-E | none | expansion |
| D-102 | #63 harm rising 2023-2025 with churn | +53.3% vs +14.1% was a truncated 2023 baseline; honest read: harm fell at stable homes, did not fall at churn homes | the honest read | expansion |
| D-103 | #64 material weakness grantees as fiscal years | money leg is ~6 months per year; 60% one Massachusetts Medicaid line; flagship Southwest Key clean before money | none | expansion |
| D-104 | #65 revoked nonprofits still funded | REFUTED: reinstatements erase it; $0 in dark window; $7.3M was an EIN typo | none | expansion |
| D-105 | #66 excluded entities taking HHS grants | 0 of 34,504 on a table holding 34% of days; near-duplicate of hunch 15's dead leg | none | expansion |
| D-106 | #67 jail counties as clinician deserts | county size; within bands 1.16x non-monotonic; NPPES gives same gradient; QPP adds nothing | none | expansion |
| D-107 | #70 VA pays one-star homes | 18.2% is below the 20.41% national one-star rate; 2.88 vs 2.89 stars | none | expansion |
| D-108 | #71 pharma dollars per head, strong version | explains under 1% of variance; tracks prescribers per head (0.84); CDC leg 8 years stale | none | expansion |
| D-109 | #72 HUD housing in repeat-disaster counties | half Puerto Rico; sign flips states-only; no dose-response; 74.7% wait sentinels | none | expansion |
| D-110 | #73 SAM adds clinicians LEIE misses | 179 SAM-only NPIs, 4 lunches; named lead was a different human | none | expansion |
| D-111 | #74 HHA/hospice ownership change via POS | 0 HHA and hospice CCNs in POS_OTHER; proxy reverses the story (changed-hands agencies rate higher) | HHA owners file landed 09-07 | expansion |
| D-112 | #75 PRF to nursing-home chains via USASpending | one award to UnitedHealthcare; TAGGS is nav text; recipient-level PRF not landed | PRF name match at 14% | expansion |
| D-113 | Hub A seed 7 FEMA dollars vs PHA capacity and NFIP | NOT run: NFIP has no FIPS and a '/'-joined county name; PHA half runnable in an hour (STATE2KX concatenated with CNTY2KX) | PHA half | expansion |
| D-114 | Hub C seed 2 as 2018-2025 chain trend | deficiency file covers 2,004 homes in 2019; only 2023 vs 2025 is fair | 2023 vs 2025 | expansion |
| D-115 | Hub C seed 8a last star before termination | 0 of 762 hospitals terminated 2019-2023 remain in Care Compare | reframed to last cost report | expansion |
| D-116 | Hub X seed 8 SAM registrations vs NPPES org names | not run; ran against HCRIS instead | HCRIS version | expansion |
| D-117 | Skeptic rerun with single-backslash \b | 633 > 217 matches, 66% loss, no error; 1,601 > 1,054 pairs | double the backslash | expansion |
| D-118 | First control run with NPI_DEACTIVATION_DATE is null | empty strings not NULLs; reported 0.00 clinicians per 10k everywhere | test for '' too | expansion |
| D-119 | Docket v1 lines 92, A34 House disbursements; 138 assistance; 142 CAMPD; A35 PTR index | raw tables with no mart stand-in in the inventory (LANDING not checked): FED_HOUSE_DISBURSEMENTS, FED_USASPENDING_ASSISTANCE_FULL, FED_EPA_CAMPD_EMISSIONS_DAILY, FED_HOUSE_FD_PTR_INDEX | build a mart or re-load | tool box; docket v2 vs v1 |
| D-120 | Docket v1 14 fake rural clinics; 16, 24 diabetes and ambulatory rosters | rosters only, nothing to measure | none | tool box; docket v2 vs v1 |
| D-121 | Docket v1 13 renaming after fire fines | duplicate of 30 | line 30 | docket v2 vs v1 |
| D-122 | Docket v1 128 failed banks and FHLB membership | one piece of the puzzle is a dead end; skip | none | tool box |
| D-123 | Docket v1 126 lender complaints before enforcement | marked skip, already ruled out, though no query was run | none | tool box |
| D-124 | Contract trends viz | truncated sample until re-pull; off-limits | re-pull | tool box |
| D-125 | 267 inventory tables not cited in any v2 idea | supporting cast 134; under 100 rows 31; catalog or lookup 26; timeline thin 20; duplicate of a sibling 18; sample shape only 16; backup copy 11; prior snapshot 11; also _RESTORE_20260907 backups 0-50 rows; 9 __PREV_ snapshots; TIMELINE _INDEX stubs; dataset catalogs (CDC_DATA_PORTAL, CMS_MAIN, FAOSTAT, DOT_BTS, NASA_OPEN_DATA); GUDID__STAGING, VA_SUICIDE_APPENDIX unparsed; API test samples (FEC_API, ENVIROFACTS, GRANTS_GOV, IRS_990, SEC_EDGAR, USASPENDING_API, HIFLD, USASPENDING_BULK, SUBAWARDS, HMDA, HMDA_LAR, OSF, NARA_AAD); EOIR one column; ITIS support; code lookups; RCRA_RCRA_* stripped duplicates; DIM lookups; LEAD_QUEUE, COHORT_QUEUE; FINANCE__FED_EPA_ICIS_FEC_* misfiled; Epstein link scrapes | appendix lists in docket v2 notes | tool box; docket v2 notes |

#### Lab joins and map techniques that died

| id | what was tried | why it died | nearest live version, if any | sources |
|---|---|---|---|---|
| D-126 | IRS auto-revocations x FAC x assistance | Tribes, transit agencies, housing authorities auto-revoke because they never file; $13.4B of nothing | none | lab |
| D-127 | Open Payments x Part D per-claim cost | survived the run; skeptic: drug mix not behaviour, and ProPublica did this join years ago | the F row stands with the caveat | lab |
| D-128 | SAM exclusions x USAspending paid-while-debarred | 22 firms found; UEI predates 2022 only via unvalidated backfill; mods on old awards are lawful | the F row stands with the caveat | lab |
| D-129 | SAM NPI x Part D 2024 | zero hits; unclear if CMS works or NPI column is empty-shaped; unchecked | check the column | lab |
| D-130 | Percolation on the connection map | measures the sampler: 0.1% of ~4.6M pairs ever measured; snap threshold is an artifact | none | lab map |
| D-131 | MATCH_PAIRS as an attraction or entity-edge measure | rows link TABLE_A to TABLE_B, not entity to entity | ENTITY_XREF | lab map |
| D-132 | Court citation network | FED_COURTLISTENER_CITATION_MAP holds 0 rows | none | lab map |
| D-133 | BLS QCEW as the clean correlation panel | only YEAR 2022; QUARTER is an ordinal; four buckets max | QCEW annual files (wish list) | lab map |
| D-134 | Copy RIPPLE_TS onto ENTITY_XREF / MATCH_PAIRS to clock the spine | one key value has many dated source rows; no single timestamp | none | lab map |
| D-135 | HRSA county/FIPS columns for Moran's I | all seven bad casts | use lat/lon | lab map |
| D-136 | HMDA_LAR / HMDA / HMDA_DC_ONLY as tract sources | stubs of 17,474 / 28,301 / 28,301 rows | HMDA_HISTORIC with CENSUS_TRACT_NUMBER | lab map |
| D-137 | Shape index's 558 origin-destination tables | loader bookkeeping columns, not flows | ~six real flow families | lab map |
| D-138 | Part D prescribers as a spectrogram | only _LOADED_AT, one value on all rows | ARCOS spectrogram | lab map |
| D-139 | Spectrogram for ripples, Voronoi | LAB flagged both as possible duds; MAP overturned Voronoi (bank branches own ground) and confirmed spectrogram on ARCOS | both live | lab; lab map |

#### Investigations: wrong turns on the way

| id | what was tried | why it died | nearest live version, if any | sources |
|---|---|---|---|---|
| D-140 | 243 excluded providers "still in prescriber file" | 242 excluded after the file year; arrow backwards | date-tested join | pitch deck |
| D-141 | Naive USASpending row count | 174x inflation from modifications | count awards, not actions | pitch deck |
| D-142 | Ghost hunt first pass, 554 | vintage; 552 excluded after or during 2022 | two survivors, Miranda and Aswad | ghost doctors |
| D-143 | Naive 2022 pharma-paid join, 532 NPIs | not date-tested; wrong by 4x | 137 NPIs | pharma paid |
| D-144 | Frank "only physician at Haskell" | 35.5% of homes list one; modal case | affiliation base rate row | frank |
| D-145 | Part B "2022-era" | registry says DY2023 | Part B DY2024 per expansion | frank |
| D-146 | "No %ANTIPSYCH% column" | ANTPSYCT_GE65_* exists; CMS devowels | ANTPSYCT columns | frank |
| D-147 | "Only DY2022 Part D landed" | FED_CMS_PART_D_PRESCRIBERS is DY2024 | DY2024 file | frank |
| D-148 | 26-brand antipsychotic list | missed 7.9% of national claims; 5.75% > 6.06% | full class list | frank |
| D-149 | "20x the peer median" | suppression depresses the median; inflated by an unknown amount | percentile rank | frank |
| D-150 | 492 distinct drugs | row count; 486 distinct brands | 486 | frank |
| D-151 | 2023 payments vs Part D cost column | DY2022 figures repeated | year-aligned compare | frank |
| D-152 | "Federal contractors mostly comply" from the EPA view | 57 rows from 3.3M facilities x 93.2M contracts is a join finding | say it is about the join | findings views |
| D-153 | SELECT * FROM LIBRARY_META."CONNECT" | it is a schema, not a table | CONNECT_EDGES | graph hunt |
| D-154 | Heaviest EIN by table count | SEC quarterly and OSHA yearly splits; measures file splitting | collapse to source systems | graph hunt |
| D-155 | Collapsed-family ranking | Colorado portal ten tables; all top 15 are Denver nonprofits | none | graph hunt |
| D-156 | Contracts-to-donations chain on EIN | EIN reaches none of those tables; false clean negative | UEI and FEC ids | graph hunt |
| D-157 | HAVING COUNT(DISTINCT KEY_TYPE) > 1 on ENTITY_INDEX | zero rows; one key type per ENTITY_ID | ENTITY_XREF | graph bridges |
| D-158 | Cross-agency filter by SPLIT_PART | three same-registry pairs slipped through | hand list | graph bridges |
| D-159 | Find the corporate owner of the ghost NPIs | both sole practitioners, ORG_NAME null | none | ghost owner |
| D-160 | Miranda convicted 2013 of black-market drug fraud | investigator's claim; not in warehouse | none | ghost owner |
| D-161 | Find the Part B payee TIN | no CMS public file carries one; NPPES EIN 100% empty | none | ghost partb |
| D-162 | Name the six DME suppliers | referrer file has no supplier link; supplier file has no referrer | none | ghost partb |
| D-163 | Molina "six-figure cheque" | bad-debt write-off, no money moved | write-off row | molina |
| D-164 | Frank DME 563 services/patient as extreme | 18,213 to 72,586 referrers higher; band 81-92 | percentile band | frank dme |
| D-165 | "Earlier reports disagree on Frank's DME row" | those figures were Miranda's | none | frank dme |
| D-166 | Beneficiary additivity 18.7% | wrong denominator; 60.5% | 60.5% | frank dme |
| D-167 | "Panel sicker than volume is high" | three denominators; reversed on common cohort | common-cohort ordering | frank dme |
| D-168 | 0.98 spend ratio as counterweight | per-episode, blind to episode count | none | frank hospice |
| D-169 | Six panel doctors "absent from Part B" | present, just under the 11-bene floor | none | frank hospice |
| D-170 | Three-facility shape as rare fraud pattern | 7,127 physicians have it | none | frank hospice |
| D-171 | Exclusion rate among shape cohort | 15 of 940,350; LEIE cannot support a rate | none | frank hospice |
| D-172 | LEIE name search on org names | three false hits, single-word collision | CCN match | frank hospice |
| D-173 | Matching DME referrer to supplier on state+HCPCS+volume | inference dressed as evidence; not done | none | frank dme |
| D-174 | Reading Room review 2026-07-21 | REVIEW schema, DECISIONS table, LEAD_QUEUE mart, REVIEW PAT all missing | LEAD_QUEUE exists now, 17,306 rows | hour dossier |
