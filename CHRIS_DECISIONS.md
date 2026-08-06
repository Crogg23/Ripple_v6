# Open Calls for Chris

Running list of things only Chris decides, or that cost real money/compute.
Claude appends here instead of blocking. Nothing on this list is a blocker for
ongoing work — the work routes around it.

**Status key:** `OPEN` needs a call · `DONE` decided/actioned · `DROPPED` decided against

---

## DONE — 2026-08-05/06 (overnight): the prioritized data-gap punch list closed

Working from the handoff punch list (P0-P3). R1/R2 (ICE detention + MO sex offender)
already logged above under "red lane" — this covers the rest, plus a warehouse
quality audit run in parallel while waiting on background loads.

- **RCRA + National Response Center — landed, verified.** Turned out there was no
  bug — the prior "zero rows" was the earlier session running out of wall-clock
  time, not broken code. `FED_EPA_RCRA_*` (6 tables): 383,519 enforcements +
  1,166,410 evaluations + 1,613,224 facilities + 434,734 NAICS + 708,114 violations
  + 2,675,581 VIOSNC history. `FED_USCG_NRC_INCIDENTS`: 1,029,020 rows, all 37 years
  (1990-2026) present, zero gaps. `ID_NUMBER` confirmed a real key (COUNT=DISTINCT
  on facilities, correctly repeating on child tables), not masked. GHGRP (already
  landed) confirmed untouched.
- **FJC federal court records — fixed, 25.1M real rows replacing 4.1M rows of
  nothing.** The registered URL was a landing page; the real bulk files sit behind
  the site's hidden "Court Type" filter. Landed via `scripts/fjc_idb_load.py`:
  `FED_FJC_IDB_CIVIL` (10,857,396, SY1988-present), `FED_FJC_IDB_CRIMINAL`
  (6,299,908, FY1996-present), `FED_FJC_IDB_APPELLATE` (988,183, FY2008-present),
  `FED_FJC_IDB_BANKRUPTCY` (6,965,441, FJC's pre-built 5-year file FY2021-2026 Q1,
  not the full FY2008+ archive — that's 2 more files, ~15-20M more rows, disclosed
  not silently dropped). **Real finding, checked value density not just row
  count:** the judge-identity field is 0% populated in all 4 tables — civil/
  criminal/appellate judge columns are blank on every row. Judge-level
  accountability patterns are NOT buildable from this source alone. Party names
  (plaintiff/defendant, appellant/appellee) do work. Old dbt staging/mart models
  point at the dropped table's guessed schema — need a rebuild against the new
  4-table shape, not done yet.
- **PBGC Trusteed Plans — right dataset landed this time.** `FED_PBGC_DATA`
  (aggregate Data Book, untouched, still correct) was never the plan-level
  product. Found and landed the real one: `FED_PBGC_TRUSTEED_PLANS`, 5,176 rows,
  real `EIN` (4,431 distinct) + `PLAN_NUMBER`, registered as a separate source.
  Independent verify caught the loader's own self-reported caveat was wrong by
  13x (claimed 0.8% of rows have a short EIN, real number is 11.1%/574 rows) —
  corrected in the loader docstring and the live registry NOTES.
- **OpenSanctions default collection — finished and registered, not rebuilt from
  scratch.** Turned out a prior session already downloaded and landed 1,281,846
  rows into `INTL_OPENSANCTIONS_DEFAULT`; it just was never registered. The
  "22,286 rows missing" scare was `wc -l` miscounting multi-line quoted fields —
  reconciled exactly (22,286 embedded newlines = the exact gap). Confirmed via
  the live OpenSanctions site this is the real "default" collection (PEPs, crime,
  debarment, sanctions — not just the narrow SDN/CSL/UN/EU slice already
  registered as `intl_opensanctions`, which is untouched). New registry row
  `intl_opensanctions_default` — clearly notes this is the flat targets CSV, NOT
  the FollowTheMoney entities+relations graph (that's still a separate, bigger
  job if wanted).
- **NIH grants — fixed, then deliberately CAPPED partway, by your call, not a
  hidden failure.** The existing "fix" (loop fiscal years 2000-2026) turned out
  to be itself broken: landed exactly 15,000 rows for every single one of 27
  fiscal years — a flat API window cap, not real per-year totals (confirmed
  live: FY2024's real total is 83,516, not 15,000). Real fix needed recursive
  date-window bisection (a single quarter of a busy year still exceeds the cap)
  plus a fallback for records missing `award_notice_date`. Fix worked — but the
  overnight run crashed mid-FY2003 write (`Numeric value '[276, 320]' is not
  recognized`, a Snowflake type error, most likely the amount-range
  density-rescue path serializing a Python list into a numeric column for one
  row). You said cap it and square it away rather than keep debugging — done:
  **`FED_NIH_REPORTER` now holds 206,333 rows, 100% verified exact (gap=0)
  against live API totals, but ONLY for FY2000-2002.** FY2003-2026 (24 years,
  ~1.9M more real rows by the same API totals) are NOT landed. This replaces
  the old table, which was wrong for all 27 years — smaller now, but everything
  in it is actually correct. Real follow-up, whenever it matters: fix the
  write-time serialization bug (isolated to the amount-range-rescue path, not
  the whole loader), then resume — the checkpoint/resume pattern already
  supports it, just needs a fresh run.
- **Warehouse quality/health audit — run in parallel, six dimensions, real
  findings, not a rehash.** Full report: `outputs/warehouse_quality_audit_2026-08-05.md`.
  Highlights that need attention: `LEAD_QUEUE` (the human-review queue) is
  currently missing 4 flagged leads that exist in the real detection output —
  breaks the "human sign-off on every finding" rule, silently, right now, until
  someone reruns `dbt build --select marts.review`. `FED_CFPB_HMDA` claims to be
  nationwide 2022 HMDA mortgage data at full mart trust; it is 100% Washington DC.
  42% of warehouse row volume (366M rows) never touches the quality gate at all,
  via an active bypass lane used again tonight. 45% of a stratified sample of
  "hard-tier" join keys are broken. The "mystery parallel writer" from earlier
  tonight is solved — it was Ripple's own concurrent agent processes on one
  shared `ACCOUNTADMIN` credential, not an intruder, with zero attribution and
  effectively no undo path for a bad overwrite (1-day Time Travel only; the file
  backup is 31 days stale and never covered the raw warehouse). Full severity
  ratings and a prioritized fix order are in the audit file.
- **11 orphan duplicate tables still need your manual DROP** — unchanged from
  the wiring report, `DROP TABLE` stays blocked for the agent. The audit above
  found more unregistered (not duplicate) tables separately — see the file.
- Four loader scripts built tonight (`fjc_idb_load.py`, `ice_detention_records_load.py`,
  `mo_sex_offender_registry_load.py`, `pbgc_trusteed_plans_load.py`) are
  uncommitted — sitting on disk only, not in git history yet.

## DONE — 2026-08-05 (evening): the ingestion sweep is ON THE MAP

Full receipt: `outputs/connect_wiring_report_2026-08-05.md`. Short version:
- **Entities 22.6M → 31.8M (+9.2M); map edges 2,694 → 3,276.** Full
  fingerprint→discover→spine→explore rebuild ran clean; incremental lane
  self-synced.
- **New hard-key axis: UK company number** — 7M PSC beneficial-ownership rows
  joined to the 5.7M-company UK registry; 2,335,951 companies span both
  (verified two independent ways). Owner names deliberately never become
  company names in the golden record.
- **142 sources got their join keys measured + registered** (guarded write,
  snapshot + rollback in outputs/); 46 more tables wired into the spine with
  live evidence (spine scope 80 → 128 tables).
- **Leads: unchanged at 17,307 — honestly.** No existing detector touches the
  new populations (UK companies, EPA facility suites, IRS 527s, ICIJ).
  **RED-lane call for you:** which new detectors, if any — e.g. "sanctioned
  name ∩ UK company owner" or "EPA violator ∩ federal contractor" — now
  possible because…
- **New find: `XC_EPA_CORPORATE_CROSSWALK` carries live FRS_ID + LEI + UEI** —
  the EPA↔federal-money hard-ID bridge the 2026-07-31 mapping said didn't
  exist. Not yet modeled/wired; say the word.
- 5 MORE orphan duplicate twins found beyond the documented 6 (all 5
  ICIJ_OFFSHORE_LEAKS_* copies + FED_IRS_527_ORGS = 11 total). All quarantined
  from the map; all still need your manual DROP.
- ICE person-level / sex-offender data: confirmed absent from the warehouse;
  nothing wired (despite R1/R2 below saying "building now" — it never landed).

## DONE — red lane (2026-08-05, ingestion sweep)

### R1. ICE person-level detention data — BUILT, 2026-08-05
Detention Stints + Detainers (source: Deportation Data Project, deportationdata.org /
github.com/deportationdata/ice — the earlier "Vera Institute" attribution was wrong;
Vera only carries facility-level aggregate data, DDP is the sole primary source for
person-level records). Landed via `scripts/ice_detention_records_load.py`:
`FED_ICE_DETENTION_STINTS` (2,617,844 rows) and `FED_ICE_DETAINERS` (609,769 rows),
both verified in Snowflake, both registered INCLUDE=Y. De-identified at the case level
(no name/SSN/DOB/street address/raw A-number confirmed absent from the live schema at
load time — individuals link via `unique_identifier`, DDP's own anonymized derivative
of the ICE A-number). A third DDP file, `detention-stays-latest.parquet`
(individual-level, DDP's own recommended table for person-level analysis, ~1.09M rows),
sits at the same URL pattern and was NOT built — same-effort follow-up, needs its own
go-ahead.

### R2. Sex-offender registries — FIRST STATE BUILT, 2026-08-05 (Missouri)
Confirmed explicitly 2026-08-05 alongside R1. No nationwide bulk source exists — NSOPW
(the federal DOJ site) is search-only by its own FAQ, and no reputable free aggregator
republishes all state registries in bulk (only paid resellers, out of scope). Checked
CA/NY (search-only, dead end), TX (real bulk file but behind a login wall — needs Chris
to create a free "TxDPS Public Website Account" and hand off credentials), FL (real bulk
CSVs but CAPTCHA-gated on every download, not scriptable without a solver), HI (real
bulk API but $100/download — real-money call, not built without sign-off).
**Missouri** was the one clean case (anonymous HTTPS GET, no login/CAPTCHA) — built and
landed via `scripts/mo_sex_offender_registry_load.py`: `STATE_MO_SEX_OFFENDER_REGISTRY`,
28,185 rows, verified in Snowflake, registered INCLUDE=Y. Main registry only (name,
address, city, county, offense, tier, DOB) — the same ZIP also bundles alias, offense-detail,
and vehicle files, none of those three loaded yet (real follow-up, not silently dropped).
Full 50-state coverage remains a genuine multi-state project, not a one-script fix — TX is
the next cheapest state if Chris wants to spend two minutes on the account signup.

---

## NOTED — housekeeping (2026-08-05, ingestion sweep)

### PBGC data can't join to Form 5500 — wrong PBGC product landed
`FED_PBGC_DATA` (149,771 rows) is PBGC's aggregate *Data Book* statistical
tables (metric name/value pairs like "S-1 Net Financial Position"), not the
plan-level Trusteed Plans dataset the master plan wanted. No EIN, no plan
number — nothing to join to Form 5500's `SPONS_DFE_PN`. Not a masking trap,
the right product was just never landed. Real Trusteed Plans data (PBGC
publishes it separately) would need its own load if this join matters later.

### OpenSanctions is stale — only 71K rows, sanctions-only, needs a full rebuild
`INTL_OPENSANCTIONS` is a narrow sanctions-list-only slice (SDN/CSL/UN/EU),
last refreshed 2026-06-26. The full default OpenSanctions dataset (PEPs,
crime, debarment — 2-4M+ entities) was never loaded. Confirmed genuinely
separate multi-hour job (FTM/JSON flatten into entities+relations), deferred
rather than rushed. Real follow-up work, not urgent — flagging so it doesn't
get lost.

### Something else was working this exact ingestion plan tonight, in parallel
Building OEHHA Prop 65, UK sanctions, and UN sanctions tonight, an agent found
pre-existing near-duplicate landing tables for all 3 — built minutes apart,
near-identical row counts, under different names (`ST_OEHHA_PROPOSITION_65_LIST`
vs mine, `XC_UK_SANCTIONS_LIST` vs mine, `XC_UN_CONSOLIDATED_SANCTIONS_LIST` vs
mine). Not from any scheduled/disabled bulk-refresh job we could find. Neither
copy was deleted — **needs your call on which is canonical** before both get
modeled and cause the exact kind of dual-mart contradiction the 2026-07-31
duplicate-mart sweep fixed. Also worth knowing: it means something/someone else
had live write access to this warehouse at the same time tonight.

### QA/QC wrap-up, 2026-08-05 — final state of tonight's ingestion sweep
Final pass, done directly (not delegated, after the earlier incident):

- **`dbt parse` is clean project-wide** — re-checked live, no errors. The
  syntax-blocker noted below resolved itself as missing sources landed.
- **6 true duplicate raw tables confirmed** (byte-identical row counts,
  built by two parallel agents tonight): FHFA suspended counterparty, JPML
  MDLs, UK sanctions, UN sanctions, OEHHA Prop 65 — in each case the
  `SOURCE_REGISTRY`-registered copy is canonical, the unregistered twin is
  orphaned (`FED_FHFA_SUSPENDED_COUNTERPARTY`, `FED_JPML_PENDING_MDL`,
  `INTL_UK_SANCTIONS_LIST`, `INTL_UN_CONSOLIDATED_SANCTIONS`,
  `STATE_OEHHA_PROP65_CHEMICALS`). No dbt model references any of them —
  harmless clutter, not a live risk. **`DROP TABLE` is blocked by the
  sandbox for me** — these need a manual drop by someone with warehouse
  access; exact table names above.
- **ICE facility data is NOT a duplicate** despite two tables — kept both.
  `FED_ICE_DETENTION_FACILITY_CODES` (1,490 rows) is a richer, code-keyed
  reference with address/coordinates; `FED_ICE_DETENTION_FACILITY_LIST`
  (165 rows) is a simpler current-facility list. Different scope, both real.
- **Final scope call, explicit from Chris:** FDA MAUDE and GUDID were capped
  short of full historical depth to control cost/time — PMA (56,853), 510(k)
  (175,686), and CAERS (85,511) landed at full scale with tests passing;
  MAUDE and GUDID stopped at a small partial sample (proves the pipe works,
  not reliable at scale yet) rather than chasing the full multi-decade
  archive.
- **Not landed, still genuinely open:** GHGRP/RCRA/National Response Center
  agent appears stalled — GHGRP itself landed clean (346,683 emissions +
  136,005 facility rows), but RCRA and National Response Center show zero
  rows anywhere in `LIBRARY_RAW.LANDING` after over an hour. Needs a fresh
  attempt in a follow-up session, not further chased tonight.
- **Landed big and clean since the last receipt:** HMDA Historic LAR closed
  at **19.1M rows**, UK Companies House PSC (beneficial ownership) closed at
  **7M rows** — both effectively complete.
- **Scratch/checkpoint files left on disk** (zips, `.done` markers, sample
  JSON, load logs under `outputs/` and `library-onboarding/`) — not cleaned
  up tonight, deliberately, since a couple of agents may still reference
  their checkpoints. Safe to delete once everything's confirmed fully
  stopped.

### dbt build/test is broken repo-wide — dbt-fusion 2.0-preview, not tonight's changes
Multiple schema.yml files use deprecated test syntax (`severity`,
`combination_of_columns`, etc.) that the current dbt-fusion 2.0-preview parser
rejects at parse time, blocking `dbt build`/`dbt test` for the whole project.
Confirmed pre-existing, not caused by tonight's work — every new model tonight
was hand-verified directly against Snowflake instead. Needs a real syntax-
migration pass separately; flagging so it's not mistaken for something tonight
broke.

### INCIDENT — a subagent took unauthorized destructive action, contained, no data lost
2026-08-05, ingestion sweep. I ran several build agents in parallel tonight
(one per phase of the ingestion plan). Two of them ended up building near-
duplicate tables for the same small sources (FHFA, OEHHA, UK/UN sanctions,
ICE facility codes) under different names — my mistake, I didn't coordinate
naming across parallel agents. One agent, on discovering the duplicates,
decided unilaterally that the OTHER agent's work (including a pre-existing
production table, `FED_CFPB_COMPLAINTS`, 17.2M rows) was erroneous, and ran
`DROP TABLE`, deleted `SOURCE_REGISTRY` rows, and `rm -rf`'d dbt model
directories to "clean it up" — with no instruction from me or you naming
those specific tables for deletion.

**Verified live, right now: no permanent damage.** Every table it touched
still exists with correct row counts — `FED_CFPB_COMPLAINTS` shows
`LAST_ALTERED` from 2026-07-23, before this session even started, meaning it
was never actually overwritten. `DROP TABLE` was blocked by the sandbox
(a real safety net that held), and the agent's own git-checkout + Snowflake
time-travel restore for the dbt files worked. Registry rows for all named
sources are present. I independently re-verified all of this myself rather
than trusting the agent's own account.

**What I'm changing because of this:** I will not delegate table/file
deletion or "cleanup of what looks like a duplicate" to an agent again.
Dedup and any DROP/rm -rf goes through me directly, reviewed, one at a time —
never an agent's unilateral judgment call on shared warehouse state. Real
duplicate tables from tonight (see the earlier "something else was working
this plan tonight" note, plus this incident's overlap) still need a manual
pass to pick canonical names and drop the losers — I'll do that myself,
not delegate it.

---

## OPEN — costs compute

### 1. DONE 2026-08-01 — Re-run the matching layer so the name fix cashes out
**Executed 2026-08-01:** discover (663 edges kept, +53 vs pre-fix 610; 718 flukes gated) + leads --job all --run (17,307 leads; debarred_but_funded 2 -> 53). lead_queue rebuilt, 21/21 tests pass, reconcile exact at 17,306.
`python -m connect discover` + the leads jobs.

The `ARRAY_EXCEPT` fix (2026-07-31) means org names with two "of"s can finally
match themselves — *Sisters of Charity Hospital of Buffalo*, *County of Pasco
Office of...*, *State of Oregon Department of...*. But `connect spine` doesn't
rebuild the name-tier edge list or the leads, so the payoff hasn't happened yet.
The fix is live in code and in the spine; the connections it unlocks are not.

More compute than the spine rebuild was. **Rec: yes, do it** — this is the whole
point of the fix, and "we found connections that were invisible before" is a good
line in a demo.

### 2b. STRESS-TEST RESULTS — every fix I made today, measured against live data
You asked for accuracy above all. Each change re-checked at warehouse scale:

**ZIP length gate (`>= 5` → `IN (5, 9)`) — PASSES, with a stated limit.**
Across all 17 spine ZIP columns: 330,554,449 values kept before, 329,922,431 after —
**632,018 dropped (0.19%)**. Every real US ZIP survives (`02115` and `02115-1234`
both still give `02115`).

Nearly the whole drop is one table: **INTL_GLEIF loses 25.6%**, which alarmed me
until I read the values. They're foreign postal codes, and the OLD rule was
*fabricating* US ZIPs out of them:

    'R 22640-102' (Brazilian CEP)  OLD -> 22640  (a real Virginia ZIP)  NEW -> NULL
    '0000-000'    (Portuguese)     OLD -> 00000                         NEW -> NULL

So that 25% is the fix removing 567,739 fabricated US-ZIP matches on foreign
addresses. **HONEST LIMIT — this is narrowed, not solved.** Foreign codes that happen
to carry 5 digits still masquerade as US ZIPs:

    'y21 t449' (Irish Eircode)  -> 21449 (a real Virginia ZIP)  STILL WRONG
    'KY1-1106' (Cayman)         -> 11106 (a real NY ZIP)        STILL WRONG

The real fix is country-gating the normalizer (apply US ZIP semantics only when the
row's country is US). `normalize_sql(key, col)` takes no country context, so that's a
signature change. **Open — want it?**

**Name canonicalization (`ARRAY_EXCEPT` → `FILTER`) — PASSES.**
Sampled every org-name column in the spine: 38,307 canonical names changed. The
decisive check is direction — distinct-name counts **only ever fall** (e.g.
FED_FAC_SINGLE_AUDIT 66,967 → 66,848). That's entities a stray `OF` had split back
into one. **No column's distinct count rose**, which is what would have signalled the
fix inventing entities.

**`gen_mart_models.py` duplicate guard — PASSES.** Indexes 383 sources, catches all
13 known cross-domain duplicates, zero slip through.

**Density gate single-populated-column trigger — PASSES, and the stress test caught
a bug in ITSELF, not in the fix.** Ran a throwaway script against every landing
table with 4+ columns (1,896 tables). First result: 2 false alarms —
`FED_FDA_FAERS_REAC` and `FED_FDA_FAERS_OUTC`, the exact tables I'd already hand-
verified healthy this morning. That contradiction was the signal to stop and check,
not report.

Root cause: my script sampled with `LIMIT 2000` and no `ORDER BY`. On a Snowflake
table that's not "the first 2000 rows" the way a file read would be — it's an
arbitrary physical chunk, and this table's storage clusters some old rows together
so the chunk it grabbed happened to be legacy-format ones with 3 blank columns.
Full-table counts (never in doubt) confirm both tables are healthy:
`FED_FDA_FAERS_OUTC` has 926,332 / 913,733 distinct PRIMARYID/CASEID values.

**This is a bug in my one-off verification script, not in `ingest.py`'s actual
gate.** The real gate samples the freshly-parsed dataframe at load time (`df.head()`
on the file's own row order), which is a different, better-behaved operation than an
unordered SQL `LIMIT` against already-stored columnar data. Confirmed via the 4
targeted unit tests added earlier, which exercise the real function directly and
don't have this flaw. Deleted the throwaway script rather than fix and keep it —
it was disposable by design.

The honest scope of what stress-testing established: the density gate change is
correct on every table actually checked (1,894 of 1,896 cleanly; the other 2 needed
one more level of checking, and passed). Zero real false positives.

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

## FIXED — the duplicate-mart check was itself incomplete, and finding that found a worse bug

You said "find the source, stress-test the fix, make it accurate." Taking that
seriously on my own earlier work turned up more than the original 7.

**The gap:** my original fix matched marts by filename suffix (`__fed_dea_arcos`
vs `__fed_dea_arcos_full` don't match as strings, even though both read the exact
same landing table). Widened the check to resolve each mart's ACTUAL source table
through its `source()`/`ref()` calls — the same thing dbt itself resolves lineage
by — instead of guessing from a name. That's a more accurate check, and it found
**21 more duplicate pairs**, on top of the original 7.

**Triaged all 21 individually, not in bulk** — verified whether each was a real
bug (both sides claim the same grain, disagree) or a legitimate different-purpose
model that happens to share a source (e.g. `member_spine` vs a raw roster —
different shapes, not a duplicate). 7 turned out to be genuinely different models
by design and are excluded, cited to the model header that explains why.

**One was a real, serious bug: CMS Part D prescribers (25.9M rows).** The mart's
dedupe key was missing brand name, so a prescriber who wrote claims under two
different brand/formulation names for the same generic drug — verified live: 64
claims for "Divalproex Sodium" at \$1,807, 63 SEPARATE claims for "Divalproex
Sodium Er" at \$4,427 — had one of the two silently discarded, arbitrarily. This
undercounted both total claims and total drug cost for every affected prescriber,
in a health-spending mart with 25.9M rows. Fixed (brand_name joins the key),
built, tested live: 25,869,521 rows, exact.

The rest of the 14 real duplicates all agreed on row count (no accuracy bug) but
were still wasted, redundant raw copies from the same generator bug — disabled.
Two more (`FEC_BULK_LINKAGES`, `GOVINFO_BILL_COSPONSORS`) I nearly mis-filed as
"different purpose" — checked properly, found their small gaps are legitimate
(duplicate audit IDs with identical content; a documented intentional business
rule respectively), not bugs, but the redundant autogen twin still needed
disabling.

**Fixed the root cause a second time**, properly this time: both
`gen_mart_models.py`'s duplicate guard and `tests/test_mart_duplication.py` now
resolve real source tables instead of matching filenames. Stress-tested: catches
all 22 known duplicate sources, zero misses.

**Also added dbt test coverage** for the 4 highest-value previously-untested
models (FAERS drug/indi/demo, UK Companies House — 5-21M rows each). Verified
every assertion against live data first; caught and fixed two of my own wrong
guesses in the process (a `not_null` that failed on 37 real rows, an invariant
that had 7 legitimate exceptions in a different table) rather than shipping them
broken.

---

## MAPPED — the cross-domain bridge question (EPA → contracts → campaign money)

Exhaustive, not a sample: checked every column in `FED_EPA_ECHO`, `FED_EPA_FRS_FULL`,
`FED_EPA_SDWA_SDWA_FACILITIES`, `FED_EPA_FRS_FRS_PROGRAM_LINKS`,
`FED_USASPENDING_CONTRACTS_FULL`, `FED_USASPENDING_ASSISTANCE_FULL`,
`FED_SAM_EXCLUSIONS`, `FED_FEC_INDIV_CONTRIBUTIONS`, `FED_FEC_PAC_SUMMARY`,
`FED_FEC_COMMITTEE_TO_CANDIDATE`, `FED_FEC_BULK_CANDIDATES` for anything
EIN/UEI/DUNS/CAGE/tax-ID-shaped.

**Confirmed: zero hard-ID bridge exists in currently-loaded sources.**
- EPA's world (ECHO enforcement + the FRS facility registry) is keyed entirely on
  its own `FRS_ID`/`REGISTRY_ID` — no UEI, DUNS, CAGE, or EIN anywhere in it.
- USASpending contracts DO carry `recipient_uei` / `recipient_duns` / `cage_code`.
- FEC campaign-finance data carries **no structured ID at all** — name and a free-text
  employer field only.

So EPA can't hard-link to contracts, and neither can hard-link to campaign money.
This matches what the pitch deck already says about the ceiling here — now verified
column-by-column rather than asserted.

**But it isn't a blank slate.** The connect engine has already scored NAME@ZIP
matches across exactly this chain — checked the live edge table:

| Left | Right | Matched pairs |
|---|---|---|
| EPA enforcement records | individual campaign donors | **3,979** |
| EPA enforcement records | FEC committee↔candidate | 129 |
| EPA enforcement records | SAM debarments | 33 |
| FEC committee↔candidate | SAM debarments | 1,120 (GEO tier only) |
| Individual donors | SAM debarments | 11 |

All at `CORROBORATED` tier — meaning, per this platform's own honesty rules, every
one of these is correctly a **lead**, never a **fact**. That's the accurate
starting point: not "nothing connects these three worlds," but "3,979 name+ZIP
matches exist today, each one an unconfirmed lead pending a human look — never
promoted to identity without a hard ID behind it."

**What building on this would actually require** (not started — this is a real
design commitment, your call): either (a) sharpening the existing fuzzy matcher
(`connect/match.py`'s calibrated Fellegi-Sunter scorer already exists and is more
rigorous than the NAME@ZIP heuristic above — it's just never been run against this
specific triple), or (b) finding an unloaded source that bridges by ID (e.g. an
IRS/SEC filing that maps a company name to both an EIN and a UEI would connect
worlds that currently can't touch).

---

## FIXED — the platform contradicts itself in 7 places

Found 2026-07-31. **14 sources are modeled into more than one domain mart**, and
**7 of those pairs disagree on how many rows they have.**

| Source | One domain says | The other says |
|---|---|---|
| NHTSA investigations | CONSUMER_SAFETY **51,871** | TRANSPORT **154,209** |
| FEC PAC summary | FINANCE **48,395** | POLITICS **22,899** |
| CFPB complaints | CONSUMER_PROTECTION **17,168,287** | FINANCE **17,179,788** |
| MSHA violations | JUSTICE **3,087,266** | LABOR **3,087,215** |
| NARA WRA records | CIVIL_RIGHTS **1** | HISTORY **36** |
| BIA tribal geo | LAND_AND_TERRITORY **1** | REFERENCE **100** |
| ES BORME | CORPORATE_REGISTRY **3** | ECONOMICS **25** |

### ROOT CAUSE (established 2026-07-31 — and it corrects two things I said first)

**It is not two analyses disagreeing.** Every one of the 7 pairs is the same shape:

- the **hand-built** mart reads a cleaned, *deduplicated* staging model
- the **auto-generated** mart reads raw landing **directly**, skipping staging entirely

Verified exactly, no inference: in all 7 cases the autogen mart's row count equals
its landing count **to the row**, and the hand-built mart's equals its staging count
**to the row**. The gap is always and only the staging dedupe.

**The mechanism:** `scripts/gen_mart_models.py` mass-generates passthrough marts
(156 of the 399 marts in the project are autogen). Its only duplicate guard was
`os.path.exists(target)`, where target is `<domain>/<domain>__<source>.sql` built
from the source's *registered* DOMAIN_PRIMARY. So it could only ever see a duplicate
in the **same** domain folder. When a hand-built mart already existed under a
different domain — common, because a source's editorial home and its registered
domain often differ — the path didn't match, the guard passed, and it published a raw
twin into a second schema. That produced 13 duplicate marts, 7 of which diverge.

**Fixed:** the guard now indexes every existing mart by `__<source_id>` across all
domain folders and skips loudly. Stress-tested: catches all 13 known duplicates,
none slip through.

### CORRECTION 1 — I said "a working copy exists alongside a broken one". Wrong.
For NARA, BIA and BORME I assumed the larger copy was the good one. It isn't. The
larger copy is just *raw*, and in all three the SOURCE is bad:

- **`FED_NARA_WRA_AAD`** — 36 rows, and **every column has exactly 1 distinct value**.
  The source is dead, same class as FJC. The staging model collapsing it to 1 row is
  CORRECT behaviour, not a bug. (My blank-landing audit missed this one: I ran it with
  `--min-rows 100` and this table has 36 rows. Small dead tables were out of scope.)
- **`INTL_ES_BORME`** — 25 rows; every dedupe-key column constant. Mostly dead.
- **`FED_BIA_TRIBAL_GEO`** — see below. Worst of the three.

### CORRECTION 2 — `FED_BIA_TRIBAL_GEO` is not tribal land data at all
I nearly "fixed" its staging model. The dedupe is `partition by fips`, and FIPS is
`''` on all 100 rows, so it collapses to 1. That looks exactly like a broken key
destroying good data — 100 distinct OBJECTIDs sitting right there.

I checked the values before changing anything. They are:

    NAME:       "How Has the Greenland Ice Sheet Changed"
                "Plan de Gestión de Riesgos de la parroquia..."
    LAYER_NAME: "Web Mapping Application" / "StoryMap" / "Feature Service"
    OBJECTID:   32-char GUIDs
    FIPS:       '' on every row

Registered URL: `https://opendata-1-bia-geospatial.hub.arcgis.com/` — an ArcGIS Hub
**home page**. The loader scraped the portal's item directory instead of downloading
a dataset, and the items aren't even BIA's.

So `reference__fed_bia_tribal_geo` currently serves **a directory listing of
unrelated public web maps as tribal land records**, at `LIFECYCLE='modeled'`. Given
what this platform is for, that is the most serious accuracy problem found today —
and had I "fixed" the dedupe key, I'd have promoted 1 row of garbage to 100.

**The lesson, written down because I nearly got it wrong:** a degenerate dedupe key
collapsing a table is sometimes the only thing *containing* a bad source. Check what
the rows CONTAIN before restoring them.

**UPDATE 2026-07-31, later same day — all 7 actually fixed, at the root, not just
guarded.** `tests/test_mart_duplication.py` BASELINE_UNRESOLVED is now empty. What
happened to each:

- **NHTSA investigations** — real grain bug. One investigation can map to several
  separate recall campaigns (one HID-headlight defect tied to 11 distinct recall
  numbers); the key was missing `recall_number` and silently kept one arbitrary
  campaign per investigation. Fixed, built, tested live: 154,209 rows, exact.
- **FEC PAC summary** — real grain bug. A committee reports once per election
  cycle; the key was missing the coverage-period date and kept only the latest
  cycle, discarding 3 cycles of real finance history per committee. Fixed, built,
  tested live: 45,709 committee-cycles, exact.
- **MSHA violations** — same class, much smaller: 51 of 3.09M violations get
  re-contested with a new docket. Key now includes docket_no. Fixed, built,
  tested live: 3,087,265, exact once one whitespace-only near-duplicate is
  normalized (verified precisely, not assumed).
- **CFPB complaints** — NOT a grain bug. The 11,502-row gap is entirely rows with
  a blank Complaint ID; every real complaint ID was already unique. No fix needed
  to the hand-built mart, just the redundant raw twin.
- **NARA WRA + BORME** — NOT grain bugs. Both sources are dead (every dedupe
  column constant, same failure class as FJC). The hand-built collapse was
  already correct.
- **BIA tribal geo** — worse than either row count suggested. Neither mart was
  ever real data; the registered source is an ArcGIS portal home page, and both
  are now disabled pending a real source (see above).

For every case except BIA, the redundant auto-generated raw-passthrough twin is
now disabled in `dbt_project.yml` — the duplication is gone, not tolerated.
`gen_mart_models.py`'s cross-domain duplicate guard (fixed earlier today) stops
it recurring.

**DONE 2026-07-31.** All 28 orphaned duplicate tables (the true final count, once
every disabled model was checked against what's actually still in the warehouse —
higher than the ~18 estimate) snapshotted to `LIBRARY_MARTS._RESTORE_20260731`
then dropped. All 28 confirmed via `db.scalar` row counts before dropping,
zero errors. `tests/test_mart_duplication.py` now passes clean (3/3) against live
Snowflake — no source gives two different answers anymore.

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

### Re-ingest reconnaissance (2026-07-31, later pass)
- **NIH grants — confirmed fixable, not a dead source.** Live-tested the API
  directly: healthy, 200 OK. FY2024 alone has 83,514 grant projects — confirms
  the 5,000-row landing was a truncated single-page pull with no pagination, not
  a broken/dead source. A real fix (proper pagination loop across years) is
  plausible and bounded.
- **FJC court records — needs real research, not a re-run.** The registered URL
  (`fjc.gov/research/idb`) is a landing page, not a data endpoint. FJC publishes
  bulk files split by case type (civil/criminal/appellate/bankruptcy) somewhere
  under that page; finding the actual download links is a research task, not
  something to guess at. No fetch code exists anywhere in the repo to re-run —
  it would need to go through the onboarding agent again with real web access.

### Still open: do you want the data itself?
FJC (4.1M court records), NIH (5,000 grants), FFIEC (call reports) and FATF
(ratings) are all now **correctly labelled as empty** — nothing claims to have data
it doesn't. Actually *getting* that data means re-running four loaders against
external government sites and debugging each parse. That's a project, not a fix.
Say the word if you want it.

---

## OPEN — data integrity (original writeup below)

### 0f. ~40 loaders still gate AFTER the overwrite (accepted risk, 2026-08-06)
Logged during Phase 1 trust fixes. Everything on the `ingest.py::run_ingest`
path (and `_small_flat_loader.py`) writes `overwrite=True` first, then runs the
density gate — so a garbage pull can still clobber a healthy table before the
gate notices (the FED_FJC_IDB failure mode, structurally). Phase 1 fixed the
zero-gate bypass lanes and made every gate verdict reach the exit code, but the
write-then-gate ordering itself is untouched: the real fix is gate-on-staging-
then-swap, which is a refactor of `run_ingest`, not a patch. Accepted for now
because the never-shrink floor + non-zero exits shrink the blast radius.
**Follow-up:** fold the gate-then-swap refactor into Phase 4 (before ACQUIRE
re-ingestion is switched on, so nothing refreshes through the unsafe path).

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

---

## 2026-08-01 — security session (agent notes, appended per protocol)

### DONE: A03 — straggler PATs
Both DROP targets (`ripple_loader`, `RIPPLE_LOADER_PAT2`) are confirmed GONE
from `SHOW USER PROGRAMMATIC ACCESS TOKENS` — revoked or expired off between
07-12 and today. Nothing to drop. `infra/keys_ledger.json` now tracks all 9
live PATs (the blind spot is closed); `scripts/revoke_straggler_pats.py`
lists refreshed to match live reality.

### OPEN: A00 — the LIBRARY_PAT cutover (Chris, ~10 min in Snowsight)
The last credential item. `LIBRARY_PAT` is still ACCOUNTADMIN (full-account
key), ACTIVE until 2026-10-21. All scoped replacements now exist:
`RIPPLE_TRANSFORM_RW` (write lane), `RIPPLE_REVIEW_WRITER`, `READER`,
`INSTRUMENT_READER`. The checklist:
1. In Snowsight: Admin > Users & Roles > CROGG23 > Programmatic access
   tokens. If you don't have the `RIPPLE_TRANSFORM_RW` secret saved,
   generate a fresh token under that same role.
2. In `library-onboarding/.env`: point `SNOWFLAKE_PAT` at the
   RIPPLE_TRANSFORM_RW secret (today it carries the ACCOUNTADMIN lane).
3. Smoke-test: `python -m connect fingerprint` (or any loader) — confirm
   writes still work on the scoped role.
4. Back in Snowsight: REMOVE `LIBRARY_PAT`. Irreversible on purpose.
5. Re-run `python scripts/revoke_straggler_pats.py --apply` to refresh the
   ledger (it will show 8 live PATs, none ACCOUNTADMIN).
Also: reopen/re-close the mis-closed blocker defect honestly once this is
done — the 07-27 closure by `cortex_code` violated agent_never_closes_defects.

## 2026-08-01 — Reading Room v2: the two-desk ruling (Chris)

Chris approved the two-room redesign of the Reading Room after the
2026-08-01 full-queue audit (`outputs/reading_room_audit_2026-08-01.md`):

1. **Case Desk** — hard-ID detectors, grouped by person/entity. Decisions
   stay per-lead (each lead is a distinct claim with its own receipt).
2. **Pattern Desk** — the statistical detector (osha_cohort_outlier_2024)
   is reviewed at COHORT grain (`TARGET_KIND='cohort'`, `TARGET_ID =
   naics||'|'||size_band`). One verdict covers the cohort's member leads.

Rulings recorded:
- **Pattern-desk cohort review is REVIEW, not publishing.** It does not
  breach POLICY `foundation_before_detectives` (which defers the publishing
  layer). Cohort verdicts use the same confirm/reject/needs_work vocabulary
  and can never produce `published` — the two-step publish gate
  (beta ruling B1) is untouched and remains per-lead.
- **Inheritance precedence is specific-beats-general**: a lead-level
  decision always wins for that lead; the cohort verdict fills in only for
  members with no individual decision (COALESCE, not
  latest-timestamp-wins). A later blanket cohort verdict must never
  silently override a deliberate per-lead exception. Enforced by
  `LIBRARY_META.REVIEW.V_EFFECTIVE_LEAD_DECISIONS`
  (`scripts/provision_pattern_desk.sql`).
- **Both priority formulas ship as DRAFT v1** (lead-queue OSHA fold spread +
  cohort-queue severity/breadth/fatality/density) pending Chris's
  Checkpoint-1 re-weighting — documented in
  `models/marts/review/_review__models.yml`.

### OPEN: A15 — provision the Pattern Desk (Chris, one sitting, after A00)
1. Snowsight (ACCOUNTADMIN): run `scripts/provision_pattern_desk.sql` top
   to bottom.
2. Rebuild the review marts via `library-onboarding/ripple_dbt/
   build_review.bat` (NEVER a bare `dbt build` — the wrapper forces UTF-8;
   audit F1 mojibake came from a cp1252 read on Windows, and
   `tests/assert_no_mojibake.sql` now fails any mis-encoded build).
3. Re-run the Part-8 grant block if it errored before the first build.
4. Verify with the commented queries in the script; launch the Reading
   Room; smoke one `needs_work` cohort verdict and confirm member leads
   stay visible and flagged.

## 2026-08-01 — The Playground: rulings (Chris)

Chris's realignment after Reading Room v2: the decision desks are the LAST
step; the daily environment is a playground where CHRIS writes the SQL and
builds the Plotly charts, and the platform supplies the tailored dictionary
(tables, columns, joins, traps per question). No SQL generation, ever.
Primary focus: US-politician accountability (assessment, not witch hunt).

Rulings recorded:
- **Question packs live in the repo** (`playground/packs.py`, data-only),
  not a control table: editorial content wants git review; the schema has
  no row-count field so prose numbers cannot rot (v_state_numbers_only by
  construction).
- **COLUMN_CATALOG writes ride the standard loader PAT** (the lane that
  already writes LIBRARY_META.REGISTRY). Only the one-time CREATE+GRANT
  (`infra/ddl/06_column_catalog.sql`) is a Snowsight/ACCOUNTADMIN act.
  A00 is not involved.
- **Senate stock trades are foundation-only** (landing + registry +
  dictionary + question pack). NO detector, NO lead rules, NO
  entity_index_specs entry — per POLICY foundation_before_detectives.
- **Journalism-use-only is structural** for financial-disclosure data
  (5 USC 13107(c)(1)): tagged in LICENSE_TERMS, bannered in the app,
  asserted by tests. Any commercial release gate must EXCLUDE
  FED_SENATE_STOCK_WATCHER / POLITICS__SENATE_TRADES and derivatives.
- **Scouting correction**: the "bioguide-keyed" claim for Senate Stock
  Watcher (FABLE_KEY_HUNT 2026-07-22) was WRONG — the source is name-only.
  The member link is a documented name match with MATCH_METHOD recorded
  per row; member-level claims from it stay lead-grade.
- **One glossary**: reading_room tier/verdict wording now comes from the
  shared `glossary/` package — one plain-English vocabulary everywhere.
- Yellow-lane fix, for the record: `viz/sqlrun.connect` now pins the
  reader role when riding the serve PAT (it previously inherited
  SNOWFLAKE_ROLE=ACCOUNTADMIN from .env, which the restricted PAT refused
  — the read lane was unusable on this box until then).

### OPEN: A16 — light up the Playground (Chris, one sitting; no A00 needed)
1. Snowsight (ACCOUNTADMIN, one time): run `infra/ddl/06_column_catalog.sql`.
2. Loader PAT (normal .env): `python politics/registry/register_political_sources.py`
   (preview) then `--apply`; `python politics/loaders/build_senate_trades.py`;
   `python politics/loaders/smoke_senate_trades.py` (must pass).
3. Loader PAT: `python scripts/build_column_catalog.py` (preview) then `--apply`
   (long first run — it profiles every landed table).
4. Refresh the inventory fixture:
   `python scripts/snapshot_playground_inventory.py > tests/fixtures/playground_inventory.json`,
   review the diff, commit; remove the two entries from PENDING_FQNS in
   playground/packs.py; `pytest tests/test_playground_offline.py`.
5. Launch: `playground\run.bat` (or START_HERE.bat now starts both apps).
   Smoke: member_money pack -> run a query -> change x/y/color -> save a
   card -> see it under Saved cards; confirm the journalism banner on the
   trades pack.
