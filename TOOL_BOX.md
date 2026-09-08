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

This is the wide net. Every method, question, hunch, ranking, chart idea
and trap that exists for this warehouse lands here — nothing held back
for a separate report. If it's an idea about the data, it's in this file.

| Part | What it is | Why it's here |
|---|---|---|
| 1 · The moves | 27 ways to walk into the data | you need an angle before a query |
| 2 · The lenses | 61 known patterns to test against | real data either fits a known shape or breaks it |
| 3 · The shelf | what the warehouse will and won't allow | some joins look fine and return 8% |
| 4 · The questions | 542 specific questions, plus 25 builds | so you never start from a blank page |
| 5 · The checks | 5 ways to know a hit is real | most exciting findings are bugs |
| 6 · The Wonder Wall | 93 ideas ranked mechanism × readiness × harm × effort | scored bets, not just a list |
| 7 · The v2 inventory | 392 more ideas — charts, cards, text-as-data | a second docket pass, different question |
| 8 · Visualization catalog | 41 chart ideas tied to named verified tables | what can be built today, no re-checking |
| 9 · News corroboration | 24 real stories tested against the warehouse | proof the warehouse can find what's already true |
| 10 · The trap log | ~175 dated column-level traps, verbatim | the actual burn history, not a sample |

**61 lenses · 27 moves · 5 checks · 934 questions · 25 cross-joins · 93 ranked wonders · 41 viz ideas · 24 corroboration tests · ~175 traps**

Overlap is fine and expected. One question can use six tools. One tool
serves fifty questions. What's not fine is a gap — an idea about this
warehouse that lives somewhere else. Everything lands here first.

Status columns throughout this file are snapshots, not live state.
`docket/docket.csv` is the live tracker — cross something off there,
not here. This file is for casting the net wide, not for tracking work.

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
| 6 · The Wonder Wall | 93 ideas scored M × D × C × E, full ranking table |
| 7 · The v2 inventory | 392 ideas by subject, v1-vs-v2 diff, misfiled tables |
| 8 · Visualization catalog | 41 chart ideas, grouped by data substrate |
| 9 · News corroboration | Echo / Retrace / Stumble, 24-story scorecard |
| 10 · The trap log | every dated trap in `.claude/traps.md`, in full |
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

---

# Part 6 — The Wonder Wall

93 ideas, ranked. Not a docket question, a scored bet: mechanism, data
readiness, consequence and effort multiplied into one priority number.
Every score below was checked with a live query, not guessed from a
table name — that's the whole discipline of this part.

**Run:** 2026-08-22 · every data-readiness score below was verified with live queries against the warehouse this session (9 query batches). Nothing here is scored from table names.

**Scope:** all 75 wonders from `The_Wonder_Wall.md` plus 18 expansion wonders generated against verified-healthy tables. 93 ranked. Priority = M × D × C × E (max 625). Novelty is deliberately unscored — it belongs to the tabled "Pie in the Sky" project and has its own column so it can be joined in later.

**Axes:** **M** mechanism (5 = exposes a systemic dynamic, 1 = describes) · **D** data readiness (verified; broken upstream capped at 2) · **C** consequence to actual people · **E** effort (5 = one SQL + a chart, 1 = new pipeline / new math / animation engine).

---

## TOP 5 TO PROTOTYPE FIRST

Selection rule: highest priority score, with two adjustments stated openly — anything already built and run is excluded (see #26/#72 below), and where five wonders tied at 500 the tie was broken toward distinct source-and-mechanism coverage. Runners-up are named.

### 1. E1 — Which mine operators get the biggest discount between the penalty proposed and the penalty actually paid
**Score 625 (M5 · D5 · C5 · E5) · origin: expansion · lens: Surprise**

Every published violation count treats a citation as an event. This asks what the citation was actually worth after it was negotiated — enforcement that evaporates between assessment and collection, which no violation count anywhere shows.

- **Tables/columns:** `LIBRARY_MARTS.LABOR.LABOR__FED_MSHA_VIOLATIONS` — `PROPOSED_PENALTY`, `AMOUNT_DUE`, `AMOUNT_PAID`, `CONTROLLER_ID`, `CONTROLLER_NAME`, `MINE_ID`, `VIOLATION_OCCUR_DATE`, `SIG_SUB`, `NEGLIGENCE`.
- **The query:** `select controller_name, count(*), sum(proposed_penalty), sum(amount_paid), 100.0*sum(amount_paid)/sum(proposed_penalty) pct_paid ... group by 1 having sum(proposed_penalty) > threshold order by pct_paid asc`. Then repeat sliced by S&S flag, negligence level, and year to see whether the discount tracks severity.
- **Already measured this session:** $1.82B proposed vs $1.27B paid across 3.02M penalised violations — **69.9% collected, $548M assessed and never collected**. The worst-paying named operators land at 7.7%, 7.8%, 9.1%, 14.3%, 17.3%, 19.7%. One holds 1,801 violations, $5.62M proposed, $432,710 paid.
- **Effort:** under half a session for the core result. A second half-session to check whether the discount is contest-driven (appeals) versus non-collection, which changes what the number means.
- **Watch for:** `AMOUNT_PAID` is zero-not-null for uncollected rows, so a mean over all rows understates; use sums. Recent violations may still be in an appeal window — exclude the trailing 24 months before ranking.

### 2. E2 — Does the severity of a nursing-home citation depend on which state inspected it
**Score 625 (M5 · D5 · C5 · E5) · origin: expansion · lens: Surprise**

Same federal tag numbers, same federal law, 50 state survey agencies applying them. If severity assignment varies by state far more than facility conditions do, the regulator is the variable — and a resident's protection depends on their address.

- **Tables/columns:** `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES` — `STATE`, `SCOPE_SEVERITY_CODE`, `DEFICIENCY_TAG_NUMBER`, `SURVEY_DATE`, `CMS_CERTIFICATION_NUMBER_CCN`; joined to `HEALTH__FED_CMS_NURSING_HOME` for facility covariates (beds, staffing, ownership type, chain).
- **The query:** harm-level share per state = `sum(case when scope_severity_code in ('G','H','I','J','K','L') then 1 else 0 end) / count(*)`, grouped by state, then re-run holding the tag number fixed so you compare like citation to like citation.
- **Already measured this session:** harm-level share runs **12.50% (KY) and 12.07% (IL) down to 1.32% (NV) and 1.85% (MD)** — a **9.5x spread** across states with 2,000+ citations each. California, with 57,877 citations, sits at 2.54%.
- **Effort:** under half a session for the state ranking; one more session to hold tag, facility size and ownership type fixed, which is what turns it from a table into a finding.
- **Watch for:** real coverage is 2023–2026 (see readiness findings); state citation volumes differ 25x, so use rates and a minimum-volume floor.

### 3. #55 — Which mine's fatality-to-violation ratio breaks the pattern: deaths without a paper trail
**Score 500 (M5 · D5 · C5 · E4) · origin: wall · lens: Anomaly**

The highest-scoring wonder on the original wall. A death that generated no enforcement, or an enforcement record with no deaths behind it, is a mechanism with a body attached.

- **Tables/columns:** `LABOR__FED_MSHA_ACCIDENTS` (`IS_FATALITY`, `DEGREE_INJURY`, `MINE_ID`, `CONTROLLER_ID`, `ACCIDENT_DATE`, `NARRATIVE`) against `LABOR__FED_MSHA_VIOLATIONS` (`MINE_ID`, `CONTROLLER_ID`, `VIOLATION_OCCUR_DATE`, `SIG_SUB`), denominated by `LABOR__FED_MSHA_MINES` (`NO_EMPLOYEES`, `CURRENT_MINE_STATUS`).
- **The approach:** deaths per 1,000 violations and deaths per employee-year, per controller, over a fixed horizon — then rank the residual against the controller's own size and mine type. The 273,621 accident narratives are the receipt layer for whatever surfaces.
- **Verified:** 1,208 fatalities (`IS_FATALITY` and `DEGREE_INJURY='FATALITY'` agree exactly, and match the raw figure the July audit cited), 3.09M violations, 19,430 controllers with violations, 6,634 with accidents, 26 years of clean overlap.
- **Effort:** one session. Two aggregates, a ratio, and a size-adjusted residual.
- **Watch for:** raw ratios shrink toward the present (fixed-horizon rule); 48% of mines have null lat/lon so keep this non-geographic; `NO_EMPLOYEES` is null on 39,735 of 91,906 mines, so the employee denominator only covers active operations.

### 4. E7 — Do facilities in more-minority communities get inspected less while staying out of compliance longer
**Score 500 (M5 · D4 · C5 · E5) · origin: expansion · lens: Causal**

A finished mart nobody is using. It already carries compliance status, inspection counts, penalty totals, community racial composition and geography on one row.

- **Tables/columns:** `LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__EPA_PENALTY_GAP` — `PCT_MINORITY`, `QUARTERS_WITH_NONCOMPLIANCE`, `TOTAL_INSPECTION_COUNT`, `FORMAL_ACTION_COUNT`, `TOTAL_PENALTIES`, `CHRONIC_NO_PENALTY`, `NEVER_INSPECTED_NONCOMPLIANT`, `IN_MAJORITY_MINORITY_COMMUNITY`, `LATITUDE`/`LONGITUDE`, `STATE`, `POPULATION_DENSITY`.
- **The query:** decile facilities by `PCT_MINORITY`, then compare mean inspections, mean quarters-in-noncompliance and chronic-no-penalty share across deciles; repeat within state and within program type to strip out where-the-industry-is confounding.
- **Already measured this session:** inspections fall **2.90 → 1.46** from the whitest to the most-minority decile while quarters in noncompliance rise **8.24 → 8.85**. 86,963 of 93,808 facilities (92.7%) have zero penalties; 53,587 (57.1%) were never inspected while noncompliant.
- **Effort:** one session for the honest version — the raw gradient is one query, but the state/program controls are what make it defensible.
- **Watch for:** 29,702 rows (32%) are missing `PCT_MINORITY` and 5,653 are missing geography — check whether the missingness itself is patterned before reporting anything. Penalty dollars run the *other* way (higher in high-minority deciles), so the finding is about inspection, not fines; say so or it reads as overstated.

### 5. E8 — Does a nursing home's staffing level predict its next deficiency, holding size and state fixed
**Score 500 (M5 · D5 · C5 · E4) · origin: expansion · lens: Causal**

Staffing is the one lever a regulator can actually pull. Deficiencies are the harm it is supposed to prevent. Nobody has connected the two on this data yet.

- **Tables/columns:** `HEALTH__FED_CMS_NURSING_HOME` — seven reported staffing measures, five case-mix-adjusted ones, `TOTAL_NURSING_STAFF_TURNOVER`, `REGISTERED_NURSE_TURNOVER`, `NUMBER_OF_ADMINISTRATORS_WHO_HAVE_LEFT_THE_NURSING_HOME`, `NUMBER_OF_CERTIFIED_BEDS`, `AVERAGE_NUMBER_OF_RESIDENTS_PER_DAY`, `OWNERSHIP_TYPE`, `CHAIN_NAME`, `STATE` — joined to `HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES` on CCN for the forward-looking outcome.
- **The approach:** staffing measured at time T, deficiency count and severity in the following window, with size, state and ownership type held fixed. Turnover is the sharper predictor to test first — it is the measure a facility can hide least.
- **Effort:** one to two sessions. The join is trivial; the care is all in the forward-window construction so you are predicting rather than describing.
- **Watch for:** the facility table is a snapshot, so staffing is "now" and the deficiencies are a 2023–2026 history — the forward window has to be built from `SURVEY_DATE` and the staffing snapshot treated as end-of-period, or the arrow points backwards.

**Tied runners-up at 500, both MSHA, both a session each:** **E10** (does a mine changing hands change its violation rate — roughly 9,500 mines have had two or more controllers, which is the ownership-change study nursing homes cannot support) and **E14** (does a death at one mine change violation rates at the same operator's other mines).

---

## THREE THINGS TO KNOW BEFORE READING THE TABLE

**The wall's own guess about which lenses were rich was wrong.** The handoff expected Density and Structure to be the deep quarries. Scored on M × D × C, they came out **second-worst and third-worst** of the ten single lenses above 25 (Structure 32.3, Density 31.9). The rich ones are **Surprise 52.4, Causal 47.8, Contagion 47.2** — so those are where the 18 expansion wonders were generated. The reason is structural, not accidental: density and structure are *display* lenses that mostly recover population and size, while surprise, causal and contagion are *mechanism* lenses, which is what the mission actually asks for. Full lens table below.

**Two wonders are already answered.** #26 and #72 (does a violation cascade to same-owner siblings; does it spread faster inside a clique) were built and run on **2026-08-21** with 20-draw control validation: nursing homes +13.3% over control, mines +34.3%, toxic-release sites +11.8%. They are excluded from the top 5 because prototyping them would be redoing yesterday's work. The live follow-on is **E13** — whether that co-spike survives controlling for the regulator's district office and calendar, which is the caveat that run flags about itself.

**MSHA is the healthiest source on this wall, by a distance.** 26 years of clean overlap between violations and accidents, a real ownership key stamped on every violation, penalty amounts proposed *and* paid, a fatality flag that reconciles exactly, and 273,621 rows of genuine prose narrative. Four of the top seven are MSHA and that is a finding, not a bias — most other sources on the wall turned out to be three-year windows.

### Lens ranking (original 75 only, M × D × C, effort ignored)

| Lens | Avg | n | Read |
|---|---:|---:|---|
| Cross-lens combos | 61.6 | 5 | Highest of all — combining two lenses genuinely adds mechanism, when both legs are sound |
| Surprise | 52.4 | 5 | **Expanded** — order-where-there-should-be-noise is the strongest mechanism family here |
| Causal | 47.8 | 5 | **Expanded** — highest mechanism scores on the wall, repeatedly killed by missing data |
| Contagion | 47.2 | 6 | **Expanded** — and the platform already has a rule engine for it |
| Anomaly | 45.8 | 5 | Bimodal: #55 is the wall's best wonder, #54 and #56 are its worst |
| Community | 45.6 | 5 | Solid; identity resolution is the recurring ceiling |
| Flow | 43.8 | 5 | Good mechanisms, repeatedly blocked by missing history |
| Prediction | 40.2 | 4 | Carried almost entirely by #59 |
| Structure | 32.3 | 7 | Expected to be rich; the domain taxonomy is too coarse to support it |
| Density | 31.9 | 7 | Expected to be rich; heat maps mostly recover population |
| Phase | 29.8 | 6 | Evocative framing, thin data |
| Compression | 25.6 | 5 | Mostly re-derives things already labelled |
| Narrative | 25.6 | 5 | See the special check below — half the lens is theoretical |
| Temporal | 24.4 | 5 | Killed by three-year windows across almost every source |

---

## SPECIAL CHECK — the Narrative lens (#66–70): half live, half theoretical

The brief asked whether free text actually exists. It does, but **not where the wall assumed**.

| Wonder | Text it assumed | What is actually there | Verdict |
|---|---|---|---|
| #66 inspection notes | CMS inspector notes | `DEFICIENCY_DESCRIPTION` is the canned federal tag label: **260 distinct values across 418,479 rows**, 277 tag numbers, avg 118 chars, repeated verbatim | **Dead as written** |
| #67 CFPB escalation phrases | complaint narratives | **Real: 3,825,161 narratives, avg 1,021 chars, max 35,984** — but no escalation outcome exists to predict (only response category / timely / closed) | **Half live** |
| #68 model legislation | state bill text | **No state legislation in the warehouse at all.** Federal bills carry only `TITLE` (avg 69 chars) | **Dead — needs a new ingest** |
| #69 FAERS dialects | adverse-event report text | FAERS has **no narrative column**, and the reporter-type field is one of the shifted columns | **Dead** |
| #70 enforcement sentiment | enforcement documents | Only short operational notes (EPA single-event violation comments, SDWA visit comments); no dated document corpus | **Dead as written** |

**The live free-text corpus, verified:** CFPB complaint narratives (3.83M, 2011–2026) · **MSHA accident narratives (273,621 real prose rows, avg 189 chars, 2000–2026, only 2 blank — the best long-run narrative corpus in the warehouse, with a hard fatality outcome attached)** · CPSC NEISS injury narratives (1.72M of 9.79M rows populated, 1999–2025) · NOAA storm event and episode narratives (1.78M rows, 39% blank).

So the Narrative lens is not dead — it is pointed at the wrong tables. The MSHA substitute is what #66 should have asked for.

## Cross-lens combos (#71–75) — flagged as instructed

| # | Score | Component check |
|---|---:|---|
| #72 | 300 | Both legs strong (#26 D4, #65 D4) — but **already answered**, see above |
| #75 | 320 | Both legs strong; this is #23 with a clock on it, and #23's evidence is already dramatic |
| #74 | 240 | Both legs verified end to end (the money→member→vote chain works) |
| #71 | 72 | Weak by construction — a presentation upgrade of #1/#2/#3, not a new question |
| **#73** | **72** | **FLAGGED: both components score low.** #8 is blocked (D2, broken domain taxonomy) and #52 is mechanism-poor (M2). Do not build. |

---

## DATA READINESS FINDINGS

Everything below was found while verifying the D axis. Bad news first.

### New defects found this session

1. **FAERS is column-shifted, and the shift is in the landing table too.** `FDA_DT` holds report codes `EXP` / `PER` / `DIR` on 4.27M rows where dates belong; `GNDR_COD` holds `Y`/`N` (E-sub values) on 4.28M rows against only 1.41M real F/M; `HEALTH__FED_FDA_FAERS_DRUG` shifts by one from `DRUG_SEQ` onward, so `ROLE_COD` holds drug names and `DRUGNAME` holds numbers. This confirms the July defect that was carried as unverified. It affects roughly 58M rows across the five FAERS tables and blocks four wonders outright (#5, #25, #49, #69). Because landing is shifted, it is an ingest defect, not a mart bug — a re-parse, not a rebuild.

2. **The nursing-home ownership-change flag is dead.** `PROVIDER_CHANGED_OWNERSHIP_IN_LAST_12_MONTHS` reads `'N'` on all 14,700 rows. CMS does not publish 14,700 facilities with zero ownership changes; this is almost certainly a load defect. It single-handedly blocks #17, #38 and #43 — three of the wall's highest-mechanism wonders.

3. **The portal dataset index is a capped crawl, not a census.** Five portals sit at exactly 25,000 rows (Canada, Australia, Virginia, HDX, UK) and two at exactly 10,000 — the round-count truncation signature. On top of that, 259,869 of 338,520 datasets (76.8%) expose no column metadata, and with-columns coverage is wildly uneven (Open Data DC 6,267 of 10,000; UK 0 of 25,000). Any "where is public data thin" reading measures the crawler. Blocks #6, #13, #35.

4. **OSHA ITA hours-worked has scale outliers.** `TOTAL_HOURS_WORKED` sums to 1,065 billion hours against 138.8M reported employees — about 7,672 hours per employee per year, which is impossible. Aggregate injury rates still come out BLS-plausible (delivery 6.3, air transport 5.34 days-away cases per 200k hours), so the corruption is in a tail that needs trimming before any per-establishment rate is trusted.

5. **OSHA ITA `EIN` is not a usable join key.** 43,260 blank of 398,620, and minimum length 1 on the non-blank values. Key on `ESTABLISHMENT_ID` instead. This is the same masked-ID trap as NPPES EIN and FCC ULS EIN.

6. **CFPB mart is 11,501 rows short of landing** (17,168,287 vs 17,179,788 — 0.067%). Small, but it is a gap, not a rounding artefact.

### Coverage limits that are not defects but change what is answerable

- **FEC individual contributions has no history.** 84.2M rows, and **99.99% of them fall in 2023–2026** (2023: 18.1M, 2024: 40.1M, 2025: 21.0M, 2026: 5.0M). Every year before 2021 combined is under 30 rows. Kills #50 outright and caps every FEC temporal wonder at three and a half years. Three rows carry a year-3312 date.
- **CMS deficiencies are really only 2023–2026.** The table spans 2017–2026 but the early years are a straggler tail: 273 rows in 2017 against 121,925 in 2024. CMS publishes a rolling window. Anything asking for "a decade" (#47) does not have one.
- **CMS penalties span 2023-06 to 2026-05 only**, with 2,470 of 16,180 (15%) carrying a null fine amount.
- **Congressional committee membership has no clock.** 3,879 rows with committee code, name, bioguide, party, rank and title — no congress number, no start date. It is a current snapshot, which kills #45's "money arriving *after* the seat" and caps #7 at correlation.
- **There is no OSHA violation data.** Only ITA injury summaries (2023/24/25) and case details. The inspections re-pull is mid-flight at roughly 300k of ~4.5M rows and rate-limited. Blocks #28.
- **There is no federal staffing or agency-headcount table anywhere** (nothing under OPM, FedScope, workforce, staffing or appropriations). USAspending agency aggregates are awards, not people. Kills #42, the wall's best causal question.
- **There is no MSHA inspector identifier.** Kills #4.
- **There is no state legislation, and federal bills carry title only.** Kills #68.
- **Cosponsorships and roll-call votes are congresses 118–119 only** (2023-01 to 2026-06). Fine for network work, but "career" questions (#56) have two terms to work with.
- **48% of mines have no coordinates** (44,356 of 91,906 null latitude) and 43% have no employee count. Keep MSHA work non-geographic and be careful with per-worker denominators.
- **NEISS narratives are 82.5% blank** (8,079,416 of 9,794,971) and average 64 characters where present.
- **NOAA storm events are 41% without coordinates** (736,104 of 1,780,730) and 39% without an event narrative.

### Surprises worth knowing

- **CFPB is 77% three credit bureaus.** TransUnion 4.60M + Equifax 4.51M + Experian 4.12M = 13.2M of 17.17M complaints. Any CFPB density, community or flow analysis that does not handle this just rediscovers the big three.
- **CFPB narratives are industrially templated.** The single most-repeated narrative text appears **27,510 times**; the next five appear 24,241 / 18,431 / 15,803 / 12,204 / 10,903 times. 2.57M distinct texts across 3.83M narratives. #23 is not a hypothesis — it is visible in one GROUP BY.
- **CFPB responses are near-canned too.** Experian answers 79.2% of 4.12M complaints with one response category; JPMorgan 79.4%, Wells Fargo 78.9%, Capital One 77.4%.
- **61.6% of FEC contribution rows say `RETIRED` or `NOT EMPLOYED`** — and the blank-occupation bucket, only 2.7M rows, carries the single largest dollar total at $5.2B. The occupation axis is emptiest exactly where the money is.
- **The politics money→member→vote chain is fully wired and verified.** 54,195,669 contributions ($6.86B) reach 695 sitting members through `POLITICS__MEMBER_FEC_ID` → `FEC_CAND_CMTE_LINKAGE`; 1,067,437 votes reach 635 members through ICPSR → bioguide; the windows overlap exactly. **This corrects a standing note that politics had zero verified cross-family joins** — that is no longer true.
- **Cross-domain entity bridging is nearly nonexistent.** Only 105,724 of 33.2M entities (0.32%) appear in two domains, none in three, and 78% of the index is labelled `other` across just five domain buckets. The useful axis is key-type reach instead: **EIN spans 34 source tables, NPI 32 (9.6M entities), CCN 23, CIK 19, FRS_ID 15 (5.4M entities)** — which is #12's answer, sitting in one GROUP BY.
- **The connection map is mostly weak-tier.** 4,910 edges: CORROBORATED 2,670 at an average 7.1% match rate, STEEL 1,386 at 52.8%, BRIDGE 496, GEO 353, STRONG 5.
- **`ENVIRONMENT__EPA_PENALTY_GAP` is a finished, unused, mission-shaped mart** — 93,808 facilities with compliance status, inspection counts, penalty totals, community racial composition and coordinates on one row. See E7.
- **MSHA ownership changes are directly observable**: 6,358 mines had 2 controllers, 2,091 had 3, one had 11. Roughly 9,500 mines changed hands. 6,082 controllers hold 2+ mines.
- **The nursing-home clinician graph is too sparse to use.** Only **273 facility pairs** share 5 or more clinicians (40,841 nursing-home links of 2.26M total, and no dates). E15 was killed by this check.
- **`ENTITY_INDEX` is 84.4M rows, not 12.88M** — the figure on the wall and in The Laboratory is stale by a factor of six.
- **The MSHA zero-deaths defect carried since July is not present.** `IS_FATALITY` and `DEGREE_INJURY = 'FATALITY'` both return exactly 1,208, matching the raw figure the audit cited. That item can come off the carried list.

---

## FULL RANKING — all 93

Sorted by priority score (M × D × C × E). `origin: wall` = one of the original 75. `origin: expansion` = generated this session against verified-healthy tables.

| Rank | ID | Origin | Lens | Restatement | M | D | C | E | Priority | Novelty | Justification | Blocking defects / caveats |
|---:|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|
| 1 | E1 | expansion | Surprise | Which mine operators get the biggest discount between the penalty proposed and the penalty actually paid | 5 | 5 | 5 | 5 | **625** | unscored | Enforcement that evaporates after assessment is invisible in every violation count anyone publishes - and the gap is enormous. | None. Verified: $1.82B proposed vs $1.27B paid across 3.02M penalised violations = 69.9% collected, $548M assessed and never collected. Worst named operators pay 7.7%-19.7% (one at 1,801 violations / $5.62M proposed / $432,710 paid). |
| 2 | E2 | expansion | Surprise | Does the severity of a nursing-home citation depend on which state inspected it | 5 | 5 | 5 | 5 | **625** | unscored | Same federal tags, same federal law, wildly different state hands - the regulator becomes the variable instead of the facility. | None. Verified: share of citations at harm-level severity (G-L) runs 12.50% in KY and 12.07% in IL down to 1.32% in NV and 1.85% in MD - a 9.5x spread across state survey agencies with 2,000+ citations each. |
| 3 | 55 | wall | Anomaly | Which mine's fatality-to-violation ratio breaks the pattern - deaths without a paper trail | 5 | 5 | 5 | 4 | **500** | unscored | Deaths that generated no enforcement is a mechanism with a body attached, on the healthiest source on the wall. | None. Verified: 1,208 fatalities (IS_FATALITY and DEGREE_INJURY='FATALITY' agree exactly, matching the raw figure the July audit cited), 3.09M violations, 19,430 controllers with violations and 6,634 with accidents, 26-year overlap. |
| 4 | E10 | expansion | Causal | Does a mine changing hands change its violation rate | 5 | 5 | 5 | 4 | **500** | unscored | This is the ownership-change study nursing homes cannot support, and mines can - the controller is stamped on every violation across 26 years. | None. Verified: 6,358 mines saw 2 controllers, 2,091 saw 3, up to one with 11 - roughly 9,500 mines changed hands at least once. 6,082 controllers hold 2+ mines. |
| 5 | E14 | expansion | Contagion | Does a death at one mine change violation rates at the same operator's other mines | 5 | 5 | 5 | 4 | **500** | unscored | A different trigger from the 08-21 rule - a body, not a citation count - and the strongest ownership key in the warehouse. | None. Verified: 1,208 fatalities, 6,082 controllers with 2+ mines, 6,634 controllers with accidents, 26-year overlap on MINE_ID / CONTROLLER_ID. |
| 6 | E7 | expansion | Causal | Do facilities in more-minority communities get inspected less while staying out of compliance longer | 5 | 4 | 5 | 5 | **500** | unscored | Mechanism-first, harm-first, geography-ready, already built - and the gradient is already visible. | 32% (29,702 of 93,808) missing PCT_MINORITY; 5,653 missing geo; 44% null last-inspection date. Verified gradient: inspections fall 2.90 to 1.46 across minority deciles while quarters-in-noncompliance rise 8.24 to 8.85. |
| 7 | E8 | expansion | Causal | Does a nursing home's staffing level predict its next deficiency, controlling for size and state | 5 | 5 | 5 | 4 | **500** | unscored | Staffing is the lever a regulator can actually pull; deficiencies are the harm it is supposed to prevent. | 2023-2026 deficiency window. Seven reported plus five case-mix-adjusted staffing measures, turnover, and administrator departures all present across 14,700 facilities. |
| 8 | 2 | wall | Density | Nursing-home fines heat-mapped per owner instead of per location | 4 | 4 | 5 | 5 | **400** | unscored | 'Does harm follow ownership or geography' is a real mechanism test, and the chain axis is live. | CHAIN_NAME blank on 4,221 of 14,700 facilities (28.7%); penalties table covers 2023-06 to 2026-05 only. |
| 9 | 23 | wall | Surprise | Which company's CFPB narratives are too similar - templated robo-text | 4 | 5 | 4 | 5 | **400** | unscored | Not just answerable - already visibly true at a glance, and mass-produced complaints distort the signal for everyone reading it. | None. Verified: the single most-repeated narrative appears 27,510 times; the next five appear 24,241 / 18,431 / 15,803 / 12,204 / 10,903 times. 2.57M distinct texts across 3.83M narratives. |
| 10 | 26 | wall | Contagion | Does one nursing-home violation cascade to sister facilities under the same owner | 5 | 4 | 5 | 4 | **400** | unscored | ALREADY ANSWERED 2026-08-21: same-owner co-spike 76.8% vs a 20-draw control of 63.5% (+13.3%) across 2,524 spikes; mines +34.3%, TRI sites +11.8%. | Not a defect - this is built and run (scripts/ripples/neighbor_spike_rule.py). The open question is the report's own caveat: state inspector calendars vs owner management. |
| 11 | E11 | expansion | Causal | Do nursing homes lose stars after a fine, or do fines follow lost stars | 5 | 4 | 5 | 4 | **400** | unscored | A directional test with real dates on both sides settles which way the arrow points. | Penalties 2023-06 to 2026-05; rating-cycle survey dates present. 2,470 penalties (15%) carry a null fine amount. |
| 12 | E13 | expansion | Contagion | Does the same-owner co-spike survive controlling for the regulator's district office and calendar | 5 | 4 | 5 | 4 | **400** | unscored | This is the open follow-on the 2026-08-21 run names itself: sister sites in one district get visited together regardless of who owns them. | Needs a district or region field. MSHA violations carry no district column directly - it would be derived from mine state and county. The rule engine already exists. |
| 13 | E16 | expansion | Contagion | Does a complaint spike at one credit bureau appear at the other two within days | 4 | 5 | 4 | 5 | **400** | unscored | Isolates whether spikes are company events or filing-mill events - and the big three ARE the corpus. | None. Verified: TransUnion 4.60M, Equifax 4.51M, Experian 4.12M = 77% of 17.17M complaints, daily dates 2011-2026. |
| 14 | E3 | expansion | Surprise | Do self-reported OSHA injury counts bunch on round numbers, and does the bunching grow with employer size | 4 | 4 | 5 | 5 | **400** | unscored | Round-number piling in self-reported harm counts is an under-reporting signature, and the repo already has a bunching detector. | OSHA ITA has scale outliers: TOTAL_HOURS_WORKED sums to 1,065B hours against 138.8M reported employees (~7,672 hrs/employee - impossible), so the tail needs trimming. Aggregate rates come out BLS-plausible. |
| 15 | E4 | expansion | Surprise | Which companies answer nearly every CFPB complaint with the same canned response | 4 | 5 | 4 | 5 | **400** | unscored | A firm that answers 79% of four million complaints identically is not answering them. | Ceiling is bounded - only 6-8 response categories exist. Verified: Experian 79.2% one category across 4.12M complaints, JPMorgan 79.4%, Wells Fargo 78.9%, Capital One 77.4%. |
| 16 | E9 | expansion | Causal | Do OSHA establishments that reported a death change their reported hours or injuries the next year | 5 | 4 | 5 | 4 | **400** | unscored | Tests whether a fatality triggers a real safety change or a reporting change - and there is a genuine panel to test it on. | Verified: 219,860 establishments appear in both 2023 and 2024. Deaths fall 859 to 812 to 778 across the three years. EIN quality is poor (min length 1, 43,260 blank) so key on ESTABLISHMENT_ID. |
| 17 | 48 | wall | Temporal | Does mine inspection have a season, and do accidents cluster in the gaps | 4 | 5 | 4 | 4 | **320** | unscored | A seasonal enforcement gap that lines up with injuries is a mechanism with a named victim - and this is the longest verified overlap on the wall. | None. Violations 1994-2026 (3.09M, 31,277 mines) and accidents 2000-2026 (273,623) both carry real dates: 26 years of clean overlap. |
| 18 | 53 | wall | Anomaly | Which facility's inspection record is statistically impossible - too clean for its peers | 4 | 4 | 5 | 4 | **320** | unscored | 'Too clean' points at capture or non-inspection, which is a mechanism with residents on the other end. | Real window 2023-2026. Peer covariates (beds, staffing, ownership type, state) all present across 14,632 CCNs. |
| 19 | 75 | wall | Combo | Surprise + Narrative - entropy collapse in filing language over time | 4 | 5 | 4 | 4 | **320** | unscored | This is #23 with a clock on it, and #23's evidence is already dramatic. | None. 14 years (2011-2026) to watch templating arrive; the same credit-bureau concentration caveat applies. |
| 20 | E17 | expansion | Contagion | Do injury rates cluster within industry-and-state cells beyond what employer size explains | 4 | 4 | 5 | 4 | **320** | unscored | Same work, same state, different odds of getting hurt is a mechanism with a worker on the other end. | Same hours-outlier caveat as E3. 1,218 NAICS codes, 3 years, ~1.18M establishment-years. |
| 21 | 12 | wall | Structure | Which join key is secretly the most valuable in the whole warehouse | 4 | 5 | 3 | 5 | **300** | unscored | Tells you where to build next, which decides who gets found; the answer is already sitting in one GROUP BY. | None. Verified this session: EIN reaches 34 tables, NPI 32 (9.6M entities), CCN 23, CIK 19, FRS_ID 15 (5.4M entities). |
| 22 | 44 | wall | Causal | Does a fine actually change behaviour - trajectories before vs after, matched controls | 5 | 4 | 5 | 3 | **300** | unscored | The single most important question you can ask an enforcement dataset, and the pieces are all present. | 3-year window means short pre/post arms; 2,470 of 16,180 penalties (15%) have a null fine amount. 3,722 facilities have 2+ penalties; 14,700-facility control pool with covariates. |
| 23 | 59 | wall | Prediction | Predicted vs actual inspection outcomes - the confident misses are the story | 5 | 4 | 5 | 3 | **300** | unscored | Residuals-as-the-finding is genuinely mechanism-first; this is #53 with a model behind it. | Same 2023-2026 window and same feature set as #53. |
| 24 | 72 | wall | Combo | Community + Contagion - does a violation spread faster inside a clique than between | 5 | 4 | 5 | 3 | **300** | unscored | The wall is right that this is the smoking-gun shape - and it was already run on 2026-08-21. | ALREADY ANSWERED: nursing homes +13.3% over a 20-draw control, mines +34.3%, TRI +11.8%. Components #26 and #65 both score well, so this is not built on weak legs. Open follow-on: inspector calendar vs owner management. |
| 25 | E12 | expansion | Causal | Does the special-focus designation actually change facility behaviour | 5 | 3 | 5 | 4 | **300** | unscored | A designed natural experiment sitting unused in the data. | Small and snapshot-only: 88 current SFF and 440 candidates, with no designation DATE - entry and exit timing would have to be inferred. |
| 26 | 24 | wall | Surprise | Are some facilities' inspection outcomes suspiciously low-entropy | 4 | 4 | 4 | 4 | **256** | unscored | The same result regardless of conditions points at the inspection process, not the facility. | Real coverage is 2023-2026: the deficiency table's 2017-2022 rows are a straggler tail (273 rows in 2017 vs 121,925 in 2024). |
| 27 | E5 | expansion | Surprise | Do nursing-home surveys bunch at the end of the certification window rather than at risk | 4 | 4 | 4 | 4 | **256** | unscored | If inspection timing is administrative rather than risk-driven, the whole inspection record measures the calendar. | Real window 2023-2026 only; SURVEY_DATE and INSPECTION_CYCLE both present across 418,479 rows. |
| 28 | 14 | wall | Structure | Which donor appears in the most different networks - small everywhere, present everywhere | 4 | 4 | 3 | 5 | **240** | unscored | The ubiquitous small donor is a genuinely different actor type from the big one. | Verified: top donor (name+ZIP) gave to 268 distinct committees. Identity is name+ZIP (CORROBORATED tier, not a hard ID); 2023-2026 window. |
| 29 | 22 | wall | Surprise | Does donation timing entropy drop right before key votes | 5 | 4 | 4 | 3 | **240** | unscored | Randomness collapsing into pattern around votes is a textbook mechanism claim, and the chain is verified end to end. | Verified: 54.2M contributions ($6.86B) reach 695 sitting members; 1.07M votes reach 635 members; windows overlap exactly. Individual contributions only; 2 congresses. |
| 30 | 65 | wall | Community | Which facilities cluster by behaviour rather than ownership - acting like a chain without being one | 5 | 4 | 4 | 3 | **240** | unscored | A behavioural chain that is not a legal chain is exactly a hidden mechanism, and CHAIN_NAME gives you ground truth to check against. | 14,700 facilities x ~50 numeric features verified populated; 2023-2026 for the deficiency-derived features. |
| 31 | 74 | wall | Combo | Causal + Flow - money before votes vs after, as two overlaid rivers | 5 | 4 | 4 | 3 | **240** | unscored | Strong mechanism on a chain that is verified end to end. | 54.2M contributions ($6.86B) reach 695 members; 1.07M votes reach 635 members; exact 2023-2026 overlap. Two congresses only. |
| 32 | 18 | wall | Phase | The percolation curve of the edge map - how close is the warehouse to one component | 3 | 5 | 3 | 5 | **225** | unscored | About the platform rather than the world, but it directly sets the next build. | None. CONNECT_EDGES is 4,910 rows with tier/match-rate/confidence: CORROBORATED 2,670 (avg 7.1% match), STEEL 1,386 (52.8%), BRIDGE 496, GEO 353, STRONG 5. |
| 33 | 41 | wall | Flow | Complaint volume migrating between financial products over time | 3 | 5 | 3 | 5 | **225** | unscored | Clean, long, one query - but describes migration rather than explaining it. | None. 17.17M complaints, 23 products, 180 issues, 2011-2026. |
| 34 | E18 | expansion | Contagion | Does an enforcement action at one facility change inspection frequency at its neighbours | 5 | 3 | 5 | 3 | **225** | unscored | Deterrence spillover is a real regulatory mechanism. | The penalty-gap mart is a snapshot with counts, not an event stream - the timed version needs the underlying EPA ICIS action records wired in. |
| 35 | 30 | wall | Contagion | Do CFPB complaint surges propagate from one company to its competitors | 4 | 4 | 3 | 4 | **192** | unscored | Attention spreading through a sector is a real dynamic and the series is the longest clean one available. | 2011-12 to 2026-07 (14 years), 8,084 companies. 'Sector' must be defined carefully around the credit-bureau mass. |
| 36 | 40 | wall | Flow | Out-of-state money flooding small races | 4 | 4 | 3 | 4 | **192** | unscored | Outside money in low-attention races is a real, consequential dynamic and the chain works. | Same verified chain as #37 plus CAND_OFFICE_DISTRICT. 2023-2026 window. |
| 37 | 7 | wall | Density | Congressional fundraising density mapped onto committee assignments | 4 | 3 | 4 | 4 | **192** | unscored | Money pooling around specific seats is a genuine mechanism; the money half is fully wired. | Committee membership has NO date or congress column - it is a current snapshot (3,879 rows, 528 members, 228 committees). Comparison is possible; change is not. |
| 38 | 3 | wall | Density | CFPB complaints heat-mapped by company instead of place | 3 | 4 | 3 | 5 | **180** | unscored | Reframes the unit but 'firms as hotspots' largely tracks customer-base size. | 77% of the 17.17M complaints are three credit bureaus (TransUnion 4.60M, Equifax 4.51M, Experian 4.12M). |
| 39 | 33 | wall | Compression | Nursing homes in compressed space - do bad actors form a visible island | 3 | 5 | 4 | 3 | **180** | unscored | Descriptive, but on unusually rich features and trivial compute. | None. ~50 numeric features per facility across 14,700 rows, zero null lat/lon. |
| 40 | E6 | expansion | Surprise | Does contribution timing spike on filing-deadline eves rather than spreading evenly | 3 | 4 | 3 | 5 | **180** | unscored | Deadline-driven money is a known artefact; worth measuring so it can be subtracted from #22. | 2023-2026 window; TRANSACTION_DATE is a real DATE with only 583 nulls in 84.2M rows. |
| 41 | 17 | wall | Phase | Is there a fine threshold where nursing-home owners start restructuring | 5 | 2 | 5 | 3 | **150** | unscored | Behavioural phase change under enforcement pressure is exactly the shape Ripple wants - and the signal column is dead. | BLOCKED: PROVIDER_CHANGED_OWNERSHIP_IN_LAST_12_MONTHS reads 'N' on all 14,700 rows (a dead column, near-certainly a load defect). No ownership-history table exists. |
| 42 | 37 | wall | Flow | Political money as literal rivers - donor regions into candidate regions | 3 | 4 | 3 | 4 | **144** | unscored | Out-of-state money is real, but the map largely restates population. | Chain verified: donor ZIP (99.94% usable) to CMTE_ID to CAND_CMTE_LINKAGE to CAND_OFFICE_ST. 2023-2026 window. |
| 43 | 67 | wall | Narrative | Which phrases in CFPB narratives predict escalation | 4 | 3 | 4 | 3 | **144** | unscored | The text exists; the outcome to predict does not, and the corpus is contaminated. | 3.83M narratives available, but the only outcome fields are COMPANY_RESPONSE / IS_TIMELY / IS_CLOSED - no litigation or referral flag. The 27,510-copy templated texts contaminate any text model. |
| 44 | 10 | wall | Structure | Which nursing-home parent company is the highest-centrality node | 2 | 4 | 4 | 4 | **128** | unscored | In a chain-to-facility star graph, 'centrality' IS facility count - the question answers itself. | Chain data is healthy (636 chains, 572 with 5+ facilities); the graph structure is the weak part, not the data. |
| 45 | 11 | wall | Structure | Which member of Congress is the bridge node in the cosponsorship network | 4 | 5 | 2 | 3 | **120** | unscored | Coalition-holders are a real structural mechanism, but nobody is harmed by the answer. | Clean: 367,735 cosponsorships, 635 members, 29,211 bills, dates present. Congress 118-119 only. |
| 46 | 29 | wall | Contagion | A bill spreading through the cosponsorship network - who catches it, who is immune | 4 | 5 | 2 | 3 | **120** | unscored | Clean diffusion data, but the outcome does not name a harmed person. | None. 367,735 cosponsorships with dates, original/withdrawn flags, 29,211 bills. |
| 47 | 45 | wall | Causal | Does committee assignment cause donation shifts - money arriving after the seat | 5 | 2 | 4 | 3 | **120** | unscored | There is no 'after the seat' to measure. | BLOCKED: committee membership has no dates and no congress number - a current snapshot only. |
| 48 | 47 | wall | Temporal | One facility's fine history as a plain line up-and-right for a decade | 2 | 3 | 4 | 5 | **120** | unscored | A single line is a receipt, not a map - and there is no decade. | Penalties span 3 years; deficiencies are only real from 2023 (273 rows in 2017 vs 121,925 in 2024). |
| 49 | 63 | wall | Community | Congressional voting communities ignoring party labels | 4 | 5 | 2 | 3 | **120** | unscored | Defection structure is real; nobody is harmed by the answer. | None. 945,523 votes, 3,364 rollcalls, 639 members, party present. |
| 50 | E15 | expansion | Contagion | Do nursing homes connected by shared clinicians behave alike | 5 | 2 | 4 | 3 | **120** | unscored | Good idea, verified too sparse to carry it. | BLOCKED: only 273 facility pairs share 5+ clinicians in the nursing-home slice (40,841 of 2.26M affiliation links), and the affiliation table has no dates. |
| 51 | 62 | wall | Community | Shell-company clusters as tight communities in the ownership graph | 4 | 3 | 3 | 3 | **108** | unscored | A real graph, disconnected from any US harm. | ICIJ relationships is 3,339,267 edges over 1,131,496 start nodes and 14 relationship types - but offshore-leaks only, mostly pre-2017, with no verified wire into a US harm dataset. |
| 52 | 64 | wall | Community | Do CFPB complainants form communities - organised campaigns | 4 | 3 | 3 | 3 | **108** | unscored | There is no complainant identity, so this collapses into #23. | CFPB publishes no filer ID; the only proxies are ZIP (36,538 values) and the narrative text itself. |
| 53 | 39 | wall | Flow | Executives moving between violating companies ahead of enforcement | 5 | 2 | 5 | 2 | **100** | unscored | Strong mechanism with no dated people-to-org history anywhere in the warehouse. | BLOCKED: only ICIJ officers (771,315, offshore-only), IRS 527 directors/officers (189,593), and CMS FACILITY_AFFILIATION (2.26M NPI-to-CCN links, NO dates - snapshot only). |
| 54 | 43 | wall | Causal | Do ownership changes cause fine-rate changes at nursing homes (diff-in-diff) | 5 | 2 | 5 | 2 | **100** | unscored | Textbook design, no treatment events to point it at. | BLOCKED: same dead ownership-change flag as #17/#38. See E10 - the identical study IS runnable on mines. |
| 55 | 66 | wall | Narrative | Inspection-note language as topics over time | 4 | 2 | 4 | 3 | **96** | unscored | The 'inspection notes' are not notes. | BLOCKED: 418,479 deficiency rows carry only 260 distinct DEFICIENCY_DESCRIPTION values across 277 tag numbers, avg 118 chars - it is the canned federal tag label, repeated. NOTE: MSHA accident NARRATIVE is the live substitute (273,621 real prose rows, avg 189 chars, 2000-2026, 2 blank). |
| 56 | 38 | wall | Flow | Ownership churn as a flow map - nursing homes moving between parents over a decade | 4 | 2 | 5 | 2 | **80** | unscored | There is no decade and there is no churn record. | BLOCKED: CHAIN_NAME is one snapshot; the change flag is dead ('N' on all 14,700 rows). Same blocker as #17/#43. |
| 57 | 20 | wall | Phase | At what date does the politics spine percolate into one mesh | 3 | 3 | 2 | 4 | **72** | unscored | The answer is already known and it is an artefact: money, votes and cosponsorships all start in 2023 because that is when the loaders pulled. | Not a defect, but the finding would describe the ingest, not the institution. |
| 58 | 21 | wall | Surprise | The whole warehouse coloured by entropy - noisy chaos vs suspiciously orderly regions | 3 | 3 | 2 | 4 | **72** | unscored | Maps the warehouse, not the harm. | COLUMN_HEALTH covers 8,613 columns across only 247 of ~4,800 tables (5%), from a stale 2026-07-28 run. |
| 59 | 27 | wall | Contagion | Removing one parent company - the trophic cascade, what dies downstream | 3 | 3 | 4 | 2 | **72** | unscored | As written it is a simulation without a dependency structure; nothing actually 'dies' when a chain is deleted. | No structural blocker, but no downstream-dependency data to cascade through either. |
| 60 | 34 | wall | Compression | Members of Congress plotted by voting behaviour alone | 3 | 4 | 2 | 3 | **72** | unscored | DW-NOMINATE already exists and is literally a column in the members table; this re-treads it. | 945,523 votes, 3,364 rollcalls, 639 members. NOMINATE dims present but population unverified (modern rows sampled as empty strings). |
| 61 | 57 | wall | Prediction | A facility's projected trajectory as a dotted line | 2 | 3 | 3 | 4 | **72** | unscored | Extrapolation is not a mechanism. | 3-year window is thin for projection. |
| 62 | 61 | wall | Community | The donor network as visible cliques - coordinated blocks, not individuals | 4 | 3 | 3 | 2 | **72** | unscored | Coordination is a real mechanism; identity and scale are the problem. | Donor identity is name+ZIP (CORROBORATED tier, not a hard ID); pairwise co-giving over 84.2M rows is the real cost. |
| 63 | 71 | wall | Combo | Density + Temporal - a heatmap that breathes | 2 | 4 | 3 | 3 | **72** | unscored | A presentation upgrade of #1/#2/#3, not a new question. | Inherits the 2023-2026 window from its components. |
| 64 | 73 | wall | Combo | Anomaly + Structure - is the weirdest record also a high-centrality node | 4 | 2 | 3 | 3 | **72** | unscored | FLAGGED per brief: both components score low - #8 is blocked (D=2) and #52 is mechanism-poor (M=2). | Inherits #8's broken domain taxonomy for the centrality half. |
| 65 | 8 | wall | Structure | Which single entity is the hidden bridge between two domains nobody connects | 4 | 2 | 3 | 3 | **72** | unscored | The premise does not survive contact with the taxonomy. | BLOCKED: ENTITY_INDEX has only 5 domain labels and 78% is 'other'; just 105,724 of 33.2M entities (0.32%) span two domains and none span three. |
| 66 | 1 | wall | Density | FEC donor money as a national heat surface | 2 | 4 | 2 | 4 | **64** | unscored | Where giving is thick mostly recovers where people and money already are; population is the confound. | Money window is 2023-2026 only (99.99% of 84.2M rows); 3 rows carry a year-3312 date. |
| 67 | 28 | wall | Contagion | Do OSHA violations spread through industries like an epidemic | 4 | 2 | 4 | 2 | **64** | unscored | Good shape, wrong dataset present. | BLOCKED: there are NO OSHA violations in the warehouse - only ITA injury summaries (2023/24/25) and case details. The inspections re-pull is mid-flight at roughly 300k of ~4.5M rows and rate-limited. |
| 68 | 52 | wall | Anomaly | Which one donor visibly pops out of an otherwise normal cluster | 2 | 4 | 2 | 4 | **64** | unscored | One dot is a receipt, not a map - this is the scope-law failure mode in wonder form. | Data fine; the question is the problem. |
| 69 | 25 | wall | Surprise | Where does FDA adverse-event reporting become uniform - the batch-filed signature | 4 | 1 | 5 | 3 | **60** | unscored | Would be a strong finding on an intact corpus. | BLOCKED: FAERS column shift verified live - FDA_DT holds report codes 'EXP'/'PER'/'DIR' on 4.27M rows, GNDR_COD holds Y/N on 4.28M rows, and FAERS_DRUG shifts from DRUG_SEQ onward. The shift is in LANDING too, so it is an ingest defect. |
| 70 | 36 | wall | Compression | Do donor giving patterns compress into a small set of archetypes | 3 | 3 | 2 | 3 | **54** | unscored | The occupation axis is mostly empty exactly where the money is. | 61.6% of the 84.2M rows say RETIRED or NOT EMPLOYED; the blank-occupation bucket is only 2.7M rows but carries the largest dollar total ($5.2B). |
| 71 | 58 | wall | Prediction | Which companies the model flags as next to appear in CFPB data | 3 | 3 | 3 | 2 | **54** | unscored | 'Lookalikes' need attributes to look alike on. | CFPB carries company NAME only - no EIN, no LEI. A firm-attribute crosswalk would have to be built first. |
| 72 | 9 | wall | Structure | Which ZIP codes are load-bearing across domains | 3 | 3 | 2 | 3 | **54** | unscored | Geography as connector is real, but ZIP-level bridging mostly restates population density. | No ZIP-keyed edge tier exists; the GEO tier is 353 edges, mostly state grain. |
| 73 | 42 | wall | Causal | Regulator staffing cuts lined up against the violation rate right after | 5 | 1 | 5 | 2 | **50** | unscored | The best causal question on the wall, and the warehouse has no staffing data at all. | DEAD: nothing under OPM / FedScope / workforce / staffing / appropriations. USAspending agency aggregates are awards, not headcount. |
| 74 | 15 | wall | Phase | Watching MSHA + OSHA + CFPB become one regulatory system | 4 | 2 | 3 | 2 | **48** | unscored | Compelling frame, no seam to sew it on. | BLOCKED: no verified key joins the three. MSHA keys on MINE_ID/CONTROLLER_ID, OSHA ITA on EIN (64% populated, min length 1 = junk), CFPB on company NAME only (no EIN, no LEI). |
| 75 | 4 | wall | Density | MSHA violations clustering around inspectors' territories | 4 | 1 | 4 | 3 | **48** | unscored | Good mechanism, no data: territory-following heat would be a strong finding if it could be measured. | DEAD: no inspector identifier exists in any MSHA table (violations carry EVENT_NO / VIOLATION_NO / MINE_ID / CONTROLLER_ID / VIOLATOR_ID only). |
| 76 | 46 | wall | Causal | Do CFPB spikes cause policy changes, or just precede press releases | 4 | 2 | 3 | 2 | **48** | unscored | The effect side of the causal claim has no data. | BLOCKED: no corporate policy-change or press-release corpus exists in the warehouse. |
| 77 | 6 | wall | Density | The 338K portal datasets as a density map by topic - where are the data deserts | 3 | 2 | 2 | 4 | **48** | unscored | Absence-as-evidence is a real meta-mechanism, but this would measure the crawler, not the world. | BLOCKED: the index is a capped crawl - five portals sit at exactly 25,000 rows and two at exactly 10,000; 259,869 of 338,520 (76.8%) expose no column metadata. |
| 78 | 60 | wall | Prediction | Which open lead-queue items a scoring model would rank first | 2 | 4 | 2 | 3 | **48** | unscored | Points at the platform's own backlog, not the world. | Verified: LIBRARY_MARTS.REVIEW.LEAD_QUEUE holds 17,306 rows. |
| 79 | 32 | wall | Compression | All the spine tables squashed to 2D - do entities collapse into unnamed types | 3 | 3 | 2 | 2 | **36** | unscored | The features are too thin to embed meaningfully. | ENTITY_INDEX is 84.4M rows now (the 12.88M figure on the wall is stale) but carries only entity_type, key_type, source_table, domain, row_count. |
| 80 | 49 | wall | Temporal | One drug's adverse-event line across its whole market life | 2 | 1 | 4 | 4 | **32** | unscored | Descriptive, and on the corrupted corpus. | BLOCKED: FAERS column shift (see #25). |
| 81 | 50 | wall | Temporal | A member's fundraising rhythm across a whole career | 2 | 2 | 2 | 4 | **32** | unscored | There is no career in this data. | BLOCKED: FEC individual contributions are 99.99% inside 2023-2026 (2023: 18.1M rows, 2024: 40.1M, 2025: 21.0M, 2026: 5.0M). Every prior year combined is under 9,000 rows. |
| 82 | 69 | wall | Narrative | Do patient-filed and company-filed adverse-event reports use different dialects | 4 | 1 | 4 | 2 | **32** | unscored | Two blockers at once. | BLOCKED: FAERS has no narrative text at all, and the reporter-type column (OCCP_COD) is one of the displaced columns. |
| 83 | 5 | wall | Density | FDA adverse-event density per drug class over time | 3 | 1 | 5 | 2 | **30** | unscored | Consequential question sitting on a corrupted corpus with no class mapping. | BLOCKED x2: FAERS is column-shifted (verified live in landing AND marts), and no drug-class lookup table exists. |
| 84 | 31 | wall | Contagion | A single enforcement action propagating through the spine, as animation | 3 | 3 | 3 | 1 | **27** | unscored | The animation is the deliverable here, not the finding. | No blocker; needs an engine that does not exist. |
| 85 | 16 | wall | Phase | At what similarity threshold does the donor network snap into one continent | 4 | 3 | 2 | 1 | **24** | unscored | Real percolation question; the cost is pairwise over 84.2M rows. | Data present; scale is the blocker, not readiness. |
| 86 | 35 | wall | Compression | The 96 portals compressed by what they publish - which are near-duplicates | 2 | 2 | 2 | 3 | **24** | unscored | Would compress crawl coverage, not publishing behaviour. | BLOCKED: same crawl caps and 76.8% missing column metadata as #6/#13. |
| 87 | 70 | wall | Narrative | The sentiment arc of enforcement documents across an administration | 3 | 2 | 2 | 2 | **24** | unscored | No dated document corpus to arc. | The candidates (EPA NPDES single-event violation comments, SDWA visit comments) are short operational notes, not documents; cross-administration coverage unverified. |
| 88 | 68 | wall | Narrative | Bill-text similarity across states - model legislation spreading | 5 | 1 | 4 | 1 | **20** | unscored | A first-class systemic mechanism with zero data behind it. | DEAD: no state legislation exists in the warehouse at all, and federal bills carry only TITLE (avg 69 chars) plus LATEST_ACTION_TEXT - not bill text. Requires a new ingest. |
| 89 | 19 | wall | Phase | Would TDA find a hole in the political money network | 3 | 3 | 2 | 1 | **18** | unscored | A 'void' needs a defined metric space and an interpretation; high risk of an unreadable result. | No blocker, but new math and no guarantee of a legible answer. |
| 90 | 54 | wall | Anomaly | Which single FEC filing is the weirdest in the whole corpus | 1 | 4 | 1 | 4 | **16** | unscored | Explicitly 'just to see' - no mechanism, no person. | None; the question has no destination. |
| 91 | 13 | wall | Structure | Which of the 96 portals is the centrality king of the portal index | 2 | 2 | 1 | 3 | **12** | unscored | Would measure crawl luck, not publishing behaviour. | BLOCKED: same crawl caps as #6; with-columns coverage is wildly uneven (Open Data DC 6,267/10,000 vs UK 0/25,000). |
| 92 | 56 | wall | Anomaly | Which member's single most out-of-character vote of their career | 1 | 4 | 1 | 3 | **12** | unscored | One dot off a line; no mechanism. | Congress 118-119 only, so 'career' is two terms. |
| 93 | 51 | wall | Temporal | The warehouse itself over time - the organism growing | 1 | 2 | 1 | 4 | **8** | unscored | The curve would measure rebuild history, not growth. | Table CREATED dates span only 2026-06 / 07 / 08 (793 / 1,281 / 847 tables) and reset on rebuild. TABLE_VITALS is a single 2026-07-28 run, not a series. |

---

## Method note

- Data readiness was verified with 9 batches of live queries against `LIBRARY_MARTS`, `LIBRARY_RAW`, `LIBRARY_META` and `LIBRARY_META.REGISTRY` on 2026-08-22 — row counts, null and blank rates, distinct-value counts, date ranges, key-coverage joins, and value samples. No D score was assigned from a table name.
- Per the standing rule, no column was accepted as a real key on a null check alone; every key claim here is paired with a distinct count and a value sample.
- Novelty is deliberately left `unscored` on every row so the tabled "Pie in the Sky" project can join on it later.
- Expansion wonders were generated only in the three lenses that scored highest on M × D × C among the original 75 (Surprise, Causal, Contagion), and only against tables verified healthy during the readiness pass.

*Generated 2026-08-22.*


---

---

# Part 7 — The v2 idea inventory

A second, bigger docket pass than Part 4's 542. Where Part 4 asks
"is someone cheating," this one asks "what would a stranger stop and
stare at." 392 ideas, three tiers — crawl (one table, one chart), walk
(two tables), run (a chain). Merged from `docket/docket_v2_2026-09-07.csv`.

```
tier      count   shape
crawl       277   one table, one chart
walk         92   two tables, one join
run          23   a chain, three or more
```

## How v1 and v2 overlap, and where they don't

v1: `docket/docket.csv`, 150 lines, read only after v2 was written.
v2: `docket/docket_v2_2026-09-07.csv`, 392 lines.

```
v1 status            count      v1 shape        v2 shape
not started             69      fraud crosses   charts, cards, stories
found something         24      two-table hits  crawl 277 / walk 92 / run 23
nothing there           22      dead ends kept  no scores, no status
part done / a little    32
```

The two dockets ask different questions.
v1 asks "is someone cheating." v2 asks "what would a stranger stare at."
Overlap is real but smaller than the table overlap suggests.

## Both found it

| v1 | v2 title | Note |
|---|---|---|
| 2, 30, 133, E44 nursing home owners and fines | Deficiencies by nursing home ownership; Nursing home chain scorecard | v1 has a 5x finding already |
| 4, E37, E39, E57, E71 paid to prescribe | Paid doctors and what they prescribe; Opioid makers and opioid prescribers | v1 mart HEALTH__ADDICTION_PRESCRIBERS_PAID exists |
| 7, 25, E69 community health centers | Health center staff on the ban list | v1 built HEALTH__FQHC_SITE_PEOPLE |
| 8, E52, E67 jail and overdose | Overdose and jail, worst-tenth counties; Jail rate against injury deaths | v1 built JUSTICE__COUNTY_DOUBLE_BURDEN |
| 11, E59, E68, 124 hospital money and quality | Hospital stars against hospital margin; Hospital profit margin against charity care; Nonprofit hospital executive pay | |
| 15, E49, E66, 80 banned vendors still paid | Banned vendors still getting contracts | |
| 22, 131, 127 redlining today | Redlined then, denied now | v1 says found something on toxic sites |
| 23, 10 equipment suppliers | Equipment suppliers: charged versus paid | |
| 27, E41 banned doctors still ordering | Eligible to refer, enrolled or not; Where banned providers were practicing | |
| 31, 74 home health ownership | Private equity in home care | |
| 77, 95 judges' holdings and gifts | Judges' stock holdings; Gifts to federal judges; Judges' gifts against their positions | |
| 78, A35, 91 senators trading what they oversee | Senators trading in what they oversee | both need a ticker-to-industry lookup |
| 84, 85, A36 money at Medicare overseers | Outside money for and against; Follow the money | v1 has the $586M number |
| 86 Google political ads | Google political ads: who they target | |
| 88 people running 527s and campaigns | People on many dark-money boards | |
| 99, 115 mines, fines, accidents | Violations against accidents per mine | both blocked on MSHA edges |
| 101, 96 flood maps and insurance | Flood insurance map | |
| 105 crossings hit again | Crossings with no warning | |
| 106, 107 the pill flood then and now | Pills shipped per county; Pills shipped against deaths; The opioid chain | |
| 109 fast-track devices and deaths | Fast-track versus full device approvals; Device life story | |
| 112 retractions and grants | NIH grants against retractions | |
| 117, E75 nursing homes and relief money | Nursing home relief money by chain | v1 built the table |
| 122 sanctioned UK controllers | Sanctioned names in UK filings | |
| 129 complaints before recalls | Complaints before recalls | |
| 137 sanctioned ships at port | Ships per owner against port calls | |
| 139 gun dealers and deaths | Gun dealers per county; Gun dealers against background checks | |
| 140 who owns dirty plants | Plant emissions against plant owner; Who owns the generators | |
| 141 outages and rates | Outages against smart meters; Revenue per customer; Outage minutes by utility | |
| 144 immigration judges | Court outcome against custody | v1 knows the FOIA file with judge codes |
| E38, E42 opt-outs and dead doctors still paid | Doctors who quit Medicare | v2 has the single-table half only |
| E43, E47, E48 hospitals before sale, conversion, closure | Facilities in many programs; Hospital profit margin against charity care | v1 has 13 years of HCRIS |
| E62 sprinkler checkbox that lies | Fire-safety citations versus health citations | |

## Only in v2

Whole shelves v1 never touched:

- **Single-table wow charts**: ARCOS map, ship tracks, tree of life, place names, earthquakes, slave voyage flows, redlining descriptions, offshore leaks graph, Congress polarization, 5-4 decisions, citation web
- **Cards**: one doctor, one member, one judge, one company, one nonprofit, one facility, one utility, one county, one country
- **JUSTICE**: fifty years of federal court, sentence length by district, reversal rate by circuit, justice agreement matrix, judges' spouses, debts, travel, law schools
- **POLITICS**: Texas lobby restaurants, California lobby firms, Canada's 12.6M donations, UN vote alignment, Freedom House, cannabis map, NYC five cycles, revolving-door lobbyists
- **ENVIRONMENT**: your tap water by zip, lead at the tap, dam hazard, orphaned wells, trade-secret frack chemicals, admitted permit deviations, Coast Guard spill calls, environmental defenders killed
- **ENERGY**: turbines getting taller, battery boom, coal retirements, smart meters, net metering, world electricity mix
- **IMMIGRATION**: days in detention, bond by facility, detainer flags, H-1B sponsors and lawyers, USCIS backlog
- **ECONOMICS / FINANCE**: debt every day, Treasury daily cash, bank deserts, small-donor share, donor employers, 13F ownership, insider selling, audit partners, GLEIF refusals, PPP by franchise
- **Meta**: what years the warehouse covers, table sizes treemap, two Senate trade sources disagreeing, two missile trackers disagreeing
- **Text as data**: mine accident narratives, OSHA injury narratives, WPA interviews, oral argument transcripts, redlining descriptions

## Only in v1, and whether they hold up

| v1 | Holds up? | Why |
|---|---|---|
| 1 banned doctors on hospice paperwork | yes | NPI, CCN; partly done, 4 found |
| 3, 17, 123 banks financing polluters | no | v1 ruled it out; found only banks' own buildings |
| 5 loan terms after disasters | maybe | HMDA is 2015-17 and FEMA is a 12% partial |
| 6 rural dialysis monopolies | yes | CMS_DIALYSIS plus DIM_COUNTY on FIPS |
| 9, E54 polluters and low wages | weak | v1 says nothing there; QCEW is county not plant |
| 12 LTCH ventilator billing | thin | LTCH is 311 rows |
| 13 renaming after fire fines | dup | v1 marks it same as 30 |
| 14 fake rural clinics | no | v1 says nothing there |
| 16, 24 diabetes and ambulatory program rosters | no | rosters only, nothing to measure |
| 18, 108, 113 royalty surgeons and recalled or sued devices | yes | Open Payments has royalty rows; MDL table for 113 |
| 19, E56 quality bonus and industry money | no | v1 says nothing there twice |
| 20, E46 same people running homes and dialysis | weak | found a little |
| 21 hospital wages vs local | weak | QCEW industry rows; no hospital key |
| 26, 97, E72 empty subsidized housing after storms | weak | v1 mixed; FEMA partial |
| 28 nursing homes exaggerating sickness | yes | MDS frequency table is there, 31M rows |
| 29, E61 hospitals near pollution failing | weak | found a little; spatial join |
| 76, 81 executives selling before bad news | yes | insider tables plus PBGC; needs CIK for sponsors |
| 79 auditor switch before failure | yes | PCAOB plus FDIC failed banks; FDIC_CERT no edges |
| 82 unions with missing money and a PAC | maybe | OLMS plus FEC committees; name match only |
| 83 lobbying before rules | yes | LDA filings plus Federal Register; issue code to rule is manual |
| 87 foreign lobbyists donating | yes | FARA_BULK is in FOREIGN_INFLUENCE; name match |
| 89 state lobbyists donating federally | yes | TX and CA lobby plus FEC indiv; name match |
| 90 revolving door and contracts | maybe | Revolving Door Project is 405 rows |
| 92, A34 House office spending | dead | FED_HOUSE_DISBURSEMENTS not in inventory |
| 93 rejected mail ballots and jail | yes | EAVS plus Vera on FIPS; EAVS columns need decoding |
| 94 judges' politics and rulings | yes | affiliations, SCDB votes, CL_PERSON_ID |
| 98 nursing homes below bad dams | yes | NID has coordinates; spatial |
| 100 shell companies after disasters | weak | USASpending mart is 6.3M actions, not full |
| 102 fracking counties and water | yes | FracFocus plus SDWA on FIPS |
| 103 spillers winning contracts | maybe | NRC plus USASpending; name match |
| 104 shell-owned aircraft and crashes | yes | FAA registry plus NTSB on tail number |
| 110 generic price spikes | yes | NADAC plus Part D drug table on drug name |
| 111 tribal facilities losing hospitals | yes | IHS plus hospital enrollments; spatial |
| 114 rising injuries, no inspection | yes | 300A three years plus OSHA inspections; EIN |
| 116 visa sponsors underpaying and unsafe | yes | OFLC plus OSHA; name match |
| 118, 128 SBA lenders and bank enforcement | maybe | needs FDIC_CERT bridge |
| 119 detention cost per person per day | thin | USASpending mart plus stints; vendor name |
| 120 detainers and jail | yes | detainers plus Vera on FIPS |
| 121 leak names among doctors and donors | yes | ICIJ officers against NPPES and FEC indiv; name |
| 125 revoked 527s still filing | yes | IRS revocation plus 8872 reports on EIN |
| 126 lender complaints before enforcement | yes | CFPB complaints plus FDIC orders; name |
| 130 expiring contracts in gentrifying areas | yes | Section 8 plus HPI on FIPS |
| 132 bankruptcy after disaster | yes | IDB bankruptcy plus storms on FIPS |
| 134 convicted but never banned | maybe | IDB criminal plus LEIE; name |
| 135 ransomware and care quality | yes | ransomware victims plus Hospital Compare; name |
| 136 tech vendors with known flaws | thin | KEV lists vendors not companies |
| 138 police killings and grants | dead | assistance table not in inventory |
| 142 spikes without violations | dead | CAMPD daily not in inventory |
| 143 trial investigators paid to promote | yes | ClinicalTrials plus Open Payments; name |
| A32, A33, A37 fraud money and donors | yes | LEIE, SAM, sanctions against FEC indiv; name |
| E32 to E36, E45, E50, E53, E55, E58, E60, E63 to E65, E70, E73 | done | v1 already ran them; keep the verdicts |
| E40 new doctors billing wound care | yes | found something; NPPES plus Part B |

## Dead in the old one

Every "missing" table is a `LIBRARY_RAW.LANDING` table.
The inventory covers marts only, so absent from the inventory is not proof it is gone.
Split by whether a mart stands in for it:

```
raw table                              mart stand-in                              v1 lines
FED_DEA_ARCOS_FULL                     HEALTH__FED_DEA_ARCOS                      106 107
FED_CMS_PARTD_PRESCRIBER_DRUG          HEALTH__FED_CMS_PARTD_PRESCRIBERS          4 110
FED_CMS_NADAC                          HEALTH__FED_CMS_NADAC                      110
FED_CLINICALTRIALS_FULL                HEALTH__FED_CLINICALTRIALS                 143
FED_HRSA_PROVIDER_RELIEF_FUND          HEALTH__FED_HRSA_PROVIDER_RELIEF_FUND      E75
FED_IRS_990_EFILE_INDEX                ECONOMICS__FED_IRS_990_EFILE_INDEX         124
FED_DOL_FORM5500_FULL                  ECONOMICS__FED_DOL_FORM5500 (33K)          81
FED_FARA_BULK                          FOREIGN_INFLUENCE__FED_FARA_BULK           87
FED_NOAA_AIS                           MARITIME__FED_NOAA_AIS                     137
FED_VOTEVIEW_ROLLCALLS                 POLITICS__FED_VOTEVIEW_ROLLCALL_META       78
FED_GOVINFO_BILLSTATUS / COSPONSORS    POLITICS__FED_GOVINFO_*                    91
FED_SEC_13F_POSITIONS                  FINANCE__FED_SEC_13F_SUBMISSION            140
INTL_UN_CONSOLIDATED_SANCTIONS         JUSTICE__XC_UN_CONSOLIDATED_SANCTIONS_LIST A37
FED_USASPENDING_CONTRACTS_FULL_R2      ECONOMICS__FED_USASPENDING_CONTRACTS (6.3M) 15 80 90 100 103 119 136 E49 E70

no mart at all
FED_USASPENDING_ASSISTANCE_FULL        —                                          138 E64 E65 E66 E69
FED_HOUSE_DISBURSEMENTS                —                                          92 A34
FED_HOUSE_FD_PTR_INDEX                 —                                          A35
FED_EPA_CAMPD_EMISSIONS_DAILY          —                                          142
```

Nine v1 lines lean on a table with no mart. Those are the ones to call dead or re-load.
Whether the raw tables still exist in LANDING was not checked; that is a warehouse query, outside this pass.


---

## The v2 catalog, by subject

### Health — 65 ideas

| Tier | Title | Question | Why it matters | Tables | Joins on | Visual | Notes |
|---|---|---|---|---|---|---|---|
| crawl | **Pills shipped per county, the DEA ledger** | Which counties received the most opioid doses per resident, and in which years? | The reader sees their own county on a map of the flood. | HEALTH__FED_DEA_ARCOS | single table | map | 178M rows. Buyer address gives county. Morphine-equivalent column already there. |
| crawl | **Overdose deaths month by month, state by state** | Which states' overdose deaths kept climbing after the national peak? | The national curve hides states still getting worse. | HEALTH__FED_CDC_OVERDOSE | single table | timeline | Has a reporting-completeness column. Show it as a shaded band. |
| crawl | **Overdose death rate by county, year by year** | Where did the overdose wave start and where did it spread? | An animated map turns a statistic into a movement. | HEALTH__FED_CDC_DRUG_POISONING_COUNTY | single table | map | Rates are given as ranges, not points. Plot the midpoint and say so. |
| crawl | **Meals priced just under $125** | Which drug companies' meal payments bunch right under the reporting line? | Pattern that looks like someone gaming a rule. | HEALTH__PHARMA_MEAL_CAP_FINGERPRINT | single table | other | Already-built table. A histogram with a spike at $124 is the whole chart. |
| crawl | **Who pays doctors the most** | Which companies paid the most money to doctors, and for what? | The names are household brands. | HEALTH__FED_CMS_OPEN_PAYMENTS | single table | ranking | 15M rows. Also a by-manufacturer rollup in PUBLIC. |
| crawl | **Nursing home star ratings by owner type** | Do for-profit and chain-owned homes score worse than nonprofit ones? | Families pick homes by stars and never see who owns them. | HEALTH__FED_CMS_NURSING_HOME | single table | other | Ownership and chain columns in the same row as stars and fines. |
| crawl | **Private equity in home health** | What share of home health agencies have a private-equity or REIT owner, by state? | A quiet takeover of care for the elderly. | HEALTH__FED_CMS_HOME_HEALTH_OWNERS | single table | map | Entity-type column names PE, LLC, nonprofit, REIT outright. |
| crawl | **Nonprofit hospital executive pay** | Which nonprofit hospital officers earn the most, and how does pay compare to hospital revenue? | Charity status next to seven-figure salaries. | HEALTH__HOSPITAL_OFFICER_PAY | single table | ranking | Built from 990 filings. Hours-worked column lets you compute pay per hour. |
| crawl | **Hospital profit margin against charity care** | Do the most profitable hospitals give the least charity care? | The scatter answers a question people argue about. | HEALTH__FED_CMS_HCRIS | single table | other | One row per hospital per fiscal year, so it can animate. |
| crawl | **Dialysis clinic death rates by owner** | Do dialysis chains have higher patient death rates than independents? | Two companies run most of the country's dialysis. | HEALTH__FED_CMS_DIALYSIS | single table | ranking | Death rate, readmission, infection, transplant waitlist all in one row. |
| crawl | **Medical device recalls over time** | Which device makers recall the most, and are serious recalls rising? | Implants and pumps people carry in their bodies. | HEALTH__FED_FDA_DEVICE_ENFORCEMENT | single table | timeline | Recall class column gives severity. |
| crawl | **Device injury reports by maker** | Which devices show up most in injury and death reports since 2020? | The raw report count is a shock on its own. | HEALTH__FED_FDA_MAUDE | single table | ranking | 2020 onward only. |
| crawl | **Drug side-effect reports that ended in death** | Which reported outcomes dominate, and how did the report count grow by year? | Millions of reports nobody reads. | HEALTH__FED_FDA_FAERS_OUTC\|HEALTH__FED_FDA_FAERS_DEMO\|HEALTH__FED_FDA_FAERS_INDI | stack, same shape | timeline | Three tables share a report ID but that key is not in the join catalog. Treat each as single until proven. |
| crawl | **Clinical trials: who sponsors, where they run** | Which sponsors run the most trials, and which countries host them? | A world map of where medicine gets tested. | HEALTH__FED_CLINICALTRIALS | single table | map | 600K trials. Phase and status columns give a funnel too. |
| crawl | **Measles week by week, 2024** | Which states drove the 2024 measles count, week by week? | A disease that was gone coming back on a chart. | HEALTH__FED_CDC_NNDSS_WEEKLY_2024 | single table | timeline | 1.9M rows across all reportable diseases. Pick one disease per chart. |
| crawl | **Leading causes of death by state, 1999 to 2017** | Which cause of death rose fastest in each state? | Small multiples, one per state, tell fifty stories. | HEALTH__FED_CDC_LEADING_CAUSES_STATE | single table | timeline | Has national total rows. Filter them out or they dominate. |
| crawl | **Suicide rate by age group** | Which age groups' suicide rates rose most? | A quiet trend line that has been climbing for years. | HEALTH__FED_CDC_SUICIDE_RATES | single table | timeline |  |
| crawl | **Veteran suicide versus everyone else, by state** | Where is the veteran suicide rate furthest above the general rate? | Two lines per state, the gap is the story. | HEALTH__FED_VA_SUICIDE_STATE | single table | map | Comparison column already built in. |
| crawl | **Abortion counts by state, month by month** | How did monthly abortion counts shift between states after 2022? | Flows between states show up as one state falling and a neighbor rising. | HEALTH__XC_GUTTMACHER_MONTHLY_ABORTION | single table | timeline | Low-high range columns. Show the band. |
| crawl | **Doctors who quit Medicare** | Which specialties opt out of Medicare most, and is it growing? | A doctor shortage told through paperwork. | HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS | single table | ranking | Effective-date columns give the timeline. |
| crawl | **Banned from Medicare, by reason** | What gets people banned from billing Medicare, and how many come back? | Reinstatement column shows who returned. | HEALTH__FED_HHS_OIG_LEIE | single table | timeline |  |
| crawl | **Doctor shortage areas map** | Where are the worst primary-care shortage areas and how big are they? | The map of where you cannot get a doctor. | HEALTH__FED_HRSA_SHORTAGE_AREAS\|HEALTH__FED_HRSA_HPSA_PRIMARY_CARE | stack, same shape | map | Two tables overlap. Pick the full one. |
| crawl | **Opioid prescribing rate by specialty and state** | Which specialties and states prescribe opioids at the highest rate? | One column in one table, huge spread. | HEALTH__FED_CMS_PART_D_PRESCRIBERS | single table | ranking | Opioid and antipsychotic rate columns already computed. |
| crawl | **Brand versus generic drug prices** | How big is the brand-to-generic price gap for the same drug, and how did it move? | People pay it at the counter. | HEALTH__FED_CMS_NADAC | single table | timeline | Effective-date rows give a price history per drug. |
| crawl | **Marketplace deductibles by metal tier** | How much does a bronze deductible vary across plans and states? | Same tier, wildly different cost. | HEALTH__FED_CMS_MARKETPLACE_PLAN_ATTRIBUTES_PUF | single table | other |  |
| crawl | **The Prop 65 list growing** | How many chemicals were added to California's cancer list each year? | A list that only gets longer. | HEALTH__ST_OEHHA_PROPOSITION_65_LIST | single table | timeline |  |
| crawl | **Fast-track versus full device approvals** | How many devices cleared by 510(k) each year versus full PMA approval? | Most devices skip the hard review. | HEALTH__FED_FDA_DEVICE_510K\|HEALTH__FED_FDA_DEVICE_PMA | stack, same shape | timeline | Two tables, no join needed, same axis. |
| crawl | **Same diagnosis, different bill** | For one diagnosis code, how much do hospitals' charges vary across the country? | One number a patient can understand. | HEALTH__FED_CMS_MEDICARE_INPATIENT_HOSPITALS_BY_PROVIDER_AND_SERVICE | single table | other | DRG column. Pick a knee replacement or a heart attack. |
| crawl | **COVID relief money to providers** | Who got the most Provider Relief Fund money and where? | Pandemic money on a map. | HEALTH__FED_HRSA_PROVIDER_RELIEF_FUND | single table | map |  |
| crawl | **Equipment suppliers: charged versus paid** | Which medical-equipment suppliers bill Medicare far above what it pays? | The gap is the markup. | HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL | single table | ranking |  |
| crawl | **Nursing home fines by year** | Which homes were fined most, and are fines rising or falling? | Fine amounts next to payment-denial periods. | HEALTH__FED_CMS_NURSING_HOME_PENALTIES | single table | timeline |  |
| crawl | **Doctor quality scores spread** | How are Medicare quality scores distributed, and who gets penalized? | A bell curve with a cliff. | HEALTH__FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE | single table | other |  |
| crawl | **Indian Health Service facilities map** | Where are IHS, tribal and urban Indian health facilities, and what do they offer? | Coverage gaps are visible at a glance. | HEALTH__FED_IHS_FACILITIES\|HEALTH__FED_IHS_SCB_FACILITY | stack, same shape | map | Several tables shown side by side, no join. If a join is wanted, it is not in the catalog. |
| crawl | **Health insurance coverage by group over time** | Which demographic groups gained or lost coverage fastest? | Confidence ranges make the honest version. | HEALTH__FED_CDC_HEALTH_INSURANCE | single table | timeline |  |
| crawl | **Anxiety and depression by state and group** | Which groups reported the most anxiety and depression, and when did it peak? | A pandemic mood chart. | HEALTH__FED_CDC_ANXIETY_DEPRESSION | single table | timeline |  |
| crawl | **Life expectancy by country** | Which countries' life expectancy fell, and when? | A line that goes down is rare and gets attention. | HEALTH__XC_OWID_LIFE_EXPECTANCY | single table | timeline |  |
| crawl | **Nursing home relief money by chain** | Which nursing home chains got the most COVID relief, and how were they rated? | Already-built table, one chart away. | HEALTH__NURSING_HOME_RELIEF_BY_CHAIN | single table | ranking | 617 rows. Built table. |
| crawl | **Addiction prescribers and who paid them** | Which addiction-drug prescribers were paid by drug companies in 2022? | Built table, one scatter. | HEALTH__ADDICTION_PRESCRIBERS_PAID | single table | other | Built table. |
| crawl | **Health center staff on the ban list** | How many community-health-center clinicians are on the exclusion or opt-out lists? | Built table, already flagged. | HEALTH__FQHC_SITE_PEOPLE | single table | ranking | Built table. |
| crawl | **Providers per zip code** | Where are doctors dense and where are they absent? | Dots on a map of nine million providers. | HEALTH__FED_CMS_NPPES\|DIM_ZIP_POINT | ZIP | map | ZIP is a code key; catalog says code keys never bridge. Practice-address zip to DIM_ZIP_POINT is a plain lookup. |
| walk | **Paid doctors and what they prescribe** | Do doctors paid by a drug maker prescribe that maker's drugs more? | The question everyone asks about pharma money. | HEALTH__FED_CMS_OPEN_PAYMENTS\|HEALTH__FED_CMS_PARTD_PRESCRIBERS | NPI | other | Catalog item 1 and 2. Drug-level Part D table is 25M rows. |
| walk | **Opioid makers and opioid prescribers** | Which opioid prescribers took opioid-maker money? | Catalog item 2 verbatim. | HEALTH__FED_CMS_OPEN_PAYMENTS\|HEALTH__FED_CMS_PART_D_PRESCRIBERS | NPI | other |  |
| walk | **Deficiencies by nursing home ownership** | Do chain-owned homes get more inspection citations per home? | Catalog item 6. | HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES\|HEALTH__FED_CMS_NURSING_HOME | CCN | ranking |  |
| walk | **Citations per resident-day** | Which homes rack up the most citations per resident-day? | Catalog item 7, which normalizes big homes against small. | HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES\|HEALTH__FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY | CCN | ranking | MDS table is 31M rows. |
| walk | **Fire-safety citations versus health citations** | Do homes with many fire citations also have many health citations? | Two inspection regimes, one facility. | HEALTH__FED_CMS_NURSING_HOME_FIRE_DEFICIENCIES\|HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES | CCN | other |  |
| walk | **Hospital stars against hospital margin** | Do richer hospitals get better star ratings? | Money and quality on one scatter. | HEALTH__FED_CMS_HOSPITAL_COMPARE\|HEALTH__FED_CMS_HCRIS | CCN | other |  |
| walk | **Doctors affiliated with one-star hospitals** | Which doctors are tied to the lowest-rated hospitals? | Catalog item 9 family, CCN. | HEALTH__FED_CMS_FACILITY_AFFILIATION\|HEALTH__FED_CMS_HOSPITAL_COMPARE | CCN | other |  |
| walk | **Where banned providers were practicing** | Where did excluded providers practice, by specialty and state? | The ban list gets addresses. | HEALTH__FED_HHS_OIG_LEIE\|HEALTH__FED_CMS_NPPES | NPI | map |  |
| walk | **Contract-banned people still paid by pharma** | Did drug companies keep paying doctors on the federal do-not-do-business list? | A built table meets a payments table. | HEALTH__SAM_EXCLUDED_PROVIDERS\|HEALTH__FED_CMS_OPEN_PAYMENTS | NPI | ranking |  |
| walk | **Medicare billing against pharma payments** | Do the highest Medicare billers also take the most pharma money? | Catalog item 1 family. | HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER\|HEALTH__FED_CMS_OPEN_PAYMENTS | NPI | other |  |
| walk | **Part B pay against specialty peers by state** | Which doctors bill far above their specialty's state average? | Catalog item 3. | HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER\|HEALTH__FED_CMS_NPPES | NPI | ranking |  |
| walk | **Eligible to refer, enrolled or not** | How many order-and-referring doctors are not actually enrolled? | Catalog item 4. | HEALTH__FED_CMS_ORDER_AND_REFERRING\|HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT | NPI | other |  |
| walk | **Home health agencies per county resident** | Which counties have the most home health agencies per person? | Catalog item 5. | HEALTH__FED_CMS_HOME_HEALTH\|DIM_COUNTY | FIPS | map |  |
| walk | **Overdose deaths where doctors are scarce** | Do counties short on doctors have higher overdose death rates? | Catalog item 38. | HEALTH__FED_CDC_DRUG_POISONING_COUNTY\|HEALTH__FED_HRSA_SHORTAGE_AREAS | FIPS | map |  |
| walk | **Shortage areas against provider count** | Are designated shortage areas really short, by provider count? | Catalog item 41. | HEALTH__FED_HRSA_SHORTAGE_AREAS\|HEALTH__FED_CMS_NPPES | FIPS | map |  |
| walk | **Pills shipped against deaths, by county** | Did counties that got more pills see more overdose deaths? | Shipment and death on one county map. | HEALTH__FED_DEA_ARCOS\|HEALTH__FED_CDC_DRUG_POISONING_COUNTY | FIPS | map | FIPS family has 15 tables; confirm ARCOS is one before building. |
| walk | **Pharma money by specialty, rolled up** | Which specialties take the most pharma money per doctor? | Uses the pre-rolled PUBLIC table. | HEALTH_MEDICINE__OPEN_PAYMENTS_BY_SPECIALTY_STATE_AGG\|HEALTH_MEDICINE__NPPES_BY_TAXONOMY_STATE_AGG | state + specialty code | ranking | Both are rollups keyed by state and specialty; not a catalog key. |
| walk | **Pharma-paid doctors with malpractice records** | Do states with more pharma money have more malpractice payments? | NPDB is de-identified, so state level only. | HEALTH__FED_HRSA_NPDB\|HEALTH_MEDICINE__OPEN_PAYMENTS_BY_SPECIALTY_STATE_AGG | state code | other | State is not a catalog key. Lookup only. |
| walk | **Health-center clinics against shortage areas** | Are federally funded clinics where the shortage areas are? | Two maps, one overlay. | HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES\|HEALTH__FED_HRSA_SHORTAGE_AREAS | FIPS | map |  |
| walk | **Facilities in many programs** | Which hospitals converted to Rural Emergency Hospitals and what did they look like before? | Enrollment table has the conversion flag. | HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS\|HEALTH__FED_CMS_POS_OTHER | CCN | timeline |  |
| run | **The opioid chain** | Can pills shipped, prescriptions written, pharma money, deaths, and treatment sites be laid on one county over twenty years? | The whole epidemic on one scrolling page. | HEALTH__FED_DEA_ARCOS\|HEALTH__FED_CMS_PART_D_PRESCRIBERS\|HEALTH__FED_CMS_OPEN_PAYMENTS\|HEALTH__FED_CDC_DRUG_POISONING_COUNTY\|HEALTH__FED_CMS_OPIOID_TREATMENT_PROGRAM_PROVIDERS\|HEALTH__ADDICTION_PRESCRIBERS_PAID | NPI, FIPS | other | Scrollytelling. Every join is a catalog key. |
| run | **Nursing home chain scorecard** | For each chain: homes, stars, citations, fines, relief money, owners? | One page per chain a family could use. | HEALTH__FED_CMS_NURSING_HOME\|HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES\|HEALTH__FED_CMS_NURSING_HOME_PENALTIES\|HEALTH__NURSING_HOME_RELIEF_BY_CHAIN\|HEALTH__FED_NURSINGHOME411 | CCN | other |  |
| run | **One doctor, every table** | For one NPI: registry, pharma money, prescribing, billing, bans, hospital ties? | A lookup page that shows the warehouse's reach. | HEALTH__FED_CMS_NPPES\|HEALTH__FED_CMS_OPEN_PAYMENTS\|HEALTH__FED_CMS_PART_D_PRESCRIBERS\|HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER\|HEALTH__FED_HHS_OIG_LEIE\|HEALTH__FED_CMS_FACILITY_AFFILIATION\|HEALTH__FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE | NPI | other | NPI is the steel key: 34 tables, 364 edges. |
| run | **Device life story** | From clearance to registry to injury report to recall, for one product code? | Follow one device through four FDA systems. | HEALTH__FED_FDA_DEVICE_510K\|HEALTH__FED_FDA_GUDID\|HEALTH__FED_FDA_MAUDE\|HEALTH__FED_FDA_DEVICE_ENFORCEMENT\|HEALTH__FED_FDA_DEVICE_CLASSIFICATION | product code | flow | Product code is not a catalog key. Needs proving. |
| run | **Private equity in home care** | Do PE-owned home health agencies score worse on care outcomes? | Owner list meets outcome list. | HEALTH__FED_CMS_HOME_HEALTH_OWNERS\|HEALTH__FED_CMS_HOME_HEALTH\|HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS | CCN | other |  |

### Politics — 53 ideas

| Tier | Title | Question | Why it matters | Tables | Joins on | Visual | Notes |
|---|---|---|---|---|---|---|---|
| crawl | **Congress drifting apart** | How far apart have the two parties' ideology scores moved since 1789? | The polarization chart, from the original source. | POLITICS__FED_VOTEVIEW_MEMBERS | single table | timeline | 51K member-Congress rows. |
| crawl | **Three branches, one axis** | How far apart do the House, Senate and Supreme Court sit each year? | One line per branch on one axis. | POLITICS__JCS_MEDIANS\|POLITICS__XC_JCS_MEDIANS | stack, same shape | timeline | XC version adds each circuit. |
| crawl | **Who actually passes bills** | Which members turn the most sponsored bills into law? | Rank by enactment rate, not by noise. | POLITICS__MEMBER_BILL_RECORD | single table | ranking | Built table. |
| crawl | **Missed votes and party loyalty** | Who misses the most votes, and who breaks with their party most? | Two numbers per member. | POLITICS__MEMBER_VOTING_RECORD | single table | other | Built table. |
| crawl | **Cosponsor web** | Which members cosponsor together, across the aisle? | A network graph of Congress. | POLITICS__FED_GOVINFO_BILL_COSPONSORS | single table | other | 1.27M rows. The BILLS-era table is a smaller sibling. |
| crawl | **Senators' stock trades** | Which senators trade most, and what did they buy before big news? | Trades on a timeline next to headlines. | POLITICS__SENATE_TRADES\|FINANCE__SENATE_TRADES | stack, same shape | timeline | FINANCE__SENATE_TRADES merges both sources with Bioguide. |
| crawl | **Margins of victory over time** | Are federal elections getting closer or more lopsided? | Every winner, every margin. | POLITICS__WHO_WON | single table | timeline |  |
| crawl | **Closest House races** | Which House seats were decided by the fewest votes? | Vote share by candidate, MIT-cleaned. | POLITICS__FED_MEDSL_HOUSE_RETURNS\|POLITICS__FED_MEDSL_SENATE_RETURNS\|POLITICS__FED_MEDSL_PRESIDENT_RETURNS | stack, same shape | map | Several tables shown side by side, no join. If a join is wanted, it is not in the catalog. |
| crawl | **Where Texas lobbyists buy dinner** | Which restaurants and which officials show up most on lobbyist meal reports? | A list of restaurants is a very human chart. | POLITICS__TX_LOBBY_FOOD_BEVERAGE | single table | ranking |  |
| crawl | **Texas lobby gifts, travel, events** | What do lobbyists give Texas officials, and who gets most? | Gifts, hotels, flights, receptions in one view. | POLITICS__TX_LOBBY_GIFTS\|POLITICS__TX_LOBBY_TRANSPORTATION\|POLITICS__TX_LOBBY_EVENTS\|POLITICS__TX_LOBBY_ENTERTAINMENT\|POLITICS__TX_LOBBY_AWARDS | stack, same shape | ranking | Same filer ID across tables; not a catalog key. |
| crawl | **Texas lobby spending by category over time** | How did total lobby spending split across meals, gifts, travel, media by year? | Cover sheets carry the totals. | POLITICS__TX_LOBBY_COVER | single table | timeline |  |
| crawl | **What Texas lobbyists work on** | Which subjects draw the most lobbying activity in Texas? | 210K subject rows, one bar chart. | POLITICS__TX_LOBBY_SUBJECT_MATTER | single table | ranking |  |
| crawl | **California's biggest lobby spenders** | Which employers pay the most for lobbying per session? | Quarter-by-quarter totals per employer. | POLITICS__CA_LOBBY_EMPLOYER\|POLITICS__CA_LOBBY_FIRM | stack, same shape | ranking | Several tables shown side by side, no join. If a join is wanted, it is not in the catalog. |
| crawl | **California lobbyists who also donate** | Which lobbyists give the most campaign money? | Lobby and donate in one row. | POLITICS__CA_LOBBY_CONTRIBUTIONS | single table | ranking |  |
| crawl | **People on many dark-money boards** | Which names sit on the most 527 organization filings? | Same names across dozens of groups. | POLITICS__IRS527_DIRECTORS_OFFICERS | single table | ranking |  |
| crawl | **Dark-money groups related to each other** | Which 527 groups declare each other as related? | A network of shells. | POLITICS__IRS527_RELATED_ENTITIES\|POLITICS__IRS527_8871_ORGS | stack, same shape | other | Several tables shown side by side, no join. If a join is wanted, it is not in the catalog. |
| crawl | **Canada's 12.6 million donations** | How did giving to each Canadian party move over time? | Bigger than most US state files. | POLITICS__INTL_ELECTIONS_CANADA_CONTRIBUTIONS | single table | timeline |  |
| crawl | **Freedom scores rising and falling** | Which countries lost the most freedom points in the last decade? | A world map that changes color. | POLITICS__INTL_FREEDOMHOUSE | single table | map |  |
| crawl | **Military spending by country** | Who spends most, and who grew fastest? | Ranking that moves over time. | POLITICS__INTL_OWID_MILSPEND | single table | timeline |  |
| crawl | **Who votes with whom at the UN** | Which countries vote with the US most and least, and how has that shifted? | A country-pair heatmap. | POLITICS__INTL_VOETEN_UNGA_VOTES | single table | other |  |
| crawl | **Corruption perception by country** | Which countries' corruption scores improved or fell most? | Simple, global, recognizable. | POLITICS__XC_OWID_CPI | single table | map |  |
| crawl | **Radio licenses by service type** | Where are FCC licenses densest, and what services dominate? | 1.7M licenses on a map. | POLITICS__FED_FCC_LICENSING\|GOVERNMENT_POWER__FCC_LICENSES_BY_STATE_SERVICE_AGG | stack, same shape | map | Rollup already exists in PUBLIC. |
| crawl | **How counties run elections** | Which jurisdictions rely most on mail ballots or fewest polling places? | One row per county, dozens of questions. | POLITICS__FED_EAC_EAVS | single table | map | Column names are survey codes. Needs a decoder. |
| crawl | **Judges' age at appointment by president** | Are presidents appointing younger judges over time? | A generational strategy in one chart. | POLITICS__FED_FJC_JUDGES\|POLITICS__FJC_APPOINTMENT | stack, same shape | timeline | Several tables shown side by side, no join. If a join is wanted, it is not in the catalog. |
| crawl | **Confirmation vote margins shrinking** | How did Senate confirmation margins for judges change by decade? | From unanimous to party-line. | POLITICS__FED_FJC_SERVICE | single table | timeline |  |
| crawl | **Circuit courts by ideology** | Which circuits lean furthest left or right, and did that change? | One dot per judge, one row per circuit. | POLITICS__JUDGE_IDEOLOGY_COA | single table | other |  |
| crawl | **Supreme Court justices by term** | How did each justice's ideology score move term by term? | The famous chart, from the source. | POLITICS__JUDGE_IDEOLOGY_SCOTUS | single table | timeline |  |
| crawl | **Cannabis legalization map by year** | When did each state approve medical and recreational cannabis? | An animated map of policy spreading. | POLITICS__ST_CANNABIS_POLICY_BUNDLES | single table | map | Dozens of rule columns for follow-ups. |
| crawl | **NYC donors, 2001 versus 2025** | How did the size and geography of NYC donations change across five cycles? | Five cycles, same city. | POLITICS__ST_NYC_CFB_CAMPAIGN_2001_CONTRIBUTION\|POLITICS__ST_NYC_CFB_CAMPAIGN_2009_CONTRIBUTION\|POLITICS__ST_NYC_CFB_CAMPAIGN_2013_CONTRIBUTION\|POLITICS__ST_NYC_CFB_CAMPAIGN_2021_CONTRIBUTIONS\|POLITICS__ST_NYC_CFB_CAMPAIGN_2025_CONTRIBUTIONS | stack, same shape | map | Same shape, stack them. |
| crawl | **Lobbyists who used to work in government** | What share of federal lobbyists held a covered government job first? | Revolving door, counted. | POLITICS__FED_SENATE_LDA_LOBBYIST_POSITIONS | single table | ranking |  |
| crawl | **Who pays to lobby Washington** | Which clients spend most on federal lobbying, and on what issues? | 820K filings, one ranking. | EDUCATION__FED_SENATE_LDA_FILINGS | single table | ranking | Table is misfiled under EDUCATION. |
| crawl | **Foreign agents by country** | Which foreign governments hire the most registered agents in the US? | A map of influence buying. | FOREIGN_INFLUENCE__FED_FARA_BULK | single table | map |  |
| crawl | **Google political ads: who they target** | Which advertisers target which age and gender, and how much did they spend weekly? | Targeting made visible. | EDUCATION__FED_GOOGLE_POLADS_CREATIVE_STATS\|EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_WEEKLY_SPEND | stack, same shape | timeline | Misfiled under EDUCATION. |
| crawl | **Federal Register output per agency** | Which agencies publish the most rules, and how did executive orders spike by year? | Government activity as a line. | REGULATORY__FED_FEDERAL_REGISTER_DOCUMENTS | single table | timeline |  |
| crawl | **Jobs with an industry interest** | Which federal roles have the most industries with a financial stake? | Small table, sharp question. | GOVERNANCE__FED_REVOLVINGDOOR_PROJECT | single table | ranking | 405 rows. |
| crawl | **Roll calls that split parties** | Which votes had the most members crossing party lines? | Vote-level drama. | POLITICS__VOTEVIEW_VOTES\|POLITICS__FED_VOTEVIEW_ROLLCALL_META | stack, same shape | ranking | Same roll-call ID; not a catalog key. |
| walk | **Cosponsoring and ideology** | Do moderates cosponsor more bills across the aisle? | Catalog item 46. | POLITICS__FED_GOVINFO_BILL_COSPONSORS\|POLITICS__FED_VOTEVIEW_MEMBERS | BIOGUIDE / ICPSR | other |  |
| walk | **Committee seats and bills sponsored** | Do members on more committees sponsor more bills? | Catalog item 47. | POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP\|POLITICS__BILLS | BIOGUIDE | other |  |
| walk | **Senators trading in what they oversee** | Do senators trade stocks in sectors their committees regulate? | The chart people will screenshot. | FINANCE__SENATE_TRADES\|POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP | BIOGUIDE | other | Sector needs a ticker-to-industry lookup; see wanted list. |
| walk | **Money raised versus margin won** | Does raising more money buy a bigger win? | Catalog FEC family. | POLITICS__FEC_CANDIDATE_SUMMARY\|POLITICS__WHO_WON\|POLITICS__FEC_CANDIDATE | FEC_CAND_ID | other |  |
| walk | **Individual money per committee per candidate** | Which candidates' committees run on small donors? | Catalog item 42. | FINANCE__FED_FEC_INDIV_CONTRIBUTIONS\|POLITICS__FEC_COMMITTEE\|POLITICS__FEC_CAND_CMTE_LINK | FEC_CMTE_ID / CAND_ID | ranking | 284M rows. Use the PUBLIC rollup first. Not a catalog key; lookup or unproven. |
| walk | **PAC money versus individual money** | Which committees lean on PACs rather than people? | Catalog item 43. | POLITICS__FED_FEC_PAC_SUMMARY\|MONEY_IN_POLITICS__FEC_INDIV_BY_CMTE_CYCLE_AGG | FEC_CMTE_ID | other |  |
| walk | **Leadership PACs per politician** | Which officeholders run the most leadership PACs and where does the money go? | Catalog item 44. | FINANCE__FED_FEC_LEADERSHIP_PAC\|FINANCE__FED_FEC_COMMITTEE_TO_CANDIDATE | FEC_CMTE_ID / CAND_ID | flow | Not a catalog key; lookup or unproven. |
| walk | **Outside money for and against** | Which candidates drew the most independent spending against them? | Support versus oppose in one bar. | FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES\|POLITICS__FEC_CANDIDATE | FEC_CAND_ID | ranking |  |
| walk | **PAC money and party loyalty** | Do members who take more PAC money vote with their party more? | Built member tables share the member key. | POLITICS__MEMBER_PAC_MONEY\|POLITICS__MEMBER_VOTING_RECORD\|POLITICS__MEMBER_SPINE | BIOGUIDE | other |  |
| walk | **Judge ideology by appointing president** | How far apart are each president's appointees on the ideology scale? | Presidents as color bands. | POLITICS__FJC_APPOINTMENT\|POLITICS__JUDGE_IDEOLOGY_COA | CL_PERSON_ID / FJC id | other | FJC id to ideology table key not in catalog; check. Not a catalog key; lookup or unproven. |
| walk | **Lobbying firms and their clients, California** | Which firms serve the most employers, and which employers hire the most firms? | A bipartite graph. | POLITICS__CA_LOBBY_EMPLOYER_FIRMS\|POLITICS__CA_LOBBY_FIRM_EMPLOYER | filer ID | other | Same source ID, not a catalog key. |
| walk | **Dark-money donors to dark-money groups** | Who gives the most to 527 groups, and which groups? | Schedule A meets the org roster. | FINANCE__FED_IRS527_SCHEDULE_A_CONTRIBUTIONS\|POLITICS__IRS527_8871_ORGS | EIN | ranking | EIN family, 34 tables; confirm both are in it. |
| walk | **Where 527 money gets spent** | Which vendors get paid most by 527 groups? | Schedule B is the spending side. | FINANCE__FED_IRS527_SCHEDULE_B_EXPENDITURES\|POLITICS__IRS527_8872_REPORTS | EIN | ranking |  |
| run | **One member of Congress, every table** | For one member: ideology, votes, bills, committees, money, trades, donors? | A card that proves the warehouse links up. | POLITICS__MEMBER_SPINE\|POLITICS__FED_VOTEVIEW_MEMBERS\|POLITICS__MEMBER_BILL_RECORD\|POLITICS__MEMBER_VOTING_RECORD\|POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP\|POLITICS__MEMBER_PAC_MONEY\|POLITICS__MEMBER_INDIV_DONATIONS\|FINANCE__SENATE_TRADES\|POLITICS__MEMBER_FEC_ID | BIOGUIDE, FEC_CAND_ID | other |  |
| run | **Follow the money** | From individual donor to committee to candidate to outside spending, as one flow? | A sankey of an election. | FINANCE__FED_FEC_INDIV_CONTRIBUTIONS\|FINANCE__FED_FEC_COMMITTEES\|FINANCE__FED_FEC_COMMITTEE_TO_CANDIDATE\|FINANCE__FED_FEC_CANDIDATES\|FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES | FEC_CMTE_ID, FEC_CAND_ID | flow |  |
| run | **Texas lobbying, whole picture** | Who spent what on which official, on which subject, for which client? | Six tables, one filer. | POLITICS__TX_LOBBY_COVER\|POLITICS__TX_LOBBY_FOOD_BEVERAGE\|POLITICS__TX_LOBBY_GIFTS\|POLITICS__TX_LOBBY_TRANSPORTATION\|POLITICS__TX_LOBBY_SUBJECT_MATTER\|POLITICS__TX_LOBBY_INDIVIDUAL_REPORTING | filer ID | other | Same-source filer ID, not a catalog key. |
| run | **Judicial confirmations against Senate polarization** | Did confirmation margins narrow as the Senate polarized, year by year? | Two long series on one axis. | POLITICS__FED_FJC_SERVICE\|POLITICS__FED_VOTEVIEW_MEMBERS\|REFERENCE__CALENDAR | year | timeline | Year is a lookup, not a catalog key. |

### Justice — 52 ideas

| Tier | Title | Question | Why it matters | Tables | Joins on | Visual | Notes |
|---|---|---|---|---|---|---|---|
| crawl | **Sentence length by charge and district** | Do the same federal charges get different prison time in different districts? | Same crime, different years behind bars. | JUSTICE__FED_FJC_IDB_CRIMINAL | single table | other | 6.3M defendants. |
| crawl | **What people sue about, by decade** | Which civil case types grew and shrank in federal court? | A stacked area of a country's grievances. | JUSTICE__FED_FJC_IDB_CIVIL | single table | timeline |  |
| crawl | **Bankruptcies per county per year** | Where did personal bankruptcy spike, and when? | A map that lights up in 2009. | JUSTICE__FED_FJC_IDB_BANKRUPTCY | single table | map | Chapter mix as a follow-up. |
| crawl | **Reversal rate by circuit** | Which appeals circuits overturn the most lower-court rulings? | One bar per circuit. | JUSTICE__FED_FJC_IDB_APPELLATE | single table | ranking |  |
| crawl | **Which justices vote together** | How often does each pair of justices agree, term by term? | The agreement matrix. | JUSTICE__FED_SCDB | single table | other |  |
| crawl | **5-4 decisions per term** | How many cases were decided by one vote each term? | A count that tracks the court's temperature. | JUSTICE__FED_SCDB | single table | timeline |  |
| crawl | **Most-cited opinions** | Which rulings get cited most, and who wrote them? | A leaderboard of law. | JUSTICE__FED_COURTLISTENER_OPINION_CLUSTERS | single table | ranking | 10M rows. |
| crawl | **Citation web** | Which opinions cite which, and where are the hubs? | A graph of precedent. | JUSTICE__FED_COURTLISTENER_PARENTHETICALS | single table | other | 6.4M citation rows. |
| crawl | **Gifts to federal judges** | Who gives judges gifts, and which judges get the most? | The disclosure forms, itemized. | JUSTICE__FED_COURTLISTENER_DISCLOSURE_GIFTS | single table | ranking |  |
| crawl | **Who pays for judges' travel** | Which organizations reimburse judges most, and for trips where? | Junkets on a map. | JUSTICE__FED_COURTLISTENER_DISCLOSURE_REIMBURSEMENTS | single table | ranking |  |
| crawl | **Judges' stock holdings** | Which companies show up most in judges' investment disclosures? | 1.9M holdings. | JUSTICE__FED_COURTLISTENER_INVESTMENTS | single table | ranking |  |
| crawl | **Judges' spouses' income sources** | Where do judges' spouses earn, by employer type? | A side of the bench nobody charts. | JUSTICE__FED_COURTLISTENER_DISCLOSURE_SPOUSAL_INCOME | single table | ranking |  |
| crawl | **Judges' debts** | Which creditors hold the most judge debt? | Debts on the record. | JUSTICE__FED_COURTLISTENER_DISCLOSURE_DEBTS | single table | ranking |  |
| crawl | **Law schools of the bench** | Which schools produce the most federal judges, by decade? | A ranking that changes slowly. | JUSTICE__FED_COURTLISTENER_JUDGE_EDUCATIONS\|JUSTICE__FED_COURTLISTENER_SCHOOLS | stack, same shape | timeline | School ID same-source; CL_PERSON_ID for judge. |
| crawl | **Party affiliation by court** | Which courts have swung party over time? | Affiliation periods as color bars. | JUSTICE__FED_COURTLISTENER_JUDGE_POLITICAL_AFFILIATIONS | single table | timeline |  |
| crawl | **Race and gender on the bench** | How did the bench's race and gender mix change per decade of appointment? | Slow change, visible. | JUSTICE__FED_COURTLISTENER_JUDGES\|JUSTICE__FED_COURTLISTENER_JUDGE_RACES\|POLITICS__FJC_JUDGE | CL_PERSON_ID | timeline |  |
| crawl | **Crimes solved, by state** | Which states clear the fewest reported crimes, and did it change since 1985? | Clearance rate is the number nobody quotes. | JUSTICE__FED_FBI_CDE | single table | map |  |
| crawl | **Gun background checks by month** | When did gun checks spike, state by state? | Spikes line up with news. | JUSTICE__FED_FBI_NICS_CHECKS | single table | timeline |  |
| crawl | **Gun dealers per county** | Where are licensed gun dealers densest per resident? | 77K dealers, every address. | JUSTICE__FED_ATF_FFL\|DIM_COUNTY | FIPS | map | FFL has coordinates; county via lookup. |
| crawl | **People killed by police** | How many per year, by race, armed status, and were officers charged? | Two trackers, one chart. | JUSTICE__XC_MAPPING_POLICE_VIOLENCE\|JUSTICE__XC_WAPO_FATAL_FORCE | stack, same shape | timeline | Different coverage; do not add them together. |
| crawl | **County jail rates over time** | Which counties' jail rates climbed most since 1970? | Vera's county trends, animated. | JUSTICE__XC_VERA_INCARCERATION_TRENDS | single table | map |  |
| crawl | **The racial jail gap by county** | Where is the Black-white jail rate gap widest? | Built table, one map. | JUSTICE__RACIAL_JAIL_DISPARITY | single table | map | Built table. |
| crawl | **Overdose and jail, worst-tenth counties** | Which counties are in the worst tenth for both overdose and jail? | Built table with the flag. | JUSTICE__COUNTY_DOUBLE_BURDEN | single table | map | Built table. |
| crawl | **Sanctioned ships** | Which sanctioned vessels exist, under which programs? | OFAC lists ship details. | JUSTICE__FED_OFAC_SDN | single table | ranking |  |
| crawl | **Thirteen blacklists in one** | Which entries appear on several federal screening lists? | Overlap counted. | JUSTICE__FED_CONSOLIDATED_SCREENING_LIST | single table | other |  |
| crawl | **A million sanctioned targets** | How does the global watchlist split by country, type, and crypto wallets? | Crypto wallets on a sanctions list is new. | JUSTICE__INTL_OPENSANCTIONS_DEFAULT | single table | other |  |
| crawl | **Exploited software flaws** | Which vendors' flaws get exploited most, and how many are ransomware-used? | Product names people recognize. | JUSTICE__FED_CISA_KEV | single table | ranking |  |
| crawl | **Ransomware gangs and their victims** | Which gangs claim the most victims, in which countries, by month? | Gang names on a timeline. | JUSTICE__XC_RANSOMWARELIVE_VICTIMS | single table | timeline |  |
| crawl | **Conflict deaths on a map** | Where did conflict events cluster, and how deadly, year by year? | 386K events. | JUSTICE__INTL_UCDP_GED | single table | map |  |
| crawl | **North Korean missile tests, two trackers** | Do the two trackers agree on count, type, and outcome? | Disagreement between sources is itself the chart. | JUSTICE__INTL_NTI_CNS_DPRK_MISSILE_TESTS\|JUSTICE__XC_NAGIX_DPRK_MISSILE_TESTS | stack, same shape | timeline | Several tables shown side by side, no join. If a join is wanted, it is not in the catalog. |
| crawl | **Human rights violations by country and article** | Which countries lose most at the European court, on which articles? | 2,000 rulings. | JUSTICE__INTL_HUDOC | single table | other |  |
| crawl | **Homicide, warheads, terrorism by country** | Three OWID series on one country page? | Simple world context. | JUSTICE__XC_OWID_HOMICIDE\|JUSTICE__XC_OWID_NUCLEAR_WARHEADS\|JUSTICE__XC_OWID_TERRORISM_DEATHS | country + year | timeline | Country code lookup. Not a catalog key; lookup or unproven. |
| crawl | **Missouri registry by county** | Where are registrants per resident highest, and what share are noncompliant? | A state registry, mapped. | JUSTICE__STATE_MO_SEX_OFFENDER_REGISTRY | single table | map | Names present. Aggregate only. |
| crawl | **FTC cases by topic** | What does the FTC go after, and did it shift? | 1,004 cases. | JUSTICE__FED_FTC_DATASETS | single table | timeline |  |
| crawl | **Biggest multidistrict lawsuits** | Which MDLs hold the most pending cases? | A ranking of mass litigation. | JUSTICE__FED_JPML_PENDING_MDLS | single table | ranking |  |
| crawl | **Bank enforcement fines** | Which banks were fined most by the FDIC, and when? | Bank names and dollar amounts. | JUSTICE__FED_FDIC_ENFORCEMENT_ORDERS | single table | timeline |  |
| crawl | **Oral argument transcripts** | Which judges talk most in oral argument, by word count? | Transcript text as data. | JUSTICE__FED_COURTLISTENER_ORAL_ARGUMENTS | single table | ranking | Transcript column where available. |
| crawl | **Courthouses map** | Where are federal courthouses, and which counties are far from one? | Distance-to-court map. | JUSTICE__FED_COURTLISTENER_COURTHOUSES\|DIM_COUNTY | FIPS | map |  |
| walk | **Judge positions against party** | Do judges with a party affiliation hold more outside positions? | Catalog item 48. | JUSTICE__FED_COURTLISTENER_POSITIONS\|JUSTICE__FED_COURTLISTENER_JUDGE_POLITICAL_AFFILIATIONS | CL_PERSON_ID | other |  |
| walk | **Disclosures per judge against positions held** | Which judges file the most disclosures relative to positions? | Catalog item 49. | JUSTICE__FED_COURTLISTENER_FINANCIAL_DISCLOSURES\|JUSTICE__FED_COURTLISTENER_POSITIONS | CL_PERSON_ID | other |  |
| walk | **Judges per court against cases filed** | Which courts are most overloaded per judge? | Catalog item 50. | JUSTICE__FED_COURTLISTENER_COURTS\|JUSTICE__FED_COURTLISTENER_FJC_IDB_CL_LINKED | CL_COURT_ID | ranking |  |
| walk | **Opinions per case by case type** | Which case types generate the most written opinions? | Catalog item 51. | JUSTICE__FED_COURTLISTENER_OPINION_CLUSTERS\|JUSTICE__FED_COURTLISTENER_FJC_IDB_CL_LINKED | DOCKET | other | DOCKET is mostly unproven: 17 tables, 2 edges. |
| walk | **Oral arguments against opinions** | Do argued cases get more opinions? | Catalog item 52. | JUSTICE__FED_COURTLISTENER_ORAL_ARGUMENTS\|JUSTICE__FED_COURTLISTENER_OPINION_CLUSTERS | DOCKET | other | DOCKET unproven. |
| walk | **Jail rate against injury deaths** | Do high-jail counties also have high injury and violence death rates? | Catalog item 39. | JUSTICE__XC_VERA_INCARCERATION_TRENDS\|HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY | FIPS | other |  |
| walk | **Judges' gifts against their positions** | Which outside positions come with the most gifts and travel? | Gift and reimbursement tables meet positions. | JUSTICE__FED_COURTLISTENER_DISCLOSURE_GIFTS\|JUSTICE__FED_COURTLISTENER_DISCLOSURE_REIMBURSEMENTS\|JUSTICE__FED_COURTLISTENER_POSITIONS | CL_PERSON_ID | other |  |
| walk | **Judge holdings against Senate trades** | Which stocks appear in both judges' and senators' disclosures? | Two branches, same tickers. | JUSTICE__FED_COURTLISTENER_INVESTMENTS\|FINANCE__SENATE_TRADES | ticker / asset name | other | Not a catalog key. Fuzzy name match. |
| walk | **Sentencing by judge** | Which judges hand down the longest sentences for the same charge? | Judge column exists in the criminal file. | JUSTICE__FED_FJC_IDB_CRIMINAL\|JUSTICE__FED_FJC_ARTICLE_III_JUDGES | judge code | ranking | Judge code not a catalog key. Needs proving. |
| walk | **Gun dealers against background checks** | Do states with more dealers per person run more checks per person? | State-level scatter. | JUSTICE__FED_ATF_FFL\|JUSTICE__FED_FBI_NICS_CHECKS | state code | other | State is a lookup, not a catalog key. |
| walk | **Same name, four sanctions lists** | Which targets appear on OFAC, EU, UK and UN lists at once? | A Venn of sanctions. | JUSTICE__FED_OFAC_SDN\|JUSTICE__INTL_EU_SANCTIONS\|JUSTICE__INTL_UK_SANCTIONS_LIST\|JUSTICE__XC_UN_CONSOLIDATED_SANCTIONS_LIST | name | other | Name match only. Not a catalog key. |
| run | **One judge, every table** | For one judge: bio, courts, votes, ideology, disclosures, gifts, trips, holdings? | The judge card. | JUSTICE__FED_FJC_ARTICLE_III_JUDGES\|JUSTICE__FED_COURTLISTENER_JUDGES\|JUSTICE__FED_COURTLISTENER_POSITIONS\|JUSTICE__FED_COURTLISTENER_JUDGE_EDUCATIONS\|JUSTICE__FED_COURTLISTENER_JUDGE_POLITICAL_AFFILIATIONS\|JUSTICE__FED_COURTLISTENER_FINANCIAL_DISCLOSURES\|JUSTICE__FED_COURTLISTENER_DISCLOSURE_GIFTS\|JUSTICE__FED_COURTLISTENER_INVESTMENTS\|POLITICS__JUDGE_IDEOLOGY_COA | CL_PERSON_ID | other | CL_PERSON_ID: 8 tables, 28 edges. |
| run | **Fifty years of federal court** | Civil, criminal, appellate and bankruptcy filings by district, one animated map? | The whole system breathing. | JUSTICE__FED_FJC_IDB_CIVIL\|JUSTICE__FED_FJC_IDB_CRIMINAL\|JUSTICE__FED_FJC_IDB_APPELLATE\|JUSTICE__FED_FJC_IDB_BANKRUPTCY\|JUSTICE__FED_COURTLISTENER_COURTS | CL_COURT_ID / district code | map | Not a catalog key; lookup or unproven. |
| run | **One name across the sanctions world** | For one entity: every list, every program, every alias, every date? | Sanctions as a lookup. | JUSTICE__FED_OFAC_SDN\|JUSTICE__FED_CONSOLIDATED_SCREENING_LIST\|JUSTICE__INTL_OPENSANCTIONS_DEFAULT\|JUSTICE__INTL_EU_SANCTIONS\|JUSTICE__INTL_UK_SANCTIONS_LIST\|JUSTICE__XC_UN_CONSOLIDATED_SANCTIONS_LIST | name | other | Name match only. Not a catalog key; lookup or unproven. |

### Environment — 44 ideas

| Tier | Title | Question | Why it matters | Tables | Joins on | Visual | Notes |
|---|---|---|---|---|---|---|---|
| crawl | **Repeat violators who paid nothing** | Which facilities broke rules most often and paid the least? | Built table with minority share nearby. | ENVIRONMENT__EPA_PENALTY_GAP | single table | map | Built table. |
| crawl | **Dirtiest power plants** | Which plants emit the most CO2 per megawatt-hour? | Names and owners on a map. | ENVIRONMENT__FED_EPA_EGRID_PLANT_2022 | single table | map |  |
| crawl | **Greenhouse gas by facility since 2010** | Which facilities cut emissions and which grew? | A slope chart per facility. | ENVIRONMENT__FED_EPA_GHGRP_EMISSION\|ENVIRONMENT__FED_EPA_GHGRP_FACILITY | stack, same shape | timeline | Same facility ID; FRS_ID likely, confirm. |
| crawl | **Toxic releases 2023** | Which facilities released the most, by chemical and by route? | Air, water, land as stacked bars. | ENVIRONMENT__FED_EPA_TRI_BASIC_2023\|ENVIRONMENT__FED_EPA_TRI_FACILITY | stack, same shape | ranking | Several tables shown side by side, no join. If a join is wanted, it is not in the catalog. |
| crawl | **Discharging into already impaired water** | How many permit holders dump into water already listed as impaired? | The flag is in the table. | ENVIRONMENT__FED_EPA_NPDES_ICIS_FACILITIES | single table | map |  |
| crawl | **Drinking water violations map** | Which water systems have the most health-based violations? | 15M rows to one map. | ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT | single table | map |  |
| crawl | **Lead at the tap** | Where did lead samples exceed the limit, and when? | Flint-style question, national scope. | ENVIRONMENT__FED_EPA_SDWA_SDWA_LCR_SAMPLES | single table | map |  |
| crawl | **Superfund sites map** | Where are Superfund sites and which are on the priority list? | Boundaries, not dots. | ENVIRONMENT__FED_EPA_SUPERFUND_SITE_BOUNDARIES | single table | map |  |
| crawl | **Fracking water use** | How much water does one frack job use, by state and year? | Gallons people can picture. | ENVIRONMENT__FED_FRACFOCUS_DISCLOSURE_LIST | single table | timeline |  |
| crawl | **Trade-secret chemicals** | What share of fracking ingredients hide their chemical ID, and is it rising? | Secrecy as a trend line. | ENVIRONMENT__FED_FRACFOCUS_REGISTRY | single table | timeline | 7.2M rows. |
| crawl | **High-hazard dams in poor condition** | Which dams would kill people if they failed and are rated poor? | Map plus years since last inspection. | ENVIRONMENT__FED_NID_DAMS | single table | map |  |
| crawl | **Storm damage by year** | Which storm types cause the most dollar damage and deaths per year? | Tornado tracks on a map. | ENVIRONMENT__FED_NOAA_STORM_EVENTS\|ENERGY_ENVIRONMENT__NOAA_STORMS_BY_STATE_EVENT_AGG | stack, same shape | timeline | Rollup exists in PUBLIC. |
| crawl | **Pipeline incidents by operator** | Which gas pipeline operators have the most serious incidents since 2010? | Operator names and deaths. | ENVIRONMENT__FED_PHMSA_FLAGGED_INCIDENTS | single table | ranking |  |
| crawl | **Spill calls to the Coast Guard** | How many spill calls per year, by type, and where? | A million calls. | ENVIRONMENT__FED_USCG_NRC_INCIDENTS | single table | timeline |  |
| crawl | **Orphaned wells map** | Where are the abandoned oil and gas wells nobody will plug? | Dots that look like a rash. | ENVIRONMENT__FED_USGS_ORPHANED_OIL_GAS_WELLS | single table | map |  |
| crawl | **A river over fifty years** | How did streamflow or groundwater level at one site change over decades? | Pick one gauge, one long line. | ENVIRONMENT__FED_USGS_WATER | single table | timeline | 6.5M readings. |
| crawl | **Killed defending land** | Where are environmental defenders killed, and by whom? | Names, countries, years. | ENVIRONMENT__INTL_GLOBAL_WITNESS_DEFENDERS | single table | map |  |
| crawl | **Country CO2, fossil share, warming** | How do CO2, fossil share and temperature anomaly move together per country? | Three OWID series, one page. | ENVIRONMENT__XC_OWID_CO2\|ENVIRONMENT__XC_OWID_FOSSIL_SHARE\|ENVIRONMENT__XC_OWID_TEMP_ANOMALY | country + year | timeline | Country code lookup, not a catalog key. |
| crawl | **Air monitors opening and closing** | Where were air-quality monitors shut down? | Fewer monitors, less data. | ENVIRONMENT__FED_EPA_AQS_SITES | single table | map |  |
| crawl | **High-priority air violators** | Which air-permitted facilities are flagged high-priority right now? | One flag, one map. | ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES | single table | map |  |
| crawl | **Admitted deviations** | What share of big air polluters admit deviating from their permit each year? | Self-reported honesty. | ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_TITLEV_CERTS | single table | timeline |  |
| crawl | **Hazardous waste, months in violation** | Which handlers stayed in serious violation the longest? | A month-by-month status strip. | ENVIRONMENT__FED_EPA_RCRA_VIOSNC_HISTORY | single table | timeline |  |
| crawl | **Stack tests failed** | Which facilities fail smokestack tests most? | Pass-fail, per facility. | ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_STACK_TESTS | single table | ranking |  |
| crawl | **Minerals by country** | Which countries hold the reserves of each critical mineral? | A world map per mineral. | ENVIRONMENT__FED_USGS_MINERALS | single table | map |  |
| crawl | **Water system size versus owner type** | Are small private systems more common than people think? | Population served by owner type. | ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS | single table | other |  |
| walk | **Violations per permit against inspections** | Do more inspections find more violations, or fewer? | Catalog item 26. | ENVIRONMENT__FED_EPA_NPDES_NPDES_PS_VIOLATIONS\|ENVIRONMENT__FED_EPA_NPDES_NPDES_INSPECTIONS | NPDES_ID | other |  |
| walk | **Enforcement by industry** | Which industries draw the most enforcement per facility? | Catalog item 27. | ENVIRONMENT__FED_EPA_NPDES_NPDES_FORMAL_ENFORCEMENT_ACTIONS\|ENVIRONMENT__FED_EPA_NPDES_NPDES_NAICS | NPDES_ID | ranking |  |
| walk | **Quarterly noncompliance by old industry code** | Which SIC sectors are chronically noncompliant? | Catalog item 28. | ENVIRONMENT__FED_EPA_NPDES_NPDES_QNCR_HISTORY\|ENVIRONMENT__FED_EPA_NPDES_NPDES_SICS | NPDES_ID | other |  |
| walk | **Violations per person served** | Which water systems have the most violations per resident? | Catalog item 29. | ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT\|ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS | PWSID | map |  |
| walk | **Site visits against violations** | Do systems with more visits have fewer violations? | Catalog item 30. | ENVIRONMENT__FED_EPA_SDWA_SDWA_SITE_VISITS\|ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT | PWSID | other |  |
| walk | **Lead exceedances by area served** | Which cities and zips drink from systems with lead exceedances? | Catalog item 31. | ENVIRONMENT__FED_EPA_SDWA_SDWA_LCR_SAMPLES\|ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS | PWSID | map |  |
| walk | **Air emissions by corporate parent** | Which parent companies own the most air pollution? | Catalog item 32. | ENVIRONMENT__FED_EPA_AIR_EMISSIONS_POLL_RPT_COMBINED_EMISSIONS\|ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK | FRS_ID | ranking |  |
| walk | **Toxic releases per county** | Which counties carry the most toxic release per resident? | Catalog item 33. | ENVIRONMENT__FED_EPA_TRI_BASIC_2023\|DIM_COUNTY | FIPS | map |  |
| walk | **EPA facilities against county jobs** | Do counties with more EPA facilities have more jobs, or just more pollution? | Catalog item 37. | ENVIRONMENT__FED_EPA_FRS_FACILITIES\|ECONOMICS__FED_BLS_QCEW | FIPS | other |  |
| walk | **Storms and FEMA housing aid** | Which counties' storm damage turned into the most FEMA housing registrations? | Catalog item 40. | ENVIRONMENT__FED_NOAA_STORM_EVENTS\|HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS | FIPS | map | FEMA table is a partial load; counts are floors. |
| walk | **Subsidiaries with EPA facilities** | Which global parents own the most EPA-tracked facilities through subsidiaries? | Catalog item 53. | ECONOMICS__INTL_GLEIF_RELATIONSHIPS\|ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK | LEI | other |  |
| walk | **Penalties against releases** | Do facilities that release the most pay the most? | ECHO penalties meet TRI pounds. | ENVIRONMENT__FED_EPA_ECHO\|ENVIRONMENT__FED_EPA_TRI_BASIC_2023 | FRS_ID | other |  |
| walk | **Facilities in every program** | Which facilities are in air, water, waste and toxic programs all at once? | Program links per facility, counted. | ENVIRONMENT__FED_EPA_FRS_FRS_PROGRAM_LINKS\|ENVIRONMENT__FED_EPA_FRS_FACILITIES | FRS_ID | ranking |  |
| walk | **Fracking water by source** | Where does frack water come from, and does that differ by state? | Source table meets job table. | ENVIRONMENT__FED_FRACFOCUS_WATER_SOURCE\|ENVIRONMENT__FED_FRACFOCUS_DISCLOSURE_LIST | job ID | other | Same-source job ID; not a catalog key. |
| walk | **Plant emissions by owner share** | Which utilities own the most emissions, weighted by share? | Catalog items 34 and 35. | ENVIRONMENT__FED_EPA_EGRID_PLANT_2022\|ENERGY__FED_EIA860_4_OWNER | EIA_PLANT_ID | ranking | EIA keys are in the keyset with zero edges. Unproven. |
| run | **One facility, every EPA system** | For one FRS ID: programs, inspections, violations, penalties, releases, gases, parent? | The facility page. | ENVIRONMENT__FED_EPA_FRS_FACILITIES\|ENVIRONMENT__FED_EPA_ECHO\|ENVIRONMENT__FED_EPA_FRS_FRS_PROGRAM_LINKS\|ENVIRONMENT__FED_EPA_TRI_BASIC_2023\|ENVIRONMENT__FED_EPA_GHGRP_EMISSION\|ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK\|ENVIRONMENT__FED_EPA_AIR_EMISSIONS_POLL_RPT_COMBINED_EMISSIONS | FRS_ID | other | FRS_ID: 17 tables, 136 edges. |
| run | **Corporate polluter family tree** | From a global parent down through subsidiaries to facilities to violations? | A tree with pollution at the leaves. | ECONOMICS__INTL_GLEIF\|ECONOMICS__INTL_GLEIF_RELATIONSHIPS\|ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK\|ENVIRONMENT__FED_EPA_ECHO | LEI, FRS_ID | flow |  |
| run | **Your tap water** | For a zip: which system, its violations, lead samples, visits, milestones? | A lookup a reader will try on their own address. | ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS\|ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS\|ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT\|ENVIRONMENT__FED_EPA_SDWA_SDWA_LCR_SAMPLES\|ENVIRONMENT__FED_EPA_SDWA_SDWA_SITE_VISITS\|ENVIRONMENT__FED_EPA_SDWA_SDWA_EVENTS_MILESTONES | PWSID | other | PWSID: 10 tables, 45 edges. |
| run | **Wastewater permit, whole life** | Permit, inspections, violations, enforcement, quarterly scorecard, one timeline? | Every NPDES table on one strip. | ENVIRONMENT__FED_EPA_NPDES_ICIS_FACILITIES\|ENVIRONMENT__FED_EPA_NPDES_NPDES_INSPECTIONS\|ENVIRONMENT__FED_EPA_NPDES_NPDES_PS_VIOLATIONS\|ENVIRONMENT__FED_EPA_NPDES_NPDES_SE_VIOLATIONS\|ENVIRONMENT__FED_EPA_NPDES_NPDES_FORMAL_ENFORCEMENT_ACTIONS\|ENVIRONMENT__FED_EPA_NPDES_NPDES_QNCR_HISTORY | NPDES_ID | timeline |  |

### Economics — 36 ideas

| Tier | Title | Question | Why it matters | Tables | Joins on | Visual | Notes |
|---|---|---|---|---|---|---|---|
| crawl | **County wages by industry** | Which counties pay best in each industry, and where did wages stall? | 3.6M rows to one map. | ECONOMICS__FED_BLS_QCEW | single table | map |  |
| crawl | **Federal jobs share by county** | Which counties depend most on federal employment? | Ownership column splits federal from private. | ECONOMICS__FED_BLS_QCEW | single table | map |  |
| crawl | **OSHA inspections by industry** | Which industries get inspected most, and find the most violations? | 5.2M inspections. | ECONOMICS__FED_DOL_OSHA_INSPECTIONS | single table | ranking |  |
| crawl | **The 2008 bank failure wave** | When did banks fail, how big, and what did it cost the insurance fund? | A timeline with a wall in 2009. | ECONOMICS__FED_FDIC_FAILED_BANKS | single table | timeline |  |
| crawl | **Foreign aid flow** | Which agencies send how much to which countries? | Agency to country sankey. | ECONOMICS__FED_FOREIGNASSISTANCE | single table | flow |  |
| crawl | **Nonprofits per resident** | Which counties have the most nonprofits per person, by category? | Two million orgs on a map. | ECONOMICS__FED_IRS_BMF\|CORPORATE_ENTITIES__IRS_BMF_BY_STATE_NTEE_AGG | stack, same shape | map | State rollup in PUBLIC. |
| crawl | **The auto-revocation wave** | How many nonprofits lost status per year, and how many came back? | 1.2M revocations, one spike. | ECONOMICS__FED_IRS_AUTO_REVOCATIONS\|CORPORATE_ENTITIES__IRS_REVOCATION_BY_STATE_YEAR_AGG | stack, same shape | timeline | Several tables shown side by side, no join. If a join is wanted, it is not in the catalog. |
| crawl | **Failed pensions, who got hurt** | Which sponsors' pension plans failed, and how many participants? | Company names next to headcounts. | ECONOMICS__FED_PBGC_TRUSTEED_PENSION_PLANS\|LABOR__FED_PBGC_TRUSTEED_PLANS | stack, same shape | ranking | Two tables, same subject. |
| crawl | **SBA loan default rate by lender** | Which lenders' SBA loans default most? | Default flag exists. | ECONOMICS__FED_SBA_LOANS | single table | ranking |  |
| crawl | **PPP loans, jobs claimed per dollar** | Which borrowers claimed the fewest jobs per loan dollar? | Pandemic money, itemized. | ECONOMICS__FED_SBA_PPP\|ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS | stack, same shape | other | 150K+ table has franchise and forgiveness columns. |
| crawl | **PPP by franchise** | Which franchise brands' locations took the most PPP money? | Brand names. | ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS | single table | ranking |  |
| crawl | **Federal contracts by agency and industry** | Which agencies buy what, and how concentrated are vendors? | 6.3M contract actions. | ECONOMICS__FED_USASPENDING_CONTRACTS\|SPENDING_BUDGET__USASPENDING_BY_AGENCY_NAICS_AGG | stack, same shape | other | Rollups in PUBLIC. |
| crawl | **Contract dollars per state** | Which states get the most federal contract money per resident? | Map with population. | SPENDING_BUDGET__USASPENDING_BY_AGENCY_STATE_AGG\|DIM_STATE | state code | map | Not a catalog key; lookup or unproven. |
| crawl | **National debt every day** | How did the debt move day by day, public versus intragovernmental? | One line, every day. | ECONOMICS__FED_TREASURY_DEBT_TO_PENNY | single table | timeline |  |
| crawl | **The government's daily cash** | What does the Treasury take in and pay out each day? | Daily ledger as a rhythm chart. | ECONOMICS__FED_TREASURY_DTS_DEPOSITS | single table | timeline |  |
| crawl | **Interest the government pays** | How did the average rate on each security type move? | Rates by type over time. | ECONOMICS__FED_TREASURY_AVG_INTEREST_RATES | single table | timeline |  |
| crawl | **Tax receipts by category** | Which receipt categories rose and fell month to month? | Monthly, with last-year comparison. | ECONOMICS__FED_TREASURY_MTS_RECEIPTS | single table | timeline |  |
| crawl | **Company registrations by country** | Which countries register the most legal entities? | 3.4M entities. | ECONOMICS__INTL_GLEIF | single table | map |  |
| crawl | **Why companies will not name their parent** | What reasons do companies give for not reporting their parent? | 6.3M refusals, a handful of reasons. | ECONOMICS__INTL_GLEIF_REPEX | single table | ranking |  |
| crawl | **Corporate family trees** | Which parents have the most subsidiaries? | A tree graph. | ECONOMICS__INTL_GLEIF_RELATIONSHIPS | single table | flow |  |
| crawl | **Hunger by country** | Which countries' food insecurity worsened? | FAO and IPC on one map. | ECONOMICS__INTL_FAO_FAOSTAT_FOOD_SECURITY\|ECONOMICS__INTL_IPC_FOOD_INSECURITY_GLOBAL | country + year | map | Not a catalog key; lookup or unproven. |
| crawl | **Inequality by country** | Which countries' Gini rose most? | OWID series. | ECONOMICS__XC_OWID_GINI | single table | timeline |  |
| crawl | **Retirement plans by assets** | Which sponsors hold the biggest plans, and how much do they pay out? | Form 5500. | ECONOMICS__FED_DOL_FORM5500 | single table | ranking |  |
| crawl | **Audit findings on grant money** | Which grantees had material weaknesses, and how much did they spend? | Single audits. | ECONOMICS__FED_FAC_SINGLE_AUDIT | single table | ranking |  |
| walk | **E-filings per nonprofit against assets** | Do bigger nonprofits file more? | Catalog item 11. | ECONOMICS__FED_IRS_990_EFILE_INDEX\|ECONOMICS__FED_IRS_BMF | EIN | other |  |
| walk | **Revocations against active nonprofits** | Which states lose the most nonprofits per active one? | Catalog item 12. | ECONOMICS__FED_IRS_REVOCATION\|ECONOMICS__FED_IRS_BMF | EIN | map |  |
| walk | **Deductible against total** | What share of nonprofits per subsection can take deductible gifts? | Catalog item 13. | ECONOMICS__FED_IRS_PUB78_ELIGIBLE_DONEES\|ECONOMICS__FED_IRS_BMF | EIN | other |  |
| walk | **Injuries per employer against industry peers** | Which employers injure far more than their industry? | Catalog item 14. | LABOR__FED_OSHA_ITA_300A_SUMMARY_2023\|LABOR__FED_OSHA_ITA_300A_SUMMARY_2024\|LABOR__FED_OSHA_ITA_300A_SUMMARY_2025 | EIN, NAICS | ranking | NAICS is a code lookup. Not a catalog key; lookup or unproven. |
| walk | **Federal money against nonprofit revenue** | Which nonprofits live almost entirely on federal grants? | Catalog item 15. | ECONOMICS__FED_FAC_SINGLE_AUDIT\|ECONOMICS__FED_IRS_BMF | EIN | ranking |  |
| walk | **Contract vendors who also get grants** | Which vendors take both contract and assistance money? | Catalog item 17. | ECONOMICS__FED_USASPENDING_CONTRACTS\|ECONOMICS__FED_FAC_SINGLE_AUDIT | UEI | other | UEI match 10 to 80 percent, sparse. |
| walk | **NIH grants against SBIR awards** | Which small companies win both NIH and SBIR money? | Catalog item 19. | SCIENCE_RESEARCH__FED_NIH_REPORTER\|SCIENCE_RESEARCH__FED_SBIR_STTR_AWARDS | UEI | other |  |
| walk | **Banned vendors still getting contracts** | Did any excluded vendor receive a contract after exclusion? | Catalog item 20. | PROCUREMENT__FED_SAM_EXCLUSIONS\|ECONOMICS__FED_USASPENDING_CONTRACTS | UEI / DUNS | timeline |  |
| walk | **Hospital nonprofits: pay against assets** | Do bigger hospital nonprofits pay executives more per asset dollar? | EIN links the pay table to the master list. | HEALTH__HOSPITAL_OFFICER_PAY\|ECONOMICS__FED_IRS_BMF | EIN | other |  |
| walk | **PPP borrowers with OSHA injuries** | Did the biggest PPP borrowers also report the most injuries? | Fuzzy name-and-zip match. | ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS\|LABOR__FED_OSHA_ITA_300A_SUMMARY_2023 | NAME@ZIP | other | NAME@ZIP is fuzzy. Multi-word names only. |
| run | **One nonprofit, every table** | For one EIN: master record, filings, revocations, audits, federal money, officer pay? | EIN is a steel key. | ECONOMICS__FED_IRS_BMF\|ECONOMICS__FED_IRS_990_EFILE_INDEX\|ECONOMICS__FED_IRS_REVOCATION\|ECONOMICS__FED_FAC_SINGLE_AUDIT\|ECONOMICS__FED_IRS_PUB78_ELIGIBLE_DONEES\|HEALTH__HOSPITAL_OFFICER_PAY | EIN | other | EIN: 34 tables, 366 edges. |
| run | **Federal money by county** | Contracts, PPP, SBA, grants, FEMA, relief: dollars per resident per county? | Where the money lands. | ECONOMICS__FED_USASPENDING_CONTRACTS\|ECONOMICS__FED_SBA_PPP\|ECONOMICS__FED_SBA_LOANS\|HEALTH__FED_HRSA_PROVIDER_RELIEF_FUND\|HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS\|DIM_COUNTY | FIPS | map | Zip to county via XWALK_ZCTA_COUNTY where needed. |

### Finance — 27 ideas

| Tier | Title | Question | Why it matters | Tables | Joins on | Visual | Notes |
|---|---|---|---|---|---|---|---|
| crawl | **Who owns the big companies** | Which managers hold the most of one company, and how concentrated is ownership? | Ownership of a household name, drawn. | FINANCE__FED_SEC_13F_SUBMISSION | single table | ranking | 3.8M holdings. |
| crawl | **Insiders selling before the drop** | Which companies' insiders sold the most, and when? | A timeline per company. | FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS\|FINANCE__FED_SEC_INSIDER_REPORTINGOWNER | stack, same shape | timeline | Same filing ID; not a catalog key. |
| crawl | **The audit partner who signs everything** | Which audit partners and firms sign the most public-company audits? | Names behind the books. | FINANCE__FED_PCAOB_FORM_AP_FILINGS | single table | ranking |  |
| crawl | **Bank deserts** | Which counties lost the most bank branches, and where are there none? | Branch counts per county per year. | FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS\|DIM_COUNTY | FIPS | map | Branch address to county lookup. |
| crawl | **Deposits per branch, over time** | Which banks hold the most deposits in the fewest branches? | Consolidation, drawn. | FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS | single table | timeline |  |
| crawl | **Credit unions ranked** | Which credit unions are biggest, and which grew fastest? | Quarterly snapshots. | FINANCE__FED_NCUA_FEDERALLY_INSURED_CU_LIST\|FINANCE__FED_NCUA_CALL_REPORTS_FS220 | stack, same shape | ranking | Several tables shown side by side, no join. If a join is wanted, it is not in the catalog. |
| crawl | **Income by zip code** | Where are the richest and poorest zips by reported income? | IRS returns, mapped. | FINANCE__FED_IRS_SOI\|DIM_ZIP_POINT | ZIP | map | Zip lookup. |
| crawl | **Small-donor share by cycle** | Did small donors become a bigger share of campaign money? | One line, twenty cycles. | FINANCE__FED_FEC_INDIV_CONTRIBUTIONS\|MONEY_IN_POLITICS__FEC_INDIV_BY_STATE_CYCLE_AGG | stack, same shape | timeline | Use the PUBLIC rollup first; 284M rows raw. |
| crawl | **Donors by occupation and employer** | Which employers' staff give the most, and to whom? | Employer column is gold. | FINANCE__FED_FEC_INDIV_CONTRIBUTIONS | single table | ranking |  |
| crawl | **Outside spending, support versus oppose** | Did independent spending turn more negative over cycles? | Support and oppose as two bars. | FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES | single table | timeline |  |
| crawl | **PAC to PAC transfers** | Which committees move the most money to other committees? | A network of transfers. | FINANCE__FED_FEC_COMMITTEE_TO_CANDIDATE | single table | flow |  |
| crawl | **Foreign banks reporting to the IRS** | Which countries have the most FATCA-registered institutions? | A tax-haven map. | FINANCE__FED_FATCA_FFI\|ECONOMICS__FED_IRS_FATCA_FFI_LIST | stack, same shape | map | Two copies of the same list. |
| crawl | **Hedge funds' weekly bets** | How did hedge fund long and short positions in stock index futures move weekly? | Positioning as a wave. | FINANCE__FED_CFTC_COT_FINANCIAL_HIST\|EDUCATION__FED_CFTC_COT_FINANCIAL | stack, same shape | timeline | Two COT tables, one misfiled under EDUCATION. |
| crawl | **Who countries owe** | Which creditors hold each country's debt, and where are the repayment cliffs? | A debt map with cliffs flagged. | FINANCE__INTL_WB_IDS\|MONEY__DEBT_REPAYMENT_CLIFF | country + year | timeline | Country lookup. Not a catalog key; lookup or unproven. |
| crawl | **Two Senate trade sources disagree** | How many senators' trades appear in one source but not the other? | Source disagreement as the chart. | FINANCE__FED_SENATE_EFD_PTR\|FINANCE__FED_SENATE_STOCK_WATCHER\|FINANCE__SENATE_TRADES | stack, same shape | other | Combined table has the match-confidence column. |
| crawl | **Filings per industry per quarter** | Which industries file the most financial statements each quarter? | Nine quarterly tables, one line. | FINANCE__FED_SEC_DERA_SUB_2024Q1\|FINANCE__FED_SEC_DERA_SUB_2024Q2\|FINANCE__FED_SEC_DERA_SUB_2024Q3\|FINANCE__FED_SEC_DERA_SUB_2024Q4\|FINANCE__FED_SEC_DERA_SUB_2025Q1\|FINANCE__FED_SEC_DERA_SUB_2025Q2\|FINANCE__FED_SEC_DERA_SUB_2025Q3\|FINANCE__FED_SEC_DERA_SUB_2025Q4\|FINANCE__FED_SEC_DERA_SUB_2026Q1 | stack, same shape | timeline | Union, no join. |
| crawl | **Who advises money market funds** | Which advisors manage the most money market funds? | Concentration in one chart. | FINANCE__FED_SEC_MONEY_MARKET_FUND_INFORMATION | single table | ranking |  |
| crawl | **Stock exchanges of the world** | How many trading venues per country, and which operators run them? | Registry as a map. | FINANCE__INTL_ISO_MIC_REGISTRY | single table | map |  |
| walk | **Auditor against filer size** | Do the Big Four audit all the big filers, and who audits the rest? | Catalog item 22. | FINANCE__FED_PCAOB_FORM_AP_FILINGS\|FINANCE__FED_SEC_EDGAR_FINANCIALS | CIK | other |  |
| walk | **Insider filings against company size** | Which companies file the most insider trades per dollar of size? | Catalog item 23. | FINANCE__FED_SEC_EDGAR_INSIDERS\|FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE | CIK | other |  |
| walk | **13F holdings per manager** | Which managers hold the most positions, and how did that change? | Catalog item 24. | FINANCE__FED_SEC_13F_SUBMISSION\|FINANCE__FED_SEC_13F_FILERS | CIK | ranking |  |
| walk | **Injuries at public companies** | Which public companies report the most workplace injuries? | Catalog item 25, thin. | LABOR__FED_OSHA_ITA_300A_SUMMARY_2024\|FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE | CIK~EIN | ranking | CIK~EIN matches 2 to 16 percent. Sample, never a rate. |
| walk | **Mortgage lenders by global ID** | Which lenders in the mortgage file are subsidiaries of which parents? | Catalog item 55. | HOUSING__FED_CFPB_HMDA_HISTORIC\|ECONOMICS__INTL_GLEIF | LEI | other | Historic HMDA uses old lender ID; use the crosswalk. |
| walk | **Branches against FHLB membership** | Do FHLB members hold more branches per county? | Catalog item 57, no edges yet. | FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS\|FINANCE__FED_FHFA_FHLB_MEMBERSHIP | FDIC_CERT | other | Key in keyset, zero edges. |
| walk | **13F positions by issuer** | Which issuers are held by the most managers? | Catalog item 56, no edges yet. | FINANCE__FED_SEC_13F_SUBMISSION\|FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE | CUSIP bridge | ranking | FTD_CUSIP_BRIDGE named in catalog but not in the inventory. Not a catalog key; lookup or unproven. |
| walk | **Senators and insiders trading the same stock** | Did a senator trade a stock the same week its insiders did? | Two disclosure regimes on one timeline. | FINANCE__SENATE_TRADES\|FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS\|FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE | ticker | timeline | Ticker not a catalog key. |
| run | **One public company, every table** | For one CIK: filings, insiders, holders, auditor, injuries, EPA sites? | The company card. | FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE\|FINANCE__FED_SEC_EDGAR_FINANCIALS\|FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS\|FINANCE__FED_SEC_13F_SUBMISSION\|FINANCE__FED_PCAOB_FORM_AP_FILINGS\|LABOR__FED_OSHA_ITA_300A_SUMMARY_2024\|ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK | CIK, CIK~EIN | other | CIK: 19 tables, 128 edges. Cross-key legs are thin. |

### Energy — 17 ideas

| Tier | Title | Question | Why it matters | Tables | Joins on | Visual | Notes |
|---|---|---|---|---|---|---|---|
| crawl | **Power plants by fuel and age** | When were plants built, by fuel, and when do they retire? | A generation-by-generation chart. | ENERGY__FED_EIA860_3_1_GENERATOR | single table | timeline | Operating and planned retirement dates. |
| crawl | **Coal retirements on a map** | Which coal generators are scheduled to retire, and where? | Retirement dates as a countdown. | ENERGY__FED_EIA860_3_1_GENERATOR\|ENERGY__FED_EIA860_2_PLANT | EIA_PLANT_ID | map | EIA keys in keyset, zero edges. |
| crawl | **Wind turbines getting taller** | How did hub height and capacity grow by install year? | A physical fact people can picture. | ENERGY__FED_EIA860_3_2_WIND | single table | timeline |  |
| crawl | **Solar tracking share** | What share of solar generators track the sun, by state and year? | Technology adoption as a map. | ENERGY__FED_EIA860_3_3_SOLAR | single table | map |  |
| crawl | **Battery storage boom** | How fast did grid battery capacity grow, and what is it used for? | A hockey stick. | ENERGY__FED_EIA860_3_4_ENERGY_STORAGE | single table | timeline |  |
| crawl | **Who owns the generators** | Which owners hold the most capacity through partial stakes? | Ownership shares as a treemap. | ENERGY__FED_EIA860_4_OWNER | single table | other |  |
| crawl | **Smart meters by utility** | Which utilities have rolled out smart meters, and which have not? | Old versus new meters, per utility. | ENERGY__FED_EIA861_ADVANCED_METERS | single table | ranking |  |
| crawl | **Outage minutes by utility** | Whose customers lose power most often and longest? | Reliability ranking. | ENERGY__FED_EIA861_RELIABILITY | single table | ranking |  |
| crawl | **Rooftop solar selling back** | Which states have the most net-metered solar and paired batteries? | Customer-owned power, mapped. | ENERGY__FED_EIA861_NET_METERING | single table | map |  |
| crawl | **Who serves which county** | Which utility serves each county, and which counties have several? | Service territory map. | ENERGY__FED_EIA861_SERVICE_TERRITORY\|DIM_COUNTY | FIPS | map |  |
| crawl | **Revenue per customer** | Which utilities charge the most per residential customer? | Sales table split by sector. | ENERGY__FED_EIA861_SALES_ULT_CUST | single table | ranking |  |
| crawl | **Energy efficiency spend** | Which utilities spend most on efficiency, and save most? | Savings per dollar. | ENERGY__FED_EIA861_ENERGY_EFFICIENCY\|ENERGY__FED_EIA861_DEMAND_RESPONSE | stack, same shape | ranking | Several tables shown side by side, no join. If a join is wanted, it is not in the catalog. |
| crawl | **World electricity mix** | Which countries' generation shifted most toward renewables? | Ember data, one stacked area per country. | ENERGY__INTL_EMBER_ELEC | single table | timeline |  |
| crawl | **Boilers and their pollution rules** | Which boilers meet which emissions standards, and how? | Compliance method per boiler. | ENERGY__FED_EIA860_6_2_ENVIROEQUIP | single table | other |  |
| walk | **Plant emissions against plant owner** | Which utilities own the dirtiest fleets? | Catalog items 34, 35. | ENVIRONMENT__FED_EPA_EGRID_PLANT_2022\|ENERGY__FED_EIA860_2_PLANT\|ENERGY__FED_EIA860_1_UTILITY | EIA_PLANT_ID / UTILITY_ID | ranking | Zero edges yet. |
| walk | **Outages against smart meters** | Do utilities with more smart meters report fewer outages? | Two EIA-861 tables, same utility ID. | ENERGY__FED_EIA861_RELIABILITY\|ENERGY__FED_EIA861_ADVANCED_METERS | UTILITY_ID | other | Zero edges yet. |
| run | **One utility, every table** | For one utility: plants, generators, customers, outages, meters, territory? | The utility card. | ENERGY__FED_EIA860_1_UTILITY\|ENERGY__FED_EIA860_2_PLANT\|ENERGY__FED_EIA860_3_1_GENERATOR\|ENERGY__FED_EIA861_SALES_ULT_CUST\|ENERGY__FED_EIA861_RELIABILITY\|ENERGY__FED_EIA861_SERVICE_TERRITORY\|ENERGY__FED_EIA861_UTILITY_DATA | UTILITY_ID | other | Needs the EIA edges built first. |

### Housing — 14 ideas

| Tier | Title | Question | Why it matters | Tables | Joins on | Visual | Notes |
|---|---|---|---|---|---|---|---|
| crawl | **Mortgage denial rate by race and county** | Where were applicants of one race denied far more than another, 2015 to 2017? | 45M applications, one honest map. | HOUSING__FED_CFPB_HMDA_HISTORIC | single table | map | Every outcome, not just approvals. |
| crawl | **Home prices by metro since 1975** | Which metros' prices rose most, and where did they fall? | The line everyone has an opinion on. | HOUSING__FED_FHFA_HPI | single table | timeline |  |
| crawl | **Redlining maps** | What did the 1930s maps say about each neighborhood, in their own words? | The original descriptions are the wow. | HOUSING__FED_MAPPING_INEQUALITY | single table | map | Full text and map shape. |
| crawl | **Subsidized housing tenants** | Who lives in HUD housing, by income, age, disability, race, per project? | One map with demographics on hover. | HOUSING__FED_HUD_ASSISTED_HOUSING_PROJECTS | single table | map | Negative values mean suppressed. |
| crawl | **Section 8 rent against market rent** | Where does Section 8 pay above or below local fair-market rent? | The gap column is built in. | HOUSING__FED_HUD_MF_SECTION8_CONTRACTS | single table | map |  |
| crawl | **Affordability restrictions expiring** | How many rural subsidized units lose their restrictions each coming year? | A cliff on a timeline. | HOUSING__FED_USDA_RD_MFH_ACTIVE_PROJECTS | single table | timeline |  |
| crawl | **FHA lenders ranked** | Which lenders write the most FHA loans, at what rates? | Lender names. | HOUSING__FED_HUD_FHA_SF_PORTFOLIO_SNAPSHOT | single table | ranking |  |
| crawl | **Twenty-five years of FHA apartment deals** | Which lenders and projects got the biggest multifamily commitments? | 2001 to 2026. | HOUSING__FED_HUD_MF_FIRM_COMMITMENTS | single table | timeline |  |
| crawl | **Flood insurance map** | Which communities are in the flood program, and how old are their maps? | Map age is a risk signal. | HOUSING__FED_FEMA_NFIP_COMMUNITY_STATUS_BOOK | single table | map |  |
| crawl | **Disaster housing aid by disaster** | Which disasters produced the most registrations and aid dollars? | Partial load; shape only. | HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS | single table | ranking | About 12 percent loaded, cut mid-load. Not a sample. |
| crawl | **Public housing authorities** | Which authorities run the most units, and how full are they? | 3,787 authorities. | HOUSING__FED_HUD_PUBLIC_HOUSING_AUTHORITIES | single table | map |  |
| walk | **Redlined then, denied now** | Do 1930s D-graded neighborhoods still see higher denial rates? | The chart that writes its own headline. | HOUSING__FED_MAPPING_INEQUALITY\|HOUSING__FED_CFPB_HMDA_HISTORIC\|DIM_TRACT | geometry / tract | map | Spatial join, not a catalog key. Needs proving. |
| walk | **Lenders across the ID change** | Which lenders kept lending through the 2017 to 2018 ID switch? | Crosswalk exists for this. | HOUSING__FED_CFPB_HMDA_ARID2017_LEI_XREF\|HOUSING__FED_CFPB_HMDA_HISTORIC | lender ID / LEI | other | Not a catalog key; lookup or unproven. |
| walk | **Home prices against disaster aid** | Did counties with big FEMA aid see prices fall after? | Catalog item 40 family. | HOUSING__FED_FHFA_HPI\|HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS | FIPS | timeline |  |

### Immigration — 12 ideas

| Tier | Title | Question | Why it matters | Tables | Joins on | Visual | Notes |
|---|---|---|---|---|---|---|---|
| crawl | **Immigration court by nationality and city** | Which nationalities fill which courts, and how long do cases take? | 12.6M cases. | IMMIGRATION__FED_EOIR_CASES | single table | map |  |
| crawl | **Days in ICE detention** | How long do people stay, by facility and year, since 2004? | Length of stay as a distribution. | IMMIGRATION__FED_ICE_DETENTION_STINTS | single table | timeline | 2.6M stays. |
| crawl | **Bond amounts by facility** | Where are bonds set highest? | Dollar amounts per facility. | IMMIGRATION__FED_ICE_DETENTION_STINTS | single table | ranking |  |
| crawl | **Detainer flags** | Which risk flags appear most on detainers, and how often none? | Dozens of yes-no columns counted. | IMMIGRATION__FED_ICE_DETAINERS | single table | other |  |
| crawl | **Detention facilities map** | Where are ICE facilities, by type? | 1,490 codes, 163 on the published list. | IMMIGRATION__FED_ICE_DETENTION_FACILITY_CODES\|IMMIGRATION__FED_ICE_DETENTION_FACILITY_LIST | stack, same shape | map | Gap between the two lists is itself a finding. |
| crawl | **H-1B sponsors and wages** | Which employers sponsor most, and what do they offer per job title? | Employer names and wages. | IMMIGRATION__FED_DOL_OFLC | single table | ranking |  |
| crawl | **Immigration lawyers ranked** | Which attorneys file the most visa cases? | Attorney column exists. | IMMIGRATION__FED_DOL_OFLC | single table | ranking |  |
| crawl | **Border encounters by nationality** | How did monthly encounters shift by nationality and outcome? | DHS stats as a stacked area. | IMMIGRATION__FED_DHS_OHSS | single table | timeline |  |
| crawl | **USCIS backlog** | How many applications are pending per form type per quarter? | The queue, drawn. | IMMIGRATION__FED_USCIS_DATA | single table | timeline |  |
| crawl | **Refugees by origin** | Which countries produced the most refugees per year? | OWID series. | IMMIGRATION__XC_OWID_REFUGEES | single table | timeline |  |
| walk | **Stays by facility on a map** | Which facilities hold people longest, mapped? | Stint table meets facility coordinates. | IMMIGRATION__FED_ICE_DETENTION_STINTS\|IMMIGRATION__FED_ICE_DETENTION_FACILITY_CODES | facility code | map | Same-source code, not a catalog key. |
| walk | **Court outcome against custody** | Do detained respondents lose more often than released ones? | Custody status column in the case table. | IMMIGRATION__FED_EOIR_CASES\|IMMIGRATION__FED_ICE_DETENTION_STINTS | anonymized person ID | other | Not a catalog key. Likely unjoinable. |

### Corporate Registry — 9 ideas

| Tier | Title | Question | Why it matters | Tables | Joins on | Visual | Notes |
|---|---|---|---|---|---|---|---|
| crawl | **Offshore leaks network** | Who connects to whom across the Panama, Paradise and Pandora papers? | A graph with 3.3M edges. | CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_RELATIONSHIPS\|CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_ENTITIES\|CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_OFFICERS\|CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_INTERMEDIARIES | ICIJ node ID | other | Same-source ID, not a catalog key. |
| crawl | **Offshore jurisdictions ranked** | Which jurisdictions host the most leaked entities, by incorporation year? | BVI, Panama, Bahamas on a timeline. | CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_ENTITIES | single table | timeline |  |
| crawl | **Middlemen ranked** | Which law firms and agents set up the most offshore companies? | Names. | CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_INTERMEDIARIES | single table | ranking |  |
| crawl | **Addresses with hundreds of companies** | Which UK addresses host the most registered companies? | The duplicate-address trick, counted. | CORPORATE_REGISTRY__INTL_UK_COMPANIES_HOUSE\|CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_ADDRESSES | stack, same shape | ranking | Several tables shown side by side, no join. If a join is wanted, it is not in the catalog. |
| crawl | **UK companies born and dying per day** | How many companies incorporate and dissolve each day? | A pulse chart. | CORPORATE_REGISTRY__INTL_UK_COMPANIES_HOUSE | single table | timeline |  |
| crawl | **Who controls UK companies, by nationality** | Which nationalities show up most as significant controllers? | 15.8M rows, partial load. | CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC | single table | ranking | Truncated load; counts are floors. |
| crawl | **Irish companies by status** | How many Irish companies are active versus dissolved, by year? | 821K rows. | CORPORATE_REGISTRY__INTL_IE_CRO | single table | timeline |  |
| walk | **Owners per UK company against sector** | Which sectors have the most layered ownership? | Catalog item 54. | CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC\|CORPORATE_REGISTRY__INTL_UK_COMPANIES_HOUSE | COMPANY_NO | other |  |
| walk | **Sanctioned names in UK filings** | Do sanctioned people appear as UK company controllers? | Name match across two lists. | CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC\|JUSTICE__INTL_UK_SANCTIONS_LIST | name | other | Not a catalog key. |

### Labor — 9 ideas

| Tier | Title | Question | Why it matters | Tables | Joins on | Visual | Notes |
|---|---|---|---|---|---|---|---|
| crawl | **Mine accident narratives** | What do the accident narratives say, by injury type and mine? | Text people will read. | LABOR__FED_MSHA_ACCIDENTS | single table | other |  |
| crawl | **Mine fines proposed versus paid** | Which operators pay the smallest share of proposed penalties? | Two columns, one gap. | LABOR__FED_MSHA_VIOLATIONS | single table | ranking | 3.1M citations. |
| crawl | **Mines open and closed** | Where are active mines, and where did they close? | Status on a map. | LABOR__FED_MSHA_MINES | single table | map |  |
| crawl | **Injury rate by establishment, three years** | Which employers' injury rates rose across 2023 to 2025? | Three yearly tables, one slope. | LABOR__FED_OSHA_ITA_300A_SUMMARY_2023\|LABOR__FED_OSHA_ITA_300A_SUMMARY_2024\|LABOR__FED_OSHA_ITA_300A_SUMMARY_2025 | EIN | timeline |  |
| crawl | **Injury narratives** | What happened, in the worker's words, by industry? | Case detail text. | LABOR__FED_OSHA_ITA_CASE_DETAIL_2023\|LABOR__FED_OSHA_ITA_CASE_DETAIL_2024\|LABOR__FED_OSHA_ITA_CASE_DETAIL_2025 | stack, same shape | other | Several tables shown side by side, no join. If a join is wanted, it is not in the catalog. |
| crawl | **Union membership since 2000** | Which unions grew and which shrank, by members and assets? | 617K filings. | LABOR__FED_DOL_OLMS | single table | timeline |  |
| crawl | **Pension funding gaps** | Which single-employer plans are furthest below their funding target? | Actuarial filings. | LABOR__FED_DOL_EBSA_FORM5500_SCHEDULE_SB | single table | ranking |  |
| walk | **Violations against accidents per mine** | Do mines with more citations have more accidents? | Catalog item 36. | LABOR__FED_MSHA_VIOLATIONS\|LABOR__FED_MSHA_ACCIDENTS\|LABOR__FED_MSHA_MINES | MSHA mine ID | other | Catalog item 58: keys in keyset, zero edges. Not a catalog key; lookup or unproven. |
| walk | **Suspicious injury numbers, queued** | Which company groups look like they under-report injuries? | Built review queue. | COHORT_QUEUE\|LABOR__FED_OSHA_ITA_300A_SUMMARY_2024 | EIN | ranking | REVIEW schema, internal. |

### Transport — 8 ideas

| Tier | Title | Question | Why it matters | Tables | Joins on | Visual | Notes |
|---|---|---|---|---|---|---|---|
| crawl | **Who owns the planes** | Which owners hold the most registered aircraft, by state? | 315K tail numbers. | TRANSPORT__FED_FAA_AIRCRAFT_REGISTRY | single table | map |  |
| crawl | **Rail deaths since 1975** | How did worker, passenger and trespasser deaths move over fifty years? | Three lines, one long axis. | TRANSPORT__FED_FRA_CASUALTIES\|TRANSPORT__FED_FRA_RAIL_DEATHS_BY_RAILROAD | stack, same shape | timeline | Several tables shown side by side, no join. If a join is wanted, it is not in the catalog. |
| crawl | **Crossings with no warning** | Where do trains hit cars at crossings with no signals? | Map with a filter. | TRANSPORT__FED_FRA_CROSSING_INCIDENTS | single table | map |  |
| crawl | **Derailments by cause** | What causes derailments, and which railroads have most per mile? | Cause codes as bars. | TRANSPORT__FED_FRA_EQUIPMENT_ACCIDENTS | single table | ranking |  |
| crawl | **Plane crashes map** | Where do crashes happen, and in what weather? | 31K events. | TRANSPORT__FED_NTSB_AVIATION_EVENTS | single table | map |  |
| crawl | **Crashes by aircraft make** | Which makes and models crash most, per registered aircraft? | Needs the registry for the denominator. | TRANSPORT__FED_NTSB_AVIATION_AIRCRAFT\|TRANSPORT__FED_FAA_AIRCRAFT_REGISTRY | tail number | ranking | Not a catalog key. |
| crawl | **Ship tracks** | What do 58M position pings look like on a coast? | The wow map. | MARITIME__FED_NOAA_AIS | single table | map | MARITIME schema. |
| walk | **Ships per owner against port calls** | Which owners run the most vessels, and where do they call? | Catalog item 60. | MARITIME__FED_NOAA_AIS\|JUSTICE__FED_OFAC_SDN | IMO / MMSI | other | 2 tables, zero edges. Sanctioned ships on AIS is the story. |

### Consumer Safety — 6 ideas

| Tier | Title | Question | Why it matters | Tables | Joins on | Visual | Notes |
|---|---|---|---|---|---|---|---|
| crawl | **What sends kids to the ER** | Which products injure which age groups most? | 9.8M ER visits. | CONSUMER_SAFETY__FED_CPSC_NEISS\|EDUCATION__FED_CPSC_NEISS_CODES | code | ranking | Decoder table is misfiled under EDUCATION. Not a catalog key; lookup or unproven. |
| crawl | **Car complaints by model** | Which make-model-years draw the most complaints, and about what? | 2.2M complaints. | CONSUMER_SAFETY__FED_NHTSA_COMPLAINTS | single table | ranking |  |
| crawl | **Investigation to recall lag** | How long from investigation opening to recall, by maker? | Time as the story. | CONSUMER_SAFETY__FED_NHTSA_INVESTIGATIONS | single table | timeline |  |
| crawl | **Biggest recalls** | Which recalls affected the most vehicles? | Ranking. | CONSUMER_SAFETY__FED_NHTSA_RECALLS | single table | ranking |  |
| crawl | **Complaints about financial companies** | Which companies draw the most CFPB complaints per product, and how do they respond? | 17M complaints. | CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS | single table | ranking |  |
| walk | **Complaints before recalls** | Did complaints spike before the recall for the same model? | Two NHTSA tables on make-model-year. | CONSUMER_SAFETY__FED_NHTSA_COMPLAINTS\|CONSUMER_SAFETY__FED_NHTSA_RECALLS | make + model + year | timeline | Not a catalog key. |

### Science — 8 ideas

| Tier | Title | Question | Why it matters | Tables | Joins on | Visual | Notes |
|---|---|---|---|---|---|---|---|
| crawl | **Earthquakes since records** | Where and how deep, magnitude 2.5 and up? | 443K quakes, one map. | SCIENCE__FED_USGS_EARTHQUAKES | single table | map |  |
| crawl | **NIH money by institution, 27 years** | Which institutions and states won the most NIH funding, year by year? | 2.1M applications. | SCIENCE_RESEARCH__FED_NIH_REPORTER | single table | timeline |  |
| crawl | **Review panels that fund most** | Which study sections score the most funded applications? | Inside baseball, but visible. | SCIENCE_RESEARCH__FED_NIH_REPORTER | single table | ranking |  |
| crawl | **SBIR repeat winners** | Which companies win SBIR awards year after year? | The mills. | SCIENCE_RESEARCH__FED_SBIR_STTR_AWARDS | single table | ranking |  |
| crawl | **Why papers get retracted** | Which reasons, journals, and countries dominate retractions by year? | 71K retractions. | SCIENCE_RESEARCH__FED_RETRACTION_WATCH\|SCIENCE_RESEARCH__XC_RETRACTION_WATCH_DATABASE | stack, same shape | timeline | Two overlapping copies. |
| crawl | **Preprints that got published** | What share of preprints made it to a journal, and how fast? | 432 rows. | SCIENCE_RESEARCH__XC_BIORXIV_MEDRXIV | single table | other |  |
| walk | **Retractions per institution** | Which research organizations have the most retracted papers? | Retraction list meets the org registry. | SCIENCE_RESEARCH__FED_RETRACTION_WATCH\|REFERENCE__XC_ROR_RESEARCH_ORGANIZATIONS | institution name | ranking | Name match, not a catalog key. |
| walk | **NIH grants against retractions** | Do the most-funded institutions also retract most? | Money and mistakes. | SCIENCE_RESEARCH__FED_NIH_REPORTER\|SCIENCE_RESEARCH__FED_RETRACTION_WATCH | institution name | other | Name match. Not a catalog key; lookup or unproven. |

### Education — 6 ideas

| Tier | Title | Question | Why it matters | Tables | Joins on | Visual | Notes |
|---|---|---|---|---|---|---|---|
| crawl | **Debt against earnings by college** | Which colleges leave graduates with the most debt per dollar earned? | One dot per school. | EDUCATION__FED_ED_COLLEGE_SCORECARD_INSTITUTION | single table | other |  |
| crawl | **Admission rate against tuition** | Are the most selective schools the most expensive? | Another scatter from the same table. | EDUCATION__FED_ED_COLLEGE_SCORECARD_INSTITUTION | single table | other |  |
| crawl | **The yield curve, every day** | When did short rates go above long rates? | Inversions as shaded bands. | EDUCATION__FED_FRB_H15_SELECTED_RATES | single table | timeline | Misfiled under EDUCATION. |
| crawl | **Commodity speculators versus hedgers** | How did speculator share move in each commodity market? | Weekly, per market. | EDUCATION__FED_CFTC_COT_FUTURES | single table | timeline | Misfiled under EDUCATION. |
| crawl | **Political ad spend by region** | Which regions got the most political ad money? | Google's own totals. | EDUCATION__FED_GOOGLE_POLADS_GEO_SPEND\|EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_GEO_SPEND | stack, same shape | map | Misfiled. |
| crawl | **Lobbying issues over time** | Which issue codes got lobbied most each quarter? | 820K filings. | EDUCATION__FED_SENATE_LDA_FILINGS | single table | timeline | Misfiled. |

### Reference — 9 ideas

| Tier | Title | Question | Why it matters | Tables | Joins on | Visual | Notes |
|---|---|---|---|---|---|---|---|
| crawl | **The tree of life** | How do 993K species entries nest from kingdom down? | A sunburst of everything named. | REFERENCE__FED_ITIS_TAXONOMIC_UNITS\|REFERENCE__FED_ITIS_HIERARCHY | stack, same shape | other | Several tables shown side by side, no join. If a join is wanted, it is not in the catalog. |
| crawl | **Common names in many languages** | Which species have the most common names, in which languages? | Names are stories. | REFERENCE__FED_ITIS_VERNACULARS | single table | ranking |  |
| crawl | **Native or introduced, by state** | Which states have the most introduced species listed? | A map of invaders. | REFERENCE__FED_ITIS_JURISDICTION | single table | map |  |
| crawl | **Rejected species names** | How many old names point to each accepted one? | Science changing its mind, counted. | REFERENCE__FED_ITIS_SYNONYM_LINKS | single table | ranking |  |
| crawl | **Place names of America** | Which names repeat most across the country, and where? | 1.2M names, one search box. | REFERENCE__FED_USGS_GNIS_ALL_NAMES | single table | map | Historical and variant names included. |
| crawl | **Global news events, toned** | Which country pairs generate the most news events, and how negative? | A GDELT sample. | REFERENCE__INTL_GDELT | single table | other | 1,015 rows only. |
| crawl | **Research organizations of the world** | Where are the universities and labs, by type? | 135K orgs on a map. | REFERENCE__XC_ROR_RESEARCH_ORGANIZATIONS | single table | map |  |
| crawl | **Fertility by country** | Which countries fell below replacement and when? | A world map crossing a line. | REFERENCE__XC_OWID_FERTILITY | single table | timeline |  |
| crawl | **County shapes and water** | Which counties are mostly water? | A geometry oddity chart. | REFERENCE__CENSUS_CB_COUNTY | single table | map |  |

### Timeline — 3 ideas

| Tier | Title | Question | Why it matters | Tables | Joins on | Visual | Notes |
|---|---|---|---|---|---|---|---|
| crawl | **What years the warehouse actually covers** | Which subjects have data for which years, and where are the holes? | A heatmap of the shelf itself. | TIMELINE__HEALTH_INDEX\|TIMELINE__POLITICS_INDEX\|TIMELINE__ENVIRONMENT_INDEX\|TIMELINE__JUSTICE_INDEX\|TIMELINE__FINANCE_INDEX\|TIMELINE__ECONOMICS_INDEX\|TIMELINE__TRANSPORT_INDEX\|TIMELINE__LABOR_INDEX\|TIMELINE__HOUSING_INDEX\|TIMELINE__IMMIGRATION_INDEX\|TIMELINE__CORPORATE_REGISTRY_INDEX | date | other | Same date axis. Meta chart, not source data. Not a catalog key; lookup or unproven. |
| crawl | **Which tables have a usable date** | How many tables carry a date, at what granularity? | The registry is a shape chart. | RIPPLE_TIME_REGISTRY | single table | other | Internal bookkeeping. |
| run | **Everything that happened on one day** | For a chosen date: every record across subjects, on one strip? | The warehouse as a newspaper. | REFERENCE__CALENDAR\|TIMELINE__POLITICS_INDEX\|TIMELINE__JUSTICE_INDEX\|TIMELINE__HEALTH_INDEX\|TIMELINE__ENVIRONMENT_INDEX\|TIMELINE__FINANCE_INDEX | date | timeline | Not a catalog key; lookup or unproven. |

### Open Data — 3 ideas

| Tier | Title | Question | Why it matters | Tables | Joins on | Visual | Notes |
|---|---|---|---|---|---|---|---|
| crawl | **France's most downloaded datasets** | Which datasets do people actually use, and how good are they? | View counts and quality score. | OPEN_DATA__INTL_FR_DATA_GOUV | single table | ranking | Do not join on GEO_IN; catalog trap. |
| crawl | **Open-data catalogs compared** | How big and how tagged are ten countries' catalogs? | One bar chart of samples. | OPEN_DATA__INTL_FR_DATA_GOUV\|OPEN_DATA__INTL_DE_GOVDATA\|OPEN_DATA__INTL_CH_OPENDATASWISS\|OPEN_DATA__INTL_GR_DATAGOV\|OPEN_DATA__INTL_AR_DATOSGOB\|OPEN_DATA__INTL_CL_DATOSGOB\|OPEN_DATA__INTL_CA_OPEN_CANADA | stack, same shape | ranking | Most are samples. |
| crawl | **DOJ Epstein pages over time** | Which DOJ pages changed, appeared, or vanished, and when? | 1.5M snapshots as a change timeline. | OPEN_DATA__XC_WAYBACK_DOJ_EPSTEIN\|FCT_WAYBACK_PAGE_CHANGES\|FCT_LIBRARY_SNAPSHOT\|FCT_DATASET_SIZE_HISTORY | URL | timeline | EPSTEIN and INVESTIGATIONS schemas hold the siblings. Not a catalog key; lookup or unproven. |

### History — 3 ideas

| Tier | Title | Question | Why it matters | Tables | Joins on | Visual | Notes |
|---|---|---|---|---|---|---|---|
| crawl | **Slave voyages, port to port** | Which ports sent and received the most voyages, and how many died at sea? | A flow map across an ocean. | HISTORY__FED_SLAVEVOYAGES_TRANSATLANTIC\|HISTORICAL_RECORDS__FED_SLAVEVOYAGES_INTRAAMERICAN | stack, same shape | flow | Column names are research codes. |
| crawl | **Voyages per year** | How did voyage counts and survival rates change across three centuries? | One long timeline. | HISTORY__FED_SLAVEVOYAGES_TRANSATLANTIC | single table | timeline |  |
| crawl | **WPA narratives** | What subjects did formerly enslaved people talk about, by state? | 100 full transcripts. | HISTORY__FED_WPA_SLAVE_NARRATIVES | single table | other |  |

### Procurement — 2 ideas

| Tier | Title | Question | Why it matters | Tables | Joins on | Visual | Notes |
|---|---|---|---|---|---|---|---|
| crawl | **Who is banned from federal business** | Which agencies exclude most, for what reasons, and how many are active? | 168K exclusions. | PROCUREMENT__FED_SAM_EXCLUSIONS | single table | ranking |  |
| crawl | **Ecuador's contract winners** | Which bidders win most, and how concentrated is it? | Open-contracting data. | PROCUREMENT__INTL_EC_SERCOP | single table | ranking |  |

### Other — 6 ideas

| Tier | Title | Question | Why it matters | Tables | Joins on | Visual | Notes |
|---|---|---|---|---|---|---|---|
| crawl | **Multistate settlements** | Which industries paid the most in multistate settlements, led by which states? | 882 cases. | LEGAL_ENFORCEMENT__FED_NAAG_MULTISTATE_SETTLEMENTS | single table | ranking |  |
| crawl | **Tribal land map** | Where are tribal land areas and how big? | 335 shapes. | LAND_AND_TERRITORY__FED_BIA_TRIBAL_GEO | single table | map |  |
| crawl | **Russian operations in Europe** | Where, when, and against what kind of target? | 150 rows. | INVESTIGATIONS__INTL_LEIDEN_RUSSIAN_OPS_EUROPE | single table | map |  |
| crawl | **Warehouse table sizes** | How big is each table, and which subjects hold the rows? | A treemap of the shelf. |  | none | other | Meta. Source is the inventory file, not a table. |
| run | **One county, every table** | For one FIPS: jobs, overdoses, jail, facilities, storms, aid, providers, water? | The county card. | DIM_COUNTY\|ECONOMICS__FED_BLS_QCEW\|HEALTH__FED_CDC_DRUG_POISONING_COUNTY\|JUSTICE__XC_VERA_INCARCERATION_TRENDS\|ENVIRONMENT__FED_EPA_FRS_FACILITIES\|ENVIRONMENT__FED_NOAA_STORM_EVENTS\|HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS\|HEALTH__FED_HRSA_SHORTAGE_AREAS | FIPS | other | FIPS: 15 tables, 78 edges. Catalog item 61 for population. |
| run | **One country, every table** | For one country: freedom, corruption, CO2, life expectancy, debt, conflict, sanctions, aid? | The country card. | POLITICS__INTL_FREEDOMHOUSE\|POLITICS__XC_OWID_CPI\|ENVIRONMENT__XC_OWID_CO2\|HEALTH__XC_OWID_LIFE_EXPECTANCY\|FINANCE__INTL_WB_IDS\|JUSTICE__INTL_UCDP_GED\|ECONOMICS__FED_FOREIGNASSISTANCE\|POLITICS__INTL_OWID_MILSPEND | country code | other | Country code is a lookup, not a catalog key. |



---

## Reading notes behind the v2 catalog

Table-by-table triage from the recon pass that built v2: what's usable,
what's a dead end, what's misfiled, what's wanted but missing.

Recon pass: read all 704 inventory rows; 437 cited in ideas, 267 accounted for below and the 2026-09-04 join catalog.
Output: `docket/docket_v2_2026-09-07.csv`, 392 ideas.

```
subject              crawl  walk  run   total
HEALTH                  40    20    5      65
POLITICS                36    13    4      53
JUSTICE                 38    11    3      52
ENVIRONMENT             25    15    4      44
ECONOMICS               24    10    2      36
FINANCE                 18     8    1      27
ENERGY                  14     2    1      17
HOUSING                 11     3    0      14
IMMIGRATION             10     2    0      12
the rest                61     8    3      72
```

## How the join rule was applied

The catalog names key families and counts, not table pairs.
So `joins_on` cites the key family. Notes say when the pair itself is unproven.

| joins_on value | Meaning |
|---|---|
| NPI, EIN, FRS_ID, CCN, CIK, FIPS, NPDES_ID, PWSID, FEC ids, LEI, CL_PERSON_ID | proven family in the catalog |
| EIA_PLANT_ID, UTILITY_ID, MSHA ids, FDIC_CERT, IMO / MMSI, CUSIP bridge | in keyset, zero edges; flagged in notes |
| DOCKET | 17 tables, 2 edges; flagged |
| same-source ID, name, ticker, product code, state, country, year | not a catalog key; lookup or unproven; flagged |

## What I found, by subject

**HEALTH** — the richest shelf. NPI is steel and ties pharma money, prescribing, billing, bans and hospital ties.
The opioid chain is the run: ARCOS, Part D, Open Payments, county deaths, treatment sites. Every hop is a catalog key.
Three built tables are one chart each: meal-cap fingerprint, addiction prescribers paid, nursing home relief by chain.
FAERS is three tables sharing a report ID that the catalog does not carry.

**POLITICS** — the member card is ready: master list, ideology, votes, bills, committees, money, trades all on Bioguide.
Texas and California lobbying are complete mini-warehouses on their own filer IDs.
Senators trading in sectors their committees oversee needs a ticker-to-industry lookup that does not exist.
Google political ads, Senate LDA filings and CFTC positioning are misfiled under EDUCATION.

**ENVIRONMENT** — FRS_ID, NPDES_ID and PWSID each support a full facility page.
"Your tap water" by zip is the reader-lookup with the widest appeal.
EIA plant and utility keys are in the keyset with zero edges, so eGRID against owner waits on that build.

**JUSTICE** — CL_PERSON_ID carries a judge card: bio, courts, disclosures, gifts, trips, holdings.
The four FJC IDB files are fifty years of federal court by district.
DOCKET is mostly unproven so opinions-per-case ideas are flagged.
Sanctions lists join only by name.

**FINANCE** — CIK gives a company card. Cross-key legs to EIN and UEI are 2 to 16 percent; sample, never rate.
Two Senate trade sources disagree; the combined table carries a confidence column, which is itself a chart.
FEC individual contributions is 284M rows; PUBLIC rollups exist and should go first.

**ECONOMICS** — EIN is the second steel key: BMF, e-file index, revocations, single audits, Pub78, hospital pay.
Treasury daily tables are pure timelines with no join needed.
GLEIF gives corporate family trees and, through LEI, reaches EPA facilities.

**ENERGY** — EIA-860 and 861 are 2024-only snapshots except generators, which carry build and retirement dates.
Several 861 tables lost a header row on load; counts are off by one.

**HOUSING** — HMDA historic is 45M rows for 2015 to 2017 only. The other HMDA tables are DC-only or samples.
Redlining against denial rates needs a spatial join the catalog does not carry.
FEMA housing registrations is a 12 percent partial load cut mid-load, not a sample.

**IMMIGRATION** — EOIR cases and ICE stints are the two big files. Person IDs are anonymized and not in the catalog.
Three tables are misfiled here: hospice enrollments, Medicare FFS enrollment, SDWA service areas.

**TIMELINE** — index tables count rows per day per source. They chart the warehouse, not the world.

**REFERENCE** — ITIS is a full tree of life. GNIS is 1.2M place names. Both are single-table wow charts.

## Tables I could not make anything of, and why

| Table | Why |
|---|---|
| everything in `_RESTORE_20260907` | backup copies, 0 to 50 rows |
| `*__PREV_*` snapshots, 9 tables | prior-version copies |
| `TIMELINE__*_INDEX` stubs: CRIMINAL_JUSTICE, HISTORY, INVESTIGATIONS, JUDICIARY, MARITIME, MONEY_FINANCE | 1 to 21 rows |
| `HEALTH__FED_CDC_DATA_PORTAL`, `HEALTH__FED_CMS_MAIN`, `ECONOMICS__INTL_FAO_FAOSTAT`, `TRANSPORT__FED_DOT_BTS`, `SCIENCE__FED_NASA_OPEN_DATA` | catalogs of datasets, not data |
| `HEALTH__FED_FDA_GUDID__STAGING`, `HEALTH__FED_VA_SUICIDE_APPENDIX` | raw or unparsed |
| `HEALTH__FED_CMS_FISCAL_INTERMEDIARY_*`, `HEALTH__FED_CMS_PENDING_*`, `HEALTH__FED_NLM_DAILYMED_SPL_SETID_MAP`, `HEALTH__FED_FDA_UNII_GSRS_SUBSTANCES` | name and ID lookups |
| `HEALTH__FED_CMS_AMBULATORY_SPECIALTY_MODEL_PARTICIPANTS`, `HEALTH__FED_CMS_MEDICARE_DIABETES_PREVENTION_PROGRAM` | rosters with nothing to measure |
| `POLITICS__FED_FEC_API`, `ENVIRONMENT__FED_EPA_ENVIROFACTS`, `ECONOMICS__FED_GRANTS_GOV`, `ECONOMICS__FED_IRS_990`, `ECONOMICS__FED_SEC_EDGAR`, `ECONOMICS__FED_US_USASPENDING_API`, `REFERENCE__FED_DHS_HIFLD`, `PROCUREMENT__FED_USASPENDING_BULK`, `PROCUREMENT__FED_USASPENDING_SUBAWARDS`, `HOUSING__FED_CFPB_HMDA`, `HOUSING__FED_CFPB_HMDA_LAR`, `SCIENCE_RESEARCH__XC_OSF_REGISTRATIONS`, `GOVERNMENT_RECORDS__FED_NARA_AAD` | test samples, shape only |
| `IMMIGRATION__FED_EOIR_CASE_DATA` | one column, broken load |
| `IMMIGRATION__FED_CBP_ENCOUNTERS`, `IMMIGRATION__FED_DHS_YEARBOOK`, `JUSTICE__FED_BOP_STATISTICS`, `JUSTICE__FED_DOJ_FCA_SETTLEMENTS`, `JUSTICE__INTL_AUSTLII`, `JUSTICE__INTL_EURLEX_CELLAR`, `JUSTICE__INTL_EU_SOCTA_EUROPOL`, `ENVIRONMENT__INTL_GEM_HAZARD`, `ENVIRONMENT__FED_NOAA_WEATHER_API`, `ENERGY__FED_EIA861_MERGERS`, `ENERGY__FED_EIA861_DELIVERY_COMPANIES`, `SCIENCE__XC_OWID_AI_INCIDENTS_ANNUAL`, `SCIENCE__INTL_EMBL_ENSEMBL`, `JUDICIARY__FED_OYEZ`, `CORPORATE_REGISTRY__INTL_ES_BORME`, `OPEN_DATA__INTL_GE_DATAGOV`, `OPEN_DATA__INTL_GH_DATAGOVGH`, `OPEN_DATA__INTL_ES_DATOSGOB`, `HISTORY__FED_DENSHO_DDR`, `HISTORY__FED_DOCSOUTH`, `TRANSPORT__FED_FRA_SAFETY`, `TRANSPORT__FED_FAA_ADIP_PRIVATE_AIRPORTS`, `EDUCATION__FED_FRB_Z1_CSV`, `HOUSING__FED_HUD_DATA` | too small, empty, or unreadable |
| `REFERENCE__FED_ITIS_*` support tables: COMMENTS, EXPERTS, PUBLICATIONS, REFERENCE_LINKS, STRIPPEDAUTHOR, TAXON_AUTHORS_LKP, TAXON_UNIT_TYPES, TU_COMMENTS_LINKS, VERN_REF_LINKS, NODC_IDS, OTHER_SOURCES, KINGDOMS, GEOGRAPHIC_DIV, LONGNAMES | citation plumbing |
| `ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_POLLUTANTS`, `*_PROGRAMS`, `*_PROGRAM_SUBPARTS`, `ENVIRONMENT__FED_EPA_FRS_FRS_NAICS_CODES`, `*_SIC_CODES`, `RCRA_NAICS` | code lookups |
| `ENVIRONMENT__FED_EPA_RCRA_RCRA_*` five tables | stripped duplicates of the RCRA set |
| `ENVIRONMENT__FED_USCG_NRC_INCIDENT_REPORTS`, `ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES`, `HEALTH__FED_CMS_HOSPITAL_GENERAL`, `HEALTH__FED_CMS_MEDICARE_PROVIDER`, `HEALTH__FED_CMS_OPEN_PAYMENTS_2022`, `_2023`, `FINANCE__FED_FEC_BULK*`, `ECONOMICS__FED_IRS_527_ORGS`, `CORPORATE_REGISTRY__FED_IRS_EO_BMF`, `ECONOMICS__FED_SEC_EDGAR_COMPANY_TICKERS`, `ECONOMICS__FED_US_SEC_EDGAR`, `POLITICS__XC_JCS_*`, `POLITICS__BILLS`, `POLITICS__BILL_COSPONSORS`, `POLITICS__VOTEVIEW_ROLLCALLS` | duplicates of a fuller sibling |
| `REFERENCE__CALENDAR`, `DIM_DATE`, `DIM_TRACT`, `REF__DIM_GEOGRAPHY`, `REF__DIM_STATE`, `DIM_STATE`, `REFERENCE__CENSUS_CB_STATE`, `REFERENCE__CENSUS_CB_ZCTA`, `REFERENCE__XC_CROSSREF_FUNDER_REGISTRY` | lookups; used as joins, not subjects |
| `LEAD_QUEUE`, `COHORT_QUEUE` | internal review queues |
| `FINANCE__FED_EPA_ICIS_FEC_*` four tables | EPA case tables misfiled under FINANCE; overlap ECHO |
| `POLITICS__FED_DOJ_EPSTEIN_LIBRARY`, `INVESTIGATIONS__XC_WAYBACK_REPLAY_DOJ_*` | link scrapes; folded into the DOJ pages idea |
| `REFERENCE__INTL_EG_CAPMAS`, `REFERENCE__INTL_EUROSTAT`, `ECONOMICS__INTL_IT_ISTAT`, `REFERENCE__FED_USGS_TOPOVIEW`, `TRANSPORT__FED_NTSB_AVIATION_INJURY`, `ENVIRONMENT__FED_USGS_WBD_HUC8`, `ENVIRONMENT__FED_WQP_MONITORING_STATIONS`, `HEALTH__INTL_HEALTHCANADA_DPD_DRUG`, `HEALTH__FED_FDA_DRUG_MASTER_FILES`, `HEALTH__FED_FDA_PURPLE_BOOK`, `HEALTH__FED_FDA_CAERS`, `HEALTH__FED_FDA_DRUG_ENFORCEMENT`, `HEALTH__FED_FDA_ESTABLISHMENT_REG`, `FINANCE__FED_OCC_*`, `FINANCE__FED_MSRB_REGISTRANTS`, `FINANCE__FED_FINRA_MPID_LIST`, `FINANCE__INTL_OSFI_REGULATED_FI`, `FINANCE__FED_SEC_BUSINESS_DEVELOPMENT_COMPANY_REPORT`, `FINANCE__FED_SEC_CLOSED_END_FUND_INFORMATION`, `FINANCE__FED_SEC_INVESTMENT_COMPANY_SERIES_CLASS`, `FINANCE__FED_FDIC_BANK_DATA`, `FINANCE__FED_NCUA_CALL_REPORTS_FOICU`, `FINANCE__FED_NCUA_CHARTER_MERGER_EVENTS`, `ECONOMICS__FED_IRS_EO_PR`, `ECONOMICS__FED_IRS_SOI_CHARITIES`, `ECONOMICS__FED_PBGC_DATA`, `ECONOMICS__FED_USASPENDING_TOPTIER_AGENCIES`, `ECONOMICS__XC_WIKIPEDIA_LARGEST_US_COMPANIES`, `ENERGY__FED_EIA861_*` minor sections, `SCIENCE__FED_NSF_AWARDS`, `CRIMINAL_JUSTICE__FED_BJS_DATA`, `GOVERNMENT_RECORDS__FED_USASPENDING_TAS_FILTER_TREE`, `ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FCES_PCES`, `*_FORMAL_ACTIONS`, `*_INFORMAL_ACTIONS`, `*_VIOLATION_HISTORY`, `ENVIRONMENT__FED_EPA_RCRA_ENFORCEMENTS`, `*_EVALUATIONS`, `*_FACILITIES`, `*_VIOLATIONS`, `ENVIRONMENT__FED_EPA_SDWA_SDWA_FACILITIES`, `*_PN_VIOLATION_ASSOC`, `ENVIRONMENT__FED_EPA_NPDES_NPDES_CS_VIOLATIONS`, `*_INFORMAL_ENFORCEMENT_ACTIONS`, `HEALTH__FED_CMS_HOSPICE`, `HEALTH__FED_CMS_IRF`, `HEALTH__FED_CMS_LTCH`, `HEALTH__FED_CMS_*_ENROLLMENTS`, `HEALTH__FED_CMS_MEDICARE_OUTPATIENT_*`, `HEALTH__FED_CMS_MEDICARE_INPATIENT_HOSPITALS_BY_PROVIDER`, `HEALTH__FED_CMS_MEDICARE_DIALYSIS_FACILITIES`, `HEALTH__FED_CMS_MEDICARE_DURABLE_*_BY_REFER`, `HEALTH__FED_HRSA_UDS_HEALTH_CENTER_INFO`, `*_TABLE3A_PATIENTS`, `HEALTH__FED_VA_ALLCAUSE_MORTALITY`, `HEALTH__FED_VA_SUICIDE_NATIONAL`, `HEALTH__FED_CDC_WONDER`, `POLITICS__CA_LOBBY_AMENDMENTS`, `*_CHG_LOG`, `*_COVER`, `*_COVER2`, `*_EMP_LOBBYIST`, `*_FIRM_LOBBYIST`, `POLITICS__IRS527_EAIN`, `POLITICS__FED_SENATE_EFD_FILINGS`, `POLITICS__FJC_SCOTUS_CROSSWALK`, `POLITICS__SCOTUS_JUSTICE`, `POLITICS__MEMBER_CROSSWALK`, `POLITICS__MEMBER_MONEY_RAISED`, `POLITICS__FED_GOVINFO_BILLSTATUS`, `POLITICS__FED_CONGRESS_LEGISLATORS`, `POLITICS__TX_LOBBY_DOCKETS`, `JUSTICE__FED_COURTLISTENER_COURT_APPEALS_TO`, `*_RACE_CODES`, `*_DISCLOSURE_AGREEMENTS`, `*_DISCLOSURE_NON_INVESTMENT_INCOME`, `*_ORIGINATING_COURT_INFO`, `JUSTICE__FED_FHFA_SUSPENDED_COUNTERPARTIES`, `HOUSING__FED_FHFA_SUSPENDED_COUNTERPARTY`, `HOUSING__FED_FHFA_NMDB`, `HOUSING__FED_CFPB_HMDA_DC_ONLY`, `IMMIGRATION__FED_ICE_STATISTICS`, `CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_OTHERS`, `OPEN_DATA__INTL_*` small samples, `EDUCATION__FED_ED_NCES_CIP_CODES`, `EDUCATION__FED_GOOGLE_POLADS_*_ID_MAPPING`, `*_ADVERTISER_DECLARED_STATS`, `*_ADVERTISER_STATS`, `LABOR__FED_PBGC_TRUSTEED_PLANS` | usable but nothing made me look twice; supporting cast for a run, not a chart on their own |

## Tables I wanted and do not have

| Wanted | For |
|---|---|
| ticker to industry lookup | senators trading in sectors their committees oversee |
| FTD_CUSIP_BRIDGE named in the catalog | 13F holdings by issuer; not in the inventory |
| FAERS report-ID key in the catalog | drug side-effect story across three tables |
| EIA plant and utility edges | every eGRID against owner idea |
| county population by year | any per-resident rate before 2020 |
| a full HMDA post-2018 load | denial rates today, not 2015 to 2017 |
| full FEMA IA load | disaster aid totals |
| judge code to FJC judge crosswalk | sentencing by judge |
| tract-level HMDA geocode | redlining then, denied now |

## Misfiled tables spotted

| Table | Sits in | Belongs in |
|---|---|---|
| `EDUCATION__FED_SENATE_LDA_FILINGS` | EDUCATION | POLITICS |
| `EDUCATION__FED_GOOGLE_POLADS_*` 8 tables | EDUCATION | POLITICS |
| `EDUCATION__FED_CFTC_COT_*`, `EDUCATION__FED_FRB_*` | EDUCATION | FINANCE |
| `EDUCATION__FED_CPSC_NEISS_CODES` | EDUCATION | CONSUMER_SAFETY |
| `IMMIGRATION__FED_CMS_*` 2 tables | IMMIGRATION | HEALTH |
| `IMMIGRATION__FED_EPA_SDWA_SDWA_SERVICE_AREAS` | IMMIGRATION | ENVIRONMENT |
| `FINANCE__FED_EPA_ICIS_FEC_*` 4 tables | FINANCE | ENVIRONMENT |
| `FINANCE__FED_FEC_*`, `FINANCE__FED_IRS527_*` | FINANCE | POLITICS |
| `JUSTICE__FED_FDIC_ENFORCEMENT_ORDERS` | JUSTICE | FINANCE |
| `ECONOMICS__FED_IRS_527_ORGS` | ECONOMICS | POLITICS |


## Appendix: every table not cited in an idea, with the reason

267 tables. Machine-grouped by description keywords, then read once by eye.

**supporting cast, nothing made me look twice** — 134

- `CORPORATE_REGISTRY__FED_ICIJ_OFFSHORELEAKS_OTHERS`
- `CRIMINAL_JUSTICE__FED_BJS_DATA`
- `ECONOMICS__FED_IRS_527_ORGS`
- `ECONOMICS__FED_IRS_EO_PR`
- `ECONOMICS__FED_PBGC_DATA`
- `ECONOMICS__FED_SEC_EDGAR`
- `ECONOMICS__FED_TREASURY_DEBT_OUTSTANDING`
- `ECONOMICS__FED_USASPENDING_TOPTIER_AGENCIES`
- `ECONOMICS__INTL_IT_ISTAT`
- `ECONOMICS__XC_WIKIPEDIA_LARGEST_US_COMPANIES`
- `EDUCATION__FED_FRB_Z1_CSV`
- `EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_DECLARED_STATS`
- `EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_STATS`
- `ENERGY__FED_EIA860_3_5_MULTIFUEL`
- `ENERGY__FED_EIA860_6_1_ENVIROASSOC`
- `ENERGY__FED_EIA861_DISTRIBUTION_SYSTEMS`
- `ENERGY__FED_EIA861_DYNAMIC_PRICING`
- `ENERGY__FED_EIA861_FRAME`
- `ENERGY__FED_EIA861_NON_NET_METERING_DISTRIBUTED`
- `ENERGY__FED_EIA861_OPERATIONAL_DATA`
- `ENERGY__FED_EIA861_SALES_ULT_CUST_CS`
- `ENERGY__FED_EIA861_SHORT_FORM`
- `ENERGY__FED_EIA_861_BALANCING_AUTHORITY`
- `ENVIRONMENT__FED_EPA_FRS_FRS_NAICS_CODES`
- `ENVIRONMENT__FED_EPA_FRS_FRS_SIC_CODES`
- `ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FCES_PCES`
- `ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS`
- `ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS`
- `ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAMS`
- `ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAM_SUBPARTS`
- `ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY`
- `ENVIRONMENT__FED_EPA_NPDES_NPDES_CS_VIOLATIONS`
- `ENVIRONMENT__FED_EPA_NPDES_NPDES_INFORMAL_ENFORCEMENT_ACTIONS`
- `ENVIRONMENT__FED_EPA_RCRA_ENFORCEMENTS`
- `ENVIRONMENT__FED_EPA_RCRA_EVALUATIONS`
- `ENVIRONMENT__FED_EPA_RCRA_FACILITIES`
- `ENVIRONMENT__FED_EPA_RCRA_RCRA_NAICS`
- `ENVIRONMENT__FED_EPA_RCRA_VIOLATIONS`
- `ENVIRONMENT__FED_EPA_SDWA_SDWA_FACILITIES`
- `ENVIRONMENT__FED_NOAA_WEATHER_API`
- `ENVIRONMENT__FED_WQP_MONITORING_STATIONS`
- `FINANCE__FED_EPA_ICIS_FEC_CASE_ENFORCEMENT_CONCLUSION_FACILITIES`
- `FINANCE__FED_EPA_ICIS_FEC_CASE_FACILITIES`
- `FINANCE__FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS`
- `FINANCE__FED_EPA_ICIS_FEC_ICIS_FEC_EPA_INSPECTIONS`
- `FINANCE__FED_FEC_BULK`
- `FINANCE__FED_FINRA_MPID_LIST`
- `FINANCE__FED_MSRB_REGISTRANTS`
- `FINANCE__FED_NCUA_CALL_REPORTS_FOICU`
- `FINANCE__FED_SEC_BUSINESS_DEVELOPMENT_COMPANY_REPORT`
- `FINANCE__FED_SEC_CLOSED_END_FUND_INFORMATION`
- `FINANCE__FED_SEC_INSIDER_DERIV_TRANS`
- `FINANCE__FED_SEC_INSIDER_SUBMISSION`
- `FINANCE__FED_SEC_INVESTMENT_COMPANY_SERIES_CLASS`
- `FINANCE__INTL_OSFI_REGULATED_FI`
- `HEALTH_MEDICINE__MEDICARE_PROVIDER_BY_STATE_TYPE_AGG`
- `HEALTH_MEDICINE__OPEN_PAYMENTS_BY_MFR_NATURE_AGG`
- `HEALTH_MEDICINE__PART_D_BY_STATE_TYPE_AGG`
- `HEALTH__FED_CDC_WONDER`
- `HEALTH__FED_CMS_AMBULATORY_SPECIALTY_MODEL_PARTICIPANTS`
- `HEALTH__FED_CMS_FEDERALLY_QUALIFIED_HEALTH_CENTER_ENROLLMENTS`
- `HEALTH__FED_CMS_HOSPICE`
- `HEALTH__FED_CMS_IRF`
- `HEALTH__FED_CMS_LTCH`
- `HEALTH__FED_CMS_MEDICARE_DIABETES_PREVENTION_PROGRAM`
- `HEALTH__FED_CMS_MEDICARE_DIALYSIS_FACILITIES`
- `HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_REFER`
- `HEALTH__FED_CMS_MEDICARE_INPATIENT_HOSPITALS_BY_PROVIDER`
- `HEALTH__FED_CMS_MEDICARE_OUTPATIENT_HOSPITALS_BY_PROVIDER_AND_SERVICE`
- `HEALTH__FED_CMS_OPEN_PAYMENTS_PROFILE_SUPPLEMENT`
- `HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_NON_PHYSICIANS`
- `HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS`
- `HEALTH__FED_CMS_RURAL_HEALTH_CLINIC_ENROLLMENTS`
- `HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS`
- `HEALTH__FED_FDA_CAERS`
- `HEALTH__FED_FDA_DRUG_ENFORCEMENT`
- `HEALTH__FED_FDA_DRUG_MASTER_FILES`
- `HEALTH__FED_FDA_ESTABLISHMENT_REG`
- `HEALTH__FED_FDA_GUDID__STAGING`
- `HEALTH__FED_FDA_PURPLE_BOOK`
- `HEALTH__FED_HRSA_UDS_HEALTH_CENTER_INFO`
- `HEALTH__FED_HRSA_UDS_TABLE3A_PATIENTS`
- `HEALTH__FED_VA_ALLCAUSE_MORTALITY`
- `HEALTH__FED_VA_SUICIDE_APPENDIX`
- `HEALTH__FED_VA_SUICIDE_NATIONAL`
- `HEALTH__INTL_HEALTHCANADA_DPD_DRUG`
- `HISTORY__FED_DOCSOUTH`
- `HOUSING__FED_CFPB_HMDA_DC_ONLY`
- `HOUSING__FED_FHFA_NMDB`
- `HOUSING__FED_FHFA_SUSPENDED_COUNTERPARTY`
- `IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS`
- `IMMIGRATION__FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT`
- `IMMIGRATION__FED_EPA_SDWA_SDWA_SERVICE_AREAS`
- `IMMIGRATION__FED_ICE_STATISTICS`
- `INVESTIGATIONS__XC_WAYBACK_REPLAY_DOJ_LISTING`
- `JUSTICE__FED_COURTLISTENER_DISCLOSURE_AGREEMENTS`
- `JUSTICE__FED_COURTLISTENER_DISCLOSURE_NON_INVESTMENT_INCOME`
- `JUSTICE__FED_COURTLISTENER_DISCLOSURE_POSITIONS`
- `JUSTICE__FED_COURTLISTENER_ORIGINATING_COURT_INFO`
- `JUSTICE__FED_FHFA_SUSPENDED_COUNTERPARTIES`
- `JUSTICE__INTL_OPENSANCTIONS`
- `JUSTICE__XC_UK_SANCTIONS_LIST`
- `LEAD_QUEUE`
- `POLITICS__BILL_COSPONSORS`
- `POLITICS__CA_LOBBY_AMENDMENTS`
- `POLITICS__CA_LOBBY_CHG_LOG`
- `POLITICS__CA_LOBBY_COVER`
- `POLITICS__CA_LOBBY_COVER2`
- `POLITICS__CA_LOBBY_EMP_LOBBYIST`
- `POLITICS__CA_LOBBY_FIRM_LOBBYIST`
- `POLITICS__FED_CONGRESS_LEGISLATORS`
- `POLITICS__FED_DOJ_EPSTEIN_LIBRARY`
- `POLITICS__FED_GOVINFO_BILLSTATUS`
- `POLITICS__IRS527_EAIN`
- `POLITICS__MEMBER_MONEY_RAISED`
- `POLITICS__TX_LOBBY_DOCKETS`
- `POLITICS__VOTEVIEW_ROLLCALLS`
- `REFERENCE__CENSUS_CB_ZCTA`
- `REFERENCE__FED_ITIS_COMMENTS`
- `REFERENCE__FED_ITIS_EXPERTS`
- `REFERENCE__FED_ITIS_GEOGRAPHIC_DIV`
- `REFERENCE__FED_ITIS_LONGNAMES`
- `REFERENCE__FED_ITIS_OTHER_SOURCES`
- `REFERENCE__FED_ITIS_PUBLICATIONS`
- `REFERENCE__FED_ITIS_STRIPPEDAUTHOR`
- `REFERENCE__FED_ITIS_TAXON_AUTHORS_LKP`
- `REFERENCE__FED_ITIS_TAXON_UNIT_TYPES`
- `REFERENCE__INTL_EUROSTAT`
- `REFERENCE__XC_CROSSREF_FUNDER_REGISTRY`
- `SCIENCE__FED_NSF_AWARDS`
- `SCIENCE__INTL_EMBL_ENSEMBL`
- `SPENDING_BUDGET__SBA_LOANS_BY_STATE_PROGRAM_AGG`
- `TRANSPORT__FED_FAA_ADIP_PRIVATE_AIRPORTS`
- `TRANSPORT__FED_NTSB_AVIATION_INJURY`

**under 100 rows** — 31

- `CORPORATE_REGISTRY__INTL_ES_BORME`
- `ECONOMICS__INTL_FAO_FAOSTAT`
- `ENERGY__FED_EIA861_DELIVERY_COMPANIES`
- `ENERGY__FED_EIA861_MERGERS`
- `ENVIRONMENT__INTL_GEM_HAZARD`
- `FINANCE__FED_NCUA_CHARTER_MERGER_EVENTS`
- `GOVERNMENT_RECORDS__FED_USASPENDING_TAS_FILTER_TREE`
- `HISTORY__FED_DENSHO_DDR`
- `HOUSING__FED_HUD_DATA`
- `IMMIGRATION__FED_CBP_ENCOUNTERS`
- `IMMIGRATION__FED_DHS_YEARBOOK`
- `JUDICIARY__FED_OYEZ`
- `JUSTICE__FED_BOP_STATISTICS`
- `JUSTICE__FED_COURTLISTENER_COURT_APPEALS_TO`
- `JUSTICE__FED_COURTLISTENER_RACE_CODES`
- `JUSTICE__FED_DOJ_FCA_SETTLEMENTS`
- `JUSTICE__INTL_AUSTLII`
- `JUSTICE__INTL_EURLEX_CELLAR`
- `JUSTICE__INTL_EU_SOCTA_EUROPOL`
- `OPEN_DATA__INTL_GE_DATAGOV`
- `OPEN_DATA__INTL_GH_DATAGOVGH`
- `POLITICS__FJC_SCOTUS_CROSSWALK`
- `POLITICS__SCOTUS_JUSTICE`
- `REFERENCE__CENSUS_CB_STATE`
- `REFERENCE__FED_ITIS_KINGDOMS`
- `REFERENCE__INTL_EG_CAPMAS`
- `REF__DIM_STATE`
- `SCIENCE__FED_NASA_OPEN_DATA`
- `SCIENCE__XC_OWID_AI_INCIDENTS_ANNUAL`
- `TRANSPORT__FED_DOT_BTS`
- `TRANSPORT__FED_FRA_SAFETY`

**catalog or lookup** — 26

- `DIM_DATE`
- `ECONOMICS__FED_SEC_EDGAR_COMPANY_TICKERS`
- `EDUCATION__FED_ED_NCES_CIP_CODES`
- `EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_ID_MAPPING`
- `EDUCATION__FED_GOOGLE_POLADS_CREATIVE_ID_MAPPING`
- `ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_POLLUTANTS`
- `ENVIRONMENT__FED_EPA_SDWA_SDWA_PN_VIOLATION_ASSOC`
- `ENVIRONMENT__FED_USGS_WBD_HUC8`
- `FINANCE__FED_FEC_CAND_CMTE_LINKAGE`
- `FINANCE__FED_OCC_NATIONAL_BANKS`
- `FINANCE__FED_OCC_THRIFTS`
- `FINANCE__FED_SEC_13F_SUBMISSIONS`
- `HEALTH__FED_CDC_DATA_PORTAL`
- `HEALTH__FED_CMS_FISCAL_INTERMEDIARY_SHARED_SYSTEM_ATTENDING_AND_RENDERING`
- `HEALTH__FED_CMS_MAIN`
- `HEALTH__FED_FDA_UNII_GSRS_SUBSTANCES`
- `HEALTH__FED_NLM_DAILYMED_SPL_SETID_MAP`
- `POLITICS__FED_SENATE_EFD_FILINGS`
- `POLITICS__MEMBER_CROSSWALK`
- `REFERENCE__FED_ITIS_NODC_IDS`
- `REFERENCE__FED_ITIS_REFERENCE_LINKS`
- `REFERENCE__FED_ITIS_TU_COMMENTS_LINKS`
- `REFERENCE__FED_ITIS_VERN_REF_LINKS`
- `REFERENCE__FED_USGS_TOPOVIEW`
- `REF__DIM_GEOGRAPHY`
- `XWALK_ZCTA_COUNTY`

**timeline count, thin or not charted** — 20

- `TIMELINE__CONSUMER_PROTECTION_INDEX`
- `TIMELINE__CONSUMER_SAFETY_INDEX`
- `TIMELINE__CRIMINAL_JUSTICE_INDEX`
- `TIMELINE__EDUCATION_INDEX`
- `TIMELINE__ENERGY_INDEX`
- `TIMELINE__FOREIGN_INFLUENCE_INDEX`
- `TIMELINE__HISTORICAL_RECORDS_INDEX`
- `TIMELINE__HISTORY_INDEX`
- `TIMELINE__INVESTIGATIONS_INDEX`
- `TIMELINE__JUDICIARY_INDEX`
- `TIMELINE__LEGAL_ENFORCEMENT_INDEX`
- `TIMELINE__MARITIME_INDEX`
- `TIMELINE__MONEY_FINANCE_INDEX`
- `TIMELINE__OPEN_DATA_INDEX`
- `TIMELINE__PROCUREMENT_INDEX`
- `TIMELINE__REFERENCE_INDEX`
- `TIMELINE__REGULATORY_INDEX`
- `TIMELINE__REVIEW_INDEX`
- `TIMELINE__SCIENCE_INDEX`
- `TIMELINE__SCIENCE_RESEARCH_INDEX`

**duplicate of a sibling** — 18

- `ECONOMICS__FED_US_SEC_EDGAR`
- `ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES`
- `ENVIRONMENT__FED_EPA_RCRA_RCRA_ENFORCEMENTS`
- `ENVIRONMENT__FED_EPA_RCRA_RCRA_EVALUATIONS`
- `ENVIRONMENT__FED_EPA_RCRA_RCRA_FACILITIES`
- `ENVIRONMENT__FED_EPA_RCRA_RCRA_VIOLATIONS`
- `ENVIRONMENT__FED_EPA_RCRA_RCRA_VIOSNC_HISTORY`
- `ENVIRONMENT__FED_USCG_NRC_INCIDENT_REPORTS`
- `FINANCE__FED_FEC_BULK_COMMITTEES`
- `HEALTH__FED_CMS_HOSPITAL_GENERAL`
- `HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVI`
- `HEALTH__FED_CMS_MEDICARE_PROVIDER`
- `HEALTH__FED_CMS_OPEN_PAYMENTS_2022`
- `HEALTH__FED_CMS_OPEN_PAYMENTS_2023`
- `IMMIGRATION__FED_EOIR_CASE_DATA`
- `INVESTIGATIONS__XC_WAYBACK_REPLAY_DOJ_DEEP_PAGES`
- `POLITICS__XC_JCS_COA`
- `POLITICS__XC_JCS_SCOTUS`

**sample, shape only** — 16

- `CORPORATE_REGISTRY__FED_IRS_EO_BMF`
- `ECONOMICS__FED_GRANTS_GOV`
- `ECONOMICS__FED_IRS_990`
- `ECONOMICS__FED_IRS_SOI_CHARITIES`
- `ECONOMICS__FED_US_USASPENDING_API`
- `ENVIRONMENT__FED_EPA_ENVIROFACTS`
- `FINANCE__FED_FDIC_BANK_DATA`
- `GOVERNMENT_RECORDS__FED_NARA_AAD`
- `HOUSING__FED_CFPB_HMDA`
- `HOUSING__FED_CFPB_HMDA_LAR`
- `OPEN_DATA__INTL_ES_DATOSGOB`
- `POLITICS__FED_FEC_API`
- `PROCUREMENT__FED_USASPENDING_BULK`
- `PROCUREMENT__FED_USASPENDING_SUBAWARDS`
- `REFERENCE__FED_DHS_HIFLD`
- `SCIENCE_RESEARCH__XC_OSF_REGISTRATIONS`

**backup copy** — 11

- `CIVIL_RIGHTS__FED_NARA_WRA_AAD`
- `ECONOMICS__FED_FINCEN_BOI`
- `ECONOMICS__INTL_GFI_TRADE`
- `EDUCATION__FED_ED_EDFACTS`
- `FINANCE__FED_FARA`
- `HEALTH__FED_CMS_HPT_MRF`
- `HISTORY__FED_DAVID_RUMSEY`
- `JUSTICE__FED_USCOURTS_STATS`
- `OPEN_DATA__INTL_BR_DADOS_GOV`
- `PROCUREMENT__INTL_ADB_DATA`
- `TRANSPORT__FED_FAA_DATA_PORTAL`

**prior snapshot** — 11

- `FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES__PREV_20260906`
- `FINANCE__FED_FEC_INDIV_CONTRIBUTIONS__PREV_20260906`
- `HEALTH__FED_CMS_HCRIS__PREV_20260906`
- `HEALTH__FED_HRSA_SHORTAGE_AREAS__PREV_20260907`
- `POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP__PREV_20260906`
- `POLITICS__FED_GOVINFO_BILLSTATUS__PREV_20260907`
- `SCIENCE__INTL_EMBL_ENSEMBL__PREV_20260907`
- `TIMELINE__FINANCE_INDEX__PREV_20260906`
- `TIMELINE__FINANCE_INDEX__PREV_20260906_221619`
- `TIMELINE__HEALTH_INDEX__PREV_20260906`
- `TIMELINE__POLITICS_INDEX__PREV_20260906`


---

---

# Part 8 — Visualization technique catalog

41 chart and technique ideas, each tied to a specific verified table —
not a chart-type list, a "here's the exact substrate" list. From
`reports/viz_ideas_inventory.md`, started 2026-08-22.

*What CAN be visualized from data that is verified clean and usable — running list,
compiled in batches. Started 2026-08-22 (viz sprint session). Each idea names its
exact data substrate and its trust level so a design template can be built against
it without re-verifying. "BUILT" = a working prototype page already exists from the
2026-08-22 sprint.*

**Trust legend:**
- ✅ CLEAN — table/columns verified this month (live queries or the Laboratory map's refute pass)
- ⚠️ CAVEAT — usable, but with a named limit that must appear on the visual
- 🚫 excluded entirely: contract trends (truncated sample), FAERS (column-shift), MSHA deaths,
  EPA penalty dollars (phantom-fines stamping), SEC 13F dollars (scale split), NHTSA (dup risk),
  UK ownership timelines (fixed 8/22 but PSC edge dates unverified since), debarment list.

---

## Batch 1 — compiled 2026-08-22

### A. Opioid shipments (178.6M rows, dated, weighted, from→to; public window 2006–2012) ✅

1. **County dose map** — every county colored by morphine-equivalent dose per resident per year. BUILT (The Rate Map).
2. **Distributor→pharmacy flow arcs** — ZIP-to-ZIP shipment routes over time. BUILT (Pill Rivers).
3. **The firehose finder** — rank pharmacies by dose received vs. their county's population; a scatter of "pharmacy size vs. town size" where the outliers ARE the story (the famous 9M-pill town in WV is findable this way).
4. **Distributor market share river** — stacked share of national dose by distributor company per quarter; shows consolidation and who owned the peak years.
5. **Drug mix shift** — oxycodone vs hydrocodone vs the rest, share per year per state; small-multiple states, spotting states whose mix flips.
6. **The one-pharmacy spectrogram** — pick any pharmacy: drugs down the side, 84 months across, cell = dose. The Laboratory's own "music" technique; substrate confirmed.
7. **Percolation dial** — drop weak shipment routes one threshold at a time and watch the national network shatter into regional islands; the snap threshold is the finding.
8. **Network centrality leaderboard** — which distributors bridge the most pharmacy communities (betweenness on the real shipment graph).

### B. Immigration detention stints (2.57M, real book-in/book-out timestamps) ✅

9. **Survival curves** — % still detained at day 7/30/90/180/365, by year booked in. BUILT (The Waiting Room).
10. **Country → state → outcome Sankey** — where people are from, who held them, how it ended. BUILT (Detention Rivers).
11. **Facility league table with funnel plot** — median stay per facility plotted against facility volume, with uncertainty bands so tiny facilities can't top the chart on noise. Uses the same stint table's facility field.
12. **Bond ladder** — distribution of bond amounts set vs posted; where the "can't afford $5,000" wall sits. Bond columns are typed numbers on the same table (fill rate unverified — check first).
13. **The revolving door** — people with multiple stints (person-hash repeats): gap between release and re-booking as a histogram.

### C. Mortgage applications, 2007–2017 (19.1M rows, race/income/outcome on one row) ✅

14. **Denial gap dot plot** — denial rate by race across income bands. BUILT (The Denial Gap).
15. **Redline echo map** — tract-level denial rate for Black applicants vs the 1930s redlining grades (the redlining polygon mart holds only a 1,155-row sample ⚠️ — works as a city case study, not national).
16. **The gap by lender** — respondent-level: which lenders show the widest same-income racial gap; funnel-plot guard for small lenders.
17. **Denial reason fingerprints** — reason mix by race per state; "collateral" vs "credit history" split reads very differently.
18. **Crash timeline** — application volume + denial rate through 2007–2012, national; the mortgage market's heartbeat through the crash.

### D. Bank branches (76k branches, deposits, coordinates; latest survey) ✅

19. **Deposit glow / density / desert map** — three views. BUILT (Bank Deserts).
20. **Branch catchment population** — assign every census tract to its nearest branch; rank catchments by people-per-branch (Voronoi stats without drawing a polygon). Tract centroids + populations verified.
21. **Bank exit timeline** — the survey is annual back years; branches that vanish year-over-year, mapped as departures per county per year (⚠️ verify all survey years are loaded before designing around it).
22. **HQ vault effect** — deposits booked to headquarters vs street branches; a log-scale strip plot that makes the accounting artifact itself the story.

### E. Corporate ownership, global LEI registry (484k dated edges, typed dates since 8/22) ✅

23. **Ownership switch-on/off clock + growing web**. BUILT (The Ownership Clock).
24. **Chain-length census** — how deep do ownership chains go (parent-of-parent-of-parent); histogram + longest-chain gallery with names.
25. **Cross-border ownership matrix** — country-of-child × country-of-parent heatmap; the offshore corridors light up.
26. **Orphaned subsidiaries** — links that switched OFF with no replacement parent; a timeline of corporate abandonment events.

### F. Consumer complaints (17.2M, product/issue/company/state/date, all verified) ✅

27. **Complaint entropy map** — which states' complaint mix is unusual vs the national mix (the entropy technique's textbook table).
28. **Company response fingerprint** — response type mix per company for the top 100 companies; who closes with relief vs without.
29. **Issue emergence tracker** — new issue-categories appearing and exploding month over month (changepoint detection on category series).
30. **Narrative volume vs outcome** — do complaints with written narratives get different responses; two-rate comparison, no NLP needed.

### G. Warehouse-wide clocks (403 sources on one shared time axis) ✅

31. **Heartbeat wall** — every source's monthly pulse. BUILT.
32. **Pulse correlation grid** — which sources beat together. BUILT (The Pulse Grid).
33. **Calendar-effect scanner** — September fiscal-year-end spikes, election-cycle money wobble, weekend gaps; the 155k-row calendar dimension joins to everything with a clock ⚠️ (calendar table verified present, join untested).
34. **Changepoint gallery** — for each source, the single month its line snapped hardest; a wall of before/after breaks (collection-artifact x-ray, honesty tool for everything else).

### H. Political money (84M itemized contributions, typed amounts + dates) ✅

35. **Money shape** — Benford digits, magnet amounts, threshold bunching, election river. BUILT (The Shape of Money).
36. **The $23 cluster hunt** — recurring-amount donor clusters (the July sweep found one generating a fifth of rows); a treemap of exact-amount "colonies."
37. **Distance-from-limit creep** — how the just-under-the-limit spike migrated as limits rose era over era; animated histogram.
38. **ZIP money vs ZIP denial** — 🅿️ PARKED: needs the mortgage table joined to contributions by geography — cross-table, design later.

### I. Health provider clouds (verified wide numeric tables) ✅

39. **Provider PCA/t-SNE atlas** — 1.3M providers, 49 real measures each, projected to 2D; clusters = practice styles, outliers = billing anomalies. ⚠️ The identical twin table must be excluded or every point doubles.
40. **Hospital funnel plots** — 6,103 hospitals × 107 cost-report measures with volume-based uncertainty bands; the honest "worst in America" guard.
41. **Chronic-condition geography** — the provider table's ~35 condition percentages averaged by county (providers have states/ZIPs); disease-burden maps with no new data.

---

## Parked — worked through 2026-08-22 (this session)

- **UNPARKED: Politics money ↔ votes.** Measured live: 1,530 of 12,794 members carry
  campaign-finance ids — and that matches the SOURCE file exactly (1,530 of 12,768 upstream),
  so nothing was lost in ingest; the ids cover the modern era, which is what the donations
  table covers. End-to-end chain verified: member → committee linkage → 16,451,066 individual
  contributions ($2.14B) reachable. Buildable today; caveat "modern members only" on the visual.
- **UNPARKED: Opioid flows ↔ overdose deaths.** NCHS county drug-poisoning mortality
  (1999–2015, 53,387 rows, 3,141 counties) ingested to landing 2026-08-22 and verified against
  source count. Joins to the county spine by FIPS; joins to opioid shipments by county name
  (same path the Rate Map uses). Caveat: death rate is a BANDED estimate ("12.1–14 per 100k"),
  not an exact count.
- **MEASURED, decision pending: EPA facility ↔ corporate parent bridge.** Fill rate is 1.4% —
  73,948 of 5,300,149 facilities carry a matched corporate id (22,736 distinct companies;
  10,297 with ultimate parent; 8,442 with SEC id; avg match confidence 0.96, zero review flags).
  The map's "fuses the whole 5.3M-facility island" claim is oversold ~70×. Whether a 74k-facility
  bridge justifies the $10–15 spine rebuild is Chris's call.
- Anything on federal contract TRENDS (🚫 truncated sample until re-pull — off-limits list).

---

*Batch 2 candidates (not yet compiled): environment/EPA facility families, water-system
violations spans (14.4M, survival), storm events, workplace injuries with hours-worked
denominators, ER injury narratives (text), court case durations, maritime AIS point cloud,
FracFocus chemicals, GLEIF×SEC overlap. Say "next batch" to continue.*


---

---

# Part 9 — The news corroboration framework

A different kind of check than Part 5's five. Instead of asking "is
this candidate real," this asks "does the warehouse already know things
the news already proved." Three grades, run against 24 real stories.

Chris's ask, verbatim: "I want you to do a full 'mapping' of real world things that have come to light and whether or not my data would corroborate or 'discover' the same thing. Obviously only things we reasonably believe I already have data for. Go looking"

All queries through the Python door, LIBRARY_RAW.LANDING, run 2026-09-05. Scripts and raw output in the session scratchpad (inv.py, cov.py, probes.py, probes2.py, probes3.py).

## Three grades
| grade | question | proves |
|---|---|---|
| Echo | story says X, table shows X | the file landed and did not rot |
| Retrace | start from the story's first clue, joins reach the end | the joins work |
| Stumble | one dumb query over the whole table, story pops in the top 20 | the warehouse can find |

## The scorecard — 24 stories
| # | story | source | table | years held | grade | result | verdict |
|---|---|---|---|---|---|---|---|
| 1 | WaPo 2019, 76B opioid pills 2006–12, Kermit WV | DEA ARCOS | FED_DEA_ARCOS_FULL | 2006–2014 | Stumble | top 8 WV pharmacies by oxy+hydro pills: Strosnider Kermit 13.2M, Family Discount Mt Gay 12.8M, CVS Huntington 10.7M, CVS Parkersburg 10.3M, Hurley Williamson 8.9M, Tug Valley 8.8M. Four of WaPo's named independents in the top 6 | **HIT** |
| 2 | Reveal 2018 "Kept Out" redlining | HMDA | FED_CFPB_HMDA_HISTORIC | 2015–2017 | Echo | morning: all 19.1M rows "Loan originated", zero denials, MISS. Reloaded same day from the all-records files, 44,992,667 rows, 8 action codes. Philadelphia 2015–16 conventional purchase, owner-occupied: Black applicants denied 27.2%, white 8.1%, raw ratio 3.34. Reveal's adjusted figure was 2.7x. Worst raw ratios: Baton Rouge 3.68, Memphis 3.59, St. Louis 3.56 | **HIT after reload** |
| 3 | 2024 ActBlue/WinRed smurfing | FEC | FED_FEC_INDIV_CONTRIBUTIONS | thru 2026 | Stumble | 1,103 name+state donors with 2,000+ gifts in 2023–24 (708 by name+zip9, which splits people). Top: Makowski MI 48,130 gifts, $99k, ~$2 each | **HIT** |
| 4 | Waco patent-court surge 2020–22 | FJC IDB | FED_FJC_IDB_CIVIL | 1988–2025 | Stumble | by FILEDATE year, district 42 (WDTX per FJC codebook) share of NOS 830: 2019 not top 3, 2020 22.4% #1, 2021 25.2% #1, 2022 23.6% #1, 2023 17.6% #2 after the July 2022 random-assignment order. TAPEYEAR lags a year, do not use it | **HIT** |
| 5 | Global Witness 2018, toddler company owners | UK PSC | UK_COMPANIES_HOUSE_PSC | current | Stumble | 5,053 individual PSCs born 2020+, 24 born before 1900, 17 over 155 | **HIT** |
| 6 | NEJM 2016, 1% of doctors = 32% of paid claims | NPDB | FED_HRSA_NPDB | 1990–2026 | Retrace | 165,248 paid practitioners; top 1% hold 13.3% of dollars, 3.4% of claims; repeaters hold 52.8% of claims | **PARTIAL** — denominator differs, NEJM counted all physicians |
| 7 | Flint lead 2015–16 | SDWA LCR | FED_EPA_SDWA_SDWA_LCR_SAMPLES | 1992–2025 | Echo | PWSID MI0002310 = "FLINT, CITY OF" confirmed. PB90 mg/L by SDWIS period: Jul–Dec 2014 .006, Jan–Jun 2015 .011, Jan–Jun 2016 **.020**, Jul–Dec 2016 .012. Press reported 11 and 20 ppb for the 2015 halves; SDWIS labels the 20 one period later. Action level .015 | **HIT** |
| 8 | Jackson MS lead 2016 | SDWA LCR | same | same | Echo | PWSID MS0250008 = "CITY OF JACKSON" confirmed. Period ending 12/31/2015 **.0286**, 2016 .016, then under .015 | **HIT** |
| 9 | Upper Big Branch 2010, 515 violations in 2009 | MSHA | FED_MSHA_VIOLATIONS | 2000–2025 | Echo + Stumble | echo: 506 violations 2009, 198 S&S, 920 in 2010. Stumble: rank 10 of 192 WV underground coal mines in 2009 | **HIT echo, MISS stumble** |
| 10 | Wells Fargo fake accounts Sep 2016 | CFPB complaints | FED_CFPB_COMPLAINTS | 2011–2026 | Echo | monthly WF complaints ~770 Jan–Aug, **1,592 Sep**, 1,383 Oct | **HIT** |
| 11 | Amazon warehouse injury rate ~2x industry | OSHA ITA 300A | FED_OSHA_ITA_300A_SUMMARY_2024 | 2024 | Stumble | NAICS 4931: Amazon TRIR 6.21 across 458 sites vs 3.51 for 9,405 others | **HIT** |
| 12 | Norfolk Southern after East Palestine | FRA | FED_FRA_EQUIPMENT_ACCIDENTS | 1975–2026 | Retrace | NS 2023: 435 accidents (452 in 2022), 9 hazmat-release cars, the 2018–24 high for hazmat only; UP 776, BNSF 492 | **WEAK** — needs per-mile rate |
| 13 | Life Care Center Kirkland, COVID 2020 | CMS nursing deficiencies | FED_CMS_NURSING_HOME_DEFICIENCIES | 2023–2026 for this CCN | Echo | rows 2023 onward only; 2020 survey absent | **MISS — vintage** |
| 14 | Charles Lieber, undisclosed China ties | NIH RePORTER | FED_NIH_REPORTER | 2000–2026 | Echo | PI_NAMES = "CHARLES LIEBER" confirmed, Harvard. FY2000–2019 $11.4M; FY2017–18 $1.4–1.6M/yr; three small rows FY2024–26 ($36–42k) | **HIT** |
| 15 | Ozempic suicidal-ideation reports 2023 | FAERS | FED_FDA_FAERS_* | 2004q1–**2014q2** | Echo | table ends 2014; semaglutide approved 2017 | **MISS — vintage** |
| 16 | 2025 ICE detention surge | ICE stints | FED_ICE_DETENTION_STINTS | 2004–2026 | Stumble | book-ins/month: 45k Dec 2024 → 104k Jun 2025 → 128k Dec 2025. Release reason "death" codeable only from 2022: 9 (2024) → 15 (2025) | **HIT** |
| 17 | ProPublica 2021, Kabbage fake NJ farms | SBA PPP | FED_SBA_PPP | 150K+ loans only (968,524 rows matches the public 150k+ file) | Stumble | fake farms were ~$20k loans; not in this slice. Address stacking works: 40 loans at one Peoria address | **MISS — slice** |
| 18 | 2024 political ad spend | Google polads | FED_GOOGLE_POLADS_ADVERTISER_WEEKLY_SPEND | 2018–2026 | Echo | Harris Victory Fund $67.0M, FF PAC $61.7M, Harris for President $53.6M, Trump 2024 $32.3M | **HIT** |
| 19 | Unusual Whales, most active House traders 2021 | House PTR index | FED_HOUSE_FD_PTR_INDEX | 2008–2026 | Stumble | PTR filings 2021–22: Lowenthal 140, DelBene 36, Blumenauer 34, Green 32, Schrader 28, Rogers 26, Gottheimer 26, Hern 25, Khanna 24, McCaul 24 | **HIT** — counts filings, not trades |
| 20 | WaPo Feb 2022, Tesla phantom braking | NHTSA complaints | FED_NHTSA_COMPLAINTS | thru 2026, headerless | Stumble | all Tesla brake+FCW complaints per month: 42 Sep 21, 83 Oct, 160 Nov, 189 Dec, 342 Jan 22, 884 Feb. Broader filter than WaPo's 107 phantom-braking reads; shape matches, magnitude does not. Feb spike is partly after NHTSA opened its probe | **HIT — shape** |
| 21 | ProPublica 2023, Thomas and Harlan Crow | CourtListener disclosures | FED_COURTLISTENER_DISCLOSURE_GIFTS | — | Echo | one Crow gift on file: Douglass bust $6,484. 2,025 gifts across 1,432 disclosures, SOURCE is OCR text with 58 nulls, and there is no people table to tie a disclosure to Thomas | **MISS — bridge** |
| 22 | Debarred firms still paid | SAM × USAspending | FULL_R2 tables | 2011–2026 | Retrace | 22 vendors, 99 actions, $1.86M (report 2026-09-04). Caveat carried: UEI did not exist before April 2022, the 2011–15 matches ride a backfilled DUNS→UEI map | **HIT** |
| 23 | Dollars for Docs | Open Payments × Part D | 2024 both | 2024 | Retrace | paid $10k+ prescribers write 1.6x–7x costlier scripts (report 2026-09-04) | **HIT** |
| 24 | June 2026 DOJ fraud takedown | NPPES × Part D | 2024 | Retrace | 4 of 5 named prescribers at 91st–99.4th pct before charges; Aquino tops out at the 86th (report 2026-09-05, which overstated this as 5 of 5) | **HIT** |

Tally after the HMDA reload: 17 hits, 1 partial, 1 weak, 5 misses. Four misses are a vintage, a load slice, or a missing bridge table. The fifth, MSHA stumble, was my query, not the data.

## What each miss means, plainly
- **HMDA (2)**: was originations only because the 2026-08-05 loader chose the first-lien-owner-occupied file family, a scope call. Fixed 2026-09-05: `scripts/hmda_historic_lar_load.py --family all --run`, 3.4 GB downloaded, 45.0M rows swapped in, registry and quality gate updated. The registry MERGE had a latent SQL bug (adjacent string literals), fixed with `||`.
- **FAERS (15)**: 42 quarters, stops 2014q2. Any drug approved after 2014 has no adverse-event trail here.
- **Nursing home deficiencies (13)**: CMS publishes a rolling ~3-year window; 2020 is gone from the public file. Not a load bug.
- **PPP (17)**: only the 150K+ file landed. Small-loan fraud, which is most PPP fraud, is out of reach.
- **MSHA stumble (9)**: raw violation count ranks UBB 10th. The story was withdrawal orders and S&S density. Right table, wrong dumb query.
- **Thomas gifts (21)**: the gifts table has no path to a judge's name. Needs the CourtListener people table, not landed.

## Skeptic pass, same day
Fourteen disagreements. Fixed in the table above: takedown was 4 of 5 not 5 of 5; FEC donor count was name+zip9 pairs; Lieber sum was $11.4M not $13M; FJC needed FILEDATE not TAPEYEAR and the peak is 2020–22; Thomas downgraded to miss; SAM caveat restored; three top-N lists were non-contiguous; PWSIDs now name-checked. Not fixed: no negative controls were run, every grade is one query. Skeptic's suspicion that SDWIS sample periods sit a step late is left open; SDWIS start and end dates are what the table says.

## Mart rebuild, same day, after the skeptic caught it stale
The landing swap does not touch the dbt mart. LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_HISTORIC still held 19,136,434 rows until `dbt run -s +housing__fed_cfpb_hmda_historic+` on 2026-09-05. Now 44,992,667 rows, 8 action codes, 6,967,834 denials; TIMELINE view and timeline__housing_index rebuilt with it. Tests: not_null and unique on lar_record_id pass at both staging and mart, the staging unique took 6m59s over 45M rows. Log: library-onboarding/ripple_dbt/logs/hmda_historic_rebuild_2026-09-05.log. Registry and gate receipt: scripts/hmda_historic_scratch/register_rerun_2026-09-05.log.
Skeptic's second pass, applied: loader now refuses --family all without denials and asks before a first-lien swap; download.sh all-records loop is live behind FAMILY=all; warehouse_topo_map report corrected; per-year null check run, all three years evenly populated. "Reproduces Reveal" is retired: the raw rate ratio is 3.4x, the raw odds ratio 4.35, Reveal's regression-adjusted odds ratio 2.7 on 2012–2016. Same direction, different statistic.

## Mart rebuilt, same day
dbt run on +housing__fed_cfpb_hmda_historic+ after `greenlight rebuild`: staging view, HOUSING mart (3m43s), TIMELINE view, timeline index, timeline warehouse, 5 of 5 succeeded. dbt test 4 of 4 passed in 7m11s, including the unique test on lar_record_id over 45M rows. Warehouse count on LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_HISTORIC: 44,992,667 rows, 6,967,834 denials. Log: library-onboarding/ripple_dbt/logs/hmda_historic_rebuild_2026-09-05.log. Registry and gate receipt: scripts/hmda_historic_scratch/register_rerun_2026-09-05.log.

## Broken-load traps found on the way
- FED_EOIR_CASE_DATA: 12.6M rows, one column, tab-separated text. Unparsed.
- FED_NHTSA_COMPLAINTS: headerless C1..C54. Usable: C3 mfr, C4 make, C5 model, C6 model year, C8 date YYYYMMDD, C12 component. 110k rows with blank date.
- FED_MSHA_VIOLATIONS: every value carries literal double quotes. Filter with '"46%'.
- FED_HRSA_NPDB: PAYMENT is a string with a leading $.
- FED_DEA_ARCOS_FULL: TRANSACTION_DATE is MMDDYYYY text; two rows hold floats.

## Cost
HMDA reload: 3 downloads totalling 3.4 GB, ~45M rows through write_pandas on X-Small. Last load of the 19M-row slice priced at ~$0.80 across 125 statements; this one is 2.4x the rows, so ~$2, exact figure in the query log tomorrow.

Roughly 60 queries. Largest scanned ARCOS 178M rows (year distribution, top WV pharmacies) and FEC 84M rows (smurf group-by). No prior run of this pattern in the query log to price against.


---

---

# Part 10 — The full trap log

Every dated trap, verbatim, from `.claude/traps.md`. Part 3's per-schema
"Trap warning" lines are a thin sample of this. This is the whole thing —
column-level, dated, one line each, the actual burn history of this
warehouse. Check here before trusting any column named anywhere above.

2026-08-30 — the scripts door logs in as ACCOUNTADMIN; a wrong command has no safety net.
2026-08-30 — the warehouse query log stores SQL text, not shell commands; price by table/statement pattern, not by script name. 500 rows = the cap, not a count.
2026-08-31 — zip loads keep only the LARGEST member per zip (08_bulk_ingest.sql:179); a count that's a multiple of the publisher's split size is the smell, but partial last chunks make totals non-round. 18 zip specs ride this path.
2026-08-31 — landing table name = UPPER(SOURCE_ID) is broken warehouse-wide; name-only registry↔landing joins fabricate hundreds of false orphans both ways.
2026-08-31 — SOURCE_REGISTRY.INCLUDE is a 'Y'/'N' STRING; Python truthiness counts 'N' as true.
2026-08-31 — LEIE UPIN column holds empty strings, not NULLs; count() without nullif(trim()) overcounts 14x.
2026-08-31 — checkpoint-sum = landing-count proves nothing about never-attempted files: both sides are zero. 13F missed 7 of 53 zips while summing exactly.
2026-08-31 — FDA_DT is the receipt date; it smears quarter-file boundaries. Reconcile FAERS by run id, never by event-date histogram.
2026-08-31 — the name-matcher's first-12-chars rule passes UNIVERSITY OF MICHIGAN = UNIVERSITY OF MISSOURI; ~12% false-positive on generic org names.
2026-08-31 — dbt test warn ≠ small: this run's 246 warns hide 99.4M failing rows.
2026-08-31 — Part D prescriber-drug has NO year column; one load run = one data year (DY22), not a series.
2026-08-31 — some loaders write audit columns UNPREFIXED (LEIE: INGESTED_AT not _INGESTED_AT); check before referencing.
2026-08-31 — USAspending landing tables carry case-sensitive lowercase and digit-leading column names; unquoted SQL resolves uppercase and misses.
2026-08-31 — the timeline rollup tables freeze the planned/actual tag at build time; it ages past current_date. Guard green also ≠ TIMELINE schema clean — nothing walks warehouse→registry.
2026-08-31 — identical row counts ≠ identical tables: hash before dropping, always. But raw HASH_AGG lies the other way too: the 8 ICIJ "different vintage" copies were the SAME snapshot with different blank spellings ('', NULL, 'NA', 'None', 'N/A', 'n/a') — blank-normalize before hashing or every loader pair "differs". Verdict: reports/row1/icij_vintage_verdict_2026-08-31.md.
2026-08-30 — portal_recon/ looks dead by import scan; connect/keys.py sys.path-imports its tagger by bare file name. Grep file names before retiring a folder.
2026-08-30 — "1,121" is the hard-ID edge count in lab_map facts, NOT the test count. The two got copy-crossed once already.
2026-08-30 — typing-layer tests query live marts but carried no snowflake marker until today; unmarked tests can burn credits from a plain pytest run.
- 2026-08-31 — CONNECT_WATERMARK content-key survives things it shouldn't: a table can be pinned "current" while SPINE_KEYSET_LIVE holds zero rows for it. connect-one then silently no-ops. Check keyset count, never the watermark, to know if a table is wired.
- 2026-08-31 — KEY_TYPE columns were CTAS-inferred VARCHAR(12)/(8); any key name over the width crashes MERGEs mid-run, leaving keyset-without-index half-states. All widened to 32; regression test in tests/test_keys_normalize.py.
- 2026-08-31 — reslice_discover's pair query has no size cap: a non-spec table with millions of keys blows Snowflake's 128MB LOB limit and kills the whole run BEFORE config pinning, so the next run redoes everything. FED_USASPENDING_CONTRACTS was the trigger; its graph keys are removed, the class remains.
- 2026-08-31 — registry SOURCE_ID is mixed-case and the index's SOURCE_TABLE is upper: name joins silently drop every lowercase registry row. Map via SOURCE_FRESHNESS.LANDING_FQN first, case-blind name second.
2026-09-01 — "never landed" by registry-vs-watermark SOURCE_ID join lied twice (FEC contributions, OpenSanctions): registry doubles and missing watermark credit both fake absence. LIKE-search LANDING table names before queuing any load.
2026-09-01 — the watermark lies BOTH ways: fed_cms_tic_mrf and fed_cms_hpt_enforcement have watermark rows and zero landed data. Watermark membership proves nothing in either direction.
2026-09-01 — FED_FEC_COMMITTEE_TO_COMMITTEE is 93% 15J earmark memos with MEMO_CD='X'; summing with itcont double-counts the same dollar under different CMTE_ID and SUB_ID. Filter MEMO_CD <> 'X' first.
2026-09-01 — FED_FCC_LICENSING.EIN is 100% empty string, 1.69M rows; detect_key fires on names. Count distinct before calling any column a key.
2026-09-01 — count parity is not coverage when the source prunes: GLEIF drops ended relationships, so a BIGGER new vintage still lost July's dead links. Rescued to RAW.RETIRED.INTL_GLEIF_RR_VINTAGE_20260731.
2026-09-01 — FED_USASPENDING_CONTRACTS_FULL is exactly 20,000,000 rows — a cap, superseded by _R2 (93M, wired); ASSISTANCE_FULL 19.9M unverified either way.
2026-09-01 — FED_HOUSE_DISBURSEMENTS ships SUBTOTAL ROWS INLINE: 371K rows (7.6%) with DESCRIPTION LIKE '%TOTALS%' hold $48.4B of the $64.5B naive sum. Filter them out or every dollar total is ~4x reality; detail-only ≈ $1.5B/yr matches the House appropriation.
2026-09-01 — FED_HOUSE_FD_PTR_INDEX.DOCID is NOT unique: the Clerk re-lists amendments in every year's zip (41,883 rows, 41,860 distinct). NO natural key exists: DOCID+INDEX_YEAR also fans out (18 exact-dupe row groups); dedup on hash(*). Only DOCID 9110829 legitimately spans years.
2026-09-01 — FED_FEC_COMMITTEES repeats 16,943 ids across cycles with NO cycle column; a raw name join inflates itoth money 2.14x. Join FINANCE__FED_FEC_COMMITTEES_DIM instead; 14.1% of real money rows (270,519) carry IS_AMBIGUOUS=true — that id's type/party/name conflicts across cycles, filter or caveat before any spend-by-attribute chart. (First shipped version flagged only cm rows, 0.07% — wrap skeptic caught it, fixed same day.)
2026-09-01 — FINANCE__FED_FEC_COMMITTEES_DIM.CYCLE is null on 55% of rows (the cm_multicycle fills); filtering or faceting on CYCLE silently drops the majority of the dimension.
2026-09-01 — FED_HOUSE_DISBURSEMENTS.AMOUNT is TEXT and 6 rows hold column-shifted junk from embedded commas; bare sum() throws — always try_to_number. SOD_QUARTER has 42 spellings in 6 styles; parse with care.

## Registry domain column mislabels tables (found 2026-09-01, via the Things tab)
- What was checked: HANDBOOK_CONTEXT dom, fed by the marts registry domain column.
- The hit: 12 tables carry domain "immigration" that are not immigration — CMS Medicare FFS enrollment, CMS Hospice Enrollments, EPA SDWA service areas among them.
- What it means: never group or filter by the registry domain column without eyeballing; the label lies on at least 12 rows. Fix belongs in the marts registry, not downstream.
2026-09-02 — PORTAL_ landing tables never exceed 10,000 rows; 169 of 1,563 sit at exactly 10,000, the scraper's page cap. Those 169 are samples, not datasets; any count or sum on them is a floor.
2026-09-02 — _INGESTED_AT reads year ~56,660,000 on at least 7 tables (EPA CAMPD, GUDID x2, GLEIF REPEX, FMCSA census, SAM entity, USCG vessels): loaders stamped epoch microseconds as seconds. year() on it throws; never trust _INGESTED_AT as a date without a range check.
2026-09-02 — ArcGIS PORTAL_ARC_ date columns land as epoch MILLISECONDS with a trailing '.0' (e.g. 1555977600000.0), often under names like LASTCHANGE or ST_REVIEW; a bare sum reads as trillions. Detect 13-digit values, divide by 1000, dateadd from 1970.
2026-09-02 — FED_CMS_OPEN_PAYMENTS APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_ID is a 12-digit numeric id (100000000xxx); any 'PAYMENT' name-match that sums it reads $1.5 quadrillion. Column name says PAYMENT, content says id.
2026-09-03 — cross-table name-matching on a bare single word is 8% real (2 of 25 verified: TESLA, PACIFICORP), not an entity signal. Common surnames/first names (JOHNSON, SMITH, THOMAS...) cluster across physician/judge/legislator/lobbyist tables because thousands of unrelated people share the name — row count in the hundreds of thousands is the tell. Multi-word names cleared 92% real (11 of 12) in the same test; trust those, verify single words one by one.
2026-09-03 — the surname leak rides columns the *_LAST_NAME filter never catches: NAME_LAST, NAME_FIRST, FILER_NAML/FILER_NAMF, a bare column named LAST, RNDRNG_PRVDR_LAST_ORG_NAME (name and org mixed in one field), CASE_NAME_SHORT, PLT/DEF party fields, FAMILY_NAME. Any "who" column pull needs this list too, not just *_LAST_NAME.
2026-09-03 — generic institutional names collide exactly like surnames: ST LUKES HOSPITAL in FED_CMS_HOSPITAL_COMPARE is many unrelated hospitals (confirmed via FACILITY_ID and a separate ROR registry ID per hospital), sitting next to MEMORIAL HOSPITAL, HOLY CROSS HOSPITAL, ST JOSEPH MEDICAL CENTER, MERCY MEDICAL CENTER, COMMUNITY HOSPITAL — all unverified same-name collisions still sitting uncaveated in gen 1's DIGEST.md "same name, many tables" table.
2026-09-03 — county names leak past the " COUNTY" suffix filter through columns like CZ_NAME (NOAA), CNTY_NM2KX/CURCNTY_NM (HUD), and XC_CENSUS_CB_COUNTY's own NAME column, where the value is the bare county name ("Jackson") with no "COUNTY" suffix to catch.
2026-09-03 — a THIRD who-column noise type, biggest yet: category/classification fields (OSHA injury type, body part, job title, political party) get tagged "who" same as name columns. 54 of 169 phase-A-round-2 verify hits were this — STRAIN, ATTORNEY, PHYSICIAN, DEMOCRAT, KITCHEN all read as "cross-table entities" until checked.
2026-09-03 — a generic-sounding multi-word name is NOT automatically noise: Knights of Columbus, Rotary International, Kaiser Foundation Hospitals, American Legion Auxiliary all verified real — one chartered parent org with many local chapters/facilities. The tell: check if the source tables imply one franchising body (IRS BMF nonprofit charters) vs many independent locals (CMS hospital directory) — ST LUKES HOSPITAL and MEMORIAL HOSPITAL are the independent-locals case, still noise.
2026-09-03 — international sanctions-list first names CAN be real: HAQQANI, AKHUND, SABAWI, BARZAN, ABDALLAH, QADHAFI, KONY, SADDAM all verified as the same small set of designated individuals mirrored across UK/UN/US sanctions tables, not a common-name coincidence like SMITH. Row count in the tens plus concentration on one regime/list family is the tell; hundreds of rows spread across unrelated sanctions programs (MOHAMED, ALI, AHMED) is still noise.
2026-09-03 — "National Association" bank names are always one entity: Wells Fargo, JPMorgan Chase, U.S. Bank, PNC, TD, KeyBank, M&T, First-Citizens, BMO, Citizens Bank all verified real. One OCC national charter, branches and SBA/PPP loans reported under it — check FED_FDIC_SOD_BRANCH_DEPOSITS' RSSDID/NAMEHCR columns to confirm one charter behind any bank name that looks generic.
2026-09-03 — a hospital/care-center name is noise unless proven otherwise, even after two rounds of fixes: ST LUKES HOSPITAL, ST MARY MEDICAL CENTER, MERCY REGIONAL MEDICAL CENTER, ROLLING HILLS CARE CENTER all re-confirmed noise in round 3 — each row carries its own separate CMS Certification Number (CCN), proof of independently-run facilities, not one chain.
2026-09-03 — "X SERVICE STATION" in the EPA facility tables (FRS/RCRA) is a generic facility-type label, not one franchise: SUNOCO SERVICE STATION and SHELL SERVICE STATION both verified noise, even though gen 1's original DIGEST listed them as real cross-agency hits alongside the genuinely real SHELL OIL CO. Retroactive correction — the brand name plus "SERVICE STATION" reads like one chain but isn't.
2026-09-03 — a bare mailing address (e.g. "200 1ST ST SW") clusters across tables because it's one hospital's canonical address reused for thousands of different affiliated physicians' billing address — an address-leak, not an entity. Same failure shape as the street-name leak (avenue/street names from NYC campaign filer addresses), just at building-number granularity.
2026-09-03 — a common-surname case-name template ("SMITH V. UNITED STATES") is noise: many different unrelated litigants share the surname, confirmed across FED_COURTLISTENER_DOCKETS/OPINION_CLUSTERS/FED_SCDB. Only a distinctively-named case is a real single hit.
2026-09-03 — final Phase A tally, full crosswalk verified: 629 candidates checked across 4 rounds, 405 confirmed real entities, 224 confirmed noise. Every tier-1 cluster (585 after all filter fixes) has now been through at least one independent verify pass — nothing in reports/recon/gen3/ is unverified.
2026-09-03 — the date trap runs in reverse too: FED_USGS_WBD_HUC8.HUC8 is an 8-digit watershed ID ("19010308") that content_recon's ymd8 regex reads as a valid date and tags date_fmt. A column that looks like a date is not a date until checked, same discipline as the ID trap. Scan of all 249 ymd8/mdy8 hits found only this one naming-suspect case — narrow, not systemic — but any auto-cast pass must exclude it by name before running. See scripts/date_cast_inventory.py.
2026-09-03 — ENTITY_XREF.FANOUT is a per-(source table, key pair) CONSTANT, not a per-value count: 6,962 on every one of 2.25M CCN→NPI affiliation rows, 821 on every FEC row. Recompute fanout with a group-by before using it as a junk-hub filter.
2026-09-03 — FED_SAM_EXCLUSIONS_FULL_R2.NPI holds '0000000000' on 12,027 of 19,238 non-blank rows (same sentinel LEIE carries). count(distinct) is safe; count(*) where NPI is not null overcounts 2.7x.
2026-09-03 — INTL_FR_DATA_GOUV_FULL.SPATIAL_GEOM contains 100% of US lat/lon points from nursing homes, colleges, power plants and air sites. A polygon that contains everything is a junk hub in any GEO_IN graph; it faked betweenness rank 5 before it was dropped.
2026-09-03 — the schema graph (CONNECT_EDGES) only knows edges the builder wired: FED_CMS_NPPES carries EIN and PARENT_ORGANIZATION_TIN columns with no EIN edge. "Only table with both keys" means only table with both EDGES; check information_schema.columns before saying a bridge is unique.
2026-09-03 — FED_CMS_NPPES.EMPLOYER_IDENTIFICATION_NUMBER_EIN and PARENT_ORGANIZATION_TIN are '<UNAVAIL>' on every populated row (1,937,362 and 156,566 rows, ONE distinct value each). CMS redacts them. The columns exist, the ids do not; never build an EIN edge from NPPES.
2026-09-03 — a fanout cutoff is not a junk filter: dropping every hospital with 500+ affiliated NPIs from the CCN↔NPI graph made the winners the hospitals with 470–490, right under the knife. Junk = blanks, zeros, '<UNAVAIL>', N/A; size alone is not junk.
2026-09-03 — FRS_ID↔LEI in ENTITY_XREF is a star forest: one LEI, hundreds of facilities, no facility touches two LEIs. Betweenness on a star is 1.0 at the hub and 0 everywhere else; no middleman is possible by construction. Same for any parent→child crosswalk.
2026-09-03 — sampled betweenness (k=300) on the million-node CCN-NPI graph cannot see a degree-2 bridge: the top physicians came out with IDENTICAL scores (0.00334, one sampled source's paths) at rank 233-242, and the biggest real bridge (cut 77) never appeared in the top 200. At that scale use articulation points plus block-cut-tree cut sizes for "quiet middleman"; betweenness only ranks hubs. Blind spot the other way: a middleman with one redundant path scores zero on cut size.
2026-09-03 — LIBRARY_META.CONNECT must be written with the schema quoted, "CONNECT" - it is a reserved word and the bare form throws a syntax error at the schema name.
2026-09-05 — FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_..._BY_REFER: `%_SPRSN_IND is null` does NOT mean the row is whole. In the 171,372 all-flags-null cohort, 88,344 rows have TOT_SUPLR_BENES itself null and 9,253 carry a positive TOT_SUPLR_SRVCS with all three family service columns zero-filled. The DME_/POS_/DRUG_ families do not sum to TOT_: beneficiaries match on 60.5% of testable rows, suppliers 62.8%, services 78.5%. Two separate causes — a total BELOW the sum is de-duplication (a supplier or patient in two families counted once at top; happens only to suppliers and benes), a total ABOVE the sum is a masked family block (money residual is never negative, so de-dup cannot explain it). Never add the families; never compare a family column to a total column as the same population.
2026-09-05 — BENE_DUAL_CNT and BENE_CC_%_PCT in the DME-by-referrer file are interval-censored at 11: BENE_DUAL_CNT publishes 0 or >=11 and NEVER 1-10; the dementia share column is null on 325,834 of 381,228 rows, exactly zero on 37,000, positive on 18,394. The dementia median reads 0.0 because the middle of the distribution is deleted, not because the typical referrer has no dementia patients. Any percentile off these columns is a percentile in a distribution with a hole in it. BENE_AVG_RISK_SCRE is the uncensored alternative — non-null on 381,227 of 381,228.
2026-09-05 — comparing percentiles computed on different denominators is not a comparison. Frank's DME volume ranked on 208,605 rows read 91.3rd while his dementia share on 55,394 rows read 94.4th, which said "sicker than he is high-volume." On the 3,468 rows carrying all four measures the order reverses: volume 93.9th, dementia 92.2nd, risk 92.0nd, dual 87.7th. Always re-rank on the common cohort before comparing two percentiles, and prefer the uncensored measure when one exists.
2026-09-05 — a CKAN package is a FOLDER, and its resources do not share a header. connect/portal_loader.py now pages every datastore_active resource, and pandas unions the keys, so a column present in only some resources is populated on only some rows. Measured on the 32 reloaded Oklahoma tables: 19 of 32 carry partially-filled columns. Worst is Vendor Payments FY2022 at 105 columns, 71 of them partial — PYMNT_AMT holds $7,871,848,150 over 589,381 rows and PAYMENT_AMOUNT holds $1,282,618,447 over 79,407; sum either alone and you lose 14% of the money and a whole month. Expenditure Summary at 1,957,980 rows has AGENCY_NUMBER on 50% of rows. Nine PO tables carry _2-suffixed twins sitting at 0%. The 11 p-card tables are clean at 16 columns. Before summing any portal_ table column, check its fill rate against count(*) and look for an alias twin.
2026-09-05 — ROWID in the Oklahoma portal tables looks like a primary key and is not one: 442,167 rows / 163,508 distinct on p-card FY2016, 668,789 / 343,102 on Vendor Payments FY2022. It restarts per monthly resource, so it collides across a package. It also silently props up drop_duplicates() in load_one — rows survive dedupe partly because ROWID differs. Ignore ROWID and FY2016 still holds 8,651 duplicate groups.
2026-09-05 — MERCHANT in the p-card tables is a card-terminal string, not a merchant identity: 90,600 distinct strings collapse to 34,742 on letters only. WAL-MART #0151 and WAL-MART #3340 are separate strings; Amazon.com, AMAZON.COM, AMAZON MKTPLACE PMTS and Amazon Payments are four. Any "distinct merchants" count off this column is a string count.
2026-09-05 — a bare LANDING name and its mart can be different files. FED_FDA_DEVICE_510K is 88 rows in LANDING, 175,686 in HEALTH__; FED_FDA_MAUDE 1,386 vs 2.74M. The reverse too: FED_DOL_FORM5500_FULL 4.3M vs mart 33k; FED_CMS_NADAC landing 1.5M vs mart 359k; FED_FARA_BULK landing 222k vs mart 48k. FED_FDIC_ENFORCEMENT is 14 rows, a stub. Check live_rows.json or count(*) on BOTH names before calling a gap or picking a leg.

## Tier-1 deep dive traps (2026-09-05, 21 hunches, each skeptic-checked)
2026-09-05 — FED_USASPENDING_CONTRACTS_FULL_R2 columns are UPPERCASE; the 2026-08-31 lowercase-USAspending trap does not apply to R2. `"recipient_uei"` quoted fails, bare RECIPIENT_UEI works.
2026-09-05 — USAspending CURRENT_TOTAL_VALUE_OF_AWARD varies per transaction within one award (Tribute: 255K / 155.98M / 70M / 5.3M / 255K on five rows); summing it is not spend and max-per-award is a ceiling. Money moved is FEDERAL_ACTION_OBLIGATION, and it is signed: 90% of in-ban actions are ≤ 0, so filter obl > 0 or every "paid while banned" total reads negative.
2026-09-05 — SAM exclusions join fans out: 1,798 UEIs carry 3+ rows with overlapping windows, so a join to award windows double-counts actions (2,289 → 1,758 distinct). Use EXISTS against the windows, never a join, before summing. ACTIVATION_DATE carries 1908 / 2084 / 2099 sentinels and 11,016 nulls; CAGE_CODE is filled on 392 of 168,328 rows; the mart is Active-only so purged past bans are invisible and every count is a floor.
2026-09-05 — HEALTH__FED_CMS_OPEN_PAYMENTS (bare) is PY2024 only; _2022 and _2023 are separate tables with zero RECORD_ID overlap. A query with no PROGRAM_YEAR filter is safe today and breaks the day a second year lands. The mart drops the manufacturer-ID column (so the id-as-money trap cannot fire there) and drops drug-name and therapeutic-area columns (product questions must go to LANDING). Payer names split on case ('ABBVIE INC.' / 'AbbVie Inc.'); fold before ranking. Natures "Debt forgiveness" ($40.8M) and "Acquisitions" ($213M) put people in the top money decile with no cheque cut; split by nature before naming anyone as "paid". Blank NPI is '' not null (48,059 rows PY2024) and dropping it removes 43% of all royalty dollars, more than any other nature. 73 rows carry year-0002 DATE_OF_PAYMENT; min(date) is unusable.
2026-09-05 — LEIE mart renames every landing column (LASTNAME→LAST_NAME, EXCLTYPE→EXCLUSION_TYPE, EXCLDATE→EXCLUSION_DATE) and blanks the '0000000000' sentinel to '' (74,908 rows), so filtering the sentinel by value on the mart catches nothing. WAS_REINSTATED is false and REINSTATEMENT_DATE blank on 100% of rows; landing REINDATE is 00000000 everywhere: the monthly file is active-exclusions only, reinstatement answers itself by construction. Only 8,839 of 83,747 rows (10.6%, 8,660 distinct) carry a real NPI, so any NPI join to LEIE measures a tenth of the ban list and every hit count is a floor. Mart _INGESTED_AT is epoch-microseconds-as-TIMESTAMP and min() throws "year 56656460"; read with to_varchar or use landing INGESTED_AT. SOURCE_FRESHNESS said data through 2026-06-18; the table holds exclusions through 2026-08-20.
2026-09-05 — LEIE exclusion type "1128Aa" is 172 rows all-time, 25 of them in 2026, 24 in one June 2026 window, 22 of those DME business names; the eight big DME exclusions in hunch 23 all come from that block. Don't gloss the code without a source, and don't read "0 of 8,129 pre-2026 exclusions in the DME file" as suspicious: only 520 of those are orgs and 33 have a DME specialty.
2026-09-05 — HCRIS mart typed the text 'nan' into FLOAT NaN, not NULL (NET_INCOME 89 rows, TOTAL_FUND_BALANCES 309, NET_MARGIN_RATIO 245, revenue 237): count() counts them, `is not null` passes them, `< 0` is false. Guard with `iff(x = 'NaN'::float, null, x)` or `to_varchar(x) <> 'NaN'`. NET_MARGIN_RATIO is NET_INCOME / gross charges, reads 2-3x smaller than a real margin and flips sign on 164 rows; use NET_INCOME over cost. The warehouse holds ONE HCRIS vintage (FY ends 2022-11 to 2024-09, one 12-month report per CCN, 0 with two): no hospital has a trend, "years of losses" is untestable, and "the year before" is a cross-section. CASH_ON_HAND_AND_IN_BANKS goes negative.
2026-09-05 — HCRIS seller stubs: when a hospital is sold the seller files a terminating report ending the day before CHOW_DT (25 of 26 short pre-sale reports). Sub-300-day reports lose 65% of the time vs 34% for full years; in the sold cohort stubs lose 85%. Any before/after-sale comparison must filter FISCAL_YEAR_LENGTH_DAYS >= 300 or it inherits the stub bias. For-profit S-10 charity care is mostly blank (1,120 of 1,841 for-profit reports NaN vs 355 of 3,055 nonprofit), so nonprofit-vs-for-profit charity is nonprofits vs the larger for-profits that filled the worksheet.
2026-09-05 — POS_OTHER: CHOW_DT is the effective date (75% land on the 1st, 25% on weekends), not a filing date, and POS keeps only the latest CHOW per CCN. CHOW_SW is '' on all 44,429 rows. MEDICARE_MEDICAID_PRVDR_NUMBER has one distinct value on 15,324 rows; the id column is CCN. No POS_OTHER category is a nursing home. CAH_OR_HOSPITAL_CCN splits on '|', not '/'; the wrong separator returns the whole string and silently matches 21 predecessors instead of 35.
2026-09-05 — SKILLED_NURSING_FACILITY_ENROLLMENTS.INCORPORATION_DATE is 62% filled, has 103 pre-1900 values, and maxes at 2024-09-17 in a 2026 file: not a recency clock, blind for 17 months of penalties. ENROLLMENT_ID is O+YYYYMMDD+6 digits (14,425 of 14,425 parse, runs to 2026-02-12) and is the record-creation date; validated against NH411's ownership-change flag, 54 of 54 'Y' homes have a record dated ≥ 2024-08-31. PROVIDER_CHANGED_OWNERSHIP_IN_LAST_12_MONTHS is all 'N' on FED_CMS_NURSING_HOME but 'Y' on 55 rows of FED_NURSINGHOME411; the old "N everywhere" note was one table.
2026-09-05 — NURSINGHOME411 CHAIN_ID is '' on 4,551 homes and count(distinct) counts it: 617 chains, not 618. CHAIN_NAME ilike '%bria%' also catches BRIAR HILL MANAGEMENT; pin on CHAIN_ID. The roster is one snapshot dated 2025-12-01 applied to fines back to 2023-06-17, so late joiners carry prior-owner fines and departed homes are invisible; the 12-month ownership flag says nothing about 2023. Illinois fines $825/bed vs $261 rest of US: any "x times national" for an Illinois chain is mostly Illinois. Repeat-tag rate tracks survey frequency at r=0.84 across chains; normalize per survey date.
2026-09-05 — NURSING_HOME_DEFICIENCIES is a rolling window with a tail, not a 2017-26 series: 40 homes in 2017, COMPLAINT_DEFICIENCY is 'N' on 100% of rows before April 2023 and switches on in Q2 2023. Never chart it as a trend or standardize on the complaint flag pre-2023. PENALTIES: only PENALTY_TYPE='Fine' carries FINE_AMOUNT; 2,470 Payment Denial rows have blank FINE_ID and count(distinct FINE_ID) drops them silently.
2026-09-05 — Sprinkler flag lives in FED_CMS_NURSING_HOME (mart PROCESSING_DATE null on all 14,700 rows; LANDING carries 2026-05-01), K-tags in FED_CMS_NURSING_HOME_FIRE_DEFICIENCIES; NURSINGHOME411 and NURSING_HOME_DEFICIENCIES hold neither. K0351 is the only "no sprinkler" tag; LIKE '%sprinkler%' inflates 4x. DEFICIENCY_CORRECTED is a status not a boolean ('Waiver has been granted' = open by permission, and can outlive a clean later survey without being closed); CORRECTION_DATE is a promise, 4 post-date the file's own publication.
2026-09-05 — HEALTH__FED_CMS_PART_D_PRESCRIBERS (by-provider) is data year 2024; the DY22 note above is the by-drug table. OPIOID_TOT_CLMS '' is a suppressed 1-10, not zero; '0' is the real zero; OPIOID_PRSCRBR_RATE is null exactly on the blanks. Part D is one year: "paid then prescribed more" has no before/after here, only targeting.
2026-09-05 — NPPES mart strips deactivated rows to blanks: ENTITY_TYPE_CODE '' on all 346,179 deactivated NPIs, dates NULL and text '' on the same row, deactivation reason blank on every one. Identity of a dead NPI rests on whatever other table names it. The NPI is a real key (9,606,683 rows, 9,606,683 distinct), so no fan-out is possible.
2026-09-05 — Home health: 95 HHA enrollment rows carry a 7-char CCN with a letter suffix (branch offices); a bare 6-char join drops them. "Not in PECOS" (1,179 agencies, 78% blank stars) is a third group, not independent; folding it in moves the blank rate 32.6% → 37%. Care Compare episode count tops out at 998, the top band is capped. HHCAHPS patient-survey stars are not landed anywhere.
2026-09-05 — HOUSING__FED_MAPPING_INEQUALITY mart is one polygon per (city, grade): 1,155 rows vs 10,154 in LANDING; any spatial count off the mart is on 11% of the map. LANDING GeoJSON parses with TRY_TO_GEOGRAPHY on 10,153 of 10,154. HOLC_ID is one distinct value, not an id; 814 blank grades plus 3 trailing-space spellings. TRI_FACILITY FAC_LATITUDE/LONGITUDE are packed DDMMSS in a NUMBER column with 2,918 zeros and ~40 swapped pairs; PREF_LATITUDE is whole degrees; TRI_BASIC_2023 has clean decimals. Grade A holds ONE facility, so any "vs A" ratio is n=1; use a 500 m buffer for a stable multiplier.
2026-09-05 — FEMA IA FIPS is unpadded TEXT for states 01-09 ('1097' and '01097' both exist; 636 distinct → 601 after lpad; 69,662 null). HMDA_HISTORIC STATE_CODE/COUNTY_CODE unpadded too, and it has NO date column, year only; county-null rows (19,331 denials) fall into any control group unless COUNTY_CODE is not null is on every query. Harvey/Irma/Maria "after" years are 2018, outside the table.
2026-09-05 — DME-by-supplier file has no total-paid column; money is TOT_SUPLR_SRVCS × AVG_SUPLR_MDCR_PYMT_AMT. _SOURCE_RUN_ID is unique per row (440,670 values), not a run id. The supplier mart has no _INGESTED_AT; the 2026-07-26 date lives only on landing. Skin-substitute HCPCS: Q4100+ is the strict family, A2001-A2999 is a second family a Q4-only filter misses, Q4001-Q4099 are casting supplies a bare 'Q4%' leaks in.
2026-09-05 — Pending-applicant files: the physician/non-physician split is not a credential (a chiropractor and a PA sit in the physician file); 17 NPIs appear in both. Opt-out affidavit file is a live snapshot: 754 duplicate NPI rows, all end dates ≥ 2026-06-30, no lapsed-opt-out history, so any cohort is survivors. ORDER_AND_REFERRING carries NPIs NPPES has deactivated, and one NPI changes surname between LEIE and CMS files; join on NPI never name.

## Politics probe traps (2026-09-05, 22 hunches probed)
2026-09-05 — FINANCE__FED_FEC_INDIV_CONTRIBUTIONS is 99.99% 2023-2026 (12 stray rows back to 2000, sentinels to year 3312); it is a four-year file, not a series. Any join to 2015-era disbursements or 2012-2020 trades is matching old payments to later gifts. It has no MEMO_CD; earmark rows are TRANSACTION_TYPE 15E.
2026-09-05 — FEC independent-expenditure mart (261K rows, 2018-2024) and LANDING (87.5K, 2024-2026) are different vintages with no overlap, and the mart's national totals read ~20x the FEC's published figure ($47B for 2022). Trust roster-level sums after amendment dedupe only; never chart national totals off it. CONNECTED_ORG_NM is blank or junk on most big spenders.
2026-09-05 — FINANCE__FED_FEC_COMMITTEES_DIM has no ZIP column; the ZIP leg must come from LANDING FED_FEC_COMMITTEES.C8, which repeats ids across cycles (60,031 rows, 38,693 ids): count people, never pairs. FED_FEC_LEADERSHIP_PAC is a 2024-only file.
2026-09-05 — POLITICS__SENATE_TRADES runs 2012-06 to 2020-12 only, 2,111 blank tickers, matched by surname plus term span; bills, votes and rollcalls start 2023. No overlap: any trade-then-vote or trade-then-bill hunch is dead until a 2023+ trades file lands. FED_HOUSE_FD_PTR_INDEX has no ticker, asset or amount; trade lines are in the PDFs. FED_CONGRESS_COMMITTEE_MEMBERSHIP is a current snapshot with no term dates. FED_SEC_EDGAR_COMPANY_TICKERS has no SIC; SIC comes from FED_SEC_DERA_SUB_* by CIK. FED_GOVINFO_BILLSTATUS has no subject column, only TITLE.
2026-09-05 — Google POLADS ELECTION_CYCLE is null on every weekly row; ADVERTISER_STATS.PUBLIC_IDS_LIST (FEC id / EIN / "Registered in US-CA") is the real key, not advertiser name.
2026-09-05 — FED_FARA_BULK Short-Form rows have SHORT_FORM_LAST_NAME/_FIRST_NAME/_DATE/_TERMINATION_DATE blank on all 43,168; the person lives only in SHORT_FORM_NAME ('Last, First') and the date only in DATE_STAMPED. Registrant windows sit on blank-DOCUMENT_TYPE rows; one registration number carries 1,281 rows. FEC EMPLOYER first-8-letters = registrant firm is the join that works (0 of 3 false); name-only inflates 9x.
2026-09-05 — Sanctions lists carry DOB but no US address; FEC carries neither, so sanctioned-name matches into FEC are 100% noise on eye check (3 of 3). OFAC SDN_TYPE is the string '-0- ' (9,785 rows) for entities, not blank; the UK list spells NAME_TYPE 7 ways ('Alias' 34k, 'ALias' 2).
2026-09-05 — FED_DOL_OLMS SHORTAGE_AMOUNT is non-zero on 78 of 617,710 rows and every one is a column-shifted year (2009/2010) with UNION_NAME numeric and YEAR_COVERED null; landing SHORTAGE same 78. There are no shortage dollars.
2026-09-05 — FED_REVOLVINGDOOR_PROJECT PERSON_NAME is 'nan' on 405 of 406 rows and '3' on one; both appointee flags false on all; landing has no name column. It is a positions-by-sector matrix, not a people table.
2026-09-05 — EDUCATION__FED_SENATE_LDA_FILINGS covers 1999-2010 and 2020-2021 only; 2011-2019 is missing. INCOME and EXPENSES are TEXT and mutually exclusive by filer type. FED_FEDERAL_REGISTER_DOCUMENTS runs 2023-01 to 2026-06, so lobby-vs-rule has zero overlap.
2026-09-05 — CA_LOBBY_COVER RPT_DATE spans year 4 to 5005 and FIRM_NAME is a firm, not a person; TX lobby amounts are range codes (exact on 29%) and TX GIFTS has no ACTIVITYDATE.
2026-09-05 — FED_EAC_EAVS has no codebook landed; C8A + C9A = C1B on 6,014 of 6,460 rows is the working key for rejected/returned mail ballots; -99 and -88 are sentinels on 231 rows; Wisconsin reports by municipality (1,851 rows) and drops out of a county join. Vera 2024 has jail rate on 1,440 counties vs 2,865 in 2018.
2026-09-05 — No congressional-district geometry exists in the warehouse (checked both catalogs for DISTRICT/CONGRESS/TIGER/CD; only CB_STATE/COUNTY/ZCTA). Any "by district" hunch rolls to state or dies. House office allowance is a formula ($1.28M-$1.75M by state), so member spend has no variance to correlate.
2026-09-05 — FED_HOUSE_DISBURSEMENTS payee ∩ FEC donor is 1,318 of 1,325 House staffers giving to their own boss; the "vendor" leg does not exist without a city on the disbursement side.
2026-09-05 — FED_COURTLISTENER_INVESTMENTS rows reading "X Bank Accounts" are cash deposits, not equity; 93% of the wide judge-vs-party number is that. FINANCIAL_DISCLOSURES.YEAR is column-shifted text on 38,530 of 70,776 rows. IDB FILEJUDG is blank on the five biggest districts; use DOCKETS.ASSIGNED_TO_ID (32.4M rows, 3,350 judges) and FED_COURTLISTENER_FJC_IDB_CL_LINKED (IDB_DATA_ID), not FED_FJC_SERVICE, which carries no district-local judge code. JUDGMENT is filled on 21% of civil cases; pro se plaintiffs win 2% vs 13%, hold pro se constant. Creditor names are OCR ("AMCRICAN EXPRESS" 167 rows).
2026-09-05 — NURSINGHOME411 "chains" include hospital systems (HCA, Lifepoint); `contains` on normalized chain names gave 5 of 15 substring false positives (FRONT PORCH, ENCOMPASS, ACADIA). LEIE org names do not reach FEC donors without an address bridge: generic institutional names collide even multi-word (HEALTH PARTNERS Evansville vs Minneapolis).
2026-09-06 — CA_LOBBY_COVER.RPT_DATE is TEXT in US 12-hour form, '5/1/2000 12:00:00 AM'. The shared recency parser in build_freshness_ledger.py cannot read it: TRY_TO_DATE and TRY_TO_TIMESTAMP both return NULL on that shape, so all 568,988 rows parse to nothing and the table reads as unmeasured, not as the year 4 to 5005 span noted on 2026-09-05. Any source landing this format is silently invisible to the freshness ledger too. CORRECTED 2026-09-07: WRONG — `recency_inner`'s `us_dt` branch (added same day as this line, still live) parses exactly this US 12-hour format. 568,848 of 568,988 rows return a real MAX date; the table is not unmeasured.
2026-09-06 — the freshness column and the coverage column are not the same column. build_freshness_ledger.py picks whichever answers "how recent is this table", which is right on an event table and wrong on a snapshot. FED_EPA_ECHO maps to FAC_DATE_LAST_INSPECTION, a per-facility attribute: 3,157,891 rows, 82.1% carry no such date, and the resulting 1908-2026 span with 62 missing years is a picture of inspection dates, not a data hole. FED_CMS_LTCH is the same shape on CERTIFICATION_DATE. Read any span next to its unparsed share.
2026-09-06 — the shared recency parser's bare-year branch only matches 19xx and 20xx, so no year column can yield a date before 1900. XC_OWID_CO2 runs to 1750 live and its 5,979 pre-1900 rows land in the unparsed count. Four sources sit pinned at 1900 for this reason, which is a parser boundary and not their real start. CORRECTED 2026-09-07: WRONG for this source — XC_OWID_CO2 is mapped to the wide-year branch, not the bare-year branch this line describes. 0 of its 5,979 pre-1900 rows land unparsed.
2026-09-06 — Snowflake's REGEXP_LIKE matches the WHOLE string, not a prefix. A pattern like '^(19|20)[0-9]{2}' therefore matches a bare '2023' and fails on '2023-09' or '5/1/2000 12:00:00 AM'. Every prefix-style pattern needs a trailing .* here. This silently cost the freshness parser four date shapes and pinned four sources at 1900. CORRECTED 2026-09-07: the regex lesson is real, checked directly in Snowflake. The "four sources at 1900" consequence is not — only one source is even sub-1900-adjacent, and it drops to unmeasured, not pinned to 1900. Neither the live ledger nor either same-day backup shows a source at 1900.
2026-09-06 — FED_FDA_DRUG_ENFORCEMENT is one row holding the whole openFDA envelope, meta and results in a single RAW variant. It is not a per-record table and has no per-row date. FED_CMS_DIALYSIS.FIVE_STAR_DATE is a range string, '01Jan2021-31Dec2024', identical on every row.
2026-09-06 — build_freshness_ledger.py --apply clears SOURCE_FRESHNESS with a DELETE before reinserting. It is not additive. Copy the table first; SOURCE_FRESHNESS__PREV_20260906 is the 2026-09-06 rollback copy.
2026-09-06 — FED_USASPENDING_CONTRACTS is one fiscal year, 6.3M rows, 2024-10-01 to 2025-09-30. FED_USASPENDING_CONTRACTS_FULL_R2 holds the same data 2006-10-01 to 2026-08-22, 93M rows, and neither FULL nor FULL_R2 has a freshness ledger row. The ledger tracks the smallest and oldest of the three. Check which contracts table you mean before using either.
2026-09-06 — the FED_USASPENDING_CONTRACTS_FULL server-side spec has a frozen manifest of 20 URLs dated 20260706. USAspending deletes the prior month's archive, so all 20 now 404. Only 20260806 exists. Its S3 listing pages at 1000 keys and the 20 files span positions 302 to 4596, so a single-fetch regex resolver cannot find them all. CORRECTED 2026-09-07: fixed before this line was written — the same commit shipped `_fetch_listing_pages` in scripts/server_side_load.py, which walks every page of the S3 listing (`paginate: "s3"`) rather than fetching once. Reran it: finds 20 of 20 current files.
2026-09-06 — the FEC bulk download URLs redirect to s3-us-gov-west-1.amazonaws.com, a GovCloud host. Snowflake's server-side fetch refuses it because the host is not in the egress network rule, so all five FEC entries in BULK_REFRESH fail with "Please verify url is present in the network rule". Nothing wrong with the URLs themselves. CORRECTED 2026-09-07: WRONG — the live RIPPLE_BULK_EGRESS rule already allows that host. The one real run logged for these five sources failed on a never-shrink row-count guard (see the same-day entry below on single-cycle FEC manifests), not a network-rule rejection; no run anywhere logs the quoted error text.
2026-09-06 — RIPPLE_REFRESH_SOURCE fetches the file BEFORE it compares the origin ETag, so "unchanged" saves the COPY and the swap but not the download. Without a cadence filter the nightly task pays full download for every enabled source every night. The filter now lives in RIPPLE_REFRESH_ENABLED; the pre-filter DDL is at infra/ddl/09b_refresh_cadence_filter.PREV.sql.
2026-09-06 — every FEC entry in BULK_REFRESH stores a single 2018 cycle URL while the live table holds many cycles: FED_FEC_CANDIDATES is cn18.zip at 7,371 rows against 27,095 live. A server-side refresh would replace a multi-cycle table with one year; the never-shrink guard catches it. Four of the five carry no cycle column, so a per-cycle append would be indistinguishable afterwards. BULK_REFRESH holds one URL per source and cannot express a manifest.
2026-09-06 — GET_DDL on a Snowflake procedure returns the name WITHOUT its schema. Re-running that text creates a copy under the session's current schema, which for the scripts door is LIBRARY_RAW.PUBLIC, and the real procedure never changes while everything reports success. Always qualify the name before redeploying. A stray RIPPLE_REFRESH_SOURCE sits in LIBRARY_RAW.PUBLIC from exactly this. CORRECTED 2026-09-07: the GET_DDL behavior is real and worth guarding against, but the stray copy doesn't exist — checked the whole account, only one RIPPLE_REFRESH_SOURCE anywhere, correctly schemed. Real bug, invented consequence.
2026-09-06 — congress_committee_membership_load.py and fec_independent_expenditure_load.py have no argparse. main() ignores argv, so `python3 <loader>.py --help` runs the FULL load and replaces a live table. Two tables were swapped today believing it was a help screen. Check for argparse before treating --help as a smoke test. CORRECTED 2026-09-07: fixed the next commit, same day the bug was written down. Both scripts `import argparse` now; `--help` prints usage and exits, no fetch, no load. This trap line was never updated after the fix shipped.
2026-09-06 — ingest.assess_density returns a key named "empty", never "ok". Reading it as density.get("ok", True) turns the density gate into a rubber stamp that scores an all-blank frame as success. Subscript density["empty"] so a contract change is loud.
2026-09-06 — the FEC individual contributions bulk file carries at least one field larger than Python's 128 KB csv default, which kills loadkit/fec_parse.py with "_csv.Error: field larger than field limit". It surfaced on cycle 2020 after 63.6M rows had already been staged. The limit is now raised in fec_parse.
2026-09-06 — the FEC Schedule E bulk file carries prank filings. Nineteen rows across 2018-2024 hold $91.0B, including $9.98B from "THE COURT OF DIVINE JUSTICE" and $6.35B from "Republican Emo Girl". Every junk row is BOTH web-filed, TRAN_ID starting 'WFT', AND over $20M; neither test alone is safe, since the plain dollar cap also catches 23 real FF PAC / MAGA Inc rows worth $1.371B and the WFT prefix alone catches 5,339 real small filers worth $191M. Amendments are a separate, much smaller inflation: a superseded filing is one whose FILE_NUM appears as another row's PREV_FILE_NUM, worth $1.34B on 2024 alone, and Food & Water Action's $114M row repeats nine times. 2024 walks 49.68 -> 4.44 $B with both flags applied, against the roughly $4.4B the FEC publishes. Landing now carries IS_SUSPECT_FILING and IS_SUPERSEDED; nothing is dropped. CORRECTED 2026-09-07: the dollar total is wrong on the full 35-row flag (all five cycles, 2018-2026) — resumming those rows fresh gives $129.53B, not $91.0B, off by $38.5B/42% low. This line's own "nineteen rows across 2018-2024" scope was never reconciled against the 35-row total quoted elsewhere for the same flag; treat that narrower count as unverified too, not just the dollar figure.
2026-09-06 — committees-historical.yaml in unitedstates/congress-legislators holds NO membership, only committee names and which congresses each sat in. The roster history lives in the git history of committee-membership-current.yaml, 210 commits back to 2012-11-09. Second trap on top: the LAST commit of a congress is the file EMPTIED for the incoming congress. Commit ee290b5d, 2021-01-01, has zero seats where the same file six days earlier had 3,847. Walk a term's commits newest-first and take the first with a real roster.
2026-09-06 — FED_CONGRESS_COMMITTEE_MEMBERSHIP.PARTY is not a party. It holds 'majority' and 'minority', 15,074 and 11,897 rows, on every congress. Join to the legislators table for D/R.
2026-09-06 — POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP is one row per congress per seat, 26,970 rows over congresses 113-119. Joining it to money without a dedupe multiplies every dollar by the number of congresses that member served. On Ways and Means plus Senate Finance in 2024 that turned $252.1M of independent expenditure into $1,431.9M, a 5.7x fan-out that reads as completely plausible. Making the join congress-aware does NOT fix it, only $252.1M to $249.1M; the fix is select distinct on the roster. Average is 3.49 congresses per member, weighted higher on the big-money incumbents.
2026-09-06 — a TIMELINE view freezes its column list at create time. Adding three columns to FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES broke LIBRARY_MARTS.TIMELINE.FINANCE__FED_FEC_INDEPENDENT_EXPENDITURES with "declared 27 column(s), but view query produces 30". The view reads src.*, so any mart column change breaks it. Regenerate the timeline view after any mart column change. CORRECTED same day: the claim that TIMELINE__WAREHOUSE does not include it was WRONG. TIMELINE__WAREHOUSE is a view over 31 MATERIALIZED TIMELINE__*_INDEX rollup tables, all last written 2026-08-30, and TIMELINE__FINANCE_INDEX still says the IE source is 261,033 rows ending 2024 while the live view reads 276,183 over five cycles. Its 1,167,067 row count is unchanged BECAUSE it is stale, not because nothing broke. Sweeping all 403 timeline views with a limit-0 select proves they COMPILE and cannot see a stale materialized rollup. No builder for the _INDEX tables exists anywhere in the repo, so scripts/refresh_timeline_index.py was written to refresh one source by rebuild rather than delete. FINANCE is now current at 276,183 across five cycles and TIMELINE__WAREHOUSE reads 1,167,068. The committee roster was given a timeline view the same day and now sits on the index at 7 days, 26,970 rows, 2014-11-13 to 2026-09-02. Its clock is 'reported', NOT 'happened': SNAPSHOT_DATE is the day the roster was read, and nothing happened on it. Any mart rebuild needs its _INDEX row refreshed too, or the shared timeline silently keeps the old span.
2026-09-06 — dbt cannot log in on the Mac. profiles.yml defaults the private key to C:/Code/Ripple_v6/.keys/ripple_dbt.p8, the Windows box's path, .keys/ is gitignored, and no .p8 exists on this disk. Snowflake's RSA_PUBLIC_KEY_2 slot is set but its private half is gone. So there are three doors, not two: Python scripts open, dbt shut, chat plug-in shut. scripts/build_marts_python_door.py builds a mart without dbt, but it does NOT read dbt_project.yml, so it ignores +enabled: false and the marts.politics pre-hook guard that would have refused the build. It also creates non-transient tables where dbt-snowflake creates transient ones: 648 of 678 sibling marts are transient, these two are not.
2026-09-06 — CAND_ID is blank, not null, on 33,937 IE rows, 12.3%. dbt's not_null test passes because landing is all TEXT and blanks arrive as ''. On clean 2024 alone that is 8,151 rows carrying $541.9M that attribute to no candidate.
2026-09-06 — the per-congress committee roster misses 14 to 35 members per congress against Voteview, about 4%, and the misses are not random. Half are legitimate: the Speaker and the party leaders hold no committee seats. The other half is real invisible turnover, biased toward exactly the people a corruption question targets. The 118th is missing Feinstein, Menendez, Santos, Gaetz, McCarthy and 19 others, all mid-term deaths, resignations or an expulsion. Menendez chaired Senate Foreign Relations, was indicted and resigned mid-118th, and is not in the 118th roster at all. One snapshot per congress also hides seat changes inside a congress: a member who joined a committee in year two is credited with the whole cycle. Never write "was on the committee in 2021"; write "held the seat as of that congress's snapshot date".
2026-09-06 — coverage_probe.py measure --write APPENDS to LIBRARY_META.REGISTRY.SOURCE_COVERAGE_YEARS, it does not replace. After a rebuild the table holds both the old and new measurement for the same SOURCE_ID and DATA_YEAR, distinguishable only by MEASURED_AT and N_TOTAL. Read the newest MEASURED_AT per source or the row count is whichever one the query happened to hit.
2026-09-06 — the marts.politics folder carries a +pre-hook guard_politics_mirror() in dbt_project.yml, written to stop anything but the hand-reconciled Python loaders from overwriting a POLITICS mart. dbt would refuse politics__fed_congress_committee_membership without --vars allow_politics_rebuild. build_marts_python_door.py never reads dbt_project.yml, so it bypasses that guard and +enabled: false too. It is not a dbt substitute; it is a way past dbt's safety rails when dbt cannot log in.
2026-09-06 — FED_CMS_HCRIS column names MOVED when it was reloaded. The old landing carried FTE___EMPLOYEES_ON_PAYROLL with three underscores; the current ingest._stringify collapses separator runs, so the same column now lands as FTE_EMPLOYEES_ON_PAYROLL. Twenty-two staging references broke at once and the staging view went dark with "invalid identifier". Any reload of an old table through land() can rename columns under downstream models, silently, because the sanitiser changed since that table was first written. Check the staging model against the new landing columns after any reload of a pre-2026-09 table.
2026-09-06 — the HCRIS grain is RPT_REC_NUM, unique on all 80,077 rows across 2011-2023. PROVIDER_CCN plus SOURCE_FILE_YEAR is NOT unique: 1,186 hospital-years carry more than one report, because a hospital files several short cost-report periods inside one file year around an ownership change. CCN 340090 filed three in 2014. Those splits are evidence for question E43, not noise to collapse. The old staging dedupe partitioned on ccn plus name plus fiscal_year_end_date ordered by _ingested_at, which is arbitrary now that all thirteen years landed in one run and share one timestamp.
2026-09-06 — SOURCE_FILE_YEAR on HCRIS is the CMS file label, not the hospital's fiscal period. Irwin County Hospital's 2023 file row covers 2022-12-01 to 2023-01-31. Group by the stamp for "which file", by FISCAL_YEAR_END_DATE for "which period".
2026-09-06 — IRS 527 Schedule A and Schedule B are both 18 fields wide and they DIVERGE AT POSITION 15. A holds the year-to-date aggregate at 15 and the contribution date at 16; B holds the expenditure date at 15 and the purpose at 16. Align the two by position and the date column lands on an aggregate. Read the values to tell them apart: A's 15 repeats the amount, B's 15 is YYYYMMDD. Field 17 is empty on all 17.9M rows, a trailing pipe rather than a field. The IRS layout doc is a legacy binary .doc this environment cannot render, so this was measured, not read. 25 ragged rows in 17,893,129, counted and dropped rather than padded.
2026-09-06 — landing has TWO meta-column conventions and both are live. Tables written through land() carry _INGESTED_AT with a leading underscore; tables written through write_pandas plus ingest._sf_col carry INGESTED_AT without it, because _sf_col strips the leading underscore. FED_CMS_HCRIS has the underscore, FED_FEC_INDIV_CONTRIBUTIONS and every IRS527 table do not. Anything that looks for one name finds half the warehouse.
2026-09-06 — GovInfo BILLSTATUS XML uses <number> and <type>, NOT <billNumber> and <billType>. A first guess reaches for the long names and silently gets None on every row. Thirteen rows across 107,150 carry no bill number at all: eleven are 117th-congress placeholders titled "Reserved for the Speaker" or "Reserved for the Minority Leader", and two are real bills whose XML simply omits number and type. Landing keeps them; filter nullif(trim(BILL_NUMBER),'') is not null before joining.
2026-09-06 — LAW_NUMBER on FED_GOVINFO_BILLSTATUS is an EMPTY STRING, never NULL, on the 104,998 bills that never became law. "count_if(LAW_NUMBER is not null)" therefore counts every bill and reports a 100% enactment rate. Use nullif(trim(LAW_NUMBER),''). The real rate falls from 2.8% in the 113th to 1.4% in the 118th.
2026-09-06 — Senate EFD filer last names carry their suffix and sometimes a bare trailing comma: 'Perdue , Jr', 'McConnell, Jr.', 'Manchin, III', 'Moran,'. A plain last-name join of the 62 distinct 2021-2026 filers to POLITICS__MEMBER_CROSSWALK lands 26 clean, 29 ambiguous and 7 missed, because the crosswalk holds every member in history and 'Marshall' hits 18 people. Strip the suffix AND restrict candidates to people who held a Senate committee seat in congresses 116-119, and it is 62 of 62 with no fan-out. The 116th is required, not optional: Perdue and Roberts left in January 2021 and appear in no 117th roster. CORRECTED 2026-09-07: the described fix isn't implemented anywhere in the codebase — senate_efd_ptr_load.py only strips the suffix/comma and says in its own docstring that "the join itself belongs in the mart, restricted to people who actually held a Senate seat in the term"; finance__fed_senate_efd_ptr.sql repeats that same intent as a comment with no actual join to POLITICS__MEMBER_CROSSWALK anywhere in its SELECT. Hand-reconstructing the fix does not reach 62 either — an earlier pass on the same day got 61 clean/1 ambiguous by counting on the raw (unstripped) last name; re-run on FILER_LAST_CLEAN (the actual join field this trap describes) the live index gives 59 distinct filers, not 61 or 62, and that number holds by every counting method tried (57 on full name, 59 on cleaned last name, 61 on raw last name, 62 on raw first+last pairs — none of them is a clean 62). The one ambiguity every method agrees on: "Scott" still matches both Tim Scott and Rick Scott, both sitting senators on a relevant committee across congresses 116-119 — Rick Scott is the one who actually filed, Tim Scott is not a filer but is a same-name committee match, so the collision is real either way.
2026-09-06 — a House PTR's format is readable off its DocID alone. Prefix 2 is an extractable text PDF, 2,633 filings; prefixes 8 and 9 are scans on which pypdf returns zero characters, 421 and 51. So the scan list comes from the index and those PDFs never need fetching. No tesseract binary and no pytesseract in this environment, so scans cannot be read at all. On the Senate side the link path says the same thing: /search/view/ptr/ is HTML, /search/view/paper/ is a scan, 699 and 100.
2026-09-06 — House PTR text loses its table structure under pypdf. A trade line arrives as 'P 10/09/202511/01/2025 $1,001 - $15,000' with no separator between transaction date, notification date and amount, and the asset name and ticker on the one or two lines above it. It is a line-state machine, not a table read. Neither chamber reports a dollar figure, only a range, so any total is a bounded estimate. CORRECTED 2026-09-07: false for the House specifically — 68 non-blank, non-scan rows carry a genuine single dollar figure ($669.27, $898.16, $4,450.50, etc.), not a range. Still true that no dedicated exact-dollar column exists in either pipeline; some row content is exact even though no column promises it.
2026-09-06 — the 283.7M-row donor mart carries 51,578 rows whose TRANSACTION_DT does not parse, and at least one that parses to 2106-08-27 and lands in the timeline as clock 'planned'. Both show up in TIMELINE__FINANCE_INDEX as a NULL RIPPLE_DAY bucket and a future day. Read any donor date span next to its unparsed count, the same rule already recorded for the freshness ledger. CORRECTED 2026-09-07: the mart's real unparseable count is 51,555, confirmed three independent ways, not 51,578. 51,578 is TIMELINE__FINANCE_INDEX's null-day bucket count — a different table. Conflated the two and got the mart's own number wrong by 23 rows.
2026-09-06 — pypdf emits NUL BYTES, not spaces, in House disclosure PDFs. The line that looks like "F      S     : New" is really 'F\x00\x00\x00\x00\x00 S\x00\x00\x00\x00\x00: New'. Python's \s does not match \x00, so every pattern written against the visible text silently fails and the form's own label lines get swallowed into whatever field is being built. A first pass landed "F S : New S O : R.W. Allen & Associates" as an asset description because of this. Replace \x00 with a space before matching anything.
2026-09-06 — a House PTR trade is THREE lines, not one. The asset name spans two lines with the owner code SP/DC/JT at the front of the first; the trade line carries type and two run-together dates; the amount's upper bound is on the line AFTER. 'P 04/09/202405/09/2024$50,001 -' followed by '$100,000' is one $50,001-$100,000 purchase. Parse it as a bare line and it lands as "$50,001", which reads like a number rather than the bottom of a range. Anchoring the regex at ^ also misses every filing that puts the asset and the trade on one line: 20 of 35 matched anchored, 35 of 35 searching.
2026-09-07 — House PTR owner codes CANNOT be split off with a word boundary, and every obvious rule breaks more than it fixes. pypdf glues the SP/DC/JT column straight onto the asset name with no space, and glues the previous row's footer onto the front of that: "...FIlINg STATuS: NewJTAltria group, Inc." is JT + Altria. Measured on 96 refetched filings, 1,446 rows: `(?<![A-Za-z0-9])` false-rejects 179 real codes, `(?<![A-Z0-9])` false-rejects 66, `(?=[A-Z][a-z])` false-rejects 2,080 because the asset is often ALL CAPS, and `(?:SP|DC|JT)(?=[A-Z]{1,3}[ (\[])` kills AT&T, JP Morgan and TJX. What works is two narrow guards: reject when the next character is / , . - ) or ', which no asset name starts with, and a named list matched by CONTAINMENT for brands that carry a code inside them — SPDR, SPX, SPY, CRISPR, UNSP, SPAC. That fixed 104 rows with zero false rejects. OWNER_RAW now lands beside OWNER on every row so the next collision is a query away, not a refetch of 2,633 PDFs.
2026-09-07 — a House PTR amount that ends in a bare dash is NOT recoverable from the next line. The upper bound is dropped by pypdf outright: the raw line reads "$15,001 - g fedcFil...", footer glued straight onto the dash. Widening the next-line rescue from one line to three recovered exactly 1 of 72. The fix is the FORM's own bracket ladder — $15,001 has one legal top and it is $50,000 — which closed all 72. Never treat a dangling bound as a filer choice; the House form offers fixed brackets only.
2026-09-07 — stripping the House PTR form footer was being done BY ACCIDENT. A bogus owner-code hit inside "SPDR" or "UNSP" chopped the asset block, and the footer happened to sit in front of the chop. Fixing the owner regex removed that accident and left "g fedcFIlINg STATuS: New" on the front of 2,794 assets. It now gets stripped on purpose. Second trap inside that: "STATUS:\s*\w+" is wrong, because there is no space after the value — \w+ matched "NewAmeresco" and landed ", Inc." as the asset. Spell the value out: (?:New|Amended).
2026-09-07 — do not try to cut the account name that trails "SUBHOLDING OF:" or "DESCRIPTION:" with a lowercase-to-uppercase seam. It looks safe and it is not: on 96 filings it cut 34 real company names — PayPal to "Pal", SiteOne to "One", AdaptHealth to "Health", Taiwan Semiconductor Manufacturing to "Manufacturing". Roughly 6 rows keep an account-name prefix instead. Visibly ugly beats silently wrong.
2026-09-07 — gen_mart_models.py picks try_to_double() off the COLUMN NAME, so any column carrying SCORE / POPULATION / RATIO / TEXT gets a numeric cast whether or not it holds numbers. Three live models shipped it on text columns and the mart column came out 100% NULL while still advertising itself as populated. HPSA_PROVIDER_RATIO_GOAL holds "3500:1" and HPSA_FORMAL_RATIO holds "3809:1" — ratios, never doubles. Measured before changing anything: 7 columns parsed 0% as numbers and lost the cast, 9 parsed 100% and kept it. Check any generated mart column against its landing values before trusting its type.
2026-09-07 — build_marts_python_door.py now READS dbt_project.yml. Until today it imported no YAML parser at all, so +enabled: false and the marts.politics pre-hook did not exist as far as it was concerned. Three gates, all checked before the connection opens: a disabled model is a hard stop with no override; a marts/politics/ model needs --allow-politics-rebuild, standing in for dbt's --vars allow_politics_rebuild; and tables are created TRANSIENT to match dbt-snowflake. Fail-safe storage on a permanent table cannot be cleared afterwards, only rebuilt away.
2026-09-07 — a row count cannot tell a real small source from a failed scrape, and 376 landing tables hold 50 rows or fewer. What separates them is DENSITY: how many of the table's own columns carry any value, counting the empty string as blank. Swept all 383 small tables 2026-09-07: 347 look real, 13 are thin, 23 are broken. The broken ones share one signature — two or three columns land and every real field is blank. FED_USCOURTS_STATS is 50 rows of TABLE_NUMBER, TITLE and two DOWNLOAD_URL columns: it is the uscourts.gov download PAGE, not the statistics. INTL_BR_DADOS_GOV is dados.gov.br's dataset CATALOGUE, not any dataset. INTL_GFI_TRADE's only populated column holds "GFI Events" and "Careers", the site's navigation menu. FED_FAA_DATA_PORTAL is the portal homepage scraped four times. Loading a catalogue and loading the data behind it are different jobs, and the first one is what usually happened.
2026-09-07 — dbt_project.yml's re-enable notes can cite the wrong table. civil_rights__fed_nara_wra_aad was re-enabled 2026-07-24 on the strength of "NARA_AAD has 554 rows, WRA subset". FED_NARA_AAD does have 554 rows; this model reads FED_NARA_WRA_AAD, which has 36, of which 2 of 12 columns carry anything. SERIES_ID is the constant '623' and NOTES_FIELD holds archive navigation crumbs. Two tables, similar names, one re-enable note. Check the model's own `source()` before trusting a row count in a comment.
2026-09-07 — the Senate EFD PTR mart's SENATOR column is not a person. It holds the literal string 'Senator' on 98 trade rows across four filers and 'Former Senator (Former Senator)' on rows from both Pat Roberts and Marco Rubio, because efdsearch prints the title where the name should be. Keying a name match on that string alone handed all 98 'Senator' rows to John Boozman. The person is FILER_FIRST plus FILER_LAST_CLEAN on POLITICS__FED_SENATE_EFD_FILINGS, joined on FILING_ID. Keyed that way, every one of 15,205 rows in FINANCE__SENATE_TRADES resolves to one of 82 bioguide ids with zero misses and the 'Scott' tie breaks on the first initial. Row count in equals row count out, checked.
2026-09-07 — dbt parse was broken for the whole project from 2026-09-06 until today and nobody noticed because nothing ran dbt. Five marts built through the Python door (IRS527 Schedule A and B, Senate EFD PTR and filings, LDA lobbyist positions) had no source declaration in any yml, and health__fed_cms_hcris was declared twice after the 13-year reload. The door does not need a source block, dbt does. A door-built mart is invisible to dbt until someone writes the yml by hand. Check `dbt parse` after any door build.
2026-09-07 — GOVERNANCE__FED_REVOLVINGDOOR_PROJECT shipped two flags that were false on every row. is_political_appointee tested for the words 'appointee' or 'political appointee' and is_revolving_door tested for 'revolv'; POSITION_TYPE only ever holds 'Senate-confirmed', 'Appointive' or 'nan'. A flag that passes an accepted_values [true,false] test can still be a constant. Replaced with is_senate_confirmed, 190 true of 405. The table is job slots and has no people: H is 'nan' on every real row, so person_name is gone and question 90's answer lives in the LDA covered_position field, not here.
2026-09-07 — FED_IRS_990_EFILE_INDEX.RETURN_ID is NOT unique (5,544,626 rows, 4,601,737 distinct); OBJECT_ID is (5,544,626 distinct). Join the XML-derived tables on OBJECT_ID only.
2026-09-07 — the IRS hosts 990 XML for object-id years 2019+ only; the old s3 irs-form-990 bucket is 404 and ProPublica's download-xml is bot-walled. 7,847 hospital returns (2016-2018 ids) plus 1,306 with 2022 ids sit in the index with no fetchable file. Tax years before 2017 are absent from FED_IRS_990_OFFICER_PAY.
2026-09-07 — 2020_TEOS_XML_CT1.zip and every 2025/2026 monthly zip use Deflate64 (zip method 9); Python zlib/zipfile refuses every member. pip install inflate64 or the whole month silently reads as errors.
2026-09-07 — Form 990 Part VII repeats an executive on every affiliate's return with the same dollars tagged "from related orgs" (Skogsbergh 5 rows in 2024, Dean 3 a year). Sum or rank rows in HEALTH__HOSPITAL_OFFICER_PAY and one person counts five times; group by person and tax year, take max. Group returns put a whole system's officer pay on one PERSON_NAME line ('Sanford Group Return', $68M): filter PERSON_NAME ilike '%group return%'.
- 2026-09-07 — 990 Part VII has pointer lines. A person can appear twice on one return; the second line's title reads "SEE SCH J, PART III" and its dollars restate a Schedule J payout, not a second job. Krabbenhoft's $44.4M is that line; his pay line says $5.1M. 239 person-returns carry one. HEALTH__HOSPITAL_OFFICER_PAY carries is_schedule_j_pointer; rank with it false. Group returns are 61 rows, flag is_group_return.
2026-09-07 — EDUCATION schema holds non-education tables: CFTC futures positioning, Federal Reserve interest rates and flow-of-funds, Google political ad spend, Senate lobbying filings. Schema name is not a content guarantee; check the table, not the folder.
2026-09-07 — IMMIGRATION__FED_EOIR_CASE_DATA landed with one column (CASE_TYPE) against 12,631,225 rows, same count as the working IMMIGRATION__FED_EOIR_CASES. A broken parallel load, not a second dataset — use FED_EOIR_CASES.
2026-09-07 — CORPORATE_REGISTRY__UK_COMPANIES_HOUSE_PSC stopped mid-load per its own yml note, ~7M of an expected 10M+ rows. Any count or coverage claim off it today is a floor.
2026-09-07 — schema _RESTORE_20260907, 11 tables, is a backup snapshot from a database restore operation, not original content. Don't cite it as a live source.
2026-09-07 — TRANSPORT__FED_FAA_ADIP_PRIVATE_AIRPORTS loaded with mangled headers: one column is a full sentence, the rest are UNNAMED_1 through UNNAMED_5. Needs a re-load with the real header row before it's usable.
