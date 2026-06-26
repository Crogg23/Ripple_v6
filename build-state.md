# Build State
Last updated: 2026-06-26

## CURRENT FOCUS
**Session 2026-06-26 — AUDITED the faceted catalog, prepped hygiene fixes, ideated next builds
(11-agent judge panel).** Catalog is structurally HEALTHY (lifecycle dist unchanged: scouted 853 /
sampled 595 / failed 59 / modeled 34 / empty 28 / landed 20 / stale 3; registry 1506 + 86 run-orphans
= 1592). Moat intact (STEEL 173 sources; IMO 2 landed = OFAC+NOAA-AIS; 7 MMSI vessel feeds scouted).
Post-catalog money/maritime sources ARE catalogued with facets (USASpending contracts 6.3M, OFAC-SDN
19k, SAM-exclusions). But the audit found **drift + 3 structural issues**:

**AUDIT FINDINGS (all query-proven this session):**
1. **The "3 broken dbt marts" are a DATA problem, not dbt — build-state misdiagnosed them.** `fed_fjc_idb`
   = 4.1M rows, **100% empty** across all 20 cols (parse failure); `fed_slavevoyages` = 201 rows of
   `DOCTYPE_HTML` (landed an HTML page); `fed_hhs_taggs` scraped 1 of 19 cols. The dbt marts collapse to
   1 row as a SYMPTOM of blank dedup keys — the models are correct. **Fix = RE-INGESTION, not mart rebuild.**
   10 marts total are ≤3-row stubs (see #3).
2. **1 vocab offender** (was 0): `fed_sam_exclusions.JURISDICTION='US'` — the post-catalog SAM load bypassed
   the naming.py US→federal guard. Fix ready: `scripts/propose_catalog_hygiene_fixes.py`.
3. **Stub-mart gate has a FLOOR HOLE.** CATALOG view gates a stub as `(mart≤3 AND land>100)` — the `>100`
   floor lets 7 small broken marts (hhs_taggs 45→1, naag 26→1, gemi 40→1, zefix 18→1, fdic_enf 14→1,
   nara_wra 36→1, borme 25→3) read as **'modeled'** falsely. Fix ready (ratio rule `land > mart*4`) in the
   same script.
4. **'epstein' is the ONLY theme in the system and it's massively OVER-APPLIED** — on 193 sources incl.
   NPPES (9.6M), NOAA-AIS (7.3M), SEC-EDGAR, bioRxiv, earthquakes (zero Epstein connection). ENTITY_TYPES
   axis was 100% empty (0 sources).
5. `fed_sam_exclusions` only **1000 of ~167k** rows landed (load incomplete → blocks debarred_but_funded).
6. `fed_ofac_sdn` registry join_keys = `[IMO]` only — missing NAME (the sanctions payload).
7. NEW unmodeled asset: 4 DOJ/Epstein **wayback corpora** (`xc_wayback_doj_epstein` = 1.5M rows, single
   TEXT col) — landed, deg=0, not in build-state ledger.
8. Portal classifications (367 heuristic/low) ~90% correct; misfires correctly quarantined in V_REVIEW_QUEUE
   (593). 226 genuinely-ambiguous + 248 deliberately-portal = 474 still `open_data_portal` (reconciled, fine).

**ARTIFACTS PRODUCED (all SAFE, preview-by-default — nothing mutated; the auto-mode classifier blocked
direct catalog writes, so everything is handed to Chris to --apply):**
- `scripts/propose_catalog_hygiene_fixes.py` — FIX 1 vocab offender + FIX 2 stub-gate ratio (rollback-snapshotted). Preview verified: catches exactly the 7 false-modeled, no collateral.
- `scripts/propose_entity_theme_tags.py` — reviewed ENTITY_TYPES + THEMES for all 54 landed/modeled sources
  (vocab-conformant). Run with `--apply`: 52 get entity_types, 46 get themes, **25 bogus 'epstein' tags
  cleaned** off the landed set (kept only on the 4 real corpora). The ~140 non-landed epstein tags are
  out of scope — separate cleanup.

**NEXT-BUILD RECOMMENDATION (judge panel of 5 generators × 3 judges; #0 won unanimously, 57/60):**
- **#1 ✅ SHIPPED — `debarred_but_funded` detector** (added to `connect/leads_specs.py`: SAM-exclusions
  UEI × USASpending contracts UEI, org-vs-org single-name, breadth=award count). Ran + persisted 2 leads
  into `LIBRARY_META.CONNECT.LEADS` (run 8b2e5f42, both active). Flagship **BELLA MIA DONNA LLC** — DLA-
  debarred (Firm, Ineligible), **222 distinct DoD contracts / $1,289,771.86 obligated**, all FY2025
  (2024-10-01→2025-09-29). FACT-grade (UEI hard-key). Scales with every additional SAM row. NB: SAM
  ACTIVATION_DATE is blank in-source, so no "awarded-after-debarment" framing yet (unlocks at full SAM load;
  UEI populated on only 187/1000 landed SAM rows — most exclusions are individuals w/ no UEI).
- **#2 THEN — load-time density gate + DENSITY_PCT on CATALOG** (`ingest.py`): makes 'landed' mean "real
  data is in it", re-grades the empty/HTML fakes, prevents recurrence before the next 800 sources. Cheap.
- **#3 COMPOUNDING — promote money/maritime into the entity spine** (`connect/spine.py` is health-only;
  keys.py already normalizes UEI/CIK/EIN/IMO/MMSI): USASpending/SEC-EDGAR/OFAC/NOAA-AIS are deg=0 islands
  today. Makes every flagship already paid-for actually connect.
- Publishing ceiling (Ghost-Tankers Plotly map of the 2 sanctioned tankers + a reusable `connect/publish.py`)
  is the natural follow-on once a detector or two is firing — data already in hand.

## NEXT ACTION
`debarred_but_funded` is SHIPPED + persisted. Remaining: (1) run the two proposed scripts
(`propose_catalog_hygiene_fixes.py --apply`, `propose_entity_theme_tags.py --apply`) to bank the catalog
cleanup; (2) re-run `scripts/sam_exclusions_load.py` to full 167k to scale the detector + unlock the
temporal angle; (3) next build = density gate (#2) then entity-spine promotion (#3). Pass 0h grants
(`scripts/grant_mcp_readonly_catalog.py`) STILL pending — agent is classifier-blocked from grants, Chris's.

---

## PRIOR FOCUS — faceted catalog
**Session 2026-06-25 (latest) — ORGANIZED THE LIBRARY: built a faceted CATALOG over
SOURCE_REGISTRY as a backend navigation tool.** The registry had 593 blank-CATEGORY rows + 165
inconsistent labels — unnavigable. Reframed organization as a FACETED catalog (tag every source on
independent axes, not one folder tree) after a 3-scheme design bake-off (faceted beat subject-first /
investigation-first, 45 vs 39/39). Stress-tested the design via an 11-agent adversarial workflow
(85 raw defects / ~20 distinct root issues, 15+ critical — RUN_TS dead column, a magic-5000 lifecycle
threshold that mislabeled 27 complete loads as 'sampled', marts case-mismatch, Python-list-can't-bind-as-
ARRAY, a 39%-coverage crosswalk; all folded into `outputs/library_org_BUILD_SPEC_2026-06-25.md`), gated
GO-WITH-FIXES on a live dry-run, and BUILT it. Snapshot `_SOURCE_REGISTRY_BAK_20260625` taken FIRST;
additive-only, idempotent, per-pass verify.

**Live in `LIBRARY_META.REGISTRY` (verified — all invariants pass, 0 vocab offenders):**
- 11 new facet columns on SOURCE_REGISTRY: DOMAIN_PRIMARY, DOMAIN_SECONDARY[], ENTITY_TYPES[],
  JOIN_KEYS_STD[], JOIN_KEY_TIER, JOIN_KEY_TIER_PROVISIONAL, THEMES[], HAS_EVENTS, DOMAIN_SOURCE,
  DOMAIN_CONFIDENCE, NEEDS_TOPIC.
- **`CATALOG`** (view, v2 post-audit) — the one-stop query: every source × facets + DERIVED LIFECYCLE
  (scouted 853 / sampled 595 / failed 59 / modeled 34 / empty 28 / landed 20 / stale 3) + TRUST_LAYER +
  LANDING_FQN + IS_ORPHAN + MART_ROW_COUNT + IS_SAMPLE. 1592 rows (1506 registry + 86 run-orphans).
- 3 FLATTEN bridges (`V_SOURCE_DOMAIN/_THEME/_KEY`), `V_DOMAIN_SUMMARY` (browse menu by data volume),
  `V_REVIEW_QUEUE` (596 to topic-tag/classify). `FACET_VOCAB` (71 controlled values) +
  `FACET_CROSSWALK` (all 165 raw categories → 22 domains).
- Facets filled: JURISDICTION from prefix (0 US/blank); JOIN_KEYS_STD = column fingerprint (646
  MEASURED, PROVISIONAL=FALSE) + free-text-derived (518 CLAIMED, PROVISIONAL=TRUE); DOMAIN via the
  crosswalk (every source classified, 0 NULL); 593 portals → open_data_portal (NEEDS_TOPIC=TRUE);
  epstein THEME (191). Other 9 themes + ENTITY_TYPES are agent-assigned later (landed-first).
- Onboarding wired FORWARD: `register.py` writes the new facets, ARRAY-safe via `PARSE_JSON(%s)` +
  `json.dumps` (the load-bearing fix — a naked Python list silently SPLATTED into adjacent columns,
  corrupting every onboarded row); `prompts/generate_catalog.txt` emits the vocab tokens; `naming.py`
  `normalize_jurisdiction` kills US→federal at the source. dbt vocab guard STAGED
  (`ripple_dbt/seeds/facet_vocab_*.csv` + `models/registry/_meta.yml`, relationships tests @ warn) —
  dbt not installed here, but SQL vocab conformance already verified 0 offenders across all 6 facets.

**Moat now queryable (impossible before):** "everything carrying a vessel ID (IMO/MMSI)" = OFAC SDN +
8 ship feeds in one WHERE; STEEL-key sources (NPI/UEI/CIK/CCN/IMO) as a filter; THEME=epstein as a column.

**Process (all logged):** design workflow (9 agents) → stress-test workflow (11 agents, GO-WITH-FIXES
gate w/ live dry-run) → 6 build passes w/ per-pass verify → independent audit workflow (5 agents, 32
confirmed findings, 11 must-fix) → ROUND-2 FIXES. Artifacts in `outputs/`:
`library_organization_design_2026-06-25.md`, `library_org_BUILD_SPEC_2026-06-25.md`,
`library_inventory_2026-06-25.xlsx`.

**Round-2 (audit fixes) — DONE:** (1) STUB-MART GATE: a mart ≤3 rows over landing >100 no longer reads
as 'modeled' — `fed_fjc_idb` (4.1M court rows, 1-row broken mart) + slavevoyages demoted modeled→landed.
(2) JOIN-KEY UNION+GATING: re-derived JOIN_KEYS_STD = fingerprint ∪ free-text (my Pass 2 had REPLACED, so
flagship moat sources showed []); domain-gated PATENT/CCN/DOCKET (Utah land-patents 14→0, parcel dockets
110→15, bus-stop CCN gated to the 10 real health sources); added NOAA AIS `IMO` (IMO moat 1→2 sources).
(3) LIFECYCLE: split `failed`(59) from `stale`(3); added `IS_SAMPLE` + `MART_ROW_COUNT`. (4) 16 domain
misfiles corrected `DOMAIN_SOURCE='human'` (SAM→sanctions, USASpending contracts→spending, company
registries GLEIF/OpenCorporates/Zefix/CRO/GEMI/BORME/SEC-EDGAR→corporate, FCC→government, basemaps→geo,
3 UNCLASSIFIED stubs). Audit-clean confirmed: bridge views, tier math, vocab (0 offenders), V_DOMAIN_SUMMARY
math, IS_ORPHAN logic.

**Round-3 (taxonomy + portals) — DONE:** #17 earthquakes/seismic/elevation → science_research (unified
earth-science monitoring); #21 FBI crime data → crime_security; #6 keyword-re-domained 367 of the 593
NEEDS_TOPIC portals off their real titles (housing 83 / economy 67 / health 63 / transport 49 / education
42 / …) at DOMAIN_CONFIDENCE='low' (stay in V_REVIEW_QUEUE) — 226 genuinely-ambiguous stay open_data_portal.
Browse menu now real: health 117 / economy 108 / housing 97 / transport 89 / corporate 85 sources.
**STILL DEFERRED (Chris):** broken dbt mart REBUILDS (fjc_idb/slavevoyages/hhs_taggs — catalog correctly
distrusts them via the stub gate, but the marts themselves need rebuilding in dbt); 2 legit USPTO PATENT
sources gated out with the Utah land-patents (re-add if the PATENT moat matters); confirm the 226
low-confidence portal domains; Pass 0h grants (run scripts/grant_mcp_readonly_catalog.py).

## NEXT ACTION
**Pass 0h grants** is the only build step left — grant read role `CLAUDE_MCP_READONLY` SELECT on
LANDING + REGISTRY views + MARTS so the MCP server can query the catalog. The agent is classifier-blocked
from running grants AND from self-editing permissions, so this one is Chris's: run
`python3 scripts/grant_mcp_readonly_catalog.py` (idempotent, read-only, has an as-role verify), or add a
Bash allow-rule for it. Then: fold in audit-workflow findings; agent-assign the other 9 THEMES +
ENTITY_TYPES at the REGISTRY checkpoint (landed-first); topic-tag the 593 NEEDS_TOPIC portals; install dbt
→ run vocab tests → promote warn→error. (Money/maritime detector work below is PRIOR focus — resume after.)

## PRIOR FOCUS — money + maritime layer
**Session 2026-06-25 (later) — WIDE-NET EXPANSION: money + maritime domains, and a
GENERALIZED detector engine.** Strategy turn with Chris reframed the goal: this is HIS
investigative tool (NOT a product, for now), and the instinct is a WIDE NET — pour in
sources that CONNECT by shared hard IDs, with a small set of GENERAL "smells" that sweep
every domain at once (not bespoke detectors per story).

**The engineering win: the "banned-but-active" pattern is now ONE general rule.**
`connect/leads.py` `compile_sql` was hardwired to the doctor case (NPI join, surname gate,
CCN facility enrichment). Generalized it to a domain-agnostic hard-key INTERSECTION (a LEFT
"flag" list ⋈ a RIGHT "active" list on a shared normalized key; optional person-name
corroboration; org/vessel single-name display; generic carry→evidence + a TITLE_FIELDS
object). Adding a smell in a new domain = one JobSpec dict in `leads_specs.py`. The flagship
`banned_but_operating` output is byte-identical after migration; 19 offline tests green.

**Domains shipped today:**
- **MARITIME × SANCTIONS (new):** landed `FED_OFAC_SDN` (19,115 OFAC SDN rows; 2,030 hulls
  carry a derived 7-digit IMO regex-extracted from REMARKS; loader `scripts/ofac_load.py`).
  Fixed a real engine bug: the IMO normalizer (`connect/keys.py`) nulled every AIS hull
  because AIS broadcasts `IMO9187629` (prefix) while OFAC stores bare `9187629` — added a
  dedicated `imo` norm mode (digits-only, tolerates the prefix, rejects the 0000000
  placeholder). New detector `sanctioned_vessel_broadcasting` (OFAC IMO × NOAA AIS IMO):
  **2 live hits** — Iran-sanctioned tankers broadcasting AIS in the Gulf, caught by hull ID
  even though they sail under changed names (EDOR→FEDOR, LAFIT→ADVANTAGE VIRTUE).
- **MONEY (in progress):** `scripts/usaspending_load.py` — USASpending bulk-download API,
  curated 36-col subset (UEI/DUNS/CAGE, parent, geography, NAICS, exec comp, permalink),
  month-by-month (a full-year request times out server-side). FY2025 prime contracts loading
  (~5-6M rows, 100% UEI). `scripts/sam_exclusions_load.py` — SAM Exclusions API (167,573
  records; each carries UEI + CAGE + NPI → bridges money AND health); incremental + fault-
  tolerant (lands every 20 pages, retries 6×, skips dead pages — the SAM API 503s often).
  NEXT: `debarred_but_funded` detector (SAM UEI × USASpending UEI) is config-only once both
  land; bonus `excluded_provider` cross-check is NPI × NPPES/LEIE.

**Operational (this machine):** `library-onboarding/.env` was ABSENT — recreated with a fresh
PAT (works as password), warehouse `RIPPLE_WH`, and `SAM_API_KEY` (expires ~89 days from
2026-06-25). Installed `pyarrow` (the Snowflake pandas-writer dep was missing — why landing
never worked here; should go in requirements). Set an account resource monitor **`RIPPLE_BUDGET`
= 15 credits/month** (~$45 compute ceiling; actual rate $3/credit), notify 75% / suspend 90% /
hard-stop 100%; tightened COMPUTE_WH auto-suspend to 60s.

**Strategy decisions (Chris):**
- WIDE NET, but CONNECTED — pick sources by whether they carry a join key.
- Hard-ID joins = FACT-grade (publishable). Cross-ID-type / name-based links = LEAD-grade
  (human-review only, never auto-published — libel risk). EIN masking keeps health↔money
  structurally fuzzy unless a shared hard ID exists (SAM exclusions' UEI+NPI is the exception).
- DETECTORS (discovery) are the moat; DOSSIERS (lookup) are partly commodity.
- Personal tool for now, not a product. Storage is a non-issue (~12 GB, ~$0.50/mo); compute is
  the only real cost and it's capped. Plan of record: `~/.claude/plans/plan-out-how-to-hidden-moon.md`.

## NEXT ACTION
When the USASpending + SAM loads finish: add the `debarred_but_funded` JobSpec (UEI: SAM
exclusions × USASpending contracts) and run it; then the `excluded_provider` NPI cross-check.
Both are config-only on the generalized engine. Then keep pouring connectable sources
(SAM entity registrations, GLEIF, SEC EDGAR, CourtListener, county property).

---

## PRIOR FOCUS — confidence ladder (earlier 2026-06-25)
**Session 2026-06-25 (cont.) — DESIGNED the confidence ladder, HARDENED it via a 6-lens
adversarial review, and ran Build 1 (foundation clean-up + honest re-baseline).** Strategy turn
with Chris: the goal is to make the engine "a beast" — wider + deeper — before any UI/publishing.

**The design — `connect/design-confidence-ladder.md` (v2).** The unified model for how Ripple
scores every record-to-record link on ONE scale: a Fellegi-Sunter match weight (bits of evidence),
from "shared hard ID = certain" down to "rare name + place = circumstantial but powerful," with
NOTHING excluded. Core rule: keep every CONNECTION at every rung (with receipts); only ever fuse
IDENTITY on a hard ID (a false merge is the one poison). Rarity weighting (u = term frequency) is
the lever that climbs weak signals up the ladder. This IS the architecture going forward.

**The review (workflow `harden-confidence-ladder`, 6 agents, ~30 findings).** Killed the original
plan ("build the FS scorer, watch 0.77 → 0.95"). Caught: the 3-state NULL bug (the #1 FS bug),
NPI label-leakage (answer key used as a feature), don't-score-the-blocker (ZIP is the block key →
0 info), single-rare-name merges, the uncapped SOUNDEX+ZIP self-join, LOG/NULL/unit SQL traps, and
an entire missing SAFETY layer (retraction, model versioning, source-trust gating of the TF corpus
+ spine, transitivity, review-queue ownership, lead staleness). All folded into v2 of the doc.

**Build 1 — DONE (foundation clean-up + honest re-baseline), branch `claude/entity-layer`, uncommitted.**
- `connect/resolve.py`: blocking now drops blank-surname rows (`last_n <> ''`) — ~2.28M NPPES
  type-2 ORG rows were collapsing into one `SOUNDEX('')` mega-block of false-positive fuel. The
  person matcher now only sees individuals (orgs → a future name+EIN matcher).
- `connect/evaluate.py`: hardened — NPI is label-only (no leakage); added a Wilson-CI lower bound
  + an `n>=300` floor on the auto-merge bar; precision-at-recall-floor (un-gameable); a
  **blocking-recall** metric (the recall ceiling the scorer can't touch); a seeded, prevalence-
  honest fixture. 19 tests green.
- **HONEST RE-BASELINE (full population, blank-org garbage removed):**
  - Precision (name-only) tops out ~**0.765** — CONFIRMED real, NOT a blank-org artifact (the junk
    scored <0.80, so it never touched operating-threshold precision; it only bloated the negative
    count 611k→72k and the fixture). The ceiling is name-twins-in-ZIP, exactly as the review said.
  - **THE finding: blocking recall = 23.7%** (1,675 of 7,066 findable true matches even reach a
    block). The OLD eval HID this — its "recall ~0.84" was scorer-recall-among-blocked, the wrong
    denominator. **End-to-end recall is ~0.23, not 0.84.** ZIP-based single-pass blocking throws
    away ~76% of matches BEFORE scoring. `recommend_HIGH` stays None (auto-merge correctly off).
- **Reprioritization (confirmed):** the bottleneck was candidate generation (recall), not scoring.

**Build 2 — DONE (multi-pass blocking + block-size cap), branch `claude/entity-layer`, uncommitted.**
- `connect/resolve.py`: blocking now runs 3 passes UNIONed (a record lands in several blocks):
  `z` surname-sound + ZIP (same place), `i` surname-sound + first-initial (ANY place — catches a
  moved person), `n` exact full name (ANY place). Added a `PAIR_BUDGET=100k` block-size cap that
  drops + LOGS quadratic mega-blocks (this run dropped 83, ~15.3M pairs; densest `i#S530~J` =
  82×6,267), pair dedup via QUALIFY, and a `TEMPORARY` scratch (auto-clean). Flows into the eval too.
- **RESULT — blocking recall 23.7% → 95.9%** (6,774 of 7,066 findable matches now reach a block).
  Candidate generation essentially solved. Runtime ~1m52s, 6.5M labeled pairs.
- **The flip side, BY DESIGN:** name-only precision @ top collapsed 0.765 → **0.037** — removing ZIP
  from blocking floods the set with name-twins (same name, different city, different person), and the
  current name-only score can't tell them apart. This ISOLATES precision as the scorer's job and —
  key — **ZIP is now a FEATURE, not the blocker**, so the FS scorer finally has a real discriminator.
**Build 3 — DONE (the Fellegi-Sunter scorer — `connect/match.py`), branch `claude/entity-layer`, uncommitted.**
First real test of the confidence ladder, and it holds. Scores each pair as a match weight M (bits) =
start + surname (TF-rarity) + first (nickname-aware) + ZIP — all three-state + LOG-guarded; hand-set v1
m/u (graduate to a MATCH_MODEL table + EM later). New CLI verb `match`. NPI label-only; head-to-head vs
the name-only score on the IDENTICAL candidate set at fixed recall.
- **RESULT — the scorer manufactures a high-confidence TIER that name-only cannot:** at **M>=10,
  precision 0.836 (lo95 0.817), ~1,500 pairs, recall 0.19** — a clean CONFIRMED-ish band. Name-only is
  flat ~0.036 at EVERY threshold (it can't separate name-twins at all). Head-to-head precision at fixed
  recall: name-only 0.036 vs FS — 0.067 @rec0.8, 0.087 @rec0.7, 0.178 @rec0.5 (~5x at the useful end).
- **The lever is ZIP-as-a-feature** (unlocked by multi-pass blocking): same name + same ZIP corroborates
  → the M>=10 tier. recommend_HIGH still None (0.84 < 0.99 → no auto-merge, correct), but 0.84 is a strong
  human-review/CONFIRMED tier. Runtime ~1m15s. Output `outputs/match_eval.json`.
- **The ceiling then:** the movers (different ZIP) stayed buried — addressed in Build 4.

**Build 4 — DONE (address + middle-initial features + ground-truth verification), branch `claude/entity-layer`, uncommitted.**
- Schema scan: NPPES carries a clean street address (mailing line1, 96% pop) + middle name (54%); LEIE
  has address (100%) + middle (74%). **DOB is a dead end** (LEIE has it, NPPES has none → nothing to
  compare). Added two features: street **address** (USPS-normalized, JW agree) and **middle initial**
  (the move-stable disambiguator — survives a relocation, unlike ZIP/address). `resolve.py` extracts both
  into the scratch (new ADDR/MID cols); `connect/match.py` v2 scores them three-state + LOG-guarded.
- **3-WAY HEAD-TO-HEAD (identical candidate set, NPI label-only), precision at fixed recall:**
  recall0.5: name-only 0.036 / name+ZIP 0.178 / **+addr+mid 0.298**; recall0.3: 0.036 / 0.178 / **0.657**;
  recall0.2: 0.036 / 0.495 / **0.762**. Each feature adds isolated, monotonic precision; address+middle
  ~doubled-to-quadrupled it. Top tier M>=20: precision 0.874. Runtime ~1m20s.
- **VERIFIED vs ground truth (empirical agree-rates by label = m/u):** m_zip predicted 0.25, MEASURED
  0.246 — the FS framework is calibrated to reality. **Group-practice address leakage is negligible:
  u_address = 0.0002** (2 in 10,000 different-person pairs falsely agree on address — the review's worry
  is quantitatively tiny). Empirical m for first/middle/address run HIGHER than the hand-set params, so
  **the current numbers are a conservative FLOOR.** Output `outputs/match_eval.json`.
**Build 5 — DONE (calibration — `connect/calibrate.py`), branch `claude/entity-layer`, uncommitted.**
Estimated m/u from ground truth with two integrity rails: (1) TRAIN/TEST split BY PERSON (hash of the
LEIE NPI) — every reported number is measured OUT-OF-SAMPLE; (2) tier labels set from MEASURED held-out
precision (Wilson lower bound), not the model's self-opinion. New CLI verb `calibrate`. Persists
versioned `LIBRARY_META.CONNECT.MATCH_MODEL` + `MATCH_RUNGS` (MERGE-style, survive a rebuild).
- **Settled the surname-TF question out-of-sample:** TF-rarity BEATS flat 0.916 vs 0.511 precision @
  recall0.3 — the rare-name weight is real signal, NOT double-counting the soundex blocking key.
- **Empirical m/u (vs my conservative hand-set):** address m 0.167/u 0.0002, first m 0.99/u 0.067,
  zip m 0.247/u 0.0034 (predicted 0.25 AGAIN), middle m 0.986/u 0.077, surname m 0.9997. The strong
  empirical DISAGREE weights on first (−6.5b) and middle (−6.0b) are what clear name-twins out.
- **CALIBRATED TIERS (held-out, measured — what "confident" now MEANS):**
  CONFIRMED M>=11 → **precision 0.876 (lo95 0.860), coverage 0.463** (n=1,770);
  STRONG M>=8 → precision 0.576, coverage 0.761; LEAD M>=0 → precision 0.118, coverage 0.992.
  Calibration lifted precision@recall0.3 from the hand-set ~0.66 floor to **0.92 out-of-sample.**
- **Where the ladder stands:** name-only 0.04 (flat, useless) → a measured, held-out **CONFIRMED tier at
  ~88% precision covering ~46% of all banned-doctor matches.** A reviewer handed CONFIRMED is right ~9/10.
**Build 6 — DONE (the safety layer — `connect/safety.py`), branch `claude/entity-layer`.** The publish-safety
spine, §9 of the design. `safety.py`: a rebuild-surviving `DECISIONS` audit log + `record` / `latest` /
`suppressed` / `gate_rows` (pure, unit-tested) / `status` / `trusted_source_predicate`. Guarantees:
retraction that STICKS (verdicts in a separate table a rebuild can't touch), staleness expiry
(`leads._expire_rule` marks leads absent from the latest run 'stale' — fires even on a zero-result rule),
review-as-recorded-act, and a source-trust hook. New CLI: `review`, `safety`; `leads.published()` = the
canonical publish read (active AND not suppressed). LIVE SMOKE PASSED (rejected Alexander Frank → vanished).

**COMMIT AUDIT + FIXES (pre-commit, 6-lens adversarial workflow `audit-entity-layer-session`).** No
blockers; fixed all majors before committing:
- `calibrate.py`: **three-state bug** (NULL surname/first scored as DISAGREE) → fixed to match.py's
  neutral-0; robust `_estimate` (guards one-label-class + all-NULL field); **content-addressed
  MODEL_VERSION** (append-versioned, was a constant); **atomic persist** (DELETE+INSERT in a transaction).
  Re-ran: CONFIRMED unchanged at **M>=11 → 0.876 / coverage 0.462** (version `fs_emp_95b289e0`); TF wins.
- `leads.py`: **staleness now fires on zero-result rules** (`_expire_rule` moved to run(), per executed
  rule); added `published()` so STATUS='stale' AND review-suppression are both enforced at the publish read.
- `match.py`: MODEL flagged as a pre-calibration SEED (operating model = calibrate's persisted MATCH_MODEL).
- `evaluate.py`: renamed the "blocking recall" metric to **candidate-recall** (it includes the size-cap +
  editdistance prune, not blocking alone). `safety.py`: %-literal caveat. Design doc: a "code vs doc"
  reconciliation note (rungs, seed-vs-operating, surname normalizer). Live: leads --run write path, STATUS,
  imports, review/safety CLI — all green. **25 tests green.** Orphaned persistent RESOLVE_SCRATCH dropped.
- NOTE: multi-pass blocking moved the eval universe — `resolve_eval.json` positives 1983→6774, candidate
  ceiling now ~0.959; all prior-quoted resolve precision/recall figures are superseded.

**Engine status: the confidence ladder + its safety half are BUILT, AUDITED, and proven end to end.**
Next (Chris's fork): BREADTH — auto-spine to widen the who's-who past health; land the EIN/CIK money
anchors. Or polish toward a published story.

## PRIOR FOCUS (2026-06-25 — entity layer)
**Session 2026-06-25 — BUILT THE ENTITY LAYER (the 5 audit gaps) on branch `claude/entity-layer`.**
Turned the wired table-graph into a queryable "who's who" + dossiers + a self-surfacing leads list +
a gated fuzzy matcher. All in `connect/`, all verified live. NOT yet committed/PR'd.

**What shipped (6 phases, all on the health/provider slice — NPPES, OIG-LEIE, Facility-Affiliation
crosswalk, 7 CCN rosters):**
- **Phase 1 — flagship LEADS (`connect leads`).** `connect/leads.py` + `leads_specs.py` compile a
  declarative job to targeted SQL, score, and MERGE into `LIBRARY_META.CONNECT.LEADS` (FIRST_SEEN /
  LAST_SEEN, stable LEAD_ID). `banned_but_operating` = **11 OIG-excluded providers / 38 facility
  affiliations**, surname-corroborated, ranked (ALEXANDER FRANK @ 12 facilities top). Runs OWN SQL,
  never imports `connect.bridge` (the FANOUT_MAX/dedup guards gated 21/38 — that's why).
- **Phase 2 — entity spine (`connect spine`).** `connect/spine.py`: hard-ID-only resolution (same
  NPI/CCN/… value across sources = one entity; **zero false-merge**). **9,678,735 entities (952,930
  multi-source)**, content-addressed stable `ENTITY_ID` (rebuild renumbers no one — proven), golden
  record via authority ladder (NPPES>…>LEIE). Tables: `ENTITY_MAP`, `ENTITY_GOLDEN`, `CONNECT_NODES`,
  `MATCH_PAIRS`. Backfills `LEADS.LEFT_ENTITY_ID`. **CORRECTION to the plan:** dropped label-prop
  cross-key clustering — NPI↔CCN is a *relationship* (works-at), not identity; fusing would merge
  doctors with hospitals. Cross-ID-type identity is the fuzzy frontier (Phase 5), correctly gated.
- **Phase 3 — dossier + search (`connect dossier`).** `entity_index.py` builds `ENTITY_INDEX`
  (per-entity×source). `dossier.py` resolves `--npi/--ccn/--ein/--id/--q` → cross-domain rollup +
  affiliated facilities; prints / `--json` / `--html`. Disambiguates multi-hit names.
- **Phase 4 — name/address normalization.** `keys.py` NAME/PERSON → token-sort + legal-suffix/credential
  strip ('SMITH, JOHN MD' == 'JOHN SMITH'); ADDRESS → USPS abbrev (no sort). Makes dossier search
  order-insensitive. Nickname seed at `ripple_dbt/seeds/connect/nickname_map.csv`. (Lift on same-order
  federal pairs is ~neutral; real win is search + cross-order matching. **`connect discover` graph
  refresh with the new NAME norm is DEFERRED** — slow at 646 tables; spine/dossier already use it.)
- **Phase 5 — fuzzy linkage, BUILT BUT GATED (`connect resolve`).** `resolve.py`: SOUNDEX(last)+ZIP
  blocking, in-warehouse JAROWINKLER+EDITDISTANCE scoring, nickname expansion → `ENTITY_LINKS` (AUTO/
  REVIEW bands). **Never touches the spine.** `leie_nppes` recipe: 40,329 candidate links.
- **Phase 6 — eval harness + the repo's FIRST tests (`connect eval`).** `evaluate.py` sweeps
  thresholds vs hard-ID ground truth → `outputs/resolve_eval.json` + `GOLD_PAIRS` + a frozen fixture.
  **Result: precision tops out ~0.77 even at score 0.99** → name+ZIP fuzzy is a lead generator, NOT
  safe for auto-merge → recommend `HIGH=None`, keep gated. `tests/` (19 tests, 15 offline + 4 live,
  all green) + `pytest.ini` + `requirements-dev.txt` + `.github/workflows/tests.yml` (first CI).

**New CLI verbs:** `spine`, `entity-index`, `dossier`, `leads`, `resolve`, `eval` (in `connect all`:
fingerprint → discover → spine → explore). **New schema `LIBRARY_META.CONNECT`** (persisted; was
file-only before). Plan file: `~/.claude/plans/come-up-with-a-foamy-rabbit.md`.

**Next:** commit + PR the branch; optionally re-run `connect discover` to refresh the graph with the
new NAME normalization; pour IRS EO BMF to extend fuzzy to org names; consider DOB/address features to
lift fuzzy precision toward an auto-merge bar.

## PRIOR FOCUS (2026-06-24 — bridge layer)
**Session 2026-06-24 (cont.) — ACTIVATED the bridge layer. Poured a real CCN↔NPI crosswalk + 7 CCN
facility sets; bridge edges 14 → 59, graph 13,321 → 14,694.**

**The premise in the prior build-state was WRONG (verified live).** It said the bridge was "fuel-gated:
the 1.9M-pair NPPES NPI↔EIN crosswalk fires zero because non-NPPES EINs don't overlap it." Reality:
`FED_CMS_NPPES.EMPLOYER_IDENTIFICATION_NUMBER__EIN` = **`<UNAVAIL>` only, 1 distinct over 9.6M rows** —
CMS masks the EIN in the public NPPES file (so does `PARENT_ORGANIZATION_TIN`). **The crown-jewel NPI↔EIN
crosswalk never existed.** A public NPI↔EIN *hard* crosswalk mostly doesn't exist (EIN is PII-masked
everywhere: NPPES, PPP, SAM all redact it) — that linkage is really an entity-resolution job for the
corroboration layer. The achievable, high-value bridge is **CCN↔NPI**.

**What shipped:**
- **12-agent research workflow** verified the exact fuel against live CMS/IRS docs (each agent downloaded
  real files + checked for masking). Winner: **CMS Doctors & Clinicians "Facility Affiliation"** (dataset
  `27ea-46a8`) — a CURRENT, national, **2.24M-row CCN↔NPI crosswalk, 0 masked** (938k NPIs × 41k CCNs).
- **`scripts/bridge_fuel_load.py` + `scripts/bridge_fuel_specs.py`** — a deterministic LLM-free bulk loader
  (reuses `ingest.py`/`register.py`: all-TEXT landing + provenance + INGEST_RUNS + registry upsert). Built
  because **`ANTHROPIC_API_KEY` is MISSING from `library-onboarding/.env`** so the LLM onboard agent can't
  run — but I'm the LLM, so for known-shape sources a deterministic loader is cleaner anyway. Features:
  per-source key-column **aliasing** (renames verified id cols → canonical `CCN`/`NPI` so the tagger detects
  them — the tagger only matches the literal `ccn`/`npi` token; per-source aliasing avoids touching the
  global tagger / risking false positives on the existing 638 tables), row `filter`, metastore URL
  resolution (CMS dated URLs rotate), chunked streaming, UTF-8 stdout.
- **8 sources poured LLM-free (+2,318,145 rows; Library now 646 tables):** the crosswalk
  `FED_CMS_FACILITY_AFFILIATION` (2,239,952) + 7 CCN facility endpoints — `FED_CMS_POS_OTHER` (44,429),
  `FED_CMS_HOSPITAL_GENERAL` (5,432), `FED_CMS_HOSPICE` (6,852), `FED_CMS_HOME_HEALTH` (12,392),
  `FED_CMS_IRF` (1,222), `FED_CMS_LTCH` (311), `FED_CMS_DIALYSIS` (7,557). All `INCLUDE=Y`.

**Bridge yield (after re-`discover`): every facility type now bridges to NPPES (9.6M providers) via CCN→NPI:**
HOME_HEALTH↔NPPES 60,526 matched · NURSING_HOME↔NPPES 35,813 · HOSPICE 26,354 · DIALYSIS 21,212 · POS
16,835 · HCRIS 15,573 · HOSPITAL 11,239 · IRF 6,486 · LTCH 2,638. **NPPES went from ~0 useful bridge
partners to 21.** Tier deltas: STEEL 202→278, GEO 4161→5114, CORROBORATED 503→587, PROBABILISTIC
2401→2616, **BRIDGE 14→59**, TOTAL 13,321→**14,694**.

**Flagship "banned but still operating" — ground-truthed (adversarial check PASSED):** the crosswalk
directly connects to `FED_HHS_OIG_LEIE` on NPI (STEEL, 11 banned providers). A targeted crosswalk×LEIE
query surfaced **38 facility affiliations of 11 OIG-excluded providers** — the provider NAME in LEIE matches
the provider NAME in the crosswalk for every one (a 10-digit-NPI coincidence could never also match on name
→ real, not fluke). Several excluded in the last 60 days (RAJIVE DAS 2026-04-20, SADYE DEXTER 2026-06-18,
AMIT SHAH 2026-05-20); ALEXANDER FRANK (patient-abuse, 1128a2) spans 15 facilities incl. 4 nursing homes.
Precise claim: "affiliated in CMS's current Facility Affiliation file" (billing history) — a strong lead, not
proof of active employment today.

**ENGINE NUANCE found (why facility↔LEIE BRIDGE edges don't show in the graph):** (1) the fanout guard
drops banned providers' large-hospital CCNs (>40 affiliated NPIs) — 21 of 38 gated; (2) the surviving
nursing-home CCNs' bridge is **deduped because facility↔LEIE already has a weak DIRECT ZIP/GEO edge** (e.g.
DIALYSIS↔LEIE shares 4,872 ZIPs). The dedup-vs-direct rule lets a low-value GEO/ZIP edge suppress a
high-value entity bridge. So the "banned but operating" story lives in the **targeted query**, not a graph
edge — see PARKED IDEAS for the tier-aware-dedup fix. **NBER 2nd crosswalk deferred** (NBER hard-blocks bot
downloads, 403; it was frozen-2017 anyway — Facility Affiliation is the better, current primary).
**EIN bridges remain blocked** (no public NPI↔EIN / CCN↔EIN hard crosswalk; EIN masked in NPPES/PPP/SAM).
**Blocked on: nothing.**

## PRIOR FOCUS (2026-06-23/24 — connect engine build)
**Session 2026-06-23/24 — built the CONNECT + EXPLORE layer and scaled the Library 45 → 638 sources.**
A new `connect/` package (the connection engine) was added and the Library jumped from 45 to 638 landing
tables. All on branch `claude/connect-engine-and-bulk-loader`, merged to `main`.

What shipped:
- **`connect/` engine** — turns the landed Library into a graph of REAL connections: it measures actual
  value overlap on a shared key (not just "both carry an EIN-shaped column"). Pipeline: `fingerprint`
  (which keys each table carries + are they populated) → `overlap` (value equi-join + spatial point-in-
  polygon) → `discover` (the edge list) → `explore` (interactive Plotly map → `outputs/connection_explorer.html`).
  Reuses the `portal_recon` tagger and `library-onboarding/snow.py`. Run: `python -m connect all`. See `connect/README.md` + `connect/HOWTO.md`.
- **`connect/portal_loader.py`** — LLM-free bulk loader. Pulls ArcGIS/Socrata datasets straight from the
  338k `PORTAL_DATASET_INDEX` via templated platform APIs (no recon/codegen), landing them identically to
  the onboarding agent (same provenance / INGEST_RUNS / registry). `--connectable` targets datasets whose
  keys overlap what the Library already holds. `python -m connect harvest --connectable --run`.
- **Hardening** — an adversarial audit found 23 real issues; fixed in two passes:
  - FLAWLESS (correctness): per-key `NORM_RULES` that PAD (never strip) IDs + drop malformed; a confidence
    gate (0–1) that kills chance-level "connections" (a collision guard over each key's value space); spatial
    fixes. Cut a 97-table graph from 809 edges → 307 honest ones (502 flukes gated).
  - EXPANDABLE (scale): set-based discovery (one keyset table + one self-join) replaced the O(n²) per-pair
    query crawl; loader gained retry/backoff, failed-run logging, SHA-idempotent `--refresh`, collision-free
    IDs, a `PLATFORMS` registry, an ArcGIS non-advancing-page guard.

**Live now: 638 landing tables (~24.3M rows), 12,804 real connections across 547 datasets**, each scored by
confidence. Headliner survives: NPPES providers ↔ HHS-OIG **banned providers** on NPI = 8,503 matched (100%).
Most new edges are local-gov datasets linking each other (industry/school codes, NPI); 730 reach into the
federal data; 17 are federal↔federal. **Blocked on: nothing.** PAT rotates ~2026-07-05.

**Deliberately deferred (don't over-build until needed):** incremental/cached re-discovery + a Snowflake-backed
graph store (only needed at ~tens-of-thousands of tables — a full rebuild currently re-indexes everything);
making the 15MB explorer fast at scale (top-N / default-filter); a crosswalk/bridge layer (NPI↔CCN, CIK↔EIN).

## PRIOR FOCUS (2026-06-20 — env recovery)
**Session 2026-06-20 — env recovery + warehouse verification + dbt hygiene (no new sources).** A fresh
container had a **dead `SNOWFLAKE_PAT`** (Snowflake `394400`), so everything Snowflake-side (connector, MCP
server, dbt) was dark. Recovered: new PAT into a gitignored `.env`, `config.py` now `load_dotenv(override=True)`
so `.env` beats stale container vars, deps + `dbt deps` installed, **live connector connection proven**
(`ACCOUNTADMIN` / `RIPPLE_WH` / `LIBRARY_RAW`). Read-only sweep confirmed **5 `LIBRARY_*` DBs, 45 landing
tables, 23,788,352 rows** (matches the ledger). Reconciled dbt vs landing and cleaned house — removed the
`fed_cms_tic_mrf` ghost, fixed 4 YAML-bomb descriptions, renamed the revolvingdoor intermediate → **`dbt
parse` clean**. Then **`dbt build` materialized all 35 modeled sources — 53 models, fully green (PASS=459,
WARN=96, 0 errors)** — after fixing 5 build bugs (epoch-micros audit casts ×2, a Snowflake-incompatible
multi-column UNPIVOT → `LATERAL FLATTEN`, a phantom-column test, a malformed accepted_values) and downgrading
73 over-strict null/enum tests to `warn` (+2 dropped). Merged via **PR #14 + #15**. **Blocked on: nothing.**

The agent now has **three fetch capabilities** (bulk/API, static scrape C1, headless-browser scrape C1b)
and **three load modes** — snapshot, **C2 incremental**, and **C3 chunked/streaming** (large files that
won't fit in memory) — each picked autonomously at recon. **C3 proven on NPPES (~9 GB)**: streamed 300,000
rows in 50k chunks at ~3 GB peak RSS where the all-in-memory load OOM-killed (exit 137) every prior batch.
C1b is
**proven full end-to-end through `onboard.py` with real creds**: recon autonomously set `scrape_js`,
codegen used the injected `render()`, Playwright cleared a JS shell, and 100 rows landed in
`LIBRARY_RAW.LANDING` + registered in `LIBRARY_META` (target `quotes.toscrape.com/js` — BAILII's wall was
down at run time; see the C1b end-to-end section for why). With full capability proven, **ran registry
batches 2 + 3** (tier-1, auth-free): batch 2 = 12 attempted → 4 landed (incl. FARA 221,900); batch 3 = 4
ran before an **Anthropic credit exhaustion** halted the queue → 3 landed (incl. Mapping Inequality 10,154),
8 credit-blocked. Credits funded → **batch 4** retried those + 8 new: **16 attempted, 10 landed** (incl.
NOAA AIS 7.3M, SCDB 83,644). Then **C3 chunked landed the two big OOM files**: NPPES 9,606,683 (full file
to EOF, via crash-resume) + FJC IDB 4,126,450. **Live total: 38 landing tables, 23,070,680 rows.** PR #2–#9
merged to `main`; the C3 big-load work is on `claude/laughing-knuth-fmjka8`. **Blocked on: nothing.**

## WHAT EXISTS
- `library-onboarding/` — the 5-checkpoint CLI agent: RECON → SCRIPT → LOAD → DBT → REGISTRY.
- LOAD lands raw to `LIBRARY_RAW.LANDING.<UPPER(SOURCE_ID)>` — all columns TEXT, stamped
  `_INGESTED_AT` / `_SOURCE_RUN_ID` / `_SRC_SHA256`. Two load modes: **snapshot** (default — replace,
  idempotent by SHA) and **incremental** (C2 — read `MAX(cursor_field)` watermark, fetch only newer rows
  via `context["since"]`, append; staging dedups on the primary key). The LOAD also rejects HTML-as-data.
- Logs every run to `LIBRARY_META.INGEST_LOGS.INGEST_RUNS`; upserts `LIBRARY_META.REGISTRY.SOURCE_REGISTRY`.
- **Unattended**: `ONBOARD_AUTO_APPROVE=1` + `ONBOARD_AUTO_REPAIR=N` (default 3, feeds errors back to
  Claude). `live_batch.py` is the hand-curated growing queue — skips anything already landed, safe to re-run.
- **Registry-driven queue (B)**: `registry_queue.py` selects candidates from `SOURCE_REGISTRY`
  (not `INCLUDE='Y'`, not already landed, has URL, conforming `SOURCE_ID`, auth filter) ordered by
  `PRIORITY_TIER`; `registry_batch.py` runs them through the full agent. **Safe by default** — previews
  the queue read-only unless `--run`. Pinning each candidate's registry `SOURCE_ID` makes onboarding
  *update that row* (`INCLUDE` blank→`Y`), so the catalog is both the queue and the completion ledger.
- A minimal dbt project at `library-onboarding/ripple_dbt/` (run with the in-repo `profiles.yml`,
  creds from env / PAT-as-password, builds into the `DBT_CROGERS` schema).

### Live sources onboarded by the agent
| SOURCE_ID | rows | how |
|---|---|---|
| `fed_usaspending_toptier_agencies` | 111 | `first_live_load.py` (deterministic) |
| `fed_sec_edgar_company_tickers` | 10,414 | full LLM agent |
| `fed_federal_register_documents` | 5,000 | full LLM agent (codegen auto-paginated) |
| `fed_fdic_failed_banks` | 4,115 | full LLM agent (after URL-hallucination prompt fix) |
| `fed_treasury_debt_to_penny` | 8,329 | full LLM agent (full daily debt history) |
| `fed_fda_drug_enforcement` | 5,000 | full LLM agent (bounded sample) |
| `fed_treasury_avg_interest_rates` | 4,961 | full LLM agent (batch 3, 2026-06-17 — full monthly history 2001→2026) |
| `xc_biorxiv_medrxiv` | 432 | **registry-driven queue** (2026-06-17 — first source onboarded straight from the catalog) |
| `fed_clinicaltrials` | 500 | registry queue, tier-1 batch (bounded API snapshot) |
| `fed_cms_hcris` | 6,103 | registry queue, tier-1 batch (117-col hospital cost report; rebuilt against real columns) |
| `fed_cfpb_complaints` | 500 | **incremental (C2)** — 2 runs (backfill + watermark-advance append) |
| `fed_cms_nursing_home` | 14,700 | **registry batch 2** (2026-06-17 — bulk CSV, Care Compare) |
| `fed_doj_fca_settlements` | 19 | registry batch 2 (DOJ False Claims Act press-release scrape) |
| `fed_doj_crt_cases` | 1 | registry batch 2 (DOJ Civil Rights portal scrape — ⚠ thin/incomplete, review) |
| `fed_fara_bulk` | 221,900 | registry batch 2 (FARA eFile bulk — foreign-agent registrations) |
| `fed_mapping_inequality` | 10,154 | **registry batch 3** (2026-06-17 — HOLC redlining, GeoJSON flattened to rows) |
| `fed_hhs_taggs` | 45 | registry batch 3 (HHS grant-tracking, incremental backfill) |
| `fed_fdic_enforcement` | 2 | registry batch 3 (FDIC enforcement portal scrape — ⚠ thin, review) |
| `fed_cms_nppes` | 9,606,683 | **chunked (C3)** — full NPPES provider file streamed to EOF (~9 GB; was OOM) |
| `fed_fjc_idb` | 4,126,450 | **chunked (C3)** — federal court cases (FJC IDB; was OOM) |
| *(batch-4 sources: noaa_ais 7.3M, scdb 83,644, etc. — see batch 4 above)* | | |
| `fed_noaa_ais` | 7,296,275 | **registry batch 4** (NOAA Marine Cadastre AIS vessel tracking — incremental) |
| `fed_scdb` | 83,644 | registry batch 4 (Supreme Court Database — case-level votes/decisions) |
| `fed_nara_aad` | 554 | registry batch 4 (NARA Access to Archival Databases) |
| `fed_revolvingdoor_project` | 409 | registry batch 4 (gov-accountability tracking; portal scrape) |
| `fed_slavevoyages_intraamerican` | 201 | registry batch 4 (intra-American slave-trade voyages) |
| `fed_wpa_slave_narratives` | 100 | registry batch 4 (WPA slave narratives 1936–38) |
| `fed_naag_multistate_settlements` | 26 | registry batch 4 (multistate AG settlements) |
| `fed_oyez` | 25 | registry batch 4 (SCOTUS oral-argument/case data, API) |
| `fed_nara_wra_aad` | 4 | registry batch 4 (WRA records — ⚠ thin, review) |
| `intl_ch_zefix` | 1 | registry batch 4 (Swiss business registry — ⚠ thin, review) |
| `fed_cms_nppes` | 300,000 | **C3 chunked** (2026-06-17 — ~9 GB NPPES streamed in 50k chunks, demo-capped at 300k) |

**37 clean sources in `LANDING`** (batches 2–5 + C3 big files). Live total: **45 landing tables,
23,788,352 raw rows** (was 19 / 1,709,487 before batch 2). The C3 chunked path then landed the two big
federal files that used to OOM-crash: **`fed_cms_nppes` 9,606,683** (full provider file, streamed to EOF)
and **`fed_fjc_idb` 4,126,450** (federal court cases) — +13.7M rows. The demo `intl_demo_quotes_toscrape_js`
was dropped (table + registry + ingest_runs) before the batch. The false-success `fed_cms_hpt_enforcement`
was dequeued earlier (registry un-flagged + junk table dropped, 2026-06-17, with Chris's OK): it had landed
an HTML page (one `DOCTYPE_HTML` column, 22 junk rows), not data — caught when its mart wouldn't build.

### Registry batch 2 — `registry_batch.py` tier-1, auth-free, per-source timeout (2026-06-17)
Ran the queue end to end through the full agent (all 4 fetch capabilities live), each source wrapped in a
12-min wall-clock `timeout` so one hang couldn't stall the session. **12 attempted, 4 landed, 1 false-success
(corrected), 7 failed.** The easy bulk/API sources were already onboarded — this tier-1 residue is the hard
portal/scrape/huge shapes, so a low hit-rate is expected.

| Source | Result | Rows |
|---|---|---|
| `fed_cms_nursing_home` | ✅ onboarded | 14,700 |
| `fed_doj_fca_settlements` | ✅ onboarded (press-release scrape) | 19 |
| `fed_doj_crt_cases` | ✅ onboarded — ⚠ **thin scrape, review** | 1 |
| `fed_fara_bulk` | ✅ onboarded (bulk) | 221,900 |
| `fed_cms_tic_mrf` | ⚠ **false success → un-flagged** (incremental first-run 0 rows, no table) | 0 |
| `fed_chronicling_america` | ❌ aborted — LoC API migrated/dead (404) | — |
| `fed_cms_hpt_mrf` | ❌ aborted — per-hospital MRF crawl, no single data file | — |
| `fed_cms_ma_enrollment` | ❌ aborted — CMS dynamic portal, grabbed instructions ZIP / no CSV links | — |
| `fed_cms_nppes` | ❌ killed (exit 137, OOM) — ~9 GB download blew container memory | — |
| `fed_densho_ddr` | ❌ aborted — portal-only, no machine-readable endpoint | — |
| `fed_docsouth` | ❌ aborted — couldn't resolve a bulk data file | — |
| `fed_epa_egrid` | ❌ aborted — multi-sheet Excel / dynamic download | — |

- **Agent gap this exposed + FIXED**: an **incremental** source whose **first** run (empty watermark, `since
  is None`) returns 0 rows was logged `success` (0 rows) and flipped `INCLUDE=Y` — a false success with no
  table (`fed_cms_tic_mrf`: recon called the per-insurer MRF incremental, the scrape found nothing). Fix in
  `ingest.run_ingest`: `allow_empty` now only applies to a *continuing* incremental run (`since is not None`);
  a first-run empty backfill fails loudly (→ auto-repair → abort), so it can't false-succeed. tic_mrf's
  registry row was un-flagged (`INCLUDE` blank); the 0-row `INGEST_RUNS` record is kept as history.
- **Also seen (not yet fixed)**: codegen occasionally emits a prose preamble before the code block →
  `extract_code` returns it → `invalid syntax (line 1)`; it self-corrected on retry here. Worth hardening
  `extract_code`/the codegen system prompt before a future batch. The DOJ CRT 1-row landing is a thin-scrape
  near-miss (no pagination) — flagged for review, not auto-dequeued (it did land structured data).

### Registry batch 3 — next 12 fresh tier-1 (skipping batch-2's 8 attempts), 2026-06-17
Worked further down the queue, excluding the 8 sources batch 2 already attempted. **Cut short by an
Anthropic API credit exhaustion partway through** — so the run splits in two:
- **Ran with working credits (4):** `fed_mapping_inequality` ✅ 10,154 (GeoJSON flattened), `fed_hhs_taggs`
  ✅ 45, `fed_fdic_enforcement` ✅ 2 (⚠ thin portal scrape), `fed_fjc_idb` ❌ killed (OOM — large bulk CSV).
- **Credit-blocked (8, NOT genuine failures — still queued for retry):** `fed_mapping_prejudice`,
  `fed_naag_multistate_settlements`, `fed_nara_aad`, `fed_nara_wra_aad`, `fed_noaa_ais`, `fed_npdb_puf`,
  `fed_olms_lm_reports`, `fed_opm_fedworkforce` — every `call_claude` returned HTTP 400 "credit balance is
  too low", so recon couldn't run and each aborted in ~6s. These left zero partial state (no landing, no
  `INGEST_RUNS`, registry untouched) — re-run them once credits are topped up.
- **BLOCKER surfaced (stopped the queue):** the `ANTHROPIC_API_KEY` has no credits left. No further batches
  can run until it's funded — this is the pipeline-wide stop condition, not source difficulty.
- **Recurring OOM on big bulk files** (`fed_cms_nppes` ~9 GB in batch 2, `fed_fjc_idb` in batch 3): the load
  path reads the whole download into pandas in memory → container OOM (exit 137). Follow-up: stream/chunk
  large downloads (or cap rows) so multi-GB sources don't get killed.

### Registry batch 4 — credits funded, retried the 8 + 8 new (2026-06-17)
After Chris topped up the Anthropic key, re-ran the queue: the 8 batch-3 credit-blocked sources + 8 new,
skipping the 9 genuinely-hard fails (dead APIs / dynamic portals / OOM-prone multi-GB). **16 attempted,
10 landed, 6 failed** — the best batch yet.
- **Landed (10):** `fed_noaa_ais` 7,296,275 (incremental — biggest source in the Library now), `fed_scdb`
  83,644, `fed_nara_aad` 554, `fed_revolvingdoor_project` 409, `fed_slavevoyages_intraamerican` 201,
  `fed_wpa_slave_narratives` 100, `fed_naag_multistate_settlements` 26, `fed_oyez` 25, `fed_nara_wra_aad` 4
  (⚠ thin), `intl_ch_zefix` 1 (⚠ thin). The 3 portal scrapes (nara_aad, revolvingdoor, naag) confirm the
  browser/scrape path earns real rows from JS/portal sources.
- **Failed (6):** `fed_mapping_prejudice` (Shapefile — no pandas path), `fed_npdb_puf`, `fed_olms_lm_reports`,
  `fed_opm_fedworkforce` (large/dynamic bulk), `fed_slavevoyages_transatlantic` (much larger than the
  intra-American set), `intl_ca_statscan` (StatCan WDS API shape).
- **Retry verdict**: of the 8 formerly credit-blocked, 4 landed (naag, nara_aad, nara_wra_aad, noaa_ais) and
  4 genuinely failed — confirming they were *not* all hard, just blocked before. The credit-block accounting
  in batch 3 was correct.
- **Thin landings flagged for review** (real data, likely incomplete): `fed_nara_wra_aad` (4),
  `intl_ch_zefix` (1) — alongside batch-2/3's `fed_doj_crt_cases` (1) and `fed_fdic_enforcement` (2).

### Registry-driven queue (B) — `xc_biorxiv_medrxiv` (2026-06-17), verified live
- `registry_batch.py --source-id xc_biorxiv_medrxiv --run` selected the row from the catalog and ran the
  full agent. End to end: RECON → LOAD (432 rows → `LIBRARY_RAW.LANDING.XC_BIORXIV_MEDRXIV`) → DBT-gen →
  REGISTRY. The candidate's row flipped `INCLUDE` blank→`Y` **in place** — registry stayed **901** rows
  (an UPDATE via the pinned `SOURCE_ID`, not a duplicate INSERT), `INCLUDE=Y` went 10→11.
- **Agent fix this exposed**: dbt-gen returned the models as JSON with multi-line SQL/YAML values; for a
  wide (~25-col) table that JSON blew past `max_tokens=4096` and truncated → `extract_json` "Unbalanced
  JSON" → checkpoint 4 aborted before REGISTRY. Fixed: dbt-gen `max_tokens` 4096→8192, and `extract_json`
  now matches the fence greedily + parses with `strict=False` (tolerates literal newlines + dbt `{{ }}`).
- dbt models for biorxiv are GENERATED (staging view + `science_research` mart + schema.yml; `dbt parse`
  clean, 14 models total) but not yet RUN.

### Registry batch 1 — `registry_batch.py --tier 1 --limit 5 --run` (2026-06-17)
First real unattended batch off the catalog. **3/5 complete**, verified live:

| Source | Result | Rows |
|---|---|---|
| `fed_clinicaltrials` | ✅ onboarded, `INCLUDE=Y` | 500 |
| `fed_cms_hcris` | ✅ onboarded, `INCLUDE=Y` | 6,103 |
| `fed_cms_hpt_enforcement` | ✅ onboarded (auto-repair recovered a CSV-parse error) | 22 |
| `fed_chronicling_america` | ❌ aborted (3 repairs) — JS-heavy API docs page recon couldn't crack | — |
| `fed_cms_hpt_mrf` | ❌ aborted (3 repairs) — per-hospital MRF scrape (GitHub index) | — |

- Registry stayed **901** rows (3 in-place UPDATEs, no duplicates); `INCLUDE=Y` 11→14. **The 2 failures
  left zero partial state** — no landing table, no `INGEST_RUNS` row, registry untouched — so they remain
  queued for a retry. Clean graceful-failure behaviour.
- Takeaway: 60% landed, but **`dbt build` then exposed quality gaps the batch's "success" counter missed**
  (see hardening below). The real tally: 2 clean (clinicaltrials, biorxiv), 1 good-data-but-broken-models
  (cms_hcris, since fixed), 1 garbage (cms_hpt_enforcement HTML). Both hard-fails are scrape/JS shapes — the
  case for **C** (a scrape + incremental/bulk path).

### dbt build + agent hardening (2026-06-17) — `dbt build` the 4 newly-onboarded sources
Building the marts (not just generating models) surfaced two systemic agent bugs and got fixed:
- **`fed_cms_hpt_enforcement` was a false success**: the generated fetch hit a docs/landing URL, so pandas
  parsed an HTML page into one bogus column (`DOCTYPE_HTML`, 22 junk rows). The mart wouldn't build → caught.
  **Fix**: `ingest._reject_html()` now fails the LOAD loudly when the payload is an HTML page / single
  `<…>`/`DOCTYPE` column. Dequeued 2026-06-17 (Chris's OK): registry un-flagged, junk landing table dropped.
  Re-onboarding it later needs `--include-landed` (the bad run still sits in `INGEST_RUNS` history).
- **`fed_cms_hcris` staging wouldn't compile**: dbt-gen built SQL from recon's *guessed* schema
  (`PROVIDER_NUMBER`) but the CSV landed `PROVIDER_CCN` + 116 other real columns. **Fix**:
  `scaffold_dbt._actual_landing_columns()` introspects the real landing columns and generates against those;
  dbt-gen `max_tokens` 8192→16384 for very wide tables. Regenerated → builds green (mart = 6,103 rows).
- **Built green now**: `health__fed_clinicaltrials` (500), `science_research__xc_biorxiv_medrxiv` (432),
  `health__fed_cms_hcris` (6,103) — all materialized into `LIBRARY_MARTS.DBT_CROGERS`.

### C2 — incremental load (2026-06-17), built + proven live
The agent now does two load modes. **Incremental** (for huge/daily-growing sources): `run_ingest` reads the
`MAX(cursor_field)` watermark from landing, hands it to the fetch as `context["since"]`, fetches only newer
rows, and **appends** (`overwrite=False`); landing is an append log, staging dedups on the primary key.
First run (empty table) → bounded backfill; a run with no new rows → clean no-op (not an error).
- Touchpoints: `ingest.run_ingest` (+ `_watermark`, `_execute_fetch(since, allow_empty)`,
  `_load_landing(overwrite)`), `recon` emits `load_mode`/`cursor_field`/`primary_key`, prompts updated. No new deps.
- **Proven on CFPB consumer complaints** (`fed_cfpb_complaints`) — the canonical "wrong shape for snapshot"
  parked source: run 1 backfilled 250; run 2 **read watermark `2026-05-15T23:59:55Z`** and appended 250 more
  forward → landing **500**, 2 `INGEST_RUNS` rows, registered `INCLUDE=Y`. Append + watermark-advance confirmed.
- Trade-off (ADR in `docs/design-incremental-and-scrape.md`): incremental breaks the snapshot-replace raw
  invariant for these sources — landing becomes append-only. Mitigated: still all-TEXT + provenance; clean
  current state lives in staging.

### C3 — chunked / streaming load (2026-06-17), built + PROVEN live on NPPES
The third load mode, for a SINGLE file too big for memory (the NPPES ~9 GB CSV, big bulk ZIPs) that was
OOM-killing the agent (exit 137 — pandas balloons a 9 GB string-column CSV to 30–50 GB, past the 16 GB box).
**snapshot + incremental paths untouched** — chunked is a separate `run_ingest` branch.
- **Autonomy**: recon flags `load_mode=chunked` when est_volume/format implies a multi-GB download
  (verified: NPPES recon picked `chunked` + `bulk_zip`, "~9 GB uncompressed"). Codegen writes `fetch_data`
  as a **generator** that yields DataFrame chunks of `context["chunk_rows"]` (50k default), streaming the
  download (`pd.read_csv(chunksize=)`, or stream-to-temp-file + `zipfile` for ZIPs).
- **Loader** (`ingest._run_chunked` / `_load_landing_chunked`): writes each chunk to the SAME landing table
  with the SAME provenance stamps — first fresh chunk replaces the table, the rest append, so peak memory is
  ~one chunk regardless of file size. Each row carries its chunk's SHA-256; `INGEST_RUNS` gets a manifest SHA
  over all chunk hashes. Config: `ONBOARD_CHUNK_ROWS` (50k), `ONBOARD_CHUNK_MAX_ROWS` (0 = unlimited).
- **Resume**: the landing row-count is the progress ledger. A crash leaves landed chunks + no `success`
  `INGEST_RUNS` row → a re-run detects that, passes `resume_from_row` (skip already-landed), and appends. A
  re-run AFTER success = clean full reload (overwrite). All three proven on a synthetic source (fresh 300,
  reload-no-dup 300, crash→resume 100+200=300).
- **PROVEN on NPPES** (`fed_cms_nppes`) — the source that OOM-killed every batch: full agent run, all 5
  checkpoints, **exit 0**. Streamed **300,000 rows × 333 columns** into `LIBRARY_RAW.LANDING.FED_CMS_NPPES`
  (6 chunks, 6 per-chunk SHAs, manifest sha `e5022b4f053e`), `INGEST_RUNS` success (433 MB processed),
  registry `INCLUDE=Y`. **Peak Python RSS 2,999 MB** — bounded + constant per chunk (lower `chunk_rows` to
  shrink it for very wide tables), vs the 30–50 GB the whole-file load needed. Demo-capped at 300k via
  `ONBOARD_CHUNK_MAX_ROWS`; uncap to land all ~8.5 M providers with the same flat memory.

### C3 — full uncapped big loads (2026-06-18): NPPES + FJC landed, transatlantic failed
Used C3 to land the 3 files that OOM-crashed pre-C3. **2 of 3 fully onboarded; 1 genuine source failure.**
- **`fed_cms_nppes` — 9,606,683 rows (FULL file, to EOF)**, `INCLUDE=Y`, ingest success. The 9 GB,
  333-column provider file — streamed in 50k/200k-row chunks at **1.2–5.9 GB peak RSS** (vs the prior
  exit-137 OOM). This took a container restart (cut at 9.05 M) **and** a 90-min timeout (cut at 9.45 M)
  before a **resume run** finished the 156,683-row tail to EOF and logged a clean success — a real-world
  proof of crash-resume. Landing carries 2 run_ids (bulk + tail) = honest provenance.
- **`fed_fjc_idb` — 4,126,450 rows**, `INCLUDE=Y`, ingest success. Federal court cases (FJC IDB).
- **`fed_slavevoyages_transatlantic` — FAILED** (genuine): no clean export endpoint — codegen got
  "not a zip file", then an HTML page; the `_reject_html` guard correctly rejected it (3 repairs → abort).
- **Three agent fixes this run forced (committed)**:
  1. **Streaming LLM calls** (`llm._real_call` → `client.messages.stream`): bumping dbt-gen `max_tokens`
     tripped the Anthropic SDK's "Streaming is required for operations >10 min" guard, which aborted the
     **dbt checkpoint for every big source** (FJC landed but didn't register until this was fixed). Now
     streams + reassembles — works at any `max_tokens`.
  2. **Wide-table dbt-gen** (`scaffold_dbt`): >60-col tables (NPPES 333) blew the JSON past `max_tokens` →
     truncation. Now a compact passthrough directive + key-only tests; `max_tokens` 16k→24k (safe w/ streaming).
  3. **Framework-enforced resume-skip** (`_load_landing_chunked`): the loader drops already-landed rows
     itself (codegen always yields from the start) — dup-safe regardless of the generated code.
- **Note**: X-Small `DBT_WH` write throughput is the real limiter on the very biggest files (~50k-row chunks =
  ~190 COPYs for NPPES). Larger `ONBOARD_CHUNK_ROWS` (200k used for the resume) cuts round-trips; memory still
  bounded. transatlantic stays queued — it needs a source-specific fetch (search/export UI), not more retries.
- Wide-table note: NPPES is 333 columns — checkpoint-4 dbt-gen truncated its JSON once (max_tokens) but
  self-recovered on auto-repair 1. Very wide tables remain a dbt-gen stress point (raise max_tokens further
  or emit YAML/SQL outside JSON) — tracked, not blocking.

### Thin-scrape fixes + Registry batch 5 (2026-06-18)
**Pagination prompt fix** then two phases. Strengthened the codegen scrape guidance (loop pages via
next-link/`?page=N`/offset until no new records; a few-row result is a "you stopped at page 1" signal) —
the thin landings had happened because a 1-row scrape is a non-error *success*, so auto-repair never fired.

**Phase 1 — re-ran the 4 thin scrapes** (dropped the thin tables, forced `snapshot` for a clean overwrite,
paginated prompt). **3 of 4 improved:**
- `fed_nara_wra_aad` 4 → **36** · `intl_ch_zefix` 1 → **18** · `fed_fdic_enforcement` 2 → **14**
- `fed_doj_crt_cases` 1 → **1** (resistant — JS-driven case search; pagination prompt didn't crack it. A
  thin scrape can't self-correct via auto-repair; needs `scrape_js` + click-through, parked).

**Phase 2 — next 12 fresh tier-1** (international registries/APIs). **12 attempted, 7 landed, 5 failed:**

| Source | Result | Rows |
|---|---|---|
| `intl_ember_elec` | ✅ Ember global electricity | 369,264 |
| `intl_it_istat` | ✅ Italy ISTAT (SDMX, incremental) | 213,284 |
| `intl_ec_sercop` | ✅ Ecuador procurement (**chunked** — recon picked it autonomously) | 132,995 |
| `intl_hudoc` | ✅ ECHR case-law (incremental) | 2,000 |
| `intl_gr_gemi` | ✅ Greece business registry | 40 |
| `intl_es_borme` | ✅ Spain BORME gazette (incremental) | 25 |
| `intl_ie_cro` | ✅ Ireland CRO — ⚠ thin (3), review | 3 |
| `intl_cz_ares` `intl_fi_ytj` `intl_fr_insee` `intl_ge_spa_procurement` `intl_jp_nta_houjin` | ❌ aborted (3 repairs) | — |

The 5 failures are foreign registry/stat APIs with awkward shapes or key/appID requirements (ARES XML, YTJ,
INSEE token, Georgia procurement, Japan NTA houjin-bangō appID). Net **+717,672 rows**; Library now **45
tables, 23,788,352 rows**. New thin to review: `intl_ie_cro` (3), plus the still-resistant `fed_doj_crt_cases` (1).

### C1 — static scrape (Phase 1, 2026-06-17), built + proven
For sources with no clean file/API. Changes: codegen prompt gained scrape + bounded-crawl + browser-UA
guidance; `lxml` added to requirements (so `pandas.read_html` works); and **the HTML-guard was corrected**
— it now judges the DataFrame's *shape* (a single HTML-ish column = junk) instead of the raw bytes. The
old raw-bytes check wrongly rejected ALL legitimate scrapes (a scraped page's raw bytes are HTML by
definition); the shape check still catches the `fed_cms_hpt_enforcement`-style single-column junk.
- **Proven**: deterministic scrape of the "largest US companies by revenue" table (Wikipedia) → **100
  clean rows** (RANK/NAME/INDUSTRY/REVENUE/EMPLOYEES/HQ) into `LIBRARY_RAW.LANDING` (unregistered demo table).
- The **full agent** also wrote correct BS4 scrape code for BAILII UKSC cases and **failed gracefully** on
  BAILII's bot-detection wall (3 repairs → clean abort, no junk landed). Codegen quality confirmed.
- **KEY FINDING**: most accountability scrape targets are **bot-protected (BAILII) or JS-rendered**, so
  static BS4 has limited reach. **C1b (Playwright + a real browser session) is the actual unlock** for
  these — now a higher priority than originally scoped (evidence-driven).

### C1b — headless-browser scrape (Playwright, 2026-06-17), built + PROVEN live
The third fetch capability (after static `scrape`). For JS-rendered / bot-protected sources static BS4
can't reach. New `browser.py` exposes `render(url, wait_selector=, scroll=, timeout_ms=)` — drives a real
headless Chromium, runs the page JS, clears the bot challenge, returns fully-rendered HTML that the
generated `fetch_data` parses with BS4 exactly like a static page.
- **Agent chooses it autonomously** (mirrors C2's `load_mode`): recon's `access_pattern` enum gained
  `scrape_js`; `ingest._execute_fetch` always injects `context["render"]`; the codegen prompt tells Claude
  to use it for `scrape_js`. **Recon can now read walled pages too** — `fetch_page` detects a challenge /
  empty shell (`browser.looks_blocked`) and escalates to the browser to profile the real source.
- **Optional + heavy**: Playwright pip pkg is small but drives a ~170 MB browser (`playwright install
  chromium`). Imported **lazily** — the agent runs fine without it; `render()` raises actionable install
  steps. Only `scrape_js` sources pay the cost. Trade-offs ADR in `docs/design-incremental-and-scrape.md`
  (slower, heavier RAM/CPU, container libs, `--no-sandbox`, `ignore_https_errors` for proxied TLS, basic
  bot checks only — not hard CAPTCHAs).
- **PROVEN — same target, before vs after** (`scripts/prove_c1b_bailii.py`, run through the real
  `ingest._execute_fetch`): BAILII UK Supreme Court 2024 index
  (`https://www.bailii.org/uk/cases/UKSC/2024/`).
  - BEFORE (`scrape`, requests+BS4): HTTP 200 but a **4.5 KB bot-challenge shell, 0 case links** → raised,
    **landed nothing** (clean graceful failure — exactly the documented C1 wall).
  - AFTER (`scrape_js`, `context["render"]`+BS4): challenge cleared → **44 UK Supreme Court 2024
    judgments** (title + URL) into a clean DataFrame. Recon autonomy independently verified (read real
    case names through the browser).
- **NOTE on the C1b PR container**: that earlier proof exercised the full RECON→SCRIPT→LOAD-*fetch* path
  (render injection + generated `fetch_data` + HTML-junk guard). The Snowflake **write** + real-LLM codegen
  weren't run there (placeholder creds). Now done — see below.

### C1b — FULL end-to-end live proof through `onboard.py` (2026-06-17, real creds)
Ran the whole agent (`onboard.py --url …`, `ONBOARD_AUTO_APPROVE=1`) with a real `ANTHROPIC_API_KEY` +
write PAT (`ACCOUNTADMIN`) + `DBT_WH`, browser at `/opt/pw-browsers`. All 5 checkpoints green, exit 0:
- **RECON → `access_pattern=scrape_js` autonomously**, **codegen wrote `context["render"](url,
  wait_selector=".quote")`**, Playwright cleared the JS shell, **LOAD landed 100 rows** →
  `LIBRARY_RAW.LANDING.INTL_DEMO_QUOTES_TOSCRAPE_JS` with full provenance (`_INGESTED_AT` /
  `_SOURCE_RUN_ID` / `_SRC_SHA256`), one `success` row in `INGEST_RUNS` (100 rows, 93,596 B, sha
  `03c989fc4da3`), and a `SOURCE_REGISTRY` row (`INCLUDE=Y`). Verified independently via the read-only
  MCP role. DBT checkpoint also ran (demo models written, not committed — see target note).

**Target = `quotes.toscrape.com/js` (a JS-render sandbox), NOT BAILII — and why:**
- **BAILII's bot wall is intermittent / IP-reputation-based.** At run time it served the *real* page to a
  plain `requests` GET (12 KB, 0 challenge markers) — so recon *correctly* called it plain `scrape`, and a
  scrape_js proof on it would've been theatre. (This is exactly the "fragile / arms-race" trade-off in the
  ADR.) BAILII still works via static scrape right now; it just isn't a JS wall *today from this IP*.
- Swept the queue's real JS candidates: **OECD** data-explorer is a true JS shell (0 visible chars static)
  but headless render returns an SPA *error* page (needs bespoke UI-driving); **ICIJ**/`pages/database`,
  OpenSanctions, GDELT, GFW, supremecourt.uk are all server-rendered (real content static → plain scrape).
  None cleanly exercises scrape_js from a single URL. `quotes.toscrape.com/js` reliably does: static = 0
  data rows (JS shell), render = real quotes. Registered with NOTES flagging it a demo to exclude from
  real analysis. **It can be dropped on request** (`DROP TABLE LIBRARY_RAW.LANDING.INTL_DEMO_QUOTES_TOSCRAPE_JS`
  + delete its `SOURCE_REGISTRY` / `INGEST_RUNS` rows).

**Autonomy hardening this exposed (committed):** recon was picking `scrape` even for JS shells because it
*escalates to the browser to read walled pages*, so the LLM saw clean rendered HTML and mislabeled it. Fixes:
(1) `browser.looks_blocked` now judges **visible text** (a JS SPA shell is 100+ KB of HTML with ~0 visible
chars — the old raw-byte-length test missed it); (2) `recon.fetch_page` returns a `browser_required` signal
(static was blocked, only render worked); (3) `recon._resolve` **forces `access_pattern=scrape_js` on that
empirical signal** rather than trusting the LLM. Deterministic across repeated runs after the fix.

### Batch 3 — `fed_treasury_avg_interest_rates` (2026-06-17), verified live
- LOAD → `LIBRARY_RAW.LANDING.FED_TREASURY_AVG_INTEREST_RATES` = **4,961 rows**, run `4046bcc7…`,
  sha `7fe37899…` (the same sha is on every row's `_SRC_SHA256` and on the `INGEST_RUNS` row — provenance chain intact).
- `INGEST_RUNS` → one `success` row (4,961 rows, 1.65 MB, ~11s).
- `SOURCE_REGISTRY` → new `INCLUDE=Y` row (Economy / Federal Debt & Interest Rates; join keys
  `record_date, security_type_desc, security_desc`). The curated `fed_fiscaldata_treasury` family row was NOT clobbered.
- Verified independently with the read-only MCP role (`CLAUDE_MCP_READONLY`); the agent wrote via the
  env PAT (`ACCOUNTADMIN`).
- **dbt for batch 3 is RUN** (2026-06-17): `dbt build` created the staging view
  `stg_fed_treasury_avg_interest_rates__avg_interest_rates` (`LIBRARY_STAGING.DBT_CROGERS`) + the mart table
  `economics__fed_treasury_avg_interest_rates` (`LIBRARY_MARTS.DBT_CROGERS`, 4,961 rows, surrogate key 1:1
  unique). Final: **PASS=18, WARN=0, ERROR=0**. One fix: the agent's `accepted_values` on
  `security_type_desc` was wrong (guessed five `Total *` labels from a *different* Treasury dataset) —
  corrected to the 3 real categories `Marketable / Non-marketable / Interest-bearing Debt` (a real guard,
  not downgraded to warn, since the categories are stable + exhaustive across the full history).

- **dbt is RUN** (batches 1–3): all **12 models** (6 sources × staging view + mart table) build into
  `LIBRARY_STAGING.DBT_CROGERS` / `LIBRARY_MARTS.DBT_CROGERS` — 0 errors. (USAspending agencies has no dbt
  models — its first load skipped checkpoint 4.)

### Session 2026-06-20 — env recovery, warehouse verified, dbt cleanup (PR #14 + #15)
Fresh ephemeral container, **no new sources** — got the stack live again and cleaned the dbt project.
- **Connection recovered (PR #14)**: the container's injected `SNOWFLAKE_PAT` was **dead** (`394400 invalid
  token`), which also killed the read-only MCP server (same bearer token). Fix: new PAT into gitignored
  `library-onboarding/.env`; `config.py` now `load_dotenv(override=True)` so `.env` wins over stale container
  vars (empty `SNOWFLAKE_WAREHOUSE`, dead PAT); set `SNOWFLAKE_WAREHOUSE=RIPPLE_WH`, `SNOWFLAKE_ROLE=ACCOUNTADMIN`.
  Installed `requirements.txt` (needed `--ignore-installed` to shadow two apt-pinned pkgs — PyJWT, cryptography),
  `dbt-snowflake 1.11.5`, `dbt deps` (dbt_utils 1.3.3). **Live connection proven via `snow.connect()`.** New
  PAT `exp` = **2026-07-05** — rotate before then.
- **Warehouse verified (read-only sweep)**: 5 DBs (`LIBRARY_RAW/META/STAGING/MARTS/TOOLS`); **45 landing
  tables / 23,788,352 rows** (matches the ledger); `SOURCE_REGISTRY` 901 rows (40 `INCLUDE=Y`); `INGEST_RUNS`
  57 runs / 49 distinct sources. **Materialization (after the dbt build below): all 35 modeled sources built
  in `…DBT_CROGERS` — 53 models green (was 9 of 36 at the start of this session).**
- **dbt reconciled + cleaned (PR #14 + #15)**: of 36 dbt source refs, 35 matched a live table; 1 **ghost**
  removed — `fed_cms_tic_mrf` (models existed, no landing table — the un-flagged false-success) → staging dir
  + schema.yml + mart deleted. Fixed **4 YAML bombs** (unquoted descriptions with embedded `: ` → `mapping
  values are not allowed`): `fed_revolvingdoor_project`, `fed_mapping_inequality` (×2), `intl_es_borme`.
  **Renamed** the revolvingdoor intermediate `…_personnel_positions` → `…__positions_sectors` to match its
  schema.yml (mart reads staging directly → ref-safe), reattaching its 10 orphaned tests. **`dbt parse` exit
  0; WARNING 14 → 3** (the 3 left are the parked deprecations). 10 landing tables remain un-modeled
  (early-proof + Wayback + a few others) — raw-only, not broken.

## DECISIONS MADE
- **Snowflake cleanup + rebrand (2026-06-17, Chris ran the DDL).** Dropped dead DBs (`RIPPLE` v3,
  `RIPPLE_PRESERVE` [empty — vault never populated], `STORMS`, `STORM_LOCATIONS`, `WEATHER_PROJECT`,
  `TEST`) + the two `DISASTER_IMPACT.PUBLIC.MY_*_DBT_MODEL` tutorial leftovers. **Renamed the live
  Library DBs**: `RIPPLE_RAW→LIBRARY_RAW`, `RIPPLE_META→LIBRARY_META`, `RIPPLE_STAGING→LIBRARY_STAGING`,
  `RIPPLE_MARTS→LIBRARY_MARTS`. Repo updated to match (database-name refs → `LIBRARY_*`; the `RIPPLE_*`
  env-var *keys* stay — the project is still "Ripple", only the warehouse DBs were rebranded). Verified:
  `SHOW DATABASES` (4 `LIBRARY_*` present, all `RIPPLE*` gone) + `dbt compile` green against the renamed
  stack (compiled SQL resolves to `LIBRARY_RAW.LANDING.*`). `RIPPLE_WH` warehouse unchanged (compute, not a DB).
- **`DISASTER_IMPACT` + `WEATHER_ANALYSIS` dropped (2026-06-18).** `DISASTER_IMPACT` was a frozen April dbt
  build (308 GB, ~50B rows of weather/ACS/econ staging in `DBT_CROGERS`, untouched 2.5 months); dependency
  check was clean (no LIBRARY view/registry/object refs) so it was dropped — reclaim clears over ~7 days of
  Failsafe. `WEATHER_ANALYSIS` was an empty shell (no user objects) — dropped too. Account is now the 4
  `LIBRARY_*` DBs + Snowflake system/shared. **MCP-server side-effect — RESOLVED**: the read-only Snowflake
  MCP server was hosted at `DISASTER_IMPACT.DBT_PROD.CLAUDE_MCP_SERVER`, so the drop disabled the MCP tool.
  Re-provisioned 2026-06-18 in a new no-data container **`LIBRARY_TOOLS.PUBLIC.CLAUDE_MCP_SERVER`** (identical
  spec recovered from `QUERY_HISTORY`; `SYSTEM_EXECUTE_SQL` tool `sql_exec_tool`), with `USAGE` re-granted to
  `CLAUDE_MCP_READONLY`. Server verified live (`SHOW MCP SERVERS`); **remaining client-side step (external):
  repoint the MCP integration's server path from the old `DISASTER_IMPACT...` to `LIBRARY_TOOLS.PUBLIC...`**.
  Lesson: don't host tooling/infra inside data DBs. The agent's own PAT connection was the fallback throughout.
- Target the live `LIBRARY_*` stack. — Chris, 2026-06-16
- `SOURCE_ID` is the linchpin; landing table = `UPPER(SOURCE_ID)`; prefixes `fed_`/`intl_`/`xc_`/`loc_`/`st_`.
- Catalog is Snowflake-native (`SOURCE_REGISTRY`); raw is an all-TEXT snapshot-replace mirror.
- Compute = `RIPPLE_WH`; the session env leaves `SNOWFLAKE_WAREHOUSE` blank, so the runners self-default it.
- Pin narrow `source_id`s so the upsert inserts a new row instead of clobbering a curated family row.
- Codegen prompt forbids substituting a host/endpoint from memory (the FDIC failure), AND avoids paging
  huge/unbounded sources — fetch a bounded snapshot (the CFPB runaway: it tried to mirror millions of rows).
- dbt builds into `DBT_CROGERS` (not the existing `CORE` schemas); over-strict auto-generated tests on
  real gov data are downgraded to `severity: warn` (Treasury historical nulls, FDA recall-type drift).
- **`.env` is the source of truth (2026-06-20).** `config.py` loads it with `override=True` so a fresh
  container's stale/injected env can't shadow it (dead `SNOWFLAKE_PAT`, empty `SNOWFLAKE_WAREHOUSE`). The PAT
  lives only in the gitignored `.env` — never committed (verified absent from git history). Rotate by ~2026-07-05.

## PARKED IDEAS
- [IDEA — HOT] **Tier-aware bridge dedup.** `bridge.discover_bridged` drops a transitive edge whenever the
  pair has ANY direct edge — so a weak GEO/ZIP edge suppresses a strong CCN→NPI entity bridge (this is why
  facility↔LEIE "banned but operating" edges vanish). Fix: only dedup a bridge against a direct edge of
  EQUAL-OR-STRONGER tier (STEEL/STRONG). | WHY: surfaces the flagship lens as a first-class graph edge. | LAYER: Library
- [IDEA — HOT] **Per-watchlist fanout relax.** The fanout guard (FANOUT_MAX=40) correctly kills junk but also
  drops a big hospital's CCN before it can bridge to a banned provider. For a SMALL high-value watchlist
  endpoint (LEIE 8,775 banned NPIs), a hospital→banned-provider hop matters even at high fanout. Allow a
  higher/disabled fanout when one endpoint is a curated watchlist. | LAYER: Library
- [IDEA — HOT] **Materialize `connect__banned_but_operating` dbt mart** from the crosswalk×LEIE join (the
  38-affiliation query): banned provider → exclusion type/date → affiliated facility (CCN, name, type). First
  shippable story from the connected Library. | LAYER: Library/Publishing
- [IDEA — SOMEDAY] **Pour IRS EO BMF** (1.97M nonprofit EINs, `https://www.irs.gov/pub/irs-soi/eo_<st>.csv`)
  as the EIN endpoint for the follow-the-money side. Lights NO bridge alone (no public EIN crosswalk) but
  anchors future EIN crosswalks + NAME@ZIP corroboration with nonprofit hospitals. | LAYER: Library
- [DONE 2026-06-17] Drive the queue from `SOURCE_REGISTRY` (by `PRIORITY_TIER`) instead of the static list.
  → `registry_queue.py` + `registry_batch.py`; proven with `xc_biorxiv_medrxiv`.
- [DONE 2026-06-17 — C2] Incremental load path (append-only landing + watermark + staging dedup). Built in
  `ingest.py`/`recon.py`/prompts; proven live on `fed_cfpb_complaints`. Design: `docs/design-incremental-and-scrape.md`.
- [DONE 2026-06-17 — C1 Phase 1] Static scrape (BS4 + `lxml` + corrected HTML-guard); proven on a Wikipedia
  table (100 rows). Codegen writes good scrape code (BAILII) but most targets are bot-protected/JS-rendered.
- [DONE 2026-06-17 — C1b] Playwright + real browser session for bot-protected / JS-rendered scrape targets.
  → `browser.render()` + `access_pattern=scrape_js` + recon browser-escalation; proven on BAILII UKSC
  (blocked static → 44 judgments rendered). Trade-offs ADR in `docs/design-incremental-and-scrape.md`.
- [IDEA — SOMEDAY] The agent writes a `sources:` block into every model's `schema.yml`; it should emit a
  single central `sources.yml` instead. | NOTE: dbt 1.11 actually tolerates the per-file blocks (parse +
  build are clean) — it only collides if you ALSO add a central one. Cosmetic, not blocking. | LAYER: Library
- [IDEA — SOMEDAY] **dbt deprecation sweep** — the agent's generated test YAML trips dbt 1.11 deprecations:
  **148× generic-test args should nest under `arguments:`** + **57× `severity` should move under `config:`**
  (these are the 3 WARNING lines left after the 2026-06-20 cleanup). Works now (warnings only). Update the
  codegen prompt + existing schema.yml files **before any dbt major bump** turns them into errors. | LAYER: Library

## OPEN QUESTIONS
- The PAT authenticates as `ACCOUNTADMIN` — a least-privilege role scoped to `LIBRARY_RAW` + `LIBRARY_META`
  (+ `LIBRARY_STAGING`/`LIBRARY_MARTS` for dbt) would be safer for routine onboarding.

## NEXT ACTION
**Bridge layer is ACTIVATED — 646 tables, 14,694 connections, 59 bridges; every CMS facility type now reaches
NPPES + LEIE on entity keys.** Uncommitted: the 8 new landings are live in Snowflake; `scripts/bridge_fuel_*`,
the merged fingerprint, and the rebuilt graph/explorer are on disk (not yet committed/PR'd). Best next moves
(Chris to pick):
1. **Ship the first story** — materialize `connect__banned_but_operating` (the crosswalk×LEIE 38-affiliation
   query: banned provider → exclusion → affiliated facility). Highest-value, lowest-effort; it's a real lead set.
2. **Tier-aware bridge dedup + watchlist fanout** (both HOT in PARKED) — so facility↔LEIE shows as a
   first-class graph edge instead of being masked by a weak ZIP edge / fanout-gated. Makes the flagship lens
   visible in the explorer, not just a query.
3. **Commit + PR** the 8 sources + loader + the corrected bridge premise.
4. **EIN/follow-the-money** — pour IRS EO BMF (1.97M nonprofit EINs) as the EIN endpoint; lights no bridge
   alone but seeds corroboration with nonprofit hospitals (NAME@ZIP) and any future EIN crosswalk.
5. (Ops) `ANTHROPIC_API_KEY` is MISSING from `.env` — the LLM onboard agent can't run until it's added (the
   deterministic `bridge_fuel_load.py` sidesteps it for known-shape sources). PAT rotates ~2026-07-05; dbt
   reads OS env not `.env` — `source library-onboarding/.env` before any dbt command.

**Re-run the map any time:** `python -m connect discover` then `explore` (full rebuild is slow at 646 tables
until the deferred incremental-cache is built). **Load more known-shape fuel:** add a dict to
`scripts/bridge_fuel_specs.py` and `python scripts/bridge_fuel_load.py --spec <id> --run`.
