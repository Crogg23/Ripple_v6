---
name: api-key-blockers
description: "RESOLVED 2026-08-22: DOL_API_KEY and LDA_API_KEY are both in library-onboarding/.env and verified live — the 2-min-signup blocker is gone; what remains is RUNNING the backfills (Senate LDA at 9% loaded; WHD loader status unchecked)"
metadata: 
  node_type: memory
  type: project
  originSessionId: d10c26ca-89ea-4453-a057-a3762df38910
  modified: 2026-08-22T23:59:43.465Z
---

**RESOLVED (verified live 2026-08-22).** Both keys sit in
`library-onboarding/.env` and both authenticate:
- `LDA_API_KEY` — tested 200 against lda.senate.gov/api/v1/filings/ with
  `Authorization: Token <key>`. (Chris minted a duplicate token in chat the same
  night before the on-file key was checked — the on-file key was kept; the
  duplicate was never filed.)
- `DOL_API_KEY` — valid; a test returned 429 (quota), not 401/403, because the
  OSHA inspections API pull (scripts/osha_inspections_api_load.py, checkpointed)
  was actively consuming the quota. DOL passes the key as a QUERY PARAM
  `X-API-KEY={key}` on apiprod.dol.gov/v4 URLs — a header-style probe 403s and
  looks like a dead key when it isn't.

**Why:** the old memory kept generating a phantom "Chris must sign up" task —
it fired 2026-08-22 and sent Chris to register a token that was already on file.
Keys were evidently added around the 2026-08-21/22 OSHA loader build.

**How to apply:** never re-ask for these signups. The real open work is the
backfills: Senate LDA filings still ~9% of publisher volume (needs its
checkpointed crawl run: page_size 250 with the key), and WHD enforcement loader
status should be checked before assuming it ran. Mind the long DOL quota windows
(sustained 429s for 7+ min observed; the loader backs off up to ~4h). See
[[loader-runtime-traps]], [[quick-wins-fix-session-2026-08-22]].
