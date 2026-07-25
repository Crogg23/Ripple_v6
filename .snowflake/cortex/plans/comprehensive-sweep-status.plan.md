# Comprehensive Sweep: What's Left to Address

## Status Summary

| System | Health | Notes |
|--------|--------|-------|
| Connect discover | OK | 1,503 edges, running cleanly |
| Entity spine | OK | 21.9M entities, 16.2M golden, 2.3M multi-source |
| Terrain map | OK | Just rewritten, Vsauce-style |
| Heartbeat (link) | BROKEN | Never succeeded since creation |
| Heartbeat (reconcile) | BROKEN | Timing out |
| Heartbeat (measure) | OK | Last success 2026-07-12 |
| Leads | PARTIAL | 1,041 active leads; 1 of 7 specs references a dropped table |
| dbt | PARTIAL | 5 marts disabled |
| Serve / Reading Room | OK | Two Streamlit apps, functional |
| Tests | UNKNOWN | 33 test files, not recently run |
| Git | DIRTY | Terrain map rewrite + threshold change uncommitted |

---

## 1. BROKEN: Heartbeat Link Tier (Never Succeeded)

**The problem:** `connect/incremental.py` has a config guard that computes a fingerprint of NORM_RULES + DISPLAY_SPECS. When the stored fingerprint in CONNECT_WATERMARK doesn't match, it refuses to run (to prevent duplicate/orphan entities). The `link` tier has **never succeeded** — `last_success: "1970-01-01T00:00:00+00:00"`.

**Root cause:** Entity specs or normalize rules changed after `connect.incremental seed` last pinned the config. Every specs fix (GLEIF, CMS, etc.) since then has widened the drift.

**Fix:**
1. Run full spine reconcile: `python -m connect spine`
2. Re-pin config: `python -m connect.incremental seed`
3. Verify heartbeat link tier succeeds on next hourly tick

**Risk:** The full spine run takes ~20-30 min. No data loss risk — it's a full rebuild from KEYSET_LIVE.

---

## 2. BROKEN: Heartbeat Reconcile Tier (Timeout)

**The problem:** The `reconcile` tier runs the full `connect all` pipeline end-to-end. This now exceeds the server-side timeout (7800s = 2h10m) on the current warehouse.

**Options:**
- **(A)** Temporarily scale RIPPLE_WH to XL or 2XL for the reconcile run
- **(B)** Break `connect all` into sequential stages with their own timeout budgets (fingerprint, discover, spine, leads — each stage independently)
- **(C)** Add checkpointing so a killed run can resume from where it stopped

**Recommendation:** Option A is the quickest fix. Option B is the correct long-term solution (each stage is independent and fast enough for an M warehouse).

---

## 3. STALE: `banned_but_operating` Lead Spec

[connect/leads_specs.py](connect/leads_specs.py):64 references `FED_CMS_FACILITY_AFFILIATION`, which was dropped on 2026-07-20 (confirmed: not in INFORMATION_SCHEMA). 

**Impact:** The 10 existing `banned_but_operating` leads are frozen (receipt evidence preserved), but the job **cannot produce new leads**.

**Fix options:**
- Replace with `FED_CMS_NPPES` (same NPI key, has provider name/address but no CCN)
- Replace with a JOIN path: NPPES -> PECOS affiliation or open payments
- Disable the spec until a replacement source is identified

---

## 4. DISABLED: 5 dbt Marts

These are disabled in `dbt_project.yml` because their source data was never loaded or was removed:

| Mart | Reason |
|------|--------|
| `economics__fed_hhs_taggs` | Source not ingested |
| `economics__intl_ch_zefix` | Source not ingested |
| `economics__intl_gr_gemi` | Source not ingested |
| `justice__fed_doj_crt_cases` | Source not ingested |
| `regulation__fed_fdic_enforcement` | Source not ingested |

**Fix:** Either ingest the source data (each needs a load script), or remove the disabled marts if the sources aren't coming soon.

---

## 5. COVERAGE GAP: 137 Dark Tables (36% of row volume)

The terrain map now honestly shows that **137 of 242 tables** can't link to anything. The biggest:

| Table | Rows | Why Dark |
|-------|------|----------|
| NOAA AIS | 58M | Only NAME key, exceeds 2M threshold |
| FHFA NMDB | 19M | Only NAME key, exceeds 2M threshold |
| CFPB Complaints | 17M | Only NAME key, exceeds 2M threshold |
| EOIR Case Data | 12M | Only NAME key, exceeds 2M threshold |
| USGS Water | 6.6M | Only NAME key, exceeds 2M threshold |

**Why:** These tables only have NAME/ADDRESS keys (no hard IDs like EIN, NPI, UEI). At their row counts, fuzzy name matching would produce too many false positives without blocking.

**Long-term fix:** Implement blocking/LSH in discover.py — partition by state/ZIP first, then fuzzy-match within blocks. This is a significant engineering effort but would illuminate another ~110M rows.

**Short-term alternative:** Some of these tables (CFPB, EOIR) have ZIP codes that could yield GEO-tier connections if wired into the FIPS crosswalk. That's simpler than full blocking.

---

## 6. UNCOMMITTED: Git Status

The following changes from this session are uncommitted:
- `scripts/build_terrain_map.py` — complete Vsauce-style rewrite
- `connect/discover.py` — NAME_MAX_ROWS raised from 300K to 2M
- `outputs/terrain_map.html` — regenerated with new data

---

## Lower Priority (Not Broken, But Worth Noting)

### Tests not recently verified
33 test files exist, none marked skip. CI runs offline tests on push. Unknown whether all currently pass after recent specs changes.

### No bridge entities detected
BRIDGE_ENTITIES table has 0 rows. The terrain map says "No bridge entities detected yet." This is because the spine resolves within key types (NPI finds NPI matches, EIN finds EIN matches) — it doesn't currently detect a single entity spanning across key types (e.g., an NPI provider that's also an EIN organization).

### `explore.py` output is outdated
The interactive Plotly graph from `connect explore` was last regenerated before the threshold raise. Stale but not broken — the terrain map supersedes it.

### Portal expansion (338K potential sources)
The PORTAL_DATASET_INDEX has 338K potential sources that could be loaded via the portal harvester. This is the natural growth path for data volume.

---

## Recommended Priority Order

1. **Fix heartbeat link tier** — 5 minutes of work, unblocks incremental pipeline
2. **Commit current changes** — preserve the terrain map rewrite
3. **Repair banned_but_operating spec** — unblocks lead generation for that rule
4. **Fix reconcile timeout** — scale warehouse or split stages
5. **Run tests** — verify nothing broke from recent changes
6. **Dark table coverage** — significant effort, biggest payoff for data illumination
7. **Re-enable disabled marts** — requires source ingestion first

---

## Critical Files

- [connect/incremental.py](connect/incremental.py) — Config guard that blocks link tier (line 243)
- [connect/leads_specs.py](connect/leads_specs.py) — banned_but_operating spec with dropped table (line 64)
- [connect/discover.py](connect/discover.py) — NAME_MAX_ROWS threshold (line 35)
- [scripts/build_terrain_map.py](scripts/build_terrain_map.py) — Terrain map generator (just rewritten)
- [scripts/heartbeat.py](scripts/heartbeat.py) — Scheduled task orchestrator
