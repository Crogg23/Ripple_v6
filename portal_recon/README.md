# portal_recon — catalog-of-catalogs (Wave 1 + Wave 2)

> **Wave 2 (dataset index) lives below** — jump to [Wave 2](#wave-2--dataset-index-harvest).
> Wave 1 (this section) figured out *which platform each portal runs*; Wave 2 opens
> each confirmed portal and harvests the *index of every dataset inside it*.

---

# Wave 1: platform fingerprint

**Goal:** for every open-data portal in the Catalog (`SOURCE_REGISTRY`, the ~321
"portal supercluster"), figure out **which platform it runs** — Socrata / CKAN /
ArcGIS Hub / OpenDataSoft / GeoNode / Junar / custom — so Wave 2 knows which reader
to point at each one.

**This wave does NOT harvest datasets.** Every probe is a count-only / metadata
endpoint (`limit=0`, `rows=0`, `?f=json`). Fingerprint only.

---

## Run it

```bash
# 0. fresh PAT must be live (see "Blocker" below)
set -a; source ../library-onboarding/.env; set +a

# prove the prober with zero Snowflake:
python fingerprint_portals.py --selftest

# inspect the registry's CATEGORY breakdown + which one it'd auto-pick:
python fingerprint_portals.py --distribution

# full run -> writes portal_recon_results.md (+ .json):
python fingerprint_portals.py

# Wave-1.5: retry only the UNKNOWNs (redirect-reprobe + CKAN subpaths + branding):
python reclaim.py
python reclaim.py --rebuild        # regenerate the report from JSON, no probing

# pin the category if auto-pick is off, or cap politeness:
python fingerprint_portals.py --category 'Open Data Portal'
python fingerprint_portals.py --budget 2
```

Output: **`portal_recon_results.md`** (summary headline + per-portal table) and
**`portal_recon_results.json`** (structured, for `--rebuild`).

---

## Status / results

Done. Pulled **194** portals (the 8 portal/open-data/meta CATEGORY tags — the
"~321 supercluster" doesn't reconstruct from any single column; 194 is the clean
platform-portal set). After the Wave-1.5 reclaim pass:

| Platform | Portals |
|---|---:|
| ArcGIS Hub | 40 |
| Socrata | 35 |
| CKAN | 25 |
| OpenDataSoft | 5 |
| UNKNOWN | 89 |

**Coverage: top-2 (ArcGIS + Socrata) = 39%, top-3 (+CKAN) = 52%, all detected =
105/194 (54%).** Those are the Wave-2 readers, by priority. The 89 UNKNOWN are
mostly bespoke national stacks (data.gouv.fr/uData, data.europa.eu/Piveau,
data.gov.cz) plus a few flagship portals registered at the wrong URL (NYC, Denver)
— registry hygiene, not a detection gap.

---

## Detection signatures (only asserted when an endpoint actually responds)

| Platform | Endpoint probed (count-only) | Confirmed by |
|---|---|---|
| Socrata | `/api/catalog/v1?limit=0` | `resultSetSize`+`results`, or `X-Socrata-*` header |
| CKAN | `/api/3/action/package_search?rows=0` | `{"success": true, "result": …}` |
| OpenDataSoft | `/api/v2/catalog/datasets?limit=0` | `total_count` / `nhits` |
| GeoNode | `/api/v2/` | `geonode` marker or GeoNode resource keys |
| Junar | `/api/v2/datastreams/?format=json` | body names `auth_key` / `junar` (401/403 ok) |
| ArcGIS Hub | `/data.json` | feed saturated with `arcgis.com` (backstop, runs last) |

Anything no endpoint confirms is **UNKNOWN** — never guessed.

## Politeness

- Short timeouts (4s connect / 6s read), **no retries**, normal identifying User-Agent.
- **Bounded reads** — every probe caps at 64 KB; we never download a full catalog.
- **Stop at first match** — a Socrata portal costs 1 request, CKAN 2, … only an
  unknown/custom portal spends the full budget.
- Budget default **6** (the six platforms). Strict "one or two requests" can't tell
  six platforms apart on custom domains; `--budget 2` reliably gets the headline
  Socrata/CKAN split but will mark more ArcGIS/ODS/GeoNode/Junar as UNKNOWN.

---

# Wave 2 — dataset index harvest

**Goal:** open each of the 105 platform-confirmed portals from Wave 1 and harvest the
**INDEX of every dataset inside it** — title, dataset ID, column/field names, row
count, last-updated. **Metadata only — nothing is downloaded or ingested**, nothing
touches `LIBRARY_RAW.LANDING`. (No Snowflake needed: input is the Wave-1 JSON,
output is files.)

Three readers, one per platform (priority order): **ArcGIS (40) · Socrata (35) ·
CKAN (25)** = 100 portals. (The 5 OpenDataSoft portals are out of scope for these
three readers.)

## Run it

```bash
# prove the ArcGIS reader on a few portals (the STEP-0 gut check):
python arcgis_reader.py --portals loc_asheville_open loc_dc_open loc_detroit_open

# each reader standalone:
python socrata_reader.py --limit 3
python ckan_reader.py --portals loc_pittsburgh_open st_ca_open

# full harvest (all three, parallel across hosts) -> writes the two outputs:
python harvest_index.py --workers 8 --ckan-enrich 200

# gently retry only the portals that errored/came back empty, merge into the index:
python harvest_index.py --reclaim --workers 4
```

## Outputs

- **`portal_datasets_index.json`** — the master asset: every dataset with all
  captured fields (compact JSON). It's ~360 MB, so it's **gitignored**; the
  committed copy is **`portal_datasets_index.json.gz`** (`gunzip -k` to restore the
  identical file).
- **`portal_datasets_index.md`** — human summary: totals, per-platform + per-portal
  breakdown, join-key counts, top-20 biggest portals, and the portals that failed.

## How each reader gets the index

| Platform | Endpoint | Per dataset we capture |
|---|---|---|
| **ArcGIS** | `hub.arcgis.com/utilities/domains/<host>` → `orgId`, then `hub.arcgis.com/api/v3/datasets?filter[orgId]=…` (JSON:API sparse fieldsets — ~17× smaller pages) | id, title, fields (columns), `recordCount`, `modified` |
| **Socrata** | `/api/catalog/v1?only=dataset&domains=<host>&scroll_id=…` (domain-scoped — the bare endpoint returns the *global federated* catalog; `scroll_id` pages past Socrata's 10k offset cap) | 4×4 id, title, `columns_field_name`, `updatedAt` (row count not exposed → `unknown`) |
| **CKAN** | `/api/3/action/package_search` (paginate the full index first), then a bounded `datastore_search?limit=0` enrichment for columns + row count | name (id), title, resources, `metadata_modified`; enriched: columns + `total` |

## Light join-key flag (STEP 3)

A cheap first signal, **not** the Wave-3 tagging: each dataset's column names are
tokenized (camelCase + non-alphanumerics) and matched against known join keys —
FIPS/GEOID, ZIP, lat/lon, EIN, NPI, NDC, CIK, UEI, LEI, NAICS, MMSI, country-ISO.
Whole-token matching avoids substring false positives (`ein` matches an `EIN`
column, never `protein`). Output is a boolean + which keys matched.

## Politeness (mandatory — these are public servers)

- **Within a portal:** sequential, paginated, 0.25s pause between requests, short
  timeouts (5s/20s), at most **one** retry (only on a network blip or 429/502/503/504).
- **Across portals:** parallel over **distinct hosts** only (no host ever sees
  concurrency) — it just cuts wall-clock time.
- **Caps:** ≤ 25,000 datasets/portal and a 300s wall-clock budget/portal, so one
  giant or slow portal can't run forever (capped/timed-out portals are flagged).
- **User-Agent:** a normal browser UA. Many of these public APIs sit behind
  Cloudflare, which 502s a custom bot UA even though the APIs are built for
  programmatic access — so we present a normal UA and stay good citizens through
  *rate*, never volume.

## Result (2026-06-21 run)

- **338,520 datasets indexed** across **96** live portals (100 attempted; 4 not
  reachable: 2 Wave-1-mislabeled ArcGIS domains, 1 empty org, 1 branding-only CKAN
  with no real API).
- **19,496 carry at least one known join key** (ZIP 11.1k · lat/lon 7.8k · FIPS
  4.4k lead). Columns captured for 78.7k, row counts for 45.2k — everything else is
  honestly `unknown`.
- Biggest boxes: the national CKAN aggregators (Australia/Canada/HDX/UK/Virginia all
  hit the 25k cap; their true totals run 33k–136k) and big ArcGIS county/city hubs.
