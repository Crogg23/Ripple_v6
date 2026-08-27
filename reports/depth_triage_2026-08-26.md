# Depth triage — 2026-08-26 (live-verified)

Chris asked: "get my depth squared away." First pass = measure the real gap,
not the labeled gap. Every number below was checked live tonight; registry
notes that turned out stale were corrected at the base table
(`LIBRARY_META.REGISTRY.MART_SAMPLE_NOTES`).

## Headline

The "1,567 shallow sources" figure is a portal artifact. Split live from the
registry:

| bucket | sources | landed rows |
|---|---|---|
| scraped city/county portals (`portal_*`) | **1,563** | 3.49M |
| real publishers | **4** | 9,500 |

The portal 1,563 belong to the SAME open scope ruling as the entity-graph
portal question (STATUS item). They are not a backfill campaign until/unless
Chris rules portals in scope. **The real depth problem is ~25 sources.**

## The two biggest labeled gaps were ALREADY CLOSED — notes were stale

- `FED_FEMA_IA_HOUSING_REGISTRATIONS`: labeled "3.08M of 25.9M (~12%)".
  Live: **26,250,920 rows, 26,250,920 distinct IDs, zero dupes** across 7
  checkpointed append runs. COMPLETE. Note corrected.
- `UK_COMPANIES_HOUSE_PSC`: labeled "7.0M of ~10M, truncated". Live:
  **15,804,612 rows** (7.0M manual + 8.8M resume runs), 15,518,623 distinct
  on a wide natural key → **285,989 (1.8%) apparent overlap at the resume
  seam**. NEAR-COMPLETE. Remaining work: verify distinct on the PSC self-link
  key, confirm the current publisher chunk-manifest total, dedupe the seam.
  Note corrected.

Pattern for the registry: "sample" notes are written once and never re-checked
against later loader runs. Same repetition-isn't-verification failure as the
audit labels.

## Real remaining gaps, ranked (non-portal)

**Tier 1 — graph fuel, STEEL keys, real size:**
1. `fed_usaspending_subawards` — 5,000-row API slice of a multi-million-row
   dataset. STEEL key. Bulk archive exists at USAspending; needs a loader
   (bridge-fuel path). Est: hours, ~$1-2.
2. `fed_cfpb_hmda` / `fed_cfpb_hmda_lar` — slices (28k / 17k). BUT
   `FED_CFPB_HMDA_HISTORIC` already holds **19.1M rows** — check what
   years/products it covers before loading anything; the gap may be partly
   closed already. HMDA full is ~100M+ rows across years → SCOPE CALL for
   Chris on how many years.
3. `fed_dhs_hifld` — 500 rows of ONE layer; HIFLD has dozens of
   infrastructure layers. STEEL. Cheap per layer; needs a which-layers pick.
4. `fed_clinicaltrials` — 500 of ~500k studies. STEEL. Full API crawl:
   hours, cheap.

**Tier 2 — cheap completions, lesser keys:**
5. `fed_nsf_awards` — 125 of ~500k. 6. `fed_atf_ffl_locations` — 2,000
   (full FFL list is ~130k over years). 7. `fed_dol_ofccp_csal` — 2,000.
8. `fed_epa_envirofacts` — 5,000 rows of ONE program table (Envirofacts is a
   whole API family — scope pick). 9. `fed_bjs_data`, `intl_hudoc`,
   `intl_gdelt` (GDELT effectively unbounded — needs a scope statement, not
   a "fill").

**Tier 3 — verify-then-retire (probably NOT gaps):**
- `fed_sam_exclusions` (10k) — superseded by `FED_SAM_EXCLUSIONS_FULL_R2`
  (168,328) already landed. Retire the sample row/table.
- `fed_usaspending_bulk` (50k) — likely superseded by
  `FED_USASPENDING_CONTRACTS_FULL_R2` (93.2M). Verify column overlap, then
  retire.
- `fed_fec_api` (500) — FEC bulk family is fully landed (84.2M individual
  contributions etc.). Verify the API slice adds nothing, then retire.

**Tier 4 — strategic scope calls (Chris), not loads:**
- `fed_sec_edgar` (200 of millions of filings) — full EDGAR is a
  platform-sized commitment, not a backfill.
- The 7 international portal-catalog indexes (DE/CH/GR/ES/CL/CA/BD) — these
  are indexes OF other portals; value depends on the portal ruling.
- Small culture/history collections (Oyez, Rumsey, Densho, WPA narratives) —
  cheap, low graph value.

## Also in the depth ledger (from earlier tonight)

- `LIBRARY_RAW.RETIRED`: the two 990-efiler indexes at exactly 500,000 rows
  are the ONLY copies and are truncated (round-cap signature). Real gap.
- CMS Open Payments: newer July snapshot quarantined while June serves —
  re-pull queued (STATUS "your move").
- Old contracts table (20M, 300 cols) vs R2 (93M, 39 cols): R2 is NOT a
  superset — the 261-column transaction detail exists only in the truncated
  table. A true fix is a full re-pull at transaction grain with all columns —
  big job, scope call.
