# Portfolio-Polish Sweep — 2026-07-30 (fresh pass)

37 candidates found across 8 dimensions (connect/ spine, security, docs-vs-reality, repo hygiene, dbt marts, UX polish, test coverage, scripts/infra). 34 confirmed by an independent adversarial-verify pass. Ranked by severity.

## BLOCKER — fix before anyone else looks at this repo

1. **`.venv/` is committed to git** — 11,834 files, ~308MB, and `.gitignore` has zero rule for it (only `.dbt-venv/` is covered). Every clone pulls down a full Python interpreter + site-packages instead of a 2-line `pip install`. The `.git` directory itself is 186MB, driven mostly by this — removing `.venv/` from the working tree won't shrink history; that needs `git filter-repo`/BFG.
2. **`ripple/pour.py`'s `classify()` has a broken backwards-compat contract** — its own docstring says it accepts the old `spec_ids` (set) or new `specs` (dict) positionally, but passing a set crashes with `AttributeError: 'set' object has no attribute 'get'`. 4 of the module's 16 tests fail on HEAD right now (`tests/test_ripple_pour.py`).

## HIGH

3. **`connect/dossier.py:73-88`** — name search does `LIKE '%TOKEN%'` per query word with no token-boundary anchoring, so "jon smith" can silently substring-match "JONES SMITHFIELD MEDICAL GROUP" and auto-return it as the single match with **no disambiguation prompt** — a wrong-entity result handed back silently, the exact failure class this platform exists to prevent.
4. **`README.md:50-52`** — claims dbt runs "86 dbt models"; actual count is 1,378 (16x off).
5. **`politics/README.md`** — 9 real loader files (judicial/FJC, SCOTUS, individual FEC donations, election outcomes) exist in `politics/loaders/` with zero mention anywhere in the README's file listing or run-order.
6. **`politics/SESSION_BRIEF_2026-06-29.md`** — tells the reader to build the FEC itcont loader next; it already exists (`build_indiv_donations.py`, `smoke_itcont.py`), plus a whole judicial/SCOTUS domain and a `who_won` domain built after this brief and never mentioned.
7. **`outputs/` — 133 tracked files, ~87-91MB** — including a 55MB `portal_index.json` blob (same class of file `.gitignore` explicitly excludes for `connect_graph.json` but doesn't cover here), a duplicated 4.8MB `mermaid.min.js`, 10 near-duplicate `_rollback_*.sql` snapshots, and a pile of dated HANDOFF/AUDIT markdown files with no index.
8. **Brand collision** — `serve/app.py` and `reading_room/app.py` are two structurally different tools that both title themselves "Ripple — The Reading Room." (An internal roadmap doc already proposed renaming `serve/app.py` to "the Atlas" — never executed.)
9. **`tests/test_leads_wave2.py::test_compile_sql_byte_stable_for_existing_specs`** — currently failing; the golden SHA256 churn-detector for `banned_but_operating`'s compiled SQL doesn't match. (Verification found these goldens were likely wrong from the moment they were committed, not recently broken — but it's failing right now either way.)
10. **`connect/incremental.py`** — 980 lines, the single largest module in `connect/`, doing the most complex logic (incremental watermarks/windowing) in the entity-resolution layer, with **zero test file**.
11. **All of `serve/`** — 1,236 lines across 5 files, zero tests. `serve_graph.py` currently has uncommitted local changes with nothing to catch a regression before commit.
12. **`viz/sqlrun.py`** — 335 lines, the platform's own documented "ONE chokepoint between any surface and Snowflake," has no test file, while its sibling `viz/` modules (card, guard, plugs, safety) each have one. Also currently uncommitted.
13. **`scripts/task_wrapper.ps1:33`** — hardcodes `C:\Users\wroge\...\Python312\python.exe` (per-user, per-machine) instead of the repo's own `.venv`, unlike `campaign_watchdog.ps1` which does it correctly. Every scheduled task silently no-ops on any other machine/user.

## MEDIUM

14. **`connect/leads_specs.py:39-47`** — `_FACILITY_NAME_TABLES` is a hardcoded 7-table list that's missed newer CCN-keyed facility tables (`FED_NURSINGHOME411`, `FED_CMS_HCRIS`, `FED_CMS_NURSING_HOME`) added since — a `banned_but_operating` lead can fire with a blank facility name and no error, silently weakening the human-reviewable evidence.
15. **`logs/`** — 46 tracked `.log` files (loader run/error logs) with zero `.gitignore` rule, inconsistent with `outputs/_*.log` which is explicitly ignored.
16. **`.gitignore` is internally inconsistent** — narrow rules for some generated files in `outputs/`, nothing for `.venv/`, `logs/`, or several other large generated blobs actually tracked (`graph.gexf`, `library_map*.html`, `portal_index.json`).
17. Four raw-exception leaks in the UI layer instead of friendly messages: `serve/app.py:126` (connection errors in the sidebar), `:335` (source sampling), `:349` (graph load), `reading_room/app.py:58` (reader query failure), `:283-286` (decision write failure).
18. **`serve/serve_workbench.py:52-57`** — only catches `sqlrun.GuardError`; any other exception (e.g. a malformed-SQL compile error) crashes the Streamlit app with a full traceback shown to the user.
19. **`connect/db.py`** — zero tests on credential loading, warehouse lane-pinning, and `fqn()` table-qualification — exactly the "errors matter" write/credential path CLAUDE.md flags, in a codebase that's already been bitten twice by masked-value bugs.
20. **`infra/launchd/*` + `HEARTBEAT_README.md`** — describes a macOS-only runbook (hardcoded `/Users/chrisr./...` paths) with nothing marking it superseded by the working `scripts/register_windows_tasks.ps1`.
21. **`scripts/acquire_recipes.json` vs `HEARTBEAT_README.md`** — README says "the seed enables exactly one verified-safe loader (fed_cisa_kev)"; actually **4** recipes are `enabled:true` (adds SEC EDGAR discovery, EPA ECHO — up to 700MB ZIPs — and DOL enforcement), a real drift between documented and actual auto-run opt-in surface.

## LOW

22. **`connect/leads.py:221-224`** — person-matching only requires surname equality when a job spec sets `require_surname=True`; a spec that omits it joins purely on the hard ID with no name-based sanity filter at all.
23. **`library-onboarding/snow.py:118`** — `ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = {secs}` via raw f-string; currently neutralized by an `int()` cast one line above, but a latent injection pattern if that cast is ever removed.
24. **`stg_fed_slavevoyages_transatlantic__records.sql`** — same generation shape (huge hand-listed uppercase column list, zero column tests) as the intra-American model that was found 100% broken this session. No re-land script exists for it yet, so it likely hasn't drifted — but nothing guards against it if the table is ever re-landed.
25. Four small UX-discoverability gaps in `serve/app.py`: no legend explaining CCN/UEI/CIK/IMO abbreviations (`:133-145`), "Facility Affiliations" section is invisible for non-NPI entities with no hint it exists (`:279-288`), disabled decision buttons in Reading Room give no local explanation of why (`reading_room/app.py:228-230`), and no loading spinner on the connection-graph page (`:341-355`).
26. **`register_windows_tasks.ps1`, `task_wrapper.ps1`, `task_nag.ps1`** all hardcode `C:\Code\Ripple_v6` instead of deriving from `$PSScriptRoot` — a clone to any other path silently breaks task registration.
