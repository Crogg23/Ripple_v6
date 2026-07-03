# Ripple — For The Founder

*An honest, complete walkthrough of your own machine. Written to be understood, not skimmed. Numbers reconciled against repo state on `main`, 2026-06-28 — graph & visual artifacts are dated 2026-06-27, and live lead/catalog counts are last-recorded from the latest run, not re-queried here (see the closing note).*

> **How to read this.** Read straight through — it's the whole machine, picture before jargon. **If you read nothing else, read §8 (the four silent traps + the honest number) and §9 (the real bottleneck + the clock that's ticking).** Those are the two things that bite you in practice.
>
> **Designing the visual layer?** This is the founder's deep version. The standalone creative brief is **[`RIPPLE_DESIGN_BRIEF.md`](RIPPLE_DESIGN_BRIEF.md)** — it carries its own 90-second primer; you don't need this explainer to start.

### Section map

| | |
|---|---|
| §0 the one sentence · §1 the big picture · §2 the four verbs | §3 the assembly line · §4 the pipeline · §5 the self-auditing catalog |
| §6 the moat (fact vs lead) · §7 the detectors | §8 the honest state · §9 the bottleneck · §10 bottom line |

---

## 0. The one sentence

**Ripple turns any public dataset on the internet into clean, connected, queryable data — and then automatically finds the places where two datasets contradict each other in a way that smells like a story.**

Banned doctors still cashing pharma checks. Debarred companies still winning federal contracts. Sanctioned ships still broadcasting their location. That's the product. Everything else is plumbing in service of that.

---

## 1. The big picture — what Ripple actually is

Forget the code for a second. Here's the thing in the world.

Imagine every public dataset is a **dot on a map**. The registry of every U.S. doctor. The federal list of doctors banned from Medicare. A registry of every cargo ship. A list of sanctioned vessels. Today those dots live in separate buildings, in separate formats, owned by separate agencies who never talk to each other.

**Ripple's job is to draw the lines between the dots.**

Not "these two datasets are both about doctors" — anyone can see that. The lines are *specific*: "this exact doctor, by his federal ID number, appears on the national provider registry **and** on the federal banned list." That kind of line — a single drawn connection between two records that should never touch — *is the shape of an investigation.* A journalist would spend three weeks finding one by hand.

### What makes that line trustworthy: the hard ID

The whole thing rests on one idea, so let's earn it before we lean on it.

**A hard ID is a government-issued number that points at exactly one real thing in the world.** A doctor's federal provider number. A ship's hull number. A company's tax ID. When the *same* hard ID shows up in two datasets, it is not a coincidence — by construction, it is the same entity. You can bet your byline on it.

That's the difference between a connection you can bet on and one you still have to check. Hold onto it — it's the spine of everything downstream (the moat, the fact-vs-lead split, the safety guarantee).

Ripple has already drawn **8,503** of that exact registry-meets-banned-list line on the hard ID (`connect/HOWTO.md:32` — NPPES × LEIE on NPI, 100% match — though see §8 trap #4: this is the 2026-06-27 graph figure and predates the all-zero-NPI cleanup, so a rebuild may trim it). Narrow it to the sharpest version — banned doctors who are *also* showing up in pharma-payment data — and you get **773 live leads.** Before your coffee's cold.

> **Three numbers, three different things. Don't conflate them.**
> - **8,503** = banned doctors who exist in the provider registry (a *fact*).
> - **~1,030** = total leads across all six detectors.
> - **773** = how many of those ~1,030 ride the single banned-and-paid edge (a *lead* worth a human's time).
>
> So: **8,503 facts → ~1,030 leads → 773 on one edge.** §6 maps all three magnitudes.

So the honest one-liner for what you've built:

> **A newsroom's secret weapon. Google Maps for public data — where the roads between datasets are the actual product.**

But here's where that metaphor breaks, and it matters: **on Google Maps every road is real and you can drive it on faith. Here, most of the roads are footpaths someone spotted from a distance — not paved highways.** Only the hard-ID connections are roads you can drive without checking. The rest are routes a human still has to walk before we call them real.

The data itself isn't the moat. Anyone can download these files. **The moat is the map of connections** — the private, fact-checked graph of how every dataset links to every other one. Nobody else has assembled it.

One caveat we'll be straight about in §8: only **~101 of these sources carry real, trustworthy data today** — the rest are scouted, sampled, or freshly landed but unverified. Build your mental model on that number now and nothing later will surprise you. **And before you write any SQL against this warehouse, read §8's four data landmines — they bite ad-hoc queries before they bite any chart.**

---

## 2. The four verbs — the spine of the whole system

Everything Ripple does is one of four verbs. Hold these four words and you hold the system:

| Verb | Plain English | Where it lives |
|---|---|---|
| **SCOUT** | Crawl the internet's public data portals, catalog every dataset, tag what kind of ID it carries | `portal_recon/` |
| **COLLECT** | Take one dataset and fully load it into your warehouse — cleanly, with your approval at every step | `library-onboarding/` |
| **CONNECT** | Match real records across datasets, score how confident we are in each match, fire the detectors | `connect/` |
| **EXPLORE** | Turn the findings into maps, entity dossiers, and a gallery of leads | `outputs/` |
| *(REVIEW)* | *The human step.* A person (you) confirms a lead before it's allowed to be called true | `connect review` (CLI only today) |

Read top to bottom, that's the life of a fact: **scouted → collected → connected → explored** — and a lead waits at **review** until a human signs off. That fifth step is greyed because it's the one part a machine never does on its own. **It's also the most important one** — it's the difference between journalism and a rumor mill (§7).

---

## 3. How one dataset becomes data — the 6-checkpoint assembly line

This is the heart of COLLECT, and the part you interact with most:

```
python onboard.py --url https://some-data-source.gov/api
python onboard.py --batch     # run the whole queue
```

Picture an **assembly line with six stations.** Claude is the worker. **You are the quality inspector at every station** — nothing moves on until you say `go` (or `edit [feedback]`, `skip`, `abort`). It's a conversation, not a black box that runs off and does god-knows-what to your warehouse.

| # | Station | What the worker does | What you approve |
|---|---|---|---|
| **1 — RECON** | Reads the source's docs (launches a real browser if the site fights back). Extracts: what is this, who publishes it, what columns, what ID. | "You understood the source." |
| **2 — SCRIPT** | Writes the Python to fetch it — bulk CSV, ZIP, paginated APIs, even scraping. | "Run that code." |
| **3 — LOAD** | Runs it. Fingerprints the bytes, stamps every row with when/where, lands it, logs the run. | "Counts and sample look right." |
| **4 — DBT** | Writes the transformation models — cleans the raw mess into analyst-ready tables, with tests. | "Model it that way." |
| **5 — REGISTRY** | Files the source's "library card" into the catalog so it's findable. | "Catalog it." |
| **6 — CONNECT** | Wires the just-landed table into the connection graph (incremental — no full rebuild). | "Link it in." |

**The one idea to take from this:** the source ID is the linchpin. When RECON decides a source is `fed_usgs_earthquakes`, that single string deterministically names *everything* downstream — landing table `FED_USGS_EARTHQUAKES`, the catalog row, the logs, the dbt models. One name, threaded through the whole system. That's why reruns never make a mess: it fingerprints with a SHA-256 and skips the reload when nothing changed.

---

## 4. The three-layer pipeline — and why every raw column is text

When data first lands it goes into **LIBRARY_RAW**, and **every column is stored as text** — even numbers, even dates. That feels wrong. Why?

**Because the source lies, constantly.** A "date" column has `2024-01-15` in most rows, `N/A` in a few, `01/15/24` in others, blanks in the rest. Tell the warehouse "this is a DATE" at load time and the load explodes the moment it hits junk. So the rule is:

> **Land everything as text — a perfect, dumb mirror of the source. Clean it later, where you can see it.**

Then three layers, each with one job:

```
LIBRARY_RAW (text mirror)  →  STAGING (clean + cast)  →  MARTS (analyst-ready)
   Python loads it             dbt renames, types,        dbt builds wide,
   dbt never touches it        dedups, casts — as views   topic-named final tables
```

If you've done SQL for six years: raw is **bronze**, staging is **silver**, marts are **gold**. Don't transform in bronze — Ripple just enforces it with a naming convention.

**Where it stands on `main`:** 86 dbt models — **42 staging views, 4 intermediate, 40 mart tables** across 21 domains, carrying 770+ data-quality tests (exact on disk this read: 42/4/40, 21 domains, 774 tests).

---

## 5. The catalog that can't lie

A genuinely clever thing you built — it's what makes the library *navigable* instead of a pile of tables.

**The problem:** a source's library card (its registry row) can claim anything. It can say "1 million rows, fully loaded" when the table has 5 rows. Trust the card and your catalog becomes a liar.

**The fix:** the catalog (`LIBRARY_META.REGISTRY.CATALOG`) doesn't trust the card. It's a *view* that looks at the **actual physical tables** and computes a **lifecycle** from reality (`scouted → queued → sampled → landed → modeled`, or `stale` / `empty`).

> **The catalog reports what's on the shelf, not what the card claims is on the shelf.**

The subtle bit is **density** — not "how many rows," but **how full the cells are: how many cells in those rows are real instead of blank.** That distinction is the whole game. The old bug trusted *file-existence alone*, which let a 4.1-million-row table that was **100% blank cells** read as top-tier data. The fix counts populated cells, so a husk gets marked `empty`. The exact threshold (the ~1% density gate) is the trust-chain fix in §8 — read them as one story.

It's also a two-for-one: the registry is both your **to-do list** (sources with a URL but no data) and your **completion ledger** (what's actually done). One table, both jobs.

---

## 6. The connection engine — the actual moat

Everything so far gets you a clean, honest warehouse. Lots of people have that. **This is the part nobody else has.**

The connection engine (`connect/`, ~4,800 lines) draws the lines. The cleverness is in **what counts as a line**, in two flavors you must never confuse:

### Fact vs. Lead — the credibility line

| | What it is | Example | What we're allowed to do |
|---|---|---|---|
| **FACT** | Two records share the same **hard ID** | Same NPI in NPPES and in LEIE → it is the *same doctor*, no question | Publishable. This is steel. |
| **LEAD** | Two records share a **name**, different ID systems | "John Smith" in the contracts database and "John Smith" in the exclusion list — same NPI? No NPI to check. Maybe the same guy, maybe two people. | Human review only. Never auto-merged. |

This is the single most important design decision in the system. **The engine surfaces both, but only auto-trusts facts.** A shared federal ID is proof. A shared name is a hunch. Treating a hunch like proof is how you libel someone — so the system structurally refuses to.

> **Same number = same person = fact. Same name = maybe = lead. Nothing crosses that line on its own.**

And: **organization names never auto-merge.** "Lockheed" vs "Lockheed Martin Corp" vs "LOCKHEED MARTIN" — the engine won't pretend it knows those are the same without a hard ID.

### How it actually matches — three moves, in order

1. **FINGERPRINT** every table — which IDs it carries, how populated each ID column is.
2. **Find real OVERLAPS** — not "both have an NPI column," but the *actual ID values intersect* (this exact doctor is in both).
3. **SCORE** each connection — weighing evidence **in bits**: a rare surname match is worth a lot, a common name almost nothing, a mismatch counts *against*. *(The method is Fellegi-Sunter if you go deeper. The intuition is enough: rare agreement = strong, common agreement = weak, contradiction = negative.)*

### The confidence ladder — the system's signature

Not all lines are equal. The engine ranks every connection by trust. **Trust comes from the strength of the link, not the topic — that's the honest part, and the color IS the credibility.**

| Tier | Plain English | Edges |
|---|---|---|
| **STEEL** | Same hard ID — basically certain | 350 |
| **STRONG** | Same domain ID (NAICS, LEI, etc.) — very likely | 9,396 |
| **BRIDGE** | Joined *through a third dataset's* key — the clever one | 133 |
| **CORROBORATED** | Name **and** place agree | 769 |
| **GEO** | Same location — a hint | 5,633 |
| **PROBABILISTIC** | Same fuzzy name — a hunch | 4,415 |

**BRIDGE is the cleverest tier:** if A links to B by NPI, and B links to C by NAICS, then A *reaches* C through B — one hop, honestly labeled as weaker than a direct join. The transitive trick, made visible.

The whole graph is **20,696 connections** across those six tiers. Three different magnitudes, three different things: 20,696 = the whole graph · 350 STEEL = the hard-ID spine · 773-of-~1,030 leads = the sharpest stories that spine surfaces.

---

## 7. The detectors — where it becomes a story machine

A connection is a line. A **detector** is a rule that says "this *kind* of line is suspicious." These are your story-finders.

Six are firing today, producing **~1,030 leads total:**

| Detector | The smell | Key | Leads |
|---|---|---|---|
| `banned_but_paid` | Doctor on LEIE *(the federal exclusion list — OIG's roster of providers banned from Medicare)* still in pharma-payments data | NPI | **773** |
| `excluded_but_billing` | OIG-excluded provider still appearing in Medicare Part D prescriber data | NPI | 236 |
| `banned_but_operating` | Excluded provider still active at a facility | NPI | 11 |
| `sanctioned_vessel_broadcasting_v2` | OFAC-sanctioned ship still broadcasting its position (all-years) | IMO | 6 |
| `debarred_but_funded` | Debarred company still receiving federal money | UEI | 2 |
| `sanctioned_vessel_broadcasting` | OFAC-sanctioned ship still broadcasting its position | IMO | 2 |

`excluded_but_billing` and a v2 vessel detector have since landed and are now firing (236 and 6 leads). **Adding a new detector is config, not architecture.**

*(Lead counts here are from the 2026-06-28 detector run recorded in the commit log; the **six wired detectors are confirmed in `connect/leads_specs.py`**, but the live `LEADS` table and the visual board both lag this state — re-run `connect leads` and rebuild the graph to make every artifact agree.)*

`leads_overlay.html` renders this as a red-string board, but it was **last built 2026-06-27** — when it showed 4 detectors and **338 of 353 leads on a single edge.** The live detectors have since grown to six (~1,030 leads); **773 of them — still the lion's share — ride that one edge** (LEIE × Open Payments on NPI), so the board needs a re-render to catch up. Either way the point holds: the overwhelming majority of leads ride a SINGLE edge. That narrowness is both the headline and the roadmap (§9).

### The safety rule — a publishing-control system, not just a flag

Every lead defaults to `PUBLISHED = False`. Behind that flag is a real publishing-control system — what makes this journalism-grade:

- An **append-only `DECISIONS` table** logs every verdict (`confirmed` / `rejected` / `retracted` / `stale`) with who and when.
- **Latest verdict per lead wins** — approve a lead and retract it later, or expire a stale one, full audit trail.
- `gate_rows()` drops everything in the suppress set `{rejected, retracted, stale}` before anything ships.

The system never calls a lead true on its own; only a human can. *(There IS a structural auto-confirm path in the code — `auto_ok` — but no current detector sets it, so all ~1,030 leads sit at `PUBLISHED = False` today.)* That human step is the quiet fifth verb, **review**.

---

## 8. The honest state of reality

You asked for the warts. Here they are, straight. **None of this means the system is fake — it's genuinely built and merged to `main`. The gap is between the *headline* and the *trustworthy core*.**

### The trust-chain story — the maturity event

The catalog's lifecycle rule *used to* mark a source fully-modeled if the **files existed** — not if the data was actually there:

> **`FED_FJC_IDB` loaded 4.1 million rows that were 100% blank cells — and the system logged it `success` and showed it as top-tier data.**

That's the nightmare for an investigative tool: confidently presenting nothing as something. Caught and fixed 2026-06-27 with two gates:

- A **density gate** — if fewer than ~1% of the *cells* are populated, the source is marked `empty`, not `success`. **This is the gate that powers the self-auditing catalog from §5.**
- A **trust gate** that swept the catalog and demoted 9 stub tables + 2 husks from fake top-tier status (`modeled` 34 → 25).

**Reframe it as a feature:** your catalog now *self-audits.* It caught itself lying. Rare, and worth saying out loud.

### The number to use externally

- "**638 connected tables**" (or the raw landing-table count) is technically true but misleading.
- The honest number is **~101 sources with real, trustworthy data** — 76 landed + ~25 modeled after demoting the 9 stubs. Lead with this.
- One nuance for your own bookkeeping: the latest session landed ~40 more sources (~4.92M rows) that are **not yet domain-tagged or trust-gated** — they're real bytes but not yet verified. Don't count them in the trustworthy core until they pass the same density/trust gate. The inflated counts were a bug the system now corrects on its own — tell *that* story.

### The four silent traps

**These bite YOU first, not the designer — any ad-hoc query you write at midnight hits them before any chart does.** They don't crash. The data looks perfectly clean and **fails silently** — worse than a crash. (They also constrain what a viz may honestly claim; that's why they're echoed in the standalone design brief.)

**1. Open Payments — beware the bare table.** It lands as two record-disjoint tables: 2024 (15.4M) and 2023 (14.7M). The `banned_but_paid` detector already reads the all-years union (`int_open_payments_all_years`), so the 773 count **does span both years.** The remaining trap: any ad-hoc query against the bare `FED_CMS_OPEN_PAYMENTS` table is 2024-only (~51% of records) — a naive aggregate there silently halves the data.

**2. AIS is a single 24-hour snapshot** (Jan 1, 2024). Every "vessel broadcasting" claim is one day, not a time series. No chart may imply "tracks ships over time" — it can't, yet.

**3. USASpending splits "Lockheed Martin" into 77 child UEIs** (26 parent UEIs, 6 parent-name spellings — even the exact name carries 42 distinct UEIs, $75.0B that won't roll up). Any "top contractor" ranking is a *floor*, not the truth, until parents are normalized.

**4. LEIE's NPI is `0000000000` on ~90% of rows.** This is the one that could libel someone, so read it in beats:

- **The fact:** LEIE lists `0000000000` as the NPI on 89.6% of its rows.
- **Why it's dangerous:** a naive JOIN on NPI treats *every one of those all-zero rows as the SAME doctor* — manufacturing thousands of fake hard-ID facts.
- **The fix:** `clean.sql` must null the zero-token *before* any NPI join.
- **The stakes:** get it wrong and every banned-doctor count is poisoned. This is the trap that turns a NULL into a libel. *(There's also a separate date bug — `TRY_CAST` collapses all of LEIE's `EXCLDATE` text into garbage 1970 dates; use `TO_DATE(col,'YYYYMMDD')` in the same clean step.)*

---

## 9. The real bottleneck (and it's good news)

> **Your problem is not invention. It's loading depth + wiring more identifiers. The hard part is built.**

- **773 of ~1,030 leads (~75%) ride one connection.** That's a narrowness *risk* — and a roadmap. Every new identifier you land lights up new detectors.
- **No new detector fires without a new key landing.** Want a "shell-company contractor" story? Land the IRS nonprofit DB (EIN) and wire it — the framework's there. "Public company doing X"? Fix the SEC EDGAR fetch (a one-line user-agent fix) to land CIK. Real ship time series? Backfill more days of AIS.

The portal firehose is mostly tapped out — ~593 of 731 easy portals are in. **The next 10x comes from a handful of high-value, identified gaps** (IRS 990/BMF, SEC EDGAR, more Open Payments years), not from more crawling.

### ~~🚨 FIVE-ALARM — rotate the token before 2026-07-05~~ RESOLVED 2026-07-02

**The PAT was rotated — new expiry 2026-09-20.** Credential expiries now live in one canonical place,
`infra/keys_ledger.json`, and the pre-flight gate checks it before any long load. What *survives* from
the original alarm: every write still runs as ACCOUNTADMIN — standing up the `LIBRARY_WRITER`
least-priv role is still on the list, it's just no longer on a 7-day fuse.

### Two plays already on the shelf

- **Fix-Everything** (~2 sessions): finish the cleaning macros, fix broken loads, drain catalog debt, wire 3 new detectors, rotate the PAT, codify infra-as-DDL.
- **The Plane** (~1 session): an offline visual warehouse explorer — the "what do I actually have, at a glance" front end. *(Full spec: [`RIPPLE_DESIGN_BRIEF.md`](RIPPLE_DESIGN_BRIEF.md) + `outputs/PLANE_handoff.md`.)*

---

## 10. The bottom line

You have a **working investigative engine with a genuine moat and a catalog that audits itself** — not a prototype.

- **Architecture is sound and live:** checkpointed onboarding, a self-honest catalog, a scored 6-tier connection graph, fact-vs-lead discipline, detectors that already surfaced 773 excluded providers appearing in pharma payment records — leads pending human review, some payments may predate the exclusion.
- **The vision is bigger than what's delivered** (300+ sources, cross-domain detectors, a publishing layer that doesn't exist yet) — fine, as long as you use the honest numbers.
- **Two real exposures:** *lead narrowness* (one edge carries ~75% of findings) and *operational hygiene* (no mart CI, the secrets fuse above, no infra-as-code). Both on the fixable-with-existing-plays list.

The distance between what this is and what you want it to be is **execution, not genius.** The genius part is done.

---

**Founder — your next moves, in order.** (1) ~~Rotate the PAT before 2026-07-05~~ **done 2026-07-02 (new exp 2026-09-20, tracked in `infra/keys_ledger.json`)** — `LIBRARY_WRITER` least-priv role still pending, no longer deadline-driven. (2) Run the **Fix-Everything** play (~2 sessions) to drain catalog debt and wire 3 new detectors. (3) Land one new identifier (EIN or CIK) to break the ~75%-on-one-edge narrowness. Want a deeper staircase on any single piece — the record-linkage math, the dbt layer, the catalog's lifecycle logic — say the word and I'll build it.

*Methodology: built from a multi-agent read of every corner of the repo plus an adversarial skeptic pass over the impressive claims. Structure numbers (graph edges/tiers, dbt models & tests, node counts) are measured directly from repo artifacts — the graph is dated 2026-06-27. Lead counts (773 · ~1,030 · per-detector) and catalog counts (~1,647 cataloged · ~101 with data) are **last-recorded from the 2026-06-28 run, not re-queried from the live warehouse here**. To make every number and artifact agree, re-run `connect leads` and rebuild `connect_graph.json`.*
