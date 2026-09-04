# Network centrality hunt — the quiet middleman
2026-09-03. Python door only (connect/db.py). Read-only. networkx 3.x installed this session.

## Verdict, Graph 1 (schema grain)
**FED_SAM_EXCLUSIONS_FULL_R2 is the one table holding the health world and the corporate/money world together — in the graph the edge builder has wired.**
Scope: the graph covers 235 of 2,208 LANDING tables (10.6%). Everything below is about those 235.
HARD graph: degree rank 61 of 171, betweenness rank 1, removal cuts off 49 tables. Entity-keys-only graph: degree rank 60 of 99, betweenness 0.505 rank 1, removal cuts off 48. Union with CONNECT_EDGES_INC: still rank 1 (0.498), degree rank 61, cuts off 50.
It is the only table with BUILT edges on both a doctor id (NPI) and a company id (UEI / DUNS). By column name, FED_CMS_NPPES also carries EIN and parent TIN columns — no EIN edge was ever built for it. Whether those columns are populated is a gated 9.6M-row check. If they are, SAM's monopoly is partly an artifact of what got wired.
**The crossing is hairline: 180 matched UEIs wide** (USAspending contracts 104, assistance 53, SBIR 14, Single Audit 3, two conf-0.22 bridge edges of 3 each), once SAM's own older snapshot is excluded. Require MATCHED ≥ 500 and the bridge vanishes; it survives at ≥ 100.
Betweenness 0.505 and "cuts off 48" are the same fact: 51 × 48 / C(98,2) = 51.5% of pairs must route through a single cut node. One test, not two.
Plain words: the federal debarment list. Who is banned from federal business. Doctors get banned (NPI), companies get banned (UEI). Same list, both ids.

Skeptic pass run 2026-09-03 (fresh context, given Chris's words). Verdict: agree on the headline; scope and thinness were understated in draft 1. All eight of its findings are folded into this version. The skeptic's own re-run of cent_g1b.py reproduced every number.

## Rule break, owned
The probe step ran 4 statements over ENTITY_XREF (2.67M rows) — three aggregates and one SAMPLE — before any price was shown. That broke the 1M-row gate.
Price after the fact: 41 past ENTITY_XREF runs, p50 $0.00, max $0.00 at the default $2/credit rate. Cheap, still a break.
Graph 2 is now gated properly: script written, not run.

## Proving the graph is real

### 1. Nodes, edges, components — CONNECT_EDGES (4,512 rows)
| variant | edge rows | nodes | unique pairs | components | largest | next sizes |
|---|---|---|---|---|---|---|
| ALL keys | 4,512 | 235 | 4,175 | 6 | 212 | 10, 6, 3, 2, 2 |
| HARD (no NAME@ZIP) | 2,000 | 209 | 1,911 | 8 | 171 | 11, 10, 6, 4, 3, 2, 2 |
| NAME@ZIP only | 2,512 | 114 | 2,512 | 2 | 111 | 3 |
| ENTITY keys only (also drop GEO_IN, FIPS, ZIP) | 1,860 | 184 | 1,780 | 12 | 99 | 40, 11, 10, 6, 4, 3, 3, 2, 2 |

Not a hairball, not confetti: one big component with real internal structure. Middlemen can exist here.
Components in the entity-key graph, by prefix: comp0 = 47 CMS + 18 SEC + 8 IRS + 6 OSHA (the health+money world, 99 tables). comp1 = 33 EPA + 3 CFPB + 2 GLEIF (environment+banking, 40 tables). comp2 = 11 FEC. comp3 = 10 CourtListener. comp4 = Congress/Voteview/GovInfo. comp5 = 4 NCUA.
The health+money world and the environment world DO NOT TOUCH on any entity key. They touch only through geography (GEO_IN, FIPS) and names (NAME@ZIP).

### 2. Value check on the id columns
Graph 1 node ids are table names: 216 distinct A, 213 distinct B, sample rows all real LANDING tables. OK.
The winner's key columns, FED_SAM_EXCLUSIONS_FULL_R2 (168,328 rows):
| column | non-blank rows | distinct | note |
|---|---|---|---|
| NPI | 19,238 | 4,867 | **12,027 rows are '0000000000'** — sentinel, not an id. Real: ~7,200 rows, 4,866 distinct |
| UNIQUE_ENTITY_ID | 47,686 | 38,427 | real UEIs |
By CLASSIFICATION: Individual 133,131 rows (19,026 with NPI, 13,502 with UEI); Special Entity Designation 25,584; Firm 8,291; Vessel 1,322.
Reproducibility: these three counts were run this session; the first draft of cent_sam.py had them stripped after they ran. Restored — the delivered script now produces every number in this table.
The edge to NPPES: 4,854 of 4,866 distinct SAM NPIs match, 99.8%, STEEL tier, confidence 0.999. The sentinel cannot fake a table-level edge; one junk value adds at most 1 to a match count of 4,854.
The edge to LEIE (HHS exclusion list): 4,687 match, 96.3%. Expected — HHS exclusions flow into SAM.
UEI edges: SAM_EXCLUSIONS (older copy) 3,209 at 100%; USAspending contracts 104; USAspending assistance 53; SBIR 14; Single Audit 3.
The UEI side is thin (104 and 53 matches) but real: banned companies that also hold federal awards.

### 3. Name-collision guard
2,512 of 4,512 edge rows (56%) are NAME@ZIP. Split out above. All findings below use the HARD or ENTITY-only graphs.
NAME@ZIP alone connects 111 tables into one blob; it makes everything look connected to everything. That is the collision effect at graph scale.
In the ALL graph the top betweenness nodes are FEC individual contributions, EPA water systems, EPA facilities — all name-driven, all high degree (76–115). No gap, no middleman. Names wash the signal out.

### 4. Junk-hub check — geography
GEO_IN edges are point-in-polygon, not identity. Three polygon tables score high on betweenness in the HARD graph purely because every US lat/lon falls inside them:
| polygon table | rows | GEO_IN degree | match rate into it | verdict |
|---|---|---|---|---|
| INTL_FR_DATA_GOUV_FULL | 130,431 | 19 | **100.0%** of nursing homes, colleges, plants, air sites | junk hub — French open data cannot contain 100% of US points; a world-sized shape |
| FED_MAPPING_INEQUALITY | 10,154 | 19 | 2.7–17% | real HOLC redlining polygons; geographic, not entity |
| FED_NOAA_WEATHER_API | 287 | 16 | 0.2% | 287 rows; geographic noise |
Dropped from the finding. Flagged as a trap.
Graph 2 junk-hub check (FANOUT) is gated with the Graph 2 run. Already visible without a scan: the FANOUT column is a per-source constant (6,962 on all 2.25M CCN→NPI rows, 821 on all FEC rows), NOT a per-value fanout. Real fanout must be recomputed.

## The math
networkx 3.x. Exact betweenness (normalized) on the largest component; graph is 171 nodes, 1,802 edges — well under the 50K threshold. Degree alongside. Greedy modularity communities for cluster names. Articulation points as the hard test: removing the node disconnects the graph.

## Ranking — HARD graph, largest component (171 nodes)
Gap = degree rank minus betweenness rank. Positive gap = quiet middleman.
| node | btw | b# | deg | d# | gap | rows | keys | bridges |
|---|---|---|---|---|---|---|---|---|
| FED_SAM_EXCLUSIONS_FULL_R2 | 0.4128 | 1 | 27 | 61 | +60 | 168,328 | NPI 20, UEI 5, EIN~UEI, DUNS~UEI | CMS(51) 20 edges ↔ SEC/IRS/spending(49) 7 edges |
| FED_EPA_TRI_BASIC_2023 | 0.2576 | 2 | 19 | 91 | +89 | 78,647 | FRS_ID 16, GEO_IN 3 | inside EPA only; geo lifts it |
| FED_NURSINGHOME411 | 0.2566 | 3 | 36 | 25 | +22 | 14,713 | CCN~NPI 26, CCN 7, GEO_IN 3 | CMS ↔ EPA via GEO only |
| FED_CMS_NURSING_HOME | 0.2280 | 4 | 31 | 39 | +35 | 14,700 | CCN~NPI 21, CCN 7, GEO_IN 3 | CMS ↔ EPA via GEO only |
| INTL_FR_DATA_GOUV_FULL | 0.1986 | 5 | 19 | 93 | +88 | 130,431 | GEO_IN 19 | junk geo hub |
| FED_MAPPING_INEQUALITY | 0.1872 | 6 | 19 | 94 | +88 | 10,154 | GEO_IN 19 | geo, not entity |
| FED_NOAA_WEATHER_API | 0.1641 | 7 | 16 | 105 | +98 | 287 | GEO_IN 16 | geo noise |
| FED_EPA_ECHO | 0.1051 | 8 | 34 | 33 | +25 | 3,157,891 | FRS_ID 16, FIPS 12, PWSID 9 | EPA core ↔ SDWA water(9) — articulation point |
| FED_USASPENDING_ASSISTANCE_FULL | 0.0878 | 9 | 28 | 60 | +51 | 19,902,879 | EIN~UEI 22, UEI 6 | money side of the SAM bridge |
| FED_IRS_990_EFILE_INDEX | 0.0863 | 10 | 27 | 62 | +52 | 5,544,626 | EIN 22, EIN~UEI 5 | nonprofit side |
| FED_FAC_SINGLE_AUDIT | 0.0863 | 11 | 27 | 64 | +53 | 411,638 | EIN 22, UEI 5 | EIN ↔ UEI translator |
| FED_NIH_REPORTER | 0.0762 | 12 | 25 | 75 | +63 | 2,122,611 | EIN~UEI 19, UEI 4, DUNS | EIN ↔ UEI translator |
| XC_EPA_CORPORATE_CROSSWALK | 0.0685 | 13 | 22 | 82 | +69 | 5,300,149 | FRS_ID 16, LEI 6 | EPA facilities ↔ GLEIF/LEI(6) — articulation point |
| FED_PCAOB_FORM_AP_FILINGS | 0.0264 | 23 | 32 | 37 | +14 | 155,384 | CIK 18, CIK~EIN 14 | CIK world ↔ EIN world |
| FED_CMS_NPPES | 0.0282 | 19 | 50 | 1 | -18 | 9,606,683 | NPI 33 | the biggest hub, NOT a middleman |

Articulation points, HARD graph (9): SAM_EXCLUSIONS_FULL_R2 splits off 49; EPA_ECHO splits off 9 (the SDWA water tables); XC_EPA_CORPORATE_CROSSWALK splits off 6 (the LEI/GLEIF tables); ED_COLLEGE_SCORECARD 3; NSF_AWARDS 2; ICE_DETENTION_FACILITY_CODES 2; FDIC_BANK_DATA 1; EIA860_1_UTILITY 1; INTL_FR_DATA_GOUV 1.

## Ranking — ENTITY keys only (99-node component), the clean run
| node | btw | b# | deg | d# | gap |
|---|---|---|---|---|---|
| FED_SAM_EXCLUSIONS_FULL_R2 | 0.5050 | 1 | 27 | 60 | +59 |
| FED_USASPENDING_ASSISTANCE_FULL | 0.1123 | 2 | 28 | 59 | +57 |
| FED_IRS_990_EFILE_INDEX | 0.1081 | 3 | 27 | 61 | +58 |
| FED_FAC_SINGLE_AUDIT | 0.1081 | 4 | 27 | 63 | +59 |
| FED_NIH_REPORTER | 0.0966 | 5 | 25 | 71 | +66 |
| FED_PCAOB_FORM_AP_FILINGS | 0.0454 | 6 | 32 | 36 | +30 |
| FED_CMS_NPPES | 0.0298 | 7 | 50 | 1 | -6 |
| FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT | 0.0295 | 8 | 49 | 2 | -6 |
| FED_CMS_PECOS_PROVIDER_ENROLLMENT | 0.0295 | 9 | 49 | 3 | -6 |
| IRS527_DIRECTORS_OFFICERS | 0.0285 | 10 | 32 | 35 | +25 |
| FED_CMS_FACILITY_AFFILIATION | 0.0267 | 11 | 49 | 4 | -7 |
| FED_DOL_EBSA_FORM5500_SCHEDULE_SB | 0.0228 | 12 | 35 | 29 | +17 |
| FED_PBGC_TRUSTEED_PENSION_PLANS | 0.0228 | 13 | 35 | 30 | +17 |
| IRS527_8871_ORGS | 0.0227 | 14 | 31 | 37 | +23 |
| FED_USASPENDING_CONTRACTS | 0.0226 | 15 | 12 | 88 | +73 |
Full top 15, nothing omitted. Articulation points: SAM_EXCLUSIONS_FULL_R2 (splits off 48), PCAOB_FORM_AP_FILINGS (splits off 2).

## Robustness — the newer edge table
CONNECT_EDGES is one full-discover run, 2026-08-28, 4,512 rows. CONNECT_EDGES_INC is the incremental builder's on-land edges, 19 runs from 2026-07-01 to 2026-08-31, 3,455 rows; 2,797 of its (A,B,KEY) triples are not in CONNECT_EDGES. It also carries bare NAME (492) and ADDRESS (127) keys — the 8%-real collision class — plus ZIP (993).
Union of both, soft keys dropped (NAME@ZIP, NAME, ADDRESS, ZIP, FIPS, GEO_IN, SIC, COUNTRY): 212 nodes, largest component 114.
| node | btw | b# | deg | d# | gap |
|---|---|---|---|---|---|
| FED_SAM_EXCLUSIONS_FULL_R2 | 0.4979 | 1 | 27 | 61 | +60 |
| FED_DOL_FORM5500 | 0.2280 | 2 | 48 | 5 | +3 |
| FED_USASPENDING_ASSISTANCE_FULL | 0.1215 | 3 | 29 | 53 | +50 |
| FED_FAC_SINGLE_AUDIT | 0.1172 | 4 | 28 | 60 | +56 |
| FED_NIH_REPORTER | 0.1089 | 5 | 26 | 67 | +62 |
| FED_IRS_990_EFILE_INDEX | 0.1085 | 6 | 27 | 62 | +56 |
| FED_PCAOB_FORM_AP_FILINGS | 0.0395 | 7 | 32 | 36 | +29 |
Articulation: SAM cuts off 50, FORM5500 cuts off 12, PCAOB 2. SAM is still the only node with both health and corporate keys. The finding does not depend on which edge table you pick.
Half of all shortest paths in the health+money world run through the debarment list. Betweenness 0.505.

## The findings, four lines each

### 1. FED_SAM_EXCLUSIONS_FULL_R2 — the debarment list
what it is: 168,328 exclusion records from SAM.gov, GSA. 4,866 real NPIs, 38,427 UEIs.
what it bridges: the CMS cluster (51 tables: NPPES, PECOS, Part D, Open Payments, facility affiliation) and the SEC/IRS/spending cluster (49 tables: USAspending, NIH, Single Audit, 990s, PCAOB, Form 5500). No other table carries both key types.
why it is quiet: degree 27, rank 60 of 171. Betweenness rank 1, score 0.51 in the clean graph. Gap +59. Removing it disconnects 48 tables.
plain words: the government's banned list. The only place a doctor's license number and a contractor's registration number sit in the same row.
chain: checked = keys per node in CONNECT_EDGES, intersected health keys {NPI, CCN} with corporate keys {EIN, UEI, CIK, LEI, DUNS}. hit = exactly one table has both. a miss would have meant several bridges and no single middleman. Also checked = NPI column distinct+sample: 12,027 zero-sentinels found and discounted; 4,854/4,866 real match to NPPES.

### 2. FED_FAC_SINGLE_AUDIT — the EIN-to-UEI translator
what it is: Federal Audit Clearinghouse, 411,638 single-audit records. Carries auditee EIN and auditee UEI on one row.
what it bridges: the EIN world (IRS 990, BMF, Form 5500, PCAOB) and the UEI world (USAspending, NIH, SBIR, SAM). EIN~UEI composite edges exist because tables like this one hold both.
why it is quiet: degree 27, rank 63. Betweenness rank 4, gap +59. 411K rows next to USAspending's 19.9M.
plain words: the audit filings that nonprofits and local governments send in when they spend federal grants. Both id numbers on the form.

### 3. FED_NIH_REPORTER — same translator, research side
what it is: 2,122,611 NIH grant records. EIN, UEI and DUNS on the same row.
what it bridges: universities and hospitals (EIN, 990) to federal award ids (UEI, USAspending). DUNS~UEI edges make it the legacy-id translator too.
why it is quiet: degree 25, rank 71. Betweenness rank 5, gap +66.
plain words: the grant ledger that happens to carry three different company id systems side by side.

### 4. FED_PCAOB_FORM_AP_FILINGS — the CIK-to-EIN hinge
what it is: 155,384 auditor Form AP filings. Issuer CIK and EIN together.
what it bridges: SEC filer world (CIK: DERA, 13F, EDGAR) to the tax-id world (EIN: IRS, DOL, pension). Articulation point: removing it strands 2 tables.
why it is quiet: degree 32, rank 36; betweenness rank 6, gap +30. Smaller gap, still real.
plain words: the form that says which accounting firm audited which public company. Two id systems, one form.

### 5. XC_EPA_CORPORATE_CROSSWALK — the facility-to-parent hinge
what it is: 5,300,149 rows crosswalking EPA facility ids (FRS_ID) to legal-entity ids (LEI).
what it bridges: the EPA facility world (33 tables) to GLEIF/ISO legal entities (6 tables). Articulation point: remove it and 6 tables fall off.
why it is quiet: degree 22, rank 82; betweenness rank 13, gap +69.
plain words: the lookup from a smokestack to the company that owns it. It is the ONLY link from environment to corporate ownership, and it is a warehouse-built XC table, not a federal source.

### 6. FED_EPA_ECHO — the water hinge
what it is: 3,157,891 enforcement and compliance records. Carries FRS_ID, FIPS and PWSID.
what it bridges: EPA facility world to the SDWA drinking-water cluster (9 tables). Articulation point for those 9.
why it is quiet: degree 34, rank 33; betweenness rank 8, gap +25.
plain words: the enforcement history file, which happens to also list the water-system id. Drop it and drinking water is an island.

### 7. IRS527_DIRECTORS_OFFICERS — the political-money hinge
what it is: 189,593 directors and officers of Section 527 political organizations. EIN of the org on every row.
what it bridges: 527 political groups (IRS side) to the EIN world of 990s, BMF, Form 5500, and by CIK~EIN to SEC filers. 3 CIK~EIN edges.
why it is quiet: degree 32, rank 35; betweenness rank 10, gap +25.
plain words: the roster of who runs dark-money political groups, keyed on the same tax id the rest of the warehouse uses.

### 8. FED_DOL_EBSA_FORM5500_SCHEDULE_SB — pension actuarial hinge
what it is: 41,802 Schedule SB actuarial filings. Sponsor EIN; CIK~EIN and EIN~UEI edges.
what it bridges: defined-benefit pension plans to SEC filers (CIK) and to federal awardees (UEI).
why it is quiet: degree 35, rank 29; betweenness rank 12, gap +17. Only 41K rows.
plain words: the pension health form. Small file, sits on the path from a company's stock filings to its retirement plan.

### 9. FED_PBGC_TRUSTEED_PENSION_PLANS — failed pensions
what it is: 21,596 plans taken over by the Pension Benefit Guaranty Corporation. Sponsor EIN.
what it bridges: same path as Schedule SB — CIK~EIN and EIN~UEI. Identical scores because it shares the same neighbor set.
why it is quiet: degree 35, rank 30; betweenness rank 13, gap +17. 21K rows.
plain words: the list of pensions that went bust and the government picked up. Its tax ids happen to tie into three worlds.

### 10. IRS527_8871_ORGS — the 527 registrations
what it is: 77,591 Form 8871 registrations of political organizations. EIN.
what it bridges: same as #7, the org-level twin of the directors table.
why it is quiet: degree 31, rank 37; betweenness rank 14, gap +23.
plain words: the sign-up form for a political money group.

Findings 7–10 share one mechanism: EIN is the warehouse's common currency, and any smallish table with EIN plus one other id system (CIK, UEI) becomes a short cut between worlds. That is a structural fact about the graph, not ten separate discoveries.

Ten findings delivered against the 10–15 asked. The graph's largest clean component is 99 nodes; past rank 15 the betweenness scores fall under 0.02 and the gaps stop meaning anything.

### Discounted, and why
| node | reason |
|---|---|
| INTL_FR_DATA_GOUV_FULL, FED_MAPPING_INEQUALITY, FED_NOAA_WEATHER_API | GEO_IN containment, not identity; the French table swallows 100% of US points |
| FED_NURSINGHOME411, FED_CMS_NURSING_HOME | their cross-cluster edges are all GEO_IN; on entity keys they sit inside CMS |
| FED_EPA_TRI_BASIC_2023 | inside EPA only; geo lifts it; vintage copy |
| FED_CMS_NPPES, PECOS, FFS enrollment, facility affiliation | degree ranks 1–4, negative gap; hubs not middlemen |
| FED_ED_COLLEGE_SCORECARD, FED_NSF_AWARDS, FED_ICE_DETENTION_FACILITY_CODES | articulation points only via ZIP/GEO; ZIP is geography |

## Cross-check against BRIDGE_ENTITIES
BRIDGE_ENTITIES is entity grain (53,795 organizations, 4 vessels), DOMAIN_COUNT max 3, and every DOMAIN_COUNT=3 row is the same triple: corporate_entities + economy_labor_trade + spending_budget, sourced from IRS BMF, 990 e-file, Single Audit, Form 5500.
Graph 1 is table grain; the two do not overlap by construction. But apply Chris's rule anyway — "if your betweenness winners are just its top DOMAIN_COUNT rows, you found nothing new":
| finding | in BRIDGE_ENTITIES' source set? | verdict |
|---|---|---|
| 1 SAM_EXCLUSIONS | no — SAM is 79% Individuals, BRIDGE_ENTITIES is organization-only | **new** |
| 2 FAC_SINGLE_AUDIT | yes, one of its four sources | rediscovery |
| 3 NIH_REPORTER, 990 EIN~UEI | 990 e-file yes | rediscovery |
| 4 PCAOB, 5 XC_EPA_CROSSWALK, 6 EPA_ECHO | no — CIK, LEI, PWSID worlds | new |
| 7–10 IRS527, Form5500 SB, PBGC | Form 5500 yes; 527 and PBGC no | mixed |
Only the SAM finding cleanly passes the cross-check. Findings 2 and 3 are the EIN↔UEI translators BRIDGE_ENTITIES already knows.

## Graph 2 — run after "go", 2026-09-03

### NPPES gate result: SAM's monopoly is real
FED_CMS_NPPES.EMPLOYER_IDENTIFICATION_NUMBER_EIN: 1,937,362 populated rows, ONE distinct value, '<UNAVAIL>'. PARENT_ORGANIZATION_TIN: 156,566 populated, one distinct value, '<UNAVAIL>'. Every type-2 org row carries the placeholder; every type-1 individual row is blank. Join to IRS BMF: 0 hits both columns.
CMS redacts the EIN in the public NPPES file. The column exists; the id does not. No second health↔money bridge is hiding in NPPES. Trap recorded.

### Graph 2 shape
2,672,384 XREF rows → distinct pairs pulled, six disjoint key families as predicted. After junk drop:
| component | key family | nodes | edges | shape |
|---|---|---|---|---|
| 0 | CCN ↔ NPI | see rerun below | | bipartite, hospital ↔ physician |
| 1 | FEC_CAND_ID ↔ FEC_CMTE_ID | 11,021 largest of 28,379 | 203,108 total | bipartite, PAC gave to candidate |
| 2+ | LEI ↔ FRS_ID | 22,736 stars, biggest 609 | n−1 each | pure stars, one family |
Betweenness: exact on the FEC component (11,021 nodes, pure-python, 13 min wall clock). Sampled k=300 on the hospital component, then replaced by the block-cut tree — see below.

### FEC family — the three PACs that fund long-shots
Edge = a committee gave to a candidate (FED_FEC_COMMITTEE_TO_CANDIDATE). Names from FED_FEC_CANDIDATES (headerless, C1=id, C2=name, C3=party, C6=office) and FINANCE__FED_FEC_COMMITTEES_DIM per the committees trap.
Draft 1 of this table came from the cut-500 run, which had deleted 516 of the highest-degree FEC nodes, WinRed among them. The skeptic caught it. This table is the clean graph, no size cut, EXACT betweenness, script cent_fec.py, output fec_out.json and fec.log.
| node | name | btw | b# | deg | d# | gap | med cand deg | IS_AMBIGUOUS |
|---|---|---|---|---|---|---|---|---|
| C00694323 | WINRED | 0.0963 | 1 | 623 | 19 | +18 | 54 | 0 |
| P00009423 | HARRIS, KAMALA D. | 0.0388 | 2 | 470 | 84 | +82 | — | — |
| P80001571 | TRUMP, DONALD J. | 0.0236 | 3 | 317 | 276 | +273 | — | — |
| C00027342 | IBEW PAC | 0.0225 | 4 | 389 | 158 | +154 | 145 | 1 |
| **C00545202** | **Center for Freethought Equality PAC** | 0.0184 | 5 | 109 | 1,007 | **+1,002** | **4** | 1 |
| S6OH00163 | BROWN, SHERROD | 0.0150 | 6 | 755 | 5 | −1 | — | — |
| C00252940 | League of Conservation Voters Action Fund | 0.0141 | 7 | 339 | 233 | +226 | 164 | 0 |
| **C00720649** | **Reform Leaders PAC** | 0.0131 | 8 | 66 | 1,471 | **+1,463** | **4** | 1 |
| S2WI00219 | BALDWIN, TAMMY | 0.0125 | 9 | 646 | 16 | +7 | — | — |
| **C00630012** | **Every State Blue** | 0.0119 | 10 | 49 | 1,795 | **+1,785** | **2** | 1 |
| C00002089 | CWA COPE | 0.0118 | 11 | 305 | 295 | +284 | 182 | 1 |
| P80000722 | BIDEN, JOSEPH R JR | 0.0102 | 16 | 143 | 808 | +792 | — | — |
| C00030718 | National Association of Realtors PAC | 0.0096 | 18 | 586 | 31 | +13 | 252 | 0 |
Ranks 12–15, 17, 20 are House and Senate candidates with degree 600–780 and negative gaps: hubs. Rank 19, Calvert, gap +2, same shape.

Mechanism, checked three ways.
First guess was cross-party giving. Wrong. Party mix reconciled to degree (cent_party.py, party.log): Freethought degree 109 = 64 DEM, 0 REP, 4 other, 41 candidates with no row in the candidates file. Reform Leaders degree 66 = 6 DEM, 48 REP, 1 other, 11 not in the file. The "0 REP" stands on the 68 that have a party on file; the 41 missing could be anything, and that is said here rather than hidden.
Second: candidate degree = number of distinct committees that gave to that candidate. Median over each PAC's candidates: Freethought 4, Reform Leaders 4, Every State Blue 2; IBEW 145, LCV 164, CWA 182, Realtors 252.
Third, the discriminating control: every committee with degree 50–120 — 695 of them. Three are in the betweenness top 100; 692 are not. Every State Blue, degree 49, sits just outside the band and is NOT one of the three.
| group | committees | medians of median candidate degree | mean candidates with ≤3 donors |
|---|---|---|---|
| in betweenness top 100 | 3 | 4, 4, 255 | 30.7 |
| not in top 100 | 692 | median 351, minimum 74 | 0.3 |
Hit: two of the three band committees that rank — Freethought and Reform Leaders — have median 4; the third sits at 255 and ranks for some other reason, unexamined. The stronger direction: no committee in the band with median candidate degree under 74 fails to rank. Long-shot funding is sufficient to put a small PAC in the top 100; it is not the only way in.
Miss would have looked like: some of the 692 also sitting near median 4 without ranking. None do; the floor is 74.
The first draft of this paragraph said "three of three." Two of three, plus an unnamed third at 255. Caught by the skeptic.
Plain words: a tiny atheist PAC, a tiny reform PAC and a tiny Democratic PAC bet on long-shots. Cut them out and dozens of candidates have no path to the rest of the money graph.
Caveat: all three carry IS_AMBIGUOUS=1 in the dim — type/party/name conflicts across cycles. The ids are stable; the labels are not.
Also true: WinRed at rank 1 is the obvious one. It processes donations for most Republican candidates, degree 623 but degree rank 19 — a hub with a modest gap, not quiet.

### LEI family — stars, no middleman by construction
Clean pull, no size cut: 96,684 nodes, 22,736 components, and ZERO facilities touching more than one LEI. Every component is a star. Betweenness 1.0 at the hub, 0.0 at every spoke, degree rank 1 — gap zero, everywhere.
Draft 1 listed four stars of 279–348 and missed the biggest; the cut-500 pass had deleted its hub. Corrected:
| LEI | name | facilities |
|---|---|---|
| 549300S5TW3VP5V06B73 | Atlantic City Electric Company | 608 |
| 254900SWFR3KS9HI2W07 | Texas Department of Transportation | 348 |
| 7NKTFWJ1G6MELP9TU740 | Consumers Energy Company | 301 |
| 549300OVVD7Z46FDMX80 | Walgreen Co. | 299 |
| 549300I645G0USPS4266 | 99 Cents Only Stores LLC | 279 |
| GA3JGKJ41LJKXDN23E90 | AutoZone, Inc. | 231 |
| 7ZW8QJWVPR4P1J1KQY45 | Google LLC | 225 |
| 5493005JBO5YSIGK1814 | Phillips 66 | 209 |
A parent→child crosswalk cannot have a middleman; nothing to find here, and that is the finding.

### First hospital run — discarded, and why
The first pass dropped every value with fanout ≥ 500 as "junk". That removed every large hospital, and the top betweenness nodes came out at degree 470–492 — hospitals sitting right under the knife. The cutoff manufactured the winners. Trap recorded.
Second pass, junk = blanks/zeros/'<UNAVAIL>'/N-A or fanout ≥ 5,000: that still dropped six real hospitals by size (360180, 220110, 220071, 100007, 330214, 390111). Owned. Component 0 came out 997,651 nodes, 2,245,712 edges, k=300 sampled betweenness. Top 200 by betweenness were all hospitals, degree 311–4,715, gaps from −164 to +1,876 (86 of 200 under degree 1,500; 77 of 200 with gap over 170). The first draft of this line said "degree 1,500–4,700, gaps under 170" — wrong, caught by the skeptic; the second draft said "−11", also wrong, caught again. Some of those hospitals do carry a quiet-middleman gap signature by Chris's rule; the block-cut pass below shows what they actually cut off: their own exclusive staff. The top physicians sat at rank 233–242 with near-identical scores, 0.003350 down to 0.003335, which is what one sampled source's path count looks like, not a ranking. Sampled betweenness on a million nodes cannot see a degree-2 bridge. So the third pass drops sampling entirely.
What that switch costs, said plainly: cut size only sees a node whose removal DISCONNECTS. A physician carrying 90% of the paths between two systems, with one redundant back road, scores zero here and would have scored high on true betweenness. That class is unsearched in this report. Exact betweenness on a million nodes is not computable in this session; the honest position is "the disconnecting bridges are found, the near-bridges are not."

### Hospital family, the hard test — block-cut tree, no sampling, no size cut
Graph: every CCN↔NPI pair from ENTITY_XREF, sentinels removed, no fanout cut. 1,050,881 nodes, 2,301,984 edges, largest component 1,008,049. 452,725 biconnected blocks, 36,930 articulation points, 6,704 of them physicians.
Cut size = nodes that lose their path to the rest when that one node is removed. Exact, from the block-cut tree rooted at the giant block. This replaces betweenness as the middleman test on this graph: a node with a big cut and a small degree is the quiet middleman by definition, and there is no k to argue about.

"Detached" below = the child side of the block-cut tree only, computed explicitly (cent_g2e.py). The first draft listed every neighbor; the skeptic caught three rows where most neighbors sit on the parent side and detach nothing. Corrected.
| NPI | name, from ENTITY_GOLDEN | deg | detached | what detaches | stays connected via |
|---|---|---|---|---|---|
| **1417615519** | **FOSTER, BRITTANY, CRNA, Atlanta GA** | **2** | **77** | 2 facilities + 75 physicians: ATHUR M BLANK HOSPITAL 113300 and Children's Healthcare of Atlanta at Scottish Rite 113301, which has only 2 roster lines in this file | Grady Memorial 110079 |
| 1518028976 | SUK, SAMUEL, Beaverton OR | 7 | 22 | 10 facilities + 12 physicians: nine Oregon nursing homes and Bristol Hospice Eugene | Bristol Hospice Oregon 381559 |
| 1871090175 | MULINIX, JACOB, Indianapolis, trainee | 2 | 19 | 1 facility + 18 physicians: FAIRBANKS 150179 | Community Hospital North 150169 |
| 1225433006 | MADATOVIAN, HARUT, Winnetka CA | 4 | 16 | 8 facilities + 8 physicians, LA home-health agencies | Wellness Plus Home Health 758004 |
| 1912462961 | MAKSIMOVA, ALLA, Sherman Oaks CA | 6 | 14 | 6 facilities + 8 physicians, LA home-health agencies | Cedars-Sinai and three agencies |
| 1356000731 | JURDI, DANIEL, San Dimas CA | 5 | 14 | 6 facilities + 8 physicians, Sun Valley and LA agencies | four Glendale agencies |
| 1871891507 | MIRANDA, ALTORY, Moseley VA | 12 | 14 | 6 facilities + 8 physicians, small Virginia rehabs and one hospice | Bon Secours St Marys and five others |
| 1437491727 | PATEL, BHAVINIBEN, Mount Pleasant TX | 5 | 13 | 5 facilities + 8 physicians, Dallas-area home health | four Dallas-area agencies |
Name check: every one of the 8 NPIs has exactly one CANONICAL_NAME and one CANONICAL_ADDR in ENTITY_GOLDEN, source FED_CMS_NPPES. Foster's GOLDEN address is Hixson TN; her NPPES practice address is Atlanta GA — mailing versus practice, both on the same NPPES row.

Finding, four lines:
what it is: NPI 1417615519, Brittany Foster, CRNA — a nurse anesthetist, taxonomy 367500000X, not a physician. Two affiliations on file.
what it bridges: ATHUR M BLANK HOSPITAL, CCN 113300 (spelled that way in the source), 75 clinicians on its roster. 73 of them appear nowhere else. One other links only to CCN 113301, a two-clinician facility. Foster is the only roster line reaching outward — to Grady Memorial, CCN 110079, degree 1,346, which is wired into everything.
why it is quiet: degree 2. Cut size 77 is the largest of any clinician among 6,704 clinician articulation points. Sampled betweenness never saw it.
plain words: a brand-new hospital's entire clinical roster is attached to the rest of American medicine by one nurse anesthetist's record. Cut that one row and 77 nodes — two facilities and 75 people — become an island.
chain: checked = articulation points and exact child-side cut sizes over the whole CCN↔NPI graph, then the detached set enumerated node by node. hit = a clinician whose removal detaches a whole facility. A miss would have meant every clinician cut ≤ 2, i.e. facilities always share several staff. The likely real-world reason: Blank Hospital opened in late 2024 (outside knowledge, not from the warehouse); the CMS affiliation file has not caught up, so its staff show one affiliation each. The bridge is real in the data; it is also a data-freshness artifact. Both are true, and the second is what a reporter would need to know before writing the first.

Second-cleanest case: Mulinix, NPPES taxonomy 390200000X — a student in an organized training program. Fairbanks, an Indianapolis addiction-treatment hospital, hangs on a trainee's record: 18 clinicians, one facility. Same shape as Foster; smaller.

Pattern under the rest of the table: one clinician tying a cluster of tiny home-health, hospice or nursing facilities to a bigger anchor. Five of the eight are home-health or hospice clusters, three of those in the Los Angeles basin. That is a structural fact about home health: many small agencies, few shared staff, one nurse or doctor on several rosters. Not a finding about any named person.

The sampled run's top physicians, re-checked: 8 of 12 are articulation points, cuts of 2–14. The sampling found real but small bridges and ranked them wrong; Foster's cut of 77 never appeared in the sampled top 200.

Hospitals with big cuts (NYU Langone 3,246; NY Presbyterian 3,039; Mayo Rochester 2,954; …) are hubs cutting off their own exclusive staff — degree-1 physicians who work nowhere else. Not middlemen. The "quiet CCNs" from the sampled run (West Jersey, Sarasota Memorial, LIJ, Nebraska Med, Montefiore, …) are the same shape: cut sizes 266–1,536, all their own leaves.

### Graph 2 cross-check against BRIDGE_ENTITIES
BRIDGE_ENTITIES is organization-only with DOMAIN_COUNT ≤ 3. Every Graph 2 winner is a person (NPI) or a PAC (FEC_CMTE_ID); none can be in it. New by construction — but also not comparable, so the cross-check is silent here rather than passed.

### Graph 2 value checks
Node ids: every winner resolved to a CANONICAL_NAME and address in ENTITY_GOLDEN — 8 of 8 NPIs, 10 of 10 CCNs in the quiet list, 12 of 12 LEI stars, 16 of 16 committees in the dim, 24 of 24 candidates in the landing file (fec_out.json names), plus the six CCNs the Foster row cites (party.log). Junk dropped: the final graphs filter blanks and all-zero values only; '<UNAVAIL>' and 'N/A' were tested in the second pass (none found in CCN or NPI values) and not re-tested on the final graphs. A placeholder would show up as a hub, not an articulation point, so it cannot have produced the Foster result. The FANOUT column was ignored as a constant.

Scripts and saved outputs:
| script | what | output |
|---|---|---|
| cent_g2.py | first pass, size cut 500 — discarded | g2_out.json |
| cent_g2b.py | second pass, size cut 5,000 — hospital sampled run, discarded | g2b_out.json, g2b.log, g2_fanout.json |
| cent_g2c.py | per-node cut loop, timed out at 10 min — do not rerun | none |
| cent_g2d.py | block-cut tree, cut sizes, names | g2d_out.json, g2d.log |
| cent_g2e.py | detached child-side sets, Blank composition, name uniqueness, NPPES taxonomy | g2e_out.json, g2e.log |
| cent_fec.py | FEC exact betweenness, control, LEI stars, names | fec_out.json, fec.log |
| cent_nppes.py | NPPES EIN/TIN value check | nppes.log |
| cent_names.py | first-pass names — corrected to the dim and C-columns, still reads the discarded g2_out.json | none, superseded by cent_fec.py |
| cent_party.py | party mix reconciled to degree; the six CCN names the Foster row cites | party.log |
Every number in the Graph 2 sections now has a saved artifact behind it.

Skeptic passes on Graph 2: two. First returned DISAGREE (FEC from the discarded run, three bridge rows wrong, false degree/gap sentence, missing LEI star, missing traps). Second returned DISAGREE-narrow (one number still wrong, control overclaimed 3-of-3, party mix unreconciled). All folded in above; each correction is marked where it sits. What it does: recompute real per-value fanout (the FANOUT column is a constant per source), drop junk hubs, pull distinct pairs, components, betweenness with k=300 sampled sources on any component over 3,000 nodes, exact below, degree gap, quiet list.
Second gated item: FED_CMS_NPPES (9.6M rows) — count distinct and sample EMPLOYER_IDENTIFICATION_NUMBER_EIN and PARENT_ORGANIZATION_TIN. If populated, NPPES is an unbuilt second health↔money bridge and SAM's monopoly is a wiring artifact. Cost from the query log: NPPES statements, 499 runs, p50 $0.00 max $0.54, X-Small.
Already known without a scan: the entity graph is six disjoint key families — CCN↔NPI (2.30M rows total: 2.25M affiliation + 52K same-row, physician↔facility), FEC_CAND↔FEC_CMTE (218K), FRS↔LEI (74K), CIK↔EIN (46K), BIOGUIDE↔ICPSR (25K), IMO↔MMSI (6.7K). No key type spans two families, so Graph 2 cannot bridge health to money; it can only find middlemen WITHIN a family — e.g. a doctor with 2–3 affiliations who links hospital systems that otherwise never share staff.
Cost from the query log: ENTITY_XREF, 41 runs, p50 $0.00 max $0.00. ENTITY_GOLDEN name lookups, 498 runs, p50 $0.00 max $0.54. All X-Small. Default $2/credit rate, not the contract rate.

## Traps found this session
- ENTITY_XREF.FANOUT is a per-(source, key pair) constant, not a per-value count. 6,962 on every CCN→NPI affiliation row. Recompute before using it as a junk filter.
- FED_SAM_EXCLUSIONS_FULL_R2.NPI holds '0000000000' on 12,027 rows. count(distinct) is fine; count(*) with NPI not null overcounts 2.7x. The LEIE version of this sentinel was already known (scripts/build_registry_setup.py, 89.6% of LEIE rows); the SAM copy is the new part.
- FED_CMS_NPPES carries EIN and parent-TIN columns that no edge was ever built on. A missing edge is not a missing column; the schema graph only knows what the builder wired.
- INTL_FR_DATA_GOUV_FULL's SPATIAL_GEOM contains 100% of US lat/lon points from four unrelated tables. A geometry that contains everything is a junk hub in any GEO_IN graph.
- LIBRARY_META.CONNECT must be quoted: "CONNECT" is a reserved word.
- FED_CMS_NPPES EIN and parent TIN are '<UNAVAIL>' on every populated row. CMS redacts them. One distinct value each.
- A fanout cutoff is a size cut, not a junk filter. Cutting at 500 manufactured the winners; cutting at 5,000 still dropped six real hospitals.
- Sampled betweenness with k=300 on a million-node graph cannot see a degree-2 bridge; it ranks hubs. Use articulation points and block-cut tree cut sizes for the quiet-middleman question at that scale.
- FRS_ID↔LEI is a star forest; parent→child crosswalks have no middlemen by construction.
- Sampled betweenness trap and the "CONNECT" reserved-word trap, both appended after the skeptic caught them missing.
All nine appended to .claude/traps.md.

## SQL and scripts
scripts/scratch/cent_probe.py — table shape probe (this is the one that broke the gate).
scripts/scratch/cent_g1.py — Graph 1 build, HARD graph, communities, betweenness, articulation points.
scripts/scratch/cent_g1b.py — entity-keys-only variant, both-key intersection test.
scripts/scratch/cent_sam.py — SAM id value check and edge rows.
scripts/scratch/cent_g1c.py — EDGES_INC alone and union rerun (first pass; the clean soft-key exclusion run was inline, results in the Robustness section).
scripts/scratch/cent_cols.py — column-name both-key test over information_schema, EDGES vs EDGES_INC run history.
scripts/scratch/cent_g2.py — Graph 2, gated.
Raw outputs: scripts/scratch/g1.json, g1_out.json.
