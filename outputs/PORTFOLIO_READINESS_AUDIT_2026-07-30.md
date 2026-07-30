# Portfolio Readiness Audit — 2026-07-30

Live, multi-agent audit of (1) whether the repo tells a clean story for a
portfolio/interview, and (2) whether the warehouse is solid enough to query
straight into visuals. Explicitly NOT a review of what the data says —
plumbing and presentation only. All checks below were run live against
Snowflake and the current filesystem, not against stale docs.

---

## 1. Security — the one thing that actually needs Chris

**Blocker, mis-closed.** `build-state.md`'s only blocker-severity defect —
"leaked/unrestricted ACCOUNTADMIN PATs still ACTIVE" — is marked `STATUS=closed`,
`CLOSED_BY=cortex_code` in `LIBRARY_META.BUILD.DEFECTS`. That's an agent
identity, not a human — a direct violation of this repo's own standing policy
`agent_never_closes_defects` ("only a human sets STATUS/CLOSED_BY on a defect").

It shouldn't have been closed. Live `SHOW USER PROGRAMMATIC ACCESS TOKENS`
shows `LIBRARY_PAT` — role-restricted to `ACCOUNTADMIN`, status `ACTIVE`,
expires 2026-10-21 — and it's the only ACCOUNTADMIN-restricted token on the
account. This session's own connection (via `library-onboarding/.env`'s
`SNOWFLAKE_PAT`) authenticated as `CURRENT_ROLE()=ACCOUNTADMIN`, meaning
`LIBRARY_PAT` is, with high confidence, the actual default credential every
build/load script in this repo uses today.

The defect's closing notes rationalize this as "the working loader token, not
the leaked one" — but the original defect text says "any one of these is
`DROP DATABASE` from anyone's laptop," which is still true of `LIBRARY_PAT`.
Its original justification (no scoped write lane existed) is also now moot —
`RIPPLE_TRANSFORM_RW` and `RIPPLE_REVIEW_WRITER` PATs exist live today.

**Action for Chris:** rotate `.env` onto a scoped write PAT and revoke
`LIBRARY_PAT`, or explicitly re-open/re-scope the defect yourself. Don't leave
it silently "closed."

Also worth knowing: `scripts/verify_defects.py` only re-checks defects with
`STATUS='open'` — it never re-audits something already (wrongly) closed. A bad
closure is currently invisible to the repo's own tooling.

---

## 2. Database reliability — live state as of 2026-07-30

**Live numbers** (`LIBRARY_META.BUILD.V_BUILD_STATE` / `...REGISTRY.V_STATE`,
queried fresh, not from the 3-day-old `build-state.md` printout):
defects_open=13 (10 still_broken, 2 clear-not-yet-closed, 1 needs_human) ·
defects_blocker=0 (only because of the mis-closure above — really 1) ·
landing.rows=875,575,558 across 1,937 tables · connect.entities=22,623,285 ·
connect.edges=610 · marts.stale_vs_landing=1.

**Known data traps — all 5 checked live, all 5 handled correctly.** This is
the good news: every trap named in `CLAUDE.md` / the standing policy log was
spot-checked directly against the query-facing marts (not landing), and every
one is correctly guarded, with zero sentinel leakage:

| Trap | Where checked | Result |
|---|---|---|
| LEIE NPI sentinel `'0000000000'` + epoch-date | `HEALTH__FED_HHS_OIG_LEIE` (83,369 rows) | 0 leaks; dates explicitly parsed, 0 rows at 1970 epoch |
| OFAC `SDN_TYPE` sentinel `'-0- '` | `JUSTICE__FED_OFAC_SDN` (19,115 rows) | 0 leaks; correctly NULLed |
| AIS stale 8-day snapshot | `MARITIME__FED_NOAA_AIS` + `REVIEW.LEAD_QUEUE` | Caveat present on all 16/16 live vessel leads |
| USASpending transaction-grain | `lead_queue` debarred_but_funded detector | Correctly sums transaction column, not cumulative |
| Open Payments 3-way split | `INT_OPEN_PAYMENTS_ALL_YEARS` (43.3M rows) | Row count exactly reconciles to sum of 3 source tables |

**But marts are stale relative to current data.** `lead_queue` — the one
mart your whole review-gated governance layer hangs off — has 1,040 rows
live, while the underlying reviewable-claims view it should reconcile against
has 17,255. That's a ~94% undercount. `dbt run` hasn't rebuilt marts against
the warehouse recently enough to catch up with the last few days of work (ID
crosswalk sweep, cohort-outlier engine, OSHA finding). The project's own
custom test (`assert_lead_queue_reconciles.sql`) correctly fails on this right
now — the safety net works, it's just telling you something's overdue.

**Test coverage collapsed as the platform grew.** 88% of marts (345 of 391)
have zero dbt tests. Coverage is concentrated entirely in the original
~46-mart core; none of the ~344 marts added by the 35-new-source buildout
have any schema tests. Not broken, but unguarded.

**Honesty Engine (provenance grader) had a crash bug, now fixed.** `python -m
honesty` crashed on Windows with a `UnicodeDecodeError` (cp1252 default
encoding choking on a UTF-8 em-dash in a new model comment). Fixed with a
6-line change (`encoding='utf-8'` added to 4 read/write calls in
`honesty/grading.py`, `report.py`, `compose.py`) — this is a mechanical,
obviously-correct fix (green-lane), so it was applied rather than just
reported. Verified via the project's own unit suite: 35/35 pass after the fix.

Regenerated `honesty/MART_GRADES.md` / `mart_grades.json` fresh (the
committed versions were 10 days stale — 47 marts vs the real 391). Fresh
grade: **389 fact, 1 lead, 1 unverified** (up from 46/1/0). The 1 new
`unverified` — `ref__dim_state` — is a false positive: a hardcoded 55-row
`FROM VALUES (...)` reference table that the grader's comma-join heuristic
misreads as an unparseable join. No real mart got silently demoted. **These
regenerated files are sitting as uncommitted local changes** — review and
commit when ready.

---

## 3. Query-for-visualization readiness

**Connects and queries cleanly.** Live connection works; 5 marts sampled
across health/politics/justice/economics/maritime all returned real,
non-trivial row counts with zero errors (9.6M, 17.9K, 3K, 10.4K, 58.1M rows
respectively).

**Typing is inconsistent — some marts need manual casts.** 2 of the 5 sampled
marts are effectively all-VARCHAR:
- `HEALTH__FED_CMS_NPPES` (9.6M rows): 332 of 333 columns are TEXT. Its `EIN`
  column samples blank — this is the same masked-EIN trap already logged in
  memory from a prior session.
- `POLITICS__FEC_CANDIDATE`: 10 of 11 columns TEXT, including `CYCLE`
  (election year) stored as the string `'2024'`.

Others are genuinely chart-ready as-is: `JUSTICE__COUNTY_DOUBLE_BURDEN` and
`MARITIME__FED_NOAA_AIS` have real NUMBER/FLOAT/DATE/BOOLEAN/GEOGRAPHY typing.
This is a per-mart problem, not a platform-wide one — check a mart's typing
before building a chart off it.

**A working, offline chart pipeline exists and was proven live.** `.venv`'s
`python -m ripple chart "<sql>"` ran a real query, picked a chart type, and
rendered a fully offline HTML file (bundled `plotly.min.js`, no CDN call) —
confirmed working end to end today. The separate `outputs/leads_overlay.html`
is confirmed broken as already logged (CDN Plotly dependency + stale baked-in
numbers) — don't use that one.

**No enforced read-only serving lane yet.** `SNOWFLAKE_SERVE_PAT` is blank in
`.env`; every query today (this audit included) ran as `ACCOUNTADMIN` via the
dev PAT, not the scoped `RIPPLE_READER` lane the docs describe. Fine for
solo use, not yet safe to hand a query tool to anyone else.

---

## 4. Portfolio narrative

**A stranger could follow it — the material exists and is good.** Best single
document: `docs/ripple_pitch_deck.md` — real numbers, real SQL, honest about
what's unproven, closes with an explicit hiring-manager translation.
`honesty/README.md` (the fact/lead/unverified provenance grader with a hard
refusal to blend fact-grade and lead-grade numbers) is a genuinely distinctive
piece of architecture worth leading a technical walkthrough with.
`connect/HOWTO.md` is well-scoped and honest about its own limits.

**Problem: none of it is linked from the front door.** `README.md` never
mentions `ripple_pitch_deck.md`, `RIPPLE_FOR_EVERYONE.md`, `honesty/README.md`,
`OVERVIEW.md`, or `PROJECT_SHAPE.md` by name. A first-time visitor has no way
to find the good stuff.

**Root is cluttered with dated internal docs and scrape debris** (confirmed
via `git ls-files`, so all of this is visible on GitHub): 18 tracked root-level
`.md` files, most of them dated working docs (`AUDIT_2026-07-14.md`,
`ROADMAP_2026-07-14.md`, `BETA_DECISIONS_2026-07-20.md`,
`handoff-to-desktop-7-25.md`, etc.) sitting at the same level as `README.md`.
Plus two unexplained raw HTML scrape dumps (`eq.html` 52KB, `publog.html`
128KB), three run-log files (`ckan_sweep*.log`, up to 120KB), and a tracked
`.DS_Store`. None of this is a real problem — it's a 30-minute `git mv` /
`git rm` pass, not a rewrite:

1. Move the ~14 dated docs into `outputs/` or a new `archive/` folder.
2. `git rm` `eq.html`, `publog.html`, the 3 log files; untrack `.DS_Store`.
3. Add a "Read next" block to `README.md` linking the 4 strongest docs.
4. Point to `OVERVIEW.md` explicitly as the architecture tour — it's already
   good, it's just undiscoverable.

---

## Bottom line

- **Portfolio story:** the writing and architecture are already there and are
  genuinely good. What's missing is discoverability and root-level tidiness —
  cheap, mechanical fixes, no rewriting.
- **Query-for-visuals:** the pipe works and your known data traps are all
  correctly guarded — but marts need a `dbt run` to catch up with recent work
  (`lead_queue` is 94% stale), a couple of specific marts need manual casts
  before charting, and the one real blocker (the ACCOUNTADMIN PAT defect
  mis-closure) needs your decision, not another audit.
