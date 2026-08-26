# RIPPLE STATUS — 2026-08-26 (late) — Mart-generator bug fixed; ready-now backlog closed; the "414" number was wrong

*One screen. Rewritten (never appended) at the end of every session. Sessions read
this at boot and brief Chris in chat — Chris never has to open it.*

**Scoreboard: test suite still clean, unchanged by tonight's extra work** — 5,156
tests, 4,910 pass / 246 warn / **0 error**. Verified twice tonight (before and
after adding 43 new marts) to make sure nothing broke while building on top of
this week's earlier fixes — same numbers both times.

**BROKE: nothing tonight, verified twice. Two standing items, not new:**
- **Senate LDA lobbying loader** (running for days now) — still alive, still on
  2008, still getting rate-limited (normal, not stuck). Check
  `logs/senate_lda_stdout.log` / `logs/senate_lda_checkpoint.json` at boot.
- **GFI trade data still broken** — the real country-by-country table is a
  Tableau Public chart embed (canvas/SVG, not HTML); needs a Tableau-aware
  scrape. Not touched tonight.

## Tonight's work (commits `d4036743`, `c00ddc0a`)

**Chris asked for a plan to finish the whole backlog. First finding: the plan
handed off from earlier tonight was built on a wrong number.**

**1. Found and fixed the real bug behind the "414 stuck sources" plan.**
The batch mart-generator (the tool that builds a finished analytics table on
top of a raw data pull) always wrote a straight copy of raw landing data, even
when a clean, deduped staging model already existed for that source. That's
the exact bug class that caused 8 known duplicate/bad-cast mart pairs earlier
this month. Fixed: the generator now checks for an existing clean staging
model first and builds on top of that instead of raw data, whenever one
exists.

**2. The "414" figure itself didn't hold up.** Checked it against the live
warehouse before building anything on top of it: the real number is **1,567**
sources stuck at that stage, not 414 — nobody had verified the actual count
before handing it off. Worse, checked what the stage actually means in the
code that assigns it (not guessed): it means *only a small preview pull ever
happened*, not "data's here, just missing a mart." Split by how confident that
is: **385 sources hit an exact, deliberate row cap** (unambiguous — need a
real full reload, not a mart). **1,182 are smaller and more scattered** — no
clean cap pattern, need a per-source look to tell "genuinely small and
complete" apart from "broken partial pull." Neither bucket has been reloaded
or fixed yet — this is a sizing finding, not a fix.

**3. Piloted the fixed generator, then ran it to completion on the one
population that's actually ready today** (real, complete data already landed,
just no mart yet — this is a different, much smaller pool than the 1,567
above). Built and verified 43 new marts in two batches (18, then 25),
`dbt build` clean on every one. Spot-checked row counts by hand against the
raw data for several of them — two looked off at first glance, both traced to
real duplicate rows in the raw data being correctly removed, not a bug.
Result: **that backlog is now fully closed** — re-running the generator finds
zero real gaps left, only sources already modeled elsewhere under a different
name (correctly left alone). All 43 sources now show as "modeled" automatically
(that flag is computed from the mart's existence, no manual step needed) and
are ready for the next entity-graph wiring pass whenever that's prioritized.

**One thing surfaced, not fixed:** two of the new marts (a California/general
Prop 65 chemical-list pair) turned out to hold slightly different row counts —
looks like the same real-world list pulled by two separate scrapes under two
different names, not a code bug. Worth a human glance, not urgent.

## YOUR MOVE (Chris)

1. **Drop the old truncated USASpending contracts table** — still open from
   earlier tonight, fully superseded.
   `DROP TABLE LIBRARY_RAW.LANDING.FED_USASPENDING_CONTRACTS_FULL;`
2. **GFI trade data** — needs a dedicated Tableau-scraping session. Not urgent.
3. **The stale politics timeline table** — view instead of table, or something
   else? Real design call, not urgent.
4. **The real 1,567-source backlog** (not 414) is the next real lever for the
   entity graph. Two different jobs live inside it: reloading the 385 with a
   confirmed hard cap, and a human/tool pass to sort the other 1,182. Both are
   bigger than anything done tonight — worth scoping as its own session before
   committing real time or spend to either.
5. **Push tonight's 10 local commits to origin**, whenever you want them off
   this machine — not done automatically, no standing approval for it.

## NEXT

Boot: check the Senate LDA loader is still moving. The ghost
`ICIS_AIR_FACILITIES` spec entry (found last round, still not fixed) is a
quick, bounded fix worth doing early. The real 1,567-source split (item 4
above) is the one open item that could genuinely reshape a future session —
worth a scoping-only pass (no reloads yet) before deciding how big to go.

**Cost note:** tonight's extra work (on top of the ~$10-14 already logged
earlier today) was a handful of small `dbt build` runs plus three full
test-suite passes (~3 min of warehouse compute each) — same small ballpark,
not separately meter-verified this instant.

## Not committed

Nothing — working tree is clean as of this session's close (10 commits ahead
of origin, not pushed). The Senate LDA loader's checkpoint/log files will be
dirty again once it lands more years; that's expected, same as every session
this week.
