# The Ripple Manual

*Every nook and cranny of how this thing actually works, and why it's built that way — written to be read like you're discovering it, not being lectured at. Numbers pulled live from the warehouse on 2026-07-30; anything that looked stale against a hand-typed doc is called out by name, not smoothed over.*

*Source material for a future presentation, not the presentation itself — this is the "car manual," not the brochure. Two shorter companion pieces already exist for a lighter read: `docs/RIPPLE_FOR_EVERYONE.md` and `docs/ripple_pitch_deck.md`.*

---

### Table of contents

0. [The hook — a dataset nobody's touched yet](#0-the-hook)
1. [SCOUT — casing every joint before you touch anything](#1-scout)
2. [COLLECT — six stops, and the machine won't move without a "go"](#2-collect)
3. [CONNECT — only a real government ID gets to draw a line](#3-connect)
4. [DETECT — turning a connection into a lead worth a human's time](#4-detect)
5. [THE HONESTY GATE — how a lead earns the right to be called true](#5-gate)
6. [THE READING ROOM — the human front door](#6-reading-room)
7. [THE PLUMBING — loadkit and infra, the seatbelts (and the ones not buckled)](#7-plumbing)
8. [THE POLITICS DOMAIN — the same lens, pointed at Congress](#8-politics)
9. [THE HONEST CURRENT STATE — is this production-grade?](#9-honest-state)
10. [The one-sentence version](#10-close)

---

## 0. The hook — a dataset nobody's touched yet {#0-the-hook}

Somewhere in a catalog of 338,520 public datasets sits New York State's *"Database of Economic Incentives."* Nobody at Ripple has ever downloaded a single row of it. And yet the platform can already tell you it's worth pulling before almost anything else in the catalog — because it looked at the *column names* (`EIN`, `ZIP`, `ADDRESS`, `NAME`) and recognized one of them as a real, unfakeable government tax ID.

That's the whole shape of Ripple, in miniature, before a single byte of real data has moved:

1. **Look at everything, the same way, before you touch any of it.** Not just the datasets that seem interesting — all of them.
2. **Figure out what's actually worth pulling, cheaply, before you spend the bandwidth to pull it.**
3. **When you do connect two things, connect them on something that can't be faked** — a tax ID, a medical license number, a ship's hull number — never a guess.

Everything below is one of those three ideas, built out into real, running machinery. Four verbs do the whole job: **SCOUT → COLLECT → CONNECT → DETECT.** Two more layers sit on top to keep the whole thing honest: **the honesty gate** (nothing gets called true without a human saying so) and **the honest current state** (this document's own limitations chapter — the machine is not finished, and it says so about itself).

---

## 1. SCOUT — casing every joint before you touch anything {#1-scout}

**portal_recon/** is the reconnaissance stage. Before Ripple lands a single row of real data, it wants to know: what data even *exists*, and which of it is worth chasing? It answers that in three waves, and every single step of all three is deliberately **count-only** — it asks a portal "how big are you and what shape is your data," never "give me the data."

**Wave 1 — fingerprinting.** For each of 181 known open-data portals (city, state, national, meta-catalog sites), the scout sends up to six tiny probes — "how many datasets do you have, limit=0" — to figure out which platform runs the site (Socrata, CKAN, OpenDataSoft, ArcGIS, and a couple of others). Every read is capped at 64 kilobytes, so even a portal that would happily hand over a multi-megabyte catalog file can't accidentally get slurped in whole. If nothing confirms a platform, the portal stays labeled `UNKNOWN` — the scout never *guesses* a platform from the website's name alone.

**Wave 1.5 — a second pass on the confused ones.** Portals that came back unknown get three more tries: follow a redirect if the URL moved, try common subpaths, or — as a last, explicitly softer resort — fetch the homepage and look for phrases like "powered by CKAN" in the raw HTML.

**Wave 2 — the actual listing.** For every portal whose platform is now known, the scout pages through that platform's real dataset-listing API and pulls one metadata record per dataset — title, column names, row count, last-updated date. Still nothing downloaded, still nothing landed. Politeness is engineered in, not a courtesy: a quarter-second delay between requests to the same host, hard per-portal caps (25,000 datasets, 300 pages, five minutes), and any concurrency only ever runs *across* different portals, never hammering one host twice at once. This is CLAUDE.md's "recon on power — a census, not a subpoena" made completely literal in code: you can survey the whole country's open-data landscape without ever taking anything meaningful from any one site.

That wave, run in June, came back with **338,520 datasets across 96 live portals** — the biggest single hauls were open.canada.ca, data.gov.au, data.gov.uk, and Ireland's national portal.

**Wave 3 — tagging.** Now, and only now, does the scout decide which of those 338,520 datasets are actually worth chasing. Every dataset's column names get split apart (`employerEin` → `employer`, `ein`) and matched, whole-word only, against a dictionary of real government ID names. A match gets sorted into one of four honesty tiers:

- **STEEL** — a real hard ID: a tax EIN, a doctor's NPI number, a ship's IMO hull number. Precise, safe to join on.
- **STRONG** — a real but softer domain code, like an industry classification.
- **GEO** — a location field: ZIP code, lat/lon. Common, but coarse — plenty of coincidental matches possible.
- **PROBABILISTIC** — just a name or address column. A hint, never a proof.

This is where the discipline gets interesting: the scout is built to be *wrong in the safe direction*. Its own code states the rule outright — **"a false STEEL tag is worse than no tag."** A "DOI" column looked, on paper, like it might be a hard identifier worth trusting — until an audit found every real-world hit was actually a "Date Of Injury" field or an unrelated demographic index. Zero real DOIs. So DOI was pulled from the trusted list entirely, on purpose, rather than left in as an occasional false positive. Two other genuinely real hard IDs (NDC drug codes, CUSIP securities codes) are *also* deliberately kept out of the top tier — known-real, just not trusted enough yet.

**Where it stands today (live, 2026-07-30):** of the 338,520 catalogued datasets, columns are visible for only 78,651 of them (23% — portals don't all expose schema up front). Of those, 185 datasets carry a STEEL-tier key, 563 STRONG, 47,438 GEO, 9,834 PROBABILISTIC — and 145 datasets carry *both* a GEO key and a STEEL key at once, which the internal brief calls "cross-joinable gold." Only about **1,563 of the 338,520 catalogued datasets (roughly 0.46%) have actually been pulled into the Library so far.** The other 99.5% are known about, sight unseen, ranked and waiting.

**Honestly:** the harvester code that produced the June numbers currently lives on an unmerged git branch, not on the main working copy — the *artifact* (the 338,520-row table) survived, the tool that made it would need to be pulled back from that branch to run again. The master catalog hasn't been refreshed since that June run. And a real, dated bug was caught and fixed the same day this research ran: three different parts of the codebase (the scout's tagger, the connector's key list, and a separate re-tiering script) had quietly drifted out of sync on *what counts as a valid key*, so some datasets were advertised as STEEL-tier while the actual connection engine would have thrown an error trying to use them. Fixed, and now guarded by a test that checks the three lists stay in lockstep.

---

## 2. COLLECT — six stops, and the machine won't move without a "go" {#2-collect}

**library-onboarding/** is where a dataset actually enters the warehouse. It's a command-line tool (`onboard.py`) that walks one data source through six steps, and — this is the part worth sitting with — it **stops and waits for a human to type something** at every single one. Not a metaphorical checkpoint. A literal blocking prompt reading real keyboard input: `-> go / edit [feedback] / skip / abort`.

1. **Recon** — fetches the source's documentation page, hands the readable text to Claude, and gets back a structured profile: what fields does it have, what's the access method, what join keys might it carry. If the page turns out to be a bot-wall or an empty JavaScript shell, the tool notices (not guesses) and automatically falls back to a real, invisible headless browser to actually read it.
2. **Script** — Claude writes the actual fetch code. It's compiled immediately, so a syntax error shows up right here, not three steps later — and the human reads the generated code, syntax-highlighted, before it ever runs.
3. **Load** — the script actually runs, the data lands in the warehouse, and every row gets stamped with when it was pulled and a checksum of the source file.
4. **dbt models** — Claude writes the cleanup layer (rename columns, cast types, dedupe), reading the *actual* landed column names off the warehouse, not recon's earlier guess — because those two can disagree, and did, in a documented case where a source's real column name (`PROVIDER_CCN`) didn't match what recon had guessed (`PROVIDER_NUMBER`).
5. **Registry** — the source gets formally catalogued.
6. **Connect** — a best-effort attempt to wire the freshly landed table into the cross-dataset connection graph immediately.

**Why stop six separate times instead of just running it end to end?** Because "it ran without an error" and "it actually worked" are not the same claim, and this codebase has the receipts to prove it. The clearest one: a source called FED_FJC_IDB once landed **4.1 million rows**, logged itself as `success`, and rode into the catalog as a real, modeled dataset — while being **100% empty in every single column**, because the parser had silently collapsed everything to blank on the way in. That failure is the direct reason a "density gate" now exists: after every load, the tool measures how much of the data is actually filled in, and if it's under 1% populated (or the whole thing looks like a scraped web page pretending to be a spreadsheet), the load gets automatically demoted from `success` to `empty` before it can poison the catalog.

Another real, separate failure it's built to catch: **the OP-2022 load**, one of the Open Payments files, actually landed **13.25 million real rows** — the data is genuinely there — but its own run log insists it errored with zero rows, because of an "I/O operation on closed file" error that fired *after* the rows had already written. Anything trusting the log instead of the actual table would think this dataset doesn't exist. Confirmed live this session: the 13.25M rows are real; the log still says error. That's a live example of exactly why every number in this document was pulled from a fresh query, not from a document.

**Honestly, about the collector's own numbers:** its batch-run log currently shows 684 sources marked "failed" out of 774 attempted. Read literally, that sounds bad. Read closely, it isn't what it looks like: 226 of those aren't failures at all — they were deliberately routed to a different, bulk-loading pipeline instead. And **385 of the remaining 458 share one identical root cause**: a single Anthropic API billing cutoff that hit mid-batch and cascaded across an entire wave of sources, not 385 separate engineering problems. Strip both of those out and the real, distinct per-source failure count is closer to 70–75 — mostly 404s, unparseable pages, and one schema-drift case. The honest number the log *should* surface (and currently doesn't distinguish) is "how many sources are actually broken" versus "how many got caught in one outage."

The headless-browser path (for sites that hide their data behind JavaScript or a bot wall) is proven to work — a standalone test script shows it clearing a real Cloudflare challenge on a UK case-law site and reading 44 real judgment records that the plain, non-browser version couldn't see at all. But that proof runs outside the full six-step pipeline; there's no fully confirmed case *this session* of that exact path landing real data all the way through a completed, checkpoint-by-checkpoint run.

---

## 3. CONNECT — only a real government ID gets to draw a line {#3-connect}

This is the part that turns a pile of separately-collected datasets into an actual map. **connect/** looks across every landed table and asks: is the same real person, company, or ship showing up in more than one place?

**The lesson everything here is built around, told as a true story:** an early version of this matching logic normalized ID codes by *stripping* leading zeros — so `'015009'` and `'15009'` looked identical. That single decision once matched an Alabama nursing home to a Puerto Rico drug store, because their CMS facility codes happened to collapse to the same number once the zeros were gone. Nobody meant to accuse an Alabama nursing home of being a Puerto Rico drug store. It just happened, mechanically, because of one bad normalization rule. The fix — and it's the fix used everywhere in this codebase today — is to **pad, never strip.** Every ID gets normalized to its correct fixed width instead of having its "meaningless" leading zeros trimmed away, because sometimes they weren't meaningless at all.

From there, the real matching mechanism runs in four steps:

1. **Tag** the column (reusing the exact same STEEL/STRONG/GEO/PROBABILISTIC tiering the scout built).
2. **Normalize** the values so an honest comparison is even possible (pad, not strip).
3. **Actually join** the two tables on that normalized value and count real matches — never trust "both tables have an EIN-shaped column" as proof of anything by itself.
4. **Score the match 0 to 1**, and here's the clever part: the engine calculates, mathematically, how many matches *pure chance* would produce given how big that ID's possible-value space is (a 10-digit medical ID has ten billion possible values; a 6-digit facility code only a million). If the real match count isn't comfortably — at least 5 times — above what coincidence would produce, the match gets thrown out as a fluke, not drawn as a connection. Two classification-code families (NAICS and SIC industry codes) are hard-excluded from ever scoring as a connection at all, because matching on "same industry" was never actually matching on "same entity" — the code's own comment says this vocabulary noise made up roughly 70% of an earlier, inflated version of the connection graph.

**The single most important design decision in this whole platform** sits right here: a match on a real government ID (padded, verified, counted) is treated as **fact** — guaranteed the same real-world thing, no human review needed to state it. A match on just a name is treated as a **lead** — worth a human's attention, never stated as proven. The "entity spine" (the platform's master who's-who list) is built by literally grouping records by their normalized hard ID — which means, by construction, it can never accidentally merge two different people. The fuzzy name-matching frontier that sits just outside it is measured, honestly, at its best setting, to be wrong about **1 match in 8** (0.876 precision) and to only catch about **half** of the true matches that exist (0.46 recall) — on one tested population (health providers) so far. That fuzzy layer never touches the spine. It only ever writes to a separate review-only table, and turning one of its guesses into a stated fact is a deliberate human decision, every time.

There's also a real, *acknowledged* tension baked in here, not hidden: a safety cap called `FANOUT_MAX` throws out any ID that maps to more than 40 things on the other side of an indirect ("bridge") connection, because that's usually a junk placeholder value exploding into thousands of fake links. But it's a blunt cutoff — it also throws out *real* high-volume links, like a large hospital's full staff roster. Chris has this flagged, openly, as an unresolved tradeoff, not a solved problem.

**The best story in this whole document, and it happened this week:** live, right now, the connection graph has **610 confirmed edges.** A document generated just three days earlier claimed **11,197.** That's not a bug and it's not decay — it's the honesty engine catching itself and cutting its own headline number by 94.5%, on purpose, because two tightenings landed: the industry-code exclusion (most of that old graph really was NAICS/SIC noise, not real links) and a decision to exclude an entire, still-unresolved category of half-finished portal data from scoring at all until someone decides whether to finish loading it or prune it. A platform whose entire purpose is catching *other* institutions inflating their numbers just watched its own flagship metric and cut it by 94.5% rather than let a bigger, wrong number stand. That's not a talking point — it's a live, dated, verifiable example of the thing this whole platform claims to be about.

**Real scale, right now:** 22,623,285 entities on the spine (up 39% from three days ago, from a same-day wiring pass that added 35 new sources and 6 new hard-ID types). Of those, 32.4% are corroborated by two or more independent government datasets, not resting on one source's say-so. The live graph itself: 89 STEEL-tier direct edges, 270 GEO, 180 corroborated-by-name-pinned-to-place, 70 bridged, 1 STRONG.

**Honestly:** the platform's separate honesty-grading engine (Chapter 5 and 9) claims to mirror this exact set of trusted hard-ID key types — and, checked live, it's currently six keys behind what connect/ actually indexes on. A real, if narrow, documentation-drift risk between two systems that are supposed to agree.

---

## 4. DETECT — turning a connection into a lead worth a human's time {#4-detect}

Once the graph exists, something has to actually look at it and ask "does anything here look wrong?" That's a **detector** — and there are two genuinely different kinds running today.

**Seven detectors are simple, declarative joins.** Each one names a "flag" list (a ban list, a sanctions list, a debarment list) and an "active" list (an ongoing-activity roster: payments, contracts, broadcasts), and joins them on a shared hard ID. `banned_but_paid`, for instance, joins the federal healthcare-exclusion list to industry payment records on the provider's medical license number. If someone's on the ban list *and* shows up getting paid, that's a lead. No AI writes the match — it's one SQL join per detector, computed at build time.

**The eighth is architecturally different, and new.** `osha_cohort_outlier_2024` isn't a ban-list join at all — there's no second "flag" dataset. It scores every 2024 OSHA workplace-safety filer against its own peer group (same industry code, same size band) on one real safety statistic: the injury rate OSHA itself already requires every employer to compute. Flag anyone running at 2x or worse than their own peer group's rate, with at least 5 real injury cases behind the number (so a tiny outlier from small-sample noise doesn't get flagged). Out of 355,360 filings, 148,940 survived every honesty filter, and **16,215 establishments cleared the outlier bar** — that one detector alone now makes up **94% of everything in the review queue.** The single worst outlier found: a hospital running at **62 times** its own peer cohort's injury rate.

Every detector's output — whichever kind — lands in the same place and flows through the same review machinery (Chapter 5), specifically so a brand-new statistical detector doesn't get to invent its own, less-scrutinized path to becoming a public claim.

**Honestly, right now, two real bugs are shipping to whoever reviews this queue today.** First: the display layer that recomputes each lead's real numbers still says a related federal debarment table "holds exactly 1,000 rows" — live count today is 9,000. Second, and more serious: it tells a reviewer that a key evidence table behind the `banned_but_operating` detector "was dropped from the warehouse... evidence frozen, cannot be re-run" — but a live check shows that table is back, with 2.26 million rows, restored days ago, and other parts of the codebase are already querying it again. Ten currently-active leads are shipping with a caveat telling a human the underlying proof is gone, when it isn't. Third, smaller: the new OSHA detector's 16,215 leads are all missing their name/location display fields in the review mart — not because the data's missing, but because that detector's name was never added to the mart's display logic when it was wired in.

---

## 5. THE HONESTY GATE — how a lead earns the right to be called true {#5-gate}

A detector finding something is not the same as Ripple *saying* something. This is the layer that keeps those two separate, and it's worth walking end to end, because it's mechanically stronger than it sounds when summarized as "human sign-off required."

A lead sits in the queue. A human — in the browsing app or a terminal tool — reviews it and presses Confirm, Reject, or Needs-work. That single click writes one row to a decisions log. **Here's the part that's enforced by the database itself, not just by app code:** the login the review tool writes through has, at the account level, only two permissions on that table — `INSERT` and `SELECT`. No `UPDATE`. No `DELETE`. Even if the app had a bug, the underlying Snowflake role *physically cannot* edit or erase a decision once it's written. That's not a promise in the code comments; it's a permission that doesn't exist to be abused.

And Confirm is deliberately **not** the same as publish. A single click used to be enough to make a claim public; as of a 2026-07-20 change, it's a private nomination only. The *only* code path anywhere in this repository that can write the word "published" is one standalone script, run manually, that (a) refuses to run unless the lead's latest verdict is already "confirmed," (b) previews by default and only writes with an explicit `--apply` flag, and (c) requires a human to type an actual reason in plain text. That word — "published" — is deliberately kept out of the list of values the everyday review tool is even allowed to write, so no accidental click, anywhere, can ever make something public.

**The honest number today: zero.** Real, non-test rows in the decisions log: zero. The only two rows in that table at all are smoke tests — one proving the write works, one proving a delete attempt correctly fails. **Every one of the 17,255+ leads currently sitting in the queue is unreviewed.** That's not a flaw in the mechanism — the mechanism is proven to work end to end — it's just an honest snapshot of where the project actually is: the gate is built and tested, and nothing real has been pushed through it yet.

There's a second, more sobering honesty story worth including here rather than hiding: this platform has a standing rule that an AI agent is never allowed to close a tracked defect — only a human can. Checked live, one blocker-severity security item (an overly powerful login credential that had leaked) *was* marked closed, and the identity that closed it was an automation/tooling account, not a person. The underlying fix looks real — the specific leaked credential is confirmed gone from the account — but the process broke: a rule meant to guarantee a human eyeballs every closure was itself quietly bypassed once, and the platform's own automated recheck can't catch a *closed* defect being wrong, because it only ever re-examines things still marked open. The good news sitting right next to that: two properly narrow-scoped replacement credentials already exist and are active — the fix isn't "hasn't started," it's "isn't finished yet."

One more current, plain fact: the browsing app's review buttons can't even write right now in this environment, because the specific credential they need isn't present in this session's configuration. And the review app itself, as currently committed, points its main queue query at a table name that doesn't exist in the warehouse at all (a copy-paste mismatch from the day it was written) — meaning, launched today, it would fail before showing a single lead. Both are real, both are fixable, neither is currently fixed.

---

## 6. THE READING ROOM — the human front door {#6-reading-room}

**serve/** is the one piece meant for someone who doesn't want to write SQL. It's a small local app with four real views: search, an entity dossier, a source page, and the connection graph — plus a fifth, a "workbench" where you can type any read-only query and get a chart back, with the exact code that drew it shown right next to it, so it's a learning tool instead of a black box.

Type a name or paste a real ID — it accepts five ID types today (a subset; more on that below) — and it searches the entity spine directly. Try it with a real one: **NPI 1164450573** resolves to a real provider in Oklahoma City, appearing across nine different federal datasets at once, including the exclusion list *and* hundreds of payment and prescribing records from the years after. That's the mission's core "receipt" idea, rendered on one screen, findable by a plain-text name search a journalist with zero SQL could type themselves.

Every row shown carries a "provenance receipt" — the exact run ID, file checksum, and source URL it came from, so a skeptic can go re-download the original government file and check the platform's work directly. Every dataset carries a freshness badge, and the badges are built to fail honestly: if the system genuinely doesn't know how fresh something is, it shows a gray "unverified" dot rather than guessing green. The "card catalog" — a plain-English index of every browsable dataset — isn't a metaphor; it's a literal, queryable database view with one row per dataset. And the Workbench specifically blocks a curious analyst from directly reading the platform's *unreviewed* claim tables (the same LEADS table Chapter 4 covers) — redirecting instead to the reviewed, gated version. That's the "no unreviewed accusation gets stated as true" rule, enforced in code at the query layer, not just written down as policy.

**Honestly:** a real bug sits in the dossier page's "facility affiliations" section — a variable name mismatch means it will error every time anyone opens that section today. The five hard-ID types the search box accepts cover under half the entity spine by count; the other 55% (tax IDs, company legal-entity IDs, water-system IDs, and several others) are currently only reachable by typing a name. And the project's own written policy still names a different, more polished front end (`evidence.dev`) as the "real" surface with this app as a "legacy fallback" — but that other app was deleted from the codebase entirely one day before this research ran. In practice, today, this Streamlit app *is* the Reading Room, whatever the policy document says.

---

## 7. THE PLUMBING — loadkit and infra, the seatbelts (and the ones not buckled) {#7-plumbing}

Every loader in this codebase is *supposed* to wear the same set of seatbelts. **loadkit/** is where they live:

- **Pre-flight checks** — before a long load starts, it verifies the login credential will actually outlive the job, and that there's still budget headroom in the account. Why bother: if the credential dies *mid*-load, the code path that would log "this failed" also needs a live connection to run — so the crash goes completely silent, and the next run just quietly overwrites a half-built table with no trace anything went wrong.
- **Atomic staging-swap** — every load writes to a side table first, and only flips it into place as the "real" table in one instant, all-or-nothing move, after the whole load succeeds. A crash mid-load leaves a harmless side table sitting off to the side; the live table is never touched.
- **Durable checkpoints** — a save file for a long crawl, so an interrupted multi-day pull resumes where it left off instead of starting over.
- **A quarantining parser**, built for one very concrete failure mode: campaign-finance files are pipe-delimited with no header row, and one badly formatted embedded pipe character used to get silently padded or truncated into the wrong column — meaning a dollar figure could quietly shift. Now, a row like that gets set aside in a reject pile instead, and the load stops if too many rows land there.
- **Reconciliation referees** — before some loads are allowed to finish, their own totals are checked, to the exact penny, against an outside published number (the government's own totals). Integer-cent math on purpose, so floating-point rounding can't fake a match.

**A story that shows exactly why the windowing logic exists:** the Senate's lobbying-disclosure API doesn't error when you page past its real limit — it just silently stops returning rows around record 2,500, no matter how the request is shaped, while the load *looks* completely healthy: zero errors, rows landing normally. The only way to catch that is to ask the API's own reported total count and refuse to mark a slice of data "done" unless the math actually adds up — which is exactly what this codebase's window-planning logic does, recursively splitting a too-big request into smaller and smaller slices until each one is provably complete.

The warehouse's own plumbing — the tables and views everything else depends on — is captured as code too (`infra/`), specifically because, as the project's own documentation states plainly, **"a predecessor infra database was already lost to a DROP once."** This isn't hypothetical caution; it's a repeat-incident-prevention measure.

**Honestly:** the checkpoint and windowing modules described above are fully built and fully unit-tested — and, checked live, **currently unused by any real loader.** Two real, currently-shipping loaders (the Senate lobbying data and a shared utility used by several federal loaders) bypass this safety layer entirely and write straight to live tables instead. And in maybe the tidiest possible demonstration of the whole "check your own homework" ethos: running the credential-tracking tool live, mid-session, produced an honest failure — the hand-maintained document listing the login token's expiration date said one date; the token itself, decoded directly, said a different one, a full month later. The tool caught its own documentation being wrong, in real time, on request.

---

## 8. THE POLITICS DOMAIN — the same lens, pointed at Congress {#8-politics}

**politics/** is worth its own chapter because it's the clearest existing proof that Ripple's "look at everyone, the same way" idea isn't just healthcare and shipping — it works on political power too. Every sitting member of Congress gets the exact same "box score," computed the same way: an identity chain that runs from their government bio ID, to their voting record, to their FEC campaign-finance filer ID, to every committee they've ever been tied to.

It's real, and it's been checked against the outside world, not just internally: Senator Sanders' full identity chain resolves correctly end to end, from his bio ID through to his real committee name. Senator Warren's 2024 fundraising total matches the FEC's own published number **to the penny.** And there's a genuinely useful honesty lesson baked into how the "bills" numbers are computed: one member sponsored 612 bills in a session and got **zero** enacted — which is exactly why this platform never shows a raw sponsorship count without also showing the enactment rate next to it. A big number alone can be a completely misleading headline.

**Honestly:** this domain has a real, live, currently-unresolved risk. Its canonical numbers are built and verified by hand-written Python — but a *separate*, newer layer of database models also targets the same physical tables, purely so an automated testing tool can run checks on top of them. Nothing except a code comment (*"NEVER build here — this will silently overwrite the audited numbers"*) stops someone from running the platform's normal one-command rebuild and having it quietly overwrite the hand-verified figures with different, unverified ones. No error would fire. The table would just start holding different numbers. Nobody has actually run that command to find out if the comment is the only thing standing in the way — the project's own tracking log lists this one as "never verified."

---

## 9. THE HONEST CURRENT STATE — is this production-grade? {#9-honest-state}

Short answer: **not yet, and here's exactly what's left**, in the same plain terms as everything above.

**The defect ledger.** Every known problem lives as one row in a real database table — severity, status, when it was last actually re-checked. Live right now: **13 open, zero currently blocker-severity.** Three high-severity items (a dead alternate front-end read path, no scoped write credential for one lane, and no automated regression tests against a known-good baseline), seven medium, three low. An automated tool can re-verify any of these and recommend "clear" — but only a human is supposed to actually flip one to closed. That rule was broken once, quietly (Chapter 5), and caught only by this research, not by the platform's own automated check.

**Data-quality test coverage — a real correction.** A previous internal document claimed roughly a third of the newer data sources lack automatic data-quality checks. Checked directly against the actual build system's own record of what's tested: **only 53 of 391 output tables (13.6%) have any automatic check wired at all. 338 (86.4%) have none.** That's more than 2.5 times worse than the number Chris had been working from. It should be corrected going forward, not repeated. Important distinction, because it sounds contradictory otherwise: this is a *different* question from the honesty-grading number below — one asks "is a rule like *this column should never be blank* attached to the table," the other asks "was this table built using only trustworthy government IDs." A table can correctly have zero data-quality tests and still be perfectly well-built.

**The honesty-grading engine** — a completely separate, zero-AI tool that reads the build system's own record of exactly how every output table was constructed, and grades each one `fact` (every join anywhere in its lineage is anchored on a real hard ID — mechanically re-derivable by a stranger), `lead` (touches the human-review layer somewhere upstream), or `unverified` (the tool genuinely can't tell, and refuses to guess in the trusting direction). Right now: **389 of 391 tables grade `fact`. One is `lead` (correctly — it's the review queue itself). One grades `unverified`,** and that one is a known, accepted false positive: a small, 55-row hardcoded reference table the checker's simple pattern-matcher can't parse cleanly, not an actual demoted table.

**Zero findings published, none confirmed.** Restated plainly, one more time, because it's the single most important honest number in this whole document: **zero** human review decisions exist on any of the 17,000-plus leads currently sitting in the queue. The mechanism is real, tested, and enforced at the database level. Nothing has gone through it yet.

**The credential question.** The specific leaked credential named in the project's own operating rules has been confirmed revoked. What's still true: the account's day-to-day working login remains a broad, powerful credential rather than a narrowly scoped one — though two properly scoped replacements already exist and are active, so the remaining work is a cutover, not a build.

Put together: **the safety mechanisms in this platform are real, not aspirational** — they're enforced by actual database permissions and actual tests, not just written down as intentions. But the platform is honest about the fact that most of them haven't been exercised on anything real yet, and the parts of it that check its own health (the defect ledger, a stale policy document, a couple of caveats sitting in the lead queue right now) are themselves running a few steps behind the live system in a few specific, named places. That gap between "the guardrail is real" and "the guardrail has actually been tested by something real yet" is the honest, current state of this project — not spun either direction.

---

## 10. The one-sentence version {#10-close}

Ripple looks at the same public record everyone else can already see, connects it only where the connection is provably real, and refuses — mechanically, not just by promise — to let any of it be called true until a person says so.
