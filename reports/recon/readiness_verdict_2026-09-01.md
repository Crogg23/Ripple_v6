# Readiness verdict — viz/analysis, 2026-09-01

Chris's ask, verbatim: confirm "data quality and connections and everything we
talked about is ready to start being visualized and analyzed."

All queries read-only, Python door, ~10 queries, heaviest a 28.5M-row semi-join.
Scripts: scratchpad readiness_r2/r3/r4.py (session-local).

## 1. Freshness — INERT, not a viz blocker

- `LIBRARY_META.REGISTRY.SOURCE_FRESHNESS`: 102 rows, max(LAST_MEASURED_AT) = 2026-07-12 07:11.
- States: stale 43, fresh 30, unknown 22, overdue 4, due 3.
- Chain: checked the ledger's own write date. A hit (recent) would mean states are live truth.
  Miss (7 weeks old) means the states describe mid-July, not today. Per trap
  "registry notes record last-written status": treat FRESHNESS_STATE as history.
- Verdict: staleness tracking is dead weight for viz. Charts should never cite it.
  Data vintages come from each table's own date columns / _INGESTED_AT instead.

## 2. Mart gaps — all four confirmed, mart readers bitten, landing readers not

| Mart (LIBRARY_MARTS) | Mart rows | Landing rows | Gap |
|---|---|---|---|
| CIVIL_RIGHTS__FED_NARA_WRA_AAD | 1 | 36 | 35 |
| CORPORATE_REGISTRY__INTL_ES_BORME | 3 | 25 | 22 |
| CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS | 17,168,287 | 17,179,788 | 11,501 |
| POLITICS__FED_FEC_PAC_SUMMARY | 45,709 | 48,395 | 2,686 |

- Chain: information_schema row_count both sides, exact match to the backup-sweep numbers.
- Verdict: viz that reads LANDING is unaffected. Viz that reads these four marts
  undercounts. Rule until rebuilt: read landing for these four.
- RETRACTED later this session: the fix-session classifier proved all four are
  BY_DESIGN — their model SQL filters/aggregates on purpose. See "Fix 3" below.
  The open question is whether those filters are wanted, not whether builds broke.

## 3. Join reality — the three likely analysis paths, row-level

### FEC money ↔ committees — READY
- FED_FEC_COMMITTEE_TO_COMMITTEE, MEMO_CD <> 'X' (real layer): 1,920,089 rows.
- Spender CMTE_ID found in FED_FEC_COMMITTEES.C1: 1,900,585 = 99.0%.
- Recipient OTHER_ID found: 1,782,716 = 92.8%.
- Note: FED_FEC_COMMITTEES landed HEADERLESS — columns are C1..C15.
  C1 = committee id, C2 = committee name (sampled). Any viz must alias them;
  candidate for a trap line / rename.
- Chain: semi-join on distinct C1. Hit = the dollar row can carry a committee name.
  The 7.2% recipient misses are mostly non-committee OTHER_IDs (candidates, blanks) —
  not a data defect, but label them "unmatched" in charts, don't drop silently.

### PTR filers ↔ members — WEAK, name-join only
- Distinct (upper(LAST), first-2-of-STATEDST) in FED_HOUSE_FD_PTR_INDEX: 9,464.
- Matched to FED_CONGRESS_LEGISLATORS (NAME_LAST, STATE): 1,717 = 18.1%.
- Chain: PTR index has NO bioguide/ICPSR — only name + state-district strings.
  A hit means the filer name-matches a legislator. The 82% misses are a mix of:
  candidates who never served (legitimately absent), name-spelling drift, and
  STATEDST format noise. Cannot separate those without a name-resolution pass.
- Verdict: fine for "PTR volume over time" charts; NOT ready for per-member
  joins without building a filer→bioguide crosswalk. That's a build, not a fix.

### SOD vendors ↔ federal contractors — NOT READY by exact name
- Distinct detail-row vendor names in FED_HOUSE_DISBURSEMENTS: 281,685.
- Exact-name matches in FED_USASPENDING_CONTRACTS.RECIPIENT_NAME: 714 = 0.25%.
- Chain: upper(trim()) both sides. Hit = same string. Near-zero means the two
  universes name entities differently (House pays staff/small vendors; and
  naming conventions diverge). Per the Utah-portal trap: same entity, different name.
- Verdict: this analysis path needs fuzzy/ID matching, doesn't exist yet.

## 4. Traps re-verified live (the chart killers)

- Subtotal rows: 371,471 of 4,914,476 (7.6%). Naive sum $64.48B; detail-only $16.12B
  across 2016-2026 ≈ $1.5B/yr. Matches trap exactly. Filter DESCRIPTION LIKE '%TOTALS%' out.
- AMOUNT is TEXT: 6 rows non-numeric, try_to_number mandatory. Confirmed.
- PTR no natural key: 41,883 rows, 41,864 distinct full-row hashes → 19 dupe rows.
  Dedup on hash(*) before counting filings. Confirmed.
- FEC itoth: 93% memo layer reconfirmed (28.56M total, 1.92M real rows).

## 5. New-table wiring + keyset state

- KEYSET_LIVE: 290,557,744 rows / 293 tables. DISPLAY_KEYSET_LIVE: 96,399,174 / 272.
  Both match the handoff to the row.
- FED_HOUSE_DISBURSEMENTS, FED_HOUSE_FD_PTR_INDEX, ST_OPENSTATES_LEGISLATORS:
  ZERO keyset rows each (query returned no rows). Unwired, as stated.
- 17 tables carry under 100 keyset rows — "wired" is thin there.
- Blocks: nothing for standalone charts of the three new tables; blocks only
  entity-graph visuals that expect them in the keyset.

## Skeptic pass — DISAGREED on 3 of 7, all three stand up

Skeptic ran its own read-only queries (scratchpad skeptic1-3.py). Verbatim highlights:

1. **Mart gaps are 77, not 4.** Full mart↔landing sweep: 573 name-matched pairs,
   77 marts smaller than landing, 57 by >0.1%. Worst: HEALTH__FED_CMS_NADAC
   359,514 vs 1,497,925; JUSTICE__FED_FBI_CDE exactly 50.000%; FARA_BULK 48,103
   vs 221,900. Some shrinkage is legitimate dedup — nobody has classified which.
   "Read landing for these four" wrongly implied the other marts are safe.

2. **FEC join inflates 2.14x.** FED_FEC_COMMITTEES is multi-cycle: 60,031 rows,
   38,693 distinct C1, 16,943 repeated IDs (max 4 rows). A name join onto the
   1.92M real money rows returns 4,116,351 rows — every dollar total doubles.
   My semi-join measured existence, not grain; it could not see this.
   Fix: dedupe the committee dimension (qualify row_number over C1 = 1) first.
   C1 verified as ID: 60,031/60,031 match ^C[0-9]{8}$; C2 name, C3 treasurer.

3. **PTR is 64% row-level, 99.6% on actual PTRs.** My 18% used distinct
   (name,state) pairs — weights a one-off candidate same as a 40-filing member.
   By FILINGTYPE: P = 8,320/8,355 = 99.6%, T 98.7%, O 93.1%, A 80.8%;
   drag is candidate types C/D/W under 19%, where a miss is correct behavior.
   FILINGTYPE was the separator I said didn't exist. Per-member PTR charts ARE ready.
   STATEDST junk: 492 rows (1.2%), immaterial.

Minor skeptic notes: "traps hold exactly" overstated (19 dupe rows vs trap's 18
groups — different hash inputs, both fine); FED_CONGRESS_LEGISLATORS.STATE has
60 distinct values, 80 rows with non-2-char state; coverage claim limited to
what was tested — 3 join paths, mart sweep, keysets, traps.

Skeptic verdicts agreed: SOD 0.25% (4), new tables unwired (5), freshness inert (6).

## Fix session — 2026-09-01, Chris said "plan it out and do it all"

### Fix 1+2 — FEC committee dim, built and verified
- New dbt model: models/marts/finance/finance__fed_fec_committees_dim.sql
  = LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES_DIM, a view.
- One row per CMTE_ID: 38,693 rows, 38,693 distinct. Named columns from the
  official cm.txt layout, which finance__fed_fec_committees had already mapped.
- Join re-test: 1,920,089 real money rows -> 1,900,585 joined rows. Was 4,116,351.
  Fan-out dead; hit rate 99.0% unchanged.
- Deliberately additive: the multi-cycle grain question flagged 2026-08-18 in
  finance__fed_fec_committees stays open. Dim pick is deterministic-arbitrary
  (order by name desc) — fine for labels, wrong for cycle-specific attributes.

### Fix 3 — the 77 short marts, classified by live recompute
- Method: dbt compile each model, run count(*) over its compiled SQL, compare
  to the stored table count. Equal = shrink is the model's own logic. Bigger =
  landing grew after last build = stale.
- Result: 74 BY_DESIGN, 3 STALE_REBUILD, 0 errors.
- The four "proven gaps" from the sweep all came back BY_DESIGN: their model
  SQL filters/aggregates (CFPB drops 11,501 by filter; WRA_AAD aggregates 36->1;
  FBI_CDE pivots 2 series -> exactly 50%). "Broken" was the wrong word; the
  question left is whether those filters are WANTED — a per-model review, not a rebuild.
- Full table: scratchpad mart_classification.csv, copied below at wrap if kept.

### Fix 4 — the 3 stale marts, rebuilt via dbt run
| Mart | Before | After | Live recompute |
|---|---|---|---|
| HEALTH__FED_HHS_OIG_LEIE | 83,369 | 83,747 | 83,747 |
| LAND_AND_TERRITORY__FED_BIA_TRIBAL_GEO | 1 | 335 | 335 |
| FINANCE__FED_EPA_ICIS_FEC..._FACILITIES | 150,866 | 150,866 | 150,866 |
- EPA note: classifier first read 150,877 for it; recount now says 150,866 =
  table. The 150,877 came from a stale pre-session compiled file the classifier
  globbed; the current model dedups 11 rows by design. Consistent now.
- BIA note: the old 1-row copy was materialized in schema DBT_CROGERS — a dev
  target. The rebuild landed in LAND_AND_TERRITORY, the right home. The
  DBT_CROGERS.LAND_AND_TERRITORY__FED_BIA_TRIBAL_GEO 1-row orphan still exists;
  dropping it needs Chris's word.

### Second skeptic pass — numbers all reproduced, four real finds, three fixed

1. **Better committee source exists**: FED_FEC_BULK_COMMITTEES has one row per
   id WITH a real CYCLE column. Coverage differs both ways: it labels 19,471
   money rows the dim misses; the dim labels 10,116 it misses. A union dim
   beats both. NOT built — Chris's fork. Dim header now names the alternative.
2. **Ambiguous ids sized**: 16,943 repeated CMTE_IDs; duplicates disagree on
   name 1,420 / type 993 / state 888 / designation 732 / cand_id 413 / party 296.
   210,872 real money rows (11.0%) join to a conflicted id. FIXED: dim now
   carries IS_AMBIGUOUS; schema tests unique+not_null on cmte_id pass.
   9 rows have blank cmte_nm — labels render empty.
3. **BIA has THREE copies**: REFERENCE__FED_BIA_TRIBAL_GEO (335 rows, built
   2026-08-30) already existed before the rebuild made LAND_AND_TERRITORY's.
   Plus the DBT_CROGERS 1-row orphan. Which schema is home = Chris's fork.
4. **Report self-contradiction**: section 2's "read landing for these four"
   FIXED with an inline retraction pointing at Fix 3.

Scope asterisks from the skeptic, honest and kept: "all 77" means all
name-matchable BASE-TABLE marts — 426 mart views and 73 marts with no
name-matched landing twin were never in the sweep. Globbing bug audited:
EPA was the only stale compiled file of the 77. Zero incremental models.
BY_DESIGN proves self-reproduction, not wantedness; count equality is not
content equality. The 2026-08-18 header comment in finance__fed_fec_committees
still says landing = 78,039 rows; it is 60,031 today.

### Forks A and B — Chris said "both", executed 2026-09-01

A. Union dim rebuilt: FINANCE__FED_FEC_COMMITTEES_DIM now 44,398 ids —
   20,007 from stg_fed_fec_bulk_committees (src='bulk_cm26', real CYCLE,
   is_ambiguous=false) + 24,391 cm-only fills (src='cm_multicycle').
   Money coverage 1,920,056 of 1,920,089 = 99.998%, was 1,900,585.
   No fan-out; dbt unique+not_null tests on cmte_id PASS.
B. BIA home = LAND_AND_TERRITORY, the hand-built mart. The REFERENCE model
   files moved to _JUNK_DRAWER/reference_bia_tribal_geo_2026-09-01 with a
   LEDGER row. Dropped, under Chris's "greenlight destroy":
   LIBRARY_MARTS.REFERENCE.REFERENCE__FED_BIA_TRIBAL_GEO and
   LIBRARY_MARTS.DBT_CROGERS.LAND_AND_TERRITORY__FED_BIA_TRIBAL_GEO.
   Verified after: exactly one BIA mart remains, LAND_AND_TERRITORY, 335 rows.

### Wrap skeptic — one blocker caught in the shipped work, fixed before close

- The union dim's first version hardcoded is_ambiguous=false on all bulk rows,
  so the flag caught 1,414 money rows (0.07%) while 270,519 (14.1%) actually
  sit on cross-cycle-conflicted ids — 99.5% of the dangerous rows flagged safe.
  A bulk row is an unambiguous PICK; the id's history still conflicts.
  FIXED: conflict set computed once from cm, applied to both sources; rebuilt;
  recount confirms 270,519 flagged. dbt tests still pass. Trap line corrected.
- New trap written: CYCLE is null on 55% of dim rows — faceting on it drops most.
- YML description was stale from before the union — rewritten.
- Naming nit: the rebuilt EPA mart is CASE_ENFORCEMENT_CONCLUSION_FACILITIES,
  not its sibling CASE_FACILITIES at 204,019 rows.
- Skeptic also noted: recipient-side OTHER_ID hit rate was never re-measured
  after the union dim — open, small, read-only to answer.

### Untouched, by rule
- SOD vendor matching: a project, parked.
- New-table keyset wiring: not asked for in this fix round.
- Chart-side trap filters: rules, not builds; they live in .claude/traps.md.
