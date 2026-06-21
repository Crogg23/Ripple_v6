# portal_recon — Wave 1: platform fingerprint

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
