# Ripple — Backfill Runbook (2026-07-23)

Companion to `DATA_AUDIT_AND_BACKFILL_PLAN_2026-07-23.md`. This is the
step-by-step for actually pouring the full data. Chris runs these locally (the
pour needs internet, which the in-IDE agent connection lacks).

Decision locked: pour as **`LIBRARY_PAT` / ACCOUNTADMIN** (the write token you
already own, active to 2026-09-20).

---

## Step 0 — `.env` changes (one time)

In `library-onboarding/.env` set:
```
SNOWFLAKE_PAT=<the LIBRARY_PAT secret>
SNOWFLAKE_ROLE=ACCOUNTADMIN
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
```
- **The PAT secret:** Snowflake only shows a PAT's secret at mint time — I can't
  read it back for you. If you saved `LIBRARY_PAT` when you created it, paste it.
  If not, rotate it in Snowsight (Settings → Authentication → Programmatic access
  tokens → `LIBRARY_PAT` → rotate) and paste the new secret. One command.
- `DBT_WH` in the current file is dead — that's why any script errored with "no
  active warehouse." `COMPUTE_WH` is live (X-Small, ~1 cr/hr, 60s auto-suspend).
- Revert `SNOWFLAKE_ROLE`/`SNOWFLAKE_PAT` back to the reader token after the
  sprint so day-to-day scripts run least-privilege again.

## Step 1 — raise the ceiling for the sprint
```
python scripts/budget_sprint.py        # raise RIPPLE_BUDGET for the one-time pour
# ... run the backfill ...
python scripts/budget_sprint.py --restore   # (or however it reverts) back to steady-state
```

## Step 2 — the reliable re-pour pattern (attended)
For an `onboard.py` source, run **without `--yes`**:
```
python onboard.py --name <SOURCE> --include-landed --skip-dbt
```
At the **SCRIPT** checkpoint, `edit` with a full-pull steer, then `go`:
> download the COMPLETE dataset — paginate through every page / fetch the full
> bulk file, not a sample slice. Remove any row or page cap.

Watch the LOAD line: row count should jump to the real universe and density > 0.

---

## Step 2b — SERVER-SIDE bulk path (GB-scale files that stall through the laptop)

For files too big to pull through this machine (CFPB 1.4 GB stalled at 0 bytes),
**Snowflake fetches them directly** on its own compute — no laptop hop. Built
2026-07-23; DDL in `infra/ddl/08_bulk_ingest.sql`, loader in
`scripts/server_side_load.py`, specs in `scripts/server_side_specs.py`.

Objects (all in `LIBRARY_RAW.LANDING`, ACCOUNTADMIN-owned, all DROP-able):
- `RIPPLE_BULK_EGRESS` network rule (egress ONLY to listed gov hosts) +
  `RIPPLE_BULK_ACCESS` external access integration + `BULK_STAGE` internal stage.
- `RIPPLE_FETCH_TO_STAGE(url, path)` — streams a URL into the stage (temp file +
  PUT; bounded memory). `RIPPLE_UNZIP_MEMBER_TO_STAGE(zip, member, out.gz)` —
  reads a staged .zip via SnowflakeFile, recompresses the chosen member to .gz
  (COPY can't read .zip).

Run:
```
python scripts/server_side_load.py --list
python scripts/server_side_load.py --spec FED_CFPB_COMPLAINTS --run
# resume a load without re-pulling GBs (file already on BULK_STAGE):
python scripts/server_side_load.py --spec <ID> --run --reuse-staged
```
Full ledger reuse: density gate + `INGEST_RUNS` log + `SOURCE_REGISTRY` upsert +
atomic staging swap — a server-side load is indistinguishable downstream.

**Cost discipline (Phase 4) — possession means storage is the recurring bill:**
- `--refresh` re-fetches but **skips the COPY/re-store when content is unchanged**
  (fingerprints the raw fetched file; SHA match = no re-store). Cheap recurring refresh.
- `LIBRARY_RAW.LANDING` Time Travel retention is **1 day** (minimal storage overhead);
  all-TEXT raw compresses well in Snowflake.
- `RIPPLE_BUDGET` (30 cr/mo, suspend at 90%) stays the hard cap; raise only for sprints.
- If raw storage ever grows material, add a Snowflake **storage lifecycle policy** to
  archive/expire cold landing tables (lever noted, not yet needed).

**Gotchas proven the hard way (bake into any new spec):**
- **Host scope + no wildcards.** Egress rule lists exact hosts; a cross-host 302
  is blocked (FEC → S3 GovCloud died on this). Only DIRECT-served URLs work today.
- **INFER_SCHEMA and MATCH_BY_COLUMN_NAME both choke** on ragged gov CSVs (a lone
  short row → "header defined N cols, data M"). The loader instead parses the
  header line in Python and does a **positional** COPY with `SKIP_HEADER=1`,
  `MULTI_LINE=TRUE`, `ERROR_ON_COLUMN_COUNT_MISMATCH=FALSE` (raw-mirror tolerance).
- **X-Small handled 1.4 GB** fetch (~65s) + unzip (~110s) fine — no disk blowup.

Status: **FED_CFPB_COMPLAINTS = DONE (17,179,788 rows, verified).**
Remaining GB targets to add as specs:
- **intl_gleif** -- DONE (3,382,301 rows) via a resolver hop (metadata API -> rotating
  .csv.zip link). Pattern is reusable for any source with a metadata-indexed download.
- **Open Payments / Part D / ECHO refresh** -- plain/zipped CSVs; confirm each
  current bulk URL, add a spec (kind + delimiter + member_pattern), run.

### Routing policy (which tool for a new source) -- Phase 3

Cheapest-capable tool wins. In order:
1. **Public file at a direct URL (CSV/ZIP)** -> `server_side_load.py` (Snowflake fetches
   it; no laptop, no LLM). This is the DEFAULT for public bulk data.
2. **Redirecting/metadata-indexed download** (GLEIF-style) -> same loader with a `resolver`.
3. **Public API needing a free key** (data.gov `api_key`) -> same loader with `auth`
   (keyed proc `RIPPLE_FETCH_TO_STAGE_KEYED` + the `RIPPLE_API_KEY` secret).
4. **SaaS app / database / true CDC** -> Openflow (heavier; only if a real SaaS source needs it).
5. **Scrape / JS-rendered site / bespoke one-off** -> `onboard.py` (the AI agent). LAST
   resort -- it costs ~3-4 Claude calls per source. Do NOT use it for anything tiers 1-3 cover.

Rule of thumb: if a source is a file or a keyed API, it should NOT go through the AI agent.

---

## Tier 1 — do these first (feed findings + cross-domain bridges)

| Source | How | "Full" = | Landed→target |
|---|---|---|---|
| **fed_sam_exclusions** | run the existing script, not onboard: `python scripts/sam_exclusions_load.py` (remove the page cap) | all exclusion pages | 1,000 → ~100k+ |
| **intl_gleif** | attended re-pour; steer = stream the whole concatenated golden-copy XML | full LEI2 concatenated file | 20,000 → ~2.9M |
| **fed_irs_990** | HEAVY / bespoke — the e-file corpus is per-year ZIPs of XML. Steer must point at the yearly index and iterate all ZIPs, not one sample file. Consider a dedicated script. | all e-file year ZIPs | 200 → millions |
| **fed_clinicaltrials** | attended; steer = use the AACT bulk / full API pagination | all trials | 500 → ~500k |
| **fed_us_sec_edgar** | attended; steer = full submissions set (all CIKs), not a page | ~900k filers | 48,990 → ~900k |

Note: `FED_IRS_BMF` (1.97M) and `FED_IRS_REVOCATION` (1.2M) are **already full** —
the org-existence + revocation universe is covered. The 990 e-file corpus adds
financials + Schedule I/R entity-to-entity money links (the dark-money graph).

## Tier 2 — strong accountability sources
| Source | How | Landed→target |
|---|---|---|
| fed_cfpb_complaints | **DONE** — server-side (Step 2b), 17.18M rows landed 2026-07-23 | 250 → 17,179,788 |
| fed_fdic_bank_data | attended, paginate full | 10,000 → ~75k+ |
| fed_nsf_awards | attended; use the "Download Awards" bulk CSV, not the scrape | 125 → ~500k |
| fed_usaspending_subawards | attended; full award_data_archive (USAspending contracts already full at 6.3M) | 5,000 → millions |
| fed_epa_envirofacts | LOW — `FED_EPA_ECHO` (3.2M) already covers most EPA; confirm overlap before spending | 5,000 → ? |

## Tier 3 — fix the broken loaders (ATTENDED, code repair — not a volume problem)
| Source | Problem | Fix |
|---|---|---|
| fed_nih_reporter | 5,000 rows all blank (parser broke) | repair codegen so the JSON envelope unnests to real columns, then re-pour |
| fed_hhs_taggs | hard SQL failure (invalid identifier) | fix the generated load SQL; portal-only, may need a scrape/export path |
| fed_cdc_wonder / fed_fbi_cde / fed_cms_hpt_mrf | 1-row loads (API envelope not unnested) | repair codegen per source; lower priority |

## Drop / deprioritize (don't spend on these)
- **fed_fincen_boi** — registry near-empty for the useful part: US domestic
  companies were **exempted** (Mar 2025), so there's little to pour. Skip.
- **fed_dea_arcos** — retail summaries are *aggregated*, no entity IDs → weak
  join value. Skip unless a specific opioid story needs it.
- **fed_grants_gov** — opportunity *listings* (solicitations), not awards. Low value.
- **Category D redundant stubs** (`fed_fara`, `fed_sec_edgar`, `fed_fec_api`,
  `fed_us_usaspending_api`, `fed_cms_main`) — a full sibling already exists; drop
  the stub, don't re-pour.

---

## After the pour
1. Re-run the audit query (row counts) to confirm the jumps + density > 0.
2. Build dbt models on the now-full tables (the part `--skip-dbt` deferred).
3. Ping the agent to re-check whether a cross-domain finding now fires (esp. once
   the FAC / Transparency-in-Coverage keystones land — see plan §5).
4. Revert `.env` to the reader token.
