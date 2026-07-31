# Open Calls for Chris

Running list of things only Chris decides, or that cost real money/compute.
Claude appends here instead of blocking. Nothing on this list is a blocker for
ongoing work — the work routes around it.

**Status key:** `OPEN` needs a call · `DONE` decided/actioned · `DROPPED` decided against

---

## OPEN — costs compute

### 1. Re-run the matching layer so the name fix cashes out
`python -m connect discover` + the leads jobs.

The `ARRAY_EXCEPT` fix (2026-07-31) means org names with two "of"s can finally
match themselves — *Sisters of Charity Hospital of Buffalo*, *County of Pasco
Office of...*, *State of Oregon Department of...*. But `connect spine` doesn't
rebuild the name-tier edge list or the leads, so the payoff hasn't happened yet.
The fix is live in code and in the spine; the connections it unlocks are not.

More compute than the spine rebuild was. **Rec: yes, do it** — this is the whole
point of the fix, and "we found connections that were invisible before" is a good
line in a demo.

### 2. `_addr_canon` fix — apply now, or batch it?
Written and validated against live Snowflake, deliberately NOT applied.

Same family of bug as the name one, in street addresses: `2 SOUTH SOUTH SOUTH RD`
canonicalizes to `2 S SOUTH S RD` — the `REPLACE` chain eats the shared space, so
repeated words come out half-converted. Fix is a token-wise `TRANSFORM`
(order-preserving; addresses can't be sorted the way names are).

Applying it bumps the config fingerprint → forces another full spine rebuild.
**Rec: hold and batch** with the next change that needs a rebuild anyway. Repeated
words in one address are much rarer than double-"of" in a name.

---

## OPEN — red lane (taste / risk)

### 3. Should CI have write access to the warehouse at all?
**UPDATE 2026-07-31 — the blast radius is already reduced; the question is smaller now.**

While reading `infra/ddl/03_warehouses_roles_monitor.sql` I found that
**`RIPPLE_TRANSFORM_RW` already exists**, and its own comment says exactly what it's
for: *"dbt transform: read RAW landing + META, build STAGING and MARTS. Least
privilege, used by GitHub Actions."* Confirmed live via SHOW ROLES. The
purpose-built least-privilege role was sitting unused while CI claimed
ACCOUNTADMIN.

Changed the workflow to use it. Safe to do now either way — the build step is still
gated on a `SNOWFLAKE_PAT` secret that doesn't exist, and `dbt parse` needs no
privileges at all.

So the remaining question is genuinely just **"do you want CI building at all?"**,
not "should CI be account admin" — that part is fixed. My rec is still parse-only,
but it's now a preference rather than a risk.

*(Original entry below.)*

### 3b. (original) Should CI have write access to the warehouse at all?
`.github/workflows/dbt.yml` pins `SNOWFLAKE_ROLE: ACCOUNTADMIN` and runs
`dbt build --select staging intermediate` on every push to main — gated only on a
`SNOWFLAKE_PAT` secret existing. No secret today, so it's dormant. The trap: the
first person who adds that secret to unblock testing silently turns on
"every push to main rebuilds LIBRARY_STAGING as account admin."

**Rec: parse-only in CI, builds stay manual.** But it's a real call, not a
rubber stamp — if you want CI builds, the fix is a scoped role, not ACCOUNTADMIN.

---

## OPEN — housekeeping

### 4. Commit the 2026-07-31 bug-sweep fixes
Four files, uncommitted, all tests green (620 passed / 3 skipped):
- `connect/keys.py` — ARRAY_EXCEPT → FILTER; ZIP length gate
- `serve/serve_queries.py` — restored the missing digits-only sentinel guard
- `tests/test_keys_normalize.py`, `tests/test_serve_queries.py`, `tests/test_honesty.py` — +6 tests incl. drift guards

---

## DONE — the scheduler had a landmine in it (2026-07-31)

`scripts/heartbeat.py` — 1,195 lines, decides when every other job runs, runs
unattended, and had **no tests at all**.

The bug: `_parse()` has a try/except clearly meant to make it total. It isn't. An
unparseable string falls back safely, but a perfectly VALID timestamp with no
timezone (`2026-07-31T10:00:00`) parses fine and comes back naive — then blows up
one frame later in `tier_age_s`, which subtracts it from an aware `now()`:

    TypeError: can't subtract offset-naive and offset-aware datetimes

Nothing catches that. In the scheduled spine, that means **every job silently stops
and nothing says why.** `iso_now()` always writes an offset today, so this is a
latent trap rather than a live outage — a hand-edited state file, a restored backup,
or any future writer that forgets `tzinfo` arms it.

Fixed (assume UTC for naive — every timestamp the file stores is UTC-derived), and
added `tests/test_heartbeat.py`: 11 tests covering the scheduling arithmetic, with a
parametrized case asserting that **whatever** ends up in the state file, computing a
tier age returns a number instead of taking the scheduler down.

**Checked and found clean:** `ingest.py`'s incremental watermark logic (the
orderability guard is correctly placed *after* the read, so a raise can't be
swallowed into a silent full-backfill duplicate) and the politics loaders (they
reconcile against OpenFEC/GovTrack and abort rather than build on unreconciled
data). Worth knowing which parts don't need your attention.

---

## DONE — data integrity (2026-07-31)

### The honest version: most of this was already built. I found the gap in it.
Ripple already had a **density gate** that catches empty loads at ingest time, a
test suite for it, and a repair script (`regrade_empty_loads.py`) that names
FED_FJC_IDB in its own docstring. FJC and NIH were **already** correctly marked
`STATUS='empty'`. Nothing was lying about those two.

**The gap:** the gate measures the fraction of populated *cells*, with a 1% floor.
A load where exactly ONE column survives the parse sails straight over it — one full
column out of fourteen is 7% of cells, seven times the floor. So two sources logged
`success` and reached the catalog as `LIFECYCLE='modeled'`, `TRUST_LAYER='mart'`:

- `fed_ffiec_call_reports` — a saved HTML page (7.1% density)
- `intl_fatf_ratings` — country names landed, all six rating columns blank (14.3%)

**Fixed** by adding a structural trigger to the gate: in a frame of 4+ columns, if
exactly one carries data, the parse didn't split. Deliberately narrow so it can't
collide with the legitimate "2 key columns + 198 optional blanks" shape the existing
floor comment protects. 4 new tests, including that protected case.

Note `_reject_html` already caught the FFIEC shape (added after that July load).
The genuinely new coverage is the **FATF shape: a non-HTML parse failure**, which
neither existing guard could see.

**Re-graded both** via the repair script → `STATUS='empty'`. Also added a `--source`
filter to that script; without it, it re-samples all ~1,000 landing tables and times
out, which made it useless for targeted repair.

### The subtle one: why re-grading wasn't enough
`LIBRARY_META.REGISTRY.CATALOG` resolves lifecycle with **`WHEN f.real_mart THEN
'modeled'` as its FIRST branch**. A mart built on garbage keeps advertising its
source as fully modeled, whatever the ingest log says. So `regrade_empty_loads.py`'s
docstring claim — *"fixing STATUS here is enough, no catalog write needed"* — is
false whenever a mart already exists.

**Do NOT fix this by making `empty` beat `real_mart` in that view.** I checked:
`fed_dea_arcos` has a stale 409-row failed run sitting right next to a genuinely
healthy **178.6M-row** dataset (verified — 16 distinct DEA numbers, 15 reporter
names in a 20k sample; your pitch deck is accurate). That precedence is what stops
ARCOS being wrongly condemned. Reordering it would trade two false positives for one
much worse false negative.

Fixed the right way instead: disabled the two garbage marts in `dbt_project.yml`,
using the pattern already there. No mart → lifecycle falls through to `empty`.

Also disabled `justice__fed_fjc_idb`. Its config comment said *"re-enabled
2026-07-24: source re-ingested (4.1M rows)"* — the row count was re-ingested, the
data wasn't.

### Still open: do you want the data itself?
FJC (4.1M court records), NIH (5,000 grants), FFIEC (call reports) and FATF
(ratings) are all now **correctly labelled as empty** — nothing claims to have data
it doesn't. Actually *getting* that data means re-running four loaders against
external government sites and debugging each parse. That's a project, not a fix.
Say the word if you want it.

---

## OPEN — data integrity (original writeup below)

### 0. `FED_FJC_IDB` is 4,126,450 rows of nothing
Found 2026-07-31. Every column, on every row, is the **empty string**. There is no
federal court data in that table at all.

It hid because every signal said it was fine:
- The loader logged **success** — the row count matched the source.
- `COUNT(col)` reads **100% populated**, because `''` is not `NULL`. (This is the
  exact trap CLAUDE.md documents for NPPES `EIN` and NOAA_AIS `imo_number`.)
- `dbt_project.yml` carries the comment *"re-enabled 2026-07-24: source re-ingested
  (4.1M rows)"* — true, and meaningless. Somebody checked the row count, not a value.

What finally exposed it: the staging model dedups on a surrogate key built from
`circuit + district + office + docket`. All four are `''` on every row, so all 4.1M
rows produced **one identical key** and the dedup collapsed them to a single row.
The 1-row mart under a 4.1M-row source was the symptom, not the bug.

**Nothing is wrong with the pipeline — it behaved correctly on garbage input.** The
bug is upstream in the load.

**Needs you:** re-ingesting FJC IDB is a loader run against an external source.
Want me to dig into why the parse produced blanks and re-run it? That's the fix;
it's just not a five-minute one, and it's real compute.

Related, already handled: I nearly put a corrupt table on your pitch deck. The
audit flagged `FED_FDA_FAERS_REAC` (20.6M rows) as suspect while I was adding it to
the top-10 slide — it turned out **healthy** (1.53M distinct case IDs); my
heuristic was counting all-NULL legacy columns as damage. Heuristic fixed, table
verified, slide is accurate.

### 0b. New tool: `scripts/audit_blank_landing.py` + full sweep results
Because finding this by accident is not a strategy. Read-only, never writes, exits
non-zero on a find so it can gate a pipeline later.

**Swept all 1,455 landing tables ≥100 rows. The headline is good news: 1,448 are
healthy.** Corruption is rare and specific, not systemic — FJC was an outlier, not
a pattern. Four real problems:

| Table | Rows | What's wrong |
|---|---|---|
| `FED_FJC_IDB` | 4,126,450 | every column blank — see #0 above |
| `FED_NIH_REPORTER` | 5,000 | every column blank; the round 5,000 says truncated/sample load |
| `FED_FFIEC_CALL_REPORTS` | 302 | **a saved web page.** First column is `DOCTYPE_HTML` holding `<html lang="en">`, while `RSSD_ID`, `INSTITUTION_NAME` and `TOTAL_ASSETS` are all empty — the loader fetched an HTML page and the parser turned the markup into a schema |
| `INTL_FATF_RATINGS` | 200 | partial parse — `COUNTRY` populated (158 distinct), the other 6 columns frozen. The country names landed; the ratings didn't |

Note `INTL_FATF_RATINGS` also has a mart (`justice__intl_fatf_ratings`) and is one
of the 26 models still without tests — a broken source under an untested model.

**The tool was wrong THREE times before it was right, and checking is what caught
it every time.** Worth reading as a pattern, because it's the same mistake in three
costumes: a signal that looks damning in isolation, and isn't.

1. `FED_FDA_FAERS_REAC` (20.6M rows) — all-NULL legacy columns read as damage. Healthy.
2. `FED_DHS_OHSS` (50,740) — 475-column ragged union, blank leading columns, 460 of
   the rest full of data. Healthy.
3. The markup detector — I added "a column named after an HTML tag means a page got
   scraped", with a list including `DIV`, `STYLE`, `BODY`, `TYPE`. It hit four
   tables and **three were false positives**: `DIV` is a real column in a Tucson
   property-assessment extract (division), `STYLE` in an Allegheny County GIS
   streets layer. Those are just words. Narrowed to `DOCTYPE` only — no real dataset
   has a column called `DOCTYPE_HTML` — and even that now only nominates: the real
   data columns must also be blank before anything is reported.

The general fix in all three: **nothing convicts on a screen.** Every signal
nominates; a full-width confirming pass decides. All three cases are written into
the code as documented regressions so the next person to "simplify" the screen sees
what it costs.
It first convicted `FED_FDA_FAERS_REAC` (20.6M rows) and `FED_DHS_OHSS` (50,740) —
both **healthy**. FAERS has dead legacy columns that read as damage; DHS_OHSS is a
475-column ragged union whose first 12 columns are blank while 460 of the rest
carry real data. My screen only looked at 12 columns.

Rewritten as **screen → confirm**: the cheap 12-column pass now only nominates, and
nothing is reported until a full-width pass over every column, on the whole table,
agrees. A corruption detector that cries wolf is worse than none — it teaches you
to ignore it. Both false positives are now regression cases documented in the code.

---

### 0d. 26 dbt models still have no tests (down from 30)
Overall coverage is genuinely good — **3,663 tests across 1,299 schema files** for
1,378 models. That's a strength worth saying out loud in an interview.

But the gap was in a bad place: **the four flag registries that power the headline
detectors had zero tests.** LEIE (banned_but_paid, excluded_but_billing), OFAC SDN
(both sanctioned_vessel rules), SAM exclusions (debarred_but_funded), and OSHA
inspection. Each declared its grain in a header comment with nothing enforcing it —
so a silent grain break would inflate lead counts on claims about named people, and
nothing would catch it.

**Fixed 2026-07-31** for the three live ones: grain verified against live data
first, then tests written, then actually run — 6 new tests, all PASS. (OSHA
inspection needs none; it's a disabled placeholder because its landing table
doesn't exist.)

26 models still uncovered, none of them detector-critical. Want me to work through
them, or leave it? Low risk either way — this was the load-bearing part.

---

## OPEN — architecture / portfolio-visible

### 0e. The honesty engine can't see an empty mart
Not a bug — a scope gap worth knowing, because it bit us today.

`python -m honesty` grades 391 marts: **389 fact, 1 lead, 1 unverified**. It's
deterministic as advertised (re-ran it; only the timestamp moved, every grade
identical).

But it grades **provenance**, not **completeness** — it walks lineage and asks "was
this derived through a hard-ID join?", never "is there anything in it?". So
`civil_rights__fed_nara_wra_aad` grades a confident **"fact"** while containing
exactly **1 row**. Same for the FJC mart sitting on 4.1M blank rows. Both are
honestly graded and both are empty.

That's the gap `scripts/audit_blank_landing.py` fills from the other side. **Want me
to wire the two together** — have the grader refuse to stamp "fact" on a mart whose
source failed the blank audit? It'd be a genuinely strong thing to show off: a
provenance grader that also knows the difference between "correctly derived" and
"actually has data in it." Your call, it's a real design change to the honesty
engine, not a fix.

### 0c. All 1,141 staging models live in a schema named after a person
`LIBRARY_STAGING.DBT_CROGERS`. The `generate_schema_name` macro's own comment says
it: models that set no custom schema "ALL resolve to `target.schema`
(DBT_CROGERS in the dev profile)."

Marts are fine — they set `schema=` and land in proper domain schemas (HEALTH,
POLITICS, ENVIRONMENT, FINANCE...). It's the staging layer that's sitting in a dev
namespace.

Why it matters for a portfolio: the deck sells "four databases, organized by
function." A reviewer who opens the warehouse sees 975 staging models in
`DBT_CROGERS`. It reads as a dev environment someone shipped by accident, which is
unfair to the actual architecture.

**Rec: route staging to domain schemas the same way marts already are.** But it's a
rename of 1,141 objects and everything that reads them, so it's your call on
whether that's worth doing before a demo or after. Not a correctness bug — purely
how it presents.

---

## OPEN — portfolio / demo polish

### 5. ~~The pitch deck's numbers have drifted~~ → FIXED, one framing call left for you
**All factual numbers corrected 2026-07-31.** See the DONE section for the full
list of what was wrong. The one thing I did NOT decide for you:

The deck now leads with "eight detectors have produced 17,256 leads" and explains
the split — 16,215 from one statistical outlier sweep, 1,041 from seven
intersection rules. I wrote that explanation because the raw total, unexplained,
makes it look like Ripple accuses 17,000 people of something.

**Your call: is that the framing you want?** The honest alternative is to lead with
the 1,041 intersection leads and present the OSHA sweep as a separate capability.
Both are true. Tell me which story and I'll reshape it.

### 5b. (original entry, for context) The pitch deck's numbers had drifted
`docs/ripple_pitch_deck.md` is the doc README sends reviewers to first, and it
says "here's the actual query that backs this up." If a reviewer runs the query,
they now get a different answer. Verified live 2026-07-31:

| Deck claim | Live now |
|---|---|
| "six detectors have produced 1,041 leads" | **8 detectors, 17,256 leads** |
| "555,381,078 rows across 1,942 tables" | **875,575,558 rows across 1,937 LANDING tables** |

Good news buried in there: the row count nearly doubled. The six original detector
counts in the deck's table are still **exactly right** (773 / 236 / 12 / 11 / 4 / 3) —
nothing broke, the deck just predates two new detectors.

The awkward part is the new one: `osha_cohort_outlier_2024` alone has **16,215**
leads — 94% of everything. I read it; it's well-built (frozen SQL, neutral
peer-relative language, receipt path, explicitly leaves the wrongdoing call to
you). It's big because it's a *statistical outlier scan*, not a rare-event match.

**This is a taste call, not a math one:** "1,041 carefully-targeted leads" and
"17,256 leads, 94% from one statistical scan" tell very different stories about
what Ripple is. I did not rewrite your pitch. Tell me which story you want and
I'll make the numbers match it.

### 6. ~~A demo chart has hardcoded numbers in it~~ → FIXED 2026-07-31
Now derived live from the cached graph, with two regression tests. No decision
needed. Original writeup kept below for the record.

### 6b. (original entry) A demo chart has hardcoded numbers in it
`connect/leads_overlay.py:247-251`. The "Detector backlog — STEEL 37 · CCN~NPI 39 ·
NPI 21 · CIK 1" caption is frozen prose — sitting eight lines below a comment
that praises the *other* caption for being "DERIVED from the live counts (never
frozen prose)." If those numbers have moved, the chart states them on screen
anyway.

I did not "fix" it by deriving them, because I couldn't confirm the source query
and a confidently-wrong derived number is worse than a visibly-dated one.
**Rec: either point me at how those four were computed and I'll derive them, or
I date-stamp the caption so it can't silently lie.**

### 7. Operational warnings that would show up in a live demo
`ripple doctor` runs GREEN, but with three advisories worth clearing before a
demo:
- **49 sources overdue+stale** — "refresh queue backing up." The most visible one.
- DR export is 26 days old (threshold 8).
- 3 optional API keys unset (CENSUS, COURTLISTENER, SOCRATA).

---

## DONE

- **2026-07-31 — pitch deck + README factual accuracy pass.** README sends
  reviewers to the deck first and the deck says "here's the actual query that
  backs this up," so every number in it is a credibility surface. Verified each
  against the live warehouse and corrected:
  - **README claimed `dbt-fusion` is in `requirements.txt`.** It isn't — that
    package has never existed on PyPI and was pulled 2026-07-30. Replaced with the
    real reason dbt lives in its own venv (genuine `snowflake-connector-python`
    version conflict).
  - **"10,500 SQL files"** → **~1,400 hand-authored.** The old number counted dbt's
    *compiled output* in `target/` (20,694 machine-generated copies). This was the
    single biggest credibility risk in the deck — a reviewer can disprove it with
    one `find` command. Also "2,800 YAML" → ~1,400.
  - **"Total registered 2,575"** never summed to its own table rows (they total
    2,460) and hid 532 sources. Now shows subtotal + remainder + true total (2,992).
  - **Top-10 largest tables omitted the two biggest datasets entirely** — DEA ARCOS
    (178.6M rows) and the grown SEC 13F (39M → 101M). ARCOS is arguably the most
    compelling dataset in the warehouse for this pitch; it wasn't on the slide.
  - Row count 555M → **875,575,558**; tables 1,942 → **1,937**; dbt models 1,032 →
    **1,378**; staging models 969 → **975**; match-pairs 16.2M → **31.1M** (plus
    22.6M entities); detectors six → **eight**.
  - Everything that was already right and stayed: portal index 338,520, the six
    original detector counts (773/236/12/11/4/3), the per-domain source counts.

- **2026-07-31 — detector-backlog chart caption is now derived.**
  `connect/leads_overlay.py` had "STEEL 37 · CCN~NPI 39 · NPI 21 · CIK 1" typed in
  by hand on 2026-06-27, eight lines under a comment bragging that the *other*
  caption is "computed from the live counts, never hardcoded." It was materially
  wrong (CCN~NPI 39 → 67) and listed NPI as backlog even though NPI had since
  gained a detector. Now derived from the cached graph — hard-ID edges only,
  minus keys a rule already covers — and fails closed (omits the caption) when the
  graph is missing. Live answer: CCN~NPI 67 · CCN 19 · BIOGUIDE 10 · CIK 3.
  Two regression tests added.

- **2026-07-31 — full spine rebuild.** Ran clean (exit 0). 22,623,285 entities
  before and after, 37,223,830 nodes — nobody merged or renumbered (ENTITY_ID is
  content-addressed). Config fingerprint re-pinned, incremental lane unblocked,
  1,041 leads restamped, zero review verdicts touched. Self-synced
  `SPINE_KEYSET_LIVE` + `CONNECT_WATERMARK`, so no separate `seed` was needed.
