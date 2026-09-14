# HOW TO LOOK — the methods chapter

292 rows, merged from 344 extract rows across five families.

How to use this chapter: find the sub-heading that matches your stage (posture > verb > lens > move > check > picture), scan the name column, read the row.
Sources are short file names; the crosswalk `xw_methods.csv` maps every L-id back to its extract ids.

#### The 7 postures — how you stand before you query

| id | name | what it is, plain | when to use it | sources |
|---|---|---|---|---|
| L-001 | Posture: follow one entity | pick a name, pull every table it touches; a life story, not a stat | you have one name and want its whole record | tool box P1 |
| L-002 | Posture: reverse the question | start from an outcome, walk back to the actor everyone missed | you have a result and no suspect | tool box P1 |
| L-003 | Posture: chase a random row | follow every foreign key three hops out from one row | to find blind spots you would never search | tool box P1 |
| L-004 | Posture: assume guilt first | take the top-10, try to prove it clean | forces rigor on the "normal" ones | tool box P1 |
| L-005 | Posture: absence hunting | ask what should be there and is not; the gap is the finding | rosters, inspections, filings with holes | tool box P1 |
| L-006 | Posture: cross-domain collision | join two schemas with no business relation | correlations nobody built for | tool box P1 |
| L-007 | Posture: outsider's question | ask what a journalist or lawyer asks first; plain beats clever | when the clever query is going nowhere | tool box P1 |

#### The 20 verbs (also called the 20 moves)

| id | name | what it is, plain | when to use it | sources |
|---|---|---|---|---|
| L-008 | Verb 1: absence | the row that should exist and does not: zero inspections, no payment row, no provider | who was never looked at; filter inspection counts to zero, size by emissions | tool box P1; idea moves 20 |
| L-009 | Verb 2: precedence | does A reliably precede B, not do they correlate; event-study chart, day zero = first event | inspection vs violation dates on one permit; reactive vs proactive enforcement | tool box P1; idea moves 20 |
| L-010 | Verb 3: digit tests | Benford on leading digits; measured numbers obey, haggled ones bend away | penalty dollars, proposed vs paid | tool box P1; idea moves 20 |
| L-011 | Verb 4: the impossible zero | round-number clustering at the bottom; zero injuries at 900,000 hours is a claim | any self-reported count with hours or size beside it | tool box P1; idea moves 20 |
| L-012 | Verb 5: same entity, two agencies, two answers | one EIN telling different stories on different forms; the warehouse's best structural edge | headcounts across OSHA 300A, Form 5500, IRS BMF | tool box P1; idea moves 20 |
| L-013 | Verb 6: disappearance | who stopped filing; last year each entity appears, then the three years before | HCRIS, auto-revocations, OLMS, water systems | tool box P1; idea moves 20 |
| L-014 | Verb 7: rebirth | same building, new name; ownership churn against penalty dates | nursing homes, mines, FRS facilities, any penalised facility | tool box P1; idea moves 20 |
| L-015 | Verb 8: address collision | many things at one door; one mailbox with 400 companies or 40 doctors | Companies House, ICIJ addresses, NPPES practice address, ATF FFL | tool box P1; idea moves 20 |
| L-016 | Verb 9: the narratives | text nobody has read; most common verbs by industry; six free-text tables none of the 542 ideas open | OSHA case detail, MSHA accidents, HOLC/redlining descriptions, CFPB, parentheticals, WPA | tool box P1; idea moves 20 |
| L-017 | Verb 10: weird for your own kind | outlier inside a matched peer group, not the national outlier; COHORT_QUEUE does this shape | Part B billing by specialty, state, patient mix | tool box P1; idea moves 20 |
| L-018 | Verb 11: the counterfactual twin | two hospitals matched on everything but one thing; paired dumbbells | ownership type on matched beds, region, mix | tool box P1; idea moves 20 |
| L-019 | Verb 12: network position, not size | rank by betweenness not degree; the node whose removal splits the graph | ICIJ relationships 3.3M links, cosponsorship, 13F co-holding | tool box P1; idea moves 20 |
| L-020 | Verb 13: cadence | when the filing arrives is itself disclosure; Friday-night and year-end dumps; clock face or day-of-week heatmap | Federal Register, NHTSA recalls, SEC insider filings | tool box P1; idea moves 20 |
| L-021 | Verb 14: reciprocity | money that goes both ways in the same cycle | FEC committee-to-candidate | tool box P1; idea moves 20 |
| L-022 | Verb 15: staleness | acting on old information; map effective date vs storm history; last inspection date | NFIP community status book, NID dam inspections | tool box P1; idea moves 20 |
| L-023 | Verb 16: where the government even looks | the looking, not the finding; questions the denominator of every other chart | AQS monitor open/close dates vs population and emissions | tool box P1; idea moves 20 |
| L-024 | Verb 17: where the warehouse contradicts itself | duplicate sources disagree; the gap is the chart | FRS pair, EFD vs Stock Watcher, CMS NH vs NH411, two Retraction Watch pulls | tool box P1; idea moves 20 |
| L-025 | Verb 18: every line in the sand | bunching just below every reporting threshold; one histogram per threshold | PPP $150,000, single-audit trigger, $125 meal line | tool box P1; idea moves 20 |
| L-026 | Verb 19: the week it always happens | seasonal signatures; same calendar week spikes every year | NICS by week, overdose by month, storm damage by season | tool box P1; idea moves 20 |
| L-027 | Verb 20: rank churn | who climbed, not who is on top; bump chart, lines crossing is the point | pharma payers, county overdose rank, employer injury rank | tool box P1; idea moves 20 |

#### The 53 lenses — math laws

| id | name | what it is, plain | when to use it | sources |
|---|---|---|---|---|
| L-028 | Zipf's law | rank vs size straight on log scale; kink or cliff = a few actors far bigger than the curve | rank FEC donors by dollars | tool box P2 |
| L-029 | Benford's law | digit 1 leads ~30%; even spread means typed, not counted | leading digit of FEC amounts | tool box P2 |
| L-030 | Power law tail | a few nodes hold almost all connections; even spread is the odd case | transfers per FEC committee | tool box P2 |
| L-031 | Pareto 80/20 | small slice carries most volume; flat spread is atypical | do 20% of 13F filers hold 80% of value | tool box P2 |
| L-032 | Small-world network | everyone a few hops from everyone; isolated islands mean silos | shortest path between donors via committees | tool box P2 |
| L-033 | Preferential attachment | early actors snowball; no entry-timing effect means something else drives growth | early vs late FEC filers | tool box P2 |
| L-034 | Log-normal | gaps and sizes skew; hard cutoff or exact interval looks scheduled | time between filings per donor | tool box P2 |
| L-035 | Poisson clustering | random events cluster; bursts on no-deadline days need explaining | FEC dates around deadlines | tool box P2 |

#### Lenses — forensic tricks and cheap tells

| id | name | what it is, plain | when to use it | sources |
|---|---|---|---|---|
| L-036 | Time of death window | an unexplained gap in the timeline; silent period means missing or unfiled | FEMA registrations after a disaster | tool box P2 |
| L-037 | Fingerprint match | same unique trait where it should not be; one person, two committees | same street address on two committees | tool box P2 |
| L-038 | Trace evidence | a small shared detail links unrelated records | same registered agent on two filings | tool box P2 |
| L-039 | Alibi check | stated fact vs independent record | contractor location vs place-of-performance | tool box P2 |
| L-040 | Staging vs real | data arranged to look natural; too many exact round totals | USASPENDING award totals | tool box P2 |
| L-041 | Chain of custody | who touched the data when; unexplained reload means unverified | HMDA historic reloaded same day | tool box P2 |
| L-042 | Behavioral profiling | one actor's habits repeat; a tic is a fingerprint | one filer's amendment day-of-week | tool box P2 |
| L-043 | Round-number clustering / bunching detector | real money is messy; spike at round numbers is limits or fabrication; repo already has a bunching detector | donations at exactly $2,500 or $5,000; self-reported counts | tool box P2; wonder rankings 14 |
| L-044 | Address reuse | same P.O. box, different names; straw-donor shape | donor addresses across donor names | tool box P2 |
| L-045 | Timing tics | unrelated actors file within minutes; coordination without a stated link | same-day filing clusters | tool box P2 |

#### Lenses — network science

| id | name | what it is, plain | when to use it | sources |
|---|---|---|---|---|
| L-046 | Betweenness centrality / network centrality | the one node every path runs through; a 2-link bridge can beat a 50-link hub; SOURCE_COUNT on ENTITY_MAP is degree already | committee on most transfer paths; thing-to-thing edge lists; Lab grade Ready | tool box P2; Laboratory; Lab warehouse map |
| L-047 | Community detection | clusters nobody labeled | donor clusters in the FEC graph | tool box P2 |
| L-048 | Bridge / cut vertex | remove one node, graph splits | one shell holding a UK ownership chain | tool box P2 |
| L-049 | Homophily check | connected actors too similar to be luck; near-total employer overlap is bundling | connected donors sharing employer | tool box P2 |

#### Lenses — stats of fraud and anomaly hunting

| id | name | what it is, plain | when to use it | sources |
|---|---|---|---|---|
| L-050 | Chi-square uniformity | categories too evenly spread to be real | FEC amounts across dollar buckets | tool box P2 |
| L-051 | Digit variance test | Benford's cousin, second digit too | second digit of USASPENDING amounts | tool box P2 |
| L-052 | Regression discontinuity | sharp jump right at a legal cutoff; cliff at $200 is structuring | counts around the $200 disclosure line | tool box P2 |
| L-053 | Cui bono | who gains, asked before who did it; no hit or miss, a question after a flag | who benefited when transfers spiked | tool box P2 |
| L-054 | Isolation forest logic | the single record easiest to separate; start there | most unlike FEC donor record | tool box P2 |
| L-055 | Z-score sweep | anything past 3 sigma, flagged blind; could be error or real extreme | every numeric column | tool box P2 |
| L-056 | Missingness pattern | is what is not there random; clustered by state means process differs | missing employer on FEC rows | tool box P2 |
| L-057 | Duplicate near-miss | two records 95% identical, not 100%; same person entered twice | donors off by one address digit | tool box P2 |

#### Lenses — physics, biology, game theory

| id | name | what it is, plain | when to use it | sources |
|---|---|---|---|---|
| L-058 | Entropy measure / information density | real randomness is messy; oddly smooth means smoothed or invented; entropy drops flag where pattern snapped into order | self-reported emissions sequence; counts across buckets; 403 tables share one clock; Lab grade Ready | tool box P2; Laboratory; Lab warehouse map |
| L-059 | Diffusion / spread rate | how fast a pattern moves through a network; speed, not right or wrong | prescribing pattern across providers sharing a rep | tool box P2 |
| L-060 | Herding / flocking | many actors move together with no stated coordination | committees moving money the same week | tool box P2 |
| L-061 | Nash tell | a move that only makes sense with information nobody admits having | bid that assumes a competitor drops out | tool box P2 |
| L-062 | Signaling | small early move announces a bigger one; a shape to watch | small gift then a big bundled one | tool box P2 |

#### Lenses — text and language

| id | name | what it is, plain | when to use it | sources |
|---|---|---|---|---|
| L-063 | Stylometry | same writer under different names | boilerplate across committee filings | tool box P2 |
| L-064 | N-gram fingerprint | a repeated phrase links unrelated records; shared template | boilerplate clause across filing purposes | tool box P2 |
| L-065 | Levenshtein distance | names one typo apart may be one entity | donor names differing by one character | tool box P2 |

#### Lenses — time series

| id | name | what it is, plain | when to use it | sources |
|---|---|---|---|---|
| L-066 | Autocorrelation | does today predict tomorrow; a sudden break is the flag | daily contribution volume | tool box P2 |
| L-067 | Change-point detection | the exact date a pattern shifted; when did this line break | contractor award size regime; any clocked series; TIMELINE__WAREHOUSE is the exact input | tool box P2; Lab warehouse map |
| L-068 | Seasonality check | a cycle that should not be cyclic | violation rate vs inspection schedule | tool box P2 |
| L-069 | Granger causality | does A's timing move before B's, consistently | lobbying filing before contract award | tool box P2 |

#### Lenses — geospatial

| id | name | what it is, plain | when to use it | sources |
|---|---|---|---|---|
| L-070 | Spatial clustering / Moran's I | events bunch more than density explains; do nearby things behave alike or opposite; works on similarity distance too | EPA violations vs facility density; value per place + shuffle test, shuffle code exists; Lab grade Ready | tool box P2; Laboratory; Lab warehouse map |
| L-071 | Distance decay | an effect should fade with distance | contribution size vs distance from HQ | tool box P2 |
| L-072 | Hot-spot mapping / Getis-Ord Gi* | one place lights up across unrelated datasets; Gi* confirms a cluster is denser than chance | one ZIP heavy in FEC, EPA, CFPB; value per place + distance-band neighbours from centroids; Lab grade Ready | tool box P2; Laboratory; Lab warehouse map |

#### Lenses — causal and bias traps

| id | name | what it is, plain | when to use it | sources |
|---|---|---|---|---|
| L-073 | Survivorship bias | you only see what is still around; always ask what got dropped | UK active-only companies | tool box P2 |
| L-074 | Simpson's paradox | a trend flips when you split the group | lending denial by lender size | tool box P2 |
| L-075 | Regression to the mean | extreme value drifts back; settling means noise | contribution spike next cycle | tool box P2 |
| L-076 | Confounding variable | a third thing drives both sides; a discipline, not a query | contribution timing vs contract timing | tool box P2 |

#### Lenses — epidemiology and information theory

| id | name | what it is, plain | when to use it | sources |
|---|---|---|---|---|
| L-077 | Contact tracing logic | who touched whom in what order; traces money step by step | committee-to-committee transfer order; two parties, same place, same time, stable ID; Lab grade Ready via ICE stints | tool box P2; Laboratory; Lab warehouse map |
| L-078 | R-naught style spread | is one actor's pattern replicating outward | one donor's style in new committees | tool box P2 |
| L-079 | Compressibility test | too repetitive compresses too well; synthetic or copy-pasted | self-reported dataset vs real noise | tool box P2 |
| L-080 | Mutual information | two columns share more signal than makes sense | award size vs lobbying spend, same firm | tool box P2 |

#### The 8 added methods

| id | name | what it is, plain | when to use it | sources |
|---|---|---|---|---|
| L-081 | Bayesian inference | update belief as each piece of evidence lands; never judge on one look | any multi-step hunt | tool box P2 |
| L-082 | Monte Carlo simulation | run a pattern thousands of times to see what normal looks like | before calling anything an outlier | tool box P2 |
| L-083 | Dimensionality reduction (PCA / t-SNE) | collapse many columns to the few that matter; squash 20+ measures per row into 2D | wide numeric tables; one row = one thing with many real numbers; 10 tables qualify; Lab grade Ready, watch the twin | tool box P2; Laboratory; Lab warehouse map |
| L-084 | Control charts / SPC | did something drift out of its normal range; factory-floor logic | any series with a baseline | tool box P2 |
| L-085 | Diff-in-diff with a placebo | before/after against an untouched group; run the same windows on never-treated units; the difference is the finding; the only one that argues cause | policy or event effects; any before/after on a file with a growth trend | tool box P2; hunch expansion #45, #51 |
| L-086 | Hash / checksum matching | byte-identical records under different labels | duplicate tables, copied rows | tool box P2 |
| L-087 | Markov chain modeling | does next state depend only on now, not the whole history | status sequences | tool box P2 |
| L-088 | Natural language classifier / text analytics | sort free text into buckets automatically; topic maps, phrase shift over time, near-duplicate detection | the six narrative tables; ~29M narrative rows, the closest thing to a human voice | tool box P2; Lab warehouse map |

#### Lenses borrowed from other sciences (the Laboratory)

| id | name | what it is, plain | when to use it | sources |
|---|---|---|---|---|
| L-089 | The organism: anatomy vs physiology | mass and distance = anatomy; circulation and ripples = how it lives | framing the four organism families | Laboratory |
| L-090 | Mass | density, heatmaps, bubble size, contours: where is there a lot? | coordinates or place code + population denominator; Ready at county and tract | Laboratory; Lab warehouse map |
| L-091 | Distance | clustering, dim reduction over join-key relatedness: what is similar to what? | cluster the registry feature vector, not CONNECT_EDGES; Ready | Laboratory; Lab warehouse map |
| L-092 | Circulation | network / force-directed graphs: what connects to what? | real edge lists: ARCOS, ICIJ, PSC, GLEIF, FACILITY_AFFILIATION, ENTITY_XREF; Ready, biggest two sealed | Laboratory; Lab warehouse map |
| L-093 | Ripples | diffusion / propagation animation: what happens if this changes? reverse peel made visual | needs dated edges; Partial, only GLEIF can carry a ripple out of its source | Laboratory; Lab warehouse map |
| L-094 | Topological Data Analysis | finds loops, holes, clumps in a point cloud that averages miss | HCRIS 6,103x107, POS_OTHER 44,429x204, QPP 503,917x62; Ready | Laboratory; Lab warehouse map |
| L-095 | Kernel Density Estimation | scattered points to a smooth heat surface | numeric lat/lon; Ready, needs nothing built; check row grain first | Laboratory; Lab warehouse map |
| L-096 | Flow maps | movement between places, origin to destination | same-row from/to with amount and date; Partial: county today, ZIP after DIM_ZIP_POINT | Laboratory; Lab warehouse map |
| L-097 | Astronomy: sky surveys / N-body | gravity-like attraction clusters billions of points; force-directed's big sibling | millions of points + a pull measure; Ready on AIS, but one week and no stored similarity | Laboratory; Lab warehouse map |
| L-098 | Neuroscience: connectome mapping | millions of connections, find the important circuits | same shape as the Catalog; Partial: runs inside ARCOS, islands don't touch across | Laboratory; Lab warehouse map |
| L-099 | Ecology: food web / trophic cascade | remove one node, watch the cascade; built around removal not spread; maybe the best ripple template | directed multi-hop chains in one namespace; Ready (ARCOS, GLEIF, MSHA controllers) | Laboratory; Lab warehouse map |
| L-100 | Finance: correlation matrices / heatmap clustering | score every pair of lines, reorder so co-movers clump; same math as distance | many series on one clock; Ready via TIMELINE__WAREHOUSE | Laboratory; Lab warehouse map |
| L-101 | Survival / time-to-event | how long until something happens, and to whom; censoring, backwards dates, cohort comparability already scored | spans and lags; 56 span + 70 lag tables scored | Lab warehouse map |
| L-102 | Group-disparity testing | rate ratios between demographic groups with a denominator per group | who gets hurt, and does the data show it | Lab warehouse map |
| L-103 | Compositional / mix-shift | which shares moved, not just how spread | 687 mix rulings already computed | Lab warehouse map |
| L-104 | Bipartite two-mode projection | entities x source files; project either way | source overlap map, or visibility-anomaly detector | Lab warehouse map |
| L-105 | Fourteen wonder lenses | Surprise, Causal, Contagion, Anomaly, Community, Flow, Prediction, Structure, Density, Phase, Compression, Narrative, Temporal, Cross-lens combos | generating and grouping wonders | wonder rankings |
| L-106 | Schema-first lens lookup | matrix of 20 schemas, best-fit lenses, posture, trap warning; the same table read lens-first | picking where a lens fits | tool box P3 |

#### How a session runs

| id | name | what it is, plain | when to use it | sources |
|---|---|---|---|---|
| L-107 | How to use the box | pick a move, pick a lens, pick a table off the matrix, check key rules, chase, only then run the 5 checks, write up after; stuck? pick blind | every session start | tool box § How to use it |
| L-108 | Look for weird, then read the weird | don't look for things; questions are the wrong start; you need the answer to ask a good one | every hunt | Laboratory |
| L-109 | The atom is an entity, not a question | pick a key, busiest value, pull every row (dossier ~10 tables), read like a story, count who else does that | starting any investigation; the joins already built the dossier; see entity card | Laboratory |
| L-110 | Hunt unit that works | one subject area x one move; four of those fills a session; settled, not to be redesigned | session planning | session 09-08 |
| L-111 | Rank tables by leverage first | rows x keys x clock; top 30 tables carry most of the surprise | before the weirdness passes | Laboratory |
| L-112 | The huntable-table funnel | mart base tables 704 > 100K+ rows 250 > real date 165 > hard key 46 (569.6M rows); hand-typed 18-id filter, 46 is a floor; framing flagged suspect by the handoff | sizing where stories can live; treat with care | how to hunt P1; handoff 09-08 P5 |
| L-113 | Breadth by machine, depth by human | same SQL over 2,000 tables, no thinking per table; read only the top 50 of each list; five passes, one evening | running the weirdness passes | Laboratory |
| L-114 | Timeline is the story | order dated events forward across datasets; the sequence carries the case | investigations | frank investigation |

#### The 5 hunt moves and the sweeps

| id | name | what it is, plain | when to use it | sources |
|---|---|---|---|---|
| L-115 | Hunt move 1: the zero hunt | which rows hold a zero or null where zero is impossible; proof: loader writes nulls elsewhere | any count column | how to hunt P3 |
| L-116 | Hunt move 2: the ratio hunt | two columns in one table that must agree, divided; contradiction inside one row, no join | hours over employees, proposed over paid | how to hunt P3 |
| L-117 | Hunt move 3: the spread hunt | group by the administrator instead of the subject; coal states sorting together is the tell | penalty collection by state | how to hunt P3 |
| L-118 | Hunt move 4: the tail hunt | sort descending, look at row one; row one is a lead, the shape of the tail is the finding | companies per address | how to hunt P3 |
| L-119 | Hunt move 5: the clock hunt | min and max on the date column before designing anything; cheapest query, run first every time | every table you are about to touch | how to hunt P3 |
| L-120 | The 230-query sweep | clock, zero, tail, ratio, spread on all 46 deep tables, ~5 each, single-table aggregates, one ranked sheet of anomalies; only ratio needs per-table thought | letting the data raise its hand | how to hunt P6 |
| L-121 | Machine trap sweep S1-S5 | S1 same numbers typed on many rows by one filer (30 flags); S2 box reads filled but empty (3,331); S3 one value in every row (0, fixed to 41 on LABOR); S4 date/id/money column that is not (2,811); S5 one key in two tables that should agree (13); scripts/trap_sweep.py | audit-scale trap finding; S1 finds stories, the rest find chores | session 09-08 |
| L-122 | Sweep gates for S1 | cardinality gate or S1 keys on YEAR columns; tail gate or it flags 76,365 MSHA rows at the $100 minimum fine | never remove from the script | session 09-08 |
| L-123 | Weirdness pass 1: shape | what normal looks like per column; distribution per column | run over every table | Laboratory |
| L-124 | Weirdness pass 2: outlier | who sits far from normal within their group; ranked top 50 | run over every entity | Laboratory |
| L-125 | Weirdness pass 3: coverage | who is in way more tables than peers; ranked list | run over every entity | Laboratory |
| L-126 | Weirdness pass 4: residual | who should join but doesn't, or double-joins; orphans and collisions; the sneaky one (a nonprofit with 40 UEIs) | run over every key | Laboratory |
| L-127 | Weirdness pass 5: change | where a time series breaks; dates per entity | run over every clocked entity | Laboratory |
| L-128 | Statistical sweep vs intersection rule | peer-cohort outlier scan returns thousands; ID intersections return few by construction | reading lead counts | pitch deck |

#### Chains — templates and how to judge one

| id | name | what it is, plain | when to use it | sources |
|---|---|---|---|---|
| L-129 | Chain A: doctor to county morgue | NPPES > Open Payments > Part D > affiliation pivot to CCN > Hospital Compare > HCRIS > ZCTA pivot to FIPS > DIM_COUNTY > CDC drug poisoning > Vera; six turns, ~87% survival | template for a person-to-place chain | tool box P3 |
| L-130 | Chain B: corporate x-ray | FRS facilities > program links > ECHO > TRI > GHGRP > corporate crosswalk pivot to LEI > GLEIF relationships > GLEIF country > ZCTA pivot > QCEW > CDC injury; six turns, ~85%; today's ceiling | template for a smokestack-to-parent chain | tool box P3 |
| L-131 | Chain C, the greedy one, and the named-example panel | adding a stock layer forces LEI to CIK, survival falls 85% to ~8%; after any 2-16% cross-key hop show the nine you could resolve, never a percentage | when a chain needs a cross-key hop | tool box P3; join depth ceiling |
| L-132 | Turns, not table count | impressiveness = how many times the chain changes what kind of thing it is about; person > facility > company > parent > place > population; strangers feel a turn, not a seventh join | judging a chain | tool box P3; join depth ceiling |
| L-133 | X per Y relative to Z | shape of every cross-join item: Y is the join key, Z is the second table's attribute | writing any join idea | viz join catalog |
| L-134 | Hit means / miss means (walk the chain) | state before running what a hit and a miss would each mean; every finding says what was checked | every chain, every finding | hunch expansion; docket crossjoin 25; frank hospice |
| L-135 | Nearest live version | a dead hunch gets the closest chain that does exist, never dropped | every tier-3 hunch | hunch matrix |

#### Query disciplines — before you trust a number

| id | name | what it is, plain | when to use it | sources |
|---|---|---|---|---|
| L-136 | Shuffle placebo / random-draw control | re-pair the two sides at random and re-measure, or compare the observed co-spike against 20 random draws; median barely moves, concentration does | before quoting a median as agreement; contagion rules (neighbor_spike_rule.py) | toolbox hunt F4; wonder rankings |
| L-137 | Constant relative precision for roundness | use significant figures, never a fixed modulus, when comparing roundness across scales | any round-number test across sizes | toolbox hunt F2 |
| L-138 | Lender-regime control | bucket every loan by its lender's own rounding habit before measuring borrower roundness | round-number tests on disbursed money | toolbox hunt F2 |
| L-139 | Tuple-block dedupe | group rows by exact (hours, employees, state, NAICS); blocks are one employer's page repeated | multi-site filers in OSHA 300A | toolbox hunt F1 |
| L-140 | Carbon-dating a per-NPI file | newest NPPES PROVIDER_ENUMERATION_DATE among NPIs present bounds the data year | any CMS per-NPI load with no year column | hunch expansion #39, #40 |
| L-141 | Clip event dates to the data range | keep only events with both windows inside [file_min+window, file_max-window] | any before/after count | hunch expansion #45, #51 |
| L-142 | Balanced panel | compare the same entities in both years, never avg(year A) vs avg(year B) | suppressed or churning cohorts (CDC 1-9) | hunch expansion #52 |
| L-143 | Per-pair difference-in-differences | expected_after = sum(before x nat_after/nat_before) per pair, not a pooled ratio-of-ratios | any DiD across pairs with different calendar windows | hunch expansion #50 |
| L-144 | Mix standardisation | re-weight year 2 to year 1's complaint/standard survey mix before reading a severity trend | deficiency severity trends | hunch expansion #44 |
| L-145 | Within-class comparison | split by ownership type or population band before calling a gap real | any cohort gap (triple owners, jail counties, HUD density) | hunch expansion #46, #55, #67 |
| L-146 | Condition on exposure | restrict both arms to entities actually inspected before comparing violators to clean | any enforcement-table comparison | hunch expansion #61 |
| L-147 | Tie-free percentile | percentile_cont(0.90) within group, or rank only non-zero rows, instead of ntile | money columns with mass zeros or integer ties | hunch expansion #54, #56, #57 |
| L-148 | Denominator by eligible roster | divide dated counts by the roster eligible at each date before reading direction | as-of-today registries (opt-out, exclusions) | hunch expansion #38 |
| L-149 | Modification-number truncation check | compare count(*) to max(modification_number) per award | any USASpending per-award count | hunch expansion #75 |
| L-150 | Roll transactions to award | USASpending rows are modifications; naive count inflates 174x | contract counts | pitch deck P3 |
| L-151 | Normaliser sanity pair | test the name normaliser on a known pair before trusting a match count | any regexp name join in Snowflake | hunch expansion #68, #70 |
| L-152 | Fixed-horizon ratio | rate a controller over a fixed window so raw ratios do not shrink toward the present | any per-entity rate over time | wonder rankings top 5 #3 |
| L-153 | Size-adjusted residual | rank the residual of a ratio against the entity's own size and type, not the raw ratio | anomaly hunting per controller/facility | wonder rankings top 5 #3 |
| L-154 | Decile gradient with within-group controls | decile on the exposure (PCT_MINORITY), compare means; repeat within state and program type to strip where-the-industry-is confounding | EJ-style gradients | wonder rankings top 5 #4 |
| L-155 | Forward-window construction | predictor at T, outcome in the following window, size/state/ownership fixed; treat a snapshot as end-of-period or the arrow points backwards | predict rather than describe | wonder rankings top 5 #5 |
| L-156 | Date-test the join | EXCLDATE < DATE_OF_PAYMENT, or the arrow reads backwards | any flag-list x activity join | pharma paid excluded |
| L-157 | Hold-the-tag comparison | compare like citation to like citation by fixing DEFICIENCY_TAG_NUMBER before comparing states | cross-regulator severity | wonder rankings top 5 #2 |
| L-158 | Rates with a minimum-volume floor | when volumes differ 25x use rates, and drop groups under a floor | state-by-state comparisons | wonder rankings top 5 #2 |
| L-159 | Sums not means when zero-not-null | AMOUNT_PAID is zero for uncollected rows, so a mean understates; use sums | penalty collection | wonder rankings top 5 #1 |
| L-160 | Exclude the appeal window | drop the trailing 24 months before ranking collection rates | MSHA penalties | wonder rankings top 5 #1 |
| L-161 | Discount split: contest vs non-collection | second pass checks whether the proposed-vs-paid gap is appeals or non-collection; changes what the number means | after the P-145 core result | wonder rankings top 5 #1 |
| L-162 | Subtract the deadline artefact | measure filing-deadline-eve spikes, M-007, so they can be subtracted from timing-entropy tests, M-056 | FEC timing | wonder rankings 40 |
| L-163 | EIN-change proxy for acquisition | same ESTABLISHMENT_ID with a different EIN across years stands in for "bought" | OSHA 300A when no M&A table | wonder table map arc 5 #101 |
| L-164 | Sponsor-change proxy for buyout | Form 5500 LAST_RPT_SPONS_EIN <> EIN stands in for a buyout | pensions when no deal list | wonder table map arc 3 #63 |
| L-165 | Self-join across years | same table, other years, on ZIP+COMPANY+ISSUE or STATE+COMPANY to find repeats or shifts | CFPB repeat complaints, servicer change | wonder table map arc 5 #118, #121 |
| L-166 | Split a packed list before joining | K_NUMBER_LIST, sanctions ADDRESSES are packed multi-value text; split first | FDA enforcement, OpenSanctions | wonder table map arc 5 #107, #114 |
| L-167 | Lead with the percentile | suppression depresses the median; the multiple inflates, the rank does not | CMS suppressed files | frank investigation S3 |
| L-168 | Common cohort | rank all measures on the rows carrying all of them | comparing percentiles | frank dme |
| L-169 | Bound the percentile | count hidden rows that could clear the bar; report the band | censored peer sets | frank dme |
| L-170 | Sign of the residual | total below sum = dedup; money never dedups, so excess = masking | non-additive columns | frank dme |
| L-171 | Absence vs zero | suppressed under 11 is blank, not zero | CMS files | frank hospice |
| L-172 | Geographic baseline | state median before national when practice norms vary | ratio outliers | frank hospice |
| L-173 | Base rate before bold | check how common the "damning" shape is across the same table | any single-row claim | frank investigation S4; frank hospice |
| L-174 | Split the headline number | one royalty vs 582 lunches: two stories in one total | any sum | pharma paid excluded |
| L-175 | Dollars vs breadth rankings | rank payers by total and by distinct recipients; they differ | payer analysis | pharma paid excluded |
| L-176 | Collapse file-split suffixes | merge year/quarter tables into source systems before ranking reach | graph counts | graph hunt ein A1 |
| L-177 | Read match rate, not matched count | share of the smaller side that landed separates walkable bridges | using CONNECT_EDGES | graph bridges |
| L-178 | Identity vs affiliation | asserted_same_row fanout 1 = identity; asserted_affiliation = two things touching | ENTITY_XREF | graph bridges |
| L-179 | Validity by format | EIN nine digits, UEI twelve alphanumerics; not by null | key coverage | ghost doctors S1 |
| L-180 | Column scan for the missing thing | scan every table's columns for %PAYEE%, %TIN%, %EIN% before saying it's hidden | absence claims | ghost partb |
| L-181 | Reach as the useful axis | cross-domain entity bridging is near zero; count how many source tables a key type spans instead | deciding where to build | wonder rankings § Surprises |

#### Verification — the 5 checks and the skeptic

| id | name | what it is, plain | when to use it | sources |
|---|---|---|---|---|
| L-182 | Check 1: provenance skepticism | who collected it, what is their incentive to shade it | any finding | tool box P5 |
| L-183 | Check 2: external baseline | an outside source confirms the same fact; only-in-warehouse may be a load bug | any finding | tool box P5 |
| L-184 | Check 3: replication / peer test twice | holds in a second year, state, or dataset; two years, two definitions, two peer sets; survives both or it's an artifact | any finding; outlier claims | tool box P5; frank investigation S3 |
| L-185 | Check 4: red-team your own pipeline | could the load script or a join be the cause | any finding | tool box P5 |
| L-186 | Check 5: the story test / who gets hurt | true AND explains something someone cares about; names a human on the other end or it's trivia; true and boring gets logged | before writing a piece; registering findings | tool box P5; pitch deck |
| L-187 | Three ingredients of wow | scale (national number), a name (one entity at the top), a stake (someone harmed or money gone); missing one lands soft | grading a candidate piece | how to hunt P5 |
| L-188 | Hub probe + fresh skeptic | one probe agent per hub (county, clinician, facility, cross-hub); each hunch rebuilt by a fresh-context skeptic from the chain text | any batch of hunches; 50 agents, 1,184 tool calls, 82 minutes for 44 | hunch expansion |
| L-189 | Skeptic rerun / score then refute | rewrite the SQL independently, check both join keys, entity vs row counts, sentinels, caps, vintages; verdict CONFIRMED/CORRECTED/REFUTED; on metadata: hunt tier inflation, name trusted as contents; four tier calls changed | before any done claim; any metadata sweep | hunch expansion; Lab warehouse map |
| L-190 | Blind spot paragraph | skeptic names what its rerun cannot see because it shares the source tables | every skeptic verdict | hunch expansion |
| L-191 | Skeptic corrections kept in view | corrections logged, not folded in silently | after skeptic pass | frank investigation; frank dme |
| L-192 | Show the whole record | present all rows, name what's omitted and why | citation and drug lists | frank investigation c6-7 |
| L-193 | Supported / not shown table | close every report with statement-by-statement support | every report | frank investigation |
| L-194 | Per-hunch card | refined line, chain that holds, what ran, number, trap | writing up any probe | hunch matrix |
| L-195 | Completeness pass the other way | which shapes exist at scale that no technique claims | after scoring a catalog | Lab warehouse map |

#### Grading schemes

| id | name | what it is, plain | when to use it | sources |
|---|---|---|---|---|
| L-196 | News three grades: Echo | story says X, table shows X; proves the file landed and did not rot | news corroboration | tool box P9; news corroboration map |
| L-197 | News three grades: Retrace | start from the story's first clue, joins reach the end; proves the joins work | news corroboration | tool box P9; news corroboration map |
| L-198 | News three grades: Stumble | one dumb query over the whole table, story pops in the top 20; proves the warehouse can find | news corroboration | tool box P9; news corroboration map |
| L-199 | M x D x C x E priority score | four axes 1-5: M mechanism (5 exposes a systemic dynamic), D data readiness (verified live; broken upstream capped at 2), C consequence to people, E effort (5 = one SQL + chart, 1 = new pipeline); max 625; novelty unscored on purpose | ranking wonders before building | tool box P6; wonder rankings |
| L-200 | Novelty column left unscored | every ranked row carries `unscored` so the tabled "Pie in the Sky" project can join on it later | any wonder ranking | wonder rankings |
| L-201 | Top-5 selection rule | highest priority; exclude anything already built and run; break ties toward distinct source-and-mechanism coverage; name runners-up | picking prototypes | wonder rankings |
| L-202 | Expansion rule | new wonders only in lenses that scored highest on M x D x C (Surprise, Causal, Contagion) and only against tables verified healthy | growing a wonder list | wonder rankings |
| L-203 | Verify D with live queries / docket data check | 9 batches: row counts, null/blank rates, distinct counts, date ranges, key-coverage joins, value samples; per entry: tables exist, row counts, year spans, staleness; no D score from a table name | scoring data readiness; before writing a join; only gate one of four | wonder rankings; docket DATA; docket README |
| L-204 | Plausibility grade A/B/C | A both tables named, key known; B one side unsure, check registry; C needs data doubted landed | first pass on a wonder before mapping | wonder list |
| L-205 | Three tiers for a hunch | 1 seeded/live: chain holds, first number, dated legs; 2 one vintage: a leg is a snapshot; 3 dead as written: a leg missing | grade any hunch before spending warehouse money | hunch matrix; hunch expansion |
| L-206 | Wish-list scoring | score = 2 x tier-3 rescues + 1 x tier-2 promotions; LIKE-search landing, marts, registry at column level before calling missing | ranking datasets to load | hunch expansion § wish list |
| L-207 | Crawl / walk / run | crawl = one table one chart (277); walk = two tables one join (92); run = a chain of three or more (23) | sizing or labelling an idea | tool box P7; docket notes; docket v2 vs v1 |
| L-208 | v1 vs v2 question | v1 asks "is someone cheating"; v2 asks "what would a stranger stop and stare at" | choosing which docket to draw from | tool box P7 |
| L-209 | Docket seven states | open, partial, confirmed, modest, dead, merged; dead covers no pattern or years do not line up; 8 regex rules in scripts/build_docket.py lines 76-92 sort free notes into the 7 labels | status column of any idea list | tool box P4; docket README |
| L-210 | Probe folder self-link | a folder named <id>_<slug> under reports/ links to its entry on rebuild | filing any probe write-up | docket README |
| L-211 | Trust legend | CLEAN = verified this month; CAVEAT = usable with a named limit that must appear on the visual; excluded | grading any viz substrate | viz inventory |
| L-212 | BUILT flag | a working prototype page exists from the 2026-08-22 sprint | reading the viz inventory | viz inventory |
| L-213 | Warehouse readiness grades | Ready / Partial / Needs new data / Needs cleanup; plus Needs, What exists, Gap, Distance to ready, Candidate tables, one blockquote line | scoring a technique against the warehouse | Lab warehouse map |
| L-214 | Rank opportunities by capability per unit of effort | not by what should be built first; that call is Chris's | listing next steps | Lab warehouse map |
| L-215 | Gap ledger, ranked by wonders unlocked | each missing table or column once, count wonders it unlocks, tag the fix kind | deciding what to land next | wonder table map |
| L-216 | Fix kinds | land a table; add a column; parse a field; reload a table | classifying a gap fix | wonder table map |
| L-217 | Fact vs lead | fact = two records share a hard government ID; lead = share a name, no ID, a hunch | governs everything; facts publishable, leads need a human | design brief primer |
| L-218 | Confidence ladder | STEEL (hard ID) > STRONG (domain ID) > BRIDGE (via 3rd dataset key) > CORROBORATED (name + place) > GEO (location) > PROBABILISTIC (fuzzy name); ordering sacred, palette free | every edge drawn; never draw weak like strong | design brief D2; atlas blueprint 3.3 |
| L-219 | The six detectors (List A and List B) | same hard ID on a flag list and an activity list at the same time; flag sources LEIE/OFAC/SAM vs active OpenPayments/AIS/USASpending; ~1,030 leads, 773 on one edge | finding smells (banned doctors still paid, sanctioned ships still broadcasting); the human decides | design brief D3; pitch deck; HOUR dossier 3 |
| L-220 | Judge a lead in order | names agree? timeline says while banned? caveat box? money size? LEIE_ROW_MISSING means check OIG | review queue | HOUR dossier 7 |
| L-221 | Priority score is arithmetic | tier weight + timeline weight + detector weight + tiebreak | ranking leads | HOUR dossier 5 |

#### The weather lens (RIPPLES)

| id | name | what it is, plain | when to use it | sources |
|---|---|---|---|---|
| L-222 | Weather lens | Ripple runs stations, takes the same readings everywhere, issues warnings a human confirms | all internal thinking; never public copy or renames | RIPPLES glossary |
| L-223 | Ripple 1: Conditions (STATE) | what is everything, right now | first question on any warehouse ask | RIPPLES |
| L-224 | Ripple 2: Systems (NEIGHBORS) | what's connected, what moves as one thing | second question | RIPPLES |
| L-225 | Ripple 3: Patterns (FLOW) | what's moving, what leads what, where it stalls | third question | RIPPLES |
| L-226 | Observation | one run of a question across everything | any sweep | RIPPLES |
| L-227 | Instrument | a dumb question mounted once, measuring everything automatically | building rules | RIPPLES |
| L-228 | Game of Life bet | simple pieces, honestly measured, allowed to touch; patterns draw themselves | design of every piece | RIPPLES |
| L-229 | Every bite is the same bite | uniform measurement makes cells comparable; sameness compounds | building readings | RIPPLES |
| L-230 | Touching by wire | follow the joins: same owner ID, address, officer; court-ready | proving connection | RIPPLES R2 |
| L-231 | Touching by resemblance | same behavioral signature, zero shared keys | finding suspects | RIPPLES R2 |
| L-232 | The loop | resemblance finds suspects, wires confirm, survives both = finding | every pattern claim | RIPPLES R2 |
| L-233 | Flow ladder | box 0 staleness, 1 direction, 2 heartbeat, 3 co-move, 4 leads, 5 wave breaks; breadth-first | any time-series claim | RIPPLES R3 |
| L-234 | Lens, not checklist | ask: which Ripple, simplest cell version, who are neighbors, what over ticks | every warehouse question | RIPPLES § sessions |
| L-235 | Start simple, breadth-first | never skip to the fancy rule | new lenses | RIPPLES § sessions |

#### Pictures for dense data

| id | name | what it is, plain | when to use it | sources |
|---|---|---|---|---|
| L-236 | Aggregate first | histograms, heatmaps, hexbins; plot group summaries, not every point | any table too big to draw; 252 tables over 1M rows, 79 over 10M; Ready | Laboratory; Lab warehouse map |
| L-237 | Encode density, not position | colour a spot by how many records landed there | overplotted coordinate pairs; 122 tables have numeric lat; Ready | Laboratory; Lab warehouse map |
| L-238 | Sample or tier by zoom | subset at first glance, more on zoom, like map tiles | ladder exists (56 states, 3,222 counties, 85,391 tracts, 46,960 ZIP rows); Partial: no polygons, bigger dots not filled areas | Laboratory; Lab warehouse map |
| L-239 | Funnel plot | rate vs volume with uncertainty bands so tiny units cannot top the chart on noise | facility league tables, lender gaps, hospitals; any league table | tool box P8; Lab warehouse map |
| L-240 | Spectrogram | one entity, categories down the side, months across, cell = intensity; the "music" technique; a static ripple image | one pharmacy's drugs over 84 months; Ready on ARCOS | tool box P8; Laboratory; Lab warehouse map |
| L-241 | Percolation dial | drop weak edges one threshold at a time, watch islands snap into one blob or the network shatter; snap threshold is the finding | shipment or ownership networks; only on a real physical network (ARCOS); invalid on the 0.1%-sampled connection map | tool box P8; Laboratory; Lab warehouse map |
| L-242 | Survival curves | share still in state at day 7/30/90/180/365 by cohort | detention stints, violation spans | tool box P8 |
| L-243 | Sankey / alluvial / chord | origin > holder > outcome flows; flow without geography | detention, election money, foreign aid; every from/to flow the map can't draw | tool box P8; Lab warehouse map |
| L-244 | Entropy map | which states' category mix is unusual vs national | CFPB complaint mix | tool box P8 |
| L-245 | Changepoint gallery | for each source, the month its line snapped hardest; collection-artifact x-ray | every timeline source | tool box P8 |
| L-246 | PCA / t-SNE atlas | wide numeric table projected to 2D; clusters = styles, outliers = anomalies | 1.3M providers x 49 measures | tool box P8 |
| L-247 | Catchment population / Voronoi | assign every tract to nearest unit; Voronoi stats without polygons; zones of influence around each point | bank branches, water systems; Ready on numbers, drawn cells blocked | tool box P8; Laboratory; Lab warehouse map |
| L-248 | Event study / before and after a date | day zero is the event, rate before and after; cleanest visual there is, build first | storms vs water violations; MSHA 12 months either side of an accident | tool box P4 build 23; Laboratory |
| L-249 | Bump chart | rank over time, lines crossing | rank churn questions | tool box P1 verb 20 |
| L-250 | Paired dumbbells | one line per twin pair | counterfactual twin | tool box P1 verb 11 |
| L-251 | Scrollytelling county chain | pills, prescriptions, money, deaths, treatment on one county over twenty years | the opioid chain | tool box P4 v2-061 |
| L-252 | Entity card | one key, every table it touches, one page | doctor, member, judge, company, nonprofit, facility, utility, county, country | tool box P7 |
| L-253 | Time-series shape: one line over time | single series | ARCOS pills per day | Laboratory |
| L-254 | Time-series shape: two lines, one axis | compare two series on one clock | payments vs scripts | Laboratory |
| L-255 | Time-series shape: same entity, many years | one sparkline per entity | one water system, 20 years | Laboratory |
| L-256 | Time-series shape: reported vs happened | two clocks; the lag is the chart | sources carrying both clocks | Laboratory |
| L-257 | Picture tags / visual vocabulary | MAP (two county layers, the overlap) · ANIM (year slider is the story) · SCAT (dots that refuse the line) · RANK (same names on top yearly) · NET (one name in three worlds); docket: map, timeline, ranking, flow, other | tagging what the viewer sees; scrollytelling for chains, sankey for money, bump for churn, dumbbell for twins | wonder list; docket v2 visual column; idea moves 20 |
| L-258 | Ripple animation style | easing not snapping; muted palette + soft glow; only the ripple moves, map stays still | if the ripple animation is built | Laboratory |

#### Bookkeeping — tagging and mapping ideas

| id | name | what it is, plain | when to use it | sources |
|---|---|---|---|---|
| L-259 | Hub tag | the join key or place column a wonder pivots on (FIPS, EIN, NPI, CCN, ZIP, UEI, NAME/ADDRESS, CIK, CL_PERSON, MINE_ID, PWSID, EIA_PLANT) | tagging a wonder; counting by hub | wonder list |
| L-260 | Five arcs of the American experience | PLACE (where you live decides) · BODY (your health) · MONEY (who gets it, who gives it) · POWER (who decides, who watches) · WORK and THINGS (the machine running) | grouping wonders into a story | wonder list |
| L-261 | Wonder-to-table mapping template | per wonder: side / table / columns needed / year col / place-key col, then `join:`, `gap:`, `trap:` lines; metadata only, nothing queried | mapping a wonder to what is landed | wonder table map arc 1 |

#### Atlas design ideas (Deepfield atlas and design brief)

| id | name | what it is, plain | when to use it | sources |
|---|---|---|---|---|
| L-262 | Phase it: private workbench first, newsroom site second | phase 1 dense Bloomberg-terminal for Chris; phase 2 scrollytelling one investigation at a time, gated on safety layer | who the viz is for | design brief D1 |
| L-263 | Selective tier visibility | let the 350-edge STEEL spine surface from 20,696 edges; default view overwhelming on purpose, signal pullable | the central UX challenge | design brief D2 |
| L-264 | Node size = degree, not row count | sizing by rows buried everything under a few giant tables | any map of tables | design brief D2 |
| L-265 | Edge width = match count | records that actually intersect | any map of tables | design brief D2 |
| L-266 | Red-string board | detector edges, width = lead count, colour = bridge key (NPI #f4a23a, IMO #3ab0c4, UEI #b07cf0) | leads overview | design brief D2, D3 |
| L-267 | Entity tiers and golden name | provider (NPI) / facility (CCN) / organization (EIN/CIK/UEI) / vessel (IMO/MMSI); golden name by authority rank, NPPES rank 1 beats LEIE rank 4 | dossiers | design brief D2, D4 |
| L-268 | The Plane: four altitudes | ORBIT (join-key bubbles, hubs >50 degree at zoom >8x) > REGION (638 datasets, STEEL/STRONG lit, ~0.55x) > STREET (viewport-culled edges, ~0.12x) > CARD (one dataset + ranked neighbours); hysteresis stops flapping | warehouse from altitude, offline | design brief D5 |
| L-269 | The lensing method | we can't see the thing; we find it by what it bends; pairs that should overlap and measurably don't become the hunt list | the atlas's spine | atlas blueprint 1 |
| L-270 | Four states, not two | LIT (>=1 verified edge) / DARK (real key, matches nothing: the hunt list) / KEYLESS (no identity column: acquisition problem) / UNCHARTED (never entered discovery: a parked decision) | any map of tables; three different jobs | atlas blueprint 2.1 |
| L-271 | Absence as a first-class layer | not a toggle or filter; its own ink, on by default, under the verified mesh like a gravity map under a star chart | atlas rest state | atlas blueprint 1, 3.6 |
| L-272 | Identity gravity | 22 fixed anchor wells, one per key family; each table at the weighted barycenter of its families (fill rate x distinct ratio); collision relaxation; deterministic seed | layout that reads out of the data; monolingual tables orbit tight, polyglots sit in the straits | atlas blueprint 3.1 |
| L-273 | Four honest node channels | luminosity = log(rows) + degree; hue = dominant key family; form = state (LIT filled+glow, DARK hollow ring, KEYLESS bare tick, UNCHARTED faint dot); halo = best proof tier | drawing a table | atlas blueprint 3.2 |
| L-274 | The DARK ring | hollow ring in lit territory beside its well, no corridor reaching it; the most important mark; never banished to a margin | drawing measured absence | atlas blueprint 3.2 |
| L-275 | Edges as bundled corridors | force-directed edge bundling per key family, computed at build; hover a well and its edges ignite as one river | macro view instead of a hairball | atlas blueprint 3.3 |
| L-276 | Tier line grammar | STEEL solid heaviest; CORROBORATED solid half; GEO dashed; BRIDGE dotted arcs routed through the crosswalk node; STRONG thin solid | drawing edges; never more certain than proven | atlas blueprint 3.3 |
| L-277 | Spectral barcodes | one stripe per ID column: hue = key family, brightness = fill rate, solidity = distinct ratio; a 100%-populated sentinel shows bright with a hollow hatched core | a table's face; the trap that fooled a null-check twice can't fool an eyeball | atlas blueprint 3.4 |
| L-278 | The unlit census HUD | four state counts always on screen, "85.1% of the Library is unconnected"; each row is also a filter | atlas chrome | atlas blueprint 3.5 |
| L-279 | The Foundry projection | same nodes left-to-right: LANDING > CONNECT > HUNCH lattice > HYPOTHESIS_CATALOG > Pattern Desk > Reading Room; ~900ms morph, identity persists | where things live vs how things flow | atlas blueprint 3.7 |
| L-280 | Semantic zoom Z0-Z3 | Z0 Field (all glyphs, wells, corridors) > Z1 Precinct (one well, 20-80 tables, all labelled) > Z2 Station (isometric slabs, height = rows, face = barcode) > Z3 Schema (fill/distinct microbars, lifecycle, edge endpoints); hard thresholds, crossfades | atlas navigation | atlas blueprint 4.1 |
| L-281 | The camera | 2.5D orthographic dolly, parallax, scroll = altitude, drag = pan, no roll no tumble; north stays north | atlas | atlas blueprint 4.2 |
| L-282 | Focus dive | double-click: dolly in, rest dims and desaturates, band transitions fire mid-flight | atlas | atlas blueprint 4.2 |
| L-283 | The flight recorder | every dive appends a breadcrumb; Esc flies back along it; always answers "where am I and how did I get here" | atlas; the question that kills other large-graph tools | atlas blueprint 4.2 |
| L-284 | The compass rose | fixed radar of wells + viewport; hover a family and its corridors ignite everywhere ("show me everything money touches") | atlas | atlas blueprint 4.2 |
| L-285 | Search is teleport with a contrail | ~500ms arc, never a hard cut; fading contrail keeps the spatial model | atlas | atlas blueprint 4.2 |
| L-286 | The URL is the state | camera, band, projection, pins, highlights serialize; a pasted link is a receipt | atlas | atlas blueprint 4.2 |
| L-287 | The receipt panel | click an edge: key, tier, matched, match rate, distinct both sides, sample values | every line produces its evidence on demand | atlas blueprint 4.3 |
| L-288 | Pins | right-click drops a survey pin; pinned glyphs stay lit through dimming, band change, morph | keeping a working set | atlas blueprint 4.3 |
| L-289 | The scope law, by camera | every dive ends in receipts; every Esc ends at the whole field; UI resists collapsing into "one nice little story" | atlas resting state | atlas blueprint 4.4 |
| L-290 | Heavy thinking at build time, dumb speed at runtime | compiler emits static atlas.json (layout, bundling, label lists); browser renders a file; Snowflake only for live receipts on registry tables | any big viz | atlas blueprint 5 |
| L-291 | Text is the performance boss | labels, not lines, limit scale; per-band priority lists cap live labels at ~120 | rendering thousands of nodes | atlas blueprint 5.2 |
| L-292 | Lineage: organs not costumes | octopus > bundled corridors; star map > deep field; isometric platforms > station interiors; manufacturing schematic > Foundry; fractal tree > zoom registers | where prior concepts went | atlas blueprint § Lineage |
