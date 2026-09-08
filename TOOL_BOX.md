# The Tool Box

A brainstorming kit, not a manual. It's for asking "what if" against the
warehouse — not for step-by-step execution. Ideas to chase, not instructions
to follow. Everything lives in this one file now — nothing to click through to.

**60 methods. 7 postures. 5 verification checks. Zero required order.**

Last touched 2026-09-08. New method, lens, or posture — add it here first.

---

## Jump to

What's in here · How to use it · The 52 lenses · 8 more methods ·
7 postures · 5 verification checks · Schema matrix · Portfolio picks ·
Coverage gaps · Standing rules

---

## What's in here

| Piece | What it is |
|---|---|
| 52 lenses | patterns and hunches to test against any table, each a check/hit/miss chain |
| 8 more methods | added 2026-09-08, ideas not yet folded into the 52 |
| 7 postures | stances for walking into the data cold |
| 5 verification checks | how you know a hit is real, not noise |
| Schema matrix | pick a schema, see its best-fit lenses, posture, and known traps |

---

## How to use it

This is a thinking tool, not a checklist. Skim it for a hunch, not a recipe.

- Pick a posture — a way of looking, not a procedure
- Pick a lens — the idea you want to test, in plain words
- Pick a table — whatever the schema matrix suggests
- Chase the candidate, get curious, see what turns up
- Only once something feels real: run it past the 5 verification checks
- Write it up after, not before

**Stuck for an idea? Pick blind.**
Close your eyes, point at a lens below, point at a schema in the matrix.
Force the pairing. Half the fun is arguing with a pairing that seems wrong.

**Looking up a lens by name?** Every lens below is bolded — search the page
for it. The schema matrix further down also names which lenses fit which
schema, so you can search from either direction.

---

## The 52 lenses

Each one: check, what a hit means, what a miss means. One worked example,
grounded in the warehouse as of the 2026-09-05 topo map.

### Math laws

**Zipf's law** — big things are rare, small things are common, in a fixed ratio
- Check: rank FEC donors by total dollars given, plot rank against amount
- Hit: a straight line on a log scale — normal, most fields look like this
- Miss: a kink or a cliff — a handful of donors way bigger than the curve predicts

**Benford's law** — real numbers start with digit 1 far more than digit 9
- Check: leading digit of every FEC contribution amount
- Hit: digit 1 leads about 30% of the time, matching the curve
- Miss: digits spread evenly instead — a sign numbers were typed, not counted

**Power law tail** — a few nodes hold almost all the connections
- Check: how many transfers each FEC committee sends or receives
- Hit: a handful of committees dominate, most have almost none — normal for networks
- Miss: everything is roughly even — unusual, worth asking why

**Pareto 80/20** — a small slice of actors carries most of the volume
- Check: do 20% of SEC 13F filers hold 80% of reported value
- Hit: yes, matches — normal concentration
- Miss: value is spread flat across filers — atypical, worth a second look

**Small-world network** — everyone is a few hops from everyone else
- Check: shortest path between any two FEC donors through shared committees
- Hit: short paths everywhere — normal for a connected donor base
- Miss: isolated islands with no bridges — could mean siloed operations

**Preferential attachment** — early actors snowball, latecomers stay small
- Check: do early-cycle FEC filers keep growing faster than late entrants
- Hit: yes — normal "rich get richer" pattern
- Miss: no correlation with entry timing — something else is driving growth

**Log-normal** — most real-world gaps and sizes skew this way, not evenly
- Check: time between filings for the same FEC donor
- Hit: matches the skewed curve — normal filing behavior
- Miss: a hard cutoff or repeating exact interval — looks scheduled, not organic

**Poisson clustering** — random events still cluster sometimes, this tests if it's too much
- Check: are FEC contribution dates bursty around deadlines, more than random predicts
- Hit: bursts match deadline pressure — expected behavior
- Miss: bursts appear on days with no deadline — worth asking what happened that day

### Forensic tricks

**Time of death window** — a gap in the timeline nobody explains
- Check: reporting gaps in FEMA housing registrations after a disaster
- Hit: no gap, or a gap that matches a known office closure
- Miss: an unexplained silent period — data went missing or wasn't filed

**Fingerprint match** — the same unique trait shows up where it shouldn't
- Check: same street address across two different-named FEC committees
- Hit: none found — clean
- Miss: found — could be one person running two committees under different names

**Trace evidence** — a small shared detail links two "unrelated" records
- Check: same registered agent on two unrelated corporate filings
- Miss: shared agent found — the two companies may be connected, not independent

**Alibi check** — a stated fact doesn't match an independent record
- Check: contractor's stated location vs USASPENDING place-of-performance
- Hit: they match — no issue
- Miss: they don't — worth asking why the paperwork disagrees with itself

**Staging vs real** — data arranged to look natural, but the seams show
- Check: suspiciously round totals in USASPENDING contract awards
- Hit: totals are irregular, like real transactions
- Miss: too many exact round numbers — someone may have made them up

**Chain of custody** — who touched the data, when, in what order
- Check: load history on FED_CFPB_HMDA_HISTORIC, reloaded same day per the topo map
- Hit: the reload is explained and logged
- Miss: an unexplained reload or overwrite — treat the table as unverified until checked

**Behavioral profiling** — one actor's habits repeat across many acts
- Check: one FEC filer's amendment timing, does it always land the same day of week
- Hit: no pattern
- Miss: a tic repeats — that's a fingerprint you can use to spot the same actor elsewhere

### Cheap tells

**Round-number clustering** — real money is messy, exact numbers are a flag
- Check: how many FEC donations land on exactly $2,500 or $5,000
- Hit: a normal spread of odd amounts
- Miss: a spike at round numbers — could be legal limits, could be fabrication

**Address reuse** — same P.O. box, different names
- Check: FEC donor addresses shared across multiple donor names
- Miss: found — classic straw-donor pattern, one person funding many "donors"

**Timing tics** — unrelated actors file within minutes of each other
- Check: same-day filing clusters across unrelated FEC committees
- Miss: found — coordination, even if no direct link is stated anywhere

### Network science

**Betweenness centrality** — the one node every path runs through
- Check: which FEC committee sits on the most transfer paths
- Hit: no single dominant node — money moves many ways
- Miss: one committee is the hub — it's a chokepoint worth naming

**Community detection** — clusters nobody labeled as a group
- Check: donor clusters in the FEC contribution graph, unlabeled
- Miss: a tight unlabeled cluster appears — ask what connects them

**Bridge/cut vertex** — remove one node, the graph splits in two
- Check: single shell company holding a UK ownership chain together
- Miss: found — that company is a structural chokepoint, not incidental

**Homophily check** — connected actors are too similar to be luck
- Check: do connected FEC donors share employer more than random chance
- Hit: some overlap, expected among coworkers
- Miss: near-total overlap — may be a bundling operation, not individual giving

### Stats of fraud

**Chi-square uniformity** — categories that are too evenly spread to be real
- Check: spread of FEC contribution amounts across dollar buckets
- Hit: uneven spread, like real behavior
- Miss: suspiciously even spread — could be generated, not observed

**Digit variance test** — Benford's cousin, checks the second digit too
- Check: second digit of USASPENDING award amounts
- Hit: matches the expected curve
- Miss: doesn't match — a second independent flag alongside first-digit Benford

**Regression discontinuity** — a sharp jump right at a legal cutoff
- Check: contribution counts right around the $200 disclosure threshold
- Hit: smooth curve through the threshold
- Miss: a cliff right at $200 — people are structuring below the reporting line

**Cui bono** — who gains, asked before who did it
- Check: who benefited when one committee's transfers spiked
- No hit/miss — it's the question you ask once a flag shows up elsewhere

### Anomaly hunting

**Isolation forest logic** — the single record easiest to separate from the rest
- Check: the one FEC donor record that's most unlike every other, by combined features
- Miss: an outlier stands out sharply — start there, not with a random row

**Z-score sweep** — anything past 3 standard deviations, flagged blind
- Check: every numeric column in FEC contributions
- Miss: values 3+ sigma out — could be data errors or could be real extremes, check both

**Missingness pattern** — what's not there, and is it random
- Check: is a missing employer field on FEC contributions random or clustered by state
- Hit: random — normal data entry gaps
- Miss: clustered — something about that state's filing process is different

**Duplicate near-miss** — two records 95% identical, not 100%
- Check: donor records that match on everything except one digit of an address
- Miss: found — likely the same person, entered twice, maybe on purpose

### Physics and biology analogies

**Entropy measure** — real randomness looks messy, not this clean
- Check: entropy of a self-reported facility's emissions sequence
- Hit: high entropy, like real measurement noise
- Miss: low entropy, oddly smooth — numbers may have been smoothed or invented

**Diffusion/spread rate** — how fast a pattern moves through a network
- Check: how fast a prescribing pattern spreads across providers who share a rep
- Tells you speed, not right or wrong — fast spread with no clinical driver is the flag

**Herding/flocking** — many actors move together with no stated coordination
- Check: multiple committees moving money the same week
- Miss: found — coordinated behavior nobody officially coordinated

### Game theory

**Nash tell** — a move that only makes sense with information nobody admits having
- Check: a bid that only makes sense if the bidder knew a competitor would drop out
- Miss: found — someone had information they shouldn't have

**Signaling** — a small early move announces a bigger one coming
- Check: a small early contribution followed by a much larger bundled one
- A pattern to watch, not a binary flag — small-then-big is the shape

### Text and language

**Stylometry** — the same writer shows up under different names
- Check: boilerplate phrasing across differently-named FEC committee filings
- Miss: matching phrasing — same drafter behind "unrelated" filers

**N-gram fingerprint** — a repeated phrase links unrelated records
- Check: a repeated boilerplate clause across unrelated corporate filing purposes
- Miss: found — a shared template, meaning a shared source or preparer

**Levenshtein distance** — names one typo apart might be the same entity
- Check: donor names differing by one character across records
- Miss: found — likely one person, split into two records by a typo

### Time series

**Autocorrelation** — does today's value predict tomorrow's
- Check: does today's contribution volume for a committee predict tomorrow's
- Hit: yes, smooth trend — normal
- Miss: no relationship, pure noise, or a sudden break — worth flagging the break

**Change-point detection** — the exact date a pattern shifted
- Check: when did a contractor's typical award size change regime
- Miss: a sharp date found — ask what happened around it

**Seasonality check** — a cycle that shouldn't be cyclic
- Check: does a violation rate cycle in a way inspection schedules don't explain
- Miss: found — something other than the official schedule is driving the cycle

**Granger causality** — does A's timing move before B's
- Check: does a lobbying filing move before a contract award, consistently
- Miss: consistent lead-lag found — worth asking about the mechanism

### Geospatial

**Spatial clustering** — events bunch in space more than chance predicts
- Check: do EPA violations cluster tighter than facility density explains
- Miss: yes — a location is over-represented for reasons beyond just having more facilities

**Distance decay** — an effect should fade with distance, does it
- Check: does contribution size fade with distance from a committee's HQ
- Hit: yes, fades as expected
- Miss: no fade, or fades wrong — donors are behaving unlike normal local giving

**Hot-spot mapping** — one place lights up across multiple unrelated datasets
- Check: one ZIP code appearing heavily in FEC, EPA, and CFPB data together
- Miss: found — that place is worth a cross-table look, not just one table

### Causal and bias traps

**Survivorship bias** — you're only seeing what's still around
- Check: are we only seeing UK companies still active, not the dissolved ones
- A warning, not a finding — always ask what got dropped before counting

**Simpson's paradox** — a trend flips when you split the group
- Check: does a lending-denial trend reverse when split by lender size
- Miss: it flips — the aggregate number was hiding the real story

**Regression to the mean** — an extreme value drifts back, that's not a trend
- Check: an extreme contribution spike, does it settle next cycle
- Hit: it settles — was noise, not a trend, don't chase it
- Miss: it doesn't settle — now it might be real

**Confounding variable** — a third thing is driving both sides of a link
- Check: is something else driving both contribution timing and contract timing
- A discipline, not a query — never call two correlated things "connected" until ruled out

### Epidemiology

**Contact tracing logic** — who touched whom, in what order
- Check: order of committee-to-committee transfers, treated like a contact chain
- Use: traces how money or influence actually moved, step by step

**R-naught style spread** — is one actor's pattern replicating outward
- Check: is one donor's giving style showing up in new committees over time
- Miss: yes, replicating — something is spreading beyond one actor's own choices

### Info theory

**Compressibility test** — data that's too repetitive compresses too well
- Check: does a self-reported dataset compress far more than real-world noise should allow
- Miss: compresses unusually well — may be synthetic or copy-pasted, not measured

**Mutual information** — two columns share more signal than makes sense
- Check: does contract award size predict a firm's lobbying spend, same firm
- Miss: strong shared signal — the two aren't independent, worth naming the link

---

## 8 more methods, added 2026-09-08

Ideas, not procedures. Each one is a different way of thinking about the
data, not a specific query to run.

| Method | The idea |
|---|---|
| Bayesian inference | update your belief as each new piece of evidence lands, don't judge on one look |
| Monte Carlo simulation | run a pattern thousands of times in your head, see what "normal" even looks like |
| Dimensionality reduction | collapse a pile of columns down to the few that actually matter |
| Control charts / SPC | ask if something drifted out of its normal range, factory-floor logic |
| Diff-in-diff | compare a before/after against a group that wasn't touched, the only one that argues cause |
| Hash / checksum matching | find records that are byte-identical under different labels |
| Markov chain modeling | ask if the next state only depends on right now, not the whole history |
| Natural language classifier | sort messy free-text fields into buckets automatically |

---

## 7 postures

Not patterns — stances. How you walk into the data before picking a lens.

| Posture | The move | What it surfaces |
|---|---|---|
| Follow one entity | pick a name, pull every table it touches | a life story, not a stat |
| Reverse the question | start from an outcome, walk back | the actor everyone missed |
| Chase a random row | follow every foreign key three hops out | blind spots you'd never search |
| Assume guilt first | take the top-10, try to prove it's clean | forces rigor on the "normal" ones |
| Absence hunting | ask what should be there and isn't | the gap is the finding |
| Cross-domain collision | join two schemas with no business relation | correlations nobody built for |
| Outsider's question | ask what a journalist or lawyer asks first | plain beats clever |

---

## 5 verification checks

A lens plus a posture finds a candidate. This layer decides if it's real.
Skip this layer and every finding is a guess dressed as a fact.

**Provenance skepticism**
- Check: who collected this table, what's their incentive to shade it
- Hit: source is neutral, third-party, no stake in the number
- Miss: source benefits from the number looking a certain way — treat the finding as soft

**External baseline**
- Check: does an outside source confirm the same fact independently
- Hit: matches a second, unrelated source
- Miss: only your warehouse shows it — could be a load bug, not a real pattern

**Replication check**
- Check: does the finding hold in a second year, state, or dataset
- Hit: holds across at least one more slice
- Miss: one-off — likely noise, not a pattern

**Red-team your own pipeline**
- Check: could the load script or a join be the actual cause, not the data
- Hit: pipeline reviewed, finding survives
- Miss: a script bug or duplicate join explains it — not a warehouse finding, a code bug

**The story test**
- Check: is this true AND does it explain something someone would care about
- True and boring: log it, move on
- True and explains something: that's the portfolio piece

---

## Schema matrix

Desk review only — no live queries, no invented table or column names beyond
what's documented. "Best-fit" means the schema's known shape plausibly
supports the lens, not that it's been tested there.

### HEALTH — 98 tables, 363.2M rows
Best-fit lenses:
- **Benford's law / digit variance** — CMS Open Payments and Part D carry real dollar amounts (`TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS`, `Tot_Drug_Cst`)
- **Power law tail / Pareto 80/20** — provider- and manufacturer-level payment concentration, natural shape for NPI-anchored money
- **Network science (betweenness, community detection)** — NPI is the widest identity bridge, 59 wired tables
- **Homophily / herding** — shared-rep prescribing patterns fits Part D prescriber data
- **Missingness pattern** — heavy documented suppression makes this a natural missingness testbed
Posture: **Follow one entity** — pull one NPI across NPPES, Open Payments, Part D, LEIE
Trap warning: LEIE NPI join only covers 10.6% of rows, a floor not a full ban list; NPPES EIN/TIN columns are `<UNAVAIL>` on every row, never build an EIN edge from NPPES; Open Payments manufacturer ID is a 12-digit numeric ID, not a payment amount

### FINANCE — 56 tables, 102.1M rows
Best-fit lenses:
- **Benford's law / digit variance** — FEC individual contributions and USAspending awards
- **Round-number clustering / regression discontinuity** — contribution limits ($200, $2,500) are documented thresholds
- **Power law / Zipf / Pareto** — donor and committee-level concentration
- **Betweenness / community detection** — committee-to-committee transfer graph
- **Address reuse / fingerprint match** — straw-donor patterns via shared address/name
Posture: **Reverse the question** — start from a spend spike, walk back to donors
Trap warning: FEC committees reuse IDs across cycles with no cycle column, join the DIM table not raw; Schedule E carries prank filings worth tens of billions; committee-to-committee is 93% earmark memos needing `MEMO_CD <> 'X'` filter; independent-expenditure mart totals read ~20x the real FEC figure

### POLITICS — 79 tables, 21.0M rows
Best-fit lenses:
- **Signaling / Nash tell** — lobbying-then-legislation timing chains
- **Change-point detection / Granger causality** — lobbying filing vs. bill/contract timing
- **Stylometry / N-gram fingerprint** — boilerplate phrasing across filings
- **Cui bono** — committee membership vs. money flow
Posture: **Cross-domain collision** — join lobbying/committee data against FINANCE money with no built relation
Trap warning: committee membership has no cycle-aware dedupe, 5.7x fan-out joining to money; PARTY column holds 'majority'/'minority', not D/R; no congressional-district geometry exists; EDUCATION schema, not POLITICS, actually holds lobbying/Fed-rate tables mislabeled by folder name

### JUSTICE — 65 tables, 57.9M rows
Best-fit lenses:
- **Small-world network / betweenness** — DOCKET key reaches 17 tables, a real case-linkage graph
- **Duplicate near-miss / Levenshtein** — litigant/party name collisions are heavily documented
- **Survivorship bias** — active-only exclusion/case snapshots
- **Time of death window** — docket filing gaps
Posture: **Absence hunting** — missing rosters, e.g. judges who resigned mid-term, are a documented gap type
Trap warning: common-surname case names ("SMITH V. UNITED STATES") are noise unless distinctive; financial disclosure YEAR is column-shifted text on over half of rows; judge district codes need `ASSIGNED_TO_ID`, not `FILEJUDG`

### ENVIRONMENT — 75 tables, 107.7M rows
Best-fit lenses:
- **Spatial clustering / hot-spot mapping** — EPA facility and emissions data is inherently geospatial
- **Entropy measure** — self-reported emissions sequences
- **Distance decay** — facility-to-community effects
- **Bridge/cut vertex** — FRS_ID is the environmental identity bridge, 20 wired tables
Posture: **Cross-domain collision** — FRS facility identity joined against FINANCE or JUSTICE enforcement
Trap warning: a junk-hub geometry (`INTL_FR_DATA_GOUV_FULL.SPATIAL_GEOM`) contains every US point and fakes centrality; lat/lon in TRI_FACILITY are packed DDMMSS with swapped pairs

### HOUSING — 18 tables, 45.8M rows
Best-fit lenses:
- **Regression discontinuity / Simpson's paradox** — HMDA lending-denial trend by lender size
- **Spatial clustering / hot-spot mapping** — HOLC redlining polygons, FEMA registrations
- **Survivorship bias** — HMDA originations-only file, zero denials documented separately
Posture: **Absence hunting** — HMDA has originations but no denials, a real documented gap
Trap warning: `HOUSING__FED_MAPPING_INEQUALITY` mart is 1,155 rows vs 10,154 in landing, 89% loss; HOLC_ID is not an id; FEMA IA FIPS is unpadded text creating false distinct-state collisions

### MARITIME — 1 table, 58.1M rows
Best-fit lenses:
- **Autocorrelation / seasonality** — AIS vessel-position time series
- **Spatial clustering** — vessel movement/port clustering
- **Diffusion/spread rate** — vessel-route pattern propagation
Posture: **Chase a random row** — follow one IMO-keyed vessel across its position history, single-table schema
Trap warning: none documented specifically for NOAA_AIS; IMO reach is only 9 tables, a single-table schema has essentially no cross-table verification in-schema

### ECONOMICS — 44 tables, 43.1M rows
Best-fit lenses:
- **Benford's law / digit variance** — SEC 13F holdings, CFPB HMDA dollar fields
- **Pareto 80/20 / power law** — 13F filer concentration
- **Log-normal / Poisson clustering** — filing interval and timing patterns
- **Mutual information** — contract size vs. lobbying spend, cross-schema but economics-anchored
Posture: **Assume guilt first** — take top-10 13F filers, try to prove clean
Trap warning: none specific to SEC 13F located; general "everything is TEXT" cast trap applies warehouse-wide

### CORPORATE_REGISTRY — 11 tables, 29.7M rows
Best-fit lenses:
- **Trace evidence** — shared registered agent across "unrelated" filings
- **Bridge/cut vertex** — UK PSC ownership chains, single shell company as chokepoint
- **Survivorship bias** — active-companies-only visibility
- **N-gram fingerprint** — boilerplate clauses across filing purposes
Posture: **Follow one entity** — walk a COMPANY_NO/LEI through PSC ownership layers
Trap warning: `UK_COMPANIES_HOUSE_PSC` stopped mid-load, ~7M of an expected 10M+ rows, any count is a floor

### IMMIGRATION — 15 tables, 19.9M rows
Best-fit lenses:
- **Time of death window** — case-processing gaps
- **Missingness pattern** — structurally broken parallel tables are a direct signal
- **Change-point detection** — case volume/backlog shifts
Posture: **Absence hunting** — the working case table vs. the broken parallel load is itself the finding
Trap warning: `IMMIGRATION__FED_EOIR_CASE_DATA` is a broken one-column parallel load, use `FED_EOIR_CASES` instead; 12 tables mislabeled "immigration" in the registry domain column are actually CMS/EPA data

### CONSUMER_PROTECTION — 1 table, 17.2M rows
Best-fit lenses:
- **Text/language (stylometry, n-gram)** — CFPB complaints are narrative text
- **Time series (seasonality, autocorrelation)** — complaint volume over time
- **Chi-square uniformity** — complaint category distribution
Posture: **Outsider's question** — what would a consumer-rights lawyer ask first
Trap warning: none specific found; single-table schema limits cross-verification, external baseline needed

### CONSUMER_SAFETY — 4 tables, 12.4M rows
Best-fit lenses:
- **Change-point detection** — recall/complaint volume shifts
- **Spatial clustering** — complaint geography if present
- **Missingness pattern** — NHTSA complaints documented as headerless/positional
Posture: **Absence hunting** — headerless columns mean most fields are effectively unusable by structure
Trap warning: `FED_NHTSA_COMPLAINTS` is headerless `C1..C54`; only C3/C4/C5/C6/C8/C12 are known-usable, 110k rows have a blank date

### REFERENCE — 34 tables, 8.4M rows
Best-fit lenses:
- **Missingness pattern / provenance skepticism** — reference/lookup tables are where mislabeling is most consequential
- **Duplicate near-miss** — code/lookup table redundancy
Posture: reference tables mainly serve other schemas' joins, not lenses of their own
Trap warning: none specific found; treat as low-signal for most of the 52 lenses given its lookup-table nature

### LABOR — 12 tables, 7.2M rows
Best-fit lenses:
- **Chi-square uniformity / column-shift detection** — DOL OLMS shows exactly this failure mode
- **Missingness pattern** — LDA lobbying coverage gaps, 1999-2010 and 2020-2021 only
- **Regression discontinuity** — wage/threshold rules
Posture: **Red-team your own pipeline** — the OLMS shortage-amount trap is a pipeline artifact, not a real signal
Trap warning: `FED_DOL_OLMS SHORTAGE_AMOUNT` non-zero rows are all column-shifted junk, no real shortage dollars in that column

### EDUCATION — 17 tables, 4.6M rows
Best-fit lenses:
- **Cross-domain collision** — this schema is a grab-bag (CFTC, Fed rates, political ads, Senate lobbying)
- **Provenance skepticism** — given the mislabeling, source-checking every table is mandatory
Posture: **Outsider's question** — "wait, why is this in EDUCATION?" is literally the finding
Trap warning: EDUCATION schema holds non-education tables — CFTC futures, Fed interest rates, Google political ads, Senate lobbying filings; schema name is not a content guarantee

### SCIENCE_RESEARCH — 6 tables, 2.5M rows
Best-fit lenses:
- **Entropy measure** — measurement/research data noise characteristics
- **Compressibility test** — synthetic-vs-measured data detection
Posture: **Chase a random row** — small schema, best explored table-by-table
Trap warning: none documented; smallest, least-verified schema, treat any finding as needing external baseline before trusting

### TRANSPORT — 12 tables, 2.2M rows
Best-fit lenses:
- **Missingness pattern** — mangled-header table is a direct example
- **Spatial clustering** — airport/facility geography
Posture: **Red-team your own pipeline** — the ADIP header trap is a load bug, not a data finding
Trap warning: `TRANSPORT__FED_FAA_ADIP_PRIVATE_AIRPORTS` loaded with mangled headers, unusable until reloaded

### OPEN_DATA — 12 tables, 1.7M rows
Best-fit lenses:
- **Missingness pattern / provenance skepticism** — PORTAL_CKA structure is column-partial by construction
- **Duplicate near-miss** — ROWID collisions across monthly resources
Posture: **Red-team your own pipeline** — this schema's shape is dominated by loader artifacts, not underlying signal
Trap warning: portal tables are folders of resources with non-shared headers, up to 71 of 105 columns partially filled on one table; ROWID is not a primary key; MERCHANT strings are terminal strings, not merchant identity

### TIMELINE — 32 tables + 403 views, 1.2M rows
Best-fit lenses:
- **Change-point detection / autocorrelation** — this schema's entire purpose is time-indexed rollups
- **Seasonality check** — built for exactly this
Posture: **Absence hunting** — stale materialized rollups behind "green" guards are the documented failure mode
Trap warning: `_INDEX` rollup tables are materialized and can go stale silently; view column lists freeze at create time and break silently on upstream changes; SNAPSHOT_DATE reflects when read, not when the event happened

### ENERGY — 29 tables, 0.5M rows
Best-fit lenses:
- **Time series (seasonality, change-point)** — EPA CAMPD daily emissions, EIA plant/utility data
- **Spatial clustering** — plant-level geography
Posture: **Chase a random row** — smallest schema by rows among the 20
Trap warning: `_INGESTED_AT` on EPA CAMPD reads as epoch-microseconds-as-seconds on at least 7 tables, never trust it as a date without a range check first

---

## The 5 lenses picked for the portfolio, 2026-09-08

| Rank | Lens | Schema | Why |
|---|---|---|---|
| 1 | Benford's law | FINANCE, FEC contributions | classic fraud test, one query, instant read |
| 2 | Address reuse | FINANCE, FEC donor records | straw-donor story, plain-English finding |
| 3 | Network centrality | HEALTH, NPI-anchored tables | one hub provider ties Open Payments to Part D |
| 4 | Cross-domain collision | ENVIRONMENT x JUSTICE, FRS_ID | same facility, enforcement in two schemas |
| 5 | Signaling | POLITICS x FINANCE, lobbying vs. award timing | who moved first — filing or the contract |

---

## Coverage gaps

**12 of the 52 lenses had zero schema hits in the desk review:**
Preferential attachment, Alibi check, Staging vs real, Chain of custody,
Behavioral profiling, Timing tics, Isolation forest logic, Z-score sweep,
Regression to the mean, Confounding variable, Contact tracing logic,
R-naught style spread.

Zero hits means the desk review found no obvious metadata shape for it —
not that it's impossible. These need a live look, not another documented one.

**Thin-coverage schemas** — metadata doesn't obviously support many of the 52:
- MARITIME and CONSUMER_PROTECTION — single-table schemas, no internal cross-table lens, weak in-schema verification
- REFERENCE — mostly lookup tables, no money, no timestamps, no network structure
- SCIENCE_RESEARCH — smallest footprint, no traps recorded, no one has stress-tested it
- ENERGY, TRANSPORT, OPEN_DATA — small and load-artifact-dominated; several "findings" here are already known pipeline bugs

**The concentration pattern**: HEALTH, FINANCE, ECONOMICS, ENVIRONMENT, and
CORPORATE_REGISTRY carry the deepest lens coverage because they anchor the
warehouse's four real identity bridges — NPI, EIN, FRS_ID, CCN/UEI. Every
other schema inherits network lenses only secondhand, through those bridges.

---

## Standing rules

- Metadata mapping was desk review only — no live queries, no invented columns
- Check `.claude/traps.md` before trusting any column named here
- A candidate isn't a finding until it survives the 5 verification checks
- Nothing here is ranked by default — pick a posture, pick a lens, run the loop
