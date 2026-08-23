# Quick-Wins Fix Session — Results (2026-08-22, evening)

*Working through `fix_session_plan_next.md` (Phases 1–5). Full receipts below;
the chat close has the short version. Counts in this file were verified live
against the warehouse during the session.*

---

## Phase 1 — free wins

| item | result |
|---|---|
| Duplicate NCHS drug-poisoning table | **DROPPED** (the one drop the permission gate allowed this session) |
| dbt test suite really runs? | **YES — 4,831 tests executed** (fix-list #21 said 505; the suite is 10x bigger than believed). Failure tally at the end of this file. |
| Dead ID columns labeled | **Done, durably**: new control table `LIBRARY_META.REGISTRY.COLUMN_TRUST` with **171 dead columns** (from `outputs/dead_id_columns_triage_2026-08-11.md`, which supersedes the fix list's "104" — 193 total minus 22 already repaired on 08-11). Plus 2 trap columns added later (see Phase 4). |

## Phase 2 — dedupe pass (all verified to exact predicted counts)

| table (landing) | before | after |
|---|---|---|
| FHFA mortgage stats (NMDB) | 19,054,246 | **11,648** |
| ForeignAssistance.gov | 3,967,456 | **95,658** |
| EPA Title V certifications | 2,574,815 | **499,113** |
| Google political-ad creative map | 4,773,180 | **971,029** |
| NHTSA recalls | 242,993 | **241,861** |

Notes:
- **Three of the four downstream marts were already clean** (Title V, Google,
  ForeignAssistance) — the duplicates landed in RAW *after* those marts were last
  built. Only the FHFA mart was stale (held 7,204 rows; real deduped data is
  11,648 — new periods arrived since). Rebuilt this session.
- **NHTSA "mass duplication" was mostly a false alarm**: rows are unique at the
  record-id level; the real dup was 1,132 rows (0.5%) of identical content under
  different record ids (e.g. one tire recall × 8 copies). The rest of the
  multiplicity is the source's own grain (campaign × vehicle × component).
- **Found and verified: a whole duplicated EPA table family.** The 5
  `FED_EPA_ICIS_ICIS_AIR_*` tables are byte-identical twins of the
  `FED_EPA_ICIS_AIR_ICIS_AIR_*` family (hash-verified on all data columns), and
  NOTHING in dbt references the orphan prefix. Drops are queued for Chris (~6M
  redundant rows).

## Phase 3 — epoch dates (both items were already fixed; verified live)

- **CFTC (fix-list #12): already fixed and rebuilt.** Both marts live-checked:
  zero epoch dates, ranges 1986→2026 (futures) and 2013→2026 (financial).
- **FAA (fix-list #11): the live replacement table is healthy** — tail-number key
  0% blank (315,447 unique), no epoch corruption (the 83 / 2,325 rows in 1970 on
  cert/airworthiness dates are real 50-year-old aircraft, re-verified 08-18).
  The defect described in the fix list belongs to the RETIRED July twin, which
  was still live in repo + warehouse. This session: disabled its 3 model files
  (`transport__fed_faa_registry` mart/staging/timeline, `enabled=false` with
  retirement headers), gutted its 2 test ymls, removed its union block from the
  transport timeline index and its row from the clock-registry seed. Warehouse
  drops queued for Chris.

## Phase 4 — the four investigations

- **Mine deaths (fix-list #7): FALSE ALARM — already repaired.** Live marts:
  1,208 fatalities correctly flagged, 814,410 S&S violations flagged, 6,631
  active mines, coordinates populated. The July quote-corruption defect was
  fixed in a prior repair session; the fix list carried the stale claim.
- **NCUA (fix-list #6): ALREADY FIXED.** The correct call-report files (FOICU +
  FS220, 4,336 credit unions each) are landed AND their marts are built and
  live. The wrongly-loaded landing table is already gone. Only residue: the
  orphan garbage mart `FINANCE.FINANCE__FED_NCUA_CALL_REPORTS` (121,713
  dictionary-sheet rows, no model behind it) — drop queued for Chris.
- **EPA penalty stamping (fix-list #4): FIXED in the model.**
  `environment__fed_epa_echo` now adds `last_penalty_amt_allocated` (splits each
  settlement evenly across the facilities sharing the same amount + same penalty
  date — the same-case fingerprint measured in the July sweep: $2.27B phantom →
  $13.5M real on the strictest grain) and `last_penalty_shared_facility_n`.
  Raw column untouched; `epa_penalty_gap` passes both through. Registered in
  COLUMN_TRUST as `case_level_stamped`.
- **SEC 13F units (fix-list #8): FIXED in the model — simpler than planned.**
  No per-filer heuristic needed: the eras are cleanly file-separated (verified
  live: per-file median value 500–1,200 for every 2013q2–2022q3 file vs
  300k–460k for every 2024+ file — an exact 1000× split on the SEC's Jan-2023
  rule change). `finance__fed_sec_13f_holdings` (a view — free rebuild) now
  carries `value_usd` (all whole dollars) + `value_unit`. Registered in
  COLUMN_TRUST as `mixed_units`. Coverage hole 2021q3–2023q4 confirmed (no
  files) — that's a completeness item, not a unit item.

## Phase 5 — batch cleanup

**openFDA "8 wiped raw tables" (fix-list #13): FALSE ALARM — nothing was ever
wiped.** These are VARIANT chunk tables: their row counts are CHUNK counts, and
the records live inside each chunk's results array. This is the exact
rows≠records trap the 2026-08-11 session itself documented after being burned
by it. Verified record counts (SUM(ARRAY_SIZE(RAW:results))), all healthy:

| raw table | "rows" | actual records | matches |
|---|---|---|---|
| CAERS | 1 | 85,511 | mart exactly |
| Drug enforcement | 1 | 17,876 | mart +60 (fresher) |
| Device classification | 1 | 7,087 | healthy |
| Device enforcement | 20 | 39,635 | mart exactly |
| MAUDE | 1,386 | 2,738,498 | mart (2020Q1+ cap) |
| Establishment reg | 166 | **330,251** | publisher's 333k |
| GUDID | 2,542 | 5,083,948 | spec's 5.08M |
| 510K | 88 | 175,686 | healthy |
| PMA | 29 | 56,853 | mart exactly |

Consequences:
- **No re-downloads needed; the four `--force` one-liners are withdrawn.**
- A server-side refresh was launched before this was understood; it re-landed
  4 small sources (harmless — same content, drug enforcement slightly fresher)
  and was **stopped mid-fetch on MAUDE** (table untouched; ~19 of 184 part
  files sit staged for reuse by any future refresh).
- **The "establishment registrations short (263k of 333k)" claim is mart-side,
  not raw-side**: raw holds 330,251 records; the mart flattens to 263k →
  rebuilt this session to close the gap.
- **The "device events 2.7M of 25.7M" claim is the documented 2020Q1+ scope
  cap** (184 of 362 part files, a deliberate bound recorded in the spec) — a
  full-history pull is a priced decision, not a defect.
- The three 1-row `*_EVENTS` stubs (MAUDE_DEVICE_EVENTS, CAERS_FOOD_EVENTS,
  FAERS_DRUG_EVENTS) were checked individually: genuinely failed first-page API
  loads holding one flat record each — junk, superseded, on the drop list.

**Remaining dup tables (fix-list #16):** measured all candidates exact-dup on
data columns (+ source-file, so per-cycle snapshots survive):

| table | before | after | dup was |
|---|---|---|---|
| CourtListener financial disclosures | 108,770 | **70,776** | 34.9% |
| EPA NPDES informal enforcement | 826,867 | **478,855** | 42.1% |
| FEC candidate master | 33,506 | **27,095** | 19.1% |
| FEC committee master | 78,039 | **60,031** | 23.1% |
| PBGC single-employer data | 149,771 | **140,454** | 6.2% |
| UK FCDO sanctions list | 58,104 | **2** | see below |

- Clean (0–1.1% dup, no action): all 7 CourtListener disclosure detail tables,
  FEC bulk candidates/committees, committee-to-candidate, both PBGC trusteed
  tables, the OFSI UK sanctions pair, **DHS immigration stats (the fix list's
  "77% dup" is stale — 0% today)**.
- **UK FCDO list was garbage from birth**: one mis-parsed column (the CSV's
  title row became the header), 2 distinct values repeated 58k times — even
  counting load metadata, the pre-dedupe table had exactly 2 distinct rows.
  Nothing real was lost; needs a loader fix + re-pull (backlog item). The OFSI
  consolidated list (57,231 distinct rows) is the live UK sanctions source —
  note the `INTL_` and `XC_` copies have identical counts but DIFFERENT content
  (different snapshot vintages), so they are not drop-twins.
- **Deliberately skipped: FAERS outcomes.** Its "78% duplication" is the
  column-shift corruption artifact (the distinguishing key was shifted out of
  its column) — deduping would delete real adverse-event records. Belongs to
  the FAERS reload session, not a dedupe pass.

**The 16 scan-errored tables (fix-list #28): ALL CLEAR.** Every error was the
old scanner's own client-side integer-conversion bug (`Python int too large` /
`ordinal must be >= 1`), not data damage. Re-probed all 16 server-side: worst
exact-dup rate 0.2% (ICIJ relationships); ICIJ ×6, OpenSanctions, ICE detainers
+ stints, both SEC fund tables, EIA, CourtListener investments, NIH RePORTER,
EPA FRS, CPSC NEISS — all duplication-clean.

## dbt test suite — first verified full run

**FINAL: PASS 4,646 · WARN 132 · FAIL 53 · of 4,831 total** (the "505
uniqueness tests" figure was a 10x undercount — the suite is real and it runs).

Failure characterization (checked, not guessed): the biggest failures are
**wrong-grain test declarations, not dirty data**. The landing tables behind the
top five (CDC NNDSS weekly 659k, PBGC 134k null years, Ember electricity 84k,
USGS water 74k, NHTSA investigations 38k, NPDES SIC codes 21k) were all measured
0.0% exact-duplicate this session — the declared unique-key combos are missing a
dimension the source genuinely has (same lesson as the recalls grain). The
fix-next list is therefore mostly test-definition edits plus a handful of real
data questions (PBGC null years the biggest). Ranked list extractable from the
run log; rerun any single test with `dbt test -s <name>`.

## Rebuilds run after the suite finished

Clock-registry seed re-seeded (old FAA twin row removed); dbt run over
everything downstream of the deduped sources + the edited models (ECHO,
penalty gap, 13F holdings view, transport timeline index, FHFA, NHTSA, FEC,
PBGC, CourtListener disclosures, NPDES informal). Verified counts post-build.

## Queued for Chris (one-liners, all classifier-blocked for sessions)

```sql
-- verified byte-identical orphan EPA twins (nothing references them):
DROP TABLE LIBRARY_RAW.LANDING.FED_EPA_ICIS_ICIS_AIR_FACILITIES;
DROP TABLE LIBRARY_RAW.LANDING.FED_EPA_ICIS_ICIS_AIR_FCES_PCES;
DROP TABLE LIBRARY_RAW.LANDING.FED_EPA_ICIS_ICIS_AIR_POLLUTANTS;
DROP TABLE LIBRARY_RAW.LANDING.FED_EPA_ICIS_ICIS_AIR_PROGRAMS;
DROP TABLE LIBRARY_RAW.LANDING.FED_EPA_ICIS_ICIS_AIR_TITLEV_CERTS;
-- retired FAA July twin (models disabled in repo this session):
DROP TABLE LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_FAA_REGISTRY;
DROP VIEW  LIBRARY_MARTS.TIMELINE.TRANSPORT__FED_FAA_REGISTRY;
DROP TABLE LIBRARY_RAW.LANDING.FED_FAA_REGISTRY;
-- orphan NCUA dictionary-sheet mart (no model behind it):
DROP TABLE LIBRARY_MARTS.FINANCE.FINANCE__FED_NCUA_CALL_REPORTS;
-- junk 1-row openFDA API stubs (superseded by the real bulk tables):
DROP TABLE LIBRARY_RAW.LANDING.FED_FDA_MAUDE_DEVICE_EVENTS;
DROP TABLE LIBRARY_RAW.LANDING.FED_FDA_CAERS_FOOD_EVENTS;
DROP TABLE LIBRARY_RAW.LANDING.FED_FDA_FAERS_DRUG_EVENTS;
```

---

# Tier 2 (same evening, Chris: "go") — the second sweep

## 🔑 The year-killer: the biggest single find of the session

The 2026-08-22 typing rollout mis-ruled **61 year columns as dates**. The guarded
date cast (correctly) refuses to guess dates from bare digits — so every
pure-digit year fed to it became NULL in the built mart. **29 mart models had
already applied it**: both Treasury fiscal/calendar year pairs ×4 tables, all
three doctor-payments program years (13–15M rows each), foreign-aid fiscal year,
pension data years (the exact 134,534-null test failure), all six workplace-injury
NAICS years, vehicle model years ×3, home-mortgage activity year, IRS tax year,
single-audit year, EPA reporting/data years, judges' degree years, incarceration
trends year, and CDC disease-surveillance's MMWR year — where the nulled year was
also the grain dimension whose loss read as "659k duplicates". Two cumulative
case-count columns (names ending in _MMWR_YEAR) were destroyed the same way.

**Fixed**: all 61 rulings corrected (ambiguous_date → ambiguous_number), all 29
model applications switched to the numeric cast, all 29 marts rebuilt, tests
green. The unapplied 32 rulings are corrected in the CSV so a future apply pass
can't poison them.

## Test-suite failure triage (the 53 fails + 19 errors)

- **Fix build: 160 PASS / 9 ERROR / 1 WARN.** Gone: disease surveillance (659k),
  electricity (84k — its declared 3-part key contradicted its own staging docs;
  now the 6-part real grain), investigations (38k — restored model year),
  water-permit SICs (21k — primary/secondary flag completes the key), pension
  null years (134k), Vera incarceration (3k), MSHA violations combo (the
  2026-07-31 grain fix added the docket to the key but forgot to SELECT the
  column — exposed now).
- **2 staging views broken by re-pull column drift, both fixed**: the sanctions
  screening list (meta columns landed unprefixed) and the NAAG settlements
  staging (the re-pull landed NAAG's real database export with a completely
  different, richer schema — staging fully rewritten, ID-keyed, 882 rows).
- **Leadership-PAC staging fixed**: expected raw bulk-file column names that the
  FEC-ids wiring batch had already renamed in landing; also its dedupe grain
  silently kept one committee per candidate — now keyed on the linkage id.
- **3 staging views remain broken by DATA-IDENTITY mismatches** (documented, not
  guessed at): the "13F submission" landing actually holds holdings-shaped rows
  (the 13F family mess), the BJS landing holds NCVS survey microdata while its
  staging expects a collections catalog, and the EPA FRS-full staging references
  a column variant its landing lacks. One more (workplace-inspections staging)
  just awaits its still-running API load.
- Platform guards: timeline-registry and runaway-duplication asserts now PASS
  (validating the FAA retirement + dedupes); lead-queue reconcile still fails by
  1 — pre-existing, queued.
- Small tail left: TRI chemical combo (664), Europol serial (1), one OSHA
  300A id null (3) — enumerated, unfixed, small.

## Short-of-publisher triage (fix-list #14) — the 30-source batch, resolved

- **9 more false alarms — the same VARIANT chunk trap** (all openFDA rows in the
  ledger measured chunk rows against publisher record counts).
- **Stale claims, already complete**: Treasury daily-cash (verified complete
  08-11), CFTC futures (mart holds the full 287k), DHS immigration stats.
- **Line-counting artifact**: ransomware victims "37% short" — the live CSV's
  raw line count includes wrapped text inside quoted fields; parsed properly it
  holds exactly **31,089 records = our table to the row** (refreshed to today).
- **Actually fixed tonight**: GLEIF ownership relationships re-pulled —
  **485,285 rows, exactly matching today's publisher golden copy** (the "73%"
  measured against a stale figure that was really the exceptions-file count);
  UK sanctions list refreshed (58,336 rows, Aug-20 snapshot) — and the broken
  FCDO twin turned out to be a bad re-load of this same file, not a separate
  source (drop queued, loader parse fix unnecessary).
- **Still running at close (all checkpointed)**: Senate lobbying full crawl
  (1.97M filings, 10× page size — the loader was still on the anonymous page
  cap; fixed), federal debarment re-pull (~167k records replacing the 9,000-row
  round-cap husk), FEMA housing registrations resume (21.7M → 25.9M).
- **By design / not defects**: home-mortgage 28k rows (deliberate DC filter),
  establishment-registration mart 263k (deliberate business-grain dedupe of
  321,723 distinct raw records), GLEIF exceptions "9.5×" (publisher's own file
  holds 6.3M today), FEC "over" rows (multi-cycle loads measured against
  single-cycle files), ECHO "2×" (verified real distinct facilities 08-11).
- **Genuinely open, parked with owners**: roll-call history (Chris's scope
  ruling, carried), Federal Register 9% (real crawl build), tiny stubs
  (NSF/EDGAR/Oyez/OSF/LOC narratives/GDELT and friends — no-loader backlog).

## New follow-up items surfaced by this session (not on the old fix list)

1. **UK FCDO sanctions loader** mis-parses the multi-row-header CSV (title row
   became the column name) — needs a parse fix + re-pull.
2. **13F family needs consolidation**: the positions mart (101M rows) is stale
   against its own model (which reads a 3.8M-row landing table), and an
   UNCATEGORIZED twin of the same 101M rows sits schema-less; landing has
   SUBMISSION vs SUBMISSIONS near-twins. Naming/ownership decision needed.
3. **dbt failure tail**: the suite's real failures (~20 marts) are now an
   enumerated, rankable worklist — several look like more loader dup/parse bugs
   of the same families fixed today.
