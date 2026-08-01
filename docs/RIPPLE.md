# Ripple — The Book

*One document. What this is, what every word means, how to drive it, and how it
works under the hood — written so a smart friend with zero data background can
read it, and so the owner never has to fight his own repo again.*

*House rule, inherited from the constitution: **never trust a number typed in
prose** — including in this file. Any count here is a dated example, marked as
such. Current truth always lives in `build-state.md` (machine-generated) or a
fresh query. This document explains the machine; it does not report its gauges.*

*(This file replaces five older explainers, now preserved in `archive/`:
`OVERVIEW.md`, `PROJECT_SHAPE.md`, `LIBRARY_SNAPSHOT.md`,
`RIPPLE_FOR_EVERYONE.md`, `RIPPLE_MANUAL.md`, `RIPPLE_FOR_THE_FOUNDER.md`.
The design brief and pitch deck still stand on their own in `docs/`.)*

---

## Contents

1. [The bar story — what this thing is](#1-the-bar-story)
2. [The decoder ring — every jargon word, translated](#2-the-decoder-ring)
3. [The building, room by room](#3-the-building)
4. [Turning it on](#4-turning-it-on)
5. [The deep tour — how it actually works](#5-the-deep-tour)
6. [The honesty machinery](#6-the-honesty-machinery)
7. [Five things that will bite you](#7-things-that-bite)
8. [The files you trust](#8-the-files-you-trust)

---

## 1. The bar story — what this thing is {#1-the-bar-story}

The government publishes enormous piles of free public data — every licensed
doctor, every banned doctor, every federal contract, every registered cargo
ship, every sanctioned vessel. The catch: **it's all in separate boxes that
never talk to each other.** The list of *banned* doctors has no idea the list
of doctors *getting pharma money* exists.

**Ripple downloads the boxes, cleans them, stores them in one warehouse, and
draws the roads between them.** Then it points at the roads that shouldn't
exist — a banned doctor still getting paid, a debarred company still winning
contracts, a sanctioned ship still broadcasting its position — and puts each
one in a queue for a human to review. As a dated example of what one run of
this looks like: an early pass flagged hundreds of officially excluded
healthcare providers who nonetheless appeared in pharmaceutical payment
records — found in about five minutes, where a journalist cross-referencing by
hand would lose weeks.

The data is free and anyone can download it. The *connections between* the
data — nobody else has built that. **The roads are the entire product.**

And the rule that makes this journalism instead of a rumor machine:

> **Same government ID number = a fact. Same name = just a hunch.**
> Ripple knows the difference, and it refuses to publish a hunch as if it
> were proof. Nothing is ever called true until a human confirms it — and
> auto-publish isn't a policy, it's structurally impossible (see §6).

Everything in this repo is one of four jobs: **fetch the data, clean the data,
connect the data, or show a human the results.** Every scary word below
belongs to one of those four jobs.

---

## 2. The decoder ring — every jargon word, translated {#2-the-decoder-ring}

Read this twice and 90% of the repo stops being scary.

### Storing the data

| The word | What it actually means |
|---|---|
| **Snowflake** | The rented cloud database where all the data lives. A giant Excel-in-the-sky. When anyone says "the warehouse," they mean this. |
| **warehouse** | Confusingly, Snowflake uses this word two ways: the whole database, *and* the little engine that runs your queries. Ours are all size "X-Small" (the cheapest) and auto-shut-off after 60 idle seconds — which is why the bill stays low. |
| **landing table** | Raw data exactly as it arrived from the government, mess and all. Nothing cleaned yet. |
| **row / column** | Same as a spreadsheet: a row is one record ("this one doctor"), a column is one attribute ("their license number"). |
| **schema** | Just "the list of what columns a table has, and what type each one is." That's the entire word. |
| **SQL** | The standard language for asking a database questions. |

### Cleaning the data

| The word | What it actually means |
|---|---|
| **dbt** | A tool that runs a big folder of SQL cleanup recipes in the right order and can test the results. A recipe-runner, nothing more. |
| **model** | One dbt recipe = one SQL file = one cleaned table or view. Not "model" like AI — an unfortunate industry word for "a saved data-shaping recipe." |
| **staging** | The first cleanup pass: rename ugly columns, fix types, nothing clever. One staging model per raw table. Dishes rinsed, not yet cooked with. |
| **mart** | A finished, cleaned, query-ready table — the thing you actually use, sorted into topic folders (health, justice, finance…). When you "query the database," you query marts. From "data mart," like a market stall of ready goods. |
| **grain** | The answer to "what does ONE row in this table mean?" One row per doctor? Per doctor-per-year? Per payment? Get grain wrong and every count and sum is silently wrong — this exact mistake once hid over a million prescription rows. The single most important word in this table. |
| **dbt test** | An automatic tripwire on a mart: "this column is never empty," "no duplicate license numbers." |
| **severity: warn** | A test set to grumble instead of stopping the show when it fails. A smoke alarm with the batteries out. |
| **YAML / .yml** | Plain-text settings files (indentation instead of brackets) where tests and table descriptions get written down. |

### Connecting the data

| The word | What it actually means |
|---|---|
| **join / join key** | A join = matching rows across two tables ("find this doctor in both lists"). The join key is the column you match on. The entire product is joins; everything else is prep. |
| **entity** | One real-world thing — a specific person, company, hospital, or ship — no matter how many datasets it appears in. |
| **entity spine** | The master who's-who list: every entity, pinned to its official government ID numbers, with a list of every dataset it shows up in. The "spine" because everything else hangs off it. |
| **NPI, EIN, CCN, IMO…** | Government ID numbers. NPI = a doctor's federal license number. EIN = a company's tax ID. CCN = a healthcare facility's Medicare number. IMO = a ship's hull number. These are the gold: they can't be faked or misspelled the way a name can. |
| **STEEL / STRONG / GEO / PROBABILISTIC** | The house four-tier trust ranking for join keys. STEEL = hard government IDs (safe). STRONG = real but softer codes. GEO = locations (coarse). PROBABILISTIC = names and addresses (a hint, never proof). |
| **fact vs. lead** | The house rule (§1). Matched on a hard ID → **fact**, can stand alone. Matched on a name → **lead**, a human must confirm before it means anything. |
| **edge** | One confirmed road between two datasets on the map: "this exact entity appears in both." |
| **detector** | One saved question that hunts a specific kind of wrong — "banned but still paid," "sanctioned ship still broadcasting." Each hit becomes a lead in the review queue. |
| **sentinel value** | A fake placeholder pretending to be data — a column "100% full" of empty strings or `0000000000`. See §7. |

### Running the machine

| The word | What it actually means |
|---|---|
| **loader / ingest** | A script that downloads one source and pours it into a landing table. "Ingest" is just the fancy word for the pour. |
| **pipeline / orchestration** | Pipeline: steps that run in order (download → clean → connect). Orchestration: the scheduling that makes them run on time. No magic. |
| **CI** | "Continuous integration" — a robot on GitHub that re-runs the tests every time code changes, so a mistake is caught the day it's made. |
| **venv** | "Virtual environment" — a private toolbox of Python packages for one project. This repo needs two (§7, item 3). |
| **Streamlit** | A tool that turns a Python script into a point-and-click web page in your browser. All the apps here are Streamlit. |
| **PAT** | "Personal access token" — a password-like key that lets a script log into Snowflake. |
| **provenance** | "Where did this claim come from, and how sure are we?" The honesty engine (§6) stamps every mart with it, by machine. |
| **heartbeat** | A small scheduled job that keeps routine refreshes running and notices staleness. The building's pulse check. |

---

## 3. The building, room by room {#3-the-building}

Open the repo folder and here's what each door actually is:

- **`scripts/` — the loading dock.** ~140 scripts that each fetch one
  government source and pour it into Snowflake, plus the maintenance crews
  (audits, generators, schedulers). Rarely opened by hand.
- **`library-onboarding/` — the kitchen.** Where new sources get walked in (a
  six-checkpoint tool that stops for human approval at every step), and where
  `ripple_dbt/` lives: all the cleaning recipes. The heart of "the data is
  clean."
- **`connect/` — the corkboard room.** The Python engine that builds the
  entity spine, draws the edges, and runs the detectors. Red string and
  pushpins — except every string must be a government ID.
- **`honesty/` — internal affairs.** The grader that stamps every mart's
  provenance (fact / lead / unverified) by machine, and the written registry
  of every known data trap. Exists so the platform can't quietly overclaim.
- **`reading_room/` — the front desk.** The review queue of leads, each with
  its receipts, waiting for a human yes/no. This is what `START_HERE.bat`
  opens.
- **`viz/` + `ripple/` — the drafting table.** The chart instrument (Plotly —
  interactive charts in the browser) and the `ripple` command line: `chart`,
  `deck`, `doctor`, `panel`, `pour`, `review`.
- **`politics/` — the annex.** A parallel wing for Congress: campaign money,
  votes, bills, judges. Built by its own Python loaders and reconciled to the
  penny against outside sources; guarded by a tripwire (§7, item 1).
- **`portal_recon/` — the scout tower.** The census of hundreds of thousands
  of public datasets that exist out in the world, catalogued and ranked by how
  joinable they are — the overwhelming majority known-about but deliberately
  not yet pulled.
- **`serve/` — the Atlas (legacy).** An older browse-the-warehouse app:
  search, entity dossiers, the connection graph. Still runs; superseded as the
  daily front door by the Reading Room.
- **Everything else.** `loadkit/` = shared safety gear all loaders wear
  (checkpoints, truncation alarms, atomic swaps). `infra/` = database setup as
  code + keys. `tests/` = the Python tripwires. `outputs/` + `archive/` = the
  dated paper trail (see `outputs/INDEX.md`). `mission_control/` = an older
  explainer app.

---

## 4. Turning it on {#4-turning-it-on}

**The honest prerequisite:** the data lives in a private Snowflake account, so
running this needs the login token file (`library-onboarding/.env` — a
template sits next to it showing the blanks). A friend without the token sees
the apps but no data. That's a feature, not a bug: it's your warehouse.

### The one-double-click path

1. Open the `C:\Code\Ripple_v6` folder.
2. Double-click **`START_HERE.bat`**.
3. A black window installs what it needs (first run only), then the browser
   opens the **Reading Room** at `127.0.0.1:8890` — that address just means "a
   page served by this computer, to this computer." Nothing is on the internet.
4. You're looking at the lead queue. Browse freely: nothing you click can
   publish anything (§6).

### The three commands that matter

```bash
# Rebuild the map: profile tables, find real connections, refresh leads
python -m connect all

# Walk a brand-new data source into the Library, approving each step
python library-onboarding/onboard.py

# Make a chart from warehouse data
python ripple.py chart
```

Everything else in the repo is either called by these, scheduled to run
itself, or a one-time tool you'll meet when you need it.

### The two-toolbox note

Python dependencies install into `.venv` from `requirements.txt`. **dbt is
deliberately not in there** — one of its parts genuinely conflicts with the
main toolbox's Snowflake connector — so it gets its own venv:

```bash
python -m venv .dbt-venv && .dbt-venv/Scripts/pip install -r requirements-dbt.txt
```

If dbt says "command not found," you're in the wrong toolbox. Not broken —
wrong door.

---

## 5. The deep tour — how it actually works {#5-the-deep-tour}

Four verbs do the whole job: **SCOUT → COLLECT → CONNECT → DETECT.** Two
honesty layers sit on top (§6). Each verb below comes with the true story
that shaped it, because the stories are why the design is what it is.

### SCOUT — casing every joint before touching anything (`portal_recon/`)

Before landing a single row, Ripple asks: what data even *exists*, and what's
worth chasing? The scout fingerprints hundreds of open-data portals, pages
through their catalogs pulling one metadata record per dataset (title,
columns, row count — never the data itself), and tags every dataset by what
kind of join key its columns carry, using the STEEL/STRONG/GEO/PROBABILISTIC
tiers. Politeness is engineered in: tiny capped reads, delays between
requests, hard per-portal limits. This is the constitution's "a census, not a
subpoena," made literal in code.

The discipline: the scout is built to be *wrong in the safe direction* — its
own code states **"a false STEEL tag is worse than no tag."** A column called
"DOI" looked like a trustworthy hard ID until an audit found every real-world
hit was actually a *Date Of Injury* field. DOI was pulled from the trusted
list entirely rather than left in as an occasional false positive.

### COLLECT — six stops, and the machine won't move without a "go" (`library-onboarding/`)

`onboard.py` walks one source through six steps — recon the documentation,
write the fetch code, load, write the cleanup models, register in the
catalog, wire into the graph — and **stops for a literal keyboard prompt at
every one** (`go / edit / skip / abort`).

Why six stops instead of running end to end? Because "it ran without an
error" and "it actually worked" are different claims, and this repo has the
receipt: a source once landed over four million rows, logged itself
`success`, and rode into the catalog — while being **100% empty in every
column**, because the parser had silently collapsed everything to blank.
That failure is why the **density gate** now exists: after every load, the
tool measures how much of the data is actually filled in, and demotes
hollow loads from `success` to `empty` before they can poison the catalog.

### CONNECT — only a real government ID gets to draw a line (`connect/`)

The founding lesson, told as the true story it is: an early version
normalized ID codes by *stripping* leading zeros — and once matched an
Alabama nursing home to a Puerto Rico drug store, because their facility
codes collapsed to the same number with the zeros gone. The fix, used
everywhere now: **pad, never strip.**

The matching mechanism, in four steps:

1. **Tag** the column (same tiers the scout uses — one shared list, guarded
   by a test that keeps the copies in lockstep).
2. **Normalize** the values so honest comparison is possible (pad, not strip).
3. **Actually join** and count real matches — never trust "both tables have
   an EIN-shaped column" as proof of anything.
4. **Score against chance.** The engine computes how many matches pure
   coincidence would produce given the ID's possible-value space; a match
   count that isn't comfortably above the coincidence line is thrown out as
   a fluke. Industry-classification codes (NAICS/SIC) are hard-banned from
   ever counting as a connection — "same industry" was never "same entity,"
   and that vocabulary noise once made up the majority of an inflated early
   graph.

The **entity spine** is built by grouping records on their normalized hard
IDs — which means, by construction, it can never falsely merge two different
people. Different ID *types* are never fused into one identity either: an
NPI (a doctor) and a CCN (a facility) get a works-at *relationship*, never
an identity, because fusing them "would merge a doctor with a hospital."
Fuzzy name-matching exists but lives outside the spine, writes only to a
review table, and never becomes a stated fact without a human decision.

### DETECT — turning a connection into a lead worth a human's time (`connect/leads*.py`)

Two genuinely different kinds of detector run today:

- **Declarative joins** (most of them): name a "flag" list (bans, sanctions,
  debarments) and an "active" list (payments, contracts, position
  broadcasts), join on a shared hard ID. On both lists at once → lead. One
  SQL join per detector, no AI anywhere.
- **Cohort outliers** (the newer kind): no second list at all. Score every
  establishment against its own peer group (same industry, same size band)
  on a statistic the government itself requires them to report, and flag
  extreme outliers with enough real cases behind the number that small-sample
  noise can't trigger it. The dated example: one hospital scored dozens of
  times its own peer group's injury rate.

Every detector's output, whichever kind, lands in the same queue and flows
through the same review machinery — deliberately, so a new detector can't
invent its own less-scrutinized path to becoming a public claim.

---

## 6. The honesty machinery {#6-the-honesty-machinery}

This is the part that makes the whole thing defensible, and none of it is a
promise — it's all enforced mechanically.

**The review gate.** A human reviews a lead and clicks Confirm, Reject, or
Needs-work; that click writes one row to a decisions log. The login the
review tool writes through has, at the database-account level, only INSERT
and SELECT permission on that table — **no UPDATE, no DELETE.** Even a buggy
app physically cannot edit or erase a decision once written.

**Confirm is not publish.** The only code path in the entire repository that
can write the word "published" is one standalone script, run manually, that
refuses to run unless the lead is already confirmed, previews by default,
only writes with an explicit `--apply` flag, and requires a typed
plain-text reason. The everyday review tool isn't even *allowed* to write
that word. No accidental click, anywhere, can make something public.

**The provenance grader** (`honesty/`). A zero-AI tool reads the build
system's own record of how every mart was constructed and grades each one:
`fact` (every join in its lineage anchors on a real hard ID — re-derivable
by a stranger), `lead` (touches the human-review layer upstream), or
`unverified` (the tool can't tell, and refuses to guess in the trusting
direction). It fails closed.

**The trap registry** (`honesty/traps.py`). Every data trap that has ever
burned this project is written down as machine-readable policy, mirrored
into the warehouse registry, and drift-tested so the copies can't silently
disagree. The greatest hits are in §7.

**The self-cut headline.** The best single credential this platform has: its
own connection count was once slashed by roughly 94% *by its own tightening
pass*, when the industry-code exclusion landed and a half-loaded category
was pulled from scoring. A platform built to catch institutions inflating
their numbers watched its own flagship metric and cut it rather than let a
bigger, wrong number stand.

**The honest current state.** The gate is built, tested end-to-end, and — as
of this writing — **nothing real has been pushed through it.** The count of
genuine human review decisions is recorded in `build-state.md`
(`decisions.total`); check it there, not here. The guardrails are real; most
haven't been exercised by a real published finding yet. That gap is the
honest state of the project, not spun in either direction.

---

## 7. Five things that will bite you {#7-things-that-bite}

1. **Never run a bare `dbt build`.** The politics tables are penny-perfect
   mirrors built by their own loaders; a naive full rebuild would flatten
   them. A pre-hook tripwire will stop you — when it does, it's protecting
   you, not misbehaving. (Rebuild deliberately with
   `--vars '{"allow_politics_rebuild": true}'` and only when you mean it.)
2. **A column can be "100% full" and 100% fake.** The famous one: the doctor
   registry's company-tax-ID column is fully populated — with blanks and the
   literal text `<UNAVAIL>`. Zero real values. Before trusting any column as
   a join key: `COUNT(DISTINCT col)` plus an eyeball of a value sample,
   every time. The traps already hit are fenced in `honesty/traps.py`; new
   columns deserve the same suspicion.
3. **Two toolboxes, on purpose.** dbt lives in `.dbt-venv` because of a real
   package conflict (§4). "Command not found" means wrong toolbox, not
   broken.
4. **The ship data is a photograph, not a movie.** The AIS vessel-position
   table covers one fixed week of January 2024. Fine for maps; never chart
   it over time. The lead queue already carries this caveat on affected
   leads.
5. **"The log says success" is not "it worked."** See the density-gate
   origin story (§5). The gate now catches hollow loads — but keep the
   reflex: check the actual table, not the log.

---

## 8. The files you trust {#8-the-files-you-trust}

- **`build-state.md`** — the instrument panel, machine-generated straight
  from the warehouse: real row counts, entity counts, open defects. **The
  only numbers that count.** Any prose that disagrees with it — including
  this file — is stale by definition.
- **`CHRIS_DECISIONS.md`** — the owner's decision ledger: what's open, what's
  been ruled. When lost, read the open items here first.
- **`CLAUDE.md`** — the operating constitution: mission, decision lanes, and
  the hard facts nobody gets to assume. It wins every argument with every
  other document, including this one.
- **`outputs/INDEX.md`** — the labeled filing cabinet for the dated audits,
  briefs, and handoffs that record how the project got here.

Everything else with a date in its name is history, kept on purpose as a
paper trail, and safe to ignore on a working day.

---

*The one-sentence version, for the friend at the bar: Ripple pours the
public record into one warehouse, draws only the connections that can't be
faked, points at the ones that shouldn't exist — and refuses, mechanically,
to call anything true until a person says so.*
