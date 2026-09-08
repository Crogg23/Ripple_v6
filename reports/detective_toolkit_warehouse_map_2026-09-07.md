# Detective toolkit — plain-words version, one chain each

Same 52 ideas as before. This time, each one walks the chain:
what you'd check, what a hit means, what a miss means.
One concrete example per idea, against real tables in the warehouse
(`reports/warehouse_topo_map_2026-09-05.md`).

---

## Math laws

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

---

## Forensic tricks

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

---

## Cheap tells

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

---

## Network science

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

---

## Stats of fraud

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
- This one has no hit/miss — it's the question you ask once a flag shows up elsewhere

---

## Anomaly hunting

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

---

## Physics and biology analogies

**Entropy measure** — real randomness looks messy, not this clean
- Check: entropy of a self-reported facility's emissions sequence
- Hit: high entropy, like real measurement noise
- Miss: low entropy, oddly smooth — numbers may have been smoothed or invented

**Diffusion/spread rate** — how fast a pattern moves through a network
- Check: how fast a prescribing pattern spreads across providers who share a rep
- This tells you speed, not right or wrong — fast spread with no clinical driver is the flag

**Herding/flocking** — many actors move together with no stated coordination
- Check: multiple committees moving money the same week
- Miss: found — coordinated behavior nobody officially coordinated

---

## Game theory

**Nash tell** — a move that only makes sense with information nobody admits having
- Check: a bid that only makes sense if the bidder knew a competitor would drop out
- Miss: found — someone had information they shouldn't have

**Signaling** — a small early move announces a bigger one coming
- Check: a small early contribution followed by a much larger bundled one
- This one's a pattern to watch, not a binary flag — small-then-big is the shape

---

## Text and language

**Stylometry** — the same writer shows up under different names
- Check: boilerplate phrasing across differently-named FEC committee filings
- Miss: matching phrasing — same drafter behind "unrelated" filers

**N-gram fingerprint** — a repeated phrase links unrelated records
- Check: a repeated boilerplate clause across unrelated corporate filing purposes
- Miss: found — a shared template, meaning a shared source or preparer

**Levenshtein distance** — names one typo apart might be the same entity
- Check: donor names differing by one character across records
- Miss: found — likely one person, split into two records by a typo

---

## Time series

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

---

## Geospatial

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

---

## Causal and bias traps

**Survivorship bias** — you're only seeing what's still around
- Check: are we only seeing UK companies still active, not the dissolved ones
- This one's a warning, not a finding — always ask what got dropped before counting

**Simpson's paradox** — a trend flips when you split the group
- Check: does a lending-denial trend reverse when split by lender size
- Miss: it flips — the aggregate number was hiding the real story

**Regression to the mean** — an extreme value drifts back, that's not a trend
- Check: an extreme contribution spike, does it settle next cycle
- Hit: it settles — was noise, not a trend, don't chase it
- Miss: it doesn't settle — now it might be real

**Confounding variable** — a third thing is driving both sides of a link
- Check: is something else driving both contribution timing and contract timing
- This one's a discipline, not a query — never call two correlated things "connected" until this is ruled out

---

## Epidemiology

**Contact tracing logic** — who touched whom, in what order
- Check: order of committee-to-committee transfers, treated like a contact chain
- Use: traces how money or influence actually moved, step by step

**R-naught style spread** — is one actor's pattern replicating outward
- Check: is one donor's giving style showing up in new committees over time
- Miss: yes, replicating — something is spreading beyond one actor's own choices

---

## Info theory

**Compressibility test** — data that's too repetitive compresses too well
- Check: does a self-reported dataset compress far more than real-world noise should allow
- Miss: compresses unusually well — may be synthetic or copy-pasted, not measured

**Mutual information** — two columns share more signal than makes sense
- Check: does contract award size predict a firm's lobbying spend, same firm
- Miss: strong shared signal — the two aren't independent, worth naming the link

---

52 ideas, one chain each, all grounded in tables that exist today
in `LIBRARY_MARTS` and `LIBRARY_RAW.LANDING`.
