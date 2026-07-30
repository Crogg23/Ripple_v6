# Handoff: Ripple remediation from the 2026-07-30 portfolio-readiness audit

**Repo:** c:\Code\Ripple_v6 (git, branch `main`)
**Read this first:** `CLAUDE.md` at repo root — the operating constitution (mission, lanes, escalation rules). Every session must read it before touching anything.

## Why this doc exists

Chris asked for a full sanity check on Ripple from a "ready to show off in a
portfolio" + "ready to query for visuals" perspective. A 4-agent audit ran
live against Snowflake and the repo. Full findings are written up in
**`outputs/PORTFOLIO_READINESS_AUDIT_2026-07-30.md`** — read that file for
the complete evidence and reasoning. This handoff does not repeat it; it's
the punch list of what to actually go fix next.

**Explicitly out of scope for this handoff:** the audit found a
blocker-severity security issue (an ACCOUNTADMIN-scoped PAT being used as the
default working credential, plus a defect that was wrongly auto-closed by an
agent). Chris is the sole operator right now and will handle credential
rotation himself, on his own timeline — **do not touch credentials, PATs, or
that defect record in this remediation pass.** It's documented in the audit
file for when he's ready.

Chris said he's burnt out on this project after days of rebuild/troubleshooting
and explicitly does **not** want data-findings analysis — this remediation
work is pure plumbing/infra, not investigation.

## Current state (as of 2026-07-30, live-verified)

- Warehouse connects fine; landing = 875.5M rows / 1,937 tables; 391 dbt
  marts (up from a stale committed 47).
- All 5 of the documented data traps (LEIE NPI sentinel, OFAC blank type, AIS
  stale snapshot, USASpending grain, Open Payments split) are confirmed
  correctly guarded live — that part does not need rework.
- Uncommitted local changes already sitting in the working tree from the
  audit (see "Task 4" below for what to do with them):
  `honesty/grading.py`, `honesty/report.py`, `honesty/compose.py` (encoding
  bugfix), `honesty/MART_GRADES.md`, `honesty/mart_grades.json` (regenerated),
  plus untracked `investigations/adhoc_2026-07-03/q02_bar.py` /
  `q03_bar.py` (harmless scratch files from a live chart-CLI test — fine to
  delete or ignore) and `.venv/...` pytest install artifacts (untracked,
  ignorable, not the venv's problem to solve).

## Remediation tasks, in priority order

### Task 1 — Rebuild stale marts (`dbt run`)
`lead_queue`, the mart the whole review-gated governance layer depends on, is
94% undercounted live (1,040 rows vs. 17,255 in the underlying reviewable-claims
view) because marts haven't been rebuilt against recent work (ID crosswalk
sweep, cohort-outlier engine, OSHA finding). The project's own custom dbt test
(`assert_lead_queue_reconciles.sql`) already catches this and is failing —
that's the trigger to fix, not a new problem to diagnose.
- Run `dbt run` (or a targeted `dbt run -s lead_queue+` if a full rebuild is
  too slow/costly) from `library-onboarding/ripple_dbt`, profiles-dir `.`.
- Re-run `dbt test -s assert_lead_queue_reconciles` (or the equivalent
  selector) to confirm it now passes.
- Standing policy `no_selectorless_dbt_build` in `build-state.md` says: never
  run a bare selector-less `dbt build` — POLITICS__* marts are Python-built
  and a bare build clobbers them. Respect that.

### Task 2 — Fix typing on TEXT-only marts
Two of five sampled marts are effectively all-VARCHAR, which blocks charting
without manual casts:
- `HEALTH__FED_CMS_NPPES` (9.6M rows): 332 of 333 columns are TEXT, including
  a blank/masked `EIN` column (known trap, not new).
- `POLITICS__FEC_CANDIDATE`: 10 of 11 columns TEXT, including `CYCLE` (an
  election year) stored as a string.
- Treat these two as a sample, not the full list — before fixing, run a
  quick `INFORMATION_SCHEMA.COLUMNS` sweep across all 391 marts (dtype counts
  per table) to find every mart that's >80% TEXT, so this gets fixed once
  instead of mart-by-mart as it's discovered. Cast obvious numeric/date
  columns at the staging or mart layer (whichever matches this project's
  existing typing convention — check how `MARITIME__FED_NOAA_AIS` or
  `JUSTICE__COUNTY_DOUBLE_BURDEN`, both already well-typed, do it).

### Task 3 — Extend dbt test coverage
88% of marts (345 of 391) have zero dbt tests. Coverage is concentrated
entirely in the original ~46-mart core; none of the ~344 marts added by the
recent onboarding wave have any schema tests.
- This is a **judgment call on scope/priority**, not a mechanical task — a
  blanket "add tests to all 344 marts" pass isn't necessarily the right call
  in one sitting. Reasonable default: prioritize marts that feed
  `lead_queue`/detectors or are likely to be queried for visuals (see Task 2's
  sweep) over marts nobody's touching yet. At minimum, add `not_null`/`unique`
  on primary/hard-ID key columns per mart — that's the cheapest test that
  catches the most damage.
- Flag to Chris (one-line, yellow-lane per CLAUDE.md) how much you actually
  covered vs. deferred, and why.

### Task 4 — Commit the honesty engine fix + regenerated grades
The audit already fixed a real bug and regenerated real artifacts; they're
sitting uncommitted:
- `honesty/grading.py`, `honesty/report.py`, `honesty/compose.py`: added
  `encoding='utf-8'` to 4 `read_text`/`write_text` calls — fixes a
  `UnicodeDecodeError` crash on Windows when a model comment contains a
  non-ASCII character (e.g. an em-dash). Verified via the project's own
  `tests/test_honesty.py` (35/35 pass).
- `honesty/MART_GRADES.md` / `mart_grades.json`: regenerated from the current
  manifest. New count: 389 fact / 1 lead / 1 unverified (up from a stale
  committed 46/1/0). The 1 new `unverified` (`ref__dim_state`) is a confirmed
  false positive — a hardcoded `FROM VALUES` reference table that the
  grader's comma-join heuristic misreads as an unparseable join. Don't "fix"
  this by weakening the grader's join taxonomy without Chris's sign-off — the
  honesty README calls that taxonomy "the one documented judgment call, made
  once." Note it as a known false positive (e.g. a comment or a short line in
  `honesty/README.md`'s Limitations section) rather than silently patching
  grading logic.
- **Do NOT re-run Task 1 before regenerating grades again** if you rebuild
  marts — regenerate `MART_GRADES.md`/`mart_grades.json` a second time after
  `dbt run` so the committed grades reflect the post-rebuild manifest, then
  commit once at the end rather than twice.
- Review the diff, then commit (ask Chris first only if anything looks
  surprising beyond what's described here — this is otherwise a green-lane
  mechanical fix per CLAUDE.md).

### Task 5 — Portfolio cleanup pass
Purely cosmetic/organizational, no content rewriting needed. Full rationale
and exact file list is in the audit doc's "Portfolio narrative" section —
short version:
1. `git mv` the ~14 dated root-level docs (`AUDIT_2026-07-14.md`,
   `ROADMAP_2026-07-14.md`, `BETA_DECISIONS_2026-07-20.md`,
   `handoff-to-desktop-7-25.md`, `PROGRESS_LOG.md`, `STRATEGIC_REVIEW.md`,
   `SYSTEMIC_FINDING.md`, `LIBRARY_SNAPSHOT.md`, `build-state.md`, etc.) into
   `outputs/` or a new `archive/` folder — cuts root `.md` count from 18 to
   ~4.
2. `git rm` `eq.html` (52KB), `publog.html` (128KB), and the three
   `ckan_sweep*.log` files at root — unexplained scrape/log debris. Untrack
   `.DS_Store` and add it to `.gitignore`.
3. Add a short "Read next" block near the top of `README.md` linking:
   `docs/ripple_pitch_deck.md` (best portfolio artifact — lead with this),
   `docs/RIPPLE_FOR_EVERYONE.md` (plain-English version), `honesty/README.md`
   (the provenance/trust engine — most distinctive piece of architecture),
   `PROJECT_SHAPE.md` (outside-reviewer's honest read).
4. Point to `OVERVIEW.md` explicitly as the architecture tour in README — it
   already does the job, it's just undiscoverable today.

## Suggested skills for the next session

- **`simplify`** — after Tasks 1-2 land real SQL/dbt changes, run this on the
  diff for a reuse/efficiency pass before considering the work done. (Not
  `/code-review` — that's for bug-hunting, not fit here since this is
  infra/plumbing work, not new logic with edge cases.)
- **`run`** — if Chris wants to actually see the fixed chart pipeline in
  action (e.g. confirming `python -m ripple chart` renders cleanly against a
  now-well-typed mart from Task 2), use this to launch and verify rather than
  just trusting the dbt run succeeded.
- Do **not** invoke `security-review` in this pass — the one security finding
  is explicitly deferred to Chris, and this remediation shouldn't go looking
  for more in the same session (scope creep away from what he asked for).

## Same session or fresh session?

**Recommend a fresh session.** Reasoning:
- The audit that produced this handoff ran a 4-agent Workflow that alone
  burned ~410K tokens; the current session is already long. Starting fresh
  avoids dragging a bloated context window into what is now execution work
  (dbt runs, SQL edits, git operations) rather than investigation.
- Nothing about the remediation needs the raw conversation history — this
  handoff doc plus `outputs/PORTFOLIO_READINESS_AUDIT_2026-07-30.md` are a
  complete, self-contained brief. A fresh session reading both starts with
  everything it needs and nothing it doesn't.
- Chris said he's burnt out. A clean new session lets him hand this off
  (today, tomorrow, whenever) without needing to re-load or explain a long
  prior conversation.

If continuing in the same session is preferred anyway (e.g. Chris wants to
keep talking to the same thread), that's fine too — nothing here requires a
fresh session, it's just the lower-friction default.
