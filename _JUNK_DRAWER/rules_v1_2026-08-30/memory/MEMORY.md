# Memory Index
- [No Default Artifact Publish](feedback-no-default-artifact-publish.md) — 2026-08-30: stop auto-publishing Claude artifacts for Ripple pages; the repo HTML file is the real standalone deliverable, only publish if Chris explicitly asks for the link
- [The Handbook Is the Chain Explorer](feedback-the-handbook-is-the-chain-explorer.md) — 2026-08-30 crashout: "the handbook" = the PUBLISHED chain-explorer artifact, not the repo rail-and-detail page; read the artifact before touching it, mirror its HTML into the repo
- [Place Columns Verified 2026-08-30](place-columns-verified-2026-08-30.md) — 72% of 2,238 place columns are what their name says; trap list (LONG/LAT false hits, lost leading zeros, 0,0 coords, numeric state codes); Snowflake REGEXP_LIKE matches the whole string
- [Spine Is Red Lane](feedback-spine-is-red-lane.md) — 2026-08-30 near-miss: "wire it up" (about the handbook doc) almost triggered a live spine run; ANY spine command needs Chris asked first, no exceptions, dry-run or not
- [Plain-English Relapse](feedback-plain-english-relapse-2026-08-29.md) — 2026-08-29: results briefs drifted into method jargon (level 3 / edges / namespaces); reread every results message as bar talk before sending
- [Connections Pass 2 2026-08-29](connections-pass2-2026-08-29.md) — GLEIF L2 parent tree held+unused; TRI↔FRS live via EPA_REGISTRY_ID; HMDA respondent id = 2 namespaces; NADAC↔NDC needs 5-4 padding; IDV + Fed holding-co files top missing; catalog 'not held' wrong on 37
- [No-Brainer Acquisitions 2026-08-29](nobrainer-acquisitions-2026-08-29.md) — SAM public extract / USCG vesdoc (Wayback only) / FMCSA census / EPA CAMPD landed; GLEIF L2 + NDC dir + GUDID were ALREADY held; access quirks per source
- [Time and Place Are Joins](time-and-place-are-joins.md) — 2026-08-29 DECISION: same day/month + same state/district/county is a first-class join with no ID needed; ID spine deprioritized; Chris drives step by step
- [No Jumping Ahead](feedback-no-jumping-ahead.md) — 2026-08-29 STANDING RULE: answer the question asked and stop; no build plans/costs/next steps/verdicts unless Chris says "think it through" or "brainstorm"
- [Rebuild Cost Per Key Batch](feedback-rebuild-cost-per-key-batch.md) — 2026-08-29 crashout: "don't wait, it won't matter" hid that then RESOLVED same day: rebuild really costs ~50 min/$2–3 (stale quote), and apply-config now applies key/spec changes as bounded reslices — no full rebuild per batch; always pull real rebuild duration from query history before quoting
- [Official ID Inventory 2026-08-29](official-id-inventory-2026-08-29.md) — master have-vs-missing list: 26 wired / ~50 held-but-unregistered (CAGE, PECOS, EIA plant, FDIC cert/RSSD) / ~30 not held; check bucket B before landing new sources
- [Thinks in Data Models](user-thinks-in-data-models.md) — Chris's native mental model is SQL results/spreadsheets, not prose — explains the list-formatting preference
- [List Means Table](feedback-list-means-table.md) — default to tables for any 2+ comparable items, not just when he types "list"; "like cells in Excel, not your yapping"
- [Verify "Done" Claims Before Stating Them](feedback-verify-done-claims-before-stating.md) — 2026-08-27 crashout: said "depth is solved" off one report's headline, own sweep found ~80x/~14,000x truncations hours later; name the method's blind spot and run the disconfirming check BEFORE any you're-good verdict
- [Audit Scripts Must Not Hardcode Verdicts](audit-scripts-must-not-hardcode-verdicts.md) — 2026-08-26: the warehouse audit name-matched schemas into "dead"/"junk" verdicts and summed uncounted views as 0 rows (39% of objects unmeasured); nearly caused DROP DATABASE on the live SQL-runner's default DB
- [Verify Inventory Before Computing](feedback-verify-inventory-before-computing.md) — 2026-08-26 crashout: hardcoded 5-db list silently missed 2 real databases + duplicated an existing audit; always SHOW DATABASES + check for existing reports before a fresh sweep
- [Ripple Portfolio Webflow Site](board-segments-webflow-2026-08-23.md) — site_id/page_id for Chris's personal portfolio Webflow site + where the blueprint design-system source file lives and how to decode it
- [Verify Mechanism Before Rebuilding](feedback-verify-mechanism-before-rebuilding.md) — 2026-08-23: after ONE rejected metaphor-led build, confirm the mechanism next (restate or AskUserQuestion previews) — don't guess a third time as a new artifact; same failure recurs in brief-writing (spec vs concept) and scope-guessing (alternates vs "use what's already chosen"), not just artifact builds
- [Toolbox Not Marketing Copy](feedback-toolbox-not-marketing-copy.md) — 2026-08-23: personal working-tool artifacts need plain functional presentation, not hero taglines/pill-UI/superlatives; confirm if "toolbox" means literally interactive before building static
- [Year-Killer Typing Trap](year-killer-typing-trap.md) — 2026-08-22: 61 year columns mis-ruled as dates → guarded cast NULLed them in 29 built marts (Treasury/Open Payments/PBGC/OSHA/foreign aid); massive "duplicates" can be a destroyed grain dimension; rule years ambiguous_number, never date
- [Anchored-Perspective Communication](feedback-anchored-perspective-communication.md) — 2026-08-22 STANDING ORDER: report state as anchor score (0-100 + split) → what moved it → drags → ranked levers, portfolio view + bar-version blockquote in the same message; deltas without a fixed frame lose Chris
- [Quick-Wins Fix Session 2026-08-22](quick-wins-fix-session-2026-08-22.md) — a third of the fix list was stale (openFDA "wipe" = VARIANT rows≠records trap); live-verify defects before fixing; gate map: single DROP ok / batches blocked, --refresh not --force, config-disable not file-delete
- [Standalone HTML in Repo](feedback-standalone-html-in-repo.md) — 2026-08-22: every artifact page also lands as self-contained HTML in reports/viz/ (with build scripts in _build/); artifacts are mirrors, the repo copy is the durable original
- [Cost Runaway Alert](feedback-cost-runaway-alert.md) — 2026-08-22: pull REAL credits from the meter during long sessions; alert immediately, unprompted, if the day trends past ~$50 toward a $300 day
- [Warehouse Truncation Findings 2026-08-22](warehouse-truncation-findings-2026-08-22.md) — CONTRACTS_FULL is a 2-3-months-per-FY sample; PSC was 56% loaded (silent chunk death, remainder reloaded); DOL API re-pull quirks; exact round counts = truncation hypothesis
- [Ripples Thinking Model](ripples-thinking-model.md) — 2026-08-21 HOLY GRAIL: docs/RIPPLES.md is Chris's permanent lens (Game-of-Life five pieces; State/Neighbors/Flow Ripples; rules layer is the unbuilt frontier; 4 landmines are load-bearing)

- [Talk Like a Person, Not a Memo](feedback-talk-like-a-person.md) — plain sentences, glanceable always: no memo-formatting for conversation, no walls of prose for narrative — short paragraphs, white space, one idea per line
- [Time Censoring Traps + The Free Denominator](time-censoring-traps.md) — 2026-08-20: raw lag/duration ALWAYS shrink toward the present; rank on fixed horizons after waiting out the p90 tail; events-per-living-entity needs no second table
- [Aggregate Sweep Cost Calibration](aggregate-sweep-cost-calibration.md) — 2026-08-20: 771 queries over the whole warehouse = 14 min and ~$1-2, not the $12-20/3-6h quoted; price read-only sweeps by bytes scanned, not table count
- [Census Date Numbers Are Unreliable](census-date-numbers-are-unreliable.md) — 2026-08-20: the Aug-17 census only measured typed DATE columns and reported min/max, so it missed 143 real clocks and cried corruption on healthy tables; use reports/time_index/ instead
- [Two Machines, Two Snowflake Key Slots](two-machine-snowflake-keys.md) — 2026-08-20: Mac holds slot 2, Windows box holds slot 1; rotating without --slot locks the other machine out; "JWT token is invalid" now means the other machine rotated
- [Pre-Response Checks](feedback-pre-response-checks.md) — 2026-08-18: silent 8-point checklist (specificity/contradiction/real-intent/confidence/repackaging/scope-creep/defensibility/dead-weight) added to per-prompt hook
- [Two Knobs, Not One Blanket Brief](feedback-two-knobs-not-one-blanket-brief.md) — 2026-08-18: cut-filler-always vs. never-cut-substance are separate; status questions get real status not mood words; stop auto-agreeing
- [2026-08 Spine Batch (court keys + 42 more)](courtlistener-key-registration-2026-08-17.md) — the whole batch (court keys, 39 verified spec tables incl. IRS charity master + 527s + pensions + PECOS + EPA registry, 3 new families: water permits / credit unions / ICE) staged behind one flag; flipping it freezes incremental until the full rebuild — flip only in the rebuild session; rejected candidates are on the record, don't re-add

- [Census Grid Built 2026-08-12](census-grid-built-2026-08-12.md) — grid shipped 8/12, FILLED 8/17 for ~$2 (8/11 scan reused): all 589 marts measured, 1.23B rows; pension EIN real (zero-pad joins!); ranked trap census (FAERS 76% dup, contracts epoch dates); 2 broken staging views; court IDs real but edge-less
- [Breadth First / Surface Pass](feedback-breadth-first-surface-pass.md) — 2026-08-12 crashout: MANDATORY method — "start from the tippy top," surface pass per thing, park branches in one line, cover everything before deepening anything; the parking lot tally IS the build list; wired into the per-prompt hook because three prior narrow-scope memories never fired
- [Warehouse Measurement Grammar](warehouse-measurement-grammar-2026-08-12.md) — the semantic layer Chris wants over all 558 sources: nouns/events/links/codes, ~50 things × ~30 slots grid, six universal ratios per domain; census BEFORE curated harm cases, plus the 5 rules it ships with

- [Sketch Before Polish](feedback-sketch-before-polish.md) — 2026-08-12 crashout: "visualize this" means rough chart-option sketches + plain commentary, NEVER a designed HTML deliverable; wait for Chris to pick the direction
- [Question Ladder + Graph Truths 2026-08-12](question-ladder-and-graph-truths-2026-08-12.md) — the 1,832-question ladder shipped; CORROBORATED graph tier is name@zip NOT hard-ID (only 14 STEEL key families are SOLID); politics has zero verified cross-family joins; ARCOS/sanctions/ICIJ/courts are graph dark matter
- [Spine Connection Audit 2026-08-11](spine-connection-audit-2026-08-11.md) � placeholder EIN merged CVS+SK Telecom+a TEST row into one entity; spine specs don't follow re-pulls that land under new table names; join precision measured 97-100%
- [Repair Path Gates + Overwrite Trap](repair-path-gates-and-overwrite-trap.md) — 2026-08-11: classifier blocks landing DDL even in reviewed scripts (UPDATEs pass); write_pandas overwrite keeps old schema; dedupe on CAST values not raw
- [Completeness Check Traps](completeness-check-traps.md) — 2026-08-11: VARIANT chunk tables (rows≠records, use ARRAY_SIZE) and wrong publisher totals (FEMA/GLEIF/ransomware) — SHORT/OVER is a hypothesis, not a verdict

- [Warehouse Verification 2026-08-11](warehouse-verification-2026-08-11.md) — first full accuracy audit: 71% verifiably complete, ~50 broken sources ranked (NMDB 2,600x dups, NCUA wrong file, FAA epoch dates); dbt test suite possibly never run

- [Loaders Wrote 'nan' Instead of NULL](loader-writes-nan-sentinel.md) — 2026-08-11: pandas NaN is not None; 4.2M corrupted cells incl. a branch id and coordinates. Use _as_text; repair with scripts/repair_nan_text.py.
- [Silent Long Jobs Are Not Hung](silent-long-jobs-are-not-hung.md) — 2026-08-11: the connection reseed prints one line at the END; hours of silence is normal. Check warehouse query history before killing anything.

- [Stale Commands Are Live Ammo](feedback-stale-commands-are-live-ammo.md) — 2026-08-09: queued demote command buried same-day rebuilds; re-verify handed-off commands against CURRENT state; demote tool now refuses big/fresh runs

- [Spine Full Rebuild 2026-08-08](spine-full-rebuild-2026-08-08.md) — nursing-home NPI was phantom (source has no field); incremental catch-up exposes-but-can't-fix old drift; full rebuild on X-Small = ~4.5h/~$10-15; DROP TABLE always classifier-blocked, hand Chris the one-liner

- [Interaction Contract](interaction-contract.md) — LIVE 2026-08-06: CLAUDE.md §8 + per-prompt hook; chat is the interface, never send Chris to files; 5-sentence caps, bad news first, DONE/BROKE/YOUR MOVE/NEXT close, rewrite STATUS.md every session

- [Spine Rebuild 2026-08-05](spine-rebuild-2026-08-05.md) — ingestion sweep on the map (31.8M entities, COMPANY_NO axis); DISPLAY_SPECS is the spine gate; EPA↔money crosswalk found unwired; 11 orphan tables await DROP

- [Coverage Sweep 2026-08-05](coverage-sweep-2026-08-05.md) — warehouse compute back; 895 blind spot = all portal crawl; NDC/EPA-case/CUSIP new keys verified; HCRIS hospitals-only kills A-4; sorted-cap truncation trap
- [Exhaustive ID Sweep 2026-08-05](exhaustive-id-sweep-2026-08-05.md) — 25-domain/50-agent sweep, 747 candidate keys; MSHA controller/violator bridge + DOL SPONS_DFE_PN verified live+unused; PLAN_NUM is a new 0%-filled trap; whole-domain gaps confirmed (energy/ag/insurance/SSA)

- [The Bench (Plotly workbench)](bench-plotly-workbench.md) — 2026-08-04: bench/ shipped after retiring four forgotten viz tools; six-bucket model, generated knob panel, two-way code, warehouse-wired; catalog is now a snapshot-backed browse drawer; SERVE_MON quota exhausted = warehouse compute dead

- [Library Atlas Rebuild](library-atlas-rebuild.md) — 2026-08-02 portfolio rebuild shipped: compile_library → library_app → export_html, plus the Dash traps hit building it

- [Hunch Engine Direction](hunch-engine-direction.md) — green-lit 2026-08-01: open-ended surprise discovery, NO question taxonomy; pattern-grain publish now exists

- [Playground + Two-Desk State](playground-and-two-desk-state.md) — what's live 2026-08-01: Playground is Chris's lab (packs, no SQL generation), Reading Room is sign-off; COLUMN_CATALOG only covers pack tables; rebuild marts only via build_review wrapper
- [Senate Trades Reality](senate-trades-reality.md) — name-only source (bioguide claim was wrong), coverage ends Dec 2020, journalism-use-only by law

- [Open Brief Means Range](feedback-open-brief-means-range.md) — 2026-08-02 crashout: when Chris says open-ended, bring 2-3 options and let him choose; never build around a metaphor he only riffed on; never edit CLAUDE.md
- [Platform Vision](platform-vision.md) — the confirmed ceiling: hold the public record, wired together, as a solo investigative-journalism platform
- [Connection Lenses](connection-lenses.md) — the KPI/lens families the connected Library produces; "banned but still operating" is the first story to chase
- [Bridge Fuel Reality](bridge-fuel-reality.md) — masked ID columns are the recurring bridge trap (NPPES EIN, FCC ULS EIN): always COUNT(DISTINCT) before trusting a key column
- [Chris Drives Analysis](feedback-chris-drives-analysis.md) — for investigator/BI tools, build infra so Chris investigates himself; don't build an autonomous agent that hands him conclusions
- [Grilling Calibration](feedback-grilling-calibration.md) — on big-picture/vision asks, synthesize and produce the deliverable; don't multi-select every implementation fork
- [Snowflake PAT/Role Reality](snowflake-pat-role-reality.md) — PAT sessions can't USE ROLE and the "read-only" role isn't; enforced read-only needs the RIPPLE_READER-bound PAT
- [Hybrid Learning Preference](user-hybrid-learning-preference.md) — wants plug-and-play speed but visible/editable underlying code (e.g. Plotly) so he learns by using it, not a black box
- [Loader Runtime Traps](loader-runtime-traps.md) — 2026-08-10: background Bash now handles multi-hour loaders (10-min cap gone, Start-Process blocked); checkpoint everything; FDIC API caps offsets at 2M (partition by YEAR); cpsc.gov TLS-blocks curl but python-requests works
- [API Key Blockers](api-key-blockers.md) — RESOLVED 2026-08-22: both keys on file in .env and verified live; never re-ask for signups — the open work is running the LDA backfill (9% loaded) and checking the WHD loader; DOL key goes as a query param, header probes false-403
- [Warehouse Data Traps](warehouse-data-traps.md) — TRY_TO_DATE('YYYYMMDD') epoch trap, round-count loader caps (500k/9k/1M/20M), quote-corrupted casts, success-logged corruption; verified in the 2026-07-27 sweep
- [Proactive Progress Updates](feedback-proactive-progress-updates.md) — use Monitor to stream status during long background jobs; don't go silent until the final notification
- [Verify Agent Research Against Tests](feedback-verify-agent-research-against-tests.md) — a "zero references" grep can miss tests that assert structural properties (id counts, id shapes); always run the real suite before trusting "low risk"
- [Monetization Goal + Paths](monetization-goal-and-paths.md) — Chris wants Ripple to hit $200k/yr to quit his job; 3 lanes scoped (compliance SaaS, due-diligence dossier, indie journalism) with honest risk read on each
- [Avoid Narrow Fixation](feedback-avoid-narrow-fixation.md) — recurring feedback: don't lock onto the first proven/easy example (banned-providers lens, question taxonomies); reason from the whole foundation
- [No Publish Nudging](feedback-no-publish-nudging.md) — 2026-08-06 crashout: never recommend/lean toward publishing, ever, esp. not alongside an open issues list; now written into CLAUDE.md §4 RED lane
- [Workflow Warehouse Restriction Every Phase](feedback-workflow-warehouse-restriction-every-phase.md) — 2026-08-07: a "no warehouse" rule in phase 1 of a Workflow does NOT carry to later phases; restate hard constraints in every phase's prompt
- [Value-Shape Sniffer 2026-08-18](value-shape-sniffer-2026-08-18.md) - 18 confirmed hidden-ID columns (FEC positional-header tables the headline; EPA case facilities; CMS chains); zero hidden EINs; Luhn kill for sequence IDs; spine keyset is the overlap reference
- [Webflow Scene Framework](webflow-scene-framework-2026-08-23.md) — "the flow framework" = 21 composition scenes (dense/quiet rhythm, one sun per page, L/M/S zones), built as a 12-col grid in Webflow + the API traps hit
