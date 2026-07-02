# POUR GO-CHECKLIST — the last mile before "go" (2026-07-01)

The code side is fixed + tested (104 green). What's left is yours: secrets, deps, budget.
Thanks to the code fixes, the model + auto-approve are now handled automatically, so your
hard prerequisites shrank to **4 things**.

## MUST DO (nothing pours without these)

- [ ] **Anthropic key.** Put a real key in `library-onboarding/.env` line 10:
      `ANTHROPIC_API_KEY=sk-ant-...`  (must be in the file — a shell export is clobbered
      by `.env`). This is the ONE true secret. Verify:
      `cd library-onboarding && python -c "from config import settings; settings.require('anthropic_api_key'); print('key OK, model:', settings.anthropic_model)"`
- [ ] **Install deps.** `pip install -r library-onboarding/requirements.txt`
      (tenacity / beautifulsoup4 / lxml are missing). Verify: `python -c "import tenacity, bs4, lxml"`
- [ ] **Raise the budget** (you're ACCOUNTADMIN; I'm blocked from `ALTER RESOURCE MONITOR`).
      Cost is no object for a one-time pour, so give big headroom:
      `ALTER RESOURCE MONITOR RIPPLE_BUDGET SET CREDIT_QUOTA = 300;`
      (optional: `ALTER RESOURCE MONITOR RIPPLE_BUDGET SET NOTIFY_USERS = (CROGG23);` for alerts)
- [ ] **Data-source API keys** — only for the key-gated sources you actually want to pour.
      Add to `.env` as needed: `FRED_API_KEY`, `FEC_API_KEY`, `EIA_API_KEY`, `CENSUS_API_KEY`,
      `BLS_API_KEY`, `PROPUBLICA_API_KEY` (SAM_API_KEY is already set). Keyless sources pour without these.

## NICE TO HAVE

- [ ] **Model choice** — blank now auto-falls-back to `claude-sonnet-4-6`. For best recon/codegen
      on a cost-is-no-object pour, set `.env` line 13 `ANTHROPIC_MODEL=claude-opus-4-8`.
- [ ] **PAT lifetime** — current token good to ~2026-09-20. Only rotate if the pour runs that long.

## THEN POUR (the canonical unattended command)

```bash
cd library-onboarding
# 1. dry smoke (no spend, no key needed) — confirms the flow walks + continues past failures:
python -m pytest ../tests/test_onboard_smoke.py -q
# 2. one real source (confirms key/model/deps/warehouse on a single load):
python onboard.py --url <one-bounded-source-url> --yes
# 3. the pour — unattended, resumable, skip-and-continue on failures:
python onboard.py --batch --yes > pour.log 2>&1
# 4. re-run to retry failures (completed sources are skipped automatically):
python onboard.py --batch --yes
```

## AFTER THE POUR — refresh the reading room (materialized snapshots go stale)

```bash
python scripts/thelibrary_inventory.py && python scripts/thelibrary_build.py --apply
```
(`CATALOG` self-updates; `THE_LIBRARY` + `FRIENDLY_LAYER` are snapshots that need this.)
