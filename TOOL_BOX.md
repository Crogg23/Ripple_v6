# The Tool Box

## Start here — what this is, in plain words

There's a data warehouse. It holds US and UK **public records** — the
paperwork governments already publish and nobody reads. Company filings,
doctor payments, campaign donations, pollution reports, court dockets,
housing loans, workplace injuries. The landed files alone run to 1.37
billion rows across 2,214 tables.

Every one of those records is public. The point isn't getting the data.
The point is that **nobody has ever put these files next to each other.**

The EPA tracks the pipe. Medicare tracks the patients. Nobody joins them.
The tax form says what the CEO earns. The Medicare report says what the
hospital gave away. Two filings that never meet.

**That's the whole project: put two files side by side that were never
meant to meet, and see what falls out.**

This document is the kit for doing that. It holds every method, every
pattern, every constraint, and every question that exists for this
warehouse. If an idea about it lives anywhere, it lives here.

```
WHAT'S IN THE WAREHOUSE           HOW MUCH
──────────────────────────────    ─────────────────────────
raw landed files                   2,214 tables, 1.37B rows
cleaned up, ready to use             676 tables, 908M rows
subject areas                         20, health to maritime
```

The cleaned-up tables are built from the raw ones, so don't add those
two row counts together. Sizes are from the 2026-09-05 survey.

---

## What you'll find in here, and why each part exists

| Part | What it is | Why it's here |
|---|---|---|
| 1 · The moves | 27 ways to walk into the data | you need an angle before a query |
| 2 · The lenses | 61 known patterns to test against | real data either fits a known shape or breaks it |
| 3 · The shelf | what the warehouse will and won't allow | some joins look fine and return 8% |
| 4 · The questions | 542 specific questions, plus 25 builds | so you never start from a blank page |
| 5 · The checks | 5 ways to know a hit is real | most exciting findings are bugs |

**61 lenses · 27 moves · 5 checks · 542 questions · 25 cross-joins**

Overlap is fine and expected. One question can use six tools. One tool
serves fifty questions. What's not fine is a gap — an idea about this
warehouse that lives somewhere else. Everything lands here first.

Last touched 2026-09-08.

---

## The words used in this file

Nothing here is jargon for its own sake. Every label below is either
counted from the data or copied from a note someone wrote by hand.

| Word | What it means here |
|---|---|
| warehouse | the whole pile of public records, raw files plus cleaned tables |
| schema | a subject area — HEALTH, FINANCE, ENVIRONMENT, and 17 more |
| table | one file of records, like every Medicare payment in 2022 |
| key | the id that lets two tables be joined — a doctor's NPI, a company's EIN |
| bridge | a table carrying two different kinds of key, letting a chain turn |
| chain | a path through several tables, each hop changing the subject |
| turn | one point where a chain changes what it's about — person to place |
| move | a way of walking into the data before you pick a pattern |
| lens | a known pattern you test the data against, like Benford's law |
| hit | the pattern showed up |
| miss | the pattern didn't — often just as interesting |
| docket | the running list of questions, tracked in `docket/docket.csv` |
| trap | a column that looks real and isn't, logged in `.claude/traps.md` |

### The ids that do the joining

Part 3 leans on these constantly. Each is a code that identifies one thing
across many different files.

| Id | What it identifies |
|---|---|
| NPI | one doctor or clinician, in Medicare records |
| CCN | one facility — a hospital, nursing home, clinic |
| EIN | one organisation, on its tax filings |
| CIK | one company, in SEC securities filings |
| LEI | one legal entity, in the global financial registry |
| UEI / DUNS | one business, as a federal contractor |
| FRS_ID | one polluting facility, in EPA records |
| PWSID | one public water system |
| NPDES_ID | one water-discharge permit |
| BIOGUIDE | one member of Congress |
| FIPS | one county or state |
| ZCTA | one ZIP code area |
| CL_PERSON_ID | one person, in court records |
| IMO / MMSI | one ship |

And the source names that keep appearing:

| Name | What it is |
|---|---|
| NPPES | the national registry of every US clinician |
| HCRIS | hospitals' annual financial reports to Medicare |
| LEIE | the list of people banned from billing Medicare |
| LDA | federal lobbying disclosure filings |
| ECHO | EPA's enforcement and compliance history |
| TRI | EPA's toxic release inventory |

---

## Jump to

| Part | What's in it |
|---|---|
| 1 · The moves | 7 postures, 20 verbs — how you walk in |
| 2 · The lenses | 53 patterns plus 8 more methods |
| 3 · The shelf | key rules, bridges, chains, schema matrix, gaps |
| 4 · The questions | 542 from the docket, 25 cross-join builds |
| 5 · The checks | 5 ways to know a hit is real |
| Picks | the 5 chosen for the portfolio |

---

## How to use it

A thinking tool, not a checklist. Skim for a hunch, not a recipe.

- Pick a move — a way of looking, not a procedure
- Pick a lens — the pattern you want to test, in plain words
- Pick a table — the schema matrix suggests where
- Check the key rules before chaining anything
- Chase the candidate, get curious, see what turns up
- Only once something feels real: run the 5 checks
- Write it up after, not before

**Stuck? Pick blind.** Point at a move, point at a schema, force the
pairing. Half the fun is arguing with one that seems wrong.

**Looking something up?** Every lens, move and subject is bolded or
headed — search the page for it. Lookup works from either direction.

---

# Part 1 — The moves

A move is the angle you take before you touch a query. Not what pattern
you're testing — how you're walking in. Most people walk in one way:
"do these two things correlate?" There are twenty-seven ways.

Two kinds here. **Postures** are stances — follow one name, or start from
the outcome and walk backward. **Verbs** are actions on the data — who
stopped filing, who was never inspected, who moved first.

## The 7 postures

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

---

## The 20 verbs

Pulled from `docket/idea_moves_20_2026-09-07.md`, 2026-09-07.
Every docket idea before these used one of three moves: describe one
table, join two, join many. These are the other twenty. None need a
new table, a new key, or a new load.

### 1 · Absence — the row that should exist and does not

Not who violated. **Who was never looked at.**

- **The facilities nobody ever inspected.** `ENVIRONMENT__FED_EPA_ECHO` carries inspection
  counts per facility. Filter to zero across the whole record, size the dot by what it emits
  from `ENVIRONMENT__FED_EPA_TRI_BASIC_2023`.
- Hit: large emitters with a decade of zero inspections, named and mapped.
- Miss: coverage is even, which quietly rebuts a common claim.

Same move elsewhere: doctors with no payment row at all, counties with no provider,
water systems with no site visit in `ENVIRONMENT__FED_EPA_SDWA_SDWA_SITE_VISITS`.

### 2 · Precedence — who moved first

Not "do A and B correlate." **Does A reliably precede B.**

- **Does the inspection find the violation, or chase it?** `ENVIRONMENT__FED_EPA_NPDES_NPDES_INSPECTIONS`
  against `ENVIRONMENT__FED_EPA_NPDES_NPDES_PS_VIOLATIONS`, same permit, dated.
- Hit: inspections cluster *after* violations surface, so enforcement is reactive.
- Miss: inspections lead, and the system works as designed.

Event-study chart. Day zero is the first event. Everything else lines up around it.

### 3 · Digit tests — numbers that were negotiated, not measured

Benford's law on leading digits. Real measurements obey it. Haggled numbers do not.

- **Do penalty dollars look computed or bargained?** `ENVIRONMENT__FED_EPA_RCRA_ENFORCEMENTS`
  final penalty, `LABOR__FED_MSHA_VIOLATIONS` proposed against paid, `JUSTICE__FED_FDIC_ENFORCEMENT_ORDERS`.
- Hit: leading-digit distribution bends away from Benford by agency, so fines are settled not calculated.
- Miss: it fits, and the penalty math is honest.

### 4 · The impossible zero

Round-number clustering at the bottom.

- **Which employers report exactly zero injuries?** `LABOR__FED_OSHA_ITA_300A_SUMMARY_2024` carries
  employee count and hours worked alongside injury counts. Zero injuries at 900,000 hours is a claim.
- Hit: zero-reporting rate varies wildly by industry at the same hours.
- Miss: zero is normal in office work and the flag is noise.

### 5 · Same entity, two agencies, two answers

The move nobody makes. **One EIN telling different stories on different forms.**

- **Employee counts.** `LABOR__FED_OSHA_ITA_300A_SUMMARY_2024` employee count against
  `ECONOMICS__FED_DOL_FORM5500` participant count against `ECONOMICS__FED_IRS_BMF` revenue class.
- Hit: the same tax ID reports headcounts that cannot both be true.
- Miss: definitions differ cleanly and the gap is explainable, which is worth stating once.

This is the warehouse's single best structural advantage. Nobody else has the forms side by side.

### 6 · Disappearance — who stopped filing

- **The hospitals that go quiet.** `HEALTH__FED_CMS_HCRIS` is one row per hospital per fiscal year.
  Find the last year each stops appearing, then look at the three years before.
- Hit: the numbers were already bad, so the dropout is predictable.
- Miss: they vanish healthy, which means the filing system loses people for other reasons.

Same move: `ECONOMICS__FED_IRS_AUTO_REVOCATIONS`, `LABOR__FED_DOL_OLMS` unions, water systems.

### 7 · Rebirth — same building, new name

- **Ownership churn at penalised facilities.** `HEALTH__FED_CMS_NURSING_HOME` chain and ownership
  against `HEALTH__FED_CMS_NURSING_HOME_PENALTIES` dates, and the certification-change history in
  `HEALTH__FED_CMS_POS_OTHER`.
- Hit: ownership changes cluster in the months after a fine.
- Miss: churn is random against penalty dates.

### 8 · Address collision — many things at one door

Chris's own example, generalised.

- **Which single addresses host absurd counts.** `CORPORATE_REGISTRY__INTL_UK_COMPANIES_HOUSE`,
  `CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_ADDRESSES`, `HEALTH__FED_CMS_NPPES` practice address,
  `JUSTICE__FED_ATF_FFL`.
- Hit: one mailbox with four hundred companies, or forty doctors, at a residential address.
- Miss: the tail is thin and it is all real office buildings.

### 9 · The narratives — text nobody has read

Six tables carry free text and none of the 542 ideas open them.

| Table | Text it holds |
|---|---|
| `LABOR__FED_OSHA_ITA_CASE_DETAIL_2023` | what happened, in the employer's words |
| `LABOR__FED_MSHA_ACCIDENTS` | the mine accident narrative |
| `HOUSING__FED_MAPPING_INEQUALITY` | the 1930s grader's written justification |
| `CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS` | the complainant's own account |
| `JUSTICE__FED_COURTLISTENER_PARENTHETICALS` | how courts summarise each other |
| `HISTORY__FED_WPA_SLAVE_NARRATIVES` | full interview transcripts |

- **The verbs of injury.** Most common action words in the OSHA narratives, by industry.
- Hit: an industry's injuries have a signature verb and a signature body part.
- Miss: narratives are boilerplate and say nothing the codes did not.

### 10 · Weird for your own kind

Not the national outlier. **The outlier inside a matched peer group.**

- **Peer-group billing.** `HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER`
  carries specialty, state, and the patient mix by age, race and chronic condition. Build the cohort,
  then rank inside it. `COHORT_QUEUE` already does this shape for injuries.
- Hit: an ordinary-looking biller is three deviations above their true peers.
- Miss: peer variance swallows everyone and national ranking was right all along.

### 11 · The counterfactual twin

- **Two hospitals, matched on everything but one thing.** `HEALTH__FED_CMS_HOSPITAL_COMPARE` and
  `HEALTH__FED_CMS_HCRIS`: match on beds, region, patient mix, then compare on ownership type.
- Hit: the twin pairs diverge on the one variable you held out.
- Miss: matched pairs perform alike and ownership does not explain outcomes.

Visual: paired dumbbells, one line per twin.

### 12 · Network position, not network size

- **Who is the broker.** `CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_RELATIONSHIPS`, 3.3M links.
  Rank by betweenness, not by degree. The node whose removal splits the graph.
- Hit: a low-profile intermediary sits on more paths than any famous name.
- Miss: brokers are the obvious big firms, which is still a clean finding.

Same move on cosponsorship and on 13F co-holding.

### 13 · Cadence — when the filing arrives

The timing of disclosure is itself disclosure.

- **Friday-night and year-end dumps.** `REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS` publication dates,
  recall dates in `CONSUMER_SAFETY__FED_NHTSA_RECALLS`, filing dates across SEC insider tables.
- Hit: bad news clusters on Fridays and on 31 December.
- Miss: publication is uniform and the folklore is wrong.

Visual: a clock face or a day-of-week heatmap, not a line.

### 14 · Reciprocity — money that goes both ways

- **Circular committee transfers.** `FINANCE__FED_FEC_COMMITTEE_TO_CANDIDATE`: does A give to B
  while B gives to A, in the same cycle?
- Hit: closed loops of committees passing the same money around.
- Miss: flow is one-directional and hierarchical.

### 15 · Staleness — acting on old information

- **Flood maps older than the storms.** `HOUSING__FED_FEMA_NFIP_COMMUNITY_STATUS_BOOK` carries the
  date each community's flood maps took effect. Compare to storm history in
  `ENVIRONMENT__FED_NOAA_STORM_EVENTS`.
- Hit: communities hit repeatedly are still regulated on 1970s maps.
- Miss: maps get refreshed after damage and the system self-corrects.

Same move: last inspection date on `ENVIRONMENT__FED_NID_DAMS`.

### 16 · Where the government even looks

Not the finding. **The looking.**

- **Air monitor placement.** `ENVIRONMENT__FED_EPA_AQS_SITES` has open and close dates and the land
  use around each monitor. Against county population and emissions.
- Hit: the places emitting most are monitored least, so the data itself is biased.
- Miss: placement follows population and emissions sensibly.

This move reframes every other chart in the warehouse, because it questions the denominator.

### 17 · Where the warehouse contradicts itself

The shelf holds duplicate sources. **The disagreement is a chart.**

| Pair | The gap |
|---|---|
| `ENVIRONMENT__FED_EPA_FRS_FACILITIES` vs `ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES` | about 85,000 IDs appear in only one |
| `FINANCE__FED_SENATE_EFD_PTR` vs `FINANCE__FED_SENATE_STOCK_WATCHER` | official filing against the tracker |
| `HEALTH__FED_CMS_NURSING_HOME` vs `HEALTH__FED_NURSINGHOME411` | CMS against an independent build |
| `SCIENCE_RESEARCH__FED_RETRACTION_WATCH` vs `SCIENCE_RESEARCH__XC_RETRACTION_WATCH_DATABASE` | two pulls, 203 rows apart |

- Hit: public data disagrees with itself by a measurable margin, source by source.
- Miss: the copies match and the redundancy is just storage.

### 18 · Every line in the sand

The meal-cap fingerprint was one instance. There are many thresholds.

- `ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS` — bunching at exactly $150,000
- `ECONOMICS__FED_FAC_SINGLE_AUDIT` — the federal-spend audit trigger
- `HEALTH__FED_CMS_OPEN_PAYMENTS` — the $125 meal line, already proven
- Hit: a spike immediately below every reporting line in the warehouse.
- Miss: distributions are smooth across the threshold.

Visual: one page, one histogram per threshold, all with the line drawn.

### 19 · The week it always happens

- **Seasonal signatures.** `JUSTICE__FED_FBI_NICS_CHECKS` by week against holidays,
  overdose by month, storm damage by season.
- Hit: the same calendar week spikes every single year.
- Miss: the seasonality is weak and the pattern is event-driven.

### 20 · Rank churn — who climbed, not who is on top

- **Movement as the subject.** Top pharma payers year over year in
  `HEALTH__FED_CMS_OPEN_PAYMENTS`, counties by overdose rate, employers by injury rate.
- Hit: the list looks stable at the top but churns violently below it.
- Miss: rankings are frozen, which says the market is closed.

Visual: bump chart. Lines crossing is the whole point.

---

---

# Part 2 — The lenses

A lens is a pattern the real world is known to follow. Money, rankings,
timing, networks — each has a shape it normally takes. You hold the lens
up to a table and ask one question: does the real data fit, or fight?

Fighting is the interesting answer. Numbers that don't follow Benford's
law were probably typed, not counted.

## The 53 lenses

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

---

# Part 3 — The shelf

What the warehouse will and won't allow, before you build anything.

The thing that kills most ambitious joins isn't a bad idea. It's a weak
key. Some ids match 100% of the time and you can chain them ten deep.
Others match 8%, and one of those hops turns your finished number from
a rate into an anecdote — no matter where in the chain you spend it.

Read the key rules before designing anything with more than two tables.

## Key rules — how deep a chain survives

From `docket/join_depth_ceiling_2026-09-07.md`, 2026-09-07.
Depth isn't the constraint. The **kind of key** is.

```
hops   all steel   county FIPS   one cross-key hop anywhere
  2      96.0%        72.2%              8.8%
  4      92.2%        52.2%              8.5%
  6      88.6%        37.7%              8.1%
 10      81.7%        19.7%              7.5%
```

A cross-key hop costs the same at hop two or hop nine. It caps the
whole chain at a sample, forever.

| Key class | Match rate | Chain rule |
|---|---|---|
| NPI, CCN, FRS_ID, PWSID, NPDES_ID, LEI, CL_PERSON_ID | 98-100% | chain freely |
| EIN, CIK, FEC ids | 86-100% | chain freely |
| FIPS | 73-100% | terminal only, never a pivot |
| UEI, DUNS | 10-80% | one hop, then stop |
| CIK~EIN, EIN~UEI, DUNS~UEI | 2-16% | sample, never a rate |
| NAME@ZIP | 8% | sample, multi-word names only |

Only hard keys bridge: NPI, EIN, CIK, DUNS, CCN, IMO, MMSI, UEI, LEI.
Code keys never bridge: NAICS, SIC, NCES, DOCKET, PATENT, FIPS, ZIP.

**The five rules that fall out**

- Steel keys chain as deep as you like — ten hops still returns four in five
- FIPS is a destination, never a doorway — aggregate there and stop
- One cross-key hop caps the chain at a sample — spend it last, or never
- Twelve bridge tables exist — every turn must land on one of them
- Six turns is today's ceiling — a seventh needs a bridge nobody built

### The 12 bridges — the real budget

A hop needs a table carrying **both** keys. These are the ones that exist.

| Bridge table | Rows | Turns |
|---|---|---|
| `HEALTH__FED_CMS_FACILITY_AFFILIATION` | 2,260,193 | NPI ➔ CCN |
| `ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK` | 5,300,149 | FRS_ID ➔ corporate ID |
| `ECONOMICS__INTL_GLEIF_RELATIONSHIPS` | 485,285 | LEI ➔ parent LEI |
| `HEALTH__FED_CMS_OPEN_PAYMENTS_PROFILE_SUPPLEMENT` | 1,697,025 | payment profile ➔ NPI |
| `HEALTH__SAM_EXCLUDED_PROVIDERS` | 16,144 | SAM entity ➔ NPI |
| `HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES` | 19,038 | NPI ➔ CCN ➔ parent centre |
| `POLITICS__MEMBER_CROSSWALK` | 12,794 | BIOGUIDE ➔ a dozen id systems |
| `POLITICS__MEMBER_FEC_ID` | 1,715 | BIOGUIDE ➔ FEC_CAND_ID |
| `XWALK_ZCTA_COUNTY` | 46,960 | ZIP ➔ FIPS |
| `FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE` | 10,398 | CIK ➔ ticker |
| `HOUSING__FED_CFPB_HMDA_ARID2017_LEI_XREF` | 5,399 | old lender id ➔ LEI |
| `HEALTH__FQHC_SITE_PEOPLE` | 239,265 | clinician ➔ site ➔ exclusion |

### What makes a chain impressive

Not table count. **Turns** — how many times the chain changes what kind
of thing it's about. A stranger feels a turn. Nobody feels a seventh join.

```
person ➔ facility ➔ company ➔ parent ➔ place ➔ population
   1        2          3        4        5        6
```

### Chain A — six turns, no cross-key hop, ~87% survival

One doctor, all the way out to the county's death rate.

```
LAYER  TABLE                                       KEY IN    KEY OUT
  1    HEALTH__FED_CMS_NPPES                       —         NPI
  2    HEALTH__FED_CMS_OPEN_PAYMENTS               NPI       NPI
  3    HEALTH__FED_CMS_PART_D_PRESCRIBERS          NPI       NPI
  4    HEALTH__FED_CMS_FACILITY_AFFILIATION pivot  NPI       CCN
  5    HEALTH__FED_CMS_HOSPITAL_COMPARE            CCN       CCN
  6    HEALTH__FED_CMS_HCRIS                       CCN       CCN
  7    XWALK_ZCTA_COUNTY                    pivot  ZIP       FIPS
  8    DIM_COUNTY                                  FIPS      FIPS
  9    HEALTH__FED_CDC_DRUG_POISONING_COUNTY       FIPS      —
 10    JUSTICE__XC_VERA_INCARCERATION_TRENDS       FIPS      —
```

Asks: do the counties whose hospitals employ the most pharma-paid,
highest-opioid prescribers carry the highest overdose and jail rates?

- Hit: money traceable from one doctor's pocket to a county's morgue
- Miss: prescribing is national, county effect washes out — still worth showing

### Chain B — six turns, the corporate x-ray, ~85% survival

One smokestack out to the global parent and back down to the workers.

```
LAYER  TABLE                                       KEY IN    KEY OUT
  1    ENVIRONMENT__FED_EPA_FRS_FACILITIES         —         FRS_ID
  2    ENVIRONMENT__FED_EPA_FRS_FRS_PROGRAM_LINKS  FRS_ID    FRS_ID
  3    ENVIRONMENT__FED_EPA_ECHO                   FRS_ID    FRS_ID
  4    ENVIRONMENT__FED_EPA_TRI_BASIC_2023         FRS_ID    FRS_ID
  5    ENVIRONMENT__FED_EPA_GHGRP_EMISSION         FRS_ID    FRS_ID
  6    ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK pvt FRS_ID    LEI
  7    ECONOMICS__INTL_GLEIF_RELATIONSHIPS   pivot LEI       parent LEI
  8    ECONOMICS__INTL_GLEIF                       LEI       country
  9    XWALK_ZCTA_COUNTY                     pivot ZIP       FIPS
 10    ECONOMICS__FED_BLS_QCEW                     FIPS      —
 11    HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY      FIPS      —
```

Asks: which foreign-owned parents hold the most American pollution, and
what do the counties around those sites earn and die of?

Six turns. Today's ceiling.

### Chain C — the greedy one, where it breaks

Adding a stock layer forces LEI ➔ CIK, a cross-key hop.
Survival falls from 85% to roughly 8%.

Everything upstream stays true, but the finished number is a sample, not
a rate. Build it as a named-example panel — here are nine parents we could
resolve to a ticker — never as a percentage.

---

## Schema matrix

Desk review only — no live queries, no invented table or column names beyond
what's documented. "Best-fit" means the schema's known shape plausibly
supports the lens, not that it's been tested there.

**What this matrix does not cover.** These 20 subject areas hold 621 of the
676 cleaned-up tables. The other 55 sit in roughly 20 small subject areas —
PROCUREMENT, EPSTEIN, INVESTIGATIONS, HISTORY, GOVERNANCE, FOREIGN_INFLUENCE,
CIVIL_RIGHTS, JUDICIARY and others, all under 250,000 rows. Part 4 carries
questions against several of them, and they have no row in this matrix yet.

Also outside it: the join layer (60 tables), 3,600 views built over the raw
files, and 254 public-facing views. Sizes from the 2026-09-05 survey.

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

---

## Lens lookup — which schemas fit which lens

The matrix above reads schema-first. This is the same information the
other way round: pick a lens, see where it fits. Reasons are the ones
given above, not new ones.

| Lens | Schemas that fit | Why |
|---|---|---|
| **Address reuse** | FINANCE | straw-donor patterns via shared address/name |
| **Autocorrelation** | MARITIME | AIS vessel-position time series |
| **Autocorrelation** | CONSUMER_PROTECTION | complaint volume over time |
| **Autocorrelation** | TIMELINE | this schema's entire purpose is time-indexed rollups |
| **Benford's law** | HEALTH | CMS Open Payments and Part D carry real dollar amounts (`TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS`, `Tot_Drug_Cst`) |
| **Benford's law** | FINANCE | FEC individual contributions and USAspending awards |
| **Benford's law** | ECONOMICS | SEC 13F holdings, CFPB HMDA dollar fields |
| **Betweenness centrality** | HEALTH | NPI is the widest identity bridge, 59 wired tables |
| **Betweenness centrality** | FINANCE | committee-to-committee transfer graph |
| **Betweenness centrality** | JUSTICE | DOCKET key reaches 17 tables, a real case-linkage graph |
| **Bridge/cut vertex** | ENVIRONMENT | FRS_ID is the environmental identity bridge, 20 wired tables |
| **Bridge/cut vertex** | CORPORATE_REGISTRY | UK PSC ownership chains, single shell company as chokepoint |
| **Change-point detection** | POLITICS | lobbying filing vs. bill/contract timing |
| **Change-point detection** | IMMIGRATION | case volume/backlog shifts |
| **Change-point detection** | CONSUMER_SAFETY | recall/complaint volume shifts |
| **Change-point detection** | TIMELINE | this schema's entire purpose is time-indexed rollups |
| **Change-point detection** | ENERGY | EPA CAMPD daily emissions, EIA plant/utility data |
| **Chi-square uniformity** | CONSUMER_PROTECTION | complaint category distribution |
| **Chi-square uniformity** | LABOR | DOL OLMS shows exactly this failure mode |
| **Community detection** | HEALTH | NPI is the widest identity bridge, 59 wired tables |
| **Community detection** | FINANCE | committee-to-committee transfer graph |
| **Compressibility test** | SCIENCE_RESEARCH | synthetic-vs-measured data detection |
| **Cross-domain collision** | EDUCATION | this schema is a grab-bag (CFTC, Fed rates, political ads, Senate lobbying) |
| **Cui bono** | POLITICS | committee membership vs. money flow |
| **Diffusion/spread rate** | MARITIME | vessel-route pattern propagation |
| **Digit variance test** | HEALTH | CMS Open Payments and Part D carry real dollar amounts (`TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS`, `Tot_Drug_Cst`) |
| **Digit variance test** | FINANCE | FEC individual contributions and USAspending awards |
| **Digit variance test** | ECONOMICS | SEC 13F holdings, CFPB HMDA dollar fields |
| **Distance decay** | ENVIRONMENT | facility-to-community effects |
| **Duplicate near-miss** | JUSTICE | litigant/party name collisions are heavily documented |
| **Duplicate near-miss** | REFERENCE | code/lookup table redundancy |
| **Duplicate near-miss** | OPEN_DATA | ROWID collisions across monthly resources |
| **Entropy measure** | ENVIRONMENT | self-reported emissions sequences |
| **Entropy measure** | SCIENCE_RESEARCH | measurement/research data noise characteristics |
| **Fingerprint match** | FINANCE | straw-donor patterns via shared address/name |
| **Granger causality** | POLITICS | lobbying filing vs. bill/contract timing |
| **Herding/flocking** | HEALTH | shared-rep prescribing patterns fits Part D prescriber data |
| **Homophily check** | HEALTH | shared-rep prescribing patterns fits Part D prescriber data |
| **Hot-spot mapping** | ENVIRONMENT | EPA facility and emissions data is inherently geospatial |
| **Hot-spot mapping** | HOUSING | HOLC redlining polygons, FEMA registrations |
| **Levenshtein distance** | JUSTICE | litigant/party name collisions are heavily documented |
| **Log-normal** | ECONOMICS | filing interval and timing patterns |
| **Missingness pattern** | HEALTH | heavy documented suppression makes this a natural missingness testbed |
| **Missingness pattern** | IMMIGRATION | structurally broken parallel tables are a direct signal |
| **Missingness pattern** | CONSUMER_SAFETY | NHTSA complaints documented as headerless/positional |
| **Missingness pattern** | REFERENCE | reference/lookup tables are where mislabeling is most consequential |
| **Missingness pattern** | LABOR | LDA lobbying coverage gaps, 1999-2010 and 2020-2021 only |
| **Missingness pattern** | TRANSPORT | mangled-header table is a direct example |
| **Missingness pattern** | OPEN_DATA | PORTAL_CKA structure is column-partial by construction |
| **Mutual information** | ECONOMICS | contract size vs. lobbying spend, cross-schema but economics-anchored |
| **N-gram fingerprint** | POLITICS | boilerplate phrasing across filings |
| **N-gram fingerprint** | CORPORATE_REGISTRY | boilerplate clauses across filing purposes |
| **N-gram fingerprint** | CONSUMER_PROTECTION | CFPB complaints are narrative text |
| **Nash tell** | POLITICS | lobbying-then-legislation timing chains |
| **Pareto 80/20** | HEALTH | provider- and manufacturer-level payment concentration, natural shape for NPI-anchored money |
| **Pareto 80/20** | ECONOMICS | 13F filer concentration |
| **Poisson clustering** | ECONOMICS | filing interval and timing patterns |
| **Power law tail** | HEALTH | provider- and manufacturer-level payment concentration, natural shape for NPI-anchored money |
| **Power law tail** | FINANCE | donor and committee-level concentration |
| **Power law tail** | ECONOMICS | 13F filer concentration |
| **Provenance skepticism** | EDUCATION | given the mislabeling, source-checking every table is mandatory |
| **Regression discontinuity** | FINANCE | contribution limits ($200, $2,500) are documented thresholds |
| **Regression discontinuity** | HOUSING | HMDA lending-denial trend by lender size |
| **Regression discontinuity** | LABOR | wage/threshold rules |
| **Round-number clustering** | FINANCE | contribution limits ($200, $2,500) are documented thresholds |
| **Seasonality check** | MARITIME | AIS vessel-position time series |
| **Seasonality check** | CONSUMER_PROTECTION | complaint volume over time |
| **Seasonality check** | TIMELINE | built for exactly this |
| **Seasonality check** | ENERGY | EPA CAMPD daily emissions, EIA plant/utility data |
| **Signaling** | POLITICS | lobbying-then-legislation timing chains |
| **Simpson's paradox** | HOUSING | HMDA lending-denial trend by lender size |
| **Small-world network** | JUSTICE | DOCKET key reaches 17 tables, a real case-linkage graph |
| **Spatial clustering** | ENVIRONMENT | EPA facility and emissions data is inherently geospatial |
| **Spatial clustering** | HOUSING | HOLC redlining polygons, FEMA registrations |
| **Spatial clustering** | MARITIME | vessel movement/port clustering |
| **Spatial clustering** | CONSUMER_SAFETY | complaint geography if present |
| **Spatial clustering** | TRANSPORT | airport/facility geography |
| **Spatial clustering** | ENERGY | plant-level geography |
| **Stylometry** | POLITICS | boilerplate phrasing across filings |
| **Stylometry** | CONSUMER_PROTECTION | CFPB complaints are narrative text |
| **Survivorship bias** | JUSTICE | active-only exclusion/case snapshots |
| **Survivorship bias** | HOUSING | HMDA originations-only file, zero denials documented separately |
| **Survivorship bias** | CORPORATE_REGISTRY | active-companies-only visibility |
| **Time of death window** | JUSTICE | docket filing gaps |
| **Time of death window** | IMMIGRATION | case-processing gaps |
| **Trace evidence** | CORPORATE_REGISTRY | shared registered agent across "unrelated" filings |
| **Zipf's law** | FINANCE | donor and committee-level concentration |

Two entries above aren't lenses: **Cross-domain collision** is a move from
Part 1, **Provenance skepticism** is a check from Part 5. Both were named
in the matrix, so both are kept here.

A lens missing from this table had no obvious metadata fit in the desk
review. That is a gap in the review, not proof the lens can't work —
see Coverage gaps below.
---

## Coverage gaps

**12 of the 53 lenses had zero schema hits in the desk review:**
Preferential attachment, Alibi check, Staging vs real, Chain of custody,
Behavioral profiling, Timing tics, Isolation forest logic, Z-score sweep,
Regression to the mean, Confounding variable, Contact tracing logic,
R-naught style spread.

Zero hits means the desk review found no obvious metadata shape for it —
not that it's impossible. These need a live look, not another documented one.

**Thin-coverage schemas** — metadata doesn't obviously support many of the 53:
- MARITIME and CONSUMER_PROTECTION — single-table schemas, no internal cross-table lens, weak in-schema verification
- REFERENCE — mostly lookup tables, no money, no timestamps, no network structure
- SCIENCE_RESEARCH — smallest footprint, no traps recorded, no one has stress-tested it
- ENERGY, TRANSPORT, OPEN_DATA — small and load-artifact-dominated; several "findings" here are already known pipeline bugs

**The concentration pattern**: HEALTH, FINANCE, ECONOMICS, ENVIRONMENT, and
CORPORATE_REGISTRY carry the deepest lens coverage because they anchor the
warehouse's four real identity bridges — NPI, EIN, FRS_ID, CCN/UEI. Every
other schema inherits network lenses only secondhand, through those bridges.

---

---

# Part 4 — The questions

542 questions, merged from the two docket passes on 2026-09-07.
Sorted by subject. Overlap with the moves and lenses above is expected —
a question can use several tools, a tool can serve several questions.

Every field from the docket is kept. Each subject gets two tables: the
question itself, then the working notes for the ones that have them.

### What "tables" measures

Counted, not judged. How many different kinds of table the question
needs joined together.

| Label | What it means | How many |
|---|---|---|
| one table | rank it, map it, plot it over time | 283 |
| two tables | A against B, on one key | 223 |
| a chain | three or more, changing key along the way | 36 |

Measured from the `tables` column. Some one-table questions list many
tables because they stack the same shape across years — still one kind
of table, not a join.

### What "status" measures — and its limits

Status is not a measurement. It's what the last person to touch the
question wrote down afterward. Walk the chain:

```
someone runs it  ➔  writes a note in    ➔  8 regex rules sort that
                    their own words         note into 7 labels
```

`scripts/build_docket.py` does the sorting, with 8 rules at lines 76-92.
Two traps are handled on purpose: "not checked yet" contains the word
"checked" but means nothing ran, and "no pattern found" means it did
run and the answer was no.

| Label below | What happened | How many |
|---|---|---|
| **found something** | someone ran it, wrote that it confirmed | 25 |
| found a little | someone ran it, wrote "modest" or "weak" | 12 |
| started, unfinished | someone started it and did not finish | 20 |
| never run | nobody has touched it, the data is sitting there | 457 |
| needs a piece | someone tried, named exactly what is missing | 5 |
| duplicate | the same question written twice, kept for the record | 1 |
| came back empty | someone ran it, wrote that it came back empty | 22 |

**What this can't tell you.** A "found something" is one person's note,
not a verified result. Nothing here has been through the 5 checks in
Part 5. A came-back-empty line means one attempt found nothing — a
different move or lens on the same question could still land.

Status is a snapshot. `docket/docket.csv` stays the live tracker — cross
something off there, not here. The ID column below is how you find a
question again in that file.

## At a glance

| Subject | Found | A little | Started | Never run | Needs a piece | Duplicate | Empty | Total |
|---|---|---|---|---|---|---|---|---|
| Health care | 21 | 10 | 14 | 81 | 0 | 1 | 14 | 141 |
| Campaign money | 0 | 0 | 0 | 32 | 1 | 0 | 0 | 33 |
| Politics and lobbying | 1 | 0 | 0 | 60 | 1 | 0 | 0 | 62 |
| Courts and enforcement | 0 | 0 | 1 | 61 | 0 | 0 | 0 | 62 |
| Pollution and environment | 1 | 1 | 1 | 50 | 1 | 0 | 4 | 58 |
| Energy | 0 | 0 | 0 | 18 | 0 | 0 | 0 | 18 |
| Banks, markets and corporate money | 0 | 1 | 2 | 39 | 0 | 0 | 1 | 43 |
| Corporate ownership | 0 | 0 | 0 | 9 | 1 | 0 | 0 | 10 |
| Housing and lending | 0 | 0 | 1 | 21 | 0 | 0 | 2 | 24 |
| Workers and workplaces | 0 | 0 | 0 | 12 | 0 | 0 | 0 | 12 |
| Immigration | 0 | 0 | 1 | 15 | 0 | 0 | 0 | 16 |
| Contracts and procurement | 2 | 0 | 0 | 2 | 0 | 0 | 1 | 5 |
| Transport and safety | 0 | 0 | 0 | 10 | 0 | 0 | 0 | 10 |
| Consumer safety | 0 | 0 | 0 | 7 | 0 | 0 | 0 | 7 |
| Consumer protection | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 |
| Science and research | 0 | 0 | 0 | 9 | 0 | 0 | 0 | 9 |
| Education | 0 | 0 | 0 | 6 | 1 | 0 | 0 | 7 |
| History | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 3 |
| Open data portals | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 3 |
| Timeline | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 3 |
| Reference and lookup | 0 | 0 | 0 | 9 | 0 | 0 | 0 | 9 |
| Other | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 6 |
| **Total** | **25** | **12** | **20** | **457** | **5** | **1** | **22** | **542** |

By size: 283 need one table, 223 need two, 36 need a chain.

---

## Health care — 141 questions

126 live, 0 needing a piece, 14 came back empty.

| ID | The question | Why it matters | Tables | Joins on | Status |
|---|---|---|---|---|---|
| v1-E68 | **Wealthy nonprofit hospitals** — Do they give very little free care to the poor despite huge profits? | Would expose 'nonprofit' hospitals not acting like one | one table |  | **found something** |
| v1-124 | **Wealthy nonprofit hospitals** — How much do they pay their top executives? | Extends the charity-care question with executive pay | two tables |  | **found something** |
| v1-2 | **Private equity-owned nursing home chains** — Which nursing home owners get fined the most per home, and does it repeat? | Shows which owners treat fines as a cost of doing business | two tables |  | **found something** |
| v1-23 | **Medical equipment suppliers banned from Medicare** — How much money did banned suppliers still collect? | Straightforward fraud, easy to state in dollars | two tables |  | **found something** |
| v1-30 | **Nursing home owners** — Do new owners appear right after a home gets penalized, like a shell game? | Would show owners dodging penalties by 'selling' to themselves | two tables |  | **found something** |
| v1-4 | **Doctors treating addiction, and drug companies** — Do addiction doctors get paid more by drugmakers when they prescribe more? | Would be a bribe-for-prescriptions pattern | two tables |  | **found something** |
| v1-7 | **Community health clinics for the poor** — Are banned doctors working at clinics serving poor neighborhoods? | Would show bad actors targeting people with fewer options | two tables |  | **found something** |
| v1-E38 | **Doctors who've opted out of Medicare** — Are drug and device companies still paying them anyway? | Opting out doesn't mean stepping away from industry money | two tables |  | **found something** |
| v1-E39 | **Nurse practitioners paid by opioid makers** — Do the paid ones prescribe way more opioids than unpaid ones? | Would show money buying opioid prescriptions directly | two tables |  | **found something** |
| v1-E40 | **Very newly licensed doctors** — Are brand-new doctors billing Medicare for millions in expensive wound-care products? | Would be a fast-growing, hard-to-catch fraud scheme | two tables |  | **found something** |
| v1-E41 | **Doctors banned from Medicare** — Can hospitals still legally order tests and equipment through them? | Would show a loophole letting banned doctors keep working | two tables |  | **found something** |
| v1-E42 | **Doctors who are officially dead or retired in the records** — Is drug industry money still being sent to them? | Would show sloppy or fraudulent payment records | two tables |  | **found something** |
| v1-E43 | **Hospitals that get sold** — Were they already losing money before the sale? | Would show a pattern of dumping failing hospitals | two tables |  | **found something** |
| v1-E44 | **One nursing home chain (Bria) already flagged as bad** — Did its safety violations get worse right before the fines hit? | Adds a timeline to an already-known bad actor | two tables |  | **found something** |
| v1-E47 | **Rural hospitals that convert to a smaller emergency-only model** — Were they already in financial trouble before converting? | Would show the conversion program catching hospitals as they fail | two tables |  | **found something** |
| v1-E48 | **Hospitals that shut down** — Were their financial reports already bad beforehand? | Would let regulators predict closures before they happen | two tables |  | **found something** |
| v1-E57 | **Doctors who bill Medicare the most** — Are they also the ones industry pays the most? | Volume and money moving together is a red flag | two tables |  | **found something** |
| v1-E62 | **Nursing homes that claim to have fire sprinklers** — Are they still getting cited for missing sprinkler systems? | Would show a safety checkbox that lies | two tables |  | **found something** |
| v1-E73 | **Banned contractors and health care workers** — Do banned contractors turn out to also be doctors? | Would be a crossover fraud pattern | two tables |  | **found something** |
| v1-27 | **People applying to become Medicare providers** — Are any of them already banned for past fraud? | Would catch fraud before it even starts | a chain |  | **found something** |
| v1-E75 | **Nursing home chains and COVID relief funds** — Did the worst chains get big pandemic bailout money? | Would show bad actors profiting from a national emergency | a chain |  | **found something** |
| v1-20 | **Nursing homes and dialysis clinics** — Are the same people running both, and is that a conflict? | Would show a hidden ownership overlap | one table |  | found a little |
| v1-25 | **Community health centers** — Are centers whose local site shut down still collecting Medicare money as if open? | Would show phantom clinics still billing | two tables |  | found a little |
| v1-31 | **Hospitals that also own home health agencies** — Do hospital-owned home health agencies perform worse but cost more? | Would show hospitals steering patients to their own worse service | two tables |  | found a little |
| v1-E35 | **States that decriminalized drugs** — Did overdose deaths rise where jails emptied out? | Tests a real policy debate with real data | two tables |  | found a little |
| v1-E51 | **Areas newly labeled as short on doctors** — Does that label actually bring in more clinics? | Tests if a government designation does what it claims | two tables |  | found a little |
| v1-E52 | **Counties with high jail populations** — Do wages, suicide, and overdose rates all get worse there? | Tests a broad 'incarceration damages a whole county' theory | two tables |  | found a little |
| v1-E60 | **Dialysis patients in counties with bad drinking water** — Do they die at a higher rate? | Would connect water quality to dialysis patient survival | two tables |  | found a little |
| v1-E61 | **Hospitals that violate hazardous waste rules** — Do they also have worse finances? | Tests if cutting corners on waste tracks with cutting corners on money | two tables |  | found a little |
| v1-E63 | **Nursing homes that lose administrators quickly** — Does patient harm go up when leadership keeps turning over? | Tests if management chaos hurts patients | two tables |  | found a little |
| v1-E71 | **Counties and drug company payments to local doctors** — Does more payment per person mean more opioid prescribing? | Tests the money-to-opioids link at a bigger scale | two tables |  | found a little |
| v1-10 | **Medical equipment suppliers** — Are the suppliers who bill the most also getting kickback-like payments? | Would show equipment fraud loop | one table |  | started, unfinished |
| v1-11 | **Hospitals losing money, and their doctors** — Do money-losing hospitals still have doctors taking big drug company payments? | Would look hypocritical — cutting care while doctors profit | two tables |  | started, unfinished |
| v1-143 | **Companies running clinical drug trials** — Are they paying the same doctors running the trial to also promote the drug? | Would be a conflict of interest in drug testing | two tables |  | started, unfinished |
| v1-18 | **Surgeons who get paid royalties on medical devices** — Do they order more of that device at the hospital they work for? | Would show doctors profiting from their own device choices | two tables |  | started, unfinished |
| v1-21 | **Hospital workers vs. everyone else nearby** — Do hospital employees get paid less than the local average wage? | Would show hospitals underpaying staff while cutting corners | two tables |  | started, unfinished |
| v1-28 | **Nursing homes and how sick they say their patients are** — Do homes exaggerate patient sickness to get paid more? | Would be a well-known Medicare fraud pattern | two tables |  | started, unfinished |
| v1-29 | **Hospitals near heavy pollution** — Do hospitals near the most toxic sites fail financially more often? | Would show pollution driving hospital closures | two tables |  | started, unfinished |
| v1-8 | **Counties with rising jail populations** — When a county's jail population spikes, does drug overdose rise later? | Would link mass incarceration to community health decline | two tables |  | started, unfinished |
| v1-9 | **Factories that pollute the most, and their workers** — Do the biggest polluters also pay their workers the least? | Would show a double harm on the same community | two tables |  | started, unfinished |
| v1-E69 | **Community health centers and government grant money** — How much grant money reaches each patient? | Basic transparency question on where the money goes | two tables |  | started, unfinished |
| v1-E74 | **Home health agencies that change owners** — Is there a record of who the new owner is? | Same shell-game question as v1-30, for home health | two tables |  | started, unfinished |
| v1-1 | **Excluded doctors and the hospices/nursing homes that keep them** — Are doctors banned from Medicare still showing up on hospice paperwork? | Banned doctors shouldn't still be treating dying patients | a chain |  | started, unfinished |
| v1-12 | **Long-term care hospitals** — Do hospitals with financial trouble also have padded ventilator equipment billing? | Would show equipment fraud on the sickest patients | a chain |  | started, unfinished |
| v1-6 | **Dialysis clinic chains in rural areas** — Do dialysis chains that dominate a rural area have worse patient outcomes? | Would show monopoly power hurting sick people | a chain |  | started, unfinished |
| v1-24 | **Doctors in a brand-new Medicare payment program** — Nothing to compare yet, program just started | Sets a baseline to check for fraud once the program is running | one table |  | never run |
| v2-001 | **Pills shipped per county, the DEA ledger** — Which counties received the most opioid doses per resident, and in which years? | The reader sees their own county on a map of the flood. | one table | single table | never run |
| v2-002 | **Overdose deaths month by month, state by state** — Which states' overdose deaths kept climbing after the national peak? | The national curve hides states still getting worse. | one table | single table | never run |
| v2-003 | **Overdose death rate by county, year by year** — Where did the overdose wave start and where did it spread? | An animated map turns a statistic into a movement. | one table | single table | never run |
| v2-004 | **Meals priced just under $125** — Which drug companies' meal payments bunch right under the reporting line? | Pattern that looks like someone gaming a rule. | one table | single table | never run |
| v2-005 | **Who pays doctors the most** — Which companies paid the most money to doctors, and for what? | The names are household brands. | one table | single table | never run |
| v2-006 | **Nursing home star ratings by owner type** — Do for-profit and chain-owned homes score worse than nonprofit ones? | Families pick homes by stars and never see who owns them. | one table | single table | never run |
| v2-007 | **Private equity in home health** — What share of home health agencies have a private-equity or REIT owner, by state? | A quiet takeover of care for the elderly. | one table | single table | never run |
| v2-008 | **Nonprofit hospital executive pay** — Which nonprofit hospital officers earn the most, and how does pay compare to hospital revenue? | Charity status next to seven-figure salaries. | one table | single table | never run |
| v2-009 | **Hospital profit margin against charity care** — Do the most profitable hospitals give the least charity care? | The scatter answers a question people argue about. | one table | single table | never run |
| v2-010 | **Dialysis clinic death rates by owner** — Do dialysis chains have higher patient death rates than independents? | Two companies run most of the country's dialysis. | one table | single table | never run |
| v2-011 | **Medical device recalls over time** — Which device makers recall the most, and are serious recalls rising? | Implants and pumps people carry in their bodies. | one table | single table | never run |
| v2-012 | **Device injury reports by maker** — Which devices show up most in injury and death reports since 2020? | The raw report count is a shock on its own. | one table | single table | never run |
| v2-013 | **Drug side-effect reports that ended in death** — Which reported outcomes dominate, and how did the report count grow by year? | Millions of reports nobody reads. | one table | stack, same shape | never run |
| v2-014 | **Clinical trials: who sponsors, where they run** — Which sponsors run the most trials, and which countries host them? | A world map of where medicine gets tested. | one table | single table | never run |
| v2-015 | **Measles week by week, 2024** — Which states drove the 2024 measles count, week by week? | A disease that was gone coming back on a chart. | one table | single table | never run |
| v2-016 | **Leading causes of death by state, 1999 to 2017** — Which cause of death rose fastest in each state? | Small multiples, one per state, tell fifty stories. | one table | single table | never run |
| v2-017 | **Suicide rate by age group** — Which age groups' suicide rates rose most? | A quiet trend line that has been climbing for years. | one table | single table | never run |
| v2-018 | **Veteran suicide versus everyone else, by state** — Where is the veteran suicide rate furthest above the general rate? | Two lines per state, the gap is the story. | one table | single table | never run |
| v2-019 | **Abortion counts by state, month by month** — How did monthly abortion counts shift between states after 2022? | Flows between states show up as one state falling and a neighbor rising. | one table | single table | never run |
| v2-020 | **Doctors who quit Medicare** — Which specialties opt out of Medicare most, and is it growing? | A doctor shortage told through paperwork. | one table | single table | never run |
| v2-021 | **Banned from Medicare, by reason** — What gets people banned from billing Medicare, and how many come back? | Reinstatement column shows who returned. | one table | single table | never run |
| v2-022 | **Doctor shortage areas map** — Where are the worst primary-care shortage areas and how big are they? | The map of where you cannot get a doctor. | one table | stack, same shape | never run |
| v2-023 | **Opioid prescribing rate by specialty and state** — Which specialties and states prescribe opioids at the highest rate? | One column in one table, huge spread. | one table | single table | never run |
| v2-024 | **Brand versus generic drug prices** — How big is the brand-to-generic price gap for the same drug, and how did it move? | People pay it at the counter. | one table | single table | never run |
| v2-025 | **Marketplace deductibles by metal tier** — How much does a bronze deductible vary across plans and states? | Same tier, wildly different cost. | one table | single table | never run |
| v2-026 | **The Prop 65 list growing** — How many chemicals were added to California's cancer list each year? | A list that only gets longer. | one table | single table | never run |
| v2-027 | **Fast-track versus full device approvals** — How many devices cleared by 510(k) each year versus full PMA approval? | Most devices skip the hard review. | one table | stack, same shape | never run |
| v2-028 | **Same diagnosis, different bill** — For one diagnosis code, how much do hospitals' charges vary across the country? | One number a patient can understand. | one table | single table | never run |
| v2-029 | **COVID relief money to providers** — Who got the most Provider Relief Fund money and where? | Pandemic money on a map. | one table | single table | never run |
| v2-030 | **Equipment suppliers: charged versus paid** — Which medical-equipment suppliers bill Medicare far above what it pays? | The gap is the markup. | one table | single table | never run |
| v2-031 | **Nursing home fines by year** — Which homes were fined most, and are fines rising or falling? | Fine amounts next to payment-denial periods. | one table | single table | never run |
| v2-032 | **Doctor quality scores spread** — How are Medicare quality scores distributed, and who gets penalized? | A bell curve with a cliff. | one table | single table | never run |
| v2-033 | **Indian Health Service facilities map** — Where are IHS, tribal and urban Indian health facilities, and what do they offer? | Coverage gaps are visible at a glance. | one table | stack, same shape | never run |
| v2-034 | **Health insurance coverage by group over time** — Which demographic groups gained or lost coverage fastest? | Confidence ranges make the honest version. | one table | single table | never run |
| v2-035 | **Anxiety and depression by state and group** — Which groups reported the most anxiety and depression, and when did it peak? | A pandemic mood chart. | one table | single table | never run |
| v2-036 | **Life expectancy by country** — Which countries' life expectancy fell, and when? | A line that goes down is rare and gets attention. | one table | single table | never run |
| v2-037 | **Nursing home relief money by chain** — Which nursing home chains got the most COVID relief, and how were they rated? | Already-built table, one chart away. | one table | single table | never run |
| v2-038 | **Addiction prescribers and who paid them** — Which addiction-drug prescribers were paid by drug companies in 2022? | Built table, one scatter. | one table | single table | never run |
| v2-039 | **Health center staff on the ban list** — How many community-health-center clinicians are on the exclusion or opt-out lists? | Built table, already flagged. | one table | single table | never run |
| v2-040 | **Providers per zip code** — Where are doctors dense and where are they absent? | Dots on a map of nine million providers. | one table | ZIP | never run |
| v1-106 | **Counties that received huge amounts of prescription painkillers years ago** — Are those same counties still struggling with opioids today? | Connects the historic pill flood to today's ongoing crisis | two tables |  | never run |
| v1-108 | **Surgeons paid royalties on medical devices** — Were they still being paid after their device got recalled? | Would show money continuing after a product proved unsafe | two tables |  | never run |
| v1-109 | **Medical devices approved through a faster review process** — Do they have more reported deaths than devices reviewed the normal way? | Would question whether faster approval means less safe | two tables |  | never run |
| v1-110 | **Generic drugs with a sudden price spike** — Do the same doctors' prescribing costs jump right along with it? | Would show someone profiting off a price spike | two tables |  | never run |
| v1-111 | **Native American tribal health facilities** — Did their nearest full-service hospital shut down? | Would show a already-underserved population losing more care | two tables |  | never run |
| v1-113 | **Drugs and devices under mass lawsuit** — Are companies still paying doctors to promote them? | Would show payments continuing despite known harm claims | two tables |  | never run |
| v1-117 | **Nursing homes that got pandemic relief loans** — Did the same ones get hit with health and safety fines? | Would show relief money not preventing bad care | two tables |  | never run |
| v1-121 | **People named in the Panama Papers-style offshore leaks** — Are any of them U.S. doctors or political donors? | Would connect offshore secrecy to domestic money and medicine | two tables |  | never run |
| v1-133 | **Nursing home chains** — Do the most-sued chains also get the most fines? | Tests if lawsuits and regulatory fines target the same bad actors | two tables |  | never run |
| v1-134 | **People convicted of health care fraud** — Are they still allowed to work in health care because they were never formally banned? | Would show a gap between conviction and consequence | two tables |  | never run |
| v1-135 | **Hospitals hit by ransomware attacks** — Does patient care quality drop afterward? | Would show cyberattacks having real medical consequences | two tables |  | never run |
| v1-76 | **Executives at public nursing home and hospital companies** — Do they sell their company stock right before bad news like a fine hits? | Classic insider-trading-style question, applied to health care | two tables |  | never run |
| v1-98 | **Nursing homes located near unsafe dams** — Are any sitting downstream of a dam rated poor with no emergency plan? | Would be a public safety hazard nobody's tracking | two tables |  | never run |
| v1-A32 | **Banned health care companies and political donors** — Do banned companies' owners also donate to political campaigns? | Would connect fraud money to political influence | two tables |  | never run |
| v1-A33 | **Private equity nursing home owners** — Do the worst-fined chains also run a political action committee? | Would show fined companies buying political protection | two tables |  | never run |
| v2-041 | **Paid doctors and what they prescribe** — Do doctors paid by a drug maker prescribe that maker's drugs more? | The question everyone asks about pharma money. | two tables | NPI | never run |
| v2-042 | **Opioid makers and opioid prescribers** — Which opioid prescribers took opioid-maker money? | Catalog item 2 verbatim. | two tables | NPI | never run |
| v2-043 | **Deficiencies by nursing home ownership** — Do chain-owned homes get more inspection citations per home? | Catalog item 6. | two tables | CCN | never run |
| v2-044 | **Citations per resident-day** — Which homes rack up the most citations per resident-day? | Catalog item 7, which normalizes big homes against small. | two tables | CCN | never run |
| v2-045 | **Fire-safety citations versus health citations** — Do homes with many fire citations also have many health citations? | Two inspection regimes, one facility. | two tables | CCN | never run |
| v2-046 | **Hospital stars against hospital margin** — Do richer hospitals get better star ratings? | Money and quality on one scatter. | two tables | CCN | never run |
| v2-047 | **Doctors affiliated with one-star hospitals** — Which doctors are tied to the lowest-rated hospitals? | Catalog item 9 family, CCN. | two tables | CCN | never run |
| v2-048 | **Where banned providers were practicing** — Where did excluded providers practice, by specialty and state? | The ban list gets addresses. | two tables | NPI | never run |
| v2-049 | **Contract-banned people still paid by pharma** — Did drug companies keep paying doctors on the federal do-not-do-business list? | A built table meets a payments table. | two tables | NPI | never run |
| v2-050 | **Medicare billing against pharma payments** — Do the highest Medicare billers also take the most pharma money? | Catalog item 1 family. | two tables | NPI | never run |
| v2-051 | **Part B pay against specialty peers by state** — Which doctors bill far above their specialty's state average? | Catalog item 3. | two tables | NPI | never run |
| v2-052 | **Eligible to refer, enrolled or not** — How many order-and-referring doctors are not actually enrolled? | Catalog item 4. | two tables | NPI | never run |
| v2-053 | **Home health agencies per county resident** — Which counties have the most home health agencies per person? | Catalog item 5. | two tables | FIPS | never run |
| v2-054 | **Overdose deaths where doctors are scarce** — Do counties short on doctors have higher overdose death rates? | Catalog item 38. | two tables | FIPS | never run |
| v2-055 | **Shortage areas against provider count** — Are designated shortage areas really short, by provider count? | Catalog item 41. | two tables | FIPS | never run |
| v2-056 | **Pills shipped against deaths, by county** — Did counties that got more pills see more overdose deaths? | Shipment and death on one county map. | two tables | FIPS | never run |
| v2-057 | **Pharma money by specialty, rolled up** — Which specialties take the most pharma money per doctor? | Uses the pre-rolled PUBLIC table. | two tables | state + specialty code | never run |
| v2-058 | **Pharma-paid doctors with malpractice records** — Do states with more pharma money have more malpractice payments? | NPDB is de-identified, so state level only. | two tables | state code | never run |
| v2-059 | **Health-center clinics against shortage areas** — Are federally funded clinics where the shortage areas are? | Two maps, one overlay. | two tables | FIPS | never run |
| v2-060 | **Facilities in many programs** — Which hospitals converted to Rural Emergency Hospitals and what did they look like before? | Enrollment table has the conversion flag. | two tables | CCN | never run |
| v2-061 | **The opioid chain** — Can pills shipped, prescriptions written, pharma money, deaths, and treatment sites be laid on one county over twenty years? | The whole epidemic on one scrolling page. | a chain | NPI, FIPS | never run |
| v2-062 | **Nursing home chain scorecard** — For each chain: homes, stars, citations, fines, relief money, owners? | One page per chain a family could use. | a chain | CCN | never run |
| v2-063 | **One doctor, every table** — For one NPI: registry, pharma money, prescribing, billing, bans, hospital ties? | A lookup page that shows the warehouse's reach. | a chain | NPI | never run |
| v2-064 | **Device life story** — From clearance to registry to injury report to recall, for one product code? | Follow one device through four FDA systems. | a chain | product code | never run |
| v2-065 | **Private equity in home care** — Do PE-owned home health agencies score worse on care outcomes? | Owner list meets outcome list. | a chain | CCN | never run |
| v1-13 | **Nursing homes with fire safety violations** — Do owners re-register the business right after getting fire-safety fines? | Would show dodging accountability by changing names | two tables |  | duplicate |
| v1-14 | **Rural health clinics** — Are clinics claiming to be 'rural' actually sitting in cities? | Would show fraud on a rural subsidy program | one table |  | came back empty |
| v1-16 | **Diabetes prevention program providers** — Are any of them on the federal fraud exclusion list? | Would catch fraud in a diabetes program | two tables |  | came back empty |
| v1-19 | **Doctors who get quality bonuses from Medicare** — Do the ones taking industry payments still get top bonuses? | Would question whether the bonus system actually rewards good care | two tables |  | came back empty |
| v1-E34 | **Counties with hazardous waste sites** — Do they have more drug overdose deaths? | Would link toxic waste to community despair | two tables |  | came back empty |
| v1-E36 | **Counties hit by major disasters** — Does overdose death rise after a disaster? | Would show disaster trauma driving addiction | two tables |  | came back empty |
| v1-E37 | **Doctors and the drug industry money they get** — Does a pay raise from a drug company lead to more prescriptions? | The classic 'paid to prescribe' question | two tables |  | came back empty |
| v1-E45 | **Nursing homes after storms** — Do safety violations spike after a storm hits the area? | Would show storms exposing nursing home neglect | two tables |  | came back empty |
| v1-E46 | **Owners who run three types of care facility at once** — Are these 'triple owners' actually better or worse than others? | Tests whether bigger ownership means better or worse care | two tables |  | came back empty |
| v1-E50 | **Areas hit by disasters** — Do new health care businesses pop up right after, chasing relief money? | Would show opportunists rushing in after disasters | two tables |  | came back empty |
| v1-E56 | **Doctors getting Medicare bonuses** — Do bonus and non-bonus doctors get similar industry money? | A stricter version of v1-19 | two tables |  | came back empty |
| v1-E58 | **U.S. states** — Do states with more malpractice payouts also get more industry money? | Tests a state-level backdrop theory | two tables |  | came back empty |
| v1-E59 | **The highest-paid hospitals** — Do they have the worst quality ratings? | Would show money not buying better care | two tables |  | came back empty |
| v1-E67 | **Counties with high jail populations** — Do they also have fewer doctors available? | Tests if incarceration and doctor shortages travel together | two tables |  | came back empty |
| v1-E70 | **Nursing homes with veteran contracts** — Are the worst-rated homes still getting VA contracts? | Would show the VA sending veterans to bad facilities | two tables |  | came back empty |

**Working notes — 141 of these 141 carry them**

| ID | Size | Years | Effort | Watch out | Needs | Notes, matches, results |
|---|---|---|---|---|---|---|
| v1-E68 | 6,103 | FY2023 | Quick — re-run and check the number | 37 hospitals over $50 million profit, under 1% charity care |  | v2-Hospital profit margin against charity care · reports/tier1_deep_dive_2026-09-05/E68_nonprofit_charity_care |
| v1-124 | 526,374 | tax years 2016-2025 | thin at both ends | Done — 526,374 person rows, 3,918 hospital EINs, 23,810 returns |  | v2-Nonprofit hospital executive pay · 9,153 of 32,963 returns are not hosted by the IRS any more (2016-2018 object ids, plus 1,306 from 2022); one executive repeats on every affiliate return, group by person and year before ranking; 61 group-return rows carry a whole system on one line |
| v1-2 | 449,372 | deficiencies 2017-26, penalties 2023-06 on | Quick — re-run and check the number | one chain gets fined 5x more per home than a comparable one |  | v2-Deficiencies by nursing home ownership/v2-Nursing home chain scorecard |
| v1-23 | 524,417 | ingested 2026-07 | Quick — re-run and check the number | $1.4 billion, one company alone took $860 million |  | v2-Equipment suppliers: charged versus paid · reports/tier1_deep_dive_2026-09-05/23_banned_dme_suppliers |
| v1-30 | 30,605 | penalties 2023-06 on | Quick — re-run and check the number | 39 homes did exactly this |  | v2-Nursing home chain scorecard · reports/tier1_deep_dive_2026-09-05/30_penalty_then_new_owner |
| v1-4 | 39,177,643 | one year | Small — mart built 2026-09-07, query it | OTP table was the wrong leg, it lists orgs; Part D to Open Payments on NPI |  | v2-Paid doctors and what they prescribe · HEALTH__ADDICTION_PRESCRIBERS_PAID: 26,193 of 44,335 addiction prescribers took drugmaker money in 2022, 59% |
| v1-7 | 159,994 | n/a | Small — mart built 2026-09-07, query it | address bridge, 58% of sites reached; every address but one predates the exclusion |  | v2-Health center staff on the ban list · HEALTH__FQHC_SITE_PEOPLE: 88 banned people at 112 clinics, 173,813 people bridged by address |
| v1-E38 | 15,442,256 | PY2023 | Quick — re-run and check the number | $70.8 million paid to opted-out doctors |  | v2-Doctors who quit Medicare · reports/tier1_deep_dive_2026-09-05/E38_optout_doctors_paid |
| v1-E39 | 16,801,930 | two years | Quick — re-run and check the number | paid ones prescribe opioids at a much higher rate |  | v2-Opioid makers and opioid prescribers · reports/tier1_deep_dive_2026-09-05/E39_paid_opioid_prescribers |
| v1-E40 | 19,388,356 | DY2024 | Quick — re-run and check the number | $1.35 billion in billing, concentrated fast |  | reports/tier1_deep_dive_2026-09-05/E40_new_doctors_skin_substitutes |
| v1-E41 | 2,102,101 | snapshot | Quick — re-run and check the number | 7 doctors doing exactly this |  | v2-Where banned providers were practicing · reports/tier1_deep_dive_2026-09-05/E41_banned_doctors_ordering |
| v1-E42 | 24,991,730 | PY2024 | Quick — re-run and check the number | $4.2 million, mostly to just 10 people |  | v2-Doctors who quit Medicare · reports/tier1_deep_dive_2026-09-05/E42_pharma_money_dead_npis |
| v1-E43 | 50,532 | FY2022-24 | Quick — re-run and check the number | 60% of sold hospitals were losing money first | HCRIS now 13 years; 1,322 hospitals changed ownership type | v2-Facilities in many programs · reports/tier1_deep_dive_2026-09-05/E43_losses_before_sale |
| v1-E44 | 434,659 | 2023-2025 | Quick — re-run and check the number | Confirmed with a clear timeline |  | v2-Nursing home chain scorecard · reports/tier1_deep_dive_2026-09-05/E44_violations_before_fines |
| v1-E47 | 50,532 | last full year | Quick — re-run and check the number | 84% were losing money first | HCRIS now 13 years, 2011-2023 | v2-Facilities in many programs · reports/tier1_deep_dive_2026-09-05/E47_conversion_finances |
| v1-E48 | 50,532 | 2024-26 | Quick — re-run and check the number | 68% were already losing money | HCRIS now 13 years; 65 to 108 hospitals stop filing a year | v2-Hospital profit margin against charity care · reports/tier1_deep_dive_2026-09-05/E48_closures_predicted |
| v1-E57 | 16,681,786 | DY2024 | Quick — re-run and check the number | a real, meaningful overlap |  | v2-Medicare billing against pharma payments · reports/tier1_deep_dive_2026-09-05/E57_volume_and_money |
| v1-E62 | 433,192 | snapshot | Quick — re-run and check the number | Confirmed as a real data quality problem |  | v2-Fire-safety citations versus health citations · reports/tier1_deep_dive_2026-09-05/E62_sprinkler_flag_lies |
| v1-E73 | 9,775,011 | snapshot | Small — mart built 2026-09-07, query it | HHS, OFAC, OPM rows filtered first or the answer is "banned doctors are doctors" |  | HEALTH__SAM_EXCLUDED_PROVIDERS: 16,144 non-HHS exclusions, 814 matched to a doctor, 660 ambiguous |
| v1-27 | 2,358,060 | 2026-07 snapshot | Quick — re-run and check the number | 9 found, small but real |  | v2-Eligible to refer, enrolled or not · reports/tier1_deep_dive_2026-09-05/27_pending_applicants_banned |
| v1-E75 | 419,846 | PRF payments 2020-2022, file dated 2025-03-28 | Medium — a verified opco-name rule would lift the chain hit rate | Name+city+state floor: 2,122 of 14,713 homes hit (14%), chains 9.7% vs independents 25%. Hospital-unit money ($1.21B) and one-word hits excluded. Zero means no name hit, not no money |  | v2-Nursing home relief money by chain · reports/dead_ends_build_B_prf_2026-09-07.md |
| v1-20 | 2,260,193 | snapshot | Medium — partial run, needs finishing | Small group found, no clear story yet |  |  |
| v1-25 | 221,023 | since 2020 | Medium — partial run, needs finishing | Small number found, worth another look |  | v2-Health center staff on the ban list |
| v1-31 | 33,075 | snapshot | Quick — re-run and check the number | mixed result |  | v2-Private equity in home care · reports/tier1_deep_dive_2026-09-05/31_hospital_owned_hha |
| v1-E35 | 260,507 | 2019-2024 | Medium — partial run, needs finishing | One state (Washington) shows a strong pattern; nationally it's not clear |  |  |
| v1-E51 | 98,196 | DiD | Medium — partial run, needs finishing | Unclear, could go either way |  |  |
| v1-E52 | 3,879,944 | one year wage | Medium — partial run, needs finishing | mostly just wages showed a real effect |  | v2-Jail rate against injury deaths |
| v1-E60 | 27,889,193 | yearly file landed | Medium — partial run, needs finishing | Real but modest signal, worth a deeper look |  |  |
| v1-E61 | 714,217 | one year | Medium — partial run, needs finishing | Modest signal, needs more care in how it's measured |  |  |
| v1-E63 | 433,192 | 2024-25 | Medium — partial run, needs finishing | Modest signal, promising |  |  |
| v1-E71 | 16,801,930 | one year | Medium — partial run, needs finishing | Weak signal, not conclusive |  | v2-Pills shipped against deaths, by county |
| v1-10 | 381,228 | DY2024 | Medium — partial run, needs finishing | Partially checked, some red flags in the data |  | v2-Equipment suppliers: charged versus paid |
| v1-11 | 16,967,082 | 2023 | Medium — partial run, needs finishing | Partially checked, real data found | HCRIS now 13 years, 2011-2023, 80,077 rows | v2-Hospital stars against hospital margin |
| v1-143 | 601,694 | n/a | Medium — flatten and name-match are SQL | full CT.gov landed 2026-09-07 into _FULL; old 500-row table and its mart untouched; NPI blank, bridge is investigator name + sponsor name | flatten LOCATIONS json to investigator-site rows; name-match to Open Payments |  |
| v1-18 | 15,501,229 | 2024 one year | Medium — partial run, needs finishing | Partially checked, real dollars found ($847M) |  |  |
| v1-21 | 3,625,540 | 2022 vs 2023 | Medium — partial run, needs finishing | Partially checked, real signal |  |  |
| v1-28 | 31,836,407 | one quarter | Medium — partial run, needs finishing | Partially checked, one time period only so far |  |  |
| v1-29 | 115,522 | 2015-2024 | Medium — partial run, needs finishing | Partially checked, one number looks suspicious and needs a second look |  |  |
| v1-8 | 347,425 | 2010-2024 | Medium — partial run, needs finishing | Partially checked, real pattern not confirmed yet |  | v2-Overdose and jail, worst-tenth counties |
| v1-9 | 3,887,442 | cross-section | Medium — partial run, needs finishing | Partially checked, weak so far |  |  |
| v1-E69 | 19,905,591 | 6 of 24 months | Medium — partial run, needs finishing | Only a few months of money data currently available |  | v2-Health center staff on the ban list |
| v1-E74 | 125,088 | snapshot 2026-07-17; owner arrival dates 1800-2026, 641 pre-1990 rows are sentinels | Medium — first probe query needed | Owners file landed 2026-09-07 (101,188 rows, 11,494 agencies, 97.7% carry a CCN). Key owners on ASSOCIATE_ID_OWNER not name; flags null on individuals; REIT flag is a constant N; 641 owner dates pre-1990 are sentinels. One snapshot, so "changed owner" reads off ASSOCIATION_DATE_OWNER (4,120 agencies since 2024), not a quarter-over-quarter diff. |  | reports/dead_ends_build_C_hha_owners_2026-09-07.md |
| v1-1 | 2,364,431 | affiliation snapshot 2026-07 | Medium — partial run, needs finishing | Found 4 so far, confirmed |  |  |
| v1-12 | 17,689,980 | 2023 | Medium — partial run, needs finishing | Partially checked, small group so far |  |  |
| v1-6 | 30,613,170 | one vintage | Medium — partial run, needs finishing | Partially checked, needs a full run |  |  |
| v1-24 | 6,637 | 2027 start | Medium — partial run, needs finishing | nothing to find yet |  |  |
| v2-001 |  |  |  |  |  | 178M rows. Buyer address gives county. Morphine-equivalent column already there. · v1-106 · visual: map |
| v2-002 |  |  |  |  |  | Has a reporting-completeness column. Show it as a shaded band. · visual: timeline |
| v2-003 |  |  |  |  |  | Rates are given as ranges, not points. Plot the midpoint and say so. · visual: map |
| v2-004 |  |  |  |  |  | Already-built table. A histogram with a spike at $124 is the whole chart. · visual: other |
| v2-005 |  |  |  |  |  | 15M rows. Also a by-manufacturer rollup in PUBLIC. · visual: ranking |
| v2-006 |  |  |  |  |  | Ownership and chain columns in the same row as stars and fines. · visual: other |
| v2-007 |  |  |  |  |  | Entity-type column names PE, LLC, nonprofit, REIT outright. · visual: map |
| v2-008 |  |  |  |  |  | Built from 990 filings. Hours-worked column lets you compute pay per hour. · v1-124 · visual: ranking |
| v2-009 |  |  |  |  |  | One row per hospital per fiscal year, so it can animate. · v1-E68/v1-E48 · visual: other |
| v2-010 |  |  |  |  |  | Death rate, readmission, infection, transplant waitlist all in one row. · visual: ranking |
| v2-011 |  |  |  |  |  | Recall class column gives severity. · visual: timeline |
| v2-012 |  |  |  |  |  | 2020 onward only. · visual: ranking |
| v2-013 |  |  |  |  |  | Three tables share a report ID but that key is not in the join catalog. Treat each as single until proven. · visual: timeline |
| v2-014 |  |  |  |  |  | 600K trials. Phase and status columns give a funnel too. · visual: map |
| v2-015 |  |  |  |  |  | 1.9M rows across all reportable diseases. Pick one disease per chart. · visual: timeline |
| v2-016 |  |  |  |  |  | Has national total rows. Filter them out or they dominate. · visual: timeline |
| v2-017 |  |  |  |  |  | visual: timeline |
| v2-018 |  |  |  |  |  | Comparison column already built in. · visual: map |
| v2-019 |  |  |  |  |  | Low-high range columns. Show the band. · visual: timeline |
| v2-020 |  |  |  |  |  | Effective-date columns give the timeline. · v1-E38/v1-E42 · visual: ranking |
| v2-021 |  |  |  |  |  | visual: timeline |
| v2-022 |  |  |  |  |  | Two tables overlap. Pick the full one. · visual: map |
| v2-023 |  |  |  |  |  | Opioid and antipsychotic rate columns already computed. · visual: ranking |
| v2-024 |  |  |  |  |  | Effective-date rows give a price history per drug. · visual: timeline |
| v2-025 |  |  |  |  |  | visual: other |
| v2-026 |  |  |  |  |  | visual: timeline |
| v2-027 |  |  |  |  |  | Two tables, no join needed, same axis. · v1-109 · visual: timeline |
| v2-028 |  |  |  |  |  | DRG column. Pick a knee replacement or a heart attack. · visual: other |
| v2-029 |  |  |  |  |  | visual: map |
| v2-030 |  |  |  |  |  | v1-23/v1-10 · visual: ranking |
| v2-031 |  |  |  |  |  | visual: timeline |
| v2-032 |  |  |  |  |  | visual: other |
| v2-033 |  |  |  |  |  | Several tables shown side by side, no join. If a join is wanted, it is not in the catalog. · visual: map |
| v2-034 |  |  |  |  |  | visual: timeline |
| v2-035 |  |  |  |  |  | visual: timeline |
| v2-036 |  |  |  |  |  | visual: timeline |
| v2-037 |  |  |  |  |  | 617 rows. Built table. · v1-117/v1-E75 · visual: ranking |
| v2-038 |  |  |  |  |  | Built table. · visual: other |
| v2-039 |  |  |  |  |  | Built table. · v1-7/v1-25/v1-E69 · visual: ranking |
| v2-040 |  |  |  |  |  | ZIP is a code key; catalog says code keys never bridge. Practice-address zip to DIM_ZIP_POINT is a plain lookup. · visual: map |
| v1-106 | 180,068,296 | 2006-14 vs 2024 | Medium — first probe query needed | sits in the single biggest untouched dataset |  | v2-Pills shipped per county, the DEA ledger |
| v1-108 | 15,600,368 | around recall date | Medium — first probe query needed | no query run yet, treat any first number as unverified |  |  |
| v1-109 | 2,919,247 | 2020+ | Medium — first probe query needed | no query run yet, treat any first number as unverified |  | v2-Fast-track versus full device approvals |
| v1-110 | 27,525,898 | effective dates | Medium — first probe query needed | no query run yet, treat any first number as unverified |  |  |
| v1-111 | 54,168 | 2015+ | Medium — first probe query needed | no query run yet, treat any first number as unverified |  |  |
| v1-113 | 15,385,209 | after MDL date | Medium — first probe query needed | no query run yet, treat any first number as unverified |  |  |
| v1-117 | 999,129 | 2020-21 vs fines | Medium — first probe query needed | no query run yet, treat any first number as unverified |  | v2-Nursing home relief money by chain |
| v1-121 | 100,328,474 | untimed | Medium — first probe query needed | no query run yet, treat any first number as unverified |  |  |
| v1-133 | 10,888,289 | by year | Medium — first probe query needed | no query run yet, treat any first number as unverified |  | v2-Nursing home chain scorecard |
| v1-134 | 6,383,655 | judgment to exclusion | Medium — first probe query needed | no query run yet, treat any first number as unverified |  |  |
| v1-135 | 50,806 | attack date on | Medium — first probe query needed | no query run yet, treat any first number as unverified |  |  |
| v1-76 | 2,697,968 | 2025Q1+, check quarters | Medium — first probe query needed | no query run yet, treat any first number as unverified |  |  |
| v1-98 | 107,466 | last inspection | Medium — first probe query needed | no query run yet, treat any first number as unverified |  |  |
| v1-A32 | 84,424,187 | untimed | Medium — first probe query needed | no query run yet, treat any first number as unverified |  |  |
| v1-A33 | 74,744 | untimed | Medium — first probe query needed | no query run yet, treat any first number as unverified |  |  |
| v2-041 |  |  |  |  |  | Catalog item 1 and 2. Drug-level Part D table is 25M rows. · v1-4/v1-E37 · visual: other |
| v2-042 |  |  |  |  |  | v1-E39 · visual: other |
| v2-043 |  |  |  |  |  | v1-2 · visual: ranking |
| v2-044 |  |  |  |  |  | MDS table is 31M rows. · visual: ranking |
| v2-045 |  |  |  |  |  | v1-E62 · visual: other |
| v2-046 |  |  |  |  |  | v1-11/v1-E59 · visual: other |
| v2-047 |  |  |  |  |  | visual: other |
| v2-048 |  |  |  |  |  | v1-E41 · visual: map |
| v2-049 |  |  |  |  |  | visual: ranking |
| v2-050 |  |  |  |  |  | v1-E57 · visual: other |
| v2-051 |  |  |  |  |  | visual: ranking |
| v2-052 |  |  |  |  |  | v1-27 · visual: other |
| v2-053 |  |  |  |  |  | visual: map |
| v2-054 |  |  |  |  |  | v1-E67 · visual: map |
| v2-055 |  |  |  |  |  | visual: map |
| v2-056 |  |  |  |  |  | FIPS family has 15 tables; confirm ARCOS is one before building. · v1-E71 · visual: map |
| v2-057 |  |  |  |  |  | Both are rollups keyed by state and specialty; not a catalog key. · visual: ranking |
| v2-058 |  |  |  |  |  | State is not a catalog key. Lookup only. · visual: other |
| v2-059 |  |  |  |  |  | visual: map |
| v2-060 |  |  |  |  |  | v1-E43/v1-E47 · visual: timeline |
| v2-061 |  |  |  |  |  | Scrollytelling. Every join is a catalog key. · v1-107 · visual: other |
| v2-062 |  |  |  |  |  | v1-2/v1-30/v1-133/v1-E44 · visual: other |
| v2-063 |  |  |  |  |  | NPI is the steel key: 34 tables, 364 edges. · visual: other |
| v2-064 |  |  |  |  |  | Product code is not a catalog key. Needs proving. · visual: flow |
| v2-065 |  |  |  |  |  | v1-31/v1-74 · visual: other |
| v1-13 | 214,455 | 2016-2026 | Medium — partial run, needs finishing | see v1-30 |  |  |
| v1-14 | 5,530 | snapshot | Skip — already ruled out | Dead end as asked, simpler version might work |  |  |
| v1-16 | 84,784 | snapshot | Medium — partial run, needs finishing | none found |  |  |
| v1-19 | 1,920,800 | 2024 | Medium — partial run, needs finishing | Checked, no clear pattern |  |  |
| v1-E34 | 761,501 | 2003-2015 | Skip — already ruled out | no real relationship found |  |  |
| v1-E36 | 26,382,920 | 2019-2024 | Skip — already ruled out | no pattern found |  |  |
| v1-E37 | 31,502,716 | PY2023-24 | Medium — partial run, needs finishing | the money is mostly stock deals and consulting fees |  | v2-Paid doctors and what they prescribe |
| v1-E45 | 2,199,209 | event windows | Medium — partial run, needs finishing | storms barely move the number |  |  |
| v1-E46 | 2,274,906 | snapshot | Medium — partial run, needs finishing | Turned out to be about nonprofit vs. for-profit, not size |  |  |
| v1-E50 | 26,262,428 | DiD | Skip — already ruled out | the boom already existed before the disaster |  |  |
| v1-E56 | 15,888,964 | PY2024 | Medium — partial run, needs finishing | No difference found |  |  |
| v1-E58 | 17,115,888 | 2022-24 | Skip — already ruled out | the comparison method itself was flawed |  |  |
| v1-E59 | 8,476 | one year | Medium — partial run, needs finishing | No relationship found |  | v2-Hospital stars against hospital margin |
| v1-E67 | 9,735,190 | snapshot | Skip — already ruled out | no relationship once population size is controlled for |  | v2-Overdose deaths where doctors are scarce |
| v1-E70 | 93,168,137 | snapshot | Medium — partial run, needs finishing | No pattern found |  |  |

## Campaign money — 33 questions

32 live, 1 needing a piece, 0 came back empty.

| ID | The question | Why it matters | Tables | Joins on | Status |
|---|---|---|---|---|---|
| v2-215 | **Who owns the big companies** — Which managers hold the most of one company, and how concentrated is ownership? | Ownership of a household name, drawn. | one table | single table | never run |
| v2-216 | **Insiders selling before the drop** — Which companies' insiders sold the most, and when? | A timeline per company. | one table | stack, same shape | never run |
| v2-217 | **The audit partner who signs everything** — Which audit partners and firms sign the most public-company audits? | Names behind the books. | one table | single table | never run |
| v2-218 | **Bank deserts** — Which counties lost the most bank branches, and where are there none? | Branch counts per county per year. | one table | FIPS | never run |
| v2-219 | **Deposits per branch, over time** — Which banks hold the most deposits in the fewest branches? | Consolidation, drawn. | one table | single table | never run |
| v2-220 | **Credit unions ranked** — Which credit unions are biggest, and which grew fastest? | Quarterly snapshots. | one table | stack, same shape | never run |
| v2-221 | **Income by zip code** — Where are the richest and poorest zips by reported income? | IRS returns, mapped. | one table | ZIP | never run |
| v2-222 | **Small-donor share by cycle** — Did small donors become a bigger share of campaign money? | One line, twenty cycles. | one table | stack, same shape | never run |
| v2-223 | **Donors by occupation and employer** — Which employers' staff give the most, and to whom? | Employer column is gold. | one table | single table | never run |
| v2-224 | **Outside spending, support versus oppose** — Did independent spending turn more negative over cycles? | Support and oppose as two bars. | one table | single table | never run |
| v2-225 | **PAC to PAC transfers** — Which committees move the most money to other committees? | A network of transfers. | one table | single table | never run |
| v2-226 | **Foreign banks reporting to the IRS** — Which countries have the most FATCA-registered institutions? | A tax-haven map. | one table | stack, same shape | never run |
| v2-227 | **Hedge funds' weekly bets** — How did hedge fund long and short positions in stock index futures move weekly? | Positioning as a wave. | one table | stack, same shape | never run |
| v2-228 | **Who countries owe** — Which creditors hold each country's debt, and where are the repayment cliffs? | A debt map with cliffs flagged. | one table | country + year | never run |
| v2-229 | **Two Senate trade sources disagree** — How many senators' trades appear in one source but not the other? | Source disagreement as the chart. | one table | stack, same shape | never run |
| v2-230 | **Filings per industry per quarter** — Which industries file the most financial statements each quarter? | Nine quarterly tables, one line. | one table | stack, same shape | never run |
| v2-231 | **Who advises money market funds** — Which advisors manage the most money market funds? | Concentration in one chart. | one table | single table | never run |
| v2-232 | **Stock exchanges of the world** — How many trading venues per country, and which operators run them? | Registry as a map. | one table | single table | never run |
| v1-79 | **Banks that failed** — Did they quietly switch auditors right before collapsing? | Would show a warning sign nobody flagged in time | two tables |  | never run |
| v1-85 | **Drug and device company political money** — Does it flow from their corporate PAC into top leaders' campaign funds? | Would trace industry money's path to power | two tables |  | never run |
| v1-87 | **Registered foreign lobbyists** — Do they also personally donate to U.S. political campaigns? | Foreign influence question | two tables |  | never run |
| v1-91 | **Members of Congress** — Do they buy a stock, then introduce a bill that helps it? | A more specific insider-trading pattern | two tables |  | never run |
| v2-233 | **Auditor against filer size** — Do the Big Four audit all the big filers, and who audits the rest? | Catalog item 22. | two tables | CIK | never run |
| v2-234 | **Insider filings against company size** — Which companies file the most insider trades per dollar of size? | Catalog item 23. | two tables | CIK | never run |
| v2-235 | **13F holdings per manager** — Which managers hold the most positions, and how did that change? | Catalog item 24. | two tables | CIK | never run |
| v2-236 | **Injuries at public companies** — Which public companies report the most workplace injuries? | Catalog item 25, thin. | two tables | CIK~EIN | never run |
| v2-237 | **Mortgage lenders by global ID** — Which lenders in the mortgage file are subsidiaries of which parents? | Catalog item 55. | two tables | LEI | never run |
| v2-238 | **Branches against FHLB membership** — Do FHLB members hold more branches per county? | Catalog item 57, no edges yet. | two tables | FDIC_CERT | never run |
| v2-239 | **13F positions by issuer** — Which issuers are held by the most managers? | Catalog item 56, no edges yet. | two tables | CUSIP bridge | never run |
| v2-240 | **Senators and insiders trading the same stock** — Did a senator trade a stock the same week its insiders did? | Two disclosure regimes on one timeline. | two tables | ticker | never run |
| v1-81 | **Company pension plans that collapse onto the government** — Did executives sell their own stock right before the collapse? | Would show executives cashing out while workers' pensions failed | a chain |  | never run |
| v2-241 | **One public company, every table** — For one CIK: filings, insiders, holders, auditor, injuries, EPA sites? | The company card. | a chain | CIK, CIK~EIN | never run |
| v1-92 | **Congressional offices** — Does office spending go to vendors who are also campaign donors? | Would show taxpayer money looping back to donors | two tables |  | needs a piece |

**Working notes — 33 of these 33 carry them**

| ID | Size | Years | Effort | Watch out | Needs | Notes, matches, results |
|---|---|---|---|---|---|---|
| v2-215 |  |  |  |  |  | 3.8M holdings. · visual: ranking |
| v2-216 |  |  |  |  |  | Same filing ID; not a catalog key. · visual: timeline |
| v2-217 |  |  |  |  |  | visual: ranking |
| v2-218 |  |  |  |  |  | Branch address to county lookup. · v1-127 · visual: map |
| v2-219 |  |  |  |  |  | visual: timeline |
| v2-220 |  |  |  |  |  | Several tables shown side by side, no join. If a join is wanted, it is not in the catalog. · visual: ranking |
| v2-221 |  |  |  |  |  | Zip lookup. · visual: map |
| v2-222 |  |  |  |  |  | Use the PUBLIC rollup first; 284M rows raw. · visual: timeline |
| v2-223 |  |  |  |  |  | visual: ranking |
| v2-224 |  |  |  |  |  | visual: timeline |
| v2-225 |  |  |  |  |  | visual: flow |
| v2-226 |  |  |  |  |  | Two copies of the same list. · visual: map |
| v2-227 |  |  |  |  |  | Two COT tables, one misfiled under EDUCATION. · visual: timeline |
| v2-228 |  |  |  |  |  | Country lookup. Not a catalog key; lookup or unproven. · visual: timeline |
| v2-229 |  |  |  |  |  | Combined table has the match-confidence column. · visual: other |
| v2-230 |  |  |  |  |  | Union, no join. · visual: timeline |
| v2-231 |  |  |  |  |  | visual: ranking |
| v2-232 |  |  |  |  |  | visual: map |
| v1-79 | 2,981,945 | 2017+ | Medium — first probe query needed | no query run yet, treat any first number as unverified |  |  |
| v1-85 | 15,453,697 | by cycle | Medium — first probe query needed | no query run yet, treat any first number as unverified |  | v2-Follow the money · reports/politics_probe_2026-09-05/85_maker_pacs_to_leadership_pacs |
| v1-87 | 84,394,012 | registration window | Medium — first probe query needed | no query run yet, treat any first number as unverified | FEC indiv now 14 cycles, 2000-2026, 283.8M rows | reports/politics_probe_2026-09-05/87_fara_agents_donating |
| v1-91 | 412,557 | 90-day window | Medium — first probe query needed | no query run yet, treat any first number as unverified | nothing on data. bills 113-119, senate trades to 2026, and house trade lines all landed. house PTR is 27,286 rows over 3,109 filings as of 2026-09-07 | v2-Senators trading in what they oversee · reports/politics_probe_2026-09-05/91_trade_then_bill |
| v2-233 |  |  |  |  |  | visual: other |
| v2-234 |  |  |  |  |  | visual: other |
| v2-235 |  |  |  |  |  | visual: ranking |
| v2-236 |  |  |  |  |  | CIK~EIN matches 2 to 16 percent. Sample, never a rate. · visual: ranking |
| v2-237 |  |  |  |  |  | Historic HMDA uses old lender ID; use the crosswalk. · visual: other |
| v2-238 |  |  |  |  |  | Key in keyset, zero edges. · visual: other |
| v2-239 |  |  |  |  |  | FTD_CUSIP_BRIDGE named in catalog but not in the inventory. Not a catalog key; lookup or unproven. · visual: ranking |
| v2-240 |  |  |  |  |  | Ticker not a catalog key. · visual: timeline |
| v1-81 | 6,983,857 | termination year | Medium — first probe query needed | no query run yet, treat any first number as unverified |  |  |
| v2-241 |  |  |  |  |  | CIK: 19 tables, 128 edges. Cross-key legs are thin. · visual: other |
| v1-92 | 89,086,588 | by quarter | Medium — first probe query needed | no query run yet, treat any first number as unverified | FEC indiv is 2023-26 only | reports/politics_probe_2026-09-05/92_office_money_to_donors |

## Politics and lobbying — 62 questions

61 live, 1 needing a piece, 0 came back empty.

| ID | The question | Why it matters | Tables | Joins on | Status |
|---|---|---|---|---|---|
| v1-84 | **Members of Congress who oversee Medicare** — Who's spending money for or against them in elections? | Would show who wants influence over Medicare oversight | a chain |  | **found something** |
| v2-066 | **Congress drifting apart** — How far apart have the two parties' ideology scores moved since 1789? | The polarization chart, from the original source. | one table | single table | never run |
| v2-067 | **Three branches, one axis** — How far apart do the House, Senate and Supreme Court sit each year? | One line per branch on one axis. | one table | stack, same shape | never run |
| v2-068 | **Who actually passes bills** — Which members turn the most sponsored bills into law? | Rank by enactment rate, not by noise. | one table | single table | never run |
| v2-069 | **Missed votes and party loyalty** — Who misses the most votes, and who breaks with their party most? | Two numbers per member. | one table | single table | never run |
| v2-070 | **Cosponsor web** — Which members cosponsor together, across the aisle? | A network graph of Congress. | one table | single table | never run |
| v2-071 | **Senators' stock trades** — Which senators trade most, and what did they buy before big news? | Trades on a timeline next to headlines. | one table | stack, same shape | never run |
| v2-072 | **Margins of victory over time** — Are federal elections getting closer or more lopsided? | Every winner, every margin. | one table | single table | never run |
| v2-073 | **Closest House races** — Which House seats were decided by the fewest votes? | Vote share by candidate, MIT-cleaned. | one table | stack, same shape | never run |
| v2-074 | **Where Texas lobbyists buy dinner** — Which restaurants and which officials show up most on lobbyist meal reports? | A list of restaurants is a very human chart. | one table | single table | never run |
| v2-075 | **Texas lobby gifts, travel, events** — What do lobbyists give Texas officials, and who gets most? | Gifts, hotels, flights, receptions in one view. | one table | stack, same shape | never run |
| v2-076 | **Texas lobby spending by category over time** — How did total lobby spending split across meals, gifts, travel, media by year? | Cover sheets carry the totals. | one table | single table | never run |
| v2-077 | **What Texas lobbyists work on** — Which subjects draw the most lobbying activity in Texas? | 210K subject rows, one bar chart. | one table | single table | never run |
| v2-078 | **California's biggest lobby spenders** — Which employers pay the most for lobbying per session? | Quarter-by-quarter totals per employer. | one table | stack, same shape | never run |
| v2-079 | **California lobbyists who also donate** — Which lobbyists give the most campaign money? | Lobby and donate in one row. | one table | single table | never run |
| v2-080 | **People on many dark-money boards** — Which names sit on the most 527 organization filings? | Same names across dozens of groups. | one table | single table | never run |
| v2-081 | **Dark-money groups related to each other** — Which 527 groups declare each other as related? | A network of shells. | one table | stack, same shape | never run |
| v2-082 | **Canada's 12.6 million donations** — How did giving to each Canadian party move over time? | Bigger than most US state files. | one table | single table | never run |
| v2-083 | **Freedom scores rising and falling** — Which countries lost the most freedom points in the last decade? | A world map that changes color. | one table | single table | never run |
| v2-084 | **Military spending by country** — Who spends most, and who grew fastest? | Ranking that moves over time. | one table | single table | never run |
| v2-085 | **Who votes with whom at the UN** — Which countries vote with the US most and least, and how has that shifted? | A country-pair heatmap. | one table | single table | never run |
| v2-086 | **Corruption perception by country** — Which countries' corruption scores improved or fell most? | Simple, global, recognizable. | one table | single table | never run |
| v2-087 | **Radio licenses by service type** — Where are FCC licenses densest, and what services dominate? | 1.7M licenses on a map. | one table | stack, same shape | never run |
| v2-088 | **How counties run elections** — Which jurisdictions rely most on mail ballots or fewest polling places? | One row per county, dozens of questions. | one table | single table | never run |
| v2-089 | **Judges' age at appointment by president** — Are presidents appointing younger judges over time? | A generational strategy in one chart. | one table | stack, same shape | never run |
| v2-090 | **Confirmation vote margins shrinking** — How did Senate confirmation margins for judges change by decade? | From unanimous to party-line. | one table | single table | never run |
| v2-091 | **Circuit courts by ideology** — Which circuits lean furthest left or right, and did that change? | One dot per judge, one row per circuit. | one table | single table | never run |
| v2-092 | **Supreme Court justices by term** — How did each justice's ideology score move term by term? | The famous chart, from the source. | one table | single table | never run |
| v2-093 | **Cannabis legalization map by year** — When did each state approve medical and recreational cannabis? | An animated map of policy spreading. | one table | single table | never run |
| v2-094 | **NYC donors, 2001 versus 2025** — How did the size and geography of NYC donations change across five cycles? | Five cycles, same city. | one table | stack, same shape | never run |
| v2-095 | **Lobbyists who used to work in government** — What share of federal lobbyists held a covered government job first? | Revolving door, counted. | one table | single table | never run |
| v2-096 | **Who pays to lobby Washington** — Which clients spend most on federal lobbying, and on what issues? | 820K filings, one ranking. | one table | single table | never run |
| v2-097 | **Foreign agents by country** — Which foreign governments hire the most registered agents in the US? | A map of influence buying. | one table | single table | never run |
| v2-098 | **Google political ads: who they target** — Which advertisers target which age and gender, and how much did they spend weekly? | Targeting made visible. | one table | stack, same shape | never run |
| v2-099 | **Federal Register output per agency** — Which agencies publish the most rules, and how did executive orders spike by year? | Government activity as a line. | one table | single table | never run |
| v2-100 | **Jobs with an industry interest** — Which federal roles have the most industries with a financial stake? | Small table, sharp question. | one table | single table | never run |
| v2-101 | **Roll calls that split parties** — Which votes had the most members crossing party lines? | Vote-level drama. | one table | stack, same shape | never run |
| v1-125 | **Political nonprofits that lost their tax status** — Are they still operating and filing paperwork as if nothing happened? | Would show a compliance gap | two tables |  | never run |
| v1-78 | **U.S. Senators** — Do they trade stock in industries their own committee oversees? | The core 'Congress insider trading' question | two tables |  | never run |
| v1-86 | **Political advertisers on Google** — Are big-spending political advertisers avoiding official campaign finance reporting? | Would show a loophole in campaign finance transparency | two tables |  | never run |
| v1-89 | **State-level lobbyists** — Do the same people wine and dine state lawmakers and donate federally? | Would show a two-level influence operation | two tables |  | never run |
| v1-93 | **Counties running elections** — Do places with more rejected mail ballots overlap with high-incarceration areas? | Would connect two forms of disenfranchisement | two tables |  | never run |
| v1-A35 | **Members of Congress and their stock trades** — Do members trade stock in industries their committee oversees? | This is the classic 'insider trading in Congress' question | two tables |  | never run |
| v1-A36 | **Fraud-flagged health industries and political donations** — Do the industries caught defrauding Medicare fund the committees that oversee Medicare? | Would show the fox funding the henhouse | two tables |  | never run |
| v2-102 | **Cosponsoring and ideology** — Do moderates cosponsor more bills across the aisle? | Catalog item 46. | two tables | BIOGUIDE / ICPSR | never run |
| v2-103 | **Committee seats and bills sponsored** — Do members on more committees sponsor more bills? | Catalog item 47. | two tables | BIOGUIDE | never run |
| v2-104 | **Senators trading in what they oversee** — Do senators trade stocks in sectors their committees regulate? | The chart people will screenshot. | two tables | BIOGUIDE | never run |
| v2-105 | **Money raised versus margin won** — Does raising more money buy a bigger win? | Catalog FEC family. | two tables | FEC_CAND_ID | never run |
| v2-106 | **Individual money per committee per candidate** — Which candidates' committees run on small donors? | Catalog item 42. | two tables | FEC_CMTE_ID / CAND_ID | never run |
| v2-107 | **PAC money versus individual money** — Which committees lean on PACs rather than people? | Catalog item 43. | two tables | FEC_CMTE_ID | never run |
| v2-108 | **Leadership PACs per politician** — Which officeholders run the most leadership PACs and where does the money go? | Catalog item 44. | two tables | FEC_CMTE_ID / CAND_ID | never run |
| v2-109 | **Outside money for and against** — Which candidates drew the most independent spending against them? | Support versus oppose in one bar. | two tables | FEC_CAND_ID | never run |
| v2-110 | **PAC money and party loyalty** — Do members who take more PAC money vote with their party more? | Built member tables share the member key. | two tables | BIOGUIDE | never run |
| v2-111 | **Judge ideology by appointing president** — How far apart are each president's appointees on the ideology scale? | Presidents as color bands. | two tables | CL_PERSON_ID / FJC id | never run |
| v2-112 | **Lobbying firms and their clients, California** — Which firms serve the most employers, and which employers hire the most firms? | A bipartite graph. | two tables | filer ID | never run |
| v2-113 | **Dark-money donors to dark-money groups** — Who gives the most to 527 groups, and which groups? | Schedule A meets the org roster. | two tables | EIN | never run |
| v2-114 | **Where 527 money gets spent** — Which vendors get paid most by 527 groups? | Schedule B is the spending side. | two tables | EIN | never run |
| v2-115 | **One member of Congress, every table** — For one member: ideology, votes, bills, committees, money, trades, donors? | A card that proves the warehouse links up. | a chain | BIOGUIDE, FEC_CAND_ID | never run |
| v2-116 | **Follow the money** — From individual donor to committee to candidate to outside spending, as one flow? | A sankey of an election. | a chain | FEC_CMTE_ID, FEC_CAND_ID | never run |
| v2-117 | **Texas lobbying, whole picture** — Who spent what on which official, on which subject, for which client? | Six tables, one filer. | a chain | filer ID | never run |
| v2-118 | **Judicial confirmations against Senate polarization** — Did confirmation margins narrow as the Senate polarized, year by year? | Two long series on one axis. | a chain | year | never run |
| v1-88 | **People who run political nonprofits** — Are the same people also treasurers of federal campaign committees? | Would show one person managing both a public and 'dark money' operation | two tables |  | needs a piece |

**Working notes — 62 of these 62 carry them**

| ID | Size | Years | Effort | Watch out | Needs | Notes, matches, results |
|---|---|---|---|---|---|---|
| v1-84 | 308,215 | by cycle | Medium — first probe query needed | roster is one row per congress; select distinct before joining or it fans out 5.7x | done: IE junk flagged, roster now per congress 113-119 | v2-Outside money for and against · reports/politics_probe_2026-09-05/84_ie_at_cms_overseers |
| v2-066 |  |  |  |  |  | 51K member-Congress rows. · visual: timeline |
| v2-067 |  |  |  |  |  | XC version adds each circuit. · visual: timeline |
| v2-068 |  |  |  |  |  | Built table. · visual: ranking |
| v2-069 |  |  |  |  |  | Built table. · visual: other |
| v2-070 |  |  |  |  |  | 1.27M rows. The BILLS-era table is a smaller sibling. · visual: other |
| v2-071 |  |  |  |  |  | FINANCE__SENATE_TRADES merges both sources with Bioguide. · visual: timeline |
| v2-072 |  |  |  |  |  | visual: timeline |
| v2-073 |  |  |  |  |  | Several tables shown side by side, no join. If a join is wanted, it is not in the catalog. · visual: map |
| v2-074 |  |  |  |  |  | visual: ranking |
| v2-075 |  |  |  |  |  | Same filer ID across tables; not a catalog key. · visual: ranking |
| v2-076 |  |  |  |  |  | visual: timeline |
| v2-077 |  |  |  |  |  | visual: ranking |
| v2-078 |  |  |  |  |  | Several tables shown side by side, no join. If a join is wanted, it is not in the catalog. · visual: ranking |
| v2-079 |  |  |  |  |  | visual: ranking |
| v2-080 |  |  |  |  |  | v1-88 · visual: ranking |
| v2-081 |  |  |  |  |  | Several tables shown side by side, no join. If a join is wanted, it is not in the catalog. · visual: other |
| v2-082 |  |  |  |  |  | visual: timeline |
| v2-083 |  |  |  |  |  | visual: map |
| v2-084 |  |  |  |  |  | visual: timeline |
| v2-085 |  |  |  |  |  | visual: other |
| v2-086 |  |  |  |  |  | visual: map |
| v2-087 |  |  |  |  |  | Rollup already exists in PUBLIC. · visual: map |
| v2-088 |  |  |  |  |  | Column names are survey codes. Needs a decoder. · visual: map |
| v2-089 |  |  |  |  |  | Several tables shown side by side, no join. If a join is wanted, it is not in the catalog. · visual: timeline |
| v2-090 |  |  |  |  |  | visual: timeline |
| v2-091 |  |  |  |  |  | visual: other |
| v2-092 |  |  |  |  |  | visual: timeline |
| v2-093 |  |  |  |  |  | Dozens of rule columns for follow-ups. · visual: map |
| v2-094 |  |  |  |  |  | Same shape, stack them. · visual: map |
| v2-095 |  |  |  |  |  | visual: ranking |
| v2-096 |  |  |  |  |  | Table is misfiled under EDUCATION. · visual: ranking |
| v2-097 |  |  |  |  |  | visual: map |
| v2-098 |  |  |  |  |  | Misfiled under EDUCATION. · v1-86 · visual: timeline |
| v2-099 |  |  |  |  |  | visual: timeline |
| v2-100 |  |  |  |  |  | 405 rows. · visual: ranking |
| v2-101 |  |  |  |  |  | Same roll-call ID; not a catalog key. · visual: ranking |
| v1-125 | 1,340,465 | after revocation | Medium — first probe query needed | no query run yet, treat any first number as unverified |  |  |
| v1-78 | 957,752 | 30-day windows | Medium — first probe query needed | amounts are ranges not numbers; roster needs select distinct | senate trades now to 2026; roster covers 113-119 | v2-Senators trading in what they oversee · reports/politics_probe_2026-09-05/78_senators_trade_their_committee |
| v1-86 | 374,229 | by cycle | Medium — first probe query needed | no query run yet, treat any first number as unverified |  | v2-Google political ads: who they target · reports/politics_probe_2026-09-05/86_google_ads_no_fec |
| v1-89 | 84,980,743 | by year | Medium — first probe query needed | no query run yet, treat any first number as unverified | FEC indiv now 14 cycles, 2000-2026, 283.8M rows | reports/politics_probe_2026-09-05/89_state_gifts_federal_checks |
| v1-93 | 164,603 | survey cycles | Medium — first probe query needed | no query run yet, treat any first number as unverified |  | reports/politics_probe_2026-09-05/93_rejected_ballots_jail |
| v1-A35 | 45,762 | untimed | Medium — first probe query needed | no query run yet, treat any first number as unverified |  | v2-Senators trading in what they oversee |
| v1-A36 | 870,609 | untimed | Medium — first probe query needed | roster is one row per congress; select distinct before joining or dollars fan out | roster now covers congresses 113-119; nothing else blocking | v2-Follow the money |
| v2-102 |  |  |  |  |  | visual: other |
| v2-103 |  |  |  |  |  | visual: other |
| v2-104 |  |  |  |  |  | Sector needs a ticker-to-industry lookup; see wanted list. · v1-78/v1-A35/v1-91 · visual: other |
| v2-105 |  |  |  |  |  | visual: other |
| v2-106 |  |  |  |  |  | 284M rows. Use the PUBLIC rollup first. Not a catalog key; lookup or unproven. · visual: ranking |
| v2-107 |  |  |  |  |  | visual: other |
| v2-108 |  |  |  |  |  | Not a catalog key; lookup or unproven. · visual: flow |
| v2-109 |  |  |  |  |  | v1-84 · visual: ranking |
| v2-110 |  |  |  |  |  | visual: other |
| v2-111 |  |  |  |  |  | FJC id to ideology table key not in catalog; check. Not a catalog key; lookup or unproven. · visual: other |
| v2-112 |  |  |  |  |  | Same source ID, not a catalog key. · visual: other |
| v2-113 |  |  |  |  |  | EIN family, 34 tables; confirm both are in it. · visual: ranking |
| v2-114 |  |  |  |  |  | visual: ranking |
| v2-115 |  |  |  |  |  | visual: other |
| v2-116 |  |  |  |  |  | v1-85/v1-A36 · visual: flow |
| v2-117 |  |  |  |  |  | Same-source filer ID, not a catalog key. · visual: other |
| v2-118 |  |  |  |  |  | Year is a lookup, not a catalog key. · visual: timeline |
| v1-88 | 249,624 | untimed | Medium — first probe query needed | no query run yet, treat any first number as unverified | 527 Schedule A and B landed, 17.9M rows | v2-People on many dark-money boards · reports/politics_probe_2026-09-05/88_shared_treasurers |

## Courts and enforcement — 62 questions

62 live, 0 needing a piece, 0 came back empty.

| ID | The question | Why it matters | Tables | Joins on | Status |
|---|---|---|---|---|---|
| v1-139 | **Gun dealers** — Are more dealers in an area linked to more gun deaths? | Tests a long-running gun policy question | two tables |  | started, unfinished |
| v2-163 | **Sentence length by charge and district** — Do the same federal charges get different prison time in different districts? | Same crime, different years behind bars. | one table | single table | never run |
| v2-164 | **What people sue about, by decade** — Which civil case types grew and shrank in federal court? | A stacked area of a country's grievances. | one table | single table | never run |
| v2-165 | **Bankruptcies per county per year** — Where did personal bankruptcy spike, and when? | A map that lights up in 2009. | one table | single table | never run |
| v2-166 | **Reversal rate by circuit** — Which appeals circuits overturn the most lower-court rulings? | One bar per circuit. | one table | single table | never run |
| v2-167 | **Which justices vote together** — How often does each pair of justices agree, term by term? | The agreement matrix. | one table | single table | never run |
| v2-168 | **5-4 decisions per term** — How many cases were decided by one vote each term? | A count that tracks the court's temperature. | one table | single table | never run |
| v2-169 | **Most-cited opinions** — Which rulings get cited most, and who wrote them? | A leaderboard of law. | one table | single table | never run |
| v2-170 | **Citation web** — Which opinions cite which, and where are the hubs? | A graph of precedent. | one table | single table | never run |
| v2-171 | **Gifts to federal judges** — Who gives judges gifts, and which judges get the most? | The disclosure forms, itemized. | one table | single table | never run |
| v2-172 | **Who pays for judges' travel** — Which organizations reimburse judges most, and for trips where? | Junkets on a map. | one table | single table | never run |
| v2-173 | **Judges' stock holdings** — Which companies show up most in judges' investment disclosures? | 1.9M holdings. | one table | single table | never run |
| v2-174 | **Judges' spouses' income sources** — Where do judges' spouses earn, by employer type? | A side of the bench nobody charts. | one table | single table | never run |
| v2-175 | **Judges' debts** — Which creditors hold the most judge debt? | Debts on the record. | one table | single table | never run |
| v2-176 | **Law schools of the bench** — Which schools produce the most federal judges, by decade? | A ranking that changes slowly. | one table | stack, same shape | never run |
| v2-177 | **Party affiliation by court** — Which courts have swung party over time? | Affiliation periods as color bars. | one table | single table | never run |
| v2-178 | **Race and gender on the bench** — How did the bench's race and gender mix change per decade of appointment? | Slow change, visible. | one table | CL_PERSON_ID | never run |
| v2-179 | **Crimes solved, by state** — Which states clear the fewest reported crimes, and did it change since 1985? | Clearance rate is the number nobody quotes. | one table | single table | never run |
| v2-180 | **Gun background checks by month** — When did gun checks spike, state by state? | Spikes line up with news. | one table | single table | never run |
| v2-181 | **Gun dealers per county** — Where are licensed gun dealers densest per resident? | 77K dealers, every address. | one table | FIPS | never run |
| v2-182 | **People killed by police** — How many per year, by race, armed status, and were officers charged? | Two trackers, one chart. | one table | stack, same shape | never run |
| v2-183 | **County jail rates over time** — Which counties' jail rates climbed most since 1970? | Vera's county trends, animated. | one table | single table | never run |
| v2-184 | **The racial jail gap by county** — Where is the Black-white jail rate gap widest? | Built table, one map. | one table | single table | never run |
| v2-185 | **Overdose and jail, worst-tenth counties** — Which counties are in the worst tenth for both overdose and jail? | Built table with the flag. | one table | single table | never run |
| v2-186 | **Sanctioned ships** — Which sanctioned vessels exist, under which programs? | OFAC lists ship details. | one table | single table | never run |
| v2-187 | **Thirteen blacklists in one** — Which entries appear on several federal screening lists? | Overlap counted. | one table | single table | never run |
| v2-188 | **A million sanctioned targets** — How does the global watchlist split by country, type, and crypto wallets? | Crypto wallets on a sanctions list is new. | one table | single table | never run |
| v2-189 | **Exploited software flaws** — Which vendors' flaws get exploited most, and how many are ransomware-used? | Product names people recognize. | one table | single table | never run |
| v2-190 | **Ransomware gangs and their victims** — Which gangs claim the most victims, in which countries, by month? | Gang names on a timeline. | one table | single table | never run |
| v2-191 | **Conflict deaths on a map** — Where did conflict events cluster, and how deadly, year by year? | 386K events. | one table | single table | never run |
| v2-192 | **North Korean missile tests, two trackers** — Do the two trackers agree on count, type, and outcome? | Disagreement between sources is itself the chart. | one table | stack, same shape | never run |
| v2-193 | **Human rights violations by country and article** — Which countries lose most at the European court, on which articles? | 2,000 rulings. | one table | single table | never run |
| v2-194 | **Homicide, warheads, terrorism by country** — Three OWID series on one country page? | Simple world context. | one table | country + year | never run |
| v2-195 | **Missouri registry by county** — Where are registrants per resident highest, and what share are noncompliant? | A state registry, mapped. | one table | single table | never run |
| v2-196 | **FTC cases by topic** — What does the FTC go after, and did it shift? | 1,004 cases. | one table | single table | never run |
| v2-197 | **Biggest multidistrict lawsuits** — Which MDLs hold the most pending cases? | A ranking of mass litigation. | one table | single table | never run |
| v2-198 | **Bank enforcement fines** — Which banks were fined most by the FDIC, and when? | Bank names and dollar amounts. | one table | single table | never run |
| v2-199 | **Oral argument transcripts** — Which judges talk most in oral argument, by word count? | Transcript text as data. | one table | single table | never run |
| v2-200 | **Courthouses map** — Where are federal courthouses, and which counties are far from one? | Distance-to-court map. | one table | FIPS | never run |
| v1-122 | **People who control companies registered in the U.K.** — Are any of them under U.S. or international sanctions? | Would show sanctioned people still running real companies | two tables |  | never run |
| v1-136 | **Government tech vendors** — Do the ones with the most known security flaws still win contracts? | Would show government still paying risky vendors | two tables |  | never run |
| v1-137 | **Ships owned by sanctioned entities** — Are any of them showing up at U.S. ports anyway? | Would be a sanctions violation happening in plain sight | two tables |  | never run |
| v1-138 | **Police departments** — Do the ones involved in the most killings still get the most federal grant money? | Would question how federal funding is allocated | two tables |  | never run |
| v1-77 | **Federal judges** — Do they own stock in companies whose cases they're deciding? | Would be a serious conflict of interest | two tables |  | never run |
| v1-94 | **Federal judges** — Does a judge's political leaning or donations predict how they rule? | A long-debated fairness-of-the-courts question | two tables |  | never run |
| v1-95 | **Federal judges** — Do gifts or debts they report ever involve parties in their own courtroom? | Would be a direct conflict of interest | two tables |  | never run |
| v2-201 | **Judge positions against party** — Do judges with a party affiliation hold more outside positions? | Catalog item 48. | two tables | CL_PERSON_ID | never run |
| v2-202 | **Disclosures per judge against positions held** — Which judges file the most disclosures relative to positions? | Catalog item 49. | two tables | CL_PERSON_ID | never run |
| v2-203 | **Judges per court against cases filed** — Which courts are most overloaded per judge? | Catalog item 50. | two tables | CL_COURT_ID | never run |
| v2-204 | **Opinions per case by case type** — Which case types generate the most written opinions? | Catalog item 51. | two tables | DOCKET | never run |
| v2-205 | **Oral arguments against opinions** — Do argued cases get more opinions? | Catalog item 52. | two tables | DOCKET | never run |
| v2-206 | **Jail rate against injury deaths** — Do high-jail counties also have high injury and violence death rates? | Catalog item 39. | two tables | FIPS | never run |
| v2-207 | **Judges' gifts against their positions** — Which outside positions come with the most gifts and travel? | Gift and reimbursement tables meet positions. | two tables | CL_PERSON_ID | never run |
| v2-208 | **Judge holdings against Senate trades** — Which stocks appear in both judges' and senators' disclosures? | Two branches, same tickers. | two tables | ticker / asset name | never run |
| v2-209 | **Sentencing by judge** — Which judges hand down the longest sentences for the same charge? | Judge column exists in the criminal file. | two tables | judge code | never run |
| v2-210 | **Gun dealers against background checks** — Do states with more dealers per person run more checks per person? | State-level scatter. | two tables | state code | never run |
| v2-211 | **Same name, four sanctions lists** — Which targets appear on OFAC, EU, UK and UN lists at once? | A Venn of sanctions. | two tables | name | never run |
| v1-A37 | **People under U.S. or international sanctions** — Do sanctioned individuals still show up as political donors? | Would be a serious legal and ethics violation | a chain |  | never run |
| v2-212 | **One judge, every table** — For one judge: bio, courts, votes, ideology, disclosures, gifts, trips, holdings? | The judge card. | a chain | CL_PERSON_ID | never run |
| v2-213 | **Fifty years of federal court** — Civil, criminal, appellate and bankruptcy filings by district, one animated map? | The whole system breathing. | a chain | CL_COURT_ID / district code | never run |
| v2-214 | **One name across the sanctions world** — For one entity: every list, every program, every alias, every date? | Sanctions as a lookup. | a chain | name | never run |
| v1-107 | **Drug distributors and the state lawsuits against them** — Did the biggest distributors in a state match who actually got sued? | Would show whether settlements matched the actual harm done | two tables |  | never run |

**Working notes — 62 of these 62 carry them**

| ID | Size | Years | Effort | Watch out | Needs | Notes, matches, results |
|---|---|---|---|---|---|---|
| v1-139 | 225,959 | state level | Medium — partial run, needs finishing | Partially checked, real signal found |  | v2-Gun dealers per county |
| v2-163 |  |  |  |  |  | 6.3M defendants. · visual: other |
| v2-164 |  |  |  |  |  | visual: timeline |
| v2-165 |  |  |  |  |  | Chapter mix as a follow-up. · visual: map |
| v2-166 |  |  |  |  |  | visual: ranking |
| v2-167 |  |  |  |  |  | visual: other |
| v2-168 |  |  |  |  |  | visual: timeline |
| v2-169 |  |  |  |  |  | 10M rows. · visual: ranking |
| v2-170 |  |  |  |  |  | 6.4M citation rows. · visual: other |
| v2-171 |  |  |  |  |  | visual: ranking |
| v2-172 |  |  |  |  |  | visual: ranking |
| v2-173 |  |  |  |  |  | v1-77 · visual: ranking |
| v2-174 |  |  |  |  |  | visual: ranking |
| v2-175 |  |  |  |  |  | visual: ranking |
| v2-176 |  |  |  |  |  | School ID same-source; CL_PERSON_ID for judge. · visual: timeline |
| v2-177 |  |  |  |  |  | visual: timeline |
| v2-178 |  |  |  |  |  | visual: timeline |
| v2-179 |  |  |  |  |  | visual: map |
| v2-180 |  |  |  |  |  | visual: timeline |
| v2-181 |  |  |  |  |  | FFL has coordinates; county via lookup. · v1-139 · visual: map |
| v2-182 |  |  |  |  |  | Different coverage; do not add them together. · visual: timeline |
| v2-183 |  |  |  |  |  | visual: map |
| v2-184 |  |  |  |  |  | Built table. · visual: map |
| v2-185 |  |  |  |  |  | Built table. · v1-8 · visual: map |
| v2-186 |  |  |  |  |  | visual: ranking |
| v2-187 |  |  |  |  |  | visual: other |
| v2-188 |  |  |  |  |  | visual: other |
| v2-189 |  |  |  |  |  | visual: ranking |
| v2-190 |  |  |  |  |  | visual: timeline |
| v2-191 |  |  |  |  |  | visual: map |
| v2-192 |  |  |  |  |  | Several tables shown side by side, no join. If a join is wanted, it is not in the catalog. · visual: timeline |
| v2-193 |  |  |  |  |  | visual: other |
| v2-194 |  |  |  |  |  | Country code lookup. Not a catalog key; lookup or unproven. · visual: timeline |
| v2-195 |  |  |  |  |  | Names present. Aggregate only. · visual: map |
| v2-196 |  |  |  |  |  | visual: timeline |
| v2-197 |  |  |  |  |  | visual: ranking |
| v2-198 |  |  |  |  |  | visual: timeline |
| v2-199 |  |  |  |  |  | Transcript column where available. · visual: ranking |
| v2-200 |  |  |  |  |  | visual: map |
| v1-122 | 17,105,571 | notified/ceased dates | Medium — first probe query needed | no query run yet, treat any first number as unverified |  | v2-Sanctioned names in UK filings |
| v1-136 | 93,155,098 | by year | Medium — first probe query needed | no query run yet, treat any first number as unverified |  |  |
| v1-137 | 58,125,631 | after designation | Medium — first probe query needed | no query run yet, treat any first number as unverified |  | v2-Ships per owner against port calls |
| v1-138 | 19,918,355 | by year | Medium — first probe query needed | no query run yet, treat any first number as unverified |  |  |
| v1-77 | 12,810,285 | disclosure years | Medium — first probe query needed | no query run yet, treat any first number as unverified |  | v2-Judges' stock holdings · reports/politics_probe_2026-09-05/77_judges_stock_vs_parties |
| v1-94 | 95,037,994 | by judge | Medium — first probe query needed | no query run yet, treat any first number as unverified | FEC indiv now 14 cycles, 2000-2026, 283.8M rows | reports/politics_probe_2026-09-05/94_judge_politics_vs_dockets |
| v1-95 | 54,272 | disclosure years | Medium — first probe query needed | no query run yet, treat any first number as unverified |  | v2-Judges' gifts against their positions · reports/politics_probe_2026-09-05/95_judge_gifts_vs_parties |
| v2-201 |  |  |  |  |  | visual: other |
| v2-202 |  |  |  |  |  | visual: other |
| v2-203 |  |  |  |  |  | visual: ranking |
| v2-204 |  |  |  |  |  | DOCKET is mostly unproven: 17 tables, 2 edges. · visual: other |
| v2-205 |  |  |  |  |  | DOCKET unproven. · visual: other |
| v2-206 |  |  |  |  |  | v1-E52 · visual: other |
| v2-207 |  |  |  |  |  | v1-95 · visual: other |
| v2-208 |  |  |  |  |  | Not a catalog key. Fuzzy name match. · visual: other |
| v2-209 |  |  |  |  |  | Judge code not a catalog key. Needs proving. · visual: ranking |
| v2-210 |  |  |  |  |  | State is a lookup, not a catalog key. · visual: other |
| v2-211 |  |  |  |  |  | Name match only. Not a catalog key. · visual: other |
| v1-A37 | 84,250,573 | untimed | Medium — first probe query needed | no query run yet, treat any first number as unverified |  |  |
| v2-212 |  |  |  |  |  | CL_PERSON_ID: 8 tables, 28 edges. · visual: other |
| v2-213 |  |  |  |  |  | Not a catalog key; lookup or unproven. · visual: map |
| v2-214 |  |  |  |  |  | Name match only. Not a catalog key; lookup or unproven. · visual: other |
| v1-107 | 178,598,908 | 2006-14 vs settlement year | Medium — first probe query needed | no query run yet, treat any first number as unverified |  | v2-The opioid chain |

## Pollution and environment — 58 questions

53 live, 1 needing a piece, 4 came back empty.

| ID | The question | Why it matters | Tables | Joins on | Status |
|---|---|---|---|---|---|
| v1-22 | **Neighborhoods once graded 'hazardous' for housing loans in the 1930s** — Do those same neighborhoods have more toxic factories today? | Would prove 90-year-old racist housing policy still poisons people today | a chain |  | **found something** |
| v1-E33 | **Sewage treatment plants after storms** — Do they violate pollution rules more right after a storm? | Would show storms overwhelming sewage systems | two tables |  | found a little |
| v1-26 | **Counties hit by big storms, and government-subsidized housing** — Does housing sit empty after a big storm instead of getting rebuilt? | Would show disaster recovery money not reaching people | two tables |  | started, unfinished |
| v2-119 | **Repeat violators who paid nothing** — Which facilities broke rules most often and paid the least? | Built table with minority share nearby. | one table | single table | never run |
| v2-120 | **Dirtiest power plants** — Which plants emit the most CO2 per megawatt-hour? | Names and owners on a map. | one table | single table | never run |
| v2-121 | **Greenhouse gas by facility since 2010** — Which facilities cut emissions and which grew? | A slope chart per facility. | one table | stack, same shape | never run |
| v2-122 | **Toxic releases 2023** — Which facilities released the most, by chemical and by route? | Air, water, land as stacked bars. | one table | stack, same shape | never run |
| v2-123 | **Discharging into already impaired water** — How many permit holders dump into water already listed as impaired? | The flag is in the table. | one table | single table | never run |
| v2-124 | **Drinking water violations map** — Which water systems have the most health-based violations? | 15M rows to one map. | one table | single table | never run |
| v2-125 | **Lead at the tap** — Where did lead samples exceed the limit, and when? | Flint-style question, national scope. | one table | single table | never run |
| v2-126 | **Superfund sites map** — Where are Superfund sites and which are on the priority list? | Boundaries, not dots. | one table | single table | never run |
| v2-127 | **Fracking water use** — How much water does one frack job use, by state and year? | Gallons people can picture. | one table | single table | never run |
| v2-128 | **Trade-secret chemicals** — What share of fracking ingredients hide their chemical ID, and is it rising? | Secrecy as a trend line. | one table | single table | never run |
| v2-129 | **High-hazard dams in poor condition** — Which dams would kill people if they failed and are rated poor? | Map plus years since last inspection. | one table | single table | never run |
| v2-130 | **Storm damage by year** — Which storm types cause the most dollar damage and deaths per year? | Tornado tracks on a map. | one table | stack, same shape | never run |
| v2-131 | **Pipeline incidents by operator** — Which gas pipeline operators have the most serious incidents since 2010? | Operator names and deaths. | one table | single table | never run |
| v2-132 | **Spill calls to the Coast Guard** — How many spill calls per year, by type, and where? | A million calls. | one table | single table | never run |
| v2-133 | **Orphaned wells map** — Where are the abandoned oil and gas wells nobody will plug? | Dots that look like a rash. | one table | single table | never run |
| v2-134 | **A river over fifty years** — How did streamflow or groundwater level at one site change over decades? | Pick one gauge, one long line. | one table | single table | never run |
| v2-135 | **Killed defending land** — Where are environmental defenders killed, and by whom? | Names, countries, years. | one table | single table | never run |
| v2-136 | **Country CO2, fossil share, warming** — How do CO2, fossil share and temperature anomaly move together per country? | Three OWID series, one page. | one table | country + year | never run |
| v2-137 | **Air monitors opening and closing** — Where were air-quality monitors shut down? | Fewer monitors, less data. | one table | single table | never run |
| v2-138 | **High-priority air violators** — Which air-permitted facilities are flagged high-priority right now? | One flag, one map. | one table | single table | never run |
| v2-139 | **Admitted deviations** — What share of big air polluters admit deviating from their permit each year? | Self-reported honesty. | one table | single table | never run |
| v2-140 | **Hazardous waste, months in violation** — Which handlers stayed in serious violation the longest? | A month-by-month status strip. | one table | single table | never run |
| v2-141 | **Stack tests failed** — Which facilities fail smokestack tests most? | Pass-fail, per facility. | one table | single table | never run |
| v2-142 | **Minerals by country** — Which countries hold the reserves of each critical mineral? | A world map per mineral. | one table | single table | never run |
| v2-143 | **Water system size versus owner type** — Are small private systems more common than people think? | Population served by owner type. | one table | single table | never run |
| v1-101 | **Counties hit hard by flooding** — Are they still using outdated flood maps? | Would show regulators failing to update risk after real damage | two tables |  | never run |
| v1-103 | **Companies that report chemical or oil spills** — Do they still win federal contracts afterward? | Would show spillers getting rewarded, not penalized | two tables |  | never run |
| v1-142 | **Industrial facilities** — Do some have pollution spikes that never trigger a violation? | Would show gaps in pollution enforcement | two tables |  | never run |
| v1-A34 | **Members of Congress and pollution in their district** — Do polluted districts get less help from their representative? | Would show political neglect of poisoned communities | two tables |  | never run |
| v2-144 | **Violations per permit against inspections** — Do more inspections find more violations, or fewer? | Catalog item 26. | two tables | NPDES_ID | never run |
| v2-145 | **Enforcement by industry** — Which industries draw the most enforcement per facility? | Catalog item 27. | two tables | NPDES_ID | never run |
| v2-146 | **Quarterly noncompliance by old industry code** — Which SIC sectors are chronically noncompliant? | Catalog item 28. | two tables | NPDES_ID | never run |
| v2-147 | **Violations per person served** — Which water systems have the most violations per resident? | Catalog item 29. | two tables | PWSID | never run |
| v2-148 | **Site visits against violations** — Do systems with more visits have fewer violations? | Catalog item 30. | two tables | PWSID | never run |
| v2-149 | **Lead exceedances by area served** — Which cities and zips drink from systems with lead exceedances? | Catalog item 31. | two tables | PWSID | never run |
| v2-150 | **Air emissions by corporate parent** — Which parent companies own the most air pollution? | Catalog item 32. | two tables | FRS_ID | never run |
| v2-151 | **Toxic releases per county** — Which counties carry the most toxic release per resident? | Catalog item 33. | two tables | FIPS | never run |
| v2-152 | **EPA facilities against county jobs** — Do counties with more EPA facilities have more jobs, or just more pollution? | Catalog item 37. | two tables | FIPS | never run |
| v2-153 | **Storms and FEMA housing aid** — Which counties' storm damage turned into the most FEMA housing registrations? | Catalog item 40. | two tables | FIPS | never run |
| v2-154 | **Subsidiaries with EPA facilities** — Which global parents own the most EPA-tracked facilities through subsidiaries? | Catalog item 53. | two tables | LEI | never run |
| v2-155 | **Penalties against releases** — Do facilities that release the most pay the most? | ECHO penalties meet TRI pounds. | two tables | FRS_ID | never run |
| v2-156 | **Facilities in every program** — Which facilities are in air, water, waste and toxic programs all at once? | Program links per facility, counted. | two tables | FRS_ID | never run |
| v2-157 | **Fracking water by source** — Where does frack water come from, and does that differ by state? | Source table meets job table. | two tables | job ID | never run |
| v2-158 | **Plant emissions by owner share** — Which utilities own the most emissions, weighted by share? | Catalog items 34 and 35. | two tables | EIA_PLANT_ID | never run |
| v1-102 | **Counties with lots of oil, gas, and fracking activity** — Do they also have the worst drinking water problems? | Would show industrial activity stacking up to hurt water quality | a chain |  | never run |
| v1-140 | **Owners of the most polluting power plants** — Which investment funds and political donors are behind them? | Would trace pollution back to who actually profits | a chain |  | never run |
| v2-159 | **One facility, every EPA system** — For one FRS ID: programs, inspections, violations, penalties, releases, gases, parent? | The facility page. | a chain | FRS_ID | never run |
| v2-160 | **Corporate polluter family tree** — From a global parent down through subsidiaries to facilities to violations? | A tree with pollution at the leaves. | a chain | LEI, FRS_ID | never run |
| v2-161 | **Your tap water** — For a zip: which system, its violations, lead samples, visits, milestones? | A lookup a reader will try on their own address. | a chain | PWSID | never run |
| v2-162 | **Wastewater permit, whole life** — Permit, inspections, violations, enforcement, quarterly scorecard, one timeline? | Every NPDES table on one strip. | a chain | NPDES_ID | never run |
| v1-17 | **Banks and the pollution sites they finance** — Same as v1-3, through a different bank record | Would show hidden bank-to-polluter money | two tables |  | needs a piece |
| v1-E32 | **Counties hit by floods** — Do drinking water violations spike after a flood? | Would show disaster damage hitting the water supply | two tables |  | came back empty |
| v1-E53 | **Poor and minority neighborhoods with water violations** — Do they get penalized less often than other neighborhoods? | Would show unequal enforcement of environmental law | two tables |  | came back empty |
| v1-E54 | **Factories that violate air pollution rules** — Do they pay workers less than clean factories? | Tests if pollution and low wages travel together | two tables |  | came back empty |
| v1-E55 | **Subsidized housing near polluting or noncompliant sites** — Is poor housing placed disproportionately near hazards? | Would show poor communities steered toward danger | two tables |  | came back empty |

**Working notes — 58 of these 58 carry them**

| ID | Size | Years | Effort | Watch out | Needs | Notes, matches, results |
|---|---|---|---|---|---|---|
| v1-22 | 276,792 | current | Quick — re-run and check the number | worst-graded areas have 18x more toxic sites than the best |  | v2-Redlined then, denied now · reports/tier1_deep_dive_2026-09-05/22_redlined_toxic_sites |
| v1-E33 | 9,732,386 | quarterly | Medium — partial run, needs finishing | Real but small, and it flips the wrong direction for related permits |  |  |
| v1-26 | 1,794,280 | 1996-2025, one MFH snapshot | Medium — partial run, needs finishing | Setup works, needs a real run |  |  |
| v2-119 |  |  |  |  |  | Built table. · visual: map |
| v2-120 |  |  |  |  |  | visual: map |
| v2-121 |  |  |  |  |  | Same facility ID; FRS_ID likely, confirm. · visual: timeline |
| v2-122 |  |  |  |  |  | Several tables shown side by side, no join. If a join is wanted, it is not in the catalog. · visual: ranking |
| v2-123 |  |  |  |  |  | visual: map |
| v2-124 |  |  |  |  |  | visual: map |
| v2-125 |  |  |  |  |  | visual: map |
| v2-126 |  |  |  |  |  | visual: map |
| v2-127 |  |  |  |  |  | visual: timeline |
| v2-128 |  |  |  |  |  | 7.2M rows. · visual: timeline |
| v2-129 |  |  |  |  |  | visual: map |
| v2-130 |  |  |  |  |  | Rollup exists in PUBLIC. · visual: timeline |
| v2-131 |  |  |  |  |  | visual: ranking |
| v2-132 |  |  |  |  |  | visual: timeline |
| v2-133 |  |  |  |  |  | visual: map |
| v2-134 |  |  |  |  |  | 6.5M readings. · visual: timeline |
| v2-135 |  |  |  |  |  | visual: map |
| v2-136 |  |  |  |  |  | Country code lookup, not a catalog key. · visual: timeline |
| v2-137 |  |  |  |  |  | visual: map |
| v2-138 |  |  |  |  |  | visual: map |
| v2-139 |  |  |  |  |  | visual: timeline |
| v2-140 |  |  |  |  |  | visual: timeline |
| v2-141 |  |  |  |  |  | visual: ranking |
| v2-142 |  |  |  |  |  | visual: map |
| v2-143 |  |  |  |  |  | visual: other |
| v1-101 | 1,805,855 | 2015+ | Medium — first probe query needed | no query run yet, treat any first number as unverified |  | v2-Flood insurance map |
| v1-103 | 94,350,772 | same years | Medium — first probe query needed | no query run yet, treat any first number as unverified |  |  |
| v1-142 | 16,637,002 | daily | Medium — first probe query needed | no query run yet, treat any first number as unverified |  |  |
| v1-A34 | 4,980,621 | untimed | Medium — first probe query needed | no query run yet, treat any first number as unverified |  |  |
| v2-144 |  |  |  |  |  | visual: other |
| v2-145 |  |  |  |  |  | visual: ranking |
| v2-146 |  |  |  |  |  | visual: other |
| v2-147 |  |  |  |  |  | visual: map |
| v2-148 |  |  |  |  |  | visual: other |
| v2-149 |  |  |  |  |  | visual: map |
| v2-150 |  |  |  |  |  | visual: ranking |
| v2-151 |  |  |  |  |  | visual: map |
| v2-152 |  |  |  |  |  | visual: other |
| v2-153 |  |  |  |  |  | FEMA table is a partial load; counts are floors. · visual: map |
| v2-154 |  |  |  |  |  | visual: other |
| v2-155 |  |  |  |  |  | visual: other |
| v2-156 |  |  |  |  |  | visual: ranking |
| v2-157 |  |  |  |  |  | Same-source job ID; not a catalog key. · visual: other |
| v2-158 |  |  |  |  |  | EIA keys are in the keyset with zero edges. Unproven. · visual: ranking |
| v1-102 | 22,752,998 | current | Medium — first probe query needed | no query run yet, treat any first number as unverified |  |  |
| v1-140 | 3,886,063 | 2022 | Medium — first probe query needed | no query run yet, treat any first number as unverified |  | v2-Plant emissions against plant owner |
| v2-159 |  |  |  |  |  | FRS_ID: 17 tables, 136 edges. · visual: other |
| v2-160 |  |  |  |  |  | visual: flow |
| v2-161 |  |  |  |  |  | PWSID: 10 tables, 45 edges. · visual: other |
| v2-162 |  |  |  |  |  | visual: timeline |
| v1-17 | 5,327,985 | n/a | Skip — already ruled out | that bank ID field is empty everywhere |  |  |
| v1-E32 | 41,683,657 | 2015-2024 | Skip — already ruled out | only true in two states |  |  |
| v1-E53 | 3,220,945 | snapshot | Medium — partial run, needs finishing | those areas are actually penalized less |  |  |
| v1-E54 | 3,721,474 | one year | Skip — already ruled out | turned out to be about oil refineries specifically |  |  |
| v1-E55 | 18,603,892 | snapshot | Skip — already ruled out | no real pattern once population size is accounted for |  |  |

## Energy — 18 questions

18 live, 0 needing a piece, 0 came back empty.

| ID | The question | Why it matters | Tables | Joins on | Status |
|---|---|---|---|---|---|
| v2-290 | **Power plants by fuel and age** — When were plants built, by fuel, and when do they retire? | A generation-by-generation chart. | one table | single table | never run |
| v2-291 | **Coal retirements on a map** — Which coal generators are scheduled to retire, and where? | Retirement dates as a countdown. | one table | EIA_PLANT_ID | never run |
| v2-292 | **Wind turbines getting taller** — How did hub height and capacity grow by install year? | A physical fact people can picture. | one table | single table | never run |
| v2-293 | **Solar tracking share** — What share of solar generators track the sun, by state and year? | Technology adoption as a map. | one table | single table | never run |
| v2-294 | **Battery storage boom** — How fast did grid battery capacity grow, and what is it used for? | A hockey stick. | one table | single table | never run |
| v2-295 | **Who owns the generators** — Which owners hold the most capacity through partial stakes? | Ownership shares as a treemap. | one table | single table | never run |
| v2-296 | **Smart meters by utility** — Which utilities have rolled out smart meters, and which have not? | Old versus new meters, per utility. | one table | single table | never run |
| v2-297 | **Outage minutes by utility** — Whose customers lose power most often and longest? | Reliability ranking. | one table | single table | never run |
| v2-298 | **Rooftop solar selling back** — Which states have the most net-metered solar and paired batteries? | Customer-owned power, mapped. | one table | single table | never run |
| v2-299 | **Who serves which county** — Which utility serves each county, and which counties have several? | Service territory map. | one table | FIPS | never run |
| v2-300 | **Revenue per customer** — Which utilities charge the most per residential customer? | Sales table split by sector. | one table | single table | never run |
| v2-301 | **Energy efficiency spend** — Which utilities spend most on efficiency, and save most? | Savings per dollar. | one table | stack, same shape | never run |
| v2-302 | **World electricity mix** — Which countries' generation shifted most toward renewables? | Ember data, one stacked area per country. | one table | single table | never run |
| v2-303 | **Boilers and their pollution rules** — Which boilers meet which emissions standards, and how? | Compliance method per boiler. | one table | single table | never run |
| v2-304 | **Plant emissions against plant owner** — Which utilities own the dirtiest fleets? | Catalog items 34, 35. | two tables | EIA_PLANT_ID / UTILITY_ID | never run |
| v2-305 | **Outages against smart meters** — Do utilities with more smart meters report fewer outages? | Two EIA-861 tables, same utility ID. | two tables | UTILITY_ID | never run |
| v1-141 | **Power utility companies** — Do the ones with the worst storm outages also charge the highest rates? | Would show customers paying more for worse service | a chain |  | never run |
| v2-306 | **One utility, every table** — For one utility: plants, generators, customers, outages, meters, territory? | The utility card. | a chain | UTILITY_ID | never run |

**Working notes — 18 of these 18 carry them**

| ID | Size | Years | Effort | Watch out | Needs | Notes, matches, results |
|---|---|---|---|---|---|---|
| v2-290 |  |  |  |  |  | Operating and planned retirement dates. · visual: timeline |
| v2-291 |  |  |  |  |  | EIA keys in keyset, zero edges. · visual: map |
| v2-292 |  |  |  |  |  | visual: timeline |
| v2-293 |  |  |  |  |  | visual: map |
| v2-294 |  |  |  |  |  | visual: timeline |
| v2-295 |  |  |  |  |  | visual: other |
| v2-296 |  |  |  |  |  | visual: ranking |
| v2-297 |  |  |  |  |  | visual: ranking |
| v2-298 |  |  |  |  |  | visual: map |
| v2-299 |  |  |  |  |  | visual: map |
| v2-300 |  |  |  |  |  | visual: ranking |
| v2-301 |  |  |  |  |  | Several tables shown side by side, no join. If a join is wanted, it is not in the catalog. · visual: ranking |
| v2-302 |  |  |  |  |  | visual: timeline |
| v2-303 |  |  |  |  |  | visual: other |
| v2-304 |  |  |  |  |  | Zero edges yet. · v1-140 · visual: ranking |
| v2-305 |  |  |  |  |  | Zero edges yet. · v1-141 · visual: other |
| v1-141 | 1,796,291 | by year | Medium — first probe query needed | no query run yet, treat any first number as unverified |  | v2-Outages against smart meters |
| v2-306 |  |  |  |  |  | Needs the EIA edges built first. · visual: other |

## Banks, markets and corporate money — 43 questions

42 live, 0 needing a piece, 1 came back empty.

| ID | The question | Why it matters | Tables | Joins on | Status |
|---|---|---|---|---|---|
| v1-E64 | **Government grant recipients flagged for weak financial controls** — Does the money keep flowing to them anyway? | Would show oversight failing in real time | two tables |  | found a little |
| v1-118 | **Banks that make small business loans** — Do the ones with the worst loan losses also have enforcement actions against them? | Would show risky lenders getting away with it | two tables |  | started, unfinished |
| v1-128 | **Home loan banks and their member banks** — Were failed banks still active members right up until they collapsed? | Would question the system's early warning ability | two tables |  | started, unfinished |
| v2-242 | **County wages by industry** — Which counties pay best in each industry, and where did wages stall? | 3.6M rows to one map. | one table | single table | never run |
| v2-243 | **Federal jobs share by county** — Which counties depend most on federal employment? | Ownership column splits federal from private. | one table | single table | never run |
| v2-244 | **OSHA inspections by industry** — Which industries get inspected most, and find the most violations? | 5.2M inspections. | one table | single table | never run |
| v2-245 | **The 2008 bank failure wave** — When did banks fail, how big, and what did it cost the insurance fund? | A timeline with a wall in 2009. | one table | single table | never run |
| v2-246 | **Foreign aid flow** — Which agencies send how much to which countries? | Agency to country sankey. | one table | single table | never run |
| v2-247 | **Nonprofits per resident** — Which counties have the most nonprofits per person, by category? | Two million orgs on a map. | one table | stack, same shape | never run |
| v2-248 | **The auto-revocation wave** — How many nonprofits lost status per year, and how many came back? | 1.2M revocations, one spike. | one table | stack, same shape | never run |
| v2-249 | **Failed pensions, who got hurt** — Which sponsors' pension plans failed, and how many participants? | Company names next to headcounts. | one table | stack, same shape | never run |
| v2-250 | **SBA loan default rate by lender** — Which lenders' SBA loans default most? | Default flag exists. | one table | single table | never run |
| v2-251 | **PPP loans, jobs claimed per dollar** — Which borrowers claimed the fewest jobs per loan dollar? | Pandemic money, itemized. | one table | stack, same shape | never run |
| v2-252 | **PPP by franchise** — Which franchise brands' locations took the most PPP money? | Brand names. | one table | single table | never run |
| v2-253 | **Federal contracts by agency and industry** — Which agencies buy what, and how concentrated are vendors? | 6.3M contract actions. | one table | stack, same shape | never run |
| v2-254 | **Contract dollars per state** — Which states get the most federal contract money per resident? | Map with population. | one table | state code | never run |
| v2-255 | **National debt every day** — How did the debt move day by day, public versus intragovernmental? | One line, every day. | one table | single table | never run |
| v2-256 | **The government's daily cash** — What does the Treasury take in and pay out each day? | Daily ledger as a rhythm chart. | one table | single table | never run |
| v2-257 | **Interest the government pays** — How did the average rate on each security type move? | Rates by type over time. | one table | single table | never run |
| v2-258 | **Tax receipts by category** — Which receipt categories rose and fell month to month? | Monthly, with last-year comparison. | one table | single table | never run |
| v2-259 | **Company registrations by country** — Which countries register the most legal entities? | 3.4M entities. | one table | single table | never run |
| v2-260 | **Why companies will not name their parent** — What reasons do companies give for not reporting their parent? | 6.3M refusals, a handful of reasons. | one table | single table | never run |
| v2-261 | **Corporate family trees** — Which parents have the most subsidiaries? | A tree graph. | one table | single table | never run |
| v2-262 | **Hunger by country** — Which countries' food insecurity worsened? | FAO and IPC on one map. | one table | country + year | never run |
| v2-263 | **Inequality by country** — Which countries' Gini rose most? | OWID series. | one table | single table | never run |
| v2-264 | **Retirement plans by assets** — Which sponsors hold the biggest plans, and how much do they pay out? | Form 5500. | one table | single table | never run |
| v2-265 | **Audit findings on grant money** — Which grantees had material weaknesses, and how much did they spend? | Single audits. | one table | single table | never run |
| v1-114 | **Workplaces with rising injury rates** — Are they going uninspected for years at a time? | Would show safety regulators missing obvious warning signs | two tables |  | never run |
| v1-80 | **Companies whose own auditors doubt they can survive** — Do they still keep winning government contracts? | Would show the government not checking a known red flag | two tables |  | never run |
| v2-266 | **E-filings per nonprofit against assets** — Do bigger nonprofits file more? | Catalog item 11. | two tables | EIN | never run |
| v2-267 | **Revocations against active nonprofits** — Which states lose the most nonprofits per active one? | Catalog item 12. | two tables | EIN | never run |
| v2-268 | **Deductible against total** — What share of nonprofits per subsection can take deductible gifts? | Catalog item 13. | two tables | EIN | never run |
| v2-269 | **Injuries per employer against industry peers** — Which employers injure far more than their industry? | Catalog item 14. | two tables | EIN, NAICS | never run |
| v2-270 | **Federal money against nonprofit revenue** — Which nonprofits live almost entirely on federal grants? | Catalog item 15. | two tables | EIN | never run |
| v2-271 | **Contract vendors who also get grants** — Which vendors take both contract and assistance money? | Catalog item 17. | two tables | UEI | never run |
| v2-272 | **NIH grants against SBIR awards** — Which small companies win both NIH and SBIR money? | Catalog item 19. | two tables | UEI | never run |
| v2-273 | **Banned vendors still getting contracts** — Did any excluded vendor receive a contract after exclusion? | Catalog item 20. | two tables | UEI / DUNS | never run |
| v2-274 | **Hospital nonprofits: pay against assets** — Do bigger hospital nonprofits pay executives more per asset dollar? | EIN links the pay table to the master list. | two tables | EIN | never run |
| v2-275 | **PPP borrowers with OSHA injuries** — Did the biggest PPP borrowers also report the most injuries? | Fuzzy name-and-zip match. | two tables | NAME@ZIP | never run |
| v1-123 | **U.S. banks and polluters with unclear corporate parents** — Who's the real parent company hiding behind them? | Would unmask ownership nobody discloses | a chain |  | never run |
| v2-276 | **One nonprofit, every table** — For one EIN: master record, filings, revocations, audits, federal money, officer pay? | EIN is a steel key. | a chain | EIN | never run |
| v2-277 | **Federal money by county** — Contracts, PPP, SBA, grants, FEMA, relief: dollars per resident per county? | Where the money lands. | a chain | FIPS | never run |
| v1-E65 | **Nonprofits that lost their tax-exempt status** — Were they still getting paid after losing it? | Would be a rules violation | two tables |  | came back empty |

**Working notes — 43 of these 43 carry them**

| ID | Size | Years | Effort | Watch out | Needs | Notes, matches, results |
|---|---|---|---|---|---|---|
| v1-E64 | 20,314,517 | capped table | Medium — partial run, needs finishing | Modest signal, but the data only covers a few months |  |  |
| v1-118 | 2,185,354 | orders 1975-2026 (thin before 1990; 23 undated); SBA loans by year | Medium — name match SBA lender to FDIC directory first | Orders landed 2026-09-07 (10,838, one row per order, cert on 97.5%). ORDER_ID is the key, not DOCKET_NUMBER (8,302 distinct). CERT_NUMBER reads 'N/A' on 183 rows, use try_to_number. ORDER_TYPE is a semicolon list on combined orders, use LIKE. SBA side has no cert: lender name + state to the FDIC directory is the bridge, and generic bank names collide. | SBA lender name to FDIC cert bridge (SBA loans carry LENDER_NAME + LENDER_STATE, no cert) | reports/dead_ends_build_C_fdic_orders_2026-09-07.md |
| v1-128 | 9,911 | at failure | Skip — already ruled out | Partially checked, one piece of the puzzle is a dead end |  |  |
| v2-242 |  |  |  |  |  | visual: map |
| v2-243 |  |  |  |  |  | visual: map |
| v2-244 |  |  |  |  |  | visual: ranking |
| v2-245 |  |  |  |  |  | visual: timeline |
| v2-246 |  |  |  |  |  | visual: flow |
| v2-247 |  |  |  |  |  | State rollup in PUBLIC. · visual: map |
| v2-248 |  |  |  |  |  | Several tables shown side by side, no join. If a join is wanted, it is not in the catalog. · visual: timeline |
| v2-249 |  |  |  |  |  | Two tables, same subject. · visual: ranking |
| v2-250 |  |  |  |  |  | visual: ranking |
| v2-251 |  |  |  |  |  | 150K+ table has franchise and forgiveness columns. · visual: other |
| v2-252 |  |  |  |  |  | visual: ranking |
| v2-253 |  |  |  |  |  | Rollups in PUBLIC. · visual: other |
| v2-254 |  |  |  |  |  | Not a catalog key; lookup or unproven. · visual: map |
| v2-255 |  |  |  |  |  | visual: timeline |
| v2-256 |  |  |  |  |  | visual: timeline |
| v2-257 |  |  |  |  |  | visual: timeline |
| v2-258 |  |  |  |  |  | visual: timeline |
| v2-259 |  |  |  |  |  | visual: map |
| v2-260 |  |  |  |  |  | visual: ranking |
| v2-261 |  |  |  |  |  | visual: flow |
| v2-262 |  |  |  |  |  | Not a catalog key; lookup or unproven. · visual: map |
| v2-263 |  |  |  |  |  | visual: timeline |
| v2-264 |  |  |  |  |  | visual: ranking |
| v2-265 |  |  |  |  |  | visual: ranking |
| v1-114 | 9,214,469 | three years | Medium — first probe query needed | no query run yet, treat any first number as unverified |  |  |
| v1-80 | 93,565,062 | after FY end | Medium — first probe query needed | no query run yet, treat any first number as unverified |  | v2-Banned vendors still getting contracts |
| v2-266 |  |  |  |  |  | visual: other |
| v2-267 |  |  |  |  |  | visual: map |
| v2-268 |  |  |  |  |  | visual: other |
| v2-269 |  |  |  |  |  | NAICS is a code lookup. Not a catalog key; lookup or unproven. · visual: ranking |
| v2-270 |  |  |  |  |  | visual: ranking |
| v2-271 |  |  |  |  |  | UEI match 10 to 80 percent, sparse. · visual: other |
| v2-272 |  |  |  |  |  | visual: other |
| v2-273 |  |  |  |  |  | v1-15/v1-E49/v1-E66/v1-80 · visual: timeline |
| v2-274 |  |  |  |  |  | visual: other |
| v2-275 |  |  |  |  |  | NAME@ZIP is fuzzy. Multi-word names only. · visual: other |
| v1-123 | 15,001,221 | current | Medium — first probe query needed | no query run yet, treat any first number as unverified |  |  |
| v2-276 |  |  |  |  |  | EIN: 34 tables, 366 edges. · visual: other |
| v2-277 |  |  |  |  |  | Zip to county via XWALK_ZCTA_COUNTY where needed. · visual: map |
| v1-E65 | 21,090,245 | dated | Medium — partial run, needs finishing | false alarm |  |  |

## Corporate ownership — 10 questions

9 live, 1 needing a piece, 0 came back empty.

| ID | The question | Why it matters | Tables | Joins on | Status |
|---|---|---|---|---|---|
| v2-356 | **Offshore leaks network** — Who connects to whom across the Panama, Paradise and Pandora papers? | A graph with 3.3M edges. | one table | ICIJ node ID | never run |
| v2-357 | **Offshore jurisdictions ranked** — Which jurisdictions host the most leaked entities, by incorporation year? | BVI, Panama, Bahamas on a timeline. | one table | single table | never run |
| v2-358 | **Middlemen ranked** — Which law firms and agents set up the most offshore companies? | Names. | one table | single table | never run |
| v2-359 | **Addresses with hundreds of companies** — Which UK addresses host the most registered companies? | The duplicate-address trick, counted. | one table | stack, same shape | never run |
| v2-360 | **UK companies born and dying per day** — How many companies incorporate and dissolve each day? | A pulse chart. | one table | single table | never run |
| v2-361 | **Who controls UK companies, by nationality** — Which nationalities show up most as significant controllers? | 15.8M rows, partial load. | one table | single table | never run |
| v2-362 | **Irish companies by status** — How many Irish companies are active versus dissolved, by year? | 821K rows. | one table | single table | never run |
| v2-363 | **Owners per UK company against sector** — Which sectors have the most layered ownership? | Catalog item 54. | two tables | COMPANY_NO | never run |
| v2-364 | **Sanctioned names in UK filings** — Do sanctioned people appear as UK company controllers? | Name match across two lists. | two tables | name | never run |
| v1-90 | **Government officials who leave for the private sector, or vice versa** — Do agency contracts shift toward an official's old industry after they arrive? | The 'revolving door' question, with real contract dollars | two tables |  | needs a piece |

**Working notes — 10 of these 10 carry them**

| ID | Size | Years | Effort | Watch out | Needs | Notes, matches, results |
|---|---|---|---|---|---|---|
| v2-356 |  |  |  |  |  | Same-source ID, not a catalog key. · visual: other |
| v2-357 |  |  |  |  |  | visual: timeline |
| v2-358 |  |  |  |  |  | visual: ranking |
| v2-359 |  |  |  |  |  | Several tables shown side by side, no join. If a join is wanted, it is not in the catalog. · visual: ranking |
| v2-360 |  |  |  |  |  | visual: timeline |
| v2-361 |  |  |  |  |  | Truncated load; counts are floors. · visual: ranking |
| v2-362 |  |  |  |  |  | visual: timeline |
| v2-363 |  |  |  |  |  | visual: other |
| v2-364 |  |  |  |  |  | Not a catalog key. · v1-122 · visual: other |
| v1-90 | 93,153,830 | no dates landed | Medium — first probe query needed | GOVERNANCE__FED_REVOLVINGDOOR_PROJECT is job slots, not people | LDA covered_position is the real source. crawl RESTARTED 2026-09-07; it had stopped with 2011 alone. GOVERNANCE__FED_REVOLVINGDOOR_PROJECT is job slots, not people | reports/politics_probe_2026-09-05/90_appointee_sector_awards |

## Housing and lending — 24 questions

22 live, 0 needing a piece, 2 came back empty.

| ID | The question | Why it matters | Tables | Joins on | Status |
|---|---|---|---|---|---|
| v1-5 | **Homeowners after disasters, and their mortgage lenders** — Do people get worse loan terms right after a hurricane or flood? | Would show lenders profiting off disaster victims | two tables |  | started, unfinished |
| v2-307 | **Mortgage denial rate by race and county** — Where were applicants of one race denied far more than another, 2015 to 2017? | 45M applications, one honest map. | one table | single table | never run |
| v2-308 | **Home prices by metro since 1975** — Which metros' prices rose most, and where did they fall? | The line everyone has an opinion on. | one table | single table | never run |
| v2-309 | **Redlining maps** — What did the 1930s maps say about each neighborhood, in their own words? | The original descriptions are the wow. | one table | single table | never run |
| v2-310 | **Subsidized housing tenants** — Who lives in HUD housing, by income, age, disability, race, per project? | One map with demographics on hover. | one table | single table | never run |
| v2-311 | **Section 8 rent against market rent** — Where does Section 8 pay above or below local fair-market rent? | The gap column is built in. | one table | single table | never run |
| v2-312 | **Affordability restrictions expiring** — How many rural subsidized units lose their restrictions each coming year? | A cliff on a timeline. | one table | single table | never run |
| v2-313 | **FHA lenders ranked** — Which lenders write the most FHA loans, at what rates? | Lender names. | one table | single table | never run |
| v2-314 | **Twenty-five years of FHA apartment deals** — Which lenders and projects got the biggest multifamily commitments? | 2001 to 2026. | one table | single table | never run |
| v2-315 | **Flood insurance map** — Which communities are in the flood program, and how old are their maps? | Map age is a risk signal. | one table | single table | never run |
| v2-316 | **Disaster housing aid by disaster** — Which disasters produced the most registrations and aid dollars? | Partial load; shape only. | one table | single table | never run |
| v2-317 | **Public housing authorities** — Which authorities run the most units, and how full are they? | 3,787 authorities. | one table | single table | never run |
| v1-100 | **Companies that win disaster relief contracts** — Did they spring up right after the disaster was declared? | Would show opportunists forming shell companies to grab relief money | two tables |  | never run |
| v1-127 | **Bank branches in historically redlined neighborhoods** — Are banks pulling branches out of those neighborhoods over time? | Would show ongoing banking abandonment of Black and Latino areas | two tables |  | never run |
| v1-130 | **Subsidized apartment buildings** — Are their affordability contracts expiring in fast-gentrifying areas? | Would show low-income housing about to disappear where it's needed most | two tables |  | never run |
| v1-131 | **Mortgage lenders using a government-backed loan program** — Do they charge higher rates in historically redlined neighborhoods? | Would extend the redlining story into today's lending | two tables |  | never run |
| v1-132 | **Neighborhoods hit by disasters** — Do bankruptcy filings spike in the year after? | Would show disasters pushing families into financial collapse | two tables |  | never run |
| v1-96 | **Communities that opted out of flood insurance** — Do they still get disaster payouts for flood damage? | Would show a gap in the insurance system | two tables |  | never run |
| v1-97 | **Neighborhoods hit by disaster three or more times** — Are they being rebuilt each time instead of relocated? | Would question the wisdom of repeatedly rebuilding in harm's way | two tables |  | never run |
| v2-318 | **Redlined then, denied now** — Do 1930s D-graded neighborhoods still see higher denial rates? | The chart that writes its own headline. | two tables | geometry / tract | never run |
| v2-319 | **Lenders across the ID change** — Which lenders kept lending through the 2017 to 2018 ID switch? | Crosswalk exists for this. | two tables | lender ID / LEI | never run |
| v2-320 | **Home prices against disaster aid** — Did counties with big FEMA aid see prices fall after? | Catalog item 40 family. | two tables | FIPS | never run |
| v1-3 | **Banks and polluting factories** — Do banks that lend money also own the polluting sites? | Would show banks quietly bankrolling pollution | two tables |  | came back empty |
| v1-E72 | **Subsidized housing in disaster-prone counties** — Is it sitting empty more than in safer counties? | Would show risk concentrated on poor renters | two tables |  | came back empty |

**Working notes — 24 of these 24 carry them**

| ID | Size | Years | Effort | Watch out | Needs | Notes, matches, results |
|---|---|---|---|---|---|---|
| v1-5 | 71,243,587 | 2015-2017 | Quick — re-run and check the number | 47 disasters checked, more digging needed |  |  |
| v2-307 |  |  |  |  |  | Every outcome, not just approvals. · visual: map |
| v2-308 |  |  |  |  |  | visual: timeline |
| v2-309 |  |  |  |  |  | Full text and map shape. · visual: map |
| v2-310 |  |  |  |  |  | Negative values mean suppressed. · visual: map |
| v2-311 |  |  |  |  |  | visual: map |
| v2-312 |  |  |  |  |  | visual: timeline |
| v2-313 |  |  |  |  |  | visual: ranking |
| v2-314 |  |  |  |  |  | visual: timeline |
| v2-315 |  |  |  |  |  | v1-101/v1-96 · visual: map |
| v2-316 |  |  |  |  |  | About 12 percent loaded, cut mid-load. Not a sample. · visual: ranking |
| v2-317 |  |  |  |  |  | visual: map |
| v1-100 | 119,404,344 | 60-day window | Medium — first probe query needed | no query run yet, treat any first number as unverified |  |  |
| v1-127 | 2,824,132 | survey years | Medium — first probe query needed | no query run yet, treat any first number as unverified |  | v2-Bank deserts |
| v1-130 | 209,116 | 2026-28 | Medium — first probe query needed | no query run yet, treat any first number as unverified |  |  |
| v1-131 | 45,055,469 | one month | Medium — first probe query needed | no query run yet, treat any first number as unverified |  | v2-Redlined then, denied now |
| v1-132 | 33,216,361 | 12 months after | Medium — first probe query needed | no query run yet, treat any first number as unverified |  |  |
| v1-96 | 26,276,045 | per disaster | Medium — first probe query needed | no query run yet, treat any first number as unverified |  | v2-Flood insurance map |
| v1-97 | 26,300,071 | 2015+ | Medium — first probe query needed | no query run yet, treat any first number as unverified |  |  |
| v2-318 |  |  |  |  |  | Spatial join, not a catalog key. Needs proving. · v1-22/v1-131 · visual: map |
| v2-319 |  |  |  |  |  | Not a catalog key; lookup or unproven. · visual: other |
| v2-320 |  |  |  |  |  | visual: timeline |
| v1-3 | 5,305,548 | 2017 HMDA | Skip — already ruled out | it only found the banks' own buildings, not loans |  |  |
| v1-E72 | 26,286,521 | snapshot | Medium — partial run, needs finishing | No pattern, and much of it turned out to be Puerto Rico |  |  |

## Workers and workplaces — 12 questions

12 live, 0 needing a piece, 0 came back empty.

| ID | The question | Why it matters | Tables | Joins on | Status |
|---|---|---|---|---|---|
| v2-339 | **Mine accident narratives** — What do the accident narratives say, by injury type and mine? | Text people will read. | one table | single table | never run |
| v2-340 | **Mine fines proposed versus paid** — Which operators pay the smallest share of proposed penalties? | Two columns, one gap. | one table | single table | never run |
| v2-341 | **Mines open and closed** — Where are active mines, and where did they close? | Status on a map. | one table | single table | never run |
| v2-342 | **Injury rate by establishment, three years** — Which employers' injury rates rose across 2023 to 2025? | Three yearly tables, one slope. | one table | EIN | never run |
| v2-343 | **Injury narratives** — What happened, in the worker's words, by industry? | Case detail text. | one table | stack, same shape | never run |
| v2-344 | **Union membership since 2000** — Which unions grew and which shrank, by members and assets? | 617K filings. | one table | single table | never run |
| v2-345 | **Pension funding gaps** — Which single-employer plans are furthest below their funding target? | Actuarial filings. | one table | single table | never run |
| v1-115 | **Mining companies with big unpaid safety fines** — Do accidents happen at their mines afterward? | Would connect ignoring fines to real harm | two tables |  | never run |
| v1-82 | **Local labor unions** — Do unions reporting missing money also have an active political fund? | Would be a red flag on where union dues go | two tables |  | never run |
| v1-99 | **Mining companies** — Do the ones with unsafe dams also have a pile of unpaid safety fines? | Would show a company ignoring safety on two fronts | two tables |  | never run |
| v2-346 | **Violations against accidents per mine** — Do mines with more citations have more accidents? | Catalog item 36. | two tables | MSHA mine ID | never run |
| v2-347 | **Suspicious injury numbers, queued** — Which company groups look like they under-report injuries? | Built review queue. | two tables | EIN | never run |

**Working notes — 12 of these 12 carry them**

| ID | Size | Years | Effort | Watch out | Needs | Notes, matches, results |
|---|---|---|---|---|---|---|
| v2-339 |  |  |  |  |  | visual: other |
| v2-340 |  |  |  |  |  | 3.1M citations. · visual: ranking |
| v2-341 |  |  |  |  |  | visual: map |
| v2-342 |  |  |  |  |  | visual: timeline |
| v2-343 |  |  |  |  |  | Several tables shown side by side, no join. If a join is wanted, it is not in the catalog. · visual: other |
| v2-344 |  |  |  |  |  | visual: timeline |
| v2-345 |  |  |  |  |  | visual: ranking |
| v1-115 | 3,360,888 | before/after | Medium — first probe query needed | no query run yet, treat any first number as unverified |  | v2-Violations against accidents per mine |
| v1-82 | 677,741 | same fiscal year | Medium — first probe query needed | no query run yet, treat any first number as unverified |  | reports/politics_probe_2026-09-05/82_union_shortage_pac |
| v1-99 | 3,271,937 | current | Medium — first probe query needed | no query run yet, treat any first number as unverified |  | v2-Violations against accidents per mine |
| v2-346 |  |  |  |  |  | Catalog item 58: keys in keyset, zero edges. Not a catalog key; lookup or unproven. · v1-99/v1-115 · visual: other |
| v2-347 |  |  |  |  |  | REVIEW schema, internal. · visual: ranking |

## Immigration — 16 questions

16 live, 0 needing a piece, 0 came back empty.

| ID | The question | Why it matters | Tables | Joins on | Status |
|---|---|---|---|---|---|
| v1-144 | **Immigration court judges** — Do outcomes vary a lot by judge and detention facility? | Would show inconsistent justice depending who you get | one table |  | started, unfinished |
| v2-321 | **Immigration court by nationality and city** — Which nationalities fill which courts, and how long do cases take? | 12.6M cases. | one table | single table | never run |
| v2-322 | **Days in ICE detention** — How long do people stay, by facility and year, since 2004? | Length of stay as a distribution. | one table | single table | never run |
| v2-323 | **Bond amounts by facility** — Where are bonds set highest? | Dollar amounts per facility. | one table | single table | never run |
| v2-324 | **Detainer flags** — Which risk flags appear most on detainers, and how often none? | Dozens of yes-no columns counted. | one table | single table | never run |
| v2-325 | **Detention facilities map** — Where are ICE facilities, by type? | 1,490 codes, 163 on the published list. | one table | stack, same shape | never run |
| v2-326 | **H-1B sponsors and wages** — Which employers sponsor most, and what do they offer per job title? | Employer names and wages. | one table | single table | never run |
| v2-327 | **Immigration lawyers ranked** — Which attorneys file the most visa cases? | Attorney column exists. | one table | single table | never run |
| v2-328 | **Border encounters by nationality** — How did monthly encounters shift by nationality and outcome? | DHS stats as a stacked area. | one table | single table | never run |
| v2-329 | **USCIS backlog** — How many applications are pending per form type per quarter? | The queue, drawn. | one table | single table | never run |
| v2-330 | **Refugees by origin** — Which countries produced the most refugees per year? | OWID series. | one table | single table | never run |
| v1-116 | **Employers who sponsor immigrant work visas** — Do they pay the legal minimum wage and also rack up serious safety violations? | Would show a workforce being underpaid and put at risk | two tables |  | never run |
| v1-119 | **Companies running immigration detention centers** — How much do they get paid per day, per detained person? | Basic transparency on a government spending question | two tables |  | never run |
| v1-120 | **Counties with lots of ICE detainer requests** — Do they also have high jail populations generally? | Tests whether immigration enforcement tracks with broader incarceration | two tables |  | never run |
| v2-331 | **Stays by facility on a map** — Which facilities hold people longest, mapped? | Stint table meets facility coordinates. | two tables | facility code | never run |
| v2-332 | **Court outcome against custody** — Do detained respondents lose more often than released ones? | Custody status column in the case table. | two tables | anonymized person ID | never run |

**Working notes — 16 of these 16 carry them**

| ID | Size | Years | Effort | Watch out | Needs | Notes, matches, results |
|---|---|---|---|---|---|---|
| v1-144 | 12,631,225 | n/a | Medium — reload zip keeping every member | case file is now 39 typed columns (court, custody, case type, nationality, hearing date); still no judge, no outcome; ~100 rows shifted by a stray tab | B_TblProceeding from the FOIA zip for judge code and decision | v2-Court outcome against custody |
| v2-321 |  |  |  |  |  | visual: map |
| v2-322 |  |  |  |  |  | 2.6M stays. · visual: timeline |
| v2-323 |  |  |  |  |  | visual: ranking |
| v2-324 |  |  |  |  |  | visual: other |
| v2-325 |  |  |  |  |  | Gap between the two lists is itself a finding. · visual: map |
| v2-326 |  |  |  |  |  | visual: ranking |
| v2-327 |  |  |  |  |  | visual: ranking |
| v2-328 |  |  |  |  |  | visual: timeline |
| v2-329 |  |  |  |  |  | visual: timeline |
| v2-330 |  |  |  |  |  | visual: timeline |
| v1-116 | 6,029,356 | by year | Medium — first probe query needed | no query run yet, treat any first number as unverified |  |  |
| v1-119 | 95,726,889 | by year | Medium — first probe query needed | no query run yet, treat any first number as unverified |  |  |
| v1-120 | 738,276 | by year | Medium — first probe query needed | no query run yet, treat any first number as unverified |  |  |
| v2-331 |  |  |  |  |  | Same-source code, not a catalog key. · visual: map |
| v2-332 |  |  |  |  |  | Not a catalog key. Likely unjoinable. · v1-144 · visual: other |

## Contracts and procurement — 5 questions

4 live, 0 needing a piece, 1 came back empty.

| ID | The question | Why it matters | Tables | Joins on | Status |
|---|---|---|---|---|---|
| v1-15 | **Companies banned from federal contracts** — Are banned companies still getting paid on disaster relief contracts? | Would be straightforward government fraud | two tables |  | **found something** |
| v1-E49 | **Banned companies** — Did they win government contracts specifically during their ban? | A tighter, dated version of v1-15 | two tables |  | **found something** |
| v2-385 | **Who is banned from federal business** — Which agencies exclude most, for what reasons, and how many are active? | 168K exclusions. | one table | single table | never run |
| v2-386 | **Ecuador's contract winners** — Which bidders win most, and how concentrated is it? | Open-contracting data. | one table | single table | never run |
| v1-E66 | **Companies banned from federal work** — Are they still getting health grants? | A grant-side version of v1-15 | two tables |  | came back empty |

**Working notes — 5 of these 5 carry them**

| ID | Size | Years | Effort | Watch out | Needs | Notes, matches, results |
|---|---|---|---|---|---|---|
| v1-15 | 93,321,752 | untimed | Quick — re-run and check the number | 26 banned companies, $169 million in contracts |  | v2-Banned vendors still getting contracts · reports/tier1_deep_dive_2026-09-05/15_banned_disaster_contractors |
| v1-E49 | 93,321,752 | timed | Quick — re-run and check the number | Confirmed, but the dollar amount is small |  | v2-Banned vendors still getting contracts · reports/tier1_deep_dive_2026-09-05/E49_contracts_during_ban |
| v2-385 |  |  |  |  |  | visual: ranking |
| v2-386 |  |  |  |  |  | visual: ranking |
| v1-E66 | 20,071,207 | capped | Medium — partial run, needs finishing | None found so far |  | v2-Banned vendors still getting contracts |

## Transport and safety — 10 questions

10 live, 0 needing a piece, 0 came back empty.

| ID | The question | Why it matters | Tables | Joins on | Status |
|---|---|---|---|---|---|
| v2-348 | **Who owns the planes** — Which owners hold the most registered aircraft, by state? | 315K tail numbers. | one table | single table | never run |
| v2-349 | **Rail deaths since 1975** — How did worker, passenger and trespasser deaths move over fifty years? | Three lines, one long axis. | one table | stack, same shape | never run |
| v2-350 | **Crossings with no warning** — Where do trains hit cars at crossings with no signals? | Map with a filter. | one table | single table | never run |
| v2-351 | **Derailments by cause** — What causes derailments, and which railroads have most per mile? | Cause codes as bars. | one table | single table | never run |
| v2-352 | **Plane crashes map** — Where do crashes happen, and in what weather? | 31K events. | one table | single table | never run |
| v2-353 | **Crashes by aircraft make** — Which makes and models crash most, per registered aircraft? | Needs the registry for the denominator. | one table | tail number | never run |
| v2-354 | **Ship tracks** — What do 58M position pings look like on a coast? | The wow map. | one table | single table | never run |
| v1-104 | **Small aircraft owned by shell companies** — Do the same addresses show up behind multiple fatal crashes? | Would show unsafe operators hiding behind shell companies | two tables |  | never run |
| v1-105 | **Railroad crossings** — Do the same crossings get hit by trains again and again? | Would show known danger spots never getting fixed | two tables |  | never run |
| v2-355 | **Ships per owner against port calls** — Which owners run the most vessels, and where do they call? | Catalog item 60. | two tables | IMO / MMSI | never run |

**Working notes — 10 of these 10 carry them**

| ID | Size | Years | Effort | Watch out | Needs | Notes, matches, results |
|---|---|---|---|---|---|---|
| v2-348 |  |  |  |  |  | visual: map |
| v2-349 |  |  |  |  |  | Several tables shown side by side, no join. If a join is wanted, it is not in the catalog. · visual: timeline |
| v2-350 |  |  |  |  |  | v1-105 · visual: map |
| v2-351 |  |  |  |  |  | visual: ranking |
| v2-352 |  |  |  |  |  | visual: map |
| v2-353 |  |  |  |  |  | Not a catalog key. · visual: ranking |
| v2-354 |  |  |  |  |  | MARITIME schema. · visual: map |
| v1-104 | 377,918 | by event | Medium — first probe query needed | no query run yet, treat any first number as unverified |  |  |
| v1-105 | 1,401,937 | 2010+ | Medium — first probe query needed | no query run yet, treat any first number as unverified |  | v2-Crossings with no warning |
| v2-355 |  |  |  |  |  | 2 tables, zero edges. Sanctioned ships on AIS is the story. · v1-137 · visual: other |

## Consumer safety — 7 questions

7 live, 0 needing a piece, 0 came back empty.

| ID | The question | Why it matters | Tables | Joins on | Status |
|---|---|---|---|---|---|
| v2-376 | **What sends kids to the ER** — Which products injure which age groups most? | 9.8M ER visits. | one table | code | never run |
| v2-377 | **Car complaints by model** — Which make-model-years draw the most complaints, and about what? | 2.2M complaints. | one table | single table | never run |
| v2-378 | **Investigation to recall lag** — How long from investigation opening to recall, by maker? | Time as the story. | one table | single table | never run |
| v2-379 | **Biggest recalls** — Which recalls affected the most vehicles? | Ranking. | one table | single table | never run |
| v2-380 | **Complaints about financial companies** — Which companies draw the most CFPB complaints per product, and how do they respond? | 17M complaints. | one table | single table | never run |
| v1-129 | **Car makes and models** — Do complaints pile up for years before an official recall happens? | Would show manufacturers slow-walking known safety issues | two tables |  | never run |
| v2-381 | **Complaints before recalls** — Did complaints spike before the recall for the same model? | Two NHTSA tables on make-model-year. | two tables | make + model + year | never run |

**Working notes — 7 of these 7 carry them**

| ID | Size | Years | Effort | Watch out | Needs | Notes, matches, results |
|---|---|---|---|---|---|---|
| v2-376 |  |  |  |  |  | Decoder table is misfiled under EDUCATION. Not a catalog key; lookup or unproven. · visual: ranking |
| v2-377 |  |  |  |  |  | visual: ranking |
| v2-378 |  |  |  |  |  | visual: timeline |
| v2-379 |  |  |  |  |  | visual: ranking |
| v2-380 |  |  |  |  |  | visual: ranking |
| v1-129 | 2,469,802 | lag years | Medium — first probe query needed | no query run yet, treat any first number as unverified |  | v2-Complaints before recalls |
| v2-381 |  |  |  |  |  | Not a catalog key. · v1-129 · visual: timeline |

## Consumer protection — 1 questions

1 live, 0 needing a piece, 0 came back empty.

| ID | The question | Why it matters | Tables | Joins on | Status |
|---|---|---|---|---|---|
| v1-126 | **Mortgage lenders** — Do consumer complaints about them pile up before regulators catch on? | Would show early warning signs being ignored | two tables |  | never run |

**Working notes — 1 of these 1 carry them**

| ID | Size | Years | Effort | Watch out | Needs | Notes, matches, results |
|---|---|---|---|---|---|---|
| v1-126 | 17,173,686 | monthly | Skip — already ruled out | no query run yet, treat any first number as unverified |  |  |

## Science and research — 9 questions

9 live, 0 needing a piece, 0 came back empty.

| ID | The question | Why it matters | Tables | Joins on | Status |
|---|---|---|---|---|---|
| v2-368 | **Earthquakes since records** — Where and how deep, magnitude 2.5 and up? | 443K quakes, one map. | one table | single table | never run |
| v2-369 | **NIH money by institution, 27 years** — Which institutions and states won the most NIH funding, year by year? | 2.1M applications. | one table | single table | never run |
| v2-370 | **Review panels that fund most** — Which study sections score the most funded applications? | Inside baseball, but visible. | one table | single table | never run |
| v2-371 | **SBIR repeat winners** — Which companies win SBIR awards year after year? | The mills. | one table | single table | never run |
| v2-372 | **Why papers get retracted** — Which reasons, journals, and countries dominate retractions by year? | 71K retractions. | one table | stack, same shape | never run |
| v2-373 | **Preprints that got published** — What share of preprints made it to a journal, and how fast? | 432 rows. | one table | single table | never run |
| v2-374 | **Retractions per institution** — Which research organizations have the most retracted papers? | Retraction list meets the org registry. | two tables | institution name | never run |
| v2-375 | **NIH grants against retractions** — Do the most-funded institutions also retract most? | Money and mistakes. | two tables | institution name | never run |
| v1-112 | **Universities and small research companies with big federal grants** — Do the ones with more retracted (fake or flawed) studies keep getting funded? | Would question the return on public research money | two tables |  | never run |

**Working notes — 9 of these 9 carry them**

| ID | Size | Years | Effort | Watch out | Needs | Notes, matches, results |
|---|---|---|---|---|---|---|
| v2-368 |  |  |  |  |  | visual: map |
| v2-369 |  |  |  |  |  | visual: timeline |
| v2-370 |  |  |  |  |  | visual: ranking |
| v2-371 |  |  |  |  |  | visual: ranking |
| v2-372 |  |  |  |  |  | Two overlapping copies. · visual: timeline |
| v2-373 |  |  |  |  |  | visual: other |
| v2-374 |  |  |  |  |  | Name match, not a catalog key. · visual: ranking |
| v2-375 |  |  |  |  |  | Name match. Not a catalog key; lookup or unproven. · v1-112 · visual: other |
| v1-112 | 2,413,705 | by year | Medium — first probe query needed | no query run yet, treat any first number as unverified |  | v2-NIH grants against retractions |

## Education — 7 questions

6 live, 1 needing a piece, 0 came back empty.

| ID | The question | Why it matters | Tables | Joins on | Status |
|---|---|---|---|---|---|
| v2-333 | **Debt against earnings by college** — Which colleges leave graduates with the most debt per dollar earned? | One dot per school. | one table | single table | never run |
| v2-334 | **Admission rate against tuition** — Are the most selective schools the most expensive? | Another scatter from the same table. | one table | single table | never run |
| v2-335 | **The yield curve, every day** — When did short rates go above long rates? | Inversions as shaded bands. | one table | single table | never run |
| v2-336 | **Commodity speculators versus hedgers** — How did speculator share move in each commodity market? | Weekly, per market. | one table | single table | never run |
| v2-337 | **Political ad spend by region** — Which regions got the most political ad money? | Google's own totals. | one table | stack, same shape | never run |
| v2-338 | **Lobbying issues over time** — Which issue codes got lobbied most each quarter? | 820K filings. | one table | single table | never run |
| v1-83 | **Health care industry lobbyists** — Does lobbying spending spike right before a new safety rule is finalized? | Would show industry trying to weaken rules before they lock in | two tables |  | needs a piece |

**Working notes — 7 of these 7 carry them**

| ID | Size | Years | Effort | Watch out | Needs | Notes, matches, results |
|---|---|---|---|---|---|---|
| v2-333 |  |  |  |  |  | visual: other |
| v2-334 |  |  |  |  |  | visual: other |
| v2-335 |  |  |  |  |  | Misfiled under EDUCATION. · visual: timeline |
| v2-336 |  |  |  |  |  | Misfiled under EDUCATION. · visual: timeline |
| v2-337 |  |  |  |  |  | Misfiled. · visual: map |
| v2-338 |  |  |  |  |  | Misfiled. · visual: timeline |
| v1-83 | 914,380 | comment windows | Medium — first probe query needed | no query run yet, treat any first number as unverified | LDA crawl RESTARTED 2026-09-07 after stopping at 2011. positions table holds 2011 only, 376,948 rows, one year of 1999-2026. blocked until it finishes | reports/politics_probe_2026-09-05/83_lobby_surge_cms_rules |

## History — 3 questions

3 live, 0 needing a piece, 0 came back empty.

| ID | The question | Why it matters | Tables | Joins on | Status |
|---|---|---|---|---|---|
| v2-382 | **Slave voyages, port to port** — Which ports sent and received the most voyages, and how many died at sea? | A flow map across an ocean. | one table | stack, same shape | never run |
| v2-383 | **Voyages per year** — How did voyage counts and survival rates change across three centuries? | One long timeline. | one table | single table | never run |
| v2-384 | **WPA narratives** — What subjects did formerly enslaved people talk about, by state? | 100 full transcripts. | one table | single table | never run |

**Working notes — 3 of these 3 carry them**

| ID | Size | Years | Effort | Watch out | Needs | Notes, matches, results |
|---|---|---|---|---|---|---|
| v2-382 |  |  |  |  |  | Column names are research codes. · visual: flow |
| v2-383 |  |  |  |  |  | visual: timeline |
| v2-384 |  |  |  |  |  | visual: other |

## Open data portals — 3 questions

3 live, 0 needing a piece, 0 came back empty.

| ID | The question | Why it matters | Tables | Joins on | Status |
|---|---|---|---|---|---|
| v2-365 | **France's most downloaded datasets** — Which datasets do people actually use, and how good are they? | View counts and quality score. | one table | single table | never run |
| v2-366 | **Open-data catalogs compared** — How big and how tagged are ten countries' catalogs? | One bar chart of samples. | one table | stack, same shape | never run |
| v2-367 | **DOJ Epstein pages over time** — Which DOJ pages changed, appeared, or vanished, and when? | 1.5M snapshots as a change timeline. | one table | URL | never run |

**Working notes — 3 of these 3 carry them**

| ID | Size | Years | Effort | Watch out | Needs | Notes, matches, results |
|---|---|---|---|---|---|---|
| v2-365 |  |  |  |  |  | Do not join on GEO_IN; catalog trap. · visual: ranking |
| v2-366 |  |  |  |  |  | Most are samples. · visual: ranking |
| v2-367 |  |  |  |  |  | EPSTEIN and INVESTIGATIONS schemas hold the siblings. Not a catalog key; lookup or unproven. · visual: timeline |

## Timeline — 3 questions

3 live, 0 needing a piece, 0 came back empty.

| ID | The question | Why it matters | Tables | Joins on | Status |
|---|---|---|---|---|---|
| v2-278 | **What years the warehouse actually covers** — Which subjects have data for which years, and where are the holes? | A heatmap of the shelf itself. | one table | date | never run |
| v2-279 | **Which tables have a usable date** — How many tables carry a date, at what granularity? | The registry is a shape chart. | one table | single table | never run |
| v2-280 | **Everything that happened on one day** — For a chosen date: every record across subjects, on one strip? | The warehouse as a newspaper. | a chain | date | never run |

**Working notes — 3 of these 3 carry them**

| ID | Size | Years | Effort | Watch out | Needs | Notes, matches, results |
|---|---|---|---|---|---|---|
| v2-278 |  |  |  |  |  | Same date axis. Meta chart, not source data. Not a catalog key; lookup or unproven. · visual: other |
| v2-279 |  |  |  |  |  | Internal bookkeeping. · visual: other |
| v2-280 |  |  |  |  |  | Not a catalog key; lookup or unproven. · visual: timeline |

## Reference and lookup — 9 questions

9 live, 0 needing a piece, 0 came back empty.

| ID | The question | Why it matters | Tables | Joins on | Status |
|---|---|---|---|---|---|
| v2-281 | **The tree of life** — How do 993K species entries nest from kingdom down? | A sunburst of everything named. | one table | stack, same shape | never run |
| v2-282 | **Common names in many languages** — Which species have the most common names, in which languages? | Names are stories. | one table | single table | never run |
| v2-283 | **Native or introduced, by state** — Which states have the most introduced species listed? | A map of invaders. | one table | single table | never run |
| v2-284 | **Rejected species names** — How many old names point to each accepted one? | Science changing its mind, counted. | one table | single table | never run |
| v2-285 | **Place names of America** — Which names repeat most across the country, and where? | 1.2M names, one search box. | one table | single table | never run |
| v2-286 | **Global news events, toned** — Which country pairs generate the most news events, and how negative? | A GDELT sample. | one table | single table | never run |
| v2-287 | **Research organizations of the world** — Where are the universities and labs, by type? | 135K orgs on a map. | one table | single table | never run |
| v2-288 | **Fertility by country** — Which countries fell below replacement and when? | A world map crossing a line. | one table | single table | never run |
| v2-289 | **County shapes and water** — Which counties are mostly water? | A geometry oddity chart. | one table | single table | never run |

**Working notes — 9 of these 9 carry them**

| ID | Size | Years | Effort | Watch out | Needs | Notes, matches, results |
|---|---|---|---|---|---|---|
| v2-281 |  |  |  |  |  | Several tables shown side by side, no join. If a join is wanted, it is not in the catalog. · visual: other |
| v2-282 |  |  |  |  |  | visual: ranking |
| v2-283 |  |  |  |  |  | visual: map |
| v2-284 |  |  |  |  |  | visual: ranking |
| v2-285 |  |  |  |  |  | Historical and variant names included. · visual: map |
| v2-286 |  |  |  |  |  | 1,015 rows only. · visual: other |
| v2-287 |  |  |  |  |  | visual: map |
| v2-288 |  |  |  |  |  | visual: timeline |
| v2-289 |  |  |  |  |  | visual: map |

## Other — 6 questions

6 live, 0 needing a piece, 0 came back empty.

| ID | The question | Why it matters | Tables | Joins on | Status |
|---|---|---|---|---|---|
| v2-387 | **Multistate settlements** — Which industries paid the most in multistate settlements, led by which states? | 882 cases. | one table | single table | never run |
| v2-388 | **Tribal land map** — Where are tribal land areas and how big? | 335 shapes. | one table | single table | never run |
| v2-389 | **Russian operations in Europe** — Where, when, and against what kind of target? | 150 rows. | one table | single table | never run |
| v2-390 | **Warehouse table sizes** — How big is each table, and which subjects hold the rows? | A treemap of the shelf. | one table | none | never run |
| v2-391 | **One county, every table** — For one FIPS: jobs, overdoses, jail, facilities, storms, aid, providers, water? | The county card. | a chain | FIPS | never run |
| v2-392 | **One country, every table** — For one country: freedom, corruption, CO2, life expectancy, debt, conflict, sanctions, aid? | The country card. | a chain | country code | never run |

**Working notes — 6 of these 6 carry them**

| ID | Size | Years | Effort | Watch out | Needs | Notes, matches, results |
|---|---|---|---|---|---|---|
| v2-387 |  |  |  |  |  | visual: ranking |
| v2-388 |  |  |  |  |  | visual: map |
| v2-389 |  |  |  |  |  | visual: map |
| v2-390 |  |  |  |  |  | Meta. Source is the inventory file, not a table. · visual: other |
| v2-391 |  |  |  |  |  | FIPS: 15 tables, 78 edges. Catalog item 61 for population. · visual: other |
| v2-392 |  |  |  |  |  | Country code is a lookup, not a catalog key. · visual: other |
---

## The 25 cross-join builds

Three-way collisions between schemas that have no business relation.
These sit outside the 542 — none of them appear in the docket above.
Each names its sides, its key, how strong that key is, and what a hit
or a miss would mean.

### 1 · The charity hospital that pays like a bank

**Do the nonprofit hospitals with the highest executive pay give the least charity care?**

- Side A: HEALTH__HOSPITAL_OFFICER_PAY - named officer, title, hours, total pay, from the 990
- Side B: HEALTH__FED_CMS_HCRIS - charity care dollars, margin, assets, per fiscal year
- Side C: HEALTH__FED_CMS_HOSPITAL_COMPARE - star rating
- Joins on: EIN for the 990 side, CCN for the Medicare side
- Key strength: EIN steel 86-100%; the EIN-to-CCN hop is the risk
- Hit: A hospital paying a CEO millions while writing off almost nothing is on the record, by name
- Miss: Pay tracks size, not stinginess, and the nonprofit label survives
- Visual: scatter, pay per hour against charity care share, one dot per hospital
- Why it's a story: Two filings that never meet: the tax form says what he earns, the Medicare report says what she gave away

### 2 · Paid by the sponsor, running the trial

**Are the doctors running a drug trial on the sponsor's payroll while they run it?**

- Side A: HEALTH__FED_CLINICALTRIALS - sponsor, phase, condition, sites, investigator
- Side B: HEALTH__FED_CMS_OPEN_PAYMENTS - which company paid which doctor, how much, what for
- Side C: HEALTH__FED_CMS_NPPES - name to NPI so the investigator resolves
- Joins on: NPI once the investigator name resolves
- Key strength: NPI steel 100%; investigator name to NPI is the weak hop
- Hit: The person testing the drug was being paid by its maker in the same year
- Miss: Investigators are paid after, not during, and the timing defence holds
- Visual: timeline per trial, payment bars under the trial bar, one row per investigator
- Why it's a story: FDA registry and CMS payments are two agencies with no reason to talk

### 3 · Who drinks from the failing pipe

**Which nursing homes, clinics and subsidised buildings sit inside a water system that keeps failing?**

- Side A: ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT - health-based violations per system
- Side B: ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS - the zips and cities each system serves
- Side C: HEALTH__FED_CMS_NURSING_HOME / HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES / HOUSING__FED_HUD_ASSISTED_HOUSING_PROJECTS
- Joins on: PWSID then ZIP
- Key strength: PWSID steel, 45 edges; zip to facility is a plain lookup
- Hit: A named nursing home is inside a system with a decade of health violations
- Miss: Violating systems serve mostly empty land and nobody vulnerable drinks it
- Visual: map, water systems shaded by violations, vulnerable buildings as dots on top
- Why it's a story: EPA tracks the pipe, CMS and HUD track the people, nobody joins them

### 4 · The government's worst supplier

**Does the federal government keep buying from the companies that injure workers and pollute most?**

- Side A: ECONOMICS__FED_USASPENDING_CONTRACTS - who won, which agency, how much
- Side B: LABOR__FED_OSHA_ITA_300A_SUMMARY_2024 - injuries and deaths per establishment
- Side C: ENVIRONMENT__FED_EPA_ECHO - inspections, violations, penalties / PROCUREMENT__FED_SAM_EXCLUSIONS
- Joins on: UEI on the contract side, EIN on the injury side
- Key strength: UEI 10-80% sparse; UEI-EIN cross is 2-16%, so this is a sample not a rate
- Hit: A named vendor is in the worst tenth on injuries and still holds nine-figure contracts
- Miss: The overlap is a handful of firms and the procurement system looks clean
- Visual: three-column ranking, contract dollars, injury rate, penalty total, sorted by dollars
- Why it's a story: Procurement, labour and environment are three agencies that never compare notes

### 5 · The judge who owned the company

**Did any judge hold stock in a company that was a party in their own courtroom?**

- Side A: JUSTICE__FED_COURTLISTENER_INVESTMENTS - holding, description, value, transaction
- Side B: JUSTICE__FED_FJC_IDB_CIVIL - the parties in every district civil case
- Side C: JUSTICE__FED_COURTLISTENER_POSITIONS - which judge sat on which court, when
- Joins on: CL_PERSON_ID for the judge; company name match for the litigant
- Key strength: CL_PERSON_ID steel; the name match to a litigant is the whole risk
- Hit: A judge, a case, a holding, and overlapping dates, all on the record
- Miss: Recusal worked, and the absence is itself the finding
- Visual: three-column strip per judge, holdings, cases, dates, overlap highlighted
- Why it's a story: The disclosure form and the docket are both public and were never laid on top of each other

### 6 · Offshore names on the donor list

**Do people named in the offshore leaks also show up as US political donors or licensed doctors?**

- Side A: CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_OFFICERS - officers, directors, shareholders
- Side B: FINANCE__FED_FEC_INDIV_CONTRIBUTIONS - donor name, city, employer, occupation
- Side C: HEALTH__FED_CMS_NPPES - the provider registry, for the doctor half
- Joins on: NAME@ZIP
- Key strength: fuzzy, 8% single-word real; multi-word names only, show as a sample
- Hit: A name that appears in a Panama-era leak also appears giving to a campaign
- Miss: Common names swamp it and the honest answer is the method does not resolve people
- Visual: three-column list, leak entity, donation, licence, with a confidence badge per row
- Why it's a story: A journalism leak, a campaign filing and a medical registry have never shared a key

### 7 · Cosponsors who share a wallet

**Do the members who cosponsor bills together also draw on the same donors?**

- Side A: POLITICS__FED_GOVINFO_BILL_COSPONSORS - who signed on to what, when
- Side B: POLITICS__MEMBER_PAC_MONEY - PAC money and outside spending per member
- Side C: POLITICS__FED_VOTEVIEW_MEMBERS - ideology score / POLITICS__MEMBER_SPINE
- Joins on: BIOGUIDE
- Key strength: proven family, 47 in the catalog
- Hit: Two members far apart on ideology cosponsor constantly and share funders
- Miss: Cosponsorship tracks party and the money adds nothing new
- Visual: network graph, members as nodes, cosponsorship as edges, node colour by shared funders
- Why it's a story: The bill feed and the money feed are both famous and rarely overlaid as one graph

### 8 · The county that got the pills and the cells

**Did the counties flooded with opioids years ago end up with the jails, not the treatment?**

- Side A: HEALTH__FED_DEA_ARCOS - every controlled shipment, buyer, dose
- Side B: JUSTICE__XC_VERA_INCARCERATION_TRENDS - jail and prison population by race, by year
- Side C: HEALTH__FED_CDC_DRUG_POISONING_COUNTY / DIM_COUNTY for population
- Joins on: FIPS
- Key strength: county family, 73-100%, 78 edges
- Hit: Pill volume in 2010 predicts jail rate in 2020 better than it predicts treatment capacity
- Miss: Both track poverty and the pill number adds nothing on top
- Visual: animated map, three layers, pills then deaths then jail, twenty years
- Why it's a story: DEA, CDC and a nonprofit prison dataset on one county code

### 9 · Downstream of a dam nobody fixed

**Which nursing homes and subsidised buildings sit below a dam rated poor with a high hazard?**

- Side A: ENVIRONMENT__FED_NID_DAMS - hazard if it fails, condition, last inspection, capacity
- Side B: HEALTH__FED_CMS_NURSING_HOME - every certified home, address, residents
- Side C: HOUSING__FED_HUD_ASSISTED_HOUSING_PROJECTS - subsidised buildings and their tenants
- Joins on: coordinates, spatial
- Key strength: not a catalog key; a distance join that has to be built and proven
- Hit: A named home full of people who cannot walk sits below a poor-rated dam
- Miss: Nothing vulnerable is downstream and the inspection backlog is a paperwork story
- Visual: map with dam as a source and a shaded downstream cone, facilities as dots
- Why it's a story: Army Corps, CMS and HUD, three agencies, one physical fact

### 10 · The parent company x-ray

**For one global parent: every subsidiary, every polluting site, every share of stock?**

- Side A: ECONOMICS__INTL_GLEIF_RELATIONSHIPS - parent and subsidiary, with dates
- Side B: ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK - facility to corporate owner, with confidence
- Side C: FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE - the ticker, for the listed ones
- Joins on: LEI then FRS_ID then CIK
- Key strength: LEI steel 3.2M matched; the LEI-to-CIK hop is the thin one
- Hit: One ticker resolves to hundreds of sites and a violation record nobody aggregates
- Miss: Ownership data is too sparse to roll up and the tree collapses
- Visual: tree, parent at the root, subsidiaries as branches, facilities as leaves sized by penalty
- Why it's a story: A global ID registry, an EPA crosswalk and a stock ticker on one page

### 11 · Ransomware, then the care

**When a hospital is hit by ransomware, do its quality scores drop afterwards?**

- Side A: JUSTICE__XC_RANSOMWARELIVE_VICTIMS - claimed victim, gang, website, date
- Side B: HEALTH__FED_CMS_HOSPITAL_COMPARE - star rating, mortality, safety, readmission
- Side C: HEALTH__FED_CMS_HCRIS - the finances, before and after
- Joins on: hospital name match to CCN
- Key strength: name match, not a catalog key; the resolve is the work
- Hit: Measured mortality or safety worsens in the reporting period after the attack
- Miss: Scores are too lagged and coarse to see it, which is its own point about the measures
- Visual: before-and-after slope per hospital, attack date as the dividing line
- Why it's a story: A ransomware leak-site scrape and a CMS quality file have never met

### 12 · The lobbyist who used to write the rules

**Do former government staff lobby the agency they left, and does their client's money follow?**

- Side A: POLITICS__FED_SENATE_LDA_LOBBYIST_POSITIONS - the covered government job they held
- Side B: EDUCATION__FED_SENATE_LDA_FILINGS - client, spend, issue, agency lobbied
- Side C: ECONOMICS__FED_USASPENDING_CONTRACTS - what that client won from that agency
- Joins on: filing ID then client name to UEI
- Key strength: same-source ID is clean; client to vendor is a name match
- Hit: A named person left an agency and lobbied it for a client that then won its contracts
- Miss: Prior-position flags are too vague to place a person at a specific agency
- Visual: three-stage flow, person to agency to client to dollars
- Why it's a story: Two lobbying tables and a spending table, one story, three filings

### 13 · Banned, and still on the payroll

**Are drug companies still paying doctors who are banned from Medicare or who opted out?**

- Side A: HEALTH__FED_HHS_OIG_LEIE - banned, why, when, reinstated or not
- Side B: HEALTH__FED_CMS_OPEN_PAYMENTS - payments by company, by date
- Side C: HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS - the doctors who walked away from Medicare
- Joins on: NPI
- Key strength: steel, 100%, 364 edges; this one is fully proven
- Hit: Payments land after the exclusion date, dated and named
- Miss: Payments all predate the ban and the system worked
- Visual: timeline per doctor, ban date as a vertical line, payment dots either side
- Why it's a story: An enforcement list and a transparency database, same key, opposite purposes

### 14 · The drug price spike and the prescriber's bill

**When a generic drug's benchmark price jumps, whose prescribing cost jumps with it?**

- Side A: HEALTH__FED_CMS_NADAC - benchmark price per unit, by effective date
- Side B: HEALTH__FED_CMS_PARTD_PRESCRIBERS - claims and cost per doctor per drug
- Side C: HEALTH__FED_CMS_OPEN_PAYMENTS - who was being paid over the same window
- Joins on: drug name and code, then NPI
- Key strength: drug code is a lookup; NPI is steel
- Hit: A price spike, then a cost spike, then a payment, in that order, for one drug
- Miss: Prescribing follows price with no money attached and it is just a market
- Visual: three stacked lines on one date axis, price, cost, payments
- Why it's a story: Medicaid pricing, Medicare claims and industry payments on one drug

### 15 · Fracked here, undrinkable there

**Do counties with the most fracking jobs have the most drinking-water violations after?**

- Side A: ENVIRONMENT__FED_FRACFOCUS_DISCLOSURE_LIST - well, operator, location, water used, dates
- Side B: ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT - violations, contaminant, health-based
- Side C: ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS - population served
- Joins on: FIPS then PWSID
- Key strength: both proven families; the county-to-system hop is the join to prove
- Hit: Violations rise in the years after jobs start, in the same counties, not before
- Miss: Timing does not line up and the correlation is geology, not drilling
- Visual: small multiples, one county per panel, jobs as bars, violations as a line
- Why it's a story: An industry disclosure site and an EPA compliance file on one county

### 16 · The union with a hole in its books

**Do unions reporting missing money also run an active political fund?**

- Side A: LABOR__FED_DOL_OLMS - union assets, receipts, disbursements, membership, since 2000
- Side B: FINANCE__FED_FEC_INDIV_CONTRIBUTIONS - contributions tied to a committee
- Side C: POLITICS__FEC_COMMITTEE - the committee roster and its treasurer
- Joins on: union name to committee name
- Key strength: name match, not a catalog key
- Hit: A union whose books do not balance runs a committee that keeps spending
- Miss: Financial trouble and political spending are unrelated and the red flag is not one
- Visual: two-panel per union, balance sheet on the left, political spend on the right
- Why it's a story: A labour filing and a campaign filing, never joined

### 17 · Sponsored a visa, hurt the worker

**Do the employers who sponsor the most foreign workers at the legal minimum also rack up injuries?**

- Side A: IMMIGRATION__FED_DOL_OFLC - sponsor, job title, wage offered, worksite
- Side B: LABOR__FED_OSHA_ITA_300A_SUMMARY_2024 - injuries, illnesses, deaths per establishment
- Side C: ECONOMICS__FED_BLS_QCEW - what that industry pays in that county
- Joins on: NAME@ZIP then EIN
- Key strength: fuzzy on the employer name; EIN if the injury file resolves
- Hit: The same employer pays the floor wage and sits in the worst tenth on injuries
- Miss: Sponsors are mostly office jobs with no injury exposure and the pairing is empty
- Visual: scatter, wage against industry median, dot size is injury rate
- Why it's a story: Two Labor Department systems that do not talk to each other

### 18 · Relief money, then the injuries

**Did the businesses that took the most pandemic relief go on to injure more workers?**

- Side A: ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS - borrower, amount, jobs claimed, forgiveness
- Side B: LABOR__FED_OSHA_ITA_300A_SUMMARY_2023 - injuries the year after
- Side C: ECONOMICS__FED_SBA_LOANS - whether their other SBA loans defaulted
- Joins on: NAME@ZIP
- Key strength: fuzzy, multi-word names only; show as a sample
- Hit: Big forgiven loans, few jobs kept, and a rising injury count at the same address
- Miss: Relief tracked payroll honestly and the injury rate is flat
- Visual: three-column ranking, loan, jobs claimed, injuries, one row per borrower
- Why it's a story: An emergency programme and a safety file, same year, never compared

### 19 · The senator, the committee, the trade

**Did a senator trade a stock in a sector their own committee oversees, in the same session?**

- Side A: FINANCE__SENATE_TRADES - senator, asset, buy or sell, date, range, Bioguide matched
- Side B: POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP - which committee, which rank, when
- Side C: FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE - ticker to company to industry code
- Joins on: BIOGUIDE, then ticker to industry
- Key strength: Bioguide proven; the ticker-to-sector lookup does not exist yet
- Hit: A dated trade in a sector the member's committee was actively working
- Miss: Trades are index funds and blind trusts and the overlap is noise
- Visual: timeline per senator, committee tenure as a band, trades as dots inside it
- Why it's a story: Two disclosure regimes, one person, and a lookup table we still have to build

### 20 · Funded, published, retracted

**Do the institutions winning the most federal research money also retract the most papers?**

- Side A: SCIENCE_RESEARCH__FED_NIH_REPORTER - grant, institution, researcher, dollars, 27 years
- Side B: SCIENCE_RESEARCH__FED_RETRACTION_WATCH - journal, authors, institution, reason
- Side C: REFERENCE__XC_ROR_RESEARCH_ORGANIZATIONS - the org registry, to resolve names
- Joins on: institution name via the ROR registry
- Key strength: name match through a registry; not a catalog key
- Hit: Retractions per funded dollar varies wildly and some big names sit at the top
- Miss: Retractions scale with volume exactly and there is no story past size
- Visual: scatter, funding on one axis, retractions on the other, size is papers
- Why it's a story: An NIH database and a watchdog list, joined through a third registry

### 21 · Toxic air, subsidised housing

**Is subsidised housing sitting closer to the biggest toxic releasers than market housing?**

- Side A: ENVIRONMENT__FED_EPA_TRI_BASIC_2023 - pounds released, by chemical, by route
- Side B: ENVIRONMENT__FED_EPA_TRI_FACILITY - the facility, its parent, its coordinates
- Side C: HOUSING__FED_HUD_ASSISTED_HOUSING_PROJECTS - buildings, units, tenant demographics
- Joins on: FIPS, then coordinates for distance
- Key strength: FIPS proven; the distance ring has to be built
- Hit: Subsidised buildings sit inside a tighter radius, with tenant demographics attached
- Miss: Distance is the same as everywhere else and the siting claim does not hold
- Visual: map with release plumes as rings, housing dots inside, tenant mix on hover
- Why it's a story: EPA pounds and HUD tenants, one distance, never measured together

### 22 · Redlined, then the bank left

**Did banks pull branches out of the neighbourhoods graded hazardous in the 1930s?**

- Side A: HOUSING__FED_MAPPING_INEQUALITY - 1930s grade, the written description, the shape
- Side B: FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS - every branch, address, deposits, by year
- Side C: REFERENCE__CENSUS_CB_ZCTA - the zip shapes to place the branch
- Joins on: spatial, then ZIP
- Key strength: not a catalog key; a shape-in-shape join to build
- Hit: Branch counts in D-graded areas fall faster than in A-graded ones, decade by decade
- Miss: Branch loss is uniform and the 1930s grade adds nothing today
- Visual: animated map per city, grades underneath, branches appearing and vanishing
- Why it's a story: A 90-year-old map and an annual bank survey on the same ground

### 23 · Storm hit, water broke

**After a big storm, does the local drinking water start failing?**

- Side A: ENVIRONMENT__FED_NOAA_STORM_EVENTS - event, location, date, damage, deaths
- Side B: ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT - violation, contaminant, date
- Side C: ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS - population served
- Joins on: FIPS then PWSID
- Key strength: proven both sides; the county-to-system hop is the work
- Hit: Violation counts jump in the ninety days after a named storm, repeatedly
- Miss: No lift after storms, which says the systems held
- Visual: event-study chart, day zero is the storm, violation rate before and after
- Why it's a story: The weather service and the water regulator, one county, one clock

### 24 · Detention where the jail is already full

**Are immigration detention facilities sited in counties that already jail the most people?**

- Side A: IMMIGRATION__FED_ICE_DETENTION_FACILITY_CODES - facility, address, coordinates, type
- Side B: JUSTICE__XC_VERA_INCARCERATION_TRENDS - jail population by county, by race, by year
- Side C: DIM_COUNTY - population, to make it a rate
- Joins on: FIPS
- Key strength: county family, proven
- Hit: Detention clusters in the counties with the highest existing jail rates
- Miss: Siting is about land and highways and tracks nothing about local incarceration
- Visual: map, counties shaded by jail rate, detention facilities as dots on top
- Why it's a story: An immigration lookup table and a prison research dataset on one county code

### 25 · The owner behind three kinds of care

**Does the same owner run nursing homes, home health and hospice, and do the fines follow them?**

- Side A: HEALTH__FED_CMS_HOME_HEALTH_OWNERS - owner name, address, percent, entity type
- Side B: HEALTH__FED_CMS_NURSING_HOME_PENALTIES - fines and payment-denial periods
- Side C: HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES - citations, severity, corrected or not
- Joins on: CCN, and owner name across the ownership file
- Key strength: CCN steel; the owner-name resolve across types is the work
- Hit: One owner name appears across three care types with fines on all of them
- Miss: Owners stay in one lane and the multi-type operator is rare
- Visual: graph, owner at the centre, facility types as branches, fines sized on the leaves
- Why it's a story: An ownership file, a penalty file and a citation file, one person at the middle

---

# Part 5 — The checks

You found something. Now assume you're wrong.

Most exciting findings are load bugs, duplicate joins, or one person's
note taken too seriously. These five checks are what separates a finding
from a guess wearing a suit. Nothing in Part 4 has been through them.

## The 5 verification checks

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

---

## Standing rules

- Metadata mapping was desk review only — no live queries, no invented columns
- Check `.claude/traps.md` before trusting any column named here
- A candidate isn't a finding until it survives the 5 checks
- Nothing here is ranked by default — pick a move, pick a lens, run the loop
- Overlap is fine. A missing idea is not. New thought goes in here first.
