# Idea Book extract — Lens & Frontier (LF)

Extracted 2026-09-13. Every row cites file § section. Nothing queried; nothing invented.

## Row counts

| section | rows |
|---|---|
| IDEAS | 98 |
| METHODS | 44 |
| RULES | 52 |
| FINDINGS | 131 |
| DEAD ENDS | 46 |
| LOOSE | 214 |

## Files read, in full

| file | lines |
|---|---|
| docs/RIPPLES.md | 208 |
| outputs/ripple_frontier_MASTER_LIST.md | 158 |
| docs/ripple_pitch_deck.md | 382 |
| reports/news_corroboration_map_2026-09-05.md | 72 |
| reports/frank_investigation_2026-09-05.md | 518 |
| reports/findings_views_evaluated_2026-09-05.md | 240 |
| reports/graph_hunt_ein_2026-09-05.md | 281 |
| reports/graph_bridges_2026-09-05.md | 272 |
| reports/ghost_doctors_and_audit_bridge_2026-09-05.md | 212 |
| reports/ghost_npi_ownership_2026-09-05.md | 244 |
| reports/ghost_npi_partb_money_2026-09-05.md | 227 |
| reports/pharma_paid_excluded_2026-09-05.md | 231 |
| reports/molina_debt_forgiveness_2026-09-05.md | 236 |
| reports/takedown_vs_warehouse_2026-09-05.md | 65 |
| reports/frank_dme_suppliers_2026-09-05.md | 319 |
| reports/frank_hospice_homehealth_2026-09-05.md | 380 |
| reports/warehouse_capabilities_2026-08-18.md | 140 |
| outputs/HOUR_DOSSIER.md | 297 |
| THE_SCRIPT.md | 67 |

Note: HOUR_DOSSIER names only pattern #1 of "four systemic patterns" and points to `outputs/PATTERN_MAP_2026-07-21.md`, which does not exist in the repo. The other three names are not recoverable from the assigned files.

---

## IDEAS

| id | idea, one plain line | subject | tables or hubs named | join key | picture | status or result | source file § section |
|---|---|---|---|---|---|---|---|
| LF-001 | When a square gets worse, what happened to its neighbors? One dumb rule, every tick | any station | entity spine, clock | owner, address, officer | rule fires across grid | not built — piece 5 frontier | RIPPLES.md § The worked example |
| LF-002 | Nursing home violations 3→9; 7 of 11 same-owner siblings spike; timed to owner buying 13th home; nearby other-owner homes flat | nursing homes | nursing deficiencies, ownership | owner ID | siblings spike together | illustrative, not run | RIPPLES.md § The worked example |
| LF-003 | "These 12 homes are secretly one chain" — wire finding shape | chains | ownership, address, officer | shared hard ID | cluster on one owner | open | RIPPLES.md § Ripple 2 NEIGHBORS |
| LF-004 | "40 unrelated companies running the same playbook" — violations spike ~18 months post-acquisition, staffing goes smooth | resemblance | uniform readings | none (behavior space) | same curve, no join | open; resemblance = queue only | RIPPLES.md § Ripple 2 NEIGHBORS |
| LF-005 | A stream that consistently leads another is a free crystal ball | flow | ~950 trendable columns | shared clock | offset rhythms | open, Box 4 | RIPPLES.md § Ripple 3 FLOW |
| LF-006 | Dead air: complaints spiked, enforcement never followed — the broken hand-off is itself a finding | flow | complaints → violations → closures | facility ID | wave breaks | open, Box 5 | RIPPLES.md § Ripple 3 FLOW |
| LF-007 | Coverage overlay: a map of "where can this method even see" | neighbor web | 14 solid connection families | — | lit vs dark graph | open | RIPPLES.md § landmine 3 |
| LF-008 | Forecast desk: instruments reading automatically every season | all | — | — | always-on layer | not built | RIPPLES.md § The actions |
| LF-009 | Box 1: is each stream rising / falling / flat / seasonal — one word per stream | flow | ~950 columns | clock | one word each | startable, clock shipped 2026-08 | RIPPLES.md § Ripple 3 FLOW |
| LF-010 | Box 2: each stream's heartbeat — drip vs burst, annual dump vs daily trickle | flow | same | clock | cadence | open | RIPPLES.md § Ripple 3 FLOW |
| LF-011 | Box 3: do two streams co-move, no lead-lag yet | flow | same | clock | pairs | open | RIPPLES.md § Ripple 3 FLOW |
| LF-012 | FARS crashes joined to recalls plus VIN body-type | vehicle deaths | FARS, NHTSA recalls | VIN | crash × recall | wish | ripple_frontier_MASTER_LIST.md § Round 2 |
| LF-013 | Public pension funded-ratios vs local tax abatements | pensions | Public Plans DB, abatement filings | locality | funded gap vs giveaways | wish | ripple_frontier_MASTER_LIST.md § Round 5 |
| LF-014 | New York IDA subsidy deals: jobs promised vs delivered | subsidies | NY IDA | project | promise vs count | wish | ripple_frontier_MASTER_LIST.md § Round 5 |
| LF-015 | EPA NPDES discharge vs permit limit | water | NPDES DMR | permit ID | exceedance | wish | ripple_frontier_MASTER_LIST.md § Round 5 |
| LF-016 | Harvard 2025 data.gov snapshot as a purged-dataset diff | data itself | data.gov snapshot | dataset ID | what vanished | wish | ripple_frontier_MASTER_LIST.md § Round 5 |
| LF-017 | NYC HPD registrations: LLC → human owner | landlords | HPD registrations, Class-C violations | building ID | LLC unmask | wish | ripple_frontier_MASTER_LIST.md § Round 5 |
| LF-018 | PROMESA + FEMA/CDBG-DR obligated vs disbursed for territories | disaster money | FEMA, CDBG-DR | grant | promised vs paid | wish | ripple_frontier_MASTER_LIST.md § Round 4 |
| LF-019 | School-district cut of corporate tax breaks | schools | GASB 77 filings | district | lost revenue | wish | ripple_frontier_MASTER_LIST.md § Round 5 |
| LF-020 | Lown Fair Share + 990 Schedule H: hospital charity vs tax break | hospitals | Lown, 990 Sch H | EIN | fair-share deficit | wish | ripple_frontier_MASTER_LIST.md § Round 4 |
| LF-021 | FCC broadcast ownership station → parent | media | FCC ownership | facility ID | station chains | wish | ripple_frontier_MASTER_LIST.md § Round 2 |
| LF-022 | SEC Exhibit 21 subsidiary trees | corporate | EDGAR Ex-21 | CIK | parent → subs | wish | ripple_frontier_MASTER_LIST.md § Round 1 |
| LF-023 | USASpending sub-awards + SAM.gov parent hierarchy | contracts | USASpending, SAM | UEI | prime → sub | wish | ripple_frontier_MASTER_LIST.md § Round 1 |
| LF-024 | Prison-phone rates + site commissions (PPI map) | prisons | FCC filings | facility | who profits | wish | ripple_frontier_MASTER_LIST.md § Round 4 |
| LF-025 | SSA ALJ dispositions by judge; BVA grant rates per VLJ | judges | SSA, BVA | judge | grant-rate spread | wish | ripple_frontier_MASTER_LIST.md § Round 4 |
| LF-026 | Put the banned-doctor list next to the pharma-payment list | health | LEIE, Open Payments | NPI | on both lists | found: 773 leads (banned_but_paid) | ripple_pitch_deck.md § dumb question; § What it's found |
| LF-027 | Debarred company still holding an active federal contract | contracts | SAM exclusions, USASpending | UEI | both lists | found: 2 leads (debarred_but_funded) | ripple_pitch_deck.md § The idea; § What it's found |
| LF-028 | Sanctioned ship whose transponder still pings off the US coast | maritime | OFAC, NOAA AIS | IMO | both lists | found: 12 v2 + 4 v1 leads | ripple_pitch_deck.md § The idea; § What it's found |
| LF-029 | Excluded provider still in the Part D prescriber file | health | LEIE, Part D | NPI | both lists | found: 236 leads; vintage trap applies | ripple_pitch_deck.md § What it's found; ghost_doctors § 2 |
| LF-030 | Excluded provider still affiliated with CMS facilities | health | LEIE, facility affiliation | NPI | both lists | found: 11 leads; source table since dropped | ripple_pitch_deck.md § What it's found; HOUR_DOSSIER § 3 |
| LF-031 | SEC filer that is also in the IRS BMF | corporate | SEC, IRS BMF | EIN | both lists | found: 3 leads | ripple_pitch_deck.md § What it's found |
| LF-032 | OSHA establishment at 2x its NAICS-and-size peer injury rate on 5+ cases | workplaces | OSHA ITA 300A | establishment | peer outlier | found: 16,215 leads | ripple_pitch_deck.md § What it's found |
| LF-033 | Top-10% opioid prescribers within specialty who take opioid-maker money, addiction-treatment excluded | health | Part D, Open Payments | NPI | pay vs rx rate | found: 6,020 doctors; 27 high tier | ripple_pitch_deck.md § Opioid prescribers |
| LF-034 | Hospitals at closure risk: negative margin AND Medicaid-dependent AND shortage/rural | hospitals | HCRIS, HRSA shortage | CCN | risk tiers | found: 4,435; 1,214 critical | ripple_pitch_deck.md § Hospitals at closure risk |
| LF-035 | PACs funding 10+ members of both parties — access, not ideology | politics | FEC | committee ID | both-sides flag | found: 2,680 PACs; 1,359 both | ripple_pitch_deck.md § PACs funding both parties |
| LF-036 | Members of Congress: money vs output | politics | FEC, votes | bioguide | dollars vs work | found: 635 rows | ripple_pitch_deck.md § findings catalog |
| LF-037 | Revoked nonprofits still flagged tax-deductible | charities | IRS revocations, Pub78 | EIN | both lists | found: 22,512 | ripple_pitch_deck.md § findings catalog |
| LF-038 | Excluded providers paid after exclusion, in shortage areas | health | LEIE, Open Payments, HRSA | NPI | subset | found: 287 | ripple_pitch_deck.md § findings catalog |
| LF-039 | Federal contractors with EPA violations | contracts | USASpending, ECHO | PARENT_UEI | both lists | found: 21 (deck), 57 rows in view; underpowered | ripple_pitch_deck.md § catalog; findings_views § 2 |
| LF-040 | Follow one company EPA → contracts → donations | corporate | ECHO, USASpending, FEC | needs crosswalks | chain | open: crosswalks not built | ripple_pitch_deck.md § What I don't know |
| LF-041 | Does the warehouse rediscover stories the press already broke? | all | 24 stories | various | echo / retrace / stumble | run: 17 hits, 1 partial, 1 weak, 5 misses | news_corroboration_map § scorecard |
| LF-042 | Were DOJ takedown defendants visible as outliers before charges? | health | NPPES, Part D 2024 | name → NPI | percentile in type | found: 4 of 5 at 91st–99.4th | takedown_vs_warehouse § What it means; news map row 24 |
| LF-043 | The 66 / 180 / 448 peers sitting where the defendants sit are the lead lists | health | Part D 2024 | NPI | at-or-above bars | open; most legit (hospice, pain, rural) | takedown_vs_warehouse § Step 5 |
| LF-044 | Gala lab-billing case needs Part B or CLIA tables, not Part D | health | Part B, CLIA | NPI | — | open | takedown_vs_warehouse § Caveats |
| LF-045 | Frank: the 23 DME suppliers and 36,017 services | Frank | DME by referrer | NPI | money trail | probed: deflates, 81–92nd pct | frank_investigation § Not checked 1; frank_dme § close |
| LF-046 | Frank: Neighborhood Hospice and Universal Rehab — hospice fraud shape | Frank | hospice, home health | CCN | long stays | probed: recert ratio 6.48, 98.97th pct; hospice untestable | frank_investigation § Not checked 2; frank_hospice |
| LF-047 | Haskell's own antipsychotic percentage | Frank | NURSINGHOME411, CMS nursing | CCN | facility measure | not checked: no facility-level measure landed | frank_investigation § Not checked 3 |
| LF-048 | What is Previse Medical and how does it tie to Frank | Frank | Open Payments 2024 | name only | — | not checked: no identifier | frank_investigation § Not checked 4 |
| LF-049 | DY2023 Part D for Frank | Frank | Part D | NPI | middle year | not checked: not landed | frank_investigation § Not checked 5 |
| LF-050 | Do the other 28 Skye write-off recipients share the nursing-home practice shape | Skye | Open Payments 2024, affiliation | NPI | shape match | not checked | frank_investigation § Not checked 6; molina § Not checked 3 |
| LF-051 | Oklahoma medical board or NPDB entry for Frank | Frank | NPDB | — | — | not checked: NPDB de-identified | frank_investigation § Not checked 7 |
| LF-052 | Pin the true vintage of the Part B tables | Part B | Part B by provider | — | — | open: registry DY2023, COVID codes prove 2021+ only | frank_investigation § Not checked 8; ghost_partb § vintage |
| LF-053 | Add FED_CMS_OPEN_PAYMENTS_2022 to the paid-after-exclusion view | health | Open Payments 2022 | NPI | fill 2022 hole | open: one-line fix, adds 137 provider-years | findings_views § 1 |
| LF-054 | MOLINA, HECTOR — $114,040 single payment 2024 | health | Open Payments 2024 | NPI | — | probed: debt forgiveness, Del Sol Medical | findings_views § 1; molina § record |
| LF-055 | Read the EPA view definition: UEI recall or deliberate confidence filter? | contracts | FEDERAL_CONTRACTOR_EPA_VIOLATOR | — | — | not checked | findings_views § Not checked 4 |
| LF-056 | Count the other 10 FINDINGS views | findings | LIBRARY_MARTS.FINDINGS | — | — | not checked: 3 of 13 counted | findings_views § Not checked 5 |
| LF-057 | Rank entities by source system, dropping portals | graph | ENTITY_INDEX | ENTITY_ID | cross-agency breadth | open: one group-by | graph_hunt_ein § honest version |
| LF-058 | Rank entities by distinct key types per ENTITY_ID | graph | ENTITY_INDEX | ENTITY_ID | multi-identity | dead: every ENTITY_ID has one key type | graph_hunt_ein § honest version; graph_bridges § Q1 |
| LF-059 | Rank entities by distinct domains after re-bucketing | graph | ENTITY_INDEX | — | cross-subject | open: needs domain fix first | graph_hunt_ein § honest version |
| LF-060 | Hunt NPPES ↔ LEIE first: 8,660 excluded resolve at 100%, then Part D and Open Payments on NPI | health | NPPES, LEIE, Part D, Open Payments | NPI | fan out from exclusion | found; became ghost-doctor hunts | graph_bridges § four strongest |
| LF-061 | FRS_ID ↔ LEI: EPA facility straight to global corporate ownership | environment | XC_EPA_CORPORATE_CROSSWALK, GLEIF | LEI | physical → owner | open: 73,948 rows, fanout 1 | graph_bridges § one bridge |
| LF-062 | Build EIN ↔ UEI and NPI ↔ DEA bridges — obvious, both missing | graph | — | — | — | open; DEA on 149,244 entities connects to nothing | graph_bridges § top key combinations |
| LF-063 | Are the Colorado portal tables ten extracts or one file ten times | portals | PORTAL_SOC_COLORADO_INFORMA_* | — | — | not checked | graph_hunt_ein § Not checked 2 |
| LF-064 | Do six CCN↔NPI same-row enrollment tables agree with each other | health | six enrollment tables | CCN, NPI | consistency | not checked | graph_bridges § Not checked 4 |
| LF-065 | BRIDGE_ENTITIES SOURCE_COUNT vs SOURCES array length | graph | BRIDGE_ENTITIES | — | — | not checked: 14 vs 3 listed | graph_bridges § BRIDGE_ENTITIES |
| LF-066 | 2,271 EINs with two UEIs: re-registration or parent-subsidiary? | nonprofits | FAC single audit | EIN | fanout 2 | not checked | ghost_doctors § 1; § Not checked 5 |
| LF-067 | Are the two ghost NPIs still active in NPPES, under which org | health | NPPES, enrollment | NPI | — | probed: both solo, ORG_NAME null | ghost_doctors § Not checked 1; ghost_ownership |
| LF-068 | The 30 excluded-during-2022 cases need a file with service dates | health | Part D | NPI | month-level | not checked | ghost_doctors § Not checked 3 |
| LF-069 | MULTIPLE_NPI_FLAG on the ghost NPIs | health | FFS enrollment | NPI | — | probed: Miranda N | ghost_doctors § Not checked 4; ghost_ownership |
| LF-070 | Ghost Part B: procedures, imaging, surgery under excluded NPIs | health | Part B by provider | NPI | — | probed: Miranda $1,229,994.33, no year | ghost_doctors § floor 4; ghost_partb |
| LF-071 | DME by referrer and FISS attending for Miranda | health | DME by referrer, FISS | NPI | money | probed: DME $46,385.19; FISS is names only | ghost_ownership § Not checked 1–2; ghost_partb |
| LF-072 | Do Miranda's four hospitals name an owner seen elsewhere | health | HOSPITAL_ENROLLMENTS | CCN | owner | not checked | ghost_ownership § Not checked 5 |
| LF-073 | Do Doctors Hospital of Laredo or Fort Duncan appear in USASpending / SAM | health × contracts | USASpending, SAM | UEI | — | not checked | ghost_partb § Not checked 4 |
| LF-074 | Part B by provider-and-service for Miranda: name the drugs behind $1.10M | health | ..._BY_PROVIDER_AND_SERVICE | NPI, HCPCS | — | not checked | ghost_partb § Not checked 2 |
| LF-075 | Aswad in a state medical board or NPDB table | health | NPDB | — | — | not checked | ghost_ownership § Not checked 6 |
| LF-076 | Run the pharma-paid-excluded join on 2023 and 2024 Open Payments | health | Open Payments 2023, 2024 | NPI | triple the window | partly done via view (287, 2023–24) | pharma_paid_excluded § Not checked 1; findings_views |
| LF-077 | Asfora: Part B / Part D, Medtronic devices implanted on his order after 2021 | health | Part B, Part D | NPI | — | not checked | pharma_paid_excluded § Not checked 2 |
| LF-078 | Name-match the 75,001 NPI-less exclusions, multi-word only | health | LEIE, Open Payments | name | — | not checked; single-word trap | pharma_paid_excluded § Not checked 3 |
| LF-079 | Do the 141 manufacturers overlap federal contractors | health × contracts | Open Payments, USASpending | UEI | — | not checked | pharma_paid_excluded § Not checked 4 |
| LF-080 | The five other excluded NPIs Medtronic paid | health | Open Payments 2022 | NPI | — | not checked | pharma_paid_excluded § Not checked 5 |
| LF-081 | Skye Orthobiologics: $7.2M written off across 30 wound-care providers — collapsed channel or consignment? | Skye | Open Payments 2024 | payer ID | write-off cluster | found; cause not answerable | molina § company is the real lead |
| LF-082 | Del Sol Medical vs Del Sol Medical Center hospital | Skye | — | name only | — | not checked | molina § Not checked 1 |
| LF-083 | Frank's $3.08M write-off beside his $10.7M Part D | Frank | Open Payments 2024, Part D | NPI | side by side | not checked, different years | molina § Not checked 2 |
| LF-084 | Skye in SAM, USAspending, or FDA tissue establishments | Skye | SAM, USASpending, FDA | — | — | not checked | molina § Not checked 4 |
| LF-085 | Molina's three addresses 600 miles apart | Molina | LEIE, NPPES, Open Payments | NPI | — | not checked | molina § Not checked 5 |
| LF-086 | Land the CMS hospice utilization file — live discharge rate | hospice | not landed | CCN | hospice fraud measure | open | frank_hospice § Where to go next 1 |
| LF-087 | Land CMS all-owners files for home health and hospice | ownership | not landed | CCN | who owns | open | frank_hospice § Where to go next 2 |
| LF-088 | Resolve Frank's absence from PECOS: vintage or partial load | Frank | PECOS | NPI | — | open | frank_hospice § Where to go next 3 |
| LF-089 | Is it the agency or the man — run the same measure on the whole panel | Frank | Part B service file | NPI | panel vs one | run: Frank 6.48, next 4.10; OK median 1.79 | frank_hospice § agency or the man |
| LF-090 | Look up anyone everywhere at once on hard IDs | all | entity spine | hard IDs | one query | capability | warehouse_capabilities § 1 |
| LF-091 | Follow the money: both ends of most flows, who funds whom, what happened after | money | FEC, USASpending, Open Payments, LDA, PPP, SOD | various | directional | capability | warehouse_capabilities § 2 |
| LF-092 | Attach harm to the actor: incident → operator's pattern | harm | mines, water, nursing homes, detention | facility/operator ID | joined at load | capability | warehouse_capabilities § 3 |
| LF-093 | Census not search: "most violations per inspection", "enforcement stopped while violations continued", across every regulated universe | all | shared grammar | — | same ruler | capability | warehouse_capabilities § 4 |
| LF-094 | Screen one name across every watch-list at once | diligence | sanctions, exclusions, revocations, failed banks, offshore leaks, ransomware, FFL | name or ID | sweep | capability | warehouse_capabilities § 5 |
| LF-095 | Before/after around enforcement actions; when did the pattern start | time | 349 dated tables | clock | trend | capability | warehouse_capabilities § 6 |
| LF-096 | Staged: judge dossiers on one hard ID over 72M dockets; charity money map; water enforcement chains; detention by operator; federal-ID Rosetta stone | staged | judges, IRS BMF, NPDES, ICE, grants | various | behind one switch | built, not switched on | warehouse_capabilities § built and about to switch on |
| LF-097 | Pattern #1: industry payments to banned providers — the top-10 review is its receipt check | health | LEIE, Open Payments | NPI | — | 1,030 pending leads 2026-07-21 | HOUR_DOSSIER § Altitude note; § 3 |
| LF-098 | Politics money-to-votes on hard IDs, not names | politics | FEC, votes | scoped build | — | open | warehouse_capabilities § Honest limits |

---

## METHODS

| id | name | what it is, plain | when to use it | source |
|---|---|---|---|---|
| LF-M001 | Weather lens | Ripple runs stations, takes the same readings everywhere, issues warnings a human confirms | all internal thinking; never public copy or renames | RIPPLES.md § GLOSSARY |
| LF-M002 | Conditions | What is everything, right now (Ripple 1 STATE) | first question on any warehouse ask | RIPPLES.md § three lenses |
| LF-M003 | Systems | What's connected, what moves as one thing (Ripple 2 NEIGHBORS) | second question | RIPPLES.md § three lenses |
| LF-M004 | Patterns | What's moving, what leads what, where it stalls (Ripple 3 FLOW) | third question | RIPPLES.md § three lenses |
| LF-M005 | Observation | One run of a question across everything | any sweep | RIPPLES.md § The actions |
| LF-M006 | Instrument | A dumb question mounted once, measuring everything automatically | building rules | RIPPLES.md § five pieces |
| LF-M007 | Game of Life bet | Simple pieces, honestly measured, allowed to touch; patterns draw themselves | design of every piece | RIPPLES.md § core idea |
| LF-M008 | Every bite is the same bite | Uniform measurement makes cells comparable; sameness compounds | building readings | RIPPLES.md § core idea |
| LF-M009 | Touching by wire | Follow the joins: same owner ID, address, officer. Court-ready | proving connection | RIPPLES.md § Ripple 2 |
| LF-M010 | Touching by resemblance | Same behavioral signature, zero shared keys | finding suspects | RIPPLES.md § Ripple 2 |
| LF-M011 | The loop | Resemblance finds suspects, wires confirm, survives both = finding | every pattern claim | RIPPLES.md § Ripple 2 |
| LF-M012 | Flow ladder | Box 0 staleness, 1 direction, 2 heartbeat, 3 co-move, 4 leads, 5 wave breaks; breadth-first | any time-series claim | RIPPLES.md § Ripple 3 |
| LF-M013 | Lens not checklist | Ask: which Ripple, simplest cell version, who are neighbors, what over ticks | every warehouse question | RIPPLES.md § How sessions use this |
| LF-M014 | Start simple, breadth-first | Never skip to the fancy rule | new lenses | RIPPLES.md § How sessions use this |
| LF-M015 | Echo grade | Story says X, table shows X; proves the file landed and did not rot | corroboration | news_corroboration_map § Three grades |
| LF-M016 | Retrace grade | Start from the story's first clue, joins reach the end; proves the joins | corroboration | news_corroboration_map § Three grades |
| LF-M017 | Stumble grade | One dumb query over the table, story pops in top 20; proves the warehouse can find | corroboration | news_corroboration_map § Three grades |
| LF-M018 | List A and List B | Same hard ID on a flag list and an activity list at the same time | intersection detectors | ripple_pitch_deck.md § The idea; HOUR_DOSSIER § 3 |
| LF-M019 | Statistical sweep vs intersection rule | Peer-cohort outlier scan returns thousands; ID intersections return few by construction | reading lead counts | ripple_pitch_deck.md § What it's found |
| LF-M020 | Who gets hurt | Every finding names a human on the other end or it's trivia | registering findings | ripple_pitch_deck.md § findings catalog |
| LF-M021 | Roll transactions to award | USASpending rows are modifications; naive count inflates 174x | contract counts | ripple_pitch_deck.md § Problem 3 |
| LF-M022 | Timeline is the story | Order dated events forward across datasets; the sequence carries the case | investigations | frank_investigation § Headline; § Step 5 |
| LF-M023 | Peer test twice | Two years, two definitions, two peer sets; survives both or it's an artifact | outlier claims | frank_investigation § Step 3 |
| LF-M024 | Lead with the percentile | Suppression depresses the median; the multiple inflates, the rank does not | CMS suppressed files | frank_investigation § Step 3 |
| LF-M025 | Base rate before bold | Check how common the "damning" shape is across the same table | any single-row claim | frank_investigation § Step 4; frank_hospice § practice shape |
| LF-M026 | Show the whole record | Present all rows, name what's omitted and why | citation and drug lists | frank_investigation § corrections 6–7 |
| LF-M027 | Supported / not shown table | Close every report with statement-by-statement support | every report | frank_investigation § What the data supports |
| LF-M028 | Skeptic corrections kept in view | Corrections logged, not folded in silently | after skeptic pass | frank_investigation § Corrections; frank_dme |
| LF-M029 | Date-test the join | EXCLDATE < DATE_OF_PAYMENT, or the arrow reads backwards | any flag-list × activity join | pharma_paid_excluded § method |
| LF-M030 | Split the headline number | One royalty vs 582 lunches: two stories in one total | any sum | pharma_paid_excluded § number breaks in two |
| LF-M031 | Dollars vs breadth rankings | Rank payers by total and by distinct recipients; they differ | payer analysis | pharma_paid_excluded § Top 10 |
| LF-M032 | Collapse file-split suffixes | Merge year/quarter tables into source systems before ranking reach | graph counts | graph_hunt_ein § Artifact 1 |
| LF-M033 | Read match rate, not matched count | Share of the smaller side that landed separates walkable bridges | using CONNECT_EDGES | graph_bridges § Read the match rate |
| LF-M034 | Identity vs affiliation | asserted_same_row fanout 1 = identity; asserted_affiliation = two things touching | ENTITY_XREF | graph_bridges § two relations |
| LF-M035 | Validity by format | EIN nine digits, UEI twelve alphanumerics; not by null | key coverage | ghost_doctors § 1 |
| LF-M036 | Column scan for the missing thing | Scan every table's columns for %PAYEE%, %TIN%, %EIN% before saying it's hidden | absence claims | ghost_partb § warehouse-wide check |
| LF-M037 | Absence vs zero | Suppressed under 11 is blank, not zero | CMS files | frank_hospice § hospice produced nothing |
| LF-M038 | Common cohort | Rank all measures on the rows carrying all of them | comparing percentiles | frank_dme § reversal |
| LF-M039 | Sign of the residual | Total below sum = dedup; money never dedups, so excess = masking | non-additive columns | frank_dme § two mechanisms |
| LF-M040 | Bound the percentile | Count hidden rows that could clear the bar; report the band | censored peer sets | frank_dme § 91.3rd is a band |
| LF-M041 | Walk the chain | What was checked, what a hit means, what a miss means | every finding | frank_hospice § Walking the chain |
| LF-M042 | Geographic baseline | State median before national when practice norms vary | ratio outliers | frank_hospice § agency or the man |
| LF-M043 | Judge a lead in order | Names agree? Timeline says while banned? Caveat box? Money size? LEIE_ROW_MISSING → check OIG | review queue | HOUR_DOSSIER § 7 |
| LF-M044 | Priority score is arithmetic | Tier weight + timeline weight + detector weight + tiebreak | ranking leads | HOUR_DOSSIER § 5 |

---

## RULES

| id | rule, plain | why | source |
|---|---|---|---|
| LF-R001 | Weather words are internal only; no public copy, no renames | real names stay stable | RIPPLES.md § GLOSSARY |
| LF-R002 | "Lead" is retired in the timing sense; queue sense prefers "warning" | one word one meaning | RIPPLES.md § outputs |
| LF-R003 | Resemblance alone is never a finding, only a queue | luck pairs by the thousand | RIPPLES.md § Ripple 2; landmine 2 |
| LF-R004 | Box 0 staleness per stream before any lead-lag claim | reporting lag impersonates a lead | RIPPLES.md § landmine 1 |
| LF-R005 | Raw lags look like they shrink near the present; wait out the tail | time censoring | RIPPLES.md § landmine 1 |
| LF-R006 | Boring-random-world null check is non-negotiable | false-positive firehose | RIPPLES.md § landmine 2 |
| LF-R007 | Never mistake well-lit for clean or dark for fine | neighbor web has holes | RIPPLES.md § landmine 3 |
| LF-R008 | A pattern is not a mechanism; auto-publish stays blocked | intent is a human story | RIPPLES.md § landmine 4 |
| LF-R009 | Instruments output confounds as readings, never silently control them away | false readings | RIPPLES.md § traps |
| LF-R010 | Subtract the climate (fiscal calendar, macro tide) before a blip counts | shared rhythm | RIPPLES.md § traps |
| LF-R011 | Normalize every key type before matching (NPI padding, IMO prefix, EIN hyphens) | same ID, different spellings | ripple_pitch_deck.md § Problem 2 |
| LF-R012 | Check dates before claiming "still X after Y" | 242 of 243 excluded after the file year | ripple_pitch_deck.md § Problem 3 |
| LF-R013 | Count hand-written SQL, not dbt compiled copies | 20,000 compiled files are not work | ripple_pitch_deck.md § What I built |
| LF-R014 | Use FILEDATE not TAPEYEAR in FJC IDB | TAPEYEAR lags a year | news_corroboration_map row 4 |
| LF-R015 | Name-check PWSIDs before citing | skeptic caught unchecked IDs | news_corroboration_map § Skeptic pass |
| LF-R016 | A landing swap does not rebuild the mart; run dbt | mart sat at 19.1M after 45M landed | news_corroboration_map § Mart rebuild |
| LF-R017 | Loader refuses --family all without denials; asks before first-lien swap | HMDA family trap | news_corroboration_map § Skeptic second pass |
| LF-R018 | FED_EOIR_CASE_DATA is one tab-separated column; unparsed | broken load | news_corroboration_map § Broken-load traps |
| LF-R019 | FED_NHTSA_COMPLAINTS is headerless C1..C54; C8 date YYYYMMDD; 110k blank dates | broken load | news_corroboration_map § Broken-load traps |
| LF-R020 | FED_MSHA_VIOLATIONS values carry literal quotes; filter '"46%' | broken load | news_corroboration_map § Broken-load traps |
| LF-R021 | FED_HRSA_NPDB PAYMENT is a $-prefixed string | broken load | news_corroboration_map § Broken-load traps |
| LF-R022 | ARCOS TRANSACTION_DATE is MMDDYYYY text; two rows hold floats | broken load | news_corroboration_map § Broken-load traps |
| LF-R023 | Registry notes are last-written intent, not landed state | Part B vintage | frank_investigation § Step 1 |
| LF-R024 | Don't compare Part B DY2023 to Part D DY2022 as one year; read as shape | cross-year ratio | frank_investigation § Step 2 |
| LF-R025 | CMS spells it ANTPSYCT; search devowelled names | declared a column missing | frank_investigation § corrections 3 |
| LF-R026 | Facility affiliation under-reports; one listed doctor is the modal case (35.5%) | base rate | frank_investigation § Step 4 |
| LF-R027 | Confirm statute text (1128a2, 1128a1, 1128b7) outside the warehouse; table stores only the code | load-bearing reading | frank_investigation § The man |
| LF-R028 | Part D carries no diagnosis; appropriateness is never showable | the whole case lives elsewhere | frank_investigation § gap that matters |
| LF-R029 | "CONNECT" is a schema; quote it | query failed | graph_hunt_ein § Q1 |
| LF-R030 | ENTITY_INDEX is a node table; an edge is two rows sharing ENTITY_ID | no from/to | graph_hunt_ein § Q1 |
| LF-R031 | Do not rank on table count, SOURCE_COUNT, or DOMAIN | file-splitting artifact; 2 domains is the ceiling | graph_hunt_ein § Q3; graph_bridges § Q1 |
| LF-R032 | EIN reaches no contracts, holdings, dockets, or campaign money tables | tax and employment key only | graph_hunt_ein § What EIN reaches |
| LF-R033 | ENTITY_ID is a key instance, one key type each | Boeing EIN and UEI are two entities | graph_bridges § Q1 |
| LF-R034 | Never mix asserted_same_row with asserted_affiliation | fanout 1 vs 6,962 | graph_bridges § two relations |
| LF-R035 | SPLIT_PART(A,'_',2) is not the agency | UK vs COMPANIES, 8871 vs DIRECTORS | graph_bridges § leaky filter |
| LF-R036 | A nonprofit missing from IRS↔OSHA is coverage, not a clean employer | 6% match rate | graph_bridges § Read the match rate |
| LF-R037 | FAC columns are AUDITEE_EIN / AUDITEE_UEI; AUDITOR_EIN is the accountant | wrong column silently | ghost_doctors § 1 |
| LF-R038 | A missing UEI before April 2022 is not a gap | identifier did not exist | ghost_doctors § 1; findings_views § chain |
| LF-R039 | LEIE REINDATE is 00000000 on every row; not a filter | OIG drops reinstated people | ghost_doctors § LEIE table |
| LF-R040 | Only 10.5% of LEIE rows carry an NPI; the rest are unjoinable | coverage floor | ghost_doctors § coverage floor |
| LF-R041 | Bucket exclusion date against the data year; after-year rows are not ghosts | 554 → 2 | ghost_doctors § First pass |
| LF-R042 | An NPI is a number, not a person; practice can bill under a departed NPI | two readings, same shape | ghost_doctors § What a hit means |
| LF-R043 | No public CMS file carries a payee TIN, EIN, or billing org | publication rule | ghost_partb § 1 |
| LF-R044 | _INGESTED_AT is load date, not vintage | ORDER_AND_REFERRING | ghost_ownership § still authorized |
| LF-R045 | A no-year table cannot place money before or after an exclusion | Part B $1.23M | ghost_partb § vintage problem |
| LF-R046 | Never add DME family columns; never take SPRSN_IND null as a clean row | 9,253 zero-filled rows | frank_dme § data trap |
| LF-R047 | BENE_DUAL_CNT and dementia share never publish 1–10 | median reads 0 from a hole | frank_dme § censored at 11 |
| LF-R048 | Spend-per-episode is blind to episode count | cannot counter a long-stay claim | frank_hospice § home health |
| LF-R049 | Recert ratio drops 1,055 infinite-ratio billers; disclose the denominator | one-direction exclusion | frank_hospice § comparison |
| LF-R050 | The 46-shape cut was chosen after seeing Frank; don't report as selection | post-hoc | frank_hospice § practice shape |
| LF-R051 | Confirm is a private nomination; publishing is a separate script that refuses without confirmed | two-step gate | HOUR_DOSSIER § 6 |
| LF-R052 | Decisions are append-only; latest verdict wins; never blind-retry an ambiguous write | audit log | HOUR_DOSSIER § 8; § 10 |

---

## FINDINGS

| id | finding | number | tables | source |
|---|---|---|---|---|
| LF-F001 | Ten largest landing tables, ARCOS first | 178,598,026; 13F 101,261,252; FEC indiv 84,172,112; CourtListener 71,677,647; AIS 58,106,517 | landing | ripple_pitch_deck.md § Problem 1 |
| LF-F002 | Total landing rows | 875,575,558 across 1,937 tables | landing | ripple_pitch_deck.md § Problem 1 |
| LF-F003 | dbt models | 1,378: 975 staging, 399 marts, 4 intermediate | dbt | ripple_pitch_deck.md § What I built |
| LF-F004 | Portal index | 338,520 datasets tagged by ID type | portal indexer | ripple_pitch_deck.md § What I built |
| LF-F005 | Entity resolution | 22.6M entities, 31.1M match-pairs | connect | ripple_pitch_deck.md § What I built |
| LF-F006 | Registry by domain | 2,992 registered; portal misc 1,404; health 135 | registry | ripple_pitch_deck.md § What I built |
| LF-F007 | Leads by detector | 17,256 total; osha 16,215; banned_but_paid 773; excluded_but_billing 236 | LEADS | ripple_pitch_deck.md § What it's found |
| LF-F008 | Opioid prescribers paid, by tier | low 5,485 $188.90 47.3%; medium 508 $2,039.88 64.1%; high 27 $54,248.21 59.8% | OPIOID_PRESCRIBER_PAID_HIGH_RX | ripple_pitch_deck.md § Opioid |
| LF-F009 | Opioid top states | FL 455 $799; CA 414 $491; TX 343 $702; NC 300; MI 250; TN 247; AZ 242; OH 234; GA 203 $996; IN 200 | same | ripple_pitch_deck.md § Opioid |
| LF-F010 | Hospital closure tiers | elevated 3,134; critical 1,214; high 87; total 4,435 | HOSPITAL_CLOSURE_RISK | ripple_pitch_deck.md § Hospitals |
| LF-F011 | Critical hospitals by state | CA 137; TX 107; LA 79; NY 58; IL 49; OH 42; FL 39; PA 34; OK 33; AZ 32 | same | ripple_pitch_deck.md § Hospitals |
| LF-F012 | Both-sides PACs top 5 | Fairshake 25 members $24,855,548; Realtors 550 $10,706,096; AIPAC 412 $8,392,834; Credit Unions 484 $6,438,914; AHA 440 $4,930,487 | PAC_FUNDS_BOTH_SIDES | ripple_pitch_deck.md § PACs |
| LF-F013 | Findings catalog | 9 registered: revoked nonprofits 22,512; opioid 6,020; hospitals 4,435; PACs 2,680; Congress 635; excluded paid 287 ×2; at facilities 28; EPA contractors 21 | FINDINGS.CATALOG | ripple_pitch_deck.md § catalog |
| LF-F014 | ARCOS stumble: WaPo's Kermit story pops | Strosnider Kermit 13.2M pills; Family Discount 12.8M; CVS Huntington 10.7M; 4 of top 6 named independents | FED_DEA_ARCOS_FULL | news_corroboration_map row 1 |
| LF-F015 | HMDA Philadelphia 2015–16 denial gap | Black 27.2%, white 8.1%, ratio 3.34; Baton Rouge 3.68, Memphis 3.59, St. Louis 3.56 | FED_CFPB_HMDA_HISTORIC | news_corroboration_map row 2 |
| LF-F016 | FEC smurfing donors | 1,103 name+state with 2,000+ gifts 2023–24; Makowski MI 48,130 gifts $99k | FED_FEC_INDIV_CONTRIBUTIONS | news_corroboration_map row 3 |
| LF-F017 | Waco patent surge | district 42 share of NOS 830: 2020 22.4%, 2021 25.2%, 2022 23.6%, 2023 17.6% | FED_FJC_IDB_CIVIL | news_corroboration_map row 4 |
| LF-F018 | Toddler and ancient PSCs | 5,053 born 2020+; 24 before 1900; 17 over 155 | UK_COMPANIES_HOUSE_PSC | news_corroboration_map row 5 |
| LF-F019 | NPDB concentration | 165,248 paid practitioners; top 1% hold 13.3% of dollars, 3.4% claims; repeaters 52.8% | FED_HRSA_NPDB | news_corroboration_map row 6 |
| LF-F020 | Flint lead | PWSID MI0002310; PB90 .006 → .011 → .020 (Jan–Jun 2016) → .012; action level .015 | FED_EPA_SDWA_SDWA_LCR_SAMPLES | news_corroboration_map row 7 |
| LF-F021 | Jackson MS lead | MS0250008; .0286 period ending 12/31/2015; .016 in 2016 | same | news_corroboration_map row 8 |
| LF-F022 | Upper Big Branch | 506 violations 2009, 198 S&S, 920 in 2010; rank 10 of 192 WV mines | FED_MSHA_VIOLATIONS | news_corroboration_map row 9 |
| LF-F023 | Wells Fargo complaint spike | ~770/month Jan–Aug 2016, 1,592 Sep, 1,383 Oct | FED_CFPB_COMPLAINTS | news_corroboration_map row 10 |
| LF-F024 | Amazon injury rate | NAICS 4931 TRIR 6.21 over 458 sites vs 3.51 for 9,405 others | FED_OSHA_ITA_300A_SUMMARY_2024 | news_corroboration_map row 11 |
| LF-F025 | Norfolk Southern 2023 | 435 accidents (452 in 2022), 9 hazmat cars; UP 776, BNSF 492 | FED_FRA_EQUIPMENT_ACCIDENTS | news_corroboration_map row 12 |
| LF-F026 | Lieber NIH money | FY2000–2019 $11.4M; FY2017–18 $1.4–1.6M/yr; FY2024–26 $36–42k | FED_NIH_REPORTER | news_corroboration_map row 14 |
| LF-F027 | ICE book-ins | 45k Dec 2024 → 104k Jun 2025 → 128k Dec 2025; deaths 9 (2024) → 15 (2025) | FED_ICE_DETENTION_STINTS | news_corroboration_map row 16 |
| LF-F028 | PPP address stacking works | 40 loans at one Peoria address | FED_SBA_PPP | news_corroboration_map row 17 |
| LF-F029 | 2024 political ad spend | Harris Victory Fund $67.0M; FF PAC $61.7M; Harris for President $53.6M; Trump 2024 $32.3M | FED_GOOGLE_POLADS_ADVERTISER_WEEKLY_SPEND | news_corroboration_map row 18 |
| LF-F030 | House PTR filings 2021–22 | Lowenthal 140, DelBene 36, Blumenauer 34, Green 32 | FED_HOUSE_FD_PTR_INDEX | news_corroboration_map row 19 |
| LF-F031 | Tesla brake complaints | 42 Sep 21 → 884 Feb 22 | FED_NHTSA_COMPLAINTS | news_corroboration_map row 20 |
| LF-F032 | Debarred still paid | 22 vendors, 99 actions, $1.86M | SAM × USAspending FULL_R2 | news_corroboration_map row 22 |
| LF-F033 | Dollars for Docs | paid $10k+ prescribers write 1.6x–7x costlier scripts | Open Payments × Part D 2024 | news_corroboration_map row 23 |
| LF-F034 | Corroboration tally | 17 hits, 1 partial, 1 weak, 5 misses of 24 | — | news_corroboration_map § scorecard |
| LF-F035 | HMDA reload | 44,992,667 rows, 8 action codes, 6,967,834 denials; mart rebuilt | HOUSING__FED_CFPB_HMDA_HISTORIC | news_corroboration_map § Mart rebuilt |
| LF-F036 | Takedown NPI matches | Moss 1457428195; McKenna 1013209543; Cline 1619934858; Morrison 1679525430; Aquino 1508818311; Gala 1740660992 | NPPES | takedown_vs_warehouse § NPI matches |
| LF-F037 | Moss outlier | claims/bene 40.4 (99.3 pct); FP median 9.2, p99 36.3; Part B 10,613 services 149 benes 99.55 pct | Part D 2024, Part B | takedown_vs_warehouse § Part D |
| LF-F038 | McKenna outlier | opioid rate 56.47 (99.0), long-acting 35.85 (99.4) among 252,542 NPs | Part D 2024 | takedown_vs_warehouse § Part D |
| LF-F039 | Peers at the defendants' bars | FP 66; NP 180; EM 448 | Part D 2024 | takedown_vs_warehouse § Step 5 |
| LF-F040 | Defendants' Open Payments tiny | Moss $1,291; McKenna $1,744; Cline $1,130; Aquino $29 | Open Payments | takedown_vs_warehouse § Open Payments |
| LF-F041 | Frank identity | NPI 1164450573; Family Practice; IND_PAC_ID 4587624473; excluded 2025-08-20 under 1128a2; no Medicare enrollment | LEIE, NPPES | frank_investigation § The man |
| LF-F042 | Frank's three affiliations | Haskell Care Center 375414; Neighborhood Hospice 371701; Universal Rehab 377668 | FED_CMS_FACILITY_AFFILIATION | frank_investigation § Step 1 |
| LF-F043 | Frank Part B | 464 benes, 3,140 services, $207,303.28, drug $0, risk 1.9925; DY2023 not proven | Part B by provider | frank_investigation § Step 1 |
| LF-F044 | Frank top HCPCS | 99309 1,099 $78,255; 99349 762 $59,464; G0179 201 $5,726 | Part B by service | frank_investigation § Step 1 |
| LF-F045 | Frank Part D DY2022 | 486 brands, 136,920 claims, $10,703,850.59; rank 9 of 102,484 FP | FED_CMS_PARTD_PRESCRIBER_DRUG | frank_investigation § Step 2 |
| LF-F046 | Frank top drugs | Eliquis $897,244; Invega Sustenna $619,074; Nuedexta $531,329; Nuplazid $406,124 (190 claims, 17 benes) | same | frank_investigation § Step 2 |
| LF-F047 | Antipsychotic share DY2022 | 8,294 claims, 6.06%; peer median 0.29%, p99 4.78%; rate pct 99.45; 61,432 peers | same | frank_investigation § Step 3 A |
| LF-F048 | Antipsychotic share DY2024 | 4.51% of 65+ claims; peer p99 4.445%, median 0.521%; rate pct 99.04; 44,406 peers | FED_CMS_PART_D_PRESCRIBERS | frank_investigation § Step 3 B |
| LF-F049 | Frank DY2024 totals | 41,925 claims; $3,531,599.20; 1,265 benes; antipsychotic 65+ 1,427 claims $303,465.32 154 benes | same | frank_investigation § Step 3 B |
| LF-F050 | Clozapine and paliperidone | 1,122 clozapine claims ~70 patients; four paliperidone products $760,881 | Part D by drug | frank_investigation § Step 3 |
| LF-F051 | Haskell facility | 58 beds, 35.4 avg residents, for-profit LLC | nursing home | frank_investigation § Step 4 |
| LF-F052 | Affiliation base rate | 14,501 homes; median 2 providers; 5,148 (35.5%) list one; OK 112 of 218 | FED_CMS_FACILITY_AFFILIATION | frank_investigation § Step 4 |
| LF-F053 | Haskell citations | 26 rows 2022-04-14 to 2024-09-27; F757 unnecessary drugs, F758 psychotropics; G harm 2023-11-21; three abuse tags 2024-09-27 | FED_CMS_NURSING_HOME_DEFICIENCIES | frank_investigation § Step 4 |
| LF-F054 | Haskell penalty | $3,422 fine 2023-11-21 | penalties | frank_investigation § Step 4 |
| LF-F055 | Frank Open Payments | 2022: 36 pmts $914.79; 2023: 18 $569.55; 2024: 1 $3,082,225.00 | Open Payments | frank_investigation § Step 6 |
| LF-F056 | Acadia top payer both years, product Nuplazid | $468.77 (2022), $245.29 (2023) | Open Payments | frank_investigation § Step 6 |
| LF-F057 | Skye write-off to Frank | $3,082,225 owed by Previse Medical, 2024-01-15; 43% of Skye's 2024 filing | Open Payments 2024 | frank_investigation § Step 6 |
| LF-F058 | Frank DME row | 23 suppliers, 84 HCPCS, 64 benes, 353 claims, 36,017 services, $76,930.72 paid | DME by referrer | frank_investigation § Step 7; frank_dme |
| LF-F059 | Paid-after-exclusion view span | 2023–2024 only; 287 doctors; 1,439 payments; $511,627.42 | EXCLUDED_PROVIDER_PAID_AFTER_EXCLUSION | findings_views § 1 |
| LF-F060 | View vs hand run: disjoint | zero overlap; combined 2022–24 $850,499.84 across 1,987 payments | same + Open Payments 2022 | findings_views § reconciliation |
| LF-F061 | Exclusion-year tail | 1995 exclusion still paid $12.87; 2019 and 2021 exclusions carry $438,013 (85.6%) from 39 people | same | findings_views § tail |
| LF-F062 | Asfora continuing stream | Medtronic $301,647 (2022) + $318,325 (2023) = $619,972 after April 2021 exclusion | Open Payments | findings_views § two names |
| LF-F063 | Miranda breadth grew | 45 payers 2022; 60 payers 2023–24 on 412 payments | Open Payments | findings_views § two names |
| LF-F064 | EPA contractor view shape | 57 rows; $106,996,950,324 fed dollars; $3,006,703 penalties; 58 facilities; 0 SNC | FEDERAL_CONTRACTOR_EPA_VIOLATOR | findings_views § 2 |
| LF-F065 | SpaceX row | $100,832,599,497 obligated; $90,000 EPA penalty; 94% of view dollars | same | findings_views § 2 |
| LF-F066 | EPA view top penalties | GM $654,150; Edwards $500,000; SiteOne $311,313 | same | findings_views § 2 |
| LF-F067 | Key reach | UEI 827,685 values in 9 tables; FRS_ID 5,404,044 in 17 | CONNECT | findings_views § chain |
| LF-F068 | CONNECT schema | 27 base tables; ENTITY_INDEX 96,399,174 rows; CONNECT_EDGES 4,512 | LIBRARY_META.CONNECT | graph_hunt_ein § Q1 |
| LF-F069 | Enrollment → NPPES edge | 2,540,936 matched, 100%, STEEL | CONNECT_EDGES | graph_hunt_ein § Q1 |
| LF-F070 | Raw heaviest entities | Caterpillar EIN 20 tables; Target 20; NPI Kim 19 | ENTITY_INDEX | graph_hunt_ein § Q2 |
| LF-F071 | Collapsed source systems | Caterpillar 6; Target 7; the same six systems every time | ENTITY_INDEX | graph_hunt_ein § Artifact 1 |
| LF-F072 | EIN reach | 55 tables; IRS EO BMF 1,983,563; Form 5500 466,444; OSHA 123,206; SEC DERA 4,744 | ENTITY_INDEX | graph_hunt_ein § What EIN reaches |
| LF-F073 | ENTITY_ID key types | 40,038,834 entities, all one key type | ENTITY_INDEX | graph_bridges § Q1 |
| LF-F074 | ENTITY_XREF | 2,672,384 rows; six key pairs only | ENTITY_XREF | graph_bridges § Q1 done properly |
| LF-F075 | Same-row bridges | FRS_ID→LEI 73,948; CCN→NPI SNF 14,251; BIOGUIDE→ICPSR 12,298; CIK→EIN ~4,200–4,800/quarter | ENTITY_XREF | graph_bridges § every key pair |
| LF-F076 | Affiliation fanouts | CCN→NPI 2,249,953 rows max 6,962; FEC cand→cmte max 821; IMO→MMSI max 21 | ENTITY_XREF | graph_bridges § every key pair |
| LF-F077 | Edge tiers | CORROBORATED 2,513; STEEL 1,345; BRIDGE 512; GEO 140; STRONG 2 | CONNECT_EDGES | graph_bridges § Q2 |
| LF-F078 | Strongest cross-agency edges | NPPES↔LEIE NPI 8,660 100%; GLEIF↔EPA crosswalk 22,743 100%; legislators↔Voteview 12,584 100%; FAC↔USAspending UEI 40,746 68.5% | CONNECT_EDGES | graph_bridges § four strongest |
| LF-F079 | IRS↔OSHA edge | 7,446 matched, 6.0% | CONNECT_EDGES | graph_bridges § Read the match rate |
| LF-F080 | BRIDGE_ENTITIES | 53,799 rows spanning >1 domain | BRIDGE_ENTITIES | graph_bridges § BRIDGE_ENTITIES |
| LF-F081 | FAC EIN↔UEI bridge | 411,638 rows; 178,295 both valid (43.3%); 61,577 pairs; 58,680 EINs; 95.9% one UEI | FED_FAC_SINGLE_AUDIT | ghost_doctors § 1 |
| LF-F082 | UEI cutover visible | 2022+ 100% UEI; 2021 2.0%; 2019 0.2% | same | ghost_doctors § 1 |
| LF-F083 | LEIE shape | 83,842 rows; 8,841 with NPI (10.5%); 8,660 distinct; REINDATE constant | FED_HHS_OIG_LEIE | ghost_doctors § LEIE |
| LF-F084 | Ghost bucket | 554 NPIs; 522 excluded after 2022; 30 during; 2 before | LEIE × Part D DY2022 | ghost_doctors § First pass |
| LF-F085 | Two ghosts | Miranda 1285673012 excl 2015-06-18 $7,702,674; Aswad 1871571406 excl 2016-01-20 $2,552,958 | same | ghost_doctors § two that survive |
| LF-F086 | Miranda enrollment | PAC 8022034875, one member; ENRLMT I20070525000116; ORG_NAME null; MULTIPLE_NPI_FLAG N | FFS, PECOS | ghost_ownership § Miranda |
| LF-F087 | Miranda hospitals | 450643 Doctors Hospital of Laredo; 450092 Fort Duncan L.P.; 451387 Uvalde County Hospital Authority; 451390 Dimmit | affiliation, HOSPITAL_ENROLLMENTS | ghost_ownership § four hospitals |
| LF-F088 | Miranda still Y to order/refer on all five | file landed 2026-08-05 | FED_CMS_ORDER_AND_REFERRING | ghost_ownership § still authorized |
| LF-F089 | Miranda drugs | Ibrance $749,617; Imbruvica $722,465; Xtandi $675,915; $5,774/claim | Part D by drug | ghost_ownership § prescribing |
| LF-F090 | Miranda industry contact | 225 pmts $4,415.57 from 45 mfrs (2022); 211 $5,111.17 43 (2023); 201 $5,528.36 49 (2024) | Open Payments | ghost_ownership § Industry |
| LF-F091 | Aswad footprint | 7 tables; no enrollment, affiliation, or order/refer row; 6 pmts $120.48 (2022), 1 $200 (2023) | various | ghost_ownership § Aswad |
| LF-F092 | Miranda Part B | $1,229,994.33 paid; drug $1,102,884.56 (89.7%); 312 benes; 62,599 services; ENT_CD I | Part B by provider | ghost_partb § 2 |
| LF-F093 | Miranda DME | 6 suppliers, 24 claims, 1,343 services, $46,385.19 | DME by referrer | ghost_partb § DME row |
| LF-F094 | FISS table is names only | 2,047,828 rows; NPI, LAST_NAME, FIRST_NAME | FISS attending/rendering | ghost_partb § FISS |
| LF-F095 | Part B by provider columns | 83 columns; no payee, TIN, EIN, group NPI; 1,296,739 rows | Part B by provider | ghost_partb § 1 |
| LF-F096 | Pharma paid excluded 2022 | 137 NPIs; 648 payments; $338,872.42; 141 manufacturers | Open Payments 2022 × LEIE | pharma_paid_excluded § headline |
| LF-F097 | Naive vs date-tested | 532 NPIs $1,329,835.35 vs 137 $338,872.42 | same | pharma_paid_excluded § method |
| LF-F098 | Nature split | Royalty 6 $303,420.98 (89.5%); Food 582 $21,468.88 avg $36.89 | same | pharma_paid_excluded § breaks in two |
| LF-F099 | Asfora royalty | Medtronic $301,647 2022-06-02; excluded 2021-04-30 1128b7 | same | pharma_paid_excluded § one row |
| LF-F100 | Remainder | $37,225.42 across 136 NPIs, $274 each | same | pharma_paid_excluded § what is left |
| LF-F101 | AbbVie breadth | 23 excluded NPIs, 38 payments, $1,274.62 | same | pharma_paid_excluded § breadth |
| LF-F102 | Longest gap | Lupiano excluded 2011-09-20, paid by 5 mfrs in 2022 | same | pharma_paid_excluded § longest |
| LF-F103 | Open Payments years | 2022: 13,306,564; 2023: 14,700,786; undated = PY2024: 15,385,047 | Open Payments | molina § table question |
| LF-F104 | Molina record | RECORD_ID 1075873943; Skye Orthobiologics LLC (100000226833); $114,040; 2024-01-22; Debt forgiveness "Bad Debt"; Del Sol Medical; no product | Open Payments 2024 | molina § record |
| LF-F105 | Molina exclusion | 2019-06-20, 1128a1; four tables only; three cities 600 miles apart | LEIE, NPPES | molina § identity |
| LF-F106 | Skye 2024 | 30 write-offs $7,195,734.55; 7 speaking $12,000; 99.8% bad debt | Open Payments 2024 | molina § company |
| LF-F107 | Skye pattern | 17 of 30 podiatry/wound; FL 11 TX 7 MI 5 MS 3; 11 on Dec 30–31; top 4 = 84% | same | molina § pattern |
| LF-F108 | Two of 30 excluded | Molina after exclusion; Frank 19 months before his | same × LEIE | molina § two of 30 |
| LF-F109 | DME family non-additivity | benes match 60.5% of 52,912; suppliers 62.8%; services 78.5% of 171,372 | DME by referrer | frank_dme § additivity |
| LF-F110 | Frank DME percentiles | services/bene 562.8 at 91.3rd (18,213 above of 208,605); band 81–92; FP 95.4th | same | frank_dme § headline |
| LF-F111 | Frank supplier density below median | 0.359 vs 0.462; 39.2nd pct; paid/service $2.14 vs $17.97 | same | frank_dme § five ratios |
| LF-F112 | Frank DME panel | dual 62.5% (92.8th); dementia 50.0% (94.4th); risk 3.117 (88.0th); age 74.1 | same | frank_dme § patient mix |
| LF-F113 | Common-cohort ordering | 3,468 FP rows: volume 93.9th > dementia 92.2 > risk 92.0 > dual 87.7 | same | frank_dme § reversal |
| LF-F114 | Dementia column fill | 325,834 null; 37,000 zero; 18,394 positive | same | frank_dme § censored |
| LF-F115 | Frank's facilities' names drift | hospice DBA Complete Hospice Care of Southern Oklahoma; HHA three names across three files | affiliation, enrollments | frank_hospice § named |
| LF-F116 | Geography | Haskell ~130 mi east; Lawton ~90 mi SW of OKC | — | frank_hospice § Geography |
| LF-F117 | Universal Healthcare quality | 1.5 stars, bottom 749 of 7,961; bathing 41.14% (2.4th); breathing 37.94%; bed 45.00%; walking 49.71%; meds 46.74% | FED_CMS_HOME_HEALTH | frank_hospice § home health |
| LF-F118 | Frank recert ratio | G0179 201 services 59 benes; G0180 31/30; ratio 6.48; 3.41 recerts per patient | Part B by service | frank_hospice § finding |
| LF-F119 | Recert peer set | national 0.57; 5,136 both-code billers median 1.04, p99 6.56; Frank rank 54, 98.97th | same | frank_hospice § comparison |
| LF-F120 | Alternate denominators | every G0179 biller 1,109 of 6,191 (82.1); either code 1,109 of 19,653 (94.4) | same | frank_hospice § comparison |
| LF-F121 | Panel test | Frank 6.48; Cox 4.10; James 2.39; Deppen 2.25; panel median 1.706 = 76th pct nationally | same | frank_hospice § agency or man |
| LF-F122 | Oklahoma baseline | 237 practitioners, median 1.79, Frank 3rd; FP only 1,582 median 1.20 rank 15 | same | frank_hospice § agency or man |
| LF-F123 | G0182 is rare | 211 providers nationally, 23,077 services | same | frank_hospice § hospice |
| LF-F124 | Practice shape counts | 940,350 affiliated; 30,511 hospice; 122,538 HHA; 7,127 all three; 950 one each; 46 nothing else | affiliation | frank_hospice § practice shape |
| LF-F125 | LEIE matches in affiliated | 15 of 940,350; 1 of 7,127; 1 of 46 | affiliation × LEIE | frank_hospice § exclusion rate |
| LF-F126 | PECOS size | 2,978,925 rows; 129,509 FP; Frank absent; both facilities present | PECOS | frank_hospice § Loose ends |
| LF-F127 | No hospice utilization file; no owner identity landed | two hospice tables, both directories | landing | frank_hospice § What the warehouse holds |
| LF-F128 | Warehouse capabilities census | 1.23B records; 589 curated tables; 31.8M resolved entities; 349 dated tables, 306 current into 2026 | — | warehouse_capabilities |
| LF-F129 | Reading Room queue 2026-07-21 | 1,030 pending: banned_but_paid 773; excluded_but_billing 236; banned_but_operating 11; vessel v2 6; v1 2; debarred 2 | safe view | HOUR_DOSSIER § 3 |
| LF-F130 | Lead #1 | Mohammed Hadi NPI 1275760100, excluded 2024-10-20 1128a1; 210 records $4,779.27, 2022-01-05 → 2024-12-10; score 6.5 | LEIE, NPPES, Open Payments 43.3M | HOUR_DOSSIER § 4 |
| LF-F131 | PAT clamp bug | USE SECONDARY ROLES NONE refused on restricted PATs; fixed in reading_room/connections.py; 15/15 tests | app | HOUR_DOSSIER § 0 |

---

## DEAD ENDS

| id | what was tried | why it died | source |
|---|---|---|---|
| LF-D001 | 243 excluded providers "still in prescriber file" | 242 excluded after the file year; arrow backwards | ripple_pitch_deck.md § Problem 3 |
| LF-D002 | Naive USASpending row count | 174x inflation from modifications | ripple_pitch_deck.md § Problem 3 |
| LF-D003 | HMDA morning echo | 19.1M rows all originated, zero denials; loader took first-lien family | news_corroboration_map row 2 |
| LF-D004 | Life Care Kirkland 2020 survey | CMS rolling ~3-year window; 2020 gone | news_corroboration_map row 13 |
| LF-D005 | Ozempic FAERS 2023 | table ends 2014q2; drug approved 2017 | news_corroboration_map row 15 |
| LF-D006 | Kabbage fake farms in PPP | only 150K+ file landed (968,524 rows); ~$20k loans absent | news_corroboration_map row 17 |
| LF-D007 | Thomas–Crow gifts | no people table to tie disclosure to a judge; SOURCE is OCR with 58 nulls | news_corroboration_map row 21 |
| LF-D008 | UBB stumble by raw count | ranks 10th; story was withdrawal orders and S&S density | news_corroboration_map row 9 |
| LF-D009 | "Reproduces Reveal" | raw ratio 3.4x / OR 4.35 vs Reveal's adjusted 2.7; different statistic | news_corroboration_map § Skeptic second pass |
| LF-D010 | Takedown "5 of 5" | Aquino tops at 86th; 4 of 5 | news_corroboration_map row 24 |
| LF-D011 | Lieber $13M; FEC name+zip9; FJC TAPEYEAR | skeptic: $11.4M; zip9 splits people; TAPEYEAR lags | news_corroboration_map § Skeptic pass |
| LF-D012 | Negative controls on the 24 stories | never run; every grade is one query | news_corroboration_map § Skeptic pass |
| LF-D013 | Frank "only physician at Haskell" | 35.5% of homes list one; modal case | frank_investigation § corrections 1 |
| LF-D014 | Part B "2022-era" | registry says DY2023 | frank_investigation § corrections 2 |
| LF-D015 | "No %ANTIPSYCH% column" | ANTPSYCT_GE65_* exists | frank_investigation § corrections 3 |
| LF-D016 | "Only DY2022 Part D landed" | FED_CMS_PART_D_PRESCRIBERS is DY2024 | frank_investigation § corrections 4 |
| LF-D017 | 26-brand antipsychotic list | missed 7.9% of national claims; 5.75% → 6.06% | frank_investigation § corrections 5 |
| LF-D018 | "20x the peer median" | suppression depresses median; inflated by unknown amount | frank_investigation § Step 3 |
| LF-D019 | 492 distinct drugs | row count; 486 distinct brands | frank_investigation § corrections 8 |
| LF-D020 | 2023 payments vs Part D cost column | DY2022 figures repeated | frank_investigation § corrections 9 |
| LF-D021 | "Federal contractors mostly comply" from the EPA view | 57 rows from 3.3M facilities × 93.2M contracts is a join finding | findings_views § 2 |
| LF-D022 | SELECT * FROM LIBRARY_META."CONNECT" | it's a schema | graph_hunt_ein § Q1 |
| LF-D023 | Heaviest EIN by table count | SEC quarterly and OSHA yearly splits; measures file splitting | graph_hunt_ein § Artifact 1 |
| LF-D024 | Collapsed-family ranking | Colorado portal ten tables; all top 15 are Denver nonprofits | graph_hunt_ein § Artifact 2 |
| LF-D025 | Contracts-to-donations chain on EIN | EIN reaches none of those tables; false clean negative | graph_hunt_ein § What EIN reaches |
| LF-D026 | HAVING COUNT(DISTINCT KEY_TYPE) > 1 | zero rows; one key type per ENTITY_ID | graph_bridges § Q1 |
| LF-D027 | Cross-agency filter by SPLIT_PART | three same-registry pairs slipped through | graph_bridges § leaky filter |
| LF-D028 | Filter LEIE on REINDATE | constant 00000000 | ghost_doctors § LEIE |
| LF-D029 | Ghost hunt first pass, 554 | vintage; 552 excluded after or during 2022 | ghost_doctors § First pass |
| LF-D030 | Find the corporate owner of the ghost NPIs | both sole practitioners, ORG_NAME null | ghost_ownership § direct answer |
| LF-D031 | Miranda convicted 2013 of black-market drug fraud | investigator's claim; not in warehouse | ghost_ownership § What the tables support |
| LF-D032 | Find the Part B payee TIN | no CMS public file carries one; NPPES EIN 100% empty | ghost_partb § 1 |
| LF-D033 | Name the six DME suppliers | referrer file has no supplier link; supplier file has no referrer | ghost_partb § DME row |
| LF-D034 | Naive 2022 pharma-paid join, 532 NPIs | not date-tested; wrong by 4x | pharma_paid_excluded § method |
| LF-D035 | Molina "six-figure cheque" | bad-debt write-off, no money moved | molina § record |
| LF-D036 | Frank DME 563 services/patient as extreme | 18,213 to 72,586 referrers higher; band 81–92 | frank_dme § headline |
| LF-D037 | "Earlier reports disagree on Frank's DME row" | those figures were Miranda's | frank_dme § correction wrong |
| LF-D038 | Beneficiary additivity 18.7% | wrong denominator; 60.5% | frank_dme § additivity |
| LF-D039 | "Panel sicker than volume is high" | three denominators; reversed on common cohort | frank_dme § reversal |
| LF-D040 | 0.98 spend ratio as counterweight | per-episode, blind to episode count | frank_hospice § home health |
| LF-D041 | Six panel doctors "absent from Part B" | present, just under the 11-bene floor | frank_hospice § agency or man |
| LF-D042 | Three-facility shape as rare fraud pattern | 7,127 physicians have it | frank_hospice § practice shape |
| LF-D043 | Exclusion rate among shape cohort | 15 of 940,350; LEIE can't support a rate | frank_hospice § exclusion rate |
| LF-D044 | LEIE name search on org names | three false hits, single-word collision | frank_hospice § Loose ends |
| LF-D045 | Matching DME referrer to supplier on state+HCPCS+volume | inference dressed as evidence; not done | frank_dme § could not be done |
| LF-D046 | Reading Room review 2026-07-21 | REVIEW schema, DECISIONS table, LEAD_QUEUE mart, REVIEW PAT all missing | HOUR_DOSSIER § 0 |

---

## LOOSE

| id | item | source |
|---|---|---|
| LF-L001 | Stations = the real things watched | RIPPLES.md § five pieces |
| LF-L002 | Readings = same simple measurements at every station | RIPPLES.md § five pieces |
| LF-L003 | Fronts = connections (shared owner, address, officer) | RIPPLES.md § five pieces |
| LF-L004 | Seasons = shared timeline; each pull one observation | RIPPLES.md § five pieces |
| LF-L005 | Instruments = a dumb question mounted once | RIPPLES.md § five pieces |
| LF-L006 | Blip = passed luck-check, unconfirmed; a queue | RIPPLES.md § outputs |
| LF-L007 | Warning = answered loudly, worth a human's time | RIPPLES.md § outputs |
| LF-L008 | Leading indicator = a stream that moves before another | RIPPLES.md § outputs |
| LF-L009 | Finding = warning that survived resemblance + fronts + Chris's sign-off | RIPPLES.md § outputs |
| LF-L010 | Dead air = the hand-off that should happen but doesn't | RIPPLES.md § outputs |
| LF-L011 | False readings = wrong explanations, never forbidden data | RIPPLES.md § traps |
| LF-L012 | The climate = shared background rhythm | RIPPLES.md § traps |
| LF-L013 | Older strata keep their names: entity spine, connection tiers, clock lanes, detectors, 52-lens catalogue, queue-vs-finding law | RIPPLES.md § Untouched older strata |
| LF-L014 | "Simple pieces. Honestly measured. Allowed to touch. Then the patterns draw themselves." | RIPPLES.md § core idea |
| LF-L015 | "Complicated pieces can't do this. The moment a piece gets clever, it gets incompatible." | RIPPLES.md § core idea |
| LF-L016 | "That pattern exists in no single row anywhere." | RIPPLES.md § worked example |
| LF-L017 | "Ripple" means exactly one thing: the platform | RIPPLES.md § GLOSSARY |
| LF-L018 | Only 14 connection families rock-solid; next tier name+zip; politics zero hard links; courts/sanctions/ARCOS/ICIJ are graph dark matter | RIPPLES.md § landmine 3 |
| LF-L019 | "It's a lens, not a checklist." New Ripples welcome; State, Neighbors, Flow are the first three | RIPPLES.md § How sessions use this |
| LF-L020 | "Has anyone ever just... put those two lists next to each other?" | ripple_pitch_deck.md § dumb question |
| LF-L021 | "Not sophisticated analysis. Not AI making predictions. Just: is this entity on List A and also on List B" | ripple_pitch_deck.md § The idea |
| LF-L022 | "The 'interesting question' takes five minutes. Making sure the answer is actually correct takes days." | ripple_pitch_deck.md § Problem 3 |
| LF-L023 | "The joins are just... sitting there." | ripple_pitch_deck.md § Why it might matter |
| LF-L024 | "Either I'm onto something, or I'm missing a reason why nobody does this." | ripple_pitch_deck.md § What I don't know |
| LF-L025 | "That's not ideology — that's access purchasing." | ripple_pitch_deck.md § PACs |
| LF-L026 | "I hold everything loosely." One person doing QA on own work | ripple_pitch_deck.md § What I don't know |
| LF-L027 | Healthcare has the cleanest IDs; environment and corporate ownership mostly don't | ripple_pitch_deck.md § Problem 2 |
| LF-L028 | Is this a product? Undecided: journalists, oversight, dataset, portfolio | ripple_pitch_deck.md § What I don't know |
| LF-L029 | "No funding. No team. No proprietary data. Just public records and a question that wouldn't leave me alone." | ripple_pitch_deck.md § close |
| LF-L030 | SDWIS sample periods may sit a step late — skeptic suspicion left open | news_corroboration_map § Skeptic pass |
| LF-L031 | "That is a lead of unusual quality. It is not a conclusion." | frank_investigation § What the data supports |
| LF-L032 | "$468.77 does not buy $406,124. The payments show who was in the building." | frank_investigation § Step 6 |
| LF-L033 | "A finding about the join, not about American industry" | findings_views § 2 |
| LF-L034 | "A headline without a body" — SpaceX ratio | findings_views § 2 |
| LF-L035 | "This is not a discovery about Caterpillar. It is a discovery about the SEC, which publishes quarterly." | graph_hunt_ein § Artifact 1 |
| LF-L036 | "The DEA number connects to nothing." | graph_bridges § top key combinations |
| LF-L037 | FRS_ID↔LEI is "the sleeper" | graph_bridges § one bridge |
| LF-L038 | "The naive join reads the arrow backwards." | ghost_doctors § First pass |
| LF-L039 | "A publication rule, not a corporate structure." | ghost_partb § Why |
| LF-L040 | "Devices pay royalties and consulting fees; drugs buy lunch." | pharma_paid_excluded § Top 10 |
| LF-L041 | "None of them cross-checked a free, public, monthly-updated federal list before writing the cheque." | pharma_paid_excluded § What this supports |
| LF-L042 | "The largest single transfer of value in this company's 2024 filing went to a doctor the government barred the following year." | molina § two of 30 |
| LF-L043 | "Cheap unit price against a high unit count is the consumables shape, not the fraud shape." | frank_dme § five ratios |
| LF-L044 | "A percentile inside a distribution with a hole in it" | frank_dme § censored |
| LF-L045 | "The ratio is a flag, not a verdict." | frank_hospice § load-bearing unknown |
| LF-L046 | "The CCN is what held." Name-only matching would have missed both | frank_hospice § named |
| LF-L047 | "Credibility is the product" | warehouse_capabilities § Honest limits |
| LF-L048 | Zero false merges: spine never guesses two similar names are one | warehouse_capabilities § 1 |
| LF-L049 | "The case serves the map." Top-10 review is a receipt check, not the deliverable | HOUR_DOSSIER § Altitude note |
| LF-L050 | Junk signature: predate-exclusion + tiny dollars + name conflict + gutting caveat. Good: three-source + paid-after + continuing activity | HOUR_DOSSIER § 7 |
| LF-L051 | All-rejects still counts: a finding about detector precision | HOUR_DOSSIER § 9 |
| LF-L052 | Vessel AIS is a Jan 1–8 2024 snapshot; SAM table is a 1,000-row capped sample with no dates | HOUR_DOSSIER § 7 |
| LF-L053 | 558 sources, 1.23B records; FAERS alone 62M | THE_SCRIPT § 1 |
| LF-L054 | 174 fields tracked as misrepresenting themselves as complete; 29 tables had plain years erased | THE_SCRIPT § 2 |
| LF-L055 | 4,800+ test suite against the data itself | THE_SCRIPT § 2 |
| LF-L056 | "Loaded" and "trustworthy" are two tracked states | THE_SCRIPT § 2 |
| LF-L057 | 75 finished tables rebuilt in one week | THE_SCRIPT § 3 |
| LF-L058 | ~32M identities; 14 verified ID types link at 97–100% | THE_SCRIPT § 4 |
| LF-L059 | "A census of the public record, not a search for one target." | THE_SCRIPT § 5 |
| LF-L060 | "A single anecdote only matters if the data proves the pattern is real and repeated." | THE_SCRIPT § 5 |
| LF-L061 | Health scored on a standing 0–100 scale | THE_SCRIPT § 7 |
| LF-L062 | "Treats 'it looks complete' as a hypothesis to test." | THE_SCRIPT § 7 |
| LF-L063 | AI helped build it; finished system runs on plain SQL | THE_SCRIPT § 6 |
| LF-L064 | Loaders checkpoint so multi-hour jobs resume | THE_SCRIPT § 6 |
| LF-L065 | Thin or absent domains: energy, agriculture, insurance, Social Security | warehouse_capabilities § Honest limits |
| LF-L066 | wish: Census / ACS tract-level demographics | ripple_frontier_MASTER_LIST.md § Round 1 |
| LF-L067 | wish: HUD ZIP↔Tract↔County↔District crosswalk | ripple_frontier_MASTER_LIST.md § Round 1 |
| LF-L068 | wish: Census TIGER/Line boundary shapes | ripple_frontier_MASTER_LIST.md § Round 1 |
| LF-L069 | wish: BLS QCEW county-by-industry employment + wages | ripple_frontier_MASTER_LIST.md § Round 1 |
| LF-L070 | wish: OSHA enforcement | ripple_frontier_MASTER_LIST.md § Round 1 |
| LF-L071 | wish: FDA FAERS adverse events (current) | ripple_frontier_MASTER_LIST.md § Round 1 |
| LF-L072 | wish: DOJ Deaths in Custody + Vera 50-year incarceration | ripple_frontier_MASTER_LIST.md § Round 1 |
| LF-L073 | wish: EPA EJScreen (Harvard mirror) | ripple_frontier_MASTER_LIST.md § Round 1 |
| LF-L074 | wish: NIH RePORTER + Drugs@FDA approvals | ripple_frontier_MASTER_LIST.md § Round 1 |
| LF-L075 | wish: CMS Hospital Price Transparency files | ripple_frontier_MASTER_LIST.md § Round 1 |
| LF-L076 | wish: SBA PPP loan-level (all sizes) | ripple_frontier_MASTER_LIST.md § Round 1 |
| LF-L077 | wish: SEC Form ADV private-fund filings | ripple_frontier_MASTER_LIST.md § Round 1 |
| LF-L078 | wish: county parcel + assessor records | ripple_frontier_MASTER_LIST.md § Round 1 |
| LF-L079 | wish: federal lobbying disclosures (LDA) | ripple_frontier_MASTER_LIST.md § Round 1 |
| LF-L080 | wish: congressional stock trades (STOCK Act) | ripple_frontier_MASTER_LIST.md § Round 1 |
| LF-L081 | wish: state campaign finance + Open States | ripple_frontier_MASTER_LIST.md § Round 1 |
| LF-L082 | wish: IRS 990 dark-money grant schedules | ripple_frontier_MASTER_LIST.md § Round 1 |
| LF-L083 | wish: HMDA mortgage records | ripple_frontier_MASTER_LIST.md § Round 1 |
| LF-L084 | wish: NASA nighttime lights | ripple_frontier_MASTER_LIST.md § Round 1 |
| LF-L085 | wish: FEMA NFIP flood claims | ripple_frontier_MASTER_LIST.md § Round 1 |
| LF-L086 | wish: DoD 1033 police militarization | ripple_frontier_MASTER_LIST.md § Round 1 |
| LF-L087 | wish: FAA registrations + flight tracks | ripple_frontier_MASTER_LIST.md § Round 1 |
| LF-L088 | wish: FHWA National Bridge Inventory | ripple_frontier_MASTER_LIST.md § Round 1 |
| LF-L089 | wish: FMCSA carrier safety | ripple_frontier_MASTER_LIST.md § Round 1 |
| LF-L090 | wish: US Customs bills of lading | ripple_frontier_MASTER_LIST.md § Round 1 |
| LF-L091 | wish: OFAC sanctioned crypto wallets | ripple_frontier_MASTER_LIST.md § Round 1 |
| LF-L092 | wish: US foreign aid + AidData Chinese loans | ripple_frontier_MASTER_LIST.md § Round 1 |
| LF-L093 | wish: OONI internet-censorship measurements | ripple_frontier_MASTER_LIST.md § Round 1 |
| LF-L094 | wish: IPUMS full-count census 1850–1940 | ripple_frontier_MASTER_LIST.md § Round 2 |
| LF-L095 | wish: Chronicling America 20M newspaper pages | ripple_frontier_MASTER_LIST.md § Round 2 |
| LF-L096 | wish: SlaveVoyages + Freedmen's Bureau | ripple_frontier_MASTER_LIST.md § Round 2 |
| LF-L097 | wish: CDC WONDER mortality 1968–2016 | ripple_frontier_MASTER_LIST.md § Round 2 |
| LF-L098 | wish: FDA Orange Book | ripple_frontier_MASTER_LIST.md § Round 2 |
| LF-L099 | wish: USPTO PatentsView | ripple_frontier_MASTER_LIST.md § Round 2 |
| LF-L100 | wish: ClinicalTrials.gov + FDAAA TrialsTracker | ripple_frontier_MASTER_LIST.md § Round 2 |
| LF-L101 | wish: OpenAlex + Unpaywall | ripple_frontier_MASTER_LIST.md § Round 2 |
| LF-L102 | wish: FFIEC Summary of Deposits back to 1994 | ripple_frontier_MASTER_LIST.md § Round 2 |
| LF-L103 | wish: MSRB EMMA muni disclosures | ripple_frontier_MASTER_LIST.md § Round 2 |
| LF-L104 | wish: SEC Form 4 insider trades + 13F | ripple_frontier_MASTER_LIST.md § Round 2 |
| LF-L105 | wish: Public Plans Database | ripple_frontier_MASTER_LIST.md § Round 2 |
| LF-L106 | wish: NVDRS violent deaths | ripple_frontier_MASTER_LIST.md § Round 2 |
| LF-L107 | wish: NEMSIS 60M ambulance runs a year | ripple_frontier_MASTER_LIST.md § Round 2 |
| LF-L108 | wish: daily tract PM2.5 surfaces | ripple_frontier_MASTER_LIST.md § Round 2 |
| LF-L109 | wish: DOI ONRR royalties by company | ripple_frontier_MASTER_LIST.md § Round 2 |
| LF-L110 | wish: USGS NWIS groundwater | ripple_frontier_MASTER_LIST.md § Round 2 |
| LF-L111 | wish: BLM mining claims | ripple_frontier_MASTER_LIST.md § Round 2 |
| LF-L112 | wish: BLM General Land Office patents | ripple_frontier_MASTER_LIST.md § Round 2 |
| LF-L113 | wish: FCC political ad files | ripple_frontier_MASTER_LIST.md § Round 2 |
| LF-L114 | wish: Medill news-desert + Media Cloud | ripple_frontier_MASTER_LIST.md § Round 2 |
| LF-L115 | wish: EU DSA takedown database | ripple_frontier_MASTER_LIST.md § Round 2 |
| LF-L116 | wish: EOIR cases + ICE detention stays (parsed) | ripple_frontier_MASTER_LIST.md § Round 2 |
| LF-L117 | wish: 287(g) roster | ripple_frontier_MASTER_LIST.md § Round 2 |
| LF-L118 | wish: CBP/IOM border-death points | ripple_frontier_MASTER_LIST.md § Round 2 |
| LF-L119 | wish: ORR child-placement geography | ripple_frontier_MASTER_LIST.md § Round 2 |
| LF-L120 | wish: FCC broadband map | ripple_frontier_MASTER_LIST.md § Round 2 |
| LF-L121 | wish: InSAR land-subsidence rasters | ripple_frontier_MASTER_LIST.md § Round 2 |
| LF-L122 | wish: Census of Governments special districts | ripple_frontier_MASTER_LIST.md § Round 2 |
| LF-L123 | wish: FRA grade-crossing incidents | ripple_frontier_MASTER_LIST.md § Round 2 |
| LF-L124 | wish: OpenSanctions | ripple_frontier_MASTER_LIST.md § Round 3 |
| LF-L125 | wish: UK Companies House PSC (held now; listed as wish then) | ripple_frontier_MASTER_LIST.md § Round 3 |
| LF-L126 | wish: Global Fishing Watch encounters | ripple_frontier_MASTER_LIST.md § Round 3 |
| LF-L127 | wish: Paris MOU ship detentions | ripple_frontier_MASTER_LIST.md § Round 3 |
| LF-L128 | wish: First Street climate risk | ripple_frontier_MASTER_LIST.md § Round 3 |
| LF-L129 | wish: Climate Impact Lab county mortality | ripple_frontier_MASTER_LIST.md § Round 3 |
| LF-L130 | wish: WRI Aqueduct water futures | ripple_frontier_MASTER_LIST.md § Round 3 |
| LF-L131 | wish: Climate Central Billion-Dollar Disasters | ripple_frontier_MASTER_LIST.md § Round 3 |
| LF-L132 | wish: EFF Atlas of Surveillance | ripple_frontier_MASTER_LIST.md § Round 3 |
| LF-L133 | wish: leaked ShotSpotter sensor locations | ripple_frontier_MASTER_LIST.md § Round 3 |
| LF-L134 | wish: Palantir deployment corpus | ripple_frontier_MASTER_LIST.md § Round 3 |
| LF-L135 | wish: ICIJ Offshore Leaks graph | ripple_frontier_MASTER_LIST.md § Round 3 |
| LF-L136 | wish: FinCEN SAR Stats + GTO counties | ripple_frontier_MASTER_LIST.md § Round 3 |
| LF-L137 | wish: WY/NV/DE registered-agent data | ripple_frontier_MASTER_LIST.md § Round 3 |
| LF-L138 | wish: OPTN/SRTR transplant registry | ripple_frontier_MASTER_LIST.md § Round 3 |
| LF-L139 | wish: FDA plasma-center registry | ripple_frontier_MASTER_LIST.md § Round 3 |
| LF-L140 | wish: March of Dimes maternity deserts (AHRF) | ripple_frontier_MASTER_LIST.md § Round 3 |
| LF-L141 | wish: stadium bond issuances | ripple_frontier_MASTER_LIST.md § Round 3 |
| LF-L142 | wish: state cannabis license + sales | ripple_frontier_MASTER_LIST.md § Round 3 |
| LF-L143 | wish: lottery retailer + sales | ripple_frontier_MASTER_LIST.md § Round 3 |
| LF-L144 | wish: EIA-861 utility territories | ripple_frontier_MASTER_LIST.md § Round 3 |
| LF-L145 | wish: FERC Form 1 | ripple_frontier_MASTER_LIST.md § Round 3 |
| LF-L146 | wish: LBNL interconnection queue | ripple_frontier_MASTER_LIST.md § Round 3 |
| LF-L147 | wish: BIS Entity List | ripple_frontier_MASTER_LIST.md § Round 3 |
| LF-L148 | wish: TeleGeography submarine cables | ripple_frontier_MASTER_LIST.md § Round 3 |
| LF-L149 | wish: Epoch AI model/compute | ripple_frontier_MASTER_LIST.md § Round 3 |
| LF-L150 | wish: DOE Section 117 foreign gifts | ripple_frontier_MASTER_LIST.md § Round 3 |
| LF-L151 | wish: IRS DAF filings (Schedule D) | ripple_frontier_MASTER_LIST.md § Round 3 |
| LF-L152 | wish: IRS 527 filings (held now) | ripple_frontier_MASTER_LIST.md § Round 3 |
| LF-L153 | wish: FACA advisory-committee database | ripple_frontier_MASTER_LIST.md § Round 3 |
| LF-L154 | wish: OSC/MSPB whistleblower records | ripple_frontier_MASTER_LIST.md § Round 3 |
| LF-L155 | wish: SBA 8(a) Tribe/ANC flag | ripple_frontier_MASTER_LIST.md § Round 4 |
| LF-L156 | wish: Cobell Land Buy-Back ledger | ripple_frontier_MASTER_LIST.md § Round 4 |
| LF-L157 | wish: IJ Policing for Profit + DOJ equitable sharing | ripple_frontier_MASTER_LIST.md § Round 4 |
| LF-L158 | wish: CFPB complaints + prison-fintech enforcement | ripple_frontier_MASTER_LIST.md § Round 4 |
| LF-L159 | wish: WaPo Fatal Force ORI crosswalk | ripple_frontier_MASTER_LIST.md § Round 4 |
| LF-L160 | wish: Campaign Zero union-contract protections | ripple_frontier_MASTER_LIST.md § Round 4 |
| LF-L161 | wish: National Police Index | ripple_frontier_MASTER_LIST.md § Round 4 |
| LF-L162 | wish: FWS Section 7 Biological Opinions | ripple_frontier_MASTER_LIST.md § Round 4 |
| LF-L163 | wish: CITES trade database | ripple_frontier_MASTER_LIST.md § Round 4 |
| LF-L164 | wish: NOAA tide-gauge trends | ripple_frontier_MASTER_LIST.md § Round 4 |
| LF-L165 | wish: Oklahoma injection-well volumes | ripple_frontier_MASTER_LIST.md § Round 4 |
| LF-L166 | wish: dialysis facility file + reports | ripple_frontier_MASTER_LIST.md § Round 4 |
| LF-L167 | wish: MA prior-auth denial + overturn | ripple_frontier_MASTER_LIST.md § Round 4 |
| LF-L168 | wish: PEN America book-ban index | ripple_frontier_MASTER_LIST.md § Round 4 |
| LF-L169 | wish: 60 years of NEH/NEA/CPB grants | ripple_frontier_MASTER_LIST.md § Round 4 |
| LF-L170 | wish: Wikimedia pageviews + protection logs | ripple_frontier_MASTER_LIST.md § Round 4 |
| LF-L171 | wish: Virginia court dispositions 33.5M | ripple_frontier_MASTER_LIST.md § Round 5 |
| LF-L172 | wish: Cook County felony charges | ripple_frontier_MASTER_LIST.md § Round 5 |
| LF-L173 | wish: New York case-level bail | ripple_frontier_MASTER_LIST.md § Round 5 |
| LF-L174 | wish: Tyler Odyssey deployments 600+ counties | ripple_frontier_MASTER_LIST.md § Round 5 |
| LF-L175 | wish: Deportation Data Project | ripple_frontier_MASTER_LIST.md § Round 5 |
| LF-L176 | wish: House Epstein estate files | ripple_frontier_MASTER_LIST.md § Round 5 |
| LF-L177 | wish: EDGI rescued EJScreen/CEJST | ripple_frontier_MASTER_LIST.md § Round 5 |
| LF-L178 | wish: NYC Class-C violations by owner | ripple_frontier_MASTER_LIST.md § Round 5 |
| LF-L179 | wish: Cook County scavenger tax sale | ripple_frontier_MASTER_LIST.md § Round 5 |
| LF-L180 | wish: State AG multistate roster | ripple_frontier_MASTER_LIST.md § Round 5 |
| LF-L181 | wish: State False Claims Act recoveries | ripple_frontier_MASTER_LIST.md § Round 5 |
| LF-L182 | wish: Delaware licensing-board discipline | ripple_frontier_MASTER_LIST.md § Round 5 |
| LF-L183 | wish: FracFocus | ripple_frontier_MASTER_LIST.md § Round 5 |
| LF-L184 | wish: EPA UST/LUST | ripple_frontier_MASTER_LIST.md § Round 5 |
| LF-L185 | wish: EU procurement / Opentender | ripple_frontier_MASTER_LIST.md § Round 5 |
| LF-L186 | wish: IATI aid flows | ripple_frontier_MASTER_LIST.md § Round 5 |
| LF-L187 | wish: World Bank debt-by-creditor | ripple_frontier_MASTER_LIST.md § Round 5 |
| LF-L188 | Frontier list: 137 datasets across 5 rounds, 2026-06-30 → 07-01; pairings live in per-round briefs | ripple_frontier_MASTER_LIST.md § header |
| LF-L189 | Registry domain counts: economy 108; housing 101; transport 91; corporate 89; education 86; science 73; justice 68; government 67; energy 60; politics 58; spending 50; history 37; crime 33; unclassified 418 | ripple_pitch_deck.md § What I built |
| LF-L190 | ~1,400 hand SQL, 309 Python, 1,400 YAML; one person, ~40 days this version | ripple_pitch_deck.md § What I built |
| LF-L191 | Hiring-manager skills list: 875M-row warehouse; 1,378 dbt models; ETL with atomic loads; graph entity resolution; temporal SQL | ripple_pitch_deck.md § hiring manager |
| LF-L192 | HMDA reload cost ~$2; prior 19M slice ~$0.80 over 125 statements | news_corroboration_map § Cost |
| LF-L193 | Statute glosses: 1128a1 program-related crime; 1128a2 patient abuse/neglect; 1128b7 fraud/kickbacks | frank_investigation; pharma_paid_excluded |
| LF-L194 | Frank's 22-row antipsychotic book listed in full; Invega Trinza 14 claims $110,556 | frank_investigation § Step 3 |
| LF-L195 | Miranda specialty differs: LEIE Internal Medicine, PECOS Hem/Onc, Part D Internal Medicine | ghost_ownership § Specialty discrepancy |
| LF-L196 | Miranda appears in 18 tables, listed | ghost_ownership § 18 tables |
| LF-L197 | Skye's 30 write-offs listed in full with NPI, entity, state, amount, date | molina § All 30 write-offs |
| LF-L198 | Fadi Jaafar twice, $187,800 combined | molina § pattern |
| LF-L199 | DME family prefixes: TOT_, DME_, POS_, DRUG_; 99 columns; 381,228 rows | frank_dme § source |
| LF-L200 | Specialties above Frank on services/bene: urology 2,894; NP 2,879; pulmonary 2,301 | frank_dme § who sits above |
| LF-L201 | Reading Room: http://127.0.0.1:8890; reads on RIPPLE_READER via SNOWFLAKE_SERVE_PAT; writes on RIPPLE_REVIEW_WRITER | HOUR_DOSSIER § 1 |
| LF-L202 | Tiers: FACT_GRADE_3_SOURCE, NPPES_CONFLICT, LEIE_ROW_MISSING; timelines PAID_ON_OR_AFTER_EXCLUSION, PAYMENTS_PREDATE_EXCLUSION | HOUR_DOSSIER § 4; § 7 |
| LF-L203 | Done = V_STATE decisions.total ≥ 10; then export decisions to git | HOUR_DOSSIER § 9 |
| LF-L204 | Detector batch detected 2026-06-26→28; queue mart recomputes fresh, never trusts capped evidence | HOUR_DOSSIER § 5 |
| LF-L205 | Warehouse shelf: 5.7M UK companies; 3.4M LEIs; 814k offshore entities; 2.0M exempt orgs; 9.6M providers; 3.3M EPA facilities; 16k judges | warehouse_capabilities § What's inside |
| LF-L206 | Events shelf: 179M pill shipments; 84M contributions; 43M pharma payments; 72M dockets; 37M adverse events; 15M water violations; 12.6M immigration cases | warehouse_capabilities § What's inside |
| LF-L207 | Receipts: reports/noun_event_inventory_2026-08-18.md; reports/census_grid_2026-08-12/ | warehouse_capabilities § footer |
| LF-L208 | Frank hospice thread: Part B holds 1,099 nursing facility visits and 762 residence visits — the panel really is that population | frank_hospice § load-bearing unknown |
| LF-L209 | Censoring cuts both ways on the recert measure: low-volume vanish (flatters), low-cert high-recert drop (damns) | frank_hospice § censoring |
| LF-L210 | Skeptic pass found 14 disagreements on the news map; 8 fixed | news_corroboration_map § Skeptic pass |
| LF-L211 | Corroboration queries ~60; ARCOS 178M and FEC 84M largest scans | news_corroboration_map § Cost |
| LF-L212 | "Not one procedure. Not one test." Frank's Part B is visits, care plans, certifications | frank_investigation § Step 1 |
| LF-L213 | THE_SCRIPT is a pull-from bank, not one block; general-adult reading level | THE_SCRIPT § header |
| LF-L214 | Portfolio: 75 finished tables rebuilt in a week; every table's reliability documented | THE_SCRIPT § 3 |
